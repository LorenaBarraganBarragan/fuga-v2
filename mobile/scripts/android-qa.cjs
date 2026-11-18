/** Local Android QA: public config only, USB API, no dotenv copied to the build. */
const fs=require('node:fs');
const path=require('node:path');
const {parseEnv}=require('node:util');
const {spawn}=require('node:child_process');
const {validateBuildEnvironment}=require('./check-public-env.cjs');

const PUBLIC_NAMES=['EXPO_PUBLIC_SUPABASE_URL','EXPO_PUBLIC_SUPABASE_ANON_KEY','EXPO_PUBLIC_API_URL','EXPO_PUBLIC_PASSWORD_RECOVERY_ENABLED','EXPO_PUBLIC_GOOGLE_ENABLED'];
const UTILITY_NAMES=['PATH','PATHEXT','SYSTEMROOT','WINDIR','COMSPEC','TEMP','TMP','USERPROFILE','APPDATA','LOCALAPPDATA','PROGRAMFILES','PROGRAMFILES(X86)','PROGRAMDATA','NUMBER_OF_PROCESSORS','PROCESSOR_ARCHITECTURE','HOME','HOMEDRIVE','HOMEPATH','ANDROID_HOME','ANDROID_SDK_ROOT','JAVA_HOME'];

function prepareQaEnvironment(values,inherited={},photos=false){
 if(Object.keys(values).some(name=>!PUBLIC_NAMES.includes(name)))throw new Error('El archivo móvil contiene variables no permitidas para QA. No se muestran valores.');
 validateBuildEnvironment(values);
 for(const name of PUBLIC_NAMES.slice(0,3))if(!values[name])throw new Error('Falta configuración pública obligatoria para Android QA.');
 const environment={};
 for(const [name,value] of Object.entries(inherited))if(UTILITY_NAMES.includes(name.toUpperCase()))environment[name]=value;
 for(const name of PUBLIC_NAMES)if(values[name]!==undefined)environment[name]=values[name];
 // This endpoint belongs to the disposable backend, never the configured financial DB.
 environment.EXPO_PUBLIC_API_URL=photos?'http://127.0.0.1:18001':'http://127.0.0.1:18000';
 environment.EXPO_PUBLIC_PASSWORD_RECOVERY_ENABLED='false';
 environment.EXPO_PUBLIC_GOOGLE_ENABLED='false';
 environment.EXPO_NO_DOTENV='1';
 environment.EXPO_OFFLINE='1';
 environment.FUGA_RELEASE_BUILD='0';
 environment.CI='1';
 environment.DEBUG='';
 validateBuildEnvironment(environment);
 return environment;
}

function redactOutput(text,environment){
 for(const name of ['EXPO_PUBLIC_SUPABASE_URL','EXPO_PUBLIC_SUPABASE_ANON_KEY'])if(environment[name])text=text.split(environment[name]).join('[PUBLIC_CONFIG]');
 return text.replace(/sb_secret_[A-Za-z0-9_-]+/g,'[REDACTED_SECRET]')
  .replace(/eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/g,'[REDACTED_JWT]')
  .replace(/sb-[A-Za-z0-9_-]+-auth-token/g,'[AUTH_STORAGE]')
  .replace(/device=[^&\s'"<>]+/g,'device=[REDACTED]');
}

function main(){
 const action=process.argv[2]||'check';
 if(!['check','build','metro','check-photos','metro-photos','metro-review'].includes(action))throw new Error('Usa check, build, metro, check-photos, metro-photos o metro-review.');
 const mobile=path.resolve(__dirname,'..');
 const photos=action.endsWith('-photos'),metro=action==='metro'||action==='metro-photos'||action==='metro-review';
 const environment=prepareQaEnvironment(parseEnv(fs.readFileSync(path.join(mobile,'.env.local'),'utf8')),process.env,photos);
 if(action==='check'||action==='check-photos'){
  console.log(JSON.stringify({public_configuration_valid:true,server_secrets_inherited:false,qa_api:environment.EXPO_PUBLIC_API_URL,optional_providers_disabled:true,dotenv_copied:false}));
  return;
 }
 const command=metro?process.execPath:'powershell.exe';
 let args;
 if(metro)args=['node_modules/expo/bin/cli','start','--localhost','--port',action==='metro-review'?'8086':photos?'8084':'8083','--clear'];
 else{
  const buildMobile=process.argv[3]||path.join(JSON.parse(fs.readFileSync(path.join(mobile,'../.tools/android-short-build.json'),'utf8')).directory,'mobile');
  args=['-NoProfile','-File',path.join(__dirname,'android-local.ps1'),'-Task','Debug','-MobileRoot',buildMobile,'-SkipPrebuild'];
 }
 const child=spawn(command,args,{cwd:mobile,env:environment,stdio:['inherit','pipe','pipe'],windowsHide:true});
 for(const stream of [child.stdout,child.stderr]){
  let pending='';stream.setEncoding('utf8');
  stream.on('data',chunk=>{pending+=chunk;const lines=pending.split('\n');pending=lines.pop();for(const line of lines)process.stdout.write(redactOutput(line,environment)+'\n');});
  stream.on('end',()=>{if(pending)process.stdout.write(redactOutput(pending,environment));});
 }
 child.on('error',()=>{console.error('No fue posible iniciar la herramienta QA. No se muestran valores.');process.exitCode=1;});
 child.on('exit',code=>{process.exitCode=code??1;});
 process.on('SIGINT',()=>child.kill('SIGINT'));
}
module.exports={prepareQaEnvironment,redactOutput};
if(require.main===module){try{main();}catch{console.error('Configuración QA inválida. Revisa las variables públicas sin compartir sus valores.');process.exitCode=1;}}
