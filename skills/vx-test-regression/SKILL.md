---
name: vx-test-regression
description: "Usar cuando se solicita implementar pruebas automatizadas VX de una tarea concreta, con fixtures aislados y casos positivos, negativos y regresiones; no confundir tests escritos con ejecutados."
---

# VX Test Regression V0.1

**Ámbito:** convertir criterios de aceptación en tests de proyecto autorizados; guía para `vx-qa-builder` y el integrador. Skill VX original; no otorga `edit`, `bash` ni acceso a MCP.

## Preparación

Identificar el framework de tests y sus dependencias ya presentes. Recibir alcance de cambios, rutas permitidas, línea base, escenario, oráculos verificables y restricciones. Evitar tests contra producción, bases de datos reales, endpoints que incurran en cargos o credenciales.

## Casos mínimos por cambio

- **Positivos:** resultado esperado para entrada permitida.
- **Negativos:** error ante entrada inválida, autorización insuficiente y estados límite.
- **Regresión:** caso vinculado a comportamiento anterior que debe mantenerse.
- **Idempotencia/concurrencia:** solo si aplica al código bajo prueba.
- **Aislamiento:** fixtures desechables, no datos del cliente ni secretos.

## Salida objetiva

Para cada test: `case_id`, propósito, entrada sintética, aserción, ruta, comando de ejecución y estado `NO_EJECUTADO|PASS|FAIL|SKIP`. Solo declarar PASS/FAIL si hay ejecución real y exit code. Si el agente no puede usar terminal, remitir comandos al ejecutor autorizado y mantener `NO_EJECUTADO`.

Una suite ejecutada no certifica automáticamente competencia, enseñanza ni promoción. El revisor independiente analiza calidad del oráculo y falsos positivos. No modificar herramientas, permisos, HOME ni MCP por una skill.
