# Priorización de Requisitos (MoSCoW) — FUGA+

*Leyenda de priorización: **Must** (esencial para el MVP), **Should** (importante, el MVP funciona sin ello), **Could** (opcional, si sobra tiempo) y **Won't** (fuera del alcance del MVP). FUGA+ ("Descubre por dónde se va tu plata") se desarrolla por una persona en 12 semanas y su MVP debe demostrarse en aproximadamente 3 minutos.*

## RF-01 — Must

**Nombre del requisito: Acceso público a la información de FUGA+.**
El sistema debe proporcionar, sin autenticación, una pantalla pública donde el visitante conozca qué es FUGA+, cómo funciona el registro de gastos en lenguaje natural, cuál es su propuesta de valor (detectar fugas de dinero por gastos pequeños y repetitivos) y qué funcionalidades ofrece. Desde esa misma pantalla el visitante debe poder acceder a las opciones de registro y de inicio de sesión. El visitante no debe poder consultar gastos personales, historial, dashboard ni información financiera de ningún usuario.

**Criterio de aceptación:** Un usuario no autenticado que abre la aplicación ve la pantalla pública con la descripción de FUGA+, la explicación del flujo de registro, las funcionalidades principales y los botones de registro e inicio de sesión; al intentar navegar a historial, dashboard o gastos, el sistema lo bloquea y lo dirige a la pantalla pública o al inicio de sesión.

## RF-02 — Must

**Nombre del requisito: Registro e inicio de sesión de usuarios.**
El sistema debe permitir que una persona se registre con correo electrónico y contraseña, y que posteriormente inicie sesión con credenciales válidas. El sistema debe asignar el rol de Usuario a toda cuenta creada mediante el registro público y diferenciar ese rol del rol Administrador. El sistema debe rechazar el inicio de sesión con credenciales inválidas y debe rechazar la sesión de cuentas desactivadas por el administrador.

**Criterio de aceptación:** Un usuario nuevo puede crear su cuenta con correo y contraseña, cerrar sesión, volver a iniciar sesión con las mismas credenciales y acceder a sus funcionalidades; un correo o contraseña incorrectos muestran un mensaje de error sin revelar cuál de los dos fue incorrecto; una cuenta desactivada no puede iniciar sesión; las cuentas creadas por registro público nunca reciben el rol Administrador.

## RF-03 — Must

**Nombre del requisito: Registro de gastos mediante texto en lenguaje natural.**
El sistema debe permitir que un usuario autenticado registre un gasto escribiendo una frase en lenguaje natural, por ejemplo "Hoy gasté $8.000 en un taxi". El sistema debe aceptar texto libre en español, con o sin signos de moneda, y enviar esa frase a la interpretación (RF-04) mostrando el resultado antes de guardar. El usuario debe poder descartar la interpretación y volver a escribir una nueva frase.

**Criterio de aceptación:** Con sesión iniciada, el usuario escribe una frase que contiene un monto y un concepto, la envía y ve en pantalla los campos interpretados sin que el gasto haya quedado almacenado aún; puede repetir el envío con otra frase y solo la última interpretación vigente se muestra.

## RF-04 — Must

**Nombre del requisito: Interpretación del gasto mediante IA (monto, categoría y descripción).**
El sistema debe enviar el texto registrado por el usuario a un modelo de IA y obtener tres campos: monto (valor numérico y moneda), categoría (perteneciente a un conjunto cerrado y predefinido de categorías, por ejemplo Transporte, Alimentación, Ocio, Educación, Servicios) y descripción (texto corto que nombra el gasto). El sistema debe mostrar esos tres campos al usuario de forma editable antes de confirmar, y debe manejar los casos en que el texto no contenga un monto reconocible, soliciting corrective input or indicating the error.

**Criterio de aceptación:** Al enviar "Hoy gasté $8.000 en un taxi", la pantalla muestra Monto = 8.000, Categoría = Transporte y Descripción = Taxi, con la posibilidad de editar cualquiera de los tres campos antes de confirmar; si la frase no contiene un monto identificable, el sistema informa que no pudo interpretar el monto y no permite guardar el gasto como confirmado.

## RF-05 — Must

**Nombre del requisito: Almacenamiento persistente de gastos confirmados.**
El sistema debe almacenar de forma persistente cada gasto confirmado por el usuario junto con: monto, categoría, descripción, fecha del gasto, usuario propietario y el texto original que originó la interpretación. Cada gasto debe quedar asociado exclusivamente a un único usuario propietario. El sistema debe conservar los gastos aunque el usuario cierre sesión y debe permitir su recuperación posterior.

