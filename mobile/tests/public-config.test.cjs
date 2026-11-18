const {test}=require('node:test');
const assert=require('node:assert/strict');
const {isPublicSupabaseKey,isSupabaseRoot,isApiRoot}=require('../src/lib/publicConfig.ts');
const jwt=role=>'local-header.'+Buffer.from(JSON.stringify({role})).toString('base64url')+'.local-signature';
test('client accepts publishable or legacy anon keys and rejects privileged credentials',()=>{
 assert.equal(isPublicSupabaseKey('sb_publishable_local_test_value'),true);
 assert.equal(isPublicSupabaseKey(jwt('anon')),true);
 for(const key of ['sb_secret_local_test_value',jwt('service_role'),jwt('authenticated'),'','not-a-public-key'])assert.equal(isPublicSupabaseKey(key),false);
});
test('Supabase client URL must be the HTTPS project root',()=>{
 assert.equal(isSupabaseRoot('https://project.example.test/'),true);
 for(const url of ['http://project.example.test','https://project.example.test/auth/v1','https://user:private@project.example.test','https://project.example.test?key=private'])assert.equal(isSupabaseRoot(url),false);
});
test('release API requires HTTPS without credentials, API prefixes or query',()=>{
 assert.equal(isApiRoot('http://192.0.2.1:8000',false),true);
 assert.equal(isApiRoot('https://api.example.test',true),true);
 for(const url of ['http://192.0.2.1:8000','https://api.example.test/api/v1','https://user:private@api.example.test','https://api.example.test?token=private'])assert.equal(isApiRoot(url,true),false);
});
