# Dev Team Capability Matrix V1

Fuente canónica de capacidades del Dev Team.

## Qué resuelve

Evita repetir en distintos registros:

- skill allowlist por agente;
- herramientas nativas objetivo;
- familias MCP primarias/condicionales;
- allowlist MCP exacta actualmente certificada.

## Regla fundamental

```text
current_mcp_exact
  = autoridad source certificada actual

mcp_primary / mcp_conditional
  = routing objetivo
  != permiso
```

La visibilidad real del host sigue requiriendo snapshot runtime.

## Consumidores

- MCP role playbook;
- Kilo tools/complements audit;
- runtime tool snapshot;
- tool plan generator;
- futuros tests de ACL y activación.

No debe copiarse la matriz completa en nuevos archivos; los consumidores deben referenciarla.
