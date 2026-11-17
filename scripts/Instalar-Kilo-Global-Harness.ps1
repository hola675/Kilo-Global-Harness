#Requires -Version 7.0
<#
.SYNOPSIS
  VECIDYA | Kilo Global Harness V4 / Pack VX 0.1.0 - instalador global, idempotente y reversible.
.DESCRIPTION
  No instala archivos dentro de ningun repositorio. No altera kilo.jsonc, modelos,
  credenciales, MCP, AutoApprove, steps ni permisos existentes.
  Diagnostico, Simular y Verificar son de solo lectura.
  Aplicar guarda backup privado, instala assets globales y conserva un manifiesto.
.EXAMPLE
  pwsh -NoProfile -File .\scripts\Instalar-Kilo-Global-Harness.ps1 -Modo Diagnostico
  pwsh -NoProfile -File .\scripts\Instalar-Kilo-Global-Harness.ps1 -Modo Simular
  pwsh -NoProfile -File .\scripts\Instalar-Kilo-Global-Harness.ps1 -Modo Aplicar -PausarTaskObserver
  pwsh -NoProfile -File .\scripts\Instalar-Kilo-Global-Harness.ps1 -Modo Verificar
  pwsh -NoProfile -File .\scripts\Instalar-Kilo-Global-Harness.ps1 -Modo Restaurar -BackupFolder <ruta>
