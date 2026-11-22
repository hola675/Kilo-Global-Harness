#Requires -Version 7.0
<#
.SYNOPSIS
  VX Dev Team Core unificado 1.6.0-rc1 — único instalador global vigente.
.DESCRIPTION
  Diagnostico/Simular: solo lectura; Aplicar: backup DPAPI CurrentUser,
  actualización de 18 agentes y 57 Skills, retiro EXPLÍCITO de hasta 14 ficheros
  legacy gestionados por VX. No cambia kilo.jsonc, MCP o recursos de terceros.
  Verificar no equivale a certificar permisos efectivos en Kilo.
#>
[CmdletBinding()]
param(
    [ValidateSet('Diagnostico','Simular','Aplicar','Verificar','Restaurar')]
    [string]$Modo = 'Diagnostico',
    [string]$RaizUsuario = $HOME,
    [switch]$ConfirmarInstalacion,
    [switch]$ConfirmarRetirarVXLegacy,
    [switch]$ConfirmarKiloCerrado,
    [switch]$ConfirmarRestauracion,
    [switch]$RecuperarInstalacionInterrumpida,
    [string]$CarpetaRespaldo
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if ($env:OS -ne 'Windows_NT') { throw 'Solo Windows con DPAPI CurrentUser.' }
if (![IO.Path]::IsPathFullyQualified($RaizUsuario)) { throw 'RaizUsuario debe ser absoluta.' }
$homeRoot = [IO.Path]::GetFullPath($RaizUsuario)
$engine = Join-Path $PSScriptRoot 'vx_unified_pack.py'
if (!(Test-Path -LiteralPath $engine -PathType Leaf)) { throw 'No existe el motor de instalación unificada.' }
$python = (Get-Command python -CommandType Application -ErrorAction Stop |
    Select-Object -First 1 -ExpandProperty Source)
if (!$python) { throw 'Python no disponible.' }

function Invoke-Pack([string]$Operation, [string[]]$ExtraArgs = @()) {
    & $python -I $engine --mode $Operation --home $homeRoot @ExtraArgs
    if ($LASTEXITCODE -ne 0) { throw "Pack Dev Team Core: $Operation falló (exit=$LASTEXITCODE)." }
}
function Assert-KiloClosed {
    if (!$ConfirmarKiloCerrado) { throw 'Requiere -ConfirmarKiloCerrado.' }
    $running = @(Get-Process -Name 'Code','VSCodium','kilo-desktop' -ErrorAction SilentlyContinue)
    if ($running.Count -gt 0) { throw 'Cierra todas las ventanas VS Code/VSCodium/Kilo Desktop antes de aplicar o restaurar.' }
}
function Assert-CurrentMain {
    $root = Split-Path $PSScriptRoot -Parent
    $branch = (& git -C $root branch --show-current | Out-String).Trim()
    if ($LASTEXITCODE -ne 0 -or $branch -cne 'main') { throw 'Instalar solo desde main sincronizada.' }
    $dirty = @(& git -C $root status --porcelain)
    if ($LASTEXITCODE -ne 0 -or $dirty.Count -gt 0) { throw 'Repositorio con cambios locales.' }
    $local = (& git -C $root rev-parse HEAD | Out-String).Trim()
    $tracked = (& git -C $root rev-parse --verify refs/remotes/origin/main | Out-String).Trim()
    if ($LASTEXITCODE -ne 0 -or $local -cne $tracked) { throw 'main local no coincide con origin/main; sincroniza y verifica CI.' }
}

switch ($Modo) {
    'Diagnostico' { Invoke-Pack 'diagnose'; return }
    'Simular' { Invoke-Pack 'simulate'; return }
    'Verificar' { Invoke-Pack 'verify'; return }
    'Restaurar' {
        Assert-KiloClosed
        if (!$ConfirmarRestauracion -or !$CarpetaRespaldo -or
            ![IO.Path]::IsPathFullyQualified($CarpetaRespaldo)) {
            throw 'Restaurar requiere respaldo absoluto y -ConfirmarRestauracion.'
        }
        $restoreArgs = @('--backup-folder',$CarpetaRespaldo,'--confirm-restore')
        if ($RecuperarInstalacionInterrumpida) { $restoreArgs += '--recover-incomplete' }
        Invoke-Pack 'restore' $restoreArgs
        return
    }
    'Aplicar' {
        if (!$ConfirmarInstalacion -or !$ConfirmarRetirarVXLegacy) {
            throw 'Aplicar requiere -ConfirmarInstalacion y -ConfirmarRetirarVXLegacy.'
        }
        Assert-KiloClosed
        Assert-CurrentMain
        Invoke-Pack 'apply' @('--confirm-install')
        Invoke-Pack 'verify'
        Write-Host '[PASS] Source del pack instalado. Reinicia Kilo y recertifica tools, task y skills reales.' -ForegroundColor Green
        return
    }
}
