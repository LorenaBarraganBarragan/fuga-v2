# PLAN MAESTRO DE IMPLEMENTACIÓN INTEGRAL — FUGA+

**Proyecto:** FUGA+ · Aplicación móvil de control de gastos personales
**Documento:** Plan Maestro de Implementación Integral (PMII)
**Versión:** 1.1.1 (revisión técnica de la versión 1.1)
**Fecha de elaboración:** 2026-11-13
**Fecha de revisión:** 2026-11-15
**Cambios de la versión 1.1:** incorporación de las 12 decisiones aprobadas C-01…C-12 (anexo D), registro de la decisión arquitectónica complementaria «FastAPI como puerta de acceso a los datos financieros» (§6.9) y auditoría de coherencia completa del documento.
**Cambios de la versión 1.1.1:** corrección de validación de fechas, separación de pruebas RLS frente a autorización del backend y aclaración de bloqueos de Supabase y cierre de fases. Sin cambios de alcance, tablas ni decisiones C-01…C-12.
**Modo de elaboración:** PLAN (sin implementación, sin commits, sin cambios de código)
**Modo de ejecución previsto:** BUILD (OpenCode, ejecución autónoma por fases)
**Línea base de requisitos:** `REQUERIMIENTOS.md` v3.0 + `HISTORIAS_DE_USUARIO.md` + 5 diagramas `.drawio`
**Ruta de destino en el repositorio:** `mi-framework-ia/docs/planificacion/PLAN_MAESTRO_IMPLEMENTACION_FUGA_PLUS.md`

---

## 0. Cómo usar este documento en BUILD

Este plan es un **contrato operativo**, no una descripción aspiracional. Cada fase (sección 20) es ejecutable de forma secuencial y verificable.

1. Ejecutar las fases **F0 → F14 en orden**. Una fase no inicia si su predecesora no cumple sus "condiciones de continuación".
2. Antes de cada fase, leer su bloque completo y el anexo correspondiente (A: API, B: DDL, C: diccionario, D: conflictos).
3. Al cerrar cada fase, actualizar `mi-framework-ia/docs/planificacion/PROGRESO_BUILD.md` (ver sección 25) con evidencia: comandos ejecutados, salida de pruebas, archivos creados.
4. Prohibido declarar una tarea "completada" sin prueba ejecutada y registrada.
5. Prohibido inventar funcionalidades, endpoints, tablas, pantallas o reglas que no estén en este plan o en la línea base.
6. Ante un bloqueo externo (credencial, servicio, dispositivo), registrar el bloqueo, continuar con el trabajo independiente y **no simular** la integración.
7. Los Should/Could/Won't **no** se implementan en la ola MVP; están en el anexo E como ampliaciones planificadas.
8. Las 12 decisiones aprobadas C-01…C-12 están en el anexo D y son **vinculantes**. No se reabren en BUILD; si aparece una contradicción nueva, se registra y se solicita aprobación.
9. Este documento **no** sustituye a `REQUERIMIENTOS.md` ni a `HISTORIAS_DE_USUARIO.md`: ante duda de alcance, mandan esos documentos y las decisiones D-01…D-15.
10. No se leen, citan, actualizan ni crean `README.md` como fuente de decisiones.

---

## 1. Resumen ejecutivo

FUGA+ es una aplicación móvil académica e individual para jóvenes y estudiantes que quieren **entender y controlar sus gastos personales**. Su propuesta central es registrar un gasto escribiéndolo en lenguaje natural («Hoy gasté $8.000 en un taxi»), interpretarlo con **reglas deterministas y diccionarios** (sin IA generativa externa), obligar a **revisar y confirmar** los campos y, con los gastos realmente guardados, producir **estadísticas** y **posibles fugas de dinero explicables con evidencia verificable**.

El repositorio contiene **solo documentación, diagramas, un esqueleto de framework de IA y el logo oficial**: no existe código de aplicación. Por tanto, el proyecto parte de cero en lo funcional, con una ventaja: la especificación está cerrada y es extraordinariamente detallada (33 RF, 16 RNF, 33 HU, 5 diagramas y 15 decisiones D-01…D-15).

**Alcance de esta ola:** 13 requerimientos Must Have que constituyen el MVP —
RF-001, RF-002, RF-004, RF-010, RF-011, RF-012, RF-013, RF-014, RF-020, RF-021, RF-023, RF-024 y RF-033.
Todo lo demás (Should/Could) queda especificado y planificado como ampliación, no se construye ahora.

**Arquitectura aprobada (no negociable):**

- Móvil: **React Native + TypeScript** sobre **Expo con development build** (no Expo Go, por el módulo nativo de voz).
- Backend: **FastAPI + Python** como API REST, única puerta de acceso a datos financieros.
- Datos: **PostgreSQL en Supabase**; identidad con **Supabase Auth** (sin JWT propio).
- Reglas deterministas en backend; **sin** MongoDB, Redis, Docker como dependencia, ni APIs de IA generativa.
- Voz: módulo nativo **Kotlin `SpeechRecognizer`** (solo Android, opcional).
- Integraciones: Supabase, Google Identity (Should), Cloudinary (Should), Expo Notifications locales (Could).

**Resultado esperado:** una aplicación instalable en Android que permite registrarse, iniciar sesión, registrar gastos por texto con revisión obligatoria, ver historial, ver estadísticas del periodo y consultar posibles fugas con su evidencia; con aislamiento estricto entre usuarios, pruebas automatizadas y build reproducible.

**Esfuerzo global estimado:** 15 fases, ~60–81 sesiones de agente de alcance medio (estimación relativa, no garantía de duración). La ruta crítica la marcan F1 (datos), F5–F6 (motor e idempotencia) y F14 (build Android), condicionada por la ausencia actual de Android SDK en la máquina.

**Bloqueo material conocido:** no hay Android SDK, `adb`, `emulator`, `gradle` ni `ANDROID_HOME`; solo existe JDK 23. El build Android real requiere instalar SDK + JDK 17/21 y aceptar licencias: es una **tarea manual de la propietaria** (sección 19). Hasta entonces, F0–F13 avanzan sin bloqueo y F14 queda parcialmente bloqueada.

---

## 2. Alcance del proyecto

### 2.1 Dentro del alcance (MVP, Must Have)

| Módulo | RF | HU | Resultado verificable |
|---|---|---|---|
| 1. Acceso y cuentas | RF-001, RF-002, RF-004 | HU-01, HU-02, HU-04 | Pantalla pública, registro, login por correo, cierre de sesión |
| 3. Registro y gestión de gastos | RF-010, RF-011, RF-012, RF-013, RF-014 | HU-10, HU-11, HU-12, HU-13, HU-14 | Texto → interpretación → revisión → guardado → historial |
| 5. Dashboard y estadísticas | RF-020, RF-021 | HU-20, HU-21 | Total, cantidad, promedio y desglose por categoría del periodo |
| 6. Detección de fugas | RF-023, RF-024 | HU-23, HU-24 | Candidatos FUGA-01 v1.0 con evidencia trazable |
| 8. Administración y privacidad | RF-033 (transversal) | HU-33 | Aislamiento por propietario probado en API y BD |

### 2.2 Fuera del alcance de esta ola (documentado, no construido)

- **Should Have:** RF-003 (Google), RF-005 (recuperación), RF-007 (perfil), RF-008 (foto), RF-015 (filtros), RF-016 (editar/eliminar), RF-030/031/032 (administración).
- **Could Have:** RF-006, RF-009, RF-017/018/019 (voz), RF-022 (comparación), RF-025 (alertas), RF-026 (sugerencias), RF-027 (resumen mensual).
- **Won't Have (for now):** RF-028, RF-029 (límite mensual).
- **Excluido por decisión:** MongoDB, JWT propio, Redis, Docker como dependencia de ejecución, IA generativa externa, push remoto, pagos, multi-moneda, OCR de facturas, exportación a PDF/Excel, biometría, modo offline con sincronización.

### 2.3 Límites explícitos

- No se promete funcionamiento en Expo Go (el módulo nativo de voz lo impide).
- No se promete iOS compilado: el código será compatible, pero la validación física se hará en Android (único entorno verificable con los recursos actuales).
- No se inventan umbrales de rendimiento: RNF-013 sigue sin cifras aprobadas; los objetivos son orientativos y se reportan mediciones reales sin declarar cumplimiento (anexo D, C-06).
- No se implementa borrado de cuentas ni de gastos desde la aplicación en el MVP (D-06, C-11); `deleted_at` existe en el modelo, inicia en `NULL`, no se usa y no se expone (C-10).
- La política de retención y el procedimiento administrativo de eliminación de datos personales están documentados en §16.9; la ausencia de un botón de eliminación **no** sustituye esas obligaciones (C-11).
- La aplicación no da asesoría financiera ni diagnósticos: el lenguaje está fijado por D-15.

---

## 3. Fuentes documentales y jerarquía

### 3.1 Jerarquía de autoridad (de mayor a menor)

1. **Decisiones cerradas D-01…D-15** (apartado «Especificación definitiva de decisiones de producto y arquitectura» de `REQUERIMIENTOS.md`). Son la última palabra cuando el cuerpo de una HU conserva frases antiguas del tipo «pendiente (D-xx)».
2. **`REQUERIMIENTOS.md` v3.0** (33 RF, 16 RNF, matriz de prioridades, matriz de trazabilidad HU↔RF).
3. **`HISTORIAS_DE_USUARIO.md`** (33 HU con CA-XX.Y, reglas R-XX.YY, dependencias y pruebas sugeridas).
4. **Los cinco diagramas** de `mi-framework-ia/docs/diagramas/` (ER, clases, componentes, casos de uso, historias), en tanto compatibles con 1–3.
5. **Recursos visuales oficiales**: `assets/logo/logo.png` y la paleta «Petrol Mint Vitality».
6. **Configuración técnica del entorno** (`mcp.json`, `opencode.json`, `opencode.jsonc`) para la auditoría de herramientas, nunca para decisiones de producto.

### 3.2 Documentos excluidos y por qué

| Documento | Motivo de exclusión |
|---|---|
| Cualquier `README.md` | Explícitamente desactualizado por el prompt maestro (§2.1). No se usa ni se modifica. |
| `mi-framework-ia/docs/architecture.md` | Placeholder vacío (0,2 KB) del framework, no arquitectura de FUGA+. |
| `mi-framework-ia/docs/manifest_schema.md` | Placeholder vacío (0,1 KB). |
| `mi-framework-ia/docs/entrevista-real.md` | Contexto de usuario (olvida registrar, quiere recordatorios). No es requisito; solo inspira lenguaje y tono. |
| `docs/respuestas-ia/salida-analisis-competitivo.md` | Material de apoyo, no línea base. |
| Pantallas antiguas de Google Stitch | Anteriores a los requisitos vigentes. Solo referencia estética (§4.5 del prompt). |

### 3.3 Verificación de inventario documental

| Elemento | Esperado | Verificado | Evidencia |
|---|---|---|---|
| Requerimientos funcionales | 33 | **33** (RF-001…RF-033) | Encabezados `### RF-` en `REQUERIMIENTOS.md` |
| Requerimientos no funcionales | 16 | **16** (RNF-001…RNF-016) | Encabezados `### RNF-` en `REQUERIMIENTOS.md` |
| Historias de usuario | 33 | **33** (HU-01…HU-33) | Encabezados `#### HU-` en `HISTORIAS_DE_USUARIO.md` |
| Módulos funcionales | 8 | **8** | Secciones 6.1–6.8 de `HISTORIAS_DE_USUARIO.md` |
| Diagramas | 5 | **5** `.drawio` | `docs/diagramas/` |
| Tablas propias del ER | — | **12** (7 MVP + 3 Should + 2 Won't) + `auth.users`, `auth.identities` | `diagrama-entidad-relacion.drawio` |
| Decisiones de diseño | 15 | **15 cerradas** (D-01…D-15) | `REQUERIMIENTOS.md` líneas 931–1011 |

### 3.4 Tratamiento de contradicciones

Toda contradicción detectada se documenta en el **anexo D** con: descripción, fuentes en conflicto, impacto y resolución. Desde la versión 1.1, las 12 decisiones C-01…C-12 están **aprobadas por la propietaria** y son vinculantes para BUILD; no quedan decisiones "por defecto" pendientes de validación.

Si durante BUILD aparece una contradicción nueva, **no se inventa una decisión**: se registra en `BLOQUEOS.md` con las fuentes en conflicto, se aplica la interpretación más conservadora que no amplíe alcance y se solicita aprobación antes de continuar en la parte afectada.

### 3.5 Regla de interpretación de las historias de usuario (C-05)

Las 33 historias de `HISTORIAS_DE_USUARIO.md` **no se modifican**. Algunas conservan en su cuerpo la fórmula histórica «pendiente (D-xx)»; esa fórmula **no reabre** ninguna decisión. La regla de interpretación es:

1. Las decisiones **D-01…D-15** de `REQUERIMIENTOS.md` y las decisiones **C-01…C-12** del anexo D de este plan prevalecen sobre cualquier frase antigua del cuerpo de una HU.
2. «Pendiente (D-xx)» se lee como «resuelto por D-xx» y no genera tarea, endpoint, tabla ni funcionalidad adicional.
3. La trazabilidad se conserva: cada HU mantiene sus CA y reglas; el plan indica en qué fase y con qué prueba se cubren.
4. Esta regla vive **exclusivamente** en el Plan Maestro; no se editan los documentos de requisitos ni las historias para "corregirlas".

---

## 4. Estado actual del repositorio

### 4.1 Inventario real (auditado)

```
fuga-v2/
├── assets/
│   └── logo/logo.png                 (500×500 px, RGBA, ~logo oficial)
├── mi-framework-ia/                  (framework de IA: agentes, core, skills, tools, evaluations, interfaces)
│   ├── agents/{coding_agent, research_agent}
│   ├── config/environments
│   ├── core/{agent_base, llm_gateway, memory, observability, orchestrator, security, skill_base}
│   ├── docs/
│   │   ├── architecture.md           (placeholder 0,2 KB)
│   │   ├── manifest_schema.md        (placeholder 0,1 KB)
│   │   ├── entrevista-real.md
│   │   ├── diagramas/*.drawio        (5 archivos)
│   │   ├── historias-usuario/HISTORIAS_DE_USUARIO.md
│   │   ├── prompts/*.md              (incluye este prompt maestro)
│   │   ├── requerimientos/REQUERIMIENTOS.md
│   │   └── respuestas-ia/
│   ├── evaluations/{agent_benchmarks, skill_tests}
│   ├── interfaces/, skills/, tools/
│   ├── mcp.json                      (CodeGraphContext)
│   ├── opencode.json                 (modificado localmente, sin commit)
│   └── README.md                     (EXCLUIDO)
└── (sin app/, sin backend/, sin mobile/, sin supabase/, sin package.json raíz, sin .gitignore raíz)
```

### 4.2 Conclusión de la auditoría

| Aspecto | Estado verificado |
|---|---|
| Código de aplicación | **Inexistente**. Cero archivos ejecutables de FUGA+. |
| Documentación funcional | **Completa y cerrada** (v3.0), con 33 RF / 16 RNF / 33 HU. |
| Diagramas | **5 presentes y legibles**; el ER usa etiquetas MVP/Should/Could/Won't por tabla. |
| Framework `mi-framework-ia` | **Esqueleto de framework de IA**, no runtime de la app. Se preserva intacto. |
| Control de versiones | Repositorio git con rama **`main`** únicamente y remoto `origin`. No existe `develop`. |
| Cambios sin commit | `mi-framework-ia/opencode.json` aparece modificado: **trabajo local de la propietaria, no tocar ni commitear**. |
| Logo | `assets/logo/logo.png` presente, 500×500 RGBA. Colores muestreados próximos a `#197570` / `#A8EFCF`; **no se modifica**. |
| `README.md` | Presentes, **excluidos** como fuente. No se actualizan ni se crean nuevos. |

### 4.3 Entorno técnico verificado

| Herramienta | Estado | Implicación |
|---|---|---|
| Node.js | **v24.16.0** | Compatible con Expo/CLI; fijar engine en `mobile/package.json`. |
| npm | **11.13.0** | Suficiente para instalar y usar `npx`. |
| Python | **3.12.6** | Compatible con FastAPI/Pydantic v2; fijar `requires-python = ">=3.12,<3.13"`. |
| Java | **solo JDK 23** (`C:\Program Files\Java\jdk-23`) | **Insuficiente/inestable** para AGP de React Native (requiere JDK 17 o 21). Debe instalarse JDK 17/21 y fijar `JAVA_HOME`. |
| Android SDK | **Ausente** (`%LOCALAPPDATA%\Android\Sdk` no existe) | No hay build ni instalación en dispositivo. Tarea manual. |
| `adb`, `emulator`, `sdkmanager`, `gradle`, `watchman` | **No encontrados** | Sin despliegue ni emulador. |
| `ANDROID_HOME` / `ANDROID_SDK_ROOT` | **Vacías** | Configuración manual pendiente. |
| Docker | **29.7.2 presente** | **No se usa**: el stack lo excluye como dependencia. |
| `supabase`, `psql`, `pg_dump` | **No instalados** | Usar `npx supabase` (vía npm) para migraciones; SQL se aplica contra el proyecto remoto. |
| `eas` | **No instalado** | Build local con Gradle; EAS queda como alternativa opcional. |
| `openssl` | **No disponible** | No se generan claves propias (Supabase Auth las gestiona). |
| npm global | `@mermaid-js/mermaid-cli@11.17.0`, `@opencode/cli@2.3.0` | Sin impacto en el stack. |

**Consecuencia directa:** el plan no puede depender de emulador ni de compilación Android en las fases tempranas. En F0–F13 pueden ejecutarse pruebas automatizadas de backend, pruebas de componentes y verificaciones estáticas de TypeScript **cuando sus dependencias estén disponibles**; las fases con criterios de aceptación de Supabase/BD/Auth requieren integración real y no se cierran solo con mocks o pruebas unitarias. F14 concentra el build Android real y queda **parcialmente bloqueada** hasta instalar el toolchain.

---

## 5. Requisitos y decisiones

### 5.1 Requerimientos Must Have (MVP) y su intención

| RF | Intención | Regla clave |
|---|---|---|
| RF-001 | Pantalla pública que explica FUGA+ y dirige a registro o login | Sin datos privados; logo y paleta oficiales |
| RF-002 | Registro e inicio de sesión con correo y contraseña | Supabase Auth; contraseña ≥ 8; sin JWT propio |
| RF-004 | Cierre de sesión seguro | Elimina sesión local + `signOut` en Supabase |
| RF-010 | Registrar gasto en lenguaje natural | Texto 1–280 caracteres; borrador solo en memoria |
| RF-011 | «Procesar con IA» con reglas deterministas | Sin API de IA; aviso de transparencia visible |
| RF-012 | Revisión y corrección obligatoria antes de guardar | Ningún guardado sin confirmación explícita |
| RF-013 | Guardar bajo el propietario y aislarlo | Propietario derivado del token; idempotencia UUID |
| RF-014 | Historial del más reciente al más antiguo | `fecha_gasto DESC, created_at DESC, id DESC`; paginado |
| RF-020 | Total, cantidad y promedio por periodo | Periodo por defecto: mes actual en `America/Bogota` |
| RF-021 | Gasto por categoría y categoría mayor | Empates: mostrar todas, orden alfabético |
| RF-023 | Detectar posibles fugas | Regla FUGA-01 v1.0 exacta (D-01) |
| RF-024 | Consultar evidencia de una fuga | Regla, versión, ocurrencias, fechas, total, IDs |
| RF-033 | Privacidad y aislamiento entre usuarios | Autorización en backend, no solo en UI |

### 5.2 Requerimientos no funcionales aplicables

| RNF | Prioridad | Cómo se materializa en el plan |
|---|---|---|
| RNF-001 Autorización obligatoria | Must | Dependencia `require_user` en toda ruta privada + suite de seguridad por ruta (F4, F13) |
| RNF-002 Privacidad y minimización | Must | DTOs sin campos sobrantes; admin sin gastos; logs sin datos (F13) |
| RNF-003 Credenciales y sesiones | Must | Supabase Auth; token en `expo-secure-store`; backend valida y consulta `disabled_at` |
| RNF-004 Validación de entradas | Must | Pydantic v2 estricto + restricciones SQL; rechazo de campos desconocidos |
| RNF-005 Integridad e idempotencia | Must | Transacción única por creación + UQ `(usuario_id, clave_idempotencia)` |
| RNF-006 Coherencia de agregados | Should | Estadísticas y fugas se calculan desde datos vigentes; sin caché persistente obsoleta |
| RNF-007 Logs sin datos sensibles | Must | Logger con filtro de campos; `correlation_id`; prohibido loguear `texto_original` y montos |
| RNF-008 TLS y secretos | Must | HTTPS en producción; `.env` fuera de git; `service_role` solo servidor |
| RNF-009 Usabilidad | Must | Estados vacío/carga/error/éxito en cada pantalla; errores junto al campo |
| RNF-010 Transparencia «Procesar con IA» | Must | Texto exacto de D-15 junto al botón |
| RNF-011 Compatibilidad | Must | Android + iOS en texto; voz solo Android con fallback |
| RNF-012 Fiabilidad | Must | Reintento sin duplicar; conservar texto ante fallo de red |
| RNF-013 Rendimiento | Should (sin umbrales) | Paginación obligatoria; índices; sin cifras inventadas (anexo D, C-06) |
| RNF-014 Mantenibilidad | Must | Versiones de diccionario/regla; contratos versionados `/api/v1`; pruebas |
| RNF-015 Auditoría administrativa | Should | Fuera de MVP; esquema `auditoria` reservado |
| RNF-016 Retención | Must | D-06 aplicado; sin borrado irreversible expuesto |

### 5.3 Decisiones D-01…D-15 (resumen operativo)

| ID | Decisión | Efecto en el código |
|---|---|---|
| D-01 | FUGA-01 v1.0: 30 días calendario, `America/Bogota`, agrupar por categoría + descripción normalizada, ≥3 gastos en ≥3 fechas distintas, cada uno COP 1.000–30.000, suma ≥ COP 15.000 | Módulo `domain/leaks/rule_fuga_01.py`, parámetros versionados en BD |
| D-02 | 9 categorías cerradas; «Otros» siempre incluida; empates se muestran todos | Catálogo en `categoria` + normalizador | 
| D-03 | Solo COP; enteros 1…100.000.000; sin flotantes; formato `es-CO`; porcentaje 1 decimal | `BIGINT` + `Decimal`/`int` en Python; formateador en móvil |
| D-04 | `America/Bogota`; fechas 2020-01-01…hoy; orden estable; mes calendario por defecto | `zoneinfo`, validadores de fecha, índices por fecha |
| D-05 | Texto 1–280; descripción 1–120; borrador solo en memoria; idempotencia UUID 24 h | Endpoint `interpret` sin persistencia; UQ + ventana 24 h |
| D-06 | Sin borrado de cuenta/gastos en MVP; desactivación con `disabled_at`; retención 30 días | `deleted_at` existe y no se expone |
| D-07 | Admin sin gastos; agregados solo con ≥10 usuarios | Fuera del MVP; regla documentada |
| D-08 | Roles Visitante/Usuario/Administrador; rol solo por aprovisionamiento seguro | `perfil.rol` con CHECK y sin escritura cliente |
| D-09 | Supabase Auth; sin JWT propio; recuperación por enlace del proveedor | SDK móvil + validación JWKS en backend |
| D-10 | Google OAuth vía Supabase, solo con credenciales y consentimiento | Should; no bloquea MVP |
| D-11 | Alertas internas + notificaciones locales; máx. 1 por candidato/7 días; nada entre 21:00 y 08:00 | Could; fuera del MVP |
| D-12 | Voz Android con Kotlin `SpeechRecognizer`, `es-CO`, ≤30 s, ≤280 caracteres, sin audio guardado | Could; módulo nativo planificado |
| D-13 | Nombres 2–80; teléfono 10 dígitos; foto ≤5 MB JPEG/PNG/WebP vía backend | Should; esquema listo |
| D-14 | Auditoría de acciones admin 90 días, sin datos financieros | Should; tabla reservada |
| D-15 | «Procesar con IA» literal + aclaración de reglas; lenguaje «posible fuga» | Textos centralizados en `src/content/` |

### 5.4 Requisitos que NO se convierten en trabajo

- Las menciones «pendiente (D-xx)» dentro del cuerpo de algunas HU quedan **sustituidas** por las decisiones cerradas. No se abre trabajo para "definir" D-01…D-15.
- Las HU Should/Could/Won't no se implementan, aunque sus tablas aparezcan en el ER.
- Las sugerencias de pruebas de las HU son orientativas; la estrategia obligatoria es la de la sección 22.

### 5.5 Decisiones aprobadas en la versión 1.1 (C-01…C-12)

| ID | Tema | Estado | Resolución vinculante (detalle en anexo D) |
|---|---|---|---|
| C-01 | Texto original del gasto | **APROBADA** | `gasto.texto_original` nullable y persistido como `NULL`; solo se guardan datos estructurados confirmados |
| C-02 | Nombres y apellidos | **APROBADA** | Opcionales en el registro; completables después (ola Should) |
| C-03 | Idempotencia | **APROBADA** | UUID por intento, ventana 24 h; `409 IDEMPOTENCY_EXPIRED`; no impide gastos legítimos idénticos con claves distintas |
| C-04 | Paginación | **APROBADA** | Cursor, 20 por carga, máximo 50, carga adicional al desplazarse |
| C-05 | Historias de usuario | **APROBADA** | No se modifican; «pendiente (D-xx)» se lee como resuelto (§3.5) |
| C-06 | Rendimiento | **APROBADA** | Objetivos orientativos; medir y documentar sin declarar cumplimiento |
| C-07 | Alojamiento del backend | **APROBADA** | Desarrollo local, diseño portable a nube; sin proveedor definitivo ni plan gratuito asumido |
| C-08 | Logo | **APROBADA** | Original intacto; solo derivados técnicos por composición, escalado proporcional y márgenes |
| C-09 | Base de datos del MVP | **APROBADA** | Solo 7 tablas: `perfil`, `categoria`, `gasto`, `regla_fuga`, `regla_fuga_version`, `fuga`, `fuga_evidencia` |
| C-10 | Campo `deleted_at` | **APROBADA** | Presente, opcional, inicialmente `NULL`, sin uso ni exposición en MVP |
| C-11 | Retención y eliminación | **APROBADA** | Sin eliminación desde la app; política y procedimiento administrativo documentados (§16.9) |
| C-12 | Fuga ↔ versión de regla | **APROBADA** | `fuga.regla_version_id` UUID FK → `regla_fuga_version(id)` desde el MVP |

---

## 6. Arquitectura

### 6.1 Vista de componentes

```
┌──────────────────────────────────────────────────────────────────────┐
│ CLIENTE · Aplicación móvil                                          │
│ React Native + TypeScript + Expo (development build)                │
│  ├─ Expo Router (navegación)                                        │
│  ├─ TanStack Query (estado de servidor) + Zustand (estado de UI)     │
│  ├─ React Hook Form + Zod (formularios y validación de entrada)      │
│  ├─ Supabase JS (Auth) + expo-secure-store (sesión)                 │
│  └─ Módulo nativo Kotlin `reconocimiento-voz` (solo Android)         │
└───────────────────────────┬──────────────────────────────────────────┘
                            │ HTTPS · JSON · Bearer <access_token>
                            ▼
┌──────────────────────────────────────────────────────────────────────┐
│ SERVIDOR · Backend FastAPI                                          │
│  ├─ api/v1 (routers, dependencias, contratos)                       │
│  ├─ services (casos de uso, transacciones, idempotencia)             │
│  ├─ domain (parser de gastos, normalizador, FUGA-01, estadísticas)   │
│  ├─ repositories (SQL explícito, siempre filtrado por propietario)   │
│  └─ core (config, seguridad/JWKS, errores, logging, correlación)     │
└───────────────────────────┬──────────────────────────────────────────┘
                            │ SQL (pooler de Supabase) · rol privilegiado
                            ▼
┌──────────────────────────────────────────────────────────────────────┐
│ DATOS · Supabase                                                    │
│  ├─ PostgreSQL: perfil, categoria, gasto, regla_fuga,               │
│  │                regla_fuga_version, fuga, fuga_evidencia          │
│  ├─ Supabase Auth: auth.users, auth.identities (identidad)          │
│  └─ RLS activo como defensa en profundidad                          │
└──────────────────────────────────────────────────────────────────────┘
        ▲                                     ▲
        │ (opcional, Should)                  │ (opcional, Could)
   Google Identity                        Expo Notifications (local)
   Cloudinary (fotos)
```

### 6.2 Responsabilidades por capa

| Capa | Responsabilidad | Prohibido |
|---|---|---|
| `mobile/app` (rutas) | Composición de pantallas y navegación | Lógica de negocio o SQL |
| `mobile/src/features` | Estado de pantalla, hooks de caso de uso, llamadas al API | Cálculos financieros definitivos |
| `mobile/src/components` | UI reutilizable y accesible | Conocer endpoints concretos |
| `mobile/src/theme` | Tokens de diseño | Colores hardcodeados fuera de aquí |
| `backend/app/api` | Validación de contrato, autenticación, códigos HTTP | Reglas de negocio |
| `backend/app/services` | Orquestación, transacciones, idempotencia | SQL crudo extenso |
| `backend/app/domain` | Reglas puras y testeables (parser, FUGA-01, agregados) | Acceso a red o BD |
| `backend/app/repositories` | SQL parametrizado, scoping por propietario | Decidir permisos |
| `supabase/migrations` | Esquema, restricciones, índices, RLS | Datos de producción |

### 6.3 Flujo de información — registrar un gasto

1. El usuario escribe el texto (1–280 caracteres) en la app.
2. La app hace `POST /api/v1/expenses/interpret` con `{ texto }` y el `Bearer` token.
3. FastAPI valida token → resuelve `usuario_id` → verifica `perfil.disabled_at IS NULL`.
4. `domain.expenses.parser` normaliza el texto y extrae monto, fecha, descripción y categoría propuesta.
5. Responde un **borrador** (`draft`) con `confianza` por campo, `categoria_id` propuesta y avisos. **No persiste nada.**
6. La app muestra la pantalla de revisión con todos los campos editables y el aviso D-15.
7. Al confirmar, la app envía `POST /api/v1/expenses` con `Idempotency-Key` (UUID v4 generado por intento).
8. El servicio abre transacción: valida payload → busca clave de idempotencia → inserta `gasto` → confirma.
9. Responde `201` con el gasto creado (o `200` si la clave ya existía con el mismo contenido; `409` si el contenido difiere).
10. La app invalida las queries de historial, estadísticas y fugas; el dashboard se recalcula bajo demanda.

### 6.4 Comunicación entre capas

- **Móvil → Backend:** HTTPS/JSON, versionado en la ruta (`/api/v1`), `Authorization: Bearer`, `X-Correlation-Id` opcional generado por el cliente.
- **Backend → Supabase Auth:** solo lectura de JWKS (clave pública, cacheada con `lru_cache` y `TTL`). Nunca se llama a `signIn` desde el backend.
- **Backend → PostgreSQL:** pool de conexiones; sentencias parametrizadas; una transacción por caso de uso.
- **Backend → servicios externos (Should/Could):** Cloudinary solo para firma de subida; notificaciones solo locales (sin servidor).

### 6.5 Gestión de errores

Modelo único de error (RFC 7807 simplificado):

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "El monto debe ser un entero entre 1 y 100000000 COP.",
    "details": [{ "field": "monto_cop", "issue": "range" }],
    "correlation_id": "c0a8f0e2-..."
  }
}
```

| Código | HTTP | Uso |
|---|---|---|
| `UNAUTHENTICATED` | 401 | Token ausente, inválido, expirado o emisor/audiencia incorrectos |
| `ACCOUNT_DISABLED` | 403 | `perfil.disabled_at` no nulo |
| `FORBIDDEN` | 403 | Rol insuficiente o recurso ajeno |
| `NOT_FOUND` | 404 | Recurso inexistente **o de otro propietario** (no se distingue) |
| `VALIDATION_ERROR` | 422 | Contrato o regla de negocio violada |
| `IDEMPOTENCY_CONFLICT` | 409 | Misma clave, contenido distinto |
| `IDEMPOTENCY_EXPIRED` | 409 | Clave reutilizada después de 24 h (ver anexo D, C-03) |
| `RATE_LIMITED` | 429 | Límite de intentos de autenticación o de interpretación |
| `UPSTREAM_ERROR` | 503 | Fallo de BD o dependencia no disponible |
| `INTERNAL_ERROR` | 500 | Error no previsto, sin filtrar detalles |

Regla transversal: **nunca** se devuelve un 500 con traza, SQL ni datos del usuario. Toda excepción no controlada se registra con `correlation_id` y se responde `INTERNAL_ERROR`.

### 6.6 Configuración por entorno

| Entorno | Uso | Backend | Móvil |
|---|---|---|---|
| `local` | Desarrollo del agente | `.env.local` + Supabase dev | `.env.local` con `EXPO_PUBLIC_API_URL=http://10.0.2.2:8000` (emulador) o IP LAN |
| `test` | Pruebas automatizadas | `.env.test` + proyecto Supabase de pruebas | No aplica |
| `prod` | Demostración/entrega | HTTPS + secretos del hosting | `EXPO_PUBLIC_API_URL` HTTPS, build release |

