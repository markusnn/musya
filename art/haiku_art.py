#!/usr/bin/env python3
"""«Хайку недели» (feat/haiku.js): two things of the category «Хайку» packed into ONE atlas assets/items/atlas_hi.webp —
hi_kake (a brocade tanzaku-kake holder with a poem strip, hangs) and hi_shikishi (a gold-edged shikishi board on a small stand).
Prints the rect map as JSON (pasted into feat/haiku.js). Preview → art/out/atlas_hi.png.
Usage: haiku_art.py [assets dir]"""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw
ASSETS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'assets')
sys.argv = [sys.argv[0], os.path.join(os.path.dirname(__file__), 'out')]     # items.py reads its out dir from argv[1]
import paint as P
from paint import hexc, mixc
import items as I
from items import px, fill, volume, line, ell, poly, text, soft, floor_shadow, dk, lt, H


def done(img):
    out = img.resize((P.W, P.H), Image.LANCZOS); a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .88; a[..., :3] += np.random.default_rng(17).normal(0, 3.0, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def ink_cols(img, x0, y0, x1, y1, rnd, col=(28, 20, 16, 235), cols=3, w=1.6, stagger=0):
    """Fake vertical calligraphy: short strokes in columns, right to left; stagger lowers each next column."""
    d = ImageDraw.Draw(img); cw = (x1 - x0) / cols
    for c in range(cols):
        x = x1 - cw * (c + .5); y = y0 + c * stagger + rnd.uniform(0, 3); ye = y1 - (cols - 1 - c) * stagger * .3
        while y < ye - 4:
            L = rnd.uniform(2.5, 6.5); dx = rnd.uniform(-1.8, 1.8)
            d.line([(px(x + dx), px(y)), (px(x - dx * .6), px(y + L))], fill=col, width=px(w * rnd.uniform(.7, 1.25)))
            if rnd.random() < .5: d.line([(px(x - 2.6), px(y + L * .5)), (px(x + 2.6), px(y + L * .4))], fill=col, width=px(w * .8))
            y += L + rnd.uniform(1.2, 3.2)


def flecks(img, box, rnd, n, col=(226, 186, 98)):
    """Kirikane: little gold squares and dust scattered over paper."""
    d = ImageDraw.Draw(img); x0, y0, x1, y1 = box
    for _ in range(n):
        x, y, s = rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(.6, 2.6)
        d.rectangle([px(x), px(y), px(x + s), px(y + s * rnd.uniform(.6, 1.2))], fill=col + (int(rnd.uniform(120, 230)),))


def kake():
    """Tanzaku-kake: a narrow brocade mount on a cord; the cream strip with a poem sits in it."""
    img = I.canvas(96, 330); rnd = random.Random(3)
    line(img, [(48, 4), (30, 34)], '#c8a86a', 2.2); line(img, [(48, 4), (66, 34)], '#c8a86a', 2.2)                 # hanging cord
    ell(img, (43, 1, 53, 9), '#8a6a3a')
    fill(img, '#2c3148', 1, rect=(16, 30, 80, 312), scale=3, contrast=1.1)                                        # indigo brocade
    d = ImageDraw.Draw(img)
    for k in range(18):                                                                                             # gold clouds pattern
        y = 38 + k * 15.5; x = 22 if k % 2 else 64
        d.arc([px(x - 6), px(y - 4), px(x + 6), px(y + 4)], 180, 360, fill=(206, 168, 92, 200), width=px(1.2))
        d.arc([px(x - 2), px(y - 6), px(x + 8), px(y + 2)], 180, 360, fill=(206, 168, 92, 160), width=px(1))
    volume(img, (16, 30, 80, 312), .45, .25)
    fill(img, '#5a4630', 2, rect=(12, 26, 84, 36), scale=3); volume(img, (12, 26, 84, 36), .5, .3)               # top and bottom bars
    fill(img, '#5a4630', 3, rect=(12, 306, 84, 316), scale=3); volume(img, (12, 306, 84, 316), .5, .3)
    fill(img, '#ece0c4', 4, rect=(30, 46, 66, 298), scale=4, contrast=.5)                                          # the strip
    soft(img, lambda d: d.rectangle([px(30), px(46), px(66), px(70)], fill=(120, 150, 190, 70)), 3)             # sky dye on top
    soft(img, lambda d: d.rectangle([px(30), px(270), px(66), px(298)], fill=(150, 110, 170, 60)), 3)           # dusk dye below
    flecks(img, (31, 48, 65, 296), rnd, 90)
    ink_cols(img, 34, 82, 62, 280, rnd, (30, 22, 18, 230), 2, 1.5, stagger=26)
    ell(img, (50, 266, 60, 276), '#b8322a')                                                                          # hanko
    volume(img, (30, 46, 66, 298), .25, .12)
    for x in (40, 56): line(img, [(x, 316), (x + rnd.uniform(-2, 2), 328)], '#b8322a', 2)                         # tassels
    return 'hi_kake', done(img), 't'


def shikishi():
    """A shikishi board (gold edge, flecked paper, a cascading poem and a seal) on a small lacquered stand."""
    img = I.canvas(176, 214); rnd = random.Random(5); floor_shadow(img, 88, 208, 74)
    fill(img, '#3a2418', 1, poly=[(30, 206), (146, 206), (138, 196), (38, 196)], scale=3); volume(img, (30, 196, 146, 206), .5, .3)   # stand foot
    line(img, [(52, 196), (66, 120)], '#3a2418', 5); line(img, [(124, 196), (110, 120)], '#3a2418', 5)
    fill(img, '#c8a050', 2, rect=(22, 14, 154, 188), scale=3, contrast=.8); volume(img, (22, 14, 154, 188), .4, .2, spec=.15)          # gold edge
    fill(img, '#efe4cc', 3, rect=(27, 19, 149, 183), scale=5, contrast=.5)
    soft(img, lambda d: d.ellipse([px(70), px(10), px(170), px(80)], fill=(214, 168, 96, 70)), 10)                                    # gold mist
    soft(img, lambda d: d.ellipse([px(10), px(140), px(110), px(200)], fill=(160, 120, 170, 50)), 10)
    d = ImageDraw.Draw(img)
    d.ellipse([px(104), px(30), px(136), px(62)], fill=(218, 196, 140, 150))                                                          # pale moon
    flecks(img, (28, 20, 148, 182), rnd, 160)
    for k in range(5):                                                                                                                 # a few red maple leaves
        x, y = 40 + k * 9 + rnd.uniform(-3, 3), 150 + rnd.uniform(-8, 20)
        for a in range(5):
            t = -math.pi / 2 + (a - 2) * .55; poly(img, [(x, y), (x + 7 * math.cos(t - .18), y + 7 * math.sin(t - .18)), (x + 9 * math.cos(t), y + 9 * math.sin(t)), (x + 7 * math.cos(t + .18), y + 7 * math.sin(t + .18))], '#b8402a')
    ink_cols(img, 46, 34, 140, 170, rnd, (26, 20, 16, 235), 4, 1.7, stagger=18)
    fill(img, '#b8322a', 6, rect=(124, 160, 138, 174), scale=2); text(img, '句', 131, 167, 10, '#f2e0c0', I.SERIF)
    return 'hi_shikishi', done(img), 'b'


if __name__ == '__main__':
    ims = [kake(), shikishi()]
    W = sum(im.width for _, im, _ in ims) + 2; x = 0; pos = {}
    for iid, im, _ in ims: pos[iid] = (x, 0, im.width, im.height); x += im.width + 2
    Hh = max(im.height for _, im, _ in ims)
    at = Image.new('RGBA', (W, Hh), (0, 0, 0, 0))
    for iid, im, _ in ims: at.paste(im, pos[iid][:2])
    at.save(os.path.join(ASSETS, 'items', 'atlas_hi.webp'), 'WEBP', quality=88, alpha_quality=92, method=6)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'out'), exist_ok=True)
    pv = Image.new('RGBA', at.size, (34, 30, 28, 255)); pv.alpha_composite(at); pv.convert('RGB').resize((at.width * 2, at.height * 2)).save(os.path.join(os.path.dirname(__file__), 'out', 'atlas_hi.png'))
    print(json.dumps({'size': [W, Hh], 'at': {iid: list(pos[iid]) + [a] for iid, _, a in ims}}))
