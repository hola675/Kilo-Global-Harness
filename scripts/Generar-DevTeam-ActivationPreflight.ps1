param(
  [ValidateSet('PASS','FAIL','UNKNOWN')]
  [string]$SourceCiStatus = 'UNKNOWN',
  [string]$RuntimeSnapshot,
  [string]$SkillEvalReport,
  [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
  [string]$Salida
)

$ErrorActionPreference='Stop'

$wavesPath=Join-Path $RepoRoot 'registry\dev-team-activation-waves-v1.json'
$matrixPath=Join-Path $RepoRoot 'registry\dev-team-capability-matrix-v1.json'
$mcpPath=Join-Path $RepoRoot 'registry\dev-team-mcp-exact-inventory-v1.json'

foreach($path in @($wavesPath,$matrixPath,$mcpPath)){
  if(!(Test-Path -LiteralPath $path)){ throw "Archivo requerido ausente: $path" }
}

$waves=Get-Content -LiteralPath $wavesPath -Raw -Encoding UTF8 | ConvertFrom-Json
$matrix=Get-Content -LiteralPath $matrixPath -Raw -Encoding UTF8 | ConvertFrom-Json
$mcp=Get-Content -LiteralPath $mcpPath -Raw -Encoding UTF8 | ConvertFrom-Json

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
