// Chapter-local browser checks. No database service is launched.
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../../..');
const tools = process.env.DDIA_TOOLS || '/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools';
const require = createRequire(path.join(tools, 'package.json'));
const { chromium } = require('playwright');
const mime = { '.html': 'text/html', '.svg': 'image/svg+xml', '.css': 'text/css', '.js': 'application/javascript' };
const server = http.createServer(async (req, res) => {
  try {
    const file = path.join(root, decodeURIComponent(new URL(req.url, 'http://localhost').pathname));
    res.setHeader('Content-Type', mime[path.extname(file)] || 'application/octet-stream');
    res.end(await fs.readFile(file));
  } catch { res.statusCode = 404; res.end('Not found'); }
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const base = `http://127.0.0.1:${server.address().port}`;
const url = base + '/books/designing-data-intensive-applications-2nd/chapters/ch06.html';
const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const pages = [], figures = [];
const onlyFigure = process.argv[2];
try {
  for (const width of onlyFigure ? [] : [1440, 375]) for (const theme of ['light', 'dark']) {
    const context = await browser.newContext({ viewport: { width, height: 960 }, colorScheme: theme });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('response', r => { if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`); });
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.locator('img').evaluateAll(imgs => imgs.forEach(i => i.loading = 'eager'));
    await page.waitForFunction(() => [...document.images].every(i => i.complete && i.naturalWidth));
    const metrics = await page.evaluate(() => {
      const p = document.querySelector('section p');
      return { width: innerWidth, scrollWidth: document.documentElement.scrollWidth,
        font: getComputedStyle(p).fontSize, lineHeight: getComputedStyle(p).lineHeight,
        background: getComputedStyle(document.body).backgroundColor,
        sections: document.querySelectorAll('article section').length,
        images: document.images.length, theme: document.documentElement.dataset.theme,
        mobileFigureScroll: [...document.querySelectorAll('.concept-figure > a')].map(a => ({ client: a.clientWidth, scroll: a.scrollWidth })) };
    });
    if (metrics.scrollWidth > width || metrics.font !== '16px' || metrics.lineHeight !== '31.2px' || metrics.sections !== 21 || metrics.images !== 5) throw Error(JSON.stringify(metrics));
    if (width === 375) {
      await page.locator('.mobile-toc summary').click();
      if (!await page.locator('.mobile-toc').evaluate(e => e.open)) throw Error('Mobile TOC');
      await page.locator('.mobile-toc a[href="#quorum"]').click();
      if (!page.url().endsWith('#quorum')) throw Error('TOC link');
      await page.locator('.mobile-toc summary').click();
    }
    await page.locator('#sources summary').click();
    if (!await page.locator('#sources').evaluate(e => e.open)) throw Error('Sources');
    await page.locator('#sources summary').click();
    await page.evaluate(() => scrollTo(0, 0));
    await page.screenshot({ path: path.join(tools, `ch06-reader-${width}-${theme}.png`) });
    await page.locator('#quorum-limits figure').scrollIntoViewIfNeeded();
    await page.screenshot({ path: path.join(tools, `ch06-quorum-${width}-${theme}.png`) });
    const opposite = theme === 'light' ? 'dark' : 'light';
    await page.locator(`[data-theme-value="${opposite}"]`).click();
    await page.reload();
    const saved = await page.evaluate(() => ({ theme: document.documentElement.dataset.theme, value: localStorage.getItem('reading-notes-theme') }));
    if (saved.theme !== opposite || saved.value !== opposite || errors.length) throw Error(JSON.stringify({ saved, errors }));
    pages.push({ ...metrics, systemTheme: theme, saved, errors });
    await context.close();
  }
  for (const stem of ['sync-ack', 'local-first', 'quorum-intersection', 'quorum-inflight', 'causal-versions']) {
    if (onlyFigure && stem !== onlyFigure) continue;
    for (const theme of ['light', 'dark']) {
      const context = await browser.newContext({ viewport: { width: 920, height: 850 }, colorScheme: theme });
      const page = await context.newPage();
      await page.goto(base + `/books/designing-data-intensive-applications-2nd/diagrams/exports/ch06-${stem}.svg`);
      const metrics = await page.evaluate(() => {
        const svg = document.querySelector('svg'), r = svg.getBoundingClientRect();
        const clipped = [...svg.querySelectorAll('text')].filter(t => {
          const b = t.getBoundingClientRect();
          return b.left < r.left - 1 || b.right > r.right + 1 || b.top < r.top - 1 || b.bottom > r.bottom + 1;
        }).map(t => t.textContent);
        return { clipped, textColor: getComputedStyle(svg).getPropertyValue('--text').trim() };
      });
      if (metrics.clipped.length || metrics.textColor !== (theme === 'dark' ? '#e6e3dc' : '#292824')) throw Error(JSON.stringify({ stem, theme, metrics }));
      await page.screenshot({ path: path.join(tools, `ch06-diagram-${stem}-${theme}.png`) });
      if (stem === 'sync-ack' && theme === 'light') {
        await page.evaluate(() => localStorage.setItem('reading-notes-theme', 'dark'));
        await page.reload();
        if (await page.locator('svg').getAttribute('data-theme') !== 'dark') throw Error('Standalone manual theme');
      }
      figures.push({ stem, theme, ...metrics });
      await context.close();
    }
  }
  await fs.writeFile(path.join(tools, `ch06-browser-results${onlyFigure ? '-' + onlyFigure : ''}.json`), JSON.stringify({ pages, figures }, null, 2));
  console.log(JSON.stringify({ pageCases: pages.length, figureCases: figures.length, passed: true, artifacts: tools }));
} finally {
  await browser.close();
  await new Promise(resolve => server.close(resolve));
}
