# Plan maestro de desarrollo — FUGA+

**Proyecto:** FUGA+ — aplicación móvil para el control de gastos personales y la detección explicable de posibles fugas de dinero.  
**Documento:** Plan maestro de desarrollo.  
**Fecha:** 25 de octubre de 2026.  
**Estado:** Plan aprobado para ejecución; las decisiones D-01 a D-16 conservan el estado indicado en la sección F.  
**Restricción:** 12 semanas efectivas, una persona, dedicación estimada de 6 horas semanales.  
**Alcance comprometido:** 13 historias Must Have.

---

## Convenciones

- **[DEFINIDO]:** decisión o dato ya presente en la documentación del repositorio.
- **[PROPUESTA]:** decisión de planificación de este documento, todavía no aprobada.
- **[SUPUESTO]:** condición necesaria que no está cuantificada en los documentos.
- **[PENDIENTE]:** decisión abierta que bloquea o condiciona la implementación.

**Fuentes principales:** `README.md`, `docs/respuestas-ia/salida-historias-usuario.md`, `docs/respuestas-ia/salida-requerimientos-priorizados.md`, `docs/entrevista-real.md` y los diagramas de `docs/diagramas/`.

---

## A. Resumen, supuestos y criterios del plan

### A.1 Objetivo

Construir y verificar un MVP móvil de FUGA+ en 12 semanas efectivas, con una persona y una dedicación estimada de **6 horas semanales**, sin incorporar funcionalidades opcionales como obligatorias.

El MVP debe demostrar el flujo completo:

> Visitante → registro o inicio de sesión → gasto escrito en lenguaje natural → «Procesar con IA» con diccionario y reglas deterministas → revisión y corrección → guardado bajo el propietario → historial → dashboard → posible fuga con evidencia → cierre de sesión.

### A.2 Restricciones y supuestos

| ID | Supuesto | Consecuencia si no se cumple |
|---|---|---|
| **S-01** | Una persona, 12 semanas efectivas, ~6 h/semana = **~72 h totales**. | El plan debe reestimarse o reducirse el alcance. |
| **S-02** | React Native + TypeScript, Python + FastAPI y MongoDB Atlas M0 están disponibles desde la semana 1. | Habría que resolver infraestructura antes de iniciar. |
| **S-03** | El MVP usa correo y contraseña; Google queda fuera. | Si Google fuera obligatorio, se reduce otra parte del alcance. |
| **S-04** | El MVP no incluye panel administrativo, voz, push, Cloudinary, recuperación de contraseña ni metas. | Si la evaluación exige alguna, el plan debe replantearse. |
| **S-05** | El procesamiento es determinista, en backend, sin API externa de IA ni modelo entrenado. | Cambiaría la arquitectura, la privacidad y las pruebas. |
| **S-06** | D-09 se aprueba antes de la semana 2; D-02, D-03, D-04, D-05 y D-15 antes de la semana 3; D-01 antes de la semana 7. | Las historias bloqueadas no pueden implementarse ni probarse; no se inventarán valores. |
| **S-07** | Existe una forma segura de crear una cuenta administrativa de prueba, aunque no exista panel administrativo. | No se podría verificar que el Administrador no accede a gastos individuales. |
| **S-08** | Los datos de demostración son sintéticos. | Se requeriría tratamiento adicional de privacidad y consentimiento. |
| **S-09** | El proveedor de despliegue no está definido; para la demostración basta ejecución local y Atlas M0, salvo que la entrega académica exija una URL pública. | Sería necesario añadir una tarea de despliegue no prevista. |

### A.3 Principios del plan

1. **Must primero.** Solo las 13 historias Must Have forman el compromiso del MVP.
2. **Seguridad transversal.** HU-33 y los RNF de seguridad se implementan desde la semana 1, no al final.
3. **Nada inventado.** Los umbrales de fugas, categorías, moneda, fechas y límites del parser provienen de decisiones aprobadas; si faltan, la historia queda bloqueada.
4. **Sin IA externa.** El componente llamado «Procesar con IA» es un diccionario y un motor de reglas deterministas, versionados y explicables.
5. **Opcional no es obligatorio.** Should, Could y Won't no se convierten en requisitos del MVP. La semana 11 es la única ventana opcional y puede usarse como colchón.
6. **Criterio de terminado verificable.** Una historia no está terminada porque exista una pantalla: debe funcionar en backend, persistir, cumplir sus criterios de aceptación y pasar sus pruebas.

### A.4 Definición de terminado por historia Must

Una historia Must se considera terminada cuando:

- Su flujo funciona de extremo a extremo en el entorno integrado.
- Sus criterios de aceptación documentados se verifican con datos de prueba.
- Tiene pruebas reproducibles del backend y, cuando aplica, del cliente.
- Respeta el aislamiento por propietario y no expone datos sensibles en logs.
- No introduce llamadas a APIs externas de IA.
- Su documentación y sus decisiones asociadas están actualizadas.
- No tiene defectos críticos abiertos.

### A.5 Resumen ejecutivo

| Indicador | Valor |
|---|---:|
| Semanas efectivas | 12 |
| Dedicación estimada | ~6 h/semana |
| Presupuesto total | ~72 h |
| Historias Must comprometidas | 13 |
| Historias Should fuera del baseline | 9 |
| Historias Could fuera del MVP | 9 |
| Historias Won't | 2 |
| Horas hasta el congelamiento del MVP | 56 h |
| Colchón, ventana opcional y cierre | 16 h |
| Congelamiento del MVP | Semana 9 |
| Entrega candidata | Semana 12 |

---

## B. Alcance del MVP

### B.1 Historias incluidas: 13 Must Have [DEFINIDO]

| HU | RF | Resultado esperado |
|---|---|---|
| HU-01 | RF-001 | Pantalla pública con acceso a registro e inicio de sesión. |
| HU-02 | RF-002 | Registro e inicio de sesión con correo y contraseña. |
| HU-04 | RF-004 | Cierre de sesión seguro. |
| HU-10 | RF-010 | Entrada de un gasto en lenguaje natural. |
| HU-11 | RF-011 | Procesamiento determinista y borrador editable. |
| HU-12 | RF-012 | Revisión y corrección antes de guardar. |
| HU-13 | RF-013 | Guardado bajo el propietario y aislamiento. |
| HU-14 | RF-014 | Historial ordenado y paginado. |
| HU-20 | RF-020 | Total, cantidad y promedio por periodo. |
| HU-21 | RF-021 | Gasto por categoría y categoría principal. |
| HU-23 | RF-023 | Detección de posibles fugas con reglas deterministas. |
| HU-24 | RF-024 | Evidencia de una posible fuga. |
| HU-33 | RF-033 | Privacidad y aislamiento verificables en backend. |

**Total:** 13 historias Must, 13 RF Must y 13 RNF Must [DEFINIDO].

### B.2 Fuera del MVP: no comprometido

| Grupo | HU | RF | Tratamiento |
|---|---|---|---|
| Should Have | HU-03, HU-05, HU-07, HU-08, HU-15, HU-16, HU-30, HU-31, HU-32 | RF-003, 005, 007, 008, 015, 016, 030, 031, 032 | Fuera del baseline. Solo una porción podría evaluarse en la semana 11 si todo lo Must está verificado. |
| Could Have | HU-06, HU-09, HU-17, HU-18, HU-19, HU-22, HU-25, HU-26, HU-27 | RF-006, 009, 017, 018, 019, 022, 025, 026, 027 | Fuera del MVP. No se inician. |
| Won't Have | HU-28, HU-29 | RF-028, RF-029 | Postergadas. No se implementan. |

**Límites explícitos del MVP [DEFINIDO]:**

