const {test}=require('node:test');
const assert=require('node:assert/strict');
const {createClient}=require('@supabase/supabase-js');
const {prepareAdminQaEnvironment}=require('../scripts/admin-qa.cjs');
const {validateBuildEnvironment}=require('../scripts/check-public-env.cjs');
const {adminQaFetch,ADMIN_QA_ORIGIN,ADMIN_QA_API,ADMIN_QA_PUBLIC_KEY}=require('../src/lib/adminQaAuth.ts');
const path=require('node:path');
const {loadComponent}=require('./component-loader.cjs');

test('client keeps production Auth options and fails closed when QA is requested outside debug',t=>{
 const previousDev=globalThis.__DEV__,names=['EXPO_PUBLIC_ADMIN_QA_MODE','EXPO_PUBLIC_SUPABASE_URL','EXPO_PUBLIC_SUPABASE_ANON_KEY','EXPO_PUBLIC_API_URL'];
 const previous=Object.fromEntries(names.map(n=>[n,process.env[n]]));
 t.after(()=>{globalThis.__DEV__=previousDev;for(const n of names){if(previous[n]===undefined)delete process.env[n];else process.env[n]=previous[n];}});
 const calls=[];
 const load=()=>loadComponent('src/lib/supabase.ts',{
  'react-native-url-polyfill/auto':{},'react-native':{Platform:{OS:'web'}},'expo-secure-store':{},
  '@supabase/supabase-js':{createClient:(...args)=>{calls.push(args);return {};},processLock:()=>{}},
  [path.resolve(__dirname,'../src/auth/callback')]:{createWebAuthStorage:()=>({})},
 });
 globalThis.__DEV__=false;
 delete process.env.EXPO_PUBLIC_ADMIN_QA_MODE;
 process.env.EXPO_PUBLIC_SUPABASE_URL='https://provider.example.test';process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY='sb_publishable_fixture';
 process.env.EXPO_PUBLIC_API_URL='https://api.example.test';
 load();assert.equal(calls.length,1);assert.equal(calls[0][2].global,undefined);
 assert.equal(calls[0][2].auth.flowType,'pkce');assert.equal(calls[0][2].auth.persistSession,true);
 const env=prepareAdminQaEnvironment();for(const n of names)process.env[n]=env[n];
 assert.throws(load);assert.equal(calls.length,1);
 globalThis.__DEV__=true;load();assert.equal(typeof calls[1][2].global.fetch,'function');
 process.env.EXPO_PUBLIC_API_URL='https://api.example.test';assert.throws(load);
});

test('admin QA launcher has synthetic config only and never inherits private values or dotenv switches',()=>{
 const env=prepareAdminQaEnvironment({PATH:'tools',DATABASE_URL:'private-fixture',SUPABASE_SERVICE_ROLE_KEY:'private-fixture',
  CLOUDINARY_API_SECRET:'private-fixture',HTTP_PROXY:'http://proxy.invalid',EXPO_PUBLIC_API_URL:'https://real.invalid',EXPO_NO_CLIENT_ENV_VARS:'1',NODE_ENV:'production'});
 assert.equal(env.EXPO_PUBLIC_API_URL,ADMIN_QA_API);
 assert.equal(env.EXPO_PUBLIC_SUPABASE_URL,ADMIN_QA_ORIGIN);
 assert.equal(env.EXPO_PUBLIC_SUPABASE_ANON_KEY,ADMIN_QA_PUBLIC_KEY);
 assert.equal(env.EXPO_NO_DOTENV,'1');assert.equal(env.NODE_ENV,'development');
 for(const key of ['DATABASE_URL','SUPABASE_SERVICE_ROLE_KEY','CLOUDINARY_API_SECRET','HTTP_PROXY','EXPO_NO_CLIENT_ENV_VARS'])assert.equal(env[key],undefined);
});

