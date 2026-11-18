import React,{useEffect,useState} from 'react';
import { BackHandler,Image,Pressable,SafeAreaView,StatusBar,Text,View } from 'react-native';
import { useFonts, PlusJakartaSans_400Regular, PlusJakartaSans_700Bold } from '@expo-google-fonts/plus-jakarta-sans';
import * as Notifications from 'expo-notifications';
import { AuthProvider,useAuth } from './src/auth/AuthProvider';
import { Access,ResetPassword } from './src/screens/Access';
import { NewExpense } from './src/screens/NewExpense';
import { History } from './src/screens/History';
import { Dashboard } from './src/screens/Dashboard';
import { Leaks } from './src/screens/Leaks';
import { Profile } from './src/screens/Profile';
import { Admin } from './src/screens/Admin';
import { Busy,Button,Confirmation,ErrorText,Page,Title,styles,colors } from './src/components/ui';

type Tab='dashboard'|'new'|'history'|'leaks'|'profile'|'admin';
function Shell(){
 const auth=useAuth(),[tab,setTab]=useState<Tab>('dashboard'),[dirty,setDirty]=useState(false),[next,setNext]=useState<Tab|null>(null);
 const [leakId,setLeakId]=useState<string|undefined>();
 useEffect(()=>{setTab('dashboard');setDirty(false);setNext(null);setLeakId(undefined);},[auth.session?.user.id]);
 function navigate(target:Tab){if(target===tab)return;if(dirty)setNext(target);else setTab(target);}
 useEffect(()=>{
  const listener=BackHandler.addEventListener('hardwareBackPress',()=>{
   if(tab!=='dashboard'&&tab!=='admin'){navigate(auth.profile?.rol==='administrador'?'admin':'dashboard');return true;}return false;
  });return()=>listener.remove();
 },[tab,dirty,auth.profile?.rol]);
 useEffect(()=>{
  let alive=true;
  const handle=(response:Notifications.NotificationResponse)=>{
   if(!alive)return;
   const data=response.notification.request.content.data;
   if(data&&data.user_id===auth.session?.user.id&&auth.profile?.rol==='usuario'&&typeof data.fuga_id==='string'){setLeakId(data.fuga_id);navigate('leaks');void Notifications.clearLastNotificationResponseAsync().catch(()=>{});}
  };
  const listener=Notifications.addNotificationResponseReceivedListener(handle);
  void Notifications.getLastNotificationResponseAsync().then(response=>{if(response)handle(response);}).catch(()=>{});
  return()=>{alive=false;listener.remove();};
 },[auth.session?.user.id,auth.profile?.rol,dirty]);
 if(auth.recovery)return <ResetPassword/>;
 if(auth.loading)return <Page><Busy/></Page>;
 if(!auth.session)return <Access/>;
 if(!auth.profile)return <Page><Title>Conectemos tu cuenta</Title><ErrorText message={auth.error||'No se pudo cargar el perfil.'}/><Button title="Reintentar" onPress={()=>void auth.reload()}/><Button secondary title="Cerrar sesión" onPress={()=>void auth.logout()}/></Page>;
 const admin=auth.profile.rol==='administrador';
 const tabs:{id:Tab;label:string}[]=admin?[{id:'admin',label:'Cuentas'},{id:'profile',label:'Sesión'}]:[
  {id:'dashboard',label:'Resumen'},{id:'new',label:'Registrar'},{id:'history',label:'Historial'},{id:'leaks',label:'Fugas'},{id:'profile',label:'Perfil'}];
 const active=admin&&tab!=='profile'?'admin':tab;
 return <View key={auth.profile.id} style={{flex:1}}>
 <View style={{flexDirection:'row',alignItems:'center',paddingHorizontal:20,paddingVertical:6,backgroundColor:'#fff',borderBottomWidth:1,borderColor:colors.border}}>
 <Image source={require('./assets/branding/logo.png')} accessibilityLabel="FUGA+" style={{width:52,height:52}}/><Text style={[styles.heading,{marginLeft:10}]}>FUGA+</Text><Text style={[styles.muted,{marginLeft:'auto'}]}>{admin?'Administración':'Tu espacio'}</Text></View>
 <View style={{flex:1}}>{active==='new'?<NewExpense onDirty={setDirty}/>:active==='history'?<History onDirty={setDirty}/>:active==='leaks'?<Leaks initialId={leakId}/>:active==='profile'?<Profile/>:active==='admin'?<Admin/>:<Dashboard/>}</View>
 <View style={{flexDirection:'row',paddingBottom:8,paddingTop:8,borderTopWidth:1,borderColor:colors.border,backgroundColor:'#fff'}}>
 {tabs.map(item=><Pressable key={item.id} accessibilityRole="button" accessibilityState={{selected:active===item.id}} onPress={()=>navigate(item.id)} style={{flex:1,minHeight:52,alignItems:'center',justifyContent:'center',backgroundColor:active===item.id?'#D8F6EC':'#fff',borderRadius:12}}><Text style={{fontSize:12,color:colors.primary,fontWeight:active===item.id?'700':'400'}}>{item.label}</Text></Pressable>)}</View>
 <Confirmation visible={next!==null} title="¿Descartar el borrador?" message="Los datos sin confirmar se perderán al salir." onCancel={()=>{setNext(null);setLeakId(undefined);}} onConfirm={()=>{if(next)setTab(next);setNext(null);setDirty(false);}}/>
 </View>;
}
export default function App(){
 useFonts({PlusJakartaSans_400Regular,PlusJakartaSans_700Bold});
 return <SafeAreaView style={{flex:1,backgroundColor:colors.bg}}><StatusBar barStyle="dark-content"/><AuthProvider><Shell/></AuthProvider></SafeAreaView>;
}
