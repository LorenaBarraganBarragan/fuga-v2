Act as a senior Requirements Analyst and Product Manager specialized in software requirements engineering, MVP definition, and MoSCoW prioritization.

Your task is to analyze the FUGA+ project context and generate the complete prioritized requirements document from scratch.

IMPORTANT:
- Do not use or depend on any previous "prioritized requirements" response.
- Generate the requirements based only on the project context provided below.
- The final document must be written in Spanish.
- The document must be concise, clear, consistent, and suitable for a university software engineering project.
- Do not generate code.
- Do not generate UML, Mermaid, Draw.io, database schemas, or architecture diagrams.

==================================================
PROJECT: FUGA+
==================================================

FUGA+ is a mobile application designed for young people and students to identify "money leaks" caused mainly by small and repetitive expenses.

The main idea is:

"Descubre por dónde se va tu plata."

The application allows an authenticated user to register an expense using natural language.

Example:

"Hoy gasté $8.000 en un taxi"

The system should interpret the text and identify:

- Amount
- Category
- Description

Example result:

Amount: $8.000
Category: Transporte
Description: Taxi

After the interpretation, the user can confirm the expense and the system stores it.

The application should then allow the user to:

- View their expense history.
- View a simple dashboard.
- Consult their expenses.
- Correct an incorrect category.
- Identify possible money leaks.

Possible money leaks are identified using predefined rules and patterns, mainly involving small and repetitive expenses.

IMPORTANT:
The identification of possible money leaks is NOT an AI prediction.
It must be treated as a rule-based analysis performed by the application.

==================================================
PROJECT SCOPE
==================================================

The project is developed by ONE person.

Development time: 12 weeks.

The MVP must be demonstrable in approximately 3 minutes.

The main demonstration flow should be:

1. Access FUGA+.
2. Register or log in.
3. Enter an expense using natural language.
4. Interpret the expense.
5. Confirm and store the expense.
6. View the expense history.
7. View the dashboard.
8. Show a possible money leak detected by predefined rules.

The project should remain realistic for one developer and a 12-week development period.

==================================================
ACTORS
==================================================

The system must consider exactly these three actors:

### Visitante

A person who accesses FUGA+ without being authenticated.

The visitor can:

- Learn what FUGA+ is.
- View basic information about how the application works.
- View the main functionalities.
- Access the registration option.
- Access the login option.

The visitor cannot access personal expenses.

### Usuario

An authenticated person with a FUGA+ account.

The user can:

- Register and log in.
- Register expenses using natural language text.
- Review the interpretation of an expense.
- Confirm and store expenses.
- View their expense history.
- View their dashboard.
- Identify possible money leaks.
- Perform basic expense queries.
- Correct an incorrectly assigned category.

A user must only access their own personal information and expenses.

### Administrador

An authenticated user with administrative permissions.

The administrator can:

- View general and aggregated application statistics.
- View registered users.
- Activate or deactivate user accounts.

The administrator must not automatically have access to the private financial details of individual users.

Do not invent additional actors.

==================================================
FUNCTIONAL REQUIREMENTS TO IDENTIFY
==================================================

Based on the project context, identify and formulate the functional requirements necessary for the MVP.

The expected core functionality should include:

1. Public access to information about FUGA+.
2. Registration and login.
3. Expense registration using natural language text.
4. AI-based interpretation of the expense.
5. Expense storage.
6. Expense history.
7. Dashboard.
8. Identification of possible money leaks using predefined rules.
9. Basic expense queries.
10. Correction of an AI-assigned category.
11. Administrative dashboard.
12. User management.
13. Optional alerts about possible money leaks.
14. Optional voice-based expense registration.
15. Optional comparison between expense periods.

Use these as the functional scope to analyze and formulate the requirements.

Do not create unnecessary additional functional requirements.

==================================================
NON-FUNCTIONAL REQUIREMENTS
==================================================

