# Plan de mejora de FUGA+

**Fecha:** 2026-11-18, America/Bogota.  
**Versión:** 1.0. Propuesta para revisión y aprobación; ninguna actividad de implementación se ejecuta con este documento.  
**Fuente:** [Auditoría técnica](auditoria-tecnica-fugaplus.md), hallazgos AUD-01 a AUD-14.  
**Restricciones:** Android prioritario, presupuesto cero, conservar Expo/React Native/TypeScript, FastAPI, PostgreSQL/Supabase Auth y procesamiento determinista. Sin migraciones remotas, datos reales, commits, pushes o despliegues por efecto de este plan.

## 1. Objetivos y alcance de entrega

1. Entregar el núcleo Must Have existente con evidencia funcional Android y sin regresiones de dinero, fechas, idempotencia, aislamiento ni FUGA-01.
2. Habilitar y validar la voz como prioridad adicional de esta entrega, reutilizando Kotlin/SpeechRecognizer y confirmación editable.
3. Obtener una compilación Android reproducible y posteriormente un APK instalable que funcione sin Metro.
4. Preparar FastAPI para Render con configuración segura, TLS PostgreSQL verificado, tolerancia acotada a arranque frío y costos controlados.
5. Consolidar pruebas y análisis estático mínimos y un manual técnico con evidencia fechada.

No se cambia el alcance documental de las HU: la línea base 3.0 mantiene voz y notificaciones como Could Have. La priorización de voz procede del prompt de auditoría y del objetivo Android, y deberá anotarse como decisión de entrega en una actualización documental autorizada. Google, imágenes, administración avanzada, sugerencias, push remoto y nuevos presupuestos no son requisitos para cerrar el núcleo.

No son objetivos: refactorización global, cobertura perfecta, reescritura de navegación, escalado horizontal, nueva base de datos, IA generativa ni nuevos servicios de pago.

## 2. Línea base comprobada

| Verificación | Resultado actual | Alcance |
|---|---|---|
| Backend | 255 aprobadas, 14 omitidas, una advertencia upstream | Suite aislada sin dotenv, HTTP externo ni BD real |
| Frontend | 44 aprobadas | Reglas y callbacks PKCE; sin componentes o hardware |
| TypeScript | Correcto | Configuración estricta actual |
| mypy | Correcto, 13 archivos | Dominio; no certifica servicios ni rutas completos |
| Ruff mínimo | 0 incidencias F/E9/I | Control mínimo viable actual |
| Ruff completo | 210 avisos | Requiere revisar reglas; no equivale a 210 vulnerabilidades |
| Dependencias | Reportes almacenados con 0 vulnerabilidades | Sin consulta nueva de avisos en la auditoría |
| Android | Bloqueo RECORD_AUDIO reproducido en memoria del plugin | Sin compilación ni permiso real probado |
| Supabase/Render | Sin operaciones reales durante la auditoría | Los antecedentes de Supabase no se revalidaron |

Los conteos son referencia, no criterio de congelación: al añadir pruebas deben registrarse los nuevos totales y no esconderse fallos u omisiones.

## 3. Arquitectura objetivo y decisiones que se conservan

Mantener aplicación Android → Supabase Auth para identidad y Android → FastAPI para finanzas. FastAPI conserva validación JWKS y autorización por rol/propietario, se conecta a Supabase PostgreSQL mediante SQLAlchemy/Psycopg y ejecuta el dominio determinista local. Mantener RLS como defensa de la vía cliente, sin convertirlo en sustituto del filtrado servidor con credenciales privilegiadas.

La arquitectura objetivo y el diagrama de componentes están en la sección 10 de la auditoría. Las mejoras son puntuales: resolver permisos, cerrar pruebas, simplificar trabajo redundante, validar configuración y preparar entrega. El plan no presupone nuevos contratos HTTP ni tablas. Si una actividad los necesita, presentar primero una propuesta compatible, impacto y aceptación; no cambiar silenciosamente clientes ni SQL remoto.

## 4. Actividades priorizadas

Cada actividad requiere autorización de implementación posterior. Complejidad baja/media/alta expresa esfuerzo relativo, no una promesa de duración. Las prioridades condicionadas se vuelven obligatorias solo si se incluye el componente indicado.

### ACT-01 — Fijar alcance y evidencia de referencia

