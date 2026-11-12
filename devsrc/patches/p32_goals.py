p='app.js'; s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:80]); s=s.replace(a,b)
G=r'''
  // 🎯 יעדים: רושמים יעדים קבועים, והאפליקציה מרכיבה מהם סדר יום עם המקום המדויק של כל יעד
  const GOAL_T = {
    tikkun: { ic: "📜", n: "תיקון הכללי", d: "עשרת המזמורים" },
    smt: { ic: "📖", n: "שניים מקרא ואחד תרגום", d: "העלייה של היום בפרשת השבוע" },
    teh: { ic: "📖", n: "פרקי תהלים", d: "ממשיכים מהמקום שעצרתם", q: [1, 3, 5, 10, 20] },
    zohar: { ic: "✨", n: "זוהר הקדוש", d: "קטעים לפי הסדר מתחילת הזוהר", q: [1, 2, 3, 5, 10] },
    hal: { ic: "⚖️", n: "שולחן ערוך", d: "סעיפים לפי הסדר", q: [1, 2, 3, 5, 10] },
    book: { ic: "📚", n: "לימוד בספר", d: "פרקים לפי הסדר מספר שתבחרו", q: [1, 2, 3, 5] },
    free: { ic: "✍️", n: "יעד אישי", d: "כל דבר שתרצו – לסימון בלבד" },
  };
  function goals() {
    const t = s.get("goals", []);
    return Array.isArray(t) ? t : [];
  }
  function goalsSave(t) {
    (s.set("goals", t), goalsRefresh());
    try {
      Jd();
    } catch (t) {}
  }
  function goalDone(t, e) {
    const i = s.get("goalsDone", {}),
      c = String(halDay(e ? new Date(Date.now() + 864e5 * e) : null));
    return !!(i[c] || {})[t];
  }
  // רשימת יחידות לימוד לפי סדר: לתהלים – מזמורים, לזוהר – קטעים, לספר – פרקים
  function goalSeq(t) {
    if ("teh" === t.k) {
      const t = $t.findIndex((t) => t && "teh" === t.cat);
      return n.filter((e) => e.g === "V" + t && e.c.length > 5).flatMap((t) => t.c.map((e, i) => ({ si: n.indexOf(t), ci: i, l: m(g(e.t)) })));
    }
    if ("zohar" === t.k) {
      const t = [120, 121, 122, 123, 124, 125, 126].filter((t) => $t[t] && $t[t].zh);
      return h.filter((e) => t.includes(+String(e.s.g).slice(1))).map((t) => ({ id: t.id, l: m(VOLS[+String(t.s.g).slice(1)] || "").replace("זוהר · ", "") + " · " + m(g(L(t.s))) + " · " + m(g(t.c.t)) }));
    }
    if ("book" === t.k) return n.filter((e) => e.g === "V" + t.b).flatMap((t) => t.c.map((e, i) => ({ si: n.indexOf(t), ci: i, l: m(g(L(t))) + " · " + m(g(e.t)) })));
    return [];
  }
  const goalSeqC = {};
  function goalToday(t) {
    // מחזיר {lbl, go}
    try {
      if ("tikkun" === t.k) return { lbl: "תיקון הכללי", go: () => It("tikkun") };
      if ("free" === t.k) return { lbl: t.txt || "יעד אישי", go: null };
      if ("hal" === t.k) {
        const e = halPlan();
        return e.on ? { lbl: "שולחן ערוך · " + halLabel(0), go: () => halOpen(0) } : { lbl: "שולחן ערוך – יש להפעיל הלכה יומית", go: () => halSheet() };
      }
      if ("smt" === t.k) {
        const t = Kd(0);
        return t && t.si >= 0 && t.k >= 0 ? { lbl: t.lbl.replace("חומש היום: ", "שמו\"ת · "), go: () => It("reader", { si: t.si, aly: t.k }) } : { lbl: "שניים מקרא ואחד תרגום", go: () => (s.set("libTab", "tanach"), It("home")) };
      }
      const e = t.k + ":" + (t.b || ""),
        i = goalSeqC[e] || (goalSeqC[e] = goalSeq(t));
      if (!i.length) return { lbl: GOAL_T[t.k].n, go: null };
      const c = (t.pos || 0) % i.length,
        l = i.slice(c, c + (t.q || 1)),
        a = l[0],
        o = l[l.length - 1],
        r = "teh" === t.k ? "תהלים " + (l.length > 1 ? a.l.replace(/^מזמור\s*/, "") + "–" + o.l.replace(/^מזמור\s*/, "") : a.l) : l.length > 1 ? a.l + " (+" + (l.length - 1) + ")" : a.l;
      return { lbl: ("book" === t.k ? m(VOLS[t.b] || "") + " · " : "zohar" === t.k ? "זוהר · " : "") + r, go: () => (a.id ? Ye(a.id) : We(a.si, a.ci)) };
    } catch (e) {
      return { lbl: (GOAL_T[t.k] || {}).n || "", go: null };
    }
  }
  function goalMark(t, e) {
    const i = s.get("goalsDone", {}),
      c = String(halDay());
    i[c] = i[c] || {};
    const l = goals(),
      a = l.find((e) => e.id === t);
    if (e && !i[c][t]) (a && ["teh", "zohar", "book"].includes(a.k) && (a.pos = (a.pos || 0) + (a.q || 1)), (i[c][t] = 1));
    else if (!e && i[c][t]) (a && ["teh", "zohar", "book"].includes(a.k) && (a.pos = Math.max(0, (a.pos || 0) - (a.q || 1))), delete i[c][t]);
    // שומרים רק 60 ימים אחרונים
    Object.keys(i)
      .sort()
      .slice(0, -60)
      .forEach((t) => delete i[t]);
    (s.set("goalsDone", i), goalsSave(l));
    l.length && l.every((t) => i[c][t.id]) && e && st("🎉 כל היעדים של היום הושלמו! אשריכם", 3500);
  }
  function goalsHtml() {
    const t = goals();
    if (!t.length)
      return '<div class="gl-empty">🎯 עוד לא קבעתם יעדים.<br>לחצו "➕ יעד חדש" – למשל תיקון הכללי, שניים מקרא, 5 פרקי תהלים או קטע זוהר – והאפליקציה תרכיב לכם סדר יום.</div>';
    const e = t.filter((t) => goalDone(t.id)).length;
    return (
      '<div class="gl-prog"><div class="gl-bar"><i style="width:' + Math.round((100 * e) / t.length) + '%"></i></div><span>' + e + " מתוך " + t.length + "</span></div>" +
      t
        .map((t, e) => {
          const i = goalToday(t),
            c = goalDone(t.id);
          return '<div class="gl-it' + (c ? " done" : "") + '"><label class="gl-ck"><input type="checkbox" data-gck="' + t.id + '"' + (c ? " checked" : "") + '></label><button type="button" class="gl-go" data-ggo="' + e + '"><span class="gl-ic">' + (GOAL_T[t.k] || {}).ic + "</span><span><b>" + o(i.lbl) + "</b>" + (i.go ? "<small>לחצו לפתיחה ←</small>" : "") + "</span></button></div>";
        })
        .join("")
    );
  }
  function goalsBind(t) {
    (a("[data-gck]", t).forEach((t) => (t.onchange = () => goalMark(t.dataset.gck, t.checked))),
      a("[data-ggo]", t).forEach(
        (t) =>
          (t.onclick = () => {
            const e = goalToday(goals()[+t.dataset.ggo]);
            e.go ? (Wt(), setTimeout(e.go, 200)) : st("סמנו ✓ כשתסיימו");
          }),
      ));
  }
  function goalsRefresh() {
    a(".gl-list").forEach((t) => {
      ((t.innerHTML = goalsHtml()), goalsBind(t));
    });
  }
  function goalsOpen() {
    const t = Ut(
      '<h3>🎯 היעדים שלי – סדר היום</h3><div class="sh-sub">היעדים הקבועים שלכם, לפי הסדר. האפליקציה יודעת מה המקום של היום בכל יעד – לחיצה פותחת אותו, ו־✓ מסמן שסיימתם (ביעדים שהולכים לפי הסדר – למחרת ממשיכים מהמקום הבא).</div><div class="gl-list">' +
        goalsHtml() +
        '</div><div class="row2" style="margin-top:10px;flex-wrap:wrap"><button class="btn pri" id="glAdd">➕ יעד חדש</button><button class="btn sm" id="glEdit">✏️ סידור ומחיקה</button><button class="btn sm" id="glRem">⏰ ' +
        (s.get("goalsRem", null) ? "תזכורת ב־" + o(s.get("goalsRem")) : "תזכורת יומית") +
        "</button></div>",
    );
    (goalsBind(t),
      (l("#glAdd", t).onclick = () => {
        (Wt(), setTimeout(goalAdd, 260));
      }),
      (l("#glEdit", t).onclick = () => {
        (Wt(), setTimeout(goalEdit, 260));
      }),
      (l("#glRem", t).onclick = () => {
        const t = prompt("באיזו שעה לקבל תזכורת יומית עם היעדים? (למשל 07:30). להשאיר ריק = בלי תזכורת", s.get("goalsRem", "") || "07:30");
        if (null == t) return;
        const e = t.trim();
        if (e && !/^\d{1,2}:\d{2}$/.test(e)) return void st("כתבו שעה בצורה 07:30");
        (s.set("goalsRem", e ? e.padStart(5, "0") : null), st(e ? "⏰ כל יום ב־" + e + " תקבלו תזכורת עם היעדים" : "התזכורת בוטלה"), Wt(), setTimeout(goalsOpen, 260));
      }));
  }
  window.__goalsOpen = goalsOpen;
  function goalAdd() {
    const t = Ut(
      '<h3>➕ יעד חדש</h3><div class="gl-types">' +
        Object.keys(GOAL_T)
          .map((t) => '<button type="button" data-gt="' + t + '"><span>' + GOAL_T[t].ic + "</span><b>" + GOAL_T[t].n + "</b><small>" + GOAL_T[t].d + "</small></button>")
          .join("") +
        "</div>",
    );
    a("[data-gt]", t).forEach(
      (t) =>
        (t.onclick = () => {
          const e = t.dataset.gt,
            i = GOAL_T[e],
            c = { id: "g" + Date.now().toString(36), k: e, q: i.q ? i.q[Math.min(2, i.q.length - 1)] : 1, pos: 0 };
          if ("free" === e) {
            const t = prompt("מה היעד? (למשל: התבודדות שעה, לימוד עם הילדים)");
            if (!t || !t.trim()) return;
            c.txt = t.trim().slice(0, 60);
          } else if ("hal" === e && !halPlan().on) {
            (s.set("halPlan", Object.assign(halPlan(), { on: !0, pos: 0, d0: halDay() })), halSet({}));
          }
          if ("book" === e) return void (Wt(), setTimeout(() => goalPickBook(c), 260));
          if (i.q) return void (Wt(), setTimeout(() => goalPickQ(c), 260));
          (goalsSave(goals().concat([c])), Wt(), st("🎯 היעד נוסף"), setTimeout(goalsOpen, 260));
        }),
    );
  }
  function goalPickQ(t) {
    const e = GOAL_T[t.k],
      i = Ut(
        "<h3>" + e.ic + " " + e.n + '</h3><div class="field"><label>' + ("teh" === t.k ? "כמה פרקים בכל יום?" : "zohar" === t.k ? "כמה קטעים בכל יום?" : "hal" === t.k ? "כמה סעיפים בכל יום?" : "כמה פרקים בכל יום?") + '</label><div class="seg" id="gq">' + e.q.map((e) => '<button data-v="' + e + '"' + (e === t.q ? ' class="on"' : "") + ">" + e + "</button>").join("") + '</div></div><button class="btn pri" id="gqOk" style="width:100%">שמירה</button>',
      );
    (a("#gq button", i).forEach(
      (e) =>
        (e.onclick = () => {
          ((t.q = +e.dataset.v), a("#gq button", i).forEach((t) => t.classList.toggle("on", t === e)));
        }),
    ),
      (l("#gqOk", i).onclick = () => {
        ("hal" === t.k && halSet({ per: t.q }), goalsSave(goals().concat([t])), Wt(), st("🎯 היעד נוסף"), setTimeout(goalsOpen, 260));
      }));
  }
  function goalPickBook(t) {
    const e = Ut(
      '<h3>📚 באיזה ספר?</h3><div style="max-height:58vh;overflow:auto">' +
        VOLS.map((t, e) => ({ t, e }))
          .filter((t) => $t[t.e] && !$t[t.e].hidden && "hidden" !== $t[t.e].cat && !ce(t.e) && !$t[t.e].special)
          .map((t) => '<button type="button" class="gl-bk" data-gb="' + t.e + '">' + o(m(t.t)) + "</button>")
          .join("") +
        "</div>",
    );
    a("[data-gb]", e).forEach(
      (e) =>
        (e.onclick = () => {
          ((t.b = +e.dataset.gb), Wt(), setTimeout(() => goalPickQ(t), 260));
        }),
    );
  }
  function goalEdit() {
    const t = () => {
      const e = goals(),
        i = Ut(
          '<h3>✏️ סידור היעדים</h3><div class="sh-sub">הסדר כאן הוא סדר היום שלכם.</div>' +
            (e.length
              ? e
                  .map(
                    (t, i) =>
                      '<div class="gl-row"><span>' + (GOAL_T[t.k] || {}).ic + " " + o(goalToday(t).lbl) + '</span><button class="btn sm" data-gu="' + i + '"' + (i ? "" : " disabled") + '>▲</button><button class="btn sm" data-gd="' + i + '"' + (i < e.length - 1 ? "" : " disabled") + '>▼</button><button class="btn sm" data-gx="' + i + '">🗑</button></div>',
                  )
                  .join("")
              : '<div class="gl-empty">אין יעדים</div>') +
            '<button class="btn pri" id="glBack" style="width:100%;margin-top:10px">סיום</button>',
        ),
        c = (i, c) => {
          const l = goals();
          ([l[i], l[i + c]] = [l[i + c], l[i]], goalsSave(l), Wt(), setTimeout(t, 200));
        };
      (a("[data-gu]", i).forEach((t) => (t.onclick = () => c(+t.dataset.gu, -1))),
        a("[data-gd]", i).forEach((t) => (t.onclick = () => c(+t.dataset.gd, 1))),
        a("[data-gx]", i).forEach(
          (e) =>
            (e.onclick = () => {
              confirm("למחוק את היעד?") && (goalsSave(goals().filter((t, i) => i !== +e.dataset.gx)), Wt(), setTimeout(t, 200));
            }),
        ),
        (l("#glBack", i).onclick = () => {
          (Wt(), setTimeout(goalsOpen, 260));
        }));
    };
    t();
  }
  function goalsLine() {
    const t = goals();
    if (!t.length) return "";
    const e = t.filter((t) => goalDone(t.id)).length,
      i = t.find((t) => !goalDone(t.id));
    return "יעדים " + e + "/" + t.length + (i ? " · הבא: " + goalToday(i).lbl : " · הכול הושלם ✓");
  }
  // בכניסה לאפליקציה: סדר היום של היעדים
  setTimeout(() => {
    try {
      const t = goals();
      if (!t.length || s.get("goalsSeen", 0) === halDay()) return;
      s.set("goalsSeen", halDay());
      const e = t.filter((t) => !goalDone(t.id));
      e.length &&
        nudge("goals" + halDay(), "🎯 <b>היעדים של היום</b><br>" + e.slice(0, 4).map((t) => o(goalToday(t).lbl)).join(" · ") + (e.length > 4 ? " …" : ""), [
          ["📋 לסדר היום", () => goalsOpen()],
          ["אחר כך", () => {}],
        ]);
    } catch (t) {}
  }, 6500);
'''
rep('''  function goZman(t) {''',G+'''  function goZman(t) {''')
# האזור שלי: לשונית יעדים
rep('''    if ("bm" === qa) {''','''    if ("goals" === qa) {
      ((e.innerHTML = '<div class="gl-list gl-page">' + goalsHtml() + '</div><div class="row2" style="margin:12px 4px;flex-wrap:wrap"><button class="btn pri" type="button" onclick="window.__goalsOpen()">🎯 ניהול היעדים</button></div>'), goalsBind(e));
      return;
    }
    if ("bm" === qa) {''')
