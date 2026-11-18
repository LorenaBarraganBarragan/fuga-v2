# Compilación y validación Android local

ACT-02/03/15, sin EAS, publicación ni cambios remotos. Expo Go no incluye FugaVoice.
La prueba automática del config plugin comprueba micrófono permitido y cámara bloqueada.
El prebuild conserva esquema fugaplus e integra el manifiesto del módulo Kotlin.

## Herramientas

Usar Node compatible con Expo 58, JDK **17** compatible con Gradle 9.4.1 y Android SDK.
El JDK 23 del sistema no satisface la toolchain 17 solicitada por los plugins; el
script prefiere el JDK 17 local de .tools/jdk17, sin modificar Java del sistema.
El catálogo instalado de React Native 0.88.1 solicita compileSdk 37, build-tools 37.0.0
y NDK 27.1.12297006; el gestor oficial denomina la plataforma `platforms;android-37.0`.
Para esta sesión las herramientas se preparan en `.tools/android-sdk`, fuera de Git.
La ruta original del proyecto es larga: se usa una unidad SUBST temporal al mismo
workspace para evitar límites de extracción y compilación Windows. No se mueven fuentes.
El script crea Q temporalmente si está libre, o verifica por identidad de directorio
que un Q existente apunta al mismo workspace; otra unidad se elige con -BuildDrive.
Solo retira el alias que él mismo creó. El SDK y las fuentes siguen en su ruta original.

## Script reproducible

Desde la raíz, `powershell -File mobile/scripts/android-local.ps1 -Task Preflight`.
Tareas disponibles: Debug (assembleDebug), Manifest (processDebugMainManifest) y
Apk (assembleRelease). Se limita la compilación a arm64-v8a y cuatro workers para el
teléfono físico; para un emulador x86 debe elegirse explícitamente esa arquitectura.
Gradle 9.4.1 bloqueó el trabajo entre sus builds incluidos con un único worker;
se aumentó el límite local a cuatro sin cambiar plugins ni versiones.

