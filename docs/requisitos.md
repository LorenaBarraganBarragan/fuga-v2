# Backlog de Requisitos — Release 1 · FUGA+

## Alcance del Release 1 (a partir de la visión y el MVP)

El Release 1 contempla el flujo principal de FUGA+: una persona puede conocer la aplicación sin registrarse, crear una cuenta, registrar gastos mediante texto, utilizar IA para interpretarlos, almacenarlos, consultar su historial, visualizar un dashboard, detectar posibles fugas mediante reglas propias y realizar consultas básicas.

También se contempla un rol de administrador para consultar estadísticas generales y gestionar usuarios.

Quedan fuera del Release 1 las integraciones bancarias, pagos, transferencias, notificaciones avanzadas y otras funcionalidades que no sean necesarias para demostrar el MVP. El registro por voz se mantiene como funcionalidad adicional si queda tiempo disponible.

---

# Backlog priorizado (MoSCoW)

## HU-01 — Must

**Como** visitante **quiero** conocer qué es FUGA+, cómo funciona y cuáles son sus principales funcionalidades **para** decidir si quiero registrarme.

```gherkin
Escenario: Consultar información de FUGA+

  Dado que una persona ingresa a FUGA+ sin iniciar sesión

  Cuando accede a la pantalla principal

  Entonces puede visualizar información básica sobre la aplicación

  Y puede conocer de forma general cómo funciona el registro de gastos

  Y puede seleccionar la opción de registrarse o iniciar sesión
```

---

## HU-02 — Must

**Como** visitante **quiero** crear una cuenta e iniciar sesión **para** acceder de forma segura a mis funcionalidades y datos personales.

```gherkin
Escenario: Crear una cuenta

  Dado que la persona se encuentra en la pantalla de registro

  Cuando ingresa los datos requeridos y confirma el registro

  Entonces el sistema crea la cuenta

  Y permite acceder a las funcionalidades de usuario

Escenario: Iniciar sesión

  Dado que existe una cuenta registrada

  Cuando el usuario ingresa sus credenciales correctas

  Entonces el sistema permite el acceso

  Y muestra la aplicación correspondiente a su rol
```

---

## HU-03 — Must

**Como** usuario **quiero** registrar un gasto escribiendo una descripción en lenguaje natural **para** no perder tiempo llenando formularios.

```gherkin
Escenario: Registrar un gasto válido

  Dado que el usuario está en la pantalla de registro

  Cuando escribe "Hoy gasté $8.000 en un taxi" y confirma

  Entonces el sistema acepta la entrada

  Y envía el texto al motor de interpretación

  Y el usuario puede continuar con el procesamiento del gasto

Escenario: Registrar un texto sin información de gasto

  Dado que el usuario está en la pantalla de registro

  Cuando escribe un texto sin valor numérico reconocible, como "hola"

  Entonces el sistema no crea un gasto

  Y muestra un mensaje indicando que debe incluir un valor
```

---

## HU-04 — Must

**Como** usuario **quiero** que la IA interprete y clasifique automáticamente mi gasto **para** no tener que categorizar manualmente cada registro.

```gherkin
Escenario: Clasificación automática exitosa

  Dado que el usuario registró el texto "Hoy gasté $8.000 en un taxi"

  Cuando el sistema procesa el texto

  Entonces identifica el valor 8000

  Y asigna la categoría "Transporte"

  Y genera la descripción "Taxi"

Escenario: Clasificación con información insuficiente

  Dado que el texto registrado es ambiguo, como "gasté algo por ahí"

  Cuando el sistema no logra identificar un valor claro

  Entonces el sistema no asigna una categoría definitiva

  Y permite que el usuario complete o corrija la información manualmente

Escenario: Revisión en lote al final del día

  Dado que el usuario registró varios gastos durante el día

  Cuando abre la vista de "revisión del día"

  Entonces puede visualizar los gastos del día con sus categorías asignadas

  Y puede corregir únicamente los que estén clasificados incorrectamente
```

*Este criterio mantiene el ajuste realizado a partir de la entrevista real: el usuario puede revisar varios gastos juntos al final del día en lugar de confirmar cada categoría inmediatamente.*

---

## HU-05 — Must

**Como** usuario **quiero** consultar el historial de mis gastos registrados **para** revisar en qué se ha ido mi dinero.

```gherkin
Escenario: Ver historial con gastos registrados

  Dado que el usuario tiene al menos un gasto registrado

  Cuando abre la sección "Historial"

  Entonces ve una lista de sus gastos ordenada por fecha

  Y cada registro muestra al menos valor, categoría y descripción

Escenario: Historial vacío

  Dado que el usuario no ha registrado ningún gasto

  Cuando abre la sección "Historial"

  Entonces ve un mensaje indicando que aún no hay gastos registrados
```

