# VX MCP Pack V1 — instalación y registro reproducible en Windows

**Fecha de corte:** 2026-11-17  
**Objetivo:** reproducir la base global de MCP validada para Kilo Desktop en Windows sin copiar secretos ni mezclarla con Agents/Skills/Rules.  
**Registro canónico:** `registry/vx-mcp-catalog-v2.json`  
**Snapshot observado:** `inventory/mcp-runtime-2026-11-17.json`

## Estado certificado

En la estación de referencia se validaron **13/13 servidores MCP conectados** mediante `kilo mcp list`.

| # | MCP | Tipo | Estado observado | Función |
|---|---|---|---|---|
| 1 | Codebase Memory | local/stdin | conectado | grafo persistente, arquitectura e impacto |
| 2 | IDA | local/stdin | conectado | ingeniería inversa con IDA 9.4+ |
| 3 | Playwright | local/stdin vía npx | conectado | automatización y QA web |
| 4 | Context7 | remoto | conectado | documentación actual por librería/version |
| 5 | ImageGen | local/stdin vía npx | conectado | generación de imágenes con sesión ChatGPT |
| 6 | GitHub | local/stdin | conectado y probado | repos, PR, issues y Actions |
| 7 | Cloudflare API | remoto/OAuth | conectado y probado | Workers, DNS, R2 y plataforma Cloudflare |
| 8 | Chrome DevTools | local/stdin vía npx | conectado y probado | consola, red, Lighthouse y performance |
| 9 | Snyk | local/stdin | conectado con límites de servicio | SAST/SCA/IaC/Secrets según organización |
| 10 | Postman | remoto/OAuth | conectado | workspaces y activos API |
| 11 | Microsoft Learn | remoto | conectado y probado | documentación oficial Microsoft |
| 12 | Sentry | remoto/OAuth | conectado | observabilidad; sin proyectos visibles al validar |
| 13 | Serena | local/stdin | conectado y probado | símbolos, referencias y navegación LSP |

“Conectado” significa handshake MCP correcto. “Probado” significa además que se ejecutó al menos una consulta funcional de lectura. No implica permisos ilimitados ni autoriza acciones destructivas.

**Extensiones opcionales no certificadas:** TinyFish se conserva separadamente en `registry/vx-mcp-optional-catalog-v1.json` como candidato no registrado ni autenticado. No se añade a los **13 MCP del pack**, ni se instala, conecta o autoriza desde este procedimiento. La skill `use-tinyfish` versionada no demuestra permisos ni disponibilidad real.

## Política de seguridad

El pack aplica estas reglas:

- **Nunca** versionar tokens, cookies, refresh tokens, claves API ni credenciales OAuth.
- OAuth se realiza de forma interactiva después de registrar los servidores.
- GitHub usa `gh auth token` solo en memoria del proceso mediante `scripts/mcp/github-mcp-kilo.ps1`.
- Antes de reescribir `~/.config/kilo/kilo.jsonc`, el instalador crea backup en `~/.config/kilo-mcp-pack-backups/`.
- MCP ajenos al pack no se eliminan: el instalador reemplaza/crea únicamente los 13 IDs gestionados.
- Operaciones WRITE/DELETE/DEPLOY/MERGE/CLOUD MUTATION deben seguir sujetas a aprobación del operador.
- `-InstalarIDAPlugin` es opt-in porque requiere una instalación local compatible de IDA.

## Requisitos base

Perfil de referencia:

- Windows 11 x64.
- PowerShell 7.
- Kilo Desktop.
- Node.js + npm/npx.
- GitHub CLI `gh`.
- `uv` y `uvx`.
- Google Chrome para Chrome DevTools MCP.
- IDA Pro 9.4+ solo si se utilizará IDA MCP con GUI.

Comprobar:

```powershell
pwsh --version
node --version
npm --version
npx --version
gh --version
uv --version
uvx --version
```

## Archivos del pack

```text
registry/vx-mcp-catalog-v2.json
inventory/mcp-runtime-2026-11-17.json
scripts/Instalar-MCP-Pack-Windows.ps1
scripts/mcp/github-mcp-kilo.ps1
docs/VX-MCP-PACK-WINDOWS-V1-20261117.md
```

