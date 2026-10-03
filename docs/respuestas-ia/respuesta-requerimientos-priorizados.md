# Priorización de Requisitos (MoSCoW) — FUGA+

## RF-01 — Must

**Acceso público:** El sistema debe permitir que una persona conozca FUGA+ sin necesidad de registrarse.

**Criterio de aceptación:** Al ingresar a la aplicación, el visitante debe poder visualizar información básica sobre FUGA+, su funcionamiento y sus principales funcionalidades, además de las opciones para registrarse o iniciar sesión.

## RF-02 — Must

**Registro e inicio de sesión:** El sistema debe permitir a los usuarios crear una cuenta e iniciar sesión para acceder a las funcionalidades personales de FUGA+.

**Criterio de aceptación:** Un visitante debe poder registrarse con sus datos básicos y posteriormente iniciar sesión para acceder a su información personal.

## RF-03 — Must

**Registro de gastos por texto:** El sistema debe permitir registrar un gasto escribiendo una descripción en lenguaje natural.

**Criterio de aceptación:** Al ingresar un texto como "Hoy gasté $8.000 en un taxi", el sistema debe aceptar la entrada y enviarla al motor de interpretación.

## RF-04 — Must

**Interpretación basada en IA:** El sistema debe interpretar la información registrada e identificar elementos como monto, categoría y descripción.

**Criterio de aceptación:** A partir del texto ingresado en RF-03, el sistema debe extraer el monto (ej. $8.000), asignar una categoría (ej. "Transporte") y generar una descripción resumida, mostrando el resultado al usuario.

## RF-05 — Must

**Almacenamiento de gastos:** El sistema debe almacenar los gastos registrados para su consulta posterior.

**Criterio de aceptación:** Tras confirmar la interpretación de RF-04, el gasto debe quedar guardado de forma persistente y recuperable en sesiones posteriores.

## RF-06 — Must

**Historial de gastos:** El sistema debe permitir visualizar los gastos registrados mediante un historial.

**Criterio de aceptación:** El usuario debe poder acceder a una lista cronológica de sus gastos almacenados, mostrando al menos fecha, monto, categoría y descripción de cada uno.

## RF-07 — Must

**Dashboard:** El sistema debe mostrar un dashboard simple con información sobre los gastos registrados.

**Criterio de aceptación:** El dashboard debe mostrar, como mínimo, un resumen visual (ej. totales por categoría) que se actualice al registrar un nuevo gasto.

## RF-08 — Must

**Identificación de posibles fugas de dinero:** El sistema debe analizar los gastos mediante reglas propias para identificar posibles fugas de dinero, principalmente relacionadas con gastos pequeños y repetitivos.

**Criterio de aceptación:** Al detectar un patrón que cumpla con una regla predefinida (ej. varios gastos pequeños en la misma categoría dentro de un período), el sistema debe señalar visualmente ese patrón como una posible fuga.

## RF-09 — Should

**Consultas básicas:** El sistema debe permitir realizar consultas básicas sobre los gastos registrados.

**Criterio de aceptación:** El usuario debe poder filtrar o consultar sus gastos por al menos un criterio simple (ej. categoría o rango de fechas) y obtener un resultado coherente con los datos almacenados.

## RF-10 — Should

**Corrección de categoría:** El sistema debe permitir al usuario modificar la categoría asignada por la IA cuando esta sea incorrecta.

**Criterio de aceptación:** El usuario debe poder seleccionar una nueva categoría y el sistema debe actualizar el gasto, reflejando el cambio en el historial y dashboard.

## RF-11 — Should

**Dashboard administrativo:** El sistema debe proporcionar al administrador un dashboard con estadísticas generales de la aplicación.

**Criterio de aceptación:** El administrador debe poder visualizar información general como cantidad de usuarios registrados, cantidad de gastos registrados y estadísticas agrupadas del sistema.

## RF-12 — Should

