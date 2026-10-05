#!/usr/bin/env python3
"""«Камидана» (feat/kamidana.js, prefix kmd): the household Shinto altar on the kitchen wall — the shelf with a
shinmei-style miniature shrine, a mirror, a shimenawa rope with shide; overlays (sakaki vases fresh/wilted, rice,
salt, water, sake, a candle stand) and 3 collectible things (sakaki pair, Ise ofuda, New Year shimekazari).
All in ONE atlas assets/items/atlas_kmd.webp. Prints the rect map as JSON (pasted into feat/kamidana.js).
Preview → art/out/atlas_kmd.png.   Usage: kamidana_art.py [assets dir]"""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw
ASSETS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'assets')
sys.argv = [sys.argv[0], os.path.join(os.path.dirname(__file__), 'out')]     # items.py reads its out dir from argv[1]
import paint as P
import items as I
from items import px, fill, volume, line, ell, poly, text, soft, floor_shadow, dk, lt, H

HINOKI, HINOKI_D, ROOF, STRAW, GOLD, PORC = '#b39a74', '#8a7352', '#4a3a2e', '#b59a5a', '#c9a24a', '#e8e4da'


def done(img, sat=.9):
    out = img.resize((P.W, P.H), Image.LANCZOS); a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * sat; a[..., :3] += np.random.default_rng(11).normal(0, 2.6, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def rope(img, pts, w=6.0, col=STRAW):
    """twisted straw rope along a polyline: base, dark twist strokes, light top"""
    line(img, pts, dk(H(col), .45), w + 1.2); line(img, pts, col, w)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0); n = max(1, int(L / (w * .8)))
        for k in range(n):
            t = (k + .5) / n; x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            line(img, [(x - w * .32, y - w * .45), (x + w * .32, y + w * .45)], dk(H(col), .38), w * .22)
    line(img, [(x, y - w * .3) for x, y in pts], lt(H(col), .3), w * .22)


def shide(img, x, y, h=40, w=9):
    """zigzag paper streamer hanging from (x,y)"""
    n = 4; seg = h / n; pts = []
    for k in range(n):
        dx = w * .5 if k % 2 == 0 else -w * .5
        pts.append([(x + dx - w * .5, y + k * seg), (x + dx + w * .5, y + k * seg), (x - dx + w * .5, y + (k + 1) * seg), (x - dx - w * .5, y + (k + 1) * seg)])
    for k, q in enumerate(pts):
        poly(img, q, '#ece6d8' if k % 2 == 0 else '#cfc8b8')
        line(img, [q[0], q[1]], '#fbf8f0', .6)


def leaf(img, x, y, ang, L, W, col, light=.25):
    ca, sa = math.cos(ang), math.sin(ang); pts = []
    for k in range(16):
        t = k / 15 * math.pi * 2; u, v = (math.cos(t) * .5 + .5) * L, math.sin(t) * W * .5 * (1 - .35 * (math.cos(t) * .5 + .5))
        pts.append((x + u * ca - v * sa, y + u * sa + v * ca))
    poly(img, pts, col)
    half = [(x + u * ca - v * sa, y + u * sa + v * ca) for u, v in ((L * t, -W * .42 * math.sin(math.pi * t) * (1 - .3 * t)) for t in np.linspace(0, 1, 9))]
    poly(img, half + [(x + L * ca, y + L * sa), (x, y)], lt(H(col), light))
    line(img, [(x, y), (x + L * .9 * ca, y + L * .9 * sa)], dk(H(col), .35), max(.5, W * .07))


