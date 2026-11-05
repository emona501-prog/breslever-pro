package com.chaiproductions.breslovpro;

import android.appwidget.AppWidgetManager;
import android.content.ComponentName;
import android.content.Context;
import android.os.Build;

import com.getcapacitor.JSObject;
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

    /** כמה ווידג'טים כבר במסך הבית, והאם אפשר לבקש הוספה ישירה */
    @PluginMethod
    public void info(PluginCall call) {
        Context ctx = getContext(); JSObject r = new JSObject();
        AppWidgetManager mgr = AppWidgetManager.getInstance(ctx);
        r.put("count", mgr.getAppWidgetIds(new ComponentName(ctx, BpWidget.class)).length);
        r.put("canPin", Build.VERSION.SDK_INT >= 26 && mgr.isRequestPinAppWidgetSupported());
        call.resolve(r);
    }

    /** הוספה ישירה של הווידג'ט למסך הבית (הטלפון מציג חלון אישור) */
    @PluginMethod
    public void pin(PluginCall call) {
        Context ctx = getContext(); JSObject r = new JSObject();
        boolean ok = false;
        try {
            AppWidgetManager mgr = AppWidgetManager.getInstance(ctx);
            if (Build.VERSION.SDK_INT >= 26 && mgr.isRequestPinAppWidgetSupported()) ok = mgr.requestPinAppWidget(new ComponentName(ctx, BpWidget.class), null, null);
        } catch (Exception e) { ok = false; }
        r.put("ok", ok);
        call.resolve(r);
    }
}
