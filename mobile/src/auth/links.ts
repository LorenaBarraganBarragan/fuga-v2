import { Platform } from 'react-native';
import { supabase } from '../lib/supabase';
import { authRedirectUrl, cleanCallbackTarget, createAuthCallbackHandler, type CallbackContext } from './callback';

function context(): CallbackContext {
 return Platform.OS==='web'
  ? {platform:'web',origin:typeof window!=='undefined'?window.location.origin:undefined}
  : {platform:'native'};
}

export function getAuthRedirectUrl(recovery=false):string {
 return authRedirectUrl(context(),recovery);
}

const handleCallback=createAuthCallbackHandler((code,options)=>supabase.auth.exchangeCodeForSession(code,options));
export async function exchangeAuthUrl(raw:string):Promise<boolean>{
 try {
  return await handleCallback(raw,context());
 } finally {
  if(Platform.OS==='web'&&typeof window!=='undefined'){
   const target=cleanCallbackTarget(raw,window.location.href);
   if(target)window.history.replaceState(window.history.state,'',target);
  }
 }
}
