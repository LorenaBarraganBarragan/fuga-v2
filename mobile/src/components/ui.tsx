import React, { ReactNode } from 'react';
import { ActivityIndicator, Modal, Pressable, ScrollView, StyleSheet, Text, TextInput, TextInputProps, View } from 'react-native';

export const colors={primary:'#1A5B5A',secondary:'#A2E8D3',tertiary:'#F5A623',text:'#243332',muted:'#5A6E6C',bg:'#F7FAF9',border:'#D7E3E0',error:'#B3261E'};
export const styles=StyleSheet.create({
 page:{flexGrow:1,padding:24,gap:16,backgroundColor:colors.bg},
 title:{fontSize:28,lineHeight:36,fontWeight:'700',color:colors.primary,fontFamily:'PlusJakartaSans_700Bold'},
 heading:{fontSize:20,lineHeight:28,fontWeight:'600',color:colors.text},
 text:{fontSize:16,lineHeight:24,color:colors.text,fontFamily:'PlusJakartaSans_400Regular'},
 muted:{fontSize:14,lineHeight:21,color:colors.muted},
 card:{padding:18,borderRadius:18,backgroundColor:'#fff',borderWidth:1,borderColor:colors.border,gap:10},
 row:{flexDirection:'row',flexWrap:'wrap',gap:8,alignItems:'center'},
 input:{minHeight:48,borderWidth:1,borderColor:colors.border,borderRadius:12,padding:12,fontSize:16,color:colors.text,backgroundColor:'#fff'},
 button:{minHeight:48,padding:14,borderRadius:12,alignItems:'center',justifyContent:'center',backgroundColor:colors.primary},
 buttonText:{color:'#fff',fontWeight:'600',fontSize:16},
 error:{color:colors.error,fontSize:15,lineHeight:22},
});
export function Page({children}:{children:ReactNode}) { return <ScrollView contentContainerStyle={styles.page} keyboardShouldPersistTaps="handled">{children}</ScrollView>; }
export function Title({children}:{children:ReactNode}) { return <Text accessibilityRole="header" style={styles.title}>{children}</Text>; }
export function Card({children}:{children:ReactNode}) { return <View style={styles.card}>{children}</View>; }
export function Button({title,onPress,disabled=false,secondary=false}:{title:string;onPress:()=>void;disabled?:boolean;secondary?:boolean}) {
 return <Pressable accessibilityRole="button" accessibilityLabel={title} accessibilityState={{disabled}} disabled={disabled} onPress={onPress} style={[styles.button,secondary&&{backgroundColor:'#D8F6EC'},disabled&&{opacity:0.5}]}><Text style={[styles.buttonText,secondary&&{color:colors.primary}]}>{title}</Text></Pressable>;
}
export function Field({label,...props}:TextInputProps & {label:string}) { return <View style={{gap:6}}><Text style={styles.muted}>{label}</Text><TextInput accessibilityLabel={label} {...props} style={[styles.input,props.style]}/></View>; }
export function ErrorText({message}:{message:string}) { return message ? <Text accessibilityRole="alert" style={styles.error}>{message}</Text> : null; }
export function Busy() { return <ActivityIndicator size="large" color={colors.primary} accessibilityLabel="Cargando"/>; }
export function Confirmation({visible,title,message,onCancel,onConfirm}:{visible:boolean;title:string;message:string;onCancel:()=>void;onConfirm:()=>void}) {
 return <Modal visible={visible} transparent animationType="fade" onRequestClose={onCancel}><View style={{flex:1,backgroundColor:'#0008',justifyContent:'center',padding:24}}><Card><Title>{title}</Title><Text style={styles.text}>{message}</Text><Button title="Confirmar" onPress={onConfirm}/><Button title="Cancelar" secondary onPress={onCancel}/></Card></View></Modal>;
}
