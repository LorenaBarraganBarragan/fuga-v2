# Diagrama Entidad-Relación de mongoDB NoSQL — FUGA+

Create the MongoDB data model diagram for the FUGA+ mobile application.

IMPORTANT: You must physically create the Draw.io file in the project filesystem. Do NOT only generate or display XML in your response.

## EXACT FILE TO CREATE

`docs/diagramas/modelo-datos-mongodb.drawio`

Do not create another folder.
Do not create any other diagram.
Do not create any other file.

## PROJECT CONTEXT

FUGA+ is a mobile application that helps young people and students identify possible money leaks by recording expenses in natural language.

The application uses MongoDB as the persistent database.

This diagram represents the Entity-Relationship model of FUGA+ adapted to a NoSQL document-oriented database using MongoDB.

It is NOT a traditional SQL ER diagram.

## IMPORTANT MONGODB / NOSQL RULE

Represent MongoDB as a document-oriented NoSQL database using collections and document fields.

Do not represent the model as SQL tables.

The purpose of this diagram is to show the main entities, their data fields, and their conceptual relationships while respecting the document-oriented nature of MongoDB.

## COLLECTION 1 — Usuarios

Collection name:

`Usuarios`

Fields:

- `_id`
- `nombre`
- `correo`
- `contraseñaHash`
- `rol`
- `estado`
- `fechaRegistro`
- `fechaActualizacion`

The `rol` field can contain:

- `USER`
- `ADMIN`

The `estado` field can contain:

- `ACTIVO`
- `INACTIVO`

Never represent a plain-text password. Use `contraseñaHash`.

## COLLECTION 2 — Gastos

Collection name:

`Gastos`

Fields:

- `_id`
- `usuarioId`
- `valor`
- `categoriaId`
- `descripcion`
- `textoOriginal`
- `fechaGasto`
- `fechaCreacion`

The expense stores the original natural-language text entered by the user in `textoOriginal`.

## COLLECTION 3 — Categorias

Collection name:

`Categorias`

Fields:

- `_id`
- `nombre`
- `descripcion`

Examples of category names may include:

- Transporte
- Alimentación
- Entretenimiento
- Compras
- Otros

## COLLECTION 4 — Fugas

Collection name:

`Fugas`

Fields:

- `_id`
- `usuarioId`
- `categoriaId`
- `periodoInicio`
- `periodoFin`
- `cantidadGastos`
- `valorTotal`
- `reglaAplicada`
- `fechaDeteccion`

The `Fugas` collection represents possible money leaks detected through rule-based analysis of expense history.

Do not describe `Fugas` as an AI prediction.

## RELATIONSHIPS

Show the following conceptual references:

### 1. Usuarios 1:N Gastos

Reference:

`Gastos.usuarioId -> Usuarios._id`

Meaning:

One user can have many expenses.

### 2. Categorias 1:N Gastos

Reference:

`Gastos.categoriaId -> Categorias._id`

Meaning:

One category can be associated with many expenses.

### 3. Usuarios 1:N Fugas

Reference:

`Fugas.usuarioId -> Usuarios._id`

Meaning:

One user can have many possible money-leak detections.

### 4. Categorias 1:N Fugas

Reference:

`Fugas.categoriaId -> Categorias._id`

Meaning:

One category can be associated with many possible money-leak detections.

### 5. Gastos -> Fugas

Show that `Fugas` is generated from the analysis of `Gastos` using business rules.

For this relationship, do not invent a database foreign key if it is not necessary.

It can be represented as a conceptual/dashed relationship labeled:

`Análisis mediante reglas`

## IMPORTANT

Do NOT create a collection for Visitor.

Visitors are public users without an account and without stored personal financial data.

Do NOT include:

- Redis
- OpenAI
- FastAPI
- React Native
- JWT
- Docker
- GitHub
- External APIs
- Deployment infrastructure

Those belong to other diagrams, not this Entity-Relationship / MongoDB data model.

## VISUAL REQUIREMENTS

Title:

**"Diagrama Entidad-Relación — FUGA+"**

Subtitle:

**"Modelo NoSQL adaptado a MongoDB"**

Use clear collection/document boxes.

Each collection should have:

- Collection name at the top.
- A clear separation between the collection name and its fields.
- Fields listed vertically.
- `_id` clearly identifiable as the document identifier.
- Reference fields such as `usuarioId` and `categoriaId` clearly visible.

Use connectors/arrows to show the conceptual relationships.

Use cardinality labels such as:

`1:N`

The diagram must make it visually clear that the model represents MongoDB/NoSQL collections and documents rather than traditional SQL tables.

All visible diagram text must be in Spanish.

Keep technical field names exactly as specified.

The diagram should be clean, readable, organized, and suitable for a university software architecture presentation.

Do not overcomplicate the diagram.

## FILE CREATION REQUIREMENTS

1. Physically create the file:

`docs/diagramas/modelo-datos-mongodb.drawio`

2. The file must contain valid editable Draw.io / diagrams.net XML.

3. Do not merely print the XML in your response.

4. After creating the file, verify that:

- The file exists.
- The file is not empty.
- It contains valid Draw.io XML structure.
- The diagram contains the four required collections.
- The title is `Diagrama Entidad-Relación — FUGA+`.
- The subtitle is `Modelo NoSQL adaptado a MongoDB`.
- The relationships are present.
- The diagram clearly represents a NoSQL/MongoDB model.

5. If the file already exists, update/overwrite only this requested diagram file.

6. Do not create additional files.

7. Do not modify other project files.

## FINAL RESPONSE

After physically creating and verifying the file, respond briefly in English confirming:

"Created and verified docs/diagramas/modelo-datos-mongodb.drawio"

Do not paste the XML into the response.