# Backlog de Requisitos — Release 1 · FUGA+

## Alcance del Release 1

El Release 1 contempla el flujo principal de FUGA+: una persona puede conocer la aplicación sin autenticarse, registrarse, iniciar sesión, registrar gastos mediante texto en lenguaje natural, obtener una interpretación mediante IA, confirmar y almacenar los gastos, consultar su historial, visualizar un dashboard y detectar posibles fugas mediante reglas predefinidas.

También contempla consultas y filtros básicos, corrección de categorías, estadísticas administrativas agregadas y gestión básica de usuarios.

Como funcionalidades opcionales se contemplan las alertas dentro de la aplicación, el registro por voz y la comparación entre períodos.

Quedan fuera del Release 1 las conexiones bancarias, pagos, transferencias, tarjetas, créditos, préstamos, inversiones, asesoría financiera profesional, entrenamiento de modelos de IA propios, predicción de mercado, datos bancarios reales de terceros, notificaciones push avanzadas, escaneo avanzado de recibos, integraciones bancarias externas y funciones administrativas avanzadas.

---

# Backlog priorizado (MoSCoW)

## HU-01 — Must

**Como** visitante
**quiero** conocer qué es FUGA+, cómo funciona y cuáles son sus principales funcionalidades
**para** conocer la propuesta de valor de la aplicación antes de registrarme.

```gherkin
Escenario: Consultar información pública de FUGA+

  Dado que una persona ingresa a FUGA+ sin iniciar sesión

  Cuando accede a la pantalla principal

  Entonces puede visualizar qué es FUGA+
  Y puede conocer de forma general cómo funciona el registro de gastos
  Y puede conocer las principales funcionalidades de la aplicación
  Y puede seleccionar la opción de registrarse o iniciar sesión

Escenario: Visitante intenta acceder a información privada

  Dado que la persona no ha iniciado sesión

  Cuando intenta acceder al historial, dashboard o gastos

  Entonces el sistema bloquea el acceso
  Y mantiene al visitante en la información pública o lo dirige al inicio de sesión
```

**Relacionado con:** RF-01.

---

## HU-02 — Must

**Como** visitante
**quiero** crear una cuenta e iniciar sesión
**para** acceder de forma segura a mis funcionalidades y datos personales.

```gherkin
Escenario: Crear una cuenta

  Dado que la persona se encuentra en la pantalla de registro

  Cuando ingresa un correo electrónico y una contraseña válidos

  Entonces el sistema crea la cuenta con rol Usuario
  Y permite iniciar sesión posteriormente

Escenario: Iniciar sesión correctamente

  Dado que existe una cuenta activa registrada

  Cuando el usuario ingresa credenciales válidas

  Entonces el sistema permite el acceso
  Y muestra las funcionalidades correspondientes al rol Usuario

Escenario: Credenciales inválidas

  Dado que existe una cuenta registrada

  Cuando la persona ingresa credenciales incorrectas

  Entonces el sistema rechaza el inicio de sesión
  Y muestra un mensaje de error sin indicar cuál credencial fue incorrecta

Escenario: Cuenta desactivada

  Dado que una cuenta fue desactivada por un Administrador

  Cuando la persona intenta iniciar sesión

  Entonces el sistema rechaza el acceso
```

**Relacionado con:** RF-02 y RNF-04.

---

## HU-03 — Must

**Como** usuario autenticado
**quiero** registrar un gasto escribiendo una frase en lenguaje natural
**para** ingresar mis gastos sin utilizar un formulario complejo.

```gherkin
Escenario: Registrar un gasto mediante texto

  Dado que el usuario inició sesión

  Cuando escribe "Hoy gasté $8.000 en un taxi"

  Entonces el sistema acepta el texto
  Y envía la información al proceso de interpretación
  Y muestra el resultado antes de almacenarlo

Escenario: Descartar una interpretación

  Dado que el sistema mostró una interpretación del gasto

  Cuando el usuario descarta la interpretación

  Entonces el gasto no se almacena
  Y el usuario puede ingresar una nueva frase

Escenario: Texto sin monto reconocible

  Dado que el usuario ingresó una frase sin un monto identificable

  Cuando el sistema procesa el texto

  Entonces no confirma el gasto
  Y solicita información adicional o muestra un mensaje indicando que no pudo identificar el monto
```

