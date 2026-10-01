#!/usr/bin/env python3
"""«Капсула времени» (feat/capsule.js, prefix tc): a kiri-wood box tied with a purple cord (closed and opened),
a bundle of tied letters and a small wall shelf for the kura — all in ONE atlas assets/items/atlas_tc.webp.
Prints the rect map as JSON (pasted into feat/capsule.js). Preview → art/out/atlas_tc.png.
Usage: capsule_art.py [assets dir]"""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw
ASSETS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'assets')
sys.argv = [sys.argv[0], os.path.join(os.path.dirname(__file__), 'out')]     # items.py reads its out dir from argv[1]
import paint as P
import items as I
from items import px, fill, volume, line, ell, poly, text, soft, floor_shadow, dk, lt, H

KIRI, KIRI_D, CORD = '#cdb995', '#a89270', '#6a3f7a'


def done(img):
    out = img.resize((P.W, P.H), Image.LANCZOS); a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .9; a[..., :3] += np.random.default_rng(7).normal(0, 3, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def grain(img, pts, seed, n, vert=True, a=46):
    """fine straight paulownia grain inside a quad (lines run along its first or second edge)"""
    m = I.mask_poly(img, pts); l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l); r = random.Random(seed)
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pts
    for k in range(n):
        t = (k + r.uniform(-.3, .3)) / n
        if vert: A, B = (x0 + (x1 - x0) * t, y0 + (y1 - y0) * t), (x3 + (x2 - x3) * t, y3 + (y2 - y3) * t)
        else: A, B = (x0 + (x3 - x0) * t, y0 + (y3 - y0) * t), (x1 + (x2 - x1) * t, y1 + (y2 - y1) * t)
        d.line([(px(A[0]), px(A[1])), (px(B[0]), px(B[1]))], fill=(70, 50, 30, r.randint(a // 2, a)), width=max(1, px(r.uniform(.4, .9))))
    z = Image.new('RGBA', img.size, (0, 0, 0, 0)); z.paste(l, (0, 0), m); img.alpha_composite(z)


def cord(img, pts, w=4.2):
    line(img, pts, dk(H(CORD), .45), w + 1.4); line(img, pts, CORD, w); line(img, [(x - .6, y - .9) for x, y in pts], lt(H(CORD), .35), w * .28)


def bow(img, cx, cy, s=1.0):
    for sx in (-1, 1):                                                           # two loops + two tails
        b = (cx - 22 * s, cy - 9 * s, cx - 2 * s, cy + 3 * s) if sx < 0 else (cx + 2 * s, cy - 9 * s, cx + 22 * s, cy + 3 * s)
        fill(img, CORD, 40 + sx, ell=b, scale=2, contrast=.7); volume(img, b, .6, .4, spec=.12)
        ell(img, (b[0] + 6 * s, b[1] + 4 * s, b[2] - 6 * s, b[3] - 4 * s), dk(H(CORD), .55))
    cord(img, [(cx - 2 * s, cy + 2 * s), (cx - 8 * s, cy + 14 * s), (cx - 6 * s, cy + 22 * s)], 3.4 * s)
    cord(img, [(cx + 2 * s, cy + 2 * s), (cx + 9 * s, cy + 12 * s), (cx + 13 * s, cy + 21 * s)], 3.4 * s)
    fill(img, CORD, 44, ell=(cx - 5 * s, cy - 6 * s, cx + 5 * s, cy + 4 * s), scale=2); volume(img, (cx - 5 * s, cy - 6 * s, cx + 5 * s, cy + 4 * s), .7, .4)


def box_closed():
    img = I.canvas(180, 140)
    floor_shadow(img, 92, 126, 84, 120)
    F, R, T = [(20, 70), (140, 70), (140, 126), (20, 126)], [(140, 70), (166, 52), (166, 108), (140, 126)], [(20, 70), (46, 52), (166, 52), (140, 70)]
    fill(img, KIRI, 1, poly=F, scale=4, stretch=(.25, 4), contrast=.8, dark=.25, light=.15); grain(img, F, 1, 26)
    fill(img, KIRI_D, 2, poly=R, scale=4, stretch=(.25, 4), contrast=.8, dark=.3); grain(img, R, 2, 8)
    fill(img, lt(H(KIRI), .12), 3, poly=T, scale=4, stretch=(4, .25), contrast=.7, dark=.2, light=.1); grain(img, T, 3, 10, vert=False, a=34)
    volume(img, (20, 52, 166, 126), .35, .18)
    soft(img, lambda d: d.rectangle([px(20), px(86), px(140), px(90)], fill=(40, 26, 14, 90)), 1.2)       # lid seam
    line(img, [(20, 87), (140, 87), (166, 69)], dk(H(KIRI), .45), .9)
    line(img, [(20, 70), (140, 70), (166, 52)], lt(H(KIRI), .35), 1.1)                                        # lit edges
    line(img, [(140, 70), (140, 126)], dk(H(KIRI), .3), .8)
    # paper label with an ink kanji on the front
    poly(img, [(100, 92), (126, 92), (126, 120), (100, 120)], '#efe7d4'); volume(img, (100, 92, 126, 120), .3, .15)
    text(img, '時', 113, 106, 17, '#1d1612', brush=True)
    # the cord: crosswise on the lid, down the front and the right side
    cord(img, [(33, 61), (153, 61)]); cord(img, [(80, 70), (106, 52)]); cord(img, [(80, 70), (80, 126)]); cord(img, [(153, 61), (153, 117)], 3.4)
    bow(img, 93, 60, 1.0)
    return done(img)


def box_open(letter=True):
    img = I.canvas(210, 160)
    floor_shadow(img, 98, 146, 92, 120)
    # the lid leans against the back, its top (with the label and the loose cord) towards us
    L = [(62, 14), (186, 6), (190, 60), (58, 70)]
    fill(img, lt(H(KIRI), .06), 11, poly=L, scale=4, stretch=(4, .25), contrast=.7, dark=.22); grain(img, L, 11, 10, vert=False, a=34); volume(img, (58, 6, 190, 70), .4, .2)
    line(img, [(58, 70), (190, 60)], dk(H(KIRI), .5), 2.2)
    soft(img, lambda d: d.polygon([(px(46), px(74)), (px(166), px(74)), (px(166), px(80)), (px(46), px(80))], fill=(20, 12, 6, 120)), 2)
    poly(img, [(150, 18), (170, 16), (172, 46), (152, 48)], '#efe7d4'); text(img, '時', 161, 32, 14, '#1d1612', brush=True)
    F, R, O = [(20, 90), (140, 90), (140, 146), (20, 146)], [(140, 90), (166, 72), (166, 128), (140, 146)], [(20, 90), (46, 72), (166, 72), (140, 90)]
    poly(img, O, '#2a1d14')                                                      # the dark inside
    poly(img, [(46, 72), (166, 72), (164, 80), (52, 80)], '#8a7454'); poly(img, [(20, 90), (46, 72), (52, 80), (30, 90)], '#6e5a40')   # inner back + left walls
    # a folded letter standing in the box
    if letter: poly(img, [(70, 52), (118, 46), (124, 92), (74, 96)], '#efe4cc'); volume(img, (70, 46, 124, 96), .35, .2)
    if letter:
        line(img, [(96, 49), (99, 94)], '#cdbd9c', 1)
        for k in range(4): line(img, [(80 + k * 9, 58 - k), (81 + k * 9, 76 - k)], '#3a2a20', 1.1)
    fill(img, KIRI, 12, poly=F, scale=4, stretch=(.25, 4), contrast=.8, dark=.25, light=.15); grain(img, F, 12, 26)
    fill(img, KIRI_D, 13, poly=R, scale=4, stretch=(.25, 4), contrast=.8, dark=.3); grain(img, R, 13, 8)
    volume(img, (20, 72, 166, 146), .35, .18)
    line(img, [(20, 90), (140, 90), (166, 72)], lt(H(KIRI), .4), 1.4); line(img, [(140, 90), (140, 146)], dk(H(KIRI), .3), .8)
    # the untied cord lies on the floor in loose curls
    cord(img, [(150, 132), (168, 142), (186, 138), (196, 146), (186, 152), (170, 150)], 3.6)
    cord(img, [(146, 138), (156, 150), (138, 154), (120, 152)], 3.6)
    return done(img)


def letters():
    img = I.canvas(180, 116)
    floor_shadow(img, 92, 104, 82, 110)
    cols = ['#e6d6b8', '#efe4cc', '#e2d0ae', '#f2ead8']
    for k, c in enumerate(cols):
        dx, b = (k % 2) * 6 - 3, 98 - k * 8
        Q = [(18 + dx, b), (130 + dx, b), (154 + dx, b - 30), (42 + dx, b - 30)]
        poly(img, [(18 + dx, b), (130 + dx, b), (130 + dx, b + 4), (18 + dx, b + 4)], dk(H(c), .3))
        poly(img, [(130 + dx, b), (154 + dx, b - 30), (154 + dx, b - 26), (130 + dx, b + 4)], dk(H(c), .4))
        fill(img, c, 20 + k, poly=Q, scale=3, contrast=.5, dark=.15, light=.1)
        line(img, [(18 + dx, b), (130 + dx, b)], lt(H(c), .3), .8)
    top = 98 - 3 * 8
    for k in range(5): line(img, [(60 + k * 8, top - 22 + k * .2), (56 + k * 8, top - 8)], '#33261c', 1.1)           # an address in ink
    poly(img, [(112, top - 24), (124, top - 24), (122, top - 10), (110, top - 10)], '#b8322a')                          # a red seal
    for x0, y0, x1, y1 in ((30, top - 15, 146, top - 15), (86, top + 28, 98, top - 30)):
        line(img, [(x0, y0), (x1, y1)], '#7a1a14', 3.6); line(img, [(x0, y0), (x1, y1)], '#c23a2c', 2.6); line(img, [(x0, y0 - .8), (x1, y1 - .8)], '#f0e8e0', .7)
    for sx in (-1, 1):
        b = (92 + sx * 12 - 9, top - 22, 92 + sx * 12 + 9, top - 10)
        fill(img, '#c23a2c', 50 + sx, ell=b, scale=2, contrast=.7); volume(img, b, .6, .4, spec=.1); ell(img, (b[0] + 5, b[1] + 4, b[2] - 5, b[3] - 4), '#6a1610')
    line(img, [(91, top - 14), (84, top + 2)], '#c23a2c', 2.6); line(img, [(93, top - 14), (102, top)], '#c23a2c', 2.6)
    ell(img, (88, top - 19, 96, top - 11), '#9a2a20')
    return done(img)


def shelf():
    img = I.canvas(240, 64)
    soft(img, lambda d: d.rectangle([px(10), px(22), px(230), px(34)], fill=(0, 0, 0, 90)), 4)               # shadow on the wall
    for x in (34, 196):                                                                                         # brackets
        fill(img, '#4a3424', x, poly=[(x, 22), (x + 12, 22), (x + 12, 60), (x, 50)], scale=3, stretch=(.3, 3))
        line(img, [(x + 2, 24), (x + 2, 48)], '#6a4c34', 1)
    fill(img, '#5e4430', 5, rect=(4, 12, 236, 24), scale=4, stretch=(6, .3), contrast=1.2); volume(img, (4, 12, 236, 24), .4, .2)
    poly(img, [(4, 9), (236, 9), (236, 12), (4, 12)], '#8a6a4a')
    return done(img)


if __name__ == '__main__':
    ims = [('box', box_closed()), ('open', box_open()), ('empty', box_open(False)), ('letters', letters()), ('shelf', shelf())]
    W = sum(im.width for _, im in ims[:3]) + 6; x = y = rowh = 0; pos = {}
    for iid, im in sorted(ims, key=lambda t: -t[1].height):
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[iid] = (x, y, im.width, im.height); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for iid, im in ims: at.paste(im, pos[iid][:2])
    at.save(os.path.join(ASSETS, 'items', 'atlas_tc.webp'), 'WEBP', quality=88, alpha_quality=92, method=6)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'out'), exist_ok=True)
    pv = Image.new('RGBA', at.size, (34, 30, 28, 255)); pv.alpha_composite(at); pv = pv.resize((pv.width * 2, pv.height * 2)); pv.convert('RGB').save(os.path.join(os.path.dirname(__file__), 'out', 'atlas_tc.png'))
    print(json.dumps({'size': [W, y + rowh], 'at': {iid: list(pos[iid]) for iid, _ in ims}}, separators=(',', ':')))
