param(
  [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference='Stop'

$fixture = Join-Path $env:RUNNER_TEMP ('vx-meeting-current-' + [guid]::NewGuid().ToString('N'))
$installer = (Resolve-Path (Join-Path $RepoRoot 'scripts/Instalar-Kilo-Global-Harness.ps1')).Path

& $installer -Modo Aplicar -RaizUsuario $fixture

$core = Join-Path $fixture '.config/kilo/harness/scripts/vx_evolution_core.py'
$db = Join-Path $fixture '.config/kilo/vx-evolution/vx-evolution.sqlite3'

if (!(Test-Path -LiteralPath $core -PathType Leaf)) {
  throw 'Core VX Evolution no instalado.'
}
if (Test-Path -LiteralPath $db) {
  throw 'El instalador no debe inicializar SQLite.'
}

$calendar = python -I $core --home $fixture meeting-joint-calendar --on-date 2026-11-14 --json |
  ConvertFrom-Json
if ($LASTEXITCODE -ne 0 -or
    $calendar.local_date -ne '2026-12-07' -or
    $calendar.local_time -ne '09:00' -or
    $calendar.session_count -ne 1 -or
    $calendar.acta_sections -ne 2 -or
    $calendar.scheduler_enabled) {
  throw 'Contrato de calendario conjunto instalado incumplido.'
}
if (Test-Path -LiteralPath $db) {
  throw 'La vista previa de calendario no debe escribir SQLite.'
}

python -I $core --home $fixture init --json | Out-Null
if ($LASTEXITCODE -ne 0 -or !(Test-Path -LiteralPath $db -PathType Leaf)) {
  throw 'Init de VX Evolution instalado fallo.'
}

$status = python -I $core --home $fixture status --json | ConvertFrom-Json
if ($LASTEXITCODE -ne 0 -or
    $status.schema_version -ne 4 -or
    !$status.joint_sessions_supported -or
    $status.scheduled_meetings) {
  throw 'Estado instalado de reuniones/SQLite v4 incorrecto.'
}

$integrity = python -I $core --home $fixture integrity --json | ConvertFrom-Json
if ($LASTEXITCODE -ne 0 -or
    $integrity.database -ne 'ok' -or
    !$integrity.foreign_keys) {
  throw 'Integridad SQLite instalada fallo.'
}

$backup = Get-ChildItem (Join-Path $fixture '.config/kilo-harness-backups') -Directory |
  Sort-Object LastWriteTimeUtc -Descending |
  Select-Object -First 1
if (!$backup) {
  throw 'No existe backup para rollback.'
}

& $installer -Modo Restaurar -RaizUsuario $fixture -BackupFolder $backup.FullName

if (Test-Path -LiteralPath $core) {
  throw 'Rollback no retiro el core instalado.'
}
if (!(Test-Path -LiteralPath $db -PathType Leaf)) {
  throw 'Rollback nunca debe borrar la SQLite privada inicializada.'
}

Write-Host 'VX MEETING CURRENT WINDOWS SMOKE: INSTALLED CORE + JOINT CALENDAR + SQLITE V4 + ROLLBACK PASS'
