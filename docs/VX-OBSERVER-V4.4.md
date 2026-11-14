# VX Evolution V4.4 — Observer ligero para Kilo Code

**Estado:** implementado en la rama de desarrollo, pendiente de CI y prueba funcional en el Kilo del usuario. Exclusivamente Kilo Code; no se instala en proyectos, Codex ni otros clientes.

## Arquitectura y fuente verificada

Los plugins locales globales Kilo se autocargan desde `~/.config/kilo/plugin/*.js` y deben exportar `{ id, server }` con un hook `event`. Los eventos `session.idle`, `session.error` y `session.compacted` están documentados por Kilo:
https://kilo.ai/docs/automate/extending/plugins

**No son datos de rendimiento:** `session.idle` significa que una sesión quedó inactiva, no que una tarea se completara con éxito; `session.error` es un evento del runtime, no una vulnerabilidad ni fallo funcional confirmado.

## Captura mínima

El plugin `plugins/vx-observer-light.js` filtra solo tres eventos; ignora mensajes, herramientas, prompts, permisos, ficheros y diff. No lee ni registra contenido de evento. Únicamente transmite a Python la señal enumerada:

| Kilo (entrada) | Agregado SQLite (sin payload) |
| --- | --- |
| `session.idle` | `session_idle` |
| `session.error` | `session_error` |
| `session.compacted` | `session_compacted` |

La tabla `observer_counts` guarda `hour_utc`, `signal`, `observed_count` y `updated_utc`. **No guarda IDs de sesión, rutas de proyecto, textos, stack traces, modelos, tokens ni resultados.** El plugin usa un identificador de sesión **únicamente en memoria** para ignorar llamadas duplicadas en menos de 10 segundos y limita su memoria a 256 claves. Un proceso registra como máximo 120 señales por hora y SQLite acepta hasta 300 agregadas por hora entre procesos. Las señales perdidas por apagones, cierre de Kilo o falta de Python no se reconstruyen ni se afirman como observadas.

No hay llamadas a modelos, MCP ni consultas de red. El plugin inicia Python con lista cerrada de argumentos y entorno reducido. No altera prompts, llamadas a herramientas ni los permisos de agentes.

## Dos permisos explícitos e independientes

**1. Instalar plugin global:** el instalador original `Instalar-Kilo-Global-Harness.ps1` NO lo incluye por defecto; se añade únicamente con `-InstalarVXObserverV44`. Al cargarse está inerte por defecto, no genera registros.

**2. Habilitar captura:** requiere SQLite v2, `observer-mode --mode light`, que actualiza `settings.observer_mode` y crea un archivo local `observer-light.flag`. La ausencia del archivo apaga inmediatamente el hook. La desactivación explícita `observer-mode --mode off` elimina el flag antes de modificar SQLite. En todos los casos, el estado del observador se consulta con `observer-status`.

Si el plugin existente Task Observer u otro hook observa las mismas sesiones, revisar solapamiento antes de activar. No pausar ni eliminar otras extensiones a ciegas.

## Instalación y verificación segura en Windows

Desde PowerShell 7, repositorio limpio y `main` actualizada:

```powershell
Set-Location 'D:\Proyectos\Kilo-Global-Harness'
$installer = '.\scripts\Instalar-Kilo-Global-Harness.ps1'
pwsh -NoProfile -File $installer -Modo Simular -InstalarVXObserverV44
pwsh -NoProfile -File $installer -Modo Aplicar -InstalarVXObserverV44
pwsh -NoProfile -File $installer -Modo Verificar -InstalarVXObserverV44

$vx = Join-Path $HOME '.config/kilo/harness/scripts/vx_evolution_core.py'
python -I $vx observer-status --json
```

El instalador **no crea ni migra** SQLite. Si el motor no se inicializó, ejecutar `python -I $vx init --json`. Si el estado indica `schema_version=1` y `migration_required=true`, ejecutar de forma **explícita** `python -I $vx observer-migrate --json`. Ese comando realiza un respaldo SQLite antes de pasar de v1 a v2 y conserva observaciones, propuestas e inventario anteriores. Si ya es v2, no migra ni duplica respaldos.

