# FUGA+ — Historias de usuario revisadas y priorizadas

## 1. Identificación del documento

| Campo | Valor |
|---|---|
| **Proyecto** | FUGA+ — aplicación móvil para registrar gastos y detectar posibles fugas de dinero |
| **Documento** | Revisión, mejora, organización y priorización de las 33 historias de usuario |
| **Versión** | 1.0 |
| **Fecha de actualización** | 25 de octubre de 2026 |
| **Estado** | Documento de trabajo para planificación; contiene decisiones pendientes de validación |
| **Archivo** | `docs/respuestas-ia/salida-historias-usuario.md` |
| **Fuente de trazabilidad** | Historias originales HU-01 a HU-33 |
| **Horizonte de planificación** | 12 semanas, desarrollo individual asistido por herramientas de IA |

> **Alcance de este documento:** es el documento único de historias de usuario de FUGA+. No crea un archivo por historia, no reemplaza la documentación de arquitectura y no modifica código, configuración, dependencias ni diagramas.

---

## 2. Objetivo y alcance

### 2.1 Objetivo

Revisar y mejorar las 33 historias de usuario originales de FUGA+, conservando sus identificadores HU-01 a HU-33, para que puedan usarse como base de planificación de un MVP de 12 semanas. Cada historia debe ser comprensible, verificable, priorizada y trazable respecto de su propósito original.

El documento también debe hacer explícitas las decisiones que aún no están acordadas —especialmente las reglas de detección de fugas, el catálogo de categorías, la moneda, las fechas y el alcance de las metas— sin inventar valores ni comportamientos.

### 2.2 Alcance incluido

- Las 33 historias funcionales originales, agrupadas en sus ocho módulos.
- Criterios de aceptación verificables en formato **Dado / Cuando / Entonces**.
- Reglas de negocio, validaciones, errores esperados, dependencias y pruebas sugeridas.
- Priorización MoSCoW justificada por historia.
- Matriz de dependencias, matriz de trazabilidad, alcance del MVP, funciones postergadas y plan de 12 semanas.
- Decisiones pendientes, riesgos y supuestos que requieren validación.

### 2.3 Alcance excluido

- Implementación de código, cambios de configuración, instalación de dependencias o modificación de diagramas.
- Conexiones bancarias, pagos, transferencias, tarjetas, créditos, préstamos, inversiones y asesoría financiera profesional.
- Entrenamiento de modelos de IA propios y uso de una API externa de IA para interpretar gastos.
- Definición unilateral de umbrales, montos mínimos, frecuencias o ventanas de detección de fugas.
- Compromisos de fechas exactas de entrega o estimaciones horarias detalladas.

### 2.4 Criterio de éxito del documento

El documento se considera completo cuando las 33 historias están presentes, cada una tiene prioridad justificada y criterios verificables, las dependencias no presentan ciclos, el MVP es coherente con 12 semanas y las decisiones pendientes están separadas de las decisiones acordadas.

---

## 3. Contexto funcional y decisiones técnicas acordadas

FUGA+ está dirigida a jóvenes y estudiantes. Permite registrar gastos en lenguaje natural, revisar y corregir la interpretación antes de guardarlos, consultar el historial, visualizar estadísticas e identificar posibles fugas de dinero entendidas como gastos pequeños y repetitivos detectados por reglas deterministas.

### 3.1 Decisiones técnicas que se conservan

| Área | Decisión acordada | Implicación para las historias |
|---|---|---|
| Aplicación móvil | React Native + TypeScript | La interfaz, la navegación y la revisión de gastos se implementan en la app móvil. |
| Backend | Python + FastAPI | La autenticación, la propiedad de los gastos, las agregaciones y las reglas de negocio se validan en el servidor. |
| Base de datos | MongoDB Atlas | Los gastos, usuarios, perfiles y configuraciones se almacenan de forma persistente; las consultas deben filtrar por propietario. |
| Autenticación | JWT y Google sign-in | El MVP puede operar con correo y contraseña; Google se integra como canal adicional sin cambiar el modelo de identidad. |
| Procesamiento del texto | Diccionario propio de palabras y reglas deterministas, sin API externa de IA | La interpretación debe ser reproducible, explicable y verificable; no se usan servicios externos de IA para este fin. |
| Etiqueta de interfaz | «Procesar con IA» | La etiqueta se conserva por decisión del proyecto, aunque la implementación sea determinista. |
| Entrada por voz | Solo Android, con Kotlin y `SpeechRecognizer` | La voz es un canal alternativo; iOS y plataformas no compatibles conservan la entrada por texto. |
| Imágenes de perfil | Cloudinary | La carga y sustitución de imágenes requiere autenticación, validación y manejo seguro de credenciales. |
| Notificaciones | Expo Notifications | Se deben distinguir notificaciones locales, generadas por la app o el dispositivo, de notificaciones push, enviadas desde un servidor. |
| Roles | Visitante, Usuario y Administrador | Las rutas, consultas y operaciones administrativas se autorizan en el backend según el rol y la propiedad del dato. |
| Privacidad | Aplicada en el backend | Ocultar información en la interfaz no es suficiente; cada consulta y operación debe validar sesión, rol y propietario. |

### 3.2 Reglas funcionales no negociables

1. El usuario revisa y corrige los datos interpretados antes de guardar.
2. Cada usuario accede y gestiona únicamente sus propios gastos.
3. El administrador solo consulta información agregada; no accede a gastos individuales ni a sus descripciones, montos o propietarios identificables.
4. Editar o eliminar un gasto actualiza el historial, los resúmenes, las estadísticas y los análisis afectados; no se aceptan resultados obsoletos.
5. Las fugas de dinero son **posibles** fugas detectadas por reglas deterministas; no son predicciones, diagnósticos ni juicios sobre los hábitos del usuario.
6. Las reglas de detección y sus parámetros deben estar aprobados, documentados y versionados. Este documento no define umbrales, montos mínimos, frecuencias ni ventanas.
7. La etiqueta «Procesar con IA» no autoriza el uso de una API externa de IA: el procesamiento acordado es determinista.

### 3.3 Notificaciones: locales frente a push

- **Notificación local:** la programa el dispositivo o la propia aplicación, por ejemplo con Expo Notifications. No requiere un servidor de envío, pero sí permiso del sistema cuando corresponda.
- **Notificación push:** la envía un servidor a un token de dispositivo. Requiere proyecto Expo/EAS, credenciales de notificación para Android e iOS, registro y almacenamiento seguro de tokens, consentimiento del usuario, manejo de tokens inválidos y una lógica de envío en el backend.
- Para el alcance actual de HU-25 se consideran alertas dentro de la aplicación y, como máximo, notificaciones locales. Las notificaciones push quedan postergadas y no se presentan como parte del MVP.

### 3.4 Voz, Expo y módulo nativo

`SpeechRecognizer` es una API nativa de Android. Un módulo Kotlin personalizado no funciona en Expo Go; requiere una compilación de desarrollo o un flujo de prebuild/EAS con el módulo nativo incluido. Esta es una dependencia de integración de HU-17 a HU-19 y un riesgo del plan, no un cambio de arquitectura.

---

## 4. Criterios usados para mejorar y priorizar las historias

### 4.1 Criterios de mejora

- **Propósito original conservado:** ninguna historia cambia de objetivo; se precisan alcance, reglas y verificabilidad.
- **Formato uniforme:** «Como [tipo de usuario], quiero [funcionalidad], para [beneficio]».
- **Criterios verificables:** cada criterio usa Dado / Cuando / Entonces y evita expresiones como «debe funcionar correctamente».
- **Detalle proporcional:** las historias de autenticación, privacidad, interpretación, fugas y administración reciben más detalle por su riesgo.
- **Sin invención de reglas:** los umbrales, montos mínimos, frecuencias, ventanas, categorías definitivas, moneda y políticas de retención se registran como decisiones pendientes.
- **Trazabilidad:** se conserva el identificador original y se documenta cualquier precisión, delimitación o postergación.
- **Cobertura de calidad:** cada historia incluye reglas, validaciones, errores, dependencias y pruebas sugeridas.
- **Seguridad desde el diseño:** la privacidad y la autorización se tratan como restricciones transversales, no como una pantalla añadida al final.

### 4.2 Criterios de priorización

- **Valor para el MVP:** se prioriza la cadena mínima que permite registrar, revisar, guardar, consultar y analizar un gasto, y demostrar una posible fuga.
- **Dependencias:** una historia no se adelanta si depende de identidad, persistencia o reglas que aún no existen.
- **Riesgo técnico:** integraciones externas, módulos nativos, correo, OAuth, Cloudinary y push se valoran por su costo de configuración y prueba.
- **Tiempo real:** 12 semanas para una persona, con integración, pruebas, seguridad, depuración y preparación de demostración. La asistencia de IA acelera la escritura, pero no elimina la verificación humana.
- **Demostración:** el flujo principal debe poder mostrarse de extremo a extremo; las funciones que solo amplían la experiencia no se consideran esenciales.
- **Privacidad y confianza:** la separación de datos y el control de acceso no son negociables, aunque su implementación sea transversal.

### 4.3 Definiciones MoSCoW

| Prioridad | Significado en este documento |
|---|---|
| **Must Have** | Esencial para que el MVP cumpla su propuesta de valor o una restricción de seguridad. Sin ello no se considera MVP. |
| **Should Have** | Importante para la experiencia o la administración, pero el MVP puede operar sin ello temporalmente. |
| **Could Have** | Útil y deseable si el cronograma lo permite; se sacrifica antes que un Must o un Should. |
| **Won't Have (for now)** | Postergado explícitamente para una versión futura. No se elimina del backlog; simplemente no se implementa en este release. |

### 4.4 Convenciones

- Los roles se escriben **Visitante**, **Usuario** y **Administrador**.
- «Gasto» designa un registro confirmado y persistido; «borrador» o «vista previa» designa una interpretación aún no guardada.
- Los importes se muestran con el formato y la moneda que se definan en D-03; no se fija aquí una moneda definitiva.
- Las fechas y los periodos dependen de la zona horaria y la configuración que se definan en D-04.
- Las referencias D-xx corresponden a decisiones pendientes de la sección 12.
- Las referencias R-xx corresponden a riesgos de la sección 12.

---

## 5. Resumen de las 33 historias y prioridades

**Módulos:** M1 = Acceso, autenticación y cuentas; M2 = Perfil del usuario; M3 = Registro y gestión de gastos; M4 = Registro por voz; M5 = Dashboard y estadísticas; M6 = Detección de fugas de dinero; M7 = Alertas, recomendaciones y metas; M8 = Administración y privacidad.

| ID | Título mejorado | Módulo | MoSCoW | ¿MVP? |
|---|---|---|---|---|
| HU-01 | Consultar información pública de FUGA+ y acceder a registro o inicio de sesión | M1 | **Must Have** | Sí |
| HU-02 | Registrarse e iniciar sesión con correo y contraseña | M1 | **Must Have** | Sí |
| HU-03 | Iniciar sesión con una cuenta de Google | M1 | **Should Have** | No |
| HU-04 | Cerrar sesión de forma segura | M1 | **Must Have** | Sí |
| HU-05 | Recuperar el acceso mediante restablecimiento de contraseña | M1 | **Should Have** | No |
| HU-06 | Desactivar la propia cuenta de usuario | M1 | **Could Have** | No |
| HU-07 | Consultar y editar nombres y teléfono del perfil | M2 | **Should Have** | No |
| HU-08 | Cambiar la foto de perfil | M2 | **Should Have** | No |
| HU-09 | Usar la foto de perfil de Google cuando esté disponible | M2 | **Could Have** | No |
| HU-10 | Registrar un gasto escrito en lenguaje natural | M3 | **Must Have** | Sí |
| HU-11 | Procesar el gasto con «Procesar con IA» y reglas deterministas | M3 | **Must Have** | Sí |
| HU-12 | Revisar y corregir los campos interpretados antes de guardar | M3 | **Must Have** | Sí |
| HU-13 | Guardar el gasto bajo la cuenta del propietario y aislarlo de otros usuarios | M3 | **Must Have** | Sí |
| HU-14 | Consultar el historial de gastos del más reciente al más antiguo | M3 | **Must Have** | Sí |
| HU-15 | Filtrar el historial por fecha y categoría | M3 | **Should Have** | No |
| HU-16 | Editar y eliminar gastos guardados, actualizando análisis y resúmenes | M3 | **Should Have** | No |
| HU-17 | Iniciar la grabación de voz para un gasto en Android | M4 | **Could Have** | No |
| HU-18 | Convertir la voz en texto con Kotlin y `SpeechRecognizer` | M4 | **Could Have** | No |
| HU-19 | Revisar la transcripción y los campos antes de guardar un gasto por voz | M4 | **Could Have** | No |
| HU-20 | Consultar total, cantidad y promedio de gasto por periodo | M5 | **Must Have** | Sí |
| HU-21 | Consultar el gasto por categoría e identificar la categoría de mayor gasto | M5 | **Must Have** | Sí |
| HU-22 | Comparar el gasto entre periodos | M5 | **Could Have** | No |
| HU-23 | Detectar posibles fugas de dinero con reglas deterministas | M6 | **Must Have** | Sí |
| HU-24 | Consultar la evidencia de una posible fuga de dinero | M6 | **Must Have** | Sí |
| HU-25 | Recibir alertas sobre posibles fugas de dinero | M7 | **Could Have** | No |
| HU-26 | Consultar sugerencias prácticas sobre posibles fugas | M7 | **Could Have** | No |
| HU-27 | Consultar el resumen mensual de posibles fugas | M7 | **Could Have** | No |
| HU-28 | Definir una meta mensual de gasto o ahorro con alcance explícito | M7 | **Won't Have (for now)** | No |
| HU-29 | Consultar el avance hacia la meta definida | M7 | **Won't Have (for now)** | No |
| HU-30 | Consultar estadísticas agregadas de uso sin acceder a gastos individuales | M8 | **Should Have** | No |
| HU-31 | Consultar usuarios registrados y la información administrativa necesaria | M8 | **Should Have** | No |
| HU-32 | Activar o desactivar cuentas de usuario desde funciones administrativas autorizadas | M8 | **Should Have** | No |
| HU-33 | Proteger la privacidad de los gastos y garantizar el aislamiento entre usuarios | M8 | **Must Have** | Sí |

### 5.1 Distribución de prioridades

| Prioridad | Cantidad | Historias |
|---|---:|---|
| **Must Have** | 13 | HU-01, HU-02, HU-04, HU-10, HU-11, HU-12, HU-13, HU-14, HU-20, HU-21, HU-23, HU-24, HU-33 |
| **Should Have** | 9 | HU-03, HU-05, HU-07, HU-08, HU-15, HU-16, HU-30, HU-31, HU-32 |
| **Could Have** | 9 | HU-06, HU-09, HU-17, HU-18, HU-19, HU-22, HU-25, HU-26, HU-27 |
| **Won't Have (for now)** | 2 | HU-28, HU-29 |
| **Total** | **33** | |

> **Lectura del MVP:** los 13 Must combinan 12 historias de funcionalidad visible y HU-33, que es una restricción transversal de seguridad y privacidad. HU-33 no representa una pantalla adicional: se implementa y verifica desde la primera historia que maneja datos.

---

## 6. Historias de usuario completas

Las historias se agrupan por módulo y conservan los identificadores originales. Cada una incluye prioridad, justificación, criterios verificables, reglas, dependencias, pruebas y decisiones pendientes. Los criterios se identifican como CA-XX.Y para facilitar su uso en pruebas y seguimiento.

### 6.1 Módulo 1 — Acceso, autenticación y cuentas

#### HU-01 — Consultar información pública de FUGA+ y acceder a registro o inicio de sesión

**Módulo:** 1 · Acceso, autenticación y cuentas  
**Prioridad:** **Must Have.** Es la entrada al producto y el primer paso de la demostración. Sin una pantalla pública no hay forma de explicar la propuesta de valor ni dirigir al Visitante al registro o al inicio de sesión.  
**MVP:** Sí.

> **Historia:** Como Visitante, quiero conocer qué es FUGA+, cómo funciona y qué funcionalidades ofrece, para decidir si creo una cuenta y empiezo a usarla.

**Objetivo y valor:** presentar de forma clara la propuesta de FUGA+ —registrar gastos en lenguaje natural y detectar posibles fugas de dinero— sin exponer información privada. Debe ofrecer accesos visibles a registro e inicio de sesión y dejar claro que las funciones financieras requieren autenticación.

**Criterios de aceptación**

- **CA-01.1** — **Dado** que una persona abre la aplicación sin sesión iniciada, **cuando** termina la carga inicial, **entonces** ve una pantalla pública con el nombre FUGA+, una descripción breve, la explicación del flujo de registro de gastos, la propuesta de posibles fugas y botones visibles de «Registrarse» e «Iniciar sesión».
- **CA-01.2** — **Dado** que el Visitante está en la pantalla pública, **cuando** pulsa «Registrarse» o «Iniciar sesión», **entonces** llega al flujo correspondiente y puede volver a la pantalla pública sin quedar autenticado.
- **CA-01.3** — **Dado** que el Visitante intenta abrir por enlace directo una ruta privada, como historial, dashboard o gastos, **cuando** la aplicación procesa la ruta, **entonces** lo redirige a la pantalla pública o al inicio de sesión y no muestra datos financieros; además, la API responde sin autorización si se intenta acceder directamente al recurso.
- **CA-01.4** — **Dado** que la pantalla pública se muestra, **cuando** el Visitante la recorre, **entonces** no aparecen gastos, montos, categorías, descripciones, correos ni datos de usuarios reales.

**Reglas de negocio, validaciones y errores**

- La pantalla es accesible sin sesión y no requiere llamadas a datos privados.
- El contenido público debe ser un texto aprobado por el proyecto; no se generan dinámicamente datos de usuarios.
- Los enlaces de registro e inicio de sesión deben estar disponibles también para accesibilidad (lector de pantalla y tamaño de toque adecuado).
- Si el contenido está embebido en la app, un fallo de red no debe mostrar datos privados; si se carga desde el backend, debe existir un estado de error con reintento.
- Un Visitante nunca recibe un token por el simple hecho de abrir la pantalla.
- Errores esperados: contenido no disponible (mensaje y reintento), ruta privada (redirección y respuesta 401 en API).

**Dependencias**

- Ninguna historia previa. Depende del texto y la identidad visual aprobados.
- Habilita el acceso a HU-02 y HU-04; los enlaces de la pantalla son la entrada funcional a HU-02.

**Pruebas sugeridas**

- Prueba de interfaz sin sesión: textos, botones y navegación.
- Prueba de navegación: registro, inicio de sesión y regreso.
- Prueba de seguridad: enlace directo a cada ruta privada sin token; verificar redirección y ausencia de datos.
- Prueba de accesibilidad y revisión del texto público.

**Ambigüedades y decisiones pendientes**

- Contenido exacto, tono y elementos legales o de privacidad que debe mostrar la pantalla (D-15).
- ¿La pantalla pública debe estar disponible sin conexión? Es una decisión de producto.
- ¿Debe incluir enlaces a política de privacidad y términos de uso? Se recomienda, pero no está acordado.

**Trazabilidad:** se conserva el propósito original «ver información pública de FUGA+»; se precisa el contenido mínimo, la navegación y la protección de rutas privadas. Sin cambio funcional.

#### HU-02 — Registrarse e iniciar sesión con correo y contraseña

**Módulo:** 1 · Acceso, autenticación y cuentas  
**Prioridad:** **Must Have.** Crea la identidad que permite asociar gastos a un propietario, aplicar permisos y cumplir la privacidad. Es la base de todo el flujo y de la demostración.  
**MVP:** Sí.

> **Historia:** Como Visitante, quiero registrarme e iniciar sesión con correo y contraseña, para acceder a mis gastos y a las funcionalidades privadas de FUGA+.

**Objetivo y valor:** permitir la creación de una cuenta de rol Usuario y el acceso posterior con credenciales válidas, sin que el registro público pueda crear administradores. La sesión debe ser segura y verificable en el backend.

**Criterios de aceptación**

- **CA-02.1** — **Dado** que el Visitante proporciona un correo válido, una contraseña que cumple la política vigente y la confirmación correcta, **cuando** envía el registro, **entonces** se crea una cuenta con rol **Usuario**, la contraseña se almacena como hash con sal y la persona puede iniciar sesión o queda autenticada según el flujo aprobado.
- **CA-02.2** — **Dado** que ya existe una cuenta con el correo indicado, **cuando** se intenta registrar de nuevo, **entonces** el sistema rechaza la operación con un mensaje claro y no crea una segunda cuenta ni modifica la existente.
- **CA-02.3** — **Dado** que el Visitante envía un correo con formato inválido, una contraseña que no cumple la política o una confirmación distinta, **cuando** intenta registrarse, **entonces** ve errores asociados a los campos y no se crea la cuenta.
- **CA-02.4** — **Dado** que una cuenta activa introduce credenciales correctas, **cuando** inicia sesión, **entonces** recibe una sesión válida y accede a sus funcionalidades privadas; **dado** que introduce credenciales incorrectas, **cuando** intenta entrar, **entonces** recibe un mensaje genérico que no revela si el correo o la contraseña fueron los incorrectos.
- **CA-02.5** — **Dado** que una cuenta fue desactivada por un administrador, **cuando** intenta iniciar sesión, **entonces** el sistema rechaza el acceso aunque las credenciales sean correctas, con un mensaje que no expone datos de la cuenta.
- **CA-02.6** — **Dado** que se completa un registro público, **cuando** se consulta el rol asignado en el backend, **entonces** el rol es **Usuario** y nunca **Administrador**; un intento de enviar un rol desde el cliente no modifica el rol asignado.

**Reglas de negocio, validaciones y errores**

- El correo se normaliza (por ejemplo, espacios exteriores y mayúsculas) y debe ser único; la unicidad se garantiza en el backend y en la base de datos.
- La política de contraseñas, la longitud máxima, la verificación de correo y la duración de la sesión están pendientes (D-09).
- El hash de contraseña debe usar un algoritmo adaptativo con sal; nunca se almacena ni se registra la contraseña en claro.
- El rol se asigna en el servidor; cualquier campo de rol enviado por el cliente se ignora.
- Los errores de credenciales no deben permitir enumerar cuentas. El registro puede indicar que el correo ya existe, según la decisión de producto.
- Los intentos fallidos pueden limitarse por tasa; el umbral y la política están pendientes (D-09).
- Respuestas esperadas: 201 al crear, 400 por validación, 409 por conflicto de correo, 401 por credenciales inválidas o cuenta desactivada, 429 si se aplica limitación de intentos, 5xx por fallo interno sin filtrar detalles.

**Dependencias**

- HU-01 como punto de entrada.
- Restricciones transversales de privacidad y autorización de HU-33, que se implementan desde esta historia aunque su verificación completa sea posterior.
- Habilita HU-03, HU-04, HU-05, HU-06, HU-07, HU-10, HU-30, HU-31 y HU-32.

**Pruebas sugeridas**

- Pruebas unitarias de normalización de correo y validación de contraseña.
- Pruebas de integración de registro, duplicado, inicio de sesión válido e inválido, cuenta desactivada y escalamiento de rol.
- Verificar que la contraseña almacenada es un hash con sal y que no aparece en logs ni respuestas.
- Prueba de extremo a extremo: registro, cierre de sesión y nuevo inicio de sesión.

**Ambigüedades y decisiones pendientes**

- Política de contraseñas, verificación de correo, recuperación, bloqueo por intentos y duración o renovación del JWT (D-09).
- ¿La cuenta queda autenticada automáticamente al registrarse o debe iniciar sesión? Se debe definir en el diseño de experiencia.
- ¿Se permite cambiar el correo desde el perfil? No está incluido en las 33 historias; queda fuera del alcance actual.

**Trazabilidad:** se conserva el propósito original «registrarse e iniciar sesión»; se precisan roles, validaciones, seguridad y errores. Sin cambio funcional.

#### HU-03 — Iniciar sesión con una cuenta de Google

**Módulo:** 1 · Acceso, autenticación y cuentas  
**Prioridad:** **Should Have.** Es un canal de autenticación acordado y reduce fricción, pero el MVP puede operar con correo y contraseña. La configuración OAuth, la verificación de tokens y las pruebas en dispositivos requieren tiempo adicional.  
**MVP:** No.

> **Historia:** Como Usuario, quiero iniciar sesión con mi cuenta de Google, para acceder sin recordar otra contraseña y aprovechar mi identidad existente.

**Objetivo y valor:** ofrecer un inicio de sesión alternativo y seguro mediante Google, creando o vinculando una cuenta de FUGA+ sin permitir tomas de control de cuentas existentes ni asignar roles privilegiados.

**Criterios de aceptación**

