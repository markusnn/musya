#!/usr/bin/env python3
"""«Слово дня» (feat/kanji.js): four calligraphy things «Каллиграфия» packed into ONE atlas assets/items/atlas_kj.webp.
The hanging scroll is painted with a BLANK paper: the game writes the player's best kanji on it.
Prints the rect map (pasted into feat/kanji.js). Preview → art/out/atlas_kj.png.  Usage: kanji_art.py"""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw
ASSETS = os.path.join(os.path.dirname(__file__), '..', 'assets')
sys.argv = [sys.argv[0], os.path.join(os.path.dirname(__file__), 'out')]     # items.py reads its out dir from argv[1]
import paint as P
from paint import hexc, mixc
import items as I
from items import px, fill, volume, line, ell, poly, text, soft, floor_shadow, dk, lt, H


def done(img):
    out = img.resize((P.W, P.H), Image.LANCZOS); a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .88; a[..., :3] += np.random.default_rng(13).normal(0, 3.2, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def brush(img, x0, y0, x1, y1, w=5, wood='#c9a870', tip='#141010', cap='#3a2a20'):
    """A brush lying from (x0,y0) (tip) to (x1,y1) (end)."""
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    hx, hy = x0 + ux * 22, y0 + uy * 22
    line(img, [(hx, hy), (x1, y1)], wood, w); line(img, [(x1 - ux * 12, y1 - uy * 12), (x1, y1)], cap, w + .6)
    line(img, [(hx + nx * w * .3, hy + ny * w * .3), (x1 + nx * w * .3, y1 + ny * w * .3)], lt(H(wood), .3), w * .25)
    poly(img, [(hx + nx * w * .55, hy + ny * w * .55), (x0 + nx * .6, y0 + ny * .6), (x0, y0), (hx - nx * w * .55, hy - ny * w * .55)], tip)


def scroll():          # kakejiku: rod + cord, indigo brocade, cream paper (blank), bottom roller
    img = I.canvas(120, 330); rnd = random.Random(3)
    line(img, [(60, 2), (36, 16)], '#c9a24a', 1.4); line(img, [(60, 2), (84, 16)], '#c9a24a', 1.4)
    fill(img, '#2a3348', 1, rect=(10, 16, 110, 310), scale=6, stretch=(1, 3), contrast=1.2, dark=.35, light=.15)   # brocade
    d = ImageDraw.Draw(img); gold = hexc('#b89a58')
    for _ in range(140):
        x, y = rnd.uniform(12, 108), rnd.uniform(18, 308); r = rnd.uniform(.8, 1.6)
        d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=mixc(hexc('#2a3348'), gold, rnd.uniform(.25, .5)))
    fill(img, '#6a5a3a', 2, rect=(10, 40, 110, 44), scale=3); fill(img, '#6a5a3a', 3, rect=(10, 266, 110, 270), scale=3)   # thin gold bands
    for x in (40, 80): fill(img, '#3a4258', 4 + x, rect=(x - 3, 16, x + 3, 40), scale=2)                   # futai strips
    fill(img, '#e6dbc2', 5, rect=(20, 46, 100, 264), scale=10, stretch=(1, 2), contrast=.6, dark=.12, light=.08)   # paper
    soft(img, lambda dd: dd.rectangle([px(20), px(46), px(100), px(52)], fill=(60, 40, 20, 50)), 2)
    fill(img, '#3a2618', 6, rect=(6, 10, 114, 18), scale=3); volume(img, (6, 10, 114, 18), .5, .3)           # top rod
    fill(img, '#2a1c12', 7, rect=(4, 308, 116, 320), scale=3); volume(img, (4, 308, 116, 320), .6, .3, spec=.2)
    for x in (0, 110): fill(img, '#d8c8a0', 8 + x, rect=(x, 306, x + 10, 322), scale=2); volume(img, (x, 306, x + 10, 322), .6, .3, spec=.3)
    volume(img, (10, 16, 110, 310), .25, .1)
    return 'kj_scroll', done(img), 't'


def rack():            # fudekake: a little wooden rack, five brushes hanging tip-down
    img = I.canvas(170, 210); rnd = random.Random(4); floor_shadow(img, 85, 204, 76)
    fill(img, '#3a2618', 1, rect=(14, 186, 156, 204), scale=4, stretch=(4, .4)); volume(img, (14, 186, 156, 204), .5, .3)
    for x in (24, 140): fill(img, '#4a3220', x, rect=(x, 30, x + 8, 190), scale=3, stretch=(.3, 4)); volume(img, (x, 30, x + 8, 190), .5, .3)
    fill(img, '#5a3e28', 2, poly=[(8, 30), (162, 30), (166, 22), (4, 22)], scale=3, stretch=(4, .4)); volume(img, (4, 22, 166, 32), .5, .3)
    for k, x in enumerate((44, 64, 84, 104, 124)):
        L = 120 - abs(k - 2) * 14 + rnd.uniform(-6, 6); w = 6.5 - abs(k - 2) * .7
        line(img, [(x, 31), (x, 38)], '#8a2a22', 1.2); ell(img, (x - 3, 36, x + 3, 42), '#8a2a22')
        wood = ['#c9a870', '#7a4a2a', '#c9a870', '#2a2018', '#b89a62'][k]
        line(img, [(x, 42), (x, 42 + L)], wood, w); line(img, [(x, 42), (x, 52)], '#2a1c12', w + .4)
        line(img, [(x - w * .2, 52), (x - w * .2, 40 + L)], lt(H(wood), .35), w * .22)
        tip = '#141010' if k != 2 else '#e8dcc0'
        poly(img, [(x - w * .6, 40 + L), (x + w * .6, 40 + L), (x + w * .45, 58 + L), (x, 70 + L), (x - w * .45, 58 + L)], tip)
        if k != 2: poly(img, [(x - w * .2, 62 + L), (x + w * .1, 62 + L), (x, 70 + L)], '#2a1a14')
    volume(img, (4, 20, 166, 205), .3, .1)
    return 'kj_rack', done(img), 'b'


