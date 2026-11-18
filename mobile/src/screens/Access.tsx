import React, { useState } from 'react';
import { Image, Platform, Text, View } from 'react-native';
import * as WebBrowser from 'expo-web-browser';
import { supabase, authConfigured } from '../lib/supabase';
import { useAuth } from '../auth/AuthProvider';
import { Welcome } from '../components/Welcome';
import { PublicFormPage } from '../components/PublicFormPage';
import { exchangeAuthUrl, getAuthRedirectUrl } from '../auth/links';
import { Button, ErrorText, Field, Page, Title, styles } from '../components/ui';

export function Access() {
 const auth=useAuth();
 const [mode,setMode]=useState<'welcome'|'login'|'register'|'reset'>('welcome');
 const [email,setEmail]=useState(''),[password,setPassword]=useState(''),[confirm,setConfirm]=useState('');
 const [busy,setBusy]=useState(false),[error,setError]=useState(''),[message,setMessage]=useState('');
 async function submit(){
  setError('');setMessage('');
  if(!authConfigured){setError('El servicio de acceso no está disponible en este entorno. Intenta más tarde.');return;}
  if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())){setError('Correo: escribe una dirección válida.');return;}
  if(mode!=='reset'&&password.length<8){setError('Contraseña: utiliza al menos 8 caracteres.');return;}
  if(mode==='register'&&password!==confirm){setError('Confirmación: las contraseñas no coinciden.');return;}
  setBusy(true);
  try {
   const normalized=email.trim().toLowerCase();
   if(mode==='login'){
    const {error:err}=await supabase.auth.signInWithPassword({email:normalized,password});
    if(err)throw new Error('No fue posible iniciar sesión. Revisa tus credenciales o el estado de tu cuenta.');
   } else if(mode==='register'){
    const {data,error:err}=await supabase.auth.signUp({email:normalized,password,options:{emailRedirectTo:getAuthRedirectUrl()}});
    if(err||data.user?.identities?.length===0)throw new Error('No fue posible crear la cuenta. Revisa los datos o prueba iniciar sesión.');
    if(!data.session)setMessage('Revisa tu correo para confirmar la cuenta y luego inicia sesión.');
   } else {
    if(process.env.EXPO_PUBLIC_PASSWORD_RECOVERY_ENABLED!=='true')throw new Error('El servicio de recuperación no está disponible por el momento.');
    const {error:err}=await supabase.auth.resetPasswordForEmail(normalized,{redirectTo:getAuthRedirectUrl(true)});
    if(err)throw new Error('El servicio de recuperación no está disponible. Intenta más tarde.');
    setMessage('Si existe una cuenta con ese correo, recibirás instrucciones para recuperar el acceso.');
   }
   setPassword('');setConfirm('');
  }catch(e){setError((e as Error).message);}finally{setBusy(false);}
 }
 async function google(){
  setError('');setBusy(true);
  try {
   if(!authConfigured||process.env.EXPO_PUBLIC_GOOGLE_ENABLED!=='true')throw new Error('Google no está configurado. Puedes iniciar sesión con correo.');
   const redirectTo=getAuthRedirectUrl();
   const {data,error:err}=await supabase.auth.signInWithOAuth({provider:'google',options:{redirectTo,skipBrowserRedirect:Platform.OS!=='web'}});
   if(err||!data.url)throw new Error('Google no está disponible.');
   if(Platform.OS==='web')return;
   const result=await WebBrowser.openAuthSessionAsync(data.url,redirectTo);
   if(result.type==='success'){
    await exchangeAuthUrl(result.url);
   }
  }catch(e){setError((e as Error).message);}finally{setBusy(false);}
 }
 function change(next:typeof mode){setMode(next);setError('');setMessage('');setPassword('');setConfirm('');}
 if(mode==='welcome')return <Welcome onCreateAccount={()=>change('register')} onLogin={()=>change('login')} error={error||auth.error}/>;
 return <PublicFormPage feedback={error||auth.error||message}><Image source={require('../../assets/branding/logo.png')} style={{width:112,height:112,alignSelf:'center'}} accessibilityLabel="Logo FUGA+"/><Title>{mode==='login'?'Qué bueno verte':mode==='register'?'Crea tu cuenta':'Recupera tu acceso'}</Title>
 <Field label="Correo electrónico" value={email} onChangeText={setEmail} keyboardType="email-address" autoCapitalize="none" autoComplete="email"/>
 {mode!=='reset'&&<Field label="Contraseña (mínimo 8 caracteres)" value={password} onChangeText={setPassword} secureTextEntry autoCapitalize="none" autoComplete={mode==='register'?'new-password':'current-password'}/>}
 {mode==='register'&&<Field label="Confirmar contraseña" value={confirm} onChangeText={setConfirm} secureTextEntry/>}
 <Button disabled={busy} title={busy?'Conectando…':mode==='login'?'Iniciar sesión':mode==='register'?'Registrarse':'Enviar enlace'} onPress={()=>void submit()}/>
 {mode==='login'&&<><Button secondary title="Continuar con Google" disabled={busy} onPress={()=>void google()}/><Button secondary title="Olvidé mi contraseña" onPress={()=>change('reset')}/></>}
 <Button secondary title="Volver al inicio" onPress={()=>change('welcome')}/>
 <ErrorText message={error||auth.error}/>{!!message&&<Text accessibilityRole="alert" style={styles.text}>{message}</Text>}</PublicFormPage>;
}

export function ResetPassword(){
 const auth=useAuth(),[password,setPassword]=useState(''),[confirm,setConfirm]=useState(''),[error,setError]=useState(''),[busy,setBusy]=useState(false);
 async function save(){
  if(password.length<8||password!==confirm){setError('Usa al menos 8 caracteres y confirma la misma contraseña.');return;}
  setBusy(true);
  const {error:err}=await supabase.auth.updateUser({password});
  setBusy(false);
  if(err)setError('No se pudo cambiar la contraseña; el enlace puede haber vencido.');
  else {setPassword('');setConfirm('');auth.finishRecovery();}
 }
 return <Page><Title>Nueva contraseña</Title><Field label="Nueva contraseña" secureTextEntry value={password} onChangeText={setPassword}/><Field label="Confirmación" secureTextEntry value={confirm} onChangeText={setConfirm}/><ErrorText message={error}/><Button title="Guardar contraseña" disabled={busy} onPress={()=>void save()}/><Button secondary title="Cerrar sesión" onPress={()=>void auth.logout()}/></Page>;
}
