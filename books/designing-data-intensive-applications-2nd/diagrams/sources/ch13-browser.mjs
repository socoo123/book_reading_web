// Chapter-local browser checks; starts a private ephemeral-port server and closes it.
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import {createRequire} from 'node:module';
const root='/Users/zy/ai_learn/book_reading_web';
const out='/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools';
const require=createRequire(path.join(out,'package.json'));
const {chromium}=require('playwright');
const book='/books/designing-data-intensive-applications-2nd/';
const url=book+'chapters/ch13.html';
const server=http.createServer(async(req,res)=>{
  try{
    const name=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
    const target=path.join(root,name.endsWith('/')?name+'index.html':name);
    res.setHeader('Content-Type',({'.html':'text/html','.svg':'image/svg+xml','.css':'text/css','.js':'application/javascript'})[path.extname(target)]||'text/plain');
    res.end(await fs.readFile(target));
  }catch{res.statusCode=404;res.end('Not found');}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const origin=`http://127.0.0.1:${server.address().port}`;
const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
const assert=(x,m)=>{if(!x)throw new Error(m);};
const results=[],errors=[];
try{
 const context=await browser.newContext({colorScheme:'dark'});
 const page=await context.newPage();
 page.on('pageerror',e=>errors.push(String(e)));
 page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
 await page.goto(origin+url);
 assert(await page.evaluate(()=>document.documentElement.dataset.theme==='system'&&getComputedStyle(document.documentElement).colorScheme==='dark'),'system theme');
 for(const width of [1440,375])for(const theme of ['light','dark']){
  await page.setViewportSize({width,height:950});
  await page.goto(origin+url);
  await page.locator(`[data-theme-value="${theme}"]`).click();
  await page.reload();
  await page.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(img=>{img.loading='eager';return img.decode();})));
  const data=await page.evaluate(()=>{
   const p=document.querySelector('.article section p'),article=document.querySelector('.article');
   return {theme:document.documentElement.dataset.theme,overflow:document.documentElement.scrollWidth>innerWidth,
    font:getComputedStyle(p).fontSize,lineHeight:getComputedStyle(p).lineHeight,
    articleWidth:article.getBoundingClientRect().width,maxWidth:getComputedStyle(article).maxWidth,
    images:[...document.images].map(i=>({loaded:i.naturalWidth>0,theme:getComputedStyle(i).colorScheme})),
    figureOverflow:[...document.querySelectorAll('.concept-figure > a')].map(e=>({width:e.clientWidth,scroll:e.scrollWidth}))};
  });
  assert(data.theme===theme&&!data.overflow,'theme or overflow '+JSON.stringify(data));
  assert(data.font==='16px'&&data.lineHeight==='31.2px'&&data.articleWidth<=720,'typography '+JSON.stringify(data));
  assert(data.images.every(i=>i.loaded&&i.theme===theme),'images');
  assert(await page.locator('.toc li').count()===26&&await page.locator('.mobile-toc li').count()===26,'TOC');
  await page.locator('#sources summary').click();
  assert(await page.locator('#sources').getAttribute('open')!==null,'sources');
  if(width===375){
   await page.locator('.mobile-toc summary').click();
   await page.locator('.mobile-toc a[href="#payment-recovery"]').click();
   assert(page.url().endsWith('#payment-recovery'),'mobile TOC target');
   const scroll=await page.locator('.concept-figure > a').first().evaluate(e=>{e.scrollLeft=40;return e.scrollLeft;});
   assert(scroll>0,'local figure scroll');
  }else{
   await page.locator('.toc a[href="#payment-recovery"]').click();
   assert(page.url().endsWith('#payment-recovery'),'desktop TOC target');
  }
  await page.locator('#payment-recovery').scrollIntoViewIfNeeded();
  await page.screenshot({path:`${out}/ch13-page-${width}-${theme}.png`});
  await page.locator('#payment-flow figure').screenshot({path:`${out}/ch13-figure-${width}-${theme}.png`});
  results.push({type:'page',width,...data});
 }
 const svgs=(await fs.readdir(root+book+'diagrams/exports')).filter(n=>/^ch13-.*\.svg$/.test(n));
 for(const svg of svgs)for(const theme of ['light','dark']){
  await page.goto(origin+url);
  await page.locator(`[data-theme-value="${theme}"]`).click();
  await page.setViewportSize({width:1200,height:850});
  await page.goto(origin+book+'diagrams/exports/'+svg);
  const data=await page.evaluate(()=>{
   const svg=document.documentElement,rect=svg.getBoundingClientRect();
   const cropped=[...document.querySelectorAll('text')].filter(t=>{
    const b=t.getBBox(),m=t.getCTM(),a=new DOMPoint(b.x,b.y).matrixTransform(m),z=new DOMPoint(b.x+b.width,b.y+b.height).matrixTransform(m);
    return a.x< -1||a.y< -1||z.x>rect.width+1||z.y>rect.height+1;
   }).map(t=>t.textContent);
   return{theme:svg.dataset.theme,cropped,surface:getComputedStyle(svg).getPropertyValue('--surface').trim()};
  });
  assert(data.theme===theme&&!data.cropped.length,'SVG cropping '+svg+JSON.stringify(data));
  assert(data.surface===(theme==='light'?'#fcfbf8':'#252524'),'SVG palette');
  if(theme==='light'||svg==='ch13-payment.svg')await page.screenshot({path:`${out}/ch13-svg-${svg}-${theme}.png`});
  results.push({type:'svg',svg,...data});
 }
 await page.goto(origin+url);
 await page.locator('.chapter-pagination .prev').click();
 assert(page.url().endsWith('ch12.html'),'previous chapter');
 await page.goto(origin+url);
 let next='not-yet-present';
 try{await fs.access(root+book+'chapters/ch14.html');next='present';}catch{}
 if(next==='present'){
  await page.locator('.chapter-pagination .next').click();
  assert(page.url().endsWith('ch14.html'),'next chapter');
 }
 assert(errors.length===0,errors.join('\n'));
 const report={checks:results.length,nextChapter:next,errors,results};
 await fs.writeFile(`${out}/ch13-browser-results.json`,JSON.stringify(report,null,2));
 console.log(JSON.stringify({checks:results.length,nextChapter:next,errors},null,2));
}finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
