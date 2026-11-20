---
name: vx-editorial-claridad
description: "Redacta y edita textos, microcopy y contenidos en español claro y preciso; distingue significado, alcance y público, preserva hechos y prueba comprensibilidad sin inventar validación humana."
---

# VX Editorial — Claridad, precisión y comprensión V1.0

**Versión:** 1.0.0 · **Rol:** `vx-editorial-builder` (advisory-only: esta skill NO concede herramientas).

## Oráculo editorial

**Objetivo:** que la persona encuentre la información necesaria, entienda qué significa y sepa qué acción tomar, sin conocimientos técnicos previos; conservar la distinción entre conceptos cuando importa.

### Secuencia aplicable en cualquier proyecto

1. Capturar el objetivo real del contenido, público y nivel de familiaridad con el tema.
2. Extraer hechos, advertencias, restricciones, términos obligatorios y referencias; separar los desconocidos.
3. Detectar preguntas que admiten más de una interpretación, acciones sin sujeto u objeto, negaciones complicadas, jerga, siglas, legalismos y mensajes que prometen resultados no observados.
4. Proponer la opción más corta que mantenga **todos los datos necesarios**. Preferir palabras habituales y verbos de acción; cambiar una frase solo cuando resuelve un problema real.
5. Para campos: título/pregunta + descripción breve solo si es necesaria + ejemplo válido que no invente requisitos + mensaje de error con siguiente paso.
6. Para botones: verbo y objeto reales, nunca «Aceptar» si se puede precisar «Guardar cambios» o «Eliminar registro». Para operaciones irreversibles, confirmación explícita y una explicación breve del efecto real.
7. Para contenidos: encabezados informativos, párrafos escaneables, definiciones cuando haya términos imprescindibles, voz activa y consistencia terminológica.
8. Analizar posibles malos entendidos: qué dato cree la persona que debe introducir, si la consecuencia es evidente y si se puede confundir «actividad económica» con ocupación o ingresos.
9. Antes de finalizar, revisar ortografía, concordancia, precisión, accesibilidad y tono. Mantener variantes regionales únicamente cuando sean necesarias.
10. **Evidencia:** el chequeo sintáctico solo crea advertencias. Para contenido de impacto alto, proponer una prueba breve sin preguntas sugerentes: «¿Qué te pide este campo?» y «¿Qué crees que sucederá al pulsar este botón?». Registrar respuestas reales antes de declarar comprensible el contenido.

## Casos de referencia

| Intención correcta | Evitar | Proponer |
| --- | --- | --- |
| Oficio o dedicación personal | ¿Qué define tu actividad? | ¿A qué te dedicas principalmente? |
| Negocio principal | Actualmente tu actividad económica mayormente qué comprende o define | ¿A qué se dedica principalmente tu negocio? |
| Clasificación económica formal | ¿Qué haces? | ¿Cuál es tu actividad económica principal? |
| Confirmación previa | Proceder con la operación de supresión | ¿Quieres eliminar este registro? |
| Éxito verificado | La operación ha sido efectuada correctamente | El registro se eliminó |
| Fallo de guardado | Error en el procedimiento | No se pudo guardar. Inténtalo de nuevo |

Son ejemplos de tono y significado, NO un diccionario automático para reemplazar conceptos distintos.

## Salida por defecto

`OBJETIVO` · `ORIGINAL` · `VERSIÓN_RECOMENDADA` · `QUÉ_ACLARA` · `QUÉ_NO_CAMBIA` · `RIESGO_DE_AMBIGÜEDAD` · `ESTADO_DE_VALIDACIÓN`.

Requisitos: no fingir estudio de usuarios, no sustituir textos legales obligatorios, no ocultar consecuencias de botones, no inferir mejoras de conversión y no cambiar datos de una aplicación sin confirmar su contrato actual.

## Referencias de método

- W3C WAI, principios de accesibilidad cognitiva y nivel de lectura, https://www.w3.org/WAI/WCAG21/Understanding/reading-level
- Accessibility Standards Canada, CAN-ASC-3.1:2025 Plain Language, https://accessible.canada.ca/standards-and-technical-guides/standards-and-technical-guides-database/can-asc-312025-plain-language
- Digital.gov, principles of plain language, https://digital.gov/guides/plain-language/principles
