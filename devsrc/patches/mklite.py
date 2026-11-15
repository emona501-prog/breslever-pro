#!/usr/bin/env python3
# 🪶 הופך את www/index.html הרגיל ל"ברסלב PRO לייט" (לנגנים / זיכרון קטן).
# לא משנה את הקוד – רק מסמן window.LITE=1 ומוריד את סרטון הפתיחה (חוסך ~0.7MB בכל פתיחה).
import re, sys
p = sys.argv[1] if len(sys.argv) > 1 else 'www/index.html'
s = open(p, encoding='utf-8').read()
assert '<script>window.LITE=1</script>' not in s, 'already lite'
s = s.replace('<head>', '<head><script>window.LITE=1</script>', 1)
s, n = re.subn(r'<video[^>]*id="spVid"[^>]*>\s*</video>', '', s, count=1, flags=re.S)
s = s.replace('<div id="splash">', '<div id="splash" class="novid">', 1)
s = s.replace('<title>', '<title>לייט · ', 1)
open(p, 'w', encoding='utf-8').write(s)
print('lite ok, video removed:', n, 'size', len(s.encode()))
