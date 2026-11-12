p='/home/claude/src/app.js'; s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:100]); s=s.replace(a,b)
# 1. examples dropdown (static) + greeting only
EX='''[["🛠️ פעולות", ["פתח לי תהלים פרק צ ותריץ את המסך", "תקריא לי את התיקון הכללי עם סימון", "פתח לי שמות הצדיקים ותקריא", "צור לי סטטוס על מעלת ההתבודדות", "צור לי חוברת על שמחה", "תזכיר לי תיקון חצות"]], ["📚 על הספרים", ["איפה רבנו מדבר על התבודדות", "כמה תורות יש בחלק ב׳", "כמה פעמים מופיע רצון", "שם אמו של רבנו", "עצה להינצל מכעס"]], ["💪 חיזוק", ["תחזק אותי באמונה", "אני מיואש, קשה לי", "תן לי חיזוק"]], ["🕯️ זמנים", ["מתי נכנסת שבת", "מתי השקיעה היום", "עד מתי קריאת שמע"]], ["⚙️ האפליקציה", ["איך מגדילים אותיות?", "איך משתפים כתמונה?", "מה חדש באפליקציה"]]]'''
rep('''<div id="botLog"></div><div class="bot-me" id="botMe" hidden></div>''','''<details class="bot-ex" id="botEx"><summary><span>💡 דוגמאות – מה אפשר לבקש ממני</span><i>▾</i></summary>' +
        ''' + EX + '''
          .map((t) => '<div class="bx-g"><b>' + t[0] + '</b><div class="bx-l">' + t[1].map((t) => '<button type="button" class="bx-i" data-ch="' + o(t) + '">' + o(t) + "</button>").join("") + "</div></div>")
          .join("") +
        '</details><div id="botLog"></div><div class="bot-me" id="botMe" hidden></div>''')
i=s.index('''        if (t.length < 2)
          return void (
            (c.innerHTML =
              '<div class="bot-tip">👋 שלום! אני העוזר שלך.''')
j=s.index('''        // "כן" – אחרי "תרצה לראות מקורות?"''')
s=s[:i]+'''        if (t.length < 2) return void (c.dataset.q || LG.children.length || (c.innerHTML = '<div class="bot-tip">👋 שלום! אני העוזר שלך – שאל אותי, או בקש שאעשה משהו בשבילך. רעיונות יש בלשונית "💡 דוגמאות" למעלה.</div>'));
'''+s[j:]
# bind examples + clear button via pointerdown (keeps keyboard, no layout jump)
rep('''      (XB.onclick = () => ((i.value = ""), (XB.hidden = !0), i.focus())),''','''      (XB.onpointerdown = (t) => (t.preventDefault(), (i.value = ""), (XB.hidden = !0), i.focus())),
      (XB.onclick = (t) => t.preventDefault()),
      a("#botEx [data-ch]", e).forEach((t) => (t.onclick = () => ((l("#botEx", e).open = !1), (i.value = t.dataset.ch.replace(/,/g, "")), n()))),''')
# 3. status on a topic
rep('''    const B = bcBook(q);
    if (!B) {''','''    const B = bcBook(q);
    if (ST && !B) {
      const e = q
        .replace(/(^| )(צור|תצור|תיצור|תכין|הכן|תעשה|לי|סטטוס|סטורי|תמונה|לשיתוף|יפה|על|בעניין|בענין|בנושא|של|מעלת|מעלה|גודל|חשיבות|עם|דיבור|חיזוק|מרבנו|רבנו|אחד)(?= |$)/g, " ")
        .replace(/\\s+/g, " ")
        .trim();
      return {
        say: "🖼️ מכין לך סטטוס" + (e ? " על «" + o(e) + "»" : " עם דיבור חיזוק מרבנו") + " – עם דיבור קצר מהספרים…",
        run: () => {
          if (!e) return botStatus();
          try {
            const t = botQAget().ask("איפה רבנו מדבר על " + e),
              i = t && t.S ? t.S.list.slice(0, 25) : [],
              c = (t) => m(g((h[t].it.b || []).filter((t) => "p" === t[0]).map((t) => t[1]).join(" "))).length,
              l = i.map((t) => t.bi).filter((t) => c(t) > 60 && c(t) < 700);
            l.length ? kf(h[l[0]].id) : i.length ? kf(h[i[0].bi].id) : (st("לא מצאתי דיבור על «" + e + "» – הנה דיבור חיזוק", 3e3), botStatus());
          } catch (t) {
            botStatus();
          }
        },
      };
    }
    if (!B) {''')
open(p,'w',encoding='utf-8').write(s)
p='/home/claude/src/shell.html'; s=open(p,encoding='utf-8').read()
a='.bot-a{padding:12px 14px;'
css='''.bot-ex{margin:4px 0 8px;border:1.5px solid var(--gold,#c9a54a);border-radius:14px;background:var(--card);overflow:hidden}.bot-ex summary{list-style:none;display:flex;align-items:center;justify-content:space-between;padding:10px 14px;font:700 14.5px var(--ui-font);color:var(--ink);cursor:pointer}.bot-ex summary::-webkit-details-marker{display:none}.bot-ex summary i{font-style:normal;transition:transform .2s}.bot-ex[open] summary i{transform:rotate(180deg)}.bot-ex[open] summary{border-bottom:1px solid var(--line)}
.bx-g{padding:8px 12px 4px}.bx-g>b{display:block;font:700 12.5px var(--ui-font);color:var(--ink2);margin-bottom:5px}.bx-l{display:flex;flex-wrap:wrap;gap:5px}.bx-i{border:1px solid var(--line);background:var(--bg,#fff);color:var(--ink);border-radius:999px;padding:5px 11px;font:13px var(--ui-font);cursor:pointer}.bx-i:active{background:var(--gold,#c9a54a);color:#1b1b1b}
#botX{width:34px!important;height:34px!important;line-height:34px!important;font-size:16px!important;touch-action:manipulation}.bot-in input{padding-inline-end:42px!important}
'''
s=s.replace(a,css+a,1); open(p,'w',encoding='utf-8').write(s)
print('ok')
