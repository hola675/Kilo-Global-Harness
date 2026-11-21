# VX Dev Team Core Unificado — instalación V1.3 RC1

**Fecha:** 2026-11-21. **Estado:** SOURCE V1.3 RC1, pendiente CI/revisión e instalación local de esta mejora. El Core V1.0 anterior fue probado en Kilo Desktop por el operador; no confundirlo con certificación del nuevo background paralelo. **No instalado automáticamente.**

## Decisión

Unificar el Pack VX 0.4.0 y Dev Team 2.3.0 en una única instalación global. No ejecutar dos instaladores ni crear dos líderes. Instalar los componentes declarados en [el manifiesto unificado](../registry/vx-unified-pack-v1.json), no concatenar indiscriminadamente las dos listas históricas.

| Familia | Seleccionados | Rol |
| --- | ---: | --- |
| Líder visible | 1 | vx-dev-team, único agente principal del pack |
| Analistas especialistas | 10 | Dev Explorer, Architect, Frontend, Backend, Data, Platform, Reviewer, Quality, Security y Research; ocultos/read-only |
| Implementadores | 6 | Frontend, Backend, Data, QA, Docs y Editorial; ocultos, edit/write/apply_patch con ask |
| Cloudflare | 1 | vx-workers-adviser; oculto/read-only |
| **TOTAL** | **18** | **1 visible y 17 ocultos** |

### Skills

**46 skills**: 18 Dev CORE, más 28 VX complementarias seleccionadas por aportar una capacidad de ejecución o dominio que no se cubre solo con la estrategia CORE (TypeScript, Python, Cloudflare, SQL, E2E, Docs, Git/CI, performance, observabilidad, editorial, IDA, incidentes y colaboración, entre otras). La lista exacta y sus rutas únicas están en el manifiesto. Las skills se cargan bajo demanda: nunca las 46 simultáneamente.

Se conservan en Git las 26 Dev adicionales que aún eran propuestas y las 7 VX no incluidas. No se activan waves W2-W5 automáticamente ni se elimina la documentación de VX Evolution.

### Retiro explícito de duplicados

Se desinstalan solamente seis agentes VX anteriores: vx-integrador, vx-inspector, vx-researcher, vx-security-reviewer, vx-test-analyst y vx-frontend-adviser. Sus funciones pasan al líder y a especialistas Dev. Se retiran exclusivamente siete archivos SKILL.md previamente administrados por VX: vx-evolution-core, vx-self-improvement, vx-security-review, vx-architecture-decisions, vx-codebase-investigation, vx-supply-chain-review y vx-accessibility-review. Sus directorios, archivos extra y código versionado quedan intactos; un backup DPAPI conserva los originales.

**No tocar:** kilo.jsonc, MCP, modelos, credenciales, AutoApprove, skills de terceros, agentes inline externos, rutas de proyectos, bases de datos o otros archivos de nombres desconocidos. Si hay colisiones en fuentes externas, bloquear y reconciliar en vez de borrar.

## Un solo procedimiento de instalación en Windows

**No instalar hasta que el PR haya pasado CI y revisión y esté integrado a main.** Utilizar PowerShell 7 externo. En D:\Proyectos\Kilo-Global-Harness, con git limpio y main sincronizada:

### 1. Preflight sin escritura

    pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Diagnostico
    pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Simular

La respuesta debe indicar READY, 18 agentes y 46 skills, sin bloqueos ni cambios a configuración. Revisar el número de archivos a retirar antes de confirmar.

### 2. Aplicación

Cerrar previamente VS Code, VSCodium y Kilo Desktop (y sesiones que estén modificando la configuración). El instalador verifica que main coincide con origin/main y que no hay cambios locales.

    pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Aplicar -ConfirmarInstalacion -ConfirmarRetirarVXLegacy -ConfirmarKiloCerrado

Crear respaldo DPAPI CurrentUser, verificar que puede descifrarse y comprobar los archivos antes de escribir. El motor instala archivos con escritura atómica y retira solo nombres de la allowlist legacy declarada. Ante un fallo intenta rollback conservador, sin eliminar directorios.

