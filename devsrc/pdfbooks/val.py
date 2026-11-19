# בודק ניקוד חשוד בטקסט שחולץ
import re,sys,collections,pymupdf
from px import *
V='ְֱֲֳִֵֶַָׇֻ'
def sus(w):
    r=[]
    cl=re.findall(r'[א-ת][֑-ׇ]*',w)
    for c in cl:
        m=c[1:]; b=c[0]
        if sum(1 for k in m if k in V)>1: r.append('2vow:'+c)
        if m.count('ּ')>1: r.append('2dag')
        if 'ּ' in m and b in 'אחעםןץ': r.append('dag:'+b)
        if ('ׁ' in m or 'ׂ' in m) and b!='ש': r.append('shin:'+b)
        if b in 'םןץף' and m and not (b=='ף' and False): r.append('fin:'+c)
    if re.search(r'(^|[^א-ת])[֑-ׇ]',w): r.append('orphan')
    return r
if __name__=='__main__':
    f=sys.argv[1]; d=pymupdf.open(f); C=collections.Counter(); ex=collections.defaultdict(list); tot=0; F=collections.Counter()
    kw=dict(pua=PUA_MESH,mode='stream',prefont=PRE_MESH) if 'mesh' in f else dict(mode=sys.argv[4] if len(sys.argv)>4 else 'geom')
    for pn in range(int(sys.argv[2]),int(sys.argv[3])):
        for l in page_lines(d[pn],**kw):
            for w in l['text'].split():
                tot+=1
                for r in sus(w):
                    k=r.split(':')[0]; C[k]+=1
                    if len(ex[k])<12: ex[k].append((pn,w,l['font'][:12]))
                    F[(k,l['font'])]+=1
    print('words',tot,dict(C))
    for k in ex: print(k,ex[k])
    print(F.most_common(12))
