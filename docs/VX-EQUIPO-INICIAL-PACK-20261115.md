# VX Evolution — Equipo inicial de desarrollo del Pack VX (propuesta de diseño)

**Fecha:** 2026-11-15. **Estado:** PROPUESTA PARA DECISIÓN; no crear ni cambiar agentes activos, skills, permisos, MCP, `kilo.jsonc`, modelos, HOME, scheduler ni scripts de instalación. **Propiedad:** únicamente agentes y skills del Pack VX (VX-D14). **Entorno objetivo:** Kilo built-in más componentes personalizados VX (VX-D16).

## 1. Diferenciar tres conceptos

1. **Agente nativo Kilo**: proporcionado por Kilo (p. ej., `code` / `plan` según runtime). No pertenece a VX; no se copia, renombra, modifica ni mantiene por el Pack.
2. **Agente VX personalizado**: archivo Markdown `agents/vx-*.md` del Pack, con función/mode/permisos; sus versiones y mejoras sí están dentro del gobierno VX.
3. **Subagente**: un agente invocado como delegado para una tarea delimitada con contexto aislado y resultado al padre; no es necesariamente otro modelo ni otro proceso residente. El modo `subagent` restringe su uso y no convierte un lector en escritor.

Las skills dan instrucciones bajo demanda; los MCP exponen herramientas externas: no son agentes, no se cuentan como integrantes. El selector PowerShell actual devuelve un plan, **no lanza agentes**.

## 2. Catálogo inicial real del repositorio (V4 vigente)

| ID estable | Modo actual | Especialidad | Escribe | Uso en equipo |
| --- | --- | --- | --- | --- |
| `vx-integrador` | `primary` | Coordinación técnica, planificación, integración, verificación y cierre Git | Sí, escritor único si hay tarea autorizada | **Coordinador principal**; recibe la solicitud del operador |
| `vx-researcher` | `subagent` | Investigación del código, dependencias, APIs y hechos con referencias | No | Descubrimiento antes de diseñar |
| `vx-test-analyst` | `subagent` | Estrategia QA, casos límite, pruebas, regresiones y cobertura | No | Definir pruebas antes/después |
| `vx-security-reviewer` | `subagent` | Autenticación, permisos, secretos, abuso y seguridad | No | Análisis de amenazas y revisión independiente |
| `vx-inspector` | `subagent` | Revisión independiente de diffs, defectos y coherencia de evidencia | No | Control de calidad de cambios antes de PR/merge |
| `vx-frontend-adviser` | `subagent` | UX/UI, HTML/CSS/React, accesibilidad y rendimiento | No | **Solo por demanda** en tareas visuales |
| `vx-workers-adviser` | `subagent` | Cloudflare Workers, KV/R2/D1/queues, bindings y riesgos | No | **Solo por demanda** en infraestructura Workers |

**No crear nuevos agentes equivalentes sin comprobar brecha funcional.** Los siete nombres actuales se mantienen como candidatos de la primera versión del Pack. Ningún rango `junior/senior/líder` se atribuye por la descripción; V4.6 solo tiene evidencia declarativa y pruebas sintéticas.

### Primera escuadra operativa de desarrollo VX

- **Coordinación y único escritor:** `vx-integrador`. Kilo `code` nativo sigue disponible en el entorno limpio para trabajo directo, pero no trabaja a la vez como segundo escritor de la misma rama; para implementaciones normales se puede elegir uno u otro como responsable, no ambos simultáneamente.
- **Descubrimiento:** `vx-researcher`.
- **Diseño de pruebas:** `vx-test-analyst`.
- **Revisión de seguridad:** `vx-security-reviewer` cuando hay archivos sensibles, instalación, permisos, autenticación, suministro de paquetes o MCP.
- **QA final:** `vx-inspector` después del diff. Su dictamen no sustituye pruebas ni aprobación humana.
- **Especialistas opcionales:** `vx-frontend-adviser` y `vx-workers-adviser` solo en proyectos de esas clases.

**Regla de capacidad inicial:** hasta 3 lectores concurrentes **cuando sea útil** y **un escritor máximo**. No invocar los seis subagentes en cada cambio; tareas triviales pueden usar cero. Los subagentes no ejecutan ni manipulan archivos: el coordinador debe ejecutar y comprobar pruebas reales si cuenta con permisos. Las skills del Pack actual son `vx-engineering-harness` y `vx-evolution-core`; otras citadas en perfiles V4 son sugerencias, **no son componentes automáticamente incluidos**.

