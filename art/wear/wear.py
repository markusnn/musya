#!/usr/bin/env python3
"""Painted clothes for Musya (same toolkit as the room items). Sizes are in cat-frame pixels (384×416 frame).
Usage: wear.py <outdir> → <outdir>/<id>.webp + wear.json"""
import json, math, random, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc
import items as I
from items import px, canvas, fill, volume, soft, line, ell, poly, text, H, dk, lt, SERIF

OUT = sys.argv[1]; META = {}


def save(img, name):
    out = img.resize((P.W, P.H), Image.LANCZOS)
    out.save(f'{OUT}/{name}.webp', 'WEBP', quality=88, alpha_quality=92, method=6)
    META[name] = [P.W, P.H]; print(name, P.W, P.H)


def flower(img, x, y, r, col, center='#e8c040', n=5, seed=0):
    d = ImageDraw.Draw(img); c = H(col)
    for k in range(n):
        a = k / n * math.tau - math.pi / 2; ex, ey = x + math.cos(a) * r * .62, y + math.sin(a) * r * .62
        d.ellipse([px(ex - r * .55), px(ey - r * .55), px(ex + r * .55), px(ey + r * .55)], fill=c)
    d.ellipse([px(x - r * .3), px(y - r * .3), px(x + r * .3), px(y + r * .3)], fill=H(center))
    volume(img, (x - r * 1.2, y - r * 1.2, x + r * 1.2, y + r * 1.2), .5, .3)


# ───────────── head ─────────────
def kabuto():
    img = canvas(190, 150)
    fill(img, '#1f1c22', 3, poly=[(20, 120), (170, 120), (178, 138), (12, 138)], scale=5, contrast=1.2)          # neck guard
    for k in range(3): ImageDraw.Draw(img).line([(px(14), px(124 + k * 5)), (px(176), px(124 + k * 5))], fill=H('#b8322a'), width=px(1.4))
    fill(img, '#2a2630', 4, ell=(36, 50, 154, 136), scale=5, contrast=1.3)                                          # bowl
    d = ImageDraw.Draw(img)
    for k in range(9): a = math.pi * (1.1 + .8 * k / 8); d.line([(px(95 + math.cos(a) * 56), px(93 + math.sin(a) * 40)), (px(95), px(93))], fill=H('#4a4652'), width=px(1.4))
    volume(img, (36, 50, 154, 136), .6, .4, spec=.35)
    fill(img, '#d8b048', 5, poly=[(95, 60), (40, 4), (56, 2), (95, 46), (134, 2), (150, 4)], scale=4, contrast=1.3)   # kuwagata horns
    ell(img, (84, 52, 106, 74), '#d8b048'); volume(img, (40, 2, 150, 74), .5, .2, spec=.4)
    save(img, 'w_kabuto')


def eboshi():
    img = canvas(90, 150)
    fill(img, '#15131a', 3, poly=[(14, 146), (76, 146), (70, 60), (50, 8), (30, 14), (20, 60)], scale=5, contrast=1.2)
    d = ImageDraw.Draw(img)
    for k in range(6): d.line([(px(22 + k * 2), px(140 - k * 18)), (px(70 - k * 3), px(138 - k * 18))], fill=H('#2a2830'), width=px(1.2))
    line(img, [(14, 140), (-4, 150)], '#f0ece0', 1.6); line(img, [(76, 140), (94, 150)], '#f0ece0', 1.6)
    volume(img, (14, 8, 76, 146), .5, .3, spec=.2)
    save(img, 'w_eboshi')


def tsunokakushi():
    img = canvas(200, 100)
    fill(img, '#c02a2a', 3, poly=[(24, 86), (176, 86), (170, 96), (30, 96)], scale=4)
    fill(img, '#fbfaf6', 4, poly=[(14, 88), (26, 30), (60, 10), (140, 10), (174, 30), (186, 88), (150, 74), (100, 70), (50, 74)], scale=5, contrast=.35, dark=.12, light=.05)
    d = ImageDraw.Draw(img); d.line([(px(22), px(40)), (px(100), px(26)), (px(178), px(40))], fill=H('#d8b048'), width=px(1.6))
    volume(img, (14, 10, 186, 96), .35, .25)
    save(img, 'w_tsuno')


