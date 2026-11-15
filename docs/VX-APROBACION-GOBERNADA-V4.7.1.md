# VX Evolution V4.7.1 — contrato de solicitud de aprobación

**Estado:** contrato de solicitud y verificación estructural, sin autenticación fuerte ni operación de instalación. Depende de `vx-component-manifest/1` y `vx-publication-preview/1` de V4.7.0. V4.7.0 fue integrado en `main` mediante `36a73e01fe46d17573f46baf82cf8c88bf5d7559`; su CI Windows terminó PASS.

## Contratos versionados

`vx-approval-request/1` enlaza una solicitud a `plan_sha256`, `manifest_sha256`, la instantánea completa de `components` (versión, estado, dependencias y archivos) y `changes` (fuente, destino, acción y hashes source/current/proposed). Incluye `request_id`, `challenge`, `issued_at`, `expires_at` y un `request_sha256` calculado sobre el documento canónico excepto ese campo. Los hashes usan JSON UTF-8 normalizado con claves ordenadas y separadores compactos.

Los tiempos deben ser UTC RFC3339 exacto con sufijo `Z`, precisión de segundos y sin offset alternativo. `expires_at` debe ser posterior a `issued_at`; la vigencia máxima contractual es 24 horas. La validación compara solicitud, manifiesto normalizado y preview actual, recalcula hashes y rechaza expiración, campos incompletos/desconocidos/duplicados, tipos incorrectos, decisiones fuera del enum o cualquier diferencia de alcance.

`vx-approval-assertion/1` representa una afirmación no autenticada (`APPROVE` o `REJECT`) que referencia `request_id`, `challenge`, `request_sha256` y `responded_at`. Una coincidencia solo devuelve `MATCHED_AUTH_UNVERIFIED` o `REJECTION_AUTH_UNVERIFIED`, con `authentication=NO_VERIFICADA`, `approval_granted=false` y `apply_supported=false`. No se emite estado `APROBADO`, no se confía en respuesta de chat y no existe ruta a instalación.

Campos raíz cerrados de `vx-approval-request/1`: `schema`, `request_id` (UUIDv4 canónico), `challenge` (43 caracteres base64url), `issued_at`, `expires_at`, `request_state` (`PENDING`), `manifest_sha256`, `plan_sha256`, `components`, `changes` y `request_sha256`. Los tipos y estructuras de `components`/`changes` deben coincidir exactamente con el preview/manifiesto V4.7.0 actual. Campos raíz cerrados de `vx-approval-assertion/1`: `schema`, `request_id`, `challenge`, `request_sha256`, `decision` (`APPROVE` o `REJECT`) y `responded_at`; los campos de identidad/firma no forman parte de este esquema no autenticado.

## Garantías y límites de seguridad

- El verificador solo establece que la estructura es válida y que los hashes/alcance coinciden con manifiesto y preview suministrados, bajo el reloj y archivos observados durante la verificación.
- `request_sha256`, `plan_sha256`, `manifest_sha256`, el UUID y el challenge no autentican personas ni vuelven el objeto resistente a un atacante que pueda alterar y recalcular el documento.
- Los puntos de entrada que reciban JSON serializado deben decodificarlo con `strict_json_loads()` para rechazar claves repetidas y constantes no estándar. Las funciones de validación reciben objetos Python ya decodificados y no pueden recuperar claves duplicadas que un parser permisivo hubiera descartado.
- No hay identidad autenticada, firma criptográfica verificada, política de separación autor/aprobador, revocación, persistencia de decisiones ni almacenamiento de challenges consumidos. Autenticidad, no repudio y prevención de replay son **NO IMPLEMENTADOS**.
- No interpretar chat, `AutoApprove`, decisiones de reunión, identidad declarada, timestamp ni hash como consentimiento autenticado.
- La caducidad usa el reloj entregado al verificador; no es prueba de tiempo confiable. La validación no bloquea escrituras concurrentes ni garantiza una instantánea transaccional.
- La validación reconsiste los hashes y el alcance contra los objetos `preview`/`manifest` que recibe; no reabre fuentes ni destinos. El llamador debe regenerar el preview inmediatamente antes de verificar. Esta librería no puede certificar procedencia ni frescura por sí sola.
- La solicitud/verificación no escribe HOME, SQLite ni destinos administrados. V4.7.0 sigue informando `apply_supported=false`.

## Análisis de amenazas

| Amenaza | Control actual | Límite |
| --- | --- | --- |
| Alterar versión, dependencia, destino, acción o hash dentro de la solicitud | Digest de solicitud y comparación exacta contra manifiesto/preview actual | Un atacante que puede recalcular hashes no queda autenticado; los hashes no son firma |
| Incluir campos `approved`, `approver`, `signature` o contenido de chat | Esquemas cerrados rechazan campos extra; una aserción `APPROVE` válida conserva `approval_granted=false` | El sistema no autentica al humano ni valida firmas |
| Reutilizar solicitud/aserción | Challenge aleatorio por defecto, referencia exacta al request | Sin registro durable de consumos no hay prevención de replay ni uso único |
| Extender vigencia o forjar tiempos | UTC exacto, máximo 24h, rechazo si `now >= expires_at` o respuesta futura | `now` lo suministra el llamador; no hay reloj confiable ni evidencia temporal autenticada |
| Aprobar un preview obsoleto o datos concurrentemente cambiados | Comparar request con el preview y manifiesto suministrados | El módulo no regenera el preview ni bloquea cambios concurrentes; el llamador debe recalcular inmediatamente antes de verificar y una futura aplicación requiere guardas transaccionales |
| JSON ambiguo con claves duplicadas/NaN | `strict_json_loads()` rechaza duplicados y constantes no estándar | Todo consumidor de JSON serializado debe usar ese parser; los objetos Python ya parseados no revelan duplicados descartados antes |

## Requisitos obligatorios para una fase autenticada posterior

La fase futura debe seleccionar un autenticador criptográfico y raíz de confianza revisados; autenticar al humano y autorizar su rol; separar autor y aprobador; firmar exactamente el digest canónico de request/plan/manifiesto/alcance/expiración; gestionar claves (custodia, rotación, revocación); comprobar vigencia con política de reloj; consumir atómicamente `request_id`/challenge una sola vez en almacenamiento durable; registrar auditoría protegida contra alteración (request/plan hashes, identidad autenticada, decisión, timestamps y resultado del verificador, con acceso controlado y sin payloads innecesarios); regenerar el preview inmediatamente antes de cualquier futura aplicación; y fallar cerrado ante concurrencia o diferencias. Este contrato no implementa ni certifica dichos controles.

## Pruebas

La suite `tests/test_vx_approval_contract_v471.py` usa manifiestos y HOME sintéticos en `TemporaryDirectory`. Cubre esquema estricto, tiempos, expiración, alcance, hashes, mutaciones, aserciones de aprobación/rechazo no autenticadas e invariantes de no escritura. La validación estructural no autoriza instalación ni publicación.
