"""Deterministic teaching-model checks and Markdown/HTML/resource consistency.

These are not database integration tests; product semantics are separately cited.
"""
from copy import deepcopy
from html.parser import HTMLParser
from itertools import permutations
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET

import markdown

BOOK = Path(__file__).resolve().parents[2]
checks = []


def passed(name):
    checks.append(name)


# Statement snapshots may straddle one atomic commit, never a half transfer.
before, after = [500, 500], [600, 400]
assert sum(before) == sum(after) == 1000
assert before[0] + after[1] == 900
assert all(sum(snapshot) == 1000 for snapshot in (before, after))
passed('read skew 900 vs both consistent snapshots 1000')

# An earlier transaction that was active at snapshot time stays invisible.
snapshot_committed = {5, 99}
versions = [(100, 5, 100), (200, 100, None)]
visible = [value for value, inserted, deleted in versions
           if inserted in snapshot_committed and deleted not in snapshot_committed]
assert visible == [100]  # T100 later committing does not change this snapshot.
passed('MVCC excludes active-at-snapshot transaction despite lower ID')

value = 42
a, b = value + 1, value + 1
value = a
value = b
assert value == 43
value = 42
for _ in range(2):
    value += 1
assert value == 44
stock, winners = 1, []
for buyer in ('A', 'B'):  # Models target-row recheck after waiting in PG17 RC.
    if stock > 0:
        stock -= 1
        winners.append(buyer)
assert stock == 0 and len(winners) == 1
version, changed = 7, []
for editor in ('A', 'B'):
    if version == 7:
        version += 1
        changed.append(editor)
assert version == 8 and changed == ['A']
passed('lost update, atomic increment, conditional stock and version CAS')

# Whole-transaction retry must rerun the business branch, not reuse the first read.
stock_at_first_read = 1
first_decision = stock_at_first_read > 0
stock_after_competing_commit = 0
# The first attempt is known aborted; its effects are not committed.
retry_decision = stock_after_competing_commit > 0
assert first_decision and not retry_decision
assert max(stock_after_competing_commit - int(retry_decision), 0) == 0
passed('known-aborted retry rereads zero stock and rejects instead of reusing old decision')

snapshot = {'A': True, 'B': True}
decisions = {doctor: sum(snapshot.values()) >= 2 for doctor in snapshot}
concurrent = deepcopy(snapshot)
for doctor, may_leave in decisions.items():
    if may_leave:
        concurrent[doctor] = False
assert sum(concurrent.values()) == 0
for order in permutations(snapshot):
    serial = deepcopy(snapshot)
    for doctor in order:
        if sum(serial.values()) >= 2:
            serial[doctor] = False
    assert sum(serial.values()) == 1
passed('write skew violates invariant; both serial/lock-and-recheck orders preserve it')


def overlap(a, b):
    return a[1] > b[0] and a[0] < b[1]


assert overlap((720, 780), (750, 810))
assert not overlap((720, 780), (780, 840))
passed('half-open reservation intervals: overlap and adjacent boundary')


def has_serial_order(nodes, edges):
    return any(all(order.index(a) < order.index(b) for a, b in edges)
               for order in permutations(nodes))


assert has_serial_order('AB', [('A', 'B')])
assert not has_serial_order('AB', [('A', 'B'), ('B', 'A')])
assert not has_serial_order('ABC', [('A', 'B'), ('B', 'C'), ('C', 'A')])
passed('one rw dependency is safe; doctor and read-only three-transaction cycles are not')


def prepare(disk, participant):
    disk[participant] = 'PREPARED'  # Persist before returning YES.
    return 'YES'


def decide(disk, votes):
    disk['C'] = 'COMMIT' if votes == {'P': 'YES', 'Q': 'YES'} else 'ABORT'


def deliver(disk, participant):
    decision = disk['C']
    assert decision in ('COMMIT', 'ABORT')
    assert disk[participant] in ('PREPARED', decision, 'ABORT')
    assert decision != 'COMMIT' or disk[participant] != 'ABORT'
    disk[participant] = decision


disk = {'P': 'ACTIVE', 'Q': 'ACTIVE'}
votes = {p: prepare(disk, p) for p in ('P', 'Q')}
decide(disk, votes)
deliver(disk, 'Q')
assert disk['P'] == 'PREPARED' and disk['Q'] == 'COMMIT'
recovered = deepcopy(disk)  # Only persistent state survives C's crash.
deliver(recovered, 'P')
deliver(recovered, 'P')  # Duplicate final decision is harmless.
assert recovered['P'] == recovered['Q'] == 'COMMIT'

