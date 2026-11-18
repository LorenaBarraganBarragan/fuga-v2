-- HU-08: registro privado de cargas; no modifica perfiles ni fotografías existentes.
CREATE TABLE IF NOT EXISTS public.perfil_foto_carga (
  public_id TEXT PRIMARY KEY,
  usuario_id UUID NOT NULL REFERENCES public.perfil(id) ON DELETE CASCADE,
  estado TEXT NOT NULL DEFAULT 'pendiente'
    CHECK (estado IN ('pendiente','activa','retirada','cancelada','eliminada')),
  secure_url TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (estado <> 'activa' OR secure_url IS NOT NULL)
);
CREATE INDEX IF NOT EXISTS perfil_foto_carga_usuario_idx
  ON public.perfil_foto_carga(usuario_id,created_at);
CREATE UNIQUE INDEX IF NOT EXISTS perfil_foto_carga_activa_idx
  ON public.perfil_foto_carga(usuario_id) WHERE estado='activa';
CREATE INDEX IF NOT EXISTS perfil_foto_carga_limpieza_idx
  ON public.perfil_foto_carga(updated_at) WHERE estado IN ('pendiente','retirada','cancelada');
ALTER TABLE public.perfil_foto_carga ENABLE ROW LEVEL SECURITY;
-- Solo FastAPI con conexión de servidor. Sin acceso mediante PostgREST del cliente.
REVOKE ALL ON public.perfil_foto_carga FROM PUBLIC,anon,authenticated;
