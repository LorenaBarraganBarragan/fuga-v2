# FUGA+

**Descubre por dónde se va tu plata.**

FUGA+ es una aplicación móvil para el control de gastos personales, dirigida principalmente a jóvenes y estudiantes. Su propósito es facilitar el registro de gastos cotidianos, ayudar a comprender los hábitos de consumo y detectar posibles fugas de dinero asociadas a gastos pequeños y repetitivos.

La aplicación permite registrar gastos mediante lenguaje natural, revisar y corregir los datos interpretados antes de confirmarlos, consultar el historial y visualizar estadísticas del comportamiento de los gastos.

La interpretación de los gastos se implementará mediante diccionarios y reglas determinísticas propias. La detección de posibles fugas también utilizará reglas explícitas y explicables, sin depender de una API externa de inteligencia artificial.

**Repositorio:** https://github.com/LorenaBarraganBarragan/fuga-v2

---

## 1. Problema

Los gastos pequeños del día a día pueden pasar desapercibidos y acumularse con el tiempo. Registrar manualmente cada movimiento puede resultar incómodo, provocar olvidos y disminuir el interés por llevar un seguimiento constante.

A partir de una entrevista con un usuario potencial, se identificó la necesidad de simplificar el registro de gastos y facilitar la consulta de la información financiera personal.

FUGA+ busca reducir esa dificultad mediante una experiencia de registro sencilla, un historial organizado y estadísticas comprensibles.

[Consultar entrevista](docs/entrevista-real.md)

## 2. Objetivos

### Objetivo general

Desarrollar un MVP móvil que facilite el registro y seguimiento de gastos personales mediante lenguaje natural, reglas de interpretación propias, estadísticas y detección explicable de posibles fugas de dinero.

### Objetivos específicos

- Facilitar el registro de gastos mediante texto y, como funcionalidad complementaria, voz en Android.
- Interpretar los datos del gasto y permitir su revisión antes de guardarlos.
- Almacenar los gastos asociados a la cuenta propietaria.
- Consultar el historial y las estadísticas de gastos.
- Detectar posibles fugas de dinero mediante reglas determinísticas.
- Proteger la privacidad y garantizar el aislamiento de los datos entre usuarios.
- Diseñar una arquitectura mantenible y viable para un proyecto académico individual de 12 semanas efectivas.

## 3. Público objetivo y actores

FUGA+ está dirigido principalmente a jóvenes y estudiantes que desean organizar sus gastos cotidianos sin utilizar herramientas financieras complejas.

| Actor | Responsabilidades |
|---|---|
| Visitante | Consultar información pública y acceder al registro o inicio de sesión. |
| Usuario | Gestionar su cuenta, registrar gastos, consultar el historial, revisar estadísticas y analizar posibles fugas. |
| Administrador | Consultar estadísticas agregadas y gestionar cuentas mediante operaciones autorizadas, sin acceder a los gastos individuales. |

El sistema debe aplicar la autorización en el backend. Ocultar botones en la interfaz no sustituye la validación de permisos ni el aislamiento de datos.

## 4. Propuesta de valor

FUGA+ busca que registrar un gasto sea más sencillo que completar formularios tradicionales.

Por ejemplo, el usuario puede escribir:

> Hoy gasté $8.000 en un taxi.

El sistema procesa el texto y propone campos como monto, categoría, descripción y fecha cuando pueda reconocerla. El usuario revisa y corrige los datos antes de confirmar el registro.

A partir de los gastos guardados, el sistema aplica reglas propias para identificar patrones que podrían representar fugas de dinero. Cada posible fuga debe poder explicarse mediante sus reglas, ocurrencias y gastos asociados.

Una posible fuga no representa una pérdida confirmada ni constituye una evaluación negativa de los hábitos del usuario.

## 5. Funcionalidades y alcance

### Funcionalidades del MVP

El MVP prioriza las siguientes capacidades:

