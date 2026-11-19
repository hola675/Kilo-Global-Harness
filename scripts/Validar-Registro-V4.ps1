#Requires -Version 7.0
<#
.SYNOPSIS
  Valida registro de agentes globales de V4 sin ejecutar ni instalar componentes.
#>
[CmdletBinding()]
param(
  [string]$RaizFuentes = (Split-Path $PSScriptRoot -Parent),
  [string]$RutaRegistro
)
$ErrorActionPreference='Stop'
# Dos disposiciones admitidas: codigo fuente (repo/registry + repo/agents)
# y copia GLOBAL instalada (kilo/harness/registro + kilo/agents).
if (!$RutaRegistro) {
  $fromSource = Join-Path $RaizFuentes 'registry/vx-agent-registry-v4.json'
  $fromGlobal = Join-Path $RaizFuentes 'vx-agent-registry-v4.json'
  if (Test-Path -LiteralPath $fromSource -PathType Leaf) {
    $RutaRegistro = $fromSource
  } elseif (Test-Path -LiteralPath $fromGlobal -PathType Leaf) {
    $RutaRegistro = $fromGlobal
    $RaizFuentes = Split-Path $RaizFuentes -Parent
  } else {
    throw 'No se encuentra el registro V4 en fuente o instalacion global.'
  }
}
if (!(Test-Path -LiteralPath $RutaRegistro -PathType Leaf)) { throw "Registro no existe: $RutaRegistro" }
$data = Get-Content -LiteralPath $RutaRegistro -Raw -Encoding UTF8 | ConvertFrom-Json -AsHashtable
if ($data.schema -ne 'vx-agent-registry/1' -or $data.global_only -ne $true) { throw 'Esquema/alcance global invalido.' }
if ($data.execution.mode_default -ne 'strict' -or [int]$data.execution.max_writers -ne 1) {
  throw 'No se admite mas de un escritor o un modo por defecto distinto de strict.'
}
if ([int]$data.execution.max_parallel_readers -lt 1 -or [int]$data.execution.max_parallel_readers -gt 3) {
  throw 'El limite de lectores debe ser 1..3.'
}
$agents = @($data.agents)
$profiles = @($data.profiles)
if ($agents.Count -lt 3 -or $profiles.Count -lt 2) { throw 'Registro incompleto.' }
$seen = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($agent in $agents) {
  $id = [string]$agent.id
  if ($id -notmatch '^vx-[a-z0-9-]+$' -or !$seen.Add($id)) { throw "Agente invalido/repetido: $id" }
  $relative = [string]$agent.file
  if ($relative -ne ("agents/" + $id + ".md")) { throw "Ruta inesperada en $id." }
  $source = Join-Path $RaizFuentes $relative
  if (!(Test-Path -LiteralPath $source -PathType Leaf)) { throw "Falta agente $id." }
  $raw = Get-Content -LiteralPath $source -Raw -Encoding UTF8
  $match = [regex]::Match($raw,'\A---\r?\n([\s\S]*?)\r?\n---\r?\n')
  if (!$match.Success) { throw "Frontmatter invalido en $id." }
  $front = $match.Groups[1].Value
  if ($front -notmatch "(?m)^mode:\s*$([regex]::Escape([string]$agent.mode))\s*$") { throw "Modo inconsistente en $id." }
  $steps = [regex]::Match($front,'(?m)^steps:\s*(\d+)\s*$')
  if (!$steps.Success -or [int]$steps.Groups[1].Value -ne [int]$agent.steps) {
    throw "Steps del agente $id no coinciden con el registro."
  }
  if ([int]$agent.steps -lt 1 -or [int]$agent.steps -gt 400) { throw "Steps fuera de limites en $id." }
  # Kilo usa nombrespaced tool ids para MCP (servidor_tool). mcp:deny no basta.
  $guardIndex = $front.IndexOf('  "*": deny',[StringComparison]::Ordinal)
  $readIndex = $front.IndexOf('  read:',[StringComparison]::Ordinal)
  if ($guardIndex -lt 0 -or $readIndex -lt 0 -or $guardIndex -gt $readIndex) {
    throw "Agente sin fallback deny inicial para herramientas no listadas: $id."
  }
  if ($front -match '(?m)^  mcp:\s*deny\s*$') {
    throw "Declaracion mcp:deny no protege herramientas namespaced: $id."
  }
  if ($id -eq 'vx-dev-team') {
    if ($front -notmatch '(?m)^  skill:\s*$' -or
        $front -notmatch '(?m)^    "\*":\s*deny\s*$' -or
        $front -notmatch '(?m)^    "vx-dev-project-policy":\s*allow\s*$' -or
        $front -notmatch '(?m)^    "vx-dev-team-handoff":\s*allow\s*$' -or
        $front -notmatch '(?m)^  task:\s*$') {
      throw 'Dev Team V2-R requiere skills deny-by-default con allowlist exacta y delegacion allowlist.'
    }
  } elseif ($front -notmatch '(?m)^  skill:\s*allow\s*$') {
    throw "Agente sin carga controlada de skills: $id."
  }
  if ($agent.role -eq 'coordinator' -and $id -ne 'vx-dev-team') {
    if ($front -notmatch '(?m)^  task:\s*$' -or
        $front -notmatch '(?m)^    "\*":\s*deny\s*$' -or
        $front -notmatch '(?m)^    "vx-inspector":\s*allow\s*$' -or
        $front -notmatch '(?m)^  edit:\s*ask\s*$' -or
        $front -notmatch '(?m)^  bash:\s*ask\s*$') {
      throw 'Coordinador VX legacy requiere delegacion y escritura condicionada por el host.'
    }
  }
  if ($agent.writes -eq $false) {
    if ($front -notmatch '(?m)^\s{2}edit:\s*deny\s*$') { throw "Agente read-only sin edit deny: $id." }
    if ($front -match '(?m)^\s{2}bash:\s*allow\s*$') { throw "Agente read-only con bash allow: $id." }
    if ($front -match '(?m)^\s{2}task:\s*allow\s*$') { throw "Agente read-only puede delegar: $id." }
  }
  if ($agent.role -eq 'builder') {
    if ($agent.writes -ne $true -or $agent.mode -ne 'all') { throw "Builder no coherente: $id" }
    foreach ($pair in @(
      @{Key='edit';Value='ask'},
      @{Key='task';Value='deny'}, @{Key='agent_manager';Value='deny'}
    )) {
      $pat = '(?m)^\s{2}' + [regex]::Escape($pair.Key) + ':\s*' + [regex]::Escape($pair.Value) + '\s*$'
      if ($front -notmatch $pat) { throw "Builder $id sin permiso $($pair.Key) = $($pair.Value)" }
    }
    if ($front -notmatch '(?m)^\s{2}bash:\s*(ask|deny)\s*$') { throw "Builder bash inseguro: $id" }
  }
}
$profilesSeen = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($p in $profiles) {
  $name = [string]$p.id
  if ($name -notmatch '^[a-z][a-z0-9-]+$' -or !$profilesSeen.Add($name)) { throw "Perfil repetido/invalido: $name." }
  if (@($p.discover).Count -gt 3 -or @($p.review).Count -gt 3) { throw "Demasiados delegados en $name." }
  foreach ($phase in @('discover','review')) {
    $list = @($p[$phase])
    if (@($list | Select-Object -Unique).Count -ne $list.Count) { throw "Duplicado de $phase en $name." }
    foreach ($a in $list) {
      if (!$seen.Contains([string]$a)) { throw "Perfil $name referencia agente inexistente: $a." }
      $role = @($agents | Where-Object { $_.id -eq $a })[0]
      if ($role.writes -ne $false -or $role.mode -ne 'subagent') { throw "No es lector seguro: $a." }
    }
  }
  if ($p.writer -and $p.writer -ne 'code') { throw "Escritor no soportado en $name." }
  if ($p.ContainsKey('builder_candidate') -and $p.builder_candidate) {
    $matched = @($agents | Where-Object { $_.id -eq $p.builder_candidate -and $_.role -eq 'builder' })
    if ($matched.Count -ne 1) { throw "Builder no registrado en perfil $name" }
  }
}
if (!$profilesSeen.Contains('general')) { throw 'Falta perfil general.' }

