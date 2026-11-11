import glob,docx,re,collections,pickle,sys
D='/mnt/user-data/attachments/04acf86a-d2b1-5d3c-a4f5-9416ecb330d5/'
def load(i):
    d=docx.Document(glob.glob(D+i+'*')[0]); out=[]
    for p in d.paragraphs:
        t=p.text
        if not t.strip(): continue
        runs=[r for r in p.runs if r.text.strip()]
        bold=bool(runs) and all(r.bold for r in runs)
        out.append(('W' if p.style.name.startswith('Normal (Web)') else 'N' if p.style.name=='Normal' else 'H', bold, t))
    return out
if __name__=='__main__':
    R={}
    for i in sys.argv[1:]:
        P=load(i); R[i]=P
        seq=''.join(k for k,b,t in P)
        short=collections.Counter()
        for k,b,t in P:
            if len(t.strip())<45: short[(k,b,re.sub(r"[א-ת\"']+",'x',t.strip())[:30])]+=1
        print(i,len(P),'WN pairs',seq.count('WN'),'WW',seq.count('WW'),'NN',seq.count('NN'))
        print('   short:',short.most_common(9))
    pickle.dump(R,open('zo_raw.pkl','wb'))
