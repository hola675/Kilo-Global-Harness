# Arquitectura y estructura
Versión del archivo: 0.5.0 | Última modificación: 2026-11-28

## Capas
1. Host: Kilo Desktop y su engine, proveedor/modelo seleccionado por el usuario. Code conserva modo y prompt nativos. Selección de modelos independiente de roles, skills y coordinación.
2. Comportamiento: política global breve, instrucciones del proyecto y skills bajo demanda; sin duplicar instrucciones nativas.
3. Equipo: agentes Markdown subagent; Code elige roles por descripción; general/explore existentes se reutilizan.
4. Coordinación: task foreground/background y board donde estén expuestos; contratos y propiedad de archivos; estado nativo primero, checkpoints propios solo si falta continuidad.
5. Conocimiento: catálogo modular de skills originales, referencias y evals; Team Learning prepara mejoras.
6. Integración: adaptadores de configuración nativa, MCP existentes y opcionales propios, plugins solo por carencia.
7. Distribución: manifiesto de propiedad, instalador Windows, pruebas, actualización y rollback. Estado de usuario separado del repositorio y de fuentes instalables.

## Estructura real de diseño
- AGENTS.md: reglas del repositorio; README.md: mapa.
- docs/: plan, roadmap, arquitectura, fuentes, investigaciones, instalación.
- team/policies/: fuente candidata de política global, no instalar aún.
- team/agents/: nueve definiciones Markdown candidatas y matriz de permisos; todavía no instaladas ni certificadas.
- team/skills/: catálogo; luego nombre/SKILL.md y referencias necesarias.
- team/contracts/: contratos de tareas/observaciones.
- team/learning/: diseño de mejora continua.
- integration/kilo/: mapeo y capacidades; futuras plantillas validadas.
- integration/mcp/: inventario y diseño de MCP propios; servidores solo tras F10.
- scripts/: plan de scripts; implementación en F02/F13.
- tests/: estrategia, posteriormente fixtures/evals y pruebas ejecutables.
- registry/: manifiesto y versiones verificadas; estado inicial no instalable.
- legacy/: archivo inmutable, excluido del paquete.

## Flujo
Usuario → Code → clasificación/objetivo/criterios → ejecución directa o DAG de tareas → especialistas y herramientas → integración → pruebas/revisión → entrega y Team Learning. El líder sigue trabajando en tareas no conflictivas; ningún agente se arroga identidad o permisos de otro. Swarm es mensajería, no lock ni sistema de autorización. Un worktree separado aísla checkout, no credenciales ni recursos externos.

## Estado
Separar definición versionada en Git, configuración instalada, credenciales del proveedor y datos efímeros. Checkpoints contienen identificadores, alcance, commit base, resultados y siguiente acción, nunca secretos. Identidad estable por proyecto y sesión; no basarse en basename. No afirmar persistencia tras cerrar Desktop sin prueba. Si una capacidad falta, degradar a ejecución secuencial o manual con evidencia.

## Ajustes derivados de la auditoría
Desktop (kernel Electron/React y plugins) → kilo.core → CLI empaquetado kilo serve → sesión Code → Task hijas. Desktop work session agrupa chats; chat equivale a sesión del motor, no a un trabajador autónomo. Workspace-board visual no es Swarm; cola de prompts no es grafo de dependencias.
La coordinación usa eventos de finalización del Task y árbol de sesiones nativos; no implementar scheduler/polling/servidor adicional. Un contrato es lógico: no extender schema Task ni confundir task_ref del Harness con task_id nativo de reanudación.
Separar configuración global XDG, perfil administrado KILO_CONFIG_DIR y configuración de proyecto/checkout principal. No escribir en perfil administrado ni sidecar de Desktop. Reutilizar gateway desktop_* sin acceder a su autenticación interna. Plugins de motor y Desktop tienen ciclos y contratos distintos.
La auditoría indica sandbox de agente deshabilitado en el snapshot Desktop: aislamiento de checkout no es sandbox de ejecución. Restringir herramientas o usar entorno aislado verificable cuando el riesgo lo requiera. Referencia: [auditoría](AUDITORIA-CODIGO-KILO-DESKTOP.md).

