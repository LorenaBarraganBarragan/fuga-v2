const {test}=require('node:test');
const assert=require('node:assert/strict');
const path=require('node:path');
const {React,TestRenderer,loadComponent}=require('./component-loader.cjs');
const {act,create}=TestRenderer;
const file=name=>path.resolve(__dirname,'../src',name);
const categories=[{id:'category-a',nombre:'Alimentación',orden:1}];
const date=()=> '2026-11-18';
const nextTurn=()=>new Promise(resolve=>setImmediate(resolve));
const button=(renderer,title)=>renderer.root.findAllByType('Pressable').find(node=>node.props.accessibilityLabel===title);

test('real ExpenseForm rejects invalid amount and emits only an explicitly confirmed payload',async()=>{
 const confirmed=[];
 const {ExpenseForm}=loadComponent('src/components/ExpenseForm.tsx',{[file('lib/api')]:{localDate:date}});
 let renderer;
 await act(async()=>{renderer=create(React.createElement(ExpenseForm,{categories,initial:{monto_cop:0,descripcion:'cafe',fecha_gasto:date(),categoria_id:'category-a'},busy:false,onSubmit:body=>confirmed.push(body)}));});
 await act(async()=>button(renderer,'Confirmar y guardar gasto').props.onPress());
 assert.equal(confirmed.length,0);
 assert.match(JSON.stringify(renderer.toJSON()),/entero entre/);
 const amount=renderer.root.findAllByType('TextInput').find(node=>node.props.accessibilityLabel.startsWith('Monto'));
 await act(async()=>amount.props.onChangeText('5000'));
 assert.equal(confirmed.length,0);
 await act(async()=>button(renderer,'Confirmar y guardar gasto').props.onPress());
 assert.equal(confirmed.length,1);assert.equal(confirmed[0].monto_cop,5000);
 await act(async()=>renderer.unmount());
});

function newExpense(api){
 let key=0;
 return loadComponent('src/screens/NewExpense.tsx',{
  [file('lib/api')]:{api,localDate:date,money:n=>String(n)},
  [file('auth/AuthProvider')]:{useAuth:()=>({session:{user:{id:'user-a'}}})},
  [file('voice/VoiceInput')]:{VoiceInput:()=>null},
  'expo-crypto':{randomUUID:()=>`local-key-${++key}`},
 });
}
const draft={draft:{monto_cop:5000,descripcion:'cafe',fecha_gasto:date(),categoria_id:'category-a',moneda:'COP'},avisos:[],ambiguedades:[],diccionario_version:'1.1',reglas_version:'1.1'};
test('real NewExpense does not save its draft and preserves UUID after a lost confirmation response',async()=>{
 const posts=[];let renderer;
 const {NewExpense}=newExpense(async(route,options)=>{
  if(route==='/categories')return categories;
  if(route==='/expenses/interpret')return draft;
  posts.push(options);if(posts.length===1)throw new Error('Respuesta perdida de prueba');
  return {id:'saved-local',descripcion:'cafe',monto_cop:5000};
 });
 await act(async()=>{renderer=create(React.createElement(NewExpense,{onDirty:()=>{}}));await nextTurn();});
 await act(async()=>renderer.root.findAllByType('TextInput')[0].props.onChangeText('Gasté 5000 en cafe'));
 await act(async()=>{button(renderer,'Procesar con IA').props.onPress();await nextTurn();});
 assert.equal(posts.length,0);
 await act(async()=>{button(renderer,'Confirmar y guardar gasto').props.onPress();await nextTurn();});
 assert.equal(posts.length,1);
 await act(async()=>{button(renderer,'Confirmar y guardar gasto').props.onPress();await nextTurn();});
 assert.equal(posts.length,2);assert.equal(posts[0].key,posts[1].key);
 assert.match(JSON.stringify(renderer.toJSON()),/Gasto guardado/);
 await act(async()=>renderer.unmount());
});
test('real NewExpense discards a draft without a financial POST',async()=>{
 let writes=0,renderer;const dirty=[];
 const {NewExpense}=newExpense(async route=>{if(route==='/categories')return categories;if(route==='/expenses/interpret')return draft;writes++;});
 await act(async()=>{renderer=create(React.createElement(NewExpense,{onDirty:value=>dirty.push(value)}));await nextTurn();});
 await act(async()=>renderer.root.findAllByType('TextInput')[0].props.onChangeText('Gasté 5000 en cafe'));
 await act(async()=>{button(renderer,'Procesar con IA').props.onPress();await nextTurn();});
 await act(async()=>button(renderer,'Descartar borrador').props.onPress());
 const dialog=renderer.root.findAllByType('Modal').find(node=>node.props.visible);
 await act(async()=>dialog.findAllByType('Pressable').find(node=>node.props.accessibilityLabel==='Confirmar').props.onPress());
 assert.equal(writes,0);assert.equal(dirty.at(-1),false);
 assert.equal(renderer.root.findAllByType('TextInput')[0].props.value,'');
 await act(async()=>renderer.unmount());
});
test('real AuthProvider never exposes the previous profile during an account switch',async()=>{
 let session={user:{id:'user-a'}},listener,renderer;
 let release;
 const sessions=[];
 const sdk={auth:{onAuthStateChange:callback=>{listener=callback;return {data:{subscription:{unsubscribe(){}}}};},getSession:async()=>({data:{session}}),signOut:async()=>({})}};
 const auth=loadComponent('src/auth/AuthProvider.tsx',{
  [file('lib/supabase')]:{supabase:sdk,authConfigured:true},
  [file('lib/api')]:{api:async()=>session.user.id==='user-a'?{id:'user-a',rol:'usuario'}:new Promise(resolve=>release=()=>resolve({id:'user-b',rol:'usuario'})),accountDenied:()=>{},accountSessionChanged:id=>sessions.push(id)},
  [file('auth/links')]:{exchangeAuthUrl:async()=>false},
  'expo-web-browser':{maybeCompleteAuthSession(){}},
  'react-native':{Linking:{getInitialURL:async()=>null,addEventListener:()=>({remove(){}})}},
 });
 function Probe(){const state=auth.useAuth();return React.createElement('Probe',{user:state.session?.user.id,profile:state.profile?.id});}
 await act(async()=>{renderer=create(React.createElement(auth.AuthProvider,null,React.createElement(Probe)));await nextTurn();});
 assert.equal(renderer.root.findByType('Probe').props.profile,'user-a');
 await act(async()=>{session={user:{id:'user-b'}};listener('SIGNED_IN',session);await nextTurn();});
 assert.equal(renderer.root.findByType('Probe').props.user,'user-b');
 assert.equal(renderer.root.findByType('Probe').props.profile,undefined);
 await act(async()=>{release();await nextTurn();});
 assert.equal(renderer.root.findByType('Probe').props.profile,'user-b');
 assert.ok(sessions.includes('user-b'));
 await act(async()=>renderer.unmount());
});

