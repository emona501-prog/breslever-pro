  // 🕯️ זמנים בצ׳אט: "מתי נכנסת שבת", "מתי השקיעה היום" – תשובה מדויקת לפי העיר (שואל על העיר בפעם הראשונה)
  let botCityQ = null;
  const ZMK = [
    [/הדלקת נרות|כניסת השבת|נכנס(ת)? (ה)?שבת|שבת נכנס/, "shab"],
    [/צאת השבת|יציאת השבת|מוצאי שבת|מוצאש|יוצא(ת)? (ה)?שבת|שבת יוצא/, "shab"],
    [/זמני שבת|שבת/, "shab"],
    [/רבנו תמ|רבינו תמ/, "rt"],
    [/צאת הכוכבימ|צאת הכוכבים|צה"כ/, "tzeit"],
    [/חצות הלילה|חצות לילה|תיקונ חצות|תיקון חצות/, "chatzotLayla"],
    [/חצות/, "chatzot"],
    [/שקיעה|השקיעה/, "set"],
    [/זריחה|הזריחה|הנצ|הנץ|נצ החמה/, "rise"],
    [/עלות השחר|עלות/, "alos"],
    [/טלית|תפילינ|תפלין|משיכיר/, "mishyakir"],
    [/קריאת שמע|קש|ק ש/, "shma"],
    [/סופ זמנ תפילה|סוף זמן תפילה|זמנ תפילה|זמן תפילה|שחרית/, "tfila"],
    [/מנחה גדולה/, "minchaG"],
    [/מנחה קטנה|מנחה/, "minchaK"],
    [/פלג/, "plag"],
  ];
  const zmLoc = (e) => ({ name: e[0], lat: e[1], lon: e[2], cl: e[3], el: e[4] });
  function botCityFind(t) {
    const e = " " + bcS(bcN(t)) + " ";
    let i = null;
    return (
      as.forEach((t) => {
        const c = bcS(bcN(t[0]));
        new RegExp(" [בלמו]?" + c + "( |$)").test(e) && (!i || c.length > bcS(bcN(i[0])).length) && (i = t);
      }),
      i
    );
  }
  function botZmAns(t, forced) {
    const q = bcF(bcN(t));
    if (!forced) {
      if (/(^| )(איפה|רבנו|רבינו|תורה|מקור|מקורות|כמה תורות|הלכה|דיבור|חיזוק|ספר)( |$)/.test(q)) return null;
      if (!/(^| )(מתי|באיזה שעה|באיזו שעה|מה השעה|שעת|זמנ|זמני|עד מתי|עד איזה שעה|עד איזו שעה|תגיד לי)( |$)/.test(q) && !/(הדלקת נרות|צאת השבת|כניסת השבת|מוצאי שבת|זמני שבת)/.test(q)) return null;
    }
    const K = (ZMK.find((t) => t[0].test(q)) || [])[1];
    if (!K) return null;
    const C = botCityFind(t),
      saved = s.get("zmCity", null);
    if (!C && !saved && !s.get("zmCityOk", !1)) return { ask: 1 };
    const L = C ? zmLoc(C) : ps(),
      mine = !C || (saved && saved.name === C[0]) || (!saved && "ירושלים" === C[0]),
      tm = /(^| )(מחר|למחר)( |$)/.test(q) ? 1 : 0,
      acts = [],
      b = (t, e, i) => (acts.push(e), '<button class="btn sm' + (i ? " pri" : "") + '" data-zq="' + (acts.length - 1) + '">' + t + "</button>");
    let x = "";
    if ("shab" === K) {
      let e = 0;
      for (6 === Cs(0) && (e = -1); 5 !== Cs(e); ) e++;
      const i = ms(e, L),
        c = ms(e + 1, L),
        a = mine ? yn(L) : L.cl || 20,
        n = Ts(e).n || "",
        r = -1 === e;
      x =
        '<div class="bot-say bot-zm">🕯️ <b>' +
        (r ? "השבת" : "שבת") +
        (n ? " " + o(n) : "") +
        "</b> · " +
        o(L.name) +
        "<br>" +
        (r ? "" : "הדלקת נרות: <b>" + zs(i.v.set - a * ls.MIN, "dn") + "</b> <small>(" + a + " דק׳ לפני השקיעה)</small><br>") +
        (r ? "השבת יוצאת היום – " : "") +
        "צאת השבת: <b>" +
        zs(c.v.tzeitShabat, "up") +
        "</b> · ר״ת: " +
        zs(c.v.rt, "up") +
        '<br><small>ערב שבת: ' +
        o(js(e)) +
        "</small></div>";
    } else {
      const e = ms(tm, L),
        i = (t) => zs(e.v[t], (os.find((e) => e[0] === t) || [])[2] || "n"),
        c = {
          shma: [["shmaGra", 'סוף זמן קריאת שמע – גר"א'], ["shmaMga", "סוף זמן קריאת שמע – מגן אברהם"]],
          tfila: [["tfilaGra", 'סוף זמן תפילה – גר"א'], ["tfilaMga", "סוף זמן תפילה – מגן אברהם"]],
        }[K] || [[K, (os.find((t) => t[0] === K) || [K, K])[1]]];
      x =
        '<div class="bot-say bot-zm">🕰️ <b>' +
        (tm ? "מחר" : "היום") +
        "</b> · " +
        o(L.name) +
        "<br>" +
        c.map((t) => o(t[1]) + ": <b>" + i(t[0]) + "</b>").join("<br>") +
        "<br><small>" +
        o(js(tm)) +
        "</small></div>";
    }
    x +=
      '<div class="bot-zl">מקור: לוח הזמנים באפליקציה – ' +
      b("לחץ כאן", () => (Wt(), setTimeout(() => ("shab" === K ? botZm(0) : botZm(-1)), 230))) +
      ("shab" === K ? " (כל הערים ופרשת השבוע)" : " (כל זמני היום)") +
      "</div>" +
      '<div class="bot-srcs">' +
      (C && !mine ? b("📍 לקבוע את " + o(C[0]) + " כעיר שלי", () => (s.set("zmCity", zmLoc(C)), s.set("zmCityOk", !0), st("📍 העיר נשמרה: " + C[0]))) : "") +
      b("📍 עיר אחרת?", () => "city") +
      "</div>";
    return { html: x, acts };
  }
  function botCityAskHtml(t) {
    return (
      '<div class="bot-say">📍 ' +
      (t || "באיזו עיר אתה? כדי שאתן לך את הזמן המדויק.") +
      '</div><div class="bot-chips">' +
      as
        .slice(0, 12)
        .map((t) => '<button class="pill" data-city="' + o(t[0]) + '">' + o(t[0]) + "</button>")
        .join("") +
      '</div><div class="bot-scope">או כתבו את שם העיר בשורה למטה.</div>'
    );
  }
