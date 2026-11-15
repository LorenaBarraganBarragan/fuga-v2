# Versiones congeladas — FUGA+ Mobile

**Generado en:** F0 · 2026-11-15  
**Regla:** No actualizar sin ejecutar una fase de regresión. Toda versión aquí es la fuente de verdad para `package.json`.

## Entorno del host (verificado en F0)

| Herramienta | Versión | Notas |
|---|---|---|
| Node.js | 24.16.0 | Compatible con Expo SDK ≥ 54 |
| npm | 11.13.0 | — |
| Python | 3.12.6 | Backend (ver `backend/pyproject.toml`) |
| Java | JDK 23 (en PATH actual) | ⚠ **No usar para Gradle**. Instalar JDK 21 (Temurin) y fijar `JAVA_HOME` antes de F14 |
| Android SDK | **AUSENTE** | Bloqueo H3 — instalación manual requerida antes de F14 |

## Versiones del SDK de Expo (a confirmar/ajustar en F0 con `npx create-expo-app@latest`)

> **Nota:** estas versiones se fijaron con base en Expo SDK 53 estable (última versión estable
> verificable sin red). Al ejecutar `npx create-expo-app@latest` con red disponible, actualizar
> esta tabla con la salida exacta de `npx expo install --check`.

| Paquete | Versión fijada | Justificación |
|---|---|---|
| `expo` | `~53.0.0` | SDK estable ≥ 54 cuando esté disponible; usar el que instale `create-expo-app@latest` |
| `react-native` | La que fije Expo SDK | No fijar independientemente |
| `react` | La que fije Expo SDK | — |
| `typescript` | `^5.3.3` | Modo estricto |
| `expo-router` | `~4.0.0` | Compatible con SDK 53 |
| `@tanstack/react-query` | `^5.17.19` | — |
| `zustand` | `^4.5.0` | — |
| `react-hook-form` | `^7.49.3` | — |
| `zod` | `^3.22.4` | — |
| `@supabase/supabase-js` | `^2.39.3` | Auth oficial |
| `expo-secure-store` | `~13.0.0` | Compatible con SDK 53 |
| `expo-font` | `~12.0.0` | — |
| `@expo-google-fonts/plus-jakarta-sans` | `^0.2.3` | Tipografía oficial |
| `expo-image` | `~1.12.0` | — |
| `jest-expo` | `~53.0.0` | Pruebas de componentes |
| `@testing-library/react-native` | `^12.4.3` | — |
| `eslint-config-expo` | `^7.0.0` | — |
| `prettier` | `^3.2.4` | — |

## Logo oficial

| Aspecto | Valor |
|---|---|
| Ruta original | `assets/logo/logo.png` |
| Ruta en mobile | `mobile/assets/branding/logo.png` |
| SHA-256 original | `FB396C3BA320B18FEC97FC059B4AB1998A92AFFEFB826DCA62DBFB31885A35B2` |
| SHA-256 copia | `FB396C3BA320B18FEC97FC059B4AB1998A92AFFEFB826DCA62DBFB31885A35B2` |
| Verificado en | F0 · 2026-11-15 |
| Dimensiones | 500 × 500 px · RGBA |

## Registro de actualizaciones

| Fecha | Fase | Cambio |
|---|---|---|
| 2026-11-15 | F0 | Versiones iniciales congeladas; logo verificado |
