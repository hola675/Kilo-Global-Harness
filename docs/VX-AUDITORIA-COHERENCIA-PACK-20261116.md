# VX Pack — Auditoría de coherencia y seguridad · 2026-11-16

**Alcance:** PR #30 y PR #31 comparadas con `main` y documentación oficial de Kilo; cambios correctivos en PR #31, NO instalados en perfil Windows del operador. Una prueba sintética o un SHA en GitHub no demuestra acceso efectivo de agentes, MCP ni aprobación humana.

## Hallazgos confirmados y acciones

| ID | Severidad | Problema comprobado | Corrección en PR #31 | Evidencia requerida |
|---|---|---|---|---|
| VX-A01 | Media | Fallback de `vx_skill_router.py` podía seleccionar skill fuera del perfil/fase | Solo candidatos elegibles; `NO_PROFILE_MATCH` cuando no existe | Test de perfil security + release |
| VX-A02 | Alta | `vx_task_dag.py` no cruzaba `writer:true` contra rol `writes` | Catálogo de escritura obligatorio; agentes lectores bloqueados | Test de owner lector e IDs |
| VX-A03 | Media | Estado BLOCKED con dependencias satisfechas quedaba sin explicación | `unblock_candidates` explícitos, sin auto-ejecutar | Test BLOCKED sin prerequisitos |
| VX-A04 | Media | Rutas de trabajo aceptaban formatos Windows y travesías mal normalizadas | Restricciones POSIX/Windows; absolutos, drives y `..` rechazados | Tests multiplataforma |
| VX-A05 | Alta | Doctor contaba archivos vacíos/symlinks como pack listo, y MCP con alias sensible a mayúsculas | Validación de frontmatter e integridad contra fuente cuando disponible; alias casefold | Tests de contenido manipulado |
| VX-A06 | Alta | Bootstrap de PR #30 podía borrar agentes/skills añadidos después de instalación al restaurar | Restore conservador: si detecta archivos nuevos, BLOQUEAR | Test Windows de alta posterior |
| VX-A07 | Alta | Restauración DPAPI de PR #30 podía sobrescribir archivos no modificados (plugins, observador, configuración adicional) | Restaura solo árboles gestionados y destinos realmente sobrescritos; conserva config y datos externos | Test de plugin modificado |
| VX-A08 | Alta | Snapshot sin aplicación o restauración repetida no distinguían estado seguro | Manifiesto de instalación obligatorio; BLOQUEAR restauraciones repetidas | Tests Windows de backup-only y doble restore |
| VX-A09 | Media | Catálogos MCP incompatibles en PR #30 (4) y #31 (5) | En PR #31 hay un único catálogo de 5 y bootstrap adaptado al mismo | Test catálogo y doctor |
| VX-A10 | Media | Tests dependían de conteos heredados de 10 skills y mensajes literales | Fixtures actualizados a Pack 0.2 y aserciones por comportamiento | CI Windows |
| VX-A11 | Alta | Bootstrap solo revisaba `kilo.jsonc`; otras configuraciones y skills externas podían crear duplicados | Preflight de `kilo.jsonc`, `kilo.json`, `config.json`, paths/urls y compatibilidad `.claude` | Tests de inline y rutas externas |
| VX-A12 | Alta | `mcp: deny` no garantiza negar herramientas MCP namespaced; inspector carecía de fallback explícito | Los 12 agentes VX inician su ACL con `"*": deny` y habilitan solo herramientas justificadas | Tests de ACL y validador PowerShell; Kilo runtime pendiente |
| VX-A13 | Alta | `vx-inspector` permitía parámetros amplios `git diff *` capaces de afectar rutas mediante opciones | Terminal completamente denegada; revisión mediante read/glob/grep/lsp y diff aportado | Test bash deny y revisión manual pendiente |
| VX-A14 | Media | `task: allow` permitía invocar subagentes externos/no verificados | Coordinador restringido a seis lectores VX, fallback deny | Unit test ACL; test de delegación Kilo pendiente |
| VX-A15 | Alta | Restaurador incremental V4 confiaba en rutas del manifiesto y podía restaurar parcialmente | Validación de destinos, copias, reparse points y hashes ANTES de escribir | CI Windows protege fichero privado y edición posterior |

## Arquitectura y límites aún abiertos

**Sigue deliberadamente sin automatizarse:** llamadas `task` reales, worktrees concurrentes, bus entre sesiones independientes, elección de modelos por coste y MCP conectados. Kilo Swarm no distribuye tareas ni comparte estado entre sesiones Agent Manager independientes. El DAG y el router son validadores deterministas **sin efectos**, no un scheduler.

**Pendientes de pruebas reales:** prioridad de agentes JSONC/Markdown en este HOME, disponibilidad de los 30 `SKILL.md` tras `/reload`, ejecución efectiva de `skill` por al menos tres perfiles, comportamiento de builders `edit/bash: ask`, conexiones MCP autenticadas solo si el usuario autoriza, restauración en una copia del perfil real sin exponer secretos.

**Puerta de integración:** CI Windows integral PASS en el HEAD candidato, review externa independiente, resolver explícitamente el solapamiento de PR #30/31, no fusionar ambas sin coordinación. Conservar PR #29 (aprobación WebAuthn V4.7.2) independiente. Mantener scheduler OFF.

## Fuentes de compatibilidad

- https://kilo.ai/docs/customize/skills
- https://kilo.ai/docs/customize/custom-subagents
- https://kilo.ai/docs/automate/agent-manager-workflows
- https://kilo.ai/docs/getting-started/settings/auto-approving-actions

**Interpretación de evidencia:** `PASS CI` = validación del código/fixture en runner Windows; `RUNTIME NO_VERIFICADO` = Kilo real del operador no ha sido inspeccionado. Las pruebas no convierten permisos declarados en permisos efectivos.
