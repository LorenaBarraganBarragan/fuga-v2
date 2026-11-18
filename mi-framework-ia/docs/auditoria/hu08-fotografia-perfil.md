# HU-08 — Fotografía de perfil: implementación y prueba controlada

Fecha: 2026-11-18, America/Bogota. Prioridad aprobada: Should Have, fuera del MVP
obligatorio. Se conserva Expo/ImagePicker, FastAPI, PostgreSQL y Cloudinary con firma
de servidor. Sin instalaciones, commits, pushes ni despliegues.

## Resultado y límites

Implementación completada y flujo principal validado en Android QA con Cloudinary
real y perfil PostgreSQL local. Supabase PostgreSQL no recibió escrituras.
FastAPI carga las tres variables Cloudinary de backend/.env.local. Solo se emitieron
indicadores de presencia, nunca valores. GET /ping devolvió inicialmente 401; después
de la corrección manual de la propietaria devolvió **200**. Después de solicitar y
recibir autorización se subieron **solo los dos PNG sintéticos**. No hubo borrados
Cloudinary ni modificaciones de perfiles, tablas o datos financieros en Supabase.

**325 pruebas backend aprobadas y 97 frontend**, cero omisiones. TypeScript, Ruff
mínimo y mypy del dominio pasan. Cobertura Python app: 90 % redondeado; servicio
de fotografías: 94 %. Node: 93,33 % de líneas de los módulos medidos; profilePhoto.ts
100 %. Son coberturas con alcances distintos, no una cobertura E2E de Android.

El bundle Android se generó por Metro: HTTP 200, API QA correcta y controles de
confirmación presentes. La clave privada vigente, ya aceptada por Cloudinary, no
aparece en el bundle; tampoco su nombre de variable. Se verificó en memoria sin
guardar el bundle ni copiar credenciales. El APK debug anterior puede cargar este
JavaScript por Metro: no hay cambios nativos ni una nueva compilación APK en esta sesión.
La primera comprobación ADB falló en el entorno restringido y no permitió determinar
la conexión. Al repetirla fuera de esa restricción se verificó un Android autorizado,
se prepararon los reverse USB, se copiaron los PNG sintéticos a Descargas y se abrió el APK.

## Flujo implementado

1. ImagePicker selecciona JPEG/PNG/WebP de hasta **5.000.000 bytes**. Se rechazan
   metadatos de tipo/tamaño desconocidos; no se asume que cualquier archivo sea JPEG.
2. Se muestra una vista previa local. Confirmar permanece deshabilitado hasta que
   la imagen se pueda abrir. Cancelar antes de confirmar no solicita firma ni sube nada.
3. Confirmar pide POST /api/v1/me/photo/signature. FastAPI registra un intento
   privado, limita a diez firmas por usuario por hora y firma parámetros exactos.
4. El cliente envía directamente a Cloudinary solo archivo, API key pública de
   carga y parámetros firmados. La firma exige allowed_formats y overwrite=false;
   la clave secreta nunca sale del servidor.
5. POST /api/v1/me/photo/complete consulta los metadatos del activo en Cloudinary
   y valida propietario registrado, identificador exacto, tipo, formato, bytes,
   dimensiones y URL HTTPS de la cuenta configurada. No acepta una URL del cliente.
6. Una transacción serializada por perfil actualiza public.perfil.foto_url y el
   estado de las cargas. El repositorio y GET /me recuperan la foto tras otra sesión.

Los errores de archivo inválido son 400; tamaño excesivo, 413; proveedor/red, 503;
sin sesión, 401. El cuerpo de solicitud mal formado conserva la validación 422 del
framework. Una fotografía ajena o no autorizada se rechaza con 403. Los mensajes
no incluyen respuestas ni diagnósticos privados de Cloudinary.
La API key que acompaña una carga firmada es pública por diseño; el API secret no lo es.