def sakaki(img, cx, base, s=1.0, wilt=False, seed=1):
    """a white vase with a sakaki branch: glossy dark-green alternate leaves fanning up (wilted: drooping, yellowed)"""
    r = random.Random(seed)
    # branch stems
    stems = []
    for k, (a, L) in enumerate(((-.32, 70), (-.08, 92), (.2, 78), (.42, 58))):
        a = a * (1.6 if wilt else 1) + (.25 if wilt else 0) * (1 if a > 0 else -1)
        x0, y0 = cx + (k - 1.5) * 1.2 * s, base - 36 * s
        pts = [(x0, y0)]
        for j in range(1, 6):
            t = j / 5; droop = (t * t * 26 * s if wilt else 0)
            pts.append((x0 + math.sin(a) * L * s * t, y0 - math.cos(a) * L * s * t + droop))
        stems.append(pts); line(img, pts, '#5a4632', 1.4 * s)
    green = ['#2f4a2c', '#3a5634', '#2a4228'] if not wilt else ['#6a6a34', '#7a6a38', '#5a5a30']
    for pts in stems:
        for j in range(1, len(pts)):
            x, y = pts[j]; side = 1 if j % 2 else -1
            ang = math.atan2(pts[j][1] - pts[j - 1][1], pts[j][0] - pts[j - 1][0]) + side * (.9 if not wilt else 1.5) + r.uniform(-.15, .15)
            if wilt: ang += .5 * side
            leaf(img, x, y, ang, r.uniform(15, 19) * s, r.uniform(7, 9) * s, r.choice(green), .22 if not wilt else .12)
        x, y = pts[-1]; a = math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0]) + (.6 if wilt else 0)
        leaf(img, x, y, a, 16 * s, 7 * s, green[0] if not wilt else '#7a6232', .25)
    if wilt:   # a fallen leaf by the vase
        leaf(img, cx + 14 * s, base - 4 * s, 2.9, 13 * s, 6 * s, '#8a6a34', .1)
    # the vase (heishi-shaped, white porcelain)
    V = [(cx - 5 * s, base - 40 * s), (cx + 5 * s, base - 40 * s), (cx + 6 * s, base - 34 * s), (cx + 12 * s, base - 22 * s), (cx + 11 * s, base - 4 * s),
         (cx + 8 * s, base), (cx - 8 * s, base), (cx - 11 * s, base - 4 * s), (cx - 12 * s, base - 22 * s), (cx - 6 * s, base - 34 * s)]
    fill(img, PORC, seed + 30, poly=V, scale=3, contrast=.4, dark=.18, light=.1); volume(img, (cx - 12 * s, base - 40 * s, cx + 12 * s, base), .7, .45, spec=.25)
    ell(img, (cx - 5.5 * s, base - 42 * s, cx + 5.5 * s, base - 38 * s), '#d8d2c4'); ell(img, (cx - 3.5 * s, base - 41.5 * s, cx + 3.5 * s, base - 39 * s), '#3a3228')


