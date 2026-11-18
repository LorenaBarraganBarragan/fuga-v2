import React, { useEffect, useRef, useState } from 'react';
import { Text, View } from 'react-native';
import * as Crypto from 'expo-crypto';
import { api, money } from '../lib/api';
import { Category, Draft, Expense, ExpenseInput } from '../lib/types';
import { Button, Card, Confirmation, ErrorText, Field, Page, Title, styles } from '../components/ui';
import { ExpenseForm } from '../components/ExpenseForm';
import { VoiceInput } from '../voice/VoiceInput';

export function NewExpense({onDirty}:{onDirty:(dirty:boolean)=>void}){
 const [text,setText]=useState(''),[draft,setDraft]=useState<Draft|null>(null),[categories,setCategories]=useState<Category[]>([]);
 const [busy,setBusy]=useState(false),[error,setError]=useState(''),[saved,setSaved]=useState<Expense|null>(null),[discard,setDiscard]=useState(false);
 const attempt=useRef({payload:'',key:''});
 async function load(){try{setCategories(await api<Category[]>('/categories'));setError('');}catch(e){setError((e as Error).message);}}
 useEffect(()=>{void load();return()=>onDirty(false);},[]);
 async function process(){
  if(!text.trim()||text.trim().length>280){setError('Escribe entre 1 y 280 caracteres.');return;}
  setBusy(true);setError('');setSaved(null);
  try{setDraft(await api<Draft>('/expenses/interpret',{method:'POST',body:{texto:text.trim()}}));onDirty(true);}
  catch(e){setError((e as Error).message);}finally{setBusy(false);}
 }
 async function save(body:ExpenseInput){
  const fingerprint=JSON.stringify(body);
  if(attempt.current.payload!==fingerprint)attempt.current={payload:fingerprint,key:Crypto.randomUUID()};
  setBusy(true);setError('');
  try{
   const result=await api<Expense>('/expenses',{method:'POST',body,key:attempt.current.key});
   setSaved(result);setDraft(null);setText('');onDirty(false);attempt.current={payload:'',key:''};
  }catch(e){setError((e as Error).message);}finally{setBusy(false);}
 }
 return <Page><Title>{draft?'Revisa tu gasto':'Un gasto, en tus palabras'}</Title>
 <Text style={styles.muted}>Interpretación mediante reglas automáticas; no utiliza IA generativa ni envía tu gasto a una IA externa.</Text>
 {!!saved&&<Card><Text accessibilityRole="alert" style={styles.heading}>Gasto guardado</Text><Text style={styles.text}>{saved.descripcion} · {money(saved.monto_cop)}</Text></Card>}
 {!draft?<><Field label="¿En qué gastaste?" multiline value={text} onChangeText={v=>{setText(v);onDirty(!!v.trim());setSaved(null);}} placeholder="Hoy gasté $8.000 en un taxi" maxLength={280} style={{minHeight:120,textAlignVertical:'top'}}/><Text style={styles.muted}>{text.length}/280 caracteres</Text>
 <VoiceInput onTranscript={v=>{setText(v.slice(0,280));onDirty(true);}}/>
 <Button title={busy?'Procesando…':'Procesar con IA'} disabled={busy||!categories.length} onPress={()=>void process()}/></>:<>
 <Card><Text style={styles.muted}>Texto original · solo en esta pantalla</Text><Text style={styles.text}>{text}</Text>{[...draft.avisos,...draft.ambiguedades].map((x,i)=><Text key={i} style={styles.muted}>{x}</Text>)}</Card>
 <ExpenseForm categories={categories} initial={{...draft.draft,monto_cop:draft.draft.monto_cop??undefined,categoria_id:draft.draft.categoria_id??undefined,diccionario_version:draft.diccionario_version,reglas_version:draft.reglas_version}} busy={busy} onSubmit={body=>void save(body)}/>
 <Button secondary title="Descartar borrador" disabled={busy} onPress={()=>setDiscard(true)}/></>}
 <ErrorText message={error}/>{!categories.length&&<Button secondary title="Reintentar cargar categorías" onPress={()=>void load()}/>}
 <Confirmation visible={discard} title="Descartar borrador" message="Los datos sin confirmar se perderán." onCancel={()=>setDiscard(false)} onConfirm={()=>{setDiscard(false);setDraft(null);setText('');onDirty(false);}}/>
 </Page>;
}
