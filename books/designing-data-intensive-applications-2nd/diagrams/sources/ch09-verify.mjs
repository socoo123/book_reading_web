// Isolated local server and Chrome; shuts down on success or failure.
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'../../../..');
const tools=process.env.DDIA_TOOLS||'/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools';
const require=createRequire(path.join(tools,'package.json'));
const {chromium}=require('playwright');
const mime={'.html':'text/html','.svg':'image/svg+xml','.css':'text/css','.js':'application/javascript'};
const server=http.createServer(async(req,res)=>{
 try{
  const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  const file=path.join(root,pathname==='/'?'index.html':pathname);
  res.setHeader('Content-Type',mime[path.extname(file)]||'application/octet-stream');
  res.end(await fs.readFile(file));
 }catch{res.statusCode=404;res.end('Not found');}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const base=`http://127.0.0.1:${server.address().port}`;
const chapter='/books/designing-data-intensive-applications-2nd/chapters/ch09.html';
const results=[],diagrams=[];
const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
try{
 for(const width of [1440,375])for(const theme of ['light','dark']){
  const context=await browser.newContext({viewport:{width,height:960},colorScheme:theme});
  const page=await context.newPage();
  const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
  await page.goto(base+chapter,{waitUntil:'networkidle'});
  await page.locator('img').evaluateAll(images=>images.forEach(i=>i.loading='eager'));
  await page.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0));
  const metrics=await page.evaluate(()=>{
   const article=document.querySelector('.article'),p=article.querySelector('section p');
   return {width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
    theme:document.documentElement.dataset.theme,scheme:getComputedStyle(document.documentElement).colorScheme,
    font:getComputedStyle(p).fontSize,lineHeight:getComputedStyle(p).lineHeight,articleWidth:article.getBoundingClientRect().width,
    sections:article.querySelectorAll('section').length,figures:article.querySelectorAll('figure').length,
    desktopToc:getComputedStyle(document.querySelector('.toc')).display,mobileToc:getComputedStyle(document.querySelector('.mobile-toc')).display,
    tables:[...article.querySelectorAll('.table-scroll')].map(e=>getComputedStyle(e).overflowX),
    code:[...article.querySelectorAll('pre')].map(e=>getComputedStyle(e).overflowX),
    figuresScroll:[...article.querySelectorAll('.concept-figure > a')].map(e=>({client:e.clientWidth,scroll:e.scrollWidth,overflow:getComputedStyle(e).overflowX}))};
  });
  if(metrics.scrollWidth>width||metrics.font!=='16px'||metrics.lineHeight!=='31.2px'||metrics.sections!==21||metrics.figures!==6)throw Error(JSON.stringify(metrics));
  if(metrics.theme!=='system'||metrics.scheme!==theme)throw Error('System theme mismatch');
  if(width===375){
   await page.locator('.mobile-toc summary').click();
   if(!await page.locator('.mobile-toc').evaluate(e=>e.open))throw Error('TOC failed');
   await page.locator('.mobile-toc a[href="#fencing"]').click();
   if(new URL(page.url()).hash!=='#fencing')throw Error('TOC anchor failed');
   await page.locator('.mobile-toc summary').click();
  }else{
   await page.locator('.toc a[href="#fencing"]').click();
   if(new URL(page.url()).hash!=='#fencing')throw Error('Desktop TOC failed');
  }
  await page.locator('#sources summary').click();
  if(!await page.locator('#sources').evaluate(e=>e.open))throw Error('Sources failed');
  await page.locator('#sources summary').click();
  await page.evaluate(()=>scrollTo(0,0));
  await page.screenshot({path:path.join(tools,`ch09-reader-${width}-${theme}.png`)});
  await page.locator('#fencing figure').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(tools,`ch09-fencing-reader-${width}-${theme}.png`)});
  const opposite=theme==='light'?'dark':'light';
  await page.locator(`[data-theme-value="${opposite}"]`).click();
  await page.reload();
  const saved=await page.evaluate(()=>({theme:document.documentElement.dataset.theme,storage:localStorage.getItem('reading-notes-theme')}));
  if(saved.theme!==opposite||saved.storage!==opposite)throw Error('Persistence failed');
  if(errors.length)throw Error(errors.join('\n'));
  results.push({...metrics,systemTheme:theme,manualSaved:saved,errors});
  await context.close();
 }
 for(const name of ['timeout','clock-order','lease-gap','fencing','replica-fencing','dst']){
  const context=await browser.newContext({viewport:{width:940,height:1000},colorScheme:'light'});
  const page=await context.newPage();
  await page.goto(base+`/books/designing-data-intensive-applications-2nd/diagrams/exports/ch09-${name}.svg`);
  const clipping=await page.evaluate(()=>{
   const root=document.querySelector('svg'),r=root.getBoundingClientRect();
   return [...root.querySelectorAll('text')].filter(t=>{
    const b=t.getBoundingClientRect();return b.left<r.left-1||b.right>r.right+1||b.top<r.top-1||b.bottom>r.bottom+1;
   }).map(t=>t.textContent);
  });
  if(clipping.length)throw Error(`Clipping ${name}: ${clipping}`);
  await page.screenshot({path:path.join(tools,`ch09-diagram-${name}-light.png`)});
  await page.evaluate(()=>localStorage.setItem('reading-notes-theme','dark'));
  await page.reload();
  if(await page.locator('svg').getAttribute('data-theme')!=='dark')throw Error('Standalone theme failed');
  await page.screenshot({path:path.join(tools,`ch09-diagram-${name}-dark.png`)});
  diagrams.push({name,clipping,standaloneSavedTheme:'dark'});
  await context.close();
 }
 await fs.writeFile(path.join(tools,'ch09-browser-results.json'),JSON.stringify({results,diagrams},null,2));
 console.log(JSON.stringify({pages:results.map(r=>({width:r.width,theme:r.systemTheme,font:r.font,lineHeight:r.lineHeight,scrollWidth:r.scrollWidth})),diagrams},null,2));
}finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
