---
name: vx-dev-source-reconciliation
description: "Reconcilia documentación, versiones, ADR, changelogs y fuentes externas para resolver qué afirmación está realmente respaldada. Usar cuando hay versiones conflictivas, decisiones duplicadas, documentación desactualizada o una dependencia externa que debe verificarse."
compatibility: "Read-only; puede usar solo MCP documentales allowlistados del rol Research."
metadata:
  version: "1.1.0"
  last_modified: "2026-11-21"
  origin: "vx-dev-original"
  category: "research"
---

# VX Dev — Source Reconciliation

## Reconciliación del catálogo contextual (Core VX 1.5 SOURCE)

Cuando haya conflictos entre catálogo global, documentos, archivo de agente, Skills instaladas o versión de un repositorio, **distinguir el alcance antes de comparar**: `VX_CORE_SOURCE` (catálogo global), `DEV_TEAM_SOURCE` (capas propuestas 18+9+9+8), `KILO_HOST_RUNTIME` (Windows del operador) y `PROJECT_LOCAL` (manifest, ramas e instrucciones del proyecto). Los totales de catálogos distintos no se suman, y un resultado CI source no certifica las habilidades cargadas por Kilo.

Para cambios X/Y/Z, usar el baseline preventivo de `vx-version-governance` como **referencia documental**, nunca como autorización de cargar otra Skill; registrar `BASE_SHA`, rama, versión declarada, fecha de evidencia y versión propia de la Skill. Un SHA de archivo fuente y otro de HOME distintos se clasifican `HASH_DRIFT`, no `RUNTIME_FAIL` por deducción. Ante diferencia local, listar rutas/tipos y preservar cambios, sin sincronizar, reescribir, instalar, activar ni modificar ACL.

Contrastar el catálogo `registry/vx-contextual-skills-v1.json` solo si la fuente está disponible; su `SOURCE_PROPOSED_NOT_RUNTIME_ACTIVATED` no demuestra carga en Kilo ni habilitación de `permission.skill`. Los prerequisitos de waves W1–W5 y la inspección de roles siguen siendo obligatorios. No invocar MCP fuera de los IDs exactos autorizados ni inferir acceso a runtime desde enlaces GitHub.

**Salida ampliada:** `{source_scope,project_scope,source_sha,runtime_sha_observed_or_unknown,source_version,installed_version_or_unknown,source_ledger,contradictions,hash_drift,missing_evidence,suggested_resolution,mutations_performed:false}`. Sin evidencia suficiente devolver `SOURCE_RUNTIME_UNVERIFIED`.

## Jerarquía
1. Evidencia runtime/ejecución actual.
2. Source actual y tests ligados al mismo SHA.
3. Documentación oficial/versionada.
4. ADR/changelog del proyecto.
5. Fuentes secundarias corroboradas.

## Protocolo
- Registrar cada fuente con fecha/versión/procedencia.
- Distinguir “describe” de “demuestra”.
- No elegir automáticamente la fuente más nueva si trata otra versión.
- Detectar contradicciones explícitas y qué dato falta para resolverlas.
- Para dependencias externas, preferir docs oficiales y version-aware.
- Mantener quotes mínimos; sintetizar, no copiar.

## Salida
`SOURCE_LEDGER`, `CONTRADICTIONS`, conclusión, confianza y unknowns.

No editar documentación ni decidir arquitectura por sí sola.

## Integración de evidencia/MCP
- Para documentación/versiones, priorizar Context7 y Microsoft Learn cuando estén autorizados.
- Registrar tool, versión, URL/ID y contradicciones con `vx-dev-mcp-evidence-ledger`.
- No volver a consultar una fuente si un handoff ya contiene evidencia suficiente y reusable.
