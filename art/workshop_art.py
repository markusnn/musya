#!/usr/bin/env python3
"""«Мастерская» (feat/workshop.js, prefix ws): the low craft workbench with tools, 13 material icons and
16 hand-made things «Сделано своими лапами» — all packed into ONE atlas assets/items/atlas_ws.webp.
Prints the rect map as JSON (pasted into feat/workshop.js). Preview → art/out/atlas_ws.png.
Usage: workshop_art.py [assets dir]"""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw
ASSETS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'assets')
sys.argv = [sys.argv[0], os.path.join(os.path.dirname(__file__), 'out')]     # items.py reads its out dir from argv[1]
import paint as P
from paint import hexc, mixc
import items as I
from items import px, fill, volume, line, ell, poly, text, soft, floor_shadow, dk, lt, H


def done(img):
    out = img.resize((P.W, P.H), Image.LANCZOS); a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .9; a[..., :3] += np.random.default_rng(13).normal(0, 3, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def arc(img, box, a0, a1, col, w):
    ImageDraw.Draw(img).arc([px(v) for v in box], a0, a1, fill=H(col), width=max(1, px(w)))


def leaf(img, cx, cy, L, ang, col, seed, maple=False):
    c, s = math.cos(ang), math.sin(ang)
    R = lambda x, y: (cx + x * c - y * s, cy + x * s + y * c)
    if maple:
        pts = []
        for k in range(10):
            a = -math.pi / 2 + k * 2 * math.pi / 10; r = L * (.5 if k % 2 else (1 if k in (0, 2, 8) else .78))
            pts.append(R(r * math.cos(a) * .9, r * math.sin(a) * .9 + L * .1))
    else:
        pts = [R(-L * .5, 0), R(-L * .2, -L * .2), R(L * .25, -L * .17), R(L * .5, 0), R(L * .25, L * .17), R(-L * .2, L * .2)]
    fill(img, col, seed, poly=pts, scale=3, contrast=.9)
    line(img, [R(-L * .5, 0), R(L * .4, 0)] if not maple else [R(0, L * .1), R(0, -L * .6)], dk(H(col), .35), max(.8, L * .05))


def paw(img, x, y, r, col):
    ell(img, (x - r, y - r * .7, x + r, y + r * .9), col)
    for a in (-.95, -.32, .32, .95):
        tx, ty = x + math.sin(a) * r * 1.35, y - math.cos(a) * r * 1.2 - r * .3
        ell(img, (tx - r * .38, ty - r * .42, tx + r * .38, ty + r * .42), col)


# ───────────── the workbench: low thick plank on short legs, a shelf below, tools on top ─────────────
BW, BH = 420, 250


def bench():
    img = I.canvas(BW, BH); rnd = random.Random(3)
    floor_shadow(img, 210, 244, 200, 130)
    for x in (34, 360):                                                          # legs
        fill(img, '#4a3424', x, rect=(x, 128, x + 26, 244), scale=4, stretch=(.3, 3), contrast=1.2); volume(img, (x, 128, x + 26, 244), .5, .3)
    fill(img, '#3c2a1c', 9, rect=(40, 196, 380, 210), scale=4, stretch=(5, .3)); volume(img, (40, 196, 380, 210), .4, .2)     # lower shelf
    fill(img, '#7a5a3a', 11, rect=(70, 168, 160, 198), scale=3, contrast=1.1); volume(img, (70, 168, 160, 198), .5, .3)       # a small box of scraps
    for k in range(5): ell(img, (78 + k * 16, 160 + (k % 2) * 4, 92 + k * 16, 172 + (k % 2) * 4), ['#b8322a', '#efe6d4', '#3a5a9a', '#c9a24a', '#5f7a3a'][k])
    fill(img, '#6a4a2e', 12, rect=(250, 176, 330, 198), scale=3, stretch=(3, .4)); volume(img, (250, 176, 330, 198), .4, .3)    # rolled washi
    ell(img, (322, 176, 336, 198), '#e8dcc0')
    fill(img, '#5a3e28', 1, poly=[(14, 104), (406, 104), (414, 134), (6, 134)], scale=5, stretch=(6, .4), contrast=1.25)      # top plank
    volume(img, (6, 104, 414, 134), .45, .2)
    line(img, [(14, 104), (406, 104)], '#9a7652', 1.6)
    d = ImageDraw.Draw(img)
    for k in range(9):
        y = 110 + k * 2.6 + rnd.uniform(-1, 1); d.line([(px(20 + rnd.uniform(0, 60)), px(y)), (px(400 - rnd.uniform(0, 60)), px(y + rnd.uniform(-1, 1)))], fill=(30, 18, 10, 60), width=px(.7))
    # tools on top: plane (kanna), saw leaning on the right, paint dish + brush, red thread ball, scissors, shavings
    fill(img, '#a07a4e', 21, poly=[(40, 84), (128, 84), (132, 104), (36, 104)], scale=3, stretch=(4, .4)); volume(img, (36, 84, 132, 104), .5, .3)
    poly(img, [(76, 84), (92, 84), (88, 98), (80, 98)], '#2a2420'); line(img, [(78, 86), (90, 86)], '#c8ccd0', 1.4)
    for k in range(4):                                                            # curled wood shavings
        x = 140 + k * 13; arc(img, (x, 88 + k % 2 * 3, x + 16, 104), 180, 20, '#d8b888', 2.4)
    fill(img, '#b8bcc0', 22, poly=[(332, 30), (396, 96), (388, 104), (322, 40)], scale=2, contrast=.5)                     # saw blade
    d = ImageDraw.Draw(img)
    for k in range(10):
        t = k / 10; x, y = 396 - t * 70, 96 - t * 64; d.line([(px(x), px(y)), (px(x + 3), px(y - 4))], fill=(60, 60, 64, 255), width=px(1))
    fill(img, '#6a4a2a', 23, poly=[(312, 22), (330, 40), (322, 46), (304, 28)], scale=2); line(img, [(304, 26), (296, 18)], '#3a2618', 4)
    ell(img, (196, 88, 250, 104), '#efe6d4'); ell(img, (200, 90, 246, 100), '#d8d0bc')                                        # paint dish
    for k, c in enumerate(['#b8322a', '#2a4a8a', '#e0b84a']): ell(img, (205 + k * 13, 91, 215 + k * 13, 98), c)
    line(img, [(244, 96), (282, 70)], '#c9a870', 2.4); poly(img, [(242, 96), (250, 92), (246, 100)], '#1a1410')
    fill(img, '#b8322a', 24, ell=(262, 76, 292, 104), scale=2, contrast=.8); volume(img, (262, 76, 292, 104), .6, .4, spec=.2)  # thread ball
    for k in range(5): arc(img, (264 + k * 2, 78 + k, 290 - k * 2, 102 - k), 200 + k * 25, 330 + k * 25, '#e05a4a', .9)
    line(img, [(276, 102), (300, 104), (316, 100)], '#c83a2a', 1)
    line(img, [(160, 102), (190, 82)], '#9aa0a8', 2); line(img, [(166, 82), (190, 102)], '#9aa0a8', 2)                       # scissors
    ell(img, (154, 98, 166, 108), '#2a2420'); ell(img, (158, 101, 163, 106), '#5a3e28')
    soft(img, lambda dd: dd.ellipse([px(150), px(96), px(176), px(106)], fill=(0, 0, 0, 40)), 2)
    return done(img)


# ───────────── material icons 64×64 ─────────────
def m_wara():
    img = I.canvas(64, 64); rnd = random.Random(1)
    for k in range(16):
        x0 = 14 + rnd.uniform(0, 8); x1 = 44 + rnd.uniform(0, 10); a = rnd.uniform(-.4, .4)
        line(img, [(x0, 54 - k * .6 + a * 20), (32, 32), (x1, 8 + k * .8)], mixc(H('#d8b860'), H('#a88838'), rnd.random()), 1.6)
    line(img, [(26, 30), (38, 36)], '#b8322a', 3.5)
    return done(img)


def m_ha():
    img = I.canvas(64, 64)
    leaf(img, 24, 36, 34, -.6, '#c8642a', 2, True); leaf(img, 42, 28, 30, .9, '#6a8a3a', 3)
    return done(img)


def m_uroko():
    img = I.canvas(64, 64)
    for k, (x, y) in enumerate(((22, 22), (40, 24), (30, 40), (46, 42), (16, 42))):
        fill(img, '#9ab0c0', 30 + k, poly=[(x - 9, y + 2), (x, y - 10), (x + 9, y + 2), (x, y + 10)], scale=2, contrast=.6)
        arc(img, (x - 7, y - 6, x + 7, y + 8), 200, 340, '#e8f0f8', 1.2); volume(img, (x - 9, y - 10, x + 9, y + 10), .5, .2, spec=.4)
    return done(img)


def m_kai():
    img = I.canvas(64, 64); c = '#e8b8a8'
    fill(img, c, 4, poly=[(32, 54)] + [(32 + 24 * math.cos(a), 30 + 22 * math.sin(a)) for a in np.linspace(math.pi * 1.05, math.pi * 1.95, 9)], scale=2, contrast=.7)
    for a in np.linspace(math.pi * 1.1, math.pi * 1.9, 7): line(img, [(32, 52), (32 + 21 * math.cos(a), 30 + 19 * math.sin(a))], dk(H(c), .25), 1.2)
    poly(img, [(26, 50), (38, 50), (36, 58), (28, 58)], dk(H(c), .15)); volume(img, (8, 8, 56, 58), .5, .25, spec=.25)
    return done(img)


def m_eda():
    img = I.canvas(64, 64)
    for (a, b), c in ((((8, 50), (56, 14)), '#6a4a2e'), (((12, 18), (54, 52)), '#7a5a3a'), (((20, 58), (44, 6)), '#5a3e28')):
        line(img, [a, b], c, 4); line(img, [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), ((a[0] + b[0]) / 2 + 9, (a[1] + b[1]) / 2 - 8)], c, 2)
    return done(img)


