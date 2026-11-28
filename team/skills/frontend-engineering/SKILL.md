---
name: frontend-engineering
description: "Construye, refactoriza y optimiza interfaces web o WebView en su stack real: HTML semántico, CSS moderno compatible, componentes, estado, contratos de datos, TypeScript cuando aplique, assets y rendimiento. Usar al implementar cambios materiales de frontend o corregir compatibilidad. No cargar para diseño conceptual sin código, edición textual, backend aislado o migraciones de stack no autorizadas."
metadata:
  version: "0.1.0"
  last_modified: "2026-11-28"
---

# Ingeniería frontend moderna, compatible y expresiva

## Alcance
Lumen implementa interfaz funcional dentro del alcance; no sustituye requisitos, contrato de dominio, política de seguridad, diseño visual aprobado ni revisión independiente. Utiliza el sistema visual existente; en UI nueva con libertad estética, la dirección preferida es Crystal World expresivo cuando pertinente. No rediseñar marca por una corrección local. No imponer React, Next.js, Tailwind, Tauri ni herramientas nuevas.

## 1. Determinar plataforma y fronteras
- Leer manifiestos, lockfiles, versiones declaradas/resueltas y configuración pertinente, soporte objetivo de navegador/WebView, SSR/SPA/estático, contratos de UI y datos. Distinguir declaración de versión instalada y capacidad observada. Si el soporte de una API importa y no está probado, consultar fuentes autorizadas o elegir alternativa conservadora; no inferir por nombre del framework.
- Para API, estado y componente consultar [plataforma y componentes](references/platform-and-components.md) cuando la decisión lo requiera. Priorizar semántica y capacidades nativas compatibles; usar primitives/librerías existentes cuando cubran comportamiento, accesibilidad o compatibilidad que no conviene reconstruir. No introducir paquetes, migrar dependencias o cambiar herramienta de build sin brecha, comparación y autorización.
- Localizar componentes, tokens, estilos y assets canónicos antes de crear otros. Para cambio de sistema visual, design-system aporta procedimiento propio si disponible; no encadenar cargas por rutina. No inventar ruta, asset, fuente, endpoint ni resultado.

## 2. Construir comportamiento y componentes
- Componer por responsabilidad y contrato; mantener API pública pequeña y separar estado de interacción, datos remotos y estado derivado cuando tengan ciclos distintos. No copiar estado derivable ni introducir stores, effects, memoización o componentes genéricos sin necesidad. Validar entradas externas en frontera; tipado estático no acredita validación runtime.
- Respetar autoridad de servidor/núcleo: ocultar botón no concede ni revoca permiso. Contemplar carga, vacío, error, éxito, desconexión, conflicto y datos antiguos según contrato. Proteger carreras y respuestas obsoletas; no simular éxito, reintentar efectos inciertos ni inventar idempotencia. Cancelar observación de solicitud no cancela necesariamente operación remota. Mantener entradas útiles cuando seguro.
- Usar HTML nativo apropiado, nombres accesibles, teclado y foco; para widgets complejos respetar patrón comprobado y alternativas. Preferir layout flexible y componentes que respondan al espacio real; probar zoom, contenido largo, orientación y densidad pertinente. No asumir que una captura verifica interacción.

## 3. Implementar presentación profesional
- Construir con tokens semánticos, estados y materiales del sistema aprobado. En creación visual autorizada, combinar color vivo, acentos luminosos, tipografía con carácter y profundidad intencional; no reducir todo a gris, ni saturar cada superficie. Asegurar jerarquía, legibilidad y contraste sobre fondo compuesto; nunca depender solo de color o brillo para estado.
- CSS moderno (grid/flex, consultas de contenedor, variables, color perceptual, filtros y capas) solo donde soporte y coste lo permitan. Definir fallback sRGB/opaco y alternativa funcional antes de mejoras; detectar capacidad no equivale a certificar comportamiento. Mantener la misma semántica y acción con efectos desactivados.
- Integrar assets con licencia/procedencia y dimensiones pertinentes: usar SVG para geometría cuando idóneo, variantes raster responsivas y formatos soportados; reservar espacio, texto alternativo según función, fuentes locales o aprobadas con fallback y carga proporcionada. No descargar, publicar ni incorporar recursos sin derechos comprobados. No ocultar información tras animaciones o assets; respetar movimiento reducido y restricciones de conectividad.

## 4. Optimizar y verificar el delta
- Priorizar defectos funcionales y de seguridad, solicitudes independientes serializadas sin necesidad, peso de recursos y trabajo de render repetido antes de microoptimizaciones. Paralelizar solo operaciones realmente independientes y con límites; no cambiar orden de efectos. Medir cuello de botella antes/después si material; no imponer virtualización, lazy loading, memo ni splitting por rutina. En web distinguir datos de campo y laboratorio, en WebView medir dispositivo objetivo cuando posible.
- Usar runner, tipos, lint y build existentes; probar interacción y estados afectados en navegador/plataforma autorizados. Verificar soporte, fallback, teclado, contraste, assets y regresiones según riesgo; si falta medio, informar NOT_RUN/BLOCKED/NOT_VERIFIED según corresponda. No instalar navegador/runner ni conceder permisos para lograr evidencia.
- Entregar incremento funcional, archivos/contratos afectados, decisiones y alternativas, versiones/soporte, resultados observables, limitaciones y siguiente acción. Una revisión propia no es independiente; Code integra con evidencia y preserva B01–B10. No certificar rendimiento ni compatibilidad por código estático.
