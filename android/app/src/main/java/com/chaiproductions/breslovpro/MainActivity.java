package com.chaiproductions.breslovpro;

import android.content.Intent;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.webkit.WebView;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import com.getcapacitor.BridgeActivity;
import java.util.Locale;

public class MainActivity extends BridgeActivity {
    // שולי בטיחות (שורת השעון למעלה, פס הניווט למטה) – מועברים לאפליקציה כמשתני CSS: --sat / --sab
    private int insetTop = 0, insetBottom = 0;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        registerPlugin(WebPrintPlugin.class);
        registerPlugin(WidgetBridgePlugin.class);
        registerPlugin(CompassPlugin.class);
        super.onCreate(savedInstanceState);

        // מסך מלא "קצה לקצה": האפליקציה נמשכת מתחת לשעון ולפס הניווט, בדיוק כמו באתר המותקן
        Window w = getWindow();
        WindowCompat.setDecorFitsSystemWindows(w, false);
        w.setStatusBarColor(Color.TRANSPARENT);
        w.setNavigationBarColor(Color.TRANSPARENT);
        if (Build.VERSION.SDK_INT >= 29) {
            w.setStatusBarContrastEnforced(false);
            w.setNavigationBarContrastEnforced(false);
        }
        WindowInsetsControllerCompat c = WindowCompat.getInsetsController(w, w.getDecorView());
        c.setAppearanceLightStatusBars(true);
        c.setAppearanceLightNavigationBars(true);

        View root = w.getDecorView();
        root.setBackgroundColor(Color.parseColor("#FBF7EE"));
        ViewCompat.setOnApplyWindowInsetsListener(root, (v, insets) -> {
            Insets s = insets.getInsets(WindowInsetsCompat.Type.systemBars() | WindowInsetsCompat.Type.displayCutout());
            Insets ime = insets.getInsets(WindowInsetsCompat.Type.ime());
            boolean kb = insets.isVisible(WindowInsetsCompat.Type.ime());
            // שורת השעון ופס הניווט מקבלים פס משלהם – האפליקציה מתחילה מתחתיהם ולא מתערבבת איתם
            v.setPadding(s.left, s.top, s.right, kb ? Math.max(ime.bottom, s.bottom) : s.bottom);
            insetTop = 0;
            insetBottom = 0;
            pushInsets();
            return WindowInsetsCompat.CONSUMED;
        });
        // אחרי טעינת הדף – לשלוח שוב (הדף עשוי להיטען אחרי החישוב הראשון)
        for (int ms : new int[] { 600, 1500, 3000, 6000 }) root.postDelayed(this::pushInsets, ms);
        takeWidgetAction(getIntent());
    }

    // לחיצה בווידג'ט / בקיצור דרך: מעבירים לאפליקציה את הפעולה (פתיחה אקראית, המשך לימוד, מצפן...)
    private String pendingAct = null;
    private int actTries = 0;

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        takeWidgetAction(intent);
    }

    private void takeWidgetAction(Intent intent) {
        if (intent == null) return;
        String a = intent.getStringExtra("wact");
        String ac = intent.getAction();
        if (a == null && ac != null && ac.startsWith("bp.w.")) a = ac.substring(5);
        if (a == null || a.isEmpty() || !a.matches("[a-z:0-9]+")) return;
        intent.removeExtra("wact");
        if (ac != null && ac.startsWith("bp.w.")) intent.setAction(Intent.ACTION_MAIN);
        pendingAct = a; actTries = 0;
        getWindow().getDecorView().postDelayed(this::deliverAct, 400);
    }

    private void deliverAct() {
        if (pendingAct == null) return;
        try {
            WebView wv = getBridge() != null ? getBridge().getWebView() : null;
            if (wv == null) { retryAct(); return; }
            final String a = pendingAct;
            wv.evaluateJavascript("(function(){try{return window.__wAct?window.__wAct('" + a + "'):'no'}catch(e){return 'no'}})()", v -> {
                if (v != null && v.contains("ok")) pendingAct = null; else retryAct();
            });
        } catch (Exception e) { retryAct(); }
    }

    private void retryAct() { if (++actTries < 25) getWindow().getDecorView().postDelayed(this::deliverAct, 600); else pendingAct = null; }

    private void pushInsets() {
        try {
            if (getBridge() == null) return;
            WebView wv = getBridge().getWebView();
            if (wv == null) return;
            String js = String.format(Locale.US,
                "try{var r=document.documentElement.style;r.setProperty('--sat','%dpx');r.setProperty('--sab','%dpx');}catch(e){}",
                insetTop, insetBottom);
            wv.post(() -> wv.evaluateJavascript(js, null));
        } catch (Exception e) { }
    }
}
