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
  if ($agent.writes -eq $false) {
    if ($front -notmatch '(?m)^\s{2}edit:\s*deny\s*$') { throw "Agente read-only sin edit deny: $id." }
    if ($front -match '(?m)^\s{2}bash:\s*allow\s*$') { throw "Agente read-only con bash allow: $id." }
    if ($front -match '(?m)^\s{2}task:\s*allow\s*$') { throw "Agente read-only puede delegar: $id." }
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
}
if (!$profilesSeen.Contains('general')) { throw 'Falta perfil general.' }
Write-Host "[PASS] Registro V4: $($agents.Count) agentes, $($profiles.Count) perfiles, solo global y un escritor maximo." -ForegroundColor Green
