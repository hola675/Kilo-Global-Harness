param(
  [Parameter(Mandatory=$true)]
  [string]$Snapshot,
  [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
  [string]$Salida
)

$ErrorActionPreference='Stop'

if (!(Test-Path -LiteralPath $Snapshot)) { throw "Snapshot no encontrado: $Snapshot" }

$expectedPath = Join-Path $RepoRoot 'registry\dev-team-capability-matrix-v1.json'
if (!(Test-Path -LiteralPath $expectedPath)) { throw "Matriz no encontrada: $expectedPath" }

$snap = Get-Content -LiteralPath $Snapshot -Raw -Encoding UTF8 | ConvertFrom-Json
$expected = Get-Content -LiteralPath $expectedPath -Raw -Encoding UTF8 | ConvertFrom-Json

function Normalize-Tool([string]$Name) {
  if (!$Name) { return $null }
  $Name.Trim().ToLowerInvariant()
}

function Tool-Family([string]$Name) {
  $n = Normalize-Tool $Name
  if ($n -match 'context7') { return 'context7' }
  if ($n -match 'microsoft.*learn|learn.*microsoft') { return 'microsoft-learn' }
  if ($n -match 'serena') { return 'serena' }
  if ($n -match 'codebase.*memory|memory.*codebase') { return 'codebase-memory' }
  if ($n -match 'github') { return 'github' }
  if ($n -match 'cloudflare') { return 'cloudflare-api' }
  if ($n -match 'playwright|kilo-playwright') { return 'kilo-playwright' }
  if ($n -match 'chrome.*devtools|devtools.*chrome') { return 'chrome-devtools' }
  if ($n -match 'sentry') { return 'sentry' }
  if ($n -match 'snyk') { return 'snyk' }
  if ($n -match 'postman') { return 'postman' }
  if ($n -match 'ida') { return 'ida' }
  if ($n -match 'imagegen|image_gen') { return 'imagegen' }
  if ($n -match 'kilo.*platform|platform.*kilo') { return 'kilo-platform' }
  return $null
}

$plans = foreach ($p in $expected.roles.PSObject.Properties) {
  $agent=$p.Name
  $profile=$p.Value
  $actual = @($snap.agents | Where-Object Agent -eq $agent | Select-Object -First 1)
  $visible = if ($actual.Count) { @($actual[0].visible_tools | ForEach-Object { Normalize-Tool $_ }) } else { @() }

  $nativePrimary=@($profile.native_primary | ForEach-Object { Normalize-Tool $_ })
  $nativeConditional=@($profile.native_conditional | ForEach-Object { Normalize-Tool $_ })
  $mcpPrimary=@($profile.mcp_primary | ForEach-Object { Normalize-Tool $_ })
  $mcpConditional=@($profile.mcp_conditional | ForEach-Object { Normalize-Tool $_ })

  $families=@($visible | ForEach-Object { Tool-Family $_ } | Where-Object { $_ } | Sort-Object -Unique)

  $missingNative=@($nativePrimary | Where-Object { $_ -notin $visible })
  $missingMcp=@($mcpPrimary | Where-Object { $_ -notin $families })

  $review=@()
  foreach($tool in $visible){
    $fam=Tool-Family $tool
    $knownNative=($tool -in $nativePrimary) -or ($tool -in $nativeConditional)
    $knownMcp=$fam -and (($fam -in $mcpPrimary) -or ($fam -in $mcpConditional))
    if(!$knownNative -and !$knownMcp){
      $review += $tool
    }
  }

  [ordered]@{
    agent=$agent
    snapshot_present=[bool]$actual.Count
    keep_visible=@($visible | Where-Object {
      ($_ -in $nativePrimary) -or
      ($_ -in $nativeConditional) -or
      ((Tool-Family $_) -in $mcpPrimary) -or
      ((Tool-Family $_) -in $mcpConditional)
    } | Sort-Object -Unique)
    missing_primary_native=$missingNative
    missing_primary_mcp_families=$missingMcp
    review_unexpected=@($review | Sort-Object -Unique)
    decision='NO_AUTO_APPLY'
  }
}

$report=[ordered]@{
  schema='dev-team-tool-plan/1'
  generated_at=(Get-Date).ToString('o')
  source_snapshot=$Snapshot
  mode='PLAN_ONLY'
  warnings=@(
    'No cambia ACL ni kilo.jsonc.',
    'Una tool visible no implica permiso seguro.',
    'Una tool faltante no autoriza bypass.',
    'review_unexpected requiere clasificacion humana/estatica antes de cualquier allow.'
  )
  agents=@($plans)
}

$json=$report | ConvertTo-Json -Depth 10
if($Salida){
  $parent=Split-Path -Parent $Salida
  if($parent -and !(Test-Path -LiteralPath $parent)){ New-Item -ItemType Directory -Path $parent -Force | Out-Null }
  Set-Content -LiteralPath $Salida -Value $json -Encoding UTF8
  Write-Host "Plan guardado: $Salida" -ForegroundColor Green
}
$json
