# VX Evolution — Roadmap maestro y próxima fase

**Edición consolidada:** 2026-11-16 · **Fuente:** integración autorizada de PR #28 (decisiones/Academy), #29 (V4.7.2 contratos), #30 (bootstrap inicial histórico) y #31 (Pack VX V0.2 seguro). **En repositorio:** 12 agentes VX, 31 skills originales, un catálogo de 6 MCP candidatos, router y DAG de solo lectura; V4.7.2 sin autenticación, `approval_granted=false` y `apply_supported=false`. **En Windows del operador:** instalación real aún NO actualizada ni validada con este pack; la última instalación/CLI documentada sigue siendo V4.6.3. Scheduler OFF, paralelismo de escritores OFF, MCP nuevos OFF, autorreformas y ascensos OFF. La CI Windows certifica fixtures, no actividad en Kilo real.

**Ámbito vinculante:** solo Kilo Code global en una PC Windows; no Codex/Claude, no configuración de agentes en repositorios ni sincronización multi-PC. 


## Integración canónica Pack VX + V4.7.2 (2026-11-16)

| Componente | En repositorio después de integrar | En Kilo Windows real | Seguridad operativa |
| --- | --- | --- | --- |
| V4.7.2 | Contratos de identidad, assertion WebAuthn, replay simulado, revocación y auditoría en memoria; tests CI Windows | **NO DESPLEGADO** | `approval_granted=false`, `apply_supported=false`, sin verificación criptográfica/persistencia |
| Pack VX V0.2.2 | 12 agentes (7 originales + 5 builders), 31 skills y DAG/router read-only | **NO INSTALADO/NO VERIFICADO** | Un escritor STRICT; tools/permiso MCP fail-closed declarados, requieren comprobación runtime |
| Bootstrap y backups | Instalador V4 incremental y bootstrap DPAPI cifrado/rollback conservador | **NO EJECUTADO SOBRE HOME REAL** | Frena ante archivos nuevos, configs inline o skills externas; snapshot CurrentUser, no portable |
| VX Academy V4.8 | Catálogos, organización y mentores **solo propuestas** de PR #28 | **NO ACTIVA** | No hay agentes certificados ni autopromociones |
| MCP | Seis candidatos de catálogo (GitHub/Context7/Serena/Playwright/Cloudflare/IDA) | **NO INSTALADOS POR ESTE PACK** | Configurar uno a uno solo por autorización específica |

**Siguiente fase:** validar Kilo real en modo lectura y una copia del HOME, revisar políticas de skills MCP y ACL; definir decisión posterior de migración, no suponer que la fusión Git la autoriza. [Detalle de integración](VX-CONSOLIDACION-MAIN-20261116.md) · [Auditoría de 17 discrepancias](VX-AUDITORIA-COHERENCIA-PACK-20261116.md).

### Puerta de instalación del Pack VX 0.2.2 (2026-11-16)

El operador autorizó instalar el Pack en su único Windows, con diagnóstico, simulación libre de bloqueos, Kilo cerrado, respaldo DPAPI CurrentUser y verificación de archivos antes del test real de permisos. **Aún no se ha ejecutado la instalación local.** La aprobación no alcanza a nuevos MCP, WebAuthn, scheduler, cambios JSONC, permisos globales ni concurrencia de escritores. [Guía de convivencia V0.2.3](VX-INSTALACION-CONVIVENCIA-0.2.3-WINDOWS.md).

### Migración V0.2.3 por convivencia (2026-11-16)

El PC Windows del operador confirmó 19 agentes inline y skills en .agents/skills y .kilocode/skills; la migración limpia 0.2.2 se bloqueó correctamente, sin cambios. El instalador por convivencia V0.2.3 permite conservar esas fuentes y aplicar únicamente los archivos VX, siempre que no existan colisiones de nombres; incluye preflight read-only, respaldo DPAPI incremental, instalación sin borrar árboles externos y rollback acotado. La presencia de inline o skills externas no constituye por sí misma un conflicto. La instalación está condicionada a preflight limpio y Kilo cerrado. El runtime sigue NO VERIFICADO. [Guía V0.2.3](VX-INSTALACION-CONVIVENCIA-0.2.3-WINDOWS.md).