**Criterio de aceptación:** Tras confirmar un gasto, el usuario cierra sesión, vuelve a iniciar sesión y el gasto aparece en su historial con monto, categoría, descripción, fecha y texto original; al revisar los datos almacenados se verifica que cada gasto tiene un único propietario y que ningún usuario puede leer gastos de otro mediante la interfaz.

## RF-06 — Must

**Nombre del requisito: Historial cronológico de gastos.**
El sistema debe mostrar al usuario autenticado la lista de sus gastos confirmados ordenados de más reciente a más antiguo, con monto, categoría, descripción y fecha de cada registro. El historial debe ser paginado o desplazamiento infinito para no cargar todas las operaciones de una vez. El usuario debe poder abrir el detalle de un gasto del historial.

**Criterio de aceptación:** Con al menos diez gastos almacenados, el historial los presenta ordenados de forma descendente por fecha, cada uno con sus cuatro campos visibles; el usuario puede desplazarse hasta el registro más antiguo y abrir el detalle de cualquier gasto listado.

## RF-07 — Must

**Nombre del requisito: Dashboard de resumen de gastos del usuario.**
El sistema debe ofrecer al usuario autenticado un dashboard simple que consolide sus gastos: total gastado en el periodo actual, cantidad de gastos registrados, promedio por gasto y total acumulado del gasto acumulado por categoría, mostrando la categoría de mayor peso. El dashboard debe construirse exclusivamente con los gastos del propio usuario.

**Criterio de aceptación:** Al entrar al dashboard, el usuario ve el total gastado, el número de gastos, el promedio por gasto y el desglose por categoría; los valores mostrados coinciden con la suma de los gastos propios del periodo seleccionado y ningún dato correspondiente a otro usuario aparece en pantalla.

## RF-08 — Must

**Nombre del requisito: Identificación de posibles fugas de dinero mediante reglas predefinidas.**
El sistema debe analizar los gastos almacenados del usuario mediante un conjunto de reglas y patrones predefinidos, centrados en gastos pequeños y repetitivos, e identificar posibles fugas. El análisis debe ser determinista y basado en reglas (por ejemplo: misma categoría o descripción con umbral de días, y categoría con al menos N repeticiones dentro de una ventana temporal), NO debe ser una predicción de IA. El sistema debe presentar cada fuga detectada indicando la categoría o descripción afectada, el número de ocurrencias, el monto acumulado y la evidencia que activó la regla. Si no hay gastos suficientes, el sistema debe indicar que aún no hay datos suficientes en lugar de mostrar resultados.

**Criterio de aceptación:** Con cinco gastos de "Café" de $4.000 en cinco días distintos, el sistema lista una posible fuga por la categoría/descripción "Café" con 5 ocurrencias y $20.000 acumulados, citando la regla activada; con menos de tres gastos registrados en total, el sistema informa que no hay suficientes gastos para el análisis; el resultado no proviene de un modelo de IA sino de la evaluación de reglas sobre los gastos almacenados.

## RF-09 — Should

**Nombre del requisito: Consultas y filtros básicos de gastos.**
El sistema debe permitir que el usuario autenticado filtre su historial por rango de fechas y por categoría, y que la lista resultante se corresponda solo con gastos propios que cumplen los criterios indicados. El usuario debe poder limpiar los filtros aplicados y volver a ver la lista completa.

**Criterio de aceptación:** Al filtrar por categoría "Transporte" y un rango de fechas, el historial muestra únicamente los gastos propios de esa categoría dentro del periodo; al limpiar los filtros se recupera la lista completa; ninguna consulta devuelve gastos de otro usuario.

## RF-10 — Should

**Nombre del requisito: Corrección de la categoría asignada por la IA.**
El sistema debe permitir que el usuario corrija la categoría de un gasto ya confirmado cuando la asignación de la IA sea incorrecta, seleccionando una categoría válida del conjunto predefinido. El cambio debe quedar persistido y debe reflejarse de inmediato en el historial, en el dashboard y en el análisis de fugas, usando la categoría corregida. La corrección puede realizarse tanto desde la vista previa previa a la confirmación como desde el detalle de un gasto almacenado.

