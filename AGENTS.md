# Instrucciones del repositorio — desarrollo del Harness
Versión del archivo: 0.1.0 | Última modificación: 2026-11-24

Estas instrucciones gobiernan este repositorio, no se instalan globalmente. Las políticas candidatas de usuario viven en team/policies/AGENTS.md.
- Leer docs/PLAN-MAESTRO.md y docs/ROADMAP.md; ejecutar la primera fase desbloqueada, sin declarar fases terminadas sin evidencia.
- Code es el único agente principal; no reemplazar prompt nativo, no crear otro modo líder ni reutilizar legacy como implementación. No modificar legacy/.
- Antes de introducir una herramienta, localizar la capacidad nativa, reproducir la carencia y comparar alternativas. Verificar documentación, versión, licencia y fuente primaria; no copiar ciegamente código externo.
- Cambios pequeños y coherentes. Un escritor por archivo; preservar trabajo concurrente. No modificar archivos ajenos a la tarea, no revertir cambios de otros. Usar ramas temporales y PR para cambios de implementación; integrar en main tras pruebas/revisión y eliminar rama integrada si autorizado. No force-push.
- Cada archivo de política, agente, skill, script o documento lleva versión individual y fecha de última modificación en cabecera o metadata compatible; no añadir campos incompatibles a configuraciones nativas. Registrar historia resumida una vez por sección en CHANGELOG.md (versiones de archivos independientes de release).
- No almacenar secretos, transcripciones, configuraciones de cliente ni datos locales en Git. No publicar ni instalar globalmente cambios sin autorización.
- Pruebas focalizadas: actualizar o sustituir pruebas obsoletas por equivalentes que mantengan cobertura; conservar invariantes de seguridad y regresiones distintas. Reportar PASS, FAIL, BLOCKED o NOT_RUN con evidencia; nunca inventar.
- Mantener instrucciones y skills en español neutro, código e interfaces según convenciones de cada proyecto. Informar decisiones, límites y riesgos.
