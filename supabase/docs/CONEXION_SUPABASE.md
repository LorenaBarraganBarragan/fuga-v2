# Preparación del proyecto nuevo `fuga-plus`

Revisión local: 2026-11-16, America/Bogota. No se ejecutó SQL remoto ni se solicitaron secretos.

## Resultado

Las nueve migraciones se ejecutaron sobre PostgreSQL 16 local con una representación mínima de
`auth.users`, `auth.uid()` y roles del proveedor, y con privilegios iniciales permisivos como los de Supabase.
La suite completa pasa 165 pruebas, incluidas 14 de integración PostgreSQL.
Se verificó crear el esquema desde cero y reaplicar migraciones/seed conservando los datos de prueba.
Esto comprueba SQL e integración relacional; no certifica GoTrue, SMTP, JWT, PostgREST ni el proyecto remoto.

Los cambios locales corrigen:
- Objetos SQL explícitamente en `public`; extensiones compatibles en `extensions` sin mover las existentes.
- Triggers repetibles con `CREATE OR REPLACE TRIGGER` (PostgreSQL 14 o superior).
- `handle_new_user` con `SECURITY DEFINER`, `search_path` vacío y rol literal `usuario`.
- Perfiles para usuarios Auth anteriores a las migraciones, sin sobrescribir perfiles existentes.
- RLS en las diez tablas propias; catálogos de solo lectura para autenticados.
- Revocación de permisos generales y de columnas sensibles, incluidos TRUNCATE y creación de objetos del cliente.
- Perfil propio activo: solo nombres, apellido y teléfono pueden editarse directamente.
- Evidencia de fuga y gasto del mismo propietario; propietario inmutable.
- COP entero y rango existente, fecha mínima y rechazo de fechas futuras en Bogotá.
- Nombres opcionales de 2–80 caracteres, catálogo cerrado y parámetros de reglas inmutables por versión.

## Orden de aplicación

Para la primera aplicación al proyecto nuevo, usar los archivos locales revisados en este orden:

| Orden | Archivo en `supabase/migrations/` | Contenido |
|---|---|---|
| 1 | `0001_extensions.sql` | pgcrypto/citext y función de timestamps |
| 2 | `0002_catalogo.sql` | Categorías, reglas, versiones y datos iniciales |
| 3 | `0003_perfil.sql` | Perfil, FK a Auth, trigger y aprovisionamiento de usuarios previos |
| 4 | `0004_gasto.sql` | Gastos, restricciones, índices e idempotencia |
| 5 | `0005_fugas.sql` | Snapshots y evidencia |
| 6 | `0006_rls.sql` | RLS y políticas de perfiles/catálogos |
| 7 | `0007_grants.sql` | Permisos mínimos y revocaciones |
| 8 | `0008_integracion.sql` | Huellas/respuesta de idempotencia, auditoría, actividad y retención |
| 9 | `0009_seguridad_integridad.sql` | Refuerzo de integridad, fechas, propietario, versiones y permisos |

`supabase/seed.sql` es opcional: 0002 ya crea las nueve categorías y FUGA-01 1.0.
El seed no crea usuarios ni gastos ficticios. Reejecutarlo no duplica los datos iniciales.
`supabase/tests/verificar_esquema.sql` es una comprobación de solo lectura posterior a las migraciones.
`supabase/tests/rls_test.sql` conserva el mismo comprobador con el nombre anterior; basta ejecutar uno.

## Cómo aplicarlas cuando se autorice el remoto

1. Abrir el proyecto `fuga-plus` en el Dashboard y confirmar que sea el proyecto correcto.
2. Revisar las tablas existentes. Si existen tablas FUGA+ de una versión distinta, comparar primero el esquema:
   `IF NOT EXISTS` no convierte estructuras arbitrarias ni garantiza compatibilidad con versiones desconocidas.
3. En **SQL Editor**, ejecutar cada archivo completo, respetando el orden. Para una primera aplicación por
   SQL Editor, se puede envolver el contenido de cada archivo con `BEGIN;` y `COMMIT;` para confirmar su conjunto
   de forma atómica. Detenerse ante el primer error y revisar; no borrar datos para forzar el avance.
4. Completar 0001–0009 antes de habilitar el cliente. No pegar únicamente fragmentos de permisos o funciones.
5. Ejecutar `verificar_esquema.sql`; se espera una fila `OK: esquema, catálogo, permisos y denegación financiera directa`.
6. Después, verificar registro y sesión reales con dos cuentas propias de prueba desde la aplicación.

Ninguna migración borra filas, cuentas o tablas. Las restricciones nuevas se validan contra los datos existentes:
si son incompatibles, la migración falla para revisión manual sin intentar corregirlos ni eliminarlos.
Los triggers y políticas se reemplazan por nombre para hacer repetible su definición.

Si se prefiere Supabase CLI, usar un único historial de migraciones y revisar el plan antes de aplicar.
No mezclar una aplicación manual sin historial con `db push` suponiendo que CLI conoce esos cambios.
Los números 0001–0009 identifican el orden actual; no renumerar archivos después de aplicarlos.
No usar `db reset` sobre bases con datos que se quieran conservar.

## RLS: comportamiento esperado