**Criterio de aceptación:** Tras corregir un gasto de "Ocio" a "Transporte", el historial, el dashboard y el análisis de fugas utilizan "Transporte"; al revisar el registro almacenado, el campo categoría conserva el valor corregido y el texto original del gasto se mantiene sin cambios.

## RF-11 — Should

**Nombre del requisito: Dashboard administrativo con estadísticas generales agregadas.**
El sistema debe proporcionar al Administrador autenticado un panel con estadísticas agregadas de la aplicación: total de usuarios registrados, número total de gastos almacenados, promedio general de gasto y distribución de gastos por categoría a nivel global. El panel no debe exponer montos, categorías ni descripciones de los gastos de un usuario identificable de forma individual.

**Criterio de aceptación:** Un Administrador autenticado ve el número de usuarios, el total de gastos, el promedio general y el reparto por categoría; al inspeccionar el panel no aparece ningún gasto con su propietario, monto ni descripción individual.

## RF-12 — Should

**Nombre del requisito: Gestión de usuarios por el Administrador.**
El sistema debe permitir al Administrador ver la lista de usuarios registrados con su estado (activo/inactivo) y activar o desactivar cuentas. Una cuenta desactivada no puede iniciar sesión ni operar. El Administrador no debe poder consultar ni modificar los gastos ni los datos financieros de ningún usuario, y no puede desactivar su propia cuenta.

**Criterio de aceptación:** El Administrador lista todos los usuarios, desactiva una cuenta y el usuario afectado no puede iniciar sesión; al reactivarla, el usuario recupera el acceso; desde el panel administrativo no es posible abrir, editar ni eliminar gastos de un usuario; el Administrador no puede desactivar su propia cuenta.

## RF-13 — Could

**Nombre del requisito: Alertas dentro de la aplicación sobre posibles fugas.**
El sistema debe mostrar una alerta en la propia aplicación cuando el análisis por reglas (RF-08) detecte una nueva posible fuga, indicando categoría, monto acumulado y número de ocurrencias. La alerta debe ser informativa dentro de la aplicación y no debe requerir notificaciones del sistema operativo.

**Criterio de aceptación:** Al detectar el análisis una posible fuga que el usuario no había visto, la aplicación muestra una alerta con la categoría, el monto acumulado y las ocurrencias; la alerta no se presenta si no hay fugas detectadas y no depende de permisos de notificaciones del dispositivo.

## RF-14 — Could

**Nombre del requisito: Registro de gastos por voz.**
El sistema debe permitir registrar un gasto mediante la transcripción de voz del usuario, reutilizando el flujo de interpretación de RF-03 y RF-04: el texto obtenido por voz se envía al mismo proceso de extracción de monto, categoría y descripción antes de la confirmación. Si la transcripción no es posible, el sistema debe indicar el fallo y permitir escribir el gasto de forma manual.

**Criterio de aceptación:** El usuario activa la entrada por voz, pronuncia una frase de gasto y el sistema muestra la interpretación con monto, categoría y descripción para confirmar, exactamente igual que en el flujo por texto; si la transcripción falla, se muestra un mensaje y el flujo manual por texto sigue disponible.

## RF-15 — Could

**Nombre del requisito: Comparación entre períodos de gastos.**
El sistema debe permitir comparar dos períodos (por ejemplo, mes actual contra mes anterior, o dos semanas) mostrando total gastado, cantidad de gastos y promedio por gasto en cada período, indicando la variación absoluta y porcentual entre ellos.

**Criterio de aceptación:** Al comparar dos períodos con datos, el sistema muestra los totales y promedios de cada período junto con la diferencia absoluta y porcentual; si uno de los períodos no tiene gastos, la comparación lo indica como período sin registros.

---

## RNF-01 — Must

**Nombre del requisito: Viabilidad para un desarrollador único en un período de 12 semanas.**
El conjunto de requisitos priorizados como Must debe poder implementarse por una sola persona en 12 semanas, con un stack tecnológico ya conocido por el desarrollador y sin depender de infraestructura institucional o de terceros de pago. El alcance Must no debe requerir el desarrollo de modelos de IA propios ni la integración con sistemas bancarios externos.

**Criterio de aceptación:** Existe una planificación de 12 semanas que asigna las tareas de todos los requisitos Must a un único desarrollador sin solapamiento de trabajo crítico; el esfuerzo total estimado de la planificación es compatible con el calendario; ningún requisito Must depende de un servicio no disponible en el entorno de desarrollo.