def sugegasa():
    img = canvas(250, 110)
    fill(img, '#b8975a', 3, poly=[(4, 92), (125, 6), (246, 92), (125, 104)], scale=4, contrast=1.1)
    d = ImageDraw.Draw(img)
    for k in range(15): t = k / 14; d.line([(px(125), px(8)), (px(6 + 238 * t), px(92 + 10 * math.sin(math.pi * t)))], fill=H('#8a6a34'), width=px(1))
    for k in range(4): r = .25 + k * .22; d.arc([px(125 - 121 * r), px(8 + 84 * r - 20 * r), px(125 + 121 * r), px(8 + 84 * r + 20 * r)], 0, 180, fill=H('#9a7a40'), width=px(1))
    volume(img, (4, 6, 246, 104), .45, .2)
    ell(img, (119, 2, 131, 12), '#6a4a22')
    save(img, 'w_sugegasa')


def tenugui():
    img = canvas(170, 80); base = H('#2a4a7a')
    fill(img, base, 3, poly=[(10, 40), (85, 26), (160, 40), (158, 60), (85, 48), (12, 60)], scale=5, contrast=.8)
    d = ImageDraw.Draw(img)
    for k in range(9): x = 16 + k * 17; d.ellipse([px(x - 3), px(44 - abs(x - 85) * .16 - 3), px(x + 3), px(44 - abs(x - 85) * .16 + 3)], fill=H('#e8e0d0'))
    fill(img, base, 4, poly=[(150, 40), (168, 50), (156, 60)], scale=4)
    fill(img, base, 5, poly=[(160, 52), (170, 76), (160, 78), (152, 58)], scale=4); fill(img, base, 6, poly=[(156, 52), (142, 76), (134, 72), (148, 54)], scale=4)
    volume(img, (10, 26, 170, 78), .4, .2)
    save(img, 'w_tenugui')


def kiku_crown():
    img = canvas(180, 70); rnd = random.Random(3)
    line(img, [(10, 50), (90, 34), (170, 50)], '#3f5a3a', 4)
    for k in range(9):
        t = k / 8; x = 12 + 156 * t; y = 50 - 16 * math.sin(math.pi * t)
        flower(img, x, y, 11 + rnd.uniform(-2, 2), rnd.choice(['#e8c040', '#f0d060', '#d8a830']), '#a87a18', 12, k)
    save(img, 'w_kiku')


def fuji_wreath():
    img = canvas(200, 120); rnd = random.Random(5)
    line(img, [(10, 40), (100, 22), (190, 40)], '#3f5a3a', 4)
    d = ImageDraw.Draw(img)
    for sx in (18, 40, 160, 182):
        for k in range(12): y = 40 + k * 6; r = 7 - k * .4; d.ellipse([px(sx - r), px(y - r * .8), px(sx + r), px(y + r * .8)], fill=H(rnd.choice(['#8a74c0', '#a898d8', '#6a54a0'])))
    for x in range(20, 184, 16):
        y = 40 - 18 * math.sin(math.pi * (x - 10) / 180); flower(img, x, y, 7, rnd.choice(['#9a88c8', '#c8bce6']), '#f0e8ff', 5)
    save(img, 'w_fuji')


def fox_ears():
    img = canvas(180, 90)
    line(img, [(8, 84), (90, 62), (172, 84)], '#1a1414', 3)
    for sx in (-1, 1):
        fill(img, '#f4efe6', 3 + sx, poly=[(90 + sx * 30, 72), (90 + sx * 58, 4), (90 + sx * 76, 72)], scale=5, contrast=.5)
        poly(img, [(90 + sx * 42, 66), (90 + sx * 58, 22), (90 + sx * 68, 66)], '#c83a3a')
        volume(img, (90 + min(sx * 30, sx * 76), 4, 90 + max(sx * 30, sx * 76), 72), .4, .2)
    save(img, 'w_foxears')


