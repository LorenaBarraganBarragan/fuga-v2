# Backlog de Requisitos — Release 1 · FUGA+

## Alcance del release 1 (a partir de la visión y el MVP)

Indispensable para la demo de 3 minutos: registrar un gasto por texto, que la IA lo
clasifique, guardarlo, consultar historial, ver un dashboard simple, detectar posibles
fugas por reglas propias, y hacer consultas básicas. Quedan fuera: voz (se evalúa como
extra si sobra tiempo), notificaciones avanzadas, y todo lo bancario/pagos.

## Backlog priorizado (MoSCoW)

### HU-01 — Must
**Como** usuario **quiero** registrar un gasto escribiendo una descripción en lenguaje
natural **para** no perder tiempo llenando formularios.

```gherkin
Escenario: Registrar un gasto válido
  Dado que el usuario está en la pantalla de registro
  Cuando escribe "Hoy gasté $8.000 en un taxi" y confirma
  Entonces el gasto queda guardado con el texto original
  Y el usuario ve una confirmación en pantalla

Escenario: Registrar un texto sin información de gasto
  Dado que el usuario está en la pantalla de registro
  Cuando escribe un texto sin valor numérico reconocible, como "hola"
  Entonces el sistema no crea un gasto
  Y muestra un mensaje pidiendo incluir un valor
```

### HU-02 — Must
**Como** usuario **quiero** que la IA interprete y clasifique automáticamente mi gasto
(valor, categoría, descripción) **para** no tener que categorizar manualmente cada
registro.

```gherkin
Escenario: Clasificación automática exitosa
  Dado que el usuario registró el texto "Hoy gasté $8.000 en un taxi"
  Cuando el sistema procesa el texto
  Entonces el gasto queda etiquetado con valor 8000, categoría "Transporte"
  y descripción "Taxi"

Escenario: Clasificación con baja confianza
  Dado que el texto registrado es ambiguo, como "gasté algo por ahí"
  Cuando el sistema no logra identificar un valor claro
  Entonces el gasto se guarda como "sin clasificar"
  Y el usuario puede completar la categoría manualmente

Escenario: Revisión en lote al final del día
  Dado que el usuario registró varios gastos a lo largo del día
  Cuando abre la vista de "revisión del día"
  Entonces ve todos los gastos del día con su categoría asignada
  Y puede corregir solo los que estén mal antes de confirmarlos todos juntos
```
*Ajuste tras entrevista real (ver `docs/ia/entrevista-real.md`): el usuario
prefiere revisar varios gastos juntos al final del día en vez de confirmar
categoría por categoría en el momento de cada registro.*

### HU-03 — Must
**Como** usuario **quiero** consultar el historial de mis gastos registrados **para**
revisar en qué se ha ido mi dinero durante el mes.

```gherkin
Escenario: Ver historial con gastos registrados
  Dado que el usuario tiene al menos un gasto registrado
  Cuando abre la sección "Historial"
  Entonces ve la lista de gastos ordenada por fecha, con valor, categoría
  y descripción de cada uno

Escenario: Historial vacío
  Dado que el usuario no ha registrado ningún gasto
  Cuando abre la sección "Historial"
  Entonces ve un mensaje indicando que aún no hay gastos registrados
```

### HU-04 — Must
**Como** usuario **quiero** ver un dashboard sencillo con el resumen de mis gastos
**para** entender de un vistazo cómo he gastado mi dinero.
*Criterio de aceptación:* dado que existen gastos registrados en el periodo actual,
cuando el usuario abre el dashboard, entonces ve los totales agrupados por categoría.

### HU-05 — Must
**Como** usuario **quiero** que el sistema identifique posibles fugas de dinero en
gastos pequeños y repetitivos **para** notar patrones que no había visto.
*Criterio de aceptación:* dado que el usuario tiene 3 o más gastos similares en la
misma categoría dentro de un periodo corto, cuando el sistema aplica las reglas de
detección, entonces esos gastos quedan marcados como "posible fuga" en el dashboard.

### HU-06 — Must
**Como** usuario **quiero** realizar consultas básicas sobre mis gastos por categoría o
rango de fechas **para** encontrar información específica sin revisar todo el
historial.
*Criterio de aceptación:* dado que el usuario tiene gastos en varias categorías, cuando
filtra por "Transporte", entonces solo ve los gastos de esa categoría.

