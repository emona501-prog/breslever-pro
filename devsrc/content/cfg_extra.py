# שינויי תצורה כלליים (רץ מתוך install.py; c = bookcfg)
c['libSubs']['tanach']=[{"id":"smt","t":"חומש · שניים מקרא ואחד תרגום"},{"id":"mg","t":"חומש · מקראות גדולות"},{"id":"nev","t":"נביאים"},{"id":"ket","t":"כתובים"}]
c['books'][59]['sub']='smt'
if not any(t['id']=='tcherin' for t in c['libTabs']):
    k=[t['id'] for t in c['libTabs']].index('rnt'); c['libTabs'].insert(k+1,{"id":"tcherin","t":"ספרי הרב מטשערין"})
c['books'][18]['cat']='tcherin'

# זוהר
c['libSubs']['zohar']=[{"id":"zohar","t":"ספר הזוהר ותיקונים"},{"id":"zx","t":"חיבורי הזוהר"}]
c['books'][60]['sub']='zohar'
import os as _o, shutil as _s
_f=open('/home/claude/content/out3/v60zh.txt').read().strip()
_o.makedirs(WWW+'data/zh',exist_ok=True)
for _x in _o.listdir(WWW+'data/zh'):
    if _x.startswith('V60.'): _o.remove(WWW+'data/zh/'+_x)
_s.copy('/home/claude/content/out3/'+_f,WWW+'data/'+_f)
c['books'][60]['zh']=_f
c['books'][60]['credit']='התרגום ללשון הקודש: "הזוהר המתורגם" מתוך תוכנת "תורת אמת", רישיון CC BY-NC-SA 2.5 – לשימוש לא מסחרי בלבד.'
# שולחן ערוך
if not any(t['id']=='sa' for t in c['libTabs']):
    k=[t['id'] for t in c['libTabs']].index('zohar'); c['libTabs'].insert(k+1,{"id":"sa","t":"שולחן ערוך"})
