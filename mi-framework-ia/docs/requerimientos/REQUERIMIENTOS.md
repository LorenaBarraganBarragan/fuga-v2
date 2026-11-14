# FUGA+ — Requerimientos funcionales y no funcionales priorizados

**Versión:** 3.0 — línea base definitiva de especificación · **Fecha:** 2026-11-13

**Estado:** ESPECIFICACIÓN DOCUMENTAL DEFINITIVA. Decisiones D-01 a D-15 cerradas y aplicables según el alcance de cada prioridad; la implementación y sus pruebas se realizan posteriormente.

**Tecnologías vigentes para conciliación:** Supabase Auth, PostgreSQL en Supabase, FastAPI, React Native/TypeScript. Toda referencia heredada a JWT emitido por backend, MongoDB o servicios sustituidos requiere corrección y no constituye decisión vigente.

## Control de línea base definitiva (versión 3.0)

- Este documento es la especificación final de producto y aceptación; se conserva la numeración y priorización original.
- Las decisiones de diseño D-01 a D-15 se fijan en el apartado **Especificación definitiva de decisiones de producto y arquitectura** de este mismo archivo.
- Stack: React Native/TypeScript, FastAPI/Python, Supabase PostgreSQL y Supabase Auth. Sin MongoDB, JWT propio, Redis, Docker ni IA generativa externa como dependencia del MVP.
- Must Have define el MVP; Should/Could son ampliaciones especificadas; Won’t no se implementa en esta versión.
- Una especificación completa no constituye evidencia de que la aplicación esté implementada o de que un proveedor externo esté configurado.

## Matriz de prioridades

| Prioridad | RF | MVP |
|---|---|---|
| Must Have | RF-001, RF-002, RF-004, RF-010, RF-011, RF-012, RF-013, RF-014, RF-020, RF-021, RF-023, RF-024, RF-033 | Sí |
| Should Have | RF-003, RF-005, RF-007, RF-008, RF-015, RF-016, RF-030, RF-031, RF-032 | No |
| Could Have | RF-006, RF-009, RF-017, RF-018, RF-019, RF-022, RF-025, RF-026, RF-027 | No |
| Won't Have (for now) | RF-028, RF-029 | No |

## Requerimientos funcionales

### RF-001 — Consultar información pública y acceder al registro o al inicio de sesión

**Identificador:** RF-001 · **Historia de origen:** HU-01 · **Prioridad:** Must Have · **MVP:** Sí

**Descripción:** El Visitante puede consultar una pantalla pública con la propuesta de valor de FUGA+ y acceder al registro o al inicio de sesión; las rutas privadas no son accesibles sin una sesión válida.

**Justificación:** Es la entrada al producto y el primer paso para identificar al Usuario y asociar sus gastos a una cuenta.

**Criterios de aceptación:**
- El Visitante ve el propósito de la aplicación y acciones visibles para registrarse o iniciar sesión.
- Al intentar abrir una ruta privada sin sesión, el sistema redirige al inicio de sesión y no muestra datos privados.
- El contenido público no incluye gastos, estadísticas privadas ni información de cuentas.

**Dependencias:** Ninguna.

### RF-002 — Registrarse e iniciar sesión con correo y contraseña

**Identificador:** RF-002 · **Historia de origen:** HU-02 · **Prioridad:** Must Have · **MVP:** Sí

**Descripción:** Un Visitante puede crear una cuenta con correo y contraseña e iniciar sesión; Supabase Auth gestiona la autenticación y la sesión. FastAPI verifica los tokens de acceso y aplica las autorizaciones correspondientes según el rol del usuario.

**Justificación:** La identidad es la base de la propiedad de los gastos, la autorización y la privacidad. Sin registro e inicio de sesión no existe cuenta a la que asociar datos.

**Criterios de aceptación:**
- Un registro con datos válidos crea una cuenta con rol **Usuario** y nunca con rol **Administrador** por defecto.
- Un correo ya registrado, un dato inválido o una contraseña que no cumple la política aprobada se rechazan con un mensaje claro y sin detalles internos.
- Un inicio de sesión válido establece una sesión gestionada por Supabase Auth; credenciales incorrectas o una cuenta inactiva se rechazan con un mensaje que no revela si el correo existe.
- La contraseña no se almacena en texto plano ni se devuelve en ninguna respuesta.

**Dependencias:** RF-001; decisión D-09 (política de contraseñas y sesión).

### RF-003 — Iniciar sesión con una cuenta de Google

**Identificador:** RF-003 · **Historia de origen:** HU-03 · **Prioridad:** Should Have · **MVP:** No

**Descripción:** Un Visitante puede iniciar sesión con una cuenta de Google; Supabase Auth gestiona el flujo OAuth con Google y crea o vincula la identidad según la regla aprobada; FastAPI verifica el token de acceso emitido por Supabase Auth y aplica la autorización por rol, sin confiar en datos de identidad suministrados por el cliente.

**Justificación:** Es un canal de acceso cómodo, pero el MVP puede operar con correo y contraseña. Depende de configuración OAuth y de una regla segura de vinculación.

**Criterios de aceptación:**
- Un flujo OAuth válido gestionado por Supabase Auth permite crear o vincular la cuenta conforme a D-10 y establece una sesión de Supabase Auth.
- Un flujo OAuth o token de acceso inválido, vencido o destinado a otro cliente se rechaza; FastAPI no acepta tokens de Google como sustituto del token de acceso de Supabase Auth.
- Un correo que ya pertenece a una cuenta local se trata según D-10 y no permite tomar el control de la cuenta sin verificación.
- La cuenta creada por Google recibe el rol **Usuario**, salvo provisión administrativa explícita.

**Dependencias:** RF-002; configuración OAuth; decisión D-10.

### RF-004 — Cerrar sesión de forma segura

**Identificador:** RF-004 · **Historia de origen:** HU-04 · **Prioridad:** Must Have · **MVP:** Sí

**Descripción:** Un Usuario autenticado puede cerrar su sesión; la aplicación elimina los datos de sesión locales y el backend invalida o revoca la sesión según la política aprobada.

**Justificación:** El cierre de sesión es parte del ciclo de seguridad y protege el acceso en dispositivos compartidos.

**Criterios de aceptación:**
- Al cerrar sesión, el token local se elimina y las pantallas privadas dejan de ser accesibles.
- El backend rechaza el uso posterior del token cuando la política de revocación lo exige.
- Cerrar sesión dos veces o hacerlo con una sesión ya vencida no produce un error bloqueante ni expone información.
- Después del cierre, el Usuario es dirigido a una pantalla pública o al inicio de sesión.

**Dependencias:** RF-002; decisión D-09.

### RF-005 — Recuperar el acceso mediante restablecimiento de contraseña

**Identificador:** RF-005 · **Historia de origen:** HU-05 · **Prioridad:** Should Have · **MVP:** No

**Descripción:** Un Usuario puede solicitar el restablecimiento de su contraseña y definir una nueva mediante un enlace o código de un solo uso, con vigencia limitada y sin revelar si el correo está registrado.

**Justificación:** Es importante para la continuidad de la cuenta, pero requiere correo transaccional y configuración adicional que no son necesarios para demostrar el flujo principal.

**Criterios de aceptación:**
- La solicitud devuelve siempre un mensaje genérico, exista o no el correo, y no confirma la existencia de la cuenta.
- El token o código de recuperación es de un solo uso, tiene vigencia limitada según D-09 y se invalida al completar el cambio.
- Una contraseña nueva que no cumple la política aprobada se rechaza; una válida permite iniciar sesión y no requiere conocer la anterior.
- Un token vencido, usado o inválido se rechaza con un mensaje claro y una opción para solicitar otro.

**Dependencias:** RF-002; proveedor de correo; decisión D-09.

### RF-006 — Desactivar la propia cuenta de usuario

**Identificador:** RF-006 · **Historia de origen:** HU-06 · **Prioridad:** Could Have · **MVP:** No

**Descripción:** Un Usuario puede desactivar su propia cuenta tras una confirmación explícita; la cuenta deja de permitir el inicio de sesión y sus sesiones activas se invalidan según la política aprobada.

**Justificación:** Mejora el control del Usuario sobre su cuenta, pero no es necesario para el flujo principal y depende de una política de retención y reactivación aún no definida.

**Criterios de aceptación:**
- La desactivación exige una confirmación explícita y solo puede aplicarse a la cuenta del Usuario autenticado.
- Después de desactivar, la cuenta no puede iniciar sesión y las sesiones activas se invalidan o quedan sujetas a la política D-09.
- Los datos se conservan o eliminan según D-06; no se eliminan de forma irreversible sin una política aprobada.
- Un Usuario no puede desactivar la cuenta de otra persona mediante esta función.

**Dependencias:** RF-002, RF-004; decisión D-06.

### RF-007 — Consultar y editar nombres y teléfono del perfil

**Identificador:** RF-007 · **Historia de origen:** HU-07 · **Prioridad:** Should Have · **MVP:** No

**Descripción:** Un Usuario autenticado puede consultar y editar su nombre, apellido y teléfono; el backend valida los campos y solo permite modificar el perfil propio.

**Justificación:** Mejora la identificación y la experiencia, pero el MVP puede operar con un perfil mínimo creado a partir de la cuenta.

