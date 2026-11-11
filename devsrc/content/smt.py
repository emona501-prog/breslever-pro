import glob,docx,re,pickle
D='/mnt/user-data/attachments/04acf86a-d2b1-5d3c-a4f5-9416ecb330d5/'
def parse(fid):
    d=docx.Document(glob.glob(D+fid+'*')[0]); ps=[p.text for p in d.paragraphs if p.text.strip()]
    k=next(i for i,p in enumerate(ps) if '\xa0\xa0\xa0' in p); toc=[x.strip() for x in ps[k].split('\xa0\xa0\xa0') if x.strip()]
    k+=1
    while ps[k].strip() in toc: k+=1
    chs=[]; cur=None; parsh=[]; pend=None
    for p in ps[k:]:
        st=p.strip()
        m=re.match(r'^(.{2,10}) פרק-([א-ת]{1,3})$',st)
        if m: cur={'ch':m.group(2),'v':[]}; chs.append(cur); continue
        if st in toc or re.match(r'^פרשת .{2,14}$',st): pend=st; continue
        for m in re.finditer(r'\{([א-ת]{1,3})\}\xa0(.*?)(?=\{[א-ת]{1,3}\}\xa0|$)',p,re.S):
            body=m.group(2); al=None
            ma=re.match(r'^&nbsp([^\xa0]*)\xa0\xa0',body)
            if ma: al=ma.group(1).strip(); body=body[ma.end():]
            parts=re.split(r'\xa0([מת])\xa0\xa0',body)
            v={'n':m.group(1),'mq':parts[0].strip(),'al':al}
            for a,b in zip(parts[1::2],parts[2::2]):
                if a=='ת': v['tg']=b.strip()
                else: v['m2']=b.strip()
            if pend: parsh.append((pend,len(chs)-1,len(cur['v']))); pend=None
            cur['v'].append(v)
    return dict(chs=chs,parsh=parsh,toc=toc)
if __name__=='__main__':
    R=pickle.load(open('parsed.pkl','rb')); S={}
    for fid,mg in [('7fac3472','8758a269'),('27ebfb7f','4fc99d88'),('ba104fed','0315f37c'),('fd137603','9e200499')]:
        r=parse(fid); S[fid]=r
        a=[len(c['v']) for c in r['chs']]; b=[len(c['v']) for c in R[mg]['chs']]
        diff=[(i+1,x,y) for i,(x,y) in enumerate(zip(a,b)) if x!=y]
        al=[v['al'] for c in r['chs'] for v in c['v'] if v['al']]
        print(fid,'chapters',len(a),len(b),'verses',sum(a),sum(b),'diff',diff[:8],'parshiot',[p[0] for p in r['parsh']],'aliyot',len(al),'no tg',sum(1 for c in r['chs'] for v in c['v'] if 'tg' not in v))
    v=S['7fac3472']['chs'][2]['v'][0]; print({k:(x[:90] if x else x) for k,x in v.items()})
    pickle.dump(S,open('smt.pkl','wb'))
