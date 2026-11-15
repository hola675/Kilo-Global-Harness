# VX Evolution V4.7.2 — diseño de seguridad de aprobación

**Estado:** diseño y pruebas de contrato aisladas sobre `work/v4-7-2-approval-security`, creada desde `main` en `11b4869589dcb34a9d4aa74e01ce945f2b879e22`. V4.7.2 no habilita autenticación, decisiones efectivas, publicación, instalación, `approval_granted` ni `apply_supported`.

## Alcance e invariantes

- Alcance de una sola PC Windows, conforme a VX-D08; sin sincronización ni servicio remoto.
- V4.7.0 preview y V4.7.1 approval request siguen como precedentes. El preview permanece `DRY_RUN`; cada resultado de V4.7.2 debe conservar `approval_granted=false` y `apply_supported=false`.
- La entrega implementa formatos cerrados y validación estructural/estados de referencia en memoria. No llama a WebAuthn/CNG/DPAPI, no genera ni almacena claves, no enrola usuarios, no crea ni modifica HOME/SQLite reales, no cambia configuración global y no programa tareas.
- Campos de identidad, credencial, UV, revocación, firma y contador en fixtures son **aserciones de prueba**, no hechos verificados. El digest y un hash de auditoría no son firma ni autenticación.
- Todo consumidor de JSON serializado debe usar `strict_json_loads()` para detectar claves duplicadas/constantes no estándar. Los validadores de objetos Python no pueden recuperar claves descartadas previamente por un parser permisivo.
- `validate_webauthn_envelope()` coteja los objetos recibidos y parsea client/authenticator data; no verifica criptográficamente la firma, no consulta un registro de credenciales ni vuelve a leer fuentes/destinos. El caller debe regenerar el preview antes de evaluar cualquier solicitud futura.
- La entrada no tiene límites máximos de bytes/campo/eventos. Como estos contratos no están expuestos por un endpoint ni consumidos desde red en V4.7.2, los límites de ingestión quedan pendientes; cualquier integración futura deberá definirlos antes de aceptar datos externos.
- Esta fase no fija límites máximos de tamaño por campo ni de longitud de la lista de eventos del chain verifier. Las funciones no son un servicio/endpoint de ingestión; cualquier consumidor futuro de entrada no confiable deberá imponer límites antes de parsear/recorrer y añadir pruebas de límite.

## Comparación de alternativas

| Alternativa | Ventajas | Riesgos/requisitos | Evaluación |
| --- | --- | --- | --- |
| Windows WebAuthn API con Windows Hello platform authenticator | API Win32 para registrar credenciales y solicitar assertions; la plataforma ofrece UI del autenticador; challenge y RP ID quedan en el protocolo de clave pública; puede exigir user verification | Requiere RP ID/origin fijo, enrolamiento autenticado, validación de assertion/attestation y revisión de la UI. La capacidad real del perfil/PC no está verificada. No confundir el inicio de sesión Windows Hello de una cuenta local con una credencial WebAuthn | **Candidato seleccionado para prototipar**, no instalado ni ejecutado |
| FIDO2 security key externa mediante la misma API | Autenticación de clave pública y posesión de token; puede requerir PIN/user verification; separa la credencial física del inicio de sesión local | Coste/disponibilidad, pérdida/recambio, enrolamiento y revocación. Si está conectada, malware local todavía puede intentar solicitudes; la UI no demuestra por sí sola que se entendió el diff | Alternativa interoperable; no fallback silencioso |
| Clave CNG/TPM protegida localmente | Claves no exportables cuando el proveedor/TPM lo garantiza; API criptográfica nativa | Una llamada de firma directa no implica necesariamente presencia/consentimiento por operación; hace falta verificar hardware y vincular una ceremonia humana | Útil para custodia/identidad del dispositivo; no seleccionada como prueba suficiente del aprobador |
| DPAPI / Windows Credential Manager | Protegen secretos almacenados con el contexto de usuario/equipo; pueden ser defensa de datos en reposo | Un proceso ejecutado bajo la sesión autorizada puede recuperar/usar el secreto. No prueban una aprobación humana fresca ni resisten por sí solos el compromiso del perfil | No seleccionar como autenticador; solo podría proteger secretos en una fase posterior |
| TTY, contraseña o nombre escrito | Baja fricción y sin dependencias | No prueba identidad ni separa autor/aprobador; no firma el objeto ni bloquea replay | Rechazado como mecanismo de aprobación |
| Windows Hello for Business / identidad organizativa | Políticas de cuenta/dispositivo y asociación a proveedor de identidad | Depende de Entra ID/AD y configuración corporativa; no se presume disponible en el único PC autorizado | No seleccionado como requisito; no añadir dependencia de nube/organización |

