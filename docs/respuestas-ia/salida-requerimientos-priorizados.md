# Requerimientos funcionales y no funcionales priorizados de FUGA+

## A. Requerimientos funcionales priorizados

**Fuente principal:** `docs/respuestas-ia/salida-historias-usuario.md` (33 historias revisadas y priorizadas). Se mantiene una relación uno a uno entre historia y requerimiento funcional para evitar duplicidad y conservar la trazabilidad. Las historias HU-16 y HU-25 agrupan más de una operación, pero se mantienen en un solo requerimiento porque comparten objetivo, prioridad y alcance.

**Convenciones:** los umbrales, montos, frecuencias, ventanas, monedas, categorías y políticas no definidas se remiten a las decisiones D-xx de la sección E. No se inventan valores numéricos ni reglas de negocio.

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

**Descripción:** Un Visitante puede crear una cuenta con correo y contraseña e iniciar sesión; el backend valida las credenciales, aplica la política de contraseñas aprobada y emite una sesión JWT con el rol correspondiente.

**Justificación:** La identidad es la base de la propiedad de los gastos, la autorización y la privacidad. Sin registro e inicio de sesión no existe cuenta a la que asociar datos.

**Criterios de aceptación:**
- Un registro con datos válidos crea una cuenta con rol **Usuario** y nunca con rol **Administrador** por defecto.
- Un correo ya registrado, un dato inválido o una contraseña que no cumple la política aprobada se rechazan con un mensaje claro y sin detalles internos.
- Un inicio de sesión válido devuelve un JWT utilizable; credenciales incorrectas o una cuenta inactiva se rechazan con un mensaje que no revela si el correo existe.
- La contraseña no se almacena en texto plano ni se devuelve en ninguna respuesta.

**Dependencias:** RF-001; decisión D-09 (política de contraseñas y sesión).

### RF-003 — Iniciar sesión con una cuenta de Google

**Identificador:** RF-003 · **Historia de origen:** HU-03 · **Prioridad:** Should Have · **MVP:** No

**Descripción:** Un Visitante puede iniciar sesión con una cuenta de Google; el backend verifica el token de identidad y crea o vincula la cuenta según la regla aprobada, sin aceptar datos de identidad enviados sin verificar.

**Justificación:** Es un canal de acceso cómodo, pero el MVP puede operar con correo y contraseña. Depende de configuración OAuth y de una regla segura de vinculación.

**Criterios de aceptación:**
- Un token de Google válido permite crear o vincular la cuenta y devuelve una sesión JWT.
- Un token inválido, vencido o de otro cliente se rechaza sin crear ni vincular cuentas.
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
- El total de las categorías coincide con el total del periodo, salvo la categoría «Otros» si el catálogo la define.
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

**Descripción:** Un Usuario autenticado puede recibir alertas dentro de la aplicación y, como máximo, notificaciones locales cuando se detecte una posible fuga nueva; las notificaciones push remotas quedan postergadas y no forman parte de este requerimiento.

**Justificación:** Las alertas añaden comodidad, pero la posible fuga ya puede consultarse en la aplicación. El push requiere infraestructura, credenciales y decisiones de privacidad adicionales.

**Criterios de aceptación:**
- Una posible fuga nueva genera una alerta dentro de la aplicación con descripción breve, ocurrencias, monto acumulado y acceso a la evidencia.
- Si el Usuario concedió permiso, puede mostrarse una notificación local; si lo denegó, la alerta dentro de la aplicación sigue funcionando.
- Sin una posible fuga nueva no se muestra una alerta vacía ni se envía una notificación innecesaria.
- Una misma fuga no se repite de forma indiscriminada; el criterio de novedad y recordatorio se define en D-11.
- Abrir la alerta lleva a la evidencia de RF-024 del propio Usuario.
- El contenido en pantalla bloqueada no expone montos, descripciones ni otros datos financieros sensibles.
- No se envían notificaciones push remotas en el alcance actual.

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

### RF-028 — Definir una meta mensual de gasto o ahorro con alcance explícito

