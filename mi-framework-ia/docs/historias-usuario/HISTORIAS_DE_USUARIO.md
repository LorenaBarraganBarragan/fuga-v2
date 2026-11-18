# FUGA+ — Historias de usuario priorizadas

**Versión:** 3.0 — línea base definitiva de especificación · **Fecha:** 2026-11-13

**Estado:** ESPECIFICACIÓN DOCUMENTAL DEFINITIVA. Decisiones D-01 a D-15 cerradas y aplicables según el alcance de cada prioridad; la implementación y sus pruebas se realizan posteriormente.

**Orden:** módulos funcionales con prioridad explícita; para planificar implementación, atender primero todas las Must Have, luego Should, Could y finalmente Won't.

**Tecnologías vigentes para conciliación:** React Native/TypeScript; FastAPI/Python; PostgreSQL en Supabase; Supabase Auth; procesamiento determinista sin API externa de IA. Las referencias antiguas a autenticación JWT propia o MongoDB en el contenido heredado no deben interpretarse como decisiones vigentes.

## Control de línea base definitiva (versión 3.0)

- Este documento es la especificación final de producto y aceptación; se conserva la numeración y priorización original.
- Las decisiones de diseño D-01 a D-15 se fijan en el apartado **Especificación definitiva de decisiones de producto y arquitectura** de este mismo archivo.
- Stack: React Native/TypeScript, FastAPI/Python, Supabase PostgreSQL y Supabase Auth. Sin MongoDB, JWT propio, Redis, Docker ni IA generativa externa como dependencia del MVP.
- Must Have define el MVP; Should/Could son ampliaciones especificadas; Won’t no se implementa en esta versión.
- Una especificación completa no constituye evidencia de que la aplicación esté implementada o de que un proveedor externo esté configurado.

## Índice de prioridad

**Decisión de entrega 2026-11-18:** se autoriza implementar el plan ACT-01 a ACT-15,
priorizando Android y la voz existente HU-17/18/19. Esta decisión de entrega no cambia
la clasificación MoSCoW 3.0 ni permite declarar voz aceptada por existir un bundle.
Permisos, Kotlin y flujo editable deben validarse en una compilación propia; el texto
continúa disponible como alternativa. Ver `docs/auditoria/ejecucion-plan-mejora-fugaplus.md`.

| Historia | Nombre | Prioridad | MVP |
|---|---|---|---|
| HU-01 | Consultar información pública de FUGA+ y acceder a registro o inicio de sesión | Must Have | Sí |
| HU-02 | Registrarse e iniciar sesión con correo y contraseña | Must Have | Sí |
| HU-03 | Iniciar sesión con una cuenta de Google | Should Have | No |
| HU-04 | Cerrar sesión de forma segura | Must Have | Sí |
| HU-05 | Recuperar el acceso mediante restablecimiento de contraseña | Should Have | No |
| HU-06 | Desactivar la propia cuenta de usuario | Could Have | No |
| HU-07 | Consultar y editar nombres y teléfono del perfil | Should Have | No |
| HU-08 | Cambiar la foto de perfil | Should Have | No |
| HU-09 | Usar la foto de perfil de Google cuando esté disponible | Could Have | No |
| HU-10 | Registrar un gasto escrito en lenguaje natural | Must Have | Sí |
| HU-11 | Procesar el gasto con «Procesar con IA» y reglas deterministas | Must Have | Sí |
| HU-12 | Revisar y corregir los campos interpretados antes de guardar | Must Have | Sí |
| HU-13 | Guardar el gasto bajo la cuenta del propietario y aislarlo de otros usuarios | Must Have | Sí |
| HU-14 | Consultar el historial de gastos del más reciente al más antiguo | Must Have | Sí |
| HU-15 | Filtrar el historial por fecha y categoría | Should Have | No |
| HU-16 | Editar y eliminar gastos guardados, actualizando análisis y resúmenes | Should Have | No |
| HU-17 | Iniciar la grabación de voz para un gasto en Android | Could Have | No |
| HU-18 | Convertir la voz en texto con Kotlin y `SpeechRecognizer` | Could Have | No |
| HU-19 | Revisar la transcripción y los campos antes de guardar un gasto por voz | Could Have | No |
| HU-20 | Consultar total, cantidad y promedio de gasto por periodo | Must Have | Sí |
| HU-21 | Consultar el gasto por categoría e identificar la categoría de mayor gasto | Must Have | Sí |
| HU-22 | Comparar el gasto entre periodos | Could Have | No |
| HU-23 | Detectar posibles fugas de dinero con reglas deterministas | Must Have | Sí |
| HU-24 | Consultar la evidencia de una posible fuga de dinero | Must Have | Sí |
| HU-25 | Recibir alertas sobre posibles fugas de dinero | Could Have | No |
| HU-26 | Consultar sugerencias prácticas sobre posibles fugas | Could Have | No |
| HU-27 | Consultar el resumen mensual de posibles fugas | Could Have | No |
| HU-28 | Definir un límite mensual global de gasto | Won't Have (for now) | No |
| HU-29 | Consultar el avance del límite mensual de gasto | Won't Have (for now) | No |
| HU-30 | Consultar estadísticas agregadas de uso sin acceder a gastos individuales | Should Have | No |
| HU-31 | Consultar usuarios registrados e información administrativa | Should Have | No |
| HU-32 | Activar o desactivar cuentas de usuario | Should Have | No |
| HU-33 | Proteger la privacidad de los gastos y garantizar el aislamiento entre usuarios | Must Have | Sí |

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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


**Trazabilidad:** se conserva el propósito original «ver información pública de FUGA+»; se precisa el contenido mínimo, la navegación y la protección de rutas privadas. Sin cambio funcional.

#### HU-02 — Registrarse e iniciar sesión con correo y contraseña

