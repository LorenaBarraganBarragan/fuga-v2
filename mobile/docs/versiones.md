# Versiones verificadas — FUGA+ móvil

## Estado vigente del plan — 2026-11-18

Node 24.16.0, npm 11.13.0, Expo 58.0.25, React Native 0.88.1 y React 19.3.0.
Compilación Android comprobada con JDK 17.0.21, Gradle 9.4.1, compileSdk 37,
targetSdk 36, minSdk 24, build-tools 37.0.0, NDK 27.1.12297006, CMake 3.22.1
y Ninja 1.13.2. Kotlin efectivo 2.2.10; el catálogo declara 2.2.0 y Gradle informa
que utiliza la versión del plugin, sin una modificación manual de esas versiones.

Debug y release compilados e instalados en Android API 36 arm64. Bienvenida release
comprobada tras arranque nuevo con Metro apagado. No se cargaron .env.local en el APK
de QA; flujos autenticados, dictado y avisos físicos siguen pendientes. Expo Web exportó.
83 pruebas frontend y TypeScript aprobados. Los resultados completos y límites están
en [el informe del plan](../../mi-framework-ia/docs/auditoria/ejecucion-plan-mejora-fugaplus.md)
y el procedimiento en [Android local](ANDROID_LOCAL.md).

## Registro histórico anterior al plan
Fecha: 2026-11-15, America/Bogota.
Fuente reproducible: package.json y package-lock.json. No son versiones propuestas.

El bootstrap anterior mencionaba SDK 53/54 sin aplicaci?n instalada. Durante esta implementaci?n
se instalaron y probaron Expo 58 y sus versiones compatibles para corregir vulnerabilidades del ?rbol anterior.
Se conserva React Native/TypeScript y el resto de decisiones funcionales 3.0.
El override de Expo evita SDKs anidados distintos; minimatch se actualiz? para corregir su aviso de seguridad.

| Paquete | Rango declarado | Instalado |
|---|---|---|
| @expo-google-fonts/plus-jakarta-sans | ^0.4.2 | 0.4.2 |
| @supabase/supabase-js | ^2.99.0 | 2.119.0 |
| expo | ~58.0.25 | 58.0.25 |
| expo-crypto | ~58.0.8 | 58.0.8 |
| expo-font | ~58.0.12 | 58.0.12 |
| expo-image-picker | ~58.0.10 | 58.0.10 |
| expo-notifications | ~58.1.9 | 58.1.9 |
| expo-secure-store | ~58.0.3 | 58.0.3 |
| expo-web-browser | ~58.0.8 | 58.0.8 |
| react | 19.3.0 | 19.3.0 |
| react-dom | 19.3.0 | 19.3.0 |
| react-native | 0.88.1 | 0.88.1 |
| react-native-url-polyfill | ^2.0.0 | 2.0.0 |
| react-native-web | ~0.21.4 | 0.21.4 |
| @types/react | ~19.3.0 | 19.3.0 |
| typescript | ~6.0.3 | 6.0.3 |

Node usado: 24.16.0. Se ejecutaron TypeScript, pruebas de reglas y exportaci?n JS para web/Android/iOS.
La generaci?n de bundles NO demuestra compilaci?n Kotlin, APK/IPA ni funcionamiento en dispositivos.
El autolinking detecta FugaVoiceModule. Android SDK/JDK compatible y macOS/Xcode siguen siendo necesarios.
El logo original permanece sin modificaciones en assets/logo/logo.png y su copia en mobile/assets/branding/logo.png.