- **CA-03.1** — **Dado** que el Usuario elige «Continuar con Google» y completa el flujo con una cuenta de Google válida, **cuando** el backend verifica el token de identidad (firma, emisor, audiencia, vigencia y correo verificado), **entonces** inicia sesión en su cuenta de FUGA+ o, si no existe, se crea una cuenta con rol **Usuario** y se emite una sesión válida.
- **CA-03.2** — **Dado** que el Usuario cancela o rechaza el flujo de Google, **cuando** vuelve a la aplicación, **entonces** no se crea ninguna cuenta ni sesión y se mantiene en la pantalla de acceso con la opción de correo y contraseña.
- **CA-03.3** — **Dado** que el token de Google es inválido, está vencido, tiene una audiencia incorrecta o el correo no está verificado, **cuando** el backend lo procesa, **entonces** rechaza la autenticación sin crear cuenta y devuelve un mensaje genérico.
- **CA-03.4** — **Dado** que la cuenta de FUGA+ vinculada a Google está desactivada, **cuando** el Usuario intenta entrar con Google, **entonces** se rechaza el acceso igual que en el inicio de sesión con contraseña.
- **CA-03.5** — **Dado** que el correo de Google coincide con una cuenta local existente, **cuando** se intenta vincular, **entonces** el sistema no inicia sesión ni fusiona datos sin cumplir la regla de vinculación aprobada (D-10); no se permite una toma de control por conocer un correo.

**Reglas de negocio, validaciones y errores**

- Solo se aceptan tokens emitidos para los identificadores de cliente configurados para Android, iOS o web del proyecto.
- La verificación se realiza en el backend; el cliente no decide la identidad ni el rol.
- Se solicitan únicamente los permisos mínimos necesarios (identidad, correo y perfil básico).
- No se almacenan secretos de OAuth en la aplicación móvil.
- El correo debe estar verificado por Google para crear o vincular una cuenta.
- Se debe definir si una cuenta creada con Google puede establecer una contraseña local posteriormente (D-10).
- Respuestas esperadas: 200/201 con sesión, 401 por token inválido o cuenta desactivada, 409 si la vinculación requiere una acción adicional, 5xx sin detalles sensibles.

**Dependencias**

- HU-02 (modelo de usuarios, sesión y roles).
- Configuración de OAuth en Google Cloud y de las aplicaciones móviles.
- HU-33 para autorización y privacidad.
- Habilita HU-09.

**Pruebas sugeridas**

- Pruebas de backend con tokens de prueba: válido, vencido, audiencia incorrecta, firma inválida y correo no verificado.
- Pruebas de integración con cuentas de prueba de Google: primer acceso, acceso posterior, cancelación y cuenta desactivada.
- Pruebas de vinculación con correo existente y de intento de toma de control.
- Prueba manual en un dispositivo Android y en iOS si el alcance lo permite.

**Ambigüedades y decisiones pendientes**

- Regla de vinculación entre una cuenta local y una cuenta de Google con el mismo correo (D-10).
- ¿La autenticación con Google crea la cuenta automáticamente o exige aceptar términos y condiciones?
- ¿Se admite iniciar sesión con Google en iOS en el MVP? La historia no limita plataforma, pero la prioridad es Should.
- ¿Qué ocurre si el Usuario elimina o cambia su cuenta de Google?

**Trazabilidad:** se conserva el propósito original «iniciar sesión con una cuenta de Google»; se precisan verificación, vinculación, roles y errores. Sin cambio funcional.

#### HU-04 — Cerrar sesión de forma segura

**Módulo:** 1 · Acceso, autenticación y cuentas  
**Prioridad:** **Must Have.** Es una medida básica de seguridad en dispositivos compartidos y completa el ciclo de autenticación. Su costo es bajo y evita que una sesión quede disponible para otra persona.  
**MVP:** Sí.

> **Historia:** Como Usuario autenticado, quiero cerrar sesión de forma segura, para impedir que otras personas accedan a mi cuenta desde el mismo dispositivo.

**Objetivo y valor:** finalizar la sesión actual, eliminar las credenciales almacenadas en el dispositivo y evitar que la navegación hacia atrás o un enlace profundo vuelvan a mostrar información privada.

**Criterios de aceptación**

- **CA-04.1** — **Dado** que el Usuario está autenticado y pulsa «Cerrar sesión», **cuando** la operación se completa, **entonces** la aplicación elimina el token y cualquier credencial de sesión del almacenamiento seguro, limpia el estado privado en memoria y navega a la pantalla pública o de inicio de sesión.
- **CA-04.2** — **Dado** que el Usuario cerró sesión, **cuando** usa el botón Atrás o un enlace directo a una pantalla privada, **entonces** no puede ver datos privados y se le solicita autenticarse de nuevo.
- **CA-04.3** — **Dado** que el Usuario cierra sesión, **cuando** el backend recibe la solicitud de cierre, **entonces** invalida la sesión o el token de renovación según la política vigente (D-09); un token de acceso vencido o revocado no permite nuevas operaciones protegidas.
- **CA-04.4** — **Dado** que el cierre de sesión ocurre sin conexión, **cuando** el Usuario lo confirma, **entonces** la aplicación elimina igualmente las credenciales locales y no vuelve a mostrar datos privados; la revocación del lado servidor se completará según la política de sesión definida.

**Reglas de negocio, validaciones y errores**

- Los tokens se guardan en almacenamiento seguro del dispositivo, no en almacenamiento plano ni en registros.
- El cierre de sesión debe limpiar cachés, estados de navegación y datos temporales que puedan contener gastos.
- La sesión actual se cierra; si se requiere «cerrar todas las sesiones», es una decisión futura (D-09).
- Un fallo de red no debe impedir el cierre local; se informa si la revocación remota quedó pendiente.
- No se muestran mensajes que revelen tokens, identificadores internos o datos de la cuenta.

**Dependencias**

- HU-02 (sesión con correo y contraseña).
- HU-03 si la sesión proviene de Google.
- HU-33 para el tratamiento seguro de credenciales.

**Pruebas sugeridas**

- Prueba de interfaz: cierre de sesión y navegación posterior.
- Prueba de almacenamiento: verificar que no quedan tokens ni datos privados tras el cierre.
- Prueba de integración: token revocado rechazado en endpoints protegidos.
- Prueba con red interrumpida: cierre local y mensaje correspondiente.

**Ambigüedades y decisiones pendientes**

- ¿Debe existir «cerrar sesión en todos los dispositivos»? (D-09).
- Duración del token de acceso, renovación y revocación inmediata (D-09).
- Comportamiento exacto sin conexión y estrategia de reintento de revocación.

**Trazabilidad:** se conserva el propósito original «cerrar sesión de forma segura»; se precisan limpieza local, revocación y navegación. Sin cambio funcional.

#### HU-05 — Recuperar el acceso mediante restablecimiento de contraseña

**Módulo:** 1 · Acceso, autenticación y cuentas  
**Prioridad:** **Should Have.** Es importante para no perder el acceso, pero no es necesaria para demostrar la propuesta de valor. Requiere un proveedor de correo, tokens de un solo uso y pruebas de seguridad; puede incorporarse después del núcleo del MVP.  
**MVP:** No.

> **Historia:** Como Usuario, quiero recuperar mi acceso mediante el restablecimiento de contraseña, para volver a entrar si olvido mis credenciales.

**Objetivo y valor:** permitir que un Usuario recupere el acceso de forma segura sin revelar si un correo está registrado y sin debilitar la autenticación.

**Criterios de aceptación**

- **CA-05.1** — **Dado** que una persona solicita recuperación para un correo registrado o no registrado, **cuando** envía la solicitud, **entonces** recibe la misma respuesta genérica en ambos casos y el sistema no revela la existencia de la cuenta.
- **CA-05.2** — **Dado** que el correo está registrado y el envío se realiza correctamente, **cuando** el Usuario abre el enlace o ingresa el código recibido, **entonces** accede a una pantalla para definir una nueva contraseña que cumple la política vigente.
- **CA-05.3** — **Dado** que el token de recuperación es válido, no ha vencido y no ha sido usado, **cuando** el Usuario define la nueva contraseña y la confirma, **entonces** el sistema actualiza la contraseña, invalida el token y cierra las sesiones existentes según la política aprobada.
- **CA-05.4** — **Dado** que el token es inválido, vencido o ya fue utilizado, **cuando** el Usuario intenta restablecer la contraseña, **entonces** ve un error y puede solicitar uno nuevo; no se modifica la contraseña.
- **CA-05.5** — **Dado** que la nueva contraseña no cumple la política o la confirmación no coincide, **cuando** se intenta guardar, **entonces** no se actualiza y se muestran errores de validación.

**Reglas de negocio, validaciones y errores**

- El token de recuperación debe ser aleatorio, de un solo uso, con vencimiento y almacenado de forma que no pueda reutilizarse si se filtra la base de datos.
- La respuesta de solicitud debe ser genérica y, en lo posible, con tiempos similares para correos existentes y no existentes.
- Se debe aplicar limitación de solicitudes por cuenta y por IP; los umbrales están pendientes (D-09).
- Las contraseñas se almacenan con hash adaptativo y sal; nunca se envían por correo ni se registran en logs.
- Al restablecer, se invalidan las sesiones o tokens de renovación existentes según D-09.
- Respuestas esperadas: 202/200 genérico al solicitar, 400 por validación, 401/410 por token inválido o vencido, 429 por exceso de solicitudes.

**Dependencias**

- HU-02 (cuenta y contraseña).
- Proveedor de correo transaccional y plantillas de mensaje.
- HU-33 para privacidad y manejo seguro de tokens.

**Pruebas sugeridas**

- Pruebas de token: válido, vencido, reutilizado y manipulado.
- Prueba de enumeración: misma respuesta para correo existente y no existente.
- Prueba de política de contraseñas y de invalidación de sesiones.
- Prueba de integración con un buzón de pruebas y de limitación de solicitudes.

**Ambigüedades y decisiones pendientes**

- Proveedor de correo, remitente, plantilla, tiempo de vencimiento y política de contraseñas (D-09).
- ¿Qué ocurre con cuentas creadas solo con Google, que no tienen contraseña local? (D-10).
- ¿Se permite recuperar la cuenta mediante preguntas de seguridad o solo por correo?
- ¿Debe mostrarse un mensaje específico si el correo no existe? Por seguridad, se recomienda no hacerlo.

**Trazabilidad:** se conserva el propósito original «recuperar el acceso mediante recuperación de contraseña»; se precisan token, prevención de enumeración de cuentas, validaciones e invalidación de sesiones. Sin cambio funcional.

#### HU-06 — Desactivar la propia cuenta de usuario

**Módulo:** 1 · Acceso, autenticación y cuentas  
**Prioridad:** **Could Have.** Es una función de autonomía y privacidad valiosa, pero no es necesaria para el MVP. La diferencia entre desactivar y eliminar, la retención de datos y la reactivación requieren decisiones que aún no están tomadas.  
**MVP:** No.

> **Historia:** Como Usuario, quiero desactivar mi cuenta, para dejar de usar el servicio y controlar qué ocurre con mi acceso y mis datos.

**Objetivo y valor:** ofrecer una salida controlada de la cuenta sin confundirla con una suspensión administrativa. La historia debe dejar explícito qué se conserva, qué se elimina y cómo se puede recuperar el acceso, si se permite.

**Criterios de aceptación**

- **CA-06.1** — **Dado** que el Usuario autenticado solicita desactivar su cuenta, **cuando** abre la opción, **entonces** ve una explicación de las consecuencias —pérdida de acceso, conservación o eliminación de datos y posibilidad de reactivación— antes de confirmar.
- **CA-06.2** — **Dado** que el Usuario confirma la desactivación y se reautentica según la política de seguridad, **cuando** la operación finaliza, **entonces** su cuenta queda en estado desactivado por el propio usuario, sus sesiones se invalidan y no puede iniciar sesión mientras permanezca en ese estado.
- **CA-06.3** — **Dado** que el Usuario cancela la confirmación, **cuando** vuelve a la aplicación, **entonces** su cuenta y sus gastos permanecen sin cambios.
- **CA-06.4** — **Dado** que un Usuario intenta desactivar la cuenta de otra persona, **cuando** envía la solicitud, **entonces** el backend la rechaza; la desactivación administrativa es una operación distinta, cubierta por HU-32.
- **CA-06.5** — **Dado** que la cuenta está desactivada por el Usuario, **cuando** se consulta su información, **entonces** los gastos se conservan o eliminan según la política de retención aprobada (D-06), y la interfaz no muestra datos de la cuenta a terceros.

**Reglas de negocio, validaciones y errores**

- La desactivación por el Usuario se distingue de la desactivación administrativa en el estado y en la razón registrada.
- Se requiere confirmación explícita y, preferiblemente, reautenticación antes de aplicar el cambio.
- No se eliminan gastos de forma automática mientras la política de retención no esté aprobada.
- Las sesiones activas se invalidan; los intentos de inicio de sesión posteriores se rechazan con un mensaje claro pero sin datos sensibles.
- La reactivación por el Usuario, por soporte o por un administrador debe definirse (D-06).
- Errores esperados: 401 sin sesión, 403 si intenta afectar otra cuenta, 409 si la cuenta ya está desactivada, 5xx sin detalles internos.

**Dependencias**

- HU-02 y HU-04 (cuenta y cierre de sesión).
- HU-33 (privacidad y autorización).
- Decisión D-06 sobre eliminación, retención y reactivación.

**Pruebas sugeridas**

- Prueba de flujo: solicitud, consecuencias, confirmación, cancelación y desactivación.
- Prueba de autorización: un Usuario no puede desactivar a otro.
- Prueba de inicio de sesión y de token existente después de la desactivación.
- Prueba de conservación o eliminación de datos según la política aprobada.

**Ambigüedades y decisiones pendientes**

- ¿Desactivar es sinónimo de eliminar la cuenta o solo de bloquear el acceso? (D-06).
- ¿Cuánto tiempo se conservan los gastos y qué se hace con ellos?
- ¿Puede el Usuario reactivar su cuenta por sí mismo? ¿Durante cuánto tiempo?
- ¿Se ofrece exportación de datos antes de desactivar? No está en las 33 historias.

**Trazabilidad:** se conserva el propósito original «desactivar la cuenta de usuario»; se delimita frente a la desactivación administrativa y se precisan consecuencias y autorización. Sin cambio funcional.

### 6.2 Módulo 2 — Perfil del usuario

#### HU-07 — Consultar y editar nombres y teléfono del perfil

**Módulo:** 2 · Perfil del usuario  
**Prioridad:** **Should Have.** Mejora la identificación y la comunicación con el Usuario, pero no es necesaria para registrar, consultar o analizar gastos. Es una historia de bajo costo que puede entrar después de los Must.  
**MVP:** No.

> **Historia:** Como Usuario, quiero consultar y editar mi nombre, apellido y teléfono, para mantener correctos los datos de mi perfil.

**Objetivo y valor:** permitir que el Usuario vea y actualice sus datos básicos sin afectar sus gastos, su correo de acceso ni la información de otros usuarios.

**Criterios de aceptación**

- **CA-07.1** — **Dado** que el Usuario autenticado abre su perfil, **cuando** la pantalla carga, **entonces** ve sus nombres, apellido y teléfono actuales, y el correo de la cuenta en modo solo lectura.
- **CA-07.2** — **Dado** que el Usuario modifica uno o más campos con valores válidos, **cuando** guarda, **entonces** los cambios se persisten en su cuenta, se confirman en pantalla y no alteran sus gastos ni su rol.
- **CA-07.3** — **Dado** que el Usuario deja vacío un campo obligatorio, introduce un teléfono con formato inválido o supera la longitud permitida, **cuando** intenta guardar, **entonces** ve el error asociado al campo y no se persiste ningún cambio.
- **CA-07.4** — **Dado** que un Usuario intenta consultar o modificar el perfil de otra persona manipulando un identificador, **cuando** el backend procesa la solicitud, **entonces** responde con error de autorización o recurso no encontrado sin devolver datos.
- **CA-07.5** — **Dado** que un Usuario no autenticado intenta acceder al perfil, **cuando** realiza la petición, **entonces** recibe 401 y la aplicación lo redirige al inicio de sesión.

**Reglas de negocio, validaciones y errores**

- El identificador del Usuario se obtiene de la sesión; no se acepta un identificador de propietario enviado por el cliente.
- El correo de acceso no se edita en esta historia. Cambiarlo requiere verificación y no está incluido en las 33 historias.
- Los campos obligatorios, longitudes máximas, caracteres permitidos y formato telefónico están pendientes de definición (D-13).
- Se deben recortar espacios exteriores y rechazar contenido vacío cuando el campo sea obligatorio.
- El teléfono es dato personal: no se muestra a otros usuarios ni en respuestas administrativas que no lo requieran.
- Respuestas esperadas: 200 al consultar o actualizar, 400 por validación, 401 sin sesión, 403/404 por acceso a otro perfil, 5xx sin detalles internos.

**Dependencias**

- HU-02 (identidad y sesión).
- HU-33 (autorización y minimización de datos).
- Habilita HU-08 y HU-09.

**Pruebas sugeridas**

- Prueba de interfaz: visualización, edición, cancelación y validación.
- Prueba de integración: persistencia y recuperación de los cambios.
- Prueba de autorización: acceso con el identificador de otro Usuario.
- Prueba de campos límite y caracteres internacionales.

**Ambigüedades y decisiones pendientes**

- ¿Nombre y apellido son obligatorios? ¿El teléfono es obligatorio? (D-13).
- Formato y país del teléfono, longitud máxima y normalización.
- ¿Se permite cambiar el correo desde el perfil? No está en el alcance actual.
- ¿Se conserva un historial de cambios de perfil? No está definido.

**Trazabilidad:** se conserva el propósito original «ver y editar nombre, apellido y teléfono»; se precisan autorización, validaciones y alcance. Sin cambio funcional.

#### HU-08 — Cambiar la foto de perfil

**Módulo:** 2 · Perfil del usuario  
**Prioridad:** **Should Have.** Personaliza la cuenta y mejora la experiencia, pero el MVP puede usar un avatar genérico. La integración con Cloudinary añade configuración, validación de archivos y manejo de credenciales.  
**MVP:** No.

> **Historia:** Como Usuario, quiero cambiar mi foto de perfil, para personalizar mi cuenta y reconocerla fácilmente.

**Objetivo y valor:** permitir la selección y actualización de una imagen de perfil almacenada en Cloudinary, sin exponer credenciales y sin afectar la privacidad de los gastos.

**Criterios de aceptación**

- **CA-08.1** — **Dado** que el Usuario autenticado abre la edición de perfil, **cuando** selecciona o captura una imagen permitida, **entonces** ve una vista previa y puede confirmar o cancelar antes de reemplazar la foto actual.
- **CA-08.2** — **Dado** que el Usuario confirma una imagen válida, **cuando** la carga finaliza, **entonces** la nueva imagen queda asociada únicamente a su perfil y se muestra en la aplicación; la imagen anterior se conserva o elimina según la política de activos (D-13).
- **CA-08.3** — **Dado** que la imagen tiene un tipo no permitido, supera el tamaño máximo o está corrupta, **cuando** se intenta cargar, **entonces** el sistema rechaza la operación, muestra un mensaje claro y mantiene la foto anterior.
- **CA-08.4** — **Dado** que la carga falla por red o por el proveedor, **cuando** el Usuario recibe el error, **entonces** puede reintentar y la foto anterior sigue visible; no queda un perfil en estado inconsistente.
- **CA-08.5** — **Dado** que un Usuario intenta cambiar la foto de otra cuenta, **cuando** manipula la solicitud, **entonces** el backend rechaza la operación y no modifica ningún perfil.

**Reglas de negocio, validaciones y errores**

- La carga debe autenticarse y asociarse al Usuario de la sesión.
- Las credenciales de Cloudinary no se incluyen en la app; se usa una firma o un endpoint del backend según el diseño aprobado.
- Tipos de archivo, tamaño máximo, recorte, compresión y moderación están pendientes (D-13).
- Se recomienda eliminar metadatos EXIF y no conservar la imagen original sin necesidad.
- La imagen de perfil es un dato personal, pero no debe mezclarse con datos de gastos.
- Respuestas esperadas: 200 al actualizar, 400 por archivo inválido, 401 sin sesión, 403/404 por otra cuenta, 413 si excede el tamaño, 502/503 si Cloudinary no responde.

**Dependencias**

- HU-07 (perfil existente).
- Cuenta y credenciales de Cloudinary.
- HU-33 (autorización y manejo de secretos).
- Se relaciona con HU-09 por la precedencia entre foto cargada y foto de Google.

**Pruebas sugeridas**

- Prueba con archivo válido, tipo inválido, archivo demasiado grande y archivo corrupto.
- Prueba de fallo del proveedor y reintento.
- Prueba de autorización con el identificador de otro Usuario.
- Revisión de que las credenciales no aparecen en el cliente ni en logs.

**Ambigüedades y decisiones pendientes**

- Formatos permitidos, tamaño máximo, recorte y política de eliminación del activo anterior (D-13).
- ¿La imagen es pública por URL o requiere acceso firmado? Es una decisión de privacidad.
- ¿Se permite eliminar la foto y volver al avatar por defecto? Se recomienda, pero no está acordado.

**Trazabilidad:** se conserva el propósito original «cambiar la foto de perfil»; se precisan Cloudinary, validaciones, autorización y errores. Sin cambio funcional.

#### HU-09 — Usar la foto de perfil de Google cuando esté disponible

**Módulo:** 2 · Perfil del usuario  
**Prioridad:** **Could Have.** Es una comodidad que depende de HU-03 y no aporta valor al flujo principal. Puede implementarse después de Google y de la foto de perfil.  
**MVP:** No.

> **Historia:** Como Usuario que inicia sesión con Google, quiero que mi foto de perfil de Google se use cuando esté disponible, para evitar cargarla manualmente.

**Objetivo y valor:** aprovechar la imagen pública del perfil de Google como imagen inicial, con una alternativa clara cuando no exista o no pueda cargarse.

**Criterios de aceptación**

- **CA-09.1** — **Dado** que una cuenta se crea o inicia sesión con Google y el perfil de Google incluye una imagen disponible, **cuando** se completa la autenticación, **entonces** la aplicación muestra esa imagen como foto de perfil, siempre que el Usuario no tenga una foto personalizada según la regla de precedencia aprobada.
- **CA-09.2** — **Dado** que Google no devuelve imagen, la URL falla o la imagen no puede cargarse, **cuando** se muestra el perfil, **entonces** aparece un avatar alternativo (iniciales o marcador visual) sin romper la pantalla.
- **CA-09.3** — **Dado** que el Usuario tiene una foto personalizada cargada mediante HU-08, **cuando** inicia sesión con Google, **entonces** se respeta la precedencia definida en D-13 y no se reemplaza silenciosamente su elección.
- **CA-09.4** — **Dado** que el Usuario no autoriza el permiso de perfil o la imagen no está disponible, **cuando** usa la aplicación, **entonces** puede seguir operando y cargar una imagen manualmente.

**Reglas de negocio, validaciones y errores**

- Solo se usan los datos de perfil que Google devuelve con el consentimiento del Usuario.
- No se descarga ni se almacena la imagen sin una necesidad definida; se puede conservar la URL o una copia según D-13.
- La precedencia entre foto de Google y foto cargada debe ser explícita; la propuesta es que la foto cargada por el Usuario prevalezca, pero requiere confirmación.
- Un fallo de carga de imagen no debe impedir el inicio de sesión.
- Respuestas esperadas: la autenticación continúa aunque la imagen no esté disponible; los errores de imagen se manejan en la interfaz.

**Dependencias**

- HU-03 (inicio de sesión con Google).
- HU-07 y HU-08 (perfil e imagen personalizada).
- Decisión D-13 sobre precedencia y almacenamiento.

**Pruebas sugeridas**

- Prueba con perfil de Google con imagen, sin imagen y con URL inválida.
- Prueba de precedencia con una foto personalizada existente.
- Prueba de denegación de permisos y de funcionamiento sin imagen.
- Prueba de que el fallo de imagen no bloquea la sesión.

**Ambigüedades y decisiones pendientes**

- Precedencia entre imagen de Google e imagen cargada (D-13).
- ¿Se actualiza la imagen cada vez que inicia sesión o solo en la creación de la cuenta?
- ¿Se almacena una copia en Cloudinary o solo la URL de Google?
- ¿Qué ocurre si el Usuario revoca el acceso a su foto en Google?

**Trazabilidad:** se conserva el propósito original «usar la foto de perfil de Google cuando esté disponible»; se precisan reglas de alternativa, precedencia y consentimiento. Sin cambio funcional.

### 6.3 Módulo 3 — Registro y gestión de gastos

#### HU-10 — Registrar un gasto escrito en lenguaje natural

