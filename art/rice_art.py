#!/usr/bin/env python3
"""«Рисовое поле» (add-on rice, feat/rice.js): three terraced paddies on the hill behind the house + one atlas
with the field parts (seedlings → golden ears, weeds, hasa-gake rack, sheaves, scarecrow, usu & kine, sickle,
a rice bale for the pantry) and 3 collectible things.
Usage: cd art && python3 rice_art.py ../assets [bg] [atlas]
  → ../assets/bg/ri_field.webp (900×1500, transparent sky — the game paints day/night sky behind it)
  → ../assets/items/atlas_ri.webp; rect map → art/out/rice/rice.json (pasted into feat/rice.js)"""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
ASSETS = os.path.abspath(sys.argv[1]); HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv[1] = os.path.join(ASSETS, 'items')
import paint as P
from paint import hexc, mixc, fbm
import items as I
from items import px, canvas, fill, volume, soft, floor_shadow, line, ell, poly, H, dk, lt, SANS
PREV = os.path.join(HERE, 'out', 'rice'); os.makedirs(PREV, exist_ok=True)
SPR = {}; ROWS = []

# the paddies: (top y, bottom y, top half-width, bottom half-width, contour bow, front wall height) — same in feat/rice.js
PAD = [(585, 700, 290, 330, 26, 30), (770, 935, 360, 400, 34, 40), (1015, 1225, 425, 470, 44, 50)]


def edge(y0, hw, bow, n=40):
    return [(450 + u * hw, y0 + bow * (1 - u * u)) for u in np.linspace(-1, 1, n)]