def hana_kanzashi():
    img = canvas(100, 140); rnd = random.Random(7)
    line(img, [(70, 20), (30, 60)], '#d8b048', 2.4)
    for x, y, r, c in ((44, 40, 16, '#e05070'), (66, 30, 13, '#f090b0'), (34, 60, 12, '#f4c4d2'), (60, 54, 11, '#c02a4a'), (48, 22, 10, '#f4c4d2')): flower(img, x, y, r, c, '#f0d060', 5)
    d = ImageDraw.Draw(img)
    for k in range(4): x = 40 + k * 6; d.line([(px(x), px(66)), (px(x + 2), px(110 + k * 6))], fill=H('#d8b048'), width=px(1)); flower(img, x + 2, 112 + k * 6, 5, '#f090b0', '#f0d060', 5)
    save(img, 'w_hanakan')


def lotus():
    img = canvas(120, 80)
    for k, a in enumerate((-1.1, -.6, -.2, .2, .6, 1.1)):
        x, y = 60 + math.sin(a) * 34, 64 - math.cos(a) * 20
        fill(img, '#f2a8c0' if k % 2 else '#f8c8d8', 3 + k, poly=[(60, 70), (x - 12, y), (x, y - 36 + abs(a) * 14), (x + 12, y)], scale=4, contrast=.5)
    fill(img, '#e8c040', 9, ell=(50, 52, 70, 66), scale=3)
    volume(img, (14, 10, 106, 74), .4, .2)
    save(img, 'w_lotus')


def momiji_crown():
    img = canvas(180, 70); rnd = random.Random(9); d = ImageDraw.Draw(img)
    line(img, [(10, 52), (90, 36), (170, 52)], '#5a3a22', 3)
    for k in range(11):
        t = k / 10; x = 12 + 156 * t; y = 50 - 16 * math.sin(math.pi * t); c = H(rnd.choice(['#c8442a', '#e0782a', '#a0281e', '#d8a030']))
        for j in range(5): a = -math.pi / 2 + (j - 2) * .6 + rnd.uniform(-.2, .2); d.polygon([(px(x), px(y)), (px(x + math.cos(a - .15) * 7), px(y + math.sin(a - .15) * 7)), (px(x + math.cos(a) * 14), px(y + math.sin(a) * 14)), (px(x + math.cos(a + .15) * 7), px(y + math.sin(a + .15) * 7))], fill=c)
    volume(img, (0, 20, 180, 70), .3, .15)
    save(img, 'w_momiji')


def tsuru_hat():
    img = canvas(120, 90); c = H('#d8384a')
    poly(img, [(6, 60), (60, 34), (66, 84)], lt(c, .1)); poly(img, [(114, 60), (70, 34), (66, 84)], c)
    poly(img, [(60, 34), (70, 34), (66, 84)], dk(c, .3)); poly(img, [(64, 50), (100, 4), (94, 22), (78, 52)], lt(c, .05)); poly(img, [(94, 22), (100, 4), (106, 18)], dk(c, .2))
    save(img, 'w_tsuru')


def oni_horns_gold():
    img = canvas(170, 80)
    for sx in (-1, 1):
        fill(img, '#d8b048', 3 + sx, poly=[(85 + sx * 36, 76), (85 + sx * 60, 6), (85 + sx * 58, 40), (85 + sx * 56, 76)], scale=4, contrast=1.3)
        volume(img, (85 + min(sx * 36, sx * 60), 6, 85 + max(sx * 36, sx * 60), 76), .6, .2, spec=.4)
    save(img, 'w_goldhorns')


