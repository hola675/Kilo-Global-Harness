# VX Evolution — Reproducibilidad TTY heredada (tests, sin cambios de runtime)

**Edición:** 2026-11-15 · **Ámbito:** módulos de pruebas V4.5/V4.5.1 · **Alcance de código:** exclusivamente `tests/test_vx_meeting_v45.py` y `tests/test_vx_joint_meeting_v451.py`.

## Antecedente

El operador reprodujo en el mismo Windows dos errores de aserción TTY tanto en `origin/main` como en la rama V4.7.1, con el mismo comando. Las pruebas esperaban el texto `sin TTY denegado` pero recibían `Confirmacion cancelada`. Los dos helpers llamaban a `subprocess.run(..., capture_output=True)` sin controlar `stdin`. Capturar stdout/stderr **no** redirige por sí mismo stdin: el subproceso podía heredar una terminal interactiva del ejecutor y pasar `sys.stdin.isatty()`. En el entorno del operador, un EOF posterior en `input()` devolvió `Confirmacion cancelada`.

## Corrección mínima

La primera tentativa empleó **`stdin=subprocess.DEVNULL`**. La CI Windows de PR #27 falló de nuevo: en Windows `NUL` es un dispositivo de caracteres y la implementación de Python puede informar **`sys.stdin.isatty() == True`**, por lo que el CLI entraba a pedir confirmación y terminaba con `Confirmacion cancelada`. Se sustituyó por **`stdin=subprocess.PIPE`**, que proporciona un conducto no interactivo; `subprocess.run()` cierra la tubería durante `communicate()` sin suministrar respuesta. Esta es la corrección propuesta actualmente para los dos helpers. Referencia de Python: https://docs.python.org/3.13/library/sys.html#sys.stdin y https://docs.python.org/3/library/subprocess.html#subprocess.PIPE.

- **No se modifica** `local_confirmation()` ni `sys.stdin.isatty()` del runtime de producción.
- **No se crea** un bypass: las operaciones de decidir/cerrar siguen exigiendo una terminal y confirmación deliberada para su uso real.
- Los tests que esperan rechazo no interactivo deben verificar la ruta prevista, con `sys.stdin.isatty() == False` desde la tubería. La verificación en Windows aún depende del siguiente run de CI.
- La corrección no autentica identidad del usuario ni implementa el contrato de aprobación V4.7.1.

## Verificaciones

Ejecutar en el repositorio (sin HOME real):

```powershell
python -I -m unittest discover -s tests -p 'test_vx_meeting_v45.py' -v
python -I -m unittest discover -s tests -p 'test_vx_joint_meeting_v451.py' -v
git diff --check
```

La CI Windows existente incluye los tests de reunión anteriores. **La primera ejecución de la PR (run `43730605841`) fue FAIL con DEVNULL**; esa falla sirvió para detectar el comportamiento de NUL en Windows. Se requiere PASS del nuevo run con PIPE y posterior al merge. Sin PASS no hay autorización para integrar. Para cerrar la incidencia **local interactiva**, el operador debe confirmar esas dos suites desde PowerShell en su PC; la CI no demuestra por sí sola reproducción de stdin de una consola interactiva.

## Invariantes

Sin instalación, edición de HOME global, SQLite real, permisos, AutoApprove, MCP, scheduler, agentes, skills, modelos ni configuración `kilo.jsonc`. El cambio es independiente de V4.7.2. La rama temporal se elimina después del merge y verificación de `main`.
