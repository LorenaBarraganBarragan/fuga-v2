-- 0005_fugas.sql — Fugas detectadas y snapshot de evidencia trazable

CREATE TABLE IF NOT EXISTS fuga (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  usuario_id UUID NOT NULL REFERENCES perfil(id) ON DELETE RESTRICT,
  regla_version_id UUID NOT NULL REFERENCES regla_fuga_version(id) ON DELETE RESTRICT,
  categoria_id UUID NOT NULL REFERENCES categoria(id) ON DELETE RESTRICT,
  descripcion_normalizada VARCHAR(120) NOT NULL,
  ocurrencias SMALLINT NOT NULL CHECK (ocurrencias > 0),
  monto_acumulado_cop BIGINT NOT NULL CHECK (monto_acumulado_cop > 0),
  fecha_desde DATE NOT NULL,
  fecha_hasta DATE NOT NULL,
  vigente BOOLEAN NOT NULL DEFAULT TRUE,
  detectada_en TIMESTAMPTZ NOT NULL DEFAULT now(),
  actualizada_en TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (fecha_hasta >= fecha_desde)
);

CREATE INDEX IF NOT EXISTS fuga_usuario_vigente_idx ON fuga (usuario_id, vigente);
CREATE INDEX IF NOT EXISTS fuga_regla_version_idx ON fuga (regla_version_id);

-- Índice único parcial (C-12): permite recalcular conservando snapshots históricos invalidados
CREATE UNIQUE INDEX IF NOT EXISTS fuga_snapshot_uq
  ON fuga (usuario_id, regla_version_id, categoria_id, descripcion_normalizada)
  WHERE vigente = TRUE;

CREATE TABLE IF NOT EXISTS fuga_evidencia (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  fuga_id UUID NOT NULL REFERENCES fuga(id) ON DELETE CASCADE,
  gasto_id UUID NOT NULL REFERENCES gasto(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT fuga_evidencia_uq UNIQUE (fuga_id, gasto_id)
);

CREATE INDEX IF NOT EXISTS fuga_evidencia_gasto_idx ON fuga_evidencia (gasto_id);
