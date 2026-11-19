# vx-dev-team — baseline source 2.2.0 con diez especialistas ocultos

**Fecha:** 2026-11-17  
**Estado:** ACTIVE SOURCE BASELINE · runtime pendiente de despliegue/revalidación de source 2.2  
**Primario visible:** `vx-dev-team`  
**Especialistas ocultos:** 10  
**Mutaciones de subagentes:** DENY  
**MCP de subagentes:** deny-by-default; `vx-dev-research` y `vx-dev-architect` tienen 5 tools documentales allowlistadas cada uno

## Objetivo

V2-R introduce la primera capa multiagente aprobada del Harness sin volver a llenar el selector principal.

El operador interactúa únicamente con `vx-dev-team`. El líder puede delegar análisis concretos a especialistas ocultos mediante `task`. Los hijos son no interactivos y trabajan en contexto aislado.

## Equipo V2-R

| ID | Rol | Visible | Escritura | Shell | Delegación | MCP |
|---|---|---:|---:|---:|---:|---:|
| `vx-dev-team` | Team Lead / Technical Lead | sí | ask | ask | allowlist | ninguno automático |
| `vx-dev-explorer` | codebase exploration | no | deny | deny | deny | deny |
| `vx-dev-architect` | architecture decisions/contracts | no | deny | deny | deny | Context7 + Microsoft Learn (5 tools) |
| `vx-dev-frontend` | frontend interaction analysis | no | deny | deny | deny | deny |
| `vx-dev-backend` | backend application analysis | no | deny | deny | deny | deny |
| `vx-dev-data` | data/persistence analysis | no | deny | deny | deny | deny |
| `vx-dev-platform` | platform/runtime analysis | no | deny | deny | deny | deny |
| `vx-dev-quality` | quality verification analysis | no | deny | deny | deny | deny |
| `vx-dev-security` | security trust/abuse analysis | no | deny | deny | deny | deny |
| `vx-dev-reviewer` | independent change review | no | deny | deny | deny | deny |
| `vx-dev-research` | technical research | no | deny | deny | deny | Context7 + Microsoft Learn (5 tools) |

Los especialistas se definen en `runtime/dev-team-v2r/agents/` para mantenerlos separados del árbol legacy de agentes VX.

## Patrón de orquestación

```text
Usuario
  │
  ▼
vx-dev-team
  │
  ├── simple  → 0-1 especialista
  ├── media   → 1-2 especialistas
  └── compleja→ 2-4 especialistas
                  │
                  ▼
          resultados estructurados
                  │
                  ▼
             vx-dev-team
                  │
             síntesis/decisión
```

No existe comunicación lateral entre hijos. No hay Swarm, Board ni Agent Manager.

## Profundidad

Solo una profundidad:

```text
Usuario → vx-dev-team → Subagente
```

Los hijos tienen `task: deny`.

## Contrato de delegación

El líder envía:

- `objective`
- `scope`
- `questions`
- `allowed_paths`
- `known_facts`
- `unknowns`
- `evidence_required`
- `exclusions`
- `output_format`
- `budget`

Los hijos devuelven como envelope común:

- `STATUS`
- `SCOPE_ANALYZED`
- `FINDINGS`
- `EVIDENCE`
- `RISKS`
- `RECOMMENDATION`
- `CONFIDENCE`
- `UNKNOWNS`
- `HANDOFF`

No se devuelve el transcript completo como contrato normal.

## Contrato especializado: vx-dev-explorer

`vx-dev-explorer` es el cartógrafo del codebase. Su función es localizar y conectar evidencia, no diseñar la solución.

Debe producir además del envelope común:

- `CODE_MAP` — entry points, nodos centrales, consumidores, dependencias, tests, configuración y boundaries relevantes;
- `IMPACT_SURFACE` — impacto `DIRECT`, `INDIRECT`, `POSSIBLE` y `OUT_OF_SCOPE`.

Clasifica evidencia como:

- `OBSERVED` — observada directamente;
- `INFERRED` — inferida a partir de varias evidencias;
- `UNKNOWN` — no verificable con el alcance o herramientas actuales.

Fronteras:

- Explorer encuentra y conecta;
- Research confirma documentación/conocimiento;
- Architect diseña;
- los especialistas de dominio analizan comportamiento específico.

No debe convertir exploración en arquitectura, revisión general o propuesta de refactor.

## Contrato especializado: vx-dev-research

`vx-dev-research` confirma conocimiento técnico y procedencia de fuentes. No sustituye a Explorer para mapear código ni a Architect para diseñar.

Su salida específica añade:

- `SOURCE_LEDGER` — fuente, tipo, versión/fecha, afirmación respaldada y autoridad;
- `CONTRADICTIONS` — conflictos entre fuentes, cuál parece vigente y qué requiere validación.

