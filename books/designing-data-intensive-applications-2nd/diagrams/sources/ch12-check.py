"""Chapter 12 teaching models, SQLite examples and Markdown/HTML consistency.

No Kafka/Flink/CDC service is started. Model clocks and failures are deterministic.
"""
from copy import deepcopy
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import sqlite3
import xml.etree.ElementTree as ET

import markdown

BOOK = Path(__file__).resolve().parents[2]
checks = []


def passed(name):
    checks.append(name)


assert (1200 - 1000) * 3600 == 720000
assert 20 * 10**12 / (250 * 10**6) == 80000
assert 20000 * 3600 == 72000000
assert (6000 + 1000) / 10 == 700
assert (100 + 9 * 0) / 10 == 10
passed('backlog, ideal retention, join-state size, restart throughput and weighted mean')

# Completion of later records cannot advance across unfinished record 42.
next_offset, done = 42, {43, 44}
while next_offset in done:
    next_offset += 1
assert next_offset == 42
done.add(42)
while next_offset in done:
    next_offset += 1
assert next_offset == 45
passed('parallel completion advances only the completed prefix')


def apply(state, changes):
    state = dict(state)
    for _, key, value in changes:
        if value is None:
            state.pop(key, None)
        else:
            state[key] = value
    return state


snapshot = {'A': 10, 'B': 20}
changes = [(101, 'A', 11), (102, 'B', None), (103, 'C', 30)]
assert apply(snapshot, changes) == {'A': 11, 'C': 30}
assert apply(snapshot, [e for e in changes if e[0] >= 104]) != {'A': 11, 'C': 30}
wrong = apply({}, changes[:1])
wrong.update(snapshot)
assert wrong['A'] == 10
buffer = dict(snapshot)
for _, key, _ in changes:
    buffer.pop(key, None)
live = apply({}, changes)
live.update(buffer)
assert live == {'A': 11, 'C': 30}
passed('snapshot S100 + changes 101–103; missed handoff, old overwrite and collision filtering')

# Minutes after midnight: device is two minutes fast.
E, S, R = 12 * 60 + 2, 12 * 60 + 7, 12 * 60 + 5
assert E + (R - S) == 12 * 60
assert E + (S - R) == 12 * 60 + 4
passed('three timestamps: correction is E + (R − S)')


