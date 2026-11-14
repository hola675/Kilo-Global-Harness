---
description: Auditar capacidades declaradas de agentes y skills de Kilo en HOME global, sin modificar archivos ni SQLite
agent: plan
---

VX Capacidades V4.6.0: $ARGUMENTS.

Este comando **solo audita la instalación global de Kilo Code en este PC Windows**. No inspecciona el proyecto abierto. Ejecuta únicamente cuando el usuario solicite la auditoría y sin copiar configuraciones privadas a la conversación ni a GitHub:

```powershell
$vxAudit = Join-Path $HOME '.config/kilo/harness/scripts/vx_capability_audit.py'
python -I $vxAudit
# Para informe estructurado que el usuario revisará LOCALMENTE:
python -I $vxAudit --json
```

**Reglas de análisis:** inventariar definiciones de agentes JSONC/Markdown y skills de las tres rutas globales compatibles, comparar presencia y campos simples `mode/steps/permission` sin mostrar los prompts ni las claves, y cruzar las `capabilities` declaradas en el registro global `vx-agent-registry-v4.json`.

Distinguir con rigor `DECLARADA_NO_PROBADA`, `NO_MEDIDO`, `NO_VERIFICADO` y `SIN_DATOS`. El mismo nombre en JSONC/Markdown no demuestra qué fuente tiene prioridad; una skill no vista en estas rutas puede estar incorporada por otra vía Kilo: no afirmar que no existe en tiempo de ejecución. No declarar seniority ni promover agentes con base en el inventario.

**No** ejecutar `inventory-sync`, `observe`, `propose` o `meeting-prepare` automáticamente: esos comandos escriben SQLite. No crear procesos residentes, task scheduler, plugins, roles, archivos dentro del proyecto ni nuevos agentes. Si hay brechas verificables, redactar propuestas separadas y consultar al usuario antes de registrarlas. Para evaluar el resultado, trabajar con pruebas reproducibles de V4.6.1+.

Referencia: `docs/VX-CAPACIDADES-V4.6.0.md`.

**V4.6.1:** después de este inventario, usar `/vx-matriz` para vincular capacidades y skills con identificadores de pruebas futuras; no confundir un resultado PASS declarado con evidencia de ejecución real.
