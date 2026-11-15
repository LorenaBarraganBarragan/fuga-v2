# Mapa del Esquema de Base de Datos y Trazabilidad a Historias de Usuario

Documento de referencia para el modelo de datos relacional de FUGA+ en Supabase PostgreSQL.

---

## 1. Tablas del MVP y Mapeo a Historias de Usuario

| Tabla | Módulo | Historias de Usuario (HU) | Requerimientos (RF) | Descripción |
|---|---|---|---|---|
| `categoria` | M3, M5, M6 | HU-10, HU-11, HU-12, HU-20, HU-21 | RF-011, RF-021 | Catálogo cerrado de 9 categorías inmutables (D-02). |
| `regla_fuga` | M6 | HU-23, HU-24 | RF-023, RF-024 | Definición base de reglas deterministas de detección (FUGA-01). |
| `regla_fuga_version` | M6 | HU-23, HU-24 | RF-023, RF-024 | Versiones y parámetros JSONB vigentes de cada regla. |
| `perfil` | M1, M8 | HU-01, HU-02, HU-04, HU-33 | RF-001, RF-002, RF-004, RF-033 | Datos de perfil asociados a `auth.users`, roles y control de acceso. |
| `gasto` | M3, M5, M6, M8 | HU-12, HU-13, HU-14, HU-20, HU-21, HU-23, HU-33 | RF-012, RF-013, RF-014, RF-020, RF-021, RF-033 | Gastos confirmados por el usuario con clave de idempotencia y scoping por propietario. |
| `fuga` | M6, M8 | HU-23, HU-24, HU-33 | RF-023, RF-024, RF-033 | Posibles fugas candidatas detectadas bajo demanda, versionadas por regla. |
| `fuga_evidencia` | M6, M8 | HU-23, HU-24, HU-33 | RF-024, RF-033 | Relación Many-to-Many entre fugas y gastos de soporte específicos. |

---

## 2. Decisiones Arquitectónicas Aplicadas al Esquema

1. **C-01:** `gasto.texto_original` es nullable y se persiste como `NULL` en el MVP para minimizar almacenamiento de texto no estructurado.
2. **C-02:** `perfil.nombres` y `perfil.apellido` son opcionales (nullable) en el registro inicial.
3. **C-03:** Idempotencia por clave UUID de 24 horas (`gasto_idempotencia_uq UNIQUE (usuario_id, clave_idempotencia)`).
4. **C-12:** `fuga.regla_version_id` es una FK UUID que referencia directamente `regla_fuga_version(id)`, garantizando integridad referencial estricta.
5. **DA-01:** FastAPI es la única puerta de enlace autorizada para datos financieros. RLS revoca acceso directo a tablas de gastos y fugas a clientes móviles.
