---
name: vx-skill-quality
description: "Diseñar, mejorar y auditar Agent Skills globales Kilo sin duplicaciones: formato SKILL.md, activación contextual correcta, permisos, seguridad de scripts, pruebas positivas/negativas y compatibilidad Windows."
compatibility: "Agent Skills; Kilo Code y Kilo Desktop. Auditoría documental y pruebas autorizadas, sin auto-instalación de terceros."
metadata:
  version: "1.0.0"
  last_modified: "2026-11-21"
  origin: "vx-unified"
  category: "skill-engineering"
---

# VX — Ingeniería y certificación de Skills

**Activar** al crear, modificar, importar, eliminar, fusionar o evaluar habilidades. Una Skill no es un subagente ni una concesión de permiso; los roles y la ejecución pertenecen al host Kilo.

## Crear solo cuando falte una capacidad

1. Identificar tarea real y consultar el catálogo canónico; clasificar `KEEP|UPDATE|MERGE|ADD|RETIRE`. Si dos Skills resuelven la misma incertidumbre, mejorar la existente antes de crear otra.
2. Mantener las Skills por contexto y procedimiento, **nunca** por cliente, marca o repositorio. Preservar las instrucciones locales sin copiarlas a HOME global.
3. Diseñar una descripción concreta, con condiciones de activación y exclusión. Kilo selecciona Skills por descripción: comprobar que el modelo discrimina el contexto correctamente.
4. Seguir el formato abierto: directorio = frontmatter `name`, minúsculas y guiones; `name` <=64 caracteres, `description` <=1024, Markdown después de YAML. Opcionales `compatibility`, `license`, `metadata.version`. Recursos adicionales en `references/`, `scripts/` y `assets/` solo si aportan valor.
5. Las rutas canónicas de distribución son las definidas por la instalación Kilo; la existencia en `skills/` del repositorio fuente **no demuestra instalación** en `~/.kilo/skills`.

## Seguridad y confianza

- Auditar instrucciones `SKILL.md`, scripts, imports, binarios, documentación y URLs antes de cualquier importación externa. Preferir fuente original, licencia clara, revisión de commits y dependencias fijadas.
- Prohibir comandos embebidos no revisados, pipelines de descarga-ejecución, accesos a secretos, exfiltración, bypass de aprobaciones, permisos wildcard elevados y herramientas de alcance desconocido.
- No ejecutar scripts de una Skill solo porque un escáner está verde. Escaneo estático es **indicio**, no garantía. Cualquier análisis LLM externo de contenidos privados exige autorización específica.
- Aplicar política `deny` por defecto: agregar archivos no añade `permission.skill`, `task`, MCP, shell ni cambios al archivo `kilo.jsonc`.
- Si se propone activar ACL en otra etapa, registrar diferencias exactas por rol y exigir aprobación y nueva certificación de permisos observados.

## Evals focalizados, sin suites acumulativas

| Tipo | Oráculo |
| --- | --- |
| `SHOULD_TRIGGER` | Solicitud real del contexto carga únicamente la Skill pertinente si está autorizada |
| `SHOULD_NOT_TRIGGER` | Otra tecnología, dominio o tarea trivial no activa la Skill |
| `CONFLICT` | Instrucciones locales más estrictas y ACL del host prevalecen |
| `DENIED` | Falta de permiso no se resuelve con herramienta alternativa o ampliación silenciosa |
| `RECOVERY` | Entorno offline, falta de tool o interrupción reporta bloqueo sin inventar PASS |
| `INTEGRITY` | Nombre, path, frontmatter, dependencias, catálogo y enlaces coherentes |

1. Incluir 2–4 ejemplos positivos y 2–4 negativos por nueva capacidad cuando el costo lo permita; medir activación correcta, errores y contexto innecesario frente a baseline sin Skill.
2. Actualizar la suite viva correspondiente con `UPDATE|REPLACE|ADD`: añadir test solo para una nueva invariante, retirar tests supersedidos después de PASS, conservar historial en Git.
3. Validar source sin ejecutar archivos no confiables; luego tests autorizados en sandbox; finalmente sync/reload, permisos y runtime real en Kilo por separado.
4. Nunca confundir `SOURCE_PASS`, `EVAL_PASS`, `ACL_PASS`, `RUNTIME_PASS` y `INSTALLED`.

## Entrega

`{skill_id,change_action,trigger_examples,negative_examples,overlap_review,security_findings,source_validation,eval_results,acl_impact,runtime_status,rollback}`.

No publicar ni instalar automáticamente en Kilo Desktop o VS Code por haber creado un archivo en GitHub.
