# Conceptos canónicos de gastos — interpretación 1.1

Esta ampliación aplica la petición de normalización general del 2026-11-18. Conserva
FastAPI, PostgreSQL, Supabase Auth y el procesamiento determinista, sin servicios externos.

## Compatibilidad y decisiones

- No añade tablas, columnas ni campos obligatorios en los contratos HTTP.
- Diccionario y reglas **de interpretación** pasan a 1.1; FUGA-01 permanece en **1.0**.
- Se aceptan confirmaciones 1.0/1.0 y 1.1/1.1. Los valores por defecto 1.0 permanecen
  para no romper clientes anteriores ni las huellas de sus reintentos idempotentes.
- El catálogo base `diccionario_v1.json` permanece intacto. La extensión
  `normalizacion_v1_1.json` contiene prefijos, equivalencias justificadas y las pocas
  palabras clave compuestas adicionales, sin duplicar el catálogo.
- La agrupación sigue siendo **categoría + concepto canónico**. No se reclasifican
  automáticamente los gastos guardados ni se mezclan categorías.
- No se reescriben las descripciones confirmadas, las fechas ni los importes de gastos
  existentes. El intérprete propone una descripción editable; el texto de entrada del
  borrador permanece intacto. La confirmación conserva la descripción elegida por el usuario.

## Normalización conservadora

Se normalizan mayúsculas, tildes, puntuación y espacios. Se reconocen prefijos temporales,
verbos de transacción y conectores iniciales. Los precios explícitos y los importes conocidos
se separan del concepto; se conservan números de modelo, ruta, plan, cantidades y otros
atributos cuando no hay evidencia suficiente de que sean un precio.

Los conectores internos no se borran globalmente: `con`, `sin`, negaciones, destinos y
calificadores se conservan. Las equivalencias se aplican a frases completas ya normalizadas
y cada una tiene una justificación. Por ejemplo:

| Variantes | Concepto |
|---|---|
| Gasté 5000 en café / Compré un café de 5000 | cafe |
| Pagué 3000 de buseta / Tomé una buseta de 3000 | buseta |
| Recarga de celular / recarga para celular | recarga celular |
| Comida para perro / alimento para perro | comida perro |
| Entrada de cine / boleta de cine | entrada cine |

`cafe`, `cafe con leche` y `cafe sin azucar` permanecen separados, igual que `buseta`
y `bus intermunicipal`. Las frases no reconocidas conservan sus palabras significativas:
no se selecciona solo la primera palabra, no hay búsqueda difusa ni inferencia de sinónimos.
Los casos ambiguos requieren revisión manual o una equivalencia explícita en una nueva versión.

## Historial y FUGA-01

El mismo normalizador se ejecuta al analizar todos los gastos, incluidos los que fueron
registrados con interpretación 1.0. No es necesario volver a registrarlos ni migrarlos.
La huella del snapshot incorpora la versión de normalización: la siguiente consulta normal
de análisis recalcula con la lógica nueva sin reutilizar snapshots de la lógica anterior.
Este cambio local no ejecuta análisis ni escrituras contra Supabase.

Los umbrales siguen siendo 30 días, 3 gastos en 3 fechas distintas, COP 1.000–30.000 por gasto
y suma mínima de COP 15.000. La regresión usa las descripciones comunicadas por el usuario:
`gaste cafe`, `cafe`, `cafe`, `por cafe`, en las fechas 14, 15, 17 y 18 de noviembre de 2026,
a COP 5.000 cada una, con la misma categoría. El resultado esperado es un candidato `cafe`
de cuatro ocurrencias y COP 20.000, sin mutar los datos de entrada.

## Verificación desde Expo Web

1. Reiniciar FastAPI para cargar los nuevos módulos; abrir Expo Web con el usuario propietario.
2. Comprobar en Historial que los cuatro gastos conservan sus descripciones, fechas y categoría.
3. Abrir Fugas y pulsar **Actualizar análisis**. Esta acción habitual escribe snapshots de fugas;
   no modifica los gastos y no se ha ejecutado automáticamente durante este cambio.
4. Con esos gastos dentro de la ventana de 30 días, esperar un grupo `cafe`, cuatro ocurrencias
   y COP 20.000. Abrir la evidencia para comprobar que muestra las descripciones guardadas originales.
5. En Registrar, probar las variantes de otras categorías y descartar el borrador si no se desea
   guardar un gasto. Verificar también que los conceptos compuestos permanecen diferenciados.

El caso fechado se prueba localmente con fecha de referencia 2026-11-18. En uso real siempre se
aplica la fecha actual en Bogotá: fuera de la ventana de 30 días no debe aparecer ese candidato.