**Módulo:** 1 · Acceso, autenticación y cuentas  
**Prioridad:** **Must Have.** Crea la identidad que permite asociar gastos a un propietario, aplicar permisos y cumplir la privacidad. Es la base de todo el flujo y de la demostración.  
**MVP:** Sí.

> **Historia:** Como Visitante, quiero registrarme e iniciar sesión con correo y contraseña, para acceder a mis gastos y a las funcionalidades privadas de FUGA+.

**Objetivo y valor:** permitir la creación de una cuenta de rol Usuario y el acceso posterior con credenciales válidas, sin que el registro público pueda crear administradores. La sesión debe ser segura y verificable en el backend.

**Criterios de aceptación**

- **CA-02.1** — **Dado** que el Visitante proporciona un correo válido, una contraseña que cumple la política vigente y la confirmación correcta, **cuando** envía el registro, **entonces** se crea una cuenta con rol **Usuario**, Supabase Auth administra el almacenamiento seguro de la contraseña y la persona puede iniciar sesión o queda autenticada según el flujo aprobado.
- **CA-02.2** — **Dado** que ya existe una cuenta con el correo indicado, **cuando** se intenta registrar de nuevo, **entonces** el sistema rechaza la operación con un mensaje claro y no crea una segunda cuenta ni modifica la existente.
- **CA-02.3** — **Dado** que el Visitante envía un correo con formato inválido, una contraseña que no cumple la política o una confirmación distinta, **cuando** intenta registrarse, **entonces** ve errores asociados a los campos y no se crea la cuenta.
- **CA-02.4** — **Dado** que una cuenta activa introduce credenciales correctas, **cuando** inicia sesión, **entonces** establece una sesión gestionada por Supabase Auth y accede a sus funcionalidades privadas; **dado** que introduce credenciales incorrectas, **cuando** intenta entrar, **entonces** recibe un mensaje genérico que no revela si el correo o la contraseña fueron los incorrectos.
- **CA-02.5** — **Dado** que una cuenta fue desactivada por un administrador, **cuando** intenta iniciar sesión, **entonces** el sistema rechaza el acceso aunque las credenciales sean correctas, con un mensaje que no expone datos de la cuenta.
- **CA-02.6** — **Dado** que se completa un registro público, **cuando** se consulta el rol asignado en el backend, **entonces** el rol es **Usuario** y nunca **Administrador**; un intento de enviar un rol desde el cliente no modifica el rol asignado.

**Reglas de negocio, validaciones y errores**

- El correo se normaliza (por ejemplo, espacios exteriores y mayúsculas) y debe ser único; la unicidad se garantiza en el backend y en la base de datos.
- La política de contraseñas, la longitud máxima, la verificación de correo y la duración de la sesión están pendientes (D-09).
- Supabase Auth gestiona el almacenamiento seguro y la verificación de contraseñas; FUGA+ no almacena contraseñas en sus tablas ni las registra en logs.
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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


**Trazabilidad:** se conserva el propósito original «registrarse e iniciar sesión»; se precisan roles, validaciones, seguridad y errores. Sin cambio funcional.

#### HU-03 — Iniciar sesión con una cuenta de Google

**Módulo:** 1 · Acceso, autenticación y cuentas  
**Prioridad:** **Should Have.** Es un canal de autenticación acordado y reduce fricción, pero el MVP puede operar con correo y contraseña. La configuración OAuth, la verificación de tokens y las pruebas en dispositivos requieren tiempo adicional.  
**MVP:** No.

> **Historia:** Como Usuario, quiero iniciar sesión con mi cuenta de Google, para acceder sin recordar otra contraseña y aprovechar mi identidad existente.

**Objetivo y valor:** ofrecer un inicio de sesión alternativo y seguro mediante Google, creando o vinculando una cuenta de FUGA+ sin permitir tomas de control de cuentas existentes ni asignar roles privilegiados.

**Criterios de aceptación**

- **CA-03.1** — **Dado** que el Usuario elige «Continuar con Google» y completa el flujo con una cuenta de Google válida, **cuando** Supabase Auth valida el flujo OAuth, **entonces** inicia sesión en su cuenta de FUGA+ o, si no existe, se crea una cuenta con rol **Usuario** y se emite una sesión válida.
- **CA-03.2** — **Dado** que el Usuario cancela o rechaza el flujo de Google, **cuando** vuelve a la aplicación, **entonces** no se crea ninguna cuenta ni sesión y se mantiene en la pantalla de acceso con la opción de correo y contraseña.
- **CA-03.3** — **Dado** que el token de Google es inválido, está vencido, tiene una audiencia incorrecta o el correo no está verificado, **cuando** Supabase Auth valida el flujo, **entonces** rechaza la autenticación sin crear cuenta y devuelve un mensaje genérico.
- **CA-03.4** — **Dado** que la cuenta de FUGA+ vinculada a Google está desactivada, **cuando** el Usuario intenta entrar con Google, **entonces** se rechaza el acceso igual que en el inicio de sesión con contraseña.
- **CA-03.5** — **Dado** que el correo de Google coincide con una cuenta local existente, **cuando** se intenta vincular, **entonces** el sistema no inicia sesión ni fusiona datos sin cumplir la regla de vinculación aprobada (D-10); no se permite una toma de control por conocer un correo.

**Reglas de negocio, validaciones y errores**

- Solo se aceptan tokens emitidos para los identificadores de cliente configurados para Android, iOS o web del proyecto.
- Supabase Auth valida el flujo OAuth; FastAPI verifica el token de acceso de Supabase Auth y el rol. El cliente no decide la identidad ni el rol.
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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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
- **No se definen en esta sección umbrales, montos mínimos, frecuencias, ventanas ni cantidad mínima de datos.** Todos son decisiones pendientes (D-01) y deben aprobarse antes de implementar.
- La agrupación es por categoría y descripción normalizada, según D-01.
- El resultado es una lista de candidatos, no una afirmación de pérdida real. La interfaz debe usar lenguaje probabilístico y no culpabilizante.
- El cálculo se realiza bajo demanda, según D-01. En cualquier caso, debe ser reproducible y no dejar resultados obsoletos.
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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