def m_koke():
    img = I.canvas(64, 64)
    fill(img, '#4a6a2a', 5, ell=(8, 22, 56, 56), scale=2, contrast=1.4, dark=.5, light=.35); volume(img, (8, 22, 56, 56), .6, .35)
    rnd = random.Random(5)
    for _ in range(14): x, y = rnd.uniform(14, 50), rnd.uniform(24, 40); line(img, [(x, y), (x + rnd.uniform(-2, 2), y - 5)], '#9ab85a', 1)
    return done(img)


def m_donguri():
    img = I.canvas(64, 64)
    for x, y, a in ((22, 34, -.3), (42, 38, .3)):
        fill(img, '#9a6a3a', int(x), ell=(x - 10, y - 8, x + 10, y + 18), scale=2, contrast=.6); volume(img, (x - 10, y - 8, x + 10, y + 18), .6, .35, spec=.35)
        fill(img, '#5a4228', int(y), ell=(x - 12, y - 14, x + 12, y + 2), scale=1, contrast=1.6); line(img, [(x, y - 14), (x + a * 8, y - 20)], '#4a3420', 2)
    return done(img)


def m_hane():
    img = I.canvas(64, 64)
    pts = [(12, 56), (20, 36), (34, 16), (52, 6), (46, 24), (34, 42), (16, 56)]
    fill(img, '#d8d4cc', 6, poly=pts, scale=2, contrast=.6); line(img, [(10, 60), (50, 8)], '#8a8478', 1.4)
    for k in range(7): t = .2 + k * .1; x, y = 10 + 40 * t, 60 - 52 * t; line(img, [(x, y), (x + 6, y + 3)], '#a8a29a', .8)
    fill(img, '#4a4440', 7, poly=[(36, 24), (50, 9), (46, 22)], scale=2)
    return done(img)


