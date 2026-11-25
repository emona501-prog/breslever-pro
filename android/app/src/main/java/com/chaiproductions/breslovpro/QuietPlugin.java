package com.chaiproductions.breslovpro;

import android.app.NotificationManager;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.media.AudioManager;
import android.os.Build;
import android.provider.Settings;
import android.widget.Toast;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

/** 🤫 שקט בזמן תפילה: רטט / השתקה מלאה, וחזרה אוטומטית למצב הקודם ברגע שיוצאים מהתפילה או מהאפליקציה */
@CapacitorPlugin(name = "Quiet")
public class QuietPlugin extends Plugin {
    static final String P = "bp_quiet";

    @Override
    public void load() {
        // אם האפליקציה נסגרה באמצע תפילה – מחזירים את הצליל
        try { restoreNow(getContext()); } catch (Exception e) { }
    }

    private static SharedPreferences sp(Context c) { return c.getSharedPreferences(P, Context.MODE_PRIVATE); }

    private static boolean dnd(Context c) {
        NotificationManager nm = (NotificationManager) c.getSystemService(Context.NOTIFICATION_SERVICE);
        return Build.VERSION.SDK_INT < 23 || (nm != null && nm.isNotificationPolicyAccessGranted());
    }

    private static boolean air(Context c) {
        try { return Settings.Global.getInt(c.getContentResolver(), Settings.Global.AIRPLANE_MODE_ON, 0) != 0; } catch (Exception e) { return false; }
    }

    static boolean restoreNow(Context c) {
        SharedPreferences s = sp(c);
        if (!s.getBoolean("on", false)) return false;
        try {
            AudioManager am = (AudioManager) c.getSystemService(Context.AUDIO_SERVICE);
            if (am != null) am.setRingerMode(s.getInt("prev", AudioManager.RINGER_MODE_NORMAL));
        } catch (Exception e) { }
        s.edit().putBoolean("on", false).apply();
        return true;
    }

    @PluginMethod
    public void info(PluginCall call) {
        Context c = getContext(); JSObject r = new JSObject();
        AudioManager am = (AudioManager) c.getSystemService(Context.AUDIO_SERVICE);
        r.put("ringer", am != null ? am.getRingerMode() : -1);
        r.put("dnd", dnd(c));
        r.put("air", air(c));
        r.put("on", sp(c).getBoolean("on", false));
        call.resolve(r);
    }

    @PluginMethod
    public void quiet(PluginCall call) {
        Context c = getContext(); JSObject r = new JSObject();
        String mode = call.getString("mode", "vibrate");
        boolean silent = "silent".equals(mode);
        try {
            AudioManager am = (AudioManager) c.getSystemService(Context.AUDIO_SERVICE);
            if (am == null) throw new Exception("no audio");
            if (silent && !dnd(c)) { r.put("ok", false); r.put("need", "dnd"); call.resolve(r); return; }
            int cur = am.getRingerMode();
            SharedPreferences s = sp(c);
            if (!s.getBoolean("on", false)) s.edit().putInt("prev", cur).putBoolean("on", true).apply();
            int want = silent ? AudioManager.RINGER_MODE_SILENT : AudioManager.RINGER_MODE_VIBRATE;
            if (cur != want && !(cur == AudioManager.RINGER_MODE_SILENT && !silent)) am.setRingerMode(want);
            r.put("ok", true);
            r.put("was", cur);
        } catch (SecurityException e) {
            sp(c).edit().putBoolean("on", false).apply();
            r.put("ok", false); r.put("need", "dnd");
        } catch (Exception e) {
            r.put("ok", false);
        }
        call.resolve(r);
    }

    /** 🔕 לוח זמני שקט קבוע – האפליקציה שולחת את החלונות לימים הקרובים, והטלפון עובד לפיהם לבד */
    @PluginMethod
    public void setSched(PluginCall call) {
        Context c = getContext(); JSObject r = new JSObject();
        try {
            QuietSchedReceiver.sp(c).edit().putString("w", call.getString("w", "[]")).putBoolean("on", Boolean.TRUE.equals(call.getBoolean("on", false))).apply();
            QuietSchedReceiver.plan(c);
            r.put("ok", true);
            SharedPreferences s = QuietSchedReceiver.sp(c);
            r.put("act", s.getLong("actE", 0) > 0);
            r.put("actN", s.getString("actN", ""));
            r.put("actE", s.getLong("actE", 0));
        } catch (Exception e) { r.put("ok", false); }
        r.put("dnd", dnd(c));
        call.resolve(r);
    }

    @PluginMethod
    public void skipSched(PluginCall call) {
        Context c = getContext();
        QuietSchedReceiver.skip(c); QuietSchedReceiver.plan(c);
        JSObject r = new JSObject(); r.put("ok", true); call.resolve(r);
    }

    @PluginMethod
    public void restore(PluginCall call) {
        JSObject r = new JSObject();
        r.put("ok", restoreNow(getContext()));
        call.resolve(r);
    }

    private void open(PluginCall call, String action) {
        JSObject r = new JSObject();
        try {
            Intent i = new Intent(action);
            i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            getContext().startActivity(i);
            r.put("ok", true);
        } catch (Exception e) { r.put("ok", false); }
        call.resolve(r);
    }

    @PluginMethod
    public void openDnd(PluginCall call) { open(call, Settings.ACTION_NOTIFICATION_POLICY_ACCESS_SETTINGS); }

    @PluginMethod
    public void openAirplane(PluginCall call) { open(call, Settings.ACTION_AIRPLANE_MODE_SETTINGS); }

    @Override
    protected void handleOnPause() {
        super.handleOnPause();
        // יוצאים מהאפליקציה באמצע תפילה – הצליל חוזר מיד לקדמותו
        Context c = getContext();
        if (restoreNow(c)) {
            try { Toast.makeText(c, "🔔 הצליל של הטלפון חזר לקדמותו", Toast.LENGTH_SHORT).show(); } catch (Exception e) { }
            try { getBridge().getWebView().post(() -> getBridge().getWebView().evaluateJavascript("try{window.__qtPaused&&window.__qtPaused()}catch(e){}", null)); } catch (Exception e) { }
        }
    }
}
