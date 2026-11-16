---
name: vx-git-ci-quality
description: "Usar para diseñar ci y gates de github actions cuando una tarea mencione git, github, ci, actions. Exigir evidencia real y no cambiar permisos."
metadata:
  version: "0.2.0"
  origin: "vx-original"
---

# VX — Diseñar CI y gates de GitHub Actions

**Activación:** Usar para diseñar ci y gates de github actions cuando una tarea mencione git, github, ci, actions. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-qa-builder`. **Revisor independiente:** `vx-inspector`. **Prerequisitos de conocimiento:** `vx-test-regression`.

## Ejecución

1. Validar triggers, permisos mínimos y versiones de acciones.
2. Aislar fixtures Windows.
3. Ejecutar pruebas reproducibles vinculadas a SHA.
4. Revisar diff.
5. No merge si fallos.
6. No borrar ramas ajenas ni usar force push..

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://docs.github.com/en/actions/security-for-github-actions