def shelf():
    img = I.canvas(380, 228)
    soft(img, lambda d: d.rectangle([px(14), px(150), px(366), px(196)], fill=(0, 0, 0, 120)), 7)              # shadow on the wall
    soft(img, lambda d: d.polygon([(px(110), px(160)), (px(120), px(50)), (px(260), px(50)), (px(270), px(160))], fill=(0, 0, 0, 80)), 9)
    for x in (40, 326):                                                                                         # brackets
        B = [(x, 176), (x + 14, 176), (x + 14, 222), (x, 204)]
        fill(img, HINOKI_D, x, poly=B, scale=3, stretch=(.3, 3)); line(img, [(x + 2, 180), (x + 2, 204)], lt(H(HINOKI_D), .2), 1)
    # the board: front face + a sliver of the underside (we look up at it)
    fill(img, HINOKI, 5, rect=(6, 160, 374, 176), scale=4, stretch=(6, .3), contrast=1.1, dark=.3); volume(img, (6, 160, 374, 176), .3, .15)
    poly(img, [(6, 176), (374, 176), (370, 181), (10, 181)], dk(H(HINOKI), .55))
    line(img, [(6, 160), (374, 160)], lt(H(HINOKI), .35), 1.2)
    # the shrine (shinmei style): plinth, body with doors, gable roof, ridge with katsuogi, crossed chigi
    fill(img, HINOKI_D, 7, rect=(118, 150, 262, 160), scale=3, stretch=(5, .4)); line(img, [(118, 150), (262, 150)], lt(H(HINOKI), .3), 1)
    fill(img, HINOKI, 8, rect=(128, 142, 252, 150), scale=3, stretch=(5, .4)); line(img, [(128, 142), (252, 142)], lt(H(HINOKI), .3), 1)
    fill(img, HINOKI, 9, rect=(138, 84, 242, 142), scale=4, stretch=(.3, 5), contrast=.9, dark=.28); volume(img, (138, 84, 242, 142), .35, .2)
    for x in (138, 236):
        fill(img, lt(H(HINOKI), .08), 10 + x, rect=(x, 84, x + 6, 142), scale=3, stretch=(.3, 4))
    fill(img, '#6a5238', 12, rect=(164, 92, 216, 142), scale=3, stretch=(.3, 4), contrast=.8)                     # the doors
    line(img, [(190, 92), (190, 142)], '#2a1e14', 1.2)
    for y in (100, 132):
        for x in (167, 213):
            ell(img, (x - 2.6, y - 2.6, x + 2.6, y + 2.6), GOLD)
    ell(img, (186, 113, 194, 121), GOLD); ell(img, (188, 115, 192, 119), lt(H(GOLD), .4))
    for x in (172, 208):
        line(img, [(x, 142), (x, 160)], HINOKI_D, 2)                                                            # little stair rails
    for k in range(3): line(img, [(174, 146 + k * 5), (206, 146 + k * 5)], lt(H(HINOKI), .2), 1.6)
    # roof: a broad gable seen from the front
    R = [(106, 92), (274, 92), (252, 56), (128, 56)]
    fill(img, ROOF, 14, poly=R, scale=3, stretch=(.4, 3), contrast=1.2, dark=.4, light=.18); volume(img, (106, 56, 274, 92), .4, .25)
    for k in range(9):
        x0 = 128 + k * 15; line(img, [(x0, 57), (x0 - 22 + k * 5.5, 91)], dk(H(ROOF), .35), .8)
    poly(img, [(104, 92), (276, 92), (274, 96), (106, 96)], dk(H(ROOF), .5))
    line(img, [(106, 92), (274, 92)], lt(H(ROOF), .25), 1)
    fill(img, HINOKI_D, 15, rect=(124, 48, 256, 57), scale=3, stretch=(5, .3)); line(img, [(124, 48), (256, 48)], lt(H(HINOKI), .2), 1)
    for x in (150, 172, 190, 208, 230):                                                                         # katsuogi logs
        fill(img, HINOKI, 16 + x, rect=(x - 5, 38, x + 5, 48), scale=2); volume(img, (x - 5, 38, x + 5, 48), .6, .4)
        ell(img, (x - 3, 39, x + 3, 45), GOLD)
    for sx in (-1, 1):                                                                                          # chigi
        x0 = 190 + sx * 66
        line(img, [(x0, 58), (x0 + sx * 14, 18)], HINOKI_D, 5); line(img, [(x0, 58), (x0 + sx * 14, 18)], HINOKI, 3.4)
        line(img, [(x0 + sx * 13, 22), (x0 + sx * 15.5, 15)], GOLD, 2.4)
    # the mirror on its cloud stand
    fill(img, '#6a4a2a', 20, poly=[(180, 160), (200, 160), (196, 138), (184, 138)], scale=2)
    ell(img, (176, 132, 204, 142), '#7a5a34')
    ell(img, (172, 100, 208, 136), dk(H(GOLD), .25)); fill(img, '#b8bcb6', 21, ell=(175, 103, 205, 133), scale=4, contrast=.5)
    volume(img, (175, 103, 205, 133), .6, .3, spec=.7)
    # shimenawa along the front edge of the board, with shide and straw tufts
    pts = [(4 + k * 372 / 12, 171 + 5 * math.sin(math.pi * k / 12) ** 1.2) for k in range(13)]
    for x in (66, 140, 240, 314):
        y = 171 + 5 * math.sin(math.pi * (x - 4) / 372) ** 1.2
        for j in range(5): line(img, [(x - 3 + j * 1.5, y + 2), (x - 4 + j * 2, y + 20)], dk(H(STRAW), .1), .9)
    rope(img, pts, 6.2)
    for x in (103, 190, 277):
        y = 172 + 5 * math.sin(math.pi * (x - 4) / 372) ** 1.2; shide(img, x, y + 2, 38, 9)
    return done(img)


def sakaki_spr(wilt):
    img = I.canvas(84, 134); sakaki(img, 42, 132, 1.0, wilt, 3 if wilt else 2); return done(img)


def dish(img, cx, base, w):
    """a small white sanbo-like dish seen from slightly below"""
    poly(img, [(cx - w * .32, base - 6), (cx + w * .32, base - 6), (cx + w * .26, base), (cx - w * .26, base)], '#cfc9bc')
    fill(img, PORC, 40, poly=[(cx - w * .5, base - 10), (cx + w * .5, base - 10), (cx + w * .42, base - 5), (cx - w * .42, base - 5)], scale=2, contrast=.3)
    line(img, [(cx - w * .5, base - 10), (cx + w * .5, base - 10)], '#fbf8f0', 1)


