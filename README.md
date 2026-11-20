# FUGA+

**Descubre a dónde se va tu dinero.**

Aplicación para registrar gastos personales, visualizar hábitos de consumo e identificar posibles fugas mediante reglas automáticas.

**Entrega académica · 19 de noviembre de 2026.** La propietaria reporta un APK Android release instalado y probado, y un backend operativo en Render con Supabase. Esta revisión contrasta código, documentación y pruebas aisladas; no consulta servicios remotos ni certifica las migraciones aplicadas en producción.

## 1. Presentación de FUGA+

Los pequeños gastos cotidianos pueden acumularse sin que la persona recuerde en qué utilizó su dinero. FUGA+ facilita su registro por texto o voz y reúne historial, estadísticas y evidencia de patrones repetitivos.

Su objetivo es ayudar a comprender los hábitos de consumo, especialmente a jóvenes y estudiantes que necesitan organizar sus gastos sin herramientas financieras complejas. Maneja únicamente pesos colombianos (COP), con importes enteros positivos de COP 1 a COP 100.000.000 por gasto.

La interpretación usa diccionario, normalización y reglas versionadas, sin enviar gastos a una IA generativa. El dictado puede utilizar servicios del dispositivo; FUGA+ no guarda archivos de audio.

## 2. Funcionalidades implementadas

**Implementada** describe un flujo presente en código e integrado con sus servicios; su aceptación se distingue en la sección 8. **Parcial** identifica límites de plataforma, configuración o aceptación pendientes.

| Funcionalidad | Estado y alcance real |
| --- | --- |
| Bienvenida y autenticación | Implementadas: registro/login con Supabase Auth, persistencia y cierre de sesión. La aceptación del registro con confirmación por correo requiere comprobar proveedor y callback reales. |
| Sesión y permisos | Implementados: JWT verificado mediante JWKS; rol y estado consultados en PostgreSQL en cada solicitud. |
| Gastos por texto | Implementados: interpretación, borrador editable, confirmación explícita y almacenamiento idempotente bajo el propietario autenticado. |
| Gastos por voz | Implementados en Android: permiso de micrófono, dictado de hasta 30 segundos, transcripción editable y confirmación. Web/iOS conservan entrada escrita. |
| Historial | Implementado: paginación, filtros por fecha/categoría, edición y eliminación lógica, con actualización de resúmenes y análisis. |
| Estadísticas | Implementadas: total, cantidad, promedio, distribución por categoría, mayor gasto y comparación con el mes anterior. |
| Fugas | Implementadas: FUGA-01, agrupación por categoría/concepto canónico, snapshots versionados, evidencia propia y resumen mensual. |
| Notificaciones locales | Parciales por plataforma/ciclo de vida: avisos nativos con permiso, control de duplicados y apertura de evidencia; no disponibles en Expo Web. |
| Perfil y fotografía | Implementados: nombres/teléfono, galería, vista previa, confirmar/cancelar y carga firmada a Cloudinary. URL persistida en `public.perfil.foto_url` y registro de cargas. |
| Administración | Implementada: login habitual, búsqueda, filtros, paginación, detalle mínimo, estadísticas de cuentas/actividad y activación/desactivación de cuentas usuarias con confirmación. El reporte manual actual acredita acceso al módulo, no todas sus operaciones. |
| Google, foto Google y recuperación | Parciales en aceptación: existe código; OAuth/correo y sus redirecciones requieren configuración y verificación real. |
| Desactivación y retención | Desactivación/reactivación implementadas con sincronización Auth y auditoría. Retención parcial: se agenda una tarea a 30 días, sin supresión física automática. |

**FUGA-01 1.0:** ventana de hoy y los 29 días anteriores en `America/Bogota`; mínimo **3 gastos en 3 fechas distintas**, cada uno entre **COP 1.000 y COP 30.000**, con suma mínima de **COP 15.000**. Son los valores del código y catálogo SQL, no una consulta nueva de parámetros remotos. La normalización 1.1 también agrupa gastos antiguos sin reescribir descripciones y distingue conceptos como «café» y «café con leche».

Los roles persistidos son `usuario` y `administrador`. El administrador gestiona metadatos de cuentas y **no accede a finanzas individuales**. El operador asigna el primer rol administrativo sobre el perfil identificado por UUID; ni el registro público ni una pantalla de la app conceden ese privilegio.

## 3. Arquitectura y tecnologías

