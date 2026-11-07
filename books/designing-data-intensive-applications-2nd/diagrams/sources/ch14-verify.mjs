// Chapter-only browser verification; ephemeral port and ch14-specific outputs.
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import { createRequire } from 'node:module';
const out = '/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools';
const { chromium } = createRequire(path.join(out, 'package.json'))('playwright');
const root = '/Users/zy/ai_learn/book_reading_web';
const book = '/books/designing-data-intensive-applications-2nd/';
const url = `${book}chapters/ch14.html`;
const server = http.createServer(async (req, res) => {
  try {
    const name = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
    const target = path.join(root, name.endsWith('/') ? name + 'index.html' : name);
    res.setHeader('Content-Type', ({'.html':'text/html', '.svg':'image/svg+xml', '.css':'text/css', '.js':'application/javascript'})[path.extname(target)] || 'text/plain');
    res.end(await fs.readFile(target));
  } catch { res.statusCode = 404; res.end('Not found'); }
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const origin = `http://127.0.0.1:${server.address().port}`;
const browser = await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless:true});
const results = [], errors = [];
const assert = (v, m) => { if (!v) throw new Error(m); };
try {
  const context = await browser.newContext({ colorScheme:'dark' });
  const page = await context.newPage();
  page.on('pageerror', e => errors.push(String(e)));
  page.on('response', r => { if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`); });
  await page.goto(origin + url);
  assert(await page.evaluate(() => document.documentElement.dataset.theme === 'system' && getComputedStyle(document.documentElement).colorScheme === 'dark'), 'system theme');
  for (const width of [1440,375]) for (const theme of ['light','dark']) {
    await page.setViewportSize({width,height:950});
    await page.goto(origin + url);
    await page.locator(`[data-theme-value="${theme}"]`).click();
    await page.reload();
    await page.locator('img').evaluateAll(imgs => Promise.all(imgs.map(img => { img.loading = 'eager'; return img.decode(); })));
    const data = await page.evaluate(() => {
      const p = document.querySelector('article section p'), article = document.querySelector('article');
      return {theme:document.documentElement.dataset.theme, overflow:document.documentElement.scrollWidth > innerWidth,
        font:getComputedStyle(p).fontSize, lineHeight:getComputedStyle(p).lineHeight, articleWidth:article.getBoundingClientRect().width,
        images:[...document.images].map(img => ({loaded:img.naturalWidth > 0,theme:getComputedStyle(img).colorScheme})),
        tocVisible:getComputedStyle(document.querySelector('.toc')).display !== 'none',
        mobileTocVisible:getComputedStyle(document.querySelector('.mobile-toc')).display !== 'none'};
    });
    assert(data.theme === theme && !data.overflow, `layout/theme ${width} ${theme}`);
    assert(data.font === '16px' && data.lineHeight === '31.2px' && data.articleWidth <= 720 && (width === 375 || data.articleWidth === 720), 'typography '+JSON.stringify(data));
    assert(data.images.every(i => i.loaded && i.theme === theme), 'images/theme');
    assert(width === 375 ? data.mobileTocVisible && !data.tocVisible : data.tocVisible && !data.mobileTocVisible, 'responsive TOC');
    await page.screenshot({path:`${out}/ch14-page-${width}-${theme}.png`});
    if (width === 375) {
      await page.locator('.mobile-toc summary').click();
      await page.locator('.mobile-toc a[href="#feedback-loops"]').click();
      const localScroll = await page.locator('.concept-figure > a').first().evaluate(el => {
        const before = el.scrollLeft; el.scrollLeft = 120;
        return {wide:el.scrollWidth > el.clientWidth,moved:el.scrollLeft > before};
      });
      assert(localScroll.wide && localScroll.moved, 'mobile figure local scrolling');
      await page.locator('.concept-figure').first().screenshot({path:`${out}/ch14-figure-${width}-${theme}.png`});
    } else await page.locator('.toc a[href="#feedback-loops"]').click();
    assert(page.url().endsWith('#feedback-loops'), 'TOC destination');
    await page.locator('#sources summary').click();
    assert(await page.locator('#sources').getAttribute('open') !== null, 'source disclosure');
    const prev = await page.locator('.chapter-pagination .prev').getAttribute('href');
    assert(prev === 'ch13.html', 'previous href');
    await page.locator('.chapter-pagination .next').click();
    assert(page.url().endsWith(book + 'index.html'), 'return to overview');
    results.push({type:'page',width,...data});
  }
  const svgs = (await fs.readdir(root + book + 'diagrams/exports')).filter(x => /^ch14-.*\.svg$/.test(x));
  for (const svg of svgs) for (const theme of ['light','dark']) {
    await page.goto(origin + url);
    await page.locator(`[data-theme-value="${theme}"]`).click();
    await page.setViewportSize({width:1000,height:800});
    await page.goto(origin + book + 'diagrams/exports/' + svg);
    const data = await page.evaluate(() => {
      const svg = document.documentElement, screen = svg.getBoundingClientRect();
      const cropped = [...document.querySelectorAll('text')].filter(t => {
        const b=t.getBBox(), m=t.getCTM();
        const a=new DOMPoint(b.x,b.y).matrixTransform(m), z=new DOMPoint(b.x+b.width,b.y+b.height).matrixTransform(m);
        return a.x < -1 || a.y < -1 || z.x > screen.width+1 || z.y > screen.height+1;
      }).map(t => t.textContent);
      return {theme:svg.dataset.theme,cropped,surface:getComputedStyle(svg).getPropertyValue('--surface').trim()};
    });
    assert(data.theme === theme && !data.cropped.length, 'SVG '+svg+' '+JSON.stringify(data));
    assert(data.surface === (theme === 'light' ? '#fcfbf8' : '#252524'), 'SVG palette');
    await page.screenshot({path:`${out}/ch14-${svg}-${theme}.png`});
    results.push({type:'svg',svg,...data});
  }
  assert(errors.length === 0, errors.join('\n'));
  const report={checks:results.length,errors,results,navigation:'ch14 → overview clicked; ch13 href checked (main agent integrates round)'};
  await fs.writeFile(`${out}/ch14-browser-results.json`,JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
} finally {
  await browser.close();
  await new Promise(resolve => server.close(resolve));
}