### 3. Verificación y pruebas funcionales

    pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Verificar

Verificar que el resultado declara SOURCE_FILES_MATCH_RUNTIME_NOT_VERIFIED. Reiniciar Kilo y comprobar en la interfaz/CLI que hay un líder visible, 17 subagentes ocultos, skill loading real y task efectivo. Probar lectura Explorer, un builder con permisos ask en fixture aislado, editorial y revisión independiente; no usar datos ni infraestructura reales.

### 4. Restauración

Guardar la ruta absoluta de BACKUP DPAPI impresa al instalar, **no compartirla ni subirla a GitHub**. Con Kilo cerrado:

    pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Restaurar -CarpetaRespaldo RUTA_REAL_BACKUP -ConfirmarRestauracion -ConfirmarKiloCerrado

El rollback rechaza sobrescribir archivos modificados desde la instalación; investigar y recuperar de forma dirigida, no forzar.

### Instalación interrumpida antes de confirmar INSTALLED

Si hubo un corte de energía o un error de PowerShell tras crear un respaldo DPAPI, el recibo puede quedar en `BACKED_UP` aunque algunos archivos se hayan actualizado. La restauración normal **rechaza** ese estado; usar recuperación extraordinaria, explícita y con Kilo cerrado, **con la ruta real de ese respaldo**:

    pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Restaurar -CarpetaRespaldo RUTA_REAL_BACKUP -ConfirmarRestauracion -RecuperarInstalacionInterrumpida -ConfirmarKiloCerrado

La recuperación verifica para todos los destinos la allowlist de archivos administrados, el respaldo DPAPI y los hashes `before/after`. Si un archivo tiene un tercer valor inesperado, **se detiene sin sobrescribir**: conservar el respaldo y revisar el conflicto manualmente. Nunca aplicar esta opción para omitir colisiones o modificar archivos ajenos.

### Skills de terceros y colisiones de identidad

El preflight comprueba el ID tanto del directorio como del campo `name` del frontmatter de cada skill externa bajo `~/.kilo/skills`, `~/.agents/skills`, `~/.kilocode/skills` y `~/.claude/skills`. Una skill ajena cuyo archivo esté en otro directorio pero declare un nombre del Core provoca `BLOCKED`. No se elimina ni renombra automáticamente la skill externa.

## Política operativa de menor burocracia

Para tareas ordinarias el líder determina automáticamente Git root, branch, SHA y archivos por inspección. No exigir formularios ni tickets manuales si el entorno es suficiente. Elegir el mínimo de especialistas; el líder puede resolver tareas sencillas sin delegar. Los seis implementadores pueden editar proyectos con consentimiento de Kilo; no se convierten en modos principales.

Conservar salvaguardas necesarias: no elevar ACL por falta de herramienta, un escritor por worktree, no producción ni cambios destructivos sin autorización, no publicar ni fusionar sin evidencias, no declarar runtime PASS solo por hashes iguales.

## Changelog

- V1.0 RC1 (2026-11-20): 18 agentes únicos, 43 skills seleccionadas, un solo instalador reversible, seis agentes y siete skills históricas retirables, pruebas de instalación/rollback en suite viva; source aún no equivale a runtime instalado.

## Comandos compatibilizados (V1.0 RC1)

La instalación única gestiona también tres comandos globales: **/vx-equipo**, **/vx-dependencias** y **/vx-editorial**. Sus rutas apuntan al único líder `vx-dev-team`; los dos primeros ya no invocan al antiguo `vx-integrador`. El comando experimental histórico `/vx-p2` se retira del HOME con respaldo DPAPI porque seleccionaba directamente a `vx-docs-builder`, que ahora debe ser subagente oculto. El fuente `commands/vx-p2.md` permanece versionado para trazabilidad. Los demás comandos del usuario se conservan, sin borrados por nombre o coincidencias amplias.

**Inventario final bajo gestión del instalador:** 18 agentes, 46 skills, 3 comandos y un bloque de política global VX. Se pueden retirar exactamente seis agentes, siete skills y un comando históricos, si existen; todo el material anterior cambiado se respalda antes de mutar. La existencia de otros comandos o recursos ajenos no convierte su funcionalidad en certificada.