def box():             # suzuribako: an open black-lacquer box with gold maki-e, inkstone, ink stick, brush, dropper
    img = I.canvas(220, 140); rnd = random.Random(5); floor_shadow(img, 110, 134, 102)
    fill(img, '#16120f', 1, poly=[(150, 18), (212, 30), (206, 104), (146, 92)], scale=5, contrast=1.3)            # lid leaning behind
    d = ImageDraw.Draw(img)
    for _ in range(3):                                                                                         # gold autumn grass on the lid
        x = rnd.uniform(160, 200); line(img, [(x, 96), (x - 6, 70), (x + 4, 46)], '#b8964a', 1.2)
    ell(img, (182, 40, 198, 56), '#d8b860')                                                                    # gold moon
    fill(img, '#1c1612', 2, poly=[(10, 60), (170, 60), (176, 128), (4, 128)], scale=5, contrast=1.3); volume(img, (4, 60, 176, 128), .5, .3, spec=.12)
    fill(img, '#0c0a08', 3, poly=[(18, 66), (162, 66), (166, 116), (14, 116)], scale=4)                        # inside
    line(img, [(10, 60), (170, 60)], '#a8884a', 1.4)
    fill(img, '#2a2826', 4, rect=(24, 70, 86, 112), scale=3, contrast=1.2); volume(img, (24, 70, 86, 112), .5, .3)   # inkstone
    fill(img, '#121112', 5, ell=(30, 74, 80, 96), scale=2); fill(img, '#050505', 6, ell=(34, 98, 76, 108), scale=2)
    soft(img, lambda dd: dd.ellipse([px(38), px(76), px(60), px(82)], fill=(255, 255, 255, 46)), .8)
    fill(img, '#1c1a20', 7, rect=(94, 74, 108, 110), scale=2); text(img, '墨', 101, 84, 8, '#c8a24a', I.SERIF)   # ink stick
    brush(img, 116, 104, 158, 74, 4.6)
    fill(img, '#7a8a8c', 8, ell=(126, 74, 150, 92), scale=2); volume(img, (126, 74, 150, 92), .6, .3, spec=.4)       # water dropper
    ell(img, (136, 74, 140, 78), '#3a4448')
    line(img, [(4, 128), (176, 128)], '#a8884a', 1.4)
    return 'kj_box', done(img), 'b'


def desk():            # fuzukue: a low writing desk, a sheet with 夢, a bronze paperweight, a brush on a rest
    img = I.canvas(260, 160); floor_shadow(img, 130, 154, 124)
    for x in (22, 222): fill(img, '#2e1e14', x, rect=(x, 66, x + 16, 152), scale=3, stretch=(.4, 3)); volume(img, (x, 66, x + 16, 152), .5, .3)
    fill(img, '#4a3020', 1, poly=[(20, 40), (240, 40), (252, 66), (8, 66)], scale=6, stretch=(5, .4), contrast=1.2)   # top
    fill(img, '#3a2418', 2, rect=(8, 66, 252, 76), scale=4, stretch=(6, .3)); volume(img, (8, 40, 252, 76), .45, .2, spec=.08)
    fill(img, '#2a2a2c', 3, rect=(24, 30, 236, 38), scale=2)                                                          # felt mat edge
    fill(img, '#e8dfca', 4, poly=[(60, 30), (180, 30), (186, 60), (54, 60)], scale=6, contrast=.5, dark=.1, light=.06)
    text(img, '夢', 122, 45, 26, '#1a1410', I.SERIF, brush=True)
    fill(img, '#5a4a30', 5, rect=(60, 26, 182, 31), scale=2); volume(img, (60, 26, 182, 31), .6, .3, spec=.4)        # paperweight
    fill(img, '#9a8a6a', 6, ell=(196, 42, 230, 54), scale=2); volume(img, (196, 42, 230, 54), .6, .3, spec=.3)     # brush rest
    brush(img, 192, 52, 238, 30, 4.4)
    soft(img, lambda dd: dd.ellipse([px(160), px(40), px(176), px(48)], fill=(20, 14, 10, 120)), .8)                  # an ink drop
    return 'kj_desk', done(img), 'b'


if __name__ == '__main__':
    ims = [scroll(), rack(), box(), desk()]
    W = sum(im.width for _, im, _ in ims) + 2 * len(ims); x = 0; pos = {}
    for iid, im, _ in ims: pos[iid] = (x, 0, im.width, im.height); x += im.width + 2
    at = Image.new('RGBA', (W, max(im.height for _, im, _ in ims)), (0, 0, 0, 0))
    for iid, im, _ in ims: at.paste(im, pos[iid][:2])
    at.save(os.path.join(ASSETS, 'items', 'atlas_kj.webp'), 'WEBP', quality=88, alpha_quality=92, method=6)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'out'), exist_ok=True)
    pv = Image.new('RGBA', at.size, (40, 36, 32, 255)); pv.alpha_composite(at); pv.save(os.path.join(os.path.dirname(__file__), 'out', 'atlas_kj.png'))
    print(json.dumps({'atlas': at.size, 'pos': pos}))
