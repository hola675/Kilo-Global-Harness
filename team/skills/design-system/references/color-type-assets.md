# Color expresivo, tipografía y dirección de assets
Versión del archivo: 0.1.0 | Última modificación: 2026-11-28

Referencia original de design-system para UI nueva o evolución autorizada. El color debe aportar identidad, orientación y emoción sin competir con la tarea. No asignar significado cultural universal a un tono.

## Construir paleta
1. Identificar color de marca aprobado, personalidad y función; si no existe, proponer familias cromáticas y elegir por contexto. Definir dominante, soporte, acento protagonista, superficies y texto, tonos de estado independientes.
2. Explorar armonía análoga (tonos cercanos), complementaria (contraste de matiz), complementaria dividida (contraste con mayor variedad), triádica (tres familias) o monocromática con acento de marca si apropiada. No usar pesos fijos como regla; la proporción depende de tarea y composición. Controlar luminosidad/croma, no solo matiz. Reservar saturación máxima para elementos relevantes. Neutros tintados pueden sostener lectura sin apagar identidad.
3. Diseñar rampas de valores para superficies, borde, texto, foco y estados; separar primitivos, semánticos y tokens de componente. OKLCH permite manipular luminosidad/croma/matiz de forma útil, pero L no prueba contraste WCAG ni garantiza gamut; verificar colores efectivos en sRGB y soporte. color-mix/gradientes opcionales, fallback explícito y seguro; no confiar en valores modernos en WebView antiguo.
4. Verificar pares reales sobre fondo compuesto, incluidas imágenes, brillos y transparencias. Para WCAG 2.2 AA web: texto normal 4.5:1, grande 3:1, elementos no textuales relevantes 3:1 con excepciones aplicables. No comunicar estado solo con color; incorporar texto/icono/forma y semántica. Si no se logra contraste estable, usar superficie opaca o cambiar color de texto. No convertir una muestra de paleta en certificado.
5. Separar tema claro/oscuro de material. Evitar blancos/grises genéricos por defecto, negros aplastados, acentos múltiples sin jerarquía, texto fino sobre reflejos, gradiente en texto esencial, neón difuso sin bordes y colores de alerta reutilizados como decoración confundible.

### Paletas de exploración propias (no tokens aprobados)
| Familia | Base profunda | Dominante | Acento | Luz | Superficie clara |
|---|---|---|---|---|---|
| Ocean Crystal | #071B38 | #087DDD | #00CFE8 | #A8F5FF | #F2FBFF |
| Aurora Crystal | #21113D | #803AF5 | #E74BD5 | #FFB3E8 | #FFF2FC |
| Emerald Crystal | #082E32 | #008B75 | #36DFA0 | #B8FFCE | #F0FFF8 |
| Solar Crystal | #481D12 | #E65B20 | #FFB52E | #FFE09B | #FFF6E6 |
| Sapphire Crystal | #101E48 | #435AF5 | #8575FF | #BBCBFF | #F2F4FF |
| Coral Crystal | #401A31 | #D52F71 | #FF746B | #FFBEB2 | #FFF3EF |
Son muestras ilustrativas, no pares de foreground/background verificados. No usar automáticamente como colores semánticos o de marca. Adaptar saturación y luminosidad, comprobar contraste y gamut según destino. Lite puede conservar acentos sólidos y bordes, sin translucidez.

## Tipografía
Seleccionar familia de display con carácter y familia de lectura/interfaz compatible con marca (pueden ser la misma); usar pocas familias/pesos justificados, no imponer una fuente. Establecer escala por función: títulos, subtítulos, texto, etiquetas, ayudas y cifras; ritmo de línea, anchura, peso, espaciado, alineación y densidad. Títulos pueden usar acento o tratamiento luminoso si legibles; texto esencial sólido y estable, color semántico de texto primario/secundario, no grises de bajo contraste. Usar cifras tabulares cuando comparación numérica lo necesite y fuente lo soporte. Verificar español con tildes/ñ, otros idiomas, texto largo y zoom. Font-display y fallback adecuados a carga/estabilidad; licencia de fuente y derecho de redistribución exactos, no descargar o empaquetar por defecto. Usar fuentes disponibles/autorizadas, no archivos de fuentes de terceros sin permiso.

## Assets, iconos, iluminación y composición
Definir familia de recursos con propósito: hero/ilustración, fondo, objeto de cristal, icono, fotografía, patrón y gráfico. Mantener perspectiva, dirección de luz, escala, temperatura cromática y nivel de detalle coherentes. Reservar objetos hero y reflejos fuertes para zonas de protagonismo; no recargar datos, formularios o tablas con imágenes decorativas. Para iconos funcionales priorizar reconocimiento, contraste y consistencia de trazo; variante volumétrica decorativa no sustituye símbolo funcional. Recursos originales o autorizados con licencia/procedencia, tamaño y formato adecuados; comprobar transparencia real si necesaria, bordes y legibilidad en fondos claro/oscuro. No usar texto incrustado como sustituto de texto accesible, ni copiar assets de referencia. Aplicar alternativa de formato, texto alternativo según función y presupuesto de carga; no generar/descargar recursos en ausencia de capacidad autorizada. Entregar brief de asset cuando falte herramienta, no fingir archivo producido.

Fuentes de criterio consultadas 2026-11-28: [MDN color](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Colors/Using_color_wisely), [OKLCH](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/oklch), [color-mix](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/color-mix), [web.dev tipografía](https://web.dev/learn/design/typography), [imágenes responsivas](https://web.dev/learn/images/responsive-images), [WCAG 2.2](https://www.w3.org/TR/WCAG22/). Principios y paletas propios; no se incluyen fuentes tipográficas, imágenes o código de terceros.
