  // 🛠️ העוזר מבצע: פתח / תקריא (עם סימון) / תריץ את המסך / צור סטטוס / תזכיר לי
  const BOT_YT = "https://www.youtube.com/@yeshurun148";
  const bcN = (t) =>
    String(t || "")
      .replace(/[֑-ׇ]/g, "")
      .replace(/(^|\s)(ליקו|לקו)["״]מ/g, "$1ליקוטי מוהרן")
      .replace(/(^|\s)(ליקו|לקו)["״]ה/g, "$1ליקוטי הלכות")
      .replace(/["'׳״`]/g, "")
      .replace(/[^א-ת0-9 ]/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  const bcF = (t) => t.replace(/ך/g, "כ").replace(/ם/g, "מ").replace(/ן/g, "נ").replace(/ף/g, "פ").replace(/ץ/g, "צ");
  const bcS = (t) =>
    bcF(t)
      .split(" ")
      .map((t) => (t.length > 1 ? t[0] + t.slice(1).replace(/[וי]/g, "") : t))
      .join(" ");
  const GV = { א: 1, ב: 2, ג: 3, ד: 4, ה: 5, ו: 6, ז: 7, ח: 8, ט: 9, י: 10, כ: 20, ך: 20, ל: 30, מ: 40, ם: 40, נ: 50, ן: 50, ס: 60, ע: 70, פ: 80, ף: 80, צ: 90, ץ: 90, ק: 100, ר: 200, ש: 300, ת: 400 };
  function gmv(t) {
    if (/^\d+$/.test(t)) return +t;
    let e = 0,
      i = 1e4;
    for (const c of t) {
      const t = GV[c];
      if (!t) return 0;
      if (t > i && !(9 === i && (6 === t || 7 === t))) return 0;
      ((e += t), (i = t));
    }
    return e;
  }
  let bcBooks = null;
  function bcBook(q) {
    bcBooks ||
      ((bcBooks = $t.map((t, e) => (t && !t.hidden && t.title ? { v: e, sk: bcS(bcN(m(String(t.title)))) } : null)).filter((t) => t && t.sk)),
      [
        ["ליקומ", 0],
        ["ליקוה", 4],
        ["תהלמ", 17],
        ["התקנ הכלל", 23],
        ["תקנ כלל", 23],
      ].forEach((t) => bcBooks.push({ v: t[1], sk: t[0] })));
    const e = " " + bcS(q) + " ";
    let i = null;
    for (const t of bcBooks) {
      const c = new RegExp("(^| )[והבלמש]?" + t.sk.replace(/ /g, " [והבלמש]?") + "(?= |$)").exec(e);
      c && (!i || t.sk.length > i.sk.length) && (i = Object.assign({ at: c.index + c[0].length - 1 }, t));
    }
    return i;
  }
  function bcChapter(v, q, after) {
    const P = /(^| )[בו]?חלק (ב|שני|השני)( |$)|תנינא/.test(q) ? 2 : /(^| )[בו]?חלק (א|ראשון|הראשון)( |$)/.test(q) ? 1 : 0;
    let num = 0;
    const T = /(?:^| )[בלומ]?(?:תורה|פרק|הלכה|שיחה|מעשה|סימן|מזמור|אות|מאמר|דף)\s+([א-ת]{1,4}|\d{1,3})(?= |$)/.exec(q);
    if (T) num = gmv(T[1]);
    else {
      const k = bcS(q).slice(0, after).trim().split(" ").length,
        t = q.split(" ")[k] || "";
      /^([א-ת]{1,4}|\d{1,3})$/.test(t) && !/^(עמ|את|של|לי|כל|מה|אמ|גמ|זה|זו|בו|בה|לו|לה|המ|הנ|כי|אכ|רק|עד|אל|על|מנ|כנ|לא|יש|אז|פה|שמ)$/.test(bcF(t)) && (num = gmv(t));
    }
    const S = [];
    n.forEach((t, e) => {
      t.g === "V" + v && (!P || (1 === P ? /חלק א|ראשון/ : /חלק ב|שני|תנינא/).test(m(String(t.short || "")))) && S.push(e);
    });
    if (!S.length) return null;
    if (!num) return { si: S[0], ci: 0, first: !0 };
    for (const t of S)
      for (let e = 0; e < n[t].c.length; e++) {
        const i = /^\s*(?:תורה|פרק|הלכה|שיחה|מעשה|סימן|מזמור|אות|מאמר|דף)?\s*([א-ת"'׳״]{1,6}|\d{1,3})(?=[\s\-–:.,]|$)/.exec(m(g(String(n[t].c[e].t || ""))));
        if (i && gmv(i[1].replace(/["'׳״]/g, "")) === num) return { si: t, ci: e };
      }
    return { si: S[0], ci: 0, miss: num };
  }
  function botCmd(t) {
    const q = bcN(t),
      R = /(תקריא|הקרא|הקראה|תקרא לי|קרא לי|תקריאי|להקריא|הקריא)/.test(q),
      H = /(סימון|סמן|הדגשה|עוקב|מודגש)/.test(q),
      C = /(תריצ|תריץ|הרצ|הרץ|גלילה|תגלול|גלול|להריצ|להריץ|ריצה)/.test(q),
      ST = /(סטטוס|סטורי|תמונה לשיתוף|כתמונה|תמונה יפה)/.test(q),
      O = /(^| )(פתח|תפתח|פתחי|תפתחי|תביא לי|קח אותי|תעביר אותי|לך ל|תראה לי|הצג)/.test(q),
      RM = /(^| )(תזכיר לי|תזכירי לי|תזכורת|להזכיר לי|תעשה לי תזכורת)( |$)/.test(q);
    if (RM && !/(איך|מה זה|איפה)/.test(q)) {
      const e = q
        .replace(/(^| )(תזכיר לי|תזכירי לי|תעשה לי תזכורת|תזכורת|להזכיר לי|אפשר|בבקשה|רוצה|לקבוע|תקבע|לי|על|ל)(?= |$)/g, " ")
        .replace(/\s+/g, " ")
        .trim();
      const i = /חצות/.test(e) ? 27 : /תיקון הכללי|תקון הכללי/.test(e) ? 23 : /תהלים|תהילים/.test(e) ? 17 : -1;
      return { say: "⏰ פותח לך תזכורת" + (e ? " – «" + o(e) + "»" : "") + ". בוחרים שעה וימים, וזה יקפוץ כהתראה.", run: () => Xl({ nav: { v: "home", p: i >= 0 ? { b: i } : {} }, lbl: e || "תזכורת", free: 1 }) };
    }
    if (!(R || C || ST || O)) return null;
    const B = bcBook(q);
    if (!B) {
      if ((R || C) && "reader" === Bt.v)
        return { say: R ? "🔊 מקריא לך מהמקום שבו אתה נמצא" + (H ? " – עם סמן עוקב" : "") : "⏬ מריץ את המסך", run: () => (R ? (H && s.set("ttsHl", !0), mf.fromItem(wi())) : ld.start()) };
      return null;
    }
    const nm = m(String(($t[B.v] || {}).title || ""));
    const ch = bcChapter(B.v, bcF(q), B.at);
    if (!ch) return null;
    const c = n[ch.si].c[ch.ci],
      lbl = nm + (ch.first ? "" : " · " + m(g(String(c.t || ""))).split(/ [-–] /)[0]),
      fid = (c.i && c.i[0] && c.i[0].id) || null,
      tk = 23 === B.v || "tikkun" === n[ch.si].id,
      acts = [];
    (R && acts.push("מקריא" + (H ? " עם סמן עוקב" : "")), C && acts.push("מריץ את המסך"), ST && acts.push("מכין סטטוס לשיתוף"));
    return {
      say: "📖 פותח לך את <b>" + o(lbl) + "</b>" + (ch.miss ? " (לא מצאתי את המספר " + ch.miss + " – פתחתי מההתחלה)" : "") + (acts.length ? " ו" + acts.join(" ו") : "") + "…",
      run: () => {
        (tk ? It("tikkun") : We(ch.si, ch.ci),
          setTimeout(() => {
            try {
              if (R) {
                H && s.set("ttsHl", !0);
                const t = tk ? l("#tkRead") : null;
                t ? t.click() : fid && mf.fromItem(fid);
              }
              (C && setTimeout(() => ld.start(), R ? 600 : 0), ST && fid && kf(fid));
            } catch (t) {
              console.warn(t);
            }
          }, 900));
      },
    };
  }
  window.__botCmd = (t) => {
    const e = botCmd(t);
    return e && e.say;
  };

  // 💡 העוזר מציע – מדי פעם, לפי היום, השעה והלוח
  function botTipPick() {
    const t = new Date(),
      e = t.getHours(),
      L = [];
    try {
      const t = xs(0),
        i = Ss(0),
        c = [ws(t), (Ms(0) || {}).n].filter(Boolean)[0],
        a = (_o(t) || []).map(Xo)[0];
      (i && L.push(["hanuka", "🕎 הי אחי, היום נר " + i + " של חנוכה! רוצה לשמוע דיבור חזק על חנוכה?", "כן, תביא!", () => botOpen("תורה על חנוכה")]),
        c && L.push(["hag", "✨ היום " + o(String(c)) + " – רוצה לראות מה רבנו אומר על זה?", "כן!", () => botOpen("תורה על " + String(c).split(/[ ·]/)[0])]),
        a && L.push(["hil", "🕯️ היום הילולת " + o(m(g(String(a)))).slice(0, 70) + " – רוצה לראות בלוח ההילולות?", "פתח", () => It("calendar")]));
    } catch (t) {}
    (5 === t.getDay() && e >= 9 && e < 17 && L.push(["shabbat", "🕯️🕯️ הי צדיק, רוצה לדעת מתי נכנסת שבת?", "כן", () => botOpen("מתי נכנסת שבת")]),
      (e >= 21 || e < 2) && L.push(["chatzot", "🌙 מה קורה אחי? רוצה שאזכיר לך לקום לתיקון חצות?", "כן, תזכיר לי", () => Xl({ nav: { v: "home", p: { b: 27 } }, lbl: "🌙 תיקון חצות", free: 1 })]),
      e >= 6 && e < 10 && L.push(["shma", "☀️ בוקר טוב! רוצה שאזכיר לך לקרוא קריאת שמע בזמן?", "כן", () => Xl({ nav: { v: "home", p: {} }, lbl: "קריאת שמע בזמן", free: 1 })]));
    const G = [
      ["booklet", "📒 ידעת שאני יכול להכין לך חוברת להדפסה על כל נושא? רק תכתוב לי על מה.", "נסה עכשיו", () => botOpen("צור לי חוברת על ", 1)],
      ["tts", '🔊 אני יכול להקריא לך – למשל "תקריא לי את התיקון הכללי עם סימון".', "נסה עכשיו", () => botOpen("תקריא לי את התיקון הכללי עם סימון")],
      ["find", "📚 אני יכול למצוא לך כל ספר במאגר ולפתוח אותו. תכתוב לי שם של ספר.", "נסה", () => botOpen("פתח לי ", 1)],
      ["goals", "🎯 אני יכול לעזור לך לעמוד ביעדים שלך – עם תזכורת כל יום.", "ליעדים שלי", () => goalsOpen()],
      ["status", "🖼️ היי חבר, רוצה שאכין לך סטטוס יפה עם דיבור חיזוק מרבנו לשתף?", "כן!", () => botStatus()],
      ["help", "🤝 צריך עזרה? אני יכול ללמד אותך איך לעבוד עם האפליקציה.", "בוא נתחיל", () => botOpen()],
      ["scroll", '📜 אני יכול לפתוח לך תהלים ולהריץ את המסך – "פתח לי תהלים פרק צ ותריץ את המסך".', "נסה", () => botOpen("פתח לי תהלים פרק צ ותריץ את המסך")],
      ["src", '💡 תשאל אותי על הספרים – "איפה רבנו מדבר על שמחה", "כמה תורות יש בחלק ב׳"…', "לשאול", () => botOpen()],
      ["yt", "🎵 הערוץ שלנו ביוטיוב – ניגונים, שירים וחיזוקים. רוצה להציץ?", "לערוץ", () => NAT.openUrl(BOT_YT)],
    ];
    const D = s.get("botTipDone", {});
    return L.find((t) => (D[t[0]] || "") !== new Date().toDateString()) || G.sort((t, e) => (D[t[0]] || 0) - (D[e[0]] || 0))[0];
  }
  function botStatus() {
    const P = (t) => t.it.b.reduce((t, e) => t + ("p" === e[0] ? e[1].length : 0), 0),
      t = h.filter((t) => [0, 8, 3].includes(+String(t.s.g).slice(1)) && t.it && t.it.b && P(t) > 120 && P(t) < 520);
    t.length ? kf(t[Math.floor(Math.random() * t.length)].id) : st("לא מצאתי דיבור קצר");
  }
  function botTip(force) {
    try {
      if (!s.get("botTips", !0) || Gt || (mf && mf.on) || ld.on || (!force && "reader" === Bt.v)) return;
      const t = Date.now();
      if (!force && t - s.get("botTipT", 0) < 3 * 36e5) return;
      const e = botTipPick();
      if (!e) return;
      s.set("botTipT", t);
      const i = s.get("botTipDone", {});
      ((i[e[0]] = /^(hanuka|hag|hil|shabbat|chatzot|shma)$/.test(e[0]) ? new Date().toDateString() : t), s.set("botTipDone", i));
      let c = document.getElementById("botTip");
      (c && c.remove(),
        (c = document.createElement("div")),
        (c.id = "botTip"),
        (c.innerHTML =
          '<span class="bot-av"></span><div class="bt-b"><p>' +
          e[1] +
          '</p><div class="bt-a"><button class="btn sm pri" data-a="y">' +
          e[2] +
          '</button><button class="btn sm" data-a="n">לא עכשיו</button></div><button class="bt-off" data-a="off">אל תציע לי יותר</button></div><button class="bt-x" data-a="n" aria-label="סגירה">✕</button>'),
        document.body.appendChild(c),
        requestAnimationFrame(() => c.classList.add("on")));
      const a = () => (c.classList.remove("on"), setTimeout(() => c.remove(), 400));
      ((c.onclick = (t) => {
        const i = t.target.closest("[data-a]");
        i && ("y" === i.dataset.a ? (a(), setTimeout(e[3], 120)) : "off" === i.dataset.a ? (s.set("botTips", !1), a(), st("בסדר 🙂 אפשר להחזיר בהגדרות ← העוזר", 3e3)) : a());
      }),
        setTimeout(a, 2e4));
    } catch (t) {
      console.warn("botTip", t);
    }
  }
  (setTimeout(botTip, 6e4), setInterval(botTip, 15 * 6e4));
  window.__botTip = () => botTip(!0);