Evidencia:

- `DOCUMENTED`
- `CORROBORATED`
- `INFERRED`
- `UNKNOWN`

Su política MCP es **deny-by-default**. Solo tiene allow explícito para:

- `context7_resolve-library-id`
- `context7_query-docs`
- `microsoft-learn_microsoft_docs_search`
- `microsoft-learn_microsoft_docs_fetch`
- `microsoft-learn_microsoft_code_sample_search`

No tiene acceso a helpers MCP genéricos ni a otros servidores. La disponibilidad de una tool no obliga a invocarla: Research trabaja local-first y consulta documentación externa únicamente cuando cambia o valida una conclusión relevante.

## Contrato especializado: vx-dev-architect

`vx-dev-architect` convierte evidencia verificada y requisitos en decisiones estructurales implementables. No sustituye a Explorer ni Research.

Su salida específica añade:

- `OPTIONS` — alternativas reales cuando exista una decisión material;
- `TRADEOFFS` — complejidad, acoplamiento, compatibilidad, riesgo, reversibilidad y testabilidad;
- `CONTRACTS` — contratos `EXISTING`, `CHANGE`, `NEW` o `DEPRECATED`;
- `DECISIONS_REQUIRED` — decisiones pendientes del líder u operador.

Clasifica afirmaciones como:

- `VERIFIED`
- `ASSUMPTION`
- `PROPOSAL`
- `UNKNOWN`

Comparte la misma allowlist documental de Research:

- `context7_resolve-library-id`
- `context7_query-docs`
- `microsoft-learn_microsoft_docs_search`
- `microsoft-learn_microsoft_docs_fetch`
- `microsoft-learn_microsoft_code_sample_search`

Architect usa esas tools únicamente para validar restricciones externas concretas; no para investigación abierta.

## Contratos especializados: Backend y Data

`vx-dev-backend` analiza comportamiento de aplicación y devuelve:

- `SERVICE_FLOW`
- `API_CONTRACTS`
- `DOMAIN_RULES`
- `FAILURE_MODES`

Su frontera termina antes del diseño físico de persistencia.

`vx-dev-data` analiza persistencia y devuelve:

- `DATA_MODEL`
- `DATA_INVARIANTS`
- `QUERY_IMPACT`
- `CONSISTENCY_RISKS`
- `MIGRATION_IMPACT`

Su frontera termina antes de decidir comportamiento de APIs o reglas de negocio.

El antiguo `vx-dev-backend-data` queda supersedido en el source. Su certificación V2-R.2 se conserva únicamente como evidencia histórica y no certifica los dos agentes nuevos.

## Contrato especializado: vx-dev-frontend

`vx-dev-frontend` analiza comportamiento de interfaz, no preferencias visuales generales.

Su salida específica añade:

- `UI_FLOW` — entrada, acción, estados intermedios, resultado y recuperación;
- `COMPONENT_MODEL` — componentes relevantes, responsabilidades y ownership de estado;
- `STATE_MODEL` — estados cliente necesarios para explicar comportamiento;
- `INTERACTION_STATES` — submit, loading, retry, navegación, optimistic/stale y otros riesgos de interacción;
- `ACCESSIBILITY_RESPONSIVE` — evidencia y riesgos de accesibilidad/responsive sin declarar conformidad completa;
- `API_TOUCHPOINTS` — contratos consumidos por la UI como `CONFIRMED`, `ASSUMED` o `MISSING`.

Fronteras:

- Frontend no diseña endpoints ni lógica de servidor;
- Backend posee APIs/servicios/auth de aplicación;
- Data posee garantías persistentes;
- Architect posee decisiones transversales;
- Quality posee estrategia de verificación;
- Security posee trust boundaries y riesgo de seguridad.

## Contrato especializado: vx-dev-quality

`vx-dev-quality` diseña la evidencia necesaria para demostrar comportamiento; no ejecuta tests ni reemplaza revisión independiente.

Su salida específica añade:

- `INVARIANTS` — propiedades que deben preservarse;
- `TEST_MATRIX` — casos con nivel, escenario, precondición, esperado, oráculo y evidencia;
- `TEST_ORACLES` — señales concretas que demuestran resultado;
- `REGRESSION_SURFACE` — riesgo `DIRECT`, `ADJACENT`, `HISTORICAL` o `POSSIBLE`;
- `ACCEPTANCE_GAPS` — ambigüedades que impiden afirmar corrección;
- `VERIFICATION_PLAN` — secuencia mínima de verificación;
- `EXECUTION_EVIDENCE` — solo `PASS`, `FAIL`, `NO_EJECUTADO` o `NO_VERIFICADO` según evidencia real recibida.

No puede producir PASS por diseñar un test ni usar ausencia de tests como prueba de bug.

## Contrato especializado: vx-dev-security

