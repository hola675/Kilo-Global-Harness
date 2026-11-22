---
name: vx-e2e-browser-testing
description: "Usar para probar flujos e2e en navegador aislado cuando una tarea mencione e2e, playwright, navegador, browser. Exigir evidencia real y no cambiar permisos."
metadata:
  version: "0.2.0"
  last_modified: "2026-11-21"
  origin: "vx-original"
---

# VX — Probar flujos E2E en navegador aislado

**Activación:** Usar para probar flujos e2e en navegador aislado cuando una tarea mencione e2e, playwright, navegador, browser. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-qa-builder`. **Revisor independiente:** `vx-frontend-adviser`. **Prerequisitos de conocimiento:** `vx-test-regression`, `vx-frontend-quality`.

## Ejecución

1. Usar entorno no productivo y datos sintéticos.
2. Selectores por roles, esperas y estados error/empty/loading.
3. Comprobar teclado/responsive.
4. Guardar evidencia con SHA.
5. Playwright MCP opcional, CLI si basta.
6. No usar sesiones personales reales..

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://playwright.dev/docs/best-practices
