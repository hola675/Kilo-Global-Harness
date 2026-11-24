# Política de pruebas y certificación
Versión del archivo: 0.1.0 | Última modificación: 2026-11-24

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
