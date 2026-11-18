import { supabase } from './supabase';
import { createApiClient, type RequestOptions } from './request';
import { isApiRoot } from './publicConfig';
export { ApiError } from './request';

let onDenied: (()=>void) | null = null;
export function accountDenied(handler:(()=>void)|null) { onDenied=handler; }
let identity: string | null = null;
let generation = 0;
const pending = new Map<number, 'waiting' | 'retrying'>();
const listeners = new Set<(waiting: boolean) => void>();
export function subscribeApiWaiting(listener: (waiting: boolean) => void) {
  listeners.add(listener); listener(pending.size > 0);
  return () => { listeners.delete(listener); };
}
const client = createApiClient({
  base: () => {
    const value=process.env.EXPO_PUBLIC_API_URL;
    return value&&isApiRoot(value,typeof __DEV__!=='undefined'&&!__DEV__)?value:undefined;
  },
  session: async () => { const {data,error}=await supabase.auth.getSession(); return error?null:data.session; },
  generation: () => generation,
  denied: () => onDenied?.(),
  fetch: (...args) => fetch(...args),
  status: (id,value) => { if(value)pending.set(id,value);else pending.delete(id); for(const listener of listeners)listener(pending.size>0); },
});
export function accountSessionChanged(userId: string | null) {
  if (identity !== userId) { identity=userId; generation++; client.cancelReads(); }
}
export const cancelPendingReads = client.cancelReads;
export function api<T>(path:string, options: RequestOptions = {}):Promise<T> { return client.request<T>(path, options); }
export const money = (n:number) => '$ '+new Intl.NumberFormat('es-CO',{maximumFractionDigits:0}).format(n)+' COP';
export const localDate = () => new Intl.DateTimeFormat('en-CA',{timeZone:'America/Bogota',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
