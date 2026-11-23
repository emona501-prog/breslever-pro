package com.chaiproductions.breslovpro;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.media.AudioAttributes;
import android.media.RingtoneManager;
import android.os.Build;
import androidx.core.app.NotificationCompat;

/** מגיע הזמן – מקפיץ מסך מלא (גם על מסך נעול) עם צליל שעון מעורר */
public class BpAlarmReceiver extends BroadcastReceiver {
    static final String CH = "bp_alarm_v1";

    @Override
    public void onReceive(Context ctx, Intent in) {
        String a = in.getAction();
        if (Intent.ACTION_BOOT_COMPLETED.equals(a) || Intent.ACTION_MY_PACKAGE_REPLACED.equals(a)) { BpAlarmPlugin.restore(ctx); return; }
        int id = in.getIntExtra("id", 1);
        String title = in.getStringExtra("title"), body = in.getStringExtra("body"), extra = in.getStringExtra("extra");
        NotificationManager nm = (NotificationManager) ctx.getSystemService(Context.NOTIFICATION_SERVICE);
        if (Build.VERSION.SDK_INT >= 26 && nm.getNotificationChannel(CH) == null) {
            NotificationChannel c = new NotificationChannel(CH, "⏰ תזכורות שעון מעורר", NotificationManager.IMPORTANCE_HIGH);
            c.setDescription("תזכורות במסך מלא עם צליל שעון מעורר");
            c.setSound(RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM), new AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_ALARM).build());
            c.enableVibration(true); c.setVibrationPattern(new long[] { 0, 800, 400, 800, 400, 800 });
            c.setBypassDnd(true); c.setLockscreenVisibility(Notification.VISIBILITY_PUBLIC);
            nm.createNotificationChannel(c);
        }
        Intent full = new Intent(ctx, BpAlarmActivity.class);
        full.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_NO_USER_ACTION);
        full.putExtra("id", id); full.putExtra("title", title); full.putExtra("body", body); full.putExtra("extra", extra);
        PendingIntent fp = PendingIntent.getActivity(ctx, id, full, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        NotificationCompat.Builder b = new NotificationCompat.Builder(ctx, CH)
            .setSmallIcon(ctx.getApplicationInfo().icon)
            .setContentTitle(title == null ? "ברסלב PRO" : title)
            .setContentText(body == null ? "" : body)
            .setPriority(NotificationCompat.PRIORITY_MAX)
            .setCategory(NotificationCompat.CATEGORY_ALARM)
            .setFullScreenIntent(fp, true)
            .setContentIntent(fp)
            .setAutoCancel(true)
            .setOngoing(true);
        try { nm.notify(7000 + (id % 1000), b.build()); } catch (Exception e) { }
        // אם המסך פתוח והטלפון לא נעול – אנדרואיד מציג רק התראה עליונה; ננסה לפתוח את המסך המלא ישירות
        try { ctx.startActivity(full); } catch (Exception e) { }
    }
}
