# VX Team — Colaboración por capacidades y handoffs entre Frontend, Backend y QA V1

**Fecha:** 2026-11-19 · **Versión:** 1.0.0 · **Estado:** SOURCE PLAN_ONLY. No está conectado todavía al runtime de Kilo.

## Decisión

El equipo no debe generar tareas a partir de cada commit, ni mantener una rama «de Frontend» eterna. **Una rama temporal por tarea**, máximo un escritor por worktree, y reconciliación con `main` en cuanto avance. Al integrar una funcionalidad que modifica un contrato compartido, el coordinador produce un evento `CAPABILITY_HANDOFF` **solo para dominios realmente dependientes**. Se prioriza terminar un flujo vertical completo sobre multiplicar agentes.

```text
Backend implementa API → PR + CI + revisión → merge confirmado a main
          ├── MAIN_ADVANCED → reconciliación de otras ramas activas
          └── CAPABILITY_HANDOFF(api_to_ui, regression)
                    ├── Frontend Builder: adaptar interfaz sobre su rama actual, o proponer work/* nueva
                    └── QA Builder: actualizar test focalizado cuando esté listo el contrato

Frontend implementa interacción → PR + CI + revisión → merge a main
          └── CAPABILITY_HANDOFF(ui_to_api, regression) → Backend Builder (+ QA)
```

Si una rama ya está `ACTIVE`, generar **`RECONCILE_THEN_EXTEND_EXISTING`** para su agente responsable: no crear una rama duplicada. Si está en revisión o trabajando en una reconciliación, `PAUSE_AND_RECHECK`; ante múltiples propietarios, bloquear el plan entero. Si no existe trabajo compatible, proponer una rama `work/*` **para esa nueva tarea** sin crearla automáticamente.

## Publicación verificable de capacidad

El productor aporta la declaración `vx-capability-publication/1` con `repo`, `main_sha`, `capability_id`, `producer_domain`, `operation`, `contract_ref`, `change_impacts` y `allowed_paths` por consumidor. No generar contratos de API o ubicaciones UI inexistentes mediante heurísticas; el implementador comprueba el código y la evidencia del PR antes de editar. Una descripción escrita por el propio agente **no acredita** por sí sola autenticación, permisos ni que el contrato exista.

Ejemplo orientativo del caso «Backend añade eliminar registro» (rutas ficticias: sustituir por las reales del proyecto):

```json
{
  "schema": "vx-capability-publication/1",
  "repo": "organizacion/proyecto",
  "main_sha": "<SHA real del merge>",
  "capability_id": "records.delete.v1",
  "producer_domain": "backend",
  "operation": "delete",
  "contract_ref": "src/api/records.ts",
  "change_impacts": ["api_to_ui", "regression"],
  "allowed_paths": {
    "frontend": ["src/components/records"],
    "qa": ["tests/records"]
  }
}
```

El Frontend Builder recibe criterios concretos: verificar método/ruta y payload/respuestas de la API en `main`, autorización y alcance del dato, confirmación antes de eliminar, estados loading/error/disabled/success, invalidación o refresco de la vista, accesibilidad y botón situado conforme al diseño real. **Nunca inventar que el botón está ya publicado ni ejecutar una eliminación productiva durante pruebas.**

En la dirección contraria, una capacidad UI que requiere API nueva usa `producer_domain=frontend` y `change_impacts=["ui_to_api","regression"]`: Backend verifica necesidades, define e implementa el endpoint autorizado, y QA cubre el contrato. Si se necesita un diseño de API previo, la tarea no debe improvisarlo fuera de scope.

## Selección proporcional del equipo

| Magnitud | Activación máxima propuesta | Criterio |
| --- | --- | --- |
| SIMPLE | 1 implementador y revisión según riesgo | Cambio localizado, una única dependencia |
| MEDIA | Hasta 2 implementadores simultáneos, en worktrees distintos y autorizados | Dos dominios afectados |
| COMPLEJA | Hasta 2 escritores simultáneos; consultores de seguridad, calidad y UX solo si aportan evidencia | Operación destructiva, tres dominios o varias invariantes |
| EXCEPCIONAL | No se despacha; dividir y aprobar antes | Fanout excesivo, propietarios ambiguos o alcance incompleto |

El enrutamiento se basa en **impactos declarados** y `MAIN_ADVANCED_VERIFIED`, no en invocar todos los agentes por cada cambio. Idempotencia por `repo/main_sha/capability_id/role`; no crear tests decorativos: `TEST_ACTION=UPDATE/REPLACE/ADD` con justificación. Los handoffs son dependencias en una cola, no una nueva jerarquía de subagentes ni permiso para trabajo lateral.

## Escritura acotada y permisos

El coordinador `vx-dev-team` puede implementar por sí mismo mediante `edit/write/apply_patch/bash: ask`, y existe ya el grupo VX de **builders** para código real: `vx-frontend-builder`, `vx-backend-builder`, `vx-data-builder`, `vx-qa-builder` y `vx-docs-builder`. Esta fase propone `write: ask` y `apply_patch: ask` **solo en source** de esos implementadores, preservando `"*": deny`, `task/agent_manager: deny` y `bash: deny` donde ya corresponde. Los diez especialistas `runtime/dev-team-v2r/agents` permanecen read-only.

Un ticket especifica `allowed_paths` y `task_id` pero **no convierte la lista en sandbox real**. Para escribir deben coincidir autorización de proyecto, rama, worktree, owner, herramientas efectivas y aprobación del host Kilo; si la herramienta está ausente, en `deny` o la sesión no puede pedir `ask`, devolver `BLOCKED_PERMISSION`. No usar otro MCP/shell ni promover a lector para eludirlo. Fuente instalada/ejecutada/certificada son estados distintos; ninguna ACL se instaló en HOME en esta fase.

**Dependencia de la issue #86:** solo `MAIN_ADVANCED_VERIFIED` y la inspección real de ramas pueden preparar la tarea; la cola SQLite actual es exclusivamente de sandbox. **No existe listener/dispatcher activo que cree botones automáticamente.** Futura activación requiere consentimiento separado, validación de permisos host y gate #81; la protección de `main` corresponde a #91.

## Ciclo cerrado

1. Identificar tarea, alcance, contrato y productor; una sola rama temporal por tarea.
2. Implementar la capacidad, tests focalizados y revisión independiente.
3. Integrar a `main` con CI real, confirmar SHA.
4. Emitir `MAIN_ADVANCED` y propuesta de `CAPABILITY_HANDOFF` para dominios relacionados.
5. Cada consumidor pausa en punto seguro, reconcilia su rama, verifica contrato, solicita permiso host y programa implementación en su propio worktree.
6. Validar integración vertical completa; QA prueba contra fixture o servicio de prueba, no contra producción.
7. PR/CI/revisión/merge de cada consumidor; el nuevo `main` vuelve a notificar dependientes si corresponde (sin bucles duplicados).
8. Archivar/eliminar solamente la rama cerrada, sin afectar trabajo de otros agentes.

**Certificación actual:** fuente y planificador puro, con pruebas integradas en `tests/test_vx_dev_team_consolidation_v1.py` y `tests/test_vx_agent_permissions_v02.py` (UPDATE). No se certifica sincronización en tiempo real ni generación de UI ejecutada.
