# VX Evolution — Roadmap maestro y próxima fase

**Edición:** 2026-11-14 · **Estado:** V4.6.0–V4.6.1 integradas (CI Windows PASS y CLI local validado); V4.6.2 integrada, CI Windows PASS y CLI local probado; batería conversacional sintética 5/5 coincidencias declaradas (sin verificación de ejecutores); V4.6.3 código/CI Windows PASS y CLI local VALIDADO: 30 hallazgos de revisión estática (11 solapamientos, 19 steps elevados, 0 diferencias explícitas); procedencia y precedencia del runtime no verificadas; V4.7–V5.0 **PENDIENTES** · **Ámbito:** **solo Kilo Code**, instalación **global** del usuario Windows, independiente del repositorio de cada proyecto.

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
| **V4.6.0** | **Línea base global de agentes/skills, solo lectura** | **Integrada en main; CI Windows PASS** | **CLI local PASS:** 39 fuentes agente, 28 agentes, 40 skills, 11 solapamientos, 19 steps elevados | Sin cambios de permisos, SQLite ni roles |
| **V4.6.1** | Matriz agente/skill→capacidad→test→evidencia declarada | **Integrada en main; CI Windows PASS** | **CLI local PASS:** 76 filas, 15 declaraciones, 0 evidencias | Prueba interactiva Kilo pendiente; seniority sin asignar |
| **V4.6.2** | Cinco ensayos sintéticos reproducibles y comparación de evidencias declaradas | **Código + CI Windows PASS (27 tests)** | **CLI Windows PASS; chat: 5/5 respuestas coincidentes**. Delegaciones/skills sin traza independiente | Fixture público no ciego; calidad NO_MEDIDO, sin escritura |
| **V4.6.3** | Auditoría organizativa declarativa: duplicados, steps, perfiles y procedencia no verificada | **Código y CI Windows PASS (26 tests)** | **CLI Windows PASS:** 11 solapamientos, 19 steps elevados, 0 diferencias explícitas; 30 hallazgos | Ninguna colisión/identidad certificada, sin cambios activos |
| V4.7.0 | Publicación gobernada, SemVer y preview DRY_RUN | Integrada en main (`36a73e01`); CI Windows PASS | Tests con HOME sintético | Sin instalación, aprobación autenticada ni rollback activo |
| V4.7.1 | Contrato de solicitud/verificación de aprobación | En implementación sobre rama de trabajo | Pruebas aisladas pendientes | Verificación estructural no autentica ni habilita apply |
| V4.8 | Métricas fiables, coste y duración reales, comparación de eficacia | Diseñado | No aplica | Datos ausentes = `NO_MEDIDO` |
| V5.0 | Equipos especializados adaptativos, ascensos y delegación medidos | Conceptual | No aplica | Condicionado a evidencia y controles anteriores |

## Validación real V4.5.1 cerrada y alcance de PC única

**Confirmado por el usuario el 14 de noviembre de 2026:** instalador V4.5.1 aplicado y verificado; SQLite migrado con respaldo a **schema v4**; `integrity.database=ok`, `foreign_keys=true`, `joint_sessions_supported=true`, Observer `light`, `scheduled_meetings=false`; calendario conjunto del **lunes 7 de diciembre de 2026 a las 09:00** con **una sesión y dos secciones**. El inventario persistido informó **79 entradas**. Las ramas temporales anteriores se eliminaron y el repositorio quedó con `main`.

**VX-D08 CONFIRMADA:** una sola instalación en este PC Windows. No crear sincronización multi-PC, servicio de nube, DB compartida ni configuración por proyecto. La ruta operativa sigue bajo el HOME de Kilo. No es necesario migrar de nuevo la base de datos para V4.6.0.

Las herramientas V4.6.0 y V4.6.1 **no escriben SQLite** ni cambian archivos de agentes o skills. El 2026-11-14 se verificaron sus ejecuciones CLI en el Windows real del usuario; falta prueba de invocación interactiva de Kilo tras /reload. Los estados de desempeño siguen NO_MEDIDO.

## V4.6: objetivo y principio de mínima complejidad

Convertir `vx-capacitacion` y `vx-auditoria-equipo` de comandos de análisis/propuestas en **un sistema evaluable** de habilidades, roles y necesidades, alimentado por el inventario global de Kilo. **No** crear un modelo nuevo, un jefe ni un equipo permanente cada vez que aparezca una incidencia. Aprovechar antes capacidades existentes y las skills por demanda.

**Separación de responsabilidades:**
- `vx-capacitacion`: detecta brechas de competencias de skills, propone formación/skill candidata, define pruebas de competencia; **no activa cambios**.
- `vx-auditoria-equipo`: comprueba capacidad, calidad, permisos, fuentes duplicadas, delegación y jerarquías; propone consolidar, formar, ampliar equipo, ascender o retirar; **no decide ascensos por sí mismo**.
- `vx-upgrade`: prepara candidatas versionadas con diff y pruebas, sin publicarlas hasta V4.7 y nueva autorización.
- `vx-reunion`: recoge decisiones explícitas del usuario en la reunión semanal/mensual; una aprobación funcional nunca es despliegue automático.
- `vx-observer`: proporciona **solo señales operativas agregadas**; un evento `session_error` no es prueba de incapacidad.
- `vx-equipo`: sigue operando tareas, con **un escritor máximo** y hasta tres lectores; no reestructura roles en mitad de un desarrollo.