**Criterios de aceptación:**
- El Usuario ve únicamente su propio perfil y puede editar los campos permitidos.
- Los campos obligatorios, formatos y longitudes se validan según D-13; un valor inválido se rechaza sin guardar parcialmente.
- Un intento de consultar o editar el perfil de otra cuenta se rechaza con 403 o 404 sin devolver datos.
- Los cambios se reflejan en la siguiente consulta del perfil.

**Dependencias:** RF-002; decisión D-13.

### RF-008 — Cambiar la foto de perfil

**Identificador:** RF-008 · **Historia de origen:** HU-08 · **Prioridad:** Should Have · **MVP:** No

**Descripción:** Un Usuario autenticado puede cargar o sustituir su foto de perfil mediante Cloudinary; el sistema valida el archivo, protege las credenciales y conserva la imagen anterior si la operación falla.

**Justificación:** Es una mejora de perfil, no una función central del registro de gastos, y requiere configuración y pruebas de un servicio externo.

**Criterios de aceptación:**
- Solo un Usuario autenticado puede cargar o cambiar su propia foto.
- El sistema acepta únicamente tipos y tamaños de archivo permitidos según D-13 y rechaza archivos inválidos con un mensaje claro.
- Las credenciales de Cloudinary no se exponen en el cliente; la carga se realiza mediante el mecanismo seguro aprobado.
- Si la carga o sustitución falla, la foto anterior se conserva o el perfil queda sin foto, sin un estado parcial inconsistente.
- La imagen se asocia al perfil correcto y no permite modificar la foto de otra cuenta.

**Dependencias:** RF-007; Cloudinary; decisión D-13.

### RF-009 — Usar la foto de perfil de Google cuando esté disponible

**Identificador:** RF-009 · **Historia de origen:** HU-09 · **Prioridad:** Could Have · **MVP:** No

**Descripción:** Cuando el Usuario inicia sesión con Google y no tiene una foto propia, el sistema puede usar la foto de su perfil de Google según la regla de precedencia aprobada; si no está disponible o el Usuario no lo autoriza, se mantiene la alternativa definida.

**Justificación:** Mejora la experiencia de perfil, pero depende de Google, de la carga de imágenes y de una regla de precedencia que aún no está cerrada.

**Criterios de aceptación:**
- La foto de Google solo se usa cuando la cuenta tiene una identidad de Google verificada y la regla D-13 lo permite.
- Una foto cargada manualmente no se reemplaza por la de Google sin consentimiento o sin la precedencia aprobada.
- Si la foto de Google no está disponible, el perfil conserva una imagen alternativa o queda sin foto, sin errores bloqueantes.
- La imagen se asocia únicamente a la cuenta autenticada.

**Dependencias:** RF-003, RF-007, RF-008; decisión D-13.

### RF-010 — Registrar un gasto escrito en lenguaje natural

**Identificador:** RF-010 · **Historia de origen:** HU-10 · **Prioridad:** Must Have · **MVP:** Sí

**Descripción:** Un Usuario autenticado puede escribir una frase en lenguaje natural para describir un gasto; la aplicación conserva el texto como borrador editable y no lo guarda como gasto hasta que se complete la revisión y la confirmación.

**Justificación:** Es el canal principal de entrada y el punto de partida del flujo de valor. Sin texto no hay interpretación, revisión ni análisis.

**Criterios de aceptación:**
- El Usuario autenticado accede a la entrada de texto y puede escribir una frase con el contenido de un gasto.
- Un texto vacío, compuesto solo por espacios o que supera el límite aprobado se rechaza con un mensaje claro antes de procesar.
- El texto se conserva como borrador y no crea un gasto por sí solo.
- Si el Usuario abandona la pantalla, no se guarda un gasto parcial; el tratamiento del borrador se rige por D-05.
- Un Visitante o una sesión vencida no puede acceder a esta función.

**Dependencias:** RF-002; decisión D-05.

### RF-011 — Procesar el gasto con «Procesar con IA» y reglas deterministas

**Identificador:** RF-011 · **Historia de origen:** HU-11 · **Prioridad:** Must Have · **MVP:** Sí

**Descripción:** Al pulsar el botón cuya etiqueta visible es exactamente «Procesar con IA», el backend interpreta el texto con un diccionario propio y reglas deterministas versionadas, y devuelve un borrador con monto, categoría, descripción, fecha cuando se reconozca y el texto original, sin usar una API externa de IA.

**Justificación:** Convierte el texto libre en datos utilizables y es el núcleo diferencial del producto. Debe ser reproducible, explicable y verificable.

**Criterios de aceptación:**
- El botón visible se denomina «Procesar con IA» y, al pulsarlo, se ejecuta el procesamiento en el backend.
- La respuesta incluye monto, categoría, descripción, fecha reconocida cuando exista y el texto original, sin guardar todavía el gasto.
- El mismo texto, con la misma versión de diccionario y reglas, produce un resultado equivalente y no realiza llamadas a APIs externas de IA.
- Si no se reconoce el monto, se informa el problema y se habilita la corrección manual; no se permite guardar con un monto inválido.
- Si la categoría es desconocida o ambigua, se aplica la regla aprobada de D-02 o se deja el campo para selección del Usuario.
- Si el procesamiento falla o supera el tiempo de espera, el texto se conserva, se muestra una opción de reintento y no se crea un gasto parcial.

**Dependencias:** RF-010; diccionario y reglas deterministas; decisiones D-02, D-03, D-04 y D-05.

### RF-012 — Revisar y corregir los campos interpretados antes de guardar

**Identificador:** RF-012 · **Historia de origen:** HU-12 · **Prioridad:** Must Have · **MVP:** Sí

**Descripción:** Antes de guardar, el Usuario ve el texto original y todos los campos interpretados, puede corregirlos y debe confirmar explícitamente el guardado; el backend repite las validaciones y no acepta valores inválidos aunque el cliente los envíe.

**Justificación:** La revisión obligatoria protege la calidad de los datos y es una expectativa explícita del Usuario. Ningún gasto debe guardarse de forma automática.

**Criterios de aceptación:**
- La vista de revisión muestra texto original, monto, categoría, descripción, fecha y moneda cuando corresponda.
- El Usuario puede corregir los campos permitidos y el texto original permanece inmutable.
- Un monto vacío, cero, negativo o no numérico, una categoría fuera del catálogo, una descripción inválida o una fecha inválida bloquean el guardado con un error por campo.
- El guardado solo ocurre tras una confirmación explícita; descartar la revisión no crea ningún gasto.
- Un Usuario no puede abrir ni modificar el borrador de otra cuenta mediante un identificador ajeno.
- Las validaciones se aplican en la interfaz y se repiten en el backend con datos manipulados.

**Dependencias:** RF-011; decisiones D-02, D-03, D-04 y D-05.

### RF-013 — Guardar el gasto bajo la cuenta del propietario y aislarlo de otros usuarios

**Identificador:** RF-013 · **Historia de origen:** HU-13 · **Prioridad:** Must Have · **MVP:** Sí

**Descripción:** Al confirmar un gasto válido, el backend lo persiste con el propietario derivado del token verificado, de forma atómica e idempotente, y garantiza que ninguna otra cuenta pueda consultarlo, editarlo o eliminarlo.

**Justificación:** Sin persistencia no hay historial, estadísticas ni fugas. La propiedad y el aislamiento son condiciones de privacidad y confianza.

**Criterios de aceptación:**
- Un gasto válido se guarda con el propietario de la sesión y devuelve un identificador único.
- Un identificador de propietario enviado por el cliente se ignora o se rechaza; nunca se guarda a nombre de otra cuenta.
- Un reintento con la misma clave de idempotencia no crea un gasto duplicado y devuelve el resultado de la operación ya realizada.
- Un fallo de escritura no deja un gasto parcial y permite reintentar.
- Un Usuario B que conoce el identificador de un gasto del Usuario A recibe 403 o 404 sin datos del gasto.
- Una sesión vencida produce 401 y no permite guardar.

**Dependencias:** RF-012, RF-033; decisión D-06 para retención.

### RF-014 — Consultar el historial de gastos del más reciente al más antiguo

**Identificador:** RF-014 · **Historia de origen:** HU-14 · **Prioridad:** Must Have · **MVP:** Sí

**Descripción:** Un Usuario autenticado puede consultar una lista paginada de sus gastos, ordenada de forma descendente por fecha del gasto y, en caso de empate, por fecha de creación, con acceso al detalle de cada gasto propio.

**Justificación:** Es la forma básica de comprobar que un gasto quedó guardado y de consultar la información acumulada. Sin historial, el registro no tiene utilidad visible.

**Criterios de aceptación:**
- La lista muestra solo gastos del propietario autenticado, con monto, categoría, descripción y fecha.
- El orden es descendente por fecha del gasto y usa la fecha de creación como desempate.
- La paginación no produce duplicados ni omisiones y permite llegar hasta el gasto más antiguo.
- Sin gastos, se muestra un estado vacío con una acción para registrar el primero, sin mensajes de error.
- Un error de red o de servidor muestra un mensaje y una opción de reintento sin borrar los datos ya cargados.
- Al abrir un gasto ajeno por identificador, se rechaza el acceso sin devolver datos.
- Un gasto eliminado mediante RF-016 deja de aparecer en el historial.

**Dependencias:** RF-013; decisiones D-04 y D-05.

### RF-015 — Filtrar el historial por fecha y categoría

**Identificador:** RF-015 · **Historia de origen:** HU-15 · **Prioridad:** Should Have · **MVP:** No

