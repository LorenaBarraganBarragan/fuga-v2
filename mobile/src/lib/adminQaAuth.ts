/** Debug-only transport for the LOCAL simulator. Never contacts the fictitious origin. */
export const ADMIN_QA_ORIGIN='https://admin-qa.invalid';
export const ADMIN_QA_API='http://127.0.0.1:18002';
export const ADMIN_QA_PUBLIC_KEY='sb_publishable_fugaplus_admin_qa';

export function adminQaFetch(nativeFetch:typeof fetch):typeof fetch {
 return async(input,init)=>{
  const raw=typeof input==='string'?input:input instanceof URL?input.href:input.url;
  const url=new URL(raw);
  if(url.origin!==ADMIN_QA_ORIGIN||url.username||url.password||url.hash)throw new Error('QA administrativo: destino no permitido.');
  const method=(init?.method||(typeof input==='object'&&'method' in input?input.method:'GET')).toUpperCase();
  const allowed=(url.pathname==='/auth/v1/token'&&method==='POST'&&['password','refresh_token'].includes(url.searchParams.get('grant_type')||''))
   ||(url.pathname==='/auth/v1/user'&&method==='GET')
   ||(url.pathname==='/auth/v1/logout'&&method==='POST')
   ||(url.pathname==='/auth/v1/settings'&&method==='GET');
  if(!allowed)throw new Error('QA administrativo: operación Auth no disponible.');
  // Supabase Auth supplies URL strings and init. Reject Request objects rather than losing their body.
  if(typeof input!=='string'&&!(input instanceof URL))throw new Error('QA administrativo: solicitud no admitida.');
  return nativeFetch(ADMIN_QA_API+url.pathname+url.search,{...init,redirect:'error'});
 };
}
