---
name: vx-onetunnel-wfp
description: "Trabajo seguro en 1VPN-Desktop-Lab / OneTunnel: PySide6/Tkinter, motor WFP nativo, SOCKS5/proxy y driver firmado con verificación fail-closed."
metadata:
  version: "1.0.0"
  origin: "vx-unified"
---

# VX — OneTunnel / 1VPN Desktop Lab

**Repositorio:** `hola675/1VPN-Desktop-Lab`. No es un cliente oficial del proveedor. Respetar `AGENTS.md`, `docs/ROADMAP-QT-V071-V080.md`, `docs/DRIVER-SIGNING-HANDOFF.md` y decisiones/arquitectura en el HEAD actual. No confundir conexión de socket local con salida HTTPS/VPN real.

## Arquitectura comprobada

- Interfaz Qt **PySide6 v0.7 Preview**, con UI Tkinter como fallback hasta certificación; no migrar a Tauri solo por política de otros proyectos.
- Controladores Python/NetworkEngine/Proxy; opciones de salida HTTP CONNECT y SOCKS5 locales; proxy de acceso corporativo activado → **NO fallback directo** si falla; credenciales permanecen en memoria.
- Motor de tráfico por aplicación: componentes nativos Windows Filtering Platform (WFP) para BLOQUEAR / DIRECTO / PROXY; el proxy transparente usa callout de kernel + relay, pero artefacto de CI **UNSIGNED** no se instala ni carga en Windows productivo. El ciclo de firma y certificación debe seguir contratos del repo, sin habilitar servicios/drivers por inercia.
- Seguridad: aislar listeners loopback, no filtrar credenciales/códigos 2FA/tokens ni endpoints privados a Git/logs; DNS/UDP/QUIC/IPv6/kill switch son ámbitos de prueba diferentes. Un 403 no prueba por sí mismo contraseña incorrecta.
- Los proyectos de WFP pueden usar APIs/documentación de Microsoft Learn y tests en un laboratorio Windows aislado; hardware/firmas/certificados requieren autorización separada.

## Equipo y gates

- Frontend: la UI no implementa lógica de red dentro de widgets; estados y fallos claros al usuario (simple por fuera, completo por dentro).
- Backend + Platform: separar proxy de acceso, flujo de autenticación y WFP; nunca crear reglas Firewall permanentes ni cambiar globalmente WinINET, rutas, DNS o Secure Boot sin un alcance explícito.
- QA: probar por capas (listener, SOCKS5, TLS verificado, IP de salida, filtrado por EXE, limpieza transaccional y rollback). No declarar PROXY transparente operable si no existe driver firmado y prueba en Windows real.
- Git: seguir `AGENTS.md` con rama feat/fix/docs, CI Windows y merge solamente con gates verdes; eliminar ramas temporales propias tras verificar merge.

Esta skill no facilita acceso no autorizado a infraestructura de terceros y no concede control del kernel o credenciales.
