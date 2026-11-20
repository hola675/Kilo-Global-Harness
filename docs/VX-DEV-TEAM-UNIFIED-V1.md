# VX Dev Team Core Unificado — instalación V1.0 RC1

**Fecha:** 2026-11-20. **Estado:** SOURCE / pendiente revisión CI y runtime local. **No instalado automáticamente.**

## Decisión

Unificar el Pack VX 0.4.0 y Dev Team 2.3.0 en una única instalación global. No ejecutar dos instaladores ni crear dos líderes. Instalar los componentes declarados en [el manifiesto unificado](../registry/vx-unified-pack-v1.json), no concatenar indiscriminadamente las dos listas históricas.

| Familia | Seleccionados | Rol |
| --- | ---: | --- |
| Líder visible | 1 | vx-dev-team, único agente principal del pack |
| Analistas especialistas | 10 | Dev Explorer, Architect, Frontend, Backend, Data, Platform, Reviewer, Quality, Security y Research; ocultos/read-only |
| Implementadores | 6 | Frontend, Backend, Data, QA, Docs y Editorial; ocultos, edit/write/apply_patch con ask |
| Cloudflare | 1 | vx-workers-adviser; oculto/read-only |
| **TOTAL** | **18** | **1 visible y 17 ocultos** |

### Skills

**43 skills**: 18 Dev CORE, más 25 VX complementarias seleccionadas por aportar una capacidad de ejecución o dominio que no se cubre solo con la estrategia CORE (TypeScript, Python, Cloudflare, SQL, E2E, Docs, Git/CI, performance, observabilidad, editorial, IDA, incidentes y colaboración, entre otras). La lista exacta y sus rutas únicas están en el manifiesto. Las skills se cargan bajo demanda: nunca las 43 simultáneamente.

Se conservan en Git las 26 Dev adicionales que aún eran propuestas y las 7 VX no incluidas. No se activan waves W2-W5 automáticamente ni se elimina la documentación de VX Evolution.

### Retiro explícito de duplicados

Se desinstalan solamente seis agentes VX anteriores: vx-integrador, vx-inspector, vx-researcher, vx-security-reviewer, vx-test-analyst y vx-frontend-adviser. Sus funciones pasan al líder y a especialistas Dev. Se retiran exclusivamente siete archivos SKILL.md previamente administrados por VX: vx-evolution-core, vx-self-improvement, vx-security-review, vx-architecture-decisions, vx-codebase-investigation, vx-supply-chain-review y vx-accessibility-review. Sus directorios, archivos extra y código versionado quedan intactos; un backup DPAPI conserva los originales.

**No tocar:** kilo.jsonc, MCP, modelos, credenciales, AutoApprove, skills de terceros, agentes inline externos, rutas de proyectos, bases de datos o otros archivos de nombres desconocidos. Si hay colisiones en fuentes externas, bloquear y reconciliar en vez de borrar.

## Un solo procedimiento de instalación en Windows

**No instalar hasta que el PR haya pasado CI y revisión y esté integrado a main.** Utilizar PowerShell 7 externo. En D:\Proyectos\Kilo-Global-Harness, con git limpio y main sincronizada:

### 1. Preflight sin escritura

    pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Diagnostico
    pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Simular

La respuesta debe indicar READY, 18 agentes y 43 skills, sin bloqueos ni cambios a configuración. Revisar el número de archivos a retirar antes de confirmar.

### 2. Aplicación

Cerrar previamente VS Code, VSCodium y Kilo Desktop (y sesiones que estén modificando la configuración). El instalador verifica que main coincide con origin/main y que no hay cambios locales.

    pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Aplicar -ConfirmarInstalacion -ConfirmarRetirarVXLegacy -ConfirmarKiloCerrado

Crear respaldo DPAPI CurrentUser, verificar que puede descifrarse y comprobar los archivos antes de escribir. El motor instala archivos con escritura atómica y retira solo nombres de la allowlist legacy declarada. Ante un fallo intenta rollback conservador, sin eliminar directorios.

### 3. Verificación y pruebas funcionales

    pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Verificar

