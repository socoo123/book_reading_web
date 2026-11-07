"""Static chapter-local checks; reports a concurrent ch14 absence separately."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re
import xml.etree.ElementTree as ET
import markdown
from html.parser import HTMLParser


class Document(HTMLParser):
    def __init__(self, content):
        super().__init__()
        self.ids, self.refs, self.images, self.text = [], [], [], []
        self.counts = {}
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.counts[tag] = self.counts.get(tag, 0) + 1
        if 'id' in a:
            self.ids.append(a['id'])
        for key in ['href', 'src']:
            if key in a:
                self.refs.append(a[key])
        if tag == 'img':
            self.images.append(a)

    def handle_data(self, data):
        self.text.append(data)


def words(content):
    return re.sub(r'\s+', '', ''.join(Document(content).text))

BOOK = Path(__file__).resolve().parents[2]
OUT = Path('/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools')
page = BOOK / 'chapters/ch13.html'
raw = page.read_text()
doc = Document(raw)
md = (BOOK / 'notes/ch13.md').read_text()
normalize = lambda s: re.sub(r'\s+', '', s)
ids = doc.ids
assert len(ids) == len(set(ids))
pending, checked = [], 0
for value in doc.refs:
    url = urlsplit(value)
    if url.scheme or url.netloc:
        continue
    assert not any(f'/{x}/' in value for x in ['notes', 'originals', 'sources'])
    target = (page.parent / unquote(url.path)).resolve() if url.path else page
    if not target.exists() and target.name == 'ch14.html':
        pending.append(value)
        continue
    assert target.is_file(), value
    if url.fragment:
        assert unquote(url.fragment) in Document(target.read_text()).ids, value
    checked += 1
for img in doc.images:
    assert img.get('alt') and img.get('width') and img.get('height')

body, source = md.split('<details id="sources">', 1)
body = re.sub(r'^# .*?\n\n\*\*.*?\*\*\n\n', '', body, count=1, flags=re.S)
parts = re.split(r'<a id="([^"]+)"></a>\s*\n\n## (\d+)　([^\n]+)\n\n', body)
for i in range(1, len(parts), 4):
    anchor, number, title, content = parts[i:i+4]
    expected = markdown.markdown(f'## {number} {title}\n\n{content}', extensions=['tables','fenced_code'])
    actual = re.search(fr'<section id="{anchor}">(.*?)</section>', raw, re.S).group(1)
    assert words(expected) == words(actual), anchor
intro = markdown.markdown(parts[0])
intro_actual = re.search(r'<header class="article-header">.*?</header>(.*?)<details class="mobile-toc">', raw, re.S).group(1)
assert words(intro) == words(intro_actual)
source = source.split('</details>',1)[0]
source = re.sub(r'^\s*<summary>.*?</summary>\s*', '', source, flags=re.S)
expected = markdown.markdown(source, extensions=['tables','fenced_code'])
actual = re.search(r'<details id="sources".*?<summary>.*?</summary>(.*?)</details>', raw, re.S).group(1)
assert words(expected) == words(actual), 'sources'

figures = []
for f in sorted((BOOK / 'diagrams/sources').glob('ch13-*.excalidraw')):
    scene = json.loads(f.read_text())
    svg = ET.parse(BOOK / 'diagrams/exports' / (f.stem + '.svg')).getroot()
    visible = normalize(''.join(svg.itertext()))
    assert scene['type'] == 'excalidraw' and scene['version'] == 2
    known = {e['id'] for e in scene['elements']}
    for e in scene['elements']:
        if e['type'] == 'text':
            assert normalize(e['text']) in visible, (f.name, e['text'])
            assert '（校验）' not in e['text']
        for key in ['startBinding','endBinding']:
            if e.get(key):
                assert e[key]['elementId'] in known
    figures.append(dict(stem=f.stem,elements=len(scene['elements'])))

stats = dict(sections=doc.counts.get('section',0), tables=doc.counts.get('table',0),
             code_blocks=doc.counts.get('pre',0), figures=doc.counts.get('figure',0),
             hanzi_before_sources_excluding_code=len(re.findall(r'[\u4e00-\u9fff]',re.sub(r'```.*?```','',md.split('<details id="sources">')[0],flags=re.S))))
assert stats['sections'] == 26 and stats['figures'] == 6
result = dict(stats=stats, local_references_checked=checked, pending_ch14=sorted(set(pending)),
              parity='introduction, all 26 sections and sources', figures=figures,
              native_elements=sum(x['elements'] for x in figures),
              published_ch13_files=1+len(figures))
(OUT/'ch13-static-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2))
