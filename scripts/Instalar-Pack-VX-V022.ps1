#Requires -Version 7.0
<#
.SYNOPSIS
  Instala Pack VX 0.2.2 en Kilo global Windows con DPAPI y preflight fail-closed.
#>
[CmdletBinding()]
param(
  [ValidateSet('Diagnostico','Simular','Aplicar','Verificar')]
  [string]$Modo = 'Diagnostico',
  [string]$RaizUsuario = $HOME,
  [switch]$ConfirmarMigracion,
  [switch]$ConfirmarKiloCerrado
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if ($env:OS -ne 'Windows_NT') { throw 'Requiere Windows y DPAPI.' }
if (![IO.Path]::IsPathFullyQualified($RaizUsuario)) { throw 'RaizUsuario debe ser absoluta.' }
$homeRoot = [IO.Path]::GetFullPath($RaizUsuario)
$repo = Split-Path $PSScriptRoot -Parent
$bootstrap = Join-Path $PSScriptRoot 'vx_pack_bootstrap.py'
$registryPath = Join-Path $repo 'registry/vx-agent-registry-v4.json'
$catalogPath = Join-Path $repo 'registry/vx-mcp-catalog-v1.json'
foreach ($file in @($bootstrap,$registryPath,$catalogPath)) {
  if (!(Test-Path -LiteralPath $file -PathType Leaf)) { throw "Falta archivo: $file" }
}
# Get-Command devuelve TODOS los python.exe de PATH; seleccionar solo el primero.
$python = [string](Get-Command python -CommandType Application -ErrorAction Stop |
  Select-Object -First 1 -ExpandProperty Source)
if ([string]::IsNullOrWhiteSpace($python) -or !(Test-Path -LiteralPath $python -PathType Leaf)) {
  throw 'Python ejecutable no encontrado; revisar PATH.'
}
$registry = Get-Content -LiteralPath $registryPath -Raw -Encoding UTF8 | ConvertFrom-Json
$catalog = Get-Content -LiteralPath $catalogPath -Raw -Encoding UTF8 | ConvertFrom-Json
if (@($registry.pack.owned_agents).Count -ne 12 -or @($registry.pack.owned_skills).Count -ne 31 -or
    @($catalog.candidates).Count -ne 6 -or
    @($catalog.candidates | Where-Object { $_.enabled_by_default -ne $false }).Count -ne 0) {
  throw 'Pack incompatible: requiere 12 agentes, 31 skills y 6 MCP deshabilitados.'
}
function Invoke-VX([string]$Mode) {
  & $python -I $bootstrap --mode $Mode --home $homeRoot
  if ($LASTEXITCODE -ne 0) { throw "Bootstrap $Mode falló (código $LASTEXITCODE)." }
}
if ($Modo -eq 'Verificar') {
  Invoke-VX 'verify'
  Write-Host '[PASS] Archivos del Pack. Validación de Kilo runtime pendiente.' -ForegroundColor Green
  return
}
$raw = & $python -I $bootstrap --mode simulate --home $homeRoot
if ($LASTEXITCODE -ne 0) { throw 'Preflight falló. NO se instaló.' }
$plan = ($raw -join [Environment]::NewLine) | ConvertFrom-Json
if ([int]$plan.agents -ne 12 -or [int]$plan.skills -ne 31 -or [int]$plan.mcp_changes -ne 0 -or
    @($plan.mcp_inventory.catalog).Count -ne 6) {
  throw 'Inventario de simulación inesperado. NO se instaló.'
}
Write-Host "VX PACK 0.2.2 — $Modo | HOME: $homeRoot" -ForegroundColor Cyan
Write-Host "Objetivo: $($plan.agents) agentes, $($plan.skills) skills, 6 MCP solo catálogo."
Write-Host "Archivos: $($plan.files); no reescribe JSONC ni credenciales."
if (@($plan.blockers).Count -gt 0) {
  Write-Warning 'Preflight BLOQUEADO. Sin cambios en HOME.'
  foreach ($reason in @($plan.blockers)) { Write-Warning ([string]$reason) }
  if ($Modo -eq 'Aplicar') { throw 'Instalación detenida por blockers.' }
}
if ($Modo -eq 'Diagnostico') { Invoke-VX 'diagnose'; return }
if ($Modo -eq 'Simular') {
  foreach ($target in @($plan.candidate_paths)) { Write-Output "[DESTINO] $target" }
  Write-Host 'SIMULACION sin cambios.' -ForegroundColor Green
  return
}
if (!$ConfirmarMigracion -or !$ConfirmarKiloCerrado) {
  throw 'Aplicar requiere -ConfirmarMigracion -ConfirmarKiloCerrado.'
}
$active = @(Get-Process -Name 'Code','VSCodium','kilo-desktop' -ErrorAction SilentlyContinue)
if ($active.Count -gt 0) {
  throw 'Cierra VS Code/VSCodium/Kilo antes de reemplazar el perfil global.'
}
Write-Host 'Aplicar: snapshot DPAPI antes de sustituir archivos globales.' -ForegroundColor Yellow
& $python -I $bootstrap --mode apply --home $homeRoot --confirm-migration
if ($LASTEXITCODE -ne 0) { throw 'Apply falló; revisar backups y blockers antes de reintentar.' }
Invoke-VX 'verify'
Write-Host '[PASS] Archivos VX instalados. Reinicia Kilo, /reload y prueba ACL/delegación.' -ForegroundColor Green