- **Problemas:** AUD-03, AUD-11, AUD-12.
- **Archivos/módulos:** requerimientos e historias 3.0, README, PROGRESO_BUILD, arquitectura y documentos de auditoría.
- **Acción:** registrar núcleo obligatorio, voz priorizada y ampliaciones incluidas; conservar una lista de archivos y resultados sin secretos; resolver el nombre y final incompleto del prompt.
- **Herramientas:** Markdown, Git de lectura y pruebas existentes.
- **Dependencias:** ninguna; revisión de estos dos documentos.
- **Complejidad / prioridad:** baja / P1.
- **Aceptación:** una única descripción de entrega y matriz de evidencia distinguen documentado, implementado, probado localmente y probado en dispositivo/proveedor.
- **Validación:** enlaces existentes y contraste con código, sin afirmar que Web, bundles o mocks certifican Android.

### ACT-02 — Corregir bloqueo global del micrófono

- **Problema:** AUD-01.
- **Archivos/módulos:** `mobile/app.json`, manifiesto del módulo FugaVoice y configuración del plugin de imágenes.
- **Acción:** retirar el bloqueo global de RECORD_AUDIO sin habilitar cámara; conservar la solicitud contextual y el módulo Kotlin actual.
- **Herramientas:** Expo config plugins, inspección en memoria y manifiesto fusionado de Gradle.
- **Dependencias:** ACT-01; herramienta Android de ACT-03 para validación completa.
- **Complejidad / prioridad:** baja / **P0**.
- **Aceptación:** manifiesto efectivo con permiso de micrófono, sin `tools:node="remove"` para RECORD_AUDIO, y sin solicitud de cámara no requerida.
- **Validación:** conceder/denegar micrófono, dictar una frase, editar transcripción, cancelar y comprobar que no se guarda gasto sin confirmar.

### ACT-03 — Preparar compilación Android local y prueba de voz

- **Problemas:** AUD-02 y parte de AUD-03.
- **Archivos/módulos:** `mobile/package.json`, `mobile/app.json`, `mobile/modules/fuga-voice`, `mobile/src/voice/VoiceInput.tsx`.
- **Acción:** localizar o instalar en una etapa autorizada SDK/JDK compatibles, ADB y licencias; conectar teléfono y compilar debug. No reemplazar Kotlin por otro servicio.
- **Herramientas:** Android SDK, Gradle wrapper generado, Expo CLI y teléfono; `expo-dev-client` solo si se decide usar su experiencia de desarrollo.
- **Dependencias:** ACT-02 para aceptar voz; preparación de herramientas puede avanzar en paralelo.
- **Complejidad / prioridad:** media / P1.
- **Aceptación:** debug propio instala, carga FugaVoice, procesa texto de máximo 280 caracteres, limita captura y conserva alternativa escrita. Se registran versiones efectivas de JDK/SDK.
- **Validación:** es-CO, fallback disponible, permiso denegado, recognizer ausente, detener, cancelar, segundo plano, nueva captura y sin archivos de audio persistidos.

### ACT-04 — Cerrar regresiones backend, SQL y aislamiento

- **Problema:** AUD-03.
- **Archivos/módulos:** `backend/tests`, fixture de integración, migraciones 0001–0009 y dominio de gastos/fugas.
- **Acción:** mantener suite aislada; ejecutar integración solo contra PostgreSQL local desechable; añadir casos faltantes cuando exista un defecto o riesgo concreto. No apuntar TEST_DATABASE_URL a Supabase.
- **Herramientas:** Pytest, PostgreSQL local autorizado y firmas de prueba. La variable existente es **FUGA_TEST_DATABASE_URL**; usar su nombre real.
- **Dependencias:** ACT-01; PostgreSQL local disponible y autorizado. La variante sin BD no depende de Android.
- **Complejidad / prioridad:** media / P1.
- **Aceptación:** suite actual sin fallos; 14 pruebas SQL ejecutadas o bloqueo explícito que impide cerrar la aceptación SQL; pruebas A/B/admin preservan privacidad y restricciones.
- **Validación:** JWT inválido/expirado y JWKS caído; rol manipulado; acceso cruzado; RLS cliente sin filas; idempotencia concurrente; edición/eliminación; reaplicación no destructiva en base desechable.

### ACT-05 — Probar cliente y callbacks más allá de funciones puras

