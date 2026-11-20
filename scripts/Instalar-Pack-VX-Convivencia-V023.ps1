#Requires -Version 7.0
<#
.SYNOPSIS
  VX Pack 0.2.3: instalación GLOBAL por convivencia con agentes inline y skills de terceros.
.DESCRIPTION
  No borra ni reescribe kilo.jsonc, MCP o skills externas. Backup de destinos VX cifrado DPAPI.
  Exige preflight sin colisiones, Kilo cerrado y autorización explícita.
#>
[CmdletBinding()]
param(
  [ValidateSet('Diagnostico','Simular','Aplicar','Verificar','Restaurar')]
  [string]$Modo = 'Diagnostico',
  [string]$RaizUsuario = $HOME,
  [switch]$ConfirmarConvivencia,
  [switch]$ConfirmarKiloCerrado,
  [switch]$ConfirmarRestauracion,
  [string]$CarpetaRespaldo
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
if ($env:OS -ne 'Windows_NT') { throw 'Solo Windows con DPAPI.' }
if (![IO.Path]::IsPathFullyQualified($RaizUsuario)) { throw 'RaizUsuario debe ser absoluta.' }
$homeRoot=[IO.Path]::GetFullPath($RaizUsuario)
$impl=Join-Path $PSScriptRoot 'vx_pack_coexist_v023.py'
if (!(Test-Path -LiteralPath $impl -PathType Leaf)) { throw 'No existe el motor de convivencia.' }
$python=[string](Get-Command python -CommandType Application -ErrorAction Stop |
  Select-Object -First 1 -ExpandProperty Source)
if ([string]::IsNullOrWhiteSpace($python) -or !(Test-Path -LiteralPath $python -PathType Leaf)) {
  throw 'No hay Python ejecutable.'
}
function Invoke-VX([string]$mode,[string[]]$argsExtra=@()) {
  & $python -I $impl --mode $mode --home $homeRoot @argsExtra
  if ($LASTEXITCODE -ne 0) { throw "VX convivencia $mode bloqueado/error: $LASTEXITCODE" }
}
if ($Modo -eq 'Verificar') {
  Invoke-VX 'verify'
  return
}
if ($Modo -eq 'Restaurar') {
  if (!$ConfirmarRestauracion -or !$ConfirmarKiloCerrado -or
      [string]::IsNullOrWhiteSpace($CarpetaRespaldo)) {
    throw 'Restaurar requiere -CarpetaRespaldo -ConfirmarRestauracion -ConfirmarKiloCerrado.'
  }
  $running=@(Get-Process -Name 'Code','VSCodium','kilo-desktop' -ErrorAction SilentlyContinue)
  if ($running.Count -gt 0) { throw 'Cierra VS Code, VSCodium y Kilo antes de restaurar.' }
  Invoke-VX 'restore' @('--backup-folder',$CarpetaRespaldo,'--confirm-restore')
  return
}
$raw= & $python -I $impl --mode simulate --home $homeRoot
if ($LASTEXITCODE -ne 0) { throw 'Preflight no se pudo interpretar. No se escribió HOME.' }
$preflight=($raw -join [Environment]::NewLine) | ConvertFrom-Json
# El wrapper V023 conserva su identificador historico, pero valida el inventario
# vigente del pack VX 0.4.0. No altera MCP, JSONC ni AutoApprove.
if ([int]$preflight.agents_expected -ne 14 -or [int]$preflight.skills_expected -ne 32 -or
    [int]$preflight.mcp_changes -ne 0 -or [int]$preflight.jsonc_changes -ne 0) {
  throw 'Plan contiene inventario o permisos inesperados.'
}
Write-Host "VX Pack convivencia 0.2.3 | $Modo | HOME: $homeRoot" -ForegroundColor Cyan
Write-Host "Inline existentes: $($preflight.inline_agents_existing); agentes VX: 14; skills VX: 32."
Write-Host "Skills externas compatibles: .agents=$($preflight.compat_skills_existing.'.agents'), .kilocode=$($preflight.compat_skills_existing.'.kilocode'), .claude=$($preflight.compat_skills_existing.'.claude')"
Write-Host "Archivos VX a crear/actualizar: $($preflight.files_changed); sin cambios: $($preflight.files_unchanged)."
if (!$preflight.ready_to_apply) {
  Write-Warning 'Hay conflictos de nombre/ruta. NO instalar ni modificar JSONC para eludir bloqueos.'
  foreach ($item in @($preflight.inline_agent_collisions)) { Write-Warning "Colisión agente: $item" }
  foreach ($item in @($preflight.compat_skill_collisions)) { Write-Warning "Colisión skill: $item" }
  foreach ($item in @($preflight.blockers)) { Write-Warning "$item" }
  if ($Modo -eq 'Aplicar') { throw 'Instalación detenida por incompatibilidades reales.' }
}
if ($Modo -eq 'Diagnostico') { return }
if ($Modo -eq 'Simular') {
  Write-Host 'Simulación: solo rutas VX; sin tocar inline, skills externas, MCP o modelos.' -ForegroundColor Green
  return
}
if (!$ConfirmarConvivencia -or !$ConfirmarKiloCerrado) {
  throw 'Aplicar requiere -ConfirmarConvivencia y -ConfirmarKiloCerrado.'
}
$running=@(Get-Process -Name 'Code','VSCodium','kilo-desktop' -ErrorAction SilentlyContinue)
if ($running.Count -gt 0) { throw 'Cierra VS Code, VSCodium y Kilo antes de aplicar.' }
Invoke-VX 'apply' @('--confirm-coexist')
Invoke-VX 'verify'
Write-Host '[PASS] Archivos VX instalados por convivencia. Reinicia Kilo y valida ACL efectivas.' -ForegroundColor Green
