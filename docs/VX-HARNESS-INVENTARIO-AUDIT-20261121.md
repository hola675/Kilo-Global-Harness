# Auditoría integral del árbol de Kilo Global Harness — 2026-11-21

**Edición:** 1.0.0 · **Ámbito:** inventario exhaustivo por ruta, trazabilidad contra el manifiesto canónico y revisión dirigida de instaladores, políticas, agentes y documentación.

> Esta tabla enumera **todos los archivos rastreados** de la rama auditada y muestra su relación con el paquete actual. **No equivale a certificar semánticamente el contenido ni el uso de cada archivo por una ejecución real**. Un archivo fuera de `vx-unified-pack-v1.json` puede seguir siendo necesario para CI, restauración, desarrollo opcional o investigación. Por tanto, **no** se considera seguro borrarlo por ausencia del manifiesto.

## Estado autorizado y conteos

- **Árbol inventariado:** **415 archivos** (tras retirar el snapshot histórico de raíz `AUDITORIA-DETALLADA.md`).
- **Assets del pack:** **80 rutas** = 18 agentes + 57 Skills + 3 comandos + 2 soportes.
- **Un solo modo visible:** `vx-dev-team` (nombre VX Dev Team); 17 hijos ocultos, siete roles con Swarm sujeto a host.
- **No cambios en runtime del usuario:** ni HOME, ni `kilo.jsonc`, ni MCP, permisos, AutoApprove o bases privadas.
- **Instalador permitido:** `scripts/Instalar-DevTeam-Unificado.ps1`; el backend importa compatibilidad desde `scripts/vx_pack_coexist_v023.py`, por lo que **este archivo no es desechable**.

## Hallazgos concretos y decisiones

1. **[Corregido en este PR]** `README.md` contenía 425 líneas y estados cronológicamente incompatibles (13/14/18/28 agentes, 31/40/43/44/53/57 Skills), además de instrucciones de instaladores antiguos. Se sustituyó por un índice vigente de Core VX 1.6 y enlaces a guías específicas.
2. **[Corregido]** `docs/ARQUITECTURA.md` aún presentaba `vx-integrador` como líder V3. Se sustituyó por la arquitectura vigente de un único `VX Dev Team` y su canal Swarm/cola.
3. **[Corregido]** la ayuda de `Instalar-DevTeam-Unificado.ps1` aún indicaba 43 Skills y V1.0; el backend `vx_unified_pack.py` decía Core V1. Ahora la descripción coincide con 18/57 y Core 1.6.
4. **[Retirado, recuperable en Git]** `AUDITORIA-DETALLADA.md` documentaba una copia del 13 de noviembre anterior al pack actual. No era un insumo del instalador canónico; se elimina del árbol de trabajo, no de la historia Git.
5. **[Retirado, recuperable en Git]** `docs/VX-CHECKPOINT-CONSOLIDACION-20261120.md` era una fotografía puntual de ramas del 20 de noviembre, sin enlaces desde las otras 77 guías Markdown consultadas. No era una fuente del instalador, las políticas ni el manifiesto actual.
6. **[Corregido]** `.gitignore` ocultaba **todo `/scripts` y `/tests`** a Git cuando eran archivos nuevos, dificultando incorporar nuevas pruebas o utilidades. Se sustituyeron por patrones de archivos temporales y caches, manteniendo excluidas credenciales, bases de datos y backups.
7. **[Compatibilidad retenida]** Seis archivos `agents/vx-integrador.md`, `vx-inspector.md`, `vx-researcher.md`, `vx-security-reviewer.md`, `vx-test-analyst.md`, `vx-frontend-adviser.md` NO pertenecen al pack activo, **pero** `registry/vx-agent-registry-v4.json`, `scripts/Validar-Registro-V4.ps1` y pruebas como `tests/test_vx_agent_permissions_v02.py` todavía los usan. Retirarlos sin migrar validador, pruebas y rollback rompería CI o la vía legacy.
8. **[Compatibilidad retenida]** Los 32 comandos de `commands/` no enumerados por el manifiesto no se instalan en el Core actual, pero hay herramientas antiguas que los copian en bloque. No son automáticamente basura; necesitan evaluación por comando antes de borrar.
9. **[Riesgo señalado]** `scripts/Instalar-Kilo-Global-Harness.ps1` aún utiliza `Get-ChildItem`/copia de `agents/` y `commands/` completos. **No usar ese instalador para renovar Core VX 1.6** o podría volver a instalar agentes/commands legacy. Las pruebas históricas siguen cubriendo su reversión; el retiro definitivo requiere sustituir primero dichos tests/gates.
10. **[Propuestas aisladas]** Los JSON `*.proposal.json` son borradores, no assets instalados. Algunas Skills propuestas pueden ser útiles después; eliminarlos exige decisión de producto y comprobar sus consumidores, no solo su sufijo.
11. **[Validación pendiente fuera del repo]** La CI Windows valida la integridad source y contratos actuales. La disponibilidad real de herramientas `task(background:true)` y Swarm exige pruebas en Kilo Desktop tras actualizar el HOME.

## Reglas para las próximas retiradas

