"""Chapter-local arithmetic, version-context and Markdown/HTML checks, not a DB test."""
from pathlib import Path
from itertools import combinations
import json
import re
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit, unquote
from html.parser import HTMLParser
import markdown


class Parser(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.texts, self.nodes = [], []
        self.feed(text)

    def handle_data(self, data):
        self.texts.append(data)

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))


def plain(text):
    return ''.join(Parser(text).texts)

BOOK = Path(__file__).resolve().parents[2]
md = (BOOK / 'notes/ch06.md').read_text()
page = BOOK / 'chapters/ch06.html'
html = page.read_text()
parsed = Parser(html)
normalize = lambda s: re.sub(r'\s+', '', s)
body, source = md.split('<details id="sources">')
parts = re.split(r'<a id="([^"]+)"></a>\s*\n\n## (\d+)　([^\n]+)\n\n', body)
intro = re.sub(r'^# .*?\n\n\*\*.*?\*\*\n\n', '', parts[0], count=1, flags=re.S)
actual_intro = re.search(r'<header class="article-header">.*?</header>\s*(.*?)<details class="mobile-toc">', html, re.S).group(1)
assert normalize(plain(markdown.markdown(intro))) == normalize(plain(actual_intro))
assert plain(re.search(r'<h1>(.*?)</h1>', html, re.S).group(1)) == md.splitlines()[0][2:]
for i in range(1, len(parts), 4):
    anchor, number, title, content = parts[i:i+4]
    section = re.search(r'<section id="' + anchor + r'">(.*?)</section>', html, re.S).group(1)
    heading = re.search(r'<h2>(.*?)</h2>', section, re.S).group(1)
    assert normalize(plain(heading)) == normalize(number + title), anchor
    section = re.sub(r'<h2>.*?</h2>', '', section, count=1, flags=re.S)
    expected = markdown.markdown(content, extensions=['tables', 'fenced_code'])
    assert normalize(plain(section)) == normalize(plain(expected)), anchor
source = source.split('</details>')[0]
expected = markdown.markdown(re.sub(r'<summary>.*?</summary>', '', source, flags=re.S), extensions=['tables', 'fenced_code'])
actual = re.search(r'<details id="sources"[^>]*>(.*?)</details>', html, re.S).group(1)
actual = re.sub(r'<summary>.*?</summary>', '', actual, count=1, flags=re.S)
assert normalize(plain(actual)) == normalize(plain(expected))
ids = [attrs['id'] for tag, attrs in parsed.nodes if 'id' in attrs]
assert len(ids) == len(set(ids))
pending = []
refs = set()
for tag, node in parsed.nodes:
    for attr in ('href', 'src'):
        if attr not in node:
            continue
        ref = node[attr]
        u = urlsplit(ref)
        if u.scheme or u.netloc:
            continue
        refs.add(ref)
        assert not re.search(r'/(notes|originals|sources)/', ref)
        target = (page.parent / unquote(u.path)).resolve() if u.path else page
        if not target.exists() and target.name == 'ch08.html':
            pending.append(ref)
            continue
        assert target.exists(), str(target)
        if u.fragment:
            assert any(attrs.get('id') == unquote(u.fragment) for tag, attrs in Parser(target.read_text()).nodes), ref
assert all(attrs.get('alt') for tag, attrs in parsed.nodes if tag == 'img')

scene_counts = {}
for sourcefile in (BOOK / 'diagrams/sources').glob('ch06-*.excalidraw'):
    scene = json.loads(sourcefile.read_text())
    root = ET.parse(BOOK / 'diagrams/exports' / (sourcefile.stem + '.svg')).getroot()
    svgtext = normalize(''.join(root.itertext()))
    for e in scene['elements']:
        assert e['type'] in ('text', 'rectangle', 'arrow', 'line')
        if e['type'] == 'text':
            assert normalize(e['text']) in svgtext, (sourcefile, e['text'])
    scene_counts[sourcefile.stem] = len(scene['elements'])

# Finite-set derivation: check only the four configurations used in the text.
for n, w, r in [(3, 2, 2), (5, 3, 3), (5, 5, 1), (5, 1, 5)]:
    for ws in combinations(range(n), w):
        for rs in combinations(range(n), r):
            assert len(set(ws) & set(rs)) >= w + r - n > 0
assert set('A').isdisjoint('B')  # n=3,w=1,r=1 may read old data
assert set('AB').isdisjoint('DE')  # changed membership
assert set('XY').isdisjoint('BC')  # temporary sloppy-quorum holders
assert set(('E1', 'E2')).isdisjoint(('W1', 'W2'))  # separate local quorums
state = {'A': (1, 1), 'B': (0, 0), 'C': (0, 0)}
read = lambda nodes: max(state[n] for n in nodes)[1]
assert (read('AB'), read('BC')) == (1, 0)  # no completed blocking read repair

# Original five writes. Server versions and caller contexts are different fields.
requests = [(0, {'奶'}), (0, {'蛋'}), (1, {'奶', '面粉'}),
            (2, {'奶', '蛋', '火腿'}), (3, {'奶', '面粉', '蛋', '培根'})]
siblings = {}
versions = []
for v, (context, value) in enumerate(requests, 1):
    siblings = {k: val for k, val in siblings.items() if k > context}
    siblings[v] = value
    versions.append(sorted(siblings))
assert versions == [[1], [1, 2], [2, 3], [3, 4], [4, 5]]
assert set.union(*siblings.values()) == {'奶', '蛋', '面粉', '火腿', '培根'}
edges = {(1, 3), (1, 4), (2, 4), (2, 5), (3, 5)}
closure = edges | {(a, d) for a, b in edges for c, d in edges if b == c}
assert (1, 5) in closure and (3, 4) not in closure and (4, 5) not in closure

before = lambda a, b: all(x <= y for x, y in zip(a, b)) and a != b
join = lambda a, b: tuple(max(x, y) for x, y in zip(a, b))
assert not before((1, 0), (0, 1)) and not before((0, 1), (1, 0))
assert before((1, 0), (2, 1)) and before((0, 1), (2, 1))
assert not before((2, 1), (0, 2)) and not before((0, 2), (2, 1))
assert join((2, 1), (0, 2)) == (2, 2)
assert before((2, 1), (2, 3)) and before((0, 2), (2, 3))
counter = join((2, 0), (0, 1))
assert sum(counter) == 3 and join(counter, (0, 1)) == counter
assert {'DVD', 'Soap'} | {'Book', 'Soap'} == {'DVD', 'Book', 'Soap'}
assert 'nice'[:3] + '!' + 'nice'[3:] == 'nic!e'
assert 'nice'[:4] + '!' + 'nice'[4:] == 'nice!'

result = dict(sections=21, figures=5, tables=html.count('<table>'),
              codeBlocks=html.count('<pre>'), bodyHan=len(re.findall(r'[\u4e00-\u9fff]', re.sub(r'```.*?```', '', body, flags=re.S))),
              localReferences=len(refs), pendingPeerLinks=sorted(set(pending)), scenes=scene_counts,
              markdownHtml='title, introduction, 21 sections and sources matched', numeric='quorum, partial-write read regression, cart, causal DAG, vectors, counter, OT passed')
out = Path('/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools/ch06-static-results.json')
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False))
