---
name: vx-tauri-desktop
description: "Diseñar y desarrollar por defecto un par Tauri 2 Windows (.exe) + Android (.apk) con lógica compartida, UI adaptativa, plugins mínimos y conectividad local segura Wi-Fi/BLE/Wi-Fi Direct condicionada a compatibilidad."
metadata:
  version: "1.1.0"
  origin: "vx-unified"
---

# VX — Tauri 2: aplicaciones hermanas Windows + Android

**Contrato vigente:** cuando el usuario solicite una NUEVA aplicación de escritorio, el equipo propone y desarrolla **dos versiones compatibles del mismo producto: Windows (`.exe`) y Android (`.apk`)**. No limitarse a una web responsive dentro de un instalador. Ambas comparten el dominio y el protocolo, pero **las pantallas y los controles se diseñan expresamente para cada dispositivo**. Si un requisito físico, licencia, hardware o regulación hace imposible una de las plataformas, registrar `PLATFORM_BLOCKED` con evidencia y alternativa; nunca fingir un ejecutable/APK compilado. Para un producto ya implementado en Qt/PySide/Electron/tecnología industrial, no migrar ni añadir Android silenciosamente sin petición de evolución/migración del producto. Este contrato **no se aplica a páginas web, APIs ni plugins de Kilo**.

## Entrega dual obligatoria (nuevos productos)

1. Una sola línea funcional/versionado y contratos compartidos: modelo de dominio, reglas, validaciones, protocolo de emparejamiento, DTO/JSON Schema, errores tipados, migraciones compatibles y tests de contrato. Preferir **un workspace de producto y dos targets de Tauri 2**; compartir Rust y TypeScript cuando sea viable y separar las diferencias por plataforma. No imponer dos repositorios, ni duplicar lógica por defecto.
2. **Windows:** comprobar Rust toolchain MSVC, Microsoft C++ Build Tools, WebView2 y gestor JS reales. Compilar y entregar el `.exe` de la aplicación y, cuando se requiera distribución instalable, NSIS `.exe` o MSI `.msi`; documentar ruta/hash, arquitectura, firma e instalación solo cuando el artefacto exista. Comando orientativo (con CLI del proyecto): `pnpm tauri build`.
3. **Android:** comprobar Android Studio/SDK/NDK/JDK, variables y targets Rust para Android; preparar `tauri android init` cuando aplique y crear APK con `pnpm tauri android build --apk` (sintaxis exacta según CLI instalada). Añadir `.aab` únicamente para distribución Play cuando corresponda. El APK no equivale al AAB ni a una publicación. No generar claves privadas ni registrar secretos de firma en Git. Registrar ABI, minSdk y ruta/hash si se compiló.
4. **Paridad del producto:** equivalencia de identidades, reglas, permisos de negocio, operaciones esenciales, formato de datos, protocolo y semántica de errores; no clonar píxel por píxel la UI Windows en Android. Diseñar un sistema de diseño común con variantes `desktop` y `mobile`: en Windows sidebar, tablas densas, atajos, multi-ventana; en Android navegación inferior, pantallas estrechas, controles táctiles, teclado virtual, áreas seguras, accesibilidad, orientación y botón Atrás. Todos los flujos principales deben ser utilizables sin ratón.
5. **Modo local-first:** ambas versiones pueden seguir trabajando sin conectividad con almacenamiento local controlado y estados `DISCONNECTED / DISCOVERING / PAIRING / CONNECTED / SYNCING / CONFLICT / ERROR`. La ausencia de Internet NO debe impedir por defecto operar en la misma LAN; no prometer sincronización en segundo plano cuando Android la restrinja.

## Conexión entre el PC y el móvil: una arquitectura, varios transportes