# התראות: תזכורת יומית ליעדים
rep('''        try {
          const t = halPlan();
          if (t.on && halSeq().length) {''','''        try {
          const t = s.get("goalsRem", null);
          if (t && goals().length) {
            const [e, c] = t.split(":").map(Number);
            for (let t = 0; t < 7; t++) {
              const l = new Date();
              (l.setDate(l.getDate() + t), l.setHours(e, c, 0, 0), l > new Date(Date.now() + 3e4) && i.push({ id: 3450 + t, title: "🎯 היעדים של היום", body: goals().map((t) => (GOAL_T[t.k] || {}).n || "").join(" · "), schedule: { at: l, allowWhileIdle: !0 }, extra: { goals: 1 } }));
            }
          }
        } catch (t) {}
        try {
          const t = halPlan();
          if (t.on && halSeq().length) {''')
rep('''        if (e.hal) return void halOpen(0);''','''        if (e.hal) return void halOpen(0);
        if (e.goals) return void goalsOpen();''')
rep('''    const e = { halPlan: 1, pgRem: 1,''','''    const e = { goals: 1, goalsRem: 1, halPlan: 1, pgRem: 1,''')
# ווידג'ט
rep('''    return { v: 2, ts: t, days: e, zm: i.slice(0, 30), rem: c.slice(0, 12), cont: l, dir: a, cfg: wdgCfg(), quotes: q, yt: ht() };''','''    let gl = "";
    try {
      gl = wdgCfg().tGoals ? goalsLine() : "";
    } catch (t) {}
    return { v: 2, ts: t, days: e, zm: i.slice(0, 30), rem: c.slice(0, 12), cont: l, dir: a, cfg: wdgCfg(), quotes: q, yt: ht(), goals: gl };''')
