# Investigación — Dev Team Skills Pack V1

**Fecha:** 2026-11-19  
**Resultado:** síntesis aplicada al pack original `vx-dev-skill-pack-v1`  
**Estado runtime:** inactivo

## Alcance

Se investigaron cinco frentes:

1. especificación y diseño de Agent Skills;
2. Kilo Skills + permisos;
3. MCP y seguridad;
4. ingeniería de proyecto/equipo;
5. UX/UI, accesibilidad y rendimiento.

Se priorizaron fuentes oficiales y repositorios mantenidos por equipos/practicantes. El pack no copia cuerpos de skills externas; transforma los patrones relevantes al modelo Dev Team certificado.

## Hallazgos de Agent Skills

### Agent Skills Specification

Fuente: https://agentskills.io/specification

Patrones adoptados:

- directorio por skill;
- `SKILL.md` obligatorio;
- `name` igual al directorio;
- `description` explica qué hace y cuándo usarla;
- progressive disclosure;
- instrucciones principales compactas;
- recursos adicionales solo si son necesarios.

Decisión VX:

- no usar `allowed-tools` experimental;
- permisos se controlan exclusivamente en Kilo;
- V1 sin scripts.

### Anthropic — Agent Skills

Fuente: https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills

Patrones adoptados:

- construir skills desde gaps reales;
- evaluar triggering;
- iterar con evidencia;
- separar metadata, instrucciones y recursos;
- vigilar over/under-triggering.

Decisión VX:

cada skill tiene evals `should_trigger` y `should_not_trigger`.

### Kilo Code Skills

Fuente: https://kilo.ai/docs/customize/skills

Patrones adoptados:

- Kilo descubre metadata al iniciar/reload;
- el modelo decide activación por `description`;
- skills globales viven en un pool compartido;
- la tool `skill` usa el permission system;
- user-level skills son trusted y pueden soportar shell injection.

Decisión VX:

- descripciones específicas;
- allowlist exacta por skill;
- prohibido shell injection;
- recertificación completa al instalar el pack.

## Hallazgos MCP

### MCP Specification

Fuente: https://modelcontextprotocol.io/specification/2025-11-25

Principios adoptados:

- consentimiento y control del usuario;
- privacidad;
- tool safety;
- descripciones/annotations no son enforcement;
- acceso a datos y operaciones debe ser comprensible y autorizado.

### OWASP MCP Security Cheat Sheet

Fuente: https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html

Riesgos incorporados:

- excessive permissions;
- tool poisoning;
- tool shadowing;
- confused deputy;
- data exfiltration;
- supply chain;
- prompt injection en outputs;
- schemas demasiado amplios.

Decisión VX:

separar `vx-dev-mcp-readonly` de `vx-dev-mcp-security`.

Research/Architect usan MCP. Security audita MCP sin necesitar acceso a las tools.

## Ingeniería de proyecto y equipo

### Google Engineering Practices

Fuente: https://google.github.io/eng-practices/

Patrones adoptados:

- cambios pequeños y autocontenidos;
- tests junto al comportamiento;
- revisión rápida pero rigurosa;
- evitar complejidad innecesaria;
- reviewer con suficiente contexto.

### GitHub branch protection

Fuente: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches

Patrones adoptados:

- PR;
- status checks;
- reviews;
- resolución de conversaciones;
- evitar force/delete en ramas importantes.

### ADR

Fuentes:
- https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/welcome.html
- https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html

Patrones adoptados:

- ADR solo para decisiones significativas;
- contexto, decisión y consecuencias;
- historial y supersesión;
- almacenamiento versionado.

### Short-lived branches / CI

Fuentes:
- https://microsoft.github.io/code-with-engineering-playbook/agile-development/branching-and-cicd/
- https://martinfowler.com/articles/branching-patterns.html

Patrón adoptado:

ramas temporales pequeñas + PR + CI + limpieza después de merge, sin convertir esto en regla rígida de tiempo para todo proyecto.

## UX/UI

### WCAG 2.2

Fuente: https://www.w3.org/WAI/WCAG22/quickref/

Incorporado:

- keyboard;
- no keyboard traps;
- focus visible;
- focus not obscured;
- labels/nombres accesibles;
- target size;
- errores y semántica.

### Core Web Vitals

Fuente: https://web.dev/articles/vitals

Se usan como referencia cuando existe medición:

- LCP;
- INP;
- CLS.

No se inventan valores ni se declara performance PASS sin medición.

### USWDS

Fuente: https://designsystem.digital.gov/documentation/accessibility/

Patrones adoptados:

- componentes accesibles no garantizan producto accesible;
- pruebas manuales + automáticas;
- responsive y continuidad;
- claridad en procesos.

### Vercel Agent Skills / Web Interface Guidelines

Fuente: https://github.com/vercel-labs/agent-skills

Patrones observados:

- skills específicas para review UI;
- categorías pequeñas y accionables;
- accesibilidad, forms, focus, interaction, layout, performance, theming.

Decisión VX:

no crear una “mega skill UX”. Se divide en:

- `vx-dev-frontend-ux`;
- `vx-dev-accessibility`;
- `vx-dev-ui-state-system`.

## Repositorios de skills estudiados como referencia

### Addy Osmani — agent-skills

https://github.com/addyosmani/agent-skills

Patrones útiles:

- lifecycle claro;
- skills composables;
- source-driven decisions;
- test/review/ship separados.

### Anthropic Skills

https://github.com/anthropics/skills

Patrones útiles:

- ejemplos reales;
- skill creator orientado a evals;
- recursos progresivos.

### Vercel Labs

https://github.com/vercel-labs/agent-skills

Patrones útiles:

- frontend/React/UI con scopes concretos;
- descripciones de triggering específicas.

### Cloudflare Security Audit Skill

https://github.com/cloudflare/security-audit-skill

Patrones útiles:

- guidance mode separado de auditoría completa;
- trust boundaries reales;
- no ejecutar target code si el sandbox no es suficiente;
- confirmed/needs-validation/rejected.

Estos patrones fueron reinterpretados; no se copiaron instrucciones extensas ni scripts.

## Resultado de diseño

El pack VX Dev V1 contiene 18 skills propias.

Principales decisiones:

- no heredar automáticamente las 31 legacy;
- no instalar skills externas;
- no usar scripts en V1;
- no usar shell injection;
- no usar `allowed-tools`;
- exact allowlist por nombre;
- separación clara MCP usage vs MCP security;
- UX dividida por responsabilidades;
- testing separado de ejecución;
- Reviewer separado de Quality/Security;
- activación = recertificación completa.

## Próximo gate

Antes de activar:

1. CI source PASS;
2. revisión de las 18 descripciones;
3. simulación de instalador;
4. backup;
5. aprobación explícita;
6. Apply único;
7. reload Kilo Desktop;
8. runtime certification completa;
9. evals de triggering;
10. tuning con version bump.