- **Problemas:** AUD-02, AUD-03.
- **Archivos/módulos:** `mobile/src/auth`, AuthProvider, NewExpense, History, ExpenseForm, `lib/api.ts`, App y pruebas.
- **Acción:** añadir pruebas dirigidas a confirmación, conservación de clave en reintento, cambio de cuenta, descarte de borrador y error de carga; seleccionar el mínimo soporte de componentes necesario en etapa autorizada.
- **Herramientas:** pruebas Node existentes; herramienta compatible de componentes solo si hace falta, TypeScript y pruebas manuales Android.
- **Dependencias:** ACT-01; ACT-03 para evidencia de callbacks nativos. No sustituir las pruebas PKCE actuales.
- **Complejidad / prioridad:** media / P1.
- **Aceptación:** una sesión no muestra datos anteriores, un borrador no se guarda al navegar y reintentar no duplica gasto. Callback web conserva origen exacto y nativo usa esquema propio.
- **Validación:** sesión restaurada/vencida, error de red, otra pestaña web, código duplicado, retorno desde correo en Android y navegación después de logout.

### ACT-06 — Definir controles de calidad y cobertura proporcionados

- **Problemas:** AUD-09 y parte de AUD-03.
- **Archivos/módulos:** `backend/pyproject.toml`, fuentes intervenidas, `mobile/package.json`, pruebas y documentación de herramientas.
- **Acción:** mantener Ruff F/E9/I, mypy y TypeScript; revisar B008, SQL interno y firmas antes de imponer reglas completas. Corregir avisos relevantes en archivos tocados. Definir cobertura de reglas críticas; no refactorizar todo para un número.
- **Herramientas:** Ruff y mypy existentes. Pylint/Flake8 no se incorporan por duplicidad. Cobertura y ESLint requieren instalación/configuración posterior solo si se aprueban.
- **Dependencias:** ACT-04/05 para establecer los flujos críticos; los controles existentes pueden correr antes.
- **Complejidad / prioridad:** media / P1 para control mínimo; ESLint y limpieza global pueden posponerse.
- **Aceptación:** controles mínimos verdes, excepciones motivadas y reporte que no confunda avisos con vulnerabilidades. Casos críticos ejercitados aunque no se alcance cobertura global perfecta.
- **Validación:** análisis sin autofix y pruebas tras cada cambio pequeño; conservar la advertencia upstream como pendiente no bloqueante si no causa fallos.

### ACT-07 — Reducir trabajo repetido del análisis sin cambiar resultados

- **Problema:** AUD-06.
- **Archivos/módulos:** `backend/app/services/leaks_service.py`, repositorios, seguridad y tests de fugas.
- **Acción:** medir consultas/escrituras actuales; reutilizar datos y evitar invalidar/reactivar sin cambios cuando sea seguro. Separar gradualmente persistencia repetida. No convertir GET en otro contrato durante esta mejora sin propuesta compatible.
- **Herramientas:** Pytest con contadores de consultas y PostgreSQL desechable; medición local.
- **Dependencias:** ACT-04; no debe desplazar la corrección de voz.
- **Complejidad / prioridad:** media / P1 de eficiencia; no bloquea validación inicial con pocos datos si se acepta la limitación.
- **Aceptación:** candidatos, evidencia, versiones y aislamiento iguales; reducción demostrable de trabajo en consultas repetidas.
- **Validación:** cuatro cafés → COP 20.000; conceptos distintos separados; misma evidencia conserva identidad; edición, borrado, cambio de día, ventana y versión del normalizador recalculan correctamente; concurrencia sin snapshots vigentes duplicados.

### ACT-08 — Optimización medida del dashboard

- **Problema:** AUD-07.
- **Archivos/módulos:** Dashboard, `analytics_service.py` y dominio de agregaciones.
- **Acción:** comparar consultas con volumen académico razonable; si se justifica, agregar en SQL/reutilizar resultados y cargar comparación opcional bajo solicitud. Conservar contratos públicos por defecto.
- **Herramientas:** SQLAlchemy, PostgreSQL local, Pytest y medición de tiempos/filas.
- **Dependencias:** ACT-04; ejecutar únicamente si la medición o el costo de la mejora lo justifica.
- **Complejidad / prioridad:** baja/media / P2.
- **Aceptación:** menos lecturas o filas sin diferencias de sumas, promedios, porcentajes y empates.
- **Validación:** mes vacío, diciembre/enero, Otros, importes extremos permitidos, redondeo y comparación con base cero.

