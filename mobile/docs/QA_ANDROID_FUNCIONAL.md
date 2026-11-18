# QA funcional Android — 2026-11-18

Esta sesión usa una cuenta ficticia **ya existente** de Supabase Auth. La propietaria
autorizó su inicio de sesión y escribe la contraseña solo en el teléfono. No se crean
cuentas, perfiles públicos ni gastos en Supabase. Los datos financieros son locales.

Para volver desde la vista previa pública de Safe Area al QA con sesión se añadió
`node mobile/scripts/android-qa.cjs metro-review` (Metro 8086 y API 18000). El reverse
8081 del teléfono debe apuntar a 8086. El modo welcome-preview del puerto 8085 es
ficticio y no permite iniciar sesión. Ver [recuperación de acceso y revisión interna](RECUPERACION_ACCESO_QA.md).
El acceso ya se confirmó en el Xiaomi; la superposición del Shell privado sigue
identificada como tarea visual pendiente. Los servicios se conservaron activos.

## Configuración y causa del APK anterior

El build anterior usó EXPO_NO_DOTENV=1, no recibió variables públicas del proceso y
la copia corta excluyó .env.local. Era un APK de comprobación pública, sin configuración.
Expo no rellena esas variables después de instalar un release:
[documentación de Expo](https://docs.expo.dev/guides/environment-variables/).

Ahora android-qa.cjs lee explícitamente mobile/.env.local, admite solo las cinco
variables públicas existentes y valida la clave publishable/anon. No copia dotenv,
no hereda claves de servidor y no muestra valores. El archivo original no se modifica.
Se comprobó con GET público que Supabase acepta la URL y la clave, y que JWKS responde.

La IP de la API configurada no corresponde a una dirección actual del computador;
esa URL no respondió. El backend original sí responde en localhost:8000 y no se toca.
Para no guardar en su base remota se usa otra API QA:

- Teléfono: http://127.0.0.1:18000, encaminado por USB al computador.
- FastAPI QA: escucha solo en 127.0.0.1:18000.
- PostgreSQL: clúster local separado, 127.0.0.1:55440, base nueva fuga_android_qa_*.
- Metro QA: localhost:8083; puerto 8081 del teléfono encaminado a 8083 del PC.

No se abre el firewall ni se expone PostgreSQL o FastAPI a la LAN. La reversión USB
es una función de [ADB](https://developer.android.com/tools/adb).

## Tipo de compilación

Se eligió **debug de QA con Metro** porque la API de desarrollo es HTTP por USB.
No se relajó HTTPS del release de entrega ni se añadió una excepción de producción.
Este APK de QA requiere computador, Metro, FastAPI QA y USB activos. El release
autónomo anterior sigue siendo otra evidencia y no es este entorno funcional.

Artefacto ignorado: mobile/.verification/android-qa-20261118/fuga-plus-qa-debug.apk.
La configuración pública del JavaScript se comprobó en memoria, sin guardar su contenido
ni imprimir valores. No hay archivos .env ni patrones de claves privadas en el APK.
La clave pública es visible por diseño en el JavaScript del cliente; no es una clave de servidor.

## Arranque reproducible

Desde la raíz, en terminales separadas:

```powershell
# Solo el clúster desechable preparado; no apuntar estas pruebas a Supabase.
& 'C:/Program Files/PostgreSQL/16/bin/pg_ctl.exe' -D .tools/pg-plan-data -l .tools/postgres-plan.log -o '-p 55440 -h 127.0.0.1' -w start
backend/.venv/Scripts/python -B backend/scripts/qa_android.py
node mobile/scripts/android-qa.cjs metro
```

Comprobación y build, reutilizando la copia corta preparada y sus herramientas:

```powershell
node mobile/scripts/android-qa.cjs check
node mobile/scripts/android-qa.cjs build
```

El helper build llama a android-local.ps1 en modo Debug; no regenera un proyecto
nativo que ya está vigente. Si cambian app.json o plugins, se debe repetir prebuild
antes de reutilizar SkipPrebuild. La copia corta debe coincidir con las fuentes actuales.
La ruta corta se obtiene de .tools/android-short-build.json, o se indica como tercer
argumento: node mobile/scripts/android-qa.cjs build C:/ruta-corta/mobile. No se guarda
una ruta de compilación específica de este computador dentro del helper.

Con el SDK preparado, después de comprobar el Android autorizado:

```powershell
.tools/android-sdk/platform-tools/adb.exe reverse tcp:8081 tcp:8083
.tools/android-sdk/platform-tools/adb.exe reverse tcp:18000 tcp:18000
.tools/android-sdk/platform-tools/adb.exe install -r mobile/.verification/android-qa-20261118/fuga-plus-qa-debug.apk
```

El estado sin datos personales se consulta en http://127.0.0.1:18000/_qa/status.
Devuelve conteos, importes ficticios, estado JWKS y conteos HTTP por módulo; nunca
JWT, claves, correos o identificadores de cuenta. /health y /ready deben dar 200
con la cabecera X-Fuga-QA: local-disposable.

## Aislamiento del ensayo

El launcher no lee backend/.env ni backend/.env.local. Usa el verificador JWT original:
firma RS256/ES256, JWKS, issuer, audience, expiración y sub UUID. No hay token de bypass.
La primera cuenta validada queda fijada durante esa ejecución; corresponde a la cuenta
ficticia que la propietaria eligió. Otra cuenta se rechaza antes de aprovisionar datos.

La identidad se refleja únicamente en auth.users del sustituto **local**, con correo
constante qa@local.invalid y sin copiar metadatos personales. El trigger y las FK reales
de las migraciones crean perfil local Usuario; las rutas financieras mantienen scoping.
No equivale a probar el trigger de Supabase remoto ni a consultar su perfil persistido.

Administración, desactivación y fotos se bloquean en esta API de ensayo. Google y
recuperación de contraseña quedan deshabilitados en el entorno móvil QA para no iniciar
otras operaciones de proveedor. No usar Registrarse ni introducir datos reales.

## Pruebas manuales en el teléfono

| Paso | Acción manual | Evidencia esperada |
|---|---|---|
| Acceso | Iniciar sesión con la cuenta ficticia existente | Resumen vacío; GET me y analytics 200; cuenta fijada localmente |
| Texto | Procesar Gasté 5000 en café; revisar y confirmar | Borrador editable; nada guardado antes de confirmar; gasto en historial |
| Fechas/fugas | Crear cuatro cafés de COP 5.000 con fechas 14, 15, 17 y 18 de noviembre de 2026 | Cuatro gastos, COP 20.000 y una posible fuga cafe al actualizar |
| Dashboard | Consultar noviembre de 2026 | Total COP 20.000, cuatro gastos, Alimentación |
| Voz | Dictar Gasté 3000 pesos en buseta; revisar transcripción y procesar | Micrófono solicitado en contexto, borrador editable, sin guardar automáticamente |
| Confirmar voz | Confirmar el gasto ficticio de buseta de COP 3.000 | Cinco gastos y COP 23.000; Transporte separado de cafe |
| Cancelar voz | Iniciar otra captura y cambiar a Resumen sin confirmar | No aumenta el número de gastos; texto sigue disponible |
| Avisos | En Fugas, permitir recordatorios, aceptar permiso Android y actualizar análisis | Aviso genérico local en canal patterns, sin datos financieros en su texto |
| Duplicados | Actualizar otra vez el mismo candidato | No aparece otro aviso del mismo concepto dentro de siete días |
| Toque | Tocar el aviso de FUGA+ | Abre la evidencia de la posible fuga con la misma sesión |

Las fechas son para esta sesión; en otra fecha usar hoy-4, hoy-3, hoy-1 y hoy, siempre
dentro de la ventana. No se cambian parámetros de FUGA-01 ni registros remotos para hacer
pasar las pruebas. El reconocedor del dispositivo puede procesar voz externamente según
el aviso existente; FUGA+ no escribe archivos de audio. No se utiliza IA generativa.

Los avisos se generan cuando se consulta el análisis, con permiso y entre 08:00 y 21:00
Bogotá. No hay análisis de fondo con la app cerrada ni push remoto. Probar segundo plano
y reapertura desde un aviso ya entregado por separado; no inferirlos por una prueba unitaria.

## Resultado observado de esta sesión

301 pruebas backend (22 SQL) y 86 frontend aprobadas, sin omisiones. TypeScript,
Ruff mínimo y mypy correctos. Los proveedores se simulan en la suite automatizada.

La propietaria confirmó en el teléfono el inicio de sesión, texto/historial/dashboard,
el dictado buseta de COP 3.000 con Transporte y el aviso local con toque/sin duplicado.
El backend aceptó el JWT real usando su verificación habitual y los SELECT locales
confirmaron seis gastos por COP 28.000: cinco cafés/COP 25.000 y una buseta/COP 3.000.
La cohorte de cuatro fechas previstas suma COP 20.000; se conservó otro café del día 16.
FUGA-01 agrupa los cinco cafés por COP 25.000. Ambos permisos Android están concedidos.

No se probaron físicamente en esta sesión permiso denegado, cancelación/segundo plano
durante dictado, cierre completo/reapertura desde aviso ni callbacks reales de correo.
Esos casos adicionales quedan preparados; no invalidan la evidencia del flujo principal.
El release con API HTTPS y la persistencia financiera remota siguen fuera de este ensayo.

Xiaomi bloquea los toques automatizados de ADB; se mantienen las comprobaciones manuales
sin ampliar permisos de inyección. No se capturan las pantallas mientras se introduce
la contraseña. Las pruebas automáticas usan otras identidades firmadas de prueba y
otra base desechable, nunca la sesión real del teléfono.

## Cierre

Al terminar, detener únicamente las terminales de Metro QA y qa_android.py con Ctrl+C.
El backend elimina solo su propia base fuga_android_qa_* al cerrar normalmente. Los
datos ficticios no son persistencia de producto ni se sincronizan con Supabase.
Retirar los reverse de los puertos 8081 y 18000 cuando deje de usarse QA. No detener
el backend original del puerto 8000. Si se desconecta USB o se apaga el PC, este APK
de desarrollo pierde conectividad; no debe presentarse como release de distribución.
