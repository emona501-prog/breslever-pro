from bb import *
import re
def drop(l,pn):
    if l['y']<75 and pn>6: return True
    if l['y']>590 or re.fullmatch(r'\[?\d+\]?',l['text']): return True
    return False
def cls(l,pn):
    f=l['font']; z=l['size']
    if f.startswith('FbAristocrat-Bold') and z>=17.5: return 'H1'
    if f.startswith('FbAristocrat-Bold'): return 'H2'
    return 'B'
CFG=dict(p0=6,p1=75,drop=drop,cls=cls,ind=999,lead=1.42,gapx=2.2,h1join=45,outdent=6,shortend=45,cind=18)
if __name__=='__main__':
    ev=build('einei',CFG); bk=to_book(ev,145,'עיני השם',first_title='הקדמה'); stats(bk)
    for s in bk: print(s['short'],'::',' | '.join('%s(%d)'%(c['t'],len(c['i'])) for c in s['c'])[:500])
    show(bk,0,3,4); show(bk,5,6,6)
    import pickle; pickle.dump(bk,open('einei.book','wb'))