- Consultar información pública.
- Registrarse e iniciar sesión con correo y contraseña.
- Cerrar sesión de forma segura.
- Registrar gastos mediante texto.
- Procesar el texto con diccionarios y reglas determinísticas.
- Revisar y corregir los campos antes de confirmar.
- Guardar cada gasto bajo su propietario.
- Consultar el historial de gastos.
- Consultar el total, la cantidad y el promedio de gastos por periodo.
- Consultar el gasto por categoría.
- Detectar posibles fugas de dinero mediante reglas.
- Consultar la evidencia que sustenta cada posible fuga.
- Aplicar autorización, privacidad y aislamiento entre usuarios.

### Funcionalidades complementarias

Se conservan en el backlog, pero no son necesarias para completar el MVP inicial:

- Inicio de sesión con Google.
- Recuperación de contraseña.
- Edición del perfil y fotografía.
- Filtros de historial.
- Edición y eliminación de gastos guardados.
- Entrada por voz en Android.
- Comparación de periodos.
- Alertas y sugerencias relacionadas con posibles fugas.
- Resumen mensual.
- Estadísticas administrativas agregadas y gestión de cuentas.

### Funcionalidades aplazadas

Las metas de gasto o ahorro y la consulta de su avance se conservan como funcionalidades futuras. Su implementación depende de definir el alcance de las metas y sus reglas de cálculo.

FUGA+ no contempla como parte del alcance actual:

- Conexiones bancarias.
- Pagos y transferencias.
- Créditos o préstamos.
- Inversiones.
- Asesoría financiera profesional.
- Entrenamiento de un modelo de IA propio.
- Interpretación obligatoria mediante APIs externas de IA.
- Notificaciones push remotas como requisito del MVP.

## 6. Historias de usuario

El proyecto cuenta con **33 historias de usuario**, identificadas de HU-01 a HU-33. Las prioridades siguen el modelo MoSCoW: Must Have, Should Have, Could Have y Won't Have (por ahora).

| ID | Historia de usuario | Prioridad | MVP |
|---|---|---|---|
| HU-01 | Consultar información pública y acceder al registro o inicio de sesión | Must Have | Sí |
| HU-02 | Registrarse e iniciar sesión con correo y contraseña | Must Have | Sí |
| HU-03 | Iniciar sesión con una cuenta de Google | Should Have | No |
| HU-04 | Cerrar sesión de forma segura | Must Have | Sí |
| HU-05 | Recuperar el acceso mediante restablecimiento de contraseña | Should Have | No |
| HU-06 | Desactivar la propia cuenta de usuario | Could Have | No |
| HU-07 | Consultar y editar nombres y teléfono del perfil | Should Have | No |
| HU-08 | Cambiar la foto de perfil | Should Have | No |
| HU-09 | Usar la foto de perfil de Google cuando esté disponible | Could Have | No |
| HU-10 | Registrar un gasto escrito en lenguaje natural | Must Have | Sí |
| HU-11 | Procesar el gasto con «Procesar con IA» y reglas determinísticas | Must Have | Sí |
| HU-12 | Revisar y corregir los campos interpretados antes de guardar | Must Have | Sí |
| HU-13 | Guardar el gasto bajo la cuenta propietaria y aislarlo de otros usuarios | Must Have | Sí |
| HU-14 | Consultar el historial de gastos del más reciente al más antiguo | Must Have | Sí |
| HU-15 | Filtrar el historial por fecha y categoría | Should Have | No |
| HU-16 | Editar y eliminar gastos guardados, actualizando análisis y resúmenes | Should Have | No |
| HU-17 | Iniciar la grabación de voz para un gasto en Android | Could Have | No |
| HU-18 | Convertir la voz en texto con Kotlin y `SpeechRecognizer` | Could Have | No |
| HU-19 | Revisar la transcripción y los campos antes de guardar un gasto por voz | Could Have | No |
| HU-20 | Consultar total, cantidad y promedio de gasto por periodo | Must Have | Sí |
| HU-21 | Consultar el gasto por categoría e identificar la categoría de mayor gasto | Must Have | Sí |
| HU-22 | Comparar el gasto entre periodos | Could Have | No |
| HU-23 | Detectar posibles fugas de dinero con reglas determinísticas | Must Have | Sí |
| HU-24 | Consultar la evidencia de una posible fuga de dinero | Must Have | Sí |
| HU-25 | Recibir alertas sobre posibles fugas de dinero | Could Have | No |
| HU-26 | Consultar sugerencias prácticas sobre posibles fugas | Could Have | No |
| HU-27 | Consultar el resumen mensual de posibles fugas | Could Have | No |
| HU-28 | Definir una meta mensual de gasto o ahorro con alcance explícito | Won't Have (por ahora) | No |
| HU-29 | Consultar el avance hacia la meta definida | Won't Have (por ahora) | No |
| HU-30 | Consultar estadísticas agregadas de uso sin acceder a gastos individuales | Should Have | No |
| HU-31 | Consultar usuarios registrados y la información administrativa necesaria | Should Have | No |
| HU-32 | Activar o desactivar cuentas de usuario desde funciones administrativas autorizadas | Should Have | No |
| HU-33 | Proteger la privacidad de los gastos y garantizar el aislamiento entre usuarios | Must Have | Sí |

