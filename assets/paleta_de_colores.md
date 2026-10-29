---
name: Petrol Mint Vitality
colors:
  surface: '#ecfdfb'
  surface-dim: '#cddddc'
  surface-bright: '#ecfdfb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#e6f7f5'
  surface-container: '#e0f1ef'
  surface-container-high: '#dbecea'
  surface-container-highest: '#d5e6e4'
  on-surface: '#0f1e1d'
  on-surface-variant: '#3f4848'
  inverse-surface: '#243332'
  inverse-on-surface: '#e3f4f2'
  outline: '#707978'
  outline-variant: '#bfc8c7'
  surface-tint: '#2a6866'
  primary: '#004342'
  on-primary: '#ffffff'
  primary-container: '#1a5b5a'
  on-primary-container: '#94d1cf'
  inverse-primary: '#95d1d0'
  secondary: '#216959'
  on-secondary: '#ffffff'
  secondary-container: '#a7eed8'
  on-secondary-container: '#276e5d'
  tertiary: '#533400'
  on-tertiary: '#ffffff'
  tertiary-container: '#724900'
  on-tertiary-container: '#ffb74e'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#b0eeec'
  primary-fixed-dim: '#95d1d0'
  on-primary-fixed: '#00201f'
  on-primary-fixed-variant: '#064f4e'
  secondary-fixed: '#aaf0db'
  secondary-fixed-dim: '#8fd4c0'
  on-secondary-fixed: '#002019'
  on-secondary-fixed-variant: '#005142'
  tertiary-fixed: '#ffddb4'
  tertiary-fixed-dim: '#ffb955'
  on-tertiary-fixed: '#291800'
  on-tertiary-fixed-variant: '#633f00'
  background: '#ecfdfb'
  on-background: '#0f1e1d'
  surface-variant: '#d5e6e4'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '800'
    lineHeight: 40px
    letterSpacing: -0.02em
  display-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 26px
    fontWeight: '700'
    lineHeight: 34px
    letterSpacing: -0.015em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 22px
    fontWeight: '700'
    lineHeight: 28px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 15px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 13px
    fontWeight: '600'
    lineHeight: 18px
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 14px
    letterSpacing: 0.04em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  gutter: 1rem
  margin: 1.25rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system embodies an energetic, friendly, and empowering financial companion designed for Android mobile devices. Geared toward university students and young adults navigating personal budgeting for the first time, it demystifies everyday micro-expenses ("gastos hormiga") without judgment or clinical formality.

The aesthetic blends **Modern Tactile FinTech** with **Soft Neomorphism-infused minimalism**:
- **Approachable Confidence:** Large, tactile surfaces, welcoming curves, and reassuring solid hues eliminate financial anxiety.
- **Micro-Leak Awareness:** Strategic splashes of vibrant amber provide visual cues for financial leaks, contrasting against fresh mint and deep petrol green.
- **Ergonomics First:** Generous touch targets (48–52px minimum height), smooth rounded corners (`rounded-2xl` to `rounded-3xl`), and spacious thumb-driven layouts tailored for one-handed mobile interactions.

## Colors

The palette balances authoritative financial grounding with youthful freshness and high-visibility alerts:

- **Primary (`#1A5B5A` - Verde Petróleo):** Anchors high-priority actions, app bar headers, prominent icons, and core CTA buttons. Conveys stability and trust without feeling bureaucratic.
- **Secondary (`#A2E8D3` - Verde Menta):** Provides lightness and fresh breathing room. Used for interactive pill badges, highlight card backgrounds, success states, and progress indicators.
- **Tertiary / Accent (`#F5A623` - Ámbar Cálido):** The focal alarm token representing money leaks ("fugas"), pending alerts, streak counters, and actionable budget callouts.
- **Neutral Dark (`#243332` - Dark Slate Teal):** Primary typography and high-emphasis icons ensuring WCAG AAA legibility against light backgrounds.
- **Neutral Muted (`#607270` - Medium Teal Gray):** Secondary text, timestamps, helper descriptions, and unselected tab icons.
- **Surface Canvas (`#F5F8F7` - Light Sage Gray):** Default app background, soft on the eyes and warmer than raw white.
- **Surface Elevated (`#FFFFFF` - Pure White):** Clean containment for cards, input containers, bottom navigation sheets, and modal dialogs.
- **Border Stroke (`#E2ECE9` - Subtle Mint Gray):** Crisp, unobtrusive boundaries defining cards and inputs.

## Typography

The typography system relies exclusively on **Plus Jakarta Sans** for its friendly geometry, modern proportions, and legibility at tiny sizes on mobile screens.

