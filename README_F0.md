# FUGA+ - F0 Base Completado

## Estructura creada

- `backend/` - FastAPI backend con estructura base
- `mobile/` - React Native + TypeScript con Expo
- `mi-framework-ia/` - Conservado intacto (no modificado)
- `assets/` - Logo y paleta de colores existentes

## Backend (F0)
- FastAPI app con health check endpoint: `GET /health`
- Estructura preparada para auth con sesiones en MongoDB
- Variables de entorno en `.env.example`
- Requirements.txt con dependencias necesarias
- Implementación de auth seguirá D-09: JWT access 15min, refresh 7 días con rotación

## Mobile (F0)
- React Native + TypeScript con Expo
- Tema centralizado en `src/theme/tokens.ts` con paleta aprobada (Brand & Style)
  - Primary: #1A5B5A, Secondary: #A2E8D3, Warning/Fugas: #F5A623
  - Background: #F5F8F7, Surfaces: #FFFFFF
  - Text: #243332, #607270
  - Borders: #E2ECE9
- Plus Jakarta Sans (configurar en fuentes)
- Logo en `assets/logo.png` (a copiar si necesario)
- Navegación base preparada

## Próximos pasos
- F1: Autenticación segura con sesiones en MongoDB, rotación de refresh tokens, validación por solicitud
- Ejecutar pruebas de seguridad D-09 antes de pasar a F2
- Seguir orden: Must Have primero, luego Should/Could si hay tiempo
- HU-28, HU-29 excluidas
- D-06, D-16 pendientes

## Notas
- Sin tocar `mi-framework-ia/`
- Sin credenciales reales en repo
- Paleta técnica original preservada en `assets/paleta_de_colores.md` con discrepancia documentada
