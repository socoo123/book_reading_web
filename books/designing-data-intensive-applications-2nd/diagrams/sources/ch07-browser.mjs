// Authoring-only reader verification; ephemeral HTTP server closes at the end.
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../../..');
const out = '/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools';
const { chromium } = createRequire(path.join(out, 'package.json'))('playwright');
const server = http.createServer(async (req, res) => {
  try {
    const target = path.join(root, decodeURIComponent(new URL(req.url, 'http://local').pathname));
    const body = await fs.readFile(target);
    const mime = { '.html':'text/html; charset=utf-8', '.css':'text/css', '.js':'text/javascript', '.svg':'image/svg+xml' }[path.extname(target)] || 'application/octet-stream';
    res.writeHead(200, {'Content-Type': mime}); res.end(body);
  } catch { res.writeHead(404); res.end('Not found'); }
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const base = `http://127.0.0.1:${server.address().port}`;
const chapter = '/books/designing-data-intensive-applications-2nd/chapters/ch07.html';
const exportsPath = '/books/designing-data-intensive-applications-2nd/diagrams/exports/';
const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const results = [];
try {
  for (const width of [1440,375]) for (const theme of ['light','dark']) {
    const context = await browser.newContext({ viewport:{width,height:1000}, colorScheme:theme });
    const page = await context.newPage(); const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('response', r => { if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`); });
    await page.goto(base+chapter);
    const initial = await page.evaluate(() => getComputedStyle(document.documentElement).colorScheme);
    assert.ok(initial.includes(theme));
    await page.locator(`[data-theme-value="${theme}"]`).click();
    await page.reload();
    assert.equal(await page.evaluate(() => localStorage.getItem('reading-notes-theme')), theme);
    await page.locator('#sources summary').click();
    assert.equal(await page.locator('#sources').evaluate(x => x.open), true);
    if (width === 375) {
      await page.locator('.mobile-toc summary').click();
      await page.locator('.mobile-toc a[href="#migration"]').click();
    } else await page.locator('.toc a[href="#migration"]').click();
    assert.ok(page.url().endsWith('#migration'));
    for (const figure of await page.locator('figure').all()) {
      await figure.scrollIntoViewIfNeeded();
      await figure.locator('img').evaluate(img => img.decode());
    }
    const metrics = await page.evaluate(() => ({
      viewport:innerWidth, pageWidth:document.documentElement.scrollWidth,
      font:getComputedStyle(document.querySelector('.article')).fontSize,
      lineHeight:getComputedStyle(document.querySelector('.article')).lineHeight,
      figures:[...document.querySelectorAll('figure > a')].map(a=>({width:a.clientWidth,scroll:a.scrollWidth})),
      images:[...document.images].map(x=>({loaded:x.complete && x.naturalWidth>0, alt:!!x.alt}))
    }));
    assert.ok(metrics.pageWidth <= width+1); assert.equal(metrics.font,'16px'); assert.equal(metrics.lineHeight,'31.2px');
    assert.ok(metrics.images.every(x=>x.loaded && x.alt));
    if (width===375) assert.ok(metrics.figures.every(x=>x.scroll>x.width));
    assert.deepEqual(errors,[]);
    await page.goto(base+chapter+'#global-index');
    await page.screenshot({path:path.join(out,`ch07-reader-${width}-${theme}.png`)});
    results.push({width,theme,...metrics,errors});
    await context.close();
  }
  for (const stem of ['ch07-fixed-shards','ch07-migration','ch07-local-index','ch07-global-index']) {
    for (const theme of ['light','dark']) {
      const context = await browser.newContext({viewport:{width:1000,height:1000}, colorScheme:theme});
      const page = await context.newPage();
      await page.goto(base+exportsPath+stem+'.svg');
      const geometry = await page.evaluate(() => {
        const svg=document.querySelector('svg'), box=svg.viewBox.baseVal;
        const overflows=[...svg.querySelectorAll('text')].filter(t=>{
          const b=t.getBoundingClientRect(),r=svg.getBoundingClientRect();
          return b.left<r.left-1||b.right>r.right+1||b.top<r.top-1||b.bottom>r.bottom+1;
        }).map(t=>t.textContent);
        return {overflows,width:box.width,height:box.height,theme:getComputedStyle(svg).getPropertyValue('--text').trim()};
      });
      assert.deepEqual(geometry.overflows,[]);
      assert.equal(geometry.theme,theme==='dark'?'#e6e3dc':'#292824');
      await page.screenshot({path:path.join(out,`${stem}-${theme}.png`)});
      results.push({stem,theme,...geometry});
      await context.close();
    }
  }
  await fs.writeFile(path.join(out,'ch07-browser-results.json'),JSON.stringify(results,null,2)+'\n');
  console.log(JSON.stringify(results,null,2));
} finally {
  await browser.close();
  await new Promise(resolve => server.close(resolve));
}
