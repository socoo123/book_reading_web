"""Small teaching checks, not distributed product integration or a protocol proof."""
from pathlib import Path
from decimal import Decimal
import json
import re
import sqlite3

BOOK = Path(__file__).resolve().parents[2]
md = (BOOK / 'notes/ch13.md').read_text()
sql = re.search(r'```sql\n(.*?)```', md, re.S).group(1)
db = sqlite3.connect(':memory:')
db.executescript('CREATE TABLE accounts(account_id INTEGER PRIMARY KEY, balance_cents INTEGER);'
                 'INSERT INTO accounts VALUES(4321,10000),(1234,0);')
db.executescript(sql)
transaction = sql[sql.index('BEGIN;'):]
try:
    db.executescript(transaction)
    raise AssertionError('duplicate must fail')
except sqlite3.IntegrityError:
    db.rollback()
assert dict(db.execute('SELECT * FROM accounts')) == {4321: 8900, 1234: 1100}
assert db.execute('SELECT COUNT(*) FROM requests').fetchone()[0] == 1

# Failure before commit: both the new identity and its effects are rolled back.
db.executescript(transaction.replace("'r7'", "'r8'").replace('COMMIT;', 'ROLLBACK;'))
assert dict(db.execute('SELECT * FROM accounts')) == {4321: 8900, 1234: 1100}
assert db.execute('SELECT COUNT(*) FROM requests').fetchone()[0] == 1
db.close()

# Durable outbox model: a committed local decision retains every output obligation.
source = sqlite3.connect(':memory:')
source.executescript('''
CREATE TABLE account(balance INTEGER, reserved INTEGER);
INSERT INTO account VALUES(100,0);
CREATE TABLE decision(request_id TEXT PRIMARY KEY, approved INTEGER);
CREATE TABLE outbox(request_id TEXT, account TEXT, role TEXT, amount INTEGER,
                    PRIMARY KEY(request_id,account,role));
BEGIN;
UPDATE account SET reserved=31;
INSERT INTO decision VALUES('r7',1);
INSERT INTO outbox VALUES('r7','A','debit',-31),('r7','B','credit',30),('r7','F','fee',1);
COMMIT;
''')
balance, reserved = source.execute('SELECT * FROM account').fetchone()
assert balance - reserved == 69
assert 80 > balance - reserved  # a subsequent request for 80 is declined
outputs = list(source.execute('SELECT * FROM outbox'))
balances = {'A': 100, 'B': 0, 'F': 0}
seen = set()


def apply(event):
    request, account, role, amount = event
    effect = (request, account, role)
    if effect in seen:
        return
    # This single model step stands for each receiver's atomic effect + dedup commit.
    balances[account] += amount
    seen.add(effect)
    if account == 'A':
        source.execute('UPDATE account SET balance=balance-31,reserved=reserved-31')
        source.commit()


apply(next(e for e in outputs if e[1] == 'B'))
assert sum(balances.values()) == 130  # direct cross-store reads are not atomic snapshots
assert len(set(tuple(e[:3]) for e in outputs) - seen) == 2
# Crash: B's receipt exists, but the publisher did not record any acknowledgement.
# On restart the committed outbox remains. Resend all, including the duplicate B.
for event in source.execute('SELECT * FROM outbox'):
    apply(event)
for event in outputs:
    apply(event)
assert balances == {'A': 69, 'B': 30, 'F': 1}
assert source.execute('SELECT * FROM account').fetchone() == (69, 0)
assert sum(balances.values()) == 100
assert len(seen) == 3
source.close()

assert Decimal('100') * Decimal('7.20') == Decimal('720.00')
assert Decimal('100') * Decimal('7.25') == Decimal('725.00')
assert len({1, 2, 3} | {3, 4}) == 4

print(json.dumps(dict(sql_duplicate_and_rollback='passed',
    partial_publish_and_recovery='passed', reservation_and_role_dedup='passed',
    partial_read_total=130, final_balances=balances, fx_and_union='passed'), ensure_ascii=False, indent=2))
