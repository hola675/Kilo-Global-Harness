# VX — Desarrollo escalonado y conectividad entre Windows y Android (V1.0)

> **Alcance:** guía operativa del Pack Global, no instalador, motor de red ni aplicación ejecutable. Solo usar Tauri cuando el proyecto haya sido definido expresamente como **DESKTOP** y se decida ese motor. En cualquier otro proyecto conservar la plataforma y el framework vigentes. El contrato de pareja Windows+Android se aplica a productos Desktop cuando esa entrega multiplataforma forma parte del alcance acordado; nunca generar APK para páginas web/APIs ajenas.

## 1. Objetivo final y fases reales

**Ejemplo de objetivo final aprobado:** «Una aplicación Tauri para Windows y Android que realiza una operación útil en ambos equipos, empareja el teléfono con el PC, intercambia mensajes bidireccionales sin Internet en la misma LAN y se entrega con EXE/APK verificables». Ajustar al producto concreto y no imponer ese objetivo a otros proyectos.

| Fase | Resultado utilizable | Gate de cierre | Agentes |
| --- | --- | --- | --- |
| 0. Diagnóstico | Sistema actual, requisitos, target Windows/Android, hardware/red, nivel de riesgo y alcance | Baseline Git, plataformas y recursos comprobados | Líder + Explorer si es necesario |
| 1. Arquitectura | Modelo, contrato de mensajes, UI diferenciada y matriz de compatibilidad | API/data/seguridad y dependencias establecidas; no instalar sin autorización | Líder, Arquitectura |
| 2. Vertical slice LAN | Primer envío PC↔Android seguro en red local con IP/QR manual | Prueba física bidireccional, logs sin secretos y validación del protocolo | Backend/Frontend, QA después |
| 3. Emparejamiento y UX | QR temporal, aceptación Windows, identificación, revocación, estados sin conexión | Una operación real con pairing/revocación sin permisos excesivos | Frontend, Backend, Editorial |
| 4. Resiliencia y descubrimiento | mDNS si aporta valor, reconnect, offline sync/ACK/conflictos | Fallo/reanudación real, pruebas de Android 17 target y Wi-Fi/hotspot | Data si se necesita, QA |
| 5. Transportes opcionales | BLE/GATT y/o Wi-Fi Direct donde hardware soporte | Prueba física de ambos roles o `HARDWARE_UNSUPPORTED` / `NOT_VERIFIED`, sin claims engañosos | Platform, Backend, QA |
| 6. Entrega y soporte | EXE e instalador Windows, APK Android, guías y rollback | Artefactos hash/versión, instalación real, pruebas de UI móvil y Windows, revisión/CI | QA, Docs, líder |

**No bloquear las fases 2–4 por Bluetooth:** la vía principal es LAN; BLE/Wi-Fi Direct son extensiones si el producto las necesita. Un sistema completo no es “listo” por tener código sin build y pruebas en dispositivos.

## 2. Qué instalar y dónde — catálogo mínimo revisado

