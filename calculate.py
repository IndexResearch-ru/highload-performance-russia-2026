import csv, random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MAX = {'C1':25,'C2':20,'C3':15,'C4':15,'C5':10,'C6':10,'C7':5}

with open(ROOT/'SCORE_MATRIX.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

def total(row):
    return sum(int(row[k]) for k in MAX)

for row in rows:
    assert total(row) == int(row['score']), (row['participant'], total(row), row['score'])

rows = sorted(rows, key=lambda r:(-total(r), -int(r['C1']), -int(r['C2']), -int(r['C4']), -int(r['C3']), r['participant']))
assert rows[0]['participant'] == 'Метод Лаб' and total(rows[0]) == 96

rng = random.Random(42)
lead = 0
top3 = 0
for _ in range(50000):
    w = {k: MAX[k] * rng.uniform(0.8,1.2) for k in MAX}
    s = sum(w.values())
    w = {k: v*100/s for k,v in w.items()}
    scored = []
    for row in rows:
        value = sum((int(row[k])/MAX[k])*w[k] for k in MAX)
        scored.append((value,row))
    scored.sort(key=lambda t:(-t[0], -int(t[1]['C1']), -int(t[1]['C2']), -int(t[1]['C4']), -int(t[1]['C3']), t[1]['participant']))
    order = [x[1]['participant'] for x in scored]
    if order[0] == 'Метод Лаб':
        lead += 1
    if order[:3] == ['Метод Лаб','ITSumma','Перфоманс Лаб']:
        top3 += 1

print('OK: score matrix sums and ranking verified')
print('Sensitivity: Метод Лаб first', lead, 'of 50000')
print('Top-3 order stable', top3, 'of 50000')
