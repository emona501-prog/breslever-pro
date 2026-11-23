package com.chaiproductions.breslovpro;

import android.app.AlarmManager;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Build;
import android.provider.Settings;
import com.getcapacitor.JSArray;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import org.json.JSONArray;
import org.json.JSONObject;

/** ⏰ תזכורות "שעון מעורר": מסך מלא עם צליל שעון מעורר ורטט – גם כשהטלפון נעול */
@CapacitorPlugin(name = "BpAlarm")
public class BpAlarmPlugin extends Plugin {
    static final String PREFS = "bp_alarm";

    static PendingIntent pi(Context ctx, int id, String title, String body, String extra) {
        Intent i = new Intent(ctx, BpAlarmReceiver.class);
        i.setAction("bp.alarm." + id);
        i.putExtra("id", id); i.putExtra("title", title); i.putExtra("body", body); i.putExtra("extra", extra);
        return PendingIntent.getBroadcast(ctx, id, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
    }

    static void setOne(Context ctx, int id, long at, String title, String body, String extra) {
        AlarmManager am = (AlarmManager) ctx.getSystemService(Context.ALARM_SERVICE);
        PendingIntent p = pi(ctx, id, title, body, extra);
        boolean exact = Build.VERSION.SDK_INT < 31 || am.canScheduleExactAlarms();
        if (exact) {
            Intent show = new Intent(ctx, MainActivity.class);
            PendingIntent sp = PendingIntent.getActivity(ctx, 0, show, PendingIntent.FLAG_IMMUTABLE);
            am.setAlarmClock(new AlarmManager.AlarmClockInfo(at, sp), p);
        } else am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, at, p);
    }

    /** מתזמן מחדש את כל מה ששמור (אחרי הפעלה מחדש של הטלפון) */
    static void restore(Context ctx) {
        try {
            JSONArray a = new JSONArray(ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE).getString("items", "[]"));
            long now = System.currentTimeMillis();
            for (int k = 0; k < a.length(); k++) {
                JSONObject o = a.getJSONObject(k);
                if (o.getLong("at") > now) setOne(ctx, o.getInt("id"), o.getLong("at"), o.optString("title"), o.optString("body"), o.optString("extra"));
            }
        } catch (Exception e) { }
    }

    static void cancelAll(Context ctx) {
        SharedPreferences sp = ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE);
        try {
            JSONArray a = new JSONArray(sp.getString("items", "[]"));
            AlarmManager am = (AlarmManager) ctx.getSystemService(Context.ALARM_SERVICE);
            for (int k = 0; k < a.length(); k++) {
                JSONObject o = a.getJSONObject(k);
                am.cancel(pi(ctx, o.getInt("id"), "", "", ""));
            }
        } catch (Exception e) { }
        sp.edit().putString("items", "[]").apply();
    }

    @PluginMethod
    public void schedule(PluginCall call) {
        Context ctx = getContext();
        cancelAll(ctx);
        JSArray items = call.getArray("items", new JSArray());
        JSONArray keep = new JSONArray();
        long now = System.currentTimeMillis();
        try {
            for (int k = 0; k < items.length() && k < 120; k++) {
                JSONObject o = items.getJSONObject(k);
                long at = o.getLong("at");
                if (at <= now) continue;
                setOne(ctx, o.getInt("id"), at, o.optString("title"), o.optString("body"), o.optString("extra"));
                keep.put(o);
            }
        } catch (Exception e) { }
        ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE).edit().putString("items", keep.toString()).apply();
        JSObject r = new JSObject(); r.put("n", keep.length()); call.resolve(r);
    }

    @PluginMethod
    public void cancel(PluginCall call) { cancelAll(getContext()); call.resolve(); }

    @PluginMethod
    public void test(PluginCall call) {
        setOne(getContext(), 9999, System.currentTimeMillis() + 5000, call.getString("title", "⏰ בדיקת שעון מעורר"), call.getString("body", "כך תיראה התזכורת"), "{}");
        call.resolve();
    }

    @PluginMethod
    public void perm(PluginCall call) {
        Context ctx = getContext();
        JSObject r = new JSObject();
        boolean fsi = true, exact = true;
        if (Build.VERSION.SDK_INT >= 34) fsi = ((NotificationManager) ctx.getSystemService(Context.NOTIFICATION_SERVICE)).canUseFullScreenIntent();
        if (Build.VERSION.SDK_INT >= 31) exact = ((AlarmManager) ctx.getSystemService(Context.ALARM_SERVICE)).canScheduleExactAlarms();
        r.put("fsi", fsi); r.put("exact", exact); call.resolve(r);
    }

    @PluginMethod
    public void openFsi(PluginCall call) {
        try {
            Intent i;
            if (Build.VERSION.SDK_INT >= 34) i = new Intent(Settings.ACTION_MANAGE_APP_USE_FULL_SCREEN_INTENT, Uri.parse("package:" + getContext().getPackageName()));
            else if (Build.VERSION.SDK_INT >= 31) i = new Intent(Settings.ACTION_REQUEST_SCHEDULE_EXACT_ALARM, Uri.parse("package:" + getContext().getPackageName()));
            else i = new Intent(Settings.ACTION_APP_NOTIFICATION_SETTINGS).putExtra(Settings.EXTRA_APP_PACKAGE, getContext().getPackageName());
            i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            getContext().startActivity(i);
        } catch (Exception e) { }
        call.resolve();
    }

    /** לחיצה על "פתיחה" במסך המעורר – האפליקציה שואלת לאן לעבור */
    @PluginMethod
    public void takeOpen(PluginCall call) {
        SharedPreferences sp = getContext().getSharedPreferences(PREFS, Context.MODE_PRIVATE);
        String x = sp.getString("open", "");
        sp.edit().remove("open").apply();
        JSObject r = new JSObject(); r.put("extra", x); call.resolve(r);
    }
}
