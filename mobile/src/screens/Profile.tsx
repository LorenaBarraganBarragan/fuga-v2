import React,{useEffect,useState} from 'react';
import { Image,Platform,Text } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { api } from '../lib/api';
import { Profile as UserProfile } from '../lib/types';
import { useAuth } from '../auth/AuthProvider';
import { Button,Confirmation,ErrorText,Field,Page,Title,styles } from '../components/ui';

type Signature={timestamp:number;public_id:string;signature:string;api_key:string;upload_url:string};
export function Profile(){
 const auth=useAuth(),[name,setName]=useState(auth.profile?.nombres||''),[surname,setSurname]=useState(auth.profile?.apellido||''),[phone,setPhone]=useState(auth.profile?.telefono||'');
 const [busy,setBusy]=useState(false),[error,setError]=useState(''),[message,setMessage]=useState(''),[logout,setLogout]=useState(false);
 const [deactivate,setDeactivate]=useState(false);
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
   if((asset.fileSize||0)>5000000)throw new Error('La fotografía debe tener máximo 5 MB.');
   const type=asset.mimeType||'image/jpeg';
   if(!['image/jpeg','image/png','image/webp'].includes(type))throw new Error('Selecciona una imagen JPEG, PNG o WebP.');
   const signature=await api<Signature>('/me/photo/signature',{method:'POST'});
   const form=new FormData();
   form.append('api_key',signature.api_key);form.append('timestamp',String(signature.timestamp));form.append('public_id',signature.public_id);form.append('signature',signature.signature);
   if(Platform.OS==='web')form.append('file',await (await fetch(asset.uri)).blob());
   else form.append('file',{uri:asset.uri,name:asset.fileName||'perfil.jpg',type} as unknown as Blob);
   const upload=await fetch(signature.upload_url,{method:'POST',body:form});
   if(!upload.ok)throw new Error('No se pudo cargar la fotografía.');
   await api<UserProfile>('/me/photo/complete',{method:'POST',body:{public_id:signature.public_id}});
   await auth.reload();setMessage('Fotografía actualizada.');
  }catch(e){setError((e as Error).message);}finally{setBusy(false);}
 }
 const admin=auth.profile?.rol==='administrador';
 return <Page><Title>{admin?'Tu sesión administrativa':'Tu perfil'}</Title><Text style={styles.muted}>{auth.session?.user.email}</Text>
 {!admin&&<>
 {!!auth.profile?.foto_url&&<Image source={{uri:auth.profile.foto_url}} style={{width:96,height:96,borderRadius:48}} accessibilityLabel="Tu fotografía de perfil"/>}
 <Field label="Nombres" value={name} maxLength={80} onChangeText={setName}/><Field label="Apellido" value={surname} maxLength={80} onChangeText={setSurname}/><Field label="Teléfono colombiano (opcional)" value={phone} onChangeText={setPhone} keyboardType="phone-pad" maxLength={10}/>
 <ErrorText message={error}/>{!!message&&<Text accessibilityRole="alert" style={styles.text}>{message}</Text>}
 <Button title="Guardar perfil" disabled={busy} onPress={()=>void save()}/><Button secondary title="Cambiar fotografía" disabled={busy} onPress={()=>void photo()}/>
 {!!googlePhoto&&<Button secondary title="Autorizar mi foto de Google" disabled={busy} onPress={()=>void useGoogle()}/>}
 </>}
 <Text style={styles.muted}>Tus gastos son privados. Un administrador gestiona estados de cuentas; no puede consultar tus gastos ni evidencias individuales.</Text>
 <Button secondary title="Cerrar sesión" onPress={()=>setLogout(true)}/>
 {auth.profile?.rol==='usuario'&&<Button secondary title="Desactivar mi cuenta" disabled={busy} onPress={()=>setDeactivate(true)}/>}
 <Confirmation visible={logout} title="Cerrar sesión" message="Se eliminará la sesión local y se solicitará el cierre en Supabase." onCancel={()=>setLogout(false)} onConfirm={()=>{void auth.logout();}}/>
 <Confirmation visible={deactivate} title="Desactivar mi cuenta" message="No podrás acceder a tus gastos. Los datos se conservan 30 días para recuperación administrativa; después se programan para supresión según la política del proyecto. No se promete el borrado inmediato de respaldos." onCancel={()=>setDeactivate(false)} onConfirm={()=>void disable()}/>
 </Page>;
}
