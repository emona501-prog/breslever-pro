  // 🧭 העוזר מוביל: "מה ללמוד?" ← שואל איזה נושא חשוב לך ← דיבורים מכמה ספרים שונים
  let botTopicQ = !1;
  const BOT_TOPICS = [["🙏", "תפילה"], ["✨", "אמונה"], ["😊", "שמחה"], ["🌙", "התבודדות"], ["↩️", "תשובה"], ["🛡️", "בטחון"], ["💰", "פרנסה"], ["🏠", "שלום בית"], ["👁️", "שמירת עיניים"], ["🌱", "ענוה"], ["📖", "לימוד תורה"], ["🕯️", "שבת"]];
  const BOT_GUIDE = /(מחפש ללמוד|רוצה ללמוד|מה ללמוד|מה אפשר ללמוד|מה כדאי ללמוד|מה אתה מציע|מה תציע|תציע לי|תמליצ|תמליץ|המלצה|לא יודע מה ללמוד|על מה ללמוד|משהו ללמוד|תנ לי משהו ללמוד|תן לי משהו ללמוד|ללמוד משהו|בא נלמד|בוא נלמד|נלמד משהו|שיעור קצר|לימוד קצר)/;
  const BOT_PACKV = () => {
    const t = (t) => $t.findIndex((e) => e && m(String(e.title || "")) === t);
    return [0, 4, 11, 8, 47, t("השתפכות הנפש"), 12].filter((t) => t >= 0 && $t[t]);
  };
  function botTopicAsk() {
    botTopicQ = !0;
    return (
      '<div class="bot-say">בשמחה, אח יקר! 😊 בוא נלמד ביחד.<br><b>איזה נושא הכי חשוב לך עכשיו?</b></div><div class="bot-chips">' +
      BOT_TOPICS.map((t) => '<button class="pill" data-tp="' + o(t[1]) + '">' + t[0] + " " + o(t[1]) + "</button>").join("") +
      '<button class="pill" data-tp="*">🎲 תפתיע אותי</button></div><div class="bot-scope">או כתבו נושא אחר בשורה למטה.</div>'
    );
  }
  function botPackHtml(t, k) {
    const e = botQAget(),
      i = e.pack(t, BOT_PACKV(), k || 0),
      acts = [];
    if (!i.length) return null;
    const c = (t) => (acts.push(t), acts.length - 1);
    let x =
      '<div class="bot-say">' +
      (k ? "הנה עוד כמה דיבורים על <b>" + o(t) + "</b> 💎" : ["בשמחה! 🙏", "איזה נושא נפלא! ✨", "יופי, אחי! 😊"][Math.floor(3 * Math.random())] + " הנה כמה דיבורים נפלאים על <b>" + o(t) + "</b>, מכמה ספרים שונים:") +
      "</div>";
    i.forEach((t) => {
      const i = e.snip(t.c.bi, t.c.H),
        a = h[t.c.bi].id;
      let l = o(i.text);
      t.R.forEach((t) => {
        try {
          l = l.replace(new RegExp(t.source, "g"), (t, e) => t.slice(0, t.length - e.length) + "<mark>" + e + "</mark>");
        } catch (t) {}
      });
      x +=
        '<div class="bot-a bot-chz"><div class="bot-where">📖 ' +
        o(e.where(t.c.bi)) +
        '</div><p class="bot-snip">' +
        (i.pre ? "…" : "") +
        l +
        (i.post ? "…" : "") +
        '</p><div class="bot-srcs"><button class="btn sm" data-pk="' +
        c(() => Ye(a)) +
        '">👈 לפתוח במקום</button><button class="btn sm" data-pk="' +
        c(() => kf(a)) +
        '">🖼️ לסטטוס</button></div></div>';
    });
    x +=
      '<div class="bot-srcs" style="margin-top:8px"><button class="btn sm pri" id="pkMore">💎 עוד דיבורים</button><button class="btn sm" data-pk="' +
      c(() => botBooklet(t)) +
      '">📒 חוברת על ' +
      o(t) +
      '</button><button class="btn sm" id="pkOther">🧭 נושא אחר</button></div>';
    return { html: x, acts };
  }
