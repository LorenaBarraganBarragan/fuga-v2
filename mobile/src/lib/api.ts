import { supabase } from './supabase';

export class ApiError extends Error {
  constructor(message:string, public status:number, public code:string) { super(message); }
}
let onDenied: (()=>void) | null = null;
export function accountDenied(handler:(()=>void)|null) { onDenied=handler; }
export async function api<T>(path:string, options: {method?:string; body?:unknown; key?:string} = {}):Promise<T> {
  const base = process.env.EXPO_PUBLIC_API_URL;
  if (!base) throw new Error('Configura EXPO_PUBLIC_API_URL para conectar la API.');
  const {data:{session},error} = await supabase.auth.getSession();
  if (error || !session) throw new Error('Inicia sesión para continuar.');
  const controller = new AbortController();
  const timeout = setTimeout(()=>controller.abort(),15000);
  try {
    const response = await fetch(base.replace(/\/$/,'')+'/api/v1'+path,{
      method:options.method || 'GET', signal:controller.signal,
      headers:{ Authorization:'Bearer '+session.access_token, 'Content-Type':'application/json', ...(options.key ? {'Idempotency-Key':options.key}: {}) },
      body:options.body === undefined ? undefined : JSON.stringify(options.body),
    });
    if (response.status === 204) return undefined as T;
    const payload = await response.json();
    if (!response.ok) {
      const code = payload.error?.code || 'REQUEST_ERROR';
      if (response.status === 401 || code === 'ACCOUNT_DISABLED') onDenied?.();
      throw new ApiError(payload.error?.message || 'No se pudo completar la solicitud.',response.status,code);
    }
    return payload as T;
  } catch (error) {
    if (error instanceof ApiError) throw error;
    throw new Error('No fue posible conectar con el servidor. Revisa tu conexión y vuelve a intentar.');
  } finally { clearTimeout(timeout); }
}
export const money = (n:number) => '$ '+new Intl.NumberFormat('es-CO',{maximumFractionDigits:0}).format(n)+' COP';
export const localDate = () => new Intl.DateTimeFormat('en-CA',{timeZone:'America/Bogota',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
