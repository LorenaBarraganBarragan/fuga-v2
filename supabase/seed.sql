-- seed.sql — Datos iniciales del catálogo para FUGA+

-- 1. Catálogo cerrado de 9 categorías (D-02)
INSERT INTO public.categoria (nombre, orden) VALUES
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

-- 2. Regla de fuga determinista FUGA-01 (D-01)
INSERT INTO public.regla_fuga (codigo, nombre, descripcion)
VALUES (
  'FUGA-01',
  'Patrón repetido de gasto',
  'Detecta gastos repetidos de bajo monto en una ventana de 30 días'
)
ON CONFLICT (codigo) DO NOTHING;

-- 3. Versión 1.0 de la regla FUGA-01 con parámetros configurables
INSERT INTO public.regla_fuga_version (regla_id, version, parametros, vigente_desde)
SELECT
  id,
  '1.0',
  '{"ventana_dias": 30, "min_gastos": 3, "min_fechas": 3, "monto_min": 1000, "monto_max": 30000, "suma_min": 15000, "zona": "America/Bogota"}'::jsonb,
  now()
FROM public.regla_fuga
WHERE codigo = 'FUGA-01'
ON CONFLICT (regla_id, version) DO NOTHING;