```text
React Native / Expo ── SDK Supabase ──> Supabase Auth
        │                              │ JWT / JWKS
        └── HTTPS /api/v1 ──> FastAPI en Render
                                  ├── SQLAlchemy / Psycopg / TLS ──> PostgreSQL en Supabase
                                  └── Firma y verificación ──> Cloudinary
        └── Carga directa de fotografía con firma ───────────> Cloudinary
```

| Capa | Implementación |
| --- | --- |
| Frontend | React Native `0.88.1`, Expo SDK `58`, React `19.3` y TypeScript `6`; Expo Web para flujos compatibles con navegador. |
| Android | Kotlin: `FugaVoice` con `SpeechRecognizer` y `FugaWindowInsets` para barras/teclado; `expo-notifications` para avisos locales. |
| Backend | Python `3.12`, FastAPI, Uvicorn, Pydantic, servicios, dominio determinista y repositorios con SQL parametrizado. |
| Identidad | Supabase Auth y PKCE; JWT RS256/ES256. SecureStore en nativo y localStorage en Web. FastAPI no emite tokens propios de usuario. |
| Persistencia y archivos | PostgreSQL, SQLAlchemy 2/Psycopg 3, RLS y autorización por propietario; Cloudinary con firma exclusiva del backend. |
| Alojamiento | Configuración de backend para Render Free; APK autónomo con acceso a servicios HTTPS. |

FastAPI es la única entrada a datos financieros. Su conexión SQL de servidor puede omitir RLS, por lo que los controles de rol, estado y propietario son obligatorios en la API.

Las migraciones `0001`–`0010` definen **11 tablas propias y 13 claves foráneas**, además de la referencia externa `auth.users`: `perfil`, `categoria`, `gasto`, `regla_fuga`, `regla_fuga_version`, `fuga`, `fuga_evidencia`, `auditoria`, `actividad_mensual`, `tarea_retencion` y `perfil_foto_carga`. El ER documenta UUID, nulabilidad y las excepciones de claves TEXT/compuestas. Este inventario describe los archivos SQL, no el estado remoto.

## 4. Estructura del repositorio

```text
mobile/              App Expo, pantallas, cliente API, módulos Kotlin y pruebas Node
backend/             FastAPI, reglas, repositorios, pruebas pytest y scripts operativos
supabase/            Migraciones, catálogo inicial y comprobaciones SQL
docs/                Arquitectura implementada, normalización, retención y dependencias
mi-framework-ia/     Framework de apoyo; requerimientos, historias, auditorías y UML
assets/              Recursos gráficos originales
scripts/             Comprobación del candidato e inventario de seguridad
.github/workflows/   Validación preparada para GitHub Actions
render.yaml          Configuración declarativa del backend
```

El framework de apoyo no es un servicio requerido por la app. Herramientas locales, keystore y archivos de acceso QA quedan fuera de Git.

## 5. Instalación y ejecución local

### Requisitos y dependencias

Python **3.12**, Node.js **24**, npm y una base PostgreSQL preparada. Android nativo requiere JDK **17** y Android SDK; consultar [Android local](mobile/docs/ANDROID_LOCAL.md). No se requieren Docker ni un servicio de IA.

PowerShell desde la raíz:

```powershell
python -m venv backend/.venv
backend/.venv/Scripts/python.exe -m pip install -r backend/requirements.lock
backend/.venv/Scripts/python.exe -m pip install --no-deps -e backend
cd mobile
npm ci
```

### Variables de entorno

Preparar `backend/.env.local` y `mobile/.env.local` a partir de sus plantillas `.env.example`, completándolos solo en el equipo de trabajo. No versionar esos archivos ni copiar sus valores a informes o logs.

| Variables del backend | Configuración necesaria |
| --- | --- |
| `APP_ENV`, `LOG_LEVEL` | `local` para desarrollo; `prod` y nivel de log permitido para producción. |
| `DATABASE_URL` | Controlador `postgresql+psycopg://`; conservar los componentes de Connect y codificar caracteres reservados de la contraseña. |
| `DATABASE_SSL_ROOT_CERT` | Para Supabase: `certs/prod-ca-2021.crt` y `sslmode=verify-full` en la conexión. Ruta resuelta desde `backend/`, también en Linux. |
| `SUPABASE_URL`, `SUPABASE_JWT_AUDIENCE` | Raíz HTTPS del proyecto y audiencia `authenticated`. Issuer/JWKS se derivan automáticamente; no conservar overrides de ejemplo innecesarios. |
| `SUPABASE_SERVICE_ROLE_KEY` | Secreto para sincronización administrativa Auth. La clave moderna `sb_secret_` se envía mediante `apikey`, sin tratarla como JWT. |
| `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` | Configuración de fotografías y firma desde FastAPI. |
| `CORS_ORIGINS` | Lista JSON de orígenes Web; desarrollo admite por defecto localhost en puertos 8081 y 19006. |

