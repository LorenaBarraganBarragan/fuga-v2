# PROMPT 01 — AUDITORÍA TÉCNICA Y PLAN DE MEJORA DE FUGA+

**Proyecto:** FUGA+  
**Versión del prompt:** 1.0  
**Tipo:** Auditoría técnica, evaluación arquitectónica y planificación de mejoras  
**Etapa:** Diagnóstico y planificación, sin implementación

---

## 1. Rol

Actúa como un equipo de especialistas compuesto por:

- Arquitecto de software.
- Ingeniero de software.
- Especialista en escalabilidad y rendimiento.
- Auditor de calidad de código.
- Especialista en ciberseguridad.
- Ingeniero DevOps e infraestructura.
- Ingeniero de pruebas y aseguramiento de calidad (QA).

Tu responsabilidad es analizar el proyecto FUGA+ existente, identificar problemas técnicos reales y generar un plan de mejora viable, priorizado y documentado.

Debes trabajar sobre el código y la documentación reales del repositorio, no sobre suposiciones.

## 2. Contexto del proyecto

FUGA+ es una aplicación orientada a la gestión de gastos personales y a la detección de posibles fugas de dinero mediante patrones de gastos repetitivos.

Sus funcionalidades incluyen:

- Registro de gastos mediante texto.
- Registro de gastos mediante voz, previsto como funcionalidad importante del MVP.
- Interpretación mediante reglas y diccionarios, sin inteligencia artificial generativa externa.
- Confirmación y edición de gastos.
- Historial de gastos.
- Dashboard con estadísticas.
- Detección de posibles fugas.
- Consulta de evidencias y resúmenes.
- Autenticación de usuarios.
- Alertas y notificaciones locales.

La aplicación ya ha sido probada parcialmente en Expo Web y Expo Go para Android, conectada con FastAPI y Supabase.

### Tecnologías conocidas

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

No asumas que una funcionalidad está completa únicamente porque existe código relacionado con ella.

## 3. Decisiones y restricciones del proyecto

Estas decisiones deben orientar todas tus recomendaciones:

1. La plataforma principal será Android.
2. El presupuesto disponible es cero; priorizar soluciones gratuitas.
3. Se prefiere Supabase para base de datos y autenticación.
4. Se prefiere Render para alojar FastAPI, siempre que sea técnicamente viable y gratuito.
5. Se desea conservar y mejorar la arquitectura existente.
6. El proyecto es académico y debe finalizarse en el menor tiempo razonable.
7. Priorizar mejoras críticas e importantes, evitando optimizaciones innecesarias.
8. No introducir microservicios, Kubernetes u otras tecnologías complejas sin necesidad demostrada.
9. No utilizar servicios externos de IA generativa.
10. Conservar las funcionalidades existentes y evitar regresiones.
11. El registro por voz sigue siendo importante para el MVP.
12. La solución debe permitir obtener evidencias para un manual técnico final.

## 4. Objetivo general

Realizar una auditoría técnica del proyecto FUGA+ considerando cuatro aspectos:

1. Calidad del código.
2. Escalabilidad.
3. Seguridad.
4. Infraestructura.

A partir de los hallazgos, generar un plan de mejora que permita preparar el proyecto para su validación, compilación Android y despliegue.

La auditoría debe incluir la evaluación de la arquitectura actual y una propuesta de arquitectura objetivo, conservando los componentes existentes cuando sean adecuados.

---

# 5. ASPECTOS DE LA AUDITORÍA

## 5.1. Auditoría de calidad del código

Analiza el frontend y backend.

### Frontend

- Organización de carpetas y módulos.
- Componentes reutilizables.
- Separación entre interfaz, servicios y lógica de negocio.
- Uso de TypeScript.
- Manejo de errores.
- Validaciones.
- Código duplicado.
- Dependencias.
- Compatibilidad entre Expo Web y Android.
- Configuración y utilización de ESLint.

### Backend

- Organización de FastAPI.
- Separación entre rutas, servicios, dominio y persistencia.
- Calidad y legibilidad del código Python.
- Validaciones y excepciones.
- Manejo de conexiones y transacciones.
- Código duplicado u obsoleto.
- Dependencias.
- Configuración de Pylint o Flake8.

### Pruebas

- Identificar las pruebas unitarias existentes.
- Identificar las pruebas de integración existentes.
- Verificar las herramientas de pruebas utilizadas.
- Revisar los resultados que puedan comprobarse localmente.
- Identificar funcionalidades críticas sin pruebas.
- Recomendar las pruebas adicionales necesarias.
- Evaluar si existe medición de cobertura.

