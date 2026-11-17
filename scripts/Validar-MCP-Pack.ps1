#Requires -Version 7.0
[CmdletBinding()]
param(
  [string]$KiloConfig,
  [switch]$Json
)

$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$registryPath = Join-Path $root 'registry\vx-mcp-catalog-v2.json'
$installerPath = Join-Path $root 'scripts\Instalar-MCP-Pack-Windows.ps1'
$wrapperPath = Join-Path $root 'scripts\mcp\github-mcp-kilo.ps1'
$docPath = Join-Path $root 'docs\VX-MCP-PACK-WINDOWS-V1-20261117.md'

$errors = [System.Collections.Generic.List[string]]::new()
$warnings = [System.Collections.Generic.List[string]]::new()

foreach ($path in @($registryPath,$installerPath,$wrapperPath,$docPath)) {
  if (!(Test-Path -LiteralPath $path -PathType Leaf)) {
    $errors.Add("Falta archivo requerido: $path")
  }
}

$ids = @()
if (Test-Path -LiteralPath $registryPath -PathType Leaf) {
  try {
    $registry = Get-Content -LiteralPath $registryPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($registry.schema -ne 'vx-mcp-catalog/2') { $errors.Add('Schema MCP inesperado.') }
    if (@($registry.servers).Count -ne 13) { $errors.Add("Se esperaban 13 servidores; encontrados $(@($registry.servers).Count).") }

    $requiredFields = @('id','status','transport','description','source','dependencies','install','kilo','auth','risk')
    foreach ($server in @($registry.servers)) {
      foreach ($field in $requiredFields) {
        if ($null -eq $server.$field -or ([string]$server.$field).Length -eq 0) {
          $errors.Add("Servidor '$($server.id)' sin campo requerido '$field'.")
        }
      }
      if ($server.id) { $ids += [string]$server.id }
    }

    $unique = @($ids | Sort-Object -Unique)
    if ($unique.Count -ne $ids.Count) { $errors.Add('Hay IDs MCP duplicados.') }
  } catch {
    $errors.Add("Registro V2 inválido: $($_.Exception.Message)")
  }
}

$expected = @(
  'codebase-memory','ida','playwright','context7','imagegen','github',
  'cloudflare-api','chrome-devtools','snyk','postman','microsoft-learn',
  'sentry','serena'
)
foreach ($id in $expected) {
  if ($id -notin $ids) { $errors.Add("Falta ID canónico: $id") }
}

if (Test-Path -LiteralPath $installerPath -PathType Leaf) {
  $installer = Get-Content -LiteralPath $installerPath -Raw -Encoding UTF8
  foreach ($id in $expected) {
    if ($installer -notmatch [regex]::Escape($id)) { $errors.Add("Instalador no referencia MCP: $id") }
  }
  foreach ($endpoint in @(
    'https://mcp.context7.com/mcp',
    'https://mcp.cloudflare.com/mcp',
    'https://mcp.postman.com/minimal',
    'https://learn.microsoft.com/api/mcp',
    'https://mcp.sentry.dev/mcp'
  )) {
    if ($installer -notmatch [regex]::Escape($endpoint)) { $errors.Add("Instalador no contiene endpoint: $endpoint") }
  }
}

if (Test-Path -LiteralPath $wrapperPath -PathType Leaf) {
  $wrapper = Get-Content -LiteralPath $wrapperPath -Raw -Encoding UTF8
  if ($wrapper -notmatch 'gh auth token') { $errors.Add('Wrapper GitHub no obtiene credencial mediante gh auth token.') }
  if ($wrapper -match '(ghp_|gho_|github_pat_)') { $errors.Add('Wrapper GitHub parece contener un token literal.') }
}

if ($KiloConfig) {
  if (!(Test-Path -LiteralPath $KiloConfig -PathType Leaf)) {
    $errors.Add("No existe KiloConfig: $KiloConfig")
  } else {
    try {
      $cfg = Get-Content -LiteralPath $KiloConfig -Raw -Encoding UTF8 | ConvertFrom-Json
      $names = @($cfg.mcp.PSObject.Properties.Name)
      foreach ($id in $expected) {
        if ($id -notin $names) { $warnings.Add("KiloConfig no contiene: $id") }
      }
    } catch {
      $errors.Add("KiloConfig no se pudo leer: $($_.Exception.Message)")
    }
  }
}

$result = [ordered]@{
  schema = 'vx-mcp-pack-validation/1'
  valid = ($errors.Count -eq 0)
  server_count = $ids.Count
  expected_count = 13
  errors = @($errors)
  warnings = @($warnings)
}

if ($Json) {
  $result | ConvertTo-Json -Depth 10
} else {
  Write-Host '=== VX MCP PACK | VALIDACION ESTATICA ===' -ForegroundColor Cyan
  Write-Host "Servidores: $($result.server_count)/13"
  if ($errors.Count -eq 0) { Write-Host '[OK] Registro y pack coherentes.' -ForegroundColor Green }
  foreach ($w in $warnings) { Write-Warning $w }
  foreach ($e in $errors) { Write-Host "[ERROR] $e" -ForegroundColor Red }
}

if ($errors.Count -gt 0) { exit 1 }
exit 0