**Trazabilidad:** se conserva el propósito original «ver evidencia de una posible fuga, incluyendo ocurrencias y monto acumulado»; se precisan consistencia, actualización y autorización. Sin cambio funcional.

### 6.7 Módulo 7 — Alertas, recomendaciones y metas

#### HU-25 — Recibir alertas sobre posibles fugas de dinero

**Módulo:** 7 · Alertas, recomendaciones y metas  
**Prioridad:** **Could Have.** Las alertas añaden comodidad, pero la posible fuga ya puede consultarse en la aplicación. Se contempla Expo Notifications para notificaciones del dispositivo; el envío push remoto sigue condicionado a verificación de costos, infraestructura, credenciales y consentimiento (D-11).  
**MVP:** No.

> **Historia:** Como Usuario, quiero recibir alertas sobre nuevas posibles fugas, para enterarme sin revisar manualmente el análisis.

**Objetivo y valor:** avisar de una posible fuga nueva o actualizada sin convertir la alerta en una afirmación de pérdida. La alerta debe respetar la privacidad, el permiso de notificaciones y las preferencias del Usuario.

**Criterios de aceptación**

- **CA-25.1** — **Dado** que el análisis detecta una posible fuga que el Usuario no había visto, **cuando** la aplicación está abierta, **entonces** muestra una alerta dentro de la app con una descripción breve, el número de ocurrencias, el monto acumulado y un acceso al detalle de la evidencia.
- **CA-25.2** — **Dado** que el Usuario concedió permiso para notificaciones locales, **cuando** se genera una alerta nueva, **entonces** la aplicación puede mostrar una notificación local; si el permiso fue denegado, la alerta dentro de la app sigue funcionando y no se bloquea el uso.
- **CA-25.3** — **Dado** que no existe una posible fuga nueva, **cuando** se evalúa el estado, **entonces** no se muestra ninguna alerta ni se genera una notificación vacía.
- **CA-25.4** — **Dado** que una misma posible fuga ya fue notificada para la misma versión de regla y evidencia, **cuando** se vuelve a evaluar, **entonces** no se repite la alerta de forma indiscriminada; el criterio exacto de novedad y recordatorio está pendiente (D-11).
- **CA-25.5** — **Dado** que el Usuario abre la alerta, **cuando** se navega al detalle, **entonces** llega a la evidencia de HU-24 correspondiente a su propia cuenta.
- **CA-25.6** — **Dado** el alcance actual, **cuando** se revisan los canales implementados, **entonces** el envío push remoto permanece deshabilitado hasta verificar y aprobar D-11 (costos, consentimiento, token de dispositivo, credenciales, servicio de envío y privacidad).
- **CA-25.7** — **Dado** que la notificación local se muestra en la pantalla bloqueada, **cuando** se utiliza el contenido genérico aprobado, **entonces** no expone montos, descripciones ni otros datos financieros sensibles; la decisión de contenido está pendiente (D-11).

**Reglas de negocio, validaciones y errores**

- Las alertas se generan solo a partir de posibles fugas del propietario; nunca incluyen datos de otros Usuarios.
- Se distingue **alerta en la aplicación** de **notificación local** y de **notificación push**. La primera es obligatoria dentro de esta historia opcional; la notificación local depende de permisos y compatibilidad, y el push remoto de D-11.
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
- Prueba de que no se envían datos a un servicio push sin habilitación y aprobación explícitas de D-11.
- Prueba de autorización y de ausencia de datos ajenos.

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


**Trazabilidad:** se conserva el propósito original «recibir alertas sobre posibles fugas»; se aprueba Expo Notifications como opción técnica, pero la activación del push remoto depende de D-11 dentro de la misma historia, sin crear un identificador nuevo. Sin pérdida de funcionalidad.

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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


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

**Decisiones de diseño aplicables**

Las decisiones mencionadas en esta historia quedan **resueltas y fijadas** por las políticas D-01 a D-15 de la línea base 3.0. En caso de contradicción con una formulación histórica de esta historia, **prevalece la especificación definitiva** incluida en este archivo.


**Trazabilidad:** se conserva el propósito original «ver un resumen mensual de posibles fugas»; se precisan asignación mensual, no duplicación y actualización. Sin cambio funcional.

#### HU-28 — Definir un límite mensual global de gasto

**Prioridad:** Won't Have (for now) · **MVP:** No · **Actor:** Usuario · **Estado:** Aprobada en revisión funcional.

> Como Usuario, quiero establecer un límite mensual global de gasto para planificar cuánto dinero deseo gastar durante un mes.

**Reglas funcionales aprobadas**

- **R-28.01** — Un único límite vigente por usuario y mes.
- **R-28.02** — El límite es global, sin separación por categorías ni metas de ahorro.
- **R-28.03** — Crear límites para el mes actual o futuros, nunca meses finalizados.
- **R-28.04** — Monto entero positivo en COP dentro del rango técnico.
- **R-28.05** — Modificar límites durante meses habilitados.
- **R-28.06** — Eliminar lógicamente con confirmación, sin afectar gastos.
- **R-28.07** — Conservar historial de cambios de monto.
- **R-28.08** — Considerar todos los gastos confirmados y no eliminados del mes, incluso anteriores al límite.
- **R-28.09** — Advertir si los gastos existentes exceden el monto, sin bloquear la operación.
- **R-28.10** — Validar y confirmar antes de guardar.
- **R-28.11** — Impedir límites vigentes duplicados; ofrecer modificar el existente.
- **R-28.12** — Permitir recreación después de eliminación lógica durante un mes habilitado.
- **R-28.13** — Usar tabla de límites y tabla de historial en PostgreSQL; verificar Supabase Auth desde FastAPI.
- **R-28.14** — Proteger propiedad, errores y reintentos sin duplicación.
- **R-28.15** — Cerrar automáticamente al finalizar el mes, preservando monto e historial.

