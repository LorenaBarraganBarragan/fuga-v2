# Arquitectura implementada de FUGA+

## Flujo
React Native/Expo → SDK Supabase Auth para identidad.
React Native/Expo → FastAPI /api/v1 para todos los datos financieros.
FastAPI → SQLAlchemy/Psycopg → PostgreSQL en Supabase.
La app no consulta tablas financieras mediante el SDK de Supabase.

## Backend
- api/v1: contratos HTTP, validaciones y dependencias.
- core/security.py: firma JWKS, issuer, audience, exp, iat y sub UUID. No existe bypass local.
- El perfil persistido decide rol y disabled_at en cada solicitud.
- require_user deniega finanzas a administradores; require_admin protege metadatos y auditoría.
- services: integración y consultas; domain: interpretación, agrupación y cálculos deterministas.
- repositories: SQL parametrizado, propietario obligatorio y cursor validado.
- Los errores SQL se convierten en indisponibilidad explícita; no se transforman en listas vacías.

## Transacciones
Los cambios de gastos y el análisis serializan por usuario mediante advisory locks transaccionales.
La creación compara una huella del intento original y garantiza idempotencia concurrente.
Las mutaciones invalidan snapshots vigentes; las consultas de fugas recalculan bajo demanda.
Cada snapshot almacena una huella de su evidencia; se conserva su ID cuando la evidencia no cambia.
La lectura de detalle comprueba propietario, vigencia y gastos no eliminados.

Los cambios de estado administrativo bloquean la fila objetivo durante la llamada al proveedor.
Si falla Supabase al desactivar, se confirma el bloqueo local y se informa sincronización pendiente.
No se permite modificar cuentas administrativas desde la gestión normal de cuentas.
No se promete revocación instantánea de todos los access tokens del proveedor.

## Dinero y fechas
COP entero 1…100.000.000; los importes confirmados no admiten coerción de strings, floats o booleanos.
Promedio y porcentajes usan Decimal y ROUND_HALF_UP; porcentajes se serializan a un decimal.
Meses válidos desde enero de 2020 hasta el actual, con límites SQL explícitos.
FUGA-01: hoy y los 29 días anteriores, según America/Bogota.
Catálogo de nueve categorías leído de BD; los UUID estáticos solo quedan para pruebas puras.
El clasificador mantiene las coincidencias existentes y el desempate por longitud; no se inventan equivalencias
ni contenido de sugerencias que no estén aprobados.

## Móvil
AuthProvider administra sesión, enlaces PKCE, perfil y limpieza al salir.
Los tokens se guardan en SecureStore en fragmentos en nativo; en web se usa sessionStorage.
La web es auxiliar de revisión; no se guarda sesión en localStorage.
No existe caché financiera persistente ni borrador servidor. Cada pantalla privada se desmonta al salir.
Los borradores se descartan al abandonar la pantalla con confirmación de cambios.
El cliente usa la misma API para gastos, filtros, edición, estadísticas, fugas, perfil y administración.
Google y recuperación se habilitan solo con configuración confirmada.
Los recordatorios locales no solicitan tokens push y no envían notificaciones remotas.

## Datos y migraciones
0001…0007: tablas y reglas existentes reutilizadas.
0008_integracion.sql (local, no aplicada remotamente):
huella de intentos/evidencia, permisos mínimos, auditoria, actividad_mensual,
tarea_retencion y estado de sincronización con Auth.
Se mantiene borrado lógico de gastos. No hay eliminación física automática de cuentas o datos reales.

## Límites de verificación
Las pruebas de integración con PostgreSQL están pospuestas por instrucción de la propietaria.
Los mocks de proveedores en pruebas no se usan como fallback de ejecución.
La identidad Supabase, SMTP, OAuth, Cloudinary, permisos de dispositivo y binarios APK/IPA siguen
requiriendo configuración y pruebas reales.
No debe declararse ninguna historia íntegramente aceptada basándose solo en bundles o pruebas unitarias.
