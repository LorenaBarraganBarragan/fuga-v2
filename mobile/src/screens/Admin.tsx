import React,{useEffect,useState} from 'react';
import { Text,View } from 'react-native';
import { api } from '../lib/api';
import { Button,Card,Confirmation,ErrorText,Field,Page,Title,styles } from '../components/ui';

type Account={id:string;nombres:string|null;apellido:string|null;email:string;rol:string;disabled_at:string|null;created_at:string;auth_sync_pendiente:boolean};
type Stats={registrados:number;activos:number;inactivos:number;actividad_mensual:{periodo:string;usuarios_activos:number}[]};
export function Admin(){
 const [items,setItems]=useState<Account[]>([]),[stats,setStats]=useState<Stats|null>(null),[q,setQ]=useState(''),[filter,setFilter]=useState<'all'|'active'|'inactive'>('all');
 const [page,setPage]=useState(1),[hasMore,setHasMore]=useState(false),[selected,setSelected]=useState<Account|null>(null),[change,setChange]=useState(false);
 const [busy,setBusy]=useState(false),[error,setError]=useState('');
 async function load(p=1){
  setBusy(true);setError('');
  try{
   const params=new URLSearchParams({q,page:String(p)});
   if(filter!=='all')params.set('activo',String(filter==='active'));
   const [users,s]=await Promise.all([api<{items:Account[];has_more:boolean}>('/admin/users?'+params),api<Stats>('/admin/stats')]);
   setItems(users.items);setHasMore(users.has_more);setPage(p);setStats(s);
  }catch(e){setError((e as Error).message);}finally{setBusy(false);}
 }
 useEffect(()=>{void load();},[]);
 async function open(id:string){
  setBusy(true);setError('');
  try{setSelected(await api<Account>('/admin/users/'+id));}catch(e){setError((e as Error).message);}finally{setBusy(false);}
 }
 async function state(){
  if(!selected)return;setBusy(true);setError('');setChange(false);
  try{
   await api('/admin/users/'+selected.id+'/state',{method:'PATCH',body:{activo:!!selected.disabled_at}});
   setSelected(null);await load(page);
  }catch(e){setError((e as Error).message);await open(selected.id);}finally{setBusy(false);}
 }
 return <Page><Title>Administración</Title><Text style={styles.muted}>Solo metadatos de cuentas. Sin gastos individuales ni evidencia financiera.</Text><ErrorText message={error}/>
 {selected?<><Card><Text style={styles.heading}>{selected.nombres||'Sin nombre'} {selected.apellido}</Text><Text style={styles.text}>{selected.email}</Text><Text style={styles.muted}>ID: {selected.id}</Text><Text style={styles.text}>Rol: {selected.rol} · {selected.disabled_at?'Inactiva':'Activa'}</Text><Text style={styles.muted}>Registro: {selected.created_at.slice(0,10)}</Text>{selected.auth_sync_pendiente&&<Text style={styles.error}>Sincronización con Supabase pendiente.</Text>}</Card>
 {selected.rol!=='administrador'&&<Button title={selected.disabled_at?'Activar cuenta':'Desactivar cuenta'} disabled={busy} onPress={()=>setChange(true)}/>}
 <Button secondary title="Volver al listado" onPress={()=>setSelected(null)}/></>:<>
 {stats&&<Card><Text style={styles.heading}>{stats.registrados} cuentas registradas</Text><Text style={styles.text}>{stats.activos} activas · {stats.inactivos} inactivas</Text>{stats.actividad_mensual.length===0&&<Text style={styles.muted}>Sin actividad registrada.</Text>}{stats.actividad_mensual.map(m=><View key={m.periodo} style={{gap:4}}><Text style={styles.muted}>{m.periodo.slice(0,7)} · {m.usuarios_activos} usuarios activos únicos</Text><View accessibilityLabel={m.usuarios_activos+' usuarios activos en '+m.periodo.slice(0,7)} style={{height:10,borderRadius:5,backgroundColor:'#EEF5F3'}}><View style={{height:10,borderRadius:5,backgroundColor:'#1A5B5A',width:(100*m.usuarios_activos/Math.max(1,...stats.actividad_mensual.map(x=>x.usuarios_activos))+'%') as `${number}%`}}/></View></View>)}</Card>}
 <Field label="Buscar por nombre o correo" value={q} onChangeText={setQ}/>
 <View style={styles.row}>{(['all','active','inactive'] as const).map((value,i)=><Button key={value} secondary title={(filter===value?'✓ ':'')+['Todas','Activas','Inactivas'][i]} onPress={()=>setFilter(value)}/>)}</View>
 <Button title="Buscar / actualizar" disabled={busy} onPress={()=>void load()}/>
 {!busy&&!items.length&&<Text style={styles.text}>Sin coincidencias.</Text>}
 {items.map(item=><Card key={item.id}><Text style={styles.heading}>{item.nombres||'Sin nombre'} {item.apellido}</Text><Text style={styles.text}>{item.email}</Text><Text style={styles.muted}>{item.rol} · {item.disabled_at?'Inactiva':'Activa'}</Text><Button secondary title="Ver cuenta" disabled={busy} onPress={()=>void open(item.id)}/></Card>)}
 <View style={styles.row}>{page>1&&<Button title="Anterior" disabled={busy} onPress={()=>void load(page-1)}/>}<Text style={styles.muted}>Página {page}</Text>{hasMore&&<Button title="Siguiente" disabled={busy} onPress={()=>void load(page+1)}/>}</View></>}
 <Confirmation visible={change} title={selected?.disabled_at?'Activar cuenta':'Desactivar cuenta'} message="La operación modifica el acceso y deja un registro de auditoría. No borra gastos." onCancel={()=>setChange(false)} onConfirm={()=>void state()}/>
 </Page>;
}
