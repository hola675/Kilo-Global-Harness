# VX Dev Team · Handoffs por capacidades y contratos

**Estado:** guía operativa del **Core VX 1.6.0-rc1**. No es un segundo orquestador ni un programa de ejecución automática.

## Objetivo

Los cambios entre Backend, Frontend, Datos, QA, Docs y Editorial se coordinan por contratos, no por una nueva rama permanente por departamento ni por un detector de commits. Solo el líder visible `vx-dev-team` distribuye las tareas reales mediante `task`; todos los builders están ocultos y operan bajo sus ACL de escritura `ask`.

## Cuándo generar un handoff

1. Un dominio entrega un cambio **verificado** que afecta un contrato consumido por otro: ruta/payload/errores de API, esquema de datos, formulario, interacción, traducciones o documentación.
2. El líder identifica exactamente los consumidores, el `base_main_sha`, los archivos permitidos, la evidencia y el objetivo aceptable.
3. Publica `CAPABILITY_HANDOFF` en su ledger de sesión o cola SQLite si resulta útil; no hace `task` hasta comprobar dependencias y capacidad.
4. Cuando una dependencia está realmente `VERIFIED`, delega a los builders necesarios. Para cambios independientes, puede usar `task(background: true)` si el host lo admite; máximo cuatro hijos activos y dos escritores con `write_scope: EXACT_FILES` disjunto.
5. Al cerrar, comprueba diff, seguridad, pruebas focales y estado Git. Ni el handoff ni un `board_post` garantizan que el destinatario actuó.

## Ejemplos reales de dependencias

- **Backend → Frontend/QA:** el endpoint ya está verificado; Frontend adapta UI y manejo de estados, QA actualiza pruebas centradas en el mismo contrato.
- **Frontend → Editorial → Frontend:** el builder de UI identifica textos confusos; Editorial revisa claridad sin alterar el significado y Frontend integra la copia verificada.
- **Datos → Backend/QA:** una migración requiere preflight, compatibilidad, respaldo y prueba; nunca ejecutar producción sin autorización explícita.
- **Docs → Editorial:** claridad humana de instrucciones sin confundir ejemplos, borradores o ausencia de acceso con estados de producción.

## Límites

- **Un solo integrador Git por worktree**, `main` única rama permanente, work/* temporal si hace falta y CI/revisión antes de merge.
- `task` no aísla worktrees y Swarm no concede permisos. Un `BLOCKED` con sesión original retiene su reserva hasta un `reset` comprobado.
- El liderazgo, la revisión y el manejo de secretos siguen en [Autopilot V2](VX-DEV-TEAM-AUTOPILOT-V2.md) y [AGENTS.md global](../rules/AGENTS-global-managed.md).
- No usar los antiguos routers de `tools/vx_team_capability_router.py`; fueron retirados del árbol y cualquier comprobación antigua permanece solo en Git history.

**Certificación:** SOURCE/PACK no es HOST_RUNTIME_PASS. Solo se declara colaboración paralela cuando hay llamadas y resultados reales del host.
