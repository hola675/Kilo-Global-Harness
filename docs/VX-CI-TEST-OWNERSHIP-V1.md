# Propiedad única de tests en CI

Regla:

```text
1 test_*.py directo
→ 1 gate propietario
```

Un gate posterior no vuelve a ejecutar una suite anterior solo para "regresión".
Si necesita esa invariante, depende del gate anterior o usa un manifest canónico.

Excepciones no se añaden de forma implícita: deben convertirse en un contrato nuevo con un oráculo distinto.
