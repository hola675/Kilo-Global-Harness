---
name: vx-technology-fit
description: "Evaluar antes de adoptar o cambiar framework, SDK, biblioteca, herramienta, dependencia o integración; preservar stack actual, licencias, compatibilidad y permisos. Tauri 2 se propone solo para nuevo producto Desktop."
compatibility: "Agent Skills; Kilo Code y Kilo Desktop Windows. No instala ni modifica dependencias automáticamente."
metadata:
  version: "1.0.0"
  origin: "vx-unified"
  category: "technology"
---

# VX — Selección tecnológica justificada

**Activar** ante elecciones de stack, nuevas dependencias, integración con hardware/servicios, migraciones o incompatibilidades. No usar para una corrección que no necesita nueva tecnología.

## Inventario inicial

1. Confirmar producto y target aprobados, runtimes, toolchain, SO/CPU, framework actual, manifest/lockfile, licencias, permisos, redes y dependencias de otras aplicaciones; no inferir hardware disponible.
2. Distinguir `EXISTING_STACK`, `PROPOSED_COMPONENT` y `MIGRATION_REQUESTED`. Un proyecto Qt/PySide6, .NET, Electron, CLI o industrial **no cambia de tecnología solo porque existe Tauri**.
3. Seleccionar el problema real: renderizado, empaquetado, transporte, persistencia, seguridad, sincronización, UX, drivers, CI o distribución. Antes de recomendar instalar, verificar si una capacidad nativa o dependencia ya presente basta.
4. Consultar versiones oficiales y soporte en la versión realmente utilizada; si la documentación no es verificable, marcar `UNVERIFIED` y no inventar compatibilidad.

## Matriz de decisión

Comparar opción existente, solución mínima y nueva tecnología mediante `fitness`:

- compatibilidad de plataforma/arquitectura y herramientas de build;
- mantenimiento, versiones soportadas, licencia y vulnerabilidades conocidas con evidencia;
- superficie de permisos, secretos y conexión externa;
- integración y capacidad real de funcionamiento offline cuando se requiere;
- impacto en UI, datos y formatos, consumo CPU/RAM, distribución;
- complejidad y costo de migración frente a valor verificable;
- pruebas disponibles, capacidad de rollback y continuidad del trabajo.

Si la comparación no justifica reemplazar el stack, recomendar **conservarlo**.

## Regla Desktop y conectividad

- **Nuevo producto explícitamente Desktop:** Tauri 2 es opción preferida para evaluar primero, no una obligación irreversible. Confirmar Windows-only o targets adicionales conforme a la solicitud y restricciones. No convertir una API/web en escritorio.
- **Producto Desktop existente:** mantener motor actual, salvo encargo de migración acompañado de análisis de driver, interfaz, empaquetado, datos y riesgos. Una app en PySide6 no tiene por qué reescribirse.
- **Tauri:** cargar `vx-tauri-desktop` solo cuando Tauri ya esté aprobado como motor. No añadir Android por ser Desktop si está fuera del alcance.
- **Red y dispositivos:** usar `vx-conectividad-dispositivos` para elegir LAN, WSS, mDNS, BLE, Wi-Fi Direct, USB u otro **solo si el requisito lo demanda**. Plugins de cliente no sustituyen servidores ni autenticación.
- **Industrial:** ninguna preferencia general reemplaza validación de protocolos, drivers, interlocks, metrología o requisitos operativos.

## Incorporación y reversión

1. Registrar origin/URL, versión, licencia, lock/hash cuando aplique, scopes y motivo técnico.
2. Proponer `ADD|KEEP|REPLACE|REJECT`, superficie afectada, pruebas de compatibilidad y reversión. Revisión adicional si implica scripts de instalación o software no firmado.
3. Solicitar autorización separada cuando la tarea exceda el alcance o eleve privilegios; `propuesta` no equivale a `instalación`.
4. Después de integrar, actualizar manifests, lockfile y documentación **solo** con permisos efectivos; no instalar software global o editar `kilo.jsonc` por recomendación.

## Salida

`{existing_stack,scope,options,verified_versions,licensing,security,fit_matrix,decision,affected_paths,permission_gate,rollback,unknowns}`.

Estados: `FIT_SUPPORTED`, `KEEP_EXISTING`, `MIGRATION_NEEDS_APPROVAL`, `VERIFICATION_REQUIRED`. Ninguno es un PASS de build físico.
