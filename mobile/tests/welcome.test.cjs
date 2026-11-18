const {test}=require('node:test');
const assert=require('node:assert/strict');
const path=require('node:path');
const {React,TestRenderer,loadComponent}=require('./component-loader.cjs');
const {act,create}=TestRenderer;
const file=name=>path.resolve(__dirname,'../src',name);
const button=(renderer,title)=>renderer.root.findAllByType('Pressable').find(n=>n.props.accessibilityLabel===title);
const StatusBar=Object.assign(()=>null,{currentHeight:24,setBarStyle:()=>{}});
const native={Platform:{OS:'android'},StatusBar,TurboModuleRegistry:{get:()=>({getConstants:()=>({HEIGHT:32})})},useWindowDimensions:()=>({width:393,height:850,fontScale:1,scale:3})};
const asset={'../../assets/branding/logo.png':1};

test('welcome buttons retain the existing registration/login/recovery routes without calling Auth',async()=>{
 let calls=0,renderer;
 const auth=new Proxy({},{get:()=>()=>{calls++;throw new Error('Auth must not run during public navigation');}});
 const {Access}=loadComponent('src/screens/Access.tsx',{
  ...asset,'react-native':native,'expo-web-browser':{},
  [file('auth/AuthProvider')]:{useAuth:()=>({error:''})},
  [file('lib/supabase')]:{supabase:{auth},authConfigured:true},
  [file('auth/links')]:{exchangeAuthUrl:async()=>{},getAuthRedirectUrl:()=>''},
 });
 await act(async()=>{renderer=create(React.createElement(Access));});
 assert.match(JSON.stringify(renderer.toJSON()),/Descubre a dónde se va tu dinero/);
 await act(async()=>button(renderer,'Crear cuenta').props.onPress());
 assert.ok(renderer.root.findAllByType('TextInput').some(n=>n.props.accessibilityLabel==='Confirmar contraseña'));
 await act(async()=>button(renderer,'Volver al inicio').props.onPress());
 await act(async()=>button(renderer,'Iniciar sesión').props.onPress());
 assert.ok(button(renderer,'Olvidé mi contraseña'));
 await act(async()=>button(renderer,'Olvidé mi contraseña').props.onPress());
 assert.ok(button(renderer,'Enviar enlace'));
 await act(async()=>button(renderer,'Volver al inicio').props.onPress());
 assert.ok(button(renderer,'Crear cuenta'));assert.equal(calls,0);
 await act(async()=>renderer.unmount());
});

test('narrow Android with large text retains readable demo, benefits and both accessible actions',async()=>{
 let created=0,logged=0,renderer;
 const {Welcome}=loadComponent('src/components/Welcome.tsx',{
  ...asset,'react-native':{...native,useWindowDimensions:()=>({width:320,height:640,fontScale:2,scale:3})},
 });
 await act(async()=>{renderer=create(React.createElement(Welcome,{onCreateAccount:()=>created++,onLogin:()=>logged++}));});
 const content=JSON.stringify(renderer.toJSON());
 for(const text of ['Ejemplo ficticio','Voz o texto','Tus gastos','Posibles fugas','sin IA generativa'])assert.ok(content.includes(text));
 assert.ok(renderer.root.findAllByType('Text').every(n=>n.props.allowFontScaling!==false&&!n.props.numberOfLines));
 assert.ok(renderer.root.findAllByType('ScrollView').length===1);
 await act(async()=>button(renderer,'Crear cuenta').props.onPress());
 await act(async()=>button(renderer,'Iniciar sesión').props.onPress());
 assert.equal(created,1);assert.equal(logged,1);
 assert.equal(renderer.root.findAllByType('TextInput').length,0);
 await act(async()=>renderer.unmount());
});

test('visual preview cannot inherit real Auth, backend or private configuration',()=>{
 const {prepareWelcomePreviewEnvironment}=require('../scripts/welcome-preview.cjs');
 const result=prepareWelcomePreviewEnvironment({PATH:'tools',EXPO_PUBLIC_SUPABASE_URL:'https://real.example.test',EXPO_PUBLIC_SUPABASE_ANON_KEY:'real-public-key',DATABASE_URL:'private-server',CLOUDINARY_API_SECRET:'private-server',SUPABASE_SERVICE_ROLE_KEY:'private-server'});
 assert.equal(result.EXPO_PUBLIC_SUPABASE_URL,'https://welcome-preview.example.invalid');
 assert.equal(result.EXPO_PUBLIC_API_URL,'http://127.0.0.1:18888');
 assert.equal(result.EXPO_NO_DOTENV,'1');
 for(const key of ['DATABASE_URL','CLOUDINARY_API_SECRET','SUPABASE_SERVICE_ROLE_KEY'])assert.equal(result[key],undefined);
});

test('Android waits for real insets rather than reserving a model-specific fixed margin',async()=>{
 let renderer,barStyle;
 const {Welcome}=loadComponent('src/components/Welcome.tsx',{
  ...asset,'react-native':{...native,StatusBar:Object.assign(()=>null,{currentHeight:0,setBarStyle:value=>{barStyle=value;}})},
  [file('components/WindowInsetsProbe')]:{WindowInsetsProbe:props=>React.createElement('InsetsProbe',props)},
 });
 await act(async()=>{renderer=create(React.createElement(Welcome,{onCreateAccount(){},onLogin(){}}));});
 const root=()=>renderer.root.findAllByType('View')[0];
 const frame=()=>renderer.root.findAllByType('View').find(n=>Array.isArray(n.props.style)&&n.props.style[1]?.paddingTop!==undefined);
 assert.equal(frame().props.style[1].opacity,0);
 await act(async()=>root().props.onLayout({nativeEvent:{layout:{width:393,height:850}}}));
 await act(async()=>renderer.root.findByType('InsetsProbe').props.onInsetsChange({nativeEvent:{systemTop:56,systemBottom:28,systemLeft:0,systemRight:0,imeBottom:0,keyboardVisible:false,frameTop:0,frameLeft:0,viewportWidth:393,viewportHeight:850,windowWidth:393,windowHeight:850}}));
 assert.equal(frame().props.style[1].paddingTop,56);
 assert.equal(barStyle,'dark-content');
 assert.equal(frame().props.style[1].paddingBottom,28);
 assert.equal(frame().props.style[1].opacity,1);
 await act(async()=>renderer.unmount());
});
