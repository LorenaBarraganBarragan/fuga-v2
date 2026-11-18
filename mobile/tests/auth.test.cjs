const {test}=require('node:test');
const assert=require('node:assert/strict');
const {createHash}=require('node:crypto');
const {createClient}=require('@supabase/supabase-js');
const {
 AUTH_LINK_ERROR,authRedirectUrl,createAuthCallbackHandler,cleanCallbackTarget,createWebAuthStorage,
}=require('../src/auth/callback.ts');

const web={platform:'web',origin:'http://localhost:8081'};
const native={platform:'native'};
const success={error:null,data:{session:{},redirectType:null}};

test('web registration and recovery use the current origin callback',()=>{
 assert.equal(authRedirectUrl(web),'http://localhost:8081/auth/callback');
 assert.equal(authRedirectUrl(web,true),'http://localhost:8081/auth/callback?flow=recovery');
 assert.equal(authRedirectUrl({platform:'web',origin:'https://app.example.test'}),'https://app.example.test/auth/callback');
});

test('native registration and recovery retain the app scheme',()=>{
 assert.equal(authRedirectUrl(native),'fugaplus://auth');
 assert.equal(authRedirectUrl(native,true),'fugaplus://auth?flow=recovery');
});

test('web redirect rejects missing or non-HTTP origins',()=>{
 for(const origin of [undefined,'file:///local','javascript:example','http://user:password@localhost:8081']){
  assert.throws(()=>authRedirectUrl({platform:'web',origin}));
 }
});

for(const raw of [
 'http://other.example.test/auth/callback?code=local-code',
 'http://localhost:8082/auth/callback?code=local-code',
 'http://localhost:8081/other?code=local-code',
 'http://user@localhost:8081/auth/callback?code=local-code',
 'fugaplus://auth?code=local-code',
 'not-a-url',
]){
 test('web ignores unrelated callback '+raw,async()=>{
  let calls=0;
  const handle=createAuthCallbackHandler(async()=>{calls++;return success;});
  assert.equal(await handle(raw,web),false);
  assert.equal(calls,0);
 });
}

for(const suffix of [
 '', '?flow=recovery', '?code=', '?code=one&code=two',
 '?error=access_denied&error_description=private-context',
 '#error=access_denied&error_description=private-context',
 '?code=local-code&error=access_denied',
 '?code=local-code#access_token=local-token',
]){
 test('invalid or non-PKCE callback is rejected '+suffix,async()=>{
  let calls=0;
  const handle=createAuthCallbackHandler(async()=>{calls++;return success;});
  await assert.rejects(handle(web.origin+'/auth/callback'+suffix,web),{message:AUTH_LINK_ERROR});
  assert.equal(calls,0);
 });
}

test('duplicate and concurrent callbacks exchange a one-use code only once',async()=>{
 let calls=0,finish;
 const pending=new Promise(resolve=>{finish=resolve;});
 const handle=createAuthCallbackHandler(async code=>{
  assert.equal(code,'local-code');calls++;
  await pending;
  return success;
 });
 const url=web.origin+'/auth/callback?code=local-code';
 const first=handle(url,web),second=handle(url,web);
 assert.equal(calls,1);
 finish();
 assert.deepEqual(await Promise.all([first,second]),[false,false]);
 assert.equal(await handle(url,web),false);
 assert.equal(calls,1);
});

test('recovery is enabled only after a successful code exchange',async()=>{
 const handle=createAuthCallbackHandler(async()=>success);
 assert.equal(await handle(web.origin+'/auth/callback?code=recovery-code&flow=recovery',web),true);
 const sdkRecovery=createAuthCallbackHandler(async()=>({...success,data:{session:{},redirectType:'recovery'}}));
 assert.equal(await sdkRecovery(web.origin+'/auth/callback?code=sdk-recovery',web),true);
});