Variables (ver §19.8): `SUPABASE_URL`, `SUPABASE_JWKS_URL`, `SUPABASE_JWT_ISSUER`, `SUPABASE_JWT_AUDIENCE`, `DATABASE_URL`, `APP_ENV`, `LOG_LEVEL`, `CORS_ORIGINS`.

**Portabilidad de despliegue (C-07).** El backend se desarrolla y prueba localmente, pero se diseña desde el inicio para desplegarse en la nube sin cambios de código:

- Toda configuración entra por variables de entorno; no hay valores de entorno hardcodeados ni rutas absolutas de la máquina.
- `EXPO_PUBLIC_API_URL` es configurable en la app; `http://10.0.2.2:8000` es solo un ejemplo de desarrollo, nunca una constante del código.
- Dependencias reproducibles (`pyproject.toml` + lock; `package-lock.json`).
- Credenciales exclusivamente en el entorno del backend o del proveedor; nunca en el repositorio ni en el bundle móvil.
- Preparado para HTTPS en producción y con CORS restringido por lista explícita.
- Sin dependencia de servicios locales, túneles ni rutas de disco para funcionar.
- Instrucciones de despliegue documentadas en `backend/docs/operacion.md` (F2) y `docs/planificacion/entrega.md` (F14).

No se elige proveedor definitivo ni se asume un plan gratuito permanente.

### 6.7 Separación lógica de negocio / infraestructura

- `domain/` no importa FastAPI, SQLAlchemy ni `httpx`: recibe y devuelve estructuras puras (dataclasses/Pydantic) y es 100 % testeable sin red.
- `repositories/` recibe `usuario_id` como parámetro **obligatorio** en toda operación sobre datos privados; no existe método "sin propietario".
- `services/` es el único lugar que abre transacciones.
- La app no conoce reglas: solo muestra lo que el backend calcula y valida lo mínimo para UX.

### 6.8 Decisiones de arquitectura (ADR resumidos)

| ADR | Decisión | Alternativa descartada | Motivo |
|---|---|---|---|
| ADR-01 | Expo con **development build** + módulo local Kotlin | React Native CLI puro | Menor configuración nativa manteniendo módulo propio; expo prebuild genera el proyecto Android |
| ADR-02 | API única FastAPI como puerta a datos | Cliente hablando directo a Supabase | D-08 exige autorización en backend y permite reglas deterministas |
| ADR-03 | SQL explícito (SQLAlchemy Core / `text()`), sin ORM de modelos | ORM declarativo completo | Consultas de agregación y RLS más claras; menos magia |
| ADR-04 | Cálculo de fugas bajo demanda + snapshot | Job programado | D-01 lo exige explícitamente |
| ADR-05 | Estado de servidor con TanStack Query | Redux global | Menos código, invalidación por query key, ideal para datos remotos |
| ADR-06 | Sin librería de gráficos en MVP | Victory/ChartKit | El desglose por categoría se resuelve con barras nativas; menos peso y menos riesgo |
| ADR-07 | Migraciones SQL versionadas en `supabase/migrations` | Alembic | Una sola fuente de verdad del esquema; Supabase CLI las aplica |
| ADR-08 | **FastAPI es la única puerta de acceso a los datos financieros** | Cliente móvil escribiendo directo en Supabase | Autenticación verificada en servidor, reglas deterministas centralizadas, credenciales de BD fuera del cliente y auditoría de autorización |

### 6.9 Decisión arquitectónica complementaria — FastAPI como puerta de acceso

Además de C-01…C-12, la propietaria aprobó la siguiente decisión, que **no sustituye a C-07** (alojamiento) sino que fija el modelo de acceso a datos:

| Aspecto | Decisión vinculante |
|---|---|
| Cliente | La aplicación móvil consume **solo la API FastAPI**; no escribe ni lee directamente las tablas financieras |
| Acceso a datos | FastAPI accede a PostgreSQL mediante conexión segura y credenciales que permanecen **exclusivamente en el backend** |
| Identidad | Supabase Auth emite los tokens; FastAPI los **valida** (JWKS, issuer, audience) y **no emite JWT propios** |
| Autorización | El propietario se deriva del claim `sub`; todo repositorio privado filtra por `usuario_id`; el rol se lee de `perfil.rol` |
| RLS | Se activa como **defensa en profundidad**; no se asume que proteja las consultas del rol privilegiado del backend |
| Superficie del cliente | El bundle móvil contiene solo `SUPABASE_URL` y `anon key`; nunca `DATABASE_URL` ni `service_role` |
| Consecuencia | Toda ruta financiera nueva exige contrato en el anexo A, prueba de aislamiento y scoping explícito |

**Verificación obligatoria:** la coherencia entre permisos PostgreSQL, aislamiento por usuario, políticas RLS y conexión del backend se prueba en F4 y se reejecuta en F13 (§10.8). Si una consulta del backend puede devolver filas de otro usuario, es un defecto **crítico**, aunque RLS esté activo.

---

## 7. Tecnologías del frontend

### 7.1 Núcleo obligatorio

| Tecnología | Versión | Justificación |
|---|---|---|
| React Native | La que fije el SDK de Expo estable elegido en F0 | Base del producto móvil |
| TypeScript | `^5.x` estricto (`strict: true`) | Contratos tipados con el backend |
| Expo SDK | **Estable vigente en F0** (≥ 54; se registra la versión exacta en `mobile/docs/versiones.md`) | Development builds, prebuild, config plugins, notificaciones |
| Expo Router | Última compatible con el SDK | Navegación file-based oficial, deep links y grupos `(auth)` / `(app)` |
| React | La que exija el SDK | — |

> **Regla de oro de versiones:** no se fija un número "a mano" en el plan. En F0 se ejecuta `npx create-expo-app@latest` y `npx expo install --check`; la salida se copia a `mobile/docs/versiones.md` y se congela en `package-lock.json`. Cualquier actualización posterior exige fase de regresión.

### 7.2 Dependencias complementarias y su justificación

| Necesidad | Librería | Justificación | Riesgo/Nota |
|---|---|---|---|
| Navegación | `expo-router` | Oficial, tipada, con layouts y grupos | Requiere `app/` y `_layout.tsx` |
| Estado de servidor | `@tanstack/react-query` | Caché, reintentos, invalidación por key | Configurar `retry: 1` para no duplicar guardados |
| Estado de UI | `zustand` | Store mínimo (tema, filtros temporales) | No duplicar estado del servidor |
| Formularios | `react-hook-form` | Rendimiento y ergonomía en formularios largos | — |
| Validación | `zod` | Esquemas compartidos de entrada | Mensajes en español |
| Cliente HTTP | `fetch` nativo envuelto en `src/lib/api.ts` | Sin dependencia extra; control total de errores e idempotencia | Timeout con `AbortController` |
| Sesión | `@supabase/supabase-js` | Auth oficial (D-09) | Requiere adaptador de storage |
| Almacenamiento seguro | `expo-secure-store` | Tokens fuera de AsyncStorage | Límite ~2 KB por ítem: dividir la sesión si es necesario |
| Fuentes | `expo-font` + `@expo-google-fonts/plus-jakarta-sans` | Tipografía oficial | Cargar antes del splash |
| Imágenes | `expo-image` | Caché y rendimiento | — |
| Notificaciones | `expo-notifications` | Solo locales (D-11, Could) | No se instala en MVP |
| Voz | Módulo local propio `modules/reconocimiento-voz` (Kotlin + `expo-modules-core`) | D-12 exige `SpeechRecognizer` nativo | No funciona en Expo Go |
| Pruebas | `jest-expo`, `@testing-library/react-native` | Pruebas de componentes y hooks | Sin emulador |
| Calidad | `eslint-config-expo`, `prettier`, `tsc --noEmit` | Consistencia y detección temprana | Obligatorio antes de cada cierre de fase |

### 7.3 Dependencias deliberadamente NO usadas

- `react-native-voice` / `@react-native-voice/voice`: wrapper no verificado con el SDK actual; D-12 pide control nativo propio.
- Cualquier librería de gráficos: innecesaria para dos visualizaciones simples.
- Redux/MobX: sobredimensionado.
- `axios`: `fetch` cubre el caso.
- Librerías de UI con tema propio (NativeBase, UI Kitten): imponen paleta y dificultan la identidad Petrol Mint Vitality.
- `expo-auth-session` en MVP: Google es Should.
- Cualquier SDK de IA: prohibido por D-05/D-15.

### 7.4 Estructura de carpetas del móvil

```
mobile/
├── app/                              # Expo Router
│   ├── _layout.tsx                   # Providers: QueryClient, Auth, Theme, SafeArea
│   ├── index.tsx                     # Bienvenida pública (HU-01)
│   ├── (auth)/
│   │   ├── _layout.tsx
│   │   ├── registro.tsx              # HU-02
│   │   ├── iniciar-sesion.tsx        # HU-02
│   │   └── recuperar.tsx             # HU-05 (Should, no en MVP)
│   ├── (app)/
│   │   ├── _layout.tsx               # Tabs + guard de sesión
│   │   ├── inicio.tsx                # Dashboard (HU-20/HU-21)
│   │   ├── gastos/
│   │   │   ├── index.tsx             # Historial (HU-14)
│   │   │   ├── nuevo.tsx             # Captura de texto (HU-10)
│   │   │   └── revisar.tsx           # Revisión y confirmación (HU-12/HU-13)
│   │   ├── fugas/
│   │   │   ├── index.tsx             # Lista (HU-23)
│   │   │   └── [id].tsx              # Evidencia (HU-24)
│   │   └── ajustes.tsx               # Cerrar sesión, acerca de, privacidad
│   └── +not-found.tsx
├── src/
│   ├── components/                   # Button, Input, Card, EmptyState, ...
│   ├── features/
│   │   ├── auth/                     # hooks, schemas, api
│   │   ├── expenses/                 # hooks, schemas, formatters
│   │   ├── analytics/
│   │   └── leaks/
│   ├── lib/                          # api.ts, supabase.ts, secureStorage.ts, errors.ts
│   ├── theme/                        # tokens.ts, typography.ts, ThemeProvider.tsx
│   ├── content/                      # textos legales y de transparencia (D-15)
│   └── types/                        # DTOs espejo del backend
├── modules/reconocimiento-voz/       # solo Could (F14+ / anexo E)
├── assets/branding/                  # logo copiado sin modificar + derivados técnicos
├── app.config.ts
├── tsconfig.json
├── package.json
└── docs/versiones.md
```

### 7.5 Compilación Android

- `npx expo prebuild --platform android` genera `mobile/android/` (se versiona o se ignora según decisión de F0; recomendación: **no versionar** `android/` e regenerar con prebuild, salvo que se requiera edición manual nativa).
- Build local: `cd mobile/android && ./gradlew assembleDebug` (Windows: `gradlew.bat assembleDebug`), con JDK 17/21 y SDK instalados.
- Alternativa si el build local falla por entorno: EAS Build gratuito con cuenta Expo (requiere login y consume cuota; **no** se activa sin aprobación).
- El módulo de voz se integra como **local Expo module** (`modules/reconocimiento-voz`) para que `prebuild` lo enlace automáticamente.

---

## 8. Tecnologías del backend

### 8.1 Stack

| Componente | Elección | Justificación |
|---|---|---|
| Lenguaje | Python 3.12 | Disponible y estable en la máquina |
| Framework | FastAPI | Tipado, OpenAPI automático, dependencias |
| Validación | Pydantic v2 + `pydantic-settings` | Contratos estrictos y configuración por entorno |
| Servidor ASGI | Uvicorn | Estándar de desarrollo |
| Acceso a datos | SQLAlchemy 2.0 Core + `psycopg[binary,pool]` | SQL explícito, pool, transacciones claras |
| Migraciones | SQL en `supabase/migrations` aplicadas con `npx supabase db push` | Una sola fuente de verdad |
| Auth | `PyJWT[crypto]` + `PyJWKClient` | Verificación JWKS de Supabase |
| HTTP cliente | `httpx` (solo pruebas/integraciones) | — |
| Pruebas | `pytest`, `pytest-asyncio`, `httpx.ASGITransport` | Rápidas, sin red |
| Calidad | `ruff`, `mypy` (modo laxo en dominio), `black` vía ruff format | Consistencia |
| Logs | `structlog` o `logging` con filtro propio | JSON con `correlation_id`, sin datos sensibles |

### 8.2 Estructura de carpetas

```
backend/
├── app/
│   ├── main.py                       # create_app(), routers, handlers globales
│   ├── api/
│   │   ├── deps.py                   # get_current_user, require_admin, correlation_id
│   │   └── v1/
│   │       ├── router.py
│   │       ├── health.py
│   │       ├── me.py
│   │       ├── categories.py
│   │       ├── expenses.py
│   │       ├── analytics.py
│   │       └── leaks.py
│   ├── core/
│   │   ├── config.py                 # Settings
│   │   ├── security.py               # JWKS, verificación, claims
│   │   ├── errors.py                 # excepciones + handlers
│   │   ├── logging.py                # configuración y filtro
│   │   └── time.py                   # America/Bogota, ventanas, periodos
│   ├── domain/
│   │   ├── expenses/
│   │   │   ├── normalizer.py
│   │   │   ├── amount_parser.py
│   │   │   ├── date_parser.py
│   │   │   ├── classifier.py
│   │   │   └── interpreter.py        # orquesta y produce Draft
│   │   ├── leaks/
│   │   │   ├── rule_fuga_01.py
│   │   │   └── grouping.py
│   │   └── analytics/
│   │       └── aggregations.py
│   ├── repositories/
│   │   ├── base.py
│   │   ├── profiles.py
│   │   ├── categories.py
│   │   ├── expenses.py
│   │   └── leaks.py
│   ├── schemas/
│   │   ├── common.py
│   │   ├── auth.py
│   │   ├── expenses.py
│   │   ├── analytics.py
│   │   └── leaks.py
│   ├── services/
│   │   ├── expenses_service.py
│   │   ├── analytics_service.py
│   │   ├── leaks_service.py
│   │   └── profiles_service.py
│   └── db/
│       ├── session.py                # engine, pool, transaction()
│       └── sql/                      # consultas .sql cuando superan 20 líneas
├── tests/
│   ├── unit/                         # dominio puro
│   ├── integration/                  # BD de pruebas
│   ├── api/                          # contratos y códigos
│   └── security/                     # autorización y aislamiento
├── pyproject.toml
├── .env.example
└── docs/
    ├── contratos.md
    └── operacion.md
```

### 8.3 Convenciones de API

- Prefijo `/api/v1`; recursos en plural y sustantivos; verbos solo cuando no hay recurso claro (`/expenses/interpret`).
- Fechas ISO `YYYY-MM-DD`; timestamps ISO 8601 con offset.
- Dinero: entero `monto_cop` (nunca string con separadores).
- IDs: UUID v4 en texto.
- Paginación por cursor (`created_at,id`) codificado en base64url; `limit` por defecto 20, máximo 50 (decisión aprobada C-04, anexo D).
- `Idempotency-Key` obligatorio en `POST /expenses`; opcional pero recomendado en el resto de POST.
- Todo error sigue el modelo de §6.5.
- OpenAPI generado en `/api/v1/openapi.json`, visible solo en `local`/`test`.

### 8.4 Manejo centralizado de errores y logging

- Excepciones de dominio (`DomainError`, `ValidationError`, `NotFoundError`) se traducen en un único `exception_handler`.
- `RequestValidationError` se mapea a `VALIDATION_ERROR` con `details[].field`.
- Middleware de correlación: acepta `X-Correlation-Id` válido o genera UUID; se devuelve en la respuesta y en los logs.
- Filtro de logs: lista negra de claves (`texto_original`, `descripcion`, `monto_cop`, `access_token`, `password`, `authorization`). Prueba automatizada que inspecciona la salida del logger.
- `LOG_LEVEL=INFO` en producción; `DEBUG` solo local y nunca con payloads completos.

### 8.5 Integración con Supabase (backend)

1. `Settings.supabase_url` construye el issuer (`{url}/auth/v1`) y el JWKS (`{url}/auth/v1/.well-known/jwks.json`).
2. `security.py` cachea el `PyJWKClient` (TTL 10 min) y valida: firma, `alg` permitido (RS256/ES256 según JWKS), `iss`, `aud = authenticated`, `exp`, `nbf`, `sub` UUID.
3. Se consulta `perfil` por `id = sub`. Si no existe → `404 NOT_FOUND` con `details: [{ "reason": "profile_not_found" }]` (la app llama a `bootstrap`). Si `disabled_at` no es nulo → `403 ACCOUNT_DISABLED`.
4. El rol se lee de `perfil.rol` (**nunca** de `user_metadata`, que el cliente puede editar).
5. Para operaciones administrativas (Should) se usa un cliente con `service_role` **solo en servidor**, jamás en el móvil.

### 8.6 Conexión a base de datos

- `DATABASE_URL` apunta al **pooler de sesión** de Supabase (puerto 5432) en desarrollo y al pooler de transacción (6543) en producción con `statement_cache_size=0` si se usa `psycopg` en modo transacción.
- Pool: `min_size=1`, `max_size=5` (plan gratuito), `pool_timeout=5`, `command_timeout=10`.
- Toda escritura ocurre dentro de `async with transaction()`; los repositorios reciben la conexión, no la crean.
- Prohibido `SELECT *` en repositorios: columnas explícitas.
- **Rol privilegiado:** la conexión del backend usa un rol de base de datos que **omite RLS** (`postgres` o el rol de servicio del proyecto). Por tanto, la barrera real de aislamiento es el filtro `usuario_id` del repositorio; RLS solo protege el acceso directo del cliente. Esto se prueba explícitamente en F4.
- **Credenciales:** `DATABASE_URL` y `SUPABASE_SERVICE_ROLE_KEY` existen solo en el entorno del backend. El móvil nunca recibe cadenas de conexión ni claves de servicio.

### 8.7 Pruebas del backend

- `pytest` con `asyncio_mode=auto`.
- Unitarias de dominio: sin BD, sin red, milisegundos.
- Integración: `TEST_DATABASE_URL` obligatoria; si falta, los tests se marcan `skip` con razón explícita (no se finge éxito).
- API: `httpx.AsyncClient(transport=ASGITransport(app=app))` + tokens de prueba firmados por el proyecto de pruebas o generados por Supabase test.
- Seguridad: matriz por ruta (sin token, token de otro usuario, rol insuficiente, cuenta deshabilitada).

---

## 9. Modelo de datos

### 9.1 Principios

- Una sola base PostgreSQL en Supabase. Identidad en `auth.users`; el resto en el esquema `public`.
- Nombres en `snake_case`, español, sin prefijos redundantes.
- Todas las tablas propias: `id UUID PRIMARY KEY DEFAULT gen_random_uuid()`, `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`, `updated_at TIMESTAMPTZ NOT NULL DEFAULT now()`.
- Dinero: `BIGINT` con `CHECK (monto BETWEEN 1 AND 100000000)`.
- Fechas de gasto: `DATE`; marcas técnicas: `TIMESTAMPTZ`.
- Borrado lógico solo donde el ER lo define (`gasto.deleted_at`, `limite_mensual.deleted_at`), no expuesto en MVP.
- `ON DELETE` explícito en cada FK; por defecto `RESTRICT` para evitar pérdidas silenciosas.

### 9.2 Tablas del MVP (7)

#### 9.2.1 `perfil`

| Columna | Tipo | Restricciones | Notas |
|---|---|---|---|
| `id` | UUID | PK, FK → `auth.users(id)` ON DELETE CASCADE | Espeja el `sub` del token |
| `nombres` | VARCHAR(80) | NULL | C-02: opcional en el registro; completable después (ola Should) |
| `apellido` | VARCHAR(80) | NULL | C-02: opcional en el registro; completable después (ola Should) |
| `telefono` | VARCHAR(10) | NULL, CHECK `^[0-9]{10}$` | Opcional (D-13) |
| `foto_url` | TEXT | NULL | Debe ser URL `https://res.cloudinary.com/...` |
| `foto_google_url` | TEXT | NULL | Solo Should |
| `rol` | VARCHAR(15) | NOT NULL DEFAULT `'usuario'`, CHECK IN (`usuario`,`administrador`) | Nunca escribible por el cliente |
| `disabled_at` | TIMESTAMPTZ | NULL | Desactivación administrativa |
| `created_at` / `updated_at` | TIMESTAMPTZ | NOT NULL | Trigger `set_updated_at` |

Índices: `perfil_rol_idx (rol)`, `perfil_disabled_idx (disabled_at) WHERE disabled_at IS NOT NULL`.

#### 9.2.2 `categoria`

| Columna | Tipo | Restricciones |
|---|---|---|
| `id` | UUID | PK |
| `nombre` | VARCHAR(40) | NOT NULL, UNIQUE |
| `orden` | SMALLINT | NOT NULL, UNIQUE |
| `activa` | BOOLEAN | NOT NULL DEFAULT true |
| `created_at` / `updated_at` | TIMESTAMPTZ | NOT NULL |

Seed obligatorio (D-02), en este orden: Alimentación, Transporte, Vivienda, Servicios, Educación, Salud, Entretenimiento, Compras, Otros.

#### 9.2.3 `gasto`

| Columna | Tipo | Restricciones | Notas |
|---|---|---|---|
| `id` | UUID | PK | |
| `usuario_id` | UUID | NOT NULL, FK → `perfil(id)` ON DELETE RESTRICT | Propietario |
| `categoria_id` | UUID | NOT NULL, FK → `categoria(id)` ON DELETE RESTRICT | |
| `monto_cop` | BIGINT | NOT NULL, CHECK 1…100000000 | Entero |
| `descripcion` | VARCHAR(120) | NOT NULL, CHECK `length(btrim(descripcion)) BETWEEN 1 AND 120` | Campo confirmado |
| `texto_original` | VARCHAR(280) | **NULL** | C-01: la columna es nullable y en el MVP se persiste `NULL`; solo se guardan los datos estructurados confirmados |
| `fecha_gasto` | DATE | NOT NULL, `CHECK (fecha_gasto >= DATE '2020-01-01')` | El límite superior (no futura) se valida en FastAPI con fecha actual de `America/Bogota`; PostgreSQL solo aplica el mínimo fijo |
| `moneda` | CHAR(3) | NOT NULL DEFAULT `'COP'`, CHECK = `'COP'` | |
| `diccionario_version` | VARCHAR(10) | NOT NULL | p. ej. `1.0` |
| `reglas_version` | VARCHAR(10) | NOT NULL | p. ej. `1.0` |
| `clave_idempotencia` | UUID | NOT NULL | UQ con `usuario_id` |
| `created_at` / `updated_at` | TIMESTAMPTZ | NOT NULL | |
| `deleted_at` | TIMESTAMPTZ | NULL | No expuesto en MVP |

Índices:
- `gasto_usuario_fecha_idx (usuario_id, fecha_gasto DESC, created_at DESC, id DESC)` — historial.
- `gasto_usuario_categoria_idx (usuario_id, categoria_id)`.
- `gasto_usuario_ventana_idx (usuario_id, fecha_gasto) WHERE deleted_at IS NULL` — fugas y estadísticas.
- `gasto_idempotencia_uq UNIQUE (usuario_id, clave_idempotencia)`.

#### 9.2.4 `regla_fuga`

| Columna | Tipo | Restricciones |
|---|---|---|
| `id` | UUID | PK |
| `codigo` | VARCHAR(20) | NOT NULL, UNIQUE (valor `FUGA-01`) |
| `nombre` | VARCHAR(80) | NOT NULL |
| `descripcion` | TEXT | NOT NULL |
| `activa` | BOOLEAN | NOT NULL DEFAULT true |
| `created_at` / `updated_at` | TIMESTAMPTZ | NOT NULL |

#### 9.2.5 `regla_fuga_version`

| Columna | Tipo | Restricciones | Notas |
|---|---|---|---|
| `id` | UUID | PK | |
| `regla_id` | UUID | NOT NULL, FK → `regla_fuga(id)` | |
| `version` | VARCHAR(10) | NOT NULL | `1.0` |
| `parametros` | JSONB | NOT NULL | `{ventana_dias:30, min_gastos:3, min_fechas:3, monto_min:1000, monto_max:30000, suma_min:15000, zona:"America/Bogota"}` |
| `vigente_desde` | TIMESTAMPTZ | NOT NULL | |
| `vigente_hasta` | TIMESTAMPTZ | NULL | |
| `created_at` | TIMESTAMPTZ | NOT NULL | |

Restricción: `UNIQUE (regla_id, version)`; solo una versión vigente por regla (índice parcial).

#### 9.2.6 `fuga`

| Columna | Tipo | Restricciones |
|---|---|---|
| `id` | UUID | PK |
| `usuario_id` | UUID | NOT NULL, FK → `perfil(id)` |
| `regla_version_id` | UUID | NOT NULL, FK → `regla_fuga_version(id)` ON DELETE RESTRICT (C-12) |
| `categoria_id` | UUID | NOT NULL, FK → `categoria(id)` |
| `descripcion_normalizada` | VARCHAR(120) | NOT NULL |
| `ocurrencias` | SMALLINT | NOT NULL, CHECK > 0 (el umbral ≥ 3 vive en `regla_fuga_version.parametros`) |
| `monto_acumulado_cop` | BIGINT | NOT NULL, CHECK > 0 (el umbral ≥ 15.000 vive en `regla_fuga_version.parametros`) |
| `fecha_desde` | DATE | NOT NULL |
| `fecha_hasta` | DATE | NOT NULL |
| `vigente` | BOOLEAN | NOT NULL DEFAULT true |
| `detectada_en` / `actualizada_en` | TIMESTAMPTZ | NOT NULL |

Índices:
- `fuga_usuario_vigente_idx (usuario_id, vigente)`.
- `fuga_snapshot_uq UNIQUE (usuario_id, regla_version_id, categoria_id, descripcion_normalizada) WHERE vigente = true` — índice único **parcial**: permite conservar snapshots históricos invalidados sin bloquear el recálculo del mismo día.
- `fuga_regla_version_idx (regla_version_id)`.

#### 9.2.7 `fuga_evidencia`

| Columna | Tipo | Restricciones |
|---|---|---|
| `id` | UUID | PK |
| `fuga_id` | UUID | NOT NULL, FK → `fuga(id)` ON DELETE CASCADE |
| `gasto_id` | UUID | NOT NULL, FK → `gasto(id)` ON DELETE CASCADE |
| `created_at` | TIMESTAMPTZ | NOT NULL |

Restricción: `UNIQUE (fuga_id, gasto_id)`.

### 9.3 Tablas fuera del MVP (existen en el ER, no se crean en F1)

| Tabla | Prioridad | Se crea en |
|---|---|---|
| `auditoria` | Should | Ola Should (anexo E) |
| `alerta` | Could | Ola Could |
| `limite_mensual`, `limite_mensual_cambio` | Won't | No se crea |