Referencia de línea base: [VX Capacidades V4.6.0](VX-CAPACIDADES-V4.6.0.md). Matriz de evaluación propuesta: [VX V4.6.1](VX-MATRIZ-COMPETENCIAS-V4.6.1.md). Ensayos sintéticos: [VX V4.6.2](VX-ENSAYOS-COMPETENCIAS-V4.6.2.md).

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
| VX-D14 | **CONFIRMADO: alcance C** — gobernar únicamente componentes VX propios | El inventario/respaldo puntual del resto de Kilo es preparatorio, no administración continua ni autorización de borrado. |
| VX-D15 | **Pack inicial todo-en-uno propuesto, parcialmente definido** | Faltan catálogo MCP, protección de respaldos, distribución y política de actualización. |
| VX-D16 | **CONFIRMADO: instalación limpia objetivo** | Estado final global: built-in Kilo + agentes/skills/comandos/reglas propios VX activos; externos personalizados anteriores respaldados y archivados fuera de descubrimiento, sin borrado irreversible. No autoriza migración real. |
| VX-D17 | **CONFIRMADO: conservar MCP y añadir faltantes solo con autorización individual** | Una migración limpia no toca MCP actuales ni credenciales; catálogo VX detecta candidatos ausentes y solicita aprobación por servidor antes de instalar/configurar. |
| Scheduler VX | **Desactivado por decisión explícita del usuario** | Ningún trabajo crea tarea Windows, recordatorio, notificación o reunión autónoma. |

## Próximo paso operativo

**P0 CERRADO** — Instalación V4.5.1 y SQLite v4 verificadas en el Windows del usuario; Observer light y datos conservados.

**P1 CERRADO, CLI LOCAL VALIDADO** — V4.6.0 auditoría global de solo lectura y mapa de capacidades declaradas ejecutada en Windows real: 28 agentes únicos, 40 skills, 11 solapamientos y 19 límites steps elevados. No migrar SQLite.

**P1.1 CERRADO, CLI LOCAL VALIDADO** — V4.6.1 matriz global y evidencia declarada: 20 pruebas unitarias y smoke/rollback CI Windows PASS; 76 filas, 15 capacidades declaradas y cero evidencias en equipo real. Prueba interactiva Kilo pendiente. Sin seniority ni pruebas reales automáticas.

**P1.2 BATERÍA SINTÉTICA CERRADA, SIN CERTIFICACIÓN DE COMPETENCIA** — V4.6.2: 27 tests y smoke/rollback CI Windows PASS; 5 casos/5 destinos en CLI local; después, 5/5 respuestas de chat coincidentes con fixture público, sin traza independiente de subagentes, sin archivos de comparación antes/después y sin evaluación ciega. La restricción PowerShell en Kilo continúa; no requiere levantarse. [Validación CLI](VX-VALIDACION-CLI-V4.6.2-20261114.md) · [Cierre de batería interactiva](VX-CIERRE-BATERIA-V4.6.2-20261114.md).

**P2.1 V4.6.3 CLI LOCAL VALIDADO; AUDITORÍA ESTÁTICA CERRADA** — Instalación reversible y verificación PASS en Windows real; 11 solapamientos de nombre con 0 diferencias explícitas comparables, 19 declaraciones steps sobre el umbral y 30 hallazgos de revisión. Skills duplicadas, skills de perfil no observadas y agentes router no observados = 0. La precedencia y autoría real siguen NO_VERIFICADO. [Acta V4.6.3](VX-VALIDACION-LOCAL-V4.6.3-20261114.md) · [Guía V4.6.3](VX-AUDITORIA-ORGANIZATIVA-V4.6.3.md).

**P2.2 PENDIENTE DE EVIDENCIA DE RUNTIME** — Examinar, por vía manual autorizada, trazas mínimas de ejecución de subagentes (sin copiar sesiones completas) y diseñar evaluaciones independientes/ciegas. Las 11 coincidencias JSONC/Markdown carecen de diferencias en campos explícitos comparados pero su prioridad real sigue NO_VERIFICADO; las **19 de 19 definiciones con steps > 400** muestran `10 000 000` en JSONC, sin otros valores elevados. La semántica documentada en Kilo es límite de iteraciones de herramientas, pero su eficacia y el consumo real permanecen NO_VERIFICADOS. Clasificar funciones y medir tareas representativas antes de proponer límites candidatos; revisar las seis declaraciones edit/bash allow sin cambiar permisos. Ninguna modificación sin pruebas y aprobación. [Revisión steps/precedencia V4.6.3](VX-REVISION-STEPS-PRECEDENCIA-V4.6.3-20261114.md).