`vx-dev-security` analiza riesgo de seguridad con trazabilidad explícita entre activo, boundary, input/control y camino de abuso.

Su salida específica añade:

- `ASSETS` — activos relevantes al alcance;
- `TRUST_BOUNDARIES` — origen, destino, dato/acción y control observado;
- `ATTACK_SURFACE` — entry points realmente relevantes;
- `ACCESS_CONTROL` — `ENFORCED`, `PARTIAL`, `MISSING` o `UNKNOWN`;
- `DATA_EXPOSURE` — flujo de datos sensibles sin revelar valores;
- `ABUSE_CASES` — actor, precondición, acción, control y resultado;
- `THREAT_FINDINGS` — attack path, evidencia, impacto, severidad, confianza y validación necesaria.

Evidencia:

- `OBSERVED`
- `CORROBORATED`
- `HYPOTHESIS`
- `DISMISSED`
- `UNKNOWN`

Severidad permitida: `CRITICAL / HIGH / MEDIUM / LOW / INFO`, siempre separada de `CONFIDENCE`.

Security no ejecuta scanners/exploits, no lee/revela secretos y no sustituye Quality ni al futuro Reviewer.

## Contrato especializado: vx-dev-platform

`vx-dev-platform` analiza runtime y entrega sin ejecutar operaciones.

Su salida específica añade:

- `RUNTIME_MAP` — procesos, runtimes, entry points, recursos y lifecycle;
- `BUILD_RELEASE_PATH` — source → build → package → gates → artefacto/entorno;
- `CONFIG_BINDINGS` — configuración por nombre/tipo, nunca valores secretos;
- `ENVIRONMENT_ASSUMPTIONS` — OS/runtime/network/filesystem/permisos documentados o inferidos;
- `DEPLOYMENT_RISKS` — build/config/compatibility/dependency/availability/observability/rollback;
- `OBSERVABILITY_GAPS` — señales faltantes para detectar fallos;
- `VALIDATION_PLAN` — LOCAL/CI/DEV/STAGING/PRODUCTION_GATE sin ejecución;
- `ROLLBACK_PLAN` — reversión conceptual y condición de aborto.

Platform no ejecuta build/CI/deploy, no administra cloud/DNS/IAM/firewall y no tiene MCP externo.

## Contrato especializado: vx-dev-reviewer

`vx-dev-reviewer` realiza una revisión independiente de un change set concreto. Requiere diff/changed paths o evidencia suficiente para distinguir el cambio.

Su salida específica añade:

- `REVIEW_SCOPE`
- `REQUIREMENT_CHECK` — ALIGNED/MISMATCH/UNPROVEN/NOT_APPLICABLE;
- `CONTRACT_CHECK`
- `REGRESSION_CHECK` — DEMONSTRATED/LIKELY/POSSIBLE/DISMISSED;
- `REVIEW_FINDINGS` — findings con evidencia, severidad, confianza y validación necesaria;
- `EVIDENCE_GAPS`
- `VERDICT` — CLEAN_WITHIN_SCOPE/CHANGES_REQUIRED/BLOCKED_FOR_EVIDENCE/PARTIAL_REVIEW.

El VERDICT del Reviewer **no autoriza merge ni deploy**. Reviewer no sustituye Quality ni Security.

## Permisos de hijos

Requeridos:

- `glob`
- `grep`

Opcional según el host:

- `lsp`

Denegados:

- `read`
- `edit`
- `write`
- `apply_patch`
- `bash`
- `task`
- `skill`
- `agent_manager`
- `external_directory`
- `board_read`
- `board_post`
- herramientas MCP namespaced, excepto allowlists explícitas por agente

### Nota de compatibilidad Kilo

La certificación runtime V2-R original detectó que Kilo exponía `list_mcp_resources`, `list_mcp_resource_templates` y `read_mcp_resource` a los hijos.

La causa está en Kilo actual: esas tres tools genéricas se clasifican internamente bajo el permiso `read`. Con `read: allow`, permanecen visibles aunque las tools MCP namespaced estén denegadas.

V2-R.1 priorizó aislamiento MCP estricto:

```yaml
read: deny
glob: allow
grep: allow
lsp: allow
```

Así los especialistas mantienen inspección local no mutable, pero pierden la herramienta `read` directa y, con ella, la exposición de los recursos MCP genéricos.

### LSP adaptativo en V2-R.2

La segunda certificación runtime confirmó que `glob` y `grep` están disponibles, mientras que `lsp` no aparece en el inventario del host actual.

Esto no es un fallo de ACL. En Kilo actual, la tool `lsp` se registra únicamente cuando el host habilita la bandera experimental `KILO_EXPERIMENTAL_LSP_TOOL`. Por tanto:

