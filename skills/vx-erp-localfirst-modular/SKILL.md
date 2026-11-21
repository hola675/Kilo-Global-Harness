---
name: vx-erp-localfirst-modular
description: "Diseñar ERP y sistemas administrativos modulares local-first: dominio, perfiles de despliegue, SQLite/PostgreSQL, sincronización resiliente, multitenancy y contratos contables."
metadata:
  version: "1.0.0"
  origin: "vx-unified"
---

# VX — ERP modular y local-first

**Activación por tipo de problema:** ERP, inventario, compras, RRHH, multi-sede, facturación autorizada, gestión de talleres o prestación de servicios. No copiar arquitectura de otro ERP por referencia funcional; estudiar baseline y gates reales. El objetivo es un **core coherente y modular**, no microservicios o herramientas por moda.

## Diseño

- Definir Domain Core, Foundations (identidad, auditoría, configuración), capacidades transversales, módulos de vertical/nicho, conectores y localizaciones como límites explícitos. Separar entidades, servicios, contratos y UI.
- Seleccionar perfil de despliegue del producto: cloud/web, single-site local, multisede/offline, HA empresarial. SQLite local y PostgreSQL central/site son candidatos, no elecciones universales. Para Desktop, **Tauri 2 es el motor preferido en nuevas implementaciones**, sujeto a pruebas de compatibilidad y a reglas explícitas del proyecto; un motor existente no se migra silenciosamente.
- Sincronización: identificar autoridad de cada dato, UUID, idempotencia, cola/reintentos, última escritura y conflictos, timestamps/versiones, rebase de esquema y fencing. **No** resolver ventas/stock/pagos con last-write-wins sin evaluar invariantes.
- Seguridad: tenants/sites y roles; cifrado de secretos, sesiones por dispositivo, ledger auditable y segregación de funciones; datos reales quedan fuera de tests sin permiso.
- UX: paneles por rol, tareas habituales, modo desconectado visible, estados de sync, errores de negocio y accesibilidad. No inventar módulos, reglamentos o flujos específicos no confirmados.
- Pruebas: contratos de dominio, importaciones, migraciones, redundancia, funcionamiento offline, recuperación, prohibición de doble ejecución de órdenes; perfil de despliegue correcto en cada entorno.

## Trabajo por fases

Primero diagnóstico/objetivo y vertical slice pequeño; después estabilizar contratos de módulos y perfilar sync; solo luego escalar nichos y sedes. Evitar convertir hipótesis arquitectónicas en decisiones definitivas sin benchmark o gate de preimplementación. Con dos writers en archivos exactos disjuntos, coordinar schema, migraciones, lockfiles y config bajo un único owner en barrera.

**Entrega:** avance funcional medido por capacidades verificadas y riesgos abiertos, nunca porcentajes inventados.
