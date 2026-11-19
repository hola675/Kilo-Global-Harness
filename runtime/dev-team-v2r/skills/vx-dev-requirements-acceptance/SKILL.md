---
name: vx-dev-requirements-acceptance
description: "Convierte una solicitud o cambio en requisitos verificables y criterios de aceptación trazables. Usar cuando el alcance es ambiguo, faltan condiciones de éxito o hay que separar requisito, supuesto, restricción y fuera de alcance."
compatibility: "Read-only; no implementa ni declara aceptación sin evidencia."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "requirements"
---

# VX Dev — Requirements Acceptance

## Frontera
No sustituye a `vx-dev-test-strategy`: esta skill define qué debe ser cierto; Test Strategy define cómo comprobarlo.

## Protocolo
1. Separar objetivo de negocio, comportamiento observable y restricciones.
2. Identificar actores, entradas, estados, errores y límites.
3. Convertir lenguaje ambiguo en criterios verificables sin inventar requisitos.
4. Marcar supuestos y decisiones pendientes explícitamente.
5. Distinguir MUST/SHOULD/COULD y fuera de alcance.
6. Vincular cada criterio con una fuente o decisión cuando exista.
7. Señalar requisitos no funcionales relevantes: seguridad, rendimiento, accesibilidad, compatibilidad y operación.
8. No tratar una expectativa implícita como requisito confirmado.

## Salida
`REQUIREMENTS`, `ACCEPTANCE_CRITERIA`, `ASSUMPTIONS`, `CONSTRAINTS`, `OUT_OF_SCOPE`, `OPEN_DECISIONS`, `TRACEABILITY`.

## Integración de evidencia/MCP
- Usar MCP solo para aclarar restricciones externas verificables, no para inventar requisitos del usuario.
- Las fuentes externas pueden respaldar compatibilidad, estándares o plataforma; los criterios de negocio siguen requiriendo fuente del proyecto/usuario.
- Registrar cualquier requisito derivado de docs como `DOCUMENTED`, no `CONFIRMED_BY_USER`.
