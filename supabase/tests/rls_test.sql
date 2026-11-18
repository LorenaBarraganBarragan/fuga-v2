-- Alias compatible: mismo contenido que verificar_esquema.sql.
-- Verificación de solo lectura después de 0001..0009. No prueba JWT ni crea usuarios.
BEGIN;
DO $$
DECLARE relation_name text;
BEGIN
  IF (SELECT count(*) FROM public.categoria) <> 9 THEN
    RAISE EXCEPTION 'El catálogo debe contener exactamente nueve categorías.';
  END IF;
  IF NOT EXISTS (SELECT 1 FROM public.regla_fuga r JOIN public.regla_fuga_version v ON v.regla_id=r.id
    WHERE r.codigo='FUGA-01' AND v.version='1.0' AND v.vigente_hasta IS NULL
      AND v.parametros='{"ventana_dias":30,"min_gastos":3,"min_fechas":3,"monto_min":1000,"monto_max":30000,"suma_min":15000,"zona":"America/Bogota"}'::jsonb) THEN
    RAISE EXCEPTION 'FUGA-01 1.0 no coincide con los parámetros aprobados.';
  END IF;
  FOREACH relation_name IN ARRAY ARRAY['categoria','regla_fuga','regla_fuga_version','perfil','gasto',
    'fuga','fuga_evidencia','auditoria','actividad_mensual','tarea_retencion'] LOOP
    IF NOT EXISTS (SELECT 1 FROM pg_class WHERE oid=('public.'||relation_name)::regclass AND relrowsecurity) THEN
      RAISE EXCEPTION 'RLS no está activo en %.',relation_name;
    END IF;
    IF has_table_privilege('anon','public.'||relation_name,'INSERT,UPDATE,DELETE,TRUNCATE')
      OR has_table_privilege('authenticated','public.'||relation_name,'INSERT,UPDATE,DELETE,TRUNCATE') THEN
      RAISE EXCEPTION 'Hay privilegios generales de escritura del cliente en %.',relation_name;
    END IF;
  END LOOP;
  IF has_column_privilege('authenticated','public.perfil','rol','UPDATE')
    OR has_column_privilege('authenticated','public.perfil','disabled_at','UPDATE')
    OR has_column_privilege('authenticated','public.perfil','auth_sync_pendiente','UPDATE')
    OR has_column_privilege('authenticated','public.perfil','foto_url','UPDATE') THEN
    RAISE EXCEPTION 'El cliente puede modificar columnas protegidas del perfil.';
  END IF;
  IF EXISTS (SELECT 1 FROM pg_policies WHERE schemaname='public' AND tablename IN ('gasto','fuga','fuga_evidencia')) THEN
    RAISE EXCEPTION 'Los clientes no deben tener políticas de acceso financiero directo.';
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgrelid='auth.users'::regclass
    AND tgname='on_auth_user_created' AND NOT tgisinternal AND tgenabled='O') THEN
    RAISE EXCEPTION 'Falta el trigger de aprovisionamiento de perfiles.';
  END IF;
END $$;

SET LOCAL ROLE authenticated;
DO $$ BEGIN
  IF EXISTS (SELECT 1 FROM public.gasto) OR EXISTS (SELECT 1 FROM public.fuga)
     OR EXISTS (SELECT 1 FROM public.fuga_evidencia) THEN
    RAISE EXCEPTION 'Se filtraron datos financieros por acceso directo.';
  END IF;
END $$;
ROLLBACK;
SELECT 'OK: esquema, catálogo, permisos y denegación financiera directa' AS resultado;
