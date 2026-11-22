# אינדקס: פסוק בתנ"ך -> המקומות בליקוטי מוהר"ן שמבארים אותו (מתוך "תנ"ך ליקוטי מוהר"ן" V52)
import json,glob,re,collections,hashlib
DATA='/home/claude/breslever-pro/www/data/'
NQ=re.compile(r'[֑-ׇ]')
GV=dict(zip('אבגדהוזחטיכלמנסעפצקרשת',[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400])); GV.update({'ך':20,'ם':40,'ן':50,'ף':80,'ץ':90})
def gm(t):
    t=re.sub(r'["\'׳״\s]','',NQ.sub('',t or ''))
    return sum(GV[c] for c in t) if t and all(c in GV for c in t) else 0
import sys
V,PFX,OUT=(('52','xtm','tlm') if len(sys.argv)<2 or sys.argv[1]=='lm' else ('53','xth','tlh'))
d=json.load(open(glob.glob(DATA+'b*_V'+V+'.*.json')[0]))
import sys as _s; _s.path.insert(0,'/home/claude/content/tlm')
from resolve import resolve,resolve_book
SRC={}
for f in glob.glob(DATA+('b00_V0.*.json' if V=='52' else 'b*_V4.*.json')):
    for x in json.load(open(f)): SRC[x['id']]=x
SKB={'tr','am','src','sl','fold','ins','go','tch','img'}
def snip(r):
    try:
        it=SRC[r[0]]['c'][r[1]]['i'][r[2]]
        t=' '.join(re.sub('<[^>]+>','',b[1]) for b in it['b'] if isinstance(b,list) and len(b)>1 and isinstance(b[1],str) and b[0] not in SKB)
        return t[r[5]:r[6]]
    except Exception: return ''
ST=collections.Counter(); LEFT=[]
P=collections.defaultdict(list); nochap=0
for s in d:
    if not s['id'].startswith(PFX): continue
    for c in s['c']:
        k=c['t'].split(' – ')[0].strip()
        m=re.match(r'^(.+?) ([א-ת"\'׳״]+)(?:, ([א-ת"\'׳״]+))?$',k)
        if not m: print('?',k); continue
        bk,ch,VS0=m.group(1),gm(m.group(2)),gm(m.group(3) or '')
        CH0=ch
        for r in c.get('irefs',[]):
            vs=VS0; ch=CH0
            if not vs:
                vs,how=resolve(bk,ch,r[7] or '',snip(r)); ST[how or 'none']+=1
                if not vs and how!='nobook':
                    c2,v2=resolve_book(bk,r[7] or '')
                    if v2: ch,vs=c2,v2; ST['book']+=1
                if not vs:
                    nochap+=1
                    if how!='nobook': LEFT.append((k,r[4],r[7]))
                    continue
            lab=r[4].replace('ליקוטי מוהר״ן · ','').replace('ליקוטי הלכות · ','')
            lab=re.sub(r'^חלק א׳ · ','ח״א · ',lab); lab=re.sub(r'^חלק ב׳ · ','ח״ב · ',lab)
            e=[r[3],lab,(r[7] or '')[:60]]
            key=bk+'|'+str(ch)+'|'+str(vs)
            if e not in P[key]: P[key].append(e)
LB=[];LI={}
P2={}
for k,v in P.items():
    P2[k]=[]
    for e in v:
        if e[1] not in LI: LI[e[1]]=len(LB); LB.append(e[1])
        P2[k].append([e[0],LI[e[1]],e[2]])
out={'v':1,'l':LB,'p':P2}
js=json.dumps(out,ensure_ascii=False,separators=(',',':'))
h=hashlib.md5(js.encode()).hexdigest()[:10]
for f in glob.glob(DATA+OUT+'.*.json'):
    import os; os.remove(f)
open(DATA+OUT+'.'+h+'.json','w').write(js)
print('pesukim',len(P),'refs',sum(len(v) for v in P.values()),'chapter-only',nochap,'bytes',len(js.encode()),'file',OUT+'.'+h+'.json')

print(dict(ST)); json.dump(LEFT,open('/home/claude/content/tlm/left_'+OUT+'.json','w'),ensure_ascii=False,indent=0)