**Relacionado con:** RF-03.

---

## HU-04 — Must

**Como** usuario
**quiero** que la IA interprete mi gasto
**para** obtener automáticamente el monto, la categoría y la descripción.

```gherkin
Escenario: Interpretar un gasto correctamente

  Dado que el usuario ingresó "Hoy gasté $8.000 en un taxi"

  Cuando el sistema procesa el texto mediante IA

  Entonces identifica el monto 8000
  Y identifica la moneda correspondiente
  Y asigna la categoría "Transporte"
  Y genera la descripción "Taxi"
  Y muestra los tres campos antes de confirmar el gasto

Escenario: Editar la interpretación

  Dado que el sistema mostró el monto, categoría y descripción

  Cuando el usuario modifica uno de los campos

  Entonces puede revisar la información modificada antes de confirmar

Escenario: Información insuficiente

  Dado que el texto no contiene un monto reconocible

  Cuando el sistema intenta interpretarlo

  Entonces informa que no pudo identificar el monto
  Y no permite confirmar el gasto como válido
```

**Relacionado con:** RF-04 y RNF-03.

> La corrección de categoría se desarrolla específicamente en HU-09. No se agrega una funcionalidad de “revisión del día” porque no está definida en los requisitos.

---

## HU-05 — Must

**Como** usuario
**quiero** consultar mi historial de gastos
**para** revisar mis registros y saber en qué he gastado mi dinero.

```gherkin
Escenario: Consultar historial

  Dado que el usuario tiene gastos confirmados

  Cuando abre la sección "Historial"

  Entonces visualiza sus gastos ordenados del más reciente al más antiguo
  Y cada registro muestra monto, categoría, descripción y fecha

Escenario: Consultar un gasto

  Dado que el usuario visualiza su historial

  Cuando selecciona un gasto

  Entonces puede consultar el detalle del gasto

Escenario: Historial con muchos registros

  Dado que el usuario tiene numerosos gastos almacenados

  Cuando consulta el historial

  Entonces el sistema utiliza paginación o desplazamiento infinito
  Y evita cargar todas las operaciones simultáneamente

Escenario: Historial vacío

  Dado que el usuario no tiene gastos confirmados

  Cuando abre el historial

  Entonces el sistema informa que todavía no existen gastos registrados
```

**Relacionado con:** RF-06 y RNF-05.

---

## HU-06 — Must

**Como** usuario
**quiero** visualizar un dashboard con el resumen de mis gastos
**para** comprender rápidamente cómo estoy gastando mi dinero.

```gherkin
Escenario: Visualizar dashboard

  Dado que el usuario tiene gastos almacenados

  Cuando accede al dashboard

  Entonces visualiza el total gastado del período
  Y visualiza la cantidad de gastos registrados
  Y visualiza el promedio por gasto
  Y visualiza la distribución del gasto por categoría
  Y puede identificar la categoría con mayor peso

Escenario: Dashboard sin gastos

  Dado que el usuario no tiene gastos registrados

  Cuando accede al dashboard

  Entonces el sistema indica que todavía no existen datos suficientes para mostrar un resumen
```

Los datos mostrados deben corresponder únicamente a los gastos del usuario autenticado.

**Relacionado con:** RF-07 y RNF-05.

---

## HU-07 — Must

**Como** usuario
**quiero** identificar posibles fugas de dinero a partir de gastos pequeños y repetitivos
**para** reconocer patrones de gasto que podrían estar generando una fuga.

