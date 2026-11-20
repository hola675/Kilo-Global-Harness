# Auditoría integral del Harness — agentes, permisos, Git y continuidad de equipo

**Corte:** 2026-11-19 · **Ámbito:** árbol source de `hola675/Kilo-Global-Harness`, GitHub API, CI #514 y último preflight aportado por operador. **No** se inspeccionó directamente HOME ni el runtime real Windows en esta auditoría. **Resultado:** `SOURCE_AUDITED_RUNTIME_PARTIAL`.

## 1. Inventario observado

| Superficie | Evidencia de source | Limitación |
| --- | --- | --- |
| Agentes VX | 13 definiciones en `agents/` (incluye líder `vx-dev-team`) | No equivale a 13 roles instalados ni visibles simultáneamente |
| Dev Team | 1 líder + 10 especialistas ocultos read-only en `runtime/dev-team-v2r/agents/` | 10 son definiciones adicionales, no implementadores con escritura |
| Skills VX | 31 `SKILL.md` tradicionales | No equivale a permisos |
| Skills Dev Team | 44 en source: 18 CORE, 9 gap, 9 UX/UI, 8 MCP operations | 26 no autorizadas para activación; 18 CORE con ACL exacta |
| MCP | 13 familias; 5 identificadores documentales exactos verificados previamente | No inferir conectividad efectiva de los demás |
| Validación | `.github/workflows/validar-harness.yml`, living gates, suites source | CI #514 PASS sobre SHA `3ad0e7b`, no certifica HOME |
| Runtime observado por operador | 6/11 agentes y 2/18 skills CORE con SHA exacto | 5 y 16 distintos; W1–W5 bloqueadas |
| Ramas | Previo: 15 ramas `work/*`; tras limpieza: 15 tags archive y una rama `main` | No incluye la nueva rama temporal de esta auditoría |
| GitHub | `main` no protegida, sin rulesets activos; `delete_branch_on_merge=false` | La revisión/CI es práctica, no barrera técnica obligatoria |

## 2. Hallazgos por severidad

### ALTO — Protección de main ausente
GitHub informa `protected=false`, `rulesets=[]` y borrado automático tras PR desactivado. Un escritor con acceso al repositorio puede omitir la práctica de PR/CI. **Recomendación:** proteger `main` mediante PR obligatorio, status check del job `powershell-windows`, rechazo de force push/borrado y revisión independiente cuando exista revisor disponible. Es una configuración GitHub **pendiente de autorización**; no se cambió.

### ALTO — Runtime divergente, no certificar permisos nuevos
SHA exacto: 6/11 agentes y 2/18 skills CORE según el preflight del usuario. Hasta clasificar BOM/EOL vs cambio de contenido, auditar diferencias de ACL y certificar ejecución/rollback, ninguna wave autoriza instalación o promoción de privilegios. **Recomendación:** actualizar evidencia mediante `Generar-DevTeam-ActivationPreflight.ps1`; diferenciar SOURCE, INSTALLED, EXECUTED y CERTIFIED.

### ALTO — MAIN_ADVANCED sin disparador ni ejecutor
Las instrucciones Git anteriores exigían una rama temporal y cierre, pero no notificaban sistemáticamente a los propietarios de **otras ramas activas** al avanzar `main`. El nuevo protocolo `docs/VX-TEAM-GIT-RECONCILIATION-V1.md` establece señal y fan-out idempotentes. El módulo `tools/vx_team_git_reconciliation.py` es **solo planificador inerte**, no un servicio de vigilancia ni ejecutor. La función automática real necesita tarea/owner registrados, acceso Git controlado, detector, cola, manejo de conflictos y permiso explícito.

### MEDIO — Roles y privilegios heterogéneos
El Dev Team 2.3.0 declara líder con `edit/write/apply_patch/bash: ask`, diez hijos `deny` para escritura y shell, con `glob/grep` y skills exactas. El pack VX anterior sí incluye builders Backend/Data/Frontend/QA/Docs con `edit: ask`; algunas herramientas `skill: allow` son más amplias que la allowlist exacta del Dev Team. Esos builders **no** deben confundirse con los especialistas Dev Team read-only. Verificar precedencia y exposición real del host antes de modificar roles.

### MEDIO — Alcance «global only» vs archivo del propio repo
La política prohíbe introducir configuración Kilo dentro de proyectos; sin embargo el árbol rastrea `.kilo/kilo.jsonc` con `snapshot:false`. No se ha demostrado que ese archivo controle el Kilo del usuario; catalogarlo como excepción source/histórica o retirarlo de forma gobernada, **no borrarlo automáticamente**.

### MEDIO — Patrones de gitignore /scripts y /tests
`.gitignore` contiene `/scripts` y `/tests`, lo que puede ocultar **archivos nuevos no rastreados** en esos directorios, aunque Git sigue actualizando los ya versionados. Revisar la necesidad histórica y migrar a patrones explícitos si se decide incorporar nuevas herramientas o tests en esos árboles; no modificar reglas sin comprobar impacto.

