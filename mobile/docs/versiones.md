# Versiones verificadas ? FUGA+ m?vil
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
