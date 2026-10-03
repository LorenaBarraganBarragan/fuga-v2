Create the Draw.io component diagram for the FUGA+ mobile application.

IMPORTANT:
- Physically create the file in the project filesystem.
- Do NOT only generate XML in the response.
- Do NOT create any other files.
- Exact file path:
  docs/diagramas/diagrama-componentes.drawio
- All visible diagram text must be in Spanish.
- Keep official technology names unchanged.

TITLE:
"Diagrama de Componentes — FUGA+"

SUBTITLE:
"Arquitectura tecnológica de la aplicación móvil"

USE THIS EXACT STACK:

1. Aplicación móvil
   React Native + TypeScript
   Purpose: Interfaz de FUGA+ para visitantes y usuarios.

2. Backend
   Python + FastAPI
   Purpose: API, lógica del sistema, autenticación y conexión entre componentes.

3. IA
   OpenAI API
   Purpose: Extraer monto, categoría y descripción de los gastos.

4. Base de datos
   MongoDB
   Purpose: Usuarios, gastos, categorías, historial y estadísticas.

5. Caché
   Redis
   Purpose: Caché, sesiones/datos temporales y consultas frecuentes.

6. Autenticación
   JWT
   Purpose: Identificar usuarios y diferenciar Usuario/Administrador.

7. Contenedores
   Docker + Docker Compose
   Purpose: Ejecutar backend, MongoDB y Redis de forma organizada.

8. Consultas
   MongoDB Aggregation
   Purpose: Totales por categoría, estadísticas y análisis del dashboard.

9. Tiempo real
   MongoDB Change Streams
   Mark clearly as "(opcional)".
   Purpose: Actualizar información cuando cambien los datos.

10. Control de versiones
    Git + GitHub
    Purpose: Código y seguimiento del proyecto.

11. API
    OpenAPI/Swagger mediante FastAPI
    Purpose: Probar y documentar los endpoints.

ARCHITECTURE:

Create these visual layers:

A. PRESENTACIÓN
- Visitante
- Usuario
- Administrador
- React Native + TypeScript

B. BACKEND
- Python + FastAPI
- JWT

C. SERVICIOS DE IA
- OpenAI API

D. DATOS
- MongoDB
- MongoDB Aggregation
- MongoDB Change Streams (opcional)
- Redis

E. INFRAESTRUCTURA
- Docker + Docker Compose

F. DESARROLLO Y DOCUMENTACIÓN
- Git + GitHub
- OpenAPI/Swagger mediante FastAPI

CONNECTIONS:

- Visitante → React Native + TypeScript
- Usuario → React Native + TypeScript
- Administrador → React Native + TypeScript
- React Native + TypeScript → Python + FastAPI
  Label: "HTTPS / JSON"
- Python + FastAPI → JWT
  Label: "Autenticación"
- Python + FastAPI → OpenAI API
  Label: "Interpretación de gastos"
- Python + FastAPI → MongoDB
  Label: "Persistencia"
- Python + FastAPI → Redis
  Label: "Caché"
- Python + FastAPI → MongoDB Aggregation
  Label: "Consultas y estadísticas"
- MongoDB Aggregation → MongoDB
  Label: "Agregaciones"
- MongoDB Change Streams → MongoDB
  Label: "Cambios en datos"
- MongoDB Change Streams → Python + FastAPI
  Label: "Actualización en tiempo real"
- Docker + Docker Compose contains/hosts:
  Python + FastAPI
  MongoDB
  Redis
- OpenAPI/Swagger mediante FastAPI → Python + FastAPI
  Label: "Documentación y pruebas"
- Git + GitHub → Proyecto
  Label: "Control de versiones"

Inside the MongoDB component, show the main logical data:
- Usuarios
- Gastos
- Categorías
- Historial
- Estadísticas

Show the main functional flow clearly:

React Native + TypeScript
        ↓
Python + FastAPI
        ↓
MongoDB

And from FastAPI:
- → OpenAI API for expense interpretation
- → Redis for cache/temporary data
- → JWT for authentication
- → MongoDB Aggregation for dashboard statistics

IMPORTANT MODELING RULES:
- This is a TECHNOLOGICAL COMPONENT DIAGRAM, not a use-case diagram.
- Do not add class diagrams or UML classes.
- Do not add Node.js.
- Do not add Express.js.
- Do not add PostgreSQL.
- Do not add MySQL.
- Do not add Firebase.
- Do not add Auth0.
- Do not add Next.js.
- Do not add AWS, Azure or GCP.
- Do not add technologies that are not in the provided Stack.
- Do not invent additional components.

DRAW.IO REQUIREMENTS:
- Use proper UML/component-style shapes where appropriate.
- Use containers/groups for the architecture layers.
- Use directional connectors with readable labels.
- Avoid crossing lines where possible.
- Keep the diagram clean and readable.
- Make the main execution flow visually prominent.
- Clearly distinguish runtime components from development/documentation technologies.
- Clearly mark MongoDB Change Streams as optional.
- Use Spanish for descriptions, labels, layer names and purposes.
- Official technology names such as React Native, TypeScript, Python, FastAPI, OpenAI API, MongoDB, Redis, JWT, Docker, Docker Compose, Git, GitHub and OpenAPI/Swagger remain unchanged.

FINAL VERIFICATION:
1. Physically create docs/diagramas/diagrama-componentes.drawio.
2. Verify the file exists.
3. Verify the file is not empty.
4. Verify it is valid Draw.io XML that can be opened by diagrams.net.
5. Do not create any other files.
6. Do not merely claim that the file was created; actually create it and verify it.