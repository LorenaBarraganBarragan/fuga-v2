Act as a senior software architect and UML component-diagram specialist.

Your task is to create ONLY the component diagram for my project FUGA+.

IMPORTANT: The project already contains the folder:

`docs/diagramas/`

Do NOT create this folder.

You must create ONLY this file:

`docs/diagramas/diagrama-componentes.drawio`

Do not create any other diagram, file, document, image, code file, or documentation.

---

# PROJECT CONTEXT

FUGA+ is a mobile application designed mainly for young people and students.

Its purpose is to help users identify possible "money leaks" by analyzing their daily expenses.

Example:

"Hoy gasté $8.000 en un taxi"

The application uses AI to interpret the expense text and extract:

* Valor
* Categoría
* Descripción

For example:

* Valor: $8.000
* Categoría: Transporte
* Descripción: Taxi

The expense is then stored in the database, displayed in the history, included in the dashboard, and used by a rule-based system to identify possible money leaks.

IMPORTANT:

Money-leak detection is NOT performed by AI.

It is performed using predefined system rules.

Example rule:

"Si existen 3 o más gastos similares dentro de una misma categoría durante un período corto, marcar como posible fuga."

---

# TECHNOLOGY STACK

Use exactly these technologies:

* React Native + TypeScript — mobile application
* Python + FastAPI — backend/API
* OpenAI API — AI-based expense interpretation
* MongoDB — primary persistent database
* Redis — cache and temporary data
* JWT — authentication and authorization
* Docker + Docker Compose — infrastructure
* Git + GitHub — version control

Do NOT introduce additional technologies.

Do NOT add:

* Kubernetes
* Kafka
* RabbitMQ
* PostgreSQL
* Firebase
* AWS
* Azure
* Google Cloud
* Other databases
* Other AI providers
* Additional message brokers
* Unrequested microservices

---

# IMPORTANT LANGUAGE RULE

The instructions and technical reasoning may be written in English.

However, ALL VISIBLE TEXT INSIDE THE DIAGRAM MUST BE IN SPANISH.

This includes:

* Diagram title
* Component names
* Actor names
* Labels
* Descriptions
* Group/container names
* Relationship labels
* Technology descriptions

Use technical names only when they represent actual technology names, such as:

* React Native
* TypeScript
* FastAPI
* OpenAI API
* MongoDB
* Redis
* JWT
* Docker Compose
* GitHub

For example, use:

"Servicio de Autenticación"

instead of:

"Authentication Service"

Use:

"Servicio de Interpretación con IA"

instead of:

"AI Interpretation Service"

---

# ARCHITECTURE

The main architecture must visually represent:

Actores
↓
Aplicación móvil
↓
Backend / API
↓
Servicios del backend
↓
Persistencia y servicios externos

The mobile application MUST NOT connect directly to:

* MongoDB
* Redis
* OpenAI API

FastAPI must act as the intermediary between the mobile application and backend services.

---

# ACTORS

Include these actors:

### Visitante

The visitor:

* Can access public information about FUGA+.
* Can see how the application works.
* Can register.
* Can log in.
* Does NOT have access to personal financial information.
* Does NOT receive a JWT simply for viewing public information.

IMPORTANT:

"Visitante" is NOT a database entity.

It is an unauthenticated/public access role.

### Usuario

The registered user can:

* Register expenses.
* Use AI interpretation.
* View expense history.
* View the dashboard.
* Filter expenses.
* Correct categories.
* View possible money leaks.

### Administrador

The administrator can:

* Access the administrative panel.
* View general statistics.
* View users.
* Activate or deactivate user accounts.

The administrator should NOT unnecessarily access detailed personal financial information.

### Desarrollador

The developer is included only to represent the development/version-control relationship:

Desarrollador → Git → GitHub

GitHub is NOT part of the application's runtime architecture.

---

# MOBILE APPLICATION COMPONENTS

Create a container/group named:

"Aplicación móvil FUGA+"

Inside it, represent these logical components:

* Acceso público
* Autenticación
* Registro de gastos
* Historial de gastos
* Dashboard
* Consultas de gastos
* Detección de posibles fugas
* Perfil de usuario
* Panel de administración

Do not create dozens of individual screens.

These should be logical application components.

The mobile application technology must be shown as:

"React Native + TypeScript"

---

# BACKEND

Create a container/group named:

"Backend FUGA+"

Represent FastAPI as the backend/API technology.

