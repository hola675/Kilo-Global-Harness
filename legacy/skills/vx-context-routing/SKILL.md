---
name: vx-context-routing
description: "Usar para seleccionar Skills VX cuando la tarea combina tecnologías o especialidades y existe riesgo de activación errónea; decidir por stack real y alcance."
compatibility: "Agent Skills; Kilo Code/Kilo Desktop. Advisory-only, no ejecuta herramientas ni cambia ACL."
metadata:
  version: "1.0.1"
  last_modified: "2026-11-22"
  origin: "vx-unified"
  category: "routing"
---

# VX — Enrutamiento técnico contextual

**Propósito:** elegir el conocimiento mínimo necesario sin introducir Skills por cliente, marca o repositorio. No duplica al líder `vx-dev-team`: produce recomendaciones y el líder dirige la tarea y autoriza cargas conforme a su ACL.

## Detectar, no adivinar

1. Leer petición y límites explícitos, estructura, manifests/lockfiles, `AGENTS.md` local, configuración, dependencias, contratos y target; solo mediante herramientas disponibles.
2. Establecer `PRODUCT_CONTEXT` (web/SaaS, desktop, móvil, CLI, ERP, industrial, infraestructura/red, librería, híbrido) y `TASK_INTENT` (investigar, implementar, depurar, integrar, migrar, mejorar UX, publicar). Puede haber varios contextos, pero uno describe el cambio predominante.
3. Separar `OBSERVED_STACK` de `PROPOSED_STACK`, `EXPLICIT_CONSTRAINTS` de inferencias y `AUTHORIZATION` de disponibilidad de herramienta.
4. Resolver tensiones en este orden: seguridad y permisos efectivos → petición explícita → reglas locales más estrictas → arquitectura existente y contratos → preferencia global documentada → recomendaciones de fuentes externas. Una regla local nunca puede elevar una denegación del host.
5. Activar como máximo las 1–3 Skills imprescindibles por etapa cuando sea razonable. No cargar todas ni delegar a todos los agentes; justificar cada elección por una capacidad requerida, no por similitud textual.

## Tabla de enrutamiento (referencias, no cargas automáticas)

| Evidencia de necesidad | Skills sugeridas | Evitar |
| --- | --- | --- |
| Cambio de código/configuración | `vx-version-governance`, `vx-dev-project-policy` | editar sin baseline |
| Varios pasos o dominios | `vx-desarrollo-escalonado`, `vx-dev-team-handoff` | planificar microcambios artificialmente |
| Nuevo producto de escritorio expresamente aprobado | `vx-technology-fit` y, si se adopta Tauri 2, `vx-tauri-desktop` | Tauri en web/API o migrar Qt por inercia |
| App desktop existente con Qt, .NET, Electron u otro | Skill técnica aplicable a su stack y contratos | cambio de framework no solicitado |
| Web/SSR y aislamiento multitenant | `vx-saas-multitenant-cloud`, UX/frontend/backend según problema | introducir Android/Desktop |
| ERP + operación offline | `vx-erp-localfirst-modular`, datos/migraciones | imponer DB/cloud genérico |
| Red Windows, VPN, proxy, firewall | `vx-windows-network-systems`, seguridad | cambios R3 de sistemas sin permiso |
| PLC/PCC/operación física | `vx-industrial-control-safety` | tocar equipos reales sin gate |
| Comunicación física entre dispositivos | `vx-conectividad-dispositivos` | instalar Bluetooth por defecto |
| UI, accesibilidad, redacción | Skills UX/UI y editorial por necesidad | cambiar stack o inventar contenido |
| Nuevos paquetes/skills | `vx-technology-fit`, `vx-skill-quality`, supply-chain | importar scripts externos sin auditoría |

Las Skills no presentes o no autorizadas **no se invocan**: el líder puede aplicar la regla equivalente ya contenida en `vx-team-bootstrap` y remitir la propuesta a revisión, sin modificar ACL.

## Oráculos contra activaciones erróneas

- «Corregir un error de login en PySide6» → diagnóstico + versionado; no Tauri, Android, React ni migración.
- «Crear nueva aplicación de escritorio Windows» → evaluar Tauri 2 como preferencia de nuevas apps; Android solo si está dentro del alcance.
- «Cambiar el componente de un sitio web» → frontend/UX; no desktop ni drivers.
- «Diseñar integración de PLC» → seguridad industrial; no tocar hardware real.
- «Actualizar dependencia de API» → supply chain + verificación de contratos; no desplegar por defecto.

## Salida

`{product_context,task_intent,observed_stack,platform_scope,selected_skills,reason_per_skill,excluded_skills,conflicts,unknowns,requires_permission}`.

Este router no concede `skill`, `task`, `bash`, `edit` ni MCP. `SELECTED` significa recomendada, no ejecutada.
