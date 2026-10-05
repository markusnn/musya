#!/usr/bin/env python3
"""«Ткацкий станок» (feat/loom.js, prefix ht): two files.
1) assets/wear/ht_base.webp — the maps the game needs to sew Musya's own kimono at runtime, LOSSLESS, 3 cells of
   232×216 (the same cell as assets/wear/kimono.webp, frame px 84..316 × 176..392):
     A = (shade, s, t, alpha): shade = luminance of a WHITE kimono painted by art/wear/kimono.py (folds, AO, sheen; /1.3),
         s,t = where the woven pattern is sampled (the same unwrapped coords kimono.py uses: asin(u)·R on the torso,
         own cylinders on the sleeves); s stored as (s+16)·255/352, t as is
     B = (cloth, obi, cord, 255)   C = (obiage, eri collar, fuki hem lining, 255)  — soft region masks
   Masks come from re-painting the same kimono with one part red and diffing; s,t are captured by swapping
   kimono.sample for a recorder.
2) assets/items/atlas_ht.webp — the painted taka-bata (wooden floor loom) for the kura, 300×360.
Usage: loom_art.py [assets dir]   (previews → art/out/ht_*.png)"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'assets')
OUTP = os.path.join(HERE, 'out'); os.makedirs(OUTP, exist_ok=True)
sys.argv = [sys.argv[0], OUTP]                      # items.py / kimono.py read their out dir from argv[1]
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'wear'))
import paint as P
import items as I
from items import px, fill, volume, line, ell, poly, soft, floor_shadow, dk, lt, H
import kimono as K

# ── 1. kimono maps ──
CAP = []
def rec_sample(mode):
    """replacement for kimono.sample: records (s,t); returns transparent or opaque red for call #mode"""
    n = [0]
    def f(tex, s, t):
        CAP.append((s.copy(), t.copy())); n[0] += 1; out = np.zeros(s.shape + (4,), np.float32)
        if n[0] == mode: out[..., 0] = 1; out[..., 3] = 1
        return out
    return f


def paint_variant(base='#ffffff', obi='#ffffff', cord='#ffffff', obiage='#ffffff', fuki='#ffffff', mode=0):
    K.sample = rec_sample(mode)
    row = ('ht_base', '', base, obi, cord, (lambda d: None), obiage, fuki, 1)
    _, _, img = K.kimono(row, YS, EL, ER)
    return np.asarray(img, np.float32) / 255


def mask(Wi, V):
    g = Wi[..., 1]; r = np.where(g > .02, (g - V[..., 1]) / np.maximum(g, 1e-3), 0)
    return np.clip((r - .12) / .55, 0, 1) * (Wi[..., 3] > .02)