### Selección de diseño

La ruta a evaluar es **WebAuthn/FIDO2 mediante Windows WebAuthn API**, con `userVerification=required`, challenge aleatorio ligado al digest exacto de request/plan/manifiesto/alcance y validación estricta de RP ID, origin, credential ID, firma y flags. Para el primer prototipo se prefiere el Windows Hello platform authenticator; un FIDO2 externo es alternativa operativa separada, nunca un downgrade silencioso. La elección concreta del autenticador, RP ID, registro y política de attestation/hardware debe aprobarse y verificarse antes de una implementación real. Si no se puede demostrar UV/origin/credencial conforme a la política, se falla cerrado. La cuenta local Windows Hello no es evidencia suficiente por sí misma.

El parser estructural V4.7.2 limita `clientDataJSON` a `type`, `challenge`, `origin` y `crossOrigin=false` opcional; solo acepta `authenticatorData` básico de 37 bytes (RP-ID hash, flags y contador), flags UP/UV y BE/BS coherentes. No acepta AT/ED/reserved flags ni extensiones en esta versión. Firma, public key COSE y flags se cotejan/formatean pero no se verifican criptográficamente; por ello una envolvente que pasa no es prueba de autenticación ni una aprobación.

Los contratos de esta PR modelan únicamente aserciones y evidencias. Aunque una estructura sea válida, el resultado permanece `NO_VERIFICADO`; no se llama a la API Windows ni se acepta una respuesta de chat.

## Modelo futuro de identidad y separación

El registro futuro vinculará una identidad estable a `credential_id`, public key, RP ID, algoritmo y estado. Enrolamiento deberá ser una ceremonia separada que verifique quién controla la identidad; el nombre/ID del payload no basta. El assertion debe firmar el challenge y el hash canónico que cubre request, plan, manifiesto, decisión, versiones, dependencias, destinos, acciones y caducidad. Verificar una firma probaría posesión de la credencial registrada, no que el humano sea distinto del autor.

La política de dos personas debe comparar identidades autenticadas y rechazar autor=aprobador, incluso si se presentan credenciales distintas del mismo sujeto. En un equipo con un solo operador o una única cuenta controlada por una persona no puede prometerse separación humana real. El usuario deberá definir la identidad independiente/enrolamiento antes de activar esta política.

## Replay, revocación y auditoría futuros

- **Replay:** persistir `request_id` y hash del challenge con una restricción única y transacción/CAS atómico para la transición terminal. Rechazar concurrentes, reintentos, expirados y usados. El contador de WebAuthn puede ser cero o no global; no sustituye consumo único durable. V4.7.2 valida que el registro modelado coincida con la solicitud y simula estados en memoria; dos propuestas desde el mismo snapshot pueden competir, así que no previene replay real.
- **Revocación:** registro versionado por credencial/sujeto con fecha, motivo y actor autenticado; fallo cerrado para revocado/desconocido. Revocar debe invalidar solicitudes pendientes según política, conservar historia y volver a comprobar vigencia en el punto de consumo. V4.7.2 no posee un registro operativo.
- **Auditoría:** eventos mínimos con secuencia, hora observada, request/plan/manifest hashes, sujeto/credencial autenticados (cuando existan), decisión, motivo codificado, resultado y versión del verificador. No guardar payloads de componentes, secretos, material de clave ni contenido de proyectos. Una cadena de hashes puede detectar alteración accidental, pero un administrador que controla la base puede reescribir toda la cadena. V4.7.2 calcula/verifica eventos sintéticos y rechaza cadena vacía; no persiste ni promete inmutabilidad.
- **Recuperación y reloj:** definir altas, rotación, pérdida, recuperación, rollback de reloj y saltos de hora antes de activar. Recuperación debe revocar credential IDs previos y nunca aceptar chat/AutoApprove como sustituto. Hora local y estado local pueden ser manipulados por un administrador.
- **Preview/frescura:** regenerar el plan al presentar la aprobación y de nuevo antes de cualquier aplicación futura; verificar hash de cada fuente/destino en el punto de uso y fallar ante cambios concurrentes.