Una respuesta de confirmación perdida se reintenta con el mismo activo sin otra
subida. Confirmar el activo ya vigente es idempotente; no se permite reactivar uno
retirado o cancelado. El cambio de cuenta o salida de pantalla interrumpe la carga;
un intento abandonado queda disponible para limpieza posterior.

## Persistencia y migración

Archivo nuevo: [0010_fotografias_perfil.sql](../../../supabase/migrations/0010_fotografias_perfil.sql).
Orden: **después de 0009_seguridad_integridad.sql**. Probado únicamente en bases
PostgreSQL locales desechables junto con las migraciones anteriores.

Añade public.perfil_foto_carga, con propietario FK al perfil, public_id único,
estados pendiente/activa/retirada/cancelada/eliminada, URL y marcas de tiempo.
Permite una sola carga activa por usuario. RLS habilitado, sin políticas ni grants
para anon/authenticated: solo acceso del backend. No cambia columnas ni URLs
existentes de perfil y no añade tablas o datos financieros.

El registro persistente permite reconocer cargas huérfanas después de cerrar la app
o reiniciar FastAPI. No basta una lista en memoria para garantizar esa limpieza.
La migración **no se aplicó en Supabase** y requerirá autorización independiente.
El proceso original del puerto 8000 no se reinició: para integrar allí fotografías
se necesitarán la migración autorizada y un reinicio que cargue las variables nuevas.
Actualizar frontend y backend conjuntamente: la carga debe enviar los nuevos campos
firmados; una versión antigua que los omita no puede usar la firma nueva.

## Fotografías anteriores y cargas huérfanas

La foto anterior se conserva hasta terminar la confirmación. Al sustituirla, su
registro pasa a retirada; nunca se borra la anterior antes de guardar la nueva URL.
Cancelar una carga pendiente la marca cancelada; una cancelación tardía no deshace
una confirmación ya completada.

[cleanup_profile_photos.py](../../../backend/scripts/cleanup_profile_photos.py) ofrece
un **dry-run por defecto** y borrado solo con --apply. Examina como máximo 50 candidatos
por ejecución (límite configurable hasta 100) y espera dos horas desde el último estado:
las firmas Cloudinary son válidas una hora y no deben poder recrear un activo ya limpiado.

Antes del borrado vuelve a bloquear el perfil y el registro, verifica la propiedad
y el estado, y excluye la foto actual y URLs referenciadas por otros perfiles.
Solo elimina identificadores exactos que el propio backend registró; no enumera ni
borra carpetas de Cloudinary. Un fallo conserva el registro para reintentar. Usa
invalidate=true al destruir el activo; la propagación de caché depende del proveedor.
Se conservan los registros eliminados como control contra reactivaciones.

**Fotos antiguas sin registro y fotos Google se conservan:** no se infiere un permiso
de borrado a partir de una URL. La futura purga definitiva de cuentas deberá coordinar
primero la limpieza de sus activos registrados; no se cambió aquí la retención de cuentas.
No se instaló ni activó un cron o worker. La limpieza es una tarea operativa explícita.

## Ensayo Android seguro

Se preparó un segundo entorno; no se cambió ni vació el QA anterior del puerto 18000.
Este último conserva sus seis gastos ficticios y continúa bloqueando fotografías.

- **FastAPI fotos:** http://127.0.0.1:18001, escucha solo loopback.
- **Metro fotos:** localhost:8084, con únicamente variables públicas del móvil.
- **Datos:** base nueva fuga_android_qa_* en PostgreSQL local 127.0.0.1:55440.
- **Identidad:** Supabase Auth real; reutilizar únicamente la cuenta ficticia existente.
- **Imágenes:** Cloudinary real, pendiente de autorización; PostgreSQL Supabase no se usa.

