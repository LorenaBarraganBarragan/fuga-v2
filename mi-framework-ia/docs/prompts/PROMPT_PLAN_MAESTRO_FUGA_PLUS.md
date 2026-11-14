# PROMPT MAESTRO — PLAN DE IMPLEMENTACIÓN INTEGRAL DE FUGA+

**Proyecto:** FUGA+  
**Modalidad:** Aplicación móvil  
**Herramienta:** OpenCode  
**Modo de ejecución inicial:** PLAN  
**Objetivo:** Generar un plan técnico integral que posteriormente será ejecutado en modo BUILD.

---

## 1. ROL Y RESPONSABILIDAD

Actúa como un equipo multidisciplinario de ingeniería de software compuesto por:

- Arquitecto de software senior.
- Ingeniero de sistemas.
- Desarrollador móvil especialista en React Native y TypeScript.
- Desarrollador backend especialista en FastAPI y Python.
- Especialista en PostgreSQL y Supabase.
- Ingeniero de seguridad y autenticación.
- Diseñador UI/UX especializado en aplicaciones móviles.
- Especialista en integración de servicios externos.
- Ingeniero de pruebas y aseguramiento de calidad.
- Ingeniero DevOps y gestor técnico de proyectos.

Tu responsabilidad es analizar la documentación vigente de FUGA+ y producir un **Plan Maestro de Implementación Integral**, suficientemente detallado para orientar el desarrollo completo de la aplicación.

El proyecto es individual, académico y está orientado principalmente a jóvenes y estudiantes que desean comprender y controlar sus gastos personales.

El horizonte de referencia del proyecto es de 12 semanas, pero la implementación podrá ejecutarse mediante sesiones autónomas prolongadas.

**Durante esta ejecución únicamente debes analizar y planificar. No debes implementar funcionalidades.**

---

## 2. REGLAS SOBRE LAS FUENTES DE INFORMACIÓN

### 2.1. Restricción absoluta sobre el README

Los archivos `README.md` del repositorio contienen información desactualizada.

Por tanto:

- NO leas ni utilices ningún `README.md` como fuente del plan.
- NO tomes decisiones de arquitectura, tecnologías, funcionalidades o alcance basándote en README antiguos.
- NO actualices los README durante esta ejecución.
- NO uses información histórica para reemplazar decisiones documentadas recientemente.

Si una herramienta muestra automáticamente contenido de un README, ignóralo como fuente de decisiones.

### 2.2. Documentación autorizada

Analiza prioritariamente:

1. `mi-framework-ia/docs/requerimientos/REQUERIMIENTOS.md`
2. `mi-framework-ia/docs/historias-usuario/HISTORIAS_DE_USUARIO.md`
3. Los cinco diagramas de `mi-framework-ia/docs/diagramas/`.
4. Los documentos de decisiones técnicas vigentes, si existen.
5. Los documentos de arquitectura y configuración que estén actualizados.
6. Las configuraciones técnicas necesarias para auditar herramientas y MCP.
7. Los recursos gráficos oficiales de `assets/`.

Verifica la existencia de los 33 requerimientos funcionales, 16 requerimientos no funcionales y 33 historias de usuario, sin asumir que todos mantienen exactamente la misma numeración o estado.

Establece una jerarquía de fuentes: decisiones aprobadas vigentes, requerimientos e historias actualizados, diagramas compatibles y recursos visuales oficiales.

Ante contradicciones, documenta el conflicto y la decisión que necesita validación.

No inventes funcionalidades ni conviertas propuestas pendientes en decisiones aprobadas.

---

## 3. AUDITORÍA DEL ESTADO ACTUAL DEL PROYECTO

Antes de generar el plan:

1. Identifica la estructura real del repositorio.
2. Determina qué archivos son documentación, configuración, prototipos o código funcional.
3. Comprueba qué funcionalidades están implementadas realmente.
4. Identifica dependencias instaladas y faltantes.
5. Detecta documentos obsoletos, sin eliminarlos.
6. Verifica la coherencia de los diagramas con los requisitos.
7. Identifica las decisiones aprobadas, pendientes y descartadas.
8. Evalúa los riesgos de implementar el proyecto con las tecnologías seleccionadas.
9. Determina qué configuraciones externas son necesarias.
10. Identifica tareas que pueden ejecutarse automáticamente y tareas que requieren intervención humana.

No confundas archivos de configuración existentes con integraciones operativas.