FastAPI local encuentra dotenv desde `backend/`, independientemente del directorio de lanzamiento. En `prod` utiliza las variables del servicio y no carga dotenv.

| Variables públicas del frontend | Uso |
| --- | --- |
| `EXPO_PUBLIC_API_URL` | Raíz de FastAPI, **sin `/api/v1`**; HTTPS pública de Render para release. |
| `EXPO_PUBLIC_SUPABASE_URL` | Raíz HTTPS del mismo proyecto Supabase. |
| `EXPO_PUBLIC_SUPABASE_ANON_KEY` | Clave pública moderna `sb_publishable_` o legacy `anon`; se conserva el nombre de variable. |
| `EXPO_PUBLIC_GOOGLE_ENABLED`, `EXPO_PUBLIC_PASSWORD_RECOVERY_ENABLED` | Activar solo tras configurar y comprobar cada proveedor. |
| `EXPO_PUBLIC_ADMIN_QA_MODE` | Ausente o `false` normalmente; desactivado obligatoriamente en release. |

Las variables `EXPO_PUBLIC_*` se incorporan al cliente. Nunca incluir conexión SQL, claves administrativas, contraseñas ni `CLOUDINARY_API_SECRET` en frontend/APK. Reiniciar Expo tras cambiarlas; un release instalado requiere recompilación para actualizar sus valores.

### Iniciar backend y frontend

Desde la raíz, en una terminal:

```powershell
backend/.venv/Scripts/python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Desde `mobile/`, en otra terminal:

```powershell
npm run web -- --localhost --port 8081
```

Abrir `http://localhost:8081`, con API `http://127.0.0.1:8000`. `/health` comprueba FastAPI, `/ready` ejecuta `SELECT 1` y `/docs` expone Swagger en desarrollo; las rutas funcionales usan `/api/v1`.

Web permite probar acceso y funciones por texto. Para nativo, `npm start` inicia Metro y `npm run android` genera/ejecuta Android con la toolchain instalada. **Expo Go no incluye los módulos Kotlin propios**: utilizar una compilación nativa de desarrollo.

Desde un teléfono, localhost es el dispositivo: usar IP LAN del computador, backend con `--host 0.0.0.0` y acceso de red privada, o seguir el [QA por USB](mobile/docs/QA_ANDROID_FUNCIONAL.md). El emulador Android usa `http://10.0.2.2:8000`. Esos destinos HTTP no se admiten para distribución release.

Registrar en Supabase Auth las redirecciones que se utilizarán:

- Nativo: `fugaplus://auth` y `fugaplus://auth?flow=recovery`.
- Web local: `http://localhost:8081/auth/callback` y `http://localhost:8081/auth/callback?flow=recovery`.

El callback intercambia código PKCE y limpia la URL, sin aceptar tokens en el enlace ni requerir una ruta FastAPI. Para correo Web, abrir la confirmación en el mismo navegador/perfil del registro; puede ser otra pestaña.

La app **no migra al arrancar**. Revisar el [orden de migraciones](supabase/docs/CONEXION_SUPABASE.md) antes de preparar una base. `0002` incorpora nueve categorías y FUGA-01; `seed.sql` es opcional. No reejecutar migraciones sobre datos existentes sin comparar esquema e historial.

## 6. Despliegue del backend

La propietaria reporta Render operativo y `/health` y `/ready` correctos. Aquí se revisaron [render.yaml](render.yaml) y [start.py](backend/scripts/start.py), sin acceder al servicio.

| Formulario de Render | Valor previsto |
| --- | --- |
| Servicio / plan / rama de entrega | Web Service Python / Free / `develop` |
| Root Directory | `backend` |
| Build Command | `pip install -r requirements.lock` |
| Start Command | `python scripts/start.py` |
| Health Check Path | `/health` |

