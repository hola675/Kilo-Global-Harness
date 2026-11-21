---
name: vx-conectividad-dispositivos
description: "Diseñar conectividad local segura entre Windows/Android u otros dispositivos usando LAN, QR, mDNS, WebSocket, Bluetooth y Wi-Fi Direct por necesidad, sin presumir compatibilidad ni instalar dependencias automáticamente."
metadata:
  version: "1.0.0"
  origin: "vx-unified"
---

# VX — Conectividad local verificable entre dispositivos

**Activación por necesidad real:** aplicar solo cuando la aplicación debe descubrir, emparejar, sincronizar o comunicarse con otro dispositivo (Windows, Android u otro), **sin exigir Tauri**. El framework del proyecto puede ser Tauri, .NET, Qt, nativo Android, web o servicio Rust; preservar el stack actual. Si la app es local sin enlace, no introducir plugins/red innecesarios.

## Decisión de transporte basada en capacidades

| Perfil | Primera opción | Dependencias/componentes | Limitación y fallback |
| --- | --- | --- | --- |
| Mismo Wi-Fi o hotspot, sin Internet | WebSocket `wss://` o HTTPS seguro, bidireccional | Servidor Rust `axum`+`tokio` con TLS `rustls`/`axum-server` cuando proceda; cliente Tauri `tauri-plugin-websocket` o cliente nativo que valide TLS | Servidor Rust separado del IPC/localhost de assets. Fallback entrada IP/QR |
| Descubrimiento automático LAN | DNS-SD/mDNS | Windows Rust `mdns-sd`; Android `NsdManager`; evaluar `tauri-plugin-dns-sd` **comunitario** si se audita | Multicast/AP isolation y permisos pueden bloquear; ofrecer QR/IP manual |
| Emparejamiento guiado | QR/código temporal + confirmación PC | `tauri-plugin-barcode-scanner` en Android si la UI lo necesita; backend Rust y credenciales por dispositivo | No incrustar credenciales persistentes ni permitir enrolamiento silencioso |
| BLE para pocos datos | GATT Central ↔ Peripheral en hardware compatible | Evaluar `tauri-plugin-blec` **comunitario, BLE cliente**; Windows GattServiceProvider como **servidor** y/o Android nativo Kotlin si hace falta | NO asumir que tener cliente BLE provee periférico/GATT; fallback LAN/hotspot |
| Wi-Fi Direct sin AP | APIs Android WifiP2pManager + adaptador Windows | Plugin nativo Kotlin/Windows solo tras detección real | Compatibilidad bilateral variable; alternativa hotspot y protocolo LAN |
| USB Android↔PC | Solo como diagnóstico/desarrollo con ADB | `adb reverse` si el puerto/entorno lo admite | No entregar ADB/depuración USB como transporte de producción |
| Dispositivos no están en la misma red | Requiere decisión separada de conectividad remota | VPN/relay opcional, con política del producto | No confundir con "sin Internet" ni introducir nube por defecto |

**Verificación de fuente:** https://v2.tauri.app/es/plugin/ · https://v2.tauri.app/plugin/websocket/ · https://docs.rs/axum/latest/axum/extract/ws/ · https://docs.rs/mdns-sd/latest/mdns_sd/ · https://docs.rs/tauri-plugin-dns-sd/latest/ · https://github.com/MnlPhlp/tauri-plugin-blec · https://learn.microsoft.com/en-us/windows/apps/develop/devices-sensors/gatt-server .

## Política de dependencias: no instalar por presencia de la skill

1. **Kit base por proyecto Tauri solo si requiere LAN:** `tauri-plugin-websocket` (cliente), `axum` + `tokio` (servidor Rust); `rustls`/servidor TLS **según arquitectura**. Añadir mediante gestor JS/Cargo del proyecto, después de comprobar versions, MSRV, licencia, CVEs y compatibilidad. Si la app usa Rust nativo, puede preferir un cliente Rust y no necesitar el plugin JS.
2. **Descubrimiento es opcional:** `mdns-sd` Windows y Android `NsdManager` (nativo) o `tauri-plugin-dns-sd` comunitario **solo tras revisión**. Mantener siempre QR/IP de reserva; mDNS no es autenticación.
3. **QR y datos solo cuando se justifiquen:** `tauri-plugin-barcode-scanner` (Android), `sql` para persistencia estructurada, `store` para preferencias no secretas; `stronghold` o almacén OS seguro para claves si el soporte objetivo está probado.
4. **BLE no instalado por defecto:** `tauri-plugin-blec` aporta cliente, no un servidor completo. Antes de incluir, revisar actividad, versión, licencias, permisos, backend Android, adaptador Windows, GATT profile, MTU, fragmentación y reconexión. Puede requerir plugin nativo Android Kotlin y Windows GATT server; si no se verifica, ofrecer alternativa Wi-Fi.
5. **Diagnóstico opcional del operador:** Windows `Wireshark` para observar TCP/DNS-SD sin capturar secretos; Android `nRF Connect` para GATT/BLE con permiso del dispositivo; `adb`/Android SDK para depuración Android. Estas **no son dependencias runtime** de la aplicación y nunca se instalan globalmente sin solicitud explícita.
6. **No instalar bibliotecas o aplicaciones de uso remoto** (VPN, tunneling, cloud relay, firewall automatizado) para resolver un problema de conexión LAN sin diagnóstico y autorización. No abrir puertos WAN/UPnP ni cambiar Windows Firewall automáticamente.

