p='app.js'; s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:80]); s=s.replace(a,b)
rep('''  function Xl() {
    const t = (function () {''','''  function selfRem() {
    const t = Ut(
      '<h3>✍️ תזכורת אישית</h3><div class="sh-sub">כתבו מה שתרצו שיופיע בתזכורת. היא תקפוץ כהתראה בזמן שתבחרו, ותופיע גם בווידג\\'ט (ברשימת התזכורות).</div><div class="field"><label>מה לכתוב בתזכורת?</label><input type="text" id="srT" maxlength="90" placeholder="למשל: לומר תיקון הכללי · להתקשר לחברותא"></div><button class="btn pri" id="srGo" style="width:100%">המשך – בחירת זמן</button>',
    );
    ((l("#srGo", t).onclick = () => {
      const e = (l("#srT", t).value || "").trim();
      if (!e) return void st("כתבו את הטקסט של התזכורת");
      (Wt(), setTimeout(() => Xl({ nav: { v: "home", p: {} }, lbl: e, free: 1 }), 280));
    }),
      setTimeout(() => {
        try {
          l("#srT", t).focus();
        } catch (t) {}
      }, 250));
  }
  window.__selfRem = selfRem;
  function Xl(ov) {
    const t = ov || (function () {''')
rep('''      f = Ut(
        '<h3>⏰ תזכורת לדף הזה</h3><div class="sh-sub">📍 ' +''','''      f = Ut(
        "<h3>" + (t.free ? "✍️ תזכורת אישית" : "⏰ תזכורת לדף הזה") + '</h3><div class="sh-sub">📍 ' +''')
rep('''    return { title: "⏰ תזכורת: " + t.lbl, body: t.note || "קבעת תזכורת ללמוד כאן", nav: t.nav, kind: "pg:" + t.id };''',
    '''    return { title: (t.free ? "✍️ " : "⏰ תזכורת: ") + t.lbl, body: t.note || (t.free ? "תזכורת אישית שקבעת" : "קבעת תזכורת ללמוד כאן"), nav: t.nav, kind: "pg:" + t.id };''')
rep('''(r += '<div id="prCard">' + n("⏰ תזכורות לדפים", '<div id="prCardBody">' + Jl() + "</div>") + "</div>"),''',
    '''(r += '<div id="prCard">' + n("⏰ תזכורות לדפים ותזכורות אישיות", '<button class="btn sm" type="button" onclick="window.__selfRem()" style="margin-bottom:10px">✍️ תזכורת אישית חדשה (טקסט חופשי)</button><div id="prCardBody">' + Jl() + "</div>") + "</div>"),''')
rep('''            l > 40 || i.push({ id: 1e3 + 50 * c + l, title: e.title, body: e.body, schedule: { at: new Date(e.at), allowWhileIdle: !0 } });''',
    '''            l > 40 || i.push({ id: 1e3 + 50 * c + l, title: e.title, body: e.body, schedule: { at: new Date(e.at), allowWhileIdle: !0 }, extra: { zk: e.k } });''')
rep('''((t.actionTypeId = "REMX"),''','''((t.actionTypeId = "REMX"),
              (t.channelId = "bp_rem_snd"),''')
rep('''        if (e.nav) return void It(e.nav.v, e.nav.p);
        if (e.open) return void ("cal" === e.open ? It("calendar") : Ye(e.open));''','''        if (e.nav) return void It(e.nav.v, e.nav.p);
        if (e.zk) return void goZman(e.zk);
        if (e.ed) return void edMsgShow(e.ed);
        if (e.open) return void ("cal" === e.open ? It("calendar") : Ye(e.open));''')
rep('''    try {
      t.registerActionTypes({''','''    try {
      t.createChannel({ id: "bp_rem_snd", name: "תזכורות ברסלב PRO", description: "תזכורות לימוד, זמני היום והודעות", importance: 5, visibility: 1, vibration: !0, lights: !0 });
    } catch (t) {}
    try {
      t.registerActionTypes({''')