**Módulo:** 3 · Registro y gestión de gastos  
**Prioridad:** **Must Have.** Es la entrada principal del producto y el inicio de la cadena de valor. Sin esta historia no existen gastos que interpretar, guardar, consultar o analizar.  
**MVP:** Sí.

> **Historia:** Como Usuario, quiero escribir un gasto en lenguaje natural, para registrarlo rápido sin completar un formulario extenso.

**Objetivo y valor:** reducir la fricción del registro permitiendo una frase cotidiana en español. El texto debe conservarse como borrador y enviarse a la interpretación, sin guardar todavía el gasto.

**Criterios de aceptación**

- **CA-10.1** — **Dado** que el Usuario autenticado abre la opción de registrar gasto, **cuando** la pantalla carga, **entonces** ve un campo de texto, un ejemplo de frase y una acción para enviar el texto a procesamiento.
- **CA-10.2** — **Dado** que el Usuario escribe «Hoy gasté $8.000 en un taxi» y envía el texto, **cuando** la aplicación responde, **entonces** se muestra una vista previa en estado borrador con el texto original y los campos interpretados, y el gasto no aparece todavía en el historial ni en las estadísticas.
- **CA-10.3** — **Dado** que el campo está vacío o contiene solo espacios, **cuando** el Usuario intenta enviarlo, **entonces** ve un mensaje de validación y no se ejecuta el procesamiento.
- **CA-10.4** — **Dado** que se produce un error de red o del servidor, **cuando** falla el envío, **entonces** el texto escrito se conserva, se muestra un mensaje comprensible y el Usuario puede reintentar sin duplicar el borrador.
- **CA-10.5** — **Dado** que el Usuario no tiene sesión, **cuando** intenta acceder al registro de gastos, **entonces** la aplicación lo redirige al inicio de sesión y la API rechaza la operación con 401.
- **CA-10.6** — **Dado** que el Usuario descarta el borrador, **cuando** confirma el descarte, **entonces** el texto y la interpretación se eliminan del estado de trabajo y no se crea ningún gasto.

**Reglas de negocio, validaciones y errores**

- El texto se acepta en español y con formato libre, incluidos signos de moneda y separadores numéricos; los formatos exactos que reconoce el diccionario están pendientes (D-05).
- La longitud máxima del texto, el tratamiento de emojis y el número de gastos por frase están pendientes (D-05). El alcance inicial es un gasto por envío.
- No se ejecuta ni se interpreta el texto como código; se trata como contenido no confiable y se escapa en la interfaz.
- El texto no se envía a una API externa de IA. Solo se usa para el procesamiento determinista acordado.
- El borrador no se guarda como gasto hasta que el Usuario confirme en HU-12 y el backend persista en HU-13.
- Respuestas esperadas: 200/201 al crear el borrador de interpretación, 400 por texto vacío o inválido, 401 sin sesión, 422 si no se puede interpretar, 429 si se limita el uso, 5xx sin detalles sensibles.

**Dependencias**

- HU-02 (Usuario autenticado).
- HU-11 (procesamiento del texto).
- HU-33 (autorización y privacidad).

**Pruebas sugeridas**

- Prueba de interfaz: estado inicial, texto válido, texto vacío, error y reintento.
- Prueba de integración: el texto llega al procesador y no se persiste como gasto antes de confirmar.
- Prueba de seguridad: caracteres especiales, HTML, texto muy largo y solicitudes sin token.
- Prueba de extremo a extremo: escribir, enviar, revisar y descartar.

**Ambigüedades y decisiones pendientes**

- Límite de caracteres, idiomas aceptados y tratamiento de mayúsculas, tildes y abreviaturas (D-05).
- ¿Se permiten varios gastos en una sola frase? El alcance inicial asume uno; requiere decisión.
- ¿El borrador sobrevive al cierre de la aplicación o a la pérdida de sesión? No está definido.
- ¿La fecha debe ser obligatoria en el texto o puede proponerse la fecha actual? (D-04).

**Trazabilidad:** se conserva el propósito original «ingresar un gasto en lenguaje natural»; se precisan borrador, validaciones, privacidad y errores. Sin cambio funcional.

#### HU-11 — Procesar el gasto con «Procesar con IA» y reglas deterministas

**Módulo:** 3 · Registro y gestión de gastos  
**Prioridad:** **Must Have.** Convierte el texto libre en datos utilizables y es el núcleo de la propuesta de valor. Debe implementarse sin API externa de IA y con resultados reproducibles.  
**MVP:** Sí.

> **Historia:** Como Usuario, quiero procesar el texto con el botón «Procesar con IA» y reglas deterministas, para obtener el monto, la categoría, la descripción y la fecha del gasto sin depender de un servicio externo de IA.

**Objetivo y valor:** interpretar la frase del Usuario mediante un diccionario propio y reglas explícitas, mostrando un borrador editable. El resultado debe ser explicable y repetible para el mismo texto y la misma versión del diccionario.

**Criterios de aceptación**

- **CA-11.1** — **Dado** que el Usuario escribió un texto válido, **cuando** pulsa el botón cuya etiqueta visible es exactamente «Procesar con IA», **entonces** el backend ejecuta el diccionario y las reglas deterministas y devuelve un borrador con monto, categoría, descripción, fecha —cuando se reconozca— y el texto original.
- **CA-11.2** — **Dado** el texto «Hoy gasté $8.000 en un taxi», **cuando** se procesa con la versión aprobada del diccionario, **entonces** el borrador muestra monto 8.000, categoría del catálogo correspondiente a transporte, descripción «Taxi» y la fecha reconocida como hoy, sin guardar el gasto todavía.
- **CA-11.3** — **Dado** que el texto no contiene un monto reconocible, **cuando** se procesa, **entonces** el sistema informa que no pudo interpretar el monto, deja el campo disponible para corrección manual y no permite guardar hasta que el monto sea válido.
- **CA-11.4** — **Dado** que el texto contiene una categoría desconocida o ambigua, **cuando** se procesa, **entonces** el sistema aplica la regla de categoría aprobada (incluido el tratamiento de «Otros», si existe) o deja el campo para que el Usuario lo seleccione; la decisión exacta está pendiente en D-02.
- **CA-11.5** — **Dado** que el procesamiento está en curso, **cuando** el Usuario pulsa repetidamente el botón, **entonces** el botón se deshabilita o las solicitudes se agrupan para no generar borradores duplicados.
- **CA-11.6** — **Dado** el mismo texto y la misma versión de diccionario y reglas, **cuando** se procesa más de una vez, **entonces** el resultado es equivalente y no contiene llamadas a una API externa de IA.
- **CA-11.7** — **Dado** que el procesamiento supera el tiempo de espera o falla, **cuando** la aplicación recibe el error, **entonces** conserva el texto, muestra un mensaje con reintento y no crea un gasto parcial.

**Reglas de negocio, validaciones y errores**

- El procesamiento se ejecuta con un diccionario y un conjunto de reglas versionados. Cada resultado debe registrar la versión usada para poder reproducir o auditar la interpretación.
- La categoría resultante debe pertenecer al catálogo cerrado aprobado; la lista definitiva está pendiente (D-02).
- El monto debe ser numérico y mayor que cero. La moneda, los decimales y los límites están pendientes (D-03).
- Si no se reconoce la fecha, se debe definir si se propone la fecha actual o se deja vacía; decisión D-04.
- No se realizan llamadas a OpenAI, a otro proveedor de IA ni a servicios de interpretación de lenguaje natural. La verificación incluye pruebas de red y revisión de dependencias.
- La respuesta debe distinguir entre campos interpretados, campos no reconocidos y errores de validación.
- Errores esperados: 400 por texto inválido, 401 sin sesión, 422 por texto no interpretable, 503 si el servicio determinista no está disponible.
- El texto original no se modifica durante el procesamiento.

**Dependencias**

- HU-10 (texto de entrada).
- Diccionario, catálogo de categorías y reglas deterministas aprobados.
- HU-12 (revisión del resultado).
- HU-33 para privacidad del texto.

**Pruebas sugeridas**

- Corpus de frases con montos en distintos formatos, tildes, abreviaturas, errores ortográficos y frases sin monto.
- Pruebas de determinismo: misma entrada y versión producen el mismo resultado.
- Prueba de que no existe tráfico hacia APIs externas de IA.
- Pruebas de validación de categoría, monto inválido, tiempo de espera y reintento.
- Prueba de ejemplo completo «Hoy gasté $8.000 en un taxi».

**Ambigüedades y decisiones pendientes**

- Contenido y mantenimiento del diccionario; sinónimos, regionalismos y errores tolerados (D-05).
- Catálogo definitivo de categorías y regla para casos ambiguos o desconocidos (D-02).
- Moneda, separadores, decimales y límites de monto (D-03).
- Tratamiento de fechas relativas («hoy», «ayer»), zona horaria y frases con varias fechas (D-04).
- Transparencia de la etiqueta «Procesar con IA» frente a una implementación determinista (D-15).
- ¿Se debe mostrar al Usuario qué palabra o regla activó la interpretación? Es recomendable para confianza, pero no está acordado.

**Trazabilidad:** se conserva el propósito original de procesar con el botón «Procesar con IA»; se sustituye explícitamente cualquier expectativa de API externa por el diccionario y las reglas deterministas acordadas. Sin cambio de objetivo.

#### HU-12 — Revisar y corregir los campos interpretados antes de guardar

**Módulo:** 3 · Registro y gestión de gastos  
**Prioridad:** **Must Have.** La revisión obligatoria es una expectativa explícita del Usuario potencial y una condición funcional del proyecto. Protege la calidad de los datos y evita guardar interpretaciones erróneas.  
**MVP:** Sí.

> **Historia:** Como Usuario, quiero revisar y corregir el monto, la categoría, la descripción y los demás campos interpretados antes de guardar, para asegurar que el gasto quede registrado correctamente.

**Objetivo y valor:** dar control total al Usuario sobre lo que se almacenará. Ningún gasto debe guardarse de forma automática tras el procesamiento; la confirmación debe ser explícita.

**Criterios de aceptación**

- **CA-12.1** — **Dado** que existe una interpretación generada, **cuando** el Usuario abre la vista de revisión, **entonces** ve el texto original y todos los campos interpretados: monto, categoría, descripción, fecha y moneda cuando corresponda.
- **CA-12.2** — **Dado** que el Usuario modifica el monto, la categoría, la descripción o la fecha, **cuando** confirma el guardado, **entonces** se persisten los valores corregidos y el texto original permanece sin cambios.
- **CA-12.3** — **Dado** que el Usuario introduce un monto vacío, cero, negativo o no numérico, **cuando** intenta guardar, **entonces** ve un error en el campo y el guardado queda bloqueado.
- **CA-12.4** — **Dado** que el Usuario selecciona una categoría fuera del catálogo, deja vacía la descripción o introduce una fecha inválida, **cuando** intenta guardar, **entonces** el sistema muestra el error correspondiente y no persiste el gasto.
- **CA-12.5** — **Dado** que el Usuario descarta la revisión, **cuando** confirma el descarte, **entonces** no se crea ningún gasto y el borrador deja de estar disponible; si hay cambios sin guardar, se advierte antes de salir.
- **CA-12.6** — **Dado** que el procesamiento no reconoció un campo, **cuando** el Usuario lo completa manualmente con un valor válido, **entonces** puede continuar con la revisión y guardar el gasto; no se guarda ningún valor inventado por el sistema.
- **CA-12.7** — **Dado** que un Usuario intenta acceder al borrador de otra persona, **cuando** envía una solicitud con otro identificador, **entonces** el backend rechaza el acceso y no devuelve el contenido.

**Reglas de negocio, validaciones y errores**

- La confirmación debe ser explícita; no existe guardado automático ni por temporizador.
- La vista previa debe validar en la interfaz y el backend debe repetir todas las validaciones; la interfaz no es la única defensa.
- El texto original es inmutable y se conserva para trazabilidad; las correcciones se aplican a los campos interpretados.
- La categoría debe pertenecer al catálogo aprobado (D-02). El monto debe ser mayor que cero y respetar la moneda y los límites (D-03).
- La fecha, la zona horaria y la política sobre fechas futuras están pendientes (D-04).
- La longitud máxima de la descripción y el tratamiento de espacios están pendientes (D-05).
- Si el Usuario abandona la pantalla con cambios, se advierte; no se guarda un borrador parcial sin consentimiento.
- Errores esperados: 400/422 por validación, 401 sin sesión, 403/404 por acceso a un borrador ajeno, 409 si el borrador ya fue guardado o expiró.

**Dependencias**

- HU-11 (interpretación).
- HU-13 (persistencia al confirmar).
- HU-33 (autorización del borrador y del gasto).

**Pruebas sugeridas**

- Prueba de interfaz: todos los campos editables, errores por campo, descarte y advertencia.
- Prueba de integración: valores corregidos persistidos y texto original conservado.
- Prueba de validación en backend con datos manipulados.
- Prueba de autorización sobre borradores de otros Usuarios.
- Prueba de extremo a extremo: procesar, corregir, confirmar y ver en historial.

**Ambigüedades y decisiones pendientes**

- ¿Se permite una fecha futura? ¿Cómo se valida según la zona horaria? (D-04).
- Longitud y contenido permitido en la descripción (D-05).
- ¿El borrador se conserva si la aplicación se cierra o la sesión vence? No está definido.
- ¿Se debe mostrar una explicación de por qué se asignó una categoría? Es recomendable, pero no está acordado.

**Trazabilidad:** se conserva el propósito original «revisar y corregir monto, categoría, descripción y otros campos antes de guardar»; se precisa la confirmación obligatoria y la validación en backend. Sin cambio funcional.

#### HU-13 — Guardar el gasto bajo la cuenta del propietario y aislarlo de otros usuarios

**Módulo:** 3 · Registro y gestión de gastos  
**Prioridad:** **Must Have.** Sin persistencia no hay historial, estadísticas ni fugas. La asignación de propietario y el aislamiento son condiciones de privacidad y confianza.  
**MVP:** Sí.

> **Historia:** Como Usuario, quiero que cada gasto se guarde en mi cuenta y quede aislado de las demás, para proteger mi información financiera.

**Objetivo y valor:** persistir el gasto confirmado con un propietario derivado de la sesión, garantizar que solo ese propietario pueda acceder a él y evitar duplicados o registros parciales por reintentos.

**Criterios de aceptación**

- **CA-13.1** — **Dado** que el Usuario confirma un gasto válido, **cuando** el backend procesa la solicitud, **entonces** obtiene el propietario del token verificado, guarda monto, categoría, descripción, fecha, moneda, texto original, versiones del diccionario y de reglas, y devuelve el identificador del gasto creado.
- **CA-13.2** — **Dado** que el cliente envía un identificador de propietario distinto al de la sesión, **cuando** el backend procesa la solicitud, **entonces** ignora o rechaza ese valor y nunca guarda el gasto a nombre de otra cuenta.
- **CA-13.3** — **Dado** que un Usuario B conoce el identificador de un gasto del Usuario A, **cuando** intenta consultarlo, editarlo o eliminarlo, **entonces** el backend responde con 404 o 403 sin revelar monto, categoría, descripción ni la existencia del recurso.
- **CA-13.4** — **Dado** que la confirmación se reintenta por un fallo de red, **cuando** llega la misma solicitud con la misma clave de idempotencia, **entonces** el sistema no crea un gasto duplicado y devuelve el resultado correspondiente a la operación ya realizada.
- **CA-13.5** — **Dado** que falla la escritura en la base de datos, **cuando** termina la operación, **entonces** no queda un gasto parcial y el Usuario puede reintentar; la respuesta no expone detalles internos.
- **CA-13.6** — **Dado** que la sesión venció antes de confirmar, **cuando** el Usuario intenta guardar, **entonces** recibe 401, el borrador se conserva localmente si la política lo permite y se le solicita iniciar sesión de nuevo antes de reintentar.

**Reglas de negocio, validaciones y errores**

- El propietario siempre se deriva de la sesión verificada; nunca de un campo controlado por el cliente.
- El gasto se valida en el backend con las mismas reglas de HU-12.
- La escritura debe ser atómica para el registro; se debe impedir la creación de duplicados por reintentos.
- Cada gasto debe tener un identificador único y un índice que permita consultas eficientes por propietario y fecha.
- No se registran montos, descripciones, tokens ni datos personales en logs de depuración.
- Los gastos se conservan hasta que una operación de eliminación o una política de retención aprobada indique lo contrario (D-06).
- Respuestas esperadas: 201 al crear, 200 si la idempotencia devuelve un resultado existente, 400/422 por validación, 401 sin sesión o sesión vencida, 403/404 por acceso ajeno, 409 por conflicto, 5xx sin datos sensibles.

**Dependencias**

- HU-12 (confirmación y validación).
- HU-33 (autorización, propiedad y privacidad).
- HU-02 (identidad y sesión).
- Habilita HU-14, HU-16, HU-20, HU-21, HU-23 y HU-28.

**Pruebas sugeridas**

- Prueba de integración: guardado y recuperación con el propietario correcto.
- Prueba de seguridad: intento de asignar otro propietario, acceso con identificador ajeno y modificación de la sesión.
- Prueba de idempotencia: dos solicitudes simultáneas o repetidas producen un solo gasto.
- Prueba de fallo de base de datos y de sesión vencida.
- Verificación de que el texto y los datos no aparecen en logs.

**Ambigüedades y decisiones pendientes**

- ¿Cuánto tiempo se conserva la clave de idempotencia y cómo se maneja un reintento con contenido distinto? (D-05/D-06).
- ¿Se admite el registro sin conexión con sincronización posterior? No está en el alcance actual.
- Moneda, decimales y límites de monto (D-03).
- Política de retención y eliminación (D-06).

**Trazabilidad:** se conserva el propósito original «guardar cada gasto en la cuenta del propietario y protegerlo del acceso de otras cuentas»; se precisan idempotencia, atomicidad, autorización y errores. Sin cambio funcional.

#### HU-14 — Consultar el historial de gastos del más reciente al más antiguo

**Módulo:** 3 · Registro y gestión de gastos  
**Prioridad:** **Must Have.** Es la forma básica de comprobar que un gasto quedó guardado y de consultar la información acumulada. Sin historial, el registro no tiene utilidad visible.  
**MVP:** Sí.

> **Historia:** Como Usuario, quiero ver mi historial de gastos ordenado del más reciente al más antiguo, para consultar y entender mis registros.

**Objetivo y valor:** ofrecer una lista cronológica de los gastos propios, con la información esencial y un rendimiento adecuado, sin exponer gastos de otras cuentas.

**Criterios de aceptación**

- **CA-14.1** — **Dado** que el Usuario tiene gastos guardados, **cuando** abre el historial, **entonces** ve una lista ordenada de forma descendente por fecha del gasto y, en caso de empate, por fecha de creación; cada elemento muestra monto, categoría, descripción y fecha.
- **CA-14.2** — **Dado** que el Usuario tiene más gastos que el tamaño de página configurado, **cuando** se desplaza o solicita la siguiente página, **entonces** recibe registros adicionales sin duplicados ni omisiones y puede llegar hasta el más antiguo.
- **CA-14.3** — **Dado** que el Usuario no tiene gastos, **cuando** abre el historial, **entonces** ve un estado vacío con una acción para registrar el primer gasto, sin mensajes de error.
- **CA-14.4** — **Dado** que la consulta falla por red o servidor, **cuando** la aplicación recibe el error, **entonces** muestra un mensaje y una acción de reintento sin borrar los datos ya cargados.
- **CA-14.5** — **Dado** que el Usuario abre el detalle de un gasto de su historial, **cuando** la pantalla carga, **entonces** ve los datos del gasto y las acciones permitidas; **dado** que intenta abrir un gasto ajeno por identificador, **entonces** recibe un error sin datos.
- **CA-14.6** — **Dado** que un gasto fue eliminado según HU-16, **cuando** el Usuario actualiza el historial, **entonces** el gasto ya no aparece en la lista.

**Reglas de negocio, validaciones y errores**

- Toda consulta se filtra por el propietario derivado de la sesión.
- La paginación debe ser estable; se recomienda paginación por cursor para evitar saltos cuando se crean gastos nuevos. El tamaño de página es configurable y su valor inicial está pendiente (D-05).
- El orden usa la fecha del gasto como criterio principal y la fecha de creación como desempate. La zona horaria está pendiente (D-04).
- Los gastos eliminados o excluidos por la política de retención no se muestran.
- El detalle no debe cargar datos de otro Usuario ni confiar en un propietario enviado por el cliente.
- Respuestas esperadas: 200 con página, 400 por parámetros inválidos, 401 sin sesión, 403/404 por recurso ajeno, 5xx sin detalles.

**Dependencias**

- HU-13 (gastos persistidos).
- HU-33 (aislamiento por propietario).
- Habilita HU-15, HU-16 y HU-24.

**Pruebas sugeridas**

- Prueba de orden con fechas iguales y distintas.
- Prueba de paginación con más registros que el tamaño de página; verificar ausencia de duplicados y omisiones.
- Prueba de estado vacío, error y reintento.
- Prueba de seguridad con el identificador de un gasto ajeno.
- Prueba de actualización tras crear o eliminar un gasto.

**Ambigüedades y decisiones pendientes**

- Tamaño de página, agrupación por día y formato de fecha (D-04/D-05).
- ¿Se muestran los gastos de meses anteriores en la misma lista o se separan por periodo? No está definido.
- ¿Se permite buscar por texto? No está en las 33 historias.
- ¿Qué ocurre con el historial si la cuenta se desactiva? Depende de D-06.

**Trazabilidad:** se conserva el propósito original «ver el historial ordenado del más reciente al más antiguo»; se precisan paginación, detalle, estados y autorización. Sin cambio funcional.

#### HU-15 — Filtrar el historial por fecha y categoría

**Módulo:** 3 · Registro y gestión de gastos  
**Prioridad:** **Should Have.** Mejora mucho la consulta cuando hay muchos gastos, pero el MVP puede operar con el historial completo. Es una extensión natural de HU-14 y puede añadirse después del núcleo.  
**MVP:** No.

> **Historia:** Como Usuario, quiero filtrar mi historial por fecha y categoría, para encontrar gastos concretos sin revisar toda la lista.

**Objetivo y valor:** permitir consultas acotadas y combinables, manteniendo el aislamiento por propietario y la coherencia con la paginación.

**Criterios de aceptación**

- **CA-15.1** — **Dado** que el Usuario está en el historial, **cuando** selecciona un rango de fechas y una categoría, **entonces** la lista muestra solo sus gastos que cumplen ambos criterios, con las fechas de inicio y fin incluidas en el rango.
- **CA-15.2** — **Dado** que el Usuario aplica solo una categoría o solo un rango de fechas, **cuando** se ejecuta el filtro, **entonces** se aplica únicamente el criterio seleccionado y se mantienen los demás filtros vacíos.
- **CA-15.3** — **Dado** que la fecha inicial es posterior a la fecha final, **cuando** el Usuario intenta aplicar el filtro, **entonces** ve un error de validación y la lista no se modifica.
- **CA-15.4** — **Dado** que no existen gastos que cumplan los filtros, **cuando** termina la consulta, **entonces** se muestra un estado vacío con la opción de limpiar filtros.
- **CA-15.5** — **Dado** que hay filtros activos, **cuando** el Usuario pulsa «Limpiar filtros», **entonces** se recupera el historial completo y los filtros visibles se restablecen.
- **CA-15.6** — **Dado** que el Usuario manipula un parámetro de propietario en la consulta, **cuando** el backend procesa el filtro, **entonces** el parámetro no tiene efecto y solo devuelve gastos de la sesión.

**Reglas de negocio, validaciones y errores**

- Los filtros se combinan con AND: rango de fechas y categoría deben cumplirse simultáneamente.
- El rango de fechas es inclusivo en ambos extremos, según la zona horaria definida (D-04).
- La categoría debe pertenecer al catálogo aprobado (D-02).
- El filtrado se aplica en el backend y respeta la paginación; no se descargan todos los gastos para filtrar en el cliente.
- Los filtros no modifican ni eliminan gastos.
- Respuestas esperadas: 200 con resultados, 400 por rango o categoría inválidos, 401 sin sesión, 403/404 si se intenta acceder a otra cuenta.

**Dependencias**

- HU-14 (historial y paginación).
- HU-33 (aislamiento de datos).
- Catálogo de categorías aprobado (D-02).

**Pruebas sugeridas**

- Prueba de límites de fecha: primer y último día del rango.
- Prueba de combinación de ambos filtros y de filtros individuales.
- Prueba de rango invertido, categoría inválida y estado vacío.
- Prueba de limpieza de filtros y de paginación con filtros activos.
- Prueba de seguridad con un propietario manipulado.

**Ambigüedades y decisiones pendientes**

