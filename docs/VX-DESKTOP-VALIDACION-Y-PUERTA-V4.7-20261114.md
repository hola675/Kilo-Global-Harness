# VX Evolution — Validación Kilo Desktop y puerta de inicio V4.7

**Registro:** 2026-11-14, según evidencia proporcionada por el operador · **Ámbito:** única PC Windows, Kilo global · **Estado:** inventario de Desktop observado, prueba `task` completada; identidad efectiva y herramienta `skill` no certificadas. **Documento únicamente, sin acciones sobre la configuración.**

## 1. Inventario visible en Kilo Desktop

El operador copió la lista de la interfaz de Kilo Desktop; los siguientes siete agentes VX aparecen en `All workspaces`:

- `vx-frontend-adviser`
- `vx-inspector`
- `vx-integrador`
- `vx-researcher`
- `vx-security-reviewer`
- `vx-test-analyst`
- `vx-workers-adviser`

Además de otros agentes globales, la interfaz muestra las dos skills nucleares **`vx-engineering-harness`** y **`vx-evolution-core`** en `All workspaces`. La presencia en el listado acredita **descubrimiento/disponibilidad aparente**; no prueba que una skill haya sido invocada. Se observaron aproximadamente 33 entradas de skills en el texto copiado; no compararlo uno-a-uno con las 40 skills únicas del inventario CLI V4.6.0 hasta verificar filtros, rutas, normalización de nombres y ámbito del listado. No clasificar la diferencia como siete skills ausentes.

MCP adicionales visibles: cinco entradas Cloudflare con ámbito Vecidya, de las cuales cuatro muestran `Needs sign-in`; los servicios de memoria, imagen, Microsoft Learn y Sequential Thinking también aparecen listados. Estas entradas externas **no intervienen en la validación básica** de delegación VX ni certifican conexión/uso efectivo. No conectar ni modificar MCP como resultado de este diagnóstico.

## 2. Ensayos A/B/C de una sesión anterior

El operador aportó el informe del coordinador de tres llamadas `task`, tres sesiones hijas con estado `completed` y respuestas sintéticas correctas para regresión de autorización, prueba negativa y límites de contadores Observer. La captura del panel de subagentes mostraba tres elementos de delegación etiquetados según los roles solicitados. Esa evidencia es más fuerte que una simple respuesta narrativa: **delegaciones visibles en la interfaz**.

Persisten límites: los resultados `task` no expusieron identidad interna independiente del ejecutor ni llamadas internas de herramientas. El subagente C declaró haber llamado a `skill` para `vx-evolution-core`, pero el texto aportado no contenía la llamada observable. Estado: `skill_invocation=NO_VERIFICADO`, no `FALLO`; `competence=NO_MEDIDO`.

## 3. Ensayo nuevo en Kilo Desktop

El inventario de Desktop incluye los siete agentes VX y las dos skills VX descritas arriba. En una nueva prueba, el operador informa:

| Elemento | Evidencia reportada | Interpretación |
| --- | --- | --- |
| Agente solicitado | `vx-inspector` disponible | Disponible en interfaz, no demuestra agente ejecutor interno |
| Llamada `task` | VERIFICADO, dirigida a `vx-inspector` | Delegación visible/resultado `completed` |
| Sesión hija | VERIFICADO, `completed` | Terminación de la tarea delegada, no certifica calidad |
| Ejecutor interno | `NO_VERIFICADO` | Falta metadato de ejecución independiente |
| Llamada real `skill` | `NO_VERIFICADO` | No hay traza interna observada en sesión hija |
| Skill cargada | `DECLARADO` por la sesión hija | No certificar uso efectivo |
| Respuesta sobre Observer | Correcta en escenario ficticio | No mide competencias ni rendimiento |

**Cierre del hito:** compatibilidad *funcional visible* de Desktop con agentes VX, skills listadas y `task` comprobada. Observabilidad insuficiente para atribuir llamada interna `skill` o identidad ejecutora. No repetir ensayos idénticos sin una nueva fuente de evidencia.

## 4. Puerta de implementación V4.7 (diseño, no autorización de cambios activos)

El siguiente incremento será **publicación gobernada** para componentes del harness. Se puede implementar primero en **modo preparación/simulación** dentro del repositorio, sin reescribir HOME ni instalar en la configuración activa. Descomposición propuesta:

1. **Manifiesto/versionado:** identidad de componente, versión SemVer, hash de contenido, ruta global permitida, dependencias, estado de procedencia, firma/validación cuando exista y registro de origen. Sin incluir tokens ni prompts privados en informes.
2. **Plan de cambios sin aplicar:** diff acotado a archivos administrados por VX, comprobación de compatibilidad y política; verificación explícita de `kilo.jsonc`, settings y permisos como superficies **protegidas** por defecto.
3. **Pruebas y revisión separadas:** unidades, integración con HOME aislado Windows, fixture de rollback, rutas fallidas y revisión humana distinta del autor. No afirmar runtime validado por CI.
4. **Puerta de aprobación:** una solicitud de aprobación explícita por cambio, con objeto, impacto y hash exacto; rechazo/expiración/desajuste de hash implican **no aplicar**. Ninguna respuesta de chat o autoaprobación cuenta como permiso para modificar el sistema.
5. **Rollback verificable:** copia previa, hash antes/después, integridad de archivos, idempotencia, restauración conservadora ante error y ausencia de borrado de datos ajenos.
6. **Registro de resultados:** diferenciar `PREPARADO`, `CI_PASS`, `VERIFICADO_EN_PC`, `APROBADO`, `APLICADO`, `ROLLBACK`, `NO_VERIFICADO`; no inferir calidad de tareas ni atribución de subagentes.
7. **Control de alcance:** una PC; una rama permanente `main`; ramas `work/*` temporales; no tocar proyectos de cliente, SQLite del HOME real, modelos, MCP, AutoApprove, agentes o skills activos mientras no se apruebe una operación concreta. Scheduler OFF.

**Criterio mínimo para empezar:** crear un contrato versionado y tests sobre HOME temporal/sintético. El instalador actual es fuente de compatibilidad y debe permanecer reversible. El usuario debe autorizar **por separado** cualquier operación sobre su HOME real y cualquier cambio de configuración protegida.

## 5. Riesgos pendientes y prioridad

| Prioridad | Hallazgo | Tratamiento |
| --- | --- | --- |
| P0 | Publicación de cambios sin autorización fuerte | Diseñar antes de aplicar en V4.7 |
| P1 | Identidad y llamadas `skill` internas no visibles | Registrar `NO_VERIFICADO`; investigar trazas soportadas sin captura de payload |
| P1 | 11 nombres duplicados JSONC/Markdown | Mantener sin fusión: no se detectaron conflictos explícitos de campos simples; prioridad runtime no probada |
| P1 | 19 declaraciones `steps=10000000` | Documentar y medir antes de proponer límites alternativos; sin reducción por defecto |
| P2 | Diferencia inventario CLI/UI de skills | Comparar únicamente si hay un fallo funcional concreto; no suponer faltantes |
| Fuera de fase | Cloudflare `Needs sign-in` | Conectividad de un workspace ajeno al objetivo de VX; no bloquear V4.7 |

**Decisión:** registrar la compatibilidad visible de Kilo Desktop y pasar al **diseño implementable** de V4.7 en repositorio con pruebas aisladas. La falta de traza interna `skill` se mantiene como deuda de observabilidad, no como razón para detener la gobernanza. Nada de scheduler, modificaciones de configuración ni reorganización autónoma.
