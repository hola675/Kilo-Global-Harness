---
name: vx-security-review
description: "Usar para revisar o diseñar cambios relacionados con autenticación, autorizaciones, entrada externa, manejo de secretos, dependencias y permisos; producir amenazas y pruebas negativas, sin explotación de sistemas reales."
---

# VX Security Review V0.1

**Uso:** Valentina/inspector/coordinador por demanda. No eleva permisos ni contiene herramientas de ataque; evaluación de seguridad sin evidencia se reporta `NO_VERIFICADO`.

## Mini modelo de amenazas
1. Definir sistema, límites de confianza, usuarios reales, actores y activos; separar entornos local/DEV/producción.
2. Identificar entradas no confiables, uso de credenciales, rutas, shell, red, almacenamiento y migraciones.
3. Para cada riesgo formular `{asset,precondition,attack_path,impact,evidence,mitigation,test}` y marcar severidad proporcional.
4. Comprobar controles: validación de inputs, autorizar **en servidor**, rutas, cifrado, logging sin secretos, permisos mínimos, actualizaciones con origen y verificación.
5. Revisar amenazas propias de agentes: instrucciones inyectadas en repos o MCP, llamadas de herramientas no autorizadas, retorno de subagente manipulable, credenciales en reportes, autoconcesión de permisos.
6. Pedir al ejecutor tests negativos en fixtures, preferentemente diferenciando casos donde la defensa debería permitir frente a bloquear.

## Publicación
No afirmar que un campo `approved` en JSON autentica identidad ni que un hash demuestra inmutabilidad. La publicación de Pack VX sigue bloqueada hasta autenticación, backups/rollback y aprobación humana verificables. Sin test real devolver `NO_EJECUTADO`.

**Salida:** hallazgos priorizados (máx. 8), evidencias ruta/línea, positivos descartados, mitigación y pruebas sugeridas. No ejecutar exploits o usar MCP externo por esta skill.
