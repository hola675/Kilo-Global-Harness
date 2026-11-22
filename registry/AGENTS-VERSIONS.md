# Registro de versiones y cambios de agentes
Registro central por sección · Actualizado: 2026-11-21

## Política
Cada agente lleva únicamente dos comentarios YAML en su frontmatter: `component_version` y `last_modified`, sin añadir claves desconocidas al esquema de Kilo. El líder muestra en `displayName` la versión global publicada del Harness, tomada del manifiesto de distribución, no su versión individual. Este registro centraliza el historial resumido y la versión individual de los agentes; los archivos operativos no contienen changelogs. La versión del Harness es independiente.

SemVer por archivo: PATCH corrección compatible; MINOR nueva capacidad compatible; MAJOR cambio incompatible. Actualizar fecha y descripción solo cuando se modifique realmente el agente. El historial previo al registro no se reconstruye artificialmente; Git conserva el detalle de los commits.

## Inventario y estado
| Agente | Archivo | Versión de seguimiento | Última modificación registrada | Resumen |
|---|---|---|---|---|
| vx-dev-team | agents/vx-dev-team.md | 1.0.1 | 2026-11-21 | Cabecera YAML con versión individual y fecha; líder muestra versión global del Harness |
| vx-dev-explorer | runtime/dev-team-v2r/agents/vx-dev-explorer.md | 1.0.1 | 2026-11-21 | Cabecera YAML compatible con versión y fecha; líder con versión visible |
| vx-dev-architect | runtime/dev-team-v2r/agents/vx-dev-architect.md | 1.0.1 | 2026-11-21 | Cabecera YAML compatible con versión y fecha; líder con versión visible |
| vx-dev-frontend | runtime/dev-team-v2r/agents/vx-dev-frontend.md | 1.0.1 | 2026-11-21 | Cabecera YAML compatible con versión y fecha; líder con versión visible |
| vx-dev-backend | runtime/dev-team-v2r/agents/vx-dev-backend.md | 1.0.1 | 2026-11-21 | Cabecera YAML compatible con versión y fecha; líder con versión visible |
| vx-dev-data | runtime/dev-team-v2r/agents/vx-dev-data.md | 1.0.1 | 2026-11-21 | Cabecera YAML compatible con versión y fecha; líder con versión visible |

Los restantes doce agentes se incorporarán al inventario cuando se inspeccionen sus versiones y cambios. No declarar fechas ni versiones ficticias.

## Cambios de esta sección
- 2026-11-21: v1.0.1 de seis agentes: dos comentarios de metadatos en el frontmatter YAML y versión global del Harness en el selector del líder; sin historial en archivos operativos.
- 2026-11-21: centralizado el historial individual; retirados los bloques largos introducidos durante el PR #106.
