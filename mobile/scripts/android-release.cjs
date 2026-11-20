/** Local release preparation. Does not read backend dotenv or copy signing credentials. */
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {parseEnv}=require('node:util');
const {spawnSync,spawn}=require('node:child_process');
const {validateBuildEnvironment}=require('./check-public-env.cjs');
const {applyReleaseSigning}=require('../plugins/withReleaseSigning.cjs');
const {redactOutput}=require('./android-qa.cjs');
const ROOT=path.resolve(__dirname,'../..');
const PUBLIC_NAMES=['EXPO_PUBLIC_API_URL','EXPO_PUBLIC_SUPABASE_URL','EXPO_PUBLIC_SUPABASE_ANON_KEY',
 'EXPO_PUBLIC_GOOGLE_ENABLED','EXPO_PUBLIC_PASSWORD_RECOVERY_ENABLED','EXPO_PUBLIC_ADMIN_QA_MODE'];
const UTILITIES=['PATH','PATHEXT','SYSTEMROOT','WINDIR','TEMP','TMP','USERPROFILE','APPDATA','LOCALAPPDATA',
 'PROGRAMFILES','PROGRAMFILES(X86)','NUMBER_OF_PROCESSORS','PROCESSOR_ARCHITECTURE','HOME','HOMEDRIVE','HOMEPATH'];
