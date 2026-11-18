const {test}=require('node:test');
const assert=require('node:assert/strict');
const path=require('node:path');
const {createHash}=require('node:crypto');
const {loadComponent}=require('./component-loader.cjs');
const file=name=>path.resolve(__dirname,'../src',name);

function adapter(platform='android',blocked=false){
 const sent=[],channels=[],stored=new Map();let permissionCalls=0;
 const module=loadComponent('src/lib/notifications.ts',{
  'react-native':{Platform:{OS:platform}},
  'expo-secure-store':{getItemAsync:async key=>stored.get(key)||null,setItemAsync:async(key,value)=>stored.set(key,value)},
  'expo-crypto':{CryptoDigestAlgorithm:{SHA256:'SHA256'},digestStringAsync:async(_,value)=>createHash('sha256').update(value).digest('hex')},
  'expo-notifications':{
   AndroidImportance:{DEFAULT:5,NONE:2},
   requestPermissionsAsync:async()=>{permissionCalls++;return {granted:true};},
   getPermissionsAsync:async()=>({granted:true}),
   setNotificationChannelAsync:async(id,config)=>channels.push({id,config}),
   getNotificationChannelAsync:async()=>({importance:blocked?2:5}),
   scheduleNotificationAsync:async request=>sent.push(request),
  },
  [file('lib/supabase')]:{supabase:{auth:{getSession:async()=>({data:{session:{user:{id:'local-user'}}}})}}},
  [file('lib/validation')]:{mayNotify:()=>true},
 });
 return {module,sent,channels,permissionCalls:()=>permissionCalls};
}
const leak={id:'local-leak',categoria_nombre:'Alimentación',descripcion_normalizada:'cafe',regla_version:'1.0'};

test('real notification adapter is unavailable on Web without requesting native permission',async()=>{
 const current=adapter('web');
 assert.equal(await current.module.enableNotifications(),false);
 assert.equal(await current.module.notifyCandidate(leak),'skipped');
 assert.equal(current.permissionCalls(),0);assert.equal(current.sent.length,0);
});
test('real Android adapter respects a blocked patterns channel',async()=>{
 const current=adapter('android',true);
 assert.equal(await current.module.enableNotifications(),false);
 assert.equal(await current.module.notifyCandidate(leak),'skipped');
 assert.equal(current.sent.length,0);
});
test('real Android adapter selects patterns and sends a generic deduplicated local notification',async()=>{
 const current=adapter();
 assert.equal(await current.module.enableNotifications(),true);
 await Promise.all([current.module.notifyCandidate(leak),current.module.notifyCandidate(leak)]);
 assert.equal(current.sent.length,1);
 assert.deepEqual(current.sent[0].trigger,{channelId:'patterns'});
 assert.deepEqual(current.sent[0].content.data,{fuga_id:'local-leak',user_id:'local-user'});
 assert.equal(current.sent[0].content.body,'FUGA+ encontró un patrón de gastos para revisar');
 assert.ok(current.channels.every(channel=>channel.id==='patterns'));
});
