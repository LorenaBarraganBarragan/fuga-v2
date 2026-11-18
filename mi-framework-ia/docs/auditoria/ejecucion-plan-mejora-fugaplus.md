# Ejecución del plan de mejora FUGA+

Fecha de inicio: 2026-11-18, America/Bogota. Autorización: solicitud expresa de ejecutar ACT-01 a ACT-15. Sin commits, pushes, despliegues o cambios en Supabase remoto.

Base de trabajo: `develop`, `ce24348` (respaldo funcional previo al plan); árbol limpio al inicio. Esto resuelve el estado sin seguimiento observado en la auditoría histórica, sin atribuir este respaldo al agente.

## Estado vigente: HU-08 — 2026-11-18

Seguimiento de fotografía implementado y probado localmente: **325 backend/31 SQL
y 97 frontend**. Cloudinary GET /ping 200 con las variables corregidas. Dos PNG
sintéticos cargados bajo autorización, sin borrados. Migración 0010 solo local,
QA fotos separado en 18001/8084. Propietaria confirmó vista previa/cancelación,
persistencia tras login/logout y sustitución; metadatos/CDN y URL local verificados.
Ver [informe HU-08](hu08-fotografia-perfil.md)
y [evidencia HU-08](evidencia-hu08-fotografia.json). Los conteos y verificaciones del
apartado siguiente corresponden al cierre QA anterior a HU-08.

## Seguimiento Android QA anterior a HU-08 — 2026-11-18

Se leyó el informe y su evidencia antes de continuar. La nueva autorización permite
revisar mobile/.env.local; posteriormente la propietaria autorizó expresamente iniciar
sesión con una cuenta ficticia ya existente. Introdujo la contraseña solo en el teléfono.
No se crearon cuentas, perfiles públicos, gastos ni tablas en Supabase remoto.

El APK release inicial omitió configuración porque EXPO_NO_DOTENV=1 estaba activo,
no había variables públicas heredadas y la copia de compilación excluía .env.local.
No era un error de Supabase. En esta continuación se validaron las variables sin
mostrar valores: clave publishable, URL Auth raíz HTTPS, GET público de settings 200
y JWKS 200. La IP de API configurada no es una dirección actual del computador;
esa URL no respondió, aunque el FastAPI original en localhost:8000 sí respondió 200.

Se preparó e instaló **debug QA con Metro y USB**, sin relajar HTTPS del release:
API http://127.0.0.1:18000 por adb reverse, Metro localhost:8083 y PostgreSQL local
en 55440. La URL original y ambos .env.local se conservaron sin cambios; no se leyó
backend/.env.local. El helper móvil inyecta exclusivamente configuración pública en
memoria y elimina variables de servidor del entorno heredado. No copia dotenv al build.

FastAPI QA usa el verificador JWT original y el JWKS real. La primera cuenta ficticia
validada queda fijada en ese proceso; se refleja únicamente en el sustituto auth.users
local, con correo constante y sin copiar metadatos personales. El trigger y las FK de
las migraciones crean perfil local Usuario. No se está verificando el perfil persistido
en Supabase remoto. Administración, fotos y desactivación quedan bloqueadas en este
ensayo; la configuración QA deshabilita Google y recuperación para no iniciar otras
operaciones remotas. No existe token de bypass ni cambio en la autorización de producto.

| Flujo | Prueba automatizada | Comprobación física/manual y observación |
|---|---|---|
| Inicio de sesión | JWT inválido rechazado, rol no confiable ignorado, segunda identidad rechazada | Propietaria inició sesión con cuenta ficticia; FastAPI aceptó JWT real y GET me/analytics dieron 200 |
| Texto y confirmación | Rutas reales de interpretación, confirmación e idempotencia sobre PostgreSQL local | Propietaria confirmó registro, historial y dashboard; solicitudes guardadas en la base QA |
| Dashboard | Agregaciones/fechas y rutas HTTP pasan | Total final confirmado por la propietaria y por SELECT local: 6 gastos, COP 28.000 |
| Voz | Componentes de permiso/ausencia/longitud y contrato de gasto pasan | Propietaria dictó buseta, confirmó COP 3.000 y Transporte; dato local coincide |
| FUGA-01 | Cuatro cafés COP 20.000, ventana/concurrencia/versiones preservadas | Fuga local vigente: cafe, 5 ocurrencias, COP 25.000; incluye un gasto adicional ficticio del día 16 |
| Aviso local | Canal, horario, siete días, concurrencia y errores pasan | Propietaria confirmó recepción, toque que abre evidencia y ausencia de duplicado |

