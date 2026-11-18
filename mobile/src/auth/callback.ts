/** PKCE callbacks shared by web and native; no SDK or React Native side effects. */
export const AUTH_LINK_ERROR = 'El enlace es inválido o venció. Solicita uno nuevo desde este navegador o dispositivo.';
export const WEB_CALLBACK_PATH = '/auth/callback';

export type CallbackContext = { platform: 'web' | 'native'; origin?: string };
type ExchangeResult = { error: unknown; data: { session: unknown; redirectType?: string | null } };
type StorageLike = Pick<Storage, 'getItem' | 'setItem' | 'removeItem'>;

export function authRedirectUrl(context: CallbackContext, recovery = false): string {
  let target = 'fugaplus://auth';
  if (context.platform === 'web') {
    const origin = new URL(context.origin || '');
    if (!['http:', 'https:'].includes(origin.protocol) || origin.username || origin.password) {
      throw new Error(AUTH_LINK_ERROR);
    }
    target = origin.origin + WEB_CALLBACK_PATH;
  }
  return target + (recovery ? '?flow=recovery' : '');
}

export function parseAuthCallback(raw: string, context: CallbackContext): URL | null {
  try {
    const url = new URL(raw);
    if (url.username || url.password) return null;
    if (context.platform === 'web') {
      if (!['http:', 'https:'].includes(url.protocol) || url.origin !== context.origin || url.pathname !== WEB_CALLBACK_PATH) return null;
    } else if (url.protocol !== 'fugaplus:' || url.hostname !== 'auth' || url.port || !['', '/'].includes(url.pathname)) {
      return null;
    }
    return url;
  } catch {
    return null;
  }
}

export function createAuthCallbackHandler(exchange: (code: string, options?: { flowId: string }) => Promise<ExchangeResult>) {
  const running = new Map<string, Promise<boolean>>();
  const completed = new Map<string, boolean>();
  return async function handle(raw: string, context: CallbackContext): Promise<boolean> {
    const url = parseAuthCallback(raw, context);
    if (!url) return false;
    const fragment = new URLSearchParams(url.hash.slice(1));
    const failed = ['error', 'error_code', 'error_description'].some(name => url.searchParams.has(name) || fragment.has(name));
    const code = url.searchParams.get('code');
    const flowId = url.searchParams.get('sb_flow_id');
    if (failed || fragment.has('access_token') || fragment.has('refresh_token') || !code?.trim() || url.searchParams.getAll('code').length !== 1) {
      throw new Error(AUTH_LINK_ERROR);
    }
    if (url.searchParams.has('sb_flow_id') && (!flowId || !/^[a-zA-Z0-9_-]{8,64}$/.test(flowId) || url.searchParams.getAll('sb_flow_id').length !== 1)) {
      throw new Error(AUTH_LINK_ERROR);
    }
    if (completed.has(code)) return completed.get(code)!;
    let operation = running.get(code);
    if (!operation) {
      operation = (async () => {
        try {
          const result = await exchange(code, flowId ? { flowId } : undefined);
          if (result.error || !result.data.session) throw new Error(AUTH_LINK_ERROR);
          const recovery = result.data.redirectType === 'recovery' || url.searchParams.get('flow') === 'recovery';
          completed.set(code, recovery);
          if (completed.size > 10) completed.delete(completed.keys().next().value!);
          return recovery;
        } catch {
          // Provider errors can contain codes or other sensitive context.
          throw new Error(AUTH_LINK_ERROR);
        }
      })();
      running.set(code, operation);
    }
    try {
      return await operation;
    } finally {
      if (running.get(code) === operation) running.delete(code);
    }
  };
}

/** Only clean the callback being consumed; never redirect to a URL from query parameters. */
export function cleanCallbackTarget(raw: string, current: string): string | null {
  try {
    const url = new URL(current);
    if (new URL(raw).href !== url.href || !parseAuthCallback(raw, { platform: 'web', origin: url.origin })) return null;
    return url.origin + '/';
  } catch {
    return null;
  }
}

/** Persist the PKCE verifier across an email link opened in another tab of the same browser. */
export function createWebAuthStorage(getStorage: () => StorageLike | null) {
  return {
    async getItem(name: string) { return getStorage()?.getItem(name) ?? null; },
    async setItem(name: string, value: string) { getStorage()?.setItem(name, value); },
    async removeItem(name: string) { getStorage()?.removeItem(name); },
  };
}
