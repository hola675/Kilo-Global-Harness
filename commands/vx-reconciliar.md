---
description: Comparar agentes Kilo globales declarados en JSONC y Markdown sin editar configuracion ni mostrar secretos
agent: plan
---

Audita las definiciones globales de agentes para la tarea $ARGUMENTS. Usa el script global PowerShell instalado en `~/.config/kilo/harness/scripts/Reconciliar-Agentes-V4.2.ps1` con `pwsh -NoProfile -File "$HOME/.config/kilo/harness/scripts/Reconciliar-Agentes-V4.2.ps1" -Json`, si está disponible, o el script fuente del harness solo si esa ruta no existe. El script no modifica archivos ni invoca modelos.

Separa los recuentos de nombres compartidos de los conflictos de campos efectivos. Lee únicamente metadatos seguros de `kilo.jsonc` y frontmatter de `agents/*.md`. No muestres prompts, descripciones, modelos, valores de entorno, tokens ni rutas privadas; evita enviar el JSON completo a repositorios públicos.

Para los campos `mode`, `steps` y permisos, informa IGUAL_EXPLICITO, DIFERENCIA_EXPLICITA o REGLAS_COMPUESTAS_REVISAR_PRECEDENCIA, sin asumir que dos fuentes equivalen a dos ejecuciones del agente. Las declaraciones de permisos en YAML complejas requieren revisión manual y prueba de runtime.

El resultado es un PLAN de reconciliación, nunca una orden para borrar agentes, cambiar permisos ni reducir `steps` automáticamente. Preserva AutoApprove, MCP, modelos, backups y configuración existente. Propón migración gradual con rollback y pruebas por agente.
