#!/usr/bin/env python3
"""«Фонарь на перевале» (feat/serial.js): three keepsakes from the fox's serial kaidan, category «Сказки лисы»,
packed into ONE atlas assets/items/atlas_sr.webp: the lantern «Домой» (家), the camellia leaf with a coin hole,
the hairpin with a little bell. Prints the rect map as JSON (pasted into feat/serial.js). Preview → art/out/atlas_sr.png.
Usage: serial_art.py [assets dir]"""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw
ASSETS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'assets')
sys.argv = [sys.argv[0], os.path.join(os.path.dirname(__file__), 'out')]     # items.py reads its out dir from argv[1]
import paint as P
from paint import hexc
import items as I
from items import px, fill, volume, line, ell, poly, text, soft, floor_shadow, H

CAP = {}


def done(img, seed=7):
    out = img.resize((P.W, P.H), Image.LANCZOS); a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .88; a[..., :3] += np.random.default_rng(seed).normal(0, 3.2, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def cap(img, iid, *a, **k): CAP[iid] = done(img)
I.save = cap


def lantern():
    """A travel lantern (bura-chōchin) on a short pole hook, warm paper, the sign 家 «дом»."""
    I.chochin('sr_chochin', '', '#e9c47e', '家', tall=True, ink='#2a0e08')
    im = CAP['sr_chochin']
    a = np.asarray(im, np.float32); h, w = a.shape[:2]                     # inner glow: the paper is lit from inside
    yy, xx = np.mgrid[0:h, 0:w]; g = np.exp(-(((xx - w / 2) / (w * .34)) ** 2 + ((yy - h * .55) / (h * .3)) ** 2))
    a[..., 0] += 38 * g * (a[..., 3] > 0); a[..., 1] += 22 * g * (a[..., 3] > 0)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def leaf():
    """A glossy camellia leaf lying on the floor, a square hole in the middle like a copper mon."""
    W, Hh = 170, 92; img = I.canvas(W, Hh); cx, cy = 86, 50
    floor_shadow(img, cx, 74, 72, 90)
    pts = []
    for k in range(60):
        t = k / 59 * math.pi * 2; c, s = math.cos(t), math.sin(t)
        r = 1 - .18 * max(0, c) ** 6                                          # a slightly drawn-out tip on the right
        x = cx + 74 * c * (1 + .14 * max(0, c) ** 3); y = cy + 30 * s * r * (1 - .25 * c)
        pts.append((x, y))
    rot = -.12; pts = [(cx + (x - cx) * math.cos(rot) - (y - cy) * math.sin(rot), cy + (x - cx) * math.sin(rot) + (y - cy) * math.cos(rot)) for x, y in pts]
    fill(img, '#2e4a2c', 31, poly=pts, scale=4, contrast=1.15, dark=.5, light=.28)
    volume(img, (12, 18, 160, 82), .7, .4, spec=.35)
    line(img, [(18, 58), (60, 52), (110, 44), (156, 36)], '#7d9a5a', 2.2)       # midrib
    for t in (.2, .38, .56, .74):
        x0, y0 = 18 + 138 * t, 58 - 22 * t
        for s in (-1, 1): line(img, [(x0, y0), (x0 + 16, y0 + s * 15 - 3)], '#4f6e40', 1.1)
    line(img, [(18, 58), (6, 62)], '#5a4a2a', 3)                                  # stalk
    a = np.asarray(img, np.float32); q = 10                                         # the coin hole, with a dark rim
    x0, y0 = px(cx - q), px(cy - 4 - q); x1, y1 = px(cx + q), px(cy - 4 + q)
    a[y0 - px(2):y1 + px(2), x0 - px(2):x1 + px(2), :3] *= .45
    a[y0:y1, x0:x1, 3] = 0
    img = Image.fromarray(a.astype(np.uint8), 'RGBA')
    for k in range(3):                                                             # raindrops
        dx, dy = [(52, 40), (120, 58), (100, 30)][k]
        ell(img, (dx - 3, dy - 2, dx + 3, dy + 3), (200, 225, 210, 150)); ell(img, (dx - 1.5, dy - 1.5, dx, dy), (255, 255, 255, 220))
    return done(img, 13)


def kanzashi():
    """A silver hairpin with a little bell on a red cord, stuck into a small lacquered stand."""
    W, Hh = 120, 210; img = I.canvas(W, Hh); cx = 60
    floor_shadow(img, cx, 200, 46, 120)
    fill(img, '#1c1210', 5, poly=[(22, 196), (98, 196), (92, 172), (28, 172)], scale=3, contrast=1.1, dark=.4, light=.3)   # lacquer stand
    poly(img, [(28, 172), (92, 172), (88, 166), (32, 166)], '#3a2418'); line(img, [(30, 184), (90, 184)], '#a8322a', 2)
    for s in (-1, 1): line(img, [(cx + s * 3.5, 168), (cx + s * 4.5, 56)], '#b9b6ae', 2.6)      # two prongs
    line(img, [(cx - 3, 166), (cx - 4, 60)], '#e8e6df', .8)
    fan = [(cx + 32 * math.cos(t), 54 + 32 * math.sin(t)) for t in np.linspace(math.pi, 2 * math.pi, 24)]
    fill(img, '#c9c6bd', 9, poly=fan, scale=2, contrast=1.2, dark=.35, light=.4)               # the round fan plate
    d = ImageDraw.Draw(img)
    for k in range(11):                                                                        # bira: thin strips hanging under it
        x = cx - 28 + k * 5.6; L = 22 + 6 * math.cos((k - 5) / 5 * 1.4)
        d.line([(px(x), px(54)), (px(x + (k - 5) * .4), px(54 + L))], fill=hexc('#dcdad2'), width=px(1.1))
        d.ellipse([px(x - 1.6), px(54 + L - 1), px(x + 1.6), px(54 + L + 2.2)], fill=hexc('#e8e4da'))
    line(img, [(cx - 30, 54), (cx + 30, 54)], '#8a8478', 1.6)
    text(img, '鈴', cx, 38, 15, '#4a4038', I.SERIF)
    volume(img, (26, 20, 94, 56), .6, .3, spec=.5)
    line(img, [(cx + 28, 46), (cx + 38, 72), (cx + 32, 96)], '#b8322a', 2.4)                   # red cord and the bell
    ell(img, (cx + 20, 94, cx + 40, 114), '#c8c3b6'); volume(img, (cx + 20, 94, cx + 40, 114), .8, .5, spec=.6)
    line(img, [(cx + 22, 107), (cx + 38, 107)], '#4a4038', 1.4); ell(img, (cx + 28, 108, cx + 32, 112), '#2a2420')
    return done(img, 17)


if __name__ == '__main__':
    ims = [('sr_chochin', lantern(), 't'), ('sr_leaf', leaf(), 'b'), ('sr_kanzashi', kanzashi(), 'b')]
    W = sum(im.width for _, im, _ in ims) + 2 * len(ims); x = 0; pos = {}
    for iid, im, _ in ims: pos[iid] = (x, 0, im.width, im.height); x += im.width + 2
    at = Image.new('RGBA', (W, max(im.height for _, im, _ in ims)), (0, 0, 0, 0))
    for iid, im, _ in ims: at.paste(im, pos[iid][:2])
    at.save(os.path.join(ASSETS, 'items', 'atlas_sr.webp'), 'WEBP', quality=88, alpha_quality=92, method=6)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'out'), exist_ok=True)
    pv = Image.new('RGBA', at.size, (34, 30, 28, 255)); pv.alpha_composite(at); pv.convert('RGB').resize((at.width * 2, at.height * 2)).save(os.path.join(os.path.dirname(__file__), 'out', 'atlas_sr.png'))
    print(json.dumps({'size': list(at.size), 'at': {iid: list(pos[iid]) + [a] for iid, _, a in ims}}))