**Identificador:** RF-028 · **Historia de origen:** HU-28 · **Prioridad:** Won't Have (por ahora) · **MVP:** No

**Descripción:** Un Usuario autenticado podría definir una meta mensual de gasto o de ahorro, siempre que el tipo, el periodo, los gastos incluidos y la fuente de datos para medir el avance estén definidos y aprobados.

**Justificación:** El alcance de la meta aún es ambiguo y una meta de ahorro requiere ingresos o una base de cálculo que el producto no tiene definida. Se posterga para no inventar una regla de negocio.

**Criterios de aceptación:**
- Una meta solo se guarda si el tipo —gasto o ahorro—, el periodo y los gastos incluidos están definidos según D-08.
- Si se elige una meta de ahorro y no existe una fuente de datos aprobada, el sistema no permite guardarla y explica el motivo.
- Una meta de gasto se valida contra los límites y la moneda aprobados en D-03.
- Solo el propietario puede crear, consultar o modificar su meta.
- No se generan metas automáticas ni valores por defecto no aprobados.

**Dependencias:** RF-002, RF-013; decisión D-08.

### RF-029 — Consultar el avance hacia la meta definida

**Identificador:** RF-029 · **Historia de origen:** HU-29 · **Prioridad:** Won't Have (por ahora) · **MVP:** No

**Descripción:** Un Usuario autenticado podría consultar el avance de su meta mensual a partir de los gastos vigentes y de la fuente de datos definida para la meta, sin generar recomendaciones ni predicciones.

**Justificación:** Depende de RF-028 y de una definición completa de la meta. No se incluye hasta que esa definición exista.

**Criterios de aceptación:**
- El avance se calcula con la meta y el periodo definidos, usando gastos vigentes del propietario.
- Si el denominador es cero o la meta no es calculable, no se muestra un porcentaje inválido; se explica la situación.
- La vista muestra el valor actual y el objetivo sin afirmar que el Usuario podrá cumplirlo.
- El avance se actualiza al crear un gasto y, cuando RF-016 esté implementada, al editar o eliminar.
- Solo el propietario puede consultar su avance.
- No se emiten recomendaciones, predicciones ni juicios sobre la capacidad de ahorro.

**Dependencias:** RF-028, RF-020, RF-021; RF-016 para actualización; decisión D-08.

### RF-030 — Consultar estadísticas agregadas de uso sin acceder a gastos individuales

**Identificador:** RF-030 · **Historia de origen:** HU-30 · **Prioridad:** Should Have · **MVP:** No

**Descripción:** Un Administrador autenticado puede consultar estadísticas agregadas de uso, definidas y aprobadas, sin acceder a gastos, descripciones, montos individuales ni datos que permitan identificar a un Usuario.

**Justificación:** La administración necesita una visión operativa, pero no es parte del flujo de valor del MVP. La privacidad impide exponer datos individuales.

**Criterios de aceptación:**
- Solo un Administrador autenticado accede a las estadísticas agregadas.
- Las métricas mostradas corresponden al conjunto aprobado en D-07 y no incluyen gastos individuales ni descripciones.
- No se muestran grupos por debajo del umbral mínimo de agregación aprobado; si el umbral no está definido, la función no se expone como terminada.
- El Administrador no puede navegar desde un agregado al detalle de un gasto ni identificar a un Usuario a partir de grupos pequeños.
- Un Usuario sin rol administrativo recibe 403 y no obtiene datos agregados reservados.
- Las cifras se actualizan según la frecuencia aprobada en D-07.

**Dependencias:** RF-002, RF-013, RF-033; decisión D-07.

### RF-031 — Consultar usuarios registrados y la información administrativa necesaria

**Identificador:** RF-031 · **Historia de origen:** HU-31 · **Prioridad:** Should Have · **MVP:** No

**Descripción:** Un Administrador autenticado puede consultar una lista paginada de usuarios con los campos administrativos mínimos aprobados, sin acceso a sus gastos, descripciones, montos ni credenciales.

**Justificación:** Facilita la operación y la gestión de cuentas, pero no es necesaria para el flujo principal y requiere definir los campos y permisos exactos.

