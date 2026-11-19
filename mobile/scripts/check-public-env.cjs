/** Build-time guard: fail before Expo can inline a privileged key. No values are logged. */
function validateBuildEnvironment(environment) {
 if(environment.EXPO_PUBLIC_ADMIN_QA_MODE!==undefined){
  if(!['','false','true'].includes(environment.EXPO_PUBLIC_ADMIN_QA_MODE))throw new Error('Indicador QA administrativo inválido.');
  if(environment.EXPO_PUBLIC_ADMIN_QA_MODE==='true'&&(environment.FUGA_RELEASE_BUILD==='1'||environment.NODE_ENV==='production'
    ||environment.EXPO_PUBLIC_SUPABASE_URL!=='https://admin-qa.invalid'
    ||environment.EXPO_PUBLIC_SUPABASE_ANON_KEY!=='sb_publishable_fugaplus_admin_qa'
    ||environment.EXPO_PUBLIC_API_URL!=='http://127.0.0.1:18002'))throw new Error('QA administrativo requiere debug y configuración exclusivamente local.');
 }
 if((environment.EXPO_PUBLIC_SUPABASE_URL==='https://admin-qa.invalid'||environment.EXPO_PUBLIC_SUPABASE_ANON_KEY==='sb_publishable_fugaplus_admin_qa')
   &&environment.EXPO_PUBLIC_ADMIN_QA_MODE!=='true')throw new Error('La configuración del simulador requiere su modo QA explícito.');
 const entries=Object.entries(environment).filter(([name])=>name.startsWith('EXPO_PUBLIC_'));
 for(const [name,value] of entries){
  // Existing feature flags contain no credential; PASSWORD_RECOVERY is not a password.
  if(['EXPO_PUBLIC_PASSWORD_RECOVERY_ENABLED','EXPO_PUBLIC_GOOGLE_ENABLED'].includes(name)){
   if(!['','true','false'].includes(value))throw new Error('Las opciones públicas de acceso deben ser true o false, sin credenciales.');
   continue;
  }
  if(/SECRET|SERVICE_ROLE|DATABASE|PASSWORD|TOKEN|JWT/i.test(name)||String(value).includes('sb_secret_'))throw new Error('Configuración pública insegura. Retira las credenciales privadas del entorno móvil; no compartas sus valores.');
  if(typeof value==='string'&&value.split('.').length===3){
   try{const payload=JSON.parse(Buffer.from(value.split('.')[1],'base64url').toString('utf8'));if(payload.role&&payload.role!=='anon')throw new Error('private-key');}
   catch(error){if(error.message==='private-key')throw new Error('Configuración pública insegura: una clave privilegiada no puede incluirse en el cliente.');}
  }
  if(['EXPO_PUBLIC_API_URL','EXPO_PUBLIC_SUPABASE_URL'].includes(name)&&value){
   let url;try{url=new URL(value);}catch{throw new Error('URL pública no válida. Revisa la raíz del servicio sin compartir valores.');}
   if(url.username||url.password||url.search||url.hash||!['','/'].includes(url.pathname))throw new Error('URL pública insegura: usa la raíz del servicio sin credenciales o parámetros.');
   if(!['https:','http:'].includes(url.protocol)||(name==='EXPO_PUBLIC_SUPABASE_URL'&&url.protocol!=='https:')||(environment.FUGA_RELEASE_BUILD==='1'&&url.protocol!=='https:'))throw new Error('El entorno de entrega requiere URLs HTTPS.');
  }
  if(name==='EXPO_PUBLIC_SUPABASE_ANON_KEY'&&value&&!/^sb_publishable_[A-Za-z0-9_-]+$/.test(value)){
   let role;try{role=JSON.parse(Buffer.from(value.split('.')[1]||'','base64url').toString('utf8')).role;}catch{}
   if(role!=='anon')throw new Error('La clave del cliente debe ser publishable o anon, nunca una credencial privada.');
  }
 }
}
module.exports={validateBuildEnvironment};
if(require.main===module){try{validateBuildEnvironment(process.env);console.log('Variables públicas: sin credenciales privadas detectadas.');}catch(error){console.error(error.message);process.exitCode=1;}}
