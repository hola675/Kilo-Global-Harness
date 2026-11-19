---
name: vx-dev-mcp-server-playbook
description: "Guía de propósito y selección para la biblioteca MCP del harness. Usar cuando hay que saber qué servidor sirve para documentación, código, GitHub, navegador, observabilidad, seguridad, APIs, Cloudflare, IDA o generación visual."
compatibility: "La superficie real depende del runtime. Confirmar tools visibles antes de cualquier llamada; el playbook no sustituye ACL."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "mcp-catalog"
---

# VX Dev — MCP Server Playbook

## Mapa de capacidades

| Servidor/familia | Usar principalmente para | Evitar asumir |
|---|---|---|
| Context7 | docs/versiones de librerías | que toda versión o tool esté disponible |
| Microsoft Learn | docs y ejemplos Microsoft | que cubra productos no Microsoft |
| Serena | símbolos, referencias, implementaciones | que lectura/edición tenga el mismo riesgo |
| Codebase Memory | grafo, arquitectura, cobertura, cambios | que índice esté fresco o que query sea read-only |
| GitHub | repo, commits, PR, issues, Actions | que una tool de GitHub sea solo lectura |
| Cloudflare API | docs/OpenAPI y, si se autoriza, API | que `execute` sea read-only |
| Playwright | comportamiento real de UI/browser | que observar una sesión autenticada sea inocuo |
| Chrome DevTools | DOM/runtime/red/consola/perf | que evaluate/navigate sean observación |
| Sentry | errores, logs, traces, métricas | que telemetría no contenga datos sensibles |
| Snyk | salud/scans de dependencias/código/IaC | que scan no envíe o procese source externamente |
| Postman | workspaces, colecciones y APIs | que endpoint/toolset dinámico sea estable |
| IDA | análisis/referencia reverse engineering | que abrir/ejecutar Python sea read-only |
| ImageGen | generación/edición visual | que sea herramienta de análisis o sin coste |

## Regla
Antes de usar cualquier fila: confirmar servidor, tool exacta, schema, efectos y datos que salen del host.

## Salida
`SERVER`, `TOOL`, `PURPOSE`, `INPUT_DATA`, `SIDE_EFFECT_EXPECTATION`, `AUTH_EXPECTATION`, `EVIDENCE_RETURNED`.
