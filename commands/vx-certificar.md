---
description: Verificar carga de skills, descubrimiento de agentes y delegación Kilo VX sin elevar permisos
---

# /vx-certificar — prueba nativa controlada

Objetivo: $ARGUMENTS

La evidencia aportada por el operador (P1 de 2026-11-16) reporta dos cargas exitosas por la herramienta nativa skill, captura del selector Vx Integrador activo y cinco builders visibles, y delegación nativa task a vx-inspector: primer intento BLOCKED por reiterar la comprobación visual, segundo intento completed con lectura de README declarada por el delegado. Conservar estas fuentes separadas (captura del operador, relato de salida de task, herramienta nativa); no tratarlas como certificación independiente de permisos ni conexión IDA. El bloqueo previo de glob hacia HOME por external_directory: deny fue correcto.

1. **Reutiliza la confirmación visual ya proporcionada por el operador para la sesión P1**, registrada como OBSERVADO_POR_OPERADOR; no exijas repetirla ni afirmes haber obtenido acceso nativo al selector. En una sesión nueva o si el agente activo cambia, solicita una nueva confirmación únicamente si realmente es necesaria. La identidad de presentación no prueba el modo activo.
2. Comprueba el uso nativo de skill en la sesión actual; no infieras carga por mera existencia de SKILL.md. Puedes usar skill para vx-engineering-harness o vx-ida-mcp-reverse-engineering si el objetivo lo requiere.
3. Para nuevas delegaciones de lectura, comprueba que task esté disponible y permitido y que el operador haya confirmado el selector en la sesión pertinente. En el encargo a vx-inspector **traslada explícitamente**: `origen_prerequisito=confirmación visual del operador`, `agente_activo_declarado=vx-integrador`, `alcance=README.md en proyecto autorizado`, `solo_lectura=true`, `bash=false`, `home=false`. El inspector no debe intentar verificar por su cuenta el selector externo; solo comprobar alcance y permisos propios. No conviertas este traspaso en autorización para escribir, cambiar ACL ni usar herramientas no permitidas. Si task se deniega, registra BLOCKED con su causa; no simules éxito. La P1 ya alcanzó completed en el segundo intento, no hace falta repetirla sin motivo.
4. **Próxima fase P2, separada de esta P1:** comprobar `edit: ask` del builder seleccionado mediante un **proyecto de pruebas sintético y aislado**, nunca el Harness ni producción. El operador debe abrir el proyecto, solicitar explícitamente una edición inocua y observar si Kilo pide aprobación **antes** de escribir; denegar primero una solicitud para confirmar ausencia de cambios y, solo en otra prueba consentida, aprobar una operación mínima. No forzar denegaciones ni asumir que un frontmatter prueba permisos efectivos. `bash: ask` queda para una prueba independiente autorizada; sin shell automático.
5. No uses glob ni read para buscar agentes globales fuera del proyecto. external_directory: deny es correcto; no ajustes permisos ni AutoApprove para eludirlo.
6. La carga de la skill de IDA no prueba ida-mcp. No ejecutes herramientas IDA, scripts, patch, debugger, conexiones ni procesos sin aprobación explícita.
7. Entrega un informe de cada gate: VERIFICADO, NO_VERIFICADO o BLOQUEADO; fuente, herramienta nativa realmente invocada y referencia mínima. Distingue archivos verificados, evidencia reportada, pruebas reales y estado no observado.

El validador local en el repositorio scripts/vx_runtime_smoke_v1.py imprime un JSON vacío con --template y verifica un JSON aportado por el operador con --check archivo.json. No obtiene pruebas del host, no escribe HOME y nunca concede certificación independiente por una declaración.
