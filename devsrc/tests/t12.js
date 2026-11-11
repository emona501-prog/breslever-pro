const {open}=require('./lib');(async()=>{let {b,p,errs}=await open({wait:12000});
const go=async(q)=>{await p.goto('http://localhost:8900/'+q);await p.waitForTimeout(6500);return await p.evaluate(()=>[document.querySelector('.view.active').id,document.querySelectorAll('#reader .item').length,(document.querySelector('#rcTxt')||{}).textContent])};
for(const q of ['?i=v0g0.3.1','?i=v59g0.0.1','?i=v49g0.0.0','?i=v60g1.0.0','?i=v93g0.5.2','?i=v98g0.22.0','?i=v114g0.2.3','?i=v116g0.3.0','?i=v18g0.1.0']) console.log(q,JSON.stringify(await go(q)));
for(const tab of ['search','index','mine','tikkun','home']){await p.click('#tabbar [data-tab="'+tab+'"]').catch(()=>{});await p.waitForTimeout(500);}
console.log('errs',errs);await b.close();})();