```gherkin
Escenario: Detectar una posible fuga

  Dado que el usuario tiene cinco gastos de "Café" de $4.000
  Y los gastos cumplen las condiciones definidas por una regla

  Cuando el sistema ejecuta el análisis de fugas

  Entonces identifica una posible fuga
  Y muestra cinco ocurrencias
  Y muestra un monto acumulado de $20.000
  Y muestra la categoría o descripción relacionada
  Y muestra la regla o evidencia que activó el resultado

Escenario: Datos insuficientes

  Dado que el usuario tiene menos de tres gastos registrados

  Cuando solicita el análisis de fugas

  Entonces el sistema informa que todavía no existen datos suficientes

Escenario: Análisis mediante reglas

  Dado que existen gastos almacenados

  Cuando se ejecuta el análisis

  Entonces el sistema utiliza reglas predefinidas y deterministas
  Y no utiliza IA para decidir si existe una posible fuga
```

**Relacionado con:** RF-08, RNF-03 y RNF-05.

---

## HU-08 — Should

**Como** usuario
**quiero** filtrar mis gastos por categoría y rango de fechas
**para** encontrar rápidamente registros específicos.

```gherkin
Escenario: Filtrar por categoría

  Dado que el usuario tiene gastos de diferentes categorías

  Cuando selecciona la categoría "Transporte"

  Entonces el sistema muestra únicamente sus gastos de Transporte

Escenario: Filtrar por rango de fechas

  Dado que el usuario tiene gastos registrados en diferentes fechas

  Cuando selecciona un rango de fechas

  Entonces el sistema muestra únicamente sus gastos dentro del período seleccionado

Escenario: Limpiar filtros

  Dado que el usuario tiene filtros aplicados

  Cuando selecciona la opción para limpiar los filtros

  Entonces el sistema vuelve a mostrar la lista completa de sus gastos
```

**Relacionado con:** RF-09 y RNF-05.

---

## HU-09 — Should

**Como** usuario
**quiero** corregir la categoría asignada por la IA
**para** mantener mis registros y análisis actualizados cuando la clasificación sea incorrecta.

```gherkin
Escenario: Corregir categoría antes de confirmar

  Dado que la IA mostró una categoría para un gasto

  Cuando el usuario selecciona otra categoría válida

  Entonces puede confirmar el gasto utilizando la categoría corregida
  Y el texto original permanece sin cambios

Escenario: Corregir categoría de un gasto almacenado

  Dado que existe un gasto confirmado

  Cuando el usuario cambia su categoría desde el detalle del gasto

  Entonces el sistema guarda la nueva categoría
  Y mantiene el texto original
  Y actualiza el historial
  Y actualiza los datos utilizados por el dashboard
  Y utiliza la categoría corregida en el análisis de posibles fugas
```

**Relacionado con:** RF-10.

---

## HU-10 — Should

**Como** administrador
**quiero** consultar estadísticas generales y gestionar las cuentas de usuarios
**para** supervisar el funcionamiento general de FUGA+.

```gherkin
Escenario: Consultar estadísticas administrativas

  Dado que el administrador inició sesión

  Cuando accede al panel administrativo

  Entonces puede visualizar el total de usuarios registrados
  Y puede visualizar el número total de gastos almacenados
  Y puede visualizar el promedio general de gasto
  Y puede visualizar la distribución global de gastos por categoría

Escenario: Gestionar usuarios

  Dado que el administrador se encuentra en el panel de usuarios

  Cuando consulta la lista de usuarios

  Entonces puede visualizar sus estados activo o inactivo
  Y puede activar o desactivar una cuenta

Escenario: Usuario desactivado

  Dado que el administrador desactivó una cuenta

  Cuando el usuario intenta iniciar sesión

  Entonces el sistema rechaza el acceso

Escenario: Protección de información financiera

  Dado que el administrador consulta el panel administrativo

  Entonces no puede visualizar gastos individuales
  Y no puede consultar montos o descripciones asociados a un usuario específico

Escenario: Protección de la cuenta administrativa

  Dado que el administrador está gestionando usuarios

  Cuando intenta desactivar su propia cuenta

  Entonces el sistema rechaza la operación
```

**Relacionado con:** RF-11, RF-12, RNF-04 y RNF-05.

---

## HU-11 — Could