**Criterios de aceptación aprobados**

- **CA-28.01** — Crear límite para mes actual o futuro.
- **CA-28.02** — Rechazar creación retroactiva.
- **CA-28.03** — Rechazar montos inválidos.
- **CA-28.04** — Garantizar unicidad de límite vigente por usuario/mes.
- **CA-28.05** — Modificar límites en periodos habilitados.
- **CA-28.06** — Conservar historial de modificaciones.
- **CA-28.07** — Eliminar lógicamente con confirmación.
- **CA-28.08** — No alterar gastos por eliminar el límite.
- **CA-28.09** — Advertir al guardar un límite ya excedido.
- **CA-28.10** — Solicitar confirmación antes de guardar.
- **CA-28.11** — No duplicar registros ante errores o reintentos.
- **CA-28.12** — Proteger límites de meses finalizados.
- **CA-28.13** — Impedir acceso a límites de otras cuentas.
- **CA-28.14** — Cerrar automáticamente por fecha sin tarea programada.

**Dependencias y observaciones:** HU-29 utiliza estos límites; cierre automático por mes según zona horaria oficial pendiente de formalización.

#### HU-29 — Consultar el avance del límite mensual de gasto

**Prioridad:** Won't Have (for now) · **MVP:** No · **Actor:** Usuario · **Estado:** Aprobada en revisión funcional.

> Como Usuario, quiero consultar cuánto he gastado respecto al límite mensual para conocer mi avance.

**Reglas funcionales aprobadas**

- **R-29.01** — Mostrar seguimiento si existe límite no eliminado.
- **R-29.02** — Consultar mes actual y meses anteriores con límite.
- **R-29.03** — Mostrar límite, gastos, porcentaje y diferencia COP.
- **R-29.04** — Contar gastos confirmados no eliminados del mes.
- **R-29.05** — Calcular (total gastado / límite) × 100.
- **R-29.06** — Diferenciar dentro, alcanzado y superado.
- **R-29.07** — Mostrar porcentaje real superior a 100 %; barra visual limitada a 100 %.
- **R-29.08** — Actualizar al crear, editar o eliminar gastos.
- **R-29.09** — Actualizar tras modificación del límite.
- **R-29.10** — Mostrar estado vacío y acceso a configuración.
- **R-29.11** — Conservar límite histórico al cerrar mes.
- **R-29.12** — Mensajes neutrales sin juicios financieros.
- **R-29.13** — Solo datos del usuario autenticado.
- **R-29.14** — Calcular en FastAPI con PostgreSQL.
- **R-29.15** — Sin notificaciones automáticas.

**Criterios de aceptación aprobados**

- **CA-29.01** — Mostrar límite del mes seleccionado.
- **CA-29.02** — Mostrar gastos, porcentaje y diferencia correctos.
- **CA-29.03** — Incluir gastos anteriores a crear el límite.
- **CA-29.04** — Excluir gastos eliminados lógicamente.
- **CA-29.05** — Mostrar disponible si no se supera.
- **CA-29.06** — Indicar 100 % al alcanzar el límite.
- **CA-29.07** — Mostrar exceso y porcentaje real.
- **CA-29.08** — No desbordar la barra visual.
- **CA-29.09** — Actualizar tras cambios de gastos.
- **CA-29.10** — Actualizar tras cambios del límite.
- **CA-29.11** — Mostrar histórico sin edición.
- **CA-29.12** — Manejar ausencia de límite sin división entre cero.
- **CA-29.13** — Impedir acceso cruzado.
- **CA-29.14** — Mensajes neutrales.

**Dependencias y observaciones:** HU-28; los gastos confirmados y no eliminados son la base del cálculo.

### 6.8 Módulo 8 — Administración y privacidad

#### HU-30 — Consultar estadísticas agregadas de uso sin acceder a gastos individuales

**Prioridad:** Should Have · **MVP:** No · **Actor:** Administrador · **Estado:** Aprobada en revisión funcional.

> Como Administrador, quiero consultar estadísticas agregadas de uso de la plataforma sin acceder a gastos individuales.

**Reglas funcionales aprobadas**

- **R-30.01** — Acceso exclusivo de administradores autorizados.
- **R-30.02** — Mostrar total de usuarios registrados.
- **R-30.03** — Mostrar cuentas activas e inactivas.
- **R-30.04** — Mostrar conteo global de gastos confirmados no eliminados.
- **R-30.05** — Mostrar usuarios con actividad mensual.
- **R-30.06** — Mostrar evolución mensual de usuarios con actividad.
- **R-30.07** — Consultar mes actual y anteriores.
- **R-30.08** — No mostrar gastos, descripciones, categorías ni importes personales.
- **R-30.09** — No permitir navegar a finanzas individuales.
- **R-30.10** — Aplicar agregación mínima según D-07.
- **R-30.11** — Consultas agregadas en FastAPI y PostgreSQL.
- **R-30.12** — Estados vacíos y errores seguros.
- **R-30.13** — Sin IA generativa ni analítica externa.
- **R-30.14** — Fuera del MVP inicial.

**Criterios de aceptación aprobados**

- **CA-30.01** — Administrador accede.
- **CA-30.02** — Usuario/visitante denegado.
- **CA-30.03** — Total de registrados correcto.
- **CA-30.04** — Estados de cuentas correctos.
- **CA-30.05** — Conteo excluye eliminados.
- **CA-30.06** — Usuarios activos únicos por mes.
- **CA-30.07** — Gráfico mensual correcto.
- **CA-30.08** — No aparecen datos financieros individuales.
- **CA-30.09** — API no entrega datos personales financieros.
- **CA-30.10** — Suprimir grupos con agregación insuficiente.
- **CA-30.11** — Estado vacío correcto.
- **CA-30.12** — Errores sin datos sensibles.
- **CA-30.13** — Indicadores actualizados.
- **CA-30.14** — Sin predicciones.