**Descripción:** Un Usuario autenticado puede filtrar su historial por rango de fechas y por categoría, aplicando ambos filtros de forma combinada y manteniendo el aislamiento por propietario.

**Justificación:** Mejora la consulta cuando hay muchos gastos, pero el historial completo es suficiente para el MVP.

**Criterios de aceptación:**
- Los filtros de fecha y categoría se pueden usar juntos y el resultado cumple ambas condiciones.
- Una fecha inválida, un rango invertido o una categoría fuera del catálogo se rechazan con un mensaje claro.
- Sin coincidencias, se muestra un estado vacío comprensible y una acción para limpiar los filtros.
- El filtrado se ejecuta en el backend sobre los gastos del propietario y no descarga gastos de otras cuentas.
- Limpiar los filtros restaura la lista completa del historial.

**Dependencias:** RF-014; decisiones D-02 y D-04.

### RF-016 — Editar y eliminar gastos guardados, actualizando análisis y resúmenes

**Identificador:** RF-016 · **Historia de origen:** HU-16 · **Prioridad:** Should Have · **MVP:** No

**Descripción:** Un Usuario autenticado puede editar o eliminar un gasto propio ya guardado; toda edición o eliminación actualiza el historial, los totales, las categorías y las posibles fugas afectadas, sin dejar resultados obsoletos.

**Justificación:** Es importante para corregir errores posteriores al guardado y mantener la confianza en los análisis, pero el MVP puede operar con la revisión previa y se beneficia de un tiempo adicional para probar la coherencia de los agregados.

**Criterios de aceptación:**
- Solo el propietario puede editar o eliminar su gasto; un identificador ajeno se rechaza con 403 o 404 sin datos.
- La edición aplica las mismas validaciones de RF-012 y persiste los valores corregidos.
- Al editar o eliminar, el historial, los totales, el desglose por categoría y las fugas afectadas se recalculan o invalidan de forma que no se muestren resultados obsoletos.
- Un gasto eliminado deja de aparecer en el historial y en la evidencia de fugas.
- Una eliminación repetida o concurrente no produce un estado inconsistente.
- La operación no deja agregados obsoletos: si el recálculo falla, se invalida la caché o se reintenta antes de mostrar resultados; el gasto y sus análisis no quedan permanentemente desincronizados.

**Dependencias:** RF-013, RF-014, RF-020, RF-021, RF-023; RNF-006.

### RF-017 — Iniciar la grabación de voz para un gasto en Android

**Identificador:** RF-017 · **Historia de origen:** HU-17 · **Prioridad:** Could Have · **MVP:** No

**Descripción:** En Android, un Usuario autenticado puede iniciar y detener una grabación de voz para describir un gasto, después de conceder el permiso de micrófono; la aplicación no conserva el audio como gasto ni como dato permanente.

**Justificación:** La voz es un canal alternativo valioso, pero el texto cubre el MVP y el módulo nativo requiere compilación y pruebas específicas.

**Criterios de aceptación:**
- La función solo se muestra en Android y requiere una sesión válida.
- Sin permiso de micrófono, se explica la situación y se ofrece el flujo de texto sin bloquear la aplicación.
- El Usuario puede iniciar y detener la grabación, y el estado de la interfaz refleja claramente si está escuchando.
- Al cancelar, no se crea ningún gasto ni se conserva el audio.
- El audio no se envía a un servicio externo no aprobado ni se almacena como archivo permanente.

**Dependencias:** RF-002, RF-010; compilación Android con permiso de micrófono; decisión D-12.

### RF-018 — Convertir la voz en texto con Kotlin y `SpeechRecognizer`

**Identificador:** RF-018 · **Historia de origen:** HU-18 · **Prioridad:** Could Have · **MVP:** No

**Descripción:** La aplicación obtiene una transcripción del audio mediante un módulo nativo de Android que utiliza `SpeechRecognizer` y entrega el texto al flujo de procesamiento, sin que el Usuario tenga que escribir la frase de nuevo.

**Justificación:** Es la implementación técnica acordada para la voz, pero no es necesaria para el MVP y depende de un puente Kotlin/React Native y de pruebas en dispositivos reales.

**Criterios de aceptación:**
- Una grabación válida produce una transcripción visible y editable en la aplicación.
- Si no se reconoce voz, el micrófono está ocupado o se produce un error del reconocedor, se muestra un mensaje y se ofrece reintentar o usar texto.
- La transcripción no se guarda como gasto hasta completar el procesamiento, la revisión y la confirmación.
- Solo existe una sesión de reconocimiento activa a la vez.
- El idioma y la variante se configuran según D-12.

**Dependencias:** RF-017; módulo Kotlin y `SpeechRecognizer`; compilación de desarrollo o EAS; decisión D-12.

### RF-019 — Revisar la transcripción y los campos antes de guardar un gasto por voz

**Identificador:** RF-019 · **Historia de origen:** HU-19 · **Prioridad:** Could Have · **MVP:** No

**Descripción:** Después de la transcripción, el Usuario puede revisar el texto reconocido, procesarlo con las mismas reglas deterministas, corregir los campos y confirmar el guardado; la voz no guarda un gasto de forma automática.

**Justificación:** La revisión obligatoria debe aplicarse también al canal de voz para mantener la calidad y la confianza en los datos.

**Criterios de aceptación:**
- La transcripción se muestra antes del procesamiento y puede corregirse.
- El procesamiento de la transcripción usa RF-011, con la etiqueta «Procesar con IA» y las mismas reglas deterministas.
- La revisión y el guardado usan RF-012 y RF-013, sin guardado automático.
- Cancelar o descartar en cualquier paso no crea un gasto.
- Un error de reconocimiento o de procesamiento conserva la transcripción y permite corregir o usar texto.

**Dependencias:** RF-011, RF-012, RF-017, RF-018.

### RF-020 — Consultar total, cantidad y promedio de gasto por periodo

**Identificador:** RF-020 · **Historia de origen:** HU-20 · **Prioridad:** Must Have · **MVP:** Sí

**Descripción:** Un Usuario autenticado puede consultar, para el periodo seleccionado, el total gastado, la cantidad de gastos y el promedio por gasto, calculados solo con sus registros y actualizados cuando cambian sus gastos.

**Justificación:** Es la primera lectura analítica del producto y permite entender el comportamiento de gasto sin revisar cada registro.

**Criterios de aceptación:**
- El panel de estadísticas muestra total, cantidad y promedio por gasto del periodo seleccionado.
- El promedio se calcula como total dividido entre la cantidad de gastos; con cantidad cero se muestra un estado sin datos, sin división por cero.
- Las cifras usan la moneda, decimales y redondeo aprobados en D-03.
- El periodo y la zona horaria se determinan según D-04.
- Al crear un gasto, las cifras se actualizan; si RF-016 está implementada, también se actualizan tras editar o eliminar.
- Un Usuario no ve cifras calculadas con gastos de otra cuenta.

**Dependencias:** RF-013; decisiones D-03 y D-04.

### RF-021 — Consultar el gasto por categoría e identificar la categoría de mayor gasto

**Identificador:** RF-021 · **Historia de origen:** HU-21 · **Prioridad:** Must Have · **MVP:** Sí

**Descripción:** Un Usuario autenticado puede consultar el total y la proporción de sus gastos por categoría en el periodo seleccionado, e identificar la categoría de mayor gasto; los empates y las categorías sin gasto se resuelven según la regla aprobada.

**Justificación:** El desglose por categoría explica en qué se concentra el gasto y complementa el total del panel de estadísticas.

**Criterios de aceptación:**
- El desglose incluye únicamente los gastos del propietario y usa el catálogo aprobado en D-02.
- La suma de todas las categorías, incluida «Otros» cuando exista, coincide con el total del periodo; ningún gasto se omite ni se cuenta dos veces.
- La categoría de mayor gasto se identifica correctamente; en caso de empate se aplica la regla D-02.
- Los porcentajes se calculan con el redondeo aprobado y no se generan porcentajes inválidos cuando el total es cero.
- Se muestra un estado sin datos cuando no hay gastos en el periodo.
- Al crear un gasto, el desglose se actualiza; si RF-016 está implementada, también tras editar o eliminar.

**Dependencias:** RF-013, RF-020; decisión D-02.

### RF-022 — Comparar el gasto entre periodos

**Identificador:** RF-022 · **Historia de origen:** HU-22 · **Prioridad:** Could Have · **MVP:** No

**Descripción:** Un Usuario autenticado puede comparar dos periodos y ver, para cada uno, total, cantidad y promedio, además de la diferencia absoluta y la variación porcentual cuando la base sea calculable.

**Justificación:** La comparación es ocasional y el periodo actual suele ser suficiente para el MVP; además añade cálculos y estados de borde.

**Criterios de aceptación:**
- Para dos periodos con datos, se muestran total, cantidad y promedio por gasto de cada uno, calculados solo con gastos del propietario.
- Si ambos periodos tienen total mayor que cero, se muestra la diferencia absoluta y la variación porcentual con la fórmula y el redondeo aprobados.
- Si el periodo base tiene total cero, se muestra la diferencia absoluta y se indica que el porcentaje no es calculable, sin división por cero.
- Si uno o ambos periodos no tienen gastos, se identifica claramente y no se inventan valores.
- Los periodos deben ser válidos y comparables según D-04.
- Al crear un gasto se actualiza la comparación; si RF-016 está implementada, también tras editar o eliminar.

**Dependencias:** RF-020, RF-021; decisiones D-03 y D-04.

