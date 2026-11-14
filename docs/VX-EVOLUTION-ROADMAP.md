# VX Evolution — Roadmap maestro y próxima fase

**Edición:** 2026-11-14 · **Estado:** V4.6.0 en implementación (auditoría de solo lectura); V4.6.1–V5.0 **PENDIENTES** · **Ámbito:** **solo Kilo Code**, instalación **global** del usuario Windows, independiente del repositorio de cada proyecto.

## Fuente de verdad y definición de estados

- **Implementado en `main`**: el código, documentación y pruebas ya fueron integrados; no implica que la instalación de Kilo del usuario esté actualizada.
- **Validado en CI**: pruebas automáticas con fixtures aislados; no equivale a una prueba funcional en el Kilo de usuario.
- **Validado en Windows del usuario**: se ha recibido una ejecución real desde su terminal y/o Kilo.
- **Pendiente local**: código integrado, pero falta verificar instalación, migración o funcionamiento real.
- **Diseño**: contrato documentado; no hay garantía de ejecución ni de compatibilidad del runtime.
- **Propuesta**: pendiente de decisiones y aprobación; nunca activa por silencio.

La referencia canónica de decisiones es [VX-EVOLUTION-DECISIONES.md](VX-EVOLUTION-DECISIONES.md). La política de reunión está en [`config/vx-reunion-policy.v1.json`](../config/vx-reunion-policy.v1.json), **con todas las automatizaciones desactivadas**.

## Estado por versión

| Hito | Entrega principal | Código y CI | Validación local | Observación |
| --- | --- | --- | --- | --- |
| V4.0 | Equipos Kilo, router, control de escritor, instalación reversible | Integrado | Parcial según auditoría previa | Un solo escritor y hasta tres lectores |
| V4.1 | Revalidación de hallazgos y control de falsos positivos | Integrado | No documentada como prueba final independiente | Separar evidencia de hipótesis |
| V4.2 | Reconciliación de agentes JSONC/Markdown | Integrado | Auditor inicial suministrado; consolidación **pendiente** | No fusiona ni toca permisos |
| V4.3 | VX Evolution Core global, inventario, observaciones y propuestas manuales | Integrado | Base del usuario creada y utilizada | SQLite de operación privada en HOME |
| V4.4 | VX Observer Light opt-in, contadores horarios sin payload | Integrado | **Validado**: señales `session_idle=1` y `session_error=1`, integridad OK (muestra puntual) | Esas señales no miden calidad |
| V4.5 | Calendario, actas y decisiones locales manuales | Integrado | **Validado junto con V4.5.1 mediante SQLite v4** | No hay scheduler |
| V4.5.1 | **Primera reunión del mes conjunta**, secciones mensual/semanal a las 09:00 | **Integrado y CI Windows PASS** | **Validado**: instalación, SQLite v4, integridad y calendario real 2026-12-07, 09:00 | Observer `light`, scheduler OFF |
| **V4.6.0** | **Línea base global de agentes/skills, solo lectura** | **En implementación; CI en curso** | Pendiente de ejecución local de la nueva herramienta | Sin cambios de permisos, SQLite ni roles |
| V4.6.1–V4.6.3 | Matriz evaluable, capacitación y auditoría de equipos | Diseñadas, **PENDIENTES** | No aplica | No crear nuevos agentes, skills o jerarquías automáticamente |
| V4.7 | Publicación gobernada, SemVer individual, validación/rollback | Diseñado | No aplica | Revisión independiente y autorización explícita |
| V4.8 | Métricas fiables, coste y duración reales, comparación de eficacia | Diseñado | No aplica | Datos ausentes = `NO_MEDIDO` |
| V5.0 | Equipos especializados adaptativos, ascensos y delegación medidos | Conceptual | No aplica | Condicionado a evidencia y controles anteriores |

## Validación real V4.5.1 cerrada y alcance de PC única

