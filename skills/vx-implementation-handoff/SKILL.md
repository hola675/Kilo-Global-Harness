---
name: vx-implementation-handoff
description: "Usar en una tarea de programación VX autorizada con implementador frontend/backend; delimitar archivos, contrato de API, worktree, pruebas y entrega al integrador. No usar en preguntas rápidas ni en auditorías solo lectura."
---

# VX Implementation Handoff V0.1

**Objetivo:** programar con un contrato mínimo y transferir resultados entre Yoan, implementadores y revisores. No instala herramientas, no concede permisos y no abre ramas automáticamente.

## Puerta de entrada

**Contrato adaptable según contexto:** antes de escribir identificar responsable, workspace efectivamente autorizado, archivos específicos permitidos/prohibidos, objetivo y aceptación. Inferir `task_id`, `base_sha`, rama/worktree y pruebas del entorno cuando existan; no exigir su introducción manual si pueden verificarse. Para un proyecto Git real verificar rama/HEAD, dependencias y alcance antes de cambios relevantes. **En un laboratorio local aislado sin Git explícitamente autorizado**, registrar `GIT_NOT_APPLICABLE` en lugar de inventar SHA/rama y trabajar solo en el archivo indicado bajo la carpeta del laboratorio. Si falta autorización, identidad del workspace, ruta segura o permiso efectivo, detener la escritura y devolver un plan. Un único escritor Git por worktree. Para ediciones concurrentes de archivos **exactos y disjuntos** en un mismo workspace, exigir contrato expreso `write_scope: EXACT_FILES`, dos builders como máximo y prohibir cambios Git/lockfiles compartidos hasta la barrera. Para cambios solapados, serializar o comprobar worktrees reales; `task` no crea aislamiento.

## Progreso incremental entre implementadores — VX Progress V1

Al entregar una API/UI/dato o contrato consumible por otro builder, incluir `task_id_or_local_ref`, `owner_agent`, `contract_version`, `allowed_paths`, `interfaces_stable`, `event: MILESTONE|BLOCKED|DELIVERED`, `evidence_ref`, `next_or_blocker` y `verification_state: CLAIMED|OBSERVED|NOT_VERIFIED`. No exigir todo para una corrección trivial de un archivo.

Si Kilo Swarm y `board_post` / `board_read` están disponibles en el host bajo los permisos V2, comunicar solo el cambio de contrato y consultar actualizaciones de hermanos en la siguiente barrera natural; no usar Board como lock, autorización o entrega garantizada. Si está denegado, el avance se incorpora a `task_result` y lo distribuye el líder en los handoffs posteriores. El receptor no altera un contrato ya estable sin nueva instrucción verificada del líder.

La integración depende de `diff` y tests reales, **nunca** de un mensaje `DONE`. Para comprobar autoría de escritura, observar la transcripción de herramientas del hijo; un archivo que existe no prueba quién lo creó.

## Desarrollo Desktop preferido: Tauri 2

Si el contrato exige una aplicación de escritorio nueva, el líder usa **Tauri 2** como arquitectura preferida. Los builders que implementen frontend o comandos Rust pueden cargar la skill complementaria `vx-tauri-desktop` con su propia ACL; el líder no la carga si no aparece en su allowlist. Dividir frontend web y backend Rust por rutas exclusivas, acordar contrato IPC antes de consumirlo y reservar `tauri.conf.json`, capacidades, manifiestos/lockfiles y registro de comandos para integración después de la barrera. No reescribir proyectos existentes ni instalar toolchains/elevar capacidades sin autorización. Verificar WebView2/MSVC, Rust y tests efectivos antes de anunciar un empaquetado PASS.

## Protocolo

1. Diagnosticar solamente los módulos implicados; evitar cargar skills no relacionadas.
2. Proponer una interfaz/contrato compatible y compartirlo con el coordinador antes de tareas dependientes.
3. Editar el mínimo necesario con los permisos efectivos de Kilo. El permiso `ask` queda bajo el control efectivo del host Kilo; en Kilo Desktop el modo `Auto` configurado por el operador puede resolverlo automáticamente, y eso no debe confundirse con una autorización permanente del agente. Ninguna aprobación es transferible entre agentes. Si la tarea es independiente y hay archivos reservados exclusivos, el líder puede lanzar el builder con `task(background: true)` real y seguir con trabajo no dependiente; si no, foreground.
4. Ejecutar pruebas solo si `bash` está permitido y el comando es seguro. Sin ejecución, usar `NO_EJECUTADO`, nunca PASS.
5. Entregar rutas, diffs/commits, contratos, pruebas verificadas, riesgos, limitaciones y bloqueos. Pedir revisión independiente antes de integrar. Un resultado `DONE` no equivale a `VERIFIED`; primero esperar a los escritores en background y comprobar que nadie alteró archivos ajenos a su alcance. Los commits/rebase/merge del mismo worktree solo después de cerrar las escrituras.
6. No realizar deploy, force push, merge sin autorización, modificaciones de HOME, MCP, modelos, credenciales, AutoApprove, agentes o skills globales.

## Handoff mínimo (ejemplo ilustrativo)

En ensayos de laboratorio sin Git, usar `base_sha: GIT_NOT_APPLICABLE` únicamente como **metadato**, no como SHA válido. Los campos de salida no son puertas universales previas si la tarea localizada ya proporciona workspace, archivo, objetivo y aceptación.

```json
{
  "schema": "vx-handoff/1",
  "task_id": "tarea-ficticia",
  "agent_id": "vx-backend-builder",
  "base_sha": "NO_VERIFICADO",
  "changed_paths": [],
  "api_contracts": [],
  "tests": [],
  "limitations": [],
  "review": "PENDIENTE"
}
```

Los campos son metadatos de coordinación, **no** una señal de test o evaluación verificada.
