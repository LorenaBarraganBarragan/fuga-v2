# Priorización de Requisitos (MoSCoW) — FUGA+

## RF-01 — Must
**Registro de gastos por texto:** El sistema debe permitir registrar un gasto escribiendo una descripción en lenguaje natural.
**Criterio de aceptación:** Al ingresar un texto como "Hoy gasté $8.000 en un taxi", el sistema debe aceptar la entrada y enviarla al motor de interpretación.

## RF-02 — Must
**Interpretación basada en IA:** El sistema debe interpretar la información registrada e identificar elementos como monto, categoría y descripción.
**Criterio de aceptación:** A partir del texto ingresado en RF-01, el sistema debe extraer el monto (ej. $8.000), asignar una categoría (ej. "Transporte") y generar una descripción resumida, mostrando el resultado al usuario.

## RF-03 — Must
**Almacenamiento de gastos:** El sistema debe almacenar los gastos registrados para su consulta posterior.
**Criterio de aceptación:** Tras confirmar la interpretación de RF-02, el gasto debe quedar guardado de forma persistente y recuperable en sesiones posteriores.

## RF-04 — Must
**Historial de gastos:** El sistema debe permitir visualizar los gastos registrados mediante un historial.
**Criterio de aceptación:** El usuario debe poder acceder a una lista cronológica de los gastos almacenados, mostrando al menos fecha, monto, categoría y descripción de cada uno.

## RF-05 — Must
**Dashboard:** El sistema debe mostrar un dashboard simple con información sobre los gastos registrados.
**Criterio de aceptación:** El dashboard debe mostrar, como mínimo, un resumen visual (ej. totales por categoría) que se actualice automáticamente al registrar un nuevo gasto.

## RF-06 — Must
**Identificación de posibles fugas de dinero:** El sistema debe analizar los gastos mediante reglas propias para identificar posibles fugas de dinero, principalmente relacionadas con gastos pequeños y repetitivos.
**Criterio de aceptación:** Al detectar un patrón que cumpla con una regla predefinida (ej. varios gastos pequeños en la misma categoría dentro de un período), el sistema debe señalar visualmente ese patrón como una posible fuga.

## RF-07 — Should
**Consultas básicas:** El sistema debe permitir realizar consultas básicas sobre los gastos registrados.
**Criterio de aceptación:** El usuario debe poder filtrar o consultar sus gastos por al menos un criterio simple (ej. categoría o rango de fechas) y obtener un resultado coherente con los datos almacenados.

## RF-08 — Could
**Registro por voz:** El sistema podrá permitir el registro de gastos mediante voz como funcionalidad adicional, si el tiempo lo permite.
**Criterio de aceptación:** Si se implementa, el usuario debe poder dictar un gasto de forma oral y que este se procese igual que una entrada de texto (RF-01/RF-02).

## RNF-01 — Must
**Tiempo de desarrollo:** La solución debe ser viable de desarrollar por una sola persona en 12 semanas.
**Criterio de aceptación:** El alcance definido para cada entregable debe ser realizable por un solo desarrollador, validado mediante una planificación de hitos dentro del período de 12 semanas.

## RNF-02 — Must
**Demostración:** El MVP debe poder demostrarse funcionalmente en aproximadamente 3 minutos.
**Criterio de aceptación:** Un recorrido de demostración (registrar gastos, ver historial, ver dashboard, ver una fuga detectada) debe poder ejecutarse de principio a fin en un máximo de 3 minutos.

## RNF-03 — Must
**Alcance de la IA:** La Inteligencia Artificial utilizada debe limitarse a la interpretación y clasificación de los gastos registrados.
**Criterio de aceptación:** Ninguna funcionalidad de IA implementada debe exceder las tareas de extracción de monto/categoría/descripción; cualquier funcionalidad adicional de IA (predicción, asesoría, etc.) queda fuera de alcance.

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
- Notificaciones avanzadas
- Escaneo avanzado de recibos
- Integraciones bancarias externas

---

## Justificación de la priorización

RF-01 a RF-06 se marcan como **Must** porque forman la cadena de valor central de FUGA+: sin registro por texto (RF-01) no hay dato que interpretar (RF-02); sin interpretación no hay nada útil que almacenar (RF-03), mostrar en historial (RF-04) o en dashboard (RF-05); y sin datos clasificados no es posible aplicar las reglas de detección de fugas (RF-06), que es el diferenciador central del producto. RF-07 (consultas básicas) se clasifica como **Should**: aporta valor funcional, pero el MVP puede demostrarse y funcionar sin un motor de consultas dedicado, ya que el historial y el dashboard ya exponen la información. RF-08 (voz) es explícitamente **Could**, tal como lo define el propio contexto del proyecto ("si el tiempo lo permite"). Las restricciones no funcionales (RNF-01 a RNF-03) se marcan como **Must** porque no son características sino condiciones de viabilidad del proyecto: si no se cumplen, el proyecto no es ejecutable en el formato solo/12 semanas ni demostrable en 3 minutos.

## Requisitos esenciales para la demostración

Los siguientes requisitos deben estar funcionales durante la demostración de 3 minutos:
- RF-01 (registro por texto)
- RF-02 (interpretación por IA)
- RF-03 (almacenamiento)
- RF-04 (historial)
- RF-05 (dashboard)
- RF-06 (detección de fugas)
- RNF-02 (restricción de tiempo de la propia demostración)

## Dependencias

- RF-02 depende de RF-01 (necesita el texto ingresado para poder interpretarlo).
- RF-03 depende de RF-02 (se almacena el gasto ya interpretado/clasificado).
- RF-04 depende de RF-03 (el historial requiere datos ya almacenados).
- RF-05 depende de RF-03 (el dashboard se alimenta de los datos almacenados y clasificados).
- RF-06 depende de RF-03 y de contar con un conjunto de gastos históricos suficiente (RF-04) para poder aplicar las reglas de detección.
- RF-07 depende de RF-03 (no se puede consultar lo que no está almacenado).
- RF-08, si se implementa, depende de RF-01 y RF-02 (la entrada por voz debería alimentar el mismo motor de interpretación que la entrada por texto).
- RNF-02 depende de que RF-01 a RF-06 funcionen de forma integrada y fluida.

## Riesgos clave

1. **RF-02 — Interpretación basada en IA:** Es el requisito de mayor riesgo técnico. Extraer correctamente monto, categoría y descripción a partir de lenguaje natural informal (distintos formatos de moneda, abreviaciones, ambigüedad) puede tomar más tiempo de lo previsto y afecta directamente a todos los requisitos posteriores.
2. **RF-06 — Identificación de fugas:** El diseño de reglas propias que generen resultados demostrables y creíbles en un conjunto de datos limitado (dado el desarrollo individual y el tiempo acotado) representa un riesgo de diseño y de validación, ya que reglas mal calibradas pueden no detectar nada relevante o generar falsos positivos.
3. **RNF-02 — Demostración de 3 minutos:** Integrar de forma fluida y sin errores todos los requisitos Must (RF-01 a RF-06) en un flujo corto y coherente es un riesgo de gestión del proyecto, especialmente al ser un desarrollo individual con tiempo limitado para pruebas de integración.