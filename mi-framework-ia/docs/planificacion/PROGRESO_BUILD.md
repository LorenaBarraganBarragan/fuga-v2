# PROGRESO BUILD — FUGA+

## Estado vigente — plan de mejora autorizado 2026-11-18

Seguimiento HU-08: 325 pruebas backend/31 SQL y 97 frontend aprobadas. Interfaz de
vista previa/confirmación, firma de servidor y limpieza conservadora implementadas.
GET Cloudinary /ping 200 tras corrección manual de credenciales. Dos PNG sintéticos
subidos bajo autorización; propietaria confirmó vista previa/cancelación, persistencia
tras login/logout y sustitución. Corregida serialización de archivos en fetch de Expo 58.
URL verificada solo en PostgreSQL QA local; migración 0010 y limpieza remotas no ejecutadas.
[Informe HU-08](../auditoria/hu08-fotografia-perfil.md).

La fuente de resultados actuales es [Ejecución ACT-01 a ACT-15](../auditoria/ejecucion-plan-mejora-fugaplus.md).
Se parte del respaldo `ce24348`, no del árbol sin seguimiento de la auditoría histórica.
Hay pruebas SQL nuevas en PostgreSQL local separado y medición de cobertura; no se
modifican Supabase remoto, claves o archivos .env.local. Voz Android es prioridad adicional.
Seguimiento QA previo a HU-08: 301 pruebas backend/22 SQL y 86 frontend aprobadas.
Debug QA con configuración pública por USB y datos financieros locales: propietaria
confirmó login real con cuenta ficticia existente, texto/dashboard, dictado y aviso
local/toque/sin duplicado. Registros locales: seis gastos/COP 28.000 y fuga cafe/COP 25.000.
El release inicial sin Metro acredita navegación pública; el debug funcional requiere Metro.
Pendientes: casos físicos adicionales de ciclo de vida/denegación, callbacks de correo,
release con backend HTTPS, CI y Render remotos. Ver evidencia-qa-android.json en auditoria.
Los apartados siguientes son bitácora histórica: sus bloqueos, conteos y referencias a
sessionStorage o Supabase sin configurar no describen automáticamente el estado actual.

## Revisión SQL para `fuga-plus` — 2026-11-16
- Proyecto remoto creado por la propietaria, plan gratuito; no se accedió a él ni se pidieron secretos.
- Revisadas y corregidas 0001–0008; añadida 0009_seguridad_integridad.sql.
- RLS en las diez tablas; catálogos de solo lectura, perfiles propios activos y columnas protegidas.
- Auth: FK a PK auth.users, trigger SECURITY DEFINER con search_path vacío, rol fijo y backfill no destructivo.
- Evidencia del mismo propietario, fechas Bogotá, catálogo cerrado y versiones de reglas inmutables.
- Todos los triggers son repetibles; la reaplicación conserva registros existentes de prueba.
- PostgreSQL 16 local: 165 pruebas pasan, incluidas 14 de integración con permisos iniciales permisivos.
- Sustituto local del esquema Auth: no equivale a validar GoTrue/JWT/SMTP del proyecto remoto.
- Guía de aplicación y conexión: supabase/docs/CONEXION_SUPABASE.md; verificación SQL de solo lectura en supabase/tests/.
- Sin migraciones remotas, despliegues, commits ni instalación de dependencias.

Fecha: 2026-11-15 · America/Bogota.
Fuente autorizada: HISTORIAS_DE_USUARIO.md y REQUERIMIENTOS.md 3.0.
D-01…D-15 prevalecen sobre criterios heredados contradictorios.
Sin commits, pushes, despliegues ni migraciones remotas.

## Estado
Hay implementación integrada de backend y móvil, pero el proyecto NO está terminado ni aceptado.
Distinguir código, pruebas locales y verificación real de proveedores.
La solicitud del 2026-11-16 autoriza nuevamente las pruebas PostgreSQL locales.
Las nueve migraciones se probaron localmente; Supabase remoto sigue pendiente.

## Lista persistente de tareas
| Trabajo | Estado | Archivos / evidencia |
|---|---|---|
| Firma JWT, claims, rol y estado persistido | Implementado y probado localmente | core/security.py; tests/security |
| Gastos: interpretar, confirmar, crear, listar, filtros, editar y borrado lógico | Implementado; integración final pendiente | api/v1/expenses.py; repositories/expenses.py; móvil NewExpense/History |
| Catálogo real y estadísticas exactas | Implementado y pruebas de dominio | categories; analytics_service; Dashboard |
| FUGA-01, ventana 30 días, snapshots y detalle de evidencia | Implementado; PostgreSQL final pendiente | leaks_service; api/v1/leaks.py; Leaks |
| Perfil, fotos firmadas y foto Google consentida | Implementado; proveedores pendientes | api/v1/me.py; Profile |
| Administración, roles, estados y auditoría | Implementado; Auth real pendiente | admin.py; accounts_service.py; Admin |
| Retención: programación a 30 días | Cola implementada; supresión y mantenimiento pendientes | tarea_retencion; no borrado real automático |
| Aplicación Expo/TypeScript y Auth | Implementada; bundles y pantalla pública comprobados | mobile/App.tsx; src/auth |
| Correo, registro/login/cierre, Google OAuth y recuperación reales | Bloqueo externo | Configurar y verificar Supabase/SMTP/OAuth |
| Voz Android | Código Kotlin y autolinking comprobados; compilación/dispositivo pendientes | modules/fuga-voice; VoiceInput |
| Alertas locales | Código y política horaria/frecuencia probados; dispositivo pendiente | notifications.ts; validation.ts |
| Comparación y resumen mensual de fugas | Código implementado; resumen SQL pendiente | analytics/comparison; leaks/monthly-summary |
| Sugerencias HU-26 | Pendiente de catálogo aprobado | No inventar contenido |
| Límites HU-28/HU-29 | Excluidos Won't | Sin implementación |
| Compatibilidad nativa y aceptación HU/RF completas | Pendiente | Android SDK/JDK compatible, macOS/Xcode para iOS, dispositivos |
| Documentación y ejecución reproducible | En actualización | README.md; docs/ARQUITECTURA_FUGA_PLUS.md; informe |
| Pruebas PostgreSQL locales | 14 de integración pasan (2026-11-16) | Base desechable; Supabase Auth real pendiente |

