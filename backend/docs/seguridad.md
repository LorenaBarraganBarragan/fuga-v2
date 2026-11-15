# Arquitectura de Seguridad y Aislamiento de Datos — FUGA+

Documento de directrices de seguridad para el backend FastAPI y la base de datos Supabase PostgreSQL.

---

## 1. Principio Rector (RF-033 / HU-33)

**FastAPI es la única puerta de acceso a los datos financieros.** Los clientes móviles no pueden conectarse directamente a PostgreSQL ni ejecutar consultas arbitrarias.

### Regla de Oro de los Repositorios
> **TODO repositorio que acceda a tablas privadas (`gasto`, `fuga`, `fuga_evidencia`, `perfil`) DEBE heredar de `ScopedRepository` o exigir obligatoriamente un `usuario_id: UUID` en su inicialización.**

Bajo ninguna circunstancia se permite construir consultas SQL o ORM sin filtrar explícitamente por `usuario_id = :usuario_id`.
El backend utiliza una conexión privilegiada que omite RLS, por lo que **la seguridad a nivel de aplicación (application-level scoping) es la primera barrera y no puede relajarse**.

---

## 2. Derivación de Identidad

1. La identidad es emitida exclusivamente por **Supabase Auth**. FastAPI no emite tokens JWT propios (D-09).
2. El `usuario_id` del propietario se extrae **exclusivamente** del claim `sub` del token JWT verificado.
3. Cualquier `usuario_id` enviado en el cuerpo JSON, query params o headers de una petición es **ignorado o rechazado**.

---

## 3. Privacidad y Sanitización de Logs (RNF-007)

1. Prohibido registrar contraseñas, tokens JWT, valores monetarios (`monto_cop`), identificadores de sesión o datos personales sensibles.
2. `SensitiveFilter` en `app.core.logging` intercepta y enmascara recursivamente cualquier campo sensible con `[REDACTED]`.

---

## 4. Respuestas de Error Uniformes

1. Ante el intento de consultar o mutar un recurso que pertenece a otro usuario, la API devuelve `404 NOT_FOUND` uniforme para evitar enumeración de recursos.
2. Todo error incluye un `correlation_id` para trazabilidad sin comprometer datos confidenciales.
