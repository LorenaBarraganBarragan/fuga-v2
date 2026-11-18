# Áreas seguras de acceso público — FUGA+

2026-11-18, America/Bogota. Corrección visual de Crear cuenta e Iniciar sesión.

## Resultado

La propietaria comprobó ambas pantallas en el Android físico: campos, botones,
desplazamiento y errores locales accesibles con el teclado abierto, sin superposición
con las barras del sistema. Se utilizó exclusivamente la vista previa ficticia;
no se introdujeron credenciales ni se enviaron formularios a Supabase.

**114 pruebas frontend aprobadas, cero fallos y cero omitidas. TypeScript aprobado.**
El APK debug se compiló e instaló con -r, conservando datos y almacenamiento de sesiones.
No se cambiaron la lógica Auth, Supabase, el backend, PostgreSQL ni las dependencias.

## Causa y corrección

Access usaba Page, cuyo padding de diseño no protege frente a las barras de Android
en modo edge-to-edge. La bienvenida ya reservaba espacio fuera del scroll, pero su
reserva inferior fija no cumplía el nuevo requisito de medir los insets reales.

Se extrajo PublicSafeArea para bienvenida y formularios públicos. Mantiene las
barras fuera del área desplazable y usa datos medidos de **WindowInsetsCompat**:
status/navigation/caption bars, display cutout e IME. No usa una altura fija por
modelo ni StatusBar.currentHeight como medida de seguridad. Los padding de 16/24 dp
del contenido siguen siendo espacios de diseño existentes, independientes de los insets.

Un observador local de Expo Modules en modules/fuga-window-insets lee únicamente
geometría del sistema. Se reutilizan Expo/Kotlin/AndroidX ya instalados, igual que
el módulo local de voz; no se añadió ninguna librería externa ni permiso Android.
No modifica listeners del decorView o de la actividad: observa su propia vista,
no consume los insets y se desregistra al salir de las pantallas públicas.

El cálculo compara la obstrucción real con el viewport disponible. Si adjustResize
ya redujo la ventana por el teclado, no vuelve a descontar esa altura. También
descuenta lo que un contenedor padre ya haya reservado. Se esperan las primeras
medidas válidas antes de mostrar controles interactivos, sin recurrir a márgenes
fijos de emergencia. El observador se enlaza automáticamente desde el directorio
modules que ya utiliza el proyecto.

PublicFormPage conserva styles.page, Field, Button, títulos, textos y colores.
Añade scroll de foco y de feedback local, keyboardShouldPersistTaps=handled y
keyboardDismissMode=on-drag. El manifiesto existente mantiene adjustResize.
El formulario de recuperación que comparte Access recibe el mismo contenedor;
ResetPassword y las pantallas privadas no se modificaron.

## Pruebas

- Navegación por gestos y por tres botones, insets laterales y recorte superior.
- Padre ya protegido, teclado superpuesto, resize completo/parcial y cierre de teclado.
- Eventos incompletos o no finitos y dimensiones todavía no medidas al arrancar.
- Campo enfocado visible al abrir teclado o cambiar foco.
- Error local desplazado a la vista en registro y login, con cero llamadas Auth.
- Regresiones existentes de bienvenida, fotos, voz, gastos, avisos y transporte HTTP.

Son 13 pruebas nuevas; se sustituyó la prueba antigua de la reserva fija de bienvenida
por una de medidas reales. Los componentes nativos se simulan en Node; la compilación
y la revisión física acreditan la integración con Android, no las simulaciones por sí solas.

Compilación debug arm64: **BUILD SUCCESSFUL en 3m53s, 290 tareas**.
APK: .verification/form-insets/fuga-plus-public-insets-debug.apk, 49.607.018 bytes.
SHA-256: `2ba22846db1439b9ad3e2d841b9f41b1f428e78021a720aa105c252676c43999`.
Se verificó presencia de FugaWindowInsets en DEX, cero archivos dotenv y cero
patrones de claves privadas en el artefacto. La compilación recibió solo configuración
ficticia en memoria; no leyó valores de .env.local.

Captura pública inicial del contenedor medido: .verification/form-insets/welcome-native.png.
Pantalla física 1280×2772; scroll entre y=152 e y=2720, medido por el dispositivo.
La revisión de teclado, campos y error de cada formulario fue confirmada por la
propietaria; no se conservaron contraseñas, volcados de texto ni capturas del teclado.

## Reproducir la revisión

El APK anterior a esta corrección no contiene el observador: se necesita el debug
nuevo, ya instalado en el teléfono de QA. Expo Go no incorpora este módulo local.
Para otra compilación se conserva el procedimiento de ANDROID_LOCAL.md y se incluyen
las fuentes modules/fuga-window-insets en la copia corta; no hay prebuild automático
ni cambios permanentes en herramientas del sistema durante esta tarea.

```powershell
node mobile/scripts/welcome-preview.cjs
.tools/android-sdk/platform-tools/adb.exe reverse tcp:8081 tcp:8085
```

Reabrir FUGA+. La configuración ficticia usa un namespace Auth distinto: no requiere
cerrar la sesión real, borrar datos ni cambiar dotenv. No introducir datos personales
ni intentar acceder con credenciales en este modo.

1. Crear cuenta: enfocar Confirmar contraseña, comprobar scroll, Registrarse y Volver.
2. Con campos vacíos, pulsar Registrarse: el error de correo es validación local.
3. Volver e iniciar sesión: enfocar Contraseña, revisar botones y error con campos vacíos.
4. Cerrar el teclado y revisar que los espacios se restauran correctamente.

Ambos recorridos fueron confirmados. Quedan como pruebas adicionales en otros
dispositivos TalkBack, fuente ampliada física, pantalla dividida y navegación por
tres botones; los casos geométricos correspondientes sí están cubiertos en Node.

## Archivos

- src/components/PublicSafeArea.tsx — marco público compartido.
- src/components/PublicFormPage.tsx — scroll, foco y mensajes.
- src/components/WindowInsetsProbe.tsx y WindowInsetsProbe.android.tsx — adaptador por plataforma.
- src/lib/publicInsets.ts — cálculo comprobable de obstrucciones reales.
- modules/fuga-window-insets/ — package/config, Gradle, manifiesto vacío y observador Kotlin.
- src/screens/Access.tsx y src/components/Welcome.tsx — sustitución de contenedores.
- tests/public-form-insets.test.cjs y tests/welcome.test.cjs — regresiones.
- docs/BIENVENIDA_VISUAL.md y este documento — actualización de alcance.

Evidencias locales: .verification/form-insets/artifact.json y evidence.json.
Sin instalaciones de dependencias, operaciones remotas, migraciones, commits,
pushes o despliegues.

Referencias: [edge-to-edge e insets de Android](https://developer.android.com/develop/ui/views/layout/edge-to-edge)
y [vistas nativas con Expo Modules](https://docs.expo.dev/modules/native-view-tutorial/).
