# שולחן ערוך (4 חלקים) + באר היטב כמפרש + לקט "חשיבות לימוד ההלכה" (מתוך ספרי האפליקציה, מילה במילה)
import pickle,json,hashlib,os,re,html
R=pickle.load(open('sa.pkl','rb'))
OUT='out4'; os.makedirs(OUT+'/mg',exist_ok=True)
esc=lambda t: html.escape(t,quote=False)
CRED='הטקסט: תוכנת "תורת אמת" (toratemetfreeware.com), רישיון CC BY-NC-SA 2.5 – לשימוש לא מסחרי בלבד.'
W={"sections":"הלכות","section":"הלכות","chapters":"סימנים","chapterOne":"סימן אחד","items":"סעיפים","item":"סעיף","next":"הסימן הבא","prev":"הסימן הקודם"}
def cfg(title,nq,tag,**kw):
    d={"title":title,"titleNiqud":nq,"author":"מָרָן רַבִּי יוֹסֵף קָארוֹ וְהָרְמָ\"א","tag":tag,"pre2":"שֻׁלְחָן עָרוּךְ","heroSize":38,"bg":"jerusalem","heroArt":"even","planWord":"סימנים","cat":"sa","words":W,"credit":CRED}; d.update(kw); return d
vols=[]
for fid,title,nq in [('6f18e94e','אורח חיים','אֹרַח חַיִּים'),('8b3829b6','יורה דעה','יוֹרֶה דֵעָה'),('b9217579','אבן העזר','אֶבֶן הָעֵזֶר'),('6ad736fc','חושן משפט','חֹשֶׁן מִשְׁפָּט')]:
    secs=R[fid]; hasbh=any('bh' in i for s in secs for c in s['c'] for i in c['i'])
    vols.append((cfg('שולחן ערוך · '+title,nq,'עִם בְּאֵר הֵיטֵב' if hasbh else 'שֻׁלְחָן עָרוּךְ',base=title,sa=1),secs,hasbh))
# לקט
s=open('/home/claude/src/shell.html',encoding='utf-8').read()
urls=json.loads(re.search(r'window\.BOOK_DATA_URLS=(\[.*?\])',s).group(1))
c=json.loads(re.search(r'<script type="application/json" id="bookcfg">(.*?)</script>',s,re.S).group(1))
allb=[]; IT={}
for u in urls:
    d=json.load(open('/home/claude/breslever-pro/www/'+u,encoding='utf-8'))
    for sc in d:
        for ci,ch in enumerate(sc.get('c',[])):
            for ii,it in enumerate(ch.get('i',[])):
                b=it.get('b')
                if isinstance(b,dict) and '@' in b: it['b']=allb[b['@']]
                else: allb.append(b)
                IT['%s.%d.%d'%(sc['id'],ci,ii)]=(it,sc,ch)
strip=lambda t: re.sub('[֑-ׇ]','',re.sub(r'<[^>]+>','',t))
PICK=[('דברי רבנו ז"ל',[('v8g0.184.*','שיחות הר"ן · שיחה קפה'),('v0g0.9.6','ליקוטי מוהר"ן חלק א · תורה ח, אות ו'),('v11g2.26.61','ליקוטי עצות · תלמוד תורה, אות סב')]),
      ('דברי רבי נתן ז"ל',[('v47g2.5.0','עלים לתרופה · מכתב יד'),('v47g2.10.25','עלים לתרופה · מכתב פד'),('v47g2.13.22','עלים לתרופה · מכתב קעה'),('v110g0.8.7','שיח שרפי קודש חלק א · א-קסח'),('v19g1.33.60','ביאור הליקוטים · בשם מוהרנ"ת')]),
      ('מספרי התלמידים',[('v16g2.28.0','השתפכות הנפש · אות לא'),('v16g3.12.0','השתפכות הנפש · אות סא'),('v44g2.0.11','אמונת עתך · סדר היום, אות יא'),('v47g5.0.0','מכתבי מוהרנ"ט · מכתב א')])]
chs=[]
for title,lst in PICK:
    its=[]
    for key,src in lst:
        keys=[k for k in IT if k.startswith(key[:-1])] if key.endswith('*') else [key]
        keys=sorted(keys,key=lambda k:int(k.split('.')[-1]))
        for k in keys:
            it,sc,ch=IT[k]
            b=[x for x in it['b'] if isinstance(x,list) and x and x[0] in ('p','h','b')]
            its.append({'n':'','b':b+[['go','📖 למקור: '+src,k]]})
        print(src,len(keys),strip(' '.join(x[1] for x in IT[keys[0]][0]['b'] if isinstance(x,list)))[:70])
    chs.append({'t':title,'i':its})
vols.append(({"title":"חשיבות לימוד ההלכה","titleNiqud":"חֲשִׁיבוּת לִמּוּד הַהֲלָכָה","author":"לֶקֶט מִדִּבְרֵי רַבֵּנוּ וְתַלְמִידָיו","tag":"שֻׁלְחָן עָרוּךְ בְּכָל יוֹם","pre2":"","heroSize":34,"bg":"dawn","heroArt":"etzot","planWord":"דיבורים","cat":"sa","words":{"sections":"חלקים","section":"חלק","chapters":"פרקים","chapterOne":"פרק אחד","items":"דיבורים","item":"דיבור","next":"הפרק הבא","prev":"הפרק הקודם"}},[{'short':'חשיבות לימוד ההלכה','c':chs}],False))
VOL0=136; man=[]
for k,(cf,secs,hasbh) in enumerate(vols):
    vi=VOL0+k; mg={}
    out=[]
    for si,sc in enumerate(secs):
        cs=[]
        for ci,ch in enumerate(sc['c']):
            its=[]
            for ii,it in enumerate(ch['i']):
                if it.get('bh'): mg['%d.%d.%d'%(si,ci,ii)]=[[0,'<br>'.join(esc(x) for x in it['bh'])]]
                its.append({'n':it['n'],'b':it['b']})
            cs.append({'t':ch['t'],'i':its})
        out.append({'id':'v%dg%d'%(vi,si),'short':sc['short'],'g':'V%d'%vi,'c':cs})
    js=json.dumps(out,ensure_ascii=False,separators=(',',':'))
    fn='b%02d_V%d.%s.json'%(vi-2,vi,hashlib.md5(js.encode()).hexdigest()[:10]); open(OUT+'/'+fn,'w',encoding='utf-8').write(js)
    if mg:
        mj=json.dumps({'n':['באר היטב'],'c':mg},ensure_ascii=False,separators=(',',':'))
        mfn='mg/V%d.%s.json'%(vi,hashlib.md5(mj.encode()).hexdigest()[:8]); open(OUT+'/'+mfn,'w',encoding='utf-8').write(mj); cf['mg']=mfn
    man.append({'vi':vi,'cfg':cf,'file':fn}); print(vi,cf['title'],len(js)//1024,'KB',('mg %dKB'%(len(mj)//1024)) if mg else '')
json.dump(man,open(OUT+'/manifest_sa.json','w',encoding='utf-8'),ensure_ascii=False)
