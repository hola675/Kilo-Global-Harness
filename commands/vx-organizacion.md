---
description: Revisar solapamientos y procedencia declarada de agentes/skills Kilo sin cambiar configuraciones ni atribuir competencias
agent: plan
---

VX Evolución V4.6.3 — Auditoría organizativa global SOLO LECTURA.

Al recibir `/vx-organizacion` o una solicitud expresa del operador:
1. Confirma que se trabaja únicamente sobre el HOME global del equipo Windows y no sobre el repositorio o proyecto abierto.
2. **No intentes cambiar la política de herramientas si terminal/PowerShell está bloqueado.** Informa el bloqueo y permite que el operador ejecute manualmente en su consola los comandos mostrados.
3. Si la política de Kilo permite la ejecución de herramientas de lectura, únicamente realizar las operaciones explícitamente autorizadas:

```powershell
$org = Join-Path $HOME '.config/kilo/harness/scripts/vx_organizational_audit.py'
python -I $org
# Opcional para revisión privada local; no publicar informe integral sin revisión:
python -I $org --json
```

Interpretar con rigor:
- `AGENT_SOURCE_OVERLAP`: mismo nombre en JSONC/Markdown, **no** colisión efectiva ni precedencia comprobada.
- `AGENT_STEPS_REVIEW`: steps declarados por encima del umbral, **no** fallo de seguridad ni mala calidad.
- `SKILL_SOURCE_OVERLAP`, `PROFILE_SKILL_UNOBSERVED`, `ROUTER_AGENT_UNOBSERVED`: observar metadatos, sin afirmar ausencia/ejecución runtime.
- Ninguna referencia `ses_*` del historial es por sí sola prueba de identidad o delegación: `delegation_provenance_verified=false`.
- Los cinco casos V4.6.2 fueron **respuestas coincidentes en fixtures públicos**, no evidencia ciega de competencia.
- Devolver hallazgos, fuentes declaradas, límites, evidencia faltante y plan **manual** de verificación. Sin promociones, contrataciones, fusiones, jubilaciones ni permisos.
- No leer ni publicar prompts privados, rutas, modelos o logs de proyectos; nunca pasar el contenido del HOME a GitHub.

**Prohibido** editar `kilo.jsonc`, agentes, skills, MCP, settings, AutoApprove, SQLite, scheduler o tareas de Windows. Sin modelos auxiliares ni autorizaciones implícitas. No crear archivos de resultados o propuestas por defecto.

Guía canónica: `docs/VX-AUDITORIA-ORGANIZATIVA-V4.6.3.md`.
