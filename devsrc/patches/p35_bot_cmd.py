p='/home/claude/src/app.js'; s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:100]); s=s.replace(a,b)
code=open('/home/claude/src/patches/p35_bot_cmd.js',encoding='utf-8').read()
rep('''  function botBookletAsk(t) {''',code+'''  function botBookletAsk(t) {''')
rep('''  function botOpen(t) {''','''  function botOpen(t, pre) {''')
rep('''      t && ((i.value = t), n()),''','''      t && ((i.value = t), pre ? ((XB.hidden = !1), setTimeout(() => { try { i.focus(); i.setSelectionRange(t.length, t.length); } catch (t) {} }, 300)) : n()),''')
rep('''      t || n(),
      clrV());''','''      (t && !pre) || n(),
      clrV());''')
rep('''        // 🛠️ פעולה: "צור לי חוברת על ..."
        const BK = botBookletAsk(t);''','''        // 🛠️ פקודות: פתח / תקריא / תריץ / סטטוס / תזכיר לי
        const CM = botCmd(t);
        if (CM) return ((c.innerHTML = '<div class="bot-say">' + CM.say + "</div>"), void setTimeout(() => (Wt(), setTimeout(CM.run, 250)), 1100));
        // 🛠️ פעולה: "צור לי חוברת על ..."
        const BK = botBookletAsk(t);''')
i=s.index('''        if (t.length < 2) return void (c.innerHTML = '<div class="bot-tip">💡 על האפליקציה''')
j=s.index('\n',i)
s=s[:i]+'''        if (t.length < 2)
          return void (
            (c.innerHTML =
              '<div class="bot-tip">👋 שלום! אני העוזר שלך. אפשר לשאול אותי, וגם לבקש שאעשה דברים:</div><div class="bot-chips">' +
              ["פתח לי תהלים פרק צ ותריץ את המסך", "תקריא לי את התיקון הכללי עם סימון", "צור לי סטטוס מתורה קיב חלק ב", "צור לי חוברת על שמחה", "תזכיר לי תיקון חצות", "איפה רבנו מדבר על התבודדות", "כמה תורות יש בחלק ב׳", "מתי נכנסת שבת", "איך מגדילים אותיות?"]
                .map((t) => '<button class="pill" data-ch="' + o(t) + '">' + o(t) + "</button>")
                .join("") +
              "</div>"),
            a("[data-ch]", c).forEach((t) => (t.onclick = () => ((i.value = t.dataset.ch), n())))
          );'''+s[j:]
rep(''' + (s.get("botFab", !1) ? "checked" : "") + "></div>",
        )),''',''' + (s.get("botFab", !1) ? "checked" : "") + '></div><div class="sw"><span>העוזר מציע רעיונות מדי פעם (לפי היום והשעה – חגים, שבת, חצות, יעדים)</span><input type="checkbox" id="botTipS" ' + (s.get("botTips", !0) ? "checked" : "") + "></div>",
        )),''')
rep('''            bf && (bf.onchange = () => (s.set("botFab", bf.checked), botFloat(bf.checked)));''','''            bf && (bf.onchange = () => (s.set("botFab", bf.checked), botFloat(bf.checked)));
            const bts = l("#botTipS");
            bts && (bts.onchange = () => s.set("botTips", bts.checked));''')
open(p,'w',encoding='utf-8').write(s)
p='/home/claude/src/shell.html'; s=open(p,encoding='utf-8').read()
css='''#botTip{position:fixed;z-index:85;left:12px;right:12px;bottom:calc(150px + var(--safe-b,0px));max-width:440px;margin:0 auto;display:flex;gap:10px;align-items:flex-start;padding:12px 12px 10px;border-radius:18px;background:var(--card,#fffdf6);border:1.5px solid var(--gold,#c9a54a);box-shadow:0 10px 30px rgba(0,0,0,.25);transform:translateY(30px);opacity:0;transition:.35s;font:15px/1.55 var(--ui-font)}#botTip.on{transform:none;opacity:1}#botTip .bot-av{width:46px;height:46px}#botTip .bt-b{flex:1}#botTip p{margin:0 0 8px;color:var(--ink)}#botTip .bt-a{display:flex;gap:6px;flex-wrap:wrap}#botTip .bt-off{border:0;background:none;color:var(--ink2);font-size:12px;margin-top:6px;padding:0;text-decoration:underline;cursor:pointer}#botTip .bt-x{border:0;background:none;font-size:16px;color:var(--ink2);cursor:pointer;padding:2px 4px}
.bot-chips{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 4px}.bot-chips .pill{font-size:13.5px}
'''
a='.bot-a{padding:12px 14px;'
s=s.replace(a,css+a,1); open(p,'w',encoding='utf-8').write(s)
print('ok')
