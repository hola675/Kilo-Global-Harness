#Requires -Version 7.0
<#
.SYNOPSIS
  V4.2: compara METADATOS seguros de agentes Kilo globales JSONC/Markdown.
.DESCRIPTION
  SOLO LECTURA. No imprime prompts, descripciones, modelos, secretos, permisos
  con patrones privados, ni rutas absolutas. No reescribe configuracion.
  El resultado es un inventario y una propuesta, NO una migracion automatica.
.EXAMPLE
  pwsh -NoProfile -File .\scripts\Reconciliar-Agentes-V4.2.ps1
  pwsh -NoProfile -File .\scripts\Reconciliar-Agentes-V4.2.ps1 -Json
#>
[CmdletBinding()]
param(
  [string]$RaizUsuario = $HOME,
  [ValidateRange(1,10000000)][int]$UmbralSteps = 400,
  [switch]$Json
)
$ErrorActionPreference = 'Stop'
if (![IO.Path]::IsPathFullyQualified($RaizUsuario)) {
  throw 'RaizUsuario debe ser ruta absoluta.'
}
$homeRoot = [IO.Path]::GetFullPath($RaizUsuario)
$kiloPath = Join-Path $homeRoot '.config/kilo'
$jsonPath = Join-Path $kiloPath 'kilo.jsonc'
$agentsPath = Join-Path $kiloPath 'agents'
$safeFields = @('mode','steps','model','temperature','top_p','description','prompt','hidden','disable','permission','tools','color')
$permissionFields = @('read','glob','grep','edit','bash','task','mcp','skill','lsp','agent_manager','external_directory')
$validPermissionValues = @('allow','ask','deny')

function Get-SafeScalar([string]$Source,[string]$Value) {
  $v = $Value.Trim().Trim('"').Trim("'")
  if ($Source -eq 'steps') {
    $number = 0L
    if ([long]::TryParse($v,[ref]$number) -and $number -ge 0 -and $number -le [long]::MaxValue) {
      return [string]$number
    }
    return 'OTRO_VALOR'
  }
  if ($Source -eq 'mode') {
    if ($v -in @('all','primary','subagent')) { return $v }
    return 'OTRO_VALOR'
  }
  if ($Source -eq 'permission') {
    if ($v -in $validPermissionValues) { return $v }
    return 'REGLAS_COMPUESTAS'
  }
  return 'DECLARADO'
}
function Get-MarkdownMetadata([string]$Path) {
  $raw = [IO.File]::ReadAllText($Path)
  $match = [regex]::Match($raw,'\A(?:\uFEFF)?---\r?\n(?<body>[\s\S]*?)\r?\n---(?:\r?\n|$)')
  if (!$match.Success) {
    return [pscustomobject]@{valid=$false; fields=@{}; permissions=@{}}
  }
  $front = $match.Groups['body'].Value
  $fields = @{}
  foreach ($m in [regex]::Matches($front,'(?m)^(?<key>[a-zA-Z][a-zA-Z0-9_-]*):[ \t]*(?<value>[^\r\n]*)\r?$')) {
    $name = $m.Groups['key'].Value
    if ($name -in $safeFields) {
      $fields[$name] = Get-SafeScalar $name $m.Groups['value'].Value
    }
  }
  $permissions = @{}
  $block = [regex]::Match($front,'(?ms)^permission:[ \t]*\r?\n(?<block>(?:[ \t]+[^\r\n]*(?:\r?\n|$))*)')
  if ($block.Success) {
    foreach ($m in [regex]::Matches($block.Groups['block'].Value,'(?m)^ {2}(?<key>[a-zA-Z][a-zA-Z0-9_-]*):[ \t]*(?<value>[^\r\n]*)\r?$')) {
      $name = $m.Groups['key'].Value
      if ($name -in $permissionFields) {
        $permissions[$name] = Get-SafeScalar 'permission' $m.Groups['value'].Value
      }
    }
  }
  return [pscustomobject]@{valid=$true;fields=$fields;permissions=$permissions}
}
function Get-JsonMetadata([System.Text.Json.JsonElement]$Node) {
  $fields = @{}
  $permissions = @{}
  if ($Node.ValueKind -ne 'Object') {
    return [pscustomobject]@{fields=$fields;permissions=$permissions;valid=$false}
  }
  foreach ($name in $safeFields) {
    $value = [System.Text.Json.JsonElement]::new()
    if (!$Node.TryGetProperty($name,[ref]$value)) { continue }
    if ($name -in @('steps','mode')) {
      if ($value.ValueKind -in @('String','Number')) {
        $v = if ($value.ValueKind -eq 'String') { $value.GetString() } else { $value.GetRawText() }
        $fields[$name] = Get-SafeScalar $name $v
      } else { $fields[$name] = 'OTRO_VALOR' }
    } else {
      $fields[$name] = 'DECLARADO'
    }
    if ($name -eq 'permission' -and $value.ValueKind -eq 'Object') {
      foreach ($permission in $permissionFields) {
        $p = [System.Text.Json.JsonElement]::new()
        if ($value.TryGetProperty($permission,[ref]$p)) {
          $permissions[$permission] = if ($p.ValueKind -eq 'String') {
            Get-SafeScalar 'permission' $p.GetString()
          } else { 'REGLAS_COMPUESTAS' }
        }
      }
    }
  }
  return [pscustomobject]@{fields=$fields;permissions=$permissions;valid=$true}
}
$jsonNodes = @{}
$metadata = @{}
$markdown = @{}
$warnings = [System.Collections.Generic.List[string]]::new()