rep('''  const WDG_DEF = { tHal: !0,''','''  const WDG_DEF = { tGoals: !0, tHal: !0,''')
rep('''      e("tHal", "ההלכות של היום (אם הפעלתם הלכה יומית)") +''','''      e("tHal", "ההלכות של היום (אם הפעלתם הלכה יומית)") +
      e("tGoals", "🎯 היעדים שלי – כמה הושלמו ומה הבא") +''')
rep('''        else if ("q:" === String(t).slice(0, 2)) {''','''        else if ("goals" === t) goalsOpen();
        else if ("q:" === String(t).slice(0, 2)) {''')
# עוזר: מושג יעדים
rep('''    { id: "contact", ic: "💬",''','''    { id: "goals", ic: "🎯", t: "היעדים שלי – סדר יום", a: "רושמים יעדים קבועים (תיקון הכללי, שניים מקרא, פרקי תהלים, קטעי זוהר, שולחן ערוך, ספר לבחירה או יעד אישי) – והאפליקציה מרכיבה סדר יום עם המקום המדויק של היום בכל יעד, תזכורת יומית, ווידג'ט וסימון ✓. נמצא ב\\"האזור שלי\\" ← יעדים ובכפתור הצף ✦.", w: "יעד יעדים מטרה מטרות סדר יום יומי קבוע קבועים חוק חוקים התחייבות משימות משימה תוכנית", go: () => goalsOpen() },
    { id: "contact", ic: "💬",''')
