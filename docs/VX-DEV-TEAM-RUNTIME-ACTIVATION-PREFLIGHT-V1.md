# Runtime Activation Preflight V1

Esta es la última fase **antes** de modificar el runtime.

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
