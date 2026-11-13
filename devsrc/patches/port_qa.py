# מעתיק את מנוע השאלות (kb/qa.js) לתוך app.js
qa=open('/home/claude/kb/qa.js',encoding='utf-8').read()
qa=qa.replace('if (typeof module !== "undefined") module.exports = botQAMake;\n','')
a='''  function inScope(sc) {
    const S = new Set(sc);'''
assert a in qa
qa=qa.replace(a,'''  const SCC = new Map();
  function inScope(sc) {
    const key = sc.join(",");
    if (SCC.has(key)) return SCC.get(key);
    const S = new Set(sc);''')
a='''    for (let i = 0; i < E.N; i++) S.has(E.V(i)) && r.push(i);
    return r;'''
assert a in qa
qa=qa.replace(a,'''    for (let i = 0; i < E.N; i++) S.has(E.V(i)) && r.push(i);
    return (SCC.size > 12 && SCC.clear(), SCC.set(key, r), r);''')
qa='\n'.join('  '+l if l.strip() else l for l in qa.split('\n')).rstrip()+'\n'
qa=qa[qa.index('  function botQAMake'):]
p='/home/claude/src/app.js'; s=open(p,encoding='utf-8').read()
i=s.index('  function botQAMake(E) {'); j=s.index('\n  let botQA = null;')
s=s[:i]+qa+s[j:]
open(p,'w',encoding='utf-8').write(s)
open('/home/claude/src/patches/p34_bot_qa_engine.js','w',encoding='utf-8').write(open('/home/claude/kb/qa.js').read())
print('ported')