### RF-023 — Detectar posibles fugas de dinero con reglas deterministas

**Identificador:** RF-023 · **Historia de origen:** HU-23 · **Prioridad:** Must Have · **MVP:** Sí

**Descripción:** El backend analiza los gastos vigentes del Usuario con un conjunto aprobado, explicable y versionado de reglas deterministas, y devuelve posibles patrones de repetición con evidencia suficiente, sin usar IA externa, aprendizaje automático ni predicciones.

**Justificación:** Es la propuesta de valor diferencial de FUGA+. Sin detección, la aplicación sería un registro de gastos más. Debe ser explicable y no inventar parámetros.

**Criterios de aceptación:**
- Una regla aprobada y versionada que se cumple produce una posible fuga con identificador de regla, versión, patrón, ocurrencias, monto acumulado, ventana temporal y evidencia.
- Un conjunto de gastos que no cumple ninguna regla produce un estado de «sin posibles fugas» y no inventa candidatos.
- Si no se alcanza la condición mínima de datos aprobada, se informa que aún no hay datos suficientes y no se muestran candidatos.
- El mismo conjunto de gastos y la misma versión de reglas producen un resultado determinista y equivalente.
- La detección se ejecuta solo sobre gastos del propietario y no mezcla cuentas.
- Un Administrador no recibe fugas ni gastos individuales; solo accede a agregados según RF-030.
- La interfaz presenta el resultado como «posible fuga», explica la regla y no afirma que exista una pérdida real ni culpa al Usuario.
- Al crear un gasto, el análisis se actualiza; la actualización tras edición o eliminación se prueba cuando RF-016 esté implementada.

**Dependencias:** RF-013, RF-033; reglas y parámetros aprobados D-01.

### RF-024 — Consultar la evidencia de una posible fuga de dinero

**Identificador:** RF-024 · **Historia de origen:** HU-24 · **Prioridad:** Must Have · **MVP:** Sí

**Descripción:** Un Usuario autenticado puede abrir una posible fuga y ver la regla aplicada, su versión, las ocurrencias, el monto acumulado, el rango de fechas y los gastos propios que la activaron, con una suma coherente con el acumulado.

**Justificación:** Una detección sin evidencia no es confiable ni accionable. El Usuario debe entender por qué el sistema identificó la posible fuga.

**Criterios de aceptación:**
- El detalle muestra nombre o descripción de la regla, versión, ocurrencias, monto acumulado y rango de fechas.
- La lista de gastos de la evidencia muestra fecha, descripción y monto, y su suma coincide con el acumulado informado.
- Solo aparecen gastos del propietario; otra cuenta y un Administrador no pueden abrir la evidencia individual.
- Si un gasto de la evidencia se edita o elimina mediante RF-016, la evidencia, las ocurrencias y el acumulado se actualizan o la fuga se marca como no vigente.
- Una fuga que dejó de cumplir la regla no se muestra como vigente ni conserva datos obsoletos.
- El texto explica la regla en lenguaje comprensible y no presenta la fuga como pérdida confirmada ni como crítica a los hábitos del Usuario.

**Dependencias:** RF-014, RF-023; RF-016 solo para la actualización posterior a edición o eliminación, no para el MVP.

### RF-025 — Recibir alertas sobre posibles fugas de dinero

**Identificador:** RF-025 · **Historia de origen:** HU-25 · **Prioridad:** Could Have · **MVP:** No

**Descripción:** Un Usuario autenticado puede recibir alertas dentro de la aplicación y notificaciones del dispositivo mediante Expo Notifications cuando se detecte una posible fuga nueva. Las notificaciones locales se contemplan en el alcance opcional; el envío push remoto requiere verificar costos, credenciales, infraestructura, consentimiento y viabilidad antes de activarlo (D-11).

**Justificación:** Las alertas añaden comodidad, pero la posible fuga ya puede consultarse en la aplicación. El push requiere infraestructura, credenciales y decisiones de privacidad adicionales.

**Criterios de aceptación:**
- Una posible fuga nueva genera una alerta dentro de la aplicación con descripción breve, ocurrencias, monto acumulado y acceso a la evidencia.
- Si el Usuario concedió permiso, puede mostrarse una notificación local; si lo denegó, la alerta dentro de la aplicación sigue funcionando.
- Sin una posible fuga nueva no se muestra una alerta vacía ni se envía una notificación innecesaria.
- Una misma fuga no se repite de forma indiscriminada; el criterio de novedad y recordatorio se define en D-11.
- Abrir la alerta lleva a la evidencia de RF-024 del propio Usuario.
- El contenido en pantalla bloqueada no expone montos, descripciones ni otros datos financieros sensibles.
- No se habilita el envío push remoto hasta aprobar D-11 y comprobar su viabilidad técnica y económica; Expo Notifications como biblioteca no implica que el envío remoto esté implementado.

**Dependencias:** RF-023, RF-024; decisión D-11.

### RF-026 — Consultar sugerencias prácticas sobre posibles fugas

**Identificador:** RF-026 · **Historia de origen:** HU-26 · **Prioridad:** Could Have · **MVP:** No

**Descripción:** Un Usuario autenticado puede consultar sugerencias prácticas asociadas a una posible fuga, provenientes de un catálogo revisado y aprobado, redactadas de forma neutral y sin constituir asesoría financiera.

**Justificación:** Las sugerencias mejoran la utilidad del análisis, pero requieren contenido revisado y no son necesarias para demostrar la detección y la evidencia.

**Criterios de aceptación:**
- Cada sugerencia está vinculada a una regla o tipo de fuga aprobado y proviene del catálogo revisado.
- El texto es informativo, no culpabilizante y no promete ahorro, rentabilidad ni resultados.
- No se generan sugerencias con IA ni se inventan recomendaciones fuera del catálogo.
- Si no existe una sugerencia aprobada para la regla, se muestra un mensaje neutro y no se improvisa contenido.
- Las sugerencias solo se muestran al propietario de la fuga.

**Dependencias:** RF-023, RF-024; catálogo de sugerencias aprobado.

### RF-027 — Consultar el resumen mensual de posibles fugas

**Identificador:** RF-027 · **Historia de origen:** HU-27 · **Prioridad:** Could Have · **MVP:** No

**Descripción:** Un Usuario autenticado puede consultar un resumen mensual de sus posibles fugas, con las ocurrencias y montos correspondientes al mes según la regla de asignación aprobada, sin duplicar gastos ni mezclar cuentas.

**Justificación:** El resumen mensual aporta una vista de tendencia, pero depende de definir la asignación mensual y no es necesario para el MVP.

**Criterios de aceptación:**
- El resumen incluye solo posibles fugas del propietario y el periodo mensual seleccionado.
- Cada gasto se asigna a un solo mes según D-01/D-04 y no se cuenta dos veces.
- La suma del resumen es coherente con las ocurrencias de las fugas incluidas.
- Un mes sin fugas muestra un estado vacío comprensible.
- El resumen no expone datos de otras cuentas ni se muestra a un Administrador.
- Los cambios en gastos actualizan el resumen cuando corresponde.

**Dependencias:** RF-023, RF-024; decisiones D-01 y D-04.

### RF-028 — Definir un límite mensual global de gasto

**Historia:** HU-28 · **Prioridad:** Won't Have (for now) · **MVP:** No

**Descripción:** El sistema deberá definir un límite mensual global de gasto conforme a las reglas aprobadas de HU-28.

**Especificación funcional:**

- Un único límite vigente por usuario y mes.
- El límite es global, sin separación por categorías ni metas de ahorro.
- Crear límites para el mes actual o futuros, nunca meses finalizados.
- Monto entero positivo en COP dentro del rango técnico.
- Modificar límites durante meses habilitados.
- Eliminar lógicamente con confirmación, sin afectar gastos.
- Conservar historial de cambios de monto.
- Considerar todos los gastos confirmados y no eliminados del mes, incluso anteriores al límite.
- Advertir si los gastos existentes exceden el monto, sin bloquear la operación.
- Validar y confirmar antes de guardar.
- Impedir límites vigentes duplicados; ofrecer modificar el existente.
- Permitir recreación después de eliminación lógica durante un mes habilitado.
- Usar tabla de límites y tabla de historial en PostgreSQL; verificar Supabase Auth desde FastAPI.
- Proteger propiedad, errores y reintentos sin duplicación.
- Cerrar automáticamente al finalizar el mes, preservando monto e historial.

**Verificación:** consultar CA-28.01 a CA-28.14 en `historias-usuario.md`.

### RF-029 — Consultar el avance del límite mensual de gasto

**Historia:** HU-29 · **Prioridad:** Won't Have (for now) · **MVP:** No

**Descripción:** El sistema deberá consultar el avance del límite mensual de gasto conforme a las reglas aprobadas de HU-29.

**Especificación funcional:**

- Mostrar seguimiento si existe límite no eliminado.
- Consultar mes actual y meses anteriores con límite.
- Mostrar límite, gastos, porcentaje y diferencia COP.
- Contar gastos confirmados no eliminados del mes.
- Calcular (total gastado / límite) × 100.
- Diferenciar dentro, alcanzado y superado.
- Mostrar porcentaje real superior a 100 %; barra visual limitada a 100 %.
- Actualizar al crear, editar o eliminar gastos.
- Actualizar tras modificación del límite.
- Mostrar estado vacío y acceso a configuración.
- Conservar límite histórico al cerrar mes.
- Mensajes neutrales sin juicios financieros.
- Solo datos del usuario autenticado.
- Calcular en FastAPI con PostgreSQL.
- Sin notificaciones automáticas.