La primera compilación detectó cachés incrementales Kotlin incompatibles entre Q:
y la ruta canónica C:. El script desactiva ese caché y usa el compilador dentro de
Gradle; no cambia Kotlin ni las fuentes. También acota las descargas y prefiere IPv4
tras errores DNS transitorios de Maven/Google. Referencias de
[incrementalidad](https://kotlinlang.org/docs/gradle-compilation-and-caches.html) y
[estrategia del compilador](https://kotlinlang.org/docs/compiler-execution-strategy.html).

El CMake 3.22.1 del SDK trae Ninja 1.10.2, que falló al regenerar build.ninja bajo
la ruta canónica larga aunque se invocara Gradle desde Q:. Se preparó **Ninja 1.13.2**
oficial en .tools/ninja, con SHA-256 del zip
`07fc8261b42b20e71d1720b39068c2e14ffcee6396b76fb7a795fb460b78dc65`,
y se sustituyó solo el ejecutable del SDK local .tools/android-sdk/cmake/3.22.1/bin.
Se conserva allí ninja-original-1.10.2.exe. No se alteraron node_modules ni CMakeLists.
En otro equipo conviene una ruta realmente corta y Ninja con soporte de rutas largas;
no copiar ni mover fuentes fuera del workspace por efecto de este script.
[Versiones oficiales de Ninja](https://github.com/ninja-build/ninja/releases).

Actualizar Ninja no bastó en esta ruta. La comprobación confirmó un input prefab
de 261 caracteres que Windows consideraba ausente; la misma ruta normalizada mide
248 y existe, al igual que su alias Q:. Gradle termina invocando CMake desde la ruta
canónica, por lo que SUBST por sí solo no garantiza la compilación.

Se preparó una copia aislada en `C:\fuga-plus-build-bd5fcedc\mobile`, sin .env ni Git,
con npm ci --ignore-scripts y el mismo lock. Se compararon por SHA-256 33 archivos de
producto/módulo/recursos/configuración/lock: ninguna diferencia. El proyecto original
no se movió. Para usar esa copia con las herramientas del workspace original:

```powershell
powershell -File mobile/scripts/android-local.ps1 -Task Debug -MobileRoot C:\fuga-plus-build-bd5fcedc\mobile
powershell -File mobile/scripts/android-local.ps1 -Task Apk -MobileRoot C:\fuga-plus-build-bd5fcedc\mobile
```

MobileRoot selecciona una copia ya preparada; el script comprueba el nombre del
paquete y no copia, elimina o actualiza fuentes automáticamente. Antes de reutilizar
la copia después de otro cambio, hay que sincronizar explícitamente fuentes y lock
y repetir su comparación. Una compilación desde fuentes antiguas no es evidencia
de una revisión nueva. La copia se deja para reproducir la compilación y no se publica.
Para reintentar Gradle sin regenerar android, añadir -SkipPrebuild únicamente si
app.json, app.config y plugins no cambiaron desde el prebuild correcto. Si cambian,
regenerar; no usar ese indicador para ocultar un manifiesto obsoleto.

El script utiliza el SDK de ANDROID_HOME o el de .tools, limita Gradle al cache del
workspace y **no carga .env.local**. Variables públicas, si se proporcionan, se pasan
por el entorno del proceso y se revisan antes de empaquetar; nunca escribir claves
privadas en una línea de terminal compartida. Un APK sin configuración pública sirve
para verificar instalación y pantalla pública, no para aceptar el flujo financiero.
El modo release exige una URL API HTTPS para utilizarla. La firma de depuración de
la plantilla, si se utiliza para probar release local, no es una firma de publicación.

## Validación en teléfono

1. Activar depuración USB y autorizar el computador; comprobar estado ADB sin publicar
   el número de serie del dispositivo en informes.
2. Instalar el APK sin desinstalar ni borrar datos de una aplicación previa. Ante
   incompatibilidad de firma, detenerse y revisar; no ejecutar uninstall/clear por defecto.
3. Abrir la bienvenida y comprobar navegación pública, botón Atrás y legibilidad.
4. Para el flujo completo, acordar un entorno y cuentas ficticias autorizados. No usar
   la cuenta real ni generar operaciones remotas como parte de la compilación.
5. Con sesión de prueba, conceder/denegar micrófono; dictar, detener, cancelar, salir
   a segundo plano y volver a iniciar. El reconocedor del dispositivo puede procesar
   voz externamente; FUGA+ no guarda audio. La transcripción se revisa antes de confirmar.
6. Probar callbacks fugaplus://auth y recuperación; Expo Web mantiene /auth/callback.
7. Para avisos, permiso Android, canal patterns, silencio y siete días. No esperar
   análisis automático con la app cerrada; pulsar Actualizar análisis inicia el flujo.
8. Registrar APK, versión, revisión, sistema y resultado; ocultar cuentas, seriales,
   tokens y datos personales en capturas.

## Evidencia

El informe de ejecución del plan es la fuente de resultados reales: allí se distingue
prebuild, manifiesto fusionado, Kotlin compilado, APK instalado, teléfono autorizado y
flujos pendientes. Generar JS, un manifiesto o un APK no prueba por sí solo dictado,
notificación, autenticación o aislamiento con proveedores reales.

Resultado de esta sesión: debug y release compilados e instalados en Android API 36
arm64. Release abre tras reiniciar el proceso con Metro apagado; la propietaria confirmó
acceso, recuperación, registro y regreso, sin enviar formularios. La restricción de
instalación Xiaomi fue resuelta por la propietaria; no se habilitó inyección de toques.
El APK de QA no contiene configuración pública real: para flujos privados, dictado y
avisos falta un entorno de prueba autorizado. No se declara aceptado el MVP completo.
