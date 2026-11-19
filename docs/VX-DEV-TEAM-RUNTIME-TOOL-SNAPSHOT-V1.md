# Runtime Tool Snapshot Protocol V1

**Estado:** source-only. No invoca tools automáticamente.

## Objetivo

Separar tres conceptos:

1. **declarado** en los archivos de agente;
2. **visible** en una sesión Kilo;
3. **probado** mediante smoke.

Nunca tratar uno como equivalente a los otros.

## Captura declarativa

```powershell
pwsh -NoProfile -File .\scripts\Inventariar-DevTeam-Tools.ps1 `
  -Origen Runtime `
  -Salida .\artifacts\dev-team-tools-declared.json
```

Esto solo lee los agentes instalados. No prueba conexión MCP.

## Snapshot efectivo

Para cada agente, iniciar una sesión aislada y pedir **inventario sin invocación** de las tools que Kilo le muestra. Guardar un JSON con:

```json
{
  "schema": "dev-team-runtime-visible-tools/1",
  "agents": [
    {
      "Agent": "vx-dev-research",
      "visible_tools": [
        "glob",
        "grep",
        "lsp",
        "skill",
        "context7_resolve-library-id"
      ]
    }
  ]
}
```

No ejecutar las tools durante esta fase.

## Comparación

```powershell
pwsh -NoProfile -File .\scripts\Comparar-DevTeam-ToolSnapshot.ps1 `
  -Snapshot .\artifacts\dev-team-runtime-visible-tools.json `
  -Salida .\artifacts\dev-team-tool-diff.json
```

## Gates

- 11/11 agentes presentes.
- Ninguna tool mutable inesperada.
- Ningún wildcard MCP.
- Tools documentales Research/Architect no exceden la allowlist certificada salvo aprobación posterior.
- Tools nuevas se clasifican antes de smoke.
- La ausencia de una tool esperada se reporta como capability gap, no se compensa con bypass.
