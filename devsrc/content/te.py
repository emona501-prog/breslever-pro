# מפענח קובצי "תורת אמת" (docx): פרקים, פסוקים, מפרשים (כולל מפרשים מרובי-פסקאות), פרשיות
import glob,docx,re,collections
D='/mnt/user-data/attachments/04acf86a-d2b1-5d3c-a4f5-9416ecb330d5/'
RX_CH=re.compile(r'^(.{2,20}?) פרק-([א-ת]{1,3})\s*$')
RX_V=re.compile(r'^\{([א-ת]{1,3})\}\s+(.*)$')
RX_S=re.compile(r'^[ \xa0]?([^\xa0]{2,30}?)\xa0\xa0[ \xa0]*(.*)$')
NORM=lambda x: re.sub(r'\s+',' ',x.replace('-',' ').replace('תרגום ','')).strip()
def parse(fid):
    d=docx.Document(glob.glob(D+fid+'*')[0])
    paras=[p.text for p in d.paragraphs if p.text.strip()]
    lines=[]
    for p in paras: lines+=p.split('\n')
    book=None; chs=[]; cur=None; v=None; oc=None; other=[]; names=collections.Counter(); parshiot=[]
    head=[p.strip() for p in paras[:4] if ('זכויות' in p or 'רשיון' in p)]
    for ln in lines:
        s=ln.rstrip()
        if not s.strip(): continue
        st=s.strip(' \xa0')
        m=RX_CH.match(st)
        if m: book=m.group(1); cur={'ch':m.group(2),'v':[]}; chs.append(cur); v=None; oc=None; continue
        m=RX_V.match(st)
        if m and cur is not None:
            v={'n':m.group(1),'t':m.group(2).strip(),'mf':[]}; cur['v'].append(v); oc=None; continue
        if oc is None:
            mp=re.match(r'^פרשת (.{2,20})$',st)
            if mp and cur is not None: parshiot.append((mp.group(1),len(chs)-1,len(cur['v']))); continue
            if mp: continue
            m=RX_S.match(s)
            if m and v is not None:
                oc=[m.group(1).strip(),[m.group(2).strip()]]; v['mf'].append(oc); names[oc[0]]+=1
            else: other.append(st[:80]); continue
        else:
            oc[1].append(st)
        me=re.search(r'\(([^()]{2,40})\)\s*$',oc[1][-1])
        if me and NORM(me.group(1))==NORM(oc[0]):
            oc[1][-1]=oc[1][-1][:me.start()].rstrip()
            if not oc[1][-1]: oc[1].pop()
            oc=None
    for c in chs:
        for vv in c['v']:
            vv['mf']=[(a,'\n'.join(b)) for a,b in vv['mf'] if b]
    return dict(parshiot=parshiot,book=book,chs=chs,names=names,other=other,head=head)
