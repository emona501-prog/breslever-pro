p='app.js'; s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:80]); s=s.replace(a,b)
# הגדרת הבהוב סוף זמן
rep('''      '> התראה בתוך האפליקציה כ־15 דקות לפני השקיעה</label><div class="zm-note">' +''','''      '> התראה בתוך האפליקציה כ־15 דקות לפני השקיעה</label><label class="zm-chk"><input type="checkbox" id="zmFl"' +
      (s.get("zmFlash", !1) ? " checked" : "") +
      '> פס מהבהב באדום בדקות האחרונות של סוף זמן קריאת שמע, סוף זמן תפילה, חצות והשקיעה</label><div class="zm-note">' +''')
rep('''    ((l("#zmAl", E).onchange = (t) => {''','''    ((l("#zmFl", E).onchange = (t) => {
      (s.set("zmFlash", t.target.checked), st(t.target.checked ? "בדקות האחרונות של הזמן יופיע פס מהבהב" : "ההבהוב בוטל"), zmFlashTick());
    }),
      (l("#zmAl", E).onchange = (t) => {''')
rep('''  function goZman(t) {''','''  // ⏳ פס מהבהב בדקות האחרונות של זמן (אופציונלי)
  function zmFlashTick() {
    let t = document.getElementById("zmFlashBar");
    const e = () => {
      t && (t.remove(), (t = null));
    };
    if (!s.get("zmFlash", !1)) return e();
    let i = null;
    try {
      const t = ms(0).v,
        e = Date.now();
      [
        ["shmaMga", 'סוף זמן קריאת שמע (מג"א)'],
        ["shmaGra", 'סוף זמן קריאת שמע (גר"א)'],
        ["tfilaMga", 'סוף זמן תפילה (מג"א)'],
        ["tfilaGra", 'סוף זמן תפילה (גר"א)'],
        ["chatzot", "חצות היום"],
        ["set", "השקיעה"],
      ].forEach(([c, l]) => {
        const a = gs(t[c]) - e;
        a > 0 && a <= 18e4 && (!i || a < i.d) && (i = { k: c, n: l, d: a });
      });
    } catch (t) {}
    if (!i) return e();
    t ||
      ((t = document.createElement("button")),
      (t.id = "zmFlashBar"),
      (t.type = "button"),
      document.body.appendChild(t),
      (t.onclick = () => {
        const e = t.dataset.k;
        (t.remove(), goZman(e));
      }));
    t.dataset.k = i.k;
    const c = Math.floor(i.d / 1e3);
    t.textContent = "⏳ " + i.n + " בעוד " + Math.floor(c / 60) + ":" + String(c % 60).padStart(2, "0") + " · לחצו לפתיחה";
  }
  setInterval(zmFlashTick, 1e3 * 5);
  setInterval(() => {
    document.getElementById("zmFlashBar") && zmFlashTick();
  }, 1e3);
  // 💡 טיפים קופצים לפי המדור (לא חוסמים, עם כפתור פעולה)
  let nudgeT = 0;
  function nudge(t, e, i) {
    // t=מזהה, e=טקסט, i=[[תווית, פעולה],...]
    if (!1 === s.get("nudgeOn", !0)) return;
    const c = s.get("nudge", {});
    if (c[t] && Date.now() - c[t] < 6048e5) return;
    if (document.getElementById("nudgeBox")) return;
    ((c[t] = Date.now()), s.set("nudge", c));
    const a = document.createElement("div");
    ((a.id = "nudgeBox"),
      (a.innerHTML =
        '<img src="' + ue + '" alt=""><div class="nb-t">' + e + '</div><div class="nb-b">' + i.map((t, e) => '<button type="button" data-nb="' + e + '"' + (0 === e ? ' class="pri"' : "") + ">" + t[0] + "</button>").join("") + '</div><button type="button" class="nb-x" aria-label="סגירה">✕</button>'),
      document.body.appendChild(a));
    const o = () => {
      (clearTimeout(nudgeT), a.remove());
    };
    ((l(".nb-x", a).onclick = o),
      a.querySelectorAll("[data-nb]").forEach(
        (t) =>
          (t.onclick = () => {
            (o(), i[+t.dataset.nb][1]());
          }),
      ),
      (nudgeT = setTimeout(o, 2e4)));
  }
  function nudgeDaily(t, e) {
    Xl({ nav: { v: "home", p: { b: t, cont: 1 } }, lbl: e, free: 0 });
    setTimeout(() => {
      const t = document.querySelector('#prT [data-v="daily"]');
      t && t.click();
    }, 350);
  }
  let nudgeLast = "";
  function nudgeCheck() {
    try {
      if ("reader" !== Bt.v || !Ue || null == Ue.si || !n[Ue.si]) return;
      const t = +String(n[Ue.si].g || "").slice(1),
        e = $t[t];
      if (!e || nudgeLast === t + ":" + Ue.si + ":" + Ue.ci) return;
      nudgeLast = t + ":" + Ue.si + ":" + Ue.ci;
      const i = Wl().some((e) => e.nav && e.nav.p && e.nav.p.b === t),
        c = m(VOLS[t] || "");
      if (e.tnx) {
        const e = [];
        ("smt" !== fi() &&
          e.push([
            "📖 לקרוא עכשיו",
            () => {
              (s.set("tnMode", "smt"), Pt(Bt.v, Bt.p));
            },
          ]),
          i || e.push(["⏰ תזכורת יומית", () => nudgeDaily(t, "שניים מקרא ואחד תרגום · " + c)]));
        return void (e.length && nudge("smt", "קראתם השבוע <b>שניים מקרא ואחד תרגום</b>?", e));
      }
      if (i || ["sidur", "birkat"].includes(e.cat)) return;
      const l = s.get("nudgeCnt", {});
      ((l[t] = (l[t] || 0) + 1), s.set("nudgeCnt", l));
      l[t] >= 3 && nudge("daily" + t, "רוצים תזכורת יומית ללמוד ב<b>" + o(c) + "</b>?", [["⏰ כן, לקבוע תזכורת", () => nudgeDaily(t, "לימוד יומי · " + c)]]);
    } catch (t) {}
  }
  try {
    new MutationObserver(() => setTimeout(nudgeCheck, 1500)).observe(document.getElementById("reader"), { childList: !0 });
  } catch (t) {}
  function goZman(t) {''')
