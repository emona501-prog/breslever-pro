import pymupdf,re,json,glob,difflib,html,pickle,collections,unicodedata
from ma2 import page_seq
from bb import to_book,stats,show
D='/home/claude/breslever-pro/www/data/'
# ---------- קורפוס לניקוד: ליקוטי מוהר"ן + ליקוטי תפילות ----------
MARK=lambda c: unicodedata.combining(c)>0
def core(w): return ''.join(c for c in unicodedata.normalize('NFKD',w) if 'א'<=c<='ת')
def corpus():
    W=[];TAG=[]
    for vol,f in ((0,'b00_V0.*.json'),(12,'b12_V12.*.json')):
        d=json.load(open(glob.glob(D+f)[0],encoding='utf-8'))
        for si,s in enumerate(d):
            for ci,c in enumerate(s['c']):
                for it in c.get('i',[]):
                    for b in it['b']:
                        if b[0] not in('p','ins'): continue
                        t=re.sub(r'<[^>]+>',' ',b[1])
                        for w in t.split():
                            k=core(w)
                            if k: W.append((k,w)); TAG.append((vol,si,ci))
    return W,TAG
W,TAG=corpus(); KEYS=[k for k,_ in W]
IDX=collections.defaultdict(list)
for i in range(len(KEYS)-3): IDX[tuple(KEYS[i:i+4])].append(i)
def vocal_core(w):
    # המילה המנוקדת בלי פיסוק מסביב (משאירים מקף/גרש בתוכה)
    m=re.match(r'^[^א-ת]*(.*?)[^א-ת֑-ׇ]*$',w)
    return m.group(1) if m else w
stat=collections.Counter()
def vocalize(tokens,hint):
    """tokens: list of PDF words (no niqud). returns list with niqud where matched"""
    keys=[core(t) for t in tokens]; n=len(keys)
    if n==0: return tokens
    cand=collections.Counter()
    for j in range(max(1,n-3)):
        g=tuple(keys[j:j+4])
        if len(g)<4 or '' in g: continue
        for p in IDX.get(g,[])[:60]: cand[p-j]+=1
    if not cand and n<4:
        # קטע קצר – מחפשים רק בסביבת המיקום האחרון
        if hint is None: stat['short-nohint']+=n; return tokens
        lo=max(0,hint-1500); hi=min(len(KEYS),hint+3000)
        for p in range(lo,hi-n+1):
            if KEYS[p:p+n]==keys: cand[p]=1; break
    if not cand: stat['nomatch']+=n; return tokens
    best=max(cand,key=lambda p:(cand[p],-abs(p-(hint or p))))
    lo=max(0,best-3); hi=min(len(KEYS),best+n+12)
    sm=difflib.SequenceMatcher(None,keys,KEYS[lo:hi],autojunk=False)
    out=list(tokens)
    mt=sum(s for _,_,s in sm.get_matching_blocks())
    if mt<0.75*n: stat['lowratio']+=n; return tokens   # התאמה חלקית מדי – משאירים בלי ניקוד, שלא יהיה חצי מנוקד
    for a,b,size in sm.get_matching_blocks():
        for k in range(size):
            t=tokens[a+k]; v=vocal_core(W[lo+b+k][1])
            m=re.match(r'^([^א-ת]*)(.*?)([^א-ת]*)$',t)
            out[a+k]=m.group(1)+v+m.group(3); stat['ok']+=1
    stat['miss']+=n-sum(s for _,_,s in sm.get_matching_blocks())
    vocalize.last=lo+b+size if sm.get_matching_blocks() else hint
    return out
vocalize.last=None
# ---------- בניית האירועים ----------
esc=lambda t: html.escape(t,quote=False)
def render(runs):
    """runs: [[font,text],...] -> HTML; LM (L) runs vocalized + bold"""
    out=[]; i=0
    # איחוד רצפים: H שאחריו L נחשב חלק מהלשון של רבנו
    seq=[]
    for k,(f,t) in enumerate(runs):
        if f=='H' and any(ff=='L' for ff,_ in runs[k+1:k+2]): f='L'
        if f=='f' and seq and seq[-1][0]=='L' and any(ff=='L' for ff,_ in runs[k+1:k+3]): f='Lf'
        seq.append([f,t])
    # קבוצות L רציפות (כולל מקורות קטנים באמצע) – ניקוד כאחד
    groups=[]
    for f,t in seq:
        key='L' if f in('L','Lf') else f
        if groups and groups[-1][0]==key: groups[-1][1].append((f,t))
        else: groups.append([key,[(f,t)]])
    for key,parts in groups:
        if key=='L':
            words=[]; owner=[]
            for pi,(f,t) in enumerate(parts):
                if f=='Lf': continue
                for w in t.split(): words.append(w); owner.append(pi)
            V=vocalize(words,vocalize.last); k=0; buf=[]
            for pi,(f,t) in enumerate(parts):
                if f=='Lf': buf.append('</b>'+esc(t.strip())+'<b>'); continue
                c=sum(1 for o in owner if o==pi); buf.append(esc(' '.join(V[k:k+c]))); k+=c
            out.append('<b>'+' '.join(x for x in buf if x)+'</b>')
        else:
            t=' '.join(x for _,x in parts)
            if key=='H': out.append('<b>'+esc(t.strip())+'</b>')
            elif key=='s': out.append('<sup>'+esc(t.replace(' ',''))+'</sup>')
            elif key=='c': out.append('•')
            else: out.append(esc(t.strip()))
    h=' '.join(x for x in out if x)
    h=re.sub(r'\s+',' ',h).replace('<b></b>','').replace(' </b>','</b> ').replace('<b> ',' <b>')
    h=re.sub(r' +([,.:;!?])',r'\1',h); h=re.sub(r'\s+<sup>','<sup>',h)
    return h.strip()