### Piloto de certificación de runtime VX 0.2.4 (2026-11-16)

Evidencia aportada por el operador: Pack V0.2.3 instalado por convivencia en su Windows con 19 agentes inline y 17 skills en directorios compatibles; hashes de 12/12 agentes y 31/31 skills VX completos, MCP sin cambios, backup DPAPI presente. En sesión real de Kilo la herramienta nativa skill cargó vx-engineering-harness y vx-ida-mcp-reverse-engineering. Una búsqueda glob hacia HOME fue bloqueada con external_directory: deny, comportamiento esperado.

Siguen sin demostrar por llamada nativa: selección de vx-integrador, disponibilidad de builders, delegación task real a vx-inspector, permisos efectivos edit/bash de builders y conexión al MCP IDA. El agente activo informó Kilo con alias Yoan, no prueba la activación de vx-integrador. NO aumentar external_directory ni usar glob fuera del proyecto para certificar. Nuevo comando /vx-certificar y validador sintético vx_runtime_smoke_v1.py para separar las ocho puertas y rechazar certificaciones basadas únicamente en autoinformes. La evidencia declarada nunca concede permisos. [Acta y próximo piloto](VX-CERTIFICACION-RUNTIME-20261116.md).

### Piloto P1 de delegación nativa (2026-11-16)

El operador mostró `Vx Integrador` activo y cinco builders visibles en el selector de Kilo. En P1 informó dos llamadas `task` a `vx-inspector`: la primera `BLOCKED` por comprobación redundante del selector y la segunda `completed` tras declarar la observación del operador en el handoff, devolviendo una revisión de solo lectura de `README.md`. El README confirma la cabecera reportada y admite desactualizaciones editoriales. Se considera **delegación con resultado observable por informe**; permisos efectivos edit/bash y conexión IDA MCP siguen NO VERIFICADOS. El handoff del coordinador ya transmite fuente del prerequisito y el inspector no intenta volver a verificar la interfaz ni escalar permisos. Próxima puerta: P2 de `edit: ask` en sandbox sintético, solo con autorización separada y verificando que la primera solicitud denegada no escriba. [Acta](VX-CERTIFICACION-RUNTIME-20261116.md).

## Resumen ejecutivo del estado y puertas del siguiente tema

| Línea de producto | Qué construye | Estado comprobable | Puerta para avanzar |
| --- | --- | --- | --- |
| **A. Núcleo VX** | Registro, equipos, observador limitado, actas, inventario y auditoría | V4.0–V4.6.3 integradas; validaciones locales parciales | Separar evidencia sintética de ejecución real y mantener mínima observación |
| **B. Gobierno de cambios VX** | Preview, contrato de solicitud, identidad, antirreplay, respaldo y publicación controlada | V4.7.0/1/2 **en repo** (V4.7.2 solo modelo sin WebAuthn), apply OFF | Implementar y validar WebAuthn real, antirreplay persistente y rollback seguro antes de proponer apply |
| **C. Instalación Pack limpio** | Backup preinstalación, conservar built-in + solo personalizaciones VX; preservar MCP, proponer faltantes | Pack V0.2 con bootstrap DPAPI e instalador incremental en código, CI aislada; HOME sin migrar | Inventario seguro, backup verificable, catálogo MCP, compatibilidad y DRY_RUN |
| **D. Equipo desarrollador IA** | Siete agentes originales con alias + cinco builders VX, especialidades, grafo y roles | 12 agentes VX en código, STRICT vigente, Agent Manager paralelo no habilitado | Probar delegación Kilo, piloto multi-escritor con worktrees y autorización nueva |
| **E. VX Academy + evolución medible** | Capacitaciones mínimas por tarea, experiencia, enseñanza, evaluaciones, especialización y departamentos | VX-D22 **diseño solicitado**; V4.8–V5.0 **no implementadas** | Validar selección de skills, medir pruebas ciegas, impedir autoenseñanza/autoascenso y evaluar costes |

### Distinción esencial de entregables

