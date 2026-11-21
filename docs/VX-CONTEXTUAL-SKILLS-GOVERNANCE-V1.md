# VX Skills contextuales + versionado preventivo — V1.0

**Fecha:** 2026-11-21. **Estado:** SOURCE / PR; no instalado ni activado en Kilo Desktop. **Baseline consultada:** Core VX 1.4 RC1: 18 agentes, 53 Skills. Las 44 Skills del Dev Team 2.3.0 forman un inventario diferente y no se suman ni se sustituyen por este documento.

## Decisión aprobada

Una biblioteca **global** por contexto, no por cliente ni repositorio, compatible con Agent Skills `SKILL.md` y Kilo Code/Kilo Desktop. Preservar `vx-dev-team` como único líder visible, sus especialistas, builders, ACL, MCP, AutoApprove, `kilo.jsonc` y scheduler actuales. Esta fase **solo escribe código fuente** en una rama y lo somete a PR; la instalación en el Windows del operador requiere autorización y pruebas separadas.

## Capas canónicas (no orquestadores duplicados)

- `vx-team-bootstrap` es el punto de entrada **ya permitido** al líder. Clasifica el tipo de tarea, establece un baseline mínimo y elige capacidades contextuales; su texto integra el gate V0 incluso si la nueva Skill todavía no está autorizada en runtime.
- `vx-context-routing` **propone** selección contextual por stack y tarea. La autorización real sigue en la allowlist exacta de cada rol, no en el catálogo.
- `vx-version-governance` define el **gate preventivo** antes de cambios X/Y/Z: HEAD, rama, estado sucio, versión, compatibilidad, recuperación, decisión release y changelog.
- `vx-technology-fit` sirve cuando se considera **añadir o reemplazar** un framework/componente; no para cada microcambio.
- `vx-desarrollo-escalonado` mantiene el método de desarrollo por etapas; `vx-engineering-harness` conserva coordinación y entrega. No introducir otro agente ni duplicar orquestador.
- `vx-skill-quality` comprueba formato, activación positiva/negativa, seguridad, superposición y compatibilidad de Skills propias/externas.

## Versionado preventivo V0

**Obligatorio para mutaciones, no consultas de lectura:**

`V0_BASELINE → CONTEXT_AND_METHOD → CHANGE_X/Y/Z → FOCUSED_VERIFY → REVIEW → VERSION_DECISION → PR`

En `V0_BASELINE` registrar `BASE_SHA/branch/status/dirty_paths/version_source/current_version`; nunca hacer `reset --hard`, stash automático ni escribir sobre cambios de terceros. **No** se crea tag ni se sube versión en cada commit. El bump depende del producto y el lanzamiento; SemVer solo donde ya aplique. En migración destructiva, revertir código no demuestra revertir datos.

### Matriz de método

| Tipo de tarea | Método mínimo | Verificación |
| --- | --- | --- |
| Microcambio | V0 + cambio localizado | test existente afectado |
| Bug reproducible | evidencia → hipótesis → causa raíz → corrección mínima | prueba de regresión, UPDATE/REPLACE/ADD |
| Funcionalidad nueva | contrato/aceptación → vertical slice → iteraciones | integración focalizada y compatibilidad |
| Refactor | invariantes actuales → diff limitado | prueba de equivalencia; no crear tests rituales |
| Integración | contratos productor/consumidor, ownership de rutas | contrato y error paths |
| Migración | compatibilidad de datos/protocolo, plan reversible, aprobación R3 si procede | ensayo aislado, rollback independiente |
| Hotfix | baseline + blast radius + fix mínimo | smoke y posterior análisis, no saltar permisos |
| Selección tecnológica | comparar existente, mínima y propuesta; licencia/seguridad/soporte | integración real según target |

## Políticas de plataforma

**Tauri 2** es preferencia para **nuevas aplicaciones expresamente Desktop**, no para web/API ni una migración no solicitada. Las apps existentes en Qt/PySide, .NET, Electron o control industrial permanecen en su stack salvo decisión fundamentada. Android se incluye solo si es parte del scope aprobado. Comunicación LAN, QR, BLE y Wi-Fi Direct se habilita exclusivamente por requisito y soporte real.

## Matriz de triggers

| Entrada | Skills relevantes | Deben quedar excluidas |
| --- | --- | --- |
| «Arregla login en aplicación PySide6» | version-governance, debug-triage, test-strategy | tauri, Android, React |
| «Crea nueva aplicación Windows» | context-routing, technology-fit; tauri si se elige | industrial / Android por defecto |
| «Añade validación a página Next.js» | version-governance, frontend-ux | escritorio, BLE |
| «Audita instrucciones de una Skill externa» | skill-quality, supply-chain-review | ejecutar scripts remotos |
| «Revisa este README sin cambios» | ninguna Skill de mutación obligatoria | crear rama/tag |
| «Actualizar driver PLC real» | industrial-control-safety, technology-fit; R3 explícito | ejecución automática |

## Seguridad de supply chain

Fuentes de inspiración: [Kilo Skills](https://github.com/Kilo-Org/skills), [Agent Skills spec](https://agentskills.io/specification), [Superpowers](https://github.com/obra/superpowers), [Anthropic Skills](https://github.com/anthropics/skills), [Vercel](https://github.com/vercel-labs/agent-skills). **No se incorporan ni ejecutan Skills de terceros.** Antes de aceptar paquetes, revisar autoría, commit, licencia, scripts, prompts de exfiltración, descarga y permisos. Un escáner estático opcional como [SkillSpector](https://github.com/NVIDIA/SkillSpector) no constituye permiso ni garantía.

## Certificación y activación posterior

1. **Source:** validate YAML name/directorio, referencias, catálogo, cambios mínimos y tests focalizados en la suite viva.
2. **PR:** CI y revisión independiente, merge solo si cumple reglas existentes; no declarar PASS sin evidence.
3. **Runtime pendiente:** hash de agentes y skills en HOME, backups DPAPI/manifest según instalador, diff exacto de allowlist por rol, solicitud de autorización independiente, instalación y `/reload`.
4. **Certificación Kilo Desktop:** escenarios SHOULD_TRIGGER, SHOULD_NOT_TRIGGER, permisos denegados, herramientas disponibles y ausencia de cambios R3. No reutilizar el PASS de snapshots anteriores.

El catálogo estructurado es [`registry/vx-contextual-skills-v1.json`](../registry/vx-contextual-skills-v1.json). La convivencia del Dev Team y las waves W1–W5 siguen las puertas del registro original.

## Changelog

- **V1.0.0 (2026-11-21):** cuatro Skills globales originales, enrutamiento contextual, baseline preventivo X/Y/Z, verificación de Skills con triggers positivos/negativos, metodología de desarrollo y rollout seguro. SOURCE; no instalación ni ACL runtime.
