package com.chaiproductions.breslovpro;

import android.content.Context;
import android.content.Intent;
import android.location.LocationManager;
import android.os.Build;
import android.provider.Settings;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import com.google.android.gms.common.api.ResolvableApiException;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.location.LocationSettingsRequest;
import com.google.android.gms.location.Priority;

/** הפעלת מיקום (GPS): אם המיקום כבוי – מציג את חלון "להפעיל מיקום?" של הטלפון, או פותח את הגדרות המיקום */
@CapacitorPlugin(name = "LocationOn")
public class LocationOnPlugin extends Plugin {
    private boolean isOn() {
        try {
            LocationManager lm = (LocationManager) getContext().getSystemService(Context.LOCATION_SERVICE);
            if (lm == null) return false;
            if (Build.VERSION.SDK_INT >= 28) return lm.isLocationEnabled();
            return lm.isProviderEnabled(LocationManager.GPS_PROVIDER) || lm.isProviderEnabled(LocationManager.NETWORK_PROVIDER);
        } catch (Exception e) { return false; }
    }

    private void openSettings() {
        try { Intent i = new Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS); i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK); getContext().startActivity(i); } catch (Exception e) { }
    }

    @PluginMethod
    public void status(PluginCall call) { JSObject r = new JSObject(); r.put("on", isOn()); call.resolve(r); }

    @PluginMethod
    public void ensure(PluginCall call) {
        if (isOn()) { JSObject r = new JSObject(); r.put("on", true); call.resolve(r); return; }
        try {
            LocationRequest req = new LocationRequest.Builder(Priority.PRIORITY_HIGH_ACCURACY, 10000).build();
            LocationSettingsRequest s = new LocationSettingsRequest.Builder().addLocationRequest(req).setAlwaysShow(true).build();
            LocationServices.getSettingsClient(getActivity()).checkLocationSettings(s)
                .addOnSuccessListener(x -> { JSObject r = new JSObject(); r.put("on", true); call.resolve(r); })
                .addOnFailureListener(e -> {
                    JSObject r = new JSObject(); r.put("on", false);
                    if (e instanceof ResolvableApiException) {
                        try { ((ResolvableApiException) e).startResolutionForResult(getActivity(), 4711); r.put("asked", true); }
                        catch (Exception x) { openSettings(); r.put("settings", true); }
                    } else { openSettings(); r.put("settings", true); }
                    call.resolve(r);
                });
        } catch (Exception e) { openSettings(); JSObject r = new JSObject(); r.put("on", false); r.put("settings", true); call.resolve(r); }
    }
}
