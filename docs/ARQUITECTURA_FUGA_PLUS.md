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
La huella incluye normalización 1.1. Consultar sin cambios no invalida ni reactiva snapshots;
se invalidan solo los anteriores que ya no correspondan a los candidatos. Evidencia nueva
se inserta en lote y los nombres de categorías se consultan juntos. Se conserva el lock por usuario.
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
Los tokens se guardan en SecureStore en fragmentos en nativo; en web se usa
**localStorage**, compartido entre pestañas del mismo navegador para PKCE.
No existe caché financiera persistente ni borrador servidor. Cada pantalla privada se desmonta al salir.
Los borradores se descartan al abandonar la pantalla con confirmación de cambios.
El cliente usa la misma API para gastos, filtros, edición, estadísticas, fugas, perfil y administración.
Google y recuperación se habilitan solo con configuración confirmada.
Los recordatorios locales no solicitan tokens push y no envían notificaciones remotas.
Se asocian al canal patterns y se serializan por usuario/categoría/concepto/versión,
con siete días de separación y silencio 21:00–08:00 Bogotá. Fallos no bloquean el análisis.
Las lecturas HTTP tienen hasta dos intentos de 45 segundos y cancelación; las mutaciones
no se reenvían automáticamente. Una respuesta de una sesión anterior se descarta.
La clave de confirmación se conserva durante el reintento manual del mismo contenido.

## Estadísticas y configuración de entrega
El backend agrega SUM/COUNT por categoría en PostgreSQL y conserva cálculos exactos/Decimal.
El dashboard no solicita comparación mensual hasta que el usuario la pide; contratos existentes intactos.
Settings valida prod, origen Auth, CORS HTTPS, Psycopg y verify-full con CA accesible.
La ruta de CA relativa se resuelve desde backend, sin modificar DATABASE_URL persistida.
Pool inicial 3+2 conexiones por proceso, timeout de conexión 5 s y límites SQL/lock explícitos.
El launcher scripts/start.py utiliza PORT y un proceso. render.yaml es preparación local, no despliegue.

## Datos y migraciones
0001…0007: tablas y reglas existentes reutilizadas.
0008_integracion.sql:
huella de intentos/evidencia, permisos mínimos, auditoria, actividad_mensual,
tarea_retencion y estado de sincronización con Auth.
Se mantiene borrado lógico de gastos. No hay eliminación física automática de cuentas o datos reales.

## Límites de verificación
El plan de mejora se ejecuta por autorización del 2026-11-18. Las pruebas SQL utilizan
un clúster local separado, no Supabase. Resultados y límites vigentes:
mi-framework-ia/docs/auditoria/ejecucion-plan-mejora-fugaplus.md.
Los mocks de proveedores en pruebas no se usan como fallback de ejecución.
La identidad Supabase, SMTP, OAuth, Cloudinary, permisos de dispositivo y binarios APK/IPA siguen
requiriendo configuración y pruebas reales.
No debe declararse ninguna historia íntegramente aceptada basándose solo en bundles o pruebas unitarias.
El estado remoto previamente comunicado por la propietaria no se recertifica al ejecutar tests locales.
