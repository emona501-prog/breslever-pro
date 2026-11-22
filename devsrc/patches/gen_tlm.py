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
P=collections.defaultdict(list); nochap=0
for s in d:
    if not s['id'].startswith(PFX): continue
    for c in s['c']:
        k=c['t'].split(' – ')[0].strip()
        m=re.match(r'^(.+?) ([א-ת"\'׳״]+)(?:, ([א-ת"\'׳״]+))?$',k)
        if not m: print('?',k); continue
        bk,ch,vs=m.group(1),gm(m.group(2)),gm(m.group(3) or '')
        if not vs: nochap+=1; continue
        for r in c.get('irefs',[]):
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
