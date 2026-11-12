p='/home/claude/src/app.js'; s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:100]); s=s.replace(a,b)
code=open('/home/claude/src/patches/p36_chizuk.js',encoding='utf-8').read()
rep('''  function botBookletAsk(t) {''',code+'''  function botBookletAsk(t) {''')
rep('''        const T = botTalk(t),
          K = T.hits.find((t) => ["distress", "sad"].includes(t.k)),''','''        const T = botTalk(t);
        // 💪 חיזוק – לפי מה שהכותב מרגיש (מצוקה חמורה נשארת עם התשובה הקיימת וקווי הסיוע)
        if (!T.hits.some((t) => "distress" === t.k)) {
          const e = botChizuk(t);
          if (e) {
            const i = (e) => {
              ((c.innerHTML = e.html),
                a("[data-cz]", c).forEach((t) => (t.onclick = () => (Wt(), setTimeout(e.acts[+t.dataset.cz], 230)))),
                (l("#czMore", c).onclick = () => i(botChizuk("", chzLast))));
            };
            return void i(e);
          }
        }
        const K = T.hits.find((t) => ["distress", "sad"].includes(t.k)),''')
open(p,'w',encoding='utf-8').write(s)
p='/home/claude/src/shell.html'; s=open(p,encoding='utf-8').read()
a='.bot-a{padding:12px 14px;'
s=s.replace(a,'.bot-chz p{font:500 16px/1.75 var(--font,inherit);margin:0 0 6px;color:var(--ink)}.bot-chz{border-color:var(--gold,#c9a54a);background:linear-gradient(180deg,rgba(201,165,74,.08),transparent)}\n'+a,1)
open(p,'w',encoding='utf-8').write(s)
print('ok')
