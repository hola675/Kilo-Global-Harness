# VX Reunión V4.5 — Gobierno local manual y calendario global de Kilo

**Estado:** implementación manual de agendas, actas y decisiones; **sin tareas programadas, sin notificaciones, sin aprobaciones automáticas de cambios y sin modificación de agents/skills**. Alcance exclusivamente Kilo Code y el almacenamiento global de Windows HOME.

## Decisiones de dirección confirmadas

| Reunión | Regla | Hora | Zona | Scheduler |
| --- | --- | --- | --- | --- |
| Semanal `vx-reunion` | Lunes | **09:00** | Local del equipo Windows | **OFF** |
| Cierre mensual | Primer lunes del mes siguiente | **PENDIENTE** | Local del equipo Windows | **OFF** |

La reunión mensual revisa el **mes anterior completo**. Por ejemplo, el cierre de noviembre de 2026 será el lunes **7 de diciembre de 2026** y el de diciembre de 2026 el lunes **4 de enero de 2027**.

**Preguntas aún abiertas:** hora del cierre mensual y si, en el primer lunes coincidente, sustituye a la reunión semanal o constituye una sesión separada. Mientras no se acuerde, se generan dos referencias diferenciadas y ninguna ejecución automática.

El calendario se calcula en el equipo que ejecuta el CLI utilizando fechas **locales de Windows**, sin congelar un desplazamiento UTC. Los límites históricos de observaciones se convierten a UTC usando las reglas del sistema operativo, incluso con horario de verano. El documento de política es `config/vx-reunion-policy.v1.json` y los tests de CI exigen que las constantes del calendario respeten sus decisiones. El CLI no programa reuniones futuras ni abre calendarios externos.

## Esquema SQLite v3: migración explícita y copia de seguridad

V4.5 agrega `meeting_agenda` (snapshot de hasta cinco propuestas por reunión), `meeting_notes` (acta sanitizada) y un índice que impide decidir dos veces una misma propuesta dentro de una reunión. Reutiliza `meetings` y `decisions` que existían reservadas desde V4.3.

La base local no se sobrescribe; `meeting-migrate` exige esquema v2 y crea un **backup SQLite antes de modificar el esquema**. Si el usuario tiene v1, debe ejecutar previamente `observer-migrate`. Ninguna actualización del instalador aplica migraciones silenciosas; ninguna restauración de archivos del harness borra la base operativa.

```powershell
$vx = Join-Path $HOME '.config/kilo/harness/scripts/vx_evolution_core.py'

python -I $vx status --json
python -I $vx meeting-calendar --cadence weekly --json
python -I $vx meeting-calendar --cadence monthly --json

# Después de confirmar estado: migración con backup, una sola vez
python -I $vx meeting-migrate --json
python -I $vx integrity --json
```

Si la base ya está en v3, `meeting-migrate` responde `migrated=false` y no crea otro backup.

## Ciclo manual: preparar → revisar → decidir → cerrar

Las siguientes operaciones son **explícitas**, requieren la solicitud del operador y escriben solamente en SQLite global. No dependen del proyecto activo.

```powershell
# 1. Solo lectura: ventana revisada y siguientes fechas locales.
python -I $vx meeting-preview --cadence weekly --json
python -I $vx meeting-preview --cadence monthly --json

# 2. Crear borrador de agenda y congelar hasta cinco propuestas P0→P3.
python -I $vx meeting-prepare --cadence weekly --json
python -I $vx meeting-prepare --cadence monthly --json

# 3. Consultar acta por ID retornado.
python -I $vx meeting-view --id '<uuid-reunion>' --json

# 4. Anotar un resultado neutro y verificable (sin clientes, rutas o secretos).
python -I $vx meeting-note --id '<uuid-reunion>' --text 'Revisión completada y próxima evaluación pendiente' --json

# 5. La decisión debe ejecutarse desde TERMINAL INTERACTIVA LOCAL:
python -I $vx meeting-decide --id '<uuid-reunion>' --proposal '<uuid-propuesta>' --decision approved --json

# 6. Cerrar solo cuando TODOS los puntos de la agenda tengan decisión:
python -I $vx meeting-close --id '<uuid-reunion>' --json
```

