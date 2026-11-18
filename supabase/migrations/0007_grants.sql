-- 0007_grants.sql — Permisos mínimos y revocaciones de seguridad

-- Supabase puede conceder privilegios por defecto: partir de cero, incluidos TRUNCATE/TRIGGER.
REVOKE ALL ON public.perfil, public.gasto, public.fuga, public.fuga_evidencia,
  public.categoria, public.regla_fuga, public.regla_fuga_version FROM PUBLIC, anon, authenticated;

-- Prohibir la escalación de privilegios modificando rol o estado de habilitación directamente
REVOKE UPDATE (id, nombres, apellido, telefono, foto_url, foto_google_url, rol, disabled_at, created_at, updated_at)
  ON public.perfil FROM PUBLIC, anon, authenticated;

-- Permitir lectura de catálogos a usuarios autenticados
GRANT SELECT ON public.categoria, public.regla_fuga, public.regla_fuga_version TO authenticated;
GRANT SELECT ON public.perfil, public.gasto, public.fuga, public.fuga_evidencia TO authenticated;
-- Las tablas financieras conservan cero políticas de acceso del cliente, incluso de lectura.
REVOKE ALL ON FUNCTION public.handle_new_user() FROM PUBLIC, anon, authenticated;