## RNF-02 — Must

**Nombre del requisito: Demostración del MVP en aproximadamente 3 minutos.**
El flujo principal de demostración (acceso público, registro o inicio de sesión, registro de gasto por texto, interpretación, confirmación, historial, dashboard y detección de una posible fuga) debe poder ejecutarse de principio a fin en aproximadamente 3 minutos, con datos de prueba cargados previamente y sin pasos manuales de configuración durante la demostración.

**Criterio de aceptación:** En una prueba cronometrada del flujo completo, con datos de prueba ya cargados, la ejecución concluye en tres minutos o menos; no se requiere crear cuentas manualmente, escribir más de un gasto de ejemplo ni reiniciar servicios durante la demostración.

## RNF-03 — Must

**Nombre del requisito: Alcance de la IA limitado a la interpretación y clasificación de gastos.**
La IA debe usarse únicamente para extraer monto, categoría y descripción a partir del texto en lenguaje natural. Queda prohibido usarla para predecir fugas, generar recomendaciones financieras, pronosticar el comportamiento de gasto o tomar decisiones automáticas sobre el usuario. La detección de fugas debe resolverse con reglas predefinidas y deterministas.

**Criterio de aceptación:** Al revisar el código y la configuración del sistema, la única invocación de IA corresponde al módulo de interpretación de RF-04; el módulo de detección de fugas (RF-08) se ejecuta con reglas locales sin llamadas a modelos de IA; no existen salidas del sistema que se presenten como predicciones o asesoramiento financiero.

## RNF-04 — Must

**Nombre del requisito: Seguridad y control de acceso basado en roles.**
Todas las rutas y operaciones que consumen datos personales deben protegerse con autenticación y autorización. El sistema debe reconocer exactamente tres roles: Visitante (sin sesión, solo información pública), Usuario (sus propios datos únicamente) y Administrador (estadísticas agregadas y gestión de cuentas). Cada petición al servidor debe validarse en el servidor, no solo en la interfaz. Las contraseñas deben almacenarse cifradas (hash con sal) y nunca en texto plano.

**Criterio de aceptación:** Un Usuario que manipula el identificador de un gasto ajeno no logra leerlo porque el servidor responde con error de autorización; un Usuario que intenta abrir el panel administrativo recibe acceso denegado; un Visitante no accede a ninguna ruta protegida; las contraseñas almacenadas aparecen como hashes con sal y no como texto legible.

## RNF-05 — Must

**Nombre del requisito: Privacidad y aislamiento de los datos de gastos del usuario.**
Los gastos de cada usuario son datos privados: deben estar asociados a un único propietario y solo ser visibles para ese propietario. El Administrador únicamente debe ver información agregada, nunca los gastos individuales ni sus montos y descripciones identificables. Los datos de gastos no deben enviarse a servicios de terceros que los acumulen fuera del control del proyecto.

**Criterio de aceptación:** Cada consulta de gastos al almacenamiento incluye el filtro de propietario y devuelve cero resultados para un usuario distinto al propietario; las estadísticas administrativas no permiten derivar el gasto de un usuario concreto; una revisión de las salidas de la aplicación confirma que los gastos del usuario no se transmiten a terceros.

---

## Won't — Explícitamente fuera de alcance del MVP

- Conexiones bancarias
- Pagos
- Transferencias
- Tarjetas
- Líneas de crédito
- Préstamos
- Inversiones
- Asesoría financiera profesional
- Entrenamiento de un modelo de IA propio
- Predicción de mercado
- Datos bancarios reales de terceros
- Notificaciones push avanzadas
- Escaneo avanzado de recibos
- Integraciones bancarias externas
- Funciones administrativas avanzadas
- Gestión de múltiples niveles de administrador

---

## Justificación de la priorización

**Acceso público y registro/inicio de sesión (RF-01, RF-02) como Must.** El acceso público es el punto de entrada al producto: sin una pantalla que explique qué es FUGA+ no hay forma de captar al visitante ni de dirigirlo al registro. El registro y el inicio de sesión son la frontera entre el rol Visitante y el rol Usuario: a partir de ellos existe la identidad que permite asociar gastos y aplicar privacidad y permisos. Ambos requisitos son, además, los dos primeros pasos del flujo de demostración de 3 minutos, por lo que no pueden quedar fuera del MVP.