for votes in ({'P': 'YES', 'Q': 'NO'}, {'Q': 'YES'}):
    disk = {'P': 'PREPARED', 'Q': 'PREPARED'}
    decide(disk, votes)
    assert disk['P'] == 'PREPARED'  # Same local observation, opposite decision.
    for p in ('P', 'Q'):
        deliver(disk, p)
    assert disk['P'] == disk['Q'] == 'ABORT'
passed('2PC durable decision recovery, repeated decision, NO and lost-YES abort paths')


def consume(disk, crash=None):
    work = deepcopy(disk)
    if 'm' not in work['ids']:
        work['ids']['m'] = None
        if crash == 'after-id':
            return False
        work['points'] += 10
        work['ids']['m'] = work['points']
        if crash == 'after-business':
            return False
    disk.update(work)  # Atomic commit of ID, business data and result.
    if crash == 'after-commit':
        return False
    return True  # ack after commit, in the duplicate branch too.


for crash in ('after-id', 'after-business', 'after-commit', None):
    disk = {'ids': {}, 'points': 0}
    first_ack = consume(disk, crash)
    if crash in ('after-id', 'after-business'):
        assert disk == {'ids': {}, 'points': 0}
    else:
        assert disk == {'ids': {'m': 10}, 'points': 10}
    assert first_ack == (crash is None)
    assert consume(disk) and consume(disk)
    assert disk == {'ids': {'m': 10}, 'points': 10}

# Unsafe alternatives produce the counterexamples described in the notes.
id_first = {'ids': {'m': None}, 'points': 0}
assert consume(id_first) and id_first['points'] == 0
business_first = {'ids': {}, 'points': 10}
assert consume(business_first) and business_first['points'] == 20
passed('idempotent crash paths, unknown commit retry and duplicate ack; split writes fail')


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def plain(markup):
    parser = Text()
    parser.feed(markup)
    return re.sub(r'\s+', '', ''.join(parser.parts))


md = (BOOK / 'notes/ch08.md').read_text()
page = (BOOK / 'chapters/ch08.html').read_text()
body = md.split('<details id="sources">')[0]
parts = re.split(r'<a id="([^"]+)"></a>\s*\n\n## (\d+)　([^\n]+)\n\n', body)
sections = re.findall(r'<section id="([^"]+)">\s*<h2>(.*?)</h2>(.*?)</section>', page, re.S)
assert len(sections) == 24
for i, (anchor, heading, content) in enumerate(sections):
    md_anchor, number, title, md_content = parts[1+i*4:5+i*4]
    assert anchor == md_anchor
    assert plain(heading) == plain(number + title)
    expected = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    assert plain(expected) == plain(content), anchor
    assert page.count(f'<li><a href="#{anchor}">') == 2
md_sources = md.split('<details id="sources">')[1].split('</details>')[0]
html_sources = re.search(r'<details id="sources"[^>]*>(.*?)</details>', page, re.S).group(1)
md_sources = re.sub(r'<summary>(.*?)</summary>', r'\1\n\n', md_sources)
assert plain(markdown.markdown(md_sources, extensions=['tables', 'fenced_code'])) == plain(html_sources)
assert 'href="ch07.html" rel="prev"' in page
assert re.search(r'class="page-link next" href="../index.html"', page)
assert not re.search(r'href="ch(?:09|1[0-3])\.', page)
passed('24 section bodies/headings, dual TOCs, sources and pagination synchronized')

stems = ['read-skew', 'mvcc', 'write-skew', 'ssi-cycle', '2pc-normal', '2pc-recovery', 'idempotent']
counts = {}
for stem in stems:
    scene = json.loads((BOOK / f'diagrams/sources/ch08-{stem}.excalidraw').read_text())
    assert scene['type'] == 'excalidraw' and scene['version'] == 2
    assert scene['files'] == {} and all(e['type'] != 'image' for e in scene['elements'])
    svg = ET.parse(BOOK / f'diagrams/exports/ch08-{stem}.svg').getroot()
    labels = ''.join(e.text or '' for e in svg.iter('{http://www.w3.org/2000/svg}text'))
    for e in scene['elements']:
        if e['type'] == 'text':
            assert re.sub(r'\s+', '', e['text']) in re.sub(r'\s+', '', labels), (stem, e['text'])
    assert f'src="../diagrams/exports/ch08-{stem}.svg"' in page
    counts[stem] = len(scene['elements'])
passed('7 native editable scenes, all scene labels in SVG, all figures linked')

no_code = re.sub(r'```.*?```', '', body, flags=re.S)
result = {'kind': 'deterministic models and static checks; no live database',
          'checks': checks, 'sections': len(sections), 'figures': len(stems),
          'hanBeforeSourcesWithoutCode': len(re.findall(r'[\u4e00-\u9fff]', no_code)),
          'nativeElementCounts': counts}
print(json.dumps(result, ensure_ascii=False, indent=2))
