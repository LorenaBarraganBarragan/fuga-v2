import React from 'react';
import { Image, Platform, Pressable, ScrollView, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { colors, ErrorText } from './ui';
import { PublicSafeArea } from './PublicSafeArea';

// Existing complementary backgrounds from ui.tsx and Dashboard.tsx, scoped to this screen.
const mint = '#D8F6EC';
const soft = '#EEF5F3';
const white = '#fff';

type IconName = 'voice' | 'chart' | 'pattern' | 'lock';
function Icon({ name }: { name: IconName }) {
  return <View style={s.icon} accessible={false} accessibilityElementsHidden importantForAccessibility="no-hide-descendants">
    {name === 'voice' ? <>
      <View style={s.microphone} /><View style={s.microphoneArc} />
      <View style={s.microphoneStem} /><View style={s.microphoneBase} />
    </> : name === 'chart' ? <View style={s.iconBars}>
      {[8, 15, 21].map(height => <View key={height} style={[s.iconBar, { height }]} />)}
    </View> : name === 'pattern' ? <>
      <View style={s.lens}><View style={s.lensDot} /></View><View style={s.lensHandle} />
    </> : <><View style={s.lockArc} /><View style={s.lockBody}><View style={s.lockDot} /></View></>}
  </View>;
}

function ExampleCard() {
  return <View style={s.example}>
    <View style={s.exampleHeader}>
      <Text style={s.exampleTitle}>Así se ve tu mes</Text>
      <View style={s.exampleBadge}><Text style={s.exampleBadgeText}>Ejemplo ficticio</Text></View>
    </View>
    <View style={s.exampleSummary}>
      <View style={s.totalGroup}>
        <Text style={s.exampleCaption}>Total de gastos · COP</Text>
        <Text style={s.total}>$75.000</Text>
        <Text style={s.exampleCaption}>6 gastos de ejemplo</Text>
      </View>
      <View style={s.chart} accessible={false} accessibilityElementsHidden importantForAccessibility="no-hide-descendants">
        {[8, 8, 8, 8, 24, 64].map((height, index) => <View key={index} style={[s.chartBar, { height, backgroundColor: index === 5 ? colors.tertiary : colors.secondary }]} />)}
      </View>
    </View>
    <View style={s.patternCard}>
      <View style={s.patternHeading}>
        <View style={s.patternIcon}><Icon name="pattern" /></View>
        <View style={s.patternCopy}>
          <Text style={s.patternTitle}>Una posible fuga</Text>
          <Text style={s.patternDetail}>Café · 4 veces · $5.000 cada uno</Text>
        </View>
      </View>
      <View style={s.patternFooter}>
        <Text style={s.patternAmount}>$20.000 <Text style={s.currency}>COP</Text></Text>
        <View style={s.reviewBadge}><Text style={s.reviewText}>Para revisar</Text></View>
      </View>
    </View>
  </View>;
}

function Action({ title, primary = false, onPress }: { title: string; primary?: boolean; onPress: () => void }) {
  return <Pressable
    accessibilityRole="button"
    accessibilityLabel={title}
    accessibilityHint={primary ? 'Abre el formulario de registro' : 'Abre el formulario de inicio de sesión'}
    onPress={onPress}
    style={({ pressed }) => [s.action, primary ? s.primaryAction : s.secondaryAction, pressed && s.pressed]}
  >
    <Text style={[s.actionText, primary && s.primaryActionText]}>{title}</Text>
    <View style={[s.arrow, primary && s.primaryArrow]} accessible={false} importantForAccessibility="no" />
  </Pressable>;
}

export function Welcome({ onCreateAccount, onLogin, error = '' }: {
  onCreateAccount: () => void;
  onLogin: () => void;
  error?: string;
}) {
  const { width, fontScale } = useWindowDimensions();
  const stacked = width < 360 || fontScale > 1.2;
  return <PublicSafeArea>
    <ScrollView style={s.scroll} contentContainerStyle={[s.scrollContent, { paddingTop: 16, paddingBottom: Platform.OS === 'android' ? 16 : 36 }]} keyboardShouldPersistTaps="handled">
    <View style={[s.content, width < 360 && s.narrowContent]}>
      <View style={s.brand}>
        <Image source={require('../../assets/branding/logo.png')} style={s.logo} accessibilityLabel="Logo FUGA+" />
        <Text style={s.brandName}>FUGA+</Text>
        <View style={s.brandNote}><View style={s.brandDot} /><Text style={s.brandNoteText}>Cada gasto cuenta</Text></View>
      </View>

      <View style={s.hero}>
        <Text style={s.eyebrow}>TU DINERO, MÁS CLARO</Text>
        <Text accessibilityRole="header" style={s.headline}>Descubre a dónde se va tu dinero</Text>
        <Text style={s.intro}>Pon tus gastos en palabras. Encuentra esos pequeños hábitos que suman.</Text>
      </View>

      <ExampleCard />

      <View style={s.actions}>
        <Action title="Crear cuenta" primary onPress={onCreateAccount} />
        <Action title="Iniciar sesión" onPress={onLogin} />
      </View>
      <ErrorText message={error} />

      <View style={[s.benefits, stacked && s.stackedBenefits]}>
        {([
          ['voice', 'Voz o texto', 'Registra a tu manera'],
          ['chart', 'Tus gastos', 'Visualiza lo que gastas'],
          ['pattern', 'Posibles fugas', 'Detecta lo que se repite'],
        ] as const).map(([icon, title, description]) => <View key={icon} style={[s.benefit, stacked && s.stackedBenefit]}>
          <View style={s.benefitIcon}><Icon name={icon} /></View>
          <View style={[s.benefitCopy, !stacked && s.centeredCopy]}>
            <Text style={[s.benefitTitle, !stacked && s.centeredText]}>{title}</Text>
            <Text style={[s.benefitDescription, !stacked && s.centeredText]}>{description}</Text>
          </View>
        </View>)}
      </View>

      <View style={s.privacy}>
        <View style={s.privacyIcon}><Icon name="lock" /></View>
        <View style={s.privacyCopy}>
          <Text style={s.privacyTitle}>Tus gastos son privados. Tú confirmas qué guardar.</Text>
          <Text style={s.privacyText}>Análisis con reglas automáticas, sin IA generativa ni envío de tus gastos a una IA externa.</Text>
        </View>
      </View>
    </View>
    </ScrollView>
  </PublicSafeArea>;
}

const s = StyleSheet.create({
  scroll: { flex: 1, backgroundColor: colors.bg },
  scrollContent: { flexGrow: 1 },
  content: { width: '100%', maxWidth: 480, alignSelf: 'center', paddingHorizontal: 24, gap: 18 },
  narrowContent: { paddingHorizontal: 20 },
  brand: { flexDirection: 'row', alignItems: 'center', gap: 10, flexWrap: 'wrap' },
  logo: { width: 44, height: 44, borderRadius: 14 },
  brandName: { fontFamily: 'PlusJakartaSans_700Bold', fontSize: 25, lineHeight: 34, color: colors.primary },
  brandNote: { marginLeft: 'auto', flexDirection: 'row', alignItems: 'center', gap: 6 },
  brandDot: { width: 7, height: 7, borderRadius: 4, backgroundColor: colors.tertiary },
  brandNoteText: { color: colors.muted, fontSize: 12, lineHeight: 18 },
  hero: { gap: 10 },
  eyebrow: { color: colors.primary, fontSize: 11, lineHeight: 16, fontWeight: '700', letterSpacing: 1.5 },
  headline: { color: colors.primary, fontFamily: 'PlusJakartaSans_700Bold', fontSize: 32, lineHeight: 40, letterSpacing: -0.8 },
  intro: { fontFamily: 'PlusJakartaSans_400Regular', color: colors.muted, fontSize: 15, lineHeight: 23 },
  example: { padding: 16, gap: 14, borderRadius: 26, backgroundColor: colors.primary, shadowColor: colors.primary, shadowOffset: { width: 0, height: 8 }, shadowOpacity: 0.12, shadowRadius: 16, elevation: 3 },
  exampleHeader: { flexDirection: 'row', alignItems: 'center', flexWrap: 'wrap', gap: 8, justifyContent: 'space-between' },
  exampleTitle: { color: white, fontSize: 14, lineHeight: 21, fontWeight: '600' },
  exampleBadge: { backgroundColor: colors.tertiary, paddingHorizontal: 9, paddingVertical: 4, borderRadius: 20 },
  exampleBadgeText: { color: colors.text, fontSize: 11, lineHeight: 17, fontWeight: '700' },
  exampleSummary: { flexDirection: 'row', alignItems: 'flex-end', flexWrap: 'wrap', gap: 14, justifyContent: 'space-between' },
  totalGroup: { gap: 2 },
  exampleCaption: { color: colors.secondary, fontSize: 12, lineHeight: 18 },
  total: { color: white, fontFamily: 'PlusJakartaSans_700Bold', fontSize: 32, lineHeight: 42, letterSpacing: -0.6 },
  chart: { height: 64, flexDirection: 'row', alignItems: 'flex-end', gap: 5, paddingBottom: 2 },
  chartBar: { width: 9, borderRadius: 4 },
  patternCard: { padding: 13, borderRadius: 18, backgroundColor: white, gap: 10 },
  patternHeading: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  patternIcon: { width: 36, height: 36, backgroundColor: mint, borderRadius: 12, alignItems: 'center', justifyContent: 'center' },
  patternCopy: { flex: 1, gap: 3 },
  patternTitle: { fontSize: 13, lineHeight: 20, color: colors.primary, fontWeight: '700' },
  patternDetail: { fontSize: 12, lineHeight: 18, color: colors.muted },
  patternFooter: { flexDirection: 'row', alignItems: 'center', flexWrap: 'wrap', gap: 8, justifyContent: 'space-between' },
  patternAmount: { fontSize: 21, lineHeight: 28, fontFamily: 'PlusJakartaSans_700Bold', color: colors.primary },
  currency: { fontSize: 11, color: colors.muted },
  reviewBadge: { borderRadius: 12, paddingVertical: 4, paddingHorizontal: 8, backgroundColor: soft },
  reviewText: { fontSize: 11, lineHeight: 17, fontWeight: '600', color: colors.primary },
  actions: { gap: 10 },
  action: { minHeight: 52, paddingVertical: 15, paddingHorizontal: 20, borderRadius: 16, borderWidth: 1.5, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 14 },
  primaryAction: { backgroundColor: colors.primary, borderColor: colors.primary },
  secondaryAction: { backgroundColor: white, borderColor: colors.border },
  pressed: { opacity: 0.75 },
  actionText: { fontFamily: 'PlusJakartaSans_700Bold', fontSize: 15, lineHeight: 22, color: colors.primary, flexShrink: 1 },
  primaryActionText: { color: white },
  arrow: { width: 7, height: 7, borderTopWidth: 1.5, borderRightWidth: 1.5, borderColor: colors.primary, transform: [{ rotate: '45deg' }] },
  primaryArrow: { borderColor: colors.secondary },
  benefits: { flexDirection: 'row', gap: 10 },
  stackedBenefits: { flexDirection: 'column' },
  benefit: { flex: 1, alignItems: 'center', gap: 9 },
  stackedBenefit: { flexDirection: 'row', alignItems: 'center', gap: 14 },
  benefitIcon: { width: 42, height: 42, borderRadius: 14, backgroundColor: mint, alignItems: 'center', justifyContent: 'center' },
  benefitCopy: { flex: 1, gap: 3 },
  centeredCopy: { flex: 0, alignSelf: 'stretch' },
  centeredText: { textAlign: 'center' },
  benefitTitle: { fontSize: 13, lineHeight: 20, fontWeight: '700', color: colors.primary },
  benefitDescription: { fontSize: 12, lineHeight: 18, color: colors.muted },
  privacy: { flexDirection: 'row', gap: 10, paddingTop: 18, borderTopWidth: 1, borderColor: colors.border },
  privacyIcon: { paddingTop: 2 },
  privacyCopy: { flex: 1, gap: 5 },
  privacyTitle: { color: colors.text, fontSize: 12, lineHeight: 19, fontWeight: '600' },
  privacyText: { color: colors.muted, fontSize: 12, lineHeight: 19 },
  icon: { width: 24, height: 24 },
  microphone: { position: 'absolute', top: 1, left: 9, width: 7, height: 13, borderRadius: 5, borderWidth: 1.8, borderColor: colors.primary },
  microphoneArc: { position: 'absolute', left: 5, top: 8, width: 15, height: 11, borderWidth: 1.8, borderTopWidth: 0, borderBottomLeftRadius: 8, borderBottomRightRadius: 8, borderColor: colors.primary },
  microphoneStem: { position: 'absolute', width: 2, height: 4, left: 11.5, top: 18, backgroundColor: colors.primary },
  microphoneBase: { position: 'absolute', width: 10, height: 1.8, left: 7.5, top: 22, backgroundColor: colors.primary, borderRadius: 1 },
  iconBars: { flex: 1, flexDirection: 'row', alignItems: 'flex-end', justifyContent: 'center', gap: 3, paddingBottom: 2 },
  iconBar: { width: 4, borderRadius: 2, backgroundColor: colors.primary },
  lens: { width: 17, height: 17, top: 1, left: 1, borderRadius: 9, borderWidth: 1.8, borderColor: colors.primary, alignItems: 'center', justifyContent: 'center' },
  lensDot: { width: 5, height: 5, borderRadius: 3, backgroundColor: colors.tertiary },
  lensHandle: { position: 'absolute', width: 9, height: 1.8, left: 14, top: 19, backgroundColor: colors.primary, transform: [{ rotate: '45deg' }] },
  lockArc: { position: 'absolute', left: 7, top: 1, width: 11, height: 12, borderRadius: 7, borderWidth: 1.8, borderColor: colors.primary },
  lockBody: { position: 'absolute', left: 4, top: 9, width: 17, height: 13, borderRadius: 4, backgroundColor: colors.bg, borderWidth: 1.8, borderColor: colors.primary, alignItems: 'center', justifyContent: 'center' },
  lockDot: { width: 2, height: 4, borderRadius: 1, backgroundColor: colors.primary },
});
