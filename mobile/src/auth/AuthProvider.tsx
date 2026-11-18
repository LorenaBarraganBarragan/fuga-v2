import React, { createContext, useContext, useEffect, useRef, useState } from 'react';
import { Session } from '@supabase/supabase-js';
import { Linking, Platform } from 'react-native';
import * as WebBrowser from 'expo-web-browser';
import { supabase, authConfigured } from '../lib/supabase';
import { api, accountDenied, accountSessionChanged } from '../lib/api';
import { Profile } from '../lib/types';
import { exchangeAuthUrl } from './links';
import { AUTH_LINK_ERROR } from './callback';

WebBrowser.maybeCompleteAuthSession();
type Auth = {session:Session|null;profile:Profile|null;loading:boolean;error:string;recovery:boolean;reload:()=>Promise<void>;logout:()=>Promise<void>;finishRecovery:()=>void};
const Context=createContext<Auth>({} as Auth);
export const useAuth=()=>useContext(Context);
export function AuthProvider({children}:{children:React.ReactNode}) {
 const [session,setSession]=useState<Session|null>(null),[profile,setProfile]=useState<Profile|null>(null);
 const [loading,setLoading]=useState(true),[error,setError]=useState(''),[recovery,setRecovery]=useState(false);
 const activeUser=useRef<string|null>(null);
 async function logout() {
  accountSessionChanged(null);
  activeUser.current=null;setProfile(null);setSession(null);setRecovery(false);setError('');
  // Attempt remote signout; clear local credentials even if the network fails.
  try { await supabase.auth.signOut({scope:'global'}); } finally { await supabase.auth.signOut({scope:'local'}); }
 }
 async function reload() {
  setLoading(true);setError('');
  try { const loaded=await api<Profile>('/me');if(loaded.id===activeUser.current)setProfile(loaded); } catch(e) { if(activeUser.current)setError((e as Error).message); }
  finally { setLoading(false); }
 }
 useEffect(()=>{
  let alive=true;
  if (!authConfigured) {setLoading(false);setError('Configura las variables públicas de Supabase en mobile/.env.local.');return;}
  const {data:{subscription}}=supabase.auth.onAuthStateChange((event,next)=>{
   if(alive){activeUser.current=next?.user.id||null;accountSessionChanged(activeUser.current);setSession(next);if(event==='PASSWORD_RECOVERY')setRecovery(true);if(!next){setProfile(null);setRecovery(false);}}
  });
  accountDenied(()=>{void logout();});
  async function consume(url:string|null|undefined) {
   if(!url)return;
   try{if(await exchangeAuthUrl(url)&&alive)setRecovery(true);}catch{if(alive)setError(AUTH_LINK_ERROR);}
  }
  async function initialize(){
   try{
    const initial=Platform.OS==='web'&&typeof window!=='undefined'?window.location.href:await Linking.getInitialURL().catch(()=>null);
    await consume(initial);
    const {data,error:err}=await supabase.auth.getSession();
    if(alive){activeUser.current=data.session?.user.id||null;accountSessionChanged(activeUser.current);setSession(data.session);if(err)setError('No se pudo recuperar la sesión.');}
   }catch{if(alive)setError('No se pudo recuperar la sesión.');}
   finally{if(alive)setLoading(false);}
  }
  void initialize();
  const listener=Linking.addEventListener('url',({url})=>{void consume(url);});
  return ()=>{alive=false;subscription.unsubscribe();listener.remove();accountDenied(null);};
 },[]);
 useEffect(()=>{setProfile(null);if(session)void reload();},[session?.user.id]);
 const visibleProfile=profile?.id===session?.user.id?profile:null;
 return <Context.Provider value={{session,profile:visibleProfile,loading,error,recovery,reload,logout,finishRecovery:()=>setRecovery(false)}}>{children}</Context.Provider>;
}