- V1.0 RC1 ajuste de seguridad: recuperacion explicita de respaldo `BACKED_UP` y bloqueo de colisiones por `name:` en skills ajenas globales; casos negativos agregados a la suite viva.

## Integración DAG e inline (corrección RC1)

El instalador único distribuye además **dos archivos de soporte** sin abrir otra instancia: `~/.config/kilo/harness/scripts/vx_task_dag.py` y `~/.config/kilo/harness/vx-unified-pack-v1.json`. `/vx-dependencias` llama al validador con `--registry` apuntando al registro unificado, no al registro histórico; el script admite también el formato legacy solo para compatibilidad, sin activar agentes retirados.

Si `kilo.jsonc` define en línea a cualquiera de los seis agentes legacy retirables (por ejemplo `vx-integrador`), la simulación devuelve `BLOCKED`: eliminar el archivo Markdown no elimina un agente inline. **No editar automáticamente `kilo.jsonc` ni deshabilitar configuración del usuario**; resolver esa colisión por el procedimiento de gestión explícito del host, con respaldo independiente. Comprobar la ausencia del segundo líder antes de aplicar el instalador.

**Inventario completo administrado:** 18 agentes, 46 skills, tres comandos, dos archivos de soporte y un bloque global de política. El número máximo de archivos legacy retirables sigue siendo 14 (seis agentes, siete SKILL.md y un comando); otros recursos globales no se eliminan.

## VX-RT-02C — Contrato adaptable para builders (V1.0.1)

**Evidencia:** en Kilo Desktop Windows, el operador configuró el modo Auto. VX-RT-02A mostró `apply_patch` realizado por el líder; no certifica escritura del builder. VX-RT-02B devolvió `NO_CHANGE_NEEDED`, sin tarea de escritura. VX-RT-02C invocó a `vx-frontend-builder`, pero este devolvió `BLOCKED` por exigir metadatos de Git no proporcionados para un laboratorio no Git. La inspección local confirmó `VX_RT02C_FILE_NOT_CREATED`. Estos resultados son runtime, no un defecto de `ask` demostrado.

**Corrección de source:** para los seis builders ocultos y las skills de colaboración/handoff, el contrato obligatorio se hace proporcional. Para un proyecto Git real, comprobar HEAD/branch, alcance de mutación, dependencias y un escritor por worktree. En un laboratorio local aislado sin Git, autorizado explícitamente por el operador con archivo y contenido exactos, declarar `GIT_NOT_APPLICABLE` sin inventar SHA/branch ni crear un repositorio Git artificial. El ID de tarea puede inferirse; no bloquear por metadatos opcionales si el objetivo y la ruta están identificados. El modo Auto del host no equivale a ampliar ACL; escrituras siguen siendo `ask` en source. Se mantiene la protección de secretos, producción, rutas fuera de alcance y múltiples escritores.

**Ensayo focalizado tras actualización global:** el operador comprobará primero que el archivo `vx-rt02c-frontend-builder.html` sigue ausente; invocará al líder `vx-dev-team` para asignar por `task` la creación exacta de ese único archivo al hijo `vx-frontend-builder`; no puede escribir el líder ni añadir herramientas de escape. La certificación exige evento `Created`/`Edited` dentro de la transcripción del hijo y comprobación independiente del contenido; si el host deniega escritura, `TOOL_UNAVAILABLE`/`BLOCKED_PERMISSION`. No repetir pruebas si la precondición dejó de cumplirse. No crear nuevos archivos de test en el repo; ampliar la suite viva `tests/test_vx_unified_pack_v1.py`.

**Estado:** código propuesto hasta PR/CI/revisión/merge, actualización local del operador y evidencia de Kilo Desktop. No reclamar `BUILDER_WRITE_PASS` antes de esas pruebas.


## VX 1.1 — Motor Desktop preferido: Tauri 2

Para **nuevas aplicaciones de escritorio**, el motor propuesto por defecto es **Tauri 2**, con frontend HTML/CSS/TypeScript y núcleo nativo Rust. Se incluye la skill complementaria `vx-tauri-desktop` (44 skills en total), que se carga únicamente cuando existe una tarea de aplicación desktop, desde builders autorizados por su propia ACL; no convertir Tauri en requisito de toda aplicación web.

