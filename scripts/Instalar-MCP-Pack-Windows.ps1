#Requires -Version 7.0
<#
.SYNOPSIS
  VX MCP Pack V1 para Kilo Desktop en Windows.
.DESCRIPTION
  Reproduce y registra el pack global de 13 MCP validado el 2026-11-17.
  Nunca guarda tokens en el repositorio ni en kilo.jsonc. OAuth sigue siendo interactivo.
  Preserva MCP no gestionados y crea backup antes de modificar la configuracion.
.EXAMPLE
  pwsh -NoProfile -File .\scripts\Instalar-MCP-Pack-Windows.ps1 -Modo Diagnostico
  pwsh -NoProfile -File .\scripts\Instalar-MCP-Pack-Windows.ps1 -Modo Aplicar
  pwsh -NoProfile -File .\scripts\Instalar-MCP-Pack-Windows.ps1 -Modo Verificar
#>
[CmdletBinding()]
param(
  [ValidateSet('Diagnostico','Aplicar','Verificar')]
  [string]$Modo = 'Diagnostico',
  [switch]$ActualizarLocales,
  [switch]$InstalarIDAPlugin,
  [switch]$SoloConfig,
  [string]$KiloConfig
)

$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$registryPath = Join-Path $root 'registry\vx-mcp-catalog-v2.json'
$githubWrapperSource = Join-Path $PSScriptRoot 'mcp\github-mcp-kilo.ps1'

if (-not $KiloConfig) {
  $KiloConfig = Join-Path $HOME '.config\kilo\kilo.jsonc'
}

$managedIds = @(
  'codebase-memory','ida','playwright','context7','imagegen','github',
  'cloudflare-api','chrome-devtools','snyk','postman','microsoft-learn',
  'sentry','serena'
)

function Write-Ok([string]$Message) { Write-Host "[OK] $Message" -ForegroundColor Green }
function Write-WarnMsg([string]$Message) { Write-Host "[WARN] $Message" -ForegroundColor Yellow }
function Write-InfoMsg([string]$Message) { Write-Host "[INFO] $Message" -ForegroundColor Cyan }

function Command-Path([string]$Name) {
  $cmd = Get-Command $Name -ErrorAction SilentlyContinue
  if ($cmd) { return $cmd.Source }
  return $null
}

function Require-Command([string]$Name,[string]$Reason) {
  $path = Command-Path $Name
  if (-not $path) { throw "Falta '$Name'. $Reason" }
  return $path
}

function Resolve-SnykCmd {
  $candidate = Join-Path $env:APPDATA 'npm\snyk.cmd'
  if (Test-Path -LiteralPath $candidate -PathType Leaf) { return $candidate }
  $cmd = Get-Command snyk.cmd -ErrorAction SilentlyContinue
  if ($cmd) { return $cmd.Source }
  return $null
}

function Read-Json([string]$Path) {
  if (!(Test-Path -LiteralPath $Path -PathType Leaf)) { throw "No existe: $Path" }
  return (Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json)
}

function Write-JsonAtomic([string]$Path,$Value) {
  $dir = Split-Path $Path -Parent
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  $tmp = Join-Path $dir ('.vx-mcp-' + [guid]::NewGuid().ToString('N') + '.tmp')
  try {
    $json = (ConvertTo-Json -InputObject $Value -Depth 80)
    [IO.File]::WriteAllText($tmp,$json + "`n",[Text.UTF8Encoding]::new($false))
    Move-Item -LiteralPath $tmp -Destination $Path -Force
  } finally {
    if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -Force }
  }
}

function Backup-KiloConfig {
  if (!(Test-Path -LiteralPath $KiloConfig -PathType Leaf)) { return $null }
  $backupRoot = Join-Path $HOME '.config\kilo-mcp-pack-backups'
  New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null
  $stamp = Get-Date -Format 'yyyyMMdd-HHmmss-fff'
  $target = Join-Path $backupRoot "kilo-$stamp.jsonc"
  Copy-Item -LiteralPath $KiloConfig -Destination $target -Force
  return $target
}

