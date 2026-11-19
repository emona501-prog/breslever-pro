from bb import *
import re
def drop(l,pn):
    if l['y']<95 and l['font'].startswith('FbTrapez-Light'): return True
    if l['y']>640: return True
    if l['font'].startswith('FbKidush'): return True
    return False
def cls(l,pn):
    f=l['font']; z=l['size']
    if f.startswith('FbLivorna-Bold') and z>=60: return 'H0'
    if f.startswith('FbTrapez-Bold') and z>=19: return 'H1'
    if f.startswith('FbTrapez-Bold') and z>=12.5: return 'H2'
    if f.startswith('FbFRealBeletBook-Bold') and l['x0']>250 and len(l['text'])<45 and not re.search(r'[.,:]$',l['text']): return 'H3'
    if f.startswith('FbLivorna') and z<=11.2 and re.fullmatch(r'\(.{3,70}\)',l['text']): return 'F'
    return 'B'
HN=['א','ב','ג','ד','ה','ו','ז','ח','ט','י','יא','יב','יג','יד','טו','טז','יז','יח','יט','כ','כא','כב','כג','כד','כה','כו','כז','כח','כט','ל']
_st={'n':0}
def fix(t):
    m=re.match(r'^\. (?=[א-ת])',t)
    if not m: return t
    rest=t[2:]
    nx=HN[_st['n']] if _st['n']<len(HN) else None
    if nx and rest.startswith(nx) and not rest.startswith('א' if nx!='א' else '\x00'):
        _st['n']+=1; return nx+'. '+rest[len(nx):]
    if rest.startswith('א'): _st['n']=1; return 'א. '+rest[1:]
    if nx and rest.startswith(nx): _st['n']+=1; return nx+'. '+rest[len(nx):]
    return rest[0]+'. '+rest[1:]
grp=lambda l: 'Q' if l['font'].startswith('FbLivorna') else 'B'
CFG=dict(p0=3,p1=380,right=425.0,left=84.8,drop=drop,cls=cls,ind=999,lead=1.32,gapx=4,skip=(8,9,10,11),grp=grp,fix=fix,pstart=lambda l,pn: re.match(r'^[א-ת]{1,2}\. ',l['text']) is not None and l['x1']>415,nocenter=lambda l,pn: l['font'].startswith('FbLivorna-Regular'),
         cpage=lambda l,pn: l['font'].startswith('FbLivorna-Bold'))
if __name__=='__main__':
    ev=build('olam',CFG); bk=to_book(ev,143,'עולם חדש',first_title='הקדמת העורך',first_sec='הקדמה ופתח דבר'); stats(bk)
    for s in bk: print(s['short'],'::',' | '.join(c['t'] for c in s['c'])[:200])
    show(bk,0,3,5,1); show(bk,0,2,6,11)
    import pickle; pickle.dump(bk,open('olam.book','wb'))
