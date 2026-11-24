---
name: vx-industrial-control-safety
description: "Ingeniería de software industrial seguro: controladores, PLC/PCC, compatibilidad de SO/drivers, adaptadores, metrología, operación offline, simulación, integración con ERP y habilitación de pilotos."
metadata:
  version: "1.0.0"
  last_modified: "2026-11-21"
  origin: "vx-unified"
---

# VX — Sistemas industriales con controles y metrología

**Ámbito:** supervisión industrial, controladores PLC/PCC, estaciones de carga/producción, integración corporativa y hardware/sensores críticos. Un prototipo software no prueba seguridad física ni homologación metrológica.

## Orden seguro de trabajo

1. **Inventario y diagnóstico read-only:** modelo exacto de controlador, firmware, buses/protocolos, drivers, licencias, SO, requisitos metrológicos, interlocks, procedimientos de emergencia, ventanas de mantenimiento y responsables.
2. **Arquitectura modular multiinstalación:** adaptadores por fabricante/protocolo, dominio, límites de operación, audit/event log, configuración por emplazamiento y componentes locales resilientes.
3. **Separación de autoridades:** control seguro de planta y la gestión corporativa no deben depender de un API directa si el contrato exige una **base de integración restringida**. Verificar mecanismo concreto; no imponer una arquitectura genérica sobre una interfaz existente.
4. **Simulación aislada:** señales sintéticas, errores, pérdida de red, reintentos idempotentes, validación de órdenes expiradas/duplicadas, estados y alarmas claros. No llamar una simulación «prueba de hardware».
5. **Validación física con gate:** requiere personal competente, permisos institucionales, hardware real identificado, respaldo, operación supervisada y protocolos de parada; sin ello `BLOCKED_PHYSICAL_VALIDATION`.
6. **Producto reutilizable:** perfiles por instalación, adaptación y versionado compatible, controles de riesgo, reversión y planes de despliegue. No sustituir drivers/SO o activar actuadores por mera instrucción de código.

## Equipo

Platform/Architect revisa firmware, drivers y límites; Backend implementa contratos seguros; Data valida audit/integration; QA prueba software aislado y fallos; Editorial/Docs produce instrucciones inequívocas. **Tauri 2 puede preferirse solo para interfaz Desktop nueva si la compatibilidad y las restricciones industriales lo permiten**; no forzar migración de SO, driver o interfaz certificada por preferencia visual.

**Nunca** desactivar interlocks, falsear medición, emular aprobaciones, alterar calibración o ejecutar órdenes reales sin autorización/seguridad. Reportar evidencia y límites en vez de declarar producto certificado.