# ───────────── neck ─────────────
def eri():
    img = canvas(170, 120)
    fill(img, '#2a2a4a', 3, poly=[(4, 20), (60, 6), (85, 60), (110, 6), (166, 20), (160, 118), (10, 118)], scale=8, contrast=.9)        # haori shoulders
    fill(img, '#c02a2a', 4, poly=[(46, 8), (85, 76), (124, 8), (112, 8), (85, 60), (58, 8)], scale=4)
    fill(img, '#f4f0e6', 5, poly=[(36, 10), (85, 96), (134, 10), (122, 10), (85, 80), (48, 10)], scale=4, contrast=.3)
    d = ImageDraw.Draw(img)
    for x, y in ((30, 70), (140, 70)): d.ellipse([px(x - 8), px(y - 8), px(x + 8), px(y + 8)], fill=H('#e8e0d0')); d.ellipse([px(x - 4), px(y - 4), px(x + 4), px(y + 4)], fill=H('#2a2a4a'))
    line(img, [(70, 100), (85, 108), (100, 100)], '#e8e0d0', 2.4); ell(img, (80, 102, 90, 112), '#e8e0d0')
    volume(img, (4, 6, 166, 118), .4, .3)
    save(img, 'w_eri')


def bowtie():
    img = canvas(90, 44)
    fill(img, '#1a1418', 3, poly=[(45, 22), (6, 4), (2, 22), (6, 40)], scale=4, contrast=1.2); fill(img, '#1a1418', 4, poly=[(45, 22), (84, 4), (88, 22), (84, 40)], scale=4, contrast=1.2)
    ell(img, (36, 14, 54, 30), '#2a2228'); volume(img, (2, 4, 88, 40), .5, .3, spec=.3)
    save(img, 'w_bowtie')


def big_suzu():
    img = canvas(140, 80)
    line(img, [(4, 8), (70, 26), (136, 8)], '#b8322a', 5)
    fill(img, '#d8b048', 3, ell=(46, 22, 94, 72), scale=3, contrast=1.3)
    d = ImageDraw.Draw(img); d.line([(px(48), px(46)), (px(92), px(46))], fill=H('#6a4a12'), width=px(2)); d.ellipse([px(64), px(50), px(76), px(62)], fill=H('#3a2a08'))
    volume(img, (46, 22, 94, 72), .7, .4, spec=.55)
    save(img, 'w_bigsuzu')


def pearls():
    img = canvas(140, 50); d = ImageDraw.Draw(img)
    for k in range(17):
        t = k / 16; x = 6 + 128 * t; y = 8 + 30 * math.sin(math.pi * t)
        fill(img, '#efe9e2', k, ell=(x - 5, y - 5, x + 5, y + 5), scale=2, contrast=.3); volume(img, (x - 5, y - 5, x + 5, y + 5), .7, .4, spec=.7)
    save(img, 'w_pearls')


def magatama():
    img = canvas(140, 80); rnd = random.Random(4)
    line(img, [(4, 6), (70, 30), (136, 6)], '#6a4a2a', 1.6)
    for k in range(7):
        t = (k + .5) / 7; x = 10 + 120 * t; y = 8 + 26 * math.sin(math.pi * t)
        if k == 3:
            fill(img, '#2f8a5a', 9, poly=[(x - 10, y), (x + 10, y - 4), (x + 12, y + 16), (x, y + 30), (x - 4, y + 20), (x + 2, y + 12), (x - 10, y + 8)], scale=3, contrast=.8); volume(img, (x - 12, y - 6, x + 14, y + 32), .6, .3, spec=.5)
        else:
            c = rnd.choice(['#c02a2a', '#2f6a8a', '#e8e0d0', '#d8b048']); fill(img, c, k, ell=(x - 5, y - 5, x + 5, y + 5), scale=2); volume(img, (x - 5, y - 5, x + 5, y + 5), .6, .4, spec=.5)
    save(img, 'w_magatama')


