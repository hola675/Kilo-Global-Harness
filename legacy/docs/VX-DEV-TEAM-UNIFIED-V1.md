# VX Dev Team · Instalación única del Core 1.6.2-rc1

**Actualización:** 2026-11-22 · **Estado:** fuente versionada. Instalación local y concurrencia real de Kilo Desktop requieren pruebas separadas.

Este es el único paquete soportado en el repositorio. No utilizar instaladores V3/V4, DevTeam-Only, packs de convivencia, clones del registro antiguo ni ejecutables de VX Evolution que ya no pertenecen al Core actual.

## Qué instala

- **18 agentes:** un líder visible **VX Dev Team** (`vx-dev-team`) y 17 subagentes ocultos (10 especialistas Dev read-only, seis builders con edición `ask`, asesor Workers read-only).
- **57 Skills:** 18 CORE, 35 CAPABILITY y 4 CONTEXTUAL; las cuatro contextuales no se añaden automáticamente a la allowlist del líder/builders.
- **3 comandos:** `/vx-equipo`, `/vx-dependencias`, `/vx-editorial`.
- **2 soportes:** `vx_task_dag.py` y copia del manifiesto de instalación.
- **AGENTS.md global completo** procedente de `rules/AGENTS-global-managed.md`: se sustituye enteramente, guardando copia cifrada del anterior.
- **Estado SQLite:** la cola persistente `~/.config/kilo/harness/state/vx-team-queue.sqlite3` se crea si falta o migra de forma aditiva a esquema v1. Conserva tareas, eventos e información existente; los snapshots de WAL están en el backup DPAPI.

**Entrypoint:** `scripts/Instalar-DevTeam-Unificado.ps1`. Backend en `scripts/vx_unified_pack.py` y dos módulos de seguridad DPAPI: `scripts/vx_pack_coexist_v023.py` y `scripts/vx_pack_bootstrap.py`. Aunque esos dos nombres son antiguos, ambos están **importados por el instalador vigente** y no se pueden retirar sin reemplazo probado.

## MCP dinámicos — permisos de los 18 agentes (SOURCE)

Desde esta revisión, el líder y los 17 subagentes declaran `permission: "*": ask`, de modo que pueden **descubrir y solicitar** cualquier herramienta MCP que la sesión efectiva de Kilo les exponga, sin enumerar servidores como Context7, GitHub, Playwright, Figma, etc. Los nombres exactos y servidores disponibles dependen de la configuración existente del usuario, no del Harness. Las excepciones explícitas del frontmatter (`task`, `agent_manager`, `edit`, `write`, `bash`, `external_directory`, etc.) conservan su prioridad. Los agentes de análisis siguen sin escritura nativa; los builders escriben únicamente con `ask` y ámbito contratado.

**No es acceso irrestricto ni instalación automática:** `ask` deja la autorización al runtime de Kilo, y una herramienta MCP puede estar ausente, desconectada o requerir OAuth/scopes propios. No se cambian `kilo.jsonc`, credenciales, listas de servidores ni ajustes AutoApprove. Operaciones MCP con efectos externos (escritura, ejecución, publicación, borrado, dinero, infraestructura, secretos o producción) requieren autorización correspondiente. Ningún agente debe usar un MCP para evadir denegaciones de la política del usuario, del proyecto o del host.

**Validación separada:** CI comprueba exclusivamente que las definiciones de los 18 agentes contienen la regla y mantienen permisos nativos. La disponibilidad y aprobación de herramientas MCP por sesión necesita prueba controlada en Kilo Desktop; reportar `SOURCE_PASS` no significa `HOST_RUNTIME_PASS`.

## Todas las Skills accesibles, MCP dinámicos con aprobación (SOURCE)