# Dev Team source actual: único primario visible + diez subagentes ocultos read-only.
if ($data.execution.dev_team_primary -ne 'vx-dev-team' -or
    $data.execution.dev_team_display_name -ne 'vx-dev-team' -or
    $data.execution.dev_team_runtime -ne 'active-v1') {
  throw 'Registro Dev Team primario incompleto.'
}
$devTeam = @($agents | Where-Object { $_.id -eq 'vx-dev-team' })
if ($devTeam.Count -ne 1 -or $devTeam[0].mode -ne 'primary' -or
    $devTeam[0].role -ne 'coordinator' -or $devTeam[0].writes -ne $true) {
  throw 'vx-dev-team no esta registrado como coordinador primario.'
}
$devFile = Join-Path $RaizFuentes 'agents/vx-dev-team.md'
if (!(Test-Path -LiteralPath $devFile -PathType Leaf)) { throw 'Falta agente global vx-dev-team.' }
$devRaw = Get-Content -LiteralPath $devFile -Raw -Encoding UTF8
$devFrontMatch = [regex]::Match($devRaw,'\A---\r?\n([\s\S]*?)\r?\n---\r?\n')
if (!$devFrontMatch.Success) { throw 'Frontmatter Dev Team invalido.' }
$devFront = $devFrontMatch.Groups[1].Value
foreach ($required in @(
  '(?m)^displayName:\s*"vx-dev-team"\s*$',
  '(?m)^color:\s*"#8B5CF6"\s*$',
  '(?m)^\s{2}skill:\s*$',
  '(?m)^\s{4}"\*":\s*deny\s*$',
  '(?m)^\s{4}"vx-dev-project-policy":\s*allow\s*$',
  '(?m)^\s{4}"vx-dev-team-handoff":\s*allow\s*$',
  '(?m)^\s{2}task:\s*$',
  '(?m)^\s{4}"\*":\s*deny\s*$',
  '(?m)^\s{2}agent_manager:\s*deny\s*$',
  '(?m)^\s{2}board_read:\s*deny\s*$',
  '(?m)^\s{2}board_post:\s*deny\s*$'
)) {
  if ($devFront -notmatch $required) { throw "Dev Team V2-R fuera de contrato: $required" }
}
$childIds = @(
  'vx-dev-explorer','vx-dev-architect','vx-dev-frontend','vx-dev-backend',
  'vx-dev-data','vx-dev-platform','vx-dev-reviewer','vx-dev-quality',
  'vx-dev-security','vx-dev-research'
)
$childSkillMatrix = @{
  'vx-dev-explorer'  = @('vx-dev-codebase-investigation','vx-dev-debug-triage')
  'vx-dev-research'  = @('vx-dev-source-reconciliation','vx-dev-mcp-readonly')
  'vx-dev-architect' = @('vx-dev-architecture-decision','vx-dev-mcp-readonly','vx-dev-project-policy')
  'vx-dev-frontend'  = @('vx-dev-frontend-ux','vx-dev-accessibility','vx-dev-ui-state-system','vx-dev-debug-triage')
  'vx-dev-backend'   = @('vx-dev-backend-contracts','vx-dev-debug-triage')
  'vx-dev-data'      = @('vx-dev-data-migration')
  'vx-dev-platform'  = @('vx-dev-platform-delivery','vx-dev-debug-triage')
  'vx-dev-quality'   = @('vx-dev-test-strategy','vx-dev-accessibility')
  'vx-dev-security'  = @('vx-dev-security-threat-review','vx-dev-supply-chain-review','vx-dev-mcp-security')
  'vx-dev-reviewer'  = @('vx-dev-independent-review','vx-dev-project-policy')
}
foreach ($child in $childIds) {
  $pat = '(?m)^\s{4}"' + [regex]::Escape($child) + '":\s*allow\s*$'
  if ($devFront -notmatch $pat) { throw "Dev Team no puede delegar a $child." }
}
if ($devFront -match '(?m)^\s{2}"[a-z0-9-]+_\*":\s*(allow|ask)\s*$') {
  throw 'Dev Team no puede tener permisos MCP automaticos en V2-R.'
}