- Sin Google sign-in.
- Sin recuperación de contraseña.
- Sin edición ni eliminación posterior al guardado.
- Sin filtros de historial.
- Sin voz.
- Sin alertas, sugerencias ni resumen mensual.
- Sin metas.
- Sin panel administrativo.
- Sin notificaciones push.
- Sin Cloudinary ni fotos de perfil.
- Sin conexiones bancarias, pagos, transferencias, créditos o inversiones.

### B.3 Flujo de demostración

El guion de demostración debe cubrir, en orden:

1. Pantalla pública y registro.
2. Inicio de sesión.
3. Registro de un gasto por texto.
4. «Procesar con IA» y presentación del borrador.
5. Corrección de un campo.
6. Confirmación y guardado.
7. Historial.
8. Dashboard con total, cantidad, promedio y categoría principal.
9. Posible fuga con evidencia.
10. Intento de acceso a un gasto ajeno, rechazado.
11. Cierre de sesión.

### B.4 Reglas de recorte

Si el cronograma se retrasa:

1. Se cancela primero la ventana opcional de la semana 11.
2. Se usa el colchón de la semana 10.
3. Se reduce la profundidad de una Must sin eliminar privacidad ni aislamiento.
4. **No se recorta HU-33 ni la suite de seguridad.**
5. No se presenta como terminada una historia cuyos criterios no se hayan verificado.

---

## C. Arquitectura y componente de IA determinista

### C.1 Arquitectura conceptual [DEFINIDO]

Tres capas:

```text
App móvil React Native + TypeScript
        │ HTTPS/JSON + JWT
        ▼
Backend Python + FastAPI
  ├─ Autenticación y autorización
  ├─ Gestión de gastos
  ├─ Procesamiento determinista
  ├─ Dashboard y agregados
  ├─ Detección de fugas
  └─ Acceso a datos
        │
        ▼
MongoDB Atlas
  usuarios · categorias · gastos · posibles_fugas
```

**Regla de arquitectura:** la app nunca accede directamente a MongoDB Atlas ni contiene credenciales de servicios externos [DEFINIDO].

### C.2 Componentes del backend [PROPUESTA]

| Componente | Responsabilidad | HU/RF |
|---|---|---|
| Autenticación | Registro, login, logout, hash de contraseña, emisión y validación de JWT. | HU-02, HU-04; RF-002, RF-004 |
| Autorización | Obtener identidad de la sesión, verificar rol y propietario, denegar por defecto. | HU-33; RF-033 |
| Gestión de gastos | Validar, confirmar y persistir el gasto; idempotencia. | HU-13; RF-013 |
| Procesamiento determinista | Diccionario, extracción de campos, validación y borrador. | HU-10, HU-11; RF-010, RF-011 |
| Historial | Consulta paginada por propietario. | HU-14; RF-014 |
| Dashboard | Agregados por periodo y categoría. | HU-20, HU-21; RF-020, RF-021 |
| Motor de fugas | Evaluar reglas aprobadas y construir evidencia. | HU-23, HU-24; RF-023, RF-024 |
| Acceso a datos | Repositorios con filtro obligatorio por `usuarioId`. | HU-33; RF-033 |

### C.3 Modelo de datos [DEFINIDO como propuesta, no implementado]

| Colección | Campos principales | Observación |
|---|---|---|
| `usuarios` | `_id`, `nombre`, `apellido?`, `telefono?`, `correo`, `contrasenaHash`, `rol`, `estado`, `imagenPerfilUrl?` | `correo` único. |
| `categorias` | `_id`, `nombre` | Catálogo cerrado según D-02. |
| `gastos` | `_id`, `usuarioId`, `categoriaId`, `monto`, `moneda`, `descripcion`, `fecha`, `textoOriginal`, `versionDiccionario`, `versionReglas`, `fechaCreacion` | Orden por `fecha` y desempate por `fechaCreacion`. |
| `posibles_fugas` | `_id`, `usuarioId`, `categoriaId`, `descripcion`, `reglaId`, `versionRegla`, `cantidadOcurrencias`, `montoAcumulado`, `ventanaInicio`, `ventanaFin`, `fechaDeteccion`, `vigente` | Evidencia derivada de gastos; sin FK física. |
| `alertas` | No se implementa | RF-025 es Could y está fuera del MVP. |

**Índices propuestos [PROPUESTA]:**

- Único en `usuarios.correo`.
- Compuesto en `gastos`: `usuarioId + fecha`.
- Compuesto en `posibles_fugas`: `usuarioId + vigente`.
- Único en `categorias.nombre`.

**Idempotencia [PROPUESTA]:** añadir una clave de idempotencia por usuario en el guardado de gastos, para cumplir RNF-005 sin duplicar registros ante reintentos.

**Sesiones y revocación [PENDIENTE]:** el modelo ER no define colección de sesiones. Si D-09 exige revocación inmediata, se añadirá el mecanismo mínimo necesario; no se decide por suposición.

### C.4 Superficie de API [PROPUESTA]

| Método y ruta | Uso | HU |
|---|---|---|
| `POST /auth/register` | Registro con correo y contraseña. | HU-02 |
| `POST /auth/login` | Inicio de sesión y emisión de JWT. | HU-02 |
| `POST /auth/logout` | Cierre de sesión según D-09. | HU-04 |
| `POST /expenses/process` | Procesar texto y devolver borrador; no guarda. | HU-10, HU-11 |
| `POST /expenses` | Confirmar y guardar el gasto revisado. | HU-12, HU-13 |
| `GET /expenses` | Historial paginado del propietario. | HU-14 |
| `GET /analytics/summary` | Total, cantidad y promedio por periodo. | HU-20 |
| `GET /analytics/categories` | Desglose por categoría y categoría principal. | HU-21 |
| `GET /leaks` | Posibles fugas vigentes del propietario. | HU-23 |
| `GET /leaks/{id}` | Evidencia de una posible fuga. | HU-24 |
| `GET /health` | Verificación operativa. | Soporte |

No se incluyen endpoints de perfil, filtros, edición, eliminación, administración, voz, alertas ni metas.

### C.5 Autenticación y seguridad [DEFINIDO + PENDIENTE]

**Definido:**

- JWT para identificar la sesión.
- Contraseña con hash adaptativo, nunca en texto plano.
- Identidad del propietario tomada del token, no de un identificador enviado por el cliente.
- Rechazo de cuentas inactivas.
- Validación de entradas en backend.
- HTTPS en producción.
- Secretos en variables de entorno, nunca en el repositorio.
- Logs sin contraseñas, tokens, montos ni descripciones.

**Pendiente D-09:**

- Requisitos exactos de contraseña.
- Verificación de correo.
- Duración, renovación y revocación del JWT.
- Cierre de todas las sesiones.
- Límites de intentos.
- Proveedor de correo, si se implementara recuperación —fuera del MVP—.

No se nombra ni se elige un algoritmo, proveedor o servicio no documentado.

### C.6 Componente de interpretación determinista

**Nombre conceptual:** `AnalizadorGasto`, apoyado en `DiccionarioGasto` y `ReglaFuga` [DEFINIDO como diseño].

**Flujo [PROPUESTA]:**

```text
Texto original
  → normalización según D-05
  → extracción de monto (D-03)
  → extracción de fecha (D-04)
  → extracción de categoría (D-02)
  → extracción de descripción
  → validación de campos
  → borrador con texto original y versiones
```

**Reglas no negociables [DEFINIDO]:**

- El botón muestra exactamente «Procesar con IA».
- No se usa API externa de IA, modelo generativo ni entrenamiento propio.
- El procesamiento no guarda automáticamente.
- El usuario revisa y corrige antes de confirmar.
- Si un campo no se reconoce, queda vacío o pendiente de selección; no se inventa.
- Se registra `versionDiccionario` y `versionReglas` en el gasto.
- La etiqueta se explica con un texto transparente aprobado en D-15.
- El texto original se conserva.

