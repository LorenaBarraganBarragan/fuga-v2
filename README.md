# FUGA+
Descubre por dónde se va tu plata.

Aplicación React Native/Expo/TypeScript y API FastAPI con PostgreSQL en Supabase y Supabase Auth.
La interpretación usa reglas propias; no envía gastos a una IA generativa.

## Estado de esta entrega
Código integrado de acceso, gastos, historial, edición/borrado lógico, estadísticas,
fugas y evidencia, perfil y administración. También hay código de voz Android,
alertas locales, comparación mensual y resumen de fugas.

**No es una certificación de MVP terminado:** Supabase, correo, Google, Cloudinary y dispositivos
reales no se han verificado. Las migraciones se probaron en PostgreSQL local el 2026-11-16;
su aplicación y verificación en Supabase remoto siguen pendientes.
No se aplicaron migraciones remotas ni se hicieron commits o despliegues.

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
DATABASE_URL debe usar postgresql+psycopg:// y un rol servidor autorizado.
CORS_ORIGINS es una lista JSON. La configuración se encuentra desde backend/ sin depender
del directorio desde el que se lanza el proceso.

Las migraciones 0001…0009 deben revisarse antes de aplicarlas: **la aplicación no migra automáticamente**.
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
backend/.venv/Scripts/python -m pytest backend/tests --ignore=backend/tests/integration -q -p no:cacheprovider
backend/.venv/Scripts/ruff check backend/app backend/tests --select F,E9,I
backend/.venv/Scripts/mypy backend/app/domain --no-incremental
cd mobile
npm test
npm run typecheck
npx expo install --check
npx expo export --platform all
```

Pruebas PostgreSQL: autorizadas nuevamente el 2026-11-16 para una base local desechable;
la ronda completa pasa 165 pruebas, incluidas 14 de integración. Supabase remoto sigue sin verificar.
El fixture requiere FUGA_TEST_DATABASE_URL y rechaza hosts remotos. Crea y retira únicamente
su propia base con prefijo fuga_test_; el esquema auth de esas pruebas es un sustituto local del proveedor,
no una verificación de Supabase Auth real.

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
