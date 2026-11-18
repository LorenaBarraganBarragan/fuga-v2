# PROMPT 01 Ã¢â‚¬â€ AUDITORÃƒÂA TÃƒâ€°CNICA Y PLAN DE MEJORA DE FUGA+

**Proyecto:** FUGA+
**VersiÃƒÂ³n del prompt:** 1.0
**Tipo:** AuditorÃƒÂ­a tÃƒÂ©cnica, evaluaciÃƒÂ³n arquitectÃƒÂ³nica y planificaciÃƒÂ³n de mejoras
**Etapa:** DiagnÃƒÂ³stico y planificaciÃƒÂ³n, sin implementaciÃƒÂ³n

---

## 1. Rol

ActÃƒÂºa como un equipo de especialistas compuesto por:

- Arquitecto de software.
- Ingeniero de software.
- Especialista en escalabilidad y rendimiento.
- Auditor de calidad de cÃƒÂ³digo.
- Especialista en ciberseguridad.
- Ingeniero DevOps e infraestructura.
- Ingeniero de pruebas y aseguramiento de calidad (QA).

Tu responsabilidad es analizar el proyecto FUGA+ existente, identificar problemas tÃƒÂ©cnicos reales y generar un plan de mejora viable, priorizado y documentado.

Debes trabajar sobre el cÃƒÂ³digo y la documentaciÃƒÂ³n reales del repositorio, no sobre suposiciones.

## 2. Contexto del proyecto

FUGA+ es una aplicaciÃƒÂ³n orientada a la gestiÃƒÂ³n de gastos personales y a la detecciÃƒÂ³n de posibles fugas de dinero mediante patrones de gastos repetitivos.

Sus funcionalidades incluyen:

- Registro de gastos mediante texto.
- Registro de gastos mediante voz, previsto como funcionalidad importante del MVP.
- InterpretaciÃƒÂ³n mediante reglas y diccionarios, sin inteligencia artificial generativa externa.
- ConfirmaciÃƒÂ³n y ediciÃƒÂ³n de gastos.
- Historial de gastos.
- Dashboard con estadÃƒÂ­sticas.
- DetecciÃƒÂ³n de posibles fugas.
- Consulta de evidencias y resÃƒÂºmenes.
- AutenticaciÃƒÂ³n de usuarios.
- Alertas y notificaciones locales.

La aplicaciÃƒÂ³n ya ha sido probada parcialmente en Expo Web y Expo Go para Android, conectada con FastAPI y Supabase.

### TecnologÃƒÂ­as conocidas

- React Native.
- Expo.
- TypeScript.
- Python.
- FastAPI.
- PostgreSQL.
- Supabase Auth.
- Supabase.
- Expo Notifications.
- Git y GitHub.

Debes verificar las versiones, dependencias y configuraciones directamente en el repositorio.

No asumas que una funcionalidad estÃƒÂ¡ completa ÃƒÂºnicamente porque existe cÃƒÂ³digo relacionado con ella.

## 3. Decisiones y restricciones del proyecto

Estas decisiones deben orientar todas tus recomendaciones:

1. La plataforma principal serÃƒÂ¡ Android.
2. El presupuesto disponible es cero; priorizar soluciones gratuitas.
3. Se prefiere Supabase para base de datos y autenticaciÃƒÂ³n.
4. Se prefiere Render para alojar FastAPI, siempre que sea tÃƒÂ©cnicamente viable y gratuito.
5. Se desea conservar y mejorar la arquitectura existente.
6. El proyecto es acadÃƒÂ©mico y debe finalizarse en el menor tiempo razonable.
7. Priorizar mejoras crÃƒÂ­ticas e importantes, evitando optimizaciones innecesarias.
8. No introducir microservicios, Kubernetes u otras tecnologÃƒÂ­as complejas sin necesidad demostrada.
9. No utilizar servicios externos de IA generativa.
10. Conservar las funcionalidades existentes y evitar regresiones.
11. El registro por voz sigue siendo importante para el MVP.
12. La soluciÃƒÂ³n debe permitir obtener evidencias para un manual tÃƒÂ©cnico final.

