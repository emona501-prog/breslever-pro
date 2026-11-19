import pymupdf,unicodedata,re,collections
FN={'TTB82o00':'L','TTBE2o00':'C','TTAE2o00':'H','TTC82o00':'F','TTC02o00':'f','TTB62o00':'T3','TTB42o00':'T2','TTB22o00':'T1','TTB02o00':'T0','TTAA2o00':'a','TTAC2o00':'R','TTC62o00':'s','TTCE2o00':'e','TTCC2o00':'c','TTC22o00':'g','TTD02o00':'d','TTBC2o00':'m'}
def mark(c): return unicodedata.combining(c)>0
def plain(c): return ''.join(k for k in unicodedata.normalize('NFKD',c) if not mark(k))
def page(d,pn,gut=None):
    p=d[pn]; W=p.rect.width
    rd=p.get_text('rawdict',flags=pymupdf.TEXT_PRESERVE_WHITESPACE); cs=[]
    for b in rd['blocks']:
        for l in b.get('lines',[]):
            for s in l['spans']:
                f=FN.get(s['font'],s['font'])
                for ch in s['chars']:
                    t=plain(ch['c'])
                    if not t: continue
                    x0,y0,x1,y1=ch['bbox']; cs.append(dict(c=t,x0=x0,x1=x1,y=ch['origin'][1],f=f,z=s['size']))
    return cs,W
def lines(cs,colsplit=None):
    out=[]
    groups={}
    for c in cs:
        col=0
        if colsplit:
            cx=(c['x0']+c['x1'])/2
            col='R' if cx>colsplit else 'L'
        groups.setdefault(col,[]).append(c)
    res={}
    for col,g in groups.items():
        g.sort(key=lambda c:(round(c['y'],0),-c['x0']))
        L=[]
        for c in g:
            for ln in reversed(L[-4:]):
                if abs(ln['y']-c['y'])<=2.0: ln['cs'].append(c); break
            else: L.append(dict(y=c['y'],cs=[c]))
        for ln in L:
            ch=sorted(ln['cs'],key=lambda c:-(c['x0']+c['x1'])/2)
            # runs by font, spaces by gap
            runs=[]; prev=None
            for c in ch:
                if c['c'].strip()=='':
                    if runs and runs[-1][1] and runs[-1][1][-1]!=' ': runs[-1][1]+=' '
                    prev=c; continue
                sp = prev is not None and prev['c'].strip()!='' and prev['x0']-c['x1']>0.25*c['z']
                if runs and runs[-1][0]==c['f']:
                    runs[-1][1]+=(' ' if sp and runs[-1][1][-1:]!=' ' else '')+c['c']
                else:
                    if sp and runs and runs[-1][1][-1:]!=' ': runs[-1][1]+=' '
                    runs.append([c['f'],c['c']])
                prev=c
            ln['runs']=runs; ln['x0']=min(c['x0'] for c in ch); ln['x1']=max(c['x1'] for c in ch)
            ln['text']=''.join(r[1] for r in runs)
        res[col]=sorted(L,key=lambda l:l['y'])
    return res
def fixltr(t): return re.sub(r'[0-9A-Za-z][0-9A-Za-z.,:/\-]*[0-9A-Za-z]', lambda m:m.group(0)[::-1], t)
if __name__=='__main__':
    import sys
    d=pymupdf.open('maay.pdf')
    for pn in map(int,sys.argv[1:]):
        cs,W=page(d,pn)
        # gutter: find x with no chars in middle region
        xs=collections.Counter()
        for c in cs:
            if 75<c['y']<560:
                for x in range(int(c['x0']),int(c['x1'])+1): xs[x]+=1
        mid=[x for x in range(int(W*0.35),int(W*0.65)) if xs[x]==0]
        gut=sum(mid)/len(mid) if mid else None
        print('=== page',pn,'W',W,'gutter',gut)
        R=lines(cs,gut)
        for col in ('R','L',0):
            for l in R.get(col,[]):
                print(col,'%5.1f %5.1f-%5.1f'%(l['y'],l['x0'],l['x1']),' '.join('[%s]%s'%(f,t) for f,t in l['runs'])[:200])
