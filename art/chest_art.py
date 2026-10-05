#!/usr/bin/env python3
"""«Сундук прабабушки» (feat/chest.js, prefix ob): an old paulownia (kiri) nagamochi with iron fittings — closed,
with the lid ajar (warm light in the gap) and propped open — a furoshiki bundle in three stages (tied, knot loosened,
spread open) and the twelve things of the family story. ALL in one atlas assets/items/atlas_ob.webp.
Prints the rect map as JSON (pasted into feat/chest.js). Preview → art/out/atlas_ob.png.
Usage: chest_art.py [assets dir]"""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
ASSETS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'assets')
OUTD = os.path.join(os.path.dirname(__file__), 'out'); os.makedirs(OUTD, exist_ok=True)
sys.argv = [sys.argv[0], OUTD]     # items.py writes its own helpers' pictures into argv[1]
import paint as P
import items as I
from items import px, fill, volume, line, ell, poly, text, soft, floor_shadow, dk, lt, H, SERIF

KIRI, KIRI_D, IRON = '#b39b74', '#8a7253', '#1b1714'


def done(img):
    out = img.resize((P.W, P.H), Image.LANCZOS); a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .88; a[..., :3] += np.random.default_rng(11).normal(0, 3, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def helper(fn, *a, **k):
    """run an items.py painter (it saves <iid>.webp into art/out) and load the result"""
    fn(*a, **k); return Image.open(os.path.join(OUTD, a[0] + '.webp')).convert('RGBA')


def grain(img, pts, seed, n, vert=True, a=46):
    m = I.mask_poly(img, pts); l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l); r = random.Random(seed)
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pts
    for k in range(n):
        t = (k + r.uniform(-.3, .3)) / n
        if vert: A, B = (x0 + (x1 - x0) * t, y0 + (y1 - y0) * t), (x3 + (x2 - x3) * t, y3 + (y2 - y3) * t)
        else: A, B = (x0 + (x3 - x0) * t, y0 + (y3 - y0) * t), (x1 + (x2 - x1) * t, y1 + (y2 - y1) * t)
        d.line([(px(A[0]), px(A[1])), (px(B[0]), px(B[1]))], fill=(70, 50, 30, r.randint(a // 2, a)), width=max(1, px(r.uniform(.4, .9))))
    z = Image.new('RGBA', img.size, (0, 0, 0, 0)); z.paste(l, (0, 0), m); img.alpha_composite(z)


def iron_corner(img, x, y, sx, sy, s=24):
    """L-shaped iron bracket on a corner, with rivets"""
    pts = [(x, y), (x + sx * s, y), (x + sx * s, y + sy * 7), (x + sx * 7, y + sy * 7), (x + sx * 7, y + sy * s), (x, y + sy * s)]
    poly(img, pts, IRON); line(img, [(x, y), (x + sx * s, y)], '#4a4038', 1)
    for (rx, ry) in ((x + sx * 4, y + sy * 4), (x + sx * (s - 4), y + sy * 3.5), (x + sx * 3.5, y + sy * (s - 4))): ell(img, (rx - 1.8, ry - 1.8, rx + 1.8, ry + 1.8), '#6a5a48')


# the chest: all three states share one 320-wide frame, body bottom at y=B
CW, CH, B = 320, 300, 286
BX0, BX1, BT, DX, DY = 22, 268, 196, 30, 20             # body front x0..x1, front top y, right side depth


def body(img, seed=1):
    F = [(BX0, BT), (BX1, BT), (BX1, B), (BX0, B)]; R = [(BX1, BT), (BX1 + DX, BT - DY), (BX1 + DX, B - DY), (BX1, B)]
    floor_shadow(img, (BX0 + BX1 + DX) / 2, B, 170, 130)
    fill(img, KIRI, seed, poly=F, scale=4, stretch=(4, .25), contrast=.8, dark=.28, light=.14); grain(img, F, seed, 14, vert=False)
    fill(img, KIRI_D, seed + 1, poly=R, scale=4, stretch=(.25, 4), contrast=.8, dark=.3); grain(img, R, seed + 1, 6)
    volume(img, (BX0, BT, BX1 + DX, B), .35, .2)
    soft(img, lambda d: d.rectangle([px(BX0), px(B - 30), px(BX1), px(B)], fill=(30, 20, 10, 60)), 6)        # age darkens the bottom
    line(img, [(BX1, BT), (BX1, B)], dk(H(KIRI), .35), .9)
    for x in (BX0, BX1): iron_corner(img, x, B, 1 if x == BX0 else -1, -1)
    iron_corner(img, BX1, B, 1, -1, 16)
    # iron ring handle (sao-tsuri) on the short side
    cx, cy = BX1 + DX * .5, BT + (B - BT) * .42 - DY * .5
    poly(img, [(cx - 8, cy - 10), (cx + 8, cy - 15), (cx + 8, cy + 5), (cx - 8, cy + 10)], IRON)
    ImageDraw.Draw(img).arc([px(cx - 11), px(cy - 2), px(cx + 11), px(cy + 26)], 0, 180, fill=H('#2a2420'), width=px(3.2))
    return F


def lid(img, dy=0, seed=5, ajar=False):
    """the lid: top face + front band + right band; dy lifts it (front edge up when ajar)"""
    lx0, lx1, ft, fb = BX0 - 6, BX1 + 6, BT - 30 - dy, BT + 4 - dy * .4
    top_back = BT - 30 - DY - dy * (.25 if ajar else 1)
    T = [(lx0, ft), (lx0 + DX, top_back), (lx1 + DX, top_back), (lx1, ft)]
    Fb = [(lx0, ft), (lx1, ft), (lx1, fb), (lx0, fb)]; Rb = [(lx1, ft), (lx1 + DX, top_back), (lx1 + DX, top_back + (fb - ft)), (lx1, fb)]
    fill(img, lt(H(KIRI), .1), seed, poly=T, scale=4, stretch=(4, .25), contrast=.7, dark=.22, light=.1); grain(img, T, seed, 10, vert=False, a=34)
    fill(img, dk(H(KIRI), .06), seed + 1, poly=Fb, scale=4, stretch=(4, .25), contrast=.8, dark=.28); grain(img, Fb, seed + 1, 5, vert=False)
    fill(img, KIRI_D, seed + 2, poly=Rb, scale=4, stretch=(.25, 4), contrast=.8, dark=.32)
    volume(img, (lx0, top_back, lx1 + DX, fb), .4, .18)
    line(img, [(lx0, ft), (lx1, ft), (lx1 + DX, top_back)], lt(H(KIRI), .35), 1.2)
    soft(img, lambda d: d.rectangle([px(lx0 + 10), px(top_back + 2), px(lx1 + DX - 10), px(top_back + 6)], fill=(235, 225, 200, 60)), 3)   # dust on the lid
    iron_corner(img, lx0, fb, 1, -1, 20); iron_corner(img, lx1, fb, -1, -1, 20)
    for x in (lx0 + 2, lx1 - 2): line(img, [(x, ft + 1), (x + DX * (.5 if x > lx0 + 10 else .3), ft - DY * .5)], IRON, 4)
    # the hasp: an iron plate on the front of the lid hanging onto the body, a ring and a small lock
    cx = (lx0 + lx1) / 2
    poly(img, [(cx - 18, ft + 6), (cx + 18, ft + 6), (cx + 14, fb + 24), (cx - 14, fb + 24)], IRON); line(img, [(cx - 18, ft + 6), (cx + 18, ft + 6)], '#4e443a', 1)
    ImageDraw.Draw(img).ellipse([px(cx - 7), px(fb + 6), px(cx + 7), px(fb + 20)], outline=H('#5a4a34'), width=px(2.4))
    for rx in (cx - 12, cx + 12): ell(img, (rx - 2, ft + 10, rx + 2, ft + 14), '#6a5a48')
    return ft, fb


def glow_slit(img, y0, y1, k=1.0):
    """warm light leaking out of the gap and spilling up onto the lid"""
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    d.polygon([(px(BX0 + 4), px(y1)), (px(BX1 - 4), px(y1)), (px(BX1 + DX - 6), px(y1 - DY)), (px(BX0 + DX), px(y0))], fill=(255, 200, 110, int(235 * k)))
    img.alpha_composite(l.filter(ImageFilter.GaussianBlur(2 * I.S)))
    g = Image.new('RGBA', img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse([px(BX0 - 10), px(y0 - 46), px(BX1 + DX + 10), px(y1 + 20)], fill=(255, 190, 100, int(80 * k)))
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(18 * I.S)))


def chest_closed():
    img = I.canvas(CW, CH); body(img); lid(img)
    return done(img)


def chest_ajar():
    img = I.canvas(CW, CH); body(img, 7)
    glow_slit(img, BT - DY - 2, BT + 2)
    ft, fb = lid(img, 22, 9, ajar=True)
    soft(img, lambda d: d.rectangle([px(BX0), px(fb - 3), px(BX1), px(fb + 2)], fill=(255, 196, 120, 120)), 2.5)    # light on the lid's lower edge
    return done(img)


def chest_open():
    img = I.canvas(CW, CH)
    # the lid propped open behind: its underside (plain darker wood) faces us
    L = [(BX0 + DX - 8, BT - DY - 150), (BX1 + DX + 2, BT - DY - 158), (BX1 + DX, BT - DY + 2), (BX0 + DX - 4, BT - DY + 4)]
    fill(img, dk(H(KIRI), .18), 21, poly=L, scale=4, stretch=(4, .25), contrast=.7, dark=.25); grain(img, L, 21, 12, vert=False, a=30)
    volume(img, (BX0 + DX - 8, BT - DY - 158, BX1 + DX + 2, BT - DY + 4), .45, .25)
    line(img, [L[0], L[1]], lt(H(KIRI), .25), 2)
    body(img, 23)
    O = [(BX0, BT), (BX0 + DX, BT - DY), (BX1 + DX, BT - DY), (BX1, BT)]
    poly(img, O, '#2a1a10')
    poly(img, [(BX0 + DX, BT - DY), (BX1 + DX, BT - DY), (BX1 + DX - 4, BT - DY + 12), (BX0 + DX + 4, BT - DY + 12)], '#7a5e3c')
    glow_slit(img, BT - DY + 2, BT - 2, 1.0)
    line(img, [(BX0, BT), (BX1, BT), (BX1 + DX, BT - DY)], lt(H(KIRI), .45), 2)
    return done(img)


# ── furoshiki: indigo cloth with white karakusa scrolls ──
FUR, FUR_FG = '#2c3c5e', '#d8d2c0'


def karakusa(img, m, seed, n=14, s=1.0):
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l); r = random.Random(seed); x0, y0, x1, y1 = [v / I.S for v in m.getbbox()]
    for _ in range(n):
        cx, cy = r.uniform(x0, x1), r.uniform(y0, y1); a0 = r.uniform(0, 6.3)
        pts = [(cx + math.cos(a0 + t * .5) * (2 + t * 1.1) * s, cy + math.sin(a0 + t * .5) * (2 + t * 1.1) * s) for t in range(16)]
        d.line([(px(x), px(y)) for x, y in pts], fill=H(FUR_FG)[:3] + (200,), width=px(1.6 * s))
        tx, ty = pts[-1]; d.ellipse([px(tx - 2.4 * s), px(ty - 2.4 * s), px(tx + 2.4 * s), px(ty + 2.4 * s)], fill=H(FUR_FG)[:3] + (200,))
    z = Image.new('RGBA', img.size, (0, 0, 0, 0)); z.paste(l, (0, 0), m); img.alpha_composite(z)


def furo(stage):
    img = I.canvas(200, 170); floor_shadow(img, 100, 160, 86, 120)
    if stage < 2:
        Bd = [(20, 158), (180, 158), (186, 104), (160, 70), (40, 70), (14, 104)]
        m = fill(img, FUR, 3, poly=Bd, scale=8, contrast=.9, dark=.4, light=.2); karakusa(img, m, 5)
        for k in range(5): line(img, [(40 + k * 28, 76), (34 + k * 30, 150)], dk(H(FUR), .35), 1.4)            # folds
        if stage == 0:   # the knot with two pert ears
            for sx in (-1, 1):
                E = [(100, 66), (100 + sx * 44, 18), (100 + sx * 56, 30), (100 + sx * 20, 74)]
                mm = fill(img, FUR, 7 + sx, poly=E, scale=5, contrast=.9); karakusa(img, mm, 8 + sx, 3, .8)
            fill(img, dk(H(FUR), .1), 9, ell=(80, 52, 120, 82), scale=3)
        else:            # loosened: the ears fall to the sides, a crack of light at the top
            soft(img, lambda d: d.ellipse([px(70), px(58), px(130), px(80)], fill=(255, 210, 140, 150)), 5)
            for sx in (-1, 1):
                E = [(100 + sx * 12, 70), (100 + sx * 70, 64), (100 + sx * 84, 96), (100 + sx * 30, 86)]
                mm = fill(img, FUR, 17 + sx, poly=E, scale=5, contrast=.9); karakusa(img, mm, 18 + sx, 3, .8)
        volume(img, (14, 18, 186, 158), .45, .3)
    else:                # spread open: a flattened diamond lying on the floor, corners and creases
        Dm = [(100, 92), (196, 128), (100, 166), (4, 128)]
        m = fill(img, FUR, 23, poly=Dm, scale=8, contrast=.9, dark=.35); karakusa(img, m, 25, 16)
        line(img, [(52, 110), (148, 146)], dk(H(FUR), .35), 1.2); line(img, [(52, 146), (148, 110)], dk(H(FUR), .35), 1.2)
        volume(img, (4, 92, 196, 166), .3, .2)
    return done(img)


# ── the twelve things ──
def kanzashi():
    img = I.canvas(200, 120); floor_shadow(img, 100, 112, 84, 90)
    line(img, [(18, 104), (166, 34)], '#120c0a', 5.2); line(img, [(20, 102), (164, 35)], '#4a3a30', 1.2)
    for k in range(4):   # silver bira-bira chains with leaves
        x0, y0 = 138 - k * 7, 52 + k * 3; x1, y1 = x0 - 6 + k * 3, y0 + 34 + k * 5
        line(img, [(x0, y0), (x1, y1)], '#b8b8b0', 1); ell(img, (x1 - 4, y1 - 2, x1 + 4, y1 + 6), '#d0d0c8')
    for p in range(5):   # a small silver plum flower
        a = p / 5 * math.tau; ell(img, (140 + math.cos(a) * 7 - 6, 46 + math.sin(a) * 7 - 6, 140 + math.cos(a) * 7 + 6, 46 + math.sin(a) * 7 + 6), '#d8d4c8')
    ell(img, (136, 42, 144, 50), '#c89a3a'); volume(img, (126, 32, 154, 60), .5, .3, spec=.2)
    fill(img, '#b8322a', 4, ell=(156, 18, 184, 46), scale=2, contrast=.6); volume(img, (156, 18, 184, 46), .7, .45, spec=.35)   # the red coral bead
    return done(img)


def koma():
    img = I.canvas(130, 140); floor_shadow(img, 65, 132, 48, 120)
    fill(img, '#b08a5a', 2, poly=[(14, 66), (116, 66), (70, 128), (60, 128)], scale=4, stretch=(.4, 3))
    for k, c in enumerate(('#a83228', '#2f6b3a', '#d8b048', '#a83228')):
        y = 74 + k * 12; w = 50 - k * 11; line(img, [(65 - w, y), (65 + w, y)], c, 4.4)
    line(img, [(65, 128), (65, 136)], '#3a3030', 2.4)
    fill(img, '#c8a070', 3, ell=(12, 50, 118, 82), scale=4)
    for r, c in ((48, '#a83228'), (34, '#2f6b3a'), (20, '#d8b048')): ImageDraw.Draw(img).ellipse([px(65 - r), px(66 - r * .3), px(65 + r), px(66 + r * .3)], outline=H(c), width=px(3.4))
    fill(img, '#6a4a2a', 4, rect=(60, 22, 70, 62), scale=2, stretch=(.3, 3)); ell(img, (59, 18, 71, 26), '#7a5a3a')
    volume(img, (12, 18, 118, 128), .5, .35, spec=.12)
    line(img, [(98, 120), (112, 110), (122, 120), (112, 130), (100, 128)], '#d8ccb0', 1.6)       # a bit of the string
    return done(img)


def notebook():
    img = I.canvas(180, 140); floor_shadow(img, 90, 128, 80, 100)
    poly(img, [(18, 116), (140, 128), (168, 92), (48, 82)], '#e0d4b8'); poly(img, [(18, 116), (140, 128), (140, 132), (18, 120)], '#c8bc9e')
    C = [(18, 110), (140, 122), (168, 86), (48, 76)]
    fill(img, '#4a5a6e', 3, poly=C, scale=5, contrast=.7, dark=.3); volume(img, (18, 76, 168, 122), .35, .2)
    for k in range(4): x, y = 140 + k * 7, 118 - k * 9; ell(img, (x - 2, y - 2, x + 2, y + 2), '#d8d0c0')
    line(img, [(140, 122), (168, 86)], '#d8d0c0', 1.4)
    poly(img, [(66, 86), (88, 88), (78, 112), (56, 110)], '#ece4d0')
    text(img, '帳', 73, 93, 11, '#1d1612', brush=True); text(img, '面', 70, 105, 11, '#1d1612', brush=True)
    line(img, [(30, 70), (150, 50)], '#9a2a22', 6); line(img, [(30, 68), (150, 48)], '#c84a3a', 2); poly(img, [(150, 47), (162, 47), (150, 54)], '#e0c8a0')
    return done(img)


def sakazuki():
    img = I.canvas(180, 130); floor_shadow(img, 90, 122, 78, 110)
    fill(img, '#7a1612', 2, poly=[(30, 96), (150, 96), (140, 122), (40, 122)], scale=3, contrast=.6); volume(img, (30, 96, 150, 122), .4, .3)
    ell(img, (64, 102, 116, 116), '#1a0806')
    for k, (w, y) in enumerate(((70, 92), (56, 72), (42, 54))):
        cx = 90; fill(img, '#a8201a', 5 + k, ell=(cx - w, y - 14, cx + w, y + 8), scale=3, contrast=.5); volume(img, (cx - w, y - 14, cx + w, y + 8), .5, .3, spec=.25)
        ell(img, (cx - w + 6, y - 12, cx + w - 6, y), '#c0302a'); soft(img, lambda d, w=w, y=y: d.ellipse([px(cx - w * .5), px(y - 10), px(cx + w * .1), px(y - 6)], fill=(255, 220, 200, 70)), 2)
        if k == 2:   # a gold crane on the top cup
            line(img, [(cx - 18, y - 6), (cx, y - 9), (cx + 14, y - 5)], '#e0b64a', 1.6); ell(img, (cx - 2, y - 11, cx + 2, y - 7), '#e0b64a')
    return done(img)


def letter():
    img = I.canvas(190, 140); floor_shadow(img, 95, 128, 82, 100)
    E = [(28, 112), (150, 126), (166, 54), (44, 40)]
    fill(img, '#b89a70', 3, poly=E, scale=4, contrast=.6, dark=.2); volume(img, (28, 40, 166, 126), .3, .2)
    Pp = [(46, 100), (150, 112), (168, 30), (64, 18)]
    fill(img, '#e6dac0', 4, poly=Pp, scale=3, contrast=.5, dark=.14); volume(img, (46, 18, 168, 112), .3, .2)
    for k in range(7):   # vertical lines of ink, one blacked out by the censor
        x = 72 + k * 12; line(img, [(x + 4, 32 + k * 1.2), (x - 6, 92 + k * 1.2)], '#2a2018' if k != 3 else '#0a0806', 1.2 if k != 3 else 5)
    poly(img, [(126, 26), (150, 30), (146, 52), (122, 48)], '#b02a22'); poly(img, [(129, 30), (147, 33), (144, 49), (125, 45)], '#e6dac0')
    text(img, '検', 135, 39, 11, '#b02a22')
    return done(img)


def fan():
    img = I.canvas(230, 150); cx, cy, R, r = 115, 140, 112, 36
    m = Image.new('L', img.size, 0); md = ImageDraw.Draw(m)
    md.pieslice([px(cx - R), px(cy - R), px(cx + R), px(cy + R)], 200, 340, fill=255); md.pieslice([px(cx - r), px(cy - r), px(cx + r), px(cy + r)], 200, 340, fill=0)
    fill(img, '#e2d4b0', 7, mask=m, scale=8, contrast=.7, dark=.25)
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l); rr = random.Random(3)
    for k in range(26):   # autumn grass (susuki) in faded ink
        a = math.radians(rr.uniform(210, 330)); r0 = rr.uniform(40, 60); r1 = rr.uniform(80, 104)
        d.line([(px(cx + math.cos(a) * r0), px(cy + math.sin(a) * r0)), (px(cx + math.cos(a + .08) * r1), px(cy + math.sin(a + .08) * r1))], fill=(90, 80, 60, 150), width=px(1.2))
    d.ellipse([px(cx + 30), px(cy - 96), px(cx + 52), px(cy - 74)], fill=(200, 160, 90, 170))
    z = Image.new('RGBA', img.size, (0, 0, 0, 0)); z.paste(l, (0, 0), m); img.alpha_composite(z)
    d = ImageDraw.Draw(img)
    for k in range(16):
        a = math.radians(200 + k * 140 / 15)
        d.line([(px(cx + math.cos(a) * r), px(cy + math.sin(a) * r)), (px(cx + math.cos(a) * R), px(cy + math.sin(a) * R))], fill=(150, 130, 100, 255), width=px(1))
        d.line([(px(cx), px(cy)), (px(cx + math.cos(a) * r), px(cy + math.sin(a) * r))], fill=H('#2a1a12'), width=px(2.4))
    # the kintsugi seams: jagged gold lines where the fan was broken
    for a0, a1, seed in ((236, 250, 1), (296, 284, 2), (262, 272, 3)):
        pts = []; q = random.Random(seed)
        for t in range(9):
            rad = 28 + t * 10.5; a = math.radians(a0 + (a1 - a0) * t / 8 + q.uniform(-2.5, 2.5)); pts.append((cx + math.cos(a) * rad, cy + math.sin(a) * rad))
        line(img, pts, '#7a5a1a', 3.4); line(img, pts, '#e8c25a', 2.2); line(img, [(x - .5, y - .6) for x, y in pts], '#fff0b0', .7)
    ell(img, (cx - 5, cy - 5, cx + 5, cy + 5), '#b8962a')
    return done(img)


