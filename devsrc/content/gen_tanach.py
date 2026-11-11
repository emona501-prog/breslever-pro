# מייצר כרכי תנ"ך: שמו"ת+רש"י (4 חומשים), מקראות גדולות (5), נביאים, כתובים. מפרשים בקבצים נפרדים (נטענים בלחיצה).
import pickle,re,json,html,os,hashlib
R=pickle.load(open('parsed.pkl','rb'))
OUT='out'; os.makedirs(OUT+'/mg',exist_ok=True)
TEAM=re.compile('[֑-ֽ֯]')
def plain(t): return re.sub(r'\s+',' ',TEAM.sub('',t).replace('-',' ').replace('־',' ')).strip()
def esc(t): return html.escape(t,quote=False).replace('\n','<br>')
HEB=['','א','ב','ג','ד','ה','ו','ז','ח','ט','י']
def chap_t(ch,rng=None): return 'פֶּרֶק '+ch+(' · פסוקים '+rng[0]+'–'+rng[1] if rng else '')
WORDS={"sections":"חלקים","section":"חלק","chapters":"פרקים","chapterOne":"פרק אחד","items":"פסוקים","item":"פסוק","next":"הפרק הבא","prev":"הפרק הקודם"}
CRED='הטקסט והמפרשים: תוכנת "תורת אמת" (toratemetfreeware.com), רישיון CC BY-NC-SA 2.5 – לשימוש לא מסחרי בלבד.'
VOL0=78
vols=[]  # (cfg, sections, mgdata|None)
def split_parshiot(r,first):
    # -> [(parsha, [(ch, verses, rng|None)])]
    marks=[(first,0,0)]+[(n,ci,vi) for n,ci,vi in r['parshiot']]
    res=[]
    for k,(name,ci,vi) in enumerate(marks):
        eci,evi=(marks[k+1][1],marks[k+1][2]) if k+1<len(marks) else (len(r['chs'])-1,len(r['chs'][-1]['v']))
        chs=[]
        for c in range(ci,eci+1):
            vs=r['chs'][c]['v']; a=vi if c==ci else 0; b=evi if c==eci else len(vs)
            if b<=a: continue
            part=vs[a:b]; rng=None if (a==0 and b==len(vs)) else (part[0]['n'],part[-1]['n'])
            chs.append((r['chs'][c]['ch'],part,rng))
        res.append((name,chs))
    return res
def add(cfg,secs,mg): vols.append((cfg,secs,mg))
CH=[('5daeb546','בראשית','סֵפֶר בְּרֵאשִׁית','רִאשׁוֹן'),('8758a269','שמות','סֵפֶר שְׁמוֹת','שֵׁנִי'),('4fc99d88','ויקרא','סֵפֶר וַיִּקְרָא','שְׁלִישִׁי'),('0315f37c','במדבר','סֵפֶר בְּמִדְבַּר','רְבִיעִי'),('9e200499','דברים','סֵפֶר דְּבָרִים','חֲמִישִׁי')]
# 1) שמו"ת + רש"י ל-4 חומשים: מקרא (עם טעמים), תרגום ועליות מקובצי "מקרא ותרגום"; רש"י מקובצי המקראות הגדולות
S=pickle.load(open('smt.pkl','rb'))
SMT={'שמות':'7fac3472','ויקרא':'27ebfb7f','במדבר':'ba104fed','דברים':'fd137603'}
for fid,name,nq,ordn in CH[1:]:
    r=R[fid]; q=S[SMT[name]]; secs=[]
    for ci,c in enumerate(q['chs']):
        assert len(c['v'])==len(r['chs'][ci]['v']),(name,ci)
        for vi,v in enumerate(c['v']): v['t']=v['mq']; v['mf']=r['chs'][ci]['v'][vi]['mf']
    q['parshiot']=[(n.replace('פרשת ',''),a,b_) for n,a,b_ in q['parsh']]
    for pn,chs in split_parshiot(q,q['toc'][0].replace('פרשת ','')):
        cs=[]
        for ch,vs,rng in chs:
            its=[]
            for v in vs:
                mf=dict(v['mf'])
                bl=[['p',plain(v['mq'])]]
                if v.get('al'): bl.insert(0,['sl',v['al'].split(' - ')[0].strip()])
                it={'n':v['n'],'b':bl,'mq':v['mq']}
                if v.get('tg'): it['tg']=v['tg']
                if mf.get('רש"י'): it['rs']='<span class="rs-s">'+esc(mf['רש"י'])+'</span>'
                its.append(it)
            cs.append({'t':chap_t(ch,rng),'i':its})
        secs.append({'short':'פרשת '+pn,'c':cs})
    add({"title":name,"titleNiqud":nq,"author":"חֲמִשָּׁה חֻמְשֵׁי תּוֹרָה","tag":"חֻמָּשׁ "+ordn+" · שְׁנַיִם מִקְרָא וְאֶחָד תַּרְגּוּם עִם רַשִׁ\"י","pre2":"","heroSize":40,"bg":"sky","heroArt":"torah","planWord":"פרקים","cat":"tanach","sub":"smt","tnx":1,"credit":CRED,
         "words":dict(WORDS,sections="פרשיות",section="פרשה")},secs,None)
