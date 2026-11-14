# VX V4.1 — Protocolo de revalidación de evidencias multiagente

**General y sin datos de clientes.** No ejecuta procesos por sí solo ni modifica proyectos.

## Objetivo
Separar seis dimensiones: selector, ejecución paralela, retorno de subagentes, exactitud de hallazgos, pruebas ejecutadas y coste medido. Un PASS de delegación **no** es un PASS de tests.

## Snapshot Git al inicio y al final (solo lectura)
```powershell
git status --short --branch
git rev-parse --verify HEAD
git rev-parse --verify refs/remotes/origin/main
git branch --show-current
```
Capturar valores y, si cambian, revalidar únicamente los hallazgos afectados. `behind N` puede variar si otra sesión actualiza referencias; no atribuir origen sin evidencia. **No ejecutar git fetch, pull, switch o checkout en una auditoría SOLO LECTURA**; fetch escribe referencias locales aunque no cambie el working tree. Si no existe un comando o referencia, marcar NO VERIFICADO.

## Ciclo de validación
1. Registrar perfil propuesto por selector y nombres de agentes **efectivamente ejecutados**; distinguir planificación de ejecución real `task(background: true)`.
2. Capturar cada hallazgo con `ruta:línea`, revisión `HEAD`, comportamiento afirmado, agente y gravedad propuesta. No compartir secretos.
3. Deduplicar la misma causa; conservar revisiones independientes con técnicas diferentes cuando aporten evidencia distinta.
4. Reabrir archivos actuales. Comprobar existencia física de imports antes de afirmar que faltan; diferenciar documentos históricos de versión actual; comprobar si una preferencia guardada se ejecuta realmente. No inferir funcionamiento a partir de un nombre de función.
5. Reconciliar contradicciones entre agentes; declarar **DESCARTADO** el falso positivo con una prueba breve que lo refute, no eliminarlo silenciosamente.
6. Clasificar: **PASS** observado / **FAIL** defecto confirmado / **DESCARTADO** sospecha refutada / **NO VERIFICADO** sin evidencia o prueba. La presencia de CI, scripts o suite no acredita ejecución reciente. Solo declarar tests PASS con comando, salida y código de salida reales.
7. Cerrar informe con revisión Git inicial/final, retornos, hallazgos, pruebas ejecutadas/no ejecutadas, límites y siguiente verificación concreta.

## Ejemplo genérico de hallazgo
```yaml
id: H-001
estado: FAIL
severidad: media
revision: "<sha observado, o NO VERIFICADO>"
agente: "vx-researcher"
evidencia:
  ruta: src/feature.py
  lineas: "20-35"
  hecho: "La opción se persiste, pero no existe llamada que la aplique"
prueba_ejecutada: false
siguiente_verificacion: "Test de integración dirigido"
```
Esta plantilla es un **contrato de reporte por chat**, no un requisito de escribir archivos dentro del proyecto.

## Alcance y privacidad
- Si la tarea es SOLO LECTURA, no ejecutar tests, compilación, generadores, despliegues ni Git de escritura; `compileall` y empaquetadores pueden generar archivos.
- No publicar capturas, logs, paths de clientes o código privado en el repositorio público del harness.
- No relanzar agentes por rutina para corregir un error preliminar: primero verificar directamente en los archivos; volver a delegar solo ante una pregunta distinta.
- No inventar consumo de tokens; registrar solo métricas reportadas por cliente o proveedor.
- Mantener AutoApprove y restricciones efectivas.

## Aceptación
Un informe multiagente diferencia claramente: **agentes sugeridos**, **agentes lanzados**, **informes recibidos**, **exactitud revalidada**, **tests realmente ejecutados** y **revisión Git inicial/final**. Un informe preliminar erróneo queda **DESCARTADO con motivo**.
