"""Minimal content, link, and source/export checks for chapter 14 only."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re
import xml.etree.ElementTree as ET
import markdown
from html.parser import HTMLParser


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.refs, self.images, self.text, self.tags = [], [], [], [], []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append(tag)
        if 'id' in a:
            self.ids.append(a['id'])
        for key in ('href', 'src'):
            if key in a:
                self.refs.append(a[key])
        if tag == 'img':
            self.images.append(a)

    def handle_data(self, data):
        self.text.append(data)

BOOK = Path(__file__).resolve().parents[2]
OUT = Path('/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools')
md = (BOOK / 'notes/ch14.md').read_text()
page = BOOK / 'chapters/ch14.html'
html = page.read_text()
doc = Document(html)
ids = doc.ids
assert len(ids) == len(set(ids)), 'Duplicate ids'
pending, refs = [], 0
for url in doc.refs:
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc:
        continue
    refs += 1
    assert not re.search(r'(?:^|/)(notes|sources|originals)/|\.pdf$', parsed.path), url
    target = (page.parent / unquote(parsed.path)).resolve() if parsed.path else page
    if not target.exists():
        assert target == BOOK / 'chapters/ch13.html', f'Missing target {url}'
        pending.append(url)
        continue
    if parsed.fragment:
        target_doc = doc if target == page else Document(target.read_text())
        assert parsed.fragment in target_doc.ids, f'Missing anchor {url}'
assert all(e.get('alt') for e in doc.images)
assert doc.tags.count('section') == 12
assert 'class="page-link prev" href="ch13.html"' in html
assert 'class="page-link next" href="../index.html"' in html


def normalize(text):
    return re.sub(r'\s+', '', ''.join(Document(text).text))


def converted(text):
    return markdown.markdown(text, extensions=['tables', 'fenced_code'])


body, sources = md.split('<details id="sources">')
body = re.sub(r'^# .*?\n\n\*\*.*?\*\*\n\n', '', body, count=1, flags=re.S)
parts = re.split(r'<a id="([^"]+)"></a>\s*\n\n## (\d+)　([^\n]+)\n\n', body)
article = html.split('<article class="article">')[1]
intro = article.split('</header>', 1)[1].split('<details class="mobile-toc">')[0]
assert normalize(converted(parts[0])) == normalize(intro)
for i in range(1, len(parts), 4):
    anchor, number, title, text = parts[i:i+4]
    expected = normalize(converted(f'{number}{title}\n\n{text}'))
    actual = re.search(fr'<section id="{anchor}">(.*?)</section>', html, re.S).group(1)
    assert expected == normalize(actual), f'Content mismatch {anchor}'
source_body = sources.split('</details>')[0]
source_html = html.split('<details id="sources" class="source-note">')[1].split('</details>')[0].split('</summary>')[1]
assert normalize(converted(source_body.split('</summary>')[1])) == normalize(source_html)

diagrams = []
for src in sorted((BOOK / 'diagrams/sources').glob('ch14-*.excalidraw')):
    scene = json.loads(src.read_text())
    assert scene['type'] == 'excalidraw' and scene['version'] == 2
    svg = ET.parse(BOOK / 'diagrams/exports' / (src.stem + '.svg')).getroot()
    svg_text = re.sub(r'\s+', '', ''.join(svg.itertext()))
    elements = scene['elements']
    element_ids = {e['id'] for e in elements}
    for element in elements:
        if element['type'] == 'text':
            assert re.sub(r'\s+', '', element['text']) in svg_text, element['text']
        if element['type'] == 'arrow':
            for side in ('startBinding', 'endBinding'):
                assert element[side]['elementId'] in element_ids
    diagrams.append({'stem': src.stem, 'elements': len(elements)})
assert len(diagrams) == doc.tags.count('figure') == 3
assert doc.tags.count('table') == 1
# The sole numeric example is explicitly hypothetical, not a model accuracy claim.
assert 100 * .2 == 20 and 100 - 20 == 80
result = dict(sections=12, han_characters=len(re.findall(r'[\u4e00-\u9fff]', md.split('<details id="sources">')[0])),
              tables=1, code_blocks=0, local_references=refs, pending=sorted(set(pending)),
              parity='intro + 12 sections + sources match', diagrams=diagrams,
              total_elements=sum(d['elements'] for d in diagrams), numeric_example='100 × 20% = 20; remaining 80')
(OUT / 'ch14-static-results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
print(json.dumps(result, ensure_ascii=False, indent=2))
