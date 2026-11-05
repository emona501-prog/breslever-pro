package com.chaiproductions.breslovpro;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.provider.Settings;

import androidx.core.content.FileProvider;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

/** עדכון מתוך האפליקציה: הורדה לתיקייה הפרטית של האפליקציה (עם התקדמות), פתיחת ההתקנה, ומחיקת קבצי עדכון ישנים */
@CapacitorPlugin(name = "Updater")
public class UpdaterPlugin extends Plugin {
    private File dir() { File d = new File(getContext().getCacheDir(), "updates"); if (!d.exists()) d.mkdirs(); return d; }

    /** מחיקת כל קבצי העדכון שכבר לא צריך */
    @PluginMethod
    public void cleanup(PluginCall call) {
        int n = 0; long bytes = 0;
        try { File[] fs = dir().listFiles(); if (fs != null) for (File f : fs) { bytes += f.length(); if (f.delete()) n++; } } catch (Exception e) { }
        JSObject r = new JSObject(); r.put("deleted", n); r.put("bytes", bytes); call.resolve(r);
    }

    @PluginMethod
    public void download(PluginCall call) {
        final String url = call.getString("url", "");
        final String ver = call.getString("version", "new").replaceAll("[^0-9a-zA-Z._-]", "");
        if (url.isEmpty()) { call.reject("no url"); return; }
        new Thread(() -> {
            HttpURLConnection c = null;
            try {
                try { File[] fs = dir().listFiles(); if (fs != null) for (File f : fs) f.delete(); } catch (Exception e) { }
                File out = new File(dir(), "breslever-pro-" + ver + ".apk");
                URL u = new URL(url); int hops = 0;
                while (true) {
                    c = (HttpURLConnection) u.openConnection(); c.setInstanceFollowRedirects(false); c.setConnectTimeout(20000); c.setReadTimeout(30000);
                    int code = c.getResponseCode();
                    if (code >= 300 && code < 400 && hops++ < 6) { String loc = c.getHeaderField("Location"); c.disconnect(); u = new URL(u, loc); continue; }
                    if (code != 200) throw new Exception("http " + code);
                    break;
                }
                long total = c.getContentLengthLong(), done = 0; int lastPct = -1;
                try (InputStream in = c.getInputStream(); FileOutputStream fo = new FileOutputStream(out)) {
                    byte[] buf = new byte[65536]; int k;
                    while ((k = in.read(buf)) > 0) { fo.write(buf, 0, k); done += k;
                        int pct = total > 0 ? (int) (done * 100 / total) : -1;
                        if (pct != lastPct) { lastPct = pct; JSObject p = new JSObject(); p.put("pct", pct); p.put("done", done); p.put("total", total); notifyListeners("progress", p); } }
                }
                JSObject r = new JSObject(); r.put("path", out.getAbsolutePath()); r.put("size", out.length()); call.resolve(r);
            } catch (Exception e) { call.reject("download failed: " + e.getMessage()); }
            finally { if (c != null) try { c.disconnect(); } catch (Exception e) { } }
        }).start();
    }

    @PluginMethod
    public void install(PluginCall call) {
        try {
            Context ctx = getContext();
            if (Build.VERSION.SDK_INT >= 26 && !ctx.getPackageManager().canRequestPackageInstalls()) {
                Intent s = new Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES, Uri.parse("package:" + ctx.getPackageName()));
                s.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK); ctx.startActivity(s);
                JSObject r = new JSObject(); r.put("needPermission", true); call.resolve(r); return;
            }
            File f = new File(call.getString("path", ""));
            if (!f.exists()) { call.reject("file missing"); return; }
            Uri uri = FileProvider.getUriForFile(ctx, ctx.getPackageName() + ".fileprovider", f);
            Intent i = new Intent(Intent.ACTION_VIEW);
            i.setDataAndType(uri, "application/vnd.android.package-archive");
            i.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_ACTIVITY_NEW_TASK);
            ctx.startActivity(i);
            JSObject r = new JSObject(); r.put("ok", true); call.resolve(r);
        } catch (Exception e) { call.reject("install failed: " + e.getMessage()); }
    }
}