**P2.3 CONFIRMACIÓN DE INTERFAZ, AÚN SIN PRUEBA DE RUNTIME** — El operador verificó que Kilo Code muestra `Pasos máximos = 10000000` en los agentes `architect` y `code-reviewer`, en coincidencia con el inventario JSONC. **No** prueba cuál fuente JSONC/Markdown define el campo final ni que el límite se aplique durante una sesión. Próximo paso: inspección de metadatos de `sources[].fields/steps/mode` para estos dos agentes mediante el auditor V4.6.0, solo lectura y sin exportar prompts. [Evidencia y guía](VX-REVISION-STEPS-PRECEDENCIA-V4.6.3-20261114.md).

**P2.4 DESKTOP VALIDADO PARCIALMENTE** — El operador confirmó en Kilo Desktop los siete agentes VX y las skills `vx-engineering-harness`/`vx-evolution-core` como `All workspaces`; una nueva delegación `task` a `vx-inspector` devolvió sesión hija `completed`. La identidad interna y la herramienta `skill` dentro del subagente siguen NO_VERIFICADO; no repetir pruebas sin nueva observabilidad. Los MCP Cloudflare marcados `Needs sign-in` no bloquean estas funciones locales. [Acta Kilo Desktop y puerta V4.7](VX-DESKTOP-VALIDACION-Y-PUERTA-V4.7-20261114.md).

**P3 V4.7.0 PREVIEW — INTEGRADO EN MAIN** — PR #25 integrada mediante `36a73e01fe46d17573f46baf82cf8c88bf5d7559`; CI Windows PASS. Publicó únicamente contrato de componentes y preview DRY_RUN. Validación de symlinks nativos Windows y HOME real no acreditada por tests sintéticos. V4.7.1 implementa solo solicitud/verificación estructural, no autorización autenticada y mantiene `apply_supported=false`. [Contrato V4.7.0](VX-PUBLICACION-GOBERNADA-V4.7.md) · [Contrato V4.7.1](VX-APROBACION-GOBERNADA-V4.7.1.md).

**P3.1 V4.7.1 — INTEGRADO EN MAIN** — PR #26 fusionada por squash con commit `d7f954c6d6b6cf237594b27e2a6a69734a4df4b8`; CI posterior al merge en revisión. Contrato de solicitud/aserción estructural, sin autenticación, firma, anti-replay ni capacidad de aplicar. `approval_granted=false` y `apply_supported=false`. Deben mantenerse estas restricciones hasta desarrollo y autorización de una fase posterior.

**P3.2 CORRECCIÓN DE TESTS TTY EN PR INDEPENDIENTE** — Los dos fixtures heredados de reuniones fijan `stdin=subprocess.PIPE` para garantizar entrada no interactiva en Windows: el primer ensayo con `subprocess.DEVNULL` falló en CI porque Windows NUL puede devolver `isatty()=True`. El cambio de PIPE se está revalidando en CI. No cambia `local_confirmation()` ni los permisos. La prueba completa local interactiva debe repetirse en Windows del operador tras CI y merge. [Alcance y verificación](VX-REPRODUCIBILIDAD-TTY-V4.7.1.md).

**P4 V4.7.2 — SIGUIENTE FASE EN DISEÑO** — Analizar autenticación y separación de funciones; comprobar el modelo de confianza y antirreplay, primero en un entorno aislado. No exponer `apply` ni permitir aprobaciones activas sin un mecanismo autenticado, respaldos y autorización explícita.

**P4 NUEVA ÉPICA PROPUESTA: PACK VX BOOTSTRAP GLOBAL (SIN IMPLEMENTAR)** — Decisión C confirmada: VX gobierna únicamente componentes VX propios. El operador confirmó el destino limpio (VX-D16): conservar agentes nativos de Kilo y activar solo personalizaciones del Pack VX; los agentes/skills personalizados anteriores se conservarán respaldados fuera de las rutas de descubrimiento una vez autorizada la migración. Pack inicial versionado con agentes/skills/comandos VX, respaldo preinstalación verificable, inventario/comparación de MCP y soporte de actualización reversible. La configuración MCP se decide por separado. No confundir backup total, instalador actual que solo respalda destinos administrados, ni lista de MCP con conectividad real. La política MCP quedó confirmada en VX-D17: conservar todos los existentes y proponer cada faltante para aprobación individual. Siguen pendientes la composición del catálogo MCP (núcleo y perfiles), protección de copias, distribución y política de actualizaciones. La desactivación de terceros durante el bootstrap requiere un plan exacto y autorización excepcional distinta de la opción C; no es administración continua. [Acta alcance C y preguntas](VX-ALCANCE-C-PACK-BOOTSTRAP-20261115.md). **No instalar ni modificar Kilo hasta aprobación del diseño.**

Se considera **finalizada la planificación** cuando este documento, el README y el registro de decisiones describen las mismas fases y se validan los invariantes en CI. Ningún cambio de runtime en V4.6 se autoriza con solo publicar este roadmap.
