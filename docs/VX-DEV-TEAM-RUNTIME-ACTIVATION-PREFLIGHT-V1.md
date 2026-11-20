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
