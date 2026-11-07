// Authoring-only Chrome checks. Dependencies use the prepared DDIA tools directory.
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../../..');
const temp = '/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-ch03';
const tools = process.env.DDIA_TOOLS || path.resolve(temp, '../ddia2-tools');
const require = createRequire(path.join(tools, 'package.json'));
const { chromium } = require('playwright');
const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml' };
const server = http.createServer(async (req, res) => {
  try {
    const file = path.join(root, decodeURIComponent(new URL(req.url, 'http://local').pathname));
    const data = await fs.readFile(file);
    res.writeHead(200, { 'Content-Type': types[path.extname(file)] || 'application/octet-stream' });
    res.end(data);
  } catch { res.writeHead(404); res.end('not found'); }
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const origin = `http://127.0.0.1:${server.address().port}`;
const route = '/books/designing-data-intensive-applications-2nd/chapters/ch03.html';
const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const results = [];
try {
  for (const width of [1440, 375]) for (const theme of ['light', 'dark']) {
    const context = await browser.newContext({ viewport: { width, height: 900 }, colorScheme: theme });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('response', response => { if (response.status() >= 400) errors.push(`${response.status()} ${response.url()}`); });
    await page.goto(origin + route);
    await page.locator('.concept-figure img').evaluateAll(images => Promise.all(images.map(image => {
      image.loading = 'eager';
      return image.decode();
    })));
    const checks = await page.evaluate(() => {
      const ids = [...document.querySelectorAll('[id]')].map(e => e.id);
      const anchors = [...document.querySelectorAll('a[href^="#"]')].map(e => e.getAttribute('href').slice(1));
      const style = getComputedStyle(document.querySelector('.article > section p'));
      return {
        overflow: document.documentElement.scrollWidth > innerWidth,
        fontSize: style.fontSize, lineHeight: style.lineHeight,
        sections: document.querySelectorAll('.article > section').length,
        figures: document.querySelectorAll('figure').length,
        duplicateIds: ids.filter((id, index) => ids.indexOf(id) !== index),
        missingAnchors: anchors.filter(id => !document.getElementById(id)),
        forbiddenLinks: [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')).filter(h => /originals\/|notes\/|\/sources\/|\.pdf(?:$|#)|\.md(?:$|#)/.test(h)),
        imagesLoaded: [...document.images].every(image => image.complete && image.naturalWidth > 0),
        localScroll: [...document.querySelectorAll('.table-scroll, pre, .concept-figure')].some(e => e.scrollWidth > e.clientWidth),
        theme: getComputedStyle(document.documentElement).colorScheme,
      };
    });
    if (checks.overflow || checks.duplicateIds.length || checks.missingAnchors.length || checks.forbiddenLinks.length || !checks.imagesLoaded || checks.fontSize !== '16px') throw new Error(JSON.stringify(checks));
    await page.screenshot({ path: path.join(temp, `${width}-${theme}-top.png`) });
    if (width === 1440) {
      for (let i = 0; i < 3; i++) await page.locator('figure').nth(i).screenshot({ path: path.join(temp, `figure-${i + 1}-${theme}.png`) });
    }
    if (width === 375) {
      await page.locator('.mobile-toc summary').click();
      if (!(await page.locator('.mobile-toc').getAttribute('open') === '')) throw new Error('Mobile TOC did not open');
      await page.locator('.mobile-toc summary').click();
      await page.locator('figure').first().screenshot({ path: path.join(temp, `mobile-figure-${theme}.png`) });
    }
    await page.locator('#sources summary').click();
    if (!(await page.locator('#sources').getAttribute('open') === '')) throw new Error('Sources did not open');
    await page.locator('[data-theme-value="dark"]').click();
    await page.reload();
    const saved = await page.evaluate(() => ({ value: localStorage.getItem('reading-notes-theme'), theme: document.documentElement.dataset.theme }));
    if (saved.value !== 'dark' || saved.theme !== 'dark') throw new Error(JSON.stringify(saved));
    if (errors.length) throw new Error(errors.join('\n'));
    results.push({ width, theme, ...checks, saved, errors });
    await context.close();
  }
  await fs.writeFile(path.join(temp, 'browser-results.json'), JSON.stringify(results, null, 2));
  console.log(JSON.stringify(results, null, 2));
} finally {
  await browser.close();
  await new Promise(resolve => server.close(resolve));
}
