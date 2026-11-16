# VX Pack 0.2.2 — instalación global supervisada en Windows

**ATENCIÓN (actualizado 2026-11-16):** si tu Kilo tiene agentes inline o skills de compatibilidad, usa la [instalación por convivencia V0.2.3](VX-INSTALACION-CONVIVENCIA-0.2.3-WINDOWS.md); esta guía de instalación limpia bloqueará ese perfil deliberadamente. No borrar perfiles externos.

**Fecha:** 2026-11-16 · **Fuente:** `main` de `hola675/Kilo-Global-Harness` · **Equipo:** una PC Windows, Kilo Code global.

El operador autorizó instalar **solo componentes VX propios**; no autoriza activar nuevos MCP, modificar `kilo.jsonc`, credenciales, permisos AutoApprove, scheduler, multiwriter ni WebAuthn. V4.7.2 sigue con `approval_granted=false`, `apply_supported=false`.

**Inventario:** 12 agentes, 31 skills (incluida IDA MCP), 6 candidatos MCP **inactivos**. Bootstrap independiente con DPAPI CurrentUser, no instalar V4 incremental en paralelo.

## 1. Actualizar la fuente desde PowerShell 7

```powershell
$ErrorActionPreference = 'Stop'
$repo = 'D:\\Proyectos\\Kilo-Global-Harness'
Set-Location -LiteralPath $repo
git status --short
git switch main
git fetch origin
git pull --ff-only origin main
git status --short
git log -1 --format='%h %s'
```

Si `git status --short` muestra cambios locales o ramas de trabajo pendientes, detener y preservar; **no usar `reset --hard`**.

## 2. Diagnóstico y simulación (sin escribir HOME)

```powershell
pwsh -NoProfile -File .\\scripts\\Validar-Registro-V4.ps1
pwsh -NoProfile -File .\\scripts\\Instalar-Pack-VX-V022.ps1 -Modo Diagnostico
pwsh -NoProfile -File .\\scripts\\Instalar-Pack-VX-V022.ps1 -Modo Simular
```

Comprobar 12 agentes, 31 skills, 6 MCP deshabilitados, `mcp_changes=0`, `blockers=[]`. Revisar los destinos de archivos. **No mover ni eliminar personalizaciones externas para eludir los bloqueos**.

El bootstrap se detiene si encuentra agentes inline en configs Kilo, skills compatibles activas en `.agents/skills`, `.kilocode/skills` o `.claude/skills`, rutas adicionales de skills, enlaces/junction/reparse peligrosos o backup demasiado grande (256 MB total o 64 MB por archivo). Si hay bloqueo, mantener instalación actual y diagnosticar individualmente. La opción V4 incremental es diferente: coexistencia, NO limpieza de perfil.

## 3. Aplicar la instalación ya autorizada

Cerrar todas las ventanas de VS Code, VSCodium y Kilo, incluido Agent Manager; esperar a que no existan sesiones escribiendo. Desde una consola PowerShell 7 **externa** al editor:

```powershell
pwsh -NoProfile -File .\\scripts\\Instalar-Pack-VX-V022.ps1 -Modo Aplicar -ConfirmarMigracion -ConfirmarKiloCerrado
```

El script repite preflight y backup DPAPI, compara hashes de los árboles, sustituye solo agentes y skills globales, y verifica las fuentes. **Anotar la ruta de backup exacta** mostrada; no enviar archivos cifrados ni registros privados a GitHub. DPAPI depende del mismo usuario Windows y no equivale a un backup portable.

## 4. Verificar archivos y runtime

```powershell
pwsh -NoProfile -File .\\scripts\\Instalar-Pack-VX-V022.ps1 -Modo Verificar
python -I .\\scripts\\vx_pack_doctor.py --json
```

Iniciar Kilo y ejecutar `/reload`. Comprobar que `vx-integrador` aparece, que hay 31 skills, que `vx-frontend-builder` solo escribe con autorización `ask`, y que `vx-inspector` no edita ni ejecuta Bash. Comprobar carga de `vx-ida-mcp-reverse-engineering` sin instalar/activar IDA MCP automáticamente. **CI no demuestra permisos efectivos**.

## 5. Restaurar únicamente si hace falta

Cerrar Kilo y utilizar exactamente la carpeta DPAPI que imprimió el instalador; no adivinar.

```powershell
$backup = 'PEGAR_RUTA_COMPLETA_BACKUP_DPAPI'
python -I .\\scripts\\vx_pack_bootstrap.py --mode restore --home $HOME --backup-folder $backup --confirm-restore
```

La restauración conservadora bloquea cambios posteriores sin revisión y no permite eliminar archivos nuevos. No usar `--force-restore` para eludir bloqueos. SQLite con WAL necesita respaldo transaccional independiente; nunca se migra aquí.

**Siguiente paso tras probar el runtime:** resolver IDAPython 9.4/MCP, certificar flujo de equipo y publicar resultados en el roadmap sin activar scheduler ni WebAuthn.
