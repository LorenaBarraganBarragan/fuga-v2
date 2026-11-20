# FUGA+

**Descubre a dónde se va tu dinero.**

Aplicación académica de control de gastos personales para jóvenes y estudiantes. Integra registro por texto y voz Android, revisión antes del guardado, historial, estadísticas y detección explicable de posibles fugas mediante diccionarios y reglas deterministas.

**Revisión documental: 19 de noviembre de 2026.** Este documento presenta problema, alcance, trazabilidad y decisiones del proyecto. El [README principal](../README.md) contiene instalación, variables y compilación. La propietaria reporta un APK release operativo y backend desplegado en Render con Supabase; ese reporte se distingue de las comprobaciones del repositorio y de los ensayos locales.

## 1. Problema

Los gastos pequeños cotidianos pueden pasar desapercibidos y acumularse. Un registro manual incómodo favorece olvidos y dificulta mantener el seguimiento. La [entrevista con un usuario potencial](docs/entrevista-real.md) identificó la necesidad de simplificar el registro y consultar información financiera comprensible.

FUGA+ permite revisar gastos y patrones repetitivos sin conexiones bancarias ni herramientas financieras complejas. Una posible fuga es un patrón para revisar, no una pérdida confirmada ni un juicio sobre el usuario.

## 2. Objetivos

**Objetivo general:** desarrollar y validar un MVP Android que facilite registrar y comprender gastos personales mediante texto, voz, estadísticas y reglas explicables.

**Objetivos específicos:**

- Registrar gastos por texto y dictado Android, manteniendo una alternativa escrita.
- Interpretar monto, fecha, descripción y categoría, con revisión y confirmación obligatorias.
- Persistir datos estructurados bajo la identidad de su propietario y prevenir duplicados accidentales.
- Consultar historial, estadísticas y evidencia de posibles fugas.
- Proteger sesiones, roles y aislamiento entre usuarios.
- Mantener una arquitectura viable para un proyecto individual y documentar pruebas y limitaciones.

La planificación original de **12 semanas efectivas** se conserva como antecedente en la sección 13.

## 3. Público objetivo y actores

Público principal: jóvenes y estudiantes que desean organizar sus gastos diarios y comprender sus hábitos de consumo.

| Actor | Responsabilidades y límites reales |
| --- | --- |
| Visitante | Consultar bienvenida, registrarse e iniciar sesión; no es un rol persistido. |
| Usuario | Registrar y gestionar gastos propios, consultar estadísticas/fugas y gestionar perfil/sesión. |
| Administrador | Buscar cuentas, consultar detalle mínimo y estadísticas de cuentas/actividad, activar/desactivar cuentas usuarias; sin finanzas individuales. |

Los roles persistidos en `public.perfil.rol` son `usuario` y `administrador`. Ambos ingresan por el mismo formulario. El operador aprovisiona el rol administrativo de forma privilegiada sobre el UUID correcto; no se concede desde el registro ni desde metadatos editables. FastAPI valida permisos, aunque la interfaz oculte operaciones.

## 4. Propuesta de valor

El usuario puede escribir o dictar «Hoy gasté 8000 en un taxi». El sistema propone campos estructurados, permite corregirlos y guarda solo después de confirmar. Los gastos alimentan un historial y un dashboard; los patrones detectados ofrecen regla, fechas, ocurrencias e información de soporte.

La etiqueta **«Procesar con IA»** se conserva por decisión de producto, acompañada de su explicación: el procesamiento usa reglas y diccionarios, sin IA generativa ni envío del gasto a un modelo externo.

## 5. Funcionalidades y alcance actual

### MVP Android de esta entrega

Incluye bienvenida, registro/login por correo, cierre de sesión, registro escrito, interpretación determinista, revisión/confirmación, persistencia privada, historial, estadísticas básicas, detección/evidencia y aislamiento de datos. **HU-17, HU-18 y HU-19 forman parte del MVP Android solicitado actualmente**: permiso de micrófono, dictado Kotlin, transcripción editable y confirmación.

La matriz oficial 3.0 mantiene esas tres historias como Could Have y registra su priorización adicional de entrega. Se conserva esa prioridad como dato de la línea base y se documenta aquí su inclusión efectiva en el MVP; no se modifican los documentos oficiales. Prioridad, alcance de entrega y estado funcional son dimensiones distintas.

### Ampliaciones ya presentes

