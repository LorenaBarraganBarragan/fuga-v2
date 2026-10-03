Modify the existing Draw.io file:

docs/diagramas/diagrama-entidad-relacion.drawio

The current diagram is understandable structurally, but the entity/collection names are not clear enough. Replace the generic text "«colección»" with explicit collection names and make the database structure easier to understand.

IMPORTANT:
- Modify ONLY this existing file.
- Do NOT create another file.
- Do NOT create any additional files.
- Physically edit the Draw.io file.
- All visible text must be in Spanish.
- Keep official technical terms such as MongoDB unchanged.

TITLE:
"Diagrama Entidad-Relación — FUGA+"

SUBTITLE:
"Estructura de datos de la aplicación"

DATABASE:
MongoDB

IMPORTANT VISUAL RULE:

Each entity must clearly display BOTH:
1. The conceptual name in Spanish.
2. The exact MongoDB collection name.

Use this format in every entity header:

"USUARIOS"
"Colección MongoDB: usuarios"

Do NOT use only "«colección»".

ENTITIES AND EXACT COLLECTION NAMES:

1. USUARIOS
Collection: usuarios

Attributes:
- _id — PK — Identificador del usuario
- nombre — Nombre del usuario
- correo — Correo electrónico
- contrasenaHash — Hash de la contraseña
- rol — Visitante / Usuario / Administrador
- estado — Activo / Inactivo


2. GASTOS
Collection: gastos

Attributes:
- _id — PK — Identificador del gasto
- usuarioId — Referencia a usuarios._id
- categoriaId — Referencia a categorias._id
- monto — Valor del gasto
- moneda — Moneda del gasto
- descripcion — Descripción del gasto
- fecha — Fecha del gasto
- textoOriginal — Texto escrito por el usuario


3. CATEGORÍAS
Collection: categorias

Attributes:
- _id — PK — Identificador de la categoría
- nombre — Nombre de la categoría

Example values:
- Transporte
- Alimentación
- Ocio
- Educación
- Servicios


4. POSIBLES FUGAS
Collection: posibles_fugas

Attributes:
- _id — PK — Identificador de la posible fuga
- usuarioId — Referencia a usuarios._id
- categoriaId — Referencia a categorias._id
- descripcion — Categoría o descripción afectada
- cantidadOcurrencias — Número de ocurrencias
- montoAcumulado — Suma de los montos acumulados
- reglaActivada — Regla de negocio activada
- fechaDeteccion — Fecha de detección


5. ALERTAS
Collection: alertas

Attributes:
- _id — PK — Identificador de la alerta
- usuarioId — Referencia a usuarios._id
- fugaId — Referencia a posibles_fugas._id
- tipo — Tipo de alerta
- mensaje — Mensaje mostrado al usuario
- fecha — Fecha de la alerta
- leida — Indica si fue leída


RELATIONSHIPS:

USUARIOS 1 ───── N GASTOS
Label: "registra"

USUARIOS 1 ───── N POSIBLES FUGAS
Label: "tiene"

USUARIOS 1 ───── N ALERTAS
Label: "recibe"

CATEGORÍAS 1 ───── N GASTOS
Label: "clasifica"

CATEGORÍAS 1 ───── N POSIBLES FUGAS
Label: "identifica"

POSIBLES FUGAS 1 ───── N GASTOS
Label: "se detecta mediante"

POSIBLES FUGAS 1 ───── N ALERTAS
Label: "genera"


VISUAL DESIGN:

Make the collection name highly visible.

For example:

┌─────────────────────────────────┐
│ USUARIOS                        │
│ Colección MongoDB: usuarios     │
├─────────────────────────────────┤
│ _id — PK                        │
│ nombre                          │
│ correo                          │
│ contrasenaHash                  │
│ rol                             │
│ estado                          │
└─────────────────────────────────┘

Use a different visual header color for each entity, but keep the overall diagram professional.

Use:
- PK = clave primaria/document identifier
- Reference = reference to another MongoDB document

For reference fields, explicitly write:
"usuarioId — Ref. usuarios._id"
"categoriaId — Ref. categorias._id"
"fugaId — Ref. posibles_fugas._id"

Do not use the term "FK" as if MongoDB were a relational SQL database.

IMPORTANT:

The diagram should make it immediately clear:

MongoDB
  ↓
Colecciones
  ↓
Documentos / atributos
  ↓
Referencias entre documentos

Add this note at the bottom:

"Nota: FUGA+ utiliza MongoDB. Las colecciones almacenan documentos y las referencias mediante usuarioId, categoriaId y fugaId relacionan documentos entre colecciones."

Do NOT add:
- React Native
- TypeScript
- FastAPI
- Python
- OpenAI API
- Redis
- JWT
- Docker
- GitHub
- Swagger

Those technologies belong to the component/architecture diagram, not this ERD.

FINAL VERIFICATION:
1. Modify docs/diagramas/diagrama-entidad-relacion.drawio.
2. Verify the file exists.
3. Verify it is not empty.
4. Verify it is valid Draw.io XML.
5. Make sure every entity visibly shows its Spanish name AND MongoDB collection name.
6. Make sure "«colección»" is no longer used as a generic placeholder.
7. Do not create any other files.