El launcher lee del dotenv de servidor exclusivamente las tres variables Cloudinary;
no hereda DATABASE_URL ni la clave administrativa Supabase. Mantiene la validación
JWT/JWKS original, fija la primera identidad ficticia validada y crea su perfil solo
en la base local. Admin, foto Google y desactivación siguen bloqueados. Solo habilita
signature, complete y cancel. No hay bypass de autenticación.

Los procesos de fotos quedaron preparados en esta sesión. Si se reinician:

```powershell
# Requiere el clúster local ya preparado, no una conexión Supabase.
backend/.venv/Scripts/python -B backend/scripts/qa_android.py --photos
node mobile/scripts/android-qa.cjs metro-photos
```

Después de **autorizar la prueba y conectar el teléfono**:

```powershell
.tools/android-sdk/platform-tools/adb.exe reverse tcp:18001 tcp:18001
.tools/android-sdk/platform-tools/adb.exe reverse tcp:8081 tcp:8084
.tools/android-sdk/platform-tools/adb.exe push mobile/tests/fixtures/profile-qa-a.png /sdcard/Download/fugaplus-hu08-qa-a.png
.tools/android-sdk/platform-tools/adb.exe push mobile/tests/fixtures/profile-qa-b.png /sdcard/Download/fugaplus-hu08-qa-b.png
.tools/android-sdk/platform-tools/adb.exe shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/Download/fugaplus-hu08-qa-a.png
.tools/android-sdk/platform-tools/adb.exe shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/Download/fugaplus-hu08-qa-b.png
```

Reabrir/recargar el APK debug para conectar Metro 8084. Si pide acceso, introducir
la contraseña solo en el teléfono. Este es un entorno local vacío distinto del QA
financiero anterior: no esperar ver allí sus gastos. No usar cuentas personales.

Los dos PNG de cuadros de colores son sintéticos, sin caras, EXIF ni información
personal. Cambiar la fotografía de la cuenta ficticia desde este entorno guarda la
URL en **el perfil local**, no en el perfil remoto. Sí crea activos reales Cloudinary;
por ello la prueba requiere autorización previa incluso con imágenes sintéticas.

La propietaria autorizó expresamente las dos cargas sintéticas, cierre/nuevo inicio
de sesión de la cuenta ficticia y persistencia solo local. No autorizó borrados
Cloudinary en esta fase. Se solicitaron las comprobaciones físicas de vista previa,
cancelación y primera carga; no se presuponen exitosas por la autorización.

Resultado físico inicial: la propietaria confirmó vista previa y cancelación sin
cambiar la foto. La primera confirmación falló antes de llegar a /photo/complete;
el perfil local seguía sin foto y los intentos consultados en Cloudinary devolvían
404. El reloj del servidor y el del teléfono coinciden con el proveedor. Se añadió
diagnóstico seguro para distinguir fallo de Internet de rechazo HTTP sin mostrar
el cuerpo privado del proveedor y se preparó el reintento controlado.

Se reprodujo una incompatibilidad local con **Expo 58**: su fetch global usa
convertFormDataAsync y rechaza la parte de archivo antigua {uri,name,type}, aunque
sea válida para el fetch histórico de React Native. La conversión falla antes de
contactar con Cloudinary y termina mostrando un error genérico de red.
Se cambió únicamente la parte nativa a File de expo-file-system, cuya interfaz
bytes()/Blob sí acepta ese serializador. Una regresión ejecuta el serializador
real del SDK instalado, reproduce el rechazo antiguo y verifica los bytes PNG nuevos.
Web conserva su Blob. No se activó una bandera global ni se cambió fetch en otras funciones.

expo-file-system 58.0.13 ya estaba instalado como dependencia de Expo y presente
en los DEX del APK. Se declaró ahora como dependencia directa de la aplicación,
sin instalación ni cambio de versión, para no depender de una importación transitiva.
La compatibilidad de API nativa se comprobó sin recompilar el APK.