## 4. Objetivo general

Realizar una auditorÃƒÂ­a tÃƒÂ©cnica del proyecto FUGA+ considerando cuatro aspectos:

1. Calidad del cÃƒÂ³digo.
2. Escalabilidad.
3. Seguridad.
4. Infraestructura.

A partir de los hallazgos, generar un plan de mejora que permita preparar el proyecto para su validaciÃƒÂ³n, compilaciÃƒÂ³n Android y despliegue.

La auditorÃƒÂ­a debe incluir la evaluaciÃƒÂ³n de la arquitectura actual y una propuesta de arquitectura objetivo, conservando los componentes existentes cuando sean adecuados.

---

# 5. ASPECTOS DE LA AUDITORÃƒÂA

## 5.1. AuditorÃƒÂ­a de calidad del cÃƒÂ³digo

Analiza el frontend y backend.

### Frontend

- OrganizaciÃƒÂ³n de carpetas y mÃƒÂ³dulos.
- Componentes reutilizables.
- SeparaciÃƒÂ³n entre interfaz, servicios y lÃƒÂ³gica de negocio.
- Uso de TypeScript.
- Manejo de errores.
- Validaciones.
- CÃƒÂ³digo duplicado.
- Dependencias.
- Compatibilidad entre Expo Web y Android.
- ConfiguraciÃƒÂ³n y utilizaciÃƒÂ³n de ESLint.

### Backend

- OrganizaciÃƒÂ³n de FastAPI.
- SeparaciÃƒÂ³n entre rutas, servicios, dominio y persistencia.
- Calidad y legibilidad del cÃƒÂ³digo Python.
- Validaciones y excepciones.
- Manejo de conexiones y transacciones.
- CÃƒÂ³digo duplicado u obsoleto.
- Dependencias.
- ConfiguraciÃƒÂ³n de Pylint o Flake8.

### Pruebas

- Identificar las pruebas unitarias existentes.
- Identificar las pruebas de integraciÃƒÂ³n existentes.
- Verificar las herramientas de pruebas utilizadas.
- Revisar los resultados que puedan comprobarse localmente.
- Identificar funcionalidades crÃƒÂ­ticas sin pruebas.
- Recomendar las pruebas adicionales necesarias.
- Evaluar si existe mediciÃƒÂ³n de cobertura.

### Herramientas de auditorÃƒÂ­a

Revisar:

- ESLint.
- Pylint o Flake8.
- Pytest.
- TypeScript.
- Herramientas de pruebas del frontend.
- Herramientas de anÃƒÂ¡lisis de dependencias.

Indicar cuÃƒÂ¡les ya estÃƒÂ¡n instaladas y cuÃƒÂ¡les se recomiendan.

No instalar herramientas durante esta etapa.

## 5.2. AuditorÃƒÂ­a de escalabilidad

Evaluar la capacidad del sistema para soportar un crecimiento razonable en usuarios, gastos y consultas.

Revisar:

- Arquitectura actual.
- Modularidad.
- SeparaciÃƒÂ³n de responsabilidades.
- Consultas a PostgreSQL.
- ÃƒÂndices y relaciones.
- PaginaciÃƒÂ³n.
- GestiÃƒÂ³n de conexiones.
- Procesamiento de gastos.
- Rendimiento del dashboard.
- AgrupaciÃƒÂ³n y normalizaciÃƒÂ³n de conceptos.
- Rendimiento de FUGA-01.
- Consultas y cÃƒÂ¡lculos repetitivos.
- Posibles cuellos de botella.
- Limitaciones de los servicios gratuitos.

Proponer mejoras simples y justificadas.

No recomendar cambios arquitectÃƒÂ³nicos grandes si el problema puede resolverse con una optimizaciÃƒÂ³n puntual.

Diferenciar entre riesgos teÃƒÂ³ricos y problemas comprobados.

## 5.3. AuditorÃƒÂ­a de seguridad

Revisar la seguridad del frontend, backend y base de datos.

### AutenticaciÃƒÂ³n y autorizaciÃƒÂ³n

