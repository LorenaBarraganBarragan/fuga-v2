const {test}=require('node:test');
const assert=require('node:assert/strict');
const {validateBuildEnvironment}=require('../scripts/check-public-env.cjs');
test('Expo build rejects secret public values before bundling without printing the value',()=>{
 const privateValue='sb_secret_local_fixture';
 for(const environment of [{EXPO_PUBLIC_SUPABASE_ANON_KEY:privateValue},{EXPO_PUBLIC_SERVICE_ROLE_KEY:'fixture'},{EXPO_PUBLIC_DATABASE_URL:'fixture'}]){
  assert.throws(()=>validateBuildEnvironment(environment),error=>!error.message.includes(privateValue));
 }
});
test('Expo build rejects legacy service-role JWT and allows public or server-only variables',()=>{
 const key=role=>'header.'+Buffer.from(JSON.stringify({role})).toString('base64url')+'.signature';
 assert.throws(()=>validateBuildEnvironment({EXPO_PUBLIC_SUPABASE_ANON_KEY:key('service_role')}));
 assert.throws(()=>validateBuildEnvironment({EXPO_PUBLIC_SUPABASE_ANON_KEY:key('authenticated')}));
 assert.doesNotThrow(()=>validateBuildEnvironment({EXPO_PUBLIC_SUPABASE_ANON_KEY:key('anon'),SUPABASE_SERVICE_ROLE_KEY:'server-only-fixture'}));
});
test('Expo never embeds URL passwords or session tokens and validates release HTTPS',()=>{
 for(const environment of [{EXPO_PUBLIC_API_URL:'https://user:private@api.example.test'},{EXPO_PUBLIC_ACCESS_TOKEN:'local-private-fixture'},{EXPO_PUBLIC_API_URL:'http://192.0.2.1:8000',FUGA_RELEASE_BUILD:'1'}])assert.throws(()=>validateBuildEnvironment(environment));
 assert.doesNotThrow(()=>validateBuildEnvironment({EXPO_PUBLIC_API_URL:'http://192.0.2.1:8000'}));
 assert.doesNotThrow(()=>validateBuildEnvironment({EXPO_PUBLIC_API_URL:'https://api.example.test',FUGA_RELEASE_BUILD:'1'}));
});

test('Expo preserves the existing boolean recovery and Google flags without allowing passwords',()=>{
 for(const value of ['true','false',''])assert.doesNotThrow(()=>validateBuildEnvironment({EXPO_PUBLIC_PASSWORD_RECOVERY_ENABLED:value,EXPO_PUBLIC_GOOGLE_ENABLED:value}));
 assert.throws(()=>validateBuildEnvironment({EXPO_PUBLIC_PASSWORD_RECOVERY_ENABLED:'sb_secret_local_fixture'}));
 assert.throws(()=>validateBuildEnvironment({EXPO_PUBLIC_PASSWORD:'local-private-fixture'}));
});
