# Áreas seguras del contenedor autenticado Android

2026-11-18, America/Bogota. Revisión sobre el QA local existente.

## Causa y corrección

La cabecera y las cinco pestañas de App.tsx estaban fuera del contenedor que mide
las barras del sistema. El SafeAreaView general no protegía ese contenido Android.
El defecto se repetía en Resumen, Registrar, Historial, Fugas y Perfil. Los
recordatorios locales se encuentran dentro de Fugas y comparten su marco.

El Shell autenticado ahora utiliza **PublicSafeArea**, el mismo componente existente
de bienvenida y formularios públicos. Su nombre histórico no limita su uso a esas
pantallas. Protege juntos la cabecera, el contenido y la navegación inferior; no
se añaden contenedores de insets a cada pantalla ni márgenes por modelo de teléfono.
La clave del contenedor sigue siendo la identidad del perfil, como antes.

Se reutilizan sin cambios WindowInsetsProbe, el módulo nativo FugaWindowInsets y
calculatePublicInsets. La medición incluye barras, recorte de cámara y teclado.
Si Android ya redujo el espacio por adjustResize o el padre ya descontó las barras,
el cálculo agrega únicamente la parte que falta. No suma dos veces el teclado.
Los formularios conservan su ScrollView y keyboardShouldPersistTaps="handled".
Los espaciados de diseño de la cabecera y las pestañas permanecen iguales.

No se cambiaron la navegación, los formularios, la lógica de autenticación, la
paleta, las notificaciones, las fotografías, el backend, las migraciones o dotenv.
No se instalaron dependencias. No se crearon gastos ni cuentas para esta revisión.

## Pruebas automatizadas

Desde mobile:

```powershell
npm.cmd run typecheck
npm.cmd test
```

TypeScript aprobado. **118 pruebas frontend aprobadas, 0 fallos, 0 omitidas**.
Las cuatro pruebas nuevas de internal-safearea.test.cjs verifican:

- Un único marco medido con cabecera, pantalla activa y pestañas en cada ruta interna.
- Teclado superpuesto, viewport reducido por Android, padre ya protegido y cierre del teclado.
- Las pestañas administrativas conservan su navegación y comparten la protección.
- Acceso público y recuperación no reciben un segundo marco autenticado.

Se ejecuta el App real con pantallas/proveedores simulados; estas pruebas verifican
la composición y los estados del contenedor, no sustituyen la revisión física del
teclado. Las pruebas existentes de formularios públicos y flujos de gastos también
pasaron. No se ejecutaron pruebas del backend al no modificarlo.

## Compilación y dispositivo

assembleDebug arm64 completado: BUILD SUCCESSFUL, 1 min 38 s, 290 tareas (7 ejecutadas,
283 actualizadas). Instalación con adb install -r: **Success**, conservando los datos
y la sesión. Se abrió FUGA+ en el Xiaomi.

APK: .verification/internal-safearea/fuga-plus-internal-safearea-debug.apk,
49.607.018 bytes. SHA256:
2ba22846db1439b9ad3e2d841b9f41b1f428e78021a720aa105c252676c43999.

El APK debug conserva el mismo hash del anterior porque no hubo cambios nativos
y este modo obtiene JavaScript de Metro, no lo incluye en el APK. La corrección
de App.tsx se sirve desde el Metro funcional 8086, reiniciado para cargarla, y se
comprobó en pantalla. El módulo nativo de insets está presente y el APK no incluye
archivos dotenv. No es una compilación release ni un despliegue.

Medición física del dashboard en una pantalla 1280×2772:

| Elemento | Antes (px, eje vertical) | Después (px, eje vertical) |
|---|---|---|
| Logo de cabecera | 20…189 | 172…341 |
| Texto FUGA+ | 58…149 | 210…301 |
| Área táctil de cada pestaña | 2577…2746 | 2525…2694 |
| Contenido desplazable | Sin protección compartida | 363…2496 |

El área segura de referencia del dispositivo es 152…2720. La cabecera y todas las
áreas táctiles de las pestañas quedan dentro. La separación inferior de 26 px
corresponde al padding de diseño existente de 8 dp; no es un segundo inset.
Se inspeccionó una captura del dashboard con únicamente los gastos ficticios
autorizados. No se guardaron capturas del perfil ni XML con datos de usuario.

La propietaria completó el recorrido en el Xiaomi y confirmó **«Todas quedan bien»**
para Resumen, Registrar, Historial, Fugas, el control de recordatorios y Perfil.
También confirmó **«Sí, campos y botones accesibles»** al abrir el teclado y
desplazarse en Registrar y Perfil, sin guardar ni cambiar datos.

La accesibilidad con teclado es una comprobación manual confirmada. La medición
final de etiquetas estáticas volvió a mostrar el viewport sin teclado; no se
presenta como una captura instrumental del IME abierto. No se ha comprobado
este cambio en otros modelos, orientaciones o iOS físico.

## Entorno que permanece disponible

- Metro funcional: 8086; teléfono 8081 → PC 8086 por USB.
- FastAPI QA financiero: 127.0.0.1:18000; teléfono 18000 → PC 18000.
- PostgreSQL QA local y QA fotográfico 18001 conservados, sin reiniciarlos.
- health y ready de ambos QA respondieron 200 durante esta revisión.

No utilizar el Metro ficticio de bienvenida 8085 para iniciar sesión. No cerrar
FastAPI QA: su cierre normal elimina la base desechable de esa ejecución.
Mantener el USB conectado y usar únicamente la cuenta ficticia existente.

## Evidencias y archivos

Evidencias locales ignoradas por Git: .verification/internal-safearea/, con
dashboard.png, dashboard.json y after-manual-review.json (solo etiquetas estáticas
y límites), apk.json, qa-before.json y evidence.json (agregados sin identidad,
pruebas y confirmaciones manuales). El auxiliar local de medición es
.tools/inspect-internal-safearea.py; filtra el XML en memoria y borra el archivo
temporal del dispositivo sin guardar datos del perfil.

La comprobación final devolvió 200 en Metro 8086, health/ready de FastAPI QA y
ready del QA fotográfico. Los puertos USB siguen conectados. Se conservaron los
seis gastos ficticios por COP 28.000 y la fuga vigente. Los contadores de peticiones
POST/PUT/PATCH/DELETE del QA financiero no cambiaron durante esta tarea.

Archivos del proyecto cambiados por esta tarea:

- App.tsx: importación y uso del contenedor compartido; sin cambios en su lógica.
- tests/internal-safearea.test.cjs: cuatro pruebas de regresión del contenedor.
- docs/AREAS_SEGURAS_INTERNAS.md: diagnóstico, pruebas y evidencia.
- docs/RECUPERACION_ACCESO_QA.md: vínculo al seguimiento de este hallazgo.

Los cambios anteriores del proyecto se conservaron. Sin commits, pushes, despliegues
ni modificaciones de datos o esquema en Supabase remoto.