El catálogo V1 se conserva como registro histórico de candidatos previos. V2 es el registro operativo del pack de 13 servidores.

## Instalación

Desde el repositorio:

```powershell
Set-Location 'D:\Proyectos\Kilo-Global-Harness'

pwsh -NoProfile -File .\scripts\Instalar-MCP-Pack-Windows.ps1 -Modo Diagnostico
```

El diagnóstico no modifica el perfil. Revisa dependencias, Chrome, Codebase Memory y los IDs MCP presentes.

Para aplicar:

```powershell
pwsh -NoProfile -File .\scripts\Instalar-MCP-Pack-Windows.ps1 -Modo Aplicar
```

El modo `Aplicar`:

1. instala Codebase Memory si falta;
2. instala/actualiza el binario nativo oficial de GitHub MCP cuando corresponde;
3. instala Snyk CLI si falta;
4. instala e inicializa Serena si falta;
5. registra los 13 MCP en `kilo.jsonc`;
6. preserva entradas MCP no gestionadas;
7. crea backup antes de escribir configuración;
8. **no** completa OAuth automáticamente.

Para actualizar componentes locales durante una reconstrucción:

```powershell
pwsh -NoProfile -File .\scripts\Instalar-MCP-Pack-Windows.ps1 -Modo Aplicar -ActualizarLocales
```

Para registrar solo configuración cuando los binarios ya existen:

```powershell
pwsh -NoProfile -File .\scripts\Instalar-MCP-Pack-Windows.ps1 -Modo Aplicar -SoloConfig
```

Para instalar también el plugin GUI oficial de IDA:

```powershell
pwsh -NoProfile -File .\scripts\Instalar-MCP-Pack-Windows.ps1 -Modo Aplicar -InstalarIDAPlugin
```

## Autenticaciones manuales posteriores

### GitHub

```powershell
gh auth login
gh auth status
```

El wrapper del pack recupera el token desde el keyring de `gh` en tiempo de ejecución y lo elimina del entorno al cerrar el servidor.

### ImageGen

```powershell
npx -y codex-imagegen-mcp@0.2 login
npx -y codex-imagegen-mcp@0.2 doctor
```

### Snyk

```powershell
snyk auth
```

No usar `snyk config get api` como prueba universal cuando la sesión usa OAuth moderno.

### MCP remotos OAuth

Con Kilo abierto:

```powershell
$KiloExe = Get-Process kilo -ErrorAction SilentlyContinue |
  Where-Object { $_.Path } |
  Select-Object -First 1 -ExpandProperty Path

& $KiloExe mcp auth cloudflare-api
& $KiloExe mcp auth postman
& $KiloExe mcp auth sentry
```

Context7 y Microsoft Learn no requieren OAuth en la configuración utilizada.

## Dependencias e instalación por servidor

### Codebase Memory

Fuente: https://github.com/DeusData/codebase-memory-mcp

El pack descarga una release Windows x64 mediante GitHub CLI, ejecuta el `install.ps1` incluido con `--skip-config` y usa la ruta administrada:

```text
%LOCALAPPDATA%\Programs\codebase-memory-mcp\codebase-memory-mcp.exe
```

Se evita que el instalador de terceros reescriba automáticamente la configuración Kilo.

### IDA MCP

Fuente oficial: https://github.com/HexRaysSA/ida-mcp

Runtime:

```text
uvx --exclude-newer=1s ida-mcp stdio --agent=kilo-desktop
```

Para GUI, IDA requiere 9.4+ y el plugin oficial. La instalación del plugin queda opt-in.

### Playwright MCP

Fuente: https://github.com/microsoft/playwright-mcp

```text
cmd /c npx -y @playwright/mcp@latest
```

No necesita instalación global; npx resuelve el paquete al arrancar.

### Context7

```text
https://mcp.context7.com/mcp
```

Se usa remoto para evitar el timeout de arranque observado con npx local en Windows.

### ImageGen

Fuente: https://github.com/ShalomObongo/codex-imagegen-mcp

