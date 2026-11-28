---
name: design-system
description: "Define o evoluciona sistemas visuales, tokens, familias de componentes, identidad de marca y dirección artística: color, tipografía, assets, materiales, iluminación, profundidad, estados y variantes Crystal World cuando pertinente. Usar para interfaces nuevas o cambios materiales de lenguaje visual compartido. No cargar para ajustar un margen aislado, cambiar texto sin impacto visual o imponer una marca/estética sobre un sistema vigente fuera de alcance."
metadata:
  version: "0.1.0"
  last_modified: "2026-11-28"
---

# Sistemas visuales con identidad: Crystal World

## Alcance
Lumen diseña lenguaje visual reusable, no sustituye flujo UX, contrato funcional, accesibilidad, implementación ni revisión independiente. Preservar marca y alcance. En producto nuevo o rediseño autorizado con libertad estética, preferencia del operador: interfaces vivas, luminosas, brillantes, profundas y modernas; no recurrir a apariencia gris genérica por defecto. Adaptar a contexto y restricciones; no imponer cristal, colores intensos ni efectos en sistemas de marca incompatibles o interfaces críticas. Lite conserva identidad sin exigir blur.

## 1. Definir dirección visual
- Identifica marca aprobada, audiencia, tareas, densidad, medio, hardware y referencias. Distingue reconstrucción fiel, evolución y creación original. Examina tokens/componentes y recursos existentes antes de crear; si hay conflicto material de marca o alcance, eleva a Code.
- Diseña paleta, escala tipográfica, espaciado, geometría, iconos, materiales y ritmo como conjunto. Para selección de color, letra y assets consulta [color, tipografía y recursos](references/color-type-assets.md); para gramática material y variantes consulta [Crystal World](references/crystal-world.md) solo cuando pertinente. No encadenar lecturas por rutina.
- Color expresivo por jerarquía: protagonista, soporte, acento, superficies y estados; reservar intensidad donde orienta. Evitar neutralidad dominante sin propósito, saturación uniforme, degradado multicolor indiscriminado, brillo que oculte texto y estética repetida por plantilla. Un fondo claro puede ser luminoso sin ser blanco plano; un tema oscuro puede ser rico sin ser negro puro.

## 2. Construir sistema semántico
- Separar tokens primitivos de roles semánticos y variantes de componente cuando aporten valor. Marca, tema claro/oscuro y perfil material son dimensiones independientes. No duplicar código de componentes por paleta o perfil; respetar sistema de tokens existente, no introducir DTCG o generador si no hay necesidad.
- Define anatomía y estados de componentes pertinentes: navegación, botón, campo, tarjeta/superficie, diálogo, tabla/fila, gráficos y feedback. Establece color de texto/fondo/borde/foco, jerarquía, tamaño, estado, iconografía y recuperación. No aplicar todos los estados a todos los componentes por plantilla. Diferenciar principal, secundaria, destructiva y deshabilitada sin depender solo de color. Preservar nombre, semántica, teclado, orden y acciones entre variantes.
- Selecciona material y luz coherentes con jerarquía; distinguir ambiente y superficie de interacción. No usar blur como única señal de profundidad ni obligar a seis capas reales. Fallback opaco funcional y visualmente cuidado, reducción de movimiento, presupuesto y compatibilidad real.

## 3. Verificar y entregar
- Comprobar contraste efectivo sobre todos los fondos relevantes, foco, semántica, lectura, estados, tamaños, zoom/reflow, tema y variantes pertinentes. No prometer conformidad integral por una paleta o captura. Medir impacto de filtros, animaciones, assets y fuentes en objetivo representativo si material; sin prueba, declarar límite. No cambiar estados de alarma, autoridad ni interlocks por estética.
- Entregar decisiones de marca y estilo, inventario de tokens/componentes afectados, variantes y ejemplos representativos cuando autorizados, criterios y evidencia, alternativas descartadas, limitaciones y dependencia de revisión. No crear biblioteca global, copiar assets de terceros ni cambiar todas las pantallas por una necesidad local. Si el sistema existente ya satisface, reutilizar. Code conserva aceptación; Veritas/Bastión contrastan objeto estable según riesgo.