**Distribución de prioridades:**

| Prioridad | Cantidad |
|---|---:|
| Must Have | 13 |
| Should Have | 9 |
| Could Have | 9 |
| Won't Have (por ahora) | 2 |
| **Total** | **33** |

HU-33 es una restricción transversal de seguridad y privacidad. Se verifica en el backend y en las operaciones que gestionan información, no mediante una pantalla independiente.

La especificación detallada, los criterios de aceptación, las dependencias y la trazabilidad se documentan en los archivos de requisitos e historias de usuario.

## 7. Requisitos funcionales

FUGA+ cuenta con **33 requisitos funcionales**, identificados de RF-001 a RF-033. Cada requisito se relaciona con una historia de usuario.

| Requisito | Funcionalidad | Historia |
|---|---|---|
| RF-001 | Información pública y acceso al registro o inicio de sesión | HU-01 |
| RF-002 | Registro e inicio de sesión con correo y contraseña | HU-02 |
| RF-003 | Inicio de sesión con Google | HU-03 |
| RF-004 | Cierre de sesión seguro | HU-04 |
| RF-005 | Restablecimiento de contraseña | HU-05 |
| RF-006 | Desactivación de la propia cuenta | HU-06 |
| RF-007 | Consulta y edición del perfil | HU-07 |
| RF-008 | Cambio de foto de perfil | HU-08 |
| RF-009 | Uso de la foto de perfil de Google | HU-09 |
| RF-010 | Registro de gastos mediante lenguaje natural | HU-10 |
| RF-011 | Procesamiento determinístico del texto del gasto | HU-11 |
| RF-012 | Revisión y corrección antes de guardar | HU-12 |
| RF-013 | Persistencia bajo el propietario y aislamiento de gastos | HU-13 |
| RF-014 | Historial ordenado y paginado | HU-14 |
| RF-015 | Filtros por fecha y categoría | HU-15 |
| RF-016 | Edición y eliminación de gastos con actualización de análisis | HU-16 |
| RF-017 | Inicio de grabación de voz en Android | HU-17 |
| RF-018 | Transcripción de voz mediante `SpeechRecognizer` | HU-18 |
| RF-019 | Revisión del gasto registrado por voz | HU-19 |
| RF-020 | Total, cantidad y promedio por periodo | HU-20 |
| RF-021 | Estadísticas por categoría | HU-21 |
| RF-022 | Comparación entre periodos | HU-22 |
| RF-023 | Detección de posibles fugas mediante reglas | HU-23 |
| RF-024 | Consulta de evidencia de posibles fugas | HU-24 |
| RF-025 | Alertas sobre posibles fugas | HU-25 |
| RF-026 | Sugerencias prácticas relacionadas con posibles fugas | HU-26 |
| RF-027 | Resumen mensual de posibles fugas | HU-27 |
| RF-028 | Definición de metas mensuales | HU-28 |
| RF-029 | Consulta del avance de metas | HU-29 |
| RF-030 | Estadísticas administrativas agregadas | HU-30 |
| RF-031 | Consulta administrativa de usuarios | HU-31 |
| RF-032 | Activación y desactivación administrativa de cuentas | HU-32 |
| RF-033 | Privacidad y aislamiento de datos entre usuarios | HU-33 |