Los 18 agentes VX pueden cargar todas las Skills **realmente descubiertas** por Kilo mediante `skill: "*": allow` (el asesor Workers ya usaba `skill: allow`). La selección seguirá siendo contextual: la lista de Skills recomendadas por especialidad no restringe la carga y no se ejecuta todo el catálogo por defecto. Esto incluye las 57 Skills del pack y otras Skills existentes del usuario/proyecto. Cargar una Skill no ejecuta su código ni concede permiso de escritura, shell, delegación, MCP ni acceso a secretos.

Las herramientas MCP permanecen disponibles para solicitud bajo `permission: "*": ask`, sujetas a autorización efectiva del host y del proveedor. No se modifica `kilo.jsonc`, servidores, credenciales, scopes ni opciones de AutoApprove. `SOURCE_PASS` no implica `HOST_RUNTIME_PASS`; comprobar las Skills y herramientas realmente expuestas tras reinstalar y reiniciar Kilo.

**Si existe `rules/AGENTS.md` sin seguimiento Git**, conservarlo fuera del checkout antes de instalar. No asumir que es basura: comparar con la política administrada y mover una copia original a un directorio privado respaldado antes de liberar el árbol. El instalador exige `main` limpio y sincronizado. No usar `git clean` ni `reset --hard` sobre contenido ajeno.

**Carga recomendada del líder:** su prompt solicita al comenzar `vx-dev-project-policy` y `vx-team-bootstrap` cuando Kilo exponga la herramienta `skill`; `vx-dev-team-handoff` se reserva para delegaciones reales. Otras Skills se seleccionan por tarea, sin cargar el catálogo completo ni suponer que una solicitud se ejecutó si Kilo la rechazó. Las Skills no alteran las ACL ni la aprobación de MCP.

## Instalación Windows

Abrir PowerShell 7 **fuera de Kilo**, cerrar Kilo Desktop/VS Code/VSCodium para aplicar y verificar que el checkout local está limpio y sincronizado.

```powershell
Set-Location 'D:\Proyectos\Kilo-Global-Harness'
git switch main
git fetch origin --prune
git pull --ff-only origin main
git status --short

pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Diagnostico
pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Simular
```

Examinar `status`, `blockers`, `state_status`, `files_to_create`, `files_to_replace` y `managed_legacy_candidates`, además del estado Git y los worktrees inventariados. La limpieza automática se limita a hasta 14 rutas legacy VX del manifiesto, nunca a ramas, worktrees, código del proyecto ni bases de datos de otras aplicaciones. Solo después de aprobar el alcance de sustitución del Core, ejecutar:

```powershell
pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 `
  -Modo Aplicar `
  -ConfirmarInstalacion `
  -ConfirmarRetirarVXLegacy `
  -ConfirmarKiloCerrado

pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Verificar
```

`Aplicar` exige `main` sincronizada, árbol limpio, Kilo cerrado, backup cifrado DPAPI CurrentUser y lista exacta de los **14 paths históricos** que puede retirar de HOME. No borra recursos de terceros, no toca `kilo.jsonc`, credenciales, MCP ni AutoApprove. Toda ruta reemplazada queda incluida en el respaldo de restauración; también el estado SQLite anterior, en un snapshot consistente. Las migraciones SQLite son versionadas, conservadoras, idempotentes y verificadas mediante integridad. Si la versión es desconocida o la base no se puede validar, se bloquea sin sobrescribirla.

## Informe automático de cada instalación y actualización

Al ejecutar **Aplicar**, el motor guarda en la carpeta privada de respaldo DPAPI tanto `install-report.json` como `install-report.md`. En la salida de consola presenta las rutas, conteos y situación de SQLite. El informe detalla para cada archivo administrado: creado, reemplazado, eliminado o sin cambios; versión y fecha declaradas antes y después (o «No declarada»); hashes y coincidencia con lo instalado. Distingue el script `vx_task_dag.py` instalado en Kilo de scripts que solo se ejecutan en el checkout, e incluye conteos agregados de tablas SQLite sin exportar tareas.