**Verificación:** consultar CA-29.01 a CA-29.14 en `historias-usuario.md`.

### RF-030 — Consultar estadísticas agregadas de uso sin acceder a gastos individuales

**Historia:** HU-30 · **Prioridad:** Should Have · **MVP:** No

**Descripción:** El sistema deberá consultar estadísticas agregadas de uso sin acceder a gastos individuales conforme a las reglas aprobadas de HU-30.

**Especificación funcional:**

- Acceso exclusivo de administradores autorizados.
- Mostrar total de usuarios registrados.
- Mostrar cuentas activas e inactivas.
- Mostrar conteo global de gastos confirmados no eliminados.
- Mostrar usuarios con actividad mensual.
- Mostrar evolución mensual de usuarios con actividad.
- Consultar mes actual y anteriores.
- No mostrar gastos, descripciones, categorías ni importes personales.
- No permitir navegar a finanzas individuales.
- Aplicar agregación mínima según D-07.
- Consultas agregadas en FastAPI y PostgreSQL.
- Estados vacíos y errores seguros.
- Sin IA generativa ni analítica externa.
- Fuera del MVP inicial.

**Verificación:** consultar CA-30.01 a CA-30.14 en `historias-usuario.md`.

### RF-031 — Consultar usuarios registrados e información administrativa

**Historia:** HU-31 · **Prioridad:** Should Have · **MVP:** No

**Descripción:** El sistema deberá consultar usuarios registrados e información administrativa conforme a las reglas aprobadas de HU-31.

**Especificación funcional:**

- Acceso exclusivo de administradores autorizados.
- Listado paginado.
- Buscar por nombre o correo.
- Filtrar por estado activo/inactivo.
- Mostrar ID, nombre disponible, correo, rol, estado y fecha de registro.
- Vista de detalle con los mismos campos.
- No mostrar contraseñas, tokens ni credenciales.
- No mostrar datos financieros individuales.
- Solo consulta, sin modificación.
- FastAPI verifica identidad y rol.
- Paginación y límites de resultados.
- Estados vacíos y búsquedas sin coincidencia.
- Errores y denegaciones seguros.
- Sincronización con Supabase Auth y perfiles administrativos.

**Verificación:** consultar CA-31.01 a CA-31.14 en `historias-usuario.md`.

### RF-032 — Activar o desactivar cuentas de usuario

**Historia:** HU-32 · **Prioridad:** Should Have · **MVP:** No

**Descripción:** El sistema deberá activar o desactivar cuentas de usuario conforme a las reglas aprobadas de HU-32.

**Especificación funcional:**

- Solo administradores autorizados.
- Gestionar desde detalle de HU-31.
- Mostrar estado actual.
- Confirmar antes de cambiar.
- Desactivar sin borrar datos.
- Restringir acceso a funciones protegidas.
- FastAPI verifica estado en cada solicitud protegida.
- Bloquear sesiones previas y verificar revocación de Supabase Auth.
- Reactivar sujeto a autenticación.
- Impedir autodesactivación del administrador.
- Proteger cuentas administrativas con política específica.
- Auditar actor, cuenta, acción y fecha.
- Evitar duplicados y conflictos concurrentes.
- Mensajes claros.
- Sincronizar estado con Supabase Auth y FastAPI.
- No permitir acceso a gastos individuales.

**Verificación:** consultar CA-32.01 a CA-32.16 en `historias-usuario.md`.

### RF-033 — Proteger la privacidad de los gastos y garantizar el aislamiento entre usuarios

**Historia:** HU-33 · **Prioridad:** Must Have · **MVP:** Sí

**Descripción:** El sistema deberá proteger la privacidad de los gastos y garantizar el aislamiento entre usuarios conforme a las reglas aprobadas de HU-33.

**Especificación funcional:**

- Autenticación para datos financieros.
- FastAPI valida firma, vigencia y validez del token de Supabase Auth.
- Identidad derivada del token, no de un ID enviado por cliente.
- Cada recurso privado tiene propietario.
- Consultas limitadas al propietario.
- Prohibir editar/eliminar recursos ajenos.
- Aislamiento en categorías, estadísticas, fugas, recomendaciones y límites cuando existan.
- Administrador sin acceso a gastos individuales.
- Autorización en backend, no solo interfaz.
- Rechazar tokens inválidos, ausentes o vencidos.
- Restringir cuentas desactivadas cuando HU-32 exista.
- HTTPS y protección de secretos.
- Controles de PostgreSQL y RLS según arquitectura de conexión.
- Errores/logs sin secretos ni datos financieros.
- Limpiar datos privados al cerrar sesión o cambiar cuenta.
- Validar propiedad en operaciones individuales y masivas.
- Pruebas automatizadas de aislamiento.
- Protección transversal desde MVP.

**Verificación:** consultar CA-33.01 a CA-33.18 en `historias-usuario.md`.


## B. Requerimientos no funcionales priorizados

Los requerimientos no funcionales se derivan de las reglas de privacidad, seguridad, integridad y calidad del documento de historias. No se fijan umbrales numéricos que el proyecto no haya aprobado; cuando un valor es necesario, se indica la decisión pendiente.

### RNF-001 — Autorización obligatoria y aislamiento en el backend

**Identificador:** RNF-001 · **Prioridad:** Must Have · **Estado:** Confirmado

**Descripción:** Toda ruta que lea o modifique datos privados debe exigir una sesión válida, verificar el rol y comprobar la propiedad del recurso en el backend, con denegación por defecto.

**Justificación:** La privacidad no puede depender de la interfaz. Un fallo de autorización expone gastos y rompe la confianza en el producto.

**Criterio de aceptación o validación:**
- Cada ruta privada tiene una prueba que intenta acceder sin sesión, con sesión de otro Usuario y con rol insuficiente; todas deben ser rechazadas.
- Las rutas administrativas exigen rol **Administrador** y no permiten acceder a gastos individuales.
- La suite de seguridad se ejecuta en cada entrega y forma parte de la verificación del MVP.
- Una ruta nueva no se considera terminada si no tiene su prueba de autorización.

**Historias relacionadas:** HU-02, HU-13, HU-14, HU-16, HU-23, HU-24, HU-30 a HU-33.

### RNF-002 — Privacidad y minimización de datos

**Identificador:** RNF-002 · **Prioridad:** Must Have · **Estado:** Confirmado

**Descripción:** El sistema recopila y devuelve solo los datos necesarios para la función solicitada. Los gastos y su detalle se muestran únicamente a su propietario. El Administrador puede consultar estadísticas agregadas no identificables (RF-030) y datos administrativos mínimos de cuentas (RF-031), pero nunca gastos financieros individuales.

**Justificación:** El producto maneja información financiera personal. La minimización reduce la exposición y el impacto de un incidente.

**Criterio de aceptación o validación:**
- Las respuestas al Usuario no incluyen datos de otras cuentas.
- Las respuestas administrativas no incluyen gastos, descripciones, montos individuales, tokens ni contraseñas.
- Los agregados administrativos respetan el umbral mínimo aprobado en D-07 y no se expone un grupo pequeño.
- Los datos personales y financieros no se incluyen en notificaciones visibles en pantalla bloqueada.
- La política de retención y eliminación se documenta en D-06 antes de implementar operaciones destructivas.

**Historias relacionadas:** HU-08, HU-09, HU-13, HU-16, HU-24, HU-25, HU-30, HU-31, HU-33.

### RNF-003 — Protección de credenciales y sesiones

**Identificador:** RNF-003 · **Prioridad:** Must Have · **Estado:** Confirmado

**Descripción:** Las contraseñas se almacenan con un hash adaptativo aprobado y nunca en texto plano; los tokens se transmiten y almacenan de forma segura, tienen vigencia limitada y pueden revocarse según la política aprobada. La vigencia, renovación y revocación concretas están pendientes en D-09.

**Justificación:** Las credenciales son la llave de acceso a los gastos. Su protección es una condición de seguridad básica.

**Criterio de aceptación o validación:**
- Ninguna respuesta, log o base de datos contiene contraseñas en texto plano.
- Un token vencido, revocado o de una cuenta inactiva es rechazado por el backend.
- El cierre de sesión y la desactivación de cuenta invalidan la sesión según D-09.
- La política de vigencia, renovación, revocación y límites de intentos está documentada y probada.
- El almacenamiento local del token usa el mecanismo seguro de la plataforma.

**Historias relacionadas:** HU-02, HU-03, HU-04, HU-05, HU-06, HU-32, HU-33.

### RNF-004 — Validación y rechazo de entradas no confiables

**Identificador:** RNF-004 · **Prioridad:** Must Have · **Estado:** Confirmado

**Descripción:** El backend valida tipo, formato, longitud, rango y pertenencia al catálogo de todos los datos recibidos, y no confía en validaciones realizadas solo en el cliente.

**Justificación:** Los datos manipulados pueden corromper gastos, eludir reglas de negocio o provocar fallos de seguridad.

**Criterio de aceptación o validación:**
- Montos, fechas, categorías, identificadores y textos inválidos se rechazan con un código de error coherente.
- Una solicitud manipulada que omite la validación del cliente no se persiste.
- Los parámetros de consulta y paginación se validan antes de usarse.
- Las pruebas incluyen valores límite, tipos incorrectos y campos desconocidos.

