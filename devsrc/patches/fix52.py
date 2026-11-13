# בנייה מחדש של "תנ"ך ליקוטי מוהר"ן" (V52): קריאה נכונה של מספרי פרקים (י''ב = 12), אימות מול התנ"ך, פסוק ופרשה מדויקים
import json,glob,re,collections,hashlib,sys
OLD=glob.glob('/home/claude/breslever-pro/www/data/b*_V52.*.json')[0]
src=json.load(open(OLD,encoding='utf-8'))
lm={s['id']:s for s in json.load(open(glob.glob('/home/claude/breslever-pro/www/data/b00_V0.*.json')[0],encoding='utf-8'))}
D=json.load(open('/home/claude/kb/env.json'))
SK={'tr','am','src','sl','fold','ins','go','tch','img'}
NQ=re.compile(r'[֑-ׇ]')
def nq(t): return NQ.sub('',t)
def nn(t):
    t=re.sub(r'\s+',' ',re.sub(r'[^א-ת ]',' ',nq(t).replace('־',' '))).strip()
    t=re.sub(r'(^| )יהוה(?= |$)',r'\1ה',t); t=re.sub(r'(^| )([והבלמש]?)אלה(ים|י|יך|יו|ינו|יכם)(?= |$)',r'\1\2אלק\3',t)
    return t
def skel(t): return ' '.join(w[0]+re.sub('[וי]','',w[1:]) for w in t.split(' ') if w)
GV=dict(zip('אבגדהוזחטיכלמנסעפצקרשת',[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400])); GV.update({'ך':20,'ם':40,'ן':50,'ף':80,'ץ':90})
def gm(t):
    t=re.sub(r'["\'׳״]','',t)
    return sum(GV[c] for c in t) if t and all(c in GV for c in t) else 0
