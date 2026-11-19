param(
  [ValidateSet('Source','Runtime')]
  [string]$Origen = 'Runtime',
  [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
  [string]$HomeRoot = $HOME,
  [string]$Salida
)

$ErrorActionPreference = 'Stop'

$leaderSource = Join-Path $RepoRoot 'agents\vx-dev-team.md'
$childrenSource = Join-Path $RepoRoot 'runtime\dev-team-v2r\agents'
$runtimeDir = Join-Path $HomeRoot '.config\kilo\agents'

function Get-AgentFiles {
  if ($Origen -eq 'Source') {
    @($leaderSource) + @(Get-ChildItem -LiteralPath $childrenSource -Filter 'vx-dev-*.md' | Select-Object -ExpandProperty FullName)
  } else {
    if (!(Test-Path -LiteralPath $runtimeDir)) { throw "No existe runtime agents dir: $runtimeDir" }
    @(Get-ChildItem -LiteralPath $runtimeDir -Filter 'vx-dev-*.md' | Select-Object -ExpandProperty FullName)
  }
}

function Get-Frontmatter([string]$Path) {
  $text = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
  $m = [regex]::Match($text, '(?s)\A---\r?\n(?<front>.*?)\r?\n---\r?\n')
  if (!$m.Success) { throw "Frontmatter invalido: $Path" }
  $m.Groups['front'].Value
}

function Get-PermissionBlock([string]$Front) {
  $m = [regex]::Match($Front, '(?ms)^permission:\s*\r?\n(?<body>.*?)(?=^[A-Za-z_][A-Za-z0-9_-]*:\s*|\z)')
  if (!$m.Success) { return '' }
  $m.Groups['body'].Value
}

function Parse-Permissions([string]$Block) {
  $rows = New-Object System.Collections.Generic.List[object]
  foreach ($line in ($Block -split "\r?\n")) {
    if ($line -match '^\s{2}([A-Za-z0-9_-]+):\s*(allow|ask|deny)\s*$') {
      $rows.Add([pscustomobject]@{ Kind='native'; Name=$matches[1]; Decision=$matches[2] })
    }
    elseif ($line -match '^\s{2}"([^"]+)":\s*(allow|ask|deny)\s*$') {
      $name=$matches[1]
      $kind = if ($name -match '_') { 'namespaced' } else { 'other' }
      $rows.Add([pscustomobject]@{ Kind=$kind; Name=$name; Decision=$matches[2] })
    }
  }
  $rows
}

$result = foreach ($file in Get-AgentFiles) {
  $front = Get-Frontmatter $file
  $id = [IO.Path]::GetFileNameWithoutExtension($file)
  $perm = Parse-Permissions (Get-PermissionBlock $front)

  [pscustomobject]@{
    Agent = $id
    SourcePath = $file
    NativeAllow = @($perm | Where-Object { $_.Kind -eq 'native' -and $_.Decision -eq 'allow' } | Select-Object -ExpandProperty Name)
    NativeAsk = @($perm | Where-Object { $_.Kind -eq 'native' -and $_.Decision -eq 'ask' } | Select-Object -ExpandProperty Name)
    NativeDeny = @($perm | Where-Object { $_.Kind -eq 'native' -and $_.Decision -eq 'deny' } | Select-Object -ExpandProperty Name)
    NamespacedAllow = @($perm | Where-Object { $_.Kind -eq 'namespaced' -and $_.Decision -eq 'allow' } | Select-Object -ExpandProperty Name)
    NamespacedAsk = @($perm | Where-Object { $_.Kind -eq 'namespaced' -and $_.Decision -eq 'ask' } | Select-Object -ExpandProperty Name)
  }
}

$doc = [ordered]@{
  schema = 'dev-team-tool-inventory/1'
  captured_at = (Get-Date).ToString('o')
  origin = $Origen
  note = 'Inventario declarativo. No acredita conexion MCP ni visibilidad efectiva de tools en una sesion Kilo.'
  agents = @($result)
}

$json = $doc | ConvertTo-Json -Depth 8
if ($Salida) {
  $parent = Split-Path -Parent $Salida
  if ($parent -and !(Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
  Set-Content -LiteralPath $Salida -Value $json -Encoding UTF8
  Write-Host "Inventario guardado: $Salida" -ForegroundColor Green
}
$json
