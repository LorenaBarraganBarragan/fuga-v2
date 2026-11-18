-- FUGA+ 3.0: refuerzo aditivo. No elimina tablas, filas ni cuentas.
-- Si existen datos incompatibles, VALIDATE CONSTRAINT falla sin corregirlos ni borrarlos.

REVOKE CREATE ON SCHEMA public FROM PUBLIC, anon, authenticated;
GRANT USAGE ON SCHEMA public TO anon, authenticated;

REVOKE ALL ON public.auditoria, public.actividad_mensual, public.tarea_retencion
  FROM PUBLIC, anon, authenticated;
REVOKE UPDATE (auth_sync_pendiente) ON public.perfil FROM PUBLIC, anon, authenticated;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conrelid='public.perfil'::regclass AND conname='perfil_nombres_validos_ck') THEN
    ALTER TABLE public.perfil ADD CONSTRAINT perfil_nombres_validos_ck
      CHECK (nombres IS NULL OR length(btrim(nombres)) BETWEEN 2 AND 80) NOT VALID;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conrelid='public.perfil'::regclass AND conname='perfil_apellido_valido_ck') THEN
    ALTER TABLE public.perfil ADD CONSTRAINT perfil_apellido_valido_ck
      CHECK (apellido IS NULL OR length(btrim(apellido)) BETWEEN 2 AND 80) NOT VALID;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conrelid='public.categoria'::regclass AND conname='categoria_catalogo_cerrado_ck') THEN
    ALTER TABLE public.categoria ADD CONSTRAINT categoria_catalogo_cerrado_ck CHECK ((nombre,orden) IN (
      ('Alimentación',1), ('Transporte',2), ('Vivienda',3), ('Servicios',4), ('Educación',5),
      ('Salud',6), ('Entretenimiento',7), ('Compras',8), ('Otros',9))) NOT VALID;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conrelid='public.regla_fuga_version'::regclass AND conname='regla_parametros_objeto_ck') THEN
    ALTER TABLE public.regla_fuga_version ADD CONSTRAINT regla_parametros_objeto_ck
      CHECK (jsonb_typeof(parametros)='object') NOT VALID;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conrelid='public.actividad_mensual'::regclass AND conname='actividad_mes_inicio_ck') THEN
    ALTER TABLE public.actividad_mensual ADD CONSTRAINT actividad_mes_inicio_ck
      CHECK (periodo >= DATE '2020-01-01' AND EXTRACT(DAY FROM periodo)=1) NOT VALID;
  END IF;
END $$;

ALTER TABLE public.perfil VALIDATE CONSTRAINT perfil_nombres_validos_ck;
ALTER TABLE public.perfil VALIDATE CONSTRAINT perfil_apellido_valido_ck;
ALTER TABLE public.categoria VALIDATE CONSTRAINT categoria_catalogo_cerrado_ck;
ALTER TABLE public.regla_fuga_version VALIDATE CONSTRAINT regla_parametros_objeto_ck;
ALTER TABLE public.actividad_mensual VALIDATE CONSTRAINT actividad_mes_inicio_ck;

DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM public.fuga_evidencia e
    JOIN public.fuga f ON f.id=e.fuga_id JOIN public.gasto g ON g.id=e.gasto_id
    WHERE f.usuario_id<>g.usuario_id) THEN
    RAISE EXCEPTION 'Existe evidencia de propietarios distintos; revisar sin borrar datos.' USING ERRCODE='23514';
  END IF;
END $$;

-- Los CHECK de fechas son estáticos; el límite de hoy se comprueba en el momento de escribir.
CREATE OR REPLACE FUNCTION public.validar_fecha_gasto()
RETURNS trigger LANGUAGE plpgsql SET search_path='' AS $$
BEGIN
  IF NEW.fecha_gasto > (statement_timestamp() AT TIME ZONE 'America/Bogota')::date THEN
    RAISE EXCEPTION 'La fecha del gasto no puede ser futura en America/Bogota.' USING ERRCODE='23514';
  END IF;
  RETURN NEW;
END $$;
CREATE OR REPLACE TRIGGER gasto_fecha_no_futura
BEFORE INSERT OR UPDATE OF fecha_gasto ON public.gasto
FOR EACH ROW EXECUTE FUNCTION public.validar_fecha_gasto();

-- Impide que una credencial privilegiada cambie accidentalmente el propietario de un recurso.
CREATE OR REPLACE FUNCTION public.impedir_cambio_propietario()
RETURNS trigger LANGUAGE plpgsql SET search_path='' AS $$
BEGIN
  IF NEW.usuario_id IS DISTINCT FROM OLD.usuario_id THEN
    RAISE EXCEPTION 'El propietario del recurso es inmutable.' USING ERRCODE='23514';
  END IF;
  RETURN NEW;
END $$;
CREATE OR REPLACE TRIGGER gasto_propietario_inmutable
BEFORE UPDATE OF usuario_id ON public.gasto
FOR EACH ROW EXECUTE FUNCTION public.impedir_cambio_propietario();
CREATE OR REPLACE TRIGGER fuga_propietario_inmutable
BEFORE UPDATE OF usuario_id ON public.fuga
FOR EACH ROW EXECUTE FUNCTION public.impedir_cambio_propietario();

CREATE OR REPLACE FUNCTION public.validar_propietario_evidencia()
RETURNS trigger LANGUAGE plpgsql SET search_path='' AS $$
DECLARE fuga_usuario uuid; gasto_usuario uuid;
BEGIN
  SELECT usuario_id INTO fuga_usuario FROM public.fuga WHERE id=NEW.fuga_id;
  SELECT usuario_id INTO gasto_usuario FROM public.gasto WHERE id=NEW.gasto_id;
  IF fuga_usuario IS NULL OR gasto_usuario IS NULL THEN
    RAISE EXCEPTION 'Fuga o gasto inexistente.' USING ERRCODE='23503';
  END IF;
  IF fuga_usuario IS DISTINCT FROM gasto_usuario THEN
    RAISE EXCEPTION 'La evidencia debe pertenecer al propietario de la fuga.' USING ERRCODE='23514';
  END IF;
  RETURN NEW;
END $$;
CREATE OR REPLACE TRIGGER fuga_evidencia_mismo_propietario
BEFORE INSERT OR UPDATE ON public.fuga_evidencia
FOR EACH ROW EXECUTE FUNCTION public.validar_propietario_evidencia();

REVOKE ALL ON FUNCTION public.validar_fecha_gasto(), public.impedir_cambio_propietario(),
  public.validar_propietario_evidencia(), public.set_updated_at() FROM PUBLIC, anon, authenticated;

-- Un cambio de parámetros exige una nueva versión, no modificar la evidencia histórica.
CREATE OR REPLACE FUNCTION public.impedir_edicion_regla_version()
RETURNS trigger LANGUAGE plpgsql SET search_path='' AS $$
BEGIN
  IF NEW.parametros IS DISTINCT FROM OLD.parametros OR NEW.version IS DISTINCT FROM OLD.version
     OR NEW.regla_id IS DISTINCT FROM OLD.regla_id THEN
    RAISE EXCEPTION 'Crear una nueva versión de regla para cambiar parámetros.' USING ERRCODE='23514';
  END IF;
  RETURN NEW;
END $$;
CREATE OR REPLACE TRIGGER regla_version_inmutable
BEFORE UPDATE ON public.regla_fuga_version
FOR EACH ROW EXECUTE FUNCTION public.impedir_edicion_regla_version();
REVOKE ALL ON FUNCTION public.impedir_edicion_regla_version() FROM PUBLIC, anon, authenticated;
