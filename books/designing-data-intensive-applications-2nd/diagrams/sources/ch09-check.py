"""Small teaching-model checks and Markdown/HTML/resource parity, not product tests."""
from pathlib import Path
from itertools import combinations, permutations
from decimal import Decimal
import importlib.util
import json
import re
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, unquote
from html.parser import HTMLParser


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.nodes, self.text = [], []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)


def text_of(source):
    return ''.join(Document(source).text)

HERE = Path(__file__).resolve().parent
BOOK = HERE.parents[1]
OUT = Path('/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools')
spec = importlib.util.spec_from_file_location('render_ch09', HERE / 'ch09-render.py')
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)
results = {}

# Reproduce the displayed calculations and the causal LWW counterexample.
assert 2 * 20 + 10 == 50
assert Decimal('0.0002') * 30 == Decimal('0.006')
assert Decimal('0.0002') * 86400 == Decimal('17.28')
assert 4000 * 16 == 64000 and Decimal(1) / 4000 == Decimal('0.00025')
assert (1200 - 1000) * 2 == 400
writes = [(Decimal('42.004'), 1), (Decimal('42.003'), 2)]
assert max(writes)[1] == 1
assert not (Decimal('10.480') > Decimal('10.500'))
assert Decimal('10.501') > Decimal('10.500')
results['calculations'] = '2d+r, drift, ISDN, queue accumulation, LWW and commit wait passed'

# Explicitly reproduce old non-atomic check/write interleaving.
token, value = 33, 10
old_check_passed = 33 >= token
token, value = 34, 12
if old_check_passed:
    value = 11
assert (token, value) == (34, 11)
results['unsafe_interleaving'] = 'A checks 33, B writes 34/12, A overwrites with 11'

# An atomic resource transition is the assumed contract. Enumerate only the
# representative schedules of old-write, new barrier and new write.
schedules = []
for order in permutations(['old', 'advance', 'new']):
    if order.index('advance') > order.index('new'):
        continue
    token, value, old_accepted = 33, 10, None
    for operation in order:
        incoming = 33 if operation == 'old' else 34
        accepted = incoming >= token
        if operation == 'old':
            old_accepted = accepted
        if not accepted:
            continue
        token = incoming
        if operation == 'old':
            value = 11
        elif operation == 'new':
            value = 12
    assert token == 34 and value == 12
    assert old_accepted == (order.index('old') < order.index('advance'))
    schedules.append({'order': order, 'old_accepted': old_accepted, 'final': [token, value]})
assert 34 >= 34  # The same lease may issue subsequent operations.
results['fencing_schedules'] = schedules

replicas = [(34, 1), (34, 1), (33, 999)]
assert all(max(replicas[i] for i in pair) == (34, 1) for pair in combinations(range(3), 2))
assert max(replicas[2:]) == (33, 999)  # One stale replica is insufficient.
results['replica_reads'] = 'All 3 two-replica sets select (34,1); single R3 does not'
assert set('ABC') & set('CDE') == {'C'}
results['majority'] = 'Two distinct majorities exist and intersect; no vote rule assumed'
calls = {'X': (0, 10, 33), 'Y': (2, 5, 34)}
assert calls['Y'][1] < calls['X'][1] and not (calls['Y'][1] < calls['X'][0])
results['token_order'] = 'Overlapping calls can complete in reverse token order'

source = (BOOK / 'notes/ch09.md').read_text()
page = (BOOK / 'chapters/ch09.html').read_text()
document = Document(page)
body, detail = source.split('<details id="sources">', 1)
parts = re.split(r'<a id="([^"]+)"></a>\s*\n\n## (\d+)　([^\n]+)\n\n', body)
norm = lambda text: re.sub(r'\s+', '', text)
for i in range(1, len(parts), 4):
    anchor, number, title, content = parts[i:i+4]
    expected = text_of(renderer.render(content))
    actual = re.search(r'<section id="' + anchor + r'">(.*?)</section>', page, flags=re.S)
    assert actual is not None, anchor
    actual = actual.group(1)
    heading = re.search(r'<h2>.*?</h2>', actual, flags=re.S).group(0)
    assert norm(text_of(heading)) == norm(number + title), anchor
    assert norm(text_of(actual.replace(heading, '', 1))) == norm(expected), anchor
source_detail = detail.split('</details>', 1)[0]
source_detail = re.sub(r'^\s*<summary>.*?</summary>\s*', '', source_detail, flags=re.S)
actual_detail = re.search(r'<details id="sources"[^>]*>(.*?)</details>', page, flags=re.S).group(1)
actual_detail = re.sub(r'<summary>.*?</summary>', '', actual_detail, count=1, flags=re.S)
assert norm(text_of(actual_detail)) == norm(text_of(renderer.render(source_detail)))
intro = re.sub(r'^# .*?\n\n\*\*.*?\*\*\n\n', '', parts[0], count=1, flags=re.S)
expected_intro = text_of(renderer.render(intro))
actual_intro = text_of(re.search(r'<header class="article-header">.*?</header>(.*?)<details class="mobile-toc">', page, flags=re.S).group(1))
assert norm(expected_intro) == norm(actual_intro)
ids = [attrs['id'] for tag, attrs in document.nodes if 'id' in attrs]
assert len(ids) == len(set(ids))
refs, pending = [], []
for tag, element in document.nodes:
    for attribute in ['href', 'src']:
        if attribute not in element:
            continue
        ref = element[attribute]
        parsed = urlparse(ref)
        if parsed.scheme or parsed.netloc:
            continue
        assert not re.search(r'/(notes|originals|sources)/', ref)
        dest = (BOOK / 'chapters' / unquote(parsed.path)).resolve() if parsed.path else (BOOK / 'chapters/ch09.html')
        if not dest.exists() and parsed.path == 'ch10.html':
            pending.append(ref)
            continue
        assert dest.exists(), ref
        if parsed.fragment:
            target = Document(dest.read_text())
            assert any(attrs.get('id') == unquote(parsed.fragment) for tag, attrs in target.nodes), ref
        refs.append(ref)
for tag, attrs in document.nodes:
    if tag == 'img':
        assert attrs.get('alt'), attrs

diagrams = []
for scene_file in sorted(HERE.glob('ch09-*.excalidraw')):
    scene = json.loads(scene_file.read_text())
    svg = ET.parse(HERE.parent / 'exports' / (scene_file.stem + '.svg')).getroot()
    svg_text = ''.join(svg.itertext())
    for element in scene['elements']:
        assert element['type'] in ['text', 'rectangle', 'arrow', 'line']
        if element['type'] == 'text':
            for line in element['text'].splitlines():
                assert norm(line) in norm(svg_text), (scene_file.name, line)
    diagrams.append({'file': scene_file.name, 'elements': len(scene['elements'])})
assert len(diagrams) == 6
results['static'] = {'sections': (len(parts)-1)//4, 'parity': '21 sections, intro and sources match',
    'local_references': len(refs), 'pending': sorted(set(pending)), 'diagrams': diagrams,
    'figures': sum(tag == 'figure' for tag, attrs in document.nodes), 'tables': sum(tag == 'table' for tag, attrs in document.nodes),
    'code_blocks': sum(tag == 'pre' for tag, attrs in document.nodes), 'han_count': len(re.findall(r'[\u4e00-\u9fff]', re.sub(r'```.*?```', '', body, flags=re.S)))}
(OUT / 'ch09-check-results.json').write_text(json.dumps(results, ensure_ascii=False, indent=2))
print(json.dumps(results, ensure_ascii=False, indent=2))