**Dependencias y observaciones:** HU-33; D-07 requiere definir el umbral de agregación mínima antes de implementar.

#### HU-31 — Consultar usuarios registrados e información administrativa

**Prioridad:** Should Have · **MVP:** No · **Actor:** Administrador · **Estado:** Aprobada en revisión funcional.

> Como Administrador, quiero consultar los usuarios registrados y su información administrativa mínima para gestionar sus cuentas.

**Reglas funcionales aprobadas**

- **R-31.01** — Acceso exclusivo de administradores autorizados.
- **R-31.02** — Listado paginado.
- **R-31.03** — Buscar por nombre o correo.
- **R-31.04** — Filtrar por estado activo/inactivo.
- **R-31.05** — Mostrar ID, nombre disponible, correo, rol, estado y fecha de registro.
- **R-31.06** — Vista de detalle con los mismos campos.
- **R-31.07** — No mostrar contraseñas, tokens ni credenciales.
- **R-31.08** — No mostrar datos financieros individuales.
- **R-31.09** — Solo consulta, sin modificación.
- **R-31.10** — FastAPI verifica identidad y rol.
- **R-31.11** — Paginación y límites de resultados.
- **R-31.12** — Estados vacíos y búsquedas sin coincidencia.
- **R-31.13** — Errores y denegaciones seguros.
- **R-31.14** — Sincronización con Supabase Auth y perfiles administrativos.

**Criterios de aceptación aprobados**

- **CA-31.01** — Administrador puede acceder.
- **CA-31.02** — Usuario/visitante denegado.
- **CA-31.03** — Campos permitidos correctos.
- **CA-31.04** — Búsqueda por nombre.
- **CA-31.05** — Búsqueda por correo.
- **CA-31.06** — Filtros de estado.
- **CA-31.07** — Paginación sin duplicados.
- **CA-31.08** — Detalle con campos mínimos.
- **CA-31.09** — Sin gastos individuales.
- **CA-31.10** — Sin secretos.
- **CA-31.11** — Sin edición desde HU-31.
- **CA-31.12** — Sin coincidencias: mensaje claro.
- **CA-31.13** — Errores seguros.
- **CA-31.14** — Datos administrativos consistentes.

**Dependencias y observaciones:** HU-33 y HU-32; sin operaciones de edición de cuentas.

#### HU-32 — Activar o desactivar cuentas de usuario

**Prioridad:** Should Have · **MVP:** No · **Actor:** Administrador · **Estado:** Aprobada en revisión funcional.

> Como Administrador, quiero activar o desactivar cuentas mediante funciones autorizadas para gestionar su acceso.

**Reglas funcionales aprobadas**

- **R-32.01** — Solo administradores autorizados.
- **R-32.02** — Gestionar desde detalle de HU-31.
- **R-32.03** — Mostrar estado actual.
- **R-32.04** — Confirmar antes de cambiar.
- **R-32.05** — Desactivar sin borrar datos.
- **R-32.06** — Restringir acceso a funciones protegidas.
- **R-32.07** — FastAPI verifica estado en cada solicitud protegida.
- **R-32.08** — Bloquear sesiones previas y verificar revocación de Supabase Auth.
- **R-32.09** — Reactivar sujeto a autenticación.
- **R-32.10** — Impedir autodesactivación del administrador.
- **R-32.11** — Proteger cuentas administrativas con política específica.
- **R-32.12** — Auditar actor, cuenta, acción y fecha.
- **R-32.13** — Evitar duplicados y conflictos concurrentes.
- **R-32.14** — Mensajes claros.
- **R-32.15** — Sincronizar estado con Supabase Auth y FastAPI.
- **R-32.16** — No permitir acceso a gastos individuales.

**Criterios de aceptación aprobados**

- **CA-32.01** — Administrador autorizado cambia estado.
- **CA-32.02** — Usuario normal no puede.
- **CA-32.03** — Estado previo visible.
- **CA-32.04** — Confirmación requerida.
- **CA-32.05** — Cancelación sin cambios.
- **CA-32.06** — Cuenta desactivada sin acceso.
- **CA-32.07** — Sesión previa no elude bloqueo.
- **CA-32.08** — Reactivación permite volver a autenticarse.
- **CA-32.09** — No se eliminan datos.
- **CA-32.10** — Sin autodesactivación.
- **CA-32.11** — Protección de cuentas administrativas.
- **CA-32.12** — Auditoría completa.
- **CA-32.13** — Concurrencia consistente.
- **CA-32.14** — Fallos parciales no se reportan como éxito.
- **CA-32.15** — Mensajes claros.
- **CA-32.16** — Sin acceso financiero.

**Dependencias y observaciones:** HU-31 y HU-33; verificar técnicamente revocación de sesiones en Supabase Auth.

#### HU-33 — Proteger la privacidad de los gastos y garantizar el aislamiento entre usuarios

**Prioridad:** Must Have · **MVP:** Sí · **Actor:** Usuario autenticado · **Estado:** Aprobada en revisión funcional.

> Como Usuario autenticado, quiero tener mis datos financieros protegidos y aislados de los de otros usuarios.

**Reglas funcionales aprobadas**