test('release guard rejects admin QA and incomplete or mixed provider configuration',()=>{
 const env=prepareAdminQaEnvironment();
 for(const changes of [{FUGA_RELEASE_BUILD:'1'},{NODE_ENV:'production'},{EXPO_PUBLIC_SUPABASE_URL:'https://real.invalid'},
  {EXPO_PUBLIC_API_URL:'https://real.invalid'},{EXPO_PUBLIC_ADMIN_QA_MODE:'false'},{EXPO_PUBLIC_ADMIN_QA_MODE:undefined},
  {EXPO_PUBLIC_SUPABASE_ANON_KEY:'sb_publishable_other'},{EXPO_PUBLIC_ADMIN_QA_MODE:'yes'}])assert.throws(()=>validateBuildEnvironment({...env,...changes}));
 assert.doesNotThrow(()=>validateBuildEnvironment({FUGA_RELEASE_BUILD:'1',NODE_ENV:'production',EXPO_PUBLIC_API_URL:'https://api.example.test',EXPO_PUBLIC_SUPABASE_URL:'https://provider.example.test',EXPO_PUBLIC_SUPABASE_ANON_KEY:'sb_publishable_fixture'}));
});

test('Auth adapter rejects other origins, provider admin, signups, redirects and unsupported request forms before sending',async()=>{
 let calls=0;const send=adminQaFetch(async()=>{calls++;return new Response('{}');});
 for(const input of ['https://real.invalid/auth/v1/token?grant_type=password','http://127.0.0.1:18002/auth/v1/token?grant_type=password',
  ADMIN_QA_ORIGIN+'/auth/v1/signup',ADMIN_QA_ORIGIN+'/auth/v1/admin/users/fixture',ADMIN_QA_ORIGIN+'/rest/v1/perfil',
  ADMIN_QA_ORIGIN+'/auth/v1/token?grant_type=pkce','https://user:pass@admin-qa.invalid/auth/v1/user',ADMIN_QA_ORIGIN+'/auth/v1/user#fragment'])await assert.rejects(send(input,{method:'POST'}));
 await assert.rejects(send(new Request(ADMIN_QA_ORIGIN+'/auth/v1/user')));
 assert.equal(calls,0);
 await send(ADMIN_QA_ORIGIN+'/auth/v1/user');assert.equal(calls,1);
});

test('real SDK uses normal password login, refresh, user and logout exclusively through the loopback adapter',async()=>{
 const requests=[];let active=true;
 const user={id:'c059ce3f-b782-4b88-a7f1-1e085b9f3000',aud:'authenticated',role:'authenticated',email:'fixture@admin-qa.invalid',created_at:'2026-01-01T00:00:00Z',app_metadata:{provider:'email'},user_metadata:{}};
 const session=()=>({access_token:'local-fixture-access',refresh_token:'local-fixture-refresh',token_type:'bearer',expires_in:900,user});
 const transport=adminQaFetch(async(url,options)=>{
  requests.push({url,method:options?.method||'GET',body:options?.body&&JSON.parse(options.body),redirect:options.redirect});
  assert.ok(url.startsWith(ADMIN_QA_API+'/auth/v1/'));assert.equal(options.redirect,'error');
  if(url.includes('/token?'))return Response.json(session());
  if(url.includes('/logout')){active=false;return Response.json({});}
  if(url.endsWith('/user'))return Response.json(user);
  throw new Error('Unexpected local request');
 });
 const client=createClient(ADMIN_QA_ORIGIN,ADMIN_QA_PUBLIC_KEY,{global:{fetch:transport},auth:{persistSession:false,autoRefreshToken:false,detectSessionInUrl:false}});
 const login=await client.auth.signInWithPassword({email:user.email,password:'local-fixture-password'});assert.equal(login.error,null);
 assert.equal(requests[0].body.email,user.email);assert.equal(requests[0].body.password,'local-fixture-password');
 assert.deepEqual(requests[0].body.gotrue_meta_security,{});
 assert.equal((await client.auth.refreshSession()).error,null);
 assert.equal((await client.auth.getUser()).data.user.id,user.id);
 assert.equal((await client.auth.signOut()).error,null);assert.equal(active,false);
 assert.ok(requests.some(r=>r.url.includes('grant_type=refresh_token')));
});
