#!/usr/bin/env python3
"""«Бонсай»: the shop/«Вещи» thumbnail of the bonsai item (assets/items/bn_tree.webp).

The tree itself is procedural and painted live in the game (feat/bonsai.js → bnPaint); the room shows that
live render. This script only freezes one sample tree (a 20-day pine in the celadon pot) as the static
thumbnail: it runs the game headless via tools/shot.py, asks X.bn.thumb() for a webp data URL in chunks
(shot.py prints at most 2000 chars per log line) and saves it.

  /Users/markvozdvizenskij/work/tg-channels/.venv/bin/python art/bonsai_art.py
"""
import base64, json, os, re, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N, CH = 40, 1800
steps = [{"js": "X.bn.plant('matsu',0);X.bn.age(20);X.bn.sync()"}]
steps += [{"log": "X.bn.thumb().slice(%d,%d)" % (i * CH, (i + 1) * CH)} for i in range(N)]
out = tempfile.mkdtemp()
r = subprocess.run([sys.executable, os.path.join(ROOT, 'tools/shot.py'), '--blocks', 'feat/bonsai.js', '--date', '2026-07-10',
                    '--out', out, '--steps', json.dumps(steps)], cwd=ROOT, capture_output=True, text=True)
parts = {}
for line in r.stdout.splitlines():
    m = re.match(r'log: X\.bn\.thumb\(\)\.slice\((\d+),\d+\) => (".*")$', line)
    if m: parts[int(m.group(1))] = json.loads(m.group(2))
url = ''.join(parts[k] for k in sorted(parts))
assert url.startswith('data:image/webp;base64,'), (r.stdout[-800:], r.stderr[-800:])
data = base64.b64decode(url.split(',', 1)[1])
dst = os.path.join(ROOT, 'assets/items/bn_tree.webp')
open(dst, 'wb').write(data)
print('wrote', dst, len(data), 'bytes')