- `REMOVE`: únicamente cuando exista evidencia de ausencia de consumidores (incluidos tests/CI, scripts legacy, enlaces de documentación, restauración), sustitución PASS y PR reversible.
- `MIGRATE`: primero modificar instalador/registro/validador/tests que dependan de una fuente histórica, después retirar el archivo; nunca al revés.
- `RETAIN_COMPAT`: preservar código de restauración, auditoría o fixtures mientras el flujo de soporte siga vivo.
- `OPTIONAL`: no significa instalado; tampoco significa que el usuario quiera perder esta capacidad.
- La versión anterior sigue accesible desde Git: no mantener instantáneas de README/arquitectura repetidas únicamente para narrar el historial.

## Matriz de clasificación por archivo

**Convenciones:** «activo» significa referencia literal en el manifiesto; «no instalado» significa fuera de ese manifiesto, **no** declaración de archivo sin uso.

### 10 HERRAMIENTAS OPCIONALES Y METADATOS (33)

- `.agents/skills/use-tinyfish/SKILL.md` — FUERA_MANIFIESTO
- `.kilo/kilo.jsonc` — FUERA_MANIFIESTO
- `.serena/.gitignore` — FUERA_MANIFIESTO
- `.serena/project.yml` — FUERA_MANIFIESTO
- `config/vx-reunion-policy.v1.json` — FUERA_MANIFIESTO
- `plugins/vx-observer-light.js` — FUERA_MANIFIESTO
- `rules/vx-global-harness-v3.md` — FUERA_MANIFIESTO
- `scripts/Auditar-Kilo-Global.ps1` — FUERA_MANIFIESTO
- `scripts/Comparar-DevTeam-ToolSnapshot.ps1` — FUERA_MANIFIESTO
- `scripts/Consolidar-Ramas-Main-V2.ps1` — FUERA_MANIFIESTO
- `scripts/Crear-DevTeam-RuntimeToolSnapshot.ps1` — FUERA_MANIFIESTO
- `scripts/Generar-DevTeam-ActivationPreflight.ps1` — FUERA_MANIFIESTO
- `scripts/Generar-DevTeam-ToolPlan.ps1` — FUERA_MANIFIESTO
- `scripts/Inventariar-DevTeam-Tools.ps1` — FUERA_MANIFIESTO
- `scripts/Reconciliar-Agentes-V4.2.ps1` — FUERA_MANIFIESTO
- `scripts/Seleccionar-Equipo-V4.ps1` — FUERA_MANIFIESTO
- `scripts/Validar-MCP-Pack.ps1` — FUERA_MANIFIESTO
- `scripts/Validar-Registro-V4.ps1` — FUERA_MANIFIESTO
- `scripts/mcp/github-mcp-kilo.ps1` — FUERA_MANIFIESTO
- `scripts/vx_approval_contract.py` — FUERA_MANIFIESTO
- `scripts/vx_approval_security_v472.py` — FUERA_MANIFIESTO
- `scripts/vx_capability_audit.py` — FUERA_MANIFIESTO
- `scripts/vx_competency_matrix.py` — FUERA_MANIFIESTO
- `scripts/vx_competency_trials.py` — FUERA_MANIFIESTO
- `scripts/vx_evolution_core.py` — FUERA_MANIFIESTO
- `scripts/vx_organizational_audit.py` — FUERA_MANIFIESTO
- `scripts/vx_pack_bootstrap.py` — FUERA_MANIFIESTO
- `scripts/vx_pack_coexist_v023.py` — FUERA_MANIFIESTO
- `scripts/vx_pack_doctor.py` — FUERA_MANIFIESTO
- `scripts/vx_publish_preview.py` — FUERA_MANIFIESTO
- `scripts/vx_runtime_smoke_v1.py` — FUERA_MANIFIESTO
- `scripts/vx_skill_router.py` — FUERA_MANIFIESTO
- `skills-lock.json` — FUERA_MANIFIESTO

### 06 CI Y SOPORTE — no retirar por nombre (91)

