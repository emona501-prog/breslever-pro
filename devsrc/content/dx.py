import glob,docx,sys,collections
D='/mnt/user-data/attachments/04acf86a-d2b1-5d3c-a4f5-9416ecb330d5/'
def paras(fid):
    d=docx.Document(glob.glob(D+fid+'*')[0]); out=[]
    for p in d.paragraphs:
        t=p.text
        if not t.strip(): continue
        sz=collections.Counter(); bold=0; tot=0
        for r in p.runs:
            n=len(r.text.strip()); 
            if not n: continue
            tot+=n; sz[r.font.size.pt if r.font.size else 0]+=n; bold+=n if r.bold else 0
        out.append({'t':t,'sz':sz.most_common(1)[0][0] if sz else 0,'b':bold/tot if tot else 0,'al':str(p.alignment)})
    return out
if __name__=='__main__':
    fid=sys.argv[1]; a=int(sys.argv[2]) if len(sys.argv)>2 else 0; n=int(sys.argv[3]) if len(sys.argv)>3 else 30
    P=paras(fid)
    c=collections.Counter((p['sz'],round(p['b'])) for p in P); print(len(P),c.most_common(8))
    for p in P[a:a+n]: print(p['sz'],round(p['b'],1),'|',repr(p['t'][:110]),'…' if len(p['t'])>110 else '', len(p['t']))
