# APK release local de FUGA+

Preparación del 2026-11-19, America/Bogota. **No se ejecutó assembleRelease ni se
generó un APK en esta tarea. Falta que la propietaria cree sus credenciales de firma.**

## Proceso preparado

El punto de entrada es `scripts/android-release.ps1`. Su lanzador Node:

1. Lee exclusivamente mobile/.env.local y admite solo API URL, URL/clave pública
   Supabase y los indicadores públicos de Google, recuperación y QA administrativo.
2. Exige las tres variables públicas esenciales. Rechaza claves privadas, variables
   ajenas, URLs no HTTPS, destinos locales y dominios ficticios de QA.
3. Rechaza QA administrativo habilitado en el archivo y construye un entorno limpio
   con EXPO_PUBLIC_ADMIN_QA_MODE=false, FUGA_RELEASE_BUILD=1 y NODE_ENV=production.
   No hereda secretos, configuración del simulador ni EXPO_NO_CLIENT_ENV_VARS.
4. Desactiva la lectura automática de dotenv. No carga backend/.env.local.
5. Sincroniza las fuentes con C:\fuga-plus-build-bd5fcedc\mobile y compara sus hashes.
   Excluye dotenv, keystores, claves, dependencias y directorios nativos generados.
   No instala dependencias; si el lock no coincide, se detiene para revisión.
6. Conserva la firma propia mediante un config plugin de Expo: un futuro prebuild
   vuelve a aplicarla. Debug conserva su configuración; release no vuelve a debug.
7. Solo al solicitar Apk comprueba el keystore, alias, contraseña y certificado,
   y llama al script Android existente. Ese script mantiene FUGA_RELEASE_BUILD=1.

La firma utiliza variables de proceso FUGA_ANDROID_*, sin prefijo EXPO_PUBLIC_.
Gradle las lee sin incorporarlas a BuildConfig ni al JavaScript. PowerShell pide
las contraseñas mediante SecureString, no las pone en argumentos y restaura el
entorno al terminar. Los logs del proceso hijo filtran contraseñas y configuración
pública. No se guarda un archivo de contraseñas.

La comprobación del certificado rechaza la identidad Android Debug y certificados
fuera de vigencia. La validación definitiva de la contraseña de la entrada privada
se realizará por Gradle al firmar; todavía no hay credenciales para probarla.

Se mantienen **co.edu.fugaplus.app**, versión **0.1.0** y versionCode **1**. El script
existente genera arm64-v8a, compatible con el Xiaomi utilizado en QA. Cambiar de
firma respecto al APK debug puede impedir actualizarlo directamente; no desinstalar
ni borrar datos automáticamente para resolver esa incompatibilidad.

## Paso pendiente de la propietaria: crear la firma

Ejecutar personalmente desde la raíz del repositorio, en una terminal local:

```powershell
New-Item -ItemType Directory -Force .\.tools\android-release-signing | Out-Null
& .\.tools\jdk17\bin\keytool.exe -genkeypair -v -storetype PKCS12 -keystore .\.tools\android-release-signing\fugaplus-release.keystore -alias fugaplus-release -keyalg RSA -keysize 3072 -validity 10000 -dname "CN=FUGA+, OU=Android, O=FUGA+, C=CO"
```

Keytool solicitará una contraseña nueva y su confirmación en la terminal. No escribir
la contraseña en el comando, un archivo del proyecto ni el chat. PKCS12 utiliza la
misma contraseña para la clave y el almacén en este procedimiento.

La carpeta .tools y los archivos *.keystore ya están ignorados por Git. El lanzador
no copia el keystore a la carpeta de compilación. Conservar una copia protegida y
la contraseña en un gestor seguro: se necesitarán para futuras actualizaciones.
No ejecutar ese comando sobre un keystore existente para reemplazarlo sin revisión.

La tarea de preparación no creó esta clave ni solicitó su contraseña.

## Comandos disponibles

Comprobar configuración sin pedir contraseñas ni compilar:

```powershell
powershell -NoProfile -File .\mobile\scripts\android-release.ps1 -Task Check
```

Sincronizar la copia y preparar Gradle, sin compilar ni necesitar la clave:

```powershell
powershell -NoProfile -File .\mobile\scripts\android-release.ps1 -Task Prepare
```

**Solo después de crear el keystore y autorizar la compilación**, generar el APK:

```powershell
powershell -NoProfile -File .\mobile\scripts\android-release.ps1 -Task Apk
```

El lanzador preguntará la contraseña del almacén y la de la clave. Con el PKCS12
anterior, pulsar Enter en la segunda pregunta para utilizar la misma contraseña.
El comando Apk aún no se ejecutó.

Salida esperada:

```text
C:\fuga-plus-build-bd5fcedc\mobile\android\app\build\outputs\apk\release\app-release.apk
```

No utilizar android-qa.cjs, admin-qa.cjs o welcome-preview.cjs para este APK. La llamada
directa antigua a android-local.ps1 -Task Apk ahora exige el entorno preparado por
el nuevo lanzador, para evitar APK sin configuración o con firma debug accidental.

## Independencia del equipo

El APK release incluye JavaScript y utiliza los endpoints HTTPS públicos configurados.
No requiere Metro en ejecución, USB, FastAPI QA ni PostgreSQL local para funcionar.
Sí necesita Internet para Supabase y Render. Metro sigue siendo el empaquetador
interno utilizado al compilar JavaScript; no será un servidor requerido por el APK.
El script Android no consulta ADB durante la tarea Apk ni instala el resultado.

Después de compilar y de acordar la instalación, comprobar el APK con USB desconectado
y Metro apagado: acceso, dashboard, registro, historial, fugas, voz, recordatorios,
fotografía y barras del sistema. Esta validación del APK firmado sigue pendiente.

## Verificaciones realizadas

- **TypeScript aprobado y 132 pruebas frontend aprobadas**, incluidos ocho casos
  nuevos de preparación release; cero fallos y cero omitidas.
- Sintaxis de los dos scripts PowerShell, sin ejecutarlos en modo Apk.
- Entorno público real válido, modo QA desactivado y firma todavía pendiente.
- Sincronización de 56 archivos por hash; sin dotenv ni keystore copiados.
- Plugin real de Expo evaluado en pruebas, persistencia de firma y transformación
  idempotente que conserva la firma debug exclusivamente en su variante.
- Pruebas de rechazo de secretos, destinos locales, copia enlazada, dependencias
  desactualizadas, credenciales ausentes y contraseñas en argumentos de keytool.
- Exportación de JavaScript Android en modo producción con las variables públicas
  actuales: API y clave pública incorporadas, adaptador administrativo excluido del
  código y del mapa de fuentes. No es un APK ni una instalación.
- Gradle `help --offline`: **BUILD SUCCESSFUL**, 29 tareas (1 ejecutada, 28 actualizadas).
  Confirma que la configuración nativa y la firma declarada son válidas sintácticamente.
  No ejecuta tareas de empaquetado release ni comprueba una clave todavía inexistente.

Evidencia local en .verification/release-preparation/. No contiene contraseñas.
No se modificaron backend, Supabase, Render, el paquete, la versión ni las dependencias.
No se hicieron commits, pushes, despliegues ni cambios al staging.
