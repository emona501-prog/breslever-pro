const {chromium}=require('playwright');
exports.open=async(opt={})=>{opt.wn=opt.wn||require('fs').readFileSync(__dirname+'/wn.txt','utf8');process.on('unhandledRejection',e=>{console.log('FAIL',String(e.message).split('\n')[0]);process.exit(1)});const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:opt.w||420,height:opt.h||860}});const p=await ctx.newPage();
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('**/raw.githubusercontent.com/**',r=>r.fulfill({body:'{"v":1}',contentType:'application/json'}));
await p.route('**/goatcounter**',r=>r.abort());
await p.addInitScript((ls)=>{const S=(k,v)=>{if(localStorage.getItem('lmhrn_'+k)==null)localStorage.setItem('lmhrn_'+k,v)};S('introOff','true');S('instNever','1');S('wnSeen',JSON.stringify(ls.wn));S('tipsOn','false');for(const k in (ls.st||{}))S(k,JSON.stringify(ls.st[k]));},opt);
await p.goto('http://localhost:'+(opt.port||8900)+'/'+(opt.q||''));await p.waitForTimeout(opt.wait||3000);return {b,p,errs};};
