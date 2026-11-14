---
description: Consultar el observador Kilo, proponer registro de correcciones y orientar activación opcional sin autoaprendizaje
agent: plan
---

Observación relevante sobre una tarea de Kilo: $ARGUMENTS.

**V4.4:** el observador de sesiones solo almacena recuentos horarios de `session.idle`, `session.error` y `session.compacted` cuando se ha instalado opcionalmente el plugin global y se ha habilitado explícitamente `observer-mode light`. No guarda mensajes, IDs de sesiones, rutas ni contenidos; no llama a modelos. Usa `observer-status` y `observer-report --days 7` para diagnóstico. Si se solicita apagarlo, usar `observer-mode --mode off`; no activar si el usuario solo quiere información. Si el esquema aún es v1, `observer-migrate` requiere backup automático y autorización explícita; no migrar al consultar. Nunca instalar hooks en repositorios.

**Observaciones de calidad:** siguen siendo explícitas y requieren evidencia, no se derivan automáticamente de `session.error` o `session.idle`.  No registres un evento por cada llamada. Solo considerar corrección explícita, fallo confirmado, regresión demostrada, brecha de capacidad o resultado útil de una evaluación.

Comprueba evidencia con archivos actuales antes de clasificar. Redacta un resumen neutro de máximo 500 caracteres, **sin código, secretos, rutas absolutas, correos o información de clientes**, y selecciona uno de `success/failure/correction/regression/gap/feedback`. Usar `python -I "$HOME/.config/kilo/harness/scripts/vx_evolution_core.py" observe --type correction --summary "Hecho verificado y generalizable" --json` solo si la tarea autoriza el registro.

El evento no modifica agentes ni skills. Si es redundante, ofrece consolidarlo en lugar de repetir observaciones de poco valor. El fingerprint identifica repeticiones textuales, no prueba equivalencia semántica. Nunca copiar el historial privado a GitHub.

La reunión semanal de VX permanece desactivada hasta V4.5. Evita duplicar Task Observer y otros hooks existentes sin auditoría de compatibilidad. No activar el plugin o la captura sin una petición concreta de instalación/activación.