**Delegación por especialidad:** Frontend Builder desarrolla pantallas y estado UI; Backend Builder implementa Rust/commands y validación IPC; Data Builder participa solo si hay almacenamiento local y migraciones reales; QA Builder cubre pruebas Rust, frontend y smoke Windows cuando las herramientas estén disponibles; Editorial/Docs se convocan según necesidad. El líder puede lanzar frontend y Rust en background si sus archivos son disjuntos. `src-tauri/tauri.conf.json`, capabilities, `Cargo.toml`, lockfiles, los puntos de registro y los artefactos generados se integran por un solo dueño después de la barrera. No permitir builds compartidos concurrentes sobre `target/`.

**Prerrequisitos y seguridad:** comprobar versiones de Rust MSVC, WebView2, C++ Build Tools, Node/package manager e IPC/capabilities reales antes de compilar. Aplicar permisos mínimos por ventana y scopes, no activar shell/FS remotos ni publicar instaladores/actualizaciones sin petición. Para proyectos existentes en Qt/PySide/Electron/otros, mantener tecnología salvo solicitud expresa de migración tras evaluación de compatibilidad y coste.

**Fuentes oficiales:** https://v2.tauri.app/concept/architecture/ · https://v2.tauri.app/security/capabilities/ · https://v2.tauri.app/start/prerequisites/

## VX 1.1 — Delegación paralela de Kilo Desktop sin convertirlo en VS Code

### Evidencia técnica y límite del host

Kilo Desktop se apoya en el motor CLI de Kilo. Según la documentación oficial de Kilo, `task` permite `background: true`: una tarea independiente continúa en una sesión hija mientras la sesión padre sigue trabajando. El resultado llega después. **Esto debe verificarse en la versión concreta de Kilo Desktop del operador; SOURCE no es RUNTIME.**

**No equivale a Agent Manager de VS Code:** `task` hereda el mismo directorio/worktree; no crea una rama o checkout aislado. `agent_manager` permanece denegado. Swarm/Board no se habilitan automáticamente ni se requiere para que `task` devuelva resultados.

Documentación del proveedor:
- https://kilo.ai/docs/automate/agent-manager
- https://kilo.ai/docs/customize/custom-subagents
- https://kilo.ai/docs/desktop/overview

### Protocolo del líder

1. Dividir la petición en contratos de resultados independientes y dependientes, **sin delegar por ritual**. Un simple arreglo puede resolverlo el líder.
2. Determinar estado Git (incluido `GIT_UNBORN_HEAD`), permisos y rutas exactas. Asignar dueño por archivo y separar los cambios de archivos comunes (config, imports centrales, package-lock, tests/snapshots compartidos).
3. Para subtareas que no dependen unas de otras, el líder usa realmente `task(background: true)` si aparece en la tool. **Máximo 4** background activos y **máximo 2** subagentes escritores. Si la tool no admite background, usar foreground y declararlo, sin simular paralelismo.
4. **Por defecto un escritor por worktree.** En un mismo workspace pueden trabajar dos builders simultáneamente **solo** con `write_scope: EXACT_FILES`, listas `allowed_paths` literales y totalmente disjuntas, permiso de edición efectivo, sin escrituras sobre archivos compartidos y sin ninguna operación Git concurrente. Para cambios solapados, serializar. Para ramas/commits independientes, usar worktrees Git reales **verificados**, no suponer que `task` los abrió.
5. Mientras los hijos trabajan, el líder puede analizar otros módulos, preparar contrato estable, revisar material ya terminado y delegar lectores independientes. No editar ni leer como definitivo un archivo todavía en escritura; no duplicar la tarea por falta de respuesta.
6. Esperar finalización real, inspeccionar diff/rutas del hijo, comprobar pruebas y pedir revisión independiente según riesgo. El líder integra en un **punto de sincronización**; no hacer commits/PR antes de esa barrera.
7. Si se corta una sesión, `HOLD_RECHECK`: comprobar el estado real antes de reanudar por `task_id` recuperable. No reiniciar a ciegas ni reescribir archivos de otro hijo.
8. Mantener Kilo Desktop **Auto** como lo eligió el operador, sin cambiar permisos, modelos, MCP, `kilo.jsonc` ni HOME para conseguir concurrencia.