- **Repositorio ≠ instalación global:** el instalador `scripts/Instalar-Kilo-Global-Harness.ps1` sigue declarando V4.6.x y **no instala** `vx_publish_preview.py` ni `vx_approval_contract.py`. V4.7.0/1 se integraron en `main`, no deben presentarse como módulos ya desplegados en Kilo del operador. El Pack final necesita reconciliar código, manifiesto/installer, pruebas y compatibilidad antes de una migración autorizada.
- **Alcance C y colaboración:** VX solo gobierna sus **propios agentes y skills**. El equipo VX puede trabajar en repositorios de software **asignados expresamente por el usuario**, sin asumir control de los agentes/skills de esos otros proyectos. Inventario/backup externo únicamente como parte delimitada de la migración.
- **Nombres y rango:** los siete alias originales están **confirmados** y el pack amplía a 12 agentes en código, todavía no cargados en Kilo real; personalidad, puesto y `SIN_EVALUAR` no crean ni amplían permisos.
- **Concurrencia:** STRICT sigue por defecto, una sola rama temporal/escritor. El objetivo `PARALLEL_WORKTREES` exige autorización para varias ramas temporales simultáneas, worktrees y tareas disjuntas; **main continúa como única permanente**. Los seis revisores VX siguen en modo solo lectura; los cinco builders solicitan aprobación de edición y se usan de forma interactiva, no como subagentes autónomos.
- **Seguridad:** scheduler OFF; no activar `apply`, migración, login MCP, publicación, AutoApprove ni cambios a HOME por documentar estas fases.

### V4.8 — Nueva capa formativa propuesta (VX Academy)

**VX-D22 — OBJETIVO SOLICITADO; CONTRATOS Y CATÁLOGO DE DISEÑO, NO IMPLEMENTADOS.** Asignar capacidades y herramientas por agente, equipo y departamento para no sobrecargar el contexto ni otorgar permisos innecesarios. Separar **competencia declarada, skill instalada, uso observado, resultado evaluado y permiso efectivo**. En el registro declarativo existen 22 capacidades curriculares propuestas para siete agentes, dos skills VX existentes al redactar la propuesta del 15 de noviembre; el Pack V0.2 posterior incorpora 30 skills VX originales en código y ninguna habilidad externa se instala automáticamente. La experiencia/enseñanza verificadas comienzan con cero eventos; no inferir niveles. Enseñanza y promoción exigen pruebas independientes antes/después, revisor separado y aprobación; **ninguna docencia concede herramientas ni escritura al aprendiz**. La selección de hasta tres skills principales por tarea existe como recomendación del router V0.2, NO es una ACL ni un límite exigido por Kilo; Kilo comparte catálogo de metadatos y carga instrucciones completas bajo demanda, sin aislamiento automático por agente. [Diseño de capacitación](VX-ACADEMY-CAPACITACION-V1-20261115.md) · [Catálogo inactivo](../registry/vx-academy-catalog-v1.proposal.json).

### VX Academy — segunda capa: mentoría y aprendizaje transferible (VX-D23)

**DISEÑO PROPUESTO, NO ACTIVO.** El usuario pidió continuar sobre [VX-D22](VX-ACADEMY-CAPACITACION-V1-20261115.md) con un sistema capaz de distinguir **especialista, mentor, evaluador y supervisor** y demostrar aprendizaje/enseñanza mediante escenarios nuevos, evidencia independiente, control de regresiones y catálogo de experiencia. El ciclo propuesto tiene ocho puertas G0–G7 y empieza sin ningún mentor certificado ni evaluaciones reales: si no hay mentor acreditado, se utiliza material auditado de manera controlada, **sin inventar título docente**. Un resultado positivo no modifica permisos ni vuelve a nadie jefe. Nuevos equipos y departamentos solo cuando el beneficio organizativo sea demostrado y exista aprobación explícita. `main` permanece la única rama permanente; scheduler, publicaciones y autoformación siguen OFF.

