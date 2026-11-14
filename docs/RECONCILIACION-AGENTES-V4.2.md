# V4.2 — Reconciliación de agentes globales (auditoría y plan seguro)

**Estado:** herramienta de solo lectura implementada; la migración de agentes heredados **no** está automatizada ni aprobada. No copiar datos privados de `kilo.jsonc` a GitHub.

## Línea base recibida del equipo

| Elemento | Resultado comunicado |
| --- | --- |
| Agentes inline en JSONC | 21 |
| Archivos Markdown de agentes globales | 18 |
| Nombres que comparten ambas fuentes | 11 |
| Valores de `steps` superiores a 400 | 19 |
| Skills detectadas | 22 en `.kilo`, 10 en `.agents`, 7 heredadas `.kilocode` |
| MCP declarados | `memory`, `codebase-memory-mcp`, `microsoft-learn`, `imagegen` |
| AutoApprove en settings de VS Code | `true`, no se comprobó la política efectiva en runtime |
| Plugin `opencode-models-discovery` | Declarado en dos superficies; duplicación funcional NO verificada |

Los números anteriores proceden del diagnóstico compartido y son **evidencia inicial**, no garantías de que la configuración siga idéntica. Un inventario anterior citaba 12 coincidencias y un número diferente de skills; prevalece la medición más reciente para planificar, sin deducir la causa del cambio.

## Uso (PowerShell 7)

Desde el repositorio fuente:
```powershell
pwsh -NoProfile -File '.\scripts\Reconciliar-Agentes-V4.2.ps1'
pwsh -NoProfile -File '.\scripts\Reconciliar-Agentes-V4.2.ps1' -Json
```

Desde el perfil global, después de ejecutar el instalador actualizado:
```powershell
pwsh -NoProfile -File "$HOME\.config\kilo\harness\scripts\Reconciliar-Agentes-V4.2.ps1"
```

Desde Kilo, usar `/vx-reconciliar`. Su función es describir diferencias y preparar un plan; **no** aplicar modificaciones al JSON ni eliminar agentes.

## Metodología y significado de estados

El auditor abre `~/.config/kilo/kilo.jsonc` con un parser JSONC compatible con comentarios y comas finales. Lee solo el frontmatter de `~/.config/kilo/agents/*.md` y **no** expone texto de prompts, descripciones, identificadores de modelos, valores de entorno ni patrones privados de permisos.

- `IGUAL_EXPLICITO`: ambos archivos declaran el mismo valor escalar seguro para `mode`, `steps` o permiso simple.
- `DIFERENCIA_EXPLICITA`: ambos declaran valores comparables distintos; no significa automáticamente que el runtime esté mal.
- `SOLAPAMIENTO_REQUIERE_REVISION`: ambas fuentes declaran un campo complejo o un valor textual; la comparación evita exponer su contenido.
- `REGLAS_COMPUESTAS_REVISAR_PRECEDENCIA`: hay permisos compuestos o no interpretables con seguridad mediante lectura superficial.
- `campos_solo_json` y `campos_solo_markdown`: presencia en una sola fuente; podría ser herencia legítima, no conflicto.

**Límite crítico:** la herramienta usa un parser deliberadamente parcial de YAML (escalares simples y nombres de permisos de primer nivel); no calcula la configuración efectiva ni puede demostrar que el agente se carga con una política determinada. Solo el runtime y una revisión específica de las reglas pueden confirmarlo.

## Proceso de migración (propuesto, NO aplicado)

1. Congelar la línea base con el auditor de solo lectura y revisar su salida **privadamente**.
2. Clasificar cada agente: ambos orígenes intencionales, herencia útil, valor contradictorio, prompt solapado o permiso que necesita revisión.
3. Preparar un diff de propiedades con el usuario; no copiar `kilo.jsonc` ni backups a un repositorio público, ni publicar datos de modelos o secretos.
4. Elegir **un solo agente piloto de bajo riesgo**. Tomar backup recuperable dentro de HOME antes de modificarlo y conservar las capas de precedencia necesarias.
5. Comprobar en Kilo que mantiene `mode`, herramientas, reglas de aprobación, modelo y `steps` esperados. Probar una tarea representativa, junto a un caso negativo de permisos.
6. Medir calidad, iteraciones y uso real solo si se dispone de métricas; revertir si hay regresiones.
7. Repetir gradualmente con los restantes, sin cambiar de golpe los 19 límites elevados. No eliminar un archivo Markdown solo por compartir nombre con JSON.

## Requisitos para una futura V4.3

- Un comparador de propiedades efectivo **con pruebas de runtime**, no basado únicamente en nombres.
- Un migrador explícito con diff, backup, `-Simular`, plan aprobado y rollback; nunca reescribir JSONC con un parser que elimine comentarios.
- Ensayar límites de `steps` según rol y tipo de tarea; `steps` no representa tokens.
- Revisar la selección de skills por capacidad, no solo por coincidencia de nombre.
- Mantener la política estricta de un escritor, `main` permanente y permisos existentes sin reducir seguridad.

## Seguridad

No ejecutar scripts de terceros, no instalar skills/MCP de forma automática, no inferir autenticación por existencia de JSON y no compartir la salida detallada sin revisarla. Un `PASS` del auditor significa que se ha leído un inventario coherente, **no** que se haya reconciliado un agente en el runtime.
