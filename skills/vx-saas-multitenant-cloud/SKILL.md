---
name: vx-saas-multitenant-cloud
description: "Arquitectura e implementación SaaS multiorganización: SSR, edge, autenticación, RBAC/ABAC, Cloudflare, bases de datos y rendimiento sin comprometer aislamiento ni despliegues."
metadata:
  version: "1.0.0"
  origin: "vx-unified"
---

# VX — SaaS web y plataformas multitenant

**Activación por patrón técnico**, no por nombre de proyecto: SaaS, directorios, sitios web públicos, membresías/organizaciones, SSR, Workers, bases edge y paneles de administración. No impone Cloudflare si el proyecto usa otra nube. Leer primero código, dependencias fijadas y reglas del repositorio; elegir el stack que realmente existe.

## Contratos clave

- Frontend: UX clara, formularios con estados completos, accesibilidad teclado/contraste, responsive, render SSR/client coherente, páginas reales sin datos ficticios, performance y SEO cuando aplique.
- Backend: identidad, sesiones, organizaciones, autorización **en servidor** (no solo botón oculto), roles/permisos mínimos, rate limit y auditoría. Verificar contexto de organización en cada query/mutación y evitar enumeración lateral de recursos.
- Datos: schema/migraciones y políticas de aislamiento; separar DB staging/test de producción y no elevar acceso D1, Postgres o KV. Idempotencia de integraciones de email/CRM/pagos con consentimiento y privacidad.
- Cloud/edge: rutas del worker, bindings, configuración de entornos, redirects, CDN/caché, CSP, límites de ejecución y secrets; **una build correcta no acredita despliegue**, el resultado público exige smoke HTTP fechado.
- Diseño: fuentes/tokens y bibliotecas visuales locales son referencia estilística, no funcionalidad de negocio lista; adaptar componentes existentes antes de injertar HTML/JS sin contrato.
- Pruebas: tests focalizados de cross-tenant, auth/RBAC, errores, SSR/hydration, e2e en entorno aislado; revisión independiente en seguridad de acceso. No generar documentos/tests duplicados.

## Delegación

Un escritor para contratos/base de datos/lockfiles; se puede implementar UI y lógica de servidor en paralelo **solo con archivos exactos disjuntos**, contratos ya establecidos y barrera antes de pruebas/merge. Integraciones Cloudflare, dominios, correo real, DNS o DB remota son **R3**: pedir autorización separada, demostrar alcance y rollback. No forzar Tauri a una plataforma web.

**Salida:** rutas editadas, contrato y tenant afectado, pruebas reales ejecutadas, riesgos y evidencia separada de deploy/configuración.