**Regla:** F1 crea solo las 7 tablas MVP + `auth` (gestionado por Supabase). Las demás quedan como migraciones futuras documentadas.

### 9.4 RLS e aislamiento

- RLS **activado** en `perfil`, `gasto`, `fuga`, `fuga_evidencia` (`ALTER TABLE ... ENABLE ROW LEVEL SECURITY`).
- Política base del cliente (`authenticated`): `SELECT` propio en `perfil` (`id = auth.uid()`); **ninguna** política de escritura directa en `gasto` ni `fuga` (el móvil no escribe en BD).
- El backend usa un **rol privilegiado** que omite RLS y **siempre** filtra por `usuario_id` en el repositorio. RLS es defensa en profundidad, no la única barrera.
- **Advertencia vinculante:** RLS **no** protege las consultas hechas con roles privilegiados (`postgres`, `service_role`, `BYPASSRLS`). Ninguna prueba puede declarar aislamiento basándose solo en RLS; la prueba debe ejercer la consulta real del backend.
- Las credenciales de base de datos y la clave de servicio viven solo en el backend; el cliente móvil no puede conectarse directamente a PostgreSQL.
- `categoria`, `regla_fuga`, `regla_fuga_version` son de lectura pública autenticada (catálogo), sin escritura.
- Pruebas diferenciadas obligatorias: (1) **RLS**: con conexión/rol `authenticated` sujeto a RLS, un usuario A no puede leer filas de B; sin política de `SELECT` sobre `gasto`, la lectura directa del cliente devuelve cero filas; (2) **autorización real**: con la misma conexión privilegiada de FastAPI (que puede omitir RLS), peticiones HTTP autenticadas como A jamás devuelven gastos, fugas, evidencia o agregados de B. El JWT no convierte por sí mismo una conexión privilegiada en conexión sujeta a RLS. Probar las dos barreras por separado (§10.8 y §22).

### 9.5 Integridad y validaciones en base de datos

| Regla | Implementación |
|---|---|
| Monto entero válido | `CHECK (monto_cop BETWEEN 1 AND 100000000)` |
| Fecha mínima ≥ 2020-01-01 | `CHECK (fecha_gasto >= DATE '2020-01-01')` (restricción fija en PostgreSQL) |
| Fecha no futura | FastAPI/Pydantic valida `fecha_gasto <= date.today()` calculado en zona `America/Bogota` **en el servidor**, antes de escribir; devuelve `422` si es futura. No se confía en el reloj del móvil. |
| Moneda única | `CHECK (moneda = 'COP')` |
| Descripción no vacía | `CHECK (length(btrim(descripcion)) BETWEEN 1 AND 120)` |
| Categoría existente | FK |
| Propietario existente | FK |
| Sin duplicado idempotente | UNIQUE `(usuario_id, clave_idempotencia)` |
| Sin evidencia duplicada | UNIQUE `(fuga_id, gasto_id)` |
| Versión de regla íntegra | FK `fuga.regla_version_id → regla_fuga_version(id)` (C-12) |
| Umbrales no duplicados en DDL | `fuga.ocurrencias > 0` y `monto_acumulado_cop > 0`; los umbrales reales viven en `regla_fuga_version.parametros` |
| `updated_at` automático | Trigger `set_updated_at()` en las tablas con columna `updated_at` (`perfil`, `categoria`, `gasto`, `regla_fuga`); `fuga` usa `actualizada_en` por nomenclatura del modelo |

### 9.6 Migraciones (orden exacto)

| # | Archivo | Contenido |
|---|---|---|
| 0001 | `0001_extensions.sql` | `pgcrypto`, `citext` (si no existen), esquema `public` |
| 0002 | `0002_catalogo.sql` | `categoria`, `regla_fuga`, `regla_fuga_version` + seed de 9 categorías y FUGA-01 v1.0 |
| 0003 | `0003_perfil.sql` | `perfil`, trigger de creación desde `auth.users`, trigger `updated_at` |
| 0004 | `0004_gasto.sql` | `gasto` + índices + restricciones |
| 0005 | `0005_fugas.sql` | `fuga` (con `regla_version_id` UUID FK), `fuga_evidencia` + índices y UQ parcial de snapshot |
| 0006 | `0006_rls.sql` | `ENABLE ROW LEVEL SECURITY` + políticas |
| 0007 | `0007_grants.sql` | Revocación de escritura a `authenticated`/`anon`; permisos mínimos |

`supabase/seed.sql`: categorías (idempotente con `ON CONFLICT DO NOTHING`), regla FUGA-01 v1.0, y **datos ficticios solo en entorno de pruebas**.

---

## 10. Autenticación y seguridad

### 10.1 Principio rector

La identidad la emite **Supabase Auth**; FastAPI **no emite JWT propios** (D-09). El backend **verifica** el token y deriva el `usuario_id` del claim `sub`. Ningún identificador de usuario enviado por el cliente se acepta como fuente de identidad (R-33.03).

FastAPI es la **puerta única** a los datos financieros (§6.9): el móvil no escribe ni lee directamente las tablas `gasto`, `fuga` ni `fuga_evidencia`. La autorización se resuelve en el backend con `sub` + `perfil.rol` + `disabled_at`, y la conexión a PostgreSQL permanece en el servidor.

### 10.2 Flujos

**Registro (HU-02)**

1. App: `supabase.auth.signUp({ email, password })` con contraseña ≥ 8.
2. Supabase crea `auth.users` (y `auth.identities`).
3. Trigger `handle_new_user` crea `perfil` con `rol='usuario'`, `nombres/apellido = NULL`.
4. Si la confirmación de correo está activa: la app muestra "revisa tu correo" y no permite sesión hasta confirmar. Si el correo saliente no está configurado, la UI muestra indisponibilidad explícita (D-09) — **no simular envío**.
5. Primer acceso autenticado: la app llama `POST /api/v1/me/bootstrap` (idempotente) para garantizar el perfil si el trigger no existiera en el entorno.

**Inicio de sesión**

1. `signInWithPassword` → sesión (`access_token`, `refresh_token`, `expires_at`).
2. La app guarda la sesión en `expo-secure-store`.
3. `supabase-js` renueva el token automáticamente (`autoRefreshToken: true`).
4. Cada request al API adjunta `Authorization: Bearer <access_token>`.
5. Backend: verifica firma/claims → carga `perfil` → verifica `disabled_at IS NULL` → autoriza.

**Cierre de sesión (HU-04)**

1. `await supabase.auth.signOut()` (revoca refresh token en el proveedor).
2. Borrar claves de `SecureStore` y limpiar caché de TanStack Query (`queryClient.clear()`).
3. Navegar al grupo `(auth)` y limpiar historial (`router.replace('/iniciar-sesion')`).
4. Si `signOut` falla por red: borrar sesión local igualmente y registrar el fallo; la UI informa "sesión cerrada en este dispositivo".

### 10.3 Verificación del token en FastAPI

```python
# app/core/security.py (esquema, no código final)
ALGORITHMS = ["RS256", "ES256", "HS256"]  # se restringe a los que publique el JWKS

def verify_token(token: str) -> Claims:
    header = jwt.get_unverified_header(token)
    key = jwks_client.get_signing_key(header["kid"])
    payload = jwt.decode(
        token, key.key,
        algorithms=[header["alg"]],
        audience=settings.jwt_audience,   # "authenticated"
        issuer=settings.jwt_issuer,       # https://<ref>.supabase.co/auth/v1
        options={"require": ["exp", "sub", "aud", "iss"]},
        leeway=30,
    )
    return Claims(sub=UUID(payload["sub"]), role=payload.get("role"), ...)
```

Reglas adicionales:
- Rechazar `alg=none` y algoritmos no publicados.
- `sub` debe ser UUID válido.
- El **rol de aplicación** se lee de `perfil.rol`, no del claim `role` de Supabase (que solo distingue `authenticated`/`anon`).
- Cachear JWKS, no tokens.
- Errores de verificación → `401 UNAUTHENTICATED` sin detalle del motivo criptográfico.

### 10.4 Gestión de sesión en el dispositivo

- `expo-secure-store` con `keychainAccessible: AFTER_FIRST_UNLOCK`.
- La sesión completa puede superar el límite de ~2 KB: implementar `secureStorage.ts` con fragmentación (`chunk:0..n`) y limpieza atómica.
- Nunca en `AsyncStorage`, nunca en logs, nunca en `console.log`.
- Al detectar `401` dos veces seguidas: forzar cierre de sesión local y redirigir a login.
- `AppState` → al volver del background, refrescar sesión si `expires_at` < ahora + 60 s.

### 10.5 Matriz de protección de endpoints (MVP)

| Endpoint | Auth | Rol | Propietario | Notas |
|---|---|---|---|---|
| `GET /health` | No | — | — | Sin datos |
| `GET /ready` | No | — | — | Verifica BD |
| `POST /me/bootstrap` | Sí | usuario | sí mismo | Idempotente |
| `GET /me` | Sí | usuario | sí mismo | |
| `GET /categories` | Sí | usuario | — | Catálogo |
| `POST /expenses/interpret` | Sí | usuario | — | No persiste |
| `POST /expenses` | Sí | usuario | forzado al token | Ignora `usuario_id` del body |
| `GET /expenses` | Sí | usuario | filtrado | Cursor |
| `GET /analytics/summary` | Sí | usuario | filtrado | |
| `GET /analytics/by-category` | Sí | usuario | filtrado | |
| `GET /leaks` | Sí | usuario | filtrado | |
| `GET /leaks/{id}` | Sí | usuario | verificado | 404 si es ajeno |

Regla: el body **nunca** incluye `usuario_id`; si se envía, se ignora y se registra como intento anómalo.

### 10.6 Controles de seguridad obligatorios

| Control | Implementación | Verificación |
|---|---|---|
| Autorización por propietario | `WHERE usuario_id = :uid` en todo repositorio | Test por ruta con usuario B |
| Denegación por defecto | Router privado con dependencia global; rutas públicas explícitas | Test de ruta sin token |
| Validación estricta | Pydantic `extra="forbid"`, límites, patrones | Test de campos desconocidos |
| Idempotencia | UUID + UQ + comparación de contenido | Test de doble POST concurrente |
| Rate limiting básico | Límite en memoria por IP+sub en `interpret` y auth (p. ej. 30/min) | Test de ráfaga |
| Sin secretos en cliente | Solo `EXPO_PUBLIC_*` no sensibles | Revisión de `mobile/` y del bundle |
| Sin datos en logs | Filtro + test de captura de logs | Test de RNF-007 |
| HTTPS | Hosting con TLS; `http` solo en local | Revisión de configuración |
| CORS | Lista explícita; en móvil nativo no aplica, pero se restringe | Test de origen |
| Rol privilegiado vs RLS | Filtro `usuario_id` obligatorio; RLS no se asume como barrera del backend | Test que ejecuta la consulta real del backend con datos de A y B |
| Credenciales de BD | Solo en el backend; el bundle móvil no contiene `DATABASE_URL` ni `service_role` | Revisión del bundle + búsqueda de cadenas |
| Dependencias | `npm audit` / `pip-audit` en F13 | Reporte sin críticos |

### 10.7 Amenazas consideradas (modelo STRIDE abreviado)

| Amenaza | Vector | Mitigación |
|---|---|---|
| Spoofing | Token robado | SecureStore, expiración corta, revocación de refresh, `disabled_at` |
| Tampering | Body con `usuario_id` ajeno | Ignorado + scoping forzado |
| Repudiation | Acciones admin | Auditoría (Should) |
| Information disclosure | IDOR en `/expenses/{id}` | 404 uniforme + scoping |
| DoS | Texto gigante / ráfagas | Límite 280 + rate limit |
| Elevation of privilege | `rol` en metadata | Rol solo en `perfil`, escritura revocada |

### 10.8 Pruebas de seguridad mínimas

**Dos niveles distintos, ambos obligatorios:** las pruebas SQL/RLS se ejecutan con un rol realmente sujeto a RLS y contexto de identidad de A/B; las pruebas HTTP de FastAPI se ejecutan contra la **conexión privilegiada real configurada para el backend**, sin sustituir el repositorio por un mock que omita el SQL. El token de A identifica a A en FastAPI, pero **no impone RLS** sobre la conexión privilegiada. Registrar el rol de BD utilizado y evidencias de ambos niveles.

1. Sin `Authorization` → 401 en **todas** las rutas privadas.
2. Token expirado → 401.
3. Token con `aud`/`iss` incorrectos → 401.
4. Usuario A solicita gasto/fuga de B → 404.
5. Usuario A lista gastos → solo los suyos.
6. Cuenta con `disabled_at` → 403 incluso con token válido.
7. Body con `usuario_id` de B → se ignora y se crea con el `sub` del token.
8. Rol `usuario` en ruta admin → 403 (cuando exista).
9. Logs de un fallo → sin montos, descripciones, tokens ni correos.
10. `POST /expenses` repetido con la misma clave → un solo registro; contenido distinto → 409.
11. Prueba RLS con conexión `authenticated` y contexto A/B: `perfil` solo propio; sin política `SELECT` de `gasto`, acceso directo del cliente a `gasto` devuelve cero filas. No ejecutar esta prueba con `postgres`, `service_role` ni roles `BYPASSRLS`.
12. Prueba de integración HTTP usando **repositorios y conexión privilegiada reales**: sembrar gastos y fugas para A y B; A obtiene únicamente sus datos en `GET /expenses`, `/analytics/summary`, `/analytics/by-category`, `/leaks` y `/leaks/{id}` (incluida evidencia); IDs de B ⇒ `404` donde corresponda. Repetir invirtiendo A/B y comprobar ausencia de filtración en agregados.
13. Las pruebas con mocks sirven para lógica aislada, **no sustituyen** las pruebas de aislamiento con PostgreSQL real. Si falta `TEST_DATABASE_URL` o Supabase, registrar bloqueo; no declarar aprobados F4, F13 ni el criterio de seguridad G2.

---

## 11. Roles

### 11.1 Visitante

| Aspecto | Definición |
|---|---|
| Permisos | Ver pantalla pública (HU-01), navegar a registro o login |
| Pantallas | `index` (bienvenida), `registro`, `iniciar-sesion` |
| Navegación | Stack público; sin tabs |
| Acciones | Registrarse, iniciar sesión, leer qué es FUGA+ y cómo funciona |
| Restricciones | Sin acceso a datos, sin llamadas privadas, sin persistencia |
| Endpoints | Ninguno privado |
| Información | Solo contenido estático de producto; logo y paleta oficiales |
| Seguridad | Sin token; cualquier intento a ruta privada redirige a login |
| Pruebas | La pantalla carga sin sesión; el CTA lleva al flujo correcto; no hay datos financieros en el bundle |

### 11.2 Usuario

| Aspecto | Definición |
|---|---|
| Permisos | Gestionar sus propios gastos, estadísticas y fugas; cerrar sesión |
| Pantallas | `inicio`, `gastos/*`, `fugas/*`, `ajustes` |
| Navegación | Tabs: Inicio · Historial · Fugas · Ajustes; stack para captura/revisión |
| Acciones | Registrar gasto (texto), revisar/confirmar, ver historial, ver estadísticas, ver fugas y evidencia, cerrar sesión |
| Restricciones | Solo sus datos; no administra cuentas; no ve datos de terceros; no edita/elimina en MVP |
| Endpoints | `me`, `categories`, `expenses/*`, `analytics/*`, `leaks/*` |
| Información | Solo sus gastos y agregados derivados |
| Seguridad | Token válido + cuenta activa + scoping por `usuario_id` |
| Pruebas | Aislamiento completo (RNF-001), historial propio, estadísticas coherentes, fugas solo propias |

### 11.3 Administrador (Should, fuera del MVP)

| Aspecto | Definición |
|---|---|
| Permisos | Consultar metadatos mínimos de cuentas y activar/desactivar cuentas (HU-31/HU-32) |
| Pantallas | `admin/usuarios` (no se construye en MVP) |
| Navegación | Acceso separado; no visible para Usuario |
| Acciones | Listar usuarios (correo, estado, fecha de registro), cambiar estado |
| Restricciones | **Sin acceso a gastos, descripciones, montos, evidencias ni agregados con < 10 usuarios** (D-07) |
| Endpoints | `GET /admin/users`, `PATCH /admin/users/{id}/status` (Should) |
| Información | Metadatos mínimos; nunca datos financieros |
| Seguridad | Rol `administrador` asignado solo por aprovisionamiento seguro; auditoría (D-14) |
| Pruebas | Admin no puede leer `/expenses` de nadie; agregados suprimidos bajo umbral; toda acción queda auditada |

### 11.4 Aprovisionamiento del rol

- `perfil.rol` tiene `DEFAULT 'usuario'` y `CHECK`.
- `REVOKE INSERT, UPDATE (rol) ON perfil FROM authenticated, anon`.
- El alta de administrador se hace con SQL manual usando `service_role` (documentado en §19.4) o `UPDATE perfil SET rol='administrador' WHERE id = '<uuid>'` ejecutado por la propietaria.
- **Prohibido** aceptar `rol` desde registro, body, query o metadata de usuario.

---

## 12. Identidad visual

### 12.1 Sistema de origen

La identidad proviene del sistema **«Petrol Mint Vitality»**. Los cuatro colores aprobados son la **fuente de verdad** y no se sustituyen:

| Token | Nombre | HEX | Uso previsto |
|---|---|---|---|
| `color.primary` | Verde petróleo | `#1A5B5A` | Marca, acciones primarias, encabezados, tab activo |
| `color.secondary` | Verde menta | `#A2E8D3` | Fondos de apoyo, chips, ilustraciones, estados positivos suaves |
| `color.tertiary` | Ámbar | `#F5A623` | **Acento puntual**: alerta de posible fuga, badge, foco |
| `color.neutral` | Gris oscuro | `#243332` | Texto principal, iconografía, superficies oscuras |

Regla de proporción: **60 % superficies claras · 30 % primary/secondary · 10 % ámbar como máximo**. El ámbar nunca se usa como fondo de bloques grandes ni como color de texto sobre blanco.

### 12.2 Principios de interfaz

1. **Claridad financiera:** el número más importante de cada pantalla se lee en < 2 segundos.
2. **Tranquilidad, no culpa:** el lenguaje y el color no alarman; una posible fuga se presenta como «patrón para revisar».
3. **Una acción principal por pantalla**, con botón tipo píldora.
4. **Progressive disclosure:** la evidencia de una fuga se despliega bajo demanda, no se satura la lista.
5. **Consistencia:** mismos componentes y espaciados en todo el producto.
6. **Accesibilidad:** contraste AA, áreas táctiles ≥ 44×44, textos escalables, etiquetas para lectores de pantalla.

### 12.3 Tono y lenguaje (D-15)

| Usar | Evitar |
|---|---|
| «Posible fuga», «patrón detectado», «revisar» | «Derroche», «error financiero», «estás gastando mal» |
| «Tus gastos», «tu periodo» | Juicios personales |
| «Interpretación mediante reglas automáticas» | «La IA analizó…» |
| «Datos insuficientes para identificar patrones» | «No hay fugas» (cuando faltan datos) |

Todo texto de producto vive en `mobile/src/content/` y se revisa contra esta tabla.

---

## 13. Logo oficial

### 13.1 Estado verificado

| Aspecto | Verificación |
|---|---|
| Ruta | `assets/logo/logo.png` |
| Existencia | **Confirmada** |
| Dimensiones | 500 × 500 px |
| Canal | RGBA (con transparencia) |
| Colores dominantes muestreados | `#197570` (petróleo) y `#A8EFCF` (menta), coherentes con la paleta |
| Modificación permitida | **Ninguna** sobre el original |

### 13.2 Reglas de uso

1. El archivo original **no se edita, redibuja, recolorea ni recorta**.
2. Se **copia** a `mobile/assets/branding/logo.png` manteniendo bytes idénticos (verificación por hash SHA-256 en F0).
3. Ubicaciones aprobadas: pantalla de bienvenida, encabezado de autenticación, `Ajustes > Acerca de`, splash.
4. Área de respeto: mínimo 16 px alrededor; no superponer texto.
5. Fondo permitido: `#F7FAF9` (claro) o `#1A5B5A` (oscuro) según contraste; nunca sobre ámbar.
6. Tamaños: 96 px (bienvenida), 64 px (auth), 40 px (acerca de). No estirar: proporción 1:1.

### 13.3 Requisitos técnicos Android (derivados, no rediseños)

**Decisión C-08:** el logo original se conserva **sin rediseñarlo**. Los únicos recursos que se generan son los técnicos exigidos por Android, mediante **composición, escalado proporcional y márgenes**; no se redibuja el arte ni se alteran colores.

| Recurso | Requisito | Procedimiento permitido |
|---|---|---|
| Icono de app | 1024×1024 PNG, sin transparencia | **Composición técnica**: logo 500×500 centrado sobre lienzo 1024×1024 con fondo `#F7FAF9` y margen; sin redibujar |
| Adaptive icon (foreground) | 432×432 con zona segura | Logo escalado proporcionalmente sobre transparente, sin recorte del arte |
| Adaptive icon (background) | Color sólido | `#1A5B5A` o `#F7FAF9` (elegir el de mayor contraste verificado) |
| Splash | `expo-splash-screen`, logo centrado | Fondo `#F7FAF9`, logo sin deformar |
| Monochrome icon | Opcional (Android 13+) | Silueta derivada; **solo si se aprueba**, no obligatorio |

> **Limitación de resolución documentada (C-08):** el original mide 500 × 500 px y el icono de tienda exige 512×512 / 1024×1024. El escalado a 1024 introduce interpolación, por lo que la calidad máxima no está garantizada. Se documenta como **limitación conocida**; se recomienda que la propietaria entregue un máster vectorial o 1024×1024 si desea máxima calidad. Mientras tanto, el derivado técnico (composición + escalado proporcional + márgenes) es aceptable para el prototipo académico y **no** constituye un rediseño.

### 13.4 Prohibiciones

- No usar iconos genéricos de banco, alcancía o gráfico de velas como sustituto.
- No aplicar filtros, sombras duras, degradados ni cambios de saturación.
- No generar un logo nuevo "mejorado".
- No usar el logo de Stitch ni capturas de pantallas antiguas como recurso.

---

## 14. Sistema de diseño

### 14.1 Tokens de color (derivados y documentados)

```ts
// mobile/src/theme/tokens.ts (esquema)
export const colors = {
  // Marca (aprobados, inmutables)
  primary:        '#1A5B5A',
  secondary:      '#A2E8D3',
  tertiary:       '#F5A623',
  neutral:        '#243332',

  // Derivados de superficies
  primaryDark:    '#12403F',
  primaryLight:   '#2A7370',
  secondarySoft:  '#D8F6EC',
  tertiarySoft:   '#FDF0D5',

  background:     '#F7FAF9',
  surface:        '#FFFFFF',
  surfaceAlt:     '#EEF5F3',
  border:         '#D7E3E0',
  borderStrong:   '#B9CCC8',

  // Texto
  textPrimary:    '#243332',
  textSecondary:  '#5A6E6C',
  textMuted:      '#7E918E',
  textOnPrimary:  '#FFFFFF',
  textOnTertiary: '#3D2A00',

  // Estados
  success:        '#1E7A4F',
  successSoft:    '#D7F0E3',
  warning:        '#8A5A00',
  warningSoft:    '#FFF1D6',
  error:          '#B3261E',
  errorSoft:      '#F9DEDC',
  info:           '#1A5B5A',
  infoSoft:       '#DDEDEB',
} as const;
```

**Contraste verificado (AA):**

| Combinación | Ratio aprox. | Uso |
|---|---|---|
| `#243332` sobre `#FFFFFF` | 12.6:1 | Texto principal ✔ |
| `#5A6E6C` sobre `#FFFFFF` | 4.9:1 | Texto secundario ✔ |
| `#FFFFFF` sobre `#1A5B5A` | 8.2:1 | Botón primario ✔ |
| `#1A5B5A` sobre `#A2E8D3` | 5.8:1 | Chip/etiqueta ✔ |
| `#3D2A00` sobre `#F5A623` | 7.4:1 | Texto sobre ámbar ✔ |
| `#F5A623` sobre `#FFFFFF` | 2.1:1 | **Solo iconos/decoración ✘ texto** |

### 14.2 Tipografía

**Familia:** Plus Jakarta Sans (400, 500, 600, 700). Carga con `expo-font` y `@expo-google-fonts/plus-jakarta-sans`; fallback del sistema mientras carga (sin bloquear la app más de 1.5 s).

| Estilo | Tamaño / Interlínea | Peso | Uso |
|---|---|---|---|
| `display` | 32 / 38 | 700 | Cifra principal del dashboard |
| `h1` | 28 / 34 | 700 | Título de pantalla |
| `h2` | 24 / 30 | 600 | Sección |
| `h3` | 20 / 26 | 600 | Título de tarjeta |
| `body` | 16 / 24 | 400 | Texto general |
| `bodyStrong` | 16 / 24 | 600 | Énfasis |
| `bodySm` | 14 / 20 | 400 | Texto secundario |
| `label` | 14 / 20 | 600 | Etiquetas de campo |
| `button` | 16 / 20 | 600 | Botones |
| `caption` | 12 / 16 | 400 | Ayudas y metadatos |
| `overline` | 12 / 16 | 700 · tracking 0.8 | Encabezado de sección |

Reglas: máximo 2 estilos por tarjeta; no usar < 12 px; permitir escalado del sistema (`allowFontScaling`); números con `fontVariant: ['tabular-nums']` en listas y estadísticas.

### 14.3 Espaciado, radios y elevación

| Token | Valor |
|---|---|
| `space.1…8` | 4, 8, 12, 16, 20, 24, 32, 40 |
| `radius.sm/md/lg/xl/pill` | 8, 12, 16, 24, 999 |
| `elevation.0…3` | 0, 1, 3, 6 (sombras suaves, opacidad ≤ 0.08) |
| `touch.min` | 44×44 |
| `content.maxWidth` | 560 (tablet) |

### 14.4 Inventario de componentes (MVP)

| Componente | Variantes / estados | Notas |
|---|---|---|
| `Button` | primary, secondary, ghost, danger; pill; loading, disabled | Altura 52, texto `button` |
| `IconButton` | 44×44, `accessibilityLabel` obligatorio | — |
| `TextField` | label, help, error, prefix/suffix | Error debajo, borde `error` |
| `CurrencyField` | Máscara es-CO, solo enteros | Muestra `$ 8.000` |
| `DateField` | Selector acotado 2020-01-01…hoy | Default hoy |
| `CategoryPicker` | Chips horizontales, 9 categorías | Preselección del backend |
| `Card` | surface, `radius.lg`, `elevation.1` | — |
| `StatCard` | etiqueta + cifra + delta opcional | Cifra en `display` |
| `ListRow` | título, subtítulo, monto, chevron | 64 px mínimo |
| `AmountText` | POS/NEG, `tabular-nums` | Formato `$ 12.500` |
| `ProgressBar` | 0–100 %, estados | Para categorías (proporción) |
| `Badge` | info, warning, success | Ámbar para «posible fuga» |
| `EmptyState` | icono, título, texto, CTA | Obligatorio en listas |
| `ErrorState` | mensaje + reintento | Nunca culpa al usuario |
| `LoadingState` | skeletons de tarjetas/filas | Sin spinner de pantalla completa |
| `Snackbar` | éxito/error, 3 s, acción | Tras guardar gasto |
| `Sheet` | Bottom sheet para confirmaciones | Cerrar sesión, descartar borrador |
| `SegmentedControl` | Mes actual / mes anterior | Dashboard |
| `Avatar` | iniciales o imagen, 40 px | Ajustes (Should) |
| `LeakCard` | badge, categoría, descripción, ocurrencias, total | Abre evidencia |

Todos los componentes: `accessibilityRole`, `accessibilityLabel`, foco visible, soporte de texto grande y modo oscuro **no** requerido en MVP (se documenta como deuda).

### 14.5 Estados obligatorios por pantalla

| Estado | Regla |
|---|---|
| Carga | Skeleton con la forma del contenido; nunca pantalla en blanco |
| Vacío | Explica por qué no hay datos y qué hacer (p. ej. «Aún no registras gastos») |
| Error | Mensaje comprensible + botón «Reintentar»; distingue red, sesión y validación |
| Éxito | Confirmación breve y actualización visible de los datos |
| Sin permisos | Explica y ofrece alternativa (p. ej. voz → texto) |
| Offline | Aviso discreto; no se pierde el texto escrito |

### 14.6 Accesibilidad

- Contraste AA en todo texto (verificado en §14.1).
- `accessibilityLabel` en iconos y cifras compuestas («Total gastado: 125.000 pesos»).
- Orden de foco lógico; `importantForAccessibility` correcto en modales.
- No depender solo del color: los estados llevan texto e icono.
- Soporte de fuente del sistema hasta 200 % sin romper layout (probar en F13).

---

## 15. Módulos funcionales

Los 8 módulos provienen de `HISTORIAS_DE_USUARIO.md` §6. Solo los módulos 1 (parcial), 3, 5 y 6 se implementan completos en el MVP; el 8 aporta la capa transversal de privacidad.

### 15.1 M1 — Acceso, autenticación y cuentas

| Atributo | Especificación |
|---|---|
| RF / HU | RF-001, RF-002, RF-004 (MVP); RF-003, RF-005, RF-006 (ampliación) / HU-01, HU-02, HU-04; HU-03, HU-05, HU-06 |
| Reglas | Correo válido; contraseña ≥ 8; sesión única por dispositivo; identidad de Supabase; cierre revoca refresh token local y remoto |
| Pantallas | Bienvenida pública, Registro, Iniciar sesión, (Recuperar: Should), Ajustes > Cerrar sesión |
| Componentes | `Card`, `TextField`, `Button`, `Logo`, `ErrorState`, `Snackbar` |
| Endpoints | Supabase Auth (SDK) + `POST /me/bootstrap`, `GET /me` |
| Servicios | `auth` en móvil; `profiles_service.ensure_profile` |
| Persistencia | `auth.users`, `auth.identities`, `perfil` |
| Validaciones | Zod en cliente; Pydantic y constraints en servidor; mensajes en español junto al campo |
| Seguridad | Token en SecureStore; backend valida JWKS; sin secretos en cliente; sin enumeración de correos («credenciales inválidas») |
| Pruebas | Registro válido/duplicado/débil; login válido/erróneo; cierre limpia estado; pantalla pública sin sesión; guard de rutas |
| CA cubiertos | CA-01.x, CA-02.x, CA-04.x |

