-- 0006_rls.sql — Row Level Security e aislamiento de datos (RF-033)

ALTER TABLE public.perfil ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.gasto ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.fuga ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.fuga_evidencia ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.categoria ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.regla_fuga ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.regla_fuga_version ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS categoria_select_autenticado ON public.categoria;
CREATE POLICY categoria_select_autenticado ON public.categoria
  FOR SELECT TO authenticated USING (true);
DROP POLICY IF EXISTS regla_select_autenticado ON public.regla_fuga;
CREATE POLICY regla_select_autenticado ON public.regla_fuga
  FOR SELECT TO authenticated USING (true);
DROP POLICY IF EXISTS regla_version_select_autenticado ON public.regla_fuga_version;
CREATE POLICY regla_version_select_autenticado ON public.regla_fuga_version
  FOR SELECT TO authenticated USING (true);

-- Política de lectura de perfil propio para usuarios autenticados
DROP POLICY IF EXISTS perfil_select_propio ON public.perfil;
CREATE POLICY perfil_select_propio ON public.perfil
  FOR SELECT TO authenticated USING (id = (SELECT auth.uid()) AND disabled_at IS NULL);

-- Política de actualización de campos propios permitidos
DROP POLICY IF EXISTS perfil_update_propio ON public.perfil;
CREATE POLICY perfil_update_propio ON public.perfil
  FOR UPDATE TO authenticated
  USING (id = (SELECT auth.uid()) AND disabled_at IS NULL)
  WITH CHECK (id = (SELECT auth.uid()) AND disabled_at IS NULL);

-- Las tablas financieras (gasto, fuga, fuga_evidencia) tienen RLS activo
-- pero NO tienen políticas de inserción ni modificación para clientes directos
-- ya que FastAPI es la única puerta de acceso a los datos financieros (DA-01).
