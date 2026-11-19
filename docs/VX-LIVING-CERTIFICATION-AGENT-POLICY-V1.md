# Living Certification — política de agentes

Esta política es transversal al harness.

## Aplicación por rol

- **Líderes/coordinadores**: deciden `UPDATE / REPLACE / ADD`, exigen PASS y retiran supersedidos.
- **Quality/Test Analyst**: diseñan el oráculo mínimo y justifican riesgo diferencial.
- **QA Builder**: implementa el test según la decisión; no duplica archivos/gates por versión.
- **Reviewer/Inspector**: detectan duplicación, tests sin invariante vigente y retiros prematuros.
- **Platform**: mantiene propiedad única de gates y separa source/integration/runtime.
- **Security**: conserva guards por riesgo vigente, no por antigüedad; retiro solo con reemplazo PASS.

La regla global vive en `rules/vx-global-harness-v3.md`. Los textos de cada agente solo contienen su obligación específica.