function publicHttpsRoot(raw){
 const url=new URL(raw),host=url.hostname.toLowerCase().replace(/^\[|\]$/g,'');
 if(url.protocol!=='https:'||!host||url.username||url.password||url.search||url.hash||!['','/'].includes(url.pathname))return false;
 if(/^(localhost|0\.|127\.|10\.|192\.168\.|169\.254\.|172\.(1[6-9]|2[0-9]|3[01])\.)/.test(host)
   ||host.includes(':')||/\.(invalid|test|local|localhost)$/.test(host)||host.includes('placeholder'))return false;
 return true;
}
function prepareReleaseEnvironment(values,inherited={}){
 if(Object.keys(values).some(k=>!PUBLIC_NAMES.includes(k)))throw new Error('El entorno movil contiene variables fuera de la lista publica permitida.');
 if(values.EXPO_PUBLIC_ADMIN_QA_MODE&&!['false'].includes(values.EXPO_PUBLIC_ADMIN_QA_MODE))throw new Error('Desactiva el modo QA administrativo antes de preparar release.');
 for(const name of PUBLIC_NAMES.slice(0,3))if(typeof values[name]!=='string'||!values[name].trim())throw new Error('Faltan variables publicas obligatorias.');
 try{if(!publicHttpsRoot(values.EXPO_PUBLIC_API_URL)||!publicHttpsRoot(values.EXPO_PUBLIC_SUPABASE_URL))throw new Error();}
 catch{throw new Error('Release requiere raices HTTPS publicas, sin direcciones locales ni configuracion ficticia.');}
 const env={};
 for(const [k,v] of Object.entries(inherited))if(UTILITIES.includes(k.toUpperCase()))env[k]=v;
 for(const name of PUBLIC_NAMES)if(values[name]!==undefined)env[name]=values[name];
 Object.assign(env,{EXPO_PUBLIC_ADMIN_QA_MODE:'false',FUGA_RELEASE_BUILD:'1',FUGA_RELEASE_PREPARED:'1',
  EXPO_NO_DOTENV:'1',EXPO_OFFLINE:'1',CI:'1',DEBUG:'',NODE_ENV:'production'});
 validateBuildEnvironment(env);return env;
}
function currentEnvironment(){
 const values=parseEnv(fs.readFileSync(path.join(ROOT,'mobile/.env.local'),'utf8'));
 return prepareReleaseEnvironment(values,process.env);
}
const hash=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
function contained(base,file){
 const resolved=path.resolve(file),relative=path.relative(base,resolved);
 if(relative.startsWith('..')||path.isAbsolute(relative))throw new Error('Ruta fuera de la copia de compilacion.');
 // Do not follow directory junctions/symlinks into another workspace or private directory.
 let cursor=resolved;
 while(cursor!==base){if(fs.existsSync(cursor)&&fs.lstatSync(cursor).isSymbolicLink())throw new Error('No se admiten enlaces en las fuentes de compilacion.');cursor=path.dirname(cursor);}
 return resolved;
}
function sourceFiles(mobile){
 const result=['App.tsx','app.json','app.config.js','package.json','package-lock.json','tsconfig.json'];
 function visit(folder){
  if(!fs.existsSync(path.join(mobile,folder)))return;
  for(const item of fs.readdirSync(path.join(mobile,folder),{withFileTypes:true})){
   if(item.isSymbolicLink())throw new Error('No se copian fuentes enlazadas.');
   if(['node_modules','build','.gradle','.expo'].includes(item.name)||item.name.startsWith('.env')||/\.(keystore|jks|p12|pfx|p8|pem|key)$/i.test(item.name))continue;
   const rel=path.join(folder,item.name);
   if(item.isDirectory())visit(rel);else if(item.isFile())result.push(rel);
  }
 }
 for(const folder of ['src','assets','modules','plugins','scripts'])visit(folder);
 return result;
}
function isolatedMobile(){
 const metadata=JSON.parse(fs.readFileSync(path.join(ROOT,'.tools/android-short-build.json'),'utf8'));
 const parent=path.resolve(metadata.directory),target=path.join(parent,'mobile');
 if(path.dirname(parent)!==path.parse(parent).root||!/^fuga-plus-build-[a-f0-9]+$/.test(path.basename(parent))
   ||!fs.existsSync(target)||fs.lstatSync(parent).isSymbolicLink()||fs.lstatSync(target).isSymbolicLink())throw new Error('Copia aislada no reconocida.');
 if(JSON.parse(fs.readFileSync(path.join(target,'package.json'),'utf8')).name!=='fuga-plus-mobile')throw new Error('Paquete de compilacion inesperado.');
 return target;
}
function synchronize(mobile,target){
 // Existing dependencies must match; never run an installer or disguise stale node_modules.
 if(!fs.existsSync(path.join(target,'node_modules'))||hash(path.join(mobile,'package-lock.json'))!==hash(path.join(target,'package-lock.json')))
  throw new Error('La copia requiere preparar sus dependencias con el lock actual antes de sincronizar.');
 const files=sourceFiles(mobile);
 for(const rel of files){
  const source=contained(mobile,path.join(mobile,rel)),destination=contained(target,path.join(target,rel));
  fs.mkdirSync(path.dirname(destination),{recursive:true});fs.copyFileSync(source,destination);
 }
 // Exact source mirror for JS and plugins; never remove generated native builds or dependencies.
 let removed=0;
 for(const folder of ['src','plugins']){
  const scan=relative=>{
   const directory=contained(target,path.join(target,relative));if(!fs.existsSync(directory))return;
   for(const item of fs.readdirSync(directory,{withFileTypes:true})){
    const rel=path.join(relative,item.name),destination=contained(target,path.join(target,rel));
    if(item.isDirectory())scan(rel);
    else if(item.isFile()&&!files.includes(rel)){fs.unlinkSync(destination);removed++;}
   }
  };scan(folder);
 }
 for(const rel of files)if(hash(path.join(mobile,rel))!==hash(path.join(target,rel)))throw new Error('La comparacion de fuentes no coincide.');
 for(const base of [mobile,target]){
  const gradle=path.join(base,'android/app/build.gradle');
  if(fs.existsSync(gradle))fs.writeFileSync(gradle,applyReleaseSigning(fs.readFileSync(gradle,'utf8')));
 }
 return {files_verified:files.length,obsolete_source_files_removed:removed,dotenv_copied:false,keystore_copied:false};
}
function signingPaths(){
 return {file:path.join(ROOT,'.tools/android-release-signing/fugaplus-release.keystore'),alias:'fugaplus-release',
  keytool:path.join(ROOT,'.tools/jdk17/bin/keytool.exe')};
}
function verifySigning(paths,passwords,run=spawnSync){
 if(!passwords.store||!passwords.key)throw new Error('Faltan las contrasenas de firma; utiliza el lanzador PowerShell interactivo.');
 if(!fs.existsSync(paths.file)||!fs.existsSync(paths.keytool))throw new Error('Falta el keystore release o el keytool local.');
 const env={...prepareUtilityEnvironment(process.env),FUGA_ANDROID_STORE_PASSWORD:passwords.store};
 const result=run(paths.keytool,['-J-Duser.language=en','-list','-rfc','-keystore',paths.file,'-alias',paths.alias,
  '-storepass:env','FUGA_ANDROID_STORE_PASSWORD'],{env,encoding:'utf8',windowsHide:true});
 if(result.status!==0||!result.stdout?.includes('PrivateKeyEntry'))throw new Error('No se pudo validar la clave privada release. Revisa el keystore, alias y contrasena localmente.');
 try{
  const pem=result.stdout.match(/-----BEGIN CERTIFICATE-----[\s\S]+?-----END CERTIFICATE-----/)[0];
  const cert=new crypto.X509Certificate(pem);
  if(/Android Debug/i.test(cert.subject)||Date.parse(cert.validTo)<=Date.now()||Date.parse(cert.validFrom)>Date.now())throw new Error();
  return {certificate_sha256:cert.fingerprint256.replace(/:/g,''),debug_certificate:false};
 }catch{throw new Error('El certificado release es de depuracion, no es valido o esta vencido.');}
}
function prepareUtilityEnvironment(inherited){
 const out={};for(const [k,v] of Object.entries(inherited))if(UTILITIES.includes(k.toUpperCase()))out[k]=v;return out;
}
function main(){
 const action=process.argv[2];if(!['check','prepare','build'].includes(action))throw new Error('Usa check, prepare o el lanzador PowerShell para build.');
 const environment=currentEnvironment(),mobile=path.join(ROOT,'mobile'),target=isolatedMobile(),signing=signingPaths();
 if(action==='check'){
  console.log(JSON.stringify({public_release_config_valid:true,admin_qa_enabled:false,release_mode:true,
   signing_keystore_present:fs.existsSync(signing.file),signing_credentials_required:true,build_started:false}));return;
 }
 const sync=synchronize(mobile,target);
 if(action==='prepare'){console.log(JSON.stringify({...sync,public_release_config_valid:true,release_mode:true,admin_qa_enabled:false,
  signing_keystore_present:fs.existsSync(signing.file),build_started:false}));return;}
 const passwords={store:process.env.FUGA_ANDROID_STORE_PASSWORD,key:process.env.FUGA_ANDROID_KEY_PASSWORD};
 verifySigning(signing,passwords);
 Object.assign(environment,{FUGA_ANDROID_KEYSTORE_PATH:signing.file,FUGA_ANDROID_KEY_ALIAS:signing.alias,
  FUGA_ANDROID_STORE_PASSWORD:passwords.store,FUGA_ANDROID_KEY_PASSWORD:passwords.key});
 const child=spawn('powershell.exe',['-NoProfile','-File',path.join(mobile,'scripts/android-local.ps1'),'-Task','Apk','-MobileRoot',target],
  {cwd:ROOT,env:environment,stdio:['inherit','pipe','pipe'],windowsHide:true});
 for(const stream of [child.stdout,child.stderr]){
  let pending='';stream.setEncoding('utf8');stream.on('data',chunk=>{
   pending+=chunk;const lines=pending.split('\n');pending=lines.pop();
   for(const line of lines)process.stdout.write(redactLine(line)+'\n');
  });stream.on('end',()=>{if(pending)process.stdout.write(redactLine(pending));});
 }
 function redactLine(value){for(const secret of [passwords.store,passwords.key])if(secret)value=value.split(secret).join('[REDACTED]');return redactOutput(value,environment);}
 child.on('error',()=>{console.error('No se pudo iniciar la compilacion release.');process.exitCode=1;});
 child.on('exit',code=>{process.exitCode=code??1;});process.on('SIGINT',()=>child.kill('SIGINT'));
}
module.exports={prepareReleaseEnvironment,sourceFiles,synchronize,applyReleaseSigning,verifySigning};
if(require.main===module){try{main();}catch{console.error('Preparacion release rechazada: revisa la guia APK_RELEASE_LOCAL.md; no se muestran valores.');process.exitCode=1;}}
