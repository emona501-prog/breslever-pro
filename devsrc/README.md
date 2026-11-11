# מקור העבודה של ברסלב PRO

- `app.js` – קוד האפליקציה בצורה קריאה. `shell.html` – המעטפת (HTML, CSS, תצורת הספרים).
- `build.sh` – מקטין את `app.js` ומרכיב את `www/index.html`. (הנתיבים בתוכו מניחים `/home/claude/src` ו-`/home/claude/tools` עם terser.)
- `content/` – סקריפטים שהופכים קובצי Word לכרכי ספרים (`www/data`) ומתקינים אותם בתצורה.
- `tests/` – בדיקות דפדפן (Playwright) מול `www`.

אין לערוך את `www/index.html` ישירות – הוא נבנה מכאן.