**Criterios de prueba [PROPUESTA]:**

- Corpus de frases con monto, categoría, descripción y fecha esperados.
- Casos de monto ausente, formato inválido, categoría desconocida, fecha ambigua y texto vacío.
- Verificación de que no existe ninguna llamada de red a un proveedor de IA.
- Casos de varias frases o varios gastos según D-05; si D-05 no lo permite, se rechazan con un mensaje claro.

No se fija una métrica numérica de acierto porque el proyecto no la ha aprobado. La aceptación se basa en el corpus acordado y en la revisión humana.

### C.7 Detección de fugas

**Contrato de regla [PROPUESTA]:**

| Campo | Uso |
|---|---|
| `idRegla` | Identificador único. |
| `version` | Versión vigente. |
| `descripcion` | Explicación legible. |
| `evaluar()` | Determina si el patrón se cumple. |
| `explicar()` | Genera la evidencia para el usuario. |

**Evidencia [DEFINIDO]:** regla aplicada, ocurrencias, monto acumulado, periodo analizado y gastos que sustentan el resultado.

**Regla de bloqueo:** los umbrales, monto mínimo, frecuencia, ventana, agrupación y condición mínima de datos provienen de **D-01**. Sin esa decisión no se implementa ni se prueba HU-23/HU-24. **No se inventan valores para la demostración.**

**Estado de datos insuficientes [PROPUESTA]:** si no hay datos suficientes según D-01, la respuesta debe indicarlo y no generar una falsa fuga.

**Versionado [DEFINIDO]:** cada regla y cada versión del diccionario tienen identificador y vigencia; el gasto conserva la versión aplicada.

### C.8 Pruebas y observabilidad

| Nivel | Alcance | RNF |
|---|---|---|
| Unidad | Diccionario, extracción de campos, reglas, cálculos. | RNF-014 |
| Integración | Registro, login, procesamiento, guardado, historial, dashboard, fugas. | RNF-004, RNF-005, RNF-012 |
| Seguridad | Sin sesión, sesión de otro usuario, recurso ajeno, cuenta inactiva, token vencido, rol insuficiente. | RNF-001, RNF-003, RNF-007 |
| Agregados | Dataset conocido; total, promedio, categoría principal y evidencia. | RNF-006, RNF-013 |
| Aceptación | Matriz de las 13 Must y guion de demostración. | RNF-009 |
| Regresión | Repetición antes de cada entrega y al congelar el MVP. | RNF-014 |

**Observabilidad [PROPUESTA]:** logs estructurados con identificador de correlación, sin datos financieros ni credenciales. No se define proveedor de monitoreo.

### C.9 Despliegue y entornos

- **Desarrollo:** ejecución local de app y backend; Atlas M0 para persistencia [DEFINIDO].
- **Pruebas:** datos sintéticos y base separada o colecciones identificables [SUPUESTO].
- **Producción:** HTTPS obligatorio; proveedor no definido [PENDIENTE].
- **Secretos:** variables de entorno; sin claves en el repositorio [DEFINIDO].
- **Respaldos y retención:** dependen de D-06 [PENDIENTE].

---

## D. Plan de 12 semanas

### D.1 Puerta de entrada

Antes de la semana 2 debe estar aprobada:

- **D-09:** política de autenticación y sesión.

Antes de la semana 3 deben estar aprobadas:

- **D-02:** catálogo de categorías y tratamiento de «Otros».
- **D-03:** moneda, configuración regional, decimales y redondeo.
- **D-04:** zona horaria, formatos de fecha y definición de periodo.
- **D-05:** límites del parser, formatos, longitud y paginación.
- **D-15:** texto de transparencia de «Procesar con IA».

Antes de la semana 7 debe estar aprobada:

- **D-01:** reglas y umbrales de detección de fugas.

Si una decisión no está aprobada, la historia dependiente no se implementa ni se marca como terminada.

### D.2 Distribución semanal

**Presupuesto:** 72 h. **MVP:** 56 h hasta el congelamiento. **Colchón, opcional y cierre:** 16 h.

| Semana | Horas | Objetivo | HU / RF | Entregable | Criterio de salida |
|---|---:|---|---|---|---|
| **1** | 6 | Base técnica y decisiones mínimas | HU-01 base, HU-02 base, HU-33 base; RF-001, RF-002, RF-033 | App shell, API, conexión a Atlas, `health`, arnés de pruebas, contrato de autenticación, esqueleto de pruebas de seguridad | Entorno reproducible; app y API inician; decisiones D-02, D-03, D-04, D-05, D-09 y D-15 registradas |
| **2** | 6 | Autenticación y sesión | HU-01, HU-02, HU-04, HU-33; RF-001, 002, 004, 033 | Registro, login, logout, hash, JWT, rechazo de cuenta inactiva, pantallas pública y de acceso | **H1:** registro, inicio y cierre funcionan; acceso cruzado rechazado |
| **3** | 6 | Texto y procesamiento determinista | HU-10, HU-11; RF-010, 011 | Pantalla de entrada, endpoint de proceso, diccionario v1, reglas v1, corpus inicial, borrador sin guardado | El borrador devuelve campos reconocidos; etiqueta exacta; ninguna llamada a IA externa |
| **4** | 7 | Revisión y persistencia | HU-12, HU-13; RF-012, 013 | Vista editable, validaciones, confirmación explícita, propietario desde JWT, idempotencia, atomicidad | **H2:** flujo texto → revisión → guardado funciona; duplicados y fallos parciales controlados |
| **5** | 6 | Historial y decisión D-01 | HU-14; RF-014 | Historial paginado, orden descendente, estados vacío/carga/error, filtro por propietario | Historial correcto con datos de prueba; **D-01 aprobada** |
| **6** | 6 | Dashboard | HU-20, HU-21; RF-020, 021 | Total, cantidad, promedio, desglose por categoría y categoría principal | Cifras coinciden con el dataset de prueba; periodo y moneda según D-03/D-04 |
| **7** | 7 | Fugas y evidencia | HU-23, HU-24; RF-023, 024 | Motor con reglas aprobadas, versionado, evidencia, estado de datos insuficientes | **H3:** una fuga se explica con regla, ocurrencias, monto, ventana y gastos |
| **8** | 6 | Integración y seguridad | Todas las Must; HU-33; RF-033 | Flujo E2E, suite IDOR/BOLA, revisión de logs, manejo de errores, smoke de rendimiento | Sin defectos críticos de seguridad; flujo completo ejecutable |
| **9** | 6 | Estabilización y aceptación | 13 Must; RNF aplicables | Matriz de aceptación, regresión, OpenAPI, datos de demostración, guion | **H4:** MVP congelado; todas las Must verificadas o con riesgo documentado |
| **10** | 6 | Colchón de Must | Solo defectos Must | Corrección de defectos, cierre de brechas de aceptación, refuerzo de pruebas | Todas las Must verificadas; no se añade alcance |
| **11** | 4 | Opcional o colchón | No comprometido | Si todo lo Must está cerrado: una porción acotada de una Should, por ejemplo HU-15; si no, colchón | **H5 opcional:** la Should no compromete el MVP; no se inician Google, Cloudinary, correo, voz ni administración |
| **12** | 6 | Cierre y entrega | Sin historias nuevas | Regresión completa, revisión de seguridad, documentación, ensayo de demostración, limitaciones conocidas | **H6:** candidato de entrega sin defectos críticos |

### D.3 Hitos

