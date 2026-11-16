---
name: vx-supply-chain-review
description: "Usar para auditar dependencias y software de terceros cuando una tarea mencione dependencias, sbom, licencia, cve. Exigir evidencia real y no cambiar permisos."
metadata:
  version: "0.2.0"
  origin: "vx-original"
---

# VX — Auditar dependencias y software de terceros

**Activación:** Usar para auditar dependencias y software de terceros cuando una tarea mencione dependencias, sbom, licencia, cve. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-security-reviewer`. **Revisor independiente:** `vx-inspector`. **Prerequisitos de conocimiento:** `vx-security-review`.

## Ejecución

1. Comprobar origen, pin, licencia y scripts postinstall/hooks.
2. Inventariar transitive dependencies y alertas verificables.
3. No descargar/ejecutar componentes desconocidos.
4. Documentar riesgo, alcance de permisos y rollback..

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://slsa.dev/
