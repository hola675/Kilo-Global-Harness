# Registro de versiones y cambios de agentes
Registro central por sección · Actualizado: 2026-11-23

## Política
Cada agente lleva únicamente dos comentarios YAML en su frontmatter: `component_version` y `last_modified`, sin añadir claves desconocidas al esquema de Kilo. El líder muestra en `displayName` la versión global publicada del Harness, tomada del manifiesto de distribución, no su versión individual. Este registro centraliza el historial resumido y la versión individual de los agentes; los archivos operativos no contienen changelogs. La versión del Harness es independiente.

SemVer por archivo: PATCH corrección compatible; MINOR nueva capacidad compatible; MAJOR cambio incompatible. Actualizar fecha y descripción solo cuando se modifique realmente el agente. El historial previo al registro no se reconstruye artificialmente; Git conserva el detalle de los commits.

## Inventario y estado
| Agente | Archivo | Versión de seguimiento | Última modificación registrada | Resumen |
|---|---|---|---|---|
| vx-dev-team | agents/vx-dev-team.md | 1.0.4 | 2026-11-23 | MCP dinámicos disponibles bajo autorización ask, respetando ACL nativas |
| vx-dev-explorer | runtime/dev-team-v2r/agents/vx-dev-explorer.md | 1.0.2 | 2026-11-23 | MCP dinámicos disponibles bajo autorización ask, respetando ACL nativas |
| vx-dev-architect | runtime/dev-team-v2r/agents/vx-dev-architect.md | 1.0.2 | 2026-11-23 | MCP dinámicos disponibles bajo autorización ask, respetando ACL nativas |
| vx-dev-frontend | runtime/dev-team-v2r/agents/vx-dev-frontend.md | 1.0.2 | 2026-11-23 | MCP dinámicos disponibles bajo autorización ask, respetando ACL nativas |
| vx-dev-backend | runtime/dev-team-v2r/agents/vx-dev-backend.md | 1.0.2 | 2026-11-23 | MCP dinámicos disponibles bajo autorización ask, respetando ACL nativas |
| vx-dev-data | runtime/dev-team-v2r/agents/vx-dev-data.md | 1.0.2 | 2026-11-23 | MCP dinámicos disponibles bajo autorización ask, respetando ACL nativas |

| vx-dev-platform | runtime/dev-team-v2r/agents/vx-dev-platform.md | 1.0.1 | 2026-11-23 | MCP dinámicos disponibles bajo autorización ask, respetando ACL nativas |
| vx-dev-reviewer | runtime/dev-team-v2r/agents/vx-dev-reviewer.md | 1.0.1 | 2026-11-23 | MCP dinámicos disponibles bajo autorización ask, respetando ACL nativas |
| vx-dev-quality | runtime/dev-team-v2r/agents/vx-dev-quality.md | 1.0.1 | 2026-11-23 | MCP dinámicos disponibles bajo autorización ask, respetando ACL nativas |
| vx-dev-security | runtime/dev-team-v2r/agents/vx-dev-security.md | 1.0.1 | 2026-11-23 | MCP dinámicos disponibles bajo autorización ask, respetando ACL nativas |
| vx-dev-research | runtime/dev-team-v2r/agents/vx-dev-research.md | 1.0.1 | 2026-11-23 | MCP dinámicos disponibles bajo autorización ask, respetando ACL nativas |
| vx-frontend-builder | agents/vx-frontend-builder.md | 1.0.2 | 2026-11-23 | MCP dinámicos disponibles bajo autorización ask, respetando ACL nativas |
| vx-backend-builder | agents/vx-backend-builder.md | 1.0.2 | 2026-11-23 | MCP dinámicos disponibles bajo autorización ask, respetando ACL nativas |
| vx-data-builder | agents/vx-data-builder.md | 1.0.2 | 2026-11-23 | MCP dinámicos disponibles bajo autorización ask, respetando ACL nativas |
| vx-qa-builder | agents/vx-qa-builder.md | 1.0.2 | 2026-11-23 | MCP dinámicos disponibles bajo autorización ask, respetando ACL nativas |
| vx-docs-builder | agents/vx-docs-builder.md | 1.0.2 | 2026-11-23 | MCP dinámicos disponibles bajo autorización ask, respetando ACL nativas |
| vx-editorial-builder | agents/vx-editorial-builder.md | 1.0.1 | 2026-11-23 | MCP dinámicos disponibles bajo autorización ask, respetando ACL nativas |
| vx-workers-adviser | agents/vx-workers-adviser.md | 1.0.2 | 2026-11-23 | MCP dinámicos disponibles bajo autorización ask, respetando ACL nativas |

La versión 1.0.0 de los doce agentes incorporados indica el inicio del seguimiento individual, no reconstruye su historial anterior.

## Cambios de esta sección
- 2026-11-23: los 18 agentes pasan a descubrimiento y solicitud MCP dinámicos mediante `permission: "*": ask`; no se alteran permisos concretos de herramientas nativas.
- 2026-11-23: seis agentes en 1.0.1 eliminan dependencias documentales de router/Skills obsoletas; líder 1.0.3 sincroniza selector con release 1.6.2-rc1.
- 2026-11-21: v1.0.1 de seis agentes: dos comentarios de metadatos en el frontmatter YAML y versión global del Harness en el selector del líder; sin historial en archivos operativos.
- 2026-11-21: centralizado el historial individual; retirados los bloques largos introducidos durante el PR #106.
