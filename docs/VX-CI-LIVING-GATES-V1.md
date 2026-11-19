# Inventario de Gates CI Vivos V1

Cada paso de `.github/workflows/validar-harness.yml` debe estar clasificado:

- **CURRENT**: protege una invariante actual.
- **REVIEW**: puede seguir siendo útil, pero debe mapearse a una invariante actual o consolidarse.
- **HISTORICAL_CANDIDATE**: parece supersedido; solo se elimina después de que su reemplazo pase.

La clasificación no depende únicamente del número de versión.

El objetivo es reducir progresivamente el workflow sin perder cobertura real.