**Fases futuras sugeridas, todavía no aprobadas como versiones:** V4.8.0 evaluación independiente y fuente de evidencia; V4.8.1 catálogo mínimo por tarea; V4.8.2 protocolos de aprendizaje/mentoría en HOME sintético; V4.9 evaluación comparada de transferencia y organización; V5.0 promociones/equipos escalables con control humano. El orden indica dependencias, no lanzamientos ni permiso de implementación.

Documentos: [Mentoría y evaluación](VX-ACADEMY-MENTORIA-EVOLUCION-V1-20261115.md) · [Contrato no ejecutable](../registry/vx-academy-mentorship-v1.proposal.json). **No aplicar en perfil global hasta resolver seguridad de V4.7, backup y permisos.**

### V4.8.0 — Evaluador independiente VX Academy (VX-D24; siguiente desarrollo propuesto)

**Propuesta registrada, NO IMPLEMENTADA.** Antes de afirmar aprendizaje, competencias, docencia o seniority, se requiere una fuente de evidencia independiente de lo que dicen los agentes: **suite versionada + runner observable en entorno aislado + holdout no expuesto + comparación de baseline y candidato + regresiones + revisor independiente + resolución humana**. El evaluador debe distinguir `DECLARED`, `RUNNER_VERIFIED`, `INDEPENDENTLY_REVIEWED` y `NO_MEDIDO`. Un hash no valida por sí mismo la veracidad de logs locales, y la V4.7.2 integrada a nivel de contratos sigue sin criptografía/autenticación WebAuthn real.

El primer piloto propuesto es una competencia de Rafael (`qa.negative-cases`) en fixtures sintéticos, sin mentor certificado ni evaluación ejecutada. El [documento del evaluador](VX-ACADEMY-EVALUADOR-INDEPENDIENTE-V1-20261115.md) y su [esquema no ejecutable](../registry/vx-academy-independent-evaluator-v1.proposal.json) fijan las puertas E0–E7, el modelo de registros y sus límites. **Cero runs, cero certificados, cero cambios de permisos.** V4.8.1 runner, V4.8.2 comparación A/B, V4.9 transferencia y V5.0 evolución organizativa siguen siendo fases futuras condicionadas a seguridad V4.7, aislamiento y autorización.

### Qué falta decidir antes de la siguiente construcción

**D1 — Catálogo MCP:** servicios exactos del Pack, obligatorios vs opcionales/perfiles, origen/licencias, compatibilidad y cada aprobación individual. **D2 — Copias:** método de cifrado y recuperación local en Windows, pruebas de integridad SQLite, ruta privada, conservación posterior; ninguna eliminación automática aprobada. **D3 — Distribución:** ZIP/PowerShell/CLI, instalación desde cero y migración desde V4, versionado y compatibilidad Kilo. **D4 — Actualizaciones:** comprobación manual vs notificación/observación automatizada (actual scheduler OFF), canales, pin y plan de reversión. **D5 — Equipo:** prueba de identidad del subagente, selección y permisos por herramienta, piloto aislado de dos escritores, contratos de comunicación. **D6 — Evolución, mentoría, evaluador VX Academy:** decidir fuente y aislamiento de runner, holdout no expuesto, revisión independiente, capacidades por tarea, límites de skills, transferencia y coste, retención de experiencia, ascensos y departamentos. VX-D24 propone contratos de evaluación; ninguna ejecución ni certificado al inicio.

