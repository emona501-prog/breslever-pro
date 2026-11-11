# הזוהר הקדוש: ארמית בכרך הראשי, לשון הקודש בקובץ נפרד (נטען לפי הצורך). + חיבורי הזוהר (ארמית בלבד).
import pickle,re,json,html,os,hashlib,glob
R=pickle.load(open('zo_raw.pkl','rb'))
OUT='out3'; os.makedirs(OUT+'/zh',exist_ok=True)
esc=lambda t: html.escape(t.strip(),quote=False).replace('\n','<br>')
DAF=re.compile(r"^דף ([א-ת'\"]+) ע''([אב])$")
CRED='הטקסט והתרגום ללשון הקודש: "הזוהר המתורגם" מתוך תוכנת "תורת אמת" (toratemetfreeware.com), רישיון CC BY-NC-SA 2.5 – לשימוש לא מסחרי בלבד.'
HL=['א','ב','ג','ד','ה','ו','ז','ח','ט','י','יא','יב','יג','יד','טו','טז','יז','יח','יט','כ','כא','כב','כג','כד','כה','כו','כז','כח','כט','ל','לא','לב','לג','לד','לה','לו','לז','לח','לט','מ']
def te(fid,deftitle):
    P=R[fid]
    toc=[]; start=0
    for k,(s,b,t) in enumerate(P[:8]):
        if '\xa0\xa0\xa0' in t: toc=[x.strip() for x in t.split('\xa0\xa0\xa0') if x.strip()]; start=k+1
    # דילוג על שורות תוכן העניינים (N קצרות) ועל שורת הכותרת
    while start<len(P) and (P[start][0]=='N' and P[start][2].strip() in toc): start+=1
    if not toc:
        start=next(k for k,(s,b,t) in enumerate(P) if b and 'הזוהר' in t)+1
    secs=[]; sec=None; ch=None; it=None; ptr=0; pend=[]; curdaf=None
    def newsec(t):
        nonlocal sec,ch,curdaf; sec={'short':t,'c':[]}; secs.append(sec); ch=None; curdaf=None
    def newch(t):
        nonlocal ch
        if sec is None: newsec(deftitle)
        ch={'t':t,'i':[]}; sec['c'].append(ch)
    for s,b,t in P[start:]:
        st=t.strip()
        if s=='W':
            hit=None
            for k in range(ptr,min(ptr+5,len(toc))):
                if toc[k]==st: hit=k; break
            if hit is not None: newsec(st); ptr=hit+1; it=None; continue
            if b and 'הזוהר המתורגם' in st: continue
            m=DAF.match(st)
            if m:
                if m.group(1)!=curdaf: curdaf=m.group(1); newch('דף '+curdaf)
                pend.append(['sl',st]); it=None; continue
            if ch is None: newch('פתיחה' if curdaf is None and toc else (sec['short'] if sec else deftitle))
            it={'n':'','b':pend+[['p',esc(t)]]}; pend=[]; ch['i'].append(it)
        else:
            if it is None or 'he' in it and False:
                if ch is None: newch(sec['short'] if sec else deftitle)
                it={'n':'','b':pend+[['p',esc(t)]]}; pend=[]; ch['i'].append(it); it=None
            else:
                it['he']=(it['he']+'<br>' if 'he' in it else '')+esc(t)
    # פרקים בלי דפים – פיצול למקטעים של 20
    for s_ in secs:
        out=[]
        for c in s_['c']:
            if c['t'].startswith('דף ') or len(c['i'])<=30: out.append(c); continue
            for a in range(0,len(c['i']),20): out.append({'t':(c['t'] if c['t']!='פתיחה' else s_['short'])+' · '+HL[(a//20)%len(HL)]+("'" if a//20<len(HL) else ''),'i':c['i'][a:a+20]})
        s_['c']=[c for c in out if c['i']]
    return [s_ for s_ in secs if s_['c']]
def small(fid,title):
    P=R[fid]; chs=[]; ch=None
    for s,b,t in P:
        st=t.strip()
        if s=='H' or st=='כל הספרים': continue
        if b and len(st)<90: ch={'t':st.rstrip(':'),'i':[]}; chs.append(ch); continue
        if ch is None: ch={'t':title,'i':[]}; chs.append(ch)
        ch['i'].append({'n':'','b':[['p',esc(t)]]})
    return [{'short':title,'c':[c for c in chs if c['i']]}]
W={"sections":"פרשיות","section":"פרשה","chapters":"דפים","chapterOne":"דף אחד","items":"קטעים","item":"קטע","next":"הדף הבא","prev":"הדף הקודם"}
W2=dict(W,sections="חלקים",section="חלק",chapters="פרקים",chapterOne="פרק אחד",next="הפרק הבא",prev="הפרק הקודם")
def cfg(title,nq,tag,sub,words,**kw):
    d={"title":title,"titleNiqud":nq,"author":"רַבִּי שִׁמְעוֹן בַּר יוֹחַאי","tag":tag,"pre2":"","heroSize":36,"bg":"stars","heroArt":"stars","planWord":"דפים","cat":"zohar","sub":sub,"words":words}; d.update(kw); return d
vols=[]
T='הַזֹּהַר הַקָּדוֹשׁ · אֲרָמִית וּלְשׁוֹן הַקֹּדֶשׁ'
for fid,title,nq,w in [('2eb69f45','הקדמת ספר הזוהר','הַקְדָּמַת סֵפֶר הַזֹּהַר',W2),('cea90f96','זוהר · בראשית','זֹהַר · בְּרֵאשִׁית',W),('b2a11294','זוהר · שמות','זֹהַר · שְׁמוֹת',W),('dbaac9ed','זוהר · ויקרא','זֹהַר · וַיִּקְרָא',W),('ebf07bf7','זוהר · במדבר','זֹהַר · בְּמִדְבַּר',W),('70a0cfb4','זוהר · דברים','זֹהַר · דְּבָרִים',W),('ddb25184','זוהר חדש','זֹהַר חָדָשׁ',W2)]:
    secs=te(fid,title); nhe=sum(1 for s in secs for c in s['c'] for i in c['i'] if 'he' in i); n=sum(len(c['i']) for s in secs for c in s['c'])
    vols.append((cfg(title,nq,T if nhe else 'הַזֹּהַר הַקָּדוֹשׁ','zohar',w,zh=1 if nhe else 0,credit=CRED),secs))
    print(title,'sections',len(secs),'chapters',sum(len(s['c']) for s in secs),'items',n,'with he',nhe)
for fid,title,nq in [('c8cb521e','ספרא דצניעותא','סִפְרָא דִּצְנִיעוּתָא'),('6738f99e','פירוש הגר"א לספרא דצניעותא','פֵּרוּשׁ הַגְּרָ"א לְסִפְרָא דִּצְנִיעוּתָא'),('275e4933','אדרא זוטא','אִדְּרָא זוּטָא'),('ef28194c','רעיא מהימנא','רַעְיָא מְהֵימְנָא'),('e2fbfcfb','מדרש הנעלם','מִדְרַשׁ הַנֶּעְלָם'),('6f0e5a98','סתרי תורה','סִתְרֵי תּוֹרָה'),('1093f13a','סתרי אותיות','סִתְרֵי אוֹתִיּוֹת'),('e98c0922','תוספות הזוהר','תּוֹסָפוֹת הַזֹּהַר'),('efa00a59','השמטות הזוהר','הַשְׁמָטוֹת הַזֹּהַר')]:
    secs=small(fid,title.split(' הזוהר')[0]); vols.append((cfg(title,nq,'חִבּוּרֵי הַזֹּהַר','zx',W2),secs))
    print(title,'chapters',len(secs[0]['c']),'items',sum(len(c['i']) for c in secs[0]['c']))
VOL0=120; man=[]
def dump_he(vi,secs):
    he={}
    for si,s in enumerate(secs):
        for ci,c in enumerate(s['c']):
            for ii,it in enumerate(c['i']):
                if 'he' in it: he['%d.%d.%d'%(si,ci,ii)]=it.pop('he')
    if not he: return None
    js=json.dumps({'he':he},ensure_ascii=False,separators=(',',':')); fn='zh/V%d.%s.json'%(vi,hashlib.md5(js.encode()).hexdigest()[:8])
    open(OUT+'/'+fn,'w',encoding='utf-8').write(js); return fn,len(js)
for k,(c,secs) in enumerate(vols):
    vi=VOL0+k; r=dump_he(vi,secs)
    if r: c['zh']=r[0]
    else: c.pop('zh',None)
    secs=[{'id':'v%dg%d'%(vi,si),'short':s['short'],'g':'V%d'%vi,'c':s['c']} for si,s in enumerate(secs)]
    js=json.dumps(secs,ensure_ascii=False,separators=(',',':'))
    fn='b%02d_V%d.%s.json'%(vi-2,vi,hashlib.md5(js.encode()).hexdigest()[:10]); open(OUT+'/'+fn,'w',encoding='utf-8').write(js)
    man.append({'vi':vi,'cfg':c,'file':fn}); print(vi,c['title'],len(js)//1024,'KB', ('he %dKB'%(r[1]//1024)) if r else '')
# תיקוני הזוהר הקיים (V60): הצמדת התרגום לפי התאמת הטקסט, בלי לשנות את הכרך עצמו
d=json.load(open(glob.glob('/home/claude/breslever-pro/www/data/*_V60.*')[0],encoding='utf-8'))
norm=lambda t: re.sub(r'[^א-ת]','',t)[:60]
P=R['4d0737c3']; mp={}
for k,(s,b,t) in enumerate(P):
    if s=='W' and len(t)>60:
        h=[]; j=k+1
        while j<len(P) and P[j][0]=='N': h.append(esc(P[j][2])); j+=1
        if h: mp.setdefault(norm(t),'<br>'.join(h))
he={}; tot=0
for si,s in enumerate(d):
    for ci,c in enumerate(s['c']):
        for ii,it in enumerate(c['i']):
            tot+=1; x=mp.get(norm(it['b'][-1][1]))
            if x: he['%d.%d.%d'%(si,ci,ii)]=x
js=json.dumps({'he':he},ensure_ascii=False,separators=(',',':')); fn='zh/V60.%s.json'%hashlib.md5(js.encode()).hexdigest()[:8]
open(OUT+'/'+fn,'w',encoding='utf-8').write(js); print('V60 he',len(he),'of',tot)
json.dump(man,open(OUT+'/manifest_zohar.json','w',encoding='utf-8'),ensure_ascii=False)
open(OUT+'/v60zh.txt','w').write(fn)
