# Dev Team Skills Activation V1

**Estado:** `SOURCE_CANDIDATE_NOT_RUNTIME_CERTIFIED`  
**Runtime protegido:** Dev Team 2.3.0 `PASS_OPERATOR_RUNTIME`  
**Rama candidata:** `work/dev-team-skills-activation-v1`

## Alcance

Esta rama prepara la Fase S1 del pack de 18 skills sin declarar que el runtime local ya cambió.

Cambios de source:

- 11 agentes con `permission.skill` deny-by-default + allowlists exactas;
- 18 skills administradas bajo `~/.kilo/skills`;
- instalador con backup/restore, simulación, aplicación y verificación de hashes;
- limpieza de skills VX legacy no aprobadas;
- preservación de `kilo.jsonc`;
- sin ampliación de permisos edit/write/bash/task;
- sin ampliación de MCP.

## Invariante de seguridad

Una skill es conocimiento/procedimiento, no autoridad. La carga de una skill nunca concede herramientas que la ACL del agente no permita.

Research y Architect conservan exactamente sus cinco MCP documentales ya certificados. Security solo recibe la skill de revisión de seguridad MCP; no recibe acceso MCP nuevo.

## Estado de runtime

Todavía no se afirma instalación local.

Antes de promover esta rama deben existir evidencias reales de operador:

1. `-Modo Diagnostico`;
2. `-Modo Simular`;
3. backup válido;
4. una ejecución explícita de `-Modo Aplicar`;
5. `-Modo Verificar` con 18/18 skills y 11/11 agentes;
6. `/reload` o reinicio fresco de Kilo;
7. smoke positivo de las 18 skills permitidas;
8. deny de al menos una skill no permitida por cada agente;
9. contratos de rol 10/10;
10. enforcement no-skill 10/10;
11. MCP Research 5/5 y Architect 5/5 sin cambios;
12. routing del líder PASS;
13. cero mutaciones producidas por contenido de skills.

## Política de merge

No se debe promocionar esta rama como baseline runtime certificada únicamente porque CI pase.

CI valida source. La certificación del runtime requiere evidencia de la instalación real.
