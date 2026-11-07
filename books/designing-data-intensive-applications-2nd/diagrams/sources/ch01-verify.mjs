// Authoring-only browser checks for chapter 1; no persistent server is started.
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');
const out = '/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-ch01';
const require = createRequire('/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools/package.json');
const { chromium } = require('playwright');
const base = '/books/designing-data-intensive-applications-2nd';
const server = http.createServer(async (req, res) => {
  try {
    const file = path.join(root, decodeURIComponent(new URL(req.url, 'http://local').pathname));
    const content = await fs.readFile(file);
    const mime = { '.html': 'text/html; charset=utf-8', '.svg': 'image/svg+xml', '.js': 'text/javascript', '.css': 'text/css' };
    res.writeHead(200, { 'Content-Type': mime[path.extname(file)] || 'application/octet-stream' });
    res.end(content);
  } catch { res.writeHead(404); res.end('Not found'); }
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const origin = `http://127.0.0.1:${server.address().port}`;
const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const results = [];
const errors = [];
const check = (value, message) => { if (!value) throw new Error(message); };
try {
  for (const width of [1440, 375]) for (const theme of ['light', 'dark']) {
    const context = await browser.newContext({ viewport: { width, height: 900 }, colorScheme: theme });
    const page = await context.newPage();
    page.on('pageerror', error => errors.push(error.message));
    page.on('response', response => { if (response.status() >= 400) errors.push(`${response.status()} ${response.url()}`); });
    await page.goto(`${origin}${base}/chapters/ch01.html`);
    await page.evaluate(() => document.fonts.ready);
    const metrics = await page.evaluate(() => {
      const article = getComputedStyle(document.querySelector('.article'));
      return {
        viewport: innerWidth, documentWidth: document.documentElement.scrollWidth,
        font: article.fontSize, lineHeight: article.lineHeight,
        theme: document.documentElement.dataset.theme,
        sections: document.querySelectorAll('article section').length,
        desktopToc: getComputedStyle(document.querySelector('.toc')).display,
        mobileToc: getComputedStyle(document.querySelector('.mobile-toc')).display,
        images: [...document.querySelectorAll('.concept-figure img')].map(img => ({ loaded: img.complete && img.naturalWidth > 0, width: img.getBoundingClientRect().width, container: img.parentElement.clientWidth }))
      };
    });
    check(metrics.documentWidth <= width, `Page overflow: ${width} ${theme}`);
    check(metrics.font === '16px' && metrics.lineHeight === '31.2px', 'Typography changed');
    check(metrics.theme === 'system' && metrics.sections === 13, 'System theme / section count');
    check(width < 860 ? metrics.desktopToc === 'none' && metrics.mobileToc !== 'none' : metrics.desktopToc !== 'none' && metrics.mobileToc === 'none', 'TOC breakpoint');
    await page.screenshot({ path: `${out}/page-${width}-${theme}.png` });

    const opposite = theme === 'light' ? 'dark' : 'light';
    await page.locator(`[data-theme-value="${opposite}"]`).click();
    await page.reload();
    check(await page.evaluate(t => document.documentElement.dataset.theme === t && localStorage.getItem('reading-notes-theme') === t, opposite), 'Manual preference persistence');
    await page.locator('[data-theme-value="system"]').click();
    if (width < 860) {
      await page.locator('.mobile-toc summary').click();
      await page.locator('.mobile-toc a[href="#authority-derived"]').click();
      check(new URL(page.url()).hash === '#authority-derived', 'Mobile anchor navigation');
    }
    await page.locator('#sources summary').click();
    check(await page.locator('#sources').evaluate(e => e.open), 'Sources disclosure');
    await page.locator('#sources summary').focus();
    check(await page.evaluate(() => document.activeElement.matches('#sources summary')), 'Keyboard disclosure focus');
    for (let i = 0; i < 2; i++) {
      const figure = page.locator('.concept-figure').nth(i);
      await figure.scrollIntoViewIfNeeded();
      await page.waitForFunction(index => {
        const img = document.querySelectorAll('.concept-figure img')[index];
        return img.complete && img.naturalWidth > 0;
      }, i);
      if (width === 1440) await figure.screenshot({ path: `${out}/figure-${i + 1}-${theme}.png` });
    }
    metrics.finalImageLoad = await page.locator('.concept-figure img').evaluateAll(imgs => imgs.every(img => img.complete && img.naturalWidth > 0));
    check(metrics.finalImageLoad, 'Image load');
    if (width < 860) {
      const local = await page.locator('.concept-figure > a').evaluateAll(es => es.every(e => e.scrollWidth > e.clientWidth && getComputedStyle(e).overflowX === 'auto'));
      check(local, 'Mobile figure local scrolling');
    }
    const scrollContainers = await page.locator('.table-scroll, pre').evaluateAll(es => es.map(e => ({
      tag: e.tagName, overflowX: getComputedStyle(e).overflowX, width: e.clientWidth, contentWidth: e.scrollWidth
    })));
    check(scrollContainers.length === 3 && scrollContainers.every(e => e.overflowX === 'auto'), 'Table and code local scroll');
    if (width < 860) check(scrollContainers.every(e => e.contentWidth > e.width), 'Mobile wide content scroll');
    results.push({ ...metrics, systemColorScheme: theme, manualPersistence: true, sources: true, scrollContainers });
    await context.close();
  }
  for (const stem of ['ch01-authority-derived', 'ch01-storage-compute']) {
    const page = await browser.newPage();
    await page.goto(`${origin}${base}/diagrams/exports/${stem}.svg`);
    const geometry = await page.evaluate(() => {
      const svg = document.documentElement;
      const v = svg.viewBox.baseVal;
      const clipped = [...document.querySelectorAll('text')].filter(el => {
        const r = el.getBoundingClientRect();
        const s = svg.getBoundingClientRect();
        return r.left < s.left - 1 || r.right > s.right + 1 || r.top < s.top - 1 || r.bottom > s.bottom + 1;
      }).map(el => el.textContent);
      return { viewBox: [v.x, v.y, v.width, v.height], clipped };
    });
    check(geometry.clipped.length === 0, `${stem} text outside viewBox`);
    results.push({ stem, ...geometry });
    await page.close();
  }
  check(errors.length === 0, JSON.stringify(errors));
  await fs.writeFile(`${out}/browser-results.json`, JSON.stringify({ results, errors }, null, 2));
  console.log(JSON.stringify({ result: 'PASS', viewportThemeCases: 4, standaloneSvgBounds: 2, errors, artifacts: out }));
} finally {
  await browser.close();
  await new Promise(resolve => server.close(resolve));
}