- **R-33.01** — Autenticación para datos financieros.
- **R-33.02** — FastAPI valida firma, vigencia y validez del token de Supabase Auth.
- **R-33.03** — Identidad derivada del token, no de un ID enviado por cliente.
- **R-33.04** — Cada recurso privado tiene propietario.
- **R-33.05** — Consultas limitadas al propietario.
- **R-33.06** — Prohibir editar/eliminar recursos ajenos.
- **R-33.07** — Aislamiento en categorías, estadísticas, fugas, recomendaciones y límites cuando existan.
- **R-33.08** — Administrador sin acceso a gastos individuales.
- **R-33.09** — Autorización en backend, no solo interfaz.
- **R-33.10** — Rechazar tokens inválidos, ausentes o vencidos.
- **R-33.11** — Restringir cuentas desactivadas cuando HU-32 exista.
- **R-33.12** — HTTPS y protección de secretos.
- **R-33.13** — Controles de PostgreSQL y RLS según arquitectura de conexión.
- **R-33.14** — Errores/logs sin secretos ni datos financieros.
- **R-33.15** — Limpiar datos privados al cerrar sesión o cambiar cuenta.
- **R-33.16** — Validar propiedad en operaciones individuales y masivas.
- **R-33.17** — Pruebas automatizadas de aislamiento.
- **R-33.18** — Protección transversal desde MVP.

**Criterios de aceptación aprobados**

- **CA-33.01** — Acceder a gastos propios.
- **CA-33.02** — Denegar lectura de gastos ajenos.
- **CA-33.03** — Denegar edición/borrado ajeno.
- **CA-33.04** — IDs manipulados no eluden autorización.
- **CA-33.05** — Sin autenticación: denegado.
- **CA-33.06** — Tokens inválidos: denegados.
- **CA-33.07** — Identidad correcta desde token.
- **CA-33.08** — Estadísticas personales aisladas.
- **CA-33.09** — Fugas y evidencias aisladas.
- **CA-33.10** — Límites aislados cuando se implementen.
- **CA-33.11** — Administrador sin gastos individuales.
- **CA-33.12** — Cuentas desactivadas bloqueadas cuando HU-32 exista.
- **CA-33.13** — Sin claves de servicio en app.
- **CA-33.14** — Logs y errores seguros.
- **CA-33.15** — Cerrar sesión limpia datos privados.
- **CA-33.16** — Operaciones masivas respetan propietario.
- **CA-33.17** — Pruebas entre dos usuarios.
- **CA-33.18** — MVP no se completa sin aislamiento.

**Dependencias y observaciones:** Transversal a todas las historias que manejen información privada; la implementación debe verificarse con pruebas.





## Especificación definitiva de decisiones de producto y arquitectura

**Estado:** decisiones D-01 a D-15 cerradas para la línea base documental 3.0. Son decisiones de diseño del proyecto, no afirmaciones de que los servicios externos estén configurados ni de que las funciones estén implementadas.

### D-01 — Detección de posibles fugas
- **Regla FUGA-01, versión 1.0:** analizar los últimos **30 días calendario**, incluido el día de consulta, usando la zona horaria `America/Bogota`. Agrupar por **categoría y descripción normalizada** (minúsculas, espacios compactados, sin tildes, equivalencias explícitas del diccionario). No agrupar únicamente por categoría, para evitar falsos positivos.
- Generar un candidato si existen **al menos 3 gastos** del mismo grupo en **3 fechas distintas** de la ventana, cada uno de valor **entre COP 1.000 y COP 30.000**, y la suma del grupo es **al menos COP 15.000**. La categoría «Otros» se admite cuando la descripción normalizada es informativa; las descripciones vacías o genéricas («gasto», «compra», «otro») no activan esta regla.
- Cada resultado expone regla y versión, categoría, descripción normalizada, número de gastos, fechas, total exacto y los identificadores de gastos que sustentan la evidencia. No se presentan predicciones, culpabilidad, ahorros garantizados ni resultados sin evidencia.
- Calcular **bajo demanda** al consultar fugas y después de confirmar un gasto si la pantalla de fugas está abierta; no se requieren trabajos programados. Sin gastos: estado vacío; con menos de tres ocurrencias elegibles: «datos insuficientes para identificar patrones». El mismo conjunto de datos produce el mismo resultado.
- Los umbrales son **parámetros configurables versionados**, pero estos valores constituyen la configuración inicial obligatoria; cualquier cambio futuro requiere nueva versión de regla y pruebas de regresión.

### D-02 — Categorías y clasificación
- Catálogo inicial cerrado: **Alimentación, Transporte, Vivienda, Servicios, Educación, Salud, Entretenimiento, Compras y Otros**. «Otros» es categoría válida y **siempre se incluye** en totales, estadísticas y filtros.
- El diccionario determinista propone categoría cuando hay coincidencia inequívoca; ante ausencia de coincidencia asigna «Otros» y permite corrección manual antes de confirmar. Si dos reglas tienen igual precedencia, prevalece la coincidencia de frase más larga y, si persiste el empate, «Otros» con revisión manual.
- Para categorías empatadas en el máximo, mostrar **todas las categorías empatadas** ordenadas alfabéticamente; nunca escoger una sin indicarlo.

### D-03 — Moneda, montos y cálculos
- El MVP maneja **únicamente pesos colombianos (COP)**, sin conversión de divisas. Montos **enteros positivos** desde **COP 1** hasta **COP 100.000.000** por gasto. El separador de miles es visual y no se almacena; se rechazan centavos, valores negativos, cero y monedas diferentes.
- Persistir montos como entero (`BIGINT` o tipo equivalente con restricción); sumar enteros en backend/base de datos, sin punto flotante. Mostrar formato local `es-CO`, con símbolo `$` y aclaración COP cuando sea necesario.
- Porcentajes comparativos: calcular con valores exactos, mostrar **un decimal** y redondeo convencional; si el periodo base es cero, mostrar «sin base de comparación», no infinito.

