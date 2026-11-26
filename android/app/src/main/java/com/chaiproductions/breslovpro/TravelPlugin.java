package com.chaiproductions.breslovpro;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.AlarmManager;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothManager;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;
import androidx.core.app.NotificationCompat;
import com.getcapacitor.JSArray;
import com.getcapacitor.JSObject;
import com.getcapacitor.PermissionState;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import com.getcapacitor.annotation.Permission;
import com.getcapacitor.annotation.PermissionCallback;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GoogleApiAvailability;
import com.google.android.gms.location.ActivityRecognition;
import com.google.android.gms.location.ActivityTransition;
import com.google.android.gms.location.ActivityTransitionRequest;
import com.google.android.gms.location.DetectedActivity;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.location.Priority;
import android.content.pm.PackageManager;
import androidx.core.content.ContextCompat;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

// 🚗 תזכורת לתפילת הדרך: מזהה נסיעה ברכב (חיישן "ברכב" של אנדרואיד) או חיבור לבלוטות' של הרכב,
// ואחרי 30 דקות ברצף – התראה אחת ביום. שום מידע לא יוצא מהטלפון.
@CapacitorPlugin(
    name = "Travel",
    permissions = {
        @Permission(strings = { Manifest.permission.ACTIVITY_RECOGNITION }, alias = "activity"),
        @Permission(strings = { Manifest.permission.BLUETOOTH_CONNECT }, alias = "bt"),
        @Permission(strings = { Manifest.permission.POST_NOTIFICATIONS }, alias = "notif"),
        @Permission(strings = { Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION }, alias = "loc"),
        @Permission(strings = { Manifest.permission.ACCESS_BACKGROUND_LOCATION }, alias = "bgloc")
    }
)
public class TravelPlugin extends Plugin {
    static final String PREFS = "bp_travel";
    static final long WAIT_MS = 30L * 60L * 1000L;

    static SharedPreferences prefs(Context c) { return c.getSharedPreferences(PREFS, Context.MODE_PRIVATE); }

    static boolean hasGms(Context c) {
        try { return GoogleApiAvailability.getInstance().isGooglePlayServicesAvailable(c) == ConnectionResult.SUCCESS; }
        catch (Throwable t) { return false; }
    }

    static PendingIntent trPI(Context c) {
        Intent i = new Intent(c, TravelReceiver.class).setAction(TravelReceiver.ACT_TR);
        int f = PendingIntent.FLAG_UPDATE_CURRENT | (Build.VERSION.SDK_INT >= 31 ? PendingIntent.FLAG_MUTABLE : 0);
        return PendingIntent.getBroadcast(c, 7101, i, f);
    }

    static PendingIntent checkPI(Context c) {
        Intent i = new Intent(c, TravelReceiver.class).setAction(TravelReceiver.ACT_CHECK);
        return PendingIntent.getBroadcast(c, 7102, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
    }

    @SuppressLint("MissingPermission")
    static boolean registerAR(Context c) {
        if (!hasGms(c)) return false;
        try {
            List<ActivityTransition> t = new ArrayList<>();
            t.add(new ActivityTransition.Builder().setActivityType(DetectedActivity.IN_VEHICLE).setActivityTransition(ActivityTransition.ACTIVITY_TRANSITION_ENTER).build());
            t.add(new ActivityTransition.Builder().setActivityType(DetectedActivity.IN_VEHICLE).setActivityTransition(ActivityTransition.ACTIVITY_TRANSITION_EXIT).build());
            ActivityRecognition.getClient(c).requestActivityTransitionUpdates(new ActivityTransitionRequest(t), trPI(c));
            return true;
        } catch (Throwable e) { return false; }
    }

    @SuppressLint("MissingPermission")
    static void unregisterAR(Context c) {
        try { ActivityRecognition.getClient(c).removeActivityTransitionUpdates(trPI(c)); } catch (Throwable e) { }
    }

    static void scheduleCheck(Context c, long at) {
        try {
            AlarmManager am = (AlarmManager) c.getSystemService(Context.ALARM_SERVICE);
            if (am == null) return;
            if (Build.VERSION.SDK_INT >= 23) am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, at, checkPI(c));
            else am.set(AlarmManager.RTC_WAKEUP, at, checkPI(c));
        } catch (Throwable e) { }
    }

    static void cancelCheck(Context c) {
        try { AlarmManager am = (AlarmManager) c.getSystemService(Context.ALARM_SERVICE); if (am != null) am.cancel(checkPI(c)); } catch (Throwable e) { }
    }

