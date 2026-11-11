#!/bin/bash
# בנייה: app.js (מקור קריא) -> www/index.html (מוקטן) בריפו
set -e
cd /home/claude/src
node --check app.js
/home/claude/tools/node_modules/.bin/terser app.js -c passes=1,sequences=true -m --comments '/^!/' -o app.min.js
python3 - <<'PY'
s=open('/home/claude/src/shell.html',encoding='utf-8').read()
js=open('/home/claude/src/app.min.js',encoding='utf-8').read()
assert s.count('/*__APP_JS__*/')==1 and '</script' not in js.lower().replace('<\\/script','')
open('/home/claude/breslever-pro/www/index.html','w',encoding='utf-8').write(s.replace('/*__APP_JS__*/',js))
print('built',len(js))
PY