Configurar las variables de backend anteriores, `APP_ENV=prod`, `PYTHON_VERSION=3.12.16`, `LOG_LEVEL=INFO` y audiencia `authenticated`. Credenciales Supabase y variables Cloudinary deben proporcionarse de forma privada en Render; las de Cloudinary no están declaradas en el YAML.

El [certificado público versionado](backend/certs/prod-ca-2021.crt) corresponde a `DATABASE_SSL_ROOT_CERT=certs/prod-ca-2021.crt` con raíz `backend`. Conservar `sslmode=verify-full`. El launcher usa `PORT`, un proceso y pool inicial de 3 conexiones más 2 adicionales.

En producción CORS admite orígenes HTTPS; `[]` es compatible con el cliente nativo. Añadir orígenes concretos si se publica Web. `/docs` está deshabilitado en `prod`: su 404 es esperado. `/health` solo verifica proceso y `/ready` conectividad SQL, **no** esquema, Auth, Cloudinary o funcionalidad completa.

No se afirma que todas las migraciones estén aplicadas en Supabase: la evidencia histórica HU-08 acredita `0010` local, sin confirmación posterior de aplicación remota en ese documento. El reporte de fotografías operativas no sustituye una verificación de tablas, índices y RLS.

## 7. APK Android release firmado

El procedimiento vigente es local, sin EAS Build. Paquete **`co.edu.fugaplus.app`**, versión **`0.1.0`**. Usar [APK release local](mobile/docs/APK_RELEASE_LOCAL.md), [Android local](mobile/docs/ANDROID_LOCAL.md) y los scripts [android-release.ps1](mobile/scripts/android-release.ps1), [android-release.cjs](mobile/scripts/android-release.cjs) y [android-local.ps1](mobile/scripts/android-local.ps1).

Requiere SDK/JDK, dependencias coincidentes con el lock, copia corta de compilación registrada localmente y keystore propio con alias `fugaplus-release`. Keystore y contraseñas quedan fuera de Git; conservarlos protegidos para futuras actualizaciones. No recrear la clave existente ni reemplazarla por debug.

Para una futura compilación autorizada, desde la raíz:

```powershell
powershell -NoProfile -File .\mobile\scripts\android-release.ps1 -Task Check
powershell -NoProfile -File .\mobile\scripts\android-release.ps1 -Task Prepare
powershell -NoProfile -File .\mobile\scripts\android-release.ps1 -Task Apk
```

`Check` valida sin compilar; `Prepare` sincroniza fuentes/firma; `Apk` compila y firma. El lanzador lee exclusivamente variables públicas permitidas de `mobile/.env.local`, exige HTTPS público, fuerza `EXPO_PUBLIC_ADMIN_QA_MODE=false` y `FUGA_RELEASE_BUILD=1`, y desactiva dotenv durante el build. El adaptador administrativo está limitado a debug y excluido del bundle release. No usar launchers de QA o bienvenida para distribución.

PowerShell solicita las contraseñas interactivamente; Gradle las recibe como variables temporales, sin incorporarlas al JavaScript. El [plugin de firma](mobile/plugins/withReleaseSigning.cjs) conserva la configuración tras prebuild.

Salida de la copia documentada:

```text
C:\fuga-plus-build-bd5fcedc\mobile\android\app\build\outputs\apk\release\app-release.apk
```

El destino depende de `.tools/android-short-build.json`, no versionado. Se genera `arm64-v8a`, con JavaScript incluido y sin instalación automática. El APK requiere Internet para los servicios HTTPS, **sin Metro, USB ni servidores del computador**. Una firma distinta puede impedir actualizar una instalación anterior; no borrar datos para resolverlo sin revisión.

El manual registra una preparación anterior a la firma. El APK final instalado y probado posteriormente es un resultado reportado por la propietaria; no se recompiló ni inspeccionó otro binario en esta revisión.

## 8. Pruebas y validaciones

