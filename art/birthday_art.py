#!/usr/bin/env python3
"""«День рождения Муси»: festive decor for the engawa (paper pennant garland, bonbori floor lamp, a blank kōhaku banner —
the text is drawn live), 6 milestone things («Праздники Муси») and 2 party dishes (strawberry shortcake, sekihan).
Same spline toolkit as story_art.py / candles_art.py.
Usage: python3 art/birthday_art.py  → assets/items/atlas_bd.webp (+ art/out/birthday_preview.png); prints the rect map."""
import json, math, os, random, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.argv = [sys.argv[0], os.path.join(ROOT, 'assets/mon')]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc
from monsters import canvas, px, soft
from story_art import cr, shape, clipped, poly_s
from items import text, SERIF, SANS

PREV = os.path.join(ROOT, 'art/out'); os.makedirs(PREV, exist_ok=True)
W_, BLK = (255, 255, 255, 255), (0, 0, 0, 255)
RED, CREAM, GOLD, INDIGO, PINK, LAC = hexc('#b8322a'), hexc('#efe3c8'), hexc('#d8b048'), hexc('#2c3e66'), hexc('#e6a2b4'), (26, 18, 16, 255)


def finish(img, seed):
    out = img.resize((P.W, P.H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(.5))
    a = np.asarray(out, np.float32); n = np.random.default_rng(seed).normal(0, 4.5, a.shape[:2])[..., None]
    a[..., :3] = np.clip(a[..., :3] + n, 0, 255); return Image.fromarray(a.astype(np.uint8), 'RGBA')


def stroke(d, pts, col, w, n=8):
    d.line([(px(x), px(y)) for x, y in cr(pts, n, False)], fill=col, width=max(1, px(w)), joint='curve')


def shadow(img, cx, y, rx, a=90):
    soft(img, lambda d: d.ellipse([px(cx - rx), px(y - rx * .16), px(cx + rx), px(y + rx * .16)], fill=(0, 0, 0, a)), 3)


def strawberry(img, x, y, r, seed):
    shape(img, hexc('#c42a2e'), seed, [(x - r, y - r * .3), (x, y - r * .62), (x + r, y - r * .3), (x + r * .5, y + r * .6), (x, y + r), (x - r * .5, y + r * .6)], scale=3, k=.7, rim=.3, spec=.35, feather=.4)
    d = ImageDraw.Draw(img)
    for i in range(7):
        a = i * 2.4; sx, sy = x + math.cos(a) * r * .45, y + math.sin(a) * r * .38 + r * .1
        d.ellipse([px(sx - .9), px(sy - 1.3), px(sx + .9), px(sy + 1.3)], fill=(240, 210, 120, 230))
    for a in (-.9, -.3, .3, .9):
        poly_s(d, [(x, y - r * .55), (x + math.sin(a) * r * .75, y - r * .55 - math.cos(a) * r * .28), (x + math.sin(a) * r * .3, y - r * .45)], (70, 120, 56, 255), 4)


# ───────────── decor ─────────────
def garland():   # one swag of washi pennants on a red-white cord; repeated between hang points along the eaves
    img = canvas(440, 120)
    cord = lambda u: (6 + u * 428, 10 + 40 * math.sin(u * math.pi))
    d = ImageDraw.Draw(img)
    stroke(d, [cord(u / 10) for u in range(11)], (196, 60, 52, 255), 2.4, 4)
    stroke(d, [(x + 1, y + 1.6) for x, y in (cord(u / 10) for u in range(11))], (236, 226, 206, 230), 1.2, 4)
    cols = [RED, CREAM, GOLD, INDIGO, PINK, RED, CREAM, GOLD, INDIGO]
    for i, col in enumerate(cols):
        u = (i + .5) / len(cols); x, y = cord(u); w = 19; L = 44 + 6 * math.sin(i * 1.7)
        m = shape(img, col, 40 + i, [(x - w, y), (x + w, y), (x + 1, y + L)], scale=3, contrast=.6, dk=.35, lt=.2, k=.6, rim=.25, smooth=False, feather=.35)
        mk = ['寿', '祝', '福', '', '✿', '寿', '祝', '福', ''][i]
        if mk and mk != '✿': text(img, mk, x, y + 13, 13, (250, 238, 214) if col in (RED, INDIGO) else (150, 40, 32), font=SANS)
        if mk == '✿': text(img, '✿', x, y + 13, 14, (250, 240, 230), font=SANS)
        ImageDraw.Draw(img).line([(px(x - w), px(y + .6)), (px(x + w), px(y + .6))], fill=mixc(col, BLK, .45), width=px(1.6))
    for x in (8, 432):   # small paper tassels at the hang points
        for k in (-3, 0, 3): stroke(ImageDraw.Draw(img), [(x, 10), (x + k, 30), (x + k * 1.4, 44)], (226, 196, 120, 230), 1.4, 3)
        shape(img, GOLD, 90 + x, ell=(x - 5, 4, x + 5, 15), scale=2, k=.6, rim=.3, spec=.3, feather=.3)
    return finish(img, 11)


def bonbori(img=None):   # paper floor lamp on a black lacquer stand (lit)
    img = canvas(100, 230)
    shadow(img, 50, 224, 40, 110)
    shape(img, LAC, 201, [(14, 214), (86, 214), (80, 226), (20, 226)], scale=4, k=.5, rim=.2, spec=.2, smooth=False, feather=.3)
    shape(img, LAC, 202, [(46, 112), (54, 112), (56, 216), (44, 216)], scale=4, k=.6, rim=.25, spec=.25, smooth=False, feather=.3)
    for y in (150, 186): shape(img, hexc('#3a2a20'), 203 + y, ell=(41, y - 4, 59, y + 4), scale=3, k=.6, rim=.3, spec=.2)
    # the shade: warm paper glowing from inside, darker red bands top and bottom
    soft(img, lambda d: d.ellipse([px(4), px(4), px(96), px(130)], fill=(255, 170, 80, 80)), 10)
    m = shape(img, hexc('#f4d39a'), 205, [(18, 20), (82, 20), (90, 46), (90, 92), (82, 116), (18, 116), (10, 92), (10, 46)], scale=6, contrast=.5, dk=.18, lt=.35, k=.25, rim=.15, feather=.5)
    def paint(dd, l):
        dd.rectangle([0, px(16), px(100), px(28)], fill=(176, 46, 38, 255)); dd.rectangle([0, px(108), px(100), px(120)], fill=(176, 46, 38, 255))
        for x in (30, 50, 70): dd.line([(px(x), px(28)), (px(x + (x - 50) * .25), px(108))], fill=(150, 96, 50, 90), width=px(1))
        for k in range(5):   # plum blossoms painted on the paper
            fx, fy = 28 + k * 11, 52 + (k % 2) * 26
            for p in range(5):
                a = p / 5 * math.tau; dd.ellipse([px(fx + math.cos(a) * 3.4 - 3), px(fy + math.sin(a) * 3.4 - 3), px(fx + math.cos(a) * 3.4 + 3), px(fy + math.sin(a) * 3.4 + 3)], fill=(214, 92, 104, 200))
    clipped(img, m, paint)
    soft(img, lambda d: d.ellipse([px(30), px(46), px(70), px(96)], fill=(255, 246, 210, 150)), 9)
    shape(img, LAC, 206, [(22, 10), (78, 10), (84, 20), (16, 20)], scale=4, k=.5, rim=.2, spec=.2, smooth=False, feather=.3)
    shape(img, GOLD, 207, ell=(44, 2, 56, 12), scale=2, k=.6, rim=.3, spec=.4, feather=.3)
    return finish(img, 21)


def banner():   # kōhaku banner between two lacquered rods; the words are written live
    img = canvas(560, 132)
    for x in (14, 546): stroke(ImageDraw.Draw(img), [(x, 0), (x, 12)], (196, 60, 52, 255), 2)
    shape(img, LAC, 301, [(4, 10), (556, 10), (556, 18), (4, 18)], scale=4, k=.5, rim=.2, spec=.3, smooth=False, feather=.3)
    m = shape(img, hexc('#f1e6cd'), 302, [(12, 17), (548, 17), (546, 112), (14, 112)], scale=7, contrast=.5, dk=.12, lt=.2, k=.25, rim=.08, smooth=False, feather=.4)
    def paint(dd, l):
        for y0 in (17, 101): dd.rectangle([0, px(y0), px(560), px(y0 + 11)], fill=(178, 44, 38, 255))
        dd.rectangle([0, px(30), px(560), px(32)], fill=(214, 170, 72, 220)); dd.rectangle([0, px(97), px(560), px(99)], fill=(214, 170, 72, 220))
        rnd = random.Random(5)
        for _ in range(26):   # washi fibres
            x, y = rnd.uniform(14, 546), rnd.uniform(34, 95); dd.line([(px(x), px(y)), (px(x + rnd.uniform(-12, 12)), px(y + rnd.uniform(-3, 3)))], fill=(200, 184, 150, 70), width=px(.6))
    clipped(img, m, paint)
    shape(img, LAC, 303, [(4, 110), (556, 110), (556, 118), (4, 118)], scale=4, k=.5, rim=.2, spec=.3, smooth=False, feather=.3)
    for x in (10, 550):   # mizuhiki tassels
        shape(img, GOLD, 310 + x, ell=(x - 6, 112, x + 6, 124), scale=2, k=.6, rim=.3, spec=.4, feather=.3)
        for k in (-2.5, 0, 2.5): stroke(ImageDraw.Draw(img), [(x, 122), (x + k, 128), (x + k * 1.5, 131)], (200, 60, 50, 230), 1.4, 3)
    return finish(img, 31)


# ───────────── things («Праздники Муси») ─────────────
def frame():   # «Неделя вместе»: a lacquer photo frame with a little tabby portrait
    img = canvas(170, 190)
    shadow(img, 85, 184, 64)
    shape(img, LAC, 401, [(46, 150), (124, 150), (138, 186), (32, 186)], scale=4, k=.4, rim=.2, smooth=False, feather=.3)
    shape(img, hexc('#5a2a1e'), 402, [(14, 8), (156, 8), (156, 170), (14, 170)], scale=5, k=.5, rim=.3, spec=.15, smooth=False, feather=.4)
    ImageDraw.Draw(img).rectangle([px(22), px(16), px(148), px(162)], fill=(200, 160, 72, 255))
    m = shape(img, hexc('#3c4a5a'), 403, [(26, 20), (144, 20), (144, 158), (26, 158)], scale=10, contrast=.6, dk=.4, lt=.3, k=.3, rim=.3, smooth=False, feather=.2)
    def cat(dd, l):   # a tabby kitten portrait, warm sepia light
        dd.ellipse([px(26), px(30), px(144), px(150)], fill=(84, 92, 104, 255))
        dd.ellipse([px(36), px(124), px(134), px(200)], fill=(176, 136, 92, 255))
        for sx in (-1, 1): dd.polygon([(px(85 + sx * 30), px(78)), (px(85 + sx * 8), px(70)), (px(85 + sx * 30), px(42))], fill=(170, 128, 86, 255))
        for sx in (-1, 1): dd.polygon([(px(85 + sx * 26), px(72)), (px(85 + sx * 14), px(70)), (px(85 + sx * 27), px(54))], fill=(214, 150, 140, 255))
        dd.ellipse([px(50), px(60), px(120), px(128)], fill=(188, 148, 102, 255))
        for k in range(4): dd.line([(px(70 + k * 10), px(62)), (px(72 + k * 9), px(80))], fill=(110, 76, 48, 200), width=px(2.4))
        for sx in (-1, 1): dd.ellipse([px(85 + sx * 14 - 6), px(90), px(85 + sx * 14 + 6), px(101)], fill=(70, 84, 44, 255)); dd.ellipse([px(85 + sx * 14 - 1), px(91), px(85 + sx * 14 + 2), px(95)], fill=(255, 255, 240, 220))
        dd.polygon([(px(81), px(106)), (px(89), px(106)), (px(85), px(111))], fill=(196, 110, 110, 255))
        for sy in (-1, 1):
            for sx in (-1, 1): dd.line([(px(85 + sx * 12), px(110 + sy * 2)), (px(85 + sx * 40), px(106 + sy * 7))], fill=(240, 230, 210, 150), width=px(.8))
    clipped(img, m, cat)
    shape(img, hexc('#efe3c8'), 404, [(56, 138), (114, 138), (114, 154), (56, 154)], scale=3, k=.3, rim=.1, smooth=False, feather=.3)
    text(img, '七日', 85, 146, 11, (150, 40, 32), font=SERIF)
    return finish(img, 41)


def ribbon():   # «Месяц вместе»: a kōhaku mizuhiki knot with ribbon tails on a little sanbō stand
    img = canvas(160, 170)
    shadow(img, 80, 164, 60)
    shape(img, hexc('#c8a878'), 411, [(28, 120), (132, 120), (124, 162), (36, 162)], scale=5, k=.5, rim=.25, smooth=False, feather=.3)
    shape(img, hexc('#d8bc8c'), 412, [(18, 110), (142, 110), (142, 122), (18, 122)], scale=5, k=.4, rim=.2, smooth=False, feather=.3)
    ImageDraw.Draw(img).ellipse([px(66), px(132), px(94), px(152)], fill=(90, 64, 40, 255))
    for sx, col in ((-1, RED), (1, CREAM)):   # tails
        shape(img, col, 413 + sx, [(80, 60), (80 + sx * 12, 62), (80 + sx * 40, 112), (80 + sx * 30, 104), (80 + sx * 22, 114)], scale=3, k=.6, rim=.25, smooth=False, feather=.3)
    for sx, col in ((-1, RED), (1, CREAM)):   # loops
        shape(img, col, 420 + sx, [(80, 58), (80 + sx * 30, 26), (80 + sx * 58, 36), (80 + sx * 50, 66), (80 + sx * 20, 70)], scale=3, k=.7, rim=.3, spec=.2, feather=.4)
        shape(img, mixc(col, BLK, .35), 422 + sx, [(80 + sx * 10, 56), (80 + sx * 30, 40), (80 + sx * 42, 46), (80 + sx * 36, 58), (80 + sx * 16, 62)], scale=3, k=.4, rim=.2, feather=.4)
    shape(img, GOLD, 425, ell=(68, 46, 92, 72), scale=2, k=.7, rim=.3, spec=.45, feather=.4)
    d = ImageDraw.Draw(img)
    for k in range(3): stroke(d, [(72 + k * 8, 50), (76 + k * 4, 60), (72 + k * 8, 70)], (250, 230, 160, 200), 1.2, 3)
    text(img, '月', 80, 135, 14, (240, 226, 196), font=SERIF)
    return finish(img, 42)


def fan():   # «100 дней»: an open gold sensu on a lacquer stand, a hundred on it
    img = canvas(220, 170)
    shadow(img, 110, 164, 70)
    shape(img, LAC, 431, [(70, 140), (150, 140), (160, 164), (60, 164)], scale=4, k=.4, rim=.2, spec=.2, smooth=False, feather=.3)
    cx, cy, R, r0 = 110, 140, 118, 34
    pts = [(cx + math.cos(a) * R, cy + math.sin(a) * R) for a in np.linspace(math.pi * 1.06, math.pi * 1.94, 12)] + [(cx + math.cos(a) * r0, cy + math.sin(a) * r0) for a in np.linspace(math.pi * 1.94, math.pi * 1.06, 6)]
    m = shape(img, hexc('#e2c060'), 432, pts, scale=6, contrast=.7, dk=.25, lt=.35, k=.4, rim=.15, spec=.15, smooth=False, feather=.4)
    def paint(dd, l):
        for i, a in enumerate(np.linspace(math.pi * 1.06, math.pi * 1.94, 15)):
            dd.line([(px(cx + math.cos(a) * r0), px(cy + math.sin(a) * r0)), (px(cx + math.cos(a) * R), px(cy + math.sin(a) * R))], fill=(150, 110, 40, 120 if i % 2 else 60), width=px(1.2))
        dd.ellipse([px(cx - 26), px(cy - 102), px(cx + 26), px(cy - 50)], fill=(196, 48, 40, 255))   # the red sun
        for k, a in enumerate(np.linspace(math.pi * 1.15, math.pi * 1.85, 7)):   # little pine & wave marks
            dd.arc([px(cx + math.cos(a) * 92 - 8), px(cy + math.sin(a) * 92 - 5), px(cx + math.cos(a) * 92 + 8), px(cy + math.sin(a) * 92 + 7)], 180, 360, fill=(70, 90, 120, 200), width=px(1.6))
    clipped(img, m, paint)
    text(img, '百', cx, cy - 76, 26, (252, 240, 216), font=SERIF)
    d = ImageDraw.Draw(img)
    for a in np.linspace(math.pi * 1.06, math.pi * 1.94, 15): d.line([(px(cx), px(cy)), (px(cx + math.cos(a) * r0), px(cy + math.sin(a) * r0))], fill=(60, 36, 22, 255), width=px(2))
    shape(img, GOLD, 433, ell=(cx - 6, cy - 6, cx + 6, cy + 6), scale=2, k=.6, rim=.3, spec=.4, feather=.3)
    return finish(img, 43)


def kusudama():   # «Полгода»: a split kusudama ball, streamers falling out (hangs from above)
    img = canvas(150, 260)
    d = ImageDraw.Draw(img); stroke(d, [(75, 0), (75, 30)], (196, 60, 52, 255), 2.2)
    for sx, col in ((-1, GOLD), (1, GOLD)):
        shape(img, col, 441 + sx, [(75, 34), (75 + sx * 34, 40), (75 + sx * 52, 72), (75 + sx * 50, 96), (75 + sx * 6, 92)], scale=4, k=.7, rim=.35, spec=.35, feather=.4)
    rnd = random.Random(7)
    for k, col in enumerate([RED, CREAM, PINK, INDIGO, RED, CREAM, GOLD, PINK]):   # streamers
        x0 = 44 + k * 9; sway = rnd.uniform(-10, 10)
        stroke(ImageDraw.Draw(img), [(x0, 90), (x0 + sway * .4, 140), (x0 - sway * .3, 190), (x0 + sway * .5, 240 - (k % 3) * 12)], mixc(col, BLK, .12), 4.2, 6)
    for k in range(18):   # confetti
        x, y = rnd.uniform(18, 132), rnd.uniform(96, 250); c = [RED, GOLD, PINK, CREAM, INDIGO][k % 5]
        ImageDraw.Draw(img).rectangle([px(x), px(y), px(x + 4), px(y + 2.4)], fill=c)
    shape(img, CREAM, 448, [(52, 90), (98, 90), (94, 150), (56, 150)], scale=5, k=.3, rim=.1, smooth=False, feather=.3)
    text(img, '半年', 75, 120, 14, (160, 40, 32), font=SANS)
    return finish(img, 44)


def cake_body(img, cx, top, w, h, seed, big=False):
    """A strawberry shortcake (whole), seen slightly from above: sponge layers, cream, berries."""
    shape(img, hexc('#f6eedd'), seed, [(cx - w, top + h * .25), (cx + w, top + h * .25), (cx + w, top + h), (cx - w, top + h)], scale=5, contrast=.4, dk=.12, lt=.2, k=.5, rim=.2, smooth=False, feather=.4)
    d = ImageDraw.Draw(img)
    for f in (.48, .74):   # sponge & strawberry layers showing through
        d.rectangle([px(cx - w + 2), px(top + h * f - 2), px(cx + w - 2), px(top + h * f + 2)], fill=(232, 196, 120, 220))
        for k in range(int(w / 9)): d.ellipse([px(cx - w + 6 + k * 18), px(top + h * f - 2.2), px(cx - w + 13 + k * 18), px(top + h * f + 2.2)], fill=(200, 52, 56, 230))
    shape(img, hexc('#fbf6ea'), seed + 1, ell=(cx - w, top, cx + w, top + h * .5), scale=4, contrast=.3, k=.4, rim=.15, spec=.15, feather=.4)
    for k in range(9 if big else 7):   # cream rosettes and berries round the rim
        a = math.pi * (1.05 + .9 * k / (8 if big else 6)); x, y = cx + math.cos(a) * w * .8, top + h * .25 + math.sin(a) * h * .2
        shape(img, hexc('#fffaf0'), seed + 10 + k, ell=(x - 7, y - 6, x + 7, y + 5), scale=2, k=.6, rim=.2, feather=.3)
        strawberry(img, x, y - 7, 6.5 if big else 5.5, seed + 30 + k)
    for k in range(5 if big else 3):
        a = math.pi * (.1 + .8 * k / (4 if big else 2)); x, y = cx + math.cos(a) * w * .78, top + h * .25 + math.sin(a) * h * .2
        shape(img, hexc('#fffaf0'), seed + 50 + k, ell=(x - 7, y - 5, x + 7, y + 6), scale=2, k=.6, rim=.2, feather=.3)
        strawberry(img, x, y - 6, 6.5 if big else 5.5, seed + 60 + k)


def candle(img, x, y, h):
    shape(img, hexc('#e7a8b8'), int(x * 7), [(x - 3, y - h), (x + 3, y - h), (x + 3, y), (x - 3, y)], scale=2, k=.5, rim=.2, smooth=False, feather=.3)
    soft(img, lambda d: d.ellipse([px(x - 7), px(y - h - 16), px(x + 7), px(y - h + 2)], fill=(255, 190, 110, 110)), 3)
    poly_s(ImageDraw.Draw(img), [(x, y - h - 12), (x + 3, y - h - 4), (x, y - h + 1), (x - 3, y - h - 4)], (255, 214, 120, 255), 5)


def cakefig():   # «Год вместе»: a big tiered cake figure with a sugar Musya and one candle
    img = canvas(220, 230)
    shadow(img, 110, 222, 92, 110)
    shape(img, hexc('#d6d0c4'), 451, ell=(10, 196, 210, 226), scale=4, k=.5, rim=.2, spec=.25, feather=.4)
    cake_body(img, 110, 120, 88, 92, 452, big=True)
    cake_body(img, 110, 64, 56, 70, 470)
    # a sugar tabby on top
    shape(img, hexc('#c89a62'), 490, ell=(92, 34, 128, 70), scale=3, k=.7, rim=.3, feather=.4)
    shape(img, hexc('#d0a46c'), 491, ell=(94, 16, 126, 44), scale=3, k=.7, rim=.3, feather=.4)
    d = ImageDraw.Draw(img)
    for sx in (-1, 1): d.polygon([(px(110 + sx * 15), px(10)), (px(110 + sx * 6), px(20)), (px(110 + sx * 16), px(24))], fill=(196, 150, 100, 255))
    for k in range(3): d.line([(px(104 + k * 6), px(18)), (px(105 + k * 5), px(26))], fill=(120, 80, 50, 220), width=px(1.6))
    for sx in (-1, 1): d.ellipse([px(110 + sx * 7 - 2), px(28), px(110 + sx * 7 + 2), px(32)], fill=(40, 40, 30, 255))
    stroke(d, [(126, 60), (138, 50), (136, 38)], (196, 150, 100, 255), 4)
    candle(img, 84, 76, 26)
    shape(img, hexc('#efe3c8'), 492, [(62, 166), (158, 166), (158, 184), (62, 184)], scale=3, k=.3, rim=.1, smooth=False, feather=.3)
    text(img, '一歳', 110, 175, 12, (160, 40, 32), font=SERIF)
    return finish(img, 45)


def maneki():   # «Ещё год»: a tabby maneki-neko in a paper party hat, holding a koban
    img = canvas(160, 210)
    shadow(img, 80, 204, 58)
    fur = hexc('#c99a64')
    shape(img, fur, 501, [(34, 200), (126, 200), (124, 140), (108, 104), (52, 104), (36, 140)], scale=5, k=.7, rim=.35, feather=.5)
    m = shape(img, fur, 502, ell=(36, 52, 124, 128), scale=5, k=.7, rim=.35, feather=.5)
    clipped(img, m, lambda dd, l: [dd.line([(px(66 + k * 9), px(54)), (px(68 + k * 8), px(78))], fill=(110, 72, 42, 210), width=px(3.4)) for k in range(4)])
    d = ImageDraw.Draw(img)
    for sx in (-1, 1): poly_s(d, [(80 + sx * 40, 34), (80 + sx * 16, 60), (80 + sx * 42, 70)], fur, 4)
    for sx in (-1, 1): stroke(d, [(80 + sx * 20, 96), (80 + sx * 12, 98)], (40, 30, 20, 255), 2.4)   # closed happy eyes
    poly_s(d, [(76, 104), (84, 104), (80, 109)], (200, 110, 110, 255), 3)
    shape(img, hexc('#f4e8d4'), 503, ell=(62, 108, 98, 128), scale=3, k=.4, rim=.2, feather=.4)
    shape(img, fur, 504, [(102, 116), (122, 104), (130, 66), (118, 60), (108, 70), (100, 104)], scale=4, k=.7, rim=.3, feather=.5)   # the raised paw
    shape(img, hexc('#f4e8d4'), 505, ell=(112, 52, 132, 72), scale=3, k=.6, rim=.2, feather=.4)
    shape(img, RED, 506, [(40, 128), (120, 128), (120, 138), (40, 138)], scale=3, k=.5, rim=.2, smooth=False, feather=.3)
    shape(img, GOLD, 507, ell=(70, 132, 90, 148), scale=2, k=.6, rim=.3, spec=.5, feather=.3)
    shape(img, GOLD, 508, ell=(46, 148, 86, 196), scale=3, k=.6, rim=.3, spec=.4, feather=.4)   # koban
    text(img, '寿', 66, 172, 14, (120, 70, 20), font=SERIF)
    m = shape(img, PINK, 509, [(80, 2), (102, 48), (58, 48)], scale=3, k=.6, rim=.2, smooth=False, feather=.3)   # party hat
    clipped(img, m, lambda dd, l: [dd.line([(px(60), px(44 - k * 12)), (px(100), px(36 - k * 12))], fill=(250, 240, 220, 230), width=px(3)) for k in range(4)])
    shape(img, GOLD, 510, ell=(75, 0, 85, 10), scale=2, k=.6, rim=.3, spec=.4, feather=.3)
    return finish(img, 46)


# ───────────── dishes (pantry: FATL.bd) ─────────────
def dish_cake():
    img = canvas(180, 140)
    shadow(img, 90, 132, 80, 100)
    shape(img, hexc('#e8e2d6'), 601, ell=(6, 104, 174, 136), scale=4, k=.5, rim=.2, spec=.3, feather=.4)
    cake_body(img, 90, 40, 70, 84, 602)
    candle(img, 90, 52, 22)
    return finish(img, 61)


def dish_sekihan():
    img = canvas(170, 130)
    shadow(img, 85, 124, 72, 100)
    shape(img, LAC, 611, [(14, 70), (156, 70), (138, 116), (32, 116)], scale=4, k=.6, rim=.3, spec=.3, feather=.5)
    shape(img, hexc('#9a2a22'), 612, [(18, 70), (152, 70), (146, 82), (24, 82)], scale=3, k=.3, rim=.1, smooth=False, feather=.3)
    m = shape(img, hexc('#c46a6a'), 613, ell=(18, 30, 152, 88), scale=2.5, contrast=1.3, dk=.35, lt=.3, k=.6, rim=.25, feather=.5)
    rnd = random.Random(3)
    def grains(dd, l):
        for _ in range(110):
            x, y = rnd.uniform(24, 146), rnd.uniform(34, 84); a = rnd.uniform(0, math.pi)
            dd.ellipse([px(x - 2.4), px(y - 1.4), px(x + 2.4), px(y + 1.4)], fill=(222, 150, 150, 200) if rnd.random() < .7 else (240, 200, 196, 210))
        for _ in range(16):
            x, y = rnd.uniform(30, 140), rnd.uniform(36, 80); dd.ellipse([px(x - 3.4), px(y - 2.4), px(x + 3.4), px(y + 2.4)], fill=(110, 26, 34, 255))
        for _ in range(26):
            x, y = rnd.uniform(40, 130), rnd.uniform(38, 70); dd.ellipse([px(x - .9), px(y - .6), px(x + .9), px(y + .6)], fill=(20, 16, 16, 255))
    clipped(img, m, grains)
    for k, (x, y) in enumerate(((112, 36), (122, 40), (104, 42))):   # nanten leaves & berries
        poly_s(ImageDraw.Draw(img), [(x, y), (x + 12, y - 8), (x + 22, y - 2), (x + 10, y + 4)], (60, 112, 56, 255), 5)
    for x, y in ((100, 34), (106, 30)): shape(img, hexc('#d0302a'), 620 + x, ell=(x - 4, y - 4, x + 4, y + 4), scale=2, k=.6, rim=.3, spec=.5, feather=.3)
    return finish(img, 62)


if __name__ == '__main__':
    parts = [('gar', garland()), ('ban', banner()), ('bon', bonbori()), ('bd_frame', frame()), ('bd_ribbon', ribbon()), ('bd_fan', fan()),
             ('bd_kusudama', kusudama()), ('bd_cakefig', cakefig()), ('bd_maneki', maneki()), ('ds_bd_cake', dish_cake()), ('ds_bd_sekihan', dish_sekihan())]
    AW, gap = 1180, 4; x = y = rowh = 0; rects = {}
    for name, p in parts:   # shelf packing
        if x + p.width > AW: x = 0; y += rowh + gap; rowh = 0
        rects[name] = [x, y, p.width, p.height]; x += p.width + gap; rowh = max(rowh, p.height)
    AH = y + rowh
    atlas = Image.new('RGBA', (AW, AH), (0, 0, 0, 0))
    for name, p in parts: atlas.alpha_composite(p, tuple(rects[name][:2]))
    atlas.save(os.path.join(ROOT, 'assets/items/atlas_bd.webp'), 'WEBP', quality=88, alpha_quality=92, method=6)
    pv = Image.new('RGBA', (AW, AH), (46, 44, 52, 255)); pv.alpha_composite(atlas); pv.save(os.path.join(PREV, 'birthday_preview.png'))
    print('atlas', AW, AH, os.path.getsize(os.path.join(ROOT, 'assets/items/atlas_bd.webp')), json.dumps(rects))