Inside the backend, create these logical components:

### Servicio de Autenticación

Responsibilities:

* Registro
* Inicio de sesión
* Validación de credenciales
* Generación y validación de JWT
* Gestión de roles Usuario/Administrador

### Servicio de Usuarios

Responsibilities:

* Datos básicos del usuario
* Consulta de usuario
* Actualización de usuario
* Estado de cuenta

### Servicio de Gastos

Responsibilities:

* Recibir gastos
* Validar información
* Coordinar el procesamiento
* Guardar gastos

### Servicio de Interpretación con IA

Responsibilities:

* Receive expense text
* Send it to OpenAI API
* Extract value
* Determine category
* Extract description
* Return structured information to the backend

Visible description must be in Spanish.

Clearly indicate:

"Interpretación de valor, categoría y descripción"

IMPORTANT:

This component is the ONLY backend component that communicates with OpenAI API.

Do NOT use OpenAI for money-leak detection.

### Servicio de Historial

Responsibilities:

* Retrieve expenses
* Order them chronologically
* Show date, value, category and description

### Servicio de Dashboard

Responsibilities:

* Calculate expense totals
* Calculate totals by category
* Provide summary information
* Generate dashboard data

It may use MongoDB aggregation operations.

### Servicio de Consultas

Responsibilities:

* Filter by category
* Filter by date range
* Perform basic expense queries

### Servicio de Detección de Posibles Fugas

This component MUST be clearly marked as:

"Basado en reglas"

It must NOT communicate with OpenAI.

Example rule:

"3 o más gastos similares en una categoría durante un período corto"

The diagram must make it visually clear that this component uses system rules, not AI.

### Servicio de Administración

Responsibilities:

* General statistics
* User management
* Activate/deactivate accounts
* Administrative operations

---

# DATABASE

Represent:

"MongoDB — Base de datos principal"

MongoDB is the primary persistent database.

Conceptually represent these collections if they improve clarity:

* Usuarios
* Gastos
* Categorías
* Resultados de fugas

Do not make every collection a separate UML component if that makes the diagram unnecessarily complex.

The main idea is:

Backend Services → MongoDB

MongoDB stores persistent application data.

---

# REDIS

Represent:

"Redis — Caché"

Redis is NOT the primary database.

Use it for:

* Cache
* Temporary data
* Frequently requested results
* Temporary session-related information when required

Clearly distinguish Redis from MongoDB visually.

MongoDB = persistent data.

Redis = temporary/cache support.

---

# OPENAI API

Represent an external component:

"OpenAI API"

Connect it ONLY with:

"Servicio de Interpretación con IA"

The visible label should communicate:

"Interpretación de gastos"

The flow should be:

Usuario
→ Aplicación móvil
→ FastAPI
→ Servicio de Interpretación con IA
→ OpenAI API
→ Resultado estructurado
→ Servicio de Gastos
→ MongoDB

Do NOT connect OpenAI directly to:

* React Native
* MongoDB
* Redis
* Detección de Posibles Fugas

---

# JWT AUTHENTICATION

Clearly represent JWT authentication.

The logical flow is:

Usuario
→ Servicio de Autenticación
→ JWT
→ Acceso autorizado a los servicios

Represent these application roles:

* Usuario
* Administrador

The visitor does not require JWT for public access.

---

# DOCKER COMPOSE

Create a visual group:

"Infraestructura — Docker Compose"

Inside it, conceptually include:

* Backend FastAPI
* MongoDB
* Redis

React Native should remain outside this infrastructure group because it is the mobile application.

OpenAI API should remain outside because it is an external service.

---

# GITHUB

Create a separate development area:

"Control de versiones"

Represent:

Desarrollador
→ Git
→ GitHub

Use the visible label:

"Repositorio del proyecto"

IMPORTANT:

GitHub is NOT part of the application's runtime flow.

Do NOT connect GitHub to:

* Users
* Mobile App
* FastAPI
* MongoDB
* Redis
* OpenAI API

---

# MAIN APPLICATION FLOW

The diagram must allow the following flow to be understood visually:

1. Visitante accesses public information.
2. Visitante registers or logs in.
3. Servicio de Autenticación validates credentials.
4. JWT is generated.
5. Usuario registers an expense using natural language.
6. Servicio de Gastos receives the expense.
7. Servicio de Interpretación con IA processes the text.
8. OpenAI API interprets the expense.
9. The result contains value, category and description.
10. Servicio de Gastos stores the expense in MongoDB.
11. Servicio de Historial retrieves expenses.
12. Servicio de Dashboard generates statistics.
13. Servicio de Detección de Posibles Fugas analyzes expenses using predefined rules.
14. The user can view a possible money leak.
15. Administrador accesses the Panel de Administración.
16. Administrator can view general statistics and manage users.

---

# COMMUNICATIONS

Show the main communication mechanisms.

Use visible Spanish labels such as:

* "HTTPS / REST"
* "JSON"
* "JWT"
* "API de OpenAI"
* "Conexión a MongoDB"
* "Caché Redis"

Do not show detailed API endpoints.

Do not show implementation-level code.

---

# VISUAL ORGANIZATION

Organize the diagram into clear visual layers.

## Layer 1 — Actores

Place on the left:

* Visitante
* Usuario
* Administrador
* Desarrollador

## Layer 2 — Aplicación

Place next to the actors:

"Aplicación móvil FUGA+"

Technology:

"React Native + TypeScript"

## Layer 3 — Backend

Place in the center:

"Backend FUGA+"

Technology:

"Python + FastAPI"

Place the backend services inside this group.

## Layer 4 — Data and external services

Place on the right:

* MongoDB
* Redis
* OpenAI API

## Layer 5 — Infrastructure and development

Place separately:

* Docker Compose
* GitHub

Keep the runtime architecture visually separate from development tools.

---

# UML STYLE

This MUST be a UML Component Diagram.

Use:

* UML components
* Dependencies
* Interfaces where useful
* Containers/groups
* Actors
* Clear relationships

Do NOT create:

* Class diagram
* Sequence diagram
* Activity diagram
* Entity-relationship diagram
* Deployment diagram
* Generic flowchart

Do not represent source-code classes.

Do not represent individual database columns.

Do not represent API endpoints.

---

# VISUAL QUALITY

The diagram must look professional and suitable for a university software-architecture presentation.

Use:

* Clear grouping
* Consistent spacing
* Readable labels
* Minimal line crossings
* Clear direction of main flows
* Consistent component shapes
* Clear distinction between application, backend, database and external services

Do not make the diagram unnecessarily huge.

It should contain enough detail to demonstrate the architecture without becoming visually confusing.

The most important flow should be easy to follow:

Usuario
→ Aplicación móvil
→ FastAPI
→ Servicios
→ MongoDB / Redis / OpenAI

---

# FILE REQUIREMENTS

The folder already exists:

`docs/diagramas/`

DO NOT create another folder.

Create ONLY:

`docs/diagramas/diagrama-componentes.drawio`

The file MUST:

* Be a valid Draw.io/diagrams.net XML file.
* Be editable.
* Open correctly in diagrams.net.
* Contain the complete component diagram.
* Use Spanish for all visible diagram text.
* Include the required technologies.
* Include the required actors.
* Include the required backend components.
* Include the required relationships.

Do NOT create:

* PNG
* JPG
* SVG
* PDF
* Markdown
* README
* Additional `.drawio` files
* Additional diagrams
* Additional documentation

ONLY create:

`docs/diagramas/diagrama-componentes.drawio`

---

# FINAL VERIFICATION

Before finishing, verify all of the following:

1. The folder `docs/diagramas/` already existed and was not duplicated.
2. Only `docs/diagramas/diagrama-componentes.drawio` was created or modified.
3. The file contains valid editable Draw.io XML.
4. The diagram is a UML component diagram.
5. All visible diagram text is in Spanish.
6. React Native + TypeScript is represented.
7. Python + FastAPI is represented.
8. OpenAI API is represented.
9. MongoDB is represented as the primary persistent database.
10. Redis is represented as cache/temporary support.
11. JWT authentication is represented.
12. Docker Compose is represented.
13. Git + GitHub are represented only as development/version-control tools.
14. Visitor, User, Administrator and Developer are represented.
15. The main backend services are represented.
16. OpenAI is connected only to the AI Interpretation Service.
17. Money-leak detection is explicitly rule-based and does not use OpenAI.
18. The mobile application does not connect directly to MongoDB, Redis or OpenAI.
19. FastAPI acts as the backend intermediary.
20. No additional technologies have been introduced.
21. No additional diagrams or files have been created.

The final output must contain ONLY the component diagram file:

`docs/diagramas/diagrama-componentes.drawio`
