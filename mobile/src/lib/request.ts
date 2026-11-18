/** Testable HTTP boundary. GET retries are bounded; mutations are never replayed. */
export class ApiError extends Error {
  status: number;
  code: string;
  constructor(message: string, status: number, code: string) {
    super(message);
    this.status = status;
    this.code = code;
  }
}

type Session = {user: {id: string}; access_token: string};
export type RequestOptions = {
  method?: string; body?: unknown; key?: string; signal?: AbortSignal;
};
type Dependencies = {
  base: () => string | undefined;
  session: () => Promise<Session | null>;
  generation: () => number;
  denied: () => void;
  fetch: typeof fetch;
  status: (id: number, value: 'waiting' | 'retrying' | null) => void;
  readTimeout?: number;
  writeTimeout?: number;
  waitNotice?: number;
  retryDelay?: number;
};

const NETWORK_ERROR = 'No fue posible conectar con el servidor. Revisa tu conexión y vuelve a intentar.';
export function createApiClient(deps: Dependencies) {
  let serial = 0;
  const reads = new Set<AbortController>();
  function cancelReads() { for (const controller of reads) controller.abort(); }
  async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
    const base = deps.base();
    if (!base) throw new Error('Configura EXPO_PUBLIC_API_URL para conectar la API.');
    const method = (options.method || 'GET').toUpperCase();
    const read = method === 'GET' || method === 'HEAD';
    const boundary = deps.generation();
    const initial = await deps.session();
    if (!initial || boundary !== deps.generation()) throw new ApiError('Inicia sesión para continuar.', 401, 'SESSION_CHANGED');
    const userId = initial.user.id;
    const id = ++serial;
    const cancellation = new AbortController();
    if (read) reads.add(cancellation);
    const cancel = () => cancellation.abort();
    options.signal?.addEventListener('abort', cancel, {once: true});
    if (options.signal?.aborted) cancel();
    const assertActive = () => {
      if (cancellation.signal.aborted) throw new ApiError('Consulta cancelada.', 0, 'CANCELLED');
      if (boundary !== deps.generation()) throw new ApiError('La sesión cambió. Vuelve a consultar.', 401, 'SESSION_CHANGED');
    };
    try {
      const attempts = read ? 2 : 1;
      for (let attempt = 0; attempt < attempts; attempt++) {
        assertActive();
        const session = await deps.session();
        assertActive();
        if (!session || session.user.id !== userId) throw new ApiError('La sesión cambió. Vuelve a consultar.', 401, 'SESSION_CHANGED');
        const controller = new AbortController();
        const abort = () => controller.abort();
        cancellation.signal.addEventListener('abort', abort, {once: true});
        const timeout = setTimeout(abort, read ? (deps.readTimeout ?? 45000) : (deps.writeTimeout ?? 15000));
        const notice = setTimeout(() => deps.status(id, attempt ? 'retrying' : 'waiting'), deps.waitNotice ?? 3000);
        let retry = false;
        try {
          const response = await deps.fetch(base.replace(/\/$/, '') + '/api/v1' + path, {
            method, signal: controller.signal,
            headers: {Authorization: 'Bearer ' + session.access_token, 'Content-Type': 'application/json', ...(options.key ? {'Idempotency-Key': options.key} : {})},
            body: options.body === undefined ? undefined : JSON.stringify(options.body),
          });
          assertActive();
          if (read && [502, 503, 504].includes(response.status) && attempt + 1 < attempts) {
            await response.body?.cancel();
            retry = true;
          } else {
            if (response.status === 204) return undefined as T;
            const payload = await response.json();
            assertActive();
            if (!response.ok) {
              const code = payload.error?.code || 'REQUEST_ERROR';
              if (response.status === 401 || code === 'ACCOUNT_DISABLED') deps.denied();
              throw new ApiError(payload.error?.message || 'No se pudo completar la solicitud.', response.status, code);
            }
            return payload as T;
          }
        } catch (error) {
          assertActive();
          if (error instanceof ApiError) throw error;
          if (read && attempt + 1 < attempts) retry = true;
          else throw new Error(NETWORK_ERROR);
        } finally {
          clearTimeout(timeout);
          clearTimeout(notice);
          cancellation.signal.removeEventListener('abort', abort);
        }
        if (retry) {
          deps.status(id, 'retrying');
          await new Promise<void>((resolve, reject) => {
            const stop = () => { clearTimeout(timer); reject(new ApiError('Consulta cancelada.', 0, 'CANCELLED')); };
            const timer = setTimeout(() => { cancellation.signal.removeEventListener('abort', stop); resolve(); }, deps.retryDelay ?? 1000);
            cancellation.signal.addEventListener('abort', stop, {once: true});
            if (cancellation.signal.aborted) stop();
          });
        }
      }
      throw new Error(NETWORK_ERROR);
    } finally {
      deps.status(id, null);
      reads.delete(cancellation);
      options.signal?.removeEventListener('abort', cancel);
    }
  }
  return {request, cancelReads};
}
