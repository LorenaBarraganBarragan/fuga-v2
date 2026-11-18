import React,{useEffect,useState} from 'react';
import { Text,View } from 'react-native';
import { api,localDate,money } from '../lib/api';
import { Breakdown,Summary } from '../lib/types';
import { Button,Card,ErrorText,Field,Page,Title,styles,colors } from '../components/ui';

type Comparison={actual:Summary;anterior:Summary|null;diferencia_cop:number|null;variacion_porcentaje:number|null;mensaje:string|null};
export function Dashboard(){
 const [period,setPeriod]=useState(localDate().slice(0,7)),[summary,setSummary]=useState<Summary|null>(null),[breakdown,setBreakdown]=useState<Breakdown|null>(null),[comparison,setComparison]=useState<Comparison|null>(null);
 const [error,setError]=useState(''),[busy,setBusy]=useState(false);
 async function load(){
  setBusy(true);setError('');setSummary(null);setBreakdown(null);setComparison(null);
  try{
   const q='?periodo='+encodeURIComponent(period);
   const [s,b]=await Promise.all([api<Summary>('/analytics/summary'+q),api<Breakdown>('/analytics/by-category'+q)]);
   setSummary(s);setBreakdown(b);
  }catch(e){setError((e as Error).message);}finally{setBusy(false);}
 }
 useEffect(()=>{void load();},[]);
 async function compare(){
  if(!summary)return;
  setBusy(true);setError('');
  try{setComparison(await api<Comparison>('/analytics/comparison?periodo='+encodeURIComponent(summary.periodo)));}
  catch(e){setError((e as Error).message);}finally{setBusy(false);}
 }
 return <Page><Text style={styles.muted}>TU DINERO, CON CLARIDAD</Text><Title>Tu mes en perspectiva</Title><Field label="Mes (YYYY-MM)" value={period} onChangeText={setPeriod}/><Button title={busy?'Consultando…':'Consultar / actualizar'} disabled={busy} onPress={()=>void load()}/><ErrorText message={error}/>
 {summary&&<><Card><Text style={styles.muted}>Total · {summary.periodo}</Text><Text style={[styles.title,{fontSize:32}]}>{money(summary.monto_total_cop)}</Text><Text style={styles.text}>{summary.cantidad_gastos} gastos · Promedio {money(summary.promedio_gasto_cop)}</Text>{summary.cantidad_gastos===0&&<Text style={styles.muted}>Sin datos para este periodo.</Text>}</Card>
 <Title>Por categoría</Title>{breakdown?.categorias_mayor_gasto.length ? <Text style={styles.text}>{breakdown.categorias_mayor_gasto.length>1?'Empate en mayor gasto: ':'Mayor gasto: '}{breakdown.categorias_mayor_gasto.join(', ')}</Text>:null}
 {breakdown?.items.map(item=><Card key={item.categoria_id}><Text style={styles.heading}>{item.categoria_nombre}</Text><Text style={styles.text}>{money(item.monto_cop)} · {item.porcentaje.toFixed(1)}%</Text><View accessibilityLabel={item.porcentaje+' por ciento'} style={{height:8,backgroundColor:'#EEF5F3',borderRadius:4}}><View style={{height:8,width:(Math.min(100,item.porcentaje)+'%') as `${number}%`,backgroundColor:colors.primary,borderRadius:4}}/></View></Card>)}
 <Button secondary title="Comparar con el mes anterior" disabled={busy} onPress={()=>void compare()}/>
 {comparison&&<Card><Text style={styles.heading}>Frente al mes anterior</Text><Text style={styles.text}>{comparison.anterior?.periodo||'Sin periodo anterior'}</Text><Text style={styles.text}>{comparison.diferencia_cop!==null?money(comparison.diferencia_cop):'Sin base de comparación'}</Text><Text style={styles.muted}>{comparison.variacion_porcentaje===null?'Sin base de comparación':comparison.variacion_porcentaje.toFixed(1)+'%'}</Text></Card>}</>}
 </Page>;
}
