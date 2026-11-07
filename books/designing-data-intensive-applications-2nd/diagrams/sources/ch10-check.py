"""Small Chapter 10 teaching models and source/page consistency checks."""
from pathlib import Path
from itertools import permutations
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json
import re
import xml.etree.ElementTree as ET

import markdown

BOOK = Path(__file__).resolve().parents[2]
TOOLS = Path('/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools')
result = {'scope': 'finite teaching examples, not an implementation or proof of a distributed protocol'}


def legal_orders(history):
    """Find sequential register/CAS histories respecting completed real-time order."""
    answers = []
    for order in permutations(history):
        positions = {op['id']: i for i, op in enumerate(order)}
        if any(a['end'] < b['start'] and positions[a['id']] > positions[b['id']]
               for a in history for b in history):
            continue
        state, valid = 0, True
        for op in order:
            if op['kind'] == 'write':
                state = op['value']
            elif op['kind'] == 'read':
                valid &= state == op['value']
            else:
                success = state == op['expected']
                valid &= success == op['success']
                if success:
                    state = op['value']
        if valid:
            answers.append([op['id'] for op in order])
    return answers


history = [dict(id='W', kind='write', start=2, end=10, value=1),
           dict(id='A', kind='read', start=3, end=4, value=1),
           dict(id='B', kind='read', start=5, end=6, value=0)]
assert not legal_orders(history)
history[2]['value'] = 1
assert legal_orders(history) == [['W', 'A', 'B']]
history[1]['value'] = 0
assert legal_orders(history) == [['A', 'W', 'B']]
cas = [dict(id='P', kind='cas', start=1, end=4, expected=0, value=2, success=True),
       dict(id='Q', kind='cas', start=2, end=5, expected=0, value=4, success=True)]
assert not legal_orders(cas)
cas[1]['success'] = False
assert legal_orders(cas) == [['P', 'Q']]
result['histories'] = 'new→old rejected; old→new and new→new accepted; two successful competing CAS rejected'

# Original quorum counterexample, then a synchronous majority write-back.
replicas = [1, 0, 0]
assert 2 + 3 > len(replicas)
first = max(replicas[i] for i in [0, 1])
second = max(replicas[i] for i in [1, 2])
assert (first, second) == (1, 0)
replicas[0] = replicas[1] = first
assert max(replicas[i] for i in [1, 2]) == 1
result['quorum'] = {'without_writeback': [first, second], 'after_majority_writeback': 1}

lamport = {'A': 1, 'C': 1, 'B': 0}
lamport['B'] = max(lamport.values()) + 1
assert sorted([(1, 'C'), (2, 'B'), (1, 'A')]) == [(1, 'A'), (1, 'C'), (2, 'B')]
assert 12 <= 13 < 15  # Photo visible, new privacy setting invisible.


def hlc_local(old, wall):
    l, c = old
    return (wall, 0) if wall > l else (l, c + 1)


def hlc_receive(old, message, wall):
    l, c = old
    lm, cm = message
    new = max(l, lm, wall)
    if new == l == lm:
        return new, max(c, cm) + 1
    if new == l:
        return new, c + 1
    if new == lm:
        return new, cm + 1
    return new, 0


assert hlc_local((1000, 2), 990) == (1000, 3)
assert hlc_local((1000, 2), 1001) == (1001, 0)
assert hlc_receive((995, 7), (1000, 3), 998) == (1000, 4)
assert hlc_receive((1000, 2), (1000, 7), 990) == (1000, 8)
assert hlc_receive((1001, 2), (1000, 7), 990) == (1001, 3)
assert hlc_receive((1000, 2), (999, 7), 1002) == (1002, 0)
result['clocks'] = {'lamport_reply': lamport['B'], 'hlc_rollback': [1000, 3], 'hlc_receive': [1000, 4], 'privacy_snapshot': 13}

# Every ordering of the two publish/ticket pairs; no waiting for the other process.
interleavings = 0
for schedule in permutations(['P.publish', 'P.ticket', 'Q.publish', 'Q.ticket']):
    if any(schedule.index(p+'.publish') > schedule.index(p+'.ticket') for p in ['P', 'Q']):
        continue
    published, tickets, decisions = {}, {}, {}
    for action in schedule:
        p, kind = action.split('.')
        if kind == 'publish':
            published[p] = p+'-value'
        else:
            ticket = len(tickets)
            tickets[p] = ticket
            other = 'Q' if p == 'P' else 'P'
            decisions[p] = published[p if ticket == 0 else other]
    winner = next(p for p in tickets if tickets[p] == 0)
    assert set(decisions.values()) == {published[winner]}
    loser = 'Q' if winner == 'P' else 'P'
    # Winner stops immediately after FAA; its already-published register remains.
    del decisions[winner]
    assert decisions[loser] == published[winner]
    interleavings += 1
assert interleavings == 6
result['fetch_add'] = {'two_process_interleavings': interleavings, 'winner_stops_after_ticket': 'survivor still reads published proposal'}


def commit_proposal(seen_votes, participants, timed_out=False):
    if any(v == 'abort' for v in seen_votes.values()):
        return 'abort'
    if len(seen_votes) == participants:
        return 'commit'
    return 'abort' if timed_out else None