rep('''  function selfRem() {''','''  function goZman(t) {
    const e = /shma/i.test(t)
      ? ["קש וברכותיה", "קריאת שמע"]
      : /tfila/i.test(t)
        ? ["עמידה לשחרית של יום חול"]
        : /mincha|plag/i.test(t)
          ? ["תפילת מנחה לימי החול"]
          : /tzeit/i.test(t)
            ? ["תפילת ערבית לימי החול"]
            : "omer" === t
              ? ["ספירת העומר"]
              : "lev" === t
                ? ["ברכת הלבנה"]
                : null;
    if (e)
      for (const t of e)
        for (let e = 0; e < n.length; e++) {
          const i = n[e];
          if ("sidur" !== ($t[+String(i.g || "").slice(1)] || {}).cat) continue;
          const c = i.c.findIndex((e) => m(g(e.t)).replace(/["״'׳]/g, "").includes(t));
          if (c >= 0) return void It("reader", { si: e, ci: c });
        }
    It("calendar");
  }
  window.__goZman = goZman;
  function edMsgOn() {
    return !!s.get("edMsg", !1);
  }
  function edMsgShow(t) {
    const e = ((s.get("live", {}) || {}).msgs || []).find((e) => String(e.id) === String(t));
    e &&
      Ut(
        "<h3>📣 " + o(e.t || "הודעה מהעורך") + '</h3><div style="white-space:pre-wrap;line-height:1.7;font-size:16px">' + o(e.b || "") + "</div>" + (e.u ? '<a class="btn pri" style="display:block;text-align:center;margin-top:12px" href="' + o(e.u) + '" target="_blank" rel="noopener">לפתיחה</a>' : ""),
      );
  }
  function edMsgCheck(t) {
    try {
      const e = (t && t.msgs) || [];
      if (!e.length) return;
      const i = s.get("edSeen", []),
        c = e.filter((t) => !i.includes(String(t.id)) && (!t.until || Date.now() < t.until));
      if (!c.length) return;
      if (!edMsgOn()) {
        if (s.get("edAsked", !1)) return;
        s.set("edAsked", !0);
        const t = Ut(
          '<h3>📣 הודעות מהעורך</h3><div style="line-height:1.7">רוצים לקבל מדי פעם הודעה קצרה מעורך האפליקציה – חיזוק, עדכון על ספר חדש או שיר חדש? ההודעות יופיעו כהתראה. אפשר לכבות בכל רגע בהגדרות.</div><div class="row2" style="margin-top:14px"><button class="btn pri" id="edY">כן, אשמח</button><button class="btn" id="edN">לא עכשיו</button></div>',
        );
        return (
          (l("#edY", t).onclick = () => {
            (s.set("edMsg", !0), Wt(), setTimeout(() => edMsgCheck(s.get("live", {})), 400));
          }),
          void (l("#edN", t).onclick = () => Wt())
        );
      }
      s.set("edSeen", i.concat(c.map((t) => String(t.id))).slice(-60));
      const a = c[c.length - 1],
        r = NAT.on ? NAT.P("LocalNotifications") : null;
      if (r)
        try {
          r.schedule({
            notifications: c.map((t, e) => ({ id: 3500 + ((+t.id || e) % 90), title: "📣 " + (t.t || "הודעה מהעורך"), body: t.b || "", channelId: "bp_rem_snd", schedule: { at: new Date(Date.now() + 1500 + 400 * e), allowWhileIdle: !0 }, extra: { ed: String(t.id) } })),
          });
        } catch (t) {}
      setTimeout(() => edMsgShow(a.id), 600);
    } catch (t) {}
  }
  function selfRem() {''')
rep('''      if (!e || null == e.v || String(e.v) === String(null == f.v ? "" : f.v)) return;''','''      if (e && Array.isArray(e.msgs) && e.msgs.length) {
        const t = s.get("live", {}) || {};
        (String(e.v) === String(null == f.v ? "" : f.v) && ((t.msgs = e.msgs), s.set("live", t)), setTimeout(() => edMsgCheck(e), 2500));
      }
      if (!e || null == e.v || String(e.v) === String(null == f.v ? "" : f.v)) return;''')
open(p,'w',encoding='utf-8').write(s); print('patched')