Perfil y fotografía firmada, filtros, edición/borrado lógico, comparación mensual, avisos locales, resumen mensual de patrones vigentes y administración tienen implementación; no deben describirse como propuestas futuras. Google, recuperación y foto Google tienen código condicionado a proveedores y aceptación real.

### Pendientes y exclusiones

HU-26 no dispone de un catálogo implementado de sugerencias aprobadas. HU-28/29 se refieren al **límite mensual global y su avance**, están excluidas y no implementadas; no son metas de ahorro genéricas. No existen sus tablas en las migraciones actuales.

Quedan fuera del alcance: conexiones bancarias, pagos/transferencias, créditos, inversiones, asesoría financiera profesional, entrenamiento de modelos e IA generativa externa obligatoria. Push remoto no es requisito de HU-25 ni una funcionalidad implementada.

## 6. Historias de usuario y priorización

Fuente: [33 historias oficiales 3.0](docs/historias-usuario/HISTORIAS_DE_USUARIO.md), con decisiones D-01 a D-15. La [especificación RF](docs/requerimientos/REQUERIMIENTOS.md) conserva correspondencia uno a uno.

La columna **MVP de entrega** incluye las 13 Must Have y las tres historias de voz incorporadas por la indicación actual. «No» significa complemento o exclusión del MVP, no ausencia de código. La prioridad MoSCoW reproduce la fuente oficial.

**Estados:** Implementada = flujo existente e integrado, sin implicar aceptación de todos los criterios en producción; Parcial = alcance funcional/configuración o aceptación por completar; Pendiente = sin implementación funcional; Excluida = fuera de esta entrega y sin implementar.

| HU | RF | Funcionalidad | MoSCoW oficial | MVP de entrega | Estado |
| --- | --- | --- | --- | --- | --- |
| HU-01 | RF-001 | Bienvenida y acceso público | Must Have | Sí | Implementada |
| HU-02 | RF-002 | Registro/login por correo y contraseña | Must Have | Sí | Parcial: login operativo; confirmación real de alta por acreditar |
| HU-03 | RF-003 | Acceso Google mediante Supabase OAuth | Should Have | No | Parcial: configuración/aceptación externa |
| HU-04 | RF-004 | Cierre de sesión | Must Have | Sí | Implementada |
| HU-05 | RF-005 | Recuperación de contraseña | Should Have | No | Parcial: correo y callback reales |
| HU-06 | RF-006 | Desactivación propia | Could Have | No | Implementada; sincronización Auth requiere configuración |
| HU-07 | RF-007 | Nombres, apellido y teléfono | Should Have | No | Implementada |
| HU-08 | RF-008 | Fotografía de perfil | Should Have | No | Implementada; limpieza operativa manual |
| HU-09 | RF-009 | Foto Google con consentimiento | Could Have | No | Parcial: depende de identidad Google vinculada |
| HU-10 | RF-010 | Registro escrito en lenguaje natural | Must Have | Sí | Implementada |
| HU-11 | RF-011 | Interpretación mediante reglas | Must Have | Sí | Implementada |
| HU-12 | RF-012 | Revisión/corrección del borrador | Must Have | Sí | Implementada |
| HU-13 | RF-013 | Guardado privado e idempotencia | Must Have | Sí | Implementada |
| HU-14 | RF-014 | Historial ordenado y paginado | Must Have | Sí | Implementada |
| HU-15 | RF-015 | Filtros de fecha/categoría | Should Have | No | Implementada |
| HU-16 | RF-016 | Edición y eliminación lógica | Should Have | No | Implementada |
| HU-17 | RF-017 | Captura de voz Android | Could Have | Sí · voz | Implementada |
| HU-18 | RF-018 | Transcripción Kotlin SpeechRecognizer | Could Have | Sí · voz | Implementada |
| HU-19 | RF-019 | Revisar/confirmar gasto dictado | Could Have | Sí · voz | Implementada |
| HU-20 | RF-020 | Total, cantidad y promedio | Must Have | Sí | Implementada |
| HU-21 | RF-021 | Estadísticas por categoría | Must Have | Sí | Implementada |
| HU-22 | RF-022 | Comparación entre periodos | Could Have | No | Implementada: mes frente al anterior |
| HU-23 | RF-023 | Detección FUGA-01 | Must Have | Sí | Implementada |
| HU-24 | RF-024 | Evidencia de fuga propia | Must Have | Sí | Implementada |
| HU-25 | RF-025 | Alertas internas y avisos locales | Could Have | No | Parcial en aceptación de plataformas/ciclo de vida; mecanismo implementado |
| HU-26 | RF-026 | Sugerencias de catálogo aprobado | Could Have | No | Pendiente |
| HU-27 | RF-027 | Resumen mensual de fugas | Could Have | No | Parcial: solo patrones vigentes de la ventana actual |
| HU-28 | RF-028 | Límite mensual global | Won't Have | No | Excluida |
| HU-29 | RF-029 | Avance del límite mensual | Won't Have | No | Excluida |
| HU-30 | RF-030 | Estadísticas administrativas de uso | Should Have | No | Parcial: cuentas/actividad; falta conteo global de gastos |
| HU-31 | RF-031 | Búsqueda, filtros y detalle de cuentas | Should Have | No | Implementada |
| HU-32 | RF-032 | Activación/desactivación administrativa | Should Have | No | Implementada; aceptación remota completa por acreditar |
| HU-33 | RF-033 | Privacidad y aislamiento transversal | Must Have | Sí | Implementada; pruebas locales no certifican permisos remotos |

