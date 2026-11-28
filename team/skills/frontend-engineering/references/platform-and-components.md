# Plataforma, componentes y rendimiento
Versión del archivo: 0.1.0 | Última modificación: 2026-11-28

Referencia contextual de frontend-engineering. No es lista de migraciones ni versiones obligatorias. Consultar documentación oficial de versión efectiva si una diferencia es material; distinguir entorno declarado, resuelto y observado.

| Necesidad | Primera opción a evaluar | Límite / alternativa |
|---|---|---|
| Diálogo modal | HTML dialog y showModal cuando soportado; controlar foco y cierre | Verificar comportamiento real y patrón accesible; reutilizar primitive compatible si no basta. Popover no es modal por defecto. |
| Layout | Flexbox/Grid, tamaños intrínsecos; consultas de contenedor cuando soportadas | Fallback de layout usable; no romper reflow ni ocultar información. |
| Anclajes/overlays | Popover/anchor positioning según soporte y semántica | Alternativa posicionada compatible; comprobar colisiones y teclado; no asumir soporte por Baseline. |
| Color y material | Variables y valores sRGB base; OKLCH/color-mix cuando soporte confirmado | @supports sobre valor/propiedad pertinentes, evitar custom property inválida que sustituya fallback; contraste y gamut efectivo, alternativa opaca sin blur. |
| Imágenes | SVG para formas, srcset/sizes o picture para raster cuando procede | Reserva dimensiones; no cargar diferido el contenido crítico indiscriminadamente; fallback de formato y licencia. |
| Tipografía | Familia aprobada, fallback, pesos necesarios y font-display apropiado | Verificar acentos, números, métricas y estabilidad de layout; no imponer fuentes externas ni variable font a runtime incompatible. |
| Interacción | Semántica nativa, acciones/eventos explícitos | No reimplementar widgets complejos sin necesidad; verificar entrada, teclado, foco y lectura. |

## Adaptación por stack
- JavaScript/TypeScript: usar semántica de plataforma; modelar estados excluyentes (uniones discriminadas si TS) y comprobar datos externos antes de confiar en tipos. No silenciar error con any/as indiscriminado ni convertir proyecto JS en TS sin alcance.
- React: derivar valores durante render cuando suficiente; effects para sincronización con sistemas externos, con dependencias/cleanup correctos; lógica de evento en handler cuando corresponde. Separar estado local y remoto por ciclo, no copiar props a estado por rutina. Memoización únicamente con necesidad; preservar identidad y claves estables según dominio.
- Next.js/SSR/RSC: solo en proyecto que realmente los use, verificar versión, frontera servidor/cliente, caché y datos por usuario, hidratación y autoridad de operaciones. No trasladar APIs de servidor, RSC o next/dynamic a SPA Tauri/Vite ni a otro framework.
- Vue/Svelte/Angular u otros: conservar sus modelos de reactividad, lifecycle y tooling vigentes; consultar fuente oficial aplicable en vez de traducir hooks React literalmente. No se declaran versiones verificadas de esos stacks en esta referencia.
- Tauri/WebView: comprobar motor y versión de plataforma efectiva, capacidades IPC y contrato de comandos; no exponer secretos ni conceder permisos desde frontend. Compatibilidad de navegadores centrales no demuestra soporte de WebView antiguo. Usar fallback funcional o bloquear requisito si no disponible.

## Optimización con evidencia
Secuencia: criterio funcional y de seguridad -> diagnóstico de red, carga, render o dispositivo -> cambio mínimo -> medición comparable -> regresiones. No prometer umbrales universales; LCP/INP/CLS orientan experiencia web, no sustituyen métricas de operación local, memoria, arranque o latencia de hardware. Mantener presupuesto del proyecto. No instalar herramientas por conveniencia; si no hay perfilador, declarar límite y priorizar corrección comprobable.

## Fuentes de criterio
Consulta 2026-11-28: [Baseline](https://web.dev/baseline), [MDN OKLCH](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/oklch), [color-mix](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/color-mix), [@supports](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@supports), [backdrop-filter](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter), [React: Effects](https://react.dev/learn/you-might-not-need-an-effect), [TypeScript: narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html), [Web Vitals](https://web.dev/articles/vitals), [imágenes responsivas](https://web.dev/learn/images/responsive-images), [font-display](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@font-face/font-display). Contraste de skills fijadas: [Vercel](https://github.com/vercel-labs/agent-skills/blob/5a37a6329fbad3666c3207392a6a7c0110e92efb/skills/react-best-practices/SKILL.md), [Addy Osmani](https://github.com/addyosmani/agent-skills/blob/e997ac5b9a74eab332d5e9793bb38a38c8cfdd74/skills/frontend-ui-engineering/SKILL.md). Síntesis original; no copiar ejemplos ni instalar dependencias. Soporte real y rendimiento NOT_VERIFIED hasta prueba.
