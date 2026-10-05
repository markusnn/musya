#!/usr/bin/env python3
"""«Кимодамэси» (肝試し, the night test of courage): four keepsakes of the walk to the little shrine —
an ofuda of courage, a candle in a paper lantern on a stand, an omamori charm, juzu prayer beads.
Same painted toolkit as candles_art.py / story_art.py. One atlas.
Usage: python3 art/kimodameshi_art.py → assets/items/atlas_km.webp (+ art/out/kimodameshi_preview.png); prints the JS rect map."""
import json, math, os, random, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from candles_art import finish, stroke, flame, candle, PREV          # sets argv for monsters.py, same toolkit
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc, fbm
from monsters import canvas, px, soft
from story_art import shape, clipped, poly_s, cr
from items import text, SERIF

INK = (24, 18, 16)


def ofuda():   # a paper talisman on a cord: 勇 (courage), 守護, a vermilion seal
    img = canvas(90, 250); d = ImageDraw.Draw(img)
    stroke(d, [(45, 0), (44, 14), (45, 30)], (120, 30, 26, 255), 2.2)
    for sx in (-1, 1): stroke(d, [(45, 30), (45 + sx * 16, 36)], (120, 30, 26, 255), 2)
    m = shape(img, (226, 216, 190, 255), 11, [(14, 34), (76, 34), (77, 244), (13, 244)], scale=6, contrast=.6, dk=.25, lt=.12, k=.4, rim=.25, smooth=False, feather=.4)
    def fold(dd, l):   # faint fibres and a darker top fold
        r = random.Random(3)
        for _ in range(40):
            y = r.uniform(36, 242); x = r.uniform(15, 70); dd.line([(px(x), px(y)), (px(x + r.uniform(3, 9)), px(y + r.uniform(-1, 1)))], fill=(150, 130, 100, 60), width=px(.6))
        dd.rectangle([px(13), px(34), px(77), px(46)], fill=(196, 180, 150, 120))
    clipped(img, m, fold)
    text(img, '奉', 45, 62, 18, INK, font=SERIF, brush=True)
    text(img, '勇', 45, 106, 44, INK, font=SERIF, brush=True)
    text(img, '守', 45, 152, 22, INK, font=SERIF, brush=True)
    text(img, '護', 45, 178, 22, INK, font=SERIF, brush=True)
    sl = Image.new('RGBA', img.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(sl)
    dd.rounded_rectangle([px(32), px(198), px(58), px(224)], px(2), fill=(186, 40, 30, 215))
    dd.rounded_rectangle([px(35), px(201), px(55), px(221)], px(1.5), outline=(240, 200, 180, 160), width=px(1.2))
    img.alpha_composite(sl.filter(ImageFilter.GaussianBlur(.5 * px(1))))
    text(img, '肝', 45, 211, 13, (250, 222, 204), font=SERIF)
    return finish(img, 21)


def lantern():   # a small chōchin with a candle inside, hanging from a bent stand
    img = canvas(150, 230); d = ImageDraw.Draw(img)
    wood = (70, 46, 30, 255)
    shape(img, wood, 31, [(22, 206), (128, 206), (132, 226), (18, 226)], scale=4, k=.6, rim=.3, smooth=False, spec=.12)
    shape(img, wood, 32, [(36, 50), (44, 50), (45, 208), (35, 208)], scale=4, k=.6, rim=.3, smooth=False, spec=.15)
    stroke(d, [(40, 52), (70, 40), (104, 40), (112, 48)], (62, 40, 26, 255), 5)
    stroke(d, [(110, 48), (110, 74)], (30, 22, 18, 255), 1.4)
    cx, cy, rx, ry = 110, 128, 31, 44
    soft(img, lambda dd: dd.ellipse([px(cx - 30), px(cy - 58), px(cx + 30), px(cy + 58)], fill=(255, 176, 90, 60)), 6)
    m = shape(img, (226, 150, 78, 255), 33, ell=(cx - rx, cy - ry, cx + rx, cy + ry), scale=4, contrast=.5, dk=.35, lt=.4, k=.2, rim=.55, spec=0)
    def ribs(dd, l):
        for k in range(-6, 7):
            y = cy + k * ry / 7; w = rx * math.sqrt(max(0, 1 - (k / 7) ** 2)) + 2
            dd.line([(px(cx - w), px(y)), (px(cx + w), px(y))], fill=(120, 60, 24, 110), width=px(1))
        dd.ellipse([px(cx - 12), px(cy - 4), px(cx + 12), px(cy + 30)], fill=(255, 236, 170, 120))
    clipped(img, m, ribs)
    soft(img, lambda dd: dd.ellipse([px(cx - 9), px(cy + 2), px(cx + 9), px(cy + 26)], fill=(255, 246, 210, 160)), 4)
    text(img, '肝', cx, cy - 8, 22, (60, 22, 12), font=SERIF, brush=True)
    for y0, y1 in ((cy - ry - 5, cy - ry + 5), (cy + ry - 5, cy + ry + 5)):
        shape(img, (24, 18, 16, 255), 34 + y0, [(cx - 19, y0), (cx + 19, y0), (cx + 19, y1), (cx - 19, y1)], scale=4, k=.5, rim=.2, smooth=False, spec=.2)
    return finish(img, 35)


def omamori():   # a brocade charm pouch with an agemaki knot
    img = canvas(100, 190); d = ImageDraw.Draw(img)
    cord = (196, 160, 70, 255)
    stroke(d, [(50, 52), (40, 26), (50, 4), (60, 26), (50, 52)], cord, 2.4)
    pts = [(24, 66), (50, 52), (76, 66), (80, 176), (20, 176)]
    m = shape(img, (128, 30, 40, 255), 41, pts, scale=5, contrast=.7, dk=.45, lt=.2, k=.55, rim=.35, smooth=False, feather=.5, spec=.12)
    def brocade(dd, l):
        for j, y in enumerate(range(70, 178, 14)):
            for i, x in enumerate(range(18 + (j % 2) * 8, 84, 16)):
                dd.ellipse([px(x - 3), px(y - 3), px(x + 3), px(y + 3)], outline=(210, 170, 80, 150), width=px(.9))
                dd.line([(px(x), px(y - 5)), (px(x), px(y + 5))], fill=(210, 170, 80, 90), width=px(.6))
        dd.rectangle([px(36), px(84), px(64), px(160)], fill=(238, 226, 196, 235))
    clipped(img, m, brocade)
    text(img, '御', 50, 102, 18, (128, 30, 40), font=SERIF)
    text(img, '守', 50, 140, 18, (128, 30, 40), font=SERIF)
    for k, (dx, dy) in enumerate(((-7, -4), (7, -4), (0, 3), (0, -9))):
        shape(img, cord, 42 + k, ell=(50 + dx - 6, 56 + dy - 5, 50 + dx + 6, 56 + dy + 5), scale=3, k=.6, rim=.3, spec=.25)
    return finish(img, 45)


def juzu():   # prayer beads on a small purple cushion
    img = canvas(190, 120)
    shape(img, (78, 52, 96, 255), 51, [(14, 84), (100, 62), (178, 84), (100, 114)], scale=6, contrast=.7, dk=.45, lt=.2, k=.5, rim=.35, feather=.8, spec=.08)
    loop = cr([(56, 74), (96, 62), (140, 70), (150, 86), (110, 98), (64, 96), (44, 86)], 12, True)
    L = [0]
    for a, b in zip(loop, loop[1:] + loop[:1]): L.append(L[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    n = 30; step = L[-1] / n; beads = []
    for i in range(n):
        s = i * step; j = max(k for k in range(len(L) - 1) if L[k] <= s); a, b = loop[j], loop[(j + 1) % len(loop)]; t = (s - L[j]) / max(1e-6, L[j + 1] - L[j])
        beads.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    for i, (x, y) in enumerate(sorted(beads, key=lambda p: p[1])):
        r = 5.2
        shape(img, (96, 54, 30, 255), 60 + i, ell=(x - r, y - r, x + r, y + r), scale=2, contrast=.5, k=.8, rim=.5, spec=.35, feather=.3)
    d = ImageDraw.Draw(img)
    stroke(d, [(110, 98), (118, 104), (132, 104)], (60, 36, 70, 255), 2)
    shape(img, (110, 66, 38, 255), 91, ell=(102, 90, 118, 106), scale=2, k=.8, rim=.5, spec=.4, feather=.3)
    for k in range(9):
        stroke(d, [(132, 104), (140 + k * .8, 108 + k * .3), (150 + k * 1.2, 112 + k * .2)], (96, 60, 120, 230), 1.1)
    shape(img, (96, 60, 120, 255), 92, ell=(126, 99, 138, 109), scale=2, k=.6, rim=.4, spec=.2)
    return finish(img, 55)


if __name__ == '__main__':
    parts = [('km_ofuda', ofuda()), ('km_lantern', lantern()), ('km_omamori', omamori()), ('km_juzu', juzu())]
    gap = 4; AW = sum(p.width for _, p in parts) + gap * (len(parts) - 1); AH = max(p.height for _, p in parts)
    atlas = Image.new('RGBA', (AW, AH), (0, 0, 0, 0)); rects = {}; x = 0
    for name, p in parts: atlas.alpha_composite(p, (x, 0)); rects[name] = [x, 0, p.width, p.height]; x += p.width + gap
    atlas.save(os.path.join(ROOT, 'assets/items/atlas_km.webp'), 'WEBP', quality=88, alpha_quality=92, method=6)
    pv = Image.new('RGBA', (AW * 2, AH * 2), (40, 38, 44, 255)); pv.alpha_composite(atlas.resize((AW * 2, AH * 2), Image.LANCZOS)); pv.save(os.path.join(PREV, 'kimodameshi_preview.png'))
    print('atlas', AW, AH, json.dumps(rects))
