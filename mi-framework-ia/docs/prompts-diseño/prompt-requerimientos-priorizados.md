# PROMPT: Create the Prioritized Requirements Document for FUGA+

Act as a software requirements analyst. Review the existing prioritized FUGA+ user stories and convert them into a clear, consistent, and testable prioritized requirements document.

**IMPORTANT: Although this prompt is written in English, all generated documentation and your final response MUST be written in Spanish.**

## 1. Source review

Inspect the existing repository documentation and locate the latest improved and prioritized FUGA+ user stories.

Use those stories as the primary source. Do not invent requirements or change agreed project decisions. If the source stories are missing or contain unresolved issues, report them instead of fabricating information.

## 2. Project constraints

FUGA+ is a mobile expense-tracking application with a 12-week development period, supported by AI tools.

Agreed technologies:

- React Native and TypeScript.
- Python and FastAPI.
- MongoDB Atlas.
- JWT and Google sign-in.
- Custom dictionary and deterministic rules for expense text processing, without an external AI API.
- Android voice input using Kotlin and `SpeechRecognizer`.
- Cloudinary for profile images.
- Expo Notifications.

Important rules:

- Users can access only their own expenses.
- Privacy must be enforced by the backend.
- Administrators can view aggregated usage statistics but not individual private expenses.
- Users must review and correct interpreted expenses before saving.
- Editing and deleting expenses must update relevant summaries and analyses.
- Potential money leaks are identified using deterministic rules.
- Do not invent money-leak thresholds, numerical performance targets, or undefined business rules.
- Consider dependencies, integration, testing, security, and realistic MVP scope.

## 3. Required document content

Create one concise Markdown document containing only these sections:

### A. Requerimientos funcionales priorizados

Identify what the application must do based on the user stories.

Assign unique identifiers: `RF-001`, `RF-002`, and so on.

For each requirement, include:

- Identificador.
- Nombre.
- Descripción clara y verificable.
- Prioridad MoSCoW: Must Have, Should Have, Could Have, or Won't Have (por ahora).
- Justificación breve de la prioridad.
- Historia de usuario de origen.
- Criterios de aceptación verificables.
- Dependencias, cuando existan.
- Inclusión en el MVP: sí, no o pendiente de validación.

### B. Requerimientos no funcionales priorizados

Identify relevant quality requirements, including security, privacy, usability, maintainability, reliability, data integrity, compatibility, and performance where applicable.

Assign unique identifiers: `RNF-001`, `RNF-002`, and so on.

For each requirement, include:

- Identificador.
- Nombre.
- Descripción verificable.
- Prioridad MoSCoW.
- Justificación breve.
- Criterio de aceptación o método de validación.
- Estado: confirmado o pendiente de definición.

Do not invent numerical thresholds when the project has not defined them. Mark them as pending decisions when necessary.

### C. Matriz de trazabilidad

Create a table linking requirements to their original user stories.

Include:

- Identificador del requerimiento.
- Tipo de requerimiento.
- Historia de usuario relacionada.
- Prioridad.
- Inclusión en el MVP.

Ensure that all relevant user stories are represented. If one story produces multiple requirements, include all relevant relationships.

### D. Alcance priorizado del MVP

Summarize:

- Essential requirements for the MVP.
- Important requirements that may be included if time permits.
- Requirements postponed to later versions.
- A realistic implementation order for the 12-week project.

Consider AI-assisted development without ignoring testing, integration, and debugging. Security and privacy requirements necessary to protect user data must not be postponed.

### E. Dependencias y decisiones pendientes

List only the most relevant dependencies and unresolved decisions that could affect implementation or prioritization.

Clearly distinguish confirmed decisions from assumptions and pending definitions.

## 4. Output and file management

Save the document at this exact repository-relative path:

`docs/respuestas-ia/salida-requerimientos-priorizados/requerimientos_priorizados_fuga.md`

Before creating or editing files:

1. Inspect the repository and identify the existing user-story documentation.
2. Reuse the existing documentation as the source of truth.
3. Create the specified output directory only if it does not exist.
4. If the target file already exists, review and update it instead of creating a duplicate.

Do not create one file per requirement. Do not create unnecessary documents. Do not modify application code, dependencies, configuration files, or diagrams. Do not delete existing files.

## 5. Validation

Before finishing, verify that:

- The entire document is written in Spanish.
- Requirements have unique identifiers.
- Requirements are clear, non-duplicative, and testable.
- Priorities are justified.
- Requirements are traceable to the user stories.
- The MVP scope is realistic for 12 weeks.
- Security and privacy are appropriately addressed.
- Undefined decisions are clearly identified.
- The file exists at the exact requested path.

Execute the task; do not stop after presenting a plan.

Finally, respond in Spanish with the exact file path, the number of functional and non-functional requirements created, the priority breakdown, and any important pending decisions.