### ACT-09 — Cerrar notificaciones locales si se incluyen

- **Problema:** AUD-08.
- **Archivos/módulos:** `mobile/src/lib/notifications.ts`, `validation.ts`, `screens/Leaks.tsx`, App y pruebas.
- **Acción:** asociar canal, serializar intentos por clave de candidato y dar un error genérico observable. Mantener usuario/categoría/concepto/versión, siete días y horario. No añadir push remotas o análisis de fondo.
- **Herramientas:** expo-notifications y SecureStore existentes, mocks y teléfono Android.
- **Dependencias:** ACT-03/05. Puede posponerse si HU-25 se excluye expresamente de la entrega.
- **Complejidad / prioridad:** baja/media / P1 condicionado a HU-25.
- **Aceptación:** aviso local con texto genérico, canal correcto y sin duplicados bajo concurrencia; la falta de permiso no impide consultar fugas.
- **Validación:** Web sigue indicando indisponibilidad; Android con permiso denegado/concedido, canal bloqueado, 08:00/21:00 Bogotá, límite de siete días, toque con otra sesión y arranque desde notificación.

### ACT-10 — Cerrar configuración de entornos y secretos

- **Problema:** AUD-05.
- **Archivos/módulos:** Settings, cliente Supabase, `.env.example`, certificado público, README y futura configuración Render.
- **Acción:** validar configuración obligatoria del entorno de entrega, distinguir prod de local, rechazar claves privadas en configuración pública y documentar variables solo por nombre. Proporcionar la CA mediante archivo público revisado o mecanismo de archivo del alojamiento.
- **Herramientas:** Pydantic Settings, configuración Expo/Render y pruebas sintéticas. No se necesitan tecnologías nuevas.
- **Dependencias:** ACT-01 y ACT-04 para pruebas de configuración. No leer/imprimir secretos en reportes o pipelines.
- **Complejidad / prioridad:** media / P1.
- **Aceptación:** Python 3.12, URL Auth raíz coherente, issuer/JWKS derivados o explícitos correctos, DATABASE_URL Psycopg, `sslmode=verify-full`, CA accesible en Linux y CORS explícito para Web. Clave sb_secret solo backend/apikey; Android contiene solo valores públicos.
- **Validación:** configuración incompleta, clave secret en cliente, CA ausente y URL incorrecta fallan de forma segura; salud y readiness distinguen proceso de dependencia. Verificar conexión real solo cuando se autorice.

### ACT-11 — Manejar arranque frío y reintentos seguros

- **Problema:** AUD-04.
- **Archivos/módulos:** `mobile/src/lib/api.ts`, pantallas de error/carga y pruebas de idempotencia.
- **Acción:** diferenciar espera de arranque y error final; usar reintentos acotados y cancelables en lecturas. Para confirmación conservar el intento y su UUID; no reintentar automáticamente mutaciones sin garantías.
- **Herramientas:** fetch/AbortController y pruebas con temporización controlada existentes o mínimas.
- **Dependencias:** ACT-05/10; se puede simular antes de Render.
- **Complejidad / prioridad:** baja/media / P1 antes de elegir Render Free para la entrega.
- **Aceptación:** una demora superior a 15 segundos tiene salida comprensible, sin espera infinita; un POST cuya respuesta se pierde no crea dos gastos.
- **Validación:** backend lento, sin red, error 503 y cancelación; posteriormente primera petición tras suspensión real, sin monitores destinados a eludir la inactividad.

### ACT-12 — Preparar versión candidata y CI sin despliegue

- **Problemas:** AUD-10 y AUD-11.
- **Archivos/módulos:** lista de fuentes/locks/migraciones, `.gitignore`, futuras `.github/workflows` y documentación de ejecución.
- **Acción:** revisar cambios y archivos no rastreados; preparar una lista revisable para control de versiones, ejecutar checkout limpio solo tras autorización y añadir workflow mínimo de pruebas/tipado. No publicar automáticamente.
- **Herramientas:** Git, GitHub Actions si su cuota gratuita lo permite, Python 3.12 y Node compatible con el SDK. PostgreSQL desechable local al runner puede añadirse en job separado; no se impone Docker.
- **Dependencias:** ACT-04/05/06/10; autorización separada para commit/push cuando corresponda.
- **Complejidad / prioridad:** baja/media / P1 para reproducibilidad; ejecución remota de CI no sustituye validación local.
- **Aceptación:** revisión limpia reproduce código auditado y módulo nativo; workflow no carga .env reales ni usa claves Supabase, y distingue omisiones SQL de aprobación completa.
- **Validación:** prueba que falla intencionadamente bloquea validación; escaneo de archivos y bundle sin secretos; resultado de pipeline asociado a una revisión identificable.

