---
name: vx-git-ci-quality
description: "Usar al crear, corregir u optimizar workflows CI/CD, GitHub Actions y gates de calidad; verificar triggers, permisos, propiedad de suites, evidencias y regresiones. No activar por simples operaciones Git sin cambios de CI."
metadata:
  version: "0.3.1"
  last_modified: "2026-11-22"
  origin: "vx-original"
---

# VX — Diseñar CI y gates de GitHub Actions

**Activación:** Usar para diseñar ci y gates de github actions cuando una tarea mencione git, github, ci, actions. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-qa-builder`. **Revisor independiente:** `vx-inspector`. **Prerequisitos de conocimiento:** `vx-test-regression`.

## Propiedad y ciclo de vida de tests

- Cada `test_*.py` directo debe tener un único gate propietario o pertenecer a un manifest canónico.
- Un gate posterior no reejecuta una suite completa anterior como ritual de regresión.
- Separar source/unit, smoke de integración/host y certificación runtime.
- Al modificar CI, decidir `UPDATE`, `REPLACE` o `ADD` para cada suite/gate afectado.
- Un gate supersedido se retira solo tras PASS del reemplazo; la historia se conserva fuera del CI activo.
- No mantener nombres/versiones históricas si la invariante vigente puede expresarse con un contrato actual más claro.

## Optimización de gates

- Mantener una matriz de propiedad: cada invariante tiene un gate principal; gates complementarios solo si observan otro entorno, contrato o riesgo.
- Separar comprobaciones baratas de formato/metadatos, tests unitarios focalizados, integración y smoke runtime. No presentar CI remoto como certificación del Kilo instalado.
- En PR, ejecutar los gates requeridos por cambios y política de rama; no omitir seguridad o integridad por ahorrar tiempo. En `main`, respetar los checks de protección obligatorios.
- Medir duración y fallos intermitentes antes de paralelizar o retirar suites. No optimizar eliminando cobertura ni suprimiendo fallos.
- Retirar gates supersedidos únicamente después de un PASS equivalente y con evidencia de cobertura. Evitar doble ejecución del mismo conjunto bajo nombres de versiones antiguas.

## Ejecución

1. Validar triggers, permisos mínimos y versiones de acciones.
2. Aislar fixtures Windows.
3. Ejecutar pruebas reproducibles vinculadas a SHA.
4. Revisar diff.
5. No merge si fallos.
6. No borrar ramas ajenas ni usar force push.
7. Para ramas activas de un equipo, exigir evidencia `last_reconciled_main_sha` antes del merge; después de avanzar main, emitir/atender `RECONCILE_REQUIRED` por cada otra rama activa desde su propio worktree. El dispatcher aún no está activado: consultar `docs/VX-TEAM-GIT-RECONCILIATION-V1.md`.

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://docs.github.com/en/actions/security-for-github-actions
