# FUGA+
Descubre por dónde se va tu plata.

Aplicación React Native/Expo/TypeScript y API FastAPI con PostgreSQL en Supabase y Supabase Auth.
La interpretación usa reglas propias; no envía gastos a una IA generativa.

## Estado de esta entrega

El 2026-11-18 se autorizó ejecutar ACT-01 a ACT-15 desde el respaldo `ce24348`.
El [informe de ejecución](mi-framework-ia/docs/auditoria/ejecucion-plan-mejora-fugaplus.md)
contiene resultados actuales, archivos y límites; la auditoría es una fotografía anterior.
Se conserva el núcleo 3.0 y se prioriza además voz Android. No se cambian umbrales de FUGA-01.
Código integrado de acceso, gastos, historial, edición/borrado lógico, estadísticas,
fugas y evidencia, perfil y administración. También hay código de voz Android,
alertas locales, comparación mensual y resumen de fugas.

Verificación actual: 325 pruebas backend (31 SQL locales), 97 frontend y controles
mínimos de tipos/análisis aprobados. El release inicial abre sin Metro. En el posterior
debug QA por USB se comprobaron acceso con cuenta ficticia, texto/dashboard, dictado y
aviso local/toque/sin duplicado. La configuración pública se carga explícitamente en
memoria; los gastos se guardan en PostgreSQL local, sin escribir finanzas en Supabase.
Consulta [QA Android funcional](mobile/docs/QA_ANDROID_FUNCIONAL.md) para ejecutar ese
entorno. El debug funcional requiere Metro; no sustituye un release configurado con API HTTPS.

HU-08 incorpora vista previa/confirmación de fotografía y gestión segura de cargas.
Cloudinary responde a GET /ping; dos PNG sintéticos autorizados se cargaron desde Android,
con cancelación, sustitución y persistencia tras login/logout confirmadas en QA local.
Ver [ensayo HU-08](mi-framework-ia/docs/auditoria/hu08-fotografia-perfil.md).
La migración nueva 0010 se probó localmente y no se aplicó en Supabase.

**No es una certificación de MVP terminado:** distinguir pruebas locales, teléfono y proveedores.
Este plan prueba SQL en PostgreSQL local desechable; no recertifica el Supabase real ya
validado anteriormente por la propietaria. Correo, Google, Cloudinary y flujos completos
de dispositivo requieren su propia evidencia. No se aplican migraciones remotas ni se
hacen commits, pushes o despliegues durante la ejecución del plan.

- [Progreso y siguiente tarea](mi-framework-ia/docs/planificacion/PROGRESO_BUILD.md)
- [Arquitectura y límites de seguridad](docs/ARQUITECTURA_FUGA_PLUS.md)
- [Migraciones revisadas y conexión a Supabase](supabase/docs/CONEXION_SUPABASE.md)
- [Informe y archivos de la entrega](docs/IMPLEMENTACION_2026-11-15.md)
- [Historias oficiales 3.0](mi-framework-ia/docs/historias-usuario/HISTORIAS_DE_USUARIO.md)
- [Requerimientos oficiales 3.0](mi-framework-ia/docs/requerimientos/REQUERIMIENTOS.md)

## Ejecutar el backend (PowerShell desde la raíz)
Python 3.12. En esta ejecución el entorno backend/.venv ya está instalado y aislado.
Para reconstruirlo en otra máquina:

```powershell
python -m venv backend/.venv
backend/.venv/Scripts/python -m pip install --upgrade pip
backend/.venv/Scripts/python -m pip install -r backend/requirements.lock
backend/.venv/Scripts/python -m pip install --no-deps -e backend
```

Copiar backend/.env.example a backend/.env.local y completar los valores reales, sin versionarlos.
DATABASE_URL debe usar postgresql+psycopg://, un rol servidor autorizado y sslmode=verify-full.
DATABASE_SSL_ROOT_CERT resuelve la CA pública desde backend, también en Linux, sin
reescribir la cadena guardada. Settings valida prod sin mostrar entradas sensibles.
CORS_ORIGINS es una lista JSON. La configuración se encuentra desde backend/ sin depender
del directorio desde el que se lanza el proceso.

Las migraciones 0001…0010 deben revisarse antes de aplicarlas: **la aplicación no migra automáticamente**.
No ejecutar scripts sobre Supabase remoto sin aprobación.
El catálogo real proviene de PostgreSQL; la API no sustituye fallas por datos ficticios.

```powershell
backend/.venv/Scripts/python -m uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000
```

/health verifica el proceso. /ready requiere conexión real a la BD.
/docs presenta los contratos en desarrollo. En producción configurar HTTPS y CORS restringido.
Los tokens deben estar firmados por claves asimétricas publicadas en JWKS de Supabase (RS256/ES256).
No se admiten JWT sin firma ni claves de prueba en ejecución normal.

## Ejecutar el móvil
Node 24 compatible con el SDK instalado. El lockfile fija Expo 58 y sus versiones compatibles.

```powershell
cd mobile
npm ci
npm start
```

Copiar mobile/.env.example a mobile/.env.local y completar:
- EXPO_PUBLIC_API_URL: http://10.0.2.2:8000 para emulador Android, o IP LAN del servidor para dispositivo físico.
- EXPO_PUBLIC_SUPABASE_URL y EXPO_PUBLIC_SUPABASE_ANON_KEY: valores públicos del proyecto.
- EXPO_PUBLIC_PASSWORD_RECOVERY_ENABLED=true solo cuando el correo saliente esté realmente configurado.
- EXPO_PUBLIC_GOOGLE_ENABLED=true solo después de configurar Google OAuth en Supabase.