### ACT-13 — Preparar ficha Render y ensayo de arranque Linux

- **Problemas:** AUD-04, AUD-05 y riesgo AUD-14.
- **Archivos/módulos:** README, lock backend, futura ficha/`render.yaml` si se decide, engine y endpoints de salud.
- **Acción:** documentar raíz `backend`, Python 3.12, build y start con puerto de plataforma; verificar imports, CA, logs a consola y configuración por entorno. Comenzar con un proceso y presupuesto de conexiones revisado.
- **Herramientas:** entorno Linux de prueba o runner gratuito, Uvicorn y Render Free después de autorización. No crear segunda base de datos en Render.
- **Dependencias:** ACT-10/11/12.
- **Complejidad / prioridad:** baja/media / P1 de preparación; métricas extensas P2.
- **Aceptación:** servicio arranca con configuración correcta, liveness/readiness definidos, sin archivos de datos persistidos localmente y procedimiento de recuperación documentado. Ningún cambio remoto ocurre por aprobar solo la ficha.
- **Validación:** arranque en limpio, SSL, logs sin secretos, parámetros de puerto, falta de dependencia y pérdida de filesystem simulada; despliegue real pertenece a autorización posterior.

### ACT-14 — Documentar retención proporcional al prototipo

- **Problema:** AUD-13.
- **Archivos/módulos:** `tarea_retencion`, `auditoria`, FK relacionadas, módulo de cuentas y manual operativo.
- **Acción:** definir procedimiento revisable para 30 días, recuperación, auditoría a 90 días y respaldos; usar datos ficticios durante validación. No implementar borrado automático de datos actuales.
- **Herramientas:** PostgreSQL desechable y documentación; automatización solo si se necesita después.
- **Dependencias:** ACT-04 y decisión de operar con usuarios reales.
- **Complejidad / prioridad:** media / P1 para usuarios reales; puede documentarse como limitación si la entrega usa exclusivamente datos de prueba.
- **Aceptación:** no se promete supresión ya implementada; orden y preservación de auditoría son coherentes con FK y política de producto.
- **Validación:** simulación de vencimiento y reactivación sin afectar cuentas ajenas; revisión humana del procedimiento antes de ejecutar cualquier limpieza.

### ACT-15 — Validación final Android y paquete de evidencias

- **Problemas:** AUD-02, AUD-03, AUD-11, AUD-12.
- **Archivos/módulos:** App completa, módulo Kotlin, callbacks, documentación técnica y futuro APK candidato.
- **Acción:** producir APK instalable, identificar revisión/versión y ejecutar flujos sobre datos de prueba autorizados; actualizar manual con resultados y límites. No publicar en tiendas por esta actividad.
- **Herramientas:** toolchain local Android, teléfono, pruebas existentes y capturas sanitizadas.
- **Dependencias:** ACT-02/03/04/05/06/10/11/12; ACT-09 si se incluye HU-25; ACT-13 para preparar backend remoto y ACT-14 si habrá usuarios reales.
- **Complejidad / prioridad:** media / P1.
- **Aceptación:** APK inicia sin Metro, texto y voz funcionan, datos aislados, resultados financieros correctos y límites conocidos registrados; no depende de credenciales en el binario.
- **Validación:** matriz de la sección 6, con evidencias de dispositivo, sin correos reales, identificadores personales o tokens en capturas.

## 5. Fases y dependencias

