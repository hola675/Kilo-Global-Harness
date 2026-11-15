# VX Evolution — Alcance C y diseño preliminar del Pack inicial (2026-11-15)

**Estado:** `VX-D14` alcance C, `VX-D16` instalación limpia y `VX-D17` preservación de MCP CONFIRMADAS. Otras decisiones del pack siguen pendientes. **Solo documentación; ningún cambio en Kilo, permisos, HOME, instalador, MCP, SQLite, scheduler o runtime.**

## 1. Decisión confirmada VX-D14 — Alcance C

**VX Evolution limita su evaluación, administración, formación, versionado, publicación y mejora a componentes propios VX, identificados mediante un registro de propiedad y procedencia.** La detección de componentes externos para *inventario inicial, compatibilidad, respaldo y diagnóstico de la instalación* no los incorpora a la gobernanza continua. Ningún agente, skill, MCP, regla o configuración ajena se elimina, reemplaza, deshabilita, actualiza o reconfigura por decisión autónoma de VX. El operador podrá autorizar una migración de entorno concreta más adelante, pero esa operación es distinta de la gestión continua VX.

La marca de nombre `vx-*` es una pista, no prueba suficiente de propiedad: se necesita manifiesto del pack, fuente reconocida, versión/hash y validación de procedencia.

## 1.1. Decisión confirmada VX-D16 — Instalación objetivo limpia

**El operador eligió explícitamente un entorno Kilo limpio con solo los agentes nativos de Kilo y el Pack VX.** Se aplica al perfil GLOBAL de Kilo en una PC Windows; no autoriza editar repositorios de proyectos.

**Estado objetivo:**
- **Preservar los agentes/modos nativos** suministrados por la instalación de Kilo. VX no copia, desinstala ni suplanta componentes nativos.
- **Instalar y mantener únicamente componentes personalizados VX propios**: agentes `vx-*` declarados y comprobados por manifiesto, skills VX, comandos y reglas administradas por el pack.
- **Los componentes personalizados previos de otros autores no permanecen activos** al terminar la migración limpia. Se archivan fuera de rutas descubiertas por Kilo en un backup reversible antes de desactivarlos/retirarlos; nunca destruirlos silenciosamente.
- **Los agentes personalizados inline en `kilo.jsonc` también requieren un plan específico** para desactivar solo sus declaraciones, preservando comentarios, orden cuando sea posible, modelos, proveedores, permisos ajenos al alcance, tokens y MCP. No reescribir el archivo entero a ciegas; validar compatibilidad y precedencia antes de cualquier cambio.
- **Skills externas en rutas globales/compatibles** (`.kilo/skills`, `.agents/skills`, `.kilocode/skills`) se inventarían, respaldan y se retiran de descubrimiento solo en una migración autorizada. No tocar skills locales de proyectos fuera del perfil global.
- **MCP e integraciones constituyen una capa distinta**: la política VX-D17 confirma conservar todos los servidores MCP existentes (incluida su configuración y estado) y proponer individualmente los faltantes del catálogo VX. No desinstalar, modificar, reautenticar ni reemplazar MCP existentes por efecto de una migración limpia de agentes/skills.
- **Si no es posible demostrar integridad y reversibilidad de una operación, fallar cerrado** y mantener el perfil actual sin cambios. En modo preparación se utilizan fixtures HOME o perfil alternativo, no rutas reales.

**Límite de consentimiento:** la selección de este estado final **no autoriza aún** modificar el perfil activo, mover/renombrar/borrar archivos ajenos, escribir `kilo.jsonc`, instalar MCP, realizar login o activar schedulers. Para una migración real habrá autorización posterior sobre un inventario completo, lista exacta de desactivaciones, backup verificado y capacidad de rollback ensayada. La excepción de migración inicial no amplía el alcance permanente de administración VX-D14.


## 1.2. Decisión confirmada VX-D17 — MCP existentes preservados y faltantes por aprobación individual

El operador eligió **conservar los MCP existentes y añadir únicamente los faltantes del Pack VX con aprobación individual**.

