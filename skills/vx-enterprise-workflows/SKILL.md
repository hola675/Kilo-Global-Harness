---
name: vx-enterprise-workflows
description: "Modelar gestión documental estructurada, planes, acuerdos, aprobaciones escalonadas, informes, RRHH, auditoría y dashboards empresariales por roles."
metadata:
  version: "1.0.0"
  last_modified: "2026-11-21"
  origin: "vx-unified"
---

# VX — Procesos empresariales, flujos y seguimiento

**Activación técnica:** coordinación corporativa, actas, acuerdos, indicadores, RRHH, planes, reportes, expedientes, aprobaciones de varios niveles o integración con ofimática. No convertir el sistema en almacén de Word/Excel sin datos estructurados.

## Patrones reutilizables

- Convertir formularios y documentos en entidades nativas: tipo, emisor, responsable, estado, plazo, versión, evidencia y trazabilidad; los archivos originales son anexos, no estado del proceso.
- Separar flujos configurables y sus contratos (trabajador/jefatura/dirección/organismo superior como ejemplo, no regla obligatoria): cada transición valida autor, rol, dependencia, plazo y políticas de segregación.
- Acuerdos pueden usar los estados `Pendiente, En proceso, Cumplido, Incumplido, Aplazado, Modificado, Cancelado` si el dominio los confirma; añadir historial de decisiones. `(Cumplidos / Total) × 100` exige denominador/período, manejo del total cero y distinción de nuevos/arrastrados.
- Consolidación de información: datos por persona/área → responsables → dirección → informe superior, con versions y cierre inmutable cuando lo apruebe el proceso. No inferir un flujo nacional o jerarquía real sin documentación.
- RRHH requiere privacidad estricta, separación de funciones, control de acceso, retención y auditoría. No generar expedientes, salarios, absentismos ni sanciones ficticias como datos reales.
- Frontend: lista y filtros por rol, recordatorios, trazabilidad de cambios, estados de aprobación inequívocos. QA: transiciones válidas/denegadas, permisos y consolidaciones. Editorial: copy explícito, no ambiguo.

## Integraciones

Mecanismo de intercambio **definido por contrato del proyecto** (eventos, API autorizada, base de integración, archivos); no introducir comunicación directa donde el sistema tenga una separación institucional explícita. No publicar datos de la organización ni activar integraciones sin autorización.

**Salida:** entidades, estados, roles, pruebas verificadas y supuestos pendientes.