Preserva la estructura y el contenido de `mi-framework-ia`. No lo conviertas automáticamente en el motor de ejecución de la aplicación.

---

## 4. IDENTIDAD VISUAL OFICIAL DE FUGA+

### 4.1. Logo

El logo oficial está ubicado en:

`assets/logo/logo.png`

Este archivo es obligatorio como recurso visual del proyecto.

Debes:

- Verificar su existencia.
- Conservar su diseño original.
- Mantener sus proporciones.
- No modificar sus colores.
- No redibujarlo.
- No reemplazarlo por iconos genéricos.
- Planificar su uso en bienvenida, autenticación y demás ubicaciones apropiadas.
- Considerar los recursos necesarios para el icono de Android y la pantalla de inicio, respetando los requisitos técnicos de cada formato.

### 4.2. Paleta de colores oficial

La identidad visual proviene del sistema de diseño **Petrol Mint Vitality**, creado en Google Stitch.

Los colores aprobados son:

| Token | Color | HEX |
|---|---|---|
| Primary | Verde petróleo | `#1A5B5A` |
| Secondary | Verde menta | `#A2E8D3` |
| Tertiary | Ámbar | `#F5A623` |
| Neutral | Gris oscuro | `#243332` |

Utiliza estos valores como fuente de verdad.

El ámbar debe utilizarse como acento puntual y no dominar la interfaz.

Los colores adicionales para superficies, fondos, bordes, errores, advertencias y estados deben derivarse de un sistema coherente y documentarse explícitamente.

### 4.3. Tipografía

**Familia oficial: Plus Jakarta Sans.**

Planifica su utilización en:

- Encabezados.
- Títulos.
- Cuerpo de texto.
- Etiquetas.
- Botones.
- Formularios.
- Estadísticas y tarjetas.

Define una escala tipográfica consistente y accesible.

### 4.4. Estilo de interfaz

El sistema de diseño debe contemplar:

- Interfaz móvil moderna.
- Tarjetas con bordes redondeados.
- Botones tipo píldora cuando corresponda.
- Superficies claras.
- Iconografía consistente.
- Formularios legibles.
- Navegación sencilla.
- Jerarquía visual clara.
- Estados de carga, vacío, error y éxito.
- Accesibilidad y contraste suficiente.
- Componentes reutilizables.

### 4.5. Restricción sobre los diseños antiguos de Stitch

Las pantallas antiguas de Stitch fueron creadas antes de actualizar los requerimientos y las historias de usuario.

Por tanto:

- NO utilices esas pantallas como definición funcional vigente.
- NO reproduzcas flujos antiguos sin validación.
- NO inventes funcionalidades basándote en diseños desactualizados.
- Utiliza Stitch exclusivamente como referencia de identidad visual, componentes y estilo.
- Diseña las pantallas definitivas conforme a los requerimientos e historias de usuario actualizados.

Planifica un sistema centralizado de tokens visuales para React Native.

---

## 5. ARQUITECTURA GENERAL DE LA APLICACIÓN

Define la arquitectura técnica de FUGA+ considerando:

- Aplicación móvil.
- Backend independiente.
- Persistencia de datos.
- Autenticación y autorización.
- Integraciones externas.
- Procesamiento determinista de gastos.
- Seguridad.
- Escalabilidad razonable para un proyecto académico.
- Mantenibilidad.
- Pruebas automatizadas.

Documenta:

1. Componentes principales.
2. Responsabilidades.
3. Comunicación entre capas.
4. Flujo de información.
5. Dependencias.
6. Gestión de errores.
7. Configuración por entorno.
8. Separación de lógica de negocio e infraestructura.

Evita introducir complejidad innecesaria.

---

## 6. TECNOLOGÍAS DEL FRONTEND

La aplicación móvil utilizará:

- React Native.
- TypeScript.

Analiza y define las herramientas complementarias necesarias para:

- Navegación.
- Gestión de estado.
- Formularios.
- Validaciones.
- Consumo de API.
- Manejo de sesiones.
- Almacenamiento seguro.
- Gestión de recursos visuales.
- Estadísticas y gráficos.
- Pruebas.
- Compilación Android.

Justifica cada dependencia adicional.

Considera la compatibilidad entre React Native, Expo y las funcionalidades nativas Android.

No elijas librerías que impidan utilizar el reconocimiento de voz nativo aprobado.

---

## 7. TECNOLOGÍAS DEL BACKEND

El backend utilizará:

- Python.
- FastAPI.

Planifica:

