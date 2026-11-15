# VX Evolution — Reproducibilidad TTY heredada (tests, sin cambios de runtime)

**Edición:** 2026-11-15 · **Ámbito:** módulos de pruebas V4.5/V4.5.1 · **Alcance de código:** exclusivamente `tests/test_vx_meeting_v45.py` y `tests/test_vx_joint_meeting_v451.py`.

## Antecedente

El operador reprodujo en el mismo Windows dos errores de aserción TTY tanto en `origin/main` como en la rama V4.7.1, con el mismo comando. Las pruebas esperaban el texto `sin TTY denegado` pero recibían `Confirmacion cancelada`. Los dos helpers llamaban a `subprocess.run(..., capture_output=True)` sin controlar `stdin`. Capturar stdout/stderr **no** redirige por sí mismo stdin: el subproceso podía heredar una terminal interactiva del ejecutor y pasar `sys.stdin.isatty()`. En el entorno del operador, un EOF posterior en `input()` devolvió `Confirmacion cancelada`.

## Corrección mínima

Se añadió **`stdin=subprocess.DEVNULL`** a los dos helpers que invocan el CLI `vx_evolution_core.py`. Esto hace no interactiva la entrada de todos los subprocesos de esas clases de pruebas, independiente de que el runner sea PowerShell, Kilo Desktop o GitHub Actions.

- **No se modifica** `local_confirmation()` ni `sys.stdin.isatty()` del runtime de producción.
- **No se crea** un bypass: las operaciones de decidir/cerrar siguen exigiendo una terminal y confirmación deliberada para su uso real.
- Los tests que esperan rechazo no interactivo verifican ahora la ruta prevista en lugar del comportamiento accidental de un stdin heredado.
- La corrección no autentica identidad del usuario ni implementa el contrato de aprobación V4.7.1.

## Verificaciones

Ejecutar en el repositorio (sin HOME real):

```powershell
python -I -m unittest discover -s tests -p 'test_vx_meeting_v45.py' -v
python -I -m unittest discover -s tests -p 'test_vx_joint_meeting_v451.py' -v
git diff --check
```

La CI Windows existente incluye los tests de reunión anteriores. Se requiere PASS en CI de PR y posterior al merge. Para cerrar la incidencia **local interactiva**, el operador debe confirmar esas dos suites desde PowerShell en su PC; la CI no demuestra por sí sola reproducción de stdin de una consola interactiva.

## Invariantes

Sin instalación, edición de HOME global, SQLite real, permisos, AutoApprove, MCP, scheduler, agentes, skills, modelos ni configuración `kilo.jsonc`. El cambio es independiente de V4.7.2. La rama temporal se elimina después del merge y verificación de `main`.
