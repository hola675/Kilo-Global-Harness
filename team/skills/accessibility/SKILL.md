---
name: accessibility
description: "Diseña y verifica accesibilidad de interfaces: semántica, nombre y estado accesible, teclado, foco, contraste real, lectura, formularios, tamaño, movimiento y alternativas. Usar al construir o revisar interacción compleja, cambios de semántica, color, contenido o layout con impacto inclusivo. No cargar para cambios sin impacto de accesibilidad ni declarar conformidad integral por una inspección parcial."
metadata:
  version: "0.1.0"
  last_modified: "2026-11-28"
---

# Accesibilidad integrada y verificable

## Alcance
Lumen diseña o corrige dentro de escritura autorizada; Veritas verifica sin editar objeto ni pruebas. Code acepta y resuelve requisitos vinculantes. Esta skill aporta técnica inclusiva, no sustituye seguridad, UX ni selección de pruebas. Para web/WebView usar WCAG 2.2 AA como referencia salvo requisito distinto aplicable; no prometer certificación legal ni trasladar criterios CSS literalmente a controles nativos.

## 1. Reconocer barreras
- Identifica tarea, controles, estados, contenido, entrada, tamaños y plataforma objetivo. Inspecciona lo afectado, no toda aplicación por rutina. Para widget complejo, cristal, foco o evaluación detallada consulta [interacción accesible](references/accessible-interaction.md).
- Usa semántica nativa compatible antes de ARIA personalizada; si hace falta widget complejo, aplica patrón apropiado y prueba comportamiento. No añadir roles contradictorios, nombres que no coincidan con etiqueta visible ni controles ocultos a tecnologías asistivas.
- Verifica estructura, encabezados, regiones, idioma, alternativas de imágenes, etiquetas y orden de lectura cuando afecten a tarea. Icono decorativo no añade ruido; control con icono requiere nombre. Evita información esencial solo en imagen, color, posición, sonido o gesto.

## 2. Construir interacción inclusiva
- Diseñar recorrido de teclado, foco visible y no oculto por overlays/cabeceras, sin trampas fuera de modalidades previstas; restaurar foco a origen o destino lógico tras cierre o cambio de contexto. Evitar tabindex positivo como parche. ARIA no implementa teclado por sí sola.
- Mantener etiquetas persistentes, restricciones antes del error, descripción asociada, errores específicos y recuperación; conservar datos seguros. Anunciar cambios relevantes sin mover foco por rutina ni duplicar mensajes. Nunca presentar estado desconocido como éxito/fallo ni atribuir autoridad a control visual.
- Comprobar contraste real por par y estado, incluyendo fondos compuestos, reflejos, hover/focus/selección y texto sobre assets. Preservar identidad cromática ajustando luminosidad, borde o superficie opaca, no exigir diseño gris. No usar brillo como indicador exclusivo. Adaptar objetivos táctiles, zoom/reflow, texto ampliado y espaciado; respetar movimiento reducido, colores forzados cuando soportados y alternativas a arrastre/gestos.

## 3. Verificar y entregar
- Combinar inspección de código/árbol accesible, interacción manual, medición de contraste y automatización existente. Probar teclado y foco en estados alcanzables; comprobar lector de pantalla real autorizado cuando criterio dependa de anuncio/semántica efectiva. Árbol o simulación no demuestra comportamiento de todos los lectores; captura no prueba interacción. No instalar escáner ni navegador por rutina.
- Registrar criterio exacto y aplicabilidad, objeto/versión, entorno, pasos, observado/esperado, impacto, evidencia y límite; diferenciar incumplimiento, hipótesis y recomendación. Veritas no modifica pruebas/objeto ni aprueba su propia corrección. Revalidar delta y regresiones pertinentes sin repetir auditoría completa.
- Si falta acceso o herramienta, revisión estática limitada y pruebas afectadas NOT_RUN/BLOCKED/NOT_VERIFIED según corresponda. No eludir deny. Para afirmación formal definir alcance, requisitos, páginas/procesos completos y evidencia suficiente con responsable autorizado; cero alertas no certifica conformidad.
