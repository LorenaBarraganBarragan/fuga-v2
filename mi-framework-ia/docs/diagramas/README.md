# Diagramas de FUGA+ para el informe final

Revisión: **19 de noviembre de 2026**. Estos cuatro diagramas representan el código y las migraciones presentes en el repositorio. No certifican por sí solos que una configuración externa esté habilitada ni que todas las migraciones se hayan aplicado en una base remota. No se consultaron datos de producción para elaborarlos.

## Archivos editables e imágenes

Los archivos `.drawio` contienen páginas independientes y conservan figuras, campos y conectores editables. Todas las imágenes tienen fondo blanco, resolución de exportación 3× y metadatos de **300 ppp**, sin capturas de cuentas ni credenciales.

| Diagrama editable | Página | PNG para Word | Tamaño en píxeles |
| --- | --- | --- | --- |
| [Casos de uso](diagrama-casos-uso.drawio) | 01 · Acceso y perfil | [Acceso y perfil](png/diagrama-casos-uso-01-acceso-perfil.png) | 4800 × 3540 |
| Casos de uso | 02 · Gastos y análisis | [Gastos y análisis](png/diagrama-casos-uso-02-gastos-analisis.png) | 4800 × 3660 |
| Casos de uso | 03 · Administración | [Administración](png/diagrama-casos-uso-03-administracion.png) | 4800 × 3540 |
| [Clases](diagrama-clases.drawio) | 01 · Identidad y contratos de gastos | [Contratos](png/diagrama-clases-01-contratos.png) | 4800 × 4560 |
| Clases | 02 · Repositorios y resultados de fugas | [Repositorios y fugas](png/diagrama-clases-02-repositorios-fugas.png) | 4800 × 4320 |
| [Componentes](diagrama-componentes.drawio) | Componentes y despliegue | [Componentes](png/diagrama-componentes.png) | 5400 × 4650 |
| [Entidad–relación](diagrama-entidad-relacion.drawio) | 01 · Esquema completo | [Esquema completo](png/diagrama-entidad-relacion-01-esquema-completo.png) | 6480 × 5460 |
| Entidad–relación | 02 · Identidad y soporte | [Identidad y soporte](png/diagrama-entidad-relacion-02-identidad-soporte.png) | 4920 × 4200 |
| Entidad–relación | 03 · Finanzas, reglas y evidencia | [Finanzas y reglas](png/diagrama-entidad-relacion-03-finanzas-reglas.png) | 4920 × 4620 |

Para Word, insertar los PNG como imágenes y conservar su proporción. Usar las páginas de detalle del ER en A4 horizontal para leer los campos; el esquema completo puede utilizarse como panorama o anexo en una página más grande. Evitar la compresión de imágenes de Word cuando se prepare el documento final. Para editar, abrir el `.drawio` correspondiente en diagrams.net y seleccionar su pestaña de página.

## Correspondencia con la implementación

### Entidad–relación

Se representan **11 tablas propias**: `categoria`, `regla_fuga`, `regla_fuga_version`, `perfil`, `gasto`, `fuga`, `fuga_evidencia`, `auditoria`, `actividad_mensual`, `tarea_retencion` y `perfil_foto_carga`. La referencia externa `auth.users`, gestionada por Supabase Auth, no forma parte de ese total y muestra únicamente los campos usados para explicar la integración.

El esquema completo incluye todos los campos resultantes de las migraciones y sus **13 claves foráneas**, incluida `perfil.id → auth.users.id`. Los identificadores relacionales son UUID; las excepciones explícitas son `perfil_foto_carga.public_id` (TEXT) y la clave compuesta de `actividad_mensual` (`usuario_id` UUID, `periodo` DATE). `auditoria.objetivo_id` es UUID opcional y **no tiene FK**. Los importes COP son BIGINT.

Se distinguen nulabilidad, claves, cardinalidades y acciones de borrado: `C` = CASCADE, `R` = RESTRICT, `N` = NO ACTION. Se resumen los índices únicos parciales de fotografías y snapshots vigentes, el aislamiento por propietario y RLS. La relación entre gastos y fugas pasa por `fuga_evidencia`; las versiones de reglas se vinculan mediante `regla_fuga_version`.

Fuentes: [migraciones 0001–0010](../../../supabase/migrations/), especialmente [integración](../../../supabase/migrations/0008_integracion.sql), [seguridad e integridad](../../../supabase/migrations/0009_seguridad_integridad.sql) y [fotografías](../../../supabase/migrations/0010_fotografias_perfil.sql).

### Clases

