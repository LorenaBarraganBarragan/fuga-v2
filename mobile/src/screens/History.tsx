import React,{useEffect,useState} from 'react';
import { Text,View } from 'react-native';
import { api,money } from '../lib/api';
import { Category,Expense,ExpenseInput } from '../lib/types';
import { Button,Card,Confirmation,ErrorText,Field,Page,Title,styles } from '../components/ui';
import { ExpenseForm } from '../components/ExpenseForm';

type List={items:Expense[];next_cursor:string|null;has_more:boolean};
export function History({onDirty}:{onDirty:(dirty:boolean)=>void}){
 const [items,setItems]=useState<Expense[]>([]),[cursor,setCursor]=useState<string|null>(null),[categories,setCategories]=useState<Category[]>([]);
 const [from,setFrom]=useState(''),[to,setTo]=useState(''),[cat,setCat]=useState('');
 const [editing,setEditing]=useState<Expense|null>(null),[deleting,setDeleting]=useState<Expense|null>(null),[discard,setDiscard]=useState(false);
 const [busy,setBusy]=useState(false),[error,setError]=useState('');
 const [applied,setApplied]=useState('');
 function query(){
  const q=new URLSearchParams();
  if(from)q.set('desde',from);if(to)q.set('hasta',to);if(cat)q.set('categoria_id',cat);
  return q.toString();
 }
 async function load(more=false,filter=applied){
  setBusy(true);setError('');
  try{
   const q=new URLSearchParams(filter);q.set('limit','20');if(more&&cursor)q.set('cursor',cursor);
   const result=await api<List>('/expenses?'+q);
   setItems(old=>more?[...old,...result.items]:result.items);setCursor(result.next_cursor);
  }catch(e){setError((e as Error).message);}finally{setBusy(false);}
 }
 useEffect(()=>{void load();api<Category[]>('/categories').then(setCategories).catch(e=>setError(e.message));return()=>onDirty(false);},[]);
 async function save(body:ExpenseInput){
  if(!editing)return;setBusy(true);setError('');
  try{await api('/expenses/'+editing.id,{method:'PUT',body});setEditing(null);onDirty(false);await load();}
  catch(e){setError((e as Error).message);}finally{setBusy(false);}
 }
 async function remove(){
  if(!deleting)return;setBusy(true);setError('');
  try{await api('/expenses/'+deleting.id,{method:'DELETE'});setDeleting(null);await load();}
  catch(e){setError((e as Error).message);setDeleting(null);}finally{setBusy(false);}
 }
 return <Page><Title>{editing?'Editar gasto':'Tu historial'}</Title><ErrorText message={error}/>
 {editing?<><ExpenseForm key={editing.id} categories={categories} initial={editing} busy={busy} onChange={()=>onDirty(true)} onSubmit={body=>void save(body)}/><Button secondary title="Cancelar edición" disabled={busy} onPress={()=>setDiscard(true)}/></>:<>
 <Text style={styles.muted}>Más recientes primero. Filtra por fecha o categoría.</Text>
 <Field label="Desde (YYYY-MM-DD, opcional)" value={from} onChangeText={setFrom}/>
 <Field label="Hasta (YYYY-MM-DD, opcional)" value={to} onChangeText={setTo}/>
 <View style={styles.row}><Button title="Todas" secondary onPress={()=>setCat('')}/>{categories.map(c=><Button key={c.id} title={(cat===c.id?'✓ ':'')+c.nombre} secondary onPress={()=>setCat(c.id)}/>)}</View>
 <Button title="Aplicar filtros" disabled={busy} onPress={()=>{const filter=query();setApplied(filter);void load(false,filter);}}/>
 <Button secondary title="Actualizar" disabled={busy} onPress={()=>void load()}/>
 {!busy&&!items.length&&<Card><Text style={styles.text}>No hay gastos para estos filtros.</Text></Card>}
 {items.map(item=><Card key={item.id}><Text style={styles.heading}>{item.descripcion}</Text><Text style={styles.text}>{money(item.monto_cop)}</Text><Text style={styles.muted}>{item.fecha_gasto} · {item.categoria_nombre}</Text><View style={styles.row}><Button secondary title="Editar" disabled={busy} onPress={()=>setEditing(item)}/><Button secondary title="Eliminar" disabled={busy} onPress={()=>setDeleting(item)}/></View></Card>)}
 {!!cursor&&<Button title="Cargar más" disabled={busy} onPress={()=>void load(true)}/>}</>}
 <Confirmation visible={!!deleting} title="Eliminar gasto" message="El gasto dejará de aparecer en tu historial, estadísticas y posibles fugas." onCancel={()=>setDeleting(null)} onConfirm={()=>void remove()}/>
 <Confirmation visible={discard} title="Descartar cambios" message="Los cambios sin guardar se perderán." onCancel={()=>setDiscard(false)} onConfirm={()=>{setDiscard(false);setEditing(null);onDirty(false);}}/>
 </Page>;
}
