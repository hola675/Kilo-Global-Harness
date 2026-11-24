# VX Dev Team · Skills contextuales y versionado preventivo

**Vigencia:** Core VX **1.6.0-rc1**, 18 agentes y 57 Skills en fuente. Las cuatro Skills contextuales están incluidas en el manifiesto de instalación, pero **no se habilitan automáticamente en el permiso `skill`** del líder o builders. Tener `SKILL.md` en HOME no prueba que Kilo haya ejecutado el comportamiento.

## Qué se conserva

- **`vx-team-bootstrap`:** Skill de entrada ya permitida al líder. Establece objetivo, baseline Git y reglas de delegación antes de crear trabajo.
- **`vx-version-governance`:** criterios preventivos de versión, changelog, migración y compatibilidad antes de mutaciones.
- **`vx-context-routing`:** clasificación por `OBSERVED_STACK`, `PLATFORM_SCOPE` y `TASK_INTENT`, no por marca/cliente; solo recomienda una Skill que realmente esté permitida.
- **`vx-technology-fit`:** evaluación de compatibilidad, licencias, mantenimiento y riesgos antes de instalar o sustituir dependencias.
- **`vx-skill-quality`:** revisión de nombres, frontmatter, activación positiva/negativa, superposición y regresiones. No modifica allowlists.
- **`vx-desarrollo-escalonado`:** mantiene objetivos finales y entregas por fases; no crea un segundo líder.
- **`vx-engineering-harness`:** contratos de implementación, controles de archivos y coordinación con especialistas actuales.

El catálogo `registry/vx-contextual-skills-v1.json` contiene **11 escenarios de referencia** para decisiones de enrutamiento. Es un archivo auxiliar del Core conservado en la fuente, no una lista de permisos ni un test ejecutado dentro del host.

## Protocolo mínimo

1. Confirmar `HEAD`, rama, cambios sucios, versión y restricciones. Si no hay acceso a Git, registrar `BASELINE_UNVERIFIED`.
2. Seleccionar la menor cantidad de Skills relevantes. No intentar cargar Skills contextuales que el host deniegue.
3. Para cambios grandes, dividir en tareas independientes con `allowed_paths` y `write_scope: EXACT_FILES`, priorizar dependencias, reservar rutas y delegar por `task` real.
4. El líder continúa mientras hay hijos activos solo en trabajo seguro; validar cambios, pruebas y revisión antes de fusionar.
5. Distinguir `SOURCE_PASS`, `INSTALLED_FILES_MATCH` y `HOST_RUNTIME_PASS`.

No modificar `kilo.jsonc`, MCP, modelos ni AutoApprove; las ACL nuevas requieren diff exacto y autorización específica. Los resultados de los 11 escenarios están definidos como expectativas fuente, no como competencia runtime.

**Referencia:** [instalación](VX-DEV-TEAM-UNIFIED-V1.md), [Autopilot](VX-DEV-TEAM-AUTOPILOT-V2.md) y [política global](../rules/AGENTS-global-managed.md).
