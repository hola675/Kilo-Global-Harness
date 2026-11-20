#Requires -Version 5.1
<#
.SYNOPSIS
  Auditoria y limpieza de ramas: main unica local y remota, con tags de archivo.
.DESCRIPTION
  V2.0.0 (2026-11-19) | PLAN_ONLY por defecto.
  No toca runtime Kilo, ACL, MCP, agents, skills ni kilo.jsonc.
  Requiere main sincronizada, worktree limpio, cero PR abiertas y confirmacion.
  Archiva cada tip como tag remoto anotado antes de borrar su rama.
.CHANGELOG
  2.0.0 - Preservacion de refs, verificaciones de SHA y retiro main-only.
#>
[CmdletBinding()]
param([switch]$Aplicar,[string]$Confirmacion='')
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
function Assert-Git([string]$Stage){if($LASTEXITCODE -ne 0){throw "Git fallo: $Stage (exit=$LASTEXITCODE)"}}
function Remote-Sha([string]$Ref){
  $lines=@(& git ls-remote origin $Ref);Assert-Git "ls-remote $Ref"
  if($lines.Count -eq 0){return ''}
  if($lines.Count -ne 1){throw "Referencia remota ambigua: $Ref"}
  return [string](($lines[0] -split '\s+')[0])
}
function Local-Sha([string]$Ref){
  $sha=(& git rev-parse --verify --quiet $Ref 2>$null | Out-String).Trim()
  if($LASTEXITCODE -ne 0){return ''}
  return $sha
}
function Open-PR-Branches {
  $url='https://api.github.com/repos/hola675/Kilo-Global-Harness/pulls?state=open&per_page=100'
  try {
    # PS 5.1 devuelve JSON arrays como un solo objeto: enumerar explicitamente.
    $response=Invoke-RestMethod -Uri $url -Headers @{'User-Agent'='Kilo-Branch-Cleanup-V2';Accept='application/vnd.github+json'} -Method Get
  }catch{
    if(!(Get-Command gh -ErrorAction SilentlyContinue)){throw 'GitHub PR API no disponible; no borrar.'}
    $json=(& gh api --method GET repos/hola675/Kilo-Global-Harness/pulls -f state=open -f per_page=100 | Out-String)
    Assert-Git 'gh api pulls'
    $response=$json | ConvertFrom-Json
  }
  $prs=[System.Collections.Generic.List[object]]::new()
  foreach($pr in $response){if($null -ne $pr){[void]$prs.Add($pr)}}
  if($prs.Count -ge 100){throw 'PR paginadas: inventario no completo.'}
  return @($prs | Where-Object {
    $null -ne $_.head -and $null -ne $_.head.repo -and
    $_.head.repo.full_name -eq 'hola675/Kilo-Global-Harness'
  } | ForEach-Object {$_.head.ref})
}
function Archive-Sha([string]$Tag,[string]$Sha){
  if($Tag -notmatch '^archive/(?:remote|local)/[A-Za-z0-9._/-]+$' -or $Sha -notmatch '^[a-f0-9]{40}$'){
    throw 'Nombre de tag o SHA no valido.'
  }
  $ref="refs/tags/$Tag"
  $remote=Remote-Sha "$ref^{}"
  if($remote){if($remote -ne $Sha){throw "Tag remoto conflictivo: $Tag"};return}
  $local=Local-Sha "$ref^{}"
  if($local -and $local -ne $Sha){throw "Tag local conflictivo: $Tag"}
  if(!$local){
    & git tag -a $Tag $Sha -m "Archive $Tag before branch retirement"
    Assert-Git "git tag $Tag"
  }
  & git push origin "$($ref):$ref"
  Assert-Git "push archive $Tag"
  if((Remote-Sha "$ref^{}") -ne $Sha){throw "Fallo verificando tag $Tag"}
}
if($Aplicar -and $Confirmacion -cne 'ARCHIVAR_Y_LIMPIAR_WORK'){
  throw 'Requiere -Aplicar -Confirmacion ARCHIVAR_Y_LIMPIAR_WORK'
}
$origin=(& git remote get-url origin | Out-String).Trim(); Assert-Git 'remote origin'
if($origin -notmatch '^(?:https://github\.com/|git@github\.com:|ssh://git@github\.com/)hola675/Kilo-Global-Harness(?:\.git)?/?$'){
  throw "Origen Git incorrecto: $origin"
}
$current=(& git branch --show-current | Out-String).Trim();Assert-Git 'rama local'
& git fetch origin --prune;Assert-Git 'fetch'
$base=Local-Sha 'refs/remotes/origin/main'
if(!$base -or $base -ne (Remote-Sha 'refs/heads/main')){throw 'origin/main no se pudo fijar.'}
$open=@(Open-PR-Branches)
$remoteRefs=@(& git for-each-ref '--format=%(refname:strip=3)|%(objectname)' 'refs/remotes/origin/')
Assert-Git 'inventario remoto'
$localRefs=@(& git for-each-ref '--format=%(refname:strip=2)|%(objectname)' 'refs/heads/')
Assert-Git 'inventario local'
$remotePlan=@(foreach($line in $remoteRefs){
  if(!$line){continue}
  $p=$line -split '\|',2
  if($p[0] -in @('main','HEAD')){continue}
  [pscustomobject]@{Scope='REMOTE';Branch=$p[0];SHA=$p[1];Archive="archive/remote/$($p[0])";Status=$(if($p[0] -in $open){'HOLD_OPEN_PR'}else{'ARCHIVE_THEN_DELETE'})}
})
$localPlan=@(foreach($line in $localRefs){
  if(!$line){continue}
  $p=$line -split '\|',2
  if($p[0] -eq 'main'){continue}
  [pscustomobject]@{Scope='LOCAL';Branch=$p[0];SHA=$p[1];Archive="archive/local/$($p[0])";Status=$(if($p[0] -eq $current){'HOLD_CURRENT'}else{'ARCHIVE_THEN_DELETE'})}
})
$plan=@($remotePlan)+@($localPlan)
$folder=Join-Path ([IO.Path]::GetTempPath()) 'Kilo-Global-Harness'
New-Item -ItemType Directory -Force -Path $folder | Out-Null
$csv=Join-Path $folder ('branch-cleanup-v2-'+(Get-Date -Format 'yyyyMMdd-HHmmss')+'.csv')
$plan | Export-Csv -LiteralPath $csv -NoTypeInformation -Encoding UTF8
$plan | Format-Table Scope,Branch,Status,Archive -AutoSize | Out-Host
Write-Host "PLAN: remotas=$($remotePlan.Count) locales=$($localPlan.Count); CSV=$csv"
if(!$Aplicar){Write-Host 'PLAN_ONLY: no tags ni borrados.';return}
if($current -ne 'main'){throw 'Aplicar solo desde main local.'}
if((Local-Sha 'refs/heads/main') -ne $base){throw 'main local no sincronizada.'}
if(@(& git status --porcelain).Count -gt 0){throw 'Worktree no limpio.'}
if($open.Count -gt 0){throw "PR abiertas: $($open -join ', '). No borrar."}
if((Remote-Sha 'refs/heads/main') -ne $base){throw 'main remoto cambio; reauditar.'}
$deletedRemote=0;$deletedLocal=0;$skipped=0
foreach($item in $remotePlan){
  $ref="refs/heads/$($item.Branch)"
  if((Remote-Sha $ref) -ne $item.SHA){Write-Warning "Cambio remoto $ref";$skipped++;continue}
  try{
    Archive-Sha -Tag $item.Archive -Sha $item.SHA
    & git push "--force-with-lease=$($ref):$($item.SHA)" origin ":$ref"
    Assert-Git "retiro remoto $ref"
    $deletedRemote++
  }catch{Write-Warning "No se elimino $ref : $_";$skipped++}
}
& git fetch origin --prune;Assert-Git 'prune'
foreach($item in $localPlan){
  if((Local-Sha "refs/heads/$($item.Branch)") -ne $item.SHA){Write-Warning "Cambio local $($item.Branch)";$skipped++;continue}
  try{
    Archive-Sha -Tag $item.Archive -Sha $item.SHA
    # Git bloquea borrar branches usadas por otros worktrees.
    & git branch -D -- $item.Branch
    Assert-Git "retiro local $($item.Branch)"
    $deletedLocal++
  }catch{Write-Warning "No se elimino local $($item.Branch) : $_";$skipped++}
}
$remainingRemote=@(& git ls-remote --heads origin);Assert-Git 'verificacion remoto'
$nonMain=@($remainingRemote | Where-Object {$_ -notmatch '\srefs/heads/main$'})
$remainingLocal=@(& git for-each-ref '--format=%(refname:strip=2)' refs/heads/ | Where-Object {$_ -ne 'main'})
Write-Host "RESULTADO: remoto_eliminadas=$deletedRemote local_eliminadas=$deletedLocal omitidas=$skipped remoto_restantes=$($nonMain.Count) local_restantes=$($remainingLocal.Count)"
if($nonMain.Count -eq 0 -and $remainingLocal.Count -eq 0){
  Write-Host 'PASS: solo main local/remota; historial recuperable bajo archive/* tags.' -ForegroundColor Green
}else{Write-Warning 'No se alcanzo main-only. Revisar PR, worktrees y tags.'}