La cohorte prevista del 14, 15, 17 y 18 de noviembre existe y suma COP 20.000.
Durante las pruebas la propietaria creó otro café del día 16; se conservó. De ahí los
cinco cafés/COP 25.000 y, después de la buseta, seis gastos/COP 28.000. No se ajustaron
datos ni parámetros para forzar el resultado. Micrófono y notificaciones tienen permiso.
Los importes y conteos de esta sección provienen solo de registros ficticios locales.

Resultados actuales: **301 pruebas backend aprobadas, incluidas 22 SQL, y 86 frontend;
cero omisiones en esas suites**. TypeScript, mypy y Ruff mínimo pasan. Siete pruebas
backend y tres frontend son nuevas para este seguimiento. Cobertura app Python: 89 %;
Node: 92,91 % de líneas en ocho archivos medidos, ahora incluyendo el launcher QA.
No es comparable como cobertura global de UI con la cifra anterior de siete módulos.
Los tests automatizados usan firmas/proveedores simulados; no usan la sesión del teléfono.

APK QA: 49.511.283 bytes, SHA-256
`986b86c487a0c96a9be11ef96f1ab13597db4394afeedfca7056722d473fb724`.
Build correcto (261 tareas, 3m44s), instalado con -r. Bundle Android respondió 200;
se comprobó en memoria la presencia de URL/clave pública/API QA. Cero archivos .env
y cero patrones sb_secret_ en el APK. Este debug requiere Metro/USB activos; no es el
release autónomo anterior ni una compilación de distribución configurada para HTTPS.

Guía y límites: [QA Android funcional](../../../mobile/docs/QA_ANDROID_FUNCIONAL.md).
Evidencia verificable sin cuentas, JWT o claves: [evidencia QA](evidencia-qa-android.json).
El entorno QA permanece activo para continuar pruebas; el estado agregado se consulta
en http://127.0.0.1:18000/_qa/status. El backend original del puerto 8000 no se cambió.
No hubo commits, pushes, despliegues ni modificaciones de migraciones/reglas del producto.

En este seguimiento se añadieron solo herramientas de QA, pruebas y documentación:
backend/scripts/qa_android.py, sus dos archivos de pruebas, mobile/scripts/android-qa.cjs,
mobile/tests/android-qa.test.cjs, mobile/docs/QA_ANDROID_FUNCIONAL.md y la evidencia QA.
Se actualizaron este informe, la referencia de evidencia histórica, README, PROGRESO_BUILD
y el inventario. No hubo cambios nuevos en backend/app, mobile/src ni archivos .env.local.

Pendientes de alcance adicional: permiso denegado físico, cancelación/cambio de aplicación
durante dictado, ciclo completo de cierre/reapertura desde aviso y callbacks de correo
reales. El flujo principal solicitado de login, texto, dashboard, dictado y aviso/toque
quedó validado en QA. No se declara probado un release conectado a datos financieros remotos.

## Alcance aprobado (ACT-01)

Se conservan las 13 HU Must de la especificación 3.0. Voz Android es prioridad adicional de entrega; se implementa también la mejora de notificaciones locales ya existente. No se añaden push remotas, IA generativa, presupuestos ni nuevos proveedores. La aceptación por hardware y por proveedores se registra separadamente de la implementación local.

## Fases

Las fases 0–5 describen el cierre inicial, previo al seguimiento QA de arriba.
El release inicial abre sin Metro; la validación funcional posterior usa debug QA.
Los ensayos locales no acreditan Render desplegado ni el esquema financiero remoto.

| Fase | Cambios / comprobación | Resultado observado |
|---|---|---|
| 0 | Lectura completa de plan/auditoría, alcance y respaldo | HEAD ce24348 limpio; sin commits del agente |
| 1 | Micrófono, plugin, prebuild y prueba nueva | 255 backend, 14 omitidas; 45 frontend; TypeScript correcto |
| 2 | Lanzador seguro, PostgreSQL separado y cobertura; cliente/reintentos | 269 backend sin omisiones, 89 % líneas; 55 frontend |
| 3 | Snapshots selectivos, evidencia en lote, SQL agregado, avisos serializados | 274 backend; 61 frontend; mypy correcto |
| 4 | Configuración segura, CI/Render local, arranque real y componentes | 294 backend con SQL; 83 frontend; Linux 274 + 20 SQL omitidas; arranque real en ambos sistemas |
| 5 | SDK, JDK 17, debug/release y dispositivo | Ambos APK instalados; bienvenida release comprobada sin Metro; propietaria confirmó acceso/recuperación/registro y regreso sin enviar formularios |
| 6 | Configuración pública explícita, USB, Auth real y finanzas locales QA | 301 backend/22 SQL, 86 frontend; propietaria confirmó login, texto/dashboard, voz, aviso/toque/sin duplicado; registros locales verificados |

## Resultados de implementación por actividad