def mgvol(r,title,nq,author,tag,sub,secs_spec,words,extra=None):
    names=[]; mg={}; secs=[]
    for si,(short,chs) in enumerate(secs_spec):
        cs=[]
        for ci,(ch,vs,rng) in enumerate(chs):
            its=[]
            for ii,v in enumerate(vs):
                its.append({'n':v['n'],'b':[['p',v['t']]]})
                row=[]
                for a,b in v['mf']:
                    if a not in names: names.append(a)
                    row.append([names.index(a),esc(b)])
                if row: mg['%d.%d.%d'%(si,ci,ii)]=row
            cs.append({'t':chap_t(ch,rng),'i':its})
        secs.append({'short':short,'c':cs})
    cfg={"title":title,"titleNiqud":nq,"author":author,"tag":tag,"pre2":"","heroSize":38,"bg":"sky","heroArt":"torah","planWord":"פרקים","cat":"tanach","sub":sub,"mg":1,"credit":CRED,"words":words}
    if extra: cfg.update(extra)
    add(cfg,secs,{'n':names,'c':mg})
# 2) מקראות גדולות – חומש
for fid,name,nq,ordn in CH:
    r=R[fid]
    mgvol(r,name+' · מקראות גדולות',nq,"חֻמָּשׁ מִקְרָאוֹת גְּדוֹלוֹת","חֻמָּשׁ "+ordn+" · עִם תַּרְגּוּמִים וּמְפָרְשִׁים","mg",
          [('פרשת '+pn,chs) for pn,chs in split_parshiot(r,name)],dict(WORDS,sections="פרשיות",section="פרשה"),{"nosearch":True,"base":name})
def whole(r): return [(c['ch'],c['v'],None) for c in r['chs']]
NEV=[('993bd9bf','יהושע','סֵפֶר יְהוֹשֻׁעַ'),('6c97214c','שופטים','סֵפֶר שׁוֹפְטִים'),('49f66db8','שמואל א','שְׁמוּאֵל א'),('0e681c2f','שמואל ב','שְׁמוּאֵל ב'),('3673ecfd','מלכים א','מְלָכִים א'),('1cb76dd4','מלכים ב','מְלָכִים ב'),('62b1389f','ישעיה','סֵפֶר יְשַׁעְיָה'),
     ('6a1489c0','עמוס','סֵפֶר עָמוֹס'),('89689f8b','עובדיה','סֵפֶר עֹבַדְיָה'),('b3251964','מיכה','סֵפֶר מִיכָה'),('291c82bc','נחום','סֵפֶר נַחוּם'),('1a8324fd','חבקוק','סֵפֶר חֲבַקּוּק'),('83109436','צפניה','סֵפֶר צְפַנְיָה'),('3b5c5903','חגי','סֵפֶר חַגַּי'),('4b5c104d','זכריה','סֵפֶר זְכַרְיָה'),('7b764065','מלאכי','סֵפֶר מַלְאָכִי')]
for fid,name,nq in NEV:
    r=R[fid]; mgvol(r,name,nq,"נְבִיאִים","נְבִיאִים · עִם מְפָרְשִׁים","nev",[(name,whole(r))],WORDS)
# 3) כתובים
r=R['88993b89']; ch=whole(r)
B=[('ספר ראשון',0,41),('ספר שני',41,72),('ספר שלישי',72,89),('ספר רביעי',89,106),('ספר חמישי',106,150)]
mgvol(r,'תהלים עם מפרשים','סֵפֶר תְּהִלִּים',"כְּתוּבִים","תְּהִלִּים · עִם רַשִׁ\"י, מְצוּדוֹת וּמַלְבִּי\"ם","ket",[(n,ch[a:b]) for n,a,b in B],WORDS)
KET=[('6031969f','משלי','סֵפֶר מִשְׁלֵי'),('673a10eb','שיר השירים · עם מפרשים','שִׁיר הַשִּׁירִים'),('c8707ebd','רות','מְגִלַּת רוּת'),('40366492','קהלת','מְגִלַּת קֹהֶלֶת'),('a9383329','עזרא','סֵפֶר עֶזְרָא'),('2460fdb4','נחמיה','סֵפֶר נְחֶמְיָה')]
for fid,name,nq in KET:
    r=R[fid]; mgvol(r,name,nq,"כְּתוּבִים","כְּתוּבִים · עִם מְפָרְשִׁים","ket",[(name.split(' · ')[0],whole(r))],WORDS,{"base":name.split(' · ')[0]} if ' · ' in name else None)
man=[]
for k,(cfg,secs,mg) in enumerate(vols):
    vi=VOL0+k
    for si,s in enumerate(secs): s['id']='v%dg%d'%(vi,si); s['g']='V%d'%vi
    secs=[{'id':s['id'],'short':s['short'],'g':s['g'],'c':s['c']} for s in secs]
    js=json.dumps(secs,ensure_ascii=False,separators=(',',':'))
    fn='b%02d_V%d.%s.json'%(vi-2,vi,hashlib.md5(js.encode()).hexdigest()[:10])
    open(OUT+'/'+fn,'w',encoding='utf-8').write(js)
    if mg:
        mj=json.dumps(mg,ensure_ascii=False,separators=(',',':'))
        mfn='mg/V%d.%s.json'%(vi,hashlib.md5(mj.encode()).hexdigest()[:8])
        open(OUT+'/'+mfn,'w',encoding='utf-8').write(mj); cfg['mg']=mfn
    man.append({'vi':vi,'cfg':cfg,'file':fn,'size':len(js),'mgsize':len(mj) if mg else 0})
    print(vi,cfg['title'],cfg['sub'],len(secs),'sec',len(js)//1024,'KB', ('mg %dKB %s'%(len(mj)//1024,','.join(mg['n']))) if mg else '')
json.dump(man,open(OUT+'/manifest_tanach.json','w',encoding='utf-8'),ensure_ascii=False)
print('total main',sum(m['size'] for m in man)//1024,'KB  mg',sum(m['mgsize'] for m in man)//1024,'KB')
