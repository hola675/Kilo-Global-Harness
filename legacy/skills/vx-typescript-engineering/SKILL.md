---
name: vx-typescript-engineering
description: "Usar al implementar, revisar o depurar código TypeScript/Node, tipos, tsconfig, build y contratos; no activar por menciones incidentales."
metadata:
  version: "0.2.1"
  last_modified: "2026-11-22"
  origin: "vx-original"
---

# VX — Implementar TypeScript y Node mantenibles

**Activación:** Usar para implementar typescript y node mantenibles cuando una tarea mencione typescript, tsconfig, tsc, node. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-backend-builder`. **Revisor independiente:** `vx-test-analyst`. **Prerequisitos de conocimiento:** `vx-implementation-handoff`.

## Ejecución

1. Leer versiones reales y tsconfig.
2. Validar entradas externas en runtime.
3. Prohibir any y casts para ocultar fallos.
4. Controlar async, AbortSignal y timeouts.
5. Ejecutar scripts de proyecto y tests si autorizados.
6. Reportar compilación real..

## Caso TypeScript de aplicación Tauri 2

En aplicaciones de escritorio nuevas, TypeScript suele formar parte de una UI web de **Tauri 2** con comandos Rust; cargar `vx-tauri-desktop` bajo demanda si está disponible. Tipar cuidadosamente los mensajes `invoke` y validar en el lado Rust: una tipificación TS no sustituye comprobación de permisos ni entradas nativas. Compartir al integrador el contrato IPC publicado, sin editar simultáneamente capacidades, lockfiles o configuración Tauri. Preservar el framework existente cuando no haya migración solicitada.

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://www.typescriptlang.org/docs/
