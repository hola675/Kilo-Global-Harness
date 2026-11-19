# VX Dev UX/UI Pro V1

**Estado:** `SOURCE_READY_RUNTIME_INACTIVE`  
**Nuevas skills:** 9  
**Runtime:** sin cambios  
**ACL/installer:** sin cambios

## Diseño

La capa sigue un patrón **router + especialistas**. `vx-dev-ux-ui-pro-review` sirve para una auditoría amplia. Los pedidos estrechos deben activar una skill especializada, evitando cargar todo el conocimiento UX/UI cuando no hace falta.

## Catálogo

| Skill | Función |
|---|---|
| `vx-dev-ux-ui-pro-review` | Auditoría integral y priorización |
| `vx-dev-design-system-governance` | Tokens, componentes, themes y drift |
| `vx-dev-responsive-resilience` | Viewports, zoom, localización, themes, datos extremos |
| `vx-dev-forms-ux` | Formularios, validación, submit y recovery |
| `vx-dev-ux-writing-content` | Microcopy, errores, onboarding y trust |
| `vx-dev-information-architecture` | Navegación, jerarquía, búsqueda y findability |
| `vx-dev-interaction-motion` | Feedback, transición, gestos y reduced motion |
| `vx-dev-data-visualization` | Charts, escalas, densidad y accesibilidad |
| `vx-dev-visual-craft` | Jerarquía visual, tipografía, color y distintividad |

## Qué aprendimos de repos públicos

Se revisaron patrones de XIAS/ux-ui-agent-skills, Designer Skills, MAX-DESIGN, AI Frontend Skill Packs, Interface Craft y Agent Toolkit.

Los patrones adoptados son arquitectónicos, no texto copiado:

- evidencia antes de puntuación;
- prioridad de task blockers/a11y sobre polish;
- design system antes de inventar;
- stress de contenido, temas, zoom y responsive;
- microcopy y forms como disciplinas separadas;
- visual craft con intención y no “AI slop”;
- router integral + especialistas;
- verificación proporcional y estados no observados marcados como desconocidos.

## Principio “Pro Max”

“Pro” no significa aplicar más efectos. Significa:

1. entender tarea, usuario y contexto;
2. revisar comportamiento real, no solo screenshot ideal;
3. preservar sistemas existentes salvo evidencia;
4. detectar edge cases y estados;
5. separar hechos de hipótesis;
6. priorizar fixes por impacto;
7. terminar con verificación explícita.

## Propuesta de roles

- Frontend: las 9.
- Reviewer: `ux-ui-pro-review`, `visual-craft`.
- Architect: `design-system-governance`, `information-architecture`.
- Quality: `responsive-resilience`, `forms-ux`, `data-visualization`.

Esto es solo propuesta; no se cambian ACL en esta rama.

## Activación futura

Antes de instalar:

- ejecutar evals de triggering y solapamiento;
- validar que el router no absorba pedidos estrechos;
- validar false positives frente a `frontend-ux`, `accessibility` y `ui-state-system`;
- aprobar ACL exactas;
- actualizar instalador y backup;
- recertificar runtime afectado.
