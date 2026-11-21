---
name: vx-octopus-flow-industrial
description: "Arquitectura segura OCTOPUS FLOW para cargaderos de combustible: control local-first, adaptadores industriales, PCC400, metrología e integración limitada por base intermedia."
metadata:
  version: "1.0.0"
  origin: "vx-unified"
---

# VX — OCTOPUS FLOW, software industrial de combustible

**Proyecto distinto de OCTOPUS ENCC y Octopus AI.** Objetivo del operador: sustituir el SO y aplicación de supervisión/gestión del PC PCC400 por OCTOPUS FLOW, conservando compatibilidad y preparándolo como producto modular para múltiples cargaderos; **Base de Combustibles Las Tunas es piloto**, no código específico obligatorio para todos. Este objetivo requiere investigación previa de hardware, drivers, licencias, seguridad funcional y metrología.

## Seguridad y límites físicos

- **Primero inventario y documentación primaria del equipo:** controladores, periféricos, interfaces, firmware, versiones, protocolos, límites seguros, certificaciones y procedimientos de emergencia. No proponer firmware, comandos físicos, sustitución de SO o drivers como hecho verificable sin datos del PCC400 y aprobación industrial.
- Seguridad ante fallo de red: FLOW continúa localmente con estados/alarma/auditoría e interlocks según diseño validado; la indisponibilidad de OCTOPUS ENCC **no** debe bloquear las funciones locales seguras.
- Diseñar arquitectura de adaptadores por fabricante/protocolo (hardware abstraction), orquestador de operación, event log, configuración por instalación, seguridad de identidad, sincronización e integración. **No** codificar lógica rígida dependiente de una sola instalación ni tratar simuladores como hardware certificado.
- Mantener separación de seguridad funcional y comandos de operación. No recomendar saltos de interlocks, alteración de medición, emulación de autorizaciones, deshabilitación de controles o calibración no autorizada.

## Integración institucional

ENCC ↔ FLOW intercambian mediante **base de datos de integración** con accesos restringidos: órdenes, estados, resultados, correlación, idempotencia y auditoría. **No API directa entre ambos**. El desacoplamiento requiere colas/estados transaccionales según contrato aprobado y reintentos seguros; impedir que órdenes vencidas/duplicadas ejecuten acciones físicas.

## Etapas y evidencias

1. **DISCOVERY (solo lectura):** identificar PC, PLC/controladores, versiones, bus/protocolo y requisitos legales/metrológicos; matriz de compatibilidad y riesgos.
2. **CONTRACTS:** módulos y adaptadores, modelos de órdenes/estados, límites y fallos; separar simulación de hardware.
3. **SIMULACIÓN AISLADA:** validar lógica con fixtures y señales sintéticas, rechazo de órdenes no autorizadas y recuperación de fallos.
4. **PILOTO FÍSICO:** solo con permisos de responsables industriales, procedimientos de respaldo, supervisión competente y ventanas de mantenimiento; pruebas reales y cumplimiento metrológico. Sin autorización, `BLOCKED_HARDWARE`.
5. **MULTINSTALACIÓN:** parametrización, compatibilidad por versión, reversión, soporte offline y validación por centro antes de distribución.

## Equipo multiagente

Architect y Platform verifican contratos y compatibilidad; Backend y Data implementan módulos aislados, QA prueba simulaciones; Security revisa límites de red/control industrial y Docs registra decisiones y planes. Editorial redacta alarmas y estados inequívocos. El líder conserva un único camino de autorización para cambios que afecten control físico. **Ningún subagente ejecuta pruebas físicas ni cambia producción por una autorización genérica de edición de código.**

**Estado:** guía basada en decisiones de diseño del operador, no evidencia de que exista SO propio, drivers probados, certificación o runtime operativo.
