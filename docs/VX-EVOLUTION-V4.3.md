# VX Evolution Core V4.3 — Contrato de arquitectura (SOLO Kilo Code)

> **Documento histórico de la fase V4.3.** Conserva el alcance y pendientes originales de esa versión; para estado real V4.5.1, validación local y próximos hitos V4.6–V5, consultar el [roadmap maestro](VX-EVOLUTION-ROADMAP.md). No interpretar sus referencias a V4.4/V4.5 «futuras» como estado del código actual.

**Estado de esta versión:** núcleo local con CLI y esquema SQLite, sin observador activo, sin automatizaciones semanales y sin aprobación automática. Este documento define hechos implementados, restricciones y fases futuras de forma diferenciada.

## Decisiones fundacionales

1. **Solo Kilo Code:** los comandos, agentes, skills y futuras integraciones usan las rutas y APIs globales de Kilo. No registrar plugins, reglas ni hooks para Codex, Claude u otros clientes. Los nombres de rutas `.agents/skills` y `.kilocode/skills` se inventarían únicamente porque **Kilo** los admite como compatibilidad.
2. **Global-only:** datos operativos bajo `%USERPROFILE%\.config\kilo\vx-evolution\`. El repositorio GitHub contiene solo el código, pruebas y documentos, nunca la base operativa, observaciones ni configuraciones privadas de Windows.
3. **Motor único:** seis responsabilidades con un solo registro, no seis bases independientes. `vx-equipo` = coordinación; `vx-observer` = observaciones; `vx-capacitacion` = mejora de skills; `vx-auditoria-equipo` = evaluación de roles; `vx-upgrade` = candidatos y versiones; `vx-reunion` = propuestas semanales/mensuales.
4. **No autopromoción:** un agente puede sugerir mejoras pero no aprobar sus propias promociones, cambiar permisos ni activar nuevas versiones unilateralmente. Las aprobaciones humanas requerirán identidad y evidencia, definidos antes de implementar la mutación de decisiones.
5. **Una sola fuente de publicación:** incluso con tres lectores simultáneos de Kilo, solo un escritor autorizado modifica activos, y todo cambio usa Git rama temporal `work/*`, pruebas, revisión y rollback.
6. **Operación independiente del repositorio:** el HOME y la BD son estables cuando el usuario cambia de proyecto. El origen del trabajo puede guardarse como HMAC de ruta usando una sal local, pero **la ruta literal nunca se persiste**. La referencia es seudónima, no anonimización absoluta si se compromete el dispositivo.
7. **Observar sin convertir logs en instrucciones:** datos y evidencias son material no confiable. No se interpretan como comandos ejecutables y no se incluyen automáticamente en prompts. La captura es explícita en V4.3; un plugin global de observación selectiva es candidato de V4.4.
8. **Reuniones sin silencios aprobatorios:** la vista previa no agenda ni aprueba nada. El usuario confirmó lunes 09:00 según la zona horaria local del equipo Windows para la futura reunión semanal; V4.5 debe implementar y validar ese horario y obtener aprobación explícita para activar el programador. El cierre mensual y el canal de notificación siguen pendientes. No se supone que Kilo esté funcionando todo el tiempo.
9. **SemVer individual:** el esquema reserva `releases` y las propuestas aceptan `--version`; **todavía no existe promoción, instalación ni cambio efectivo de versión**. El hash de inventario sirve para detectar cambios pero no es una versión.
10. **Medición honesta:** no inferir tokens, costos o calidad sin evidencia del runtime. Un inventario o evento no demuestra que la skill haya mejorado.

## Arquitectura física (propuesta validada para V4.3)

```text
Código versionado en Kilo-Global-Harness (GitHub)
  scripts/vx_evolution_core.py
  commands/vx-evolution.md, vx-reunion.md, ...
  docs/...
                 |
Instalador existente de Kilo
                 v
HOME/.config/kilo/harness/scripts/vx_evolution_core.py  # código ejecutable
HOME/.config/kilo/commands/vx-*.md                      # comandos Kilo
HOME/.kilo/skills/vx-evolution-core/SKILL.md           # guía por demanda
                 |
CLI Python 3.13+ (stdlib, sin servicios terceros)
                 v
HOME/.config/kilo/vx-evolution/
  vx-evolution.sqlite3            # BD operativa local (WAL, 1 escritor)
  backups/                        # copias SQLite creadas explícitamente
  vx-evolution.sqlite3-wal        # transitorio, generado por SQLite
  vx-evolution.sqlite3-shm        # transitorio, generado por SQLite
```

El instalador no ejecuta `init` ni crea la BD automáticamente. Para inicializarla hace falta un comando explícito en Windows después de instalar el código. Cualquier dato creado por V4.3 **no forma parte de la restauración del instalador de archivos**, porque eliminarlo supondría destruir el historial del usuario.

## Esquema inicial SQLite, version 1

| Tabla | Estado V4.3 | Finalidad |
| --- | --- | --- |
| `settings` | Activa | Identidad de motor Kilo, sal por usuario, observer_mode=off |
| `inventory` | Activa | Agentes/skills globales por nombre y fuente (sin perder fuentes superpuestas), huella y presencia |
| `observations` | Activa (manual) | Evento y resumen breve, proyecto HMAC opcional, fingerprint de recurrencia |
| `proposals` | Activa (pending_review) | Candidaturas para agente, skill, equipo, core y gobernanza, con prioridad y versión opcional |
| `activity_log` | Activa | Auditoría mínima de operaciones por ID, sin contenido privado |
| `releases` | Reservada | Versiones individuales y sus evidencias, nunca publicadas aquí |
| `relationships` | Reservada | Dependencia, uso y jerarquía, sin crear estructura automáticamente |
| `meetings` | Reservada | Reuniones semanales y cierres mensuales con estados |
| `decisions` | Reservada | Aprobaciones/rechazos ligados a reuniones, sin escritura automática |

Las relaciones `supervises` deberán validarse como un grafo dirigido acíclico (DAG) **antes de activar escritura**. Toda decisión de promoción requerirá evaluator distinto del sujeto, evidencia verificable y permiso humano. Las versiones activas no se sobrescribirán en la misma tabla: se crearán revisiones reproducibles.

## Comandos Python implementados

```powershell
$vx = "$HOME\.config\kilo\harness\scripts\vx_evolution_core.py"
python -I $vx status --json                  # sin crear BD
python -I $vx init --json                    # inicialización explicita
python -I $vx inventory-sync --json          # escanea SOLO Kilo global
python -I $vx integrity --json               # quick_check + foreign keys
python -I $vx observe --type correction --summary "Comprobar imports antes de reportar ausencia" --json
python -I $vx propose --kind skill --target vx-import-check --title "Revisar comprobacion de imports" --reason "Evitar falsos positivos" --priority P1 --version 0.1.0-rc.1 --json
python -I $vx meeting-preview --cadence weekly --json
python -I $vx meeting-preview --cadence monthly --json
python -I $vx backup --json                   # copia de BD manual
```

Todas las acciones se procesan localmente. `inventory-sync` puede marcar una fuente como ausente sin borrar el historial; no instala agentes. `observe` y `propose` registran datos en HOME, por lo que **sí escriben el registro privado**; `status`, `integrity` y `meeting-preview` son lecturas. Rechaza texto con patrones obvios de secretos, correos y rutas, pero ningún filtro regular garantiza privacidad perfecta. No pegar prompts, código privado, tokens ni datos personales.

**Importante:** el uso de `-I` aísla Python de site-packages y variables PYTHONPATH; este núcleo solo necesita biblioteca estándar.

## Formas de operación y riesgos

- **Interrupción o apagón:** las transacciones SQLite son atómicas y el backup explícito permite recuperar un punto consistente. WAL no sustituye el backup. Si hay corrupción, ejecutar `integrity` e investigar antes de restaurar.
- **Concurrencia:** `busy_timeout=5000`, WAL futuro; un único writer transaccional. Las reuniones y observaciones no requerirán múltiples escritores. No colocar la BD en carpeta de sincronización nube o unidad de red.
- **Almacenamiento:** se garantiza que la BD se resuelve dentro de HOME y no dentro de un repositorio. Se rechazan symlinks externos a HOME para inventario.
- **Secretos:** nunca guardar valores de `kilo.jsonc` ni contenidos de SKILL.md o agentes en SQLite; solo identidad, origen relativo y SHA256. Los datos escritos manualmente siguen siendo responsabilidad del remitente.
- **Retención:** la política se ha dejado intencionadamente en `pending_governance`. No implementar borrado automático hasta acordar horizontes y métodos de anonimización.
- **Versiones y gobierno:** `pending_review` no implica aprobación. Aunque existan tablas `decisions` y `releases`, el CLI de V4.3 no escribe en ellas.
- **Perfiles existentes:** los 21 agentes JSON y 18 Markdown del informe anterior pueden compartir nombres; el inventario guarda entradas por fuente sin deducir cuál vence en Kilo. `vx-reconciliar` sigue siendo el comprobador de precedencia y discrepancias.

## Auditoría de huecos previa a V4.4

| Área | Hueco real | Control propuesto |
| --- | --- | --- |
| Historial de todas las tareas | V4.3 solo registra observaciones explícitas | Plugin Kilo global liviano, con whitelist de eventos y consentimiento |
| Capacidad de skill | Inventario solo nombre/fuente/huella | Clasificación de capacidades validada, versión y suite de tareas |
| Duplicación semántica | Fingerprint de texto exacto; no fusiona similares | Dedupe por familia/causa tras confirmación de auditor |
| Aprobaciones | Tablas reservadas, no hay identidad de aprobador | Reunión con confirmación explícita y registro verificable |
| Versionado operativo | Registro de propuestas con SemVer, sin instalación | Candidata inmutable, validación, diff, rollback y prueba negativa |
| Reunión semanal | Solo agenda previa; lunes 09:00 hora local confirmado | Implementar y probar la zona horaria efectiva Windows y cambios de horario de verano en V4.5; programador desactivado hasta aprobación explícita |
| Cierre mensual | Solo vista previa | Consolidación histórica y cierre formal con checklist |
| Retención de datos | Pendiente | Elegir TTL de eventos y backup seguro |
| Métricas reales | No se computan tokens ni tiempos automáticamente | Instrumentación Kilo y fuente medible; NO MEDIDO por defecto |
| Promociones | Sin contratación o ascensos automáticos | Evaluador independiente, DAG sin ciclos, votación/aprobación |
| Multi-PC | BD local a un HOME, sin sincronización | Decidir si futuro backup/export cifrado o instancia única |
| Registro de privacidad | Resúmenes manuales potencialmente sensibles | Minimización, filtros y auditoría privada; no extraer logs crudos |

## Preguntas pendientes para la dirección (sin bloquear V4.3)

1. **Reunión semanal — CONFIRMADA:** lunes 09:00 en zona local del equipo Windows (independiente del proyecto). **No programar antes de implementar y validar V4.5 ni activar sin autorización expresa.** La especificación de diseño está en `config/vx-reunion-policy.v1.json`; el motor V4.3 no interpreta aún esta política.
2. **Cierre mensual:** ¿último día laborable o primer lunes del mes siguiente? El cierre deberá dar tiempo a consolidar eventos.
3. **Retención:** ¿conservar observaciones detalladas 90 días y actas/versiones indefinidamente hasta aprobación de borrado? Es una propuesta, no valor activo.
4. **Equipo:** ¿el motor se usará en un solo ordenador Windows o habrá dos o más clientes Kilo? La respuesta cambia el plan de sincronización/backup.

## Procedencia metodológica

Las ideas de observación y mejora se inspiran en [Task Observer / One Skill to Rule Them All](https://github.com/rebelytics/one-skill-to-rule-them-all), cuyo proyecto distribuye material bajo CC BY 4.0. V4.3 **no copia ni ejecuta** scripts, hooks o prompts originales: implementa un núcleo nuevo orientado a Kilo. Cualquier reutilización literal posterior exige auditoría de licencia y atribución.

Para las decisiones aún abiertas consultar [VX Evolution — decisiones y preguntas](VX-EVOLUTION-DECISIONES.md).

## Fases previstas

- **V4.3 (esta entrega):** core local Kilo-only, SQLite, inventario, observaciones manuales, propuestas, agenda preview, comandos globales y tests.
- **V4.4:** Observer ligero de eventos de Kilo con privacidad/deduplicación y límite de coste.
- **V4.5:** VX Reunión semanal y cierre mensual, decisiones explícitas con garantías y programación opcional.
- **V4.6:** capacitación y auditoría organizativa con evaluaciones y candidatos.
- **V4.7:** vx-upgrade con releases inmutables, gates y rollback sin alterar modelo/credenciales.
- **V4.8:** observabilidad, métricas reales y comparación vs single-agent.

No hay servicio de fondo ni reuniones programadas en esta entrega. La decisión semanal está documentada pero la vista previa V4.3 usa periodos UTC y no implementa el disparador local.