La prioridad y la inclusión en el MVP de cada requisito se mantienen en la matriz de requisitos priorizados.

## 8. Requisitos no funcionales

El proyecto define **16 requisitos no funcionales** para establecer condiciones de seguridad, privacidad, calidad y mantenimiento.

| ID | Requisito |
|---|---|
| RNF-001 | Autorización obligatoria y aislamiento en el backend |
| RNF-002 | Privacidad y minimización de datos |
| RNF-003 | Protección de credenciales y sesiones |
| RNF-004 | Validación y rechazo de entradas no confiables |
| RNF-005 | Integridad transaccional e idempotencia |
| RNF-006 | Coherencia de agregados y análisis tras cambios |
| RNF-007 | Registro seguro y ausencia de datos sensibles en logs |
| RNF-008 | Transporte cifrado y manejo seguro de secretos |
| RNF-009 | Usabilidad del flujo de revisión y de los estados de error |
| RNF-010 | Transparencia de la etiqueta «Procesar con IA» |
| RNF-011 | Compatibilidad de plataformas y límites de Expo |
| RNF-012 | Fiabilidad, recuperación y ausencia de estados parciales |
| RNF-013 | Rendimiento y capacidad bajo condiciones representativas |
| RNF-014 | Mantenibilidad, versionado y pruebas automatizadas |
| RNF-015 | Auditabilidad de acciones administrativas |
| RNF-016 | Retención, desactivación y eliminación de datos |

Los requisitos no funcionales se aplican de acuerdo con su prioridad, las historias relacionadas y las decisiones pendientes. La privacidad y la seguridad no deben eliminarse para reducir el alcance.

## 9. Tecnologías y herramientas

La arquitectura prevista utiliza las siguientes tecnologías. Su estado de implementación debe verificarse en el repositorio.

| Componente | Tecnología | Propósito |
|---|---|---|
| Aplicación móvil | React Native + TypeScript | Interfaz móvil multiplataforma |
| Backend | Python + FastAPI | API y lógica de negocio |
| Base de datos | MongoDB Atlas | Persistencia documental en la nube |
| Consultas y estadísticas | MongoDB Aggregation | Agregación de gastos y estadísticas |
| Autenticación | JWT | Identificación de la sesión y autorización |
| Acceso con Google | Google Identity Services | Inicio de sesión complementario |
| Voz en Android | Kotlin + Android `SpeechRecognizer` | Conversión de voz en texto |
| Fotos de perfil | Cloudinary | Almacenamiento de imágenes |
| Notificaciones | Expo Notifications | Notificaciones compatibles con el alcance aprobado |
| Control de versiones | Git + GitHub | Historial y colaboración con el repositorio |
| Desarrollo | VS Code y Android Studio | Edición, compilación y depuración |
| Pruebas de API | Postman | Validación de endpoints |
| Documentación de API | OpenAPI / Swagger | Consulta y prueba de endpoints |
| Agente de desarrollo | OpenCode | Análisis del repositorio y apoyo a la implementación |
| Documentación técnica | Context7 | Consulta de documentación de bibliotecas |
| Integraciones externas | Composio | Acceso a integraciones compatibles, según configuración |
| Análisis de código | CodeGraphContext | Exploración de relaciones y dependencias, si está configurado |

### Decisiones técnicas

