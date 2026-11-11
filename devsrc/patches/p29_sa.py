p='app.js'; s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:80]); s=s.replace(a,b)
# 1) מפרשים: סעיף עם כמה פסקאות (הגה) – לא לאבד פסקאות
rep('''      const e = l.filter((t) => "p" === t[0]),
        c = e.length ? e[0][1] : "";''','''      const e = l.filter((t) => "p" === t[0]),
        c = e.map((t) => t[1]).join("clean" === mgv ? " " : "<br>");''')
# 2) לימוד הלכה יומי
rep('''  function goZman(t) {''','''  // ⚖️ הלכה יומית לפי סדר השולחן ערוך
  const HAL_DEF = { on: !1, per: 2, time: "08:00", pos: 0, d0: 0 };
  function halPlan() {
    return Object.assign({}, HAL_DEF, s.get("halPlan", {}) || {});
  }
  function halDay(t) {
    const e = t || new Date();
    return Math.round((new Date(e.getFullYear(), e.getMonth(), e.getDate()) - new Date(2020, 0, 1)) / 864e5);
  }
  let halSeqC = null;
  function halSeq() {
    return halSeqC || (halSeqC = h.filter((t) => ($t[+String(t.s.g).slice(1)] || {}).sa && t.it.n).map((t) => t.id));
  }
  function halIdx(t) {
    const e = halPlan(),
      i = halSeq().length || 1;
    return (((e.pos + (halDay() + (t || 0) - e.d0) * e.per) % i) + i) % i;
  }
  function halIds(t) {
    const e = halPlan(),
      i = halSeq(),
      c = halIdx(t),
      l = [];
    for (let t = 0; t < e.per && i.length; t++) l.push(i[(c + t) % i.length]);
    return l;
  }
  function halLabel(t) {
    try {
      const e = halIds(t).map((t) => y[t]).filter(Boolean);
      if (!e.length) return "";
      const i = e[0],
        c = e[e.length - 1],
        l = (t) => m(g(t.c.t)).split(" – ")[0],
        a = ($t[+String(i.s.g).slice(1)] || {}).base || "";
      return i.c === c.c
        ? a + " · " + l(i) + " · " + (e.length > 1 ? "סעיפים " + m(i.it.n) + "–" + m(c.it.n) : "סעיף " + m(i.it.n))
        : a + " · " + l(i) + " סעיף " + m(i.it.n) + " – " + l(c) + " סעיף " + m(c.it.n);
    } catch (t) {
      return "";
    }
  }
  function halOpen(t) {
    const e = halIds(t || 0);
    if (!e.length || !y[e[0]]) return void st("השולחן ערוך עוד לא נטען");
    (s.set("halSeen", halDay()), Ye(e[0]));
  }
  window.__halOpen = halOpen;
  function halMark() {
    const t = halPlan();
    if (!t.on || "reader" !== Bt.v) return;
    const e = new Set(halIds(0));
    a("#reader .item[data-id]").forEach((t) => t.classList.toggle("hal-today", e.has(t.dataset.id)));
  }
  try {
    new MutationObserver(() => setTimeout(halMark, 60)).observe(document.getElementById("reader"), { childList: !0 });
  } catch (t) {}
  function halSet(t) {
    const e = halPlan(),
      i = Object.assign({}, e, t);
    (e.on && (null != t.per || null != t.on) && ((i.pos = halIdx(0)), (i.d0 = halDay())), s.set("halPlan", i));
    try {
      Jd();
    } catch (t) {}
    try {
      window.__remSync && window.__remSync();
    } catch (t) {}
  }
  function halSheet() {
    const t = halPlan(),
      e = Ut(
        '<h3>⚖️ הלכה יומית</h3><div class="sh-sub">כל יום מגיעות ההלכות הבאות לפי סדר השולחן ערוך: אורח חיים, יורה דעה, אבן העזר וחושן משפט – ובסוף מתחילים מחדש. ההתראה מגיעה בשעה שתבחרו, ומופיעה גם בווידג\\'ט.</div>' +
          (t.on ? '<div class="hal-now">📖 היום: <b>' + o(halLabel(0)) + "</b></div>" : "") +
          '<div class="field"><label>כמה סעיפים בכל יום?</label><div class="seg" id="halPer">' +
          [1, 2, 3, 5, 10].map((e) => '<button data-v="' + e + '"' + (t.per === e ? ' class="on"' : "") + ">" + e + "</button>").join("") +
          '</div></div><div class="field"><label>שעת ההתראה</label><input type="time" id="halTime" value="' +
          o(t.time) +
          '"></div>' +
          (t.on
            ? '<div class="row2" style="flex-wrap:wrap"><button class="btn pri" id="halGo">📖 ללמוד עכשיו</button><button class="btn sm" id="halRe">⏮ להתחיל מההתחלה</button><button class="btn sm" id="halOff">לכבות</button></div>'
            : '<button class="btn pri" id="halOn" style="width:100%">✅ כן, שלחו לי כל יום הלכות לפי הסדר</button>'),
      );
    (a("#halPer button", e).forEach(
      (t) =>
        (t.onclick = () => {
          (halSet({ per: +t.dataset.v }), a("#halPer button", e).forEach((e) => e.classList.toggle("on", e === t)));
        }),
    ),
      (l("#halTime", e).onchange = (t) => halSet({ time: t.target.value || "08:00" })));
    const i = (t, i) => {
      const c = l(t, e);
      c && (c.onclick = i);
    };
    (i("#halOn", () => {
      (s.set("halPlan", Object.assign(halPlan(), { on: !0, pos: 0, d0: halDay() })), halSet({}), Wt(), st("⚖️ מעולה! כל יום תקבלו הלכות לפי סדר השולחן ערוך", 3e3), halRefresh());
      try {
        NAT.on && NAT.P("LocalNotifications") && NAT.P("LocalNotifications").requestPermissions();
      } catch (t) {}
    }),
      i("#halGo", () => {
        (Wt(), setTimeout(() => halOpen(0), 250));
      }),
      i("#halRe", () => {
        confirm("להתחיל שוב מסימן א באורח חיים?") && (s.set("halPlan", Object.assign(halPlan(), { pos: 0, d0: halDay() })), halSet({}), Wt(), halRefresh());
      }),
      i("#halOff", () => {
        (halSet({ on: !1 }), Wt(), st("הלימוד היומי כובה"), halRefresh());
      }));
  }
  window.__halSheet = halSheet;
  function halCardHtml() {
    const t = halPlan();
    return t.on
      ? '<div class="hal-card"><div class="hal-ic">⚖️</div><div class="hal-tx"><b>ההלכות של היום</b><small>' + o(halLabel(0)) + '</small></div><button class="btn pri sm" type="button" onclick="window.__halOpen()">ללמוד</button><button class="btn sm" type="button" onclick="window.__halSheet()" aria-label="הגדרות">⚙️</button></div>'
      : '<div class="hal-card"><div class="hal-ic">⚖️</div><div class="hal-tx"><b>רוצה לקבל כל יום ' + t.per + ' הלכות לפי סדר השולחן ערוך?</b><small>התראה יומית, בווידג\\'ט ובראש המסך. אפשר לבחור כמה סעיפים.</small></div><button class="btn pri sm" type="button" onclick="window.__halSheet()">כן!</button></div>';
  }
  function halRefresh() {
    a(".hal-card").forEach((t) => {
      t.outerHTML = halCardHtml();
    });
  }
  window.__halCard = halCardHtml;
  setTimeout(() => {
    try {
      const t = halPlan();
      t.on &&
        s.get("halSeen", 0) !== halDay() &&
        nudge("hal" + halDay(), "⚖️ <b>ההלכות של היום</b><br>" + o(halLabel(0)), [
          ["📖 ללמוד עכשיו", () => halOpen(0)],
          ["אחר כך", () => {}],
        ]);
    } catch (t) {}
  }, 9e3);
  function goZman(t) {''')