- **Numeric & Metric Display:** Balance figures and financial leak amounts utilize `display-lg` and `display-md` with extra-bold weights (`800`) to highlight monetary figures instantly.
- **Clear Information Density:** `body-md` (14px) serves as the primary reading size for transactions, category tags, and notifications, retaining clarity on varied Android DPI densities.
- **Uppercase Labels:** `label-sm` is reserved for micro-badges (e.g., "FUGA DETECTADA", "HOY") using bold weight and slight positive letter-spacing (`0.04em`) to maintain sharp readability.

## Layout & Spacing

Built for vertical mobile ergonomics:

- **Grid & Margins:** A fluid 4-column layout on mobile with an outer margin of `1.25rem` (20px) to keep critical controls comfortably away from phone bezel edges and gesture bars.
- **Rhythm & Touch Bounds:**
  - Component padding utilizes `space-md` (16px) internally for cards and bottom navigation.
  - Interactive touch elements maintain strict minimum tap bounds of 48px to 52px height.
  - Section headers sit `space-lg` (24px) apart to allow distinct modular scanning.
- **Android Safe Zones:** Bottom navigation items and floating action triggers feature an automatic `safe-area-inset-bottom` buffer combined with `space-md` spacing to prevent accidental home-indicator swipes.

## Elevation & Depth

Visual hierarchy uses a refined combination of clean white surfaces, tonal borders, and tinted soft shadows:

- **Level 0 (Flat Canvas):** `#F5F8F7` provides a calming canvas where un-elevated elements integrate smoothly.
- **Level 1 (Card & ListItem Elevation):** Pure `#FFFFFF` background bound by a 1px solid `#E2ECE9` outline and a soft, low-contrast ambient shadow: `box-shadow: 0 4px 16px -2px rgba(26, 91, 90, 0.06);`.
- **Level 2 (Modals & Bottom Sheets):** Floating dialogs and bottom sheets feature deeper diffusion: `box-shadow: 0 12px 32px -4px rgba(26, 91, 90, 0.12);`.
- **Accent Glow (Fuga Alert Highlights):** Warning cards highlighting spending leaks use a warm, subtle tint: `box-shadow: 0 4px 20px -2px rgba(245, 166, 35, 0.18);`.

## Shapes

The interface embraces organic, playful curved geometry:

- **Standard Cards & Modals (`rounded-2xl` / 16–20px):** Containers, list grouped items, and modal sheets use pronounced soft corners.
- **Pills & Interactive Action Items (`rounded-full` / 9999px):** Primary buttons, filter chips, category icons, and badges feature full pill geometry for immediate tactile affordance.
- **App Launcher / Waterdrop Motif:** Key illustrations and avatar backdrops mirror the organic teardrop and circular geometry derived from the app's droplet identity.

## Components

### Buttons
- **Primary Action (CTA):** Height of 48–52px. Full pill curvature (`rounded-full`). Background `#1A5B5A` (Verde Petróleo) with pure white text (`#FFFFFF`) in `label-lg` font. Subtle active state press depression (`scale(0.98)`).
- **Secondary / Soft Button:** Height 48px, background `#A2E8D3` (Verde Menta) with `#1A5B5A` dark teal text for secondary workflows like "Ver desglose".
- **Leak Warning Button:** Height 48px, background `#F5A623` (Ámbar) with `#FFFFFF` text for immediate leak interventions ("Frenar fuga").

### Cards & Financial Tiles
- **Standard Transaction Card:** White `#FFFFFF` background, 16px padding, `rounded-2xl` (16px), 1px border `#E2ECE9`. Contains category icon (44x44px rounded circle in mint or amber), bold transaction title in `#243332`, and numeric spending value.
- **Fuga Highlight Card:** Special gradient/accent card with `#F5A623` left accent bar (4px) or soft amber tinted background (`rgba(245, 166, 35, 0.08)`) to flag micro-leaks immediately.

### Chips & Filter Pills
- Compact 32–36px height, `rounded-full` border radius.
- **Active State:** `#1A5B5A` fill with `#FFFFFF` text.
- **Inactive State:** `#FFFFFF` fill, `#E2ECE9` border, `#607270` text.

### Text Inputs
- 52px height containers with `#FFFFFF` fill and 1.5px border `#E2ECE9`. Corner radius `rounded-xl` (12–16px).
- Placeholder text in `#607270`.
- Focus state activates a 2px stroke in `#1A5B5A` with a soft mint drop shadow ring (`rgba(162, 232, 211, 0.4)`).

### Badges & Leak Trackers
- Pill format with 6px vertical padding and 12px horizontal padding.
- `label-sm` font.
- Mint variant: background `#A2E8D3` with `#1A5B5A` text.
- Amber leak variant: background `#F5A623` with `#FFFFFF` text.