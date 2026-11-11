p='app.js'; s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:80]); s=s.replace(a,b)
BOT=r'''
  // 🤖 העוזר של ברסלב PRO – בלי בינה מלאכותית: מאגר מתוך ההסברים שבאפליקציה + חיפוש לפי מילים
  const BOT_STOP = new Set("יש לכם לנו האם איך אפשר את של על מה זה זו אני רוצה רציתי לי אתם אותו אותה פונקציה פונקציות אפשרות אפשרויות באפליקציה אפליקציה האפליקציה עם בלי כל גם רק או אם כן לא כמו היא הוא הם הן שלי שלכם איפה איזה איזו מתי למה כדי צריך יכול יכולה ניתן מאפשר מאפשרת שם פה כאן עוד בבקשה תודה דבר משהו לעשות עושים".split(" "));
  const BOT_SYN = {
    שיתוף: "שתף שיתוף לשתף ווצאפ וואטסאפ whatsapp שליחה לשלוח",
    מעוצב: "מעוצב תמונה תמונות עיצוב עורך גלויה סטטוס",
    תזכורת: "תזכורת תזכורות התראה התראות שעון מעורר להזכיר",
    חיפוש: "חיפוש לחפש חפש מצוא למצוא",
    הקראה: "הקראה הקראת קריאה בקול להקריא קול שמע לשמוע דיבור",
    סימניה: "סימניה סימניות לסמן סימון שמירה לשמור",
    הגדרות: "הגדרות הגדרה להגדיר לשנות שינוי",
    גופן: "גופן גודל אותיות פונט טקסט גדול קטן",
    לילה: "לילה חושך כהה מצב תצוגה רקע",
    ווידגט: "ווידגט וידגט ווידג'ט וידג'ט מסך הבית",
    זמנים: "זמנים זמני היום שקיעה זריחה קריאת שמע תפילה שבת",
    מצפן: "מצפן כיוון התפילה ירושלים מזרח",
    הלכה: "הלכה הלכות שולחן ערוך שלחן פוסקים",
    חדר: "חדר פרטי החדר",
    גיבוי: "גיבוי שחזור לגבות להעביר טלפון חדש",
    הדפסה: "הדפסה להדפיס חוברת קונטרס pdf",
    תהלים: "תהלים תהילים פרקי",
    תנך: "תנך חומש פרשה פרשת עליה עליות שניים מקרא תרגום רשי מקראות נביאים כתובים",
    זוהר: "זוהר זהר ארמית תיקוני",
    רעיון: "רעיון הצעה לשפר שיפור חסר",
  };
  function botNorm(t) {
    return m(String(t || ""))
      .replace(/<[^>]+>/g, " ")
      .replace(/['"׳״`]/g, "")
      .replace(/[^א-תa-z0-9 ]/gi, " ")
      .replace(/ך/g, "כ")
      .replace(/ם/g, "מ")
      .replace(/ן/g, "נ")
      .replace(/ף/g, "פ")
      .replace(/ץ/g, "צ")
      .toLowerCase()
      .replace(/\s+/g, " ")
      .trim();
  }
  function botTok(t) {
    const e = [];
    return (
      botNorm(t)
        .split(" ")
        .forEach((t) => {
          if (!t || BOT_STOP.has(t)) return;
          e.push(t);
          t.length > 3 && /^[הובלשמכ]/.test(t) && !BOT_STOP.has(t.slice(1)) && e.push(t.slice(1));
          t.length > 4 && /^(וה|שה|וב|ול|מה|כש|וכ|לה|בה)/.test(t) && e.push(t.slice(2));
        }),
      [...new Set(e)]
    );
  }
  let botKb = null;
  function botBuild() {
    if (botKb) return botKb;
    const t = [],
      e = (e, i, c, l, a) => t.push({ ic: e, t: i, txt: botNorm(i + " " + (c || "")) + " " + botNorm(l || ""), raw: c, go: a, kt: botNorm(i) + " " + botNorm(l || "") });
    // פעולות עם "קח אותי לשם"
    [
      ["⚙️", "הגדרות", "כל ההגדרות של האפליקציה: גופן, תצוגה, צבעים, תזכורות, ווידג'ט, גיבוי ועוד.", "הגדרות", () => It("settings")],
      ["⚖️", "הלכה יומית לפי סדר השולחן ערוך", "כל יום מקבלים הלכות לפי הסדר – אורח חיים, יורה דעה, אבן העזר וחושן משפט – עם התראה ובווידג'ט. בוחרים כמה סעיפים ובאיזו שעה.", "הלכה יומית שולחן ערוך סעיפים כל יום", () => halSheet()],
      ["✍️", "תזכורת אישית", "תזכורת עם טקסט שאתם כותבים, בשעה שתבחרו – קופצת כהתראה ומופיעה גם בווידג'ט.", "תזכורת אישית טקסט חופשי", () => selfRem()],
      ["🔎", "חיפוש מהיר של ספר או כותרת", "כותבים שם של ספר, חלק או כותרת (למשל: הלל) ומגיעים ישר למקום.", "חיפוש ספר כותרת הלל", () => sfOpen()],
      ["🔍", "חיפוש בתוך הספרים", "חיפוש מילים בתוך כל הטקסטים של הספרים – בסרגל התחתון.", "חיפוש מילה טקסט תוכן", () => It("search")],
      ["🗂️", "מפתחות", "מפתחות נושאים לכל הספרים.", "מפתחות נושאים", () => It("index")],
      ["🔖", "האזור שלי – סימניות, הערות והדגשות", "כל מה שסימנתם, כתבתם והדגשתם במקום אחד.", "סימניות הערות הדגשות האזור שלי", () => It("mine")],
      ["📜", "התיקון הכללי", "התיקון הכללי עם סימון 'אמרתי' והקראה.", "תיקון הכללי", () => It("tikkun")],
      ["🕯️", "לוח הילולות וזמני היום", "לוח שנה עברי, הילולות צדיקים, זמני היום והתראות לפני סוף זמן.", "לוח הילולות זמני היום תאריך עברי", () => It("calendar")],
      ["🧭", "מצפן – כיוון התפילה", "מצפן שמראה את הכיוון לירושלים ולהר הבית.", "מצפן כיוון התפילה", () => It("dir")],
      ["🎲", "פתיחה אקראית", "דיבור אקראי מהספרים. לחיצה ארוכה על שם ספר מוסיפה אותו לרשימת הספרים שמהם מגרילים.", "פתיחה אקראית הגרלה קוביה דיבור", () => It("random")],
      ["💎", "דיבורים נבחרים", "לקט דיבורים נבחרים לפי נושאים.", "דיבורים נבחרים", () => It("pearls")],
      ["📅", "סדר היום שלי", "סדר לימוד יומי אישי.", "סדר היום", () => It("day")],
      ["📖", "תוכנית לימוד", "תוכנית לסיום ספר עד תאריך שתבחרו.", "תוכנית לימוד סיום", () => It("plan")],
      ["🍞", "ברכת המזון", "ברכת המזון בנוסחים השונים.", "ברכת המזון", () => It("birkat")],
      ["📱", "הגדרות הווידג'ט", "בוחרים מה יופיע בווידג'ט, דיבור מתחלף, לוגו הערוץ ועוד.", "ווידגט מסך הבית", () => botSettings("wdgCard")],
      ["📣", "הודעות מהעורך", "מדי פעם הודעה קצרה מעורך האפליקציה – מפעילים בהגדרות.", "הודעות עורך", () => botSettings("edMsgC")],
    ].forEach((t) => e(t[0], t[1], t[2], t[3], t[4]));
    // ההסברים שבמדריך
    Er.forEach((t) => e(t[0], t[1], g(t[2]), "", null));
    // מה חדש
    (rr.items || []).forEach((t) => e(t[1], t[2], g(t[3]), "", null));
    return (botKb = t);
  }
  function botSettings(t) {
    (It("settings"),
      setTimeout(() => {
        const e = document.getElementById(t);
        e && e.scrollIntoView({ behavior: "smooth", block: "center" });
      }, 450));
  }
  function botFind(t) {
    let e = botTok(t);
    if (!e.length) return { q: e, r: [] };
    const i = [];
    e.forEach((t) => {
      for (const e in BOT_SYN) {
        const c = BOT_SYN[e].split(" ");
        c.some((e) => e === t || (t.length > 3 && e.startsWith(t))) && c.forEach((t) => i.push(t));
      }
    });
    const c = botBuild()
      .map((t) => {
        let c = 0,
          l = 0;
        const a = " " + t.txt + " ",
          o = " " + t.kt + " ";
        (e.forEach((t) => {
          const e = o.includes(" " + t) ? 4 : a.includes(" " + t + " ") ? 2 : t.length > 3 && a.includes(" " + t) ? 1.5 : 0;
          (e && l++, (c += e));
        }),
          i.forEach((t) => {
            o.includes(" " + t) ? (c += 1) : a.includes(" " + t + " ") && (c += 0.4);
          }),
          t.go && (c += 0.3));
        return { e: t, sc: c, hit: l };
      })
      .filter((t) => t.sc >= 2.5 && t.hit >= Math.min(2, Math.ceil(e.length / 2)) - (e.length > 2 ? 0 : 1))
      .sort((t, e) => e.sc - t.sc);
    return { q: e, r: c.slice(0, 3) };
  }
  // 📥 תיבת רעיונות: נשלח לגיליון גוגל של העורך (Apps Script). אם עוד אין כתובת – נשמר בתור ונשלח אחר כך.
  function inboxUrl() {
    return ((s.get("live", {}) || {}).inbox || "").trim();
  }
  function ideaSend(t) {
    const e = s.get("ideaQ", []);
    (e.push({ t: String(t).slice(0, 1500), ts: Date.now(), v: pr }), s.set("ideaQ", e.slice(-30)), ideaFlush());
  }
  function ideaFlush() {
    const t = inboxUrl(),
      e = s.get("ideaQ", []);
    if (!t || !e.length || !navigator.onLine) return;
    s.set("ideaQ", []);
    e.forEach((e) => {
      fetch(t, { method: "POST", mode: "no-cors", headers: { "Content-Type": "text/plain;charset=utf-8" }, body: JSON.stringify(e) }).catch(() => {
        const t = s.get("ideaQ", []);
        (t.push(e), s.set("ideaQ", t));
      });
    });
  }
  setTimeout(ideaFlush, 12e3);
  function botOpen(t) {
    const e = Ut(
      '<h3>🤖 העוזר של ברסלב PRO</h3><div class="sh-sub">שאלו על כל דבר באפליקציה – איפה נמצאת הגדרה, איך עושים משהו, האם יש פונקציה מסוימת.</div><div class="bot-row"><input type="search" id="botQ" placeholder="למשל: יש שיתוף מעוצב? איך מגדילים אותיות?" enterkeyhint="search"><button class="btn pri" id="botGo">שאל</button></div><div id="botR" class="bot-res"></div>',
    );
    const i = l("#botQ", e),
      c = l("#botR", e),
      n = () => {
        const t = (i.value || "").trim();
        if (t.length < 2) return void (c.innerHTML = '<div class="bot-tip">💡 אפשר לשאול למשל: "איך מקבלים הלכה יומית?", "יש מצפן?", "איך משתפים כתמונה?"</div>');
        const e = botFind(t);
        (e.r.length
          ? ((c.innerHTML =
              e.r
                .map(
                  (t, e) =>
                    '<div class="bot-a"><b>' +
                    t.e.ic +
                    " " +
                    o(t.e.t) +
                    "</b><p>" +
                    o(String(t.e.raw || "").slice(0, 420)) +
                    (String(t.e.raw || "").length > 420 ? "…" : "") +
                    "</p>" +
                    (t.e.go ? '<button class="btn pri sm" data-bg="' + e + '">👈 קח אותי לשם</button>' : "") +
                    "</div>",
                )
                .join("") + '<div class="bot-more">לא מה שחיפשתם? <button class="btn sm" id="botIdea">💡 להציע את זה כרעיון לעורך</button></div>'),
            a("[data-bg]", c).forEach(
              (t) =>
                (t.onclick = () => {
                  const i = e.r[+t.dataset.bg].e.go;
                  (Wt(), setTimeout(i, 250));
                }),
            ))
          : (c.innerHTML =
              '<div class="bot-a bot-new"><b>💡 זה יכול להיות רעיון מצוין!</b><p>לא מצאתי באפליקציה פונקציה כזו. רוצים לשלוח את הרעיון לעורך? הוא קורא כל הצעה.</p><textarea id="botTxt" rows="3">' +
              o(t) +
              '</textarea><button class="btn pri" id="botSend" style="width:100%;margin-top:8px">📨 שליחת הרעיון</button></div>'),
          (function () {
            const t = l("#botIdea", c);
            t &&
              (t.onclick = () => {
                ((c.innerHTML =
                  '<div class="bot-a bot-new"><b>💡 הצעה לעורך</b><textarea id="botTxt" rows="3">' + o(i.value) + '</textarea><button class="btn pri" id="botSend" style="width:100%;margin-top:8px">📨 שליחת הרעיון</button></div>'),
                  e());
              });
            const e = () => {
              const t = l("#botSend", c);
              t &&
                (t.onclick = () => {
                  const t = (l("#botTxt", c).value || "").trim();
                  t &&
                    (ideaSend(t),
                    (c.innerHTML = '<div class="bot-a"><b>🙏 תודה רבה!</b><p>הרעיון נשלח לעורך' + (inboxUrl() ? "" : " (יישלח ברגע שיהיה חיבור)") + ". כל הצעה עוזרת לשפר את האפליקציה.</p></div>"));
                });
            };
            e();
          })());
      };
    ((l("#botGo", e).onclick = n), (i.onkeydown = (t) => "Enter" === t.key && n()), t && ((i.value = t), n()), setTimeout(() => { try { i.focus(); } catch (t) {} }, 250), n());
  }
  window.__botOpen = botOpen;
  document.addEventListener(
    "click",
    (t) => {
      const e = t.target.closest && t.target.closest('[data-f="bot"],#toolBot,#helpBot');
      e && (t.preventDefault(), t.stopPropagation(), Wt && document.querySelector("#sheet.open,.sheet.open") && Wt(), setTimeout(() => botOpen(), 120), "fi" === e.className.split(" ")[0] && document.body.classList.remove("fab-open"));
    },
    !0,
  );
  // 📥 תיבת הרעיונות – רק בעיני העורך
  const INBOX_GS = `// ברסלב PRO – תיבת רעיונות. מדביקים בגיליון גוגל ← הרחבות ← Apps Script
const KEY = 'החליפו-לסיסמה-שלכם';
function sheet_(){ const ss = SpreadsheetApp.getActive(); return ss.getSheetByName('רעיונות') || ss.insertSheet('רעיונות'); }
function doPost(e){
  try{
    const d = JSON.parse(e.postData.contents || '{}');
    const t = String(d.t || '').slice(0, 1500).trim();
    if(!t) return ContentService.createTextOutput('no');
    const sh = sheet_();
    if(sh.getLastRow() === 0) sh.appendRow(['זמן','רעיון','גרסה','סטטוס']);
    sh.appendRow([new Date(), t, String(d.v || ''), 'חדש']);
    MailApp.sendEmail(Session.getEffectiveUser().getEmail(), '💡 רעיון חדש מברסלב PRO', t);
    return ContentService.createTextOutput('ok');
  }catch(err){ return ContentService.createTextOutput('err'); }
}
function doGet(e){
  const p = e.parameter || {};
  if(p.key !== KEY) return ContentService.createTextOutput(JSON.stringify({err:'key'})).setMimeType(ContentService.MimeType.JSON);
  const sh = sheet_();
  if(p.a === 'done' && p.r) sh.getRange(Number(p.r), 4).setValue('טופל');
  if(p.a === 'del' && p.r) sh.deleteRow(Number(p.r));
  const v = sh.getLastRow() > 1 ? sh.getRange(2, 1, sh.getLastRow() - 1, 4).getValues() : [];
  const rows = v.map((x, i) => ({ r: i + 2, ts: new Date(x[0]).getTime(), t: x[1], v: x[2], st: x[3] })).reverse();
  return ContentService.createTextOutput(JSON.stringify({ rows })).setMimeType(ContentService.MimeType.JSON);
}`;
  function inboxHtml() {
    const t = inboxUrl();
    return (
      '<div style="font-size:13.5px;color:var(--ink2);line-height:1.65">רעיונות שמשתמשים שולחים מהעוזר 🤖 נשמרים בגיליון גוגל שלך ומגיעים אליך גם במייל. רק מי שיש לו הסיסמה רואה אותם – והיא שמורה רק במכשיר הזה.</div>' +
      (t
        ? '<div class="row2" style="margin-top:8px"><button class="btn pri sm" id="ibLoad">📥 פתיחת התיבה</button><button class="btn sm" id="ibKeyB">🔑 סיסמה</button></div><div id="ibList" style="margin-top:8px"></div>'
        : '<details style="margin-top:8px"><summary><b>הגדרה חד־פעמית (כ־5 דקות)</b></summary><ol style="line-height:1.8;font-size:13.5px;padding-inline-start:18px"><li>פתחו גיליון חדש ב־Google Sheets.</li><li>תפריט <b>הרחבות ← Apps Script</b>.</li><li>מחקו את מה שיש שם והדביקו את הקוד (כפתור "העתקת הקוד" למטה).</li><li>בשורה הראשונה החליפו את הסיסמה לסיסמה שלכם.</li><li><b>פריסה ← פריסה חדשה ← אפליקציית אינטרנט</b>. "הפעלה בתור": אני. "למי יש גישה": כל אחד. אשרו את ההרשאות.</li><li>העתיקו את כתובת אפליקציית האינטרנט והדביקו כאן למטה, יחד עם הסיסמה.</li></ol><button class="btn sm" id="ibCopy">📋 העתקת הקוד</button></details>') +
      '<input id="ibUrl" type="url" placeholder="כתובת אפליקציית האינטרנט (https://script.google.com/...)" value="' +
      o(t) +
      '" style="width:100%;margin:8px 0 4px;direction:ltr"><input id="ibKey" type="password" placeholder="הסיסמה מהשורה הראשונה בקוד" value="' +
      o(s.get("inboxKey", "")) +
      '" style="width:100%;margin:4px 0;direction:ltr"><button class="btn sm" id="ibSave">💾 שמירה ופרסום הכתובת לכל המשתמשים</button>'
    );
  }
  function inboxBind(t, e) {
    const i = (e) => l(e, t),
      c = i("#ibCopy");
    c && (c.onclick = () => nt(INBOX_GS));
    const a = i("#ibSave");
    a &&
      (a.onclick = async () => {
        const t = (i("#ibUrl").value || "").trim(),
          c = (i("#ibKey").value || "").trim();
        if (t && !/^https:\/\/script\.google(usercontent)?\.com\//.test(t)) return void st("הכתובת צריכה להתחיל ב־https://script.google.com/");
        (c && s.set("inboxKey", c), (a.disabled = !0), (a.textContent = "⏳ שומר…"));
        try {
          (await e((e) => ((e.inbox = t), e)), st("✅ נשמר. מעכשיו הרעיונות יגיעו אליך", 3e3), Ft.settings());
        } catch (t) {
          ((a.disabled = !1), (a.textContent = "💾 שמירה ופרסום הכתובת לכל המשתמשים"), st("❌ " + (t.message || t), 5e3));
        }
      });
    const n = i("#ibKeyB");
    n &&
      (n.onclick = () => {
        const t = prompt("הסיסמה של תיבת הרעיונות:", s.get("inboxKey", ""));
        null != t && s.set("inboxKey", t.trim());
      });
    const r = i("#ibLoad"),
      f = async (t, e) => {
        const c = i("#ibList");
        c.innerHTML = '<div class="sh-sub">טוען…</div>';
        try {
          const i = inboxUrl() + "?key=" + encodeURIComponent(s.get("inboxKey", "")) + (t ? "&a=" + t + "&r=" + e : "") + "&_=" + Date.now(),
            l = await (await fetch(i)).json();
          if (l.err) return void (c.innerHTML = '<div class="sh-sub">❌ הסיסמה לא נכונה. לחצו "🔑 סיסמה".</div>');
          (s.set("ibSeen", Date.now()),
            (c.innerHTML = l.rows.length
              ? l.rows
                  .map(
                    (t) =>
                      '<div class="ib-it' + ("טופל" === t.st ? " done" : "") + '"><small>' + new Date(t.ts).toLocaleString("he-IL") + (t.v ? " · גרסה " + o(t.v) : "") + " · " + o(t.st || "") + "</small><p>" + o(t.t) + '</p><div class="row2"><button class="btn sm" data-ibd="' + t.r + '">✔️ טופל</button><button class="btn sm" data-ibx="' + t.r + '">🗑 מחיקה</button></div></div>',
                  )
                  .join("")
              : '<div class="sh-sub">התיבה ריקה.</div>'),
            a("[data-ibd]", c).forEach((t) => (t.onclick = () => f("done", t.dataset.ibd))),
            a("[data-ibx]", c).forEach((t) => (t.onclick = () => confirm("למחוק את הרעיון?") && f("del", t.dataset.ibx))));
        } catch (t) {
          c.innerHTML = '<div class="sh-sub">❌ לא הצלחתי להתחבר לתיבה. בדקו את החיבור ואת הכתובת.</div>';
        }
      };
    r && (r.onclick = () => f());
  }
  // לעורך: בדיקה שקטה אם יש רעיונות חדשים
  setTimeout(async () => {
    try {
      if (!s.get("ghTok", "") || !s.get("inboxKey", "") || !inboxUrl()) return;
      const t = await (await fetch(inboxUrl() + "?key=" + encodeURIComponent(s.get("inboxKey", "")) + "&_=" + Date.now())).json(),
        e = (t.rows || []).filter((t) => "חדש" === t.st && t.ts > (s.get("ibSeen", 0) || 0)).length;
      e && nudge("ib" + Date.now(), "📥 <b>" + e + " רעיונות חדשים</b> בתיבת הרעיונות", [["לפתיחה", () => botSettings("ibCard")]]);
    } catch (t) {}
  }, 15e3);
'''
rep('''  function goZman(t) {''',BOT+'''  function goZman(t) {''')
# כרטיס בהגדרות (עורך) – באותו מקום של הודעות העורך
rep('''            "📣 הודעות העורך",''','''            "📣 הודעות העורך",''')
rep('''        (r += n(
          "📣 הודעות מהעורך",''','''        Tf.on && s.get("ghTok", "") && (r += '<div id="ibCard">' + n("📥 תיבת הרעיונות (רק אצלך)", inboxHtml()) + "</div>"),
        (r += n(
          "📣 הודעות מהעורך",''')
