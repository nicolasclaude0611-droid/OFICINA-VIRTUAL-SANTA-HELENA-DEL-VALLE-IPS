// node capturar.js <variacion> <pantalla> <salida.png> [frente]
const {chromium}=require('playwright');const path=require('path');(async()=>{
const [v,p,out,capa]=process.argv.slice(2);const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1920}});
await pg.goto('file://'+path.resolve(__dirname,'historia.html')+`?v=${v}&p=${p}`+(capa?'&capa=frente':''));
await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(300);
await pg.locator('#h').screenshot({path:out,omitBackground:!!capa});await b.close();})();