#>
[CmdletBinding()]
param(
  [ValidateSet('Diagnostico','Simular','Aplicar','Verificar','Restaurar')]
  [string]$Modo = 'Diagnostico',
  [switch]$PausarTaskObserver,
  [switch]$InstalarVXObserverV44,
  [string]$BackupFolder,
  [switch]$ForzarRestauracion,
  [string]$RaizUsuario
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if ($RaizUsuario) {
  if (![IO.Path]::IsPathFullyQualified($RaizUsuario)) { throw 'RaizUsuario debe ser una ruta absoluta.' }
  $homeRoot = [IO.Path]::GetFullPath($RaizUsuario)
  if ($homeRoot.StartsWith(([IO.Path]::GetFullPath($root) + [IO.Path]::DirectorySeparatorChar),[StringComparison]::OrdinalIgnoreCase)) {
    throw 'RaizUsuario no puede estar dentro del repositorio del harness.'
  }
} else { $homeRoot = $HOME }
$kiloDir = Join-Path $homeRoot '.config/kilo'
$skillRoot = Join-Path $homeRoot '.kilo/skills'
$agentsSkillRoot = Join-Path $homeRoot '.agents/skills'
$legacySkillRoot = Join-Path $homeRoot '.kilocode/skills'
$globalAgentsFile = Join-Path $kiloDir 'AGENTS.md'
$configFile = Join-Path $kiloDir 'kilo.jsonc'
$observerPath = Join-Path $skillRoot 'task-observer'
$backupRoot = Join-Path $homeRoot '.config/kilo-harness-backups'
$startMarker = '<!-- VX-HARNESS-V3:BEGIN -->'
$endMarker = '<!-- VX-HARNESS-V3:END -->'

function Hash-File([string]$Path) {
  if (!(Test-Path -LiteralPath $Path -PathType Leaf)) { return $null }
  return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
}
function Read-Utf8([string]$Path) {
  return [IO.File]::ReadAllText($Path, [Text.Encoding]::UTF8)
}
function Write-Utf8Atomic([string]$Path,[string]$Text) {
  $dir = Split-Path $Path -Parent
  New-Item -Path $dir -ItemType Directory -Force | Out-Null
  $tmp = Join-Path $dir ('.vx-tmp-' + [guid]::NewGuid().ToString('N'))
  try {
    [IO.File]::WriteAllText($tmp,$Text,[Text.UTF8Encoding]::new($false))
    Move-Item -LiteralPath $tmp -Destination $Path -Force
  } finally {
    if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -Force }
  }
}
function Read-JsonFile([string]$Path) {
  return (Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json -AsHashtable)
}
function Save-JsonFile([string]$Path,$Value) {
  Write-Utf8Atomic $Path ((ConvertTo-Json -InputObject $Value -Depth 40) + "`n")
}
function Read-KiloMetadata {
  if (!(Test-Path -LiteralPath $configFile -PathType Leaf)) { return $null }
  # System.Text.Json tolera JSONC: comentarios y comas finales, sin reescritura.
  $opt = [System.Text.Json.JsonDocumentOptions]::new()
  $opt.CommentHandling = [System.Text.Json.JsonCommentHandling]::Skip
  $opt.AllowTrailingCommas = $true
  $doc = [System.Text.Json.JsonDocument]::Parse((Read-Utf8 $configFile), $opt)
  try {
    $rootEl = $doc.RootElement
    $a = [System.Text.Json.JsonElement]::new()
    $m = [System.Text.Json.JsonElement]::new()
    $names = @()
    $high = 0
    $loose = 0
    $mcpNames = @()
    if ($rootEl.TryGetProperty('agent',[ref]$a) -and $a.ValueKind -eq 'Object') {
      foreach ($p in $a.EnumerateObject()) {
        $names += $p.Name
        $s = [System.Text.Json.JsonElement]::new()
        if ($p.Value.TryGetProperty('steps',[ref]$s) -and $s.ValueKind -eq 'Number') {
          if ($s.GetDouble() -gt 400) { $high++ }
        }
        $permission = [System.Text.Json.JsonElement]::new()
        if ($p.Value.TryGetProperty('permission',[ref]$permission) -and $permission.ValueKind -eq 'Object') {
          foreach ($name in @('edit','bash')) {
            $v = [System.Text.Json.JsonElement]::new()
            if ($permission.TryGetProperty($name,[ref]$v) -and $v.ValueKind -eq 'String' -and $v.GetString() -eq 'allow') { $loose++; break }
          }
        }
      }
    }
    if ($rootEl.TryGetProperty('mcp',[ref]$m) -and $m.ValueKind -eq 'Object') {
      foreach ($p in $m.EnumerateObject()) { $mcpNames += $p.Name }
    }
    return [pscustomobject]@{
      Agents = @($names)
      MCP = @($mcpNames)
      HighSteps = $high
      UnrestrictedAgentCount = $loose
    }
  } finally { $doc.Dispose() }
}
function Skill-Names([string]$RootPath) {
  if (!(Test-Path -LiteralPath $RootPath)) { return @() }
  return @(Get-ChildItem -LiteralPath $RootPath -Directory -ErrorAction SilentlyContinue |
    Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') } |
    Select-Object -ExpandProperty Name)
}
function Global-Assets {
  $assets = @()
  $rulesSource = Join-Path $root 'rules/vx-global-harness-v3.md'
  $assets += [pscustomobject]@{Source=$rulesSource; Target=(Join-Path $kiloDir 'rules/vx-global-harness-v3.md')}
  foreach ($dir in @('commands','agents')) {
    $src = Join-Path $root $dir
    foreach ($f in @(Get-ChildItem -LiteralPath $src -Filter '*.md' -File -ErrorAction Stop)) {
      $assets += [pscustomobject]@{Source=$f.FullName;Target=(Join-Path (Join-Path $kiloDir $dir) $f.Name)}
    }
  }
  # Pack VX: exclusivamente skills del registro VX; configuraciones de terceros intactas.
  $pack = Read-JsonFile (Join-Path $root 'registry/vx-agent-registry-v4.json')
  if (!$pack.ContainsKey('pack') -or @($pack.pack.owned_skills).Count -lt 2) {
    throw 'Pack VX sin lista cerrada de skills.'
  }
  $seenSkills = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
  foreach ($entry in @($pack.pack.owned_skills)) {
    $name = [string]$entry
    if ($name -notmatch '^vx-[a-z0-9-]+$' -or !$seenSkills.Add($name)) {
      throw "Skill VX invalida o duplicada: $name"
    }
    $src = Join-Path $root ("skills/{0}/SKILL.md" -f $name)
    if (!(Test-Path -LiteralPath $src -PathType Leaf)) { throw "Falta skill VX: $name" }
    $assets += [pscustomobject]@{Source=$src;Target=(Join-Path (Join-Path $skillRoot $name) 'SKILL.md')}
  }
  # V4.4: plugin opt-in SOLO cuando el operador lo solicita.
  # Al instalarlo, sigue INERTE hasta activar observer-mode light en la BD.
  if ($InstalarVXObserverV44) {
    $assets += [pscustomobject]@{
      Source=(Join-Path $root 'plugins/vx-observer-light.js');
      Target=(Join-Path $kiloDir 'plugin/vx-observer-light.js')
    }
  }
  # V4.3: nucleo operativo Kilo-only (NO inicializa ni toca la BD privada).
  $assets += [pscustomobject]@{
    Source=(Join-Path $root 'scripts/vx_evolution_core.py');
    Target=(Join-Path $kiloDir 'harness/scripts/vx_evolution_core.py')
  }
  # V4.6.0: auditoría de capacidades global y sin acceso a SQLite.
  $assets += [pscustomobject]@{
    Source=(Join-Path $root 'scripts/vx_capability_audit.py');
    Target=(Join-Path $kiloDir 'harness/scripts/vx_capability_audit.py')
  }
  # V4.6.1: matriz de competencias y evidencias DECLARADAS, de solo lectura.
  $assets += [pscustomobject]@{
    Source=(Join-Path $root 'scripts/vx_competency_matrix.py');
    Target=(Join-Path $kiloDir 'harness/scripts/vx_competency_matrix.py')
  }
  # V4.6.2: ensayos sintéticos y comparación declarativa, solo lectura.
  $assets += [pscustomobject]@{
    Source=(Join-Path $root 'scripts/vx_competency_trials.py');
    Target=(Join-Path $kiloDir 'harness/scripts/vx_competency_trials.py')
  }
  # V4.6.3: diagnóstico organizativo de metadatos sin cambiar el runtime.
  $assets += [pscustomobject]@{
    Source=(Join-Path $root 'scripts/vx_organizational_audit.py');
    Target=(Join-Path $kiloDir 'harness/scripts/vx_organizational_audit.py')
  }
  # Recursos adicionales V4 - SIEMPRE en perfil global, nunca en repositorios.
  $assets += [pscustomobject]@{
    Source=(Join-Path $root 'registry/vx-agent-registry-v4.json');
    Target=(Join-Path $kiloDir 'harness/vx-agent-registry-v4.json')
  }
  # Matriz DAG y router de skills: únicamente metadatos, sin cambios MCP ni permisos.
  $assets += [pscustomobject]@{
    Source=(Join-Path $root 'registry/vx-skill-dependencies-v1.json');
    Target=(Join-Path $kiloDir 'harness/vx-skill-dependencies-v1.json')
  }
  $assets += [pscustomobject]@{
    Source=(Join-Path $root 'scripts/vx_skill_router.py');
    Target=(Join-Path $kiloDir 'harness/scripts/vx_skill_router.py')
  }
  $assets += [pscustomobject]@{
    Source=(Join-Path $root 'scripts/vx_task_dag.py');
    Target=(Join-Path $kiloDir 'harness/scripts/vx_task_dag.py')
  }
  # Catalogo MCP pasivo y diagnostico sin secretos.
  $assets += [pscustomobject]@{
    Source=(Join-Path $root 'registry/vx-mcp-catalog-v1.json');
    Target=(Join-Path $kiloDir 'harness/vx-mcp-catalog-v1.json')
  }
  # V2 registra el pack operativo de 13 MCP. Sigue siendo metadato pasivo:
  # este instalador general NO instala, autentica ni modifica servidores MCP.
  $assets += [pscustomobject]@{
    Source=(Join-Path $root 'registry/vx-mcp-catalog-v2.json');
    Target=(Join-Path $kiloDir 'harness/vx-mcp-catalog-v2.json')
  }
  $assets += [pscustomobject]@{
    Source=(Join-Path $root 'scripts/Validar-MCP-Pack.ps1');
    Target=(Join-Path $kiloDir 'harness/scripts/Validar-MCP-Pack.ps1')
  }
  $assets += [pscustomobject]@{
    Source=(Join-Path $root 'scripts/vx_pack_doctor.py');
    Target=(Join-Path $kiloDir 'harness/scripts/vx_pack_doctor.py')
  }
  foreach ($name in @('Seleccionar-Equipo-V4.ps1','Validar-Registro-V4.ps1','Reconciliar-Agentes-V4.2.ps1')) {
    $assets += [pscustomobject]@{
      Source=(Join-Path (Join-Path $root 'scripts') $name);
      Target=(Join-Path (Join-Path $kiloDir 'harness/scripts') $name)
    }
  }
  return @($assets)
}
function Managed-AgentsBlock {
  $source = Read-Utf8 (Join-Path $root 'rules/AGENTS-global-managed.md')
  return ($startMarker + "`n" + $source.Trim() + "`n" + $endMarker)
}
function Replace-ManagedBlock([string]$Original,[string]$Block) {
  $beg = $Original.IndexOf($startMarker,[StringComparison]::Ordinal)
  $end = $Original.IndexOf($endMarker,[StringComparison]::Ordinal)
  if (($beg -ge 0) -xor ($end -ge 0)) { throw 'AGENTS.md contiene marcadores incompletos; no se sobrescribe.' }
  if ($beg -ge 0) {
    if ($end -lt $beg) { throw 'Marcadores de AGENTS.md desordenados.' }
    $finish = $end + $endMarker.Length
    return ($Original.Substring(0,$beg) + $Block + $Original.Substring($finish))
  }
  if ([string]::IsNullOrWhiteSpace($Original)) { return ($Block + "`n") }
  return ($Original.TrimEnd() + "`n`n" + $Block + "`n")
}
function Report-State {
  Write-Host "=== VECIDYA | KILO GLOBAL HARNESS V4 | $Modo ===" -ForegroundColor Cyan
  Write-Host "Configuracion principal: $configFile (existe: $(Test-Path $configFile))"
  try {
    $meta = Read-KiloMetadata
    if ($null -ne $meta) {
      Write-Host "Agentes JSON: $(@($meta.Agents).Count); steps > 400: $($meta.HighSteps); edit/bash allow global: $($meta.UnrestrictedAgentCount)"
      Write-Host "MCP configurados ($(@($meta.MCP).Count)): $(@($meta.MCP) -join ', ')"
      $mdAgents = @(Get-ChildItem (Join-Path $kiloDir 'agents') -Filter '*.md' -File -ErrorAction SilentlyContinue | ForEach-Object BaseName)
      $duplicates = @($meta.Agents | Where-Object { $_ -in $mdAgents })
      Write-Host "Agentes duplicados JSON/Markdown: $($duplicates.Count)"
    }
  } catch { Write-Warning "No se pudo interpretar metadata JSONC: $($_.Exception.Message)" }
  $global = @(Skill-Names $skillRoot)
  $compatible = @(Skill-Names $agentsSkillRoot)
  $legacy = @(Skill-Names $legacySkillRoot)
  Write-Host "Skills: .kilo=$($global.Count), .agents=$($compatible.Count), .kilocode=$($legacy.Count)"
  $dups = @(($global + $compatible + $legacy) | Group-Object | Where-Object { $_.Count -gt 1 })
  Write-Host "Skills repetidas por nombre: $($dups.Count)"
  Write-Host "task-observer activa: $(Test-Path $observerPath)"
  Write-Host "VX Observer instalado: $(Test-Path (Join-Path $kiloDir 'plugin/vx-observer-light.js')) (modo de captura independiente)"
  if (!$RaizUsuario -and $env:APPDATA) {
    $settingsFile = Join-Path $env:APPDATA 'Code/User/settings.json'
    if (Test-Path $settingsFile) {
      $auto = Select-String -LiteralPath $settingsFile -Pattern 'kilo-code\.new\.autoApprove\.enabled' -ErrorAction SilentlyContinue
      Write-Host "AutoApprove: clave presente en Settings (no modificada): $([bool]$auto)"
    }
  }
  Write-Host 'Los datos MCP solo acreditan configuracion, no conexiones activas.'
}
function Save-Manifest($Manifest) {
  Save-JsonFile (Join-Path $Manifest.BackupFolder 'manifest.json') $Manifest
}
function Assert-NoReparse([string]$Path) {
  $cursor = [IO.Path]::GetFullPath($Path)
  while ($true) {
    if (Test-Path -LiteralPath $cursor) {
      $item = Get-Item -LiteralPath $cursor -Force
      if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
        throw 'Ruta de backup/restauracion contiene junction o enlace simbolico.'
      }
    }
    $parent = [IO.Path]::GetDirectoryName($cursor)
    if ([string]::IsNullOrEmpty($parent) -or $parent -eq $cursor) { break }
    $cursor = $parent
  }
}
function Assert-VXRestoreTarget([string]$Path) {
  if (![IO.Path]::IsPathFullyQualified($Path)) { throw 'Destino de restauracion no es ruta absoluta.' }
  $full = [IO.Path]::GetFullPath($Path)
  $relative = [IO.Path]::GetRelativePath($homeRoot,$full).Replace('\','/')
  $patterns = @(
    '^\.config/kilo/AGENTS\.md$',
    '^\.config/kilo/(agents|commands)/vx-[a-z0-9-]+\.md$',
    '^\.config/kilo/rules/vx-[a-z0-9-]+\.md$',
    '^\.config/kilo/harness/vx-[a-z0-9-]+\.json$',
    '^\.config/kilo/harness/scripts/(vx_[a-z0-9_]+\.py|Seleccionar-Equipo-V4\.ps1|Validar-Registro-V4\.ps1|Reconciliar-Agentes-V4\.2\.ps1|Auditar-Kilo-Global\.ps1|Validar-MCP-Pack\.ps1),
    '^\.config/kilo/plugin/vx-observer-light\.js$',
    '^\.kilo/skills/vx-[a-z0-9-]+/SKILL\.md$'
  )
  if (@($patterns | Where-Object { $relative -match $_ }).Count -eq 0) {
    throw "Destino fuera del alcance VX: $relative"
  }
  Assert-NoReparse $full
  return $full
}
function Restore-Manifest([string]$Dir,[bool]$Force) {
  if (![IO.Path]::IsPathFullyQualified($Dir)) { throw 'BackupFolder debe ser ruta absoluta.' }
  $actual = [IO.Path]::GetFullPath($Dir).TrimEnd('\','/')
  $rootBackup = [IO.Path]::GetFullPath($backupRoot).TrimEnd('\','/')
  if (![string]::Equals([IO.Path]::GetDirectoryName($actual),$rootBackup,[StringComparison]::OrdinalIgnoreCase)) {
    throw 'BackupFolder debe ser hijo directo del directorio de backups VX.'
  }
  Assert-NoReparse $actual
  $path = Join-Path $actual 'manifest.json'
  if (!(Test-Path -LiteralPath $path -PathType Leaf)) { throw "No existe manifiesto: $path" }
  $m = Read-JsonFile $path
  if ($m.version -notin @('3.0.0','4.0.0')) { throw 'Version de manifiesto incompatible.' }
  if ($m.BackupFolder -and ![string]::Equals([IO.Path]::GetFullPath([string]$m.BackupFolder),$actual,[StringComparison]::OrdinalIgnoreCase)) {
    throw 'Manifiesto no pertenece al backup indicado.'
  }
  if (@($m.files).Count -lt 1) { throw 'Manifiesto sin archivos.' }
  $toRestore = @()
  $seenTargets = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
  foreach ($entry in @($m.files)) {
    $target = Assert-VXRestoreTarget ([string]$entry.target)
    if (!$seenTargets.Add($target)) { throw 'Destino duplicado en manifiesto.' }
    $shaCurrent = Hash-File $target
    if (!$Force -and $shaCurrent) {
      if (!$entry.installedSha256 -or $shaCurrent -ne [string]$entry.installedSha256) {
        throw 'Un archivo fue alterado tras instalar VX; restauración bloqueada sin cambios parciales.'
      }
    }
    $copy = $null
    if ($entry.existed) {
      $copy = [string]$entry.backup
      if (![IO.Path]::IsPathFullyQualified($copy) -or
          ![string]::Equals([IO.Path]::GetDirectoryName([IO.Path]::GetFullPath($copy)),$actual,[StringComparison]::OrdinalIgnoreCase) -or
          !(Test-Path -LiteralPath $copy -PathType Leaf)) {
        throw 'Respaldo de archivo faltante o fuera del directorio autorizado.'
      }
      Assert-NoReparse $copy
    }
    $toRestore += [pscustomobject]@{ Target=$target; Existed=[bool]$entry.existed; Backup=$copy }
  }
  if ($m.observerMoved) {
    $obs = [string]$m.observerBackup
    if (![IO.Path]::IsPathFullyQualified($obs) -or
        ![string]::Equals([IO.Path]::GetDirectoryName([IO.Path]::GetFullPath($obs)),$actual,[StringComparison]::OrdinalIgnoreCase)) {
      throw 'Respaldo de observer fuera del directorio autorizado.'
    }
    Assert-NoReparse $obs
    Assert-NoReparse $observerPath
  }
  # Solo despues de validar absolutamente todo comienza la restauracion.
  $restored = 0
  foreach ($entry in $toRestore) {
    if ($entry.Existed) {
      New-Item -Path (Split-Path $entry.Target -Parent) -ItemType Directory -Force | Out-Null
      Copy-Item -LiteralPath $entry.Backup -Destination $entry.Target -Force
    } elseif (Test-Path -LiteralPath $entry.Target -PathType Leaf) {
      Remove-Item -LiteralPath $entry.Target -Force
    }
    $restored++
  }
  if ($m.observerMoved) {
    if ((Test-Path -LiteralPath $m.observerBackup) -and !(Test-Path -LiteralPath $observerPath)) {
      New-Item -Path (Split-Path $observerPath -Parent) -ItemType Directory -Force | Out-Null
      Move-Item -LiteralPath $m.observerBackup -Destination $observerPath
      Write-Host 'task-observer restaurada.'
    } else { Write-Warning 'task-observer requiere restauracion manual; no se sobreescribio.' }
  }
  Write-Host "Restaurados: $restored; pendientes: 0" -ForegroundColor Green
}

if ($Modo -eq 'Restaurar') {
  if ([string]::IsNullOrWhiteSpace($BackupFolder)) { throw 'Debes especificar -BackupFolder.' }
  Restore-Manifest $BackupFolder ([bool]$ForzarRestauracion)
  return
}
# Validacion de roles y rutas antes de escribir. Si falla, no tocar la instalacion.
$validator = Join-Path $root 'scripts/Validar-Registro-V4.ps1'
if (!(Test-Path -LiteralPath $validator -PathType Leaf)) { throw 'Falta el validador V4.' }
& $validator -RaizFuentes $root
$assets = @(Global-Assets)
$expectedPaths = @($assets | ForEach-Object Target)
if ($expectedPaths.Count -ne @($expectedPaths | Select-Object -Unique).Count) { throw 'Colision de rutas internas en el paquete.' }
foreach ($a in $assets) {
  if (!(Test-Path -LiteralPath $a.Source -PathType Leaf)) { throw "Paquete incompleto: $($a.Source)" }
  Assert-NoReparse $a.Source
  Assert-NoReparse $a.Target
}
Assert-NoReparse $globalAgentsFile
$block = Managed-AgentsBlock
$currentAgents = if (Test-Path -LiteralPath $globalAgentsFile) { Read-Utf8 $globalAgentsFile } else { '' }
$plannedAgents = Replace-ManagedBlock $currentAgents $block
$allItems = @($assets) + @([pscustomobject]@{Source=$null;Target=$globalAgentsFile})
if ($Modo -eq 'Diagnostico') { Report-State; Write-Host 'DIAGNOSTICO sin cambios.' -ForegroundColor Green; return }
if ($Modo -eq 'Simular') {
  Report-State
  foreach ($item in $allItems) {
    $exists = Test-Path -LiteralPath $item.Target -PathType Leaf
    $state = if ($exists) {'ACTUALIZAR SI CAMBIA'}else{'CREAR'}
    Write-Host "[$state] $($item.Target)"
  }
  if ($PausarTaskObserver) { Write-Host "[PAUSAR] $observerPath (respaldo privado)" }
  Write-Host 'SIMULACION sin cambios.' -ForegroundColor Green
  return
}
if ($Modo -eq 'Verificar') {
  $fail = 0
  foreach ($item in $assets) {
    $ok = (Hash-File $item.Source) -eq (Hash-File $item.Target)
    if (!$ok) { $fail++ }
    Write-Host "[$(if($ok){'OK'}else{'DIFERENTE'})] $($item.Target)"
  }
  $currentAgents = if (Test-Path $globalAgentsFile) { Read-Utf8 $globalAgentsFile } else { '' }
  $ok = $currentAgents.Contains($block)
  if (!$ok) { $fail++ }
  Write-Host "[$(if($ok){'OK'}else{'DIFERENTE'})] Seccion administrada de AGENTS.md"
  if ($fail -gt 0) { throw "Verificacion incompleta: $fail elementos." }
  Write-Host 'VERIFICACION DE ARCHIVOS: OK. Falta prueba funcional de Kilo en Windows.' -ForegroundColor Green
  return
}

# Modo Aplicar; por diseno solo toca rutas globales y archivos VX del paquete.
$stamp = (Get-Date -Format 'yyyyMMdd-HHmmss-fff') + '-' + ([guid]::NewGuid().ToString('N').Substring(0,8))
$backupDir = Join-Path $backupRoot $stamp
New-Item -Path $backupDir -ItemType Directory -Force | Out-Null
$manifest = [ordered]@{
  version='4.0.0'; created=$stamp; BackupFolder=$backupDir;
  files=@(); observerMoved=$false; observerBackup=''
}
$index=0
foreach ($item in $allItems) {
  $target = $item.Target
  $existed = Test-Path -LiteralPath $target -PathType Leaf
  $backupFile = ''
  if ($existed) {
    $backupFile = Join-Path $backupDir ("file-$index.bak")
    Copy-Item -LiteralPath $target -Destination $backupFile -Force
  }
  $manifest.files += [ordered]@{target=$target;existed=[bool]$existed;backup=$backupFile;installedSha256=$null}
  $index++
}
Save-Manifest $manifest
try {
  $index=0
  foreach ($item in $assets) {
    $text = Read-Utf8 $item.Source
    Write-Utf8Atomic $item.Target $text
    $manifest.files[$index].installedSha256 = Hash-File $item.Target
    Save-Manifest $manifest
    $index++
  }
  Write-Utf8Atomic $globalAgentsFile $plannedAgents
  $manifest.files[$index].installedSha256 = Hash-File $globalAgentsFile
  Save-Manifest $manifest
  if ($PausarTaskObserver -and (Test-Path -LiteralPath $observerPath)) {
    $dest = Join-Path $backupDir 'task-observer-pausado'
    Move-Item -LiteralPath $observerPath -Destination $dest
    $manifest.observerMoved = $true
    $manifest.observerBackup = $dest
    Save-Manifest $manifest
  }
} catch {
  $msg=$_.Exception.Message
  Write-Warning "Instalacion interrumpida: $msg. Intentando restaurar..."
  Restore-Manifest $backupDir $true
  throw "No se completo Aplicar: $msg"
}
Write-Host 'APLICACION V4.4 COMPLETADA: solo rutas globales; AutoApprove, modelos, MCP y JSONC intactos.' -ForegroundColor Green
Write-Host "BACKUP PRIVADO (NO SUBIR): $backupDir" -ForegroundColor Yellow
Write-Host 'Ejecuta -Modo Verificar, luego /reload en Kilo.'
,
    '^\.config/kilo/plugin/vx-observer-light\.js$',
    '^\.kilo/skills/vx-[a-z0-9-]+/SKILL\.md$'
  )
  if (@($patterns | Where-Object { $relative -match $_ }).Count -eq 0) {
    throw "Destino fuera del alcance VX: $relative"
  }
  Assert-NoReparse $full
  return $full
}
function Restore-Manifest([string]$Dir,[bool]$Force) {
  if (![IO.Path]::IsPathFullyQualified($Dir)) { throw 'BackupFolder debe ser ruta absoluta.' }
  $actual = [IO.Path]::GetFullPath($Dir).TrimEnd('\','/')
  $rootBackup = [IO.Path]::GetFullPath($backupRoot).TrimEnd('\','/')
  if (![string]::Equals([IO.Path]::GetDirectoryName($actual),$rootBackup,[StringComparison]::OrdinalIgnoreCase)) {
    throw 'BackupFolder debe ser hijo directo del directorio de backups VX.'
  }
  Assert-NoReparse $actual
  $path = Join-Path $actual 'manifest.json'
  if (!(Test-Path -LiteralPath $path -PathType Leaf)) { throw "No existe manifiesto: $path" }
  $m = Read-JsonFile $path
  if ($m.version -notin @('3.0.0','4.0.0')) { throw 'Version de manifiesto incompatible.' }
  if ($m.BackupFolder -and ![string]::Equals([IO.Path]::GetFullPath([string]$m.BackupFolder),$actual,[StringComparison]::OrdinalIgnoreCase)) {
    throw 'Manifiesto no pertenece al backup indicado.'
  }
  if (@($m.files).Count -lt 1) { throw 'Manifiesto sin archivos.' }
  $toRestore = @()
  $seenTargets = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
  foreach ($entry in @($m.files)) {
    $target = Assert-VXRestoreTarget ([string]$entry.target)
    if (!$seenTargets.Add($target)) { throw 'Destino duplicado en manifiesto.' }
    $shaCurrent = Hash-File $target
    if (!$Force -and $shaCurrent) {
      if (!$entry.installedSha256 -or $shaCurrent -ne [string]$entry.installedSha256) {
        throw 'Un archivo fue alterado tras instalar VX; restauración bloqueada sin cambios parciales.'
      }
    }
    $copy = $null
    if ($entry.existed) {
      $copy = [string]$entry.backup
      if (![IO.Path]::IsPathFullyQualified($copy) -or
          ![string]::Equals([IO.Path]::GetDirectoryName([IO.Path]::GetFullPath($copy)),$actual,[StringComparison]::OrdinalIgnoreCase) -or
          !(Test-Path -LiteralPath $copy -PathType Leaf)) {
        throw 'Respaldo de archivo faltante o fuera del directorio autorizado.'
      }
      Assert-NoReparse $copy
    }
    $toRestore += [pscustomobject]@{ Target=$target; Existed=[bool]$entry.existed; Backup=$copy }
  }
  if ($m.observerMoved) {
    $obs = [string]$m.observerBackup
    if (![IO.Path]::IsPathFullyQualified($obs) -or
        ![string]::Equals([IO.Path]::GetDirectoryName([IO.Path]::GetFullPath($obs)),$actual,[StringComparison]::OrdinalIgnoreCase)) {
      throw 'Respaldo de observer fuera del directorio autorizado.'
    }
    Assert-NoReparse $obs
    Assert-NoReparse $observerPath
  }
  # Solo despues de validar absolutamente todo comienza la restauracion.
  $restored = 0
  foreach ($entry in $toRestore) {
    if ($entry.Existed) {
      New-Item -Path (Split-Path $entry.Target -Parent) -ItemType Directory -Force | Out-Null
      Copy-Item -LiteralPath $entry.Backup -Destination $entry.Target -Force
    } elseif (Test-Path -LiteralPath $entry.Target -PathType Leaf) {
      Remove-Item -LiteralPath $entry.Target -Force
    }
    $restored++
  }
  if ($m.observerMoved) {
    if ((Test-Path -LiteralPath $m.observerBackup) -and !(Test-Path -LiteralPath $observerPath)) {
      New-Item -Path (Split-Path $observerPath -Parent) -ItemType Directory -Force | Out-Null
      Move-Item -LiteralPath $m.observerBackup -Destination $observerPath
      Write-Host 'task-observer restaurada.'
    } else { Write-Warning 'task-observer requiere restauracion manual; no se sobreescribio.' }
  }
  Write-Host "Restaurados: $restored; pendientes: 0" -ForegroundColor Green
}

if ($Modo -eq 'Restaurar') {
  if ([string]::IsNullOrWhiteSpace($BackupFolder)) { throw 'Debes especificar -BackupFolder.' }
  Restore-Manifest $BackupFolder ([bool]$ForzarRestauracion)
  return
}
# Validacion de roles y rutas antes de escribir. Si falla, no tocar la instalacion.
$validator = Join-Path $root 'scripts/Validar-Registro-V4.ps1'
if (!(Test-Path -LiteralPath $validator -PathType Leaf)) { throw 'Falta el validador V4.' }
& $validator -RaizFuentes $root
$assets = @(Global-Assets)
$expectedPaths = @($assets | ForEach-Object Target)
if ($expectedPaths.Count -ne @($expectedPaths | Select-Object -Unique).Count) { throw 'Colision de rutas internas en el paquete.' }
foreach ($a in $assets) {
  if (!(Test-Path -LiteralPath $a.Source -PathType Leaf)) { throw "Paquete incompleto: $($a.Source)" }
  Assert-NoReparse $a.Source
  Assert-NoReparse $a.Target
}
Assert-NoReparse $globalAgentsFile
$block = Managed-AgentsBlock
$currentAgents = if (Test-Path -LiteralPath $globalAgentsFile) { Read-Utf8 $globalAgentsFile } else { '' }
$plannedAgents = Replace-ManagedBlock $currentAgents $block
$allItems = @($assets) + @([pscustomobject]@{Source=$null;Target=$globalAgentsFile})
if ($Modo -eq 'Diagnostico') { Report-State; Write-Host 'DIAGNOSTICO sin cambios.' -ForegroundColor Green; return }
if ($Modo -eq 'Simular') {
  Report-State
  foreach ($item in $allItems) {
    $exists = Test-Path -LiteralPath $item.Target -PathType Leaf
    $state = if ($exists) {'ACTUALIZAR SI CAMBIA'}else{'CREAR'}
    Write-Host "[$state] $($item.Target)"
  }
  if ($PausarTaskObserver) { Write-Host "[PAUSAR] $observerPath (respaldo privado)" }
  Write-Host 'SIMULACION sin cambios.' -ForegroundColor Green
  return
}
if ($Modo -eq 'Verificar') {
  $fail = 0
  foreach ($item in $assets) {
    $ok = (Hash-File $item.Source) -eq (Hash-File $item.Target)
    if (!$ok) { $fail++ }
    Write-Host "[$(if($ok){'OK'}else{'DIFERENTE'})] $($item.Target)"
  }
  $currentAgents = if (Test-Path $globalAgentsFile) { Read-Utf8 $globalAgentsFile } else { '' }
  $ok = $currentAgents.Contains($block)
  if (!$ok) { $fail++ }
  Write-Host "[$(if($ok){'OK'}else{'DIFERENTE'})] Seccion administrada de AGENTS.md"
  if ($fail -gt 0) { throw "Verificacion incompleta: $fail elementos." }
  Write-Host 'VERIFICACION DE ARCHIVOS: OK. Falta prueba funcional de Kilo en Windows.' -ForegroundColor Green
  return
}

# Modo Aplicar; por diseno solo toca rutas globales y archivos VX del paquete.
$stamp = (Get-Date -Format 'yyyyMMdd-HHmmss-fff') + '-' + ([guid]::NewGuid().ToString('N').Substring(0,8))
$backupDir = Join-Path $backupRoot $stamp
New-Item -Path $backupDir -ItemType Directory -Force | Out-Null
$manifest = [ordered]@{
  version='4.0.0'; created=$stamp; BackupFolder=$backupDir;
  files=@(); observerMoved=$false; observerBackup=''
}
$index=0
foreach ($item in $allItems) {
  $target = $item.Target
  $existed = Test-Path -LiteralPath $target -PathType Leaf
  $backupFile = ''
  if ($existed) {
    $backupFile = Join-Path $backupDir ("file-$index.bak")
    Copy-Item -LiteralPath $target -Destination $backupFile -Force
  }
  $manifest.files += [ordered]@{target=$target;existed=[bool]$existed;backup=$backupFile;installedSha256=$null}
  $index++
}
Save-Manifest $manifest
try {
  $index=0
  foreach ($item in $assets) {
    $text = Read-Utf8 $item.Source
    Write-Utf8Atomic $item.Target $text
    $manifest.files[$index].installedSha256 = Hash-File $item.Target
    Save-Manifest $manifest
    $index++
  }
  Write-Utf8Atomic $globalAgentsFile $plannedAgents
  $manifest.files[$index].installedSha256 = Hash-File $globalAgentsFile
  Save-Manifest $manifest
  if ($PausarTaskObserver -and (Test-Path -LiteralPath $observerPath)) {
    $dest = Join-Path $backupDir 'task-observer-pausado'
    Move-Item -LiteralPath $observerPath -Destination $dest
    $manifest.observerMoved = $true
    $manifest.observerBackup = $dest
    Save-Manifest $manifest
  }
} catch {
  $msg=$_.Exception.Message
  Write-Warning "Instalacion interrumpida: $msg. Intentando restaurar..."
  Restore-Manifest $backupDir $true
  throw "No se completo Aplicar: $msg"
}
Write-Host 'APLICACION V4.4 COMPLETADA: solo rutas globales; AutoApprove, modelos, MCP y JSONC intactos.' -ForegroundColor Green
Write-Host "BACKUP PRIVADO (NO SUBIR): $backupDir" -ForegroundColor Yellow
Write-Host 'Ejecuta -Modo Verificar, luego /reload en Kilo.'
