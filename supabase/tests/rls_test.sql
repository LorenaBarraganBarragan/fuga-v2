-- rls_test.sql — Verificación de políticas RLS y aislamiento (RF-033, F1)
-- Ejecutar en Supabase SQL Editor o psql simulando identidades

BEGIN;

-- 1. Verificar catálogo sembrado
SELECT count(*) AS total_categorias FROM categoria;
-- Esperado: 9

SELECT count(*) AS total_reglas FROM regla_fuga WHERE codigo = 'FUGA-01';
-- Esperado: 1

SELECT count(*) AS total_regla_versiones FROM regla_fuga_version WHERE version = '1.0';
-- Esperado: 1

-- 2. Simulación de usuario autenticado
-- SET LOCAL ROLE authenticated;
-- SET LOCAL "request.jwt.claims" = '{"sub": "11111111-1111-1111-1111-111111111111", "role": "authenticated"}';

-- (a) Lectura directa de gastos por el cliente debe retornar 0 filas
-- SELECT count(*) FROM gasto;
-- Esperado: 0

-- (b) Lectura de perfil ajeno no debe retornar filas
-- SELECT * FROM perfil WHERE id = '22222222-2222-2222-2222-222222222222';
-- Esperado: 0 filas

-- (c) Intento de escalar rol debe fallar por permiso
-- UPDATE perfil SET rol = 'administrador' WHERE id = '11111111-1111-1111-1111-111111111111';
-- Esperado: ERROR de permisos por REVOKE UPDATE (rol)

ROLLBACK;
