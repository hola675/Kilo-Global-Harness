# Tool Plan Generator V1

Este generador convierte un snapshot **visible** de Kilo en un plan de revisión por agente.

No modifica configuración.

## Entrada

```text
dev-team-runtime-visible-tools.json
```

## Salida

Por agente:

- `keep_visible`
- `missing_primary_native`
- `missing_primary_mcp_families`
- `review_unexpected`
- `decision = NO_AUTO_APPLY`

## Uso

```powershell
pwsh -NoProfile -File .\scripts\Generar-DevTeam-ToolPlan.ps1 `
  -Snapshot .\artifacts\dev-team-runtime-visible-tools.json `
  -Salida .\artifacts\dev-team-tool-plan.json
```

La salida sirve para revisión y futura propuesta ACL. Nunca debe aplicarse automáticamente.
