# QA administrativo local de FUGA+

Preparado el 2026-11-18, America/Bogota. **La prueba manual del Xiaomi no se inició.**
No se cambiaron los puertos USB ni se inició el servidor administrativo o su Metro.

## Separación del entorno financiero

| Recurso | QA financiero existente | QA administrativo preparado |
|---|---|---|
| FastAPI | 127.0.0.1:18000 | 127.0.0.1:18002 |
| Metro | 8086 | 8087 |
| Base PostgreSQL | La que conserva el proceso financiero | Nueva `fuga_admin_qa_<uuid>` por ejecución |
| Identidad | Cuenta ficticia existente en Supabase Auth | Auth simulado local, sin Supabase remoto |
| Sesión móvil | Espacio de almacenamiento actual | Espacio distinto, derivado del origen ficticio |

Se reutiliza exclusivamente el clúster local de QA en 127.0.0.1:55440. El lanzador
no admite DSN, cuentas, host o puerto por argumentos y no lee dotenv. Crea y elimina
únicamente la base aleatoria que le pertenece; no reutiliza ni elimina la financiera.
Las migraciones existentes se aplican solo a esa base nueva, sin cambios de SQL.

## Autenticación y autorización

El mismo formulario de Access y el SDK real de Supabase realizan el inicio de sesión.
Solo en modo QA debug, un adaptador redirige las rutas Auth permitidas desde
`https://admin-qa.invalid` hacia el simulador loopback. Ese dominio es ficticio y
no recibe conexiones. No se modificó la validación HTTPS habitual del cliente.
Se rechazan registro, OAuth, recuperación, destinos distintos y redirecciones HTTP.

El proveedor local implementa contraseña, renovación rotativa, consulta de usuario,
cierre de sesión, JWKS y bloqueo/reactivación de las cuentas ficticias. Genera una
clave RSA efímera y tokens RS256 con emisor local, audiencia authenticated, expiración
y kid. La clave de firma y la clave administrativa ficticia permanecen en memoria.
La clave pública de cliente es sintética; no concede permisos administrativos.

FastAPI usa sus routers y verificaciones originales: firma, emisor, audiencia,
expiración, estado persistido y rol de public.perfil. Solo se inyecta la conexión
a la base local; no se reemplazan get_token_claims, get_current_user, require_admin
ni require_user. Los metadatos del token no asignan el rol de aplicación.

accounts_service sigue ejecutando su flujo original, incluida la auditoría y las
tareas locales de retención. Su llamada administrativa por apikey tiene como único
destino el proveedor simulado de este proceso. Este rechaza identidades ajenas a
sus fixtures y protege al administrador. Desactivar bloquea el acceso existente;
reactivar permite un nuevo inicio de sesión. No se borran gastos.

El proceso solo escucha en loopback y bloquea conexiones externas y DNS externo.
No admite solicitudes con Origin de navegador ni un Host distinto del loopback.
Fotografías y autodesactivación quedan fuera de este ensayo. No hay credenciales
reales ni llamadas a Supabase, Cloudinary u otros proveedores.

## Bloqueos de producción

- El backend requiere APP_ENV=test, FUGA_ADMIN_QA=1 y FUGA_LOAD_DOTENV=0. Su CLI
  rechaza un proceso marcado como producción o release antes de crear la base.
- El lanzador móvil construye un entorno permitido desde cero, sin leer archivos
  dotenv ni heredar claves, URLs reales o proxies. Solo inicia Metro debug local.
- La configuración de Expo rechaza el modo QA en release/production o si se mezcla
  con otra URL o clave. El cliente también rechaza su activación cuando __DEV__ es falso.
- Se exportó un bundle Android de producción con configuración pública sintética:
  su mapa de fuentes y su código no incluyen adminQaAuth.ts ni el adaptador.
- La exportación debug de QA sí incluye el adaptador y la configuración ficticia.
  Ambas exportaciones fueron comprobaciones locales, sin despliegue ni instalación.
- El paquete Python de producción contiene app; el simulador está en scripts y
  no se importa desde la aplicación ni desde su lanzador normal.

## Datos de prueba y acceso

Al iniciar el CLI se generan 27 cuentas ficticias: un administrador y 26 usuarios.
Inicialmente hay 19 cuentas activas y 8 inactivas; se cargan tres meses de actividad
para revisar el gráfico. El listado permite probar dos páginas, búsquedas y filtros.
No hay datos financieros de personas reales ni datos del QA financiero existente.

La contraseña se genera aleatoriamente para cada ejecución. El acceso administrativo
se guarda solo mientras corre el ensayo en **.tools/admin-qa/login.local.json**,
carpeta ignorada por Git. Abrir ese archivo localmente cuando llegue el momento y
escribir los datos solo en el teléfono. No compartir ni copiar su contenido a logs,
documentación o chat. Todavía no se generó ese archivo para la prueba manual.

La misma contraseña ficticia permite iniciar sesión con los usuarios locales activos
para comprobar denegaciones por rol; sus correos aparecen en el listado ficticio.
Ninguno de estos accesos sirve en Supabase remoto.

Una segunda ejecución simultánea se rechaza mediante run.lock antes de sobrescribir
el acceso local. Si el proceso termina de forma abrupta y deja ese bloqueo, comprobar
primero que no quede un proceso administrativo activo; no borrar archivos de otros QA.

