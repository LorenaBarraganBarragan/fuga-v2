const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {prepareReleaseEnvironment,sourceFiles,synchronize,applyReleaseSigning,verifySigning}=require('../scripts/android-release.cjs');
const values=()=>({EXPO_PUBLIC_API_URL:'https://fuga-api.example.com',EXPO_PUBLIC_SUPABASE_URL:'https://project.supabase.co',EXPO_PUBLIC_SUPABASE_ANON_KEY:'sb_publishable_public_fixture'});
const gradle=`apply plugin: 'com.android.application'
android {
 signingConfigs { debug { } }
 buildTypes {
  debug { signingConfig signingConfigs.debug }
  release {
   // Expo template
   signingConfig signingConfigs.debug
   minifyEnabled true
  }
 }
}
`;
function temporary(t){const folder=fs.mkdtempSync(path.join(os.tmpdir(),'fuga-release-test-'));t.after(()=>fs.rmSync(folder,{recursive:true,force:true}));return folder;}

test('release environment accepts only required public values and clears inherited secrets and simulation',()=>{
 const env=prepareReleaseEnvironment(values(),{PATH:'tools',DATABASE_URL:'private-fixture',CLOUDINARY_API_SECRET:'private-fixture',SUPABASE_SERVICE_ROLE_KEY:'private-fixture',EXPO_PUBLIC_ADMIN_QA_MODE:'true',EXPO_NO_CLIENT_ENV_VARS:'1',FUGA_ADMIN_QA:'1',HTTP_PROXY:'private-fixture',EXPO_PUBLIC_API_URL:'http://127.0.0.1:18000'});
 assert.equal(env.EXPO_PUBLIC_API_URL,values().EXPO_PUBLIC_API_URL);
 assert.equal(env.EXPO_PUBLIC_ADMIN_QA_MODE,'false');assert.equal(env.FUGA_RELEASE_BUILD,'1');assert.equal(env.EXPO_NO_DOTENV,'1');assert.equal(env.NODE_ENV,'production');
 for(const name of ['DATABASE_URL','CLOUDINARY_API_SECRET','SUPABASE_SERVICE_ROLE_KEY','EXPO_NO_CLIENT_ENV_VARS','FUGA_ADMIN_QA','HTTP_PROXY'])assert.equal(env[name],undefined);
 assert.throws(()=>prepareReleaseEnvironment({...values(),EXPO_PUBLIC_ADMIN_QA_MODE:'true'}));
 assert.throws(()=>prepareReleaseEnvironment({...values(),CLOUDINARY_API_SECRET:'private-fixture'}));
 assert.throws(()=>prepareReleaseEnvironment({...values(),EXPO_PUBLIC_EXTRA:'arbitrary-fixture'}));
});

test('release rejects missing config, private keys, URL credentials and local or fictitious backends',()=>{
 for(const name of ['EXPO_PUBLIC_API_URL','EXPO_PUBLIC_SUPABASE_URL','EXPO_PUBLIC_SUPABASE_ANON_KEY'])assert.throws(()=>prepareReleaseEnvironment({...values(),[name]:''}));
 for(const api of ['http://public.example.com','https://localhost','https://127.0.0.1','https://192.168.1.10','https://10.0.0.1','https://172.16.0.1','https://[::1]','https://admin-qa.invalid','https://api.local','https://user:fixture@public.example.com','https://api.example.com/api/v1'])assert.throws(()=>prepareReleaseEnvironment({...values(),EXPO_PUBLIC_API_URL:api}));
 assert.throws(()=>prepareReleaseEnvironment({...values(),EXPO_PUBLIC_SUPABASE_ANON_KEY:'sb_secret_private_fixture'}),error=>!error.message.includes('private_fixture'));
});

