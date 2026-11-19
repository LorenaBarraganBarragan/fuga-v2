/** Starts only the administrative Metro; no dotenv, adb, builds or financial QA changes. */
const path=require('node:path');
const {spawn}=require('node:child_process');
const {validateBuildEnvironment}=require('./check-public-env.cjs');
const {redactOutput}=require('./android-qa.cjs');

function prepareAdminQaEnvironment(inherited={}){
 const environment={};
 const names=['PATH','PATHEXT','SYSTEMROOT','WINDIR','COMSPEC','TEMP','TMP','USERPROFILE','APPDATA','LOCALAPPDATA','PROGRAMFILES','PROGRAMFILES(X86)','NUMBER_OF_PROCESSORS','PROCESSOR_ARCHITECTURE','HOME','HOMEDRIVE','HOMEPATH'];
 for(const [name,value] of Object.entries(inherited))if(names.includes(name.toUpperCase()))environment[name]=value;
 Object.assign(environment,{EXPO_PUBLIC_ADMIN_QA_MODE:'true',EXPO_PUBLIC_SUPABASE_URL:'https://admin-qa.invalid',
  EXPO_PUBLIC_SUPABASE_ANON_KEY:'sb_publishable_fugaplus_admin_qa',EXPO_PUBLIC_API_URL:'http://127.0.0.1:18002',
  EXPO_PUBLIC_GOOGLE_ENABLED:'false',EXPO_PUBLIC_PASSWORD_RECOVERY_ENABLED:'false',
  EXPO_NO_DOTENV:'1',EXPO_OFFLINE:'1',FUGA_RELEASE_BUILD:'0',CI:'1',DEBUG:'',NODE_ENV:'development'});
 validateBuildEnvironment(environment);return environment;
}
function main(){
 const action=process.argv[2];if(!['check','metro'].includes(action))throw new Error('Usa check o metro.');
 const environment=prepareAdminQaEnvironment(process.env);
 if(action==='check'){console.log('QA administrativo: configuración sintética válida, sin dotenv ni secretos heredados.');return;}
 const child=spawn(process.execPath,['node_modules/expo/bin/cli','start','--localhost','--port','8087','--clear'],{cwd:path.resolve(__dirname,'..'),env:environment,stdio:['inherit','pipe','pipe'],windowsHide:true});
 for(const stream of [child.stdout,child.stderr]){
  let pending='';stream.setEncoding('utf8');
  stream.on('data',chunk=>{pending+=chunk;const lines=pending.split('\n');pending=lines.pop();for(const line of lines)process.stdout.write(redactOutput(line,environment)+'\n');});
  stream.on('end',()=>{if(pending)process.stdout.write(redactOutput(pending,environment));});
 }
 child.on('error',()=>{console.error('No se pudo iniciar Metro administrativo.');process.exitCode=1;});
 child.on('exit',code=>{process.exitCode=code??1;});process.on('SIGINT',()=>child.kill('SIGINT'));
}
module.exports={prepareAdminQaEnvironment};
if(require.main===module){try{main();}catch{console.error('Configuración QA administrativa rechazada.');process.exitCode=1;}}