**Criterios de aceptación:**
- Solo un Administrador autenticado puede consultar la lista de usuarios.
- La lista muestra únicamente los campos aprobados en D-14 y no incluye gastos, descripciones, montos, contraseñas ni tokens.
- La búsqueda, el filtrado y la paginación se limitan a los campos y criterios aprobados en D-14.
- Un Usuario sin rol administrativo recibe 403.
- La consulta no permite inferir datos financieros individuales ni acceder al detalle de una cuenta.
- Los datos se presentan de forma consistente con la política de minimización.

**Dependencias:** RF-030, RF-033; decisiones D-07, D-14 y D-16.

### RF-032 — Activar o desactivar cuentas de usuario desde funciones administrativas autorizadas

**Identificador:** RF-032 · **Historia de origen:** HU-32 · **Prioridad:** Should Have · **MVP:** No

**Descripción:** Un Administrador autorizado puede activar o desactivar una cuenta de Usuario; la desactivación impide el inicio de sesión, invalida sus sesiones según la política aprobada y queda registrada para auditoría.

**Justificación:** Es necesaria para la operación una vez existe el panel administrativo, pero no forma parte del MVP y depende de reglas de auditoría y protección del último administrador.

**Criterios de aceptación:**
- Solo un Administrador autenticado y autorizado puede activar o desactivar cuentas.
- La desactivación impide nuevos inicios de sesión y revoca o invalida las sesiones activas según D-09.
- Un Administrador no puede desactivar su propia cuenta ni dejar el sistema sin un administrador activo, según D-14/D-16.
- La operación queda registrada con actor, fecha, cuenta afectada y motivo cuando D-14 lo exija.
- La activación restaura la posibilidad de iniciar sesión, sin cambiar el rol ni los datos del Usuario.
- El Administrador no obtiene acceso a los gastos de la cuenta afectada.

**Dependencias:** RF-031, RF-033; decisiones D-09, D-14 y D-16.

### RF-033 — Proteger la privacidad de los gastos y garantizar el aislamiento entre usuarios

**Identificador:** RF-033 · **Historia de origen:** HU-33 · **Prioridad:** Must Have · **MVP:** Sí

**Descripción:** Toda operación sobre gastos, análisis o evidencia se autoriza en el backend con la identidad de la sesión y el propietario del recurso; ningún Usuario puede acceder a datos de otra cuenta y ningún Administrador puede acceder a gastos individuales.

**Justificación:** Es una restricción transversal de seguridad y privacidad. Sin ella, el producto no es confiable y los demás requisitos no pueden considerarse terminados.

**Criterios de aceptación:**
- El backend deriva el propietario de la sesión y no confía en un identificador de propietario enviado por el cliente.
- Un Usuario que intenta leer, editar o eliminar un gasto ajeno recibe 403 o 404 sin datos del recurso.
- Un Administrador solo accede a estadísticas agregadas y recibe rechazo en rutas de gastos, fugas y evidencia individual.
- La autorización se aplica en cada operación de lectura o escritura, no solo en la pantalla que muestra el dato.
- La ocultación de información en la interfaz no sustituye la validación en el backend.

**Dependencias:** RF-002; se verifica con RF-013, RF-014, RF-016 y RF-030 a RF-032.

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

**Descripción:** El sistema recopila y devuelve solo los datos necesarios para la función solicitada; los gastos y su detalle se muestran únicamente a su propietario y el Administrador solo recibe agregados que no permitan identificar a una persona.

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
- Las operaciones que afectan varios documentos mantienen una única fuente de verdad o un mecanismo de compensación probado.

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

## C. Matriz de trazabilidad

Las 33 historias de usuario están representadas por al menos un requerimiento funcional. Las historias HU-16 y HU-25 conservan un solo RF porque agrupan operaciones con el mismo objetivo y prioridad. Los requerimientos no funcionales se vinculan a las historias donde se verifican.