function Get-KiloExe {
  $running = Get-Process kilo -ErrorAction SilentlyContinue |
    Where-Object { $_.Path } |
    Select-Object -First 1 -ExpandProperty Path
  if ($running) { return $running }

  $base = Join-Path $env:LOCALAPPDATA 'KiloDesktop'
  if (Test-Path -LiteralPath $base) {
    $candidate = Get-ChildItem -LiteralPath $base -Directory -Filter 'app-*' -ErrorAction SilentlyContinue |
      Sort-Object Name -Descending |
      ForEach-Object { Join-Path $_.FullName 'resources\kilo\windows-x64-baseline\bin\kilo.exe' } |
      Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } |
      Select-Object -First 1
    if ($candidate) { return $candidate }
  }
  return $null
}

function Get-LatestRelease([string]$Repo) {
  $gh = Require-Command 'gh' 'GitHub CLI es necesario para descargas reproducibles.'
  $json = & $gh api "repos/$Repo/releases/latest"
  if ($LASTEXITCODE -ne 0) { throw "No se pudo consultar release: $Repo" }
  return ($json | ConvertFrom-Json)
}

function Download-ReleaseAsset([string]$Repo,[string]$Tag,[string]$AssetName,[string]$Directory) {
  $gh = Require-Command 'gh' 'GitHub CLI es necesario para descargar releases.'
  New-Item -ItemType Directory -Force -Path $Directory | Out-Null
  $target = Join-Path $Directory $AssetName
  Remove-Item -LiteralPath $target -Force -ErrorAction SilentlyContinue
  & $gh release download $Tag --repo $Repo --pattern $AssetName --dir $Directory
  if ($LASTEXITCODE -ne 0 -or !(Test-Path -LiteralPath $target -PathType Leaf)) {
    throw "Fallo descargando $Repo / $AssetName"
  }
  return $target
}

function Ensure-CodebaseMemory {
  $targetDir = Join-Path $env:LOCALAPPDATA 'Programs\codebase-memory-mcp'
  $exe = Join-Path $targetDir 'codebase-memory-mcp.exe'
  if ((Test-Path -LiteralPath $exe -PathType Leaf) -and -not $ActualizarLocales) {
    Write-Ok "Codebase Memory presente: $exe"
    return $exe
  }

  $release = Get-LatestRelease 'DeusData/codebase-memory-mcp'
  $asset = @($release.assets | Where-Object {
    $_.name -match '(?i)windows' -and $_.name -match '(?i)(amd64|x86_64)' -and
    $_.name -match '(?i)\.zip$' -and $_.name -notmatch '(?i)-ui-'
  }) | Select-Object -First 1
  if (-not $asset) { throw 'No se encontro asset Windows x64 de Codebase Memory.' }

  $temp = Join-Path $env:TEMP ('vx-cbm-' + [guid]::NewGuid().ToString('N'))
  New-Item -ItemType Directory -Force -Path $temp | Out-Null
  try {
    $archive = Download-ReleaseAsset 'DeusData/codebase-memory-mcp' $release.tag_name $asset.name $temp
    $extract = Join-Path $temp 'extract'
    Expand-Archive -LiteralPath $archive -DestinationPath $extract -Force
    $installer = Get-ChildItem -LiteralPath $extract -Filter 'install.ps1' -File -Recurse |
      Select-Object -First 1 -ExpandProperty FullName
    if (-not $installer) { throw 'Release Codebase Memory sin install.ps1.' }

    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $installer --skip-config "--dir=$targetDir"
    if ($LASTEXITCODE -ne 0) { throw 'Fallo instalador de Codebase Memory.' }
  } finally {
    Remove-Item -LiteralPath $temp -Recurse -Force -ErrorAction SilentlyContinue
  }

  if (!(Test-Path -LiteralPath $exe -PathType Leaf)) { throw "No aparecio $exe" }
  Write-Ok "Codebase Memory instalado: $exe"
  return $exe
}

