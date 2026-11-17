#!/usr/bin/env python3
# 💎 מלקט "דיבורים יפים קצרים" מתוך ספרי רבנו ותלמידיו – משפטים שלמים ועומדים בפני עצמם (לא אמצע מהלך).
# הטקסט נשאר מילה במילה כמו בספר; נשמר גם המקור (מזהה הקטע) כדי לפתוח אותו.
import json, glob, re, os, sys, hashlib
W = '/home/claude/breslever-pro/www'
shell = open('/home/claude/src/shell.html', encoding='utf-8').read()
cfg = json.loads(re.search(r'<script[^>]*id="bookcfg"[^>]*>(.*?)</script>', shell, re.S).group(1))
vols = None
def walk(o):
    global vols
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, list) and v and isinstance(v[0], dict) and 'title' in v[0] and 'cat' in v[0]: vols = v
            else: walk(v)
walk(cfg)
CATS = {'rn', 'rnt', 'anash', 'tcherin'}
NIQ = re.compile(r'[֑-ׇ]')
TAG = re.compile(r'<[^>]+>')
plain = lambda s: NIQ.sub('', s)
# פתיחות שמעידות על "אמצע מהלך"
BAD_START = re.compile(r'^(?:ו?(?:זהו|זה|זאת|זהו ש|וזה|כי|נמצא|ועל כן|על כן|לכן|ולכן|וכן|כן|כמו כן|ונמצא|והנה|הנה|ואז|אז|ע"כ|ועי"ז|ועל ידי זה|ובזה|בזה|כנ"ל|הנ"ל|ע"ש|שם|ואם|אבל|אך|רק|ואף|אף|גם|וגם|וכשה|ומשם|משם|ושם|ואחר|אחר כך|ואח"כ|וכו|שזהו|שזה|היינו|הינו|דהיינו|דהינו|ולהפך|להפך|ועלידי|עלידי|ועל-ידי|על-ידי|מכל שכן|ומכל שכן|כל שכן|ובפרט|בפרט|ועוד|עוד|ואדרבא|אדרבא|ובאמת|בחינת|וזה בחינת|שהוא|שהם|והוא|והם|וזה שאמר|וזהו שאמר|כמו שכתוב|כמ"ש|כמש"כ|וכמו|כמו|ומה|מה ש|ואיך|ואין|וכל|ובכל|ובשביל|בשביל זה|ומחמת|מחמת|וע"י|ע"י)\b)')
BAD_ANY = re.compile(r'כמו שאומרים|כמו שאמר|שאומרים:|וכמו ש|כמו שמובא|כמובן|כמבאר|כאמור|כמובא|כמו שכתוב|וכמו שכתוב|שנאמר|כמו שאמרו|שאמרו רז"ל|כתוב:|שאמר:|^\'|כנ"ל|הנ"ל|לעיל|להלן|כמבואר|וכו|וגו|ע"ש|עיין|\(|\)|\[|\]|בחינת|כמ"ש|כמש"כ|הוא בחינ|זהו בחינ|ודו"ק|כנזכר|הנזכר|שם\s*$|"[^"]{0,2}$')
GOOD = [
    (r'מצו[הה] גדולה', 6), (r'העיקר', 4), (r'אין שום יאוש|אל תתיאש|אסור להתיאש|אין יאוש|אסור להיות זקן', 8), (r'שמחה|בשמחה|לשמוח', 4),
    (r'תמיד', 2), (r'אמונה|להאמין', 3), (r'תפלה|להתפלל|התבודדות|מתבודד', 3), (r'תשובה', 2), (r'בטחון|לבטוח', 3),
    (r'רצון|רצונות|כסופין|כוסף', 3), (r'חזק|להתחזק|התחזקות', 3), (r'כל אחד|כל אדם|האדם', 1), (r'עולם', 1),
    (r'השם יתברך|ה\' יתברך|השי"ת|הקב"ה', 1), (r'ישועה|ישועות|גאולה', 2), (r'נקודה טובה|נקודות טובות|אזמרה', 5), (r'צריך', 1),
    (r'אל תפחד|אל ירע|לא לפחד|כלל לא לפחד', 6), (r'גשר צר מאד', 9), (r'טוב מאד|מה טוב|אשרי', 2), (r'אפילו', 1),
]
# סיפור / דיווח (לא דיבור מחזק)
NARR = re.compile(r'(?:^|\s)ו?(?:היה|הייתי|היתה|היו|הייתם|אמר|ואמר|אמרתי|אמרו|שאל|שאלתי|נסע|נסעתי|נסענו|הבאתי|הביא|כתבתי|כתב לי|ראיתי|ראה|בא|באתי|הלך|הלכתי|שמעתי|ספר|ספרתי|עמד|ישב|נכנס|יצא|השיב|ענה|ועתה|ושחק|שחק|הוטב|הודיע|קבלתי|מכתבך|מכתבו|שלומך|שלומכם|בני חביבי|ידידי|אהובי)(?=\s|[,.:])')
MAXIM = re.compile(r'צריך|צריכין|צריכים|העקר|העיקר|אין שום|אל ת|אל י|אסור|מצוה|אשרי|כל אחד|כל אדם|האדם|ודע|דע ש|תמיד|אי אפשר|עלידי|על ידי|זוכין|זוכים|יזכה|תחזק|להתחזק|להיות בשמחה|אין יאוש|העולם|לעולם|שאין|כי אין')
def sentences(text):
    t = TAG.sub('', text).replace(' ', ' ')
    t = re.sub(r'\s+', ' ', t).strip()
    # חיתוך אחרי נקודה / נקודתיים / סימן קריאה
    parts = re.split(r'(?<=[.:!?])\s+', t)
    return [p.strip() for p in parts if p.strip()]