| Identificador | Tipo | Historia de usuario relacionada | Prioridad | Inclusión en el MVP |
|---|---|---|---|---|
| RF-001 | Funcional | HU-01 | Must Have | Sí |
| RF-002 | Funcional | HU-02 | Must Have | Sí |
| RF-003 | Funcional | HU-03 | Should Have | No |
| RF-004 | Funcional | HU-04 | Must Have | Sí |
| RF-005 | Funcional | HU-05 | Should Have | No |
| RF-006 | Funcional | HU-06 | Could Have | No |
| RF-007 | Funcional | HU-07 | Should Have | No |
| RF-008 | Funcional | HU-08 | Should Have | No |
| RF-009 | Funcional | HU-09 | Could Have | No |
| RF-010 | Funcional | HU-10 | Must Have | Sí |
| RF-011 | Funcional | HU-11 | Must Have | Sí |
| RF-012 | Funcional | HU-12 | Must Have | Sí |
| RF-013 | Funcional | HU-13 | Must Have | Sí |
| RF-014 | Funcional | HU-14 | Must Have | Sí |
| RF-015 | Funcional | HU-15 | Should Have | No |
| RF-016 | Funcional | HU-16 | Should Have | No |
| RF-017 | Funcional | HU-17 | Could Have | No |
| RF-018 | Funcional | HU-18 | Could Have | No |
| RF-019 | Funcional | HU-19 | Could Have | No |
| RF-020 | Funcional | HU-20 | Must Have | Sí |
| RF-021 | Funcional | HU-21 | Must Have | Sí |
| RF-022 | Funcional | HU-22 | Could Have | No |
| RF-023 | Funcional | HU-23 | Must Have | Sí |
| RF-024 | Funcional | HU-24 | Must Have | Sí |
| RF-025 | Funcional | HU-25 | Could Have | No |
| RF-026 | Funcional | HU-26 | Could Have | No |
| RF-027 | Funcional | HU-27 | Could Have | No |
| RF-028 | Funcional | HU-28 | Won't Have (por ahora) | No |
| RF-029 | Funcional | HU-29 | Won't Have (por ahora) | No |
| RF-030 | Funcional | HU-30 | Should Have | No |
| RF-031 | Funcional | HU-31 | Should Have | No |
| RF-032 | Funcional | HU-32 | Should Have | No |
| RF-033 | Funcional | HU-33 | Must Have | Sí |
| RNF-001 | No funcional | HU-02, HU-13, HU-14, HU-16, HU-23, HU-24, HU-30 a HU-33 | Must Have | Sí |
| RNF-002 | No funcional | HU-08, HU-09, HU-13, HU-16, HU-24, HU-25, HU-30, HU-31, HU-33 | Must Have | Sí |
| RNF-003 | No funcional | HU-02, HU-03, HU-04, HU-05, HU-06, HU-32, HU-33 | Must Have | Sí |
| RNF-004 | No funcional | HU-02, HU-10, HU-11, HU-12, HU-13, HU-14, HU-15, HU-16, HU-18 | Must Have | Sí |
| RNF-005 | No funcional | HU-13, HU-16 | Must Have | Sí |
| RNF-006 | No funcional | HU-16, HU-20, HU-21, HU-22, HU-23, HU-24, HU-27, HU-29 | Should Have | No |
| RNF-007 | No funcional | HU-02, HU-13, HU-32, HU-33 | Must Have | Sí |
| RNF-008 | No funcional | HU-02, HU-03, HU-08, HU-33 | Must Have | Sí |
| RNF-009 | No funcional | HU-01, HU-02, HU-10, HU-11, HU-12, HU-14, HU-20, HU-21, HU-23, HU-24 | Must Have | Sí |
| RNF-010 | No funcional | HU-01, HU-11, HU-33 | Must Have | Sí |
| RNF-011 | No funcional | HU-01, HU-08, HU-10, HU-17, HU-18, HU-19, HU-25 | Must Have | Sí |
| RNF-012 | No funcional | HU-10, HU-11, HU-12, HU-13, HU-14, HU-18, HU-19 | Must Have | Sí |
| RNF-013 | No funcional | HU-11, HU-14, HU-20, HU-21, HU-23, HU-30 | Should Have | No |
| RNF-014 | No funcional | HU-11, HU-23, HU-24, HU-33; todas las historias | Must Have | Sí |
| RNF-015 | No funcional | HU-31, HU-32, HU-33 | Should Have | No |
| RNF-016 | No funcional | HU-06, HU-13, HU-16, HU-29, HU-32, HU-33 | Must Have | Sí |

