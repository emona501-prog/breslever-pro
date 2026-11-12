p='/home/claude/src/app.js'; s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:100]); s=s.replace(a,b)
code=open('/home/claude/src/patches/p39_rem.js',encoding='utf-8').read()
rep('''  function botBookletAsk(t) {''',code+'''  function botBookletAsk(t) {''')
# reminder branch: create directly or ask for time in chat
rep('''      const i = /חצות/.test(e) ? 27 : /תיקון הכללי|תקון הכללי/.test(e) ? 23 : /תהלים|תהילים/.test(e) ? 17 : -1;
      return {''','''      const i = /חצות/.test(e) ? 27 : /תיקון הכללי|תקון הכללי/.test(e) ? 23 : /תהלים|תהילים/.test(e) ? 17 : -1,
        lbl = (e || "תזכורת")
          .replace(/(^| )(מחר|למחר|היום|הערב|בערב|בבוקר|בלילה|בצהריים|כל יום|כל בוקר|כל ערב|כל לילה|בעוד \\S+( דקות| שעות| שעה| דקה)?|ב ?\\d{1,2}([:.]\\d{2})?|בשעה ?\\d{1,2}([:.]\\d{2})?|\\d{1,2}[:.]\\d{2})(?= |$)/g, " ")
          .replace(/\\s+/g, " ")
          .trim() || "תזכורת",
        nav = { v: "home", p: i >= 0 ? { b: i } : {} },
        w = botRemTime(q, lbl);
      if (w) {
        const t = botRemMake(lbl, nav, w);
        return { stay: 1, say: "✅ קבעתי לך תזכורת: <b>" + o(lbl) + "</b> – " + botRemDesc(w) + (w.z ? " (לפי זמני היום בעיר שלך)" : "") + ". תקבל התראה בזמן 🔔", undo: t.id };
      }
      return { stay: 1, ask: { lbl, nav }, say: "⏰ בשמחה! מתי להזכיר לך «" + o(lbl) + "»?" };
      return {''')
rep('''        const CM = botCmd(t);
        if (CM) return ((c.innerHTML = '<div class="bot-say">' + CM.say + "</div>"), void setTimeout(() => (Wt(), setTimeout(CM.run, 250)), 1100));''','''        const CM = botCmd(t);
        if (CM && CM.stay) {
          const e = CM.ask
            ? [
                ["בעוד שעה", { at: Date.now() + 36e5 }],
                ["הערב ב־20:00", botRemTime("הערב ב 20:00")],
                ["מחר ב־8:00", botRemTime("מחר ב 8")],
                ["כל יום ב־8:00", { daily: 1, time: "08:00" }],
                ["כל ערב ב־21:00", { daily: 1, time: "21:00" }],
              ]
            : [];
          return void (
            (c.innerHTML =
              '<div class="bot-say">' +
              CM.say +
              "</div>" +
              (CM.ask ? '<div class="bot-chips">' + e.map((t, e) => '<button class="pill" data-rw="' + e + '">' + t[0] + "</button>").join("") + '</div><div class="bot-scope">או כתבו שעה, למשל: "מחר ב־7:30" · "כל יום ב־21:00"</div>' : "") +
              '<div class="bot-srcs">' +
              (CM.undo ? '<button class="btn sm" id="remUndo">↩️ בטל</button>' : "") +
              '<button class="btn sm" id="remList">📋 כל התזכורות שלי</button></div>'),
            a("[data-rw]", c).forEach(
              (t) =>
                (t.onclick = () => {
                  const i = e[+t.dataset.rw][1];
                  (botRemMake(CM.ask.lbl, CM.ask.nav, i), (c.innerHTML = '<div class="bot-say">✅ קבעתי לך תזכורת: <b>' + o(CM.ask.lbl) + "</b> – " + botRemDesc(i) + ". תקבל התראה בזמן 🔔</div>"));
                }),
            ),
            CM.ask && (botRemQ = CM.ask),
            l("#remUndo", c) && (l("#remUndo", c).onclick = () => (Yl(Wl().filter((t) => t.id !== CM.undo)), (c.innerHTML = '<div class="bot-say">↩️ ביטלתי את התזכורת.</div>'))),
            l("#remList", c) &&
              (l("#remList", c).onclick = () => (
                Wt(),
                It("settings"),
                setTimeout(() => {
                  const t = document.getElementById("prCard");
                  t && t.scrollIntoView({ block: "start" });
                }, 400)
              ))
          );
        }
        if (CM) return ((c.innerHTML = '<div class="bot-say">' + CM.say + "</div>"), void setTimeout(() => (Wt(), setTimeout(CM.run, 250)), 1100));''')
# answer with time after ask
rep('''        botPend = null;
        // 🕯️ זמנים: תשובה בצ׳אט לפי העיר''','''        botPend = null;
        if (botRemQ) {
          const e = botRemTime(bcF(bcN(t)), botRemQ.lbl),
            i = botRemQ;
          if (((botRemQ = null), e)) return (botRemMake(i.lbl, i.nav, e), void (c.innerHTML = '<div class="bot-say">✅ קבעתי לך תזכורת: <b>' + o(i.lbl) + "</b> – " + botRemDesc(e) + ". תקבל התראה בזמן 🔔</div>"));
        }
        // 🕯️ זמנים: תשובה בצ׳אט לפי העיר''')
rep('''  let botLogNodes = [],''','''  let botRemQ = null,
    botLogNodes = [],''')
open(p,'w',encoding='utf-8').write(s)
print('ok')
