# שולחן ערוך: הלכות -> סימנים -> סעיפים; באר היטב כמפרש
import pickle,re,html
S=pickle.load(open('sa_raw.pkl','rb'))
esc=lambda t: html.escape(t.strip(' \xa0'),quote=False)
def parse(fid):
    ps=S[fid]
    k=next(i for i,(s,t) in enumerate(ps) if '\xa0\xa0\xa0' in t and t.count('הלכות')>3)
    toc=[x.strip(' \xa0') for x in ps[k][1].split('\xa0\xa0\xa0') if x.strip(' \xa0')]
    start=k+2  # אחרי רשימת הסימנים
    secs=[]; sec=None; ch=None; it=None
    def newsec(t):
        nonlocal sec,ch,it; sec={'short':t,'c':[]}; secs.append(sec); ch=None; it=None
    for s,t in ps[start:]:
        if t.lstrip(' \xa0').startswith('באר היטב'):
            body=t.strip(' \xa0')[len('באר היטב'):].strip(' \xa0')
            if it is not None: it.setdefault('bh',[]).append(body)
            continue
        for ln in t.split('\n'):
            st=ln.strip(' \xa0')
            if not st: continue
            if st in toc and (sec is None or st!=sec['short']): newsec(st); continue
            if sec is not None and st==sec['short']: continue
            m=re.match(r'^סימן ([א-ת]{1,4}) - (.*)$',st)
            if m and len(st)<160:
                if sec is None: newsec(toc[0])
                ch={'t':'סימן '+m.group(1)+' – '+re.sub(r"\.? ?ובו .*סעיפים?:?$|\.? ?ובו סעיף אחד:?$","",m.group(2)).strip(' .:'),'i':[]}; sec['c'].append(ch); it=None; continue
            pl=re.sub(r'[\u0591-\u05c7]','',st)
            mo=re.match(r"^(.*?)\s*ובו .{0,14}סעיפים?\s*:?$|^(.*?)\s*ובו סעיף אחד",pl)
            if mo and ch is not None and not ch['i']:
                pre=(mo.group(1) or mo.group(2) or '').strip()
                if pre: ch['t']+=' '+pre
                continue
            m=re.match(r'^([א-ת]{1,3})\.?\xa0(.*)$',ln.strip(' '))
            if m and ch is not None:
                it={'n':m.group(1),'b':[['p',esc(m.group(2))]]}; ch['i'].append(it); continue
            if ch is None: continue
            if it is None: it={'n':'','b':[]}; ch['i'].append(it)
            if st.startswith('הגה:'):
                it['b'].append(['p','<b>הגה:</b> '+esc(st[4:])])
            else: it['b'].append(['p',esc(st)])
    return toc,secs
if __name__=='__main__':
    import json
    R={}
    for fid in ['6f18e94e','8b3829b6','b9217579','6ad736fc']:
        toc,secs=parse(fid); R[fid]=secs
        nch=sum(len(s['c']) for s in secs); nit=sum(len(c['i']) for s in secs for c in s['c']); nbh=sum(1 for s in secs for c in s['c'] for i in c['i'] if 'bh' in i)
        empty=[c['t'] for s in secs for c in s['c'] if not c['i']]
        nonum=sum(1 for s in secs for c in s['c'] for i in c['i'] if not i['n'])
        sz=len(json.dumps(secs,ensure_ascii=False))
        print(fid,'toc',len(toc),'secs',len(secs),'simanim',nch,'seifim',nit,'bh',nbh,'no-num',nonum,'empty',len(empty),empty[:3],'size',sz//1024,'KB')
    pickle.dump(R,open('sa.pkl','wb'))
    s=R['6f18e94e'][0]['c'][0]; print(s['t'],[ (i['n'],[b[1][:50] for b in i['b']]) for i in s['i'][:3]])
    s=R['8b3829b6'][0]['c'][0]; print(s['t'],[ (i['n'],[b[1][:50] for b in i['b']],[x[:40] for x in i.get('bh',[])]) for i in s['i'][:2]])