**Historias relacionadas:** HU-02, HU-10, HU-11, HU-12, HU-13, HU-14, HU-15, HU-16, HU-18.

### RNF-005 — Integridad transaccional e idempotencia

**Identificador:** RNF-005 · **Prioridad:** Must Have · **Estado:** Confirmado

**Descripción:** Las operaciones que crean o modifican gastos se ejecutan de forma atómica y controlan los reintentos para no producir registros parciales ni duplicados.

**Justificación:** Un gasto duplicado o parcial altera el historial, los totales y las fugas, y es difícil de detectar por el Usuario.

**Criterio de aceptación o validación:**
- Un fallo durante el guardado no deja un gasto parcial.
- Dos solicitudes con la misma clave de idempotencia producen un solo gasto.
- Las pruebas cubren reintentos simultáneos y fallos de base de datos.
- Las operaciones que afectan varias tablas o filas de PostgreSQL preservan la integridad mediante transacciones y restricciones apropiadas; cualquier operación externa no transaccional requiere una estrategia de recuperación probada.

**Historias relacionadas:** HU-13, HU-16.

### RNF-006 — Coherencia de agregados y análisis tras cambios

**Identificador:** RNF-006 · **Prioridad:** Should Have · **Estado:** Confirmado

**Descripción:** Toda edición o eliminación de un gasto debe actualizar o invalidar el historial, los totales, el desglose por categoría, las comparaciones y las posibles fugas afectadas, sin mostrar resultados obsoletos.

**Justificación:** La utilidad del análisis depende de que las cifras correspondan a los gastos vigentes. Este requerimiento se activa cuando RF-016 esté implementada.

**Criterio de aceptación o validación:**
- Después de editar un gasto, el total, la categoría y la evidencia de fuga reflejan el valor nuevo.
- Después de eliminar un gasto, este desaparece del historial y de los agregados.
- Las pruebas comparan los valores antes y después de la operación.
- No se muestran cachés obsoletos después del cambio.

**Historias relacionadas:** HU-16, HU-20, HU-21, HU-22, HU-23, HU-24, HU-27, HU-29.

### RNF-007 — Registro seguro y ausencia de datos sensibles en logs

**Identificador:** RNF-007 · **Prioridad:** Must Have · **Estado:** Confirmado

**Descripción:** Los logs de aplicación y de error no incluyen contraseñas, tokens, montos, descripciones de gastos ni otros datos personales o financieros identificables.

**Justificación:** Los logs suelen tener menor protección que la base de datos y pueden convertirse en una fuga secundaria.

**Criterio de aceptación o validación:**
- Una revisión de los logs de una ejecución de prueba no encuentra tokens, contraseñas, montos ni descripciones.
- Los errores se registran con un identificador de correlación y un mensaje técnico sin datos sensibles.
- El acceso a los logs está restringido.
- Las pruebas de seguridad incluyen una comprobación de logs después de un fallo.

**Historias relacionadas:** HU-02, HU-13, HU-32, HU-33.

### RNF-008 — Transporte cifrado y manejo seguro de secretos

**Identificador:** RNF-008 · **Prioridad:** Must Have · **Estado:** Confirmado

**Descripción:** Todo el tráfico entre la aplicación y el backend en producción usa HTTPS/TLS, y las credenciales de servicios externos se almacenan fuera del cliente y del repositorio.

**Justificación:** El texto y los tokens no deben viajar en claro. Las credenciales de Cloudinary, Google o base de datos no pueden quedar expuestas en la aplicación.

**Criterio de aceptación o validación:**
- Las URL de producción del backend y de los servicios externos usan HTTPS.
- Las claves y secretos se cargan desde variables de entorno o un gestor de secretos, no desde el código ni el repositorio.
- El cliente no contiene secretos de Cloudinary ni de base de datos.
- La configuración de producción se revisa antes de la entrega.

**Historias relacionadas:** HU-02, HU-03, HU-08, HU-33.

### RNF-009 — Usabilidad del flujo de revisión y de los estados de error

**Identificador:** RNF-009 · **Prioridad:** Must Have · **Estado:** Confirmado

**Descripción:** El flujo principal se puede completar sin documentación externa, la revisión antes de guardar es explícita y los estados vacíos, de carga y de error ofrecen información comprensible y una acción útil.

**Justificación:** La revisión obligatoria solo protege los datos si el Usuario entiende qué está corrigiendo. Los errores ambiguos generan pérdida de confianza.

**Criterio de aceptación o validación:**
- Un Usuario nuevo completa registro, carga de texto, revisión y guardado sin ayuda externa en una prueba guiada.
- Cada error de validación se muestra junto al campo correspondiente y explica cómo corregirlo.
- Los estados vacíos, de carga y de fallo tienen un mensaje claro y, cuando aplica, una acción de reintento.
- La interfaz está en español y no usa lenguaje que culpe al Usuario por sus gastos.
- La confirmación de guardado es explícita y el descarte advierte si hay cambios sin guardar.

**Historias relacionadas:** HU-01, HU-02, HU-10, HU-11, HU-12, HU-14, HU-20, HU-21, HU-23, HU-24.

### RNF-010 — Transparencia de la etiqueta «Procesar con IA»

**Identificador:** RNF-010 · **Prioridad:** Must Have · **Estado:** Pendiente de definición (D-15)

**Descripción:** La interfaz conserva la etiqueta «Procesar con IA», pero explica de forma clara que el procesamiento se realiza con un diccionario y reglas deterministas, sin una API externa de IA, para no generar expectativas engañosas.

**Justificación:** La etiqueta es una decisión del proyecto, pero su transparencia afecta la confianza y la comprensión del Usuario.

**Criterio de aceptación o validación:**
- El botón muestra exactamente «Procesar con IA».
- Existe un texto de ayuda o aviso aprobado que explica el procesamiento determinista y la ausencia de una API externa.
- El texto no afirma que existe un modelo de IA generativa ni oculta cómo se obtiene el resultado.
- La redacción final se aprueba en D-15 antes de considerar terminado el criterio.

**Historias relacionadas:** HU-01, HU-11, HU-33.

### RNF-011 — Compatibilidad de plataformas y límites de Expo

**Identificador:** RNF-011 · **Prioridad:** Must Have · **Estado:** Confirmado

**Descripción:** El flujo principal funciona en Android e iOS con React Native y TypeScript; la entrada por voz se limita a Android y requiere una compilación con el módulo nativo Kotlin, por lo que no se promete su funcionamiento en Expo Go.

**Justificación:** El producto es móvil y debe operar en las plataformas objetivo. La voz tiene una restricción técnica conocida que debe comunicarse y probarse.

**Criterio de aceptación o validación:**
- El flujo de texto, revisión, historial y panel de estadísticas funciona en Android e iOS.
- La voz solo se ofrece en Android y muestra una alternativa de texto en las demás plataformas.
- La compilación con el módulo nativo se prueba en un dispositivo o emulador Android compatible.
- La documentación indica que Expo Go no soporta el módulo nativo de voz.
- Las dependencias de Expo Notifications y Cloudinary se prueban en el entorno de desarrollo acordado.

**Historias relacionadas:** HU-01, HU-08, HU-10, HU-17, HU-18, HU-19, HU-25.

### RNF-012 — Fiabilidad, recuperación y ausencia de estados parciales

**Identificador:** RNF-012 · **Prioridad:** Must Have · **Estado:** Confirmado

**Descripción:** Ante errores de red, fallos del backend o interrupciones, la aplicación conserva el texto o la transcripción cuando sea posible, informa el problema y permite reintentar sin crear gastos parciales ni perder datos ya confirmados.

**Justificación:** La red móvil es inestable y el Usuario no debe perder lo que escribió ni quedar con datos inconsistentes.

**Criterio de aceptación o validación:**
- Un fallo de red durante el procesamiento conserva el texto y ofrece reintento.
- Un fallo durante el guardado no crea un gasto parcial ni un duplicado.
- Los datos ya cargados en el historial no se borran por un error de una página siguiente.
- Los estados de error distinguen entre falta de sesión, error de validación y fallo temporal.
- Las pruebas simulan pérdida de conexión y respuestas 5xx.

**Historias relacionadas:** HU-10, HU-11, HU-12, HU-13, HU-14, HU-18, HU-19.

### RNF-013 — Rendimiento y capacidad bajo condiciones representativas

**Identificador:** RNF-013 · **Prioridad:** Should Have · **Estado:** Pendiente de definición; umbrales no aprobados

**Descripción:** El sistema debe responder en tiempos y volúmenes adecuados para el uso previsto, pero los umbrales numéricos de latencia, tamaño de página, concurrencia y volumen de gastos aún no están definidos.

**Justificación:** Un rendimiento deficiente afecta la usabilidad y la detección de fugas, pero no se deben inventar cifras de aceptación.

**Criterio de aceptación o validación:**
- Antes de la entrega se aprueban y documentan los umbrales de latencia, volumen y concurrencia.
- Se ejecutan pruebas con un conjunto de datos representativo del tamaño acordado.
- La paginación evita cargar todos los gastos en una sola respuesta.
- El análisis de fugas se limita al propietario y no recorre datos de todas las cuentas.
- Los resultados de las pruebas se registran y se comparan con los umbrales aprobados.

**Historias relacionadas:** HU-11, HU-14, HU-20, HU-21, HU-23, HU-30.