assert commit_proposal({'P':'yes', 'Q':'yes'}, 2) == 'commit'
assert commit_proposal({'P':'yes', 'Q':'abort'}, 2) == 'abort'
assert commit_proposal({'P':'yes'}, 2) is None
assert commit_proposal({'P':'yes'}, 2, timed_out=True) == 'abort'
# Delayed all-yes history can create both proposals in the book's timeout model.
assert {commit_proposal({'P':'yes'}, 2, True), commit_proposal({'P':'yes','Q':'yes'}, 2)} == {'abort','commit'}
result['atomic_commit'] = 'commit requires all yes; timeout proposes abort but does not authorize unilateral final abort'

# Raft Figure 8's relevant distinction: a term-2 entry on a majority in term 4
# does not make it directly committed; a candidate with a term-3 tail is newer.
old_entry_term, current_term, copies, total = 2, 4, 3, 5
assert copies > total // 2 and old_entry_term != current_term
assert (3, 3) > (2, 9)  # compare last term before last index
assert not ((6, 8) >= (7, 8))  # C cannot displace B in the chapter's handoff.
assert (4, 10) > (3, 3)  # current-term entry changes the election restriction
accepted = [(3, 'Y'), (5, 'X')]
assert max(accepted, key=lambda item:item[0])[1] == 'X'
result['leader_rules'] = 'term-first election comparison; old-term majority is insufficient; Paxos highest accepted ballot selects X'

# Concrete read trace: term evidence and quorum alone leave state machine stale.
log, state, applied, read_index = {49:1, 50:1}, 0, 48, 50
assert state == 0 and applied < read_index
for index in range(applied + 1, read_index + 1):
    state, applied = log[index], index
assert state == 1 and applied >= read_index
result['read_barrier'] = {'before_apply': 0, 'after_apply': state, 'read_index': read_index}


class Document(HTMLParser):
    def __init__(self, content):
        super().__init__(convert_charrefs=True)
        self.nodes, self.text = [], []
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)


def normalized(content):
    return re.sub(r'\s+', '', ''.join(Document(content).text))


md = (BOOK / 'notes/ch10.md').read_text()
page = (BOOK / 'chapters/ch10.html').read_text()
body, sources = md.split('<details id="sources">', 1)
parts = re.split(r'<a id="([^"]+)"></a>\s*\n\n## (\d+)　([^\n]+)\n\n', body)
intro = re.sub(r'^# .*?\n\n\*\*.*?\*\*\n\n', '', parts[0], count=1, flags=re.S)
intro_html = page.split('</header>', 2)[2].split('<details class="mobile-toc">')[0]
assert normalized(markdown.markdown(intro)) == normalized(intro_html)
for i in range(1, len(parts), 4):
    anchor, number, title, content = parts[i:i+4]
    actual = re.search(rf'<section id="{anchor}">(.*?)</section>', page, re.S).group(1)
    expected = markdown.markdown(f'## {number} {title}\n\n{content}', extensions=['tables', 'fenced_code'])
    assert normalized(actual) == normalized(expected), anchor
source_body = re.sub(r'^\s*<summary>.*?</summary>\s*', '', sources.split('</details>')[0], flags=re.S)
actual_sources = re.search(r'<details id="sources".*?</summary>(.*?)</details>', page, re.S).group(1)
assert normalized(actual_sources) == normalized(markdown.markdown(source_body, extensions=['tables','fenced_code']))

parsed = Document(page)
ids = [attrs['id'] for tag, attrs in parsed.nodes if 'id' in attrs]
assert len(ids) == len(set(ids))
local_refs = set()
for tag, attrs in parsed.nodes:
    for attr in ['href', 'src']:
        if attr not in attrs:
            continue
        ref = urlsplit(attrs[attr])
        if ref.scheme or ref.netloc:
            continue
        target = (BOOK / 'chapters' / unquote(ref.path)).resolve() if ref.path else BOOK / 'chapters/ch10.html'
        assert target.is_file(), target
        assert not any(part in ['notes','originals','sources'] for part in target.relative_to(BOOK.parent.parent).parts)
        if ref.fragment:
            target_ids = [a.get('id') for _, a in Document(target.read_text()).nodes]
            assert unquote(ref.fragment) in target_ids, attrs[attr]
        local_refs.add(attrs[attr])

figures = re.findall(r'!\[[^\]]*\]\(\.\./diagrams/exports/(ch10-[^)]+)\.svg\)', md)
scene_counts = {}
for stem in figures:
    scene = json.loads((BOOK / f'diagrams/sources/{stem}.excalidraw').read_text())
    svg = ET.parse(BOOK / f'diagrams/exports/{stem}.svg').getroot()
    assert scene['type'] == 'excalidraw' and all(e['type'] != 'image' for e in scene['elements'])
    native_lines = [line for e in scene['elements'] if e['type'] == 'text' for line in e['text'].splitlines()]
    svg_lines = [''.join(e.itertext()) for e in svg.iter('{http://www.w3.org/2000/svg}text')]
    clean = lambda lines: Counter(re.sub(r'\s+', '', line) for line in lines if line.strip())
    assert clean(native_lines) == clean(svg_lines), stem
    assert svg.find('{http://www.w3.org/2000/svg}title') is not None
    scene_counts[stem] = len(scene['elements'])
assert len(figures) == 6 and (len(parts)-1)//4 == 22
result['static'] = {'sections':22, 'figures':6, 'local_refs':len(local_refs), 'body_han':len(re.findall(r'[\u4e00-\u9fff]',body)), 'all_han':len(re.findall(r'[\u4e00-\u9fff]',md)), 'native_elements':scene_counts, 'text_parity':'intro + all sections + sources'}
(TOOLS / 'ch10-check-results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