- `.github/workflows/validar-harness.yml` — SOURCE_CI
- `tests/Test-DevTeam-Only-Reset.ps1` — SOURCE_CI
- `tests/Test-VX-Meeting-Current-Smoke.ps1` — SOURCE_CI
- `tests/dev_team_agent_parser_support.py` — SOURCE_CI
- `tests/fixtures/dev-team-v230/backend/account_service.ts` — SOURCE_CI
- `tests/fixtures/dev-team-v230/backend/accounts_handler.ts` — SOURCE_CI
- `tests/fixtures/dev-team-v230/data/historical_rows.sql` — SOURCE_CI
- `tests/fixtures/dev-team-v230/data/migration.sql` — SOURCE_CI
- `tests/fixtures/dev-team-v230/data/schema.sql` — SOURCE_CI
- `tests/fixtures/dev-team-v230/explorer/app.test.ts` — SOURCE_CI
- `tests/fixtures/dev-team-v230/explorer/app.ts` — SOURCE_CI
- `tests/fixtures/dev-team-v230/explorer/config.json` — SOURCE_CI
- `tests/fixtures/dev-team-v230/explorer/report_service.ts` — SOURCE_CI
- `tests/fixtures/dev-team-v230/platform/config/production.json` — SOURCE_CI
- `tests/fixtures/dev-team-v230/platform/config/staging.json` — SOURCE_CI
- `tests/fixtures/dev-team-v230/platform/pipeline.yml` — SOURCE_CI
- `tests/fixtures/dev-team-v230/reviewer/after.ts` — SOURCE_CI
- `tests/fixtures/dev-team-v230/reviewer/before.ts` — SOURCE_CI
- `tests/fixtures/dev-team-v230/reviewer/test_tenant_data.ts` — SOURCE_CI
- `tests/fixtures/dev-team-v230/security/auth.ts` — SOURCE_CI
- `tests/fixtures/dev-team-v230/security/handler.ts` — SOURCE_CI
- `tests/fixtures/dev-team-v230/security/tenant_store.ts` — SOURCE_CI
- `tests/fixtures/dev-team-v2r2/architect/module-a.ts` — SOURCE_CI
- `tests/fixtures/dev-team-v2r2/architect/module-b.ts` — SOURCE_CI
- `tests/fixtures/dev-team-v2r2/backend-data/order_service.ts` — SOURCE_CI
- `tests/fixtures/dev-team-v2r2/frontend/LoginPanel.tsx` — SOURCE_CI
- `tests/fixtures/dev-team-v2r2/quality/calculator.py` — SOURCE_CI
- `tests/fixtures/dev-team-v2r2/quality/test_calculator.py` — SOURCE_CI
- `tests/fixtures/dev-team-v2r2/research/decision-a.md` — SOURCE_CI
- `tests/fixtures/dev-team-v2r2/research/decision-b.md` — SOURCE_CI
- `tests/test_vx_agent_permissions_v02.py` — SOURCE_CI
- `tests/test_vx_approval_contract_v471.py` — SOURCE_CI
- `tests/test_vx_approval_security_v472.py` — SOURCE_CI
- `tests/test_vx_capability_audit_v460.py` — SOURCE_CI
- `tests/test_vx_ci_living_gates_v1.py` — SOURCE_CI
- `tests/test_vx_ci_no_duplicate_test_invocations.py` — SOURCE_CI
- `tests/test_vx_competency_matrix_v461.py` — SOURCE_CI
- `tests/test_vx_competency_trials_v462.py` — SOURCE_CI
- `tests/test_vx_consolidacion_v01.py` — SOURCE_CI
- `tests/test_vx_dev_team_activation_preflight_v1.py` — SOURCE_CI
- `tests/test_vx_dev_team_activation_waves_v1.py` — SOURCE_CI
- `tests/test_vx_dev_team_agent_parser.py` — SOURCE_CI
- `tests/test_vx_dev_team_capability_matrix_v1.py` — SOURCE_CI
- `tests/test_vx_dev_team_consolidation_v1.py` — SOURCE_CI
- `tests/test_vx_dev_team_current_certification_manifest.py` — SOURCE_CI
- `tests/test_vx_dev_team_living_certification_policy_v1.py` — SOURCE_CI
- `tests/test_vx_dev_team_mcp_current_contract.py` — SOURCE_CI
- `tests/test_vx_dev_team_mcp_exact_inventory_v1.py` — SOURCE_CI
- `tests/test_vx_dev_team_mcp_operations_v1.py` — SOURCE_CI
- `tests/test_vx_dev_team_runtime_tool_inventory_v1.py` — SOURCE_CI
- `tests/test_vx_dev_team_runtime_visible_tool_capture_v1.py` — SOURCE_CI
- `tests/test_vx_dev_team_skill_eval_runner_v1.py` — SOURCE_CI
- `tests/test_vx_dev_team_skill_mcp_integration_v1.py` — SOURCE_CI
- `tests/test_vx_dev_team_skills_gap_v2.py` — SOURCE_CI
- `tests/test_vx_dev_team_skills_matrix_v1.py` — SOURCE_CI
- `tests/test_vx_dev_team_tool_plan_generator_v1.py` — SOURCE_CI
- `tests/test_vx_dev_team_v1.py` — SOURCE_CI
- `tests/test_vx_dev_team_v210_split.py` — SOURCE_CI
- `tests/test_vx_dev_team_v230_runtime_certification.py` — SOURCE_CI
- `tests/test_vx_dev_ux_ui_pro_v1.py` — SOURCE_CI
- `tests/test_vx_evolution_core.py` — SOURCE_CI
- `tests/test_vx_evolution_current_certification_manifest.py` — SOURCE_CI
- `tests/test_vx_historical_test_retirement_plan.py` — SOURCE_CI
- `tests/test_vx_ida_mcp_skill.py` — SOURCE_CI
- `tests/test_vx_kilo_tools_complements_audit_v1.py` — SOURCE_CI
- `tests/test_vx_living_certification_agent_policy_v1.py` — SOURCE_CI
- `tests/test_vx_meeting_current_contract.py` — SOURCE_CI
- `tests/test_vx_observer_light.py` — SOURCE_CI
- `tests/test_vx_organizational_audit_v463.py` — SOURCE_CI
- `tests/test_vx_p2_mode_gate_v025.py` — SOURCE_CI
- `tests/test_vx_pack_bootstrap_v1.py` — SOURCE_CI
- `tests/test_vx_pack_coexist_current.py` — SOURCE_CI
- `tests/test_vx_pack_current_certification_manifest.py` — SOURCE_CI
- `tests/test_vx_pack_current_contract.py` — SOURCE_CI
- `tests/test_vx_pack_doctor.py` — SOURCE_CI
- `tests/test_vx_publish_preview_v470.py` — SOURCE_CI
- `tests/test_vx_runtime_evidence_current.py` — SOURCE_CI
- `tests/test_vx_skill_router_v02.py` — SOURCE_CI
- `tests/test_vx_task_dag_v01.py` — SOURCE_CI
- `tests/test_vx_unified_pack_v1.py` — SOURCE_CI
- `tools/__init__.py` — SOURCE_CI
- `tools/dev_team_agent_parser.py` — SOURCE_CI
- `tools/dev_team_skill_eval_runner.py` — SOURCE_CI
- `tools/plan_historical_test_retirement.py` — SOURCE_CI
- `tools/run_dev_team_current_certification.py` — SOURCE_CI
- `tools/run_vx_evolution_current_certification.py` — SOURCE_CI
- `tools/run_vx_pack_current_certification.py` — SOURCE_CI
- `tools/vx_team_capability_router.py` — SOURCE_CI
- `tools/vx_team_git_queue_store.py` — SOURCE_CI
- `tools/vx_team_git_reconciliation.py` — SOURCE_CI
- `tools/vx_team_git_worktrees.py` — SOURCE_CI