rep('''            const g = l("#nudgeC");
            g &&''','''            try {
              const t = l("#ibCard");
              t &&
                inboxBind(t, async (t) => {
                  const e = await Gd("contents/" + Rd),
                    i = JSON.parse(Qd(e.content));
                  (t(i), await Gd("contents/" + Rd, { method: "PUT", body: JSON.stringify({ message: "📥 כתובת תיבת הרעיונות", content: Vd(JSON.stringify(i)), sha: e.sha }) }));
                  const c = s.get("live", {}) || {};
                  ((c.inbox = i.inbox), s.set("live", c));
                });
            } catch (t) {}
            const g = l("#nudgeC");
            g &&''')
# שמירת כתובת התיבה מתוך live גם כשהגרסה לא השתנתה
rep('''      if (e && Array.isArray(e.msgs) && e.msgs.length) {''','''      if (e && "string" == typeof e.inbox && e.inbox !== ((s.get("live", {}) || {}).inbox || "")) {
        const t = s.get("live", {}) || {};
        ((t.inbox = e.inbox), s.set("live", t), setTimeout(ideaFlush, 1500));
      }
      if (e && Array.isArray(e.msgs) && e.msgs.length) {''')
# שמירה על inbox כשמפרסמים תיקונים
rep('''                          msgs: (s.get("live", {}) || {}).msgs || [],''','''                          msgs: (s.get("live", {}) || {}).msgs || [],
                          inbox: (s.get("live", {}) || {}).inbox || void 0,''')
