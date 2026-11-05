package com.chaiproductions.breslovpro;

import android.content.Context;
import android.hardware.GeomagneticField;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

/** מצפן מדויק: קורא ישירות את חיישן הסיבוב של הטלפון, ומתקן לצפון האמיתי (סטיה מגנטית לפי המיקום) */
@CapacitorPlugin(name = "Compass")
public class CompassPlugin extends Plugin implements SensorEventListener {
    private SensorManager sm;
    private Sensor sensor;
    private float decl = 0f;
    private long last = 0;
    private int acc = 3;
    private final float[] R = new float[9];

    @PluginMethod
    public void start(PluginCall call) {
        try {
            sm = (SensorManager) getContext().getSystemService(Context.SENSOR_SERVICE);
            if (sm == null) { call.reject("no sensor manager"); return; }
            sensor = sm.getDefaultSensor(Sensor.TYPE_ROTATION_VECTOR);
            src = "rv";
            if (sensor == null) { sensor = sm.getDefaultSensor(Sensor.TYPE_GEOMAGNETIC_ROTATION_VECTOR); src = "geo"; }
            inited = false;
            if (sensor == null) { call.reject("no rotation sensor"); return; }
            Double lat = call.getDouble("lat"), lon = call.getDouble("lon");
            if (lat != null && lon != null) {
                GeomagneticField gf = new GeomagneticField(lat.floatValue(), lon.floatValue(), 0f, System.currentTimeMillis());
                decl = gf.getDeclination();
            }
            sm.unregisterListener(this);
            sm.registerListener(this, sensor, SensorManager.SENSOR_DELAY_GAME);
            JSObject r = new JSObject(); r.put("ok", true); r.put("decl", decl);
            call.resolve(r);
        } catch (Exception e) { call.reject("compass failed: " + e.getMessage()); }
    }

    @PluginMethod
    public void stop(PluginCall call) {
        try { if (sm != null) sm.unregisterListener(this); } catch (Exception e) { }
        call.resolve();
    }

    @Override
    protected void handleOnPause() { try { if (sm != null) sm.unregisterListener(this); } catch (Exception e) { } }

    private double fs = 0, fc = 0; private boolean inited = false, flatState = true; private String src = "rv";

    @Override
    public void onSensorChanged(SensorEvent ev) {
        SensorManager.getRotationMatrixFromVector(R, ev.values);
        // שטוח / זקוף – עם "השהיה" כדי שלא יקפוץ בין המצבים
        float up = Math.abs(R[8]);
        if (flatState && up < 0.55f) flatState = false; else if (!flatState && up > 0.75f) flatState = true;
        double h = flatState ? Math.atan2(R[1], R[4]) : Math.atan2(-R[2], -R[5]);
        // סינון רעידות: ממוצע נע על הכיוון (סינוס/קוסינוס) – חלק ויציב
        double s1 = Math.sin(h), c1 = Math.cos(h);
        if (!inited) { fs = s1; fc = c1; inited = true; } else { fs += (s1 - fs) * 0.18; fc += (c1 - fc) * 0.18; }
        long now = System.currentTimeMillis();
        if (now - last < 50) return;
        last = now;
        double hd = ((Math.toDegrees(Math.atan2(fs, fc)) + decl) % 360 + 360) % 360;
        JSObject o = new JSObject();
        o.put("h", hd); o.put("flat", flatState); o.put("acc", acc); o.put("src", src); o.put("decl", decl);
        if (ev.values.length > 4 && ev.values[4] >= 0) o.put("accDeg", Math.toDegrees(ev.values[4]));
        notifyListeners("heading", o);
    }

    @Override
    public void onAccuracyChanged(Sensor s, int a) { acc = a; }
}