def merge(a,b):
    a=[list(x) for x in a]; b=[list(x) for x in b]
    if a and b and a[-1][0]==b[0][0]: a[-1][1]=a[-1][1].rstrip()+' '+b[0][1].lstrip(); return a+b[1:]
    if a: a[-1][1]=a[-1][1].rstrip()+' '
    return a+b
CH1=re.compile(r'^(תמצית הדברים|קיום התורה למעשה|ליקוטי תפילות|לקוטי תפילות|הקדמה מרבי נתן)')
def build():
    d=pymupdf.open('maay.pdf'); ev=[]; cur=None; notes=[]; prevl=None; titlebuf=None
    def flush():
        nonlocal cur
        if cur: ev.append(('P',render(cur['runs']),cur['pn'])); cur=None
    def addnote(lbl,runs,pn):
        h=render(runs); notes.append((lbl,h,pn))
    for pn in range(len(d)):
        items=page_seq(d,pn); fn=None
        for l in items:
            fs=l['fonts']; tot=sum(fs.values()); main=fs.most_common(1)[0][0]
            t=l['text'].strip()
            if pn==0 and t in('בס"ד','בסימנא טבא'): continue
            # הערות שוליים (שורות בתחתית העמוד, בגופן ההערות)
            isF=(fs['F']+fs['f']+fs['e']+fs['a'])>0.6*tot
            if isF and (l.get('full') or (fn is not None)):
                lead=l['runs'][0][1].strip()
                m=re.match(r'^([א-ת]{1,2})\s?\.\s*',l['text'].strip())
                if m and (l['runs'][0][0]=='a' or fn is None or l['x0']<62):
                    rr=[list(r) for r in l['runs']]
                    rest=l['text'].strip()[m.end():]
                    # מסירים את התווית מהרצים
                    k=len(m.group(0)); out=[]
                    for f,t in rr:
                        t2=t.lstrip() if not out and k>0 else t
                        if k>0:
                            cut=min(k,len(t2)); k-=cut; t2=t2[cut:]
                        if t2: out.append([f,t2])
                    fn=[m.group(1),out,pn]; notes.append(fn)
                elif fn is not None: fn[1]=merge(fn[1],l['runs'])
                elif notes and l.get('full'): fn=notes[-1]; fn[1]=merge(fn[1],l['runs'])
                continue
            tf=[f for f in ('T0','T1','T2','T3') if fs[f]>0.6*tot]
            if tf:
                flush(); k=tf[0]
                if k=='T0': continue
                kind={'T1':'H0','T2':'H1'}.get(k) or ('H1' if CH1.match(t) else 'H2')
                if kind=='H0': t=re.sub(r'^(ספר )?ליקוטי מוהר"ן ?','',t).strip()
                if kind=='H0': t=re.sub(r'^חלק א (סימן|תורה) ','חלק א · תורה ',t)
                if kind=='H2' and ev and ev[-1][0]=='H0' and ev[-1][2]==pn: kind='H1'
                if ev and ev[-1][0]==kind and ev[-1][2]==pn and prevl is not None and prevl.get('_t')==k and l['y']-prevl['y']<45:
                    ev[-1]=(kind,ev[-1][1]+' '+esc(t),pn)
                else: ev.append((kind,esc(t),pn))
                l['_t']=k; l['pn']=pn; prevl=l; continue
            first=l['runs'][0][0]
            newp = first in('H','c') or cur is None or (prevl is not None and prevl.get('_t'))
            if prevl is not None and prevl.get('pn')==pn and l['y']>prevl['y']+22: newp=True
            if newp: flush(); cur=dict(runs=list(l['runs']),pn=pn)
            else: cur['runs']=merge(cur['runs'],l['runs'])
            l['pn']=pn; prevl=l
    flush()
    # תורה א: כותרת הנושא עוברת למקום שבו מתחיל הביאור (אחרי הקדמת רבי נתן)
    for i,e in enumerate(ev):
        if e[0]=='H1' and i>0 and ev[i-1][0]=='H0' and i+1<len(ev) and ev[i+1][0]=='H1':
            j=next((k for k in range(i+2,len(ev)) if ev[k][0]=='P' and ev[k][1].startswith('<b>תורה</b> זו נדרשה')),None)
            if j: ev.insert(j,e); del ev[i]
            break
    ev[:]=[(k,re.sub(r'^(.*?)\s*\1$',r'\1',t) if k=='H0' else t,p) for k,t,p in ev]
    # הצמדת הערות: לפסקה עם הסימון התואם (בעמוד של ההערה או לפניו)
    out=list(ev); used=0
    for lbl,runs,pn in notes:
        h='<b>'+esc(lbl)+'.</b> '+render(runs)
        idx=None
        for i in range(len(out)-1,-1,-1):
            if out[i][0]=='P' and out[i][2]<=pn and ('<sup>'+lbl+'</sup>') in out[i][1]: idx=i; break
        if idx is None:
            for i in range(len(out)-1,-1,-1):
                if out[i][0]=='P' and out[i][2]<=pn: idx=i; break
        else: used+=1
        j=idx+1
        while j<len(out) and out[j][0]=='F': j+=1
        out.insert(j,('F',h,pn))
    print('notes',len(notes),'matched to marker',used)
    return out
if __name__=='__main__':
    ev=build()
    print('vocalize',dict(stat))
    bk=to_book(ev,147,'מעיינות אשר',first_title='הקדמה מרבי נתן זי"ע'); stats(bk)
    for s in bk: print(s['short'],'::',' | '.join('%s(%d)'%(c['t'],len(c['i'])) for c in s['c'])[:300])
    show(bk,0,2,6,0)
    pickle.dump(bk,open('maay.book','wb'))
