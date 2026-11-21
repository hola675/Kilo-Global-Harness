---
name: vx-octopus-encc
description: "Diseño de OCTOPUS ENCC: procesos documentales estructurados, planes, acuerdos, aprobaciones y gestión empresarial con permisos y auditoría."
metadata:
  version: "1.0.0"
  origin: "vx-unified"
---

# VX — OCTOPUS ENCC, gestión estructurada

**Ámbito funcional facilitado por el operador (no inferir código existente):** OCTOPUS ENCC es la plataforma de gestión empresarial de DTCC Las Tunas / ENCC–CUPET. **NO confundir con OCTOPUS FLOW industrial ni con Octopus AI servidor IA**. No se confirmó un repositorio canónico ni un stack productivo en la fuente disponible: antes de implementar leer instrucciones y esquema del proyecto real, sin adjudicar tecnologías, APIs o despliegues inexistentes.

## Entidades y circuitos

- Actividad operativa: informes diarios, reportes económicos, partes de combustible, cumplimiento de planes, RRHH, conciliaciones/cuadres, actas y acuerdos de reuniones, indicaciones nacionales.
- Roles: Dirección, secretarías, jefaturas y trabajadores. Planes anuales/mensuales/semanales e individuales y por áreas; relación entre objetivo, responsable, fecha, evidencia y estado.
- Aprobaciones con estados y cambios **trazables**: trabajador → jefe de área → Director de UEB → instancia nacional, según proceso. Consolidación mensual: trabajador → jefatura → secretarías → Director → Consejo de Dirección → nacional.
- Acuerdos: `Pendiente, En proceso, Cumplido, Incumplido, Aplazado, Modificado, Cancelado`; métricas de total, cumplidos, incumplidos, pendientes/vencidos, % cumplimiento, distribución por área, cambios y arrastre mensual. El porcentaje `Cumplidos / Total * 100` debe indicar denominador y período.
- Capital Humano: plantilla/plazas/cargos, expedientes, contratación y movimientos, asistencia, vacaciones/licencias, nóminas, evaluación, formación, seguridad/salud y disciplina; permisos y privacidad reforzados.

## Diseño y delegación

1. Migrar gradualmente de Word/Excel a **entidades y flujos nativos**; no crear un repositorio opaco de archivos como sustituto. Conservar anexos/actas como evidencia vinculada a registros, con versionado.
2. Backend/Data: modelos de flujo, permisos por rol/área, políticas de segregación, transiciones de estado y auditoría inmutable; ninguna aprobación debe omitirse por acceso a interfaz.
3. Frontend: vistas por rol, listas y filtros, estados y explicaciones claras, seguimiento de pendientes/vencidos, teclado y contraste.
4. QA/Editorial: pruebas de transiciones autorizadas y denegadas, acuerdos arrastrados, cambios de responsables/fechas, consolidación, aclaración de términos institucionales. No inventar cifras reales, expedientes ni datos de empleados.
5. Cuando un área tenga flujos distintos, conservar contratos/versiones y reportar supuestos al líder. No instalar servicios, exponer datos empresariales ni activar conexiones con sistemas nacionales sin autorización expresa.

## Separación con OCTOPUS FLOW

**Único intercambio permitido por la arquitectura propuesta:** una base de datos de integración con accesos restringidos, órdenes, estados, resultados y auditoría. **No** introducir una API directa ENCC↔FLOW sin cambiar expresamente esta decisión. El estado de implementación efectiva de la integración debe verificarse en cada sistema; la definición documental no prueba comunicación operativa.

**Evidencia:** decisiones funcionales proporcionadas en el proyecto OCTOPUS; código/repositorio/roles productivos deben confirmarse antes de declarar STATUS=IMPLEMENTED.