**Prioridad A — Wi-Fi LAN / hotspot, sin Internet:** si Windows y Android comparten red local o hotspot, ejecutar un **servicio nativo local y autenticado en Windows** (Rust, fuera del WebView/servidor de assets). Android se conecta como cliente sobre WebSocket/HTTPS *bidireccional* con un contrato versionado. El plugin oficial `tauri-plugin-websocket` ofrece **cliente** WebSocket multiplataforma, NO crea por sí mismo servidor, descubrimiento de pares ni emparejamiento. Servidor: Rust con biblioteca revisada (p. ej., tokio/axum/tungstenite) solo cuando el producto lo necesite. Ofrecer descubrimiento mDNS/DNS-SD bajo demanda y alternativa manual IP/QR; comprobar cortafuegos de Windows, aislamiento de clientes del router, IP variable y subredes. Escuchar solo interfaz local autorizada, con puerto restringido; no abrir WAN, UPnP ni puertos del sistema automáticamente. `127.0.0.1` de cada dispositivo es **su propio dispositivo**.

**Prioridad B — Wi-Fi Direct / hotspot sin router:** Android tiene APIs Wi-Fi P2P para descubrir/conectar equipos, pero **el soporte del adaptador, Windows, drivers y permisos puede impedir el enlace con un PC concreto**. No asumir que es el mismo Wi-Fi LAN o que cualquier equipo permite P2P. Si Wi-Fi Direct bilateral no resulta viable, ofrecer hotspot de Windows/Android y usar el **mismo protocolo LAN autenticado** como transporte. Este modo exige integración Android nativa Kotlin/plugin si las APIs disponibles no llegan desde el frontend.

**Prioridad C — Bluetooth:** modo alternativo **condicionado**, no equivalencia automática a LAN. Distinguir Bluetooth Classic/RFCOMM frente a **BLE/GATT**; elegir según cantidad/frecuencia/tamaño de mensajes y roles cliente/periférico realmente soportados por ambos dispositivos. Para BLE se puede evaluar el plugin **comunitario** `tauri-plugin-blec` (cliente BLE para Windows y Android), pero **un cliente no implementa el periférico/servidor GATT** del otro extremo. Validar API, mantenimiento, licencia, versión, roles, hardware y pruebas en dos dispositivos físicos; cuando haga falta, desarrollar adaptadores nativos Rust/Windows + Kotlin/Android. BLE no es transporte por defecto de archivos grandes, altas tasas ni sincronización masiva. Si no hay soporte verificable, marcar `BLE_NOT_VERIFIED` y continuar con LAN/hotspot; no afirmar Bluetooth operativo ni instalar plugins de terceros sin revisión.

**Aislamiento entre capas:** la mensajería **entre dispositivos** es un transporte de red/BLE; `tauri::command` es IPC **interno** entre frontend y Rust del mismo dispositivo. No confundir ambos, ni usar eventos de Tauri entre ventanas como red remota. `tauri-plugin-localhost` expone ASSETS en localhost y advierte riesgos; **no es un servidor peer-to-peer para Android**.

### Emparejamiento y seguridad mínimas

- Emparejar por decisión explícita del usuario: PC muestra QR/código **efímero** con identificador/fingerprint y endpoint local; móvil solicita conexión, PC confirma identidad/dispositivo y ambos establecen credenciales **únicas por dispositivo**. Permitir revocar, renovar y desvincular. Proteger contra replay, abuso de descubrimiento y enrolamiento inesperado.
- Tráfico autenticado **y cifrado** (TLS/WSS con validación real del servidor y, donde corresponda, pinning/certificado propio validado en pairing). No confiar en IP/mismo Wi-Fi/QR como autenticación permanente; no desactivar verificación TLS ni usar tokens fijos hardcoded. Si no hay transporte seguro implementado, limitar a prototipo y declarar `SECURE_PAIRING_NOT_IMPLEMENTED`, sin publicar servicio productivo.
- No meter contraseñas ni tokens en QR persistente, URL de logs, commits o mensajes. Guardar secretos mediante almacén seguro comprobado por plataforma (Stronghold u OS keychain/Keystore tras validación), nunca Store/SQL en texto claro para credenciales.
- Aplicar controles de autorización **en Rust y en el servidor local** a cada comando/operación: permisos por rol/dispositivo, schemas, límites de payload, rate limits, expiración de sesiones, privacidad de eventos, TLS y cortafuegos mínimos. En Android pedir únicamente permisos realmente utilizados; documentar `BLUETOOTH_SCAN`/`BLUETOOTH_CONNECT` (Android 12+) y `NEARBY_WIFI_DEVICES` (Android 13+ para APIs de dispositivos cercanos), con compatibilidad de versiones anteriores y consentimiento. No solicitar ubicación o acceso de red amplia por comodidad.
- Protocolo versionado `hello/capabilities/pair/command/event/ack/error` con `request_id`, `device_id`, `schema_version` y `correlation_id`; reintentos idempotentes, ACK, deduplicación, sincronización incremental y reconciliación de conflictos visible. Nunca duplicar órdenes peligrosas automáticamente al reconectar.

