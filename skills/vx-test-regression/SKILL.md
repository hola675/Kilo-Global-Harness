---
# last_modified: "2026-11-22"
name: vx-test-regression
description: "Usar al escribir, actualizar, sustituir o depurar pruebas automatizadas de un cambio concreto; elegir UPDATE, REPLACE o ADD por invariante, fixtures aislados y ejecución focalizada. No activar para diseñar estrategia sin implementar tests."
metadata:
  version: "0.2.1"
---

# VX Test Regression

**Ámbito:** convertir criterios de aceptación en tests de proyecto autorizados; guía para `vx-qa-builder` y el integrador. Skill VX original; no otorga `edit`, `bash` ni acceso a MCP.

## Preparación

Identificar el framework de tests y sus dependencias ya presentes. Recibir alcance de cambios, rutas permitidas, línea base, escenario, oráculos verificables y restricciones. Evitar tests contra producción, bases de datos reales, endpoints que incurran en cargos o credenciales.

## Certificación viva

Antes de escribir o proponer un test:

1. Identificar la invariante actual.
2. Clasificar la acción como `UPDATE`, `REPLACE` o `ADD`.
3. `ADD` solo cuando exista riesgo diferencial.
4. Si `REPLACE`, mantener temporalmente el test anterior únicamente hasta obtener PASS real del reemplazo.
5. Tras PASS, retirar el supersedido del CI activo si el alcance autorizado lo permite.
6. No crear suites nuevas solo porque cambió la versión del componente.
7. La historia queda en Git/PR/registry, no en tests activos duplicados.

## Selección y optimización de pruebas

1. Identificar el cambio observable y el **oráculo independiente**: no basta comprobar que existe una frase, archivo o mock si el riesgo es funcional.
2. Buscar la prueba existente más cercana y decidir `UPDATE`, `REPLACE` o `ADD` antes de escribir. `ADD` requiere nueva invariante o riesgo que ninguna prueba cubra.
3. Ejecutar primero la prueba focalizada. Ampliar a contrato, integración, smoke o E2E cuando cambien interfaces, dependencias, instalación, concurrencia o seguridad.
4. Mantener temporalmente el test antiguo durante `REPLACE`; retirar solo cuando el reemplazo haya pasado y cubra los mismos riesgos. Si no puede demostrarse equivalencia, conservar ambos y explicar la diferencia.
5. Evitar suites por versión, nombres históricos y reejecución completa de gates anteriores sin motivo. CI mantiene la cobertura vigente y la historia queda en Git.
6. Medir coste cuando resulte relevante: duración, repetición, flakiness y mantenimiento. Optimizar sin reducir las invariantes verificadas.
7. Separar `SOURCE_PASS`, `CI_PASS` y `HOST_RUNTIME_PASS`. Un test local o CI nunca certifica herramientas reales del host ni instalación.

## Casos mínimos por cambio

- **Positivos:** resultado esperado para entrada permitida.
- **Negativos:** error ante entrada inválida, autorización insuficiente y estados límite.
- **Regresión:** caso vinculado a comportamiento anterior que debe mantenerse.
- **Idempotencia/concurrencia:** solo si aplica al código bajo prueba.
- **Aislamiento:** fixtures desechables, no datos del cliente ni secretos.

## Salida objetiva

Para cada test: `case_id`, propósito, entrada sintética, aserción, ruta, comando de ejecución y estado `NO_EJECUTADO|PASS|FAIL|SKIP`. Solo declarar PASS/FAIL si hay ejecución real y exit code. Si el agente no puede usar terminal, remitir comandos al ejecutor autorizado y mantener `NO_EJECUTADO`.

Una suite ejecutada no certifica automáticamente competencia, enseñanza ni promoción. El revisor independiente analiza calidad del oráculo y falsos positivos. No modificar herramientas, permisos, HOME ni MCP por una skill.