El modo `Informe` **no reinstala, no migra y no borra**; reconstruye un informe para respaldos anteriores que aún no tenían reportes. Si existe uno, lo conserva sin reescribir el historial:

```powershell
pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Informe -CarpetaRespaldo 'C:\Users\Admin\.config\kilo-harness-backups\vx-unified-20261122-152634-3933e6fb'
```

Sin `-CarpetaRespaldo` elige el recibo más reciente. Los informes no demuestran por sí mismos que Kilo habilite las herramientas y permisos del agente. Solo se reportan elementos del manifiesto y sus rutas aprobadas; nunca se limpia trabajo de proyecto por inferencia.


### R2 — Observador Kilo experimental (desactivado)

El prototipo se mantiene **solo en el checkout** en `runtime/kilo-observer/vx-runtime-observer.js`; no se copia a `~/.config/kilo/plugin/`, no se añade a `kilo.json(c)`, no eleva ACL y no se inicia con el instalador. Requiere conjuntamente `VX_OBSERVER_ENABLE=1` y `VX_OBSERVER_PROJECT=<nombre-exacto-de-directorio>` para hacer cualquier escritura; ninguna sesión de otro proyecto queda incluida. La carga en Kilo Desktop y la existencia del runtime Bun con `bun:sqlite` deben comprobarse en una instalación/laboratorio aislado. La documentación oficial de plugins confirma hooks para CLI y VS Code, **no acredita Desktop de este usuario**.

El código observa `task`, `skill`, `board_post`, `board_read` y eventos de ciclo de sesión, **sin leer, serializar ni persistir argumentos, prompts, respuestas, texto de archivos, credenciales, rutas completas ni IDs de sesión sin hash**. Las observaciones quedan en una base separada, `~/.config/kilo/harness/state/vx-runtime-observations.sqlite3`, con clave de idempotencia, tabla `host_observations` y esquema independiente v1. No toca las tablas `tasks`, `events` ni `project_config` de la cola existente: un hook observado no es un task verificado.

Consultar su estado sin crear ni mutar ninguna DB:

```powershell
python -I .\scripts\vx_task_dag.py --observer-report
python -I .\scripts\vx_task_dag.py --observer-report --project vecidya
```

Mientras no se autorice su activación en un HOME de prueba, el resultado esperado es `ABSENT`. No activar `VX_OBSERVER_ENABLE=1` ni `VX_OBSERVER_PROJECT` en sesiones productivas/Vecidya en curso. Al iniciar el laboratorio, copiar la fuente al directorio plugin de ese perfil y verificar eventos reales antes de extender el instalador. Una vez verificado, R3 contempla enlazar eventos observados con IDs de tareas reales, sin inferir resultados por el mero regreso de una herramienta.

### R3 — Contrato de observación probado sin el host

El plugin se dividió en un adaptador Bun y el normalizador puro 
`runtime/kilo-observer/lib/vx-observer-hooks.js`. Las pruebas Node simulan callbacks
`task`, `skill` y eventos de sesión, comprueban que no llegan al escritor
argumentos, respuestas ni identificadores en claro y validan la idempotencia de las claves.
El código escribe de forma transaccional mínima con
`INSERT OR IGNORE` en su SQLite independiente y no toca la cola DAG de estados de tareas.

Para ejecutar las pruebas sin Kilo ni escritura en el HOME:

```powershell
node --test .\tests\test_vx_observer_contract.mjs
python -I .\scripts\vx_task_dag.py --observer-report
```

**GATE R3 abierto:** los tests de callbacks simulados NO demuestran que Kilo Desktop
cargue el plugin, ni que emita identificadores equivalentes a los documentados para CLI.
Primero validar en un perfil separado y proyecto temporal, con consentimiento y respaldo.
No activar observación en Vecidya hasta que haya evidencia de compatibilidad y
verificación privada de datos. La consulta devuelve observaciones, no tareas VERIFIED.