| Fase | Actividades | Resultado revisable | Puerta de salida |
|---|---|---|---|
| 0. Aprobación del diagnóstico | ACT-01 | Alcance y lista de trabajo aceptados | No implementar por inferencia de este plan |
| 1. Funcionamiento Android prioritario | ACT-02 y ACT-03; comenzar ACT-04 | Micrófono sin bloqueo y debug propio | Permiso y dictado comprobados; texto sigue funcionando |
| 2. Calidad, seguridad y regresiones | ACT-04, ACT-05, ACT-06 | Pruebas y controles mínimos reproducibles | Núcleo y aislamiento probados; SQL pendiente identificado si no puede ejecutarse |
| 3. Eficiencia y ampliaciones incluidas | ACT-07; ACT-08 solo si se justifica; ACT-09 si se incluye | Menor trabajo medido y avisos Android verificables | Sin alterar umbrales, evidencia ni contratos; P2 puede aplazarse |
| 4. Preparación de infraestructura | ACT-10, ACT-11, ACT-12, ACT-13; ACT-14 según uso | Configuración Linux/Render y revisión candidata | SSL/secretos/arranque/reintentos revisados, sin despliegue remoto automático |
| 5. Candidato Android y manual | ACT-15 y cierre documental | APK y expediente de evidencia | Cumplir sección 9 y solicitar autorización concreta de despliegue |

ACT-10 puede adelantarse si bloquea la prueba Android de conexión. La preparación de herramientas de ACT-03 puede hacerse junto a pruebas locales, pero corregir micrófono precede a la aceptación de voz. No ejecutar optimizaciones o ampliaciones simultáneamente al primer cambio crítico.

El riesgo de presupuesto de conexiones/rate limiting de AUD-14 se revisa en ACT-13 con carga local modesta; una implementación dedicada queda P2 si no hay uso público amplio o saturación medida.

## 6. Matriz mínima de validación

| Caso | Validación requerida | Criterio observable |
|---|---|---|
| Registro/login/cierre | Pruebas existentes y Android con cuenta de prueba autorizada | Perfil Usuario, sesión renovable, pantallas privadas cerradas al salir |
| PKCE web y nativo | Unitarias, SDK simulado y callback del binario | Origen/ruta correctos, un intercambio por código y sin tokens en URL visible |
| Texto → borrador | Frases de varias categorías y datos incompletos | Descripción editable, categoría revisable, nada se persiste antes de confirmar |
| Confirmación/reintento | POST con UUID y respuesta perdida simulada | Mismo intento devuelve mismo gasto; cambio de contenido produce conflicto |
| Historial | Orden, cursor, fechas y categoría | Página estable sin acceso a filas ajenas |
| Edición/borrado | SQL local y E2E si se incluye HU-16 | Excluye eliminados de historia, estadísticas y fugas; conserva idempotencia original |
| Dashboard | Importes exactos, vacío, Otros, empate y base cero | Resultados idénticos antes/después de optimizaciones |
| FUGA-01 | Umbrales y ventana inalterados | 3 gastos/3 fechas, COP 1.000–30.000, suma mínima COP 15.000 y 30 días |
| Normalización | Regresiones 1.0/1.1 y conceptos compuestos | Variantes equivalentes se agrupan; café con leche y bus intermunicipal se distinguen |
| Cuatro cafés conocidos | Fixture local fechado 2026-11-18 | Cuatro evidencias, concepto cafe y COP 20.000; originales intactos |
| Aislamiento | Usuarios A/B y administrador, SQL y API | B no lee/edita/elimina A; admin no accede a finanzas; cliente directo no obtiene filas financieras |
| Voz | Permisos y ciclo de vida del dispositivo | Transcripción revisable, sin audio persistido ni guardado automático; fallback de texto |
| Notificaciones, si incluidas | Política, errores y entrega Android | Canal correcto, siete días, silencio horario, contenido genérico y toque seguro |
| Infraestructura | Linux, CA, configuración sintética, demoras | TLS completo, secretos no impresos, errores recuperables y sin duplicar mutaciones |

La prueba fechada de noviembre es de regresión local. Para un E2E futuro se utilizarán fechas relativas dentro de la ventana y datos ficticios autorizados; no se cambiarán las fechas ni los gastos existentes para hacer pasar una prueba.

Las pruebas de integración nunca se ejecutan contra producción. El fixture actual exige host loopback y crea su propia base `fuga_test_*`; el esquema Auth de ese fixture es un sustituto local, no Supabase Auth real. El uso posterior de un entorno Supabase de prueba requiere autorización y no se infiere de este plan.

## 7. Herramientas, costos y configuración propuesta

### Herramientas que se reutilizan

- Python, FastAPI, SQLAlchemy/Psycopg, Pytest, Ruff, mypy y pip-audit existentes.
- Node, Expo, React Native, TypeScript, pruebas Node, Supabase SDK, SecureStore y expo-notifications existentes.
- SQL y migraciones numeradas actuales; no imponer Alembic ni sustituir la base.
- Kotlin/SpeechRecognizer; no integrar un proveedor de voz nuevo ni IA generativa.
- Markdown, Mermaid y Git para documentación y trazabilidad.

