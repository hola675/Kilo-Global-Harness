---
name: vx-debugging-root-cause
description: "Usar para defectos reproducibles, fallos de builds/tests, errores de integración o regresiones; investigar causa raíz con hipótesis verificables antes de cambiar código. No usar para crear funciones nuevas sin error observado."
---

# VX Debugging Root Cause V0.1

**Objetivo:** corregir causas y no silenciar síntomas. Skill VX original, inspirada en principios públicos de `obra/superpowers`, sin importar scripts ni código externo. No aumenta permisos.

## Protocolo
1. **Reproducción:** obtener versión, entrada mínima, comando, código de salida y observado vs esperado. Si no puedes ejecutar, marcar `NO_REPRODUCIDO`.
2. **Delimitación:** identificar cuándo apareció el fallo (`git diff`, contrato, dependencia, entorno); excluir datos de cliente y secretos. No confundir correlación con causa.
3. **Hipótesis:** redactar un máximo de tres, cada una con evidencia que la confirmaría o falsaría; priorizar la más económica de probar.
4. **Aislamiento:** revisar capas en orden (entrada → contrato → función → IO/dependencia → salida), con logs mínimos y entorno sintético. No modificar producción ni instalar herramientas no autorizadas.
5. **Prueba que falla:** cuando sea posible, registrar un test que falle **antes** del cambio y pase **después**, con oráculo independiente. Evitar mocks que prueben únicamente el mock.
6. **Corrección:** modificar la causa más pequeña, sin eliminar controles, saltar tests o debilitar seguridad para hacer verde el build.
7. **Regresiones:** ejecutar suite relevante y negativa con permisos; registrar cualquier test no ejecutado.
8. **Cierre:** `{reproduction,root_cause,evidence,fix,tests_before_after,regressions,remaining_risks}`.

**Anti-patrones:** repetir parches sin nueva evidencia, tratar un stacktrace parcial como diagnóstico, declarar PASS sin ejecutar, afirmar una versión de API sin verificar, añadir un agente nuevo por cada error.
