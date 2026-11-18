import { Platform } from 'react-native';
import * as SecureStore from 'expo-secure-store';
import * as Notifications from 'expo-notifications';
import { supabase } from './supabase';
import { Leak } from './types';
import * as Crypto from 'expo-crypto';
import { mayNotify } from './validation';
import { createReminderDispatcher } from './reminders';

export async function enableNotifications(){
 if(Platform.OS==='web')return false;
 if(Platform.OS==='android')await Notifications.setNotificationChannelAsync('patterns',{name:'Posibles fugas',importance:Notifications.AndroidImportance.DEFAULT});
 const result=await Notifications.requestPermissionsAsync();
 if(!result.granted)return false;
 if(Platform.OS==='android'&&(await Notifications.getNotificationChannelAsync('patterns'))?.importance===Notifications.AndroidImportance.NONE)return false;
 return true;
}
const dispatch=createReminderDispatcher({
 supported:()=>Platform.OS!=='web',
 permission:async()=>{
  if(!(await Notifications.getPermissionsAsync()).granted)return false;
  if(Platform.OS==='android'){
   await Notifications.setNotificationChannelAsync('patterns',{name:'Posibles fugas',importance:Notifications.AndroidImportance.DEFAULT});
   const channel=await Notifications.getNotificationChannelAsync('patterns');
   if(channel?.importance===Notifications.AndroidImportance.NONE)return false;
  }
  return true;
 },
 user:async()=>{const {data:{session}}=await supabase.auth.getSession();return session?.user.id||null;},
 digest:value=>Crypto.digestStringAsync(Crypto.CryptoDigestAlgorithm.SHA256,value),
 last:SecureStore.getItemAsync,
 save:SecureStore.setItemAsync,
 allowed:mayNotify,
 now:()=>new Date(),
 deliver:async(leak,userId,identifier)=>{
  await Notifications.scheduleNotificationAsync({identifier,content:{title:'FUGA+',body:'FUGA+ encontró un patrón de gastos para revisar',data:{fuga_id:leak.id,user_id:userId}},trigger:Platform.OS==='android'?{channelId:'patterns'}:null});
 },
});
export function notifyCandidate(leak:Leak){return dispatch(leak);}
