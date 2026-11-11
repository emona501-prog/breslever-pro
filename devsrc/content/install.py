# מתקין כרכים חדשים (לפי manifest) לתוך shell.html ו-www/data. אידמפוטנטי.
import re,json,sys,shutil,os
SH='/home/claude/src/shell.html'; WWW='/home/claude/breslever-pro/www/'
s=open(SH,encoding='utf-8').read()
m=re.search(r'(<script type="application/json" id="bookcfg">)(.*?)(</script>)',s,re.S)
c=json.loads(m.group(2))
mu=re.search(r'window\.BOOK_DATA_URLS=(\[.*?\])',s); urls=json.loads(mu.group(1))
def setvol(vi,cfg,fn,src):
    while len(c['groups'])<=vi: c['groups'].append(''); c['books'].append(None)
    c['groups'][vi]=cfg['title']; c['books'][vi]=cfg
    global urls
    urls=[u for u in urls if not re.search(r'_V%d\.'%vi,u)]+['data/'+fn]
    for f in os.listdir(WWW+'data'):
        if re.search(r'_V%d\.'%vi,f) and f!=fn: os.remove(WWW+'data/'+f)
    shutil.copy(src+'/'+fn,WWW+'data/'+fn)
    if isinstance(cfg.get('mg'),str):
        os.makedirs(WWW+'data/mg',exist_ok=True)
        for f in os.listdir(WWW+'data/mg'):
            if f.startswith('V%d.'%vi): os.remove(WWW+'data/mg/'+f)
        shutil.copy(src+'/'+cfg['mg'],WWW+'data/'+cfg['mg'])
for man in sys.argv[1:]:
    src=os.path.dirname(os.path.abspath(man))
    for e in json.load(open(man,encoding='utf-8')): setvol(e['vi'],e['cfg'],e['file'],src)
exec(open('/home/claude/content/cfg_extra.py',encoding='utf-8').read())
# לשמור על סדר טעינה לפי מספר הכרך (ה-@ הגלובלי תלוי בסדר)
urls.sort(key=lambda u:int(re.search(r'_V(\d+)\.',u).group(1)))
s=s[:m.start(2)]+json.dumps(c,ensure_ascii=False)+s[m.end(2):]
mu=re.search(r'window\.BOOK_DATA_URLS=(\[.*?\])',s)
s=s[:mu.start(1)]+json.dumps(urls,ensure_ascii=False,separators=(',',':'))+s[mu.end(1):]
open(SH,'w',encoding='utf-8').write(s); print('installed; vols',len(c['groups']),'urls',len(urls))