def m_tsuchi():
    img = I.canvas(64, 64)
    fill(img, '#a8603a', 8, poly=[(10, 46), (16, 26), (34, 16), (52, 24), (56, 44), (40, 54), (20, 54)], scale=2, contrast=1.1); volume(img, (10, 16, 56, 54), .7, .35, spec=.15)
    for k in range(3): arc(img, (22 + k * 6, 28 + k * 4, 40 + k * 6, 40 + k * 4), 200, 320, '#7a4024', 1)
    return done(img)


def m_nuno():
    img = I.canvas(64, 64); c = H('#2e4a7a')
    fill(img, c, 9, poly=[(8, 22), (48, 12), (58, 40), (16, 54)], scale=3, contrast=.9); volume(img, (8, 12, 58, 54), .5, .3)
    d = ImageDraw.Draw(img)
    for k in range(9): x, y = 18 + (k % 3) * 12 + (k // 3) * 3, 22 + (k // 3) * 10; d.ellipse([px(x - 2), px(y - 2), px(x + 2), px(y + 2)], fill=H('#e8e0cc'))
    poly(img, [(48, 12), (58, 40), (50, 30)], dk(c, .3))
    return done(img)


def m_kami():
    img = I.canvas(64, 64)
    for k in range(3): fill(img, mixc(H('#efe6d0'), H('#d8c8a8'), k * .3), 10 + k, poly=[(8 + k * 2, 18 + k * 8), (52 + k * 2, 12 + k * 8), (56 + k * 2, 32 + k * 8), (12 + k * 2, 38 + k * 8)], scale=2, contrast=.5)
    text(img, '和', 34, 40, 13, '#8a6a4a', I.SERIF)
    return done(img)


def m_ito():
    img = I.canvas(64, 64)
    fill(img, '#c9a070', 12, rect=(18, 10, 46, 16), scale=2); fill(img, '#c9a070', 13, rect=(18, 48, 46, 54), scale=2)
    fill(img, '#c8322a', 14, rect=(21, 16, 43, 48), scale=1, contrast=.6); volume(img, (21, 16, 43, 48), .6, .3, spec=.2)
    for k in range(8): line(img, [(21, 18 + k * 4), (43, 20 + k * 4)], '#e05a4a', .7)
    line(img, [(43, 40), (54, 50), (58, 44)], '#c8322a', 1)
    return done(img)


def m_enogu():
    img = I.canvas(64, 64)
    ell(img, (6, 26, 58, 56), '#e8e0d0'); ell(img, (10, 30, 54, 52), '#d0c8b8')
    for k, c in enumerate(['#b8322a', '#2a4a8a', '#e0b84a', '#3f7a4a']): x = 15 + k * 10; ell(img, (x - 4, 36, x + 4, 46), c)
    line(img, [(36, 34), (58, 6)], '#c9a870', 3); poly(img, [(33, 38), (38, 31), (40, 34)], '#1a1410')
    return done(img)


MATS = [('wara', m_wara), ('ha', m_ha), ('uroko', m_uroko), ('kai', m_kai), ('eda', m_eda), ('koke', m_koke), ('donguri', m_donguri),
        ('hane', m_hane), ('tsuchi', m_tsuchi), ('nuno', m_nuno), ('kami', m_kami), ('ito', m_ito), ('enogu', m_enogu)]


# ───────────── 16 hand-made things ─────────────
def i_chochin():
    img = I.canvas(96, 168); c = H('#efd6a0')
    line(img, [(48, 0), (48, 26)], '#2a1c12', 1.6)
    fill(img, '#6a4a2e', 1, rect=(30, 26, 66, 34), scale=2); fill(img, '#6a4a2e', 2, rect=(30, 148, 66, 156), scale=2)
    fill(img, c, 3, ell=(10, 30, 86, 152), scale=4, contrast=.9, dark=.3, light=.3)
    a = np.asarray(img, np.float32)
    for k in range(1, 11): yk = px(30 + 122 * k / 11); a[max(0, yk - 1):yk + 1, :, :3] *= .7
    img = Image.fromarray(a.astype(np.uint8), 'RGBA')
    paw(img, 48, 94, 11, '#8a3a24')
    soft(img, lambda d: d.ellipse([px(26), px(60), px(70), px(124)], fill=(255, 220, 140, 70)), 8)
    volume(img, (10, 30, 86, 152), .45, .4)
    line(img, [(48, 156), (48, 166)], '#b8322a', 2)
    return done(img)


def i_kaeru():
    img = I.canvas(124, 92); g = H('#5f9a4a'); floor_shadow(img, 62, 86, 52)
    poly(img, [(12, 82), (40, 40), (62, 30), (86, 40), (112, 82)], g)
    poly(img, [(12, 82), (40, 40), (52, 82)], dk(g, .2)); poly(img, [(112, 82), (86, 40), (72, 82)], dk(g, .12))
    poly(img, [(40, 40), (62, 30), (86, 40), (62, 60)], lt(g, .15))
    poly(img, [(52, 82), (62, 60), (72, 82)], dk(g, .3))
    for x in (46, 78):
        poly(img, [(x - 10, 38), (x, 20), (x + 10, 38)], lt(g, .2)); ell(img, (x - 5, 26, x + 5, 36), '#f2ecd8'); ell(img, (x - 2, 29, x + 2, 34), '#141010')
    line(img, [(40, 40), (62, 60), (86, 40)], dk(g, .35), .8); line(img, [(62, 30), (62, 60)], dk(g, .25), .6)
    line(img, [(54, 50), (62, 54), (70, 50)], '#2a3a1e', 1)
    return done(img)


def i_teru():
    img = I.canvas(92, 150); W_ = H('#efe8dc')
    line(img, [(46, 0), (46, 18)], '#c8322a', 1.4)
    fill(img, W_, 1, poly=[(46, 52), (14, 132), (30, 128), (40, 140), (52, 128), (64, 140), (78, 130), (46, 52)], scale=3, contrast=.6)
    poly(img, [(46, 56), (36, 134), (40, 140), (46, 132)], dk(W_, .1))
    line(img, [(28, 62), (64, 62)], '#c8322a', 2.4); ell(img, (42, 60, 50, 70), '#c8322a')
    fill(img, W_, 2, ell=(20, 14, 72, 64), scale=3, contrast=.5); volume(img, (20, 14, 72, 64), .55, .3, spec=.15)
    ell(img, (34, 32, 38, 38), '#1a1410'); ell(img, (54, 32, 58, 38), '#1a1410'); arc(img, (40, 38, 52, 48), 20, 160, '#1a1410', 1.2)
    ell(img, (28, 40, 36, 44), '#f0b0b0'); ell(img, (56, 40, 64, 44), '#f0b0b0')
    return done(img)


def i_uma():
    img = I.canvas(164, 150); s = H('#d2b060'); floor_shadow(img, 82, 144, 66); rnd = random.Random(4)
    def bundle(a, b, w, seed):
        n = int(w / 1.6)
        for k in range(n):
            o = (k - n / 2) * 1.5; dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
            line(img, [(a[0] + nx * o, a[1] + ny * o), (b[0] + nx * o + rnd.uniform(-1, 1), b[1] + ny * o)], mixc(s, H('#9a7a30'), rnd.random() * .7), 1.5)
    for a, b in (((48, 82), (38, 140)), ((60, 84), (64, 140)), ((106, 84), (102, 140)), ((118, 82), (126, 140))): bundle(a, b, 9, 0)
    bundle((30, 76), (128, 76), 26, 1)
    bundle((120, 76), (142, 30), 14, 2); bundle((136, 34), (160, 46), 12, 3)
    bundle((30, 72), (12, 98), 8, 4)
    for x, y in ((48, 76), (100, 76), (128, 58), (140, 36)): line(img, [(x - 3, y - 14), (x + 3, y + 14)], '#b8322a', 3.4)
    ell(img, (144, 34, 149, 39), '#1a1410')
    volume(img, (8, 26, 160, 142), .45, .2)
    return done(img)


def i_wreath():
    img = I.canvas(156, 164); rnd = random.Random(6)
    line(img, [(78, 0), (78, 14)], '#5a3e28', 1.4)
    arc(img, (22, 18, 134, 130), 0, 360, '#5a3e28', 5)
    cols = ['#c8642a', '#b8402a', '#d89a3a', '#6a8a3a', '#a85a2a', '#8a9a3a']
    for k in range(22):
        a = k / 22 * 2 * math.pi; x, y = 78 + 54 * math.cos(a), 74 + 54 * math.sin(a)
        leaf(img, x, y, rnd.uniform(24, 32), a + math.pi / 2 + rnd.uniform(-.5, .5), cols[k % len(cols)], 40 + k, k % 3 == 0)
    for a in (2.2, 2.5, .6):
        x, y = 78 + 52 * math.cos(a), 74 + 52 * math.sin(a); fill(img, '#9a6a3a', int(a * 10), ell=(x - 6, y - 4, x + 6, y + 10), scale=1); ell(img, (x - 7, y - 7, x + 7, y + 1), '#5a4228')
    poly(img, [(70, 124), (86, 124), (98, 160), (88, 156), (78, 132), (68, 156), (58, 160)], '#b8322a')
    ell(img, (70, 118, 86, 132), '#c8322a')
    return done(img)


def i_shells():
    img = I.canvas(92, 196)
    line(img, [(46, 0), (46, 176)], '#d8cfbf', 1.2)
    fill(img, '#c9a24a', 1, ell=(36, 10, 56, 32), scale=2); volume(img, (36, 10, 56, 32), .6, .4, spec=.4); line(img, [(40, 26), (52, 26)], '#5a4020', 1)
    cols = ['#e8b8a8', '#efe0d0', '#d8a8a0', '#f0d8c0', '#e0c0b8']
    for k in range(5):
        y = 48 + k * 26; x = 46 + (10 if k % 2 else -10); c = H(cols[k])
        fill(img, c, 10 + k, poly=[(x - 3, y + 18), (x - 8, y + 14)] + [(x + 15 * math.cos(a), y + 8 + 14 * math.sin(a)) for a in np.linspace(math.pi * .92, math.pi * 2.08, 17)] + [(x + 8, y + 14), (x + 3, y + 18)], scale=1, contrast=.7)
        poly(img, [(x - 6, y + 15), (x + 6, y + 15), (x + 4, y + 20), (x - 4, y + 20)], dk(c, .12))
        for a in np.linspace(math.pi * 1.05, math.pi * 1.95, 7): line(img, [(x, y + 16), (x + 13.5 * math.cos(a), y + 8 + 12.5 * math.sin(a))], dk(c, .22), .7)
        volume(img, (x - 13, y - 6, x + 13, y + 18), .5, .2, spec=.3); line(img, [(46, y + 4), (x, y)], '#d8cfbf', .8)
    fill(img, '#efe6d4', 20, rect=(38, 176, 54, 194), scale=2); text(img, '潮', 46, 185, 10, '#3a5a7a', I.SERIF)
    return done(img)


def i_frame():
    img = I.canvas(152, 168); rnd = random.Random(7)
    line(img, [(76, 0), (30, 26)], '#c8b890', 1); line(img, [(76, 0), (122, 26)], '#c8b890', 1)
    fill(img, '#e8dcc0', 1, rect=(26, 30, 126, 150), scale=4, contrast=.5)                                     # washi backing
    leaf(img, 76, 84, 56, -.3, '#b8402a', 3, True)
    fill(img, '#4a6a2a', 4, ell=(32, 124, 120, 152), scale=2, contrast=1.3); volume(img, (32, 124, 120, 152), .5, .3)
    for (a, b) in (((10, 28), (142, 24)), ((10, 150), (142, 154)), ((24, 10), (28, 166)), ((126, 8), (124, 166))):
        line(img, [a, b], '#5a3e28', 6); line(img, [(a[0] + 1, a[1] - 1), (b[0] + 1, b[1] - 1)], '#7a5a3a', 2)
    for x, y in ((26, 26), (125, 25), (26, 151), (125, 152)):
        for k in range(3): line(img, [(x - 6, y - 4 + k * 3), (x + 6, y + 4 + k * 3 - 6)], '#b8322a', 1.4)
    return done(img)


def i_omamori():
    img = I.canvas(72, 152)
    line(img, [(36, 2), (23, 22), (36, 38), (49, 22), (36, 2)], '#c9a24a', 2)
    body = [(10, 52), (36, 40), (62, 52), (63, 148), (9, 148)]
    fill(img, '#2e4a7a', 1, poly=body, scale=4, contrast=1.1)
    fill(img, '#b8322a', 2, poly=[(10, 92), (36, 92), (36, 148), (9, 148)], scale=3, contrast=1.1)
    fill(img, '#c9a24a', 3, poly=[(36, 110), (63, 104), (63, 148), (36, 148)], scale=3, contrast=1)
    d = ImageDraw.Draw(img)
    for k in range(14): y = 54 + k * 6.6; d.line([(px(35), px(y)), (px(37), px(y + 3))], fill=H('#efe6d4'), width=px(1))
    for k in range(10): x = 12 + k * 5; d.line([(px(x), px(91)), (px(x + 2), px(93))], fill=H('#efe6d4'), width=px(1))
    paw(img, 23, 72, 6, '#efe6d4'); text(img, '猫', 22, 122, 16, '#efe6d4', I.SERIF)
    volume(img, (8, 40, 64, 148), .5, .25)
    return done(img)


def i_kokeshi():
    img = I.canvas(84, 192); floor_shadow(img, 42, 186, 28)
    fill(img, '#d8b888', 1, poly=[(24, 76), (60, 76), (64, 182), (20, 182)], scale=3, stretch=(.4, 2)); volume(img, (20, 76, 64, 182), .55, .35)
    fill(img, '#b8322a', 2, poly=[(23, 96), (61, 96), (63, 160), (21, 160)], scale=3)
    for y in (100, 156): line(img, [(22, y), (62, y)], '#2a1c12', 2)
    for k in range(3): leaf(img, 42 + (k - 1) * 11, 128 + (k % 2) * 8, 14, -1.2 + k, '#e0b84a', 10 + k, True)
    fill(img, '#efe0c8', 3, ell=(14, 14, 70, 80), scale=3, contrast=.4); volume(img, (14, 14, 70, 80), .5, .3, spec=.15)
    for s in (-1, 1): poly(img, [(42 + s * 12, 22), (42 + s * 26, 2), (42 + s * 28, 30)], '#2a2018'); poly(img, [(42 + s * 15, 22), (42 + s * 24, 10), (42 + s * 24, 26)], '#d89090')
    fill(img, '#2a2018', 4, poly=[(16, 40), (22, 18), (42, 12), (62, 18), (68, 40), (56, 28), (42, 34), (28, 28)], scale=2)
    for x in (32, 52): arc(img, (x - 5, 46, x + 5, 54), 200, 340, '#1a1410', 1.4)
    poly(img, [(39, 56), (45, 56), (42, 60)], '#c87070')
    for s in (-1, 1): line(img, [(42 + s * 8, 60), (42 + s * 22, 57)], '#6a5a4a', .6); line(img, [(42 + s * 8, 62), (42 + s * 22, 64)], '#6a5a4a', .6)
    return done(img)


def i_sensu():
    img = I.canvas(196, 132); floor_shadow(img, 98, 126, 70)
    cx, cy, R0, R1 = 98, 122, 22, 112
    for k in range(14):
        a0 = math.pi * (1.1 + .8 * k / 14); a1 = math.pi * (1.1 + .8 * (k + 1) / 14)
        c = H('#ead8b0') if k % 2 else H('#dcc8a0')
        poly(img, [(cx + R0 * math.cos(a0), cy + R0 * math.sin(a0)), (cx + R1 * math.cos(a0), cy + R1 * math.sin(a0)), (cx + R1 * math.cos(a1), cy + R1 * math.sin(a1)), (cx + R0 * math.cos(a1), cy + R0 * math.sin(a1))], c)
    fill(img, '#2a2420', 1, poly=[(70, 52), (78, 40), (88, 48), (100, 46), (110, 40), (116, 54), (114, 74), (72, 74)], scale=2)    # Musya's silhouette
    poly(img, [(80, 44), (84, 30), (90, 44)], '#2a2420'); poly(img, [(102, 44), (108, 30), (112, 46)], '#2a2420')
    line(img, [(114, 70), (130, 60), (134, 46)], '#2a2420', 4)
    ell(img, (126, 24, 146, 44), '#e8c860'); soft(img, lambda d: d.ellipse([px(118), px(16), px(154), px(52)], fill=(240, 220, 140, 60)), 6)
    for k in range(15): a = math.pi * (1.1 + .8 * k / 14); line(img, [(cx, cy), (cx + (R0 + 4) * math.cos(a), cy + (R0 + 4) * math.sin(a))], '#5a3e28', 2.4)
    ell(img, (cx - 5, cy - 5, cx + 5, cy + 5), '#c9a24a')
    volume(img, (cx - R1, cy - R1, cx + R1, cy + 6), .35, .15)
    return done(img)


def i_kendama():
    img = I.canvas(104, 184); floor_shadow(img, 52, 178, 36)
    fill(img, '#7a5a3a', 1, poly=[(46, 70), (58, 70), (56, 176), (48, 176)], scale=3, stretch=(.3, 3)); volume(img, (46, 70, 58, 176), .5, .3)
    fill(img, '#6a4a2e', 2, rect=(16, 66, 88, 78), scale=3, stretch=(3, .3)); volume(img, (16, 66, 88, 78), .5, .3)
    for x in (16, 88): fill(img, '#5a3e28', x, ell=(x - 10, 56, x + 10, 84), scale=2); arc(img, (x - 8, 58, x + 8, 66), 200, 340, '#3a2818', 1)
    line(img, [(52, 110), (82, 84), (72, 40)], '#e8dcc0', 1)
    fill(img, '#9a6a3a', 3, ell=(48, 18, 96, 62), scale=2, contrast=.6); volume(img, (48, 18, 96, 62), .6, .35, spec=.4)        # acorn ball
    fill(img, '#5a4228', 4, ell=(44, 2, 100, 34), scale=1, contrast=1.6); line(img, [(72, 2), (76, -2)], '#4a3420', 3)
    return done(img)


def i_kinchaku():
    img = I.canvas(112, 132); floor_shadow(img, 56, 126, 44); c = H('#7a3a5a')
    fill(img, c, 1, poly=[(28, 40), (84, 40), (100, 82), (92, 122), (20, 122), (12, 82)], scale=4, contrast=1)
    d = ImageDraw.Draw(img)
    for k in range(5):
        for j in range(4):
            x, y = 26 + k * 15 + (j % 2) * 7, 58 + j * 15
            d.polygon([(px(x), px(y - 4)), (px(x + 4), px(y)), (px(x), px(y + 4)), (px(x - 4), px(y))], fill=H('#e8a0b6'))
    fill(img, c, 2, poly=[(26, 22), (40, 34), (56, 20), (72, 34), (86, 22), (84, 44), (28, 44)], scale=3)
    line(img, [(26, 44), (86, 44)], dk(c, .4), 2)
    line(img, [(34, 46), (56, 50), (78, 46)], '#e0b84a', 2.4); line(img, [(56, 50), (50, 76)], '#e0b84a', 2); line(img, [(56, 50), (64, 78)], '#e0b84a', 2)
    ell(img, (46, 74, 54, 82), '#e0b84a'); ell(img, (60, 76, 68, 84), '#e0b84a')
    volume(img, (12, 20, 100, 122), .5, .3)
    return done(img)


def i_furin():
    img = I.canvas(92, 196); c = H('#a8603a')
    line(img, [(46, 0), (46, 14)], '#3a2618', 1.4)
    fill(img, c, 1, poly=[(46, 14), (66, 22), (76, 46), (78, 76), (14, 76), (16, 46), (26, 22)], scale=3, contrast=1.1)
    fill(img, '#2a4a5a', 2, poly=[(46, 14), (60, 19), (66, 30), (26, 30), (32, 19)], scale=2)                                   # glazed top
    paw(img, 46, 54, 8, '#efe6d4')
    for x in (24, 68): ell(img, (x - 3, 62, x + 3, 68), '#efe6d4')
    volume(img, (14, 14, 78, 76), .6, .35, spec=.2)
    line(img, [(46, 70), (46, 132)], '#d8cfbf', 1)
    ell(img, (41, 82, 51, 92), '#5a3e28')
    fill(img, '#efe6d4', 3, rect=(32, 132, 60, 192), scale=3, contrast=.5); text(img, '音', 46, 152, 14, '#2a4a5a', I.SERIF)
    paw(img, 46, 176, 5, '#a8603a')
    return done(img)


def i_mizuhiki():
    img = I.canvas(124, 152)
    line(img, [(62, 0), (62, 22)], '#c9a24a', 1.4)
    def knot(col, off, w):
        pts = []
        for k in range(120):
            t = k / 119 * 2 * math.pi; x = 62 + 42 * math.sin(t) + off; y = 66 + 26 * math.sin(2 * t) + 20 * math.cos(t) * .6
            pts.append((x, y))
        line(img, pts, col, w)
    for off, col in ((-3, '#efe6d4'), (0, '#c8322a'), (3, '#c9a24a')): knot(col, off, 2.4)
    for k, col in enumerate(('#efe6d4', '#c8322a', '#c9a24a')):
        line(img, [(56 + k * 3, 92), (40 + k * 4, 140)], col, 2); line(img, [(66 + k * 3, 92), (84 + k * 4, 140)], col, 2)
    pts = [(62, 96), (70, 118), (76, 146), (66, 140), (58, 118)]
    fill(img, '#d8d4cc', 4, poly=pts, scale=2, contrast=.5); line(img, [(62, 96), (70, 148)], '#8a8478', 1)
    return done(img)


def i_hokora():
    img = I.canvas(172, 192); floor_shadow(img, 86, 186, 76)
    fill(img, '#6a6660', 1, rect=(20, 160, 152, 184), scale=3, contrast=1.2); volume(img, (20, 160, 152, 184), .5, .3)   # stone base
    fill(img, '#7a5a3a', 2, rect=(40, 84, 132, 160), scale=3, stretch=(.4, 3)); volume(img, (40, 84, 132, 160), .5, .3)
    fill(img, '#1a120c', 3, rect=(58, 100, 114, 156), scale=2)
    soft(img, lambda d: d.ellipse([px(70), px(112), px(102), px(150)], fill=(255, 190, 110, 120)), 6)
    fill(img, '#efe6d4', 4, ell=(76, 128, 96, 150), scale=1); text(img, '神', 86, 120, 12, '#c9a24a', I.SERIF)
    poly(img, [(8, 92), (86, 30), (164, 92), (150, 96), (86, 46), (22, 96)], '#3a2a1c')
    fill(img, '#4a3626', 5, poly=[(14, 88), (86, 34), (158, 88), (86, 80)], scale=3, stretch=(3, .4))
    fill(img, '#5a7a32', 6, poly=[(30, 80), (60, 54), (86, 40), (112, 54), (142, 80), (100, 72), (70, 74)], scale=2, contrast=1.4, dark=.5, light=.35)
    line(img, [(48, 96), (124, 96)], '#d8c8a0', 3)
    for x in (62, 86, 110): poly(img, [(x - 4, 96), (x + 4, 96), (x + 1, 104), (x + 5, 104), (x - 1, 114), (x - 3, 104)], '#efe6d4')
    fill(img, '#a8603a', 7, ell=(140, 140, 160, 162), scale=1); poly(img, [(142, 142), (146, 132), (150, 142)], '#a8603a'); poly(img, [(150, 142), (154, 132), (158, 142)], '#a8603a')
    return done(img)


def i_hotaru():
    img = I.canvas(112, 172); floor_shadow(img, 56, 166, 42)
    soft(img, lambda d: d.ellipse([px(18), px(48), px(94), px(150)], fill=(200, 240, 120, 70)), 10)
    fill(img, '#d8d0a8', 1, rect=(22, 50, 90, 152), scale=3, contrast=.4, dark=.2)
    a = np.asarray(img, np.float32); a[px(50):px(152), px(22):px(90), 3] *= .8; img = Image.fromarray(a.astype(np.uint8), 'RGBA')
    rnd = random.Random(9)
    for _ in range(7):
        x, y = rnd.uniform(32, 80), rnd.uniform(66, 140)
        soft(img, lambda d, x=x, y=y: d.ellipse([px(x - 6), px(y - 6), px(x + 6), px(y + 6)], fill=(220, 255, 120, 200)), 3); ell(img, (x - 1.6, y - 1.6, x + 1.6, y + 1.6), '#f8ffd0')
    for x in (22, 46, 66, 90): line(img, [(x, 46), (x, 154)], '#6a4a2e', 2.6 if x in (22, 90) else 1.2)
    for y in (48, 152): line(img, [(16, y), (96, y)], '#5a3e28', 5)
    line(img, [(28, 46), (56, 14), (84, 46)], '#5a3e28', 2.4); ell(img, (52, 10, 60, 18), '#5a3e28')
    for x, y in ((22, 48), (90, 48), (22, 152), (90, 152)):
        for k in range(2): line(img, [(x - 4, y - 3 + k * 3), (x + 4, y + k * 3)], '#b8322a', 1.2)
    return done(img)


THINGS = [('ws_chochin', i_chochin, 't'), ('ws_kaeru', i_kaeru, 'b'), ('ws_teru', i_teru, 't'), ('ws_uma', i_uma, 'b'), ('ws_wreath', i_wreath, 't'),
          ('ws_shells', i_shells, 't'), ('ws_frame', i_frame, 't'), ('ws_omamori', i_omamori, 't'), ('ws_kokeshi', i_kokeshi, 'b'), ('ws_sensu', i_sensu, 'b'),
          ('ws_kendama', i_kendama, 'b'), ('ws_kinchaku', i_kinchaku, 'b'), ('ws_furin', i_furin, 't'), ('ws_mizuhiki', i_mizuhiki, 't'),
          ('ws_hokora', i_hokora, 'b'), ('ws_hotaru', i_hotaru, 'b')]

if __name__ == '__main__':
    ims = [('bench', bench(), 'b')] + [('m_' + k, f(), 'i') for k, f in MATS] + [(iid, f(), a) for iid, f, a in THINGS]
    W = 1200; x = y = rowh = 0; pos = {}
    for iid, im, _ in sorted(ims, key=lambda t: -t[1].height):
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[iid] = (x, y, im.width, im.height); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for iid, im, _ in ims: at.paste(im, pos[iid][:2])
    at.save(os.path.join(ASSETS, 'items', 'atlas_ws.webp'), 'WEBP', quality=88, alpha_quality=92, method=6)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'out'), exist_ok=True)
    pv = Image.new('RGBA', at.size, (34, 30, 28, 255)); pv.alpha_composite(at); pv.convert('RGB').save(os.path.join(os.path.dirname(__file__), 'out', 'atlas_ws.png'))
    print(json.dumps({'size': [W, y + rowh], 'at': {iid: list(pos[iid]) + [a] for iid, _, a in ims}}, separators=(',', ':')))
