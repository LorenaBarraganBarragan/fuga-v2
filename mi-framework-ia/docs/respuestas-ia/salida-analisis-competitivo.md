# Análisis Competitivo: FUGA+

## Competidor 1: Cleo

**Tipo de competencia:** Directa (en el componente de IA conversacional) e indirecta (en el modelo de negocio, ya que incluye productos financieros fuera del alcance de FUGA+).
**Público objetivo:** Usuarios jóvenes; es reconocida por su tono informal y su enfoque en audiencias más jóvenes.
**Método de registro de gastos:** No manual mediante texto libre del usuario: requiere que el usuario conecte sus cuentas bancarias, y a partir de ahí Cleo rastrea automáticamente los patrones de gasto.
**Uso de Inteligencia Artificial:** Utiliza procesamiento de lenguaje natural y machine learning para analizar los datos bancarios del usuario y ofrecer orientación financiera personalizada mediante una interfaz conversacional.
**Análisis de gastos:** La IA identifica patrones, señala categorías de alto gasto y genera resúmenes personalizados semanales o mensuales; además detecta patrones recurrentes como suscripciones o arriendos.
**Fortalezas:** Interfaz conversacional atractiva para público joven; detección automática de patrones recurrentes; tono humorístico ("roast mode") que aumenta el engagement.
**Limitaciones frente a FUGA+:** Depende de la conexión bancaria (no ofrece registro por texto libre sin vincular cuentas); su modelo de negocio incluye adelantos de efectivo y otros productos financieros, elementos fuera del alcance del MVP de FUGA+. No está enfocada específicamente en la detección de "fugas" por gastos pequeños y recurrentes como concepto central del producto.

## Competidor 2: PocketGuard

**Tipo de competencia:** Indirecta.
**Público objetivo:** Usuarios que buscan una herramienta de presupuesto automatizada; [UNCONFIRMED] si tiene un enfoque específico en jóvenes o estudiantes.
**Método de registro de gastos:** No manual mediante texto libre: requiere conectar cuentas corrientes, de crédito y ahorro, tras lo cual importa y categoriza automáticamente las transacciones.
**Uso de Inteligencia Artificial:** Utiliza un algoritmo para categorizar transacciones y un algoritmo que detecta suscripciones escaneando cargos recurrentes de ciertos proveedores; no se confirma el uso de procesamiento de lenguaje natural para entrada de datos [UNCONFIRMED].
**Análisis de gastos:** Calcula un "Leftover" (dinero disponible) restando cuentas recurrentes, gastos programados y ahorros, y escanea las transacciones para detectar cargos recurrentes y suscripciones olvidadas.
**Fortalezas:** Detección automática de suscripciones y gastos recurrentes; interfaz simple orientada a un solo número clave de gasto disponible.
**Limitaciones frente a FUGA+:** Depende completamente de la vinculación bancaria (fuera del alcance del MVP de FUGA+); la versión gratuita está limitada a dos cuentas vinculadas y dos categorías de presupuesto; no permite registrar gastos mediante lenguaje natural ni está enfocada en estudiantes.

## Competidor 3: Spendee

**Tipo de competencia:** Directa.
**Público objetivo:** Incluye explícitamente a estudiantes que comparten gastos, además de familias y roomies.
**Método de registro de gastos:** Manual: la versión gratuita incluye entradas de compra manuales, con selección de categoría, descripción y la posibilidad de agregar fotos.
**Uso de Inteligencia Artificial:** [UNCONFIRMED]. No se encontró evidencia de interpretación por lenguaje natural; la categorización es manual o por reglas definidas por el usuario.
**Análisis de gastos:** Ofrece un gráfico de línea de ingresos/gastos y un gráfico circular de en qué se gastó el dinero; también permite crear presupuestos detallados por categoría con notificaciones de progreso.
**Fortalezas:** Diseño visual atractivo y simple; billeteras compartidas; buena adopción entre estudiantes.
**Limitaciones frente a FUGA+:** El registro es completamente manual (sin interpretación de lenguaje natural), lo que implica más fricción por transacción; no cuenta con un mecanismo específico para identificar "fugas de dinero" por gastos pequeños y recurrentes, sino solo visualización general de categorías.

## Oportunidades de diferenciación

1. **Registro por lenguaje natural sin conexión bancaria:** Ninguno de los tres competidores combina interpretación de texto libre con un modelo que no dependa de vincular cuentas bancarias (Cleo y PocketGuard requieren esa conexión; Spendee usa formularios manuales estructurados). FUGA+ puede ocupar ese espacio intermedio: rapidez de registro sin exponer datos bancarios.
2. **Foco explícito en "fugas" de gastos pequeños y recurrentes:** Aunque PocketGuard detecta suscripciones, lo hace sobre datos bancarios y con foco en cancelación de servicios; ninguno de los tres construye su propuesta de valor central alrededor del concepto de "fuga" aplicado a micro-gastos cotidianos (café, transporte, delivery) como hábito a corregir.
3. **Simplicidad para estudiantes sin fricción de reglas o vínculos bancarios:** Spendee, aunque manual, exige seleccionar categoría y campos por formulario; FUGA+ puede reducir esa fricción a una sola frase en lenguaje natural, ideal para un uso rápido y frecuente por parte de jóvenes y estudiantes.

**Principal ventaja competitiva de FUGA+:**

Frente a estos competidores, la ventaja de FUGA+ radica en combinar el registro por lenguaje natural (que Cleo sí ofrece, pero atado a datos bancarios) con reglas propias orientadas específicamente a detectar fugas por gastos pequeños y recurrentes (que PocketGuard aborda solo parcialmente vía suscripciones bancarias), todo sin requerir vinculación bancaria, lo cual reduce la barrera de entrada y la fricción de privacidad para estudiantes.

## Conclusión

FUGA+ no compite directamente en ninguna de las tres dimensiones por separado, pero sí en su combinación: entrada por lenguaje natural, sin vínculo bancario, y foco explícito en fugas por micro-gastos. Esa combinación no fue identificada en ninguno de los tres competidores analizados, lo que representa una oportunidad de nicho viable para un MVP desarrollado por una sola persona en 12 semanas, sin necesidad de replicar funcionalidades bancarias.