## 3. Primer ciclo de desarrollo propuesto

1. **Solicitud:** operador describe objetivo, alcance, aceptación, repositorio y riesgos. El coordinador abre expediente mínimo con tarea y versión.
2. **Diagnóstico:** `vx-researcher` localiza fuentes; `vx-test-analyst` define pruebas; seguridad/UX/Workers entra solo si corresponde.
3. **Plan:** el coordinador sintetiza hallazgos, distingue `HECHO`, `DECLARADO`, `NO_VERIFICADO`, `NO_MEDIDO`, acuerda cambios mínimos. No cambiar permisos ni publicar automáticamente.
4. **Construcción:** crear una única rama `work/*` solo si procede y el entorno está limpio; **un único escritor** (`vx-integrador` o un turno separado de Kilo `code`). Sin worktrees paralelos salvo consentimiento explícito.
5. **Pruebas:** ejecutor autorizado corre unit/integration/build y registra códigos de salida; el analista de pruebas no afirma haberlas ejecutado. Tests sintéticos no equivalen a validación en Kilo real.
6. **Revisión:** `vx-inspector` revisa diff y cobertura; `vx-security-reviewer` analiza solo riesgos específicos distintos. Corregir, volver a comprobar, abrir PR.
7. **Integración:** CI PASS, revisión, autorización de merge según política, validación de `main`, limpieza de rama temporal propia. No deploy ni tocar HOME real sin autorización específica.
8. **Evolución:** con evidencia real, VX registra oportunidad de mejorar un componente VX, genera candidato versionado y lo somete al mismo ciclo. No promoción automática ni autoaprobación.

### Ejemplos de selección contextual

| Tarea | Lectores previos | Implementa | Cierre |
| --- | --- | --- | --- |
| Contrato de aprobación VX | Researcher + Security + Test | Integrador | Inspector + CI |
| Script de respaldo/instalador VX | Researcher + Security + Test | Integrador | Inspector + pruebas de rollback en HOME sintético |
| Interfaz de diagnóstico VX | Frontend + Test (Researcher opcional) | Integrador o Code por turno | Inspector + pruebas visuales reales cuando disponibles |
| MCP catálogo VX | Researcher + Security | Integrador | Test + Inspector (sin conectar servidores de terceros) |
| Cambios en Workers ajenos a VX | Fuera de la administración **VX Evolution**; solo equipo Kilo usado para desarrollo autorizado del proyecto del usuario, no evolución del agente ajeno | Kilo Code según tarea autorizada | Nunca publicar tercero como actualización VX |

## 4. Expansión futura, sin crear agentes ahora

Los huecos probables a estudiar con pruebas reales son especialista de instalador/Windows, curador de catálogo MCP, analista de métricas y responsable de documentación. **Inicialmente son capacidades o skills candidatas para el equipo existente**, no nuevos agentes preinstalados. Solo añadir un agente VX cuando exista una necesidad repetida, test de valor incremental contra configuración de un solo agente, revisión de permisos, versión/manifest y aprobación.

## 5. Puertas de aceptación antes de activar el primer equipo

- Verificar sintaxis/configuración global de los siete Markdown y registro V4; que Kilo los muestre, sin duplicados de otras fuentes.
- Probar una delegación `task` de solo lectura con evidencia de identidad del ejecutor y salida; una sesión `completed` por sí sola no verifica llamada interna a skill.
- Probar una tarea VX sintética con único escritor, pruebas, revisión independiente y cierre Git.
- Registrar coste/tiempo solo cuando exista medición auténtica; ninguna puntuación de seniority hasta V4.8.
- Si hay problemas, mantener los siete roles existentes, con orquestación secuencial y bloqueo de publicación hasta solucionarlos.

## 6. Pregunta pendiente de dirección

**¿Confirma el operador los siete nombres actuales como lista inicial oficial del Pack VX y la regla de un único escritor sin crear más agentes ahora?** Esta propuesta **no es autorización de instalación ni cambio de permisos**.

Fuentes internas: `agents/vx-*.md`, `registry/vx-agent-registry-v4.json`, `docs/OPERACION-EQUIPOS-V4.md`, `docs/VX-EVOLUTION-ROADMAP.md`. Documentación Kilo: https://kilo.ai/docs/customize/custom-subagents y https://kilo.ai/docs/customize/custom-modes.
