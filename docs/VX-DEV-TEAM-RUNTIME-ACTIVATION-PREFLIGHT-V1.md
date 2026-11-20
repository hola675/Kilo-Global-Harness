# Runtime Activation Preflight V1

Esta es la última fase **antes** de modificar el runtime.

**V1.1 — diagnóstico de integridad de W1:** se comparan SHA-256 de las 11 fuentes de agentes y las 18 skills core contra sus archivos instalados. Utiliza exactamente las rutas del instalador actual (`~/.config/kilo/agents` y `~/.kilo/skills`). No se instalan ni se reparan archivos durante esta operación.

El preflight:

- verifica evidencia disponible;
- enumera blockers por wave;
- genera `READY_FOR_OPERATOR_REVIEW` solo cuando el único blocker restante sea la aprobación;
- nunca cambia agentes, skills, MCP ni `kilo.jsonc`;
- nunca establece `operator_approval=true`.

Ejemplo:

```powershell
pwsh -NoProfile -File .\scripts\Generar-DevTeam-ActivationPreflight.ps1 `
  -SourceCiStatus PASS `
  -RuntimeSnapshot .\artifacts\dev-team-runtime-visible-tools.json `
  -SkillEvalReport .\artifacts\dev-team-skill-eval-report.json `
  -Salida .\artifacts\dev-team-activation-preflight.json
```

La aplicación runtime seguirá siendo un paso separado, explícito y reversible.

## Preflight en el Windows del operador

```powershell
pwsh -NoProfile -File .\scripts\Generar-DevTeam-ActivationPreflight.ps1 `
  -SourceCiStatus PASS `
  -Salida .\artifacts\dev-team-activation-preflight.json
```

Los checks `runtime_agent_hash_match` y `skill_source_hash_18_of_18` solo son PASS con **11/11 y 18/18** archivos idénticos, respectivamente. El campo `hash_evidence` informa nombres de archivos ausentes, diferentes o no legibles, sin exportar sus contenidos. `-RaizUsuario <ruta-absoluta>` sirve para ensayos aislados; si se omite, se inspecciona `$HOME`.

Este control **no** prueba capacidades efectivas del host, ACL, visibilidad, comportamiento de herramientas MCP ni resultado de los smoke tests runtime. Un archivo instalado idéntico al source no acredita una ejecución funcional. Las waves W2–W5 permanecen bloqueadas por sus verificaciones y aprobaciones propias.

`-SourceCiStatus PASS` es una **declaración del operador**; debe apoyarse en un run real del HEAD vigente, no deducirse de las comparaciones de hashes. No permitir `operator_approval=true` en este generador. Ningún resultado `READY_FOR_OPERATOR_REVIEW` autoriza instalación ni activación.

## Diagnóstico de deriva local V1.2 (solo lectura)

En `hash_evidence.agents.drift_details` y `hash_evidence.skills.drift_details` se emite, para cada par con SHA distinto, únicamente identificador, clasificación y tamaños en bytes. **No** se incluyen contenidos, rutas absolutas, tokens ni diffs textuales.

Clasificaciones: `UTF8_BOM_ONLY`, `EOL_OR_BOM_ONLY`, `TRAILING_WHITESPACE_ONLY`, `CONTENT_CHANGED`, `NOT_VALID_UTF8_OR_UNREADABLE`, `UNKNOWN_BYTE_DIFFERENCE`.

Incluso una diferencia de formato mantiene el check SHA-256 **FAIL**. `CONTENT_CHANGED` indica contenido distinto tras normalizar únicamente BOM, finales de línea y espacios finales; **no** presume que los permisos sean maliciosos ni recomienda reemplazar archivos. Se debe revisar el contenido localmente mediante comparación visual antes de cualquier despliegue.

Ejemplo de inspección sin escribir en la instalación:

```powershell
$r=Get-Content .\artifacts\dev-team-activation-preflight.json -Raw | ConvertFrom-Json
$r.hash_evidence.agents.drift_details | Format-Table -AutoSize
$r.hash_evidence.skills.drift_details | Format-Table -AutoSize
```

El operador puede investigar una diferencia real de forma local con `code --diff <fuente> <instalado>`; esta comparación no modifica archivos. No ejecutar `Instalar-DevTeam-Only.ps1 -Modo Aplicar` como mecanismo automático de reparación de hashes.

## V1.3 — Anexo editorial del Pack VX 0.4.0 (solo diagnóstico)

El preflight añade `vx_editorial_extension` para consultar dos archivos instalados: `vx-editorial-builder.md` bajo `~/.config/kilo/agents/` y `vx-editorial-claridad/SKILL.md` bajo `~/.kilo/skills/`. Aplica los mismos SHA-256 y clasificaciones de deriva sin exportar rutas absolutas ni contenidos.

| Estado | Interpretación |
| --- | --- |
| `SOURCE_FILES_MATCH_ONLY` | Ambos archivos idénticos a source. **No certifica delegación ni ejecución**. |
| `NOT_INSTALLED_OR_INCOMPLETE` | Uno o ambos archivos no se encuentran en source o en la instalación. |
| `HASH_DRIFT_REQUIRES_REVIEW` | Existen archivos no idénticos, ilegibles o con diferencias de contenido o formato. |

Esta comprobación es **independiente de W1 CORE**: no cambia los 11 roles ni las 18 skills Dev Team, no altera los gates de la wave y jamás autoriza instalar el Pack VX. Los campos `task_permission_runtime_verified=false` y `runtime_functionality_verified=false` permanecen falsos aunque los dos hashes coincidan. El líder `vx-dev-team` todavía requiere una prueba real de permiso de `task` en Kilo, con consentimiento del host y revisión independiente.

Consulta sin modificar HOME:

```powershell
$r = & pwsh -NoProfile -File .\scripts\Generar-DevTeam-ActivationPreflight.ps1 -SourceCiStatus UNKNOWN | ConvertFrom-Json
$r.vx_editorial_extension | Format-List status,scope,task_permission_runtime_verified,runtime_functionality_verified
$r.vx_editorial_extension.agent.drift_details | Format-Table -AutoSize
$r.vx_editorial_extension.skill.drift_details | Format-Table -AutoSize
```

**TEST_ACTION=UPDATE:** la suite viva `tests/test_vx_dev_team_activation_preflight_v1.py` cubre ausencias, igualdad y modificación de contenido editorial. Sin suite paralela histórica. `SourceCiStatus` sigue siendo una declaración externa, no una verificación remota de GitHub realizada por este script.
