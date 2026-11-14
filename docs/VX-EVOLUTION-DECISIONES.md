# VX Evolution — Decisiones y dudas de dirección

**Fecha de registro:** 2026-11-14. **Ámbito:** exclusivamente Kilo Code, todos los proyectos, almacenamiento operativo global en HOME. Esta tabla separa decisiones expresadas por el usuario de propuestas técnicas que todavía necesitan aprobación.

| ID | Decisión / duda | Estado | Propuesta y efecto |
| --- | --- | --- | --- |
| VX-D01 | Solo Kilo Code; no Codex, Claude ni otros harnesses | **CONFIRMADA** | Comandos, skills, APIs y hooks únicamente globales de Kilo |
| VX-D02 | Memoria/registro de trabajo independiente del repositorio | **CONFIRMADA** | SQLite en HOME; referencias a proyectos seudónimas, nunca bases por proyecto |
| VX-D03 | Reunión semanal y cierre mensual global | **CONFIRMADA** | Los dos tipos existen en contrato; ejecución automática aún no implementada |
| VX-D04 | En las reuniones el usuario revisa y aprueba propuestas | **CONFIRMADA** | Los agentes solo proponen; V4.3 no implementa decisiones |
| VX-D05 | Día/hora y zona horaria de reunión semanal | **PENDIENTE** | Sugerencia: día fijo semanal, horario de Windows configurable; no imponer |
| VX-D06 | Día/regla de cierre mensual | **PENDIENTE** | Alternativas: último día hábil o primer día hábil siguiente |
| VX-D07 | Política de retención y borrado | **PENDIENTE** | Propuesta: observaciones detalladas 90 días, agregados y decisiones con histórico versionado; no borrar nada hasta definir |
| VX-D08 | Única PC Windows o varias instalaciones Kilo | **PENDIENTE** | Una sola PC permite SQLite local sin sincronización; multi-PC requiere otro diseño |
| VX-D09 | Captura de tareas automática y nivel de detalle | **PENDIENTE DE DISEÑO** | V4.4: plugin global ligero, eventos de cierre/fallo; nunca volcar cada tool call |
| VX-D10 | Identidad y mecanismo para registrar aprobación | **PENDIENTE DE DISEÑO** | Revisión explícita en sesión vs interfaz dedicada; no deducir aprobación del silencio |
| VX-D11 | Condiciones para ascenso, contratación, fusión y jubilación de agentes | **PENDIENTE** | Métricas reales, auditor independiente, evaluación negativa y rollback |
| VX-D12 | Reconciliar 11 agentes compartidos y 19 limites steps altos | **PENDIENTE DE EJECUCIÓN** | Mantener auditor V4.2 como pista paralela sin modificar configuración privada |

## Invariantes confirmados

1. Una sola rama temporal de trabajo y `main` permanente.
2. Configuraciones Kilo/skills/agents y datos operativos exclusivamente en HOME.
3. AutoApprove no se cambia; no implica conceder más permisos.
4. Los agentes no aprueban ni publican sus propios cambios.
5. Evidencia y revisión previa a modificar skills, agentes, dependencias o jerarquías.
6. No usar documentación externa no auditada como instrucciones ejecutables ni almacenar secretos/proyectos privados en GitHub.

## Alcance de V4.3 frente a fases futuras

**Implementado en el código fuente:** SQLite schema v1, inventario Kilo global, observaciones explícitas, propuestas `pending_review`, hashes, backup manual, agenda `meeting-preview`, comandos y skill de gobierno, test Windows.

**Pendiente:** instrumentación automática de todas las tareas (V4.4), calendario/notificaciones y decisiones persistidas (V4.5), evaluación/autocapacitación y jerarquías (V4.6), publicación versionada y rollback de componentes (V4.7).

No confundir una tabla vacía `meetings` o `decisions` con una función de reuniones ejecutada. El motor V4.3 no debe arrancar servicios residentes sin autorización.

## Política de revisión

Antes de V4.4 recoger respuestas a VX-D05–VX-D09. Antes de V4.5 concretar VX-D10. No bloquear la preparación de infraestructura global, pero tampoco tomar decisiones organizativas sensibles por defecto.

## Riesgos que revisaremos de nuevo

- Captura de información de proyectos, datos personales y secretos.
- Duplicación de observaciones de subagentes; familias semánticas aún no implementadas.
- Acoplamiento con hooks o plugins existentes de Kilo, incluidos task-observer y descubrimiento de modelos.
- Calidad de métricas cuando Kilo no reporte tokens/costo.
- Corrupción SQLite, apagones, migraciones y backups.
- Sesgos en evaluaciones que podrían promocionar agentes mediocres o retirar especialistas útiles.
