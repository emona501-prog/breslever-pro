import sys,pymupdf,pickle,os
from px import *
CFG={'mesh':dict(pua=PUA_MESH,mode='stream',prefont=PRE_MESH),'shem':dict(mode='stream',prefont=('',),pua={'*':{'\uf076':'◆'}}),
     'olam':dict(mode='stream',prefont=('',),noswap=1),'lev':dict(mode='stream',prefont=('',),noswap=1),'einei':dict(mode='stream',prefont=('',),noswap=1),'orach':dict(mode='stream',prefont=('',),noswap=1),'maay':dict(mode='geom')}
def load(name):
    pk=name+'.pkl'
    if os.path.exists(pk) and os.path.getmtime(pk)>os.path.getmtime('px.py'): return pickle.load(open(pk,'rb'))
    d=pymupdf.open(name+'.pdf'); P=[]
    for p in d: P.append(page_lines(p,**CFG[name]))
    pickle.dump(P,open(pk,'wb')); return P
if __name__=='__main__':
    name=sys.argv[1]; P=load(name); a,b=int(sys.argv[2]),int(sys.argv[3]); body=sys.argv[4] if len(sys.argv)>4 else None
    for pn in range(a,b):
        for l in P[pn]:
            if body and l['font'].startswith(body.split(':')[0]) and abs(l['size']-float(body.split(':')[1]))<0.6: continue
            print('%3d %6.1f %5.1f-%5.1f %4.1f %-20s| %s'%(pn,l['y'],l['x0'],l['x1'],l['size'],l['font'][:20],l['text'][:110]))
