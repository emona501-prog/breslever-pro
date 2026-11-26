package com.chaiproductions.breslovpro;

import android.annotation.SuppressLint;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;
import com.google.android.gms.location.ActivityTransition;
import com.google.android.gms.location.ActivityTransitionEvent;
import com.google.android.gms.location.ActivityTransitionResult;
import com.google.android.gms.location.DetectedActivity;
import com.google.android.gms.location.LocationResult;
import android.location.Location;

// 🚗 מקבל: כניסה/יציאה מרכב, חיבור/ניתוק בלוטות' של הרכב, בדיקה אחרי 30 דקות, והפעלה מחדש של הטלפון
public class TravelReceiver extends BroadcastReceiver {
    static final String ACT_TR = "bp.travel.tr";
    static final String ACT_CHECK = "bp.travel.check";
    static final String ACT_LOC = "bp.travel.loc";

    @SuppressLint("MissingPermission")
    @Override
    public void onReceive(Context c, Intent in) {
        try {
            SharedPreferences p = TravelPlugin.prefs(c);
            if (!p.getBoolean("on", false)) return;
            String a = in.getAction();
            long now = System.currentTimeMillis();
            if (ActivityTransitionResult.hasResult(in)) {
                ActivityTransitionResult r = ActivityTransitionResult.extractResult(in);
                if (r == null) return;
                for (ActivityTransitionEvent e : r.getTransitionEvents()) {
                    if (e.getActivityType() != DetectedActivity.IN_VEHICLE) continue;
                    if (e.getTransitionType() == ActivityTransition.ACTIVITY_TRANSITION_ENTER) {
                        p.edit().putLong("vehSince", now).apply();
                        tripStart(c, now);
                    } else {
                        p.edit().putLong("vehSince", 0).apply();
                        if (p.getLong("btSince", 0) == 0) { TravelPlugin.cancelCheck(c); TravelPlugin.stopLoc(c); }
                    }
                }
                return;
            }
            if (a == null) return;
            if (BluetoothDevice.ACTION_ACL_CONNECTED.equals(a) || BluetoothDevice.ACTION_ACL_DISCONNECTED.equals(a)) {
                String car = p.getString("carAddr", "");
                BluetoothDevice d = in.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
                if (car.isEmpty() || d == null || !car.equalsIgnoreCase(d.getAddress())) return;
                if (BluetoothDevice.ACTION_ACL_CONNECTED.equals(a)) {
                    p.edit().putLong("btSince", now).apply();
                    tripStart(c, now);
                } else {
                    p.edit().putLong("btSince", 0).apply();
                    if (p.getLong("vehSince", 0) == 0) { TravelPlugin.cancelCheck(c); TravelPlugin.stopLoc(c); }
                }
                return;
            }
            if (ACT_LOC.equals(a)) {
                if (!LocationResult.hasResult(in)) return;
                LocationResult lr = LocationResult.extractResult(in);
                if (lr == null) return;
                // בטיחות: לא עוקבים יותר מ־4 שעות ברצף
                if (now - p.getLong("locSince", now) > 4L * 3600000L) { TravelPlugin.stopLoc(c); return; }
                for (Location L : lr.getLocations()) onLoc(c, p, L);
                return;
            }
            if (ACT_CHECK.equals(a)) {
                long since = Math.max(p.getLong("vehSince", 0), p.getLong("btSince", 0));
                if (since == 0 || now - since < TravelPlugin.WAIT_MS - 60000L) return;
                String day = TravelPlugin.today();
                if (day.equals(p.getString("lastDay", ""))) return; // פעם אחת ביום
                p.edit().putString("lastDay", day).apply();
                TravelPlugin.notifyNow(c);
                return;
            }
            if (Intent.ACTION_BOOT_COMPLETED.equals(a) || Intent.ACTION_MY_PACKAGE_REPLACED.equals(a)) {
                p.edit().putLong("vehSince", 0).putLong("btSince", 0).apply();
                TravelPlugin.stopLoc(c);
                TravelPlugin.registerAR(c);
            }
        } catch (Throwable e) { }
    }

    // תחילת נסיעה: עם הרשאת מיקום – מודדים מהירות; בלי – כמו פעם, לפי חצי שעה בנסיעה
    static void tripStart(Context c, long now) {
        if (TravelPlugin.today().equals(TravelPlugin.prefs(c).getString("lastDay", ""))) return; // כבר הזכרנו היום
        if (TravelPlugin.speedOk(c)) { TravelPlugin.cancelCheck(c); TravelPlugin.startLoc(c); }
        else TravelPlugin.scheduleCheck(c, now + TravelPlugin.WAIT_MS);
    }

    // כל נקודת מיקום: מהירות מעל הסף X דקות ברצף (עם סליחה לרמזור/פקק קצר) → תזכורת
    static void onLoc(Context c, SharedPreferences p, Location L) {
        long t = L.getTime();
        float ms = -1f;
        if (L.hasSpeed() && (Build.VERSION.SDK_INT < 26 || !L.hasSpeedAccuracy() || L.getSpeedAccuracyMetersPerSecond() < 5f)) ms = L.getSpeed();
        else {
            long pt = p.getLong("pT", 0);
            if (pt > 0 && t - pt > 3000 && t - pt < 120000) {
                float[] d = new float[1];
                Location.distanceBetween(Double.longBitsToDouble(p.getLong("pLa", 0)), Double.longBitsToDouble(p.getLong("pLo", 0)), L.getLatitude(), L.getLongitude(), d);
                ms = d[0] / ((t - pt) / 1000f);
            }
        }
        SharedPreferences.Editor e = p.edit().putLong("pT", t).putLong("pLa", Double.doubleToLongBits(L.getLatitude())).putLong("pLo", Double.doubleToLongBits(L.getLongitude()));
        if (ms < 0 || L.getAccuracy() > 80f) { e.apply(); return; }
        float kmh = ms * 3.6f;
        long fs = p.getLong("fastSince", 0), lf = p.getLong("lastFast", 0);
        if (kmh >= TravelPlugin.kmh(c)) {
            if (fs == 0 || t - lf > GRACE()) fs = t;
            lf = t;
        } else if (fs > 0 && t - lf > GRACE()) { fs = 0; }
        e.putLong("fastSince", fs).putLong("lastFast", lf).apply();
        if (fs > 0 && lf - fs >= TravelPlugin.fastMs(c)) {
            String day = TravelPlugin.today();
            if (!day.equals(p.getString("lastDay", ""))) {
                p.edit().putString("lastDay", day).apply();
                TravelPlugin.notifyNow(c);
            }
            TravelPlugin.stopLoc(c);
        }
    }

    static long GRACE() { return TravelPlugin.GRACE_MS; }
}
