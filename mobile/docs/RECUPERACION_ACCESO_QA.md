# Recuperación de acceso Android y revisión interna

2026-11-18, America/Bogota. Sin commits, pushes o despliegues.

## Diagnóstico

El teléfono conservaba adb reverse de su puerto 8081 hacia **Metro 8085**, iniciado
con welcome-preview.cjs. Ese modo usa un dominio Auth ficticio y una API sin servicio
para revisar pantallas públicas sin cerrar la sesión real. No permite iniciar sesión.
Se comprobó en memoria el bundle servido: contenía esa configuración ficticia.

FastAPI, PostgreSQL local y los Metro anteriores estaban activos. La causa principal
era el modo de ejecución, no una modificación en Safe Area ni un rechazo verificado
de contraseña por Supabase. No se cambió la contraseña ni se manipularon tokens.

GET público de Auth settings y JWKS respondieron 200 con la configuración pública
existente. La clave de cliente se identificó como publishable sin mostrar su valor.
No se leyó backend/.env.local ni se modificaron archivos dotenv.

## Corrección mínima aplicada

android-qa.cjs añade **metro-review**, que inicia un Metro nuevo en 8086 con las
variables públicas existentes y FastAPI QA en 127.0.0.1:18000. Así se carga el código
actual sin detener los otros Metro ni reiniciar las bases desechables.

Se verificó en memoria que el nuevo bundle contiene la URL/clave pública esperadas,
la API QA correcta y los componentes actuales de Safe Area. Ya no contiene la
configuración Auth ficticia de la vista previa. No se guardó ese bundle.

Se cambió el reverse USB de 8081 hacia 8086 y se confirmó el de 18000 hacia 18000.
Se reabrió el APK debug ya instalado, sin reinstalar, limpiar datos, forzar logout,
crear cuentas o introducir credenciales desde herramientas. La propietaria confirmó:
**«Sí, ya veo el dashboard»**. El SDK puede recuperar una sesión válida existente;
si solicita acceso, la contraseña se introduce únicamente en el teléfono.

No se modificaron AuthProvider, Access, App, el cliente Supabase, los componentes de
insets, la paleta, el backend ni las migraciones para resolver el acceso.

## Entorno que queda activo

| Componente | Estado / dirección local |
|---|---|
| Metro funcional de esta revisión | 8086, activo |
| FastAPI QA financiero | 127.0.0.1:18000, health/ready 200 |
| PostgreSQL QA | 127.0.0.1:55440, accesible por FastAPI |
| USB | Teléfono 8081 → PC 8086; teléfono 18000 → PC 18000 |
| Datos ficticios conservados | 6 gastos, COP 28.000, una fuga vigente |
| QA de fotografías | 18001, conservado separado; ready 200 |
| Servicios anteriores | Backend 8000 y Metro 8083/8084/8085 permanecen activos |

No se detuvieron los servicios al terminar. El APK permanece abierto en el QA
funcional. Es un entorno debug que necesita USB y PC; no es un despliegue.
El QA financiero usa únicamente PostgreSQL local. Supabase Auth se utiliza para
la cuenta ficticia existente; no se crearon usuarios ni se hicieron operaciones
administrativas, escrituras de perfiles o cambios de esquema en Supabase.

Para reproducir solo cuando Metro 8086 no esté ya activo:

```powershell
node mobile/scripts/android-qa.cjs check
node mobile/scripts/android-qa.cjs metro-review
.tools/android-sdk/platform-tools/adb.exe reverse tcp:8081 tcp:8086
.tools/android-sdk/platform-tools/adb.exe reverse tcp:18000 tcp:18000
```

No usar welcome-preview.cjs para pruebas con sesión. No reiniciar el proceso
FastAPI QA para cambiar de pantalla: al cerrarse normalmente elimina su base
desechable. No apuntar esta revisión al backend conectado a datos remotos.

## Revisión interna y hallazgo original

Se preparó el recorrido Resumen → Registrar → Historial → Fugas → Perfil y el
control de recordatorios dentro de Fugas, sin guardar nuevos datos ni cambiar permisos.
La propietaria informó superposición **en todas** las pantallas internas.

La cabecera y las pestañas son compartidas por el Shell autenticado de App.tsx.
Ese Shell todavía utiliza el SafeAreaView general y no el contenedor medido que
ya protege bienvenida y formularios públicos. Por eso el mismo defecto se repite.
Se midieron únicamente etiquetas estáticas, sin guardar perfiles ni correos:

- Texto de la cabecera FUGA+: y=58…149, dentro del área superior reservada al sistema.
- Pestañas inferiores: y=2577…2746, con parte del área táctil en la zona de gestos.
- Referencia del marco seguro medido en este teléfono: y=152…2720, pantalla 1280×2772.

| Pantalla / control | Acceso para revisión | Barras del sistema |
|---|---|---|
| Dashboard / Resumen | Acceso confirmado | Superposición reportada |
| Registrar | Recorrido preparado, sin confirmar gastos | Superposición reportada |
| Historial | Consulta de gastos ficticios existentes | Superposición reportada |
| Fugas | Lista/evidencia del QA local | Superposición reportada |
| Recordatorios locales | Control dentro de Fugas, no una pantalla independiente | Afectado por el mismo contenedor |
| Perfil | Solo consulta, sin guardar o cambiar fotografía | Superposición reportada |

En la recuperación de acceso no se aplicó un cambio al Shell privado: esa tarea
estaba limitada a restablecer el inicio de sesión. Posteriormente se autorizó y
aplicó la protección compartida en App.tsx. La implementación, las 118 pruebas
aprobadas y las mediciones del Xiaomi están documentadas en
[Áreas seguras internas](AREAS_SEGURAS_INTERNAS.md). Allí se registra por separado
la confirmación manual de las pantallas y el teclado.

Las fotografías del ensayo HU-08 pertenecen a su QA separado. Cambiar fotografía
sigue bloqueado en el QA financiero por diseño; no hace falta habilitar cargas
para revisar visualmente el perfil. No se emitieron nuevas cargas ni borrados.

## Pruebas y evidencia

**114 pruebas frontend aprobadas, cero fallos y cero omitidas; TypeScript aprobado.**
No se repitieron pruebas del backend: no hubo cambios en su código; se comprobaron
health, ready, validación de la sesión y consultas de estado QA.

Evidencia local sin credenciales: .verification/qa-access/evidence.json y
shell-bounds.json. Los datos financieros locales permanecen en seis gastos por
COP 28.000. No se guardaron bundles con configuración ni capturas de perfiles.

Archivos de esta tarea: scripts/android-qa.cjs, este documento y la referencia de
modo funcional añadida en docs/QA_ANDROID_FUNCIONAL.md. Los demás cambios previos
del proyecto se conservaron.
