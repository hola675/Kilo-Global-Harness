---
description: Registrar una observación útil en el historial global Kilo, sin aprendizaje ni hooks automáticos
agent: plan
---

Observación relevante sobre una tarea de Kilo: $ARGUMENTS.

**V4.3 = captura explícita y ligera, sin hooks automáticos**. No registres un evento por cada llamada. Solo considerar corrección explícita, fallo confirmado, regresión demostrada, brecha de capacidad o resultado útil de una evaluación.

Comprueba evidencia con archivos actuales antes de clasificar. Redacta un resumen neutro de máximo 500 caracteres, **sin código, secretos, rutas absolutas, correos o información de clientes**, y selecciona uno de `success/failure/correction/regression/gap/feedback`. Usar `python -I "$HOME/.config/kilo/harness/scripts/vx_evolution_core.py" observe --type correction --summary "Hecho verificado y generalizable" --json` solo si la tarea autoriza el registro.

El evento no modifica agentes ni skills. Si es redundante, ofrece consolidarlo en lugar de repetir observaciones de poco valor. El fingerprint identifica repeticiones textuales, no prueba equivalencia semántica. Nunca copiar el historial privado a GitHub.