### Herramientas de auditoría

Revisar:

- ESLint.
- Pylint o Flake8.
- Pytest.
- TypeScript.
- Herramientas de pruebas del frontend.
- Herramientas de análisis de dependencias.

Indicar cuáles ya están instaladas y cuáles se recomiendan.

No instalar herramientas durante esta etapa.

## 5.2. Auditoría de escalabilidad

Evaluar la capacidad del sistema para soportar un crecimiento razonable en usuarios, gastos y consultas.

Revisar:

- Arquitectura actual.
- Modularidad.
- Separación de responsabilidades.
- Consultas a PostgreSQL.
- Índices y relaciones.
- Paginación.
- Gestión de conexiones.
- Procesamiento de gastos.
- Rendimiento del dashboard.
- Agrupación y normalización de conceptos.
- Rendimiento de FUGA-01.
- Consultas y cálculos repetitivos.
- Posibles cuellos de botella.
- Limitaciones de los servicios gratuitos.

Proponer mejoras simples y justificadas.

No recomendar cambios arquitectónicos grandes si el problema puede resolverse con una optimización puntual.

Diferenciar entre riesgos teóricos y problemas comprobados.

## 5.3. Auditoría de seguridad

Revisar la seguridad del frontend, backend y base de datos.

### Autenticación y autorización

- Supabase Auth.
- Validación de tokens en FastAPI.
- Gestión y revocación de sesiones.
- Acceso a recursos por usuario.
- Protección de endpoints.
- Controles de autorización.

### Base de datos

- Políticas RLS.
- Permisos de tablas.
- Integridad referencial.
- Validaciones.
- Protección frente a acceso no autorizado.
- Eliminación lógica.
- Auditoría de operaciones relevantes.

### Aplicación y API

- Validación de entradas.
- Manejo de errores.
- CORS.
- Exposición de información sensible.
- Protección de rutas.
- Dependencias vulnerables.
- Configuración de producción.
- Almacenamiento de sesiones en Android.
- Uso correcto de claves públicas y secretas.

Verificar que los secretos no estén expuestos en el frontend ni incluidos en archivos rastreados por Git.

No mostrar valores de credenciales, contraseñas, tokens ni cadenas de conexión.

No realizar pruebas destructivas ni ataques sobre servicios externos.

## 5.4. Auditoría de infraestructura

Evaluar la infraestructura existente y su preparación para despliegue.

### Supabase

- Base de datos PostgreSQL.
- Autenticación.
- Migraciones.
- Variables de entorno.
- Límites del plan gratuito.
- Configuración necesaria para producción.

### Render

- Viabilidad de alojar FastAPI.
- Compatibilidad con el proyecto.
- Variables de entorno.
- HTTPS.
- Comandos de instalación y arranque.
- Limitaciones del servicio gratuito.
- Suspensión por inactividad.
- Persistencia de datos y logs.

### Android y Expo

- Configuración de Expo.
- Dependencias nativas.
- Compatibilidad de Expo Notifications.
- Compatibilidad del registro por voz.
- Autenticación y enlaces profundos.
- Generación de APK instalable.
- Opciones gratuitas de compilación.
- Diferencias entre Expo Go y una aplicación Android compilada.

### GitHub y automatización

- Estructura del repositorio.
- Ramas y estrategia de versiones.
- Archivos `.gitignore`.
- Configuraciones YAML existentes.
- Posibilidad de incorporar GitHub Actions.
- Ejecución automatizada de pruebas y análisis estático.
- Gestión segura de variables y secretos.

Determinar qué automatizaciones serían útiles y cuáles serían innecesarias para el alcance académico.

---

# 6. EVALUACIÓN DE ARQUITECTURA

Analiza la arquitectura realmente implementada.

Debes identificar:

1. Estilo arquitectónico actual.
2. Componentes principales.
3. Responsabilidades de cada componente.
4. Comunicación entre Android, FastAPI y Supabase.
5. Flujo de autenticación.
6. Flujo de registro de gastos.
7. Flujo de detección de fugas.
8. Dependencias entre módulos.
9. Ventajas y limitaciones de la arquitectura.
10. Riesgos arquitectónicos encontrados.

Propón una arquitectura objetivo que mejore la mantenibilidad, seguridad y escalabilidad sin reemplazar innecesariamente las tecnologías actuales.

Justifica por qué conviene conservar o modificar cada componente.

Incluye una descripción que permita elaborar posteriormente diagramas de componentes, despliegue y arquitectura.

No modifiques la arquitectura en esta etapa.

---

# 7. CLASIFICACIÓN DE HALLAZGOS

Clasifica los hallazgos según su prioridad:

**P0 — Crítico**

Problemas que comprometen la seguridad, impiden el funcionamiento esencial o bloquean el despliegue.

**P1 — Importante**

Problemas que deben corregirse para mejorar la estabilidad, calidad y preparación de la entrega.

**P2 — Opcional**

Mejoras que pueden quedar documentadas para una versión futura.

Cada hallazgo debe contener:

- Identificador.
- Aspecto auditado.
- Descripción del problema.
- Evidencia en el repositorio.
- Archivo o componente afectado.
- Impacto.
- Riesgo.
- Solución recomendada.
- Complejidad: baja, media o alta.
- Prioridad.
- Prueba necesaria para comprobar la corrección.

No inventar problemas ni presentar recomendaciones genéricas como si fueran hallazgos confirmados.

---

# 8. GENERACIÓN DEL PLAN DE MEJORA

A partir de la auditoría, elaborar un plan de mejora técnico y ejecutable.

El plan debe incluir:

## 8.1. Objetivos

Definir los resultados técnicos que se desean alcanzar.

## 8.2. Actividades priorizadas

Para cada actividad indicar:

- Código de actividad.
- Problema que resuelve.
- Archivos o módulos involucrados.
- Acción técnica propuesta.
- Herramientas necesarias.
- Dependencias entre actividades.
- Complejidad estimada.
- Prioridad.
- Criterio de aceptación.
- Prueba de validación.

## 8.3. Fases de implementación

Organizar las mejoras en etapas pequeñas, evitando cambios simultáneos innecesarios.

Priorizar:

1. Correcciones críticas de seguridad y funcionamiento.
2. Calidad del código y pruebas.
3. Mejoras necesarias de escalabilidad.
4. Configuración de infraestructura.
5. Preparación del despliegue Android y backend.

El orden puede ajustarse según los hallazgos reales.

## 8.4. Validación

Definir cómo comprobar que cada mejora funciona y no afecta las funcionalidades existentes.

Incluir pruebas unitarias, de integración, análisis estático y pruebas funcionales cuando corresponda.

## 8.5. Criterio de finalización

Definir cuándo FUGA+ estará suficientemente preparado para pasar a la planificación del despliegue.

Evitar exigir perfección técnica o mejoras opcionales que retrasen innecesariamente la entrega.

---

# 9. DOCUMENTACIÓN Y EVIDENCIAS

La auditoría y el plan deben facilitar la elaboración del manual técnico final.

Identificar las evidencias necesarias de:

- Arquitectura del sistema.
- Diagramas.
- Estructura de carpetas.
- Ramas y commits de Git.
- Herramientas de análisis estático.
- Resultados de ESLint y Pylint/Flake8.
- Pruebas unitarias.
- Pruebas de integración.
- Pruebas funcionales.
- Seguridad.
- Base de datos.
- Infraestructura.
- Archivos YAML.
- CI/CD.
- Despliegue.
- Capturas de la aplicación Android.
- Limitaciones técnicas conocidas.

Indicar en qué etapa debe capturarse cada evidencia.

---

# 10. UBICACIÓN DE LOS DOCUMENTOS

El proyecto contiene la carpeta `mi-framework-ia`, utilizada para organizar la documentación del proceso de desarrollo.

Este prompt se guarda en:

`mi-framework-ia/docs/prompts/prompt-01-auditoria-plan-mejora-v1.md`

Los documentos de resultado deben guardarse en:

**Documento 1 — Auditoría técnica**

`mi-framework-ia/docs/auditoria/auditoria-tecnica-fugaplus.md`

Contenido esperado:

- Resumen ejecutivo.
- Alcance.
- Metodología de auditoría.
- Herramientas revisadas.
- Resultados por los cuatro aspectos.
- Hallazgos y evidencias.
- Evaluación arquitectónica.
- Riesgos.
- Conclusiones.

**Documento 2 — Plan de mejora**

`mi-framework-ia/docs/auditoria/plan-mejora-fugaplus.md`

Contenido esperado:

- Objetivos.
- Mejoras priorizadas.
- Actividades técnicas.
- Fases de implementación.
- Herramientas.
- Criterios de aceptación.
- Pruebas.
- Riesgos y dependencias.
- Condiciones para iniciar el despliegue.

En esta primera ejecución, debes GENERAR ambos documentos Markdown en las rutas indicadas, creando la carpeta `auditoria` si no existe.

No modificar otros archivos del proyecto.

---

# 11. RESTRICCIONES DE EJECUCIÓN

Esta etapa es exclusivamente de auditoría, documentación y planificación.

Está permitido:

- Leer código