**Como** usuario
**quiero** registrar un gasto mediante voz
**para** utilizar una alternativa al ingreso manual de texto.

```gherkin
Escenario: Registrar gasto mediante voz

  Dado que el usuario inició sesión

  Cuando activa el registro por voz y dicta una frase de gasto

  Entonces el sistema transcribe la voz
  Y envía el texto al mismo proceso de interpretación utilizado para los gastos escritos

Escenario: Error de transcripción

  Dado que la transcripción de voz no puede realizarse

  Cuando el sistema detecta el error

  Entonces informa al usuario
  Y permite continuar mediante el registro manual por texto
```

**Relacionado con:** RF-14.

---

## HU-12 — Could

**Como** usuario
**quiero** recibir una alerta dentro de la aplicación cuando se detecte una posible fuga
**para** conocer el resultado del análisis sin tener que buscarlo manualmente.

```gherkin
Escenario: Mostrar alerta de posible fuga

  Dado que el análisis de reglas detectó una nueva posible fuga

  Cuando el usuario consulta la aplicación

  Entonces puede visualizar una alerta dentro de la aplicación
  Y la alerta muestra la categoría o descripción
  Y muestra el monto acumulado
  Y muestra el número de ocurrencias

Escenario: No existen fugas

  Dado que el análisis no detectó posibles fugas

  Cuando el usuario consulta la aplicación

  Entonces no se muestra una alerta de posible fuga
```

La funcionalidad no requiere notificaciones del sistema operativo.

**Relacionado con:** RF-13.

---

## HU-13 — Could

**Como** usuario
**quiero** comparar dos períodos de gastos
**para** identificar diferencias entre mis hábitos de gasto en diferentes períodos.

```gherkin
Escenario: Comparar dos períodos

  Dado que existen gastos registrados en dos períodos diferentes

  Cuando el usuario selecciona los dos períodos

  Entonces el sistema muestra el total gastado de cada período
  Y muestra la cantidad de gastos de cada período
  Y muestra el promedio por gasto de cada período
  Y muestra la variación absoluta
  Y muestra la variación porcentual

Escenario: Período sin registros

  Dado que uno de los períodos seleccionados no tiene gastos

  Cuando el usuario realiza la comparación

  Entonces el sistema indica que ese período no tiene registros
```

**Relacionado con:** RF-15.

---

# HU-14 — Won't

**Conexiones bancarias**

Como usuario, quisiera conectar mi cuenta bancaria para registrar automáticamente mis gastos, pero esta funcionalidad queda fuera del Release 1.

---

# HU-15 — Won't

**Pagos, transferencias y tarjetas**

Las funcionalidades relacionadas con pagos, transferencias y gestión de tarjetas quedan fuera del Release 1.

---

# HU-16 — Won't

**Créditos, préstamos e inversiones**

Las funcionalidades relacionadas con líneas de crédito, préstamos e inversiones quedan fuera del Release 1.

---

# HU-17 — Won't

**Asesoría financiera profesional**

FUGA+ no proporcionará asesoría financiera profesional ni recomendaciones financieras personalizadas.

---

# HU-18 — Won't

**Entrenamiento de un modelo de IA propio**

El proyecto no contempla desarrollar ni entrenar un modelo de IA propio.

---

# HU-19 — Won't

**Predicción de mercado**

El sistema no realizará predicciones sobre mercados financieros ni comportamiento futuro de mercados.

---

# HU-20 — Won't

**Datos bancarios reales de terceros**

El sistema no utilizará datos bancarios reales de terceros.

---

# HU-21 — Won't

**Notificaciones push avanzadas**

Las notificaciones push del sistema operativo quedan fuera del Release 1.

---

# HU-22 — Won't

**Escaneo avanzado de recibos**

El procesamiento avanzado de recibos mediante imágenes queda fuera del Release 1.

---

# HU-23 — Won't

**Integraciones bancarias externas**

Las integraciones con servicios bancarios externos quedan fuera del Release 1.

---

# HU-24 — Won't