**Cadena de valor central (RF-03 a RF-08) como Must.** El registro por texto, la interpretación por IA, el almacenamiento, el historial, el dashboard y la detección de fugas forman una cadena de valor indivisible: cada eslabón consume el anterior y el producto pierde su sentido si alguno falta. Sin RF-03 no hay entrada de datos; sin RF-04 la frase en lenguaje natural no se convierte en información utilizable; sin RF-05 no hay datos que consultar ni analizar; sin RF-06 y RF-07 el usuario no ve el resultado de lo que registró; y sin RF-08 no se cumple la propuesta de valor central de FUGA+, que es descubrir por dónde se va la plata. Estos seis requisitos son además el núcleo exacto del flujo de demostración.

**Consultas y corrección de categoría (RF-09, RF-10) como Should.** Ambas capacidades mejoran la experiencia y la confianza del usuario, pero no son necesarias para que el flujo principal funcione: el MVP puede operar con un historial completo y sin filtros, y con una categoría editable únicamente en la vista previa a la confirmación. Como la interpretación por IA no es infalible, la corrección de categoría debe quedar contemplada en el MVP; su implementación completa, conectada al análisis de fugas y al dashboard, puede programarse después de las acciones Must.

**Dashboard administrativo y gestión de usuarios (RF-11, RF-12) como Should.** El Administrador es un actor requerido por el sistema y su rol debe existir desde el inicio (RNF-04), pero su panel no forma parte del flujo de valor que se demuestra en 3 minutos. El MVP se sostiene sin un panel administrativo completo; no obstante, la activación y desactivación de cuentas sí es relevante para poder responder ante cuentas indebidas en una demostración o prueba.

**Alertas, registro por voz y comparación de períodos (RF-13, RF-14, RF-15) como Could.** Los tres requisitos son valiosos para el producto pero no para su núcleo de valor demostrado: las alertas repiten información ya disponible en el análisis de fugas, el registro por voz es una forma alternativa de entrada que no aporta una capacidad nueva, y la comparación de períodos amplía el dashboard sin resolver un problema central del MVP. Se incluyen como Could porque solo se desarrollan si el cronograma de 12 semanas lo permite una vez completados todos los Must y Should, y se sacrifican de inmediato si comprometen la entrega.

**Requisitos no funcionales como Must.** RNF-01 y RNF-02 no son ajustes de calidad sino condiciones de existencia del proyecto: si el alcance Must no cabe en 12 semanas para una persona, el MVP no se entrega; si el flujo no cabe en 3 minutos, el objetivo de demostración no se cumple. RNF-03 es Must porque delimita qué significa "IA" en este proyecto y evita que la detección de fugas se presente como predicción, lo que diferenciaría falsamente el producto. RNF-04 y RNF-05 son Must porque los gastos son datos financieros privados y el sistema maneja tres roles con privilegios distintos: sin control de acceso por roles ni aislamiento por usuario, el sistema no puede considerarse aceptable ni demostrable frente a usuarios reales. Los Won't se excluyen explícitamente porque cada uno de ellos implica banca, pagos, regulación o infraestructura de IA que es inviable para un desarrollador único en 12 semanas.

---

## Requisitos esenciales para la demostración

El flujo principal de demostración de 3 minutos (RNF-02) se construye con los siguientes requisitos:

- RF-01 — Acceso público
- RF-02 — Registro e inicio de sesión
- RF-03 — Registro por texto
- RF-04 — Interpretación por IA
- RF-05 — Almacenamiento
- RF-06 — Historial
- RF-07 — Dashboard
- RF-08 — Detección de posibles fugas
- RNF-02 — Restricción de tiempo de la demostración

Orden de ejecución: el Visitante entra por RF-01 y se autentica con RF-02; el Usuario registra un gasto con RF-03, ve la interpretación de RF-04 y la confirma, lo que activa RF-05; luego consulta RF-06 y RF-07; finalmente RF-08 muestra una posible fuga detectada por reglas predefinidas sobre los gastos ya almacenados.

El panel administrativo (RF-11 y RF-12) puede mostrarse brevemente como parte del recorrido general del sistema para evidenciar que existe una gestión de usuarios y estadísticas agregadas, pero **no forma parte del flujo principal de 3 minutos**: queda fuera de la ruta crítica de la demostración y se presenta, si el tiempo lo permite, después del flujo principal.

---

## Dependencias

Dependencias lógicas entre los requisitos:

- RF-02 depende de RF-01 (el acceso público ofrece los puntos de entrada al registro).
- RF-03 depende de RF-02 (solo un usuario autenticado registra gastos).
- RF-04 depende de RF-03 (se interpreta el texto capturado en RF-03).
- RF-05 depende de RF-04 (se almacena lo confirmado tras la interpretación).
- RF-06 depende de RF-05 (el historial se construye sobre gastos almacenados).
- RF-07 depende de RF-05 (el dashboard consolida gastos almacenados).
- RF-08 depende de RF-05 y de una cantidad suficiente de gastos históricos almacenados (el análisis se ejecuta sobre datos persistidos y requiere volumen para detectar repetición).
- RF-09 depende de RF-05 (los filtros operan sobre gastos almacenados).
- RF-10 depende de RF-04 y RF-05 (se corrige una categoría ya interpretada y ya persistida, en la vista previa o sobre el gasto almacenado).
- RF-11 depende de la existencia de usuarios registrados y de los datos almacenados por el sistema (las estadísticas agregadas se calculan sobre ese conjunto).
- RF-12 depende de RF-02 y de la gestión de roles y permisos (solo el Administrador, definido en RF-02, gestiona cuentas).
- RF-13 depende de RF-08 (la alerta se genera a partir de una fuga ya detectada por reglas).
- RF-14 depende de RF-03 y RF-04 (la voz produce texto que recorre el mismo flujo de registro e interpretación).
- RF-15 depende de RF-05 y RF-07 (compara datos almacenados usando los totales y promedios ya calculados en el dashboard).
- RNF-02 depende de que RF-02, RF-03, RF-04, RF-05, RF-06, RF-07 y RF-08 funcionen correctamente de forma integrada.

Cadena crítica para la demostración: **RF-01 → RF-02 → RF-03 → RF-04 → RF-05 → (RF-06, RF-07, RF-08)**. Si algún eslabón de esta cadena falla, la demostración de 3 minutos no puede completarse.

---

## Riesgos clave

**1. RF-04 — Interpretación basada en IA.**
Riesgo técnico: el texto informal en español ("Hoy gasté $8.000 en un taxi") puede no permitir extraer de forma confiable el monto, la categoría y la descripción; pueden aparecer formatos de moneda variables ("8.000", "$8k", "ocho mil"), abreviaturas o frases sin monto claro. Mitigación: restringir la salida a un esquema cerrado con tres campos y un conjunto cerrado de categorías, validar el formato de la respuesta antes de mostrarla, mostrar siempre los campos editables (soporte de RF-10) y exigir un monto reconocible para poder confirmar.

**2. RF-08 — Identificación de fugas.**
Riesgo de diseño y validación: definir reglas que generen resultados creíbles es la parte más difícil del producto; reglas demasiado laxas producen falsos positivos que hacen perder confianza en la herramienta, y reglas demasiado estrictas no detectan fugas reales. Además, con pocos datos de un usuario el análisis puede no ser representativo. Mitigación: pocas reglas iniciales y explicables (repetición por categoría o descripción en una ventana temporal, con umbral mínimo de ocurrencias y monto acumulado), mostrar la evidencia que activó la regla, indicar explícitamente cuando no hay datos suficientes y validar las reglas con un conjunto de gastos de prueba antes de la demostración.

**3. RNF-04 — Seguridad y roles.**
Riesgo de implementación: errores en la autenticación, en la autorización por rol o en la validación de propiedad pueden exponer gastos de un usuario a otro, o permitir que un Usuario alcance funciones administrativas. Mitigación: validación de sesión y de permisos en el servidor en cada petición protegida (no solo ocultando opciones en la interfaz), filtro obligatorio de propietario en toda consulta de gastos, contraseñas almacenadas con hash y sal, y pruebas explícitas de acceso directo con identificadores ajenos.

**4. RNF-02 — Demostración de 3 minutos.**
Riesgo de integración y pruebas: al ser un desarrollador único, cualquier fallo de integración entre autenticación, interpretación, almacenamiento, historial, dashboard y análisis rompe la demostración completa; además, la interpretación por IA añade latencia variable y las dependencias externas pueden fallar durante la exposición. Mitigación: datos de prueba cargados previamente, una sola ruta crítica probada de extremo a extremo antes de la demostración, respuesta de interpretación rápida o con alternativa de carga manual, y un plan de contingencia (grabación de respaldo) ante fallos de la IA o de la red durante la exposición.