**Conteo de la matriz:** 33 requerimientos funcionales y 16 no funcionales. No hay historias sin representación; las RNF transversales no sustituyen los RF, sino que definen cómo se verifican.

## D. Alcance priorizado del MVP

### D.1 Requerimientos esenciales del MVP

El MVP se define por **13 requerimientos funcionales Must** y **13 no funcionales Must**. El flujo esencial es: información pública → registro o inicio de sesión → gasto por texto → procesamiento determinista → revisión → guardado → historial → panel de estadísticas → posible fuga con evidencia → cierre de sesión.

| Grupo | Requerimientos | Resultado esperado |
|---|---|---|
| Acceso y sesión | RF-001, RF-002, RF-004 | Entrada pública, identidad y cierre de sesión seguro. |
| Registro y consulta de gastos | RF-010, RF-011, RF-012, RF-013, RF-014 | Texto, interpretación, revisión, persistencia e historial. |
| Panel de estadísticas | RF-020, RF-021 | Total, cantidad, promedio y desglose por categoría. |
| Fugas | RF-023, RF-024 | Detección determinista y evidencia explicable. |
| Privacidad | RF-033 | Aislamiento entre usuarios y límites del Administrador. |
| Seguridad y calidad | RNF-001, RNF-002, RNF-003, RNF-004, RNF-005, RNF-007, RNF-008, RNF-009, RNF-010, RNF-011, RNF-012, RNF-014, RNF-016 | Autorización, privacidad, integridad, confiabilidad y pruebas. |

**Condiciones de borde del MVP:**
- No incluye Google, recuperación de contraseña, perfil editable, foto, filtros, edición/eliminación posterior, voz, alertas, sugerencias, resumen mensual ni metas.
- No incluye panel administrativo. El rol **Administrador** existe y se prueba con cuentas de prueba para verificar que no accede a gastos individuales.
- No incluye notificaciones push. Las alertas locales quedan fuera del MVP junto con RF-025.
- RNF-010 y RNF-016 están pendientes de D-15 y D-06 respectivamente. Son Must porque afectan transparencia y privacidad, pero no se consideran cerrados hasta resolver esas decisiones.
- RNF-006 es Should porque RF-016 no está en el MVP. Si RF-016 se adelanta, RNF-006 se vuelve obligatorio y no puede quedar fuera de la entrega.

### D.2 Requerimientos importantes si hay tiempo

Estos requerimientos son Should y se abordan después de estabilizar el MVP. No sustituyen ni retrasan la seguridad ni la privacidad.

| Requerimiento | Función | Condición para incluirlo |
|---|---|---|
| RF-003 | Inicio de sesión con Google | OAuth configurado y prueba de vinculación segura (D-10). |
| RF-005 | Recuperación de contraseña | Proveedor de correo y política de tokens (D-09). |
| RF-007, RF-008 | Perfil editable y foto con Cloudinary | Cloudinary configurado y reglas de imagen (D-13). |
| RF-015 | Filtros de historial | Historial estable y catálogo/categorías definidos (D-02, D-04). |
| RF-016 | Edición y eliminación | RNF-006 implementado y probado. |
| RF-030, RF-031, RF-032 | Panel administrativo agregado y gestión de cuentas | D-07, D-14 y D-16 resueltas; pruebas de privacidad. |
| RNF-006 | Coherencia de agregados tras cambios | Obligatorio si se implementa RF-016. |
| RNF-013 | Rendimiento y capacidad | Umbrales aprobados y conjunto de prueba representativo. |
| RNF-015 | Auditoría administrativa | Política D-14 aprobada. |

### D.3 Requerimientos postergados