ESLint, cobertura, herramientas Android o expo-dev-client se consideran incorporaciones posibles para tareas concretas, no instalaciones autorizadas por la auditoría. No duplicar Ruff con Pylint/Flake8 para completar una lista de herramientas.

### Ficha de backend para revisar antes de desplegar

| Elemento | Propuesta, todavía sin aplicar |
|---|---|
| Alojamiento | Servicio web Python de Render Free para demostración |
| Raíz | `backend` |
| Runtime | Python 3.12 compatible con `pyproject.toml` |
| Build | `pip install -r requirements.lock` |
| Start | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Procesos | Inicialmente uno; revisar pool 5 + 10 y límites efectivos |
| Identidad | SUPABASE_URL, SUPABASE_JWT_AUDIENCE; JWKS/issuer derivados si no se definen |
| Administración | SUPABASE_SERVICE_ROLE_KEY solo servidor; clave sb_secret por apikey |
| Datos | DATABASE_URL Psycopg hacia Supabase; verify-full y CA disponible en Linux |
| Web | CORS_ORIGINS explícito; no es sustituto de autenticación |
| Producción | APP_ENV con valor acordado `prod`, LOG_LEVEL sin depuración sensible |
| Salud | `/health` proceso; `/ready` dependencia PostgreSQL; elegir uso de cada uno conscientemente |
| Persistencia | Ningún dato financiero en filesystem del servicio; logs a consola sanitizados |
| Ampliaciones | Cloudinary/Google/correo solo cuando se incluyan y estén configurados |