Nunca incluir DATABASE_URL, service role ni secretos de Cloudinary en el móvil.
Registrar fugaplus://auth y fugaplus://auth?flow=recovery en las redirecciones de Supabase.

Para Expo Web, usar `npm run web -- --localhost --port 8081` y abrir `http://localhost:8081`.
En Supabase → Authentication → URL Configuration, añadir las redirecciones exactas
`http://localhost:8081/auth/callback` y `http://localhost:8081/auth/callback?flow=recovery`,
sin retirar las direcciones nativas anteriores. El callback intercambia el código mediante PKCE
y limpia la URL; no acepta tokens de sesión en la URL. No requiere una ruta nueva en FastAPI.
La confirmación debe abrirse en el mismo navegador y perfil donde se inició el registro;
se admite otra pestaña porque el verificador PKCE y la sesión web usan localStorage.
Los dispositivos nativos conservan SecureStore. En Web, `EXPO_PUBLIC_API_URL` puede ser
`http://127.0.0.1:8000`, sin `/api/v1`; `EXPO_PUBLIC_SUPABASE_ANON_KEY` admite una clave
publishable pública, nunca una clave secret/service role. Expo carga `mobile/.env.local`;
reiniciar Expo después de cambiar esas variables. Google y recuperación siguen condicionados
a su configuración y a las banderas existentes.

Para Android nativo, instalar antes el Android SDK, licencias y JDK compatible con el SDK Expo:
```powershell
cd mobile
npm run android
```
El módulo de voz Kotlin se autovincula desde mobile/modules/fuga-voice.
Requiere un development build; no se promete voz en Expo Go. iOS conserva entrada de texto;
la compilación iOS requiere un entorno macOS/Xcode. Generar un bundle JS no equivale a crear un APK/IPA.

## Configuración de ampliaciones
- Google: proveedor habilitado y credenciales/redirecciones verificadas; vinculación mediante Supabase.
- Recuperación: SMTP/correo y enlace de un solo uso gestionados por Supabase. Sin configurar, se muestra indisponibilidad.
- Fotos: CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY y CLOUDINARY_API_SECRET solo en backend/.env.local.
  Carga firmada y verificación servidor de propietario, formato y máximo 5 MB antes de guardar la URL.
- Administración: aprovisionar el rol administrador por un mecanismo seguro del operador,
  nunca desde registro ni metadatos editables. Configurar SUPABASE_SERVICE_ROLE_KEY en el backend
  para sincronizar bloqueo/reactivación con Auth. Los gastos individuales están denegados a administradores.
- Retención: se programan tareas a 30 días sin borrar datos automáticamente. La supresión efectiva y
  el mantenimiento de auditoría a 90 días requieren revisión y autorización antes de operar sobre datos reales.

## Pruebas
Sin PostgreSQL:
```powershell
backend/.venv/Scripts/python -B backend/scripts/test_safe.py --coverage
backend/.venv/Scripts/ruff check backend/app backend/tests --select F,E9,I
backend/.venv/Scripts/mypy backend/app/domain --no-incremental
cd mobile
npm run test:coverage
npm run typecheck
npx expo install --check
npx expo export --platform all
```

Pruebas PostgreSQL: autorizadas para una base local desechable; los totales actuales
y cobertura están en el informe de ejecución, sin confundirlos con Supabase remoto.
El fixture requiere FUGA_TEST_DATABASE_URL y rechaza hosts remotos. Crea y retira únicamente
su propia base con prefijo fuga_test_; el esquema auth de esas pruebas es un sustituto local del proveedor,
no una verificación de Supabase Auth real. El lanzador elimina dotenv y HTTP externo.

Para un clúster local ya preparado y autorizado:
```powershell
$env:FUGA_TEST_DATABASE_URL='postgresql://fuga_test@127.0.0.1:55440/postgres'
backend/.venv/Scripts/python -B backend/scripts/test_safe.py --integration --coverage
```

[Android local y validación](mobile/docs/ANDROID_LOCAL.md) describe el script
`mobile/scripts/android-local.ps1`, SDK, manifiesto y diferencia entre APK y Expo Go.
app.config.js bloquea claves privadas antes de empaquetar. La compilación automatizada
de esta sesión no carga .env.local. Un APK sin configuración pública no certifica finanzas.

[Retención operativa](docs/RETENCION_OPERATIVA.md) define revisión, FK y límites de supresión.
`render.yaml` y `.github/workflows/validate.yml` preparan alojamiento y validación;
no crean servicios, despliegan ni acceden a datos reales. El launcher usa PORT y un proceso.
Las lecturas del cliente tienen hasta dos intentos cancelables de 45 s; mutaciones no
se reenvían automáticamente. Una respuesta de una sesión anterior se descarta.

Smoke público con Chrome existente, sin credenciales y perfil temporal:
1. Exportar web con npx expo export --platform web desde mobile/.
2. Servir desde la raíz con python -m http.server 8766 --bind 127.0.0.1 --directory mobile/dist.
3. En otra terminal: backend/.venv/Scripts/python mobile/scripts/smoke_web.py.
No prueba cuentas reales ni el flujo privado. Ver mobile/docs/smoke-web.json y public-smoke.png.

## Referencias técnicas
- https://supabase.com/docs/guides/auth/quickstarts/react-native
- https://docs.expo.dev/versions/latest/
- https://docs.expo.dev/modules/module-api/
- https://pyjwt.readthedocs.io/en/stable/usage.html
