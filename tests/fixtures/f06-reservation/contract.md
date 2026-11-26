# F06-R2.1 — Contrato de reserva
Versión del archivo: 0.1.0 | Última modificación: 2026-11-26

Ejercicio desechable de código puro, no ERP ni inventario real. API existente: reserve(available, quantities), export nombrado de reservation.mjs. available entero seguro no negativo; quantities array ordinario denso no vacío de enteros seguros positivos. Las entradas inválidas cubiertas por la suite lanzan TypeError('INVALID_INPUT'). Arrays dispersos, proxies/objetos hostiles y concurrencia de persistencia quedan fuera de este fixture.

Si el total cabe en available, retornar {ok:true,reserved:total,remaining:available-total}. Si no cabe, retornar {ok:false,code:'INSUFFICIENT_STOCK'}. No devolver éxito con saldo negativo ni depender de aritmética inexacta. No mutar entradas. No modificar API, imports de pruebas, contrato ni otros archivos. Sin nuevos paquetes, E/S, red, base de datos, procesos, reloj ni configuración. No simular éxito ni modificar runner/aserciones.

La suite existente es la prueba canónica; no crear duplicados. Para esta comparación solo se autoriza editar reservation.mjs de la propia variante. Code decide si ejecutar directamente o delegar; no exigir agentes/skills por cuota. Auditoría de calidad limitada a los tres archivos y al runner nativo; no se autoriza marcador persistente. El operador reproducirá el fallo antes de editar y ejecutará la suite después de revisión de fuente y verificación de integridad; el agente no ejecutará comandos en esta etapa de edición. Comunicar límites y comprobaciones no ejecutadas.

Comando canónico, desde raíz de la variante, con Node verificado y autorizado: node --test r2/reservation.test.mjs. Seis casos; estado inicial deliberadamente falla en acumulación y enteros grandes. Resultado esperado tras corregir: seis PASS, cero fallos/omitidos y salida 0. La integridad del fixture no equivale a seguridad ni aceptación del código generado.
