from bb import *
from st import load
import re
P=load('orach')
DIV={}; MARK=[]; NOTES=[]
for pn,L in enumerate(P):
    d=[l['y'] for l in L if l['font'].startswith('FbAristocrat-Bold') and abs(l['size']-11)<.4 and 'אורח לצדיק' in l['text']]
    DIV[pn]=min(d) if d else None
    for l in L:
        if abs(l['size']-9.3)<.4 and re.fullmatch(r'\d+',l['text']) and (DIV[pn] is None or l['y']<DIV[pn]): MARK.append((pn,int(l['text']),l['y']+5.3))
    if DIV[pn] is not None:
        for l in L:
            if l['y']>DIV[pn]+3 and l['y']<570:
                m=re.match(r'^(\d+)\. ',l['text'])
                if m: NOTES.append([int(m.group(1)),pn,[l['text']]])
                elif NOTES: NOTES[-1][2].append(l['text'])
def drop(l,pn):
    if l['y']<75 and pn>6: return True
    if l['y']>570: return True
    if DIV.get(pn) is not None and l['y']>=DIV[pn]-1: return True
    if abs(l['size']-9.3)<.4 and re.fullmatch(r'\d+',l['text']): return True
    return False
def cls(l,pn):
    f=l['font']; z=l['size']
    if f.startswith('FbAristocrat-Bold') and z>=14.5: return 'H1'
    if f.startswith('FbAristocrat-Bold'): return 'H2'
    return 'B'
CFG=dict(p0=6,p1=64,drop=drop,cls=cls,ind=999,lead=1.3,gapx=2.2,h1join=45,outdent=6,shortend=45,cind=18)
if __name__=='__main__':
    ev=build('orach',CFG)
    # הצמדת ההערות ("אורח לצדיק") לפסקה שבה מופיע הסימון
    byn={}
    for n,pn,ls in NOTES: byn.setdefault(n,[]).append((pn,' '.join(ls)))
    out=[]; used=set(); miss=0
    for e in ev:
        out.append(e)
        if e[0]!='P': continue
        ms=sorted({(pn,n) for (pn,n,y) in MARK for (p2,y2) in e[3] if p2==pn and abs(y2-y)<3.2})
        for pn,n in ms:
            cand=[x for x in byn.get(n,[]) if x[0]>=pn and (n,x[0]) not in used]
            if not cand: miss+=1; continue
            used.add((n,cand[0][0])); out.append(('F','<b>אורח לצדיק</b> · '+esc(cand[0][1]),pn))
    print('markers',len(MARK),'notes',len(NOTES),'attached',len(used),'missing',miss)
    bk=to_book(out,146,'אורח צדיקים',first_title='הקדמה'); stats(bk)
    for s in bk: print(s['short'],'::',' | '.join('%s(%d)'%(c['t'],len(c['i'])) for c in s['c'])[:500])
    show(bk,2,3,6)
    import pickle; pickle.dump(bk,open('orach.book','wb'))
