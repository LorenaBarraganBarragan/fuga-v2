/**
 * FUGA+ Design Tokens
 * Approved palette from Stitch Brand & Style (assets/paleta_de_colores.md)
 * Primary: #1A5B5A, Secondary: #A2E8D3, Warning/Fugas: #F5A623
 * Note: Original technical values preserved in source file; this uses approved Brand & Style
 */

export const colors = {
  // Brand colors
  primary: '#1A5B5A',
  secondary: '#A2E8D3',
  warning: '#F5A623',
  warningFugas: '#F5A623',
  
  // Surfaces
  background: '#F5F8F7',
  surface: '#FFFFFF',
  surfaceElevated: '#FFFFFF',
  
  // Text
  textPrimary: '#243332',
  textSecondary: '#607270',
  textOnPrimary: '#FFFFFF',
  textOnSecondary: '#1A5B5A',
  textOnWarning: '#FFFFFF',
  
  // Borders
  border: '#E2ECE9',
  borderFocus: '#1A5B5A',
  
  // States
  error: '#BA1A1A',
  success: '#216959',
  disabled: '#BFC8C7',
} as const;

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
} as const;

export const borderRadius = {
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  full: 9999,
} as const;

export const typography = {
  fontFamily: 'Plus Jakarta Sans',
  sizes: {
    displayLg: 32,
    displayMd: 26,
    headlineLg: 22,
    headlineMd: 18,
    bodyLg: 16,
    bodyMd: 14,
    bodySm: 12,
    labelLg: 15,
    labelMd: 13,
    labelSm: 11,
  },
  weights: {
    regular: '400' as const,
    semibold: '600' as const,
    bold: '700' as const,
    extrabold: '800' as const,
  },
} as const;

export const touchTarget = {
  minHeight: 48,
  minHeightLarge: 52,
} as const;