**Confirmado por el usuario el 14 de noviembre de 2026:** instalador V4.5.1 aplicado y verificado; SQLite migrado con respaldo a **schema v4**; `integrity.database=ok`, `foreign_keys=true`, `joint_sessions_supported=true`, Observer `light`, `scheduled_meetings=false`; calendario conjunto del **lunes 7 de diciembre de 2026 a las 09:00** con **una sesión y dos secciones**. El inventario persistido informó **79 entradas**. Las ramas temporales anteriores se eliminaron y el repositorio quedó con `main`.

**VX-D08 CONFIRMADA:** una sola instalación en este PC Windows. No crear sincronización multi-PC, servicio de nube, DB compartida ni configuración por proyecto. La ruta operativa sigue bajo el HOME de Kilo. No es necesario migrar de nuevo la base de datos para V4.6.0.

La función nueva V4.6.0 **no escribe SQLite**, no produce evaluaciones de calidad ni cambia archivos de agentes o skills. La prueba de compatibilidad del CLI en el Windows real del usuario se solicitará después de superar CI.

## V4.6: objetivo y principio de mínima complejidad

Convertir `vx-capacitacion` y `vx-auditoria-equipo` de comandos de análisis/propuestas en **un sistema evaluable** de habilidades, roles y necesidades, alimentado por el inventario global de Kilo. **No** crear un modelo nuevo, un jefe ni un equipo permanente cada vez que aparezca una incidencia. Aprovechar antes capacidades existentes y las skills por demanda.

**Separación de responsabilidades:**
- `vx-capacitacion`: detecta brechas de competencias de skills, propone formación/skill candidata, define pruebas de competencia; **no activa cambios**.
- `vx-auditoria-equipo`: comprueba capacidad, calidad, permisos, fuentes duplicadas, delegación y jerarquías; propone consolidar, formar, ampliar equipo, ascender o retirar; **no decide ascensos por sí mismo**.
- `vx-upgrade`: prepara candidatas versionadas con diff y pruebas, sin publicarlas hasta V4.7 y nueva autorización.
- `vx-reunion`: recoge decisiones explícitas del usuario en la reunión semanal/mensual; una aprobación funcional nunca es despliegue automático.
- `vx-observer`: proporciona **solo señales operativas agregadas**; un evento `session_error` no es prueba de incapacidad.
- `vx-equipo`: sigue operando tareas, con **un escritor máximo** y hasta tres lectores; no reestructura roles en mitad de un desarrollo.

Referencia de implementación de línea base: [VX Capacidades V4.6.0](VX-CAPACIDADES-V4.6.0.md).

### Entregables propuestos

| Subfase | Entregable | Condición de aceptación |
| --- | --- | --- |
| **V4.6.0 — Línea base (primero)** | Inventario **de solo lectura** de agentes JSONC/Markdown y skills globales Kilo (rutas compatibles, duplicados, posibles conflictos, dependencias declaradas y huellas). Informe de huecos sin secretos. | Funciona en Windows sin modificar `kilo.jsonc`, agentes, skills, plugins, MCP ni permisos; informa claramente `desconocido/no_verificado`. |
| **V4.6.1 — Matriz de capacidades** | Contrato versionado para `agent/skill → capacidad → evidencia → prueba → estado`; rúbrica de competencias (aprendiz, especialista, senior, líder, principal) como **evaluación**, no como jerarquía activa. | No equipara número de tareas a calidad; marca evidencia incompleta; evita autocalificación única. |
| **V4.6.2 — Evaluaciones y formación** | Fixtures y escenarios reproducibles de al menos una habilidad existente y una posible brecha; propuesta de capacitación con criterios previos/después, posibles regresiones y coste estimado **solo cuando medible**. | Comparación verificable; sin ejecutar cambios sobre activos; pruebas negativas para falsos positivos y privacidad. |
| **V4.6.3 — Auditoría organizativa** | Identificar roles redundantes, fuente efectiva de cada agente, necesidades de supervisión y candidatos de delegación, fusión o contratación. Propuestas a `pending_review`. | Un evaluador independiente; no crear relaciones `supervises` activas, ascensos o agentes nuevos sin confirmación humana y validación técnica. |
| **Cierre V4.6** | Informe trazable + documentación, comandos por demanda, pruebas de Windows, CI y compatibilidad con observer/reuniones | CI PASS y validación local cuando corresponda; `main` integrado, solo una rama de trabajo temporal, rollback diseñado. |

