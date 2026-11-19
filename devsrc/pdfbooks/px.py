# מחלץ שורות מעמוד PDF לפי מיקום האותיות (RTL), עם ניקוד נכון
import pymupdf, unicodedata, re, sys, collections
HEB=lambda c: 'א'<=c<='ת' or c in 'יִשׁשׂוֹ' or 'יִ'<=c<='ﭏ'
MARK=lambda c: ('֑'<=c<='ׇ' and c not in '־׀׃׆') or unicodedata.combining(c)>0
PRE_MESH=('FbMazalMedium','FbThilaMedium','FbShefa')
PUA_MESH={'*':{'\ue802':'ךְ','\ue803':'ךָ','\ue804':'לֹ','\ue805':'לֹּ'}}
def nk(t):
    return unicodedata.normalize('NFC',unicodedata.normalize('NFKC',t)) if any('\ufb00'<=c<='\ufb4f' for c in t) else unicodedata.normalize('NFC',t)
def real_marks(b,cs,isM):
    return [m for m in cs if isM(m) and m['x1']-m['x0']<0.5 and abs(m['ox']-b['x0'])<0.9]
def page_lines(page, pua=None, mode='stream', prefont=None, gapf=0.1, noswap=0):
    rd=page.get_text('rawdict', flags=pymupdf.TEXT_PRESERVE_WHITESPACE)
    chars=[]; sid=0
    for b in rd['blocks']:
        for l in b.get('lines',[]):
            for s in l['spans']:
                sid+=1
                for ch in s['chars']:
                    c=ch['c']
                    if pua and c in pua.get(s['font'],{}): c=pua[s['font']][c]
                    elif pua and c in pua.get('*',{}): c=pua['*'][c]
                    if c=='\t': c=' '
                    c=nk(c)
                    x0,y0,x1,y1=ch['bbox']; ox,oy=ch['origin']
                    chars.append(dict(c=c,x0=x0,x1=x1,ox=ox,oy=oy,size=s['size'],font=s['font'],sid=sid,k=len(chars)))
    lines=[]
    for c in sorted(chars,key=lambda c:(round(c['oy'],1),c['k'])):
        for L in reversed(lines[-8:]):
            if abs(L['y']-c['oy'])<=max(1.2,0.18*max(c['size'],L['size'])):
                L['cs'].append(c); break
        else: lines.append(dict(y=c['oy'],size=c['size'],cs=[c]))
    out=[]
    for L in lines:
        cs=sorted(L['cs'],key=lambda c:c['k'])
        isM=lambda c: c['c']!='' and all(MARK(k) for k in c['c'])
        base=[c for c in cs if not isM(c)]
        if not [b for b in base if b['c'].strip()]: continue
        for b in base: b['m']=[]
        real=[b for b in base if b['c'].strip()]
        real=[b for b in base if b['c'].strip()]
        PRE=set('\u05bc\u05b9\u05c1\u05c2')
        H=lambda b: b is not None and '\u05d0'<=b['c'][0]<='\u05ea'
        hasd=lambda b: '\u05bc' in b['c'] or any(m['c']=='\u05bc' for m in b['m'])
        hasv=lambda b: any(m['c'] not in PRE for m in b['m'])
        VAL={'\u05bc':lambda b: H(b) and not hasd(b) and b['c'][0] not in 'אחעםןץ', '\u05c1':lambda b:H(b) and b['c'][0]=='ש','\u05c2':lambda b:H(b) and b['c'][0]=='ש'}
        for i,c in enumerate(cs):
            if not isM(c): continue
            tgt=None
            mx=c['ox'] if c['x1']-c['x0']<0.5 else (c['x0']+c['x1'])/2
            if mode=='stream' and c['x1']-c['x0']<0.5:
                ins=[b for b in real if b['x0']+0.95<mx<b['x1']-0.95]
                if ins: tgt=ins[0]
                else:
                    pb=next((d for d in reversed(cs[:i]) if not isM(d) and d['c'].strip() and d['sid']==c['sid']),None)
                    nb=next((d for d in cs[i+1:] if not isM(d) and d['c'].strip() and d['sid']==c['sid']),None)
                    near=lambda b: b is not None and (abs(mx-b['x0'])<2.6 or abs(mx-b['x1'])<2.6)
                    if not near(pb): pb=None
                    if not near(nb): nb=None
                    rev=(pb is not None and nb is not None and (pb['x0']+pb['x1'])<(nb['x0']+nb['x1']))
                    if pb is None and nb is None:
                        # בלי שכנים באותו מקטע: לפי הקצוות
                        L_=[b for b in real if abs(b['x0']-mx)<1.1]; R_=[b for b in real if abs(b['x1']-mx)<1.1]
                        pb=L_[0] if L_ else None; nb=R_[0] if R_ else None; rev=False
                    pretype=c['c'] in PRE and prefont is not None and any(f in c['font'] for f in prefont)
                    a_,b_=(nb,pb) if (pretype!=rev) else (pb,nb)
                    ok=VAL.get(c['c'],lambda b:H(b) and not any(k in '\u05b0\u05b1\u05b2\u05b3\u05b4\u05b5\u05b6\u05b7\u05b8\u05bb\u05b9' for k in b['c'][1:]))
                    kf=None
                    if c['c'] in '\u05b0\u05b8':
                        for cand in (nb,pb):
                            if cand is not None and cand['c']=='ך' and not cand['m']:
                                j=cs.index(cand); own=False
                                for d in cs[j+1:]:
                                    if not isM(d):
                                        if d['c'].strip(): break
                                        continue
                                    if d is not c and d['c'] in '\u05b0\u05b8': own=True
                                if not (own and cand is nb) : kf=cand; break
                    if kf is not None: tgt=kf
                    elif c['c']=='\u05b9' and pretype:
                        # חולם: שייך ל-ו שאחריו, אלא אם ה-ו עיצורית (יש לה תנועה משלה) – אז לאות שלפניו
                        vv=a_
                        if vv is not None and vv['c'][0]=='ו' and not hasv(vv) and not any(isM(d) and d['c'] not in PRE and d['sid']==vv['sid'] and abs(d['ox']-vv['x0'])<1.1 and not (d['c'] in '\u05b0\u05b8' and any(r['c']=='ך' and abs(r['x1']-vv['x0'])<1.3 for r in real)) for d in cs): tgt=vv
                        else: tgt=b_ if H(b_) else a_
                    else:
                        tgt=a_ if ok(a_) else b_ if ok(b_) else None
                        if tgt is None:
                            G=[b for b in real if (abs(b['x0']-mx)<1.1 or abs(b['x1']-mx)<1.1) and ok(b)]
                            tgt=G[0] if G else (a_ if H(a_) else b_ if H(b_) else None)
            if tgt is None:
                tgt=min(real,key=lambda b:0 if b['x0']-0.3<=mx<=b['x1']+0.3 else min(abs(mx-b['x0']),abs(mx-b['x1'])))
            tgt['m'].append(c)
        # כ"ף סופית: שווא/קמץ שנפלו על האות שלפניה
        for j,b in enumerate(real):
            if b['c']=='ך' and not b['m']:
                p=next((r for r in real if abs(r['x0']-b['x1'])<1.5 and r is not b),None)
                if p is not None and sum(1 for m in p['m'] if m['c'] not in PRE)>=2:
                    mv=next((m for m in p['m'] if m['c']=='\u05b0'),None) or next((m for m in p['m'] if m['c']=='\u05b8'),None)
                    if mv is not None: p['m'].remove(mv); b['m'].append(mv)
        real.sort(key=lambda b:(-(b['x0']+b['x1'])/2, b['k']))
        sz=collections.Counter(round(b['size'],1) for b in real).most_common(1)[0][0]
        spx=[(c['x0']+c['x1'])/2 for c in cs if c['c']==' ' and c['x1']-c['x0']>0.5]
        toks=[]; prev=None
        for b in real:
            if prev is not None and (prev['x0']-b['x1']>gapf*sz or (prev['x0']-b['x1']>0.35 and any(b['x1']-0.4<=sp<=prev['x0']+0.4 for sp in spx))): toks.append(' ')
            toks.append(unicodedata.normalize('NFC',b['c']+''.join(dict.fromkeys(m['c'] for m in b['m'] if m['c'] not in b['c'])))); prev=b
        txt=''.join(toks)
        txt=re.sub(r'[0-9A-Za-z][0-9A-Za-z.,:/\-]*[0-9A-Za-z]', lambda m:m.group(0)[::-1], txt)
        if not noswap: txt=txt.translate({40:41,41:40,91:93,93:91})
        fonts=collections.Counter(b['font'] for b in real).most_common(1)[0][0]
        out.append(dict(y=L['y'],x0=min(b['x0'] for b in real),x1=max(b['x1'] for b in real),size=sz,font=fonts,bold=('bold' in fonts.lower()),text=re.sub(r' +',' ',txt).strip(),n=len(real),
                        fonts=collections.Counter(b['font'] for b in real)))
    out.sort(key=lambda l:l['y'])
    return out
if __name__=='__main__':
    d=pymupdf.open(sys.argv[1])
    for pn in sys.argv[2:]:
        p=d[int(pn)]
        print('=== page',pn,p.rect)
        for l in page_lines(p,PUA_MESH if 'mesh' in sys.argv[1] else None, 'stream' if sys.argv[1][:4] in ('mesh','shem') else 'geom', PRE_MESH if 'mesh' in sys.argv[1] else None): print('%6.1f %5.1f-%5.1f %4.1f %-22s| %s'%(l['y'],l['x0'],l['x1'],l['size'],l['font'][:22],l['text']))
