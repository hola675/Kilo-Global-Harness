# VX Evolution — Decisiones y dudas de dirección

**Fecha de registro:** 2026-11-14. **Ámbito:** exclusivamente Kilo Code, todos los proyectos, almacenamiento operativo global en HOME. Esta tabla separa decisiones expresadas por el usuario de propuestas técnicas que todavía necesitan aprobación.

| ID | Decisión / duda | Estado | Propuesta y efecto |
| --- | --- | --- | --- |
| VX-D01 | Solo Kilo Code; no Codex, Claude ni otros harnesses | **CONFIRMADA** | Comandos, skills, APIs y hooks únicamente globales de Kilo |
| VX-D02 | Memoria/registro de trabajo independiente del repositorio | **CONFIRMADA** | SQLite en HOME; referencias a proyectos seudónimas, nunca bases por proyecto |
| VX-D03 | Reunión semanal y cierre mensual global | **CONFIRMADA; MANUAL IMPLEMENTADO** | V4.5.1 permite una sesión conjunta el primer lunes con dos secciones, y lunes ordinarios semanales. Sin tareas automáticas |
| VX-D04 | En las reuniones el usuario revisa y aprueba propuestas | **CONFIRMADA; PARCIALMENTE IMPLEMENTADO** | Desde V4.5 hay decisiones manuales por terminal TTY, identidad no verificada; nunca publicación de agentes/skills |
| VX-D05 | Día/hora y zona horaria de reunión semanal | **CONFIRMADA, NO PROGRAMADA** | Lunes a las 09:00, horario local del equipo Windows (`system_local`). No programar ni notificar hasta recibir nueva aprobación expresa posterior a V4.5.1 y prueba local. Política de diseño: `config/vx-reunion-policy.v1.json` |
| VX-D06 | Cierre mensual y coincidencia con semanal | **CONFIRMADA, NO PROGRAMADA** | Primer lunes del mes siguiente a las 09:00 hora local Windows; **una sola sesión** con sección mensual y sección semanal, en ese orden. Scheduler apagado hasta nueva autorización expresa |
| VX-D07 | Política de retención y borrado | **PENDIENTE** | Propuesta: observaciones detalladas 90 días, agregados y decisiones con histórico versionado; no borrar nada hasta definir |
| VX-D08 | Única PC Windows o varias instalaciones Kilo | **CONFIRMADA: SOLO ESTE PC WINDOWS** | Mantener SQLite y las reglas Kilo únicamente en el perfil HOME local; **sin sincronización, base remota ni clientes múltiples** |
| VX-D09 | Captura ligera de eventos Kilo y nivel de detalle | **IMPLEMENTADA PARCIALMENTE, OPT-IN** | V4.4: plugin global opcional, apagado por defecto; solo contadores horarios de idle/error/compacted sin payload. La captura real de resultados, correcciones y calidad de tareas sigue pendiente y requerirá revisión de privacidad |
| VX-D10 | Identidad y mecanismo para registrar aprobación | **IMPLEMENTACIÓN PARCIAL, IDENTIDAD NO VERIFICADA** | V4.5: TTY no autentica. V4.7.1 integra solo el contrato estructural; no otorga autorización. V4.7.2 diseña seguridad WebAuthn/FIDO2 y pruebas aisladas; no activa aprobaciones |
| VX-D11 | Condiciones para ascenso, contratación, fusión y jubilación de agentes | **PENDIENTE** | Métricas reales, auditor independiente, evaluación negativa y rollback |
| VX-D12 | Reconciliar 11 agentes compartidos y 19 limites steps altos | **PENDIENTE DE EJECUCIÓN** | Mantener auditor V4.2 como pista paralela sin modificar configuración privada |

## Política semanal acordada

- Reunión VX global: **cada lunes a las 09:00**.
- Zona horaria: **la configurada en Windows en el equipo al momento de ejecutar**; no fijar Europe/Madrid, zona geográfica o desplazamiento UTC, y respetar el cambio estacional que aplique Windows.
- **V4.5.1 implementada en código, CI y verificada localmente el 2026-11-14**: SQLite v4, integridad OK, evento Observer `light` conservado, calendario conjunto 2026-12-07 09:00, una sesión con dos secciones; **no** se crean tareas programadas, avisos ni reuniones automáticas. V4.3 tenía calendario por periodos UTC, pero el planificador vigente ya utiliza fechas locales.
- **Cierre mensual VX-D06:** primer lunes del mes siguiente a las 09:00, mes anterior completo, primera sección de una sesión conjunta. No programar nada.
- **Coincidencia en primer lunes:** confirmada **una única sesión con dos secciones independientes** (mensual y semanal). No duplicar convocatoria ni aprobar por silencio.

