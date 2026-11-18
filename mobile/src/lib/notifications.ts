import { Platform } from 'react-native';
import * as SecureStore from 'expo-secure-store';
import * as Notifications from 'expo-notifications';
import { supabase } from './supabase';
import { Leak } from './types';
import * as Crypto from 'expo-crypto';
import { mayNotify } from './validation';

export async function enableNotifications(){
 if(Platform.OS==='web')return false;
 if(Platform.OS==='android')await Notifications.setNotificationChannelAsync('patterns',{name:'Posibles fugas',importance:Notifications.AndroidImportance.DEFAULT});
 const result=await Notifications.requestPermissionsAsync();
 return result.granted;
}
export async function notifyCandidate(leak:Leak){
 if(Platform.OS==='web')return;
 const permission=await Notifications.getPermissionsAsync();
 if(!permission.granted)return;
 const {data:{session}}=await supabase.auth.getSession();if(!session)return;
 const group=await Crypto.digestStringAsync(Crypto.CryptoDigestAlgorithm.SHA256,leak.categoria_nombre+'|'+leak.descripcion_normalizada+'|'+leak.regla_version);
 const name='alert.'+session.user.id+'.'+group;
 const last=Number(await SecureStore.getItemAsync(name)||0);
 if(!mayNotify(last,new Date()))return;
 await Notifications.scheduleNotificationAsync({content:{title:'FUGA+',body:'FUGA+ encontró un patrón de gastos para revisar',data:{fuga_id:leak.id,user_id:session.user.id}},trigger:null});
 await SecureStore.setItemAsync(name,String(Date.now()));
}