### Contrato de evidencia y anti-alucinación

Toda propuesta mostrará: identificador, componente y fuente real, problema observable, evidencia reproducible, naturaleza del dato (`verificado`/`hipotesis`/`sin_datos`), competencia afectada, cambio mínimo, alternativas, test base y candidata, riesgo, costo si se midió, evaluador distinto, decisión y versión propuesta. **No** guardar prompts completos, datos de clientes, rutas privadas, contraseñas ni código de proyectos en SQLite.

Los contadores horarios de observer solo informan de uso/errores del runtime; **no** de éxito de una tarea, tokens, calidad, competencia o gasto. No inferir evaluación, contrataciones o mejoras a partir de esos contadores.

### Reglas de promoción y creación de nuevos equipos

1. **Primero formar, luego ampliar:** antes de proponer contratar un nuevo agente, demostrar que un skill nuevo o la capacitación de uno existente es insuficiente.
2. **Seniority por resultados:** la clasificación requiere tareas de dificultad conocida y verificadas externamente, precisión de revisión y baja regresión. Antigüedad, número de interacciones o autorreporte no bastan.
3. **Un senior también puede implementar:** dirigir no implica permanecer inactivo ni crear un jefe sin subordinados.
4. **Jerarquías sin ciclos** y sin autoaprobación de permisos. El registro de relaciones existe como estructura de datos; V4.6 no debe convertirlo automáticamente en políticas de ejecución.
5. **Costo de coordinación explícito:** preferir un solo especialista cuando multiagente añada más latencia/tokens que calidad.
6. **No importar repositorios masivamente:** las skills externas deben revisarse por licencia, procedencia, riesgo de instrucciones y pruebas antes de ser candidatas.

## Bloqueos, riesgos y decisiones aún abiertas

| Ref | Decisión/estado | Efecto |
| --- | --- | --- |
| VX-D07 | Retención de observaciones y backups **pendiente** | No añadir limpieza automática. Propuesta a decidir: 90 días horario, agregados más largos. |
| VX-D08 | **CONFIRMADA: solo esta PC Windows** | Sin sincronización multi-PC, nube ni SQLite remoto. |
| VX-D10 | Terminal TTY permite confirmación deliberada pero **no valida identidad** | Para publicación V4.7 hace falta aprobación más robusta. |
| VX-D11 | Criterios de ascenso y contratación **pendientes** | En V4.6 usar rúbrica propuesta y validación humana, sin atribuir rangos reales aún. |
| VX-D12 | Duplicidades de agentes y límites steps históricos **pendientes de auditoría efectiva** | Usar reconciliador V4.2 antes de editar fuentes. |
| Scheduler VX | **Desactivado por decisión explícita del usuario** | Ningún trabajo crea tarea Windows, recordatorio, notificación o reunión autónoma. |

## Próximo paso operativo

**P0 CERRADO** — Instalación V4.5.1 y SQLite v4 verificadas en el Windows del usuario; Observer light y datos conservados.

**P1 EN CURSO** — Integrar V4.6.0: auditoría Kilo global **solo lectura** y mapa de capacidades **declaradas**. No hacer migración adicional de SQLite hasta demostrar que hace falta.

**P2** — Probar evaluaciones y propuestas de capacitación/auditoría con fixtures de Kilo, registrar riesgos y presentar a `vx-reunion` para aprobación, nunca auto-publicar.

**P3** — Después del cierre y pruebas de V4.6, diseñar V4.7 de versiones, validación y rollback.

Se considera **finalizada la planificación** cuando este documento, el README y el registro de decisiones describen las mismas fases y se validan los invariantes en CI. Ningún cambio de runtime en V4.6 se autoriza con solo publicar este roadmap.
