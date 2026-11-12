  // ⏰ העוזר קובע תזכורת בעצמו: מפענח שעה/יום מהבקשה ("מחר ב-8", "בעוד שעה", "כל יום ב-21:30", "בחצות")
  function botRemTime(q, lbl) {
    const n2 = (t) => String(t).padStart(2, "0"),
      now = new Date();
    let daily = /(^| )(כל יום|כל בוקר|כל ערב|כל לילה|יומי|יומית|קבוע|כל הימים)( |$)/.test(q),
      day = /(^| )(מחר|למחר)( |$)/.test(q) ? 1 : 0,
      h = null,
      mi = 0;
    const R = /בעוד (\d+|חצי|רבע|שעה|שעתיים|דקה) ?(דקות|דקה|שעות|שעה)?/.exec(q);
    if (R && !daily) {
      const t = "חצי" === R[1] ? 30 : "רבע" === R[1] ? 15 : "שעה" === R[1] ? 60 : "שעתיים" === R[1] ? 120 : "דקה" === R[1] ? 1 : +R[1] * (/שע/.test(R[2] || "") ? 60 : 1);
      return { at: Date.now() + 6e4 * t };
    }
    const T = /(?:^| )(?:ב|בשעה|ב שעה|לשעה|עד)\s?(\d{1,2})(?:[:.](\d{2}))?(?= |$)/.exec(q) || /(?:^| )(\d{1,2})[:.](\d{2})(?= |$)/.exec(q);
    T && ((h = +T[1]), (mi = +(T[2] || 0)));
    // זמני היום
    let zk = null;
    /חצות/.test(q) && (zk = "chatzotLayla");
    /קריאת שמע|קש( |$)/.test(q) && !/מיטה|המיטה/.test(q) && (zk = "shmaGra");
    /שקיעה/.test(q) && (zk = "set");
    /הדלקת נרות/.test(q) && (zk = "candle");
    if (null === h && zk)
      try {
        let t = day;
        const e = (t) => {
          const e = ms(t);
          return "candle" === zk ? e.v.set - yn(e.L) * ls.MIN : e.v[zk];
        };
        let i = e(t);
        "shmaGra" === zk && (i -= 30 * 6e4);
        i < Date.now() + 6e4 && !daily && ((t += 1), (i = e(t) - ("shmaGra" === zk ? 30 * 6e4 : 0)));
        if (!daily) return { at: i, z: zk };
        const c = new Date(i);
        return { daily: 1, time: n2(c.getHours()) + ":" + n2(c.getMinutes()), z: zk };
      } catch (t) {}
    if (null === h) {
      /(^| )(בבוקר|בוקר)( |$)/.test(q) ? (h = 8) : /(^| )(בצהריים|צהריים)( |$)/.test(q) ? (h = 13) : /(^| )(בערב|הערב|ערב)( |$)/.test(q) ? (h = 20) : /(^| )(בלילה|הלילה)( |$)/.test(q) && (h = 22);
    } else /(בערב|הערב|בלילה|אחה צ|אחר הצהריים)/.test(q) && h < 12 && (h += 12);
    if (null === h) return null;
    if (daily) return { daily: 1, time: n2(h) + ":" + n2(mi) };
    const d = new Date(now);
    return (d.setDate(d.getDate() + day), d.setHours(h, mi, 0, 0), d <= now && !day && (d.getHours() < 12 && !/בבוקר/.test(q) && h + 12 < 24 && new Date(d.getTime() + 432e5) > now ? d.setTime(d.getTime() + 432e5) : d.setDate(d.getDate() + 1)), { at: d.getTime() });
  }
  function botRemMake(lbl, nav, w) {
    const e = { id: Date.now().toString(36), lbl: lbl, nav: nav, note: "", type: w.daily ? "days" : "once" };
    w.daily ? ((e.time = w.time), (e.days = [0, 1, 2, 3, 4, 5, 6])) : (e.at = w.at);
    const i = Wl();
    (i.push(e), Yl(i));
    try {
      "Notification" in window && "default" === Notification.permission && !NAT.on && Notification.requestPermission();
    } catch (t) {}
    return e;
  }
  function botRemDesc(w) {
    if (w.daily) return "כל יום בשעה " + w.time;
    const t = new Date(w.at),
      e = new Date(),
      i = String(t.getHours()).padStart(2, "0") + ":" + String(t.getMinutes()).padStart(2, "0"),
      c = t.toDateString() === e.toDateString() ? "היום" : new Date(e.getTime() + 864e5).toDateString() === t.toDateString() ? "מחר" : t.getDate() + "." + (t.getMonth() + 1);
    return c + " בשעה " + i;
  }
