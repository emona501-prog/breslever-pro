p='app.js'; s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:80]); s=s.replace(a,b)
rep('''  function pi(t) {
    const e = $t[t];
    if (e && e.mg) {''','''  // זוהר: ארמית / לשון הקודש / משולב. התרגום בקובץ נפרד שנטען לפי הצורך.
  function zhMode() {
    const t = s.get("zhMode", "both");
    return ["both", "ar", "he"].includes(t) ? t : "both";
  }
  const ZH = { c: {}, p: {} };
  function zhLoad(t) {
    const e = $t[t];
    return e && "string" == typeof e.zh
      ? ZH.c[t]
        ? Promise.resolve(ZH.c[t])
        : ZH.p[t] ||
          (ZH.p[t] = fetch("data/" + e.zh)
            .then((t) => {
              if (!t.ok) throw new Error("zh");
              return t.json();
            })
            .then((e) => ((ZH.c[t] = e), e))
            .catch((e) => {
              throw (delete ZH.p[t], e);
            }))
      : Promise.reject(new Error("nozh"));
  }
  function zhApply() {
    const t = document.getElementById("reader");
    if (!t) return;
    const e = zhMode();
    (t.classList.toggle("zh-ar", "ar" === e), t.classList.toggle("zh-he", "he" === e));
    a("[data-zhm]", t).forEach((t) => t.classList.toggle("on", t.dataset.zhm === e));
    if ("ar" === e) return;
    a(".item[data-id]", t).forEach((t) => {
      if (t.dataset.zh) return;
      const e = t.dataset.id,
        i = /^v(\\d+)g/.exec(e || "");
      if (!i || "string" != typeof ($t[+i[1]] || {}).zh) return;
      t.dataset.zh = "1";
      zhLoad(+i[1])
        .then((i) => {
          const c = i.he[e.slice(e.indexOf("g") + 1)],
            a = l(".txt", t);
          if (!c || !a) return void t.classList.add("zh-nohe");
          const o = document.createElement("div");
          ((o.className = "zh-heb"), (o.innerHTML = c), a.appendChild(o));
        })
        .catch(() => {
          (delete t.dataset.zh, t.classList.add("zh-nohe"));
        });
    });
  }
  try {
    new MutationObserver(() => setTimeout(zhApply, 40)).observe(document.getElementById("reader"), { childList: !0 });
  } catch (t) {}
  document.addEventListener(
    "click",
    (t) => {
      const e = t.target.closest && t.target.closest("[data-zhm]");
      e && (t.preventDefault(), t.stopPropagation(), s.set("zhMode", e.dataset.zhm), zhApply());
    },
    !0,
  );
  function pi(t) {
    const e = $t[t];
    if (e && "string" == typeof e.zh) {
      const t = zhMode(),
        i = (e, i) => '<button type="button" data-zhm="' + e + '"' + (t === e ? ' class="on"' : "") + ">" + i + "</button>";
      return (
        '<div class="tn-bar">' +
        i("both", "📖 ארמית ולשון הקודש") +
        i("ar", "ארמית בלבד") +
        i("he", "לשון הקודש בלבד") +
        '</div><div class="tn-hint">' +
        hi(
          "<b>ארמית ולשון הקודש</b> – כל קטע בלשון הזוהר, ומתחתיו התרגום ללשון הקודש.<br><b>ארמית בלבד</b> – לשון הזוהר בלבד.<br><b>לשון הקודש בלבד</b> – רק התרגום (קטע שאין לו תרגום מוצג בארמית)." +
            (e.credit ? "<br><small>" + o(e.credit) + "</small>" : ""),
        ) +
        "</div>"
      );
    }
    if (e && e.mg) {''')
rep('''            t.querySelectorAll(".smt2,.smt3,.rs-box.open,.mg-p.open").forEach((e) => {
              const i =''','''            t.querySelectorAll(".smt2,.smt3,.rs-box.open,.mg-p.open,.zh-heb").forEach((e) => {
              if (!e.offsetParent) return;
              const i =''')
open(p,'w',encoding='utf-8').write(s); print('patched')
p='shell.html'; s=open(p,encoding='utf-8').read()
a="  .mg-box{display:none;margin-top:8px}"
assert s.count(a)==1
s=s.replace(a,'''  .zh-heb{margin:8px 0 2px;padding:9px 12px;border-radius:12px;background:var(--soft,rgba(176,138,58,.08));border-inline-start:3px solid var(--accent,#b08a3a);font-size:.92em;line-height:1.75;text-align:justify}
  #reader.zh-ar .zh-heb{display:none}
  #reader.zh-he .item[data-zh]:not(.zh-nohe) .txt > p{display:none}
  #reader.zh-he .zh-heb{background:none;border:0;padding:0;font-size:1em}
'''+a)
open(p,'w',encoding='utf-8').write(s)