- Supabase Auth.
- ValidaciÃƒÂ³n de tokens en FastAPI.
- GestiÃƒÂ³n y revocaciÃƒÂ³n de sesiones.
- Acceso a recursos por usuario.
- ProtecciÃƒÂ³n de endpoints.
- Controles de autorizaciÃƒÂ³n.

### Base de datos

- PolÃƒÂ­ticas RLS.
- Permisos de tablas.
- Integridad referencial.
- Validaciones.
- ProtecciÃƒÂ³n frente a acceso no autorizado.
- EliminaciÃƒÂ³n lÃƒÂ³gica.
- AuditorÃƒÂ­a de operaciones relevantes.

### AplicaciÃƒÂ³n y API

- ValidaciÃƒÂ³n de entradas.
- Manejo de errores.
- CORS.
- ExposiciÃƒÂ³n de informaciÃƒÂ³n sensible.
- ProtecciÃƒÂ³n de rutas.
- Dependencias vulnerables.
- ConfiguraciÃƒÂ³n de producciÃƒÂ³n.
- Almacenamiento de sesiones en Android.
- Uso correcto de claves pÃƒÂºblicas y secretas.

Verificar que los secretos no estÃƒÂ©n expuestos en el frontend ni incluidos en archivos rastreados por Git.

No mostrar valores de credenciales, contraseÃƒÂ±as, tokens ni cadenas de conexiÃƒÂ³n.

No realizar pruebas destructivas ni ataques sobre servicios externos.

## 5.4. AuditorÃƒÂ­a de infraestructura

Evaluar la infraestructura existente y su preparaciÃƒÂ³n para despliegue.

### Supabase

- Base de datos PostgreSQL.
- AutenticaciÃƒÂ³n.
- Migraciones.
- Variables de entorno.
- LÃƒÂ­mites del plan gratuito.
- ConfiguraciÃƒÂ³n necesaria para producciÃƒÂ³n.

### Render

- Viabilidad de alojar FastAPI.
- Compatibilidad con el proyecto.
- Variables de entorno.
- HTTPS.
- Comandos de instalaciÃƒÂ³n y arranque.
- Limitaciones del servicio gratuito.
- SuspensiÃƒÂ³n por inactividad.
- Persistencia de datos y logs.

### Android y Expo

- ConfiguraciÃƒÂ³n de Expo.
- Dependencias nativas.
- Compatibilidad de Expo Notifications.
- Compatibilidad del registro por voz.
- AutenticaciÃƒÂ³n y enlaces profundos.
- GeneraciÃƒÂ³n de APK instalable.
- Opciones gratuitas de compilaciÃƒÂ³n.
- Diferencias entre Expo Go y una aplicaciÃƒÂ³n Android compilada.

### GitHub y automatizaciÃƒÂ³n

- Estructura del repositorio.
- Ramas y estrategia de versiones.
- Archivos `.gitignore`.
- Configuraciones YAML existentes.
- Posibilidad de incorporar GitHub Actions.
- EjecuciÃƒÂ³n automatizada de pruebas y anÃƒÂ¡lisis estÃƒÂ¡tico.
- GestiÃƒÂ³n segura de variables y secretos.

Determinar quÃƒÂ© automatizaciones serÃƒÂ­an ÃƒÂºtiles y cuÃƒÂ¡les serÃƒÂ­an innecesarias para el alcance acadÃƒÂ©mico.

---

# 6. EVALUACIÃƒâ€œN DE ARQUITECTURA

Analiza la arquitectura realmente implementada.

Debes identificar:

1. Estilo arquitectÃƒÂ³nico actual.
2. Componentes principales.
3. Responsabilidades de cada componente.
4. ComunicaciÃƒÂ³n entre Android, FastAPI y Supabase.
5. Flujo de autenticaciÃƒÂ³n.
6. Flujo de registro de gastos.
7. Flujo de detecciÃƒÂ³n de fugas.
8. Dependencias entre mÃƒÂ³dulos.
9. Ventajas y limitaciones de la arquitectura.
10. Riesgos arquitectÃƒÂ³nicos encontrados.

