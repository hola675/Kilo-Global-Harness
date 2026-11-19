---
name: vx-dev-supply-chain-review
description: "Audita dependencias, acciones CI, paquetes y herramientas de terceros por origen, versión, scripts, permisos, licencia y superficie de supply chain. Usar al añadir/actualizar paquetes, acciones GitHub, binarios o tooling externo."
compatibility: "Read-only; no instala ni ejecuta dependencias."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "supply-chain"
---

# VX Dev — Supply Chain Review

## Protocolo
1. Identificar origen canónico, maintainer y licencia.
2. Verificar pin/version y si existe lockfile/hash/provenance.
3. Revisar install/postinstall hooks y permisos requeridos.
4. Distinguir dependencia directa/transitiva.
5. Revisar advisories/CVE solo con fuente verificable y versión afectada.
6. Para CI actions, preferir versiones/pins controlados y permisos mínimos del workflow.
7. Para herramientas descargables, exigir checksum/firma cuando exista.
8. Evaluar rollback y blast radius.
9. No confundir popularidad con seguridad.

## Salida
`{component,source,version,pin,permissions,hooks,license,known_risks,evidence,recommendation}`.

Inspiración: SLSA, GitHub Actions security, OWASP supply-chain guidance.
