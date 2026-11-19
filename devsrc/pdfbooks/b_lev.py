from bb import *
import re
def drop(l,pn):
    if l['y']<82 and pn>6: return True
    if l['y']>590 or re.fullmatch(r'\[?\d+\]?',l['text']): return True
    return False
def cls(l,pn):
    f=l['font']; z=l['size']
    if f.startswith('FbLivorna-Bold') and z>=15.5 and len(l['text'])>3: return 'H1'
    if f.startswith('FbLivorna-Bold') and re.fullmatch(r'[א-ת]{1,2}\.',l['text']): return 'H2'
    return 'B'
fix=lambda t: re.sub(r'^(\d+)\. \1(?=\S)',r'\1. ',t)
CFG=dict(p0=6,p1=62,drop=drop,cls=cls,ind=999,lead=1.3,gapx=2.2,fix=fix,h1join=40,outdent=6,shortend=40,cind=18)
if __name__=='__main__':
    ev=build('lev',CFG); bk=to_book(ev,144,'דרכי ראיית הלב',first_title='הקדמה ומבוא'); stats(bk)
    for s in bk: print(s['short'],'::',' | '.join('%s(%d)'%(c['t'],len(c['i'])) for c in s['c'])[:400])
    show(bk,0,2,5); show(bk,3,4,8)
    import pickle; pickle.dump(bk,open('lev.book','wb'))