| Hito | Semana | Criterio |
|---|---:|---|
| **H1 — Identidad y acceso** | 2 | Registro, login, logout, roles y aislamiento inicial. |
| **H2 — Núcleo de gastos** | 4 | Texto, procesamiento, revisión y guardado de extremo a extremo. |
| **H3 — Análisis** | 7 | Historial, dashboard y fugas con evidencia. |
| **H4 — MVP congelado** | 9 | Las 13 Must pasan la aceptación y la demostración. |
| **H5 — Should opcional** | 11 | Solo si H4 está cerrado; en caso contrario, colchón. |
| **H6 — Candidato de entrega** | 12 | Regresión, seguridad y demostración listas. |

### D.4 Comparación con el plan documentado

El documento de historias propone congelar el MVP en la semana 7 y dedicar las semanas 8–10 a Should. **[PROPUESTA]** Con ~6 h/semana, ese ritmo no es realista: este plan desplaza el congelamiento a la semana 9, elimina las Should del baseline y deja solo una ventana opcional de 4 h en la semana 11.

Si la dedicación real fuera mayor, podría recuperarse el plan documentado; si fuera menor, se aplican las reglas de recorte de la sección B.4.

### D.5 Cadencia semanal

- **Inicio:** revisar objetivo, dependencias y decisiones bloqueantes.
- **Mitad:** integrar y ejecutar pruebas; no acumular cambios.
- **Fin:** demostración interna, revisión de riesgos y ajuste del alcance.
- **Cada entrega:** regresión y suite de seguridad de HU-33.
- **Regla:** no se inicia una historia si su decisión bloqueante sigue pendiente.

---

## E. Trazabilidad y verificación

### E.1 Matriz de las 13 historias Must

| HU | RF | RNF principales | Semana | Evidencia de aceptación |
|---|---|---|---|---|
| HU-01 | RF-001 | RNF-009, RNF-010 | 1–2 | Pantalla pública sin sesión; acceso a registro/login; texto de transparencia aprobado. |
| HU-02 | RF-002 | RNF-001, 003, 004, 007, 008, 009 | 2 | Registro e inicio correctos; correo duplicado rechazado; credenciales inválidas rechazadas; cuenta inactiva rechazada. |
| HU-04 | RF-004 | RNF-003 | 2 | Logout invalida la sesión según D-09; ruta protegida rechazada después del cierre. |
| HU-10 | RF-010 | RNF-004, 009, 012 | 3 | Texto aceptado y conservado; texto vacío o excesivo rechazado según D-05. |
| HU-11 | RF-011 | RNF-004, 010, 014 | 3 | Borrador con monto, categoría, descripción y fecha cuando se reconocen; no guarda; versión registrada; sin API externa. |
| HU-12 | RF-012 | RNF-004, 009, 012 | 4 | Campos editables; validación por campo; confirmación explícita; advertencia al descartar. |
| HU-13 | RF-013 | RNF-001, 002, 005, 007 | 4 | Propietario desde JWT; acceso ajeno rechazado; doble envío no duplica; fallo no deja registro parcial. |
| HU-14 | RF-014 | RNF-001, 009, 012, 013 | 5 | Orden descendente; paginación; solo gastos propios; estados vacío/carga/error. |
| HU-20 | RF-020 | RNF-006, 009, 013 | 6 | Total, cantidad y promedio coinciden con el dataset; límites de periodo según D-04. |
| HU-21 | RF-021 | RNF-006, 009, 013 | 6 | Desglose por categoría; categoría principal; desempate según D-02. |
| HU-23 | RF-023 | RNF-006, 014 | 7 | Solo reglas aprobadas en D-01; versión registrada; estado de datos insuficientes; sin umbrales inventados. |
| HU-24 | RF-024 | RNF-001, 002, 006, 014 | 7 | Evidencia con regla, ocurrencias, monto acumulado, ventana y gastos; solo del propietario. |
| HU-33 | RF-033 | RNF-001, 002, 003, 007, 008 | 1–9 | Suite de acceso cruzado, recurso ajeno, rol insuficiente, cuenta inactiva y logs sin datos sensibles. |

### E.2 Cobertura de los RNF

| RNF | Semana | Evidencia |
|---|---:|---|
| RNF-001 | 1–9 | Middleware de sesión, filtro por propietario y pruebas de acceso cruzado. |
| RNF-002 | 4, 7, 8 | Respuestas mínimas; evidencia solo del propietario; administrador sin gastos individuales. |
| RNF-003 | 2, 8 | Hash, JWT, rechazo de cuenta inactiva, cierre de sesión y pruebas de token. |
| RNF-004 | 3, 4, 8 | Validación de tipo, formato, rango, longitud y catálogo. |
| RNF-005 | 4 | Idempotencia y atomicidad del guardado. |
| RNF-006 | 6, 7 | Agregados y fugas coherentes tras crear gastos; edición/borrado fuera del MVP. |
| RNF-007 | 1–9 | Revisión de logs sin tokens, contraseñas, montos ni descripciones. |
| RNF-008 | 1, 8 | HTTPS y secretos en variables de entorno. |
| RNF-009 | 2–7 | Estados vacío, carga, error y confirmación explícita. |
| RNF-010 | 3 | Etiqueta exacta y texto de transparencia D-15. |
| RNF-011 | 1–9 | Flujo de texto en Android e iOS; voz fuera del MVP. |
| RNF-012 | 3–5 | Errores de red, reintento y ausencia de estados parciales. |
| RNF-013 | 8 | Smoke con dataset representativo; umbrales pendientes de aprobación. |
| RNF-014 | 1–9 | Versiones de diccionario/reglas y pruebas reproducibles. |
| RNF-015 | Fuera del MVP | Solo aplica a administración Should; no se implementa auditoría. |
| RNF-016 | 8–9 | Política de retención documentada según D-06; sin operaciones destructivas en el MVP. |

### E.3 Trazabilidad de lo no incluido

| Grupo | HU | RF | Estado |
|---|---|---|---|
| Should | HU-03, 05, 07, 08, 15, 16, 30, 31, 32 | RF-003, 005, 007, 008, 015, 016, 030, 031, 032 | No comprometido; solo evaluación opcional en semana 11. |
| Could | HU-06, 09, 17, 18, 19, 22, 25, 26, 27 | RF-006, 009, 017, 018, 019, 022, 025, 026, 027 | Fuera del MVP. |
| Won't | HU-28, 29 | RF-028, 029 | Postergadas. |

### E.4 Lista de verificación para congelar el MVP

- [ ] Las 13 Must tienen evidencia de aceptación.
- [ ] La suite de seguridad demuestra aislamiento entre usuarios.
- [ ] El Administrador de prueba no accede a gastos individuales.
- [ ] El flujo de demostración se completa sin pasos manuales ocultos.
- [ ] El dashboard y las fugas se recalculan al crear un gasto.
- [ ] Los datos de prueba son sintéticos.
- [ ] No existe ninguna llamada a API externa de IA.
- [ ] Las decisiones pendientes están registradas y no se presentan como acordadas.
- [ ] No hay defectos críticos abiertos.
- [ ] La documentación de limitaciones está actualizada.

---

## F. Riesgos, decisiones abiertas y control de cambios

### F.1 Decisiones abiertas y momento límite

