/** Client keys are public credentials, never service-role or secret keys. */
export function isPublicSupabaseKey(key: string): boolean {
  if (/^sb_publishable_[A-Za-z0-9_-]+$/.test(key)) return true;
  if (key.startsWith('sb_secret_')) return false;
  try {
    const payload = key.split('.')[1];
    if (!payload || key.split('.').length !== 3) return false;
    const normalized = payload.replace(/-/g, '+').replace(/_/g, '/');
    const parsed = JSON.parse(atob(normalized.padEnd(Math.ceil(normalized.length / 4) * 4, '=')));
    return parsed.role === 'anon';
  } catch { return false; }
}
export function isSupabaseRoot(value: string): boolean {
  try {
    const url = new URL(value);
    return url.protocol === 'https:' && !!url.hostname && !url.username && !url.password && !url.search && !url.hash && ['','/'].includes(url.pathname);
  } catch { return false; }
}
export function isApiRoot(value: string, production: boolean): boolean {
  try {
    const url = new URL(value);
    return (url.protocol === 'https:' || (!production && url.protocol === 'http:')) && !!url.hostname && !url.username && !url.password && !url.search && !url.hash && ['','/'].includes(url.pathname);
  } catch { return false; }
}
