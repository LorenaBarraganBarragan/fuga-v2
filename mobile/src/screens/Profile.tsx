import React,{useEffect,useRef,useState} from 'react';
import { Image,Platform,Text } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { api } from '../lib/api';
import { appendNativePhoto,photoUploadFailure,photoUploadForm,PhotoSignature,validatePhotoAsset } from '../lib/profilePhoto';
import { useAuth } from '../auth/AuthProvider';
import { Button,Confirmation,ErrorText,Field,Page,Title,styles } from '../components/ui';

export function Profile(){
 const auth=useAuth(),[name,setName]=useState(auth.profile?.nombres||''),[surname,setSurname]=useState(auth.profile?.apellido||''),[phone,setPhone]=useState(auth.profile?.telefono||'');
 const [busy,setBusy]=useState(false),[error,setError]=useState(''),[message,setMessage]=useState(''),[logout,setLogout]=useState(false);
 const [deactivate,setDeactivate]=useState(false);
 const [selected,setSelected]=useState<ReturnType<typeof validatePhotoAsset>|null>(null),[previewReady,setPreviewReady]=useState(false);
 const attempt=useRef<{signature:PhotoSignature;uploaded:boolean}|null>(null);
 const uploading=useRef(false);
 const identity=auth.session?.user.id;
 const active=useRef(identity),mounted=useRef(true),controller=useRef<AbortController|null>(null);
 active.current=identity;
 useEffect(()=>{mounted.current=true;setSelected(null);setPreviewReady(false);return()=>{mounted.current=false;controller.current?.abort();attempt.current=null;};},[identity]);
 async function disable(){
  setDeactivate(false);setBusy(true);setError('');
  try{await api('/me/deactivate',{method:'POST',body:{confirmado:true}});await auth.logout();}
  catch(e){setError((e as Error).message);}finally{setBusy(false);}
 }
 const googlePhoto=auth.session?.user.identities?.find(i=>i.provider==='google')?.identity_data?.avatar_url as string|undefined;
 async function useGoogle(){
  if(!googlePhoto)return;setBusy(true);setError('');
  try{await api('/me/photo/google',{method:'POST',body:{url:googlePhoto}});await auth.reload();setMessage('Foto de Google autorizada. Una fotografía cargada manualmente tiene prioridad.');}
  catch(e){setError((e as Error).message);}finally{setBusy(false);}
 }
 async function save(){
  setError('');setMessage('');
  if((name.trim()&&name.trim().length<2)||(surname.trim()&&surname.trim().length<2)||(phone&&!/^\d{10}$/.test(phone))){setError('Nombres: 2 a 80 caracteres. Teléfono opcional: 10 dígitos.');return;}
  setBusy(true);
  try{await api('/me',{method:'PATCH',body:{nombres:name.trim()||null,apellido:surname.trim()||null,telefono:phone||null}});await auth.reload();setMessage('Perfil actualizado.');}
  catch(e){setError((e as Error).message);}finally{setBusy(false);}
 }
 async function photo(){
  setError('');setMessage('');setBusy(true);
  try{
   const permission=await ImagePicker.requestMediaLibraryPermissionsAsync();
   if(!permission.granted)throw new Error('Puedes seguir usando la aplicación sin dar permiso para fotografías.');
   const result=await ImagePicker.launchImageLibraryAsync({mediaTypes:['images'],quality:1});
   const asset=result.assets?.[0];if(result.canceled||!asset)return;
   if(!mounted.current||active.current!==identity)return;
   setSelected(validatePhotoAsset(asset));setPreviewReady(false);attempt.current=null;
  }catch(e){setError((e as Error).message);}finally{setBusy(false);}
 }
 async function confirmPhoto(){
  if(!selected||!previewReady||busy||uploading.current)return;
  uploading.current=true;
  const owner=identity,abort=new AbortController();controller.current=abort;
  const assertOwner=()=>{if(!mounted.current||owner!==active.current||abort.signal.aborted)throw new Error('La carga fue cancelada o la sesión cambió.');};
  setBusy(true);setError('');setMessage('');
  const timeout=setTimeout(()=>abort.abort(),45000);
  try{
   validatePhotoAsset(selected);assertOwner();
   if(!attempt.current){const signature=await api<PhotoSignature>('/me/photo/signature',{method:'POST',signal:abort.signal});assertOwner();attempt.current={signature,uploaded:false};}
   const uploadAttempt=attempt.current;
   if(!uploadAttempt.uploaded){
    const form=photoUploadForm(uploadAttempt.signature);
    if(Platform.OS==='web'){
     const file=selected.file instanceof Blob?selected.file:await(await fetch(selected.uri,{signal:abort.signal})).blob();
     validatePhotoAsset({...selected,file:{size:file.size,type:file.type||selected.mimeType}});form.append('file',file,selected.fileName||'perfil.jpg');
    }else{
     const {File}=require('expo-file-system') as typeof import('expo-file-system');
     appendNativePhoto(form,selected,uri=>new File(uri));
    }
    assertOwner();
    let upload:Response;
    try{upload=await fetch(uploadAttempt.signature.upload_url,{method:'POST',body:form,signal:abort.signal});}
    catch{throw new Error('No se pudo cargar la fotografía. Comprueba que el teléfono tenga Internet por Wi-Fi o datos; el USB solo conecta con FastAPI.');}
    if(!upload.ok)throw new Error(await photoUploadFailure(upload));
    uploadAttempt.uploaded=true;
   }
   assertOwner();
   await api('/me/photo/complete',{method:'POST',body:{public_id:uploadAttempt.signature.public_id},signal:abort.signal});
   assertOwner();setSelected(null);attempt.current=null;setMessage('Fotografía actualizada.');
   await auth.reload();
  }catch(e){if(mounted.current&&owner===active.current)setError(abort.signal.aborted?'La carga se interrumpió. Puedes reintentar o cancelar.':(e as Error).message);}
  finally{uploading.current=false;clearTimeout(timeout);if(mounted.current&&owner===active.current)setBusy(false);}
 }
 async function cancelPhoto(){
  if(busy)return;
  setBusy(true);setError('');
  try{
   if(attempt.current){await api('/me/photo/cancel',{method:'POST',body:{public_id:attempt.current.signature.public_id}});}
   attempt.current=null;setSelected(null);setPreviewReady(false);
   await auth.reload();
  }catch{setError('No se pudo cancelar la carga. Puedes reintentar; la fotografía actual se conserva.');}
  finally{if(mounted.current)setBusy(false);}
 }
 const admin=auth.profile?.rol==='administrador';
 return <Page><Title>{admin?'Tu sesión administrativa':'Tu perfil'}</Title><Text style={styles.muted}>{auth.session?.user.email}</Text>
 {!admin&&<>
 {!!auth.profile?.foto_url&&<Image source={{uri:auth.profile.foto_url}} style={{width:96,height:96,borderRadius:48}} accessibilityLabel="Tu fotografía de perfil"/>}
 <Field label="Nombres" value={name} maxLength={80} onChangeText={setName}/><Field label="Apellido" value={surname} maxLength={80} onChangeText={setSurname}/><Field label="Teléfono colombiano (opcional)" value={phone} onChangeText={setPhone} keyboardType="phone-pad" maxLength={10}/>
 <ErrorText message={error}/>{!!message&&<Text accessibilityRole="alert" style={styles.text}>{message}</Text>}
 <Button title="Guardar perfil" disabled={busy||!!selected} onPress={()=>void save()}/><Button secondary title="Cambiar fotografía" disabled={busy||!!selected} onPress={()=>void photo()}/>
 {selected&&<>
 <Text style={styles.text}>Vista previa. Tu fotografía actual se conserva hasta confirmar la carga.</Text>
 <Image source={{uri:selected.uri}} style={{width:192,height:192,borderRadius:24}} accessibilityLabel="Vista previa de la fotografía seleccionada" onLoad={()=>setPreviewReady(true)} onError={()=>{setPreviewReady(false);setError('No se pudo abrir la imagen. Cancela y selecciona otra fotografía.');}}/>
 <Button title="Confirmar fotografía" disabled={busy||!previewReady} onPress={()=>void confirmPhoto()}/>
 <Button secondary title="Cancelar fotografía" disabled={busy} onPress={()=>void cancelPhoto()}/>
 </>}
 {!!googlePhoto&&<Button secondary title="Autorizar mi foto de Google" disabled={busy} onPress={()=>void useGoogle()}/>}
 </>}
 <Text style={styles.muted}>Tus gastos son privados. Un administrador gestiona estados de cuentas; no puede consultar tus gastos ni evidencias individuales.</Text>
 <Button secondary title="Cerrar sesión" onPress={()=>setLogout(true)}/>
 {auth.profile?.rol==='usuario'&&<Button secondary title="Desactivar mi cuenta" disabled={busy} onPress={()=>setDeactivate(true)}/>}
 <Confirmation visible={logout} title="Cerrar sesión" message="Se eliminará la sesión local y se solicitará el cierre en Supabase." onCancel={()=>setLogout(false)} onConfirm={()=>{void auth.logout();}}/>
 <Confirmation visible={deactivate} title="Desactivar mi cuenta" message="No podrás acceder a tus gastos. Los datos se conservan 30 días para recuperación administrativa; después se programan para supresión según la política del proyecto. No se promete el borrado inmediato de respaldos." onCancel={()=>setDeactivate(false)} onConfirm={()=>void disable()}/>
 </Page>;
}