def photo():
    img = I.canvas(150, 196); floor_shadow(img, 75, 190, 62, 110)
    poly(img, [(56, 186), (96, 186), (100, 196), (52, 196)], '#2a1e16')
    fill(img, '#3a2a1e', 2, rect=(10, 8, 140, 186), scale=4, contrast=.6); volume(img, (10, 8, 140, 186), .3, .2)
    fill(img, '#d8c8a4', 3, rect=(22, 24, 128, 150), scale=3, contrast=.4)            # the print, sepia
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    d.rectangle([px(22), px(24), px(128), px(70)], fill=(196, 176, 140, 255))
    d.polygon([(px(18), px(84)), (px(54), px(52)), (px(98), px(52)), (px(132), px(84))], fill=(70, 52, 36, 255))              # roof
    d.rectangle([px(30), px(84), px(120), px(128)], fill=(120, 96, 70, 255))
    for k in range(4): d.rectangle([px(36 + k * 21), px(88), px(52 + k * 21), px(122)], fill=(214, 198, 166, 255))          # shoji
    d.rectangle([px(22), px(122), px(128), px(130)], fill=(80, 60, 42, 255))                                                  # veranda
    d.ellipse([px(84), px(98), px(92), px(112)], fill=(236, 226, 206, 150))                                                   # a pale small shape behind the shoji
    d.ellipse([px(46), px(110), px(58), px(124)], fill=(60, 44, 30, 255)); d.polygon([(px(47), px(112)), (px(49), px(106)), (px(52), px(111))], fill=(60, 44, 30, 255))
    d.polygon([(px(52), px(111)), (px(55), px(106)), (px(57), px(112))], fill=(60, 44, 30, 255)); d.line([(px(57), px(122)), (px(64), px(124)), (px(66), px(118))], fill=(60, 44, 30, 255), width=px(2))   # the cat
    d.rectangle([px(22), px(130), px(128), px(150)], fill=(150, 130, 100, 255))
    img.alpha_composite(l.filter(ImageFilter.GaussianBlur(.7 * I.S)))
    rr = random.Random(5)
    for _ in range(14): x, y = rr.uniform(24, 126), rr.uniform(26, 148); line(img, [(x, y), (x + rr.uniform(-8, 8), y + rr.uniform(4, 14))], '#efe4cc', .5)
    soft(img, lambda d: d.rectangle([px(22), px(24), px(128), px(150)], outline=(60, 40, 20, 120), width=px(6)), 4)
    text(img, '昭和二十八年', 75, 168, 10, '#c8b890')
    return done(img)


