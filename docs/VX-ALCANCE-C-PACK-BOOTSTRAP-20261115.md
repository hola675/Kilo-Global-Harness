# VX Evolution — Alcance C y diseño preliminar del Pack inicial (2026-11-15)

**Estado:** `VX-D14` CONFIRMADA por el operador; arquitectura de bootstrap/pack propuesta y pendiente de decisiones. **Solo documentación; ningún cambio en Kilo, permisos, HOME, instalador, MCP, SQLite, scheduler o runtime.**

## 1. Decisión confirmada VX-D14 — Alcance C

**VX Evolution limita su evaluación, administración, formación, versionado, publicación y mejora a componentes propios VX, identificados mediante un registro de propiedad y procedencia.** La detección de componentes externos para *inventario inicial, compatibilidad, respaldo y diagnóstico de la instalación* no los incorpora a la gobernanza continua. Ningún agente, skill, MCP, regla o configuración ajena se elimina, reemplaza, deshabilita, actualiza o reconfigura por decisión autónoma de VX. El operador podrá autorizar una migración de entorno concreta más adelante, pero esa operación es distinta de la gestión continua VX.

La marca de nombre `vx-*` es una pista, no prueba suficiente de propiedad: se necesita manifiesto del pack, fuente reconocida, versión/hash y validación de procedencia.

## 2. Propuesta todavía NO CONFIRMADA — Pack integral de Kilo

**Objetivo aspiracional:** instalar VX desde cero o incorporarlo a un perfil Kilo existente, con una experiencia todo-en-uno, respaldos verificables, manifiestos de componentes, catálogo de MCP y actualizaciones gobernadas.

| Capa | Incluye potencialmente | Límite |
| --- | --- | --- |
| Nativo Kilo | Agentes/modos built-in suministrados por Kilo | Preservar; VX no los reinstala ni administra |
| Paquete VX base | Agentes VX Markdown, skills VX, reglas/commands VX, CLI, registro, políticas, documentación | Versiones y cambios gobernados solo de componentes VX |
| Catálogo de MCP | Nombre/capacidades/versión compatible, procedencia, dependencias, comandos y permisos requeridos | MCP externos son integraciones opcionales, no componentes VX administrados; no conectar, actualizar ni descargar sin consentimiento |
| Configuración global | Marcadores y rutas de instalación VX, sin secretos | No reescribir completamente `kilo.jsonc`, modelos, providers, permisos ni AutoApprove |
| Datos operativos | Base SQLite y respaldos locales VX | Nunca migrar/borrar/recrear sin plan y autorización de la operación |

**Diferencia conceptual:** los agentes nativos (built-in) pertenecen a Kilo; los agentes VX son custom agents hechos con los formatos nativos de Kilo. Una skill no equivale a un servidor MCP: skill es una instrucción; MCP expone herramientas/servicios que pueden requerir ejecutables, cuentas o autenticación.

## 3. Flujo propuesto para instalación: puertas obligatorias

0. **Preflight solo lectura:** detectar versión de Kilo y plataforma Desktop/VS Code, ubicación de configuración global, existencia de componentes, compatibilidad, permisos y dependencias. No asumir que `configurado` equivale a `conectado`.
1. **Backup ANTES de cualquier modificación:** inventariar e incluir las rutas y configuraciones efectivamente afectadas, agentes y skills existentes, ficheros de configuración, definiciones MCP y estado del registro; respetar archivos/secretos sensibles y almacenar backup fuera de repositorio protegido con ACL/cifrado según se decida. Recibo con hashes, propietario y verificación de restauración en HOME sintético. La copia existente del instalador V4 solo respalda destinos gestionados, **no es una imagen completa del perfil**.
2. **Seleccionar estrategia:** bootstrap nuevo o adopción de perfil con preservación por defecto. "Limpia" no significa borrar la instalación anterior, eliminar agentes nativos o destruir integraciones externas.
3. **Comparación/dry-run:** pack vs inventario; clasificar `PRESENTE_COMPATIBLE`, `AUSENTE`, `DIFERENTE`, `NO_VERIFICADO`, `REQUIERE_LOGIN`, `INCOMPATIBLE`; colisiones, reparse points y procedencia; generar diff exacto vinculado a hash.
4. **Aprobación explícita acotada:** diferenciar instalar pack VX, preparar una integración MCP opcional, cambiar configuración global y reemplazar un componente. Nunca consentimiento genérico para todo. Sin mecanismo de autenticación y rollback V4.7 completo, solo diseño.
5. **Instalación futura y comprobación:** staging + escrituras mínimas de VX + verificación de hash + comprobar que Kilo descubre los componentes, y que MCP conectan con pruebas no destructivas y sin exponer secretos; fallos de red/sign-in deben quedar `PENDIENTE`, no `PASS`.
6. **Rollback/versionado:** manifiesto de versión del pack + versiones individuales/pines; migraciones reversibles, registro de hashes antes/después; recuperación segura y sin eliminar cambios posteriores de usuario.
7. **Actualizaciones posteriores:** solo componentes VX propios, cambios candidatos comprobados, aprobación independiente y opción de revertir. No actualización silenciosa de terceros, modelos ni MCP.