- ¿Se permiten varias categorías a la vez? No está definido; el criterio inicial es una.
- ¿Los filtros se conservan al salir de la pantalla o al reiniciar la app? No está definido.
- Formato de fecha, zona horaria y rango máximo permitido (D-04).
- ¿Se ofrece búsqueda por descripción? No está en las 33 historias.

**Trazabilidad:** se conserva el propósito original «filtrar por fecha y categoría»; se precisan combinación, límites, estado vacío y autorización. Sin cambio funcional.

#### HU-16 — Editar y eliminar gastos guardados, actualizando análisis y resúmenes

**Módulo:** 3 · Registro y gestión de gastos  
**Prioridad:** **Should Have.** Corregir o eliminar un gasto ya guardado es importante para la confianza y la calidad de los datos, pero el MVP puede sostenerse con la revisión previa a la confirmación. La coherencia con estadísticas y fugas añade complejidad, por lo que se planifica después de los Must.  
**MVP:** No.

> **Historia:** Como Usuario, quiero editar o eliminar gastos guardados, para corregir errores y mantener actualizados mis análisis y resúmenes.

**Objetivo y valor:** permitir la corrección posterior de un gasto sin perder el texto original y garantizar que el historial, el dashboard y las posibles fugas reflejen el cambio o la eliminación.

**Criterios de aceptación**

- **CA-16.1** — **Dado** que el Usuario abre el detalle de un gasto propio, **cuando** elige editar, **entonces** puede modificar monto, categoría, descripción y fecha, mientras el texto original permanece en modo solo lectura.
- **CA-16.2** — **Dado** que el Usuario guarda una edición con valores válidos, **cuando** el backend la procesa, **entonces** persiste los cambios, actualiza la fecha de modificación y el historial muestra los nuevos valores.
- **CA-16.3** — **Dado** que el Usuario edita un gasto, **cuando** vuelve a consultar el dashboard, las estadísticas por categoría o las posibles fugas, **entonces** los resultados se recalculan o invalidan y reflejan el valor actualizado; no se muestran totales obsoletos.
- **CA-16.4** — **Dado** que el Usuario elige eliminar un gasto propio, **cuando** confirma la eliminación, **entonces** el gasto deja de aparecer en el historial, el dashboard, las estadísticas y las fugas, y la operación queda registrada según la política de auditoría.
- **CA-16.5** — **Dado** que el Usuario intenta editar o eliminar un gasto de otra cuenta, **cuando** envía la solicitud, **entonces** el backend la rechaza sin revelar datos ni confirmar la existencia del recurso.
- **CA-16.6** — **Dado** que la edición o eliminación falla, **cuando** termina la operación, **entonces** el gasto conserva su estado anterior y el Usuario recibe un mensaje con posibilidad de reintentar; no queda un estado parcial.
- **CA-16.7** — **Dado** que el Usuario introduce valores inválidos al editar, **cuando** intenta guardar, **entonces** se aplican las mismas validaciones de HU-12 y no se modifica el gasto.

**Reglas de negocio, validaciones y errores**

- Solo el propietario puede editar o eliminar; el propietario se deriva de la sesión.
- El texto original no se modifica; las correcciones se aplican a los campos estructurados.
- La eliminación puede ser lógica o física; la decisión y la retención están pendientes (D-06). En cualquier caso, el gasto eliminado no debe aparecer en ningún análisis.
- Las vistas agregadas deben calcularse sobre datos vigentes o invalidar sus cachés al modificar o eliminar. No se acepta una actualización diferida indefinida.
- Las operaciones deben ser atómicas y estar protegidas contra reintentos duplicados.
- Si hay concurrencia, se debe definir la estrategia (por ejemplo, control de versión); está pendiente.
- Respuestas esperadas: 200 al editar, 204 al eliminar, 400/422 por validación, 401 sin sesión, 403/404 por recurso ajeno, 409 por conflicto de concurrencia.

**Dependencias**

- HU-13 (gasto persistido).
- HU-14 (detalle e historial).
- HU-20, HU-21 y HU-23 para verificar la actualización de agregados y fugas.
- HU-33 (autorización).
- Decisión D-06 sobre eliminación y retención.

**Pruebas sugeridas**

- Prueba de edición de cada campo y persistencia posterior.
- Prueba de eliminación y desaparición en historial, dashboard, estadísticas y fugas.
- Prueba de autorización con identificadores ajenos.
- Prueba de validaciones y de fallo atómico.
- Prueba de concurrencia o de doble envío.

**Ambigüedades y decisiones pendientes**

- ¿La eliminación es lógica o física? ¿Se permite deshacer? (D-06).
- ¿Se conserva un historial de cambios o auditoría de ediciones? (D-14).
- ¿Cómo afecta cambiar la fecha de un gasto a los periodos y a las estadísticas? Debe recalcularse.
- ¿Qué ocurre si el gasto forma parte de una posible fuga mientras se edita? El análisis debe recalcularse.

**Trazabilidad:** se conserva el propósito original «editar y eliminar gastos guardados y actualizar los análisis y resúmenes afectados». Se mantiene una sola historia con dos operaciones; no se divide ni se elimina funcionalidad. La consistencia de agregados se hace explícita.

### 6.4 Módulo 4 — Registro por voz

#### HU-17 — Iniciar la grabación de voz para un gasto en Android

**Módulo:** 4 · Registro por voz  
**Prioridad:** **Could Have.** La voz es valiosa para el Usuario potencial y forma parte de la tecnología acordada, pero no es necesaria para el MVP. Exige permiso de micrófono, integración nativa, pruebas en dispositivos y una compilación de desarrollo; se implementa solo si el núcleo está estable.  
**MVP:** No.

> **Historia:** Como Usuario de Android, quiero iniciar la grabación de voz de un gasto, para registrarlo hablando en lugar de escribiendo.

**Objetivo y valor:** ofrecer un canal de entrada alternativo y de baja fricción, con control claro para iniciar, detener o cancelar, y con una salida manual disponible si el micrófono o el permiso no están disponibles.

**Criterios de aceptación**

- **CA-17.1** — **Dado** que el Usuario autenticado está en la pantalla de registro de gasto en un dispositivo Android compatible, **cuando** pulsa el control de voz, **entonces** la aplicación solicita el permiso de micrófono si aún no lo tiene y, una vez concedido, inicia una sesión de reconocimiento con un estado visible de escucha.
- **CA-17.2** — **Dado** que la sesión de voz está activa, **cuando** el Usuario pulsa detener, **entonces** la captura finaliza y el resultado se entrega al flujo de transcripción; **cuando** pulsa cancelar, **entonces** se descarta la captura y no se modifica el texto existente.
- **CA-17.3** — **Dado** que el Usuario deniega el permiso de micrófono, **cuando** intenta usar la voz, **entonces** ve una explicación clara, puede seguir con la entrada por texto y no se repite la solicitud de forma invasiva.
- **CA-17.4** — **Dado** que el dispositivo no es Android o el servicio de reconocimiento no está disponible, **cuando** el Usuario intenta usar la voz, **entonces** la opción no se ofrece o se muestra un mensaje de no disponible, sin bloquear el registro por texto.
- **CA-17.5** — **Dado** que la aplicación pasa a segundo plano, se navega fuera de la pantalla o se cierra la sesión, **cuando** ocurre el cambio, **entonces** la captura se detiene y los recursos del reconocedor se liberan.
- **CA-17.6** — **Dado** que el Usuario usa la voz, **cuando** la aplicación termina la captura, **entonces** no conserva el audio como archivo propio ni lo envía a un backend de FUGA+; solo utiliza el texto reconocido por el servicio del sistema.

**Reglas de negocio, validaciones y errores**

- La voz está disponible únicamente en Android; iOS y otras plataformas conservan la entrada por texto.
- El permiso `RECORD_AUDIO` debe solicitarse en tiempo de ejecución y explicarse antes o durante la solicitud.
- No se inicia una segunda sesión de reconocimiento mientras una esté activa.
- El audio no se almacena como archivo de la aplicación. Si el servicio del sistema operativo procesa audio fuera del dispositivo, debe existir un aviso de privacidad (D-12).
- La captura debe detenerse al perder el foco, al cancelar o al cerrar sesión.
- Errores esperados: permiso denegado, servicio no disponible, micrófono ocupado, error de red del reconocedor, tiempo de espera; todos deben ofrecer texto manual.
- La sesión de autenticación se valida antes de iniciar el flujo; un Usuario no autenticado no accede a la pantalla.

**Dependencias**

- HU-02 (Usuario autenticado).
- HU-10 (pantalla de entrada de gasto).
- HU-18 (conversión de voz a texto).
- Compilación de desarrollo con módulo nativo Kotlin; Expo Go no es suficiente.
- Decisión D-12 sobre privacidad, duración y tratamiento del audio.

**Pruebas sugeridas**

- Prueba manual en al menos dos versiones de Android y un dispositivo físico.
- Prueba de permiso concedido, denegado y revocado desde ajustes.
- Prueba de inicio, detención, cancelación y paso a segundo plano.
- Prueba de servicio no disponible y de ausencia de micrófono.
- Revisión de que no se persiste audio y de que el texto manual sigue disponible.

**Ambigüedades y decisiones pendientes**

- Versión mínima de Android y dispositivos objetivo (D-12).
- ¿Se permite voz sin conexión? Depende del servicio de reconocimiento del sistema.
- ¿Cuánto tiempo máximo puede durar una captura? (D-12).
- ¿Se muestra un aviso explícito de que el sistema puede procesar el audio en la nube? (D-12).
- ¿La opción de voz se oculta en iOS o se muestra deshabilitada con explicación?

**Trazabilidad:** se conserva el propósito original «iniciar la grabación de voz para un gasto en Android»; se precisan permisos, ciclo de vida, privacidad y alternativa. Sin cambio funcional.

#### HU-18 — Convertir la voz en texto con Kotlin y `SpeechRecognizer`

**Módulo:** 4 · Registro por voz  
**Prioridad:** **Could Have.** Es la implementación técnica que hace posible HU-17 y HU-19. Su dependencia de un módulo nativo y de las variaciones de Android la mantiene fuera del MVP, pero debe evaluarse si se prioriza la voz.  
**MVP:** No.

> **Historia:** Como Usuario de Android, quiero que mi voz se convierta en texto con `SpeechRecognizer`, para revisar y procesar la transcripción como un gasto.

**Objetivo y valor:** obtener una transcripción en español que el Usuario pueda editar antes de procesarla, aislando la complejidad nativa de Android del resto de la aplicación.

**Criterios de aceptación**

- **CA-18.1** — **Dado** que una sesión de voz está activa y el Usuario pronuncia una frase, **cuando** el reconocedor entrega un resultado final, **entonces** el módulo Kotlin envía la transcripción a React Native y la aplicación la muestra en un campo editable.
- **CA-18.2** — **Dado** que el reconocedor entrega resultados parciales, **cuando** la sesión continúa, **entonces** la aplicación puede mostrarlos como estado temporal, pero solo utiliza el resultado final para la transcripción que se envía a revisión.
- **CA-18.3** — **Dado** que el reconocedor devuelve un error de falta de coincidencia, tiempo de espera, red, ocupado o no disponible, **cuando** el módulo lo recibe, **entonces** lo traduce a un estado comprensible para la interfaz, permite reintentar o escribir manualmente y no bloquea la aplicación.
- **CA-18.4** — **Dado** que el Usuario cancela o la pantalla se cierra, **cuando** termina la sesión, **entonces** el reconocedor se detiene, se destruyen los recursos y no se entrega una transcripción tardía a una pantalla inactiva.
- **CA-18.5** — **Dado** que el servicio se inicia con el idioma configurado, **cuando** el Usuario habla en español, **entonces** la transcripción se obtiene en ese idioma; si el idioma no está disponible, se muestra un error y se ofrece texto manual.
- **CA-18.6** — **Dado** que se produce una transcripción, **cuando** el flujo termina, **entonces** no se inicia automáticamente el procesamiento ni se guarda el gasto: la transcripción queda editable para HU-19.

**Reglas de negocio, validaciones y errores**

- El módulo usa `SpeechRecognizer` de Android y expone a React Native solo eventos y resultados necesarios; no se acopla la lógica de gastos al código nativo.
- El idioma inicial debe definirse; se propone español de Colombia o el idioma español del dispositivo, pero la decisión está pendiente (D-12).
- Debe existir una sola sesión de reconocimiento activa y un manejo explícito de `onResults`, `onPartialResults`, `onError` y `onEndOfSpeech`.
- La transcripción puede ser vacía o imprecisa; el Usuario debe poder editarla o descartarla.
- No se guarda audio; el texto se mantiene en memoria hasta que el Usuario lo procese o descarte.
- Errores esperados: `ERROR_NO_MATCH`, `ERROR_SPEECH_TIMEOUT`, `ERROR_NETWORK`, `ERROR_RECOGNIZER_BUSY`, `ERROR_INSUFFICIENT_PERMISSIONS`, servicio no disponible.
- La duración máxima y el tamaño máximo de la transcripción están pendientes (D-12).

**Dependencias**

- HU-17 (inicio y permisos de la captura).
- Módulo nativo Kotlin integrado en la compilación de Android.
- HU-19 (revisión y procesamiento de la transcripción).
- Decisión D-12 sobre idioma, duración y privacidad.

**Pruebas sugeridas**

- Pruebas de instrumentación con un reconocedor simulado para cada error y para resultado final.
- Pruebas de ciclo de vida: pausa, reanudación, cancelación y cierre.
- Pruebas manuales de idioma, ruido, silencio y frases largas.
- Prueba de que no hay procesamiento ni guardado automático.
- Prueba de entrega tardía de resultados después de cancelar.

**Ambigüedades y decisiones pendientes**

- Idioma y variante regional; comportamiento si el dispositivo no tiene el paquete de idioma (D-12).
- ¿Se aceptan resultados parciales para habilitar el botón de procesar? La recomendación es esperar el resultado final.
- ¿Existe un límite de duración o de caracteres? (D-12).
- ¿El servicio del sistema requiere conexión o puede funcionar sin ella? Depende del dispositivo.
- ¿Se debe advertir que el reconocimiento puede usar servicios de Google? (D-12).

**Trazabilidad:** se conserva el propósito original «convertir voz en texto con Kotlin y `SpeechRecognizer`»; se precisan estados, errores, ciclo de vida y privacidad. Sin cambio funcional.

#### HU-19 — Revisar la transcripción y los campos antes de guardar un gasto por voz

**Módulo:** 4 · Registro por voz  
**Prioridad:** **Could Have.** Completa el flujo de voz y garantiza que la transcripción no se guarde sin revisión. Depende de las tres historias anteriores y de la interpretación determinista; se posterga con el resto del módulo.  
**MVP:** No.

> **Historia:** Como Usuario de Android, quiero revisar la transcripción y los campos interpretados antes de guardar un gasto por voz, para corregir errores de reconocimiento o de interpretación.

**Objetivo y valor:** mantener el control del Usuario en el canal de voz. El flujo debe ser exactamente: voz → transcripción editable → «Procesar con IA» → revisión de campos → confirmación y guardado.

**Criterios de aceptación**

- **CA-19.1** — **Dado** que el reconocedor produjo una transcripción, **cuando** el Usuario la recibe, **entonces** la ve en un campo editable y puede corregirla antes de pulsar «Procesar con IA».
- **CA-19.2** — **Dado** que el Usuario modifica la transcripción, **cuando** pulsa «Procesar con IA», **entonces** el procesamiento utiliza el texto editado y el texto original guardado con el gasto es la transcripción editada, no una versión anterior.
- **CA-19.3** — **Dado** que la transcripción está vacía, **cuando** el Usuario intenta procesarla, **entonces** el sistema muestra un error y permite volver a grabar o escribir manualmente; no se envía una transcripción vacía al procesador.
- **CA-19.4** — **Dado** que el procesamiento devuelve campos, **cuando** el Usuario continúa, **entonces** debe pasar por la revisión de HU-12 y confirmar explícitamente antes de guardar; no existe guardado automático.
- **CA-19.5** — **Dado** que la voz falla en cualquier punto, **cuando** el Usuario lo decide, **entonces** puede continuar con la entrada por texto sin perder el flujo de revisión.
- **CA-19.6** — **Dado** que el Usuario cancela la revisión o descarta el gasto, **cuando** confirma el descarte, **entonces** no se guarda ningún registro y el texto se elimina del estado de trabajo.

**Reglas de negocio, validaciones y errores**

- El flujo no puede saltarse la transcripción editable, el procesamiento ni la revisión.
- La transcripción es texto no confiable: se escapa en la interfaz y se valida como cualquier texto de gasto.
- La transcripción editada se convierte en el texto original del gasto; si se desea conservar también la transcripción automática sin editar, debe decidirse y documentarse (D-12).
- Se aplican las mismas validaciones de HU-12 y la misma persistencia de HU-13.
- La voz solo está disponible en Android; el flujo manual es la alternativa.
- Errores esperados: transcripción vacía, error de reconocimiento, error de procesamiento, error de validación, error de guardado; todos con opción de reintento o texto manual.

**Dependencias**

- HU-10, HU-11 y HU-12 (entrada, procesamiento y revisión).
- HU-17 y HU-18 (captura y transcripción).
- HU-13 para la persistencia final.
- Decisión D-12 sobre conservación de la transcripción.

**Pruebas sugeridas**

- Prueba de extremo a extremo en dispositivo Android: voz, transcripción, edición, procesamiento, revisión y guardado.
- Prueba de transcripción vacía, error de voz y cambio a texto manual.
- Prueba de edición de la transcripción y verificación de que el gasto guarda el texto editado.
- Prueba de cancelación y descarte.
- Prueba de autorización y privacidad del texto.

**Ambigüedades y decisiones pendientes**

- ¿Se conserva la transcripción automática original además de la editada? (D-12).
- ¿Se admite más de un gasto en una misma transcripción? El alcance inicial asume uno.
- ¿Cómo se manejan puntuación, mayúsculas y palabras mal reconocidas? Depende del diccionario y del reconocedor (D-05/D-12).
- ¿Se permite reintentar la grabación sin perder una transcripción editada? Debe definirse en la experiencia.

**Trazabilidad:** se conserva el propósito original «revisar y corregir la transcripción y los campos antes de guardar»; se precisa el flujo obligatorio y la relación con HU-11, HU-12 y HU-13. Sin cambio funcional.

### 6.5 Módulo 5 — Dashboard y estadísticas

#### HU-20 — Consultar total, cantidad y promedio de gasto por periodo

**Módulo:** 5 · Dashboard y estadísticas  
**Prioridad:** **Must Have.** Responde a la primera necesidad expresada por el Usuario potencial: saber cuánto gastó en el mes. Es la vista que da sentido a los datos registrados y forma parte del flujo de demostración.  
**MVP:** Sí.

> **Historia:** Como Usuario, quiero consultar el total gastado, la cantidad de gastos y el promedio por gasto en un periodo, para entender cuánto gasto.

**Objetivo y valor:** ofrecer un resumen claro y confiable del periodo seleccionado, calculado exclusivamente con los gastos del Usuario y actualizado cuando los datos cambian.

**Criterios de aceptación**

- **CA-20.1** — **Dado** que el Usuario autenticado abre el dashboard, **cuando** la pantalla carga, **entonces** ve el periodo seleccionado —por defecto el mes actual, según la zona horaria definida— y los valores de total gastado, cantidad de gastos y promedio por gasto.
- **CA-20.2** — **Dado** un periodo con gastos, **cuando** se comparan los valores mostrados con los registros del Usuario, **entonces** el total coincide con la suma de los montos, la cantidad coincide con el número de gastos y el promedio coincide con total dividido por cantidad, con el redondeo de presentación aprobado.
- **CA-20.3** — **Dado** un periodo sin gastos, **cuando** el dashboard carga, **entonces** muestra cero o «sin datos» de forma explícita, evitando una división por cero y explicando que no hay registros.
- **CA-20.4** — **Dado** que el Usuario cambia el periodo, **cuando** se aplica la selección, **entonces** los tres valores se recalculan para ese periodo y solo incluyen gastos propios.
- **CA-20.5** — **Dado** que el Usuario crea, edita o elimina un gasto, **cuando** vuelve al dashboard o actualiza, **entonces** los valores reflejan el cambio y no se muestra un total obsoleto.
- **CA-20.6** — **Dado** que un Usuario intenta obtener el dashboard de otro mediante parámetros manipulados, **cuando** el backend procesa la solicitud, **entonces** solo calcula con la identidad de la sesión y no devuelve datos ajenos.

**Reglas de negocio, validaciones y errores**

- Los cálculos se realizan en el backend sobre los gastos vigentes del propietario; no se acepta un identificador de propietario enviado por el cliente.
- El periodo por defecto es el mes actual; los periodos disponibles dependen de D-04.
- El promedio se define como **promedio por gasto** (total / cantidad). Si el producto necesita promedio por día, es una decisión adicional.
- Los gastos eliminados no se incluyen. Los gastos editados usan sus valores vigentes.
- Los importes se muestran con la moneda y el formato definidos en D-03; el cálculo no debe depender del redondeo visual.
- Respuestas esperadas: 200 con el resumen, 400 por periodo inválido, 401 sin sesión, 5xx sin detalles internos.

**Dependencias**

- HU-13 (gastos persistidos).
- HU-16 para la actualización tras edición o eliminación.
- HU-33 (privacidad y filtro por propietario).
- Decisiones D-03 y D-04 sobre moneda, fechas y periodos.

**Pruebas sugeridas**

- Prueba con un conjunto conocido de gastos: total, cantidad y promedio exactos.
- Prueba de periodo vacío y de un solo gasto.
- Prueba de límites del mes y de zona horaria.
- Prueba después de crear, editar y eliminar.
- Prueba de seguridad con propietario manipulado.
- Prueba de redondeo y formato de moneda.

**Ambigüedades y decisiones pendientes**

- ¿El promedio debe ser por gasto o por día? La historia original es ambigua; se adopta por gasto para el MVP.
- Periodos disponibles: mes, semana, rango personalizado o comparación (D-04).
- Zona horaria y límites exactos del mes (D-04).
- Moneda, decimales y redondeo (D-03).
- ¿Se incluyen gastos futuros? Depende de D-04.

**Trazabilidad:** se conserva el propósito original «ver total, número de gastos y promedio por periodo»; se precisa el promedio por gasto, el periodo y la actualización. Sin cambio funcional.

#### HU-21 — Consultar el gasto por categoría e identificar la categoría de mayor gasto

**Módulo:** 5 · Dashboard y estadísticas  
**Prioridad:** **Must Have.** Explica en qué se concentra el dinero y alimenta la propuesta de posibles fugas. Sin el desglose, el dashboard solo muestra un total y pierde valor para el Usuario.  
**MVP:** Sí.

> **Historia:** Como Usuario, quiero ver el gasto por categoría y cuál es la categoría de mayor gasto, para identificar en qué se concentra mi dinero.

**Objetivo y valor:** presentar una distribución comprensible del gasto del periodo, destacando la categoría con mayor importe sin juzgar los hábitos del Usuario.

**Criterios de aceptación**

- **CA-21.1** — **Dado** un periodo con gastos en varias categorías, **cuando** el Usuario abre el desglose, **entonces** ve cada categoría con su total y su participación respecto del total del periodo.
- **CA-21.2** — **Dado** el mismo conjunto de datos, **cuando** el sistema identifica la categoría de mayor gasto, **entonces** destaca la categoría cuyo total es el máximo y el valor coincide con la suma de sus gastos.
- **CA-21.3** — **Dado** que dos o más categorías tienen el mismo total máximo, **cuando** se muestra el resultado, **entonces** se indica el empate o se aplica la regla de desempate aprobada (D-02), sin elegir una arbitrariamente sin explicación.
- **CA-21.4** — **Dado** un periodo sin gastos, **cuando** se abre el desglose, **entonces** se muestra un estado vacío y no se inventa una categoría principal.
- **CA-21.5** — **Dado** que el Usuario crea, edita o elimina un gasto, **cuando** actualiza el dashboard, **entonces** la distribución y la categoría principal reflejan los datos vigentes.
- **CA-21.6** — **Dado** que el Usuario consulta el desglose, **cuando** se revisan los datos, **entonces** solo aparecen gastos propios y no se incluyen categorías de otros Usuarios.

**Reglas de negocio, validaciones y errores**

- Las categorías deben pertenecer al catálogo cerrado aprobado (D-02).
- Las categorías sin gastos pueden omitirse o mostrarse en cero; la decisión está pendiente.
- El porcentaje se calcula sobre el total del periodo; si el total es cero, no se calcula y se muestra el estado vacío.
- Los gastos eliminados no se incluyen; los editados usan la categoría vigente.
- La categoría «Otros» y su tratamiento deben definirse en D-02.
- Respuestas esperadas: 200 con distribución, 400 por periodo inválido, 401 sin sesión, 5xx sin datos sensibles.

**Dependencias**