def hopping_starts(t, length=300, step=60):
    return {start for start in range((t // step) * step - length, (t // step) * step + 1, step)
            if start <= t < start + length}


# Seconds relative to 10:00; the two records are 273s apart.
assert (240 // 60) * 60 == 240
assert 219 // 60 == 3
assert len(hopping_starts(219)) == 5
assert not hopping_starts(219) & hopping_starts(492)
assert 492 - 219 == 273 < 300
assert hopping_starts(219, step=1) & hopping_starts(492, step=1)


def sessions(events, gap=30):
    groups = []
    for t in sorted(events):
        if not groups or t - groups[-1][-1] > gap:
            groups.append([t])
        else:
            groups[-1].append(t)
    return groups


assert sessions([0, 50]) == [[0], [50]]
assert sessions([0, 50, 25]) == [[0, 25, 50]]
passed('half-open tumbling, five hopping memberships, distance window and late session merge')

# One [0,60) event-time window; W=60 emits and W=180 cleans up.
state, watermark, view, side = 0, -1, {}, []
for kind, value in [('event', 10), ('event', 40), ('watermark', 60),
                    ('event', 25), ('watermark', 180), ('event', 30)]:
    if kind == 'watermark':
        watermark = value
        if watermark >= 60 and state is not None:
            view[(0, 60)] = state
        if watermark >= 180:
            state = None
    elif state is None:
        side.append(value)
    elif 0 <= value < 60:
        state += 1
        if watermark >= 60:
            view[(0, 60)] = state
assert view == {(0, 60): 3} and side == [30]
assert min(10 * 60 + 2, 9 * 60 + 58) == 9 * 60 + 58
passed('late count updates the same key 2→3; cleanup routes later record aside; minimum watermark')

# Reversed arrival order still matches a click two minutes after its search.
def stream_join(arrivals):
    left, right, output = {}, {}, []
    for kind, key, timestamp in arrivals:
        own, other = (left, right) if kind == 'search' else (right, left)
        own[key] = timestamp
        if key in other and key in left and key in right and 0 <= right[key] - left[key] <= 3600:
            output.append((key, left[key], right[key]))
    return output


events = [('search', 'S', 0), ('click', 'S', 120)]
assert stream_join(events) == stream_join(list(reversed(events))) == [('S', 0, 120)]
passed('stream–stream join buffers both sides under reversed arrival order')

md = (BOOK / 'notes/ch12.md').read_text()
query = re.search(r'```sql\n(.*?)```', md, re.S).group(1)
with sqlite3.connect(':memory:') as db:
    db.executescript('''CREATE TABLE posts(post_id TEXT PRIMARY KEY, sender_id TEXT, created_at INT);
    CREATE TABLE follows(follower_id TEXT, followee_id TEXT);
    INSERT INTO posts VALUES ('P1','乙',1);
    INSERT INTO follows VALUES ('甲','乙');''')
    assert db.execute(query).fetchall() == [('甲', 'P1', 1)]
    db.execute("INSERT INTO posts VALUES ('P2','乙',2)")
    db.execute("INSERT INTO follows VALUES ('丙','乙')")
    assert set(db.execute(query).fetchall()) == {(who, post, t) for who in ['甲', '丙'] for post, t in [('P1', 1), ('P2', 2)]}
    db.execute("DELETE FROM posts WHERE post_id='P1'")
    assert set(db.execute(query).fetchall()) == {('甲', 'P2', 2), ('丙', 'P2', 2)}
    db.execute("DELETE FROM follows WHERE follower_id='甲'")
    assert db.execute(query).fetchall() == [('丙', 'P2', 2)]
u, v, du, dv = set(), set(), {'P'}, {'F'}
join = lambda a, b: {(x, y) for x in a for y in b}
assert join(du, v) | join(u, dv) == set()
assert join(du, v) | join(u, dv) | join(du, dv) == join(u | du, v | dv)
assert join(du, v) | join(u | du, dv) == {('P', 'F')}
passed('actual notes SQL: insert/delete post and follow; simultaneous increments require cross term')

checkpoint = {'count': 8, 'next': 42}
inputs = {42: 1, 43: 1, 44: 1}


def finish(state):
    return state['count'] + sum(v for k, v in inputs.items() if k >= state['next'])


assert finish(checkpoint) == finish({'count': 10, 'next': 44}) == 11
assert finish({'count': 10, 'next': 42}) == 13
assert finish({'count': 8, 'next': 44}) == 9
required, acks = {'source', 'operator', 'sink'}, {'sink'}
assert not required <= acks
acks.update({'source', 'operator'})
assert required <= acks
passed('paired checkpoint restores 11; mismatched snapshots produce 13/9; sink barrier alone insufficient')


class Crash(Exception):
    pass


def consume(db, crash=None):
    try:
        with db:
            balance, offset = db.execute('SELECT balance, next_offset FROM state').fetchone()
            if 42 >= offset:
                db.execute('UPDATE state SET balance=?', (balance + 5,))
                if crash == 'after-business':
                    raise Crash()
                db.execute('UPDATE state SET next_offset=43')
                if crash == 'before-commit':
                    raise Crash()
        if crash == 'after-commit':
            raise Crash()
        return True
    except Crash:
        return False


for failure in ('after-business', 'before-commit', 'after-commit', None):
    with sqlite3.connect(':memory:') as db:
        db.executescript('CREATE TABLE state(balance INT, next_offset INT); INSERT INTO state VALUES(100,42);')
        first_ack = consume(db, failure)
        assert first_ack == (failure is None)
        assert consume(db) and consume(db)
        assert db.execute('SELECT * FROM state').fetchone() == (105, 43)
passed('SQLite same-transaction balance/offset survives precommit rollback and postcommit retry')


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


page = (BOOK / 'chapters/ch12.html').read_text()
body = md.split('<details id="sources">')[0]
parts = re.split(r'<a id="([^"]+)"></a>\s*\n\n## (\d+)　([^\n]+)\n\n', body)
sections = re.findall(r'<section id="([^"]+)">\s*<h2>(.*?)</h2>(.*?)</section>', page, re.S)
assert len(sections) == 23
for i, (anchor, heading, content) in enumerate(sections):
    md_anchor, number, title, md_content = parts[1+i*4:5+i*4]
    assert anchor == md_anchor and plain(heading) == plain(number + title)
    assert plain(markdown.markdown(md_content, extensions=['tables', 'fenced_code'])) == plain(content), anchor
    assert page.count(f'<li><a href="#{anchor}">') == 2
intro = re.sub(r'^# .*?\n\n\*\*.*?\*\*\n\n', '', parts[0], count=1, flags=re.S)
html_intro = re.search(r'</header>\s*(<p>订单.*?)<details class="mobile-toc"', page, re.S).group(1)
assert plain(markdown.markdown(intro)) == plain(html_intro)
md_sources = md.split('<details id="sources">')[1].split('</details>')[0]
html_sources = re.search(r'<details id="sources"[^>]*>(.*?)</details>', page, re.S).group(1)
md_sources = re.sub(r'<summary>(.*?)</summary>', r'\1\n\n', md_sources)
assert plain(markdown.markdown(md_sources, extensions=['tables', 'fenced_code'])) == plain(html_sources)
assert 'href="ch11.html" rel="prev"' in page
assert re.search(r'class="page-link next" href="../index.html"', page)
assert not re.search(r'href="ch(?:13|14)\.', page)
passed('23 section texts/headings, intro, sources, dual TOCs and pagination synchronized')

stems = ['log-groups', 'cdc-order', 'snapshot-cut', 'watermark-late', 'join-state', 'checkpoint-cut', 'effect-boundary']
counts = {}
for stem in stems:
    scene = json.loads((BOOK / f'diagrams/sources/ch12-{stem}.excalidraw').read_text())
    assert scene['type'] == 'excalidraw' and scene['version'] == 2
    assert scene['files'] == {} and all(e['type'] != 'image' for e in scene['elements'])
    svg = ET.parse(BOOK / f'diagrams/exports/ch12-{stem}.svg').getroot()
    labels = ''.join(e.text or '' for e in svg.iter('{http://www.w3.org/2000/svg}text'))
    for e in scene['elements']:
        if e['type'] == 'text':
            assert re.sub(r'\s+', '', e['text']) in re.sub(r'\s+', '', labels), (stem, e['text'])
    assert f'src="../diagrams/exports/ch12-{stem}.svg"' in page
    counts[stem] = len(scene['elements'])
passed('seven native editable scenes, every scene label in SVG, all images linked')

no_code = re.sub(r'```.*?```', '', body, flags=re.S)
print(json.dumps({'kind': 'deterministic teaching models and SQLite; no product integration',
                  'checks': checks, 'sections': len(sections), 'figures': len(stems),
                  'hanBeforeSourcesWithoutCode': len(re.findall(r'[\u4e00-\u9fff]', no_code)),
                  'nativeElementCounts': counts}, ensure_ascii=False, indent=2))