- La migración limpia VX-D16 afecta a agentes y skills personalizados, **no** a las definiciones, credenciales ni conexiones MCP existentes. No desactivar, borrar, mover, sustituir, actualizar ni reautenticar automáticamente MCP existentes.
- Inventariar en modo lectura los MCP globales configurados y, cuando pueda comprobarse sin exponer secretos, su estado. La comparación con el catálogo VX debe contemplar identidad/proveedor, versión y compatibilidad cuando haya evidencia, no basarse exclusivamente en nombres iguales.
- Informar `YA_CONFIGURADO`, `FALTANTE`, `REQUIERE_LOGIN`, `INCOMPATIBLE` o `NO_VERIFICADO` con evidencia. No confundir presencia en JSONC con conexión real.
- Por cada MCP del pack ausente, generar **una propuesta individual** con origen/licencia, permisos, dependencia ejecutable, cambios exactos, compatibilidad, riesgo, posibles costes y procedimiento de reversión. Sin consentimiento individual **no** descargar paquetes, ejecutar scripts, modificar `kilo.jsonc`, habilitar procesos, solicitar credenciales ni conectar servidores.
- Una integración MCP externa no pasa a ser un componente administrado por VX: solo el catálogo/recomendación VX pertenece al pack. La configuración y actualizaciones del servidor externo se rigen por permisos específicos del usuario.
- **No hay autorización de ejecución ni de instalación MCP en esta decisión.** La composición concreta del catálogo y la selección de MCP obligatorios/opcionales siguen pendientes.

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
2. **Seleccionar estrategia:** el estado objetivo confirmado es un perfil global limpio: built-in Kilo + personalizaciones VX exclusivamente. La transición desde perfil existente se realizará con inventario y backup completo verificable; los archivos personalizados ajenos pasan a archivo recuperable fuera de rutas Kilo, no a eliminación irreversible. Los MCP actuales se conservan por VX-D17. Los faltantes del catálogo se proponen con aprobación individual; no se instalan automáticamente.
3. **Comparación/dry-run:** pack vs inventario; clasificar `PRESENTE_COMPATIBLE`, `AUSENTE`, `DIFERENTE`, `NO_VERIFICADO`, `REQUIERE_LOGIN`, `INCOMPATIBLE`; colisiones, reparse points y procedencia; generar diff exacto vinculado a hash.
4. **Aprobación explícita acotada:** diferenciar instalar pack VX, preparar una integración MCP opcional, cambiar configuración global y reemplazar un componente. Nunca consentimiento genérico para todo. Sin mecanismo de autenticación y rollback V4.7 completo, solo diseño.
5. **Instalación futura y comprobación:** staging + escrituras mínimas de VX + verificación de hash + comprobar que Kilo descubre los componentes, y que MCP conectan con pruebas no destructivas y sin exponer secretos; fallos de red/sign-in deben quedar `PENDIENTE`, no `PASS`.
6. **Rollback/versionado:** manifiesto de versión del pack + versiones individuales/pines; migraciones reversibles, registro de hashes antes/después; recuperación segura y sin eliminar cambios posteriores de usuario.
7. **Actualizaciones posteriores:** solo componentes VX propios, cambios candidatos comprobados, aprobación independiente y opción de revertir. No actualización silenciosa de terceros, modelos ni MCP.

## 4. Decisiones abiertas para el operador antes de implementar bootstrap

1. **CERRADA — Destino de perfil limpio (VX-D16):** built-in Kilo + Pack VX; agentes/skills personalizados ajenos no activos al terminar. La ejecución sobre el perfil real sigue pendiente de backup validado, simulación y autorización concreta. No confundir decisión de destino con permiso para retirar archivos ahora.
2. **CERRADA — Nativos y personalizados:** conservar los built-in distribuidos por Kilo, añadir agentes VX propios escritos en formatos soportados por Kilo. Los personalizados existentes ajenos a VX se archivan/desactivan al migrar mediante autorización posterior; no se eliminan los nativos.
3. **POLÍTICA CONFIRMADA VX-D17:** conservar todos los MCP existentes y presentar los faltantes del catálogo VX para aprobación individual. **PENDIENTE SOLO EL DISEÑO DEL CATÁLOGO:** composición mínima y perfiles, método de instalación de cada MCP y cómo gestionar `REQUIERE_LOGIN` sin credenciales almacenadas. No instalar ni conectar automáticamente.
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

Hasta que las decisiones abiertas queden registradas, se pruebe la recuperación y se autorice una migración concreta: **no cambiar instalador, MCP, agentes nativos, agentes ajenos, skills ajenas, configuración global o archivos en HOME.** La decisión VX-D17 tampoco autoriza instalar una integración faltante. La rama documental no debe tocar V4.7.2 que ya desarrolla otro agente. La nueva iniciativa de bootstrap debería llevar su propia épica/etapa luego de V4.7 y después de pruebas reversibles.

Referencias: [decisiones](VX-EVOLUTION-DECISIONES.md), [roadmap](VX-EVOLUTION-ROADMAP.md), [instalador](../scripts/Instalar-Kilo-Global-Harness.ps1), [MCP audit](../commands/vx-mcp.md), [Kilo Custom Modes](https://kilo.ai/docs/customize/custom-modes), [Kilo Skills](https://kilo.ai/docs/customize/skills), [Kilo MCP](https://kilo.ai/docs/automate/mcp/using-in-kilo-code).
