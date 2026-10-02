Prompt: Prioritized requirements for the entire project
Act as a senior requirements analyst and Product Manager specializing in MVP definition and prioritization using the MoSCoW method. PROJECT CONTEXT
"""
FUGA+ is a mobile application initially aimed at young people and students, designed to help them understand their spending habits and discover potential money leaks—primarily those linked to small, recurring expenses.
Users will be able to log an expense using natural language text. For example: “Today I spent $8,000 on a taxi.”
Artificial Intelligence will interpret and classify the expense data, identifying elements such as amount, category, and description.
Expenses will be stored in a history log and viewable via a simple dashboard.
The system will use custom rules to analyze expenses and identify potential money leaks.
The project will be developed individually over 12 weeks, and the MVP must be demonstrable within approximately 3 minutes.
At a minimum, the MVP must allow for: logging expenses via text; interpreting and classifying expenses using AI; storing and viewing the history; displaying a simple dashboard; identifying potential leaks using custom rules; and performing basic queries on recorded expenses.
Excluded from the MVP are: bank connections, payments, transfers, cards, credit facilities, loans, investments, professional financial advice, training a custom AI model, market prediction, real third-party banking data, advanced notifications, advanced receipt scanning, and external banking integrations.
Voice functionality may only be developed as an additional feature if time permits.
"""
PRIORITY REQUIREMENTS
"""
RF-01 — Expense logging via text: The system must allow the user to log an expense by typing a description in natural language.

RF-02 — AI-based interpretation: The system must interpret the recorded information and identify elements such as amount, category, and description.

RF-03 — Expense storage: The system must store recorded expenses for future reference.

RF-04 — Expense history: The system must allow users to view recorded expenses via a history log.

RF-05 — Dashboard: The system must display a simple dashboard showing information about recorded expenses.

RF-06 — Identification of potential money leaks: The system must analyze expenses using custom rules to identify potential... ...money leaks primarily related to small, repetitive expenses.

RF-07 — Basic queries: The system must allow for basic queries regarding recorded expenses.

RF-08 — Voice-based entry: The system may allow expense entry via voice as an additional feature, time permitting.

RNF-01 — Development time: The solution must be feasible for development by a single person over 12 weeks.

RNF-02 — Demonstration: The MVP must be capable of a functional demonstration within approximately 3 minutes.

RNF-03 — AI scope: The Artificial Intelligence used must be limited to the interpretation and classification of recorded expenses.

TASK
Analyze the provided requirements and assign them a priority using the MoSCoW method.
The prioritization must determine which features are essential for FUGA+ to be considered a functional MVP, which are important but can wait, which are desirable, and which fall outside the current scope.
Consider:
•	The primary goal of FUGA+.
•	The 3-minute demonstration.
•	The 12-week timeframe.
•	The fact that the project will be developed individually.
•	Dependencies between requirements.
•	The technical risk associated with Artificial Intelligence.
•	The need for a functional MVP before adding extra features.
OUTPUT FORMAT
Use this format for each requirement:
RF-01 — Must
Expense entry: The system must allow an expense to be recorded via text.
Acceptance criterion: Upon entering text such as “Today I spent $8,000 on a taxi,” the system must record the corresponding information.
Continue with all requirements and use only these priorities:
Must: essential for the MVP's operation and demonstration.
Should: important, but the MVP can function without this capability initially.
Could: desirable and can be implemented if time permits.
Won't: explicitly out of scope for the current MVP.
Then include:
Prioritization justification
Briefly explain the key prioritization decisions. Essential requirements for the demonstration
List the requirements that must be functional during the 3-minute demonstration.
Dependencies
Indicate which requirements depend on other requirements being implemented beforehand.
Key risks
Identify up to 3 requirements that