def rice():
    img = I.canvas(44, 34); dish(img, 22, 33, 40)
    fill(img, '#efeae0', 41, ell=(6, 8, 38, 30), scale=2, contrast=.5); volume(img, (6, 8, 38, 30), .7, .4, spec=.2)
    r = random.Random(4)
    for k in range(40):
        a, rr = r.uniform(math.pi, 2 * math.pi), r.uniform(0, 1) ** .5
        x, y = 22 + math.cos(a) * 14 * rr, 22 + math.sin(a) * 12 * rr
        ell(img, (x - 1.4, y - .8, x + 1.4, y + .8), r.choice(['#fffdf6', '#ddd6c6', '#f6f1e6']))
    return done(img)


def salt():
    img = I.canvas(40, 36); dish(img, 20, 35, 36)
    fill(img, '#f4f2ee', 42, poly=[(20, 5), (32, 26), (8, 26)], scale=2, contrast=.4); volume(img, (8, 5, 32, 26), .8, .3, spec=.3)
    line(img, [(20, 5), (12, 25)], '#ffffff', .8)
    return done(img)


def water():
    img = I.canvas(30, 38); dish(img, 15, 37, 28)
    fill(img, PORC, 43, ell=(4, 10, 26, 30), scale=2, contrast=.4); volume(img, (4, 10, 26, 30), .7, .45, spec=.35)
    fill(img, '#ddd8cc', 44, ell=(7, 7, 23, 13), scale=2); ell(img, (12, 2, 18, 8), '#e6e1d6'); volume(img, (7, 2, 23, 13), .6, .3, spec=.2)
    return done(img)


def sake():
    img = I.canvas(26, 52); dish(img, 13, 51, 24)
    V = [(10, 4), (16, 4), (16, 12), (21, 22), (21, 40), (18, 43), (8, 43), (5, 40), (5, 22), (10, 12)]
    fill(img, PORC, 45, poly=V, scale=2, contrast=.4); volume(img, (5, 4, 21, 43), .7, .45, spec=.3)
    poly(img, [(9, 2), (17, 2), (17, 8), (9, 8)], '#e4dfd2'); line(img, [(9, 8), (17, 8)], '#b8322a', 1.4)
    return done(img)


def candle():
    img = I.canvas(22, 48)
    fill(img, '#5a4a36', 46, poly=[(9, 22), (13, 22), (14, 44), (8, 44)], scale=2)
    ell(img, (3, 42, 19, 47), '#4a3a2a'); ell(img, (4, 18, 18, 24), '#6a5640')
    fill(img, '#efe6d2', 47, rect=(8, 8, 14, 20), scale=2, contrast=.3); volume(img, (8, 8, 14, 20), .6, .3)
    line(img, [(11, 8), (11, 5)], '#2a2018', .9)
    return done(img)


# ── collectible things ──
def item_sakaki():
    img = I.canvas(150, 176); floor_shadow(img, 75, 170, 66)
    sakaki(img, 44, 170, 1.25, False, 5); sakaki(img, 108, 170, 1.25, False, 6)
    return done(img)


