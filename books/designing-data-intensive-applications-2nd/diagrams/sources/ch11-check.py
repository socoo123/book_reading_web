"""Minimal chapter-11 examples and static consistency checks; no real cluster."""
from pathlib import Path
from collections import Counter, defaultdict
from datetime import date
from itertools import groupby
import heapq
import json
import re
import sqlite3
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit, unquote
from html.parser import HTMLParser
import markdown


class Document(HTMLParser):
    def __init__(self, content):
        super().__init__(convert_charrefs=True)
        self.nodes, self.text = [], []
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)


def plain(content):
    return ''.join(Document(content).text)

BOOK = Path(__file__).resolve().parents[2]
TOOLS = Path('/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools')
md = (BOOK / 'notes/ch11.md').read_text()
page_html = (BOOK / 'chapters/ch11.html').read_text()
page = Document(page_html)
result = {'scope': 'local commands, SQLite and deterministic teaching models; no cluster'}

# Execute the actual Markdown snippets, rather than copied command text.
blocks = re.findall(r'```(\w+)\n(.*?)```', md, re.S)
with tempfile.TemporaryDirectory(prefix='ch11-examples-', dir=TOOLS) as directory:
    shell = next(code for lang, code in blocks if lang == 'sh')
    command_output = subprocess.check_output(['/bin/sh', '-c', shell], cwd=directory, text=True)
    python = next(code for lang, code in blocks if lang == 'python')
    python_output = subprocess.check_output(['python3', '-c', python], cwd=directory, text=True)
    canon = lambda value: [' '.join(line.split()) for line in value.splitlines()]
    expected = ['3 /', '3 /book', '1 /about', '1 /css/site.css']
    assert canon(command_output) == canon(python_output) == expected
    filtered = shell.split('export LC_ALL=C')[1].replace("awk '{print $7}'", "awk '$7 !~ /\\.css$/ {print $7}'")
    filtered = 'export LC_ALL=C\n' + filtered
    filtered_output = subprocess.check_output(['/bin/sh', '-c', filtered], cwd=directory, text=True)
    assert canon(filtered_output) == expected[:3]
    urls = [line.split()[6] for line in (Path(directory) / 'access.log').read_text().splitlines()]
    db = sqlite3.connect(':memory:')
    db.execute('CREATE TABLE logs(url TEXT NOT NULL)')
    db.executemany('INSERT INTO logs VALUES (?)', [(url,) for url in urls])
    sql = next(code for lang, code in blocks if lang == 'sql')
    query = db.execute(sql).fetchall()
    assert query == [('/',3),('/book',3),('/about',1),('/css/site.css',1)]
    result['pipeline_python_sql'] = {'rows':len(urls), 'output':expected,'css_filter':canon(filtered_output)}

segments = [[('A',1),('C',1)], [('A',1),('B',1)], [('B',1),('C',1)]]
merged = list(heapq.merge(*segments))
assert [k for k,v in merged] == list('AABBCC')
assert {key: sum(v for k,v in values) for key,values in groupby(merged,key=lambda x:x[0])} == {'A':2,'B':2,'C':2}

# A single small input drives all join strategies and an independent SQL oracle.
profiles = [(104,'1989-01-30'), (103,'1947-12-18')]
events = [(104,'/x',1), (104,'/z',2), (103,'/x',3), (999,'/missing',4)]
db.executescript('CREATE TABLE profiles(user_id INTEGER PRIMARY KEY, dob TEXT); CREATE TABLE events(user_id INTEGER,url TEXT,t INTEGER);')
db.executemany('INSERT INTO profiles VALUES (?,?)', profiles)
db.executemany('INSERT INTO events VALUES (?,?,?)', events)
oracle = sorted(db.execute('SELECT e.url,p.dob FROM events e JOIN profiles p USING(user_id)').fetchall())
records = [(uid,0,0,dob) for uid,dob in profiles] + [(uid,1,t,url) for uid,url,t in events]
sort_join = []
for uid, rows in groupby(sorted(records),key=lambda x:x[0]):
    dob = None
    for _, kind, _, value in rows:
        if kind == 0: dob = value
        elif dob is not None: sort_join.append((value,dob))
broadcast = dict(profiles)
broadcast_join = [(url,broadcast[uid]) for uid,url,_ in events if uid in broadcast]
partitioned_join = []
for shard in range(2):
    local = {uid:dob for uid,dob in profiles if uid%2==shard}
    partitioned_join += [(url,local[uid]) for uid,url,_ in events if uid%2==shard and uid in local]
assert sorted(sort_join) == sorted(broadcast_join) == sorted(partitioned_join) == oracle
as_of = date(2025,6,27)
ages = {}
for uid,birthday in profiles:
    d = date.fromisoformat(birthday)
    ages[uid] = as_of.year-d.year-((as_of.month,as_of.day)<(d.month,d.day))
