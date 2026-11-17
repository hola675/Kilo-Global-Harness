#Requires -Version 7.0
<#
.SYNOPSIS
  Instala el baseline minimo aprobado de Kilo Global Harness: solo Dev Team.
.DESCRIPTION
  Elimina del perfil global los recursos VX heredados, hace backup reversible y
  copia unicamente agents/vx-dev-team.md. NO modifica kilo.jsonc, MCP, modelos,
  AutoApprove, agentes nativos ni recursos de terceros.
#>
[CmdletBinding()]
param(
  [ValidateSet('Diagnostico','Simular','Aplicar','Verificar','Restaurar')]
  [string]$Modo = 'Diagnostico',
  [string]$RaizUsuario,
  [string]$BackupFolder
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$repoRoot = Split-Path $PSScriptRoot -Parent
$homeRoot = if ($RaizUsuario) {
  if (![IO.Path]::IsPathFullyQualified($RaizUsuario)) { throw 'RaizUsuario debe ser absoluta.' }
  [IO.Path]::GetFullPath($RaizUsuario)
} else { [IO.Path]::GetFullPath($HOME) }

$kiloDir = Join-Path $homeRoot '.config/kilo'
$agentDir = Join-Path $kiloDir 'agents'
$commandDir = Join-Path $kiloDir 'commands'
$ruleDir = Join-Path $kiloDir 'rules'
$pluginDir = Join-Path $kiloDir 'plugin'
$harnessDir = Join-Path $kiloDir 'harness'
$agentsFile = Join-Path $kiloDir 'AGENTS.md'
$configFile = Join-Path $kiloDir 'kilo.jsonc'
$devSource = Join-Path $repoRoot 'agents/vx-dev-team.md'
$devTarget = Join-Path $agentDir 'vx-dev-team.md'
$backupRoot = Join-Path $homeRoot '.config/kilo-devteam-backups'
$startMarker = '<!-- VX-HARNESS-V3:BEGIN -->'
$endMarker = '<!-- VX-HARNESS-V3:END -->'

function Hash-File([string]$Path) {
  if (!(Test-Path -LiteralPath $Path -PathType Leaf)) { return $null }
  return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
}

function Write-Utf8Atomic([string]$Path,[string]$Text) {
  $parent = Split-Path $Path -Parent
  New-Item -ItemType Directory -Path $parent -Force | Out-Null
  $tmp = Join-Path $parent ('.devteam-' + [guid]::NewGuid().ToString('N'))
  try {
    [IO.File]::WriteAllText($tmp,$Text,[Text.UTF8Encoding]::new($false))
    Move-Item -LiteralPath $tmp -Destination $Path -Force
  } finally {
    if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -Force }
  }
}

function Remove-VXManagedBlock([string]$Text) {
  $begin = $Text.IndexOf($startMarker,[StringComparison]::Ordinal)
  $end = $Text.IndexOf($endMarker,[StringComparison]::Ordinal)
  if (($begin -ge 0) -xor ($end -ge 0)) {
    throw 'AGENTS.md tiene marcadores VX incompletos; limpieza bloqueada.'
  }
  if ($begin -lt 0) { return $Text }
  if ($end -lt $begin) { throw 'AGENTS.md tiene marcadores VX desordenados.' }
  $finish = $end + $endMarker.Length
  $clean = $Text.Substring(0,$begin) + $Text.Substring($finish)
  $clean = $clean -replace '(\r?\n){3,}',[Environment]::NewLine + [Environment]::NewLine
  if ($clean.Trim().Length -eq 0) { return '' }
  return $clean.TrimEnd() + [Environment]::NewLine
}

function Add-UniqueItem(
  [System.Collections.ArrayList]$List,
  [System.Collections.Generic.HashSet[string]]$Seen,
  [string]$Path,
  [string]$Kind
) {
  if ([string]::IsNullOrWhiteSpace($Path)) { return }
  $full = [IO.Path]::GetFullPath($Path)
  if ($Seen.Add($full)) {
    [void]$List.Add([pscustomobject]@{Path=$full;Kind=$Kind})
  }
}