---

## HU-06 — Must

**Como** usuario **quiero** ver un dashboard sencillo con el resumen de mis gastos **para** entender de un vistazo cómo he gastado mi dinero.

```gherkin
Escenario: Visualizar resumen de gastos

  Dado que el usuario tiene gastos registrados

  Cuando abre el dashboard

  Entonces visualiza un resumen de sus gastos

  Y puede ver los totales agrupados por categoría

Escenario: Dashboard sin gastos

  Dado que el usuario no tiene gastos registrados

  Cuando abre el dashboard

  Entonces el sistema muestra un estado indicando que todavía no existen datos para analizar
```

---

## HU-07 — Must

**Como** usuario **quiero** que el sistema identifique posibles fugas de dinero en gastos pequeños y repetitivos **para** detectar patrones que no había visto.

```gherkin
Escenario: Detectar una posible fuga

  Dado que el usuario tiene 3 o más gastos similares en la misma categoría

  Y los gastos se encuentran dentro de un periodo corto

  Cuando el sistema aplica las reglas de detección

  Entonces los gastos cumplen la condición definida

  Y el sistema los marca como "posible fuga"

  Y la información se muestra en el dashboard
```

La detección se realizará mediante **reglas definidas por el proyecto**, no mediante una valoración de la IA sobre si un gasto es bueno o malo.

---

## HU-08 — Should

**Como** usuario **quiero** realizar consultas básicas sobre mis gastos por categoría o rango de fechas **para** encontrar información específica sin revisar todo el historial.

```gherkin
Escenario: Filtrar gastos por categoría

  Dado que el usuario tiene gastos registrados en varias categorías

  Cuando selecciona la categoría "Transporte"

  Entonces el sistema muestra únicamente los gastos correspondientes a esa categoría

Escenario: Filtrar gastos por rango de fechas

  Dado que el usuario tiene gastos registrados en diferentes fechas

  Cuando selecciona un rango de fechas

  Entonces el sistema muestra únicamente los gastos correspondientes al periodo seleccionado
```

---

## HU-09 — Should

**Como** usuario **quiero** corregir manualmente la categoría que la IA asignó a un gasto **para** mantener mi historial preciso cuando la IA se equivoque.

```gherkin
Escenario: Corregir una categoría

  Dado que un gasto tiene una categoría incorrecta

  Cuando el usuario selecciona una nueva categoría y guarda el cambio

  Entonces el sistema actualiza la categoría del gasto

  Y el cambio se refleja en el historial

  Y el dashboard utiliza la nueva categoría
```

---

## HU-10 — Should

**Como** administrador **quiero** consultar estadísticas generales y gestionar los usuarios registrados **para** supervisar el funcionamiento de FUGA+.

```gherkin
Escenario: Consultar estadísticas generales

  Dado que el administrador inició sesión con permisos administrativos

  Cuando accede al panel de administración

  Entonces puede visualizar estadísticas generales

  Y puede consultar información como cantidad de usuarios registrados

  Y puede consultar estadísticas generales de uso de la aplicación

Escenario: Gestionar un usuario

  Dado que el administrador se encuentra en el panel de usuarios

  Cuando consulta la lista de usuarios

  Entonces puede visualizar las cuentas registradas

  Y puede activar o desactivar una cuenta según sea necesario
```

El administrador trabajará principalmente con **información general y estadísticas**, evitando exponer innecesariamente los detalles financieros personales de los usuarios.

---

## HU-11 — Could

**Como** usuario **quiero** registrar un gasto usando mi voz en lugar de texto **para** hacerlo más rápido cuando estoy ocupado.

```gherkin
Escenario: Registrar un gasto mediante voz

  Dado que el usuario activa la opción de registro por voz

  Cuando dicta un gasto

  Entonces el sistema transcribe el contenido

  Y procesa el texto utilizando el mismo flujo de interpretación de HU-04
```

Esta funcionalidad solo se implementará si queda tiempo después de completar las funcionalidades Must y Should.

---

## HU-12 — Won't (explícitamente fuera de este Release)

**Como** usuario **quisiera** conectar mi cuenta bancaria para que mis gastos se registren automáticamente, **pero** esta funcionalidad no se desarrollará en el Release 1 porque requiere integraciones bancarias externas y aumenta considerablemente el alcance y riesgo del proyecto.

---

# Refinamiento crítico (checklist INVEST aplicado)

