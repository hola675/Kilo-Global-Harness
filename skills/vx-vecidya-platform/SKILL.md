---
name: vx-vecidya-platform
description: "Desarrollo verificable de Vecidya: SaaS React Router SSR/Cloudflare, seguridad multi-organización, GHL separado y Crystal Depth como biblioteca visual, respetando gobierno documental."
metadata:
  version: "1.0.0"
  origin: "vx-unified"
---

# VX — Vecidya Platform y sistema visual Crystal Depth

**Repositorio:** `hola675/Vecidya`. **Trabajo producto:** `vecidya-platform/`; `vecidya-crystal-depth/` es laboratorio/biblioteca HTML/CSS de patrones y atmósferas, no importación directa de React ni prueba de deploy. **No inferir estado reciente desde esta skill**: consultar `AGENTS.md`, `vecidya-platform/docs/GOVERNANCE.md`, `STATUS.md`, `PROJECT_STATE.md` y fuente/CI en el HEAD actual antes de editar. Si estos textos contradicen la skill, prevalecen código y gobierno local.

## Arquitectura verificada en la fuente

- TypeScript, React 19, React Router 8 SSR, Vite 8, Tailwind CSS 4; Cloudflare Workers, `workers/app.ts`, D1 SQLite + Drizzle, Better Auth con organizaciones. Node >=22.12, pnpm de `vecidya-platform/package.json` y lockfile en el HEAD actual.
- Producto: presencia web y directorio de comercios **Vecindario**, perfiles públicos, funciones de plataforma, MiniWeb, Diagnóstico y administración según rutas reales. **No duplicar GHL:** leads, contactos, campañas y seguimiento comercial pertenecen a GHL; la metadata de integración no demuestra que el conector esté operativo.
- Seguridad: todo recurso de organización requiere sesión, membresía y permiso; `platform_admin` exige membresía de plataforma activa, organización explícita, acción autorizada y auditoría. No impersonar propietarios; no añadir datos comerciales ficticios ni asociar marcas terceras sin derechos.
- Entornos: `wrangler deploy` puede publicar en `vecidya.com`. **Prohibido ejecutar deploy, D1 remoto, migración productiva, correos reales o cambios de Cloudflare/DNS** sin autorización separada. Tests E2E solo contra Worker/D1 aislados salvo indicación expresa.
- Diseño: biblioteca `vecidya-crystal-depth/` como manual de composición, superficies, escenas por profundidad, sistema claro/oscuro, movimiento reducido y tokens. Leer `docs/INTEGRACION.md`, `docs/DIRECCION-ARTISTICA.md` y `assets/pattern-registry.json` antes de adoptar patrones. Premium visual no justifica sacrificar legibilidad, accesibilidad, jerarquía ni datos reales.

## Trabajo por especialidad

- **Frontend + UX:** comprobar la ruta y shell reales antes de proponer una escena Crystal; estados loading/error/empty/denied, navegación, teclado, zoom, contraste, `prefers-reduced-motion` y responsive móvil. Reutilizar CSS/componentes existentes, no importar HTML puro en JSX sin adaptación y pruebas.
- **Backend + Datos:** schema Drizzle como fuente de verdad; filtros por organización, guards en Worker y migra­ciones de alcance limitado; no usar D1 remoto para test. Documentar derechos de miembros, consentimiento y aislamiento intertenant.
- **QA:** preferir tests focales actuales (scripts de package.json y `docs/TESTING.md`); cubrir selección de organización, restricciones Admin, consentimiento, R1 contrato/QA Chromium R2 cuando aplique, sin afirmar HTTP público realizado si no existe evidencia anónima fechada.
- **Editorial + Docs:** lenguaje comercial inequívoco y respetuoso, frases que describen acción económica concreta, no inventar planes/precios/licencias; mantener máximo documental y reconciliar en docs canónicos (el proyecto impone techo de documentos). El contenido de biblioteca **no** habilita funciones de negocio.

## Gobernanza de rama y evidencias

Vecidya exige `origin/main` fresco, rama y **worktree aislado** por checkpoint; las ramas recomendadas están en `AGENTS.md` (e.g. `feat/app-mini-*`, `fix/*`). No trabajar directo en `main` ni realizar el merge sin autorización local separada; la norma específica de Vecidya prevalece sobre la pauta general del Harness. Actualizar código y documentación canónica en el mismo cambio, sin abrir un Markdown por fase. Evidencias `CODE/TEST/RAN/CONFIG/GIT/HTTP/DOC`: `HTTP` público con fecha para afirmar “publicado”. Un CI verde no demuestra publicación.

**Fuentes locales:** `AGENTS.md`; `vecidya-platform/README.md`, `docs/{STATUS,PROJECT_STATE,GOVERNANCE,TESTING,ARCHITECTURE}.md`; `vecidya-crystal-depth/README.md` y guías de diseño. Esta skill es perfil de dominio, no permiso de despliegue.
