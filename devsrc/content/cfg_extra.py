# שינויי תצורה כלליים (רץ מתוך install.py; c = bookcfg)
c['libSubs']['tanach']=[{"id":"smt","t":"חומש · שניים מקרא ואחד תרגום"},{"id":"mg","t":"חומש · מקראות גדולות"},{"id":"nev","t":"נביאים"},{"id":"ket","t":"כתובים"}]
c['books'][59]['sub']='smt'
if not any(t['id']=='tcherin' for t in c['libTabs']):
    k=[t['id'] for t in c['libTabs']].index('rnt'); c['libTabs'].insert(k+1,{"id":"tcherin","t":"ספרי הרב מטשערין"})
c['books'][18]['cat']='tcherin'
