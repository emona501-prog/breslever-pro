# ספרי ברסלב חדשים מקבצי docx (תוכן עניינים בפסקה 2, כותרות לפי התאמה לתוכן העניינים)
import pickle,re,json,html,os,hashlib
A=pickle.load(open('bres.pkl','rb'))
OUT='out2'; os.makedirs(OUT,exist_ok=True)
esc=lambda t: html.escape(t,quote=False)
NUM=re.compile(r'^(?:[א-ת]{1,2} ?- ?[א-ת]{1,4}|[א-ת]{1,4}\.)$')
def walk(fid,skip_first_toc=True):
    """-> רשימת אירועים: ('h',level,text) / ('p',[lines])"""
    P=A[fid]
    toc=[(len(l)-len(l.lstrip(' \xa0'))>0, l.strip(' \xa0')) for l in P[2]['t'].split('\n') if l.strip(' \xa0')]
    ptr=0; ev=[]
    for p in P[3:]:
        lines=[l.strip(' \xa0') for l in p['t'].split('\n')]; lines=[l for l in lines if l]
        if not lines: continue
        hit=None
        for k in range(ptr,min(ptr+4,len(toc))):
            if toc[k][1]==lines[0]: hit=k; break
        if hit is not None:
            ev.append(('h',1 if toc[hit][0] else 0,lines[0])); ptr=hit+1; lines=lines[1:]
            # כותרות רצופות באותה פסקה
            while lines and ptr<len(toc) and toc[ptr][1]==lines[0]:
                ev.append(('h',1 if toc[ptr][0] else 0,lines[0])); ptr+=1; lines=lines[1:]
        if lines: ev.append(('p',lines))
    return ev,len(toc),ptr
def items_numbered(ev,title):
    """כותרות ממוספרות = קטעים; שאר הכותרות = פרקים. -> chapters"""
    chs=[]; cur=None; it=None
    def newch(t):
        nonlocal cur,it; cur={'t':t,'i':[]}; chs.append(cur); it=None
    for e in ev:
        if e[0]=='h':
            if NUM.match(e[2]):
                if cur is None: newch(title)
                it={'n':e[2].rstrip('.'),'b':[]}; cur['i'].append(it)
            else:
                if e[2]==title or re.sub(r'[-, ]','',e[2])==re.sub(r'[-, ]','',title): continue
                newch(e[2])
        else:
            if cur is None: newch(title)
            if it is None: it={'n':'','b':[]}; cur['i'].append(it)
            for l in e[1]: it['b'].append(['p',esc(l)])
            if not it['n']: it=None
    chs=[c for c in chs if c['i']]
    out=[]
    for c in chs:  # פיצול פרקים ארוכים
        nums=[x for x in c['i']]
        if len(nums)<=30: out.append(c); continue
        for a in range(0,len(nums),25):
            part=nums[a:a+25]; f=next((x['n'] for x in part if x['n']),''); l=next((x['n'] for x in reversed(part) if x['n']),'')
            out.append({'t':c['t']+(' · '+f+' – '+l if f else ' · המשך'),'i':part})
    return out
def two_level(ev,flat0=False):
    """level0=חלק, level1=פרק. flat0: חלק יחיד, level0=פרק, level1=כותרת פנימית"""
    secs=[]; sec=None; ch=None
    def newsec(t):
        nonlocal sec,ch; sec={'short':t,'c':[]}; secs.append(sec); ch=None
    def newch(t):
        nonlocal ch
        if sec is None: newsec(t)
        ch={'t':t,'i':[]}; sec['c'].append(ch)
    pend=None
    for e in ev:
        if e[0]=='h':
            if flat0:
                if e[1]==0: newch(e[2])
                else: pend=e[2]
            else:
                if e[1]==0: newsec(e[2])
                else: newch(e[2])
        else:
            if ch is None: newch(sec['short'] if sec else 'פתיחה')
            b=([['h',esc(pend)]] if pend else [])+[['p',esc(l)] for l in e[1]]; pend=None
            ch['i'].append({'n':'','b':b})
    for s in secs: s['c']=[c for c in s['c'] if c['i']]
    return [s for s in secs if s['c']]
def flat(ev,title,per_line=False):
    chs=[]; ch=None
    for e in ev:
        if e[0]=='h': ch={'t':e[2],'i':[]}; chs.append(ch)
        else:
            if ch is None: ch={'t':'פתיחה','i':[]}; chs.append(ch)
            if per_line: ch['i']+=[{'n':'','b':[['p',esc(l)]]} for l in e[1]]
            else: ch['i'].append({'n':'','b':[['p',esc(l)] for l in e[1]]})
    return [{'short':title,'c':[c for c in chs if c['i']]}]
W=lambda ch,ch1,it,it1,nx,pv,sec='חלקים',sec1='חלק': {"group":"","sections":sec,"section":sec1,"chapters":ch,"chapterOne":ch1,"items":it,"item":it1,"next":nx,"prev":pv}
def cfg(title,nq,author,cat,bg,art,plan,words,**kw):
    d={"title":title,"titleNiqud":nq,"author":author,"pre2":"סֵפֶר","heroSize":38,"bg":bg,"heroArt":art,"planWord":plan,"cat":cat,"words":words}; d.update(kw); return d
