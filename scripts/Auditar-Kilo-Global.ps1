#Requires -Version 7.0
<#
.SYNOPSIS
 Auditoria global segura de Kilo Code. Solo lectura; nunca imprime credenciales.
.EXAMPLE
 pwsh -NoProfile -File .\scripts\Auditar-Kilo-Global.ps1
 pwsh -NoProfile -File .\scripts\Auditar-Kilo-Global.ps1 -Json
#>
[CmdletBinding()]
param(
  [string]$RaizUsuario = $HOME,
  [switch]$Json
)
$ErrorActionPreference = 'Stop'
if (![IO.Path]::IsPathFullyQualified($RaizUsuario)) { throw 'RaizUsuario debe ser absoluta.' }
$homeRoot = [IO.Path]::GetFullPath($RaizUsuario)
$configDir = Join-Path $homeRoot '.config/kilo'
$configFile = Join-Path $configDir 'kilo.jsonc'

function Read-Jsonc([string]$Path) {
  if (!(Test-Path -LiteralPath $Path -PathType Leaf)) { return $null }
  $opt = [System.Text.Json.JsonDocumentOptions]::new()
  $opt.CommentHandling = [System.Text.Json.JsonCommentHandling]::Skip
  $opt.AllowTrailingCommas = $true
  return [System.Text.Json.JsonDocument]::Parse([IO.File]::ReadAllText($Path),$opt)
}
function Get-Skills([string]$Path) {
  if (!(Test-Path -LiteralPath $Path)) { return @() }
  return @(Get-ChildItem -LiteralPath $Path -Directory -ErrorAction SilentlyContinue |
    Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') } |
    ForEach-Object Name)
}
function Get-Plugins([string]$Path) {
  $doc = Read-Jsonc $Path
  if (!$doc) { return @() }
  try {
    $prop = [System.Text.Json.JsonElement]::new()
    if (!$doc.RootElement.TryGetProperty('plugin',[ref]$prop)) { return @() }
    if ($prop.ValueKind -ne 'Array') { return @() }
    return @($prop.EnumerateArray() | Where-Object { $_.ValueKind -eq 'String' } |
      ForEach-Object { $_.GetString() })
  } finally { $doc.Dispose() }
}

$agents = @()
$mcp = @()
$configOk = $false
$doc = Read-Jsonc $configFile
if ($doc) {
  $configOk = $true
  try {
    $root = $doc.RootElement
    $agentProp = [System.Text.Json.JsonElement]::new()
    if ($root.TryGetProperty('agent',[ref]$agentProp) -and $agentProp.ValueKind -eq 'Object') {
      foreach ($entry in $agentProp.EnumerateObject()) {
        $steps = $null
        $s = [System.Text.Json.JsonElement]::new()
        if ($entry.Value.ValueKind -eq 'Object' -and
          $entry.Value.TryGetProperty('steps',[ref]$s) -and $s.ValueKind -eq 'Number') {
          $steps = $s.GetDouble()
        }
        $agents += [pscustomobject]@{
          name = $entry.Name
          steps = $steps
          high_steps = ($null -ne $steps -and $steps -gt 400)
        }
      }
    }
    $mcpProp = [System.Text.Json.JsonElement]::new()
    if ($root.TryGetProperty('mcp',[ref]$mcpProp) -and $mcpProp.ValueKind -eq 'Object') {
      foreach ($entry in $mcpProp.EnumerateObject()) {
        $enabled = 'no-declarado'
        $e = [System.Text.Json.JsonElement]::new()
        if ($entry.Value.ValueKind -eq 'Object' -and
          $entry.Value.TryGetProperty('enabled',[ref]$e)) {
          if ($e.ValueKind -eq 'True') { $enabled = 'true' }
          elseif ($e.ValueKind -eq 'False') { $enabled = 'false' }
        }
        $mcp += [pscustomobject]@{name=$entry.Name;enabled=$enabled}
      }
    }
  } finally { $doc.Dispose() }
}
$agentsPath = Join-Path $configDir 'agents'
$mdAgents = @()
if (Test-Path -LiteralPath $agentsPath) {
  $mdAgents = @(Get-ChildItem -LiteralPath $agentsPath -File -Filter '*.md' |
    Select-Object -ExpandProperty BaseName)
}
$duplicates = @($agents | Where-Object { $_.name -in $mdAgents } |
  Select-Object -ExpandProperty name)

