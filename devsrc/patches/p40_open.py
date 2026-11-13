p='/home/claude/src/app.js'; s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:100]); s=s.replace(a,b)
# section / chapter-title resolver
rep('''  function botCmd(t) {''','''  // מציאת חלק/פרק לפי שם (למשל "פרק שירה ליום שלישי", "הלל") כשאין שם של ספר
  const BC_STOP = new Set("פתח תפתח פתחי תפתחי תביא לי קח אותי תעביר לך תראה הצג את של עם בבקשה אפשר רוצה תקריא הקרא תקרא קרא תריצ תריץ הרצ הרץ גלילה המסכ המסך מסכ מסך ותריצ ותריץ ותקריא סימונ סימון אותמ אותם אותו אותה צור סטטוס".split(" ").map((t) => bcS(t)));
  function bcSecFind(q) {
    const e = " " + bcS(q) + " ",
      W = bcS(q)
        .split(" ")
        .filter((t) => t.length > 1 && !BC_STOP.has(t));
    let best = null;
    n.forEach((t, i) => {
      const c = $t[+String(t.g || "").slice(1)];
      if (!c || c.hidden) return;
      const l = bcS(bcN(m(String(t.short || ""))));
      l.length > 2 && new RegExp("(^| )[והבלמש]?" + l.replace(/ /g, " [והבלמש]?") + "(?= |$)").test(e) && (!best || l.length > best.len) && (best = { si: i, len: l.length, sk: l });
    });
    if (best) {
      const t = n[best.si],
        i = new Set(best.sk.split(" ")),
        c = W.filter((t) => !i.has(t));
      // "של היום" – לפי היום בשבוע
      const l = ["ראשנ", "שנ", "שלש", "רבע", "חמש", "שש", "שבת"][new Date().getDay()];
      /(^| )(הימ|של הימ|להימ)( |$)/.test(bcS(q)) && c.push(l, "לימ");
      let a = 0,
        o = -1;
      if (c.length)
        t.c.forEach((t, e) => {
          const i = bcS(bcN(m(g(String(t.t || "")))))
              .split(" ")
              .map((t) => t.replace(/^[והבלמש]/, "")),
            l = c.filter((t) => i.includes(t) || i.includes(t.replace(/^[והבלמש]/, ""))).length;
          l > a && ((a = l), (o = e));
        });
      return { si: best.si, ci: o >= 0 ? o : 0, first: o < 0 };
    }
    // שם של פרק בכל הספרים (למשל "הלל", "ברכת המזון")
    let r = null;
    n.forEach((t, i) => {
      const c = $t[+String(t.g || "").slice(1)];
      c &&
        !c.hidden &&
        t.c.forEach((t, c) => {
          const l = bcS(bcN(m(g(String(t.t || "")))).split(/ [-–] /)[0]);
          (l.length > 3 || (l.length > 2 && 1 === W.length && W[0] === l)) && new RegExp("(^| )[והבלמש]?" + l.replace(/ /g, " [והבלמש]?") + "(?= |$)").test(e) && (!r || l.length > r.len) && (r = { si: i, ci: c, len: l.length });
        });
    });
    // מילה אחת שפותחת שם של פרק ("הלל" ← "הלל לראש חודש ולמועדים")
    !r &&
      1 === W.length &&
      W[0].length > 2 &&
      n.forEach((t, i) => {
        const c = $t[+String(t.g || "").slice(1)];
        c &&
          !c.hidden &&
          t.c.forEach((t, c) => {
            const l = bcS(bcN(m(g(String(t.t || ""))))).split(" ");
            l[0] === W[0] && l.length <= 5 && (!r || l.length < r.len) && (r = { si: i, ci: c, len: l.length });
          });
      });
    return r;
  }
  const BOT_YES = ["בשמחה, אח יקר! 📖", "בשמחה רבה! 📖", "ברור, אחי! 📖", "בכיף! 📖"];
  function botCmd(t) {''')
rep('''    if (!B) {
      if ((R || C) && "reader" === Bt.v)''','''    if (!B && (O || R || C || ST)) {
      const e = bcSecFind(q);
      if (e) {
        const t = n[e.si],
          i = t.c[e.ci],
          c = m(String(t.short || "")) + (e.first ? "" : " · " + m(g(String(i.t || "")))),
          a = (i.i && i.i[0] && i.i[0].id) || null,
          r = [];
        return (
          R && r.push("מקריא לך" + (H ? " עם סמן עוקב" : "")),
          C && r.push("מריץ את המסך"),
          ST && r.push("מכין סטטוס"),
          {
            say: BOT_YES[Math.floor(Math.random() * BOT_YES.length)] + " הנה <b>" + o(c) + "</b>" + (r.length ? " – ו" + r.join(" ו") : ""),
            run: () => {
              (We(e.si, e.ci),
                setTimeout(() => {
                  try {
                    (R && (H && s.set("ttsHl", !0), a && mf.fromItem(a)), C && setTimeout(() => ld.start(), R ? 600 : 0), ST && a && kf(a));
                  } catch (t) {}
                }, 900));
            },
          }
        );
      }
    }
    if (!B) {
      if ((R || C) && "reader" === Bt.v)''')
# warmer say for book opens
rep('''      say: "📖 פותח לך את <b>" + o(lbl) + "</b>" + (ch.miss''','''      say: BOT_YES[Math.floor(Math.random() * BOT_YES.length)] + " הנה <b>" + o(lbl) + "</b>" + (ch.miss''')
rep('''(acts.length ? " ו" + acts.join(" ו") : "") + "…",''','''(acts.length ? " – ו" + acts.join(" ו") : ""),''')
rep('''    (R && acts.push("מקריא" + (H ? " עם סמן עוקב" : "")), C && acts.push("מריץ את המסך"), ST && acts.push("מכין סטטוס לשיתוף"));''','''    (R && acts.push("מקריא לך" + (H ? " עם סמן עוקב" : "")), C && acts.push("מריץ את המסך"), ST && acts.push("מכין סטטוס לשיתוף"));''')
# dedupe double sends
rep('''      n = () => {
        const t = (i.value || "").trim();''','''      n = () => {
        const t = (i.value || "").trim();
        // שליחה כפולה (Enter + "שאל" / מקלדת ששולחת פעמיים) – מתעלמים
        if (t.length >= 2 && botLastQ.t === t && Date.now() - botLastQ.at < 2500) return;
        t.length >= 2 && (botLastQ = { t, at: Date.now() });''')
rep('''  let botRemQ = null,''','''  let botLastQ = { t: "", at: 0 },
    botRemQ = null,''')
open(p,'w',encoding='utf-8').write(s)
print('ok')
