package com.chaiproductions.breslovpro;

import android.appwidget.AppWidgetManager;
import android.content.ComponentName;
import android.content.Context;
import android.os.Build;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.util.Base64;
import androidx.core.content.pm.ShortcutInfoCompat;
import androidx.core.content.pm.ShortcutManagerCompat;
import androidx.core.graphics.drawable.IconCompat;

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

    /** 🪜 "הסולם שלי" (חסימה חכמה): שולחים לסולם את היעדים ומה סומן. אם הסולם לא מותקן – לא קורה כלום. */
    @PluginMethod
    public void sulam(PluginCall call) {
        String data = call.getString("data", "");
        Context ctx = getContext();
        try {
            Intent i = new Intent("com.chaiapps.chasima.BP_SYNC");
            i.setComponent(new ComponentName("com.chaiapps.chasima", "com.chaiapps.chasima.BpSync"));
            i.putExtra("d", data);
            i.putExtra("pkg", ctx.getPackageName());
            i.addFlags(Intent.FLAG_INCLUDE_STOPPED_PACKAGES);
            ctx.sendBroadcast(i);
        } catch (Exception e) { }
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

    /** 📲 קיצור דרך במסך הבית: אייקון שפותח ישר מקום מסוים באפליקציה (הטלפון מציג חלון אישור) */
    @PluginMethod
    public void pinShortcut(PluginCall call) {
        Context ctx = getContext(); JSObject r = new JSObject();
        boolean ok = false;
        try {
            String id = call.getString("id", "sc"), label = call.getString("label", "ברסלב PRO"), act = call.getString("act", ""), icon = call.getString("icon", "");
            if (act.matches("[a-z:0-9]+") && ShortcutManagerCompat.isRequestPinShortcutSupported(ctx)) {
                Intent it = new Intent(ctx, MainActivity.class);
                it.setAction("bp.w." + act);
                it.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);
                IconCompat ic = null;
                if (icon != null && !icon.isEmpty()) {
                    byte[] b = Base64.decode(icon, Base64.DEFAULT);
                    Bitmap bm = BitmapFactory.decodeByteArray(b, 0, b.length);
                    if (bm != null) ic = IconCompat.createWithBitmap(bm);
                }
                if (ic == null) ic = IconCompat.createWithResource(ctx, R.mipmap.ic_launcher);
                ShortcutInfoCompat si = new ShortcutInfoCompat.Builder(ctx, id).setShortLabel(label).setLongLabel(label).setIcon(ic).setIntent(it).build();
                ok = ShortcutManagerCompat.requestPinShortcut(ctx, si, null);
            }
        } catch (Exception e) { ok = false; }
        r.put("ok", ok);
        call.resolve(r);
    }
}