## 4. Decisiones abiertas para el operador antes de implementar bootstrap

1. **Perfil existente:** ¿convive VX con agentes/skills actuales (recomendado) o se desea perfil Kilo alternativo, limpio y aislado? Desactivar/eliminar componentes ajenos entra en conflicto con VX-D14 y exigiría política excepcional.
2. **Qué significa "nativos":** ¿mantener los built-in de Kilo y añadir agentes VX definidos en Markdown nativo, o reemplazar el conjunto visible por solo built-in + VX? Lo segundo implica intervención sobre componentes ajenos que aún no está autorizada.
3. **MCP del pack:** ¿catálogo `core` mínimo y extensiones opcionales por perfil, o un conjunto obligatorio? ¿Se permite preparar instaladores de terceros *solo tras aprobación específica* y sin credenciales, o únicamente mostrar instrucciones? Servidores que requieren login quedan pendientes hasta que el operador se autentique.
4. **Protección de respaldo:** alcance de credenciales/configuración, cifrado/ACL, ruta local, retención y procedimiento ante backup parcial/insuficiente.
5. **Actualizaciones:** ¿solicitar siempre confirmación del plan concreto (recomendado) o permitir solo comprobaciones automáticas de disponibilidad sin aplicar? Scheduler actual permanece OFF.
6. **Distribución y compatibilidad:** un pack zip/snapshot descargable + instalador PowerShell 7, o también paquete Marketplace/CLI; versiones de Windows/Kilo soportadas y migración desde instalaciones anteriores. Las pruebas se realizarán primero en HOME aislado.

## 5. Compatibilidad técnica y deuda identificada

- El repositorio actual ya contiene instalador con `Diagnostico`, `Simular`, `Aplicar`, `Verificar`, `Restaurar`; conserva `kilo.jsonc` y credenciales; solo protege/respaldaba destinos administrados. **No implementar "backup total" asumiendo que ya existe**.
- El catálogo MCP no está implementado en el instalador; `commands/vx-mcp.md` solo audita y propone. Los MCP ya configurados pueden necesitar login, procesos locales, red o herramientas de pago: comparar nombres no demuestra conectividad.
- Kilo soporta agentes built-in y agentes personalizados Markdown/JSONC; las configuraciones pueden combinarse por precedencia. Las skills se descubren en rutas globales y de compatibilidad; no duplicar nombres sin evaluación de precedencia.
- V4.7.0 es DRY_RUN. V4.7.1 solo emite coincidencias estructurales `AUTH_UNVERIFIED`; `approval_granted=false`, `apply_supported=false`. La instalación integral es **diseño**, no una función habilitada.
- No almacenar credenciales en GitHub, backups sin protección, informes ni logs; nunca pedir contraseña/token en un informe de evaluación o incluirlo en manifiestos.

## 6. Puerta de avance

Hasta que las decisiones abiertas queden registradas: **no cambiar instalador, MCP, agentes nativos, agentes ajenos, skills ajenas, configuración global o archivos en HOME.** La rama documental no debe tocar V4.7.2 que ya desarrolla otro agente. La nueva iniciativa de bootstrap debería llevar su propia épica/etapa luego de V4.7 y después de pruebas reversibles.

Referencias: [decisiones](VX-EVOLUTION-DECISIONES.md), [roadmap](VX-EVOLUTION-ROADMAP.md), [instalador](../scripts/Instalar-Kilo-Global-Harness.ps1), [MCP audit](../commands/vx-mcp.md), [Kilo Custom Modes](https://kilo.ai/docs/customize/custom-modes), [Kilo Skills](https://kilo.ai/docs/customize/skills), [Kilo MCP](https://kilo.ai/docs/automate/mcp/using-in-kilo-code).
