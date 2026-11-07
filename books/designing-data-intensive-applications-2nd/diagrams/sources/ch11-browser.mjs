// Chapter-11-only authoring verification. The ephemeral server closes on completion.
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'../../../..');
const out='/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools';
const {chromium}=createRequire(path.join(out,'package.json'))('playwright');
const server=http.createServer(async(req,res)=>{
  try {
    const target=path.join(root,decodeURIComponent(new URL(req.url,'http://local').pathname));
    const body=await fs.readFile(target);
    const mime={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml'}[path.extname(target)]||'application/octet-stream';
    res.writeHead(200,{'Content-Type':mime});res.end(body);
  }catch{res.writeHead(404);res.end('Not found');}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const base=`http://127.0.0.1:${server.address().port}`;
const chapter='/books/designing-data-intensive-applications-2nd/chapters/ch11.html';
const exportsPath='/books/designing-data-intensive-applications-2nd/diagrams/exports/';
const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
const results=[];
try {
  for(const width of [1440,375]) for(const theme of ['light','dark']) {
    const context=await browser.newContext({viewport:{width,height:1000},colorScheme:theme});
    const page=await context.newPage(),errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
    await page.goto(base+chapter);
    assert.ok((await page.evaluate(()=>getComputedStyle(document.documentElement).colorScheme)).includes(theme));
    // Explicit manual override opposite to system, persistence, and return to chosen theme.
    const opposite=theme==='light'?'dark':'light';
    await page.locator(`[data-theme-value="${opposite}"]`).click();await page.reload();
    assert.equal(await page.evaluate(()=>localStorage.getItem('reading-notes-theme')),opposite);
    await page.locator(`[data-theme-value="${theme}"]`).click();
    await page.locator('#sources summary').click();assert.equal(await page.locator('#sources').evaluate(x=>x.open),true);
    if(width===375){await page.locator('.mobile-toc summary').click();await page.locator('.mobile-toc a[href="#shuffle"]').click();}
    else await page.locator('.toc a[href="#shuffle"]').click();
    assert.ok(page.url().endsWith('#shuffle'));
    for(const figure of await page.locator('figure').all()){
      await figure.scrollIntoViewIfNeeded();await figure.locator('img').evaluate(img=>img.decode());
    }
    const metrics=await page.evaluate(()=>({
      viewport:innerWidth,pageWidth:document.documentElement.scrollWidth,
      font:getComputedStyle(document.querySelector('.article')).fontSize,
      lineHeight:getComputedStyle(document.querySelector('.article')).lineHeight,
      figures:[...document.querySelectorAll('figure>a')].map(a=>({width:a.clientWidth,scroll:a.scrollWidth})),
      images:[...document.images].map(i=>({loaded:i.complete&&i.naturalWidth>0,alt:!!i.alt})),
      localScroll:[...document.querySelectorAll('pre,.table-scroll')].map(x=>({width:x.clientWidth,scroll:x.scrollWidth})),
      navigation:[...document.querySelectorAll('.chapter-pagination .page-link')].map(a=>a.getAttribute('href'))
    }));
    assert.ok(metrics.pageWidth<=width+1);assert.equal(metrics.font,'16px');assert.equal(metrics.lineHeight,'31.2px');
    assert.ok(metrics.images.every(x=>x.loaded&&x.alt));
    if(width===375){assert.ok(metrics.figures.every(x=>x.scroll>x.width));assert.ok(metrics.localScroll.some(x=>x.scroll>x.width));}
    assert.deepEqual(metrics.navigation,['ch10.html','ch12.html']);assert.deepEqual(errors,[]);
    await page.goto(base+chapter+'#publish');await page.screenshot({path:path.join(out,`ch11-reader-${width}-${theme}.png`)});
    if(width===375&&theme==='dark'){
      await page.locator('#shuffle figure').scrollIntoViewIfNeeded();
      await page.screenshot({path:path.join(out,'ch11-reader-mobile-figure-dark.png')});
    }
    results.push({width,theme,...metrics,errors});await context.close();
  }
  for(const stem of ['ch11-layers','ch11-shuffle','ch11-join','ch11-publish']) for(const theme of ['light','dark']){
    const context=await browser.newContext({viewport:{width:1100,height:1000},colorScheme:theme});
    const page=await context.newPage();await page.goto(base+exportsPath+stem+'.svg');
    const geometry=await page.evaluate(()=>{
      const svg=document.querySelector('svg'),r=svg.getBoundingClientRect();
      const overflows=[...svg.querySelectorAll('text')].filter(t=>{const b=t.getBoundingClientRect();return b.left<r.left-1||b.right>r.right+1||b.top<r.top-1||b.bottom>r.bottom+1;}).map(t=>t.textContent);
      return {overflows,theme:getComputedStyle(svg).getPropertyValue('--text').trim(),width:svg.viewBox.baseVal.width,height:svg.viewBox.baseVal.height};
    });
    assert.deepEqual(geometry.overflows,[]);assert.equal(geometry.theme,theme==='dark'?'#e6e3dc':'#292824');
    await page.screenshot({path:path.join(out,`${stem}-${theme}.png`)});
    results.push({stem,theme,...geometry});await context.close();
  }
  await fs.writeFile(path.join(out,'ch11-browser-results.json'),JSON.stringify(results,null,2)+'\n');
  console.log(JSON.stringify(results,null,2));
} finally {await browser.close();await new Promise(resolve=>server.close(resolve));}
