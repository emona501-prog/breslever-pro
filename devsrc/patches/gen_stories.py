# ליקוט "סיפורים שונים מכלל ספרי ברסלב" – לשונית חדשה בתוך סיפורי מעשיות (V2), כהפניות (irefs) לקטעים המקוריים, מילה במילה
import json,re,hashlib,os,collections,glob
W='/home/claude/breslever-pro/www/'; SH='/home/claude/src/shell.html'
s=open(SH,encoding='utf-8').read()
urls=json.loads(re.search(r'window\.BOOK_DATA_URLS=(\[.*?\])',s).group(1))
cfg=json.loads(re.search(r'<script type="application/json" id="bookcfg">(.*?)</script>',s,re.S).group(1))
V={};allb=[]
for u in urls:
    vi=int(re.search(r'_V(\d+)\.',u).group(1)); d=json.load(open(W+u,encoding='utf-8'))
    for sc in d:
        for ch in sc.get('c',[]):
            for it in ch.get('i',[]):
                b=it.get('b')
                if isinstance(b,dict) and '@' in b: it['b']=allb[b['@']]
                else: allb.append(b)
    V[vi]=d
nq=lambda t: re.sub('[֑-ׇ]','',t or '')
txt=lambda b: re.sub(r'<[^>]+>','',' '.join(x[1] for x in (b or []) if isinstance(x,list) and len(x)>1 and isinstance(x[1],str) and x[0] in ('p','h','b')))
E=r'(?=[\s,.:;])'
OPEN=[('maase',r'(^|[\s(])ו?(מעשה|מעשה היה|והיה מעשה|היה מעשה) ?(ב|ש|מ|היה|באחד|באיש|בצדיק|בחסיד)(?!ראשית|רכבה|מצו)'),
 ('paam',r'(^\W*(פעם|ופעם)(?! אחת)|(^|[\s(])(פעם אחת|פעםאחת|פעם-אחת|פעם א[\'׳]|פ"א)) (?!אמר|דבר|שאל|אמרו|הזהיר|צוה|הקפיד|השיב|ענה|גער|שח|שמעתי שאמר|כשדבר|כשאמר|התלוצץ|הוכיח)'),
 ('siper',r'(^|[\s(])ו?ש?(ספר|סיפר|ספרו|סיפרו|מספרים|מספר) (?!הרבה)(לי|לנו|רבנו|מוהרנ|אדמו|ר[\'׳]|רבי|הרב|הרה|אחד|אבי|זקני|לפני|בשם|ש)'),
 ('shamati',r'(^|[\s(])ו?שמעתי (מ|מפי )\S+ (ש|ספר|סיפר|שספר|שסיפר)'),
 ('mashal',r'(^|[\s(])(משל|והמשל|ומשל)'+E),
 ('chalom',r'(^|[\s(])(חלם|חלמתי|חלמו|בחלום|בחלומו|בחלומי|החלום|חלום)'+E),
 ('haya',r'^\W*ו?(היה איש|היה מלך|היה פעם|פעם היה|היה עשיר|היה עני|היה צדיק|היה אדם|היה חסיד|היה בעל)'+E)]
OPEN=[(k,re.compile(r)) for k,r in OPEN]
WHOLE={(5,'ספורים נפלאים'),(9,'ספורים חדשים'),(10,'סדר הנסיעה שלו לארץ ישראל')}
ORDER=[0,8,9,10,24,5,16,44,48,110,113,18,19]
secs_out=[];stat=collections.Counter()
for v in ORDER:
    bt=nq(cfg['books'][v]['title']).replace('״','"')
    groups=collections.OrderedDict()
    for sc in V[v]:
        sn=nq(sc['short']); whole=any(v==a and b in sn for a,b in WHOLE)
        if 'הקדמ' in sn: continue
        cs=[c for c in sc['c'] if c.get('i')]
        for ci,c in enumerate(sc['c']):
            for ii,it in enumerate(c.get('i',[])):
                t=nq(txt(it.get('b'))).strip()
                if len(t)<100 or len(t)>9000 or t.startswith('חסר'): continue
                ok=whole
                if not ok:
                    for k,r in OPEN:
                        if r.search(t[:(90 if k in ('maase','chalom','mashal') else 60)]): ok=k; break
                if not ok: continue
                ct=nq(c.get('t','')).strip()
                n=nq(str(it.get('n') or '')).strip()
                lbl=bt+(' · '+n if v==110 and n else ' · '+ct+((' ('+n+')') if n and len(c['i'])>1 else ''))
                key=sn if (v in (110,48) or any(w in sn for w in ('ספורים חדשים','ספורים נפלאים','אבני"ה ברזל'))) else ''
                groups.setdefault(key,[]).append([sc['id'],ci,ii,'%s.%d.%d'%(sc['id'],ci,ii),lbl])
                stat[v]+=1
    for key,refs in groups.items():
        title=bt+(' · '+key if key and len(groups)>1 else (' · שאר הסיפורים' if len(groups)>1 else ''))
        secs_out.append({'t':title,'i':[],'irefs':refs})
f=[u for u in urls if '_V2.' in u][0]
d=json.load(open(W+f,encoding='utf-8'))
d=[x for x in d if x['id']!='v2g5']
d.append({'id':'v2g5','short':'סִפּוּרִים שׁוֹנִים מִכְּלַל סִפְרֵי בְּרֶסְלֶב','g':'V2','c':secs_out})
js=json.dumps(d,ensure_ascii=False,separators=(',',':'))
fn='b02_V2.%s.json'%hashlib.md5(js.encode()).hexdigest()[:10]
open('/home/claude/content/out8/'+fn,'w',encoding='utf-8').write(js)
print('chapters',len(secs_out),'stories',sum(stat.values()),{cfg['books'][k]['title']:n for k,n in stat.items()},fn)
print([ (c['t'],len(c['irefs'])) for c in secs_out])
