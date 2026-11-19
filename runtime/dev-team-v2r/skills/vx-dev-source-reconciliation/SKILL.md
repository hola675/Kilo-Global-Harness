---
name: vx-dev-source-reconciliation
description: "Reconcilia documentación, versiones, ADR, changelogs y fuentes externas para resolver qué afirmación está realmente respaldada. Usar cuando hay versiones conflictivas, decisiones duplicadas, documentación desactualizada o una dependencia externa que debe verificarse."
compatibility: "Read-only; puede usar solo MCP documentales allowlistados del rol Research."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "research"
---

# VX Dev — Source Reconciliation

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
