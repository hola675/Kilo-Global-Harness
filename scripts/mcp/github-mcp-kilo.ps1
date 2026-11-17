$ErrorActionPreference = 'Stop'

$gh = (Get-Command gh -ErrorAction Stop).Source
$exe = Join-Path $env:LOCALAPPDATA 'Programs\github-mcp-server\current\github-mcp-server.exe'

if (!(Test-Path -LiteralPath $exe -PathType Leaf)) {
  Write-Error "No se encontro GitHub MCP: $exe"
  exit 1
}

$token = (& $gh auth token 2>$null)
if ($null -eq $token) {
  Write-Error 'GitHub CLI no devolvio un token.'
  exit 1
}
$token = ([string]$token).Trim()
if ([string]::IsNullOrWhiteSpace($token)) {
  Write-Error 'GitHub CLI no devolvio un token util.'
  exit 1
}

$env:GITHUB_PERSONAL_ACCESS_TOKEN = $token
$env:GITHUB_TOOLSETS = 'context,repos,issues,pull_requests,actions'

try {
  & $exe stdio
  $code = $LASTEXITCODE
}
finally {
  Remove-Item Env:GITHUB_PERSONAL_ACCESS_TOKEN -ErrorAction SilentlyContinue
  Remove-Item Env:GITHUB_TOOLSETS -ErrorAction SilentlyContinue
}

exit $code
