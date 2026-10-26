Iteracion 5. ClaudeIA

# PROMPT: PLAN TÉCNICO DE DESARROLLO DE FUGA+

## Rol y objetivo
Actúa como arquitecto de software que acompaña un proyecto de grado. Analiza el proyecto FUGA+, que está en el directorio de trabajo actual, y produce un plan técnico que defina herramientas, frontend, backend, base de datos y orden de desarrollo, basado únicamente en la documentación y el código existentes. Esto es un plan, no una implementación: no escribas código ni implementes historias de usuario.

Trabaja con los archivos locales. No uses URLs ni busques el repositorio en internet.

**Archivo de destino:** `docs/respuestas-ia/plan_maestro.md`
**Idioma:** español.

## Contexto del proyecto
- Tipo de proyecto: proyecto de grado, app móvil con IA para detectar fugas de dinero.
- Tiempo disponible: 12 semanas efectivas.
- Tamaño del equipo: 1 persona
- Dedicación aproximada: 6 horas

Si algún dato falta, no lo supongas: márcalo como supuesto en el plan.

## Regla de control (máxima prioridad)
**Hasta que yo escriba "APROBADO", no uses herramientas de escritura ni edición, ni ejecutes comandos que modifiquen archivos.** Solo lectura. Si no sabes si una acción modifica algo, no la ejecutes.

## Fase 1: Revisión (solo lectura, sin proponer arquitectura)
Recorre el proyecto completo: README, historias de usuario, requerimientos funcionales y no funcionales, arquitectura y diseño, diagramas UML, estructura de carpetas, dependencias, configuraciones, integraciones existentes y cualquier otro documento que aclare el alcance. No te limites al README. Si algún archivo no se puede leer (por ejemplo, imágenes de diagramas), dilo expresamente y no afirmes haberlo revisado.

Entrega un resumen con:
1. **Archivos revisados** y **archivos que no pudiste abrir**.
2. **Estado del proyecto**, con estas etiquetas:
   - `[DEFINIDO]`: está en la documentación.
   - `[IMPLEMENTADO]`: ya existe en el código.
   - `[PENDIENTE]`: definido pero no implementado.
3. **Decisiones técnicas ya tomadas** (stack, motor de base de datos, servicios, etc.), indicando el archivo donde aparecen.
4. **Contradicciones** entre documentos. No elijas una versión arbitrariamente.
5. **Vacíos**: decisiones técnicas necesarias que la documentación no define.
6. **Historias de usuario y requerimientos**: ID, título corto y prioridad si está documentada.

Termina con "Fase 1 completa. ¿Procedo con la propuesta del plan?" y **espera mi respuesta**. No generes la propuesta en el mismo mensaje.

## Fase 2: Propuesta del plan (tras mi confirmación)
Preséntala en el chat, sin crear ni modificar archivos. Incluye todo lo necesario para poder desarrollar la aplicación, con la extensión que el contenido requiera. Evita únicamente el relleno y la repetición de documentación que ya existe.

**A. Herramientas y tecnologías**: para desarrollar, probar y administrar; para qué sirve cada una y si es indispensable u opcional. Revisa primero lo que ya existe en el proyecto.

**B. Frontend móvil**: tecnología, estructura de carpetas, módulos derivados de las historias y requerimientos, y comunicación con el backend.

**C. Backend**: tecnología, estructura de carpetas, módulos, endpoints (método, ruta y propósito), autenticación, permisos, validaciones y seguridad según los requerimientos no funcionales documentados.

**D. Base de datos**: motor, entidades o colecciones, campos esenciales y relaciones. Explica cómo se protegen los datos financieros del usuario y cómo se garantiza que cada usuario solo acceda a su propia información.

**E. Orden de desarrollo en 12 semanas**: de la configuración inicial a las pruebas finales, con el entregable de cada semana y las historias o requerimientos que cubre. Indica qué se recortaría primero si hay retraso, según la prioridad documentada, sin volver obligatorio lo opcional.

**F. Decisiones abiertas y riesgos**: decisiones que me corresponden, con 2 opciones y su principal contraste, y los riesgos técnicos principales.

