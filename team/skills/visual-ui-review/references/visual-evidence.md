# Evidencia visual, comparación y gravedad
Versión del archivo: 0.1.0 | Última modificación: 2026-11-28

Referencia de visual-ui-review. Las capturas son evidencia de representación en condiciones concretas; no de interacción, autorización, accesibilidad completa ni rendimiento.

## Seleccionar muestra y método
Identificar revisión, referencia y aprobación, ruta/componente, viewport/DPR, zoom, plataforma/motor, fuentes cargadas, tema/material, datos e idioma, estado de interacción. Usar datos ficticios o autorizados, excluir secretos e información privada de capturas y no publicar sin autorización. Seleccionar tamaños según objetivo y puntos de cambio, estados relevantes y casos extremos representativos.

| Método | Demuestra | No demuestra por sí solo |
|---|---|---|
| Código/tokens | Implementación declarada y riesgos | Render ni interacción efectiva |
| Captura contextual | Apariencia y defectos visibles del estado | Teclado, anuncios, reglas de negocio |
| DOM/estilos medidos | Geometría y propiedades en entorno observado | Experiencia completa o conformidad integral |
| Interacción autorizada | Resultado de recorrido probado | Todos los recorridos y plataformas |
| Comparación de imágenes | Diferencia respecto a referencia comparable | Que referencia o resultado sean correctos |
| Medición de rendimiento | Métrica y escenario registrados | Otros equipos/cargas sin prueba |

Para visual regression estabilizar datos, fuentes, animaciones y estado de forma controlada sin ocultar defecto; registrar motor/plataforma y resolver diferencias legítimas. Umbrales de diferencia solo justificados por ruido observado y oráculo; no ampliar tolerancia o reemplazar baseline sin aceptación. Probar una muestra válida y una defectuosa conocida antes de confiar en detección de defecto material. Usar Playwright, herramientas de diseño o inspector solo si expuestos y autorizados; no instalar ni enviar datos a un MCP por comodidad.

## Rúbrica visual original
| Dimensión | Qué observar |
|---|---|
| Composición | Jerarquía, alineación, espaciado, ritmo y puntos de atención según tarea. |
| Identidad | Paleta, tipografía, escala, componentes y recursos coherentes con marca aprobada. |
| Material | Espesor, luz, sombras, reflejos y separación de planos; no brillo sobre contenido esencial. |
| Lectura | Contraste efectivo, tamaño/longitud, números, etiquetas y contenido realista. |
| Adaptación | Reflow, contenido largo, tamaño táctil, zoom, tema, variantes y fallback. |
| Estados | Activo, selección, foco, hover, error, carga o deshabilitado donde correspondan; significado inequívoco. |
| Assets | Bordes, proporción, nitidez, perspectiva y procedencia; no evaluar licencia por apariencia. |

Gravedad: bloqueante si impide tarea crítica o causa riesgo material comprobado; alta si barrera material importante sin alternativa adecuada; media si degrada uso, identidad aprobada o mantenibilidad con alternativa; baja para acabado local; recomendación para preferencia no contractual. Ajustar según contexto y frecuencia. Un hallazgo hipotético no es FAIL funcional. Ejemplo propio: tarjeta cristal con texto claro sobre reflejo claro es riesgo si solo hay diseño, defecto de contraste si medición efectiva incumple criterio aplicable; verificar fondo opaco o cambio de texto, no eliminar toda identidad cromática.

Fuentes consultadas 2026-11-28: [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots), [Playwright best practices](https://playwright.dev/docs/best-practices), [Nielsen heurísticas](https://www.nngroup.com/articles/ten-usability-heuristics/) revisadas 2024-01-30, [WAI Easy Checks](https://www.w3.org/WAI/test-evaluate/preliminary/), [WCAG 2.2](https://www.w3.org/TR/WCAG22/). Heurísticas no son norma ni evidencia de usuario. Rúbrica y ejemplo propios.