| Componente | Sitio / tecnología | Dónde se añade | Cuándo se justifica | Observación |
| --- | --- | --- | --- | --- |
| Tauri 2 CLI + Rust + Node/pnpm | https://v2.tauri.app/start/prerequisites/ | Entorno de desarrollo por proyecto Desktop | Al desarrollar Tauri explícito | Verificar MSVC, Windows C++ Build Tools y WebView2; no instalar globalmente sin encargo |
| Android Studio, Android SDK/NDK/JDK y ADB | https://v2.tauri.app/start/prerequisites/ | PC de desarrollo para target Android | Si se compila APK/ejecuta teléfono | No es dependencia de la app en producción |
| WebSocket Tauri oficial | https://v2.tauri.app/plugin/websocket/ | Dependencia del proyecto Tauri | Cliente de enlace LAN desde UI | **Cliente**, no instala servidor |
| `axum` + `tokio` + TLS `rustls` | https://docs.rs/axum/ · https://docs.rs/axum-server/ | `src-tauri/Cargo.toml` del proyecto autorizado o crate de servicio | PC necesita recibir órdenes seguras del teléfono | Control de firewall, interfaces, autenticación y versiones; no exponer a WAN |
| `mdns-sd` Windows | https://docs.rs/mdns-sd/ | Rust servicio Windows | Descubrimiento en red local | Fallback IP/QR obligatorio; no confundir discovery con auth |
| `NsdManager` Android | https://developer.android.com/develop/connectivity/wifi/nsd | Plugin nativo Kotlin de Android, según arquitectura | Búsqueda LAN en Android | Revisar permiso de red local y limitaciones del router |
| `tauri-plugin-dns-sd` | https://docs.rs/tauri-plugin-dns-sd/ | Plugin Tauri comunitario **opcional** | Sustituir integración propia tras auditoría | Revisar licencia, mantenimiento, permisos, pruebas Windows/Android; no oficial |
| Barcode Scanner oficial | https://v2.tauri.app/plugin/barcode-scanner/ | Target Android | Escanear QR de pairing | Cámara solo con consentimiento/uso real |
| Plugin BLE cliente `tauri-plugin-blec` | https://github.com/MnlPhlp/tauri-plugin-blec | Plugin comunitario **opcional** del proyecto | BLE si hay adaptador/rol y caso de uso | No aporta GATT server automáticamente; auditar licencias/actualizaciones |
| Windows GATT Server / Android companion APIs | https://learn.microsoft.com/en-us/windows/apps/develop/devices-sensors/gatt-server · https://developer.android.com/develop/connectivity/bluetooth/companion-device-pairing | Adaptadores nativos Rust/Windows/Kotlin | Roles BLE completos y emparejamiento físico | Requiere hardware/driver y permisos; no se resuelve con un plugin JS |
| SQLite / Store / Stronghold | https://v2.tauri.app/plugin/ | Por necesidad, en app local | Datos estructurados, preferencias, secretos según soporte | Store no almacena credenciales en texto plano |
| Wireshark / nRF Connect Android | https://www.wireshark.org/ · https://www.nordicsemi.com/Products/Development-tools/nrf-connect-for-mobile | Herramientas **opcionales de diagnóstico**, fuera del proyecto | Diagnóstico TCP/mDNS o perfiles GATT con consentimiento | No forman parte del APK/EXE; cuidar capturas con datos sensibles |
| VPN/relays (Tailscale, etc.) | Fuera del alcance por defecto | Solo proyecto que requiere **conexión remota entre redes** | Si dos equipos no comparten LAN y el usuario lo pidió | **No necesarios para LAN sin Internet**; no introducir servidor/nube por conveniencia |

Los nombres de paquetes y las versiones exactas deben fijarse **después** de verificar compatibilidad, licencia, actualizaciones y asesoría de seguridad del proyecto. La tabla no autoriza instalar plugins automáticamente ni modificar la configuración del usuario.

### Ejemplos de instalación POR PROYECTO — solo si se decide usar estos componentes

En un proyecto Tauri ya autorizado, con `pnpm` y toolchains previamente instalados:

```powershell
# Desde la raíz de la app Tauri, bajo tarea de implementación autorizada:
pnpm tauri add websocket
# Opcional si el flujo Android usa QR:
pnpm tauri add barcode-scanner

# El servidor Rust va en las dependencias del crate correspondiente:
# cd .\src-tauri
# cargo add axum --features ws
# cargo add tokio --features full
# cargo add axum-server --features tls-rustls

# mDNS solo si se decide descubrimiento automático:
# cargo add mdns-sd
```

**Estos comandos son guía, no fueron ejecutados.** No ejecutar en `Kilo-Global-Harness`: este repositorio solo distribuye instrucciones/skills. El plugin WebSocket podría no satisfacer validación de certificados emparejados; antes de elegirlo para WSS con certificados locales, comprobar TLS, trust store y pinning o implementar cliente Rust con verificación propia auditada. Nunca desactivar TLS para “hacerlo funcionar”.

## 3. Preflight sin instalación y rutas de fallo

Desde Windows, lectura de disponibilidad:

