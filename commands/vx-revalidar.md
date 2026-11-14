---
description: Revalidar hallazgos multiagente en el árbol Git actual sin modificar archivos
agent: plan
---

En modo SOLO LECTURA, contrasta los resultados previos de subagentes para la tarea $ARGUMENTS. Si puedes, consulta el protocolo global `docs/PROTOCOLO-REVALIDACION-V4.1.md` del harness; aplica siempre estas reglas:

1. Captura `git status --short --branch`, `git rev-parse --verify HEAD` y `git rev-parse --verify refs/remotes/origin/main` al inicio y final. No ejecutes `git fetch`, pull, checkout, tests o build. Si Git no está disponible, NO VERIFICADO.
2. Distingue agentes realmente invocados y retornos recibidos de los sugeridos por el selector. Un plan no ejecuta agentes.
3. Comprueba ruta:línea y contenido actual para cada hallazgo. Verifica imports antes de declarar ausencia; distingue documentación histórica de funciones actuales.
4. Marca DESCARTADO los falsos positivos con evidencia concreta y FAIL únicamente defectos confirmados. Separa PASS del paralelismo de PASS de tests; si la suite no se ejecutó, NO VERIFICADO.
5. Si HEAD u origin/main cambian, reabre solo hallazgos afectados. No atribuyas la causa del cambio sin logs.
6. Entrega informe PASS/FAIL/DESCARTADO/NO VERIFICADO, gravedad, evidencia, revisión Git, pruebas realizadas frente a propuestas y próximos pasos.

No almacenes resultados privados del proyecto en el repositorio público del harness y no muestres secretos. No invoques de nuevo a los mismos subagentes si sus resultados ya están disponibles.