### 15.2 M2 — Perfil del usuario (Should, esquema preparado)

| Atributo | Especificación |
|---|---|
| RF / HU | RF-007, RF-008, RF-009 / HU-07, HU-08, HU-09 |
| Estado | **No se implementa en MVP**; `perfil` ya contiene las columnas |
| Pantallas previstas | Ajustes > Perfil, Cambiar foto |
| Endpoints previstos | `PATCH /me`, `POST /me/photo-signature` |
| Nota | El perfil existe desde F1 para sostener identidad y rol; sin UI editable en MVP |

### 15.3 M3 — Registro y gestión de gastos (núcleo del MVP)

| Atributo | Especificación |
|---|---|
| RF / HU | RF-010, RF-011, RF-012, RF-013, RF-014 (MVP); RF-015, RF-016 (ampliación) / HU-10, HU-11, HU-12, HU-13, HU-14 |
| Reglas | Texto 1–280; descripción 1–120; monto entero 1…100.000.000 COP; fecha 2020-01-01…hoy; categoría del catálogo; sin guardar sin confirmación; idempotencia 24 h; borrador solo en memoria (D-05) |
| Pantallas | `gastos/nuevo` (texto), `gastos/revisar` (formulario editable), `gastos/index` (historial) |
| Componentes | `TextField` multilínea con contador, `CurrencyField`, `DateField`, `CategoryPicker`, `PrimaryButton «Procesar con IA»`, `Card` de revisión, `ListRow`, `EmptyState`, paginación infinita |
| Endpoints | `POST /expenses/interpret`, `POST /expenses`, `GET /expenses` |
| Servicios | `expenses_service.interpret`, `.create` (transacción + idempotencia), `.list` |
| Dominio | `normalizer`, `amount_parser`, `date_parser`, `classifier`, `interpreter` |
| Persistencia | `gasto` (7 columnas de negocio + auditoría técnica); sin borradores en servidor |
| Validaciones | Servidor rechaza: monto 0/negativo/decimal/fuera de rango, fecha futura o < 2020, descripción vacía o > 120, categoría inexistente, texto > 280 o vacío, campos desconocidos |
| Seguridad | `usuario_id` del token; historial filtrado; 404 en recurso ajeno; sin texto en logs |
| Pruebas | Ver §22.4 (tabla de casos del parser) y §22.5 (idempotencia) |
| CA cubiertos | CA-10.x, CA-11.x, CA-12.x, CA-13.x, CA-14.x |

**Contrato de la interpretación (respuesta):**

```json
{
  "draft": {
    "texto": "Hoy gasté $8.000 en un taxi",
    "monto_cop": 8000,
    "fecha_gasto": "2026-11-13",
    "descripcion": "taxi",
    "categoria_id": "uuid-transporte",
    "categoria_nombre": "Transporte",
    "moneda": "COP"
  },
  "confianza": { "monto": "alta", "fecha": "alta", "categoria": "media", "descripcion": "media" },
  "avisos": ["Categoría propuesta por coincidencia de diccionario; verifícala."],
  "ambiguedades": [],
  "diccionario_version": "1.0",
  "reglas_version": "1.0"
}
```

**Regla de confirmación:** la app **solo** habilita «Guardar gasto» cuando `monto_cop` es válido, `fecha_gasto` está en rango, `descripcion` tiene 1–120 caracteres y `categoria_id` pertenece al catálogo. El backend revalida todo (RNF-004).

### 15.4 M4 — Registro por voz (Could, no MVP)

| Atributo | Especificación |
|---|---|
| RF / HU | RF-017, RF-018, RF-019 / HU-17, HU-18, HU-19 |
| Estado | **No se implementa en MVP.** El plan reserva el módulo y documenta su integración |
| Restricciones | Solo Android; `es-CO` con fallback `es`; ≤ 30 s; ≤ 280 caracteres; sin guardar audio (D-12) |
| Pantallas previstas | Botón de micrófono en `gastos/nuevo`; hoja de captura con estado «escuchando» |
| Integración | Módulo local Expo con Kotlin `SpeechRecognizer`; permisos `RECORD_AUDIO` |
| Fallback | Si no hay permiso/servicio: entrada por texto, sin bloquear |
| Pruebas previstas | Permiso concedido/denegado, silencio, timeout 30 s, transcripción > 280 (truncar con aviso), dispositivo sin reconocedor |

### 15.5 M5 — Dashboard y estadísticas (MVP)

| Atributo | Especificación |
|---|---|
| RF / HU | RF-020, RF-021 (MVP); RF-022 (ampliación) / HU-20, HU-21 |
| Reglas | Periodo por defecto: mes calendario actual en `America/Bogota`; total/cantidad/promedio con enteros; promedio redondeado a peso; desglose por categoría; empates se muestran todos; «Otros» siempre incluida |
| Pantallas | `inicio` con selector de mes, tres `StatCard` y barras por categoría |
| Componentes | `SegmentedControl`, `StatCard`, `ProgressBar`, `EmptyState`, `ErrorState` |
| Endpoints | `GET /analytics/summary`, `GET /analytics/by-category` |
| Servicios | `analytics_service.summary`, `.by_category` |
| Persistencia | Lectura agregada sobre `gasto`; sin tablas de resumen en MVP |
| Validaciones | `periodo` con formato `YYYY-MM` entre `2020-01` y el mes actual; rango `desde/hasta` inclusivo y ≤ 366 días |
| Seguridad | Agregados siempre `WHERE usuario_id = :uid`; nunca se devuelven IDs de otros |
| Pruebas | Mes vacío, un gasto, varios, cambio de mes, promedio con redondeo, categoría mayor, empate, «Otros» incluida, cifras contrastadas contra SQL manual |
| CA cubiertos | CA-20.x, CA-21.x |

**Fórmulas exactas:**
- `total_cop = SUM(monto_cop)`.
- `cantidad = COUNT(*)`.
- `promedio_cop = ROUND(total_cop / cantidad)` con `cantidad > 0`; si `cantidad = 0`, `promedio_cop = null` y la UI muestra «—».
- `porcentaje_categoria = ROUND(100.0 * suma_categoria / total_cop, 1)`; si `total_cop = 0`, no se calcula porcentaje.
- `categoria_mayor`: todas las que empatan en el máximo, ordenadas alfabéticamente.

### 15.6 M6 — Detección de posibles fugas (MVP)

| Atributo | Especificación |
|---|---|
| RF / HU | RF-023, RF-024 (MVP); RF-025, RF-026, RF-027 (ampliación) / HU-23, HU-24 |
| Regla | FUGA-01 v1.0 exacta (D-01) |
| Pantallas | `fugas/index` (lista de candidatos), `fugas/[id]` (evidencia) |
| Componentes | `LeakCard`, `Badge` ámbar, `ListRow` de gastos de soporte, `EmptyState` con dos variantes |
| Endpoints | `GET /leaks`, `GET /leaks/{id}` |
| Servicios | `leaks_service.detect_and_snapshot`, `.get_detail` |
| Dominio | `rule_fuga_01`, `grouping`, `normalizer` (compartido con gastos) |
| Persistencia | `fuga`, `fuga_evidencia`; `regla_fuga_version.parametros` es la fuente de umbrales |
| Validaciones | Ventana de 30 días; ≥ 3 gastos; ≥ 3 fechas distintas; cada gasto 1.000–30.000; suma ≥ 15.000; excluir `deleted_at`; descripciones genéricas no activan |
| Seguridad | Cálculo solo con gastos del propietario; evidencia solo de gastos propios; 404 si la fuga es ajena |
| Pruebas | Ver §22.6 (matriz de la regla) |
| CA cubiertos | CA-23.x, CA-24.x |

**Algoritmo (pseudocódigo vinculante):**

```
ventana = [hoy_local - 29 días, hoy_local]           # 30 días calendario inclusivos
gastos  = SELECT ... WHERE usuario_id = :uid
          AND deleted_at IS NULL
          AND fecha_gasto BETWEEN ventana.desde AND ventana.hasta

para cada gasto:
    si monto_cop < 1000 o monto_cop > 30000: descartar
    si descripcion_normalizada ∈ GENERICAS: descartar
    clave = (categoria_id, descripcion_normalizada)
    agrupar

para cada grupo:
    si count(gastos) >= 3
       y count(fechas distintas) >= 3
       y sum(monto_cop) >= 15000:
         emitir candidato con evidencia ordenada por fecha_gasto ASC, id ASC
```

`GENERICAS` se toma **exclusivamente** del campo `genericas` de `domain/expenses/diccionario_v1.json` (anexo C.1), que es la fuente de verdad; el código no mantiene una lista paralela. Cualquier cambio exige nueva versión del diccionario.

**Idempotencia del cálculo:** el snapshot se reemplaza de forma transaccional por `(usuario_id, regla_version_id)` (C-12): se marcan `vigente=false` los anteriores y se insertan los nuevos con su evidencia. Dos ejecuciones con los mismos datos producen el mismo conjunto (comparación por clave natural y totales). El índice único es **parcial** (`WHERE vigente = true`) para permitir recalcular el mismo día sin colisionar con el snapshot histórico.

### 15.7 M7 — Alertas, recomendaciones y metas (Could/Won't, no MVP)

