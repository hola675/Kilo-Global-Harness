#Requires -Version 7.0
<#
.SYNOPSIS
  VECIDYA Kilo Code Harness V2.0 - instalacion GLOBAL, reversible.
.DESCRIPTION
  Diagnostico (predeterminado) NO escribe en Windows. Aplicar cambia solo
  configuracion global de Kilo, settings de usuario VS Code y crea comandos/skill
  globales. NO edita ningun repositorio. NO toca credenciales, proveedores ni MCP.
  Solo admite archivos de configuracion que sean JSON estricto: si tienen
  comentarios JSONC o comas finales, no aplica (para no destruir comentarios).
.EXAMPLE
  pwsh -NoProfile -File .\scripts\Instalar-Kilo-Global-Harness-V2.ps1
  pwsh -NoProfile -File .\scripts\Instalar-Kilo-Global-Harness-V2.ps1 -Modo Aplicar
  pwsh -NoProfile -File .\scripts\Instalar-Kilo-Global-Harness-V2.ps1 -Modo Aplicar -PausarTaskObserver
#>
[CmdletBinding()]
param(
  [ValidateSet('Diagnostico','Aplicar','Restaurar')][string]$Modo = 'Diagnostico',
  [switch]$PausarTaskObserver,
  [string]$BackupFolder
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$globalConfigPath = Join-Path $HOME '.config\kilo\kilo.jsonc'
$vsCodeSettingsPath = Join-Path $env:APPDATA 'Code\User\settings.json'
$rulesDst = Join-Path $HOME '.config\kilo\rules\vx-global-harness-v2.md'
$commandsDst = Join-Path $HOME '.config\kilo\commands'
$skillDst = Join-Path $HOME '.kilo\skills\vx-engineering-harness'
$observerSrc = Join-Path $HOME '.kilo\skills\task-observer'

function Leer-JsonEstricto([string]$path) {
  if (!(Test-Path -LiteralPath $path)) { throw "Archivo no encontrado: $path" }
  $raw = Get-Content -LiteralPath $path -Raw -Encoding UTF8
  try { return ($raw | ConvertFrom-Json -AsHashtable -ErrorAction Stop) }
  catch { throw "El archivo NO es JSON estricto: $path. No se reescribira JSONC con comentarios/trailing commas. Use la UI de Kilo para los cambios manuales." }
}
function Guardar-Json([string]$path, $obj) {
  $json = ConvertTo-Json -InputObject $obj -Depth 100
  $tmp = $path + '.vx-harness-temp'
  [IO.File]::WriteAllText($tmp,($json + "`n"),[Text.UTF8Encoding]::new($false))
  Move-Item -LiteralPath $tmp -Destination $path -Force
}

Write-Host "=== VECIDYA KILO HARNESS V2 | $Modo | GLOBAL ONLY ===" -ForegroundColor Cyan
if ($Modo -eq 'Restaurar') {
  if (!$BackupFolder) { throw 'Para restaurar especifica -BackupFolder con la ruta devuelta durante Aplicar.' }
  $manifestPath = Join-Path $BackupFolder 'manifest.json'
  $manifest = Leer-JsonEstricto $manifestPath
  Write-Warning 'Restaurar reemplazara archivos globales por los guardados en ese backup. Revisa antes cualquier cambio posterior que quieras conservar.'
  foreach ($it in $manifest.files) {
    if ($it.existed) {
      New-Item -ItemType Directory -Path (Split-Path $it.target -Parent) -Force | Out-Null
      Copy-Item -LiteralPath $it.backup -Destination $it.target -Force
    } elseif (Test-Path -LiteralPath $it.target) {
      Remove-Item -LiteralPath $it.target -Force
    }
  }
  foreach ($d in $manifest.createdDirectories) {
    if (Test-Path $d) { Remove-Item -LiteralPath $d -Recurse -Force }
  }
  if ($manifest.observerMoved -and (Test-Path $manifest.observerBackup) -and !(Test-Path $observerSrc)) {
    Move-Item -LiteralPath $manifest.observerBackup -Destination $observerSrc
  }
  Write-Host 'Restauracion terminada. Recarga VS Code y Kilo.' -ForegroundColor Green
  exit 0
}

$config = Leer-JsonEstricto $globalConfigPath
$vsConfig = $null
try { if (Test-Path $vsCodeSettingsPath) { $vsConfig = Leer-JsonEstricto $vsCodeSettingsPath } }
catch { Write-Warning $_.Exception.Message; Write-Warning 'Los settings de VS Code no se modificaran.' }
$agentNames = @($config.agent.Keys)
$dangerousAgents = @($agentNames | Where-Object {
  $p = $config.agent[$_].permission
  $p -and (($p.bash -is [string] -and $p.bash -eq 'allow') -or ($p.edit -is [string] -and $p.edit -eq 'allow'))
})
$highSteps = @($agentNames | Where-Object {
  $s = $config.agent[$_].steps
  ($s -is [int] -or $s -is [long] -or $s -is [double]) -and $s -gt 160
})
Write-Host "Agentes definidos en config: $($agentNames.Count)"
Write-Host "Agentes con steps > 160: $($highSteps.Count)"
Write-Host "Agentes con edit/bash sin confirmacion: $($dangerousAgents.Count)"
Write-Host "MCP configurados: $(@($config.mcp.Keys).Count)"
Write-Host "AutoApprove VS Code: $(if($null -ne $vsConfig){$vsConfig['kilo-code.new.autoApprove.enabled']}else{'desconocido'})"
Write-Host "Skill task-observer presente: $(Test-Path $observerSrc)"
Write-Host "Destino de regla: $rulesDst"
Write-Host "Destino de comandos: $commandsDst"
Write-Host "Destino de skill: $skillDst"
if ($Modo -eq 'Diagnostico') {
  Write-Host 'DIAGNOSTICO: no se ha modificado ningun archivo.' -ForegroundColor Green
  Write-Host 'Para aplicar: pwsh -NoProfile -File .\scripts\Instalar-Kilo-Global-Harness-V2.ps1 -Modo Aplicar'
  exit 0
}

# Todo se valida ANTES del primer cambio
if (!(Test-Path (Join-Path $root 'rules\vx-global-harness-v2.md'))) {throw 'Paquete incompleto: falta regla'}
if (!(Test-Path (Join-Path $root 'skills\vx-engineering-harness\SKILL.md'))) {throw 'Paquete incompleto: falta skill'}
$commandSources = @(Get-ChildItem (Join-Path $root 'commands') -Filter '*.md' -File)
if (!$commandSources.Count) {throw 'Paquete incompleto: faltan comandos'}
$pendingNew = @($rulesDst)
$pendingNew += @($commandSources | ForEach-Object {Join-Path $commandsDst $_.Name})
$pendingNew += @(Join-Path $skillDst 'SKILL.md')
$collisions = @($pendingNew | Where-Object { Test-Path -LiteralPath $_ })
if ($collisions.Count) { throw "Hay destinos existentes: $($collisions -join ', '). No se sobrescribira ningun asset de la instalacion previa." }

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupDir = Join-Path $HOME "Downloads\Kilo-Harness-Backup-$stamp"
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
$manifest = [ordered]@{ version = '2.0.0'; created = $stamp; files = @(); createdDirectories = @(); observerMoved = $false; observerBackup = '' }
function Backup-Target([string]$path) {
  $existed = Test-Path -LiteralPath $path -PathType Leaf
  $back = ''
  if ($existed) {
    $back = Join-Path $backupDir ("file-" + $manifest.files.Count + '.bak')
    Copy-Item -LiteralPath $path -Destination $back -Force
  }
  $manifest.files += [ordered]@{target=$path;existed=[bool]$existed;backup=$back}
}
Backup-Target $globalConfigPath
if ($vsConfig) { Backup-Target $vsCodeSettingsPath }
foreach ($file in $pendingNew) {Backup-Target $file}
$manifest.createdDirectories += @($skillDst)
# Respaldar manifiesto antes de escribir configuraciones
Guardar-Json (Join-Path $backupDir 'manifest.json') $manifest

# Respeto de configuracion existente: NO tocar modelos, MCP ni nombres de agentes.
# Wildcard ask primero; permisos especificos despues (precedencia ultimas reglas).
$oldPerm = $config.permission
$perms = [ordered]@{
  '*' = 'ask'
  read = 'allow'
  glob = 'allow'
  grep = 'allow'
  lsp = 'allow'
  skill = 'allow'
  todoread = 'allow'
  todowrite = 'allow'
  edit = 'ask'
  bash = 'ask'
  task = 'ask'
  agent_manager = 'ask'
  external_directory = 'ask'
  doom_loop = 'ask'
}
if ($oldPerm -is [System.Collections.IDictionary]) {
  foreach ($k in $oldPerm.Keys) {
    if (!$perms.Contains($k)) {
      # Permisos MCP personalizados antiguos: preservarlos pero forzar aprobacion
      $perms[$k] = if ($oldPerm[$k] -eq 'deny') {'deny'} else {'ask'}
    }
  }
}
$config.permission = $perms

foreach ($name in $agentNames) {
  $a = $config.agent[$name]
  if (($a.steps -is [int] -or $a.steps -is [long] -or $a.steps -is [double]) -and $a.steps -gt 160) {
    $a.steps = if ($a.mode -eq 'subagent') {60} else {120}
  }
  if ($a.permission -is [System.Collections.IDictionary]) {
    foreach ($kind in @('bash','edit','mcp')) {
      $val = $a.permission[$kind]
      if ($val -is [string] -and $val -eq 'allow') { $a.permission[$kind] = 'ask' }
      elseif ($val -is [System.Collections.IDictionary]) {
        foreach ($pattern in @($val.Keys)) {if ($val[$pattern] -eq 'allow') {$val[$pattern] = 'ask'}}
      }
    }
  }
}
$ruleUri = ($HOME -replace '\\','/') + '/.config/kilo/rules/vx-global-harness-v2.md'
if ($null -eq $config.instructions) { $config.instructions = @() }
if ($config.instructions -notcontains $ruleUri) { $config.instructions = @($ruleUri) + @($config.instructions) }
Guardar-Json $globalConfigPath $config

if ($vsConfig) {
  $vsConfig['kilo-code.new.autoApprove.enabled'] = $false
  Guardar-Json $vsCodeSettingsPath $vsConfig
}
New-Item -ItemType Directory -Path (Split-Path $rulesDst -Parent),$commandsDst,$skillDst -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $root 'rules\vx-global-harness-v2.md') -Destination $rulesDst
foreach ($src in $commandSources) {Copy-Item -LiteralPath $src.FullName -Destination (Join-Path $commandsDst $src.Name)}
Copy-Item -LiteralPath (Join-Path $root 'skills\vx-engineering-harness\SKILL.md') -Destination (Join-Path $skillDst 'SKILL.md')

if ($PausarTaskObserver -and (Test-Path $observerSrc)) {
  $dest = Join-Path $backupDir 'task-observer-pausado'
  Move-Item -LiteralPath $observerSrc -Destination $dest
  $manifest.observerMoved = $true
  $manifest.observerBackup = $dest
}
Guardar-Json (Join-Path $backupDir 'manifest.json') $manifest
Write-Host 'Configuracion global V2 aplicada. NO se editaron repositorios ni definiciones Markdown de agentes.' -ForegroundColor Green
Write-Host "BACKUP LOCAL (NO COMPARTIR; puede contener secretos): $backupDir" -ForegroundColor Yellow
Write-Warning 'Quedan definiciones duplicadas en agents/*.md y agent del config. Consolidarlas solo despues de validar la precedencia en Kilo.'
Write-Host 'Recarga VS Code y ejecuta /reload. Verifica permisos en Settings > Auto Approve.'