# 3) כרטיס בלשונית השולחן ערוך
rep('''      if (c && "room" === Ge())
        try {
          He(i);
        } catch (t) {
          console.error(t);
        }''','''      if (c && "room" === Ge())
        try {
          He(i);
        } catch (t) {
          console.error(t);
        }
      if (c && "sa" === Ge())
        try {
          const t = document.createElement("div");
          ((t.className = "hal-wrap"), (t.innerHTML = halCardHtml()), i.appendChild(t));
        } catch (t) {
          console.error(t);
        }''')
# 4) התראות (מכשיר): 14 ימים קדימה
rep('''        if (
          (i.forEach((t) => {
            ((t.actionTypeId = "REMX"),''','''        try {
          const t = halPlan();
          if (t.on && halSeq().length) {
            const [e, c] = t.time.split(":").map(Number);
            for (let l = 0; l < 14; l++) {
              const a = new Date();
              (a.setDate(a.getDate() + l), a.setHours(e, c, 0, 0), a > new Date(Date.now() + 3e4) && i.push({ id: 3400 + l, title: "⚖️ ההלכות של היום", body: halLabel(l), schedule: { at: a, allowWhileIdle: !0 }, extra: { hal: 1 } }));
            }
          }
        } catch (t) {}
        if (
          (i.forEach((t) => {
            ((t.actionTypeId = "REMX"),''')
rep('''        if (e.zk) return void goZman(e.zk);''','''        if (e.zk) return void goZman(e.zk);
        if (e.hal) return void halOpen(0);''')