Identify the non-functional requirements necessary to guarantee the project's feasibility and quality.

At minimum, consider:

1. Development time and feasibility for one developer during 12 weeks.
2. Demonstration of the MVP in approximately 3 minutes.
3. Limitation of AI scope to expense interpretation and classification.
4. Security and role-based access.
5. Privacy of user expense data.

Do not create unnecessary additional non-functional requirements.

==================================================
MOSCOW PRIORITIZATION
==================================================

Prioritize the identified requirements using MoSCoW:

- Must: Essential for the MVP.
- Should: Important but the MVP can operate without it.
- Could: Optional and can be implemented if time remains.
- Won't: Explicitly outside the MVP scope.

Use this expected prioritization as guidance:

### MUST

The following core requirements should be Must:

- Public access.
- Registration and login.
- Expense registration by text.
- AI interpretation.
- Expense storage.
- Expense history.
- Dashboard.
- Identification of possible money leaks.
- Development feasibility.
- 3-minute demonstration.
- AI scope.
- Security and roles.
- Privacy.

### SHOULD

The following should normally be Should:

- Basic expense queries.
- Correction of category.
- Administrative dashboard.
- User management.

### COULD

The following should normally be Could:

- Alerts about possible money leaks.
- Voice registration.
- Comparison between periods.

### WON'T

The following are explicitly outside the MVP:

- Bank connections.
- Payments.
- Transfers.
- Credit/debit card management.
- Credit lines.
- Loans.
- Investments.
- Professional financial advice.
- Training a proprietary AI model.
- Market prediction.
- Real third-party banking data.
- Advanced push notifications.
- Advanced receipt scanning.
- External banking integrations.
- Advanced administrative functions.
- Multiple administrator levels.

Do not move these features into the MVP unless the project context explicitly changes.

==================================================
REQUIREMENT FORMAT
==================================================

For every functional requirement, use this format:

## RF-XX — Priority

**\*\*Nombre del requisito:\*\*** Description of the requirement.

**\*\*Criterio de aceptación:\*\*** A concrete and verifiable acceptance criterion.

Use sequential numbering starting with RF-01.

For every non-functional requirement, use:

## RNF-XX — Priority

**\*\*Nombre del requisito:\*\*** Description of the requirement.

**\*\*Criterio de aceptación:\*\*** A concrete and verifiable acceptance criterion.

Use sequential numbering starting with RNF-01.

==================================================
EXPECTED FUNCTIONAL REQUIREMENT CONTENT
==================================================

The generated requirements should cover the following concepts:

RF-01:
Public access so a visitor can learn about FUGA+ without registering.

RF-02:
Registration and login so a user can access personal functionality.

RF-03:
Natural-language expense registration.

RF-04:
AI interpretation that extracts amount, category, and description.

RF-05:
Persistent storage of confirmed expenses.

RF-06:
Chronological expense history.

RF-07:
Simple dashboard with expense summaries.

RF-08:
Rule-based identification of possible money leaks.

RF-09:
Basic expense queries or filters.

RF-10:
Correction of an incorrectly assigned category.

RF-11:
Administrative dashboard with general and aggregated statistics.

RF-12:
User management by the administrator.

RF-13:
Optional in-app alerts about possible money leaks.

RF-14:
Optional voice expense registration.

RF-15:
Optional comparison between different expense periods.

The wording may be improved for clarity, but do not change the intended scope.

==================================================
EXPECTED NON-FUNCTIONAL REQUIREMENT CONTENT
==================================================

The generated requirements should cover:

RNF-01:
Feasibility for one developer in 12 weeks.

RNF-02:
MVP demonstration in approximately 3 minutes.

RNF-03:
AI limited to expense interpretation and classification.

RNF-04:
Security and role-based access.

RNF-05:
Privacy and isolation of user expense data.

==================================================
WON'T SECTION
==================================================

Create a section titled exactly:

## Won't — Explícitamente fuera de alcance del MVP