| ID | Decisión | Necesaria antes de | Efecto si no se resuelve |
|---|---|---|---|
| **D-01** | Umbrales, frecuencia, ventana, agrupación y condición mínima de fugas. | Semana 7 | HU-23/HU-24 no se pueden implementar ni probar. No se inventan valores. |
| **D-02** | Catálogo de categorías, «Otros» y desempate de categoría principal. | Semana 3 | Parser, dashboard y evidencia quedan indefinidos. |
| **D-03** | Moneda, configuración regional, decimales, límites y redondeo. | Semana 3 | Cálculos y formatos pueden requerir migración. |
| **D-04** | Zona horaria, formatos de fecha, periodos y fechas futuras. | Semana 3 | Historial, dashboard y fugas pueden ser incorrectos. |
| **D-05** | Límites del parser, formatos, longitud, varias frases y paginación. | Semana 3 | No hay criterios de borde para parser ni historial. |
| **D-09** | Contraseñas, verificación, vigencia/renovación/revocación de JWT, intentos y correo. | Semana 2 | La seguridad de sesión queda incompleta. |
| **D-15** | Texto público y explicación de «Procesar con IA». | Semana 3 | La interfaz puede generar expectativas engañosas. |
| **D-06** | Retención, desactivación, eliminación y respaldos. | Semana 8 | No se puede cerrar la política de privacidad ni operaciones destructivas. |
| **D-16** | Provisión de administradores y prevención del registro público de administradores. | Semana 8 | No hay vía segura para la cuenta administrativa de prueba. |
| **D-07** | Métricas administrativas y umbral mínimo de agregación. | Fuera del MVP | Bloquea HU-30/HU-31 si se promoten. |
| **D-08** | Alcance de metas. | Fuera del MVP | Bloquea HU-28/HU-29. |
| **D-10** | Vinculación de cuentas de Google. | Fuera del MVP | Bloquea HU-03/HU-09. |
| **D-11** | Notificaciones y recordatorios. | Fuera del MVP | Bloquea HU-25. |
| **D-12** | Alcance de voz. | Fuera del MVP | Bloquea HU-17 a HU-19. |
| **D-13** | Perfil, imagen y Cloudinary. | Fuera del MVP | Bloquea HU-07 a HU-09. |
| **D-14** | Administración, auditoría y último administrador. | Fuera del MVP | Bloquea HU-30 a HU-32 y RNF-015. |

### F.2 Riesgos priorizados

| Riesgo | Prob. | Impacto | Mitigación en este plan |
|---|---|---|---|
| **R-04:** alcance de 12 semanas demasiado grande para una persona. | Alta | Alto | 56 h para Must, 6 h de colchón, 4 h opcionales, congelamiento en semana 9 y recorte de opcionales. |
| **R-01:** el diccionario no cubre el español cotidiano. | Alta | Alto | Corpus inicial, pruebas de límites, borrador editable y revisión humana. |
| **R-02:** reglas de fuga con falsos positivos o negativos. | Alta | Alto | D-01 antes de implementar, pocas reglas explicables, evidencia y pruebas con fixtures. |
| **R-03:** fuga de datos entre usuarios. | Media | Crítico | Filtro por propietario, suite IDOR/BOLA y revisión de logs. |
| **R-09:** JWT válido después de desactivar una cuenta. | Media | Alto | Verificar estado de cuenta en cada solicitud o mecanismo de revocación según D-09. |
| **R-10:** errores de moneda, decimales o zona horaria. | Media | Alto | Resolver D-03/D-04 antes de la semana 3 y probar límites. |
| **R-13:** contradicciones documentales sobre IA y arquitectura. | Alta | Medio | Este plan usa las fuentes definitivas; la corrección documental se trata como tarea separada. |
| **R-15:** confiar en código generado por IA sin revisión. | Media | Alto | Revisión humana, pruebas y prohibición de inventar reglas de negocio. |
| **P-R01:** decisiones D-xx tardías. | Media | Alto | Puertas de decisión en semanas 1, 3, 5 y 8; la historia bloqueada no avanza. |
| **P-R02:** problemas de acceso a Atlas o al entorno. | Media | Medio | Verificación en semana 1; datos sintéticos y ejecución local. |
| **P-R03:** fallo de la demostración por red o entorno. | Media | Medio | Datos precargados, ensayo cronometrado y grabación de respaldo. |

Los riesgos R-01 a R-15 del documento de historias se conservan; esta tabla prioriza los que afectan directamente al plan de 72 h.

### F.3 Control de cambios

1. **Baseline:** solo las 13 Must.
2. **Nuevas ideas:** van al backlog, no al MVP.
3. **Cambio en una Must:** exige análisis de impacto en HU, RF, RNF y horas.
4. **Congelamiento:** después de la semana 9 no se añade alcance.
5. **Semana 11:** solo se usa si H4 está cerrado; en caso contrario, es colchón.
6. **Registro semanal:** decisiones, defectos, riesgos y cambios de alcance.
7. **Prohibición:** no se cambia un umbral, categoría, moneda o límite para “hacer que la demo funcione”.

### F.4 Criterios de éxito del plan

- Las 13 Must se demuestran de extremo a extremo.
- La privacidad y el aislamiento se verifican en backend.
- El componente «Procesar con IA» es determinista, versionado y transparente.
- Las fugas se explican con evidencia y reglas aprobadas, sin valores inventados.
- El MVP se congela en la semana 9 y se entrega en la semana 12.
- Las funcionalidades opcionales no se presentan como obligatorias ni como terminadas.

---

## G. Estructura técnica del proyecto

**Alcance de esta sección.** Define la estructura de carpetas, las pantallas y las herramientas con las que se implementará el MVP. Es una estructura objetivo, **no implementación**: no se crean carpetas ni se escribe código en esta fase.

**Etiquetas usadas en los árboles:**

- **[EXISTE]:** ya está en el repositorio y se conserva.
- **[PROPUESTA]:** carpeta o archivo nuevo por crear.
- **[PENDIENTE]:** el archivo puede crearse, pero su contenido depende de una decisión D-xx no aprobada.

**Estado actual relevante:**

- `[EXISTE]` `docs/`, `.gitignore`, `README.md`, `opencode.json`, `mcp.json`.
- `[EXISTE]` `agents/`, `core/`, `skills/`, `tools/`, `interfaces/`, `config/` y `evaluations/`: esqueleto del framework de agentes, ajeno a FUGA+. No se reutiliza, no se elimina y no se mezcla con el backend.
- **No existe** `package.json`, `requirements.txt`, `tsconfig.json`, `app.json` ni ninguna carpeta de aplicación.
- `interfaces/api/main.py` es un docstring de una línea; no es la aplicación FastAPI de FUGA+.
- `.gitignore` cubre Python, pero no `node_modules/`, `.expo/`, `dist/` ni `coverage/`.

**Decisión de organización:** la aplicación se crea en dos carpetas nuevas de primer nivel, `backend/` y `mobile/`, sin mover ni renombrar el esqueleto existente.

---

### G.1 Estructura de carpetas del backend (FastAPI)

#### G.1.1 Árbol