### Planificador DAG (no despachador)

El soporte instalado `scripts/vx_task_dag.py` conserva el `mode: STRICT` original y añade el opt-in `mode: PARALLEL_SAFE`. Lee únicamente un JSON local explícito; valida dependencias, rutas literales y capacidades declaradas. No usa red, no ejecuta agentes ni reserva archivos.

Ejemplo de **dos implementaciones independientes** sobre el mismo workspace, editando archivos exclusivos y sin operaciones Git simultáneas (ejemplo ilustrativo, sustituir nombres/paths por el código real):

```json
{
  "schema": "vx-task-plan/1",
  "mode": "PARALLEL_SAFE",
  "max_background_tasks": 4,
  "max_parallel_writers": 2,
  "allow_shared_worktree_exact_files": true,
  "tasks": [
    {
      "id": "api-catalog",
      "owner": "vx-backend-builder",
      "reviewer": "vx-dev-reviewer",
      "state": "PENDING",
      "writer": true,
      "worktree": "workspace-actual",
      "write_scope": "EXACT_FILES",
      "allowed_paths": ["src/backend/catalog.py"],
      "depends_on": []
    },
    {
      "id": "ui-profile",
      "owner": "vx-frontend-builder",
      "reviewer": "vx-dev-reviewer",
      "state": "PENDING",
      "writer": true,
      "worktree": "workspace-actual",
      "write_scope": "EXACT_FILES",
      "allowed_paths": ["src/frontend/profile.tsx"],
      "depends_on": []
    }
  ]
}
```

El resultado `background_candidates` propone tareas paralelas, `parallel_deferred` explica bloqueos y `file_lease_proposals` enumera el ownership declarado. Los indicadores `file_leases_enforced: false`, `worktree_identity_verified: false`, `background_tool_verified: false` y `actions_executed: 0` **no cambian** al recibir un plan válido: el host y el líder deben demostrar la ejecución real. En modo compartido, una ruta glob, un solapamiento padre/hijo o ausencia de opt-in bloquea el segundo escritor. El DAG no certifica si las instrucciones del hijo se cumplen; el líder coteja cambios reales al terminar.

### Validación runtime focalizada (una sola vez)

En laboratorio aislado existente y **sin modificar instalaciones adicionales**, proponer dos tareas de edición de archivos sintéticos distintos con aceptación conocida y sin dependencia. Abrir en Kilo Desktop el líder `vx-dev-team`; verificar en el historial que se iniciaron dos hijos con `task(background: true)` y que el líder realizó una tercera actividad independiente mientras estaban activos. Comprobar los eventos de escritura dentro de cada hijo, que ninguna ruta se superpuso y que el padre esperó la barrera antes de probar. Si no se observan sesiones solapadas, registrar `BACKGROUND_RUNTIME_NOT_VERIFIED` y seguir operando foreground; **no crear más pruebas decorativas**.

### Changelog

- **V1.1 RC1 (2026-11-21):** delegación `task(background: true)` condicionada al host de Kilo Desktop, parent-work-while-children-run, dos writers con archivos exactos y disjuntos, DAG `PARALLEL_SAFE` plan-only, barrera de integración, fallback foreground y tests ampliados en la suite viva; ACL y AutoApprove intactos.


## VX 1.2 — Contrato de aplicaciones hermanas Windows y Android (Tauri 2)

**Política nueva:** cada **aplicación de escritorio nueva** de este equipo se diseña para **Windows `.exe` y Android `.apk`**, con núcleo, protocolo, modelos de negocio y tests compatibles, y UI diferenciada por plataforma. `.aab` se reserva a Google Play cuando se solicite. Si falta el toolchain o el hardware, no se cancela silenciosamente el target: registrar `PLATFORM_BLOCKED` con causa verificable y dejar las tareas/artefactos pendientes. Esta política no migra proyectos anteriores (Qt/PySide/Electron/industrial) sin encargo expreso.