- **Could Have:** RF-006 (desactivación propia), RF-009 (foto de Google), RF-017 a RF-019 (voz Android), RF-022 (comparación de periodos), RF-025 (alertas), RF-026 (sugerencias) y RF-027 (resumen mensual).
- **Won't Have (por ahora):** RF-028 y RF-029 (metas y avance), porque su alcance no está definido y una meta de ahorro carece de fuente de datos.
- **Push remoto:** no forma parte de RF-025 ni del MVP. Requiere proyecto Expo/EAS, credenciales, tokens, consentimiento y backend de envío.
- **Funciones avanzadas:** exportaciones masivas, múltiples niveles administrativos, auditoría avanzada, conexiones bancarias, pagos, inversiones y asesoría financiera.
- **Modelos de IA:** no se entrena un modelo propio ni se usa una API externa de IA para interpretar gastos.

### D.4 Orden de implementación realista para 12 semanas

El orden prioriza el flujo Must, la seguridad desde la primera semana y una integración temprana. La IA puede acelerar el andamiaje y las pruebas, pero no elimina la revisión, la integración ni la depuración.

| Semana | Requerimientos | Entregable y verificación |
|---|---|---|
| 1 | RF-001; inicio de RF-002; RNF-001, RNF-003, RNF-007, RNF-008, RNF-014 | Entorno reproducible, pantalla pública, modelo de usuario, contrato de autenticación y primer arnés de seguridad. |
| 2 | RF-002, RF-004; RNF-002, RNF-004, RNF-005 | Registro, inicio y cierre de sesión; validaciones; pruebas de acceso cruzado y de sesión. |
| 3 | RF-010, RF-011; RNF-009, RNF-010 | Entrada de texto, diccionario y reglas versionadas, etiqueta «Procesar con IA» y textos de ayuda. Resolver D-02 a D-05. |
| 4 | RF-012, RF-013; RNF-012 | Revisión, validaciones en backend, guardado atómico e idempotente; pruebas de fallo y reintento. |
| 5 | RF-014, RF-020, RF-021 | Historial paginado, panel de estadísticas y desglose por categoría con datos de prueba. |
| 6 | RF-023, RF-024; RNF-016 | Motor de reglas con D-01 aprobada, evidencia y estados de datos insuficientes; política de retención D-06. |
| 7 | Todas las Must; RNF-001 a RNF-005, RNF-007 a RNF-012, RNF-014, RNF-016 | Integración de extremo a extremo, suite de seguridad, regresión, rendimiento preliminar, demostración cronometrada y congelación del MVP. No se agrega alcance nuevo. |
| 8 | RF-003, RF-005, RF-007, RF-008 | Integraciones Should. Si una dependencia externa no está lista, se priorizan las demás y no se compromete el MVP. |
| 9 | RF-015, RF-016; inicio de RF-030; RNF-006 | Filtros, edición/eliminación con recálculo, primeras métricas administrativas y pruebas de coherencia. |
| 10 | RF-030, RF-031, RF-032; RNF-015 | Panel administrativo agregado, lista de usuarios, activación/desactivación y auditoría. |
| 11 | RF-022, RF-025, RF-027 o una parte estable de voz; RNF-013 | Could Have seleccionadas y medición de rendimiento. La voz completa no se promete; la semana también sirve de colchón. |
| 12 | Sin requerimientos nuevos | Regresión completa, pruebas de seguridad, documentación, datos de demostración, ensayo y corrección de defectos críticos. |

**Ruta crítica:** RF-001 → RF-002 → RF-010 → RF-011 → RF-012 → RF-013 → RF-014 → RF-020/RF-021 → RF-023 → RF-024. RF-033 se verifica de forma transversal y RF-004 cierra el ciclo de sesión.

**Regla de recorte:** si el cronograma se retrasa, se cancelan primero las Could, luego las Should con dependencias externas y, por último, se reduce la profundidad de una Must sin eliminar la privacidad ni la seguridad. RF-033 y los RNF de seguridad y privacidad no se recortan.

## E. Dependencias y decisiones pendientes

### E.1 Decisiones confirmadas

