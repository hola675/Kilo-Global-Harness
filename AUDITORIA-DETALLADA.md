# Auditoría técnica VECIDYA · Kilo Code Global Harness V2

**Base:** archivo aportado `Kilo-Code-Auditoria-20261113-114114.zip`.
**Alcance:** solamente copia incluida; no se accedió a Windows en remoto.
**Seguridad:** NO se han reproducido secretos ni configuraciones originales.

## Inventario acreditado

| Componente | Observado | Interpretación |
| --- | ---: | --- |
| Entradas ZIP | 501 | Incluye subdirectorios, recursos y documentación |
| Skills en `.kilo/skills` | 22 | Globales |
| Skills en `.agents/skills` | 9 | Globales compatibles |
| Skills en `.kilocode/skills` | 7 | Heredadas; carga efectiva por confirmar |
| Total carpetas `SKILL.md` | 38 | 38 nombres únicos, sin duplicados exactos |
| Skills con `name` y `description` frontmatter | 38 | Forma básica válida; no prueba la ejecución ni seguridad |
| Agentes en `kilo.jsonc` | 21 | Incluye agentes built-in personalizados |
| Agentes en Markdown | 11 | Mismos nombres también presentes en config |
| Definiciones `steps > 160` | 19 | Usan 10.000.000 iteraciones (no tokens) |
| MCP en JSON | 4 | Cloudflare, memory, codebase-memory-mcp, microsoft-learn |
| Extensión VS Code | 7.8.27 | `kilocode.kilo-code` |
| Node / npm / pnpm | 26.12.1 / 12.2.2 / 12.18.0 | Reportado por el equipo |
| Docker / WSL | Detectados | Disponible en PATH no significa motor operativo |
| Ollama / kilo CLI | No detectados | La extensión puede seguir operativa sin CLI en PATH |
| VS Code auto-approve | `true` | Riesgo global alto |

La configuración actual **no declara `model`, `small_model` ni `subagent_model`**;
no significa que Kilo carezca de modelos, ya que puede guardar su selección en
el runtime de la extensión. En una captura anterior se apreciaban nueve MCP;
el ZIP trae cuatro. Debe prevalecer la enumeración del runtime de la sesión actual.

## Hallazgos priorizados

### P0 — Riesgo operativo

1. `kilo-code.new.autoApprove.enabled = true` y `agentWorkStyle = autonomous`.
   La combinación requiere permisos por herramienta cuidadosamente configurados.
2. `code-simplifier` tiene `edit: allow` y `bash: allow` en la definición JSON.
   Otros agentes disponen de `bash: allow` sin filtros.
3. Diecinueve definiciones utilizan `steps: 10000000`. Un valor alto reduce el
   corte de sesiones, puede elevar consumo y dificultar detectar loops.
4. El ZIP fue producido con un sanitizador que reemplazó tres valores legítimos
   de permisos por `[REDACTADO]`. No debe usarse como copia restaurable.

### P1 — Configuración coherente

5. Once definiciones conviven en `~/.config/kilo/agents/*.md` y el objeto
   global `agent` de `kilo.jsonc`. Hay diferencias de `steps`, `name` y permisos
   sanitizados; primero se debe verificar precedencia exacta por nombre.
6. `task-observer` (`SKILL.md` >50 KB) declara activación previa a herramientas
   y en cualquier tarea de múltiples pasos. Puede crear ruido y gasto de tokens;
   revisar y pausar opcionalmente, sin borrar contenido.
7. La regla Codebase Memory global ordena preferir el grafo siempre. Debe
   condicionarse a conexión, índice, frescura y cobertura para no crear fallos
   o confianza excesiva cuando el repositorio no esté indexado.
8. Siete skills se ubican en `.kilocode/skills` heredada. Hay que verificar
   qué carga la extensión moderna antes de migrar, y preservar metadatos de
   los instaladores para poder actualizar o revertir.

### P2 — Rendimiento, contexto y mantenimiento

9. No aparecen presupuestos explícitos de modelos/subagentes en el ZIP. Se
   necesita ver Settings -> Models y sus proveedores disponibles, sin APIs.
10. Los MCP necesitan un inventario de herramientas efectivamente conectadas;
    una entrada en JSON no demuestra salud de conexión ni calidad del servicio.
11. Evitar múltiples skills que repitan auditoría, diseño o depuración; activar
    por tarea solo una o dos, con `description` y `name` bien delimitados.
12. Evitar actualización automática de skills por defecto y pin de versiones
    de MCP con `npx -y` en entornos de producción de desarrollo, tras verificar
    versiones. No deshabilitar a ciegas todas las actualizaciones de VS Code.

## Arquitectura objetivo (global-only)

- **Reglas:** `~/.config/kilo/AGENTS.md` + reglas globales referenciadas en `instructions`.
- **Workflows:** `~/.config/kilo/commands/vx-*.md`.
- **Agentes:** una única fuente global canónica, tras reconciliar Markdown/JSON.
- **Skills:** `~/.kilo/skills/` como ubicación preferente, manteniendo por ahora
  las globales `~/.agents/skills/` compatibles para no romper ownership.
- **MCP:** solo servidores activos útiles para la tarea; lectura por defecto,
  escritura y despliegues mediante aprobaciones.
- **Memoria:** grafo de código con cobertura comprobada + memoria de decisiones
  explícitas, separando datos del repositorio y conocimiento persistente.
- **Modelos:** modelo principal por calidad, modelo pequeño para clasificación,
  subagente barato para exploración; seleccionar exclusivamente IDs reales
  disponibles en tu cuenta.
- **Costo:** steps acotados, resúmenes incrementales, `/compact`, herramientas
  específicas y no volcar el código completo al contexto.
- **Actualización:** inventario de versiones, cambios manuales revisados,
  backup y rollback.

## Flujo de trabajo global propuesto

`/vx-plan` -> `/vx-implementar` -> `/vx-validar` -> `/vx-revisar-diff` ->
`/vx-cierre`, con `/vx-diagnosticar`, `/vx-auditar` y `/vx-mcp` cuando haga falta.
Cada comando vive globalmente, pero puede trabajar sobre la carpeta activa.

## Límites de este paquete

- El instalador incluye un P0 de permisos y un harness global mínimo, pero no
  intenta resolver por sí solo duplicados entre agent Markdown y JSON.
- No instala más servidores MCP, no toca credenciales, no configura proveedores
  no verificados y no escribe archivos en repositorios.
- Los resultados de pruebas de runtime en Windows siguen pendientes.
