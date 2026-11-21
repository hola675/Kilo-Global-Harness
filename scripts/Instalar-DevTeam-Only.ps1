#Requires -Version 7.0
<#
.SYNOPSIS
  Instala Dev Team V2-R: un lider visible y diez subagentes ocultos read-only.
.DESCRIPTION
  Retira runtime VX legacy, instala unicamente el runtime aprobado V2-R y crea
  backup reversible. NO modifica kilo.jsonc, MCP, modelos, AutoApprove, agentes
  nativos ni recursos de terceros.
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
$skillDir = Join-Path $homeRoot '.kilo/skills'
$commandDir = Join-Path $kiloDir 'commands'
$ruleDir = Join-Path $kiloDir 'rules'
$pluginDir = Join-Path $kiloDir 'plugin'
$harnessDir = Join-Path $kiloDir 'harness'
$agentsFile = Join-Path $kiloDir 'AGENTS.md'
$configFile = Join-Path $kiloDir 'kilo.jsonc'
$backupRoot = Join-Path $homeRoot '.config/kilo-devteam-backups'
$startMarker = '<!-- VX-HARNESS-V3:BEGIN -->'
$endMarker = '<!-- VX-HARNESS-V3:END -->'

$approvedAgents = [ordered]@{
  'vx-dev-team.md'         = (Join-Path $repoRoot 'agents/vx-dev-team.md')
  'vx-dev-explorer.md'     = (Join-Path $repoRoot 'runtime/dev-team-v2r/agents/vx-dev-explorer.md')
  'vx-dev-architect.md'    = (Join-Path $repoRoot 'runtime/dev-team-v2r/agents/vx-dev-architect.md')
  'vx-dev-frontend.md'     = (Join-Path $repoRoot 'runtime/dev-team-v2r/agents/vx-dev-frontend.md')
  'vx-dev-backend.md'      = (Join-Path $repoRoot 'runtime/dev-team-v2r/agents/vx-dev-backend.md')
  'vx-dev-data.md'         = (Join-Path $repoRoot 'runtime/dev-team-v2r/agents/vx-dev-data.md')
  'vx-dev-platform.md'     = (Join-Path $repoRoot 'runtime/dev-team-v2r/agents/vx-dev-platform.md')
  'vx-dev-reviewer.md'     = (Join-Path $repoRoot 'runtime/dev-team-v2r/agents/vx-dev-reviewer.md')
  'vx-dev-quality.md'      = (Join-Path $repoRoot 'runtime/dev-team-v2r/agents/vx-dev-quality.md')
  'vx-dev-security.md'     = (Join-Path $repoRoot 'runtime/dev-team-v2r/agents/vx-dev-security.md')
  'vx-dev-research.md'     = (Join-Path $repoRoot 'runtime/dev-team-v2r/agents/vx-dev-research.md')
}
$approvedNames = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($name in $approvedAgents.Keys) { [void]$approvedNames.Add($name) }