### D-04 — Fechas, periodos y zona horaria
- Zona horaria funcional **`America/Bogota`**. Fecha del gasto en formato ISO `YYYY-MM-DD`, sin hora obligatoria. Si no se reconoce una fecha en el texto, proponer la fecha actual local y permitir corrección antes de guardar.
- Admitir fechas desde **2020-01-01** hasta **la fecha actual local**; no registrar gastos futuros. El historial ordena por `fecha_gasto DESC, created_at DESC, id DESC`, para desempate estable.
- Dashboard inicial: **mes calendario actual**, del primer al último día local; permitir elegir otros meses desde enero de 2020. Comparación opcional: mes seleccionado frente al mes inmediatamente anterior. Rangos inclusivos en fechas y consultas SQL con límites temporales explícitos.
- Una fuga se atribuye a la ventana móvil de 30 días en la que se calcula; para resúmenes mensuales opcionales se contabilizan **solo los gastos cuya fecha cae dentro del mes**, sin duplicar gastos entre categorías.

### D-05 — Procesamiento, límites e idempotencia
- «**Procesar con IA**» es el **nombre de interfaz**, acompañado de la explicación visible «Interpretación automática mediante reglas; no utiliza IA generativa». No se invoca una API externa de IA.
- Entrada de texto: **1 a 280 caracteres** tras recortar espacios. Diccionario versionado, reglas con prioridad fija y pruebas de frases de ejemplo; extraer monto, fecha, descripción y categoría propuesta. Si faltan monto o datos esenciales, exigir corrección; **jamás guardar sin confirmación explícita**.
- La descripción final tiene **1 a 120 caracteres**; el usuario puede modificar todos los campos interpretados. No persistir borradores incompletos en el servidor; el borrador se mantiene solo en memoria de la pantalla y se descarta al abandonarla.
- Confirmación de gasto con clave de idempotencia UUID por intento; conservarla **24 horas**. Misma clave y mismo contenido devuelven el mismo resultado; misma clave con contenido distinto produce **409 Conflict**.

### D-06 — Eliminación, desactivación y conservación
- En el MVP no se ofrece eliminar la cuenta ni gastos (HU-06 y HU-16 no son Must). Cuando se implementen, la eliminación de gastos será **lógica**, con `deleted_at`, y excluirá de inmediato esos registros de historial, dashboard y fugas.
- Desactivar una cuenta: marcar `disabled_at`, impedir operaciones privadas mediante validación en backend y solicitar revocación de sesiones al proveedor cuando esté disponible. La denegación por estado de cuenta **no depende únicamente de que expire el token**.
- Los datos de una cuenta desactivada se conservan durante **30 días** para recuperación administrativa y después se programan para supresión conforme a las obligaciones legales aplicables; no prometer borrado irreversible de copias de seguridad antes de sus ciclos de retención. Para un prototipo académico sin usuarios reales, emplear datos de prueba.
- No conservar transcripciones de voz ni texto original del gasto más allá de los campos confirmados, salvo que el usuario lo incorpore voluntariamente a la descripción final.

### D-07 — Privacidad de estadísticas administrativas
- Administrador: puede consultar **metadatos mínimos de cuentas** necesarios para HU-31/HU-32, pero **no gastos individuales, descripciones, evidencias de fugas ni totales identificables por persona**.
- Los agregados financieros administrativos solo se muestran cuando el grupo contiene **al menos 10 usuarios distintos**; grupos menores se suprimen. No permitir filtros combinables que revelen grupos pequeños ni exponer identificadores en la respuesta.

### D-08 — Roles y autorización
- Roles **Visitante, Usuario y Administrador**. La identidad la verifica Supabase Auth; FastAPI valida firma, emisor, audiencia, expiración y estado de cuenta, y aplica autorización por rol y propietario **en cada solicitud protegida**.
- El rol administrativo se asigna **solo por un mecanismo de aprovisionamiento seguro**, nunca por un campo editable del registro. Un Administrador no obtiene acceso a gastos de usuarios aunque conozca su identificador.
- Para acceso directo a Supabase desde el cliente, activar y probar **Row Level Security (RLS)**; si el backend usa credenciales privilegiadas, filtrar explícitamente por el usuario autenticado y no exponer dichas credenciales al móvil.

### D-09 — Registro, contraseñas, sesiones y recuperación
- Autenticación administrada por **Supabase Auth**, sin emitir JWT propios en FastAPI. Registro con correo válido y contraseña de **mínimo 8 caracteres**; confirmación de correo activada cuando el proveedor de correo del proyecto esté configurado.
- Sesión gestionada por SDK de Supabase con renovación segura de tokens; el backend rechaza tokens inválidos o expirados. Al cerrar sesión se elimina la sesión local y se solicita cierre en Supabase. No prometer revocación instantánea de tokens de acceso ya emitidos; el backend consulta el estado deshabilitado de la cuenta para bloquear solicitudes.
- Recuperación mediante **enlace de restablecimiento enviado por Supabase Auth**, con caducidad y un solo uso conforme a la configuración real del proveedor; no inventar una duración independiente ni construir un sistema de tokens propio. Si el correo saliente no está configurado, mostrar una indisponibilidad explícita en vez de simular un envío.

### D-10 — Google OAuth
- Inicio con Google mediante **proveedor OAuth de Supabase Auth**, solo cuando credenciales, URI de redirección y consentimiento estén configurados. Nunca unir dos cuentas basándose exclusivamente en coincidencia de correo: exigir la vinculación autenticada/verificada que soporte el proveedor.
- Google es **Should Have**, no dependencia del registro por correo del MVP. Si falla OAuth, conservar el acceso por correo y mostrar error recuperable.

### D-11 — Alertas y notificaciones
- HU-25 es **Could Have**. La aplicación puede mostrar alertas **internas** basadas en FUGA-01; **Expo Notifications** se adopta para notificaciones **locales** opcionales con permiso del sistema operativo.
- **No se incluye push remoto en la línea base**: no se requiere servidor de envío, token push ni servicio de terceros para cumplir HU-25. La decisión evita asumir precios o cuotas no verificados. Cualquier ampliación a push remoto será cambio de alcance documentado.
- Máximo **una alerta local por candidato y versión de regla en 7 días**, sin notificaciones entre **21:00 y 08:00** hora local. Texto genérico: «FUGA+ encontró un patrón de gastos para revisar»; sin importes ni descripciones en pantalla bloqueada. Si se deniega el permiso, la alerta interna sigue disponible.