### RNF-014 — Mantenibilidad, versionado y pruebas automatizadas

**Identificador:** RNF-014 · **Prioridad:** Must Have · **Estado:** Confirmado

**Descripción:** El diccionario, las reglas de fugas y los contratos de la API están versionados; los criterios de aceptación y las pruebas de seguridad se automatizan para permitir cambios controlados durante las 12 semanas.

**Justificación:** El desarrollo asistido por IA acelera la escritura, pero exige revisión y pruebas repetibles para evitar regresiones y reglas inconsistentes.

**Criterio de aceptación o validación:**
- Cada regla de fuga y cada versión del diccionario tienen identificador y fecha de vigencia.
- Las pruebas de aceptación de las historias Must se ejecutan de forma automatizada o reproducible.
- La suite de seguridad de RNF-001 se ejecuta en cada entrega.
- Los cambios de contrato se revisan y no rompen a los consumidores sin una decisión explícita.
- El código generado con IA pasa por revisión humana antes de integrarse.

**Historias relacionadas:** HU-11, HU-23, HU-24, HU-33; todas las historias.

### RNF-015 — Auditabilidad de acciones administrativas

**Identificador:** RNF-015 · **Prioridad:** Should Have · **Estado:** Pendiente de definición (D-14)

**Descripción:** Las acciones administrativas sensibles, como activar o desactivar una cuenta, deben quedar registradas con el actor, la fecha, la cuenta afectada y el motivo cuando la política lo exija, y el acceso a ese registro debe estar restringido.

**Justificación:** La auditoría permite investigar incidentes y evita cambios administrativos sin trazabilidad, pero depende de la política de administración aún pendiente.

**Criterio de aceptación o validación:**
- Cada activación o desactivación administrativa genera un registro con actor, fecha y cuenta afectada.
- El motivo se registra cuando D-14 lo hace obligatorio.
- Solo personal autorizado puede consultar el registro de auditoría.
- El registro no contiene gastos, descripciones, montos ni tokens.
- La retención del registro se define en D-14/D-06.

**Historias relacionadas:** HU-31, HU-32, HU-33.

### RNF-016 — Retención, desactivación y eliminación de datos

**Identificador:** RNF-016 · **Prioridad:** Must Have · **Estado:** Pendiente de definición (D-06)

**Descripción:** El sistema debe aplicar una política aprobada de retención, desactivación y eliminación de cuentas y gastos, sin borrar datos de forma irreversible ni conservarlos indefinidamente sin justificación.

**Justificación:** La privacidad exige saber durante cuánto tiempo se conservan los datos y qué ocurre al desactivar o eliminar una cuenta. No se debe implementar una política inventada.

**Criterio de aceptación o validación:**
- La política D-06 define qué se conserva, durante cuánto tiempo, qué se elimina y cómo se gestionan los respaldos.
- Ninguna operación de borrado irreversible se expone antes de aprobar la política.
- La desactivación de cuenta impide el acceso y aplica la retención aprobada.
- Las pruebas verifican que los datos no se conservan más allá de lo definido y que los respaldos siguen la misma política.
- La política es comprensible para el Usuario y se refleja en los avisos correspondientes.

**Historias relacionadas:** HU-06, HU-13, HU-16, HU-29, HU-32, HU-33.


## Trazabilidad y coherencia de la línea base

- Cada RF-XXX corresponde a HU-XX y conserva su prioridad y alcance.
- Las RNF se aplican transversalmente a las historias afectadas.
- Los parámetros de producto, autenticación, privacidad, fechas, fugas y notificaciones se encuentran **cerrados** en D-01 a D-15.
- La validación de proveedores y las pruebas funcionales se ejecutarán durante implementación; no son decisiones de producto abiertas.


## Especificación definitiva de decisiones de producto y arquitectura

**Estado:** decisiones D-01 a D-15 cerradas para la línea base documental 3.0. Son decisiones de diseño del proyecto, no afirmaciones de que los servicios externos estén configurados ni de que las funciones estén implementadas.

### D-01 — Detección de posibles fugas
- **Regla FUGA-01, versión 1.0:** analizar los últimos **30 días calendario**, incluido el día de consulta, usando la zona horaria `America/Bogota`. Agrupar por **categoría y descripción normalizada** (minúsculas, espacios compactados, sin tildes, equivalencias explícitas del diccionario). No agrupar únicamente por categoría, para evitar falsos positivos.
- Generar un candidato si existen **al menos 3 gastos** del mismo grupo en **3 fechas distintas** de la ventana, cada uno de valor **entre COP 1.000 y COP 30.000**, y la suma del grupo es **al menos COP 15.000**. La categoría «Otros» se admite cuando la descripción normalizada es informativa; las descripciones vacías o genéricas («gasto», «compra», «otro») no activan esta regla.
- Cada resultado expone regla y versión, categoría, descripción normalizada, número de gastos, fechas, total exacto y los identificadores de gastos que sustentan la evidencia. No se presentan predicciones, culpabilidad, ahorros garantizados ni resultados sin evidencia.
- Calcular **bajo demanda** al consultar fugas y después de confirmar un gasto si la pantalla de fugas está abierta; no se requieren trabajos programados. Sin gastos: estado vacío; con menos de tres ocurrencias elegibles: «datos insuficientes para identificar patrones». El mismo conjunto de datos produce el mismo resultado.
- Los umbrales son **parámetros configurables versionados**, pero estos valores constituyen la configuración inicial obligatoria; cualquier cambio futuro requiere nueva versión de regla y pruebas de regresión.

### D-02 — Categorías y clasificación
- Catálogo inicial cerrado: **Alimentación, Transporte, Vivienda, Servicios, Educación, Salud, Entretenimiento, Compras y Otros**. «Otros» es categoría válida y **siempre se incluye** en totales, estadísticas y filtros.
- El diccionario determinista propone categoría cuando hay coincidencia inequívoca; ante ausencia de coincidencia asigna «Otros» y permite corrección manual antes de confirmar. Si dos reglas tienen igual precedencia, prevalece la coincidencia de frase más larga y, si persiste el empate, «Otros» con revisión manual.
- Para categorías empatadas en el máximo, mostrar **todas las categorías empatadas** ordenadas alfabéticamente; nunca escoger una sin indicarlo.

### D-03 — Moneda, montos y cálculos
- El MVP maneja **únicamente pesos colombianos (COP)**, sin conversión de divisas. Montos **enteros positivos** desde **COP 1** hasta **COP 100.000.000** por gasto. El separador de miles es visual y no se almacena; se rechazan centavos, valores negativos, cero y monedas diferentes.
- Persistir montos como entero (`BIGINT` o tipo equivalente con restricción); sumar enteros en backend/base de datos, sin punto flotante. Mostrar formato local `es-CO`, con símbolo `$` y aclaración COP cuando sea necesario.
- Porcentajes comparativos: calcular con valores exactos, mostrar **un decimal** y redondeo convencional; si el periodo base es cero, mostrar «sin base de comparación», no infinito.

### D-04 — Fechas, periodos y zona horaria
- Zona horaria funcional **`America/Bogota`**. Fecha del gasto en formato ISO `YYYY-MM-DD`, sin hora obligatoria. Si no se reconoce una fecha en el texto, proponer la fecha actual local y permitir corrección antes de guardar.
- Admitir fechas desde **2020-01-01** hasta **la fecha actual local**; no registrar gastos futuros. El historial ordena por `fecha_gasto DESC, created_at DESC, id DESC`, para desempate estable.
- Dashboard inicial: **mes calendario actual**, del primer al último día local; permitir elegir otros meses desde enero de 2020. Comparación opcional: mes seleccionado frente al mes inmediatamente anterior. Rangos inclusivos en fechas y consultas SQL con límites temporales explícitos.
- Una fuga se atribuye a la ventana móvil de 30 días en la que se calcula; para resúmenes mensuales opcionales se contabilizan **solo los gastos cuya fecha cae dentro del mes**, sin duplicar gastos entre categorías.

### D-05 — Procesamiento, límites e idempotencia
- «**Procesar con IA**» es el **nombre de interfaz**, acompañado de la explicación visible «Interpretación automática mediante reglas; no utiliza IA generativa». No se invoca una API externa de IA.
- Entrada de texto: **1 a 280 caracteres** tras recortar espacios. Diccionario versionado, reglas con prioridad fija y pruebas de frases de ejemplo; extraer monto, fecha, descripción y categoría propuesta. Si faltan monto o datos esenciales, exigir corrección; **jamás guardar sin confirmación explícita**.
- La descripción final tiene **1 a 120 caracteres**; el usuario puede modificar todos los campos interpretados. No persistir borradores incompletos en el servidor; el borrador se mantiene solo en memoria de la pantalla y se descarta al abandonarla.
- Confirmación de gasto con clave de idempotencia UUID por intento; conservarla **24 horas**. Misma clave y mismo contenido devuelven el mismo resultado; misma clave con contenido distinto produce **409 Conflict**.

### D-06 — Eliminación, desactivación y conservación
- En el MVP no se ofrece eliminar la cuenta ni gastos (HU-06 y HU-16 no son Must). Cuando se implementen, la eliminación de gastos será **lógica**, con `deleted_at`, y excluirá de inmediato esos registros de historial, dashboard y fugas.
- Desactivar una cuenta: marcar `disabled_at`, impedir operaciones privadas mediante validación en backend y solicitar revocación de sesiones al proveedor cuando esté disponible. La denegación por estado de cuenta **no depende únicamente de que expire el token**.
- Los datos de una cuenta desactivada se conservan durante **30 días** para recuperación administrativa y después se programan para supresión conforme a las obligaciones legales aplicables; no prometer borrado irreversible de copias de seguridad antes de sus ciclos de retención. Para un prototipo académico sin usuarios reales, emplear datos de prueba.
- No conservar transcripciones de voz ni texto original del gasto más allá de los campos confirmados, salvo que el usuario lo incorpore voluntariamente a la descripción final.