$approvedSkills = [ordered]@{
  'vx-dev-project-policy'          = (Join-Path $repoRoot 'runtime/dev-team-v2r/skills/vx-dev-project-policy')
  'vx-dev-team-handoff'           = (Join-Path $repoRoot 'runtime/dev-team-v2r/skills/vx-dev-team-handoff')
  'vx-dev-mcp-readonly'           = (Join-Path $repoRoot 'runtime/dev-team-v2r/skills/vx-dev-mcp-readonly')
  'vx-dev-mcp-security'           = (Join-Path $repoRoot 'runtime/dev-team-v2r/skills/vx-dev-mcp-security')
  'vx-dev-codebase-investigation' = (Join-Path $repoRoot 'runtime/dev-team-v2r/skills/vx-dev-codebase-investigation')
  'vx-dev-source-reconciliation'  = (Join-Path $repoRoot 'runtime/dev-team-v2r/skills/vx-dev-source-reconciliation')
  'vx-dev-architecture-decision'  = (Join-Path $repoRoot 'runtime/dev-team-v2r/skills/vx-dev-architecture-decision')
  'vx-dev-backend-contracts'      = (Join-Path $repoRoot 'runtime/dev-team-v2r/skills/vx-dev-backend-contracts')
  'vx-dev-data-migration'         = (Join-Path $repoRoot 'runtime/dev-team-v2r/skills/vx-dev-data-migration')
  'vx-dev-platform-delivery'      = (Join-Path $repoRoot 'runtime/dev-team-v2r/skills/vx-dev-platform-delivery')
  'vx-dev-debug-triage'           = (Join-Path $repoRoot 'runtime/dev-team-v2r/skills/vx-dev-debug-triage')
  'vx-dev-frontend-ux'            = (Join-Path $repoRoot 'runtime/dev-team-v2r/skills/vx-dev-frontend-ux')
  'vx-dev-accessibility'          = (Join-Path $repoRoot 'runtime/dev-team-v2r/skills/vx-dev-accessibility')
  'vx-dev-ui-state-system'        = (Join-Path $repoRoot 'runtime/dev-team-v2r/skills/vx-dev-ui-state-system')
  'vx-dev-test-strategy'          = (Join-Path $repoRoot 'runtime/dev-team-v2r/skills/vx-dev-test-strategy')
  'vx-dev-security-threat-review' = (Join-Path $repoRoot 'runtime/dev-team-v2r/skills/vx-dev-security-threat-review')
  'vx-dev-supply-chain-review'    = (Join-Path $repoRoot 'runtime/dev-team-v2r/skills/vx-dev-supply-chain-review')
  'vx-dev-independent-review'     = (Join-Path $repoRoot 'runtime/dev-team-v2r/skills/vx-dev-independent-review')
}
$approvedSkillNames = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($name in $approvedSkills.Keys) { [void]$approvedSkillNames.Add($name) }

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
  $clean = $clean -replace '(\r?\n){3,}',([Environment]::NewLine + [Environment]::NewLine)
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
  if ($Seen.Add($full)) { [void]$List.Add([pscustomobject]@{Path=$full;Kind=$Kind}) }
}

