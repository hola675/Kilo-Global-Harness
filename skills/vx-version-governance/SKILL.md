---
name: vx-version-governance
description: "Usar antes de cambios de archivos, código, configuración o contratos para establecer baseline Git, versión individual y rollback; no activar para consultas solo lectura."
compatibility: "Agent Skills; Kilo Code y Kilo Desktop Windows. Solo instrucciones: respeta ACL, lectura y aprobaciones del host."
metadata:
  version: "1.1.1"
  last_modified: "2026-11-22"
  origin: "vx-unified"
  category: "governance"
---

# VX — Gobernanza preventiva de versiones

**Activar al iniciar cualquier tarea que vaya a modificar archivos, configuración, contratos, dependencias o código.** Una consulta exclusivamente de lectura no necesita este gate. Esta skill no ejecuta comandos, no concede permisos ni instala nada: el líder/implementador usa solo herramientas efectivamente permitidas.

## Gate V0: baseline antes del primer cambio

1. Identificar repositorio y política local; inspeccionar `git status --porcelain`, rama/worktree, `HEAD`, remoto y última base de `main` solo si el permiso y la conectividad permiten consultarlos. Nunca suponer que el disco está limpio.
2. Registrar `BASE_SHA` (o `GIT_UNBORN_HEAD` / `GIT_NOT_APPLICABLE`), `BRANCH`, `DIRTY_PATHS`, `VERSION_SOURCE` y `CURRENT_VERSION` o `UNKNOWN`. Comprobar primero el manifiesto canónico: según stack `package.json`, `pyproject.toml`, `Cargo.toml`, `*.csproj`, manifiesto de app o release tags. No inventar números basándose en el nombre del repositorio.
3. Enumerar cambios solicitados X/Y/Z con `change_id`, rutas afectadas, contratos y consumidores. Si aparecen rutas sucias ajenas o propietarias de otro agente, **preservar** esas ediciones y marcar `OVERLAP_BLOCKED`; no hacer stash, checkout, reset ni editar encima.
4. Decidir aislamiento proporcional: microcambio en rama/tarea autorizada existente; tarea independiente en `work/*` o worktree dedicado si la política Git lo exige. No crear rama innecesaria ni operar sobre Git desde subagentes read-only.
5. Si no es posible observar el baseline, registrar `BASELINE_UNVERIFIED` y restringir mutaciones de riesgo hasta obtener evidencia; no declarar protección de rollback ficticia.

## Impacto y decisión de versión

- `DOCS_ONLY`, `INTERNAL_REFACTOR`, `BUGFIX`, `FEATURE`, `BREAKING`, `DATA_MIGRATION`, `HOTFIX`, `SECURITY`, `DEPENDENCY`: seleccionar uno o varios con justificación.
- SemVer únicamente cuando el producto ya lo adopta; no romper calendarios de releases, versionado de cuatro componentes, CalVer o versiones fijadas por fabricante.
- **PATCH / MINOR / MAJOR son propuestas**, no permisos para modificar manifests: cambios incompatibles requieren análisis de consumidores, contratos, migración y aprobación apropiada.
- No incrementar versión por cada archivo o commit. Separar `WORK_VERSION` y `RELEASE_VERSION`; tags, binarios, publicación, producción y cambios de paquete solo si son parte de la tarea autorizada.
- Para X/Y/Z registrar qué se preserva, qué cambia y el punto de recuperación (SHA/commit/tag real). No crear tags por rutina: Git ofrece historia si los commits existen; para datos externos exigir respaldo validado separado.

## Versionado individual del Harness

- En el Harness, la versión del pack y la versión de cada agente, Skill, política o script son **independientes**. La versión del pack aparece en el nombre visible del líder; no debe propagarse como versión individual de los hijos.
- Antes de editar un archivo gestionado, leer sus metadatos canónicos y el registro de su sección. Si cambia el comportamiento, incrementar solo la versión individual que corresponda según la política local; mantener fecha ISO de última modificación. Un ajuste exclusivamente documental no fuerza un release del producto.
- Resumir el cambio **solo en** `registry/AGENTS-VERSIONS.md`, `registry/SKILLS-VERSIONS.md`, `registry/POLICIES-VERSIONS.md` o `registry/SCRIPTS-VERSIONS.md` según corresponda. No introducir changelogs acumulativos en los archivos operativos.
- Los scripts y políticas pueden usar cabecera comentada en lugar de frontmatter. No insertar YAML en archivos cuyo parser o intérprete no lo admita.
- No alterar el `displayName` del líder al actualizar una Skill, script o política; ese nombre identifica la versión del Harness, no la versión individual del archivo.

## Ejecución y cierre

1. Anclar contratos y tests al baseline; un escritor Git por worktree; escribir solo rutas autorizadas.
2. Después de cada lote coherente, revisar diff y actualizar `CHANGE_LEDGER`; usar commits atómicos sujetos a política. Si `main` avanza, seguir el protocolo `MAIN_ADVANCED` sin reconciliación destructiva.
3. Test `UPDATE|REPLACE|ADD` según invariantes actuales. Distinguir `SOURCE_VALIDATED`, `CI_PASS`, `RUNTIME_PASS` y `RELEASED`.
4. Actualizar changelog/ADR únicamente si el cambio lo justifica; anotar deprecaciones, migraciones y reversión. No asumir que revertir código revierte una base de datos.
5. Antes de PR/merge verificar diff, versionado decidido, tests afectados, permisos, dependencias y rollback real. No declarar cierre por el éxito de un subagente.

## Salida obligatoria para cambios

`{base_sha,branch,dirty_paths,current_version,version_source,change_ids,change_class,affected_contracts,proposed_bump,release_decision,rollback_anchor,test_action,evidence,status}`

Estados: `BASELINE_READY`, `BASELINE_UNVERIFIED`, `OVERLAP_BLOCKED`, `CHANGE_READY_FOR_REVIEW`, `RELEASE_NOT_REQUESTED`. Ninguno equivale a licencia de edición, merge o deploy.