def plaid_scarf():
    img = canvas(180, 120); base = H('#8a2a2a')
    m = I.mask_poly(img, poly=[(4, 20), (90, 44), (176, 20), (170, 50), (90, 70), (10, 50)]); fill(img, base, 3, mask=m, scale=6, contrast=.8)
    m2 = I.mask_poly(img, poly=[(110, 50), (140, 50), (146, 118), (116, 118)]); fill(img, base, 4, mask=m2, scale=6, contrast=.8)
    for mm in (m, m2):
        l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l)
        for x in range(0, 180, 14): d.line([(px(x), 0), (px(x), px(120))], fill=(230, 200, 120, 150), width=px(2))
        for y in range(0, 120, 14): d.line([(0, px(y)), (px(180), px(y))], fill=(30, 20, 40, 150), width=px(3))
        a = np.asarray(l, np.float32); a[..., 3] *= np.asarray(mm, np.float32) / 255; img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))
    d = ImageDraw.Draw(img)
    for k in range(6): d.line([(px(118 + k * 5), px(118)), (px(118 + k * 5), px(126))], fill=base, width=px(1.4))
    volume(img, (4, 20, 176, 120), .45, .25)
    save(img, 'w_scarf2')


def bandana():
    img = canvas(150, 100); base = H('#b8322a')
    fill(img, base, 3, poly=[(4, 10), (75, 22), (146, 10), (75, 96)], scale=5, contrast=.8)
    d = ImageDraw.Draw(img); rnd = random.Random(2)
    for _ in range(26):
        x, y = rnd.uniform(30, 120), rnd.uniform(20, 70)
        if abs(x - 75) < (96 - y) * .72: d.ellipse([px(x - 2.4), px(y - 2.4), px(x + 2.4), px(y + 2.4)], fill=H('#f2e6d0'))
    volume(img, (4, 10, 146, 96), .45, .25)
    save(img, 'w_bandana')


def sakura_lei():
    img = canvas(160, 50); rnd = random.Random(8)
    for k in range(12):
        t = k / 11; x = 8 + 144 * t; y = 10 + 26 * math.sin(math.pi * t); flower(img, x, y, 8, rnd.choice(['#f4c4d2', '#e896b0', '#f8dde4']), '#c9738f', 5)
    save(img, 'w_sakura')


def hachimaki():
    img = canvas(170, 80)
    fill(img, '#f2eee4', 3, poly=[(8, 44), (85, 30), (162, 44), (160, 60), (85, 48), (10, 60)], scale=5, contrast=.4, dark=.15)
    ell(img, (72, 30, 98, 52), '#c42a24')
    fill(img, '#f2eee4', 4, poly=[(150, 44), (168, 52), (158, 62)], scale=4, contrast=.4)
    fill(img, '#f2eee4', 5, poly=[(160, 54), (170, 78), (160, 80), (152, 60)], scale=4, contrast=.4); fill(img, '#f2eee4', 6, poly=[(156, 54), (140, 78), (132, 74), (148, 56)], scale=4, contrast=.4)
    volume(img, (8, 30, 170, 80), .4, .2)
    save(img, 'w_hachimaki')


def navy_scarf():
    img = canvas(180, 120); base = H('#2b3450')
    fill(img, base, 3, poly=[(4, 20), (90, 44), (176, 20), (170, 50), (90, 70), (10, 50)], scale=6, contrast=.8)
    fill(img, base, 4, poly=[(110, 50), (140, 50), (146, 118), (116, 118)], scale=6, contrast=.8)
    d = ImageDraw.Draw(img)
    for k in range(9): x = 14 + k * 19; y = 34 + 10 * math.sin(math.pi * (x - 4) / 172); d.ellipse([px(x - 3), px(y - 3), px(x + 3), px(y + 3)], fill=H('#eea3bb'))
    for k in range(6): d.line([(px(118 + k * 5), px(118)), (px(118 + k * 5), px(126))], fill=base, width=px(1.4))
    volume(img, (4, 20, 176, 120), .45, .25)
    save(img, 'w_scarf')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for f in (kabuto, eboshi, tsunokakushi, sugegasa, tenugui, kiku_crown, fuji_wreath, fox_ears, hana_kanzashi, lotus, momiji_crown, tsuru_hat, oni_horns_gold,
              eri, bowtie, big_suzu, pearls, magatama, plaid_scarf, bandana, sakura_lei, hachimaki, navy_scarf): f()
    json.dump(META, open(f'{OUT}/wear.json', 'w'))
