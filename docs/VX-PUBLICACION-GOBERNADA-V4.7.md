# VX Evolution V4.7.0 — contrato de publicación gobernada (fase inicial)

**Estado:** integrado en `main` mediante `36a73e01fe46d17573f46baf82cf8c88bf5d7559`; CI Windows PASS. Implementado como diseño de contrato y `DRY_RUN`; no instala, aplica, aprueba, restaura ni cambia el HOME real. El flujo usa un HOME Windows temporal sintético para pruebas. Scheduler, reuniones automáticas y procesos residentes no forman parte de esta fase.

## Contrato `vx-component-manifest/1`

Cada componente declara `id` estable (`[a-z][a-z0-9-]{0,63}`), `version` SemVer 2.0.0, `state`, dependencias de versión exacta y una lista no vacía de archivos. Cada archivo incluye rutas relativas `source`/`target` y SHA-256 minúsculo de los bytes de origen. El CLI vuelve a calcular el hash antes de planear; una discrepancia, ruta insegura, componente duplicado, destino duplicado (comparado con `casefold()` para evitar colisiones en Windows) o dependencia inválida detiene el plan completo.

Estados del contrato: `PREPARADO`, `CI_PASS`, `VERIFICADO_EN_PC`, `APROBADO`, `APLICADO`, `ROLLBACK` y `NO_VERIFICADO`. El preview admite únicamente `PREPARADO` y `NO_VERIFICADO`: reporta `PREPARADO` para la propuesta y no afirma resultados de fases posteriores. Un hash garantiza integridad de bytes comparados; no valida autoría, firma, procedencia ni autorización.

Ejemplo mínimo del manifiesto (el hash corresponde exactamente a los bytes `candidate` más LF):

```json
{
  "schema": "vx-component-manifest/1",
  "components": [{
    "id": "vx-demo",
    "version": "1.2.3",
    "state": "NO_VERIFICADO",
    "dependencies": [],
    "files": [{
      "source": "package/vx-demo.md",
      "target": ".config/kilo/agents/vx-demo.md",
      "sha256": "34d835da31fa37550123ef54e1bbf04e1898d286dec5d8cd735789951cc3649d"
    }]
  }]
}
```

El preview admite solo componentes `vx-*` y limita cada destino a la ruta administrada del mismo componente (por ejemplo `.config/kilo/agents/<id>.md`, `.config/kilo/commands/<id>.md`, `.config/kilo/rules/<id>.md`, `.config/kilo/harness/<id>/...` o `*/skills/<id>/SKILL.md`). Rechaza traversal, enlaces y reparse points (incluidas junctions Windows), incluso symlinks colgantes; prohíbe explícitamente `kilo.jsonc`, settings, permisos, modelos, MCP, SQLite y manifiestos de instalación. Informa acciones `CREAR`, `ACTUALIZAR` o `SIN_CAMBIOS`, hashes y un SHA-256 canónico del plan que cubre esquema, componentes ordenados, versiones, estados, dependencias normalizadas y cambios propuestos. No crea directorios, archivos temporales, backups o manifiestos. `apply_supported=false` es parte del informe y no existe comando de aplicación en este módulo. Como el preview no bloquea escrituras concurrentes de terceros, el árbol del paquete y el HOME sintético deben permanecer estables durante la lectura; un plan no es autorización ni una captura transaccional.

## Prueba

```powershell
python -I -m unittest discover -s tests -p 'test_vx_publish_preview_v470.py' -v
```

Las pruebas crean HOME sintético bajo `TemporaryDirectory`, fijan archivos protegidos ficticios y comparan su snapshot. En Windows, las pruebas de symlink pueden quedar `SKIPPED` si el host no permite crearlos; el test controlado de guard cubre que se revise la ruta aun cuando `exists()` sea falso, pero no se presenta como validación del symlink nativo de Windows. El workflow de CI debe ejecutar esta suite en `windows-latest`. Esto no equivale a validación en Kilo Desktop ni HOME real.

## Aprobación y rollback de fases futuras (NO IMPLEMENTADOS)

Antes de cualquier publicación posterior deberá existir una aprobación humana explícita, específica al objeto, diff, dependencias y `plan_sha256`; rechazo, expiración, cambio de hash o discrepancia de manifiesto significan no aplicar. Ni el chat, una decisión de reunión, AutoApprove, un hash sin firma ni la aprobación del propio autor autorizan la publicación. La aprobación separada no se implementa en V4.7.0-preview.

Una fase posterior que incorpore escritura deberá respaldar solo destinos VX permitidos, verificar hashes de original y copia, registrar hash instalado, restaurar conservadoramente ante error y negarse a sobrescribir archivos cambiados desde la aplicación. Rollback nunca borrará datos ajenos, `kilo.jsonc`, settings, permisos, modelos, MCP o SQLite. Esta guía no habilita ni prueba tales operaciones; el instalador reversible existente sigue sin cambios.
