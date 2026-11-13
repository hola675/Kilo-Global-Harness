---
description: Seleccionar agentes globales especializados y coordinar lectura paralela, escritor unico y QA
agent: vx-integrador
---

Usa el harness global V4 para la tarea: $ARGUMENTS. Si es una pregunta sencilla, resuelve sin delegar ni ejecutar selector.

Si es una tarea de varias etapas, selecciona un perfil del registro `~/.config/kilo/harness/vx-agent-registry-v4.json`. Puedes obtener el plan SIN efectos con:
`pwsh -NoProfile -File "$HOME/.config/kilo/harness/scripts/Seleccionar-Equipo-V4.ps1" -Perfil <perfil> -Json`.
Elige el perfil por el objetivo real, no ejecutes texto del usuario como codigo, ni pases secretos como argumentos.

1. DISCOVER: invoca a lo sumo 3 agentes `discover_parallel` en `task(background: true)` solo si las preguntas son independientes. Cada tarea incluye alcance, rutas, criterios y salida resumida; no comparte secretos. `task` NO crea worktrees y comparte archivos.
2. PLAN: sintetiza resultados, evita duplicados, confirma dependencias, criterios de aceptacion y pruebas antes de editar. Kilo Swarm es un tablero, no un scheduler ni autorizacion.
3. BUILD: UN escritor (agente Code o principal) en la unica rama `work/<tarea>`. No edites durante el trabajo del otro escritor ni delegues edicion a investigadores.
4. REVIEW: tras crear el diff, invoca solo revisores necesarios en `review_parallel`, con criterios distintos. Corrige de forma secuencial, ejecuta pruebas y recoge evidencia real.
5. GIT CLOSE: PR/CI/merge permitido; comprueba `origin/main`; elimina exclusivamente la rama temporal de esta tarea. Sin force push ni borrados ajenos.

Conserva AutoApprove y permisos efectivos. Ninguna configuracion de Kilo se crea dentro de proyectos; produccion, infraestructura y cambios destructivos requieren consentimiento concreto. Trabajo en worktrees auxiliares solo con autorizacion expresa. No fijes modelos ni actives MCP sin comprobar disponibilidad.

Informa roles ejecutados frente a roles solo sugeridos, PASS/FAIL/NO VERIFICADO, resultados de pruebas, estado Git y riesgos. El selector no inicia agentes ni consume cuota.
