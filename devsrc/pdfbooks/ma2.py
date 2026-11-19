import pymupdf,unicodedata,re,collections,json,glob,difflib,html
from ma import FN,plain
TITLE={'T0','T1','T2','T3'}
HEB='אבגדהוזחטיכלמנסעפצקרשת'
def dec(t): # TTAA/TTAC: ` = א, a = ב ...
    return ''.join(HEB[ord(c)-ord('`')] if '`'<=c<='u' else c for c in t)
MK=[]
def chars(d,pn):
    MK.clear(); p=d[pn]; rd=p.get_text('rawdict',flags=pymupdf.TEXT_PRESERVE_WHITESPACE); cs=[]
    for b in rd['blocks']:
        for l in b.get('lines',[]):
            for s in l['spans']:
                f=FN.get(s['font'],s['font'])
                for ch in s['chars']:
                    if 'TTCA' in s['font']: MK.append(ch['origin'][1]); continue
                    t=plain(ch['c'])
                    if f in('a','R'): t=dec(t)
                    if not t: continue
                    x0,y0,x1,y1=ch['bbox']; cs.append(dict(c=t,x0=x0,x1=x1,y=ch['origin'][1],f=f,z=s['size']))
    return [c for c in cs if c['y']>75]
def group(cs,tol=2.0):
    cs=sorted(cs,key=lambda c:(c['y'],-c['x0'])); L=[]
    for c in cs:
        for ln in reversed(L[-6:]):
            if abs(ln['y']-c['y'])<=tol: ln['cs'].append(c); break
        else: L.append(dict(y=c['y'],cs=[c]))
    return sorted(L,key=lambda l:l['y'])
def mkline(ln):
    ch=sorted(ln['cs'],key=lambda c:-(c['x0']+c['x1'])/2); runs=[]; prev=None
    expl=any(abs(y-ln['y'])<2.5 for y in MK)   # שורה עם ניקוד בגופן נפרד: רק רווחים מפורשים
    for c in ch:
        if c['c'].strip()=='':
            if runs and runs[-1][1][-1:]!=' ': runs[-1][1]+=' '
            prev=c; continue
        sp=(not expl) and prev is not None and prev['c'].strip()!='' and prev['x0']-c['x1']>0.25*c['z']
        if runs and runs[-1][0]==c['f']: runs[-1][1]+=(' ' if sp and runs[-1][1][-1:]!=' ' else '')+c['c']
        else:
            if sp and runs and runs[-1][1][-1:]!=' ': runs[-1][1]+=' '
            runs.append([c['f'],c['c']])
        prev=c
    for r in runs: r[1]=re.sub('\ufffd(?=א)','ל',r[1]).replace('\ufffd','ך')
    for r in runs: r[1]=re.sub(r'[0-9A-Za-z][0-9A-Za-z.,:/\-]*[0-9A-Za-z]', lambda m:m.group(0)[::-1], r[1]).translate({40:41,41:40,91:93,93:91})
    nb=[c for c in ch if c['c'].strip()]
    return dict(y=ln['y'],x0=min(c['x0'] for c in nb),x1=max(c['x1'] for c in nb),runs=runs,text=''.join(r[1] for r in runs),
                fonts=collections.Counter(c['f'] for c in nb))
GL,GR=229.5,242.5
def page_seq(d,pn):
    cs=chars(d,pn)
    FW=group(cs)
    items=[]; band=[]
    def flush():
        if not band: return
        allc=[c for l in band for c in l['cs']]
        R=[c for c in allc if (c['x0']+c['x1'])/2>236]; Lc=[c for c in allc if (c['x0']+c['x1'])/2<=236]
        for col in (R,Lc):
            for ln in group(col):
                if any(c['c'].strip() for c in ln['cs']): items.append(mkline(ln))
        band.clear()
    for ln in FW:
        nb=[c for c in ln['cs'] if c['c'].strip()]
        if not nb: continue
        cross=any(c['x0']<GR and c['x1']>GL for c in nb)
        if cross:
            flush(); m=mkline(ln); m['full']=1; items.append(m)
        else: band.append(ln)
    flush()
    return items
if __name__=='__main__':
    import sys
    d=pymupdf.open('maay.pdf')
    for pn in map(int,sys.argv[1:]):
        print('=== page',pn)
        for l in page_seq(d,pn): print('F' if l.get('full') else ' ','%5.1f %5.1f-%5.1f'%(l['y'],l['x0'],l['x1']),' '.join('[%s]%s'%(f,t) for f,t in l['runs'])[:170])
