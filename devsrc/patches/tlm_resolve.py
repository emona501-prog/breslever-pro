# איתור הפסוק המדויק לערכים שרשומים רק לפי פרק: התאמה גמישה (כתיב מלא/חסר, הבדל של אות) מול התנ"ך שבאפליקציה
import json,re,collections,glob
NQ=re.compile(r'[֑-ׇ]')
D=json.load(open('/home/claude/kb/env.json'))
GV=dict(zip('אבגדהוזחטיכלמנסעפצקרשת',[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400])); GV.update({'ך':20,'ם':40,'ן':50,'ף':80,'ץ':90})
def gm(t):
    t=re.sub(r'["\'׳״\s]','',NQ.sub('',t or ''))
    return sum(GV[c] for c in t) if t and all(c in GV for c in t) else 0
FIN=str.maketrans('ךםןףץ','כמנפצ')
def words(t):
    t=NQ.sub('',t).replace('־',' ')
    t=re.sub(r"ה'",'ה',t)
    t=re.sub(r'[^א-ת ]',' ',t)
    out=[]
    for w in t.split():
        w=w.translate(FIN)
        if w in('יהוה','הויה','יי','השמ'): w='ה'
        w=re.sub(r'^([והבלמשכ]?)אל[הק](ימ|י|יכ|יו|ינו|יכמ)$',r'\1אלה\2',w)
        out.append(w[0]+re.sub('[וי]','',w[1:]))
    return out
def lev1(a,b):
    if a==b: return True
    if abs(len(a)-len(b))>1 or min(len(a),len(b))<2: return False
    if len(a)==len(b): return sum(x!=y for x,y in zip(a,b))==1
    if len(a)<len(b): a,b=b,a
    return any(a[:i]+a[i+1:]==b for i in range(len(a)))
def run(q,v):
    """הרצף הארוך ביותר של מילים עוקבות מ-q שמופיע ב-v (מילה = שווה או הבדל של אות אחת); מחזיר (אורך, כמה מדויקות)"""
    best=(0,0)
    for i in range(len(q)):
        for j in range(len(v)):
            k=0;ex=0
            while i+k<len(q) and j+k<len(v) and lev1(q[i+k],v[j+k]):
                ex+=q[i+k]==v[j+k]; k+=1
            if (k,ex)>best: best=(k,ex)
    return best
B=D['books']; bmap={}
BOOKS=['בראשית','שמות','ויקרא','במדבר','דברים','יהושע','שופטים','שמואל א','שמואל ב','מלכים א','מלכים ב','ישעיה','ירמיה','יחזקאל','הושע','יואל','עמוס','עובדיה','יונה','מיכה','נחום','חבקוק','צפניה','חגי','זכריה','מלאכי','תהלים','משלי','איוב','שיר השירים','רות','איכה','קהלת','אסתר','דניאל','עזרא','נחמיה','דברי הימים א','דברי הימים ב']
for i,b in enumerate(B):
    if not b: continue
    t=NQ.sub('',b.get('title','')).split(' · ')[0].replace(' עם מפרשים','').strip()
    if b.get('cat')=='tanach' and t in BOOKS and t not in bmap.values(): bmap[i]=t
pass
TV=collections.defaultdict(lambda:collections.defaultdict(list))
for i,v in enumerate(D['vi']):
    if v in bmap:
        mm=re.match(r'\s*(?:פרק|מזמור)\s+([א-ת"\'׳״]+)',D['ch'][i]); ch=gm(mm.group(1)) if mm else 0
        if not ch: continue
        m2=re.match(r'^v\d+g\d+\.\d+\.(\d+)$',D['id'][i])
        TV[bmap[v]][ch].append(words(D['T'][i]))
def resolve(bk,ch,quote,snip):
    """מחזיר (פסוק, שיטה) או (0,'')"""
    if bk not in TV or ch not in TV[bk]: return 0,'nobook'
    V=TV[bk][ch]
    def best(q,need):
        sc=[(run(q,v),n+1) for n,v in enumerate(V)]
        sc.sort(reverse=True)
        if not sc or sc[0][0][0]<need: return 0
        if len(sc)>1 and sc[1][0]==sc[0][0]: 
            # תיקו: אם זה אותו ביטוי בכמה פסוקים – לוקחים את הראשון רק כשההתאמה מלאה
            return 0
        return sc[0][1]
    q=words(quote) if quote else []
    if q:
        need=len(q) if len(q)<=2 else max(2,int(len(q)*0.6+0.5))
        if len(q)==1 and len(q[0])<4: need=99
        r=best(q,need)
        if r: return r,'quote'
    s=words(snip) if snip else []
    if s:
        sc=[(run(v,s),n+1) for n,v in enumerate(V)]; sc.sort(reverse=True)
        if sc and sc[0][0][0]>=3 and (len(sc)==1 or sc[1][0][0]<sc[0][0][0]): return sc[0][1],'snip'
    return 0,''
def resolve_book(bk,quote):
    """הפרק שצוין שגוי: מחפשים את הלשון בכל הספר – רק התאמה מלאה ויחידה של 3 מילים ומעלה. מחזיר (פרק,פסוק)"""
    q=words(quote) if quote else []
    if bk not in TV or len(q)<3: return 0,0
    hit=[]
    for ch,V in TV[bk].items():
        for n,v in enumerate(V):
            if run(q,v)[0]>=len(q): hit.append((ch,n+1))
            if len(hit)>1: return 0,0
    return hit[0] if len(hit)==1 else (0,0)
