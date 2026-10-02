# FUGA+

App móvil de gestión de gastos personales con Inteligencia Artificial, dirigida
inicialmente a jóvenes y estudiantes.

**Repositorio:** https://github.com/Lorenaba/FUGA-plus

## Problema

Muchas personas realizan pequeños gastos durante el día y luego no recuerdan
con claridad en qué se fue su dinero. Registrar cada gasto manualmente resulta
tedioso, lo que dificulta llevar un seguimiento constante de los hábitos de
consumo.

## Usuarios

Jóvenes y estudiantes que quieren organizar sus gastos cotidianos y entender
mejor sus hábitos de consumo, sin usar herramientas financieras complejas.

## Propuesta de valor

FUGA+ permite registrar un gasto escribiendo una frase en lenguaje natural
(ej. *"Hoy gasté $8.000 en un taxi"*). La IA interpreta y clasifica el gasto
(valor, categoría, descripción), lo guarda en un historial, y el sistema
aplica reglas propias para detectar **posibles fugas de dinero** en gastos
pequeños y repetitivos — sin necesidad de conectar cuentas bancarias ni
manejar pagos.

## Alcance del MVP (Release 1)

- Registro de gastos mediante texto en lenguaje natural
- Clasificación automática por IA (valor, categoría, descripción)
- Historial de gastos consultable
- Dashboard sencillo con totales por categoría
- Detección de posibles fugas de dinero mediante reglas propias
- Consultas básicas por categoría y rango de fechas

**Fuera de este release:** pagos, conexión bancaria, tarjetas, créditos,
inversiones, asesoría financiera, notificaciones avanzadas, registro por voz
(evaluado como funcionalidad adicional si el tiempo lo permite).

## Uso de IA en el proyecto

| Fase | ¿Para qué se usa la IA? | Herramienta | Riesgo a vigilar |
|---|---|---|---|
| Análisis de requisitos | Organizar ideas, definir necesidades y delimitar qué entra y qué queda fuera del MVP. | ChatGPT / Claude | Que la IA sugiera demasiadas funcionalidades y el alcance supere las 12 semanas. |
| Diseño | Apoyar bocetos y prototipos de pantallas, priorizando una interfaz sencilla. | Figma AI | Diseñar alrededor de funcionalidades que no alcancen a implementarse. |
| Desarrollo | Interpretar y clasificar los gastos registrados por el usuario (ej. "taxi" → Transporte). La detección de fugas usa reglas propias, no IA. | API de OpenAI o Claude + reglas propias | Clasificación incorrecta, o reglas de detección demasiado laxas/estrictas. |
| Pruebas | Generar ejemplos de gastos con errores, abreviaciones y lenguaje cotidiano para probar la interpretación. | Claude / GitHub Copilot | Probar solo frases perfectas y que la app falle con lenguaje real. |
| Documentación | Apoyar la redacción del README y demás documentación del proyecto. | ChatGPT / Claude | Documentar funcionalidades como terminadas cuando aún están en desarrollo. |
| Despliegue | Participación mínima; el despliegue es principalmente manual. | — | Publicar una versión con errores no probados. |
| Mantenimiento | Participación limitada, dentro del alcance de las 12 semanas del curso. | No aplica | Prometer mejoras futuras fuera del alcance definido. |

### Resultados de los análisis generados con IA

**Análisis competitivo** — Se identificaron 3 competidores reales: **Cleo** y
**PocketGuard** (dependen de vincular cuentas bancarias, sin registro por
texto libre) y **Spendee** (registro manual por formulario, sin
interpretación de lenguaje natural). Ninguno combina registro por lenguaje
natural + detección explícita de "fugas" por gastos pequeños sin conexión
bancaria — esa combinación es la ventaja diferencial validada de FUGA+.

**Documento de visión** — Define el problema (gastos pequeños que pasan
desapercibidos), el usuario objetivo (jóvenes y estudiantes) y el alcance
del MVP, marcando explícitamente la voz como funcionalidad opcional
[ASSUMPTION]. Sirve como documento base para todo el proyecto.

**Requisitos priorizados (MoSCoW)** — De 8 requisitos funcionales y 3 no
funcionales: **6 Must** (registro, interpretación IA, almacenamiento,
historial, dashboard, detección de fugas) + 3 RNF Must (viabilidad en 12
semanas, demo de 3 min, alcance de la IA limitado a clasificación),
**1 Should** (consultas), **1 Could** (voz), y el resto explícitamente
**Won't** (todo lo bancario/financiero). Este resultado fue la base sobre la
que se construyó el backlog de historias de usuario del release 1.

Los prompts completos usados en cada fase, sus salidas completas y las
entrevistas con usuarios están documentados en [`docs/ia/`](docs/ia/).

## Tecnología

- **App móvil:** React Native 
- **IA:** API de OpenAI o Claude para interpretación y clasificación de
  gastos en lenguaje natural
- **Detección de fugas:** reglas propias en el código, no aprendizaje
  automático

## Estructura del repositorio

```
FUGA-plus/
├── docs/
│   ├── vision.md                    # Problema, usuarios, propuesta de valor, MVP
│   ├── requisitos.md                # Backlog priorizado (MoSCoW) con criterios Gherkin
│   ├── requisitos.xlsx              # Mismo backlog en formato hoja de cálculo
│   └── ia/
│       ├── entrevista-real.md       # Entrevista a un usuario potencial
│       ├── entrevista-cliente.md    # Validación con IA en rol de cliente/usuario
│       └── prompts/                 # Biblioteca de prompts usados en el proyecto
├── mobile/                          # Código de la app (por crear)
└── README.md

```

## Equipo

**Lorena Barragán** — Desarrolladora y responsable del proyecto (proyecto
individual: análisis, diseño, desarrollo, IA, datos, pruebas y documentación).

## Estado del proyecto

Proyecto académico en desarrollo — Electiva CPC, Corporación Universitaria
Minuto de Dios. Duración estimada: 12 semanas.

## Documentación relacionada

- [Documento de visión](docs/vision.md)
- [Backlog de requisitos – Release 1](docs/requisitos.md)
- [Entrevistas y prompts con IA](docs/ia/)