# לא לייצא סיסמת תיבה בגיבוי
rep('''      e !== SPFX + "ghTok" && e !== SPFX + "live" && (t[e] = localStorage.getItem(e));''','''      e !== SPFX + "ghTok" && e !== SPFX + "live" && e !== SPFX + "inboxKey" && (t[e] = localStorage.getItem(e));''')
# כפתור במדריך
rep('''        '<h3>❓ מדריך לברסלב PRO</h3><div class="sh-sub">🎬 בקרוב: סרטון הסבר מפורט על כל האפליקציה.</div>''','''        '<h3>❓ מדריך לברסלב PRO</h3><button class="btn pri" id="helpBot" style="width:100%;margin:4px 0 8px">🤖 שאלו את העוזר – הוא מכיר כל פינה באפליקציה</button><div class="sh-sub">🎬 בקרוב: סרטון הסבר מפורט על כל האפליקציה.</div>''')
open(p,'w',encoding='utf-8').write(s); print('patched')
p='shell.html'; s=open(p,encoding='utf-8').read()
def rp(a,b):
    global s
    assert s.count(a)==1,a; s=s.replace(a,b)
rp('''    <button class="fi" data-f="fhelp">❔<span>מה כל כפתור עושה?</span></button>''','''    <button class="fi" data-f="bot">🤖<span>שאלו את העוזר</span></button>
    <button class="fi" data-f="fhelp">❔<span>מה כל כפתור עושה?</span></button>''')