1. Organización de carpetas.
2. Endpoints REST.
3. Modelos de entrada y salida.
4. Validaciones.
5. Servicios de negocio.
6. Repositorios de datos.
7. Manejo centralizado de errores.
8. Autorización.
9. Integración con Supabase.
10. Registro de eventos técnicos.
11. Pruebas automatizadas.
12. Configuración de entornos.

No introduzcas servicios adicionales sin necesidad justificada.

---

## 8. BASE DE DATOS Y SUPABASE

La persistencia propuesta es:

- Supabase.
- PostgreSQL.

Planifica:

- Modelo entidad-relación.
- Tablas.
- Columnas.
- Tipos de datos.
- Claves primarias y foráneas.
- Restricciones.
- Índices.
- Migraciones.
- Datos ficticios de prueba.
- Integridad referencial.
- Políticas Row Level Security.
- Aislamiento de datos por usuario.
- Procedimientos de validación.

Distingue entre lo que OpenCode puede generar automáticamente y lo que requiere configuración de la cuenta de Supabase.

No presupongas que la base de datos ya está creada o conectada.

---

## 9. AUTENTICACIÓN Y AUTORIZACIÓN

Revisa las decisiones vigentes relacionadas con:

- Supabase Auth.
- Inicio de sesión mediante correo y contraseña.
- Inicio de sesión con Google.
- Recuperación de acceso.
- Gestión de sesiones.
- Verificación de identidad.
- Tokens.
- Permisos por rol.

No implementes un sistema JWT independiente si la arquitectura aprobada utiliza los mecanismos de sesión de Supabase Auth.

Verifica las decisiones documentadas antes de seleccionar el flujo definitivo.

Diseña la autorización tanto en el frontend como en el backend y la base de datos.

---

## 10. ROLES DE FUGA+

Considera los roles:

1. Visitante.
2. Usuario.
3. Administrador.

Para cada rol define:

- Permisos.
- Pantallas.
- Navegación.
- Acciones disponibles.
- Restricciones.
- Endpoints autorizados.
- Acceso a información.
- Criterios de seguridad.
- Pruebas.

El administrador no debe disponer de acceso indiscriminado a los gastos personales de otros usuarios.

Las capacidades exactas de cada rol deben derivarse de los documentos vigentes.

---

## 11. MÓDULOS FUNCIONALES

Identifica y planifica todas las funcionalidades aprobadas.

Verifica especialmente:

- Registro de usuarios.
- Inicio de sesión.
- Recuperación de acceso.
- Gestión de perfil.
- Registro de gastos.
- Interpretación de texto natural mediante reglas.
- Identificación de monto, moneda, categoría y descripción.
- Revisión y corrección obligatoria.
- Confirmación y almacenamiento.
- Historial.
- Consulta, edición y eliminación de gastos.
- Dashboard.
- Estadísticas.
- Identificación de posibles fugas.
- Notificaciones.
- Reconocimiento de voz.
- Funcionalidades administrativas.

La lista anterior es una referencia de análisis, no una autorización para agregar funcionalidades ausentes de los requisitos.

Para cada módulo especifica:

1. Requerimientos asociados.
2. Historias de usuario.
3. Reglas de negocio.
4. Pantallas.
5. Componentes.
6. Endpoints.
7. Servicios.
8. Persistencia.
9. Validaciones.
10. Seguridad.
11. Pruebas.
12. Criterios de aceptación.

---

## 12. PROCESAMIENTO DE GASTOS

El procesamiento de texto se realizará mediante reglas deterministas y diccionarios.

No utilizar APIs externas de inteligencia artificial generativa.

Ejemplo conceptual:

"Hoy gasté $8.000 en un taxi".

La aplicación debe identificar los datos pertinentes según las reglas aprobadas, presentar una revisión editable y guardar el registro únicamente después de la confirmación del usuario.

Planifica:

- Normalización de texto.
- Extracción de montos.
- Formato colombiano.
- Identificación de categorías.
- Tratamiento de ambigüedades.
- Validaciones.
- Confirmación obligatoria.
- Manejo de entradas inválidas.
- Pruebas con ejemplos variados.

No presupongas reglas de clasificación no aprobadas.

---

## 13. DETECCIÓN DE POSIBLES FUGAS

Planifica una detección explicable basada en los gastos realmente registrados.

No utilizar predicciones injustificadas ni juicios sobre el comportamiento financiero.

Define la implementación únicamente a partir de las reglas aprobadas.

