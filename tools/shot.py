#!/usr/bin/env python3
"""Check «Мусин дом» in headless Chrome: add-on blocks, a scripted run, screenshots, errors.

Run with the Python that has Playwright:
  /Users/markvozdvizenskij/work/tg-channels/.venv/bin/python tools/shot.py --blocks feat/x.js --steps steps.json --out /tmp/x

--blocks   add-on .js files inserted right before «Boot» (index.html itself is never changed)
--steps    JSON list, run in order after the game has loaded:
             {"js": "goRoom('courtyard')"}     code run INSIDE the game closure (sees S, goRoom, hk, …)
             {"log": "S.room"}                 print the value of an expression
             {"wait": 1500}                    milliseconds
             {"click": [x, y]}                 a real mouse click at page coordinates
             {"clickSel": "#homeBtn"}          click an element
             {"shot": "name"}                  save <out>/name.png
--state    JSON file with a saved game (localStorage "musya-jp-v1"); default: a fresh player who has
           finished the first story and has seen today's festival, so nothing pops up by itself
--fresh    start as a brand-new player instead
--date     2027-01-01 — the game's calendar day (?date=)
--hour     2.5 — fake time of day (?hour=), hourNow() and dayTint() follow it
--size     480x900 (phone) or 1280x800
--pre      JS run inside the closure right after loading, before story/festival/add-on boot
Prints console errors and page errors; exit code 1 if there were any.
"""
import argparse, json, os, re, sys, threading, time, http.server, socketserver, functools
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOT = '// ───────────────────────── Boot ─────────────────────────'
LOADED = 'resize();ui();hudTick();weatherLabel();'

ap = argparse.ArgumentParser()
ap.add_argument('--blocks', nargs='*', default=[])
ap.add_argument('--steps', default='[]')
ap.add_argument('--state')
ap.add_argument('--fresh', action='store_true')
ap.add_argument('--date')
ap.add_argument('--hour', help='fake time of day, e.g. 2.5 (?hour=)')
ap.add_argument('--size', default='480x900')
ap.add_argument('--pre', default='')
ap.add_argument('--out', default='.')
ap.add_argument('--wait', type=int, default=2500, help='ms after load before the steps')
a = ap.parse_args()

html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
assert html.count(BOOT) == 1 and html.count(LOADED) == 1
blocks = ''.join('\n// ── block: %s\n%s\n' % (b, open(b, encoding='utf-8').read()) for b in a.blocks)
html = html.replace(BOOT, blocks + BOOT)
seen = '' if (a.fresh or a.state) else '{const F=festNow();if(F)festProg(F).seen=1;}'   # the seeded player has already seen today's festival
html = html.replace(LOADED, LOADED + 'window.__ev=c=>eval(c);window.__ready=1;' + seen + a.pre + ';')
tmp = os.path.join(ROOT, 't_%d.html' % os.getpid())
open(tmp, 'w', encoding='utf-8').write(html)

steps = json.loads(open(a.steps).read() if os.path.exists(a.steps) else a.steps)
os.makedirs(a.out, exist_ok=True)
state = None
if a.state:
    state = open(a.state, encoding='utf-8').read()
elif not a.fresh:
    state = json.dumps({"story": {"ch": 9, "prog": [], "started": True, "done": True, "seen": 9}, "stats": {"got": ["story1", "story"], "seen": []},
                        "owned": ["r_bell", "r_ricebowl", "r_ribbon", "r_pearl", "r_foxbrush", "r_hyakki", "r_candle", "r_temari", "r_mirror", "r_key"],
                        "t": int(time.time() * 1000) - 60000})

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *x): pass
srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), functools.partial(Q, directory=ROOT))
srv.daemon_threads = True
threading.Thread(target=srv.serve_forever, daemon=True).start()
port = srv.server_address[1]
errs = []
W, H = map(int, a.size.split('x'))
try:
    with sync_playwright() as p:
        br = p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--autoplay-policy=no-user-gesture-required'])
        pg = br.new_page(viewport={'width': W, 'height': H}, device_scale_factor=1)
        pg.on('pageerror', lambda e: errs.append('pageerror: %s' % e))
        pg.on('console', lambda m: errs.append('console.%s: %s' % (m.type, m.text)) if m.type == 'error' else None)
        if state:
            pg.add_init_script('try{if(!sessionStorage.getItem("__seeded")){sessionStorage.setItem("__seeded","1");localStorage.setItem("musya-jp-v1",%s);localStorage.setItem("musya-3d-tip","1");}}catch(e){}' % json.dumps(state))
        else:
            pg.add_init_script('try{localStorage.setItem("musya-3d-tip","1");}catch(e){}')
        q = '&'.join(x for x in [('date=' + a.date) if a.date else '', ('hour=' + a.hour) if a.hour else ''] if x)
        url = 'http://127.0.0.1:%d/%s' % (port, os.path.basename(tmp)) + ('?' + q if q else '')
        pg.goto(url)
        pg.wait_for_function('window.__ready===1', timeout=60000)
        pg.wait_for_timeout(a.wait)
        for st in steps:
            if 'js' in st: pg.evaluate('c=>__ev(c)', st['js'])
            if 'log' in st: print('log:', st['log'], '=>', json.dumps(pg.evaluate('c=>{const v=__ev(c);try{return JSON.parse(JSON.stringify(v))}catch(e){return String(v)}}', st['log']), ensure_ascii=False)[:2000])
            if 'wait' in st: pg.wait_for_timeout(st['wait'])
            if 'click' in st: pg.mouse.click(*st['click'])
            if 'clickSel' in st: pg.click(st['clickSel'])
            if 'shot' in st:
                f = os.path.join(a.out, st['shot'] + '.png'); pg.screenshot(path=f); print('shot:', f)
        br.close()
finally:
    srv.shutdown()
    try: os.remove(tmp)
    except OSError: pass
for e in errs: print(e)
sys.exit(1 if any(not re.search(r'favicon|Failed to load resource', e) for e in errs) else 0)