### HU-07 — Should
**Como** usuario **quiero** ver resaltada una alerta simple cuando el sistema detecte
una posible fuga **para** enterarme sin tener que revisar el dashboard a fondo.
*Criterio de aceptación:* dado que existe al menos una fuga detectada, cuando el
usuario abre la app, entonces ve un aviso visible sobre esa fuga. [SUPUESTO: aviso
dentro de la app, no notificación push]

### HU-08 — Should
**Como** usuario **quiero** corregir manualmente la categoría que la IA asignó a un
gasto **para** mantener mi historial preciso cuando la IA se equivoque.
*Criterio de aceptación:* dado que un gasto fue mal clasificado, cuando el usuario
edita su categoría, entonces el historial y el dashboard reflejan el cambio.

### HU-09 — Could
**Como** usuario **quiero** registrar un gasto usando mi voz en lugar de texto **para**
hacerlo más rápido cuando estoy ocupado.
*Criterio de aceptación:* dado que el usuario activa el registro por voz, cuando dicta
un gasto, entonces el sistema lo transcribe y lo procesa igual que un registro por
texto.

### HU-10 — Could
**Como** usuario **quiero** ver una comparación simple de mis gastos mes a mes **para**
entender si estoy mejorando con el tiempo.
*Criterio de aceptación:* dado que el usuario tiene gastos en más de un mes, cuando
abre "Estadísticas", entonces ve una comparación básica entre los meses disponibles.

### HU-11 — Won't (explícitamente fuera de este release)
**Como** usuario **quisiera** conectar mi cuenta bancaria para que mis gastos se
registren automáticamente, **pero** esta funcionalidad no se desarrollará en el release
1 porque implica integraciones bancarias externas fuera del alcance de las 12 semanas
y del riesgo que un solo desarrollador puede asumir.

---

## Refinamiento crítico (checklist INVEST aplicado)

| Problema detectado | Corrección aplicada | Justificación (INVEST) |
|---|---|---|
| El requisito original "Interpretación mediante IA" (RF-02) venía mezclado con el registro (RF-01) como si fuera un solo paso, sin poder construirse ni probarse por separado. | Se separó en HU-01 (registrar texto) y HU-02 (clasificar con IA) como historias independientes, cada una con su propio escenario de éxito y de falla. | **Independent** — ahora cada historia puede desarrollarse y probarse sin esperar a la otra. |
| El requisito de "Dashboard" (RF-05) no tenía ningún estado observable ni forma de fallar; solo decía "mostrar dashboard". | Se agregó un criterio con estado verificable: totales agrupados por categoría, con un caso donde no hay datos. | **Testable** — antes no se podía imaginar cómo fallaría el escenario; ahora sí. |
| El requisito de "fugas de dinero" (RF-06) corría el riesgo de sonar como si la IA juzgara qué gasto es "malo", lo cual está fuera de las restricciones del negocio. | Se reescribió el criterio usando una regla explícita y objetiva (3+ gastos similares en un periodo) y el término "posible fuga", nunca "gasto innecesario". | **Valuable / Negotiable** — entrega valor real (detectar patrones) sin prometer un juicio que el sistema no puede sostener, y deja abierto el CÓMO se define el umbral. |
| La historia de registro por voz (Could) era muy amplia ("usar mi voz") sin límite claro de tamaño. | Se acotó a: transcribir y reutilizar el mismo pipeline de clasificación de texto ya construido en HU-02, en lugar de crear lógica nueva. | **Small** — cabe en pocos días porque no duplica trabajo ya hecho. |
| HU-02 asumía que el sistema pediría confirmación de categoría gasto por gasto antes de guardar. La entrevista real mostró que el usuario prefiere registrar varios gastos juntos al final del día, y confirmar categoría uno por uno le resultaría molesto e interrumpiría su flujo real de uso. | Se ajustó el criterio de aceptación de HU-02 para que la confirmación sea una **revisión en lote**: el usuario ve todos los gastos del día clasificados de una vez y corrige solo los que estén mal, en lugar de una pregunta por cada gasto. | **Valuable** — el diseño ahora coincide con el hábito real de uso (registrar al final del día) confirmado en `docs/ia/entrevista-real.md`, en vez de un supuesto no validado. |

---

*Documento generado a partir de la conversación en `docs/ia/entrevista-cliente.md` y del
prompt de priorización MoSCoW (ver `docs/ia/prompts.md`), con refinamiento humano
aplicado sobre el borrador inicial.*