$runtimeAgentDir = Join-Path $RaizFuentes 'runtime/dev-team-v2r/agents'
$installedAgentDir = Join-Path $RaizFuentes 'agents'
$validateChildren = Test-Path -LiteralPath $runtimeAgentDir -PathType Container
if (!$validateChildren) {
  $validateChildren = $true
  foreach ($child in $childIds) {
    if (!(Test-Path -LiteralPath (Join-Path $installedAgentDir ($child + '.md')) -PathType Leaf)) {
      $validateChildren = $false
      break
    }
  }
}
if ($validateChildren) {
  foreach ($child in $childIds) {
    $childFile = Join-Path $runtimeAgentDir ($child + '.md')
    if (!(Test-Path -LiteralPath $childFile -PathType Leaf)) {
      $childFile = Join-Path $installedAgentDir ($child + '.md')
    }
    if (!(Test-Path -LiteralPath $childFile -PathType Leaf)) { throw "Falta subagente V2-R: $child" }
    $childRaw = Get-Content -LiteralPath $childFile -Raw -Encoding UTF8
    $childFrontMatch = [regex]::Match($childRaw,'\A---\r?\n([\s\S]*?)\r?\n---\r?\n')
    if (!$childFrontMatch.Success) { throw "Frontmatter invalido en subagente V2-R: $child" }
    $childFront = $childFrontMatch.Groups[1].Value
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
      '(?m)^\s{2}board_read:\s*deny\s*$',
      '(?m)^\s{2}board_post:\s*deny\s*$'
    )) {
      if ($childFront -notmatch $required) { throw "Subagente $child no es read-only/oculto: $required" }
    }
    if ($childFront -match '(?m)^\s{2}"[a-z0-9-]+_\*":\s*(allow|ask)\s*$') {
      throw "Subagente $child contiene permisos MCP automaticos."
    }
    foreach ($skill in $childSkillMatrix[$child]) {
      $skillPat = '(?m)^\s{4}"' + [regex]::Escape($skill) + '":\s*allow\s*$'
      if ($childFront -notmatch $skillPat) { throw "Subagente $child no permite skill aprobada: $skill" }
    }
  }
}