## Límite confirmado de Observer V4.4

- El plugin no se instala por defecto; requiere `-InstalarVXObserverV44`. Instalarlo no activa captura.
- Los contadores solo se habilitan mediante `observer-mode --mode light` sobre SQLite v2; se apagan con `observer-mode --mode off`.
- Los eventos no prueban calidad, tarea completada, capacitación ni fallos de código. No generan propuestas ni promociones.
- Lunes 09:00 hora local Windows sigue **sin scheduler**; V4.5.1 permite actas manuales, pero la automatización no está habilitada.

## Invariantes confirmados

1. Una sola rama temporal de trabajo y `main` permanente.
2. Configuraciones Kilo/skills/agents y datos operativos exclusivamente en HOME.
3. AutoApprove no se cambia; no implica conceder más permisos.
4. Los agentes no aprueban ni publican sus propios cambios.
5. Evidencia y revisión previa a modificar skills, agentes, dependencias o jerarquías.
6. No usar documentación externa no auditada como instrucciones ejecutables ni almacenar secretos/proyectos privados en GitHub.

## Alcance histórico de V4.3 frente a fases posteriores (no estado actual)

**Implementado en el código fuente:** SQLite schema v1, inventario Kilo global, observaciones explícitas, propuestas `pending_review`, hashes, backup manual, agenda `meeting-preview`, comandos y skill de gobierno, test Windows.

**Pendiente:** instrumentación automática de todas las tareas (V4.4), calendario/notificaciones y decisiones persistidas (V4.5), evaluación/autocapacitación y jerarquías (V4.6), publicación versionada y rollback de componentes (V4.7).

No confundir una tabla vacía `meetings` o `decisions` con una función de reuniones ejecutada. El motor V4.3 no debe arrancar servicios residentes sin autorización.

## Política de revisión

VX-D05 y VX-D06 están confirmadas; la activación del programador **continúa sin autorizarse**. Antes de V4.6 recopilar información sobre VX-D07 (retención), VX-D08 (si se usarán varias PCs) y VX-D11 (criterios de ascenso); no inventar ninguna respuesta. VX-D10 tiene control TTY no autenticado, insuficiente para publicaciones de V4.7. No bloquear las herramientas de solo lectura, pero no hacer cambios organizativos sensibles por defecto.

## Riesgos que revisaremos de nuevo

- Captura de información de proyectos, datos personales y secretos.
- Duplicación de observaciones de subagentes; familias semánticas aún no implementadas.
- Acoplamiento con hooks o plugins existentes de Kilo, incluidos task-observer y descubrimiento de modelos.
- Calidad de métricas cuando Kilo no reporte tokens/costo.
- Corrupción SQLite, apagones, migraciones y backups.
- Sesgos en evaluaciones que podrían promocionar agentes mediocres o retirar especialistas útiles.


## Decisión adicional de V4.5: funcionamiento manual sin scheduler

Se autoriza **implementar y probar** el módulo de reuniones. La activación de cualquier tarea recurrente, notificación o automatización requiere aprobación expresa **posterior**; confirmar día u hora no equivale a activarla. Las decisiones registradas en actas no constituyen autorización técnica de despliegue de agentes/skills. Consultar [VX Reunión V4.5](VX-REUNION-V4.5.md).

## V4.5.1 — Decisión de sesión conjunta

Se confirma lunes a las **09:00 hora local de Windows**, primer lunes del mes siguiente como cierre del mes anterior, **una sola sesión** y **dos secciones** dentro del acta: cierre mensual primero, seguimiento semanal después. En SQLite v4 se implementa como una sesión vinculada a dos secciones, sin duplicación de propuestas; requiere `joint-migrate` explícito con respaldo desde esquema v3. Todas las tareas programadas y notificaciones permanecen desactivadas. El operador deberá autorizar de nuevo cualquier activación futura.

## Actualización del roadmap: V4.6

