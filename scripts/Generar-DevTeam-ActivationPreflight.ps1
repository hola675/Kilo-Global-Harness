param(
  [ValidateSet('PASS','FAIL','UNKNOWN')]
  [string]$SourceCiStatus = 'UNKNOWN',
  [string]$RuntimeSnapshot,
  [string]$SkillEvalReport,
  [string]$RaizUsuario,
  [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
  [string]$Salida
)

$ErrorActionPreference='Stop'

$wavesPath=Join-Path $RepoRoot 'registry\dev-team-activation-waves-v1.json'
$matrixPath=Join-Path $RepoRoot 'registry\dev-team-capability-matrix-v1.json'
$mcpPath=Join-Path $RepoRoot 'registry\dev-team-mcp-exact-inventory-v1.json'
$skillsMatrixPath=Join-Path $RepoRoot 'registry\dev-team-skills-matrix-v1.proposal.json'

foreach($path in @($wavesPath,$matrixPath,$mcpPath,$skillsMatrixPath)){
  if(!(Test-Path -LiteralPath $path)){ throw "Archivo requerido ausente: $path" }
}

$waves=Get-Content -LiteralPath $wavesPath -Raw -Encoding UTF8 | ConvertFrom-Json
$matrix=Get-Content -LiteralPath $matrixPath -Raw -Encoding UTF8 | ConvertFrom-Json
$mcp=Get-Content -LiteralPath $mcpPath -Raw -Encoding UTF8 | ConvertFrom-Json
$skillsMatrix=Get-Content -LiteralPath $skillsMatrixPath -Raw -Encoding UTF8 | ConvertFrom-Json

# V1.1: evidencia SHA256 solo-lectura con las mismas rutas del instalador vigente.
$homeRoot=if([string]::IsNullOrWhiteSpace($RaizUsuario)){
  [IO.Path]::GetFullPath($HOME)
}else{
  if(![IO.Path]::IsPathFullyQualified($RaizUsuario)){ throw 'RaizUsuario debe ser absoluta.' }
  [IO.Path]::GetFullPath($RaizUsuario)
}

# V1.2: clasificacion de deriva; NO equivale a smoke ni permiso runtime.
# Unicamente interpreta archivos de texto UTF-8; una diferencia de formato sigue FAIL.
function Get-DriftKind {
  param([string]$Source,[string]$Installed)
  try {
    $utf8=[Text.UTF8Encoding]::new($false,$true)
    $a=$utf8.GetString([IO.File]::ReadAllBytes($Source))
    $b=$utf8.GetString([IO.File]::ReadAllBytes($Installed))
  }catch{
    return 'NOT_VALID_UTF8_OR_UNREADABLE'
  }
  if($a -ceq $b){ return 'UNKNOWN_BYTE_DIFFERENCE' }
  $withoutBomA=$a.TrimStart([char]0xFEFF)
  $withoutBomB=$b.TrimStart([char]0xFEFF)
  if($withoutBomA -ceq $withoutBomB){ return 'UTF8_BOM_ONLY' }
  $normA=$withoutBomA.Replace("`r`n","`n").Replace("`r","`n")
  $normB=$withoutBomB.Replace("`r`n","`n").Replace("`r","`n")
  if($normA -ceq $normB){ return 'EOL_OR_BOM_ONLY' }
  $stripA=[regex]::Replace($normA,'(?m)[ \t]+(?=\n|$)','')
  $stripB=[regex]::Replace($normB,'(?m)[ \t]+(?=\n|$)','')
  if($stripA -ceq $stripB){ return 'TRAILING_WHITESPACE_ONLY' }
  return 'CONTENT_CHANGED'
}

function Test-HashPairs {
  param([object[]]$Pairs,[int]$Expected)
  $missing=[System.Collections.Generic.List[string]]::new()
  $different=[System.Collections.Generic.List[string]]::new()
  $unreadable=[System.Collections.Generic.List[string]]::new()
  $details=[System.Collections.Generic.List[object]]::new()
  $matched=0
  foreach($pair in $Pairs){
    $name=[string]$pair.name
    if(!(Test-Path -LiteralPath $pair.source -PathType Leaf)){
      $missing.Add("$($name):source")
      continue
    }
    if(!(Test-Path -LiteralPath $pair.target -PathType Leaf)){
      $missing.Add("$($name):installed")
      continue
    }
    try{
      $sourceHash=(Get-FileHash -LiteralPath $pair.source -Algorithm SHA256).Hash
      $targetHash=(Get-FileHash -LiteralPath $pair.target -Algorithm SHA256).Hash
      if($sourceHash -ceq $targetHash){$matched++}
      else{
        $different.Add($name)
        $details.Add([pscustomobject]@{
          name=$name
          kind=(Get-DriftKind -Source $pair.source -Installed $pair.target)
          source_bytes=(Get-Item -LiteralPath $pair.source).Length
          installed_bytes=(Get-Item -LiteralPath $pair.target).Length
        })
      }
    }catch{$unreadable.Add($name)}
  }
  return [pscustomobject]@{
    status=if($Pairs.Count -eq $Expected -and $matched -eq $Expected){'PASS'}else{'FAIL'}
    expected=$Expected
    matched=$matched
    missing=@($missing)
    different=@($different)
    unreadable=@($unreadable)
    drift_details=@($details)
  }
}

$roles=@($matrix.roles.PSObject.Properties.Name)
if($roles.Count -ne 11 -or @($roles | Select-Object -Unique).Count -ne 11){
  throw 'La matriz canonica no contiene exactamente 11 agentes unicos.'
}
$agentPairs=@(foreach($id in $roles){
  if($id -notmatch '^vx-dev-[a-z0-9-]+$'){throw "ID agente invalido: $id"}
  $relative=if($id -eq 'vx-dev-team'){"agents/$id.md"}else{"runtime/dev-team-v2r/agents/$id.md"}
  [pscustomobject]@{
    name=$id
    source=Join-Path $RepoRoot $relative
    target=Join-Path $homeRoot (".config/kilo/agents/$id.md")
  }
})
$skillEntries=@($skillsMatrix.dev_team_pack.skills)
$skillIds=@($skillEntries | ForEach-Object {[string]$_.id})
if($skillIds.Count -ne 18 -or @($skillIds | Select-Object -Unique).Count -ne 18){
  throw 'El pack V1 no contiene exactamente 18 skills unicas.'
}
$skillPairs=@(foreach($entry in $skillEntries){
  $id=[string]$entry.id
  if($id -notmatch '^vx-dev-[a-z0-9-]+$'){throw "ID skill invalido: $id"}
  $relative="runtime/dev-team-v2r/skills/$id/SKILL.md"
  if(([string]$entry.source).Replace('\','/') -cne $relative){
    throw "Fuente manifest skill incoherente: $id"
  }
  [pscustomobject]@{
    name=$id
    source=Join-Path $RepoRoot $relative
    target=Join-Path $homeRoot (".kilo/skills/$id/SKILL.md")
  }
})
$agentHashCheck=Test-HashPairs -Pairs $agentPairs -Expected 11
$skillHashCheck=Test-HashPairs -Pairs $skillPairs -Expected 18

$runtime=$null
if($RuntimeSnapshot){
  if(!(Test-Path -LiteralPath $RuntimeSnapshot)){ throw "Runtime snapshot ausente: $RuntimeSnapshot" }
  $runtime=Get-Content -LiteralPath $RuntimeSnapshot -Raw -Encoding UTF8 | ConvertFrom-Json
}

$evals=$null
if($SkillEvalReport){
  if(!(Test-Path -LiteralPath $SkillEvalReport)){ throw "Skill eval report ausente: $SkillEvalReport" }
  $evals=Get-Content -LiteralPath $SkillEvalReport -Raw -Encoding UTF8 | ConvertFrom-Json
}

$runtimeObserved=0
if($runtime){
  $runtimeObserved=@($runtime.agents | Where-Object { $_.capture_status -in @('OBSERVED','VISIBLE_LIST') }).Count
}

$evalComplete=$false
if($evals){
  $evalComplete=($evals.status -eq 'COMPLETE' -and [int]$evals.totals.pending -eq 0)
}

$verifiedMcpIds=0
foreach($server in $mcp.servers.PSObject.Properties){
  $verifiedMcpIds += @($server.Value.runtime_verified_exact).Count
}

$checks=[ordered]@{
  source_ci_pass=($SourceCiStatus -eq 'PASS')
  canonical_roles_11=(@($matrix.roles.PSObject.Properties).Count -eq 11)
  runtime_agent_hash_match=($agentHashCheck.status -eq 'PASS')
  skill_source_hash_18_of_18=($skillHashCheck.status -eq 'PASS')
  runtime_snapshot_11_of_11=($runtimeObserved -eq 11)
  skill_eval_report_complete=$evalComplete
  runtime_verified_mcp_id_count=$verifiedMcpIds
  operator_approval=$false
}

$plans=@()
foreach($wave in $waves.waves){
  $blocking=New-Object System.Collections.Generic.List[string]
  foreach($req in $wave.prerequisites){
    switch($req){
      'source_ci_pass' { if(!$checks.source_ci_pass){$blocking.Add($req)} }
      'runtime_agent_hash_match' { if(!$checks.runtime_agent_hash_match){$blocking.Add($req)} }
      'skill_source_hash_18_of_18' { if(!$checks.skill_source_hash_18_of_18){$blocking.Add($req)} }
      'runtime_visible_snapshot_11_of_11' { if(!$checks.runtime_snapshot_11_of_11){$blocking.Add($req)} }
      'skill_eval_report_complete' { if(!$checks.skill_eval_report_complete){$blocking.Add($req)} }
      'operator_approval' { $blocking.Add($req) }
      default { $blocking.Add($req) }
    }
  }
  $plans += [ordered]@{
    id=$wave.id
    readiness=if($blocking.Count -eq 1 -and $blocking[0] -eq 'operator_approval'){'READY_FOR_OPERATOR_REVIEW'}else{'BLOCKED'}
    blockers=@($blocking)
    action='NO_AUTO_APPLY'
  }
}

$report=[ordered]@{
  schema='dev-team-activation-preflight/1'
  generated_at=(Get-Date).ToString('o')
  mode='PLAN_ONLY'
  checks=$checks
  hash_evidence=[ordered]@{
    scope='FILE_SHA256_ONLY_NOT_RUNTIME_BEHAVIOR'
    agents=$agentHashCheck
    skills=$skillHashCheck
  }
  waves=$plans
  invariant='This preflight never applies runtime changes and never grants operator approval.'
}

$json=$report | ConvertTo-Json -Depth 10
if($Salida){
  $parent=Split-Path -Parent $Salida
  if($parent -and !(Test-Path -LiteralPath $parent)){New-Item -ItemType Directory -Path $parent -Force | Out-Null}
  Set-Content -LiteralPath $Salida -Value $json -Encoding UTF8
  Write-Host "Preflight guardado: $Salida" -ForegroundColor Green
}
$json