PropÃƒÂ³n una arquitectura objetivo que mejore la mantenibilidad, seguridad y escalabilidad sin reemplazar innecesariamente las tecnologÃƒÂ­as actuales.

Justifica por quÃƒÂ© conviene conservar o modificar cada componente.

Incluye una descripciÃƒÂ³n que permita elaborar posteriormente diagramas de componentes, despliegue y arquitectura.

No modifiques la arquitectura en esta etapa.

---

# 7. CLASIFICACIÃƒâ€œN DE HALLAZGOS

Clasifica los hallazgos segÃƒÂºn su prioridad:

**P0 Ã¢â‚¬â€ CrÃƒÂ­tico**

Problemas que comprometen la seguridad, impiden el funcionamiento esencial o bloquean el despliegue.

**P1 Ã¢â‚¬â€ Importante**

Problemas que deben corregirse para mejorar la estabilidad, calidad y preparaciÃƒÂ³n de la entrega.

**P2 Ã¢â‚¬â€ Opcional**

Mejoras que pueden quedar documentadas para una versiÃƒÂ³n futura.

Cada hallazgo debe contener:

- Identificador.
- Aspecto auditado.
- DescripciÃƒÂ³n del problema.
- Evidencia en el repositorio.
- Archivo o componente afectado.
- Impacto.
- Riesgo.
- SoluciÃƒÂ³n recomendada.
- Complejidad: baja, media o alta.
- Prioridad.
- Prueba necesaria para comprobar la correcciÃƒÂ³n.

No inventar problemas ni presentar recomendaciones genÃƒÂ©ricas como si fueran hallazgos confirmados.

---

# 8. GENERACIÃƒâ€œN DEL PLAN DE MEJORA

A partir de la auditorÃƒÂ­a, elaborar un plan de mejora tÃƒÂ©cnico y ejecutable.

El plan debe incluir:

## 8.1. Objetivos

Definir los resultados tÃƒÂ©cnicos que se desean alcanzar.

## 8.2. Actividades priorizadas

Para cada actividad indicar:

- CÃƒÂ³digo de actividad.
- Problema que resuelve.
- Archivos o mÃƒÂ³dulos involucrados.
- AcciÃƒÂ³n tÃƒÂ©cnica propuesta.
- Herramientas necesarias.
- Dependencias entre actividades.
- Complejidad estimada.
- Prioridad.
- Criterio de aceptaciÃƒÂ³n.
- Prueba de validaciÃƒÂ³n.

## 8.3. Fases de implementaciÃƒÂ³n

Organizar las mejoras en etapas pequeÃƒÂ±as, evitando cambios simultÃƒÂ¡neos innecesarios.

Priorizar:

1. Correcciones crÃƒÂ­ticas de seguridad y funcionamiento.
2. Calidad del cÃƒÂ³digo y pruebas.
3. Mejoras necesarias de escalabilidad.
4. ConfiguraciÃƒÂ³n de infraestructura.
5. PreparaciÃƒÂ³n del despliegue Android y backend.

El orden puede ajustarse segÃƒÂºn los hallazgos reales.

## 8.4. ValidaciÃƒÂ³n

Definir cÃƒÂ³mo comprobar que cada mejora funciona y no afecta las funcionalidades existentes.

Incluir pruebas unitarias, de integraciÃƒÂ³n, anÃƒÂ¡lisis estÃƒÂ¡tico y pruebas funcionales cuando corresponda.

## 8.5. Criterio de finalizaciÃƒÂ³n

Definir cuÃƒÂ¡ndo FUGA+ estarÃƒÂ¡ suficientemente preparado para pasar a la planificaciÃƒÂ³n del despliegue.

Evitar exigir perfecciÃƒÂ³n tÃƒÂ©cnica o mejoras opcionales que retrasen innecesariamente la entrega.

---

# 9. DOCUMENTACIÃƒâ€œN Y EVIDENCIAS

La auditorÃƒÂ­a y el plan deben facilitar la elaboraciÃƒÂ³n del manual tÃƒÂ©cnico final.

