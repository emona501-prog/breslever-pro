import pickle,json,hashlib,re
OUT='/home/claude/content/out9/'
bk=pickle.load(open('maay.book','rb'))
ab=dict(t='על הספר',i=[dict(n='',b=[['p','<b>מעיינות אשר</b><br>ביאורים על תורות מליקוטי מוהר"ן חלק א:<br>תורה א · מב · קב · מג · קכט · רסג']]),
                     dict(n='',b=[['p','בכל תורה: לשון רבנו (באותיות מודגשות) ולצדה הביאור, ואחריה תמצית הדברים, קיום התורה למעשה בפועל, הוספות, ותפילה מליקוטי תפילות.']]),
                     dict(n='',b=[['ins','הניקוד של לשון רבנו נלקח מליקוטי מוהר"ן שבאפליקציה. הביאור, ההוספות והתפילות – כמו בספר המודפס.']])])
bk[0]['c'].insert(0,ab)
for s in bk:
    for c in s['c']:
        for it in c['i']:
            for bl in it['b']: bl[1]=re.sub(r' +([,.:;!?])',r'\1',re.sub(r'\s+',' ',bl[1])).strip()
        c['i']=[it for it in c['i'] if any(bl[1] for bl in it['b'])]
data=json.dumps(bk,ensure_ascii=False,separators=(',',':'))
fn='b145_V147.%s.json'%hashlib.md5(data.encode()).hexdigest()[:10]
open(OUT+fn,'w',encoding='utf-8').write(data)
W={"group":"","sections":"תורות","section":"תורה","chapters":"פרקים","chapterOne":"פרק אחד","items":"קטעים","item":"קטע","next":"הפרק הבא","prev":"הפרק הקודם"}
cfg={"title":"מעיינות אשר","titleNiqud":"מַעְיְנוֹת אָשֵׁר","author":"בֵּאוּרִים עַל תּוֹרוֹת מִלִּקּוּטֵי מוֹהֲרַ\"ן","tag":"לָשׁוֹן רַבֵּנוּ וּבֵאוּרוֹ · תַּמְצִית הַדְּבָרִים · קִיּוּם הַתּוֹרָה לְמַעֲשֶׂה","pre2":"","heroSize":40,"bg":"dawn","heroArt":"etzot","planWord":"קטעים","cat":"kuntres","words":W}
json.dump([dict(vi=147,cfg=cfg,file=fn)],open(OUT+'manifest_maay.json','w',encoding='utf-8'),ensure_ascii=False)
print(fn,len(data)//1024,'KB', sum(len(c['i']) for s in bk for c in s['c']),'items')
