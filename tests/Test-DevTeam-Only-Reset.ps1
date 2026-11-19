#Requires -Version 7.0
$ErrorActionPreference = 'Stop'

$repo = Split-Path $PSScriptRoot -Parent
$installer = Join-Path $repo 'scripts/Instalar-DevTeam-Only.ps1'
$tmp = Join-Path ([IO.Path]::GetTempPath()) ('devteam-v2r-test-' + [guid]::NewGuid().ToString('N'))

$approved = @(
  'vx-dev-team.md',
  'vx-dev-explorer.md',
  'vx-dev-architect.md',
  'vx-dev-frontend.md',
  'vx-dev-backend.md',
  'vx-dev-data.md',
  'vx-dev-platform.md',
  'vx-dev-quality.md',
  'vx-dev-security.md',
  'vx-dev-research.md'
)

try {
  $kilo = Join-Path $tmp '.config/kilo'
  New-Item -ItemType Directory -Force -Path (
    (Join-Path $kilo 'agents'),
    (Join-Path $kilo 'commands'),
    (Join-Path $kilo 'rules'),
    (Join-Path $kilo 'plugin'),
    (Join-Path $kilo 'harness/scripts'),
    (Join-Path $tmp '.kilo/skills/vx-old'),
    (Join-Path $tmp '.kilo/skills/third-party'),
    (Join-Path $tmp '.agents/skills/vx-old'),
    (Join-Path $tmp '.kilocode/skills/vx-old')
  ) | Out-Null

  $config = Join-Path $kilo 'kilo.jsonc'
  @'
{
  // sentinel
  "mcp": {
    "KEEP_ME": {
      "type": "remote",
      "url": "https://example.invalid/mcp"
    }
  }
}
'@ | Set-Content -LiteralPath $config -Encoding UTF8
  $configHashBefore = (Get-FileHash -LiteralPath $config -Algorithm SHA256).Hash

  'OLD DEV TEAM' | Set-Content -LiteralPath (Join-Path $kilo 'agents/vx-dev-team.md') -Encoding UTF8
  'OLD CHILD' | Set-Content -LiteralPath (Join-Path $kilo 'agents/vx-dev-explorer.md') -Encoding UTF8
  'OLD COMBINED CHILD' | Set-Content -LiteralPath (Join-Path $kilo 'agents/vx-dev-backend-data.md') -Encoding UTF8
  'LEGACY BACKEND' | Set-Content -LiteralPath (Join-Path $kilo 'agents/vx-backend-builder.md') -Encoding UTF8
  'LEGACY INTEGRATOR' | Set-Content -LiteralPath (Join-Path $kilo 'agents/vx-integrador.md') -Encoding UTF8
  'THIRD PARTY' | Set-Content -LiteralPath (Join-Path $kilo 'agents/my-agent.md') -Encoding UTF8

  'LEGACY COMMAND' | Set-Content -LiteralPath (Join-Path $kilo 'commands/vx-pack.md') -Encoding UTF8
  'LEGACY RULE' | Set-Content -LiteralPath (Join-Path $kilo 'rules/vx-global-harness-v3.md') -Encoding UTF8
  'LEGACY PLUGIN' | Set-Content -LiteralPath (Join-Path $kilo 'plugin/vx-observer-light.js') -Encoding UTF8
  '{}' | Set-Content -LiteralPath (Join-Path $kilo 'harness/vx-old.json') -Encoding UTF8
  'print("legacy")' | Set-Content -LiteralPath (Join-Path $kilo 'harness/scripts/vx_old.py') -Encoding UTF8

  'name: vx-old' | Set-Content -LiteralPath (Join-Path $tmp '.kilo/skills/vx-old/SKILL.md') -Encoding UTF8
  'name: third-party' | Set-Content -LiteralPath (Join-Path $tmp '.kilo/skills/third-party/SKILL.md') -Encoding UTF8
  'name: vx-old' | Set-Content -LiteralPath (Join-Path $tmp '.agents/skills/vx-old/SKILL.md') -Encoding UTF8
  'name: vx-old' | Set-Content -LiteralPath (Join-Path $tmp '.kilocode/skills/vx-old/SKILL.md') -Encoding UTF8

  @'
KEEP-BEFORE
<!-- VX-HARNESS-V3:BEGIN -->
LEGACY MANAGED BLOCK
<!-- VX-HARNESS-V3:END -->
KEEP-AFTER
'@ | Set-Content -LiteralPath (Join-Path $kilo 'AGENTS.md') -Encoding UTF8

  & $installer -Modo Diagnostico -RaizUsuario $tmp
  & $installer -Modo Simular -RaizUsuario $tmp

  if (!(Test-Path -LiteralPath (Join-Path $kilo 'agents/vx-backend-builder.md'))) {
    throw 'Simular modifico el HOME.'
  }

  & $installer -Modo Aplicar -RaizUsuario $tmp
  & $installer -Modo Verificar -RaizUsuario $tmp

  foreach ($name in $approved) {
    $path = Join-Path $kilo ('agents/' + $name)
    if (!(Test-Path -LiteralPath $path -PathType Leaf)) { throw "Falta aprobado instalado: $name" }
  }

  $leader = Get-Content -LiteralPath (Join-Path $kilo 'agents/vx-dev-team.md') -Raw -Encoding UTF8
  if ($leader -notmatch '(?m)^  task:\s*$' -or
      $leader -notmatch '(?m)^    "vx-dev-explorer":\s*allow\s*$') {
    throw 'Dev Team no puede delegar al pool V2-R.'
  }

  foreach ($name in $approved | Where-Object { $_ -ne 'vx-dev-team.md' }) {
    $child = Get-Content -LiteralPath (Join-Path $kilo ('agents/' + $name)) -Raw -Encoding UTF8
    foreach ($pat in @(
      '(?m)^mode:\s*subagent\s*$',
      '(?m)^hidden:\s*true\s*$',
      '(?m)^  read:\s*deny\s*$',
      '(?m)^  edit:\s*deny\s*$',
      '(?m)^  write:\s*deny\s*$',
      '(?m)^  bash:\s*deny\s*$',
      '(?m)^  task:\s*deny\s*$'
    )) {
      if ($child -notmatch $pat) { throw "Subagente $name no cumple read-only/hidden: $pat" }
    }
  }

  foreach ($path in @(
    (Join-Path $kilo 'agents/vx-backend-builder.md'),
    (Join-Path $kilo 'agents/vx-integrador.md'),
    (Join-Path $kilo 'commands/vx-pack.md'),
    (Join-Path $kilo 'rules/vx-global-harness-v3.md'),
    (Join-Path $kilo 'plugin/vx-observer-light.js'),
    (Join-Path $kilo 'harness/vx-old.json'),
    (Join-Path $kilo 'harness/scripts/vx_old.py'),
    (Join-Path $tmp '.kilo/skills/vx-old'),
    (Join-Path $tmp '.agents/skills/vx-old'),
    (Join-Path $tmp '.kilocode/skills/vx-old')
  )) {
    if (Test-Path -LiteralPath $path) { throw "No se retiro legacy: $path" }
  }

  if (Test-Path -LiteralPath (Join-Path $kilo 'agents/vx-dev-backend-data.md')) {
    throw 'No se retiro el subagente combinado supersedido.'
  }

  if (!(Test-Path -LiteralPath (Join-Path $kilo 'agents/my-agent.md'))) {
    throw 'Se elimino agente de terceros.'
  }
  if (!(Test-Path -LiteralPath (Join-Path $tmp '.kilo/skills/third-party/SKILL.md'))) {
    throw 'Se elimino skill de terceros.'
  }

  $agentsText = Get-Content -LiteralPath (Join-Path $kilo 'AGENTS.md') -Raw -Encoding UTF8
  if ($agentsText -notmatch 'KEEP-BEFORE' -or $agentsText -notmatch 'KEEP-AFTER') {
    throw 'Se perdio contenido ajeno de AGENTS.md.'
  }
  if ($agentsText -match 'VX-HARNESS-V3') {
    throw 'No se retiro bloque VX legacy de AGENTS.md.'
  }

  $configHashAfter = (Get-FileHash -LiteralPath $config -Algorithm SHA256).Hash
  if ($configHashBefore -ne $configHashAfter) {
    throw 'kilo.jsonc fue modificado.'
  }

  $backup = Get-ChildItem -LiteralPath (Join-Path $tmp '.config/kilo-devteam-backups') -Directory |
    Sort-Object Name -Descending | Select-Object -First 1
  if (!$backup) { throw 'No se creo backup.' }

  & $installer -Modo Restaurar -RaizUsuario $tmp -BackupFolder $backup.FullName

  if ((Get-Content -LiteralPath (Join-Path $kilo 'agents/vx-dev-team.md') -Raw -Encoding UTF8) -notmatch 'OLD DEV TEAM') {
    throw 'Restore no recupero Dev Team previo.'
  }
  if ((Get-Content -LiteralPath (Join-Path $kilo 'agents/vx-dev-explorer.md') -Raw -Encoding UTF8) -notmatch 'OLD CHILD') {
    throw 'Restore no recupero subagente previo.'
  }
  if ((Get-Content -LiteralPath (Join-Path $kilo 'agents/vx-dev-backend-data.md') -Raw -Encoding UTF8) -notmatch 'OLD COMBINED CHILD') {
    throw 'Restore no recupero el subagente combinado previo.'
  }

  foreach ($name in $approved | Where-Object { $_ -notin @('vx-dev-team.md','vx-dev-explorer.md') }) {
    if (Test-Path -LiteralPath (Join-Path $kilo ('agents/' + $name))) {
      throw "Restore dejo agente que no existia antes: $name"
    }
  }

  foreach ($path in @(
    (Join-Path $kilo 'agents/vx-backend-builder.md'),
    (Join-Path $kilo 'agents/vx-integrador.md'),
    (Join-Path $kilo 'commands/vx-pack.md'),
    (Join-Path $tmp '.kilo/skills/vx-old')
  )) {
    if (!(Test-Path -LiteralPath $path)) { throw "Restore no recupero: $path" }
  }

  $restoredAgents = Get-Content -LiteralPath (Join-Path $kilo 'AGENTS.md') -Raw -Encoding UTF8
  if ($restoredAgents -notmatch 'LEGACY MANAGED BLOCK') {
    throw 'Restore no recupero AGENTS.md.'
  }
  if ($configHashBefore -ne (Get-FileHash -LiteralPath $config -Algorithm SHA256).Hash) {
    throw 'Restore altero kilo.jsonc.'
  }

  Write-Host 'DEV TEAM V2-R: APPLY + VERIFY + 9 HIDDEN NON-MUTATING CHILDREN + PLATFORM + BACKEND/DATA SPLIT + RESTORE PASS' -ForegroundColor Green
}
finally {
  if (Test-Path -LiteralPath $tmp) {
    Remove-Item -LiteralPath $tmp -Recurse -Force -ErrorAction SilentlyContinue
  }
}
