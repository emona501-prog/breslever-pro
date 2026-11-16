package com.chaiproductions.breslovpro;

import android.annotation.SuppressLint;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import com.google.android.gms.location.ActivityTransition;
import com.google.android.gms.location.ActivityTransitionEvent;
import com.google.android.gms.location.ActivityTransitionResult;
import com.google.android.gms.location.DetectedActivity;

// 🚗 מקבל: כניסה/יציאה מרכב, חיבור/ניתוק בלוטות' של הרכב, בדיקה אחרי 30 דקות, והפעלה מחדש של הטלפון
public class TravelReceiver extends BroadcastReceiver {
    static final String ACT_TR = "bp.travel.tr";
    static final String ACT_CHECK = "bp.travel.check";

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
                        TravelPlugin.scheduleCheck(c, now + TravelPlugin.WAIT_MS);
                    } else {
                        p.edit().putLong("vehSince", 0).apply();
                        if (p.getLong("btSince", 0) == 0) TravelPlugin.cancelCheck(c);
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
                    TravelPlugin.scheduleCheck(c, now + TravelPlugin.WAIT_MS);
                } else {
                    p.edit().putLong("btSince", 0).apply();
                    if (p.getLong("vehSince", 0) == 0) TravelPlugin.cancelCheck(c);
                }
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
                TravelPlugin.registerAR(c);
            }
        } catch (Throwable e) { }
    }
}
