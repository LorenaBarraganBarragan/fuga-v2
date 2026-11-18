# Revisión de dependencias — 2026-11-18

Consultas de avisos ejecutadas sin instalación/corrección automática ni llamadas a Supabase.
Reportes completos: backend/docs/audit-dependencias.json y mobile/docs/audit-dependencias.json.

## Python

pip-audit contra requirements.lock, con --disable-pip y --no-deps, devolvió salida 0
y cero dependencias con avisos. El runtime de ensayo Linux/Render preparado es Python
3.12.16; Windows conserva 3.12.6. No se cambió Python del sistema.

## npm: conservar resultado bruto y revisar su significado

npm audit devolvió salida 1 y **25 alertas high propagadas**, todas derivadas de un
único aviso de picomatch, GHSA-fc5q-39xc-vjpf / CVE-2026-112366. No son 25 fallos
independientes encontrados en el código de FUGA+. El árbol incluye picomatch 4.0.7
y copias 2.3.2 usadas por herramientas de patrones/construcción.

Al contrastar la fuente primaria, el aviso figura **retirado el 2026-11-18**, sin
versión parcheada declarada. Se conserva el JSON de npm y este contraste en lugar
de anunciar cero alertas brutas o aplicar una reparación inventada.
[Ficha oficial](https://github.com/advisories/GHSA-fc5q-39xc-vjpf).

El mantenedor rechazó la clasificación del problema para patrones definidos por
el usuario y recomienda no aceptar patrones no confiables. En los flujos auditados,
el texto financiero se envía a reglas Python y no se utiliza como patrón glob de
Metro/picomatch. Esto es un análisis de alcance del uso actual, no una garantía
universal de seguridad del paquete. [Discusión del mantenedor](https://github.com/micromatch/picomatch/pull/235).

La reparación sugerida por npm degrada Expo 58 a 54 y React Native 0.88 a 0.83.
No se ejecutó npm audit fix --force ni se alteró el stack aprobado. Tampoco se añadió
un override a una versión supuestamente corregida que la ficha no declara.
Revisar el aviso/feed al preparar distribución y actuar si aparece una corrección
compatible o una exposición aplicable; no suprimir globalmente avisos futuros.

## Herramientas de QA

coverage se añadió al lock Python. react-test-renderer 19.3.0, coincidente con React,
añadió dos paquetes de desarrollo y permite pruebas de componentes con los controles
nativos simulados, dentro del ejecutor Node existente. No forma parte del bundle de
la aplicación. La herramienta está deprecada: sus avisos no se silencian y una
migración a otra herramienta de componentes queda documentada como mantenimiento.
No se instaló Jest ni se reemplazó el stack de pruebas para esta entrega.
[Aviso del proyecto React](https://react.dev/warnings/react-test-renderer).

Los tests, TypeScript y configuración del SDK deben repetirse ante cambios del lock.
Los avisos de Gradle/SDK o TestClient también se registran por separado: no justificar
una migración tecnológica ni ocultar una compilación fallida por ser upstream.