if (Test-Path -LiteralPath $jsonPath -PathType Leaf) {
  $opts = [System.Text.Json.JsonDocumentOptions]::new()
  $opts.CommentHandling = [System.Text.Json.JsonCommentHandling]::Skip
  $opts.AllowTrailingCommas = $true
  $doc = [System.Text.Json.JsonDocument]::Parse([IO.File]::ReadAllText($jsonPath),$opts)
  try {
    $agents = [System.Text.Json.JsonElement]::new()
    if ($doc.RootElement.ValueKind -eq 'Object' -and
        $doc.RootElement.TryGetProperty('agent',[ref]$agents) -and
        $agents.ValueKind -eq 'Object') {
      foreach ($node in $agents.EnumerateObject()) {
        $jsonNodes[$node.Name] = Get-JsonMetadata $node.Value
      }
    }
  } finally { $doc.Dispose() }
} else {
  $warnings.Add('No existe kilo.jsonc en la ruta global consultada.')
}
if (Test-Path -LiteralPath $agentsPath -PathType Container) {
  foreach ($file in @(Get-ChildItem -LiteralPath $agentsPath -File -Filter '*.md')) {
    $markdown[$file.BaseName] = Get-MarkdownMetadata $file.FullName
    if (!$markdown[$file.BaseName].valid) {
      $warnings.Add("Frontmatter de agente no interpretable: $($file.BaseName)")
    }
  }
}

$duplicates = @()
$stepWarnings = @()
# También se notifican limites Markdown (no solo los del JSONC). No se cambian.
foreach ($id in @($jsonNodes.Keys | Sort-Object)) {
  $jsonMeta = $jsonNodes[$id]
  if ($jsonMeta.fields.ContainsKey('steps')) {
    $n = 0L
    if ([long]::TryParse([string]$jsonMeta.fields.steps,[ref]$n) -and $n -gt $UmbralSteps) {
      $stepWarnings += [ordered]@{agente=$id;steps=$n;fuente='jsonc';decision='REVISAR_NO_MODIFICAR'}
    }
  }
  if (!$markdown.ContainsKey($id)) { continue }
  $md = $markdown[$id]
  $overlaps = @()
  $onlyJson = @()
  $onlyMarkdown = @()
  foreach ($field in $safeFields) {
    $inJson = $jsonMeta.fields.ContainsKey($field)
    $inMd = $md.fields.ContainsKey($field)
    if ($inJson -and $inMd) {
      $j = [string]$jsonMeta.fields[$field]; $m = [string]$md.fields[$field]
      $state = if ($field -in @('mode','steps')) {
        if ($j -eq $m) {'IGUAL_EXPLICITO'} else {'DIFERENCIA_EXPLICITA'}
      } else { 'SOLAPAMIENTO_REQUIERE_REVISION' }
      $overlaps += [ordered]@{campo=$field;estado=$state;json_valor=$(if($field -in @('mode','steps')){$j}else{'OCULTO'});markdown_valor=$(if($field -in @('mode','steps')){$m}else{'OCULTO'})}
    } elseif ($inJson) { $onlyJson += $field }
    elseif ($inMd) { $onlyMarkdown += $field }
  }
  foreach ($key in $permissionFields) {
    if (!$jsonMeta.permissions.ContainsKey($key) -or !$md.permissions.ContainsKey($key)) { continue }
    $j = [string]$jsonMeta.permissions[$key]
    $m = [string]$md.permissions[$key]
    $state = if ($j -eq $m -and $j -in $validPermissionValues) {
      'IGUAL_EXPLICITO'
    } elseif ($j -in $validPermissionValues -and $m -in $validPermissionValues) {
      'DIFERENCIA_EXPLICITA'
    } else { 'REGLAS_COMPUESTAS_REVISAR_PRECEDENCIA' }
    $overlaps += [ordered]@{campo="permission.$key";estado=$state;json_valor=$j;markdown_valor=$m}
  }
  $duplicates += [ordered]@{
    agente=$id
    markdown_frontmatter_valido=[bool]$md.valid
    campos_solapados=$overlaps
    campos_solo_json=$onlyJson
    campos_solo_markdown=$onlyMarkdown
    requiere_revision=[bool](@($overlaps | Where-Object { $_.estado -ne 'IGUAL_EXPLICITO' }).Count -gt 0 -or !$md.valid)
  }
}

