---
name: vx-dev-mcp-security
description: "Revisa seguridad de una integración MCP desde source/configuración: least privilege, tool poisoning, scopes, trust boundaries, outputs no confiables y aprobación humana. Usar al evaluar un servidor MCP nuevo, un cambio de scopes o una allowlist de tools."
compatibility: "Análisis defensivo read-only; no conecta, instala ni explota servidores MCP."
metadata:
  version: "1.0.0"
  last_modified: "2026-11-21"
  origin: "vx-dev-original"
  category: "mcp-security"
---

# VX Dev — MCP Security Review

## Checklist
1. Identificar servidor, transporte, origen, versión y propietario.
2. Enumerar tools y efectos reales: read/write/delete/execute/send.
3. Verificar scopes mínimos y credenciales separadas por servidor.
4. Revisar tool descriptions, parámetros y schemas como superficie de ataque.
5. Detectar tool poisoning, shadowing, confused deputy y output prompt injection.
6. Exigir aprobación humana para acciones sensibles/irreversibles.
7. Verificar que tokens no se registren ni se reutilicen para audiencias incorrectas.
8. Limitar filesystem/network/host access cuando aplique.
9. Tratar annotations de “read-only” como hints, no enforcement.
10. Proponer prueba segura y evidencia requerida antes de activar.

## Salida
`{server,trust_boundaries,tools,scopes,side_effects,threats,controls,evidence,activation_gate}`.

No instalar, autenticar, elevar permisos ni ejecutar pruebas ofensivas por cargar esta skill.
