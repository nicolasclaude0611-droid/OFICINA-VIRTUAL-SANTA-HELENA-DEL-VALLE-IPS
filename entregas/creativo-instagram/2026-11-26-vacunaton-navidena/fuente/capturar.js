// node fuente/capturar.js  -> genera A/ y B/ con post, historia-1..3 y recordatorio
const {chromium}=require('playwright');const path=require('path');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
const piezas=[['post','post'],['h1','historia-1'],['h2','historia-2'],['h3','historia-3'],['rec','recordatorio-viernes-11']];
for(const v of ['A','B']) for(const [k,n] of piezas){
 await p.goto('file://'+path.resolve(__dirname,'piezas.html')+`?v=${v}&p=${k}`);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(250);
 await p.locator('#pz').screenshot({path:path.resolve(__dirname,'..',v,n+'.png')});}
await b.close();})();
