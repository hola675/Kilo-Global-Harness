---
name: vx-kmcero-operaciones
description: "Ingeniería de KMCero El Sendero: control e inteligencia de negocio de combustible, PySide6/SQLite local-first, conciliación TPV externo y transferencia offline segura."
metadata:
  version: "1.0.0"
  origin: "vx-unified"
---

# VX — KMCero, Servicentro El Sendero

**Repositorio:** `hola675/KMCero`. Producto de gestión administrativa/BI local, **NO es un TPV**. El TPV externo cobra ventas (efectivo CUP y transferencias CUP); KMCero recibe/importa comprobantes y cierres ya ocurridos y los concilia. No generar nuevas ventas, facturas ni pagos desde KMCero.

## Verdad de proyecto

Leer `README.md`, `docs/PRODUCTO-Y-OPERACION.md`, `docs/INTERCAMBIO-OFFLINE-Y-SEGURIDAD.md`, `docs/AGENTE-IMPLEMENTACION-PYSIDE6.md` y código/tests del HEAD antes de modificar. La fuente en noviembre 2026 describe v0.5 laboratorio **no homologado** para operación oficial.

- Python >=3.11, PySide6 como interfaz Qt de consulta autenticada y Tkinter legado de laboratorio; SQLite operativo e identidades/sesiones locales separadas. No migrar a Tauri por defecto.
- Tanques físicos, productos, propietarios/custodia (`PROPIO`/`TERCERO`), destino `VENTA` / `INTERNO`, recepciones, consumos, traspasos de dos patas, cuadre y cierres con evidencia. El combustible físico compartido NO implica que la propiedad contable sea común.
- Separar **origen servicentro** de **destino empresa**; los cierres exportados son datos comprobados y firmados/autenticados según mecanismo realmente implementado, no un sistema de ventas distribuido. El importador oficial TPV y transferencia a empresa estaban pendientes.
- La UI Qt es consulta en la baseline; los cambios con mutación requieren guard de servicio, identidad de sitio, autorización de sesión y auditoría. Un acceso directo a SQLite no es prueba de seguridad de la app.
- No incluir precios, tanques, proveedores, responsables o ingresos ficticios como datos oficiales. Los ejemplos deben etiquetarse sintéticos.

## Gates

1. Verificar estado real de `kmcero/`, `pyproject.toml` y tests; no operar con las bases reales de `%LOCALAPPDATA%\KMCero` durante ensayos.
2. Backend + Data: transactions, invariant físico/contable, ledger append-only, importaciones verificadas, deduplicación y conciliación; QA con SQLite temporal y comprobantes sintéticos.
3. Frontend: navegación PySide6 con sesión/rol/sitio, tablas y cierres legibles para personal operativo, UI deshabilitada si no hay permiso.
4. Pruebas focalizadas: `py -3 -m unittest discover -s tests -v` cuando justificado; cambios económicos requieren reversión y reporte de diferencias. No declarar “listo para explotación” sin validación institucional/homologación.

No instalar controladores, introducir pagos automáticos ni exportar datos reales sin autorización del operador.
