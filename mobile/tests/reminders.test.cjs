const {test}=require('node:test');
const assert=require('node:assert/strict');
const {createHash}=require('node:crypto');
const {createReminderDispatcher}=require('../src/lib/reminders.ts');
const {mayNotify}=require('../src/lib/validation.ts');
const leak={id:'snapshot-a',categoria_nombre:'Alimentación',descripcion_normalizada:'cafe',regla_version:'1.0'};
function setup(overrides={}) {
 const memory=new Map(),sent=[];
 let user='user-a',now=new Date('2026-11-18T17:00:00Z');
 const notify=createReminderDispatcher({supported:()=>true,permission:async()=>true,user:async()=>user,digest:async x=>createHash('sha256').update(x).digest('hex'),last:async key=>memory.get(key)||null,save:async(key,value)=>{memory.set(key,value);},allowed:mayNotify,now:()=>now,deliver:async(...args)=>{sent.push(args);},...overrides});
 return {notify,memory,sent,user:value=>user=value,now:value=>now=new Date(value)};
}
test('concurrent requests for one concept deliver only once and persist cooldown',async()=>{
 const state=setup();await Promise.all(Array.from({length:8},()=>state.notify(leak)));
 assert.equal(state.sent.length,1);assert.equal(state.memory.size,1);
 await state.notify({...leak,id:'a-new-snapshot'});assert.equal(state.sent.length,1);
});
test('different users, categories, concepts and rule versions have separate cooldowns',async()=>{
 const state=setup();await state.notify(leak);
 await state.notify({...leak,categoria_nombre:'Otros'});
 await state.notify({...leak,descripcion_normalizada:'cafe con leche'});
 await state.notify({...leak,regla_version:'future-test'});
 state.user('user-b');await state.notify(leak);assert.equal(state.sent.length,5);
});
test('web and permission denial never deliver or write cooldown',async()=>{
 for(const overrides of [{supported:()=>false},{permission:async()=>false}]){
  const state=setup(overrides);assert.equal(await state.notify(leak),'skipped');assert.equal(state.sent.length,0);assert.equal(state.memory.size,0);
 }
});
test('night is skipped and exactly seven days permits another reminder',async()=>{
 const state=setup();state.now('2026-11-19T02:00:00Z');assert.equal(await state.notify(leak),'skipped');
 state.now('2026-11-19T13:00:00Z');await state.notify(leak);
 state.now('2026-11-26T12:59:59Z');assert.equal(await state.notify(leak),'skipped');
 state.now('2026-11-26T13:00:00Z');await state.notify(leak);assert.equal(state.sent.length,2);
});
test('delivery failure is generic, does not consume cooldown, and releases the lock',async()=>{
 let attempts=0;const state=setup({deliver:async()=>{if(++attempts===1)throw new Error('secret-provider-details');}});
 await assert.rejects(state.notify(leak),error=>!error.message.includes('secret-provider-details'));
 assert.equal(state.memory.size,0);assert.equal(await state.notify(leak),'sent');
});
test('session switch during asynchronous checks suppresses delivery',async()=>{
 let reads=0;const state=setup({user:async()=>++reads===1?'user-a':'user-b'});
 assert.equal(await state.notify(leak),'skipped');assert.equal(state.sent.length,0);
});
test('crossing 21:00 during preparation does not deliver outside quiet hours',async()=>{
 let calls=0;const state=setup({now:()=>new Date(++calls===1?'2026-11-19T01:59:59Z':'2026-11-19T02:00:00Z')});
 assert.equal(await state.notify(leak),'skipped');assert.equal(state.sent.length,0);
});
