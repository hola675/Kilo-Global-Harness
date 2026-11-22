# Registro de versiones y cambios de agentes
Registro central por sección · Actualizado: 2026-11-21

## Política
Las definiciones de agentes contienen solo configuración y comportamiento operativo. No incluir cabeceras de versionado, fechas de modificación ni changelogs en cada archivo. Este registro es la única fuente del historial y versión individual de los agentes. La versión del Harness es independiente.

SemVer por archivo: PATCH corrección compatible; MINOR nueva capacidad compatible; MAJOR cambio incompatible. Actualizar fecha y descripción solo cuando se modifique realmente el agente. El historial previo al registro no se reconstruye artificialmente; Git conserva el detalle de los commits.

## Inventario y estado
| Agente | Archivo | Versión de seguimiento | Última modificación registrada | Resumen |
|---|---|---|---|---|
| vx-dev-team | agents/vx-dev-team.md | 1.0.0 | 2026-11-21 | Inicio de registro externo; definición conservada |
| vx-dev-explorer | runtime/dev-team-v2r/agents/vx-dev-explorer.md | 1.0.0 | 2026-11-21 | Inicio de registro externo; definición conservada |
| vx-dev-architect | runtime/dev-team-v2r/agents/vx-dev-architect.md | 1.0.0 | 2026-11-21 | Inicio de registro externo; definición conservada |
| vx-dev-frontend | runtime/dev-team-v2r/agents/vx-dev-frontend.md | 1.0.0 | 2026-11-21 | Inicio de registro externo; definición conservada |
| vx-dev-backend | runtime/dev-team-v2r/agents/vx-dev-backend.md | 1.0.0 | 2026-11-21 | Inicio de registro externo; definición conservada |
| vx-dev-data | runtime/dev-team-v2r/agents/vx-dev-data.md | 1.0.0 | 2026-11-21 | Inicio de registro externo; definición conservada |

Los restantes doce agentes se incorporarán al inventario cuando se inspeccionen sus versiones y cambios. No declarar fechas ni versiones ficticias.

## Cambios de esta sección
- 2026-11-21: centralizado el seguimiento individual; retiradas las cabeceras de metadatos y los bloques de historial/contrato introducidos en seis archivos durante el PR #106. Se conserva la configuración funcional previa.
