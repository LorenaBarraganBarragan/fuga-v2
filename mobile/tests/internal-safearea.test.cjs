const {test}=require('node:test');
const assert=require('node:assert/strict');
const path=require('node:path');
const {React,TestRenderer,loadComponent}=require('./component-loader.cjs');
const {act,create}=TestRenderer;
const file=name=>path.resolve(__dirname,'../src',name);
const metrics=changes=>({systemTop:46,systemBottom:16,systemLeft:0,systemRight:0,imeBottom:0,keyboardVisible:false,frameTop:0,frameLeft:0,viewportWidth:393,viewportHeight:851,windowWidth:393,windowHeight:851,...changes});

function app(authChanges={}){
 const status=Object.assign(()=>null,{setBarStyle(){}});
 const auth={loading:false,session:{user:{id:'fictional-qa'}},profile:{id:'fictional-qa',rol:'usuario'},...authChanges};
 const screens=['Dashboard','NewExpense','History','Leaks','Profile','Admin'];
 const overrides={
  './assets/branding/logo.png':1,
  'react-native':{Platform:{OS:'android'},StatusBar:status,SafeAreaView:'SafeAreaView',BackHandler:{addEventListener:()=>({remove(){}})}},
  '@expo-google-fonts/plus-jakarta-sans':{useFonts:()=>[true]},
  'expo-notifications':{addNotificationResponseReceivedListener:()=>({remove(){}}),getLastNotificationResponseAsync:async()=>null},
  [file('auth/AuthProvider')]:{AuthProvider:({children})=>children,useAuth:()=>auth},
  [file('lib/api')]:{subscribeApiWaiting:()=>()=>{},cancelPendingReads(){}},
  [file('screens/Access')]:{Access:()=>React.createElement('PublicAccess'),ResetPassword:()=>React.createElement('PublicRecovery')},
  [file('components/WindowInsetsProbe')]:{WindowInsetsProbe:props=>React.createElement('InsetsProbe',props)},
 };
 for(const name of screens)overrides[file('screens/'+name)]={[name]:()=>React.createElement('Screen',{name})};
 return loadComponent('App.tsx',overrides).default;
}
const frame=renderer=>renderer.root.findAllByType('View').find(n=>Array.isArray(n.props.style)&&n.props.style[1]?.paddingBottom!==undefined);
const tabs=renderer=>renderer.root.findAllByType('Pressable').filter(n=>typeof n.props.accessibilityState?.selected==='boolean');
async function mount(changes){let renderer;await act(async()=>{renderer=create(React.createElement(app(changes)));});return renderer;}
async function measure(renderer,changes){await act(async()=>renderer.root.findByType('InsetsProbe').props.onInsetsChange({nativeEvent:metrics(changes)}));}

test('all authenticated tabs share one measured frame around header, screen and footer',async()=>{
 const renderer=await mount();
 assert.equal(frame(renderer).props.pointerEvents,'none');
 await measure(renderer);
 assert.equal(renderer.root.findAllByType('InsetsProbe').length,1);
 assert.equal(frame(renderer).props.style[1].paddingTop,46);
 assert.equal(frame(renderer).props.style[1].paddingBottom,16);
 assert.equal(frame(renderer).props.pointerEvents,'auto');
 for(const [index,name] of ['Dashboard','NewExpense','History','Leaks','Profile'].entries()){
  await act(async()=>tabs(renderer)[index].props.onPress());
  const safe=frame(renderer);
  assert.equal(safe.findByType('Screen').props.name,name);
  assert.equal(safe.findAllByType('Image').length,1,'shared logo is inside safe frame');
  assert.equal(safe.findAllByType('Pressable').filter(n=>typeof n.props.accessibilityState?.selected==='boolean').length,5);
  assert.equal(tabs(renderer)[index].props.accessibilityState.selected,true);
  assert.equal(renderer.root.findAllByType('InsetsProbe').length,1);
 }
 await act(async()=>renderer.unmount());
});

test('keyboard overlap and Android resize are handled once for authenticated content and tabs',async()=>{
 const renderer=await mount();
 await measure(renderer,{keyboardVisible:true,imeBottom:320});
 assert.equal(frame(renderer).props.style[1].paddingBottom,320);
 assert.equal(frame(renderer).findAllByType('Screen').length,1);
 assert.equal(frame(renderer).findAllByType('Pressable').filter(n=>typeof n.props.accessibilityState?.selected==='boolean').length,5);
 await measure(renderer,{keyboardVisible:true,imeBottom:320,viewportHeight:531});
 assert.equal(frame(renderer).props.style[1].paddingBottom,0,'OS resize already excluded the IME');
 await measure(renderer,{frameTop:46,viewportHeight:789});
 assert.equal(frame(renderer).props.style[1].paddingTop,0);
 assert.equal(frame(renderer).props.style[1].paddingBottom,0,'an inset parent does not add a second safe area');
 await measure(renderer);
 assert.equal(frame(renderer).props.style[1].paddingBottom,16);
 await act(async()=>renderer.unmount());
});

test('administrative tabs use the same frame without changing role navigation',async()=>{
 const renderer=await mount({profile:{id:'fictional-admin',rol:'administrador'}});
 await measure(renderer);
 assert.equal(frame(renderer).findByType('Screen').props.name,'Admin');
 assert.equal(tabs(renderer).length,2);
 await act(async()=>tabs(renderer)[1].props.onPress());
 assert.equal(frame(renderer).findByType('Screen').props.name,'Profile');
 assert.equal(renderer.root.findAllByType('InsetsProbe').length,1);
 await act(async()=>renderer.unmount());
});

test('public access and recovery are not wrapped in a second authenticated safe area',async()=>{
 for(const [changes,screen] of [[{session:null,profile:null},'PublicAccess'],[{recovery:true},'PublicRecovery']]){
  const renderer=await mount(changes);
  assert.equal(renderer.root.findAllByType(screen).length,1);
  assert.equal(renderer.root.findAllByType('InsetsProbe').length,0);
  await act(async()=>renderer.unmount());
 }
});
