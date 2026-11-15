# BLOQUEOS — FUGA+

Registro de bloqueos activos y resueltos. Un bloqueo resuelto **no se borra**; se marca con `RESUELTO` y fecha.

---

## Bloqueos activos

### H1 — Proyecto Supabase no creado
- **Fase afectada:** F1 (y en cascada F2–F4, F6–F8, F13)
- **Descripción:** No existe un proyecto en Supabase con las credenciales necesarias para aplicar las migraciones y configurar Auth.
- **Qué falta (§19.1):** Crear cuenta/organización en supabase.com; crear proyecto `fuga-plus-dev`; copiar `Project URL`, `anon key`, `service_role key` y `Database password` a `backend/.env.local`.
- **Impacto:** F1 no puede cerrarse. F5 y partes de F9 pueden avanzar sin Supabase.
- **Responsable:** Propietaria del proyecto.
- **Detectado:** 2026-11-15

### H2 — Supabase Auth no configurado
- **Fase afectada:** F3
- **Descripción:** No se ha habilitado el proveedor de email, ni configurado SMTP, ni las redirect URLs.
- **Qué falta (§19.3):** Authentication → Email provider activo; `Site URL` y `Redirect URLs` en el panel; confirmar si se requiere SMTP propio.
- **Impacto:** Sin registro ni login real. F3 bloqueada.
- **Responsable:** Propietaria.
- **Detectado:** 2026-11-15

### H3 — JDK 17/21 y Android SDK ausentes
- **Fase afectada:** F14
- **Descripción:** Solo existe JDK 23 en la máquina. React Native/AGP requieren JDK 17 o 21. `ANDROID_HOME` vacío.
- **Qué falta (§19.7):** Instalar JDK 21 (Temurin recomendado); instalar Android SDK (Platform 34/35 + Build-Tools via Android Studio o command-line tools); fijar `JAVA_HOME` y `ANDROID_HOME`.
- **Impacto:** F14 parcialmente bloqueada. F0–F13 no se ven afectadas.
- **Responsable:** Propietaria.
- **Detectado:** 2026-11-15

### H4 — Dispositivo o emulador Android no disponible
- **Fase afectada:** F14
- **Descripción:** No hay dispositivo físico conectado con depuración USB ni emulador configurado.
- **Qué falta (§19.10):** Dispositivo Android con `adb devices` visible, o AVD en Android Studio.
- **Impacto:** Sin prueba de aceptación en hardware.
- **Responsable:** Propietaria.
- **Detectado:** 2026-11-15

### H5 — Proveedor de hosting del backend no elegido
- **Fase afectada:** F14 (demostración)
- **Descripción:** C-07 aprobó diseño portable sin proveedor definitivo. No se ha elegido dónde desplegar el backend para la demo.
- **Qué falta (§19.9):** Elegir proveedor (Render, Railway, Fly.io u otro); configurar HTTPS; apuntar `EXPO_PUBLIC_API_URL` a la URL de producción.
- **Impacto:** Demo solo en red local. El diseño ya es portable; no afecta F0–F13.
- **Responsable:** Propietaria.
- **Detectado:** 2026-11-15

### SANDBOX — Sin red en el sandbox del agente
- **Fase afectada:** F0 (parcial)
- **Descripción:** El sandbox de ejecución no tiene acceso a internet; `npx create-expo-app`, `pip index` y similares fallan.
- **Impacto:** No se pudo confirmar la versión actual de Expo SDK con `create-expo-app@latest`. Las versiones en `mobile/docs/versiones.md` son las conocidas estables; deben confirmarse con red real.
- **Acción requerida:** Ejecutar manualmente en tu terminal con red: `npx create-expo-app@latest --version` y actualizar `mobile/docs/versiones.md`.
- **Detectado:** 2026-11-15

---

## Bloqueos resueltos

*(ninguno aún)*