**Distribución oficial:** 13 Must Have, 9 Should Have, 9 Could Have y 2 Won't Have: **33**. El MVP de entrega incorpora **16 historias** al sumar las tres de voz, sin convertir las Should/Could ya desarrolladas en Must. HU-33 es transversal y no requiere una pantalla independiente.

## 7. Requisitos funcionales y trazabilidad

La tabla anterior conserva los **33 RF**, RF-001 a RF-033, relacionados con HU-01 a HU-33; no elimina requisitos por no estar implementados. Los criterios detallados y dependencias siguen en los [requerimientos oficiales](docs/requerimientos/REQUERIMIENTOS.md).

Contratos principales: `/api/v1/expenses` para interpretación, confirmación, consulta y cambios; `/analytics` para agregados/comparación; `/leaks` para detección, detalle y resumen; `/me` para perfil/fotografía y `/admin` para cuentas. Registro y login utilizan directamente el SDK Supabase Auth, no un emisor JWT propio en FastAPI.

Límites que afectan al cumplimiento:

- **RF-025:** alertas internas y notificaciones locales no exigen push remoto. Funcionan al consultar análisis, con permiso y deduplicación; otras situaciones Android deben acreditarse manualmente. La ausencia de push no es una carencia de este requisito.
- **RF-027:** la ruta mensual recalcula la ventana actual y suma gastos del mes asociados a fugas `vigente=TRUE`, sin duplicar gastos. No reconstruye un histórico completo de todas las fugas de meses anteriores.
- **RF-030:** `/admin/stats` devuelve registrados/activos/inactivos y actividad mensual. No devuelve el conteo global de gastos exigido por la especificación ni todos los controles de consulta por mes; no se anuncia cumplimiento integral.
- **C-04 / historial:** la API aplica cursor, 20 registros por carga y máximo 50. La interfaz actual ofrece «Cargar más»; la carga automática al desplazarse prevista en el plan no está implementada.

## 8. Requisitos no funcionales

Se conservan los **16 RNF** oficiales. La tabla indica controles y límites, no una certificación total:

| ID | Requisito y correspondencia actual |
| --- | --- |
| RNF-001 | Autorización/aislamiento: rol, estado y propietario verificados en FastAPI. |
| RNF-002 | Minimización: datos confirmados; `texto_original` persistido NULL, sin audio ni borradores de servidor. |
| RNF-003 | Credenciales/sesiones: Supabase SDK, SecureStore nativo, localStorage Web y secretos exclusivos del servidor. |
| RNF-004 | Entradas: validación de COP, fechas, UUID, categorías y versiones. |
| RNF-005 | Transacciones/idempotencia: locks por usuario, huella, clave UUID y reintentos controlados. |
| RNF-006 | Coherencia: invalidación de snapshots tras cambios y recálculo bajo demanda. |
| RNF-007 | Logs: filtrado de tokens, claves y datos sensibles; errores sin credenciales. |
| RNF-008 | Transporte/secretos: HTTPS y PostgreSQL con TLS verify-full en producción. |
| RNF-009 | Usabilidad: revisión editable, errores, confirmaciones e insets; evidencia física limitada al dispositivo ensayado. |
| RNF-010 | Transparencia de «Procesar con IA»: explicación del mecanismo determinista. |
| RNF-011 | Compatibilidad: voz Android en build nativo, texto Web/iOS; sin certificación iOS física. |
| RNF-012 | Fiabilidad: lecturas cancelables/reintentos acotados; mutaciones sin reenvío automático, fallos explícitos. |
| RNF-013 | Rendimiento: mediciones históricas de alcance limitado; sin SLA global ni carga de producción acreditada. |
| RNF-014 | Mantenibilidad: capas, versiones, pruebas automatizadas y controles estáticos documentados. |
| RNF-015 | Auditoría: consultas administrativas, estados y denegaciones; sin contenido financiero. |
| RNF-016 | Retención: cola a 30 días y cancelación al reactivar; depuración/supresión efectiva y auditoría a 90 días requieren operación revisada. |

