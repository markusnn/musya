#!/usr/bin/env python3
"""«Нурикабэ у ворот» (feat/nurikabe.js, prefix nu): the wall yōkai — an old whitewashed wall on a row of stones with a
small tiled roof, sleepy kind eyes and a mouth → assets/mon/m_nu_wall.webp. ONE atlas assets/items/atlas_nu.webp holds
three things (a roof tile, a plaster chip with an eye, a traveller's staff) and two face patches cut from the same wall
(eyes closed = blink, a yawn) that the game draws over the face. Prints the rect map as JSON (pasted into the JS).
Previews → art/out/nu_*.png. Usage: nurikabe_art.py [assets dir]"""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'assets')
sys.argv = [sys.argv[0], os.path.join(HERE, 'out')]          # items.py reads its out dir from argv[1]
import paint as P
import items as I
from paint import textured_fill, fbm
from items import px, fill, volume, line, ell, poly, soft, floor_shadow, dk, lt, H

WW, WH = 640, 478                     # the wall picture (final px)
EYES = ((250, 192), (390, 192))
PATCH = {'blink': (196, 160, 248, 68), 'yawn': (196, 158, 250, 174)}   # x, y, w, h in the wall picture


def done(img, seed=11, sat=.9):
    out = img.resize((P.W, P.H), Image.LANCZOS); a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * sat; a[..., :3] += np.random.default_rng(seed).normal(0, 3.2, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def rmask(pts, r):
    """polygon → mask with rounded corners (blur + threshold)"""
    m = Image.new('L', (px(P.W), px(P.H)), 0); ImageDraw.Draw(m).polygon([(px(x), px(y)) for x, y in pts], fill=255)
    return m.filter(ImageFilter.GaussianBlur(px(r))).point(lambda v: 255 if v > 127 else 0).filter(ImageFilter.GaussianBlur(px(.7)))


def jblob(cx, cy, r, seed, n=28, k=.3):
    rr = random.Random(seed); f1, f2, f3 = rr.uniform(0, 6), rr.uniform(0, 6), rr.uniform(0, 6)
    q = lambda a: 1 + k * (.8 * math.sin(3 * a + f1) + .45 * math.sin(5 * a + f2) + .25 * math.sin(8 * a + f3)) / 1.5 + rr.uniform(-.03, .03)
    return [(cx + r * q(a) * math.cos(a), cy + r * .8 * q(a) * math.sin(a)) for a in (2 * math.pi * i / n for i in range(n))]


def blur_f(a, r):
    """three box blurs on a float array (≈ gaussian, no 8-bit banding)"""
    for _ in range(3):
        for ax in (0, 1):
            pad = [(r + 1, r) if i == ax else (0, 0) for i in range(2)]; c = np.cumsum(np.pad(a, pad, mode='edge'), axis=ax); n = a.shape[ax]
            a = (np.take(c, np.arange(2 * r + 1, n + 2 * r + 1), axis=ax) - np.take(c, np.arange(0, n), axis=ax)) / (2 * r + 1)
    return a


def paste_masked(img, layer, mask):
    z = Image.new('RGBA', img.size, (0, 0, 0, 0)); z.paste(layer, (0, 0), mask); img.alpha_composite(z)


def crack(d, x, y, ang, n, rr, w=1.3):
    pts = [(x, y)]
    for _ in range(n):
        ang += rr.uniform(-.55, .55); L = rr.uniform(7, 15); x += math.cos(ang) * L; y += math.sin(ang) * L; pts.append((x, y))
        if rr.random() < .12 and n > 4: crack(d, x, y, ang + rr.choice((-1, 1)) * rr.uniform(.6, 1.1), n // 2, rr, w * .7)
    d.line([(px(a + .9), px(b + .9)) for a, b in pts], fill=(250, 246, 236, 80), width=max(1, px(w * .8)), joint='curve')
    d.line([(px(a), px(b)) for a, b in pts], fill=(70, 60, 50, 210), width=max(1, px(w)), joint='curve')


# ───────────────────────────── the wall ─────────────────────────────
def wall_body():
    img = I.canvas(WW, WH)
    floor_shadow(img, 320, 468, 316, 130)
    body = [(30, 456), (25, 330), (29, 210), (36, 120), (170, 112), (320, 108), (470, 112), (604, 120), (611, 210), (615, 330), (610, 456)]
    M = rmask(body, 9)
    t = textured_fill(M, H('#d2cab9'), H('#a09886'), H('#e8e2d4'), 20 * I.S, 3, contrast=.85)
    a = np.asarray(t, np.float32); h, w = a.shape[:2]
    hs = blur_f(np.asarray(M.resize((w // 4, h // 4), Image.BILINEAR), np.float32) / 255, px(40) // 6); gy, gx = np.gradient(hs)
    ls = ((-gx * -.55 + -gy * -.8) * px(70) / 4).astype(np.float32)             # normal = −∇h, light from the upper left
    lam = np.asarray(Image.fromarray(ls, 'F').resize((w, h), Image.BICUBIC), np.float32)
    yy = np.arange(h, dtype=np.float32)[:, None] / I.S
    sh = np.clip(.9 + lam, .55, 1.2) * (1.04 - .16 * np.clip((yy - 150) / 300, 0, 1))
    a[..., :3] *= sh[..., None]
    dirt = np.clip((yy - 330) / 126, 0, 1) ** 1.4 * (.55 + .45 * fbm(w, h, 30 * I.S, 4, 8))        # damp, dirty foot
    a[..., :3] = a[..., :3] * (1 - .55 * dirt[..., None]) + np.array([74, 72, 52], np.float32) * .55 * dirt[..., None]
    st = fbm(w, h, 16 * I.S, 4, 9, stretch=(1, 9)); run = np.clip(1 - (yy - 120) / 150, 0, 1) * np.clip((st - .45) * 2.2, 0, 1)
    a[..., :3] *= (1 - .2 * run[..., None])                                                      # rain streaks below the eave
    img.alpha_composite(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA'))
    # bare clay where the whitewash fell off (keep the face clear)
    for k, (cx, cy, r) in enumerate(((96, 304, 40), (548, 200, 26), (486, 374, 22), (130, 170, 16))):
        pts = jblob(cx, cy, r, 20 + k, k=.38)
        soft(img, lambda d, pts=pts: d.polygon([(px(x + 2), px(y + 3)) for x, y in pts], fill=(70, 62, 50, 200)), 1.2)
        m = I.mask_poly(img, pts).filter(ImageFilter.GaussianBlur(px(.8))); img.alpha_composite(textured_fill(m, H('#86684c'), H('#5a4430'), H('#9c7e5c'), 6 * I.S, 30 + k, contrast=1.0))
        L = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L); rr = random.Random(40 + k)
        for _ in range(int(r * 1.3)):                                                           # chopped straw in the clay
            x0, y0, an = cx + rr.uniform(-r, r), cy + rr.uniform(-r * .7, r * .7), rr.uniform(-.6, .6)
            d.line([(px(x0), px(y0)), (px(x0 + 9 * math.cos(an)), px(y0 + 9 * math.sin(an)))], fill=(196, 168, 110, 150), width=px(.8))
        paste_masked(img, L, m)
        line(img, pts[len(pts) * 9 // 16:len(pts) * 15 // 16], (240, 234, 220, 200), 1.0)        # the lit broken edge of the plaster
    # cracks
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L); rr = random.Random(5)
    for x, y, an, n in ((40, 250, -.2, 9), (606, 260, 3.4, 8), (200, 452, -1.3, 8), (452, 452, -1.9, 9), (96, 300, -1.2, 6), (548, 196, 2.2, 6), (330, 118, 1.7, 5), (140, 118, 1.3, 6)):
        crack(d, x, y, an, n, rr)
    paste_masked(img, L, M)
    # moss creeping up from the ground and from under the roof corners
    mm = fbm(img.width, img.height, 14 * I.S, 4, 12); yy2 = np.arange(img.height)[:, None] / I.S; xx2 = np.arange(img.width)[None, :] / I.S
    g = np.clip((yy2 - 380) / 60, 0, 1) * np.clip((mm - .42) * 3.2, 0, 1)
    g = np.maximum(g, np.clip(1 - (yy2 - 116) / 50, 0, 1) * np.clip(1 - np.minimum(xx2 - 30, 610 - xx2) / 90, 0, 1) * np.clip((mm - .5) * 3, 0, 1))
    mt = textured_fill(Image.fromarray((g * 235).astype(np.uint8)), H('#58703c'), H('#30431f'), H('#7d9450'), 5 * I.S, 13, contrast=1.2)
    paste_masked(img, mt, M)
    # a row of mossy footing stones
    rr = random.Random(7); x = 30
    while x < 618:
        rx = rr.uniform(32, 44); P.stone(img, min(x + rx * .6, 610 - rx * .3), 452 + rr.uniform(-3, 3), rx, rr.uniform(16, 21), rr.randint(1, 99), base=H('#555a53'))
        x += rx * 1.45
    return img, M


def roof(img):
    soft(img, lambda d: d.rectangle([px(30), px(104), px(610), px(140)], fill=(30, 26, 22, 120)), 7)          # shadow under the eave
    fill(img, '#3a2a1e', 61, rect=(20, 98, 620, 114), scale=4, stretch=(6, .4))                            # the beam under the tiles
    R = [(4, 104), (70, 52), (570, 52), (636, 104)]
    fill(img, '#4a4e52', 62, poly=R, scale=6, stretch=(1, 3), contrast=1.1, dark=.5, light=.15)
    n = 24
    for i in range(n + 1):                                                                                   # round tiles (maru-gawara)
        u = i / n; xb, xt = 12 + u * 616, 76 + u * 488
        line(img, [(xt + 2.5, 54), (xb + 3.5, 100)], (24, 26, 30, 255), 4)
        line(img, [(xt, 54), (xb, 100)], (98, 104, 110, 255), 6.5); line(img, [(xt - 1.6, 54), (xb - 2.2, 100)], (150, 156, 160, 255), 1.6)
    for k in range(1, 4):                                                                                    # overlaps of the rows
        y = 54 + k * 11.5; f = (y - 52) / 52
        line(img, [(70 - 66 * f, y), (570 + 66 * f, y)], (30, 32, 36, 150), 1.2)
    volume(img, (4, 52, 636, 104), .35, .2)
    for i in range(n + 1):                                                                                   # round end tiles at the eave
        xb = 12 + i / n * 616
        ell(img, (xb - 10, 94, xb + 10, 114), (44, 47, 52, 255)); ell(img, (xb - 8, 96, xb + 8, 112), (88, 94, 100, 255))
        ell(img, (xb - 3.5, 101, xb + 3.5, 108), (52, 56, 60, 255)); ell(img, (xb - 7, 96.5, xb - 1, 101), (140, 146, 150, 200))
    fill(img, '#3a3e42', 63, poly=[(58, 56), (64, 40), (576, 40), (582, 56)], scale=4, stretch=(6, .5))   # the ridge
    volume(img, (56, 38, 584, 58), .6, .3, spec=.08)
    for sx in (-1, 1):                                                                                       # upturned ridge ends
        x0 = 320 + sx * 264
        poly(img, [(x0 - 12 * sx, 58), (x0 - 12 * sx, 36), (x0 + 6 * sx, 22), (x0 + 14 * sx, 30), (x0 + 10 * sx, 58)], (52, 56, 60, 255))
        line(img, [(x0 - 10 * sx, 36), (x0 + 6 * sx, 24)], (130, 136, 140, 255), 1.4)
    for cx, cy, r, sd in ((150, 72, 18, 1), (420, 64, 12, 2), (560, 86, 15, 3)):                         # moss on the tiles
        m = I.mask_poly(img, jblob(cx, cy, r, 70 + sd, k=.5)).filter(ImageFilter.GaussianBlur(px(1.2))); img.alpha_composite(textured_fill(m, H('#4e6236'), H('#2a3a1c'), H('#73884a'), 3 * I.S, 80 + sd, contrast=1.2))
    rr = random.Random(9)
    for _ in range(14):                                                                                      # a tuft of grass on the ridge
        x0 = 446 + rr.uniform(-10, 10); an = -math.pi / 2 + rr.uniform(-.7, .7); L = rr.uniform(10, 22)
        line(img, [(x0, 42), (x0 + math.cos(an) * L * .5 + rr.uniform(-2, 2), 42 + math.sin(an) * L * .6), (x0 + math.cos(an) * L, 42 + math.sin(an) * L)], rr.choice(((92, 120, 60, 255), (120, 140, 70, 255), (70, 96, 48, 255))), 1.3)


def face(img, kind):
    """kind: open (sleepy, kind) · closed (blink) · yawn"""
    for (cx, cy) in EYES:
        soft(img, lambda d, cx=cx, cy=cy: d.ellipse([px(cx - 50), px(cy - 30), px(cx + 50), px(cy + 32)], fill=(70, 58, 44, 46)), 8)       # sockets
        s = -1 if cx < 320 else 1                                                                                                         # kind brows
        line(img, [(cx - 32, cy - 38 - 4 * s), (cx, cy - 44), (cx + 32, cy - 38 + 4 * s)], (120, 108, 92, 150), 5)
        line(img, [(cx - 31, cy - 39.5 - 4 * s), (cx, cy - 45.5), (cx + 31, cy - 39.5 + 4 * s)], (246, 240, 228, 120), 1.4)
    for (cx, cy) in ((192, 250), (448, 250)):
        soft(img, lambda d, cx=cx, cy=cy: d.ellipse([px(cx - 32), px(cy - 16), px(cx + 32), px(cy + 16)], fill=(214, 128, 104, 72)), 8)     # warm cheeks
    ink = (40, 28, 22, 255)
    for (cx, cy) in EYES:
        if kind == 'open':
            L = Image.new('RGBA', img.size, (0, 0, 0, 0)); box = (cx - 36, cy - 20, cx + 36, cy + 22)
            ell(L, box, (238, 232, 216, 255))
            ell(L, (cx - 18, cy - 10, cx + 18, cy + 26), (92, 64, 40, 255)); ell(L, (cx - 11, cy - 3, cx + 11, cy + 19), (24, 16, 12, 255))
            ell(L, (cx - 11, cy - 2, cx - 2, cy + 7), (255, 252, 240, 255)); ell(L, (cx + 5, cy + 10, cx + 10, cy + 15), (230, 224, 210, 200))
            lid = [(cx - 46, cy - 34), (cx + 46, cy - 34), (cx + 46, cy + 2), (cx + 24, cy - 2.5), (cx, cy - 4), (cx - 24, cy - 2.5), (cx - 46, cy + 2)]
            ImageDraw.Draw(L).polygon([(px(x), px(y)) for x, y in lid], fill=(206, 196, 178, 255))                                           # heavy sleepy lid
            m = I.mask_poly(L, ell=box); paste_masked(img, L, m)
            soft(img, lambda d, cx=cx, cy=cy: d.rectangle([px(cx - 32), px(cy - 2), px(cx + 32), px(cy + 5)], fill=(30, 20, 14, 70)), 2)   # the lid's shadow on the eye
            line(img, [(cx - 38, cy + 2), (cx - 24, cy - 3), (cx, cy - 4.5), (cx + 24, cy - 3), (cx + 38, cy + 2), (cx + 43, cy - 2)], ink, 4)
            line(img, [(cx - 26, cy + 22), (cx, cy + 25), (cx + 26, cy + 22)], (120, 100, 84, 170), 1.7)                                       # lower lid
        elif kind == 'closed':
            line(img, [(cx - 37, cy - 1), (cx - 19, cy + 8), (cx, cy + 11), (cx + 19, cy + 8), (cx + 37, cy - 1), (cx + 42, cy - 5)], ink, 4)
            for k in (-1, 0, 1): line(img, [(cx + k * 15, cy + 10 - abs(k) * 2.5), (cx + k * 18, cy + 17 - abs(k) * 2.5)], ink, 1.7)
        else:                                                                                                                             # squeezed shut
            line(img, [(cx - 35, cy + 7), (cx - 16, cy - 3), (cx, cy - 6), (cx + 16, cy - 3), (cx + 35, cy + 7)], ink, 4.2)
            line(img, [(cx - 28, cy + 14), (cx, cy + 9), (cx + 28, cy + 14)], (90, 70, 56, 200), 1.9)
    if kind == 'yawn':
        cx = EYES[1][0] + 44; ell(img, (cx - 5, 204, cx + 5, 218), (170, 210, 236, 230)); ell(img, (cx - 3, 206, cx + 1, 211), (240, 250, 255, 255))   # a sleepy tear
        soft(img, lambda d: d.ellipse([px(280), px(242), px(360), px(326)], fill=(60, 40, 30, 90)), 4)
        ell(img, (284, 240, 356, 322), (34, 20, 16, 255)); ell(img, (294, 250, 346, 304), (58, 30, 24, 255))
        ell(img, (296, 286, 344, 318), (150, 80, 72, 255)); ell(img, (305, 290, 335, 303), (182, 108, 96, 255))
        line(img, [(286, 264), (294, 246), (320, 238), (346, 246), (354, 264)], (120, 100, 84, 200), 2)
    else:                                                                                                                                 # a kind smile, a little open
        M = [(292, 254), (306, 262), (320, 264), (334, 262), (348, 254)]
        poly(img, M + [(338, 266), (320, 276), (302, 266)], (40, 24, 20, 255)); ell(img, (308, 266, 332, 278), (150, 82, 72, 255))
        poly(img, [(292, 250), (348, 250), (348, 254), (334, 262), (320, 264), (306, 262), (292, 254)], (214, 204, 186, 255))
        line(img, M, ink, 3.2); line(img, [(286, 249), (292, 254)], (70, 52, 42, 220), 2.2); line(img, [(348, 254), (354, 249)], (70, 52, 42, 220), 2.2)
        line(img, [(304, 282), (320, 285), (336, 282)], (120, 100, 84, 120), 1.5)


def wall(kind):
    random.seed(1); img, M = wall_body(); roof(img); face(img, kind); return done(img, 11)


# ───────────────────────────── things ─────────────────────────────
def tile():
    img = I.canvas(176, 124); floor_shadow(img, 92, 112, 80, 120)
    C = '#4c5156'
    fill(img, C, 1, poly=[(64, 30), (160, 22), (168, 34), (168, 88), (160, 100), (64, 104)], scale=4, stretch=(4, 1), contrast=1.1)
    volume(img, (60, 20, 170, 104), .7, .3, spec=.12, lx=-.2, ly=-.9)
    for y in (46, 64, 82): line(img, [(68, y), (162, y - 6 + (y - 46) * .2)], (40, 42, 46, 160), 1)
    ell(img, (14, 22, 104, 112), (40, 43, 48, 255)); fill(img, '#5a6066', 2, ell=(18, 26, 100, 108), scale=3, contrast=1.1); volume(img, (18, 26, 100, 108), .6, .35, spec=.1)
    ell(img, (28, 36, 90, 98), (66, 72, 78, 255)); ell(img, (31, 39, 87, 95), (84, 90, 96, 255))
    for k in range(3):                                                                                       # mitsudomoe
        an = k * 2 * math.pi / 3 - .5; cx, cy = 59 + 12 * math.cos(an), 67 + 12 * math.sin(an)
        ell(img, (cx - 7, cy - 7, cx + 7, cy + 7), (44, 48, 52, 255))
        line(img, [(cx + 6 * math.cos(an + 1.6), cy + 6 * math.sin(an + 1.6)), (cx + 12 * math.cos(an + 2.4), cy + 12 * math.sin(an + 2.4)), (59 + 4 * math.cos(an + 2.6), 67 + 4 * math.sin(an + 2.6))], (44, 48, 52, 255), 3.4)
    for k in range(10): ell(img, (66 + k * 4.2, 64 - (k % 3), 68 + k * 4.2, 66 - (k % 3)), (150, 156, 160, 255)) if k % 4 == 0 else None
    m = I.mask_poly(img, jblob(132, 30, 22, 5, k=.45)); img.alpha_composite(textured_fill(m, H('#5a7440'), H('#2e4020'), H('#8aa456'), 3 * I.S, 6, contrast=1.3))
    m = I.mask_poly(img, jblob(28, 96, 12, 7, k=.45)); img.alpha_composite(textured_fill(m, H('#5a7440'), H('#2e4020'), H('#8aa456'), 3 * I.S, 8, contrast=1.3))
    return done(img, 21)


def chip():
    img = I.canvas(160, 128); floor_shadow(img, 82, 118, 70, 120)
    F = [(18, 40), (52, 16), (104, 12), (140, 34), (146, 78), (120, 104), (62, 110), (22, 92)]
    poly(img, [(x + 6, y + 9) for x, y in F], (122, 92, 62, 255))                                             # the clay thickness
    fill(img, '#8e6e4e', 3, poly=[(x + 6, y + 9) for x, y in F], scale=3, contrast=1.1)
    fill(img, '#ddd6c6', 4, poly=F, scale=8, contrast=.8, dark=.25, light=.1); volume(img, (18, 12, 146, 110), .45, .25, spec=.05)
    line(img, F[:4], (248, 244, 234, 255), 1.4); line(img, [(30, 70), (44, 66), (52, 74), (64, 72)], (90, 80, 68, 200), 1)
    cx, cy = 84, 58                                                                                          # the little eye, half asleep
    soft(img, lambda d: d.ellipse([px(cx - 26), px(cy - 15), px(cx + 26), px(cy + 17)], fill=(70, 58, 44, 50)), 4)
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); box = (cx - 19, cy - 10, cx + 19, cy + 12)
    ell(L, box, (238, 232, 216, 255)); ell(L, (cx - 9, cy - 5, cx + 9, cy + 13), (88, 62, 40, 255)); ell(L, (cx - 5, cy - 1, cx + 5, cy + 9), (24, 16, 12, 255))
    ell(L, (cx - 5, cy, cx, cy + 4), (255, 252, 240, 255))
    ImageDraw.Draw(L).polygon([(px(x), px(y)) for x, y in [(cx - 24, cy - 18), (cx + 24, cy - 18), (cx + 24, cy + 1), (cx, cy - 2), (cx - 24, cy + 1)]], fill=(206, 196, 178, 255))
    paste_masked(img, L, I.mask_poly(L, ell=box))
    line(img, [(cx - 20, cy + 1), (cx - 10, cy - 2), (cx, cy - 2.5), (cx + 10, cy - 2), (cx + 20, cy + 1), (cx + 23, cy - 1)], (40, 28, 22, 255), 2.6)
    soft(img, lambda d: d.ellipse([px(cx - 46), px(cy + 16), px(cx - 26), px(cy + 28)], fill=(214, 128, 104, 70)), 4)
    m = I.mask_poly(img, jblob(128, 92, 14, 9, k=.45)); img.alpha_composite(textured_fill(m, H('#5a7440'), H('#2e4020'), H('#8aa456'), 3 * I.S, 10, contrast=1.3))
    return done(img, 22)


def staff():
    img = I.canvas(112, 280); floor_shadow(img, 60, 270, 34, 120)
    pts = [(62, 270), (60, 210), (63, 150), (59, 90), (62, 40), (58, 18)]
    line(img, pts, (52, 36, 24, 255), 9.5); line(img, pts, (112, 82, 54, 255), 7.5); line(img, [(x - 2, y) for x, y in pts], (160, 124, 84, 255), 2)
    for y in (64, 130, 196, 238): ell(img, (56, y - 3, 66, y + 3), (76, 54, 34, 255))                          # knots
    fill(img, '#6a4a30', 5, ell=(46, 4, 72, 30), scale=3); volume(img, (46, 4, 72, 30), .6, .35, spec=.1)       # the knob
    line(img, [(52, 40), (66, 44)], (178, 40, 32, 255), 3); line(img, [(60, 44), (44, 64)], (178, 40, 32, 255), 2.2)   # red cord
    fill(img, '#c99a52', 6, ell=(26, 64, 50, 88), scale=3); volume(img, (26, 64, 50, 88), .6, .35, spec=.2)    # hyōtan gourd
    fill(img, '#c99a52', 7, ell=(20, 82, 56, 122), scale=3); volume(img, (20, 82, 56, 122), .6, .35, spec=.2)
    line(img, [(28, 86), (48, 86)], (178, 40, 32, 255), 2.4); ell(img, (34, 58, 42, 66), (90, 60, 34, 255))
    zz = [(68, 52), (88, 58), (78, 70), (96, 78), (84, 92), (100, 100)]                                      # a paper shide
    line(img, zz, (90, 86, 80, 255), 5.2); line(img, zz, (236, 230, 216, 255), 4)
    line(img, [(64, 50), (70, 52)], (236, 230, 216, 255), 2)
    return done(img, 23)


if __name__ == '__main__':
    W0 = wall('open'); W1 = wall('closed'); W2 = wall('yawn')
    os.makedirs(os.path.join(ASSETS, 'mon'), exist_ok=True)
    W0.save(os.path.join(ASSETS, 'mon', 'm_nu_wall.webp'), 'WEBP', quality=88, alpha_quality=92, method=6)
    crop = lambda im, k: im.crop((PATCH[k][0], PATCH[k][1], PATCH[k][0] + PATCH[k][2], PATCH[k][1] + PATCH[k][3]))
    ims = [('nu_tile', tile()), ('nu_chip', chip()), ('nu_staff', staff()), ('blink', crop(W1, 'blink')), ('yawn', crop(W2, 'yawn'))]
    Wd = 520; x = y = rowh = 0; pos = {}
    for iid, im in sorted(ims, key=lambda t: -t[1].height):
        if x + im.width + 2 > Wd: x = 0; y += rowh + 2; rowh = 0
        pos[iid] = (x, y, im.width, im.height); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (Wd, y + rowh), (0, 0, 0, 0))
    for iid, im in ims: at.paste(im, pos[iid][:2])
    at.save(os.path.join(ASSETS, 'items', 'atlas_nu.webp'), 'WEBP', quality=90, alpha_quality=92, method=6)
    out = os.path.join(HERE, 'out'); os.makedirs(out, exist_ok=True)
    pv = Image.new('RGBA', (WW * 3 + 20, WH), (34, 30, 28, 255))
    for k, im in enumerate((W0, W1, W2)): pv.alpha_composite(im, (k * (WW + 10), 0))
    pv.convert('RGB').save(os.path.join(out, 'nu_wall.png'))
    pa = Image.new('RGBA', at.size, (34, 30, 28, 255)); pa.alpha_composite(at); pa.convert('RGB').save(os.path.join(out, 'nu_atlas.png'))
    # the wall in the entrance (2D approximation: torii plane, base y 962, 560 px wide)
    bg = Image.new('RGBA', (1800, 1400), (0, 0, 0, 255))
    for n in ('sky', 'shrine', 'trunks', 'torii', 'path'): bg.alpha_composite(Image.open(os.path.join(ASSETS, 'layers', f'entrance_{n}.webp')).convert('RGBA').resize((1800, 1400)))
    sc = 560 / WW; wv = W0.resize((560, int(WH * sc)), Image.LANCZOS); wa = np.asarray(wv, np.float32); wa[..., :3] *= .62; wv = Image.fromarray(wa.astype(np.uint8), 'RGBA')
    bg.alpha_composite(wv, (900 - 280, 962 - wv.height)); bg.crop((420, 300, 1380, 1400)).convert('RGB').resize((480, 550)).save(os.path.join(out, 'nu_in_room.png'))
    print(json.dumps({'size': [Wd, y + rowh], 'mon': [WW, WH], 'at': {iid: list(pos[iid]) for iid, _ in ims}}, separators=(',', ':')))
