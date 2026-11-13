p='/home/claude/src/app.js'; s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:100]); s=s.replace(a,b)
code=open('/home/claude/src/patches/p41_guide.js',encoding='utf-8').read()
rep('''  function botBookletAsk(t) {''',code+'''  function botBookletAsk(t) {''')
# flow hook: before chizuk/talk. place right after pending-yes block (botPend = null;)
rep('''        botPend = null;
        if (botRemQ) {''','''        botPend = null;
        // 🧭 לימוד מודרך
        {
          const PK = (t, e) => {
            const i = botPackHtml(t, e);
            if (!i) return ((c.innerHTML = '<div class="bot-say">לא מצאתי דיבורים על «' + o(t) + "» 🙏 נסה נושא אחר:</div>" + botTopicAsk().replace(/^<div class="bot-say">[\\s\\S]*?<\\/div>/, "")), TB(), !0);
            ((c.innerHTML = i.html),
              a("[data-pk]", c).forEach((t) => (t.onclick = () => (Wt(), setTimeout(i.acts[+t.dataset.pk], 230)))),
              (l("#pkMore", c).onclick = () => PK(t, (e || 0) + 1)),
              (l("#pkOther", c).onclick = () => ((c.innerHTML = botTopicAsk()), TB())));
            return !0;
          };
          const TB = () =>
            a("[data-tp]", c).forEach(
              (t) =>
                (t.onclick = () => {
                  botTopicQ = !1;
                  const e = "*" === t.dataset.tp ? BOT_TOPICS[Math.floor(Math.random() * BOT_TOPICS.length)][1] : t.dataset.tp;
                  PK(e, 0);
                }),
            );
          const q = " " + bcF(bcN(t)) + " ";
          if (botTopicQ) {
            botTopicQ = !1;
            const e = bcN(t)
              .replace(/(^| )(על|את|הנושא|נושא|של|מעלת|מעלה|בבקשה|אני|רוצה|לי|תביא|תן|דיבורים|אולי|נגיד|למשל)(?= |$)/g, " ")
              .replace(/\\s+/g, " ")
              .trim();
            if (e && e.split(" ").length <= 4 && !/(^| )(איך|איפה|מתי|כמה)( |$)/.test(q) && PK(e, 0)) return;
          }
          if (BOT_GUIDE.test(q)) return ((c.innerHTML = botTopicAsk()), void TB());
          const D = /(^| )(דיבורים|לימוד|ללמוד|תלמד אותי|דברי חיזוק|מאמרים) (על|בעניין|בענין|בנושא) (.+)$/.exec(bcN(t));
          if (D && PK(D[4].trim(), 0)) return;
        }
        if (botRemQ) {''')
# talk: one greeting only
rep('''          W = T.hits.length ? (K ? [K] : T.hits.slice(0, 2)) : [],''','''          W = T.hits.length ? (K ? [K] : T.hits.filter((t) => "hello" !== t.k || 1 === T.hits.length).slice(0, 2)) : [],''')
# examples: add guide items
rep('''["💪 חיזוק", ["תחזק אותי באמונה",''','''["🧭 לימוד", ["מה כדאי ללמוד עכשיו?", "דיבורים על תפילה", "דיבורים על שמחה"]], ["💪 חיזוק", ["תחזק אותי באמונה",''')
open(p,'w',encoding='utf-8').write(s)
print('ok')
