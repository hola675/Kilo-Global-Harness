---
description: Evaluar brechas de skills Kilo y proponer capacitación o skill nueva con evidencia
agent: plan
---

Formación para la tarea: $ARGUMENTS.

Consulta el inventario global existente (`inventory-sync` solo cuando se solicite actualizarlo) y las auditorías previas de Kilo; considera las skills que Kilo carga desde `~/.kilo/skills`, `~/.agents/skills` y rutas heredadas. No importes skills de repositorios externos por inercia.

Para cada brecha, identifica evidencia repetida, habilidad actual, competencias faltantes, método de formación, criterios de prueba, tiempo/costo cualitativo y regresiones posibles. Prioriza mejorar una skill existente sobre crear duplicadas.

Cuando el usuario solicite registrar la mejora, usa VX Evolution `propose --kind skill --target <skill> --title <titulo-neutro> --reason <evidencia-sin-datos-privados> --priority P1`. Esto crea una propuesta `pending_review`, nunca una nueva skill activa.

Las evaluaciones, instalaciones de skill y versiones candidatas reproducibles requieren fases posteriores. No declares 'capacitado' a un agente hasta superar tests reales.