def drawing():
    img = I.canvas(180, 140); floor_shadow(img, 90, 132, 80, 90)
    poly(img, [(14, 22), (166, 14), (172, 124), (20, 130)], '#ece4d2'); volume(img, (14, 14, 172, 130), .25, .2)
    def cr(pts, c, w=2.6): line(img, pts, c, w)
    cr([(30, 108), (160, 104)], '#5a8a3a', 3)                                                                        # grass
    cr([(36, 104), (36, 70), (62, 50), (88, 70), (88, 104)], '#7a4a2a'); cr([(30, 72), (62, 46), (94, 72)], '#3a3a5a', 3.4)   # house
    poly(img, [(104, 104), (124, 104), (114, 70)], '#c8302a'); ell(img, (106, 56, 122, 72), '#f0d8b8'); poly(img, [(104, 66), (106, 54), (122, 54), (124, 66), (120, 60), (108, 60)], '#1a1414')   # the girl
    ell(img, (132, 86, 156, 104), '#8a7050'); ell(img, (146, 76, 160, 90), '#8a7050'); poly(img, [(147, 79), (149, 72), (152, 78)], '#8a7050'); poly(img, [(154, 78), (158, 71), (159, 80)], '#8a7050')
    for k in range(3): cr([(136 + k * 6, 88), (138 + k * 6, 100)], '#4a3a2a', 1.4)
    cr([(132, 96), (124, 84)], '#8a7050', 2.2)                                                                       # cat with stripes
    ell(img, (138, 22, 156, 40), '#e8c84a')                                                                          # a moon
    text(img, 'ミワ', 40, 30, 11, '#b8322a')
    return done(img)