- **Tecnologías:** React Native + TypeScript, Python + FastAPI, MongoDB Atlas, JWT, Google sign-in, Cloudinary y Expo Notifications.
- **Procesamiento:** diccionario propio y reglas deterministas, sin API externa de IA. Se conserva la etiqueta «Procesar con IA» con explicación transparente.
- **Privacidad:** el backend aplica la autorización y el aislamiento; el Usuario solo accede a sus gastos; el Administrador solo accede a agregados y nunca a gastos individuales.
- **Revisión:** el Usuario revisa y corrige los campos antes de guardar; no hay guardado automático.
- **Coherencia:** si se implementa edición o eliminación, los resúmenes y análisis afectados deben actualizarse.
- **Fugas:** son posibles patrones detectados por reglas deterministas, no predicciones ni diagnósticos.
- **Voz:** solo Android, con Kotlin y `SpeechRecognizer`; no se promete en Expo Go.
- **Alcance:** 12 semanas, MVP de 13 RF Must y 13 RNF Must; push remoto, metas y voz se postergan.
- **Prioridades:** se conservan las prioridades de las 33 historias: 13 Must, 9 Should, 9 Could y 2 Won't para los RF.

### E.2 Dependencias y decisiones pendientes más relevantes

| ID | Tipo | Dependencia o decisión | Requerimientos afectados | Efecto si no se resuelve |
|---|---|---|---|---|
| D-01 | Pendiente | Umbrales, monto mínimo, frecuencia, ventana, agrupación y condición mínima de datos para fugas. | RF-023, RF-024, RF-027 | No se puede implementar ni probar la detección; no se deben inventar valores. |
| D-02 | Pendiente | Catálogo de categorías, tratamiento de «Otros» y desempate de la categoría principal. | RF-011, RF-012, RF-015, RF-021, RF-026 | La interpretación y el panel de estadísticas quedan indefinidos. |
| D-03 | Pendiente | Moneda, configuración regional, decimales, separadores, límites y redondeo. | RF-011 a RF-013, RF-020 a RF-022, RF-028, RF-029 | Los cálculos y formatos pueden requerir migración. |
| D-04 | Pendiente | Zona horaria, formatos de fecha, periodos, meses parciales y fechas futuras. | RF-011, RF-012, RF-014, RF-015, RF-020 a RF-022, RF-027 | El orden, los filtros y las comparaciones pueden ser incorrectos. |
| D-05 | Pendiente | Límites del parser, formatos, varias frases, longitud de descripción y tamaño de página. | RF-010 a RF-012, RF-014, RF-019 | No hay criterios de borde para el diccionario ni la paginación. |
| D-06 | Pendiente | Retención, desactivación, eliminación, reactivación y respaldos. | RF-006, RF-013, RF-016, RF-029, RF-032; RNF-016 | No se deben exponer borrados irreversibles ni definir retención por suposición. |
| D-07 | Pendiente | Métricas administrativas, umbral mínimo de agregación y frecuencia de actualización. | RF-030, RF-031; RNF-002 | Los agregados podrían reidentificar a un Usuario. |
| D-08 | Pendiente | Alcance de la meta: gasto o ahorro, fuente de ingresos, gastos incluidos y avance. | RF-028, RF-029 | Las metas siguen postergadas y no pueden implementarse sin una regla. |
| D-09 | Pendiente | Política de contraseñas, verificación de correo, vigencia, renovación, revocación, límites de intentos y proveedor de correo. | RF-002, RF-004, RF-005, RF-006, RF-032; RNF-003 | La seguridad de sesión y recuperación queda incompleta. |
| D-10 | Pendiente | Vinculación entre cuentas de Google y cuentas locales, correos coincidentes y cuentas solo con Google. | RF-003, RF-009 | Existe riesgo de toma de control de cuenta. |
| D-11 | Pendiente | Notificaciones locales, contenido, frecuencia, recordatorios, pantalla bloqueada y preferencias. | RF-025; RNF-002 | Las alertas no tienen un alcance de privacidad cerrado. |
| D-12 | Pendiente | Versión mínima de Android, idioma, duración, audio, transcripción y funcionamiento sin conexión. | RF-017 a RF-019 | La voz no se puede implementar ni probar de forma consistente. |
| D-13 | Pendiente | Campos y formatos de perfil, límites de imagen, recorte, precedencia Google/carga y borrado en Cloudinary. | RF-007 a RF-009 | El perfil y la foto quedan indefinidos. |
| D-14 | Pendiente | Campos visibles, búsqueda, motivo de desactivación, auditoría y protección del último administrador. | RF-031, RF-032; RNF-015 | La administración puede ser insegura o quedar sin trazabilidad. |
| D-15 | Pendiente | Texto público y explicación de la etiqueta «Procesar con IA» y del procesamiento determinista. | RF-001, RF-011; RNF-010 | La interfaz puede generar expectativas engañosas. |
| D-16 | Pendiente | Provisión de administradores y prevención del registro público de administradores. | RF-030 a RF-032 | No existe una vía segura para operar el rol administrativo. |

