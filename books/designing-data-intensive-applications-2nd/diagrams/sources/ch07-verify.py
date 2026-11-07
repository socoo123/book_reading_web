"""Minimal content examples and static checks for chapter 7 (no database integration)."""
from pathlib import Path
from collections import Counter
from urllib.parse import urlsplit, unquote
from html.parser import HTMLParser
import json
import re
import xml.etree.ElementTree as ET
import markdown

BOOK = Path(__file__).resolve().parents[2]
ROOT = BOOK.parents[1]
PAGE = BOOK / 'chapters/ch07.html'
MD = BOOK / 'notes/ch07.md'
OUT = Path('/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools')
results = {}

class Document(HTMLParser):
    def __init__(self, value):
        super().__init__()
        self.tags, self.parts = [], []
        self.feed(value)
    def handle_starttag(self, tag, attrs):
        self.tags.append({'tag': tag, **dict(attrs)})
    def handle_data(self, text):
        self.parts.append(text)
    def text(self):
        return ''.join(self.parts)

# 3 -> 4 nodes: nine records move with direct modulo; only three whole shards
# move in the declared fixed-shard assignment.
mod_moves = [h for h in range(12) if h % 3 != h % 4]
assert mod_moves == list(range(3, 12))
old = {s: s // 4 for s in range(12)}
new = {**old, 3: 3, 7: 3, 11: 3}
assert Counter(new.values()) == {0: 3, 1: 3, 2: 3, 3: 3}
assert [s for s in old if old[s] != new[s]] == [3, 7, 11]
assert new[15 % 12] == 3 and old[15 % 12] == 0
results['modulo_and_fixed_shards'] = {'direct_moves': len(mod_moves), 'fixed_moves': 3, 'sample_hash15_shard': 3}

def ring_owner(h, marks):
    return next((m for m in marks if h <= m), marks[0])
changed = [h for h in range(1024) if ring_owner(h, [100, 400, 700]) != ring_owner(h, [100, 400, 550, 700])]
assert changed == list(range(401, 551))
ring_counts = Counter(ring_owner(h, [100, 400, 550, 700]) for h in range(1024))
assert ring_counts == {100: 424, 400: 300, 550: 150, 700: 150}
results['ring'] = {'moved_positions': len(changed), 'fraction': len(changed)/1024, 'counts': dict(ring_counts)}

readings = [('A', '10:00', 21), ('B', '10:00', 18), ('A', '10:01', 22), ('B', '10:01', 19)]
assert [v for s,t,v in sorted(readings) if s == 'A' and '10:00' <= t < '10:02'] == [21, 22]
assert 1500 / 5 == 300 and 200 * 5 == 1000
results['range_and_hot_key'] = {'sensor_A': [21, 22], 'writes_per_bucket_ideal': 300, 'full_read_subrequests_per_second': 1000}

records = {101: ('red','Ford'), 202: ('blue','Honda'), 501: ('red','Honda')}
local = {d: [k for k,(c,m) in records.items() if k//500 == d and c == 'red'] for d in [0,1]}
red = {k for k,(c,m) in records.items() if c == 'red'}
honda = {k for k,(c,m) in records.items() if m == 'Honda'}
assert local == {0:[101],1:[501]} and red & honda == {501}
assert {k//500 for k in red} == {0,1}
# Async blue recolor: verifying red candidates removes false positives but
# cannot retrieve ID 501 from an as-yet-unupdated blue postings list.
records[501] = ('blue','Honda')
assert {k for k in red if records[k][0] == 'red'} == {101}
assert 501 not in {202}
results['secondary_indexes'] = {'local_red': local, 'red_AND_Honda': [501], 'red_record_shards': [0,1]}

# Explicit migration ordering: snapshot 40 is installed before ordered replay.
snapshot = {'x': 0, 'deleted': 'old'}
log = [(41,'set','x',1), (42,'delete','deleted',None)] + [(n,'set',f'k{n}',n) for n in range(43,49)]
target = snapshot.copy()
applied = 40
for pos, op, key, value in log:
    if op == 'set': target[key] = value
    else: target.pop(key, None)
    applied = pos
assert target['x'] == 1 and 'deleted' not in target and applied == 48
can_cutover = lambda position, old_stopped: position >= 48 and old_stopped
assert not can_cutover(47, True) and not can_cutover(48, False)
assert can_cutover(applied, True)
authority = {'owner': 'B', 'epoch': 2}
can_write = lambda node, epoch: authority == {'owner': node, 'epoch': epoch}
assert can_write('B', 2) and not can_write('A', 1)
results['migration_model'] = {'applied': applied, 'old_owner_rejected': True, 'deleted_record_absent': True}

page_html = PAGE.read_text()
doc = Document(page_html)
ids = [tag['id'] for tag in doc.tags if 'id' in tag]
assert len(ids) == len(set(ids))
pending = []
refs = 0
for tag in [t for t in doc.tags if 'href' in t or 'src' in t]:
    value = tag.get('href', tag.get('src'))
    u = urlsplit(value)
    if u.scheme or u.netloc: continue
    assert not any(x in value for x in ['/notes/', '/sources/', '/originals/', '.pdf'])
    target_path = (PAGE.parent / unquote(u.path)).resolve() if u.path else PAGE
    if not target_path.exists():
        if target_path.name in ['ch06.html', 'ch08.html']:
            pending.append(target_path.name)
            continue
        raise AssertionError(f'Missing target: {value}')
    if u.fragment:
        target_doc = doc if target_path == PAGE else Document(target_path.read_text())
        assert any(t.get('id') == unquote(u.fragment) for t in target_doc.tags), value
    refs += 1
assert all(t.get('alt') for t in doc.tags if t['tag'] == 'img')

source = MD.read_text()
normalize = lambda t: re.sub(r'\s+', '', t)
sections = re.findall(r'<a id="([^"]+)"></a>\s*## (\d+)　([^\n]+)\n(.*?)(?=<a id="|<details id="sources"|\Z)', source, re.S)
for anchor, number, title, content in sections:
    expected = Document(markdown.markdown(content, extensions=['fenced_code','tables'])).text()
    actual = re.search(fr'<section id="{anchor}">(.*?)</section>', page_html, re.S).group(1)
    body_text = Document(re.sub(r'<h2>.*?</h2>', '', actual, count=1, flags=re.S)).text()
    assert normalize(expected) == normalize(body_text), anchor
sources = source.split('<summary>来源、原书对应与核查说明</summary>',1)[1].split('</details>',1)[0]
expected = Document(markdown.markdown(sources,extensions=['tables'])).text()
actual = Document(page_html.split('<details id="sources" class="source-note">',1)[1].split('</details>',1)[0]).text().replace('来源、原书对应与核查说明','',1)
assert normalize(expected) == normalize(actual)
intro = '\n'.join(source.split('<a id="shards-and-replicas">')[0].splitlines()[4:])
intro_text = Document(markdown.markdown(intro)).text()
intro_actual = Document(page_html.split('<header class="article-header">',1)[1].split('</header>',1)[1].split('<details class="mobile-toc">',1)[0]).text()
assert normalize(intro_text) == normalize(intro_actual)

diagrams = []
for scene in sorted((BOOK/'diagrams/sources').glob('ch07-*.excalidraw')):
    data = json.loads(scene.read_text())
    svg = ET.parse(BOOK/'diagrams/exports'/f'{scene.stem}.svg').getroot()
    svgtext = ''.join(svg.itertext())
    labels = [x['text'] for x in data['elements'] if x['type'] == 'text']
    for label in labels:
        assert normalize(label) in normalize(svgtext), (scene.name, label)
    assert all(x['type'] in ['text','rectangle','arrow'] for x in data['elements'])
    diagrams.append({'stem':scene.stem, 'native_elements':len(data['elements'])})

results['static'] = {'sections':len(sections),'figures':sum(t['tag']=='figure' for t in doc.tags),'tables':sum(t['tag']=='table' for t in doc.tags),
                     'code_blocks':sum(t['tag']=='pre' for t in doc.tags), 'local_references_checked':refs,
                     'same_round_pending_links':sorted(set(pending)), 'md_html_full_text_match':True,
                     'diagrams':diagrams}
(OUT/'ch07-static-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))
