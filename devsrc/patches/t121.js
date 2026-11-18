// יוצר "משתמש עשיר": סדר יום שמור, יעדים, סימניות – ושומר את ה-localStorage לקובץ זרע
const {open}=require('./lib');const fs=require('fs');(async()=>{const ids=['v0g0.3.1','v4g28.5.3','v2g5.7.39','v12g1.38.6','v8g0.4.0'];const bm={},nt={},rd={};ids.forEach((i,k)=>{bm[i]={ts:Date.now()-k*1e3};nt[i]={t:'הערה '+k,ts:Date.now()}});rd['v0g0.0.0']=Date.now();
const {b,p}=await open({wait:7000,st:{bm,notes:nt,basket:ids,read:rd,last:{id:ids[1],ts:Date.now()}}});await p.evaluate(()=>{const s=document.getElementById('splash');s&&s.remove();window.__It('day')});await p.waitForTimeout(500);
await p.evaluate(()=>[...document.querySelectorAll('.view.active button')].find(e=>/בניית סדר היום/.test(e.textContent)).click());await p.waitForTimeout(1000);
for(const v of [8,9,11,0])await p.evaluate(v=>{const c=document.querySelector('[data-dt="'+v+'"]');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))},v);
await p.evaluate(()=>{const t=document.querySelector('#dsTeh');t&&(t.checked=true,t.dispatchEvent(new Event('change',{bubbles:true})));const k=document.querySelector('#dsTk');k&&(k.checked=true,k.dispatchEvent(new Event('change',{bubbles:true})))});
await p.waitForTimeout(4000);await p.evaluate(()=>[...document.querySelectorAll('.view.active button')].find(e=>/שמור/.test(e.textContent)).click());await p.waitForTimeout(1200);
const ls=await p.evaluate(()=>{const o={};for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);o[k]=localStorage.getItem(k)}return o});
delete ls.lzDbg;fs.writeFileSync('seed.json',JSON.stringify(ls));console.log(Object.keys(ls).join(' '));await b.close();})();