### E.3 Dependencias externas

- **Google OAuth:** requerido por RF-003 y RF-009; no bloquea el MVP.
- **Proveedor de correo transaccional:** requerido por RF-005; no bloquea el MVP.
- **Cloudinary:** requerido por RF-008 y RF-009; no bloquea el MVP.
- **Expo/EAS, FCM/APNs y backend de envío:** requeridos solo si se implementa push remoto, que está postergado.
- **Compilación Android con módulo Kotlin y dispositivo o emulador compatible:** requerido por RF-017 a RF-019; no bloquea el MVP.
- **MongoDB Atlas, hospedaje del backend y HTTPS:** requeridos por todas las historias; deben estar disponibles desde la semana 1.
- **Herramientas de IA:** apoyan escritura y pruebas, pero no son una dependencia de ejecución del producto ni sustituyen la revisión humana.

### E.4 Supuestos

- **S-01:** el proyecto lo desarrolla una persona durante 12 semanas con apoyo de IA.
- **S-02:** React Native, FastAPI, MongoDB Atlas y el entorno de despliegue están disponibles.
- **S-03:** el MVP puede usar correo y contraseña; Google se incorpora después.
- **S-04:** existe una vía segura para provisionar la primera cuenta administradora.
- **S-05:** el procesamiento determinista se ejecuta en el backend y no llama a una API externa de IA.
- **S-06:** la voz es solo para Android y el texto es la alternativa en iOS.
- **S-07:** las notificaciones del alcance actual son locales o dentro de la aplicación; el push es futuro.
- **S-08:** los datos de demostración son sintéticos y no contienen información financiera real.
- **S-09:** la moneda y la configuración regional se definirán en D-03; no se asume una moneda por los ejemplos del documento fuente.
- **S-10:** las decisiones pendientes se resolverán antes de las semanas indicadas; si no, las historias afectadas se postergarán.
- **S-11:** el MVP puede demostrarse sin panel administrativo, sin voz y sin push.
- **S-12:** las dependencias externas pueden usarse en el contexto académico sin costos o infraestructura no previstos.

### E.5 Orden recomendado para resolver lo pendiente

1. **Antes de la semana 3:** D-02, D-03, D-04 y D-05, porque bloquean la interpretación, la persistencia y el panel de estadísticas.
2. **Antes de la semana 6:** D-01, porque bloquea la detección verificable de fugas.
3. **Antes de la semana 8:** D-09, D-10, D-13 y D-15, por seguridad, integraciones y transparencia.
4. **Antes de la semana 10:** D-07, D-14 y D-16, por el panel administrativo y la auditoría.
5. **Antes de implementar la función correspondiente:** D-06 para retención y borrado; D-08 para metas; D-11 para alertas; D-12 para voz.
6. **Antes de cerrar el MVP:** resolver RNF-010 y RNF-016, que son Must pero dependen de D-15 y D-06. Si no se resuelven, el MVP no puede declararse cerrado aunque el flujo funcione.

**Criterio de cierre:** el documento está completo para planificación, pero la implementación no debe comenzar las historias afectadas por decisiones pendientes sin aprobación explícita. La seguridad y la privacidad no se postergan; las funciones que dependen de una decisión no aprobada se retrasan antes que inventar una regla.