Use a bullet list containing:

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

==================================================
JUSTIFICATION
==================================================

After the requirements, create:

## Justificación de la priorización

Explain the prioritization clearly.

The justification should explain:

- Why public access and registration/login are Must.
- Why expense registration, AI interpretation, storage, history, dashboard, and money-leak detection form the central value chain and therefore are Must.
- Why queries and category correction are Should.
- Why administrative dashboard and user management are Should.
- Why alerts, voice registration, and period comparison are Could.
- Why the non-functional requirements are Must because they establish feasibility, demonstration, AI scope, security, roles, and privacy.

Do not use subjective rankings or scores.

==================================================
DEMONSTRATION
==================================================

Create:

## Requisitos esenciales para la demostración

Include:

- RF-01 — Acceso público
- RF-02 — Registro e inicio de sesión
- RF-03 — Registro por texto
- RF-04 — Interpretación por IA
- RF-05 — Almacenamiento
- RF-06 — Historial
- RF-07 — Dashboard
- RF-08 — Detección de posibles fugas
- RNF-02 — Restricción de tiempo de la demostración

Explain that the administrative panel can be shown briefly as part of the general system but is not the main 3-minute flow.

==================================================
DEPENDENCIES
==================================================

Create:

## Dependencias

Describe the logical dependencies between the requirements.

At minimum, use this dependency chain:

RF-02 depends on RF-01.

RF-03 depends on RF-02.

RF-04 depends on RF-03.

RF-05 depends on RF-04.

RF-06 depends on RF-05.

RF-07 depends on RF-05.

RF-08 depends on RF-05 and sufficient historical expenses.

RF-09 depends on RF-05.

RF-10 depends on RF-04 and RF-05.

RF-11 depends on users and stored system data.

RF-12 depends on RF-02 and role/permission management.

RF-13 depends on RF-08.

RF-14 depends on RF-03 and RF-04.

RF-15 depends on RF-05 and RF-07.

RNF-02 depends on RF-02 through RF-08 working together.

==================================================
RISKS
==================================================

Create:

## Riesgos clave

Include these four key risks:

1. RF-04 — Interpretación basada en IA:
Technical risk related to correctly extracting amount, category, and description from informal natural language.

2. RF-08 — Identificación de fugas:
Design and validation risk related to defining rules that generate credible results and avoid excessive false positives.

3. RNF-04 — Seguridad y roles:
Risk related to authentication, authorization, role separation, and protection of user data.

4. RNF-02 — Demostración de 3 minutos:
Integration and testing risk caused by having to demonstrate the main flow in a short period as a solo developer.

==================================================
FINAL DOCUMENT STRUCTURE
==================================================

The final generated document MUST follow this exact order:

# Priorización de Requisitos (MoSCoW) — FUGA+

## RF-01 — Must
...
## RF-02 — Must
...
Continue through RF-15.

---

## RNF-01 — Must
...
Continue through RNF-05.

---

## Won't — Explícitamente fuera de alcance del MVP

...

---

## Justificación de la priorización

...

---

## Requisitos esenciales para la demostración

...

---

## Dependencias

...

---

## Riesgos clave

...

==================================================
OUTPUT FILE
==================================================

IMPORTANT:

Do not only display the result in the chat.

Physically create the final Markdown document inside the project filesystem.

The exact file to create is:

docs/respuestas-ia/salida-requerimientos-priorizados.md

If the file already exists, replace its contents with the newly generated document.

Do not create another file with a different name.

Do not create another folder.

After generating the document:

1. Verify that the file exists.
2. Verify that it is not empty.
3. Verify that it contains the complete requirements document.
4. Verify that the document is written in Spanish.
5. Verify that RF-01 through RF-15 are present.
6. Verify that RNF-01 through RNF-05 are present.
7. Verify that the Won't, Justificación, Requisitos esenciales para la demostración, Dependencias, and Riesgos clave sections are present.

Do not generate any other files.