---
name: vx-frontend-quality
description: "Usar para implementar o revisar una interfaz web accesible, coherente, responsiva y verificable en un proyecto de software asignado; no usar para backend sin UI ni afirmar capturas/pruebas de navegador no ejecutadas."
---

# VX Frontend Quality V0.1

**Especialidad:** UI, UX, frontend React/HTML/CSS y accesibilidad. Para Daniela (auditoría read-only) y `vx-frontend-builder` (implementación con permisos). No genera imágenes ni instala dependencias automáticamente.

## Reconocimiento
Verificar framework, router, estilos existentes, design tokens, componentes reutilizables, navegador/test runner disponibles. Identificar usuarios, contenido, estados críticos y tamaños de pantalla previstos. Ante falta de referencia visual, hacer una propuesta y marcarla como tal.

## Criterios de aceptación
- Semántica: landmarks, headings coherentes, etiquetas de inputs, mensajes de error vinculados.
- Teclado: tabulación, foco visible, escape de diálogos y sin trampas de foco.
- Contraste: exigir medidas, **no** afirmar conformidad WCAG por opinión.
- Responsive: contemplar longitudes de texto, zoom y overflow; preferir unidades fluidas.
- Estados: cargando, vacío, error, éxito, validación y accesibilidad de feedback.
- Performance: no cargar librerías pesadas ni imágenes innecesarias; medir antes de optimizar.
- Coherencia: seguir sistema visual del proyecto y no introducir estilos globales que rompan otras pantallas.

## Flujo
1. Daniela prepara criterios y prioridades, y señala límites de evidencia.
2. Implementador obtiene contrato de tarea y rango de archivos; `edit/bash` bajo aprobación.
3. Validar typecheck/lint/tests con salida real; pruebas visuales en navegador solo si existe herramienta permitida.
4. Rafael diseña casos E2E; QA builder los automatiza si la tarea lo justifica.
5. Daniela revisa la entrega; Lucas revisa diff. Cerrar con `{screens,files,acceptance_checks,measured_checks,unknowns}`.

**No confundir** una propuesta de diseño con un screenshot existente. Nunca escribir en Kilo HOME por trabajar en frontend.
