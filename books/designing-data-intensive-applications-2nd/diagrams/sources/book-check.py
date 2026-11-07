"""Whole-book publication/parity checks. Usage: python3 book-check.py OUTPUT_DIR.

OUTPUT_DIR may contain round5-baseline.json and round5-before-chapters.json.
Dependencies: Python-Markdown; no website runtime dependencies.
"""
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import markdown

BOOK = Path(__file__).resolve().parents[2]
ROOT = BOOK.parents[1]
OUT = Path(sys.argv[1])
compact = lambda s: re.sub(r'\s+', '', s)


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links, self.images, self.text = [], [], [], []
        self.counts = Counter()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.counts[tag] += 1
        if 'id' in a:
            self.ids.append(a['id'])
        if tag in ('a', 'link') and 'href' in a:
            self.links.append(a['href'])
        if tag in ('img', 'script') and 'src' in a:
            self.links.append(a['src'])
        if tag == 'img':
            self.images.append(a)

    def handle_data(self, data):
        self.text.append(data)


def text(value):
    return compact(''.join(Document(value).text))


def render(value):
    return markdown.markdown(value, extensions=['tables', 'fenced_code'])


def sections(value):
    return dict(re.findall(r'<section\b[^>]*id="([^"]+)"[^>]*>(.*?)</section>', value, re.S))


def web_file(p):
    return not {'notes', 'sources', 'originals'}.intersection(p.parts) and p.suffix in {
        '.html', '.css', '.js', '.svg', '.png', '.jpg', '.jpeg', '.webp', '.avif', '.gif', '.ico', '.woff', '.woff2'}


pages = [ROOT / 'index.html', BOOK / 'index.html', BOOK / 'guide.html', *sorted((BOOK / 'chapters').glob('ch??.html'))]
docs = {p: Document(p.read_text()) for p in pages}
page_results = []
for p, doc in docs.items():
    assert len(doc.ids) == len(set(doc.ids)), f'duplicate IDs: {p}'
    for link in doc.links:
        u = urlsplit(link)
        if u.scheme or u.netloc:
            continue
        target = (p.parent / unquote(u.path)).resolve() if u.path else p
        if target.is_dir():
            target /= 'index.html'
        assert target.exists(), f'{p}: missing {link}'
        assert web_file(target.relative_to(ROOT)), f'{p}: excluded publication target {link}'
        if u.fragment and target.suffix == '.html':
            td = docs.get(target) or Document(target.read_text())
            assert unquote(u.fragment) in td.ids, f'{p}: missing anchor {link}'
    assert all(i.get('alt', '').strip() for i in doc.images), f'{p}: missing alt'
    page_results.append({'page': str(p.relative_to(ROOT)), 'references': len(doc.links), 'images': len(doc.images)})

stats = []
for name in [f'ch{n:02}' for n in range(1, 15)] + ['guide']:
    md = (BOOK / f'notes/{name}.md').read_text()
    hp = BOOK / (f'chapters/{name}.html' if name != 'guide' else 'guide.html')
    html = hp.read_text()
    md_body = md.split('<details', 1)[0]
    chunks = re.split(r'<a id="([^"]+)"></a>\s*(?=## )', md_body)
    hs = sections(html)
    checked = []
    for i in range(1, len(chunks), 2):
        anchor, content = chunks[i:i+2]
        assert text(render(content)) == text(hs[anchor]), f'{name}: section differs {anchor}'
        checked.append(anchor)
    assert len(checked) == len(re.findall(r'^## ', md, re.M)), f'{name}: unverified sections'
    ms = re.search(r'<details\b[^>]*id="sources"[^>]*>(.*?)</details>', md, re.S).group(1)
    hsources = re.search(r'<details\b[^>]*id="sources"[^>]*>(.*?)</details>', html, re.S).group(1)
    strip_summary = lambda s: re.sub(r'<summary>.*?</summary>', '', s, flags=re.S)
    assert text(render(strip_summary(ms))) == text(strip_summary(hsources)), f'{name}: source differs'
    intro = chunks[0].split('\n\n', 2)[-1] if name != 'guide' else chunks[0].split('\n\n', 1)[-1]
    assert text(render(intro)) in text(html), f'{name}: intro differs'
    md_render = Document(render(re.sub(r'</?details[^>]*>|<summary>.*?</summary>', '', md)))
    for tag in ('table', 'pre'):
        assert md_render.counts[tag] == docs[hp].counts[tag], f'{name}: {tag} count'
    # Markdown links must resolve locally too, including cross-book destinations.
    for link in md_render.links:
        u = urlsplit(link)
        if u.scheme or u.netloc:
            continue
        target = (BOOK / 'notes' / unquote(u.path)).resolve() if u.path else BOOK / f'notes/{name}.md'
        assert target.exists(), f'{name}: Markdown link {link}'
        if u.fragment:
            assert f'id="{unquote(u.fragment)}"' in target.read_text(), f'{name}: Markdown anchor {link}'
    stats.append({'name': name, 'sections': len(checked), 'whole_sections_matched': checked,
                  'source_matched': True, 'intro_matched': True,
                  'tables': docs[hp].counts['table'], 'code_blocks': docs[hp].counts['pre'],
                  'figures': docs[hp].counts['figure'],
                  'body_han': len(re.findall(r'[\u3400-\u9fff]', re.sub(r'```.*?```', '', md_body, flags=re.S)))})
