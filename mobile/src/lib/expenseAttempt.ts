/** One UUID per confirmed payload and owner; transient draft only, never persisted. */
export function createExpenseAttempt(uuid: () => string) {
  let attempt = {owner: '', payload: '', key: ''};
  return {
    prepare(owner: string, body: object) {
      const payload = JSON.stringify(body, Object.keys(body).sort());
      if (attempt.owner !== owner || attempt.payload !== payload) attempt = {owner, payload, key: uuid()};
      return attempt.key;
    },
    clear() { attempt = {owner: '', payload: '', key: ''}; },
  };
}
