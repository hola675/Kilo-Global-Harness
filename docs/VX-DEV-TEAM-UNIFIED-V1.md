# VX Dev Team · Instalación única del Core 1.6.2-rc1

**Actualización:** 2026-11-22 · **Estado:** fuente versionada. Instalación local y concurrencia real de Kilo Desktop requieren pruebas separadas.

Este es el único paquete soportado en el repositorio. No utilizar instaladores V3/V4, DevTeam-Only, packs de convivencia, clones del registro antiguo ni ejecutables de VX Evolution que ya no pertenecen al Core actual.

## Qué instala

- **18 agentes:** un líder visible **VX Dev Team** (`vx-dev-team`) y 17 subagentes ocultos (10 especialistas Dev read-only, seis builders con edición `ask`, asesor Workers read-only).
- **57 Skills:** 18 CORE, 35 CAPABILITY y 4 CONTEXTUAL; las cuatro contextuales no se añaden automáticamente a la allowlist del líder/builders.
- **3 comandos:** `/vx-equipo`, `/vx-dependencias`, `/vx-editorial`.
- **2 soportes:** `vx_task_dag.py` y copia del manifiesto de instalación.
- **AGENTS.md global completo** procedente de `rules/AGENTS-global-managed.md`: se sustituye enteramente, guardando copia cifrada del anterior.
- **Estado SQLite:** la cola persistente `~/.config/kilo/harness/state/vx-team-queue.sqlite3` se crea si falta o migra de forma aditiva a esquema v1. Conserva tareas, eventos e información existente; los snapshots de WAL están en el backup DPAPI.

**Entrypoint:** `scripts/Instalar-DevTeam-Unificado.ps1`. Backend en `scripts/vx_unified_pack.py` y dos módulos de seguridad DPAPI: `scripts/vx_pack_coexist_v023.py` y `scripts/vx_pack_bootstrap.py`. Aunque esos dos nombres son antiguos, ambos están **importados por el instalador vigente** y no se pueden retirar sin reemplazo probado.

## Instalación Windows

Abrir PowerShell 7 **fuera de Kilo**, cerrar Kilo Desktop/VS Code/VSCodium para aplicar y verificar que el checkout local está limpio y sincronizado.

```powershell
Set-Location 'D:\Proyectos\Kilo-Global-Harness'
git switch main
git fetch origin --prune
git pull --ff-only origin main
git status --short

pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Diagnostico
pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Simular
```

Examinar `status`, `blockers`, `state_status`, `files_to_create`, `files_to_replace` y `managed_legacy_candidates`, además del estado Git y los worktrees inventariados. La limpieza automática se limita a hasta 14 rutas legacy VX del manifiesto, nunca a ramas, worktrees, código del proyecto ni bases de datos de otras aplicaciones. Solo después de aprobar el alcance de sustitución del Core, ejecutar:

```powershell
pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 `
  -Modo Aplicar `
  -ConfirmarInstalacion `
  -ConfirmarRetirarVXLegacy `
  -ConfirmarKiloCerrado

pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Verificar
```

`Aplicar` exige `main` sincronizada, árbol limpio, Kilo cerrado, backup cifrado DPAPI CurrentUser y lista exacta de los **14 paths históricos** que puede retirar de HOME. No borra recursos de terceros, no toca `kilo.jsonc`, credenciales, MCP ni AutoApprove. Toda ruta reemplazada queda incluida en el respaldo de restauración; también el estado SQLite anterior, en un snapshot consistente. Las migraciones SQLite son versionadas, conservadoras, idempotentes y verificadas mediante integridad. Si la versión es desconocida o la base no se puede validar, se bloquea sin sobrescribirla.

## Informe automático de cada instalación y actualización

