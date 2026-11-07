// Authoring-only tool. Dependencies live outside the website; see ../../README.md.
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const tools = process.env.DDIA_TOOLS || '/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools';
const require = createRequire(path.join(tools, 'package.json'));
const { build } = require('esbuild');
const { chromium } = require('playwright');
const input = path.resolve(process.argv[2] || path.join(here, 'overview-dataflow.skeleton.json'));
const stem = path.basename(input).replace(/\.skeleton\.json$|\.excalidraw$/, '');
const title = process.argv[3] || '从权威记录到派生视图';
const description = process.argv[4] || '实线从业务输入到权威记录系统；虚线从权威记录到派生视图。更新可能滞后，重建需要源数据与转换条件仍可用。';
const escapeXml = value => value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
const result = await build({ entryPoints: [path.join(here, 'excalidraw-browser.js')],
  bundle: true, write: false, format: 'iife', nodePaths: [path.join(tools, 'node_modules')],
  define: { 'process.env.NODE_ENV': '"production"' }, loader: { '.woff2': 'dataurl' } });
const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1200, height: 800 } });
  await page.route('http://ddia-authoring.local/**', route => route.fulfill({ contentType: 'text/html', body: '<!doctype html><div id="editor" style="height:760px"></div>' }));
  await page.goto('http://ddia-authoring.local/');
  await page.addScriptTag({ content: result.outputFiles[0].text });
  const source = JSON.parse(await fs.readFile(input, 'utf8'));
  const exported = await page.evaluate(async (source) => {
    const api = window.diagramTools;
    const elements = Array.isArray(source) ? api.convertToExcalidrawElements(source) : api.restoreElements(source.elements, null);
    const scene = { type: 'excalidraw', version: 2, source: 'https://excalidraw.com', elements,
      appState: { viewBackgroundColor: '#fcfbf8', theme: 'light', exportBackground: true }, files: {} };
    const svg = await api.exportToSvg({ elements, appState: { ...scene.appState, exportWithDarkMode: false, exportEmbedScene: false }, files: {}, exportPadding: 24 });
    return { scene, svg: svg.outerHTML };
  }, source);
  await fs.writeFile(path.join(here, `${stem}.excalidraw`), JSON.stringify(exported.scene, null, 2) + '\n');
  // Preserve Excalidraw geometry; add site palette, accessible title, and standalone theme support.
  let svg = exported.svg;
  const colors = { '#fcfbf8':'surface', '#292824':'text', '#66645d':'muted', '#f0ece4':'soft', '#386d74':'accent' };
  for (const [hex, name] of Object.entries(colors)) svg = svg.replaceAll(hex, `var(--${name})`);
  svg = svg.replace(/font-family="[^"]*"/g, 'font-family="Helvetica, Arial, PingFang SC, Microsoft YaHei, sans-serif"');
  const metadata = `<title id="diagram-title">${escapeXml(title)}</title><desc id="diagram-desc">${escapeXml(description)}</desc>
<style>:root{--surface:#fcfbf8;--text:#292824;--muted:#66645d;--soft:#f0ece4;--accent:#386d74}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){--surface:#252524;--text:#e6e3dc;--muted:#b6b1a7;--soft:#353534;--accent:#94c8cf}}
:root[data-theme="dark"]{--surface:#252524;--text:#e6e3dc;--muted:#b6b1a7;--soft:#353534;--accent:#94c8cf}</style>`;
  svg = svg.replace(/<svg\b([^>]*)>/, `<svg$1 role="img" aria-labelledby="diagram-title diagram-desc">${metadata}`);
  svg = svg.replace('</svg>', `<script><![CDATA[try{const t=localStorage.getItem('reading-notes-theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t);}catch{}]]></script></svg>`);
  const out = path.resolve(here, '../exports');
  await fs.mkdir(out, { recursive: true });
  await fs.writeFile(path.join(out, `${stem}.svg`), svg + '\n');
  // Reload the saved scene through the official restore + editor API, then edit and restore one label.
  const roundTrip = await page.evaluate(async scene => {
    await window.mountEditor(scene);
    const api = window.editorAPI;
    await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    const elements = api.getSceneElements();
    const label = elements.find(e => e.type === 'text');
    api.updateScene({ elements: elements.map(e => e.id === label.id ? { ...e, text: label.text + '（校验）' } : e) });
    await new Promise(resolve => requestAnimationFrame(resolve));
    const editable = api.getSceneElements().find(e => e.id === label.id).text.endsWith('（校验）');
    api.updateScene({ elements });
    return { elements: elements.length, editable };
  }, JSON.parse(await fs.readFile(path.join(here, `${stem}.excalidraw`), 'utf8')));
  if (!roundTrip.editable) throw new Error('Editor round-trip failed');
  console.log(JSON.stringify({ input, output: path.join(out, `${stem}.svg`), ...roundTrip }));
} finally { await browser.close(); }