### OTROS — revisar alcance (36)

- `.gitignore` — FUERA_MANIFIESTO
- `inventory/harness-sources-2026-11-13.json` — FUERA_MANIFIESTO
- `inventory/mcp-runtime-2026-11-17.json` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-data-visualization/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-design-system-governance/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-doc-traceability/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-forms-ux/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-incident-analysis/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-information-architecture/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-interaction-motion/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-mcp-capability-routing/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-mcp-context-budget/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-mcp-evidence-ledger/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-mcp-failure-recovery/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-mcp-handoff/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-mcp-sensitive-data/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-mcp-server-playbook/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-mcp-tool-contract/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-observability-privacy/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-performance-analysis/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-regression-analysis/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-release-readiness/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-requirements-acceptance/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-responsive-resilience/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-sql-performance/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-task-dependency-planning/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-ux-ui-pro-review/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-ux-writing-content/SKILL.md` — FUERA_MANIFIESTO
- `runtime/dev-team-v2r/skills/vx-dev-visual-craft/SKILL.md` — FUERA_MANIFIESTO
- `skills/vx-accessibility-review/SKILL.md` — FUERA_MANIFIESTO
- `skills/vx-architecture-decisions/SKILL.md` — FUERA_MANIFIESTO
- `skills/vx-codebase-investigation/SKILL.md` — FUERA_MANIFIESTO
- `skills/vx-evolution-core/SKILL.md` — FUERA_MANIFIESTO
- `skills/vx-security-review/SKILL.md` — FUERA_MANIFIESTO
- `skills/vx-self-improvement/SKILL.md` — FUERA_MANIFIESTO
- `skills/vx-supply-chain-review/SKILL.md` — FUERA_MANIFIESTO

### 09 DOCUMENTACIÓN — vigente, temática o histórica (79)

- `README.md` — DOCUMENTACION
- `docs/ARQUITECTURA.md` — DOCUMENTACION
- `docs/IMAGEGEN-MCP.md` — DOCUMENTACION
- `docs/OPERACION-EQUIPOS-V4.md` — DOCUMENTACION
- `docs/PROTOCOLO-REVALIDACION-V4.1.md` — DOCUMENTACION
- `docs/RECONCILIACION-AGENTES-V4.2.md` — DOCUMENTACION
- `docs/VX-ACADEMY-CAPACITACION-V1-20261115.md` — DOCUMENTACION
- `docs/VX-ACADEMY-EVALUADOR-INDEPENDIENTE-V1-20261115.md` — DOCUMENTACION
- `docs/VX-ACADEMY-MENTORIA-EVOLUCION-V1-20261115.md` — DOCUMENTACION
- `docs/VX-ALCANCE-C-PACK-BOOTSTRAP-20261115.md` — DOCUMENTACION
- `docs/VX-APROBACION-GOBERNADA-V4.7.1.md` — DOCUMENTACION
- `docs/VX-APROBACION-SEGURIDAD-V4.7.2.md` — DOCUMENTACION
- `docs/VX-AUDITORIA-COHERENCIA-PACK-20261116.md` — DOCUMENTACION
- `docs/VX-AUDITORIA-ORGANIZATIVA-V4.6.3.md` — DOCUMENTACION
- `docs/VX-CAPACIDADES-V4.6.0.md` — DOCUMENTACION
- `docs/VX-CERTIFICACION-RUNTIME-20261116.md` — DOCUMENTACION
- `docs/VX-CI-LIVING-GATES-V1.md` — DOCUMENTACION
- `docs/VX-CI-TEST-OWNERSHIP-V1.md` — DOCUMENTACION
- `docs/VX-CIERRE-BATERIA-V4.6.2-20261114.md` — DOCUMENTACION
- `docs/VX-CONSOLIDACION-MAIN-20261116.md` — DOCUMENTACION
- `docs/VX-CONTEXTUAL-SKILLS-GOVERNANCE-V1.md` — DOCUMENTACION
- `docs/VX-DESARROLLO-ESCALONADO-CONECTIVIDAD-V1.md` — DOCUMENTACION
- `docs/VX-DESKTOP-VALIDACION-Y-PUERTA-V4.7-20261114.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-230-RUNTIME-CERTIFICATION.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-ACTIVATION-WAVES-V1.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-ARCHITECTURE-V1.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-AUTOPILOT-V2.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-CAPABILITY-MATRIX-V1.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-CONSOLIDATION-V1.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-CURRENT-PACK-V1.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-LIVING-CERTIFICATION-V1.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-MCP-EXACT-INVENTORY-V1.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-MCP-MATRIX-V1.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-MCP-OPERATIONS-V1.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-MCP-READONLY-MATRIX-V1.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-RUNTIME-ACTIVATION-PREFLIGHT-V1.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-RUNTIME-TOOL-SNAPSHOT-V1.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-RUNTIME-V1.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-SKILL-ACTIVATION-V1.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-SKILL-EVAL-RUNNER-V1.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-SKILL-MCP-INTEGRATION-V1.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-SKILLS-GAP-V2.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-SKILLS-MATRIX-V1.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-SKILLS-RESEARCH-V1.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-TOOL-PLAN-GENERATOR-V1.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-UNIFIED-V1.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-V2R-READONLY.md` — DOCUMENTACION
- `docs/VX-DEV-TEAM-V2R2-CERTIFICACION-ESPECIALISTAS.md` — DOCUMENTACION
- `docs/VX-DEV-UX-UI-PRO-V1.md` — DOCUMENTACION
- `docs/VX-ENSAYOS-COMPETENCIAS-V4.6.2.md` — DOCUMENTACION
- `docs/VX-EQUIPO-INICIAL-PACK-20261115.md` — DOCUMENTACION
- `docs/VX-EVOLUTION-DECISIONES.md` — DOCUMENTACION
- `docs/VX-EVOLUTION-ROADMAP.md` — DOCUMENTACION
- `docs/VX-EVOLUTION-V4.3.md` — DOCUMENTACION
- `docs/VX-HARNESS-AUDITORIA-EQUIPO-Y-GIT-20261119.md` — DOCUMENTACION
- `docs/VX-HISTORICAL-TEST-RETIREMENT-V1.md` — DOCUMENTACION
- `docs/VX-INSTALACION-CONVIVENCIA-0.2.3-WINDOWS.md` — DOCUMENTACION
- `docs/VX-INSTALACION-PACK-0.2.2-WINDOWS.md` — DOCUMENTACION
- `docs/VX-KILO-TOOLS-COMPLEMENTS-AUDIT-V1.md` — DOCUMENTACION
- `docs/VX-LIVING-CERTIFICATION-AGENT-POLICY-V1.md` — DOCUMENTACION
- `docs/VX-MATRIZ-COMPETENCIAS-V4.6.1.md` — DOCUMENTACION
- `docs/VX-MCP-PACK-WINDOWS-V1-20261117.md` — DOCUMENTACION
- `docs/VX-OBSERVER-V4.4.md` — DOCUMENTACION
- `docs/VX-PACK-DESARROLLO-MVP-20261116.md` — DOCUMENTACION
- `docs/VX-PACK-OPERACION-MVP-20261116.md` — DOCUMENTACION
- `docs/VX-PERMISOS-Y-AUTONOMIA-V1-20261115.md` — DOCUMENTACION
- `docs/VX-PERSONAS-RELACIONES-V1-20261115.md` — DOCUMENTACION
- `docs/VX-PUBLICACION-GOBERNADA-V4.7.md` — DOCUMENTACION
- `docs/VX-REPRODUCIBILIDAD-TTY-V4.7.1.md` — DOCUMENTACION
- `docs/VX-REUNION-V4.5.md` — DOCUMENTACION
- `docs/VX-REVISION-STEPS-PRECEDENCIA-V4.6.3-20261114.md` — DOCUMENTACION
- `docs/VX-TEAM-CAPABILITY-HANDOFF-V1.md` — DOCUMENTACION
- `docs/VX-TEAM-GIT-RECONCILIATION-V1.md` — DOCUMENTACION
- `docs/VX-TEAM-GLOBAL-CAPABILITIES-V14.md` — DOCUMENTACION
- `docs/VX-VALIDACION-CLI-V4.6.2-20261114.md` — DOCUMENTACION
- `docs/VX-VALIDACION-LOCAL-V4.6.3-20261114.md` — DOCUMENTACION
- `docs/investigacion/HARNESSES-Y-AGENTES-2026-11-13.md` — DOCUMENTACION
- `docs/investigacion/ORQUESTACION-MULTIAGENTE-V4.md` — DOCUMENTACION
- `docs/VX-HARNESS-INVENTARIO-AUDIT-20261121.md` — DOCUMENTACION

### 01 ACTIVOS — instalados desde manifiesto (80)

- `agents/vx-backend-builder.md` — AGENTE BUILDER
- `agents/vx-data-builder.md` — AGENTE BUILDER
- `agents/vx-dev-team.md` — AGENTE LEAD
- `agents/vx-docs-builder.md` — AGENTE BUILDER
- `agents/vx-editorial-builder.md` — AGENTE BUILDER
- `agents/vx-frontend-builder.md` — AGENTE BUILDER
- `agents/vx-qa-builder.md` — AGENTE BUILDER
- `agents/vx-workers-adviser.md` — AGENTE SPECIALIST
- `commands/vx-dependencias.md` — COMANDO ACTIVO
- `commands/vx-editorial.md` — COMANDO ACTIVO
- `commands/vx-equipo.md` — COMANDO ACTIVO
- `registry/vx-unified-pack-v1.json` — SOPORTE ACTIVO
- `runtime/dev-team-v2r/agents/vx-dev-architect.md` — AGENTE READONLY
- `runtime/dev-team-v2r/agents/vx-dev-backend.md` — AGENTE READONLY
- `runtime/dev-team-v2r/agents/vx-dev-data.md` — AGENTE READONLY
- `runtime/dev-team-v2r/agents/vx-dev-explorer.md` — AGENTE READONLY
- `runtime/dev-team-v2r/agents/vx-dev-frontend.md` — AGENTE READONLY
- `runtime/dev-team-v2r/agents/vx-dev-platform.md` — AGENTE READONLY
- `runtime/dev-team-v2r/agents/vx-dev-quality.md` — AGENTE READONLY
- `runtime/dev-team-v2r/agents/vx-dev-research.md` — AGENTE READONLY
- `runtime/dev-team-v2r/agents/vx-dev-reviewer.md` — AGENTE READONLY
- `runtime/dev-team-v2r/agents/vx-dev-security.md` — AGENTE READONLY
- `runtime/dev-team-v2r/skills/vx-dev-accessibility/SKILL.md` — SKILL ACTIVA
- `runtime/dev-team-v2r/skills/vx-dev-architecture-decision/SKILL.md` — SKILL ACTIVA
- `runtime/dev-team-v2r/skills/vx-dev-backend-contracts/SKILL.md` — SKILL ACTIVA
- `runtime/dev-team-v2r/skills/vx-dev-codebase-investigation/SKILL.md` — SKILL ACTIVA
- `runtime/dev-team-v2r/skills/vx-dev-data-migration/SKILL.md` — SKILL ACTIVA
- `runtime/dev-team-v2r/skills/vx-dev-debug-triage/SKILL.md` — SKILL ACTIVA
- `runtime/dev-team-v2r/skills/vx-dev-frontend-ux/SKILL.md` — SKILL ACTIVA
- `runtime/dev-team-v2r/skills/vx-dev-independent-review/SKILL.md` — SKILL ACTIVA
- `runtime/dev-team-v2r/skills/vx-dev-mcp-readonly/SKILL.md` — SKILL ACTIVA
- `runtime/dev-team-v2r/skills/vx-dev-mcp-security/SKILL.md` — SKILL ACTIVA
- `runtime/dev-team-v2r/skills/vx-dev-platform-delivery/SKILL.md` — SKILL ACTIVA
- `runtime/dev-team-v2r/skills/vx-dev-project-policy/SKILL.md` — SKILL ACTIVA
- `runtime/dev-team-v2r/skills/vx-dev-security-threat-review/SKILL.md` — SKILL ACTIVA
- `runtime/dev-team-v2r/skills/vx-dev-source-reconciliation/SKILL.md` — SKILL ACTIVA
- `runtime/dev-team-v2r/skills/vx-dev-supply-chain-review/SKILL.md` — SKILL ACTIVA
- `runtime/dev-team-v2r/skills/vx-dev-team-handoff/SKILL.md` — SKILL ACTIVA
- `runtime/dev-team-v2r/skills/vx-dev-test-strategy/SKILL.md` — SKILL ACTIVA
- `runtime/dev-team-v2r/skills/vx-dev-ui-state-system/SKILL.md` — SKILL ACTIVA
- `scripts/vx_task_dag.py` — SOPORTE ACTIVO
- `skills/vx-agent-collaboration/SKILL.md` — SKILL ACTIVA
- `skills/vx-api-contract-design/SKILL.md` — SKILL ACTIVA
- `skills/vx-cloudflare-storage-messaging/SKILL.md` — SKILL ACTIVA
- `skills/vx-cloudflare-worker-runtime/SKILL.md` — SKILL ACTIVA
- `skills/vx-conectividad-dispositivos/SKILL.md` — SKILL ACTIVA
- `skills/vx-context-routing/SKILL.md` — SKILL ACTIVA
- `skills/vx-data-contracts/SKILL.md` — SKILL ACTIVA
- `skills/vx-debugging-root-cause/SKILL.md` — SKILL ACTIVA
- `skills/vx-desarrollo-escalonado/SKILL.md` — SKILL ACTIVA
- `skills/vx-docs-traceability/SKILL.md` — SKILL ACTIVA
- `skills/vx-e2e-browser-testing/SKILL.md` — SKILL ACTIVA
- `skills/vx-editorial-claridad/SKILL.md` — SKILL ACTIVA
- `skills/vx-engineering-harness/SKILL.md` — SKILL ACTIVA
- `skills/vx-enterprise-workflows/SKILL.md` — SKILL ACTIVA
- `skills/vx-erp-localfirst-modular/SKILL.md` — SKILL ACTIVA
- `skills/vx-frontend-quality/SKILL.md` — SKILL ACTIVA
- `skills/vx-git-ci-quality/SKILL.md` — SKILL ACTIVA
- `skills/vx-ida-mcp-reverse-engineering/SKILL.md` — SKILL ACTIVA
- `skills/vx-implementation-handoff/SKILL.md` — SKILL ACTIVA
- `skills/vx-incident-diagnosis/SKILL.md` — SKILL ACTIVA
- `skills/vx-industrial-control-safety/SKILL.md` — SKILL ACTIVA
- `skills/vx-inventory-reconciliation/SKILL.md` — SKILL ACTIVA
- `skills/vx-mcp-safe-integration/SKILL.md` — SKILL ACTIVA
- `skills/vx-observability-privacy/SKILL.md` — SKILL ACTIVA
- `skills/vx-performance-measurement/SKILL.md` — SKILL ACTIVA
- `skills/vx-python-engineering/SKILL.md` — SKILL ACTIVA
- `skills/vx-release-readiness/SKILL.md` — SKILL ACTIVA
- `skills/vx-requirements-acceptance/SKILL.md` — SKILL ACTIVA
- `skills/vx-saas-multitenant-cloud/SKILL.md` — SKILL ACTIVA
- `skills/vx-skill-quality/SKILL.md` — SKILL ACTIVA
- `skills/vx-sql-query-performance/SKILL.md` — SKILL ACTIVA
- `skills/vx-task-dependency-graph/SKILL.md` — SKILL ACTIVA
- `skills/vx-tauri-desktop/SKILL.md` — SKILL ACTIVA
- `skills/vx-team-bootstrap/SKILL.md` — SKILL ACTIVA
- `skills/vx-technology-fit/SKILL.md` — SKILL ACTIVA
- `skills/vx-test-regression/SKILL.md` — SKILL ACTIVA
- `skills/vx-typescript-engineering/SKILL.md` — SKILL ACTIVA
- `skills/vx-version-governance/SKILL.md` — SKILL ACTIVA
- `skills/vx-windows-network-systems/SKILL.md` — SKILL ACTIVA

### 03 LEGACY — agentes fuera de pack (6)

- `agents/vx-frontend-adviser.md` — LEGACY_AGENT_NO_INSTALADO
- `agents/vx-inspector.md` — LEGACY_AGENT_NO_INSTALADO
- `agents/vx-integrador.md` — LEGACY_AGENT_NO_INSTALADO
- `agents/vx-researcher.md` — LEGACY_AGENT_NO_INSTALADO
- `agents/vx-security-reviewer.md` — LEGACY_AGENT_NO_INSTALADO
- `agents/vx-test-analyst.md` — LEGACY_AGENT_NO_INSTALADO

### 04 LEGACY/OPTATIVOS — comandos fuera del pack (32)

- `commands/vx-auditar.md` — NO_INSTALADO_EN_CORE
- `commands/vx-auditoria-equipo.md` — NO_INSTALADO_EN_CORE
- `commands/vx-capacidades.md` — NO_INSTALADO_EN_CORE
- `commands/vx-capacitacion.md` — NO_INSTALADO_EN_CORE
- `commands/vx-certificar.md` — NO_INSTALADO_EN_CORE
- `commands/vx-cierre.md` — NO_INSTALADO_EN_CORE
- `commands/vx-dev-tools-snapshot.md` — NO_INSTALADO_EN_CORE
- `commands/vx-diagnosticar.md` — NO_INSTALADO_EN_CORE
- `commands/vx-ensayos.md` — NO_INSTALADO_EN_CORE
- `commands/vx-evolution.md` — NO_INSTALADO_EN_CORE
- `commands/vx-git-ciclo.md` — NO_INSTALADO_EN_CORE
- `commands/vx-harness-estado.md` — NO_INSTALADO_EN_CORE
- `commands/vx-ida.md` — NO_INSTALADO_EN_CORE
- `commands/vx-imagegen.md` — NO_INSTALADO_EN_CORE
- `commands/vx-implementar.md` — NO_INSTALADO_EN_CORE
- `commands/vx-matriz.md` — NO_INSTALADO_EN_CORE
- `commands/vx-mcp.md` — NO_INSTALADO_EN_CORE
- `commands/vx-modelos.md` — NO_INSTALADO_EN_CORE
- `commands/vx-observer.md` — NO_INSTALADO_EN_CORE
- `commands/vx-organizacion.md` — NO_INSTALADO_EN_CORE
- `commands/vx-p2.md` — NO_INSTALADO_EN_CORE
- `commands/vx-pack.md` — NO_INSTALADO_EN_CORE
- `commands/vx-plan.md` — NO_INSTALADO_EN_CORE
- `commands/vx-reconciliar.md` — NO_INSTALADO_EN_CORE
- `commands/vx-refactor.md` — NO_INSTALADO_EN_CORE
- `commands/vx-reparar.md` — NO_INSTALADO_EN_CORE
- `commands/vx-retro.md` — NO_INSTALADO_EN_CORE
- `commands/vx-reunion.md` — NO_INSTALADO_EN_CORE
- `commands/vx-revalidar.md` — NO_INSTALADO_EN_CORE
- `commands/vx-revisar-diff.md` — NO_INSTALADO_EN_CORE
- `commands/vx-upgrade.md` — NO_INSTALADO_EN_CORE
- `commands/vx-validar.md` — NO_INSTALADO_EN_CORE

### 08 REGISTROS — runtime, evidencia o compatibilidad (34)

- `registry/dev-team-activation-waves-v1.json` — FUERA_MANIFIESTO
- `registry/dev-team-capability-matrix-v1.json` — FUERA_MANIFIESTO
- `registry/dev-team-consolidation-v1.json` — FUERA_MANIFIESTO
- `registry/dev-team-current-certification-v1.json` — FUERA_MANIFIESTO
- `registry/dev-team-current-pack-v1.json` — FUERA_MANIFIESTO
- `registry/dev-team-living-certification-policy-v1.json` — FUERA_MANIFIESTO
- `registry/dev-team-mcp-exact-inventory-v1.json` — FUERA_MANIFIESTO
- `registry/dev-team-only-baseline-v1.json` — FUERA_MANIFIESTO
- `registry/dev-team-readonly-baseline-v2.json` — FUERA_MANIFIESTO
- `registry/dev-team-runtime-activation-manifest.template.json` — FUERA_MANIFIESTO
- `registry/dev-team-runtime-visible-tools.template.json` — FUERA_MANIFIESTO
- `registry/dev-team-skill-activation-v1.json` — FUERA_MANIFIESTO
- `registry/dev-team-v230-runtime-certification-v1.json` — FUERA_MANIFIESTO
- `registry/dev-team-v2r2-specialist-certification-v1.json` — FUERA_MANIFIESTO
- `registry/vx-agent-registry-v4.json` — FUERA_MANIFIESTO
- `registry/vx-ci-living-gates-v1.json` — FUERA_MANIFIESTO
- `registry/vx-contextual-skills-v1.json` — FUERA_MANIFIESTO
- `registry/vx-dev-team-mcp-matrix-v1.json` — FUERA_MANIFIESTO
- `registry/vx-dev-team-v1.json` — FUERA_MANIFIESTO
- `registry/vx-evolution-current-certification-v1.json` — FUERA_MANIFIESTO
- `registry/vx-historical-test-pass-evidence-dev-team-mcp-run-457.json` — FUERA_MANIFIESTO
- `registry/vx-historical-test-pass-evidence-meeting-run-463.json` — FUERA_MANIFIESTO
- `registry/vx-historical-test-pass-evidence-run-450.json` — FUERA_MANIFIESTO
- `registry/vx-historical-test-pass-evidence-run-457.json` — FUERA_MANIFIESTO
- `registry/vx-historical-test-pass-evidence.template.json` — FUERA_MANIFIESTO
- `registry/vx-living-certification-agent-policy-v1.json` — FUERA_MANIFIESTO
- `registry/vx-mcp-catalog-v1.json` — FUERA_MANIFIESTO
- `registry/vx-mcp-catalog-v2.json` — FUERA_MANIFIESTO
- `registry/vx-mcp-optional-catalog-v1.json` — FUERA_MANIFIESTO
- `registry/vx-meeting-current-certification-v1.json` — FUERA_MANIFIESTO
- `registry/vx-pack-current-certification-v1.json` — FUERA_MANIFIESTO
- `registry/vx-skill-dependencies-v1.json` — FUERA_MANIFIESTO
- `registry/vx-team-capability-handoffs-v1.json` — FUERA_MANIFIESTO
- `registry/vx-team-git-reconciliation-v1.json` — FUERA_MANIFIESTO

### 07 PROPUESTAS — no activas (16)

- `registry/dev-team-mcp-operations-evals-v1.proposal.json` — PROPUESTA_INACTIVA
- `registry/dev-team-mcp-operations-v1.proposal.json` — PROPUESTA_INACTIVA
- `registry/dev-team-mcp-readonly-matrix-v1.proposal.json` — PROPUESTA_INACTIVA
- `registry/dev-team-mcp-role-playbook-v1.proposal.json` — PROPUESTA_INACTIVA
- `registry/dev-team-skill-evals-v1.proposal.json` — PROPUESTA_INACTIVA
- `registry/dev-team-skill-evals-v2.proposal.json` — PROPUESTA_INACTIVA
- `registry/dev-team-skill-mcp-integration-v1.proposal.json` — PROPUESTA_INACTIVA
- `registry/dev-team-skills-gap-v2.proposal.json` — PROPUESTA_INACTIVA
- `registry/dev-team-skills-matrix-v1.proposal.json` — PROPUESTA_INACTIVA
- `registry/dev-team-ux-ui-pro-evals-v1.proposal.json` — PROPUESTA_INACTIVA
- `registry/dev-team-ux-ui-pro-v1.proposal.json` — PROPUESTA_INACTIVA
- `registry/kilo-tools-complements-audit-v1.proposal.json` — PROPUESTA_INACTIVA
- `registry/vx-academy-catalog-v1.proposal.json` — PROPUESTA_INACTIVA
- `registry/vx-academy-independent-evaluator-v1.proposal.json` — PROPUESTA_INACTIVA
- `registry/vx-academy-mentorship-v1.proposal.json` — PROPUESTA_INACTIVA
- `registry/vx-organization-graph-v1.proposal.json` — PROPUESTA_INACTIVA

### 02 CANÓNICOS — política e instalador (3)

- `rules/AGENTS-global-managed.md` — FUERA_MANIFIESTO
- `scripts/Instalar-DevTeam-Unificado.ps1` — FUERA_MANIFIESTO
- `scripts/vx_unified_pack.py` — FUERA_MANIFIESTO

### 05 LEGACY — instaladores alternativos NO ejecutar (5)

- `scripts/Instalar-DevTeam-Only.ps1` — FUERA_MANIFIESTO
- `scripts/Instalar-Kilo-Global-Harness.ps1` — FUERA_MANIFIESTO
- `scripts/Instalar-MCP-Pack-Windows.ps1` — FUERA_MANIFIESTO
- `scripts/Instalar-Pack-VX-Convivencia-V023.ps1` — FUERA_MANIFIESTO
- `scripts/Instalar-Pack-VX-V022.ps1` — FUERA_MANIFIESTO

## Control al finalizar

- El inventario posterior al merge debe conservar **18/57/3/2** y un solo líder visible.
- Los seis agentes legacy y comandos fuera de la lista deben permanecer **no instalados** por el instalador canónico.
- Antes de cualquier borrado adicional, ejecutar el CI existente, revisar dependencias de prueba y corregir enlaces afectados.
- Cerrar ramas temporales verificadas tras PR; `main` será la única rama remota permanente.
- Este inventario no representa una prueba de runtime del HOME de Windows.

**Changelog:** v1.0.0 — inventario exhaustivo del árbol, clasificación por rol, consolidación documental y retiro de snapshot histórico.
