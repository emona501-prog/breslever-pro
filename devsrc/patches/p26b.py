p='app.js'; s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:80]); s=s.replace(a,b)
rep('''                          ui: s.get("ui", null) || {},
                        };
                        !Object.keys(t.struct).length && f.struct && (t.struct = f.struct);''','''                          ui: s.get("ui", null) || {},
                          msgs: (s.get("live", {}) || {}).msgs || [],
                        };
                        !Object.keys(t.struct).length && f.struct && (t.struct = f.struct);''')
rep('''        Tf.on &&
          lr &&
          (r += n(
            "📊 כניסות לאפליקציה",''','''        Tf.on &&
          s.get("ghTok", "") &&
          (r += n(
            "📣 הודעות העורך",
            '<div style="font-size:13.5px;color:var(--ink2);line-height:1.65;margin-bottom:8px">הודעה קצרה שתקפוץ כהתראה אצל כל מי שאישר לקבל הודעות מהעורך. היא מגיעה למשתמש בפעם הבאה שהאפליקציה שלו נפתחת או חוזרת לחזית.</div><input id="edT" type="text" maxlength="60" placeholder="כותרת (למשל: שיר חדש בערוץ!)" style="width:100%;margin:4px 0"><textarea id="edB" rows="3" maxlength="400" placeholder="תוכן ההודעה" style="width:100%;margin:4px 0"></textarea><input id="edU" type="url" placeholder="קישור (לא חובה)" style="width:100%;margin:4px 0;direction:ltr"><div class="row2"><button class="btn pri" id="edSend">📣 שלח לכולם</button><button class="btn sm" id="edClr">🗑 מחיקת כל ההודעות</button></div><div id="edList" style="font-size:13px;color:var(--muted);margin-top:8px">' +
              ((s.get("live", {}) || {}).msgs || [])
                .slice(-5)
                .reverse()
                .map((t) => "• " + o(t.t || "") + " — " + o((t.b || "").slice(0, 60)))
                .join("<br>") +
              "</div>",
          )),
        (r += n(
          "📣 הודעות מהעורך",
          '<div class="sw"><span>לקבל מדי פעם הודעה קצרה מהעורך (חיזוק, ספר חדש, שיר חדש) – כהתראה</span><input type="checkbox" id="edMsgC" ' + (s.get("edMsg", !1) ? "checked" : "") + "></div>",
        )),
        Tf.on &&
          lr &&
          (r += n(
            "📊 כניסות לאפליקציה",''')
rep('''          const i = l("#livePub");
          i &&''','''          {
            const t = l("#edMsgC");
            t &&
              (t.onchange = () => {
                (s.set("edMsg", t.checked), s.set("edAsked", !0), st(t.checked ? "📣 תקבלו הודעות מהעורך" : "הודעות העורך כובו"));
              });
            const e = async (t) => {
                const e = await Gd("contents/" + Rd),
                  i = JSON.parse(Qd(e.content));
                ((i.msgs = t(i.msgs || [])), await Gd("contents/" + Rd, { method: "PUT", body: JSON.stringify({ message: "📣 הודעת העורך", content: Vd(JSON.stringify(i)), sha: e.sha }) }));
                const c = s.get("live", {}) || {};
                ((c.msgs = i.msgs), s.set("live", c));
              },
              i = l("#edSend"),
              c = l("#edClr");
            (i &&
              (i.onclick = async () => {
                const t = (l("#edT").value || "").trim(),
                  c = (l("#edB").value || "").trim(),
                  a = (l("#edU").value || "").trim();
                if (!t && !c) return void st("כתבו כותרת או תוכן");
                if (confirm("לשלוח את ההודעה לכל מי שאישר הודעות מהעורך?")) {
                  ((i.disabled = !0), (i.textContent = "⏳ שולח…"));
                  try {
                    const i = Date.now();
                    (await e((e) => e.concat([{ id: i, t: t || "הודעה מהעורך", b: c, u: a || void 0, until: i + 6048e5 }]).slice(-12)),
                      s.set("edSeen", s.get("edSeen", []).concat([String(i)])),
                      st("✅ ההודעה נשלחה", 3e3),
                      Ft.settings());
                  } catch (t) {
                    ((i.disabled = !1), (i.textContent = "📣 שלח לכולם"), st("❌ השליחה נכשלה: " + (t.message || t), 6e3));
                  }
                }
              }),
              c &&
                (c.onclick = async () => {
                  if (confirm("למחוק את כל ההודעות ששלחת?"))
                    try {
                      (await e(() => []), st("נמחק"), Ft.settings());
                    } catch (t) {
                      st("❌ " + (t.message || t), 5e3);
                    }
                }));
          }
          const i = l("#livePub");
          i &&''')
open(p,'w',encoding='utf-8').write(s); print('patched')