**Gestión de usuarios:** El sistema debe permitir al administrador gestionar las cuentas de los usuarios registrados.

**Criterio de aceptación:** El administrador debe poder consultar la lista de usuarios y activar o desactivar una cuenta cuando sea necesario.

## RF-13 — Could

**Alertas sobre posibles fugas:** El sistema podrá mostrar una alerta dentro de la aplicación cuando se detecte una posible fuga de dinero.

**Criterio de aceptación:** Si se implementa, cuando RF-08 detecte una posible fuga, el sistema debe mostrar un aviso al usuario dentro de la aplicación.

## RF-14 — Could

**Registro por voz:** El sistema podrá permitir el registro de gastos mediante voz como funcionalidad adicional, si el tiempo lo permite.

**Criterio de aceptación:** Si se implementa, el usuario debe poder dictar un gasto de forma oral y este debe procesarse mediante el mismo flujo utilizado para una entrada de texto (RF-03/RF-04).

## RF-15 — Could

**Comparación de períodos:** El sistema podrá permitir comparar los gastos entre diferentes períodos, por ejemplo, entre meses.

**Criterio de aceptación:** Si se implementa, el usuario debe poder seleccionar dos períodos y visualizar una comparación básica de sus gastos.

---

## RNF-01 — Must

**Tiempo de desarrollo:** La solución debe ser viable de desarrollar por una sola persona en 12 semanas.

**Criterio de aceptación:** El alcance definido para cada entregable debe ser realizable por un solo desarrollador, validado mediante una planificación de hitos dentro del período de 12 semanas.

## RNF-02 — Must

**Demostración:** El MVP debe poder demostrarse funcionalmente en aproximadamente 3 minutos.

**Criterio de aceptación:** Un recorrido de demostración que incluya acceso, registro de un gasto, interpretación, almacenamiento, historial, dashboard y detección de una posible fuga debe poder ejecutarse de principio a fin en aproximadamente 3 minutos.

## RNF-03 — Must

**Alcance de la IA:** La Inteligencia Artificial utilizada debe limitarse a la interpretación y clasificación de los gastos registrados.

**Criterio de aceptación:** Ninguna funcionalidad de IA implementada debe exceder las tareas de extracción de monto, categoría y descripción. Cualquier funcionalidad adicional de IA, como predicción, asesoría financiera o entrenamiento de un modelo propio, queda fuera de alcance.

## RNF-04 — Must

**Seguridad y roles:** El sistema debe controlar el acceso según el tipo de usuario autenticado.

**Criterio de aceptación:** Los usuarios deben acceder únicamente a sus funcionalidades y datos personales, mientras que las funciones administrativas deben estar disponibles exclusivamente para cuentas con rol de administrador.

## RNF-05 — Must

**Privacidad de los datos:** El sistema debe proteger la información personal y los gastos registrados por cada usuario.

**Criterio de aceptación:** Un usuario no debe poder consultar, modificar o eliminar directamente los gastos pertenecientes a otra cuenta.

---

## Won't — Explícitamente fuera de alcance del MVP

* Conexiones bancarias
* Pagos
* Transferencias
* Tarjetas
* Líneas de crédito
* Préstamos
* Inversiones
* Asesoría financiera profesional
* Entrenamiento de un modelo de IA propio
* Predicción de mercado
* Datos bancarios reales de terceros
* Notificaciones push avanzadas
* Escaneo avanzado de recibos
* Integraciones bancarias externas
* Funciones administrativas avanzadas
* Gestión de múltiples niveles de administrador

---

## Justificación de la priorización

RF-01 y RF-02 se clasifican como **Must** porque permiten establecer el acceso inicial a FUGA+ y diferenciar entre una persona que conoce la aplicación y un usuario que puede utilizar sus funcionalidades personales.

RF-03 a RF-08 se clasifican como **Must** porque forman la cadena de valor central de FUGA+: registrar un gasto, interpretarlo mediante IA, almacenarlo, consultarlo, visualizarlo y detectar posibles fugas de dinero.