### D-12 — Voz
- Captura de voz opcional para Android mediante **Kotlin `SpeechRecognizer`**, idioma preferido `es-CO`, con alternativa `es` cuando esté disponible. Máximo **30 segundos** por captura y **280 caracteres** de transcripción editable.
- Solicitar permiso de micrófono en contexto; nunca grabar ni guardar archivos de audio en FUGA+. Mostrar aviso de que el servicio de reconocimiento del dispositivo **puede procesar audio mediante servicios externos** según su configuración. Si el permiso o el reconocimiento no están disponibles, ofrecer entrada por texto sin bloquear el flujo.

### D-13 — Perfil e imágenes
- Nombres: **2 a 80 caracteres**; teléfono colombiano opcional de **10 dígitos**, sin tratarlo como identificador de autenticación.
- Foto de perfil opcional: JPEG/PNG/WebP, máximo **5 MB**, subida a **Cloudinary** mediante firma o endpoint controlado por backend; nunca exponer secretos de Cloudinary en el cliente. La foto de Google puede utilizarse como sugerencia inicial si el usuario lo permite, y una foto cargada manualmente tiene precedencia.

### D-14 — Auditoría
- Registrar eventos administrativos de **consulta de listado, cambio de estado de cuenta y fallo de autorización** con fecha UTC, actor, acción, resultado y cuenta objetivo cuando proceda; **sin gastos, contraseñas, tokens ni contenido financiero**. Retener registros de auditoría **90 días** en el prototipo y restringir acceso a responsables autorizados.
- No exigir auditoría avanzada de edición de gastos en el MVP; cuando HU-16 exista, registrar identificador, actor y fecha del cambio sin duplicar descripciones sensibles.

### D-15 — Transparencia y lenguaje
- Mantener literalmente el botón **«Procesar con IA»** por decisión de producto, pero añadir junto al flujo la aclaración «Interpretación mediante reglas automáticas; no utiliza IA generativa ni envía tu gasto a una IA externa».
- Usar «**posible fuga**», «patrón detectado» y «revisar»; evitar «derroche», «error financiero», promesas de ahorro o diagnósticos personales.
- Las explicaciones de fugas deben mostrar regla, intervalo, número de ocurrencias y gastos de soporte; el usuario decide cómo interpretar el hallazgo.

### Política de cambios
Esta línea base define **qué debe construirse**. Las historias Should/Could y las Won't quedan documentadas para evolución, pero **no son obligaciones del MVP**. Cambios de umbrales, proveedores, costos, reglas de privacidad o alcance requieren nueva versión documental y actualización simultánea de RF/HU. Las pruebas de aceptación y las verificaciones de configuración externa son actividades de implementación, no decisiones documentales pendientes.

## Matriz explícita de trazabilidad HU ↔ RF

La correspondencia por identificador y alcance constituye la trazabilidad definitiva de la especificación; la implementación se valida mediante pruebas. Las RNF son transversales y se relacionan en sus apartados.

| Historia | Requerimiento | Prioridad | MVP |
|---|---|---|---|
| HU-01 | RF-001 | Must Have | Sí |
| HU-02 | RF-002 | Must Have | Sí |
| HU-03 | RF-003 | Should Have | No |
| HU-04 | RF-004 | Must Have | Sí |
| HU-05 | RF-005 | Should Have | No |
| HU-06 | RF-006 | Could Have | No |
| HU-07 | RF-007 | Should Have | No |
| HU-08 | RF-008 | Should Have | No |
| HU-09 | RF-009 | Could Have | No |
| HU-10 | RF-010 | Must Have | Sí |
| HU-11 | RF-011 | Must Have | Sí |
| HU-12 | RF-012 | Must Have | Sí |
| HU-13 | RF-013 | Must Have | Sí |
| HU-14 | RF-014 | Must Have | Sí |
| HU-15 | RF-015 | Should Have | No |
| HU-16 | RF-016 | Should Have | No |
| HU-17 | RF-017 | Could Have | No |
| HU-18 | RF-018 | Could Have | No |
| HU-19 | RF-019 | Could Have | No |
| HU-20 | RF-020 | Must Have | Sí |
| HU-21 | RF-021 | Must Have | Sí |
| HU-22 | RF-022 | Could Have | No |
| HU-23 | RF-023 | Must Have | Sí |
| HU-24 | RF-024 | Must Have | Sí |
| HU-25 | RF-025 | Could Have | No |
| HU-26 | RF-026 | Could Have | No |
| HU-27 | RF-027 | Could Have | No |
| HU-28 | RF-028 | Won't Have (for now) | No |
| HU-29 | RF-029 | Won't Have (for now) | No |
| HU-30 | RF-030 | Should Have | No |
| HU-31 | RF-031 | Should Have | No |
| HU-32 | RF-032 | Should Have | No |
| HU-33 | RF-033 | Must Have | Sí |

## Verificaciones de implementación posteriores a la especificación

1. Verificar mediante pruebas los parámetros ya fijados en D-01, D-02, D-03, D-04 y D-09.
2. Probar autorización por propietario y rol con Supabase Auth, FastAPI y políticas de acceso PostgreSQL; no asumir que la documentación demuestra aislamiento efectivo.
3. Probar las notificaciones locales definidas en D-11; el push remoto está excluido de esta línea base.
4. Verificar el cumplimiento de las políticas cerradas D-06, D-07, D-10, D-14 y D-15 cuando se implementen sus historias.
5. Ejecutar las pruebas de aceptación de cada HU y registrar evidencia; no confundir revisión documental con validación funcional.