- HU-13 (gastos persistidos).
- HU-20 (periodo y total del dashboard).
- HU-16 para la actualización tras cambios.
- Catálogo de categorías aprobado (D-02).

**Pruebas sugeridas**

- Prueba con varias categorías y totales conocidos; verificar suma y porcentajes.
- Prueba de categoría principal y de empate.
- Prueba de periodo vacío y de una sola categoría.
- Prueba después de editar la categoría de un gasto.
- Prueba de seguridad y de exclusión de datos ajenos.

**Ambigüedades y decisiones pendientes**

- Lista definitiva de categorías y regla de «Otros» (D-02).
- ¿Cómo se representa un empate? La propuesta provisional es mostrar todas las categorías empatadas e indicarlo.
- ¿Se muestran categorías con cero? No está definido.
- ¿Se incluye una gráfica, una lista o ambas? Es una decisión de diseño.
- ¿La categoría principal se calcula solo por monto o también por frecuencia? La historia pide mayor gasto; se asume por monto.

**Trazabilidad:** se conserva el propósito original «ver gastos por categoría e identificar la de mayor gasto»; se precisan empate, porcentajes, periodo y actualización. Sin cambio funcional.

#### HU-22 — Comparar el gasto entre periodos

**Módulo:** 5 · Dashboard y estadísticas  
**Prioridad:** **Could Have.** El Usuario potencial indicó que el mes actual suele ser suficiente y que la comparación es ocasional. No es necesaria para el MVP y añade cálculos y estados de borde.  
**MVP:** No.

> **Historia:** Como Usuario, quiero comparar mis gastos entre dos periodos, para detectar cambios en mi comportamiento de gasto.

**Objetivo y valor:** permitir una comparación descriptiva —no predictiva ni valorativa— entre dos periodos, mostrando totales, cantidades, promedios y variaciones.

**Criterios de aceptación**

- **CA-22.1** — **Dado** que el Usuario selecciona dos periodos con datos, **cuando** se ejecuta la comparación, **entonces** ve para cada periodo el total, la cantidad de gastos y el promedio por gasto, calculados solo con sus registros.
- **CA-22.2** — **Dado** que ambos periodos tienen total mayor que cero, **cuando** se muestra la variación, **entonces** se presenta la diferencia absoluta y la variación porcentual con la fórmula y el redondeo aprobados.
- **CA-22.3** — **Dado** que el periodo base tiene total cero, **cuando** se calcula la variación porcentual, **entonces** el sistema indica que no es calculable y muestra la diferencia absoluta sin producir una división por cero.
- **CA-22.4** — **Dado** que uno o ambos periodos no tienen gastos, **cuando** se muestra la comparación, **entonces** se identifica claramente el periodo sin registros y no se muestran valores inventados.
- **CA-22.5** — **Dado** que el Usuario crea, edita o elimina un gasto de cualquiera de los periodos, **cuando** actualiza la comparación, **entonces** los valores se recalculan.
- **CA-22.6** — **Dado** que el Usuario intenta comparar datos de otra cuenta, **cuando** manipula parámetros, **entonces** el backend solo usa la identidad de la sesión y no devuelve información ajena.

**Reglas de negocio, validaciones y errores**

- Los periodos deben ser válidos y comparables según el selector aprobado (D-04). El alcance inicial puede limitarse a meses, pero no se fija aquí.
- La diferencia absoluta se calcula como periodo B menos periodo A; la variación porcentual se calcula respecto del periodo base A, con la fórmula documentada en la interfaz.
- El promedio es por gasto, coherente con HU-20.
- No se emiten juicios de valor ni predicciones sobre el comportamiento del Usuario.
- Los gastos eliminados no se incluyen; los editados usan valores vigentes.
- Respuestas esperadas: 200 con la comparación, 400 por periodos inválidos, 401 sin sesión, 5xx sin datos sensibles.

**Dependencias**

- HU-20 y HU-21 (métricas y desglose del periodo).
- HU-16 para la actualización tras cambios.
- Decisión D-04 sobre periodos y zona horaria.

**Pruebas sugeridas**

- Prueba con dos periodos de totales conocidos y verificación de fórmulas.
- Prueba con periodo base cero y con ambos periodos vacíos.
- Prueba de un solo periodo con datos.
- Prueba de límites de periodo y de actualización tras cambios.
- Prueba de seguridad con parámetros manipulados.

**Ambigüedades y decisiones pendientes**

- Tipos de periodo permitidos: meses, semanas o rangos personalizados (D-04).
- ¿Se permiten periodos solapados? No está definido.
- ¿Cómo se presenta una variación negativa? Debe ser descriptiva, sin lenguaje que juzgue al Usuario.
- Fórmula, redondeo y moneda exactos (D-03/D-04).
- ¿La comparación incluye el mes actual parcial? Debe definirse.

**Trazabilidad:** se conserva el propósito original «comparar gastos entre distintos periodos»; se precisan fórmulas, estados sin datos y actualización. Sin cambio funcional.

### 6.6 Módulo 6 — Detección de fugas de dinero

#### HU-23 — Detectar posibles fugas de dinero con reglas deterministas

**Módulo:** 6 · Detección de fugas de dinero  
**Prioridad:** **Must Have.** Es la propuesta de valor diferencial de FUGA+. Sin detección, la aplicación sería un registro de gastos más. Debe ser determinista, explicable y no inventar parámetros.  
**MVP:** Sí.

> **Historia:** Como Usuario, quiero que FUGA+ detecte posibles fugas de dinero con reglas deterministas, para identificar gastos pequeños y repetitivos que podrían pasar desapercibidos.

**Objetivo y valor:** analizar los gastos propios con un conjunto aprobado de reglas explícitas y devolver posibles patrones de repetición, con evidencia suficiente para que el Usuario entienda el resultado. No es una predicción ni un juicio.

**Criterios de aceptación**

- **CA-23.1** — **Dado** que el Usuario autenticado tiene gastos que satisfacen una regla aprobada y versionada, **cuando** solicita el análisis, **entonces** el backend devuelve una o más posibles fugas con el identificador y la versión de la regla, el patrón afectado, el número de ocurrencias, el monto acumulado, la ventana temporal y las evidencias de los gastos que la activaron.
- **CA-23.2** — **Dado** un conjunto de gastos que no satisface ninguna regla, **cuando** se ejecuta el análisis, **entonces** el sistema no inventa fugas y muestra un estado de «sin posibles fugas» para el periodo o conjunto evaluado.
- **CA-23.3** — **Dado** que no se cumple la condición mínima de datos aprobada, **cuando** el Usuario solicita el análisis, **entonces** el sistema informa que aún no hay datos suficientes y no presenta candidatos.
- **CA-23.4** — **Dado** el mismo conjunto de gastos y la misma versión de reglas, **cuando** se repite el análisis, **entonces** el resultado es determinista y equivalente; no interviene un modelo de IA, aprendizaje automático ni una predicción.
- **CA-23.5 (diferido a HU-16)** — **Dado** que el Usuario edita o elimina un gasto que formaba parte de una posible fuga, **cuando** se vuelve a calcular el análisis, **entonces** el resultado se actualiza y la fuga que ya no cumple la regla deja de presentarse como vigente.
- **CA-23.6** — **Dado** que un Administrador intenta obtener las fugas o los gastos individuales de un Usuario, **cuando** accede a las rutas correspondientes, **entonces** el backend lo rechaza; el Administrador solo dispone de agregados según HU-30.
- **CA-23.7** — **Dado** que el análisis se muestra en la aplicación, **cuando** el Usuario lee el resultado, **entonces** el texto lo presenta como «posible fuga» y explica la regla aplicada, sin afirmar que el Usuario derrocha ni que la fuga es segura.

**Alcance del criterio diferido:** este criterio no forma parte de la verificación del MVP. Hasta que HU-16 esté implementada no existen ediciones ni eliminaciones posteriores al guardado; en el MVP el análisis se actualiza al crear gastos.

**Reglas de negocio, validaciones y errores**

- El análisis se ejecuta únicamente sobre gastos vigentes del propietario; no se mezclan cuentas.
- Las reglas son deterministas y explicables. Cada regla debe tener identificador, descripción, parámetros, versión y fecha de vigencia.
- **No se definen en este documento umbrales, montos mínimos, frecuencias, ventanas ni cantidad mínima de datos.** Todos son decisiones pendientes (D-01) y deben aprobarse antes de implementar.
- La agrupación por categoría, descripción normalizada o ambas es una decisión pendiente (D-01). No se asume una regla no aprobada.
- El resultado es una lista de candidatos, no una afirmación de pérdida real. La interfaz debe usar lenguaje probabilístico y no culpabilizante.
- El cálculo puede ejecutarse al solicitar el análisis o mediante un proceso programado; la estrategia está pendiente. En cualquier caso, debe ser reproducible y no dejar resultados obsoletos.
- Se debe controlar el costo de ejecución para no recorrer todos los gastos de todos los Usuarios en una sola consulta; el análisis se limita al propietario.
- Respuestas esperadas: 200 con candidatos o estado sin datos, 400 por periodo inválido, 401 sin sesión, 403 por acceso administrativo indebido, 5xx sin detalles internos.

**Dependencias**

- HU-13 (gastos persistidos).
- HU-16 (no bloqueante en el MVP; actualiza el análisis tras edición o eliminación cuando esté implementada).
- Reglas y parámetros aprobados (D-01).
- HU-33 (privacidad y aislamiento).
- Habilita HU-24, HU-25, HU-26 y HU-27.

**Pruebas sugeridas**

- Pruebas con conjuntos construidos a partir de los parámetros aprobados: justo por debajo, en el límite y por encima de cada umbral.
- Prueba de determinismo: misma entrada y versión, mismo resultado.
- Prueba de datos insuficientes y de ausencia de candidatos.
- Prueba de que no existen llamadas a IA externa ni modelos de aprendizaje.
- Prueba de actualización tras editar o eliminar un gasto.
- Prueba de seguridad: otro Usuario no recibe el análisis; el Administrador no accede al detalle.
- Revisión del texto para evitar juicios o promesas.

**Ambigüedades y decisiones pendientes**

- Umbrales, monto mínimo, frecuencia, ventana temporal, cantidad mínima de datos y agrupación (D-01).
- ¿El análisis se calcula al abrir la pantalla, al guardar un gasto o mediante un proceso programado? No está definido.
- ¿Cómo se tratan las descripciones equivalentes con errores de escritura o sinónimos? Depende del diccionario y de D-01/D-05.
- ¿Se analizan todos los gastos o solo los de un periodo? Debe definirse.
- ¿Qué ocurre con monedas distintas si el producto las admite? Debe definirse en D-03/D-01.

**Trazabilidad:** se conserva el propósito original «detectar posibles fugas mediante reglas deterministas»; se precisa la evidencia, el versionado, la ausencia de IA y la necesidad de aprobar los umbrales. Sin cambio funcional.

#### HU-24 — Consultar la evidencia de una posible fuga de dinero

**Módulo:** 6 · Detección de fugas de dinero  
**Prioridad:** **Must Have.** Una detección sin evidencia no es confiable ni accionable. El Usuario debe poder entender qué gastos activaron la regla y cuánto suman.  
**MVP:** Sí.

> **Historia:** Como Usuario, quiero ver la evidencia de cada posible fuga, para entender por qué el sistema la identificó y decidir si me interesa revisarla.

**Objetivo y valor:** hacer explicable y auditable el resultado, mostrando la regla, las ocurrencias, el acumulado y los gastos que sustentan la posible fuga, siempre dentro de la cuenta del Usuario.

**Criterios de aceptación**

- **CA-24.1** — **Dado** que existe una posible fuga, **cuando** el Usuario abre su detalle, **entonces** ve el nombre o la descripción de la regla aplicada, su versión, el número de ocurrencias, el monto acumulado y el rango de fechas en que se detectó.
- **CA-24.2** — **Dado** el detalle de la evidencia, **cuando** el Usuario revisa la lista de gastos que activaron la regla, **entonces** cada elemento muestra fecha, descripción y monto, y la suma de esos montos coincide con el acumulado informado.
- **CA-24.3 (diferido a HU-16)** — **Dado** que un gasto de la evidencia se edita o elimina, **cuando** se recalcula la fuga, **entonces** la evidencia, el número de ocurrencias y el acumulado se actualizan o la fuga se marca como no vigente; no se muestran datos obsoletos.
- **CA-24.4** — **Dado** que el Usuario consulta la evidencia, **cuando** se revisan los datos, **entonces** solo aparecen sus gastos y nunca los de otra cuenta.
- **CA-24.5** — **Dado** que un Administrador intenta abrir la evidencia individual, **cuando** usa una ruta o un identificador de fuga, **entonces** el backend lo rechaza y no devuelve gastos ni montos identificables.
- **CA-24.6** — **Dado** que se muestra la evidencia, **cuando** el Usuario la lee, **entonces** la interfaz explica la regla en lenguaje comprensible y no presenta la fuga como una pérdida confirmada ni como una crítica a sus hábitos.

**Alcance del criterio diferido:** este criterio no forma parte de la verificación del MVP. La actualización de la evidencia tras editar o eliminar un gasto se prueba cuando HU-16 esté implementada.

**Reglas de negocio, validaciones y errores**

- La evidencia debe ser consistente con el cálculo: ocurrencias, suma y rango de fechas deben corresponder a los gastos mostrados.
- Solo se incluyen gastos vigentes del propietario; los eliminados no aparecen.
- La evidencia puede mostrar los gastos individuales al propietario, pero no a un administrador ni a terceros.
- La versión de la regla y la fecha de cálculo deben conservarse para explicar cambios futuros.
- Si la fuga deja de cumplir la regla, debe desaparecer o marcarse como no vigente; no se mantiene como si siguiera activa.
- Respuestas esperadas: 200 con evidencia, 401 sin sesión, 403/404 por acceso ajeno o administrativo indebido, 410 si la fuga dejó de ser vigente y se consulta por identificador histórico.

**Dependencias**

- HU-23 (detección y reglas).
- HU-14 (detalle de gastos propios).
- HU-16 (no bloqueante en el MVP; actualiza la evidencia tras edición o eliminación cuando esté implementada).
- HU-33 (privacidad).

**Pruebas sugeridas**

- Prueba de consistencia entre gastos listados, ocurrencias y suma acumulada.
- Prueba de actualización tras editar o eliminar un gasto de la evidencia.
- Prueba de autorización para otro Usuario y para Administrador.
- Prueba de fuga no vigente y de identificador histórico.
- Revisión del texto explicativo y de la ausencia de juicios.

**Ambigüedades y decisiones pendientes**

- Nivel de detalle de la evidencia: ¿se listan todos los gastos o un resumen? La historia pide ocurrencias y acumulado; se recomienda listar los gastos propios.
- ¿Se permite exportar la evidencia? No está en el alcance.
- ¿Se conserva el historial de fugas anteriores? No está definido.
- ¿Cómo se explica una regla basada en descripción normalizada? Depende de D-01.

**Trazabilidad:** se conserva el propósito original «ver evidencia de una posible fuga, incluyendo ocurrencias y monto acumulado»; se precisan consistencia, actualización y autorización. Sin cambio funcional.

### 6.7 Módulo 7 — Alertas, recomendaciones y metas

#### HU-25 — Recibir alertas sobre posibles fugas de dinero

**Módulo:** 7 · Alertas, recomendaciones y metas  
**Prioridad:** **Could Have.** Las alertas añaden comodidad, pero la posible fuga ya puede consultarse en la aplicación. El alcance actual se limita a alertas dentro de la app y, como máximo, notificaciones locales; el push remoto requiere infraestructura adicional y queda postergado.  
**MVP:** No.

> **Historia:** Como Usuario, quiero recibir alertas sobre nuevas posibles fugas, para enterarme sin revisar manualmente el análisis.

**Objetivo y valor:** avisar de una posible fuga nueva o actualizada sin convertir la alerta en una afirmación de pérdida. La alerta debe respetar la privacidad, el permiso de notificaciones y las preferencias del Usuario.

**Criterios de aceptación**

- **CA-25.1** — **Dado** que el análisis detecta una posible fuga que el Usuario no había visto, **cuando** la aplicación está abierta, **entonces** muestra una alerta dentro de la app con una descripción breve, el número de ocurrencias, el monto acumulado y un acceso al detalle de la evidencia.
- **CA-25.2** — **Dado** que el Usuario concedió permiso para notificaciones locales, **cuando** se genera una alerta nueva, **entonces** la aplicación puede mostrar una notificación local; si el permiso fue denegado, la alerta dentro de la app sigue funcionando y no se bloquea el uso.
- **CA-25.3** — **Dado** que no existe una posible fuga nueva, **cuando** se evalúa el estado, **entonces** no se muestra ninguna alerta ni se genera una notificación vacía.
- **CA-25.4** — **Dado** que una misma posible fuga ya fue notificada para la misma versión de regla y evidencia, **cuando** se vuelve a evaluar, **entonces** no se repite la alerta de forma indiscriminada; el criterio exacto de novedad y recordatorio está pendiente (D-11).
- **CA-25.5** — **Dado** que el Usuario abre la alerta, **cuando** se navega al detalle, **entonces** llega a la evidencia de HU-24 correspondiente a su propia cuenta.
- **CA-25.6** — **Dado** el alcance actual, **cuando** se revisan los canales implementados, **entonces** no se envían notificaciones push remotas; si se implementan en el futuro, requieren consentimiento, token de dispositivo, credenciales y backend de envío (D-11).
- **CA-25.7** — **Dado** que la notificación local se muestra en la pantalla bloqueada, **cuando** se utiliza el contenido genérico aprobado, **entonces** no expone montos, descripciones ni otros datos financieros sensibles; la decisión de contenido está pendiente (D-11).

**Reglas de negocio, validaciones y errores**

- Las alertas se generan solo a partir de posibles fugas del propietario; nunca incluyen datos de otros Usuarios.
- Se distingue **alerta en la aplicación** de **notificación local** y de **notificación push**. El MVP de esta historia, si se implementa, usa las dos primeras.
- La notificación local requiere permiso del sistema; la denegación no debe impedir el uso de la aplicación.
- El contenido debe ser informativo y no culpabilizante; no se afirma que la fuga sea una pérdida real.
- El estado de leído, descartado o pospuesto debe conservarse si se implementa; su alcance está pendiente (D-11).
- No se envían montos o descripciones a un servicio de push sin una decisión explícita de privacidad.
- Errores esperados: permiso denegado, notificaciones deshabilitadas, fallo al programar la notificación local, alerta asociada a una fuga ya no vigente; todos deben tener una alternativa en la aplicación.

**Dependencias**

- HU-23 y HU-24 (detección y evidencia).
- Expo Notifications y configuración de notificaciones locales.
- Decisión D-11 sobre canales, contenido, frecuencia y preferencias.
- HU-33 (privacidad y datos en notificaciones).

**Pruebas sugeridas**

- Prueba de alerta en la app con y sin permiso de notificaciones.
- Prueba de no generar alerta cuando no hay fuga o cuando ya fue notificada.
- Prueba de navegación desde la alerta a la evidencia.
- Prueba de contenido genérico en pantalla bloqueada.
- Prueba de que no se envían datos a un servicio push en el alcance actual.
- Prueba de autorización y de ausencia de datos ajenos.

**Ambigüedades y decisiones pendientes**

- ¿Se admiten notificaciones push en una versión futura? Requieren Expo/EAS, credenciales FCM/APNs, tokens y backend (D-11).
- Frecuencia, horario de silencio, recordatorios y preferencias del Usuario (D-11).
- Contenido exacto de la alerta y si puede incluir montos en la pantalla bloqueada (D-11).
- ¿Cómo se define una fuga «nueva»: por identificador, por regla, por periodo o por evidencia? (D-01/D-11).
- ¿Se debe notificar cuando la fuga cambia de monto o desaparece? No está definido.

**Trazabilidad:** se conserva el propósito original «recibir alertas sobre posibles fugas»; se delimita el canal a alertas en la app y locales, y el push remoto queda como extensión futura de la misma historia, sin crear un identificador nuevo. Sin pérdida de funcionalidad.

#### HU-26 — Consultar sugerencias prácticas sobre posibles fugas

**Módulo:** 7 · Alertas, recomendaciones y metas  
**Prioridad:** **Could Have.** Las sugerencias pueden aportar valor, pero exigen contenido revisado, tono cuidadoso y evitar que se confundan con asesoría financiera. La detección y la evidencia ya permiten al Usuario decidir.  
**MVP:** No.

> **Historia:** Como Usuario, quiero ver sugerencias prácticas relacionadas con las posibles fugas, para considerar acciones concretas sin recibir asesoría financiera.

**Objetivo y valor:** acompañar la evidencia con ideas acotadas y no personalizadas, provenientes de un catálogo aprobado y asociadas a la regla o categoría detectada, sin juicios ni promesas de ahorro.

**Criterios de aceptación**

- **CA-26.1** — **Dado** que existe una posible fuga con sugerencias aprobadas en el catálogo, **cuando** el Usuario abre su detalle, **entonces** ve una o más sugerencias claramente etiquetadas como tales, relacionadas con la regla o la categoría de la fuga.
- **CA-26.2** — **Dado** que la regla o categoría no tiene una sugerencia aprobada, **cuando** el Usuario abre el detalle, **entonces** la fuga y su evidencia siguen visibles y no se genera una sugerencia improvisada.
- **CA-26.3** — **Dado** que el catálogo de sugerencias está definido y versionado, **cuando** se muestran, **entonces** el contenido es determinista y no se genera en tiempo de ejecución mediante IA.
- **CA-26.4** — **Dado** que el Usuario lee una sugerencia, **cuando** se revisa el texto, **entonces** no contiene juicios sobre sus hábitos, no promete un ahorro garantizado y no se presenta como asesoría financiera profesional.
- **CA-26.5** — **Dado** que la fuga deja de ser vigente, **cuando** el Usuario vuelve a consultar, **entonces** la sugerencia asociada deja de mostrarse o se marca como no vigente junto con la fuga.
- **CA-26.6** — **Dado** que un Usuario consulta una fuga ajena o un Administrador intenta ver la sugerencia individual, **cuando** accede, **entonces** el backend lo rechaza.

**Reglas de negocio, validaciones y errores**

- El catálogo de sugerencias debe estar aprobado, versionado y vinculado a reglas o categorías; no se inventa contenido en tiempo de ejecución.
- Las sugerencias no son asesoría financiera, no predicen resultados y no garantizan ahorros.
- El tono debe ser neutral, útil y no culpabilizante.
- Las sugerencias solo se muestran al propietario de la fuga.
- Si el catálogo no está disponible, la aplicación debe seguir mostrando la fuga y la evidencia sin sugerencias.
- Errores esperados: catálogo vacío, sugerencia no encontrada, fuga no vigente, acceso no autorizado; ninguno debe romper la vista de evidencia.

**Dependencias**

- HU-23 y HU-24 (fuga y evidencia).
- Catálogo de sugerencias aprobado y versionado.
- HU-33 (autorización).
- Decisiones D-01 y D-11 sobre reglas y contenido.

**Pruebas sugeridas**

- Prueba de correspondencia entre regla/categoría y sugerencia aprobada.
- Prueba sin sugerencia y con catálogo vacío.
- Prueba de actualización al desaparecer la fuga.
- Revisión de contenido para detectar juicios, promesas o lenguaje de asesoría.
- Prueba de autorización y privacidad.

**Ambigüedades y decisiones pendientes**

- Contenido, cantidad y tono de las sugerencias; quién las aprueba.
- ¿Se personalizan por monto, frecuencia o categoría? La propuesta es no personalizarlas en el MVP.
- ¿El Usuario puede descartar una sugerencia o marcar que no le interesa? No está definido.
- ¿Se requiere revisión legal o pedagógica del contenido? Debe decidirse.

**Trazabilidad:** se conserva el propósito original «ver sugerencias prácticas relacionadas con las fugas»; se precisa el catálogo, el tono y la prohibición de asesoría. Sin cambio funcional.

#### HU-27 — Consultar el resumen mensual de posibles fugas

**Módulo:** 7 · Alertas, recomendaciones y metas  
**Prioridad:** **Could Have.** El dashboard y el detalle de fugas ya ofrecen información suficiente. Un resumen mensual añade valor de consulta, pero no es necesario para el MVP y requiere definir cómo se asignan las fugas a cada mes.  
**MVP:** No.

> **Historia:** Como Usuario, quiero ver un resumen mensual de posibles fugas, para entender su acumulado en el mes.

**Objetivo y valor:** ofrecer una vista mensual agregada de las posibles fugas, con su monto acumulado y sus ocurrencias, sin duplicar gastos ni presentar la cifra como pérdida confirmada.

**Criterios de aceptación**

