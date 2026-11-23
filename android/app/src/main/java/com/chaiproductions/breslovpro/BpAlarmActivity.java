package com.chaiproductions.breslovpro;

import android.app.Activity;
import android.app.KeyguardManager;
import android.app.NotificationManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.media.AudioAttributes;
import android.media.MediaPlayer;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.view.Gravity;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

/** מסך "שעון מעורר" של ברסלב PRO */
public class BpAlarmActivity extends Activity {
    private MediaPlayer mp;
    private Vibrator vib;
    private final Handler h = new Handler(Looper.getMainLooper());
    private int id;
    private String title, body, extra;

    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        if (Build.VERSION.SDK_INT >= 27) { setShowWhenLocked(true); setTurnScreenOn(true);
            KeyguardManager km = (KeyguardManager) getSystemService(Context.KEYGUARD_SERVICE); if (km != null) km.requestDismissKeyguard(this, null); }
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON | WindowManager.LayoutParams.FLAG_SHOW_WHEN_LOCKED | WindowManager.LayoutParams.FLAG_TURN_SCREEN_ON);
        Intent in = getIntent();
        id = in.getIntExtra("id", 1); title = in.getStringExtra("title"); body = in.getStringExtra("body"); extra = in.getStringExtra("extra");
        float d = getResources().getDisplayMetrics().density;

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL); root.setGravity(Gravity.CENTER); root.setPadding((int) (28 * d), (int) (40 * d), (int) (28 * d), (int) (40 * d));
        GradientDrawable bg = new GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM, new int[] { Color.parseColor("#020E29"), Color.parseColor("#1B2F5C") });
        root.setBackground(bg);
        TextView ic = new TextView(this); ic.setText("⏰"); ic.setTextSize(72); ic.setGravity(Gravity.CENTER); root.addView(ic);
        TextView t = new TextView(this); t.setText(title == null ? "ברסלב PRO" : title); t.setTextColor(Color.parseColor("#F3D58A")); t.setTextSize(28); t.setTypeface(Typeface.DEFAULT_BOLD); t.setGravity(Gravity.CENTER); t.setPadding(0, (int) (18 * d), 0, (int) (8 * d)); root.addView(t);
        TextView bd = new TextView(this); bd.setText(body == null ? "" : body); bd.setTextColor(Color.WHITE); bd.setTextSize(19); bd.setGravity(Gravity.CENTER); bd.setPadding(0, 0, 0, (int) (36 * d)); root.addView(bd);
        root.addView(btn("📖 פתיחה", "#E8A33D", "#020E29", v -> { stop(); getSharedPreferences(BpAlarmPlugin.PREFS, MODE_PRIVATE).edit().putString("open", extra == null ? "{}" : extra).apply();
            Intent m = new Intent(this, MainActivity.class); m.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_SINGLE_TOP); m.putExtra("bpAlarmOpen", 1); startActivity(m); finish(); }, d));
        root.addView(btn("💤 נודניק – עוד 10 דקות", "#2E4A85", "#FFFFFF", v -> { stop();
            BpAlarmPlugin.setOne(this, 8000 + (id % 1000), System.currentTimeMillis() + 10 * 60000L, title, body, extra); finish(); }, d));
        root.addView(btn("✕ סגירה", "#00000000", "#BFC8DA", v -> { stop(); finish(); }, d));
        setContentView(root);
        start();
        h.postDelayed(() -> { stop(); }, 90000);
    }

    private Button btn(String txt, String bgc, String fg, View.OnClickListener l, float d) {
        Button b = new Button(this); b.setText(txt); b.setAllCaps(false); b.setTextSize(19); b.setTextColor(Color.parseColor(fg));
        GradientDrawable g = new GradientDrawable(); g.setColor(Color.parseColor(bgc)); g.setCornerRadius(18 * d); if (bgc.startsWith("#00")) g.setStroke((int) (1.5 * d), Color.parseColor("#4A5A80"));
        b.setBackground(g); b.setOnClickListener(l);
        LinearLayout.LayoutParams p = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, (int) (60 * d)); p.setMargins(0, (int) (8 * d), 0, (int) (8 * d)); b.setLayoutParams(p);
        return b;
    }

    private void start() {
        try {
            Uri u = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM);
            if (u == null) u = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_RINGTONE);
            mp = new MediaPlayer();
            mp.setAudioAttributes(new AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_ALARM).setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION).build());
            mp.setDataSource(this, u); mp.setLooping(true); mp.prepare(); mp.start();
        } catch (Exception e) { }
        try {
            vib = (Vibrator) getSystemService(Context.VIBRATOR_SERVICE);
            long[] pat = { 0, 900, 500, 900, 500 };
            if (Build.VERSION.SDK_INT >= 26) vib.vibrate(VibrationEffect.createWaveform(pat, 0)); else vib.vibrate(pat, 0);
        } catch (Exception e) { }
    }

    private void stop() {
        try { if (mp != null) { mp.stop(); mp.release(); mp = null; } } catch (Exception e) { }
        try { if (vib != null) vib.cancel(); } catch (Exception e) { }
        try { ((NotificationManager) getSystemService(NOTIFICATION_SERVICE)).cancel(7000 + (id % 1000)); } catch (Exception e) { }
    }

    @Override protected void onDestroy() { stop(); super.onDestroy(); }
    @Override public void onBackPressed() { }
}