def down2(a):
    h, w = a.shape; return a.reshape(h // 2, 2, w // 2, 2).mean((1, 3))


def kimono_maps():
    global YS, EL, ER
    YS, EL, ER = K.body_edges()
    CAP.clear(); Wi = paint_variant(); (s_t, t_t), (s_s, t_s) = CAP[0], CAP[1]
    T = mask(Wi, paint_variant(mode=1)); SV = mask(Wi, paint_variant(mode=2))
    OB = mask(Wi, paint_variant(obi='#ff0000')); CO = mask(Wi, paint_variant(cord='#ff0000'))
    OA = mask(Wi, paint_variant(obiage='#ff0000')); FK = mask(Wi, paint_variant(fuki='#ff0000'))
    BA = mask(Wi, paint_variant(base='#ff0000')); ER_ = np.clip(BA - T - SV - FK, 0, 1)
    cloth = np.clip(T + SV, 0, 1)
    s_t, t_t, s_s, t_s = (down2(np.asarray(a, np.float32)) for a in (s_t, t_t, s_s, t_s))
    s = np.where(SV > T, s_s, s_t); t = np.where(SV > T, t_s, t_t)
    lum = (Wi[..., :3] * [.3, .59, .11]).sum(-1)
    A = np.dstack([np.clip(lum / 1.3, 0, 1) * 255, np.clip((s + 16) * 255 / 352, 0, 255), np.clip(t, 0, 255), Wi[..., 3] * 255])
    one = np.full(lum.shape, 255.)
    B = np.dstack([cloth * 255, OB * 255, CO * 255, one]); C = np.dstack([OA * 255, ER_ * 255, FK * 255, one])
    out = np.concatenate([A, B, C], 1)
    im = Image.fromarray(np.round(out).astype(np.uint8), 'RGBA')
    im.save(f'{ASSETS}/wear/ht_base.webp', 'WEBP', lossless=True, exact=True, method=6)
    im.save(f'{OUTP}/ht_base.png')
    # preview: indigo cloth with white waves-ish stripes, ochre obi — the runtime formula
    al = cloth[..., None] * np.where(((s // 12 + t // 12) % 2 == 0)[..., None], H('#2a3a6a')[:3], H('#e8e0cc')[:3]) / 255
    al = al + OB[..., None] * np.array(H('#c09030')[:3]) / 255 + CO[..., None] * np.array(H('#b8322a')[:3]) / 255
    al = al + OA[..., None] * np.array(H('#e8b8c0')[:3]) / 255 + ER_[..., None] * np.array(H('#2a3a6a')[:3]) / 255 * 1.1 + FK[..., None] * np.array(H('#e8e0cc')[:3]) / 255 * .85
    rest = np.clip(1 - cloth - OB - CO - OA - ER_ - FK, 0, 1)[..., None] * .96
    pv = np.clip((al + rest) * (lum * 1.0)[..., None], 0, 1)
    Image.fromarray(np.dstack([pv * 255, Wi[..., 3] * 255]).astype(np.uint8), 'RGBA').resize((464, 432)).save(f'{OUTP}/ht_preview.png')
    print('ht_base', im.size, os.path.getsize(f'{ASSETS}/wear/ht_base.webp'))


# ── 2. the loom ──
WOOD, WD, WL = '#6e4c30', '#2e1c10', '#9a7450'
def beam(img, p0, p1, w, seed, col=WOOD):
    """a squared wooden bar from p0 to p1 with a lit top edge"""
    w *= 1.35; (x0, y0), (x1, y1) = p0, p1; L = math.hypot(x1 - x0, y1 - y0); nx, ny = -(y1 - y0) / L * w / 2, (x1 - x0) / L * w / 2
    pts = [(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)]
    poly(img, [(x + (1 if x > (x0 + x1) / 2 else -1) * .8, y + (1 if y > (y0 + y1) / 2 else -1) * .8) for x, y in pts], dk(H(col), .7))   # dark rim
    fill(img, col, seed, poly=pts, scale=3, stretch=(1, 5) if abs(y1 - y0) > abs(x1 - x0) else (5, 1), contrast=1.1)
    hi = (-nx * .7, -ny * .7) if ny > 0 else (nx * .7, ny * .7)
    line(img, [(x0 + hi[0], y0 + hi[1]), (x1 + hi[0], y1 + hi[1])], lt(H(col), .22), max(.8, w * .16))
    line(img, [(x0 - hi[0], y0 - hi[1]), (x1 - hi[0], y1 - hi[1])], dk(H(col), .45), max(.8, w * .14))


def loom():
    img = I.canvas(300, 360); B = 345                         # B: floor line of the front posts
    floor_shadow(img, 150, B + 2, 150, 120)
    D = (40, -30)                                              # depth offset front → back
    bk = lambda x, y: (x + D[0], y + D[1])
    # treadles on the floor (back layer)
    for x in (120, 150):
        beam(img, (x, B - 4), bk(x - 6, B - 4), 7, 11 + x, '#4a321e')
    # back posts, back rail, warp beam with wound thread
    for x in (52, 238): beam(img, bk(x, B), bk(x, 46), 13, 3 + x)
    beam(img, bk(46, 52), bk(244, 52), 12, 21)
    beam(img, bk(52, B - 14), bk(238, B - 14), 10, 22)
    wb = bk(145, 118)
    fill(img, '#d9ccb0', 31, ell=(wb[0] - 92, wb[1] - 13, wb[0] + 92, wb[1] + 13), scale=2, stretch=(1, 6))
    fill(img, '#d9ccb0', 32, rect=(wb[0] - 92, wb[1] - 13, wb[0] + 92, wb[1] + 13), scale=2, stretch=(1, 6), contrast=.7)
    volume(img, (wb[0] - 92, wb[1] - 14, wb[0] + 92, wb[1] + 14), k=.6, rim=.5)
    for x in range(-88, 90, 4): line(img, [(wb[0] + x, wb[1] - 13), (wb[0] + x + 1, wb[1] + 13)], (150, 136, 112, 90), .6)
    # heddle pulleys and cords from the top rail
    for x in (100, 196):
        q = bk(x, 52); ell(img, (q[0] - 7, q[1] + 2, q[0] + 7, q[1] + 16), '#3a2616'); line(img, [(q[0], q[1] + 16), (x + 20, 148)], (40, 30, 20, 220), 1.1)
    # warp threads: from the warp beam down to the reed, then the woven cloth to the breast beam
    for i in range(46):
        u = i / 45; xa = wb[0] - 86 + u * 172; xb = 74 + u * 150
        line(img, [(xa, wb[1] + 10), (xb + 6, 182)], (232, 222, 196, 150 if i % 2 else 110), .7)
    # heddle frames (two, slightly apart) and the hanging beater with the reed
    for k, y in enumerate((150, 162)):
        beam(img, (78 + k * 4, y), (236 + k * 4, y), 4, 40 + k, '#3e2a1a')
    for x in range(80, 236, 3): line(img, [(x, 150), (x + 3, 166)], (60, 44, 30, 110), .5)
    beam(img, (62, 172), (240, 172), 7, 51, '#5a3c24'); beam(img, (62, 200), (240, 200), 8, 52)
    for x in range(66, 238, 3): line(img, [(x, 175), (x, 197)], (40, 30, 22, 120), .6)
    beam(img, (64, 120), (64, 204), 6, 53); beam(img, (238, 120), (238, 204), 6, 54)
    # woven indigo kasuri cloth from the reed to the breast beam
    fill(img, '#26365e', 61, poly=[(70, 204), (236, 204), (232, 236), (66, 236)], scale=2, stretch=(4, 1), contrast=.8)
    rr = np.random.default_rng(5)
    for _ in range(26):
        x, y = rr.uniform(74, 226), rr.uniform(208, 232); line(img, [(x - 4, y), (x + 4, y)], (220, 214, 196, 170), 1.2)
    for y in range(206, 236, 2): line(img, [(68, y), (234, y)], (10, 16, 34, 40), .4)
    # front posts, side rails (front → back), breast beam with the cloth roll, the bench
    for x in (40, 228):
        beam(img, (x, B), (x, 200), 15, 70 + x); beam(img, (x, 214), bk(x + 12, 120), 9, 80 + x); beam(img, (x, B - 10), bk(x + 12, B - 10), 9, 90 + x)
    beam(img, (34, 238), (234, 238), 13, 95)
    fill(img, '#1e2a4a', 96, ell=(64, 246, 236, 266), scale=2, stretch=(6, 1)); fill(img, '#1e2a4a', 97, rect=(64, 246, 236, 262), scale=2, stretch=(6, 1))
    volume(img, (60, 244, 240, 268), k=.6, rim=.45)
    beam(img, (90, 296), (238, 296), 12, 99, '#7a5638')
    for x in (100, 226): beam(img, (x, 302), (x, B + 2), 9, 101 + x, '#5a3c24')
    # the shuttle (hi) resting on the breast beam
    fill(img, '#8a5a2e', 120, poly=[(118, 226), (136, 221), (178, 221), (196, 226), (178, 231), (136, 231)], scale=2, stretch=(5, 1))
    volume(img, (118, 220, 196, 232), k=.7, rim=.3, spec=.3); line(img, [(150, 226), (166, 226)], '#e8dcc0', 1.4)
    I.save  # noqa (style reference only)
    out = img.resize((P.W, P.H), Image.LANCZOS); a = np.asarray(out, np.float32)
    l = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True); a[..., :3] = l + (a[..., :3] - l) * .88
    a[..., :3] += np.random.default_rng(7).normal(0, 3, a.shape[:2])[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')
    im.save(f'{ASSETS}/items/atlas_ht.webp', 'WEBP', quality=88, alpha_quality=92, method=6); im.save(f'{OUTP}/ht_loom.png')
    print('atlas_ht', im.size, os.path.getsize(f'{ASSETS}/items/atlas_ht.webp'))


if __name__ == '__main__':
    what = os.environ.get('HT', 'all')
    if what in ('all', 'kimono'): kimono_maps()
    if what in ('all', 'loom'): loom()