rp('''    <button class="tool" id="toolNotes"><span class="ic">📝</span>הערות</button>''','''    <button class="tool" id="toolNotes"><span class="ic">📝</span>הערות</button>
    <button class="tool" id="toolBot"><span class="ic">🤖</span>שאלו את העוזר</button>''')
s=s.replace(".rnd-hint{",'''.bot-row{display:flex;gap:6px}.bot-row input{flex:1;min-width:0;padding:11px 12px;border:1px solid var(--line);border-radius:12px;font:inherit;background:var(--card);color:var(--ink)}
.bot-res{margin-top:10px;max-height:58vh;overflow:auto}
.bot-a{padding:12px 14px;border-radius:14px;background:var(--card);border:1px solid var(--line);margin-bottom:8px}
.bot-a b{font:800 15px var(--ui-font);color:var(--ink)}.bot-a p{margin:6px 0 8px;font-size:14px;line-height:1.65;color:var(--ink2)}
.bot-a textarea{width:100%;border:1px solid var(--line);border-radius:10px;padding:8px;font:inherit;background:var(--bg);color:var(--ink)}
.bot-new{border-color:var(--accent,#b08a3a);background:var(--soft,rgba(176,138,58,.08))}
.bot-more{text-align:center;font-size:13px;color:var(--muted);margin-top:6px}.bot-tip{font-size:13.5px;color:var(--muted);padding:4px}
.ib-it{padding:10px 12px;border:1px solid var(--line);border-radius:12px;margin-bottom:6px}.ib-it.done{opacity:.55}.ib-it p{margin:4px 0;white-space:pre-wrap}.ib-it small{color:var(--muted)}
.rnd-hint{''',1)
open(p,'w',encoding='utf-8').write(s)
