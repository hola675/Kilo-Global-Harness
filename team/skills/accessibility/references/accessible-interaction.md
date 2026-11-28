# Interacción accesible y contraste verificable
Versión del archivo: 0.1.0 | Última modificación: 2026-11-28

Referencia contextual de accessibility. WCAG 2.2 (Recomendación W3C de 2024-12-12) es normativa web; APG, guías explicativas y comprobaciones preliminares son informativas. Verificar criterio/nivel/excepciones y alcance contractual.

| Garantía web | Criterios de referencia | Comprobación focalizada |
|---|---|---|
| Significado y nombre | 1.1.1, 1.3.1, 2.5.3, 4.1.2 | Etiquetas, relaciones, nombre/rol/valor y estados accesibles. |
| Contraste y color | 1.4.1, 1.4.3, 1.4.11 | Texto normal 4.5:1, grande 3:1; información visual necesaria de controles/gráficos 3:1 frente a colores adyacentes, según excepciones. No solo color. |
| Tamaño y adaptación | 1.4.4, 1.4.10, 1.4.12, 2.5.8 | Texto al 200 %, reflow equivalente a 320 CSS px de ancho para scroll vertical o 256 de alto para horizontal, con excepciones; espaciado sin pérdida; objetivo 24×24 CSS px o excepciones. Elegir mayor según contexto. |
| Teclado y foco | 2.1.1, 2.1.2, 2.4.3, 2.4.7, 2.4.11 | Recorrido real, foco visible, no totalmente oculto por contenido del autor (mínimo AA 2.4.11), cierre y regreso lógico. |
| Movimiento y entradas | 2.2.2, 2.3.1, 2.5.7 | Pausar/detener movimiento cuando aplique, evitar destellos peligrosos, alternativa a arrastre cuando requerida; respetar prefers-reduced-motion como técnica, no criterio AA universal. |
| Formularios y feedback | 3.3.1–3.3.4, 3.3.7, 3.3.8, 4.1.3 | Error/ayuda, prevención de errores relevantes, evitar entradas redundantes cuando aplique, autenticación accesible, anuncios sin cambio de foco innecesario. |

## Interacciones específicas
- Modal: nombre accesible y modalidad real; foco inicial lógico, tabulación dentro, salida accesible y recuperación de foco al invocador o destino lógico. Comprobar Escape según patrón y restricciones válidas; no anunciar aria-modal si fondo aún interactivo. Popover no es modal por definición.
- Selector: preferir select nativo para elección simple adecuada. Combobox editable o de selección tiene patrón y teclado según popup; preservar edición de texto y estados de expansión, selección y foco. Consultar APG exacto para variante; no traducir menú de acciones a listbox sin verificar semántica.
- Campos: label visible y asociado, error específico, estado invalid cuando corresponda, descripción vinculada, entrada preservada si segura; status sin interrumpir por cada pulsación. Confirmación depende de autoridad real.
- Crystal World: verificar colores finales de primer plano/fondo en estados y zonas extremas representativas, no comparar hex de token aislado sobre transparencia. Si gradiente/imagen dinámica impide contraste estable, estabilizar superficie. Controles, borde/foco y lectura deben conservarse sin blur, animación ni sombras; en colores forzados respetar colores de sistema cuando proceda. Conservar acentos y marca si compatible.

## Evidencia
Separar inspección estática, automatización, teclado/manual, lector de pantalla real y prueba con usuarios; registrar cobertura y herramienta/versión. Para contraste usar método WCAG sobre fondo efectivo; una muestra ilustrativa de paleta no certifica estados. Revisar casos no decidibles por herramienta. No afirmar cumplimiento completo por cero violaciones de axe. No copiar código ni instalar herramientas.

Fuentes consultadas 2026-11-28: [WCAG 2.2 fijada](https://www.w3.org/TR/2024/REC-WCAG22-20241212/), [APG modal](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/), [APG combobox](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/), [WAI Easy Checks](https://www.w3.org/WAI/test-evaluate/preliminary/), [WAI evaluación](https://www.w3.org/WAI/test-evaluate/conformance/), [Playwright accessibility](https://playwright.dev/docs/accessibility-testing), [MDN forced-colors](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/forced-colors), [MDN prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion). Síntesis original sin ejemplos ni assets de terceros incorporados.
