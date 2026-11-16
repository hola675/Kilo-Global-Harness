# VX Pack 0.2.3 — instalación por convivencia en Windows

**Fecha:** 2026-11-16. **Estado:** código preparado; sin despliegue verificado en el PC del operador. Instalación autorizada, pero solo si el inventario real carece de colisiones. No borrar agentes o skills existentes para desbloquear.

## Problema resuelto

El HOME informado por el operador tiene **19 agentes inline** en el JSONC global y skills existentes en las carpetas .agents/skills y .kilocode/skills. El modo limpio 0.2.2 detuvo la sustitución por seguridad, sin escribir archivos. Tener fuentes existentes no constituye necesariamente un fallo; Kilo las admite. Lo importante es la colisión de nombres.

- https://kilo.ai/docs/customize/custom-subagents
- https://kilo.ai/docs/customize/skills

Esta entrega añade un procedimiento de **convivencia**, no migración destructiva. El modo limpio 0.2.2 permanece disponible para perfiles nuevos; no volver a ejecutarlo sobre este HOME.

## Contrato de seguridad

- Conserva byte a byte kilo.jsonc, kilo.json y config.json, sin editar credenciales, modelos, proveedores, MCP ni agentes inline.
- No borra ni mueve directorios .agents/skills, .kilocode/skills, .claude/skills, .kilo/skills ni .config/kilo/agents. Los componentes ajenos permanecen intactos.
- Instala 12 agentes VX, 31 skills VX, comando /vx-ida, reglas y scripts VX; solo actualiza rutas VX y el bloque delimitado en AGENTS.md.
- Bloquea coincidencia de ID entre agentes VX e inline; entre skills VX y cualquier directorio de compatibilidad; nombres globales de distinto casing; rutas/URLs adicionales no inventariables; symlink/junction/reparse; JSONC ilegible; marcadores VX corruptos.
- Si hay conflictos, no modifica HOME ni deshabilita nada.
- Respaldo cifrado con DPAPI CurrentUser de los archivos que cambia, en carpeta vx-coexist-* bajo el directorio de backups global. La restauración solo modifica esos destinos y rechaza cambios posteriores.
- Scheduler, AutoApprove, MCP nuevos, publicación V4.7.2 y escritores concurrentes continúan deshabilitados. La seguridad de permisos efectiva debe comprobarse dentro de Kilo tras /reload.

## 1. Actualizar código (PowerShell 7)

    $ErrorActionPreference='Stop'
    $repo='D:\Proyectos\Kilo-Global-Harness'
    Set-Location -LiteralPath $repo
    if (@(git status --porcelain).Count -gt 0) { throw 'Cambios locales: revisar y conservar.' }
    git switch main
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo cambiar a main.' }
    git pull --ff-only origin main
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo actualizar main.' }

## 2. Diagnóstico y simulación — solo lectura

    pwsh -NoProfile -File .\scripts\Instalar-Pack-VX-Convivencia-V023.ps1 -Modo Diagnostico
    pwsh -NoProfile -File .\scripts\Instalar-Pack-VX-Convivencia-V023.ps1 -Modo Simular

Esperado: inline_agents_existing=19, agents_expected=12, skills_expected=31, ready_to_apply=true, sin collisions ni blockers. Si hay coincidencias, detener y revisar nombres, sin difundir secretos ni editar JSONC. No usar el antiguo instalador de sustitución limpia.

## 3. Aplicación autorizada tras preflight sin bloqueos

Cerrar todas las ventanas de VS Code, VSCodium, Kilo y Agent Manager. Ejecutar en consola PowerShell 7 externa:

    $repo='D:\Proyectos\Kilo-Global-Harness'
    pwsh -NoProfile -File "$repo\scripts\Instalar-Pack-VX-Convivencia-V023.ps1" -Modo Aplicar -ConfirmarConvivencia -ConfirmarKiloCerrado
    if ($LASTEXITCODE -ne 0) { throw 'Instalación no completada; revisar bloqueos y backup.' }

Guardar la ruta exacta del BACKUP DPAPI impresa; no subirla a GitHub.

## 4. Verificación

    pwsh -NoProfile -File "$repo\scripts\Instalar-Pack-VX-Convivencia-V023.ps1" -Modo Verificar
    python -I "$repo\scripts\vx_pack_doctor.py" --json

El doctor fue diseñado originalmente para un Pack limpio: legacy_custom_count u other_custom_count no son fallos por sí mismos en convivencia. Revisar hash de archivos, modo/alias de vx-integrador, vx-inspector (sin bash ni edit), builders (edit: ask), comando /vx-ida y carga de skills real. IDA MCP no se activa ni configura.

## 5. Restauración

Cerrar Kilo. Los backups 0.2.2 y 0.2.3 no son intercambiables.

    $backup = 'PEGAR_RUTA_COMPLETA_vx-coexist-DEL_RESULTADO'
    pwsh -NoProfile -File "$repo\scripts\Instalar-Pack-VX-Convivencia-V023.ps1" -Modo Restaurar -CarpetaRespaldo $backup -ConfirmarRestauracion -ConfirmarKiloCerrado

Restauración parcial o archivos con hash diferente se bloquean y requieren revisión manual; nunca eliminar archivos ajenos. DPAPI depende del mismo usuario de Windows. Este proceso no migra ni respalda transaccionalmente SQLite.

## Puertas del siguiente ciclo

Conservar los 19 agentes inline y skills externos; resolver solo colisiones comprobadas. Certificar Kilo runtime tras /reload, comprobar permisos efectivos y la skill IDA. Solo entonces declarar instalación operativa.

## Actualización de contenido Pack V0.2.4 (posterior a instalación inicial)

La instalación inicial V0.2.3 quedó comprobada en el Windows del operador: 12/12 agentes VX, 31/31 skills VX y contenido íntegro. El nuevo contenido añade comando /vx-certificar, guía de evidencias y aclara que un bloqueo external_directory no es un fallo de instalación. Antes de volver a aplicar el instalador por convivencia V023 (que sigue siendo el mecanismo de distribución), ejecutar Diagnostico y Simular y comprobar que los nuevos destinos VX no colisionan. Cerrar Kilo, conservar el backup anterior y anotar el nuevo backup si se decide actualizar. No modificar JSONC/MCP/skills externas. [Evidencia y pruebas](VX-CERTIFICACION-RUNTIME-20261116.md).
