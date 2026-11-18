// סורק עומק (3 רמות) עם מרגל הטעינה ומשתמש "עשיר". שימוש: node t122.js view1,view2 out.txt
const {chromium}=require('playwright');const fs=require('fs');
const VIEWS=process.argv[2].split(','),OUT=process.argv[3];const SEED=JSON.parse(fs.readFileSync(__dirname+'/seed.json','utf8'));
const CAP=[0,90,22,10],T0=Date.now(),BUDGET=(+process.argv[4]||25)*60e3;
const SEL='button,[data-go],[data-act],[data-cm],.tile,.hcard,.chip,.pill,[role=button],.act,.row,.pcard,li[data-id],.card,.sw input,.seg button,summary,[onclick]';
const BAD='מחק|מחיק|איפוס|אפס|שחזור|ייבוא|יבוא|יציאה|התקן|עדכון גרסה|הורד|שלח|שתף|שיתוף|הדפס|ביט|פייבוקס|יוטיוב|וואטסאפ|PDF|צלם';
(async()=>{const b=await chromium.launch();const found={};const perr=new Set();let clicks=0;
for(const view of VIEWS){
 const c=await b.newContext({viewport:{width:420,height:900}});const p=await c.newPage();let cur='';
 await p.addInitScript(([S,process_curv])=>{for(const k in S)localStorage.setItem(k,S[k]);localStorage.setItem('lzDbg','1');if(process_curv)localStorage.setItem('lmhrn_curv','9');localStorage.setItem('lmhrn_wnSeen','"2026-11-17b"');window.open=()=>null;window.print=()=>{};try{Object.defineProperty(navigator,'share',{value:undefined})}catch(e){}},[SEED,!!process.argv[5]]);
 p.on('console',m=>{const t=m.text();if(/LZ-UNLOADED/.test(t)){const st=t.replace(/http:\/\/localhost:8900\/[^:]*:1389:/g,'@').replace(/LZ-UNLOADED V\d+ \.\w+ :: /,'').replace(/at Proxy\.\w+ \(<anonymous>\) \| +/,'').slice(0,150);(found[st]=found[st]||new Set()).add(view+' › '+cur)}});
 p.on('pageerror',e=>perr.add(view+' › '+cur+' :: '+String(e.message).slice(0,140)));p.on('dialog',d=>d.dismiss().catch(()=>{}));
 const boot=async()=>{await p.goto('http://localhost:8900/').catch(()=>{});await p.waitForTimeout(6500);};await boot();
 const ev=(f,a)=>p.evaluate(f,a).catch(()=>null);
 const reset=async()=>{const ok=await ev(v=>{const s=document.getElementById('splash');s&&s.remove();if(!window.__It)return 0;try{window.__It('home');window.__It(v,v==='vol'?{v:9}:v==='sec'?{s:window.__secs(1).find(x=>x.split(' ')[1]==='V9').split(' ')[0]}:{})}catch(e){}return 1},view);if(!ok)await boot(),await ev(v=>{const s=document.getElementById('splash');s&&s.remove();window.__It&&window.__It(v)},view);
   for(let k=0;k<3;k++){const open=await ev(()=>{const s=[...document.querySelectorAll('body *')].filter(e=>e.offsetParent&&getComputedStyle(e).position==='fixed'&&e.offsetHeight>200&&!e.matches('nav,.tabbar,#fab,.view,.prl-tick')&&!e.closest('.view'));if(!s.length)return 0;const bg=document.querySelector('.sheet-bg,.sbg,#sheetBg,.modal-bg');bg&&bg.click();return 1});if(!open)break;await p.keyboard.press('Escape').catch(()=>{});await p.waitForTimeout(150);}
   await p.waitForTimeout(120);};
 // המיכל העליון: חלון צף אם יש, אחרת המסך הפעיל
 const cont=()=>ev(()=>{document.querySelectorAll('[data-crawl]').forEach(e=>e.removeAttribute('data-crawl'));const s=[...document.querySelectorAll('body *')].filter(e=>e.offsetParent&&getComputedStyle(e).position==='fixed'&&e.offsetHeight>200&&e.offsetWidth>250&&!e.matches('nav,.tabbar,#fab,.view,.prl-tick,#splash')&&!e.closest('.view')&&e.querySelector('button,.row,.pill'));const e=s.sort((a,b)=>(+getComputedStyle(b).zIndex||0)-(+getComputedStyle(a).zIndex||0))[0]||document.querySelector('.view.active');if(!e)return '';e.setAttribute('data-crawl','1');return (e.id||e.className).slice(0,30)+'|'+(document.querySelector('.view.active')||{}).id+'|'+e.innerText.replace(/\s+/g,' ').slice(0,60)});
 const list=()=>ev(([SEL,BAD])=>{const R=document.querySelector('[data-crawl]');if(!R)return[];const B=new RegExp(BAD);return [...R.querySelectorAll(SEL)].filter(e=>e.offsetParent&&!e.closest('a[href]')&&!e.querySelector(SEL.split(',').slice(0,1)[0])).map(e=>{const t=(e.textContent||e.id||'').trim().replace(/\s+/g,' ').slice(0,24);return B.test(t)?null:t}).map((t,i)=>t==null?null:t+'#'+i)},[SEL,BAD]).then(x=>x||[]);
 const click=(i)=>ev(([SEL,i])=>{const R=document.querySelector('[data-crawl]');const e=R&&[...R.querySelectorAll(SEL)].filter(e=>e.offsetParent&&!e.closest('a[href]')&&!e.querySelector('button'))[i];if(!e)return 0;e.click();return 1},[SEL,i]).then(async r=>{clicks++;await p.waitForTimeout(330);return r});
 const reach=async(path)=>{await reset();for(const i of path){await cont();if(!await click(i))return false;}return true;};
 const spread=(L,cap)=>{const idx=L.map((t,i)=>t?i:-1).filter(i=>i>=0);if(idx.length<=cap)return idx;const st=idx.length/cap;return Array.from({length:cap},(_,k)=>idx[Math.floor(k*st)]);};
 await reset();const base=await cont();const L1=await list();
 for(const i of spread(L1,CAP[1])){if(Date.now()-T0>BUDGET)break;cur=L1[i];if(!await reach([i]))continue;const s1=await cont();if(!s1||s1===base)continue;
   const L2=await list();let lost=false;
   for(const j of spread(L2,CAP[2])){cur=L1[i]+' › '+L2[j];if(lost){if(!await reach([i]))break;await cont();lost=false;}
     if(!await click(j)){lost=true;continue;}const s2=await cont();if(s2===s1)continue;lost=true;if(!s2||s2===base)continue;
     const L3=await list();let lost3=false;
     for(const k of spread(L3,CAP[3])){cur=L1[i]+' › '+L2[j]+' › '+L3[k];if(lost3){if(!await reach([i,j]))break;await cont();lost3=false;}
       if(!await click(k)){lost3=true;continue;}const s3=await cont();if(s3!==s2)lost3=true;}
   }
 }
 fs.appendFileSync(OUT,'view '+view+' L1='+L1.filter(Boolean).length+' clicks so far '+clicks+' t='+Math.round((Date.now()-T0)/1e3)+'s\n');await c.close();
}
fs.appendFileSync(OUT,'\n=== LZ-UNLOADED ('+Object.keys(found).length+' stacks) ===\n'+Object.keys(found).map(k=>k+'\n      e.g. '+[...found[k]].slice(0,3).join('  ||  ')).join('\n')+'\n=== page errors ===\n'+[...perr].slice(0,40).join('\n')+'\nDONE\n');
await b.close();})();
