# Skill ↔ MCP Integration V1

**Estado:** `SOURCE_READY_RUNTIME_INACTIVE`  
**Skills revisadas:** 34 no-MCP  
**Runtime/ACL/MCP config:** sin cambios

## Objetivo

Hacer que las skills de dominio usen MCP con criterio, sin duplicar el manual MCP dentro de cada una.

Cada skill ahora contiene un bloque corto `## Integración de evidencia/MCP` que responde cuatro preguntas:

1. ¿qué evidencia local/nativa debe preferirse?;
2. ¿qué familia MCP aporta valor si hace falta evidencia externa/runtime?;
3. ¿qué riesgos o límites aplican?;
4. ¿cómo reutilizar y entregar la evidencia sin repetir llamadas?

## Patrón transversal

```text
EVIDENCIA LOCAL SUFICIENTE?
  ├─ sí → continuar sin MCP
  └─ no → routing MCP
             ↓
        tool exacta autorizada
             ↓
          evidencia
             ↓
      ledger / handoff / reuse
```

## Ejemplos

- Explorer no usa Serena si glob/grep/LSP ya responden.
- Frontend no afirma comportamiento visual solo leyendo source; usa browser evidence si está autorizado.
- Quality no convierte un resultado MCP en PASS sin ejecución identificada.
- Security trata Snyk/Sentry/Postman/Cloudflare como fuentes condicionales, no como permisos.
- Release Readiness reutiliza CI/PR/Sentry ya recopilados en lugar de reconsultar.
- UX/UI Pro diferencia screenshot, runtime, código, docs y hipótesis.
- Incident Analysis usa timestamps/IDs exactos y no confunde correlación temporal con causa.

## Resultado

Las 34 skills no-MCP quedan alineadas con MCP Operations V1, pero no requieren que MCP esté presente. Si el runtime no expone una herramienta autorizada, la skill conserva su flujo normal y marca la evidencia faltante.
