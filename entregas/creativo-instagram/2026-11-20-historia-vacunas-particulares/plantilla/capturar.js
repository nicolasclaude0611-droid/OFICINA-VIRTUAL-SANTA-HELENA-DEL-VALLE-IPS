// node capturar.js <variacion> <pantalla> <salida.png>
const {chromium}=require('playwright');const path=require('path');(async()=>{
const [v,p,out]=process.argv.slice(2);const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1920}});
await pg.goto('file://'+path.resolve(__dirname,'historia.html')+`?v=${v}&p=${p}`);
await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(300);
await pg.locator('#h').screenshot({path:out});await b.close();})();
