# בונה ספר (פרקים ← קטעים ← פסקאות) מהשורות שחולצו
import re,json,sys,html,collections
from st import load
def esc(t): return html.escape(t,quote=False)
def build(name,cfg):
    P=load(name); R=cfg.get('right'); Lm=cfg.get('left'); auto=R is None
    ev=[]  # ('H1',text) ('H2',text) ('P',text) ('F',text)
    cur=None; prev=None
    def flush():
        nonlocal cur
        if cur:
            if cur['kind']=='C': ev.append(('P','<br>'.join(esc(x) for x in cur['ls']),cur['pn'],cur['ys']))
            else: ev.append(('P',esc(' '.join(cur['ls'])),cur['pn'],cur['ys']))
        cur=None
    for pn in range(cfg['p0'],cfg['p1']):
        if pn in cfg.get('skip',()): continue
        Lp=[l for l in P[pn] if not cfg['drop'](l,pn)]
        if auto:
            bl=[l for l in Lp if cfg['cls'](l,pn)=='B' and l['x1']-l['x0']>cfg.get('minw',180)]
            if bl:
                R=collections.Counter(round(l['x1']) for l in bl).most_common(1)[0][0]+0.3; Lm=collections.Counter(round(l['x0']) for l in bl).most_common(1)[0][0]-0.3
            elif R is None: R,Lm=cfg.get('R0',361),cfg.get('L0',63)
        for l in Lp:
            l['pn']=pn
            if cfg.get('fix'): l['text']=cfg['fix'](l['text'])
            k=cfg['cls'](l,pn)
            if k=='skip': continue
            if k in ('H0','H1','H2','H3'):
                flush()
                # כותרת בכמה שורות – מאחדים
                if ev and ev[-1][0]==k and ev[-1][2]==pn and prev is not None and prev.get('_k')==k and prev['font']==l['font'] and abs(prev['size']-l['size'])<0.6 and l['y']-prev['y']<2.2*l['size']: ev[-1]=(k,ev[-1][1]+' '+esc(l['text']),pn)
                elif k=='H1' and cfg.get('h1join') and ev and ev[-1][0]=='H1' and ev[-1][2]==pn and prev is not None and prev.get('_k')=='H1' and l['y']-prev['y']<cfg['h1join']: ev[-1]=(k,ev[-1][1]+' · '+esc(l['text']),pn)
                else: ev.append((k,esc(l['text']),pn))
                l['_k']=k; prev=l; continue
            if k=='F':
                flush(); ev.append(('F',esc(l['text']),pn)); l['_k']=k; prev=l; continue
            # גוף
            w=R-Lm; ind=R-l['x1']; rag=l['x0']-Lm
            centered = ind>cfg.get('cind',22) and rag>cfg.get('cind',22) and abs(ind-rag)<cfg.get('ctol',14)
            if cfg.get('cpage') and cfg['cpage'](l,pn): centered=True
            if cfg.get('nocenter') and cfg['nocenter'](l,pn): centered=False
            newp=False
            if cfg.get('pstart') and cfg['pstart'](l,pn): newp=True
            if cur is None: newp=True
            elif prev is None or prev.get('_k')!='B': newp=True
            else:
                samepage = prev['pn']==pn
                gap = l['y']-prev['y'] if samepage else 0
                lead=cfg.get('lead',1.32)*max(l['size'],prev['size'])
                if cfg.get('grp') and cfg['grp'](l)!=cfg['grp'](prev): newp=True
                elif centered != (cur['kind']=='C'): newp=True
                elif centered:
                    if samepage and gap>1.9*l['size']: newp=True
                else:
                    if ind>cfg.get('ind',8) and ind<cfg.get('indmax',40): newp=True      # שורה ראשונה מוזחת
                    elif cfg.get('outdent') and l['x1']-R>cfg['outdent']: newp=True
                    elif cfg.get('shortend') and samepage and (prev['x0']-Lm)>cfg['shortend'] and re.search(r'[.:!?]\)?["״]?$',prev['text']): newp=True
                    elif samepage and gap>lead+cfg.get('gapx',3.5): newp=True
                    elif (prev['x0']-Lm)>cfg.get('short',30) and re.search(r'[.:!?"״\')\]]$',prev['text']) and cfg.get('shortbreak',True) and not cfg.get('noind',False)==False and False: newp=True
            if newp:
                flush(); cur=dict(kind='C' if centered else 'J',ls=[l['text']],pn=pn,ys=[(pn,l['y'])])
            else: cur['ls'].append(l['text']); cur['ys'].append((pn,l['y']))
            l['_k']='B'; prev=l
    flush()
    return ev
def to_book(ev,vi,short,first_title='פתיחה',first_sec=None):
    """H0 = חלק (section). H1 = פרק. H2/H3 = כותרת משנה (בלוק h). כל פסקה = קטע."""
    secs=[]; sec=None; ch=None; pend=[]
    def newsec(t):
        nonlocal sec,ch
        sec=dict(id='v%dg%d'%(vi,len(secs)),short=t,g='V%d'%vi,c=[]); secs.append(sec); ch=None
    def newch(t):
        nonlocal ch
        if sec is None: newsec(first_sec or short)
        ch=dict(t=t,i=[]); sec['c'].append(ch)
    for e in ev:
        k,t=e[0],e[1]
        if k=='H0': newsec(re.sub(r'<[^>]+>','',t)); pend=[]; continue
        if k=='H1': newch(re.sub(r'<[^>]+>','',t)); pend=[]; continue
        if ch is None: newch(first_title if (sec is None or not sec['c']) and not secs[1:] else (sec['short'] if sec else first_title))
        if k in('H2','H3'): pend.append(['h',t]); continue
        if k=='F':
            if ch['i'] and not pend: ch['i'][-1]['b'].append(['f',t])
            else: pend.append(['f',t])
            continue
        ch['i'].append(dict(n='',b=pend+[['p',t]])); pend=[]
    if pend and ch:
        if ch['i']: ch['i'][-1]['b']+=pend
        else: ch['i'].append(dict(n='',b=pend))
    for s_ in secs:
        for c in s_['c']:
            if re.fullmatch(r"פרק [א-ת]{1,2}'?",c['t']) and c['i'] and c['i'][0]['b'][0][0]=='h':
                c['t']+=' · '+re.sub(r'<[^>]+>','',c['i'][0]['b'].pop(0)[1])
        if len(s_['c'])>1 and not s_['c'][0]['i'] and s_['c'][0]['t'] not in s_['short']: s_['short']+=' · '+s_['c'][0]['t']
        s_['c']=[c for c in s_['c'] if c['i']]
    return [s_ for s_ in secs if s_['c']]
def stats(book):
    for s in book:
        n=sum(len(c['i']) for c in s['c']); w=sum(len(re.sub(r'<[^>]+>','',b[1]).split()) for c in s['c'] for i in c['i'] for b in i['b'])
        print(s['short'],'| chapters',len(s['c']),'items',n,'words',w)
def show(book,a=0,b=3,maxp=6,si=0):
    for c in book[si]['c'][a:b]:
        print('#####',c['t'])
        for it in c['i'][:maxp]:
            for bl in it['b']: print('  [%s] %s'%(bl[0],bl[1][:230]))