## Catálogo oficial de plugins: seleccionar por necesidad, no activar todos

Basarse en el **catálogo oficial** https://v2.tauri.app/es/plugin/ y en la tabla de plataformas del plugin elegido en la versión fijada del proyecto. La ficha oficial puede cambiar; comprobar Windows/Android, versiones Rust, permisos/capabilities, scopes y APIs antes de añadirlo.

| Plugin / función | Uso previsto en el producto dual | Decisión y precaución |
| --- | --- | --- |
| `websocket` | Cliente Android/Windows de comunicación LAN bidireccional | Recomendable si existe servidor Rust; **no es servidor ni descubrimiento** |
| `http-client` | Peticiones de control REST/HTTPS local al par | Opcional; scopes de red y validación TLS reales |
| `store` | Preferencias no sensibles y UX local | No almacenar claves, secretos o tokens sin cifrar |
| `sql` | Datos relacionales estructurados/offline, cola sincronización | Añadir si hay esquema/consultas; versionar migraciones |
| `stronghold` | Custodia local de secretos si el uso/versiones son compatibles | Evaluar cifrado, política de claves y soporte por target |
| `barcode-scanner` | Escanear QR de pairing desde Android | Permisos de cámara cuando se usa; no activar por defecto |
| `deep-linking` | Abrir el flujo de invitación/emparejamiento | Validar parámetros y evitar tokens reutilizables |
| `dialog`, `notification`, `os-info` | Diálogos y estado nativo por plataforma | Respetar diferencias Android/Windows y permisos |
| `file-system`, `opener`, `upload` | Importar/exportar archivos o transferencias autorizadas | Scopes estrictos; no convertir a acceso global al disco |
| `log` | Diagnóstico del enlace sin secretos | Nunca registrar contenido sensible, token o QR completo |
| `geolocation`, `biometric`, `haptics`, `nfc` | Sensores/UX específicos del móvil | Solo si los flujos lo requieren, con fallback en PC |
| `localhost`, `shell`, `updater` | Casos especializados | **No** son sustitutos del servidor par; revisar riesgos, soporte móvil y consentimiento |
| Comunidad `tauri-plugin-blec` | BLE/GATT como cliente, cuando sea viable | **No oficial**, no sustituye servidor GATT; auditar antes de instalar |

No inferir que el catálogo es un API universal ni que cada plugin vale para todas las plataformas. No instalar plugins, ejecutar comandos de instalación, elevar permisos, habilitar capacidades, abrir puertos o modificar AndroidManifest sin tareas explícitamente autorizadas.

## Trabajo en equipo y concurrente: líder único