### R3 — Laboratorio aislado de Kilo en Windows

El laboratorio tiene un instalador **independiente del pack global**, en
`scripts/Probar-Observador-Kilo.ps1`, y solo puede crear un directorio NUEVO
dentro de TEMP. No inicia Kilo ni copia credenciales, modos, modelos, MCP o datos
de Vecidya. El adaptador del plugin acepta `VX_OBSERVER_STATE_ROOT` para
dirigir SQLite exclusivamente a un directorio elegido; valida que sea absoluto,
que no contenga NUL y que no atraviese symlinks conocidos.

```powershell
# Ejecutar desde el checkout de Kilo-Global-Harness
pwsh -NoProfile -File .\scripts\Probar-Observador-Kilo.ps1 -Modo Diagnostico
pwsh -NoProfile -File .\scripts\Probar-Observador-Kilo.ps1 -Modo Preparar
pwsh -NoProfile -File .\scripts\Probar-Observador-Kilo.ps1 -Modo Verificar
# Tras cerrar manualmente el Kilo CLI del laboratorio:
pwsh -NoProfile -File .\scripts\Probar-Observador-Kilo.ps1 -Modo Limpiar -ConfirmarLimpieza -ConfirmarLabCerrado
```

El modo Preparar crea `%TEMP%\vx-kilo-observer-lab\vx-observer-lab\.kilo\plugin\`
y un `Iniciar-Laboratorio.ps1` para inicio **manual**, que fija variables HOME,
USERPROFILE, XDG y APPDATA únicamente en su propio proceso. No los cambia en la
terminal actual ni en Windows. El script busca primero `kilo` en PATH y después el CLI
incluido en Kilo Desktop bajo `%LOCALAPPDATA%\KiloDesktop\app-*\resources\kilo\<variant>\bin\kilo.exe`.
Al generar el lanzador fija la ruta absoluta encontrada ANTES de aislar `LOCALAPPDATA`,
por lo que no requiere instalar otro CLI ni modificar PATH global. No reutiliza la sesión
Desktop que está trabajando en Vecidya.

El laboratorio sin iniciar debe devolver observaciones `ABSENT`. Tras iniciar
manualmente CLI y generar eventos de prueba sin secretos, Verificar comprueba solo
conteos en su base propia. La prueba Bun en CI realiza inserciones y consultas
reales con DB desechable en la carpeta temporal del runner.

**GATE R3:** SQLite real y callbacks probados en CI no son prueba de carga del
plugin en Kilo Desktop. Tampoco demuestran la vinculación de IDs de task con
estados VERIFIED de la cola principal. No integrar al instalador global ni
activar sobre Vecidya sin evidencia específica y rollback de laboratorio.

### R3 — Evidencia local de hooks Kilo CLI (2026-11-23)

**Alcance certificado: observabilidad básica en laboratorio, no ejecución ni resultados de agentes.** El operador ejecutó manualmente Kilo CLI `7.8.27`, incluido en Kilo Desktop `app-1.0.0`, dentro de `%TEMP%\vx-kilo-observer-lab\vx-observer-lab`. El plugin se cargó desde `.kilo/plugin` del proyecto temporal y la base independiente se creó en `%TEMP%\vx-kilo-observer-lab\state\vx-runtime-observations.sqlite3`. No fue necesario instalar otro CLI ni modificar PATH global. El informe del lanzador indicó `global_install_changes: 0`; esto no constituye una auditoría del sistema operativo.

**Evidencia proporcionada por el operador:** tras tres sesiones, el informe `vx-host-observer-report/1` devolvió `total_events: 12`: tres `session.created`, cuatro `session.updated`, tres `session.idle`, un `TOOL_CALLED_NOT_CONFIRMED` y un `TOOL_RETURNED_NOT_VERIFIED`. La consulta SQLite de solo lectura confirmó para ambos eventos `tool=skill`, mismo prefijo de `session_ref=5f147f42a452` y de `call_ref=e390e496a5fc`; marcas UTC `2026-11-23T10:10:16.967Z` y `2026-11-23T10:10:17.060Z`. Se comparten únicamente prefijos hash, no identificadores originales ni contenido. El intervalo de 93 ms es entre observaciones, no una métrica de éxito funcional.

**Certificación parcial:** `R3_HOST_HOOKS_OBSERVED_PASS` para detección CLI, carga del plugin en CLI aislado, hooks de ciclo de sesión, callbacks antes/después de `skill`, correlación por sesión/llamada y persistencia SQLite. El informe canónico permanece `OBSERVED_NOT_CERTIFIED`, `actions_executed: 0`, `host_results_verified: false`, `runtime_verified: false` y `tasks_registered: false`. Ningún retorno equivale a una entrega verificada; no hay evidencia suficiente para `HOST_RUNTIME_PASS` integral, Kilo Desktop GUI, Board, delegación, permisos de escritura, DAG ni éxito de herramientas.

**Siguiente gate:** correlacionar futuras llamadas del host con IDs de tareas DAG **solo mediante relación explícita y verificable**, sin reconstruir IDs desde hashes ni crear tareas por el mero evento. Mantener el observador opt-in y fuera del instalador global. Las pruebas de privacidad, fallo seguro, rollback, retención y coexistencia deberán preceder a cualquier habilitación productiva.

### R4 — Correlación explícita solo lectura (fuente experimental)

El script `scripts/vx_observer_dag_correlation.py` consulta dos bases SQLite existentes en modo `ro` y `query_only`. Exige `--queue-db`, `--observer-db`, `--project`, `--task-id`, `--session-ref` y `--call-ref`. Los dos últimos son hashes SHA256 **completos**, obtenidos del observador por una operación autorizada; los prefijos publicados para R3 no bastan. El operador debe aportar expresamente el vínculo: no se infiere de la coincidencia de hora ni del nombre de herramienta.

El resultado `CORRELATED_NOT_VERIFIED` requiere tarea existente en el proyecto correcto y **exactamente un evento before y uno after** para el mismo par de hashes y la misma herramienta reconocida. El resultado informa únicamente de la correlación, no de la identidad autenticada, entrega, éxito ni revisión. `NOT_CORRELATED` cubre ausencias y ambigüedades. Es una consulta puntual **sin tabla de vínculos**, sin cambios de estado y sin invocar Kilo. No habilita permisos, no instala plugins y no participa en el instalador global. Tests focalizados: `python -m unittest discover -s tests -p test_vx_observer_dag_correlation.py -v`.

**Gate R4 sigue abierto:** falta verificar en el host cómo obtener y autenticar vínculos de tareas reales, verificar resultados externos, controlar datos sensibles y cerrar la integración de coordinación. No utilizar este informe para marcar `VERIFIED`.

### R4.2 — Vínculo explícito con tarea del host (experimental)

El correlador v1.1.0 admite opcionalmente `--link-file <ruta-absoluta>`, un archivo JSON de como máximo 4096 bytes con exactamente `schema: vx-observer-task-link/1`, `project`, `task_id`, `host_task_id`, `session_ref`, `call_ref` y `tool`. El operador obtiene estos campos por un procedimiento autorizado: **nunca inferir automáticamente** los hashes desde un ID de host ni almacenar prompts o credenciales. No guardar este JSON en Git ni en repositorios de clientes.

La consulta exige coincidencia exacta del proyecto, tarea y hashes SHA256 completos con el argumento CLI, así como `host_task_id` con la tarea ya existente en SQLite y `tool` con ambos hooks de la misma llamada. Los archivos de vínculo son privados, preexistentes y de solo lectura; ninguna operación escribe en la cola ni en la base de eventos. Si la evidencia coincide, devuelve `LINKED_OBSERVED_NOT_VERIFIED`, que **no** es prueba de identidad autenticada, entrega, aprobación, resultado correcto ni ejecución completa del agente. Ausencias producen `NOT_CORRELATED` y contradicciones se rechazan. Sin `--link-file`, el contrato R4 original sigue compatible.

**Gate abierto:** falta corroborar el origen auténtico del vínculo con Kilo y resultados de tareas reales; el informe siempre conserva `explicit_mapping_authenticated: false` y `host_results_verified: false`. Mantener fuera del instalador y de producción.

### R4.3 — Integridad de recibo de evidencia (sin autenticación del host)

El correlador v1.2.0 añade opcionalmente `--receipt-file` y `--artifact-file` (ambos obligatorios conjuntamente y solo junto a `--link-file`). El recibo JSON v1 exige exactamente los campos del vínculo R4.2, más `artifact_sha256`. La lectura está limitada a un recibo de 4096 bytes y una evidencia de 1 MiB; el digest SHA256 se calcula sin guardar ni mostrar el contenido. Los archivos deben ser absolutos, regulares, preexistentes y diferentes de las bases SQLite y el archivo de vínculo. Rechaza recibos cuyo proyecto, tarea, host, hashes o herramienta difieran del vínculo. En ausencia de hooks pareados no se examina la integridad y se conserva `NOT_CORRELATED`.

`RECEIPT_INTEGRITY_MATCH_NOT_AUTHENTICATED` significa exclusivamente que la evidencia conserva los bytes referenciados por el recibo y que la llamada observada corresponde al vínculo declarado. `RECEIPT_INTEGRITY_MISMATCH` detecta bytes diferentes; ambos mantienen `receipt_origin_authenticated=false`, `artifact_content_reviewed=false`, `host_results_verified=false`, `dag_state_modified=false`. **Un SHA256 no acredita procedencia ni ejecución real del host**, y un recibo autogenerado puede coincidir sin ser confiable. No considerar `VERIFIED` ni `DELIVERED` por esta fase.

La comprobación es experimental, solo lectura y fuera del instalador global. Siguiente gate: una fuente de recibos autenticada y verificable fuera de la declaración del propio operador; definir confianza del emisor y comprobar resultados efectivamente antes de cambiar estados DAG.

### R4.4 — Sello HMAC opcional con emisor configurado (no autenticación de Kilo)

El correlador v1.3.0 incorpora `--attestation-file`, `--trust-key-file` y `--trusted-issuer`, que deben proporcionarse conjuntamente con vínculo, recibo y evidencia. El sello `vx-receipt-hmac/1` contiene exactamente `schema`, `issuer`, `receipt_sha256`, `mac_sha256`. HMAC-SHA256 cubre el dominio `VX-OBSERVER-RECEIPT-MAC-V1`, emisor y hash de los **bytes exactos** del recibo. Exige clave binaria de 32–128 bytes y valida estructura, fuente, hash y MAC en comparación constante. No escribe la clave en salida ni en SQLite; el operador debe custodiarla fuera del repositorio y no compartirla con agentes de menor confianza. En esta fase no se generan ni distribuyen claves, no se gestiona rotación y no se instala la función globalmente.

`RECEIPT_MAC_MATCH_KEY_POSSESSION_ONLY` indica únicamente que el sello coincide con una clave que el operador decidió confiar; **no identifica por sí mismo a Kilo, no prueba que el host haya emitido el recibo y no valida ejecución, resultado, autoría, aprobación ni revisión**. Una persona o proceso con acceso a la clave podría fabricar un sello. MAC incorrecto genera `RECEIPT_MAC_INVALID`; parámetros incompletos y emisor incompatible se rechazan. `receipt_origin_authenticated` y `host_results_verified` permanecen siempre falsos. Sin parámetros nuevos se conservan los estados anteriores. La cola DAG permanece inalterada.

**Gate para futura autenticación de host:** diseñar custodia y aislamiento de clave, un emisor atestado e independiente de la sesión solicitante, protección anti-replay y revocación, verificación de resultados del host y evidencia de tareas reales. Ningún resultado R4.4 autoriza promover estados DAG.

### R4.5 — Política de confianza, caducidad y revocación (experimental)

Se admite `--trust-policy-file` únicamente junto a todos los parámetros HMAC de R4.4. El archivo JSON privado `vx-receipt-trust-policy/1` contiene exactamente `schema`, `issuer`, `project`, `allowed_tools`, `key_sha256`, `revoked`, `not_after_utc`, `revoked_receipts_sha256`. El archivo tiene un límite de 8192 bytes; admite una lista de herramientas declaradas y hasta 128 hashes de recibos revocados. Rechaza claves distintas, emisor/proyecto/herramienta no autorizados, caducidad vencida y revocación. Las entradas se validan antes de emitir estado de coincidencia de política y no modifican ni la cola DAG ni SQLite del observador.

`RECEIPT_MAC_MATCH_POLICY_SCOPED_ONLY` significa únicamente **MAC correcto y política externa suministrada coherente con esa clave y contexto**. La política es controlada por quien la suministra: no es evidencia de que Kilo haya emitido el sello. Su lista de revocación es estática y **no constituye prevención atómica de replay**: una invocación repetida puede validar el mismo recibo mientras no se revoque externamente. No se ha implementado custodia segura del emisor, autoridad independiente, rotación automática ni promoción de `DELIVERED`/`VERIFIED`. Los campos `receipt_origin_authenticated` y `host_results_verified` siguen siendo falsos.

**Siguiente gate:** fuente independiente de identidad, registro antirreutilización transaccional con aislamiento y controles de ACL, revisión efectiva de resultados y validación en un laboratorio real de Kilo. No introducir claves ni archivos privados en Git ni instalar esta función globalmente.

### R6 — Limpieza de ramas remotas con comprobación previa

`scripts/Eliminar-RamasFusionadas.ps1` es una herramienta manual,
no ejecutada por el instalador. Por defecto solo simula. Exige GitHub CLI autenticado
y una copia limpia de `main`, consulta refs remotas reales, los PR
fusionados a `main` y el último commit **histórico** de cada PR,
comprueba los worktrees y aplica `--force-with-lease` al borrar cada ref.
Un commit nuevo posterior al PR o una rama local divergente bloquean el borrado.

```powershell
pwsh -NoProfile -File .\scripts\Eliminar-RamasFusionadas.ps1
pwsh -NoProfile -File .\scripts\Eliminar-RamasFusionadas.ps1 -Aplicar -ConfirmarBorrado
```

No elimina la rama `main`, y las ramas locales únicamente se borran
si se añade expresamente `-EliminarLocales` después de todas las comprobaciones.
El comando no se ejecuta automáticamente durante una instalación del pack.

## Restauración

Conservar privada la carpeta `vx-unified-...` que informa el motor. Si una instalación genera errores, consultar antes de restaurar modificaciones posteriores en los destinos:

```powershell
pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 `
  -Modo Restaurar `
  -CarpetaRespaldo 'RUTA_ABSOLUTA_DEL_BACKUP_DPAPI' `
  -ConfirmarRestauracion `
  -ConfirmarKiloCerrado
