import React,{useEffect,useRef} from 'react';
import {KeyboardAvoidingView,Platform,ScrollView,StyleSheet} from 'react-native';
import {PublicSafeArea,usePublicInsets} from './PublicSafeArea';
import {styles} from './ui';

function FormScroll({children,feedback}:{children:React.ReactNode;feedback:string}){
 const scroll=useRef<React.ElementRef<typeof ScrollView>>(null),focused=useRef<number|null>(null);
 const insets=usePublicInsets();
 function revealFocused(){
  if(Platform.OS!=='android'||!insets.keyboardVisible||focused.current===null)return;
  scroll.current?.scrollResponderScrollNativeHandleToKeyboard(focused.current,16,true);
 }
 useEffect(()=>{
  if(!insets.keyboardVisible)return;
  const frame=requestAnimationFrame(revealFocused);
  return()=>cancelAnimationFrame(frame);
 },[insets.keyboardVisible,insets.bottom]);
 useEffect(()=>{
  if(!feedback)return;
  const frame=requestAnimationFrame(()=>scroll.current?.scrollToEnd({animated:true}));
  return()=>cancelAnimationFrame(frame);
 },[feedback]);
 const content=<ScrollView ref={scroll} style={layout.fill} contentContainerStyle={styles.page}
  keyboardShouldPersistTaps="handled" keyboardDismissMode="on-drag" automaticallyAdjustKeyboardInsets={false}
  onFocus={event=>{focused.current=event.nativeEvent.target;revealFocused();}}>
  {children}
 </ScrollView>;
 return Platform.OS==='ios'?<KeyboardAvoidingView style={layout.fill} behavior="padding">{content}</KeyboardAvoidingView>:content;
}

export function PublicFormPage({children,feedback=''}:{children:React.ReactNode;feedback?:string}){
 return <PublicSafeArea><FormScroll feedback={feedback}>{children}</FormScroll></PublicSafeArea>;
}
const layout=StyleSheet.create({fill:{flex:1}});
