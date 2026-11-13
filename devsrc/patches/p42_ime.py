p='/home/claude/src/app.js'; s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:100]); s=s.replace(a,b)
# שינוי ערך מהקוד בזמן שהמקלדת פתוחה מבלבל את המקלדת (סמסונג) – ואז מקש המחיקה לא מוחק. מאפסים את המקלדת: blur ואז focus
rep('''          (clrV(), thr() && t.length >= 2 && ((i.value = ""), (XB.hidden = !0), ME.scrollIntoView({ block: "start", behavior: "smooth" })));''','''          (clrV(), thr() && t.length >= 2 && (botSetVal(i, ""), (XB.hidden = !0), ME.scrollIntoView({ block: "start", behavior: "smooth" })));''')
rep('''      (XB.onpointerdown = (t) => (t.preventDefault(), (i.value = ""), (XB.hidden = !0), i.focus())),''','''      (XB.onpointerdown = (t) => (t.preventDefault(), botSetVal(i, "", !0), (XB.hidden = !0))),''')
rep('''  let botLastQ = { t: "", at: 0 },''','''  // מחליף טקסט בשורה ומאפס את המקלדת – אחרת במקלדות מסוימות (סמסונג) מקש המחיקה מפסיק לעבוד
  function botSetVal(t, e, i) {
    const c = document.activeElement === t || i;
    (c && t.blur(),
      (t.value = e),
      c &&
        setTimeout(() => {
          try {
            (t.focus(), t.setSelectionRange(e.length, e.length));
          } catch (t) {}
        }, 60));
  }
  let botLastQ = { t: "", at: 0 },''')
open(p,'w',encoding='utf-8').write(s)
print('ok')