RF-09 y RF-10 se clasifican como **Should** porque aportan mayor control sobre la información, pero el MVP puede demostrar su funcionamiento principal sin depender completamente de estas funcionalidades.

RF-11 y RF-12 se clasifican como **Should** porque permiten incorporar el rol administrativo y demostrar la gestión general de la aplicación, pero no son necesarias para el funcionamiento básico del usuario.

RF-13, RF-14 y RF-15 se clasifican como **Could** porque aportan funcionalidades adicionales que pueden desarrollarse si queda tiempo disponible después de completar las funcionalidades principales.

Los requisitos no funcionales RNF-01 a RNF-05 se consideran **Must** porque establecen las condiciones de viabilidad, demostración, alcance de la IA, seguridad y privacidad del proyecto.

---

## Requisitos esenciales para la demostración

Los siguientes requisitos deben estar funcionales durante la demostración de 3 minutos:

* RF-01 — Acceso público
* RF-02 — Registro e inicio de sesión
* RF-03 — Registro por texto
* RF-04 — Interpretación por IA
* RF-05 — Almacenamiento
* RF-06 — Historial
* RF-07 — Dashboard
* RF-08 — Detección de posibles fugas
* RNF-02 — Restricción de tiempo de la demostración

El panel administrativo puede mostrarse de forma breve como parte de la arquitectura general del sistema, sin que todas sus funcionalidades tengan que ser protagonistas de la demostración.

---

## Dependencias

* RF-02 depende de RF-01, ya que el visitante debe poder acceder a la opción de registro desde la parte pública.
* RF-03 depende de RF-02, ya que el registro de gastos requiere un usuario autenticado.
* RF-04 depende de RF-03, porque necesita el texto ingresado para poder interpretarlo.
* RF-05 depende de RF-04, porque se almacena el gasto después de ser interpretado.
* RF-06 depende de RF-05, porque el historial requiere datos almacenados.
* RF-07 depende de RF-05, porque el dashboard se alimenta de los gastos almacenados.
* RF-08 depende de RF-05 y de contar con suficientes gastos históricos para aplicar las reglas de detección.
* RF-09 depende de RF-05, ya que no se puede consultar información que no esté almacenada.
* RF-10 depende de RF-04 y RF-05, porque la corrección modifica información previamente interpretada y almacenada.
* RF-11 depende de la existencia de usuarios y datos almacenados en el sistema.
* RF-12 depende de RF-02 y del sistema de roles y permisos.
* RF-13 depende de RF-08, ya que necesita una posible fuga detectada para generar la alerta.
* RF-14, si se implementa, depende de RF-03 y RF-04, ya que la entrada de voz debe alimentar el mismo flujo de interpretación.
* RF-15, si se implementa, depende de RF-05 y RF-07, porque necesita datos históricos para realizar la comparación.
* RNF-02 depende de que RF-02 a RF-08 funcionen de forma integrada y fluida.

---

## Riesgos clave

1. **RF-04 — Interpretación basada en IA:** Es uno de los requisitos de mayor riesgo técnico. Extraer correctamente monto, categoría y descripción a partir de lenguaje natural informal puede requerir pruebas y ajustes.

2. **RF-08 — Identificación de fugas:** El diseño de reglas propias que generen resultados demostrables y creíbles representa un riesgo de diseño y validación. Reglas mal calibradas pueden no detectar patrones relevantes o generar falsos positivos.

3. **RNF-04 — Seguridad y roles:** La incorporación de usuarios y administrador requiere controlar correctamente la autenticación y autorización para evitar que un usuario acceda a funciones administrativas o a datos de otras cuentas.

4. **RNF-02 — Demostración de 3 minutos:** Integrar de forma fluida las funcionalidades principales en un recorrido corto puede representar un riesgo de integración y pruebas, especialmente al tratarse de un desarrollo individual.
