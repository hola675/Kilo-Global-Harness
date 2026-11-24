# Auditoría final · Harness mínimo VX Dev Team

**Edición:** 2.0.0 · **Fecha:** 2026-11-21 · **Ámbito:** contenido activo del repositorio, dependencias de instalación y certificación fuente. No inventaría ni modifica archivos privados de Windows.

## Resultado de depuración

| Grupo | Conservados |
| --- | ---: |
| Agentes del manifiesto | 18 |
| Skills del manifiesto | 57 |
| Comandos activos | 3 |
| Archivos de soporte instalados | 2 |
| **Total instalado desde manifiesto** | **80** |
| Instalador, backend y dos dependencias de seguridad | 4 |
| Política `AGENTS.md` administrada | 1 |
| Documentación (incluido README) | 9 |
| CI de Windows | 1 |
| Pruebas actuales de Core | 2 |
| Parser de agentes para pruebas | 1 |
| Catálogo contextual de consulta, no ACL | 1 |
| `.gitignore` | 1 |
| **Total en el repositorio depurado** | **100** |

**Recorte:** 415 archivos rastreados antes de la eliminación por lote; **315 retirados**, **100 conservados**. El árbol antes de esta fase inicial tenía 416, incluyendo auditorías antiguas eliminadas por separado. El historial completo puede recuperarse por Git; los 315 no desaparecen de commits históricos.

## Qué se eliminó del árbol actual

| Carpeta/componente | Retirados |
| --- | ---: |
| Seis agentes VX legacy y 32 comandos fuera de Core | 38 |
| Instaladores y scripts auxiliares sin consumidores del Core actual | 28 |
| Skill sources no elegidas por el manifiesto | 7 |
| `runtime/` histórico fuera de Core | 26 |
| Registros viejos, propuestas, preflights y snapshots no instalados | 49 |
| Documentación histórica o superada | 70 |
| Tests históricos/fixtures reemplazados por certificación focal | 77 |
| Herramientas de prototipo no instaladas | 10 |
| Configuraciones experimentales, inventarios, plugin opcional y metadatos | 10 |
| **Total retirado por lote** | **315** |

La limpieza incluye `vx-integrador`, `vx-inspector`, otros cuatro agentes de generaciones antiguas, instaladores V3/V4/DevTeam-Only, comandos sin entrada al Core, componentes de VX Evolution/Observer/Academy y ensayos antiguos. **No se elimina ningún archivo incluido entre los 80 assets del manifiesto actual**.

## Dependencias de instalación que se conservaron

```text
scripts/Instalar-DevTeam-Unificado.ps1
  └─ scripts/vx_unified_pack.py
       ├─ scripts/vx_pack_coexist_v023.py
       │    └─ scripts/vx_pack_bootstrap.py
       ├─ registry/vx-unified-pack-v1.json
       ├─ rules/AGENTS-global-managed.md
       └─ 18 agentes / 57 Skills / 3 comandos / vx_task_dag.py
```

**Nota de seguridad:** `vx_pack_coexist_v023.py` y `vx_pack_bootstrap.py` conservan nombres anteriores, pero el instalador los **importa actualmente** para revisión de perfil, seguridad de rutas, backups DPAPI y reversión. El retiro de archivos fuente V4 fue posible tras fijar en el motor **las 14 rutas exactas históricas** admitidas para retirar de HOME. La ausencia de `registry/vx-agent-registry-v4.json` no elimina la protección frente a rutas ajenas.

## Validación que debe mantenerse

- `tests/test_vx_unified_pack_v1.py`: composición del pack, 100 rutas fuente, ACL Board y Skills, restricciones de builders, DAG/SQLite (dependencias, prioridades, bloqueo, reanudación, IDs de host, colisiones), simulación sin mutaciones, rollback y conservación de terceros.
- `tests/dev_team_agent_parser_support.py` y `tools/dev_team_agent_parser.py`: lectura de definición YAML para la prueba viva, sin modificar agentes.
- `.github/workflows/validar-harness.yml`: Windows, sintaxis del instalador, compilación, suite focal, diagnóstico y simulación aislados sin mutación de HOME.
- `scripts/Instalar-DevTeam-Unificado.ps1`: `Aplicar` exige `main` sincronizada y limpia, Kilo cerrado, confirmación y backup DPAPI.
- **Gates distintos:** `SOURCE_PASS` no confirma `INSTALLED_FILES_MATCH` ni `HOST_RUNTIME_PASS`.

## Exclusiones expresas

No eliminar del perfil del usuario plugins, SDK, MCP, contraseñas, archivos no gestionados, modelos, bases de datos ni proyectos. La limpieza es **solo del repositorio fuente**. El instalador mantiene su lista exacta de retiros de VX antiguos con respaldo y consentimiento.

No se habilitó ningún daemon, scheduler, servicio residente, Agent Manager ni tareas con Kilo Desktop cerrado. `task(background: true)` y Swarm se certificarán en el host después de instalar.

## Referencias vigentes

- [README](../README.md)
- [Arquitectura](ARQUITECTURA.md)
- [Instalación](VX-DEV-TEAM-UNIFIED-V1.md)
- [Autopilot y recuperación](VX-DEV-TEAM-AUTOPILOT-V2.md)
- [Política global](../rules/AGENTS-global-managed.md)

**Changelog:** v2.0.0 — reducción a paquete funcional, sustitución de CI de 943 líneas por suite focal, eliminación de dependencias del registro V4, documentación de rutas conservadas. v1.0.0 — inventario previo de 415 rutas (historia Git).
