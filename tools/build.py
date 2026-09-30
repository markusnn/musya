#!/usr/bin/env python3
"""Paste the add-on blocks (feat/*.js) into index.html between the add-on markers, right before «Boot».
The blocks in feat/ are the source: edit them there and run this again (it replaces what was pasted before).
Then checks: the script parses (node), no duplicate top-level function names in the core.
Usage: python3 tools/build.py [--check-only]"""
import os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, 'index.html')
BOOT = '// ───────────────────────── Boot ─────────────────────────'
BEGIN, END = '// ═════ add-ons (built from feat/*.js by tools/build.py — edit them there) ═════', '// ═════ end of add-ons ═════'
# order matters for hooks that stop at the first answer (hit, gate, click, sleepTap)
ORDER = ['rooms', 'rooms2', 'story2', 'return', 'lanterns', 'visitors', 'rumors', 'haunt', 'dreams',
         'candles', 'trust', 'travel', 'sakura', 'gacha', 'kimono3d']

s = open(HTML, encoding='utf-8').read()
if BEGIN not in s:
    assert s.count(BOOT) == 1
    s = s.replace(BOOT, BEGIN + '\n' + END + '\n\n' + BOOT)
files = [os.path.join(ROOT, 'feat', n + '.js') for n in ORDER]
extra = sorted(f for f in (os.path.join(ROOT, 'feat', x) for x in os.listdir(os.path.join(ROOT, 'feat')) if x.endswith('.js')) if f not in files)
if extra: print('not in ORDER, appended:', [os.path.basename(f) for f in extra])
body = ''
for f in files + extra:
    if not os.path.exists(f): print('missing:', os.path.basename(f)); continue
    code = open(f, encoding='utf-8').read().strip()
    assert code.startswith('{') and code.endswith('}'), os.path.basename(f) + ' must be one { … } block'
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
