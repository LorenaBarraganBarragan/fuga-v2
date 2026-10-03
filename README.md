# FUGA+

**FUGA+** es una aplicación móvil para el control de gastos personales, dirigida principalmente a jóvenes y estudiantes.

Permite registrar gastos utilizando lenguaje natural, por ejemplo:

> "Hoy gasté $8.000 en un taxi"

La aplicación interpreta la información del gasto mediante IA, permite al usuario revisarla antes de confirmarla y posteriormente organiza los datos para consultar el historial y visualizar estadísticas.

Además, FUGA+ identifica posibles **fugas de dinero** mediante reglas definidas por el proyecto, enfocadas en gastos pequeños y repetitivos.

**Repositorio:** [GitHub](https://github.com/LorenaBarraganBarragan/fuga-v2)

---

## Problema

Los gastos pequeños del día a día pueden pasar desapercibidos y acumularse con el tiempo.

A partir de la entrevista realizada a un usuario potencial, se identificó que registrar manualmente cada gasto puede generar olvido y pérdida de interés en el seguimiento de las finanzas personales.

FUGA+ busca reducir esta fricción permitiendo registrar los gastos de una manera más natural y sencilla.

[Ver entrevista](docs/entrevista-real.md)

---

## Objetivo

Desarrollar un MVP que facilite el registro y seguimiento de gastos personales mediante lenguaje natural e inteligencia artificial.

El proyecto contempla:

* Registro de gastos.
* Interpretación de la información mediante IA.
* Confirmación y almacenamiento de los gastos.
* Historial de movimientos.
* Visualización de estadísticas.
* Identificación de posibles fugas de dinero mediante reglas.

El proyecto se desarrolla de manera individual en un período académico de 12 semanas.

---

## Público objetivo

FUGA+ está dirigido principalmente a **jóvenes y estudiantes** que desean organizar sus gastos cotidianos y comprender mejor sus hábitos de consumo sin utilizar herramientas financieras complejas.

El sistema contempla diferentes roles de usuario, cuyos permisos y responsabilidades se encuentran definidos en la documentación de requisitos.

[Ver requisitos](docs/requisitos.md)

---

## Propuesta de valor

FUGA+ busca hacer que registrar un gasto sea más sencillo que utilizar formularios tradicionales.

El usuario puede expresar un gasto utilizando una frase cotidiana. La IA interpreta la información y presenta los datos identificados para que el usuario pueda revisarlos y corregirlos antes de confirmar el registro.

A partir de los gastos registrados, FUGA+ aplica reglas propias para identificar posibles patrones de gastos pequeños y repetitivos que podrían representar una fuga de dinero.

La detección de fugas utiliza **reglas deterministas y explicables**, no inteligencia artificial.

---

## Funcionalidades principales

El alcance del proyecto contempla las siguientes funcionalidades:

* Información pública sobre FUGA+.
* Registro e inicio de sesión.
* Registro de gastos mediante lenguaje natural.
* Interpretación del gasto mediante IA.
* Confirmación y almacenamiento de gastos.
* Consulta del historial.
* Visualización de estadísticas.
* Detección de posibles fugas de dinero.
* Corrección de información de los gastos.
* Funcionalidades adicionales definidas en el Release 1.

El detalle completo de los requisitos, historias de usuario y prioridades se encuentra en la documentación del proyecto.

[Ver requisitos](docs/requisitos.md)
[Ver requisitos priorizados](docs/respuestas-ia/salida-requerimientos-priorizados.md)

---

## Alcance

### Incluido

El MVP se centra en la gestión básica de gastos personales, su interpretación mediante lenguaje natural, consulta de información y detección de posibles fugas mediante reglas.

### Fuera del alcance principal

El proyecto no contempla como parte del alcance principal:

* Conexiones bancarias.
* Pagos y transferencias.
* Créditos o préstamos.
* Inversiones.
* Asesoría financiera profesional.
* Entrenamiento de un modelo de IA propio.
* Integraciones bancarias externas.

El alcance puede evolucionar durante el desarrollo académico y se mantiene documentado en los requisitos del proyecto.

---

## Tecnologías

La arquitectura de FUGA+ contempla tecnologías para la aplicación móvil, backend, inteligencia artificial, almacenamiento, autenticación e infraestructura.

Entre las tecnologías definidas para la solución se encuentran:

* **React Native + TypeScript** — aplicación móvil.
* **Python + FastAPI** — backend y API.
* **OpenAI API** — interpretación del texto de los gastos.
* **MongoDB** — almacenamiento de información.
* **MongoDB Aggregation** — procesamiento de estadísticas.
* **Redis** — almacenamiento temporal y caché.
* **JWT** — autenticación y autorización.
* **Docker + Docker Compose** — infraestructura y ejecución de servicios.
* **OpenAPI / Swagger** — documentación de la API.
* **Git + GitHub** — control de versiones.

Estas tecnologías corresponden a la arquitectura definida para FUGA+ y su implementación puede evolucionar durante el desarrollo.

[Ver arquitectura](docs/architecture.md)

---

## Arquitectura

FUGA+ se plantea como una solución compuesta por una aplicación móvil, un backend y servicios de datos e infraestructura.

De forma general, el flujo es:

**Aplicación móvil → Backend → Servicios de IA y lógica de negocio → Datos**

La aplicación móvil permite la interacción con el usuario. El backend gestiona las operaciones del sistema, coordina la interpretación de los gastos y aplica las reglas de negocio. Los servicios de datos permiten almacenar y procesar la información necesaria para el funcionamiento de la aplicación.

La arquitectura detallada se encuentra en la documentación y en los diagramas del proyecto.

[Ver arquitectura](docs/architecture.md)

[Ver diagramas](docs/diagramas/)

---

## Documentación

### Requisitos y análisis

* [Requisitos del proyecto](docs/requisitos.md)
* [Entrevista real](docs/entrevista-real.md)
* [Visión del proyecto](docs/respuestas-ia/salida-vision.md)
* [Análisis competitivo](docs/respuestas-ia/salida-analisis-competitivo.md)
* [Requisitos priorizados](docs/respuestas-ia/salida-requerimientos-priorizados.md)

### Arquitectura y diseño

* [Arquitectura](docs/architecture.md)
* [Esquema de manifiestos](docs/manifest_schema.md)
* [Diagramas](docs/diagramas/)
* [Prompts de análisis y diseño](docs/prompts-diseño/)

---

## Uso de inteligencia artificial

La inteligencia artificial forma parte del proceso de análisis, diseño y definición de FUGA+.

Durante el desarrollo se ha utilizado para apoyar actividades como:

* Análisis de la visión del proyecto.
* Análisis competitivo.
* Priorización de requisitos.
* Apoyo en el diseño del sistema.
* Interpretación de los gastos escritos en lenguaje natural.

La IA utilizada dentro de la funcionalidad principal de FUGA+ se limita a la interpretación de la información proporcionada por el usuario.

La detección de posibles fugas de dinero se realiza mediante **reglas definidas por el proyecto**.

---

## Estado del proyecto

FUGA+ se encuentra en **desarrollo académico, en fase de diseño y documentación**.

Actualmente se han trabajado aspectos como:

* Definición del problema.
* Identificación del usuario objetivo.
* Visión y propuesta de valor.
* Análisis competitivo.
* Requisitos.
* Priorización del MVP.
* Arquitectura.
* Diseño del modelo del sistema.
* Diagramas de diseño.

La implementación funcional del MVP continuará de acuerdo con el proceso de desarrollo definido para el proyecto.

---

## Autor

**Lorena Barragán**

Proyecto académico individual — Ingeniería de Sistemas.