```text
backend/                                      # [PROPUESTA] API y lógica de FUGA+
├── app/
│   ├── main.py                               # [PROPUESTA] crea FastAPI, monta routers y manejadores de error
│   ├── api/
│   │   ├── deps.py                           # sesión, usuario actual y propietario; deniega por defecto (HU-33)
│   │   └── v1/
│   │       ├── router.py                     # agrupa los routers bajo /api/v1
│   │       ├── auth.py                       # registro, login y logout (HU-02, HU-04; RF-002, RF-004)
│   │       ├── expenses.py                   # procesar, guardar e historial (HU-10–HU-14; RF-010–RF-014)
│   │       ├── analytics.py                  # resumen y categorías (HU-20, HU-21; RF-020, RF-021)
│   │       ├── leaks.py                      # fugas y evidencia (HU-23, HU-24; RF-023, RF-024)
│   │       └── health.py                     # verificación operativa
│   ├── core/
│   │   ├── config.py                         # Settings y variables de entorno (pydantic-settings) [PROPUESTA]
│   │   ├── database.py                       # cliente pymongo, ping e índices [PROPUESTA]
│   │   ├── security/
│   │   │   ├── passwords.py                  # hash y verificación de contraseña (RNF-003)
│   │   │   ├── tokens.py                     # emisión y validación de JWT (RNF-003)
│   │   │   └── authorization.py              # rol, propietario y denegación por defecto (HU-33)
│   │   ├── errors.py                         # errores de dominio sin filtrar datos sensibles (RNF-007)
│   │   └── logging.py                        # logs estructurados sin montos ni credenciales (RNF-007)
│   ├── schemas/
│   │   ├── auth.py                           # registro, login y respuesta de sesión (HU-02, HU-04)
│   │   ├── expense.py                        # borrador, confirmación e historial (HU-10–HU-14)
│   │   ├── analytics.py                      # resumen y desglose por categoría (HU-20, HU-21)
│   │   ├── leak.py                           # fuga y evidencia (HU-23, HU-24)
│   │   ├── processing.py                     # resultado del analizador y campos no reconocidos (HU-11)
│   │   └── common.py                         # paginación, error y salud
│   ├── services/
│   │   ├── auth_service.py                   # registro, credenciales y cierre (HU-02, HU-04)
│   │   ├── expense_service.py                # confirmación, propietario e idempotencia (HU-12, HU-13; RNF-005)
│   │   ├── processing_service.py             # invoca el analizador y arma el borrador (HU-11; RF-011)
│   │   ├── analytics_service.py              # agregados por periodo y categoría (HU-20, HU-21)
│   │   └── leak_service.py                   # evalúa reglas y arma evidencia (HU-23, HU-24)
│   ├── processing/
│   │   ├── analyzer.py                       # AnalizadorGasto; orquesta normalización y extracción (HU-11)
│   │   ├── normalization.py                  # normalización del texto según D-05
│   │   ├── extractors/
│   │   │   ├── amount.py                     # monto y decimales según D-03
│   │   │   ├── date.py                       # fecha y zona horaria según D-04
│   │   │   ├── category.py                   # categoría según D-02
│   │   │   └── description.py                # descripción restante del texto
│   │   └── dictionary/
│   │       ├── loader.py                     # carga y valida la versión vigente
│   │       └── v1/
│   │           ├── dictionary.json           # DiccionarioGasto; contenido [PENDIENTE] de D-02
│   │           └── metadata.json             # versión y vigencia del diccionario
│   ├── leaks/
│   │   ├── base_rule.py                      # contrato ReglaFuga: evaluar() y explicar()
│   │   ├── registry.py                       # registro y versión de reglas vigentes
│   │   └── rules/
│   │       └── README.md                     # reglas [PENDIENTE] de D-01; no se fijan umbrales
│   ├── repositories/
│   │   ├── base.py                           # filtro obligatorio por usuarioId (HU-33; RNF-001)
│   │   ├── users.py                          # usuarios por correo e identificador
│   │   ├── categories.py                     # catálogo cerrado según D-02
│   │   ├── expenses.py                       # gastos del propietario; historial paginado
│   │   └── leaks.py                          # fugas vigentes del propietario
│   └── utils/
│       ├── pagination.py                     # límites y cursores según D-05
│       └── periods.py                        # definición de periodo según D-04
├── seeds/
│   ├── categorias.json                       # catálogo [PENDIENTE] de D-02; no se inventan categorías
│   └── demo_gastos.json                      # datos sintéticos para pruebas y demostración
├── scripts/
│   ├── seed_categories.py                    # carga el catálogo aprobado
│   └── seed_demo_data.py                     # genera datos sintéticos de demostración
├── tests/
│   ├── conftest.py                           # fixtures, base de pruebas y cliente HTTP
│   ├── unit/
│   │   ├── test_analyzer.py                  # normalización, extracción y borrador (HU-11)
│   │   ├── test_extractors.py                # montos, fechas, categorías y descripción (HU-10, HU-11)
│   │   ├── test_rules.py                     # contrato de reglas y evidencia (HU-23, HU-24)
│   │   └── test_analytics.py                 # total, promedio y desglose (HU-20, HU-21)
│   ├── integration/
│   │   ├── test_auth.py                      # registro, login y logout (HU-02, HU-04)
│   │   ├── test_expenses.py                  # procesar, revisar y guardar (HU-10–HU-13)
│   │   ├── test_history.py                   # orden y paginación (HU-14)
│   │   ├── test_analytics.py                 # agregados con dataset conocido (HU-20, HU-21)
│   │   └── test_leaks.py                     # fugas y evidencia con D-01 (HU-23, HU-24)
│   ├── security/
│   │   ├── test_isolation.py                 # acceso cruzado entre usuarios (HU-33)
│   │   ├── test_roles.py                     # rol insuficiente y administrador sin gastos (HU-33)
│   │   ├── test_sessions.py                  # token ausente, vencido o de cuenta inactiva (HU-02, HU-04)
│   │   └── test_logs.py                      # ausencia de datos sensibles en logs (RNF-007)
│   └── fixtures/
│       ├── corpus_frases.json                # frases y resultados esperados del analizador
│       └── synthetic_expenses.json           # gastos sintéticos para agregados y fugas
├── .env.example                              # variables requeridas, sin secretos reales
├── requirements.txt                          # dependencias Python fijadas
├── pytest.ini                                # configuración de pruebas
└── README.md                                 # ejecución local, variables y pruebas
```

#### G.1.2 Correspondencia con los componentes de C.2

| Componente de C.2 | Rutas | HU / RF |
|---|---|---|
| Autenticación | `api/v1/auth.py`, `services/auth_service.py`, `core/security/passwords.py`, `core/security/tokens.py` | HU-02, HU-04; RF-002, RF-004 |
| Autorización | `api/deps.py`, `core/security/authorization.py`, `repositories/base.py` | HU-33; RF-033 |
| Gestión de gastos | `api/v1/expenses.py`, `services/expense_service.py`, `schemas/expense.py` | HU-12, HU-13; RF-012, RF-013 |
| Procesamiento determinista | `processing/analyzer.py`, `processing/normalization.py`, `processing/extractors/`, `processing/dictionary/` | HU-10, HU-11; RF-010, RF-011 |
| Historial | `api/v1/expenses.py` (GET), `services/expense_service.py`, `repositories/expenses.py` | HU-14; RF-014 |
| Dashboard | `api/v1/analytics.py`, `services/analytics_service.py` | HU-20, HU-21; RF-020, RF-021 |
| Motor de fugas | `leaks/base_rule.py`, `leaks/registry.py`, `leaks/rules/`, `services/leak_service.py` | HU-23, HU-24; RF-023, RF-024 |
| Acceso a datos | `core/database.py`, `repositories/` | HU-33; RF-033 |

#### G.1.3 Reglas estructurales del backend

1. **Propietario desde la sesión.** `api/deps.py` obtiene el `usuarioId` del JWT validado; ningún esquema de entrada acepta `usuarioId` como campo libre (HU-13, HU-33).
2. **Repositorios sin consultas globales.** Todo método de `repositories/` recibe el propietario y lo aplica al filtro; no existe un `find_all` sin usuario (RNF-001).
3. **Procesar no guarda.** `POST /expenses/process` solo devuelve un borrador; la persistencia ocurre en `POST /expenses` tras la confirmación (HU-11, HU-12).
4. **Reglas y diccionario versionados.** Cada archivo de `processing/dictionary/v1/` y cada regla de `leaks/rules/` declara versión y vigencia; el gasto conserva las versiones aplicadas (RNF-014).
5. **Decisiones pendientes, contenido vacío.** `dictionary.json`, `seeds/categorias.json` y `leaks/rules/` no reciben valores hasta que D-02 y D-01 se aprueben. Un archivo `[PENDIENTE]` puede existir como marcador, nunca con datos inventados.
6. **Sin módulos fuera del MVP.** No se crean carpetas de voz, Google, administración, metas, alertas, Cloudinary ni notificaciones.
7. **Secretos fuera del repositorio.** `.env` ya está ignorado; solo se versiona `.env.example` (RNF-008).
8. **El esqueleto existente no se toca.** `interfaces/api/main.py`, `core/`, `agents/`, `skills/` y `tools/` permanecen como están; el backend de FUGA+ vive en `backend/`.

