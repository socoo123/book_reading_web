"""Small executable checks for the chapter's teaching data (no service deployments)."""
from pathlib import Path
import re
import sqlite3
import json
import xml.etree.ElementTree as ET
import pandas as pd

book = Path(__file__).resolve().parents[2]
text = (book / 'notes/ch03.md').read_text()
blocks = re.findall(r'```([^\n]+)\n(.*?)```', text, re.S)
sql = [code for lang, code in blocks if lang == 'sql']
db = sqlite3.connect(':memory:')
db.executescript('''
CREATE TABLE users(user_id INTEGER PRIMARY KEY, name TEXT, region_id TEXT);
CREATE TABLE regions(region_id TEXT PRIMARY KEY, region_name TEXT);
INSERT INTO users VALUES(7,'Lin','r1'),(9,'Mei','r1');
INSERT INTO regions VALUES('r1','杭州');
CREATE TABLE dim_product(product_id INTEGER PRIMARY KEY, category TEXT);
INSERT INTO dim_product VALUES(10,'乳品'),(11,'烘焙');
CREATE TABLE fact_sales(sale_id INTEGER, product_id INTEGER, store_id INTEGER,
 date_id INTEGER, quantity INTEGER, amount_cents INTEGER);
INSERT INTO fact_sales VALUES(1,10,1,20261101,2,1200),
 (2,11,1,20261101,1,800),(3,10,2,20261102,1,600);
CREATE TABLE locations(id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE within(child INTEGER, parent INTEGER);
CREATE TABLE people(id INTEGER PRIMARY KEY, name TEXT, born_id INTEGER, lives_id INTEGER);
INSERT INTO locations VALUES(1,'United States'),(2,'Idaho'),(3,'Europe'),
 (4,'United Kingdom'),(5,'England'),(6,'London'),(7,'France'),(8,'Saint-Lo'),(9,'North America');
INSERT INTO within VALUES(2,1),(1,9),(4,3),(5,4),(6,5),(7,3),(8,7);
INSERT INTO people VALUES(100,'Lucy',2,6),(101,'Alain',8,6);
''')
assert db.execute(sql[0]).fetchall() == [(7, 'Lin', '杭州')]
assert dict(db.execute(sql[1]).fetchall()) == {'乳品': 1800, '烘焙': 800}
assert db.execute(sql[3]).fetchall() == [('Lucy',)]

# A zero-length containment route must match the root itself.
db.execute("INSERT INTO people VALUES(102,'RootExample',1,3)")
assert db.execute(sql[3]).fetchall() == [('Lucy',), ('RootExample',)]
# For this ID-only recursive relation, UNION also terminates on a cycle.
db.execute('INSERT INTO within VALUES(1,2)')
assert db.execute(sql[3]).fetchall() == [('Lucy',), ('RootExample',)]

# Datalog example: evaluate exactly the two positive closure rules as sets.
locations = ['Idaho', 'United States', 'North America', 'Europe',
             'United Kingdom', 'England', 'London', 'France', 'Saint-Lo']
within = {('Idaho', 'United States'), ('United States', 'North America'),
          ('United Kingdom', 'Europe'), ('England', 'United Kingdom'),
          ('London', 'England'), ('France', 'Europe'), ('Saint-Lo', 'France')}
inside = {(x, x) for x in locations}
rounds = []
while True:
    new = {(x, z) for x, y in within for y2, z in inside if y == y2} - inside
    if not new:
        break
    rounds.append(len(new))
    inside |= new
assert ('Idaho', 'North America') in inside and ('London', 'Europe') in inside
assert ('Saint-Lo', 'United States') not in inside

python = [code for lang, code in blocks if lang == 'python']
scope = {}
exec(python[0], scope)
events, project = scope['events'], scope['project']
assert [project(events[:i]) for i in range(1, 5)] == [500, 497, 492, 495]
assert 495 + 3 == 498  # duplicate additive cancellation after a lost checkpoint
exec(python[1], scope)
matrix = scope['matrix']
assert matrix.loc[7, 'A'] == 5 and pd.isna(matrix.loc[7, 'C'])
assert matrix.loc[7].mean() == 4
assert abs(matrix.loc[7].fillna(0).mean() - 8 / 3) < 1e-12
try:
    pd.concat([scope['ratings'], scope['ratings'].iloc[[0]]]).pivot(
        index='user_id', columns='movie', values='rating')
except ValueError:
    pass
else:
    raise AssertionError('pivot must reject duplicate coordinates')

observations = [('2026-01-03', 'Sharks', 2), ('2026-01-20', 'Sharks', 3),
                ('2026-01-21', 'Dolphins', 8), ('2026-02-02', 'Sharks', 1)]
totals = {}
for date, category, count in observations:
    if category == 'Sharks':
        totals[date[:7]] = totals.get(date[:7], 0) + count
assert totals == {'2026-01': 5, '2026-02': 1}
for lang, code in blocks:
    if lang == 'json':
        json.loads(code)

diagrams = []
for path in sorted((book / 'diagrams/sources').glob('ch03-*.excalidraw')):
    scene = json.loads(path.read_text())
    svg = ET.parse(book / 'diagrams/exports' / (path.stem + '.svg')).getroot()
    exported_text = ''.join(svg.itertext())
    for element in scene['elements']:
        if element['type'] == 'text':
            for line in element['text'].splitlines():
                assert line.strip() in exported_text, (path.name, line)
    diagrams.append({'file': path.name, 'elements': len(scene['elements'])})

result = {'sqlite': sqlite3.sqlite_version, 'pandas': pd.__version__,
          'checks': ['region join', 'sales aggregate', 'recursive SQL with zero hops and cycle',
                     'positive Datalog rules evaluated as Python sets', 'event replay and duplicate arithmetic',
                     'Pandas pivot, missing values and duplicate-coordinate rejection',
                     'observation arithmetic', 'JSON syntax', 'scene/SVG text parity'],
          'datalog_new_facts_per_round': rounds, 'diagrams': diagrams}
print(json.dumps(result, ensure_ascii=False, indent=2))