vols=[]
# שיח שרפי קודש – 6 חלקים
secs=[]
for fid,nm in [('e9018675','חלק א'),('e5117c29','חלק ב'),('4e793967','חלק ג'),('21cf94d1','חלק ד'),('9ebac7d7','חלק ה'),('74d45582','חלק ו')]:
    ev,n,ptr=walk(fid); print(fid,'toc',n,'matched',ptr)
    secs.append({'short':nm,'c':items_numbered(ev,A[fid][2]['t'].strip().split('\n')[0].strip())})
vols.append((cfg('שיח שרפי קודש','שִׂיחַ שַׂרְפֵי קֹדֶשׁ','עַל פִּי שִׂיחוֹת רַבִּי לֵוִי יִצְחָק בֶּנְדֶּר זצ"ל','anash','jerusalem','chayei','שיחות',W('פרקים','פרק אחד','שיחות','שיחה','הפרק הבא','הפרק הקודם')),secs))
secs=[]
for fid,nm in [('c2a59434','חלק א'),('19862529','חלק ב')]:
    ev,n,ptr=walk(fid); print(fid,'toc',n,'matched',ptr)
    secs.append({'short':nm,'c':items_numbered(ev,'מכתבים')})
vols.append((cfg('אב"י הנחל','אִבֵּי הַנַּחַל','רַבִּי יִשְׂרָאֵל דֹּב אוֹדֶסֶר זצ"ל','anash','springs','lh','מכתבים',W('פרקים','פרק אחד','מכתבים','מכתב','הפרק הבא','הפרק הקודם')),secs))
ev,n,ptr=walk('6ab1da12'); print('tovot',n,ptr)
vols.append((cfg('טובות זכרונות','טוֹבוֹת זִכְרוֹנוֹת','רַבִּי אַבְרָהָם שְׁטֶרְנְהַרְץ זצ"ל','anash','dawn','chayei','סימנים',W('סימנים','סימן אחד','קטעים','קטע','הסימן הבא','הסימן הקודם')),flat(ev,'טובות זכרונות')))
ev,n,ptr=walk('a223d5f9'); print('rinat',n,ptr)
vols.append((cfg('רינת ציון','רִנַּת צִיּוֹן','רַבִּי אַבְרָהָם שְׁטֶרְנְהַרְץ זצ"ל','anash','jerusalem','biur','מאמרים',W('מאמרים','מאמר אחד','קטעים','קטע','המאמר הבא','המאמר הקודם')),flat(ev,'רינת ציון')))
ev,n,ptr=walk('96c3a208'); print('tzer',n,ptr)
vols.append((cfg('קונטרס הצירופים · המהדורה המורחבת','קוּנְטְרֵס הַצֵּרוּפִים','רַבִּי נָתָן בְּרַבִּי יְהוּדָה מִטְּבֶרְיָה זצ"ל','anash','stars','stars','אותיות',W('אותיות','אות אחת','צירופים','צירוף','האות הבאה','האות הקודמת'),pre2='',heroSize=34,tag='הַמַּהֲדוּרָה הַמֻּרְחֶבֶת'),flat(ev,'קונטרס הצירופים',per_line=True)))
T='רַבִּי נַחְמָן מִטְּשֶׁעהְרִין זצ"ל'
for fid,title,nq,mode,bg,art in [('9ece6ebc','זמרת הארץ','זִמְרַת הָאָרֶץ','2','field','etzot'),('297b0d83','ירח האיתנים','יֶרַח הָאֵיתָנִים','f','dawn','biur'),('e67f01fa','יקרא דשבתא','יְקָרָא דְּשַׁבְּתָא','2','jerusalem','tefilot'),('516402f6','נחת השולחן','נַחַת הַשֻּׁלְחָן','2','sky','even'),('6fabce53','רמזי המעשיות','רִמְזֵי הַמַּעֲשִׂיּוֹת','1','forest','voyage')]:
    ev,n,ptr=walk(fid); print(title,'toc',n,'matched',ptr)
    if mode=='2': secs=two_level(ev)
    elif mode=='f': secs=[{'short':title,'c':sum((s['c'] for s in two_level(ev,True)),[])}]
    else: secs=flat(ev,title)
    vols.append((cfg(title,nq,T,'tcherin',bg,art,'סימנים',W('סימנים','סימן אחד','קטעים','קטע','הסימן הבא','הסימן הקודם')),secs))
VOL0=110; man=[]
for k,(c,secs) in enumerate(vols):
    vi=VOL0+k
    secs=[{'id':'v%dg%d'%(vi,si),'short':s['short'],'g':'V%d'%vi,'c':s['c']} for si,s in enumerate(secs)]
    js=json.dumps(secs,ensure_ascii=False,separators=(',',':'))
    fn='b%02d_V%d.%s.json'%(vi-2,vi,hashlib.md5(js.encode()).hexdigest()[:10]); open(OUT+'/'+fn,'w',encoding='utf-8').write(js)
    man.append({'vi':vi,'cfg':c,'file':fn})
    print(vi,c['title'],'| sections',[(s['short'][:18],len(s['c']),sum(len(x['i']) for x in s['c'])) for s in secs][:7],len(js)//1024,'KB')
json.dump(man,open(OUT+'/manifest_bres.json','w',encoding='utf-8'),ensure_ascii=False)