| Atributo | Especificación |
|---|---|
| RF / HU | RF-025, RF-026, RF-027 (Could); RF-028, RF-029 (Won't) / HU-25 a HU-29 |
| Estado | **Fuera de alcance**. Sin pantallas ni endpoints en esta ola |
| Nota | D-11 fija notificaciones locales; D-06 y la política de cambios excluyen límites mensuales |

### 15.8 M8 — Administración y privacidad (transversal + Should)

| Atributo | Especificación |
|---|---|
| RF / HU | RF-033 (MVP, transversal); RF-030, RF-031, RF-032 (Should) / HU-33; HU-30, HU-31, HU-32 |
| En MVP | Solo la parte de **aislamiento y privacidad**: autorización por propietario, RLS, sin datos en logs, 404 uniforme, pruebas de seguridad |
| Fuera de MVP | Pantallas y endpoints administrativos, agregados con umbral ≥ 10 usuarios, auditoría |
| Pantallas previstas | `admin/usuarios` (no se construye) |
| Endpoints previstos | `GET /admin/users`, `PATCH /admin/users/{id}/status` (no se construyen) |
| Seguridad | Admin sin gastos; rol por aprovisionamiento seguro; auditoría 90 días (D-14) |
| Pruebas | Aislamiento total entre usuarios (obligatorio en MVP) |

---

## 16. Reglas de negocio

### 16.1 Dinero (D-03)

| ID | Regla |
|---|---|
| RN-DIN-01 | Moneda única COP; `moneda = 'COP'` en toda fila. |
| RN-DIN-02 | Monto entero entre 1 y 100.000.000 COP por gasto. |
| RN-DIN-03 | Sin centavos, negativos, cero ni notación científica. |
| RN-DIN-04 | Aritmética con enteros; prohibido `float` para dinero. |
| RN-DIN-05 | Formato visual `es-CO`: `$ 8.000`; aclarar «COP» cuando haya ambigüedad. |
| RN-DIN-06 | Porcentajes con un decimal y redondeo convencional; base cero ⇒ «sin base de comparación». |

### 16.2 Fechas y periodos (D-04)

| ID | Regla |
|---|---|
| RN-FEC-01 | Zona funcional `America/Bogota` en cálculo y presentación de «hoy». |
| RN-FEC-02 | `fecha_gasto` entre 2020-01-01 y la fecha local actual; sin futuro. |
| RN-FEC-03 | Orden del historial: `fecha_gasto DESC, created_at DESC, id DESC`. |
| RN-FEC-04 | Dashboard por mes calendario local; permite meses desde 2020-01. |
| RN-FEC-05 | Rangos inclusivos; SQL con límites explícitos (`>= desde AND <= hasta`). |
| RN-FEC-06 | Fuga atribuida a la ventana móvil de 30 días en que se calcula. |

### 16.3 Gastos (D-05, D-06)

| ID | Regla |
|---|---|
| RN-GAS-01 | Texto de entrada 1–280 caracteres tras recortar extremos. |
| RN-GAS-02 | Descripción final 1–120 caracteres, editable por el usuario. |
| RN-GAS-03 | Nunca se guarda sin confirmación explícita en la pantalla de revisión. |
| RN-GAS-04 | El borrador vive solo en memoria; al abandonar la pantalla se descarta (con aviso si hay cambios). |
| RN-GAS-05 | Idempotencia: UUID por intento, ventana 24 h; misma clave + mismo contenido ⇒ mismo resultado; contenido distinto ⇒ 409. |
| RN-GAS-06 | Propietario = `sub` del token; el `usuario_id` del body se ignora. |
| RN-GAS-07 | Sin borrado físico en el MVP; `deleted_at` existe y no se usa. |

### 16.4 Interpretación determinista (D-02, D-05, D-15)

| ID | Regla |
|---|---|
| RN-INT-01 | Normalización: minúsculas, sin tildes, espacios colapsados, sin signos redundantes. |
| RN-INT-02 | Monto: se aceptan formas como `8000`, `8.000`, `$ 8.000`, `$8.000`, `COP 8.000`, `8.000 pesos`. |
| RN-INT-03 | Se rechaza separador decimal con coma o punto seguido de 1–2 dígitos (`8,50`, `8.5`) por ambigüedad. |
| RN-INT-04 | Fecha: `hoy`, `ayer`, `YYYY-MM-DD`, `DD/MM`, `DD/MM/YYYY`, `DD de <mes>`. Sin coincidencia ⇒ fecha local actual con aviso. |
| RN-INT-05 | Descripción: se eliminan muletillas (`gasté`, `pagué`, `compré`, `en`, `un`, `una`) y el monto; se conserva el núcleo semántico; máximo 120. |
| RN-INT-06 | Categoría: diccionario con prioridad fija; coincidencia más larga gana; empate ⇒ «Otros» + revisión manual. |
| RN-INT-07 | Sin coincidencia de categoría ⇒ «Otros», nunca se inventa una categoría. |
| RN-INT-08 | La UI conserva la etiqueta «Procesar con IA» y muestra el aviso de D-15. |

### 16.5 Fugas (D-01, D-15)

| ID | Regla |
|---|---|
| RN-FUG-01 | Ventana de 30 días calendario inclusivos, incluido hoy, `America/Bogota`. |
| RN-FUG-02 | Agrupación por `(categoria_id, descripcion_normalizada)`. |
| RN-FUG-03 | Elegibilidad por gasto: 1.000 ≤ monto ≤ 30.000. |
| RN-FUG-04 | Umbrales: ≥ 3 gastos, ≥ 3 fechas distintas, suma ≥ 15.000. |
| RN-FUG-05 | «Otros» admite descripción informativa; descripciones genéricas no activan. |
| RN-FUG-06 | Resultado incluye regla, versión, categoría, descripción normalizada, ocurrencias, fechas, total exacto e IDs de evidencia. |
| RN-FUG-07 | Sin gastos ⇒ estado vacío; con datos insuficientes ⇒ «datos insuficientes para identificar patrones». |
| RN-FUG-08 | Determinismo: mismo conjunto de datos ⇒ mismo resultado. |
| RN-FUG-09 | Umbrales versionados; cambiarlos exige nueva versión y pruebas de regresión. |
| RN-FUG-10 | Lenguaje: «posible fuga», «patrón detectado», «revisar»; sin juicios ni promesas de ahorro. |

### 16.6 Privacidad y autorización (D-07, D-08, RNF-001)

| ID | Regla |
|---|---|
| RN-PRI-01 | Toda lectura/escritura privada exige token válido y cuenta activa. |
| RN-PRI-02 | Todo recurso privado se consulta con `usuario_id` del token. |
| RN-PRI-03 | Recurso ajeno ⇒ 404 (no 403), para no filtrar existencia. |
| RN-PRI-04 | Administrador sin acceso a gastos individuales ni a grupos < 10 usuarios. |
| RN-PRI-05 | Logs sin montos, descripciones, tokens, correos ni evidencias. |
| RN-PRI-06 | Notificaciones sin importes ni descripciones en pantalla bloqueada (Could). |

### 16.7 Cuentas y sesiones (D-06, D-09)

| ID | Regla |
|---|---|
| RN-CUE-01 | Contraseña ≥ 8 caracteres; validación también en servidor. |
| RN-CUE-02 | Correo no confirmado ⇒ no puede operar si la confirmación está activa. |
| RN-CUE-03 | Cuenta con `disabled_at` ⇒ 403 en toda ruta privada, aunque el token siga vigente. |
| RN-CUE-04 | Cierre de sesión limpia SecureStore y caché de queries. |
| RN-CUE-05 | Sin borrado de cuenta ni de gastos en el MVP. |

### 16.8 Idempotencia (D-05, RNF-005)

| ID | Regla |
|---|---|
| RN-IDM-01 | `Idempotency-Key` obligatorio en `POST /expenses`; formato UUID v4. |
| RN-IDM-02 | Clave única por usuario. |
| RN-IDM-03 | Mismo contenido ⇒ `200` con el gasto existente (sin duplicar). |
| RN-IDM-04 | Contenido distinto ⇒ `409 IDEMPOTENCY_CONFLICT`. |
| RN-IDM-05 | Pasadas 24 h, la clave se considera expirada ⇒ `409 IDEMPOTENCY_EXPIRED` (anexo D, C-03). |
| RN-IDM-06 | La comprobación y la inserción ocurren en la misma transacción. |
| RN-IDM-07 | La idempotencia es **por clave**, no por contenido: dos gastos legítimos con valores idénticos y claves distintas se registran como dos gastos. |
| RN-IDM-08 | Pasada la ventana de 24 h, la clave no se reutiliza: se responde `409 IDEMPOTENCY_EXPIRED` y la app genera una clave nueva para un intento nuevo. |

### 16.9 Retención y eliminación de datos (C-11)

**Principio.** El MVP **no** ofrece eliminación de gastos ni de cuenta desde la aplicación. Esa ausencia es una decisión de alcance, **no** un sustituto de las obligaciones de privacidad: toda solicitud legítima de eliminación de datos personales se atiende por el procedimiento administrativo de esta sección.

**Política de retención.**

| Dato | Retención | Observación |
|---|---|---|
| `perfil` (nombres, apellido, teléfono, foto) | Mientras la cuenta esté activa | Completar o corregir es posible por vía administrativa en el MVP |
| `gasto`, `fuga`, `fuga_evidencia` | Mientras la cuenta esté activa | Sin borrado lógico expuesto; `deleted_at` permanece `NULL` (C-10) |
| Cuenta desactivada (`disabled_at`) | 30 días desde la desactivación | Permite reversión y atención de solicitudes; después se elimina o anonimiza |
| Logs de aplicación | 30 días | Sin montos, descripciones, tokens ni correos (RNF-007) |
| Copias de seguridad | Según la política del proveedor de PostgreSQL | No se promete borrado inmediato en backups; se documenta al solicitar la eliminación |

**Procedimiento administrativo (solo propietaria, con rol privilegiado).**

1. Recibir la solicitud por el canal oficial definido para el proyecto y registrar fecha y folio.
2. Verificar identidad con el correo de la cuenta registrada; si no coincide, no ejecutar.
3. Confirmar por escrito el alcance (solo datos personales, o cuenta completa) y el carácter irreversible.
4. Ejecutar en una **única transacción**, en este orden por las FKs: `fuga_evidencia` → `fuga` → `gasto` → `perfil` → `auth.users(id)`.
5. Revocar sesiones activas del usuario desde Supabase Auth.
6. Verificar con consultas de conteo que no quedan filas del `usuario_id` afectado.
7. Registrar la acción en `BITACORA.md` con folio, fecha y resultado, **sin** datos financieros ni credenciales.
8. Responder a la persona solicitante dentro del plazo que fije la propietaria.

**Prohibiciones.** No se implementa un botón de eliminación en el MVP; no se usa `deleted_at` como mecanismo de borrado; no se declara una eliminación sin haber ejecutado y verificado los pasos 4–6.

---

## 17. Integraciones externas

### 17.1 Supabase (PostgreSQL + Auth) — **obligatoria**

| Aspecto | Detalle |
|---|---|
| Propósito | Persistencia única y proveedor de identidad |
| Dependencias | Proyecto Supabase, `npx supabase` CLI, `DATABASE_URL`, claves `anon` y `service_role` |
| Requisitos | Proyecto creado, migraciones aplicadas, Auth con email habilitado, redirect URLs configuradas |
| Compatibilidad | Total con FastAPI y React Native |
| Configuración | `supabase/config.toml` + variables de entorno |
| Variables | `SUPABASE_URL`, `SUPABASE_ANON_KEY` (móvil), `SUPABASE_SERVICE_ROLE_KEY` (solo backend), `DATABASE_URL` |
| Credenciales | Las genera Supabase; nunca en git |
| Automatizable | Migraciones, seeds, RLS, pruebas SQL |
| Manual | Crear proyecto, copiar claves, configurar Auth y correo |
| Costos | Plan Free (ver §23) |
| Pruebas | Conexión, migraciones idempotentes, RLS con dos usuarios |
| Alternativa si bloquea | Proyecto Supabase de pruebas independiente; en último caso, PostgreSQL local (no hay `psql`, requeriría instalación manual) |

### 17.2 Supabase Auth con Google — **Should**

| Aspecto | Detalle |
|---|---|
| Propósito | Login social (HU-03) |
| Requisitos | Proyecto en Google Cloud, OAuth consent, Client ID/Secret, redirect `https://<ref>.supabase.co/auth/v1/callback` |
| Variables | Solo en panel de Supabase (no en código) |
| Automatizable | Código de botón y manejo de sesión |
| Manual | Crear credenciales, configurar proveedor, probar consentimiento |
| Costos | Gratuito |
| Alternativa | Correo y contraseña (ya en MVP) |

### 17.3 Cloudinary — **Should**

| Aspecto | Detalle |
|---|---|
| Propósito | Almacenar foto de perfil (HU-08) |
| Requisitos | Cuenta, cloud name, API key/secret, preset o firma |
| Configuración | Backend genera firma (`timestamp` + `folder` + `upload_preset`) con `hmac-sha1`; el móvil sube directo |
| Variables | `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` (solo backend) |
| Automatizable | Endpoint de firma, validación de tipo/tamaño, actualización de `foto_url` |
| Manual | Crear cuenta y credenciales |
| Costos | Free tier con créditos mensuales (verificar al activar) |
| Alternativa | Sin foto de perfil en MVP (la app funciona con iniciales) |

### 17.4 Android `SpeechRecognizer` (Kotlin) — **Could**

| Aspecto | Detalle |
|---|---|
| Propósito | Dictado de gastos (HU-17/18/19) |
| Requisitos | Módulo local Expo, `RECORD_AUDIO`, dispositivo con reconocedor, `es-CO` |
| Compatibilidad | **Solo Android**; no funciona en Expo Go; requiere development build |
| Configuración | `app.config.ts` + `plugins/withVoz.ts` o módulo local |
| Variables | Ninguna (servicio del sistema) |
| Automatizable | Código Kotlin, permisos, UI y fallback |
| Manual | Probar en dispositivo físico; aceptar aviso de que el sistema puede procesar audio externamente |
| Costos | Gratuito (servicio del dispositivo) |
| Alternativa | Entrada por texto (siempre disponible) |

### 17.5 Expo Notifications (locales) — **Could**

| Aspecto | Detalle |
|---|---|
| Propósito | Recordatorio de posible fuga (HU-25) |
| Requisitos | `expo-notifications`, permiso `POST_NOTIFICATIONS` (Android 13+) |
| Alcance | **Solo locales**; sin push remoto ni servidor de envío (D-11) |
| Reglas | Máx. 1 por candidato/versión en 7 días; nada entre 21:00 y 08:00; texto genérico |
| Automatizable | Programación local y preferencias |
| Manual | Probar permiso concedido/denegado en dispositivo |
| Costos | Gratuito |
| Alternativa | Alerta interna en la pantalla de fugas |

### 17.6 Integraciones descartadas

| Servicio | Motivo |
|---|---|
| OpenAI / Gemini / cualquier LLM | Prohibido por D-05/D-15 |
| Firebase Cloud Messaging | Push remoto excluido |
| Pasarelas de pago | Fuera de alcance |
| MongoDB / Redis | Excluidos del stack |
| Google Analytics / Crashlytics | No aprobados; sin telemetría en MVP |

---

## 18. Auditoría MCP

### 18.1 Configuraciones revisadas

| Archivo | Contenido relevante | Estado |
|---|---|---|
| `mi-framework-ia/mcp.json` | Servidor `codegraphcontext` | Presente |
| `mi-framework-ia/opencode.json` | Configuración de OpenCode con MCP | **Modificado localmente sin commit** (no tocar) |
| `C:\Users\Loren\.config\opencode\opencode.jsonc` | MCP globales: **Context7** y **Composio** | Activos en la sesión |
| `C:\Users\Loren\.claude.json` | Sin `mcpServers` | Sin MCP de Claude |
| Configs de Cursor / Claude Desktop / VS Code | Ausentes o sin MCP | Nada que auditar |

### 18.2 Servidores detectados

| # | Nombre | Función | Ubicación | Estado verificado | Utilidad para FUGA+ | Dependencias | Costos/límites | Recomendación |
|---|---|---|---|---|---|---|---|---|
| 1 | **Context7** | Documentación actualizada de librerías | `opencode.jsonc` global | **Verificado y operativo** en esta sesión | **Alta**: Expo, Supabase, FastAPI, Cloudinary | Conexión a internet | Gratuito con límites de uso | **Mantener**. Usar antes de fijar versiones y APIs |
| 2 | **Composio** | Conectores de apps/servicios | `opencode.jsonc` global | Disponible; **no requerido** | Baja para este proyecto | Cuenta/credenciales por toolkit | Según plan | **No usar** en MVP |
| 3 | **CodeGraphContext** | Grafo de código local (Python 0.6.13 instalado) | `mi-framework-ia/mcp.json` y `opencode.json` | **Instalado pero inactivo** en esta sesión (la config vive dentro de `mi-framework-ia/`, no en la raíz) | Media, cuando exista código | Python + BD local en `~/.codegraphcontext` | Gratuito | **Opcional**. Activar solo si se trabaja desde la raíz; no es requisito |
| 4 | **Chrome DevTools MCP** | Depuración de navegador | No configurado | **No existe** | Nula (app móvil nativa) | — | — | **No instalar** |
| 5 | Playwright/Puppeteer MCP | Automatización web | No configurado | No existe | Nula | — | — | **No instalar** |

### 18.3 Conclusión

- Los MCP actuales **son suficientes** para el plan y la implementación: Context7 cubre la documentación de librerías; el resto del trabajo es código y pruebas locales.
- **No se instala ni modifica ningún MCP** (restricción del prompt §15 y §24).
- No se requiere MCP de base de datos: las migraciones se aplican con `npx supabase` y se validan con pruebas.
- Si en F14 se necesita inspección de UI Android, la herramienta adecuada es `adb`/scrcpy (manual), no un MCP de navegador.

---

## 19. Configuraciones manuales de la propietaria

> Todo lo siguiente **no puede completarlo el agente** sin credenciales, cuentas o hardware. Cada procedimiento indica cuándo, con qué, qué crear, qué necesita el código, dónde guardar, cómo comprobar y qué pasa si se pospone.

### 19.1 Crear el proyecto Supabase

| Campo | Detalle |
|---|---|
| Cuándo | Antes de F1 |
| Servicio | https://supabase.com (plan Free) |
| Qué crear | Organización + proyecto en la región más cercana (p. ej. `us-east-1` o `sa-east-1`), nombre `fuga-plus-dev` |
| Qué necesita el código | `Project URL`, `anon key`, `service_role key`, `Database password` |
| Dónde guardar | `backend/.env.local` (ignorado por git) y gestor de contraseñas; **nunca** en el repositorio |
| Cómo comprobar | `curl <url>/auth/v1/health` responde 200; `npx supabase link` conecta |
| Si se pospone | F1 no puede cerrarse; F2–F4 y las fases que requieren Auth/BD real tampoco pueden cumplir sus criterios de integración. Pueden adelantarse tareas independientes (parser determinista, componentes UI, contratos, documentación, pruebas unitarias con mocks), pero no marcar esas fases completas ni sus puertas de calidad como aprobadas. |

### 19.2 Configurar PostgreSQL y aplicar migraciones

| Campo | Detalle |
|---|---|
| Cuándo | F1 |
| Servicio | SQL Editor de Supabase o `npx supabase db push` |
| Qué crear | Base `postgres`, esquema `public`, las 7 tablas MVP, índices, triggers y políticas RLS |
| Qué necesita el código | `DATABASE_URL` (pooler) |
| Dónde guardar | `backend/.env.local`; migraciones versionadas en `supabase/migrations/` |
| Cómo comprobar | `SELECT count(*) FROM categoria;` = 9; `\d gasto` con constraints; `SELECT tablename FROM pg_tables WHERE schemaname='public';` = 7 |
| Si se pospone | Backend sin persistencia; pruebas de integración `skip` |

### 19.3 Configurar Supabase Auth

| Campo | Detalle |
|---|---|
| Cuándo | F3 |
| Servicio | Supabase Dashboard → Authentication |
| Qué crear | Email provider activo; confirmación de correo según disponibilidad de SMTP; `Site URL` y `Redirect URLs` (`fugaplus://**`, `http://localhost:8081/**`) |
| Qué necesita el código | `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_JWKS_URL`, issuer y audience |
| Dónde guardar | Variables de entorno / panel |
| Cómo comprobar | Registro de prueba crea fila en `auth.users` **y** en `perfil`; login devuelve `access_token` |
| Si se pospone | Sin registro ni login; F3 bloqueada |

### 19.4 Aprovisionar el rol Administrador (solo Should)

| Campo | Detalle |
|---|---|
| Cuándo | Ola Should (no MVP) |
| Servicio | SQL Editor con rol de servicio |
| Qué crear | `UPDATE public.perfil SET rol='administrador' WHERE id='<uuid>';` |
| Qué necesita el código | Nada adicional; el rol se lee de `perfil` |
| Dónde guardar | Registro de la acción en bitácora, sin contraseñas |
| Cómo comprobar | `GET /me` devuelve `rol: "administrador"`; el usuario no puede cambiar su rol desde la app |
| Si se pospone | HU-31/HU-32 no aplican al MVP |

### 19.5 Credenciales OAuth de Google (Should)

| Campo | Detalle |
|---|---|
| Cuándo | Ola Should |
| Servicio | Google Cloud Console → APIs & Services → Credentials |
| Qué crear | OAuth Client ID (Web), URI de redirección de Supabase, consent screen en modo prueba |
| Qué necesita el código | Ninguna clave en el móvil; Supabase gestiona el flujo |
| Dónde guardar | Panel de Supabase (Client ID/Secret) |
| Cómo comprobar | Login Google devuelve sesión y `perfil` con correo verificado |
| Si se pospone | El MVP sigue con correo y contraseña (D-10) |

### 19.6 Cloudinary (Should)

| Campo | Detalle |
|---|---|
| Cuándo | Ola Should |
| Servicio | https://cloudinary.com (plan Free) |
| Qué crear | Cuenta, `cloud_name`, API key/secret, carpeta `fuga-plus/perfiles` |
| Qué necesita el código | `CLOUDINARY_*` en backend; el móvil solo recibe firma y `upload_url` |
| Dónde guardar | `.env` del backend / gestor de secretos |
| Cómo comprobar | Firma válida permite subir un JPEG de prueba; la URL resultante se guarda en `perfil.foto_url` |
| Si se pospone | Sin foto de perfil; el resto funciona |

### 19.7 Permisos Android y build

| Campo | Detalle |
|---|---|
| Cuándo | F0 para preparar; F14 para compilar |
| Servicio | Android Studio / command-line tools |
| Qué crear | Android SDK (Platform 34/35 + Build-Tools), **JDK 17 o 21**, `ANDROID_HOME`, `adb`, un AVD o dispositivo físico con depuración USB |
| Qué necesita el código | `JAVA_HOME` apuntando a JDK 17/21 (no 23); `ANDROID_HOME`; `local.properties` con `sdk.dir` |
| Dónde guardar | Configuración del sistema (variables de usuario), no en el repo |
| Cómo comprobar | `adb devices` lista el dispositivo; `./gradlew assembleDebug` termina en `BUILD SUCCESSFUL` |
| Si se pospone | F14 bloqueada; la app no se instala; el resto se valida con pruebas |

> **Advertencia verificada:** hoy solo existe JDK 23. React Native/AGP requieren JDK 17 o 21. Instalar JDK 21 (Temurin) y **no** usar el 23 para Gradle.

### 19.8 Variables de entorno

| Archivo | Variable | Quién la usa | Secreta |
|---|---|---|---|
| `backend/.env.local` | `APP_ENV=local` | Backend | No |
| | `LOG_LEVEL=INFO` | Backend | No |
| | `SUPABASE_URL` | Backend | No |
| | `SUPABASE_JWKS_URL` | Backend | No |
| | `SUPABASE_JWT_ISSUER` | Backend | No |
| | `SUPABASE_JWT_AUDIENCE=authenticated` | Backend | No |
| | `DATABASE_URL` | Backend | **Sí** |
| | `SUPABASE_SERVICE_ROLE_KEY` | Backend (solo admin) | **Sí** |
| | `CLOUDINARY_*` | Backend (Should) | **Sí** |
| | `CORS_ORIGINS` | Backend | No |
| `mobile/.env.local` | `EXPO_PUBLIC_API_URL` | Móvil | No |
| | `EXPO_PUBLIC_SUPABASE_URL` | Móvil | No |
| | `EXPO_PUBLIC_SUPABASE_ANON_KEY` | Móvil | No (es pública por diseño) |

Reglas: `.env*` en `.gitignore`; `.env.example` con valores vacíos y comentarios; prohibido commitear claves; rotar cualquier clave que se filtre.

### 19.9 Alojamiento del backend (C-07)

| Campo | Detalle |
|---|---|
| Cuándo | Desarrollo local desde F2; despliegue remoto antes de la demostración (F14) |
| Servicio | **No se selecciona proveedor definitivo en PLAN.** Se evalúan opciones al desplegar (Render, Railway, Fly.io u otra) sin asumir plan gratuito permanente |
| Qué crear | Servicio web con `uvicorn app.main:app --host 0.0.0.0 --port $PORT`, variables de entorno y HTTPS |
| Qué necesita el código | Configuración 100 % por variables de entorno; `DATABASE_URL` de producción; `CORS_ORIGINS` restringido; sin rutas locales ni IPs fijas |
| Dónde guardar | Panel de secretos del proveedor; nunca en el repositorio |
| Cómo comprobar | `GET /health` y `GET /ready` responden 200 por HTTPS desde el dispositivo; la app apunta a esa URL con `EXPO_PUBLIC_API_URL` |
| Si se pospone | Demo con backend local en la misma red Wi-Fi (documentar IP, puerto y firewall); no se declara despliegue en nube |

**Requisitos de portabilidad exigidos (C-07):**

1. Configuración mediante variables de entorno, con validación al arranque y `.env.example` completo.
2. Dependencias reproducibles (`pyproject.toml` + lock; `package-lock.json` en móvil).
3. `EXPO_PUBLIC_API_URL` configurable en la app, sin URL de API hardcodeada.
4. Credenciales gestionadas de forma segura fuera del repositorio y del bundle.
5. Preparación para HTTPS en producción (sin `http` salvo en local).
6. Instrucciones de despliegue documentadas (`backend/docs/operacion.md` y `docs/planificacion/entrega.md`).
7. Ausencia de dependencias innecesarias de rutas locales, túneles o servicios de la máquina.

**Nota de costo:** si el proveedor elegido en F14 exige un plan de pago, se detiene y se solicita aprobación; no se activa facturación por iniciativa del agente.

### 19.10 Pruebas en dispositivo

| Campo | Detalle |
|---|---|
| Cuándo | F14 y antes de la entrega |
| Servicio | Dispositivo Android físico (recomendado) o emulador |
| Qué crear | APK debug/release instalada; datos de prueba |
| Qué necesita el código | `EXPO_PUBLIC_API_URL` accesible desde el dispositivo |
| Dónde guardar | Evidencia en `mi-framework-ia/docs/planificacion/evidencias/` (capturas, fecha) |
| Cómo comprobar | Registro → login → gasto → historial → estadísticas → fugas, sin errores |
| Si se pospone | Validación incompleta; no se puede declarar la app "instalable" |

### 19.11 Verificación de costos

| Campo | Detalle |
|---|---|
| Cuándo | Antes de activar cualquier servicio y al cierre |
| Servicio | Paneles de Supabase, Cloudinary, Google Cloud, hosting, Expo |
| Qué crear | Registro de límites y consumo |
| Dónde guardar | §23 de este plan + `docs/planificacion/costos.md` |
| Cómo comprobar | Todos los servicios en plan Free; sin método de pago activo |
| Si se pospone | Riesgo de cobro o de bloqueo por cuota |

### 19.12 Resumen de bloqueos humanos

| # | Bloqueo | Fase afectada | Impacto si no se resuelve |
|---|---|---|---|
| H1 | Crear proyecto Supabase | F1 | Sin BD ni Auth: backend no persiste |
| H2 | Configurar Auth y correo | F3 | Sin registro/login real |
| H3 | Instalar JDK 17/21 + Android SDK | F14 | Sin compilación ni instalación |
| H4 | Dispositivo o emulador | F14 | Sin validación en hardware |
| H5 | Hosting del backend (proveedor no elegido, C-07) | F14 | Demo solo en red local; el diseño ya es portable |
| H6 | Cuenta Cloudinary | Should | Sin foto de perfil |
| H7 | Credenciales Google | Should | Sin login social |

---

## 20. Fases de implementación

**Convenciones de la sección:**
- Cada fase declara los **18 atributos** exigidos por el prompt maestro.
- "Esfuerzo" se expresa en **sesiones de agente** (una sesión ≈ un bloque de trabajo con verificaciones); es una estimación relativa, **no** una garantía de duración.
- Una fase se cierra solo si sus "criterios de aceptación" se demuestran con comandos y salidas registradas.
- Todas las rutas son relativas a la raíz del repositorio.

### F0 — Preparación del repositorio y entorno

1. **Identificador:** F0.
2. **Nombre:** Bootstrap del repositorio, ramas, convenciones y línea base de versiones.
3. **Objetivo:** Dejar un repositorio listo para construir sin tocar `mi-framework-ia` ni el logo, con `develop` sincronizada, `.gitignore`, estructura de carpetas y decisiones de versiones congeladas.
4. **Requisitos e historias relacionadas:** Transversal (RNF-014). No implementa RF/HU.
5. **Dependencias:** Ninguna. Es la primera fase.
6. **Actividades detalladas:**
   - Verificar que `main` está limpio salvo el cambio local conocido en `mi-framework-ia/opencode.json`; **no** commitearlo ni revertirlo.
   - Crear `.gitignore` raíz con: `node_modules/`, `.expo/`, `dist/`, `*.log`, `.env*` (excepto `.env.example`), `backend/.venv/`, `__pycache__/`, `.pytest_cache/`, `mobile/android/`, `mobile/ios/`, `.DS_Store`, `*.keystore`, `*.jks`.
   - Crear la estructura vacía: `backend/`, `supabase/`, `mobile/`, `docs/` (raíz) y `mi-framework-ia/docs/planificacion/`.
   - Copiar este plan a `mi-framework-ia/docs/planificacion/` (ver §27).
   - Copiar `assets/logo/logo.png` a `mobile/assets/branding/logo.png` y registrar `sha256` en `mobile/docs/versiones.md`.
   - Crear `backend/.env.example` y `mobile/.env.example`.
   - Resolver versiones con `npx create-expo-app@latest` (proyecto temporal) y `pip index versions fastapi`; congelar en `mobile/docs/versiones.md` y `backend/pyproject.toml`.
   - Crear `docs/planificacion/PROGRESO_BUILD.md` con la plantilla de §25.
   - Definir convenciones: Conventional Commits, nombres de ramas (`main`, `develop`), prefijos de archivos y idioma del código (identificadores en inglés, textos en español).
7. **Archivos y carpetas:** `.gitignore`, `docs/planificacion/`, `mi-framework-ia/docs/planificacion/PLAN_MAESTRO_IMPLEMENTACION_FUGA_PLUS.md`, `mobile/docs/versiones.md`, `backend/.env.example`, `mobile/.env.example`.
8. **Frontend:** Solo estructura y decisión de SDK; no se crea app todavía.
9. **Backend:** Solo estructura y `pyproject.toml` inicial con dependencias fijadas.
10. **Base de datos:** Nada aún.
11. **Integraciones:** Ninguna activa.
12. **Comandos necesarios:** `git status`, `git branch -a`, `node -v`, `npm -v`, `python --version`, `java -version`, `npx create-expo-app@latest --help`, `Get-FileHash assets/logo/logo.png -Algorithm SHA256`.
13. **Pruebas:** `git status` muestra solo el cambio preexistente; el hash del logo copiado coincide con el original; el plan existe en ambas rutas con el mismo hash.
14. **Criterios de aceptación:** (a) `develop` creada y sincronizada con `main`; (b) `.gitignore` cubre secretos y artefactos; (c) versiones congeladas y documentadas; (d) logo byte-idéntico; (e) `mi-framework-ia` sin cambios funcionales.
15. **Entregables:** repositorio preparado, plan copiado, `versiones.md`, plantilla de progreso.
16. **Riesgos:** commitear por error `opencode.json`; ignorar `android/` cuando se necesite parche nativo; fijar una versión de Expo incompatible con el SDK elegido.
17. **Condiciones de continuación:** estructura creada, `develop` activa, hash del logo verificado, plan en el repositorio.
18. **Estimación de esfuerzo:** 1–2 sesiones.

### F1 — Supabase: esquema MVP, migraciones, seeds y RLS

1. **Identificador:** F1.
2. **Nombre:** Base de datos MVP en Supabase.
3. **Objetivo:** Crear las 7 tablas MVP con restricciones, índices, triggers, catálogo sembrado, regla FUGA-01 v1.0 y RLS activo, aplicables de forma idempotente.
4. **Requisitos e historias relacionadas:** Base de RF-013, RF-014, RF-020, RF-021, RF-023, RF-024, RF-033; HU-13, HU-14, HU-20, HU-21, HU-23, HU-24, HU-33. RNF-001, RNF-005, RNF-016.
5. **Dependencias:** F0; proyecto Supabase creado (H1 de §19.1).
6. **Actividades detalladas:**
   - Inicializar `supabase/config.toml` con `npx supabase init`.
   - Escribir migraciones 0001–0007 según §9.6.
   - Modelar `fuga.regla_version_id` como UUID FK → `regla_fuga_version(id)` (C-12) y el índice único **parcial** del snapshot (§9.2.6).
   - Implementar `set_updated_at()` y `handle_new_user()` (crea `perfil` con `rol='usuario'`).
   - Cargar seed del catálogo (9 categorías) y `regla_fuga` FUGA-01 + versión 1.0 con `parametros` JSONB.
   - Activar RLS y escribir políticas de §9.4; revocar escritura a `anon`/`authenticated` en `gasto`, `fuga`, `fuga_evidencia`.
   - Aplicar con `npx supabase db push` y verificar idempotencia reaplicando.
   - Crear `supabase/tests/rls_test.sql` con dos usuarios simulados.
   - Documentar en `supabase/docs/esquema.md` el mapa tabla → HU.
7. **Archivos y carpetas:** `supabase/config.toml`, `supabase/migrations/0001…0007`, `supabase/seed.sql`, `supabase/tests/rls_test.sql`, `supabase/docs/esquema.md`.
8. **Frontend:** Ninguno.
9. **Backend:** Ninguno todavía; solo `DATABASE_URL` en `.env.local`.
10. **Base de datos:** `categoria`, `regla_fuga`, `regla_fuga_version`, `perfil`, `gasto`, `fuga`, `fuga_evidencia`.
11. **Integraciones:** Supabase (PostgreSQL + Auth trigger).
12. **Comandos necesarios:** `npx supabase init`, `npx supabase link --project-ref <ref>`, `npx supabase db push`, `npx supabase db lint`.
13. **Pruebas:** reaplicar migraciones sin error; `SELECT count(*) FROM categoria` = 9; insertar gasto con monto 0 o fecha anterior a `2020-01-01` falla con violación de CHECK; dos gastos con la misma `(usuario_id, clave_idempotencia)` fallan por UQ; RLS probado con rol sujeto a políticas (el cliente no puede leer directamente `gasto`). **La fecha futura no se rechaza por CHECK en F1:** se verifica mediante prueba de API `422` en F6 con fecha de servidor `America/Bogota` y se vuelve a probar en F13.
14. **Criterios de aceptación:** esquema completo y reproducible desde cero; catálogo correcto; restricciones activas; RLS probado con dos identidades; ninguna tabla fuera del alcance MVP.
15. **Entregables:** migraciones, seed, pruebas RLS, documentación del esquema.
16. **Riesgos:** pooler/credenciales mal configuradas; trigger de `auth.users` sin permisos; políticas RLS que bloqueen al backend; diferencias entre proyecto local y remoto.
17. **Condiciones de continuación:** `npx supabase db lint` sin errores críticos; pruebas RLS en verde; catálogo consultable.
18. **Estimación de esfuerzo:** 3–4 sesiones.

### F2 — Esqueleto backend y seguridad transversal

1. **Identificador:** F2.
2. **Nombre:** API base FastAPI con configuración, errores, logs y verificación de token.
3. **Objetivo:** Levantar un backend ejecutable con `/health`, `/ready`, manejo centralizado de errores, logging seguro, conexión a BD y dependencia de autenticación reutilizable.
4. **Requisitos e historias relacionadas:** RNF-001, RNF-004, RNF-007, RNF-008, RNF-012; habilita RF-033 y todas las rutas privadas.
5. **Dependencias:** F1.
6. **Actividades detalladas:**
   - Crear `pyproject.toml` con dependencias fijadas y `ruff`/`pytest` configurados.
   - Implementar `Settings` con `pydantic-settings` y validación de variables obligatorias al arranque.
   - Crear `main.py` con routers, `CORSMiddleware`, middleware de correlación y handlers de error.
   - Implementar `errors.py` con la jerarquía de §6.5 y el mapeo a HTTP.
   - Implementar `security.py` con JWKS, validación de claims y `CurrentUser` (incluye `disabled_at`).
   - Implementar `db/session.py` con pool y contexto transaccional.
   - Configurar logging con filtro de claves sensibles.
   - Escribir pruebas base: `/health`, `/ready`, 401 sin token, 401 token inválido, 403 cuenta deshabilitada.
   - Añadir `backend/docs/operacion.md` con comandos de arranque.
7. **Archivos y carpetas:** `backend/app/{main.py,core/*,api/deps.py,api/v1/{router.py,health.py},db/session.py}`, `backend/tests/{api,security}`, `backend/pyproject.toml`, `backend/.env.example`.
8. **Frontend:** Ninguno.
9. **Backend:** Esqueleto completo y dependencias de autorización.
10. **Base de datos:** Conexión y consulta de `perfil` para autorización.
11. **Integraciones:** Supabase Auth (JWKS) y PostgreSQL.
12. **Comandos necesarios:** `python -m venv .venv`, `.venv\Scripts\activate`, `pip install -e ".[dev]"`, `uvicorn app.main:app --reload`, `pytest -q`, `ruff check .`.
13. **Pruebas:** unitarias de configuración; API de health; seguridad de token; filtro de logs (capturar salida y buscar `monto_cop`, `token`, `password`).
14. **Criterios de aceptación:** servidor arranca; `/health` 200 y `/ready` 200 con BD; toda ruta privada devuelve 401 sin token; los errores tienen `code` y `correlation_id`; los logs pasan el test de datos sensibles.
15. **Entregables:** backend ejecutable, suite base, documentación de operación.
16. **Riesgos:** versión de `psycopg`/SQLAlchemy incompatible con Python 3.12; JWKS inaccesible; CORS mal configurado.
17. **Condiciones de continuación:** `pytest` en verde (unit + api); `ruff` sin errores; `/ready` verifica BD real.
18. **Estimación de esfuerzo:** 4–5 sesiones.

### F3 — Autenticación, sesión y registro (HU-01 backend / HU-02 / HU-04)

1. **Identificador:** F3.
2. **Nombre:** Identidad y ciclo de sesión.
3. **Objetivo:** Permitir registro, inicio y cierre de sesión reales con Supabase Auth, y garantizar que el backend reconoce al usuario en cada request.
4. **Requisitos e historias relacionadas:** RF-001, RF-002, RF-004; HU-01, HU-02, HU-04; RNF-003, RNF-009.
5. **Dependencias:** F2; Auth configurado (§19.3).
6. **Actividades detalladas:**
   - Implementar `POST /me/bootstrap` idempotente y `GET /me`.
   - Implementar `profiles_service.ensure_profile` con manejo de carrera (dos llamadas simultáneas).
   - Verificar que el trigger de F1 y el bootstrap son compatibles.
   - Definir la política de errores de autenticación (mensajes sin enumeración de correos).
   - Documentar el flujo de confirmación de correo y el caso "correo no configurado".
   - Preparar pruebas con tokens reales del proyecto de pruebas (dos usuarios).
   - (Frontend se implementa en F9; aquí solo contratos y pruebas de API.)
7. **Archivos y carpetas:** `backend/app/api/v1/{me.py,router.py}`, `services/profiles_service.py`, `repositories/profiles.py`, `schemas/auth.py`, `tests/api/test_me.py`, `tests/security/test_auth_flows.py`.
8. **Frontend:** Solo consumo documentado; sin pantallas.
9. **Backend:** Endpoints de identidad y perfil.
10. **Base de datos:** `perfil` (lectura/creación).
11. **Integraciones:** Supabase Auth.
12. **Comandos necesarios:** `pytest tests/api/test_me.py -q`, `pytest tests/security/test_auth_flows.py -q`.
13. **Pruebas:** bootstrap crea perfil una sola vez; `GET /me` devuelve rol y estado; token de usuario deshabilitado → 403; dos llamadas concurrentes a bootstrap → un solo perfil.
14. **Criterios de aceptación:** un usuario registrado en Supabase obtiene `GET /me` 200 con `rol: "usuario"`; no se puede crear un `perfil` con rol elevado; errores uniformes.
15. **Entregables:** API de identidad + pruebas.
16. **Riesgos:** desfase entre trigger y bootstrap; tokens de prueba caducados; correo sin configurar que bloquea el registro.
17. **Condiciones de continuación:** pruebas de identidad en verde con dos usuarios reales del proyecto de pruebas.
18. **Estimación de esfuerzo:** 2–3 sesiones.

### F4 — Autorización por propietario, perfil base y aislamiento

1. **Identificador:** F4.
2. **Nombre:** Núcleo de autorización y privacidad (RF-033).
3. **Objetivo:** Establecer el patrón obligatorio de scoping por propietario en repositorios y demostrarlo con pruebas de aislamiento antes de construir features.
4. **Requisitos e historias relacionadas:** RF-033; HU-33; RNF-001, RNF-002, RNF-007.
5. **Dependencias:** F3.
6. **Actividades detalladas:**
   - Definir `repositories/base.py` con helper que exige `usuario_id`.
   - Implementar `categories.py` (catálogo) con lectura autenticada.
   - Implementar un endpoint temporal de "ping privado" para probar el scoping (se retira en F6).
   - Escribir la matriz de pruebas de seguridad de §10.8 como suite parametrizada.
   - Documentar la regla "todo repositorio privado recibe `uid`" en `backend/docs/seguridad.md`.
   - Revisar RLS de F1 contra el acceso del backend y del cliente.
7. **Archivos y carpetas:** `repositories/{base,categories,profiles}.py`, `tests/security/test_ownership.py`, `backend/docs/seguridad.md`.
8. **Frontend:** Ninguno.
9. **Backend:** Patrón de autorización y catálogo.
10. **Base de datos:** `categoria` (seed) y `perfil`.
11. **Integraciones:** Supabase.
12. **Comandos necesarios:** `pytest tests/security -q`.
13. **Pruebas:** usuario A no ve datos de B; 404 uniforme; cuenta deshabilitada bloqueada; catálogo devuelve 9 categorías ordenadas. Para validar el aislamiento, utilizar endpoints FastAPI y conexión privilegiada real con datos A/B; contrastar por separado RLS bajo `authenticated`. Si aún no existe el endpoint financiero, ejecutar una ruta de prueba que use el repositorio real y repetir la matriz completa en F6/F8/F13.
14. **Criterios de aceptación:** suite de seguridad en verde; ningún repositorio privado sin `uid`; catálogo estable.
15. **Entregables:** capa de autorización + suite de aislamiento.
16. **Riesgos:** relajar el scoping "temporalmente" y olvidar revertirlo; confiar solo en RLS.
17. **Condiciones de continuación:** `pytest tests/security` 100 % verde y revisado.
18. **Estimación de esfuerzo:** 3–4 sesiones.

### F5 — Motor determinista de interpretación de gastos

1. **Identificador:** F5.
2. **Nombre:** Parser, normalizador y clasificador (dominio puro).
3. **Objetivo:** Convertir texto libre en un borrador estructurado (monto, fecha, descripción, categoría) con reglas deterministas versionadas y sin dependencias externas.
4. **Requisitos e historias relacionadas:** RF-010, RF-011, RF-012; HU-10, HU-11, HU-12; RNF-004, RNF-010, RNF-014.
5. **Dependencias:** F4 (catálogo).
6. **Actividades detalladas:**
   - Implementar `normalizer.py` (minúsculas, sin tildes, colapsar espacios, limpiar signos).
   - Implementar `amount_parser.py` con la gramática de RN-INT-02/03 y rechazo de decimales.
   - Implementar `date_parser.py` con las formas de RN-INT-04 y default hoy local.
   - Implementar `classifier.py` con diccionario v1.0 (categoría → palabras clave), prioridad por longitud y empate → Otros.
   - Implementar `interpreter.py` que produce `Draft` + `confianza` + `avisos` + versión de diccionario/reglas.
   - Crear `domain/expenses/diccionario_v1.json` (versionado) con categorías, sinónimos y genéricos.
   - Endpoint `POST /expenses/interpret` que **no persiste**.
   - Construir la tabla de casos de prueba de §22.4 (≥ 40 frases).
7. **Archivos y carpetas:** `backend/app/domain/expenses/*`, `backend/app/api/v1/expenses.py` (solo interpret), `backend/app/schemas/expenses.py`, `backend/tests/unit/domain/*`.
8. **Frontend:** Ninguno (contrato definido en §15.3).
9. **Backend:** Dominio + endpoint de interpretación.
10. **Base de datos:** Solo lectura de `categoria`.
11. **Integraciones:** Ninguna.
12. **Comandos necesarios:** `pytest tests/unit/domain -q`, `pytest tests/api/test_interpret.py -q`.
13. **Pruebas:** tabla de §22.4; determinismo (misma entrada ⇒ misma salida); texto vacío/281 caracteres ⇒ 422; entrada sin monto ⇒ aviso y monto nulo; fecha futura en texto ⇒ se ignora y se usa hoy con aviso.
14. **Criterios de aceptación:** ≥ 90 % de acierto en el corpus de frases de prueba; cero excepciones no controladas; todos los campos del borrador editables; nada persistido.
15. **Entregables:** motor de interpretación, diccionario v1.0, corpus de pruebas.
16. **Riesgos:** ambigüedad de montos con puntos; falsos positivos de categoría; frases con múltiples montos.
17. **Condiciones de continuación:** corpus en verde; revisión manual de 10 frases reales con resultado aceptable.
18. **Estimación de esfuerzo:** 5–7 sesiones.

### F6 — API de gastos: creación idempotente y consulta

1. **Identificador:** F6.
2. **Nombre:** Persistencia, idempotencia e historial.
3. **Objetivo:** Guardar gastos confirmados bajo el propietario con idempotencia estricta y servirlos paginados en orden estable.
4. **Requisitos e historias relacionadas:** RF-012, RF-013, RF-014; HU-12, HU-13, HU-14; RNF-004, RNF-005, RNF-006, RNF-012.
5. **Dependencias:** F5.
6. **Actividades detalladas:**
   - Implementar `expenses_service.create` con transacción, validación de categoría y control de idempotencia.
   - Definir comparación de contenido (monto, fecha, descripción, categoría) para decidir 200 vs 409.
   - Implementar expiración de 24 h (RN-IDM-05).
   - Implementar `GET /expenses` con cursor opaco y filtros mínimos (no se implementan filtros avanzados: RF-015 es Should).
   - Implementar `GET /expenses/{id}` (solo lectura propia; útil para la app).
   - Añadir pruebas de concurrencia (dos POST simultáneos con la misma clave).
   - Verificar que `usuario_id` del body se ignora.
7. **Archivos y carpetas:** `backend/app/api/v1/expenses.py`, `services/expenses_service.py`, `repositories/expenses.py`, `schemas/expenses.py`, `tests/api/test_expenses.py`, `tests/integration/test_idempotency.py`.
8. **Frontend:** Ninguno.
9. **Backend:** Endpoints de gastos.
10. **Base de datos:** `gasto`.
11. **Integraciones:** Supabase PostgreSQL.
12. **Comandos necesarios:** `pytest tests/api/test_expenses.py -q`, `pytest tests/integration -q -m integration`.
13. **Pruebas:** creación válida 201; misma clave mismo contenido 200 (un solo registro); misma clave distinto contenido 409; clave expirada 409; monto inválido 422; fecha futura 422 (fecha del servidor en `America/Bogota`, sin confiar en el reloj móvil); categoría inexistente 422; listado paginado sin duplicados ni huecos; gasto ajeno 404.
14. **Criterios de aceptación:** ninguna ruta permite crear un gasto con `usuario_id` ajeno; la idempotencia se demuestra con prueba concurrente; el orden del historial es exactamente `fecha_gasto DESC, created_at DESC, id DESC`.
15. **Entregables:** API de gastos completa (MVP) + pruebas de integridad.
16. **Riesgos:** carrera de idempotencia sin UQ; cursor mal codificado; fechas con zona horaria incorrecta.
17. **Condiciones de continuación:** todas las pruebas de §22.5 en verde; revisión de SQL sin `SELECT *`.
18. **Estimación de esfuerzo:** 4–6 sesiones.

### F7 — Estadísticas y agregados (HU-20 / HU-21)

1. **Identificador:** F7.
2. **Nombre:** Dashboard analítico del backend.
3. **Objetivo:** Calcular total, cantidad, promedio y desglose por categoría por periodo, exclusivamente con gastos del propietario.
4. **Requisitos e historias relacionadas:** RF-020, RF-021; HU-20, HU-21; RNF-006, RNF-013.
5. **Dependencias:** F6.
6. **Actividades detalladas:**
   - Implementar `analytics/aggregations.py` con las fórmulas de §15.5.
   - Implementar `GET /analytics/summary` y `GET /analytics/by-category`.
   - Resolver periodo: `periodo=YYYY-MM` o `desde/hasta`; default mes actual local.
   - Garantizar redondeo entero del promedio y porcentajes a 1 decimal.
   - Incluir «Otros» siempre; empates devueltos completos.
   - Añadir índices si el plan de consulta lo requiere (verificar con `EXPLAIN`).
7. **Archivos y carpetas:** `backend/app/domain/analytics/aggregations.py`, `api/v1/analytics.py`, `services/analytics_service.py`, `repositories/expenses.py` (consultas agregadas), `tests/api/test_analytics.py`.
8. **Frontend:** Ninguno.
9. **Backend:** Agregados y endpoints.
10. **Base de datos:** Lectura de `gasto` + `categoria`.
11. **Integraciones:** Ninguna adicional.
12. **Comandos necesarios:** `pytest tests/api/test_analytics.py -q`.
13. **Pruebas:** periodo vacío; un gasto; varios; cambio de mes; promedio con `.5`; categoría mayor; empate; «Otros» incluida; usuario B no altera cifras de A.
14. **Criterios de aceptación:** cifras idénticas a un cálculo SQL manual de control; sin `float` en la ruta de dinero; periodo inválido ⇒ 422.
15. **Entregables:** API analítica + pruebas de contraste.
16. **Riesgos:** desfase de zona horaria en el borde del mes; redondeo inconsistente entre backend y app.
17. **Condiciones de continuación:** contraste SQL manual reproducible y documentado en la bitácora.
18. **Estimación de esfuerzo:** 3–4 sesiones.

### F8 — Detección de posibles fugas y evidencia (HU-23 / HU-24)

1. **Identificador:** F8.
2. **Nombre:** Regla FUGA-01 v1.0 y snapshot de evidencia.
3. **Objetivo:** Detectar patrones de gasto bajo demanda, con umbrales versionados y evidencia trazable a gastos reales del propietario.
4. **Requisitos e historias relacionadas:** RF-023, RF-024; HU-23, HU-24; RNF-006, RNF-014; D-01, D-15.
5. **Dependencias:** F7 (agregados y lectura de gastos).
6. **Actividades detalladas:**
   - Implementar `grouping.py` (clave `categoria_id + descripcion_normalizada`, lista de genéricos).
   - Implementar `rule_fuga_01.py` con parámetros inyectados desde `regla_fuga_version.parametros`.
   - Implementar `leaks_service.detect_and_snapshot` transaccional: invalidar el snapshot anterior de `(usuario_id, regla_version_id)` e insertar el nuevo con evidencia (C-12).
   - Implementar `GET /leaks` (dispara cálculo bajo demanda) y `GET /leaks/{id}` (detalle con gastos de soporte).
   - Distinguir tres estados: sin gastos, datos insuficientes, candidatos.
   - Garantizar lenguaje D-15 en todos los textos de respuesta.
   - Añadir pruebas de determinismo y de regresión de umbrales.
7. **Archivos y carpetas:** `backend/app/domain/leaks/{rule_fuga_01,grouping}.py`, `services/leaks_service.py`, `repositories/leaks.py`, `api/v1/leaks.py`, `schemas/leaks.py`, `tests/unit/domain/test_rule_fuga_01.py`, `tests/api/test_leaks.py`.
8. **Frontend:** Ninguno.
9. **Backend:** Motor de fugas + endpoints.
10. **Base de datos:** `fuga`, `fuga_evidencia`, `regla_fuga`, `regla_fuga_version`, `gasto`.
11. **Integraciones:** Ninguna.
12. **Comandos necesarios:** `pytest tests/unit/domain/test_rule_fuga_01.py -q`, `pytest tests/api/test_leaks.py -q`.
13. **Pruebas:** matriz de §22.6 (≥ 18 casos: umbral exacto, un gasto fuera de rango, dos fechas, suma 14.999, etc.); determinismo; snapshot no duplica; fuga ajena 404; gasto eliminado lógicamente no cuenta.
14. **Criterios de aceptación:** todos los casos de borde de §22.6 en verde; una fuga siempre tiene ≥ 3 evidencias; el detalle muestra total exacto y fechas; nunca se exponen gastos de otro usuario.
15. **Entregables:** regla implementada, snapshot, endpoints y pruebas.
16. **Riesgos:** agrupar por categoría sola (falsos positivos); zona horaria en el borde de los 30 días; descripciones genéricas que activan la regla.
17. **Condiciones de continuación:** suite de la regla en verde y revisada contra D-01 línea por línea.
18. **Estimación de esfuerzo:** 5–6 sesiones.

### F9 — Sistema de diseño, navegación y pantallas públicas/autenticación

1. **Identificador:** F9.
2. **Nombre:** Shell de la app, tema y flujos de entrada.
3. **Objetivo:** Construir la app Expo con tokens visuales, navegación protegida y pantallas de bienvenida, registro, inicio y cierre de sesión.
4. **Requisitos e historias relacionadas:** RF-001, RF-002, RF-004; HU-01, HU-02, HU-04; RNF-009, RNF-011.
5. **Dependencias:** F3 (API de identidad) y F0 (SDK congelado).
6. **Actividades detalladas:**
   - Crear el proyecto Expo con TypeScript y Expo Router.
   - Implementar `tokens.ts`, `typography.ts`, `ThemeProvider` y carga de Plus Jakarta Sans.
   - Implementar componentes base: `Button`, `TextField`, `Card`, `Logo`, `ErrorState`, `LoadingState`, `Snackbar`.
   - Implementar `supabase.ts` con `expo-secure-store` fragmentado y `autoRefreshToken`.
   - Implementar layouts `(auth)` y `(app)` con guard de sesión y redirección.
   - Pantalla de bienvenida con propuesta de valor, logo y CTA.
   - Pantallas de registro y login con validación Zod y errores junto al campo.
   - Cierre de sesión en Ajustes con confirmación en `Sheet`.
   - Configurar `app.config.ts` (nombre, slug, package `com.fugaplus.app`, iconos y splash derivados).
7. **Archivos y carpetas:** `mobile/app/**`, `mobile/src/{theme,components,lib,features/auth,content}`, `mobile/app.config.ts`, `mobile/package.json`, `mobile/tsconfig.json`.
8. **Frontend:** Shell completo + 4 pantallas.
9. **Backend:** Consumo de `/me/bootstrap`, `/me`.
10. **Base de datos:** Ninguna directa.
11. **Integraciones:** Supabase Auth.
12. **Comandos necesarios:** `npx expo start --dev-client`, `npx tsc --noEmit`, `npm test`.
13. **Pruebas:** RNTL de Button/TextField/Logo; flujo de registro (mock de Supabase); guard de rutas; cierre de sesión limpia SecureStore y queries; `tsc --noEmit` sin errores.
14. **Criterios de aceptación:** app arranca en development build; un usuario puede registrarse, iniciar sesión y cerrar sesión; ninguna ruta privada accesible sin sesión; tokens visuales aplicados sin colores hardcodeados fuera de `theme/`.
15. **Entregables:** app shell, tema, autenticación móvil.
16. **Riesgos:** límite de tamaño de SecureStore; fuentes que bloquean el splash; `EXPO_PUBLIC_API_URL` inalcanzable desde el dispositivo.
17. **Condiciones de continuación:** flujo de auth completo contra el backend local; `tsc` y lint limpios.
18. **Estimación de esfuerzo:** 6–8 sesiones.

### F10 — Flujo móvil de captura, revisión y confirmación (HU-10/11/12/13)

1. **Identificador:** F10.
2. **Nombre:** Registro de gasto por texto de extremo a extremo.
3. **Objetivo:** Permitir escribir un gasto, interpretarlo, revisarlo, corregirlo y guardarlo con idempotencia y manejo de errores de red.
4. **Requisitos e historias relacionadas:** RF-010, RF-011, RF-012, RF-013; HU-10, HU-11, HU-12, HU-13; RNF-009, RNF-012.
5. **Dependencias:** F6 (API de gastos) y F9 (shell).
6. **Actividades detalladas:**
   - Pantalla `gastos/nuevo`: `TextInput` multilínea con contador 280, botón «Procesar con IA» y aviso D-15.
   - Hook `useInterpretExpense` con TanStack Query (`mutation`), reintento manual y conservación del texto ante error.
   - Pantalla `gastos/revisar`: formulario con `CurrencyField`, `DateField`, `CategoryPicker`, descripción editable y confianza por campo.
   - Bloqueo de «Guardar» hasta que el formulario sea válido; advertencia al descartar cambios.
   - Generación de `Idempotency-Key` con `crypto.randomUUID()` por intento; reintento reutiliza la misma clave.
   - Manejo de 409/422/401/5xx con mensajes específicos y acción útil.
   - Invalidación de `expenses`, `analytics` y `leaks` tras guardar.
   - Snackbar de éxito y navegación al historial.
7. **Archivos y carpetas:** `mobile/app/(app)/gastos/{nuevo,revisar}.tsx`, `mobile/src/features/expenses/*`, `mobile/src/components/{CurrencyField,DateField,CategoryPicker}.tsx`.
8. **Frontend:** Dos pantallas y sus hooks.
9. **Backend:** `POST /expenses/interpret`, `POST /expenses` (ya existentes).
10. **Base de datos:** `gasto` (vía API).
11. **Integraciones:** Ninguna.
12. **Comandos necesarios:** `npm test -- expenses`, `npx tsc --noEmit`.
13. **Pruebas:** flujo feliz; texto vacío; 281 caracteres; sin monto; error de red conserva texto; doble tap en guardar produce un solo gasto; 409 muestra conflicto; descartar advierte.
14. **Criterios de aceptación:** un gasto se registra en ≤ 4 interacciones desde el inicio; nunca se guarda sin confirmación; el doble envío no duplica; los errores son comprensibles y no culpan al usuario.
15. **Entregables:** flujo completo de registro por texto.
16. **Riesgos:** teclado numérico y máscara de moneda; pérdida de estado al navegar; claves de idempotencia regeneradas en reintento.
17. **Condiciones de continuación:** flujo E2E manual en dev build + pruebas de componentes en verde.
18. **Estimación de esfuerzo:** 6–8 sesiones.

### F11 — Historial, dashboard y ajustes en la app (HU-14/20/21)

1. **Identificador:** F11.
2. **Nombre:** Consulta de gastos y estadísticas.
3. **Objetivo:** Mostrar el historial paginado, el resumen del periodo y el desglose por categoría con estados vacíos y de error.
4. **Requisitos e historias relacionadas:** RF-014, RF-020, RF-021; HU-14, HU-20, HU-21; RNF-009, RNF-013.
5. **Dependencias:** F7 y F10.
6. **Actividades detalladas:**
   - Historial con `FlatList` paginada por cursor (20 por carga, máximo 50, carga adicional al desplazarse — C-04), `ListRow`, `AmountText` y `EmptyState`.
   - Pull-to-refresh e invalidación tras guardar.
   - Dashboard con `SegmentedControl` (mes actual/anterior), tres `StatCard` y barras por categoría.
   - Formato `es-CO` centralizado (`formatCOP`, `formatDate`, `formatPercent`).
   - Estado «sin base de comparación» cuando el periodo no tiene datos.
   - Ajustes: cerrar sesión, versión, aviso de privacidad y texto de transparencia.
7. **Archivos y carpetas:** `mobile/app/(app)/{inicio,gastos/index,ajustes}.tsx`, `mobile/src/features/{expenses,analytics}`, `mobile/src/lib/format.ts`.
8. **Frontend:** Tres pantallas.
9. **Backend:** `GET /expenses`, `GET /analytics/*`.
10. **Base de datos:** Lectura vía API.
11. **Integraciones:** Ninguna.
12. **Comandos necesarios:** `npm test -- history analytics`, `npx tsc --noEmit`.
13. **Pruebas:** lista vacía; 25 gastos con paginación; orden correcto; cambio de mes; promedio; categoría mayor; empate; error de red con reintento; formato de moneda con miles.
14. **Criterios de aceptación:** cifras de la app coinciden con el backend; el scroll no recarga todo; los estados vacío/error/carga existen en todas las pantallas.
15. **Entregables:** historial, dashboard y ajustes funcionales.
16. **Riesgos:** listas largas y rendimiento; desfase de formato entre plataformas; fechas en el borde del mes.
17. **Condiciones de continuación:** pruebas de componentes + verificación manual con 30 gastos sembrados.
18. **Estimación de esfuerzo:** 5–7 sesiones.

### F12 — Pantalla de fugas, evidencia y privacidad de la UX (HU-23/24/33)

1. **Identificador:** F12.
2. **Nombre:** Posibles fugas y cierre de privacidad en la interfaz.
3. **Objetivo:** Presentar candidatos y su evidencia con lenguaje D-15, y demostrar que la app nunca muestra datos de terceros.
4. **Requisitos e historias relacionadas:** RF-023, RF-024, RF-033; HU-23, HU-24, HU-33; RNF-002, RNF-009.
5. **Dependencias:** F8 y F11.
6. **Actividades detalladas:**
   - Lista de fugas con `LeakCard`: badge ámbar, categoría, descripción, ocurrencias, total.
   - Detalle con regla y versión, ventana de fechas, total exacto y lista de gastos de soporte.
   - Tres estados: sin gastos, datos insuficientes, con candidatos.
   - Textos de D-15 en `src/content/fugas.ts`; prohibido lenguaje de culpa.
   - Recalcular al volver a la pantalla y tras guardar un gasto.
   - Revisión de accesibilidad de cifras y badges (etiquetas completas).
7. **Archivos y carpetas:** `mobile/app/(app)/fugas/{index,[id]}.tsx`, `mobile/src/features/leaks/*`, `mobile/src/components/{LeakCard,Badge}.tsx`, `mobile/src/content/fugas.ts`.
8. **Frontend:** Dos pantallas y componentes.
9. **Backend:** `GET /leaks`, `GET /leaks/{id}`.
10. **Base de datos:** `fuga`, `fuga_evidencia` vía API.
11. **Integraciones:** Ninguna.
12. **Comandos necesarios:** `npm test -- leaks`, `npx tsc --noEmit`.
13. **Pruebas:** estado vacío; datos insuficientes; un candidato; varios; evidencia con 3 gastos; fuga inexistente 404 → estado de error; ningún texto prohibido en `content/`.
14. **Criterios de aceptación:** toda cifra mostrada proviene de la API; cada candidato abre evidencia verificable; el lenguaje cumple D-15; no se muestra información de otras cuentas bajo ninguna ruta.
15. **Entregables:** módulo de fugas en la app.
16. **Riesgos:** saturar la lista; mostrar totales sin contexto; prometer ahorros.
17. **Condiciones de continuación:** revisión de textos contra D-15 + pruebas en verde.
18. **Estimación de esfuerzo:** 4–5 sesiones.

### F13 — Endurecimiento: seguridad, accesibilidad, rendimiento y regresión

1. **Identificador:** F13.
2. **Nombre:** Quality gate integral.
3. **Objetivo:** Cerrar brechas de seguridad, accesibilidad y rendimiento antes del build, y dejar una suite reproducible que demuestre el MVP.
4. **Requisitos e historias relacionadas:** RNF-001…RNF-016 (transversal); todas las HU Must.
5. **Dependencias:** F12.
6. **Actividades detalladas:**
   - Ejecutar la suite completa de seguridad de §10.8 sobre todas las rutas.
   - Revisar logs reales de una sesión de prueba (RNF-007).
   - Auditar dependencias: `npm audit --omit=dev`, `pip-audit`.
   - Verificar accesibilidad: contraste, tamaños táctiles, escalado de fuente al 200 %, etiquetas.
   - Medir con datos sembrados (p. ej. 500 gastos): tiempo de historial y de fugas; documentar resultados **sin inventar umbrales** (RNF-013).
   - Revisar `EXPLAIN ANALYZE` de las consultas de historial, agregados y fugas.
   - Escribir el informe `docs/planificacion/calidad.md` con evidencia.
   - Congelar contratos: generar OpenAPI y compararlo con `backend/docs/contratos.md`.
7. **Archivos y carpetas:** `backend/tests/security/*`, `mobile/src/**/__tests__`, `docs/planificacion/calidad.md`, `backend/docs/contratos.md`.
8. **Frontend:** Correcciones de accesibilidad y rendimiento.
9. **Backend:** Índices, límites y validaciones finales.
10. **Base de datos:** Índices adicionales si `EXPLAIN` lo justifica.
11. **Integraciones:** Verificación de que ninguna está declarada operativa sin prueba.
12. **Comandos necesarios:** `pytest -q`, `npm test -- --coverage`, `npm audit --omit=dev`, `pip-audit`, `ruff check .`, `npx tsc --noEmit`.
13. **Pruebas:** suite completa; regresión de todos los CA Must; prueba de carga ligera (script con 500 gastos); auditoría de logs; revisión de accesibilidad.
14. **Criterios de aceptación:** 100 % de pruebas Must en verde; cero vulnerabilidades críticas/altas sin mitigar; informe de calidad con cifras reales; sin datos sensibles en logs.
15. **Entregables:** informe de calidad, suite consolidada, contratos congelados.
16. **Riesgos:** descubrir un problema de diseño tarde; que el rendimiento con datos reales degrade las fugas.
17. **Condiciones de continuación:** informe aprobado y reproducible desde cero con un solo comando documentado.
18. **Estimación de esfuerzo:** 5–6 sesiones.

### F14 — Build Android, entrega y cierre

1. **Identificador:** F14.
2. **Nombre:** Compilación, instalación y documentación de entrega.
3. **Objetivo:** Producir un APK instalable, validar el flujo completo en dispositivo y cerrar la documentación del proyecto.
4. **Requisitos e historias relacionadas:** Todas las Must; RNF-011 (compilación Android).
5. **Dependencias:** F13; toolchain Android (H3) y dispositivo/emulador (H4).
6. **Actividades detalladas:**
   - Verificar JDK 17/21 y `ANDROID_HOME`; documentar `local.properties`.
   - `npx expo prebuild --platform android --clean`; revisar `AndroidManifest.xml` (permisos mínimos, `package`).
   - Compilar `assembleDebug` y luego `assembleRelease` con keystore de depuración documentada (sin publicar en tienda).
   - Instalar con `adb install -r` y ejecutar el guion de aceptación de §22.7.
   - Capturar evidencia (pantallas, logs) en `docs/planificacion/evidencias/`.
   - Escribir `docs/planificacion/entrega.md`: arquitectura, comandos, limitaciones, backlog.
   - Actualizar `PROGRESO_BUILD.md` con el estado final y las tareas pendientes reales.
7. **Archivos y carpetas:** `mobile/android/` (generado), `docs/planificacion/{entrega.md,evidencias/}`, `mobile/app.config.ts` (versión y `versionCode`).
8. **Frontend:** Ajustes finales de splash, icono y nombre visible.
9. **Backend:** Despliegue en hosting (H5) o ejecución local documentada.
10. **Base de datos:** Proyecto de producción/demostración con migraciones aplicadas.
11. **Integraciones:** Verificación final de cada una; las no configuradas se declaran **no disponibles**, sin simulaciones.
12. **Comandos necesarios:** `npx expo prebuild --platform android --clean`, `cd mobile/android; .\gradlew.bat assembleDebug`, `adb devices`, `adb install -r app-debug.apk`, `adb logcat`.
13. **Pruebas:** guion de aceptación de §26 en dispositivo; reinstalación limpia; modo avión (mensajes de error); rotación de pantalla; fuente grande.
14. **Criterios de aceptación:** APK instalada y flujo completo ejecutado sin bloqueos; evidencia registrada; limitaciones documentadas con honestidad.
15. **Entregables:** APK, informe de entrega, evidencias, backlog actualizado.
16. **Riesgos:** JDK 23 rompe Gradle; SDK incompleto; red del dispositivo no alcanza el backend; claves sin rotar.
17. **Condiciones de continuación:** ninguna (fase final). Si el build queda bloqueado, se declara el bloqueo y se entrega el estado real.
18. **Estimación de esfuerzo:** 4–6 sesiones (más el tiempo de instalación manual del toolchain, que no controla el agente).

### 20.1 Diagrama de dependencias entre fases

```
F0 ─▶ F1 ─▶ F2 ─▶ F3 ─▶ F4 ─▶ F5 ─▶ F6 ─▶ F7 ─▶ F8
                                              │
                          F9 ─────────────────┴─▶ F10 ─▶ F11 ─▶ F12 ─▶ F13 ─▶ F14
                          ▲
                     (F9 depende de F3 y F0)
```

Ruta crítica: **F0 → F1 → F2 → F3 → F5 → F6 → F9 → F10 → F13 → F14**.
Trabajo paralelizable (si se usan subagentes en BUILD): F9 puede avanzar mientras se completa F7–F8, porque depende de F3.

### 20.2 Regla de ejecución autónoma

**Dependencias de integración (aclaración vinculante):** F0 puede completarse sin Supabase. F1 requiere un proyecto Supabase real para aplicar migraciones y verificar las siete tablas. F2–F4 requieren la integración pertinente de PostgreSQL/Auth para sus criterios de aceptación; F6–F8 y F13 requieren datos reales de prueba y pruebas de API/aislamiento. F5 (motor determinista) y partes de F9–F12 pueden desarrollarse y probarse aisladamente, pero **no se declaran completas** si sus criterios dependen de rutas autenticadas o persistencia real todavía no disponibles. Los `skip` por falta de servicio son bloqueos registrados, no resultados aprobatorios. F14 requiere además el toolchain Android y pruebas en dispositivo. Esta aclaración no cambia el orden F0–F14 ni autoriza saltar fases dependientes.

Entre fases **no se piden aprobaciones ordinarias**. El agente continúa si:
1. La fase anterior cumple sus condiciones de continuación.
2. No hay un bloqueo humano nuevo (credencial, hardware, costo).
3. No se requiere una operación destructiva, un gasto o una decisión de alcance.

Si se cumple un bloqueo: registrar en `PROGRESO_BUILD.md`, marcar la fase como `BLOQUEADA` o `PARCIAL` según evidencia, continuar **solo con actividades independientes** y **no** declarar completada una fase ni aprobada una puerta de calidad si faltan pruebas obligatorias de integración. En particular, ausencia de Supabase/Auth no se sustituye con mocks para cerrar F1–F4, F6–F8 o F13.

---

## 21. Matriz de trazabilidad

### 21.1 Trazabilidad RF ↔ HU ↔ módulo ↔ fase ↔ prueba

| RF | HU | Módulo | Fase | Prueba principal | Prioridad | MVP |
|---|---|---|---|---|---|---|
| RF-001 | HU-01 | M1 | F9 | `mobile/__tests__/bienvenida.test.tsx` | Must | Sí |
| RF-002 | HU-02 | M1 | F3 · F9 | `tests/security/test_auth_flows.py` + `auth.test.tsx` | Must | Sí |
| RF-003 | HU-03 | M1 | Anexo E | Manual OAuth | Should | No |
| RF-004 | HU-04 | M1 | F3 · F9 | `logout.test.tsx` + `test_me.py` | Must | Sí |
| RF-005 | HU-05 | M1 | Anexo E | Manual reset | Should | No |
| RF-006 | HU-06 | M1 | Anexo E | — | Could | No |
| RF-007 | HU-07 | M2 | Anexo E | `test_me_patch.py` | Should | No |
| RF-008 | HU-08 | M2 | Anexo E | `test_photo_signature.py` | Should | No |
| RF-009 | HU-09 | M2 | Anexo E | — | Could | No |
| RF-010 | HU-10 | M3 | F5 · F10 | `test_interpret.py` + `nuevo.test.tsx` | Must | Sí |
| RF-011 | HU-11 | M3 | F5 | `test_interpret.py` (corpus §22.4) | Must | Sí |
| RF-012 | HU-12 | M3 | F5 · F10 | `revisar.test.tsx` | Must | Sí |
| RF-013 | HU-13 | M3 | F6 · F10 | `test_idempotency.py` | Must | Sí |
| RF-014 | HU-14 | M3 | F6 · F11 | `test_expenses.py` + `historial.test.tsx` | Must | Sí |
| RF-015 | HU-15 | M3 | Anexo E | `test_expenses_filters.py` | Should | No |
| RF-016 | HU-16 | M3 | Anexo E | `test_expenses_update.py` | Should | No |
| RF-017 | HU-17 | M4 | Anexo E | Manual Android | Could | No |
| RF-018 | HU-18 | M4 | Anexo E | Manual Android | Could | No |
| RF-019 | HU-19 | M4 | Anexo E | Manual Android | Could | No |
| RF-020 | HU-20 | M5 | F7 · F11 | `test_analytics.py` | Must | Sí |
| RF-021 | HU-21 | M5 | F7 · F11 | `test_analytics.py` | Must | Sí |
| RF-022 | HU-22 | M5 | Anexo E | `test_comparison.py` | Could | No |
| RF-023 | HU-23 | M6 | F8 · F12 | `test_rule_fuga_01.py` | Must | Sí |
| RF-024 | HU-24 | M6 | F8 · F12 | `test_leaks.py` | Must | Sí |
| RF-025 | HU-25 | M7 | Anexo E | Manual permisos | Could | No |
| RF-026 | HU-26 | M7 | Anexo E | — | Could | No |
| RF-027 | HU-27 | M7 | Anexo E | `test_monthly_leaks.py` | Could | No |
| RF-028 | HU-28 | M7 | No se implementa | — | Won't | No |
| RF-029 | HU-29 | M7 | No se implementa | — | Won't | No |
| RF-030 | HU-30 | M8 | Anexo E | `test_admin_stats.py` | Should | No |
| RF-031 | HU-31 | M8 | Anexo E | `test_admin_users.py` | Should | No |
| RF-032 | HU-32 | M8 | Anexo E | `test_admin_status.py` | Should | No |
| RF-033 | HU-33 | M8 | F4 · F13 | `tests/security/*` | Must | Sí |

### 21.2 Trazabilidad RNF ↔ fase ↔ evidencia

| RNF | Fase que lo satisface | Evidencia exigida |
|---|---|---|
| RNF-001 | F4, F13 | Suite `tests/security` al 100 % |
| RNF-002 | F6, F8, F12 | Revisión de DTOs + pruebas de aislamiento |
| RNF-003 | F3, F9 | SecureStore + validación JWKS + logout |
| RNF-004 | F2, F5, F6 | Pruebas de límites y campos desconocidos |
| RNF-005 | F6 | Prueba de concurrencia de idempotencia |
| RNF-006 | F7, F8 | Contraste antes/después (Should: edición) |
| RNF-007 | F2, F13 | Test de captura de logs |
| RNF-008 | F0, F14 | `.gitignore`, revisión de secretos, HTTPS |
| RNF-009 | F9–F12 | Estados vacío/carga/error en cada pantalla |
| RNF-010 | F5, F10 | Texto D-15 verificado en la UI |
| RNF-011 | F9, F14 | Build Android + fallback iOS |
| RNF-012 | F6, F10 | Pruebas de red caída y reintento |
| RNF-013 | F13 | Informe con cifras reales (sin umbral inventado) |
| RNF-014 | Todas | Versiones y suites por fase |
| RNF-015 | Anexo E | Auditoría (Should) |
| RNF-016 | F1, F13 | `deleted_at` no expuesto; política D-06 |

### 21.3 Cobertura de criterios de aceptación

- Cada HU Must tiene al menos **una prueba automatizada** que mapea a sus `CA-XX.Y` mediante el nombre del test (`test_ca_13_2_...`).
- Los CA que requieren interacción humana (usabilidad, lenguaje) se validan en F13/F14 con guion y evidencia.
- No se declara cobertura de un CA sin prueba o evidencia registrada.

---

## 22. Estrategia de pruebas

### 22.1 Pirámide y herramientas

| Nivel | Alcance | Herramienta | Dónde corre | Obligatorio |
|---|---|---|---|---|
| Unitario dominio | Parser, fechas, montos, normalizador, FUGA-01, agregados | `pytest` | Local, sin BD | Sí |
| Unitario componentes | Componentes y hooks | `jest-expo` + RNTL | Local | Sí |
| Integración BD | Repositorios, constraints, RLS, idempotencia | `pytest` + Supabase test | Requiere `TEST_DATABASE_URL` | Sí para cerrar fases dependientes; `skip` justificado implica fase bloqueada/parcial, no aprobada |
| API | Contratos, códigos, validaciones | `pytest` + `httpx.ASGITransport` | Local | Sí |
| Seguridad | Autorización y aislamiento | `pytest` parametrizado | Local | Sí |
| Contrato | OpenAPI vs DTOs | Script de comparación | Local | Sí |
| E2E móvil | Flujos completos | Manual guiado (F14); Maestro opcional | Dispositivo | Manual obligatorio |
| Compilación | Build Android | Gradle | Local | Sí (F14) |

### 22.2 Reglas de calidad

1. Ninguna fase se cierra con pruebas en rojo.
2. Un `skip` debe llevar `reason` y registrarse en `PROGRESO_BUILD.md`; si afecta un criterio de aceptación obligatorio, la fase **no se considera completada**. Las pruebas con mocks no sustituyen las pruebas de integración real.
3. Prohibido `assert` sin mensaje en pruebas de reglas de negocio.
4. Prohibido mockear el dominio en sus propias pruebas.
5. La suite de seguridad se ejecuta en **cada** cierre de fase desde F4.
6. Cobertura mínima orientativa: dominio ≥ 90 %, servicios ≥ 80 %, componentes críticos ≥ 70 %. No es un umbral de aceptación del producto, sino una guía interna.
7. Los datos de prueba son ficticios y se generan con un script reproducible (`supabase/seed.test.sql`).

### 22.3 Convención de nombres

- `test_ca_<HU>_<n>_<descripcion>` para criterios de aceptación.
- `test_<regla>` para reglas de negocio (`test_rn_din_02_rechaza_cero`).
- `test_<endpoint>_<caso>` para API.
- En móvil: `<Componente>.test.tsx` y `flujo_<nombre>.test.tsx`.

### 22.4 Corpus obligatorio del intérprete (F5)

| # | Entrada | Monto | Fecha | Categoría | Descripción esperada |
|---|---|---|---|---|---|
| 1 | `Hoy gasté $8.000 en un taxi` | 8000 | hoy | Transporte | taxi |
| 2 | `Ayer pagué 12500 de almuerzo` | 12500 | ayer | Alimentación | almuerzo |
| 3 | `Mercado 45000` | 45000 | hoy | Alimentación | mercado |
| 4 | `Uber al trabajo 9.500` | 9500 | hoy | Transporte | uber al trabajo |
| 5 | `Pagué el recibo de luz 32000` | 32000 | hoy | Servicios | recibo de luz |
| 6 | `Netflix 16900` | 16900 | hoy | Entretenimiento | netflix |
| 7 | `Compré una camisa en 60000` | 60000 | hoy | Compras | camisa |
| 8 | `Medicina 23000` | 23000 | hoy | Salud | medicina |
| 9 | `Curso de inglés 120000` | 120000 | hoy | Educación | curso de ingles |
| 10 | `Arriendo 800000` | 800000 | hoy | Vivienda | arriendo |
| 11 | `Gasté 5000 en algo` | 5000 | hoy | Otros | algo |
| 12 | `Taxi 8000` | 8000 | hoy | Transporte | taxi |
| 13 | `8000 taxi` | 8000 | hoy | Transporte | taxi |
| 14 | `COP 8.000 taxi` | 8000 | hoy | Transporte | taxi |
| 15 | `8.000 pesos de taxi` | 8000 | hoy | Transporte | taxi |
| 16 | `Ayer 3.500 bus` | 3500 | ayer | Transporte | bus |
| 17 | `Almuerzo 8,50` | **inválido** | — | — | Se rechaza decimal |
| 18 | `0 en nada` | **inválido** | — | — | Monto 0 rechazado |
| 19 | `Taxi -5000` | **inválido** | — | — | Negativo rechazado |
| 20 | `Gasté 100000001` | **inválido** | — | — | Fuera de rango |
| 21 | `` (vacío) | **inválido** | — | — | Texto vacío |
| 22 | 281 caracteres | **inválido** | — | — | Longitud |
| 23 | `Café 4000` | 4000 | hoy | Alimentación | cafe |
| 24 | `Cine 25000` | 25000 | hoy | Entretenimiento | cine |
| 25 | `Transporte 3000` | 3000 | hoy | Transporte | transporte |
| 26 | `Domicilio 18000` | 18000 | hoy | Alimentación | domicilio |
| 27 | `Farmacia 12000` | 12000 | hoy | Salud | farmacia |
| 28 | `Universidad 250000` | 250000 | hoy | Educación | universidad |
| 29 | `Internet 89900` | 89900 | hoy | Servicios | internet |
| 30 | `Zapatos 150000` | 150000 | hoy | Compras | zapatos |
| 31 | `Hoy gasté $8.000 en un taxi y $5.000 en café` | **ambigüedad** (no autosuma) | hoy | — | Marca ambigüedad y exige revisión obligatoria |
| 32 | `Fecha 15/03 taxi 7000` | 7000 | 15/03 del año actual si no es futura | Transporte | taxi |
| 33 | `2025-12-01 arriendo 800000` | 800000 | 2025-12-01 | Vivienda | arriendo |
| 34 | `Mañana taxi 8000` | 8000 | **hoy** + aviso | Transporte | taxi |
| 35 | `Ayer` | **inválido** | — | — | Sin monto |
| 36 | `Pagué 4500 de transmilenio` | 4500 | hoy | Transporte | transmilenio |
| 37 | `Snacks 2500` | 2500 | hoy | Alimentación | snacks |
| 38 | `Regalo 45000` | 45000 | hoy | Compras | regalo |
| 39 | `Spotify 14900` | 14900 | hoy | Entretenimiento | spotify |
| 40 | `Agua 2500` | 2500 | hoy | Alimentación | agua |
| 41 | `Gasto 5000` | 5000 | hoy | Otros | (genérico, marcado) |
| 42 | `Compra 9000` | 9000 | hoy | Otros | (genérico, marcado) |

Criterio de aceptación: los casos 1–16, 23–30, 32–34, 36–40 deben acertar monto, fecha y categoría; los inválidos (17–22, 35) deben rechazarse con mensaje claro; los ambiguos (31) deben marcar revisión obligatoria; los genéricos (41–42) deben caer en «Otros» con aviso.

### 22.5 Matriz de idempotencia (F6)

| Caso | Entrada | Resultado esperado |
|---|---|---|
| I-01 | Primera clave K, contenido A | 201, un registro |
| I-02 | Repetición K, contenido A | 200, mismo `id`, sin duplicado |
| I-03 | K, contenido B (monto distinto) | 409 `IDEMPOTENCY_CONFLICT` |
| I-04 | K usada hace 25 h, contenido A | 409 `IDEMPOTENCY_EXPIRED` |
| I-05 | Dos POST simultáneos K + A | Uno 201, otro 200; un solo registro |
| I-06 | K con formato inválido | 422 |
| I-07 | Sin `Idempotency-Key` | 422 |
| I-08 | K de otro usuario | Se trata como clave nueva de este usuario |
| I-09 | Dos gastos legítimos idénticos (mismos monto, fecha, categoría y descripción) con claves K1 ≠ K2 | 201 y 201; **dos** registros distintos (la idempotencia es por clave, no por contenido — RN-IDM-07) |

### 22.6 Matriz de la regla FUGA-01 (F8)

| Caso | Datos | Resultado |
|---|---|---|
| F-01 | 3 gastos, misma categoría y descripción, 3 fechas, 5.000 c/u (suma 15.000) | **Candidato** (borde exacto) |
| F-02 | Igual que F-01 pero suma 14.999 | Sin candidato |
| F-03 | 3 gastos, solo 2 fechas distintas | Sin candidato |
| F-04 | 2 gastos | Sin candidato |
| F-05 | 3 gastos, uno de 999 | Ese gasto se descarta → no hay candidato |
| F-06 | 3 gastos, uno de 30.001 | Se descarta → no hay candidato |
| F-07 | 4 gastos, 3 elegibles, 3 fechas | Candidato con 3 ocurrencias |
| F-08 | Misma categoría, descripciones distintas | No se agrupan → sin candidato |
| F-09 | Distinta categoría, misma descripción | No se agrupan |
| F-10 | Descripción con tildes/mayúsculas/espacios | Se normaliza y agrupa |
| F-11 | Descripción «gasto» | Descartada por genérica |
| F-12 | Categoría «Otros» con descripción informativa | Candidato válido |
| F-13 | Gasto con `deleted_at` | Excluido |
| F-14 | Gasto en el día 30 de la ventana | Incluido |
| F-15 | Gasto en el día 31 (fuera) | Excluido |
| F-16 | Cambio de día en `America/Bogota` (23:59 vs 00:01) | Atribución correcta al día local |
| F-17 | Mismo conjunto ejecutado dos veces | Mismo resultado, sin duplicar snapshot |
| F-18 | Usuario A con candidato; B sin datos | B ve «sin datos»; A ve su candidato |

### 22.7 Guion de aceptación en dispositivo (F14)

1. Instalación limpia del APK.
2. Bienvenida → registro con correo nuevo → confirmación (si aplica) → login.
3. Registrar «Hoy gasté $8.000 en un taxi» → revisar → corregir categoría → guardar.
4. Repetir con 3 gastos similares en 3 fechas distintas (usar el selector de fecha) para activar una fuga.
5. Ver historial: orden correcto, montos formateados, paginación.
6. Ver dashboard: total, cantidad, promedio y categoría mayor coherentes.
7. Ver fugas: candidato con evidencia de 3 gastos.
8. Cerrar sesión → verificar que no se puede volver atrás a una pantalla privada.
9. Iniciar sesión con otro usuario → confirmar que no ve nada del primero.
10. Modo avión → intentar procesar → mensaje comprensible y texto conservado.
11. Fuente del sistema al 200 % → ninguna pantalla rota.
12. Capturar evidencia de cada paso.

### 22.8 Definición de "terminado" por funcionalidad

Una funcionalidad está terminada solo si: (a) tiene endpoint/UI implementados; (b) sus CA tienen prueba o evidencia; (c) pasa la suite de seguridad; (d) no introduce datos sensibles en logs; (e) está registrada en `PROGRESO_BUILD.md` con comandos y resultados; (f) su contrato está documentado.

---

## 23. Costos

### 23.1 Principio

Proyecto académico individual: se **prioriza** operar en planes gratuitos y no se activa ningún plan de pago, método de pago ni servicio con costo sin aprobación explícita de la propietaria. Conforme a C-07, **no se asume que exista un plan gratuito permanente**: el diseño debe permitir cambiar de proveedor o de plan sin reescribir código, y cualquier costo futuro se decide fuera de BUILD.

### 23.2 Estimación por servicio

| Servicio | Plan previsto | Límite gratuito (verificar al activar) | Costo estimado | Estado de verificación |
|---|---|---|---|---|
| Supabase | Free | 2 proyectos, 500 MB BD, 50.000 MAU, pausa por inactividad | $0 | **A verificar en el panel al crear el proyecto** |
| Hosting backend | Proveedor no elegido (C-07): free tier si existe, o local | Instancia pequeña con suspensión por inactividad; el plan puede cambiar | $0 en MVP; costo futuro sujeto a aprobación | **No verificado**: depende del proveedor y de su plan vigente |
| Cloudinary | Free | Créditos mensuales de transformación/almacenamiento | $0 | **A verificar** al crear la cuenta (Should) |
| Google OAuth | Gratuito | Sin costo por autenticación | $0 | Verificado conceptualmente; requiere consent screen (Should) |
| Expo / EAS | Free | Builds locales ilimitados; EAS con cuota mensual limitada | $0 usando build local | **EAS no se usa por defecto** |
| Notificaciones | Locales | Sin servidor | $0 | N/A (Could) |
| Android SDK / JDK | Gratuito | — | $0 | Descarga manual |
| Repositorio Git | GitHub free | — | $0 | Activo |
| Herramientas dev | VS Code/OpenCode | — | $0 | Activo |

### 23.3 Riesgos de costo

| Riesgo | Condición | Mitigación |
|---|---|---|
| Pausa de Supabase Free | 7 días sin actividad | Reanudar antes de la demo; no depender de disponibilidad continua |
| Límite de MAU/almacenamiento | Uso intensivo | Datos de prueba acotados; limpiar seeds |
| Hosting con suspensión | Inactividad | Despertar el servicio antes de la demo; plan B local |
| Cloudinary por encima del free | Muchas subidas | No implementado en MVP |
| EAS Build | Gasto de cuota | Build local por defecto |

### 23.4 Lo que el agente no puede decidir

Contratar, activar facturación, introducir tarjetas, aceptar términos de pago o habilitar servicios de pago. Cualquier necesidad así se documenta como **bloqueo de decisión** y se eleva a la propietaria.

---

## 24. Riesgos

### 24.1 Riesgos técnicos

| ID | Riesgo | Prob. | Impacto | Mitigación | Fase |
|---|---|---|---|---|---|
| R-01 | JDK 23 incompatible con Gradle/AGP | Alta | Alto | Instalar JDK 21; fijar `JAVA_HOME`; verificar antes de F14 | F0/F14 |
| R-02 | Android SDK ausente | Alta | Alto | Instalación manual documentada (§19.7); F14 parcialmente bloqueada | F14 |
| R-03 | Módulo nativo de voz no enlaza con prebuild | Media | Medio | Diferir a ola Could; usar módulo local Expo documentado | Anexo E |
| R-04 | Límite de tamaño de `expo-secure-store` | Media | Medio | Fragmentación de la sesión | F9 |
| R-05 | Pooler de Supabase incompatible con prepared statements | Media | Medio | Usar pooler de sesión o `statement_cache_size=0` | F2 |
| R-06 | Ambigüedad del parser de montos colombianos | Alta | Medio | Gramática estricta + corpus de 42 casos | F5 |
| R-07 | Falsos positivos en fugas | Media | Alto | Agrupar por descripción + excluir genéricos + matriz F-01…F-18 | F8 |
| R-08 | Condiciones de carrera en idempotencia | Media | Alto | UQ + transacción + prueba concurrente | F6 |
| R-09 | Zona horaria mal aplicada en bordes de mes/día | Media | Alto | `zoneinfo` centralizado + pruebas de borde | F5/F7/F8 |
| R-10 | Regresión por actualización de Expo/RN | Media | Alto | Versiones congeladas + `expo install --check` | Todas |
| R-11 | Rendimiento degradado en fugas con muchos gastos | Media | Medio | Índices + `EXPLAIN` + límite de ventana | F13 |
| R-12 | Fuga de secretos al repositorio | Baja | Crítico | `.gitignore` + revisión + rotación | F0/F13 |
| R-13 | Dependencias con vulnerabilidades | Media | Medio | `npm audit`, `pip-audit` | F13 |
| R-14 | El agente "simula" una integración no configurada | Media | Alto | Regla explícita de honestidad + evidencia obligatoria | Todas |
| R-15 | Deriva de alcance (implementar Should/Could) | Media | Medio | Anexo E + puerta de §26 | Todas |
| R-23 | Asumir que RLS aísla las consultas del rol privilegiado | Media | Crítico | Filtro `usuario_id` obligatorio + prueba con la consulta real del backend (§6.9, §10.8) | F4/F13 |
| R-24 | Implementar idempotencia por contenido y bloquear gastos legítimos idénticos | Baja | Alto | Idempotencia por clave UUID (RN-IDM-07) + prueba I-09 | F6 |

### 24.2 Riesgos de producto y documentales

| ID | Riesgo | Impacto | Mitigación |
|---|---|---|---|
| R-16 | Contradicción nueva no prevista durante BUILD | Retrabajo | Las C-01…C-12 están cerradas; toda contradicción nueva se registra y se escala antes de codificar (§3.4) |
| R-17 | RNF-013 sin umbrales aprobados | No se puede "aprobar" rendimiento | Medir y reportar; no inventar cifras |
| R-18 | `texto_original` vs D-06 | Riesgo de privacidad | Persistir NULL (anexo D, C-01) |
| R-19 | Icono 500×500 insuficiente para tienda | Calidad visual | Derivado técnico + solicitar máster 1024 |
| R-20 | Correo saliente no configurado | Registro bloqueado | Modo sin confirmación documentado o SMTP propio |
| R-21 | Expectativa de "IA real" por la etiqueta | Confusión del usuario | Aviso D-15 visible antes de procesar |
| R-22 | Datos reales en pruebas | Privacidad | Solo datos ficticios |

### 24.3 Matriz de severidad y respuesta

| Severidad | Ejemplo | Respuesta |
|---|---|---|
| Crítico | Acceso a gastos ajenos, secreto filtrado | Detener la fase, corregir, añadir prueba de regresión, registrar |
| Alto | Duplicados de gasto, fuga falsa sistemática | Corregir antes de cerrar la fase |
| Medio | Estado de error ausente, formato incorrecto | Corregir en la misma fase o registrar deuda con fase asignada |
| Bajo | Texto mejorable, espaciado | Registrar en backlog de pulido (F13) |

---

## 25. Plan de continuidad

### 25.1 Problema

La implementación se ejecutará en sesiones autónomas prolongadas que pueden interrumpirse por límites de tokens, permisos, red o reinicio del entorno. Sin un estado persistente, el agente repetiría trabajo o declararía avances falsos.

### 25.2 Archivos de seguimiento

| Archivo | Propósito | Se actualiza |
|---|---|---|
| `mi-framework-ia/docs/planificacion/PROGRESO_BUILD.md` | Estado por fase y siguiente tarea | Al inicio y cierre de cada fase |
| `mi-framework-ia/docs/planificacion/BITACORA.md` | Registro cronológico de comandos y resultados | Tras cada hito relevante |
| `mi-framework-ia/docs/planificacion/BLOQUEOS.md` | Bloqueos humanos y externos | Al detectar y al resolver |
| `mi-framework-ia/docs/planificacion/evidencias/` | Capturas, salidas de test, reportes | Al cerrar fases |

### 25.3 Plantilla de `PROGRESO_BUILD.md`

```markdown
# PROGRESO DE BUILD — FUGA+

**Última actualización:** YYYY-MM-DD HH:MM (America/Bogota)
**Fase actual:** F<n> — <nombre>
**Siguiente tarea concreta:** <acción atómica>

## Estado por fase

| Fase | Estado | Evidencia | Notas |
|---|---|---|---|
| F0 | COMPLETADA / EN CURSO / BLOQUEADA / PENDIENTE | comando + resultado | |
| ... | | | |

## Funcionalidades implementadas

| RF | HU | Estado | Prueba | Evidencia |
|---|---|---|---|---|

## Archivos modificados (última sesión)

- `ruta` — qué cambió

## Pruebas ejecutadas

| Comando | Resultado | Fecha |
|---|---|---|

## Errores conocidos

| ID | Descripción | Severidad | Estado |
|---|---|---|---|

## Configuraciones manuales pendientes

| ID | Qué falta | Responsable | Impacto |
|---|---|---|---|

## Siguiente tarea

1. <paso atómico>
2. <paso atómico>
```

### 25.4 Protocolo de checkpoint (cada 20–30 minutos de trabajo o al cambiar de fase)

1. Ejecutar `git status --short` y registrar.
2. Ejecutar la suite de la fase y guardar el resumen.
3. Actualizar `PROGRESO_BUILD.md`: fase, siguiente tarea, pruebas, errores.
4. Añadir una línea a `BITACORA.md` con hora, acción y resultado.
5. Si hay bloqueo: moverlo a `BLOQUEOS.md` y elegir una tarea independiente.
6. **No** hacer commit salvo que la fase esté cerrada y validada (y solo en `develop`).

### 25.5 Recuperación tras interrupción

Al reanudar una sesión:

1. Leer `PROGRESO_BUILD.md` (sección "Siguiente tarea") y `BLOQUEOS.md`.
2. Verificar el estado real del repositorio (`git status`, `git log --oneline -5`, `git branch --show-current`).
3. Ejecutar la suite indicada; si falla algo que estaba "en verde", tratarlo como regresión de la fase actual.
4. Reanudar desde la primera tarea no evidenciada.
5. Si el archivo de progreso contradice el repositorio, **manda el repositorio** y se corrige el archivo.

### 25.6 Regla de honestidad

- "Implementado" exige código en disco y prueba ejecutada.
- "Configurado" exige evidencia de conexión real (no solo variable definida).
- "Funciona en dispositivo" exige captura y fecha.
- "Pendiente" es un estado válido y preferible a una afirmación falsa.
- El agente nunca borra un bloqueo del archivo sin evidencia de resolución.

### 25.7 Control de deriva

- Antes de empezar una tarea, verificar que pertenece a una fase y a un RF Must.
- Si la tarea no está en el plan, se registra como propuesta y **no se implementa**.
- Las ideas de mejora van a `docs/planificacion/IDEAS.md`, nunca directo al código.

---

## 26. Criterios de aceptación final

### 26.1 Puertas de aceptación (gates)

| Gate | Criterio | Evidencia |
|---|---|---|
| G0 · Repositorio | `develop` existe, `.gitignore` correcto, logo intacto, plan versionado | `git branch`, hash SHA-256 |
| G1 · Datos | Exactamente las 7 tablas MVP (C-09), `deleted_at` presente y sin uso (C-10), `fuga.regla_version_id` FK (C-12), constraints, índices, catálogo y FUGA-01 v1.0 aplicados | `db lint`, consultas de verificación |
| G2 · Seguridad | Todas las rutas privadas exigen token y propietario; suite de aislamiento en verde | `pytest tests/security` |
| G3 · Auth | Registro, login, sesión persistente y logout funcionan | Prueba de API + manual en app |
| G4 · Gastos | Texto → borrador → revisión → guardado idempotente → historial | Suite de F5/F6/F10 |
| G5 · Estadísticas | Total, cantidad, promedio y desglose coinciden con SQL de control | Contraste documentado |
| G6 · Fugas | FUGA-01 v1.0 con evidencia trazable y lenguaje D-15 | Matriz F-01…F-18 en verde |
| G7 · UX | Estados vacío/carga/error/éxito, accesibilidad AA, textos en español | Revisión + capturas |
| G8 · Calidad | `pytest`, `npm test`, `tsc`, `ruff`, auditorías sin críticos | Informe `calidad.md` |
| G9 · Build | APK instalable y guion de §22.7 ejecutado | `adb` + evidencias |
| G10 · Documentación | Plan, progreso, entrega y bloqueos actualizados y veraces | Archivos revisados |

### 26.2 Criterios de producto (MVP)

1. Un Visitante entiende qué es FUGA+ y puede registrarse o iniciar sesión.
2. Un Usuario registra un gasto en lenguaje natural y **nunca** se guarda sin su confirmación.
3. El gasto queda asociado al propietario del token y es invisible para cualquier otro usuario.
4. El historial muestra los gastos del más reciente al más antiguo, paginado.
5. El dashboard muestra total, cantidad, promedio y desglose por categoría del periodo, con «Otros» incluida.
6. Las posibles fugas se explican con regla, versión, ocurrencia, fechas, total e identificadores de evidencia.
7. Las cifras son enteras en COP y coherentes con los gastos vigentes.
8. El cierre de sesión deja el dispositivo sin acceso a datos.
9. No existe ninguna ruta, pantalla ni log que exponga datos de otra cuenta.
10. La app se instala en Android y completa el guion de aceptación.

### 26.3 Criterios de NO aceptación

- Declarar una integración operativa sin haberla probado.
- Mostrar datos de ejemplo como si fueran reales.
- Implementar funcionalidades Should/Could dentro del MVP sin decisión documentada.
- Introducir una tecnología fuera del stack aprobado.
- Modificar el logo, la paleta o el framework.
- Dejar pruebas en rojo "para después".
- Omitir el aviso de transparencia de D-15.

---

## 27. Procedimiento de transición de PLAN a BUILD

### 27.1 Estado al cierre del modo PLAN

- Este documento (**versión 1.1 consolidada**) se generó y actualizó en `C:\Users\Loren\.opencode\plan\PLAN_MAESTRO_IMPLEMENTACION_FUGA_PLUS.md` (única ruta escribible en modo PLAN).
- **No** se ha modificado código, configuración, ramas ni el repositorio.
- **No** se han ejecutado commits, merges ni pushes.
- El repositorio sigue en `main`, con el cambio local preexistente en `mi-framework-ia/opencode.json`.
- Las decisiones C-01…C-12 y DA-01 quedan cerradas; BUILD no las reinterpreta.

### 27.2 Secuencia exacta para BUILD (PowerShell, desde la raíz del repositorio)

```powershell
# 0. Verificar estado y no arrastrar cambios ajenos
git status --short
git branch --show-current

# 1. Copiar el plan a la ruta exigida por el prompt maestro
New-Item -ItemType Directory -Force -Path "mi-framework-ia\docs\planificacion" | Out-Null
Copy-Item "C:\Users\Loren\.opencode\plan\PLAN_MAESTRO_IMPLEMENTACION_FUGA_PLUS.md" `
          "mi-framework-ia\docs\planificacion\PLAN_MAESTRO_IMPLEMENTACION_FUGA_PLUS.md"

# 2. Verificar que el archivo llegó íntegro
Get-FileHash "C:\Users\Loren\.opencode\plan\PLAN_MAESTRO_IMPLEMENTACION_FUGA_PLUS.md" -Algorithm SHA256
Get-FileHash "mi-framework-ia\docs\planificacion\PLAN_MAESTRO_IMPLEMENTACION_FUGA_PLUS.md" -Algorithm SHA256

# 3. Confirmar que el framework no se alteró más allá del plan
git status --short

# 4. Crear develop desde main (sin tocar main todavía)
git switch -c develop

# 5. (Solo si la propietaria aprueba) versionar el plan en main
#    Nota: el plan debe conservarse en main según el prompt §21.
git switch main
git add "mi-framework-ia/docs/planificacion/PLAN_MAESTRO_IMPLEMENTACION_FUGA_PLUS.md"
git commit -m "docs(plan): add master implementation plan for FUGA+"
git switch develop
git merge main --ff-only

# 6. Comenzar F0
```

> **Importante:** los comandos 4–5 son los únicos que tocan git y **solo** se ejecutan en BUILD con aprobación. El cambio local en `mi-framework-ia/opencode.json` **no** se añade a ningún commit.

### 27.3 Sincronización `develop` ← `main` antes de implementar

```powershell
git switch develop
git fetch origin
git merge origin/main --ff-only
```

Si el merge no es fast-forward: detenerse, revisar y resolver manualmente; **no** forzar.

### 27.4 Reglas de git durante BUILD

- Solo dos ramas permanentes: `main` (documentación aprobada y estable) y `develop` (implementación).
- No crear ramas adicionales.
- Commits pequeños con Conventional Commits (`feat(expenses): ...`, `test(leaks): ...`, `docs(plan): ...`).
- No commitear secretos, `android/` generado, `node_modules/`, ni `opencode.json`.
- No hacer push sin autorización explícita.
- Prohibido `reset --hard`, `push --force`, `clean -fd` sobre trabajo no verificado.

### 27.5 Orden de arranque en BUILD

1. Copiar el plan y verificar hash.
2. Confirmar ramas.
3. Ejecutar F0 completo.
4. Antes de F1, comprobar el bloqueo H1 (proyecto Supabase). Si no existe, ejecutar F2/F5 en modo dominio puro y registrar el bloqueo — **sin** simular la BD.
5. Actualizar `PROGRESO_BUILD.md` al final de cada fase.

### 27.6 Qué NO debe hacer el agente al cambiar a BUILD

- No reinterpretar el alcance: el MVP son los 13 Must.
- No implementar el anexo E sin una nueva decisión documentada.
- No cambiar la paleta, el logo ni la tipografía.
- No sustituir Expo por React Native CLI sin ADR y aprobación.
- No introducir Docker, Redis, MongoDB ni IA generativa.
- No declarar terminado lo que no tenga evidencia.

---

## Anexo A — Contrato de API (MVP)

### A.1 Resumen de endpoints

| Método | Ruta | Auth | RF/HU | Descripción |
|---|---|---|---|---|
| GET | `/api/v1/health` | No | — | Liveness sin datos |
| GET | `/api/v1/ready` | No | — | Verifica BD |
| POST | `/api/v1/me/bootstrap` | Sí | RF-002/HU-02 | Crea el perfil si falta (idempotente) |
| GET | `/api/v1/me` | Sí | RF-002/HU-02 | Perfil, rol y estado |
| GET | `/api/v1/categories` | Sí | RF-010/HU-10 | Catálogo de 9 categorías |
| POST | `/api/v1/expenses/interpret` | Sí | RF-011/HU-11 | Texto → borrador (no persiste) |
| POST | `/api/v1/expenses` | Sí | RF-013/HU-13 | Crea gasto confirmado (idempotente) |
| GET | `/api/v1/expenses` | Sí | RF-014/HU-14 | Historial paginado |
| GET | `/api/v1/expenses/{id}` | Sí | RF-014/HU-14 | Detalle propio |
| GET | `/api/v1/analytics/summary` | Sí | RF-020/HU-20 | Total, cantidad, promedio |
| GET | `/api/v1/analytics/by-category` | Sí | RF-021/HU-21 | Desglose por categoría |
| GET | `/api/v1/leaks` | Sí | RF-023/HU-23 | Candidatos con cálculo bajo demanda |
| GET | `/api/v1/leaks/{id}` | Sí | RF-024/HU-24 | Evidencia de la fuga |

### A.2 `POST /api/v1/expenses/interpret`

**Request**
```json
{ "texto": "Hoy gasté $8.000 en un taxi" }
```
**200**
```json
{
  "draft": {
    "monto_cop": 8000,
    "fecha_gasto": "2026-11-13",
    "descripcion": "taxi",
    "categoria_id": "3f2a...",
    "categoria_nombre": "Transporte",
    "moneda": "COP"
  },
  "confianza": { "monto": "alta", "fecha": "alta", "descripcion": "media", "categoria": "media" },
  "avisos": ["Categoría propuesta por diccionario; verifícala antes de guardar."],
  "diccionario_version": "1.0",
  "reglas_version": "1.0",
  "ambiguedades": []
}
```
**Errores:** `422` texto vacío, > 280 o con múltiples montos no resolubles (se devuelve `ambiguedades` cuando aún puede revisarse).

### A.3 `POST /api/v1/expenses`

**Headers:** `Authorization: Bearer …`, `Idempotency-Key: <uuid v4>`, `Content-Type: application/json`
**Request**
```json
{
  "monto_cop": 8000,
  "fecha_gasto": "2026-11-13",
  "descripcion": "taxi",
  "categoria_id": "3f2a...",
  "moneda": "COP",
  "diccionario_version": "1.0",
  "reglas_version": "1.0"
}
```
(`texto_original` **no** se envía en el MVP; ver anexo D, C-01.)

**201**
```json
{
  "id": "8b1c...",
  "monto_cop": 8000,
  "fecha_gasto": "2026-11-13",
  "descripcion": "taxi",
  "categoria": { "id": "3f2a...", "nombre": "Transporte" },
  "moneda": "COP",
  "created_at": "2026-11-13T15:42:11-05:00"
}
```
**200** (idempotente, mismo contenido) → mismo cuerpo e `id`.
**409** `IDEMPOTENCY_CONFLICT` / `IDEMPOTENCY_EXPIRED`.
**422** validación; **401/403** sesión/cuenta.

### A.4 `GET /api/v1/expenses`

**Query:** `limit` (1–50, defecto 20), `cursor` (opaco), `desde`, `hasta` (opcionales, ISO).
**200**
```json
{
  "items": [
    { "id": "8b1c...", "monto_cop": 8000, "fecha_gasto": "2026-11-13",
      "descripcion": "taxi", "categoria": { "id": "3f2a...", "nombre": "Transporte" } }
  ],
  "next_cursor": "eyJjcmVhdGVkX2F0IjoiMjAyNi0xMS0xM1QyMDoxMjozM1oiLCJpZCI6Ijh...",
  "has_more": true
}
```
Orden garantizado: `fecha_gasto DESC, created_at DESC, id DESC`.

### A.5 `GET /api/v1/analytics/summary`

**Query:** `periodo=2026-11` **o** `desde=2026-11-01&hasta=2026-11-30`.
**200**
```json
{
  "periodo": { "desde": "2026-11-01", "hasta": "2026-11-30", "etiqueta": "noviembre de 2026" },
  "total_cop": 125000,
  "cantidad": 10,
  "promedio_cop": 12500,
  "moneda": "COP"
}
```
Periodo vacío: `total_cop: 0`, `cantidad: 0`, `promedio_cop: null`.

### A.6 `GET /api/v1/analytics/by-category`

```json
{
  "periodo": { "desde": "2026-11-01", "hasta": "2026-11-30" },
  "total_cop": 125000,
  "categorias": [
    { "id": "3f2a...", "nombre": "Transporte", "total_cop": 45000, "cantidad": 4, "porcentaje": 36.0 },
    { "id": "9c11...", "nombre": "Alimentación", "total_cop": 35000, "cantidad": 3, "porcentaje": 28.0 },
    { "id": "77bb...", "nombre": "Otros", "total_cop": 45000, "cantidad": 3, "porcentaje": 36.0 }
  ],
  "categoria_mayor": ["Transporte", "Otros"]
}
```
`categoria_mayor` es un arreglo para representar empates; se ordena alfabéticamente.

### A.7 `GET /api/v1/leaks`

**200 — con candidatos**
```json
{
  "estado": "con_candidatos",
  "regla": { "codigo": "FUGA-01", "version": "1.0", "regla_version_id": "rv01..." },
  "ventana": { "desde": "2026-10-15", "hasta": "2026-11-13" },
  "items": [
    {
      "id": "f01...",
      "categoria": { "id": "3f2a...", "nombre": "Transporte" },
      "descripcion_normalizada": "taxi",
      "ocurrencias": 4,
      "monto_acumulado_cop": 32000,
      "fecha_desde": "2026-10-20",
      "fecha_hasta": "2026-11-10",
      "evidencia_ids": ["g1...", "g2...", "g3...", "g4..."]
    }
  ]
}
```
**200 — sin gastos:** `{ "estado": "sin_gastos", "items": [] }`
**200 — datos insuficientes:** `{ "estado": "datos_insuficientes", "items": [] }`

### A.8 `GET /api/v1/leaks/{id}`

```json
{
  "id": "f01...",
  "regla": { "codigo": "FUGA-01", "version": "1.0", "regla_version_id": "rv01..." },
  "ventana": { "desde": "2026-10-15", "hasta": "2026-11-13" },
  "categoria": { "id": "3f2a...", "nombre": "Transporte" },
  "descripcion_normalizada": "taxi",
  "ocurrencias": 4,
  "monto_acumulado_cop": 32000,
  "evidencia": [
    { "gasto_id": "g1...", "fecha_gasto": "2026-10-20", "monto_cop": 8000, "descripcion": "taxi" }
  ]
}
```
Si la fuga no pertenece al usuario: `404 NOT_FOUND`.

### A.9 Códigos de error por endpoint

| Endpoint | 400 | 401 | 403 | 404 | 409 | 422 |
|---|---|---|---|---|---|---|
| `/expenses/interpret` | — | ✔ | ✔ | — | — | ✔ |
| `/expenses` (POST) | — | ✔ | ✔ | — | ✔ | ✔ |
| `/expenses` (GET) | — | ✔ | ✔ | — | — | ✔ |
| `/expenses/{id}` | — | ✔ | ✔ | ✔ | — | ✔ |
| `/analytics/*` | — | ✔ | ✔ | — | — | ✔ |
| `/leaks/*` | — | ✔ | ✔ | ✔ | — | — |

---

## Anexo B — Referencias de migración, RLS y seed

### B.1 Orden y contenido (resumen ejecutable)

```sql
-- 0001_extensions.sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS citext;

-- 0002_catalogo.sql
CREATE TABLE categoria (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  nombre VARCHAR(40) NOT NULL UNIQUE,
  orden SMALLINT NOT NULL UNIQUE,
  activa BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE regla_fuga (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  codigo VARCHAR(20) NOT NULL UNIQUE,
  nombre VARCHAR(80) NOT NULL,
  descripcion TEXT NOT NULL,
  activa BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE regla_fuga_version (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  regla_id UUID NOT NULL REFERENCES regla_fuga(id) ON DELETE RESTRICT,
  version VARCHAR(10) NOT NULL,
  parametros JSONB NOT NULL,
  vigente_desde TIMESTAMPTZ NOT NULL DEFAULT now(),
  vigente_hasta TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (regla_id, version)
);
CREATE UNIQUE INDEX regla_version_vigente_uq
  ON regla_fuga_version (regla_id) WHERE vigente_hasta IS NULL;
```

```sql
-- 0003_perfil.sql
CREATE TABLE perfil (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  nombres VARCHAR(80),
  apellido VARCHAR(80),
  telefono VARCHAR(10) CHECK (telefono ~ '^[0-9]{10}$'),
  foto_url TEXT,
  foto_google_url TEXT,
  rol VARCHAR(15) NOT NULL DEFAULT 'usuario'
      CHECK (rol IN ('usuario','administrador')),
  disabled_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER LANGUAGE plpgsql SECURITY DEFINER SET search_path = public AS $$
BEGIN
  INSERT INTO public.perfil (id) VALUES (NEW.id) ON CONFLICT (id) DO NOTHING;
  RETURN NEW;
END; $$;

CREATE TRIGGER on_auth_user_created
AFTER INSERT ON auth.users
FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

```sql
-- 0004_gasto.sql (extracto)
CREATE TABLE gasto (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  usuario_id UUID NOT NULL REFERENCES perfil(id) ON DELETE RESTRICT,
  categoria_id UUID NOT NULL REFERENCES categoria(id) ON DELETE RESTRICT,
  monto_cop BIGINT NOT NULL CHECK (monto_cop BETWEEN 1 AND 100000000),
  descripcion VARCHAR(120) NOT NULL
    CHECK (length(btrim(descripcion)) BETWEEN 1 AND 120),
  texto_original VARCHAR(280),
  fecha_gasto DATE NOT NULL
    CHECK (fecha_gasto >= DATE '2020-01-01'),
  moneda CHAR(3) NOT NULL DEFAULT 'COP' CHECK (moneda = 'COP'),
  diccionario_version VARCHAR(10) NOT NULL,
  reglas_version VARCHAR(10) NOT NULL,
  clave_idempotencia UUID NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  deleted_at TIMESTAMPTZ,
  CONSTRAINT gasto_idempotencia_uq UNIQUE (usuario_id, clave_idempotencia)
);
```

```sql
-- 0005_fugas.sql
CREATE TABLE fuga (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  usuario_id UUID NOT NULL REFERENCES perfil(id) ON DELETE RESTRICT,
  regla_version_id UUID NOT NULL REFERENCES regla_fuga_version(id) ON DELETE RESTRICT,
  categoria_id UUID NOT NULL REFERENCES categoria(id) ON DELETE RESTRICT,
  descripcion_normalizada VARCHAR(120) NOT NULL,
  ocurrencias SMALLINT NOT NULL CHECK (ocurrencias > 0),
  monto_acumulado_cop BIGINT NOT NULL CHECK (monto_acumulado_cop > 0),
  fecha_desde DATE NOT NULL,
  fecha_hasta DATE NOT NULL,
  vigente BOOLEAN NOT NULL DEFAULT TRUE,
  detectada_en TIMESTAMPTZ NOT NULL DEFAULT now(),
  actualizada_en TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (fecha_hasta >= fecha_desde)
);

CREATE INDEX fuga_usuario_vigente_idx ON fuga (usuario_id, vigente);
CREATE INDEX fuga_regla_version_idx ON fuga (regla_version_id);

-- Índice único parcial: permite recalcular el mismo día conservando el snapshot histórico.
CREATE UNIQUE INDEX fuga_snapshot_uq
  ON fuga (usuario_id, regla_version_id, categoria_id, descripcion_normalizada)
  WHERE vigente = TRUE;

CREATE TABLE fuga_evidencia (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  fuga_id UUID NOT NULL REFERENCES fuga(id) ON DELETE CASCADE,
  gasto_id UUID NOT NULL REFERENCES gasto(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT fuga_evidencia_uq UNIQUE (fuga_id, gasto_id)
);

CREATE INDEX fuga_evidencia_gasto_idx ON fuga_evidencia (gasto_id);
```

```sql
-- 0006_rls.sql (extracto)
ALTER TABLE perfil ENABLE ROW LEVEL SECURITY;
ALTER TABLE gasto ENABLE ROW LEVEL SECURITY;
ALTER TABLE fuga ENABLE ROW LEVEL SECURITY;
ALTER TABLE fuga_evidencia ENABLE ROW LEVEL SECURITY;

CREATE POLICY perfil_select_propio ON perfil
  FOR SELECT TO authenticated USING (id = auth.uid());

-- El cliente no escribe gastos: sin políticas de INSERT/UPDATE/DELETE.
```

```sql
-- 0007_grants.sql
REVOKE INSERT, UPDATE, DELETE ON gasto FROM anon, authenticated;
REVOKE INSERT, UPDATE, DELETE ON fuga FROM anon, authenticated;
REVOKE INSERT, UPDATE, DELETE ON fuga_evidencia FROM anon, authenticated;
REVOKE UPDATE (rol, disabled_at) ON perfil FROM anon, authenticated;
GRANT SELECT ON categoria, regla_fuga, regla_fuga_version TO authenticated;
```

### B.2 Seed del catálogo

```sql
INSERT INTO categoria (nombre, orden) VALUES
  ('Alimentación', 1), ('Transporte', 2), ('Vivienda', 3),
  ('Servicios', 4), ('Educación', 5), ('Salud', 6),
  ('Entretenimiento', 7), ('Compras', 8), ('Otros', 9)
ON CONFLICT (nombre) DO NOTHING;

INSERT INTO regla_fuga (codigo, nombre, descripcion)
VALUES ('FUGA-01', 'Patrón repetido de gasto',
        'Detecta gastos repetidos de bajo monto en 30 días')
ON CONFLICT (codigo) DO NOTHING;

INSERT INTO regla_fuga_version (regla_id, version, parametros, vigente_desde)
SELECT id, '1.0',
  '{"ventana_dias":30,"min_gastos":3,"min_fechas":3,
    "monto_min":1000,"monto_max":30000,"suma_min":15000,
    "zona":"America/Bogota"}'::jsonb, now()
FROM regla_fuga WHERE codigo = 'FUGA-01'
ON CONFLICT (regla_id, version) DO NOTHING;
```

### B.3 Prueba RLS de referencia

```sql
-- Ejecutar con JWT de usuario A
SELECT count(*) FROM gasto;                      -- 0 filas: el cliente no lee gasto directamente
SELECT count(*) FROM gasto WHERE usuario_id = '<uuid-B>';  -- 0
UPDATE perfil SET rol = 'administrador' WHERE id = auth.uid();  -- error de permiso
```

### B.4 Diferencias entre generación automática y configuración manual

| Elemento | Automático (agente) | Manual (propietaria) |
|---|---|---|
| Archivos de migración | ✔ | — |
| Aplicar migraciones | ✔ con `npx supabase db push` | Requiere proyecto y `link` |
| Crear proyecto Supabase | ✘ | ✔ |
| Copiar claves | ✘ | ✔ |
| Configurar Auth/Google/SMTP | Parcial (documentado) | ✔ |
| Seeds | ✔ | — |
| RLS | ✔ | Validación final ✔ |

---

## Anexo C — Diccionario determinista v1.0

### C.1 Estructura

```json
{
  "version": "1.0",
  "vigente_desde": "2026-11-13",
  "categorias": [
    { "nombre": "Alimentación", "claves": ["almuerzo","cena","desayuno","mercado","supermercado",
      "restaurante","cafe","cafeteria","domicilio","comida","panaderia","agua","snacks","fruta"] },
    { "nombre": "Transporte", "claves": ["taxi","uber","bus","transmilenio","metro","gasolina",
      "peaje","parqueadero","moto","bicicleta","transporte","pasaje"] },
    { "nombre": "Vivienda", "claves": ["arriendo","alquiler","administracion","hipoteca","muebles",
      "reparacion","vivienda"] },
    { "nombre": "Servicios", "claves": ["luz","agua","gas","internet","telefono","celular","recibo",
      "servicios","energia"] },
    { "nombre": "Educación", "claves": ["universidad","curso","matricula","libros","colegio",
      "educacion","ingles","taller"] },
    { "nombre": "Salud", "claves": ["medicina","farmacia","medico","cita","salud","odontologo",
      "examen","droga"] },
    { "nombre": "Entretenimiento", "claves": ["cine","netflix","spotify","streaming","juego",
      "concierto","salida","entretenimiento","suscripcion"] },
    { "nombre": "Compras", "claves": ["camisa","zapatos","ropa","regalo","compra","tienda",
      "celular nuevo","audifonos","compras"] },
    { "nombre": "Otros", "claves": [] }
  ],
  "genericas": ["gasto","gastos","compra","compras","otro","otros","varios","pago","pagos","cosa"],
  "muletillas": ["gaste","pague","compre","en","un","una","unos","unas","de","el","la","los","las","por"],
  "equivalencias": {
    "taxis": "taxi", "resto": "restaurante", "mercadito": "mercado",
    "transmi": "transmilenio", "celu": "celular", "profe": "universidad"
  }
}
```

### C.2 Reglas de resolución

1. Normalizar entrada (RN-INT-01).
2. Aplicar `equivalencias`.
3. Buscar claves por **frase completa** (mayor longitud primero).
4. Si hay una única categoría ganadora ⇒ asignarla.
5. Si empatan ⇒ «Otros» + aviso `revision_manual`.
6. Si no hay coincidencia ⇒ «Otros».
7. Si la descripción resultante es genérica ⇒ marcar `descripcion_generica: true` (relevante para FUGA-01).

### C.3 Gobierno del diccionario

- Cambiar claves exige **nueva versión** (`1.1`, `2.0`) y actualizar `diccionario_version` en las pruebas.
- Prohibido editar `1.0` una vez usado en datos persistidos.
- Cada versión tiene archivo propio: `diccionario_v1.0.json`, `diccionario_v1.1.json`.
- El backend selecciona la versión vigente por configuración y la devuelve en la respuesta.

---

## Anexo D — Decisiones aprobadas C-01…C-12 y decisión arquitectónica complementaria

### D.1 Estado de las decisiones

Las 12 decisiones **C-01…C-12** fueron **aprobadas por la propietaria** el **2026-11-13** y son **vinculantes** para BUILD. Sustituyen a la tabla de «decisiones por defecto» de la versión 1.0. Ninguna queda pendiente de validación ni se reabre durante la implementación.

| ID | Tema / conflicto original | Fuentes | Decisión aprobada (vinculante) | Estado | Impacto en el plan |
|---|---|---|---|---|---|
| **C-01** | `gasto.texto_original` NOT NULL en el ER frente a la minimización de datos | ER vs D-06 | El texto original completo **no se conserva** en la base de datos. `gasto.texto_original` es **nullable** y se persiste como `NULL`. Solo se guardan los datos estructurados tras la confirmación del usuario. El borrador vive en memoria y nunca se envía al servidor para almacenamiento. | **APROBADA** | §9.2.3, Anexo A.3, Anexo B.1 |
| **C-02** | `perfil.nombres` y `apellido` NOT NULL en el ER, pero el registro no los pide | ER vs HU-02 | Nombres y apellidos son **opcionales**: no se exigen para registrarse y pueden completarse posteriormente. El alta crea el perfil con ambos en `NULL`. | **APROBADA** | §9.2.1, §10.2, §15.2 |
| **C-03** | Comportamiento de la idempotencia pasadas 24 h | D-05 | Clave **UUID por intento** con ventana de **24 horas**. Evita duplicados accidentales **sin impedir** registrar dos gastos legítimos con valores idénticos (claves distintas). Clave expirada ⇒ `409 IDEMPOTENCY_EXPIRED`. Misma clave y mismo contenido ⇒ `200`; misma clave y contenido distinto ⇒ `409 IDEMPOTENCY_CONFLICT`. | **APROBADA** | §6.5, §16.8, §22.5, Anexo A.3 |
| **C-04** | RNF-013 no fija tamaño de página ni patrón de carga | RNF-013 | Historial con **20 registros por carga**, **máximo 50** por solicitud y **carga adicional al desplazarse**. Paginación **por cursor**. | **APROBADA** | §8.3, §11.2, F11, Anexo A.4 |
| **C-05** | Algunas HU conservan «pendiente (D-xx)» aunque las decisiones están cerradas | HU vs D-01…D-15 | Las HU **no se modifican**. «Pendiente (D-xx)» se interpreta como **resuelto por D-xx**; no reabre decisiones ni crea trabajo. La regla vive solo en este plan (§3.5). | **APROBADA** | §3.5, §5.4 |
| **C-06** | RNF-013 sin umbrales de latencia o volumen aprobados | RNF-013 | Los objetivos de rendimiento son **orientativos y ajustables** según pruebas reales. Se **mide y documenta** sin declarar cumplimiento de umbrales no aprobados. | **APROBADA** | §5.2, §22.2, F13 |
| **C-07** | Alojamiento del backend no definido | Documento de requerimientos | FastAPI se **desarrolla y prueba localmente** en la primera etapa, pero se **diseña para desplegarse en la nube**. Exige: configuración por variables de entorno, dependencias reproducibles, URL de API configurable en el móvil, credenciales seguras, preparación para HTTPS, instrucciones de despliegue y ausencia de dependencias de rutas o servicios locales. **No se elige proveedor definitivo ni se asume plan gratuito permanente.** | **APROBADA** | §6.6, §19.9, §23.1, F2, F14 |
| **C-08** | Logo de 500×500 px frente a requisitos de icono Android | `assets/` vs requisito técnico | El logo original **se conserva sin rediseñar**. Solo se generan los recursos técnicos necesarios para Android mediante **composición, escalado proporcional y márgenes**. Se documenta la limitación de resolución de 500 × 500 px. | **APROBADA** | §13.3, §13.4, F0, F9 |
| **C-09** | Tablas Should/Could/Won't presentes en el ER | ER | En el MVP se crean **únicamente siete tablas**: `perfil`, `categoria`, `gasto`, `regla_fuga`, `regla_fuga_version`, `fuga`, `fuga_evidencia`. Las demás se añaden por migraciones posteriores. | **APROBADA** | §9.2, §9.3, F1, Anexo B.1, G1 |
| **C-10** | `deleted_at` existe en el ER pero no hay borrado en el MVP | ER vs D-06 | `deleted_at` se conserva como campo **opcional**, inicialmente `NULL`, **sin utilizarlo ni exponer funciones de eliminación** de gastos durante el MVP. | **APROBADA** | §9.1, §9.2.3, §16.3, G1 |
| **C-11** | Retención y eliminación de datos personales | RNF-016 vs D-06 | **No se implementa eliminación de gastos desde la app** en el MVP. Se documenta la **política de retención** y el **procedimiento administrativo** para solicitudes legítimas de eliminación de datos personales. La ausencia de un botón de eliminación **no** sustituye las obligaciones de privacidad. | **APROBADA** | §2.3, §16.9, §24, G10 |
| **C-12** | `fuga.regla_version` referenciaba solo el texto de versión | ER | Se usa **`regla_version_id`** como clave foránea al identificador único de `regla_fuga_version(id)` **desde el MVP**. Se actualizan DDL, relaciones, consultas, contratos, pruebas, ejemplos y referencias dependientes. **No se implementan reglas adicionales** por esta decisión. | **APROBADA** | §9.2.6, §9.5, §9.6, §15.6, F1, F8, Anexo A.7/A.8, Anexo B.1 |

### D.2 Decisión arquitectónica complementaria (DA-01)

| Campo | Contenido |
|---|---|
| **ID** | **DA-01** |
| **Título** | FastAPI como puerta de acceso a los datos financieros |
| **Fecha** | 2026-11-13 |
| **Estado** | **APROBADA** |
| **Decisión** | La aplicación móvil utiliza la **API FastAPI**. FastAPI accede a PostgreSQL mediante conexión segura. La app móvil **no escribe directamente** en las tablas financieras. La autenticación usa **Supabase Auth** y FastAPI **valida** los tokens emitidos; **no se implementan JWT propios**. Las credenciales de base de datos permanecen **exclusivamente en el backend**. |
| **Alcance** | Todas las operaciones sobre `gasto`, `fuga` y `fuga_evidencia`; lectura de `perfil` para autorización; catálogo `categoria` y versiones de regla. |
| **Consecuencias** | El backend concentra validación, reglas deterministas e idempotencia; el cliente solo consume contratos `/api/v1`. RLS queda como defensa en profundidad para acceso directo del cliente, que en el MVP no existe para datos financieros. |
| **Verificación** | Coherencia entre permisos PostgreSQL, aislamiento por usuario, RLS y conexión del backend; prueba con la consulta real del backend para A y B (F4, F13). **No se asume que RLS proteja consultas de roles privilegiados.** |
| **Relación con C-07** | **No sustituye** a C-07: C-07 fija el modelo de alojamiento portable; DA-01 fija el modelo de acceso a datos. Ambos coexisten. |
| **Registro** | §6.9, ADR-08, §8.6, §9.4, §10.1, §10.6 |

### D.3 Regla de interpretación de las HU (C-05)

Se aplica lo dispuesto en **§3.5**: las 33 HU no se modifican; las referencias «pendiente (D-xx)» se leen como resueltas por D-01…D-15 y por C-01…C-12; la trazabilidad se conserva en la matriz de §21.

### D.4 Contradicciones adicionales detectadas en la auditoría de la versión 1.1

Todas se resolvieron **dentro del plan**; ninguna requiere modificar requisitos, HU, diagramas ni código.

| ID | Contradicción detectada | Ubicación | Resolución aplicada |
|---|---|---|---|
| A-01 | El Anexo B anunciaba migraciones 0001–0007 pero omitía el DDL de `fuga` y `fuga_evidencia` | Anexo B.1 | Se añadió el bloque `0005_fugas.sql` completo |
| A-02 | La FK `fuga.regla_version` apuntaba a una columna sin restricción única propia (DDL inválido en PostgreSQL) | §9.2.6 / C-12 | Sustituida por `regla_version_id` UUID FK → `regla_fuga_version(id)` |
| A-03 | El `UNIQUE` del snapshot incluía `fecha_hasta` y no era parcial: un recálculo el mismo día colisionaba con el snapshot invalidado | §9.2.6 | Índice único **parcial** `WHERE vigente = true` sin `fecha_hasta` |
| A-04 | `CHECK (ocurrencias >= 3)` y `CHECK (monto_acumulado_cop >= 15000)` duplicaban en DDL umbrales versionados en `regla_fuga_version.parametros` | §9.2.6 | `CHECK > 0`; los umbrales viven solo en la versión de la regla |
| A-05 | La prueba RLS de referencia esperaba que el cliente leyera «solo las filas de A», pero no existe política `SELECT` sobre `gasto` | Anexo B.3 | Corregido: el cliente obtiene **0 filas**; los datos financieros se leen por FastAPI |
| A-06 | El código `PROFILE_NOT_FOUND` no existía en el modelo unificado de errores | §8.5 | Reemplazado por `404 NOT_FOUND` con `details.reason = profile_not_found` |
| A-07 | La respuesta de interpretación incluía `ambiguedades` en el Anexo A pero no en el contrato de §15.3 | §15.3 | Campo unificado en ambos contratos |
| A-08 | La lista `GENERICAS` de §15.6 difería de `genericas` del diccionario del Anexo C | §15.6 / Anexo C | El diccionario es la **fuente única**; el código no mantiene listas paralelas |
| A-09 | F14 remitía al «guion de aceptación de §26», que no contiene el guion | F14 | Corregido a §22.7 |
| A-10 | §23.1 afirmaba que «todo debe operar en planes gratuitos», en tensión con C-07 | §23.1 / §23.2 | Matizado: se prioriza free tier, no se asume permanencia y todo costo se aprueba |
| A-11 | §6.1 decía «service role» mientras §19.8 limitaba esa clave a tareas admin | §6.1 / §8.6 / §19.8 | Precisado como **rol privilegiado de base de datos**; `service_role` queda para administración |
| A-12 | El caso 31 del corpus admitía dos resultados («13000 o ambigüedad») | §22.4 | Fijado: **ambigüedad**, sin autosuma; revisión obligatoria |
| A-13 | El anexo D de la v1.0 presentaba C-12 como cambio futuro, contradiciendo la decisión aprobada | Anexo D | Sustituido por la decisión vinculante C-12 |
| A-14 | §9.5 afirmaba que el trigger `set_updated_at()` aplicaba a «todas las tablas propias», pero `fuga` usa `detectada_en`/`actualizada_en` | §9.5 vs §9.2.6 / Anexo B.1 | Precisado: el trigger aplica a las tablas con `updated_at`; `fuga` conserva `actualizada_en` |

### D.5 Observaciones técnicas no bloqueantes

| ID | Observación | Tratamiento |
|---|---|---|
| O-01 | `CHECK` con `CURRENT_DATE` en la versión 1.1 | **RESUELTA en 1.1.1:** CHECK fijo para fecha mínima; FastAPI valida que la fecha no sea futura en `America/Bogota`; pruebas SQL y API separadas (§9.5, F1, F6, anexo B.1). |
| O-02 | El rate limiting «en memoria» no se comparte entre instancias | Aceptable para el MVP de instancia única; se documenta en F13 y no se presenta como protección distribuida |
| O-03 | La eliminación administrativa debe respetar el orden de FKs (`gasto` → `perfil` con `RESTRICT`) | Procedimiento de §16.9 fija el orden y la verificación posterior |

### D.6 Registro de revisión técnica 1.1.1 (2026-11-15)

| Ajuste | Secciones revisadas | Verificación prevista |
|---|---|---|
| T-01: fecha de gasto | §9.2.3, §9.5, F1, F6, anexo B.1 y O-01 | SQL rechaza fecha anterior al mínimo; API rechaza fecha futura con `422` usando `America/Bogota`. |
| T-02: aislamiento | §9.4, §10.8, F4 y §22 | RLS con rol sujeto a políticas, más API real con conexión privilegiada y dos usuarios; ningún mock sustituye estas pruebas. |
| T-03: Supabase | §4, §19.1, F1, §20.2 y §22 | Fases con integración obligatoria no se cierran con `skip` ni mocks; tareas independientes pueden adelantarse sin cambiar la secuencia. |

**Alcance de esta revisión:** edición documental únicamente. No se ejecutaron migraciones, tests, comandos Git ni BUILD. Las verificaciones de ejecución quedan pendientes de las fases correspondientes.

**Regla de uso del anexo D:** las decisiones C-01…C-12 y DA-01 se aplican **sin reabrir discusión**; se registran en `BITACORA.md` al iniciar BUILD. Ninguna introduce funcionalidades nuevas ni altera prioridades Must/Should/Could/Won't. Cualquier contradicción futura se registra y se escala (no se resuelve por invención).

---

## Anexo E — Backlog de ampliación (no se implementa en la ola MVP)

### E.1 Ola Should (después de G9)

| Orden | RF/HU | Trabajo | Dependencia | Riesgo |
|---|---|---|---|---|
| S1 | RF-007/HU-07 | Perfil editable (nombres, teléfono) | F9 | Bajo |
| S2 | RF-008/HU-08 | Foto con Cloudinary firmado | S1 + cuenta Cloudinary | Medio |
| S3 | RF-005/HU-05 | Recuperación de contraseña | Supabase SMTP | Bajo |
| S4 | RF-003/HU-03 | Google OAuth | Credenciales Google | Medio |
| S5 | RF-015/HU-15 | Filtros de historial | F11 | Bajo |
| S6 | RF-016/HU-16 | Editar/eliminar gasto (lógico) + invalidación de agregados | F11/F8 | Alto |
| S7 | RF-030/031/032 | Administración + auditoría | Rol admin + D-07/D-14 | Alto |

### E.2 Ola Could

| Orden | RF/HU | Trabajo | Nota |
|---|---|---|---|
| C1 | RF-017/018/019 | Voz con módulo Kotlin | Requiere build y dispositivo |
| C2 | RF-025 | Alertas locales | D-11; permiso del sistema |
| C3 | RF-026 | Sugerencias prácticas | Sin promesas de ahorro |
| C4 | RF-027 | Resumen mensual de fugas | D-04 |
| C5 | RF-022 | Comparación entre periodos | RNF-006 |
| C6 | RF-006 / RF-009 | Desactivar cuenta / foto de Google | D-06/D-13 |

### E.3 Won't (for now)

- RF-028 y RF-029: límite mensual global y su avance. **No se crean** `limite_mensual` ni `limite_mensual_cambio`.

### E.4 Criterio de entrada a una ola

1. La ola MVP cumple G0–G10.
2. Existe decisión documentada de la propietaria.
3. Se actualizan `REQUERIMIENTOS.md` y `HISTORIAS_DE_USUARIO.md` si cambia el alcance.
4. Se añade la fase correspondiente a este plan (no se implementa "por fuera" del plan).

---

## Cierre del documento

Este Plan Maestro (**versión 1.1 consolidada**) cubre los 27 apartados exigidos por `PROMPT_PLAN_MAESTRO_FUGA_PLUS.md`, define 15 fases ejecutables con sus 18 atributos e incorpora las 12 decisiones aprobadas C-01…C-12 y la decisión arquitectónica complementaria DA-01. Deja el proyecto listo para una ejecución autónoma en modo BUILD sin ambigüedades de alcance, sin tecnologías inventadas y sin afirmaciones de integraciones no verificadas.

**Restricciones respetadas durante la elaboración y la revisión 1.1:**

- No se programó la aplicación.
- No se modificó código funcional ni el framework `mi-framework-ia`.
- No se usó ni actualizó ningún `README.md`.
- No se alteró el logo ni la paleta.
- No se modificaron los requerimientos, las 33 historias de usuario ni los cinco diagramas `.drawio`.
- No se usaron pantallas antiguas como requisitos.
- No se inventaron historias ni funcionalidades, ni se alteraron las prioridades Must/Should/Could/Won't.
- No se introdujeron tecnologías innecesarias.
- No se instalaron ni modificaron MCP.
- No se ejecutaron operaciones destructivas, commits, ramas ni pushes.

**Resultado:** Plan Maestro de Implementación Integral de FUGA+ versión 1.1, basado en la documentación vigente, coherente con las decisiones aprobadas, compatible con las tecnologías aprobadas, fiel a la identidad visual y preparado para ejecución posterior en BUILD.