| Procedencia | Resultado verificable y límites |
| --- | --- |
| Esta revisión, 2026-11-19 | **307 backend aprobadas, 39 omitidas, 0 fallos**; Python 3.12.6 y `test_safe.py`, sin dotenv real, PostgreSQL ni HTTP externo. Las omitidas requieren PostgreSQL local. |
| Esta revisión | **132 frontend aprobadas, 0 fallos, 0 omitidas; TypeScript aprobado**; Node 24.16.0. Componentes, lógica y configuración con proveedores/controles nativos simulados. |
| [QA administrativo documentado](mobile/docs/QA_ANDROID_ADMIN.md#validación-automatizada) | **346 backend aprobadas**, incluida integración SQL, y 124 frontend en esa etapa. PostgreSQL local desechable y Auth simulado; no repetido aquí ni atribuible a Supabase remoto. |
| [Evidencia HU-08](mi-framework-ia/docs/auditoria/evidencia-hu08-fotografia.json) | 325 backend, incluidas 31 SQL, y 97 frontend en esa etapa. Dos PNG sintéticos cargados a Cloudinary bajo autorización; URL solo en PostgreSQL local, persistencia y sustitución confirmadas físicamente. |
| [Plan de mejora](mi-framework-ia/docs/auditoria/ejecucion-plan-mejora-fugaplus.md) | Resultados históricos por fase: Windows/Linux, cobertura, arranque sintético y compilaciones iniciales. No describen por sí solos el release posterior. |
| Reporte actual de la propietaria | APK release físico: login, texto, voz, dashboard, fugas, notificaciones, fotografía persistente y acceso administrativo. Render/Supabase operativos según su reporte; no revalidados remotamente aquí. |

Los conteos de etapas distintas **no se suman**. Se observaron avisos de deprecación de Starlette/httpx y `react-test-renderer`, sin fallos. La cobertura histórica tiene exclusiones y no representa cobertura total de UI, Kotlin o proveedores.

Comandos reproducibles, primero desde la raíz y después desde `mobile/`:

```powershell
backend/.venv/Scripts/python.exe -B backend/scripts/test_safe.py
cd mobile
npm test
npm run typecheck
```

Para integración, configurar `FUGA_TEST_DATABASE_URL` solo contra un clúster PostgreSQL **local desechable**, con permisos para crear bases; desde la raíz:

```powershell
backend/.venv/Scripts/python.exe -B backend/scripts/test_safe.py --integration
```

El fixture aplica migraciones en una base temporal `fuga_test_*`, sustituye Auth y retira su propia base. Rechaza hosts remotos y `hostaddr`. No usar Supabase ni las bases QA que se quieran conservar.

Controles adicionales: `test_safe.py --coverage`, `npm run test:coverage`, Ruff `--select F,E9,I` y mypy sobre `backend/app/domain`. No se recalculó cobertura aquí. [validate.yml](.github/workflows/validate.yml) prepara CI y SQL local; su existencia no prueba una ejecución remota aprobada.

El [smoke Web](mobile/docs/smoke-web.json) y su [captura](mobile/docs/public-smoke.png) documentan navegación pública histórica sin login. Los ensayos [QA financiero](mobile/docs/QA_ANDROID_FUNCIONAL.md) y [administrativo](mobile/docs/QA_ANDROID_ADMIN.md) están separados de producción; no se iniciaron ni cambiaron en esta revisión.

## 9. Diagramas UML

Cuatro archivos editables conciliados con código/migraciones y **9 PNG de alta resolución, a 300 ppp**, para Word:

| Editable | Imágenes PNG |
| --- | --- |
| [Casos de uso](mi-framework-ia/docs/diagramas/diagrama-casos-uso.drawio) | [Acceso/perfil](mi-framework-ia/docs/diagramas/png/diagrama-casos-uso-01-acceso-perfil.png), [gastos/análisis](mi-framework-ia/docs/diagramas/png/diagrama-casos-uso-02-gastos-analisis.png), [administración](mi-framework-ia/docs/diagramas/png/diagrama-casos-uso-03-administracion.png) |
| [Clases](mi-framework-ia/docs/diagramas/diagrama-clases.drawio) | [Contratos](mi-framework-ia/docs/diagramas/png/diagrama-clases-01-contratos.png), [repositorios/fugas](mi-framework-ia/docs/diagramas/png/diagrama-clases-02-repositorios-fugas.png) |
| [Componentes](mi-framework-ia/docs/diagramas/diagrama-componentes.drawio) | [Componentes y despliegue](mi-framework-ia/docs/diagramas/png/diagrama-componentes.png) |
| [Entidad–relación](mi-framework-ia/docs/diagramas/diagrama-entidad-relacion.drawio) | [Completo](mi-framework-ia/docs/diagramas/png/diagrama-entidad-relacion-01-esquema-completo.png), [identidad/soporte](mi-framework-ia/docs/diagramas/png/diagrama-entidad-relacion-02-identidad-soporte.png), [finanzas/reglas](mi-framework-ia/docs/diagramas/png/diagrama-entidad-relacion-03-finanzas-reglas.png) |

El [índice UML](mi-framework-ia/docs/diagramas/README.md) detalla fuentes y dimensiones. El mapa de historias de esa carpeta conserva la especificación y puede incluir funciones previstas; no acredita implementación.

## 10. Estado actual y limitaciones

El núcleo financiero, las ampliaciones Android y la administración están integrados. Para cerrar la aceptación, conservar la diferencia entre pruebas aisladas, SQL local, teléfono y servicios desplegados:

- **Correo/Google:** falta evidencia integral de registro con confirmación, recuperación y OAuth reales. Las banderas no certifican configuración.
- **Administración:** acceso release reportado; documentar por separado búsquedas, filtros, estados contra Auth y revisión de todas sus pantallas/teclado si se presentan en la sustentación.
- **Android/Web:** voz solo Android; avisos locales sin soporte Web. Las [áreas seguras](mobile/docs/AREAS_SEGURAS_INTERNAS.md) se comprobaron en el Xiaomi; faltan otros modelos, iOS físico y pruebas adicionales de accesibilidad.
- **Notificaciones:** se originan al consultar análisis, con siete días entre avisos por patrón/versión y silencio 21:00–08:00 Bogotá. No hay push remoto ni análisis con la app cerrada; los demás estados/restricciones Android requieren evidencia específica.
- **Fotos/retención:** JPEG, PNG y WebP hasta 5.000.000 bytes. La limpieza de activos registrados es manual, con simulación previa; no hay cron ni supresión automática de cuentas. La carga no acredita un borrado real.
- **Conectividad:** sin modo financiero offline, caché financiera persistente o conversión de divisas. Lecturas: hasta dos intentos de 45 segundos y cancelación; mutaciones sin reenvío automático. Falta registrar el comportamiento real ante arranque lento del servicio desplegado.
- **Evidencia final:** consolidar esquema remoto, firma/hash del APK y recorridos de aceptación. `SELECT 1` y bundles JS no prueban esos puntos.
- **Dependencias:** la [revisión de seguridad](docs/DEPENDENCIAS_SEGURIDAD.md) es histórica; no se consultaron avisos nuevos ni se afirma ausencia actual de vulnerabilidades.

El alcance actual no incorpora metas de ahorro, límites mensuales ni IA generativa. Las prioridades Must/Should/Could/Won't de la especificación 3.0 se conservan; implementar voz adicional no reclasifica la matriz ni acredita todas las historias.

## 11. Documentación adicional

- [Arquitectura implementada](docs/ARQUITECTURA_FUGA_PLUS.md) y [seguridad del backend](backend/docs/seguridad.md).
- [Requerimientos definitivos 3.0](mi-framework-ia/docs/requerimientos/REQUERIMIENTOS.md) e [historias de usuario 3.0](mi-framework-ia/docs/historias-usuario/HISTORIAS_DE_USUARIO.md): especificación y prioridades, no aceptación automática.
- [Normalización](docs/NORMALIZACION_CONCEPTOS.md) y [retención operativa](docs/RETENCION_OPERATIVA.md).
- [Migraciones y conexión Supabase](supabase/docs/CONEXION_SUPABASE.md) y [comprobador SQL](supabase/tests/verificar_esquema.sql).
- [Auditoría inicial](mi-framework-ia/docs/auditoria/auditoria-tecnica-fugaplus.md), [plan de mejora](mi-framework-ia/docs/auditoria/plan-mejora-fugaplus.md) e [informe de ejecución](mi-framework-ia/docs/auditoria/ejecucion-plan-mejora-fugaplus.md).
- [Ensayo HU-08](mi-framework-ia/docs/auditoria/hu08-fotografia-perfil.md), [formularios y áreas seguras](mobile/docs/AREAS_SEGURAS_FORMULARIOS.md) y [bienvenida visual](mobile/docs/BIENVENIDA_VISUAL.md).
- [OpenAPI exportado](backend/docs/openapi.json): referencia estática que debe contrastarse con las rutas actuales.

Los manuales e informes registran etapas y pueden conservar estados anteriores, como firma pendiente o Render aún no desplegado. Este README distingue ese historial del código revisado y del reporte posterior de la propietaria, sin modificar retrospectivamente las evidencias.