## Amenazas y riesgos residuales

| Amenaza | Requisito futuro | Residual en una sola PC |
| --- | --- | --- |
| Perfil de usuario, proceso o administrador local comprometido | Autenticador criptográfico, UI verificada, ACL, root de confianza y checks en cada paso | Un administrador con control del proceso/almacenamiento puede sustituir verificador/registro/log; no prometer resistencia total |
| Autor falsifica o aprueba su propio cambio | Identidad vinculada a credencial y política fija de sujeto distinto | Identidad declarada/credenciales distintas no prueban personas distintas |
| Replay/reintento/concurrencia/crash | Consumo durable y atómico con transiciones recuperables | El prototipo usa estados de memoria; no ofrece garantía operativa |
| Clave perdida/robada o revocada tarde | Enrolamiento, rotación, revocación y recovery con auditoría | Recuperación sin segundo factor crea un bypass; no hay proceso real implementado |
| Reloj atrasado y plan obsoleto/TOCTOU | Política de tiempo, preview fresco y comprobaciones de hash en el punto de consumo | El reloj y archivos locales pueden alterarse; sin bloqueo no hay snapshot transaccional |
| Manipulación/truncamiento de auditoría | Almacenamiento con ACL, encadenamiento y ancla independiente si el riesgo lo exige | El hash chain local no prueba no repudio ni resiste al administrador que puede reescribirlo |

## Referencias oficiales para la comparación

- [Windows WebAuthn API](https://learn.microsoft.com/windows/win32/webauthn/-webauthn-portal) — Win32 API, Windows Hello platform authenticator y FIDO2 external keys; Windows 10 1903+ / Windows 11.
- [WebAuthNAuthenticatorMakeCredential](https://learn.microsoft.com/windows/win32/api/webauthn/nf-webauthn-webauthnauthenticatormakecredential) y [WebAuthNAuthenticatorGetAssertion](https://learn.microsoft.com/windows/win32/api/webauthn/nf-webauthn-webauthnauthenticatorgetassertion) — creación de credencial/obtención de assertion, RP ID y sistema UI.
- [Windows Hello for Business overview](https://learn.microsoft.com/windows/security/identity-protection/hello-for-business/) — credenciales de clave pública y ámbito de cuentas; no extender sus garantías a login local sin verificación.
- [CNG Key Storage Providers](https://learn.microsoft.com/windows/win32/seccertenroll/cng-key-storage-providers) — distingue Microsoft Software KSP del Microsoft Platform Crypto Provider (TPM); un KSP de TPM protege una clave, pero no define por sí solo la ceremonia de aprobación humana.
- [Windows credential handling](https://learn.microsoft.com/windows/win32/secbp/handling-passwords) y [CryptProtectData / DPAPI](https://learn.microsoft.com/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata) — almacenamiento protegido de secretos, no autenticación de consentimiento.

## Verificación aislada prevista

Las pruebas V4.7.2 usan solamente claves ficticias/datos sintéticos, `TemporaryDirectory`, relojes inyectados, un modelo replay en memoria y auditoría hash-chain temporal. Deben comprobar mutación de challenge/scope/firma/flags, autor=aprobador, estado revocado, replay modelado, crash lógico de estados, alteración/reordenado de auditoría y snapshots sin escritura. Aun con todas las pruebas PASS, **no se acredita** WebAuthn real, autenticación humana, almacenamiento atómico durable, protección de revocación, hora confiable o seguridad frente a administrador local. Toda respuesta mantiene `approval_granted=false` y `apply_supported=false`.

Comando local de la suite aislada: `python -I -m unittest discover -s tests -p 'test_vx_approval_security_v472.py' -v`. La prueba de replay usa únicamente transiciones desde snapshots en memoria: dos propuestas concurrentes desde el mismo estado inicial pueden producir el mismo siguiente estado y esto demuestra explícitamente que no hay CAS/atomicidad implementada.