Al ejecutar **Aplicar**, el motor guarda en la carpeta privada de respaldo DPAPI tanto `install-report.json` como `install-report.md`. En la salida de consola presenta las rutas, conteos y situación de SQLite. El informe detalla para cada archivo administrado: creado, reemplazado, eliminado o sin cambios; versión y fecha declaradas antes y después (o «No declarada»); hashes y coincidencia con lo instalado. Distingue el script `vx_task_dag.py` instalado en Kilo de scripts que solo se ejecutan en el checkout, e incluye conteos agregados de tablas SQLite sin exportar tareas.

El modo `Informe` **no reinstala, no migra y no borra**; reconstruye un informe para respaldos anteriores que aún no tenían reportes. Si existe uno, lo conserva sin reescribir el historial:

```powershell
pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Informe -CarpetaRespaldo 'C:\Users\Admin\.config\kilo-harness-backups\vx-unified-20261122-152634-3933e6fb'
```

Sin `-CarpetaRespaldo` elige el recibo más reciente. Los informes no demuestran por sí mismos que Kilo habilite las herramientas y permisos del agente. Solo se reportan elementos del manifiesto y sus rutas aprobadas; nunca se limpia trabajo de proyecto por inferencia.


### R2 — Observador Kilo experimental (desactivado)

El prototipo se mantiene **solo en el checkout** en `runtime/kilo-observer/vx-runtime-observer.js`; no se copia a `~/.config/kilo/plugin/`, no se añade a `kilo.json(c)`, no eleva ACL y no se inicia con el instalador. Requiere conjuntamente `VX_OBSERVER_ENABLE=1` y `VX_OBSERVER_PROJECT=<nombre-exacto-de-directorio>` para hacer cualquier escritura; ninguna sesión de otro proyecto queda incluida. La carga en Kilo Desktop y la existencia del runtime Bun con `bun:sqlite` deben comprobarse en una instalación/laboratorio aislado. La documentación oficial de plugins confirma hooks para CLI y VS Code, **no acredita Desktop de este usuario**.

El código observa `task`, `skill`, `board_post`, `board_read` y eventos de ciclo de sesión, **sin leer, serializar ni persistir argumentos, prompts, respuestas, texto de archivos, credenciales, rutas completas ni IDs de sesión sin hash**. Las observaciones quedan en una base separada, `~/.config/kilo/harness/state/vx-runtime-observations.sqlite3`, con clave de idempotencia, tabla `host_observations` y esquema independiente v1. No toca las tablas `tasks`, `events` ni `project_config` de la cola existente: un hook observado no es un task verificado.

Consultar su estado sin crear ni mutar ninguna DB:

```powershell
python -I .\scripts\vx_task_dag.py --observer-report
python -I .\scripts\vx_task_dag.py --observer-report --project vecidya
```

Mientras no se autorice su activación en un HOME de prueba, el resultado esperado es `ABSENT`. No activar `VX_OBSERVER_ENABLE=1` ni `VX_OBSERVER_PROJECT` en sesiones productivas/Vecidya en curso. Al iniciar el laboratorio, copiar la fuente al directorio plugin de ese perfil y verificar eventos reales antes de extender el instalador. Una vez verificado, R3 contempla enlazar eventos observados con IDs de tareas reales, sin inferir resultados por el mero regreso de una herramienta.

## Restauración

Conservar privada la carpeta `vx-unified-...` que informa el motor. Si una instalación genera errores, consultar antes de restaurar modificaciones posteriores en los destinos:

```powershell
pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 `
  -Modo Restaurar `
  -CarpetaRespaldo 'RUTA_ABSOLUTA_DEL_BACKUP_DPAPI' `
  -ConfirmarRestauracion `
  -ConfirmarKiloCerrado
```

La recuperación de una aplicación interrumpida utiliza además `-RecuperarInstalacionInterrumpida` solo si se confirma el estado. Ninguna restauración debe machacar ediciones de terceros posteriores. **Si la cola SQLite recibió tareas o eventos nuevos tras instalar, Restaurar se bloquea en lugar de perderlos.** La recuperación segura requiere revisar esos cambios antes de revertir.

