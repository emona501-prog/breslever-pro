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
            if (sensor == null) sensor = sm.getDefaultSensor(Sensor.TYPE_GEOMAGNETIC_ROTATION_VECTOR);
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

    @Override
    public void onSensorChanged(SensorEvent ev) {
        long now = System.currentTimeMillis();
        if (now - last < 40) return;
        last = now;
        SensorManager.getRotationMatrixFromVector(R, ev.values);
        // R[8] = רכיב ה"למעלה" של ציר המסך: קרוב ל־1 כשהטלפון שוכב שטוח
        boolean flat = Math.abs(R[8]) > 0.66f;
        double h;
        if (flat) h = Math.toDegrees(Math.atan2(R[1], R[4]));            // לאן מצביע ראש המסך
        else h = Math.toDegrees(Math.atan2(-R[2], -R[5]));               // לאן פונה גב הטלפון (המצלמה)
        h = ((h + decl) % 360 + 360) % 360;
        JSObject o = new JSObject();
        o.put("h", h); o.put("flat", flat); o.put("acc", acc);
        notifyListeners("heading", o);
    }

    @Override
    public void onAccuracyChanged(Sensor s, int a) { acc = a; }
}
