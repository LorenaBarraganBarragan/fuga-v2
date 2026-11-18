const {test}=require('node:test');
const assert=require('node:assert/strict');
const {prepareQaEnvironment,redactOutput}=require('../scripts/android-qa.cjs');
const values=()=>({EXPO_PUBLIC_SUPABASE_URL:'https://provider.example.test',EXPO_PUBLIC_SUPABASE_ANON_KEY:'sb_publishable_local_fixture',EXPO_PUBLIC_API_URL:'http://192.0.2.1:8000'});

test('QA uses the USB backend and never inherits server secrets or old public values',()=>{
 const result=prepareQaEnvironment(values(),{PATH:'tools',SUPABASE_SERVICE_ROLE_KEY:'server-only',DATABASE_URL:'server-only',AWS_SECRET_ACCESS_KEY:'server-only',EXPO_PUBLIC_API_URL:'https://old.example.test',EXPO_NO_CLIENT_ENV_VARS:'1'});
 assert.equal(result.EXPO_PUBLIC_API_URL,'http://127.0.0.1:18000');
 assert.equal(result.EXPO_PUBLIC_SUPABASE_ANON_KEY,'sb_publishable_local_fixture');
 for(const name of ['SUPABASE_SERVICE_ROLE_KEY','DATABASE_URL','AWS_SECRET_ACCESS_KEY','EXPO_NO_CLIENT_ENV_VARS'])assert.equal(result[name],undefined);
 assert.equal(result.EXPO_NO_DOTENV,'1');assert.equal(result.FUGA_RELEASE_BUILD,'0');
 assert.equal(result.EXPO_PUBLIC_PASSWORD_RECOVERY_ENABLED,'false');assert.equal(result.EXPO_PUBLIC_GOOGLE_ENABLED,'false');
});
test('QA rejects missing configuration, private keys, privileged JWTs and unknown variables',()=>{
 for(const changes of [{EXPO_PUBLIC_SUPABASE_URL:''},{EXPO_PUBLIC_SUPABASE_ANON_KEY:'sb_secret_fixture'},{SUPABASE_SERVICE_ROLE_KEY:'server-only'},{EXPO_PUBLIC_EXTRA:'not-allowed'},{EXPO_PUBLIC_SUPABASE_ANON_KEY:'header.'+Buffer.from('{"role":"service_role"}').toString('base64url')+'.signature'}])assert.throws(()=>prepareQaEnvironment({...values(),...changes}));
});
test('QA tool output redacts configured values and dynamic credentials',()=>{
 const environment=prepareQaEnvironment(values());
 const output=redactOutput(environment.EXPO_PUBLIC_SUPABASE_URL+' '+environment.EXPO_PUBLIC_SUPABASE_ANON_KEY+' sb_secret_fixture eyJhbGciOiJFUzI1NiJ9.eyJzdWIiOiJmaXh0dXJlIn0.signature device=local-inspector-id&page=1',environment);
 for(const value of [environment.EXPO_PUBLIC_SUPABASE_URL,environment.EXPO_PUBLIC_SUPABASE_ANON_KEY,'sb_secret_fixture','eyJhbGciOiJFUzI1NiJ9','local-inspector-id'])assert.ok(!output.includes(value));
});

test('photo QA has a separate USB backend and never inherits Cloudinary credentials',()=>{
 const environment=prepareQaEnvironment(values(),{CLOUDINARY_API_SECRET:'backend-only',CLOUDINARY_API_KEY:'backend-only'},true);
 assert.equal(environment.EXPO_PUBLIC_API_URL,'http://127.0.0.1:18001');
 assert.equal(environment.CLOUDINARY_API_SECRET,undefined);assert.equal(environment.CLOUDINARY_API_KEY,undefined);
});
