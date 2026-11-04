package com.chaiproductions.breslovpro;

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
    }

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
