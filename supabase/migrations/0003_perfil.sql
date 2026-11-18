-- 0003_perfil.sql — Perfil de usuario y trigger de provisión desde auth.users

CREATE TABLE IF NOT EXISTS public.perfil (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  nombres VARCHAR(80),
  apellido VARCHAR(80),
  telefono VARCHAR(10) CHECK (telefono IS NULL OR telefono ~ '^[0-9]{10}$'),
  foto_url TEXT,
  foto_google_url TEXT,
  rol VARCHAR(15) NOT NULL DEFAULT 'usuario'
      CHECK (rol IN ('usuario', 'administrador')),
  disabled_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS perfil_rol_idx ON public.perfil (rol);
CREATE INDEX IF NOT EXISTS perfil_disabled_idx ON public.perfil (disabled_at) WHERE disabled_at IS NOT NULL;

CREATE OR REPLACE TRIGGER perfil_set_updated_at
BEFORE UPDATE ON public.perfil
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

-- Función que aprovisiona automáticamente el perfil cuando se registra un usuario en Supabase Auth
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER LANGUAGE plpgsql SECURITY DEFINER SET search_path = '' AS $$
BEGIN
  INSERT INTO public.perfil (id, rol)
  VALUES (NEW.id, 'usuario')
  ON CONFLICT (id) DO NOTHING;
  RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER on_auth_user_created
AFTER INSERT ON auth.users
FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Existing Auth users are bootstrapped without modifying their metadata or existing profiles.
INSERT INTO public.perfil (id, rol)
SELECT id, 'usuario' FROM auth.users
ON CONFLICT (id) DO NOTHING;