**Decisión de ejecución pendiente:** próxima fase técnica es **V4.6.0 — línea base de agentes y skills globales Kilo, solo lectura**; después V4.6.1 matriz de capacidades, V4.6.2 capacitación evaluable, V4.6.3 auditoría de organización. Ninguna propuesta se materializará en agentes, permisos, jefaturas, skills activas, MCP o versiones. Se exige un evaluador independiente y prueba reproducible antes de proponer ascensos. Fuente vigente: [Roadmap VX Evolution](VX-EVOLUTION-ROADMAP.md).

**Puerta de validación V4.5.1 completada con evidencia local:** el usuario instaló y verificó SQLite schema v4, integridad OK, `joint_sessions_supported=true`, Observer `light` y calendario conjunto (2026-12-07, 09:00, 1 sesión, 2 secciones). El registro global indicó 79 fuentes inventariadas. Mantener programación semanal y mensual desactivada.

## VX-D08 confirmada y avance V4.6.0

El usuario confirmó que VX Evolution se usará **únicamente en este PC Windows**. Quedan fuera de alcance las bases compartidas, sincronización, cloud y despliegues multi-PC. V4.6.0 incorpora una auditoría global **de solo lectura** que identifica agentes/skills declarados y diferencias de fuentes, sin escribir SQLite, modificar permisos ni calificar capacidades no evaluadas. Pruebas locales de esta nueva herramienta pendientes; guía [VX Capacidades V4.6.0](VX-CAPACIDADES-V4.6.0.md).


## V4.6.1 — Límite de las evidencias (sin nueva autorización)

La V4.6.0 ya fue integrada en `main` y superó CI Windows; su ejecución real en Kilo permanece pendiente. Se implementa V4.6.1 como **matriz de capacidades declaradas y evidencias opcionales también declaradas**, sin asignar rangos, puntuación, permisos ni jerarquías. Incluso un resultado `PASS` con `review_source=other` no acredita revisión independiente: necesita verificación técnica y humana posterior. No se modifica ninguna decisión VX-D01–VX-D12 ni se autoriza activación de programador o reuniones. [Guía V4.6.1](VX-MATRIZ-COMPETENCIAS-V4.6.1.md).


## Validación local V4.6.0–V4.6.1 y avance de ensayos V4.6.2

El usuario ejecutó en este Windows el 14-11-2026 la instalación de V4.6.1 (`Simular`, `Aplicar`, `Verificar`), auditoría de capacidades y matriz global; el CLI devolvió PASS. Se observaron 39 fuentes de agente/28 agentes, 40 skills, 11 agentes superpuestos JSONC/Markdown, 19 límites `steps > 400`, 76 filas de matriz, 15 capacidades declaradas y cero evidencias. Git quedó actualizado y se eliminó la rama temporal remota V4.6.1; `main` es la única rama permanente. Aún falta prueba interactiva dentro de Kilo luego de `/reload`; no registrar precedencia efectiva, competencia o seniority sin pruebas independientes.

V4.6.2 implementa **solo escenarios sintéticos no ciegos y un comparador declarativo, sin ejecución autónoma ni puntuación real**. La revisión de una brecha de evidencia no equivale a fallo de un agente. No hay autorización para escribir propuestas SQLite, instalar habilidades, activar tareas programadas, ascender o contratar. [Guía V4.6.2](VX-ENSAYOS-COMPETENCIAS-V4.6.2.md).


## Cierre de CLI V4.6.2 — bloqueo legítimo de herramientas

El 2026-11-14 el operador ejecutó en PowerShell 7 `python -I $trial` y `python -I $trial --list-cases` en el Windows designado, con 5 casos sintéticos y 5 objetivos presentes en la matriz; 0 respuestas y 0 coincidencias antes/después. Rendimiento `NO_MEDIDO`, formación `NO_VERIFICADO`. En Kilo, la invocación de PowerShell fue **bloqueada por política**; no se eludió ni modificó. La presencia del comando `/vx-ensayos` y la ejecución local del CLI no prueban ejecución de `vx-inspector`, `vx-test-analyst` ni de la skill. No ampliar AutoApprove, permisos o scheduler por este hecho. La siguiente prueba será manual, sin herramientas, con revisión independiente. [Evidencia operativa](VX-VALIDACION-CLI-V4.6.2-20261114.md).


## Batería conversacional V4.6.2 completada: cinco respuestas, competencia NO_MEDIDO