```powershell
rustc --version
cargo --version
node --version
pnpm --version
java -version
adb version
Get-NetAdapter | Select-Object Name, Status, InterfaceDescription
Get-PnpDevice -Class Bluetooth | Select-Object FriendlyName, Status
```

La ausencia de `adb`, Java o Bluetooth produce `MISSING_TOOL` / `MISSING_HARDWARE` y una recomendación condicionada; no implica permisos para instalar, activar ADB, cambiar firewall o modificar sistema. El operador decide la instalación y las versiones.

**Android SDK/versión:** Android 17 (targetSdk 37+) agrega `ACCESS_LOCAL_NETWORK` o selectores del sistema para conexiones LAN; Bluetooth 12+ `BLUETOOTH_SCAN`/`CONNECT`, Wi-Fi Direct Android 13+ `NEARBY_WIFI_DEVICES` según API. No exigir todos los permisos para usar solamente Wi-Fi LAN; pedir el mínimo basado en la función.

**Fallos identificables:** `NETWORK_UNREACHABLE` (no hay ruta), `DISCOVERY_FAILED` (mDNS bloqueado), `PERMISSION_DENIED` (SO), `PAIRING_REJECTED` (usuario), `TLS_INVALID` (autenticación), `PROTOCOL_MISMATCH` (versión), `BLE_UNSUPPORTED` (hardware/rol). Cada error tiene diagnóstico distinto; cambiar de transporte no puede ocultar un defecto de autenticación.

## 4. Skill de escalonamiento y equipo

El líder tiene permitido `vx-desarrollo-escalonado` para conservar `FINAL_GOAL`, `PLATFORM_SCOPE`, etapas y una **hoja de ruta viva**, actualizada después de cada incremento realmente verificado. Los builders pueden cargar `vx-conectividad-dispositivos` solo en tareas de red/apareamiento.

Por defecto trabajar con un único escritor Git por worktree y tareas dependientes secuenciales; dos writers simultáneos solo sobre **archivos exactos disjuntos** con contrato expreso y `task(background: true)` realmente soportado en Kilo Desktop. El líder sigue trabajando fuera de sus archivos. Después del barrier, pruebas focalizadas, revisión independiente, PR/CI y rama temporal archivada/eliminada tras merge verificado.

No crear una suite de test histórica por cada fix: actualizar pruebas vivas y eliminar/retirar el ensayo obsoleto cuando corresponda. El roadmap se mide por **capacidades finales aceptadas**, no por número de agentes, prompts o commits. Sin porcentaje inventado.

## 5. Estado real de esta ampliación

- **SOURCE:** skill Tauri ajustada a Desktop explícito; nueva skill general de conectividad; nueva skill de desarrollo escalonado, reglas del líder, y guía de dependencias.
- **No instalado por este PR:** Rust/Android Studio, plugins de Tauri, librerías Rust, nRF Connect, Wireshark, servicios o herramientas del PC del operador.
- **No certificado por este PR:** compilación EXE/APK, servidores locales, conectividad BLE/Wi-Fi Direct, permiso Android 17, ni herramientas de background en Kilo Desktop.
- **Siguiente gate real:** instalar el pack Global tras CI/revisión/merge; elegir un proyecto Desktop concreto y hacer preflight real para decidir qué dependencias instalar **en ese proyecto**, con control de riesgos y pruebas en Windows + teléfono físico.

## Fuentes

- https://v2.tauri.app/es/plugin/
- https://v2.tauri.app/start/prerequisites/
- https://v2.tauri.app/plugin/websocket/
- https://docs.rs/axum/latest/axum/extract/ws/
- https://docs.rs/mdns-sd/latest/
- https://docs.rs/tauri-plugin-dns-sd/latest/
- https://developer.android.com/privacy-and-security/local-network-permission
- https://developer.android.com/develop/connectivity/wifi/wifi-direct
- https://developer.android.com/develop/connectivity/bluetooth/bt-permissions
- https://learn.microsoft.com/en-us/windows/apps/develop/devices-sensors/gatt-server
