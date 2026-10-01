#!/usr/bin/env python3
"""Paste the add-on blocks (feat/*.js) into index.html between the add-on markers, right before «Boot».
The blocks in feat/ are the source: edit them there and run this again (it replaces what was pasted before).
Then checks: the script parses (node), no duplicate top-level function names in the core.
Only the add-ons named in feat/READY are built in.
Usage: python3 tools/build.py [--check-only]"""
import os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, 'index.html')
BOOT = '// ───────────────────────── Boot ─────────────────────────'
BEGIN, END = '// ═════ add-ons (built from feat/*.js by tools/build.py — edit them there) ═════', '// ═════ end of add-ons ═════'
# order matters for hooks that stop at the first answer (hit, gate, click, sleepTap)
ORDER = ['rooms', 'rooms2', 'story2', 'return', 'lanterns', 'visitors', 'rumors', 'haunt', 'dreams',
         'candles', 'trust', 'travel', 'sakura', 'gacha', 'kimono3d',
         'ema', 'parade', 'forest', 'seasons', 'birthday', 'pet2', 'zen',
         'stars', 'hanafuda', 'workshop', 'cranes', 'birds', 'koi', 'serial', 'ryokan', 'kanji']

s = open(HTML, encoding='utf-8').read()
if BEGIN not in s:
    assert s.count(BOOT) == 1
    s = s.replace(BOOT, BEGIN + '\n' + END + '\n\n' + BOOT)
# only add-ons listed in feat/READY (one name per line) are built in — the others may still be in progress
ready = [l.strip() for l in open(os.path.join(ROOT, 'feat', 'READY'), encoding='utf-8') if l.strip() and not l.startswith('#')]
unknown = [n for n in ready if n not in ORDER]
assert not unknown, 'add to ORDER: %s' % unknown
files = [os.path.join(ROOT, 'feat', n + '.js') for n in ORDER if n in ready]
extra = []
body = ''
for f in files + extra:
    if not os.path.exists(f): print('missing:', os.path.basename(f)); continue
    code = open(f, encoding='utf-8').read().strip()
    body_ = re.sub(r'^(\s*//[^\n]*\n)+', '', code + '\n').strip()   # leading comment lines are fine
    assert body_.startswith('{') and body_.endswith('}'), os.path.basename(f) + ' must be one { … } block'
    body += '// ── %s\n%s\n' % (os.path.basename(f), code)
i, j = s.index(BEGIN) + len(BEGIN), s.index(END)
if '--check-only' not in sys.argv:
    s = s[:i] + '\n' + body + s[j:]
    open(HTML, 'w', encoding='utf-8').write(s)
# checks
js = re.search(r'<script>\n\(\(\)=>\{(.*)\}\)\(\);\n</script>', s, re.S)
assert js, 'main script not found'
with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as t:
    t.write('(()=>{' + js.group(1) + '})');
r = subprocess.run(['node', '--check', t.name], capture_output=True, text=True)
os.unlink(t.name)
print('syntax:', 'ok' if r.returncode == 0 else r.stderr[:1500])
core = s[:s.index(BEGIN)] + s[s.index(END):]
dup = sorted({m for m in re.findall(r'\nfunction ([A-Za-z0-9_]+)', core) if len(re.findall(r'\nfunction ' + m + r'\(', core)) > 1})
print('duplicate core functions:', dup or 'none')
print('size: %.0f KB' % (len(s.encode('utf-8')) / 1024))