El usuario compartió respuestas de Kilo para los cinco casos `v462-review-unsafe`, `v462-review-guarded`, `v462-precedence`, `v462-skill-observer` y `v462-regression-gap`. Los cinco pares de decisión/razón coinciden con sus fixtures públicos; una retransmisión idéntica de `v462-review-guarded` se deduplicó. Kilo declara delegaciones a `vx-inspector` y `vx-test-analyst`, y uso de la skill `vx-evolution-core`; estas identidades no se comprobaron contra registros independientes. Referencias internas completas de sesiones NO publicadas en GitHub. La coincidencia 5/5 no supone competencia verificada ni prueba de mejora; no existen resultados ciegos, comparación anterior/posterior ni autorización de ascensos o cambios. [Cierre de la batería](VX-CIERRE-BATERIA-V4.6.2-20261114.md). V4.6.3 queda **pendiente** como auditoría de procedencia, solapamientos y riesgos con análisis solo lectura.


## VX V4.6.3 — Auditoría de organización por metadatos, solo lectura

Se prepara un auditor que reutiliza inventario V4.6.0 y matriz V4.6.1 para separar solapamientos declarados de colisiones efectivas, diferencias explícitas frente a precedencia real y límites steps frente a desempeño/seguridad. La batería V4.6.2 terminó con cinco respuestas coincidentes **no ciegas**, pero las delegaciones no tienen trazabilidad verificada; `session_logs_read=false` y `delegation_provenance_verified=false`. `/vx-organizacion` no ejecuta modelos, no lee logs Kilo ni escribe propuestas SQLite; sin cambios de configuración global, AutoApprove, skills, MCP, permisos, tareas programadas o jerarquías. Este diseño no modifica decisiones confirmadas. [Guía V4.6.3](VX-AUDITORIA-ORGANIZATIVA-V4.6.3.md).

### Cierre local de diagnóstico V4.6.3

El operador ejecutó instalación Simular/Aplicar/Verificar y `vx_organizational_audit.py` desde PowerShell 7.6.8 en el PC Windows designado; CLI PASS. Se identificaron 11 coincidencias de nombre JSONC/Markdown sin diferencias explícitas en campos comparados, 19 entradas steps mayores de 400, cero skills repetidas, cero skills de perfil no observadas y cero declaraciones de router sin agente observado: 30 hallazgos para inspección humana. La simulación también informó 6 definiciones JSONC con edit/bash `allow`, sin demostrar alcance efectivo ni autorización para cambiar permisos. La rama temporal V4.6.3 fue eliminada; solo origin/main permanece. Fuente: [acta de validación Windows](VX-VALIDACION-LOCAL-V4.6.3-20261114.md). Aún falta determinar precedencia real y procedencia de delegaciones. Los resultados no justifican fusión, retiro, promoción, habilitación del scheduler o modificación de configuraciones.

### Revisión complementaria V4.6.3 de límites y precedencia