## Después de instalar

Abrir Kilo Desktop y certificar invocaciones reales de `skill`, `task`, permisos de escritura de builders, `task(background: true)` y `board_post/board_read` si están presentes. El líder y seis builders tienen Board autorizado en source; los once analistas read-only no.

**Tres estados diferentes:** `SOURCE_PASS` (CI) → `INSTALLED_FILES_MATCH` (verificación del instalador) → `HOST_RUNTIME_PASS` (evidencia en Kilo). La cola SQLite no ejecuta agentes ni funciona con Kilo cerrado.

Ver [arquitectura](ARQUITECTURA.md), [autonomía](VX-DEV-TEAM-AUTOPILOT-V2.md) y [registro de depuración](VX-HARNESS-INVENTARIO-AUDIT-20261121.md).


## Roadmap vivo de implementación — 2026-11-23

**Objetivo:** evolucionar un único Harness instalable, sin perder la ejecución actual de Vecidya ni confundir fuente, instalación y runtime. Esta sección es la fuente canónica de avance; no generar documentos de roadmap por fase.

| Orden | Fase | Estado | Criterio de aceptación |
|---|---|---|---|
| R1 | Saneamiento de contratos y referencias | SOURCE_PASS_PENDIENTE_MAIN | Ningún agente referencia un ejecutable retirado o Skill inexistente; documentación/selector/manifiesto concuerdan; CI PASS |
| R2 | Observador no invasivo de Kilo | SOURCE_PASS_NO_ACTIVADO | Plugin local desactivado por defecto, sin alterar herramientas ni registrar conversaciones, prompts, tokens, rutas completas o credenciales |
| R3 | Persistencia del runtime | PENDIENTE_HOST | Eventos observados con idempotencia y consulta solo lectura; no confundirlos con tareas DAG registradas ni éxito certificado |
| R4 | Coordinación multiagente | PENDIENTE_HOST | Conflictos de escritura probados, ID real de host, recuperación y barrera de integración; sin elevar ACL |
| R5 | Certificación integral | PENDIENTE_HOST | CI Windows y laboratorio real de Kilo con herramientas, Skills, delegación, Board y persistencia; evidencia verificable |
| R6 | Consolidación Git/contexto | BLOQUEADO_LIMPIEZA_REMOTA | Reducir duplicaciones sin perder conducta; PR y CI; retirar solo ramas fusionadas sin trabajo exclusivo |

### Gates de seguridad y reversibilidad

- **G0:** Inventariar checkout, PR, CI, worktrees y respaldos. No interrumpir Vecidya.
- **G1:** Cambiar referencias/documentación/versiones sin modificar ACL ni otros proyectos.
- **G2:** Investigar el contrato oficial de eventos Kilo; el soporte documentado en CLI/VS Code no certifica el Desktop. El observador se entrega desactivado.
- **G3:** Laboratorio aislado antes de activar el plugin globalmente: sin secretos, contenido de cliente, salida de herramientas ni rutas completas. Si el host no soporta hooks, seguir con el ledger de sesión.
- **G4:** Los eventos del hook demuestran observación, no entrega, aprobación o estado VERIFIED. Persistencia y cola DAG requieren contratos separados.
- **G5:** Cambios por PR, CI y respaldo. Para instalar en Windows, Kilo cerrado, confirmación explícita y restauración disponible.

**Evidencia de partida:** 53 pruebas CI Windows correctas tras R1/R2; usuario confirmó instalación de 18 agentes/57 Skills y base SQLite íntegra con tres tablas y cero registros de tareas, eventos y proyectos. Hubo delegación real en Vecidya, no reflejada automáticamente en esa base.

**Bloqueo Git:** 14 ramas remotas de PR fusionados continúan en GitHub. El navegador de automatización no posee autenticación para borrarlas. Para continuar sin crear una rama adicional se reutiliza temporalmente una rama fusionada, sincronizada con main mediante merge no destructivo (sin force-push).
