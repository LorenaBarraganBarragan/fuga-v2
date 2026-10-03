# Task — Create FUGA+ Class Diagram

Create ONLY this file:

`docs/diagramas/diagrama-clases.drawio`

Do NOT create additional folders.
Do NOT create any other files.
Do NOT modify any existing files.

## Objective

Create a UML class diagram for the FUGA+ mobile application.

The diagram must show the main classes, their attributes, methods, and relationships.

The diagram must be editable in Draw.io / diagrams.net and must use valid Draw.io XML.

## IMPORTANT LANGUAGE REQUIREMENT

The instructions in this prompt are written in English, but ALL VISIBLE TEXT INSIDE THE DIAGRAM MUST BE IN SPANISH.

Technical data types such as `String`, `Decimal`, `Integer`, and `DateTime` may remain in English.

The visible diagram title must be:

**Diagrama de Clases — FUGA+**

Subtitle:

**Clases principales, atributos, métodos y relaciones**

## Classes

### 1. Usuario

Attributes:

- `- id: String`
- `- nombre: String`
- `- correo: String`
- `- contraseñaHash: String`
- `- rol: Rol`
- `- estado: EstadoUsuario`

Methods:

- `+ registrarse()`
- `+ iniciarSesion()`
- `+ actualizarPerfil()`

Possible roles:

- `USER`
- `ADMIN`

Possible states:

- `ACTIVO`
- `INACTIVO`

Passwords must never be stored as plain text.

Do NOT create a `Visitor` class. A visitor is an unauthenticated person who can access the public part of the application.

### 2. Gasto

Attributes:

- `- id: String`
- `- usuarioId: String`
- `- valor: Decimal`
- `- categoriaId: String`
- `- descripcion: String`
- `- textoOriginal: String`
- `- fechaGasto: DateTime`

Methods:

- `+ registrar()`
- `+ actualizarCategoria()`
- `+ consultar()`

This class represents an expense registered by a user.

### 3. Categoria

Attributes:

- `- id: String`
- `- nombre: String`
- `- descripcion: String`

Methods:

- `+ crear()`
- `+ actualizar()`
- `+ consultar()`

Example categories:

- Transporte
- Alimentación
- Entretenimiento
- Compras
- Otros

### 4. PosibleFuga

Attributes:

- `- id: String`
- `- usuarioId: String`
- `- categoriaId: String`
- `- periodoInicio: DateTime`
- `- periodoFin: DateTime`
- `- cantidadGastos: Integer`
- `- valorTotal: Decimal`
- `- reglaAplicada: String`
- `- fechaDeteccion: DateTime`

Methods:

- `+ detectar()`
- `+ consultar()`

This class represents a possible money leak detected using business rules.

It must NOT represent an AI prediction.

Example rule:

`3 o más gastos similares en una categoría durante un periodo corto`

### 5. AnalizadorGasto

Attributes:

- `- textoEntrada: String`
- `- valorDetectado: Decimal`
- `- categoriaDetectada: String`
- `- descripcionDetectada: String`

Methods:

- `+ analizarTexto()`
- `+ extraerValor()`
- `+ clasificarCategoria()`
- `+ generarDescripcion()`

This class represents the application logic responsible for analyzing the natural-language expense entered by the user and extracting:

- value
- category
- description

It represents the expense interpretation logic and its interaction with the AI service.

Do NOT create a class named `OpenAI`.

### 6. Autenticacion

Attributes:

- `- token: String`
- `- usuarioId: String`
- `- rol: String`

Methods:

- `+ autenticar()`
- `+ generarToken()`
- `+ validarToken()`
- `+ verificarRol()`

This class represents authentication and authorization logic.

JWT is an implementation technology, therefore do NOT create a class named `JWT`.

## Relationships

Create these UML relationships:

### Usuario — Gasto

`Usuario 1 ---- 0..* Gasto`

Meaning: one user can register many expenses.

### Categoria — Gasto

`Categoria 1 ---- 0..* Gasto`

Meaning: one category can be associated with many expenses.

### Usuario — PosibleFuga

`Usuario 1 ---- 0..* PosibleFuga`

Meaning: one user can have multiple possible money leaks.

### Categoria — PosibleFuga

`Categoria 1 ---- 0..* PosibleFuga`

Meaning: one category can be associated with multiple possible money leaks.

### Gasto — AnalizadorGasto

Create a UML dependency relationship from `Gasto` to `AnalizadorGasto`.

Use a dashed dependency arrow.

Meaning: the analyzer participates in interpreting the expense.

### Usuario — Autenticacion

Create a UML dependency relationship from `Usuario` to `Autenticacion`.

Use a dashed dependency arrow.

Meaning: authentication identifies and authorizes the user.

## Classes that MUST NOT appear

Do NOT create classes for infrastructure or technologies.

Do NOT add:

- `Redis`
- `MongoDB`
- `OpenAI`
- `FastAPI`
- `React Native`
- `JWT`
- `Docker`
- `GitHub`
- `API Gateway`
- `Database`
- `Visitor`

The diagram must focus on the main FUGA+ classes and application logic.

## UML Style

Use standard UML class diagram notation.

Each class must have three sections:

1. Class name
2. Attributes
3. Methods

Use:

- `-` for private attributes.
- `+` for public methods.
- Cardinalities such as `1` and `0..*`.
- Clearly visible UML relationships.
- Dashed arrows for dependencies.

Do not add inheritance unless there is a real inheritance relationship.

## Visual Organization

Make the diagram clean and easy to understand.

Avoid overlapping elements.

Use enough spacing between classes.

Make relationships easy to follow.

Keep the six main classes visually balanced.

The title and subtitle must be clearly visible at the top.

## File Requirements

Physically create:

`docs/diagramas/diagrama-clases.drawio`

The file must:

- Be valid Draw.io XML.
- Be editable in Draw.io / diagrams.net.
- Contain the complete class diagram.
- Have all six required classes.
- Have all required relationships.
- Have the Spanish title and subtitle.
- Have Spanish visible labels.
- Not be empty.

## Mandatory Verification

After creating the file:

1. Verify that `docs/diagramas/diagrama-clases.drawio` physically exists.
2. Verify that the file is not empty.
3. Verify that it contains valid Draw.io XML.
4. Verify that all six classes exist:
   - Usuario
   - Gasto
   - Categoria
   - PosibleFuga
   - AnalizadorGasto
   - Autenticacion
5. Verify that all required relationships exist.
6. Verify that the title is `Diagrama de Clases — FUGA+`.
7. Verify that all visible diagram text is in Spanish.
8. Do not create any other file.
9. Do not modify any other project file.

## Final Response

After completing and verifying the file, respond only with a short confirmation that the file was successfully created and verified.