# 5) התראה בדפדפן (בלי אפליקציה)
rep('''    const o = Rl();
    t.on &&
      i >= t.time &&''','''    try {
      const t = halPlan(),
        e = s.get("halLast", 0);
      t.on && i >= t.time && e !== halDay() && (s.set("halLast", halDay()), NAT.on || ta({ title: "⚖️ ההלכות של היום", body: halLabel(0), kind: "hal" }));
    } catch (t) {}
    const o = Rl();
    t.on &&
      i >= t.time &&''')
# 6) ווידג'ט
rep('''        e.push({ from: l, heb: is(new Date(i.y, i.m - 1, i.d, 12)), par: Ts(t).n || "", hil: _o(c).slice(0, 6).map(Xo), aly: o ? o.lbl : "", ev: a });''',
    '''        e.push({ from: l, heb: is(new Date(i.y, i.m - 1, i.d, 12)), par: Ts(t).n || "", hil: _o(c).slice(0, 6).map(Xo), aly: o ? o.lbl : "", ev: a, hal: halPlan().on ? halLabel(t) : "" });''')
rep('''      if (e.on)
        for (let i = 0; i < 2; i++) {
          const l = new Date();
          l.setDate(l.getDate() + i);
          const [a, o] = e.time.split(":").map(Number);
          (l.setHours(a, o, 0, 0), l > t && c.push({ t: +l, n: "תזכורת לימוד יומית" }));
        }''','''      if (e.on)
        for (let i = 0; i < 2; i++) {
          const l = new Date();
          l.setDate(l.getDate() + i);
          const [a, o] = e.time.split(":").map(Number);
          (l.setHours(a, o, 0, 0), l > t && c.push({ t: +l, n: "תזכורת לימוד יומית" }));
        }
      const i = halPlan();
      if (i.on)
        for (let e = 0; e < 2; e++) {
          const l = new Date();
          l.setDate(l.getDate() + e);
          const [a, o] = i.time.split(":").map(Number);
          (l.setHours(a, o, 0, 0), l > t && c.push({ t: +l, n: "⚖️ " + halLabel(e) }));
        }''')
# 7) כרטיס בהגדרות
rep('''        (r += '<div id="wdgCard">' + n("📱 הגדרות הווידג'ט", wdgSettingsHtml()) + "</div>"),''','''        (r += n("⚖️ הלכה יומית", '<div style="font-size:13.5px;color:var(--ink2);line-height:1.6;margin-bottom:8px">הלכות לפי סדר השולחן ערוך, כל יום – עם התראה ובווידג\\'ט.</div><button class="btn sm" type="button" onclick="window.__halSheet()">' + (halPlan().on ? "⚙️ הגדרות הלימוד היומי · " + halPlan().per + " סעיפים ב־" + o(halPlan().time) : "✅ להפעלה") + "</button>")),
        (r += '<div id="wdgCard">' + n("📱 הגדרות הווידג'ט", wdgSettingsHtml()) + "</div>"),''')
rep('''      e("tEv", "אירועי היום (ראש חודש, חנוכה וכו׳)") +''','''      e("tEv", "אירועי היום (ראש חודש, חנוכה וכו׳)") +
      e("tHal", "ההלכות של היום (אם הפעלתם הלכה יומית)") +''')
rep('''  const WDG_DEF = { yt: !0,''','''  const WDG_DEF = { tHal: !0, yt: !0,''')
open(p,'w',encoding='utf-8').write(s); print('patched')
p='shell.html'; s=open(p,encoding='utf-8').read()
a=".rnd-hint{"
s=s.replace(a,'''.hal-wrap{grid-column:1/-1}
.hal-card{display:flex;align-items:center;gap:10px;padding:12px 14px;margin:0 0 10px;border-radius:18px;border:1px solid var(--accent,#b08a3a);background:linear-gradient(135deg,var(--card,#fffaf0),var(--soft,rgba(176,138,58,.10)))}
.hal-card .hal-ic{font-size:30px}.hal-card .hal-tx{flex:1;min-width:0}.hal-card b{display:block;font:800 15px var(--ui-font);color:var(--ink)}.hal-card small{display:block;font:500 12.5px var(--ui-font);color:var(--muted);margin-top:2px}
.hal-now{padding:10px 12px;border-radius:12px;background:var(--soft,rgba(176,138,58,.10));margin:6px 0 10px;font:600 14px var(--ui-font)}
#reader .item.hal-today{box-shadow:inset -4px 0 0 var(--accent,#b08a3a);background:color-mix(in srgb,var(--accent,#b08a3a) 7%,transparent);border-radius:10px}
'''+a,1)
open(p,'w',encoding='utf-8').write(s)