## 9. Tecnologías y decisiones aprobadas

| Componente | Tecnología y uso real |
| --- | --- |
| App | React Native 0.88.1, Expo 58 y TypeScript 6; Android y alternativa Expo Web. |
| Backend | Python 3.12, FastAPI, Uvicorn y Pydantic; rutas, servicios, dominio y repositorios. |
| Base de datos | PostgreSQL en Supabase; SQLAlchemy 2/Psycopg 3, migraciones, constraints, índices y RLS. |
| Consultas/estadísticas | SQL parametrizado, `SUM`, `COUNT`, `GROUP BY`, filtros de propietario/mes y cálculos exactos con Decimal/ROUND_HALF_UP en Python. |
| Identidad | Supabase Auth, correo/contraseña, PKCE y OAuth Google condicionado; validación JWT/JWKS en FastAPI. |
| Voz | Módulo Kotlin `FugaVoice` con Android SpeechRecognizer, permiso contextual y revisión escrita. |
| Imágenes | Cloudinary: carga directa firmada, verificación servidor y URL en perfil. |
| Notificaciones | expo-notifications: avisos locales, sin infraestructura push remota. |
| Despliegue | Backend en Render según reporte de la propietaria; configuración en render.yaml y APK release autónomo. |
| Calidad/documentación | pytest, Node test runner, TypeScript, Ruff, mypy, OpenAPI/Swagger, Git/GitHub y diagrams.net. |

**Correcciones frente al README anterior:** PostgreSQL sustituye MongoDB Atlas; agregaciones SQL/Python sustituyen MongoDB Aggregation; Supabase Auth administra identidad y OAuth en lugar de un JWT propio o Google Identity Services independiente. Expo, Render y los servicios ya integrados se describen como implementación, no como propuesta.

### Decisiones D-01 a D-15

| ID | Decisión que se conserva |
| --- | --- |
| D-01 | FUGA-01 1.0, ventana de 30 días, categoría/concepto y parámetros versionados; ver sección 10. |
| D-02 | Nueve categorías, «Otros» incluido en totales; desempate por frase más larga y revisión si persiste ambigüedad. |
| D-03 | COP entero 1–100.000.000; porcentajes a un decimal y comparación sin división por cero. |
| D-04 | America/Bogota; fechas ISO desde 2020-01-01 hasta hoy, meses calendario e historial con desempate estable. |
| D-05 | Texto 1–280, descripción 1–120, borrador en memoria, confirmación e idempotencia UUID por 24 horas. |
| D-06 | Borrado lógico de gastos y bloqueo por disabled_at; retención a 30 días sin promesa de borrar respaldos. |
| D-07 | Sin finanzas individuales para administradores; cualquier agregado financiero futuro exige mínimo 10 usuarios. Los agregados actuales son de cuentas/actividad. |
| D-08 | Roles y autorización en cada solicitud; aprovisionamiento administrativo privilegiado y RLS sin confiar en que cubra una conexión SQL privilegiada. |
| D-09 | Supabase Auth; contraseña mínima de 8 caracteres, renovación/cierre SDK y recuperación gestionada por el proveedor. Sin revocación instantánea prometida de access tokens. |
| D-10 | Google mediante Supabase OAuth configurado; sin vincular cuentas solo por coincidencia de correo. |
| D-11 | Avisos locales con permiso, siete días entre recordatorios por patrón/versión y silencio 21:00–08:00 Bogotá; sin datos financieros en pantalla bloqueada. |
| D-12 | Voz Android es-CO/es, máximo 30 segundos/280 caracteres, sin audio persistido y con alternativa escrita. |
| D-13 | Nombres opcionales 2–80, teléfono opcional de 10 dígitos; JPEG/PNG/WebP hasta 5.000.000 bytes, firma y precedencia de fotografía manual. |
| D-14 | Auditoría administrativa restringida; política de 90 días, sin depuración automática acreditada. |
| D-15 | Etiqueta y explicación transparente; lenguaje de «posible fuga», sin culpa, pérdidas confirmadas ni ahorros garantizados. |