def item_ofuda():
    img = I.canvas(110, 214); floor_shadow(img, 55, 208, 50)
    # a little wooden stand (ofuda-tate) with a roof and the wrapped Jingu taima inside
    fill(img, HINOKI_D, 50, rect=(14, 186, 96, 206), scale=3, stretch=(5, .4)); line(img, [(14, 186), (96, 186)], lt(H(HINOKI), .25), 1)
    fill(img, HINOKI, 51, rect=(20, 44, 30, 188), scale=3, stretch=(.3, 5)); fill(img, HINOKI, 52, rect=(80, 44, 90, 188), scale=3, stretch=(.3, 5))
    fill(img, '#f2eee4', 53, rect=(32, 52, 78, 184), scale=3, contrast=.3); volume(img, (32, 52, 78, 184), .4, .2)
    line(img, [(55, 52), (55, 184)], '#d8d0c0', .8)
    for k, ch in enumerate('天照皇大神宮'):
        text(img, ch, 55, 70 + k * 19, 15, '#1d1612', brush=True)
    poly(img, [(48, 172), (62, 172), (62, 182), (48, 182)], '#b8322a')
    line(img, [(30, 62), (80, 62)], '#b8322a', 1.4)
    R = [(4, 50), (106, 50), (90, 26), (20, 26)]
    fill(img, ROOF, 54, poly=R, scale=3, stretch=(.4, 3), contrast=1.1); volume(img, (4, 26, 106, 50), .4, .25)
    poly(img, [(2, 50), (108, 50), (106, 54), (4, 54)], dk(H(ROOF), .5))
    fill(img, HINOKI_D, 55, rect=(18, 20, 92, 27), scale=2)
    for x in (40, 55, 70): fill(img, HINOKI, 56 + x, rect=(x - 4, 12, x + 4, 20), scale=2); ell(img, (x - 2.4, 13, x + 2.4, 18), GOLD)
    return done(img)


def item_shime():
    img = I.canvas(184, 232)
    # urajiro ferns fanning behind the top, yuzuriha leaves
    for sx in (-1, 1):
        for k in range(9):
            t = k / 8; x, y = 92 + sx * (8 + 60 * t), 62 - 26 * math.sin(math.pi * t * .8)
            leaf(img, 92 + sx * 6, 66, (math.pi if sx < 0 else 0) - sx * (.2 + .5 * (1 - t)), 22 + 52 * t * (1 - .3 * t), 12, '#3e5a34', .2)
    for a in (-2.1, -1.05):
        leaf(img, 92, 70, a, 46, 18, '#2f4a2c', .25); leaf(img, 92, 70, -math.pi - a, 46, 18, '#2f4a2c', .25)
    # the straw ring with a twisted loop
    pts = [(92 + 40 * math.cos(a), 108 + 36 * math.sin(a)) for a in np.linspace(-math.pi / 2, 3 * math.pi / 2, 25)]
    rope(img, pts, 10)
    # long straw tails below + shide on both sides
    for k in range(9): line(img, [(80 + k * 3, 140), (76 + k * 3.6, 214 + (k % 3) * 4)], dk(H(STRAW), .08 * (k % 2)), 2.2)
    rope(img, [(70, 140), (114, 140)], 9)
    shide(img, 52, 96, 54, 12); shide(img, 132, 96, 54, 12)
    # red-white mizuhiki band and the daidai orange on top
    fill(img, '#efe9dc', 60, rect=(78, 54, 106, 74), scale=2, contrast=.3); line(img, [(78, 64), (106, 64)], '#b8322a', 2.4)
    fill(img, '#d8742a', 61, ell=(72, 20, 112, 58), scale=3, contrast=.8, dark=.35, light=.2); volume(img, (72, 20, 112, 58), .8, .4, spec=.4)
    leaf(img, 92, 22, -2.3, 18, 9, '#3a5634', .25); ell(img, (89, 18, 95, 24), '#4a3a22')
    return done(img)


if __name__ == '__main__':
    ims = [('shelf', shelf()), ('sk', sakaki_spr(False)), ('skw', sakaki_spr(True)), ('rice', rice()), ('salt', salt()), ('water', water()),
           ('sake', sake()), ('candle', candle()), ('i_sakaki', item_sakaki()), ('i_ofuda', item_ofuda()), ('i_shime', item_shime())]
    W = 380 + 184 + 150 + 6; x = y = rowh = 0; pos = {}
    for iid, im in sorted(ims, key=lambda t: -t[1].height):
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[iid] = (x, y, im.width, im.height); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for iid, im in ims: at.paste(im, pos[iid][:2])
    at.save(os.path.join(ASSETS, 'items', 'atlas_kmd.webp'), 'WEBP', quality=88, alpha_quality=92, method=6)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'out'), exist_ok=True)
    pv = Image.new('RGBA', at.size, (40, 32, 26, 255)); pv.alpha_composite(at); pv = pv.resize((pv.width * 2, pv.height * 2)); pv.convert('RGB').save(os.path.join(os.path.dirname(__file__), 'out', 'atlas_kmd.png'))
    print(json.dumps({'size': [W, y + rowh], 'at': {iid: list(pos[iid]) for iid, _ in ims}}, separators=(',', ':')))