```

La recuperación de una aplicación interrumpida utiliza además `-RecuperarInstalacionInterrumpida` solo si se confirma el estado. Ninguna restauración debe machacar ediciones de terceros posteriores. **Si la cola SQLite recibió tareas o eventos nuevos tras instalar, Restaurar se bloquea en lugar de perderlos.** La recuperación segura requiere revisar esos cambios antes de revertir.

## Después de instalar

Abrir Kilo Desktop y certificar invocaciones reales de `skill`, `task`, permisos de escritura de builders, `task(background: true)` y `board_post/board_read` si están presentes. El líder y seis builders tienen Board autorizado en source; los once analistas read-only no.

**Tres estados diferentes:** `SOURCE_PASS` (CI) → `INSTALLED_FILES_MATCH` (verificación del instalador) → `HOST_RUNTIME_PASS` (evidencia en Kilo). La cola SQLite no ejecuta agentes ni funciona con Kilo cerrado.

Ver [arquitectura](ARQUITECTURA.md), [autonomía](VX-DEV-TEAM-AUTOPILOT-V2.md) y [registro de depuración](VX-HARNESS-INVENTARIO-AUDIT-20261121.md).


## Roadmap vivo de implementación — 2026-11-23

**Objetivo:** evolucionar un único Harness instalable, sin perder la ejecución actual de Vecidya ni confundir fuente, instalación y runtime. Esta sección es la fuente canónica de avance; no generar documentos de roadmap por fase.

| Orden | Fase | Estado | Criterio de aceptación |
|---|---|---|---|
| R1 | Saneamiento de contratos y referencias | SOURCE_PASS_PENDIENTE_MAIN | Ningún agente referencia un ejecutable retirado o Skill inexistente; documentación/selector/manifiesto concuerdan; CI PASS |
| R2 | Observador no invasivo de Kilo | SOURCE_PASS_NO_ACTIVADO | Plugin local desactivado por defecto, sin alterar herramientas ni registrar conversaciones, prompts, tokens, rutas completas o credenciales |
| R3 | Persistencia del runtime | R3_HOST_HOOKS_OBSERVED_PASS_DAG_PENDING | Eventos observados con idempotencia y consulta solo lectura; no confundirlos con tareas DAG registradas ni éxito certificado |
| R4 | Coordinación multiagente | R4_SCOPED_TRUST_POLICY_SOURCE_PENDING_TRUSTED_HOST | Conflictos de escritura probados, ID real de host, recuperación y barrera de integración; sin elevar ACL |
| R5 | Certificación integral | PENDIENTE_HOST | CI Windows y laboratorio real de Kilo con herramientas, Skills, delegación, Board y persistencia; evidencia verificable |
| R6 | Consolidación Git/contexto | BLOQUEADO_LIMPIEZA_REMOTA | Reducir duplicaciones sin perder conducta; PR y CI; retirar solo ramas fusionadas sin trabajo exclusivo |

### Gates de seguridad y reversibilidad

- **G0:** Inventariar checkout, PR, CI, worktrees y respaldos. No interrumpir Vecidya.
- **G1:** Cambiar referencias/documentación/versiones sin modificar ACL ni otros proyectos.
- **G2:** Investigar el contrato oficial de eventos Kilo; el soporte documentado en CLI/VS Code no certifica el Desktop. El observador se entrega desactivado.
- **G3:** Laboratorio aislado antes de activar el plugin globalmente: sin secretos, contenido de cliente, salida de herramientas ni rutas completas. Si el host no soporta hooks, seguir con el ledger de sesión.
- **G4:** Los eventos del hook demuestran observación, no entrega, aprobación o estado VERIFIED. Persistencia y cola DAG requieren contratos separados.
- **G5:** Cambios por PR, CI y respaldo. Para instalar en Windows, Kilo cerrado, confirmación explícita y restauración disponible.

**Evidencia de partida:** 53 pruebas CI Windows correctas tras R1/R2; usuario confirmó instalación de 18 agentes/57 Skills y base SQLite íntegra con tres tablas y cero registros de tareas, eventos y proyectos. Hubo delegación real en Vecidya, no reflejada automáticamente en esa base.

**Bloqueo Git:** 14 ramas remotas de PR fusionados continúan en GitHub. El navegador de automatización no posee autenticación para borrarlas. Para continuar sin crear una rama adicional se reutiliza temporalmente una rama fusionada, sincronizada con main mediante merge no destructivo (sin force-push).