**Cierre de la prueba real:** después de esa corrección la propietaria confirmó
la foto A visible, su persistencia tras cerrar/iniciar sesión, cancelación de B
conservando A y sustitución por B al confirmar. SELECT local verifica que foto_url
coincide con el registro activo de B. GET de metadatos y del CDN verifica ambos
PNG de 128×128 y 385/384 bytes, con SHA-256 idéntico a las dos imágenes sintéticas.
Tres intentos anteriores no crearon imágenes: sus consultas específicas son 404.
Estado local final: una activa, una retirada, dos pendientes y una cancelada.
La foto A sigue conservada en Cloudinary; no se probó ni autorizó su borrado.
El QA financiero anterior conserva sus seis gastos y COP 28.000 sin cambios.

| Prueba manual | Resultado esperado / observado |
|---|---|
| Seleccionar A y cancelar | Confirmado por la propietaria: vista previa y perfil conservado |
| Seleccionar A y confirmar | Confirmado físicamente y por SELECT/Cloudinary: foto A y URL local |
| Cerrar sesión e iniciar con la misma cuenta | Confirmado por la propietaria: foto A permanece |
| Seleccionar B y cancelar | Confirmado por la propietaria: foto A permanece |
| Seleccionar B y confirmar | Confirmado por la propietaria y metadatos: foto B activa, A retirada |
| Interrumpir red/reintentar | Automatizado; no se simuló físicamente una interrupción después de cargar A |
| Rechazar permiso o usar archivo inválido | Automatizado; queda la comprobación física adicional |

El cierre de sesión puede revocar la sesión de Auth real. Debe autorizarse junto
con el nuevo inicio de sesión; no crea usuarios ni cambia perfiles remotos.
No se ejecuta todavía limpieza real. Después de dos horas, bajo autorización
separada del borrado de los activos de ensayo:

```powershell
# Primero: solo SELECT sobre la base local; sin llamadas Cloudinary.
backend/.venv/Scripts/python -B backend/scripts/cleanup_profile_photos.py --qa-local
# Solo tras revisar el dry-run y autorizar el borrado de prueba:
backend/.venv/Scripts/python -B backend/scripts/cleanup_profile_photos.py --qa-local --apply
```

La limpieza de QA utiliza exclusivamente el nombre validado de su base local
registrado por el launcher, nunca DATABASE_URL de backend/.env.local.
Conservar FastAPI activo hasta terminar la prueba de persistencia y revisar la
limpieza; su base es desechable. Al volver al QA financiero, restablecer:

```powershell
.tools/android-sdk/platform-tools/adb.exe reverse tcp:8081 tcp:8083
```

## Evidencia y pruebas

[Evidencia HU-08](evidencia-hu08-fotografia.json). Proveedores simulados y PostgreSQL
local en toda la suite: las pruebas no utilizan las credenciales o sesiones del móvil.
Pruebas nuevas: 24 backend y 11 frontend, además de las suites existentes.

| Criterio HU-08 | Evidencia automatizada | Estado físico |
|---|---|---|
| CA-08.1 Vista previa/confirmar/cancelar | Componente real Profile con controles nativos simulados | Vista previa y cancelación confirmadas por la propietaria |
| CA-08.2 Asociación y persistencia | Rutas reales, SELECT perfil local y JWT nuevo de misma identidad | Login/logout, foto A persistente y sustitución por B confirmados |
| CA-08.3 Tipo/tamaño/corrupto | Frontera 5 MB, metadatos proveedor, vista previa dañada, 400/413 | Dos PNG válidos confirmados; inválidos/tamaño quedan como casos físicos adicionales |
| CA-08.4 Error/reintento | Fallo proveedor 503, URL previa intacta, reintento idempotente, sin segunda subida | Fallo inicial de serialización diagnosticado/corregido; interrupción de red tras A no simulada |
| CA-08.5 Otra cuenta | Registro de propietario, identificadores ajenos rechazados, RLS/grants y concurrencia | Cubierto local; sin manipulación de cuentas reales |