def grain(im, seed, amt=3.2, sat=.88):
    a = np.asarray(im, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * sat
    a[..., :3] += np.random.default_rng(seed).normal(0, amt, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def keep(name, img, seed=1):
    SPR[name] = grain(img.resize((P.W, P.H), Image.LANCZOS), seed)


def blade(img, x0, y0, ang, L, w, col, bend=0.0, n=10):
    """A tapered curved leaf from (x0,y0): ang from vertical (+ right), bend adds curvature towards the tip."""
    x, y = x0, y0; c = [(x, y)]
    for i in range(1, n + 1):
        t = i / n; a = ang + bend * t * t; x += math.sin(a) * L / n; y -= math.cos(a) * L / n; c.append((x, y))
    left, right = [], []
    for i, (x, y) in enumerate(c):
        j = min(i, n - 1); dx = c[j + 1][0] - c[j][0]; dy = c[j + 1][1] - c[j][1]; d = math.hypot(dx, dy) or 1
        hw = w * .5 * (1 - i / n) ** .8; left.append((x - dy / d * hw, y + dx / d * hw)); right.append((x + dy / d * hw, y - dx / d * hw))
    poly(img, left + right[::-1], col)
    return c[-1]


def panicle(img, x, y, ang, L, col, grain_col, rnd, droop=2.0, n=9):
    """A drooping rice ear: a thin stalk arching over with grains along it."""
    pts = [(x, y)]; a = ang
    for i in range(1, n + 1):
        t = i / n; a = ang + droop * t; x += math.sin(a) * L / n; y -= math.cos(a) * L / n; pts.append((x, y))
    line(img, pts, dk(H(col), .2), 1.4)
    for i, (gx, gy) in enumerate(pts[2:], 2):
        for s in (-1, 1):
            r = 2.6 * (1 - i / (n + 4)); c = mixc(H(grain_col), H('#ffffff') if rnd.random() < .2 else dk(H(grain_col), .25), rnd.uniform(0, .3))
            ell(img, (gx + s * 2.2 - r, gy - r * 1.3, gx + s * 2.2 + r, gy + r * 1.3), c)


def clump(img, cx, base, h, n, cols, seed, spread=.45, droop=.5, wid=.055, ears=0, ear_col='#b8a050', grain_col='#d8bf6a', ear_droop=2.2):
    rnd = random.Random(seed); tips = []
    order = sorted(range(n), key=lambda i: rnd.random())
    for k, i in enumerate(order):
        ang = rnd.uniform(-spread, spread); L = h * rnd.uniform(.62, 1.0); col = mixc(H(rnd.choice(cols)), BLACK, .3 * (1 - k / n))
        tip = blade(img, cx + rnd.uniform(-h * .05, h * .05), base, ang, L, h * wid * rnd.uniform(.8, 1.2), col, bend=math.copysign(droop * rnd.uniform(.4, 1.2), ang))
        tips.append((tip, ang))
    for e in range(ears):
        ang = rnd.uniform(-.25, .25); L = h * rnd.uniform(.75, .95); x, y = cx + rnd.uniform(-3, 3), base
        top = blade(img, x, y, ang, L, 1.6, H(ear_col), bend=0, n=6)
        panicle(img, top[0], top[1], ang, h * .32, ear_col, grain_col, rnd, droop=ear_droop * rnd.choice((-1, 1)) * rnd.uniform(.8, 1.1))


BLACK = (0, 0, 0, 255)
G_SEED = ['#6f8f44', '#86a552', '#5d7d3a', '#9cb862']
G_MID = ['#4f7034', '#5f8240', '#6c8f48', '#43602c']
G_DEEP = ['#3f5f2c', '#4c6e34', '#567a3a', '#36522a']
G_GOLD = ['#a8894a', '#bea056', '#8f7638', '#c9ad62']


def parts():
    img = canvas(46, 58); soft(img, lambda d: d.ellipse([px(8), px(50), px(38), px(57)], fill=(30, 26, 18, 120)), 2)
    clump(img, 23, 54, 48, 8, G_SEED, 11, spread=.5, droop=.6, wid=.07); keep('nae', img, 2)
    img = canvas(72, 106); clump(img, 36, 102, 96, 13, G_MID, 12, spread=.42, droop=.7, wid=.05); keep('g1', img, 3)
    img = canvas(96, 152); clump(img, 48, 148, 138, 16, G_DEEP, 13, spread=.4, droop=.8, wid=.045, ears=4, ear_col='#7f8f48', grain_col='#a9b46a', ear_droop=1.2); keep('g2', img, 4)
    img = canvas(104, 160); clump(img, 52, 156, 136, 14, G_GOLD, 14, spread=.42, droop=.9, wid=.042, ears=8, ear_col='#a68a40', grain_col='#e0c26a', ear_droop=2.6); keep('gold', img, 5)
    # stubble after the harvest
    img = canvas(56, 32); rnd = random.Random(15); soft(img, lambda d: d.ellipse([px(4), px(22), px(52), px(31)], fill=(30, 24, 16, 140)), 2)
    for i in range(14):
        x = 28 + rnd.uniform(-18, 18); h = rnd.uniform(9, 18); line(img, [(x, 27), (x + rnd.uniform(-3, 3), 27 - h)], mixc(H('#b89a5a'), H('#6a5530'), rnd.random()), 2.2)
    keep('stub', img, 6)
    # a weed (hie — barnyard grass): darker blue-green, splayed, with purplish heads
    img = canvas(58, 66); clump(img, 29, 62, 58, 9, ['#2f4a3a', '#3a5a44', '#26402f'], 16, spread=.95, droop=.6, wid=.11, ears=2, ear_col='#4a3a4a', grain_col='#7a5a6a', ear_droop=1.0); keep('weed', img, 7)
    # a cut sheaf (flies to the rack)
    img = canvas(66, 126); rnd = random.Random(17)
    for i in range(16):
        x = 33 + rnd.uniform(-7, 7); line(img, [(x + rnd.uniform(-4, 4), 122), (x, 70), (33 + rnd.uniform(-10, 10), 34)], mixc(H('#b49352'), H('#7c6532'), rnd.random()), 2.4)
    for i in range(7):
        panicle(img, 33 + rnd.uniform(-8, 8), 38, rnd.uniform(-.3, .3), 34, '#a68a40', '#e0c26a', rnd, droop=rnd.choice((-1, 1)) * 2.4)
    fill(img, '#6a5228', 18, rect=(24, 82, 42, 90), scale=2)
    keep('sheaf', img, 8)
    # a sheaf hung over the rack pole (ears down on the left, cut straw on the right)
    img = canvas(86, 132); rnd = random.Random(19)
    for s, L, ears in ((-1, 92, True), (1, 80, False)):
        for i in range(12):
            a = math.pi + s * rnd.uniform(.08, .32); tip = blade(img, 43 + s * 4, 12, a, L * rnd.uniform(.8, 1), 3.2, mixc(H('#b49352'), H('#6f5a2e'), rnd.random()), bend=-s * .15)
            if ears and i % 2 == 0: panicle(img, tip[0], tip[1], math.pi + s * .2, 22, '#a68a40', '#e2c46e', rnd, droop=rnd.choice((-1, 1)) * .9, n=6)
    fill(img, '#5a4424', 20, ell=(30, 4, 56, 22), scale=2); keep('hang', img, 9)
    # hasa-gake: X-legs of bamboo and two long poles
    img = canvas(400, 300); bam = H('#9a8a5c'); floor_shadow(img, 200, 294, 190, 70)
    for x in (34, 200, 366):
        for s in (-1, 1): line(img, [(x - s * 6, 30), (x + s * 34, 296)], dk(bam, .35), 7); line(img, [(x - s * 6, 30), (x + s * 34, 296)], bam, 4)
        line(img, [(x - 14, 60), (x + 14, 60)], H('#4a3a22'), 4)
    for y in (64, 150):
        line(img, [(4, y), (396, y + 3)], dk(bam, .4), 10); line(img, [(4, y - 1), (396, y + 2)], bam, 6); line(img, [(4, y - 3), (396, y)], lt(bam, .3), 1.6)
        for x in range(30, 400, 46): line(img, [(x, y - 4), (x, y + 5)], dk(bam, .5), 2)
    keep('rack', img, 10)
    # the scarecrow (kakashi): bamboo cross, indigo kimono, a cloth face «henohenomoheji», a straw hat
    img = scarecrow(); keep('kakashi', img, 11); ROWS.append(row('ri_kakashi', 'Пугало какаси', 'b'))
    img = canvas(184, 100); floor_shadow(img, 92, 92, 84, 90); kasa(img, 92, 70, 170, 56); keep('kasa', img, 12); ROWS.append(row('ri_kasa', 'Соломенная шляпа', 'b'))
    img = kakeho(); keep('kakeho', img, 13); ROWS.append(row('ri_kakeho', 'Сноп риса какэхо', 't'))
    # usu (mortar) and kine (mallet)
    img = canvas(280, 214); floor_shadow(img, 140, 206, 128, 110)
    body = [(18, 56), (262, 56), (246, 120), (236, 200), (44, 200), (34, 120)]
    fill(img, '#6a4a30', 21, poly=body, scale=6, stretch=(1, 6), contrast=1.4, dark=.5, light=.25); volume(img, (18, 40, 262, 204), k=.7, rim=.5)
    fill(img, '#3a2a1a', 22, rect=(30, 112, 250, 124), scale=3, stretch=(6, 1)); fill(img, '#3a2a1a', 23, rect=(40, 176, 240, 186), scale=3, stretch=(6, 1))
    fill(img, '#8a6a46', 24, ell=(16, 26, 264, 88), scale=6, stretch=(4, 1), contrast=1.2, dark=.35, light=.3)
    fill(img, '#2a1c12', 25, ell=(40, 34, 240, 80), scale=5, dark=.5, light=.15)
    keep('usu', img, 14)
    img = canvas(112, 320); wood = H('#9a7a4e')
    fill(img, dk(wood, .1), 26, rect=(48, 64, 64, 318), scale=3, stretch=(1, 8), contrast=1.2)
    fill(img, wood, 27, rect=(8, 12, 104, 72), scale=4, stretch=(6, 1), contrast=1.3, dark=.4, light=.3); volume(img, (8, 12, 104, 72), k=.6, rim=.3)
    fill(img, lt(wood, .15), 28, ell=(0, 12, 18, 72), scale=3); fill(img, dk(wood, .2), 29, ell=(96, 12, 112, 72), scale=3)
    keep('kine', img, 15)
    # the sickle
    img = canvas(122, 104); line(img, [(22, 98), (64, 46)], H('#3a2618'), 11); line(img, [(22, 98), (64, 46)], H('#6a4a2c'), 7)
    outer = [(62, 46), (78, 22), (100, 10), (118, 12)]; inner = [(116, 16), (98, 18), (82, 30), (68, 50)]
    poly(img, outer + inner, '#8c9296'); line(img, outer, '#d8dde0', 2); keep('kama', img, 16)
    # a straw rice bale (komedawara) — the own rice in the pantry
    img = canvas(130, 100); floor_shadow(img, 65, 94, 60, 100)
    fill(img, '#b0924e', 30, poly=[(16, 22), (114, 22), (122, 52), (114, 86), (16, 86), (8, 52)], scale=2, stretch=(6, 1), contrast=1.5, dark=.45, light=.3)
    volume(img, (6, 18, 124, 90), k=.6, rim=.5)
    for x in (30, 65, 100): line(img, [(x - 3, 20), (x + 3, 52), (x - 3, 88)], '#5a4422', 4)
    fill(img, '#9a7c40', 31, ell=(0, 20, 22, 88), scale=2, contrast=1.4); fill(img, '#9a7c40', 32, ell=(108, 20, 130, 88), scale=2, contrast=1.4)
    keep('tawara', img, 17)


def row(iid, name, a):
    return {'id': iid, 'n': name, 'c': 'Рисовое поле', 'a': a, 'p': 0}


def kasa(img, cx, by, w, h, cords=True):
    straw = H('#b89b5c'); pts = [(cx - w / 2, by), (cx - w * .1, by - h * .92), (cx, by - h), (cx + w * .1, by - h * .92), (cx + w / 2, by), (cx, by + h * .12)]
    fill(img, straw, 41, poly=pts, scale=2, stretch=(1, 3), contrast=1.4, dark=.4, light=.3)
    for k in range(-9, 10): line(img, [(cx, by - h + 2), (cx + k * w / 19, by + h * .1 * (1 - (k / 9) ** 2))], dk(straw, .3), .8)
    for f in (.35, .65): line(img, [(cx - w / 2 * f - 2, by - h * (1 - f)), (cx, by - h * (1 - f) + h * .1 * f), (cx + w / 2 * f + 2, by - h * (1 - f))], dk(straw, .35), 1.2)
    volume(img, (cx - w / 2, by - h, cx + w / 2, by + h * .14), k=.6, rim=.3)
    if cords: line(img, [(cx - w * .22, by + 2), (cx - w * .12, by + 18), (cx - w * .02, by + 22)], '#9a2a22', 2); line(img, [(cx + w * .22, by + 2), (cx + w * .12, by + 18), (cx + w * .02, by + 22)], '#9a2a22', 2)


def scarecrow():
    img = canvas(176, 280); floor_shadow(img, 88, 274, 40, 90); bam = H('#8a7a50'); rnd = random.Random(51)
    line(img, [(88, 276), (88, 40)], dk(bam, .3), 8); line(img, [(87, 276), (87, 40)], bam, 5)
    line(img, [(8, 116), (168, 112)], dk(bam, .3), 7); line(img, [(8, 115), (168, 111)], bam, 4)
    # straw skirt (mino)
    for i in range(40):
        x = 60 + i * 1.4; line(img, [(x, 176), (x + rnd.uniform(-8, 8), 236 + rnd.uniform(-8, 6))], mixc(H('#a88d52'), H('#6d5a30'), rnd.random()), 2.2)
    # indigo kimono with patches
    ind = H('#2e3e5a')
    fill(img, ind, 52, poly=[(56, 102), (120, 102), (126, 186), (50, 186)], scale=5, contrast=1.3, dark=.5, light=.25)
    fill(img, ind, 53, poly=[(14, 104), (60, 102), (60, 140), (24, 136)], scale=4, contrast=1.3); fill(img, ind, 54, poly=[(116, 102), (162, 102), (154, 136), (116, 140)], scale=4, contrast=1.3)
    fill(img, '#b8b0a0', 55, rect=(64, 140, 82, 156), scale=2); fill(img, '#8a4a3a', 56, rect=(100, 120, 114, 134), scale=2)
    line(img, [(70, 102), (88, 136), (106, 102)], '#d8d0c0', 3); fill(img, '#7a3a2a', 57, rect=(54, 158, 122, 168), scale=2)
    volume(img, (12, 100, 164, 190), k=.5, rim=.35)
    # cloth face with «へのへのもへじ»
    fill(img, '#e2dccb', 58, ell=(56, 44, 120, 104), scale=3, dark=.25, light=.1); volume(img, (56, 44, 120, 104), k=.5, rim=.4)
    for ch, x, y, s in (('へ', 76, 60, 13), ('へ', 100, 60, 13), ('の', 76, 72, 13), ('の', 100, 72, 13), ('も', 88, 84, 12), ('へ', 88, 95, 12)): I.text(img, ch, x, y, s, '#1c1a18', SANS)
    line(img, [(118, 60), (124, 74), (120, 92)], '#2a2622', 1.6)    # the «じ» stroke on the cheek
    kasa(img, 88, 52, 120, 40, cords=False)
    # naruko clappers hanging from the right arm
    for k, x in enumerate((150, 160)):
        line(img, [(x, 113), (x, 132)], '#5a4a30', 1.2); fill(img, '#9a7a4a', 60 + k, rect=(x - 6, 132, x + 6, 152), scale=2); volume(img, (x - 6, 132, x + 6, 152), k=.5)
    return img


def kakeho():
    img = canvas(132, 236); rnd = random.Random(71)
    line(img, [(52, 30), (66, 4), (80, 30)], '#b8322a', 2.4); line(img, [(54, 30), (66, 8), (78, 30)], '#e8e0d0', 1.2)
    for i in range(22):
        x = 66 + rnd.uniform(-10, 10); line(img, [(66 + rnd.uniform(-5, 5), 34), (x, 100), (66 + (x - 66) * 2.4, 156)], mixc(H('#b49352'), H('#7c6532'), rnd.random()), 2.4)
    for i in range(14):
        panicle(img, 66 + rnd.uniform(-26, 26), 150, rnd.uniform(-.6, .6) + math.pi, 52, '#a68a40', '#e0c26a', rnd, droop=rnd.uniform(-.5, .5), n=9)
    fill(img, '#b8322a', 72, rect=(52, 36, 80, 50), scale=2); line(img, [(52, 43), (80, 43)], '#e8e0d0', 2)
    fill(img, '#e8e2d2', 73, poly=[(72, 50), (84, 50), (78, 64), (88, 64), (80, 82), (74, 82), (80, 66), (70, 66)], scale=2, dark=.15)    # a paper shide
    return img


def bg():
    img = canvas(900, 1500); rnd = random.Random(5)
    def ridge(base, amp, seed, n=60):
        r = random.Random(seed); xs = np.linspace(-20, 920, n); ys = np.zeros(n); v = 0
        for i in range(n): v = v * .82 + r.uniform(-1, 1); ys[i] = v
        ys = (ys - ys.min()) / (ys.max() - ys.min() + 1e-6)
        return [(x, base - amp * y) for x, y in zip(xs, ys)]
    for base, amp, col, fog, seed in ((420, 120, '#5c6a72', '#8e989c', 1), (500, 90, '#45534e', '#7f8a88', 2)):
        L = canvas(900, 1500); pts = ridge(base, amp, seed) + [(920, 1500), (-20, 1500)]
        fill(L, col, seed + 10, poly=pts, scale=40, stretch=(3, 1), contrast=.9, dark=.25, light=.15)
        a = np.asarray(L, np.float32); yy = np.arange(a.shape[0])[:, None] / I.S
        w = np.clip((yy - (base - amp * .6)) / (amp * 1.2), 0, 1) * .8; f = np.array(H(fog)[:3], np.float32)
        a[..., :3] = a[..., :3] * (1 - w[..., None]) + f * w[..., None]; img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))
    # the hill and a cedar wood on its crest
    hill = [(-20, 590), (150, 566), (330, 552), (520, 556), (720, 548), (920, 566), (920, 1500), (-20, 1500)]
    PAL = [hexc('#1a2620'), hexc('#24342a'), hexc('#2e4234'), hexc('#3a5040'), hexc('#4a604c')]
    for i in range(16):
        x = (i + rnd.uniform(0, 1)) * 60 - 20; P.cedar(img, x * I.S, (572 + rnd.uniform(-6, 10)) * I.S, rnd.uniform(110, 190) * I.S, rnd.uniform(70, 100) * I.S, 300 + i, PAL, P.BARK)
    fill(img, '#3a4230', 61, poly=hill, scale=22, stretch=(3, 1), contrast=1.5, dark=.5, light=.25)
    P.bushes(img, 600, 0, 900, 62, [hexc('#1c281e'), hexc('#26362a'), hexc('#324432'), hexc('#3e523c'), hexc('#4c6248')], count=10, rmin=26, rmax=48)
    for x, base, h in ((26, 760, 560), (874, 780, 600)):
        P.cedar(img, x * I.S, base * I.S, h * I.S, 190 * I.S, 400 + x, PAL, P.BARK)
    # terraces: the paddy bed (wet mud), its front wall and the grass lip of the ridge
    for i, (t, b, wt, wb, bow, wall) in enumerate(PAD):
        top = edge(t, wt, bow); bot = edge(b, wb, bow); lo = edge(b + wall, wb + wall * .4, bow)
        fill(img, '#5a5440', 70 + i, poly=[(x, y - 16) for x, y in top] + [(x + 8, y) for x, y in top[::-1]], scale=10, stretch=(4, 1), contrast=1.2)   # ridge path behind
        fill(img, '#3e372b', 80 + i, poly=top + bot[::-1], scale=14, stretch=(5, 1), contrast=1.3, dark=.45, light=.22)
        a = np.asarray(img, np.float32)     # a faint wet sheen towards the far edge
        m = Image.new('L', img.size, 0); ImageDraw.Draw(m).polygon([(px(x), px(y)) for x, y in top + bot[::-1]], fill=255)
        yy = np.arange(a.shape[0])[:, None] / I.S; sh = np.clip(1 - (yy - t) / (b - t + bow), 0, 1) ** 2 * .22 * (np.asarray(m, np.float32) / 255)
        a[..., :3] = a[..., :3] * (1 - sh[..., None]) + np.array([150, 160, 160], np.float32) * sh[..., None]; img = Image.fromarray(a.astype(np.uint8), 'RGBA')
        fill(img, '#4e4230', 90 + i, poly=bot + lo[::-1], scale=6, stretch=(1, 3), contrast=1.4, dark=.5, light=.2)
        d = ImageDraw.Draw(img)
        for x, y in bot[::1]:
            for k in range(5):
                gx = x + rnd.uniform(-14, 14); gy = y + rnd.uniform(-2, 4); h = rnd.uniform(5, 13) * (.7 + .3 * i)
                d.line([(px(gx), px(gy)), (px(gx + rnd.uniform(-5, 5)), px(gy - h))], fill=mixc(H('#3c5030'), H('#7a8a52'), rnd.random()), width=px(1.3))
        for x, y in top:
            for k in range(3):
                gx = x + rnd.uniform(-14, 14); h = rnd.uniform(4, 10) * (.7 + .3 * i)
                d.line([(px(gx), px(y - 14)), (px(gx + rnd.uniform(-4, 4)), px(y - 14 - h))], fill=mixc(H('#3c5030'), H('#6e7e4a'), rnd.random()), width=px(1.1))
    # the earth path at the bottom where Musya sits, and a corner of the house roof
    t2, b2, wt2, wb2, bow2, wall2 = PAD[2]; lo = edge(b2 + wall2, wb2 + wall2 * .4, bow2)
    fill(img, '#5e5240', 95, poly=lo + [(920, 1500), (-20, 1500)], scale=16, stretch=(4, 1), contrast=1.2, dark=.4, light=.25)
    for k in range(26):
        x = rnd.uniform(160, 900); y = rnd.uniform(1340, 1490); r = rnd.uniform(4, 10)
        fill(img, '#6e675a', 100 + k, ell=(x - r, y - r * .6, x + r, y + r * .6), scale=2, contrast=1.3); volume(img, (x - r, y - r * .6, x + r, y + r * .6), k=.5)
    d = ImageDraw.Draw(img)
    for k in range(700):
        x = rnd.uniform(0, 900); y = rnd.uniform(1330, 1500); h = rnd.uniform(6, 16)
        if 200 < x < 860 and 1350 < y < 1470 and rnd.random() < .8: continue
        d.line([(px(x), px(y)), (px(x + rnd.uniform(-5, 5)), px(y - h))], fill=mixc(H('#34462c'), H('#6e7e4a'), rnd.random()), width=px(1.4))
    roof = [(-10, 1388), (150, 1420), (250, 1448), (250, 1470), (-10, 1470)]
    fill(img, '#2c2e30', 110, poly=roof, scale=3, stretch=(1, 4), contrast=1.4, dark=.5, light=.3)
    for x in range(0, 250, 16): line(img, [(x, 1388 + x * .24), (x, 1470)], '#1a1c1e', 2)
    fill(img, '#3a3c3e', 111, poly=[(-10, 1384), (250, 1446), (250, 1452), (-10, 1392)], scale=2)
    fill(img, '#1a1410', 112, rect=(-10, 1470, 250, 1500), scale=4)
    soft(img, lambda d: d.rectangle([px(40), px(1474), px(160), px(1500)], fill=(240, 180, 90, 90)), 6)
    # morning mist along the wood and between the terraces
    for y0, y1, al in ((540, 640, .35), (740, 800, .12), (980, 1040, .1)):
        a = np.asarray(img, np.float32); yy = np.arange(a.shape[0])[:, None] / I.S
        w = np.exp(-((yy - (y0 + y1) / 2) / ((y1 - y0) / 2)) ** 2) * al * (.7 + .3 * fbm(a.shape[1], a.shape[0], 120, 3, int(y0))) * (a[..., 3] / 255)
        a[..., :3] = a[..., :3] * (1 - w[..., None]) + np.array([170, 178, 176], np.float32) * w[..., None]; img = Image.fromarray(a.astype(np.uint8), 'RGBA')
    out = img.resize((900, 1500), Image.LANCZOS); out = grain(out, 5, 4.0, .85)
    p = os.path.join(ASSETS, 'bg', 'ri_field.webp'); out.save(p, 'WEBP', quality=80, alpha_quality=80, method=6)
    pv = Image.new('RGBA', out.size, (120, 130, 140, 255)); pv.alpha_composite(out); pv.convert('RGB').resize((450, 750)).save(os.path.join(PREV, 'ri_field.png'))
    print('bg', os.path.getsize(p) // 1024, 'KB')


def pack():
    lst = sorted(SPR.items(), key=lambda t: -t[1].height); W = 1000; x = y = rowh = 0; pos = {}
    for k, im in lst:
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[k] = (x, y); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for k, im in lst: at.paste(im, pos[k])
    p = os.path.join(ASSETS, 'items', 'atlas_ri.webp'); at.save(p, 'WEBP', quality=86, alpha_quality=90, method=6)
    prev = Image.new('RGBA', at.size, (60, 70, 60, 255)); prev.alpha_composite(at); prev.convert('RGB').save(os.path.join(PREV, 'atlas_ri.png'))
    name = {'ri_kakashi': 'kakashi', 'ri_kasa': 'kasa', 'ri_kakeho': 'kakeho'}
    for r in ROWS: k = name[r['id']]; r['w'], r['h'] = SPR[k].size; r['at'] = ['ri', *pos[k]]
    spr = {k: [*pos[k], *SPR[k].size] for k in SPR}
    print('atlas', at.size, os.path.getsize(p) // 1024, 'KB')
    return {'atlas': list(at.size), 'items': ROWS, 'spr': spr}


if __name__ == '__main__':
    what = sys.argv[2:] or ['bg', 'atlas']
    if 'atlas' in what:
        parts(); out = pack(); json.dump(out, open(os.path.join(PREV, 'rice.json'), 'w'), ensure_ascii=False)
        print(json.dumps(out, ensure_ascii=False, separators=(',', ':')))
    if 'bg' in what: bg()
