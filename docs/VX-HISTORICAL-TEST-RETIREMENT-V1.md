# Retiro histórico post-PASS

El retiro de tests antiguos queda separado de la certificación.

```text
reemplazo vigente
→ PASS real
→ evidence JSON
→ plan_historical_test_retirement.py
→ READY_TO_REMOVE
→ revisión humana/PR
→ borrar test + gate antiguo
```

El planner nunca borra archivos ni modifica CI. Solo evita retirar un test antes de que todos sus reemplazos tengan evidencia de PASS.