function Get-LegacyItems {
  $items = [System.Collections.ArrayList]::new()
  $seen = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)

  if (Test-Path -LiteralPath $agentDir) {
    foreach ($f in @(Get-ChildItem -LiteralPath $agentDir -Filter 'vx-*.md' -File -ErrorAction SilentlyContinue |
        Where-Object Name -ne 'vx-dev-team.md')) {
      Add-UniqueItem $items $seen $f.FullName 'file'
    }
  }

  foreach ($pair in @(
    @{Root=$commandDir;Filter='vx-*.md'},
    @{Root=$ruleDir;Filter='vx-*.md'}
  )) {
    if (Test-Path -LiteralPath $pair.Root) {
      foreach ($f in @(Get-ChildItem -LiteralPath $pair.Root -Filter $pair.Filter -File -ErrorAction SilentlyContinue)) {
        Add-UniqueItem $items $seen $f.FullName 'file'
      }
    }
  }

  $observer = Join-Path $pluginDir 'vx-observer-light.js'
  if (Test-Path -LiteralPath $observer -PathType Leaf) {
    Add-UniqueItem $items $seen $observer 'file'
  }

  foreach ($skillRoot in @(
    (Join-Path $homeRoot '.kilo/skills'),
    (Join-Path $homeRoot '.agents/skills'),
    (Join-Path $homeRoot '.kilocode/skills')
  )) {
    if (Test-Path -LiteralPath $skillRoot) {
      foreach ($d in @(Get-ChildItem -LiteralPath $skillRoot -Filter 'vx-*' -Directory -ErrorAction SilentlyContinue)) {
        Add-UniqueItem $items $seen $d.FullName 'dir'
      }
    }
  }

  if (Test-Path -LiteralPath $harnessDir) {
    foreach ($f in @(Get-ChildItem -LiteralPath $harnessDir -File -Recurse -ErrorAction SilentlyContinue)) {
      if ($f.Name -match '^(vx[-_]|Seleccionar-Equipo-V4|Validar-Registro-V4|Reconciliar-Agentes-V4\.2|Validar-MCP-Pack)') {
        Add-UniqueItem $items $seen $f.FullName 'file'
      }
    }
  }

  return @($items)
}

function Assert-DevTeamSource {
  if (!(Test-Path -LiteralPath $devSource -PathType Leaf)) { throw "Falta fuente Dev Team: $devSource" }
  $text = Get-Content -LiteralPath $devSource -Raw -Encoding UTF8
  foreach ($required in @(
    '(?m)^displayName:\s*"👥 Dev Team"\s*$',
    '(?m)^mode:\s*primary\s*$',
    '(?m)^color:\s*"#8B5CF6"\s*$',
    '(?m)^\s{2}skill:\s*deny\s*$',
    '(?m)^\s{2}task:\s*deny\s*$',
    '(?m)^\s{2}agent_manager:\s*deny\s*$'
  )) {
    if ($text -notmatch $required) { throw "Dev Team no cumple baseline minimo: $required" }
  }
  if ($text -match '(?m)^\s{2}"[a-z0-9-]+_\*":\s*(allow|ask)\s*$') {
    throw 'Dev Team contiene permisos MCP automaticos; baseline bloqueado.'
  }
}

function Show-State {
  $legacy = @(Get-LegacyItems)
  $vxAgents = @()
  if (Test-Path -LiteralPath $agentDir) {
    $vxAgents = @(Get-ChildItem -LiteralPath $agentDir -Filter 'vx-*.md' -File -ErrorAction SilentlyContinue |
      Select-Object -ExpandProperty Name)
  }
  Write-Host "=== DEV TEAM ONLY | $Modo ===" -ForegroundColor Cyan
  Write-Host "HOME: $homeRoot"
  Write-Host "Dev Team instalado: $(Test-Path -LiteralPath $devTarget -PathType Leaf)"
  Write-Host "Agentes VX visibles: $($vxAgents.Count) [$($vxAgents -join ', ')]"
  Write-Host "Recursos VX legacy detectados para retirar: $($legacy.Count)"
  Write-Host "kilo.jsonc: $(if(Test-Path -LiteralPath $configFile){'PRESERVADO'}else{'NO EXISTE'})"
  Write-Host 'MCP: fuera del alcance de este instalador; no se modifican.'
}

