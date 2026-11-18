const {test}=require('node:test');
const assert=require('node:assert/strict');
const {createApiClient}=require('../src/lib/request.ts');
const {createExpenseAttempt}=require('../src/lib/expenseAttempt.ts');

function setup(fetch, overrides={}) {
 let generation=0;
 const status=[];
 const deps={base:()=> 'https://api.example.test',session:async()=>({user:{id:'user-a'},access_token:'local-token'}),generation:()=>generation,denied:()=>{},fetch,status:(...x)=>status.push(x),readTimeout:15,writeTimeout:15,retryDelay:0,waitNotice:2,...overrides};
 return {...createApiClient(deps),status,changeSession:()=>generation++};
}
const ok=value=>new Response(JSON.stringify(value),{status:200,headers:{'Content-Type':'application/json'}});
test('read wakes a slow server, reports waiting and retries only twice',async()=>{
 let calls=0;
 const client=setup(async(_url,{signal})=>{
  calls++;
  if(calls===1)return new Promise((_,reject)=>signal.addEventListener('abort',()=>reject(new Error('timeout')),{once:true}));
  return ok({total:20000});
 });
 assert.deepEqual(await client.request('/leaks'),{total:20000});
 assert.equal(calls,2);
 assert.ok(client.status.some(([,status])=>status==='waiting'));
 assert.ok(client.status.some(([,status])=>status==='retrying'));
 assert.equal(client.status.at(-1)[1],null);
});
test('read retries a temporary 503 and keeps the endpoint contract',async()=>{
 const urls=[];
 const client=setup(async url=>{urls.push(url);return urls.length===1?new Response('',{status:503}):ok({items:[]});});
 assert.deepEqual(await client.request('/expenses?limit=20'),{items:[]});
 assert.deepEqual(urls,['https://api.example.test/api/v1/expenses?limit=20','https://api.example.test/api/v1/expenses?limit=20']);
});
test('network failure exposes a generic message and stops after two reads',async()=>{
 let calls=0;
 const client=setup(async()=>{calls++;throw new Error('private-provider-context');});
 await assert.rejects(client.request('/expenses'),error=>!error.message.includes('private-provider')&&/conectar/.test(error.message));
 assert.equal(calls,2);
});
test('401 is never retried and invalidates the current session once',async()=>{
 let calls=0,denied=0;
 const client=setup(async()=>{calls++;return new Response(JSON.stringify({error:{code:'UNAUTHENTICATED',message:'Inicia sesión.'}}),{status:401});},{denied:()=>denied++});
 await assert.rejects(client.request('/me'),error=>error.status===401);
 assert.equal(calls,1);assert.equal(denied,1);
});
test('session changes discard a late financial response',async()=>{
 let release;
 const client=setup(()=>new Promise(resolve=>release=resolve));
 const result=client.request('/expenses');
 await new Promise(resolve=>setImmediate(resolve));
 client.changeSession();release(ok({items:['must-not-be-displayed']}));
 await assert.rejects(result,error=>error.code==='SESSION_CHANGED');
});
test('cancel stops an active read without retry',async()=>{
 let calls=0;
 const client=setup(async(_url,{signal})=>{calls++;return new Promise((_,reject)=>signal.addEventListener('abort',()=>reject(new Error('aborted')),{once:true}));});
 const result=client.request('/leaks');
 await new Promise(resolve=>setImmediate(resolve));
 client.cancelReads();
 await assert.rejects(result,error=>error.code==='CANCELLED');assert.equal(calls,1);
});
test('external cancellation is respected before sending any request',async()=>{
 let calls=0;
 const client=setup(async()=>{calls++;return ok({});});
 const controller=new AbortController();controller.abort();
 await assert.rejects(client.request('/expenses',{signal:controller.signal}),error=>error.code==='CANCELLED');
 assert.equal(calls,0);
});
test('lost POST response is retried manually with the same key, not automatically',async()=>{
 const keys=[];let uuids=0;
 const attempt=createExpenseAttempt(()=>`attempt-${++uuids}`);
 const body={monto_cop:5000,descripcion:'cafe'};
 const client=setup(async(_url,options)=>{keys.push(options.headers['Idempotency-Key']);if(keys.length===1)throw new Error('response lost');return ok({id:'same-expense'});});
 await assert.rejects(client.request('/expenses',{method:'POST',body,key:attempt.prepare('user-a',body)}));
 assert.equal(keys.length,1);
 assert.deepEqual(await client.request('/expenses',{method:'POST',body,key:attempt.prepare('user-a',body)}),{id:'same-expense'});
 assert.equal(keys[0],keys[1]);assert.equal(uuids,1);
});
test('PUT and DELETE failures are never replayed automatically',async()=>{
 for(const method of ['PUT','DELETE']){
  let calls=0;const client=setup(async()=>{calls++;throw new Error('offline');});
  await assert.rejects(client.request('/expenses/local-id',{method}));assert.equal(calls,1);
 }
});
test('expense attempts isolate owner, edited payload and discarded drafts',()=>{
 let count=0;const attempt=createExpenseAttempt(()=>String(++count));
 const a=attempt.prepare('a',{monto_cop:5000,descripcion:'cafe'});
 assert.equal(a,attempt.prepare('a',{descripcion:'cafe',monto_cop:5000}));
 assert.notEqual(a,attempt.prepare('a',{monto_cop:6000,descripcion:'cafe'}));
 const b=attempt.prepare('b',{monto_cop:5000,descripcion:'cafe'});assert.notEqual(a,b);
 attempt.clear();assert.notEqual(b,attempt.prepare('b',{monto_cop:5000,descripcion:'cafe'}));
});