- **CA-27.1** — **Dado** que el Usuario selecciona un mes, **cuando** se calcula el resumen, **entonces** ve el monto acumulado de las posibles fugas vigentes de ese mes, la cantidad de posibles fugas y, si se muestra, el número de ocurrencias.
- **CA-27.2** — **Dado** un mes sin posibles fugas, **cuando** se abre el resumen, **entonces** se muestra un estado vacío o un valor cero explícito, sin inventar candidatos.
- **CA-27.3** — **Dado** que un gasto se edita o elimina, **cuando** se recalcula el resumen, **entonces** el monto y las ocurrencias se actualizan y no se conservan cifras obsoletas.
- **CA-27.4** — **Dado** que una fuga abarca gastos de más de un mes, **cuando** se calcula el resumen, **entonces** se aplica la regla de asignación aprobada (D-01/D-04) y no se cuenta un mismo gasto dos veces.
- **CA-27.5** — **Dado** que el Usuario consulta el resumen, **cuando** se revisan los datos, **entonces** solo aparecen sus gastos y no se mezclan cuentas.
- **CA-27.6** — **Dado** que se muestra el resumen, **cuando** el Usuario lee la cifra, **entonces** se identifica como suma de posibles fugas, no como pérdida comprobada ni como predicción.

**Reglas de negocio, validaciones y errores**

- El mes se define según la zona horaria y los límites aprobados (D-04).
- La asignación de una fuga a un mes y el tratamiento de ventanas que cruzan meses están pendientes (D-01). El resumen no puede duplicar el mismo gasto.
- Solo se incluyen fugas vigentes de gastos propios; los gastos eliminados no se cuentan.
- La versión de reglas debe registrarse para explicar cambios en el resumen.
- No se envían notificaciones push desde esta historia.
- Respuestas esperadas: 200 con resumen, 400 por mes inválido, 401 sin sesión, 5xx sin datos sensibles.

**Dependencias**

- HU-23 y HU-24 (detección y evidencia).
- HU-16 para la actualización tras cambios.
- Decisiones D-01 y D-04 sobre ventanas y meses.

**Pruebas sugeridas**

- Prueba con fugas de un solo mes y con ventanas que cruzan meses.
- Prueba de mes vacío y de actualización tras editar o eliminar.
- Prueba de no duplicación de gastos.
- Prueba de autorización y privacidad.
- Revisión del texto para no presentar la cifra como pérdida confirmada.

**Ambigüedades y decisiones pendientes**

- ¿Cómo se asigna una fuga con ventana de varios meses? (D-01).
- ¿El resumen muestra cantidad de fugas, ocurrencias o ambas?
- ¿Se compara con el mes anterior? No está en la historia.
- ¿Se incluye un detalle navegable por fuga? Se recomienda, pero no está definido.
- ¿Se genera un resumen mensual automático o solo bajo demanda? No está definido.

**Trazabilidad:** se conserva el propósito original «ver un resumen mensual de posibles fugas»; se precisan asignación mensual, no duplicación y actualización. Sin cambio funcional.

#### HU-28 — Definir una meta mensual de gasto o ahorro con alcance explícito

**Módulo:** 7 · Alertas, recomendaciones y metas  
**Prioridad:** **Won't Have (for now).** La historia no especifica si la meta es de gasto o de ahorro, qué gastos cuenta, cómo se mide el ahorro ni si existe información de ingresos. Una meta de ahorro requeriría datos que hoy no forman parte del alcance. Se posterga para no inventar reglas ni prometer una función incompleta.  
**MVP:** No.

> **Historia:** Como Usuario, quiero definir una meta mensual de gasto o ahorro con alcance explícito, para orientar mi seguimiento.

**Objetivo y valor futuro:** permitir que el Usuario fije un objetivo mensual con reglas claras y verificables, sin que el sistema le imponga una interpretación de «ahorro» o de «gasto» que no haya sido definida.

**Criterios de aceptación (para una versión futura, no para el MVP)**

- **CA-28.1** — **Dado** que el Usuario autenticado abre la creación de meta, **cuando** la pantalla carga, **entonces** debe elegir explícitamente el tipo de meta —límite de gasto o meta de ahorro—, el periodo mensual, el monto y la moneda.
- **CA-28.2** — **Dado** que el tipo de meta es límite de gasto, **cuando** el Usuario guarda una meta válida, **entonces** debe quedar definido qué gastos se incluyen y si se consideran todos o solo determinadas categorías.
- **CA-28.3** — **Dado** que el tipo de meta es ahorro, **cuando** el Usuario intenta guardarla, **entonces** el sistema solo debe permitirlo si existe una fuente de ingresos o una base de cálculo aprobada; mientras no exista, debe explicar que la meta de ahorro no está disponible.
- **CA-28.4** — **Dado** que el Usuario define monto cero, negativo, no numérico o fuera de los límites, **cuando** intenta guardar, **entonces** ve un error y no se crea la meta.
- **CA-28.5** — **Dado** que el Usuario ya tiene una meta activa para el mismo periodo y tipo, **cuando** intenta crear otra, **entonces** el sistema aplica la regla de unicidad que se apruebe (reemplazar, editar o rechazar) y no deja dos metas contradictorias.
- **CA-28.6** — **Dado** que el Usuario edita o elimina su meta, **cuando** confirma, **entonces** el cambio se persiste y solo afecta su cuenta; no se modifica el historial de gastos.
- **CA-28.7** — **Dado** que un Usuario intenta acceder a la meta de otra cuenta, **cuando** manipula el identificador, **entonces** el backend lo rechaza.

**Reglas de negocio, validaciones y errores**

- El tipo de meta, el periodo, el monto, la moneda, la fuente de cálculo y los gastos incluidos deben estar definidos antes de implementar.
- Una meta de ahorro no puede calcularse sin ingresos, presupuesto base o una definición equivalente; hoy no existe un módulo de ingresos en las 33 historias.
- Solo puede existir una meta activa por Usuario, periodo y tipo, salvo que se apruebe otra regla.
- La meta pertenece al Usuario y no se comparte con administradores ni con otros Usuarios.
- Errores esperados: 400 por validación, 401 sin sesión, 403/404 por acceso ajeno, 409 por conflicto de meta existente, 422 si el tipo de meta no es calculable.

**Dependencias**

- HU-02 (Usuario).
- HU-13 (gastos para calcular el avance).
- HU-20 y HU-21 (métricas del periodo).
- Decisión D-08 sobre tipo, alcance, ingresos y unicidad.
- Decisión D-03 sobre moneda y límites.

**Pruebas sugeridas (futuras)**

- Prueba de creación de meta de gasto y de meta de ahorro con y sin fuente de ingresos.
- Prueba de validaciones y de unicidad.
- Prueba de autorización y de persistencia.
- Prueba de edición y eliminación.
- Revisión de que la meta no se presenta como asesoría financiera.

**Ambigüedades y decisiones pendientes**

- ¿La meta es de gasto, de ahorro o ambas? (D-08).
- Si es de ahorro, ¿cómo se calcula sin ingresos? ¿Se añadirá un módulo de ingresos?
- ¿Qué gastos cuentan: todos, algunas categorías o todos menos ciertas categorías?
- ¿La meta se define por mes calendario o por un periodo personalizado?
- ¿Se permite una sola meta activa? ¿Se puede editar o solo reemplazar?
- ¿Se notifica al Usuario cuando se acerca o supera la meta? No está definido.

**Trazabilidad:** se conserva la funcionalidad original de «definir una meta mensual de gasto o ahorro con alcance explícito». Se posterga explícitamente por ambigüedad de alcance y ausencia de datos de ingresos. No se elimina del backlog.

#### HU-29 — Consultar el avance hacia la meta definida

**Módulo:** 7 · Alertas, recomendaciones y metas  
**Prioridad:** **Won't Have (for now).** Depende de HU-28 y de una definición de meta que aún no existe. Implementarla antes sería construir una vista sobre una regla indefinida.  
**MVP:** No.

> **Historia:** Como Usuario, quiero consultar el avance hacia mi meta, para saber si voy dentro del límite o si debo ajustar.

**Objetivo y valor futuro:** mostrar el progreso de forma descriptiva, con el monto consumido o ahorrado, el restante y el porcentaje, sin emitir juicios ni recomendaciones financieras.

**Criterios de aceptación (para una versión futura, no para el MVP)**

- **CA-29.1** — **Dado** que el Usuario tiene una meta activa, **cuando** abre su avance, **entonces** ve el tipo de meta, el periodo, el monto objetivo, el valor acumulado, el restante o excedido y el porcentaje de avance, según la definición aprobada.
- **CA-29.2** — **Dado** que el Usuario no tiene una meta activa, **cuando** abre la sección, **entonces** ve un estado vacío con la opción de crear una meta, sin inventar valores.
- **CA-29.3** — **Dado** que el Usuario registra, edita o elimina un gasto, **cuando** vuelve al avance, **entonces** los valores se recalculan y reflejan los datos vigentes.
- **CA-29.4** — **Dado** que la meta es de ahorro y no existe una base de cálculo aprobada, **cuando** se consulta el avance, **entonces** el sistema informa que no es calculable y no muestra un porcentaje ficticio.
- **CA-29.5** — **Dado** que el Usuario supera el límite o no alcanza la meta, **cuando** se muestra el resultado, **entonces** la interfaz lo comunica de forma neutral, sin juicios ni predicciones.
- **CA-29.6** — **Dado** que un Usuario intenta ver el avance de otra cuenta, **cuando** manipula el identificador, **entonces** el backend lo rechaza.

**Reglas de negocio, validaciones y errores**

- El cálculo depende enteramente de la definición de HU-28 y debe documentarse antes de implementar.
- El avance se calcula con gastos vigentes del propietario y con el periodo de la meta.
- No se muestran porcentajes cuando el denominador es cero o la meta no es calculable.
- No se generan recomendaciones, predicciones ni afirmaciones sobre la capacidad de ahorro del Usuario.
- Solo el propietario puede consultar su avance.
- Errores esperados: 400 por meta o periodo inválido, 401 sin sesión, 403/404 por acceso ajeno, 409 si la meta no está definida, 422 si no es calculable.

**Dependencias**

- HU-28 (meta definida).
- HU-20 y HU-21 (métricas del periodo).
- HU-16 (actualización tras cambios).
- Decisión D-08.

**Pruebas sugeridas (futuras)**

- Prueba de avance con meta de gasto y con meta de ahorro.
- Prueba sin meta, con meta vencida y con denominador cero.
- Prueba de actualización tras crear, editar o eliminar gastos.
- Prueba de autorización.
- Revisión del tono neutral del resultado.

**Ambigüedades y decisiones pendientes**

- Fórmula de avance para gasto y para ahorro (D-08).
- ¿El avance se reinicia cada mes o se acumula?
- ¿Se muestran alertas al acercarse a la meta? No está definido.
- ¿Se puede consultar el avance de meses anteriores? No está definido.
- ¿Cómo se trata un gasto que pertenece a otro periodo? Debe definirse.

**Trazabilidad:** se conserva la funcionalidad original de «seguir el avance de la meta». Se posterga junto con HU-28 por dependencia y falta de definición. No se elimina del backlog.

### 6.8 Módulo 8 — Administración y privacidad

#### HU-30 — Consultar estadísticas agregadas de uso sin acceder a gastos individuales

**Módulo:** 8 · Administración y privacidad  
**Prioridad:** **Should Have.** El rol Administrador debe existir y la privacidad debe respetarse, pero el panel agregado no forma parte del flujo principal de valor del MVP. Es importante para la operación y puede implementarse después de los Must.  
**MVP:** No.

> **Historia:** Como Administrador, quiero consultar estadísticas agregadas de uso, para supervisar la aplicación sin acceder a gastos individuales.

**Objetivo y valor:** ofrecer una visión global del uso —usuarios y gastos— sin permitir identificar a una persona ni reconstruir sus gastos. La agregación debe proteger la privacidad incluso frente al propio Administrador.

**Criterios de aceptación**

- **CA-30.1** — **Dado** que un Administrador autenticado abre el panel, **cuando** la consulta finaliza, **entonces** ve métricas agregadas aprobadas, como total de usuarios registrados, usuarios activos o inactivos, total de gastos registrados y distribución agregada por categoría, con la fecha o el periodo de actualización.
- **CA-30.2** — **Dado** el panel agregado, **cuando** el Administrador intenta abrir un gasto, una descripción, un monto individual o el detalle de un Usuario, **entonces** no existe una acción que lo permita y cualquier llamada directa a una ruta de gastos individuales es rechazada por el backend.
- **CA-30.3** — **Dado** que un grupo de datos es demasiado pequeño y podría permitir identificar a una persona, **cuando** se calcula una métrica, **entonces** se aplica la regla de agregación mínima aprobada (D-07) y se suprime o agrupa la información.
- **CA-30.4** — **Dado** que un Usuario sin rol Administrador intenta abrir el panel o llamar a su API, **cuando** se procesa la solicitud, **entonces** recibe 403 y no obtiene métricas.
- **CA-30.5** — **Dado** que el Administrador aplica un filtro, **cuando** intenta aislar a un único Usuario o un gasto individual, **entonces** el sistema no ofrece ese filtro o lo rechaza; las métricas solo se presentan en el nivel agregado aprobado.
- **CA-30.6** — **Dado** que se accede al panel, **cuando** se registra la operación, **entonces** queda una auditoría del acceso administrativo sin incluir montos, descripciones ni datos financieros individuales.

**Reglas de negocio, validaciones y errores**

- El rol se valida en el backend con la identidad vigente; no se confía únicamente en un rol incluido en el token si puede estar desactualizado.
- Las consultas administrativas usan agregaciones y no devuelven documentos individuales de gastos.
- La agregación mínima y las métricas exactas están pendientes (D-07). No se inventa un umbral de anonimización.
- Los filtros no pueden aislar a un Usuario ni a un gasto; no se ofrece búsqueda por identificador de gasto.
- Los datos personales se minimizan: el panel no necesita nombres, teléfonos, correos ni descripciones de gastos.
- Los logs administrativos no deben contener información financiera individual.
- Respuestas esperadas: 200 con métricas agregadas, 401 sin sesión, 403 sin rol, 400 por filtro inválido, 5xx sin datos sensibles.

**Dependencias**

- HU-02 (usuarios y roles).
- HU-13 (datos de gastos para agregar).
- HU-33 (privacidad y autorización).
- Decisión D-07 sobre métricas, umbral de agregación y filtros.

**Pruebas sugeridas**

- Prueba de acceso con rol Administrador y con rol Usuario.
- Prueba de que la respuesta solo contiene métricas agregadas y ningún gasto individual.
- Prueba de grupo pequeño y regla de supresión.
- Prueba de filtros que intentan aislar a un Usuario.
- Prueba de auditoría y de ausencia de datos sensibles en logs.
- Prueba de que un Administrador no puede llamar a endpoints de gastos individuales.

**Ambigüedades y decisiones pendientes**

- Métricas exactas del panel y periodo de análisis (D-07).
- Umbral mínimo de agregación para evitar reidentificación (D-07).
- ¿Se permite exportar estadísticas? No está definido y requeriría controles adicionales.
- ¿Con qué frecuencia se actualizan las métricas?
- ¿Se muestran usuarios activos por periodo o solo el estado actual?

**Trazabilidad:** se conserva el propósito original «ver estadísticas agregadas sin acceder a gastos individuales»; se precisan métricas, agregación mínima y controles de acceso. Sin cambio funcional.

#### HU-31 — Consultar usuarios registrados y la información administrativa necesaria

**Módulo:** 8 · Administración y privacidad  
**Prioridad:** **Should Have.** Es necesaria para gestionar cuentas y aplicar HU-32, pero el MVP puede operar sin un panel de usuarios. Debe implementarse con minimización de datos y sin acceso a gastos.  
**MVP:** No.

> **Historia:** Como Administrador, quiero consultar los usuarios registrados y la información administrativa necesaria, para gestionar sus cuentas.

**Objetivo y valor:** permitir la localización y revisión del estado de las cuentas para tareas administrativas, sin convertir al Administrador en un observador de la vida financiera de los Usuarios.

**Criterios de aceptación**

- **CA-31.1** — **Dado** que un Administrador autenticado abre la gestión de usuarios, **cuando** la lista carga, **entonces** ve una lista paginada con los campos administrativos aprobados, como identificador, nombre visible, correo, rol, estado y fecha de registro, sin gastos ni montos.
- **CA-31.2** — **Dado** que la lista está paginada, **cuando** el Administrador navega, **entonces** no se repiten ni se omiten usuarios y puede localizar una cuenta mediante los criterios de búsqueda aprobados (D-14).
- **CA-31.3** — **Dado** que un Usuario sin rol Administrador intenta consultar la lista, **cuando** llama a la API, **entonces** recibe 403 y no obtiene datos de otras cuentas.
- **CA-31.4** — **Dado** que el Administrador consulta un Usuario, **cuando** revisa su información, **entonces** no puede ver sus gastos, descripciones, montos, estadísticas individuales ni posibles fugas.
- **CA-31.5** — **Dado** que se muestran datos personales, **cuando** se revisa la respuesta, **entonces** solo aparecen los campos necesarios para la gestión y no se incluyen datos de perfil no requeridos ni información financiera.
- **CA-31.6** — **Dado** que el Administrador intenta acceder a la lista mediante un rol manipulado en el cliente, **cuando** el backend procesa la solicitud, **entonces** valida el rol real y rechaza el acceso si no corresponde.

**Reglas de negocio, validaciones y errores**

- La lista se limita a información administrativa; no incluye gastos ni agregados por Usuario que permitan reconstruir su comportamiento.
- El acceso se valida en el backend; no se confía en la interfaz.
- Los campos exactos, la búsqueda, el orden y la paginación están pendientes (D-14).
- Los datos personales se minimizan y se protegen en logs y exportaciones.
- No se permite modificar datos financieros desde esta vista.
- Respuestas esperadas: 200 con página, 401 sin sesión, 403 sin rol, 400 por filtro inválido, 5xx sin datos sensibles.

**Dependencias**

- HU-02 (cuentas y roles).
- HU-30 (panel administrativo y criterios de privacidad).
- HU-33 (autorización).
- Decisión D-14 sobre campos y búsqueda.

**Pruebas sugeridas**

- Prueba de acceso con y sin rol Administrador.
- Prueba de paginación y búsqueda.
- Prueba de que la respuesta no contiene gastos, montos, descripciones ni fugas.
- Prueba de minimización de datos y de logs.
- Prueba de manipulación de rol desde el cliente.

**Ambigüedades y decisiones pendientes**

- Campos exactos que necesita la administración (D-14).
- ¿Se permite buscar por correo, nombre o identificador? ¿Se permite exportar? (D-14).
- ¿Se muestra la última sesión o la fecha de desactivación?
- ¿Se pueden eliminar cuentas desde esta vista? No está en el alcance; la desactivación es HU-32.

**Trazabilidad:** se conserva el propósito original «ver usuarios registrados y la información administrativa necesaria»; se precisan campos, minimización y prohibición de acceso a gastos. Sin cambio funcional.

#### HU-32 — Activar o desactivar cuentas de usuario desde funciones administrativas autorizadas

**Módulo:** 8 · Administración y privacidad  
**Prioridad:** **Should Have.** Es una capacidad administrativa relevante para responder ante cuentas indebidas y para aplicar el estado de cuenta. No es necesaria para demostrar el valor principal, pero debe existir antes de operar con usuarios reales.  
**MVP:** No.

> **Historia:** Como Administrador, quiero activar o desactivar cuentas de usuario, para atender cuentas indebidas o suspender el acceso cuando corresponda.

**Objetivo y valor:** permitir la suspensión y reactivación controlada de cuentas, asegurando que una cuenta desactivada no pueda operar y que la acción quede auditada, sin que el Administrador acceda a los gastos.

**Criterios de aceptación**

- **CA-32.1** — **Dado** que un Administrador autenticado selecciona una cuenta activa, **cuando** confirma la desactivación, **entonces** la cuenta queda inactiva, se invalidan sus sesiones o tokens de renovación según la política y el Usuario no puede iniciar sesión ni realizar operaciones protegidas.
- **CA-32.2** — **Dado** que una cuenta está inactiva, **cuando** el Administrador confirma la reactivación, **entonces** la cuenta vuelve a estado activo y el Usuario puede iniciar sesión, conservando sus datos según D-06.
- **CA-32.3** — **Dado** que el Usuario afectado tenía una sesión abierta, **cuando** intenta realizar una nueva operación después de la desactivación, **entonces** el backend la rechaza y la aplicación lo redirige al inicio de sesión con un mensaje general.
- **CA-32.4** — **Dado** que el Administrador intenta desactivar su propia cuenta, **cuando** envía la solicitud, **entonces** el sistema la rechaza para evitar la pérdida de acceso administrativo.
- **CA-32.5** — **Dado** que un Usuario sin rol Administrador intenta desactivar o reactivar una cuenta, **cuando** llama a la API, **entonces** recibe 403 y la cuenta no cambia.
- **CA-32.6** — **Dado** que se desactiva o reactiva una cuenta, **cuando** termina la operación, **entonces** se registra una auditoría con administrador, cuenta afectada, acción, fecha y motivo si se solicita; la auditoría no incluye gastos ni montos.
- **CA-32.7** — **Dado** que la cuenta ya está en el estado solicitado, **cuando** se repite la operación, **entonces** el sistema responde de forma idempotente o con un mensaje claro, sin efectos duplicados.

**Reglas de negocio, validaciones y errores**

- Solo un Administrador autorizado puede cambiar el estado de una cuenta.
- La desactivación administrativa se distingue de la desactivación por el propio Usuario (HU-06).
- El backend debe comprobar el estado de la cuenta en cada operación protegida o invalidar la sesión; no basta con ocultar opciones en la app.
- No se puede desactivar la propia cuenta. La regla sobre desactivar a otros administradores o al último administrador está pendiente (D-14).
- La desactivación no elimina gastos automáticamente; la retención depende de D-06.
- El motivo es opcional o obligatorio según D-14; la auditoría es recomendable en todos los casos.
- Respuestas esperadas: 200 al cambiar, 400 por solicitud inválida, 401 sin sesión, 403 sin rol o por intento de auto-desactivación, 404 si la cuenta no existe, 409 si hay conflicto, 5xx sin datos sensibles.

**Dependencias**

- HU-02 (cuentas y sesiones).
- HU-31 (lista y selección de usuarios).
- HU-33 (autorización y privacidad).
- Decisiones D-09, D-14 y D-06.

**Pruebas sugeridas**

- Prueba de desactivación y bloqueo de inicio de sesión.
- Prueba de bloqueo de una sesión ya abierta.
- Prueba de reactivación y recuperación de acceso.
- Prueba de auto-desactivación y de acceso sin rol.
- Prueba de idempotencia y de auditoría.
- Prueba de que el Administrador no puede ver gastos durante la operación.

**Ambigüedades y decisiones pendientes**

- ¿Puede un Administrador desactivar a otro Administrador? ¿Se protege al último administrador activo? (D-14).
- ¿El motivo de la desactivación es obligatorio? ¿Se notifica al Usuario? (D-11/D-14).
- ¿El Usuario puede solicitar la reactivación o debe hacerlo un Administrador? (D-06).
- ¿Cuánto tiempo se conserva la auditoría? (D-14).
- ¿La desactivación invalida todos los dispositivos de inmediato o al vencer el token? (D-09).

**Trazabilidad:** se conserva el propósito original «activar o desactivar cuentas mediante funciones administrativas autorizadas»; se precisan revocación de sesión, auto-protección, auditoría y errores. Sin cambio funcional.

#### HU-33 — Proteger la privacidad de los gastos y garantizar el aislamiento entre usuarios

**Módulo:** 8 · Administración y privacidad  
**Prioridad:** **Must Have.** Es una restricción de seguridad y confianza, no una función opcional. Si un Usuario puede ver o modificar gastos de otro, el producto no es aceptable. Debe implementarse desde la primera historia que maneja datos y verificarse en todas las demás.  
**MVP:** Sí.

> **Historia:** Como Usuario, quiero que el backend impida que otras personas accedan a mis gastos, para que mi privacidad no dependa de la interfaz.

**Objetivo y valor:** garantizar el aislamiento de datos por propietario y por rol, de modo que ni otro Usuario ni un Administrador puedan leer, modificar o eliminar gastos individuales ajenos. La privacidad debe aplicarse en el servidor y en cada consulta.

**Criterios de aceptación**