**Funciones administrativas avanzadas**

El Release 1 no contempla funciones administrativas adicionales diferentes a las definidas en RF-11 y RF-12.

---

# HU-25 — Won't

**Múltiples niveles de administrador**

El sistema tendrá únicamente el rol Administrador definido en los requisitos. No se implementarán múltiples niveles administrativos.

---

# Refinamiento y trazabilidad

Cada historia de usuario debe corresponder a los requisitos funcionales definidos para FUGA+:

| Historia | Requisito    | Prioridad |
| -------- | ------------ | --------- |
| HU-01    | RF-01        | Must      |
| HU-02    | RF-02        | Must      |
| HU-03    | RF-03        | Must      |
| HU-04    | RF-04        | Must      |
| HU-05    | RF-06        | Must      |
| HU-06    | RF-07        | Must      |
| HU-07    | RF-08        | Must      |
| HU-08    | RF-09        | Should    |
| HU-09    | RF-10        | Should    |
| HU-10    | RF-11, RF-12 | Should    |
| HU-11    | RF-14        | Could     |
| HU-12    | RF-13        | Could     |
| HU-13    | RF-15        | Could     |

RF-05 (almacenamiento persistente) se implementa como parte del flujo de confirmación del gasto de HU-03/HU-04 y sirve como dependencia de HU-05, HU-06, HU-07, HU-08 y HU-09.

Los requisitos no funcionales RNF-01 a RNF-05 actúan como restricciones transversales del conjunto de historias y no necesitan convertirse individualmente en historias de usuario.

---

# Requisitos esenciales para la demostración

La demostración principal de aproximadamente 3 minutos debe mostrar:

* HU-01 — Acceso público.
* HU-02 — Registro e inicio de sesión.
* HU-03 — Registro de gasto mediante texto.
* HU-04 — Interpretación mediante IA.
* Almacenamiento persistente del gasto.
* HU-05 — Historial.
* HU-06 — Dashboard.
* HU-07 — Detección de posibles fugas.

La ruta principal es:

**HU-01 → HU-02 → HU-03 → HU-04 → almacenamiento → HU-05 → HU-06 → HU-07**

El panel administrativo de HU-10 puede mostrarse como funcionalidad complementaria, pero no forma parte de la ruta crítica de la demostración.

---

# Dependencias

* HU-02 depende de HU-01.
* HU-03 depende de HU-02.
* HU-04 depende de HU-03.
* El almacenamiento persistente depende de la confirmación de la interpretación de HU-04.
* HU-05 depende del almacenamiento persistente.
* HU-06 depende del almacenamiento persistente.
* HU-07 depende del almacenamiento persistente y de contar con suficientes gastos históricos.
* HU-08 depende del historial y de los gastos almacenados.
* HU-09 depende de la interpretación de HU-04 y de los gastos almacenados.
* HU-10 depende de autenticación, roles y datos almacenados.
* HU-11 depende de HU-03 y HU-04.
* HU-12 depende de HU-07.
* HU-13 depende de los gastos almacenados y de las métricas utilizadas por el dashboard.
* Las historias Won't quedan fuera del Release 1.

---

# Riesgos clave

1. **HU-04 — Interpretación mediante IA:** la extracción de monto, moneda, categoría y descripción puede requerir validaciones y pruebas con diferentes formas de lenguaje natural.

2. **HU-07 — Detección de posibles fugas:** las reglas deben ser claras, deterministas y explicables para evitar resultados inconsistentes.

3. **HU-02 y HU-10 — Autenticación y roles:** deben mantenerse correctamente separados los permisos de Visitante, Usuario y Administrador.

4. **HU-06 — Dashboard:** los cálculos deben utilizar exclusivamente los gastos del usuario correspondiente.

5. **RNF-02 — Demostración:** la ruta crítica debe estar integrada y probada de extremo a extremo para mantenerse dentro del tiempo establecido.

6. **RNF-05 — Privacidad:** todas las consultas de gastos deben estar aisladas por propietario y el Administrador debe recibir únicamente información agregada.