    // ---------- 🏎️ זיהוי לפי מהירות: רק נסיעה מהירה ורצופה (כביש בין־עירוני) מקפיצה תזכורת ----------
    static int kmh(Context c) { return prefs(c).getInt("kmh", 70); }
    static long fastMs(Context c) { return prefs(c).getInt("fastMin", 10) * 60000L; }
    static final long GRACE_MS = 150000L; // רמזור / פקק קצר – לא שובר את הרצף

    static boolean speedOk(Context c) {
        if (!prefs(c).getBoolean("useSpeed", true) || !hasGms(c)) return false;
        if (ContextCompat.checkSelfPermission(c, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) return false;
        return Build.VERSION.SDK_INT < 29 || ContextCompat.checkSelfPermission(c, Manifest.permission.ACCESS_BACKGROUND_LOCATION) == PackageManager.PERMISSION_GRANTED;
    }

    static PendingIntent locPI(Context c) {
        Intent i = new Intent(c, TravelReceiver.class).setAction(TravelReceiver.ACT_LOC);
        int f = PendingIntent.FLAG_UPDATE_CURRENT | (Build.VERSION.SDK_INT >= 31 ? PendingIntent.FLAG_MUTABLE : 0);
        return PendingIntent.getBroadcast(c, 7105, i, f);
    }

    @SuppressLint("MissingPermission")
    static void startLoc(Context c) {
        try {
            if (prefs(c).getBoolean("locOn", false)) return;
            LocationRequest r = new LocationRequest.Builder(Priority.PRIORITY_HIGH_ACCURACY, 20000L).setMinUpdateIntervalMillis(10000L).build();
            LocationServices.getFusedLocationProviderClient(c).requestLocationUpdates(r, locPI(c));
            prefs(c).edit().putBoolean("locOn", true).putLong("locSince", System.currentTimeMillis()).putLong("fastSince", 0).putLong("lastFast", 0).putLong("pT", 0).apply();
        } catch (Throwable e) { }
    }

    static void stopLoc(Context c) {
        try { LocationServices.getFusedLocationProviderClient(c).removeLocationUpdates(locPI(c)); } catch (Throwable e) { }
        prefs(c).edit().putBoolean("locOn", false).putLong("fastSince", 0).putLong("lastFast", 0).apply();
    }

    static String today() {
        java.util.Calendar k = java.util.Calendar.getInstance();
        return k.get(java.util.Calendar.YEAR) + "-" + k.get(java.util.Calendar.DAY_OF_YEAR);
    }

    // ההתראה עצמה – לחיצה פותחת את תפילת הדרך עם ההלכה
    static void notifyNow(Context c) {
        try {
            NotificationManager nm = (NotificationManager) c.getSystemService(Context.NOTIFICATION_SERVICE);
            if (nm == null) return;
            if (Build.VERSION.SDK_INT >= 26) {
                NotificationChannel ch = new NotificationChannel("travel", "תפילת הדרך", NotificationManager.IMPORTANCE_HIGH);
                ch.setDescription("תזכורת לתפילת הדרך כשיוצאים לנסיעה");
                nm.createNotificationChannel(ch);
            }
            Intent open = new Intent(c, MainActivity.class).putExtra("wact", "haderech").addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);
            PendingIntent pi = PendingIntent.getActivity(c, 7103, open, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
            NotificationCompat.Builder b = new NotificationCompat.Builder(c, "travel")
                .setSmallIcon(R.drawable.ic_stat_car)
                .setContentTitle("היי צדיק! 🚗 יצאת מהעיר?")
                .setContentText("רוצה לקרוא תפילת הדרך? לחצו כאן")
                .setPriority(NotificationCompat.PRIORITY_HIGH)
                .setAutoCancel(true)
                .setContentIntent(pi);
            nm.notify(7104, b.build());
        } catch (Throwable e) { }
    }

    // ---------- מהאפליקציה ----------
    private boolean need(String alias, int minSdk) { return Build.VERSION.SDK_INT >= minSdk && getPermissionState(alias) != PermissionState.GRANTED; }

    @PluginMethod
    public void status(PluginCall call) {
        SharedPreferences p = prefs(getContext());
        JSObject r = new JSObject();
        r.put("on", p.getBoolean("on", false));
        r.put("gms", hasGms(getContext()));
        r.put("car", p.getString("carName", ""));
        r.put("speed", speedOk(getContext()));
        r.put("useSpeed", p.getBoolean("useSpeed", true));
        r.put("kmh", kmh(getContext()));
        r.put("fastMin", p.getInt("fastMin", 10));
        r.put("tracking", p.getBoolean("locOn", false));
        call.resolve(r);
    }

    @PluginMethod
    public void start(PluginCall call) {
        if (need("notif", 33)) { requestPermissionForAlias("notif", call, "afterNotif"); return; }
        afterNotif(call);
    }

    @PermissionCallback
    private void afterNotif(PluginCall call) {
        if (hasGms(getContext()) && need("activity", 29)) { requestPermissionForAlias("activity", call, "afterActivity"); return; }
        afterActivity(call);
    }

    @PermissionCallback
    private void afterActivity(PluginCall call) {
        if (Boolean.TRUE.equals(call.getBoolean("speed", true)) && hasGms(getContext()) && need("loc", 23)) { requestPermissionForAlias("loc", call, "afterLoc"); return; }
        afterLoc(call);
    }

    @PermissionCallback
    private void afterLoc(PluginCall call) {
        if (Boolean.TRUE.equals(call.getBoolean("speed", true)) && hasGms(getContext()) && !need("loc", 23) && need("bgloc", 29)) { requestPermissionForAlias("bgloc", call, "afterBg"); return; }
        afterBg(call);
    }

    @PermissionCallback
    private void afterBg(PluginCall call) {
        Context c = getContext();
        prefs(c).edit().putBoolean("useSpeed", Boolean.TRUE.equals(call.getBoolean("speed", true))).apply();
        boolean ar = !need("activity", 29) && registerAR(c);
        prefs(c).edit().putBoolean("on", true).apply();
        JSObject r = new JSObject();
        r.put("ok", true);
        r.put("ar", ar);
        r.put("gms", hasGms(c));
        r.put("notif", !need("notif", 33));
        r.put("speed", speedOk(c));
        r.put("loc", !need("loc", 23));
        call.resolve(r);
    }

    // הגדרות המהירות: כמה קמ"ש וכמה דקות ברצף
    @PluginMethod
    public void setSpeed(PluginCall call) {
        SharedPreferences.Editor e = prefs(getContext()).edit();
        Integer k = call.getInt("kmh"), m = call.getInt("min");
        Boolean u = call.getBoolean("use");
        if (k != null) e.putInt("kmh", Math.max(40, Math.min(130, k)));
        if (m != null) e.putInt("fastMin", Math.max(3, Math.min(60, m)));
        if (u != null) e.putBoolean("useSpeed", u);
        e.apply();
        JSObject r = new JSObject(); r.put("speed", speedOk(getContext())); call.resolve(r);
    }

    @PluginMethod
    public void stop(PluginCall call) {
        Context c = getContext();
        stopLoc(c);
        unregisterAR(c);
        cancelCheck(c);
        prefs(c).edit().putBoolean("on", false).putLong("vehSince", 0).putLong("btSince", 0).apply();
        call.resolve();
    }

    // רשימת מכשירי הבלוטות' המוכרים – כדי לבחור את הרכב
    @PluginMethod
    public void bonded(PluginCall call) {
        if (need("bt", 31)) { requestPermissionForAlias("bt", call, "afterBt"); return; }
        afterBt(call);
    }

    @SuppressLint("MissingPermission")
    @PermissionCallback
    private void afterBt(PluginCall call) {
        JSArray a = new JSArray();
        try {
            if (need("bt", 31)) { call.reject("no bluetooth permission"); return; }
            BluetoothManager bm = (BluetoothManager) getContext().getSystemService(Context.BLUETOOTH_SERVICE);
            BluetoothAdapter ad = bm != null ? bm.getAdapter() : null;
            Set<BluetoothDevice> s = ad != null ? ad.getBondedDevices() : null;
            if (s != null) for (BluetoothDevice d : s) {
                JSObject o = new JSObject();
                o.put("name", d.getName() != null ? d.getName() : d.getAddress());
                o.put("addr", d.getAddress());
                a.put(o);
            }
        } catch (Throwable e) { }
        JSObject r = new JSObject();
        r.put("list", a);
        call.resolve(r);
    }

    @PluginMethod
    public void setCar(PluginCall call) {
        String addr = call.getString("addr", ""), name = call.getString("name", "");
        prefs(getContext()).edit().putString("carAddr", addr).putString("carName", name).apply();
        call.resolve();
    }

    // בדיקה: מקפיץ את ההתראה עכשיו
    @PluginMethod
    public void test(PluginCall call) {
        notifyNow(getContext());
        call.resolve();
    }

    @Override
    public void load() {
        // אחרי עדכון / הפעלה מחדש – רושמים שוב את הזיהוי
        try { if (prefs(getContext()).getBoolean("on", false)) registerAR(getContext()); } catch (Throwable e) { }
    }
}
