---
name: visual-ui-review
description: "Inspecciona interfaces renderizadas y fidelidad visual: composición, jerarquía, color, tipografía, assets, materiales, estados, responsive, contraste y regresiones. Usar para revisión material de UI o comparación con diseño aprobado; distinguir autoinspección de evaluación independiente. No cargar para cambios internos sin interfaz ni certificar interacción, rendimiento o accesibilidad completa mediante capturas."
metadata:
  version: "0.1.0"
  last_modified: "2026-11-28"
---

# Inspección visual profesional basada en evidencia

## Alcance
Lumen autoinspecciona su entrega; Veritas revisa objeto estable e independiente, sin mutarlo ni alterar pruebas/baselines. Code acepta y asigna correcciones. No sustituir pruebas funcionales, accessibility ni aprobación de marca. Evaluar según encargo: fidelidad, evolución, diseño original o regresión. Una preferencia estética no es defecto contractual salvo criterio aprobado.

## 1. Fijar comparación
- Identificar objeto y revisión, pantalla/flujo, referencia aprobada si existe, intención visual, tema, perfil material, estados y entorno: navegador/WebView, tamaños, DPR, fuentes, datos e idioma pertinentes. Verificar acceso autorizado; no navegar a producción, cuentas o recursos sensibles por rutina.
- Elegir evidencia mínima que distinga criterio: captura existente con contexto, render autorizado, medidas DOM/estilo o interacción. Para comparación de capturas, estados y clasificación consulta [evidencia visual](references/visual-evidence.md). Si no hay render, revisión de código/diseño limitada; no inventar imagen, coordenada o defecto observado. No repetir capturas idénticas.

## 2. Inspeccionar en orden de impacto
- Primero barreras de tarea: contenido cortado, desbordamiento, superposición, controles inaccesibles, jerarquía de acción ambigua, estado engañoso, foco tapado, contraste insuficiente. Distinguir defecto observado de riesgo inferido; para semántica/teclado usar comprobación funcional pertinente, no deducir de imagen.
- Luego composición: alineación, ritmo, escala, espacios, densidad, adaptación a texto y pantalla, consistencia de componentes, fuentes y assets. No exigir simetría, tarjetas, bordes redondeados o espaciado uniforme cuando la intención justifica otra composición.
- Si Crystal World aplica, evaluar armonía cromática y protagonismo, tipografía expresiva/legible, luz y perspectiva coherentes, materiales y espesor visual, separación de planos, estados, calidad de recursos y fallback opaco. Evitar gris genérico en creación autorizada, pero no penalizar neutralidad funcional o marca que la exige. No prescribir brillo o saturación máxima en cada superficie. Evaluar Premium/Professional/Lite según contexto.
- Probar estados alcanzables y tamaños relevantes, contenido extremo autorizado, temas y reducción de efectos según impacto. No afirmar compatibilidad de hardware o rendimiento sin medición. No alterar autoridad, alarmas o interlocks por estética.

## 3. Clasificar y verificar corrección
- Cada hallazgo: objeto/estado/entorno, criterio, observado/esperado, impacto, gravedad y evidencia, alcance de corrección propuesto; distinguir regresión, defecto previo, diferencia válida, incertidumbre y recomendación. Priorizar bloqueo de tarea y seguridad, luego barreras/materialidad y acabado; no asignar gravedad alta por gusto.
- Para comparación automatizada usar baseline aprobado y condiciones equivalentes; no aceptar primer snapshot como diseño válido ni actualizar referencia para silenciar diferencia. Variaciones de plataforma, fuente o datos requieren explicación; no esconder contenido relevante ni relajar tolerancia para obtener verde. Reutilizar herramientas existentes autorizadas.
- Entregar hallazgos sin duplicados, riesgos residuales y estado por criterio; si no hay defecto material, explicitar qué se inspeccionó. Veritas devuelve correcciones a Code y comprueba delta estable después; no edita objeto ni pruebas. Sin evidencia suficiente, NOT_RUN/BLOCKED/NOT_VERIFIED por alcance.
