# Arquitectura vigente · Kilo Global Harness / VX Dev Team

**Fuente de verdad:** `registry/vx-unified-pack-v1.json` (Core VX **1.6.2-rc1**). Esta guía sustituye el diagrama V3 de `vx-integrador/vx-inspector`, conservado únicamente en el historial Git.

## Capas

1. **Kilo runtime del operador:** cliente Kilo Desktop/Kilo Code con su `kilo.jsonc`, credenciales, modelos, permisos efectivos y MCP. El Harness no reescribe esos recursos y ningún source test acredita su estado.
2. **Política global administrada:** `rules/AGENTS-global-managed.md`, instalada mediante sustitución completa de `~/.config/kilo/AGENTS.md` por el instalador unificado, con respaldo DPAPI de los bytes anteriores. No hay un segundo AGENTS por proyecto generado por VX.
3. **Líder:** `agents/vx-dev-team.md` se instala como **VX Dev Team** acompañado de la versión global publicada del Harness en `displayName`, único modo principal visible. La versión individual y última fecha del líder, al igual que las de cada subagente, se anotan mediante dos comentarios en el frontmatter YAML; el historial resumido reside solo en `registry/AGENTS-VERSIONS.md`. Selecciona Skills permitidas y coordina tareas dependientes, revisión, Git y reportes.
4. **Subagentes:** diez roles Dev en `runtime/dev-team-v2r/agents/`, seis builders en `agents/` y `vx-workers-adviser`. **17 ocultos** subordinados al líder. Los especialistas de lectura no escriben ni delegan.
5. **Skills:** 57 fuentes seleccionadas entre `skills/` y `runtime/dev-team-v2r/skills/`. Se copian globalmente y se cargan solo con permiso `skill` efectivo. Catálogos de propuestas no amplían la allowlist.
6. **Comandos del pack:** únicamente `/vx-equipo`, `/vx-dependencias` y `/vx-editorial`. Los comandos anteriores ya no están en el árbol activo; su historia permanece en Git.
7. **Control de dependencias:** `scripts/vx_task_dag.py` con DAG y cola SQLite opcional en HOME privada. La cola persiste metadatos de coordinación; no despacha, bloquea físicamente archivos, ejecuta worktrees ni deja tareas trabajando al cerrar Kilo.
8. **Ejecución y progreso:** herramientas nativas `task` y, cuando estén disponibles, `board_read/board_post` de Kilo Swarm. `task(background: true)` comparte workspace, no crea worktree. El líder puede continuar leyendo/diseñando fuera de rutas reservadas; dos escritores simultáneos solo con rutas exactas disjuntas (`write_scope: EXACT_FILES`) y ACL reales.
9. **Git/CI:** un integrador por worktree, PR sobre `main`, pruebas focalizadas, revisión por riesgo y limpieza de rama verificada. `.github/workflows/validar-harness.yml` valida archivos fuente y contratos Windows, no autoría de subagentes runtime.

## Cadena de ejecución comprobable

```text
Petición → VX Dev Team (único líder visible)
          ├─ PLAN / DAG / fuentes e instrucciones globales
          ├─ task → lectores read-only (si ayuda)
          ├─ task(background:true) → builder A [archivos exactos]
          ├─ task(background:true) → builder B [otros archivos]
          ├─ trabajo propio seguro del líder (fuera de reservas)
          ├─ eventos Swarm si el host lo permite
          └─ task_result → verificación independiente
                            ↓
                    integración y CI
                            ↓
                       PR → main
```

El planificador **no es un scheduler de modelos**. Un mensaje Swarm no confirma que otro agente lo leyera ni autoriza un cambio. Un resultado de builder no es evidencia suficiente de autoría: comprobar trazas de escritura y diff cuando el objetivo lo requiere.

## Instalación y reversión

Utilizar exclusivamente `scripts/Instalar-DevTeam-Unificado.ps1` para el paquete Core actual. Su backend `scripts/vx_unified_pack.py` conserva pruebas de compatibilidad, validación de propiedad, backup DPAPI y restauración controlada. **No ejecutar simultáneamente** los instaladores históricos V3/V4, DevTeam-Only, VX 0.2.2 ni convivencia VX 0.2.3 para administrar este mismo perfil global.

El Core conserva únicamente seis scripts en `scripts/`: el instalador PowerShell, su motor Python, dos módulos de seguridad/backup importados, el DAG/cola y el validador de metadatos del CI. Se retiraron los demás instaladores y los registros antiguos; consultar el [informe de depuración](VX-HARNESS-INVENTARIO-AUDIT-20261121.md).

## Configuración y seguridad

- Toda instalación global escribe solo assets VX permitidos dentro del HOME del usuario, con confirmación/backup; nunca en repositorios de clientes.
- Sin autoelevación de ACL, AutoApprove, MCP, modelos, tokens, secretos o infraestructura.
- `agent_manager` permanece denegado al líder Desktop. Los worktrees se preparan solo cuando existe una herramienta autorizada y el repositorio lo exige.
- Los roles `board_read/post: allow` son exactamente el líder y seis builders, condicionados a que esas herramientas existan en el host.
- `SOURCE_PASS`, `INSTALLED_FILES_MATCH` y `HOST_RUNTIME_PASS` son estados distintos.

Ver [guía operativa](VX-DEV-TEAM-AUTOPILOT-V2.md), [manifiesto](../registry/vx-unified-pack-v1.json) y [política global](../rules/AGENTS-global-managed.md).
