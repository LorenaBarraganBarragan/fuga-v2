# Entrevista real — Usuario potencial de FUGA+

**Perfil del entrevistado:** joven/estudiante, perfil objetivo de FUGA+.

## Bloque 1 — Hábitos actuales de gasto

**¿Llevas algún tipo de control de tus gastos hoy en día?**
Mentalmente, sin ninguna herramienta.

**¿Cuándo fue la última vez que no supiste en qué se te fue la plata?**
Todos los principios y finales de mes.

**¿En qué gastas más seguido sin darte cuenta?**
Comida y transporte.

## Bloque 2 — Experiencia previa con apps

**¿Habías intentado usar alguna app o método antes para controlar gastos?**
Sí, usó Monefy hace un tiempo.

**¿Por qué dejaste de usarla?**
Se le olvidaba registrar los datos y se aburrió de tener que escribir.

**¿Qué le cambiarías para que sí te funcionara?**
Un recordatorio, y que tuviera funciones nuevas.

## Bloque 3 — Registro por texto natural

**¿Anotarías cada gasto con una frase corta como "gasté 8 mil en un taxi"?**
Sí.

**¿En qué momento del día se te olvidaría más registrar un gasto?**
Justo al momento de pagar.

**¿Preferirías escribirlo apenas gastas, o de una sola vez al final del día?**
Al final del día.

**¿Recordarías todos los gastos pequeños del día, o se te pasarían algunos?**
Cree que sí los recordaría todos.

## Bloque 4 — Clasificación automática

**Si la app clasifica mal un gasto, ¿lo corregirías o te daría pereza?**
Lo corregiría él mismo, pero si está ocupado lo dejaría sin arreglar.

**¿Qué tan grave sería que la clasificación fallara seguido?**
Si falla en repetidas ocasiones, dejaría de usar la app.

**¿Prefieres que la app adivine sola, o que siempre te pregunte antes de guardar?**
Prefiere que **siempre le pregunte antes de guardar**, para verificar que la categoría quedó bien y ahí sí almacenar.

## Bloque 5 — Detección de "fugas de dinero"

**Si la app te dijera "esto parece una fuga de dinero", ¿te parecería útil o te sentirías juzgado?**
Le parecería útil.

**¿Qué harías con esa información?**
Disminuiría esas compras.

## Bloque 6 — Dashboard y consultas

**¿Qué es lo primero que quieres ver al revisar tus gastos?**
El total gastado en el mes.

**¿Con qué frecuencia abrirías la app a revisar tu resumen?**
Semanalmente.

**Si buscaras "cuánto gasté en transporte este mes", ¿qué tan fácil esperarías que fuera?**
Que sea fácil: poder seleccionar la categoría y la fecha fácilmente.

## Bloque 7 — Fricción y abandono

**¿Qué te haría dejar de usar una app de gastos a la semana de instalarla?**
Que sea poco atractiva y que por eso no la use tan seguido.

**Si un día se te olvida registrar varios gastos, ¿te frustraría tanto como para no volver a intentarlo?**
Seguiría igual registrando, pero le gustarían recordatorios para evitar que se le olvide.

**¿Qué tan dispuesto estarías a corregir errores manualmente?**
Sí corregiría errores manualmente, pero solo al principio.

## Bloque 8 — Funcionalidades adicionales

**¿Usarías el registro por voz en vez de escribir?**
Sí, le gustaría mucho más el registro por voz.

**¿En qué situación la usarías más?**
La usaría en muchas situaciones, ya que no tendría que escribir, solo hablar.

**¿Te interesaría ver comparación mes a mes, o con el mes actual basta?**
Con ver el mes actual basta, aunque en algunas situaciones sí sería bueno ver la comparación.

---

## Hallazgos clave para el backlog

- **Preferencia fuerte por confirmación antes de guardar** — no quiere que la app adivine y guarde sola; quiere revisar la categoría antes de que quede almacenada. Esto afecta el diseño de HU-02.
- **Registro al final del día, no al momento del gasto** — la app debe soportar registrar varios gastos de una sola vez, no solo uno a la vez justo al pagar.
- **Los recordatorios son un dolor real** (motivo de abandono de Monefy) — candidato fuerte a subir de prioridad en el release (hoy está fuera del MVP, considerar para el siguiente).
- **Preferencia muy marcada por voz sobre texto** — más fuerte de lo esperado; vale la pena revisar si "Could" sigue siendo la prioridad correcta o si debería subir a "Should".
- **Corrección manual solo "al principio"** — sugiere que espera que la IA mejore con el tiempo (aprendizaje), lo cual hoy no está en el alcance (se resuelve con reglas fijas, no aprendizaje real); dejarlo como expectativa a gestionar, no a prometer.