Los valores de decisión permitidos son `approved`, `rejected`, `deferred` y `revision_requested`. Una decisión aplazada o que requiere revisión conserva el estado de propuesta `pending_review` y puede aparecer en otra reunión; no se ejecuta de forma automática.

Las llamadas `meeting-decide` y `meeting-close` **rechazan stdin sin TTY** y exigen que el operador escriba un desafío efímero mostrado en terminal. Este mecanismo reduce aprobaciones accidentales, **pero no autentica criptográficamente a una persona**: la base registra `local_operator_unverified` y el resultado declara `identity_verified=false`. Una decisión aprobada **NO autoriza** por sí sola al sistema a implementar un cambio de agentes, habilidades, modelos, permisos ni a activar un plugin. V4.7 deberá incorporar una comprobación más fuerte antes de publicar cambios.

**Protección contra el silencio:** no se puede cerrar una reunión con puntos de agenda sin decisión. El máximo de cinco puntos por reunión evita reuniones inmanejables; otras propuestas quedan disponibles para la siguiente.

## Informes mensuales y semanales

`meeting-preview` calcula ventanas de revisión **por fecha calendario local**:

- Semanal: semana anterior a la reunión del lunes.
- Mensual: mes completo anterior a la reunión del primer lunes siguiente.

Devuelve observaciones explícitas verificables y propuestas pendientes. Las señales de `session.idle/error/compacted` de V4.4 pueden consultarse mediante `observer-report`, pero **no son prueba de éxito, fallos de código, calidad ni tokens consumidos**. No se asignan ascensos ni capacitación sin evaluaciones independientes.

El acta es el registro estructurado JSON/SQLite generado por `meeting-view`. Esta versión no genera PDF, DOCX, correos ni archivos en proyectos.

## Seguridad, mantenimiento y pruebas

1. **Global-only:** HOME/.config/kilo/vx-evolution.sqlite3 y los archivos globales Kilo existentes; ningún archivo se escribe en el repositorio del proyecto activo.
2. **Versión y cambios:** no publicar ni fusionar cambios de un agente por la aprobación de una propuesta. `releases` y `relationships` siguen sin escritura operativa.
3. **Sin scheduler:** ningún comando instala tareas del Programador de Windows, recordatorios, calendario o emails. El estado `scheduled_meetings=false` permanece invariante.
4. **Privacidad:** notas y títulos se validan con límites y patrones de protección; un filtro regex no reemplaza una revisión humana de privacidad.
5. **Recuperación:** SQLite WAL, backup consistente en migración, integridad y rollback del instalador que no elimina la base privada.
6. **Idempotencia:** un único borrador por cadencia y período; la agenda no se regenera al solicitar el mismo borrador.
7. **Compatibilidad:** V4.4 Observer Light continúa funcionando tanto con SQLite v2 como v3.
8. **Retención:** ninguna depuración automática hasta aprobación de una política de conservación.
9. **Auditoría:** cada decisión y cierre deja un registro de actividad. Las notas no contienen rutas ni texto original de las tareas, salvo lo introducido expresamente por un operador.
10. **Pruebas reales pendientes:** después de instalar y migrar el perfil Windows del usuario, ejecutar calendario/preview/manual con una propuesta de prueba; CI no sustituye esa prueba.

## Límite de la etapa y siguientes aprobaciones

- **V4.5 implementa** fecha local, agenda, acta, decisión interactiva y cierre manual.
- **V4.5 no activa** la reunión semanal los lunes ni el cierre mensual automáticamente, ni les asigna hora cuando no existe.
- La programación (en Windows o cualquier plataforma) requiere una **petición explícita nueva**, aun después del PASS de CI. No inferir autorización por haber confirmado el día o por haber aprobado una propuesta de skill.
- La evaluación técnica de habilidades y promociones continúa en V4.6; la publicación versionada y rollback de agentes/skills en V4.7.