- MongoDB Atlas se utilizará inicialmente con el plan gratuito M0 si su capacidad y condiciones vigentes son suficientes.
- El backend debe validar los datos y aplicar los permisos, independientemente de las validaciones de la aplicación móvil.
- Las credenciales y claves privadas deben mantenerse en variables de entorno o mecanismos seguros, nunca en el repositorio.
- Redis y Docker no se consideran dependencias obligatorias del MVP hasta justificar su necesidad y validar su configuración.
- La interpretación del gasto no requiere OpenAI API ni otra API externa de IA.
- El reconocimiento de voz es complementario y requiere una compilación de Android que incluya el módulo nativo; no se debe asumir compatibilidad con Expo Go.
- Los servicios externos deben evaluarse considerando disponibilidad, límites, configuración y posibles costos.

## 10. Interpretación de gastos y detección de fugas

### Interpretación del gasto

El procesamiento utiliza diccionarios propios y reglas determinísticas para proponer:

- Monto.
- Categoría.
- Descripción.
- Fecha, cuando se reconozca.
- Texto original del usuario.

El botón de la interfaz conserva la etiqueta «Procesar con IA» por decisión de requisitos, pero el mecanismo implementado debe explicarse transparentemente: se utilizarán reglas propias y no una API externa de IA.

El procesamiento genera un borrador. No guarda automáticamente el gasto. El usuario debe revisar los datos y confirmar la operación.

### Detección de posibles fugas

La detección se basa en reglas determinísticas versionadas y criterios aprobados por el proyecto.

Cada resultado debe explicar la regla aplicada, las ocurrencias identificadas, el periodo analizado y los gastos que sustentan el resultado.

Los umbrales de monto, frecuencia, ventanas de tiempo y condiciones mínimas deben definirse antes de implementar las reglas. No deben inventarse valores para presentar resultados artificiales.

## 11. Arquitectura

La solución se organiza conceptualmente en tres capas principales:

1. **Aplicación móvil:** presenta la interfaz, recoge los datos, permite revisar los gastos y muestra el historial y las estadísticas.
2. **Backend:** autentica las solicitudes, valida los datos, aplica las reglas de negocio, controla los permisos y expone la API.
3. **Persistencia:** almacena usuarios, gastos, categorías y la información necesaria para generar estadísticas y evidencias.

Los servicios externos se incorporan únicamente cuando corresponda a una funcionalidad aprobada.

La arquitectura detallada y los diagramas deben mantenerse alineados con las historias, los requisitos y la estructura real del código.

- [Arquitectura](docs/architecture.md)
- [Diagramas del sistema](docs/diagramas/)
- [Plan maestro](docs/prompts-diseño/plan_maestro.md)

## 12. Seguridad y privacidad

FUGA+ debe cumplir las siguientes reglas:

- Cada gasto pertenece a un único usuario.
- El backend obtiene la identidad del propietario desde una sesión validada, no desde un identificador enviado libremente por el cliente.
- Un usuario no puede consultar, modificar ni eliminar gastos de otra cuenta.
- El Administrador no puede acceder a los gastos individuales.
- Las estadísticas administrativas deben utilizar datos agregados y limitarse a la información autorizada.
- Las contraseñas no se almacenan en texto plano.
- Los tokens, claves y datos financieros sensibles no deben aparecer en registros técnicos.
- Las operaciones de edición y eliminación deben mantener coherentes el historial, las estadísticas y las posibles fugas.
- Las políticas de retención y eliminación deben definirse antes de habilitar operaciones irreversibles.

## 13. Plan de desarrollo

El proyecto se desarrolla individualmente en 12 semanas efectivas.