Se sustituyó el modelo conceptual anterior por una selección de **clases realmente declaradas en Python**, con nombres y tipos de campos obtenidos del código. El archivo está codificado en UTF-8, con acentos legibles. Incluye esquemas Pydantic de identidad, interpretación, gastos y fugas, los dataclasses `CurrentUser` y `FugaCandidata`, repositorios y sus relaciones reales de herencia o composición.

No se supone que exista una clase ORM para cada tabla: el backend utiliza repositorios con consultas SQL. Los DTO que declaran `str` para un UUID serializado conservan ese tipo; el ER muestra el tipo PostgreSQL UUID. Los servicios basados en funciones se representan en componentes. Esta es una vista seleccionada del backend, no un inventario de todas las clases de las dependencias.

Fuentes: [seguridad](../../../backend/app/core/security.py), [esquemas](../../../backend/app/schemas/), [repositorios](../../../backend/app/repositories/) y [regla FUGA-01](../../../backend/app/domain/leaks/rule_fuga_01.py).

### Casos de uso

Se distinguen visitante sin sesión y los dos roles persistidos, `usuario` y `administrador`. Ambos roles se autentican desde el mismo formulario; FastAPI obtiene el rol de `perfil`, sin conceder al administrador acceso a las finanzas individuales. Se muestran las operaciones administrativas implementadas: búsqueda, filtros, paginación, detalle mínimo, estadísticas de cuentas/actividad y activación/desactivación de cuentas usuarias.

La vista de usuario incluye interpretación por texto, dictado Android con revisión, confirmación, historial, edición y borrado lógico, estadísticas, comparación mensual, análisis/evidencia de fugas, avisos locales y perfil con fotografía. La recuperación por correo y Google están marcados como dependientes de configuración externa. No se representan metas, límites mensuales, recomendaciones inteligentes ni push remotas como funcionalidades implementadas.

Fuentes: [pantallas](../../../mobile/src/screens/), [voz](../../../mobile/src/voice/VoiceInput.tsx), [notificaciones](../../../mobile/src/lib/notifications.ts), [API v1](../../../backend/app/api/v1/) y [gestión de cuentas](../../../backend/app/services/accounts_service.py).

### Componentes y despliegue

Se muestra el APK Android con Expo/React Native, los módulos Kotlin de voz y medición de insets, notificaciones locales, Supabase Auth y su almacenamiento de sesión. El backend FastAPI/Uvicorn en Render valida JWT con JWKS, rol y propietario; accede a PostgreSQL de Supabase mediante SQLAlchemy/Psycopg y TLS. El cliente sube fotografías directamente a Cloudinary con firma obtenida del backend, que verifica la carga y persiste su URL. Los flujos numerados identifican las solicitudes; las respuestas utilizan esos mismos canales.

El APK release incorpora el JavaScript y no requiere Metro ni USB. Los simuladores QA no forman parte de esta vista de producción. El dictado depende del permiso y del reconocedor del dispositivo; el análisis de fugas usa reglas/diccionario, sin IA generativa externa. Los avisos se originan al consultar el análisis, sin un motor de análisis ejecutándose con la aplicación cerrada.

Fuentes: [App.tsx](../../../mobile/App.tsx), [módulos Android](../../../mobile/modules/), [cliente Supabase](../../../mobile/src/lib/supabase.ts), [servicio de fotografías](../../../backend/app/services/profile_photos.py), [sesión PostgreSQL](../../../backend/app/db/session.py), [configuración Render](../../../render.yaml) y [compilación release](../../../mobile/scripts/android-release.ps1).

## Alcance y comprobaciones

- Se conservaron los parámetros de FUGA-01 1.0 presentes en código y semillas: 30 días, mínimo 3 gastos en 3 fechas distintas, COP 1.000–30.000 por gasto y suma mínima de COP 15.000. La normalización de conceptos usa la versión 1.1.
- Se comprobaron XML editable, referencias de conectores, correspondencia de las 11 tablas / 81 columnas / 13 FK con las migraciones, 16 clases con el código, UTF-8, dimensiones y densidad de los nueve PNG. Se revisaron visualmente las nueve páginas.
- No se modificaron código funcional, migraciones, datos, variables de entorno ni staging. No se ejecutaron servicios de aplicación, consultas de producción ni pruebas que accedan a datos.
- [diagrama-historias-usuario.drawio](diagrama-historias-usuario.drawio) se conservó sin cambios: corresponde al mapa de especificación y puede contener funcionalidades previstas. Para describir **lo implementado**, utilizar los cuatro diagramas revisados en este índice.
