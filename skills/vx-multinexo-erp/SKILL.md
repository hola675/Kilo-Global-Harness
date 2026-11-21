---
name: vx-multinexo-erp
description: "Arquitectura y desarrollo de Multinexo – Vecidya ERP modular/local-first, con deployment profiles, sync/tenancy, gates G0 y selección tecnológica basada en pruebas."
metadata:
  version: "1.0.0"
  origin: "vx-unified"
---

# VX — Multinexo ERP modular e híbrido

**Proyecto exacto:** `hola675/Multinexo-Vecidya-ERP`. Independiente de MotoNexo; MotoNexo es **referencia funcional**, no base de código ni arquitectura reutilizable automáticamente. Multinexo no es Vecidya Platform; su futura integración Vecidya/GHL no convierte al SaaS Vecidya en core del ERP.

## Baseline fuente y jerarquía

Antes de implementar: leer HEAD actual de `README.md`, `docs/05-reference/README.md`, `docs/05-reference/DEPLOYMENT-PROFILES.md`, `docs/05-reference/STACK-SCORECARD-V1.md`, `docs/04-quality/PRE-IMPLEMENTATION-GATE.md` y riesgos/ADRs implicados. Estado observado en fuente al redactar: arquitectura candidata V1, **Gate G0 OPEN**, `R-001` Hyperdrive tenant-isolation staging pendiente y S-012 elección de runtime Desktop aún abierta; no inferir aprobación productiva de CI de spikes.

- Capas: Core, Foundations, Capabilities, Domain Extensions, Industry Packs, Localizations, Connectors; Sync, Security, Integration y Product Experience como planos transversales.
- Perfiles: DP-1 Cloud/Web; DP-2 Solo Resilient (Node + SQLite + Site Bridge); DP-3 Multi-Station (PostgreSQL Site Coordinator, workstations SQLite, Sync Policy/fencing); DP-4 Enterprise HA futuro.
- Candidato de datos: PostgreSQL cloud/site, SQLite local, PowerSync como candidato para DP-3; Cloudflare Workers/Hyperdrive edge candidato, **D1 no es almacenamiento ERP primario por defecto**. Protecciones: tenant/site isolation, UUIDv7, fencing, last-stock y strong invariants, migraciones compatibles, recuperación y cifrado local.
- **Motor Desktop:** **Electron lidera un spike**, Tauri 2 es alternativa fuerte; S-012 no había seleccionado ganador definitivo. **No sobrescribir el benchmark ni forzar Tauri por la preferencia genérica del Harness**. Elegir a partir de pruebas Windows reales y necesidades del producto. No exigir Android si el perfil del producto no lo aprobó.
- Modelo inicial: modular monolith first; no multiplicar microservicios ni variantes por nicho antes de demostrar el segundo vertical Retail/Distribution.

## Protocolo por fase

1. Vincular cada tarea al `FINAL_GOAL`, Deployment Profile y riesgo/gate relevante. Si es investigación/spike, entregar evidencia y trade-offs, no producción.
2. Architect/Backend: contratos de aggregate, invariantes y API; Data: autoridad por sitio, migraciones y conflictos de sync; Frontend: tareas por UX; QA: AVS focales y pruebas para el gate afectado.
3. Rutas exactas separadas para writers; ningún cambio concurrente en schema, lockfiles o configuración de bridge. Antes de integrar reconciliar dependencias con S-012/G0 y el HEAD vigente.
4. No afirmar RPO/RTO, tenant isolation, pagos, normativas o sincronización offline prod verificadas sin pruebas de entorno y revisión de seguridad. No tocar datos de tiendas reales ni instalar servicios en LAN empresarial sin autorización.

**Fuentes:** README, deployment profiles, pre-implementation gate, Reference Candidate A, Risk Register y Changelog en el repositorio Multinexo. Esta skill es guía, no permiso de migración.
