---
name: vx-team-bootstrap
description: "Inicio del pack unificado: seleccionar perfil de proyecto, comprobar instrucciones locales, distribuir permisos por rol y coordinar fases y resultados paralelos con un único líder visible."
metadata:
  version: "1.0.0"
  origin: "vx-unified"
---

# VX — Inicio, sincronización y gobierno del equipo

**Solo `vx-dev-team` es principal visible.** Esta skill gobierna la primera decisión de cada tarea; no lanza automáticamente procesos, subagentes, Git, MCP ni cambios de permiso. Las skills no elevan la ACL del host. El modo Auto sigue siendo elección del operador; `ask` permanece en escritura y shell según rol.

## Inicio proporcional y mínimo

1. **Intención:** detectar si es consulta, revisión, microcambio o desarrollo por fases. Para microcambio, leer lo indispensable, aplicar una modificación y probar; **no** invocar todo el equipo ni generar un roadmap artificial.
2. **Identidad de proyecto:** leer `git remote -v`, raíz, archivos `AGENTS.md` y guías del proyecto *solo con las herramientas permitidas*, o usar una identificación exacta proporcionada por el usuario. Emparejar con `routing.project_profiles` del registro global; no activar una skill por una coincidencia vaga de palabras. Repositorios con un mismo nombre comercial pero distinto subproducto requieren una selección explícita de carpeta.
3. **Precedencia:** restricciones del usuario y reglas del proyecto (AGENTS, GOVERNANCE, STATUS, documentación canónica) prevalecen sobre recomendaciones generales de este pack cuando son más específicas o estrictas. Global-only se refiere a instalación de agentes/skills en HOME; **no** borrar ni reemplazar instrucciones propias de proyectos ya existentes.
4. **Meta y plataforma:** `FINAL_GOAL`, `PLATFORM_SCOPE`, `BASELINE`, entregable inmediato, criterio de aceptación y permiso disponible; para trabajo complejo cargar `vx-desarrollo-escalonado` si está en la ACL.
5. **Ruta de especialización:** cada builder carga su skill de dominio únicamente si está autorizada por su **allowlist exacta**. El líder no necesita cargar todas las skills; pasa el perfil, fuentes locales y evidencia conocida en el handoff.
6. **Contexto compartido ligero:** líder conserva **un ledger de tarea**, no una base de datos persistente: `goal, project_profile, base_sha|GIT_UNBORN_HEAD|GIT_NOT_APPLICABLE, phase, task_id, owner, allowed_paths, depends_on, contract_version, state, evidence`. Se comparte con los hijos solo el fragmento mínimo para su trabajo. **No guardar secretos, clientes, credenciales, contenido privado ni correos**.
7. **Planificación:** usar DAG `PARALLEL_SAFE` existente como asesor no ejecutor; como máximo cuatro hijos en background y dos escritores de archivos exactos disjuntos (o worktrees realmente aislados). `task(background:true)` solo si el host ofrece ese parámetro. Si el hijo depende de otro contrato aún inestable, esperar o usar foreground.
8. **Propiedad efectiva:** `task` no crea worktrees ni locks. No compartir cambios Git/lockfiles, dependencias o scripts que muten directorios ajenos entre escritores; no permitir que líder o QA toquen archivos reservados mientras la fase está activa. El permiso `ask` puede ser resuelto por Auto sin diálogo; eso **no** autoriza firewall, secretos, despliegues, migraciones, borrados o cambios de ACL.
9. **Handoff:** el hijo responde `status, task_id, files_changed, tests_executed, contract_version, evidence, blockers`. Solo líder actualiza ledger; `DONE` es entrega del hijo, nunca `VERIFIED`. Al recibir varios resultados, cotejar diff real y versiones de contrato antes de ejecutar tests focalizados.
10. **Barrera y continuación:** al terminar escritores, resolver imports/archivos compartidos mediante un único dueño, probar, revisar independientemente cuando hay riesgo, integrar con reglas Git del proyecto y marcar `VERIFIED` solo con evidencia. Tras un avance, actualizar el roadmap **vivo**, no crear reportes acumulativos. Ante interrupción: `HOLD_RECHECK`; no invocar de nuevo hijos de forma ciega.

## Escalones de autorización

| Nivel | Ejemplos | Regla |
| --- | --- | --- |
| R0 lectura | localizar, comparar, proyectar cambios | Permitido solo si la herramienta efectiva lo permite; no leer secretos |
| R1 código y pruebas | editar `allowed_paths` exactos y ejecutar tests específicos | Builder `edit/write/apply_patch: ask`, shell `ask` si lo necesita; Auto lo resuelve según host |
| R2 integración Git | rama/commit/PR/CI del proyecto autorizado | Solo integrador dueño del checkout y reglas específicas del repo; no forzar push ni borrar ramas ajenas |
| R3 infraestructura o datos sensibles | producción, permisos IAM, DNS/firewall, D1 remota, migración destructiva, driver Windows, firma, pagos | Necesita autorización específica adicional, evidencia, evaluación de riesgo y rollback; un R1 no la sustituye |
| R4 no permitido | exfiltración, secretos en logs, evadir un bloqueo del host, impersonación, alterar ACL o MCP para terminar tarea | BLOQUEADO |

## Sincronización con `main`

Un `MAIN_ADVANCED` comprobado es **señal de reconciliación**, no autorización de rebase ni trigger de escritura. El líder pausa las tareas afectadas en punto seguro, verifica rama y diff, decide actualizar contratos y pruebas, y retoma solo con base coherente. Un hijo no debe cambiar la rama compartida mientras otro trabaja. Solo el dueño autorizado archiva y elimina su rama después de verificar merge, CI y copia histórica requerida.

## Estado honesto

`BOOTSTRAP_SOURCE_READY` significa que existen estas instrucciones; no demuestra `BACKGROUND_RUNTIME_PASS`, locks de archivos, coordinación intersesión ni instalación en el PC. No generar timers o monitorizadores sin pedido expreso.
