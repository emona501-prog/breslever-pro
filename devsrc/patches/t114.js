// סורק: מפעיל lzDbg, עובר על כל המסכים, לוחץ על כל כפתור (ועל כל כפתור בחלון שנפתח), ואוסף גישות לספר שלא נטען
const {chromium}=require('playwright');
const VIEWS=(process.argv[2]||'home,tikkun,calendar,settings,day,search,birkat,random,mine,dir,plan,pearls,index,vol,sec').split(',');
(async()=>{const b=await chromium.launch();const found={};const perr=[];
for(const view of VIEWS){
 const c=await b.newContext({viewport:{width:420,height:900}});const p=await c.newPage();
 await p.addInitScript(()=>{localStorage.setItem('lzDbg','1');localStorage.setItem('lmhrn_introOff','true');localStorage.setItem('lmhrn_wnSeen','"2026-11-17b"');
   window.open=()=>null;window.print=()=>{};try{Object.defineProperty(navigator,'share',{value:undefined})}catch(e){}});
 let cur='';p.on('console',m=>{const t=m.text();if(/LZ-UNLOADED/.test(t)){const k=view+' › '+cur;(found[k]=found[k]||new Set()).add(t.slice(0,60))}});
 p.on('pageerror',e=>perr.push(view+' › '+cur+' :: '+String(e.message).slice(0,140)));p.on('dialog',d=>d.dismiss().catch(()=>{}));
 await p.goto('http://localhost:8900/');await p.waitForTimeout(7000);
 const reset=async()=>{await p.evaluate(v=>{const s=document.getElementById('splash');s&&s.remove();document.querySelectorAll('.sheet-bg,.modal-bg,.ovl,.sheet.open,[data-sheet]').forEach(e=>{});try{window.__It(v,v==='vol'?{v:0}:v==='sec'?{si:0}:{})}catch(e){}
   document.querySelectorAll('.sbg,.sheetbg,.mbg,.bot-panel.open').forEach(e=>e.click&&0);},view).catch(()=>{});
   await p.keyboard.press('Escape').catch(()=>{});await p.evaluate(()=>{history.length;document.querySelectorAll('[id$="Sheet"].open,.sheet.open,.pop.open').forEach(e=>e.classList.remove('open'));const bg=document.querySelector('#sheetBg,.sheet-bg');bg&&bg.click();}).catch(()=>{});await p.waitForTimeout(250);};
 const SEL='button,[data-go],[data-act],[data-cm],.tile,.hcard,.chip,[role=button],.act,.row[data-id],li[data-id],.card[data-id],.sw input';
 const list=async(root)=>await p.evaluate(([SEL,root])=>{const R=root?document.querySelector(root):document;if(!R)return[];return [...R.querySelectorAll(SEL)].filter(e=>e.offsetParent&&!e.closest('a[href^=http]')).map((e,i)=>(e.textContent||e.id||'').trim().replace(/\s+/g,' ').slice(0,28)+'#'+i)},[SEL,root]);
 const clickN=async(root,i)=>await p.evaluate(([SEL,root,i])=>{const R=root?document.querySelector(root):document;const e=R&&[...R.querySelectorAll(SEL)].filter(e=>e.offsetParent&&!e.closest('a[href^=http]'))[i];if(!e)return 0;if(/מחק|איפוס|אפס הכל|שחזור|ייבוא|יציאה/.test(e.textContent))return 0;e.click();return 1},[SEL,root,i]).catch(()=>0);
 await reset();const L=await list('.view.active');
 for(let i=0;i<Math.min(L.length,70);i++){await reset();cur=L[i];if(!await clickN('.view.active',i))continue;await p.waitForTimeout(450);
   // שכבה שנייה – כל מה שנפתח
   const top=await p.evaluate(()=>{const s=[...document.querySelectorAll('.sheet,.modal,.pop,.bot-panel,[class*=sheet]')].filter(e=>e.offsetParent&&getComputedStyle(e).position==='fixed');const e=s[s.length-1];if(!e)return null;e.setAttribute('data-crawl','1');return 1});
   if(top){const L2=await list('[data-crawl]');for(let j=0;j<Math.min(L2.length,14);j++){const lab=cur;cur=lab+' › '+L2[j];await clickN('[data-crawl]',j);await p.waitForTimeout(300);cur=lab;
       if(!await p.evaluate(()=>!!document.querySelector('[data-crawl]')&&document.querySelector('[data-crawl]').offsetParent!==null))break;}
     await p.evaluate(()=>document.querySelectorAll('[data-crawl]').forEach(e=>e.removeAttribute('data-crawl')));}
 }
 console.log('view',view,'clickables',L.length);await c.close();
}
console.log('\n=== LZ-UNLOADED ===');Object.keys(found).forEach(k=>console.log(k,'=>',[...found[k]].join(' ; ')));
console.log('\n=== page errors ===');[...new Set(perr)].slice(0,30).forEach(x=>console.log(x));
await b.close();})();
