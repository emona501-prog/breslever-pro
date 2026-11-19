from bb import *
import re
def drop(l,pn):
    if l['y']<60: return True
    if re.fullmatch(r'\d+',l['text']): return True
    return False
def cls(l,pn):
    f=l['font']; z=l['size']
    if f.startswith('FbThila') and z>=21: return 'H1'
    if f.startswith('FbThila') and z>=17: return 'H2' if pn>=30 else 'H1'
    if (f.startswith('FbTarfon') or (z<=13.2 and re.fullmatch(r'\(.{4,60}\)',l['text']) and l['x1']<200)): return 'F'
    return 'B'
CFG=dict(p0=16,p1=415,right=425.3,left=56.8,drop=drop,cls=cls,ind=8,indmax=30,cind=24,lead=1.32,gapx=3.0,skip=(19,20),cpage=lambda l,pn: 21<=pn<=29 and not l['font'].startswith('FbThila'))
if __name__=='__main__':
    ev=build('mesh',CFG); bk=to_book(ev,141,'משלים קטנים עם מסרים גדולים',first_title='הקדמה'); stats(bk)
    import collections; print(collections.Counter(len(c['i']) for c in bk[0]['c']).most_common(8))
    show(bk,0,2,4); show(bk,12,14,5)
    import pickle; pickle.dump(bk,open('mesh.book','wb'))