# לחיצה על תזכורת לספר – ממשיכה מהמקום האחרון באותו ספר
rep('''        if (e.nav) return void It(e.nav.v, e.nav.p);
        if (e.zk) return void goZman(e.zk);''','''        if (e.nav && e.nav.p && e.nav.p.cont) {
          const t = tt.last && y[tt.last.id];
          if (t && t.s.g === "V" + e.nav.p.b) return void Ye(tt.last.id);
        }
        if (e.nav) return void It(e.nav.v, e.nav.p);
        if (e.zk) return void goZman(e.zk);''')
# הגדרה: טיפים קופצים
rep('''        (r += n(
          "📣 הודעות מהעורך",''','''        (r += n(
          "💡 טיפים ותזכורות קופצות",
          '<div class="sw"><span>להציע לי תזכורות וטיפים לפי המדור שאני נמצא בו (למשל: "קראתם שניים מקרא?")</span><input type="checkbox" id="nudgeC" ' + (!1 !== s.get("nudgeOn", !0) ? "checked" : "") + "></div>",
        )),
        (r += n(
          "📣 הודעות מהעורך",''')
rep('''            const t = l("#edMsgC");
            t &&''','''            const g = l("#nudgeC");
            g &&
              (g.onchange = () => {
                (s.set("nudgeOn", g.checked), g.checked && s.set("nudge", {}));
              });
            const t = l("#edMsgC");
            t &&''')
open(p,'w',encoding='utf-8').write(s); print('patched')
p='shell.html'; s=open(p,encoding='utf-8').read()
a=".rnd-hint{"
assert s.count(a)==1
s=s.replace(a,'''#zmFlashBar{position:fixed;top:calc(var(--safe-t,0px) + 4px);left:8px;right:8px;z-index:9000;border:0;border-radius:14px;padding:10px 12px;font:800 15px var(--ui-font);color:#fff;background:#c0392b;box-shadow:0 6px 22px rgba(192,57,43,.5);animation:zmfl 1s infinite;cursor:pointer}
@keyframes zmfl{0%,100%{background:#c0392b;transform:scale(1)}50%{background:#ff5a45;transform:scale(1.02)}}
@media (prefers-reduced-motion:reduce){#zmFlashBar{animation:none}}
#nudgeBox{position:fixed;left:10px;right:10px;bottom:calc(74px + var(--safe-b,0px));z-index:8000;display:grid;grid-template-columns:46px 1fr 28px;gap:4px 10px;align-items:center;background:var(--card,#fffaf0);border:1px solid var(--line,#e2d6bb);border-radius:18px;padding:10px 12px;box-shadow:0 10px 30px rgba(0,0,0,.22);font-family:var(--ui-font);animation:nbin .3s ease-out}
@keyframes nbin{from{transform:translateY(30px);opacity:0}}
#nudgeBox img{width:46px;height:46px;border-radius:50%;grid-row:1/3}
#nudgeBox .nb-t{font-size:14.5px;line-height:1.45;color:var(--ink)}
#nudgeBox .nb-b{grid-column:2/4;display:flex;gap:6px;flex-wrap:wrap}
#nudgeBox .nb-b button{border:1px solid var(--line);background:none;color:var(--ink);border-radius:999px;padding:6px 12px;font:700 13px var(--ui-font);cursor:pointer}
#nudgeBox .nb-b button.pri{background:var(--navy,#1f2a44);border-color:var(--navy,#1f2a44);color:#fff}
#nudgeBox .nb-x{grid-column:3;grid-row:1;border:0;background:none;color:var(--muted);font-size:16px;cursor:pointer}
body.clean #nudgeBox{display:none}
'''+a)
open(p,'w',encoding='utf-8').write(s)
