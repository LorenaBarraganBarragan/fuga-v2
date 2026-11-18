/** Serialize delivery for a candidate; no remote push or background jobs. */
type Reminder = {id: string; categoria_nombre: string; descripcion_normalizada: string; regla_version: string};
type Dependencies = {
  supported: () => boolean;
  permission: () => Promise<boolean>;
  user: () => Promise<string | null>;
  digest: (value: string) => Promise<string>;
  last: (key: string) => Promise<string | null>;
  save: (key: string, value: string) => Promise<void>;
  allowed: (last: number, now: Date) => boolean;
  deliver: (leak: Reminder, userId: string, identifier: string) => Promise<void>;
  now: () => Date;
};
export function createReminderDispatcher(deps: Dependencies) {
  const running = new Map<string, Promise<'sent' | 'skipped'>>();
  return async (leak: Reminder): Promise<'sent' | 'skipped'> => {
    if (!deps.supported()) return 'skipped';
    const userId = await deps.user();
    if (!userId) return 'skipped';
    const group = await deps.digest(leak.categoria_nombre + '|' + leak.descripcion_normalizada + '|' + leak.regla_version);
    const key = 'alert.' + userId + '.' + group;
    const prior = running.get(key);
    if (prior) return prior;
    const task = (async (): Promise<'sent' | 'skipped'> => {
      if (!await deps.permission()) return 'skipped';
      const stored = Number(await deps.last(key) || 0);
      const last = Number.isFinite(stored) && stored >= 0 ? stored : 0;
      const now = deps.now();
      if (!deps.allowed(last, now) || await deps.user() !== userId) return 'skipped';
      // A stable OS identifier also replaces rather than stacks an accidental duplicate.
      const identifier = 'pattern.' + await deps.digest(key);
      if (await deps.user() !== userId) return 'skipped';
      const deliveryTime = deps.now();
      if (!deps.allowed(last, deliveryTime)) return 'skipped';
      await deps.deliver(leak, userId, identifier);
      await deps.save(key, String(deliveryTime.getTime()));
      return 'sent';
    })().catch(() => { throw new Error('No se pudo mostrar el recordatorio local. El análisis sigue disponible.'); });
    running.set(key, task);
    try { return await task; }
    catch { throw new Error('No se pudo mostrar el recordatorio local. El análisis sigue disponible.'); }
    finally { if (running.get(key) === task) running.delete(key); }
  };
}
