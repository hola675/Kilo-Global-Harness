# Dev Team Consolidation V1

Estado: **SOURCE_CERTIFIED_RUNTIME_PARTIAL**

La consolidación source está cerrada sobre `main`. El pack canónico vigente está en `registry/dev-team-current-pack-v1.json`. No se declara que el runtime instalado sea idéntico al source actual.

## Estado por fase

1. Parser canónico — implementado.
2. Tests migrados — implementado.
3. Matriz canónica — implementada.
4. Consumidores canónicos — implementados.
5. CI — **PASS** en `Validar Kilo Global Harness` run **#511**, commit `af2f299c75a8`.
6. Snapshot visible 11/11 — flujo listo; captura runtime completa pendiente.
7. MCP exact IDs — cinco IDs documentales verificados; resto pendiente runtime.
8. Evals 44 skills — runner listo; observaciones runtime pendientes.
9. Waves — definidas, no autorizadas.
10. Preflight runtime — plan-only con SHA-256 y clasificación de deriva; **no aplicado**.

## Evidencia del Windows del operador

El preflight ejecutado el 19 de noviembre de 2026 observó:

- agentes: **6/11** byte-idénticos al source actual; 5 diferentes;
- skills CORE V1: **2/18** byte-idénticas; 16 diferentes;
- archivos faltantes: **0**;
- W1–W5: **BLOCKED**;
- aprobación del operador: **false**;
- mutación causada por preflight: **ninguna**.

Esto no borra la certificación histórica de Dev Team 2.3.0, que estaba ligada a otro snapshot source. Sí impide reutilizar aquel PASS para afirmar que la instalación actual coincide con el source posterior.

## Pack actual

El source reconciliado contiene:

- 11 agentes Dev Team: 1 líder + 10 especialistas;
- 44 skills: 18 CORE, 9 Gap Fill, 9 UX/UI Pro y 8 MCP Operations;
- 13 familias MCP canónicas;
- 5 IDs documentales exactos con evidencia runtime previa.

Las 26 skills posteriores al CORE siguen **NOT_AUTHORIZED** como waves. Tener una skill en source no concede ACL ni la activa en Kilo.

## Legacy retirado

Dos proposals iniciales sin autoridad vigente fueron retirados del árbol activo y permanecen recuperables en Git history:

- `registry/vx-dev-team-v1.proposal.json`;
- `registry/vx-dev-team-mcp-matrix-v1.proposal.json`.

Los registros de certificación histórica y evidencia runtime se conservan; no son legacy eliminable mientras aporten trazabilidad.

## Lo que ya no debe hacerse

- añadir parsers regex nuevos para `permission.skill` o `permission.task`;
- copiar matrices de roles a otros registries;
- tratar tool candidate como tool visible;
- tratar CI como runtime certification;
- activar 44 skills en una sola wave;
- restaurar propuestas V1 retiradas como autoridad;
- borrar ramas con commits exclusivos sin referencia de archivo recuperable.

## Certificación source

Run **#511** de `Validar Kilo Global Harness` completó **42/42 PASS** sobre `main`, commit `af2f299c75a842eeeee56b3a2fb4b01af607ee35`.

Este PASS certifica source/CI. No activa waves, MCP, ACL, scheduler ni modifica `kilo.jsonc`.

La limpieza final de ramas usa `scripts/Consolidar-Ramas-Main-V2.ps1`: PLAN_ONLY por defecto, archivo previo mediante tags `archive/*`, verificación SHA, `force-with-lease` remoto y CAS local. El objetivo es dejar `main` como única **rama activa**, preservando commits retirados como tags de recuperación.
