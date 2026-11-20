# Dev Team — Pack canónico y reconciliación V1

**Fecha:** 2026-11-19 · **Estado:** `SOURCE_RECONCILED_RUNTIME_NOT_FULLY_VERIFIED`.

Este es el punto de entrada para el Dev Team actual, no una orden de instalación. El registro estructurado es [dev-team-current-pack-v1.json](../registry/dev-team-current-pack-v1.json). Las propuestas originales V1 obsoletas se conservan en el historial Git, no en el árbol de trabajo corriente.

## Inventario y autoridad

| Capa | En source | Autoridad vigente | Estado del operador |
|---|---:|---|---|
| Agentes | 1 líder visible + 10 especialistas ocultos | `registry/dev-team-capability-matrix-v1.json`, `registry/dev-team-readonly-baseline-v2.json` y archivos Markdown | 6/11 hashes idénticos; 5 diferentes |
| Skills CORE V1 | 18 | `registry/dev-team-skills-matrix-v1.proposal.json` | 2/18 hashes idénticos; 16 diferentes |
| Skills Gap Fill V2 | 9 | `registry/dev-team-skills-gap-v2.proposal.json` | NO autorizadas como wave |
| Skills UX/UI Pro | 9 | `registry/dev-team-ux-ui-pro-v1.proposal.json` | NO autorizadas como wave |
| Skills MCP Operations | 8 | `registry/dev-team-mcp-operations-v1.proposal.json` | NO autorizadas como wave |
| MCP | 13 familias | `registry/dev-team-mcp-exact-inventory-v1.json` | 5 IDs documentales certificados; resto no habilitado por esta propuesta |
| Tools nativas/complementos | Propuesta sin activaciones | `registry/kilo-tools-complements-audit-v1.proposal.json` | Inventario runtime por completar |

**44 skills en source no significan 44 skills activadas.** Solo hay allowlists exactas de las 18 CORE en los archivos de agentes. Las skills no conceden por sí mismas ACL adicionales. El alias histórico `playwright` se normaliza como `kilo-playwright` exclusivamente en la documentación de familia; no se cambia ninguna configuración MCP.

## Regla de prioridad

1. **Agentes y ACL:** fuente de roles actual + matriz canónica. No copiar ACL de propuestas históricas.
2. **Skills:** fuentes por capa y `SKILL.md` existentes; las 18 CORE tienen asignación exacta. Las 26 restantes siguen propuestas.
3. **MCP:** inventario canónico por ID observado. Candidatos nunca se convierten en allow automáticamente.
4. **Tools y complementos:** herramientas nativas antes de duplicaciones MCP, sujeto a disponibilidad real del host, pruebas y permiso.
5. **Runtime:** evidencia observada en el Windows del operador. CI/source PASS no afirma instalación funcional.

## Certificación y diferencias locales

El operador aportó un preflight en modo `PLAN_ONLY` con 5 agentes y 16 skills CORE distintos de source, sin archivos faltantes. El origen de esa deriva se investiga con `hash_evidence.*.drift_details` (BOM, EOL, espacios finales o contenido). **Incluso las diferencias de formato continúan bloqueando W1** por su SHA. No se sobrescriben archivos instalados sin estudiar cambios de instrucciones/ACL, backup y aprobación independiente.

El PASS de Dev Team 2.3.0 se emitió para un snapshot anterior: [certificación histórica](VX-DEV-TEAM-230-RUNTIME-CERTIFICATION.md). No se reutiliza para declarar certificación de un source posterior modificado.

Las waves se definen en `registry/dev-team-activation-waves-v1.json` y permanecen bloqueadas por sus gates. La validación de permisos MCP genéricos pendiente está trazada en [issue #81](https://github.com/hola675/Kilo-Global-Harness/issues/81). No se modifica `kilo.jsonc`, ACL runtime, scheduler, MCP o herramientas sin autorización separada.

## Política de eliminación legacy y ramas

Las dos propuestas iniciales `registry/vx-dev-team-v1.proposal.json` y `registry/vx-dev-team-mcp-matrix-v1.proposal.json` describían un conjunto de 13 roles no actual y ACL de diseño, distinto de los 11 roles vigentes. Se retiran del árbol activo y quedan en el historial Git; otros registros históricos conservan trazabilidad y no se eliminan hasta ser sustituidos con evidencia.

Se fusionan cambios exclusivamente vía PR sobre `main`, CI y revisión independiente. Tras el merge, se retiran ramas `work/*` utilizando una operación con verificación SHA y, para las no fusionadas directamente, referencias archivadas recuperables. No eliminar ramas locales que estén asociadas a worktrees o tengan trabajo sin guardar. El borrado de referencias no certifica runtime.

## Cierre seguro de ramas después del merge

Una vez que el CI y la revisión de esta consolidación sean PASS y el merge esté en `main`, el operador puede verificar y eliminar ramas remotas/locales sin perder los commits exclusivos. El script versionado `scripts/Consolidar-Ramas-Main-V2.ps1` **no ejecuta borrados por defecto**:

```powershell
cd D:\Proyectos\Kilo-Global-Harness
git switch main
git fetch origin --prune
git pull --ff-only origin main
pwsh -NoProfile -File .\scripts\Consolidar-Ramas-Main-V2.ps1
```

Inspeccionar el CSV en `$env:TEMP\Kilo-Global-Harness`. El segundo comando requiere aprobación explícita:

```powershell
pwsh -NoProfile -File .\scripts\Consolidar-Ramas-Main-V2.ps1 -Aplicar -Confirmacion ARCHIVAR_Y_LIMPIAR_WORK
```

Antes de cada retiro, el script guarda el SHA del tip en un **tag remoto anotado** `archive/remote/...` (o `archive/local/...`), verifica ese tag y usa `--force-with-lease` para evitar cambios concurrentes. Aborta con PR abiertas, `main` desactualizada o worktree sucio. Git rechaza eliminar una rama usada en otro worktree. Al final comprueba que solo existe la rama `main` tanto local como remota; los tags son historia recuperable, **no ramas activas**. El script puede dejar ramas retenidas si falla una protección y deberá investigarse, sin hacer force manual.

Los tags `archive/*` permiten rescatar commits históricos; no deben ejecutarse como runtime ni considerarse certificados.

## Siguiente paso

Sin modificar tu instalación, sincroniza `main` y ejecuta el preflight. Inspecciona clasificaciones y diffs de los cinco agentes con derivación, especialmente permisos y routing, antes de planear una ola de actualización. Las pruebas `TEST_ACTION: UPDATE` deben residir en la suite actual, no crear duplicados históricos.
