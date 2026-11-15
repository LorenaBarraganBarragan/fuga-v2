-- 0006_rls.sql — Row Level Security e aislamiento de datos (RF-033)

ALTER TABLE perfil ENABLE ROW LEVEL SECURITY;
ALTER TABLE gasto ENABLE ROW LEVEL SECURITY;
ALTER TABLE fuga ENABLE ROW LEVEL SECURITY;
ALTER TABLE fuga_evidencia ENABLE ROW LEVEL SECURITY;

-- Política de lectura de perfil propio para usuarios autenticados
DROP POLICY IF EXISTS perfil_select_propio ON perfil;
CREATE POLICY perfil_select_propio ON perfil
  FOR SELECT TO authenticated USING (id = auth.uid());

-- Política de actualización de campos propios permitidos
DROP POLICY IF EXISTS perfil_update_propio ON perfil;
CREATE POLICY perfil_update_propio ON perfil
  FOR UPDATE TO authenticated USING (id = auth.uid());

-- Las tablas financieras (gasto, fuga, fuga_evidencia) tienen RLS activo
-- pero NO tienen políticas de inserción ni modificación para clientes directos
-- ya que FastAPI es la única puerta de acceso a los datos financieros (DA-01).
