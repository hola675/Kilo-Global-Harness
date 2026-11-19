param(
  [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
  [string]$Salida = (Join-Path (Split-Path -Parent $PSScriptRoot) 'artifacts\dev-team-runtime-visible-tools.json')
)

$ErrorActionPreference='Stop'
$template = Join-Path $RepoRoot 'registry\dev-team-runtime-visible-tools.template.json'
if (!(Test-Path -LiteralPath $template)) { throw "Template ausente: $template" }
$destDir=Split-Path -Parent $Salida
if($destDir -and !(Test-Path -LiteralPath $destDir)){ New-Item -ItemType Directory -Path $destDir -Force | Out-Null }
Copy-Item -LiteralPath $template -Destination $Salida -Force
Write-Host "Snapshot template creado: $Salida" -ForegroundColor Green
Write-Host "Estado: PENDING_OPERATOR_RUNTIME. Rellena solo con evidencia visible de Kilo; no invoques tools." -ForegroundColor Yellow
