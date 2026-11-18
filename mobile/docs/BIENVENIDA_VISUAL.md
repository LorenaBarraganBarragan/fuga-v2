# Revisión visual de bienvenida — FUGA+

2026-11-18, America/Bogota. Alcance: presentación pública de bienvenida.

Actualización posterior de formularios: bienvenida y acceso ahora reutilizan
PublicSafeArea con WindowInsets reales de Android, sustituyendo la reserva inferior
fija del primer rediseño. Suite actual: 114 pruebas frontend y TypeScript aprobados.
El nuevo APK debug ya está instalado. Ver [áreas seguras de formularios](AREAS_SEGURAS_FORMULARIOS.md).

Se revisaron primero ui.tsx, Access.tsx, App.tsx, las pantallas existentes y el
logo original. No existía un rediseño guardado al retomar la tarea interrumpida.

## Identidad conservada

| Uso | HEX existente | Fuente |
|---|---|---|
| Verde principal | #1A5B5A | components/ui.tsx, colors.primary |
| Aguamarina | #A2E8D3 | components/ui.tsx, colors.secondary |
| Amarillo | #F5A623 | components/ui.tsx, colors.tertiary |
| Texto y texto secundario | #243332 / #5A6E6C | components/ui.tsx |
| Fondo y bordes | #F7FAF9 / #D7E3E0 | components/ui.tsx |
| Fondos complementarios | #D8F6EC / #EEF5F3 / #fff | ui.tsx y Dashboard.tsx |

Se reutilizan assets/branding/logo.png y Plus Jakarta Sans. Los iconos de voz,
gráfico, patrón y privacidad se construyen con View y bordes nativos: sin emojis,
fuentes de iconos, SVG ni dependencias nuevas. No se introduce morado.
Los estilos nuevos están encapsulados en Welcome.tsx; ui.tsx y los colores de
las demás pantallas permanecen intactos.

## Composición

- Logo, nombre y mensaje «Descubre a dónde se va tu dinero».
- Tarjeta verde de ejemplo, barras decorativas y posible patrón de cafés repetidos.
- Datos expresamente ficticios: seis gastos por COP 75.000; cuatro cafés de
  COP 5.000 suman COP 20.000. Los otros dos importes ilustrativos son 15.000 y 40.000,
  representados por las dos barras mayores. No se consulta ni crea ningún gasto.
- Botón principal Crear cuenta y secundario Iniciar sesión, con los callbacks ya
  existentes de Access. Registro, inicio y recuperación mantienen sus formularios.
- Tres beneficios: voz/texto, visualización de gastos y posibles fugas.
- Explicación de privacidad, confirmación del usuario y reglas automáticas sin IA generativa.

Botones de al menos 52 dp, etiquetas e indicaciones para lectores de pantalla,
iconos/gráfico decorativos excluidos de TalkBack, texto escalable sin truncamiento,
contenido desplazable y marco superior/inferior reservado fuera del scroll para Android.
En el teléfono se detectó que StatusBar podía informar altura cero durante el arranque;
se añadió inicialmente una reserva y actualización de la altura nativa después del layout,
además de iconos oscuros sobre el fondo claro. No se modificó App.tsx ni las pantallas privadas.
La actualización posterior citada arriba reemplaza esa reserva por medidas de las
barras, el recorte y el teclado, sin márgenes específicos de un modelo.
Los beneficios
se apilan con ancho inferior a 360 dp o fuente ampliada. En pantallas grandes el
contenido se centra y limita a 480 dp. No hay alturas fijas en bloques de texto.

## Verificación automatizada

`npm test`: **101 aprobadas, cero fallos y cero omitidas**.
`npm run typecheck`: aprobado.

Cuatro pruebas nuevas verifican los callbacks originales hacia registro/inicio/
recuperación sin llamadas Auth, el contenido accesible en 320 dp con fuente al
200 %, la exclusión de configuración real/privada en el launcher visual y la
reserva del marco seguro cuando Android comunica altura cero antes del primer layout.
La prueba de fuente ampliada comprueba la estructura de componentes; no sustituye
una revisión física con TalkBack o la fuente del sistema ampliada.

Chrome con perfil vacío y emulación de viewport exacto: anchos 320 y 393 px;
documentElement.scrollWidth coincide con innerWidth en ambos, sin desbordamiento
horizontal. Capturas inspeccionadas en .verification/welcome/web-exact-320.png y
web-exact-393.png. No son capturas nativas Android ni una prueba de autenticación.

## Android: vista previa aislada

No es necesario cerrar sesión ni borrar datos. El launcher usa configuración
ficticia en memoria: otro namespace de almacenamiento Auth y una API local sin
servicio. No lee dotenv, no hereda credenciales y no utiliza Supabase real.
La aplicación y su navegación son las existentes; únicamente cambia la
configuración del proceso de revisión. No enviar formularios ni introducir datos.

```powershell
# Desde la raíz; dependencias y APK debug ya preparados en las pruebas anteriores.
node mobile/scripts/welcome-preview.cjs
.tools/android-sdk/platform-tools/adb.exe reverse tcp:8081 tcp:8085
```

Reabrir el APK debug instalado. Requiere PC, Metro y USB activos; no es despliegue,
APK nuevo ni cambio de .env.local. La sesión real conserva su almacenamiento.

Recorrido disponible para revisión, sin enviar formularios:

1. Revisar logo, colores, jerarquía, tarjeta marcada Ejemplo ficticio y ambos botones.
2. Desplazar para ver los tres beneficios y la explicación de privacidad.
3. Abrir Crear cuenta y volver; abrir Iniciar sesión y volver, sin enviar formularios.
4. Comprobar que no haya recortes junto a la cámara, barra de estado o navegación.

La propietaria desbloqueó el Android y dejó FUGA+ abierta. Se capturó únicamente
la bienvenida pública del APK, a 1280×2772 píxeles. La primera captura permitió
detectar y corregir la superposición de las barras del sistema. Se conserva en
.verification/welcome/android-review.png la captura nativa de revisión. El viewport
del scroll se verificó entre y=152 e y=2616 en una pantalla de 1280×2772: el contenido
queda fuera de las barras del sistema. La propietaria abrió la vista previa y no
solicitó ajustes adicionales para esta pantalla. No se presupone una confirmación
manual de los formularios: su recorrido está cubierto por pruebas automatizadas.
Evidencia técnica local: .verification/welcome/evidence.json.

Para regresar posteriormente al QA de fotografías, sin modificar cuentas:

```powershell
.tools/android-sdk/platform-tools/adb.exe reverse tcp:8081 tcp:8084
```

Reabrir el APK con ese Metro activo. No cambiar el reverse mientras se revisa
la bienvenida. No se detuvieron ni modificaron los backend o bases de QA previos.

## Archivos de esta tarea

- src/components/Welcome.tsx: presentación nueva, sin servicios ni estado de usuario.
- src/screens/Access.tsx: conexión visual a los mismos callbacks; lógica Auth intacta.
- scripts/welcome-preview.cjs: configuración ficticia para revisar sin cerrar sesión.
- tests/welcome.test.cjs: regresiones de navegación, accesibilidad e aislamiento.
- docs/BIENVENIDA_VISUAL.md: instrucciones y alcance de la evidencia.

Se conserva el trabajo anterior del repositorio. Sin instalaciones, cambios en
backend/esquema, migraciones, escrituras remotas, commits, pushes ni despliegues.
