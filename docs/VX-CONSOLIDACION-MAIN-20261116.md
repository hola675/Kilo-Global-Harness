# Consolidación final del repositorio — Pack VX V0.2 + VX Evolution V4.7.2

**Fecha:** 2026-11-16. **Ámbito:** `hola675/Kilo-Global-Harness`, únicamente código/documentación/pruebas Git. La autorización para fusionar ramas NO autoriza instalaciones en HOME, cambios de configuración Kilo, autenticación, tareas Windows, MCP ni despliegue productivo.

## Composición y reconciliación

| Fuente | Conservado | Resolución |
| --- | --- | --- |
| PR #28 | VX-D14–D24, alcance C, organización, Academy, mentoría, evaluador independiente y catálogos propuestos | Los catálogos siguen inactivos y su inventario de 7 agentes / 2 skills es histórico (15-11), no el Pack actual |
| PR #29 | `vx_approval_security_v472.py`, sus tests y diseño WebAuthn/FIDO2 | Se añade CI Windows, **sin** función WebAuthn real: `approval_granted=false`, `apply_supported=false` |
| PR #30 | Diseño de cinco nuevos builders y bootstrap cifrado DPAPI; acta original V0.1 preservada | **NO** conservar restaurador antiguo ni catálogo MCP antiguo de 4; supersedidos por versión auditada de PR #31 |
| PR #31 | 12 agentes, 30 skills, catálogo único 5 MCP, router, DAG, doctor, ACL, instalador V4 endurecido, bootstrap Windows y 17 hallazgos | Fuente principal del Pack V0.2, con inventario de scripts de bootstrap restringido |

### Controles de seguridad

- `main` única rama permanente; merges Git autorizados, NO autorización de `--mode apply` o `--confirm-migration` sobre el HOME real.
- `vx_publish_preview.py` (V4.7.0), `vx_approval_contract.py` (V4.7.1), `vx_approval_security_v472.py` (V4.7.2) permanecen **en repositorio**, **excluidos** de la lista de scripts de instalación del Pack. La publicación sigue deshabilitada.
- `approval_granted=false` y `apply_supported=false` en contratos; no hay enrolamiento, verificación de firmas, replay atómico, revocación durable ni auditoría protegida.
- Bootstrap DPAPI CurrentUser, backup verificado y rollback conservador; no reescribe `kilo.jsonc` ni toca MCP/credenciales existentes. `force-restore` tampoco borra nuevas skills; cambios entre backup y sustitución bloquean.
- Permisos de los 12 agentes VX denegados por defecto con excepciones explícitas; DAG STRICT con un escritor, builders con `edit: ask` y sin delegación libre. Los permisos efectivos se comprobarán en Kilo real.
- Academy, autocapacitación, worktrees paralelos, programación semanal/mensual y nuevos MCP continúan **INACTIVOS**.

### Evidencia y siguiente etapa

Antes de la consolidación, CI Windows de cada PR: #28, #29, #30, #31 PASS de sus respectivos SHA. La integración también debe superar CI Windows con `test_vx_approval_security_v472.py`, `test_vx_pack_bootstrap_v1.py`, validadores de 30 skills y tests de ACL/DAG, sin ocultar SKIP por permisos de symlink Windows. **No confundir CI con prueba manual del PC del operador**.

**Próxima etapa después del merge:** `doctor` read-only en HOME autorizado, compatibilidad/precedencia real de modos, carga `skill` desde tres agentes, simulación de instalación sin tocar Kilo, prueba de rollback en copia y autorización distinta antes de aplicar. [Roadmap canónico](VX-EVOLUTION-ROADMAP.md) · [Decisiones](VX-EVOLUTION-DECISIONES.md) · [Auditoría V0.2](VX-AUDITORIA-COHERENCIA-PACK-20261116.md).