Tras revisar compatibilidad de plugins y reiniciar Kilo para que cargue el archivo JS, para activar la captura:

```powershell
python -I $vx observer-mode --mode light --json
python -I $vx observer-status --json
python -I $vx observer-report --days 7 --json
```

Para desactivar **sin desinstalar ni borrar el histórico**:

```powershell
python -I $vx observer-mode --mode off --json
```

Para quitar el código mediante restauración, apagar antes `observer-mode off`, consultar el backup privado real del instalador y ejecutar `-Modo Restaurar -BackupFolder <ruta-real>`. No usar rollback sin revisar archivos modificados por otros procesos. La restauración del instalador no elimina `vx-evolution.sqlite3`.

## Comandos y significado

```text
status                       Estado general global
observer-status              Versión, modo off/light y flag local
observer-migrate             Migración explícita SQLite v1 -> v2, con respaldo
observer-mode --mode off     Apagar grabación
observer-mode --mode light   Autorizar contador de señales
observer-event --event ...   Entrada interna del plugin, lista cerrada
observer-report --days 7     Resumen agregado de los últimos 7 días
meeting-preview              Sigue siendo vista previa NO programada
```

Un conteo de `session_idle` **NO** representa número de tareas resueltas. Un incremento de `session_error` señala una investigación pendiente; no crea propuestas, no concluye culpabilidad de un agente ni activa capacitación automáticamente.

## Pruebas y criterios de aceptación

- Python: esquema v2 nuevo, migración explicita v1, backup consistente, estado apagado por defecto, whitelist de eventos, cambios de modo, límites de tasa, agregación y cero datos de sesión, no impacto en propuestas.
- Node: sintaxis ECMAScript, export `default.id` y `server().event` como especifica Kilo.
- Windows: instalador sin flag **no instala plugin**; instalación opt-in global, `Verificar` y rollback respetan la BD; la política semanal lunes 09:00 permanece inactiva.
- **Pendiente con el usuario:** verificar en el runtime Kilo que el plugin carga, que las señales reales aumentan en `observer-report` y que no interfiere con Task Observer ni permisos. CI no prueba la aplicación Kilo instalada.

## Huecos conscientes y continuación

1. **Semántica:** solo señales de runtime, no detecta calidad, regresiones, errores de código ni oportunidades de formación automáticamente. Las observaciones `observe` continuarán siendo explícitas y revalidadas.
2. **Persistencia de duplicados:** la supresión se hace en la memoria del plugin (10 s), no entre reinicios; el conteo agregado refleja señales, no sesiones únicas.
3. **Rendimiento:** inicia un proceso Python por evento permitido; está acotado por tasa, pero debe medirse el overhead en Windows. Si fuera notable, migrar a un recolector por lotes.
4. **Retención:** no se ejecuta purga automática hasta definir la política VX-D07. La tabla horaria puede crecer; futuro mantenimiento con backup y retención aprobada.
5. **Compatibilidad:** Kilo tiene varias superficies (CLI/VSCode) y una API de plugins susceptible de cambios. Una prueba de runtime es obligatoria antes de asumir soporte completo.
6. **Reunión:** lunes 09:00 hora local de Windows es solo una decisión de diseño para V4.5. V4.4 no crea Programador de tareas, calendarios, alertas ni aprobaciones.
7. **Multi-PC:** las bases locales independientes no se fusionan. VX-D08 permanece pendiente.

## Control del flujo

Ningún evento genera un upgrade, una skill, un jefe ni una nueva jerarquía. `vx-auditoria-equipo` y `vx-capacitacion` podrán usar estos agregados **como señales débiles**, nunca como pruebas de calidad. Los cambios de agentes requieren revisión independiente y aprobación del usuario en `vx-reunion` de V4.5 o posterior.
