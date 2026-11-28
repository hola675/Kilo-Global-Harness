# Crystal World — gramática de materiales, iluminación y profundidad
Versión del archivo: 0.1.0 | Última modificación: 2026-11-28

Dirección artística propia, contextual y adaptable; no librería ni marca universal. Preferencia para creación visual autorizada: riqueza cromática, profundidad tangible, superficies pulidas y luminosidad intencional. No aspecto neutro genérico. Preservar el contexto operativo, marca aprobada y accesibilidad. No simular refracción física real si solo es aproximación CSS.

## Jerarquía material
| Nivel lógico | Función | Tratamiento candidato |
|---|---|---|
| L0 Ambiente | Luz y atmósfera de fondo | Campo cromático, gradiente tonal o iluminación suave, no competir con información. |
| L1 Escenario | Organizar el espacio | Planos diferenciados, ritmo, composiciones y fondos con zonas de lectura estables. |
| L2 Estructura | Navegación y regiones | Material estable, bordes y elevación discretos. |
| L3 Superficie | Tarjetas, tablas, formularios | Cristal claro/esmerilado/tintado u opaco; área de texto legible. |
| L4 Interacción | Controles y selección | Relieve, reflejo dirigido, respuesta de foco/press, estado funcional inequívoco. |
| L5 Protagonista | Acción principal, pieza visual o dato prioritario | Mayor contraste/volumen/luz según objetivo; evitar múltiples protagonistas competidores. |

No es z-index, orden de foco ni obligación de seis capas CSS. Simular espesor con borde interno/externo y luces discretas, sombras coherentes con dirección de luz y altura relativa; controlar brillos especulares en bordes y superficies, no sobre texto. Usar sombras con matiz del ambiente cuando aporte naturalidad; no repetir una sombra negra idéntica en todos los planos. Los objetos/íconos tridimensionales comparten perspectiva, dirección de luz, escala y material; iconos funcionales conservan silueta clara, incluso en modo monocromo.

## Perfiles de representación
- Premium: composición rica, color protagonista, materiales translúcidos y detalles de luz cuando soportados; recursos optimizados. No confundir premium con blur generalizado o neón constante.
- Professional: acentos vivos, superficies estables en tablas/formularios, profundidad contenida; ritmo de uso repetido y texto prioritario.
- Lite: identidad mediante geometría, color sRGB, bordes, superficies sólidas y sombras simples; reducir transparencias, animación y coste. No convertirlo en tema gris por defecto. Fallback conserva acciones e información incluso sin filtros.
En cada perfil mantener mismo contrato funcional y semántico. Paletas/temas de marca pueden cambiar independientemente. Mantener modo opaco explícito; respetar movimiento reducido, preferencias disponibles y alto contraste/colores forzados cuando pertinente. No depender solo de una media query de transparencia.

## Componentes y verificación
Botón: jerarquía de acción, relieve claro, estado foco/press/disabled/carga; no hacer texto brillante ilegible. Campo: superficie estable, etiqueta, borde/foco/error y ayuda. Tarjeta: contraste de plano sin ocultar contenido. Diálogo: distinguir overlay y contenido; no impedir foco/teclado. Tabla: lectura alineada, fila/selección y encabezado inequívocos, no blur por fila. Navegación: ubicación y activo identificables. Gráficos: leyenda/etiquetas, contraste y redundancia semántica; no confiar en color aislado.
Comprobar sobre fondos extremos representativos, tema y material, recursos limitados y alternativas. Aceptación visual incluye identidad, jerarquía, contraste, ausencia de solapamiento, coherencia de luz, densidad y comportamiento; no prometer fps o consumo sin medir. Uso industrial: estados/alarma, interlocks y autoridad preservados.
Fuentes de criterio: [Josh W. Comeau: sombras](https://www.joshwcomeau.com/css/designing-shadows/) (actualizado 2026-04-27), [MDN backdrop-filter](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter), [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [DTCG Format 2025.10](https://www.designtokens.org/tr/2025.10/format/) como referencia de interoperabilidad, no requisito. Consulta 2026-11-28. Material original, sin recursos de terceros.
