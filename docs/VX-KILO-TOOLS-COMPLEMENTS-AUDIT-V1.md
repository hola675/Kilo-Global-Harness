# Kilo Tools & Complements Audit V1

**Estado:** `SOURCE_READY_RUNTIME_INACTIVE`  
**Runtime:** sin cambios

## Hallazgo principal

Kilo Code 2026 ya incorpora suficientes capacidades para que el harness no necesite convertir cada necesidad en un MCP nuevo.

Prioridad:

```text
Kilo native tool
   ↓ si insuficiente
specialized MCP
   ↓ si sigue faltando una capacidad transversal
trusted internal plugin
```

## Nativas que debemos aprovechar mejor

- `websearch` + `webfetch`: investigación web general.
- `lsp`: evidencia semántica barata antes de Serena/Codebase Memory.
- `plan`, `todowrite`, `todoread`: planificación/resumibilidad del líder.
- `task`: subtareas enfocadas en la misma worktree.
- `agent_manager`: sesiones top-level independientes y worktrees.
- `browser_open`: preview localhost en Agent Manager.
- Browser Automation: registra `kilo-playwright`.
- `board_post` / `board_read`: coordinación Kilo Swarm, solo si el modelo de trabajo realmente necesita background collaboration.

## Consolidaciones propuestas

### Browser

Preferir el Playwright integrado de Kilo si pasa nuestros smokes. Mantener un Playwright MCP separado solo si demuestra una capacidad necesaria que el integrado no ofrece.

Chrome DevTools permanece especializado: DOM/runtime/network/performance de bajo nivel, no reemplazo automático de Playwright.

### Web

Usar `websearch/webfetch` para web pública general.

Conservar:
- Context7 para documentación de librerías;
- Microsoft Learn para ecosistema Microsoft.

Así evitamos un MCP genérico extra solo para web.

## Kilo Platform MCP

Es útil para:
- usage/spend de Kilo;
- agent profiles;
- cloud agents.

Pero su `call` es una gateway mixta: puede consultar o mutar según endpoint.

Propuesta:
- líder únicamente;
- `search`: candidato read-like;
- `call`: ASK o DENY hasta clasificar endpoints;
- subagentes: DENY inicialmente.

## Plugin propio propuesto: vx-harness-guard

No instalar plugin externo genérico.

Construir uno pequeño y auditable para problemas que las permissions no resuelven bien:

1. audit trail local de tool/permission/session events;
2. redacción post-tool antes de logs reutilizables;
3. preservación de IDs/evidence ledger durante compaction;
4. gates adicionales solo cuando no puedan expresarse con ACL.

Nunca:
- auto-allow silencioso;
- tokens/credenciales;
- telemetría remota por defecto;
- bypass de edit/write/bash/MCP permissions.

## Agent Manager

No reemplaza `task`.

`task`:
- hijo enfocado;
- mismo workspace/worktree;
- resultado vuelve al padre.

Agent Manager:
- sesión top-level;
- branch/worktree propio;
- diff/terminal/transcript independiente.

Para nuestro harness, Agent Manager debe ser Wave 2 y solo líder con `ask` hasta certificar aislamiento.

## Kilo Swarm

Puede mejorar comunicación de varios task children, pero ahora no es necesario para el modelo depth=1 secuencial.

Mantener DENY hasta evaluar:
- children en background;
- conflictos de archivos;
- contaminación de instrucciones por board;
- reglas de qué mensajes son evidencia vs coordinación.

## Extensiones VS Code

Las más útiles para los agentes son las que mejoran LSP/diagnósticos. Una extensión puramente visual mejora al humano, no necesariamente al agente.

Priorizar según proyecto:
- JS/TS: ESLint + TypeScript language service;
- Python: Pyright/Pylance compatible;
- Rust: rust-analyzer;
- YAML/JSON schema tooling;
- Docker tooling.

Evitar duplicar funciones que ya cubren GitHub/Postman/Playwright MCP salvo valor humano claro.

## Oleadas

### Wave A — inventario y consolidación
- capturar tools nativas visibles por agente;
- capturar MCP tools exactas;
- comparar Playwright externo vs `kilo-playwright`;
- comprobar websearch/webfetch;
- comprobar LSP real.

### Wave B — tools nativas
- líder: plan/todo;
- Research: websearch/webfetch;
- Frontend/Quality: browser_open ASK si disponible.

### Wave C — orchestration
- Agent Manager ASK solo leader;
- sin Swarm todavía.

### Wave D — Kilo MCP
- search read-like;
- call clasificado endpoint por endpoint.

### Wave E — plugin propio
- desarrollar `vx-harness-guard`;
- tests aislados;
- sin instalar hasta revisión manual.