open(p,'w',encoding='utf-8').write(s); print('ok')
p='shell.html'; s=open(p,encoding='utf-8').read()
def rp(a,b):
    global s
    assert s.count(a)==1,a; s=s.replace(a,b)
rp('''    <button class="pill on" data-mt="bm">🔖 סימניות</button>''','''    <button class="pill" data-mt="goals">🎯 יעדים</button>
    <button class="pill on" data-mt="bm">🔖 סימניות</button>''')
rp('''    <button class="fi" data-f="bot">🤖<span>שאלו את העוזר</span></button>''','''    <button class="fi" data-f="goals">🎯<span>היעדים שלי – סדר היום</span></button>
    <button class="fi" data-f="bot">🤖<span>שאלו את העוזר</span></button>''')
s=s.replace(".rnd-hint{",'''.gl-empty{padding:14px;text-align:center;color:var(--muted);font-size:14px;line-height:1.7}
.gl-prog{display:flex;align-items:center;gap:10px;margin:4px 2px 10px;font:700 13px var(--ui-font);color:var(--muted)}.gl-bar{flex:1;height:8px;border-radius:99px;background:var(--line)}.gl-bar i{display:block;height:100%;border-radius:99px;background:var(--ok,#3c8d5a);transition:width .3s}
.gl-it{display:flex;align-items:center;gap:8px;padding:8px 10px;border:1px solid var(--line);border-radius:14px;background:var(--card);margin-bottom:7px}
.gl-it.done{opacity:.6}.gl-it.done b{text-decoration:line-through}
.gl-ck input{width:22px;height:22px;accent-color:var(--ok,#3c8d5a)}
.gl-go{flex:1;display:flex;align-items:center;gap:10px;border:0;background:none;text-align:right;font:inherit;color:var(--ink);cursor:pointer;padding:2px}
.gl-go .gl-ic{font-size:22px}.gl-go b{display:block;font:700 14.5px var(--ui-font)}.gl-go small{color:var(--accent,#8a6a2a);font-size:12px}
.gl-types{display:grid;grid-template-columns:1fr 1fr;gap:8px}.gl-types button{border:1px solid var(--line);background:var(--card);border-radius:14px;padding:12px 8px;text-align:center;cursor:pointer;font:inherit;color:var(--ink)}.gl-types span{font-size:26px;display:block}.gl-types b{display:block;font-size:14px}.gl-types small{display:block;color:var(--muted);font-size:11.5px;margin-top:3px}
.gl-row{display:flex;align-items:center;gap:6px;padding:7px 0;border-bottom:1px solid var(--line)}.gl-row span{flex:1;font-size:14px}
.gl-bk{display:block;width:100%;text-align:right;border:0;border-bottom:1px solid var(--line);background:none;padding:11px 4px;font:inherit;color:var(--ink);cursor:pointer}
.gl-page{padding:4px 12px}
.rnd-hint{''',1)
open(p,'w',encoding='utf-8').write(s)
