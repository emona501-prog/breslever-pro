p='/home/claude/src/app.js'; s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:100]); s=s.replace(a,b)
code=open('/home/claude/src/patches/p37_zm.js',encoding='utf-8').read()
rep('''  function botBookletAsk(t) {''',code+'''  function botBookletAsk(t) {''')
rep('''        botPend = null;
        // 🛠️ פקודות: פתח / תקריא / תריץ / סטטוס / תזכיר לי''','''        botPend = null;
        // 🕯️ זמנים: תשובה בצ׳אט לפי העיר
        {
          const ZR = (q, forced) => {
            const e = botZmAns(q, forced);
            if (!e) return !1;
            if (e.ask) {
              botCityQ = q;
              c.innerHTML = botCityAskHtml();
              a("[data-city]", c).forEach((t) => (t.onclick = () => ((i.value = t.dataset.city), n())));
              return !0;
            }
            c.innerHTML = e.html;
            a("[data-zq]", c).forEach(
              (t) =>
                (t.onclick = () => {
                  const i = e.acts[+t.dataset.zq]();
                  "city" === i && ((botCityQ = q), (c.innerHTML = botCityAskHtml("באיזו עיר?")), a("[data-city]", c).forEach((t) => (t.onclick = () => ((l("#botQ").value = t.dataset.city), n()))));
                }),
            );
            return !0;
          };
          if (botCityQ) {
            const e = botCityFind(t),
              q = botCityQ;
            if (e) {
              ((botCityQ = null), s.set("zmCity", zmLoc(e)), s.set("zmCityOk", !0), st("📍 העיר נשמרה: " + e[0], 2200));
              if (ZR(q, 1)) return;
            } else if (t.split(" ").length <= 3) {
              c.innerHTML = botCityAskHtml("לא מצאתי עיר בשם הזה ברשימה שלי 🙏 בחרו מהרשימה:");
              a("[data-city]", c).forEach((t) => (t.onclick = () => ((i.value = t.dataset.city), n())));
              return;
            } else botCityQ = null;
          }
          if (ZR(t)) return;
        }
        // 🛠️ פקודות: פתח / תקריא / תריץ / סטטוס / תזכיר לי''')
open(p,'w',encoding='utf-8').write(s)
p='/home/claude/src/shell.html'; s=open(p,encoding='utf-8').read()
a='.bot-a{padding:12px 14px;'
s=s.replace(a,'.bot-zm{line-height:1.9}.bot-zm b{font-size:1.08em}.bot-zl{font-size:13px;color:var(--ink2);margin:6px 2px}.bot-zl .btn{padding:2px 10px;font-size:13px;text-decoration:underline}\n'+a,1)
open(p,'w',encoding='utf-8').write(s)
print('ok')
