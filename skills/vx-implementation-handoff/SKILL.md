---
name: vx-implementation-handoff
description: "Usar en una tarea de programación VX autorizada con implementador frontend/backend; delimitar archivos, contrato de API, worktree, pruebas y entrega al integrador. No usar en preguntas rápidas ni en auditorías solo lectura."
---

# VX Implementation Handoff V0.1

**Objetivo:** programar con un contrato mínimo y transferir resultados entre Yoan, implementadores y revisores. No instala herramientas, no concede permisos y no abre ramas automáticamente.

## Puerta de entrada

Recibir identificador de tarea, responsable, repositorio, rama/worktree y base SHA, archivos permitidos/prohibidos, contrato de salida y pruebas de aceptación. Sin este alcance, detener la escritura y devolver un plan. Nunca escribir en el mismo worktree simultáneamente con otro agente. Para paralelismo real se exige autorización expresa y worktrees Git aislados; `task` no equivale a aislamiento.

## Protocolo

1. Diagnosticar solamente los módulos implicados; evitar cargar skills no relacionadas.
2. Proponer una interfaz/contrato compatible y compartirlo con el coordinador antes de tareas dependientes.
3. Editar el mínimo necesario con los permisos efectivos de Kilo. El permiso `ask` requiere aprobación real; ninguna aprobación es transferible entre agentes.
4. Ejecutar pruebas solo si `bash` está permitido y el comando es seguro. Sin ejecución, usar `NO_EJECUTADO`, nunca PASS.
5. Entregar rutas, diffs/commits, contratos, pruebas verificadas, riesgos, limitaciones y bloqueos. Pedir revisión independiente antes de integrar.
6. No realizar deploy, force push, merge sin autorización, modificaciones de HOME, MCP, modelos, credenciales, AutoApprove, agentes o skills globales.

## Handoff mínimo (ejemplo ilustrativo)

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