test('signing plugin changes only release signing and is idempotent without any credentials',()=>{
 const first=applyReleaseSigning(gradle),second=applyReleaseSigning(first);
 assert.equal(first,second);assert.match(first,/debug \{ signingConfig signingConfigs.debug \}/);
 assert.match(first,/release \{[\s\S]*signingConfig signingConfigs.fugaRelease/);
 assert.match(first,/minifyEnabled true/);assert.equal(first.split('FUGA RELEASE SIGNING BEGIN').length-1,1);
 assert.match(first,/System.getenv\('FUGA_ANDROID_STORE_PASSWORD'\)/);
 assert.match(first,/it.name.contains\('Release'\)/);
 assert.throws(()=>applyReleaseSigning(gradle.replace('release {','customRelease {')));
 assert.throws(()=>applyReleaseSigning(gradle.replace('signingConfig signingConfigs.debug\n   minify','signingConfig signingConfigs.existingPrivate\n   minify')));
});

test('real Expo config mod preserves package/version and wires persistent release signing',async()=>{
 const withSigning=require('../plugins/withReleaseSigning.cjs');
 const original=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../app.json'),'utf8')).expo;
 const config=withSigning(structuredClone(original));
 const evaluated=await config.mods.android.appBuildGradle({...config,modResults:{language:'groovy',contents:gradle},modRequest:{platform:'android',modName:'appBuildGradle',introspect:true},mods:{},_internal:{}});
 assert.match(evaluated.modResults.contents,/signingConfigs.fugaRelease/);
 assert.equal(config.android.package,'co.edu.fugaplus.app');assert.equal(config.version,original.version);
});

test('synchronization includes the QA guard and plugin but excludes dotenv, keystore and generated directories',t=>{
 const folder=temporary(t),source=path.join(folder,'source'),copy=path.join(folder,'copy');
 for(const base of [source,copy])fs.mkdirSync(base,{recursive:true});
 for(const base of [source,copy]){
  fs.writeFileSync(path.join(base,'package-lock.json'),'same-lock');fs.mkdirSync(path.join(base,'android/app'),{recursive:true});fs.writeFileSync(path.join(base,'android/app/build.gradle'),gradle);
 }
 for(const name of ['App.tsx','app.json','app.config.js','package.json','tsconfig.json'])fs.writeFileSync(path.join(source,name),'fixture');
 for(const directory of ['src/lib','plugins','assets','scripts','modules/local/build'])fs.mkdirSync(path.join(source,directory),{recursive:true});
 fs.writeFileSync(path.join(source,'src/lib/adminQaAuth.ts'),'debug-only fixture');fs.writeFileSync(path.join(source,'plugins/signing.cjs'),'fixture');
 fs.writeFileSync(path.join(source,'.env.local'),'not-copied');fs.writeFileSync(path.join(source,'assets/private.keystore'),'not-copied');fs.writeFileSync(path.join(source,'modules/local/build/generated.txt'),'not-copied');
 fs.writeFileSync(path.join(source,'assets/private.p8'),'not-copied');fs.writeFileSync(path.join(source,'assets/private.pfx'),'not-copied');
 fs.mkdirSync(path.join(copy,'node_modules'));fs.mkdirSync(path.join(copy,'src'));fs.writeFileSync(path.join(copy,'src/obsolete.ts'),'obsolete');
 const result=synchronize(source,copy);
 assert.equal(result.dotenv_copied,false);assert.equal(result.keystore_copied,false);
 assert.equal(fs.readFileSync(path.join(copy,'src/lib/adminQaAuth.ts'),'utf8'),'debug-only fixture');
 assert.equal(fs.existsSync(path.join(copy,'.env.local')),false);assert.equal(fs.existsSync(path.join(copy,'assets/private.keystore')),false);
 assert.equal(fs.existsSync(path.join(copy,'assets/private.p8')),false);assert.equal(fs.existsSync(path.join(copy,'assets/private.pfx')),false);
 assert.equal(fs.existsSync(path.join(copy,'modules/local/build/generated.txt')),false);assert.equal(fs.existsSync(path.join(copy,'src/obsolete.ts')),false);
 assert.match(fs.readFileSync(path.join(copy,'android/app/build.gradle'),'utf8'),/signingConfigs.fugaRelease/);
 assert.ok(sourceFiles(source).includes(path.join('src','lib','adminQaAuth.ts')));
 fs.writeFileSync(path.join(copy,'package-lock.json'),'stale-lock');assert.throws(()=>synchronize(source,copy));
});

test('synchronization refuses targets linked outside the isolated source tree',t=>{
 const folder=temporary(t),source=path.join(folder,'source'),copy=path.join(folder,'copy'),outside=path.join(folder,'outside');
 for(const base of [source,copy,outside])fs.mkdirSync(base);
 for(const base of [source,copy])fs.writeFileSync(path.join(base,'package-lock.json'),'same-lock');
 fs.mkdirSync(path.join(copy,'node_modules'));fs.symlinkSync(outside,path.join(copy,'src'),process.platform==='win32'?'junction':'dir');
 for(const name of ['App.tsx','app.json','app.config.js','package.json','tsconfig.json'])fs.writeFileSync(path.join(source,name),'fixture');
 fs.mkdirSync(path.join(source,'src'));fs.writeFileSync(path.join(source,'src/test.ts'),'fixture');
 assert.throws(()=>synchronize(source,copy));assert.deepEqual(fs.readdirSync(outside),[]);
});

test('signature preflight refuses missing secrets before invoking keytool and never logs them',()=>{
 let invoked=false;
 assert.throws(()=>verifySigning({},{},()=>{invoked=true;}));assert.equal(invoked,false);
});

test('keytool receives password variable names instead of password arguments and failures do not expose them',t=>{
 const folder=temporary(t),file=path.join(folder,'fixture.keystore'),keytool=path.join(folder,'fixture-keytool');
 fs.writeFileSync(file,'not-a-real-keystore');fs.writeFileSync(keytool,'not-an-executable');
 const secrets={store:'fixture-store-password',key:'fixture-key-password'};
 assert.throws(()=>verifySigning({file,keytool,alias:'fixture-alias'},secrets,(exe,args,options)=>{
  assert.equal(exe,keytool);assert.ok(args.includes('-storepass:env'));
  assert.ok(!args.some(arg=>arg===secrets.store||arg===secrets.key));
  assert.equal(options.env.FUGA_ANDROID_STORE_PASSWORD,secrets.store);
  return {status:1,stderr:secrets.store,stdout:''};
 }),error=>!error.message.includes(secrets.store)&&!error.message.includes(secrets.key));
});