out = []
for f in sorted(glob.glob(W + '/data/b*_V*.json')):
    vi = int(re.search(r'_V(\d+)\.', f).group(1))
    if vi >= len(vols) or vols[vi].get('cat') not in CATS or vols[vi].get('hidden'): continue
    if vi in (1, 26): continue
    for sec in json.load(open(f, encoding='utf-8')):
        if sec.get('dup'): continue
        for ci, ch in enumerate(sec.get('c', [])):
            for ii, it in enumerate(ch.get('i', [])):
                txt = ' '.join(b[1] for b in it.get('b', []) if isinstance(b, list) and len(b) > 1 and b[0] == 'p' and isinstance(b[1], str))
                if not txt: continue
                for s in sentences(txt):
                    p = plain(s)
                    L = len(p)
                    if L < 24 or L > 175: continue
                    if BAD_START.match(p) or BAD_ANY.search(p) or NARR.search(p) or not MAXIM.search(p): continue
                    if not re.search(r'[.:!]$', p): continue
                    if p.count(' ') < 4: continue
                    sc = sum(w for r, w in GOOD if re.search(r, p))
                    if sc < 7 or (L < 40 and sc < 8): continue
                    sc += 2 if L < 120 else 0
                    out.append({'t': s, 'id': '%s.%d.%d' % (sec['id'], ci, ii), 'v': vi, 'sc': sc})
# כפילויות (אותו משפט בכמה ספרים)
seen = set(); uniq = []
for o in sorted(out, key=lambda o: -o['sc']):
    k = re.sub(r'\W', '', plain(o['t']))[:60]
    if k in seen: continue
    seen.add(k); uniq.append(o)
# גיוון: עד 120 לכל ספר, סה"כ עד 900
per = {}; sel = []
for o in uniq:
    if per.get(o['v'], 0) >= 120: continue
    per[o['v']] = per.get(o['v'], 0) + 1; sel.append(o)
    if len(sel) >= 900: break
print('candidates', len(out), 'unique', len(uniq), 'selected', len(sel), file=sys.stderr)
data = [[o['t'], o['id']] for o in sel]
js = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
h = hashlib.md5(js.encode()).hexdigest()[:10]
for old in glob.glob(W + '/data/pearls.*.json'): os.remove(old)
open(W + '/data/pearls.%s.json' % h, 'w', encoding='utf-8').write(js)
print('data/pearls.%s.json' % h)
SH = '/home/claude/src/shell.html'
sh = open(SH, encoding='utf-8').read()
fn = 'data/pearls.%s.json' % h
if 'window.BOOK_PEARLS=' in sh: sh = re.sub(r'window\.BOOK_PEARLS="[^"]*";', 'window.BOOK_PEARLS="%s";' % fn, sh)
else: sh = sh.replace('<script>window.BOOK_SKEL=', '<script>window.BOOK_PEARLS="%s";window.BOOK_SKEL=' % fn, 1)
open(SH, 'w', encoding='utf-8').write(sh)
if '--show' in sys.argv:
    import random; random.seed(3)
    for o in random.sample(sel, min(40, len(sel))): print(o['sc'], vols[o['v']]['title'], '|', plain(o['t']), file=sys.stderr)