$skillRoots = [ordered]@{
  kilo = (Join-Path $homeRoot '.kilo/skills')
  agents = (Join-Path $homeRoot '.agents/skills')
  legacy = (Join-Path $homeRoot '.kilocode/skills')
}
$skillInventory = [ordered]@{}
foreach ($k in $skillRoots.Keys) { $skillInventory[$k] = @(Get-Skills $skillRoots[$k]) }
$allNames = @($skillInventory.Values | ForEach-Object { $_ })
$skillDuplicates = @($allNames | Group-Object | Where-Object Count -gt 1 | ForEach-Object Name)

$autoApprove = 'no-verificado'
$settingsFile = if ($env:APPDATA -and !$PSBoundParameters.ContainsKey('RaizUsuario')) {
  Join-Path $env:APPDATA 'Code/User/settings.json'
} else {
  Join-Path $homeRoot 'AppData/Roaming/Code/User/settings.json'
}
try {
  $settings = Read-Jsonc $settingsFile
  if ($settings) {
    try {
      $v=[System.Text.Json.JsonElement]::new()
      if ($settings.RootElement.TryGetProperty('kilo-code.new.autoApprove.enabled',[ref]$v)) {
        if ($v.ValueKind -eq 'True') { $autoApprove = 'true' }
        elseif ($v.ValueKind -eq 'False') { $autoApprove = 'false' }
      }
    } finally { $settings.Dispose() }
  }
} catch { $autoApprove = 'no-verificado' }

$pluginFiles=[ordered]@{
  server=(Join-Path $configDir 'opencode.json')
  tui=(Join-Path $configDir 'tui.json')
}
$plugins=[ordered]@{}
foreach ($key in $pluginFiles.Keys) {
  try { $plugins[$key] = @(Get-Plugins $pluginFiles[$key]) }
  catch { $plugins[$key] = @('ERROR_AL_LEER') }
}
$sharedPlugins = @($plugins.server | Where-Object { $_ -in $plugins.tui })
$result = [ordered]@{
  audit_schema = 'vx-kilo-global-audit/1'
  config_present = $configOk
  agents_inline_count = $agents.Count
  agents_markdown_count = $mdAgents.Count
  duplicates_merged_by_kilo = @($duplicates)
  high_steps_over_400 = @($agents | Where-Object high_steps | Select-Object name,steps)
  mcp_configured_only = @($mcp)
  imagegen_configured = [bool](@($mcp | Where-Object name -eq 'imagegen').Count)
  skills_by_global_root = $skillInventory
  repeated_skill_names = @($skillDuplicates)
  plugin_entries_by_target = $plugins
  plugins_in_both_targets = @($sharedPlugins)
  auto_approve_settings_file = $autoApprove
  limitations = @(
    'No verifica conexion MCP ni herramientas efectivas de la sesion.'
    'No verifica que AutoApprove este operativo en el cliente.'
    'Las definiciones duplicadas de agentes se fusionan por precedencia: no prueba conflicto.'
    'Un plugin en server y TUI puede ser normal; no prueba doble ejecucion.'
    'No lee ni imprime valores de credenciales, modelos ni variables de entorno.'
  )
}
if ($Json) {
  $result | ConvertTo-Json -Depth 30
} else {
  Write-Host '=== VECIDYA | AUDITORIA GLOBAL KILO | SOLO LECTURA ===' -ForegroundColor Cyan
  Write-Host "Agentes: JSON=$($agents.Count); Markdown=$($mdAgents.Count); fusionados/duplicados=$($duplicates.Count)"
  Write-Host "Steps > 400: $(@($result.high_steps_over_400).Count)"
  Write-Host "Skills globales: .kilo=$($skillInventory.kilo.Count); .agents=$($skillInventory.agents.Count); heredadas=$($skillInventory.legacy.Count)"
  Write-Host "MCP configurados: $(@($mcp | ForEach-Object name) -join ', ')"
  Write-Host "ImageGen declarado: $($result.imagegen_configured) (conexion no verificada)"
  Write-Host "AutoApprove en settings: $autoApprove (runtime no verificado)"
  Write-Host "Plugins en ambos targets: $(@($sharedPlugins) -join ', ') (puede ser intencional)"
  Write-Host 'No se ha modificado ningun archivo.' -ForegroundColor Green
}