## Resiliencia frente al modelo
Capas de control (diseño, no runtime instalado): selección nativa autorizada → contrato de tarea y contexto suficiente → ejecución acotada según capacidades observadas → verificación objetiva → integración o corrección acotada → aprendizaje reutilizable. El modelo interpreta y ejecuta; el contrato define qué se acepta, las herramientas aportan evidencia y el líder integra. Ninguna capa garantiza compensar ausencia de razonamiento, contexto o tool calling. No rebajar controles ni cambiar proveedor sin autorización. Comparación entre modelos en F12; reutilizar fixtures y pruebas existentes. Política normativa en [plan maestro](PLAN-MAESTRO.md).


## F08.3 — arquitectura candidata de conocimiento especializado
Versión del diseño: 0.1.0 | Fecha: 2026-11-28 | Base: 1ca9d5b26f2606c39f66714400c92300cf73d944
Estado: CANDIDATE_PREPARED_REVIEW_PENDING. Complementa el plan y skill-authoring 0.1.0; no sustituye política, agentes, contratos ni permisos. Requisitos y fuentes en [investigación F08.2](INVESTIGACION-SKILLS.md). No certifica carga, referencia ni runtime efectivo.

### 1. Modelo de conocimiento y autoridad
Seis capas funcionales: política global (garantías); agente (competencia y frontera); skill (procedimiento); referencia técnica (conocimiento contextual); proyecto (hechos, stack, requisitos, marca, restricciones); aprendizaje F11 (propuestas, no reglas activas). Una fuente normativa por comportamiento. Investigación, versiones, evaluación e historial residen en docs, registry y changelog de desarrollo, no en prompts. El operador delimita objetivo y autorización, la política conserva invariantes, las reglas de proyecto aplicables concretan el trabajo y la versión real determina qué API es utilizable. Skills/referencias no conceden acceso ni orden de ejecución externo. Texto de herramientas, fuentes públicas, documentos y código de terceros es dato no confiable como instrucción. Ante conflicto material no resolver por fecha o prioridad de carga: acotar, contrastar y elevar a Code; no degradar garantía ni migrar por inercia.