| Objeto | Cliente sin sesión | Cliente autenticado |
|---|---|---|
| Categorías y reglas | Sin acceso | Lectura; sin escritura ni TRUNCATE |
| Perfil | Sin acceso | Solo propio y activo; edición limitada a nombres/apellido/teléfono |
| Gastos, fugas y evidencia | Sin acceso | Cero filas por lectura directa; escritura denegada |
| Auditoría, actividad y retención | Sin acceso | Sin acceso directo |

Los datos financieros se acceden exclusivamente por FastAPI, como exige DA-01.
El backend usa una conexión privilegiada: los filtros por propietario y las comprobaciones de rol/estado
siguen siendo obligatorios porque el propietario SQL o un rol BYPASSRLS puede omitir RLS.
Ver todas las filas desde el SQL Editor administrativo no demuestra que los clientes puedan verlas.

La FK del perfil referencia la clave primaria `auth.users.id`; no se crean ni reemplazan tablas del proveedor.
El registro nunca toma el rol desde metadatos editables. La desactivación es lógica; el borrado de una cuenta Auth
con datos dependientes puede quedar bloqueado por FKs, de acuerdo con la política de conservación.
No hay purga automática de datos reales ni se certifica la retención efectiva de respaldos del proveedor.

## Conectar FastAPI, sin compartir secretos en el chat

1. Copiar `backend/.env.example` a `backend/.env.local` y editarlo únicamente en la máquina local.
2. En **Connect**, copiar la cadena **Session pooler**, puerto 5432, si la red del computador es IPv4.
   El host depende del proyecto: no inventarlo a partir del nombre o la región.
3. Adaptar el prefijo a `postgresql+psycopg://`, conservar el usuario/host de Supabase y añadir `sslmode=require`.
   Codificar caracteres reservados de la contraseña en la URI (por ejemplo, `@` como `%40`).
4. Completar `SUPABASE_URL` con la URL real del proyecto. `fuga-plus` es el nombre visible, no el project ref.
   Issuer y JWKS se derivan de esa URL; eliminar/reemplazar los placeholders si se copió todo el ejemplo.
5. Mantener `SUPABASE_JWT_AUDIENCE=authenticated`. Verificar en Auth la clave de firma asimétrica RS256/ES256;
   el backend actual no acepta tokens HS256 ni tokens sin verificar.
6. Dejar `SUPABASE_SERVICE_ROLE_KEY` vacío hasta configurar administración. Si se utiliza, es secreto exclusivo
   del backend: no copiarlo al móvil, Git, capturas o chat.

Ejemplo de estructura, sin valores privados:
```dotenv
SUPABASE_URL=https://<project-ref>.supabase.co
SUPABASE_JWT_AUDIENCE=authenticated
DATABASE_URL=postgresql+psycopg://postgres.<project-ref>:<password-url-encoded>@<session-pooler-host>:5432/postgres?sslmode=require
```

Reiniciar FastAPI tras cambiar su entorno. `/health` comprueba el proceso y `/ready` debe responder 200 cuando
la conexión funcione. No basta con `/ready`: también deben comprobarse tablas, Auth y flujo de gastos.

## Conectar el móvil

En `mobile/.env.local`, guardar solo la URL pública y la clave **publishable/anon pública** del mismo proyecto:
```dotenv
EXPO_PUBLIC_SUPABASE_URL=https://<project-ref>.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=<publishable-o-anon-publica>
EXPO_PUBLIC_API_URL=http://<IP-WIFI-DEL-COMPUTADOR>:8000
```
No usar `localhost` como dirección del computador desde un celular físico.
Para que Android alcance FastAPI, iniciarlo en `--host 0.0.0.0` y permitir la conexión en la red privada.
Reiniciar Expo después de editar el entorno. Usar la IP Wi-Fi actual, no asumir que una IP anterior sigue vigente.

En Auth, configurar correo/contraseña con mínimo ocho caracteres y confirmación según el correo saliente disponible.
Registrar las redirecciones de la compilación nativa `fugaplus://auth` y `fugaplus://auth?flow=recovery`.
Expo Go no registra el esquema personalizado de la aplicación: los enlaces de confirmación, recuperación y OAuth
deben comprobarse en una compilación nativa o configurarse específicamente para el entorno de pruebas.
No habilitar las banderas de Google/recuperación hasta verificar los proveedores reales.

`supabase/config.toml` describe el entorno local de CLI; su `project_id=fuga-plus-dev` no enlaza ni configura
el proyecto remoto llamado `fuga-plus`. No se ejecutó `supabase link`, `db push`, ni SQL remoto en esta revisión.

## Evidencia y referencias

- Pruebas: `backend/tests/integration/test_migrations_security.py` y `test_full_flow.py`.
- Ronda final: 165 pruebas pasan, incluidas 14 PostgreSQL. Advertencia upstream de TestClient/httpx sin fallo.
- Se usó PostgreSQL local instalado, sin descargar un servidor ni usar Docker; el clúster se detiene al terminar.
- https://supabase.com/docs/guides/auth/managing-user-data
- https://supabase.com/docs/guides/database/postgres/row-level-security
- https://supabase.com/docs/guides/database/postgres/column-level-security
- https://supabase.com/docs/guides/database/connecting-to-postgres
