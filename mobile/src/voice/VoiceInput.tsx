import React,{useEffect,useState} from 'react';
import { PermissionsAndroid,Platform,Text } from 'react-native';
import { requireOptionalNativeModule } from 'expo-modules-core';
import { Button,ErrorText,styles } from '../components/ui';

type VoiceModule={start:()=>Promise<string>;stop:()=>Promise<void>;cancel:()=>Promise<void>};
const native=Platform.OS==='android'?requireOptionalNativeModule<VoiceModule>('FugaVoice'):null;
export function VoiceInput({onTranscript}:{onTranscript:(text:string)=>void}){
 const [recording,setRecording]=useState(false),[error,setError]=useState('');
 useEffect(()=>()=>{if(native)void native.cancel().catch(()=>{});},[]);
 async function start(){
  if(!native)return;
  setError('');
  const permission=await PermissionsAndroid.request(PermissionsAndroid.PERMISSIONS.RECORD_AUDIO,{
   title:'Dictar un gasto',message:'El reconocimiento del dispositivo puede procesar audio mediante servicios externos. FUGA+ no guarda archivos de audio.',
   buttonPositive:'Permitir',buttonNegative:'Ahora no',
  });
  if(permission!==PermissionsAndroid.RESULTS.GRANTED){setError('Sin permiso de micrófono. Puedes escribir tu gasto.');return;}
  setRecording(true);
  try{const text=await native.start();if(text.trim())onTranscript(text.trim().slice(0,280));}
  catch{setError('No fue posible reconocer la voz. Puedes reintentar o escribir tu gasto.');}
  finally{setRecording(false);}
 }
 if(!native)return <Text style={styles.muted}>{Platform.OS==='android'?'El dictado no está disponible en esta versión. Puedes escribir tu gasto.':'Puedes registrar tu gasto por texto. La voz está disponible solo en Android.'}</Text>;
 return <><Text style={styles.muted}>Voz opcional · máximo 30 segundos. El servicio del dispositivo puede procesar audio externamente. FUGA+ no guarda audio.</Text>
 <Button secondary title={recording?'Detener y transcribir':'Dictar gasto'} onPress={()=>{if(recording)void native.stop();else void start();}}/><ErrorText message={error}/></>;
}