# Incluir limites elevados declarados solo o adicionalmente en Markdown.
foreach ($id in @($markdown.Keys | Sort-Object)) {
  $mdMeta = $markdown[$id]
  if (!$mdMeta.fields.ContainsKey('steps')) { continue }
  $n = 0L
  if ([long]::TryParse([string]$mdMeta.fields.steps,[ref]$n) -and $n -gt $UmbralSteps) {
    $stepWarnings += [ordered]@{agente=$id;steps=$n;fuente='markdown';decision='REVISAR_NO_MODIFICAR'}
  }
}

$report=[ordered]@{
  schema='vx-kilo-reconciliation/1'
  version='4.2.0'
  alcance='GLOBAL_SOLO_LECTURA'
  agentes_json=$jsonNodes.Count
  agentes_markdown=$markdown.Count
  agentes_en_ambos=$duplicates.Count
  limites_steps_superiores_al_umbral=@($stepWarnings).Count
  umbral_steps=$UmbralSteps
  coincidencias=@($duplicates)
  limites_excesivos=@($stepWarnings)
  advertencias=@($warnings)
  restricciones=@(
    'No cambia kilo.jsonc, AGENTS.md, permisos, modelos ni MCP.'
    'No revela contenido de prompts, descripciones, modelos ni credenciales.'
    'El parser de YAML solo interpreta escalares simples y permisos basicos: no calcula la configuracion efectiva.'
    'La precedencia de Kilo requiere comprobacion en el runtime antes de eliminar definiciones.'
    'Ningun conflicto implica por si mismo un fallo del agente.'
  )
  plan=@(
    'P0: comparar manualmente permisos efectivos y campos en conflicto por agente con respaldo.'
    'P0: probar limites steps acotados en casos reales; no editar el JSON privado automaticamente.'
    'P1: migrar un agente piloto en una ventana controlada, revalidar comportamiento y rollback.'
    'P1: verificar solapamiento de skills por capacidad, no solo por nombre.'
  )
}
if ($Json) {
  ConvertTo-Json -InputObject $report -Depth 24
} else {
  Write-Host '=== VX V4.2 | RECONCILIACION GLOBAL | SOLO LECTURA ===' -ForegroundColor Cyan
  Write-Host "JSON=$($jsonNodes.Count) Markdown=$($markdown.Count) Compartidos=$($duplicates.Count)"
  Write-Host "Steps > $UmbralSteps (JSON + Markdown): $(@($stepWarnings).Count)"
  foreach ($d in $duplicates) {
    $flags=@($d.campos_solapados | Where-Object { $_.estado -ne 'IGUAL_EXPLICITO' } | ForEach-Object campo)
    Write-Host "[$(if($d.requiere_revision){'REVISAR'}else{'SIN CONFLICTO EXPLICITO'})] $($d.agente) | solapamientos: $(@($flags) -join ', ')"
  }
  Write-Host 'No se han mostrado secretos ni cambiado archivos.' -ForegroundColor Green
  Write-Host 'Para un reporte estructurado: agrega -Json (evita compartirlo publicamente sin revisarlo).'
}
