Create the UML Use Case Diagram for FUGA+.

IMPORTANT: Do not just describe the diagram. Do not only generate XML in the chat.

You MUST physically create this exact file in the current project:

docs/diagramas/diagrama-casos-uso.drawio

First verify that the folder exists. If it does not exist, create it.

Then create the actual Draw.io XML file using the terminal/filesystem.

After creating it, VERIFY the file physically exists with a terminal command and verify that its file size is greater than 0.

Use ONLY this file path:

docs/diagramas/diagrama-casos-uso.drawio

Do not create another file.
Do not create temporary files.
Do not create Markdown files.

The diagram must contain:

TITLE:
Diagrama de Casos de Uso — FUGA+

SUBTITLE:
Requisitos funcionales y actores del sistema

SYSTEM BOUNDARY:
Sistema FUGA+

ACTORS:

* Visitante
* Usuario
* Administrador

USE CASES:

Visitante:

* UC-01 Conocer FUGA+
* UC-02 Registrarse
* UC-03 Iniciar sesión

Usuario:

* UC-03 Iniciar sesión
* UC-04 Registrar gasto en lenguaje natural
* UC-05 Interpretar gasto con IA
* UC-06 Confirmar gasto
* UC-07 Consultar historial de gastos
* UC-08 Consultar dashboard personal
* UC-09 Detectar posibles fugas de dinero
* UC-10 Filtrar historial
* UC-11 Corregir categoría del gasto
* UC-14 Recibir alerta de posible fuga
* UC-15 Registrar gasto por voz
* UC-16 Comparar periodos

Administrador:

* UC-03 Iniciar sesión
* UC-12 Consultar estadísticas generales
* UC-13 Gestionar usuarios

IMPORTANT RELATIONSHIPS:

UC-04 Registrar gasto en lenguaje natural
<<include>>
UC-05 Interpretar gasto con IA

UC-04 Registrar gasto en lenguaje natural
<<include>>
UC-06 Confirmar gasto

UC-07 Consultar historial de gastos
<<include>>
UC-10 Filtrar historial

UC-09 Detectar posibles fugas de dinero
<<extend>>
UC-14 Recibir alerta de posible fuga

UC-15 Registrar gasto por voz
reuses the normal expense registration flow.

The diagram must represent that:

* AI only interprets amount, currency, category and description.
* Money leaks are detected using deterministic rules, not AI prediction.
* Users can correct the AI-assigned category.
* Administrators only access aggregated statistics and user account management.
* Administrators cannot access individual financial information.
* Disabled users cannot log in.

Do NOT create actors for AI, MongoDB, database, backend, frontend, API, JWT or OpenAI.

Do NOT create use cases for:

* bank connections
* payments
* transfers
* cards
* loans
* investments
* professional financial advice
* market prediction
* custom AI model training
* real third-party banking data
* advanced push notifications
* advanced receipt scanning
* external banking integrations
* advanced administration
* multiple administrator levels

All visible text in the diagram MUST be in Spanish.

Use standard UML notation:

* stick figures for actors
* ovals for use cases
* rectangle for the system boundary
* solid lines for actor associations
* dashed arrows for <<include>> and <<extend>>

Organize the diagram visually into these areas:

1. Acceso público
2. Gestión de gastos
3. Historial y análisis
4. Administración
5. Funciones opcionales

Make the diagram clean, readable and well spaced.

The final result MUST be a valid Draw.io .drawio file that opens in diagrams.net.

FINAL ACTION:

Physically create:

docs/diagramas/diagrama-casos-uso.drawio

Then run a terminal verification equivalent to:

Test-Path "docs/diagramas/diagrama-casos-uso.drawio"

and verify that the result is True.

Then verify the file is not empty.

Only after the physical file exists, report:

Created and verified:
docs/diagramas/diagrama-casos-uso.drawio
