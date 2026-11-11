p='app.js'; s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:80]); s=s.replace(a,b)
rep('''    return { v: 1, ts: t, days: e, zm: i.slice(0, 30), rem: c.slice(0, 12), cont: l, dir: a };''','''    let q = [];
    try {
      q = wdgQuotes();
    } catch (t) {}
    return { v: 2, ts: t, days: e, zm: i.slice(0, 30), rem: c.slice(0, 12), cont: l, dir: a, cfg: wdgCfg(), quotes: q, yt: ht() };''')
rep('''  let _d = null;
  function Jd() {''','''  const WDG_DEF = { yt: !0, quote: !0, quoteMed: !1, aly: !0, cont: !0, dir: !0, row1: !0, row2: !0, tHil: !0, tRem: !0, tAly: !0, tEv: !0, tZm: !0, qmin: 10, qv: null };
  function wdgCfg() {
    return Object.assign({}, WDG_DEF, s.get("wdgCfg", {}) || {});
  }
  function wdgVols() {
    const t = wdgCfg().qv;
    if (Array.isArray(t) && t.length) return t;
    const e = [];
    VOLS.forEach((t, i) => {
      /ספר המידות|ספר המדות|ליקוטי עצות|לקוטי עצות/.test(m(t)) && $t[i] && !$t[i].hidden && e.push(i);
    });
    return e.length ? e : VOLS.map((t, e) => e).filter((t) => $t[t] && "rn" === $t[t].cat);
  }
  function wdgQuotes() {
    if (!wdgCfg().quote) return [];
    const t = wdgVols(),
      e = [];
    for (const i of h) {
      if (!t.includes(+String(i.s.g).slice(1)) || i.s.dup) continue;
      const c = i.it.b.reduce((t, e) => t + ("p" === e[0] ? e[1].length : 0), 0);
      c >= 30 && c <= 420 && e.push(i);
    }
    const i = [];
    for (let t = 0; t < 60 && e.length && i.length < 30; t++) {
      const t = e.splice(Math.floor(Math.random() * e.length), 1)[0],
        c = x(t.it, { noNiqud: !1 }).replace(/\\s+/g, " ").trim();
      c.replace(/[\\u0591-\\u05c7]/g, "").length <= 190 && i.push({ t: c, s: m(VOLS[+String(t.s.g).slice(1)] || "") + " · " + m(g(t.c.t)), id: t.it.id });
    }
    return i;
  }
  function wdgSettingsHtml() {
    const t = wdgCfg(),
      e = (e, i) => '<div class="sw"><span>' + i + '</span><input type="checkbox" data-wc="' + e + '"' + (t[e] ? " checked" : "") + "></div>";
    return (
      '<div style="font-size:13.5px;color:var(--ink2);line-height:1.65;margin-bottom:8px">כאן בוחרים מה יופיע בווידג\\'ט של מסך הבית (באפליקציית אנדרואיד). <b>גודל:</b> לחיצה ארוכה על הווידג\\'ט וגרירת הפינות – קטן, בינוני או גדול. ככל שהוא גבוה יותר, נכנס בו יותר.</div>' +
      e("yt", "לוגו ערוץ גאולה וישועה (לחיצה פותחת את הערוץ)") +
      e("quote", "דיבור מתחלף מהספרים שבחרתי (בווידג\\'ט הגדול)") +
      e("quoteMed", "להציג דיבור מתחלף גם בגודל הבינוני") +
      '<div class="field" style="margin-top:6px"><label>כל כמה זמן להחליף דיבור</label><div class="seg" id="wcMin">' +
      [1, 5, 10, 30, 60].map((e) => '<button data-v="' + e + '"' + (+t.qmin === e ? ' class="on"' : "") + ">" + (60 === e ? "שעה" : e + " דק׳") + "</button>").join("") +
      '</div></div><button class="btn sm" type="button" id="wcBooks" style="margin:4px 0 10px">📚 מאילו ספרים להביא דיבורים (' +
      wdgVols().length +
      ")</button>" +
      "<div class=\\"sh-sub\\">בווידג'ט הגדול:</div>" +
      e("aly", "שורת חומש היום") +
      e("cont", "שורת המשך הלימוד") +
      e("dir", "שורת כיוון התפילה") +
      e("row1", "כפתורים: פתיחה אקראית · המשך לימוד · מצפן · תיקון הכללי") +
      e("row2", "כפתורים: תהלים · לוח הילולות · תזכורת · חיפוש") +
      '<div class="sh-sub">בשורה המתחלפת (בכל הגדלים):</div>' +
      e("tHil", "הילולות היום") +
      e("tRem", "התזכורות שלי (כולל תזכורות אישיות)") +
      e("tAly", "חומש היום") +
      e("tEv", "אירועי היום (ראש חודש, חנוכה וכו׳)") +
      e("tZm", "זמני היום הבאים")
    );
  }
  function wdgSettingsBind(t) {
    const e = (t) => {
      (s.set("wdgCfg", Object.assign({}, s.get("wdgCfg", {}) || {}, t)), Jd());
    };
    (a("[data-wc]", t).forEach(
      (t) =>
        (t.onchange = () => {
          (e({ [t.dataset.wc]: t.checked }), st("הווידג'ט עודכן ✓", 1200));
        }),
    ),
      a("#wcMin button", t).forEach(
        (i) =>
          (i.onclick = () => {
            (e({ qmin: +i.dataset.v }), a("#wcMin button", t).forEach((t) => t.classList.toggle("on", t === i)));
          }),
      ));
    const i = l("#wcBooks", t);
    i &&
      (i.onclick = () => {
        const t = wdgVols(),
          c = Ut(
            '<h3>📚 ספרים לדיבורים בווידג\\'ט</h3><div class="sh-sub">ברירת המחדל: ספר המידות וליקוטי עצות. הדיבורים שנבחרים הם קצרים – כאלה שנכנסים בווידג\\'ט.</div><div style="max-height:52vh;overflow:auto">' +
              VOLS.map((e, i) => ({ e, i }))
                .filter((t) => $t[t.i] && !$t[t.i].hidden && "hidden" !== $t[t.i].cat && !$t[t.i].mg && !$t[t.i].special && !["sidur", "birkat", "tanach"].includes($t[t.i].cat))
                .map((e) => '<label class="sw"><span>' + o(m(e.e)) + '</span><input type="checkbox" data-wv="' + e.i + '"' + (t.includes(e.i) ? " checked" : "") + "></label>")
                .join("") +
              '</div><button class="btn pri" id="wvOk" style="width:100%;margin-top:10px">שמירה</button>',
          );
        l("#wvOk", c).onclick = () => {
          const t = a("[data-wv]", c)
            .filter((t) => t.checked)
            .map((t) => +t.dataset.wv);
          (e({ qv: t.length ? t : null }), Wt(), st("נשמר ✓ הדיבורים יתעדכנו בווידג'ט", 2200), setTimeout(() => "settings" === Bt.v && Ft.settings(), 350));
        };
      });
  }
  let _d = null;
  function Jd() {''')
rep('''        else if ("dir" === t) It("dir");
        else if ("tikkun" === t) It("tikkun");''','''        else if ("q:" === String(t).slice(0, 2)) {
          const e = String(t).slice(2);
          y[e] ? Ye(e) : It("random");
        } else if ("dir" === t) It("dir");
        else if ("tikkun" === t) It("tikkun");''')
rep('''        (r += n(
          "💡 טיפים ותזכורות קופצות",''','''        (r += '<div id="wdgCard">' + n("📱 הגדרות הווידג'ט", wdgSettingsHtml()) + "</div>"),
        (r += n(
          "💡 טיפים ותזכורות קופצות",''')
rep('''            const g = l("#nudgeC");
            g &&''','''            try {
              const t = l("#wdgCard");
              t && wdgSettingsBind(t);
            } catch (t) {}
            const g = l("#nudgeC");
            g &&''')
open(p,'w',encoding='utf-8').write(s); print('patched')
