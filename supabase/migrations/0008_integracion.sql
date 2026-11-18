-- Migración ADITIVA LOCAL; requiere aprobación para aplicar en Supabase remoto.
ALTER TABLE public.gasto ADD COLUMN IF NOT EXISTS request_hash TEXT;
ALTER TABLE public.gasto ADD COLUMN IF NOT EXISTS idempotency_response JSONB;
ALTER TABLE public.fuga ADD COLUMN IF NOT EXISTS evidencia_hash TEXT;
ALTER TABLE public.perfil ADD COLUMN IF NOT EXISTS auth_sync_pendiente BOOLEAN NOT NULL DEFAULT FALSE;

CREATE TABLE IF NOT EXISTS public.auditoria (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  actor_id UUID NOT NULL REFERENCES public.perfil(id),
  accion VARCHAR(60) NOT NULL,
  objetivo_id UUID,
  resultado VARCHAR(20) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS auditoria_fecha_idx ON public.auditoria(created_at);
ALTER TABLE public.auditoria ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.auditoria FROM anon, authenticated;

-- Revocar el permiso general antes de permitir columnas concretas.
REVOKE UPDATE ON public.perfil FROM anon, authenticated;
REVOKE UPDATE (id, rol, disabled_at, foto_google_url, created_at, updated_at) ON public.perfil FROM anon, authenticated;
REVOKE UPDATE (foto_url) ON public.perfil FROM anon, authenticated;
GRANT UPDATE (nombres, apellido, telefono) ON public.perfil TO authenticated;
-- RLS sin políticas financieras permite SELECT pero siempre oculta todas las filas.
GRANT SELECT ON public.perfil, public.gasto, public.fuga, public.fuga_evidencia TO authenticated;

-- Datos administrativos para HU-30 (sin información financiera individual).
CREATE TABLE IF NOT EXISTS public.actividad_mensual (
  usuario_id UUID NOT NULL REFERENCES public.perfil(id),
  periodo DATE NOT NULL,
  PRIMARY KEY (usuario_id, periodo)
);
ALTER TABLE public.actividad_mensual ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.actividad_mensual FROM anon, authenticated;

-- Revocaciones pendientes y retención; ningún borrado automático de datos reales.
CREATE TABLE IF NOT EXISTS public.tarea_retencion (
  usuario_id UUID PRIMARY KEY REFERENCES public.perfil(id),
  suprimir_desde TIMESTAMPTZ NOT NULL,
  estado VARCHAR(20) NOT NULL DEFAULT 'pendiente' CHECK (estado IN ('pendiente','cancelada'))
);
ALTER TABLE public.tarea_retencion ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.tarea_retencion FROM anon, authenticated;