El operador enumeró los once agentes con fuentes JSONC/Markdown superpuestas. Después completó las **19 de 19 definiciones con steps superiores a 400**: todas declaran `steps = 10000000` en `kilo-agent-jsonc`; no hay otros valores elevados en esta muestra. La [documentación oficial Kilo](https://kilo.ai/docs/customize/custom-modes) define steps como rondas de llamadas a herramientas hasta forzar texto, y explica fusión y precedencia de configuración. La regla documentada **no prueba** prioridad efectiva en la sesión instalada ni que se hayan consumido millones de rondas. Los cambios de límites y permisos requieren autorización separada y evaluación funcional. [Acta de observaciones](VX-REVISION-STEPS-PRECEDENCIA-V4.6.3-20261114.md).


### Comprobación declarada en interfaz Kilo de dos agentes (V4.6.3)

El operador verificó manualmente **Pasos máximos = 10000000** en los editores visuales de `architect` y `code-reviewer`. Los dos valores coinciden con las declaraciones `kilo-agent-jsonc` ya inventariadas. Esto incrementa la evidencia del valor **mostrado**, pero no demuestra la procedencia efectiva de la combinación JSONC/Markdown ni que Kilo aplique ese límite en una sesión. Sin cambios de archivos, políticas, AutoApprove, agentes ni scheduler. La siguiente prueba será comparar únicamente metadatos de ambas fuentes en V4.6.0 y, si hace falta, revisar de forma manual el comportamiento autorizado de Kilo, nunca mediante una reconfiguración de prueba. [Registro de evidencias](VX-REVISION-STEPS-PRECEDENCIA-V4.6.3-20261114.md).

## V4.7.0 — fase inicial de preview solamente

V4.7.0 integrado en `main` mediante `36a73e01fe46d17573f46baf82cf8c88bf5d7559`; define `vx-component-manifest/1` con SemVer, SHA-256, dependencias y estados, y solo construye informes `DRY_RUN` con HOME sintético. V4.7.1 integrado en `main` mediante `11b4869589dcb34a9d4aa74e01ce945f2b879e22`; define solicitudes y aserciones estructurales ligadas a hashes/scope, pero la respuesta sigue `AUTH_UNVERIFIED`, `approval_granted=false` y `apply_supported=false`. Sin instalación ni cambios en HOME real. [Contrato de publicación V4.7](VX-PUBLICACION-GOBERNADA-V4.7.md) · [Contrato de solicitud V4.7.1](VX-APROBACION-GOBERNADA-V4.7.1.md).

## V4.7.2 — propuesta de seguridad, solo contratos/pruebas aisladas

**No es una decisión operativa ni una aprobación activa.** Alternativas comparadas: WebAuthn/FIDO2 por Windows WebAuthn API (recomendado para prototipar: challenge ligado al request/plan, firma de clave pública, user verification y RP ID/origin); clave CNG/TPM (protege clave, pero la llamada directa no garantiza gesto/consentimiento por operación); DPAPI/Credential Manager (protegen secretos en reposo, no autentican aprobador); y TTY/contraseña escrita (no satisfacen identidad ni vínculo criptográfico). La API de Windows documenta Windows Hello platform authenticator y llaves FIDO2; no se asume disponible ni enrolada en este PC. El inicio de sesión Windows Hello de una cuenta local no se considera una credencial WebAuthn ni prueba de aprobación.

V4.7.2 requiere identidad enlazada a credencial registrada bajo un RP/origin fijo, user verification requerida, autor y aprobador distintos, challenge/digest canónico, consumo durable/atómico, revocación con historial y auditoría mínima. La fase actual solo define estructuras y transiciones de modelo en memoria; no ejecuta WebAuthn, no crea claves ni persistencia, no registra identidades y mantiene `approval_granted=false` / `apply_supported=false`. Una sola PC no permite asumir independencia de personas; el compromiso del perfil/admin local y la manipulación del reloj/log siguen siendo riesgos residuales. DPAPI no se usará como sustituto de autenticación. Referencias: [Windows WebAuthn API](https://learn.microsoft.com/windows/win32/webauthn/-webauthn-portal), [Hello for Business](https://learn.microsoft.com/windows/security/identity-protection/hello-for-business/), [DPAPI](https://learn.microsoft.com/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata), [Credential handling](https://learn.microsoft.com/windows/win32/secbp/handling-passwords). [Diseño V4.7.2](VX-APROBACION-SEGURIDAD-V4.7.2.md).


### VX-D13 — Evidencia Desktop y próxima fase V4.7 (registro sin cambio activo)

Se recibió el inventario visual de Kilo Desktop con los siete agentes VX en `All workspaces`, junto a las skills VX `vx-engineering-harness` y `vx-evolution-core`. Una prueba nueva ejecutó `task` hacia `vx-inspector` y reportó la sesión hija `completed`; no se obtuvo metadato independiente del ejecutor ni llamada interna observable `skill`. Por ello, el uso de la skill permanece `DECLARADO` y su invocación `NO_VERIFICADO`, no se etiqueta como error. Las tres tareas sintéticas A/B/C previas tuvieron resultados correctos y tres delegaciones visibles, sin evaluación ciega ni calidad medida.

**Decisión conservadora:** no repetir las mismas pruebas sin nueva evidencia, no cambiar límites `steps`, permisos, agentes o skills activos. Diseñar V4.7 con manifiestos versionados, simulación, CI en HOME aislado, aprobación expresa vinculada al hash y rollback; cualquier aplicación al HOME Windows requiere autorización específica. Cuatro MCP Cloudflare marcados `Needs sign-in` no bloquean el alcance de VX. [Acta y puerta V4.7](VX-DESKTOP-VALIDACION-Y-PUERTA-V4.7-20261114.md).
