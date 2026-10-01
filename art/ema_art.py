#!/usr/bin/env python3
"""«Доска эма» (feat/ema.js): the wooden ema rack for the entrance, two live plaques (written / fulfilled)
and eight gifts «Дары с доски эма» — everything packed into ONE atlas assets/items/atlas_em.webp.
Prints the rect map as JSON (pasted into feat/ema.js). Preview → art/out/atlas_em.png.
Usage: ema_art.py [assets dir]"""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw
ASSETS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'assets')
sys.argv = [sys.argv[0], os.path.join(os.path.dirname(__file__), 'out')]     # items.py reads its out dir from argv[1]
import paint as P
from paint import hexc, mixc
import items as I
from items import px, fill, volume, line, ell, poly, text, soft, floor_shadow, dk, lt, H

CAP = {}


def done(img):
    out = img.resize((P.W, P.H), Image.LANCZOS); a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .88; a[..., :3] += np.random.default_rng(11).normal(0, 3.2, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def cap(img, iid, *a, **k): CAP[iid] = done(img)          # items.save → keep the picture instead of writing a file
I.save = cap


def rot(pts, cx, cy, a):
    c, s = math.cos(a), math.sin(a); return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def pent(x, y, w, h):   # ema outline, (x,y) = top centre
    return [(x - w / 2, y + h * .22), (x, y), (x + w / 2, y + h * .22), (x + w / 2, y + h), (x - w / 2, y + h)]


def ink_cols(img, x0, y0, x1, y1, rnd, col=(28, 20, 16, 235), cols=3, w=1.6):
    d = ImageDraw.Draw(img); cw = (x1 - x0) / cols
    for c in range(cols):
        x = x1 - cw * (c + .5); y = y0 + rnd.uniform(0, 3)
        while y < y1 - 4:
            L = rnd.uniform(2.5, 6); dx = rnd.uniform(-1.6, 1.6)
            d.line([(px(x + dx), px(y)), (px(x - dx * .6), px(y + L))], fill=col, width=px(w * rnd.uniform(.7, 1.2)))
            if rnd.random() < .45: d.line([(px(x - 2.4), px(y + L * .5)), (px(x + 2.4), px(y + L * .4))], fill=col, width=px(w * .8))
            y += L + rnd.uniform(1.5, 3.5)


# ───────────── the rack: posts, little gabled roof, two rows of old faded ema, a front bar with 3 hooks ─────────────
RW, RH = 250, 400
HOOKS = [(62, 214), (125, 210), (188, 214)]      # where the 3 live plaques hang (sprite px), JS reads them


def rack():
    img = I.canvas(RW, RH); rnd = random.Random(5)
    floor_shadow(img, 125, 396, 118, 90)
    for x in (24, 212):                                                     # posts
        fill(img, '#4a3626', x, rect=(x, 36, x + 14, 398), scale=4, stretch=(.3, 4), contrast=1.3); volume(img, (x, 36, x + 14, 398), .5, .3)
    for y, h in ((60, 9), (128, 8), (204, 9), (330, 8)):                    # bars
        fill(img, '#5a4230', y, rect=(14, y, 236, y + h), scale=4, stretch=(5, .3), contrast=1.2); volume(img, (14, y, 236, y + h), .45, .2)
    for row, (y0, n, sc) in enumerate(((66, 9, 1), (134, 8, 1))):          # old ema, faded by rain and sun
        xs = [26 + (198 / (n - 1)) * k + rnd.uniform(-5, 5) for k in range(n)]; rnd.shuffle(xs)
        for x in xs:
            w, h = rnd.uniform(34, 42), rnd.uniform(28, 34); a = rnd.uniform(-.18, .18); y = y0 + rnd.uniform(4, 9)
            base = mixc(hexc('#a88e6a'), hexc('#6e5a44'), rnd.uniform(0, .7))
            line(img, [(x - 4, y0 - 2), (x, y), (x + 4, y0 - 2)], mixc(hexc('#8a3a2c'), hexc('#5a4a3a'), rnd.uniform(.2, .8)), 1.2)
            pts = rot(pent(x, y, w, h), x, y, a); fill(img, base, int(x * 7 + row), poly=pts, scale=6, stretch=(4, .5), contrast=1.1, dark=.35, light=.12)
            ink_cols(img, x - w * .32, y + h * .3, x + w * .32, y + h * .92, rnd, (40, 32, 26, 120), 2, 1.1)
            if rnd.random() < .35: ell(img, (x + w * .12, y + h * .3, x + w * .32, y + h * .5), (120, 46, 36, 150))
            d = ImageDraw.Draw(img); d.line([(px(p[0]), px(p[1])) for p in pts + pts[:1]], fill=(30, 22, 16, 120), width=px(.8))
    for hx, hy in HOOKS:                                                    # brass hooks on the front bar
        ell(img, (hx - 2.5, 203, hx + 2.5, 209), '#9c8456')
    # roof: dark cedar shingles with a light barge board
    roof = [(2, 44), (125, 4), (248, 44), (238, 50), (125, 14), (12, 50)]
    fill(img, '#2c2a26', 3, poly=[(0, 40), (125, 0), (250, 40), (250, 52), (125, 14), (0, 52)], scale=5, stretch=(3, .4), contrast=1.4)
    fill(img, '#6a5038', 4, poly=roof, scale=4, stretch=(4, .4)); volume(img, (0, 0, 250, 52), .4, .2)
    d = ImageDraw.Draw(img)
    for k in range(9):   # shingle lines
        u = k / 8; d.line([(px(4 + 121 * u), px(42 - 38 * u)), (px(14 + 121 * u), px(50 - 36 * u))], fill=(20, 18, 16, 110), width=px(.8))
        d.line([(px(246 - 121 * u), px(42 - 38 * u)), (px(236 - 121 * u), px(50 - 36 * u))], fill=(20, 18, 16, 110), width=px(.8))
    fill(img, '#efe6d2', 9, rect=(116, 16, 134, 40), scale=3, contrast=.6)                 # little paper tag 絵馬
    text(img, '絵', 125, 23, 9, '#2a1a12', I.SERIF); text(img, '馬', 125, 33, 9, '#2a1a12', I.SERIF)
    return done(img)


def plaque(fulfilled):
    img = I.canvas(66, 64); rnd = random.Random(3 + fulfilled)
    line(img, [(33, 1), (24, 12), (33, 8), (42, 12), (33, 1)], '#b3322a', 1.6)
    pts = pent(33, 6, 60, 56); fill(img, '#d6b483' if not fulfilled else '#e0c08c', 21, poly=pts, scale=7, stretch=(5, .5), contrast=1.15, dark=.28, light=.18)
    d = ImageDraw.Draw(img); d.line([(px(p[0]), px(p[1])) for p in pts[:3]], fill=hexc('#6a4a2a'), width=px(2.2))
    ink_cols(img, 12, 24, 46, 58, rnd, (26, 18, 14, 240), 3, 1.7)
    soft(img, lambda dd: dd.ellipse([px(46), px(22), px(58), px(34)], fill=(190, 60, 44, 200)), .4)  # small painted sun
    if fulfilled:   # a red seal and a gold ribbon of «fulfilled»
        poly(img, [(42, 44), (56, 44), (56, 58), (42, 58)], '#b8322a'); text(img, '叶', 49, 51, 11, '#f2e2c8', I.SERIF)
        line(img, [(6, 20), (60, 20)], '#d8b048', 1.4)
    volume(img, (3, 6, 63, 62), .4, .18)
    return done(img)


# ───────────── gifts ─────────────
def g_uma():
    img = I.canvas(160, 140)
    line(img, [(46, 4), (80, 20), (114, 4)], '#b3322a', 2.4)
    pts = [(8, 38), (80, 16), (152, 38), (152, 136), (8, 136)]
    fill(img, '#cfae7c', 31, poly=pts, scale=14, stretch=(6, .6), contrast=1.2, dark=.3, light=.15)
    d = ImageDraw.Draw(img); d.line([(px(x), px(y)) for x, y in pts[:3]], fill=hexc('#5a3e22'), width=px(4))
    soft(img, lambda dd: dd.ellipse([px(20), px(44), px(46), px(70)], fill=(196, 56, 42, 220)), .5)
    W_ = hexc('#f1ebde')
    ell(img, (44, 76, 110, 106), W_)                                                   # body
    poly(img, [(98, 84), (112, 56), (124, 54), (114, 90)], W_)                          # neck
    poly(img, [(112, 52), (134, 62), (136, 70), (118, 70)], W_)                         # head
    for x0, x1 in ((50, 46), (60, 62), (94, 90), (104, 108)): line(img, [(x0, 100), (x1, 126)], '#e6dfd0', 4.2)
    line(img, [(46, 86), (30, 96), (26, 114)], '#d8d0c0', 4)                            # tail
    line(img, [(104, 60), (116, 50)], '#3a2a20', 3); line(img, [(100, 70), (110, 58)], '#3a2a20', 2.4)   # mane
    ell(img, (124, 59, 128, 63), '#1a1210')
    line(img, [(60, 78), (98, 80)], '#b8322a', 2.2)                                     # saddle cloth
    volume(img, (26, 50, 136, 128), .4, .2); volume(img, (8, 16, 152, 136), .35, .15)
    return 'em_uma', done(img), 't'


def g_kitsune():
    img = I.canvas(140, 150)
    line(img, [(40, 4), (70, 22), (100, 4)], '#b3322a', 2.4)
    face = [(14, 14), (40, 46), (100, 46), (126, 14), (122, 70), (70, 146), (18, 70)]
    fill(img, '#efe6d4', 41, poly=face, scale=10, stretch=(3, .6), contrast=.8, dark=.2, light=.1)
    for s in (-1, 1):
        poly(img, [(70 + s * 50, 22), (70 + s * 34, 46), (70 + s * 48, 52)], '#c84a3a')            # inner ears
        line(img, [(70 + s * 12, 78), (70 + s * 32, 70)], '#c8302a', 3)                             # red eye marks
        line(img, [(70 + s * 14, 84), (70 + s * 28, 80)], '#1a1210', 2.6)                           # closed eyes
        line(img, [(70 + s * 6, 60), (70 + s * 14, 52)], '#c8302a', 2.2)
    ell(img, (63, 128, 77, 140), '#1a1210')
    text(img, '稲荷', 70, 104, 16, '#2a1a12', I.SERIF, brush=True)
    volume(img, (14, 14, 126, 146), .45, .2)
    return 'em_kitsune', done(img), 't'


def g_tanzaku():
    img = I.canvas(170, 300); rnd = random.Random(8); floor_shadow(img, 85, 294, 50)
    fill(img, '#5a4630', 2, poly=[(56, 262), (114, 262), (106, 296), (64, 296)], scale=4); volume(img, (56, 262, 114, 296), .5, .3)   # pot
    for k in range(6): line(img, [(84, 266 - k * 44), (82 + (k % 2) * 4, 222 - k * 44)], '#6f8a4a', 7); line(img, [(78, 222 - k * 44), (90, 222 - k * 44)], '#4d6434', 2)
    for (x0, y0, x1, y1) in ((84, 120, 30, 70), (84, 90, 140, 40), (84, 170, 150, 140), (84, 200, 22, 160)):
        line(img, [(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 - 8), (x1, y1)], '#5f7a40', 2.4)
        for u in np.linspace(.2, 1, 6):
            x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u - 8 * math.sin(u * math.pi); a = rnd.uniform(-.6, .6) + (0 if x1 > x0 else math.pi)
            poly(img, [(x, y), (x + 18 * math.cos(a - .3), y + 18 * math.sin(a - .3) + 6), (x + 6 * math.cos(a), y + 6 * math.sin(a) + 10)], mixc(hexc('#4f7a3a'), hexc('#7a9a52'), rnd.random()))
    for k, (x, y) in enumerate(((40, 84), (124, 56), (60, 150), (136, 152), (36, 172), (106, 108))):
        c = ['#c8402e', '#e0b84a', '#3a5a9a', '#efe6d4', '#7a4a8a', '#3f7a4a'][k]
        line(img, [(x + 6, y - 6), (x + 6, y)], '#d8d0c0', .8)
        fill(img, c, 50 + k, rect=(x, y, x + 12, y + 44), scale=3, contrast=.7); volume(img, (x, y, x + 12, y + 44), .3, .1)
        ink_cols(img, x + 3, y + 6, x + 9, y + 40, rnd, (30, 22, 20, 170), 1, 1)
    return 'em_tanzaku', done(img), 'b'


def g_senba():
    img = I.canvas(130, 330); rnd = random.Random(9)
    ell(img, (20, 2, 110, 22), '#7a5a3a'); ell(img, (30, 7, 100, 17), (0, 0, 0, 0))
    d = ImageDraw.Draw(img); d.ellipse([px(20), px(2), px(110), px(22)], outline=hexc('#7a5a3a'), width=px(3))
    cols = ['#d8384a', '#e8a0b6', '#e0b84a', '#3a5a9a', '#efe6d4', '#6a4a9a', '#3f7a4a']
    for s, x in enumerate((30, 50, 70, 90, 110)):
        line(img, [(x, 14), (x, 312 - (s % 2) * 18)], '#d8d0c0', .8)
        for k in range(9):
            y = 30 + k * 31 + (s % 2) * 12; c = H(cols[(s * 3 + k) % len(cols)]); w = 9
            if y > 300 - (s % 2) * 18: break
            poly(img, [(x - w, y + 3), (x, y - 2), (x + 1, y + 7)], lt(c, .1)); poly(img, [(x + w, y + 3), (x, y - 2), (x + 1, y + 7)], c)
            poly(img, [(x + 1, y + 1), (x + w * .9, y - 7), (x + w * .5, y + 2)], dk(c, .15))
    for x in (30, 50, 70, 90, 110): ell(img, (x - 3, 312 - (x // 20 % 2) * 18, x + 3, 320 - (x // 20 % 2) * 18), '#b8322a')
    return 'em_senba', done(img), 't'


def g_kumade():
    img = I.canvas(180, 270); rnd = random.Random(10); floor_shadow(img, 90, 264, 40)
    line(img, [(90, 150), (90, 262)], '#b89a62', 7)
    for k in range(13):                                             # rake fingers
        a = math.pi * (1.1 + .8 * k / 12); x, y = 90 + math.cos(a) * 82, 150 + math.sin(a) * 120
        line(img, [(90, 150), (x, y), (x + math.cos(a + 1.4) * 8, y + math.sin(a + 1.4) * 8 + 6)], '#c9a870', 3.2)
    d = ImageDraw.Draw(img); d.arc([px(14), px(36), px(166), px(264)], 200, 340, fill=hexc('#a8884e'), width=px(3))
    for k in range(9):                                              # gold koban coins and small charms
        x, y = 40 + (k % 5) * 25 + rnd.uniform(-4, 4), 72 + (k // 5) * 34 + rnd.uniform(-4, 4)
        fill(img, '#e2b84a', 60 + k, ell=(x - 8, y - 11, x + 8, y + 11), scale=2, contrast=.6); volume(img, (x - 8, y - 11, x + 8, y + 11), .6, .3, spec=.3)
    fill(img, '#b8322a', 70, rect=(66, 110, 114, 150), scale=3); text(img, '福', 90, 130, 26, '#f2d890', I.SERIF)
    for x, c in ((52, '#e8a0b6'), (128, '#efe6d4')): fill(img, c, x, ell=(x - 13, 120, x + 13, 146), scale=3); volume(img, (x - 13, 120, x + 13, 146), .5, .3)
    line(img, [(70, 152), (60, 178)], '#d8384a', 3); line(img, [(110, 152), (120, 178)], '#d8384a', 3)
    volume(img, (8, 30, 172, 160), .4, .15)
    return 'em_kumade', done(img), 'b'


def g_suzuri():
    img = I.canvas(190, 120); floor_shadow(img, 95, 112, 84)
    fill(img, '#2a2826', 1, poly=[(16, 52), (130, 52), (134, 104), (12, 104)], scale=4, contrast=1.3); volume(img, (12, 52, 134, 104), .5, .3)
    fill(img, '#181716', 2, ell=(30, 58, 116, 84), scale=3); fill(img, '#0c0b0b', 3, ell=(38, 86, 108, 100), scale=2)
    soft(img, lambda d: d.ellipse([px(46), px(62), px(80), px(72)], fill=(255, 255, 255, 40)), 1)
    fill(img, '#1c1a20', 4, rect=(140, 58, 176, 72), scale=2); text(img, '墨', 158, 65, 9, '#c8a24a', I.SERIF)     # ink stick
    line(img, [(40, 30), (170, 6)], '#c9a870', 6); line(img, [(150, 10), (176, 5)], '#3a2a20', 6)                    # brush
    poly(img, [(40, 26), (22, 38), (16, 42), (24, 40), (42, 34)], '#141010')
    fill(img, '#e0c08c', 5, poly=pent(170, 74, 30, 30), scale=4); ink_cols(img, 162, 86, 178, 102, random.Random(4), (30, 22, 18, 220), 2, 1)
    return 'em_suzuri', done(img), 'b'


def g_inu():
    img = I.canvas(170, 160); floor_shadow(img, 84, 152, 64)
    Wc = '#efe8da'
    for x in (44, 66, 104, 126): fill(img, Wc, x, rect=(x - 9, 104, x + 9, 148), scale=4, contrast=.5)
    fill(img, Wc, 1, ell=(26, 68, 146, 128), scale=6, contrast=.5); volume(img, (26, 68, 146, 128), .5, .3)
    fill(img, Wc, 2, ell=(84, 16, 156, 82), scale=6, contrast=.5); volume(img, (84, 16, 156, 82), .5, .3, spec=.15)
    for s in (-1, 1): poly(img, [(120 + s * 22, 30), (120 + s * 34, 14), (120 + s * 30, 40)], '#c84a3a')
    d = ImageDraw.Draw(img)
    for s in (-1, 1): d.arc([px(120 + s * 13 - 7), px(40), px(120 + s * 13 + 7), px(52)], 200, 340, fill=hexc('#1a1210'), width=px(2.4))
    ell(img, (116, 56, 124, 62), '#1a1210'); d.arc([px(112), px(58), px(128), px(70)], 20, 160, fill=hexc('#b8322a'), width=px(2))
    for x, y, c in ((56, 84, '#d8384a'), (78, 100, '#3f7a4a'), (44, 104, '#e0b84a'), (100, 92, '#3a5a9a')):
        d.ellipse([px(x - 8), px(y - 6), px(x + 8), px(y + 6)], fill=hexc(c)); d.ellipse([px(x - 4), px(y - 3), px(x + 4), px(y + 3)], fill=hexc('#efe8da'))
    line(img, [(90, 78), (150, 80)], '#b8322a', 5); ell(img, (114, 80, 126, 92), '#e2b84a')                 # bib and bell
    line(img, [(28, 82), (14, 64), (20, 56)], '#efe8da', 6)
    return 'em_inu', done(img), 'b'


def g_daruma():
    I.daruma('em_daruma', '', '#b8322a', '願', eyes=2)
    return 'em_daruma', CAP['em_daruma'], 'b'


GIFTS = [g_uma, g_kitsune, g_daruma, g_tanzaku, g_senba, g_kumade, g_suzuri, g_inu]

if __name__ == '__main__':
    ims = [('em_rack', rack(), 'b'), ('em_p0', plaque(0), 't'), ('em_p1', plaque(1), 't')] + [f() for f in GIFTS]
    W = 1000; x = y = rowh = 0; pos = {}
    for iid, im, _ in sorted(ims, key=lambda t: -t[1].height):
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[iid] = (x, y, im.width, im.height); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for iid, im, _ in ims: at.paste(im, pos[iid][:2])
    at.save(os.path.join(ASSETS, 'items', 'atlas_em.webp'), 'WEBP', quality=88, alpha_quality=92, method=6)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'out'), exist_ok=True)
    pv = Image.new('RGBA', at.size, (34, 30, 28, 255)); pv.alpha_composite(at); pv.convert('RGB').save(os.path.join(os.path.dirname(__file__), 'out', 'atlas_em.png'))
    print(json.dumps({'size': [W, y + rowh], 'at': {iid: list(p) + [a] for (iid, _, a), p in zip(ims, [pos[i] for i, _, _ in ims])}, 'hooks': HOOKS, 'rack': [RW, RH]}))
