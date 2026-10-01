#!/usr/bin/env python3
"""«Дарума желаний» (feat/daruma.js): wish daruma in 5 colours — ONE atlas assets/items/atlas_dm.webp:
  big bodies with blank eyes (260×286, the panel face and the runtime item picture),
  small 152×167 thumbnails × 0/1/2 painted eyes (the «🧺 Вещи» tray), three ink dabs for the brush.
Prints the rect map as JSON (pasted into feat/daruma.js). Preview → art/out/atlas_dm.png.
Usage: daruma_art.py [assets dir]"""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
ASSETS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'assets')
sys.argv = [sys.argv[0], os.path.join(os.path.dirname(__file__), 'out')]     # items.py reads its out dir from argv[1]
import paint as P
from paint import mixc, fbm
import items as I
from items import px, fill, volume, text, soft, floor_shadow, dk, lt, H

BW, BH = 260, 286              # big body
SW_, SH_ = 152, 167            # small thumbnail
EYES = {'R': (157, 99, 19), 'L': (103, 99, 19)}     # sockets in big px: R = viewer's right = the daruma's own left eye (painted first)
INK = '#17120f'
COLS = {   # body, gold decor, belly kanji
    'red': ('#b3302a', '#e0b64a', '#e6c05a'),
    'white': ('#e9e2d2', '#c49a3e', '#a8302a'),
    'gold': ('#cf9f3c', '#7a2a1c', '#6a1c14'),
    'black': ('#211e22', '#d6ac50', '#dcb456'),
    'pink': ('#df9aae', '#f0d27a', '#8a2238'),
}


def done(img):
    out = img.resize((P.W, P.H), Image.LANCZOS); a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .9; a[..., :3] += np.random.default_rng(7).normal(0, 3.0, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def body_poly(cx=130, cy=148, rx=110, ry=126, n=90):
    pts = []
    for k in range(n):
        t = k / n * math.tau; s = math.sin(t)
        r = rx * (1 + .1 * s) * (1 - .06 * max(0, -s) ** 2)          # wider hips, a rounder narrower head
        pts.append((cx + r * math.cos(t), min(cy + ry * s, 270)))
    return pts


def taper(img, pts, w0, w1, col, wmid=None):
    """A brush stroke along a polyline: tapered polygon (w0 at start, w1 at the end, wmid in the middle)."""
    wmid = wmid if wmid is not None else (w0 + w1) / 2; L = []; R = []; n = len(pts)
    for i, (x, y) in enumerate(pts):
        a = pts[max(0, i - 1)]; b = pts[min(n - 1, i + 1)]; dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy) or 1
        u = i / (n - 1); w = (w0 + (wmid - w0) * u * 2) if u < .5 else (wmid + (w1 - wmid) * (u - .5) * 2)
        nx, ny = -dy / d * w / 2, dx / d * w / 2; L.append((x + nx, y + ny)); R.append((x - nx, y - ny))
    ImageDraw.Draw(img).polygon([(px(x), px(y)) for x, y in L + R[::-1]], fill=H(col))


def curve(p0, p1, p2, n=14):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in (k / (n - 1) for k in range(n))]


def blot(img, cx, cy, r, seed):
    """A painted pupil: an ink blot with a dry-brush rim, kept inside the socket."""
    rnd = random.Random(seed)
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    for k in range(14):
        a = rnd.uniform(0, math.tau); o = rnd.uniform(0, r * .22); rr = r * rnd.uniform(.5, .66)
        x, y = cx + math.cos(a) * o, cy + math.sin(a) * o; d.ellipse([px(x - rr), px(y - rr), px(x + rr), px(y + rr)], fill=H(INK))
    l = l.filter(ImageFilter.GaussianBlur(.5 * P.SS))
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).ellipse([px(cx - r + 1), px(cy - r + 1), px(cx + r - 1), px(cy + r - 1)], fill=255)
    a = np.asarray(l, np.float32); a[..., 3] *= np.asarray(m, np.float32) / 255
    img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))
    ImageDraw.Draw(img).ellipse([px(cx - r * .32 - 3), px(cy - r * .36 - 3), px(cx - r * .32 + 3), px(cy - r * .36 + 3)], fill=(255, 250, 238, 150))   # wet shine