| Actividad | Trabajo realizado | Aceptación o límite actual |
|---|---|---|
| ACT-01 | Alcance anotado en RF/HU sin reclasificar MoSCoW; README/arquitectura/progreso actualizados; prompt canónico completo | Implementación documental realizada |
| ACT-02 | Retirado bloqueo de micrófono, cámara sigue bloqueada; test del plugin y manifiesto final de Gradle | RECORD_AUDIO presente, CAMERA ausente; permiso concedido y dictado físico confirmados en QA |
| ACT-03 | SDK/JDK y compilación reproducible; FugaVoice Kotlin/DEX; debug QA instalado | Dictado físico buseta y guardado confirmados; quedan casos adicionales de permiso/ciclo de vida |
| ACT-04 | Suite segura y PostgreSQL local; fixtures rechazan hostaddr/remoto; controles QA adicionales | 301 pruebas actuales, incluidas 22 SQL; tests sin proveedores reales |
| ACT-05 | Transporte y componentes; confirmación, UUID, cambio de cuenta y error de carga | Pruebas automáticas pasan; login/texto/historial/dashboard Android QA confirmados; callback real de correo pendiente |
| ACT-06 | Ruff mínimo/mypy/TypeScript; coverage Python y cobertura Node de módulos; UI con renderer React coincidente | Controles verdes; advertencias upstream y alcance de cobertura explícitos |
| ACT-07 | Evita invalidar/reactivar snapshots sin cambios; índice en memoria de evidencia, inserción en lote y catálogo conjunto | Repetición: 2 escrituras antes, 0 después; concurrencia, ventana y versión pasan |
| ACT-08 | SUM/COUNT SQL por categoría con multiplicidad conservada; comparación mensual bajo solicitud | Cuatro filas pueden convertirse en una sin perder conteos, importes o porcentajes |
| ACT-09 | Canal patterns, control concurrente, errores genéricos y horario | Automáticas pasan; entrega, toque y ausencia de duplicado confirmados físicamente; otros estados de ciclo de vida pendientes |
| ACT-10 | Validación prod y CA relativa portable; public keys verificadas en runtime y antes del bundle | Configuraciones inseguras rechazadas sin valores sensibles; .env.local no editados |
| ACT-11 | Dos intentos máximos de lectura, espera visible, cancelación; escrituras no automáticas | Pruebas de lentitud, 503, cancelación, cambio de sesión y UUID pasan |
| ACT-12 | Workflow sin despliegue ni secrets; inventario de archivos y escáner; base Git respaldada por propietaria | YAML preparado/localmente comprobado; no commit/push ni corrida GitHub |
| ACT-13 | Launcher portable, PORT, un proceso, pool y timeouts; render.yaml Free/manual | Arranque real sintético pasa Windows y Linux; no se desplegó Render |
| ACT-14 | Procedimiento de retención y prueba de cola/reactivación/FK | 30 días y cancelación probados localmente; sin ejecutor ni borrados reales |
| ACT-15 | Artefactos identificados por hash, revisión de secretos y evidencias QA | Release público sin Metro y debug funcional por USB comprobados; no se acredita un release de distribución con backend HTTPS |

## Pruebas y medidas del cierre inicial (antes del seguimiento QA)

- PostgreSQL 16.10: clúster nuevo `.tools/pg-plan-data`, rol ficticio fuga_test y puerto 55440.
  El clúster antiguo tenía otro rol; no se alteraron sus registros para habilitar pruebas.
  Los fixtures crean/retiran únicamente su base fuga_test_*; Auth es un sustituto local.
- Launcher `backend/scripts/test_safe.py`: no carga dotenv, bloquea HTTP externo y,
  salvo integración explícita local, bloquea PostgreSQL. Se pueden generar informes de cobertura.
- Windows Python 3.12.6: **294 pruebas completas, cero omitidas**, en la ronda final,
  una deprecación Starlette/httpx y cobertura de líneas 89 % de app.
- Ubuntu: se encontró Python 3.14 fuera del rango aprobado; se preparó Python 3.12.16
  portátil con checksum, en entorno separado. **274 aprobadas y 20 omitidas** al no conectar
  a SQL desde Linux. Las mismas 20 se ejecutaron en Windows; no se ocultan como éxitos Linux.
- `smoke_start.py`: Uvicorn real, configuración prod sintética, solo loopback; /health=200,
  /ready=503 por BD deliberadamente ausente, /docs=404 y /api/v1/expenses=401 en ambos sistemas.
  El ensayo no prueba Supabase ni tiempos reales de suspensión de Render.
- Node: **83 pruebas aprobadas, cero omitidas**, TypeScript correcto. La cobertura
  mide siete módulos/guard ejecutados directamente; se excluyen TSX, el adaptador
  notifications.ts transpilado y utilidades de prueba para evitar porcentajes sobre
  líneas transformadas. No representa cobertura total de la app ni del puente nativo.
  Resultado de ese alcance: **99,39 % de líneas, 88,80 % de ramas y 97,30 % de funciones**.