---

### G.2 Estructura de carpetas del frontend (React Native + TypeScript)

#### G.2.1 Árbol

```text
mobile/                                       # [PROPUESTA] aplicación móvil FUGA+
├── App.tsx                                   # [PROPUESTA] monta AuthProvider y RootNavigator
├── app.json                                  # configuración de la app (nombre, slug, orientación)
├── package.json                              # dependencias y scripts de Node
├── tsconfig.json                             # configuración de TypeScript
├── babel.config.js                           # transformación del proyecto [PROPUESTA]
├── jest.config.js                            # configuración de pruebas [PROPUESTA]
├── .env.example                              # EXPO_PUBLIC_API_URL, sin secretos
├── src/
│   ├── navigation/
│   │   ├── RootNavigator.tsx                 # elige pila pública o autenticada según la sesión
│   │   ├── PublicStack.tsx                   # Public → Register → Login (HU-01, HU-02)
│   │   ├── AppTabs.tsx                       # Gasto, Historial, Dashboard y Fugas
│   │   ├── AppStack.tsx                      # tabs + revisión + evidencia (HU-12, HU-24)
│   │   └── types.ts                          # rutas y parámetros tipados
│   ├── screens/
│   │   ├── PublicScreen.tsx                  # información pública y accesos (HU-01; RF-001)
│   │   ├── RegisterScreen.tsx                # registro con correo y contraseña (HU-02; RF-002)
│   │   ├── LoginScreen.tsx                   # inicio de sesión (HU-02; RF-002)
│   │   ├── NewExpenseScreen.tsx              # texto y «Procesar con IA» (HU-10, HU-11; RF-010, RF-011)
│   │   ├── ReviewExpenseScreen.tsx           # borrador editable y confirmación (HU-12, HU-13; RF-012, RF-013)
│   │   ├── HistoryScreen.tsx                 # historial paginado (HU-14; RF-014)
│   │   ├── DashboardScreen.tsx               # total, promedio, categorías (HU-20, HU-21; RF-020, RF-021)
│   │   ├── LeaksScreen.tsx                   # posibles fugas (HU-23; RF-023)
│   │   └── LeakEvidenceScreen.tsx            # evidencia de una fuga (HU-24; RF-024)
│   ├── components/
│   │   ├── AppButton.tsx                     # botón con estado de carga y deshabilitado
│   │   ├── AppInput.tsx                      # entrada con etiqueta y error
│   │   ├── FormField.tsx                     # campo editable del borrador (HU-12)
│   │   ├── LoadingState.tsx                  # estado de carga (RNF-009)
│   │   ├── EmptyState.tsx                    # estado vacío (RNF-009)
│   │   ├── ErrorState.tsx                    # error con reintento (RNF-009, RNF-012)
│   │   ├── ExpenseCard.tsx                   # ítem del historial (HU-14)
│   │   ├── CategoryBreakdown.tsx             # desglose por categoría (HU-21)
│   │   ├── LeakCard.tsx                      # resumen de una posible fuga (HU-23)
│   │   ├── EvidenceList.tsx                  # regla, ocurrencias y gastos (HU-24)
│   │   └── LogoutButton.tsx                  # cierre de sesión (HU-04; RF-004)
│   ├── services/
│   │   ├── apiClient.ts                      # fetch, base URL, JWT, timeout y errores
│   │   ├── authService.ts                    # register, login y logout (HU-02, HU-04)
│   │   ├── expenseService.ts                 # process, create e historial (HU-10–HU-14)
│   │   ├── analyticsService.ts               # resumen y categorías (HU-20, HU-21)
│   │   └── leakService.ts                    # fugas y evidencia (HU-23, HU-24)
│   ├── auth/
│   │   ├── AuthContext.tsx                   # estado global de sesión y usuario
│   │   ├── useAuth.ts                        # hook de acceso a la sesión
│   │   └── tokenStorage.ts                   # almacenamiento seguro del JWT (expo-secure-store) [PROPUESTA]
│   ├── types/
│   │   ├── auth.ts                           # usuario, credenciales y sesión
│   │   ├── expense.ts                        # gasto, borrador y página de historial
│   │   ├── analytics.ts                      # resumen y desglose por categoría
│   │   ├── leak.ts                           # fuga y evidencia
│   │   └── api.ts                            # error normalizado y respuesta paginada
│   ├── utils/
│   │   ├── formatCurrency.ts                 # moneda, decimales y redondeo según D-03
│   │   ├── formatDate.ts                     # fecha y zona horaria según D-04
│   │   ├── validation.ts                     # validación previa del formulario (RNF-004)
│   │   └── errors.ts                         # mensajes de error sin datos sensibles
│   └── theme/
│       ├── colors.ts                         # paleta de la interfaz
│       └── spacing.ts                        # espaciado y tamaños base
└── __tests__/
    ├── utils/formatCurrency.test.ts          # formato de moneda (D-03)
    ├── utils/formatDate.test.ts              # formato de fecha (D-04)
    ├── auth/AuthContext.test.tsx             # restauración y cierre de sesión (HU-02, HU-04)
    ├── screens/ReviewExpenseScreen.test.tsx  # edición y confirmación (HU-12)
    ├── screens/HistoryScreen.test.tsx        # carga, vacío y error (HU-14; RNF-009)
    └── services/apiClient.test.ts            # JWT, 401 y errores de red (RNF-012)
```

#### G.2.2 Pantallas del MVP y justificación

| Pantalla | HU | RF | Ruta de navegación |
|---|---|---|---|
| `PublicScreen` | HU-01 | RF-001 | Pila pública |
| `RegisterScreen` | HU-02 | RF-002 | Pila pública |
| `LoginScreen` | HU-02 | RF-002 | Pila pública |
| `NewExpenseScreen` | HU-10, HU-11 | RF-010, RF-011 | Pestaña «Gasto» |
| `ReviewExpenseScreen` | HU-12, HU-13 | RF-012, RF-013 | Pila autenticada, sobre «Gasto» |
| `HistoryScreen` | HU-14 | RF-014 | Pestaña «Historial» |
| `DashboardScreen` | HU-20, HU-21 | RF-020, RF-021 | Pestaña «Dashboard» |
| `LeaksScreen` | HU-23 | RF-023 | Pestaña «Fugas» |
| `LeakEvidenceScreen` | HU-24 | RF-024 | Pila autenticada, sobre «Fugas» |

**Cobertura de las 13 Must:**

- **HU-04 (logout):** no tiene pantalla propia; se ejecuta con `LogoutButton` en el encabezado de las pantallas autenticadas.
- **HU-13 (propietario) y HU-33 (aislamiento):** no tienen pantalla; se verifican en backend y en el manejo del token.
- Las 9 pantallas cubren las 11 historias restantes; no se agregan pantallas de perfil, filtros, edición, administración, voz, alertas ni metas.

#### G.2.3 Comunicación con el backend

**Cliente HTTP.**

- `apiClient.ts` usa `fetch` nativo, sin librería adicional.
- La URL base proviene de `EXPO_PUBLIC_API_URL`; no se codifican URLs ni secretos.
- Cada solicitud envía `Content-Type: application/json` y `Authorization: Bearer <token>`.
- Se aplica un tiempo límite con `AbortController` y se normalizan los errores de red, validación y autorización.
- Los mensajes de error no incluyen tokens, montos ni descripciones en consola o logs.

**Manejo del JWT.**