### D-07 — Privacidad de estadísticas administrativas
- Administrador: puede consultar **metadatos mínimos de cuentas** necesarios para HU-31/HU-32, pero **no gastos individuales, descripciones, evidencias de fugas ni totales identificables por persona**.
- Los agregados financieros administrativos solo se muestran cuando el grupo contiene **al menos 10 usuarios distintos**; grupos menores se suprimen. No permitir filtros combinables que revelen grupos pequeños ni exponer identificadores en la respuesta.

### D-08 — Roles y autorización
- Roles **Visitante, Usuario y Administrador**. La identidad la verifica Supabase Auth; FastAPI valida firma, emisor, audiencia, expiración y estado de cuenta, y aplica autorización por rol y propietario **en cada solicitud protegida**.
- El rol administrativo se asigna **solo por un mecanismo de aprovisionamiento seguro**, nunca por un campo editable del registro. Un Administrador no obtiene acceso a gastos de usuarios aunque conozca su identificador.
- Para acceso directo a Supabase desde el cliente, activar y probar **Row Level Security (RLS)**; si el backend usa credenciales privilegiadas, filtrar explícitamente por el usuario autenticado y no exponer dichas credenciales al móvil.

### D-09 — Registro, contraseñas, sesiones y recuperación
- Autenticación administrada por **Supabase Auth**, sin emitir JWT propios en FastAPI. Registro con correo válido y contraseña de **mínimo 8 caracteres**; confirmación de correo activada cuando el proveedor de correo del proyecto esté configurado.
- Sesión gestionada por SDK de Supabase con renovación segura de tokens; el backend rechaza tokens inválidos o expirados. Al cerrar sesión se elimina la sesión local y se solicita cierre en Supabase. No prometer revocación instantánea de tokens de acceso ya emitidos; el backend consulta el estado deshabilitado de la cuenta para bloquear solicitudes.
- Recuperación mediante **enlace de restablecimiento enviado por Supabase Auth**, con caducidad y un solo uso conforme a la configuración real del proveedor; no inventar una duración independiente ni construir un sistema de tokens propio. Si el correo saliente no está configurado, mostrar una indisponibilidad explícita en vez de simular un envío.

### D-10 — Google OAuth
- Inicio con Google mediante **proveedor OAuth de Supabase Auth**, solo cuando credenciales, URI de redirección y consentimiento estén configurados. Nunca unir dos cuentas basándose exclusivamente en coincidencia de correo: exigir la vinculación autenticada/verificada que soporte el proveedor.
- Google es **Should Have**, no dependencia del registro por correo del MVP. Si falla OAuth, conservar el acceso por correo y mostrar error recuperable.

### D-11 — Alertas y notificaciones
- HU-25 es **Could Have**. La aplicación puede mostrar alertas **internas** basadas en FUGA-01; **Expo Notifications** se adopta para notificaciones **locales** opcionales con permiso del sistema operativo.
- **No se incluye push remoto en la línea base**: no se requiere servidor de envío, token push ni servicio de terceros para cumplir HU-25. La decisión evita asumir precios o cuotas no verificados. Cualquier ampliación a push remoto será cambio de alcance documentado.
- Máximo **una alerta local por candidato y versión de regla en 7 días**, sin notificaciones entre **21:00 y 08:00** hora local. Texto genérico: «FUGA+ encontró un patrón de gastos para revisar»; sin importes ni descripciones en pantalla bloqueada. Si se deniega el permiso, la alerta interna sigue disponible.

### D-12 — Voz
- Captura de voz opcional para Android mediante **Kotlin `SpeechRecognizer`**, idioma preferido `es-CO`, con alternativa `es` cuando esté disponible. Máximo **30 segundos** por captura y **280 caracteres** de transcripción editable.
- Solicitar permiso de micrófono en contexto; nunca grabar ni guardar archivos de audio en FUGA+. Mostrar aviso de que el servicio de reconocimiento del dispositivo **puede procesar audio mediante servicios externos** según su configuración. Si el permiso o el reconocimiento no están disponibles, ofrecer entrada por texto sin bloquear el flujo.

### D-13 — Perfil e imágenes
- Nombres: **2 a 80 caracteres**; teléfono colombiano opcional de **10 dígitos**, sin tratarlo como identificador de autenticación.
- Foto de perfil opcional: JPEG/PNG/WebP, máximo **5 MB**, subida a **Cloudinary** mediante firma o endpoint controlado por backend; nunca exponer secretos de Cloudinary en el cliente. La foto de Google puede utilizarse como sugerencia inicial si el usuario lo permite, y una foto cargada manualmente tiene precedencia.

### D-14 — Auditoría
- Registrar eventos administrativos de **consulta de listado, cambio de estado de cuenta y fallo de autorización** con fecha UTC, actor, acción, resultado y cuenta objetivo cuando proceda; **sin gastos, contraseñas, tokens ni contenido financiero**. Retener registros de auditoría **90 días** en el prototipo y restringir acceso a responsables autorizados.
- No exigir auditoría avanzada de edición de gastos en el MVP; cuando HU-16 exista, registrar identificador, actor y fecha del cambio sin duplicar descripciones sensibles.

### D-15 — Transparencia y lenguaje
- Mantener literalmente el botón **«Procesar con IA»** por decisión de producto, pero añadir junto al flujo la aclaración «Interpretación mediante reglas automáticas; no utiliza IA generativa ni envía tu gasto a una IA externa».
- Usar «**posible fuga**», «patrón detectado» y «revisar»; evitar «derroche», «error financiero», promesas de ahorro o diagnósticos personales.
- Las explicaciones de fugas deben mostrar regla, intervalo, número de ocurrencias y gastos de soporte; el usuario decide cómo interpretar el hallazgo.

### Política de cambios
Esta línea base define **qué debe construirse**. Las historias Should/Could y las Won't quedan documentadas para evolución, pero **no son obligaciones del MVP**. Cambios de umbrales, proveedores, costos, reglas de privacidad o alcance requieren nueva versión documental y actualización simultánea de RF/HU. Las pruebas de aceptación y las verificaciones de configuración externa son actividades de implementación, no decisiones documentales pendientes.

## Matriz explícita de trazabilidad HU ↔ RF

La correspondencia por identificador y alcance constituye la trazabilidad definitiva de la especificación; la implementación se valida mediante pruebas. Las RNF son transversales y se relacionan en sus apartados.

| Historia | Requerimiento | Prioridad | MVP |
|---|---|---|---|
| HU-01 | RF-001 | Must Have | Sí |
| HU-02 | RF-002 | Must Have | Sí |
| HU-03 | RF-003 | Should Have | No |
| HU-04 | RF-004 | Must Have | Sí |
| HU-05 | RF-005 | Should Have | No |
| HU-06 | RF-006 | Could Have | No |
| HU-07 | RF-007 | Should Have | No |
| HU-08 | RF-008 | Should Have | No |
| HU-09 | RF-009 | Could Have | No |
| HU-10 | RF-010 | Must Have | Sí |
| HU-11 | RF-011 | Must Have | Sí |
| HU-12 | RF-012 | Must Have | Sí |
| HU-13 | RF-013 | Must Have | Sí |
| HU-14 | RF-014 | Must Have | Sí |
| HU-15 | RF-015 | Should Have | No |
| HU-16 | RF-016 | Should Have | No |
| HU-17 | RF-017 | Could Have | No |
| HU-18 | RF-018 | Could Have | No |
| HU-19 | RF-019 | Could Have | No |
| HU-20 | RF-020 | Must Have | Sí |
| HU-21 | RF-021 | Must Have | Sí |
| HU-22 | RF-022 | Could Have | No |
| HU-23 | RF-023 | Must Have | Sí |
| HU-24 | RF-024 | Must Have | Sí |
| HU-25 | RF-025 | Could Have | No |
| HU-26 | RF-026 | Could Have | No |
| HU-27 | RF-027 | Could Have | No |
| HU-28 | RF-028 | Won't Have (for now) | No |
| HU-29 | RF-029 | Won't Have (for now) | No |
| HU-30 | RF-030 | Should Have | No |
| HU-31 | RF-031 | Should Have | No |
| HU-32 | RF-032 | Should Have | No |
| HU-33 | RF-033 | Must Have | Sí |

## Verificaciones de implementación posteriores a la especificación

1. Verificar mediante pruebas los parámetros ya fijados en D-01, D-02, D-03, D-04 y D-09.
2. Probar autorización por propietario y rol con Supabase Auth, FastAPI y políticas de acceso PostgreSQL; no asumir que la documentación demuestra aislamiento efectivo.
3. Probar las notificaciones locales definidas en D-11; el push remoto está excluido de esta línea base.
4. Verificar el cumplimiento de las políticas cerradas D-06, D-07, D-10, D-14 y D-15 cuando se implementen sus historias.
5. Ejecutar las pruebas de aceptación de cada HU y registrar evidencia; no confundir revisión documental con validación funcional.
