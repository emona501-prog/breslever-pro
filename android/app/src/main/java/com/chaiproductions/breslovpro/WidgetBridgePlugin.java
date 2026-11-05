package com.chaiproductions.breslovpro;

import android.content.Context;
import android.content.SharedPreferences;

import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

/** גשר לווידג'ט: האפליקציה שולחת לכאן את נתוני היום (JSON), והווידג'ט במסך הבית מציג אותם */
@CapacitorPlugin(name = "WidgetBridge")
public class WidgetBridgePlugin extends Plugin {
    @PluginMethod
    public void update(PluginCall call) {
        String data = call.getString("data", "");
        Context ctx = getContext();
        SharedPreferences sp = ctx.getSharedPreferences(BpWidget.PREFS, Context.MODE_PRIVATE);
        sp.edit().putString("data", data).putLong("ts", System.currentTimeMillis()).apply();
        try { BpWidget.updateAll(ctx); } catch (Exception e) { }
        call.resolve();
    }
}