- `AuthContext` conserva la sesión en memoria y `tokenStorage` la guarda con `expo-secure-store` `[PROPUESTA]`; no se usa `AsyncStorage` para el token (RNF-003).
- Al iniciar la app se intenta restaurar el token; si no existe o es inválido, `RootNavigator` muestra la pila pública.
- Un `401` limpia la sesión y devuelve al login; el comportamiento exacto de revocación depende de **D-09**.
- El token nunca se pasa como parámetro de navegación ni se escribe en la URL.
- El cierre de sesión llama a `POST /auth/logout` y elimina el token local; la revocación efectiva se ajusta a D-09.

**Estados de interfaz.**

| Estado | Comportamiento | RNF |
|---|---|---|
| Carga | Indicador y bloqueo de acciones que puedan duplicar el envío. | RNF-009, RNF-012 |
| Vacío | Mensaje explicativo, sin inventar datos ni ceros engañosos. | RNF-009 |
| Error | Mensaje comprensible y acción de reintento cuando el fallo es recuperable. | RNF-009, RNF-012 |
| Éxito | Confirmación explícita antes de navegar; el gasto no se guarda sin confirmación. | HU-12, RNF-009 |

**Contratos por pantalla.**

| Pantalla | Llamada | Observación |
|---|---|---|
| `PublicScreen` | Ninguna | Solo navegación a registro e inicio de sesión. |
| `RegisterScreen` | `POST /auth/register` | Valida campos antes de enviar; el backend vuelve a validar. |
| `LoginScreen` | `POST /auth/login` | Guarda el token y pasa a la pila autenticada. |
| `NewExpenseScreen` | `POST /expenses/process` | No guarda; entrega el borrador a la revisión. |
| `ReviewExpenseScreen` | `POST /expenses` | Envía solo los campos corregidos y la clave de idempotencia; el propietario lo pone el backend. |
| `HistoryScreen` | `GET /expenses` | Paginación y orden según D-05 y D-04. |
| `DashboardScreen` | `GET /analytics/summary` y `GET /analytics/categories` | Dos consultas; el periodo se elige con los valores aprobados en D-04. |
| `LeaksScreen` | `GET /leaks` | Solo fugas vigentes del propietario. |
| `LeakEvidenceScreen` | `GET /leaks/{id}` | Si el recurso no pertenece al usuario, el backend responde denegado. |

**Reglas del cliente.**

1. La app no accede a MongoDB ni contiene credenciales de servicios externos.
2. Las validaciones del cliente son de experiencia; la autorización y la validación definitiva están en el backend (RNF-004).
3. `formatCurrency.ts` y `formatDate.ts` no fijan moneda, configuración regional ni zona horaria: reciben esos valores de la configuración aprobada en D-03 y D-04.
4. No se implementan pantallas ni servicios de voz, Google, administración, metas, alertas o Cloudinary.

---

### G.3 Herramientas y tecnologías

#### G.3.1 Herramientas del proyecto

| Herramienta | Etiqueta | Para qué sirve | ¿Indispensable? |
|---|---|---|---|
| Git + GitHub | `[EXISTE]` | Control de versiones e historial del repositorio. | Sí |
| VS Code | `[DEFINIDO]` en README §9 | Edición y depuración del código. El editor concreto es sustituible. | Sí, la función |
| Python 3.12 | `[EXISTE]` en el entorno (referencia en `mcp.json`) | Ejecutar el backend y las pruebas. | Sí |
| `pip` + `venv` | `[PROPUESTA]` | Instalar dependencias y aislar el entorno Python. | Sí |
| Node.js LTS + `npm` | `[PROPUESTA]` | Ejecutar React Native, instalar paquetes y correr Jest. | Sí |
| Android Studio + SDK y emulador | `[DEFINIDO]` en README §9 | Compilar y ejecutar la app en Android. | Sí, para Android |
| Expo CLI (`npx expo`) | `[PROPUESTA]` | Iniciar y compilar la app si se adopta el flujo administrado de Expo. | Sí, si se aprueba Expo |
| MongoDB Atlas M0 | `[DEFINIDO]` en README §9 | Persistencia documental en la nube. | Sí |
| Swagger UI / OpenAPI | `[DEFINIDO]` en README §9 | Documentar y probar los endpoints; FastAPI lo genera. | Sí |
| `pytest` | `[PROPUESTA]` | Pruebas unitarias, de integración y de seguridad del backend. | Sí |
| `httpx` | `[PROPUESTA]` | Cliente de pruebas HTTP para FastAPI. | Sí |
| Jest + React Native Testing Library | `[PROPUESTA]` | Pruebas de componentes, hooks y utilidades del cliente. | Sí |
| TypeScript | `[DEFINIDO]` en README §9 | Tipado del cliente y verificación en compilación. | Sí |
| MongoDB Compass | `[PROPUESTA]` | Inspección visual de colecciones y documentos durante el desarrollo. | No, opcional |
| Postman | `[DEFINIDO]` en README §9 | Pruebas manuales de API; Swagger ya cubre el mismo uso. | No, opcional |
| ESLint + Prettier | `[PROPUESTA]` | Consistencia de estilo; no aporta funcionalidad del MVP. | No, opcional |
| OpenCode | `[EXISTE]` | Apoyo al análisis del repositorio y a la implementación. | No, opcional |
| CodeGraphContext | `[EXISTE]` | Exploración de relaciones y dependencias del código. | No, opcional |
| Context7 | `[DEFINIDO]` en README §9 | Consulta de documentación de bibliotecas. | No, opcional |

#### G.3.2 Herramientas y servicios excluidos

| Elemento | Motivo |
|---|---|
| Docker | El README no lo considera dependencia obligatoria del MVP. |
| Redis | Sin necesidad demostrable para el alcance Must. |
| Cloudinary | HU-08 y HU-09 están fuera del MVP. |
| Google Identity Services | HU-03 está fuera del MVP. |
| Expo Notifications / EAS push | HU-25 está fuera del MVP; el push remoto está postergado. |
| Kotlin / `SpeechRecognizer` | HU-17 a HU-19 están fuera del MVP. |
| Servicios de monitoreo o APM | No hay requisito que los exija; los logs estructurados cubren RNF-007. |
| Panel administrativo | HU-30 a HU-32 están fuera del MVP. |

#### G.3.3 Ajustes previos a la creación de carpetas

1. Ampliar `.gitignore` con `node_modules/`, `.expo/`, `dist/`, `coverage/` y archivos de entorno del cliente antes de crear `mobile/`. Es el único archivo existente que requiere ajuste, y se hará en la fase de implementación, no en esta sección.
2. Crear `backend/` y `mobile/` como carpetas nuevas; no mover ni renombrar `agents/`, `core/`, `interfaces/`, `skills/`, `tools/`, `config/` ni `evaluations/`.
3. No generar código de aplicación en esta fase: esta sección solo fija la estructura y las responsabilidades.
4. Mantener `[PENDIENTE]` todo contenido dependiente de D-01, D-02, D-03, D-04, D-05, D-09 y D-15 hasta su aprobación.

#### G.3.4 Verificación de la estructura

- [ ] `backend/` cubre los ocho componentes de C.2 sin duplicarlos.
- [ ] `mobile/` cubre las 9 pantallas y las 13 Must.
- [ ] Cada carpeta funcional cita al menos una HU o RF.
- [ ] No existe ninguna carpeta de voz, Google, administración, metas, alertas o Cloudinary.
- [ ] Los repositorios exigen `usuarioId` y la identidad proviene del JWT.
- [ ] El procesamiento no guarda y el guardado exige confirmación.
- [ ] Las reglas y el diccionario están versionados y bloqueados por D-01 y D-02.
- [ ] El token se guarda de forma segura y no se registra en logs.
- [ ] Las herramientas listadas son las mínimas para desarrollar, probar y administrar el MVP.
