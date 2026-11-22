# Registro de versiones: scripts, comandos y herramientas
Actualizado: 2026-11-22

## Política
Cada script/comando conserva versión individual y fecha en comentarios compatibles con su formato. La versión global del Harness es independiente. Este archivo centraliza únicamente el historial resumido; Git conserva los detalles. Los números 1.0.0 son el inicio del seguimiento individual, no versiones históricas reconstruidas.

| Componente | Versión | Fecha | Resumen |
|---|---|---|---|
| scripts/Instalar-DevTeam-Unificado.ps1 | 1.0.1 | 2026-11-22 | Identifica candidato 1.6.1; mantiene gates de instalación |
| scripts/vx_unified_pack.py | 1.0.0 | 2026-11-21 | Cabecera de seguimiento; lógica intacta |
| scripts/vx_verify_metadata.py | 1.0.2 | 2026-11-22 | Valida fechas reales, duplicados, rutas y estructura; conectado a CI Windows |
| scripts/vx_task_dag.py | 1.2.0 | 2026-11-22 | Añade auditoría SQLite de solo lectura por proyecto/tarea; conserva gate declarativo del líder |
| commands/vx-equipo.md | 1.0.0 | 2026-11-21 | Comentarios YAML; sin cambio funcional |
| commands/vx-dependencias.md | 1.0.0 | 2026-11-21 | Comentarios YAML; sin cambio funcional |
| commands/vx-editorial.md | 1.0.0 | 2026-11-21 | Comentarios YAML; sin cambio funcional |

Otros scripts existentes no se consideran versionados hasta inventario y revisión explícitos.
