# /vx-dev-tools-snapshot

Objetivo: capturar únicamente las tools que el host Kilo muestra como disponibles para el agente actual.

Reglas:
- no invoques ninguna tool;
- no pruebes permisos;
- no amplíes ACL;
- no consultes MCP;
- no incluyas secretos ni argumentos;
- devuelve solo nombres/IDs visibles;
- si el host no permite introspección fiable, responde `NO_VERIFICADO`.

Salida:

```text
AGENT
CAPTURE_STATUS: VISIBLE_LIST | NO_VERIFICADO
VISIBLE_TOOLS
- <tool-id>
EVIDENCE
- host/session only; no invocation
```

Este comando produce evidencia de **visibilidad**, no de funcionamiento.