def last_letter():
    img = I.canvas(170, 140); floor_shadow(img, 85, 130, 74, 100)
    E = [(40, 124), (100, 128), (138, 22), (78, 16)]
    fill(img, '#efe6d2', 3, poly=E, scale=3, contrast=.45, dark=.12); volume(img, (40, 16, 138, 128), .3, .2)
    for k, ch in enumerate('後の人へ'): text(img, ch, 94 - k * 8 * .36 + 8, 40 + k * 20, 15, '#1d1612', brush=True)
    line(img, [(30, 84), (150, 96)], '#9a2a22', 3); line(img, [(30, 83), (150, 95)], '#c84a3a', 1.2)
    for p in range(5):   # a pressed camellia
        a = p / 5 * math.tau + .3; fill(img, '#a8201a', 30 + p, ell=(50 + math.cos(a) * 11 - 10, 100 + math.sin(a) * 9 - 9, 50 + math.cos(a) * 11 + 10, 100 + math.sin(a) * 9 + 9), scale=2, contrast=.6)
    ell(img, (45, 95, 55, 105), '#e0b040'); volume(img, (30, 82, 72, 120), .4, .3)
    return done(img)


if __name__ == '__main__':
    ims = [('closed', chest_closed()), ('ajar', chest_ajar()), ('open', chest_open()), ('f0', furo(0)), ('f1', furo(1)), ('f2', furo(2)),
           ('ob_kanzashi', kanzashi()), ('ob_koma', koma()), ('ob_notebook', notebook()), ('ob_sakazuki', sakazuki()), ('ob_letter', letter()), ('ob_fan', fan()),
           ('ob_photo', photo()),
           ('ob_kokeshi', helper(I.kokeshi, 'ob_kokeshi', 'Кокэси', '#c89a68', 'kiku', 170, 'bob')),
           ('ob_furin', helper(I.furin, 'ob_furin', 'Фурин', '#d6e4f0', 'asagao', ch='鈴')),
           ('ob_drawing', drawing()),
           ('ob_chochin', helper(I.chochin, 'ob_chochin', 'Фонарь', '#e4d4ac', '春', True)),
           ('ob_last', last_letter())]
    # crop the chest states to their visible top (the bottom and width stay shared)
    for i, (k, im) in enumerate(ims):
        if k in ('closed', 'ajar', 'open'): bb = im.getbbox(); ims[i] = (k, im.crop((0, max(0, bb[1] - 2), im.width, im.height)))
    # a crack in the old glass chime
    fu = dict(ims)['ob_furin']; d = ImageDraw.Draw(fu); d.line([(38, 58), (44, 70), (40, 80), (47, 94)], fill=(250, 250, 255, 200), width=1)
    W = 1100; x = y = rowh = 0; pos = {}
    for iid, im in sorted(ims, key=lambda t: -t[1].height):
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[iid] = (x, y, im.width, im.height); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for iid, im in ims: at.paste(im, pos[iid][:2])
    at.save(os.path.join(ASSETS, 'items', 'atlas_ob.webp'), 'WEBP', quality=88, alpha_quality=92, method=6)
    pv = Image.new('RGBA', at.size, (40, 34, 30, 255)); pv.alpha_composite(at); pv.convert('RGB').save(os.path.join(OUTD, 'atlas_ob.png'))
    for f in ('ob_kokeshi', 'ob_furin', 'ob_chochin'):
        try: os.remove(os.path.join(OUTD, f + '.webp'))
        except OSError: pass
    print(json.dumps({'size': [W, y + rowh], 'at': {iid: list(pos[iid]) for iid, _ in ims}}, separators=(',', ':')))
