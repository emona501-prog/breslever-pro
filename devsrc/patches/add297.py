# הוספת סימן רצז(א) – כלאי בהמה (שו"ע+רמ"א מנוקד מהמשתמש, באר היטב מהמשתמש) לתוך V137 סעיף v137g47
import json,re,hashlib,html,glob,os,shutil
D='/home/claude/breslever-pro/www/data/'; SH='/home/claude/src/shell.html'
SRC=os.environ['SRC']; BH='/home/claude/content/out7/bh297.txt'
L=[l.strip() for l in open(SRC,encoding='utf-8') if l.strip()]
assert L[0]=='הלכות כלאי בהמה' and L[1].startswith('סימן רצז (א)')
title='סימן רצז (א) – '+L[1].split(' - ',1)[1].strip()
its=[]
for l in L[3:]:
    n,t=l.split(' ',1)
    t=re.sub(r'\s+\.', '.', re.sub(r'\s+',' ',t)).strip()
    its.append({'n':n,'b':[['p',t]]})
assert [i['n'] for i in its]==['א','ב','ג','ד','ה','ו','ז','ח','ט','י','יא','יב','יג','יד','טו','טז'],[i['n'] for i in its]
fn=[f for f in os.listdir(D) if re.search(r'_V137\.',f)][0]
d=json.load(open(D+fn,encoding='utf-8'))
si=[k for k,s in enumerate(d) if s['id']=='v137g47'][0]; assert si==47 and not d[si]['c']
d[si]['c']=[{'t':title,'i':its}]
mf=glob.glob(D+'mg/V137.*.json')[0]; m=json.load(open(mf,encoding='utf-8'))
nm={i['n']:k for k,i in enumerate(its)}
for l in open(BH,encoding='utf-8'):
    l=l.strip()
    if not l: continue
    n,t=l.split(' ',1); m['c']['%d.0.%d'%(si,nm[n])]=[[0,html.escape(t,quote=False)]]
js=json.dumps(d,ensure_ascii=False,separators=(',',':'))
nfn='b135_V137.%s.json'%hashlib.md5(js.encode()).hexdigest()[:10]
mj=json.dumps(m,ensure_ascii=False,separators=(',',':'))
nmf='mg/V137.%s.json'%hashlib.md5(mj.encode()).hexdigest()[:8]
os.remove(D+fn); os.remove(mf)
open(D+nfn,'w',encoding='utf-8').write(js); open(D+nmf,'w',encoding='utf-8').write(mj)
s=open(SH,encoding='utf-8').read()
assert s.count('data/'+fn)==1 and s.count(os.path.basename(mf))==1
s=s.replace('data/'+fn,'data/'+nfn).replace('mg/'+os.path.basename(mf),nmf)
open(SH,'w',encoding='utf-8').write(s)
print(title,len(its),'seifim; bh',sum(1 for k in m['c'] if k.startswith('%d.'%si)),'->',nfn,nmf)
