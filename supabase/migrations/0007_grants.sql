-- 0007_grants.sql — Permisos mínimos y revocaciones de seguridad

-- Revocar cualquier intento de mutación directa en tablas financieras por parte del móvil
REVOKE INSERT, UPDATE, DELETE ON gasto FROM anon, authenticated;
REVOKE INSERT, UPDATE, DELETE ON fuga FROM anon, authenticated;
REVOKE INSERT, UPDATE, DELETE ON fuga_evidencia FROM anon, authenticated;

-- Prohibir la escalación de privilegios modificando rol o estado de habilitación directamente
REVOKE UPDATE (rol, disabled_at) ON perfil FROM anon, authenticated;

-- Permitir lectura de catálogos a usuarios autenticados
GRANT SELECT ON categoria, regla_fuga, regla_fuga_version TO authenticated;
