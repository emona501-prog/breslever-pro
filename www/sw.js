// ברסלב PRO – service worker: התקנה למסך הבית, התראות, ועבודה בלי אינטרנט באתר (אייפון / דפדפן).
// כל ספר שנפתח פעם אחת נשמר במכשיר; העמוד הראשי – מהרשת כשיש, ומהמטמון כשאין.
// באפליקציה המותקנת (localhost) לא שומרים כלום – הספרים כבר בתוך האפליקציה.
const C = 'bpro-v1';
const WEB = location.protocol === 'https:' && location.hostname !== 'localhost';
self.addEventListener('install', e => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', e => {
  if (!WEB) return;
  const r = e.request;
  if (r.method !== 'GET') return;
  const u = new URL(r.url);
  if (u.origin !== location.origin) return;
  const p = u.pathname;
  // קבצי ספרים / ספריות / תמונות – השם כולל חתימה, לא משתנים: קודם מהמכשיר
  if (/\/(data|lib)\/|\.(png|mp3|json)$/.test(p) && !/version\.json$/.test(p)) {
    e.respondWith(caches.open(C).then(async c => {
      const hit = await c.match(r);
      if (hit) return hit;
      const res = await fetch(r);
      if (res.ok) {
        // גרסה ישנה של אותו ספר (b12_V14.<hash>.json) – מוחקים
        const m = /\/data\/([^/.]+)\.[0-9a-f]+\.json$/.exec(p);
        if (m) (await c.keys()).forEach(k => { const q = new URL(k.url).pathname; q !== p && q.indexOf('/data/' + m[1] + '.') >= 0 && c.delete(k); });
        c.put(r, res.clone());
      }
      return res;
    }));
    return;
  }
  // העמוד עצמו – מהרשת (כדי לקבל עדכונים), ובלי אינטרנט – מהמכשיר
  if (r.mode === 'navigate' || /\.html$|\/$/.test(p)) {
    e.respondWith(fetch(r).then(res => {
      if (res.ok) { const k = res.clone(); caches.open(C).then(c => c.put(r.mode === 'navigate' ? new Request(u.origin + p) : r, k)); }
      return res;
    }).catch(() => caches.open(C).then(c => c.match(r.mode === 'navigate' ? new Request(u.origin + p) : r, { ignoreSearch: true })).then(h => h || Response.error())));
  }
});