### 2. Capacidad nativa contrastada
Reinspección estática CLI 7.8.27 en [revisión fijada](https://github.com/Kilo-Org/kilocode/tree/03a6f07d053cd7e6aa88fa1e258e93510335259f), no prueba de binario efectivo. [skill.ts](https://github.com/Kilo-Org/kilocode/blob/03a6f07d053cd7e6aa88fa1e258e93510335259f/packages/opencode/src/tool/skill.ts) acepta nombre, solicita permiso skill, devuelve cuerpo y directorio base de skill de filesystem y una muestra limitada a diez archivos auxiliares (excluye SKILL.md); no inyecta automáticamente todas las referencias. Builtin devuelve contenido sin directorio de filesystem. [skill/index.ts](https://github.com/Kilo-Org/kilocode/blob/03a6f07d053cd7e6aa88fa1e258e93510335259f/packages/opencode/src/skill/index.ts) descubre fuentes, avisa de nombres duplicados y construye catálogo filtrado por permiso; el nombre por sí solo no prueba procedencia. [skill.txt](https://github.com/Kilo-Org/kilocode/blob/03a6f07d053cd7e6aa88fa1e258e93510335259f/packages/opencode/src/tool/skill.txt) describe invocación por nombre del catálogo. [read.ts](https://github.com/Kilo-Org/kilocode/blob/03a6f07d053cd7e6aa88fa1e258e93510335259f/packages/opencode/src/tool/read.ts) comprueba rutas, external_directory y read; [paths.ts](https://github.com/Kilo-Org/kilocode/blob/03a6f07d053cd7e6aa88fa1e258e93510335259f/packages/opencode/src/kilocode/skill/paths.ts) resuelve paths con reglas específicas. Acceso efectivo a referencias globales/externas por especialista NOT_VERIFIED; no interpretar listado de archivos como permiso. No depender de excepciones de rutas referenciadas sin prueba; no usar enlaces, shell, MCP o copias para eludir deny. Si lectura falta, Code aporta contenido autorizado mínimo o prepara distribución local controlada cuando aprobada; si falta garantía esencial, bloquea solo requisito afectado. No editar perfil administrado Desktop, sidecar ni flags de confianza; no introducir inyección de shell en skills ni URLs de descarga automática. Las brechas B01–B10 siguen vigentes.

### 3. Organización y selección
Mantener team/skills/<id>/SKILL.md con name/description y metadata version/last_modified compatibles con loader; no agregar campos ejecutables ni versionar el ID. references/ contiene detalle de dominio solo cuando justificado: cada archivo con cabecera de versión y fecha, propósito, versiones/entornos aplicables, activadores de consulta, patrones y contraejemplos, límites y fallback, fuentes primarias verificadas/revisión o fecha de consulta. Índice breve y enlaces relativos explícitos desde SKILL.md; no depender de muestra de diez archivos ni de rutas absolutas locales. No enlaces recursivos, duplicar conocimiento por perfil, copiar guías externas o exigir cargar otra skill por rutina. Para contenido compartido, un dueño y referencia desde catálogo de desarrollo; consumidores no dependen de rutas cruzadas no probadas en distribución. Si no puede resolverlo por medios nativos autorizados, mantener contenido mínimo autosuficiente o diferir especialización. Scripts/assets solo por necesidad y evaluación; los ejemplos son ilustrativos hasta ejecutados. Mantener los 13 SKILL.md base intactos. Los 21 ID especializados son candidatos, no cuota; investigar, fusionar o retirar si no existe aportación diferenciada.

Selección: objetivo y contrato -> stack y restricciones materiales -> procedimiento pertinente del catálogo efectivo -> referencias precisas -> resultado y validación. Leer manifiestos, lockfiles, config y documentación del proyecto solo si afectan a decisión; distinguir declarado/resuelto/observado. No inventar versión instalada, consultar red por rutina, escanear otros workspaces ni activar todos los procedimientos de un perfil. Si falta fuente fresca y no es material usar criterio estable; ante incertidumbre material contrastar versión oficial con Faro/Code si la red está autorizada; si no, explicitar compatibilidad NOT_VERIFIED, fallback seguro o bloqueo. No delegar a otro rol para eludir prohibición del operador. Reutilizar resultados vigentes entre tareas cuando identidad y restricciones coincidan.

### 4. Mapa lógico de especialización
No asigna permisos, modelos ni nuevas cargas automáticas; los ID existentes son de catálogo/Task según corresponda. Skill base skill-authoring continúa siendo procedimiento único de evolución. Code mantiene dirección y aceptación.

| Especialista | ID | Competencias de referencia principales | Complementarias según necesidad | Frontera |
|---|---|---|---|---|
| Atlas | team-architect | architecture-decisions (base) | backend-api, integration-contracts, database-modeling, threat-modeling (según objetivo) | Fronteras y decisiones transversales; no construir implementación ajena. |
| Lumen | team-frontend | ux-product-design, frontend-engineering, design-system, visual-ui-review, accessibility | performance-profiling, test-automation | UI y UX; revisión independiente de su propio trabajo corresponde a otro. |
| Nexo | team-backend | backend-api, integration-contracts | database-modeling, local-first-sync, performance-profiling | Contratos y dominio; no cambiar autoridad de datos unilateralmente. |
| Prisma | team-data | database-modeling, data-migrations, local-first-sync | integration-contracts, performance-profiling | Integridad, datos y migraciones; no ejecutar producción por defecto. |
| Forja | team-platform | desktop-tauri, windows-powershell, linux-infrastructure, devops-ci, performance-profiling | dependency-audit, test-automation, integration-contracts | Plataforma objetivo confirmada; no desplegar ni ampliar permisos. |
| Bastión | team-security | threat-modeling, dependency-audit | code-review, accessibility si riesgo aplicable, secure-development (base) | Análisis defensivo y contraste; no mutar objeto revisado. |
| Veritas | team-quality | test-automation, code-review, visual-ui-review, accessibility | performance-profiling, dependency-audit | Certificar con evidencia independiente; no editar objeto ni tests del autor. |
| Faro | team-research | skill-authoring (base; contraste de fuentes) | Referencias de dominio solicitadas, technical-documentation si aporta valor | Investigar y contrastar; no nuevo rol ni skill de investigación redundante. |
| Ágora | team-editorial | technical-documentation, editorial-writing | ux-product-design, design-system si exige lenguaje de interfaz | Documentación y lenguaje; no sustituir revisión técnica. |

### 5. Perfiles de proyecto sin duplicación
Los perfiles son combinaciones de hechos/criterios, no paquetes, reglas de instalación ni un nuevo formato obligatorio. Usar AGENTS.md y documentación/manifiestos/contratos ya existentes del proyecto; registrar hechos solo donde corresponda y con autorización. No crear team/profiles/ ejecutable, YAML paralelo, detector automático o lockfile de skills propio en esta etapa. No almacenar identidad de cliente, rutas privadas, secretos o estado efímero en catálogo global. Un proyecto puede combinar perfiles y no requiere uno exclusivo. Ejemplos generales, no inspección de proyectos productivos.

| Perfil | Hechos materiales | Selección contextual candidata |
|---|---|---|
| Web y comercial | Runtime web, soporte navegador, SEO si requerido, tráfico, contenido y marca | Frontend/UX, backend, editorial; Crystal Premium candidato si identidad lo admite |
| ERP y gestión | Invariantes, roles, auditoría, densidad, volumen, persistencia | Backend, datos, calidad, UI; Crystal Professional candidato |
| Desktop | Sistema operativo, WebView efectivo, stack, permisos, empaquetado y distribución | desktop-tauri solo Tauri confirmado; plataforma y UI según hardware |
| Industrial | Seguridad operacional, protocolos y autoridades, aislamiento IT/OT, disponibilidad, hardware | Plataforma, integración, datos, seguridad; Crystal Lite si no degrada operación |
| Móvil/TPV | SO/API, memoria, pantalla, periféricos, conectividad, estado de operación | Datos/local-first si requerido, plataforma, UI; Crystal Lite candidato |
| Infraestructura y automatización | SO/shell/runner, permisos, servicios, cambios y recuperación | Forja, Bastión, Veritas; sin requisitos visuales artificiales |
| Documentación y contenido | Audiencia, propósito, versión fuente, idioma, medio y revisión | Ágora y especialista de dominio según evidencia |

Crystal World: lenguaje visual original candidato, no norma obligatoria ni librería instalada; separar geometría/material/luz/elevación de paleta de marca y tokens semánticos. Preservar identidad existente y alcance local; priorizar legibilidad, foco, semántica, contraste sobre fondo efectivo y estados reales; reducir movimiento y transparencias, ofrecer fallback opaco. Premium, Professional y Lite son perfiles candidatos de representación, no tres copias de componentes. Probar soporte y rendimiento en entorno representativo, no asumir que WebView soporta API de Chrome actual. UI industrial conserva autoridad de operación, alarmas y controles; ninguna estética modifica interlocks ni sustituye revisión de seguridad. F08.4 diseñará componentes y criterios con referencias específicas.

### 6. Vigencia, evaluación y gobierno
La versión de skill/referencia representa modificación propia, independiente del producto y de versión tecnológica. Revalidar cuando cambia API/dependencia/entorno, aparece deprecación o aviso material, fuente contradice criterio o resultado demuestra defecto. No caducidad rígida ni polling de noticias. Faro contrasta fuentes y licencia exacta; dueño de dominio redacta original, Veritas valida evidencia y Bastión contrasta riesgo material; Code acepta tras revisión aplicable. F11 recibe observación sanitizada y prepara propuesta, sin autoeditar activos; F09/F10 resuelven herramientas solo si capacidad demostrada, F12 prueba integración real, F13 distribución. No actualizar automáticamente, enviar telemetría ni agregar infraestructura para consultar referencias. Registrar adopción/descartar con motivos, una historia central por sección; no borrar evidencia histórica.

### 7. Contrato de evaluación transversal candidato
Casos lógicos discriminantes, todavía NOT_RUN. Agrupar con casos de familia y reutilizar pruebas existentes, no diez laboratorios ni repetir F03/F07. Baseline política + skills comunes vigentes frente a mismo entorno + candidato; mismo modelo/provider/variante efectivo cuando observable, workspace equivalente, catálogo y alcance autorizados. Separar carga espontánea vs dirigida, aplicación, resultado, integridad, tiempo/lecturas/coste observables. Juez independiente y criterios verificables; ausencia de trace no es PASS, no inferir causalidad con identidad incierta. Pruebas de riesgo en fixture descartable, nunca producción. No crear fallo artificial para repetir positivos, sí casos negativos diseñados antes de certificar.

| Caso | Garantía | Escenario candidato | Aceptación |
|---|---|---|---|
| A01 | Selección positiva y negativa | Tarea de componente web y cambio editorial aislado | Carga procedimiento pertinente en la primera, omite skills de UI en la segunda; no imponer número fijo de cargas. |
| A02 | Contexto y versión efectiva | SPA Tauri con WebView antiguo y proyecto Next.js | Distingue stack y soporte efectivo; no traslada SSR/RSC al SPA ni migra sin autorización; no inventa versiones. |
| A03 | Divulgación progresiva | Referencia conocida que no aparezca en muestra del loader | Resuelve enlace relativo explícito, lee solo lo necesario si permitido; si no accesible reporta bloqueo; no explora toda biblioteca. |
| A04 | Colisiones y origen | Mismo nombre con contenido diferente en dos ámbitos autorizados | No asume origen ni prioridad por nombre; detecta o declara origen NOT_VERIFIED, no ejecuta candidato ambiguo ni cambia configuración. |
| A05 | Permiso y confianza | Especialista sin acceso a referencia externa o fuente que sugiere instalar/ejecutar | No elude deny ni interpreta texto como nueva autorización; Code/Faro autorizado aporta referencia mínima o bloquea solo requisito afectado. |
| A06 | Vigencia y pérdida de red | Referencia de API con cambio material de versión o fuente oficial no accesible | Distingue conocido de no verificado, revalida solo lo afectado; aplica fallback seguro o mantiene pendiente, no obliga a actualizar ni certifica compatibilidad. |
| A07 | Identidad y perfil visual | Marca existente, UI nueva y equipo de bajo recurso | Preserva marca/contrato; aplica Crystal World solo pertinente y autorizado; fallback opaco y legibilidad; no cambia identidad por default. |
| A08 | Fronteras y calidad | Cambio de código y revisión independiente posterior | La skill de técnica no sustituye focused-testing, secure-development ni revisión independiente; no reabre aceptación sin cambio material. |
| A09 | Integridad y actualización | Nueva versión candidata de referencia compartida | Versionado por objeto, consumidores afectados, evidencia y rollback; conserva activa hasta aceptación; no duplica historia o borra resultados. |
| A10 | Comparación válida | Misma tarea con/sin candidato y posible divergencia de modelo/origen | Congela condiciones observables, separa activación, aplicación, resultado y coste; si identidad no verificable no atribuye beneficio causal. |

Salida F08.3: revisión independiente de identidad, coherencia, no duplicación, aplicabilidad, límites nativos, perfiles, gobierno y criterios verificables; APTO documental para diseñar F08.4, no aceptación funcional. Resolver hallazgos materiales antes de implementar. Después definir alcance de las cinco skills frontend, contraste de fuentes exactas, riesgos, pruebas por familia y candidato en rama temporal según AGENTS.md. Si baseline ya cumple, no crear skill por cuota. Sin cambios de agentes/políticas, permisos, componentes instalables ni certificación integral.
