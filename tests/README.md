# Política de pruebas y certificación
Versión del archivo: 0.5.0 | Última modificación: 2026-11-24

## Estrategia
- T0 estática: esquema, YAML/JSONC, nombres, metadatos, referencias, licencias y manifiesto.
- T1 unitarias/contrato: tareas, transiciones, DAG, validación, deduplicación, MCP, scripts y fallos.
- T2 runtime real Desktop: descubrimiento, Code, permisos efectivos, invocación, overlap, Swarm, retorno, cancelación, reanudación y scope de archivos.
- T3 evals skills: routing positivo/negativo/ambiguo, baseline vs candidato, evidencia y fallos. Mantener fixtures comparables y repetir casos no deterministas cuando coste lo permita.
- T4 integración: proyecto web, ERP/local-first, desktop si procede, pruebas de integración y revisión independiente.
- T5 distribución: instalación limpia/repetida, actualización, configuración ajena, fallo parcial, rollback, desinstalación, rutas con espacios y Unicode, enlaces/junctions y sin red cuando proceda.
## Criterios
PASS solo con comando/resultado o evidencia observable en runtime, versión y commit; FAIL, BLOCKED, NOT_RUN explícitos. Un retorno de tool no certifica implementación. Pruebas enfocadas al delta y dependencias; sustituir pruebas redundantes tras demostrar equivalencia, conservar regresiones distintas y seguridad. No repetir toda la suite para todo cambio; ejecutar suite crítica y e2e al liberar. No acumular capturas ni logs con secretos.
## Métricas
Tiempo total, trabajo simultáneo observado (intervalos solapados), llamadas, reintentos, conflictos, criterios satisfechos, regresiones y uso/coste solo si proveedor expone dato válido. Baseline directa vs delegada en tareas equivalentes. No prometer aceleración porcentual antes de medir; bloquear release ante fallo crítico, permisos fuera de alcance, pérdida de datos, instalación no reversible o capacidades centrales sin certificar.

## Casos obligatorios derivados del código
- T2: versión/hash de CLI empaquetado frente a PATH; global vs perfil Desktop; marcador de instrucción efectivo en sesión nueva, shadowing, configuración de checkout principal, duplicados de skills/agentes.
- T2: Task foreground, dos background con solapamiento real y notificación al padre, task_id propio vs ajeno, depth 1 y nesting solo si habilitado; no confundir estado de tool con fin de hijo. Board incremental, alcance por raíz y ausencia de confirmación de lectura.
- T2: permisos por agente y sesión, denies heredados, MCP invocable y negado, estado de sandbox efectivo; no inferir confinamiento de worktree. Usar fixture inocuo, no probar fuera del alcance real autorizado.
- T2: error/cancelación, compactación, reanudación y reinicio separados; no equiparar persistencia de historial a recuperación de tarea activa.
- T3/T4: selección nativa de modelo, detección de skill, Team Learning sin plugin primero, aislamiento multi-root de observaciones.
- T5: proteger perfil administrado y sidecar, configuración ajena, divergencias de versión del host y recertificación. No exponer credenciales.
La referencia estática no acredita PASS de ningún caso.

## Comparación de resiliencia por modelo (F12)
Usar mismos fixtures, contratos, límites de herramientas y criterios de aceptación; registrar modelo/proveedor cuando observable, variante, contexto, operaciones correctas, fallos, reintentos, latencia, coste observable y recuperación. Seleccionar al menos dos modelos representativos autorizados (gratuito y de pago/suscripción si disponibles) sin prometer equivalencia. No ampliar coste sin autorización. Una prueba no ejecutada queda NOT_RUN/BLOCKED, no PASS. Comparar con baseline sin Harness cuando sea viable y proporcional. Revisar divergencias, adaptar granularidad/contexto y repetir solo caso afectado; no bajar criterios de seguridad/calidad ni confundir evaluación de salida con introspección del modelo.

## Núcleo F04
[Matriz focalizada del núcleo](F04-NUCLEO.md): carga y comportamiento del candidato completo; casos nuevos de decisión y aceptación, sin duplicar PoC F03.

## Equipo F05
[Matriz F05](F05-EQUIPO.md): descubrimiento, selección de roles, herramientas y aceptación por rol; recuperar comprobación pendiente de coordinación en F07 sin duplicar F03/F04.
