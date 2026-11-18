-- 0004_gasto.sql — Tabla de gastos personales e índices de consulta

CREATE TABLE IF NOT EXISTS public.gasto (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  usuario_id UUID NOT NULL REFERENCES public.perfil(id) ON DELETE RESTRICT,
  categoria_id UUID NOT NULL REFERENCES public.categoria(id) ON DELETE RESTRICT,
  monto_cop BIGINT NOT NULL CHECK (monto_cop BETWEEN 1 AND 100000000),
  descripcion VARCHAR(120) NOT NULL
    CHECK (length(btrim(descripcion)) BETWEEN 1 AND 120),
  texto_original VARCHAR(280), -- Nullable; en MVP se persiste NULL (C-01)
  fecha_gasto DATE NOT NULL
    CHECK (fecha_gasto >= DATE '2020-01-01'),
  moneda CHAR(3) NOT NULL DEFAULT 'COP' CHECK (moneda = 'COP'),
  diccionario_version VARCHAR(10) NOT NULL,
  reglas_version VARCHAR(10) NOT NULL,
  clave_idempotencia UUID NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  deleted_at TIMESTAMPTZ,
  CONSTRAINT gasto_idempotencia_uq UNIQUE (usuario_id, clave_idempotencia)
);

-- Índices de consulta optimizados
CREATE INDEX IF NOT EXISTS gasto_usuario_fecha_idx
  ON public.gasto (usuario_id, fecha_gasto DESC, created_at DESC, id DESC);

CREATE INDEX IF NOT EXISTS gasto_usuario_categoria_idx
  ON public.gasto (usuario_id, categoria_id);

CREATE INDEX IF NOT EXISTS gasto_usuario_ventana_idx
  ON public.gasto (usuario_id, fecha_gasto) WHERE deleted_at IS NULL;

CREATE OR REPLACE TRIGGER gasto_set_updated_at
BEFORE UPDATE ON public.gasto
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();
