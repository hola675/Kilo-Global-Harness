---
name: vx-windows-network-systems
description: "Desarrollo seguro de software Windows con red, proxy, VPN autorizada, SOCKS/HTTPS, firewalls, WFP y drivers: diagnóstico por capas, pruebas reales, firma y rollback."
metadata:
  version: "1.0.0"
  last_modified: "2026-11-21"
  origin: "vx-unified"
---

# VX — Sistemas Windows, proxy y comunicaciones

**Ámbito técnico genérico:** apps Windows con proxy local, VPN autorizada, HTTP CONNECT, SOCKS5, reglas por proceso, Windows Filtering Platform, adaptadores/servicios de red y diagnóstico de salida. No confundir puerto escuchando, tunnel conectado, TLS válido o IP externa verificada. No cambiar firewall, sistema, rutas, DNS, proxy global o drivers por defecto.

## Contratos técnicos

1. Separar **plano de control** (UI, cuentas/permisos, elección de ruta, sesiones) del **plano de datos** (sockets, cifrado, reglas, túnel, tráfico por aplicación).
2. Diagnóstico read-only primero: proceso propietario de puerto, bind loopback, reglas efectivas, upstream, handshake TLS y salida de red. Un HTTP 403 por sí solo no demuestra credenciales erróneas; no registrar correo, contraseña, 2FA o tokens.
3. Si se configura un proxy corporativo explícito, **no hacer fallback directo** a Internet ante su fallo, salvo regla autorizada del producto. Describir con precisión fail-closed y fallback para cada flujo.
4. WFP: bloquear/permitir/redirect por EXE y protocolo, IPv4/IPv6, TCP/UDP/QUIC/DNS; privilegios/driver firmado y ciclo de firma son gates separados. Un kernel callout no firmado o sin test real no se instala ni se considera productivo.
5. UI Desktop: en desarrollos nuevos con alcance Desktop, **Tauri 2 preferido**; preservar stack existente hasta encargo de migración. Cualquier refactor de UI no otorga capacidad del kernel ni acceso a firma.
6. Pruebas por capas: listener local, proxy, TLS, IP de salida, escape/leak, kill switch, limpieza de reglas, rollback tras crash y compatibilidad Windows; exigir entorno aislado al tocar WFP.

**Seguridad y permiso:** usar solo endpoints/servicios controlados o autorizados. Nunca sugerir ocultar tráfico para acceso no autorizado, eludir permisos del host ni instalar controladores sin validación de firma y respaldo. Para red entre Windows/Android usar `vx-conectividad-dispositivos` cuando corresponda; no confundir LAN con VPN pública.

**Resultado:** evidencia verificable por capa y limitaciones explícitas (`DRIVER_UNSIGNED`, `TLS_NOT_VERIFIED`, `HARDWARE_UNAVAILABLE`).