### Reglas de contenido
- **Trazabilidad:** cada módulo, entidad y endpoint debe indicar la historia (HU-xx) o el requerimiento (RF/RNF-xx) que lo justifica. Si no puedes justificarlo con un ID, no lo incluyas.
- Etiqueta cada decisión como `[DEFINIDO]` o `[PROPUESTA]` (con una línea de justificación).
- No inventes funcionalidades, actores, módulos, campos ni tecnologías. No contradigas la documentación.
- No pidas información que ya está documentada.
- **Componente de IA:** usa lo que la documentación defina. Si no lo define, no elijas proveedor ni modelo: preséntalo en la sección F como decisión abierta con sus opciones.
- No agregues servicios o infraestructura sin una necesidad demostrable.
- No conviertas funcionalidades opcionales en obligatorias.

## Fase 3: Creación del archivo (solo tras escribir "APROBADO")
1. Verifica el nombre exacto de la carpeta `docs/prompts-diseño/` (tiene "ñ"). Si no existe, indícalo y créala. Después de crear el archivo, confirma que el nombre de la carpeta quedó con la "ñ" correcta.
2. Si `plan_maestro.md` ya existe, léelo primero, resúmeme qué contiene y qué cambiarías, y espera mi decisión.
3. Genera `plan_maestro.md` y confirma la ruta final.
4. **No modifiques** README, historias de usuario, requerimientos, diagramas ni ningún otro archivo.

## Reglas generales
- No hagas cuestionarios extensos. Pregunta solo lo estrictamente necesario, de una sola vez.
- Comienza ahora por la Fase 1.

Iteracion 5. ClaudeIA prompt de seguimiento
El plan_maestro.md quedó bien en cronograma, trazabilidad, modelo de datos y API, pero le faltan tres partes que son indispensables para empezar a desarrollar. Complétalas SIN modificar ni reescribir el contenido existente.

## Qué agregar
Añade al final de `docs/prompts-diseño/plan_maestro.md` una sección nueva llamada **"G. Estructura técnica del proyecto"**, sin renumerar ni alterar las secciones A–F.

### G.1 Estructura de carpetas del backend (FastAPI)
- Árbol completo de carpetas y archivos (bloque de código), con una línea de explicación por carpeta o archivo clave.
- Debe reflejar los componentes ya definidos en C.2: autenticación, autorización, gestión de gastos, procesamiento determinista (AnalizadorGasto, DiccionarioGasto), historial, dashboard, motor de fugas y acceso a datos con filtro obligatorio por usuarioId.
- Incluye dónde viven: configuración y variables de entorno, esquemas de validación, repositorios, reglas versionadas, diccionario versionado, pruebas (unitarias, integración y seguridad) y datos de prueba sintéticos.

### G.2 Estructura de carpetas del frontend (React Native + TypeScript)
- Árbol completo de carpetas y archivos, con una línea de explicación por carpeta o archivo clave.
- Incluye: pantallas (derivadas de las 13 historias Must), navegación, componentes reutilizables, servicios de API, manejo del token de sesión, estado, tipos TypeScript, utilidades de formato (moneda y fecha según D-03 y D-04) y pruebas.
- Lista las pantallas del MVP, cada una con la HU que la justifica, y explica cómo se comunican con el backend (cliente HTTP, manejo del JWT, estados de carga, vacío y error).

### G.3 Herramientas y tecnologías
- Lista de herramientas para desarrollar, probar y administrar (editor, gestor de paquetes, emulador o dispositivo, cliente de API, pruebas, control de versiones, Atlas, etc.).
- Para cada una: para qué sirve e indicar si es indispensable u opcional.
- Revisa primero package.json, requirements.txt, archivos de configuración y lo que ya exista en el repo. No agregues herramientas innecesarias.

## Reglas
- Antes de proponer los árboles, inspecciona las carpetas y archivos que YA existen en el repositorio. Distingue con etiquetas: `[EXISTE]` (ya está en el repo), `[PROPUESTA]` (carpeta nueva por crear).
- Usa las tecnologías ya definidas (React Native + TypeScript, Python + FastAPI, MongoDB Atlas). No cambies ni agregues librerías o servicios sin necesidad demostrable; si recomiendas una librería concreta (navegación, estado, cliente HTTP, hash, JWT, validación), márcala como `[PROPUESTA]` con una línea de justificación.
- No incluyas carpetas ni módulos de funcionalidades fuera del MVP (voz, Google, administración, metas, alertas, Cloudinary).
- Cada carpeta funcional importante debe citar la HU o RF que la justifica.
- Esto es estructura, no implementación: no escribas código de la aplicación ni crees las carpetas del proyecto.
- No modifiques ningún otro archivo.

Antes de escribir, muéstrame en el chat un resumen de lo que encontraste en el repo y espera mi "APROBADO" para actualizar el archivo.