test('native callbacks still exchange PKCE codes and distinguish recovery',async()=>{
 const received=[];
 const handle=createAuthCallbackHandler(async code=>{received.push(code);return success;});
 assert.equal(await handle('fugaplus://auth?code=native-code',native),false);
 assert.equal(await handle('fugaplus://auth?flow=recovery&code=native-recovery',native),true);
 assert.equal(await handle(web.origin+'/auth/callback?code=web-code',native),false);
 assert.equal(await handle('fugaplus://other?code=wrong-host',native),false);
 assert.deepEqual(received,['native-code','native-recovery']);
});

test('callback forwards the SDK flow id to select its own PKCE verifier',async()=>{
 const received=[];
 const handle=createAuthCallbackHandler(async(code,options)=>{received.push({code,options});return success;});
 assert.equal(await handle(web.origin+'/auth/callback?code=web-flow&sb_flow_id=local_flow_123',web),false);
 assert.equal(await handle('fugaplus://auth?code=native-flow&sb_flow_id=native_flow_123',native),false);
 assert.deepEqual(received,[
  {code:'web-flow',options:{flowId:'local_flow_123'}},
  {code:'native-flow',options:{flowId:'native_flow_123'}},
 ]);
});

test('invalid flow ids cannot fall back to another pending verifier',async()=>{
 let calls=0;
 const handle=createAuthCallbackHandler(async()=>{calls++;return success;});
 for(const suffix of ['', '../other', 'short', 'one_valid_id&sb_flow_id=another_valid_id']){
  await assert.rejects(handle(web.origin+'/auth/callback?code=local-code&sb_flow_id='+suffix,web),{message:AUTH_LINK_ERROR});
 }
 assert.equal(calls,0);
});

test('provider and network failures expose only a generic error and allow retry',async()=>{
 let calls=0;
 const handle=createAuthCallbackHandler(async()=>{
  calls++;
  if(calls===1)return {error:new Error('private-context'),data:{session:null}};
  if(calls===2)throw new Error('private-context');
  return success;
 });
 const url=web.origin+'/auth/callback?code=retry-code';
 await assert.rejects(handle(url,web),{message:AUTH_LINK_ERROR});
 await assert.rejects(handle(url,web),{message:AUTH_LINK_ERROR});
 assert.equal(await handle(url,web),false);
 assert.equal(calls,3);
});

test('an exchange without a session never opens recovery',async()=>{
 const handle=createAuthCallbackHandler(async()=>({error:null,data:{session:null}}));
 await assert.rejects(handle(web.origin+'/auth/callback?code=empty-session&flow=recovery',web),{message:AUTH_LINK_ERROR});
});

test('cleanup removes code, error, hash and arbitrary redirect targets',()=>{
 for(const suffix of ['?code=local-code','?error=access_denied#private-context','?code=local-code&next=https://other.example.test']){
  const url=web.origin+'/auth/callback'+suffix;
  assert.equal(cleanCallbackTarget(url,url),web.origin+'/');
 }
 assert.equal(cleanCallbackTarget(web.origin+'/auth/callback?code=old',web.origin+'/auth/callback?code=new'),null);
 assert.equal(cleanCallbackTarget(web.origin+'/?code=unrelated',web.origin+'/?code=unrelated'),null);
 assert.equal(cleanCallbackTarget('https://other.example.test/auth/callback',web.origin+'/auth/callback'),null);
});

function memoryStorage(){
 const values=new Map();
 return {
  getItem:name=>values.get(name)??null,
  setItem:(name,value)=>values.set(name,value),
  removeItem:name=>values.delete(name),
 };
}

test('web storage shares PKCE state across tab adapters and removes it',async()=>{
 const shared=memoryStorage();
 const first=createWebAuthStorage(()=>shared),second=createWebAuthStorage(()=>shared);
 await first.setItem('verifier','local-verifier');
 assert.equal(await second.getItem('verifier'),'local-verifier');
 await second.removeItem('verifier');
 assert.equal(await first.getItem('verifier'),null);
});