**El próximo tema aportado por el operador debe registrarse como una nueva decisión o revisión de estas puertas, sin ejecutarse por el mero hecho de definirlo.**

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
| V4.7.1 | Contrato estructural de solicitud y aserción de aprobación | **Integrado en main** (PR #26, `d7f954c6`); CI Windows PASS | Pruebas aisladas; sin ejecución en HOME real | `approval_granted=false`; `apply_supported=false` | 
| V4.7.2 | Controles de seguridad de aprobación | **PR #29 abierta** (`64ce0e74`), CI Windows PASS; no integrada | Solo pruebas aisladas, según PR | No declarar autenticación real ni publicaciones habilitadas por una CI verde | 
| V4.7.3+ | Backup/restauración, autenticación gobernada e instalación controlada | **Diseño futuro**, numeración interna provisional | No aplica | Condicionada a aislamiento, aprobación y rollback real | 
| Pack VX Bootstrap | Distribución inicial limpia con respaldo, catálogo MCP y componentes VX | **PR #28 documental**, no implementado | Sin prueba de instalación integral en Kilo real | No modifica ni desactiva agentes, skills o MCP activos |
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
| VX-D15 | **Pack integral definido parcialmente** | Instalación limpia y política de backup confirmadas; faltan catálogo MCP y mecanismo de cifrado/recuperación/retención, distribución y actualización. |
| VX-D16 | **CONFIRMADO: instalación limpia objetivo** | Estado final global: built-in Kilo + agentes/skills/comandos/reglas propios VX activos; externos personalizados anteriores respaldados y archivados fuera de descubrimiento, sin borrado irreversible. No autoriza migración real. |
| VX-D17 | **CONFIRMADO: conservar MCP y añadir faltantes solo con autorización individual** | Una migración limpia no toca MCP actuales ni credenciales; catálogo VX detecta candidatos ausentes y solicita aprobación por servidor antes de instalar/configurar. |
| VX-D18 | **CONFIRMADO: respaldo Kilo previo, protegido y verificable** | Backup local íntegro de configuración/datos afectados, cifrar material sensible, detener ante fallo y conservar copia anterior hasta validación final; aún sin ejecutar. |
| VX-D19 | **CONFIRMADO: siete agentes IA con alias humanos** | Yoan, Daniela, Rafael, Sofía, Valentina, Lucas y Mateo; IDs `vx-*` estables, sin modificación de agentes/permisos activos. |
| VX-D20 | **CONFIRMADO: objetivo de desarrollo paralelo real** | Modo `PARALLEL_WORKTREES` futuro con múltiples escritores aislados por rama/worktree, contratos e integración; requiere autorización especial, pruebas y verificación del runtime. STRICT actual sin cambios. |
| VX-D21 | **CONFIRMADO: crecimiento de equipos y departamentos por evidencias** | Versiones de persona y capacidad, niveles SIN_EVALUAR al inicio, promociones y nuevos nodos/gerencias solo con evaluación real y consentimiento; org `reports_to` sin ciclos. |
| VX-D22 | **OBJETIVO REGISTRADO: catálogo de capacitación selectiva** | Skills/herramientas mínimas por agente, tarea y equipo; competencias declaradas no certificadas, sin permisos añadidos. |
| VX-D23 | **PROPUESTA: mentoría, transferencia y promoción demostradas** | Docente ≠ evaluador ≠ supervisor; sin certificados iniciales; evaluación independiente y autorización humana; no ejecutar. |
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

**P3.1 V4.7.1 — INTEGRADO EN MAIN** — PR #26 fusionada por squash con commit `d7f954c6d6b6cf237594b27e2a6a69734a4df4b8`; CI Windows posterior al merge PASS (run 43730455042). Contrato de solicitud/aserción estructural, sin autenticación, firma, anti-replay ni capacidad de aplicar. `approval_granted=false` y `apply_supported=false`. Deben mantenerse estas restricciones hasta desarrollo y autorización de una fase posterior.

**P3.2 CORRECCIÓN TTY — INTEGRADA EN MAIN** — PR #27 fusionada con commit `11b4869589dcb34a9d4aa74e01ce945f2b879e22`; Windows CI posterior al merge PASS (run 43731726923). Los dos fixtures heredados fijan `stdin=subprocess.PIPE` por el comportamiento de Windows NUL (`DEVNULL` falló en run anterior). No cambia `local_confirmation()` ni los permisos. La prueba completa local interactiva debe repetirse en Windows del operador tras CI y merge. [Alcance y verificación](VX-REPRODUCIBILIDAD-TTY-V4.7.1.md).

**P4 V4.7.2 — DESARROLLO CON PR #29 ABIERTA (NO MERGE)** — El agente preparó contratos de seguridad de aprobaciones en rama `work/v4-7-2-approval-security`, commit `64ce0e74313199c33f6cc0f519dd5173cb5a712d`; CI Windows PASS. Quedan revisión independiente del código, requisitos de autenticación confiable y decisión de integración. Analizar separación de funciones/antirreplay en pruebas aisladas. No exponer `apply` ni permitir aprobaciones activas sin un mecanismo autenticado, respaldos y autorización explícita.

**P5 NUEVA ÉPICA: PACK VX BOOTSTRAP GLOBAL (SIN IMPLEMENTAR)** — Decisión C confirmada: VX gobierna únicamente componentes VX propios. El operador confirmó el destino limpio (VX-D16): conservar agentes nativos de Kilo y activar solo personalizaciones del Pack VX; los agentes/skills personalizados anteriores se conservarán respaldados fuera de las rutas de descubrimiento una vez autorizada la migración. Pack inicial versionado con agentes/skills/comandos VX, respaldo preinstalación verificable, inventario/comparación de MCP y soporte de actualización reversible. La configuración MCP se decide por separado. No confundir backup total, instalador actual que solo respalda destinos administrados, ni lista de MCP con conectividad real. La política MCP quedó confirmada en VX-D17: conservar todos los existentes y proponer cada faltante para aprobación individual. Se aprobó VX-D18: respaldo local íntegro y verificado antes de migración, permisos restrictivos y cifrado de material sensible; conservar una copia anterior hasta validar instalación. Falta elegir tecnología de protección y definir retención posterior. Siguen pendientes la composición del catálogo MCP (núcleo y perfiles), distribución y política de actualizaciones. La desactivación de terceros durante el bootstrap requiere un plan exacto y autorización excepcional distinta de la opción C; no es administración continua. [Acta alcance C y preguntas](VX-ALCANCE-C-PACK-BOOTSTRAP-20261115.md). **No instalar ni modificar Kilo hasta aprobación del diseño.**

**P5.1 EQUIPO VX CON SIETE ALIAS CONFIRMADOS (SIN CAMBIOS ACTIVOS)** — El operador confirmó Yoan (`vx-integrador`), Daniela (`vx-frontend-adviser`), Rafael (`vx-test-analyst`), Sofía (`vx-researcher`), Valentina (`vx-security-reviewer`), Lucas (`vx-inspector`) y Mateo (`vx-workers-adviser`). **Todos los subagentes actuales siguen de solo lectura**. Se diseñó `registry/vx-organization-graph-v1.proposal.json` (inactivo) y matriz de permisos A0–A4. [Equipo](VX-EQUIPO-INICIAL-PACK-20261115.md) · [Personas](VX-PERSONAS-RELACIONES-V1-20261115.md) · [Autonomía](VX-PERMISOS-Y-AUTONOMIA-V1-20261115.md).

**P5.2 PARALELISMO REAL MULTI-ESCRITOR (OBJETIVO CONFIRMADO, NO HABILITADO)** — Mantener STRICT actual (una rama/escritor) hasta ensayos. Luego, con permiso explícito, usar Agent Manager con worktrees aislados y ramas temporales por línea, Kilo nativo `code` como escritores iniciales y especialistas VX lectores; después promover implementadores VX solo por versión/permisos probados. Máximo inicial propuesto 2 escritores en worktrees disjuntos; `main` única rama permanente. Intercambio por contratos de tareas/versiones, no asumir Swarm cross-session; tests/PR/merge secuenciados por DAG y revisión independiente. **Permisos actuales y scheduler intactos.**

**P5.3 ORGANIZACIÓN EVOLUTIVA (FUTURA, SIN ASCENSOS ACTIVOS)** — Registrar nivel SIN_EVALUAR y cambios de persona/competencias/permisos como versiones separadas. Evaluaciones reales V4.8 antes de proponer nuevos agentes, subordinados o departamentos. La estructura administrativa y el grafo de dependencias deben ser acíclicos; las colaboraciones cruzadas sí pueden repetirse. Ninguna promoción concede permisos, capacidad de publicar o aprobar.

Se considera **finalizada la planificación** cuando este documento, el README y el registro de decisiones describen las mismas fases y se validan los invariantes en CI. Ningún cambio de runtime en V4.6 se autoriza con solo publicar este roadmap.
