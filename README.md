# VECIDYA · Kilo Code Global Harness V2.0

**Fuente:** auditoría `Kilo-Code-Auditoria-20261113-114114.zip`. El paquete contiene
solo nuevas instrucciones, flujos, una skill y scripts. **NO incluye ninguna
configuración privada ni credenciales de tu ZIP.**

## Regla contractual: SOLO GLOBAL

Todos los archivos que instala el script van a `%USERPROFILE%\.config\kilo\`
o `%USERPROFILE%\.kilo\skills\` y a la configuración de usuario de VS Code.
NO escribe `.kilo`, `.agents`, `.kilocode`, `AGENTS.md` o `CLAUDE.md` dentro
 de los repositorios. Leer documentación del proyecto no equivale a instalar
habilidades en él.

## Auditoría de referencia

- `kilo.jsonc` es válido y tiene **21 entradas de agente** (incluye built-ins personalizados).
- Hay **11 archivos Markdown de agente** con nombres presentes también en el JSON.
- **19 agentes** tienen `steps=10000000` en la copia.
- **22 skills** en `~/.kilo/skills`, **9** en `~/.agents/skills`,
  **7** en `~/.kilocode/skills` (la carga efectiva de las heredadas debe validarse).
- MCP en el ZIP: **cloudflare, memory, codebase-memory-mcp, microsoft-learn**.
- VS Code tiene estilo autónomo y autoaprobación de Kilo activada.
- `task-observer` tiene un disparador amplio y una skill de más de 50 KB;
  puede elevar el consumo de contexto si se invoca en cada sesión.
- Extensión detectada: `kilocode.kilo-code@7.8.27`; CLI `kilo` no visible en PATH.
- Node 26.12.1, npm 12.2.2, pnpm 12.18.0 y Git 2.56.0 detectados.
- Las copias de la auditoría incluyen **tres valores `[REDACTADO]` en permisos**;
  nunca restaura el JSON de auditoría ni lo uses como backup operativo.

## Cómo utilizarlo

1. Descomprime el ZIP en `Downloads\Kilo-Global-Harness-V2`.
2. Desde PowerShell 7, dentro de la carpeta extraída:

```powershell
pwsh -NoProfile -File .\scripts\Instalar-Kilo-Global-Harness-V2.ps1
```

Este comando es **DIAGNÓSTICO, SIN CAMBIOS**. Verifica también si tu
`kilo.jsonc` sigue siendo JSON estricto. Si contiene comentarios o comas
finales, el instalador se niega a reescribirlo para no destruirlos.

3. Si el informe es coherente, aplica solamente al entorno global:

```powershell
pwsh -NoProfile -File .\scripts\Instalar-Kilo-Global-Harness-V2.ps1 -Modo Aplicar
```

Opcional: agrega `-PausarTaskObserver` para trasladar esa skill fuera del
catálogo activo y guardarla junto al backup. NO borra la skill.

4. Abre VS Code, revisa Settings -> Auto Approve, inicia una sesión y escribe
`/reload`. Prueba `/vx-auditar` y `/vx-plan` en un repositorio sin permitir
escrituras. Verifica manualmente las acciones de los agentes antiguos.

### Qué modifica `-Modo Aplicar`

- Crea regla global `rules/vx-global-harness-v2.md` y la registra en `instructions`.
- Instala nueve workflows globales bajo `~/.config/kilo/commands`.
- Instala una skill global `vx-engineering-harness` en `~/.kilo/skills`.
- Conserva todos los servidores MCP, modelos, credenciales y nombres de agentes.
- Reduce `steps > 160` a 120 (primarios) o 60 (subagentes) en la definición
  JSON **sin tocar las definiciones Markdown existentes**.
- Cambia `edit`/`bash`/`mcp` con valor `allow` a `ask` en las entradas JSON de agentes.
- Configura aprobación global `ask` con lectura/búsqueda permitidas.
- Desactiva `kilo-code.new.autoApprove.enabled` en settings de usuario de VS Code.
- Guarda backup privado de archivos existentes en `Downloads` antes de alterar.

**Limitación importante:** los 11 archivos Markdown de agente pueden contener
permisos propios. No se eliminan ni se sobrescriben automáticamente. Es una
fase pendiente para consolidar a una sola fuente de verdad tras las pruebas.

### Restablecer

Usa la ruta exacta indicada por el script cuando lo aplicaste:

```powershell
pwsh -NoProfile -File .\scripts\Instalar-Kilo-Global-Harness-V2.ps1 `
  -Modo Restaurar -BackupFolder 'C:\Users\Admin\Downloads\Kilo-Harness-Backup-AAAAMMDD-HHMMSS'
```

**No subas backups:** contienen copias originales, quizá con credenciales.
Restaurar reemplaza los archivos por su versión guardada; revisa cambios
posteriores antes de hacerlo.

## Política de actualización

**Congelación por defecto:** no se habilitan actualizadores automáticos ni
se ejecuta `npx skills update`, `gh skill update`, `npm update` o cambios
masivos. Se revisan versiones, hashes y changelogs antes de aceptar cada cambio.
Este paquete NO toca el mecanismo de actualización de VS Code ni la actualización
server-side del modelo Auto. Las skills instaladas no se autoactualizan por
su mera presencia en carpetas. Evitar `npx ...@latest` en MCP críticos después
 de verificar una versión estable.

## Próximas fases (NO automáticas)

1. Comprobar en Kilo la precedencia de agentes JSON y Markdown, migrar
   duplicados al único origen global elegido con backup y pruebas.
2. Consolidar las 22+9+7 skills globales sin romper rastreo de sus instaladores.
3. Diagnosticar MCP por conexión efectiva (captura runtime), no solo por JSON;
   limitar MCP activos para bajar carga de contexto.
4. Probar modelos/presupuestos en Settings -> Models. No hay proveedores ni
   modelo fijado en `kilo.jsonc` del ZIP; puede haber configuración privada de UI.
5. Validar con una tarea end-to-end en un repo de prueba sin crear dotfiles
   locales de agente.
