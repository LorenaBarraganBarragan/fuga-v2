-- 0002_catalogo.sql — Catálogo de categorías y reglas de fuga

CREATE TABLE IF NOT EXISTS categoria (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  nombre VARCHAR(40) NOT NULL UNIQUE,
  orden SMALLINT NOT NULL UNIQUE,
  activa BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TRIGGER categoria_set_updated_at
BEFORE UPDATE ON categoria
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TABLE IF NOT EXISTS regla_fuga (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  codigo VARCHAR(20) NOT NULL UNIQUE,
  nombre VARCHAR(80) NOT NULL,
  descripcion TEXT NOT NULL,
  activa BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TRIGGER regla_fuga_set_updated_at
BEFORE UPDATE ON regla_fuga
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TABLE IF NOT EXISTS regla_fuga_version (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  regla_id UUID NOT NULL REFERENCES regla_fuga(id) ON DELETE RESTRICT,
  version VARCHAR(10) NOT NULL,
  parametros JSONB NOT NULL,
  vigente_desde TIMESTAMPTZ NOT NULL DEFAULT now(),
  vigente_hasta TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (regla_id, version)
);

CREATE UNIQUE INDEX IF NOT EXISTS regla_version_vigente_uq
  ON regla_fuga_version (regla_id) WHERE vigente_hasta IS NULL;

-- Seed inicial de catálogo (9 categorías D-02)
INSERT INTO categoria (nombre, orden) VALUES
  ('Alimentación', 1),
  ('Transporte', 2),
  ('Vivienda', 3),
  ('Servicios', 4),
  ('Educación', 5),
  ('Salud', 6),
  ('Entretenimiento', 7),
  ('Compras', 8),
  ('Otros', 9)
ON CONFLICT (nombre) DO NOTHING;

-- Seed de regla FUGA-01 y versión 1.0 (D-01)
INSERT INTO regla_fuga (codigo, nombre, descripcion)
VALUES (
  'FUGA-01',
  'Patrón repetido de gasto',
  'Detecta gastos repetidos de bajo monto en una ventana de 30 días'
)
ON CONFLICT (codigo) DO NOTHING;

INSERT INTO regla_fuga_version (regla_id, version, parametros, vigente_desde)
SELECT
  id,
  '1.0',
  '{"ventana_dias": 30, "min_gastos": 3, "min_fechas": 3, "monto_min": 1000, "monto_max": 30000, "suma_min": 15000, "zona": "America/Bogota"}'::jsonb,
  now()
FROM regla_fuga
WHERE codigo = 'FUGA-01'
ON CONFLICT (regla_id, version) DO NOTHING;
