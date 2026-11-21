---
name: vx-tauri-desktop
description: "Usar para desarrollar nuevas aplicaciones de escritorio con Tauri 2, Rust, WebView2 y frontend web. Preferencia de arquitectura VX, sin instalaciones ni permisos implícitos."
metadata:
  version: "1.0.0"
  origin: "vx-unified"
---

# VX — Ingeniería de aplicaciones de escritorio con Tauri 2

**Preferencia vigente:** para una aplicación de escritorio nueva, proponer **Tauri 2** como motor por defecto. **No migrar** silenciosamente un proyecto existente en Qt, Electron, Python o framework industrial; respetar el stack actual o justificar una excepción con requisitos comprobados y decisión del operador. No convertir una web o API en desktop sin petición expresa.

## Activación y responsabilidades del equipo

El líder `vx-dev-team` determina producto/entorno, divide contratos y carga esta skill únicamente en las tareas Tauri. `vx-dev-architect` o `vx-dev-platform` pueden asesorar en solo lectura cuando corresponda; no implementar desde ellos.

- `vx-frontend-builder`: UI en HTML/CSS/TypeScript y framework existente del proyecto (Vite como opción habitual para nuevas SPA). Accesibilidad, estados y ciclo de vida de ventanas.
- `vx-backend-builder`: comandos `#[tauri::command]`, capas Rust, serialización, validación del límite de confianza, integraciones nativas y errores tipados. No exponer shell/FS por comodidad.
- `vx-data-builder`: almacenamiento local, migraciones y transacciones cuando el requisito lo justifique; nunca modificar datos productivos sin autorización.
- `vx-qa-builder`: tests Rust `cargo test`, tests del frontend, pruebas de invocación Rust ↔ TS, Windows/WebView2 y paquete instalable **solo si se ejecutaron**. Evitar suites redundantes.
- `vx-editorial-builder`: microcopy y errores legibles; `vx-docs-builder`: guía de instalación, permisos y operación.
- Revisor independiente según impacto; no invocar todos estos agentes para cambios pequeños.

## Contrato de aplicación Tauri 2

1. Detectar antes de generar nada si el proyecto ya usa Tauri y leer `src-tauri/tauri.conf.json`, `Cargo.toml`, `package.json`, `src-tauri/capabilities/*.json` y los scripts reales, sin suponer versiones exactas. Si es nuevo, usar versión mayor 2 de Tauri y fijar versiones reproducibles desde el registro disponible; no atribuir un minor/patch como último sin comprobar.
2. En Windows comprobar Rust toolchain **MSVC**, Microsoft C++ Build Tools, **WebView2** y herramienta JS/package manager disponibles antes de instalar o compilar. Ninguna instalación automática, descarga de script remoto o elevación de privilegios sin encargo explícito.
3. Usar UI web local y `src-tauri/` Rust nativo con separación clara. Las llamadas del frontend cruzan el IPC mediante APIs oficiales y comandos registrados; validar entradas y autorizaciones dentro del lado Rust. No activar permisos solo porque un plugin esté instalado.
4. Definir capacidades **mínimas por ventana/origen** en `src-tauri/capabilities/`: permitir únicamente comandos y scopes necesarios (archivos, rutas, shell, HTTP, notificaciones). Prohibir permisos wildcard innecesarios, scripts remotos en la WebView y ejecución arbitraria de shell. Revisar CSP de producción, URL remotas y dependencias.
5. Reservar dueños exclusivos de archivos antes de background: frontend solo UI, backend solo `src-tauri/src/` asignado, QA solo tests/fixtures, Docs solo docs. `Cargo.toml`, `Cargo.lock`, `package.json`, lockfile JS, `tauri.conf.json`, `src-tauri/capabilities/`, `build.rs` y puntos de registro son **archivos compartidos**: un integrador los cambia después de la barrera; no permitir dos writers allí. Evitar tests/cargo build simultáneos que compitan por `target/`.
6. Separar tareas con contratos estables: Backend puede construir un comando Rust independiente mientras Frontend prepara la pantalla sin asumir IPC inexistente; el bridge TypeScript y permisos finales se integran tras comprobar comandos reales. Si un componente depende del output de otro, serializar ese tramo.
7. Probar en capas: `cargo fmt --check`, `cargo check`, `cargo test`, typecheck/test del frontend, ejecutar `tauri dev` en Windows y comprobar UI/IPC, después build de instalador mediante CLI (`nsis` o `msi`) según distribución aprobada. Solo reportar resultados observados; si faltan toolchain/WebView2, usar `NOT_EXECUTED` o `BLOCKED`.
8. Seguridad de distribución: no publicar binarios, firmar, actualizar endpoints, activar auto-updater ni desplegar sin petición explícita; si se distribuye en Windows, definir estrategia de firma y WebView2 offline/online apropiada.

**Regla de no regresión:** Tauri es el motor preferido para **nuevas apps de escritorio**, no una reescritura obligatoria de software ya implementado ni un sustituto automático de software embebido/industrial con restricciones de drivers, latencia o certificación metrológica.

## Fuentes oficiales

- https://v2.tauri.app/start/create-project/
- https://v2.tauri.app/start/prerequisites/
- https://v2.tauri.app/start/frontend/
- https://v2.tauri.app/security/capabilities/
- https://v2.tauri.app/security/permissions/
- https://v2.tauri.app/distribute/windows-installer/

## Informe mínimo

`{desktop_engine: "Tauri 2", existing_stack, exceptions, prerequisites_checked, files_changed, ipc_contract, capabilities_scopes, tests_executed, tests_not_executed, packaging_state, reviewer}`.

Una skill ofrece procedimiento, **no concede herramientas, permisos, MCP ni capacidad de iniciar procesos por sí misma**.
