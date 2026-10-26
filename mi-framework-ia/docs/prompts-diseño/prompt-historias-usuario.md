# OPENCODE INSTRUCTIONS: REVIEW, IMPROVE, AND PRIORITIZE THE 33 FUGA+ USER STORIES

## 1. Objective

Review, improve, organize, and prioritize the 33 FUGA+ user stories included in this prompt.

The goal is to produce consistent, actionable documentation that can be used to plan the development of the FUGA+ mobile application over 12 weeks.

Development will be supported by AI tools. Account for this assistance when evaluating complexity and feasibility, but do not overlook integration, testing, dependencies, security, debugging, and verification.

### Mandatory language requirement

**All generated content MUST be written in Spanish.** This includes the main document, user stories, headings, tables, explanations, acceptance criteria, planning documents, reports, and any additional documentation.

This prompt is written in English, but the final deliverables and your final response to me must be in Spanish. Keep technical names, technology names, and original identifiers unchanged when appropriate.

## 2. Mandatory execution rules

1. Work in the existing FUGA+ repository. Do not create another project.
2. Before making changes, inspect the repository structure and identify the existing documentation related to user stories.
3. Reuse the existing documentation structure and the most appropriate existing user-story document.
4. If a main user-story document already exists, update it instead of creating a duplicate.
5. If no suitable document exists, create one main Markdown document in the most appropriate existing documentation directory.
6. Do not create a separate file for each user story.
7. Consolidate all 33 user stories into **one single main Markdown file**.
8. Create only additional documents that provide a clear, necessary benefit. Prefer consolidating related information into the main document.
9. Do not create another folder with a new name just to store the user stories.
10. Do not delete or overwrite existing documentation without inspecting its contents and purpose first.
11. Do not modify application code, configuration files, dependencies, or diagrams as part of this task.
12. Complete the task. Do not stop after presenting an analysis or implementation plan.
13. At the end, verify the generated documentation and report the exact paths of all files changed or created.

If previous attempts created a new folder or separate files for individual stories, inspect those artifacts before proceeding. Reuse useful information where appropriate, avoid unnecessary duplication, and do not delete existing artifacts automatically.

## 3. FUGA+ project context and agreed technologies

FUGA+ is a mobile application for young people and students. It allows users to record expenses, review their expense history, view statistics, and identify potential money leaks.

The current technical decisions are:

- Mobile application: React Native and TypeScript.
- Backend: Python and FastAPI.
- Database: MongoDB Atlas.
- Authentication: JWT and Google sign-in.
- Expense text processing: a custom word dictionary and deterministic rules, without using an external AI API.
- Interface button label: “Procesar con IA”. Despite this label, the agreed implementation uses the custom dictionary and deterministic rules.
- Voice expense entry: Android only, using Kotlin and Android `SpeechRecognizer`.
- Profile images: Cloudinary.
- Notifications: Expo Notifications. Distinguish local notifications from push notifications and identify any additional requirements for push notifications.

Important functional constraints:

- Users must be able to review and correct interpreted expense data before saving it.
- Each user may access and manage only their own expenses.
- Privacy must be enforced by the backend, not merely by hiding information in the user interface.
- Administrators may view aggregated application usage statistics but must not access individual users' private expenses.
- Editing or deleting expenses must update affected summaries, statistics, and analyses.
- Money leaks are potential small, repetitive expenses identified through deterministic rules. They are not predictions or judgments about users' spending habits.
- Do not invent detection thresholds, minimum amounts, frequencies, or rules that have not been agreed upon. Record these as pending decisions.

Preserve these technical decisions. If you identify inconsistencies, explain them and document the required decisions instead of silently changing the architecture.

## 4. The 33 original user stories to review

Preserve the original identifiers HU-01 through HU-33 for traceability.

### Module 1. Access, authentication, and accounts

**HU-01.** View public information about FUGA+.

**HU-02.** Register and sign in to the application.

**HU-03.** Sign in using a Google account.

**HU-04.** Sign out securely.

**HU-05.** Recover access through password recovery.

**HU-06.** Deactivate the user account.

### Module 2. User profile

**HU-07.** View and edit first name, last name, and phone number.

**HU-08.** Change the profile picture.

**HU-09.** Use the Google profile picture when available.

### Module 3. Expense registration and management

**HU-10.** Enter an expense in natural language, for example: “Hoy gasté $8.000 en un taxi”.

**HU-11.** Process the expense using the “Procesar con IA” button and a custom dictionary and deterministic rules, without an external AI API.

**HU-12.** Review and correct the amount, category, description, and other interpreted fields before saving.

**HU-13.** Save each expense under its owner's account and protect it from access by other accounts.

**HU-14.** View expense history sorted from newest to oldest.

**HU-15.** Filter expenses by date and category.

**HU-16.** Edit and delete saved expenses and update the affected analyses and summaries.

### Module 4. Voice-based expense entry

**HU-17.** Start voice recording for an expense on Android devices.

**HU-18.** Convert speech into text using Kotlin and Android `SpeechRecognizer`.