### MEDIO — Cobertura de permisos no equiparable a seguridad runtime
`"*": deny` es una buena defensa declarativa, pero la prueba negativa real de herramientas namespaced y helpers MCP genéricos sigue pendiente (issue #81). `lsp` y disponibilidad MCP pueden variar por host. No concluir que el source prueba que todas las denegaciones son efectivas.

## 3. Matriz propuesta para desbloqueo gradual (NO APLICADA)

| Nivel | Rol / operación | Estado actual | Gate para habilitar |
| --- | --- | --- | --- |
| A0 OBSERVE | Diez especialistas Dev Team | Read-only declarado, runtime parcial | Visibilidad de tool real, pruebas negativas de edit/bash/task/MCP |
| A1 PROPOSE | Especialistas Dev Team y lectores VX | Diseño/recomendación sin ejecutar | Revisión independiente de hallazgos; no subir privilegios |
| A2 WORKTREE_WRITE | Líder Dev Team o builder VX autorizado | `ask` según source, efectivo no confirmado | Worktree aislado, owner, allowed_paths, test de comandos, rollback y aprobación de operador para cambios de ACL |
| A2 RECONCILE | Futuro ejecutor de `MAIN_ADVANCED` | **NO ACTIVADO** | Dispatcher autenticado, lease de SHA, punto seguro, worktree limpio, pruebas de conflicto/permisos, revisión y opt-in explícito |
| A3 INTEGRATE | Coordinación de PR | PR/CI como práctica source | Protección de main, CI obligatorio, revisor independiente, validación de SHA remoto |
| A4 PUBLISH | Deploy, instalación global, scheduler o ACL | No autorizado | Aprobación externa específica, backups, prueba de reversión, certificación runtime |

**Principio de mínima autoridad:** no conceder `bash: allow` global, no convertir `ask` en `allow` por conveniencia, no dar shell/edit a los 10 especialistas solo para reconciliar; el reconciliador futuro debe ser una capacidad separada con permiso por repositorio/branch/comando.

## 4. Política nueva de ramas y continuidad

Una rama `work/<tema>` **por tarea**. Varias tareas independientes pueden avanzar simultáneamente en ramas separadas, pero cada una con **un único propietario y un escritor por worktree**. Si hay un único worktree compartido, se escribe de manera serial, no paralela.

Cuando `main` cambia, emitir `MAIN_ADVANCED(repo,new_main_sha)`; generar una tarea `RECONCILE_REQUIRED` por branch activa (sin duplicar por reintentos), notificar a su dueño, esperar punto seguro, conciliar su rama sin rebase destructivo, verificar pruebas y reanudar. Si falta permiso, hay conflicto o árbol sucio, **no inventar un merge**: pausar solo esa tarea. Si main avanza de nuevo, trabajar contra el SHA más reciente.

Al completar: PR, CI, revisión, merge, SHA remoto confirmado, archivo y eliminación de **solo esa rama propia**. El cierre de una tarea genera `MAIN_ADVANCED` para las demás activas. El ciclo evita acumulación, pero no elimina work-in-progress ajeno.

## 5. Certificación viva y próximos gates

1. **Source:** validar contrato JSON, filtrado de repositorios, fan-out y no-mutación en la **suite existente**. Mantener acción `UPDATE`, no duplicar test suites.
2. **Runtime read-only:** preflight de hashes, tool snapshot real por rol, MCP exactos, issue #81.
3. **A2 sintético:** repos Git locales con dos y tres ramas concurrentes; eventos repetidos; dirty worktree; conflictos; otra rama en worktree; main avanzando dos veces; apagón/recuperación.
4. **A3 GitHub:** configurar protección de `main` tras autorización; verificar status checks y reviews sin autorizar bypass.
5. **A2 runtime opt-in:** activar watcher/dispatcher por separado, con aprobación y rollback; no junto al cambio de políticas.
6. **Cierre:** no conservar una nueva batería por versión; sustituir únicamente oráculos supersedidos tras PASS y mantener historia en Git/PR.

## Estado final de esta auditoría

- Políticas/documentación/planificador source: **incorporados en PR de auditoría, sujetos a CI/revisión/merge**.
- Automatización `MAIN_ADVANCED`: **NO ACTIVADA**.
- Permisos ampliados: **0**.
- Instalaciones sobre Windows/HOME: **0**.
- Protección de main: **pendiente**.
- Certificación runtime: **parcial y bloqueada**.

Referencias: `rules/AGENTS-global-managed.md`, `agents/vx-dev-team.md`, `docs/VX-DEV-TEAM-CURRENT-PACK-V1.md`, `docs/VX-PERMISOS-Y-AUTONOMIA-V1-20261115.md`, `registry/vx-team-git-reconciliation-v1.json`, `registry/dev-team-activation-waves-v1.json`.