Archivos de implementación: frontend Profile.tsx y lib/profilePhoto.ts; backend
api/v1/me.py, services/profile_photos.py y filtro logging.py; migración 0010;
cleanup_profile_photos.py; launchers QA y pruebas HU-08/QA. Los dos PNG de prueba
están en mobile/tests/fixtures. No se modificaron gastos, reglas, umbrales ni credenciales.

Referencias oficiales consultadas (Context7 no estaba disponible en esta sesión):
[firmas Cloudinary](https://cloudinary.com/documentation/authentication_signatures),
[carga y destrucción](https://cloudinary.com/documentation/image_upload_api_reference),
[ping de solo lectura](https://cloudinary.com/documentation/admin_api#ping) e
[ImagePicker SDK 58](https://docs.expo.dev/versions/latest/sdk/imagepicker/).

## Archivos de esta actividad

No incluye los cambios anteriores del plan de mejora. Los .env.local se conservaron sin escrituras del agente.

- [backend/app/api/v1/me.py](../../../backend/app/api/v1/me.py)
- [backend/app/core/logging.py](../../../backend/app/core/logging.py)
- [backend/app/services/profile_photos.py](../../../backend/app/services/profile_photos.py)
- [backend/scripts/cleanup_profile_photos.py](../../../backend/scripts/cleanup_profile_photos.py)
- [backend/scripts/qa_android.py](../../../backend/scripts/qa_android.py)
- [backend/tests/integration/test_android_qa.py](../../../backend/tests/integration/test_android_qa.py)
- [backend/tests/integration/test_profile_photos_hu08.py](../../../backend/tests/integration/test_profile_photos_hu08.py)
- [backend/tests/unit/api/test_profile_photos_hu08.py](../../../backend/tests/unit/api/test_profile_photos_hu08.py)
- [mobile/src/screens/Profile.tsx](../../../mobile/src/screens/Profile.tsx)
- [mobile/src/lib/profilePhoto.ts](../../../mobile/src/lib/profilePhoto.ts)
- [mobile/scripts/android-qa.cjs](../../../mobile/scripts/android-qa.cjs)
- [mobile/tests/android-qa.test.cjs](../../../mobile/tests/android-qa.test.cjs)
- [mobile/tests/profile-photo.test.cjs](../../../mobile/tests/profile-photo.test.cjs)
- [mobile/tests/fixtures/profile-qa-a.png](../../../mobile/tests/fixtures/profile-qa-a.png)
- [mobile/tests/fixtures/profile-qa-b.png](../../../mobile/tests/fixtures/profile-qa-b.png)
- [supabase/migrations/0010_fotografias_perfil.sql](../../../supabase/migrations/0010_fotografias_perfil.sql)
- [supabase/docs/CONEXION_SUPABASE.md](../../../supabase/docs/CONEXION_SUPABASE.md)
- [README.md](../../../README.md)
- [mi-framework-ia/docs/planificacion/PROGRESO_BUILD.md](../../../mi-framework-ia/docs/planificacion/PROGRESO_BUILD.md)
- [mi-framework-ia/docs/auditoria/ejecucion-plan-mejora-fugaplus.md](../../../mi-framework-ia/docs/auditoria/ejecucion-plan-mejora-fugaplus.md)
- [mi-framework-ia/docs/auditoria/hu08-fotografia-perfil.md](../../../mi-framework-ia/docs/auditoria/hu08-fotografia-perfil.md)
- [mi-framework-ia/docs/auditoria/evidencia-hu08-fotografia.json](../../../mi-framework-ia/docs/auditoria/evidencia-hu08-fotografia.json)
- [mi-framework-ia/docs/auditoria/inventario-candidato.json](../../../mi-framework-ia/docs/auditoria/inventario-candidato.json)
- [mobile/package.json](../../../mobile/package.json)
- [mobile/package-lock.json](../../../mobile/package-lock.json)
