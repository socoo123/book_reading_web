// Chapter-local browser / resource verification, without persistent dev server.
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'../../../..');
const tools=process.env.DDIA_TOOLS || '/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools';
const require=createRequire(path.join(tools,'package.json'));
const {chromium}=require('playwright');
const mime={'.html':'text/html','.svg':'image/svg+xml','.css':'text/css','.js':'application/javascript'};
const server=http.createServer(async(req,res)=>{
  try{
    const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
    const filename=path.join(root,pathname==='/'?'index.html':pathname);
    res.setHeader('Content-Type',mime[path.extname(filename)]||'application/octet-stream');
    res.end(await fs.readFile(filename));
  }catch{res.statusCode=404;res.end('Not found');}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const base=`http://127.0.0.1:${server.address().port}`;
const chapter='/books/designing-data-intensive-applications-2nd/chapters/ch05.html';
const results=[],pending=[];
const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
try{
  const resourcePage=await browser.newPage();
  await resourcePage.goto(base+chapter);
  const refs=await resourcePage.locator('[href],[src]').evaluateAll(ns=>ns.flatMap(n=>['href','src'].filter(a=>n.hasAttribute(a)).map(a=>n.getAttribute(a))));
  for(const ref of new Set(refs)){
    const u=new URL(ref,base+chapter);
    if(u.origin!==base)continue;
    if(/\/(notes|originals|sources)\//.test(u.pathname))throw Error('Unpublished dependency '+ref);
    let content;
    try{content=await fs.readFile(path.join(root,decodeURIComponent(u.pathname)),'utf8');}
    catch(e){if(/\/ch0[68]\.html$/.test(u.pathname)){pending.push(ref);continue;}throw e;}
    if(u.hash&&!new RegExp(`id=["']${u.hash.slice(1)}["']`).test(content))throw Error('Missing anchor '+ref);
  }
  const numberCheck=await resourcePage.evaluate(()=>({rounded:JSON.parse('9007199254740993'),exact:JSON.parse('9007199254740994')}));
  if(numberCheck.rounded!==9007199254740992||numberCheck.exact!==9007199254740994)throw Error('JSON integer check');
  await resourcePage.close();
  for(const width of [1440,375])for(const theme of ['light','dark']){
    const context=await browser.newContext({viewport:{width,height:960},colorScheme:theme});
    const page=await context.newPage(),errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
    await page.goto(base+chapter,{waitUntil:'networkidle'});
    await page.locator('img').evaluateAll(images=>images.forEach(i=>i.loading='eager'));
    await page.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0));
    const metrics=await page.evaluate(()=>{
      const p=document.querySelector('.article section p'),ids=[...document.querySelectorAll('[id]')].map(e=>e.id);
      return {width:innerWidth,scrollWidth:document.documentElement.scrollWidth,theme:document.documentElement.dataset.theme,
        font:getComputedStyle(p).fontSize,lineHeight:getComputedStyle(p).lineHeight,sections:document.querySelectorAll('.article section').length,
        figures:document.querySelectorAll('figure').length,duplicateIDs:ids.filter((id,i)=>ids.indexOf(id)!==i),
        figureScroll:[...document.querySelectorAll('.concept-figure>a')].map(e=>({client:e.clientWidth,scroll:e.scrollWidth,overflow:getComputedStyle(e).overflowX}))};
    });
    if(metrics.scrollWidth>width||metrics.font!=='16px'||metrics.duplicateIDs.length||metrics.sections!==15||metrics.figures!==3)throw Error(JSON.stringify(metrics));
    if(width===375){await page.locator('.mobile-toc summary').click();await page.locator('.mobile-toc a[href="#bytes"]').click();if(!page.url().endsWith('#bytes'))throw Error('TOC navigation');await page.locator('.mobile-toc summary').click();}
    else{await page.locator('.toc a[href="#bytes"]').click();if(!page.url().endsWith('#bytes'))throw Error('TOC navigation');}
    await page.locator('#sources summary').click();
    if(!await page.locator('#sources').evaluate(e=>e.open))throw Error('Sources did not open');
    await page.locator('#sources summary').click();
    await page.evaluate(()=>scrollTo(0,0));
    await page.screenshot({path:path.join(tools,`ch05-reader-${width}-${theme}.png`)});
    await page.locator('#durable-boundary figure').scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join(tools,`ch05-workflow-${width}-${theme}.png`)});
    const opposite=theme==='light'?'dark':'light';
    await page.locator(`[data-theme-value="${opposite}"]`).click();
    await page.reload();
    const saved=await page.evaluate(()=>({theme:document.documentElement.dataset.theme,storage:localStorage.getItem('reading-notes-theme')}));
    if(saved.theme!==opposite||saved.storage!==opposite)throw Error('Theme persistence failed');
    if(errors.length)throw Error(errors.join('\n'));
    results.push({...metrics,systemTheme:theme,manualSaved:saved,errors});
    await context.close();
  }
  const diagrams=[];
  for(const stem of ['compatibility','avro-resolution','durable-boundary'])for(const theme of ['light','dark']){
    const context=await browser.newContext({viewport:{width:950,height:1000},colorScheme:theme});
    const page=await context.newPage();
    await page.goto(base+`/books/designing-data-intensive-applications-2nd/diagrams/exports/ch05-${stem}.svg`);
    const clipping=await page.evaluate(()=>{
      const root=document.querySelector('svg');
      return [...root.querySelectorAll('text')].filter(t=>{
        const b=t.getBoundingClientRect(),r=root.getBoundingClientRect();
        return b.left<r.left-1||b.right>r.right+1||b.top<r.top-1||b.bottom>r.bottom+1;
      }).map(t=>t.textContent);
    });
    if(clipping.length)throw Error('Clipped SVG text: '+clipping.join(','));
    await page.screenshot({path:path.join(tools,`ch05-diagram-${stem}-${theme}.png`)});
    diagrams.push({stem,theme,clipping});
    await context.close();
  }
  const output={resourceRefs:new Set(refs).size,pendingSameRound:pending,numberCheck,results,diagrams};
  await fs.writeFile(path.join(tools,'ch05-browser-results.json'),JSON.stringify(output,null,2)+'\n');
  console.log(JSON.stringify(output,null,2));
}finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
