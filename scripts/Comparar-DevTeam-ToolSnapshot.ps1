param(
  [Parameter(Mandatory=$true)]
  [string]$Snapshot,
  [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
  [string]$Salida
)

$ErrorActionPreference='Stop'
if (!(Test-Path -LiteralPath $Snapshot)) { throw "Snapshot no encontrado: $Snapshot" }

$expectedPath = Join-Path $RepoRoot 'registry\dev-team-capability-matrix-v1.json'
if (!(Test-Path -LiteralPath $expectedPath)) { throw "Matriz esperada no encontrada: $expectedPath" }

$snap = Get-Content -LiteralPath $Snapshot -Raw -Encoding UTF8 | ConvertFrom-Json
$expected = Get-Content -LiteralPath $expectedPath -Raw -Encoding UTF8 | ConvertFrom-Json

$rows = foreach ($p in $expected.roles.PSObject.Properties) {
  $agent=$p.Name
  $profile=$p.Value
  $actual = @($snap.agents | Where-Object Agent -eq $agent | Select-Object -First 1)
  $visible = if ($actual.Count) { @($actual[0].visible_tools) } else { @() }

  $nativeExpected=@($profile.native_primary)
  $mcpExpected=@($profile.mcp_primary)

  [pscustomobject]@{
    Agent=$agent
    SnapshotPresent=[bool]$actual.Count
    NativeExpected=$nativeExpected
    MCPFamiliesExpected=$mcpExpected
    VisibleCount=$visible.Count
    MissingNative=@($nativeExpected | Where-Object { $_ -notin $visible })
    UnexpectedVisible=@($visible | Where-Object {
      $tool=$_
      ($tool -notin $nativeExpected) -and
      -not (@($profile.native_conditional) -contains $tool)
    })
  }
}

$report=[ordered]@{
  schema='dev-team-tool-runtime-diff/1'
  compared_at=(Get-Date).ToString('o')
  source_snapshot=$Snapshot
  warning='MCP family matching requiere normalizacion por prefijo/tool ID. UnexpectedVisible es diagnostico, no fallo automatico.'
  agents=@($rows)
}

$json=$report | ConvertTo-Json -Depth 8
if ($Salida) {
  $parent=Split-Path -Parent $Salida
  if ($parent -and !(Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
  Set-Content -LiteralPath $Salida -Value $json -Encoding UTF8
  Write-Host "Comparacion guardada: $Salida" -ForegroundColor Green
}
$json
