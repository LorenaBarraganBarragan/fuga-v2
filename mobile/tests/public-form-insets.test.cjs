const {test}=require('node:test');
const assert=require('node:assert/strict');
const path=require('node:path');
const {calculatePublicInsets}=require('../src/lib/publicInsets.ts');
const {React,TestRenderer,loadComponent}=require('./component-loader.cjs');
const {act,create}=TestRenderer;
const file=name=>path.resolve(__dirname,'../src',name);
const metrics=changes=>({systemTop:32,systemBottom:24,systemLeft:0,systemRight:0,imeBottom:0,keyboardVisible:false,frameTop:0,frameLeft:0,viewportWidth:393,viewportHeight:851,windowWidth:393,windowHeight:851,...changes});

for(const [name,changes,expected] of [
 ['gesture navigation',{}, {top:32,bottom:24,left:0,right:0}],
 ['three-button navigation',{systemBottom:48},{top:32,bottom:48,left:0,right:0}],
 ['cutout and side bars',{systemTop:68,systemLeft:22,systemRight:12},{top:68,bottom:24,left:22,right:12}],
 ['parent already inset',{frameTop:32,viewportHeight:795},{top:0,bottom:0,left:0,right:0}],
 ['keyboard overlay',{keyboardVisible:true,imeBottom:320},{top:32,bottom:320,left:0,right:0}],
 ['adjustResize already removed keyboard',{keyboardVisible:true,imeBottom:320,viewportHeight:531},{top:32,bottom:0,left:0,right:0}],
 ['partial resize',{keyboardVisible:true,imeBottom:320,viewportHeight:600},{top:32,bottom:69,left:0,right:0}],
 ['hidden keyboard with stale size',{imeBottom:320},{top:32,bottom:24,left:0,right:0}],
 ['no system bars',{systemTop:0,systemBottom:0},{top:0,bottom:0,left:0,right:0}],
])test('public frame uses measured '+name,()=>{
 const result=calculatePublicInsets(metrics(changes));
 for(const key of ['top','bottom','left','right'])assert.equal(result[key],expected[key]);
 assert.equal(result.ready,true);
});

test('missing, nonfinite and startup dimensions are not mistaken for measured zero insets',()=>{
 for(const value of [undefined,{},metrics({viewportHeight:0}),metrics({systemTop:-1}),metrics({imeBottom:NaN}),metrics({windowHeight:Infinity}),metrics({systemLeft:undefined})])assert.equal(calculatePublicInsets(value),null);
});

function access(){
 const calls=[],scrollCalls=[];
 const status=Object.assign(()=>null,{setBarStyle(){}});
 const native={Platform:{OS:'android'},StatusBar:status,useWindowDimensions:()=>({width:393,height:851,fontScale:1,scale:3})};
 const {Access}=loadComponent('src/screens/Access.tsx',{
  '../../assets/branding/logo.png':1,'react-native':native,'expo-web-browser':{},
  [file('auth/AuthProvider')]:{useAuth:()=>({error:''})},
  [file('lib/supabase')]:{authConfigured:true,supabase:{auth:new Proxy({},{get:()=>()=>{calls.push('Auth');throw new Error('No Auth expected');}})}},
  [file('auth/links')]:{exchangeAuthUrl:async()=>{},getAuthRedirectUrl:()=>''},
  [file('components/WindowInsetsProbe')]:{WindowInsetsProbe:props=>React.createElement('InsetsProbe',props)},
 });
 const node={scrollToEnd:options=>scrollCalls.push({end:options}),scrollResponderScrollNativeHandleToKeyboard:(...args)=>scrollCalls.push({focus:args})};
 return {Access,calls,scrollCalls,node};
}
function raf(t){
 const previous=globalThis.requestAnimationFrame,previousCancel=globalThis.cancelAnimationFrame;
 globalThis.requestAnimationFrame=callback=>{callback(0);return 1;};globalThis.cancelAnimationFrame=()=>{};
 t.after(()=>{if(previous)globalThis.requestAnimationFrame=previous;else delete globalThis.requestAnimationFrame;if(previousCancel)globalThis.cancelAnimationFrame=previousCancel;else delete globalThis.cancelAnimationFrame;});
}
const button=(renderer,title)=>renderer.root.findAllByType('Pressable').find(n=>n.props.accessibilityLabel===title);
async function mount(mode){
 const state=access();let renderer;
 await act(async()=>{renderer=create(React.createElement(state.Access),{createNodeMock:e=>e.type==='ScrollView'?state.node:null});});
 await act(async()=>button(renderer,mode).props.onPress());
 await act(async()=>renderer.root.findByType('InsetsProbe').props.onInsetsChange({nativeEvent:metrics()}));
 return {...state,renderer};
}

test('register keeps focused fields reachable for overlay and resized keyboard without Auth',async t=>{
 raf(t);const state=await mount('Crear cuenta'),{renderer}=state;
 const scroll=()=>renderer.root.findByType('ScrollView');
 assert.equal(scroll().props.keyboardShouldPersistTaps,'handled');
 assert.equal(scroll().props.keyboardDismissMode,'on-drag');
 await act(async()=>scroll().props.onFocus({nativeEvent:{target:123}}));
 await act(async()=>renderer.root.findByType('InsetsProbe').props.onInsetsChange({nativeEvent:metrics({keyboardVisible:true,imeBottom:320})}));
 assert.deepEqual(state.scrollCalls.at(-1).focus,[123,16,true]);
 await act(async()=>scroll().props.onFocus({nativeEvent:{target:456}}));
 assert.deepEqual(state.scrollCalls.at(-1).focus,[456,16,true]);
 await act(async()=>renderer.root.findByType('InsetsProbe').props.onInsetsChange({nativeEvent:metrics({keyboardVisible:true,imeBottom:320,viewportHeight:531})}));
 const frame=renderer.root.findAllByType('View').find(n=>Array.isArray(n.props.style)&&n.props.style[1]?.paddingBottom!==undefined);
 assert.equal(frame.props.style[1].paddingBottom,0);
 assert.equal(state.calls.length,0);
 await act(async()=>renderer.unmount());
});

for(const [mode,submit] of [['Crear cuenta','Registrarse'],['Iniciar sesión','Iniciar sesión']])test(mode+' reveals local validation feedback without contacting Auth',async t=>{
 raf(t);const state=await mount(mode),{renderer}=state;
 await act(async()=>button(renderer,submit).props.onPress());
 assert.match(JSON.stringify(renderer.toJSON()),/Correo: escribe una dirección válida/);
 assert.ok(state.scrollCalls.some(c=>c.end?.animated));
 assert.equal(state.calls.length,0);
 assert.ok(button(renderer,'Volver al inicio'));
 await act(async()=>renderer.unmount());
});