- `lsp: allow` significa "permitirla si existe";
- no significa "forzar que Kilo la registre";
- V2-R.2 exige `glob` + `grep`;
- `lsp` es una capacidad opcional;
- no se activa ninguna bandera experimental global automáticamente.

### Estado runtime del source 2.2

Los cambios en GitHub **no modifican Kilo Desktop por sí solos**. Hasta ejecutar explícitamente el instalador/sincronización y recargar Kilo Desktop:

- la baseline source tiene 10 especialistas;
- el runtime instalado puede seguir usando definiciones anteriores hasta sync/install + reload;
- las definiciones actuales source 2.2 deben considerarse `RUNTIME_NOT_VERIFIED` como conjunto;
- no se hereda el PASS histórico de `vx-dev-backend-data` a Backend/Data ni a los nuevos Platform/Reviewer;
- la evidencia Wave 1 de Research/Architect solo acredita las capacidades ejercitadas en aquella sesión, no todo el prompt source actual.

## Instalación

El instalador canónico continúa siendo:

```powershell
$script = '.\scripts\Instalar-DevTeam-Only.ps1'
pwsh -NoProfile -File $script -Modo Diagnostico
pwsh -NoProfile -File $script -Modo Simular
pwsh -NoProfile -File $script -Modo Aplicar
pwsh -NoProfile -File $script -Modo Verificar
```

La semántica de “Only” es: **Dev Team es el único modo personalizado visible aprobado**. Los diez especialistas son internos y `hidden: true`.

## Seguridad

El instalador:

- preserva `kilo.jsonc` byte-a-byte;
- no modifica ni autentica los 13 MCP;
- preserva agentes/skills de terceros;
- retira agentes VX legacy no aprobados;
- crea backup reversible;
- puede restaurar backups V1 y V2-R.

## Evidencia requerida antes de V2-W

Antes de permitir cualquier subagente escritor:

1. Kilo debe mostrar solo `vx-dev-team` en el selector;
2. el líder debe delegar exitosamente a al menos Explorer y Architect;
3. un hijo debe ser incapaz de editar y ejecutar shell;
4. el padre debe recibir solo el resultado estructurado;
5. una tarea simple no debe invocar agentes innecesarios;
6. una tarea compleja debe mantener máximo 2-4 especialistas salvo excepción explícita;
7. no debe cambiar `kilo.jsonc` ni la lista de MCP.

## Dirección actual de evolución

Las WAVE de recertificación quedan pausadas mientras se pule el diseño operativo del equipo.

Prioridad actual:

1. mantener `vx-dev-team` como coordinador único visible;
2. conservar diez especialistas read-only, una sola profundidad y deny-by-default;
3. mantener MCP tool-by-tool únicamente para Research/Architect;
4. validar en CI la baseline source 2.2;
5. desplegar/sincronizar explícitamente source → Kilo Desktop solo cuando el operador lo solicite;
6. ejecutar reload + smoke runtime fresco antes de declarar las definiciones actuales certificadas.

`vx-dev-platform` y `vx-dev-reviewer` ya existen en el source y forman parte de la ACL del líder; no tienen permisos operacionales adicionales.

## Próxima fase

- `vx-dev-explorer` ya usa el contrato `CODE_MAP / IMPACT_SURFACE`;
- `vx-dev-research` ya usa `SOURCE_LEDGER / CONTRADICTIONS` y su allowlist documental;
- `vx-dev-architect` ya usa `OPTIONS / TRADEOFFS / CONTRACTS / DECISIONS_REQUIRED` y su allowlist documental;
- `vx-dev-frontend` ya usa `UI_FLOW / COMPONENT_MODEL / STATE_MODEL / INTERACTION_STATES / ACCESSIBILITY_RESPONSIVE / API_TOUCHPOINTS`;
- `vx-dev-quality` ya usa `INVARIANTS / TEST_MATRIX / TEST_ORACLES / REGRESSION_SURFACE / ACCEPTANCE_GAPS / VERIFICATION_PLAN`;
- `vx-dev-security` ya usa `ASSETS / TRUST_BOUNDARIES / ATTACK_SURFACE / ACCESS_CONTROL / DATA_EXPOSURE / ABUSE_CASES / THREAT_FINDINGS`;
- `vx-dev-platform` ya usa `RUNTIME_MAP / BUILD_RELEASE_PATH / CONFIG_BINDINGS / DEPLOYMENT_RISKS / VALIDATION_PLAN / ROLLBACK_PLAN`;
- `vx-dev-reviewer` ya usa `REVIEW_SCOPE / REQUIREMENT_CHECK / CONTRACT_CHECK / REGRESSION_CHECK / REVIEW_FINDINGS / VERDICT`;
- mantener el runtime actual estable hasta una sincronización explícita;
- siguiente gate: CI source 2.2 → sync/reload opcional → smoke runtime fresco.