## Pruebas realizadas
- Backend actual: 151 pruebas sin PostgreSQL pasan; una advertencia de deprecación upstream de TestClient/httpx.
- Ruff F/E9/I y mypy dominio: verificaciones locales; repetir solo tras cambios relevantes.
- Móvil: 16 pruebas de validación y política de notificaciones pasan; TypeScript sin errores.
- Bundles web/Android/iOS generados; esto NO es un APK/IPA ni una prueba de voz.
- Autolinking reconoce FugaVoiceModule.
- Smoke Chrome real: bienvenida 390×844, navegación registro/login/recuperación y falta de configuración explícita.
- Auditorías npm y pip-audit: cero vulnerabilidades conocidas en la revisión posterior a actualizaciones.
- Ronda PostgreSQL ANTERIOR a la petición de posponer: 104 pasaron y 1 falló por permisos SELECT
  del rol authenticated. Se preparó ajuste local de permisos/bootstrap, NO se reejecutó.
  Esa ronda NO certifica las migraciones finales ni Supabase Auth.
- No se contactó Supabase remoto para aplicar cambios.

## Dependencias
Entorno Python aislado, sin paquetes del usuario; requirements.lock.
Expo estable 58 con React/React Native compatibles, package-lock.json y TypeScript requerido.
Se actualizaron versiones dentro del mismo stack para corregir vulnerabilidades; falta certificación nativa.

## Bloqueos y permisos
- Sin credenciales/proveedores reales verificados.
- Aplicar migraciones remotas y desplegar requiere aprobación separada.
- No eliminar datos reales; la cola de retención no ejecuta borrados.
- No descargar PostgreSQL portátil. Las pruebas locales se autorizaron nuevamente el 2026-11-16.
- Prettier adicional fue rechazado por revisión automática; no se instaló.
- La restricción anterior de dependencias fue revocada expresamente para Python y Expo.

## Siguiente tarea concreta
Revisar las variables de los ejemplos y preparar el entorno Supabase de desarrollo.
Cuando exista autorización específica, revisar/aplicar 0001…0009 en ese entorno y verificar Auth,
aislamiento entre dos usuarios, permisos RLS y flujo móvil completo.
Antes de cerrar las HU, validar también SMTP, Google, Cloudinary y dispositivos.
No repetir bootstrap ni reemplazar la arquitectura; reutilizar los módulos actuales.

## Sesi?n de visualizaci?n local
- Expo en desarrollo: http://localhost:8081, con las dependencias existentes.
- FastAPI con recarga: http://127.0.0.1:8000; documentaci?n /docs y salud /health.
- /health y /docs responden 200; /ready devuelve 503 por falta de BD; /api/v1/expenses devuelve 401 sin sesi?n.
- Se verificaron bienvenida, registro, login, recuperaci?n y regreso en Chrome contra el servidor de desarrollo.
- Se ampli? smoke_web.py para admitir --url y --timeout; no se reconstruy? la aplicaci?n.
- No hay .env.local con Supabase configurado: las pantallas privadas requieren servicios reales.
- No se ejecutaron migraciones, despliegues, commits ni pruebas PostgreSQL.
- Los servidores de desarrollo se dejan activos para la revisi?n de la propietaria.
- Logs y PIDs locales: mobile/.verification/ (ignorado por Git).

## Visualizaci?n Android con Expo Go ? 2026-11-16
- Revisada compatibilidad de SDK 58 y dependencias con Expo Go.
- FugaVoice se requiere opcionalmente y usa alternativa de texto; la voz Kotlin necesita compilaci?n nativa.
- Expo Go LAN iniciado en exp://192.168.88.232:8082 con --go --lan; puerto web 8081 conservado.
- Manifiesto Android responde 200, SDK 58.0.0; bundle Android de desarrollo responde 200.
- QR y PID temporales en mobile/.verification/expo-go-qr.png y expo-go.json (ignorados por Git).
- Falta confirmar conexi?n y ejecuci?n en el tel?fono f?sico; no se modific? el firewall ni se usaron t?neles.
- Sin cambios funcionales, instalaciones, compilaciones nativas, despliegues ni servicios externos configurados.