function Save-Manifest([string]$Dir,$Manifest) {
  New-Item -ItemType Directory -Path $Dir -Force | Out-Null
  [IO.File]::WriteAllText(
    (Join-Path $Dir 'manifest.json'),
    (($Manifest | ConvertTo-Json -Depth 12) + [Environment]::NewLine),
    [Text.UTF8Encoding]::new($false)
  )
}

function Backup-Target(
  [string]$Dir,
  [System.Collections.ArrayList]$Entries,
  [string]$Path,
  [string]$Kind,
  [int]$Index
) {
  $exists = Test-Path -LiteralPath $Path
  $backup = ''
  if ($exists) {
    $backup = Join-Path $Dir ("item-{0}" -f $Index)
    if ($Kind -eq 'dir') {
      Copy-Item -LiteralPath $Path -Destination $backup -Recurse -Force
    } else {
      Copy-Item -LiteralPath $Path -Destination $backup -Force
    }
  }
  [void]$Entries.Add([ordered]@{
    target=[IO.Path]::GetFullPath($Path)
    kind=$Kind
    existed=[bool]$exists
    backup=$backup
  })
}

function Restore-Backup([string]$Dir) {
  if ([string]::IsNullOrWhiteSpace($Dir) -or ![IO.Path]::IsPathFullyQualified($Dir)) {
    throw 'Restaurar requiere -BackupFolder absoluto.'
  }
  $manifestPath = Join-Path $Dir 'manifest.json'
  if (!(Test-Path -LiteralPath $manifestPath -PathType Leaf)) { throw "Falta manifiesto: $manifestPath" }
  $m = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
  if ($m.schema -ne 'dev-team-only-backup/1') { throw 'Backup incompatible.' }

  foreach ($entry in @($m.entries)) {
    $target = [string]$entry.target
    if (Test-Path -LiteralPath $target) { Remove-Item -LiteralPath $target -Recurse -Force }
    if ([bool]$entry.existed) {
      $parent = Split-Path $target -Parent
      New-Item -ItemType Directory -Path $parent -Force | Out-Null
      if ([string]$entry.kind -eq 'dir') {
        Copy-Item -LiteralPath ([string]$entry.backup) -Destination $target -Recurse -Force
      } else {
        Copy-Item -LiteralPath ([string]$entry.backup) -Destination $target -Force
      }
    }
  }

  Write-Host '[PASS] Estado VX previo restaurado desde backup.' -ForegroundColor Green
}

Assert-DevTeamSource

if ($Modo -eq 'Restaurar') {
  Restore-Backup $BackupFolder
  return
}

$legacy = @(Get-LegacyItems)

if ($Modo -eq 'Diagnostico') {
  Show-State
  Write-Host 'DIAGNOSTICO: sin cambios.' -ForegroundColor Green
  return
}

if ($Modo -eq 'Simular') {
  Show-State
  foreach ($item in $legacy) { Write-Host "[RETIRAR] $($item.Path)" }
  Write-Host "[INSTALAR/ACTUALIZAR] $devTarget"
  if (Test-Path -LiteralPath $agentsFile -PathType Leaf) {
    $raw = Get-Content -LiteralPath $agentsFile -Raw -Encoding UTF8
    if ($raw.Contains($startMarker)) { Write-Host "[LIMPIAR BLOQUE LEGACY] $agentsFile" }
  }
  Write-Host 'SIMULACION: sin cambios.' -ForegroundColor Green
  return
}

