#!/usr/bin/env python3
"""«Музыка дома» (feat/music.js, prefix og): a wind-up gramophone with a brass morning-glory horn, a walnut box,
a black shellac record with a red label — ONE picture in the atlas assets/items/atlas_og.webp.
Prints the rect map as JSON (pasted into feat/music.js). Preview → art/out/atlas_og.png.
Usage: music_art.py [assets dir]"""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw
ASSETS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'assets')
sys.argv = [sys.argv[0], os.path.join(os.path.dirname(__file__), 'out')]     # items.py reads its out dir from argv[1]
import paint as P
import items as I
from items import px, fill, volume, line, ell, poly, soft, floor_shadow, dk, lt, H

WAL, WAL_D, BRASS, BRASS_D, BRASS_L = '#6a4630', '#4a2f20', '#c29a48', '#7a5a26', '#ecd28a'


def done(img):
    out = img.resize((P.W, P.H), Image.LANCZOS); a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .9; a[..., :3] += np.random.default_rng(5).normal(0, 3, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def hull(pts):
    pts = sorted(set(pts)); lo, up = [], []
    cr = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def elp(cx, cy, rx, ry, rot, n=72):
    c, s = math.cos(rot), math.sin(rot)
    return [(round(cx + rx * math.cos(t) * c - ry * math.sin(t) * s, 2), round(cy + rx * math.cos(t) * s + ry * math.sin(t) * c, 2)) for t in (2 * math.pi * k / n for k in range(n))]


def gramophone():
    img = I.canvas(210, 250)
    floor_shadow(img, 104, 236, 92, 120)
    # walnut box: front, right side, top
    F, R, T = [(22, 172), (150, 172), (150, 232), (22, 232)], [(150, 172), (182, 154), (182, 212), (150, 232)], [(22, 172), (54, 154), (182, 154), (150, 172)]
    fill(img, WAL, 1, poly=F, scale=4, stretch=(4, .3), contrast=.9, dark=.3, light=.12)
    fill(img, WAL_D, 2, poly=R, scale=4, stretch=(4, .3), contrast=.9, dark=.3)
    fill(img, I.lt(H(WAL), .1), 3, poly=T, scale=4, stretch=(4, .3), contrast=.7, dark=.2, light=.1)
    volume(img, (22, 154, 182, 232), .35, .2)
    poly(img, [(34, 182), (138, 182), (138, 222), (34, 222)], dk(H(WAL), .25))          # inset panel
    line(img, [(34, 182), (138, 182)], dk(H(WAL), .55), 1); line(img, [(34, 222), (138, 222)], lt(H(WAL), .2), .8)
    for x, y in ((22, 232), (150, 232), (182, 212)): ell(img, (x - 5, y - 3, x + 5, y + 5), BRASS_D); ell(img, (x - 4, y - 3, x + 3, y + 2), BRASS)   # feet
    line(img, [(22, 172), (150, 172), (182, 154)], BRASS, 1.6); line(img, [(22, 171), (150, 171)], BRASS_L, .6)                                     # brass trim
    ell(img, (80, 196, 92, 208), BRASS_D); ell(img, (81, 197, 90, 206), BRASS)                                                                         # badge
    # crank handle on the side
    line(img, [(170, 188), (196, 182)], dk(H(BRASS), .3), 3); line(img, [(196, 182), (198, 198)], dk(H(BRASS), .3), 3)
    ell(img, (193, 194, 205, 206), '#2a1c14'); ell(img, (195, 195, 201, 200), '#5a4030')
    # turntable + record on the top face
    ell(img, (52, 152, 148, 172), '#1c1612'); ell(img, (55, 153, 145, 169), '#0e0b0a')
    for k in range(5): ImageDraw.Draw(img).ellipse([px(60 + k * 6), px(155 + k * 1.1), px(140 - k * 6), px(167 - k * 1.1)], outline=(60, 54, 50, 90), width=max(1, px(.5)))
    soft(img, lambda d: d.ellipse([px(70), px(155), px(96), px(160)], fill=(200, 190, 170, 70)), .8)                                                  # sheen
    ell(img, (90, 158, 110, 164), '#9a2a22'); ell(img, (98, 160, 102, 162), '#e8d7a0')
    # tone arm: from the back-right pillar to the needle, and the pipe up into the horn
    ell(img, (156, 150, 168, 158), BRASS_D)
    line(img, [(162, 154), (162, 140)], BRASS_D, 4); line(img, [(161, 154), (161, 141)], BRASS_L, 1)
    line(img, [(162, 146), (134, 158), (126, 162)], BRASS_D, 3); line(img, [(162, 145), (134, 157)], BRASS, 1.4)
    ell(img, (120, 158, 130, 166), '#2a2018')
    # the horn: a brass cone from the neck above the arm to a big flared mouth turned up-left
    cx, cy, rx, ry, rot = 74, 66, 60, 50, -.35
    rim = elp(cx, cy, rx, ry, rot); neck = elp(160, 136, 6, 6, 0, 16)
    H0 = hull(rim + neck)
    fill(img, BRASS, 7, poly=H0, scale=5, stretch=(1.5, .6), contrast=.8, dark=.4, light=.25)
    volume(img, (10, 10, 168, 144), .55, .35, spec=.18)
    for k in range(10):                                                                         # panel seams on the outside
        t = 2 * math.pi * k / 10 + .2; a = (cx + rx * math.cos(t) * math.cos(rot) - ry * math.sin(t) * math.sin(rot), cy + rx * math.cos(t) * math.sin(rot) + ry * math.sin(t) * math.cos(rot))
        if a[0] + a[1] > cx + cy + 10: line(img, [a, (160, 136)], dk(H(BRASS), .38), .8)
    # mouth: dark throat with lit inner panels
    m = I.mask_poly(img, poly=rim)
    fill(img, '#8a6a30', 8, mask=m, scale=4, contrast=.6, dark=.35, light=.2)
    tx, ty = 104, 90                                                                             # the throat (towards the neck)
    soft(img, lambda d: d.ellipse([px(tx - 26), px(ty - 22), px(tx + 18), px(ty + 16)], fill=(26, 18, 8, 230)), 9)
    soft(img, lambda d: d.ellipse([px(tx - 9), px(ty - 8), px(tx + 6), px(ty + 6)], fill=(8, 5, 2, 255)), 3)
    z = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(z)
    for k in range(12):
        t = 2 * math.pi * k / 12; a = (cx + rx * math.cos(t) * math.cos(rot) - ry * math.sin(t) * math.sin(rot), cy + rx * math.cos(t) * math.sin(rot) + ry * math.sin(t) * math.cos(rot))
        d.line([(px(a[0]), px(a[1])), (px(tx), px(ty))], fill=(40, 26, 10, 120), width=max(1, px(1)))
        b = (a[0] * .8 + tx * .2 - 3, a[1] * .8 + ty * .2 - 3)
        d.line([(px(a[0] - 3), px(a[1] - 3)), (px(b[0]), px(b[1]))], fill=(236, 210, 140, 60), width=max(1, px(2.4)))
    w = Image.new('RGBA', img.size, (0, 0, 0, 0)); w.paste(z, (0, 0), m); img.alpha_composite(w)
    pts = rim + rim[:1]
    line(img, pts, dk(H(BRASS), .45), 3.2); line(img, [(x - .6, y - .9) for x, y in pts[38:72]], BRASS_L, 1.3)              # rolled rim
    line(img, [(x - .6, y - .9) for x, y in pts[0:12]], BRASS_L, 1.3)
    # collar where the horn meets the arm pipe
    ell(img, (152, 128, 168, 144), BRASS_D); ell(img, (154, 129, 164, 139), BRASS)
    return done(img)


if __name__ == '__main__':
    g = gramophone(); W, Hh = g.width, g.height
    at = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); at.paste(g, (0, 0))
    at.save(os.path.join(ASSETS, 'items', 'atlas_og.webp'), 'WEBP', quality=88, alpha_quality=92, method=6)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'out'), exist_ok=True)
    pv = Image.new('RGBA', at.size, (34, 30, 28, 255)); pv.alpha_composite(at); pv = pv.resize((pv.width * 2, pv.height * 2)); pv.convert('RGB').save(os.path.join(os.path.dirname(__file__), 'out', 'atlas_og.png'))
    print(json.dumps({'size': [W, Hh], 'at': {'gramo': [0, 0, W, Hh]}}, separators=(',', ':')))
