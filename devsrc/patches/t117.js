// הפעלה טרייה (שום ספר לא נטען) + מרגל: מפעילים פעולות "לפי מזהה" ורואים מי קורא טקסט שלא נטען
const {chromium}=require('playwright');
const ACTS={
 wdg:()=>JSON.stringify(window.__wdgData()).length,
 natRem:()=>{const r=window.__natRem&&window.__natRem();return r&&r.then?r.then(x=>JSON.stringify(x||'').length):JSON.stringify(r||'').length},
 halCard:()=>String(window.__halCard&&window.__halCard()).length,
 halOpen:()=>window.__halOpen&&window.__halOpen(),
 goals:()=>window.__goalsOpen&&window.__goalsOpen(),
 prlCard:()=>{const L=window.__PRL.list();const p=L.find(x=>x.id)||L[0];window.__prlCard(p);return p.id},
 prlGo:()=>{const L=window.__PRL.list();const p=L.find(x=>x.id);window.__prlGo(p);return p.id},
 botStatus:()=>window.__botOpen('תכין לי סטטוס'),
 botRead:()=>window.__botOpen('תקריא לי שיחות הר"ן שיחה ה'),
 botChz:()=>window.__botOpen('אני מרגיש מיואש תחזק אותי'),
 botStory:()=>window.__botOpen('ספר לי סיפור'),
 botOpenT:()=>window.__botOpen('פתח ליקוטי מוהרן תורה ו'),
 botQ:()=>window.__botOpen('איפה רבנו מדבר על התבודדות'),
 botDib:()=>window.__botOpen('דיבור קצר על שמחה'),
 hd:()=>window.__hdOpen&&window.__hdOpen(),
 thm:()=>window.__thmOpen&&window.__thmOpen(),
 mine:()=>window.__It('mine'),day:()=>window.__It('day'),plan:()=>window.__It('plan'),pearls:()=>window.__It('pearls'),index:()=>window.__It('index'),random:()=>window.__It('random'),
};
(async()=>{const b=await chromium.launch();const only=process.argv[2]?process.argv[2].split(','):Object.keys(ACTS);
for(const k of only){const c=await b.newContext({viewport:{width:420,height:900}});const p=await c.newPage();const W=new Set(),E=[];
 await p.addInitScript(()=>{localStorage.setItem('lzDbg','1');localStorage.setItem('lmhrn_introOff','true');localStorage.setItem('lmhrn_wnSeen','"2026-11-17b"');window.open=()=>null;window.print=()=>{}});
 let on=0;p.on('console',m=>{const t=m.text();if(on&&/LZ-UNLOADED/.test(t))W.add(t.replace(/http:\/\/localhost:8900\/:1389:/g,'@').replace(/LZ-UNLOADED V\d+/,'').slice(0,170))});p.on('pageerror',e=>E.push(String(e.message).slice(0,120)));
 await p.goto('http://localhost:8900/');await p.waitForTimeout(7000);await p.evaluate(()=>{const s=document.getElementById('splash');s&&s.remove()});on=1;
 let r;try{r=await p.evaluate(ACTS[k])}catch(e){r='X '+String(e.message).slice(0,80)}
 await p.waitForTimeout(3500);
 const txt=await p.evaluate(()=>{const e=[...document.querySelectorAll('.sheet,.bot-ans,#botAns,.toast,.view.active')].filter(e=>e.offsetParent).pop();return e?e.innerText.replace(/\s+/g,' ').slice(0,160):''}).catch(()=>'');
 console.log('##',k,'ret=',String(r).slice(0,40),'| warn',W.size,'| err',E.length,'\n   ',txt);[...W].slice(0,4).forEach(w=>console.log('   W',w));E.slice(0,2).forEach(w=>console.log('   E',w));
 await c.close();}
await b.close();})();