- **`vx-dev-team`**: contrato del producto, mapa de pantallas y flujos Desktop/Mobile, matriz Windows/Android, API de dominio y protocolo entre dispositivos, ownership y barrera de integración.
- **`vx-frontend-builder`**: componentes/diseño común + variantes de interacción Windows/Android, responsive real, estados sin conexión y pairing. Es dueño de los archivos exactos UI asignados.
- **`vx-backend-builder`**: dominio Rust, comandos Tauri y servidor/cliente LAN, validación, autenticación y transporte; interfaz tipada estable para Frontend. Evita dar por hecha una API nativa Android inexistente.
- **`vx-data-builder`**: solo cuando hay almacenamiento, migraciones y sincronización local-first real.
- **`vx-qa-builder`**: pruebas de contrato, Rust/TypeScript, e2e Windows y Android físicos, desconexión/reconexión, redes/seguridad y build/install de `.exe` y `.apk`; no declarar PASS de dispositivos no probados.
- **`vx-editorial-builder`** y **`vx-docs-builder`**: lenguaje claro de conexión/permisos/errores y guía de instalación/emparejamiento.
- Paralelismo Kilo Desktop **solo** si `task(background: true)` existe en el host; máximo dos escritores sobre **archivos exactos disjuntos**. `tauri.conf.json`, `Cargo.toml`, `Cargo.lock`, `package.json`, lockfiles, `src-tauri/capabilities/`, `src-tauri/gen/android/`, configuración de firma, registradores IPC y puerto/servicio compartidos tienen un **único dueño en la barrera**. No simultanear cambios de rama ni builds sobre `target/`.

## QA y entregables: no simular dos versiones

**Matriz mínima:** UI desktop ratón/teclado, UI Android táctil vertical/horizontal, IPC Rust↔TS en ambos, LAN bidireccional entre **dos dispositivos reales**, pairing/revocación, conexión rota/reconexión, red sin Internet, permisos denegados, compatibilidad de esquemas, datos locales, conflictos, seguridad y BLE/Wi-Fi Direct **solo si están implementados**. Construir con herramientas realmente disponibles: Windows `pnpm tauri build`; Android `pnpm tauri android build --apk` (CLI equivalente del proyecto). Para Play `--aab` si se solicita; firma/distribución solo cuando se autoricen. Verificar `cargo fmt --check`, `cargo check`, `cargo test`, tests frontend, `tauri dev` y `tauri android dev` cuando estén soportados y ejecutados.

**Salida obligatoria por versión y conexión:**

`{windows: {status: BUILT|TESTED|BLOCKED|NOT_EXECUTED, exe_path, installer_path, hash}, android: {status: BUILT|TESTED|BLOCKED|NOT_EXECUTED, apk_path, aab_path, hash}, ui_parity, ipc_contract, lan_pairing_status, ble_status, wifi_direct_status, plugin_matrix, permissions, test_evidence, unresolved_risks}`

**No declarar "dos versiones listas", "Bluetooth funciona" ni "sin Internet comprobado" sin artefactos y pruebas reales.** Cuando falte toolchain o un dispositivo, seguir con código y contratos aprobados, registrar `BUILD_BLOCKED_BY_ENVIRONMENT`/`HARDWARE_NOT_VERIFIED` en ese target y no fabricar resultados. Las apps existentes y los sistemas industriales conservan sus restricciones.

## Fuentes primarias revisadas

- Catálogo y tabla de compatibilidad: https://v2.tauri.app/es/plugin/ y https://v2.tauri.app/plugin/
- Build Android APK/AAB: https://v2.tauri.app/distribute/google-play/
- Windows: https://v2.tauri.app/distribute/windows-installer/
- Android prerequisitos: https://v2.tauri.app/start/prerequisites/
- WebSocket (cliente): https://v2.tauri.app/plugin/websocket/
- Permisos/capabilities: https://v2.tauri.app/security/capabilities/
- Plugins móviles nativos: https://v2.tauri.app/develop/plugins/develop-mobile/
- Wi-Fi Direct Android: https://developer.android.com/develop/connectivity/wifi/wifi-direct
- Bluetooth Android: https://developer.android.com/develop/connectivity/bluetooth/bt-permissions
- BLE comunitario (auditar): https://github.com/MnlPhlp/tauri-plugin-blec

Una skill no añade nuevas tools, no garantiza acceso al hardware y no modifica automáticamente la instalación global de Kilo.