## Inicio manual posterior, paso por paso

Estos comandos **no se ejecutaron para iniciar la prueba manual**. Se utilizarán
después de que la propietaria revise los resultados, desde la raíz del repositorio.
El clúster PostgreSQL QA existente debe seguir activo. No detener FastAPI 18000.

1. Terminal independiente, iniciar exclusivamente el QA administrativo:

   ```powershell
   backend/.venv/Scripts/python.exe -B backend/scripts/qa_admin_android.py
   ```

2. Otra terminal, comprobar la configuración ficticia y luego iniciar su Metro:

   ```powershell
   node mobile/scripts/admin-qa.cjs check
   node mobile/scripts/admin-qa.cjs metro
   ```

3. Cuando ambos estén listos, agregar el puerto administrativo y cambiar
   temporalmente el destino de Metro para el APK debug existente:

   ```powershell
   .tools/android-sdk/platform-tools/adb.exe reverse tcp:18002 tcp:18002
   .tools/android-sdk/platform-tools/adb.exe reverse tcp:8081 tcp:8087
   ```

4. Reabrir FUGA+ sin borrar sus datos. Debe aparecer el formulario habitual de
   acceso con el almacenamiento separado de QA. No cerrar la sesión real desde
   el entorno financiero ni desinstalar el APK. Introducir el acceso ficticio local.

5. Recorrer Cuentas → búsqueda → Activas/Inactivas → Buscar/actualizar → páginas →
   Ver cuenta → Volver al listado → Sesión → Cuentas. Los filtros se aplican al
   pulsar Buscar/actualizar. Comprobar cifras y gráfico mensual.

6. Desactivar y reactivar únicamente una cuenta marcada como ficticia. Confirmar
   explícitamente cada operación. El administrador no permite su propia desactivación.

7. Revisar hora, cámara, batería, señal y navegación inferior; abrir el teclado en
   Buscar por nombre o correo y desplazarse hasta los controles. App conserva el
   contenedor medido PublicSafeArea, sin nuevos márgenes ni cambios de diseño.

No se necesita recompilar código nativo: el APK debug existente ya tiene el módulo
de insets. Los cambios de JavaScript se cargarán desde el Metro administrativo.

Para regresar al QA financiero, sin detener sus servicios:

```powershell
.tools/android-sdk/platform-tools/adb.exe reverse tcp:8081 tcp:8086
```

Reabrir el APK. La sesión financiera conserva su almacenamiento independiente.
Solo cuando termine el ensayo administrativo se detendrá su propio CLI; ese cierre
elimina su base desechable y el archivo de acceso, no la base financiera.

## Validación automatizada

Comandos utilizados con red externa y dotenv reales deshabilitados por test_safe:

```powershell
$env:FUGA_TEST_DATABASE_URL='postgresql://fuga_test@127.0.0.1:55440/postgres'
backend/.venv/Scripts/python.exe -B backend/scripts/test_safe.py --integration
```

Desde mobile:

```powershell
npm.cmd run typecheck
npm.cmd test
```

Resultados: **346 pruebas backend aprobadas, 124 frontend aprobadas, TypeScript
aprobado y Ruff (F/E9/I) aprobado**. Cero fallos y cero omitidas. Son 21 casos nuevos
de backend y 6 de frontend. La advertencia de deprecación de TestClient es de la
dependencia existente; no se instalaron ni cambiaron dependencias.

El QA financiero conservó sus seis gastos ficticios por COP 28.000 y una fuga.
Sus contadores de operaciones de escritura no cambiaron. FastAPI financiero 18000,
el QA fotográfico 18001 y Metro 8086 respondieron correctamente al finalizar.
Los puertos administrativos 18002/8087 permanecen sin servicio y no se generó el
archivo de acceso de la prueba manual. El staging conserva el mismo contenido.

Evidencia local ignorada: .verification/admin-qa/evidence.json y release-evidence.json.
Las pruebas nuevas cubren:

- Guards de QA/release, red externa, configuración mixta y segundo lanzador.
- JWT firmado y JWKS servido por HTTP loopback, sin saltarse la validación real.
- SDK real contra el simulador, incluyendo contraseña, perfil, renovación y logout.
- Listado, búsqueda, filtros, dos páginas, detalle, estadísticas y auditoría.
- Usuario sin permisos administrativos y administrador sin acceso a finanzas.
- Metadatos que intentan forzar rol y tokens con firma/algoritmo, audiencia, emisor
  o expiración no válidos.
- Bloqueo/reactivación local, rechazo de sesiones deshabilitadas, retención local
  y protección del administrador.
- Pantalla Admin real con API simulada: búsqueda/filtro, detalle y confirmación
  obligatoria antes de cambiar estado.
- Opciones de autenticación de producción conservadas y guard runtime de debug.

Los servidores temporales de las pruebas se cerraron automáticamente. No se
iniciaron los servicios permanentes 18002/8087 ni se utilizó el Xiaomi.
La verificación visual administrativa de barras y teclado sigue pendiente.

Archivos de aplicación cambiados: src/lib/supabase.ts y scripts/check-public-env.cjs.
Los restantes archivos de esta tarea son el adaptador, los lanzadores QA, las pruebas
y este documento. No se modificaron Access, AuthProvider, App, Admin, backend/app,
las migraciones, las configuraciones dotenv ni el staging previo.
