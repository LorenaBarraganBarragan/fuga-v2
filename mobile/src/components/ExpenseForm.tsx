import React, { useState } from 'react';
import { Pressable, Text, View } from 'react-native';
import { Category, ExpenseInput } from '../lib/types';
import { localDate } from '../lib/api';
import { expenseError } from '../lib/validation';
import { Button, ErrorText, Field, styles, colors } from './ui';

export function ExpenseForm({categories,initial,busy,onSubmit,onChange}:{categories:Category[];initial:Partial<ExpenseInput>;busy:boolean;onSubmit:(value:ExpenseInput)=>void;onChange?:()=>void}){
 const [amount,setAmount]=useState(initial.monto_cop?.toString()||''),[description,setDescription]=useState(initial.descripcion||'');
 const [date,setDate]=useState(initial.fecha_gasto||localDate()),[category,setCategory]=useState(initial.categoria_id||''),[error,setError]=useState('');
 function changed(){onChange?.();setError('');}
 function submit(){
  const issue=expenseError(amount,description,date,category,categories.map(c=>c.id),localDate());
  if(issue){setError(issue);return;}
  onSubmit({monto_cop:Number(amount),descripcion:description.trim(),fecha_gasto:date,categoria_id:category,moneda:'COP',diccionario_version:initial.diccionario_version||'1.0',reglas_version:initial.reglas_version||'1.0'});
 }
 return <View style={{gap:14}}><Field label="Monto en COP (sin puntos ni centavos)" value={amount} onChangeText={v=>{setAmount(v);changed();}} keyboardType="number-pad"/>
 <Field label="Descripción" value={description} onChangeText={v=>{setDescription(v);changed();}} maxLength={120}/>
 <Field label="Fecha del gasto (YYYY-MM-DD)" value={date} onChangeText={v=>{setDate(v);changed();}} autoCapitalize="none"/>
 <Text style={styles.muted}>Categoría</Text><View style={styles.row}>{categories.map(c=><Pressable key={c.id} accessibilityRole="button" accessibilityState={{selected:category===c.id}} accessibilityLabel={c.nombre} onPress={()=>{setCategory(c.id);changed();}} style={{padding:12,minHeight:48,borderRadius:24,backgroundColor:category===c.id?colors.secondary:'#EEF5F3'}}><Text style={styles.text}>{c.nombre}</Text></Pressable>)}</View>
 <ErrorText message={error}/><Button title={busy?'Guardando…':'Confirmar y guardar gasto'} disabled={busy} onPress={submit}/></View>;
}