- **CA-33.1** — **Dado** que el Usuario A tiene un gasto y el Usuario B conoce su identificador, **cuando** B intenta consultarlo, editarlo o eliminarlo por cualquier ruta, **entonces** el backend responde con 404 o 403 y no devuelve monto, categoría, descripción, fecha, texto original ni ninguna indicación que confirme la existencia del recurso.
- **CA-33.2** — **Dado** que una solicitud incluye un identificador de propietario distinto al de la sesión, **cuando** el backend la procesa, **entonces** ignora o rechaza el valor y solo opera sobre la identidad verificada; no existe forma de cambiar de propietario mediante parámetros, cuerpo o encabezados controlados por el cliente.
- **CA-33.3** — **Dado** un Administrador autenticado, **cuando** intenta acceder a un gasto individual, a una descripción, a un monto o a una posible fuga de un Usuario, **entonces** el backend lo rechaza; solo puede usar las vistas agregadas de HU-30, sin posibilidad de reconstruir datos individuales.
- **CA-33.4** — **Dado** cualquier endpoint protegido, **cuando** se llama sin token, con token inválido, vencido o de una cuenta inactiva, **entonces** responde 401 o 403 y no ejecuta la operación.
- **CA-33.5** — **Dado** que se ejecuta la suite de seguridad, **cuando** se prueban referencias directas a objetos, escalamiento de rol, asignación masiva de campos y manipulación de identificadores, **entonces** todas las pruebas de acceso cruzado fallan de forma segura y no filtran datos.
- **CA-33.6** — **Dado** que se revisan logs, respuestas de error, telemetría y almacenamiento del cliente, **cuando** se buscan datos sensibles, **entonces** no aparecen contraseñas, tokens, montos, descripciones ni textos de gastos en claro.
- **CA-33.7** — **Dado** que un Administrador consulta estadísticas, **cuando** el grupo de datos es demasiado pequeño, **entonces** se aplica la regla de agregación mínima aprobada (D-07) y no se permite identificar a una persona.
- **CA-33.8** — **Dado** que un Usuario edita o elimina un gasto, **cuando** se recalculan los agregados, **entonces** los cambios solo afectan sus propios resultados y no alteran los de otra cuenta.

**Reglas de negocio, validaciones y errores**

- El propietario se deriva siempre de la sesión verificada. No se acepta `user_id`, `owner_id` ni equivalentes enviados por el cliente para decidir el alcance de una consulta.
- El control de acceso se aplica en el backend y en la capa de acceso a datos; no basta con ocultar botones en la interfaz.
- Se aplica el principio de mínimo privilegio: Usuario solo sus datos; Administrador solo agregados y gestión de cuentas; Visitante solo información pública.
- Los errores no deben revelar la existencia de recursos ajenos; se prefiere 404 cuando corresponda.
- Los logs y la telemetría deben redactar tokens, contraseñas y datos financieros. Las contraseñas se almacenan con hash y sal.
- La comunicación usa TLS. Los secretos no se incluyen en la app ni en el repositorio.
- Las imágenes de perfil en Cloudinary no deben contener datos de gastos; el acceso a los gastos no depende de Cloudinary.
- La retención, el borrado y los respaldos deben seguir la política aprobada (D-06). La privacidad no termina en la interfaz.
- La suite de seguridad debe ejecutarse en cada entrega y antes de la demostración.
- Respuestas esperadas: 401 sin sesión, 403 por rol insuficiente, 404 por recurso ajeno o inexistente, 400 por datos inválidos, 5xx sin detalles internos.

**Dependencias**

- HU-02 (identidad, sesión y roles).
- HU-13 (propiedad del gasto) y todas las historias que leen o modifican gastos.
- HU-30 a HU-32 para verificar que el Administrador no accede a datos individuales.
- Decisiones D-06, D-07 y D-09 sobre retención, agregación y sesiones.

**Pruebas sugeridas**

- Suite automatizada de acceso cruzado entre dos Usuarios para cada endpoint de gastos.
- Prueba de referencias directas a objetos (IDOR/BOLA) y de escalamiento de rol.
- Prueba de asignación masiva de campos, incluidos propietario y rol.
- Prueba de token ausente, inválido, vencido y de cuenta inactiva.
- Prueba de que las respuestas administrativas solo contienen agregados.
- Revisión de logs, mensajes de error, telemetría y almacenamiento seguro del cliente.
- Prueba de regresión después de editar o eliminar gastos.

**Ambigüedades y decisiones pendientes**

- Política de retención, eliminación y respaldos (D-06).
- Umbral de agregación administrativa (D-07).
- Duración, renovación y revocación de sesiones (D-09).
- ¿Se requiere cifrado adicional a nivel de campo, además del cifrado del proveedor de base de datos? Debe decidirse.
- ¿Se necesita un registro de auditoría de accesos a datos personales? (D-14).
- ¿Cómo se manejan solicitudes legales de acceso a datos? No está definido.

**Trazabilidad:** se conserva el propósito original «proteger la privacidad de los gastos y garantizar la separación de datos entre usuarios»; se eleva a restricción transversal verificable y se conecta con todas las historias que manejan gastos. Sin cambio funcional.

---

## 7. Matriz de dependencias entre historias

La matriz se presenta como una lista de precedencias para mantenerla legible. Cada fila indica qué historias deben existir, al menos en su parte funcional, antes de completar la historia de la columna izquierda. HU-33 es una restricción transversal: se implementa desde el inicio y se verifica con las historias que manipulan datos, por lo que no debe interpretarse como una pantalla que se construye al final.

| ID | Depende de | Tipo principal | Nota |
|---|---|---|---|
| HU-01 | — | Funcional | Punto de entrada; no requiere sesión. |
| HU-02 | HU-01 | Seguridad / identidad | Implementa las bases de autorización que exige HU-33. |
| HU-03 | HU-02 | Técnico / seguridad | Requiere configuración OAuth y verificación de tokens. |
| HU-04 | HU-02 | Seguridad | Cierra la sesión creada por HU-02 o HU-03. |
| HU-05 | HU-02 | Técnico | Requiere correo transaccional y tokens de recuperación. |
| HU-06 | HU-02, HU-04 | Funcional / seguridad | Requiere política de retención (D-06). |
| HU-07 | HU-02 | Funcional | Perfil asociado a la identidad. |
| HU-08 | HU-07 | Técnico | Requiere Cloudinary y validación de archivos. |
| HU-09 | HU-03, HU-07, HU-08 | Funcional / técnico | Depende de Google y de la precedencia de imagen (D-13). |
| HU-10 | HU-02 | Funcional | Entrada de texto autenticada. |
| HU-11 | HU-10 | Funcional / técnico | Requiere diccionario y reglas deterministas. |
| HU-12 | HU-11 | Funcional | Revisión obligatoria antes de guardar. |
| HU-13 | HU-12, HU-33 | Datos / seguridad | Persistencia con propietario derivado de la sesión. |
| HU-14 | HU-13 | Funcional | Historial sobre gastos persistidos. |
| HU-15 | HU-14 | Funcional | Filtros sobre el historial. |
| HU-16 | HU-13, HU-14, HU-20, HU-21, HU-23 | Datos / funcional | Edición y borrado deben mantener coherentes los agregados. |
| HU-17 | HU-02, HU-10 | Técnico | Android, permiso de micrófono y compilación con módulo nativo. |
| HU-18 | HU-17 | Técnico | `SpeechRecognizer` y puente Kotlin/React Native. |
| HU-19 | HU-11, HU-12, HU-17, HU-18 | Funcional | Flujo obligatorio de voz, revisión y guardado. |
| HU-20 | HU-13 | Funcional / datos | Agregación del periodo. |
| HU-21 | HU-13, HU-20 | Funcional / datos | Desglose por categoría sobre el periodo del dashboard. |
| HU-22 | HU-20, HU-21 | Funcional | Comparación de métricas ya calculadas. |
| HU-23 | HU-13, HU-33 | Datos / seguridad | Requiere reglas aprobadas y versionadas (D-01). |
| HU-24 | HU-14, HU-23 | Funcional | Evidencia navegable desde la detección. |
| HU-25 | HU-23, HU-24 | Técnico | Expo Notifications; alcance local y en la aplicación (D-11). |
| HU-26 | HU-23, HU-24 | Contenido / funcional | Requiere catálogo de sugerencias aprobado. |
| HU-27 | HU-23, HU-24 | Funcional | Requiere regla de asignación mensual (D-01/D-04). |
| HU-28 | HU-02, HU-13 | Funcional / producto | Alcance de meta pendiente (D-08). |
| HU-29 | HU-28, HU-20, HU-21, HU-16 | Funcional | Depende de una meta y de datos vigentes. |
| HU-30 | HU-02, HU-13, HU-33 | Administrativo / seguridad | Requiere rol y agregación mínima (D-07). |
| HU-31 | HU-02, HU-30, HU-33 | Administrativo | Lista de usuarios sin acceso a gastos. |
| HU-32 | HU-02, HU-31, HU-33 | Administrativo / seguridad | Requiere invalidación de sesiones (D-09). |
| HU-33 | HU-02 | Seguridad transversal | Se verifica con HU-13, HU-14, HU-16 y HU-30 a HU-32. |

### 7.1 Reglas de lectura

- Una historia no se considera terminada si una predecesora solo existe en la interfaz y no está validada en el backend.
- Las dependencias de datos incluyen la coherencia: si una edición o eliminación cambia un gasto, las vistas agregadas y las fugas deben recalcularse o invalidar su caché.
- HU-16 no bloquea HU-23 ni HU-24 en el MVP: la detección y la evidencia se calculan sobre los gastos vigentes. La actualización tras edición o eliminación se verifica cuando HU-16 esté implementada.
- Las dependencias técnicas externas (Google, Cloudinary, correo, Expo, Android) requieren configuración y pruebas; no se resuelven solo escribiendo código.
- Las decisiones pendientes que bloquean una dependencia deben resolverse antes de implementar la historia afectada. En particular, HU-23 no puede implementarse sin D-01 y HU-28 no puede implementarse sin D-08.

### 7.2 Cadena crítica del MVP

**HU-01 → HU-02 → HU-10 → HU-11 → HU-12 → HU-13 → HU-14 → HU-20 / HU-21 → HU-23 → HU-24**, con **HU-33** verificada de forma transversal y **HU-04** completando el ciclo de sesión.

Si falla un eslabón de esta cadena, el flujo de demostración no puede completarse. Las historias Should y Could se planifican después de estabilizar esta cadena.

---

## 8. Matriz de trazabilidad

Todas las historias originales se conservan. La columna «Cambio realizado» indica si la historia fue reescrita, precisada, delimitada o postergada. Ninguna historia fue eliminada y no se crearon identificadores nuevos para reemplazar los originales.

| ID | Propósito original | Título mejorado | Cambio realizado | ¿Funcionalidad conservada? |
|---|---|---|---|---|
| HU-01 | Ver información pública de FUGA+. | Consultar información pública de FUGA+ y acceder a registro o inicio de sesión | Detallada; se precisan contenido público, navegación y bloqueo de rutas privadas. | Sí |
| HU-02 | Registrarse e iniciar sesión. | Registrarse e iniciar sesión con correo y contraseña | Precisados roles, validaciones, hash, sesión y errores. | Sí |
| HU-03 | Iniciar sesión con Google. | Iniciar sesión con una cuenta de Google | Precisados verificación de token, vinculación y roles. | Sí |
| HU-04 | Cerrar sesión de forma segura. | Cerrar sesión de forma segura | Precisadas limpieza local, revocación y navegación. | Sí |
| HU-05 | Recuperar el acceso mediante recuperación de contraseña. | Recuperar el acceso mediante restablecimiento de contraseña | Precisados token de un solo uso, prevención de enumeración de cuentas e invalidación. | Sí |
| HU-06 | Desactivar la cuenta de usuario. | Desactivar la propia cuenta de usuario | Delimitada frente a la desactivación administrativa; retención pendiente. | Sí |
| HU-07 | Ver y editar nombre, apellido y teléfono. | Consultar y editar nombres y teléfono del perfil | Precisados campos, autorización y validaciones. | Sí |
| HU-08 | Cambiar la foto de perfil. | Cambiar la foto de perfil | Precisada integración con Cloudinary, validación y seguridad. | Sí |
| HU-09 | Usar la foto de Google cuando esté disponible. | Usar la foto de perfil de Google cuando esté disponible | Precisadas alternativa, precedencia y consentimiento. | Sí |
| HU-10 | Ingresar un gasto en lenguaje natural. | Registrar un gasto escrito en lenguaje natural | Precisados borrador, validaciones, privacidad y errores. | Sí |
| HU-11 | Procesar el gasto con «Procesar con IA» y diccionario/reglas deterministas, sin API externa. | Procesar el gasto con «Procesar con IA» y reglas deterministas | Precisados determinismo, versionado, campos, errores y verificación de no uso de IA externa. | Sí |
| HU-12 | Revisar y corregir monto, categoría, descripción y otros campos antes de guardar. | Revisar y corregir los campos interpretados antes de guardar | Precisada revisión obligatoria, validación en backend y descarte. | Sí |
| HU-13 | Guardar el gasto bajo la cuenta del propietario y protegerlo de otras cuentas. | Guardar el gasto bajo la cuenta del propietario y aislarlo de otros usuarios | Precisados propiedad derivada de la sesión, idempotencia y atomicidad. | Sí |
| HU-14 | Ver el historial del más reciente al más antiguo. | Consultar el historial de gastos del más reciente al más antiguo | Precisados orden, paginación, detalle y estados. | Sí |
| HU-15 | Filtrar por fecha y categoría. | Filtrar el historial por fecha y categoría | Precisados combinación AND, límites, limpieza y autorización. | Sí |
| HU-16 | Editar y eliminar gastos guardados y actualizar análisis y resúmenes. | Editar y eliminar gastos guardados, actualizando análisis y resúmenes | Precisada coherencia de agregados; se conservan ambas operaciones. | Sí |
| HU-17 | Iniciar la grabación de voz en Android. | Iniciar la grabación de voz para un gasto en Android | Precisados permisos, ciclo de vida, privacidad y alternativa. | Sí |
| HU-18 | Convertir voz en texto con Kotlin y `SpeechRecognizer`. | Convertir la voz en texto con Kotlin y `SpeechRecognizer` | Precisados errores, sesión única, idioma y puente nativo. | Sí |
| HU-19 | Revisar transcripción y campos antes de guardar el gasto por voz. | Revisar la transcripción y los campos antes de guardar un gasto por voz | Precisado el flujo obligatorio voz → transcripción → procesamiento → revisión → guardado. | Sí |
| HU-20 | Ver total, número de gastos y promedio por periodo. | Consultar total, cantidad y promedio de gasto por periodo | Precisados promedio por gasto, periodo, cero y actualización. | Sí |
| HU-21 | Ver gastos por categoría e identificar la de mayor gasto. | Consultar el gasto por categoría e identificar la categoría de mayor gasto | Precisados empate, porcentajes y actualización. | Sí |
| HU-22 | Comparar gastos entre periodos. | Comparar el gasto entre periodos | Precisadas fórmulas, base cero y estados sin datos. | Sí |
| HU-23 | Detectar posibles fugas con reglas deterministas. | Detectar posibles fugas de dinero con reglas deterministas | Precisados evidencia, versionado, datos insuficientes y prohibición de IA/predicción. | Sí |
| HU-24 | Ver evidencia de una fuga, incluidas ocurrencias y acumulado. | Consultar la evidencia de una posible fuga de dinero | Precisadas consistencia, actualización y autorización. | Sí |
| HU-25 | Recibir alertas sobre posibles fugas. | Recibir alertas sobre posibles fugas de dinero | Delimitadas las alertas en la aplicación y locales; push remoto postergado. | Sí, con alcance de canal precisado |
| HU-26 | Ver sugerencias prácticas sobre posibles fugas. | Consultar sugerencias prácticas sobre posibles fugas | Precisados catálogo aprobado, tono y prohibición de asesoría. | Sí |
| HU-27 | Ver un resumen mensual de posibles fugas. | Consultar el resumen mensual de posibles fugas | Precisada asignación mensual y no duplicación. | Sí |
| HU-28 | Definir una meta mensual de gasto o ahorro con alcance explícito. | Definir una meta mensual de gasto o ahorro con alcance explícito | Postergada; el alcance sigue ambiguo y falta base para medir ahorro. | Sí, en backlog |
| HU-29 | Seguir el avance de la meta. | Consultar el avance hacia la meta definida | Postergada; depende de HU-28 y de una definición de meta. | Sí, en backlog |
| HU-30 | Ver estadísticas agregadas sin acceder a gastos individuales. | Consultar estadísticas agregadas de uso sin acceder a gastos individuales | Precisados métricas, agregación mínima y controles. | Sí |
| HU-31 | Ver usuarios registrados y datos administrativos necesarios. | Consultar usuarios registrados y la información administrativa necesaria | Precisados campos mínimos, minimización y prohibición de ver gastos. | Sí |
| HU-32 | Activar o desactivar cuentas mediante funciones autorizadas. | Activar o desactivar cuentas de usuario desde funciones administrativas autorizadas | Precisadas revocación de sesión, auto-protección y auditoría. | Sí |
| HU-33 | Proteger la privacidad y separar los datos entre usuarios. | Proteger la privacidad de los gastos y garantizar el aislamiento entre usuarios | Elevada a restricción transversal verificable en backend. | Sí |

### 8.1 Cambios de alcance y decisiones de trazabilidad

- **No hubo divisiones ni fusiones de historias.** Se conservaron los 33 identificadores y se mantuvo una sola historia para HU-16, aunque incluya edición y eliminación.
- **HU-11** conserva la etiqueta «Procesar con IA» y el propósito original, pero deja explícito que la implementación es un diccionario propio con reglas deterministas, sin API externa de IA. Cualquier documento anterior que mencione OpenAI debe actualizarse en otra tarea.
- **HU-25** conserva el propósito de alertar. Se delimita el canal: en el alcance actual se consideran alertas dentro de la app y notificaciones locales; las push remotas son una extensión futura de la misma historia y no un identificador nuevo.
- **HU-28 y HU-29** se conservan en el backlog como **Won't Have (for now)**. No se eliminan; se posterga su implementación hasta que se defina el alcance de la meta y, si aplica, la fuente de datos de ahorro.
- **HU-33** no reemplaza una funcionalidad de pantalla; es una restricción transversal que se implementa y verifica con las historias que acceden a gastos.
- **Colisión de identificadores del diagrama:** el diagrama existente usa HU-01 a HU-14 con otros significados. Este documento mantiene los 33 identificadores originales; el diagrama debe corregirse en una tarea separada para no mezclar ambas numeraciones.
- **Historias Should y Could:** se conservan completas y trazables, aunque no formen parte del MVP. Su postergación es de planificación, no de alcance funcional permanente.

---

## 9. Alcance propuesto del MVP

### 9.1 Definición

El MVP está formado por las **13 historias Must Have**. Su objetivo es demostrar, de extremo a extremo y con datos propios, el flujo que justifica FUGA+:

1. Un Visitante conoce la aplicación y accede al registro o al inicio de sesión (HU-01).
2. Se registra o inicia sesión con correo y contraseña (HU-02) y puede cerrar sesión (HU-04).
3. Escribe un gasto en lenguaje natural (HU-10), lo procesa con el diccionario y las reglas deterministas mediante «Procesar con IA» (HU-11), revisa y corrige los campos (HU-12) y lo guarda bajo su cuenta (HU-13).
4. Consulta su historial (HU-14) y su dashboard de total, cantidad, promedio y categoría principal (HU-20, HU-21).
5. El sistema detecta posibles fugas con reglas deterministas (HU-23) y muestra su evidencia (HU-24).
6. Todo el flujo está protegido por autorización y aislamiento de datos en el backend (HU-33).

### 9.2 Historias incluidas

| Módulo | Historias Must incluidas | Resultado esperado |
|---|---|---|
| M1. Acceso y cuentas | HU-01, HU-02, HU-04 | Entrada pública, identidad y cierre de sesión seguro. |
| M2. Perfil | — | El MVP puede usar un perfil mínimo sin edición ni foto. |
| M3. Gastos | HU-10, HU-11, HU-12, HU-13, HU-14 | Registro por texto, interpretación, revisión, persistencia e historial. |
| M4. Voz | — | La entrada por texto es suficiente para el MVP. |
| M5. Dashboard | HU-20, HU-21 | Totales, promedio y desglose por categoría del periodo. |
| M6. Fugas | HU-23, HU-24 | Detección determinista y evidencia explicable. |
| M7. Alertas y metas | — | No se incluyen alertas, sugerencias, resumen mensual ni metas. |
| M8. Administración y privacidad | HU-33 | Aislamiento de datos, roles y verificación de seguridad. |

**Total:** 13 historias Must. Doce son funcionalidades visibles y HU-33 es una restricción transversal. El panel administrativo (HU-30 a HU-32) no hace parte del MVP, aunque el modelo de roles y las reglas de autorización sí deben existir.

### 9.3 Flujo de demostración del MVP

**Visitante → pantalla pública → registro o inicio de sesión → registrar gasto por texto → «Procesar con IA» → revisar y corregir → confirmar y guardar → historial → dashboard → posible fuga con evidencia → cierre de sesión.**

La demostración debe poder ejecutarse con datos de prueba precargados y sin pasos manuales de configuración. Las reglas de detección utilizadas en la demostración deben ser las aprobadas en D-01, no valores inventados para la ocasión.

### 9.4 Criterios de salida del MVP

- Todas las historias Must cumplen sus criterios de aceptación en un entorno integrado.
- La suite de seguridad de HU-33 demuestra que un Usuario no puede leer, editar ni eliminar gastos de otro, y que un Administrador no accede a gastos individuales.
- El flujo de demostración se completa en un tiempo compatible con la exposición académica, sin depender de servicios no configurados.
- El dashboard y las fugas se recalculan correctamente después de crear un gasto; la edición y el borrado se verifican en la fase Should, porque no forman parte del MVP.
- Los datos de prueba existen y están separados de cualquier dato real.
- La documentación de decisiones pendientes está actualizada y no se presenta como acordado lo que sigue pendiente.

### 9.5 Límites conocidos del MVP

- **Sin Google sign-in:** se usa correo y contraseña. Google queda como Should y no cambia la arquitectura de autenticación.
- **Sin recuperación de contraseña:** el MVP no incluye correo transaccional. Debe existir un procedimiento operativo para pruebas, sin presentarlo como función terminada.
- **Sin edición ni eliminación posterior al guardado:** la corrección se realiza antes de confirmar. HU-16 se planifica después de los Must; si se implementa, debe actualizar agregados y fugas.
- **Sin filtros:** el historial completo es suficiente para el MVP.
- **Sin voz:** Android y el módulo Kotlin se postergan; el texto es el canal principal.
- **Sin alertas, sugerencias ni resumen mensual:** la evidencia de la fuga está disponible en la pantalla de análisis.
- **Sin metas:** HU-28 y HU-29 están postergadas.
- **Sin panel administrativo:** el rol existe y se prueba con cuentas de prueba; las funciones HU-30 a HU-32 se implementan después.
- **Sin notificaciones push:** no se configura Expo push ni backend de envío en el MVP.

### 9.6 Realismo para 12 semanas

El MVP es ambicioso pero acotado: no incluye las integraciones externas más costosas (Google, correo, Cloudinary, voz nativa, push) ni el panel administrativo. La seguridad transversal se implementa desde la primera semana, no al final. El plan reserva una semana de integración y prueba antes de congelar el MVP, y semanas posteriores para Should y Could. Si el avance del núcleo no es suficiente, se recortan primero las historias Should y Could; no se recorta HU-33.

---

## 10. Funcionalidades postergadas

### 10.1 Should Have posteriores al MVP

| Historias | Función | Motivo de postergación |
|---|---|---|
| HU-03 | Inicio de sesión con Google | Requiere OAuth, verificación de tokens y pruebas en dispositivos; el correo y la contraseña cubren el MVP. |
| HU-05 | Recuperación de contraseña | Requiere proveedor de correo, plantillas y tokens; importante pero no central para la demostración. |
| HU-07, HU-08 | Perfil editable y foto con Cloudinary | Mejoran la experiencia, pero no son necesarios para registrar y analizar gastos. |
| HU-15 | Filtros de historial | Útiles con muchos datos; el historial completo funciona en el MVP. |
| HU-16 | Edición y eliminación posterior | La revisión previa cubre la corrección inicial; la coherencia de agregados requiere tiempo. |
| HU-30, HU-31, HU-32 | Panel administrativo y gestión de cuentas | Importantes para operación, pero fuera del flujo de valor y de la demostración principal. |

### 10.2 Could Have si el cronograma lo permite

| Historias | Función | Condición para intentarlo |
|---|---|---|
| HU-06 | Desactivación por el propio Usuario | Debe existir una política de retención y reactivación (D-06). |
| HU-09 | Foto de perfil de Google | Depende de HU-03 y de una regla de precedencia (D-13). |
| HU-17, HU-18, HU-19 | Registro por voz en Android | Solo con compilación de desarrollo, dispositivo de prueba y núcleo estable; no se intenta en las últimas semanas. |
| HU-22 | Comparación entre periodos | Solo si HU-20 y HU-21 están estables y existe tiempo para pruebas de fórmulas. |
| HU-25 | Alertas de posibles fugas | Alcance local y en la aplicación; el push remoto no se incluye. |
| HU-26 | Sugerencias prácticas | Requiere catálogo revisado y aprobado; no se improvisa contenido. |
| HU-27 | Resumen mensual de fugas | Requiere definir la asignación mensual (D-01/D-04). |