def daruma(key, eyes):
    body, gold, kan = (H(c) for c in COLS[key]); img = I.canvas(BW, BH)
    floor_shadow(img, 130, 274, 104, 120)
    poly = body_poly()
    fill(img, body, 11 + len(key), poly=poly, scale=7, contrast=.75 if key in ('white', 'pink') else 1.0, dark=.32 if key in ('white', 'pink') else .4, light=.15)
    # gold scrolls on the cheeks of the body (the crane and the turtle, stylised)
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        for k in range(4):
            r = 74 + k * 9; cx = 130 + sx * 4
            a0, a1 = (150, 205) if sx < 0 else (-25, 30)
            d.arc([px(cx - r), px(104 - r * .86), px(cx + r), px(104 + r * .86)], a0 + k * 3, a1 - k * 3, fill=gold, width=px(2.6 - k * .35))
        for k in range(3):   # curls
            x, y = 130 + sx * (96 - k * 4), 150 + k * 16
            d.arc([px(x - 9), px(y - 9), px(x + 9), px(y + 9)], 200 if sx < 0 else -20, 520 if sx < 0 else 300, fill=gold, width=px(2))
    # the face
    fill(img, '#f2ede2', 3, ell=(62, 46, 198, 160), scale=6, contrast=.45, dark=.12, light=.06)
    d = ImageDraw.Draw(img)
    d.ellipse([px(62), px(46), px(198), px(160)], outline=gold, width=px(2.4))
    # eyebrows — two flying cranes: thick tapered strokes with feathered tails
    for sx in (-1, 1):
        ex = 130 + sx * 27
        taper(img, curve((ex - sx * 26, 82), (ex - sx * 2, 58), (ex + sx * 24, 76)), 3, 1.2, INK, wmid=9)
        for k in range(4):
            x0 = ex + sx * (14 + k * 3); taper(img, [(x0, 70 + k * 1.5), (x0 + sx * 12, 66 + k * 4.5)], 2.2, .4, INK)
    # sockets (blank: the eyes are painted by the player)
    for side, (x, y, r) in EYES.items():
        soft(img, lambda dd, x=x, y=y, r=r: dd.ellipse([px(x - r - 2), px(y - r), px(x + r + 2), px(y + r + 3)], fill=(60, 40, 30, 70)), 1.2)
        d = ImageDraw.Draw(img); d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=H('#fbf8f0'), outline=H(INK), width=px(2.2))
    if eyes >= 1: blot(img, *EYES['R'], 101)
    if eyes >= 2: blot(img, *EYES['L'], 202)
    # nose, moustache and the turtle beard
    taper(img, curve((126, 112), (131, 120), (137, 113), 8), 1.5, 1.2, INK, wmid=3)
    for sx in (-1, 1):
        taper(img, curve((130 + sx * 3, 127), (130 + sx * 18, 122), (130 + sx * 34, 132)), 4, .8, INK, wmid=6)
        taper(img, curve((130 + sx * 30, 131), (130 + sx * 40, 136), (130 + sx * 44, 128), 8), 2, .5, INK, wmid=3)
    rnd = random.Random(key)
    for k in range(15):   # beard strokes along the chin
        a = math.pi * (.18 + .64 * k / 14); bx, by = 130 + math.cos(a) * 30, 136 + math.sin(a) * 10
        taper(img, [(bx, by), (bx + math.cos(a) * 16 + rnd.uniform(-2, 2), by + math.sin(a) * 15 + rnd.uniform(0, 3))], 2.6, .5, INK)
    d = ImageDraw.Draw(img); d.arc([px(118), px(130), px(142), px(142)], 20, 160, fill=H('#a8302a'), width=px(2.2))
    # belly: 願 «wish»
    for ox, oy in ((-.7, 0), (.7, 0), (0, .6)): text(img, '願', 130 + ox, 212 + oy, 54, kan, I.SERIF, brush=True)   # a heavier brush
    volume(img, (20, 20, 240, 272), .6, .42, spec=.22)
    return done(img)


def dab(seed, s=64):
    """An ink dab for the runtime brush: round core, ragged dry-brush rim, bristle streaks."""
    yy, xx = np.mgrid[0:s, 0:s] / (s - 1) * 2 - 1; r = np.hypot(xx, yy)
    n = fbm(s, s, 10, 4, seed); st = fbm(s, s, 6, 3, seed + 5, (.25, 4))
    edge = .78 + (n - .5) * .32
    a = np.clip((edge - r) / .12, 0, 1) * (.82 + .18 * st)
    a *= np.where((r > .55) & (st < .35), .55, 1)
    rgb = np.zeros((s, s, 3), np.float32) + np.array(H(INK)[:3], np.float32)
    return Image.fromarray(np.dstack([rgb, a * 255]).astype(np.uint8), 'RGBA')


if __name__ == '__main__':
    keys = list(COLS); R = {'big': {}, 'sm': {}, 'dab': [], 'eye': EYES, 'bw': [BW, BH]}
    big = {}; sm = {}
    for k in keys:
        for e in (0, 1, 2):
            im = daruma(k, e)
            if e == 0: big[k] = im
            sm[k + str(e)] = im.resize((SW_, SH_), Image.LANCZOS)
    AW = len(keys) * (BW + 2) - 2; AH = BH + 2 + 3 * (SH_ + 2) - 2
    atl = Image.new('RGBA', (AW, AH), (0, 0, 0, 0))
    for i, k in enumerate(keys):
        x = i * (BW + 2); atl.alpha_composite(big[k], (x, 0)); R['big'][k] = [x, 0, BW, BH]
        for e in (0, 1, 2):
            sx, sy = i * (SW_ + 2), BH + 2 + e * (SH_ + 2); atl.alpha_composite(sm[k + str(e)], (sx, sy)); R['sm'][k + str(e)] = [sx, sy, SW_, SH_]
    for j in range(3):
        x, y = 5 * (SW_ + 2) + 10 + j * 66, BH + 2; atl.alpha_composite(dab(31 + j * 7), (x, y)); R['dab'].append([x, y, 64, 64])
    os.makedirs(os.path.join(ASSETS, 'items'), exist_ok=True)
    atl.save(os.path.join(ASSETS, 'items', 'atlas_dm.webp'), 'WEBP', quality=88, alpha_quality=90, method=6)
    pv = Image.new('RGBA', atl.size, (52, 46, 40, 255)); pv.alpha_composite(atl); pv.convert('RGB').save(os.path.join(os.path.dirname(__file__), 'out', 'atlas_dm.png'))
    R['size'] = [AW, AH]
    print(json.dumps(R, separators=(',', ':')))
