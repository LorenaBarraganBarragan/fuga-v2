import React,{useEffect,useState} from 'react';
import { Text } from 'react-native';
import { api,localDate,money } from '../lib/api';
import { Leak,LeakDetail } from '../lib/types';
import { Button,Card,ErrorText,Field,Page,Title,styles } from '../components/ui';
import { notifyCandidate, enableNotifications } from '../lib/notifications';

type List={items:Leak[];total:number;estado:string;mensaje_d15:string};
export function Leaks({initialId}:{initialId?:string}){
 const [list,setList]=useState<List|null>(null),[detail,setDetail]=useState<LeakDetail|null>(null),[error,setError]=useState(''),[busy,setBusy]=useState(false);
 const [month,setMonth]=useState(localDate().slice(0,7)),[monthly,setMonthly]=useState<{periodo:string;monto_acumulado_cop:number;cantidad_fugas:number;ocurrencias:number;mensaje:string}|null>(null);
 async function summary(){setBusy(true);setError('');setMonthly(null);try{setMonthly(await api('/leaks/monthly-summary?periodo='+encodeURIComponent(month)));}catch(e){setError((e as Error).message);}finally{setBusy(false);}}
 async function load(){
  setBusy(true);setError('');setDetail(null);
  try{const result=await api<List>('/leaks');setList(result);for(const item of result.items)void notifyCandidate(item).catch(()=>setError('No se pudo mostrar el recordatorio local. El análisis sigue disponible.'));}
  catch(e){setList(null);setError((e as Error).message);}finally{setBusy(false);}
 }
 useEffect(()=>{if(initialId)void open(initialId);else void load();},[initialId]);
 async function open(id:string){
  setBusy(true);setError('');
  try{setDetail(await api<LeakDetail>('/leaks/'+id));}catch(e){setError((e as Error).message);}finally{setBusy(false);}
 }
 return <Page><Title>{detail?'La evidencia, a tu alcance':'Posibles fugas'}</Title><Text style={styles.muted}>Son patrones para revisar, no pérdidas confirmadas. Tú decides cómo interpretarlos.</Text><ErrorText message={error}/>
 {detail?<><Card><Text style={styles.heading}>{detail.fuga.descripcion_normalizada}</Text><Text style={styles.text}>{detail.fuga.regla_codigo} · v{detail.fuga.regla_version}</Text><Text style={styles.text}>Últimos 30 días: al menos 3 gastos entre $1.000 y $30.000 COP, en 3 fechas diferentes, con suma de al menos $15.000 COP.</Text><Text style={styles.text}>{detail.fuga.ocurrencias} ocurrencias · {money(detail.fuga.monto_acumulado_cop)}</Text><Text style={styles.muted}>{detail.fuga.fecha_desde} a {detail.fuga.fecha_hasta}</Text></Card>
 {detail.evidencias.map(g=><Card key={g.id}><Text style={styles.heading}>{g.descripcion}</Text><Text style={styles.text}>{money(g.monto_cop)}</Text><Text style={styles.muted}>{g.fecha_gasto}</Text></Card>)}
 <Button secondary title="Volver a posibles fugas" onPress={()=>setDetail(null)}/></>:<>
 <Button title={busy?'Analizando…':'Actualizar análisis'} disabled={busy} onPress={()=>void load()}/>
 <Field label="Mes del resumen (YYYY-MM)" value={month} onChangeText={setMonth}/><Button secondary title="Resumen mensual de patrones vigentes" disabled={busy} onPress={()=>void summary()}/>
 {monthly&&<Card><Text style={styles.heading}>{monthly.periodo} · {money(monthly.monto_acumulado_cop)}</Text><Text style={styles.text}>{monthly.cantidad_fugas} posibles fugas · {monthly.ocurrencias} gastos</Text><Text style={styles.muted}>{monthly.mensaje}</Text></Card>}
 <Button secondary title="Permitir recordatorios locales" onPress={()=>{void enableNotifications().then(ok=>{if(!ok)setError('Los recordatorios no están disponibles o no tienen permiso. El análisis dentro de la app sigue disponible.');}).catch(()=>setError('Notificaciones locales no disponibles en este entorno.'));}}/>
 {!!list&&<Text style={styles.text}>{list.mensaje_d15}</Text>}
 {list?.items.map(item=><Card key={item.id}><Text style={styles.heading}>{item.descripcion_normalizada}</Text><Text style={styles.text}>{item.categoria_nombre} · {item.ocurrencias} ocurrencias</Text><Text style={styles.text}>{money(item.monto_acumulado_cop)}</Text><Button secondary disabled={busy} title="Revisar evidencia" onPress={()=>void open(item.id)}/></Card>)}</>}
 </Page>;
}