Identificar las evidencias necesarias de:

- Arquitectura del sistema.
- Diagramas.
- Estructura de carpetas.
- Ramas y commits de Git.
- Herramientas de anÃƒÂ¡lisis estÃƒÂ¡tico.
- Resultados de ESLint y Pylint/Flake8.
- Pruebas unitarias.
- Pruebas de integraciÃƒÂ³n.
- Pruebas funcionales.
- Seguridad.
- Base de datos.
- Infraestructura.
- Archivos YAML.
- CI/CD.
- Despliegue.
- Capturas de la aplicaciÃƒÂ³n Android.
- Limitaciones tÃƒÂ©cnicas conocidas.

Indicar en quÃƒÂ© etapa debe capturarse cada evidencia.

---

# 10. UBICACIÃƒâ€œN DE LOS DOCUMENTOS

El proyecto contiene la carpeta `mi-framework-ia`, utilizada para organizar la documentaciÃƒÂ³n del proceso de desarrollo.

Este prompt se guarda en:

`mi-framework-ia/docs/prompts/prompt-01-auditoria-plan-mejora-v1.md`

Los documentos de resultado deben guardarse en:

**Documento 1 Ã¢â‚¬â€ AuditorÃƒÂ­a tÃƒÂ©cnica**

`mi-framework-ia/docs/auditoria/auditoria-tecnica-fugaplus.md`

Contenido esperado:

- Resumen ejecutivo.
- Alcance.
- MetodologÃƒÂ­a de auditorÃƒÂ­a.
- Herramientas revisadas.
- Resultados por los cuatro aspectos.
- Hallazgos y evidencias.
- EvaluaciÃƒÂ³n arquitectÃƒÂ³nica.
- Riesgos.
- Conclusiones.

**Documento 2 Ã¢â‚¬â€ Plan de mejora**

`mi-framework-ia/docs/auditoria/plan-mejora-fugaplus.md`

Contenido esperado:

- Objetivos.
- Mejoras priorizadas.
- Actividades tÃƒÂ©cnicas.
- Fases de implementaciÃƒÂ³n.
- Herramientas.
- Criterios de aceptaciÃƒÂ³n.
- Pruebas.
- Riesgos y dependencias.
- Condiciones para iniciar el despliegue.

En esta primera ejecuciÃƒÂ³n, debes GENERAR ambos documentos Markdown en las rutas indicadas, creando la carpeta `auditoria` si no existe.

No modificar otros archivos del proyecto.

---

# 11. RESTRICCIONES DE EJECUCIÃƒâ€œN

Esta etapa es exclusivamente de auditorÃƒÂ­a, documentaciÃƒÂ³n y planificaciÃƒÂ³n.

EstÃƒÂ¡ permitido:

- Leer cÃƒÂ³digo

- Leer documentaciÃƒÂ³n, configuraciones de ejemplo y pruebas.
- Ejecutar comprobaciones locales aisladas sin cargar credenciales reales ni contactar proveedores.
- Crear exclusivamente los dos documentos Markdown indicados en el apartado 10.

No estÃƒÂ¡ permitido durante esta auditorÃƒÂ­a:

- Implementar mejoras o modificar otros archivos del proyecto.
- Instalar dependencias, ejecutar migraciones, semillas o servicios.
- Leer o revelar valores de .env.local, contraseÃƒÂ±as, claves o tokens.
- Crear, modificar o eliminar datos reales, desplegar, hacer commit o push.

Si una comprobaciÃƒÂ³n requiere modificar el entorno, datos o archivos adicionales, registrar
el lÃƒÂ­mite y proponer su validaciÃƒÂ³n posterior. Distinguir cÃƒÂ³digo existente, pruebas locales,
evidencia histÃƒÂ³rica y pruebas reales. No declarar una funcionalidad aceptada por existir
una implementaciÃƒÂ³n. Finalizar con los documentos creados, hallazgos principales y primera
tarea recomendada. Una ejecuciÃƒÂ³n de este prompt no autoriza el plan de implementaciÃƒÂ³n.