El arranque FastAPI propuesto adapta el comando oficial de Render al módulo y estructura existentes. [Referencia](https://render.com/docs/deploy-fastapi).

Render Free suspende por inactividad y el almacenamiento es efímero; la ficha debe contemplar despertar, cuotas y recuperación sin pagos. No desplegar antes de cerrar ACT-11. [Límites](https://render.com/docs/free).

Supabase Free requiere vigilar espacio y pausa por inactividad, sin prometer cuotas ilimitadas. Conservar la base existente y comprobar consumo en el panel antes de la demostración. [Plan gratuito](https://supabase.com/pricing).

El pooler de sesión permite conexión IPv4 de un backend persistente; mantener modo y Psycopg compatibles, sin cambiar a transacción por intuición. [Conexión PostgreSQL](https://supabase.com/docs/guides/database/connecting-to-postgres).

La opción gratuita preferida para incorporar Kotlin es compilación local con Android SDK/Expo CLI. Expo Go sirve para comprobaciones compatibles, pero no incluye FugaVoice. No se requiere publicar en tienda ni contratar EAS para generar el binario local. [Guía local](https://docs.expo.dev/guides/local-app-development/).

CI será pequeño y sin despliegue automático; confirmar las cuotas si el repositorio es privado y limitar artefactos. [Condiciones GitHub Actions](https://docs.github.com/en/billing/concepts/product-billing/github-actions).

## 8. Evidencias y riesgos de ejecución

### Evidencias para el manual técnico

| Etapa | Evidencia | Datos que deben ocultarse |
|---|---|---|
| ACT-01 | Matriz de alcance, árbol de carpetas y arquitectura actual/objetivo | Rutas personales del equipo cuando se comparta fuera del proyecto |
| ACT-02/03 | Manifiesto fusionado, versiones SDK/JDK, permiso y voz Android | Cuentas personales, audios y transcripciones privadas |
| ACT-04/05 | Comandos, totales, omisiones y casos de aislamiento | JWT, DSN, usuarios/correos reales |
| ACT-06 | Ruff/mypy/TypeScript; ESLint/cobertura si se incorporan | Valores de entorno en terminal |
| ACT-07/08 | Conteo de consultas y tiempos con fixtures | Descripciones y montos de usuarios reales |
| ACT-09 | Bandeja y navegación de notificación genérica | Payload con IDs de cuenta o fuga |
| ACT-10/13 | Ficha de variables por nombre, CA y salud/configuración | Contraseñas, claves y cadenas de conexión |
| ACT-12 | Workflow YAML, rama/revisión y corrida asociada | Secrets de Actions y URL de remoto con credenciales |
| ACT-14 | Procedimiento y simulación de retención | Información personal y datos reales a eliminar |
| ACT-15 | APK identificado, instalación limpia, flujos y limitaciones | Firma privada del APK, sesión y datos personales |
| Despliegue posterior autorizado | HTTPS, cold start, readiness y recuperación | Credenciales o pantallas de configuración con claves visibles |

### Riesgos y mitigación

- **Cambio amplio de configuración nativa:** modificar primero solo el permiso; validar cámara y voz, conservar el diff revisable.
- **Herramientas Android no disponibles:** localizar instalaciones antes de descargar; no confundir ausencia en PATH con ausencia total. Posponer voz aceptada si no hay dispositivo, sin declararla terminada.
- **Mock confundido con proveedor real:** etiquetar cada evidencia; pruebas de Auth simulado y PostgreSQL local no certifican SMTP, OAuth o RLS remoto actual.
- **Optimizaciones alteran evidencia/idempotencia:** aplicar ACT-07/08 después de pruebas; conservar contratos, ventanas y versiones.
- **Limpieza de estilo masiva:** limitar alcance y revisar excepciones; no usar autofix indiscriminado sobre archivos no relacionados.
- **Credenciales incorporadas al APK o Git:** comprobar lista de archivos y artefactos antes de versionar/distribuir; nunca copiar `.env.local` al informe.
- **Plan gratuito insuficiente:** controlar consumo y aceptar suspensión; no migrar de proveedor ni contratar recursos sin una decisión nueva.
- **Retención destruye evidencia o perfiles ajenos:** simular localmente y exigir revisión antes de actuar sobre datos reales.
- **Ampliaciones retrasan el núcleo:** cerrar primero texto, sesión, aislamiento, estadísticas, fugas/evidencia y la voz priorizada; notificaciones y P2 pueden quedar explícitamente fuera.

## 9. Criterio de finalización y autorización de despliegue

FUGA+ estará suficientemente preparado para planificar el despliegue cuando:

1. AUD-01 esté corregido y voz validada en compilación propia, o la propietaria acepte explícitamente una entrega sin esa prioridad adicional.
2. Las 13 HU Must tengan evidencia de aceptación del flujo Android, incluyendo aislamiento A/B/admin y evidencia de fugas.
3. Pruebas actuales y nuevas necesarias pasen; integración SQL se ejecute en base desechable; omisiones y deprecaciones estén identificadas sin contarlas como aprobaciones.
4. TypeScript, mypy de dominio y Ruff mínimo sigan correctos. Avisos restantes estén clasificados; no se exige limpiar los 210 ni alcanzar cobertura perfecta.
5. Exista una revisión candidata reproducible con locks y módulo nativo, y se haya comprobado que no distribuye secretos.
6. El APK de entrega funcione sin Metro y el callback nativo esté registrado. No basta un bundle o Expo Go.
7. Configuración Linux/Render, CA, SSL, comandos, variables y manejo de arranque frío estén revisados y probados de forma local/simulada antes del despliegue.
8. Se documenten límites de cuotas, recuperación, evidencia histórica y retención; las funciones opcionales incluidas tengan aceptación y las excluidas no se anuncien como completas.
9. El manual técnico contenga diagramas, estructura, versiones, resultados, configuración por nombres y capturas sanitizadas de Android.

Estas condiciones permiten **solicitar una autorización concreta** para desplegar backend y distribuir la versión candidata. No autorizan migraciones remotas, altas o modificaciones de usuarios reales, commit, push o publicación. Los P2 pueden quedar en backlog con motivo y responsable de revisión; la pipeline puede ejecutarse localmente mientras no se autorice GitHub.

## 10. Primera tarea concreta

**ACT-02: resolver el conflicto de RECORD_AUDIO en `mobile/app.json`.**

Preparar un cambio mínimo que retire `microphonePermission: false` como bloqueo global, conserve deshabilitada la cámara y mantenga el permiso contextual del módulo de voz. Antes de aceptarlo, inspeccionar la salida del plugin y el manifiesto fusionado; después probar concesión/denegación, dictado, cancelación y confirmación manual en Android. No tocar FUGA-01, registros existentes ni tecnologías.

Esta actividad está propuesta, **no implementada**. El primer paso de la siguiente sesión será revisar la aprobación de este diagnóstico y el alcance exacto de ese cambio.