Verificar que el resultado declara SOURCE_FILES_MATCH_RUNTIME_NOT_VERIFIED. Reiniciar Kilo y comprobar en la interfaz/CLI que hay un líder visible, 17 subagentes ocultos, skill loading real y task efectivo. Probar lectura Explorer, un builder con permisos ask en fixture aislado, editorial y revisión independiente; no usar datos ni infraestructura reales.

### 4. Restauración

Guardar la ruta absoluta de BACKUP DPAPI impresa al instalar, **no compartirla ni subirla a GitHub**. Con Kilo cerrado:

    pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Restaurar -CarpetaRespaldo RUTA_REAL_BACKUP -ConfirmarRestauracion -ConfirmarKiloCerrado

El rollback rechaza sobrescribir archivos modificados desde la instalación; investigar y recuperar de forma dirigida, no forzar.

### Instalación interrumpida antes de confirmar INSTALLED

Si hubo un corte de energía o un error de PowerShell tras crear un respaldo DPAPI, el recibo puede quedar en `BACKED_UP` aunque algunos archivos se hayan actualizado. La restauración normal **rechaza** ese estado; usar recuperación extraordinaria, explícita y con Kilo cerrado, **con la ruta real de ese respaldo**:

    pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Restaurar -CarpetaRespaldo RUTA_REAL_BACKUP -ConfirmarRestauracion -RecuperarInstalacionInterrumpida -ConfirmarKiloCerrado

La recuperación verifica para todos los destinos la allowlist de archivos administrados, el respaldo DPAPI y los hashes `before/after`. Si un archivo tiene un tercer valor inesperado, **se detiene sin sobrescribir**: conservar el respaldo y revisar el conflicto manualmente. Nunca aplicar esta opción para omitir colisiones o modificar archivos ajenos.

### Skills de terceros y colisiones de identidad

El preflight comprueba el ID tanto del directorio como del campo `name` del frontmatter de cada skill externa bajo `~/.kilo/skills`, `~/.agents/skills`, `~/.kilocode/skills` y `~/.claude/skills`. Una skill ajena cuyo archivo esté en otro directorio pero declare un nombre del Core provoca `BLOCKED`. No se elimina ni renombra automáticamente la skill externa.

## Política operativa de menor burocracia

Para tareas ordinarias el líder determina automáticamente Git root, branch, SHA y archivos por inspección. No exigir formularios ni tickets manuales si el entorno es suficiente. Elegir el mínimo de especialistas; el líder puede resolver tareas sencillas sin delegar. Los seis implementadores pueden editar proyectos con consentimiento de Kilo; no se convierten en modos principales.

Conservar salvaguardas necesarias: no elevar ACL por falta de herramienta, un escritor por worktree, no producción ni cambios destructivos sin autorización, no publicar ni fusionar sin evidencias, no declarar runtime PASS solo por hashes iguales.

## Changelog

- V1.0 RC1 (2026-11-20): 18 agentes únicos, 43 skills seleccionadas, un solo instalador reversible, seis agentes y siete skills históricas retirables, pruebas de instalación/rollback en suite viva; source aún no equivale a runtime instalado.

## Comandos compatibilizados (V1.0 RC1)

La instalación única gestiona también tres comandos globales: **/vx-equipo**, **/vx-dependencias** y **/vx-editorial**. Sus rutas apuntan al único líder `vx-dev-team`; los dos primeros ya no invocan al antiguo `vx-integrador`. El comando experimental histórico `/vx-p2` se retira del HOME con respaldo DPAPI porque seleccionaba directamente a `vx-docs-builder`, que ahora debe ser subagente oculto. El fuente `commands/vx-p2.md` permanece versionado para trazabilidad. Los demás comandos del usuario se conservan, sin borrados por nombre o coincidencias amplias.

**Inventario final bajo gestión del instalador:** 18 agentes, 43 skills, 3 comandos y un bloque de política global VX. Se pueden retirar exactamente seis agentes, siete skills y un comando históricos, si existen; todo el material anterior cambiado se respalda antes de mutar. La existencia de otros comandos o recursos ajenos no convierte su funcionalidad en certificada.

- V1.0 RC1 ajuste de seguridad: recuperacion explicita de respaldo `BACKED_UP` y bloqueo de colisiones por `name:` en skills ajenas globales; casos negativos agregados a la suite viva.
