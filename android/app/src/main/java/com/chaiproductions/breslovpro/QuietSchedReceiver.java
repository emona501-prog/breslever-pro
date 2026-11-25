package com.chaiproductions.breslovpro;

import android.app.AlarmManager;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.media.AudioManager;
import android.os.Build;
import androidx.core.app.NotificationCompat;

import org.json.JSONArray;
import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

/**
 * 🔕 לוח זמני שקט קבוע: חלונות זמן (שחרית, מנחה, ערבית, שיעור…) שהאפליקציה מחשבת מראש לימים הקרובים.
 * בתחילת חלון – רטט / השתקה; בסוף – חוזרים בדיוק למצב שהיה (רק אם אנחנו שינינו ואף אחד לא נגע בינתיים).
 * עובד גם כשהאפליקציה סגורה ואחרי הפעלה מחדש של הטלפון.
 */
public class QuietSchedReceiver extends BroadcastReceiver {
    static final String P = "bp_qsched", CH = "bp_qsched_v1", TICK = "bp.qs.TICK", SKIP = "bp.qs.SKIP";
    static final int NID = 7700;

    static SharedPreferences sp(Context c) { return c.getSharedPreferences(P, Context.MODE_PRIVATE); }

    @Override
    public void onReceive(Context c, Intent in) {
        String a = in.getAction();
        if (SKIP.equals(a)) skip(c);
        plan(c);
    }

    static boolean dnd(Context c) {
        NotificationManager nm = (NotificationManager) c.getSystemService(Context.NOTIFICATION_SERVICE);
        return Build.VERSION.SDK_INT < 23 || (nm != null && nm.isNotificationPolicyAccessGranted());
    }

    /** מסתכל על השעה עכשיו: נכנס לחלון / יוצא מחלון, וקובע את ההתעוררות הבאה */
    static synchronized void plan(Context c) {
        SharedPreferences s = sp(c);
        long now = System.currentTimeMillis();
        JSONArray w;
        try { w = new JSONArray(s.getString("w", "[]")); } catch (Exception e) { w = new JSONArray(); }
        boolean on = s.getBoolean("on", false);
        long actE = s.getLong("actE", 0);
        // יציאה מחלון שהסתיים (או שהלוח כובה)
        if (actE > 0 && (now >= actE - 1000 || !on)) end(c);
        actE = s.getLong("actE", 0);
        long next = Long.MAX_VALUE;
        if (on) {
            long skipS = s.getLong("skip", 0);
            for (int i = 0; i < w.length(); i++) {
                JSONObject o = w.optJSONObject(i);
                if (o == null) continue;
                long st = o.optLong("s"), en = o.optLong("e");
                if (en <= now) continue;
                if (st <= now + 1000) {
                    if (actE == 0 && st != skipS) { start(c, o); actE = en; }
                    if (en < next) next = en;
                } else if (st < next) next = st;
            }
        }
        if (actE > 0 && actE < next) next = actE;
        AlarmManager am = (AlarmManager) c.getSystemService(Context.ALARM_SERVICE);
        Intent t = new Intent(c, QuietSchedReceiver.class).setAction(TICK);
        PendingIntent p = PendingIntent.getBroadcast(c, 7701, t, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        am.cancel(p);
        if (next == Long.MAX_VALUE) return;
        boolean exact = Build.VERSION.SDK_INT < 31 || am.canScheduleExactAlarms();
        if (exact) am.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, next, p);
        else am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, next, p);
    }

    static void start(Context c, JSONObject o) {
        SharedPreferences s = sp(c);
        int set = -1, want = AudioManager.RINGER_MODE_VIBRATE;
        try {
            AudioManager am = (AudioManager) c.getSystemService(Context.AUDIO_SERVICE);
            int cur = am.getRingerMode();
            if ("silent".equals(o.optString("m")) && dnd(c)) want = AudioManager.RINGER_MODE_SILENT;
            // כבר שקט / כבר במצב הרצוי – לא נוגעים (וגם לא נחזיר בסוף)
            if (cur != want && cur != AudioManager.RINGER_MODE_SILENT) {
                s.edit().putInt("prev", cur).apply();
                am.setRingerMode(want);
                set = want;
            }
        } catch (Exception e) { set = -1; }
        s.edit().putLong("actS", o.optLong("s")).putLong("actE", o.optLong("e")).putInt("set", set).putString("actN", o.optString("n")).apply();
        note(c, o.optString("n"), o.optLong("e"), want == AudioManager.RINGER_MODE_SILENT);
    }

    static void end(Context c) {
        SharedPreferences s = sp(c);
        int set = s.getInt("set", -1);
        try {
            AudioManager am = (AudioManager) c.getSystemService(Context.AUDIO_SERVICE);
            // מחזירים רק אם המצב עדיין מה שאנחנו קבענו (אם המשתמש שינה בעצמו – מכבדים)
            if (set != -1 && am.getRingerMode() == set) am.setRingerMode(s.getInt("prev", AudioManager.RINGER_MODE_NORMAL));
        } catch (Exception e) { }
        s.edit().putLong("actE", 0).putLong("actS", 0).putInt("set", -1).apply();
        try { ((NotificationManager) c.getSystemService(Context.NOTIFICATION_SERVICE)).cancel(NID); } catch (Exception e) { }
    }

    /** "בטל הפעם" – מחזירים את הצליל עכשיו ולא נכנסים שוב לאותו חלון */
    static void skip(Context c) {
        SharedPreferences s = sp(c);
        long st = s.getLong("actS", 0);
        end(c);
        s.edit().putLong("skip", st).apply();
    }

    static void note(Context c, String name, long until, boolean silent) {
        try {
            NotificationManager nm = (NotificationManager) c.getSystemService(Context.NOTIFICATION_SERVICE);
            if (Build.VERSION.SDK_INT >= 26 && nm.getNotificationChannel(CH) == null) {
                NotificationChannel ch = new NotificationChannel(CH, "🔕 לוח זמני שקט", NotificationManager.IMPORTANCE_LOW);
                ch.setDescription("הודעה שקטה כשהטלפון עובר לרטט / שקט לפי הלוח");
                ch.setSound(null, null); ch.enableVibration(false);
                nm.createNotificationChannel(ch);
            }
            String t = new SimpleDateFormat("HH:mm", Locale.getDefault()).format(new Date(until));
            Intent sk = new Intent(c, QuietSchedReceiver.class).setAction(SKIP);
            PendingIntent skp = PendingIntent.getBroadcast(c, 7702, sk, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
            Intent op = c.getPackageManager().getLaunchIntentForPackage(c.getPackageName());
            PendingIntent opp = op == null ? null : PendingIntent.getActivity(c, 7703, op, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
            NotificationCompat.Builder b = new NotificationCompat.Builder(c, CH)
                .setSmallIcon(c.getApplicationInfo().icon)
                .setContentTitle((silent ? "🔕 " : "📳 ") + (name == null || name.isEmpty() ? "זמן שקט" : name))
                .setContentText((silent ? "הטלפון בשקט" : "הטלפון ברטט") + " עד " + t + " · ברסלב PRO")
                .setPriority(NotificationCompat.PRIORITY_LOW)
                .setOngoing(true)
                .setSilent(true)
                .addAction(0, "🔔 בטל הפעם", skp);
            if (opp != null) b.setContentIntent(opp);
            nm.notify(NID, b.build());
        } catch (Exception e) { }
    }
}