assert ages == {104:36,103:77}
groups = Counter((url, 'under40' if ages[uid]<40 else '40plus') for uid,url,_ in events if uid in ages)
assert groups == {('/x','under40'):1,('/x','40plus'):1,('/z','under40'):1}
hot = [(104, f'/p{i}', i) for i in range(8)]
salted = {(104,salt):broadcast[104] for salt in range(4)}
salted_join = [(url,salted[(uid,t%4)]) for uid,url,t in hot]
assert salted_join == [(url,broadcast[uid]) for uid,url,t in hot]
assert len(set(t%4 for uid,url,t in hot)) == 4
result['shuffle_and_joins'] = {'merged':merged,'inner_join':oracle,'ages':ages,'hot_salt_subtasks':4,'missing_profile_dropped':True}

# Numerical claims and failure/publication boundaries, as a toy model only.
assert divmod(900,128)==(7,4)
assert (10+4)/10==1.4 and 14-4==10 and 4-3==1
assert 20*50==1000 and 2*50==100
attempts = {'a1': {'complete':False,'rows':['partial']}, 'a2': {'complete':True,'rows':['full']}}
committed = {0:attempts['a2']['rows']}
assert committed == {0:['full']}  # never concatenate unsuccessful attempts
current = 'V17'
required = {'p0':12,'p1':8}
applied = {'p0':12,'p1':7}
ready = lambda: all(applied[p]>=offset for p,offset in required.items())
assert not ready()  # an end notification alone cannot release the gate
assert current=='V17'
applied['p1']=8
assert ready()
old_reader = current
current = 'V18'
assert old_reader=='V17' and current=='V18'
score=0
for _ in range(2): score+=10
assert score==20
versioned = {}
for _ in range(2): versioned[('V18',104)] = 10
assert versioned[('V18',104)]==10
result['recovery_publication_model'] = {'failed_attempt_excluded':True,'early_notification_blocks_publish':True,'reader_version_pinned':True,'increment_twice':score,'deterministic_overwrite':10}

ids = [attrs['id'] for tag, attrs in page.nodes if 'id' in attrs]
assert len(ids)==len(set(ids))
pending, refs = [], 0
for tag, node in page.nodes:
    for attr in ('href','src'):
        if attr not in node: continue
        url=urlsplit(node[attr]); refs+=1
        if url.scheme or url.netloc: continue
        assert not any(x in url.path for x in ('/notes/','/sources/','/originals/','.pdf'))
        target=(BOOK/'chapters'/unquote(url.path)).resolve() if url.path else BOOK/'chapters/ch11.html'
        if not target.exists() and target.name in ('ch10.html','ch12.html'):
            pending.append(str(target)); continue
        assert target.exists(), target
        if url.fragment and target.suffix=='.html':
            dest=Document(target.read_text())
            assert any(attrs.get('id')==unquote(url.fragment) for tag, attrs in dest.nodes), (target,url.fragment)
for tag, attrs in page.nodes:
    if tag=='img': assert attrs.get('alt')

body, sources = md.split('<details id="sources">',1)
parts=re.split(r'<a id="([^"]+)"></a>\s*\n\n## (\d+)　([^\n]+)\n\n',body)
normalize=lambda text: re.sub(r'\s+','',text)
for i in range(1,len(parts),4):
    anchor,number,title,content=parts[i:i+4]
    expected=plain(markdown.markdown(content,extensions=['tables','fenced_code']))
    actual=re.search(r'<section id="'+anchor+r'">(.*?)</section>',page_html,re.S).group(1)
    assert normalize(plain(actual))==normalize(number+title+expected),anchor
sources=sources.split('</details>')[0]
sources=re.sub(r'^\s*<summary>.*?</summary>','',sources,flags=re.S)
expected=plain(markdown.markdown(sources,extensions=['tables','fenced_code']))
actual=re.search(r'<details id="sources"[^>]*>.*?</summary>(.*?)</details>',page_html,re.S).group(1)
assert normalize(plain(actual))==normalize(expected)

counts={}
for scene in sorted((BOOK/'diagrams/sources').glob('ch11-*.excalidraw')):
    data=json.loads(scene.read_text()); svg=ET.parse(BOOK/'diagrams/exports'/f'{scene.stem}.svg')
    assert all(e['type'] in ('text','rectangle','arrow') for e in data['elements'])
    exported=''.join(svg.getroot().itertext())
    for e in data['elements']:
        if e['type']=='text':
            assert normalize(e['text']) in normalize(exported), (scene.name,e['text'])
    counts[scene.stem]=len(data['elements'])
assert len(counts)==4
result['static']={'references':refs,'sections':18,'parity':'all sections + sources','figures':4,
                  'native_elements':counts,'pending_sibling_pages':sorted(set(pending)),
                  'body_han':len(re.findall(r'[\u4e00-\u9fff]',re.sub(r'```.*?```','',body,flags=re.S))),
                  'body_tables':sum(tag=='table' for tag,attrs in Document(markdown.markdown(body,extensions=['tables'])).nodes),
                  'code_blocks':len(blocks)}
(TOOLS/'ch11-check-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