assert sum(s['sections'] for s in stats[:-1]) == 250
assert sum(s['figures'] for s in stats[:-1]) == 64

diagrams = []
for p in sorted((BOOK / 'diagrams/sources').glob('*.excalidraw')):
    scene = json.loads(p.read_text())
    svg = BOOK / 'diagrams/exports' / (p.stem + '.svg')
    tree = ET.parse(svg)
    svg_text = compact(''.join(tree.getroot().itertext()))
    elements = [e for e in scene['elements'] if not e.get('isDeleted')]
    assert scene['type'] == 'excalidraw' and elements
    ids = {e['id'] for e in elements}
    assert len(ids) == len(elements), f'{p}: duplicate elements'
    for e in elements:
        if e['type'] == 'text':
            assert compact(e['text']) in svg_text, f'{p}: missing text {e["text"]}'
        for key in ('startBinding', 'endBinding'):
            if e.get(key):
                assert e[key]['elementId'] in ids, f'{p}: broken arrow binding'
    assert '--surface' in svg.read_text() and 'prefers-color-scheme' in svg.read_text()
    diagrams.append({'name': p.stem, 'elements': len(elements)})
assert len(diagrams) == 65
assert {d['name'] for d in diagrams} == {p.stem for p in (BOOK / 'diagrams/exports').glob('*.svg')}

preservation = []
before = OUT / 'round5-before-chapters.json'
if before.exists():
    for name, old in json.loads(before.read_text()).items():
        old_sections = sections(old)
        new_sections = sections((BOOK / 'chapters' / name).read_text())
        assert old_sections.keys() == new_sections.keys(), f'{name}: changed section set'
        for anchor, value in old_sections.items():
            a, b = text(value), text(new_sections[anchor])
            if name == 'ch01.html' and anchor == 'lake-pipelines':
                b = b.replace('，持续传播见第12章CDC', '')
            if name == 'ch08.html':
                a = a.replace('本轮先保留这个清楚的局部保证', '本章先保留这个清楚的局部保证')
            assert a == b, f'{name}: unexpected body change {anchor}'
        old_source = re.search(r'<details\b[^>]*id="sources"[^>]*>(.*?)</details>', old, re.S).group(1)
        new_source = re.search(r'<details\b[^>]*id="sources"[^>]*>(.*?)</details>', (BOOK / 'chapters' / name).read_text(), re.S).group(1)
        assert text(old_source) == text(new_source), f'{name}: historical source changed'
        preservation.append({'chapter': name, 'sections_preserved': len(old_sections), 'historical_source_preserved': True})

baseline_result = None
baseline = OUT / 'round5-baseline.json'
if baseline.exists():
    hashes = json.loads(baseline.read_text())
    changed = []
    for name, digest in hashes.items():
        p = Path(name)
        assert p.exists(), f'baseline file removed: {p}'
        if hashlib.sha256(p.read_bytes()).hexdigest() != digest:
            assert p.is_relative_to(BOOK), f'outside book changed: {p}'
            assert p.suffix not in ('.svg', '.excalidraw') and 'originals' not in p.parts and not p.name.endswith('-report.md'), f'protected material changed: {p}'
            changed.append(str(p.relative_to(ROOT)))
    baseline_result = {'total': len(hashes), 'unchanged': len(hashes)-len(changed), 'changed': changed}

published = sorted(str(p.relative_to(ROOT)) for p in BOOK.rglob('*') if p.is_file() and web_file(p.relative_to(ROOT)))
assert len(published) == 81
result = {'pages': page_results, 'statistics': stats, 'diagrams': diagrams,
          'preservation': preservation, 'baseline': baseline_result,
          'published_count': len(published), 'published': published}
(OUT / 'round5-static-results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
print(json.dumps({'pages': len(pages), 'references': sum(p['references'] for p in page_results),
                  'sections': sum(s['sections'] for s in stats), 'diagrams': len(diagrams),
                  'published': len(published), 'baseline': baseline_result}, ensure_ascii=False, indent=2))
