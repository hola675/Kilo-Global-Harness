# Registro de versiones: scripts, comandos y herramientas
Actualizado: 2026-11-23

## Política
Cada script/comando conserva versión individual y fecha en comentarios compatibles con su formato. La versión global del Harness es independiente. Este archivo centraliza únicamente el historial resumido; Git conserva los detalles. Los números 1.0.0 son el inicio del seguimiento individual, no versiones históricas reconstruidas.

| Componente | Versión | Fecha | Resumen |
|---|---|---|---|
| scripts/Instalar-DevTeam-Unificado.ps1 | 1.0.5 | 2026-11-23 | Nombre del release actualizado; informes e instalación conservadora |
| scripts/vx_unified_pack.py | 1.2.0 | 2026-11-22 | Inventario histórico de archivos y versiones antes/después, scripts, SQLite y reportes JSON/Markdown por backup |
| scripts/vx_verify_metadata.py | 1.0.2 | 2026-11-22 | Valida fechas reales, duplicados, rutas y estructura; conectado a CI Windows |
| scripts/vx_task_dag.py | 1.5.1 | 2026-11-23 | Consulta readonly agregada a base independiente de observaciones del host |
| commands/vx-equipo.md | 1.0.1 | 2026-11-23 | Catálogo correcto de 57 Skills: 18 CORE, 35 CAPABILITY y 4 CONTEXTUAL |
| commands/vx-dependencias.md | 1.0.0 | 2026-11-21 | Comentarios YAML; sin cambio funcional |
| commands/vx-editorial.md | 1.0.0 | 2026-11-21 | Comentarios YAML; sin cambio funcional |

| runtime/kilo-observer/vx-runtime-observer.js | 0.2.0 | 2026-11-23 | Observador experimental con doble opt-in y eventos filtrados; sin instalación ni certificado Desktop |
| runtime/kilo-observer/lib/vx-observer-hooks.js | 0.1.0 | 2026-11-23 | Normalización determinista de eventos sin argumentos ni respuestas; tests Node offline |
| scripts/Eliminar-RamasFusionadas.ps1 | 1.0.0 | 2026-11-23 | Simulación Git por defecto; elimina solo work/* con PR fusionado, historial inmutable y SHA protegido |

Los módulos históricos de respaldo aún requieren versionado individual después de auditoría específica; no se retiran mientras sean dependencias del instalador.
