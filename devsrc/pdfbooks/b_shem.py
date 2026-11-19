from bb import *
import re
def drop(l,pn):
    if l['y']<60 or l['y']>548: return True
    if re.fullmatch(r'\d+',l['text']): return True
    return False
def cls(l,pn):
    f=l['font']; z=l['size']
    if f.startswith('FbThila') and z>=25: return 'H0'
    if f.startswith('FbThila') and z>=21:
        if re.fullmatch(r"פרק [א-י]{1,2}'?",l['text']): return 'H0'
        if pn==10 and l['text']=='הקדמה': return 'H0'
        if pn==20 and l['text'].startswith('הסכמות'): return 'H0'
        return 'H1'
    if f.startswith('GuttmanStam') and z>=30: return 'H1'
    if f.startswith('GuttmanStam') and 19<=z<30: return 'H2'
    if f.startswith('FbThila') and z>=17: return 'H2'
    return 'B'
CFG=dict(p0=10,p1=200,right=348.8,left=71.0,drop=drop,cls=cls,ind=8,indmax=30,cind=20,lead=1.45,gapx=4,
         pstart=lambda l,pn: l['text'].startswith('◆'), cpage=lambda l,pn: l['font'].startswith(('FbSfaradi','GuttmanStam','Livorna')))
if __name__=='__main__':
    ev=build('shem',CFG); bk=to_book(ev,142,'כולנו יודעי שמך',first_title='הקדמה'); stats(bk)
    show(bk,0,2,3,0); show(bk,0,3,4,3); show(bk,0,3,6,8)
    import pickle; pickle.dump(bk,open('shem.book','wb'))
