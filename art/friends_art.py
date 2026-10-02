#!/usr/bin/env python3
"""«Истории друзей» (feat/friends.js): seven keepsakes, one per gate guest, category «Памятные вещи друзей»,
packed into ONE atlas assets/items/atlas_yu.webp. Prints the rect map as JSON (pasted into feat/friends.js).
Preview → art/out/atlas_yu.png.   Usage: friends_art.py [assets dir]"""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw
ASSETS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'assets')
sys.argv = [sys.argv[0], os.path.join(os.path.dirname(__file__), 'out')]     # items.py reads its out dir from argv[1]
import paint as P
from paint import hexc
import items as I
from items import px, fill, volume, line, ell, poly, text, soft, floor_shadow

CAP = {}


def done(img, seed=7):
    out = img.resize((P.W, P.H), Image.LANCZOS); a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .88; a[..., :3] += np.random.default_rng(seed).normal(0, 3.2, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def cap(img, iid, *a, **k): CAP[iid] = done(img)
I.save = cap


def glow(im, cx, cy, rx, ry, rgb):
    """Light the picture from inside (paper lit by a flame) where it is opaque."""
    a = np.asarray(im, np.float32); h, w = a.shape[:2]; yy, xx = np.mgrid[0:h, 0:w]
    g = np.exp(-(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)) * (a[..., 3] > 0)
    for c in range(3): a[..., c] += rgb[c] * g
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def shell():
    """Kappa: a freshwater clam shell from the revived river, nacre inside, a wet pebble beside it."""
    W, Hh = 140, 100; img = I.canvas(W, Hh); floor_shadow(img, 70, 90, 60, 100)
    ell(img, (96, 66, 126, 88), '#55605a'); volume(img, (96, 66, 126, 88), .7, .4, spec=.5)          # pebble
    outer = [(70 + 58 * math.cos(t), 62 + 40 * math.sin(t) * (1 if math.sin(t) < 0 else .55)) for t in np.linspace(0, 2 * math.pi, 64)]
    fill(img, '#3a3a2c', 11, poly=outer, scale=3, contrast=1.3, dark=.5, light=.3)
    d = ImageDraw.Draw(img)
    for k in range(1, 6):                                                                           # growth rings
        r = k / 6; d.arc([px(70 - 58 * r), px(62 - 40 * r), px(70 + 58 * r), px(62 + 40 * r)], 190, 350, fill=hexc('#5c5a44'), width=px(1.2))
    inner = [(70 + 46 * math.cos(t), 64 + 26 * math.sin(t)) for t in np.linspace(math.pi * 1.05, math.pi * 1.95, 30)] + [(112, 66), (28, 66)]
    fill(img, '#d9d4e2', 12, poly=inner, scale=2, contrast=1.1, dark=.25, light=.35)
    a = np.asarray(img, np.float32); h, w = a.shape[:2]; yy, xx = np.mgrid[0:h, 0:w]               # nacre: soft rainbow sheen
    m = np.asarray(I.mask_poly(img, inner), np.float32) / 255; ph = (xx / w * 9 + yy / h * 5)
    for c, off in enumerate((0, 2.1, 4.2)): a[..., c] += m * 13 * np.sin(ph + off)
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')
    volume(img, (12, 20, 128, 90), .6, .35, spec=.45)
    for x, y in ((50, 50), (84, 46)): ell(img, (x - 2, y - 2, x + 2, y + 2), (255, 255, 255, 200))    # drops
    return done(img, 21)


def fox_lantern():
    """Fox bride: the little procession lantern Kotaro carried, paper lit by cold fox fire, 狐."""
    I.chochin('yu_fox', '', '#ece6da', '狐', tall=False, ink='#8a1e12')
    im = CAP['yu_fox']; w, h = im.size
    return glow(im, w / 2, h * .55, w * .34, h * .28, (-10, 22, 40))


def chawan():
    """Tanuki: a rough raku tea bowl with a tanuki paw print on its side."""
    I.chawan('yu_chawan', '', '#6a4632', 'raku')
    im = CAP['yu_chawan']; img = I.canvas(*im.size); img.alpha_composite(im.resize(img.size, Image.LANCZOS))
    cx, cy = 82, 58
    ell(img, (cx - 9, cy - 5, cx + 9, cy + 9), '#e8d8b8')                                             # the pad
    for dx, dy in ((-11, -10), (-4, -15), (4, -15), (11, -10)): ell(img, (cx + dx - 3.4, cy + dy - 3.4, cx + dx + 3.4, cy + dy + 3.4), '#e8d8b8')
    volume(img, (12, 26, 138, 96), .3, .2)
    return done(img, 23)


def bachi():
    """Nekomata: O-Sei's shamisen plectrum (ivory, a fan-shaped blade on a narrow grip) lying on a folded purple silk cloth."""
    W, Hh = 160, 96; img = I.canvas(W, Hh); floor_shadow(img, 80, 88, 70, 90)
    fill(img, '#4a2a52', 31, poly=[(8, 72), (118, 54), (154, 74), (40, 94)], scale=4, contrast=1.1, dark=.45, light=.3)   # fukusa
    line(img, [(16, 76), (120, 58), (150, 74)], '#7a5a86', 1.2)
    a = math.radians(-62); ca, sa = math.cos(a), math.sin(a)
    T = lambda u, v: (44 + u * ca - v * sa * .55, 80 + u * sa * .55 + v * ca)      # local (u along the bachi, v across) → picture, squashed: it lies flat
    grip = [T(0, -6), T(0, 6), T(46, 7), T(46, -7)]
    blade = [T(44, -7), T(44, 7), T(118, 34)] + [T(122 - 4 * math.cos(k / 8 * math.pi), 34 - 68 * k / 8) for k in range(9)] + [T(118, -34)]
    fill(img, '#d8ccb0', 34, poly=grip, scale=3, contrast=1.2, dark=.3, light=.3)
    fill(img, '#ebe2cc', 33, poly=blade, scale=3, contrast=1.2, dark=.28, light=.35)
    line(img, [T(116, -32), T(120, 0), T(116, 32)], '#f7f0de', 1.3)                      # the thin playing edge
    for k in range(5): line(img, [T(6 + k * 8, -5), T(6 + k * 8, 5)], '#b8a888', .6)       # worn grain on the grip
    volume(img, (20, 4, 150, 90), .55, .3, spec=.35)
    return done(img, 37)


def fuda():
    """Akaname: the night bath-keeper's wooden name tag on a cord: 湯 and his name 垢嘗, cut with a claw."""
    W, Hh = 80, 180; img = I.canvas(W, Hh); cx = 40
    line(img, [(cx, 0), (cx - 8, 30), (cx, 40)], '#b8322a', 2); line(img, [(cx, 0), (cx + 8, 30), (cx, 40)], '#b8322a', 2)
    tag = [(12, 40), (68, 40), (68, 160), (40, 176), (12, 160)]
    fill(img, '#b08a5a', 41, poly=tag, scale=6, stretch=(.3, 3), contrast=1.2, dark=.4, light=.25)
    ell(img, (cx - 4, 46, cx + 4, 54), '#2a1a10')
    text(img, '湯', cx, 80, 34, '#2a140a', I.SERIF, brush=True)
    text(img, '垢', cx, 118, 20, '#3a2010', I.SERIF, brush=True); text(img, '嘗', cx, 140, 20, '#3a2010', I.SERIF, brush=True)
    for k in range(5): line(img, [(46 + k, 108 + k * 8), (50 + k, 112 + k * 8)], '#e8d0a0', .6)       # fresh claw cuts
    volume(img, (12, 40, 68, 176), .5, .3)
    return done(img, 43)


def kanban():
    """Obake: the old signboard of the Tsuruya inn (鶴屋), weathered wood on two cords, a crane painted in the corner."""
    W, Hh = 230, 130; img = I.canvas(W, Hh)
    for x in (40, 190): line(img, [(x, 0), (x, 34)], '#3a2a1a', 2)
    fill(img, '#6a4a30', 51, rect=(10, 32, 220, 120), scale=7, stretch=(3, .3), contrast=1.3, dark=.5, light=.25)
    ImageDraw.Draw(img).rectangle([px(10), px(32), px(220), px(120)], outline=hexc('#2a1a10'), width=px(3))
    text(img, '鶴屋', 132, 78, 52, '#e8dcc0', I.SERIF, brush=True)
    ell(img, (26, 50, 62, 66), '#e8e2d4'); line(img, [(58, 56), (74, 40), (80, 42)], '#e8e2d4', 2.4)  # the crane
    ell(img, (74, 38, 80, 44), '#c03a2a'); line(img, [(32, 64), (28, 96)], '#2a2018', 1.4); line(img, [(40, 64), (44, 96)], '#2a2018', 1.4)
    poly(img, [(26, 56), (14, 50), (24, 62)], '#2a2018')
    a = np.asarray(img, np.float32); rng = np.random.default_rng(5)                                  # weathering: missing paint, cracks
    a[..., :3] *= (1 - .18 * rng.random(a.shape[:2]))[..., None]
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')
    line(img, [(150, 32), (156, 60), (152, 74)], '#1a120a', 1.2)
    volume(img, (10, 32, 220, 120), .4, .25)
    return done(img, 53)


def koma():
    """Zashiki-warashi: the old spinning top she took from her first house in Tōno, darkened by years."""
    I.toy('yu_koma', '', 'koma', col='#8a2a22')
    im = CAP['yu_koma']; a = np.asarray(im, np.float32); a[..., :3] *= [.78, .74, .7]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


if __name__ == '__main__':
    ims = [('yu_shell', shell(), 'b'), ('yu_fox', fox_lantern(), 't'), ('yu_chawan', chawan(), 'b'), ('yu_bachi', bachi(), 'b'),
           ('yu_fuda', fuda(), 't'), ('yu_kanban', kanban(), 't'), ('yu_koma', koma(), 'b')]
    W = sum(im.width for _, im, _ in ims) + 2 * len(ims); x = 0; pos = {}
    for iid, im, _ in ims: pos[iid] = (x, 0, im.width, im.height); x += im.width + 2
    at = Image.new('RGBA', (W, max(im.height for _, im, _ in ims)), (0, 0, 0, 0))
    for iid, im, _ in ims: at.paste(im, pos[iid][:2])
    at.save(os.path.join(ASSETS, 'items', 'atlas_yu.webp'), 'WEBP', quality=88, alpha_quality=92, method=6)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'out'), exist_ok=True)
    pv = Image.new('RGBA', at.size, (34, 30, 28, 255)); pv.alpha_composite(at); pv.convert('RGB').resize((at.width * 2, at.height * 2)).save(os.path.join(os.path.dirname(__file__), 'out', 'atlas_yu.png'))
    print(json.dumps({'size': list(at.size), 'at': {iid: list(pos[iid]) + [a] for iid, _, a in ims}}))
