#Requires -Version 7.0
<#
.SYNOPSIS
  Propone un equipo Kilo segun perfil/tarea. SOLO LECTURA. No inicia agentes ni consume cuota.
.EXAMPLE
  pwsh -NoProfile -File .\scripts\Seleccionar-Equipo-V4.ps1 -Perfil cloudflare -Json
  pwsh -NoProfile -File .\scripts\Seleccionar-Equipo-V4.ps1 -Tarea "Corregir UI React" -Json
#>
[CmdletBinding()]
param(
  [ValidateSet('auto','general','backend','frontend','cloudflare','database','security','refactor','design','docs')]
  [string]$Perfil = 'auto',
  [string]$Tarea = '',
  [ValidateRange(1,3)][int]$MaxLectores = 3,
  [switch]$SoloLectura,
  [switch]$Json,
  [string]$RaizUsuario = $HOME
)
$ErrorActionPreference='Stop'
$globalPath = Join-Path $RaizUsuario '.config/kilo/harness/vx-agent-registry-v4.json'
$repoPath = Join-Path (Split-Path $PSScriptRoot -Parent) 'registry/vx-agent-registry-v4.json'
$path = if (Test-Path -LiteralPath $globalPath -PathType Leaf) { $globalPath } else { $repoPath }
if (!(Test-Path -LiteralPath $path)) { throw 'No se encontro registro V4 global ni de fuente.' }
$data = Get-Content -LiteralPath $path -Raw -Encoding UTF8 | ConvertFrom-Json -AsHashtable
if ($data.schema -ne 'vx-agent-registry/1' -or $data.global_only -ne $true) { throw 'Registro V4 no reconocido.' }
$profileMap = @{}
foreach ($p in $data.profiles) { $profileMap[[string]$p.id] = $p }
if ($Perfil -eq 'auto') {
  $priority = @('cloudflare','security','database','frontend','backend','refactor','design','docs')
  $scores = @()
  foreach ($key in $priority) {
    $score = 0
    foreach ($word in @($profileMap[$key].patterns)) {
      $pat = '(?i)(?<![\p{L}\p{N}])' + [regex]::Escape([string]$word) + '(?![\p{L}\p{N}])'
      if ($Tarea -match $pat) { $score++ }
    }
    if ($score -gt 0) {
      $scores += [pscustomobject]@{profile=$key;score=$score;rank=[array]::IndexOf($priority,$key)}
    }
  }
  $detected = @($scores | Sort-Object @{Expression='score';Descending=$true},@{Expression='rank';Descending=$false}) | Select-Object -First 1
  $Perfil = if ($null -ne $detected) { [string]$detected.profile } else { 'general' }
}
$p = $profileMap[$Perfil]
if (!$p) { throw "Perfil no disponible: $Perfil" }
$known = @($data.agents | ForEach-Object { $_.id })
$discovery = @($p.discover | Where-Object { $_ -in $known } | Select-Object -First $MaxLectores)
$review = @($p.review | Where-Object { $_ -in $known } | Select-Object -First $MaxLectores)
$writer = if ($SoloLectura) { $null } else { $p.writer }
$plan = [ordered]@{
  schema = 'vx-team-plan/1'
  profile = $Perfil
  mode = 'strict'
  strategy = 'Kilo task(background=true) para lectores independientes; un writer despues del analisis'
  coordinator = 'vx-integrador'
  discover_parallel = $discovery
  implementation = $writer
  review_parallel = $review
  max_parallel_readers = $MaxLectores
  max_writers = $(if ($SoloLectura) {0}else{1})
  skill_suggestions = @($p.skills)
  actions_executed = 0
  git_policy = 'main permanente; solo work/<tarea> temporal; merge tras pruebas; borrar solo rama propia'
  requires_user_confirmation = 'produccion, infraestructura, datos destructivos, ampliacion a worktrees paralelos'
  limitations = 'Este script SOLO PLANIFICA. La delegacion real ocurre en Kilo y su runtime.'
}
if ($Json) {
  ConvertTo-Json -InputObject $plan -Depth 8
} else {
  Write-Host '=== VX TEAM ROUTER V4 | SOLO LECTURA ===' -ForegroundColor Cyan
  Write-Host "Perfil: $Perfil | Modo: strict | Lectores max: $MaxLectores"
  Write-Host "Descubrimiento en paralelo: $($discovery -join ', ')"
  Write-Host "Implementacion unica: $(if($writer){$writer}else{'ninguna: solo lectura'})"
  Write-Host "Revision en paralelo (despues del diff): $($review -join ', ')"
  Write-Host "Skills sugeridas, por demanda: $(@($p.skills) -join ', ')"
  Write-Host 'Sin tareas lanzadas, sin modificaciones, sin consumo de modelos.' -ForegroundColor Green
}