### Responsabilidades y empaquetado

- **Líder:** mantiene contrato funcional único, mapas de UX Windows/Android, esquema de datos, ownership exacto por archivo y barrera de integración.
- **Frontend:** usa UI compartida con adaptaciones para ratón/teclado/ventanas Windows y táctil/orientación/safe areas/teclado virtual/back Android.
- **Backend Rust:** comandos locales Tauri, servicio Windows de enlace LAN y cliente Android usando contrato versionado de red. No confundir IPC interno con conexión PC–móvil.
- **Data:** modelos, sincronización incremental, migraciones y conflictos solo si el producto los requiere.
- **QA:** pruebas focalizadas de `.exe` y `.apk`, navegación táctil, permisos, IPC, pairing, cifrado, desconexiones, revocación y LAN sin Internet con dos dispositivos físicos. Tests simulados no certifican enlace Bluetooth.
- **Editorial/Docs:** textos y procedimientos de emparejamiento, instalación, permisos, errores y soporte.

Para ambos targets comprobar Rust MSVC/C++ Build Tools/WebView2 y Android Studio/SDK/NDK/JDK/targets Android según versión real. Comandos orientativos con la CLI instalada: `pnpm tauri build` para Windows; `pnpm tauri android build --apk` para Android; `--aab` solo si corresponde. No confundir ejecutable, instalador y paquetes firmados. Versionar artefactos/hashes cuando **existen**; no incluir llaves privadas ni certificados de firma en Git.

### Comunicación local por Wi-Fi / Bluetooth

1. **Preferido: Wi-Fi LAN/hotspot sin Internet.** Servicio nativo Rust en Windows para comunicación autenticada, cifrada y bidireccional; Android cliente por WebSocket/HTTPS. Descubrimiento mDNS/DNS-SD opcional con fallback de IP/QR manual. Pairing con QR temporal, confirmación física en PC, identidad propia por móvil y revocación. Sin abrir WAN/UPnP/firewall automáticamente.
2. **Wi-Fi Direct:** Android ofrece APIs nativas de P2P, pero Windows y sus drivers pueden no soportar el mismo enlace. Requiere verificación de hardware, adaptadores y permisos (incluido `NEARBY_WIFI_DEVICES` para APIs correspondientes en Android 13+). Un hotspot puede mantener el mismo canal LAN como alternativa más práctica.
3. **Bluetooth:** distinguir Bluetooth Classic y BLE/GATT; el plugin comunitario `tauri-plugin-blec` es **cliente** y no implementa de forma automática el periférico/servidor GATT. Exige roles compatibles, adaptadores nativos Rust/Kotlin cuando sean necesarios y permisos de cercanía (`BLUETOOTH_SCAN`, `BLUETOOTH_CONNECT` en Android 12+ según funcionalidad). BLE no es canal predeterminado para grandes transferencias; si no se probó, estado `BLE_NOT_VERIFIED`.
4. **Seguridad:** TLS con identidad autenticada, tokens por dispositivo/expiración, protección ante replay, rate limits, validación del protocolo y revocación. Sin credenciales hardcodeadas, sin deshabilitar verificación TLS y sin exposición pública por defecto. Reintentos idempotentes y reconciliación visible de conflictos offline.

### Plugins del catálogo oficial: incluir solo lo necesario

Fuente solicitada: https://v2.tauri.app/es/plugin/ y compatibilidad por plataforma en https://v2.tauri.app/plugin/.

- **Conectividad:** `websocket` (cliente, no servidor), `http-client` (cliente HTTP opcional), `deep-linking` (invitaciones) y `barcode-scanner` (QR Android cuando corresponda).
- **Datos y seguridad:** `sql` (datos estructurados), `store` (preferencias no sensibles), `stronghold` (secretos solo tras validar versión/soporte), `file-system` (scopes mínimos), `log` (sin tokens).
- **UX de plataforma:** `dialog`, `notifications`, `os-info`, `haptics`, `biometric` y `nfc` solo si los flujos requieren sus funciones.
- **Excepciones:** `localhost` expone assets locales y no crea un servidor de dispositivos; `shell` no debe habilitarse para ganar conectividad. Plugins comunitarios BLE/red requieren auditoría de licencia/soporte/seguridad.

