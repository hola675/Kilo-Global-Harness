#Requires -Version 7.0
$ErrorActionPreference = 'Stop'

$repo = Split-Path $PSScriptRoot -Parent
$installer = Join-Path $repo 'scripts/Instalar-DevTeam-Only.ps1'
$tmp = Join-Path ([IO.Path]::GetTempPath()) ('devteam-only-test-' + [guid]::NewGuid().ToString('N'))

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

  $dev = Get-Content -LiteralPath (Join-Path $kilo 'agents/vx-dev-team.md') -Raw -Encoding UTF8
  if ($dev -notmatch '(?m)^  skill:\s*deny\s*$' -or $dev -notmatch '(?m)^  task:\s*deny\s*$') {
    throw 'Dev Team instalado no es singleton.'
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

  Write-Host 'DEV TEAM ONLY RESET: APPLY + VERIFY + RESTORE PASS' -ForegroundColor Green
}
finally {
  if (Test-Path -LiteralPath $tmp) {
    Remove-Item -LiteralPath $tmp -Recurse -Force -ErrorAction SilentlyContinue
  }
}