test('real History shows a loading failure and can recover without any mutation',async()=>{
 let fail=true,renderer;const calls=[];
 const {History}=loadComponent('src/screens/History.tsx',{
  [file('lib/api')]:{money:String,api:async(route,options)=>{
   calls.push({route,options});if(route==='/categories')return categories;
   if(fail)throw new Error('No fue posible conectar con el servidor.');
   return {items:[{id:'local-expense',descripcion:'buseta',monto_cop:3000,fecha_gasto:date(),categoria_nombre:'Transporte'}],next_cursor:null,has_more:false};
  }},
 });
 await act(async()=>{renderer=create(React.createElement(History,{onDirty:()=>{}}));await nextTurn();});
 assert.match(JSON.stringify(renderer.toJSON()),/No fue posible conectar/);
 fail=false;
 await act(async()=>{button(renderer,'Actualizar').props.onPress();await nextTurn();});
 assert.match(JSON.stringify(renderer.toJSON()),/buseta/);
 assert.doesNotMatch(JSON.stringify(renderer.toJSON()),/No fue posible conectar/);
 assert.ok(calls.every(call=>!call.options?.method));
 await act(async()=>renderer.unmount());
});

test('real Dashboard requests comparison only on demand and uses the displayed period',async()=>{
 const calls=[];let renderer;
 const summary={periodo:'2026-11',monto_total_cop:20000,cantidad_gastos:4,promedio_gasto_cop:5000};
 const {Dashboard}=loadComponent('src/screens/Dashboard.tsx',{
  [file('lib/api')]:{money:String,localDate:date,api:async route=>{
   calls.push(route);
   if(route.includes('/summary'))return summary;
   if(route.includes('/by-category'))return {items:[],categorias_mayor_gasto:[]};
   return {actual:summary,anterior:null,diferencia_cop:null,variacion_porcentaje:null,mensaje:null};
  }},
 });
 await act(async()=>{renderer=create(React.createElement(Dashboard));await nextTurn();});
 assert.equal(calls.length,2);assert.ok(calls.every(route=>!route.includes('comparison')));
 await act(async()=>renderer.root.findAllByType('TextInput')[0].props.onChangeText('2027-01'));
 await act(async()=>{button(renderer,'Comparar con el mes anterior').props.onPress();await nextTurn();});
 assert.equal(calls.at(-1),'/analytics/comparison?periodo=2026-11');
 assert.match(JSON.stringify(renderer.toJSON()),/Sin base de comparación/);
 await act(async()=>renderer.unmount());
});