| Etapa | Trabajo principal | Resultado esperado |
|---|---|---|
| Semanas 1–2 | Entorno, estructura, acceso, autenticación y seguridad inicial | Aplicación ejecutable y gestión de sesiones |
| Semanas 3–4 | Registro de gastos, procesamiento determinístico, revisión y guardado | Flujo de registro funcional |
| Semana 5 | Historial y estadísticas básicas | Consulta de movimientos y dashboard |
| Semana 6 | Detección de fugas y evidencia | Análisis explicable basado en reglas |
| Semana 7 | Integración, pruebas de seguridad y estabilización | MVP integrado y demostrable |
| Semanas 8–10 | Funcionalidades complementarias priorizadas | Mejoras según tiempo y dependencias |
| Semana 11 | Complementos seleccionados y pruebas de rendimiento | Funcionalidades adicionales estables, si es viable |
| Semana 12 | Regresión, documentación y preparación de la entrega | Versión final documentada y probada |

El orden definitivo debe seguir la matriz de dependencias y los criterios de aceptación. Las funcionalidades complementarias no deben retrasar la seguridad ni el flujo principal del MVP.

## 14. Pruebas y criterios de aceptación

La validación debe incluir:

- Pruebas de registro, inicio y cierre de sesión.
- Validación de textos y montos inválidos.
- Pruebas del diccionario y las reglas determinísticas.
- Verificación de la revisión obligatoria antes del guardado.
- Pruebas de persistencia, reintentos y prevención de duplicados.
- Pruebas de aislamiento entre usuarios.
- Verificación de que el Administrador no acceda a gastos individuales.
- Pruebas de historial, estadísticas y detección de fugas.
- Pruebas de recuperación ante errores de red y del backend.
- Pruebas de regresión tras cada cambio relevante.

Una funcionalidad no debe marcarse como terminada solo porque exista una pantalla: también debe funcionar en el backend, persistir los datos cuando corresponda y cumplir sus criterios de aceptación.

## 15. Documentación del proyecto

### Requisitos y análisis

- [Entrevista real](docs/entrevista-real.md)
- [Visión del proyecto](docs/respuestas-ia/salida-vision.md)
- [Análisis competitivo](docs/respuestas-ia/salida-analisis-competitivo.md)
- [Historias de usuario](docs/respuestas-ia/salida-historias-usuario.md)
- [Requisitos priorizados y trazabilidad](docs/respuestas-ia/salida-requerimientos-priorizados.md)

### Arquitectura y diseño

- [Arquitectura](docs/architecture.md)
- [Diagramas](docs/diagramas/)
- [Prompts de análisis y diseño](docs/prompts-diseño/)
- [Plan maestro](docs/prompts-diseño/plan_maestro.md)

Los enlaces deben verificarse contra el árbol real del repositorio. Si un documento todavía no existe, debe crearse como tarea de documentación o retirarse temporalmente el enlace hasta que esté disponible.

## 16. Uso de herramientas de inteligencia artificial

Durante el análisis y desarrollo pueden utilizarse asistentes de IA para apoyar:

- La revisión de requisitos e historias de usuario.
- La planificación de la arquitectura.
- La consulta de documentación técnica.
- El análisis de código y dependencias.
- La generación inicial de código y pruebas.
- La revisión de documentación.

Todo resultado debe revisarse antes de incorporarse al proyecto. La asistencia de desarrollo no sustituye las pruebas ni la validación de los requisitos.

La funcionalidad de interpretación de gastos de FUGA+ no depende de un proveedor externo de modelos de IA. Se basa en reglas y diccionarios propios, mientras que la detección de fugas utiliza reglas determinísticas explicables.

## 17. Estado del proyecto

FUGA+ es un proyecto académico de Ingeniería de Sistemas, desarrollado individualmente en el marco de Electiva CPC.

El proyecto cuenta con documentación de visión, historias de usuario, requisitos priorizados, trazabilidad y diseño. La implementación funcional debe evaluarse según el estado real del repositorio y los resultados de las pruebas.

Las funcionalidades deben identificarse como **definidas**, **en desarrollo**, **implementadas** o **validadas**, evitando afirmar que están terminadas sin evidencia.

## 18. Autor

**Lorena Barragan Barragan**

Proyecto académico — Ingeniería de Sistemas  
Electiva CPC — Periodo académico 2026-2