HEB=lambda n:''.join(['ת'*(n//400)]+[{0:'',100:'ק',200:'ר',300:'ש'}[(n%400)//100*100]]+([{15:'טו',16:'טז'}[n%100]] if n%100 in (15,16) else [{0:'',10:'י',20:'כ',30:'ל',40:'מ',50:'נ',60:'ס',70:'ע',80:'פ',90:'צ'}[(n%100)//10*10],{0:'',1:'א',2:'ב',3:'ג',4:'ד',5:'ה',6:'ו',7:'ז',8:'ח',9:'ט'}[n%10]]))
BOOKS=['בראשית','שמות','ויקרא','במדבר','דברים','יהושע','שופטים','שמואל א','שמואל ב','מלכים א','מלכים ב','ישעיה','ירמיה','יחזקאל','הושע','יואל','עמוס','עובדיה','יונה','מיכה','נחום','חבקוק','צפניה','חגי','זכריה','מלאכי','תהלים','משלי','איוב','שיר השירים','רות','איכה','קהלת','אסתר','דניאל','עזרא','נחמיה','דברי הימים א','דברי הימים ב']
CH={'בראשית':50,'שמות':40,'ויקרא':27,'במדבר':36,'דברים':34,'יהושע':24,'שופטים':21,'שמואל א':31,'שמואל ב':24,'מלכים א':22,'מלכים ב':25,'ישעיה':66,'ירמיה':52,'יחזקאל':48,'הושע':14,'יואל':4,'עמוס':9,'עובדיה':1,'יונה':4,'מיכה':7,'נחום':3,'חבקוק':3,'צפניה':3,'חגי':2,'זכריה':14,'מלאכי':3,'תהלים':150,'משלי':31,'איוב':42,'שיר השירים':8,'רות':4,'איכה':5,'קהלת':12,'אסתר':10,'דניאל':12,'עזרא':10,'נחמיה':13,'דברי הימים א':29,'דברי הימים ב':36}
ALIAS={'ישעיהו':'ישעיה','ירמיהו':'ירמיה','תלים':'תהלים','תהילים':'תהלים','שה"ש':'שיר השירים','שיר':'שיר השירים','ש"א':'שמואל א','ש"ב':'שמואל ב','שמואל-א':'שמואל א','מ"א':'מלכים א','מ"ב':'מלכים ב','דה"א':'דברי הימים א','דה"ב':'דברי הימים ב','דהי"א':'דברי הימים א','דהי"ב':'דברי הימים ב'}
# --- התנ"ך שבאפליקציה: ספר -> פרק -> [(פסוק, טקסט, פרשה)]
B=D['books']; bmap={}
for i,b in enumerate(B):
    if not b: continue
    t=nq(b.get('title',''))
    if b.get('cat')=='tanach' and '·' not in t and t in BOOKS: bmap[i]=t
bmap[17]='תהלים'
TV=collections.defaultdict(lambda:collections.defaultdict(list)); RAW={}
for i,v in enumerate(D['vi']):
    if v in bmap:
        mm=re.match(r'\s*פרק\s+([א-ת"\'׳״]+)',D['ch'][i]); ch=gm(mm.group(1)) if mm else 0
        if not ch: continue
        bk=bmap[v]; vs=len(TV[bk][ch])+1
        TV[bk][ch].append((vs,' '+nn(D['T'][i])+' ',D['sec'][i] if D['sec'][i].startswith('פרשת') else '',D['T'][i]))
print('tanach books in app:',len(TV))
def find_in(bk,ch,q):
    """מחזיר רשימת (פרק,פסוק) שבהם מופיע הציטוט"""
    if bk not in TV or not q: return []
    qw=q.split(' '); qs=' '+q+' '; qk=' '+skel(q)+' '
    chs=[ch] if ch and ch in TV[bk] else []
    out=[]
    for pass_ in (chs, [c for c in TV[bk] if c!=ch]):
        for c in pass_:
            for vs,t,ps,_ in TV[bk][c]:
                ok = qs in t or qk in ' '+skel(t.strip())+' '
                if not ok and len(qw)>=2:
                    pos=0; ok=True
                    for w in qw:
                        j=t.find(' '+w+' ',pos)
                        if j<0 or (pos and j-pos>60): ok=False;break
                        pos=j+len(w)+1
                if ok: out.append((c,vs))
        if out: return out
    # ציטוט שנמשך על שני פסוקים: מנסים חצי ראשון
    if len(qw)>=4: return find_in(bk,ch,' '.join(qw[:len(qw)//2]))
    return []
def item_text(r):
    it=lm[r[0]]['c'][r[1]]['i'][r[2]]
    return ' '.join(re.sub(r'<[^>]+>','',b[1]) for b in it['b'] if isinstance(b,list) and len(b)>1 and isinstance(b[1],str) and b[0] not in SK)
PAREN=re.compile(r'\(([^()]{2,60})\)')
def parse_ref(s):
    s=nq(s).replace("''",'"').replace('״','"').replace('׳',"'").strip()
    s=re.sub(r'^(עיין|ועיין|עין|ועין|ע\')\s+','',s)
    for name in sorted(list(BOOKS)+list(ALIAS),key=len,reverse=True):
        if s.startswith(name+' ') or s.startswith(name+','):
            bk=ALIAS.get(name,name); rest=s[len(name):].strip(' ,')
            if re.match(r'^(רבה|רבא|ר"|רבתי|זוטא)',rest): return ('MIDRASH',bk,None,None)
            m=re.match(r'^([א-ת"\']{1,6})(?:\s*,\s*([א-ת"\']{1,5}))?(?:\s|$|[;.,])',rest)
            if not m: return (None,bk,None,None)
            c=gm(m.group(1)); v=gm(m.group(2)) if m.group(2) else None
            if not c or c>CH.get(bk,999): return (None,bk,c,v)
            return ('OK',bk,c,v)
    return (None,None,None,None)
def title_book(t):
    t=nq(t)
    for b in sorted(BOOKS,key=len,reverse=True):
        if t.startswith(b+' '): return b,t[len(b)+1:]
    return None,t
# --- מעבר על כל ההפניות (החלק לפי פרשות/ספרים מכיל את כולן)
stat=collections.Counter(); recs=[]; logs=collections.defaultdict(list)
for s in src:
    if s['id'].startswith('xtt'): continue
    for c in s['c']:
        tb,rest=title_book(c['t'])
        for r in c['irefs']:
            txt=item_text(r); sn=nq(txt[r[5]:r[6]]) if r[5] is not None else nq(txt)
            q=nn(r[7] or '')
            cands=[]
            for m in PAREN.finditer(sn):
                p=parse_ref(m.group(1))
                if p[1]==tb: cands.append((m.start(),m.end(),p))
            qpos=-1
            if q:
                sk=nn(sn); # position approx in nq text
                i=nq(sn).find(nq(r[7] or '').split(' ')[0]) if r[7] else -1; qpos=i
            pick=None
            if cands:
                if qpos>=0:
                    before=[x for x in cands if x[1]<=qpos+2]
                    pick=(before[-1] if before else min(cands,key=lambda x:abs(x[0]-qpos)))
                else: pick=cands[0]
            q_ex=''
            if not q and pick:
                mq=re.match(r"\s*:?\s*''([^']{3,90}?)''",sn[pick[1]:])
                if mq: q_ex=mq.group(1).strip(); q=nn(q_ex); stat['quote_from_snippet']+=1
            if pick and pick[2][0]=='MIDRASH': stat['midrash_dropped']+=1; logs['midrash'].append((c['t'],r[3])); continue
            ch=vs=None
            if pick and pick[2][0]=='OK': ch,vs=pick[2][2],pick[2][3]; stat['from_paren']+=1
            else:
                # בלי סוגריים תואמים: מפרשים את הכותרת הישנה (י, ב = י"ב)
                j=gm(re.sub(r'[,\s]','',rest)); f=gm(rest.split(',')[0].strip())
                ch = j if j and j<=CH.get(tb,999) else (f if f and f<=CH.get(tb,999) else None)
                stat['from_title']+=1
                if not ch and q:
                    h=find_in(tb,0,q) if tb in TV else []
                    if not h:
                        for ob in TV:
                            h2=find_in(ob,0,q)
                            if h2 and len(q.split(' '))>=3: tb=ob; h=h2; stat['book_changed_by_quote']+=1; break
                    if h: ch=h[0][0]; stat['resolved_by_quote']+=1
                if not ch: stat['unresolved_dropped']+=1; logs['unresolved'].append((c['t'],r[7],r[3])); continue
            # אימות מול התנ"ך
            if tb in TV:
                hits=find_in(tb,ch,q) if q else []
                if hits:
                    same=[h for h in hits if h[0]==ch]
                    if same: ch,vs2=same[0]; vs=vs or vs2; stat['verified_verse']+=1
                    else: logs['moved'].append((tb,ch,'->',hits[0],r[7])); ch,vs=hits[0]; stat['moved_by_quote']+=1
                elif q: stat['quote_not_found']+=1
                else: stat['no_quote']+=1
            else: stat['book_not_in_app']+=1
            recs.append(dict(bk=tb,ch=ch,vs=vs,r=r,txt=txt,qx=q_ex))
print(dict(stat)); print('records',len(recs))
# --- קיצור הקטע סביב הציטוט (מיפוי בין טקסט בלי ניקוד לטקסט המקורי)
def shorten(rec):
    r=rec['r']; txt=rec['txt']; a,b=(r[5] or 0),(r[6] or len(txt))
    idx=[k for k,ch in enumerate(txt) if not NQ.match(ch)]; plain=''.join(txt[k] for k in idx)
    pa=sum(1 for k in idx if k<a); pb=sum(1 for k in idx if k<b)
    q=nq(r[7] or '').strip()
    p=plain.find(q[:25],pa,pb) if q else -1
    if p<0:
        m=None
        for mm in PAREN.finditer(plain,pa,pb):
            pr=parse_ref(mm.group(1))
            if pr[1]==rec['bk']: m=mm;break
        p=m.start() if m else pa
    s_=max(pa,p-170); e_=min(pb,p+max(len(q),40)+190)
    while s_>pa and plain[s_-1]!=' ': s_-=1
    while e_<pb and plain[e_]!=' ': e_+=1
    oa=idx[s_] if s_<len(idx) else a; ob=idx[e_] if e_<len(idx) else len(txt)
    return oa,ob,(1 if oa>0 else 0),(1 if ob<len(txt.rstrip()) else 0)
PAR=['בראשית','נח','לך לך','וירא','חיי שרה','תולדות','ויצא','וישלח','וישב','מקץ','ויגש','ויחי','שמות','וארא','בא','בשלח','יתרו','משפטים','תרומה','תצוה','כי תשא','ויקהל','פקודי','ויקרא','צו','שמיני','תזריע','מצורע','אחרי מות','קדושים','אמור','בהר','בחקתי','במדבר','נשא','בהעלתך','שלח לך','קרח','חקת','בלק','פינחס','מטות','מסעי','דברים','ואתחנן','עקב','ראה','שופטים','כי תצא','כי תבוא','נצבים','וילך','האזינו','וזאת הברכה']
TORAH=BOOKS[:5]
def parsha(bk,ch,vs):
    if bk not in TORAH or bk not in TV or ch not in TV[bk]: return None
    L=TV[bk][ch]; v=vs if vs and vs<=len(L) else 1
    p=L[v-1][2].replace('פרשת ','').strip()
    return p or None
def vtitle(bk,ch,vs):
    t=bk+' '+HEB(ch)+(', '+HEB(vs) if vs else '')
    if vs and bk in TV and ch in TV[bk] and vs<=len(TV[bk][ch]):
        w=nq(TV[bk][ch][vs-1][3]).replace('־',' ').split()
        t+=' – '+' '.join(w[:6]).rstrip(':,;.')+('…' if len(w)>6 else '')
    return t
groups=collections.OrderedDict()
for rec in recs:
    sec = parsha(rec['bk'],rec['ch'],rec['vs']) if rec['bk'] in TORAH else rec['bk']
    if rec['bk'] in TORAH and not sec: sec=rec['bk']; stat['torah_no_parsha']+=1
    rec['sec']=sec
order={('P',p):i for i,p in enumerate(PAR)}; order.update({('B',b):100+i for i,b in enumerate(BOOKS)})
def skey(rec): return order.get(('P',rec['sec']), order.get(('B',rec['sec']),999))
BI={b:i for i,b in enumerate(BOOKS)}
recs.sort(key=lambda x:(skey(x),BI[x['bk']],x['ch'],x['vs'] or 999,x['r'][0],x['r'][1],x['r'][2],x['r'][5] or 0))
out=[]; secmap={}
for rec in recs:
    sname=('פרשת '+rec['sec']) if rec['sec'] in PAR else rec['sec']
    if sname not in secmap:
        secmap[sname]={'id':'xtm%d'%len(secmap),'short':sname,'g':'V52','c':[]}; out.append(secmap[sname])
    S=secmap[sname]; t=vtitle(rec['bk'],rec['ch'],rec['vs'])
    if not S['c'] or S['c'][-1]['t']!=t: S['c'].append({'t':t,'irefs':[]})
    a,b,pre,post=shorten(rec); r=rec['r']
    q=r[7] or rec.get('qx') or ''
    if not q and rec['vs'] and rec['bk'] in TV:
        w=nq(TV[rec['bk']][rec['ch']][rec['vs']-1][3]).replace('־',' ').split(); q=' '.join(w[:8]).rstrip(':,;.')+('…' if len(w)>8 else ''); stat['quote_filled']+=1
    ir=[r[0],r[1],r[2],r[3],r[4],a,b,q,pre,post]
    if any(x[3]==ir[3] and x[5]==ir[5] for x in S['c'][-1]['irefs']): stat['dup_removed']+=1; continue
    S['c'][-1]['irefs'].append(ir)
    rec['ir']=ir; rec['vt']=t
# --- החלק לפי סדר התורות
for sid,lbl,xid in [('v0g0','חלק א׳','xtt0'),('v0g1','חלק ב׳','xtt1')]:
    by=collections.defaultdict(list)
    for rec in recs:
        if 'ir' in rec and rec['r'][0]==sid: by[rec['r'][1]].append(rec)
    S={'id':xid,'short':lbl,'g':'V52','c':[]}
    for ci in sorted(by):
        L=sorted(by[ci],key=lambda x:(x['r'][2],x['ir'][5]))
        ir=[]
        for x in L:
            y=list(x['ir']); lab=x['vt'].split(' – ')[0]
            al=x['r'][4].split('· אות ')[-1] if '· אות ' in x['r'][4] else ''
            y[4]=lab+(' · אות '+al if al else '')
            ir.append(y)
        S['c'].append({'t':lm[sid]['c'][ci]['t'],'irefs':ir})
    out.append(S)
print(dict(stat))
print('sections',len(out),'chapters',sum(len(s['c']) for s in out),'refs',sum(len(c['irefs']) for s in out for c in s['c']))
miss=[p for p in PAR if 'פרשת '+p not in secmap]; print('parshiyot missing:',miss)
data=json.dumps(out,ensure_ascii=False,separators=(',',':'))
h=hashlib.md5(data.encode()).hexdigest()[:10]; fn=re.sub(r'\.[0-9a-f]{10}\.json$','.%s.json'%h,OLD.split('/')[-1])
open('/home/claude/content/out6/'+fn,'w',encoding='utf-8').write(data)
json.dump(logs,open('/home/claude/content/out6/fix52_log.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(fn,len(data))
