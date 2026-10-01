#!/usr/bin/env python3
"""«Тысяча журавликов» (senbazuru): small paper cranes in 10 colours for the hanging strings, 6 washi/chiyogami
paper swatches for the folding game, and 4 milestone things (paper box, a 100-crane garland, a crane fūrin, the golden crane).
Same spline toolkit as birthday_art.py / story_art.py.
Usage: python3 art/cranes_art.py  → assets/items/atlas_cr.webp (+ art/out/cranes_preview.png); prints the rect map."""
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

PREV = os.path.join(ROOT, 'art/out'); os.makedirs(PREV, exist_ok=True)
W_, BLK = (255, 255, 255, 255), (0, 0, 0, 255)
COLS = ['#c8322c', '#e0663a', '#e6a2b4', '#e2b040', '#efe6d2', '#6a9a58', '#3a8a8a', '#3d5f9e', '#2c3466', '#7a4a8a']
LAC, GOLD = (26, 18, 16, 255), hexc('#d8b048')


def finish(img, seed, blur=.45):
    out = img.resize((P.W, P.H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(out, np.float32); n = np.random.default_rng(seed).normal(0, 4, a.shape[:2])[..., None]
    a[..., :3] = np.clip(a[..., :3] + n, 0, 255); return Image.fromarray(a.astype(np.uint8), 'RGBA')


def facet(img, col, pts, lt, seed):   # one flat paper facet: lt>0 lighter, lt<0 darker
    c = mixc(col, W_ if lt > 0 else BLK, abs(lt))
    return shape(img, c, seed, pts, scale=2, contrast=.35, dk=.12, lt=.08, k=.35, rim=.05, smooth=False, feather=.2)


def crease(img, a, b, col=(255, 255, 255, 70), w=.6):
    d = ImageDraw.Draw(img); d.line([(px(a[0]), px(a[1])), (px(b[0]), px(b[1]))], fill=col, width=max(1, px(w)))


def crane_at(img, col, ox, oy, s=1.0, seed=1, flip=False):
    """A folded crane in 3/4 view (neck up-left with the head, tail up-right, wings spread), fitted in 72×46 at s=1."""
    f = (lambda x, y: (ox + (72 - x if flip else x) * s, oy + y * s))
    P_ = lambda pts: [f(*p) for p in pts]
    facet(img, col, P_([(36, 25), (63, 9), (52, 27)]), -.32, seed)            # far wing
    facet(img, col, P_([(44, 26), (49, 27), (67, 5), (65, 5)]), -.12, seed + 1)  # tail
    facet(img, col, P_([(22, 27), (36, 20), (52, 27), (36, 35)]), .0, seed + 2)  # body
    facet(img, col, P_([(36, 20), (52, 27), (36, 35)]), -.18, seed + 3)          # body shadow side
    facet(img, col, P_([(24, 28), (29, 26), (9, 6), (7, 7)]), .1, seed + 4)      # neck
    facet(img, col, P_([(7, 6), (11, 8), (3, 14)]), -.05, seed + 5)              # head
    facet(img, col, P_([(27, 28), (45, 28), (24, 45)]), .22, seed + 6)           # near wing (lit)
    crease(img, f(36, 28), f(26, 43)); crease(img, f(36, 20), f(36, 35), (0, 0, 0, 60), .5)


def string_crane(i):
    img = canvas(72, 46); crane_at(img, hexc(COLS[i]), 0, 0, 1, 10 + i * 7); return finish(img, 3 + i, .35)


# ───────────── washi / chiyogami swatches (the paper the player folds) ─────────────
def washi(base, seed):
    img = canvas(160, 160)
    shape(img, base, seed, [(-4, -4), (164, -4), (164, 164), (-4, 164)], scale=6, contrast=.5, dk=.18, lt=.1, k=.1, rim=0, smooth=False, feather=0)
    rnd = random.Random(seed); d = ImageDraw.Draw(img)
    for _ in range(70):   # paper fibres
        x, y, a, L = rnd.uniform(0, 160), rnd.uniform(0, 160), rnd.uniform(0, math.pi), rnd.uniform(4, 14)
        d.line([(px(x), px(y)), (px(x + math.cos(a) * L), px(y + math.sin(a) * L))], fill=(255, 255, 255, 26), width=1)
    return img


def sw_asanoha():
    img = washi(hexc('#2c3a66'), 1); d = ImageDraw.Draw(img); c = (226, 220, 200, 200); w = px(.9)
    s = 40; h = s * math.sqrt(3) / 2
    for r in range(-1, 6):
        for q in range(-1, 6):
            cx = q * s + (s / 2 if r % 2 else 0); cy = r * h
            pts = [(cx + math.cos(a) * s / math.sqrt(3), cy + math.sin(a) * s / math.sqrt(3)) for a in [math.pi / 6 + k * math.pi / 3 for k in range(6)]]
            for p in pts: d.line([(px(cx), px(cy)), (px(p[0]), px(p[1]))], fill=c, width=w)
            for k in range(6): d.line([(px(pts[k][0]), px(pts[k][1])), (px(pts[(k + 1) % 6][0]), px(pts[(k + 1) % 6][1]))], fill=c, width=w)
    return finish(img, 11, .3)


def sw_seigaiha():
    img = washi(hexc('#2e7a82'), 2); d = ImageDraw.Draw(img); R = 22
    for r in range(-1, 16):
        for q in range(-1, 6):
            cx = q * R * 2 + (R if r % 2 else 0); cy = r * R * .55
            for k, rr in enumerate((R, R * .76, R * .52, R * .28)):
                d.pieslice([px(cx - rr), px(cy - rr), px(cx + rr), px(cy + rr)], 180, 360, fill=(46, 122, 130, 255) if k % 2 == 0 else (214, 226, 214, 235))
    return finish(img, 12, .3)


def sw_sakura():
    img = washi(hexc('#d98aa0'), 3); d = ImageDraw.Draw(img); rnd = random.Random(5)
    for _ in range(16):
        x, y, r = rnd.uniform(0, 160), rnd.uniform(0, 160), rnd.uniform(7, 12); a0 = rnd.uniform(0, 1)
        for k in range(5):
            a = a0 + k * math.tau / 5; ex, ey = x + math.cos(a) * r * .62, y + math.sin(a) * r * .62
            d.ellipse([px(ex - r * .42), px(ey - r * .42), px(ex + r * .42), px(ey + r * .42)], fill=(250, 226, 230, 235))
        d.ellipse([px(x - r * .2), px(y - r * .2), px(x + r * .2), px(y + r * .2)], fill=(200, 70, 90, 255))
    return finish(img, 13, .35)


def sw_ichimatsu():
    img = washi(hexc('#b8322a'), 4); d = ImageDraw.Draw(img)
    for r in range(8):
        for q in range(8):
            if (r + q) % 2: d.rectangle([px(q * 20), px(r * 20), px(q * 20 + 20), px(r * 20 + 20)], fill=(236, 222, 196, 235))
    return finish(img, 14, .3)


def sw_kikko():
    img = washi(hexc('#7a4a8a'), 5); d = ImageDraw.Draw(img); s = 18; c = (226, 190, 96, 230)
    for r in range(-1, 8):
        for q in range(-1, 7):
            cx = q * s * 1.5 * 2 + (s * 1.5 if r % 2 else 0); cy = r * s * math.sqrt(3) / 2 * 1.0 * 2
            pts = [(cx + math.cos(k * math.pi / 3) * s, cy + math.sin(k * math.pi / 3) * s) for k in range(6)]
            d.polygon([(px(x), px(y)) for x, y in pts], outline=c, width=px(1.2))
            d.ellipse([px(cx - 3), px(cy - 3), px(cx + 3), px(cy + 3)], fill=c)
    return finish(img, 15, .3)


def sw_kinpaku():
    img = washi(hexc('#3c6a4a'), 6); d = ImageDraw.Draw(img); rnd = random.Random(9)
    for _ in range(60):
        x, y, r = rnd.uniform(0, 160), rnd.uniform(0, 160), rnd.uniform(1, 4)
        d.polygon([(px(x + math.cos(a) * r * rnd.uniform(.6, 1.3)), px(y + math.sin(a) * r * rnd.uniform(.6, 1.3))) for a in [k * 1.2 for k in range(5)]], fill=(232, 196, 100, 230))
    return finish(img, 16, .35)


# ───────────── milestone things ─────────────
def shadow(img, cx, y, rx, a=90):
    soft(img, lambda d: d.ellipse([px(cx - rx), px(y - rx * .16), px(cx + rx), px(y + rx * .16)], fill=(0, 0, 0, a)), 3)


def paperbox():   # 100: a lacquer box with a stack of chiyogami squares and one crane on top
    img = canvas(190, 140); shadow(img, 95, 132, 86)
    shape(img, hexc('#5a1a16'), 101, [(20, 52), (108, 20), (178, 46), (178, 58), (90, 92), (20, 66)], scale=4, k=.6, rim=.2, spec=.25, smooth=False, feather=.3)   # open lid behind
    shape(img, LAC, 102, [(12, 74), (100, 50), (182, 72), (182, 112), (94, 134), (12, 112)], scale=4, k=.6, rim=.3, spec=.2, smooth=False, feather=.3)
    shape(img, hexc('#2a1a14'), 103, [(12, 74), (94, 98), (94, 134), (12, 112)], scale=4, k=.5, rim=.2, smooth=False, feather=.3)
    for k, c in enumerate(['#efe6d2', '#3d5f9e', '#e6a2b4', '#e2b040', '#c8322c']):   # paper stack
        y = 66 - k * 3.2
        facet(img, hexc(c), [(24, y + 8), (100, y - 14), (170, y + 6), (94, y + 30)], .05 * k, 104 + k)
    d = ImageDraw.Draw(img)
    d.line([(px(12), px(74)), (px(94), px(98)), (px(182), px(72))], fill=(200, 160, 80, 200), width=px(1.6))
    crane_at(img, hexc('#c8322c'), 64, 22, .9, 120)
    return finish(img, 21)


def garland():   # 250: a short senbazuru bundle (five strings) to hang
    img = canvas(130, 330); d = ImageDraw.Draw(img)
    shape(img, hexc('#c8a050'), 201, ell=(52, 2, 78, 20), scale=2, k=.6, rim=.3, spec=.4, feather=.3)
    for k in range(5):
        x = 22 + k * 21.5
        d.line([(px(65), px(12)), (px(x), px(36))], fill=(210, 190, 150, 220), width=px(1))
        d.line([(px(x), px(36)), (px(x), px(300))], fill=(230, 214, 180, 200), width=px(.7))
        for j in range(15):
            ci = (j // 3 + k * 2) % len(COLS); y = 36 + j * 17
            crane_at(img, hexc(COLS[ci]), x - 15, y - 2, .42, 300 + k * 20 + j, flip=(j + k) % 2 == 1)
        for t in range(4): d.line([(px(x), px(296)), (px(x - 3 + t * 2), px(318))], fill=(196, 50, 44, 230), width=px(1))
        shape(img, hexc('#c8322c'), 210 + k, ell=(x - 3, 292, x + 3, 300), scale=2, k=.5, rim=.2, feather=.3)
    return finish(img, 22)


def furin():   # 500: a glass wind bell with a red crane on it and a paper strip
    img = canvas(110, 250); d = ImageDraw.Draw(img)
    d.line([(px(55), px(0)), (px(55), px(22))], fill=(210, 190, 150, 230), width=px(1))
    m = shape(img, hexc('#b8d0d8', 200), 301, [(26, 70), (32, 34), (55, 22), (78, 34), (84, 70)], scale=3, k=.6, rim=.5, spec=.6, feather=.4)
    crane_at(img, hexc('#c8322c'), 30, 40, .68, 302)
    soft(img, lambda dd: dd.ellipse([px(30), px(26), px(46), px(40)], fill=(255, 255, 255, 120)), 1.5)
    d.ellipse([px(26), px(64), px(84), px(76)], outline=(150, 180, 190, 220), width=px(1.2))
    d.line([(px(55), px(70)), (px(55), px(120))], fill=(196, 50, 44, 230), width=px(1))
    shape(img, hexc('#c8322c'), 303, ell=(51, 84, 59, 92), scale=2, k=.6, rim=.3, spec=.4, feather=.3)
    shape(img, hexc('#efe6d2'), 304, [(40, 120), (70, 120), (70, 238), (40, 238)], scale=4, k=.4, rim=.15, smooth=False, feather=.3)
    crane_at(img, hexc('#3d5f9e'), 41, 140, .4, 305)
    crane_at(img, hexc('#e6a2b4'), 41, 182, .4, 306, flip=True)
    return finish(img, 23)


def goldcrane():   # 1000: the golden crane of the wish on a lacquer stand
    img = canvas(230, 200); shadow(img, 115, 190, 96)
    shape(img, LAC, 401, [(26, 160), (204, 160), (196, 186), (34, 186)], scale=4, k=.6, rim=.3, spec=.3, smooth=False, feather=.3)
    shape(img, hexc('#9a2a22'), 402, [(30, 156), (200, 156), (204, 164), (26, 164)], scale=3, k=.4, rim=.1, smooth=False, feather=.3)
    soft(img, lambda d: d.ellipse([px(40), px(30), px(190), px(150)], fill=(255, 210, 120, 70)), 14)
    crane_at(img, hexc('#d8a838'), 18, 40, 2.7, 403)
    d = ImageDraw.Draw(img); rnd = random.Random(4)
    for _ in range(22):
        x, y = rnd.uniform(40, 190), rnd.uniform(40, 150); d.ellipse([px(x - .8), px(y - .8), px(x + .8), px(y + .8)], fill=(255, 240, 190, 230))
    return finish(img, 24)


if __name__ == '__main__':
    parts = [('k%d' % i, string_crane(i)) for i in range(len(COLS))]
    parts += [('p0', sw_asanoha()), ('p1', sw_seigaiha()), ('p2', sw_sakura()), ('p3', sw_ichimatsu()), ('p4', sw_kikko()), ('p5', sw_kinpaku())]
    parts += [('cr_box', paperbox()), ('cr_garland', garland()), ('cr_furin', furin()), ('cr_gold', goldcrane())]
    AW, gap = 1000, 4; x = y = rowh = 0; rects = {}
    for name, p in parts:   # shelf packing
        if x + p.width > AW: x = 0; y += rowh + gap; rowh = 0
        rects[name] = [x, y, p.width, p.height]; x += p.width + gap; rowh = max(rowh, p.height)
    AH = y + rowh
    atlas = Image.new('RGBA', (AW, AH), (0, 0, 0, 0))
    for name, p in parts: atlas.alpha_composite(p, tuple(rects[name][:2]))
    f = os.path.join(ROOT, 'assets/items/atlas_cr.webp')
    atlas.save(f, 'WEBP', quality=88, alpha_quality=92, method=6)
    pv = Image.new('RGBA', (AW, AH), (46, 44, 52, 255)); pv.alpha_composite(atlas); pv.save(os.path.join(PREV, 'cranes_preview.png'))
    print('atlas', AW, AH, os.path.getsize(f), json.dumps(rects))