Cuando una regla esté pendiente, identifícala como decisión bloqueante o pendiente de definición.

Las posibles fugas deben poder justificarse mediante evidencia verificable.

---

## 14. INTEGRACIONES EXTERNAS

Analiza las integraciones contempladas:

- Supabase.
- Google Identity.
- Cloudinary.
- Android SpeechRecognizer mediante Kotlin.
- Expo Notifications.
- Otros servicios explícitamente aprobados.

Para cada integración documenta:

- Propósito.
- Dependencias.
- Requisitos.
- Compatibilidad.
- Configuración.
- Variables de entorno.
- Credenciales necesarias.
- Actividades automatizables.
- Actividades manuales.
- Costos potenciales.
- Pruebas.
- Alternativas en caso de bloqueo.

No declares operativa una integración sin comprobarla.

---

## 15. AUDITORÍA DE SERVIDORES MCP

Revisa las configuraciones existentes:

- `mi-framework-ia/mcp.json`.
- `mi-framework-ia/opencode.json`.
- Configuraciones MCP globales accesibles.
- Herramientas disponibles en OpenCode.

Investiga los servidores instalados y configurados, incluidos Context7, Chrome DevTools u otros que realmente aparezcan.

Para cada servidor indica:

1. Nombre.
2. Función.
3. Ubicación de configuración.
4. Estado verificado.
5. Utilidad para FUGA+.
6. Dependencias.
7. Costos o limitaciones.
8. Recomendación.

Determina si los MCP actuales son suficientes.

Solo recomienda nuevos servidores cuando aporten una capacidad necesaria que no esté cubierta.

No instales ni modifiques MCP automáticamente.

---

## 16. CONFIGURACIONES MANUALES DE LA PROPIETARIA

Crea una sección específica para las actividades que no puede completar el agente sin intervención humana.

Incluye, según corresponda:

- Creación del proyecto Supabase.
- Configuración de PostgreSQL.
- Configuración de Supabase Auth.
- Credenciales OAuth de Google.
- Configuración de Cloudinary.
- Permisos Android.
- Servicios de notificaciones.
- Configuración del alojamiento del backend.
- Variables de entorno.
- Pruebas en dispositivo.
- Verificación de costos.

Cada procedimiento debe indicar:

1. Cuándo debe realizarse.
2. Qué servicio utilizar.
3. Qué configuración crear.
4. Qué información necesita el código.
5. Dónde se debe guardar de forma segura.
6. Cómo comprobar el resultado.
7. Qué ocurre si se pospone.

No solicitar contraseñas ni secretos dentro de archivos versionados.

---

## 17. ESTRATEGIA DE IMPLEMENTACIÓN AUTÓNOMA

El plan deberá estar preparado para ejecutarse posteriormente en OpenCode mediante el modo BUILD.

El objetivo será realizar una implementación continua, sin solicitar aprobaciones entre fases técnicas ordinarias.

Durante la futura ejecución:

- Implementar módulos según dependencias.
- Ejecutar pruebas.
- Corregir errores ordinarios.
- Continuar automáticamente entre fases.
- Registrar avances.
- Evitar repetir tareas completadas.
- Documentar bloqueos.
- Continuar con módulos independientes si faltan servicios externos.
- Mantener el proyecto compilable.
- No afirmar que algo funciona sin pruebas.

La autonomía no autoriza operaciones destructivas, publicación de secretos, contratación de servicios ni gastos sin aprobación.

No se debe garantizar una duración específica ni una ejecución ininterrumpida si existen límites de herramientas, permisos o sesiones.

---

## 18. FASES DEL PLAN MAESTRO

Organiza la implementación en fases técnicas dependientes.

Para cada fase documenta:

1. Identificador.
2. Nombre.
3. Objetivo.
4. Requisitos e historias relacionadas.
5. Dependencias.
6. Actividades detalladas.
7. Archivos y carpetas.
8. Frontend.
9. Backend.
10. Base de datos.
11. Integraciones.
12. Comandos necesarios.
13. Pruebas.
14. Criterios de aceptación.
15. Entregables.
16. Riesgos.
17. Condiciones de continuación.
18. Estimación de esfuerzo.

Incluye una matriz de trazabilidad entre requerimientos, historias de usuario, módulos, fases y pruebas.

La planificación debe permitir ejecutar toda la aplicación, no solamente crear un prototipo visual.

---

## 19. PRUEBAS Y VALIDACIÓN

Define una estrategia de calidad que incluya:

- Pruebas unitarias.
- Pruebas de integración.
- Pruebas de API.
- Pruebas de autenticación.
- Pruebas de autorización.
- Pruebas de base de datos.
- Pruebas de reglas de negocio.
- Pruebas de interfaz.
- Pruebas de navegación.
- Pruebas de casos límite.
- Validación de historias de usuario.
- Compilación Android.
- Pruebas en emulador o dispositivo cuando estén disponibles.

Establece criterios verificables para considerar completada cada funcionalidad.

---

## 20. CONTROL DE COSTOS

FUGA+ es un proyecto académico individual.

Prioriza servicios gratuitos o con niveles gratuitos adecuados para el alcance.

Analiza los costos potenciales de:

- Supabase.
- Alojamiento del backend.
- Cloudinary.
- Autenticación.
- Google OAuth.
- Notificaciones.
- Herramientas de desarrollo.
- Compilación y distribución móvil.

Distingue entre límites gratuitos verificados, estimaciones y condiciones pendientes de comprobar.

No actives servicios de pago.

---

## 21. GIT Y CONTROL DE VERSIONES

El repositorio utilizará únicamente dos ramas permanentes:

- `main`: documentación aprobada y versiones estables.
- `develop`: implementación y pruebas.

El prompt y el plan maestro aprobados deberán conservarse en `main`.

La implementación posterior se realizará en `develop`.

No crees ramas adicionales.

No ejecutes commits, merges, pushes ni operaciones destructivas durante la generación del plan.

Incluye en el plan el procedimiento para sincronizar `develop` con `main` antes de comenzar la implementación.

---

## 22. CONTINUIDAD DE EJECUCIÓN

Define un mecanismo de recuperación para ejecuciones prolongadas.

Durante BUILD se deberán mantener archivos de seguimiento que registren:

- Fases completadas.
- Funcionalidades implementadas.
- Archivos modificados.
- Pruebas ejecutadas.
- Errores.
- Dependencias pendientes.
- Configuraciones manuales.
- Siguiente tarea.

El agente deberá poder recuperar el contexto después de una interrupción.

No debe declarar completadas tareas sin evidencias.

---

## 23. ENTREGABLE DEL MODO PLAN

Genera el documento:

`mi-framework-ia/docs/planificacion/PLAN_MAESTRO_IMPLEMENTACION_FUGA_PLUS.md`

El documento debe contener, como mínimo:

1. Resumen ejecutivo.
2. Alcance del proyecto.
3. Fuentes documentales y jerarquía.
4. Estado actual del repositorio.
5. Requisitos y decisiones.
6. Arquitectura.
7. Tecnologías frontend.
8. Tecnologías backend.
9. Modelo de datos.
10. Autenticación y seguridad.
11. Roles.
12. Identidad visual.
13. Logo oficial.
14. Sistema de diseño.
15. Módulos funcionales.
16. Reglas de negocio.
17. Integraciones externas.
18. Auditoría MCP.
19. Configuraciones manuales.
20. Fases de implementación.
21. Matriz de trazabilidad.
22. Estrategia de pruebas.
23. Costos.
24. Riesgos.
25. Plan de continuidad.
26. Criterios de aceptación final.
27. Procedimiento de transición de PLAN a BUILD.

No generes un plan superficial.

Cada fase debe proporcionar instrucciones concretas, dependencias y resultados verificables para que pueda ser ejecutada posteriormente por un agente de programación.

---

## 24. RESTRICCIONES FINALES

Durante esta ejecución:

- NO programes la aplicación.
- NO modifiques código funcional.
- NO utilices los README desactualizados.
- NO alteres el logo.
- NO reemplaces la paleta aprobada.
- NO utilices pantallas antiguas como requisitos.
- NO inventes historias de usuario.
- NO introduzcas tecnologías innecesarias.
- NO modifiques el framework existente.
- NO instales MCP adicionales.
- NO ejecutes operaciones destructivas.
- NO hagas commits ni pushes.
- NO afirmes que una integración está operativa sin verificarla.

Si el modo PLAN no permite crear archivos, presenta el plan completo y solicita exclusivamente la operación necesaria para guardarlo, sin iniciar la implementación.

**RESULTADO ESPERADO:**

Un Plan Maestro de Implementación Integral de FUGA+, basado en la documentación vigente, compatible con las tecnologías aprobadas, fiel a su identidad visual y preparado para una ejecución posterior autónoma y continua mediante OpenCode en modo BUILD.