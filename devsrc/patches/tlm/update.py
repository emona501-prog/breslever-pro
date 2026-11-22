# מריץ מחדש את קישור הפסוקים (ליקוטי מוהר"ן + ליקוטי הלכות) ומעדכן את שמות הקבצים באפליקציה
import subprocess,re,os
D='/home/claude/breslever-pro/www/data'
for a in ('lm','lh'): subprocess.run(['python3','/home/claude/content/tlm/gen.py',a],check=True)
p='/home/claude/src/app.js'; s=open(p,encoding='utf-8').read()
for f in os.listdir(D):
    if re.match(r'tl[mh]\.[0-9a-f]+\.json$',f): s=re.sub(r'"'+f[:3]+r'\.[0-9a-f]+\.json"','"'+f+'"',s)
open(p,'w',encoding='utf-8').write(s); print('tlm/tlh updated in app.js')
