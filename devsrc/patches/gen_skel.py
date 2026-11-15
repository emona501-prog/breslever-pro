# בונה "שלד" של כל הספרים (מבנה בלי טקסט) – נטען בפתיחה. הטקסט של כל ספר נטען רק כשפותחים אותו.
# הפלט: www/data/skel.<hash>.json + window.BOOK_SKEL ב-shell.html
import json,re,hashlib,os,sys
W='/home/claude/breslever-pro/www/'; SH='/home/claude/src/shell.html'
s=open(SH,encoding='utf-8').read()
urls=json.loads(re.search(r'window\.BOOK_DATA_URLS=(\[.*?\])',s).group(1))
V={};order=[];owner=[];ownerIdx=[];local={}
for u in urls:
    v=int(re.search(r'_V(\d+)\.',u).group(1)); d=json.load(open(W+u,encoding='utf-8'))
    V[v]=d;order.append(v);local[v]=[]
    for sc in d:
        for ch in sc.get('c',[]):
            for it in ch.get('i',[]):
                b=it.get('b')
                if not(isinstance(b,dict) and '@' in b):
                    owner.append(v); ownerIdx.append(len(local[v])); local[v].append(b)
secVol={sc['id']:v for v in order for sc in V[v] if sc.get('id')}
secMap={sc['id']:sc for v in order for sc in V[v] if sc.get('id')}
def resolveB(it):
    b=it.get('b')
    if isinstance(b,dict) and '@' in b: return local[owner[b['@']]][ownerIdx[b['@']]]
    return b
SK={};T=0
for v in order:
    deps=set();secs=[]
    for sc in V[v]:
        s2={k:x for k,x in sc.items() if k!='c'}; s2['c']=[]
        for ch in sc.get('c',[]):
            c2={k:x for k,x in ch.items() if k not in('i','irefs')}
            items=[]
            for it in ch.get('i',[]):
                i2={k:x for k,x in it.items() if k!='b'}
                b=it.get('b')
                rb=resolveB(it) or []
                # מידע מבני שנקרא מתוך הטקסט: סימון עלייה (שניים מקרא) וכותרת הקטע
                for e in rb:
                    if isinstance(e,list) and len(e)>1 and e[0]=='sl': i2['sl']=e[1]; break
                if rb and isinstance(rb[0],list) and len(rb[0])>1 and rb[0][0]=='h': i2['h0']=rb[0][1]
                if isinstance(b,dict) and '@' in b:
                    ov=owner[b['@']]; i2['@']=[ov,ownerIdx[b['@']]]
                    ov!=v and deps.add(ov)
                items.append(i2)
            # הפניות לקטעים בספרים אחרים: נשארים רק אלה שיוצרים קטע (כמו בטעינה הרגילה), כדי שהמספור לא ישתנה
            for ir in ch.get('irefs',[]) or []:
                src=secMap.get(ir[0]); l=src and src['c'][ir[1]] if src and ir[1]<len(src['c']) else None
                a=l and l.get('i') and ir[2]<len(l['i']) and l['i'][ir[2]]
                if not a: continue
                ab=resolveB(a)
                if not ab: continue
                if len(ir)>5 and ir[5] is not None:
                    skip={'tr','am','src','sl','fold','ins','go','tch','img'}
                    txt=' '.join(re.sub(r'<[^>]+>','',e[1]) for e in ab if isinstance(e,list) and len(e)>1 and isinstance(e[1],str) and e[0] not in skip)
                    # JS slice על מחרוזת UTF-16 – בעברית זהה לתווים
                    if not txt[ir[5]:ir[6]].strip(): continue
                items.append({'n':'','ir':ir}); deps.add(secVol[ir[0]])
            for rf in ch.get('refs',[]) or []:
                rf[0] in secVol and deps.add(secVol[rf[0]])
            if 'refs' in ch: c2['refs']=ch['refs']
            c2['i']=items; T+=len(items)
            s2['c'].append(c2)
        secs.append(s2)
    deps.discard(v)
    SK[v]={'u':[u for u in urls if re.search(r'_V%d\.'%v,u)][0],'d':sorted(deps),'s':secs}
out={'order':order,'v':SK}
js=json.dumps(out,ensure_ascii=False,separators=(',',':'))
fn='data/skel.%s.json'%hashlib.md5(js.encode()).hexdigest()[:10]
for f in os.listdir(W+'data'):
    if f.startswith('skel.') and 'data/'+f!=fn: os.remove(W+'data/'+f)
open(W+fn,'w',encoding='utf-8').write(js)
if 'window.BOOK_SKEL=' in s: s=re.sub(r'window\.BOOK_SKEL="[^"]*";','window.BOOK_SKEL="%s";'%fn,s)
else: s=s.replace('<script>window.BOOK_DATA_URLS=','<script>window.BOOK_SKEL="%s";window.BOOK_DATA_URLS='%fn,1)
open(SH,'w',encoding='utf-8').write(s)
print(fn, round(len(js)/1e6,2),'MB items',T)