test('SDK registration and another-tab PKCE callback work with mocked HTTP only',async()=>{
 const shared=memoryStorage(),requests=[];
 const storageKey='local-auth-test';
 const user={id:'11111111-1111-4111-8111-111111111111',aud:'authenticated',role:'authenticated',email:'tester@example.test',app_metadata:{provider:'email'},user_metadata:{},identities:[{id:'local-identity'}],created_at:new Date().toISOString()};
 const encoded=value=>Buffer.from(JSON.stringify(value)).toString('base64url');
 const token=encoded({alg:'HS256',typ:'JWT'})+'.'+encoded({sub:user.id,exp:Math.floor(Date.now()/1000)+3600})+'.local-signature';
 const fetchMock=async(input,init)=>{
  const url=new URL(String(input)),body=JSON.parse(init.body);
  assert.equal(url.origin,'https://auth.example.test');
  assert.equal(init.method,'POST');
  requests.push({url,body});
  if(url.pathname==='/auth/v1/signup'){
   assert.equal(url.searchParams.get('redirect_to'),authRedirectUrl(web));
   assert.equal(body.code_challenge_method,'s256');
   return new Response(JSON.stringify(user),{status:200,headers:{'content-type':'application/json'}});
  }
  assert.equal(url.pathname,'/auth/v1/token');
  assert.equal(url.searchParams.get('grant_type'),'pkce');
  assert.equal(body.auth_code,'local-confirmation-code');
  const challenge=createHash('sha256').update(body.code_verifier).digest('base64url');
  assert.equal(challenge,requests[0].body.code_challenge);
  return new Response(JSON.stringify({access_token:token,refresh_token:'local-refresh-only',token_type:'bearer',expires_in:3600,user}),{status:200,headers:{'content-type':'application/json'}});
 };
 const client=()=>createClient('https://auth.example.test','sb_publishable_local-test-only',{
  global:{fetch:fetchMock},
  auth:{storage:createWebAuthStorage(()=>shared),storageKey,flowType:'pkce',detectSessionInUrl:false,autoRefreshToken:false,persistSession:true},
 });
 const first=client(),second=client();
 try{
  const signup=await first.auth.signUp({email:user.email,password:'Local-only-password-123',options:{emailRedirectTo:authRedirectUrl(web)}});
  assert.equal(signup.error,null);
  assert.ok(shared.getItem(storageKey+'-code-verifier'));
  const handle=createAuthCallbackHandler(code=>second.auth.exchangeCodeForSession(code));
  const url=web.origin+'/auth/callback?code=local-confirmation-code';
  assert.equal(await handle(url,web),false);
  assert.equal(await handle(url,web),false);
  assert.equal(requests.length,2);
  assert.equal(shared.getItem(storageKey+'-code-verifier'),null);
  const {data,error}=await second.auth.getSession();
  assert.equal(error,null);
  assert.equal(data.session.user.id,user.id);
 }finally{
  await first.auth.stopAutoRefresh();
  await second.auth.stopAutoRefresh();
 }
});

test('SDK callback without the original verifier fails without any HTTP request',async()=>{
 let requests=0;
 const memory=memoryStorage();
 const client=createClient('https://auth.example.test','sb_publishable_local-test-only',{
  global:{fetch:async()=>{requests++;throw new Error('HTTP must not run');}},
  auth:{storage:createWebAuthStorage(()=>memory),storageKey:'missing-verifier-test',flowType:'pkce',detectSessionInUrl:false,autoRefreshToken:false,persistSession:true},
 });
 try{
  const handle=createAuthCallbackHandler((code,options)=>client.auth.exchangeCodeForSession(code,options));
  await assert.rejects(handle(web.origin+'/auth/callback?code=missing-verifier',web),{message:AUTH_LINK_ERROR});
  assert.equal(requests,0);
  assert.equal((await client.auth.getSession()).data.session,null);
 }finally{await client.auth.stopAutoRefresh();}
});
