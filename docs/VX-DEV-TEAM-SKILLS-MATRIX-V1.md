# Dev Team Skills Matrix V1

**Estado:** `PROPOSAL_INACTIVE`  
**Baseline protegida:** Dev Team 2.3.0 `PASS_OPERATOR_RUNTIME`  
**Objetivo:** introducir skills por allowlist mínima sin convertir el Dev Team en un segundo Pack VX ni invalidar innecesariamente la certificación actual.

## Principio

Una skill aporta contexto/procedimiento. **No concede permisos.**

La baseline actual mantiene:

- 1 líder visible;
- 10 especialistas ocultos;
- hijos read-only;
- `skill: deny`;
- MCP deny-by-default;
- depth=1.

Mientras esta propuesta esté inactiva, ninguno de esos permisos cambia.

## Inventario

El repositorio contiene **31 skills VX**.

La matriz V1 las clasifica en:

- **DIRECT: 12** — contenido razonablemente compatible con el rol sin adaptación previa;
- **ADAPT: 9** — mezcla implementación, ejecución o roles legacy y requiere variante Dev-Team;
- **EXCLUDE_BASELINE: 10** — especialización de proyecto/legacy o contradice la arquitectura del Dev Team.

Registro canónico:

`registry/dev-team-skills-matrix-v1.proposal.json`

## Wave S1

La primera activación propuesta afecta solo a cuatro especialistas:

| Agente | Skill |
|---|---|
| `vx-dev-explorer` | `vx-codebase-investigation` |
| `vx-dev-architect` | `vx-architecture-decisions` |
| `vx-dev-data` | `vx-data-contracts` |
| `vx-dev-security` | `vx-security-review` |

Los otros seis especialistas y el líder permanecen sin cambios.

### Forma de permiso prevista

No se usará `skill: allow` global.

Cada agente afectado usará un mapa exacto:

```yaml
skill:
  "*": deny
  "<skill-id-aprobada>": allow
```

Así la tool `skill` puede existir, pero solo carga la skill allowlistada.

## Fuentes congeladas

El instalador DevTeam-Only actual elimina todos los directorios `vx-*` de:

- `~/.kilo/skills`
- `~/.agents/skills`
- `~/.kilocode/skills`

Por tanto S1 no puede depender de que el Pack VX histórico siga instalado.

Antes de activar S1, las cuatro skills se copiarán a:

`runtime/dev-team-v2r/skills/<skill-id>/SKILL.md`

Esas copias serán las fuentes canónicas del Dev Team. Esto evita que una edición futura del Pack VX cambie silenciosamente una skill ya certificada.

En runtime se instalarán únicamente en:

`~/.kilo/skills/<skill-id>/SKILL.md`

Los roots de compatibilidad seguirán sin contener skills VX aprobadas del Dev Team.

## Instalador

S1 requerirá una modificación explícita de `Instalar-DevTeam-Only.ps1` para:

1. administrar exactamente las cuatro skills aprobadas;
2. incluirlas en diagnóstico/simulación;
3. respaldar targets existentes;
4. instalar/actualizar solo esas cuatro;
5. seguir retirando cualquier otra `vx-*` legacy;
6. verificar hashes source↔runtime;
7. restaurar skills junto con agentes en rollback;
8. conservar `kilo.jsonc` byte-a-byte.

No habrá instalación silenciosa: solo mediante `-Modo Aplicar` después de CI, simulación y autorización.

## Seguridad de contenido

Wave S1 exige:

- sin `!\`command\`` embebido;
- sin scripts ejecutables requeridos;
- sin cambios a `edit/write/apply_patch/bash/task`;
- sin cambios MCP;
- sin Agent Manager/Board;
- sin ampliación de profundidad.

## Recertificación

Activar `permission.skill` cambia la ACL de los cuatro especialistas y, por tanto, invalida **solo su certificación runtime individual**.

La recertificación S1 deberá demostrar por cada uno:

1. subtarea fresca desde `vx-dev-team`;
2. `glob/grep` siguen disponibles;
3. tool `skill` disponible;
4. skill allowlistada carga correctamente;
5. skill no allowlistada segura devuelve `DENIED`;
6. edit/write/apply_patch/bash/task siguen denegadas;
7. MCP no cambia;
8. contrato de rol sigue PASS;
9. no hay mutaciones.

Los otros seis especialistas conservan su PASS si sus archivos, ACL y host semantics no cambian.

## S2

Después de S1 se evaluarán, sin activación automática:

- líder: requirements / implementation handoff / release readiness;
- Research: MCP safe integration;
- Frontend: accessibility review;
- Data: SQL query performance;
- Platform: release readiness + observability/privacy;
- Quality: requirements/acceptance;
- Security: supply-chain review.

## S3 — adaptaciones

No se activarán directamente skills que contradigan contratos read-only.

Gaps previstos:

- Backend: API contract/root-cause en variante analítica;
- Frontend: frontend quality read-only;
- Quality: test strategy/regression read-only;
- Research: source reconciliation/traceability;
- Reviewer: independent change review;
- líder: task dependency graph compatible con depth=1.

## Estado actual

```text
DEV_TEAM_RUNTIME_CERTIFICATION: PASS_OPERATOR_RUNTIME
SKILLS_MATRIX_V1: PROPOSAL_INACTIVE
SKILLS_REPO_INVENTORY: 31
S1_TARGET_AGENTS: 4
S1_APPROVED_SKILLS: 4
RUNTIME_SKILL_CHANGES: NONE
KILO_JSONC_CHANGES: NONE
```
