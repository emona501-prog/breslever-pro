package com.chaiproductions.breslovpro;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Bundle;
import android.os.SystemClock;
import android.view.View;
import android.widget.RemoteViews;

import org.json.JSONArray;
import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

/** ווידג'ט "ברסלב PRO – היום": תאריך עברי, פרשה, הזמן הקרוב עם ספירה לאחור, הילולות ותזכורות מתחלפות, מצפן וכפתורים מהירים.
 *  שלושה גדלים – קטן, בינוני וגדול – לפי הגודל שהמשתמש קובע במסך הבית. */
public class BpWidget extends AppWidgetProvider {
    public static final String PREFS = "bp_widget";
    public static final String TICK = "com.chaiproductions.breslovpro.WIDGET_TICK";
    public static final String DICE = "com.chaiproductions.breslovpro.WIDGET_DICE";

    @Override
    public void onUpdate(Context ctx, AppWidgetManager mgr, int[] ids) {
        for (int id : ids) updateOne(ctx, mgr, id);
        scheduleNext(ctx);
    }

    @Override
    public void onAppWidgetOptionsChanged(Context ctx, AppWidgetManager mgr, int id, Bundle opts) {
        updateOne(ctx, mgr, id);
    }

    @Override
    public void onReceive(Context ctx, Intent intent) {
        super.onReceive(ctx, intent);
        String a = intent.getAction();
        if (DICE.equals(a)) {
            // 🎲 דיבור חדש בווידג'ט עצמו
            try {
                SharedPreferences sp = ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE);
                sp.edit().putInt("qoff", sp.getInt("qoff", 0) + 1 + (int) (Math.random() * 17)).apply();
            } catch (Exception e) { }
            updateAll(ctx);
        }
        if (TICK.equals(a) || Intent.ACTION_TIME_CHANGED.equals(a) || Intent.ACTION_TIMEZONE_CHANGED.equals(a)) updateAll(ctx);
    }

    public static void updateAll(Context ctx) {
        AppWidgetManager mgr = AppWidgetManager.getInstance(ctx);
        int[] ids = mgr.getAppWidgetIds(new ComponentName(ctx, BpWidget.class));
        for (int id : ids) updateOne(ctx, mgr, id);
        if (ids.length > 0) scheduleNext(ctx);
    }

    private static PendingIntent act(Context ctx, String a, int req) {
        Intent i = new Intent(ctx, MainActivity.class);
        i.setAction("bp.w." + a);
        i.putExtra("wact", a);
        i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_SINGLE_TOP);
        return PendingIntent.getActivity(ctx, req, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
    }

    private static PendingIntent web(Context ctx, String url, int req) {
        Intent i = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
        i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        return PendingIntent.getActivity(ctx, req, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
    }

    private static JSONObject data(Context ctx) {
        try {
            String s = ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE).getString("data", "");
            if (s == null || s.isEmpty()) return null;
            return new JSONObject(s);
        } catch (Exception e) { return null; }
    }

    private static String hm(long t) { return new SimpleDateFormat("HH:mm", Locale.US).format(new Date(t)); }

    static void updateOne(Context ctx, AppWidgetManager mgr, int id) {
        int size = 1; // 0 קטן, 1 בינוני, 2 גדול
        try {
            Bundle o = mgr.getAppWidgetOptions(id);
            int h = o.getInt(AppWidgetManager.OPTION_APPWIDGET_MIN_HEIGHT, 110);
            int hmax = o.getInt(AppWidgetManager.OPTION_APPWIDGET_MAX_HEIGHT, h);
            int hh = Math.max(h, Math.min(hmax, h + 40));
            size = hh < 100 ? 0 : (hh < 230 ? 1 : 2);
        } catch (Exception e) { }
        int layout = size == 0 ? R.layout.widget_small : (size == 1 ? R.layout.widget_medium : R.layout.widget_large);
        RemoteViews rv = new RemoteViews(ctx.getPackageName(), layout);
        rv.setOnClickPendingIntent(R.id.w_root, act(ctx, "home", 1));
        long now = System.currentTimeMillis();
        JSONObject d = data(ctx);
        try {
            if (d == null) {
                rv.setTextViewText(R.id.w_heb, "ברסלב PRO");
                rv.setTextViewText(R.id.w_zl, "פתחו את האפליקציה פעם אחת כדי לטעון את נתוני היום");
                rv.setViewVisibility(R.id.w_cd, View.GONE);
                mgr.updateAppWidget(id, rv);
                return;
            }
            JSONObject cfg = d.optJSONObject("cfg");
            if (cfg == null) cfg = new JSONObject();
            // לוגו ערוץ "גאולה וישועה" – קישור לערוץ
            rv.setViewVisibility(R.id.w_yt, cfg.optBoolean("yt", true) ? View.VISIBLE : View.GONE);
            rv.setOnClickPendingIntent(R.id.w_yt, web(ctx, d.optString("yt", "https://www.youtube.com/@yeshurun148"), 30));
            // היום (התאריך העברי מתחלף בצאת הכוכבים)
            JSONArray days = d.optJSONArray("days");
            JSONObject day = null;
            if (days != null) for (int k = 0; k < days.length(); k++) { JSONObject x = days.getJSONObject(k); if (x.optLong("from", 0) <= now) day = x; }
            if (day == null && days != null && days.length() > 0) day = days.getJSONObject(0);
            String heb = day != null ? day.optString("heb", "") : "";
            rv.setTextViewText(R.id.w_heb, heb);
            String par = day != null ? day.optString("par", "") : "";
            if (size > 0) { rv.setTextViewText(R.id.w_par, par); rv.setViewVisibility(R.id.w_par, par.isEmpty() ? View.GONE : View.VISIBLE); }

            // הזמן הקרוב + ספירה לאחור
            JSONArray zm = d.optJSONArray("zm");
            JSONObject nz = null; long nextT = 0;
            List<String> moreZ = new ArrayList<>();
            if (zm != null) for (int k = 0; k < zm.length(); k++) { JSONObject z = zm.getJSONObject(k); long t = z.optLong("t", 0); if (t > now) { if (nz == null) { nz = z; nextT = t; } else if (moreZ.size() < 3) moreZ.add("🕰️ " + z.optString("n") + " " + hm(t)); } }
            if (nz != null) {
                rv.setTextViewText(R.id.w_zl, nz.optString("i", "🕰️") + " " + nz.optString("n") + " · " + hm(nextT));
                rv.setViewVisibility(R.id.w_cd, View.VISIBLE);
                rv.setChronometer(R.id.w_cd, SystemClock.elapsedRealtime() + (nextT - now), "בעוד %s", true);
                rv.setChronometerCountDown(R.id.w_cd, true);
            } else { rv.setTextViewText(R.id.w_zl, "🕰️ זמני היום – פתחו את האפליקציה לעדכון"); rv.setViewVisibility(R.id.w_cd, View.GONE); }
            rv.setOnClickPendingIntent(R.id.w_zrow, act(ctx, "zm", 2));

            // סרגל מתחלף: הילולות, תזכורות, חומש היום, עוד זמנים
            List<String> tick = new ArrayList<>();
            if (day != null && cfg.optBoolean("tHil", true)) { JSONArray hil = day.optJSONArray("hil"); if (hil != null) for (int k = 0; k < hil.length(); k++) tick.add("🕯️ " + hil.getString(k)); }
            JSONArray rem = d.optJSONArray("rem");
            if (rem != null && cfg.optBoolean("tRem", true)) for (int k = 0; k < rem.length(); k++) { JSONObject r = rem.getJSONObject(k); long t = r.optLong("t", 0); if (t > now && t - now < 36L * 3600000L) tick.add("⏰ " + hm(t) + " · " + r.optString("n")); }
            if (day != null && !day.optString("aly", "").isEmpty() && cfg.optBoolean("tAly", true) && !(size == 2 && cfg.optBoolean("aly", true))) tick.add("📖 " + day.optString("aly"));
            if (day != null && !day.optString("ev", "").isEmpty() && cfg.optBoolean("tEv", true)) tick.add("✨ " + day.optString("ev"));
            if (day != null && !day.optString("hal", "").isEmpty() && cfg.optBoolean("tHal", true)) tick.add("⚖️ " + day.optString("hal"));
            if (cfg.optBoolean("tZm", true)) tick.addAll(moreZ);
            if (tick.isEmpty()) tick.add("✦ יום טוב! לחצו לפתיחת האפליקציה");
            rv.removeAllViews(R.id.w_flip);
            for (String t : tick) { RemoteViews it = new RemoteViews(ctx.getPackageName(), R.layout.widget_tick); it.setTextViewText(R.id.w_tick_t, t); rv.addView(R.id.w_flip, it); }
            rv.setOnClickPendingIntent(R.id.w_flip, act(ctx, "cal", 3));

            if (size > 0) {
                rv.setOnClickPendingIntent(R.id.b_rand, act(ctx, "random", 10));
                rv.setOnClickPendingIntent(R.id.b_cont, act(ctx, "cont", 11));
                rv.setOnClickPendingIntent(R.id.b_dir, act(ctx, "dir", 12));
                rv.setOnClickPendingIntent(R.id.b_tik, act(ctx, "tikkun", 13));
            }
            // דיבור מתחלף (מהספרים שנבחרו באפליקציה). בגדול – תמיד; בבינוני – אם סומן.
            boolean qShown = false;
            if (size > 0) {
                JSONArray qs = d.optJSONArray("quotes");
                boolean want = cfg.optBoolean("quote", true) && qs != null && qs.length() > 0 && (size == 2 || cfg.optBoolean("quoteMed", false));
                if (want) {
                    long qms = Math.max(1, cfg.optInt("qmin", 10)) * 60000L;
                    int off = ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE).getInt("qoff", 0);
                    JSONObject q = qs.getJSONObject((int) (((now / qms) + off) % qs.length()));
                    String src = q.optString("s", "");
                    rv.setTextViewText(R.id.w_quote, q.optString("t", "") + (src.isEmpty() ? "" : "\n— " + src));
                    rv.setOnClickPendingIntent(R.id.w_quote, act(ctx, "q:" + q.optString("id", ""), 20));
                    qShown = true;
                }
                rv.setViewVisibility(R.id.w_quote, want ? View.VISIBLE : View.GONE);
                if (qShown) {
                    Intent di = new Intent(ctx, BpWidget.class); di.setAction(DICE);
                    rv.setOnClickPendingIntent(R.id.b_rand, PendingIntent.getBroadcast(ctx, 78, di, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE));
                    rv.setTextViewText(R.id.b_rand, "🎲\nדיבור חדש");
                } else rv.setTextViewText(R.id.b_rand, "🎲\nפתיחה אקראית");
            }
            if (size == 2) {
                rv.setViewVisibility(R.id.w_aly, cfg.optBoolean("aly", true) ? View.VISIBLE : View.GONE);
                rv.setViewVisibility(R.id.w_cont, cfg.optBoolean("cont", true) ? View.VISIBLE : View.GONE);
                rv.setViewVisibility(R.id.w_dir, cfg.optBoolean("dir", true) ? View.VISIBLE : View.GONE);
                rv.setViewVisibility(R.id.w_row1, cfg.optBoolean("row1", true) ? View.VISIBLE : View.GONE);
                rv.setViewVisibility(R.id.w_row2, cfg.optBoolean("row2", true) ? View.VISIBLE : View.GONE);
                rv.setTextViewText(R.id.w_aly, day != null && !day.optString("aly", "").isEmpty() ? "📖 " + day.optString("aly") : "📖 חומש היום");
                rv.setOnClickPendingIntent(R.id.w_aly, act(ctx, "aly", 4));
                rv.setTextViewText(R.id.w_dir, "🧭 " + d.optString("dir", "כיוון התפילה"));
                rv.setOnClickPendingIntent(R.id.w_dir, act(ctx, "dir", 5));
                String cont = d.optString("cont", "");
                rv.setTextViewText(R.id.w_cont, cont.isEmpty() ? "📚 לספרייה" : "📚 המשך: " + cont);
                rv.setOnClickPendingIntent(R.id.w_cont, act(ctx, "cont", 6));
                rv.setOnClickPendingIntent(R.id.b_teh, act(ctx, "teh", 14));
                rv.setOnClickPendingIntent(R.id.b_cal, act(ctx, "cal", 15));
                rv.setOnClickPendingIntent(R.id.b_rem, act(ctx, "addrem", 16));
                rv.setOnClickPendingIntent(R.id.b_srch, act(ctx, "search", 17));
            }
        } catch (Exception e) { }
        mgr.updateAppWidget(id, rv);
    }

    /** רענון בזמן הקרוב (הזמן הבא שעובר / חצי שעה) */
    static void scheduleNext(Context ctx) {
        try {
            long now = System.currentTimeMillis(); long next = now + 30L * 60000L;
            JSONObject d = data(ctx);
            if (d != null) {
                JSONArray zm = d.optJSONArray("zm");
                if (zm != null) for (int k = 0; k < zm.length(); k++) { long t = zm.getJSONObject(k).optLong("t", 0); if (t > now + 5000) { next = Math.min(next, t + 3000); break; } }
                JSONObject cfg = d.optJSONObject("cfg");
                JSONArray qs = d.optJSONArray("quotes");
                if (qs != null && qs.length() > 1 && (cfg == null || cfg.optBoolean("quote", true))) {
                    long qms = Math.max(1, cfg == null ? 10 : cfg.optInt("qmin", 10)) * 60000L;
                    next = Math.min(next, ((now / qms) + 1) * qms + 800);
                }
                JSONArray days = d.optJSONArray("days");
                if (days != null) for (int k = 0; k < days.length(); k++) { long t = days.getJSONObject(k).optLong("from", 0); if (t > now + 5000) { next = Math.min(next, t + 3000); break; } }
            }
            Intent i = new Intent(ctx, BpWidget.class); i.setAction(TICK);
            PendingIntent pi = PendingIntent.getBroadcast(ctx, 77, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
            AlarmManager am = (AlarmManager) ctx.getSystemService(Context.ALARM_SERVICE);
            if (am != null) am.setAndAllowWhileIdle(AlarmManager.RTC, next, pi);
        } catch (Exception e) { }
    }
}
