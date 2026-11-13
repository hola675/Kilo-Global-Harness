# ImageGen MCP · Validacion en Kilo Code

Estado declarado el 13-11-2026: el operador comprobo tres generaciones con **codex-imagegen-mcp@0.2.3** mediante el CLI de ese paquete. Los archivos se almacenaron en una biblioteca local del MCP, fuera del repositorio, con resoluciones cuadrada, horizontal y panoramica. **Esta evidencia confirma el CLI, no la visibilidad efectiva de las herramientas en la sesion de Kilo.**

## Validacion sin gastar cuota

1. Desde Kilo Code ejecutar \`/reload\` tras instalar/configurar el servidor.
2. En Settings > Agent Behaviour > MCP Servers, comprobar que \`imagegen\` esta conectado. Su mera presencia en \`kilo.jsonc\` no prueba conectividad.
3. En el chat de Kilo: "Enumera las herramientas disponibles del servidor MCP \`imagegen\`, sus nombres y parametros requeridos. No generes imagenes, no ejecutes herramientas de pago y no muestres secretos".
4. Registrar PASS solo si el cliente expone realmente las herramientas; FAIL si informa desconexion; NO VERIFICADO si la sesion no permite listarlas.
5. Una prueba posterior de imagen real solo cuando el usuario la solicite expresamente: consume cuota y puede generar archivos.

## Reglas

- Mantener el MCP en la configuracion global; nunca crear configuraciones MCP en repositorios.
- No introducir credenciales en \`kilo.jsonc\` publico ni logs. Usar las variables de entorno admitidas por Kilo.
- Por defecto guardar las salidas fuera del repositorio. Mover al proyecto solo si el usuario solicita expresamente integrar assets.
- No activar ImageGen para una tarea de texto o programacion donde ninguna imagen sea necesaria.
- No reintentar generaciones fallidas de forma ilimitada; informar errores, cuota y alternativas.
- No asumir que las llamadas del CLI y las del cliente Kilo usan la misma autenticacion si su configuracion difiere.

Referencia: https://kilo.ai/docs/automate/mcp/using-in-kilo-code