- Se instalaron solo `coverage` en Python y `react-test-renderer` de la misma versión
  React 19.3.0 como soporte de QA. El renderer está deprecado y emite aviso explícito;
  permite probar hooks/componentes reales con host nativo simulado y sin introducir Jest
  u otro stack de ejecución. No valida el puente Android. Una migración de herramientas
  de testing puede evaluarse después; no se oculta esta limitación.
- La medición SQL previa reprodujo dos UPDATE de snapshots por análisis sin cambios;
  la prueba final exige cero. Se preservan identidad, COP 20.000 para los cuatro cafés,
  evidencia, cambio de ventana/versión y exclusión lógica. No hay cambios de migraciones
  ni de parámetros/versionado FUGA-01.
- Ruff F/E9/I global y mypy de 13 archivos pasan. Ruff completo también pasa en los
  módulos de lógica/configuración intervenidos, scripts y pruebas nuevos: se corrigieron anotaciones/longitudes
  locales y se justificaron únicamente los casos CLI, subprocess fijo sin shell,
  sondeo HTTP loopback y listener 0.0.0.0 de la plataforma. No se impone limpieza
  global ni se confunden los 210 avisos históricos con vulnerabilidades.
  El fixture SQL existente conserva tres E501 en su DDL de prueba; quedan fuera de
  ese resultado de Ruff completo y no fallan el control mínimo aprobado.
- Un probe temporal con fallo deliberado devolvió exit 1 a través de test_safe.py;
  fue retirado inmediatamente. Es evidencia de propagación de fallo local, no una
  regresión ni una corrida GitHub. La suite normal volvió a aprobar sus 294 casos.
- Comparación SHA-256 contra la base inicial: **15 archivos protegidos sin cambios**,
  incluidas migraciones/seed y fuentes de regla, diccionario/normalizador y regresiones.

## Infraestructura y fuentes

