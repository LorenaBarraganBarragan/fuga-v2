/** Public visual review only: fictional configuration, no dotenv, no live backend. */
const path=require('node:path');
const {spawn}=require('node:child_process');
const {prepareQaEnvironment}=require('./android-qa.cjs');

function prepareWelcomePreviewEnvironment(inherited={}){
 const environment=prepareQaEnvironment({
  EXPO_PUBLIC_SUPABASE_URL:'https://welcome-preview.example.invalid',
  EXPO_PUBLIC_SUPABASE_ANON_KEY:'sb_publishable_visual_preview_fixture',
  EXPO_PUBLIC_API_URL:'http://127.0.0.1:18888',
 },inherited);
 environment.EXPO_PUBLIC_API_URL='http://127.0.0.1:18888';
 return environment;
}

function main(){
 const child=spawn(process.execPath,['node_modules/expo/bin/cli','start','--localhost','--port','8085','--clear'],{
  cwd:path.resolve(__dirname,'..'),env:prepareWelcomePreviewEnvironment(process.env),stdio:'inherit',windowsHide:true,
 });
 child.on('error',()=>{console.error('No fue posible abrir la vista previa local.');process.exitCode=1;});
 child.on('exit',code=>{process.exitCode=code??1;});
 process.on('SIGINT',()=>child.kill('SIGINT'));
}
module.exports={prepareWelcomePreviewEnvironment};
if(require.main===module)main();
