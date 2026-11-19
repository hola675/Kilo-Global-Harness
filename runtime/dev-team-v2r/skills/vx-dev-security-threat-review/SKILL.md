---
name: vx-dev-security-threat-review
description: "Realiza revisión defensiva de seguridad basada en activos, trust boundaries, inputs no confiables, autorización, exposición de datos y abuse cases. Usar en auth, multi-tenant, secretos, integraciones externas o cambios sensibles."
compatibility: "Read-only; no ejecuta exploits, scanners ni pruebas sobre producción."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "security"
---

# VX Dev — Security Threat Review

## Método
1. Definir activos y principals.
2. Dibujar trust boundaries reales.
3. Enumerar entradas no confiables y decisiones de autorización.
4. Revisar controles server-side, tenant/object ownership y least privilege.
5. Identificar exposición de secretos/PII/logs.
6. Formular abuse cases con precondición → path → impacto.
7. Clasificar cada hallazgo: OBSERVED/CORROBORATED/HYPOTHESIS/DISMISSED/UNKNOWN.
8. Severidad solo cuando el impacto y la precondición están sustentados.
9. Proponer test negativo seguro y mínima mitigación efectiva.

## Salida
`ASSETS`, `TRUST_BOUNDARIES`, `ATTACK_SURFACE`, `ACCESS_CONTROL`, `DATA_EXPOSURE`, `ABUSE_CASES`, `THREAT_FINDINGS`.

No afirmar explotación demostrada si solo existe un riesgo plausible.