if ($Modo -eq 'Verificar') {
  $errors = [System.Collections.Generic.List[string]]::new()
  if (!(Test-Path -LiteralPath $devTarget -PathType Leaf)) {
    $errors.Add('Dev Team no esta instalado.')
  } elseif ((Hash-File $devTarget) -ne (Hash-File $devSource)) {
    $errors.Add('Dev Team instalado difiere de la fuente aprobada.')
  }

  $remaining = @(Get-LegacyItems)
  if ($remaining.Count -gt 0) {
    $errors.Add("Quedan $($remaining.Count) recursos VX legacy.")
  }

  if (Test-Path -LiteralPath $agentsFile -PathType Leaf) {
    $raw = Get-Content -LiteralPath $agentsFile -Raw -Encoding UTF8
    if ($raw.Contains($startMarker) -or $raw.Contains($endMarker)) {
      $errors.Add('AGENTS.md conserva el bloque VX legacy.')
    }
  }

  if ($errors.Count -gt 0) {
    foreach ($e in $errors) { Write-Host "[FAIL] $e" -ForegroundColor Red }
    throw "Baseline Dev Team Only incompleto: $($errors.Count) errores."
  }

  Write-Host '[PASS] Solo Dev Team queda activo dentro del namespace VX.' -ForegroundColor Green
  Write-Host '[PASS] Skills/workflows/reglas/plugins/runtime VX legacy no estan instalados.' -ForegroundColor Green
  Write-Host '[PASS] Este verificador no modifica ni autentica MCP.' -ForegroundColor Green
  return
}

# Aplicar
$stamp = (Get-Date -Format 'yyyyMMdd-HHmmss-fff') + '-' + ([guid]::NewGuid().ToString('N').Substring(0,8))
$backupDir = Join-Path $backupRoot $stamp
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
$entries = [System.Collections.ArrayList]::new()
$index = 0

Backup-Target $backupDir $entries $devTarget 'file' $index
$index++
Backup-Target $backupDir $entries $agentsFile 'file' $index
$index++
foreach ($item in $legacy) {
  Backup-Target $backupDir $entries $item.Path $item.Kind $index
  $index++
}

$configHashBefore = Hash-File $configFile
$manifest = [ordered]@{
  schema='dev-team-only-backup/1'
  created=$stamp
  home=$homeRoot
  config_hash_before=$configHashBefore
  entries=@($entries)
}
Save-Manifest $backupDir $manifest

try {
  foreach ($item in $legacy) {
    if (Test-Path -LiteralPath $item.Path) {
      Remove-Item -LiteralPath $item.Path -Recurse -Force
    }
  }

  if (Test-Path -LiteralPath $agentsFile -PathType Leaf) {
    $raw = Get-Content -LiteralPath $agentsFile -Raw -Encoding UTF8
    $clean = Remove-VXManagedBlock $raw
    if ([string]::IsNullOrWhiteSpace($clean)) {
      Remove-Item -LiteralPath $agentsFile -Force
    } elseif ($clean -ne $raw) {
      Write-Utf8Atomic $agentsFile $clean
    }
  }

  New-Item -ItemType Directory -Path $agentDir -Force | Out-Null
  Copy-Item -LiteralPath $devSource -Destination $devTarget -Force

  $configHashAfter = Hash-File $configFile
  if ($configHashBefore -ne $configHashAfter) {
    throw 'kilo.jsonc cambio durante la operacion; rollback obligatorio.'
  }
} catch {
  $message = $_.Exception.Message
  Write-Warning "Aplicacion interrumpida: $message"
  Restore-Backup $backupDir
  throw
}

Write-Host '[PASS] Baseline aplicado: solo Dev Team dentro del Harness VX.' -ForegroundColor Green
Write-Host '[PASS] kilo.jsonc y configuracion MCP preservados.' -ForegroundColor Green
Write-Host "BACKUP: $backupDir" -ForegroundColor Yellow
Write-Host 'Ejecuta este mismo script con -Modo Verificar y luego /reload en Kilo.' -ForegroundColor Cyan