Ni catálogo ni skill instalan plugins por su sola existencia. Las capacidades de Tauri se habilitan por ventana, plataforma y scopes mínimos mediante cambios autorizados. Las tareas independientes pueden ir en `task(background: true)` si la herramienta real de Kilo Desktop lo permite; dos escritores máximo sobre archivos exactos disjuntos y un responsable de archivos compartidos `tauri.conf.json`, Cargo/JS locks, capabilities, AndroidManifest y registro IPC.

### Gate real de entrega dual

El cierre del producto requiere un reporte separado de `windows_status`, `android_status`, `lan_pairing_status`, `ble_status` y `wifi_direct_status`, con estado `BUILT/TESTED/BLOCKED/NOT_EXECUTED` según evidencia. Para declarar un enlace seguro y sin Internet se necesitan dos dispositivos reales, pairing confirmado, intercambio bidireccional y prueba de desconexión. Si no hubo teléfono físico ni compilación Android, la tarea sigue **parcial** aunque el build de Windows pase.

**Referencias verificadas:** https://v2.tauri.app/distribute/google-play/ · https://v2.tauri.app/distribute/windows-installer/ · https://v2.tauri.app/plugin/websocket/ · https://v2.tauri.app/security/capabilities/ · https://developer.android.com/develop/connectivity/wifi/wifi-direct · https://developer.android.com/develop/connectivity/bluetooth/bt-permissions · https://github.com/MnlPhlp/tauri-plugin-blec

**Estado:** implementación documental/políticas/source del pack; **aún no certifica APK, EXE, BLE, Wi-Fi Direct o enlace LAN real** en el PC del operador.

### Changelog

- **V1.2 RC1 (2026-11-21):** skill `vx-tauri-desktop` v1.1.0, dos targets Windows/Android por defecto para nuevas apps de escritorio, selección fundamentada de plugins Tauri 2, conexión Wi-Fi LAN/hotspot local-first, Bluetooth/Wi-Fi Direct condicional, protocolo seguro de pairing y QA/entrega dual sin pruebas ficticias.


## VX 1.3 — Habilidades independientes y selección explícita de plataforma

La **elección de Tauri depende de que el proyecto se haya especificado como Desktop**; no es framework obligatorio para ERP web, API, sitios, scripts u otras plataformas. Para nuevas aplicaciones de escritorio el contrato puede incluir Windows + Android según el alcance del producto, con UI y capacidades por plataforma y bloqueos explícitos si falta el SDK/hardware.

El pack mantiene 18 agentes y añade dos skills bajo demanda, para un total de **46** (18 CORE + 28 complementarias):
- `vx-conectividad-dispositivos`: guía transversal a frameworks para LAN, servicio Rust, WebSocket cliente, QR/pairing, DNS-SD, Bluetooth BLE/GATT y Wi-Fi Direct, con detección de hardware y permisos Android 17 `ACCESS_LOCAL_NETWORK`. No instala plugins.
- `vx-desarrollo-escalonado`: permite al líder conservar `FINAL_GOAL`, base real, PLATFORM_SCOPE, entregas por etapas y una sola hoja de ruta viva. La ACL `skill` del líder agrega únicamente este ID, sin cambiar escritura/MCP/Auto.

Guía práctica de qué añadir **solo por proyecto** y cómo validar dependencias/etapas: [VX Desarrollo Escalonado y Conectividad](VX-DESARROLLO-ESCALONADO-CONECTIVIDAD-V1.md). El catálogo Tauri no incorpora por sí mismo servidor Rust ni conexión Bluetooth completa. Prohibido afirmar que se compilaron EXE/APK o que el enlace es seguro sin pruebas físicas y artefactos.

### Changelog

- **V1.3 RC1 (2026-11-21):** Tauri solo para proyectos explícitos Desktop; conectividad independiente del framework con fases/diagnóstico y dependencias condicionales; meta final, fases, gates, Android 17 LAN y 46 skills. Sin instalación ni permisos globales nuevos.