function Ensure-GitHubMcp {
  $gh = Require-Command 'gh' 'Instala GitHub CLI y autentica con gh auth login.'
  & $gh auth status *> $null
  if ($LASTEXITCODE -ne 0) { throw 'GitHub CLI no esta autenticado. Ejecuta gh auth login.' }

  $base = Join-Path $env:LOCALAPPDATA 'Programs\github-mcp-server'
  $current = Join-Path $base 'current'
  $exe = Join-Path $current 'github-mcp-server.exe'
  $wrapper = Join-Path $base 'github-mcp-kilo.ps1'

  if (!(Test-Path -LiteralPath $exe -PathType Leaf) -or $ActualizarLocales) {
    $release = Get-LatestRelease 'github/github-mcp-server'
    $assetName = 'github-mcp-server_Windows_x86_64.zip'
    $asset = @($release.assets | Where-Object { $_.name -eq $assetName }) | Select-Object -First 1
    if (-not $asset) { throw "La release $($release.tag_name) no contiene $assetName" }

    $temp = Join-Path $env:TEMP ('vx-ghmcp-' + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Force -Path $temp | Out-Null
    try {
      $archive = Download-ReleaseAsset 'github/github-mcp-server' $release.tag_name $assetName $temp
      if ($asset.digest -and ([string]$asset.digest).StartsWith('sha256:')) {
        $expected = ([string]$asset.digest).Substring(7).ToLowerInvariant()
        $actual = (Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actual -ne $expected) { throw 'SHA256 incorrecto para GitHub MCP.' }
        Write-Ok 'GitHub MCP: SHA256 verificado.'
      }
      if (Test-Path -LiteralPath $current) { Remove-Item -LiteralPath $current -Recurse -Force }
      New-Item -ItemType Directory -Force -Path $current | Out-Null
      Expand-Archive -LiteralPath $archive -DestinationPath $current -Force
    } finally {
      Remove-Item -LiteralPath $temp -Recurse -Force -ErrorAction SilentlyContinue
    }
  }

  New-Item -ItemType Directory -Force -Path $base | Out-Null
  Copy-Item -LiteralPath $githubWrapperSource -Destination $wrapper -Force
  if (!(Test-Path -LiteralPath $exe -PathType Leaf)) { throw "No aparecio $exe" }
  Write-Ok "GitHub MCP presente: $exe"
  return $wrapper
}

function Ensure-Snyk {
  $snyk = Resolve-SnykCmd
  if (-not $snyk -or $ActualizarLocales) {
    $npm = Require-Command 'npm' 'Node.js/npm son necesarios para Snyk.'
    & $npm install -g snyk@latest
    if ($LASTEXITCODE -ne 0) { throw 'Fallo instalando Snyk CLI.' }
  }
  $snyk = Resolve-SnykCmd
  if (-not $snyk) { throw 'Snyk CLI se instalo pero snyk.cmd no quedo disponible.' }
  $output = Join-Path $env:LOCALAPPDATA 'SnykMCP\output'
  New-Item -ItemType Directory -Force -Path $output | Out-Null
  Write-Ok "Snyk presente: $snyk"
  return [pscustomobject]@{Exe=$snyk;Output=$output}
}

function Ensure-Serena {
  $serena = Command-Path 'serena'
  $uv = Require-Command 'uv' 'uv es necesario para Serena.'
  if (-not $serena) {
    & $uv tool install -p 3.13 serena-agent
    if ($LASTEXITCODE -ne 0) { throw 'Fallo instalando Serena.' }
  } elseif ($ActualizarLocales) {
    & $uv tool upgrade serena-agent
    if ($LASTEXITCODE -ne 0) { throw 'Fallo actualizando Serena.' }
  }

  $serena = Command-Path 'serena'
  if (-not $serena) {
    $fallback = Join-Path $HOME '.local\bin\serena.exe'
    if (Test-Path -LiteralPath $fallback -PathType Leaf) { $serena = $fallback }
  }
  if (-not $serena) { throw 'Serena fue instalada pero no se encontro serena.exe.' }

  & $serena init
  if ($LASTEXITCODE -ne 0) { throw 'serena init fallo.' }
  Write-Ok "Serena presente: $serena"
  return $serena
}

function Optional-IDAPlugin {
  if (-not $InstalarIDAPlugin) { return }
  $uvx = Require-Command 'uvx' 'uvx es necesario para instalar el plugin oficial de IDA.'
  Write-WarnMsg 'La instalacion del plugin IDA puede ser interactiva y requiere IDA 9.4+.'
  & $uvx ida-hcli plugin install 'ida-mcp@https://github.com/HexRaysSA/ida-mcp'
  if ($LASTEXITCODE -ne 0) { throw 'Fallo instalando el plugin GUI de IDA MCP.' }
}

function New-McpConfig($cbmExe,$githubWrapper,$snykInfo,$serenaExe) {
  $uvx = Require-Command 'uvx' 'uvx es requerido por IDA MCP.'
  $snykCmd = $snykInfo.Exe
  return [ordered]@{
    'codebase-memory' = [ordered]@{
      type='local'; command=@($cbmExe); enabled=$true; timeout=30000
    }
    'ida' = [ordered]@{
      type='local'; command=@($uvx,'--exclude-newer=1s','ida-mcp','stdio','--agent=kilo-desktop'); enabled=$true; timeout=60000
    }
    'playwright' = [ordered]@{
      type='local'; command=@('cmd','/c','npx','-y','@playwright/mcp@latest'); enabled=$true; timeout=60000
    }
    'context7' = [ordered]@{
      type='remote'; url='https://mcp.context7.com/mcp'; oauth=$false; enabled=$true; timeout=60000
    }
    'imagegen' = [ordered]@{
      type='local'; command=@('cmd','/c','npx','-y','codex-imagegen-mcp@0.2','serve'); enabled=$true; timeout=300000
    }
    'github' = [ordered]@{
      type='local'; command=@('pwsh','-NoLogo','-NoProfile','-ExecutionPolicy','Bypass','-File',$githubWrapper); enabled=$true; timeout=120000
    }
    'cloudflare-api' = [ordered]@{
      type='remote'; url='https://mcp.cloudflare.com/mcp'; enabled=$true; timeout=120000
    }
    'chrome-devtools' = [ordered]@{
      type='local'; command=@('cmd','/c','npx','-y','chrome-devtools-mcp@latest'); enabled=$true; timeout=120000
    }
    'snyk' = [ordered]@{
      type='local'; command=@('cmd','/c',$snykCmd,'mcp','-t','stdio','--profile','full','-o',$snykInfo.Output); enabled=$true; timeout=600000
    }
    'postman' = [ordered]@{
      type='remote'; url='https://mcp.postman.com/minimal'; enabled=$true; timeout=120000
    }
    'microsoft-learn' = [ordered]@{
      type='remote'; url='https://learn.microsoft.com/api/mcp'; enabled=$true; timeout=120000
    }
    'sentry' = [ordered]@{
      type='remote'; url='https://mcp.sentry.dev/mcp'; enabled=$true; timeout=120000
    }
    'serena' = [ordered]@{
      type='local'; command=@($serenaExe,'start-mcp-server','--context','ide','--project-from-cwd','--open-web-dashboard','false'); enabled=$true; timeout=300000
    }
  }
}

function Merge-McpConfig($managed) {
  $configDir = Split-Path $KiloConfig -Parent
  New-Item -ItemType Directory -Force -Path $configDir | Out-Null

  if (Test-Path -LiteralPath $KiloConfig -PathType Leaf) {
    try {
      $data = Get-Content -LiteralPath $KiloConfig -Raw -Encoding UTF8 | ConvertFrom-Json -AsHashtable
    } catch {
      throw "kilo.jsonc no se puede convertir de forma segura con ConvertFrom-Json. El pack no lo reescribe: $($_.Exception.Message)"
    }
  } else {
    $data = [ordered]@{ '$schema'='https://kilo.ai/config.json'; mcp=[ordered]@{} }
  }

  if (-not $data.ContainsKey('mcp') -or $null -eq $data.mcp) { $data.mcp = [ordered]@{} }
  if ($data.mcp -isnot [System.Collections.IDictionary]) {
    throw 'La propiedad mcp existe pero no es un objeto JSON.'
  }

  foreach ($id in $managed.Keys) { $data.mcp[$id] = $managed[$id] }

  $backup = Backup-KiloConfig
  if ($backup) { Write-InfoMsg "Backup kilo.jsonc: $backup" }
  Write-WarnMsg 'Aplicar reserializa kilo.jsonc; el backup conserva comentarios/formato previos.'
  Write-JsonAtomic $KiloConfig $data
  Write-Ok "Configuracion MCP escrita: $KiloConfig"
}

function Diagnose {
  Write-Host '=== VX MCP PACK | DIAGNOSTICO ===' -ForegroundColor Cyan
  $checks = @(
    @{Name='pwsh'; Required=$true},
    @{Name='node'; Required=$true},
    @{Name='npm'; Required=$true},
    @{Name='npx'; Required=$true},
    @{Name='gh'; Required=$true},
    @{Name='uv'; Required=$true},
    @{Name='uvx'; Required=$true},
    @{Name='snyk'; Required=$false},
    @{Name='serena'; Required=$false}
  )
  foreach ($c in $checks) {
    $path = Command-Path $c.Name
    if ($path) { Write-Ok "$($c.Name): $path" }
    elseif ($c.Required) { Write-WarnMsg "$($c.Name): FALTA (requerido para pack completo)" }
    else { Write-InfoMsg "$($c.Name): no instalado; Aplicar puede instalarlo" }
  }

  $chromeCandidates = @(
    (Join-Path $env:ProgramFiles 'Google\Chrome\Application\chrome.exe'),
    (Join-Path ${env:ProgramFiles(x86)} 'Google\Chrome\Application\chrome.exe'),
    (Join-Path $env:LOCALAPPDATA 'Google\Chrome\Application\chrome.exe')
  ) | Where-Object { $_ -and (Test-Path -LiteralPath $_ -PathType Leaf) }
  if ($chromeCandidates) { Write-Ok "Chrome: $($chromeCandidates[0])" }
  else { Write-WarnMsg 'Chrome no detectado; Chrome DevTools necesitara Chrome.' }

  $cbm = Join-Path $env:LOCALAPPDATA 'Programs\codebase-memory-mcp\codebase-memory-mcp.exe'
  if (Test-Path -LiteralPath $cbm -PathType Leaf) { Write-Ok "Codebase Memory: $cbm" }
  else { Write-InfoMsg 'Codebase Memory no instalado en la ruta administrada.' }

  if (Test-Path -LiteralPath $KiloConfig -PathType Leaf) {
    try {
      $cfg = Get-Content -LiteralPath $KiloConfig -Raw -Encoding UTF8 | ConvertFrom-Json
      $names = @($cfg.mcp.PSObject.Properties.Name)
      Write-InfoMsg "MCP configurados en Kilo: $($names.Count)"
      foreach ($id in $managedIds) {
        if ($id -in $names) { Write-Ok "config:$id" } else { Write-WarnMsg "config:$id ausente" }
      }
    } catch {
      Write-WarnMsg "No se pudo leer kilo.jsonc con ConvertFrom-Json: $($_.Exception.Message)"
    }
  } else {
    Write-InfoMsg 'kilo.jsonc todavia no existe.'
  }
}

function Verify {
  Write-Host '=== VX MCP PACK | VERIFICAR ===' -ForegroundColor Cyan
  if (!(Test-Path -LiteralPath $registryPath -PathType Leaf)) { throw "Falta registro: $registryPath" }
  $reg = Read-Json $registryPath
  if (@($reg.servers).Count -ne 13) { throw 'El registro V2 debe contener exactamente 13 servidores.' }
  $ids = @($reg.servers | ForEach-Object id)
  if (@($ids | Sort-Object -Unique).Count -ne 13) { throw 'IDs MCP duplicados en registro V2.' }
  Write-Ok 'Registro V2: 13 IDs unicos.'

  if (!(Test-Path -LiteralPath $KiloConfig -PathType Leaf)) { throw "Falta $KiloConfig" }
  $cfg = Get-Content -LiteralPath $KiloConfig -Raw -Encoding UTF8 | ConvertFrom-Json
  $names = @($cfg.mcp.PSObject.Properties.Name)
  $missing = @($managedIds | Where-Object { $_ -notin $names })
  if ($missing.Count) { throw "Faltan MCP gestionados en Kilo: $($missing -join ', ')" }
  Write-Ok 'kilo.jsonc contiene los 13 MCP del pack.'

  $kilo = Get-KiloExe
  if ($kilo) {
    Write-InfoMsg "Kilo CLI: $kilo"
    & $kilo mcp list
  } else {
    Write-WarnMsg 'Kilo CLI no encontrado/ejecutandose; no se puede verificar handshake. Abre Kilo y repite -Modo Verificar.'
  }
}

if (!(Test-Path -LiteralPath $registryPath -PathType Leaf)) {
  throw "Falta registro canonico: $registryPath"
}

switch ($Modo) {
  'Diagnostico' {
    Diagnose
    exit 0
  }
  'Verificar' {
    Verify
    exit 0
  }
  'Aplicar' {
    Write-Host '=== VX MCP PACK | APLICAR ===' -ForegroundColor Cyan
    Require-Command 'pwsh' 'PowerShell 7 es obligatorio.' | Out-Null
    Require-Command 'node' 'Node.js es obligatorio.' | Out-Null
    Require-Command 'npm' 'npm es obligatorio.' | Out-Null
    Require-Command 'npx' 'npx es obligatorio.' | Out-Null
    Require-Command 'gh' 'GitHub CLI es obligatorio.' | Out-Null
    Require-Command 'uv' 'uv es obligatorio.' | Out-Null
    Require-Command 'uvx' 'uvx es obligatorio.' | Out-Null

    if ($SoloConfig) {
      $cbmExe = Join-Path $env:LOCALAPPDATA 'Programs\codebase-memory-mcp\codebase-memory-mcp.exe'
      $githubWrapper = Join-Path $env:LOCALAPPDATA 'Programs\github-mcp-server\github-mcp-kilo.ps1'
      $snykExe = Resolve-SnykCmd
      $serenaExe = Command-Path 'serena'
      if (-not $serenaExe) {
        $fallback = Join-Path $HOME '.local\bin\serena.exe'
        if (Test-Path -LiteralPath $fallback -PathType Leaf) { $serenaExe = $fallback }
      }
      if (!(Test-Path -LiteralPath $cbmExe -PathType Leaf)) { throw 'SoloConfig requiere Codebase Memory ya instalado.' }
      if (!(Test-Path -LiteralPath $githubWrapper -PathType Leaf)) { throw 'SoloConfig requiere wrapper GitHub ya instalado.' }
      if (-not $snykExe) { throw 'SoloConfig requiere Snyk ya instalado.' }
      if (-not $serenaExe) { throw 'SoloConfig requiere Serena ya instalada.' }
      $snykInfo = [pscustomobject]@{Exe=$snykExe;Output=(Join-Path $env:LOCALAPPDATA 'SnykMCP\output')}
      New-Item -ItemType Directory -Force -Path $snykInfo.Output | Out-Null
    } else {
      $cbmExe = Ensure-CodebaseMemory
      $githubWrapper = Ensure-GitHubMcp
      $snykInfo = Ensure-Snyk
      $serenaExe = Ensure-Serena
      Optional-IDAPlugin
    }

    $managed = New-McpConfig $cbmExe $githubWrapper $snykInfo $serenaExe
    Merge-McpConfig $managed

    Write-Host ''
    Write-WarnMsg 'Autenticaciones deliberadamente manuales:'
    Write-Host '  gh auth status'
    Write-Host '  npx -y codex-imagegen-mcp@0.2 login'
    Write-Host '  npx -y codex-imagegen-mcp@0.2 doctor'
    Write-Host '  snyk auth'
    Write-Host '  kilo mcp auth cloudflare-api'
    Write-Host '  kilo mcp auth postman'
    Write-Host '  kilo mcp auth sentry'
    Write-WarnMsg 'IDA GUI requiere el plugin oficial; usa -InstalarIDAPlugin solo con IDA 9.4+ disponible.'
    Write-InfoMsg 'Reinicia Kilo y ejecuta este script con -Modo Verificar.'
    exit 0
  }
}