El [Plan Maestro 1.1.1, anexo D](docs/planificacion/PLAN_MAESTRO_IMPLEMENTACION_FUGA_PLUS_v1.1.1.md#anexo-d--decisiones-aprobadas-c-01c-12-y-decisión-arquitectónica-complementaria) conserva C-01…C-12 y DA-01: minimización/nombres opcionales (C-01/02); idempotencia y cursor de 20 registros, máximo 50 (C-03/04); interpretación de decisiones cerradas y medición sin umbrales inventados (C-05/06); portabilidad sin gratuidad permanente (C-07); logo original (C-08); núcleo inicial de siete tablas (C-09); exclusión inicial de borrado y procedimiento de privacidad (C-10/11); FK UUID `regla_version_id` (C-12).

Es un antecedente por fases: las migraciones posteriores incorporaron auditoría, actividad, retención y fotografías hasta 11 tablas; HU-16 añadió edición/borrado lógico como ampliación autorizada. Su existencia no elimina esos antecedentes ni permite afirmar que todas las puertas de aceptación estén cerradas. DA-01 mantiene FastAPI como puerta financiera y Supabase como emisor de identidad. Redis, Docker y modelos externos no son dependencias del MVP.

## 10. Interpretación, voz y detección de fugas

### Registro y normalización

El intérprete propone monto, fecha, categoría y descripción; una ausencia o ambigüedad requiere corrección. El texto original permanece en el borrador, pero el backend guarda los datos confirmados y `texto_original=NULL`. Los gastos legítimos idénticos pueden registrarse con claves distintas; reutilizar una clave con contenido distinto o vencida genera conflicto.

Interpretación/normalización **1.1** conserva compatibilidad con confirmaciones 1.0. Normaliza mayúsculas, tildes, puntuación, espacios, prefijos y equivalencias justificadas. Se comparte con el análisis de gastos antiguos, sin reescribirlos ni fusionar automáticamente conceptos compuestos diferentes. Ver [normalización](../docs/NORMALIZACION_CONCEPTOS.md).

El catálogo inicial es Alimentación, Transporte, Vivienda, Servicios, Educación, Salud, Entretenimiento, Compras y Otros. Los UUID y el catálogo operativo se consultan en PostgreSQL; no se sustituyen fallos de conexión por datos ficticios.

La voz Android convierte el dictado a texto, que utiliza el mismo flujo de revisión/confirmación. Requiere permiso y build nativo con Kotlin, **no Expo Go**. El reconocedor del dispositivo puede procesar audio externamente; esto no convierte el intérprete financiero en un servicio de IA generativa.

### FUGA-01 1.0

- Ventana: día actual y 29 anteriores, en America/Bogota.
- Grupo: misma categoría y concepto canónico informativo.
- Mínimo: **3 gastos en 3 fechas distintas**.
- Importe individual: **COP 1.000–30.000**; suma mínima: **COP 15.000**.
- Exclusión de borrados, fechas fuera de ventana y descripciones genéricas; «Otros» puede participar con concepto informativo.
- Evidencia: regla/versión, ocurrencias, fechas, total y gastos propios asociados.

Son los parámetros del código y catálogo SQL versionado, sin una consulta remota nueva. Se leen de la versión activa; no se cambian umbrales para forzar resultados. El análisis bajo demanda puede escribir snapshots/evidencia, mientras conserva los gastos originales. El mismo conjunto de evidencia mantiene un snapshot estable. FUGA-01 no predice pérdidas ni garantiza ahorro.

### HU-25: alertas y notificaciones

La pantalla Fugas muestra el patrón, importe, ocurrencias y acceso a evidencia. Al consultar análisis, `notifyCandidate` puede emitir un aviso local genérico, sujeto a permiso, deduplicación y horario. Tocar el aviso solo abre evidencia bajo la sesión de su propietario. Si no hay permiso, el análisis interno sigue disponible.

Expo Web no ofrece estos avisos locales. No hay push remoto, token push ni motor de análisis ejecutándose con la app cerrada; el estado cerrado/segundo plano no se acredita por una prueba en primer plano. La entrega/toque/sin duplicado se documentó físicamente en QA; los demás escenarios siguen separados de esa evidencia.

## 11. Arquitectura y persistencia

1. **Cliente React Native/Expo:** pantallas, formularios, AuthProvider y SDK Supabase; datos financieros por HTTPS `/api/v1`.
2. **FastAPI:** validación de JWT/JWKS, roles/estado, servicios, dominio determinista y repositorios SQL con propietario obligatorio.
3. **PostgreSQL en Supabase:** datos relacionales, constraints, índices, versiones, snapshots, evidencia y RLS.
4. **Servicios:** Supabase Auth para identidad; Cloudinary para fotografías; Render para el backend; Kotlin y Expo Notifications para funciones Android.

Las migraciones `0001`–`0010` definen `perfil`, `categoria`, `gasto`, `regla_fuga`, `regla_fuga_version`, `fuga`, `fuga_evidencia`, `auditoria`, `actividad_mensual`, `tarea_retencion` y `perfil_foto_carga`: **11 tablas propias y 13 FK**, además de la referencia externa `auth.users`. Predominan UUID; `perfil_foto_carga.public_id` es TEXT y `actividad_mensual` tiene PK compuesta. No hay tablas de límites mensuales.

El APK release incorpora JavaScript y usa servicios HTTPS, sin Metro, USB ni PostgreSQL del computador. Render utiliza el launcher versionado, variables privadas y TLS PostgreSQL con certificado público. `/health` verifica proceso; `/ready` ejecuta SELECT 1, sin certificar esquema o servicios externos; `/docs` se deshabilita en producción.

Fuentes: [arquitectura implementada](../docs/ARQUITECTURA_FUGA_PLUS.md), [migraciones/conexión](../supabase/docs/CONEXION_SUPABASE.md), [Render](../render.yaml) y [compilación release firmada](../mobile/docs/APK_RELEASE_LOCAL.md). La antigua plantilla `docs/architecture.md` no sustituye esa arquitectura real.

## 12. Seguridad y privacidad

- Identidad exclusivamente del JWT verificado; no se confía en un propietario enviado por el cliente.
- Rol/disabled_at en PostgreSQL, require_user/require_admin y filtros por propietario; no se relajan en QA.
- Perfil enlazado con `auth.users.id`; el trigger crea rol usuario, nunca administrador por metadatos de registro.
- Conexión SQL de servidor privada; RLS y permisos directos financieros no sustituyen el aislamiento de FastAPI.
- Claves públicas Supabase en cliente; clave administrativa moderna por `apikey` solo en backend. Sin secretos de firma Cloudinary o contraseñas en APK/Git/logs.
- Cambios de estado auditados; si falla Auth al desactivar, se conserva el bloqueo local y se informa sincronización pendiente.
- Cloudinary verifica propietario, formato y tamaño antes de persistir URL; la foto anterior se retira después de confirmar la nueva. Limpieza conservadora manual, sin borrar activos ajenos.
- Supresión y auditoría requieren operación revisada: cola de retención no equivale a eliminación física ni a borrado de respaldos.

Ver [seguridad del backend](../backend/docs/seguridad.md), [fotografías HU-08](docs/auditoria/hu08-fotografia-perfil.md) y [retención operativa](../docs/RETENCION_OPERATIVA.md).

## 13. Planificación académica de 12 semanas

Antecedente de organización, **no cronología certificada de ejecución**:

| Etapa | Trabajo previsto | Resultado esperado |
| --- | --- | --- |
| Semanas 1–2 | Entorno, acceso y seguridad | App ejecutable y sesiones |
| Semanas 3–4 | Registro, interpretación y confirmación | Flujo de gasto funcional |
| Semana 5 | Historial y estadísticas | Movimientos y dashboard |
| Semana 6 | Fugas y evidencia | Detección explicable |
| Semana 7 | Integración y estabilización | MVP demostrable |
| Semanas 8–10 | Ampliaciones priorizadas | Mejoras según dependencias |
| Semana 11 | Complementos/rendimiento | Validaciones adicionales |
| Semana 12 | Regresión/documentación | Preparación de la entrega |

El estado posterior se registra en el [informe de ejecución ACT-01…ACT-15](docs/auditoria/ejecucion-plan-mejora-fugaplus.md), no se infiere de este calendario. Voz es parte del MVP Android actual, aunque el calendario y la matriz inicial la trataran como ampliación.

## 14. Pruebas y criterios de aceptación

| Procedencia | Resultado y alcance |
| --- | --- |
| Revisión previa del README principal, 2026-11-19 | **307 backend aprobadas, 39 omitidas; 132 frontend aprobadas; TypeScript correcto.** Ejecución aislada, sin PostgreSQL ni HTTP externo; las 39 omitidas requieren SQL local. No se repitieron en esta edición documental. |
| [QA administrativo](../mobile/docs/QA_ANDROID_ADMIN.md#validación-automatizada) | **346 backend**, incluidas pruebas SQL locales, y 124 frontend en esa etapa; PostgreSQL desechable y Auth simulado. |
| [Evidencia HU-08](docs/auditoria/evidencia-hu08-fotografia.json) | 325 backend, 31 SQL incluidas, y 97 frontend en esa etapa; dos PNG sintéticos Cloudinary con URL solo en PostgreSQL local. Persistencia/sustitución confirmadas físicamente. |
| Reporte actual de la propietaria | APK release instalado: login, texto/voz, dashboard, fugas, notificaciones, fotografía persistente y acceso administrativo; Render/Supabase operativos. No es una medición remota nueva del agente. |

Los conteos corresponden a etapas y no se suman. Cobertura y auditorías de dependencias son resultados fechados, con exclusiones y avisos; no certifican seguridad o cobertura total actuales. Los controles nativos simulados no sustituyen permisos, teclado y comportamiento físico.

Comandos con dependencias ya instaladas, desde la raíz del repositorio:

```powershell
backend/.venv/Scripts/python.exe -B backend/scripts/test_safe.py
cd mobile
npm test
npm run typecheck
```

La integración mediante `test_safe.py --integration` exige FUGA_TEST_DATABASE_URL local desechable y crea/retira su propia base. No usar Supabase ni datos QA que deban conservarse. Para instrucciones completas y cobertura, ver [pruebas del README principal](../README.md#8-pruebas-y-validaciones).

La aceptación debe comprobar datos inválidos, interpretación, revisión obligatoria, idempotencia, aislamiento, permisos administrativos, coherencia tras cambios, fallos de red y regresión. Deben acreditarse por separado correo/OAuth, escenarios adicionales de notificaciones, operaciones administrativas remotas, carga representativa y otras plataformas. El acceso a una pantalla o SELECT 1 no cierra esos criterios.

## 15. Documentación y diagramas

### Fuentes oficiales y seguimiento

- [Entrevista](docs/entrevista-real.md), [visión](docs/respuestas-ia/salida-vision.md) y [análisis competitivo](docs/respuestas-ia/salida-analisis-competitivo.md).
- [Historias 3.0](docs/historias-usuario/HISTORIAS_DE_USUARIO.md) y [requerimientos 3.0](docs/requerimientos/REQUERIMIENTOS.md).
- [Plan Maestro 1.1.1](docs/planificacion/PLAN_MAESTRO_IMPLEMENTACION_FUGA_PLUS_v1.1.1.md), [progreso](docs/planificacion/PROGRESO_BUILD.md) y [bitácora](docs/planificacion/BITACORA.md).
- [Auditoría histórica](docs/auditoria/auditoria-tecnica-fugaplus.md), [plan de mejora](docs/auditoria/plan-mejora-fugaplus.md) e [informe de ejecución](docs/auditoria/ejecucion-plan-mejora-fugaplus.md).
- [Arquitectura real](../docs/ARQUITECTURA_FUGA_PLUS.md), [normalización](../docs/NORMALIZACION_CONCEPTOS.md), [dependencias](../docs/DEPENDENCIAS_SEGURIDAD.md) y [OpenAPI estático](../backend/docs/openapi.json).
- [QA Android financiero](../mobile/docs/QA_ANDROID_FUNCIONAL.md), [QA administrativo](../mobile/docs/QA_ANDROID_ADMIN.md), [áreas seguras](../mobile/docs/AREAS_SEGURAS_INTERNAS.md) y [release local](../mobile/docs/APK_RELEASE_LOCAL.md).
- [Prompts existentes](docs/prompts/) y [ejecución/instalación principal](../README.md).

Los documentos de planificación, auditoría inicial y versiones conservan etapas anteriores; no se utilizan como prueba de que hoy falten funciones ya implementadas. Se sustituyeron los enlaces inexistentes a salidas de HU/RF y a `prompts-diseño` por las rutas vigentes anteriores.

### UML editable y PNG para Word

Cuatro diagramas conciliados con código y migraciones; nueve imágenes de alta resolución a **300 ppp**. [Índice, fuentes y dimensiones](docs/diagramas/README.md).

| Editable | PNG |
| --- | --- |
| [Casos de uso](docs/diagramas/diagrama-casos-uso.drawio) | [Acceso/perfil](docs/diagramas/png/diagrama-casos-uso-01-acceso-perfil.png), [gastos/análisis](docs/diagramas/png/diagrama-casos-uso-02-gastos-analisis.png), [administración](docs/diagramas/png/diagrama-casos-uso-03-administracion.png) |
| [Clases](docs/diagramas/diagrama-clases.drawio) | [Contratos](docs/diagramas/png/diagrama-clases-01-contratos.png), [repositorios/fugas](docs/diagramas/png/diagrama-clases-02-repositorios-fugas.png) |
| [Componentes](docs/diagramas/diagrama-componentes.drawio) | [Componentes/despliegue](docs/diagramas/png/diagrama-componentes.png) |
| [Entidad–relación](docs/diagramas/diagrama-entidad-relacion.drawio) | [Completo](docs/diagramas/png/diagrama-entidad-relacion-01-esquema-completo.png), [identidad/soporte](docs/diagramas/png/diagrama-entidad-relacion-02-identidad-soporte.png), [finanzas/reglas](docs/diagramas/png/diagrama-entidad-relacion-03-finanzas-reglas.png) |

El mapa de historias conservado en esa carpeta representa especificación, no inventario de funciones implementadas. Los diagramas no acreditan migraciones aplicadas remotamente.

## 16. Uso de herramientas de inteligencia artificial

Los asistentes se utilizan como apoyo al análisis de requisitos, planificación, consulta técnica, revisión de código, elaboración de pruebas y documentación. La responsabilidad académica y la validación de resultados permanecen en la autora; una respuesta generada no sustituye pruebas ni aceptación.

OpenCode, Context7, Composio y CodeGraphContext figuraban como herramientas de apoyo en la documentación anterior. No se presentan como servicios activos del producto ni como integraciones verificadas por su mera mención. El runtime no necesita un gateway LLM o agentes del framework para interpretar gastos.

El uso de IA durante el desarrollo se distingue del comportamiento de FUGA+: diccionario y reglas propias para gastos/fugas; reconocimiento de voz Android dependiente del servicio del dispositivo, sin guardar audio.

## 17. Estado del proyecto y siguientes validaciones

**Comprobable en repositorio:** frontend/API integrados, módulos nativos, contratos, diez migraciones con once tablas propias, cuatro UML/nueve PNG y suites automatizadas. El estado funcional por HU se registra en la sección 6, con parciales y exclusiones explícitas.

**Reportado por la propietaria:** APK Android release instalado y probado, backend Render operativo y persistencia en Supabase. Los ensayos locales históricos mantienen su alcance: una URL guardada en PostgreSQL local no prueba un cambio en el perfil remoto.

**Por consolidar:** evidencia del esquema remoto y aplicación de 0010, firma/hash del APK final, aceptación completa de registro/correo/OAuth y administración, límites de HU-27/HU-30, escenarios Android adicionales y rendimiento representativo. No se afirma que las diez migraciones estén aplicadas ni que todas las historias estén aceptadas. No se consultaron credenciales o datos remotos para esta edición.

El siguiente cierre académico consiste en revisar esta trazabilidad y adjuntar evidencias verificables de los flujos seleccionados, sin presentar los parciales o las exclusiones como funcionalidades terminadas. Los cambios de alcance se deben conciliar posteriormente en las fuentes oficiales bajo autorización; esta tarea modifica solo este README.

## 18. Autoría

**Lorena Barragan Barragan**

Proyecto académico individual — Ingeniería de Sistemas

Electiva CPC — Periodo académico 2026-2
