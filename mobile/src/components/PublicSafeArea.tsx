import React,{createContext,useContext,useState} from 'react';
import {ActivityIndicator,Platform,StatusBar,StyleSheet,View} from 'react-native';
import {calculatePublicInsets,emptyPublicInsets,PublicInsets} from '../lib/publicInsets';
import {WindowInsetsProbe} from './WindowInsetsProbe';
import {colors} from './ui';

const Context=createContext<PublicInsets>({...emptyPublicInsets,ready:Platform.OS!=='android'});
export const usePublicInsets=()=>useContext(Context);

export function PublicSafeArea({children}:{children:React.ReactNode}){
 const [viewport,setViewport]=useState({width:0,height:0});
 const [insets,setInsets]=useState<PublicInsets>({...emptyPublicInsets,ready:Platform.OS!=='android'});
 return <View collapsable={false} style={layout.screen} onLayout={event=>{
  const {width,height}=event.nativeEvent.layout;
  setViewport(current=>current.width===width&&current.height===height?current:{width,height});
  if(Platform.OS==='android')StatusBar.setBarStyle('dark-content');
 }}>
  <StatusBar barStyle="dark-content"/>
  {Platform.OS==='android'&&<WindowInsetsProbe viewportWidth={viewport.width} viewportHeight={viewport.height} onInsetsChange={event=>{
   const next=calculatePublicInsets(event.nativeEvent);
   if(next)setInsets(current=>Object.keys(next).every(key=>next[key as keyof PublicInsets]===current[key as keyof PublicInsets])?current:next);
  }}/>}
  <Context.Provider value={insets}>
   <View style={[layout.screen,{paddingTop:insets.top,paddingBottom:insets.bottom,paddingLeft:insets.left,paddingRight:insets.right,opacity:insets.ready?1:0}]} pointerEvents={insets.ready?'auto':'none'}>
    {children}
   </View>
  </Context.Provider>
  {!insets.ready&&<View style={layout.loading}><ActivityIndicator color={colors.primary} accessibilityLabel="Preparando pantalla"/></View>}
 </View>;
}
const layout=StyleSheet.create({screen:{flex:1,backgroundColor:colors.bg},loading:{position:'absolute',top:0,right:0,bottom:0,left:0,alignItems:'center',justifyContent:'center'}});