La preparación Render usa Python 3.12.16, la misma rama 3.12 comprobada en Linux,
mediante PYTHON_VERSION y .python-version. Render admite una versión publicada
explícita; no se usa el Python 3.14 predeterminado. [Referencia](https://render.com/docs/python-version).
Los servicios no se crean por existir render.yaml. La validación de GitHub Actions
permanece local; no se envió código o secretos ni se activó una ejecución remota.
El workflow fija Ubuntu 24.04 para evitar cambios de ubuntu-latest y reutilizar
PostgreSQL 16 instalado en el runner; lo inicia únicamente para el job desechable.
Incluye también el smoke sintético del launcher. La disponibilidad documentada se
contrastó con el [inventario oficial del runner](https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md).

La extracción inicial de herramientas Android con PowerShell falló por la ruta larga;
se verificó el checksum y se extrajo con Python en un alias corto al mismo workspace.
Gradle intentó provisionar JDK 17 y falló al moverlo; se reutilizó su zip oficial,
se verificó checksum de Adoptium y se preparó .tools/jdk17. No se cambió Java del sistema.
Los avisos del SDK/Gradle sobre APIs deprecadas se registran como upstream. Ambos
ensamblados terminaron con BUILD SUCCESSFUL; no se modificaron versiones para silenciarlos.

Se reprodujeron después dos bloqueos del toolchain: CMake/Ninja regenera build.ninja
en la ruta larga canónica pese a SUBST; y Gradle 9.4.1 no progresa entre builds
incluidos con un único worker en la copia nueva. Ninja 1.13.2 verificado no bastó
para el primero: un input prefab sin normalizar de 261 caracteres da inexistente,
mientras su equivalente normalizado de 248 y el alias Q sí existen. Se preparó una
copia aislada corta C:\fuga-plus-build-bd5fcedc\mobile, sin .env ni Git; npm ci usa
el mismo lock. Comparación SHA-256 de 33 archivos de producto/configuración/recursos:
cero diferencias. El script acepta MobileRoot y usa cuatro workers. No se movieron
fuentes originales ni se alteraron librerías para ocultar estos fallos.

Metro QA separado en localhost:8083, con EXPO_NO_DOTENV/EXPO_OFFLINE y sin variables
públicas heredadas: bundle Android respondió 200, 5.475.995 bytes, cero coincidencias
del patrón sb_secret_ con sufijo de 24 caracteres. Es un control acotado sobre ese
artefacto, no una afirmación de escaneo universal de secretos o aceptación de UI.

El entorno Linux temporal bajo /tmp dejó de estar disponible al cerrar WSL. Se repitió
la verificación con el entorno persistente .tools/linux-venv y CPython 3.12.16. El primer
smoke contra ese filesystem montado excedió diez segundos; se amplió únicamente el
plazo del comprobador a 60 segundos y la prueba pasó. Esto no altera timeouts de API
ni acredita latencia de Render. El launcher no lee dotenv y todas las URLs son sintéticas.

## Comandos reproducibles

Desde la raíz, con el PostgreSQL desechable iniciado (se detuvo al cerrar las pruebas):

```powershell
& 'C:/Program Files/PostgreSQL/16/bin/pg_ctl.exe' -D .tools/pg-plan-data -l .tools/postgres-plan.log -o '-p 55440 -h 127.0.0.1' -w start
$env:FUGA_TEST_DATABASE_URL='postgresql://fuga_test@127.0.0.1:55440/postgres'
backend/.venv/Scripts/python -B backend/scripts/test_safe.py --integration --coverage
backend/.venv/Scripts/ruff check backend/app backend/tests backend/scripts scripts --select F,E9,I --no-cache
backend/.venv/Scripts/mypy backend/app/domain
backend/.venv/Scripts/python -B backend/scripts/smoke_start.py
powershell -File mobile/scripts/android-local.ps1 -Task Preflight
```

Desde mobile: `npm run test:coverage` y `npm run typecheck`. Sin PostgreSQL, omitir
--integration: se bloquea la BD y se informan las 20 omisiones. Desde Ubuntu con el
entorno preparado: `.tools/linux-venv/bin/python -B backend/scripts/test_safe.py` y
`.tools/linux-venv/bin/python -B backend/scripts/smoke_start.py`.

No copiar este DSN ficticio a la aplicación ni sustituirlo por Supabase. Los scripts
de pruebas limpian entorno y bloquean proveedores; los fixtures solo crean/borran
su base local fuga_test_*. El procedimiento Android está en
[ANDROID_LOCAL.md](../../../mobile/docs/ANDROID_LOCAL.md).

## Dependencias y límites de aceptación

- Auditoría actualizada Python: **cero avisos**. npm: **25 alertas high propagadas**
  desde un único aviso de picomatch, retirado en la fuente primaria el 2026-11-18.
  No se degradó Expo ni se ejecutó audit fix --force. Ver
  [análisis y fuentes](../../../docs/DEPENDENCIAS_SEGURIDAD.md).
- En el cierre inicial no se leyó ni editó ningún .env.local ni hubo operaciones de
  proveedor. El seguimiento QA posterior autorizó leer el archivo público móvil e
  iniciar sesión con una cuenta ficticia existente; no se modificaron .env.local ni
  datos financieros remotos. No hubo staging, commits, pushes o despliegues.
- No se modificaron migraciones, catálogo, diccionario, versión/umbrales FUGA-01 ni
  los contratos públicos de finanzas. El pool baja de 5+10 a 3+2 por proceso y se
  documenta un proceso inicial, sin introducir otra BD, Redis o servicios de pago.
- CI y Render están preparados y comprobados localmente; falta una revisión versionada
  autorizada, checkout limpio y corrida real de GitHub. No se reclama un pipeline verde
  remoto ni aceptación de arranque frío en Render.
- Retención: cola/reactivación/FK probadas; procedimiento revisable disponible. Sigue
  pendiente la decisión humana de auditoría/perfil a 30/90 días antes de suprimir datos
  reales. No se implementó ni anunció borrado automático.
- El APK inicial sin valores públicos solo acredita instalación/navegación pública.
  Auth, finanzas locales, dictado y aviso/toque se validaron después en el debug QA
  autorizado, con verificaciones manuales y conteos locales descritos arriba.
- La revisión final preservó las opciones booleanas existentes PASSWORD_RECOVERY_ENABLED
  y GOOGLE_ENABLED: el guard distingue esos flags de credenciales y comprueba sus
  valores. Una prueba específica evita bloquear Expo Web cuando recuperación es false.
  Es corrección del guard nuevo, sin habilitar proveedores ni cambiar funciones del MVP.

## Android: artefactos y aceptación física del cierre inicial

El debug **compiló correctamente** en la copia corta (261 tareas, última reanudación
3 minutos). FugaVoice está en el DEX. AAPT confirma RECORD_AUDIO y POST_NOTIFICATIONS,
sin CAMERA. Versión 0.1.0, package co.edu.fugaplus.app, arquitectura arm64-v8a.

- Artefacto local ignorado: mobile/.verification/plan-mejora/android-debug.apk.
- Tamaño: 49.507.823 bytes.
- SHA-256: b52a8e92688d5e98e766149f988f0e7f1ead2215c8421a8b01741be886b703e1.
- Teléfono Xiaomi, API 36 y arm64-v8a. INSTALL_FAILED_USER_RESTRICTED se resolvió
  cuando la propietaria autorizó instalar FUGA+ por USB. Debug y release se instalaron
  con -r, preservando datos; no se ejecutó uninstall ni clear ni se eludieron permisos.
- Bienvenida debug comprobada visualmente. Después se instaló release, se detuvo
  únicamente Metro QA, se retiró su reverse USB, se forzó el cierre de FUGA+ y se abrió
  de nuevo: puerto 8083 cerrado, proceso activo y bienvenida del release visible.
- Release: **BUILD SUCCESSFUL**, 327 tareas, 15m19s; 23.244.408 bytes, JS integrado
  2.059.352 bytes. SHA-256 **129c4a394f1948953eb6ccac554b5a4659e45c4a80733342edc5577974ba3103**.
  Firma verificada, no debuggable, nombre FugaVoice en DEX, micrófono y avisos presentes,
  cámara ausente. Archivo: mobile/.verification/plan-mejora/android-release.apk.
- El APK no contiene archivos .env ni coincidencias del patrón de claves sb_secret_
  revisado en todas sus entradas. No había variables EXPO_PUBLIC heredadas y no se
  cargó dotenv. Se usó la firma de depuración de la plantilla para esta prueba release
  local; no es una firma privada de distribución ni un APK configurado para cuentas reales.
- Capturas públicas ignoradas: debug-welcome.png y release-welcome-no-metro.png,
  bajo mobile/.verification/plan-mejora. No contienen cuentas, gastos ni tokens.
- Xiaomi bloquea inyección de toques por ADB. El árbol UI no permitió identificar
  controles y el probe opcional de inspector no obtuvo resultado. No se consideran
  éxitos de automatización. La propietaria confirmó manualmente que acceso, recuperación,
  registro y regreso cargan correctamente en el release sin Metro, sin enviar formularios.
  Dictado/avisos y flujos privados todavía sin aceptación física. No se ampliaron permisos
  para automatizar.
- Expo Web también exportó correctamente: 534 módulos, 15 recursos y bundle de 1,1 MB
  en mobile/.verification/plan-mejora/web. Es compilación, no una prueba E2E del navegador.
- El proceso Gradle avisó de metaspace 512 MiB insuficiente al finalizar debug.
  Se acotó heap a 2 GiB y metaspace a 1 GiB en el comando del script para release;
  no se alteró configuración de Java del sistema. Se mantienen los avisos upstream.
- Una descarga DNS de kotlin-compiler 32.2.1 se completó desde dl.google.com con
  checksum oficial; SHA-256 del JAR: dc7779cfb581591ca2b6f478f0a952c0e918dee76b5c15dd6f6819367b3eb1cf.

## Cierre operativo inicial y siguiente paso (histórico)

PostgreSQL desechable y Metro QA detenidos; reverse USB y alias temporal Q creados
para QA retirados. El script puede recrear el alias al volver a compilar.
Se deja el release instalado en el teléfono y los artefactos de compilación para revisión.
No se tocaron servidores previos de la propietaria. La copia corta y .tools conservan
las herramientas para reproducir el build, sin ponerlas en Git.

Siguiente paso: autorizar una prueba controlada con cuenta y gastos ficticios, y generar
una compilación que reciba únicamente configuración pública válida. Para desarrollo local
se puede reutilizar debug, FastAPI y USB/LAN; release exige API HTTPS. El despliegue de
Render, la ejecución remota de CI, cualquier commit/push y operaciones Supabase se mantienen
como autorizaciones separadas. No hace falta rehacer módulos ni cambiar tecnologías.

## Archivos modificados y creados

Lista acumulada respecto de ce24348: plan, QA Android y HU-08, sin staging ni commits.
Herramientas, entornos, builds nativos y APK permanecen ignorados.

| Archivo | Cambio |
|---|---|
| [.github/workflows/validate.yml](../../../.github/workflows/validate.yml) | Creado |
| [.gitignore](../../../.gitignore) | Modificado |
| [README.md](../../../README.md) | Modificado |
| [backend/.env.example](../../../backend/.env.example) | Modificado |
| [backend/.python-version](../../../backend/.python-version) | Creado |
| [backend/app/api/v1/me.py](../../../backend/app/api/v1/me.py) | Modificado |
| [backend/app/core/config.py](../../../backend/app/core/config.py) | Modificado |
| [backend/app/core/logging.py](../../../backend/app/core/logging.py) | Modificado |
| [backend/app/db/session.py](../../../backend/app/db/session.py) | Modificado |
| [backend/app/domain/analytics/aggregations.py](../../../backend/app/domain/analytics/aggregations.py) | Modificado |
| [backend/app/services/analytics_service.py](../../../backend/app/services/analytics_service.py) | Modificado |
| [backend/app/services/leaks_service.py](../../../backend/app/services/leaks_service.py) | Modificado |
| [backend/app/services/profile_photos.py](../../../backend/app/services/profile_photos.py) | Creado |
| [backend/docs/audit-dependencias.json](../../../backend/docs/audit-dependencias.json) | Modificado |
| [backend/pyproject.toml](../../../backend/pyproject.toml) | Modificado |
| [backend/requirements.lock](../../../backend/requirements.lock) | Modificado |
| [backend/scripts/cleanup_profile_photos.py](../../../backend/scripts/cleanup_profile_photos.py) | Creado |
| [backend/scripts/qa_android.py](../../../backend/scripts/qa_android.py) | Creado |
| [backend/scripts/smoke_start.py](../../../backend/scripts/smoke_start.py) | Creado |
| [backend/scripts/start.py](../../../backend/scripts/start.py) | Creado |
| [backend/scripts/test_safe.py](../../../backend/scripts/test_safe.py) | Creado |
| [backend/tests/integration/conftest.py](../../../backend/tests/integration/conftest.py) | Modificado |
| [backend/tests/integration/test_android_qa.py](../../../backend/tests/integration/test_android_qa.py) | Creado |
| [backend/tests/integration/test_improvement_plan.py](../../../backend/tests/integration/test_improvement_plan.py) | Creado |
| [backend/tests/integration/test_profile_photos_hu08.py](../../../backend/tests/integration/test_profile_photos_hu08.py) | Creado |
| [backend/tests/unit/api/test_profile_photos_hu08.py](../../../backend/tests/unit/api/test_profile_photos_hu08.py) | Creado |
| [backend/tests/unit/test_android_qa_safety.py](../../../backend/tests/unit/test_android_qa_safety.py) | Creado |
| [backend/tests/unit/test_concept_leaks_service.py](../../../backend/tests/unit/test_concept_leaks_service.py) | Modificado |
| [backend/tests/unit/test_production_config.py](../../../backend/tests/unit/test_production_config.py) | Creado |
| [docs/ARQUITECTURA_FUGA_PLUS.md](../../../docs/ARQUITECTURA_FUGA_PLUS.md) | Modificado |
| [docs/DEPENDENCIAS_SEGURIDAD.md](../../../docs/DEPENDENCIAS_SEGURIDAD.md) | Creado |
| [docs/RETENCION_OPERATIVA.md](../../../docs/RETENCION_OPERATIVA.md) | Creado |
| [mi-framework-ia/docs/auditoria/auditoria-tecnica-fugaplus.md](../../../mi-framework-ia/docs/auditoria/auditoria-tecnica-fugaplus.md) | Modificado |
| [mi-framework-ia/docs/auditoria/ejecucion-plan-mejora-fugaplus.md](../../../mi-framework-ia/docs/auditoria/ejecucion-plan-mejora-fugaplus.md) | Creado |
| [mi-framework-ia/docs/auditoria/evidencia-hu08-fotografia.json](../../../mi-framework-ia/docs/auditoria/evidencia-hu08-fotografia.json) | Creado |
| [mi-framework-ia/docs/auditoria/evidencia-qa-android.json](../../../mi-framework-ia/docs/auditoria/evidencia-qa-android.json) | Creado |
| [mi-framework-ia/docs/auditoria/evidencia-validacion-plan.json](../../../mi-framework-ia/docs/auditoria/evidencia-validacion-plan.json) | Creado |
| [mi-framework-ia/docs/auditoria/hu08-fotografia-perfil.md](../../../mi-framework-ia/docs/auditoria/hu08-fotografia-perfil.md) | Creado |
| [mi-framework-ia/docs/auditoria/inventario-candidato.json](../../../mi-framework-ia/docs/auditoria/inventario-candidato.json) | Creado |
| [mi-framework-ia/docs/auditoria/plan-mejora-fugaplus.md](../../../mi-framework-ia/docs/auditoria/plan-mejora-fugaplus.md) | Modificado |
| [mi-framework-ia/docs/historias-usuario/HISTORIAS_DE_USUARIO.md](../../../mi-framework-ia/docs/historias-usuario/HISTORIAS_DE_USUARIO.md) | Modificado |
| [mi-framework-ia/docs/planificacion/PROGRESO_BUILD.md](../../../mi-framework-ia/docs/planificacion/PROGRESO_BUILD.md) | Modificado |
| [mi-framework-ia/docs/prompts/prompt-01-auditoria-plan-mejora-v1.md](../../../mi-framework-ia/docs/prompts/prompt-01-auditoria-plan-mejora-v1.md) | Creado |
| [mi-framework-ia/docs/requerimientos/REQUERIMIENTOS.md](../../../mi-framework-ia/docs/requerimientos/REQUERIMIENTOS.md) | Modificado |
| [mobile/.env.example](../../../mobile/.env.example) | Modificado |
| [mobile/App.tsx](../../../mobile/App.tsx) | Modificado |
| [mobile/app.config.js](../../../mobile/app.config.js) | Creado |
| [mobile/app.json](../../../mobile/app.json) | Modificado |
| [mobile/docs/ANDROID_LOCAL.md](../../../mobile/docs/ANDROID_LOCAL.md) | Creado |
| [mobile/docs/QA_ANDROID_FUNCIONAL.md](../../../mobile/docs/QA_ANDROID_FUNCIONAL.md) | Creado |
| [mobile/docs/audit-dependencias.json](../../../mobile/docs/audit-dependencias.json) | Modificado |
| [mobile/docs/versiones.md](../../../mobile/docs/versiones.md) | Modificado |
| [mobile/package-lock.json](../../../mobile/package-lock.json) | Modificado |
| [mobile/package.json](../../../mobile/package.json) | Modificado |
| [mobile/scripts/android-local.ps1](../../../mobile/scripts/android-local.ps1) | Creado |
| [mobile/scripts/android-qa.cjs](../../../mobile/scripts/android-qa.cjs) | Creado |
| [mobile/scripts/check-public-env.cjs](../../../mobile/scripts/check-public-env.cjs) | Creado |
| [mobile/src/auth/AuthProvider.tsx](../../../mobile/src/auth/AuthProvider.tsx) | Modificado |
| [mobile/src/lib/api.ts](../../../mobile/src/lib/api.ts) | Modificado |
| [mobile/src/lib/expenseAttempt.ts](../../../mobile/src/lib/expenseAttempt.ts) | Creado |
| [mobile/src/lib/notifications.ts](../../../mobile/src/lib/notifications.ts) | Modificado |
| [mobile/src/lib/profilePhoto.ts](../../../mobile/src/lib/profilePhoto.ts) | Creado |
| [mobile/src/lib/publicConfig.ts](../../../mobile/src/lib/publicConfig.ts) | Creado |
| [mobile/src/lib/reminders.ts](../../../mobile/src/lib/reminders.ts) | Creado |
| [mobile/src/lib/request.ts](../../../mobile/src/lib/request.ts) | Creado |
| [mobile/src/lib/supabase.ts](../../../mobile/src/lib/supabase.ts) | Modificado |
| [mobile/src/screens/Dashboard.tsx](../../../mobile/src/screens/Dashboard.tsx) | Modificado |
| [mobile/src/screens/Leaks.tsx](../../../mobile/src/screens/Leaks.tsx) | Modificado |
| [mobile/src/screens/NewExpense.tsx](../../../mobile/src/screens/NewExpense.tsx) | Modificado |
| [mobile/src/screens/Profile.tsx](../../../mobile/src/screens/Profile.tsx) | Modificado |
| [mobile/tests/android-qa.test.cjs](../../../mobile/tests/android-qa.test.cjs) | Creado |
| [mobile/tests/build-env.test.cjs](../../../mobile/tests/build-env.test.cjs) | Creado |
| [mobile/tests/component-loader.cjs](../../../mobile/tests/component-loader.cjs) | Creado |
| [mobile/tests/components.test.cjs](../../../mobile/tests/components.test.cjs) | Creado |
| [mobile/tests/delivery-config.test.cjs](../../../mobile/tests/delivery-config.test.cjs) | Creado |
| [mobile/tests/fixtures/profile-qa-a.png](../../../mobile/tests/fixtures/profile-qa-a.png) | Creado |
| [mobile/tests/fixtures/profile-qa-b.png](../../../mobile/tests/fixtures/profile-qa-b.png) | Creado |
| [mobile/tests/native-config.test.cjs](../../../mobile/tests/native-config.test.cjs) | Creado |
| [mobile/tests/notifications-adapter.test.cjs](../../../mobile/tests/notifications-adapter.test.cjs) | Creado |
| [mobile/tests/profile-photo.test.cjs](../../../mobile/tests/profile-photo.test.cjs) | Creado |
| [mobile/tests/public-config.test.cjs](../../../mobile/tests/public-config.test.cjs) | Creado |
| [mobile/tests/reminders.test.cjs](../../../mobile/tests/reminders.test.cjs) | Creado |
| [mobile/tests/request.test.cjs](../../../mobile/tests/request.test.cjs) | Creado |
| [mobile/tests/voice-component.test.cjs](../../../mobile/tests/voice-component.test.cjs) | Creado |
| [render.yaml](../../../render.yaml) | Creado |
| [scripts/check_candidate.py](../../../scripts/check_candidate.py) | Creado |
| [supabase/docs/CONEXION_SUPABASE.md](../../../supabase/docs/CONEXION_SUPABASE.md) | Modificado |
| [supabase/migrations/0010_fotografias_perfil.sql](../../../supabase/migrations/0010_fotografias_perfil.sql) | Creado |
