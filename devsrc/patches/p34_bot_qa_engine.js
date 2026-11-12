// 🤖 שלב 1: שאלות על תוכן הספרים – בלי בינה מלאכותית. מקור משותף לאב-טיפוס (node) ולאפליקציה.
function botQAMake(E) {
  // E: { N, T(i) טקסט מנורמל, V(i) כרך, ID(i), SEC(i), CH(i), B: books[], rc(term,loose), cc }
  const fin = (s) => s.replace(/ך/g, "כ").replace(/ם/g, "מ").replace(/ן/g, "נ").replace(/ף/g, "פ").replace(/ץ/g, "צ");
  const pre = (s) =>
    String(s || "")
      .replace(/[֑-ׇ]/g, "")
      .replace(/ע["״]י/g, "על ידי")
      .replace(/(^|\s)ר['׳](?=\s|[א-ת])/g, "$1רבי ")
      .replace(/(^|\s)(ליקו|לקו)["״]מ/g, "$1ליקוטי מוהרן")
      .replace(/(^|\s)(ליקו|לקו)["״]ה/g, "$1ליקוטי הלכות")
      .replace(/(^|\s)(ליקו|לקו)["״]ע/g, "$1ליקוטי עצות")
      .replace(/(^|\s)(ליקו|לקו)["״]ת/g, "$1ליקוטי תפילות")
      .replace(/(^|\s)שו["״]ע/g, "$1שולחן ערוך")
      .replace(/(^|\s)(רנ["״]ת|מוהרנ["״]ת|מוהרנת)/g, "$1מוהרנת")
      .replace(/ז["״]ל|זצ["״]ל|זיע["״]א/g, " ");
  const norm = (s) =>
    pre(s)
      .replace(/["'׳״`“”’]/g, "")
      .replace(/[^א-תa-z0-9 ]/gi, " ")
      .replace(/\s+/g, " ")
      .trim();
  // שלד: בלי ו/י (חוץ מאות ראשונה) – כדי שכתיב מלא/חסר לא יפריע
  const sk = (w) => ((w = fin(w)), w.length > 1 ? w[0] + w.slice(1).replace(/[וי]/g, "") : w);
  const skl = (s) => norm(s).split(" ").filter(Boolean).map(sk);
  const PFX = /^[והבלשמכ]/;

  // ---- היקף: ספרים, יחידות, מחברים ----
  const B = E.B;
  const vols = (f) => B.map((b, i) => (b && !b.hidden && f(b, i) ? i : -1)).filter((i) => i >= 0);
  const BRES = vols((b, i) => ["rn", "rnt", "anash", "tcherin"].includes(b.cat) && ![1, 26].includes(i));
  const STORY = [2, 5, 8, 9, 10, 24, 25, 48, 110, 111, 112];
  const ALIAS = []; // {w:[skel...], vols, lbl, kind}
  const al = (txt, vs, lbl, kind) => txt.split("|").forEach((t) => ALIAS.push({ w: skl(t), vols: vs, lbl, kind }));
  B.forEach((b, i) => {
    if (!b || b.hidden || !["rn", "rnt", "anash", "tcherin"].includes(b.cat)) return;
    al(b.title, [i], b.title, "book");
  });
  al("ליקוטי מוהרן|ספר ליקוטי מוהרן|ליקוטי מוהרן חלק א|ליקוטי מוהרן חלק ב|ליקומ", [0], "ליקוטי מוהר״ן", "book");
  al("ליקוטי הלכות|ליקוה", [4], "ליקוטי הלכות", "book");
  al("סיפורי מעשיות|ספורי מעשיות|הסיפורי מעשיות", [2], "סיפורי מעשיות", "book");
  al("ספר המידות|ספר המדות", [3], "ספר המידות", "book");
  al("שיחות הרן|שיחות רבנו", [8], "שיחות הר״ן", "book");
  al("חיי מוהרן", [9], "חיי מוהר״ן", "book");
  al("שבחי הרן", [10], "שבחי הר״ן", "book");
  al("ליקוטי עצות", [11], "ליקוטי עצות", "book");
  al("ליקוטי תפילות", [12], "ליקוטי תפילות", "book");
  al("מכתבי מוהרנת|עלים לתרופה", [47], "עלים לתרופה", "book");
  al("ימי מוהרנת", [24], "ימי מוהרנ״ת", "book");
  al("שיח שרפי קודש|שיש|שיח שרפי קדש", [110], "שיח שרפי קודש", "book");
  al("כוכבי אור", [5], "כוכבי אור", "book");
  al("זוהר|הזוהר|ספר הזוהר|זוהר הקדוש", vols((b) => b.cat === "zohar"), "הזוהר", "book");
  al("שולחן ערוך", vols((b) => b.cat === "sa" && b.title.indexOf("חשיבות") < 0), "שולחן ערוך", "book");
  al("תנך", vols((b) => b.cat === "tanach"), "תנ״ך", "book");
  // מחברים
  al("רבי נתן|מוהרנת|רבי נתן מברסלב|רבינו נתן", vols((b) => b.cat === "rnt"), "ספרי רבי נתן", "auth");
  al("רבי אברהם בר נחמן|רבי אברהם בן רבי נחמן|רבי אברהם בן נחמן|רבי אברהם בר רבי נחמן|רבי אברהם חזן|רבי אברהם חזאן|רבי אברהם בן רבי נחמן מטולטשין", vols((b) => /אברהם בן רבי נחמ/.test(b.author || "")), "ספרי רבי אברהם בן רבי נחמן", "auth");
  al("רבי נחמן מטשערין|רבי נחמן מטשרין|הרב מטשערין|הרב מטשרין", vols((b) => b.cat === "tcherin"), "ספרי הרב מטשערין", "auth");
  // יחידות (תורה/הלכה/שיחה...)
  const UNITS = [
    ["תורה|תורות|התורה|בתורה|התורות|מאמר|המאמר|מאמרים", [0], "ליקוטי מוהר״ן", "תורות"],
    ["הלכה|הלכות|ההלכה|בהלכה|ההלכות", [4], "ליקוטי הלכות", "הלכות"],
    ["שיחה|שיחות|השיחה|בשיחה|השיחות", [8, 9, 110], "השיחות", "שיחות"],
    ["סיפור|סיפורים|ספורים|הסיפור|הסיפורים|מעשה|מעשיות|מעשיות|סיפורי", STORY, "ספרי הסיפורים", "סיפורים"],
    ["עצה|עצות|העצה|העצות|עצת", [11, 41, 45], "ליקוטי עצות", "עצות"],
    ["תפילה|תפילות|התפילה|בתפילה|תפלה|תפלות", [12, 46], "ליקוטי תפילות", "תפילות"],
    ["מכתב|מכתבים|המכתב|המכתבים", [47], "עלים לתרופה", "מכתבים"],
    ["סימן|סימנים|הסימנים|סעיף|סעיפים|הסעיפים", vols((b) => b.cat === "sa" && b.title.indexOf("חשיבות") < 0), "שולחן ערוך", "סימנים"],
  ].map(([w, v, lbl, pl]) => ({ w: new Set(w.split("|").map((t) => sk(norm(t)))), vols: v, lbl, pl }));
  ALIAS.sort((a, b) => b.w.length - a.w.length);

  const STOP = new Set(
    (
      "המילה מילה המלה מלה המילים מילים הביטוי ביטוי המושג מושג השם איפה היכן באיזה באיזו איזה איזו איזהו מה מי מהו מהי מהם יש האם הם על של שלו את עם כמה פעמים פעם מופיע מופיעה מופיעים מופיעות מוזכר מוזכרת מוזכרים נזכר נזכרת נאמר נאמרה נאמרו אמר אומר אמרו כתוב כתובה כתובים כותב מדבר מדברת מדברים מדובר מביא מובא מובאת הכי ביותר בה בו לי לנו אני רוצה תגיד תראה תמצא תביא מקור מקורות המקור ענין עניין העניין הענין נושא בנושא בעניין לגבי אודות מעלת מעלה מעלות גודל חשיבות ספר בספר הספר הספרים ספרי שם כל או גם אם כי זה זו הזה הזאת זאת שבו שבה ידי על בא באה שהוא שהיא הוא היא רבנו רבינו רבי מוהרן הקדוש הקדושה בבקשה אפשר צריך למצוא לחפש חפש מחפש מצא דבר דברים בעניין יותר פחות ארוכה ארוך קצרה קצר הארוכה הארוך הקצרה הקצר ארוכות להינצל להנצל להימלט ניצול נגד לבטל לשבר להתגבר איך מה לעשות כשיש כשאני תרופה סגולה"
    )
      .split(" ")
      .map((t) => sk(norm(t))),
  );
  // "רבנו" לא בשאלה רגילה – אבל בתוך ביטוי ("לשון רבנו") נשאר: מטפלים בזה בבניית הביטויים

  // ---- עובדות מתועדות (רק ממה שכתוב בספרים שבאפליקציה) ----
  const FACTS = [
    {
      m: [["אמו", "אמא", "אימו", "אמה", "אם", "אמא של"], ["רבנו", "רבינו", "מוהרן", "רבי נחמן", "הרן"]],
      a: "שם אמו של רבנו – <b>פֵיגָא</b> (בת אדל, בתו של הבעל שם טוב). רבנו עצמו אמר: \"ואני שמי נחמן בן פיגא\".",
      s: ["v5g1.2.13", "v110g1.11.24"],
    },
    {
      m: [["נולד", "לידה", "לידתו", "הולדת", "הולדתו", "נפטר", "פטירה", "פטירתו", "הסתלקות", "הסתלקותו", "הסתלק", "נסתלק", "יארצייט", "הילולא", "הילולה", "ההילולא", "ההילולה", "שנות חייו", "כמה שנים חי", "בן כמה היה", "בן כמה"], ["רבנו", "רבינו", "מוהרן", "רבי נחמן", "הרן", "הרבי"]],
      no: [["אזמרה", "תורה", "אמו", "אביו"]],
      a: "רבנו <b>נולד בראש חודש ניסן שנת תקל\"ב</b> (1772), ביום שבת, ו<b>נסתלק ביום ג' ח\"י תשרי שנת תקע\"א</b> (1810), בחול המועד סוכות, באומן – כבן שלושים ושמונה שנים וחצי.",
      s: ["v9g7.0.0", "v9g10.6.0", "v24g1.65.0"],
    },
    {
      m: [["אזמרה", "רפב", "אזמרה לאלקי בעודי", "נקודות טובות"], ["שנה", "שנת", "מתי", "תאריך", "נאמרה", "נאמר", "אמר", "אמרה", "באיזו", "באיזה"]],
      no: [["לילך", "ללכת", "הזהיר"]],
      a: "התורה <b>\"אזמרה לאלקי בעודי\"</b> (ליקוטי מוהר״ן א, רפ\"ב) נאמרה <b>בשמיני עצרת שנת תקס\"ח</b>.",
      s: ["v9g1.58.56", "v9g1.32.1", "v0g0.283.0"],
    },
    {
      m: [["הזהיר", "הזהירו", "ציוה", "ציווה", "צוה"], ["ללכת", "לילך", "ילך", "הולכים"], ["תורה", "תורות", "מאמר", "איזה", "איזו", "עם", "איתה", "אתה"]],
      a: "זו התורה <b>\"אזמרה לאלקי בעודי\"</b> – ליקוטי מוהר״ן חלק א׳ סימן רפ\"ב. שם כתוב: \"והזהיר רבנו, זכרונו לברכה, מאד לילך עם התורה הזאת, כי הוא יסוד גדול לכל מי שרוצה להתקרב להשם יתברך\". וכן בחלק ב׳ סימן מ\"ח: \"וראוי לילך עם מה שנאמר במאמר אזמרה\".",
      s: ["v0g0.283.0", "v0g1.44.0", "v9g21.125.1"],
    },
    {
      m: [["תרנגול", "הינדיק", "תרנגול הודו", "תרנגולת"], ["בן המלך", "בן מלך", "נסיך", "המלך", "מלך", "חשב", "שחשב", "משל", "מעשה", "סיפור", "המשל", "מתחת לשולחן", "שולחן"]],
      a: "זה <b>\"המשל מההינדיק\"</b> (תרנגול הודו) – בן מלך שנפל לשגעון שהוא תרנגול הודו, וישב ערום תחת השולחן, עד שבא חכם וריפא אותו לאט לאט. נמצא בסיפורי מעשיות, בין הסיפורים הקצרים.",
      s: ["v2g3.8.0"],
    },
    {
      m: [["תלמיד", "תלמידו", "תלמידיו", "תלמידים", "משמש", "ממשיך", "ממלא מקומו"], ["רבי נתן", "מוהרנת", "נתן"]],
      no: [["רבנו של"]],
      a: "בספרים שבאפליקציה <b>אין קביעה מפורשת</b> מי \"הגדול\" שבתלמידי מוהרנ״ת. מה שכן כתוב:<br>• <b>רבי נחמן מטולטשין</b> – \"תלמיד ומשמש מוהרנ״ת\", ששקד על דלתיו, נסע אליו פעמיים בחודש ושימש אותו לעת זקנתו.<br>• <b>רבי משה ברסלבר</b> – \"תלמיד מובהק של מוהרנ״ת\".",
      s: ["v5g9.4.8", "v5g7.3.22", "v110g2.2.15"],
    },
    {
      m: [["אדמוני", "גינגי", "גנגי", "גינגית", "אדום", "אדום שיער", "צבע שיער", "צבע השיער", "שערו", "שערותיו", "מראהו", "איך נראה", "מראה פניו"], ["רבנו", "רבינו", "מוהרן", "רבי נחמן", "הרן"]],
      a: "חיפשתי בכל הספרים שבאפליקציה – <b>לא מצאתי תיאור של צבע שערו או של מראה פניו של רבנו</b>, ולכן איני יכול לאשר או להכחיש. (מצאתי רק על מוהרנ״ת, ש\"פניו היו אדומות מרב התלהבותו\".) אם יש לך מקור – שלח אותו לעורך ונוסיף.",
      s: ["v110g1.15.8"],
      idea: 1,
    },
  ].map((f) => Object.assign(f, { mS: f.m.map((g) => g.map((t) => skl(t).join(" "))), noS: (f.no || []).map((g) => g.map((t) => skl(t).join(" "))) }));
  const hasAlt = (qs, alt) => new RegExp("(^| )([והבלשמכ]{1,2})?" + alt + "( |$)").test(qs);
  function fact(qs) {
    for (const f of FACTS) if (f.mS.every((g) => g.some((t) => hasAlt(qs, t))) && !f.noS.some((g) => g.some((t) => hasAlt(qs, t)))) return f;
    return null;
  }

  // ---- כלים לחיפוש ----
  const ESC = (t) => t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  // כתיב גמיש: מילה כפי שנכתבה + אפשר להוסיף ו/י בכל מקום (התבודדת → התבודדות),
  // או כתיב חסר מדויק בלי ו/י (תפילה → תפלה, עיקר → עקר). אות סופית בשאלה = סוף מילה בכתיב החסר.
  const FN = { ך: "כ", ם: "מ", ן: "נ", ף: "פ", ץ: "צ" },
    FX = { מ: "[מם]", נ: "[נן]", צ: "[צץ]", פ: "[פף]", כ: "[כך]" };
  const lt = (c) => FX[c] || ESC(c);
  function wordRe(w) {
    const end = /[ךםןףץ]$/.test(w),
      L = w.replace(/[ךםןףץ]/g, (c) => FN[c]).replace(/(.)וו/g, "$1ו").replace(/(.)יי/g, "$1י");
    if (L.length < 3) return E.cc + L.split("").map(lt).join("");
    const st = L.split("").map(lt).join("[וי]*"),
      d = L[0] + L.slice(1).replace(/[וי]/g, "");
    return E.cc + (d !== L && d.length >= 2 ? "(?:" + st + "|" + d.split("").map(lt).join("") + (end ? "(?![א-ת])" : "") + ")" : st);
  }
  // אות שימוש בתחילת מילה (מכעס, בלילה, התורה): מורידים אותה רק אם בלי האות המילה נפוצה הרבה יותר בספרים
  function cntRe(re, idx, cap) {
    let n = 0;
    for (const i of idx) if (re.test(E.T(i)) && ++n >= cap) break;
    return n;
  }
  function pickBase(w, idx) {
    let b = w;
    for (let k = 0; k < 2 && b.length > 3 && /^[והבלשמכ]/.test(b); k++) {
      const c = b.slice(1),
        n0 = cntRe(termRe([b]), idx, 600),
        n1 = cntRe(termRe([c]), idx, 600);
      if (n1 >= 1.5 * n0 + 2) b = c;
      else break;
    }
    return b;
  }
  function termRe(words, g) {
    const body = words.map((w) => wordRe(w)).join("[^א-ת]{1,3}");
    const tail = words.length === 1 && words[0].length <= 2 ? "(?![א-ת])" : "";
    return new RegExp("(?:^|[^א-ת])(" + body + ")" + tail, g ? "g" : "");
  }
  function inScope(sc) {
    const S = new Set(sc);
    const r = [];
    for (let i = 0; i < E.N; i++) S.has(E.V(i)) && r.push(i);
    return r;
  }
  const BW = { 0: 300, 8: 160, 9: 140, 2: 140, 4: 100, 11: 100, 10: 80, 3: 60 };
  const partOk = (P) => (P.part ? (i) => (1 === P.part ? /חלק א|חלק ראשון/ : /חלק ב|חלק שני|תנינא/).test(E.SEC(i) || "") : null);
  function scopeIdx(P) {
    const f = partOk(P),
      a = inScope(P.scope);
    return f ? a.filter(f) : a;
  }
  const ck = (i) => E.ID(i).replace(/\.\d+$/, "");
  const bookT = (i) => (B[E.V(i)] || {}).title || "";

  // ---- ניתוח השאלה ----
  function parse(q) {
    const raw = norm(q);
    let w = raw.split(" ").filter(Boolean);
    let s = w.map(sk);
    const qs = s.join(" ");
    // חלק א׳ / חלק ב׳ (תנינא)
    let part = 0;
    const P1 = new Set(["א", "ראשנ", "הראשנ", "קמא"]),
      P2 = new Set(["ב", "שני", "השני", "שנ", "השנ", "תננא"]);
    for (let i = 0; i < s.length; i++) {
      if (/^[בוש]?(ה)?חלק$/.test(s[i]) && i + 1 < s.length && (P1.has(s[i + 1]) || P2.has(s[i + 1]))) {
        ((part = P1.has(s[i + 1]) ? 1 : 2), w.splice(i, 2), s.splice(i, 2), i--);
      } else if (/^[בו]?תננא$/.test(s[i])) ((part = 2), w.splice(i, 1), s.splice(i, 1), i--);
    }
    let book = null,
      auth = null,
      unit = null;
    // כינויים של ספרים/מחברים – הארוך קודם
    for (const a of ALIAS) {
      const n = a.w.length;
      for (let i = 0; i + n <= s.length; i++) {
        let ok = true;
        for (let j = 0; j < n && ok; j++) {
          const x = s[i + j],
            y = a.w[j];
          ok = x === y || (j === 0 && x.length > y.length && PFX.test(x) && (x.slice(1) === y || x.slice(2) === y));
        }
        if (ok) {
          a.kind === "book" ? book || (book = a) : auth || (auth = a);
          w.splice(i, n);
          s.splice(i, n);
          i--;
        }
      }
    }
    // יחידה ראשונה בשאלה
    const keep = [],
      keepS = [];
    w.forEach((t, i) => {
      const u = UNITS.find((u) => u.w.has(s[i]));
      if (u) {
        unit || (unit = u);
        return;
      }
      keep.push(t);
      keepS.push(s[i]);
    });
    // מילים לחיפוש: בלי מילות שאלה. "רבנו"/"רבי" נשארים רק כחלק מביטוי קבוע
    let terms = [];
    for (let i = 0; i < keep.length; i++) {
      // "רבנו" נשאר רק בביטוי "לשון רבנו"
      if (STOP.has(keepS[i]) || keepS[i] === "של" && !(i > 0 && keepS[i - 1] === "לשנ" && /^רב/.test(keepS[i]))) continue;
      if (keep[i].length < 2) continue;
      terms.push(keep[i]);
    }
    let scope = null,
      lbl = "";
    if (book) ((scope = book.vols), (lbl = book.lbl));
    else if (unit && auth) {
      const x = unit.vols.filter((v) => auth.vols.includes(v));
      x.length ? ((scope = x), (lbl = unit.lbl)) : ((scope = auth.vols), (lbl = auth.lbl));
    } else if (auth) ((scope = auth.vols), (lbl = auth.lbl));
    else if (unit) ((scope = unit.vols), (lbl = unit.lbl));
    return { raw, qs, terms, part, scope: scope || BRES, lbl: lbl || "ספרי ברסלב", explicit: !!(book || auth || unit), unit, book, auth };
  }
  // בונה מונחים: ביטוי שלם אם קיים בטקסט, אחרת חלקים
  function groupTerms(words, idx) {
    const has = (ws) => {
      const re = termRe(ws);
      for (const i of idx) if (re.test(E.T(i))) return true;
      return false;
    };
    const out = [];
    words = words.map((w) => pickBase(w, idx));
    for (let i = 0; i < words.length; ) {
      let took = 0;
      for (let n = Math.min(5, words.length - i); n >= 2; n--)
        if (has(words.slice(i, i + n))) {
          out.push(words.slice(i, i + n));
          took = n;
          break;
        }
      if (took) i += took;
      else (out.push([words[i]]), i++);
    }
    return out;
  }
  function hitsIn(t, re) {
    re.lastIndex = 0;
    const p = [];
    let m;
    while ((m = re.exec(t)) && p.length < 400) (p.push(m.index + m[0].length - m[1].length), m[0].length || re.lastIndex++);
    return p;
  }
  // מילים נרדפות בלשון הספרים (רק לחיפוש מקורות, לא לספירה)
  const SYNX = {};
  [
    "חינוך|חנוך|לחנך|מחנך",
    "ילדים|ילדיו|בנים|בניו|בניהם|קטנים|תינוקות|נערים",
    "כעס|כועס|כעסן|רוגז|חמה",
    "פרנסה|ממון|מזונות|עשירות|משא ומתן",
    "עצבות|עצב|מרה שחורה|דאגה|דאגות",
    "שמחה|שמח|לשמח|משמח|שמחת",
    "תפילה|תפלה|להתפלל|מתפלל|תפלות",
    "התבודדות|מתבודד|להתבודד|בינו לבין קונו|שיחה בינו",
    "אשה|אשתו|נשים|שלום בית",
    "חולה|חולי|רפואה|לרפאות|חולאת",
    "בושה|בשת|בושת|ביישן",
    "ענווה|ענוה|ענו|ענותנות|שפלות",
    "גאווה|גאוה|גדלות|גסות",
    "אמונה|להאמין|מאמין|אמונת",
    "בטחון|לבטוח|בוטח",
    "שינה|לישן|ישן|שנה בלילה",
    "אכילה|לאכול|אוכל|מאכל|מאכלים",
    "נסיעה|לנסוע|נוסע|נסיעות|בדרך",
    "חתונה|חתן|כלה|נישואין|שידוך|שדוך",
    "פחד|מורא|יראה|מפחד|לפחד",
    "יסורים|ייסורים|צרות|צער",
  ].forEach((l) => {
    const a = l.split("|").map((t) => norm(t));
    a.forEach((t) => (SYNX[skl(t).join(" ")] = a));
  });
  // מושגים שבספרים נאמרים בלשון אחרת לגמרי
  const CONC = [
    { m: [["חינוך", "חנוך", "לחנך", "גידול", "לגדל"], ["ילדים", "הילדים", "בנים", "הבנים", "ילד", "נער", "נערים", "קטנים", "תינוקות"]], p: "גדול בנים|לגדל בניו|לגדל בנים|לגדל את בניו|לחנך|חנוך הבנים|חנוך בניו|חנוך נערים|חנוך הנער|מלמדי תינוקות|מלמד תינוקות|חנוך הילדים|חינוך הילדים|חינוך ילדים|חנוך ילדים", l: "חינוך ילדים" },
    { m: [["שלום בית", "שלום הבית"]], p: "שלום בית|שלום הבית|שלום ביתו|שלום בביתו|שלום בין איש לאשתו", l: "שלום בית" },
    { m: [["שמירת עיניים", "שמירת העיניים", "שמירת עינים", "שמירת העינים"]], p: "שמירת עינים|שמירת העינים|שמירת עיניו|לשמור עיניו|לשמר עיניו|ראית עינים|הסתכלות", l: "שמירת עיניים" },
    // "מה המעלה הגדולה ביותר" – בספרים זה כתוב "גדולה מן הכל", "גדול מכל", "למעלה מן הכל"
    {
      m: [["הגדולה ביותר", "הגדול ביותר", "הכי גדולה", "הכי גדול", "הכי חשובה", "הכי חשוב", "החשובה ביותר", "החשוב ביותר", "הגבוהה ביותר", "הגבוה ביותר", "הכי גבוהה", "הכי גבוה", "מעל הכל", "מן הכל", "גדולה מכל", "גדול מכל", "העליונה ביותר"]],
      p: "מעלה עליונה וגדולה מן הכל|גדולה מן הכל|גדול מן הכל|גבוה מן הכל|גבוהה מן הכל|למעלה מן הכל|גדול מכל|גדולה מכל|גדולה מכלם|גדול מכלם|עולה על כלם|גדולה מאד מכל",
      l: "גדולה מן הכל / גדול מכל / למעלה מן הכל",
      x: 1,
      drop: "גדולה גדול ביותר הכי חשובה חשוב גבוהה גבוה מעלה מעלת מעלות עליונה הכל מכל מן מעל דבר הדבר",
    },
  ].map((c) => Object.assign(c, { mS: c.m.map((g) => g.map((t) => skl(t).join(" "))), dropS: new Set(skl(c.drop || "")) }));
  function concRe(qs) {
    const c = CONC.find((c) => c.mS.every((g) => g.some((t) => hasAlt(qs, t))));
    if (!c) return null;
    const a = c.p.split("|").map((t) => norm(t));
    return { l: c.l, x: c.x, dropS: c.dropS, re: new RegExp("(?:^|[^א-ת])((?:" + a.map((t) => t.split(" ").map((w) => E.cc + w.split("").map(lt).join("")).join("[^א-ת]{1,3}")).join("|") + "))", "g") };
  }
  function synRe(g) {
    if (g.length !== 1) return null;
    const a = SYNX[sk(g[0])];
    if (!a) return null;
    return new RegExp("(?:^|[^א-ת])((?:" + a.map((t) => t.split(" ").map((w) => wordRe(w)).join("[^א-ת]{1,3}")).join("|") + "))", "g");
  }
  function search(P, syn, cn) {
    const idx = scopeIdx(P);
    // מושג "עוטף" (x): שאר המילים בשאלה נשארות כתנאי נוסף
    const rest = cn && cn.x ? P.terms.filter((t) => !cn.dropS.has(sk(t)) && !cn.dropS.has(sk(t.replace(/^[הו]/, "")))) : [];
    const G0 = rest.length ? groupTerms(rest, idx) : [];
    const G = cn ? G0.concat([[cn.l]]) : groupTerms(P.terms, idx);
    const R = cn ? G0.map((g) => termRe(g, 1)).concat([cn.re]) : G.map((g) => (syn && synRe(g)) || termRe(g, 1));
    const nT = G.length;
    const ch = new Map();
    let total = 0,
      items = 0;
    const need = nT;
    const scan = (need) => {
      ch.clear();
      ((total = 0), (items = 0));
      for (const i of idx) {
        const t = E.T(i);
        const H = [];
        let got = 0;
        for (const re of R) {
          const h = hitsIn(t, re);
          H.push(h);
          h.length && got++;
        }
        if (got < need) continue;
        items++;
        let cnt = 0;
        H.forEach((h) => (cnt += h.length));
        total += cnt;
        // מרחק: חלון קטן שמכיל את כל המונחים
        let span = 0;
        if (nT > 1) {
          span = 1e9;
          const f = H.filter((h) => h.length);
          for (const p of f[0].slice(0, 40)) {
            let lo = p,
              hi = p;
            for (const h of f.slice(1)) {
              let best = h[0];
              for (const q of h) Math.abs(q - p) < Math.abs(best - p) && (best = q);
              ((lo = Math.min(lo, best)), (hi = Math.max(hi, best)));
            }
            span = Math.min(span, hi - lo);
          }
        }
        const sc = got * 1000 - Math.min(span, 900) + Math.min(cnt, 30) * 3;
        const k = ck(i);
        const c = ch.get(k) || { k, best: -1e9, bi: i, cnt: 0, n: 0, len: 0, first: i };
        (sc > c.best && ((c.best = sc), (c.bi = i), (c.H = H)), (c.cnt += cnt), c.n++, ch.set(k, c));
      }
    };
    scan(need);
    let partial = false;
    if (!ch.size && nT >= 3) (scan(nT - 1), (partial = true));
    // ציון לפרק: ההתאמה הטובה + צפיפות + כותרת
    const tre = R.map((r) => new RegExp(r.source));
    const list = [...ch.values()].map((c) => {
      const title = (E.CH(c.bi) || "") + " " + (E.SEC(c.bi) || "");
      const tb = tre.some((r) => r.test(" " + title)) ? 2500 : 0;
      c.score = c.best + tb + Math.min(c.cnt, 60) * (nT > 1 ? 4 : 25) + (BW[E.V(c.bi)] || 0);
      c.tb = tb;
      return c;
    });
    list.sort((a, b) => b.score - a.score);
    return { G, R, list, total, items, partial, idx };
  }
  function snip(i, H) {
    const t = E.T(i).replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&");
    const pos = (H || []).filter((h) => h && h.length).map((h) => h[0]);
    const p = pos.length ? Math.min(...pos) : 0;
    const a = Math.max(0, p - 70),
      b = Math.min(t.length, p + 150);
    return { pre: a > 0, text: t.slice(a, b), post: b < t.length };
  }
  function where(i) {
    return [bookT(i), E.SEC(i), E.CH(i)].filter(Boolean).join(" · ");
  }
  function longest(P, short) {
    const idx = scopeIdx(P);
    const L = new Map();
    for (const i of idx) {
      const k = ck(i),
        c = L.get(k) || { k, i, len: 0, words: 0 };
      ((c.len += E.T(i).length), (c.words += E.T(i).split(" ").length), L.set(k, c));
    }
    const a = [...L.values()].filter((c) => c.words > 5).sort((x, y) => (short ? x.words - y.words : y.words - x.words));
    return a.slice(0, 5);
  }

  // ---- הכניסה הראשית ----
  function ask(q) {
    const P = parse(q);
    const f = fact(P.qs);
    if (f) return { kind: "fact", f, P };
    const isCountW = /(^| )כמה (פעמים|פעם)( |$)|(^| )(מופיע|מופיעה|מוזכר|מוזכרת|נזכר)( |$)/.test(P.raw) && /(^| )כמה( |$)/.test(P.raw);
    const isCountU = !isCountW && /(^| )כמה( |$)/.test(P.raw) && P.unit;
    const lg = /הכי (ארוכ|ארוך|קצר)|(ארוכה|ארוך|קצרה|קצר|הארוכה|הארוך|הקצרה|הקצר) ביותר/.exec(P.raw);
    if (lg) {
      const short = /קצר/.test(lg[0]);
      return { kind: "long", short, P, list: longest(P, short) };
    }
    // "כמה תורות יש בחלק ב׳ של ליקוטי מוהר״ן" – ספירת היחידות עצמן
    if (isCountU && !P.terms.length) {
      const idx = scopeIdx(P),
        C = new Map();
      for (const i of idx) C.has(ck(i)) || C.set(ck(i), i);
      const L = [...C.values()],
        byV = new Set(L.map((i) => E.V(i))).size > 1,
        G = new Map();
      L.forEach((i) => {
        const k = byV ? bookT(i) : E.SEC(i) || "";
        G.set(k, (G.get(k) || 0) + 1);
      });
      return { kind: "struct", P, n: L.length, first: L[0], last: L[L.length - 1], groups: G.size > 1 && G.size <= 8 ? [...G.entries()] : null };
    }
    if (!P.terms.length) return null;
    const tj = P.terms.map(sk).join(" ");
    if (P.raw.split(" ").length <= 2 && B.some((b) => b && b.title && skl(b.title).join(" ") === tj)) return null;
    const kd = isCountW ? "countW" : isCountU ? "countU" : "src";
    const cn = "src" === kd && concRe(P.qs);
    let S = search(P, 0, cn);
    // מעט תוצאות? מנסים שוב עם מילים נרדפות
    "src" === kd && !cn && S.list.length < 3 && ((S = search(P, 1)), (S.syn = 1));
    return { kind: kd, P, S };
  }
  return { ask, parse, where, snip, norm, bookT, ck, BRES };
}
if (typeof module !== "undefined") module.exports = botQAMake;