function Get-LegacyItems {
  $items = [System.Collections.ArrayList]::new()
  $seen = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)

  if (Test-Path -LiteralPath $agentDir) {
    foreach ($f in @(Get-ChildItem -LiteralPath $agentDir -Filter 'vx-*.md' -File -ErrorAction SilentlyContinue)) {
      if (!$approvedNames.Contains($f.Name)) { Add-UniqueItem $items $seen $f.FullName 'file' }
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
  if (Test-Path -LiteralPath $observer -PathType Leaf) { Add-UniqueItem $items $seen $observer 'file' }

  foreach ($skillRoot in @(
    $skillDir,
    (Join-Path $homeRoot '.agents/skills'),
    (Join-Path $homeRoot '.kilocode/skills')
  )) {
    if (Test-Path -LiteralPath $skillRoot) {
      foreach ($d in @(Get-ChildItem -LiteralPath $skillRoot -Filter 'vx-*' -Directory -ErrorAction SilentlyContinue)) {
        if (($skillRoot -eq $skillDir) -and $approvedSkillNames.Contains($d.Name)) { continue }
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

function Assert-SkillSources {
  foreach ($pair in $approvedSkills.GetEnumerator()) {
    $skillFile = Join-Path $pair.Value 'SKILL.md'
    if (!(Test-Path -LiteralPath $skillFile -PathType Leaf)) { throw "Falta skill aprobada: $skillFile" }
    $text = Get-Content -LiteralPath $skillFile -Raw -Encoding UTF8
    if ($text -match '!\x60[^\x60]+\x60') { throw "Skill $($pair.Key) contiene shell injection embebido." }
  }
}

function Assert-AgentSources {
  foreach ($pair in $approvedAgents.GetEnumerator()) {
    if (!(Test-Path -LiteralPath $pair.Value -PathType Leaf)) { throw "Falta fuente aprobada: $($pair.Value)" }
  }

  $leader = Get-Content -LiteralPath $approvedAgents['vx-dev-team.md'] -Raw -Encoding UTF8
  foreach ($required in @(
    '(?m)^displayName:\s*"VX Dev Team"\s*$',
    '(?m)^mode:\s*primary\s*$',
    '(?m)^color:\s*"#8B5CF6"\s*$',
    '(?m)^\s{2}skill:\s*$',
    '(?m)^\s{4}"\*":\s*deny\s*$',
    '(?m)^\s{2}task:\s*$',
    '(?m)^\s{2}agent_manager:\s*deny\s*$',
    '(?m)^\s{2}board_read:\s*allow\s*$',
    '(?m)^\s{2}board_post:\s*allow\s*$'
  )) {
    if ($leader -notmatch $required) { throw "Dev Team V2-R invalido: $required" }
  }

  foreach ($name in $approvedAgents.Keys | Where-Object { $_ -ne 'vx-dev-team.md' }) {
    $childId = [IO.Path]::GetFileNameWithoutExtension($name)
    $pattern = '(?m)^\s{4}"' + [regex]::Escape($childId) + '":\s*allow\s*$'
    if ($leader -notmatch $pattern) { throw "Dev Team no permite delegar al subagente aprobado: $childId" }
  }
  if ($leader -match '(?m)^\s{4}"vx-dev-backend-data":\s*allow\s*$') {
    throw 'Dev Team conserva ACL del subagente supersedido vx-dev-backend-data.'
  }

  foreach ($name in $approvedAgents.Keys | Where-Object { $_ -ne 'vx-dev-team.md' }) {
    $text = Get-Content -LiteralPath $approvedAgents[$name] -Raw -Encoding UTF8
    foreach ($required in @(
      '(?m)^mode:\s*subagent\s*$',
      '(?m)^hidden:\s*true\s*$',
      '(?m)^\s{2}read:\s*deny\s*$',
      '(?m)^\s{2}skill:\s*$',
      '(?m)^\s{4}"\*":\s*deny\s*$',
      '(?m)^\s{2}task:\s*deny\s*$',
      '(?m)^\s{2}edit:\s*deny\s*$',
      '(?m)^\s{2}write:\s*deny\s*$',
      '(?m)^\s{2}apply_patch:\s*deny\s*$',
      '(?m)^\s{2}bash:\s*deny\s*$',
      '(?m)^\s{2}agent_manager:\s*deny\s*$',
    '(?m)^\s{2}board_read:\s*allow\s*$',
    '(?m)^\s{2}board_post:\s*allow\s*$',
      '(?m)^\s{2}board_read:\s*deny\s*$',
      '(?m)^\s{2}board_post:\s*deny\s*$'
    )) {
      if ($text -notmatch $required) { throw "Subagente $name no es read-only/oculto: $required" }
    }
    if ($text -match '(?m)^\s{2}"[a-z0-9-]+_\*":\s*(allow|ask)\s*$') {
      throw "Subagente $name contiene permisos MCP automaticos."
    }
  }

  $agentSkillMatrix = @{
    'vx-dev-team.md'      = @('vx-dev-project-policy','vx-dev-team-handoff')
    'vx-dev-explorer.md'  = @('vx-dev-codebase-investigation','vx-dev-debug-triage')
    'vx-dev-research.md'  = @('vx-dev-source-reconciliation','vx-dev-mcp-readonly')
    'vx-dev-architect.md' = @('vx-dev-architecture-decision','vx-dev-mcp-readonly','vx-dev-project-policy')
    'vx-dev-frontend.md'  = @('vx-dev-frontend-ux','vx-dev-accessibility','vx-dev-ui-state-system','vx-dev-debug-triage')
    'vx-dev-backend.md'   = @('vx-dev-backend-contracts','vx-dev-debug-triage')
    'vx-dev-data.md'      = @('vx-dev-data-migration')
    'vx-dev-platform.md'  = @('vx-dev-platform-delivery','vx-dev-debug-triage')
    'vx-dev-quality.md'   = @('vx-dev-test-strategy','vx-dev-accessibility')
    'vx-dev-security.md'  = @('vx-dev-security-threat-review','vx-dev-supply-chain-review','vx-dev-mcp-security')
    'vx-dev-reviewer.md'  = @('vx-dev-independent-review','vx-dev-project-policy')
  }
  foreach ($name in $agentSkillMatrix.Keys) {
    $text = Get-Content -LiteralPath $approvedAgents[$name] -Raw -Encoding UTF8
    foreach ($skill in $agentSkillMatrix[$name]) {
      $pattern = '(?m)^\s{4}"' + [regex]::Escape($skill) + '":\s*allow\s*$'
      if ($text -notmatch $pattern) { throw "Agente $name no permite skill aprobada: $skill" }
    }
  }
}

function Show-State {
  $legacy = @(Get-LegacyItems)
  $installed = @()
  foreach ($name in $approvedAgents.Keys) {
    if (Test-Path -LiteralPath (Join-Path $agentDir $name) -PathType Leaf) { $installed += $name }
  }
  Write-Host "=== DEV TEAM V2-R | $Modo ===" -ForegroundColor Cyan
  Write-Host "HOME: $homeRoot"
  Write-Host "Agentes aprobados instalados detectados: $($installed.Count)/$($approvedAgents.Count)"
  $installedSkills = @($approvedSkills.Keys | Where-Object { Test-Path -LiteralPath (Join-Path $skillDir $_) -PathType Container })
  Write-Host "Skills Dev Team instaladas detectadas: $($installedSkills.Count)/$($approvedSkills.Count)"
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
  if (@('dev-team-only-backup/1','dev-team-v2r-backup/1') -notcontains [string]$m.schema) {
    throw 'Backup incompatible.'
  }

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

Assert-SkillSources
Assert-AgentSources

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
  foreach ($name in $approvedAgents.Keys) { Write-Host "[INSTALAR/ACTUALIZAR] $(Join-Path $agentDir $name)" }
  foreach ($name in $approvedSkills.Keys) { Write-Host "[INSTALAR/ACTUALIZAR SKILL] $(Join-Path $skillDir $name)" }
  if (Test-Path -LiteralPath $agentsFile -PathType Leaf) {
    $raw = Get-Content -LiteralPath $agentsFile -Raw -Encoding UTF8
    if ($raw.Contains($startMarker)) { Write-Host "[LIMPIAR BLOQUE LEGACY] $agentsFile" }
  }
  Write-Host 'SIMULACION: sin cambios.' -ForegroundColor Green
  return
}

if ($Modo -eq 'Verificar') {
  $errors = [System.Collections.Generic.List[string]]::new()

  foreach ($pair in $approvedAgents.GetEnumerator()) {
    $target = Join-Path $agentDir $pair.Key
    if (!(Test-Path -LiteralPath $target -PathType Leaf)) {
      $errors.Add("Falta agente aprobado: $($pair.Key)")
    } elseif ((Hash-File $target) -ne (Hash-File $pair.Value)) {
      $errors.Add("Agente instalado difiere de fuente aprobada: $($pair.Key)")
    }
  }

  foreach ($pair in $approvedSkills.GetEnumerator()) {
    $targetSkill = Join-Path (Join-Path $skillDir $pair.Key) 'SKILL.md'
    $sourceSkill = Join-Path $pair.Value 'SKILL.md'
    if (!(Test-Path -LiteralPath $targetSkill -PathType Leaf)) {
      $errors.Add("Falta skill aprobada: $($pair.Key)")
    } elseif ((Hash-File $targetSkill) -ne (Hash-File $sourceSkill)) {
      $errors.Add("Skill instalada difiere de fuente aprobada: $($pair.Key)")
    }
  }

  $remaining = @(Get-LegacyItems)
  if ($remaining.Count -gt 0) { $errors.Add("Quedan $($remaining.Count) recursos VX legacy.") }

  if (Test-Path -LiteralPath $agentsFile -PathType Leaf) {
    $raw = Get-Content -LiteralPath $agentsFile -Raw -Encoding UTF8
    if ($raw.Contains($startMarker) -or $raw.Contains($endMarker)) {
      $errors.Add('AGENTS.md conserva el bloque VX legacy.')
    }
  }

  if ($errors.Count -gt 0) {
    foreach ($e in $errors) { Write-Host "[FAIL] $e" -ForegroundColor Red }
    throw "Baseline Dev Team V2-R incompleto: $($errors.Count) errores."
  }

  Write-Host '[PASS] Dev Team es el unico primario VX aprobado.' -ForegroundColor Green
  Write-Host '[PASS] Diez subagentes ocultos V2-R instalados y coinciden con sus fuentes.' -ForegroundColor Green
  Write-Host '[PASS] 18 skills Dev Team instaladas y coinciden con sus fuentes.' -ForegroundColor Green
  Write-Host '[PASS] Skills VX no aprobadas/workflows/reglas/plugins/runtime legacy no estan instalados.' -ForegroundColor Green
  Write-Host '[PASS] Este verificador no modifica ni autentica MCP.' -ForegroundColor Green
  return
}

$stamp = (Get-Date -Format 'yyyyMMdd-HHmmss-fff') + '-' + ([guid]::NewGuid().ToString('N').Substring(0,8))
$backupDir = Join-Path $backupRoot $stamp
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
$entries = [System.Collections.ArrayList]::new()
$index = 0

foreach ($name in $approvedAgents.Keys) {
  Backup-Target $backupDir $entries (Join-Path $agentDir $name) 'file' $index
  $index++
}
Backup-Target $backupDir $entries $agentsFile 'file' $index
$index++
foreach ($name in $approvedSkills.Keys) {
  Backup-Target $backupDir $entries (Join-Path $skillDir $name) 'dir' $index
  $index++
}
foreach ($item in $legacy) {
  Backup-Target $backupDir $entries $item.Path $item.Kind $index
  $index++
}

$configHashBefore = Hash-File $configFile
$manifest = [ordered]@{
  schema='dev-team-v2r-backup/1'
  created=$stamp
  home=$homeRoot
  config_hash_before=$configHashBefore
  approved_agents=@($approvedAgents.Keys)
  approved_skills=@($approvedSkills.Keys)
  entries=@($entries)
}
Save-Manifest $backupDir $manifest

try {
  foreach ($item in $legacy) {
    if (Test-Path -LiteralPath $item.Path) { Remove-Item -LiteralPath $item.Path -Recurse -Force }
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
  foreach ($pair in $approvedAgents.GetEnumerator()) {
    Copy-Item -LiteralPath $pair.Value -Destination (Join-Path $agentDir $pair.Key) -Force
  }

  New-Item -ItemType Directory -Path $skillDir -Force | Out-Null
  foreach ($pair in $approvedSkills.GetEnumerator()) {
    $target = Join-Path $skillDir $pair.Key
    if (Test-Path -LiteralPath $target) { Remove-Item -LiteralPath $target -Recurse -Force }
    Copy-Item -LiteralPath $pair.Value -Destination $target -Recurse -Force
  }

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

Write-Host '[PASS] Baseline aplicado: Dev Team + 10 subagentes ocultos read-only + 18 skills allowlistadas.' -ForegroundColor Green
Write-Host '[PASS] kilo.jsonc y configuracion MCP preservados.' -ForegroundColor Green
Write-Host "BACKUP: $backupDir" -ForegroundColor Yellow
Write-Host 'Ejecuta este mismo script con -Modo Verificar y luego /reload en Kilo.' -ForegroundColor Cyan