if (!$data.ContainsKey('pack') -or $data.pack.id -ne 'vx-development-team') { throw 'Pack VX ausente.' }
if (@($data.pack.owned_agents).Count -ne $agents.Count) { throw 'Pack VX no enumera todos los agentes.' }
foreach ($id in @($data.pack.owned_agents)) {
  if (!$seen.Contains([string]$id)) { throw "Agente VX no registrado: $id" }
}
$skillBase = Join-Path $RaizFuentes 'skills'
if (!(Test-Path -LiteralPath $skillBase -PathType Container)) {
  $userRoot = Split-Path (Split-Path $RaizFuentes -Parent) -Parent
  $skillBase = Join-Path $userRoot '.kilo/skills'
}
$seenPackSkills = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($entry in @($data.pack.owned_skills)) {
  $skill = [string]$entry
  if ($skill -notmatch '^vx-[a-z0-9-]+$' -or !$seenPackSkills.Add($skill)) { throw "Skill VX invalida: $skill" }
  $file = Join-Path (Join-Path $skillBase $skill) 'SKILL.md'
  if (!(Test-Path -LiteralPath $file -PathType Leaf)) { throw "Falta skill VX: $skill" }
  $skillText = Get-Content -LiteralPath $file -Raw -Encoding UTF8
  if ($skillText -notmatch ('(?m)^name:\s*' + [regex]::Escape($skill) + '\s*$')) {
    throw "Nombre de skill VX no coincide: $skill"
  }
}
$catalogPath = Join-Path $RaizFuentes 'registry/vx-mcp-catalog-v1.json'
if (!(Test-Path -LiteralPath $catalogPath -PathType Leaf)) {
  $catalogPath = Join-Path $RaizFuentes 'harness/vx-mcp-catalog-v1.json'
}
if (!(Test-Path -LiteralPath $catalogPath -PathType Leaf)) { throw 'Catalogo MCP VX ausente.' }
$catalog = Get-Content -LiteralPath $catalogPath -Raw -Encoding UTF8 | ConvertFrom-Json -AsHashtable
if ($catalog.schema -ne 'vx-mcp-catalog/1' -or $catalog.policy.installation -ne 'approval-per-server') {
  throw 'Catalogo MCP VX incompatible.'
}
foreach ($candidate in @($catalog.candidates)) {
  if ($candidate.enabled_by_default -ne $false) { throw 'MCP con activacion automatica.' }
}
Write-Host "[PASS] Registro V4: $($agents.Count) agentes, $($profiles.Count) perfiles, $($seenPackSkills.Count) skills VX, catalogo MCP pasivo." -ForegroundColor Green
