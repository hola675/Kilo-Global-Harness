# Política de Certificación Viva V1

## Objetivo

Evitar que el harness acumule pruebas históricas, duplicadas o irrelevantes.

La regla central es:

```text
CAMBIO
→ test mínimo de la verdad nueva
→ ejecutar
→ si reemplaza una prueba anterior y pasa
→ eliminar la prueba supersedida
→ conservar historia en Git/evidencia
```

## Qué se mantiene activo

Solo pruebas que validen:

- contrato actual;
- invariante actual;
- regresión todavía plausible;
- gate actual de certificación.

## Qué no permanece activo

- tests de topologías anteriores;
- certificaciones de versiones supersedidas;
- duplicados de la misma invariante;
- tests conservados únicamente "por si acaso".

## Historia

La historia vive en:

- commits;
- PR;
- changelog;
- registry de certificación;
- evidencia runtime;
- ADR cuando aplica.

No en CI activo.

## Alcance de cada cambio

Un cambio localizado debe tener una prueba localizada. Solo se amplía el alcance si cambió una invariante transversal.

## Cierre

Al terminar un cambio, el líder debe responder:

1. qué invariante cambió;
2. qué test actual la valida;
3. qué test anterior quedó supersedido;
4. cuál se eliminó;
5. qué evidencia queda como histórica.