```text
cmd /c npx -y codex-imagegen-mcp@0.2 serve
```

Autenticación ChatGPT separada del archivo Kilo.

### GitHub MCP

Fuente: https://github.com/github/github-mcp-server

El pack usa el binario Windows x64 oficial y verifica SHA256 cuando la release publica `digest`. No usa Docker y no guarda PAT en `kilo.jsonc`.

### Cloudflare API

```text
https://mcp.cloudflare.com/mcp
```

OAuth interactivo. Puede exponer operaciones de infraestructura; mantener mutaciones bajo aprobación.

### Chrome DevTools

Fuente: https://github.com/ChromeDevTools/chrome-devtools-mcp

```text
cmd /c npx -y chrome-devtools-mcp@latest
```

Requiere Chrome. Expone consola, red, performance y debugging.

### Snyk

```powershell
npm install -g snyk@latest
snyk auth
```

Kilo lo arranca con perfil estable `full` y directorio de salida para resultados grandes:

```text
snyk mcp -t stdio --profile full -o %LOCALAPPDATA%\SnykMCP\output
```

En la validación de referencia, Snyk Code sufrió timeout del servicio, Secrets no estaba habilitado para la organización y SCA/IaC dependían de la ruta analizada. Estos límites no invalidan el handshake MCP.

### Postman

Perfil global minimal:

```text
https://mcp.postman.com/minimal
```

El perfil reducido evita cargar innecesariamente todas las herramientas de Postman.

### Microsoft Learn

```text
https://learn.microsoft.com/api/mcp
```

Sin autenticación en el endpoint utilizado.

### Sentry

```text
https://mcp.sentry.dev/mcp
```

OAuth interactivo. En la validación se observó una organización accesible, pero ningún proyecto visible.

### Serena

Fuente: https://github.com/oraios/serena

```powershell
uv tool install -p 3.13 serena-agent
serena init
```

Kilo:

```text
serena start-mcp-server --context ide --project-from-cwd --open-web-dashboard false
```

El contexto `ide` reduce duplicación con las herramientas nativas de Kilo. Los language servers dependen del lenguaje del proyecto.

## Verificación

Abrir Kilo Desktop y ejecutar:

```powershell
pwsh -NoProfile -File .\scripts\Instalar-MCP-Pack-Windows.ps1 -Modo Verificar
```

El resultado esperado es:

```text
13 server(s)
```

y cada servidor debe aparecer como `connected`.

El script verifica además:

- el registro V2 contiene exactamente 13 IDs únicos;
- `kilo.jsonc` contiene los 13 IDs gestionados;
- si Kilo CLI está disponible, ejecuta `kilo mcp list`.

## Actualización

No existe actualización silenciosa del pack.

- Codebase Memory/GitHub MCP/Snyk/Serena: `-ActualizarLocales`.
- Playwright/Chrome DevTools: usan `@latest` al arrancar.
- IDA: `uvx` resuelve la versión estable según el comando registrado.
- ImageGen queda fijado a la línea `0.2` hasta revisión explícita.
- MCP remotos se actualizan en el servicio del proveedor.

Después de cualquier actualización, ejecutar `-Modo Verificar` y una prueba funcional de lectura.

## Rollback

Los backups de `kilo.jsonc` se guardan en:

```text
~/.config/kilo-mcp-pack-backups/
```

Para volver atrás:

1. cerrar Kilo;
2. seleccionar el backup correcto;
3. copiarlo sobre `~/.config/kilo/kilo.jsonc`;
4. abrir Kilo;
5. ejecutar `kilo mcp list`.

El rollback de configuración no elimina binarios locales ni credenciales almacenadas por los proveedores.

## Límites

- El pack está diseñado para **Windows + Kilo Desktop**.
- No instala Agents, Skills ni Rules.
- No intenta resolver automáticamente restricciones de proxy corporativo.
- No fuerza activación de Snyk Secrets ni de servicios externos.
- No crea proyectos Sentry/Postman/Cloudflare.
- No instala SonarQube, Grafana, Supabase, MongoDB, Figma o BrowserStack globalmente; se añaden por proyecto cuando exista una necesidad real.