### 10.3 Won't Have (for now)

- **HU-28 — Meta mensual de gasto o ahorro:** el alcance no está definido y una meta de ahorro requiere ingresos o una base de cálculo que hoy no existe.
- **HU-29 — Avance de la meta:** depende de HU-28.
- **Notificaciones push remotas:** extensión futura de HU-25. Requieren proyecto Expo/EAS, credenciales FCM/APNs, registro y almacenamiento de tokens, consentimiento, backend de envío y manejo de tokens inválidos. No forman parte del MVP ni del alcance actual de HU-25.
- **Funciones administrativas avanzadas:** múltiples niveles de administrador, exportaciones masivas, auditoría avanzada o gestión de permisos granular.
- **Conexiones bancarias, pagos, transferencias, tarjetas, créditos, préstamos, inversiones y asesoría financiera profesional.**
- **Entrenamiento de un modelo de IA propio, predicción de mercado o escaneo avanzado de recibos.**

### 10.4 Criterios para promover una historia postergada

Una historia Should o Could puede adelantarse solo si:

1. Todos los Must están implementados y verificados.
2. La suite de seguridad y las pruebas de regresión están estables.
3. La dependencia externa está configurada y probada.
4. La historia no pone en riesgo la fecha de la demostración ni la calidad del MVP.
5. Las decisiones pendientes que la bloquean están resueltas.

---

## 11. Plan de implementación sugerido para 12 semanas

El plan organiza el trabajo en semanas relativas, no en fechas exactas. Asume un desarrollador, con apoyo de herramientas de IA para generar andamiaje, pruebas y documentación, pero con revisión humana obligatoria. La integración, la seguridad, la depuración y la preparación de la demostración tienen tiempo reservado.

### 11.1 Secuencia semanal

| Semana | Enfoque | Historias | Entregable y verificación |
|---|---|---|---|
| 1 | Base técnica, seguridad y acceso público | HU-01, inicio de HU-02, bases de HU-33 | Entorno reproducible, API y base de datos conectadas, modelo de usuario, pantalla pública, contrato de autenticación, primer arnés de pruebas de seguridad. |
| 2 | Autenticación, sesión y aislamiento inicial | HU-02, HU-04, HU-33 | Registro, inicio de sesión, cierre de sesión, roles, almacenamiento seguro de tokens, rechazo de cuentas inactivas y pruebas de acceso cruzado. |
| 3 | Entrada de texto y procesamiento determinista | HU-10, HU-11 | Pantalla de entrada, endpoint de procesamiento, diccionario y reglas versionadas, corpus inicial de frases y verificación de ausencia de API externa de IA. |
| 4 | Revisión y persistencia | HU-12, HU-13 | Vista editable, validaciones en cliente y backend, confirmación explícita, propietario derivado de la sesión, idempotencia y pruebas de atomicidad. |
| 5 | Historial y dashboard | HU-14, HU-20, HU-21 | Historial paginado, resumen del periodo, promedio por gasto, desglose y categoría principal, con pruebas de datos conocidos. |
| 6 | Fugas y evidencia | HU-23, HU-24 | Motor de reglas con configuración aprobada, versionado, estado de datos insuficientes, evidencia consistente y pruebas de límites. |
| 7 | Integración y congelación del MVP | Todas las Must | Flujo completo de extremo a extremo, suite de seguridad, pruebas de regresión, revisión de rendimiento, primera demostración cronometrada y corrección de defectos. **No se agrega alcance nuevo.** |
| 8 | Acceso y perfil Should | HU-03, HU-05, HU-07, HU-08 | Integración de Google, recuperación por correo, perfil editable y carga en Cloudinary. Si una integración externa no está lista, se priorizan las demás y no se compromete el MVP. |
| 9 | Historial y administración Should | HU-15, HU-16, inicio de HU-30 | Filtros, edición y eliminación con recálculo de agregados, primeras métricas administrativas agregadas y pruebas de privacidad. |
| 10 | Cierre administrativo | HU-30, HU-31, HU-32 | Panel agregado, lista de usuarios y activación/desactivación con revocación de sesión y auditoría. Regresión de todas las historias Should. |
| 11 | Could Have y colchón | HU-22, HU-25, HU-27 o una porción de voz si el núcleo está estable | Solo funciones que no comprometan el MVP. La voz completa (HU-17 a HU-19) no se promete en esta semana; si no hay tiempo, se posterga. Semana también usable como colchón de defectos. |
| 12 | Candidato de entrega y demostración | Sin historias nuevas | Regresión completa, revisión de seguridad, documentación, guion y ensayo de demostración, datos de prueba, plan de contingencia y corrección de defectos críticos. |

### 11.2 Hitos

| Hito | Momento | Criterio |
|---|---|---|
| **H1 — Identidad y acceso** | Fin de la semana 2 | Registro, inicio y cierre de sesión funcionan con roles y pruebas de aislamiento inicial. |
| **H2 — Núcleo de gastos** | Fin de la semana 4 | Texto, procesamiento, revisión y persistencia funcionan de extremo a extremo. |
| **H3 — Análisis** | Fin de la semana 6 | Historial, dashboard y fugas con evidencia están integrados. |
| **H4 — MVP congelado** | Fin de la semana 7 | Todas las Must pasan la verificación y la demostración cronometrada. |
| **H5 — Should completadas o decididas** | Fin de la semana 10 | Las Should planificadas están terminadas o formalmente postergadas. |
| **H6 — Candidato de entrega** | Fin de la semana 12 | Regresión, seguridad y demostración listas; no hay defectos críticos abiertos. |

### 11.3 Uso de IA durante el desarrollo

La IA puede apoyar en:

- Generación de andamiaje, tipos, endpoints y componentes repetitivos.
- Generación y ampliación de pruebas unitarias, de integración y de seguridad.
- Construcción y revisión del corpus de frases para el diccionario.
- Redacción de documentación y revisión de consistencia.

La IA **no** reemplaza:

- La revisión humana del código y de las decisiones de seguridad.
- La verificación de que no se realizan llamadas a APIs externas de IA.
- La definición de umbrales de fugas, que debe ser aprobada por el proyecto.
- Las pruebas en dispositivos reales, especialmente para voz, permisos y notificaciones.
- La validación de integraciones externas y el manejo de secretos.

### 11.4 Cadencia y control

- **Inicio de semana:** revisar el objetivo, las dependencias y las decisiones pendientes que bloquean.
- **Mitad de semana:** integrar lo construido y ejecutar pruebas automatizadas; no acumular cambios para el final.
- **Fin de semana:** demostración interna, revisión de riesgos y ajuste del alcance.
- **Cada entrega:** ejecutar pruebas de regresión y la suite de seguridad de HU-33.
- **Antes de la semana 7:** no iniciar Should ni Could si el núcleo no está estable.

### 11.5 Plan de contingencia

Si el cronograma se retrasa, el orden de recorte es:

1. Cancelar las Could Have de la semana 11.
2. Postergar las Should Have que dependan de integraciones externas.
3. Reducir el alcance de una Should, por ejemplo limitar la administración a agregados y desactivación.
4. Si el núcleo Must está en riesgo, reducir la profundidad de una Must sin eliminar la privacidad: por ejemplo, mantener el total y la categoría principal antes que añadir visualizaciones adicionales.

**No se recorta HU-33.** Tampoco se presenta como terminada una función cuyos criterios de aceptación no se hayan verificado.

---

## 12. Decisiones pendientes, riesgos y supuestos

### 12.1 Decisiones pendientes

Las siguientes decisiones **no están acordadas** y no deben implementarse por suposición. Cada una indica las historias afectadas y el efecto de no resolverla.

| ID | Decisión pendiente | Impacto | Historias afectadas |
|---|---|---|---|
| **D-01** | Reglas de detección de fugas: umbrales, monto mínimo, frecuencia, ventana temporal, agrupación por categoría o descripción, condición mínima de datos y asignación a un mes. | Sin esta decisión no se puede implementar ni probar la detección de forma verificable. No se deben inventar valores. | HU-23, HU-24, HU-25, HU-26, HU-27 |
| **D-02** | Catálogo definitivo de categorías, tratamiento de «Otros», desempate de la categoría principal y visualización de categorías sin gasto. | Afecta la interpretación, la edición, el dashboard y la evidencia de fugas. | HU-11, HU-12, HU-15, HU-21, HU-23, HU-26 |
| **D-03** | Moneda, configuración regional, decimales, separadores, límites de monto y redondeo. | Afecta todos los cálculos y la visualización; una decisión tardía obliga a migrar datos y pruebas. | HU-11, HU-12, HU-13, HU-20, HU-21, HU-22, HU-28, HU-29 |
| **D-04** | Zona horaria, formatos de fecha, periodos disponibles, límites del mes, fechas futuras y frases relativas como «hoy» o «ayer». | Afecta el orden del historial, los filtros, el dashboard, las comparaciones y el resumen mensual. | HU-11, HU-12, HU-14, HU-15, HU-20, HU-21, HU-22, HU-27 |
| **D-05** | Alcance del parser: longitud del texto, formatos numéricos, abreviaturas, errores tolerados, varias frases o varios gastos, longitud de descripción y tamaño de página del historial. | Afecta la calidad de la interpretación y las pruebas del diccionario. | HU-10, HU-11, HU-12, HU-14, HU-19 |
| **D-06** | Diferencia entre desactivar y eliminar, retención de gastos, eliminación lógica o física, reactivación, exportación y respaldos. | Afecta la privacidad, la desactivación y la coherencia del historial. | HU-06, HU-13, HU-16, HU-29, HU-32, HU-33 |
| **D-07** | Métricas administrativas exactas, umbral mínimo de agregación para evitar reidentificación, filtros permitidos y frecuencia de actualización. | Sin un umbral, las estadísticas agregadas pueden revelar información individual. | HU-30, HU-31, HU-33 |
| **D-08** | Alcance de la meta: gasto o ahorro, fuente de ingresos, gastos incluidos, periodo, unicidad, edición y cálculo de avance. | Bloquea HU-28 y HU-29; una meta de ahorro no es calculable con los datos actuales. | HU-28, HU-29 |
| **D-09** | Política de autenticación: requisitos de contraseña, verificación de correo, duración y renovación del JWT, revocación, cierre de todas las sesiones, límites de intentos y proveedor de correo. | Afecta la seguridad, la recuperación, la desactivación y la experiencia de sesión. | HU-02, HU-04, HU-05, HU-06, HU-32, HU-33 |
| **D-10** | Vinculación de cuentas de Google con cuentas locales, tratamiento de correos coincidentes, cuentas solo con Google y verificación de correo. | Sin una regla segura se puede permitir una toma de control de cuenta. | HU-03, HU-05, HU-09 |
| **D-11** | Notificaciones: local frente a push, contenido, datos visibles en pantalla bloqueada, frecuencia, recordatorios, horario de silencio, estado leído y preferencias. | Determina si HU-25 es viable y cómo se protege la privacidad en el dispositivo. | HU-25, HU-32 |
| **D-12** | Voz: versión mínima de Android, idioma y variante, duración máxima, funcionamiento sin conexión, tratamiento del audio, conservación de la transcripción automática y aviso de privacidad. | Afecta la viabilidad técnica y la privacidad del canal de voz. | HU-17, HU-18, HU-19 |
| **D-13** | Perfil: campos obligatorios, formato de teléfono, cambio de correo, límites y tipos de imagen, recorte, moderación, precedencia entre foto de Google y foto cargada, y eliminación de activos en Cloudinary. | Afecta el perfil, la integración con Cloudinary y la experiencia. | HU-07, HU-08, HU-09 |
| **D-14** | Administración: campos visibles de los usuarios, búsqueda, exportación, motivo de desactivación, auditoría, tratamiento de otros administradores y protección del último administrador. | Afecta la operación, la privacidad y la continuidad administrativa. | HU-30, HU-31, HU-32, HU-33 |
| **D-15** | Comunicación del producto: texto público, uso de la etiqueta «Procesar con IA», explicación de que el procesamiento es determinista, avisos de privacidad y términos de uso. | Evita expectativas engañosas y da claridad sobre el tratamiento de datos. | HU-01, HU-11, HU-33 |
| **D-16** | Provisión de administradores: cómo se crea la primera cuenta administrativa, quién la autoriza y cómo se evita el registro público de administradores. | Sin esta decisión no hay una vía segura para operar el rol administrativo. | HU-02, HU-30, HU-31, HU-32 |

#### Orden recomendado para resolver decisiones

1. **Antes de la semana 3:** D-02, D-03, D-04 y D-05, porque bloquean la interpretación y la persistencia.
2. **Antes de la semana 6:** D-01, porque bloquea la detección verificable.
3. **Antes de la semana 8:** D-09, D-10, D-13 y D-15, por las integraciones y la comunicación.
4. **Antes de la semana 10:** D-07, D-14 y D-16, por la administración.
5. **Antes de iniciar HU-17 o HU-25:** D-11 y D-12.
6. **Antes de HU-28:** D-08.

### 12.2 Riesgos

| ID | Riesgo | Probabilidad | Impacto | Mitigación | Historias |
|---|---|---|---|---|---|
| **R-01** | El diccionario no cubre la variedad del español cotidiano (montos, abreviaturas, regionalismos, errores). | Alta | Alto | Conjunto representativo de frases, pruebas de límites, vista previa editable, corrección manual y revisión del contenido. | HU-10, HU-11, HU-12, HU-19 |
| **R-02** | Las reglas de fugas producen falsos positivos o falsos negativos y erosionan la confianza. | Alta | Alto | Aprobar D-01 antes de implementar, usar pocas reglas explicables, mostrar evidencia, versionar y probar con datos de fixture. | HU-23, HU-24, HU-25, HU-26, HU-27 |
| **R-03** | Fuga de datos entre usuarios o acceso administrativo indebido. | Media | Crítico | Filtro de propietario en el backend, pruebas IDOR/BOLA, prohibición de datos individuales en administración, revisión de logs y suite de seguridad. | HU-13, HU-14, HU-16, HU-30, HU-33 |
| **R-04** | El alcance de 12 semanas es demasiado grande para una persona. | Alta | Alto | Congelar el MVP en la semana 7, recortar Could y luego Should, reservar colchón y no iniciar integraciones opcionales antes del núcleo. | Todas |
| **R-05** | Integraciones externas (Google, correo, Cloudinary) no están configuradas o fallan en el entorno. | Media | Medio | Verificarlas temprano, tener una alternativa, no incluirlas en el MVP y probar con cuentas de prueba. | HU-03, HU-05, HU-08, HU-09 |
| **R-06** | El módulo nativo de voz no funciona en Expo Go o falla en dispositivos Android diversos. | Alta | Medio | Usar compilación de desarrollo, probar en dispositivos reales, limitar el alcance a Android y postergar si no hay tiempo. | HU-17, HU-18, HU-19 |
| **R-07** | Las notificaciones push requieren credenciales y backend que no están en el alcance. | Media | Medio | Mantener solo alertas en la aplicación y locales; documentar push como extensión futura. | HU-25 |
| **R-08** | Editar o eliminar un gasto deja agregados o fugas obsoletos. | Media | Alto | Calcular sobre datos vigentes o invalidar cachés, pruebas de recálculo y una única fuente de verdad. | HU-16, HU-20, HU-21, HU-23, HU-24, HU-27 |
| **R-09** | Un JWT sigue siendo válido después de desactivar una cuenta. | Media | Alto | Validar el estado de la cuenta en el backend o usar versionado/revocación de tokens; probar con una sesión abierta. | HU-02, HU-04, HU-32, HU-33 |
| **R-10** | Errores de moneda, decimales, zona horaria o límites de periodo producen cálculos incorrectos. | Media | Alto | Resolver D-03 y D-04, usar pruebas de límites y no confiar en el redondeo visual. | HU-11, HU-14, HU-20, HU-21, HU-22, HU-27 |
| **R-11** | Las estadísticas administrativas permiten reidentificar a un Usuario por grupos pequeños. | Media | Alto | Aplicar agregación mínima, evitar filtros individuales y revisar la salida antes de exponerla. | HU-30, HU-31, HU-33 |
| **R-12** | La demostración falla por red, lentitud o un servicio externo. | Media | Medio | Datos de prueba precargados, flujo principal ensayado, grabación de respaldo y evitar dependencias externas en la ruta crítica. | Todas las del flujo |
| **R-13** | La documentación existente contradice la decisión técnica actual (OpenAI frente a diccionario) o usa identificadores distintos en el diagrama. | Alta | Medio | Este documento fija la decisión actual y advierte la inconsistencia; actualizar README, requisitos y diagrama en tareas separadas. | HU-11, HU-23, HU-33 |
| **R-14** | Exposición de secretos de Cloudinary o de datos de perfil. | Media | Alto | Cargas firmadas o endpoint de backend, secretos fuera del cliente, validación de archivos y política de acceso a imágenes. | HU-08, HU-09, HU-33 |
| **R-15** | Confiar demasiado en código generado por IA sin revisión humana. | Media | Alto | Revisión obligatoria, pruebas, análisis de dependencias, revisión de seguridad y prohibición de que la IA invente reglas de negocio. | Todas |

### 12.3 Supuestos que requieren validación

| ID | Supuesto | Consecuencia si es falso |
|---|---|---|
| **A-01** | El proyecto lo desarrolla una sola persona durante 12 semanas, con apoyo de IA. | El plan debería reestimarse o reducirse el alcance. |
| **A-02** | React Native + TypeScript, FastAPI y MongoDB Atlas están disponibles y son accesibles desde el entorno. | Habría que resolver infraestructura antes de la semana 1. |
| **A-03** | El MVP puede usar correo y contraseña; Google se incorpora después. | Si Google es obligatorio para el MVP, se debe renegociar el alcance o reducir otra parte. |
| **A-04** | Existe una vía segura para provisionar una cuenta administradora, sin registro público de administradores. | Sin ella, no se puede probar el rol administrativo ni HU-30 a HU-32. |
| **A-05** | El procesamiento determinista se ejecuta en el backend y no llama a una API externa de IA. | Si se exigiera un servicio externo, cambiaría la arquitectura y la privacidad. |
| **A-06** | La voz es solo para Android y el texto es la alternativa en iOS. | Si se exige voz en iOS, aumenta considerablemente el alcance nativo. |
| **A-07** | Las notificaciones del alcance actual son locales o dentro de la app; el push es futuro. | Si el push es obligatorio, se necesitan credenciales, tokens y backend de envío. |
| **A-08** | Los datos de demostración son sintéticos y no contienen información financiera real. | Se requeriría un tratamiento de privacidad y consentimiento adicional. |
| **A-09** | La moneda y la configuración regional se decidirán en D-03; el ejemplo «$8.000» no fija por sí solo la moneda. | Los cálculos y formatos podrían requerir migración. |
| **A-10** | Las dependencias externas pueden usarse en un plan académico sin infraestructura institucional ni costos no previstos. | Habría que buscar alternativas o reducir el alcance. |
| **A-11** | Las decisiones pendientes pueden resolverse antes de las semanas indicadas. | Las historias bloqueadas deben postergarse; no se deben inventar reglas. |
| **A-12** | El alcance del MVP puede demostrarse sin panel administrativo, sin voz y sin push. | Si la evaluación exige esas funciones, el plan debe replantearse. |

### 12.4 Preguntas prioritarias para validar con el responsable del producto

1. ¿Cuáles son los valores exactos de las reglas de fugas y quién los aprueba? (D-01)
2. ¿Cuál es el catálogo cerrado de categorías y cómo se trata «Otros»? (D-02)
3. ¿Cuál es la moneda oficial y la configuración regional? (D-03)
4. ¿Cómo se define una meta: gasto, ahorro o ambas? (D-08)
5. ¿Qué datos puede ver exactamente un Administrador y con qué umbral de agregación? (D-07)
6. ¿Qué ocurre al desactivar o eliminar una cuenta y cuánto se conservan los datos? (D-06)
7. ¿Se acepta que el MVP use solo correo y contraseña y que Google, la voz y el push queden después? (A-03/A-06/A-07)
8. ¿Se acepta la etiqueta «Procesar con IA» con una explicación transparente de que el procesamiento es determinista? (D-15)

---

## Anexo A. Verificación de calidad del documento

### A.1 Conteos verificados

| Verificación | Resultado |
|---|---:|
| Historias de usuario | 33 |
| Identificadores únicos HU-01 a HU-33 | 33 |
| Historias Must Have | 13 |
| Historias Should Have | 9 |
| Historias Could Have | 9 |
| Historias Won't Have (for now) | 2 |
| Historias en el MVP | 13 |
| Filas en la tabla resumen | 33 |
| Filas en la matriz de dependencias | 33 |
| Filas en la matriz de trazabilidad | 33 |
| Criterios de aceptación | 196 |
| Criterios de aceptación duplicados | 0 |
| Decisiones pendientes D-01 a D-16 | 16 |
| Riesgos R-01 a R-15 | 15 |
| Supuestos A-01 a A-12 | 12 |
| Secciones principales | 12 |
| Tablas Markdown con columnas consistentes | 16 de 16 |
| Ciclos en el grafo de dependencias | 0 |

### A.2 Comprobaciones realizadas

- [x] Las 33 historias originales están presentes y conservan sus identificadores.
- [x] La tabla resumen, la matriz de dependencias y la matriz de trazabilidad contienen exactamente las mismas 33 historias, sin faltantes ni sobrantes.
- [x] La distribución MoSCoW coincide con las historias: 13 Must, 9 Should, 9 Could y 2 Won't.
- [x] El MVP contiene exactamente las 13 historias Must.
- [x] Cada historia tiene al menos un criterio de aceptación en formato Dado / Cuando / Entonces.
- [x] Los 196 criterios de aceptación tienen identificadores únicos.
- [x] Todas las referencias a HU-01 a HU-33 corresponden a historias existentes.
- [x] Todas las referencias D-xx, R-xx y A-xx tienen una definición en la sección 12.
- [x] El grafo de dependencias de la sección 7 no tiene ciclos.
- [x] No quedan marcadores de escritura por partes ni texto provisional.
- [x] El archivo está codificado en UTF-8 y no contiene caracteres de reemplazo.
- [x] Las tablas Markdown tienen un número consistente de columnas.
- [x] No se modificaron código, configuración, dependencias ni diagramas.
- [x] El único archivo creado o modificado por esta tarea es este documento.

### A.3 Pendientes fuera del alcance de este documento

1. **Resolver las decisiones de producto D-01 a D-16.** Las más urgentes para el núcleo son D-02, D-03, D-04, D-05 y D-01.
2. **Actualizar la documentación existente que contradice la decisión actual:** `README.md`, `docs/respuestas-ia/salida-requerimientos-priorizados.md` y cualquier referencia a OpenAI o a una API externa de IA.
3. **Corregir la colisión de identificadores del diagrama** `docs/diagramas/diagrama-historias-usuario.drawio`, que usa HU-01 a HU-14 con otros significados.
4. **Restaurar o reemplazar `docs/requisitos.md`**, actualmente ausente del árbol de trabajo y enlazado desde el README. No fue eliminado por esta tarea.
5. **Completar la arquitectura y el esquema** en `docs/architecture.md` y `docs/manifest_schema.md`, que hoy son marcadores de posición.
6. **Configurar y verificar las integraciones externas** cuando se aborden las historias correspondientes: Google, correo, Cloudinary, compilación Android con módulo nativo y notificaciones.
7. **Implementar el producto.** Este documento es de planificación; no contiene código ni sustituye las pruebas de implementación.
8. **Revisar y confirmar los supuestos A-01 a A-12** con el responsable del producto o el docente.

### A.4 Criterio de cierre

El documento se considera completo para la fase de planificación porque las 33 historias están revisadas, priorizadas, trazadas y conectadas con un MVP y un plan de 12 semanas. No se considera que el producto esté implementado ni que las decisiones pendientes estén resueltas. Cualquier cambio de alcance debe actualizar simultáneamente la historia, la tabla resumen, la matriz de dependencias, la matriz de trazabilidad, el MVP y el plan.

### A.5 Estado de Git observado

El estado de Git incluye cambios preexistentes que no pertenecen a esta tarea:

- `M docs/diagramas/diagrama-casos-uso.drawio`
- `D docs/requisitos.md`
- `?? docs/prompts-diseño/prompt-historias-usuario.md`
- `?? docs/respuestas-ia/salida-historias-usuario.md`

Este documento no fue confirmado ni subido a Git. No se realizó ningún commit.