| Problema detectado                                                                                                                                           | Corrección aplicada                                                                                            | Justificación (INVEST)                                                                              |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| El sistema originalmente comenzaba directamente con el registro de gastos y no contemplaba una experiencia para una persona que aún no conoce la aplicación. | Se agregó HU-01 para permitir que un visitante conozca FUGA+ antes de registrarse.                             | **Valuable** — permite presentar el propósito de la aplicación y facilitar la conversión a usuario. |
| No estaba definido cómo una persona pasaba de visitante a usuario.                                                                                           | Se agregó HU-02 para crear cuenta e iniciar sesión.                                                            | **Testable** — permite verificar claramente el registro, autenticación y acceso.                    |
| El requisito original de interpretación mediante IA estaba separado del registro, pero no contemplaba información insuficiente.                              | HU-03 maneja la entrada y HU-04 maneja la interpretación, incluyendo un escenario de información insuficiente. | **Independent / Testable** — cada funcionalidad tiene un objetivo y comportamiento verificable.     |
| El dashboard no tenía estados observables para validar su funcionamiento.                                                                                    | HU-06 incluye tanto el dashboard con datos como el estado sin gastos.                                          | **Testable** — existen condiciones claras para comprobar el resultado.                              |
| La detección de fugas podía interpretarse como un juicio de la IA sobre los gastos.                                                                          | HU-07 utiliza una regla explícita basada en gastos similares y utiliza el término "posible fuga".              | **Valuable / Negotiable** — detecta patrones sin afirmar que un gasto sea innecesario.              |
| No existía un rol administrativo definido.                                                                                                                   | Se agregó HU-10 para estadísticas generales y gestión básica de usuarios.                                      | **Valuable / Testable** — establece claramente qué puede hacer el administrador.                    |
| El registro por voz podía convertirse en una funcionalidad demasiado grande.                                                                                 | HU-11 se limita a transcribir la voz y reutilizar el flujo de texto existente.                                 | **Small** — evita crear un sistema de procesamiento diferente.                                      |
| La conexión bancaria tenía un impacto demasiado grande para el MVP.                                                                                          | Se mantiene como HU-12 Won't.                                                                                  | **Negotiable / Small** — queda explícitamente fuera del Release 1.                                  |

---

# Requisitos esenciales para la demostración

Las funcionalidades principales que deben estar disponibles durante la demostración de 3 minutos son:

* HU-01 — Acceso público y presentación de FUGA+
* HU-02 — Registro e inicio de sesión
* HU-03 — Registro de gasto por texto
* HU-04 — Interpretación mediante IA
* HU-05 — Historial
* HU-06 — Dashboard
* HU-07 — Detección de posibles fugas

El panel administrativo de HU-10 podrá mostrarse brevemente como una funcionalidad complementaria del sistema.

---

# Dependencias

* HU-02 depende de HU-01, porque el visitante debe poder acceder al registro desde la parte pública.
* HU-03 depende de HU-02, porque el registro de gastos requiere un usuario autenticado.
* HU-04 depende de HU-03, porque la IA necesita el texto ingresado.
* HU-05 depende de HU-04 y del almacenamiento de los datos.
* HU-06 depende de los gastos almacenados.
* HU-07 depende de los gastos almacenados y de contar con suficientes registros históricos para aplicar las reglas.
* HU-08 depende del historial y de los datos almacenados.
* HU-09 depende de HU-04 y de los gastos almacenados.
* HU-10 depende del sistema de autenticación, roles y datos generales almacenados.
* HU-11 depende de HU-03 y HU-04, porque la entrada de voz debe reutilizar el flujo de registro e interpretación.
* HU-12 queda explícitamente fuera del alcance del Release 1.

---

# Riesgos clave

1. **HU-04 — Interpretación basada en IA:** Extraer correctamente monto, categoría y descripción a partir de lenguaje natural puede requerir pruebas y ajustes.

2. **HU-07 — Identificación de posibles fugas:** Las reglas deben estar suficientemente calibradas para detectar patrones demostrables sin generar demasiados falsos positivos.

3. **HU-02 — Autenticación y roles:** La incorporación de usuarios y administrador requiere controlar correctamente los permisos para evitar accesos indebidos.

4. **HU-10 — Panel administrativo:** Se debe evitar que las funcionalidades administrativas aumenten demasiado el alcance del MVP.

5. **HU-06 — Dashboard:** El dashboard debe integrarse correctamente con los datos almacenados para que los cambios en los gastos se reflejen de forma coherente.

---

*Documento actualizado a partir de la visión y requisitos de FUGA+, incorporando acceso público, autenticación de usuarios y rol administrativo, sin modificar el objetivo principal del MVP.*
