---
name: vx-inventory-reconciliation
description: "Gestionar combustible, almacenes e inventario físico/contable, conciliaciones de TPV externo, asientos, cierres, importaciones y evidencia offline sin crear transacciones inventadas."
metadata:
  version: "1.0.0"
  origin: "vx-unified"
---

# VX — Inventario físico, conciliación y operaciones

**Ámbito genérico:** inventarios de almacenes, combustible, logística, ventas importadas, consumos internos, conciliaciones y cierres. Verificar si el software es **TPV que cobra** o **backoffice que recibe del TPV**; no atribuirle emisión de ventas/pagos sin contrato explícito.

## Modelo y seguridad

- Diferenciar existencia física, titularidad/custodia, ubicación, producto, lote, destino, responsable, período y evidencia documental; los bienes compartidos físicamente pueden pertenecer a terceros.
- Movimientos auditablemente relacionados: recepciones, consumos, transferencias, traspasos en dos patas y cierre. Validar transiciones e invariantes antes de modificar stock; tener clara fuente de autoridad en cada punto.
- Conciliar comprobantes externos mediante referencias y deduplicación; importación no equivale a cobro. Evitar el doble conteo, cambios silenciosos de titularidad y ajustes de inventario sin autorización.
- Soporte offline/local-first: SQLite temporal para tests, cola y exportación de cierres firmados cuando exista infraestructura comprobada; estado «sin sincronizar» visible. No afirmar criptografía o firma no implementada.
- UX por rol/sitio y contexto operativo; mostrar unidades, moneda, fechas y errores sin ambigüedad. Los ejemplos de precios, combustible o proveedores son sintéticos y no saldos oficiales.

## Colaboración

Data/Backend define ledger y comprobantes; Frontend diseña consulta/edición conforme a guardias; QA cubre idempotencia, invariantes, diferencias de cierre, devolución, rollback y datos ajenos; Docs/Editorial mantiene terminología común. Un solo dueño del schema y migraciones en la barrera. **No utilizar bases reales, pagos o integración externa para pruebas** sin permiso.

**Entrega:** entradas/salidas verificadas y límites de operación, no declaraciones de homologación sin aprobación institucional.