## Seguridad, emparejamiento y red

- Fase de discovery **no confiable**: no asumir que estar en la LAN equivale a permiso. El QR/código temporal ofrece endpoint + identificación efímera/fingerprint, requiere aceptación de usuario en ambos extremos y protocolo criptográfico revisado. No usar pares autoconfiados, secretos fijos, certificados aceptados sin verificación, ni tokens persistentes dentro de QR/logs.
- Usar autenticación mutua de identidad a nivel de aplicación, TLS válido con validación del peer y almacenamiento de claves por dispositivo en mecanismo seguro OS; evaluar pinning **solo con implementación real comprobable**, no asumir que el plugin WebSocket JS permite certificados autofirmados. Cuando no sea posible validar TLS y pairing de manera segura, bloquear producción con `SECURE_PAIRING_NOT_VERIFIED`.
- JSON/CBOR estructurado con versionado, `request_id`, `device_id`, ACK, límites por mensaje, idempotencia y permisos por operación. Reconexion exponencial, deduplicación, colas offline, transacciones y resolución visible de conflictos. Evitar ejecutar órdenes dos veces al recuperar conexión.
- Preferir escucha en una interfaz LAN específica y firewall permitido explícitamente; verificar IPv4/IPv6, DNS, AP/client isolation, hotspot, dirección cambiante y subred. El `localhost` de Android NO llega al PC.
- **Permisos Android por versión:** `INTERNET` cuando se usan sockets; Bluetooth `BLUETOOTH_SCAN/CONNECT` en Android 12+ donde aplique; Wi-Fi Direct `NEARBY_WIFI_DEVICES` Android 13+ y permisos anteriores según API; **`ACCESS_LOCAL_NETWORK` en Android 17 (targetSdk 37+)** para acceso LAN, o APIs mediadas por sistema que lo eviten si proceden. Comprobar en documentación oficial el target SDK, el alcance y el consentimiento. `CompanionDeviceManager` puede servir para emparejamiento cercano con soporte dispositivo, no sustituye autorización de negocio ni cifrado.
- En Windows GATT periferico depende de Bluetooth/driver y soporte `GattServiceProvider`; un PC sin adaptador no hará Bluetooth ni por software ni por Tauri. BLE throughput limitado, no apto por defecto para archivos grandes.

## Secuencia mínima de diagnóstico antes de instalar

A. Identificar objetivo (mensajería, control remoto, sync de datos, archivos), dimensiones/cadencia, operación offline, número de dispositivos, versiones Windows/Android, hardware BT/Wi-Fi, conexión actual, permisos y entorno autorizado.

B. Comprobar red local y conectividad a una IP/puerto autorizado; registrar fallos separados `NETWORK_UNREACHABLE`, `DISCOVERY_FAILED`, `PAIRING_DENIED`, `TLS_INVALID`, `PROTOCOL_MISMATCH`, `PERMISSION_DENIED` o `HARDWARE_UNSUPPORTED`; no colapsar todo en "falla la conexión".

C. Probar primero enlace seguro LAN por IP/QR en dos dispositivos reales; luego descubrimiento mDNS, reconexión, red sin Internet, revocación. Probar BLE/Wi-Fi Direct únicamente tras evaluar capacidad del hardware y autorización.

D. Dependencias elegidas se añaden **solo** al proyecto autorizado, fijando versión, lockfile, permisos Tauri/Android, SBOM mínimo y plan de reversión. Ninguna instalación global, plugin comunitario o cambio de firewall/producción sin permiso.

## Entregable y veredicto

Entregar `{goal, platforms, existing_stack, transport_primary, transport_fallback, components_chosen, third_party_review, android_permissions_by_sdk, windows_capabilities, security_model, files_owned, tests_executed, two_device_evidence, unsupported_transports, installation_proposals, result}`.

Estados por transporte `IMPLEMENTED_NOT_TESTED / CONNECTED_VERIFIED / HARDWARE_NOT_VERIFIED / BLOCKED`. Para declarar `CONNECTED_VERIFIED` exigir intercambio real de ida/vuelta entre Windows y Android, pairing y expiración/revocación, desconexión/reconexión y pruebas sin Internet (si eso era un requisito); no convertir simulaciones en evidencia física.
