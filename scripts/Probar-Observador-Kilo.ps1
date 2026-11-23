#Requires -Version 7.0
# component_version: 1.1.0
# last_modified: 2026-11-23
<#
.SYNOPSIS
  Preparación de laboratorio R3 aislado; NO instala ni inicia Kilo.
#>
[CmdletBinding()]
param(
    [ValidateSet('Diagnostico','Preparar','Verificar','Limpiar')]
    [string]$Modo = 'Diagnostico',
    [string]$RaizLaboratorio = (Join-Path $env:TEMP 'vx-kilo-observer-lab'),
    [string]$KiloExecutable,
    [switch]$ConfirmarLimpieza,
    [switch]$ConfirmarLabCerrado
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if ($env:OS -ne 'Windows_NT') { throw 'Solo Windows.' }
if (-not [IO.Path]::IsPathFullyQualified($RaizLaboratorio)) { throw 'Ruta lab no absoluta.' }
$Lab = [IO.Path]::GetFullPath($RaizLaboratorio).TrimEnd([IO.Path]::DirectorySeparatorChar)
$Temp = [IO.Path]::GetFullPath($env:TEMP).TrimEnd([IO.Path]::DirectorySeparatorChar)
if (-not $Lab.StartsWith(($Temp + [IO.Path]::DirectorySeparatorChar),[StringComparison]::OrdinalIgnoreCase)) {
    throw 'El laboratorio debe residir bajo TEMP y nunca en el perfil Kilo real.'
}
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Project = Join-Path $Lab 'vx-observer-lab'
$Plugins = Join-Path $Project '.kilo\plugin'
$Db = Join-Path $Lab 'state\vx-runtime-observations.sqlite3'
$SourcePlugin = Join-Path $Repo 'runtime\kilo-observer\vx-runtime-observer.js'
$SourceHelper = Join-Path $Repo 'runtime\kilo-observer\lib\vx-observer-hooks.js'
$Dag = Join-Path $Repo 'scripts\vx_task_dag.py'
$Marker = Join-Path $Lab '.vx-observer-lab.marker'
function Resolve-KiloExecutable {
    if ($KiloExecutable) {
        if (-not [IO.Path]::IsPathFullyQualified($KiloExecutable) -or
            -not (Test-Path -LiteralPath $KiloExecutable -PathType Leaf)) {
            throw "KiloExecutable no es un ejecutable absoluto existente: $KiloExecutable"
        }
        return (Resolve-Path -LiteralPath $KiloExecutable).Path
    }
    $Command = Get-Command kilo -CommandType Application -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if ($Command) { return $Command.Source }

    # Kilo Desktop bundles its own CLI. Search installed app versions without
    # changing PATH, user profile, or the Desktop installation.
    $DesktopRoot = Join-Path $env:LOCALAPPDATA 'KiloDesktop'
    if (Test-Path -LiteralPath $DesktopRoot -PathType Container) {
        $Apps = Get-ChildItem -LiteralPath $DesktopRoot -Directory -Filter 'app-*' |
            Sort-Object { try { [version]($_.Name -replace '^app-', '') } catch { [version]'0.0.0' } } -Descending
        foreach ($App in $Apps) {
            foreach ($Variant in @('windows-x64-baseline','windows-x64','windows-arm64')) {
                $Candidate = Join-Path $App.FullName "resources\kilo\$Variant\bin\kilo.exe"
                if (Test-Path -LiteralPath $Candidate -PathType Leaf) { return $Candidate }
            }
        }
    }
    return $null
}
$ResolvedKilo = Resolve-KiloExecutable
foreach ($Source in @($SourcePlugin,$SourceHelper,$Dag)) {
    if (-not (Test-Path -LiteralPath $Source -PathType Leaf)) { throw "Fuente ausente: $Source" }
}
if ($Modo -eq 'Preparar') {
    if (Test-Path -LiteralPath $Lab) { throw 'Laboratorio ya existe: no sobrescribir.' }
    $Parent = Split-Path -Parent $Lab
    if ((Get-Item -LiteralPath $Parent).Attributes -band [IO.FileAttributes]::ReparsePoint) {
        throw 'Directorio padre es un enlace/junction: abortar.'
    }
    $null = New-Item -ItemType Directory -Path (Join-Path $Plugins 'lib') -Force
    Copy-Item -LiteralPath $SourcePlugin -Destination (Join-Path $Plugins 'vx-runtime-observer.js')
    Copy-Item -LiteralPath $SourceHelper -Destination (Join-Path $Plugins 'lib\vx-observer-hooks.js')
    $KiloLiteral = if ($ResolvedKilo) { "'" + $ResolvedKilo.Replace("'", "''") + "'" } else { '$null' }
    $Launcher = @'
# SOLO ejecutar a mano. Sin claves ni proyectos reales.
$ErrorActionPreference = 'Stop'
$Lab = Split-Path -Parent $MyInvocation.MyCommand.Path
$Project = Join-Path $Lab 'vx-observer-lab'
$env:USERPROFILE = Join-Path $Lab 'profile'
$env:HOME = $env:USERPROFILE
$env:XDG_CONFIG_HOME = Join-Path $Lab 'xdg-config'
$env:XDG_DATA_HOME = Join-Path $Lab 'xdg-data'
$env:XDG_CACHE_HOME = Join-Path $Lab 'xdg-cache'
$env:XDG_STATE_HOME = Join-Path $Lab 'xdg-state'
$env:APPDATA = Join-Path $Lab 'appdata-roaming'
$env:LOCALAPPDATA = Join-Path $Lab 'appdata-local'
$env:VX_OBSERVER_ENABLE = '1'
$env:VX_OBSERVER_PROJECT = 'vx-observer-lab'
$env:VX_OBSERVER_STATE_ROOT = Join-Path $Lab 'state'
Remove-Item Env:KILO_PURE -ErrorAction SilentlyContinue
$KiloExe = __VX_KILO_EXE__
if (-not $KiloExe) {
    $KiloCommand = Get-Command kilo -CommandType Application -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if ($KiloCommand) { $KiloExe = $KiloCommand.Source }
}
if (-not $KiloExe -or -not (Test-Path -LiteralPath $KiloExe -PathType Leaf)) {
    throw 'Kilo CLI no encontrado. Diagnostica con -Modo Diagnostico; no se ha ejecutado el lab.'
}
Write-Host "CLI aislado: $KiloExe" -ForegroundColor Cyan
Write-Host 'Proyecto aislado. No se copian credenciales, modelos ni MCP.' -ForegroundColor Yellow
Push-Location $Project
try { & $KiloExe $Project } finally { Pop-Location }
'@
    $Launcher = $Launcher.Replace('__VX_KILO_EXE__', $KiloLiteral)
    Set-Content -LiteralPath (Join-Path $Lab 'Iniciar-Laboratorio.ps1') -Value $Launcher -Encoding utf8
    Set-Content -LiteralPath $Marker -Value 'VX_OBSERVER_LAB_V1' -Encoding ascii
    Write-Host 'LAB_PREPARED: Kilo NO iniciado, perfil real sin cambios.' -ForegroundColor Green
}
if ($Modo -eq 'Verificar') {
    if (-not (Test-Path -LiteralPath $Project -PathType Container)) {
        throw 'Laboratorio no preparado.'
    }
    $Py = (Get-Command python -CommandType Application -ErrorAction Stop | Select-Object -First 1 -ExpandProperty Source)
    & $Py -I $Dag --observer-report --observer-db $Db --project 'vx-observer-lab'
    if ($LASTEXITCODE -ne 0) { throw 'Lectura SQLite lab falló.' }
}
if ($Modo -eq 'Limpiar') {
    if (-not $ConfirmarLimpieza -or -not $ConfirmarLabCerrado) {
        throw 'Limpiar requiere -ConfirmarLimpieza y -ConfirmarLabCerrado.'
    }
    if (-not (Test-Path -LiteralPath $Marker -PathType Leaf)) {
        throw 'Sin marcador de laboratorio VX: no borrar.'
    }
    if ((Get-Content -LiteralPath $Marker -Raw).Trim() -cne 'VX_OBSERVER_LAB_V1') {
        throw 'Marcador alterado: no borrar.'
    }
    if (@(Get-ChildItem -LiteralPath $Lab -Recurse -Force -Attributes ReparsePoint).Count -gt 0) {
        throw 'Laboratorio contiene enlaces/junctions: limpieza bloqueada.'
    }
    Remove-Item -LiteralPath $Lab -Recurse -Force -ErrorAction Stop
    Write-Host 'LAB_REMOVED: solo carpeta temporal del laboratorio.' -ForegroundColor Green
    return
}
[ordered]@{
    schema = 'vx-observer-lab-status/1'
    mode = $Modo
    lab = $Lab
    project = $Project
    plugin_staged = (Test-Path -LiteralPath (Join-Path $Plugins 'vx-runtime-observer.js') -PathType Leaf)
    db_present = (Test-Path -LiteralPath $Db -PathType Leaf)
    kilo_cli_available = [bool]$ResolvedKilo
    kilo_executable = $ResolvedKilo
    global_install_changes = 0
    kilo_started_by_this_script = $false
} | ConvertTo-Json -Depth 3