**HU-19.** Review and correct the transcription and expense fields before saving. The flow must be: voice input → editable transcription → processing through “Procesar con IA” → review interpreted fields → confirm and save.

### Module 5. Dashboard and statistics

**HU-20.** View total spending, the number of expenses, and average spending per period.

**HU-21.** View expenses by category and identify the category with the highest spending.

**HU-22.** Compare expenses across different periods.

### Module 6. Money leak detection

**HU-23.** Detect potential small, repetitive expenses using deterministic rules.

**HU-24.** View evidence for a potential money leak, including occurrence count and accumulated amount.

### Module 7. Alerts, recommendations, and goals

**HU-25.** Receive alerts about potential money leaks.

**HU-26.** View practical suggestions related to identified potential money leaks.

**HU-27.** View a monthly summary of potential money leaks.

**HU-28.** Set a monthly spending or savings goal, clearly defining its scope.

**HU-29.** Track progress toward the established goal.

### Module 8. Administration and privacy

**HU-30.** View aggregated application usage statistics without accessing individual private expenses.

**HU-31.** View registered users and the administrative information required for management.

**HU-32.** Activate or deactivate user accounts through authorized administrative functions.

**HU-33.** Protect expense privacy and enforce data separation between users.

## 5. Requirements for improving the user stories

For every story:

1. Preserve the original identifier.
2. Improve the title and wording without changing the original functional purpose.
3. Use the following user-story format in Spanish: “Como [tipo de usuario], quiero [funcionalidad], para [beneficio]”.
4. Briefly explain the objective and value for the user.
5. Define acceptance criteria using the Given-When-Then structure, written in Spanish as “Dado, Cuando y Entonces”.
6. Include relevant business rules, validations, and error handling.
7. Identify technical and functional dependencies.
8. Suggest appropriate tests.
9. Identify ambiguities and decisions that still require confirmation.
10. Avoid vague criteria such as “it must work correctly”. Acceptance criteria must be verifiable.

Stories do not need identical lengths. Keep the level of detail proportional to their complexity.

If a story needs to be split, merged, or substantially rewritten, document the change and maintain traceability to the original identifier. Do not silently remove any original functionality.

## 6. Prioritization and planning

Assign a MoSCoW priority to each story:

- **Must Have:** essential for the MVP.
- **Should Have:** important, but the MVP can operate without it.
- **Could Have:** useful if time allows.
- **Won't Have (for now):** explicitly postponed to a later version.

Justify every priority.

Consider the following:

- The project has 12 weeks available.
- AI tools will support development.
- Integration, testing, security, debugging, and demo preparation require time.
- Not all 33 stories must be included in the MVP.
- Dependencies must be respected when establishing implementation order.
- A feature should not be considered essential merely because it is useful or interesting.
- AI assistance does not eliminate the need for integration and testing.

Propose a realistic implementation sequence organized into phases or weeks. Identify which stories belong in the MVP and which should be postponed.

Do not invent exact hour estimates or make unsupported commitments about individual delivery dates.

## 7. Required structure of the main document

The main Markdown document must contain the following sections, in this order:

1. Project name, document title, and update date.
2. Objective and scope.
3. Functional context and agreed technical decisions.
4. Criteria used to improve and prioritize the stories.
5. A summary table containing all 33 identifiers, improved titles, modules, and priorities.
6. All 33 complete user stories, grouped by module and retaining their original identifiers.
7. A dependency matrix between user stories.
8. A traceability matrix linking original stories to their improved versions. If a story is split, merged, or substantially changed, document the mapping without losing traceability.
9. Proposed MVP scope.
10. Features postponed to future versions.
11. A suggested 12-week implementation plan.
12. Pending decisions, risks, and assumptions requiring validation.

Additional documents, such as a risk register or a decision log, may be created only when they provide clear value. Do not create individual files for each user story.

## 8. Final quality checks

Before finishing, verify that:

- All 33 original user stories are included.
- All identifiers are unique and preserved.
- No original functionality has been lost.
- Every story has a justified MoSCoW priority.
- Acceptance criteria are verifiable.
- Dependencies are consistent.
- Pending decisions are clearly distinguished from agreed decisions.
- The proposed MVP is realistic for 12 weeks with AI-assisted development.
- All generated documentation is written in Spanish.
- No unnecessary folders, duplicate documents, or individual story files have been created by this task.
- No application code, configuration, dependencies, or diagrams have been modified.
- Existing documentation was updated where appropriate instead of unnecessarily duplicated.

## 9. Execution and final report

Work directly within the existing repository and its documentation structure.

Deliver all 33 user stories in **one single main Markdown file**, using the most appropriate existing documentation location.

When finished, provide a final report in Spanish stating:

- Which existing file was updated or which main file was created, including its exact path.
- Which additional documents were created, if any, and why.
- How many stories were assigned to each MoSCoW priority.
- Which stories are included in the MVP.
- Which decisions remain unresolved.
- Whether any instruction could not be completed and why.

**Start by inspecting the repository. Then perform the documentation changes and verify the results. Do not stop after presenting a plan. All deliverables and your final response must be in Spanish.**