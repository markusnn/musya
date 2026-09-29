#!/usr/bin/env python3
"""Second batch of room decorations: every room gets about thirty things of its own, like the kitchen.
Pictures are packed into one atlas per room (the Claude copy of the game allows ~500 files).
Usage: room_items2.py <outdir> → <outdir>/atlas_<room>.webp + rooms2.json (rows carry "at": [room, x, y])"""
import json, math, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc
import items as I
import room_items as RI
from items import px, canvas, fill, volume, soft, floor_shadow, line, ell, poly, text, H, dk, lt, SERIF, SANS, mask_poly
from room_items import clip, barrel, crock, plate, rope, cr, blob, figure_base, screen, fox_statue, WOOD, WOOD_D, WOOD_L

OUT = sys.argv[1]
ROWS, IMGS = [], {}
SLUG = {'Веранда': 'ver', 'Спальня': 'bed', 'Онсэн': 'ons', 'Гардероб': 'war', 'Дворик': 'crt', 'Вход': 'ent', 'Игры': 'gam'}


def save(img, iid, name, cat, anchor='b', price=60, glow=None):
    out = img.resize((P.W, P.H), Image.LANCZOS)
    a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .88
    a[..., :3] += np.random.default_rng(abs(hash(iid)) % 2 ** 32).normal(0, 3.5, a.shape[:2])[..., None]
    IMGS.setdefault(cat, []).append((iid, Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')))
    row = {'id': iid, 'n': name, 'c': cat, 'w': P.W, 'h': P.H, 'a': anchor, 'p': price}
    if glow: row['glow'] = glow
    ROWS.append(row); print(iid, P.W, P.H, name)


def pack():
    for cat, lst in IMGS.items():
        lst = sorted(lst, key=lambda t: -t[1].height); W = 1400; x = y = rowh = 0; pos = {}
        for iid, im in lst:
            if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
            pos[iid] = (x, y); x += im.width + 2; rowh = max(rowh, im.height)
        at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
        for iid, im in lst: at.paste(im, pos[iid])
        at.save(f'{OUT}/atlas_{SLUG[cat]}.webp', 'WEBP', quality=86, alpha_quality=90, method=6)
        for r in ROWS:
            if r['id'] in pos: r['at'] = [SLUG[cat], pos[r['id']][0], pos[r['id']][1]]
        print('atlas', cat, at.size)


def glass(img, poly_pts, seed, tint=(200, 220, 225)):
    m = mask_poly(img, poly=poly_pts); tmp = Image.new('RGBA', img.size, (0, 0, 0, 0))
    fill(tmp, tint + (255,), seed, mask=m, scale=4, contrast=.3); a = np.asarray(tmp, np.float32); a[..., 3] *= .55
    img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))
    xs = [p[0] for p in poly_pts]; ys = [p[1] for p in poly_pts]
    soft(img, lambda d: d.rectangle([px(min(xs) + 5), px(min(ys) + 6), px(min(xs) + 10), px(max(ys) - 6)], fill=(255, 255, 255, 120)), 1)


def flowers(img, cx, cy, rx, ry, cols, n, seed, r=(6, 10), center='#e8c040', petals=5):
    rr = random.Random(seed); d = ImageDraw.Draw(img)
    for _ in range(n):
        x, y = cx + rr.uniform(-rx, rx), cy + rr.uniform(-ry, ry); rad = rr.uniform(*r); c = H(rr.choice(cols))
        for k in range(petals):
            a = k / petals * math.tau; d.ellipse([px(x + math.cos(a) * rad * .6 - rad * .5), px(y + math.sin(a) * rad * .6 - rad * .5), px(x + math.cos(a) * rad * .6 + rad * .5), px(y + math.sin(a) * rad * .6 + rad * .5)], fill=c)
        d.ellipse([px(x - rad * .25), px(y - rad * .25), px(x + rad * .25), px(y + rad * .25)], fill=H(center))


def leaves(img, blobs, pal, n, seed, size=(4, 8)):
    P.dab_mass(ImageDraw.Draw(img), [(px(x), px(y), px(rx), px(ry)) for x, y, rx, ry in blobs], n, 'leaf', [hexc(c) for c in pal], random.Random(seed), size=size)


def pot(img, cx, base, w, h, col, seed):
    fill(img, col, seed, poly=[(cx - w / 2, base - h), (cx + w / 2, base - h), (cx + w * .4, base), (cx - w * .4, base)], scale=6, contrast=1.3)
    ImageDraw.Draw(img).rectangle([px(cx - w / 2 - 4), px(base - h - 6), px(cx + w / 2 + 4), px(base - h + 4)], fill=dk(H(col), .35))
    volume(img, (cx - w / 2 - 4, base - h - 6, cx + w / 2 + 4, base), .5, .3, spec=.2)


def rack(img, col, seed, pattern, sleeve=True, W=300, Hh=330):
    floor_shadow(img, W / 2, Hh - 6, W * .46)
    fill(img, '#1a120c', seed, rect=(4, 20, W - 4, 32), scale=5, stretch=(6, .5)); fill(img, '#1a120c', seed + 1, rect=(40, 32, 52, Hh - 6), scale=4); fill(img, '#1a120c', seed + 2, rect=(W - 52, 32, W - 40, Hh - 6), scale=4)
    for x in (30, W - 70): fill(img, '#1a120c', seed + 3 + x, rect=(x, Hh - 24, x + 40, Hh - 6), scale=4)
    pts = [(10, 36), (W - 10, 36), (W - 14, 150), (W * .73, 160), (W * .77, Hh - 30), (W * .23, Hh - 30), (W * .27, 160), (14, 150)] if sleeve else [(W * .25, 36), (W * .75, 36), (W * .78, Hh - 30), (W * .22, Hh - 30)]
    m = fill(img, col, seed + 5, poly=pts, scale=10, stretch=(1, 3), contrast=.9); rr = random.Random(seed)
    if pattern == 'tsuru': clip(img, m, lambda d: [d.polygon([(px(x), px(y)), (px(x + 14), px(y - 10)), (px(x + 28), px(y)), (px(x + 14), px(y - 4))], fill=(244, 240, 230, 230)) for x, y in [(rr.uniform(20, W - 50), rr.uniform(60, Hh - 60)) for _ in range(12)]])
    elif pattern == 'sakura': flowers(img, W / 2, Hh * .55, W * .4, Hh * .35, ['#f4c4d2', '#f8dde4'], 30, seed, (5, 8))
    elif pattern == 'fuji': clip(img, m, lambda d: [d.ellipse([px(x - 4), px(y + k * 7), px(x + 4), px(y + k * 7 + 6)], fill=(170, 150, 220, 230)) for x in range(30, W - 20, 26) for y in (60,) for k in range(10)])
    elif pattern == 'asagao': flowers(img, W / 2, Hh * .6, W * .38, Hh * .3, ['#3a4ab8', '#6a3ab0'], 16, seed, (9, 13), '#f4f0f8')
    elif pattern == 'plain': pass
    fill(img, '#d8b048', seed + 6, rect=(W * .27, 150, W * .73, 184), scale=4, contrast=.8)
    poly(img, [(W / 2 - 22, 36), (W / 2, 100), (W / 2 + 22, 36)], '#f2eee4'); volume(img, (10, 36, W - 10, Hh - 30), .35, .2)


# ───────────────────────────── ВЕРАНДА (+17) ─────────────────────────────
def veranda():
    C = 'Веранда'
    img = canvas(200, 230); rope(img, [(10, 10), (100, 30), (190, 10)], '#6a4a2a', 2)          # three wind chimes
    for k, (x, c) in enumerate(((40, '#b9d6e6'), (100, '#f0c8d4'), (160, '#cfe6d8'))):
        y = 18 + 12 * math.sin(math.pi * (x - 10) / 180); line(img, [(x, y), (x, y + 30)], '#1a1410', 1)
        m = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(m).pieslice([px(x - 22), px(y + 26), px(x + 22), px(y + 86)], 180, 360, fill=H(c)[:3] + (170,)); img.alpha_composite(m)
        line(img, [(x, y + 56), (x, y + 110)], '#1a1410', 1); fill(img, '#e8dcc0', 10 + k, rect=(x - 10, y + 110, x + 10, y + 190), scale=4, contrast=.5)
    save(img, 'v2_furin3', 'Гирлянда фуринов', C, 't', 90)
    img = canvas(220, 200); floor_shadow(img, 110, 194, 96)
    P.pine(img, px(110), px(130), px(130), 21, P.PAL_PINE, P.BARK, lean=-.4, pads=3, spread=.9)
    fill(img, '#6a6d66', 22, poly=[(30, 128), (190, 128), (170, 194), (50, 194)], scale=5, contrast=1.3); volume(img, (30, 128, 190, 194), .5, .3)
    save(img, 'v2_bonsai_stone', 'Сосна в каменной чаше', C, 'b', 150)
    img = canvas(320, 150); floor_shadow(img, 160, 144, 150)                                   # bamboo bench
    for k in range(9): fill(img, '#b8a060', 30 + k, rect=(14, 40 + k * 6, 306, 45 + k * 6), scale=5, stretch=(8, .3), contrast=.9)
    for x in (30, 280): fill(img, '#8a7040', 40 + x, rect=(x, 94, x + 14, 144), scale=4)
    fill(img, '#c02a2a', 42, poly=[(60, 36), (260, 36), (268, 48), (52, 48)], scale=4); volume(img, (14, 36, 306, 144), .4, .2)
    save(img, 'v2_endai', 'Бамбуковая скамья эндай', C, 'b', 160)
    img = canvas(200, 160); floor_shadow(img, 100, 154, 90)                                    # barley tea
    fill(img, WOOD, 43, rect=(10, 128, 190, 146), scale=5, stretch=(5, .5))
    glass(img, [(40, 128), (90, 128), (96, 40), (34, 40)], 44, (140, 90, 40)); ImageDraw.Draw(img).line([(px(96), px(60)), (px(112), px(70)), (px(96), px(100))], fill=(220, 225, 230, 200), width=px(3))
    for x in (130, 166): glass(img, [(x - 14, 128), (x + 14, 128), (x + 16, 80), (x - 16, 80)], 45 + x, (150, 100, 45)); ell(img, (x - 6, 86, x + 2, 94), '#e8f4f8')
    save(img, 'v2_mugicha', 'Ячменный чай мугитя', C, 'b', 50)
    img = canvas(90, 170); line(img, [(45, 0), (45, 20)], '#120c09', 2)                         # small white lantern
    m = fill(img, '#f2eadc', 46, ell=(8, 24, 82, 160), scale=5, contrast=.6)
    clip(img, m, lambda d: [d.line([(0, px(24 + 136 * k / 10)), (px(90), px(24 + 136 * k / 10))], fill=(120, 90, 50, 140), width=px(1.4)) for k in range(1, 10)])
    text(img, '夏', 45, 92, 30, '#1a1410', SERIF); volume(img, (8, 24, 82, 160), .5, .45)
    save(img, 'v2_chochin', 'Белый фонарик «Лето»', C, 't', 50, glow=[45, 92])
    img = canvas(300, 170); rope(img, [(4, 12), (150, 26), (296, 12)], '#8a6a3a', 2)            # drying tenugui
    for k, (x, c) in enumerate(((50, '#2a4a7a'), (130, '#f2eee4'), (210, '#b8322a'), (270, '#2f6a3a'))):
        y = 14 + 10 * math.sin(math.pi * (x - 4) / 292); fill(img, c, 50 + k, poly=[(x - 26, y), (x + 26, y), (x + 24, y + 130), (x - 24, y + 132)], scale=5, contrast=.6)
        rr = random.Random(k); d = ImageDraw.Draw(img); [d.ellipse([px(a - 3), px(b - 3), px(a + 3), px(b + 3)], fill=H('#e8e0d0' if c != '#f2eee4' else '#2a4a7a')) for a, b in [(x + rr.uniform(-18, 18), y + rr.uniform(10, 120)) for _ in range(8)]]
        ImageDraw.Draw(img).rectangle([px(x - 3), px(y - 4), px(x + 3), px(y + 6)], fill=H('#c8a070'))
    save(img, 'v2_towels', 'Сохнущие тэнугуи', C, 't', 50)
    img = canvas(100, 190); floor_shadow(img, 50, 184, 36)                                     # sparklers in a cup
    fill(img, '#4a6a8a', 55, poly=[(24, 184), (76, 184), (82, 120), (18, 120)], scale=4, contrast=.8); volume(img, (18, 120, 82, 184), .5, .3, spec=.3)
    rr = random.Random(5)
    for k in range(9): x = 30 + k * 5; line(img, [(x, 124), (x + rr.uniform(-16, 16), 20 + rr.uniform(0, 30))], rr.choice(['#c02a2a', '#2a4a8a', '#e8c040', '#2f6a3a']), 1.4)
    save(img, 'v2_hanabi', 'Бенгальские огни сэнко', C, 'b', 30)
    img = canvas(180, 200); floor_shadow(img, 90, 194, 70)                                     # hydrangea
    leaves(img, [(90, 110, 70, 30)], ['#1a3a1a', '#2a5a2a', '#3a7a3a'], 500, 56)
    for k, (x, y) in enumerate(((60, 70), (110, 60), (90, 100), (130, 96), (50, 110))): flowers(img, x, y, 22, 18, ['#5a7ad8', '#7a9ae8', '#9a8ae0', '#6a6ac8'], 26, 57 + k, (4, 6), '#e8f0ff', 4)
    pot(img, 90, 194, 110, 60, '#2a3a4a', 58)
    save(img, 'v2_ajisai', 'Гортензия адзисай', C, 'b', 110)
    img = canvas(160, 280); floor_shadow(img, 80, 274, 60)                                     # sunflowers in a jug
    for k, (x, y) in enumerate(((50, 60), (100, 40), (80, 100))):
        line(img, [(80, 200), (x, y)], '#3a6a2a', 4); flowers(img, x, y, 1, 1, ['#f0c020'], 1, 60 + k, (22, 24), '#5a3a1a', 14)
    leaves(img, [(80, 160, 40, 20)], ['#2a5a2a', '#3a7a3a', '#5a9a3a'], 200, 61)
    crock(img, 80, 274, 110, 90, '#8a6a4a', 62)
    save(img, 'v2_himawari', 'Подсолнухи в кувшине', C, 'b', 90)
    img = canvas(320, 90); floor_shadow(img, 160, 84, 150)                                     # goza mat
    m = fill(img, '#c8b070', 63, poly=[(30, 20), (290, 20), (316, 80), (4, 80)], scale=6, stretch=(6, .3), contrast=.9)
    clip(img, m, lambda d: [d.line([(0, px(y)), (px(320), px(y))], fill=(120, 100, 50, 150), width=px(1)) for y in range(22, 80, 4)])
    for y in (20, 78): ImageDraw.Draw(img).line([(px(30 if y < 50 else 4), px(y)), (px(290 if y < 50 else 316), px(y))], fill=H('#2a4a2a'), width=px(4))
    save(img, 'v2_goza', 'Соломенный коврик гоза', C, 'b', 50)
    img = canvas(140, 290); floor_shadow(img, 70, 284, 60)                                     # scratching post
    fill(img, '#8a6a4a', 64, rect=(10, 260, 130, 284), scale=5); m = fill(img, '#c8ae74', 65, rect=(52, 30, 88, 262), scale=4, stretch=(.3, 3))
    clip(img, m, lambda d: [d.line([(px(50), px(y)), (px(90), px(y + 4))], fill=(120, 90, 40, 200), width=px(2)) for y in range(32, 262, 7)])
    fill(img, '#8a6a4a', 66, ell=(40, 18, 100, 40), scale=4); line(img, [(92, 30), (116, 90)], '#e8e0d0', 1.4)
    fill(img, '#c02a2a', 67, ell=(106, 86, 128, 108), scale=3); volume(img, (106, 86, 128, 108), .6, .4, spec=.3); volume(img, (52, 18, 100, 262), .45, .3)
    save(img, 'v2_scratch', 'Когтеточка для Муси', C, 'b', 70)
    img = canvas(160, 110); fill(img, WOOD_D, 68, rect=(0, 0, 160, 16), scale=5)               # swallow nest
    fill(img, '#8a7050', 69, poly=[(30, 16), (130, 16), (116, 70), (80, 88), (44, 70)], scale=3, contrast=1.4)
    for k, x in enumerate((58, 80, 102)):
        fill(img, '#2a2a3a', 70 + k, ell=(x - 12, 2, x + 12, 28), scale=3); poly(img, [(x - 8, 20), (x + 8, 20), (x, 36)], '#f0c040'); ell(img, (x - 6, 8, x - 2, 12), '#f4f0e6')
    save(img, 'v2_tsubame', 'Гнездо ласточек', C, 't', 60)
    img = canvas(170, 220); floor_shadow(img, 85, 214, 70)                                     # shigaraki tanuki
    blob(img, [(40, 210), (30, 150), (50, 100), (85, 88), (120, 100), (140, 150), (130, 210)], hexc('#6a4a30'), 73)
    blob(img, [(56, 200), (50, 150), (85, 128), (120, 150), (114, 200)], hexc('#c8a878'), 74, k=.3)
    blob(img, [(50, 100), (48, 60), (85, 42), (122, 60), (120, 100), (85, 112)], hexc('#6a4a30'), 75)
    for sx in (-1, 1): ell(img, (85 + sx * 18 - 12, 60, 85 + sx * 18 + 12, 84), '#2a1a10'); ell(img, (85 + sx * 18 - 5, 66, 85 + sx * 18 + 3, 74), '#f4f0e6')
    blob(img, [(36, 50), (85, 20), (134, 50), (85, 58)], hexc('#b8975a'), 76, k=.3)
    fill(img, '#e8e0cc', 77, rect=(124, 140, 150, 190), scale=3); text(img, '酒', 137, 166, 14, '#1a1410', SERIF)
    save(img, 'v2_tanuki', 'Тануки из Сигараки', C, 'b', 130)
    img = canvas(150, 200); floor_shadow(img, 75, 194, 60)                                     # bucket with flowers
    flowers(img, 75, 70, 50, 34, ['#e8a0b6', '#f2eee4', '#c02a4a', '#e8c040'], 26, 78, (6, 10)); leaves(img, [(75, 96, 50, 16)], ['#2a5a2a', '#3a7a3a'], 120, 79)
    fill(img, WOOD_L, 80, poly=[(30, 110), (120, 110), (112, 194), (38, 194)], scale=6, stretch=(.4, 3)); [rope(img, [(32, y), (75, y + 3), (118, y)], '#2a2018', 3) for y in (124, 180)]
    volume(img, (30, 110, 120, 194), .45, .3)
    save(img, 'v2_flowerbucket', 'Ведёрко с цветами', C, 'b', 60)
    img = canvas(120, 260); floor_shadow(img, 60, 254, 30)                                     # small koinobori
    line(img, [(40, 254), (40, 10)], '#8a6038', 4)
    for k, (y, c) in enumerate(((30, '#1a1a2a'), (80, '#c02a2a'), (130, '#2a4a8a'))):
        fill(img, c, 81 + k, poly=[(42, y), (110, y + 6), (100, y + 16), (116, y + 28), (42, y + 34)], scale=3, contrast=.8); ell(img, (48, y + 8, 60, y + 20), '#f4f0e6'); ell(img, (51, y + 11, 57, y + 17), '#1a1414')
    save(img, 'v2_koinobori', 'Маленький коинобори', C, 'b', 50)
    img = canvas(130, 150); floor_shadow(img, 65, 144, 52)                                     # kakigori
    fill(img, (200, 220, 230, 255), 84, poly=[(30, 144), (100, 144), (116, 100), (14, 100)], scale=3, contrast=.3); volume(img, (14, 100, 116, 144), .5, .3, spec=.4)
    blob(img, [(20, 104), (30, 60), (65, 30), (100, 60), (110, 104)], hexc('#f4f4f8'), 85, scale=2, k=.3)
    soft(img, lambda d: d.ellipse([px(34), px(40), px(96), px(90)], fill=(220, 40, 60, 170)), 3); ell(img, (60, 20, 74, 34), '#c02a2a')
    save(img, 'v2_kakigori', 'Какигори со льдом', C, 'b', 30)
    img = canvas(200, 100); floor_shadow(img, 100, 94, 84); plate(img, 100, 78, 180)           # watermelon slices
    for k, x in enumerate((50, 100, 150)):
        poly(img, [(x - 26, 76), (x + 26, 76), (x, 30)], '#d83a3a'); ImageDraw.Draw(img).line([(px(x - 26), px(76)), (px(x + 26), px(76))], fill=H('#2f6a2a'), width=px(5))
        d = ImageDraw.Draw(img); [d.ellipse([px(x + t - 2), px(56 + abs(t) * .4 - 3), px(x + t + 2), px(56 + abs(t) * .4 + 3)], fill=H('#1a1414')) for t in (-10, 0, 10)]
    save(img, 'v2_suika', 'Дольки арбуза', C, 'b', 30)


# ───────────────────────────── СПАЛЬНЯ (+17) ─────────────────────────────
def bedroom():
    C = 'Спальня'
    img = canvas(260, 190); floor_shadow(img, 130, 184, 120)                                   # folded futons
    for k, c in enumerate(('#2a3a6a', '#f2eee4', '#b8322a', '#e8dcc0')):
        y = 180 - k * 36; fill(img, c, 100 + k, poly=[(14 + k * 4, y), (246 - k * 4, y), (240 - k * 4, y - 34), (20 + k * 4, y - 34)], scale=5, contrast=.6); volume(img, (14, y - 34, 246, y), .4, .25)
    save(img, 'b2_futons', 'Стопка футонов', C, 'b', 120)
    img = canvas(300, 230); floor_shadow(img, 150, 226, 140)
    def moon(im):
        I.ell(im, (180, 30, 240, 90), '#f4e8c0'); P.pine(im, px(90), px(210), px(150), 44, [hexc('#1a1a1a'), hexc('#2a2a2a'), hexc('#3a3a38')], (hexc('#1a1a1a'), hexc('#2a2a2a'), hexc('#3a3a38')), lean=.3, pads=3, spread=.8)
    screen(img, 10, 10, 280, 212, 4, moon, base='#3a3a4a', seed=105)
    save(img, 'b2_byobu_moon', 'Ширма «Луна и сосны»', C, 'b', 200)
    img = canvas(160, 140); floor_shadow(img, 80, 134, 70)                                     # music box
    fill(img, '#2a1a14', 110, rect=(20, 70, 140, 134), scale=5); fill(img, '#3a2418', 111, poly=[(20, 70), (140, 70), (150, 10), (30, 10)], scale=5)
    fill(img, '#c02a2a', 112, rect=(28, 66, 132, 76), scale=3); poly(img, [(70, 60), (84, 44), (98, 60), (84, 54)], '#f4f0e6')
    d = ImageDraw.Draw(img); d.arc([px(40), px(84), px(120), px(124)], 200, 340, fill=H('#d8b048'), width=px(2)); volume(img, (20, 10, 150, 134), .4, .25, spec=.3)
    save(img, 'b2_musicbox', 'Музыкальная шкатулка', C, 'b', 90)
    img = canvas(140, 150); floor_shadow(img, 70, 144, 56)                                     # plush tanuki
    blob(img, [(30, 144), (24, 100), (70, 70), (116, 100), (110, 144)], hexc('#8a6a48'), 113, scale=3, k=.4)
    blob(img, [(34, 70), (40, 30), (70, 18), (100, 30), (106, 70), (70, 84)], hexc('#8a6a48'), 114, scale=3, k=.4)
    for sx in (-1, 1): ell(img, (70 + sx * 18 - 12, 40, 70 + sx * 18 + 12, 62), '#3a2a1c'); ell(img, (70 + sx * 18 - 4, 46, 70 + sx * 18 + 4, 54), '#f4f0e6')
    ell(img, (62, 60, 78, 72), '#2a1a10'); blob(img, [(46, 140), (50, 104), (70, 96), (90, 104), (94, 140)], hexc('#d8c09a'), 115, scale=3, k=.3)
    save(img, 'b2_tanuki', 'Плюшевый тануки', C, 'b', 50)
    img = canvas(160, 150); floor_shadow(img, 80, 144, 70)                                     # water by the bed
    fill(img, '#2a1a14', 116, rect=(10, 120, 150, 140), scale=4); glass(img, [(40, 120), (80, 120), (84, 50), (36, 50)], 117)
    ImageDraw.Draw(img).line([(px(84), px(66)), (px(98), px(76)), (px(84), px(100))], fill=(220, 225, 230, 200), width=px(3)); glass(img, [(104, 120), (132, 120), (134, 88), (102, 88)], 118)
    save(img, 'b2_water', 'Кувшин воды у постели', C, 'b', 30)
    img = canvas(220, 170); line(img, [(60, 16), (110, 0), (160, 16)], '#1a120c', 1.6)            # framed Fuji picture
    fill(img, '#3a2418', 119, rect=(10, 16, 210, 166), scale=5); fill(img, '#d8d4c8', 120, rect=(22, 28, 198, 154), scale=6, contrast=.4)
    poly(img, [(40, 140), (100, 60), (120, 60), (180, 140)], '#4a5a7a'); poly(img, [(88, 76), (100, 60), (120, 60), (132, 76), (118, 72), (110, 80), (102, 72)], '#f4f0e6'); ell(img, (150, 40, 172, 62), '#c02a2a')
    save(img, 'b2_fuji', 'Картина «Фудзи»', C, 't', 110)
    img = canvas(220, 130); floor_shadow(img, 110, 124, 100)                                   # wicker cat bed
    fill(img, '#b08a50', 121, ell=(10, 50, 210, 126), scale=4, stretch=(4, 1), contrast=1.2)
    clip(img, mask_poly(img, ell=(10, 50, 210, 126)), lambda d: [d.arc([px(x - 10), px(50), px(x + 10), px(126)], 0, 360, fill=(110, 80, 40, 160), width=px(1.2)) for x in range(10, 210, 12)])
    fill(img, '#e8a0b6', 122, ell=(30, 48, 190, 90), scale=4, contrast=.5); volume(img, (10, 48, 210, 126), .45, .3)
    save(img, 'b2_catbed', 'Корзинка-лежанка', C, 'b', 70)
    img = canvas(170, 170); floor_shadow(img, 85, 164, 66)                                     # baku amulet
    figure_base(img, 85, 164, 120, '#3a2a1a', 123)
    blob(img, [(34, 138), (30, 90), (70, 70), (126, 76), (140, 110), (136, 138)], hexc('#5a6a7a'), 124)
    blob(img, [(20, 100), (10, 60), (30, 40), (60, 44), (68, 80)], hexc('#5a6a7a'), 125); line(img, [(16, 64), (4, 96), (12, 112)], '#5a6a7a', 7)
    ell(img, (34, 56, 42, 64), '#d8b048'); d = ImageDraw.Draw(img); d.arc([px(70), px(90), px(120), px(130)], 200, 340, fill=H('#d8b048'), width=px(2))
    save(img, 'b2_baku', 'Баку — пожиратель кошмаров', C, 'b', 150)
    img = canvas(120, 190); floor_shadow(img, 60, 184, 44)                                     # incense
    fill(img, '#6a6d66', 126, ell=(14, 150, 106, 184), scale=4, contrast=1.3); volume(img, (14, 150, 106, 184), .5, .3)
    for k, x in enumerate((48, 60, 72)): line(img, [(x, 160), (x + (k - 1) * 8, 90)], '#6a3a2a', 1.6); ell(img, (x + (k - 1) * 8 - 2, 86, x + (k - 1) * 8 + 2, 90), '#e04020')
    for k in range(5): soft(img, lambda d, k=k: d.ellipse([px(50 + math.sin(k) * 14), px(70 - k * 14), px(70 + math.sin(k) * 14), px(84 - k * 14)], fill=(200, 200, 205, 90)), 4)
    save(img, 'b2_incense', 'Палочки благовоний', C, 'b', 30)
    img = canvas(140, 90); floor_shadow(img, 70, 84, 60)                                       # letters
    for k in range(4): fill(img, '#efe6d0', 127 + k, poly=[(20 + k * 3, 80 - k * 10), (120 - k * 2, 80 - k * 10), (116, 60 - k * 10), (24, 60 - k * 10)], scale=3, contrast=.3)
    rope(img, [(70, 30), (70, 80)], '#c02a2a', 3); rope(img, [(20, 58), (120, 58)], '#c02a2a', 3)
    save(img, 'b2_letters', 'Стопка писем', C, 'b', 30)
    img = canvas(130, 190); floor_shadow(img, 65, 184, 50)                                     # bronze mirror
    fill(img, '#2a1a14', 131, rect=(30, 160, 100, 184), scale=4); line(img, [(65, 160), (65, 130)], '#2a1a14', 6)
    fill(img, '#8a6a2a', 132, ell=(10, 20, 120, 130), scale=3, contrast=1.3); fill(img, '#c8b88a', 133, ell=(22, 32, 108, 118), scale=4, contrast=.5)
    volume(img, (22, 32, 108, 118), .6, .3, spec=.6)
    save(img, 'b2_kagami', 'Бронзовое зеркало', C, 'b', 80)
    img = canvas(140, 300); rr = random.Random(9)                                               # senbazuru
    for s in range(4):
        x = 20 + s * 33; line(img, [(x, 0), (x, 290)], '#c8c0b0', 1)
        for k in range(10):
            y = 16 + k * 28; c = H(rr.choice(['#d8384a', '#e8a0b6', '#3a5a9a', '#e8c040', '#2f6a3a', '#f4f0e6']))
            poly(img, [(x - 11, y + 6), (x, y), (x + 11, y + 6), (x, y + 12)], c); poly(img, [(x, y), (x + 6, y - 6), (x + 3, y + 2)], dk(c, .2))
    save(img, 'b2_senbazuru', 'Тысяча журавликов', C, 't', 90)
    img = canvas(130, 150); line(img, [(65, 0), (65, 20)], '#1a1410', 2)                         # paper ball lamp
    soft(img, lambda d: d.ellipse([px(0), px(10), px(130), px(150)], fill=(250, 220, 150, 90)), 10)
    fill(img, '#f4ead0', 134, ell=(12, 20, 118, 140), scale=5, contrast=.5)
    clip(img, mask_poly(img, ell=(12, 20, 118, 140)), lambda d: [d.arc([px(12), px(20 + k * 12), px(118), px(140 - k * 12)], 0, 360, fill=(200, 170, 120, 120), width=px(1)) for k in range(5)])
    save(img, 'b2_paperlamp', 'Бумажный шар-светильник', C, 't', 70, glow=[65, 80])
    img = canvas(240, 170); floor_shadow(img, 120, 164, 110)                                   # writing desk
    fill(img, '#4a2a1a', 135, rect=(10, 70, 230, 88), scale=5, stretch=(6, .5)); fill(img, '#3a2014', 136, rect=(20, 88, 40, 164), scale=4); fill(img, '#3a2014', 137, rect=(200, 88, 220, 164), scale=4)
    fill(img, '#efe6d0', 138, rect=(40, 52, 130, 70), scale=3, contrast=.2); text(img, '心', 85, 61, 12, '#1a1410', SERIF)
    fill(img, '#2a2622', 139, rect=(150, 54, 196, 70), scale=3); line(img, [(160, 50), (196, 20)], '#8a6038', 3); ell(img, (190, 14, 200, 24), '#1a1410')
    volume(img, (10, 14, 230, 164), .35, .2)
    save(img, 'b2_tsukue', 'Столик для письма', C, 'b', 110)
    img = canvas(200, 250); rack(img, '#2a3a6a', 140, 'asagao', True, 200, 250)
    save(img, 'b2_yukata', 'Юката на вешалке', C, 'b', 120)
    img = canvas(200, 150); floor_shadow(img, 100, 144, 90)                                    # toy box
    fill(img, '#8a5a30', 150, rect=(14, 70, 186, 144), scale=6, stretch=(4, .5))
    for k, (x, c) in enumerate(((50, '#c02a2a'), (80, '#2a4a8a'), (120, '#e8c040'))): I.ell(img, (x - 18, 40, x + 18, 76), c); volume(img, (x - 18, 40, x + 18, 76), .6, .4, spec=.3)
    line(img, [(150, 70), (170, 20)], '#8a6038', 3); I.ell(img, (160, 6, 184, 30), '#c02a2a'); poly(img, [(94, 70), (110, 40), (126, 70)], '#d8384a')
    volume(img, (14, 70, 186, 144), .4, .2)
    save(img, 'b2_toybox', 'Ящик с игрушками', C, 'b', 60)
    img = canvas(190, 160); floor_shadow(img, 95, 154, 86)                                     # cushion stack
    for k, c in enumerate(('#2a3a6a', '#b8322a', '#2f6a3a', '#8a5a2a')):
        y = 150 - k * 30; fill(img, c, 155 + k, poly=[(14, y), (176, y), (170, y - 26), (20, y - 26)], scale=5, contrast=.7); volume(img, (14, y - 26, 176, y), .45, .3)
        for x, yy in ((20, y - 26), (170, y - 26)): I.ell(img, (x - 4, yy - 4, x + 4, yy + 4), dk(H(c), .3))
    save(img, 'b2_zabutons', 'Стопка дзабутонов', C, 'b', 60)

def stone_blk(img, x0, y0, x1, y1, seed, col='#6a6d66', moss=True):
    P.stone(img, (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2, seed, hexc(col), moss)


def bamboo(img, x, y0, y1, w, seed, col='#8aa050'):
    fill(img, col, seed, rect=(x - w / 2, y0, x + w / 2, y1), scale=4, stretch=(.3, 4), contrast=.8); volume(img, (x - w / 2, y0, x + w / 2, y1), .6, .4, spec=.2)
    for yy in range(int(y0) + 26, int(y1), 34): ImageDraw.Draw(img).line([(px(x - w / 2), px(yy)), (px(x + w / 2), px(yy))], fill=dk(H(col), .4), width=px(2))


# ───────────────────────────── ОНСЭН (+18) ─────────────────────────────
def onsen():
    C = 'Онсэн'
    img = canvas(300, 280); floor_shadow(img, 150, 274, 140)                                   # bamboo screen
    for k in range(13): bamboo(img, 18 + k * 22, 20 + (k % 3) * 6, 270, 20, 200 + k, '#9aa860' if k % 2 else '#8a9a50')
    for y in (70, 200): rope(img, [(8, y), (292, y)], '#2a2018', 4)
    save(img, 'o2_takegaki', 'Бамбуковая ширма', C, 'b', 110)
    img = canvas(170, 190); floor_shadow(img, 85, 184, 76)                                     # bucket of towels
    fill(img, WOOD_L, 201, poly=[(22, 90), (148, 90), (136, 184), (34, 184)], scale=6, stretch=(.4, 3)); [rope(img, [(24, y), (85, y + 3), (146, y)], '#2a2018', 3) for y in (110, 168)]
    volume(img, (22, 90, 148, 184), .45, .3)
    for k, (x, c) in enumerate(((56, '#f2eee4'), (86, '#e8a0b6'), (116, '#9ac0d8'))): blob(img, [(x - 26, 96), (x - 20, 50), (x, 36), (x + 20, 50), (x + 26, 96)], hexc(c), 202 + k, scale=3, k=.4)
    save(img, 'o2_towelbucket', 'Ведро со свёрнутыми полотенцами', C, 'b', 50)
    img = canvas(130, 230); floor_shadow(img, 65, 224, 56); P.toro(img, 65, 224, 200, 204)       # mossy lantern
    soft(img, lambda d: d.ellipse([px(45), px(64), px(85), px(92)], fill=(255, 200, 110, 190)), 5)
    save(img, 'o2_toro', 'Замшелый фонарь', C, 'b', 140, glow=[65, 78])
    img = canvas(240, 210); floor_shadow(img, 120, 204, 116); barrel(img, 120, 204, 220, 150, '#a88458', 205)  # ofuro tub
    fill(img, '#8ab0b8', 206, ell=(24, 44, 216, 70), scale=4, contrast=.5)
    for k in range(4): soft(img, lambda d, k=k: d.ellipse([px(50 + k * 40), px(10 - k % 2 * 6), px(90 + k * 40), px(56)], fill=(240, 240, 240, 80)), 7)
    save(img, 'o2_ofuro', 'Деревянная бочка-офуро', C, 'b', 220)
    img = canvas(190, 150); floor_shadow(img, 95, 144, 86)                                     # basket of bath things
    fill(img, '#b08a50', 207, poly=[(20, 70), (170, 70), (156, 144), (34, 144)], scale=4, stretch=(4, 1), contrast=1.2)
    clip(img, mask_poly(img, poly=[(20, 70), (170, 70), (156, 144), (34, 144)]), lambda d: [d.line([(px(x), px(70)), (px(x - 8), px(144))], fill=(110, 80, 40, 150), width=px(1.4)) for x in range(24, 170, 9)])
    fill(img, '#e8c040', 208, rect=(40, 30, 70, 76), scale=3); fill(img, '#f2eee4', 209, rect=(76, 20, 104, 76), scale=3); fill(img, '#c02a4a', 210, rect=(110, 40, 136, 76), scale=3)
    text(img, '湯', 90, 48, 16, '#1a1410', SERIF); fill(img, '#9ac0d8', 211, ell=(132, 48, 166, 80), scale=3); volume(img, (20, 20, 170, 144), .4, .25, spec=.2)
    save(img, 'o2_bathkit', 'Корзинка банных вещей', C, 'b', 40)
    img = canvas(120, 180); ell(img, (56, 4, 64, 12), '#8a8a80'); line(img, [(60, 8), (60, 110)], '#8a6038', 4)  # uchiwa on a nail
    fill(img, '#f2eee4', 212, ell=(10, 10, 110, 110), scale=4, contrast=.4); ImageDraw.Draw(img).ellipse([px(10), px(10), px(110), px(110)], outline=H('#2a4a7a'), width=px(3))
    for k in range(3): ImageDraw.Draw(img).arc([px(20 + k * 8), px(56 + k * 6), px(100 - k * 8), px(106 - k * 2)], 200, 340, fill=H('#3a6aa8'), width=px(3))
    text(img, '湯', 60, 44, 30, '#b8322a', SERIF); line(img, [(60, 108), (60, 176)], '#8a6038', 6)
    save(img, 'o2_uchiwa', 'Утива «Юи» на гвоздике', C, 't', 30)
    img = canvas(260, 220); floor_shadow(img, 150, 214, 110)                                   # kakei spout into stone
    stone_blk(img, 120, 150, 250, 214, 213)
    fill(img, '#4a6a70', 214, ell=(140, 150, 230, 176), scale=3, contrast=.5)
    bamboo(img, 40, 40, 214, 22, 215, '#8a9a50'); fill(img, '#8a9a50', 216, poly=[(40, 60), (190, 100), (190, 116), (40, 80)], scale=4, stretch=(4, .3)); volume(img, (40, 60, 190, 116), .5, .4)
    ImageDraw.Draw(img).line([(px(190), px(110)), (px(192), px(160))], fill=(200, 225, 235, 200), width=px(5))
    save(img, 'o2_kakei', 'Бамбуковый жёлоб какэи', C, 'b', 150)
    img = canvas(160, 130); floor_shadow(img, 80, 124, 70)                                     # onsen eggs
    fill(img, '#b08a50', 217, ell=(10, 50, 150, 124), scale=4, stretch=(4, 1), contrast=1.2)
    for k, (x, y) in enumerate(((50, 60), (80, 50), (110, 60), (66, 76), (96, 76))): fill(img, '#f2ead8', 218 + k, ell=(x - 16, y - 20, x + 16, y + 20), scale=2, contrast=.3); volume(img, (x - 16, y - 20, x + 16, y + 20), .6, .4, spec=.3)
    save(img, 'o2_tamago', 'Онсэн-тамаго в корзинке', C, 'b', 30)
    img = canvas(200, 130); floor_shadow(img, 100, 124, 90)                                    # floating sake tray
    fill(img, WOOD, 223, poly=[(10, 90), (190, 90), (176, 120), (24, 120)], scale=5, stretch=(4, .5)); volume(img, (10, 90, 190, 120), .4, .2)
    fill(img, '#f2eee4', 224, poly=[(56, 92), (84, 92), (90, 40), (78, 24), (62, 24), (50, 40)], scale=3, contrast=.4); volume(img, (50, 24, 90, 92), .6, .4, spec=.4); text(img, '酒', 70, 64, 18, '#2a4a7a', SERIF)
    for x in (120, 150): fill(img, '#c02a2a', 225 + x, ell=(x - 14, 76, x + 14, 92), scale=3); volume(img, (x - 14, 76, x + 14, 92), .5, .3, spec=.3)
    save(img, 'o2_sake', 'Плавающий поднос с сакэ', C, 'b', 90)
    img = canvas(200, 180); fill(img, WOOD_D, 226, rect=(0, 10, 200, 26), scale=5)             # scrubs on pegs
    for k, (x, c) in enumerate(((40, '#c8a870'), (100, '#e8e0cc'), (160, '#e8a0b6'))):
        ell(img, (x - 5, 24, x + 5, 34), '#3a2418'); line(img, [(x, 32), (x, 60)], '#e8e0cc', 1.4)
        m = fill(img, c, 227 + k, poly=[(x - 22, 60), (x + 22, 60), (x + 26, 170), (x - 26, 170)], scale=2, contrast=1.4)
        clip(img, m, lambda d, x=x: [d.line([(px(x - 26), px(y)), (px(x + 26), px(y + 6))], fill=(0, 0, 0, 50), width=px(2)) for y in range(60, 170, 8)])
    save(img, 'o2_scrubs', 'Мочалки на крючках', C, 't', 30)
    img = canvas(170, 160); floor_shadow(img, 85, 154, 76)                                     # coffee milk crate
    fill(img, '#c02a2a', 229, rect=(14, 90, 156, 154), scale=4); volume(img, (14, 90, 156, 154), .4, .2)
    for k, x in enumerate((40, 70, 100, 130)):
        glass(img, [(x - 12, 100), (x + 12, 100), (x + 12, 40), (x + 8, 26), (x - 8, 26), (x - 12, 40)], 230 + k, (170, 120, 70) if k % 2 else (230, 225, 210))
        fill(img, '#e8c040' if k % 2 else '#3a6aa8', 234 + k, ell=(x - 9, 18, x + 9, 30), scale=2)
    save(img, 'o2_coffeemilk', 'Ящик кофейного молока', C, 'b', 40)
    img = canvas(300, 130); floor_shadow(img, 150, 124, 140)                                   # changing bench
    fill(img, '#b88a58', 238, rect=(10, 50, 290, 72), scale=5, stretch=(8, .5))
    for x in (30, 260): fill(img, '#8a6038', 239 + x, rect=(x, 72, x + 16, 124), scale=4)
    fill(img, '#2a3a6a', 240, poly=[(170, 50), (250, 50), (240, 30), (180, 30)], scale=4); volume(img, (10, 30, 290, 124), .35, .2)
    save(img, 'o2_bench', 'Скамья в раздевалке', C, 'b', 90)
    img = canvas(320, 200); line(img, [(100, 10), (160, 0), (220, 10)], '#1a120c', 1.4)         # sento Fuji mural
    fill(img, '#e8e0d0', 241, rect=(10, 10, 310, 196), scale=6, contrast=.2)
    for k in range(10): fill(img, '#7ab0d8' if k % 2 else '#88bce0', 242 + k, rect=(10 + k * 30, 10, 40 + k * 30, 100), scale=6, contrast=.2)
    poly(img, [(40, 170), (160, 50), (180, 50), (300, 170)], '#3a5a8a'); poly(img, [(140, 70), (160, 50), (180, 50), (200, 70), (184, 64), (170, 78), (156, 64)], '#f4f0e6')
    fill(img, '#2f5a3a', 252, poly=[(10, 196), (10, 150), (60, 160), (110, 176), (110, 196)], scale=3); fill(img, '#2f5a3a', 253, poly=[(310, 196), (310, 140), (250, 164), (220, 196)], scale=3)
    fill(img, '#5a8ab8', 254, rect=(10, 170, 310, 196), scale=3, stretch=(6, .3), contrast=.5)
    save(img, 'o2_sento_fuji', 'Роспись «Фудзи», как в сэнто', C, 't', 240)
    img = canvas(170, 140); floor_shadow(img, 85, 134, 80); stone_blk(img, 10, 40, 160, 134, 255, '#5a5c56')  # stone basin
    fill(img, '#3a5a60', 256, ell=(30, 44, 140, 72), scale=3, contrast=.5); ImageDraw.Draw(img).ellipse([px(60), px(50), px(80), px(60)], fill=(230, 240, 245, 150))
    save(img, 'o2_basin', 'Каменная чаша с водой', C, 'b', 100)
    img = canvas(180, 150); floor_shadow(img, 90, 144, 80)                                     # folded yukata with obi
    fill(img, '#2a3a6a', 257, poly=[(20, 144), (160, 144), (166, 70), (14, 70)], scale=4, contrast=.6)
    flowers(img, 90, 108, 60, 26, ['#f2eee4', '#9ac0d8'], 12, 258, (5, 8)); fill(img, '#d8a040', 259, rect=(14, 60, 166, 76), scale=3)
    poly(img, [(70, 60), (90, 40), (110, 60)], '#f2eee4'); volume(img, (14, 40, 166, 144), .4, .25)
    save(img, 'o2_yukata', 'Сложенная юката', C, 'b', 70)
    img = canvas(220, 110); floor_shadow(img, 110, 104, 100)                                   # duck family
    for k, (x, sc) in enumerate(((60, 1.3), (120, .8), (160, .7), (196, .6))):
        blob(img, [(x - 34 * sc, 100), (x - 30 * sc, 76), (x + 30 * sc, 70), (x + 34 * sc, 96)], hexc('#f0c830'), 260 + k, scale=2, k=.5, spec=.3)
        blob(img, [(x + 4 * sc, 74), (x + 2 * sc, 48), (x + 20 * sc, 38), (x + 34 * sc, 50), (x + 30 * sc, 74)], hexc('#f0c830'), 264 + k, scale=2, k=.5, spec=.3)
        poly(img, [(x + 32 * sc, 52), (x + 46 * sc, 56), (x + 32 * sc, 62)], '#e07020'); ell(img, (x + 20 * sc, 48, x + 25 * sc, 53), '#1a1414')
    save(img, 'o2_ducks', 'Семейка уточек', C, 'b', 40)
    img = canvas(130, 200); floor_shadow(img, 65, 194, 56)                                     # old scales
    fill(img, '#f2eee4', 268, rect=(20, 170, 110, 194), scale=3, contrast=.4); line(img, [(65, 170), (65, 110)], '#8a8a80', 6)
    fill(img, '#e8e0cc', 269, ell=(14, 20, 116, 122), scale=3, contrast=.4); ImageDraw.Draw(img).ellipse([px(14), px(20), px(116), px(122)], outline=H('#8a8a80'), width=px(5))
    d = ImageDraw.Draw(img); [d.line([(px(65 + math.cos(a) * 42), px(71 + math.sin(a) * 42)), (px(65 + math.cos(a) * 36), px(71 + math.sin(a) * 36))], fill=H('#1a1410'), width=px(1.4)) for a in [math.pi * (1 + t / 12) for t in range(13)]]
    line(img, [(65, 71), (40, 50)], '#c02a2a', 2); volume(img, (14, 20, 116, 122), .4, .3, spec=.3)
    save(img, 'o2_scales', 'Старые банные весы', C, 'b', 60)
    img = canvas(150, 90); floor_shadow(img, 75, 84, 66)                                       # petals bowl
    fill(img, WOOD_L, 270, poly=[(14, 44), (136, 44), (116, 84), (34, 84)], scale=5, stretch=(4, .5)); fill(img, '#8ab0b8', 271, ell=(16, 36, 134, 56), scale=3, contrast=.4)
    flowers(img, 75, 44, 50, 8, ['#f4c4d2', '#e8a0b6', '#f8dde4'], 16, 272, (4, 6))
    save(img, 'o2_petals', 'Кадка с лепестками', C, 'b', 40)


# ───────────────────────────── ГАРДЕРОБ (+21) ─────────────────────────────
def wardrobe():
    C = 'Гардероб'
    for k, (iid, name, col, pat) in enumerate((('wr2_tsuru', 'Чёрное кимоно с журавлями', '#1a1a22', 'tsuru'), ('wr2_sakura', 'Розовое кимоно с сакурой', '#e8a0b6', 'sakura'),
                                                ('wr2_fuji', 'Кимоно «Глициния»', '#e8e0f0', 'fuji'), ('wr2_yukata', 'Летняя юката с вьюнком', '#f2eee4', 'asagao'))):
        img = canvas(300, 330); rack(img, col, 300 + k * 10, pat); save(img, iid, name, C, 'b', 220)
    img = canvas(240, 260); floor_shadow(img, 120, 254, 100)                                   # haori on a stand
    fill(img, '#1a120c', 340, rect=(10, 20, 230, 30), scale=4); fill(img, '#1a120c', 341, rect=(114, 30, 126, 250), scale=4); fill(img, '#1a120c', 342, rect=(60, 240, 180, 254), scale=4)
    m = fill(img, '#2a2a3a', 343, poly=[(20, 32), (220, 32), (214, 140), (170, 150), (172, 230), (68, 230), (70, 150), (26, 140)], scale=8, contrast=.7)
    clip(img, m, lambda d: [d.line([(px(x), px(32)), (px(x), px(230))], fill=(90, 90, 120, 80), width=px(1)) for x in range(20, 220, 8)])
    clip(img, m, lambda d: d.rectangle([px(20), px(32), px(220), px(58)], fill=(160, 40, 40, 255)))
    ImageDraw.Draw(img).ellipse([px(104), px(70), px(136), px(102)], outline=H('#f2eee4'), width=px(2))
    for k in range(5): a = k / 5 * math.tau - math.pi / 2; ell(img, (120 + math.cos(a) * 8 - 5, 86 + math.sin(a) * 8 - 5, 120 + math.cos(a) * 8 + 5, 86 + math.sin(a) * 8 + 5), '#f2eee4')
    volume(img, (20, 32, 220, 230), .35, .2)
    save(img, 'wr2_haori', 'Накидка хаори', C, 'b', 180)
    img = canvas(200, 250); floor_shadow(img, 100, 244, 90)                                    # hakama
    m = fill(img, '#4a2a3a', 344, poly=[(50, 20), (150, 20), (180, 244), (104, 244), (100, 150), (96, 244), (20, 244)], scale=8, stretch=(.4, 3), contrast=.8)
    clip(img, m, lambda d: [d.line([(px(60 + k * 16), px(30)), (px(40 + k * 22), px(244))], fill=(0, 0, 0, 60), width=px(2)) for k in range(7)])
    fill(img, '#e8e0cc', 345, rect=(46, 14, 154, 30), scale=3); save(img, 'wr2_hakama', 'Штаны-юбка хакама', C, 'b', 150)
    img = canvas(160, 300); floor_shadow(img, 80, 294, 60)                                     # dress form
    fill(img, '#2a1a14', 346, rect=(40, 278, 120, 294), scale=4); line(img, [(80, 278), (80, 220)], '#2a1a14', 6)
    m = fill(img, '#b8322a', 347, poly=[(40, 30), (120, 30), (130, 80), (116, 150), (126, 222), (34, 222), (44, 150), (30, 80)], scale=8, contrast=.7)
    clip(img, m, lambda d: d.polygon([(px(60), px(30)), (px(80), px(90)), (px(100), px(30))], fill=(242, 238, 228, 255)))
    fill(img, '#d8b048', 348, rect=(38, 120, 122, 150), scale=3); ell(img, (70, 16, 90, 34), '#2a1a14'); volume(img, (30, 16, 130, 222), .5, .35)
    save(img, 'wr2_dressform', 'Манекен в кимоно', C, 'b', 200)
    img = canvas(200, 170); floor_shadow(img, 100, 164, 92)                                    # folded kimono stack
    for k, c in enumerate(('#2a3a6a', '#b8322a', '#2f6a3a', '#e8a0b6', '#d8b048')):
        y = 162 - k * 26; fill(img, c, 350 + k, poly=[(20, y), (180, y), (176, y - 24), (24, y - 24)], scale=5, contrast=.5); volume(img, (20, y - 24, 180, y), .4, .25)
        ImageDraw.Draw(img).line([(px(24), px(y - 6)), (px(176), px(y - 6))], fill=lt(H(c), .3), width=px(1.2))
    rope(img, [(100, 30), (100, 162)], '#d8b048', 2)
    save(img, 'wr2_stack', 'Стопка сложенных кимоно', C, 'b', 90)
    img = canvas(180, 110); floor_shadow(img, 90, 104, 80)                                     # combs on a cloth
    fill(img, '#b8322a', 355, poly=[(10, 60), (170, 60), (160, 104), (20, 104)], scale=4, contrast=.5)
    for k, (x, c) in enumerate(((56, '#2a1410'), (124, '#d8b048'))):
        fill(img, c, 356 + k, poly=[(x - 36, 60), (x + 36, 60), (x + 30, 30), (x - 30, 30)], scale=3); volume(img, (x - 36, 30, x + 36, 60), .5, .4, spec=.4)
        d = ImageDraw.Draw(img); [d.line([(px(x - 32 + t * 4), px(60)), (px(x - 32 + t * 4), px(76))], fill=H(c), width=px(1.6)) for t in range(17)]
    flowers(img, 56, 40, 16, 4, ['#f4c4d2'], 3, 358, (4, 5))
    save(img, 'wr2_kushi', 'Гребни куси', C, 'b', 70)
    img = canvas(150, 320); floor_shadow(img, 75, 314, 64)                                     # standing mirror
    fill(img, '#3a2014', 359, rect=(14, 10, 136, 300), scale=5); fill(img, '#c8d8dc', 360, rect=(28, 24, 122, 286), scale=6, contrast=.3)
    volume(img, (28, 24, 122, 286), .4, .2, spec=.5); fill(img, '#b8322a', 361, rect=(14, 10, 136, 70), scale=4, contrast=.6)
    flowers(img, 75, 40, 50, 20, ['#f2eee4', '#e8a0b6'], 7, 362, (5, 8)); fill(img, '#3a2014', 363, rect=(4, 296, 146, 314), scale=4)
    save(img, 'wr2_mirror', 'Зеркало в рост с накидкой', C, 'b', 170)
    img = canvas(200, 150); floor_shadow(img, 100, 144, 92)                                    # box of masks
    fill(img, WOOD_L, 364, rect=(14, 80, 186, 144), scale=6, stretch=(4, .5))
    for k, (x, c, e) in enumerate(((50, '#f2eee4', '#c02a2a'), (100, '#c02a2a', '#1a1414'), (150, '#f0e0c8', '#1a1414'))):
        blob(img, [(x - 24, 84), (x - 26, 40), (x, 24), (x + 26, 40), (x + 24, 84)], hexc(c), 365 + k, scale=3, k=.4, spec=.2)
        for sx in (-1, 1): ell(img, (x + sx * 10 - 5, 46, x + sx * 10 + 5, 52), e)
    volume(img, (14, 80, 186, 144), .4, .2)
    save(img, 'wr2_maskbox', 'Ящик с масками', C, 'b', 80)
    img = canvas(240, 200); fill(img, WOOD_D, 368, rect=(0, 150, 240, 166), scale=5)            # shelf of hats
    for k, (x, c) in enumerate(((50, '#c8ab6d'), (130, '#2a2a2a'), (200, '#b8975a'))):
        m = fill(img, c, 369 + k, poly=[(x - 44, 150), (x, 96 + k * 6), (x + 44, 150)], scale=3, stretch=(3, 1), contrast=1.1)
        clip(img, m, lambda d, x=x, k=k: [d.line([(px(x), px(96 + k * 6)), (px(x + t * 11), px(150))], fill=(0, 0, 0, 60), width=px(1)) for t in range(-4, 5)])
    save(img, 'wr2_kasa', 'Полка с шляпами каса', C, 't', 80)
    img = canvas(220, 230); floor_shadow(img, 110, 224, 96)                                    # obi on a stand
    fill(img, '#1a120c', 374, rect=(20, 40, 32, 224), scale=4); fill(img, '#1a120c', 375, rect=(188, 40, 200, 224), scale=4); fill(img, '#1a120c', 376, rect=(10, 30, 210, 44), scale=4)
    m = fill(img, '#d8b048', 377, poly=[(36, 44), (184, 44), (184, 200), (36, 200)], scale=6, stretch=(.4, 3), contrast=.9)
    clip(img, m, lambda d: [d.ellipse([px(x - 14), px(y - 14), px(x + 14), px(y + 14)], outline=(160, 40, 40, 200), width=px(3)) for x in range(56, 184, 36) for y in range(64, 200, 36)])
    volume(img, (36, 44, 184, 200), .35, .2, spec=.2)
    save(img, 'wr2_obistand', 'Парчовый оби на стойке', C, 'b', 190)
    img = canvas(200, 120); floor_shadow(img, 100, 114, 90)                                    # thread spools
    fill(img, WOOD, 378, rect=(10, 94, 190, 114), scale=5)
    for k, (x, c) in enumerate(((34, '#c02a2a'), (70, '#2a4a8a'), (106, '#d8b048'), (142, '#2f6a3a'), (174, '#e8a0b6'))):
        fill(img, WOOD_L, 379 + k, rect=(x - 14, 30, x + 14, 38), scale=2); fill(img, WOOD_L, 384 + k, rect=(x - 14, 86, x + 14, 94), scale=2)
        m = fill(img, c, 389 + k, rect=(x - 12, 38, x + 12, 86), scale=2, contrast=.6); clip(img, m, lambda d, x=x: [d.line([(px(x - 12), px(y)), (px(x + 12), px(y + 2))], fill=(0, 0, 0, 50), width=px(1)) for y in range(38, 86, 3)])
        volume(img, (x - 14, 30, x + 14, 94), .6, .4, spec=.2)
    save(img, 'wr2_spools', 'Катушки шёлковых ниток', C, 'b', 40)
    img = canvas(190, 120); floor_shadow(img, 95, 114, 80)                                     # charcoal iron
    blob(img, [(20, 110), (24, 70), (70, 50), (130, 50), (150, 70), (150, 110)], hexc('#2a2622'), 394, scale=3, spec=.2)
    soft(img, lambda d: d.ellipse([px(40), px(46), px(130), px(70)], fill=(230, 90, 40, 170)), 5); line(img, [(150, 80), (186, 60)], WOOD, 8)
    save(img, 'wr2_iron', 'Угольный утюг хиноси', C, 'b', 50)
    img = canvas(220, 170); floor_shadow(img, 110, 164, 100)                                   # rolls of cloth
    for k, (x, y, c) in enumerate(((50, 130, '#b8322a'), (110, 130, '#2a3a6a'), (170, 130, '#2f6a3a'), (80, 80, '#d8b048'), (140, 80, '#e8a0b6'))):
        fill(img, c, 395 + k, ell=(x - 32, y - 32, x + 32, y + 32), scale=3, contrast=.6); ImageDraw.Draw(img).ellipse([px(x - 12), px(y - 12), px(x + 12), px(y + 12)], fill=dk(H(c), .3))
        ImageDraw.Draw(img).ellipse([px(x - 5), px(y - 5), px(x + 5), px(y + 5)], fill=H(WOOD_L)); volume(img, (x - 32, y - 32, x + 32, y + 32), .5, .3)
    save(img, 'wr2_rolls', 'Рулоны ткани тан', C, 'b', 90)
    img = canvas(160, 110); floor_shadow(img, 80, 104, 70)                                     # tabi socks
    for k, x in enumerate((50, 110)):
        fill(img, '#f4f0e6', 400 + k, poly=[(x - 20, 10), (x + 16, 10), (x + 18, 70), (x + 36, 84), (x + 30, 100), (x - 26, 100), (x - 24, 70)], scale=3, contrast=.4)
        line(img, [(x + 18, 80), (x + 22, 100)], '#c8c0b0', 1.6); volume(img, (x - 26, 10, x + 36, 100), .5, .3)
    save(img, 'wr2_tabi', 'Носки таби', C, 'b', 20)
    img = canvas(170, 110); floor_shadow(img, 85, 104, 76)                                     # okobo
    for k, x in enumerate((50, 120)):
        fill(img, '#2a1410', 402 + k, poly=[(x - 26, 100), (x + 26, 100), (x + 22, 50), (x - 22, 50)], scale=3, stretch=(.3, 3)); volume(img, (x - 26, 50, x + 26, 100), .5, .3, spec=.4)
        fill(img, '#c02a2a', 404 + k, ell=(x - 24, 36, x + 24, 56), scale=2); line(img, [(x - 10, 46), (x, 38), (x + 10, 46)], '#e8a0b6', 3)
    save(img, 'wr2_okobo', 'Высокие сандалии окобо', C, 'b', 60)
    img = canvas(240, 200); floor_shadow(img, 120, 194, 110)                                   # open trunk with kimono
    fill(img, '#3a2014', 406, rect=(20, 100, 220, 194), scale=6, stretch=(4, .5)); fill(img, '#2a1410', 407, poly=[(20, 100), (220, 100), (230, 20), (30, 30)], scale=6)
    for x in (40, 200): ImageDraw.Draw(img).rectangle([px(x - 8), px(110), px(x + 8), px(184)], fill=H('#b8975a'))
    blob(img, [(36, 110), (60, 80), (120, 70), (180, 84), (204, 110)], hexc('#b8322a'), 408, scale=4, k=.3); flowers(img, 120, 92, 60, 10, ['#f2eee4', '#d8b048'], 10, 409, (5, 7))
    line(img, [(160, 100), (190, 160)], '#e8a0b6', 7); volume(img, (20, 20, 230, 194), .35, .2)
    save(img, 'wr2_chest', 'Открытый сундук с нарядами', C, 'b', 150)
    img = canvas(140, 290); floor_shadow(img, 70, 284, 60)                                     # umbrella stand
    for k, (x, c) in enumerate(((50, '#b8322a'), (74, '#2a3a6a'), (94, '#d8b048'))):
        fill(img, c, 410 + k, poly=[(x - 14, 60), (x + 14, 60), (x + 6, 200), (x - 6, 200)], scale=3, stretch=(.3, 3)); line(img, [(x, 60), (x, 20)], WOOD_D, 3); ell(img, (x - 4, 14, x + 4, 22), '#1a1410')
    barrel(img, 70, 284, 100, 110, '#6a4a30', 413)
    save(img, 'wr2_kasatate', 'Подставка для зонтиков', C, 'b', 70)
    img = canvas(130, 150); floor_shadow(img, 65, 144, 54)                                     # kinchaku
    blob(img, [(20, 140), (14, 90), (30, 50), (65, 44), (100, 50), (116, 90), (110, 140)], hexc('#6a3a8a'), 414, scale=3, k=.4)
    flowers(img, 65, 100, 30, 20, ['#f4c4d2', '#f2eee4'], 6, 415, (6, 9)); rope(img, [(30, 52), (65, 60), (100, 52)], '#d8b048', 3)
    line(img, [(50, 50), (40, 10), (90, 10), (80, 50)], '#d8b048', 3)
    save(img, 'wr2_kinchaku', 'Мешочек кинтяку', C, 'b', 40)


# ───────────────────────────── ДВОРИК (+22) ─────────────────────────────
def courtyard():
    C = 'Дворик'
    img = canvas(160, 300); floor_shadow(img, 80, 294, 70)                                     # kasuga lantern
    stone_blk(img, 30, 270, 130, 294, 500); stone_blk(img, 66, 150, 94, 272, 501); stone_blk(img, 40, 130, 120, 152, 502)
    stone_blk(img, 50, 80, 110, 132, 503); ImageDraw.Draw(img).rectangle([px(64), px(92), px(96), px(122)], fill=H('#1a1410'))
    soft(img, lambda d: d.ellipse([px(58), px(88), px(102), px(126)], fill=(255, 200, 110, 200)), 5)
    poly(img, [(20, 82), (80, 40), (140, 82)], '#5a5c56'); volume(img, (20, 40, 140, 82), .5, .3); stone_blk(img, 70, 20, 90, 44, 504)
    save(img, 'c2_kasuga', 'Каменный фонарь касуга', C, 'b', 200, glow=[80, 107])
    img = canvas(280, 90); floor_shadow(img, 140, 84, 130); stone_blk(img, 10, 30, 270, 76, 505, '#7a7c74')  # slab bridge
    fill(img, '#3a5a60', 506, poly=[(0, 76), (280, 76), (280, 90), (0, 90)], scale=3, contrast=.5)
    save(img, 'c2_slab', 'Каменный мостик-плита', C, 'b', 110)
    img = canvas(320, 180); floor_shadow(img, 160, 174, 150)                                   # yotsume bamboo fence
    for x in range(20, 320, 50): bamboo(img, x, 20, 174, 12, 507 + x, '#b8a060')
    for y in (50, 100, 140): fill(img, '#a89050', 508 + y, rect=(4, y, 316, y + 10), scale=4, stretch=(6, .3)); volume(img, (4, y, 316, y + 10), .5, .4)
    for x in range(20, 320, 50):
        for y in (55, 105, 145): line(img, [(x - 8, y - 6), (x + 8, y + 6)], '#2a2018', 2)
    save(img, 'c2_fence', 'Бамбуковая изгородь ёцумэ', C, 'b', 90)
    img = canvas(140, 300); floor_shadow(img, 70, 294, 60)                                     # stone pagoda
    stone_blk(img, 30, 270, 110, 294, 510)
    for k in range(5):
        y = 262 - k * 46; w = 110 - k * 14; stone_blk(img, 70 - w / 4, y - 24, 70 + w / 4, y, 511 + k)
        poly(img, [(70 - w / 2, y - 22), (70 + w / 2, y - 22), (70 + w / 2 - 8, y - 36), (70 - w / 2 + 8, y - 36)], '#5a5c56'); volume(img, (70 - w / 2, y - 36, 70 + w / 2, y - 22), .5, .3)
    line(img, [(70, 36), (70, 4)], '#5a5c56', 5)
    save(img, 'c2_pagoda', 'Каменная пагода', C, 'b', 190)
    img = canvas(260, 150); floor_shadow(img, 130, 144, 124)                                   # karesansui box
    fill(img, WOOD_D, 516, poly=[(20, 50), (240, 50), (256, 144), (4, 144)], scale=5); m = fill(img, '#e0dccc', 517, poly=[(30, 58), (230, 58), (244, 136), (16, 136)], scale=3, contrast=.4)
    clip(img, m, lambda d: [d.line([(px(10), px(y)), (px(250), px(y))], fill=(150, 145, 130, 200), width=px(1.2)) for y in range(62, 136, 6)])
    for k, (x, y, r) in enumerate(((80, 90, 18), (170, 108, 12), (200, 80, 9))):
        clip(img, m, lambda d, x=x, y=y, r=r: [d.ellipse([px(x - r - t), px(y - r * .5 - t * .5), px(x + r + t), px(y + r * .5 + t * .5)], outline=(150, 145, 130, 220), width=px(1.2)) for t in range(6, 30, 6)])
        stone_blk(img, x - r, y - r * 1.2, x + r, y + r * .5, 518 + k, '#4a4d48')
    save(img, 'c2_karesansui', 'Сад камней в ящике', C, 'b', 160)
    img = canvas(220, 170); floor_shadow(img, 110, 164, 100)                                   # lotus bowl
    crock(img, 110, 164, 200, 90, '#4a5a6a', 521); fill(img, '#2a4a50', 522, ell=(26, 70, 194, 96), scale=3)
    for k, (x, y, r) in enumerate(((60, 80, 20), (150, 86, 18), (110, 76, 14))): fill(img, '#3a7a3a', 523 + k, ell=(x - r, y - r * .4, x + r, y + r * .4), scale=3)
    line(img, [(110, 80), (116, 30)], '#3a6a2a', 3)
    for k in range(7): a = math.pi * (1.1 + k / 6 * .8); poly(img, [(116, 30), (116 + math.cos(a - .2) * 20, 30 + math.sin(a - .2) * 22), (116 + math.cos(a) * 30, 30 + math.sin(a) * 30), (116 + math.cos(a + .2) * 20, 30 + math.sin(a + .2) * 22)], '#f0b0c4' if k % 2 else '#e890aa')
    save(img, 'c2_lotus', 'Чаша с лотосом', C, 'b', 120)
    img = canvas(260, 120); floor_shadow(img, 130, 114, 120)                                   # stone bench
    stone_blk(img, 30, 70, 70, 114, 526, '#6a6d66', False); stone_blk(img, 190, 70, 230, 114, 527, '#6a6d66', False); stone_blk(img, 10, 40, 250, 76, 528, '#7a7c74')
    save(img, 'c2_bench', 'Каменная скамья', C, 'b', 110)
    img = canvas(200, 150); floor_shadow(img, 100, 144, 90)                                    # shears + basket of cuttings
    fill(img, '#b08a50', 529, ell=(20, 70, 180, 144), scale=4, stretch=(4, 1), contrast=1.2); leaves(img, [(100, 76, 70, 20)], ['#2a5a2a', '#3a7a3a', '#4a8a3a'], 260, 530)
    line(img, [(40, 40), (130, 100)], '#8a8a90', 5); line(img, [(40, 60), (130, 90)], '#8a8a90', 5); fill(img, '#c02a2a', 531, ell=(14, 30, 50, 50), scale=2); fill(img, '#c02a2a', 532, ell=(14, 56, 50, 76), scale=2)
    save(img, 'c2_shears', 'Садовые ножницы и корзинка', C, 'b', 40)
    img = canvas(220, 290); floor_shadow(img, 110, 284, 100)                                   # well
    stone_blk(img, 20, 180, 200, 284, 533, '#5a5c56'); fill(img, '#1a1410', 534, ell=(34, 172, 186, 196), scale=3)
    for x in (30, 180): fill(img, WOOD_D, 535 + x, rect=(x, 40, x + 12, 190), scale=4)
    poly(img, [(0, 50), (110, 10), (220, 50), (210, 60), (110, 24), (10, 60)], '#3a2a1a'); fill(img, WOOD, 537, rect=(30, 70, 190, 78), scale=3)
    line(img, [(110, 78), (110, 130)], '#b8975a', 2); fill(img, WOOD_L, 538, poly=[(94, 130), (126, 130), (122, 160), (98, 160)], scale=3)
    save(img, 'c2_well', 'Колодец с ведёрком', C, 'b', 200)
    img = canvas(110, 240); line(img, [(55, 0), (55, 40)], '#1a1410', 2)                          # hanging bronze lantern
    poly(img, [(10, 70), (55, 40), (100, 70)], '#3a4a3a'); fill(img, '#4a5a4a', 539, rect=(24, 70, 86, 170), scale=3, contrast=1.3)
    for x in (34, 55, 76): ImageDraw.Draw(img).rectangle([px(x - 4), px(90), px(x + 4), px(150)], fill=(255, 200, 110, 230))
    poly(img, [(18, 170), (92, 170), (80, 190), (30, 190)], '#3a4a3a'); line(img, [(55, 190), (55, 236)], '#3a4a3a', 2); volume(img, (10, 40, 100, 190), .5, .3, spec=.2)
    save(img, 'c2_tsuridoro', 'Подвесной бронзовый фонарь', C, 't', 130, glow=[55, 120])
    img = canvas(200, 240); floor_shadow(img, 100, 234, 80)                                    # maple in a pot
    P.maple(img, px(100), px(180), px(200), 540, [hexc('#5a1a10'), hexc('#8a2a14'), hexc('#b8401a'), hexc('#d8602a'), hexc('#e88a3a')], P.BARK)
    pot(img, 100, 234, 120, 56, '#2a2a2a', 541)
    save(img, 'c2_maple', 'Красный клён в горшке', C, 'b', 150)
    img = canvas(220, 250); floor_shadow(img, 110, 244, 100)                                   # two crane statues
    for k, (x, up) in enumerate(((70, 1), (150, 0))):
        blob(img, [(x - 30, 170), (x - 20, 130), (x + 20, 124), (x + 36, 150), (x + 10, 176)], hexc('#5a6a60'), 542 + k, scale=3)
        line(img, [(x + 10, 132), (x + 16, 80 if up else 110), (x + 30, 60 if up else 100)], '#5a6a60', 7); poly(img, [(x + 30, 56 if up else 96), (x + 56, 64 if up else 104), (x + 30, 66 if up else 106)], '#4a5a50')
        line(img, [(x - 4, 172), (x - 4, 230)], '#4a5a50', 4); line(img, [(x + 8, 172), (x + 10, 230)], '#4a5a50', 4)
    figure_base(img, 110, 244, 200, '#4a4d48', 544)
    save(img, 'c2_cranes', 'Бронзовые журавли', C, 'b', 180)
    img = canvas(150, 200); floor_shadow(img, 75, 194, 60)                                     # moon rabbit
    figure_base(img, 75, 194, 110, '#5a5c56', 545)
    blob(img, [(30, 168), (24, 120), (60, 96), (104, 110), (120, 168)], hexc('#d8d4cc'), 546, scale=3)
    blob(img, [(50, 104), (46, 70), (74, 58), (100, 72), (96, 104)], hexc('#d8d4cc'), 547, scale=3)
    for x in (60, 82): blob(img, [(x - 6, 62), (x - 8, 20), (x, 8), (x + 8, 20), (x + 6, 62)], hexc('#d8d4cc'), 548 + x, scale=3)
    ell(img, (80, 78, 88, 86), '#c02a2a'); fill(img, WOOD, 549, ell=(96, 130, 136, 150), scale=3); line(img, [(108, 140), (100, 100)], WOOD_D, 5)
    save(img, 'c2_usagi', 'Лунный кролик с пестиком', C, 'b', 120)
    img = canvas(240, 150); floor_shadow(img, 120, 144, 110)                                   # wheelbarrow
    fill(img, WOOD, 550, poly=[(40, 50), (180, 50), (164, 110), (56, 110)], scale=5, stretch=(4, .5)); volume(img, (40, 50, 180, 110), .4, .2)
    blob(img, [(56, 54), (90, 30), (140, 34), (170, 54)], hexc('#5a4030'), 551, scale=3, k=.3); leaves(img, [(110, 40, 50, 14)], ['#2a5a2a', '#3a7a3a'], 120, 552)
    line(img, [(170, 80), (236, 60)], WOOD_D, 5); fill(img, '#2a2018', 553, ell=(20, 88, 76, 144), scale=3); ell(img, (40, 108, 56, 124), '#8a8a80')
    save(img, 'c2_cart', 'Садовая тачка с землёй', C, 'b', 70)
    img = canvas(200, 120); floor_shadow(img, 100, 114, 90)                                    # stone mushrooms
    for k, (x, h, r) in enumerate(((50, 70, 34), (120, 90, 44), (170, 50, 24))):
        stone_blk(img, x - r * .35, 114 - h, x + r * .35, 114, 554 + k, '#8a8a80', False)
        blob(img, [(x - r, 114 - h + 10), (x - r * .6, 114 - h - 16), (x + r * .6, 114 - h - 16), (x + r, 114 - h + 10)], hexc('#6a6d66'), 557 + k, scale=3)
    save(img, 'c2_kinoko', 'Каменные грибы', C, 'b', 60)
    img = canvas(260, 100); floor_shadow(img, 130, 94, 120)                                    # moss mounds
    for k, (x, rx) in enumerate(((60, 50), (140, 60), (210, 40))):
        blob(img, [(x - rx, 94), (x - rx * .7, 94 - rx * .7), (x, 94 - rx), (x + rx * .7, 94 - rx * .7), (x + rx, 94)], hexc('#3a6a2a'), 560 + k, scale=2, contrast=1.5)
        leaves(img, [(x, 94 - rx * .5, rx * .8, rx * .4)], ['#2a5a1a', '#4a7a2a', '#6a9a3a'], 180, 563 + k, (2, 4))
    save(img, 'c2_moss', 'Моховые кочки', C, 'b', 50)
    img = canvas(200, 150); floor_shadow(img, 100, 144, 80)                                    # copper watering can
    blob(img, [(40, 144), (36, 80), (60, 60), (120, 60), (144, 80), (140, 144)], hexc('#b86a3a'), 566, scale=3, spec=.4)
    line(img, [(140, 110), (196, 50)], '#a85a2a', 8); ell(img, (184, 36, 200, 56), '#a85a2a'); ImageDraw.Draw(img).arc([px(56), px(20), px(124), px(90)], 180, 360, fill=H('#a85a2a'), width=px(6))
    save(img, 'c2_teuro', 'Медная лейка', C, 'b', 50)
    img = canvas(200, 230); line(img, [(20, 10), (180, 10)], WOOD_D, 5)                          # bamboo wind chime
    for k in range(6):
        x = 30 + k * 28; L = 90 + (k % 3) * 36; line(img, [(x, 10), (x, 40)], '#e8e0cc', 1)
        bamboo(img, x, 40, 40 + L, 14, 567 + k, '#b8a060'); ImageDraw.Draw(img).ellipse([px(x - 7), px(36), px(x + 7), px(46)], fill=H('#3a2a14'))
    save(img, 'c2_kazeguruma', 'Бамбуковая ветряная дудка', C, 't', 50)
    img = canvas(260, 270); floor_shadow(img, 130, 264, 126)                                   # garden gate
    for x in (30, 216): fill(img, WOOD_D, 573 + x, rect=(x, 50, x + 14, 264), scale=4)
    poly(img, [(4, 60), (130, 20), (256, 60), (246, 70), (130, 34), (14, 70)], '#3a2a1a'); leaves(img, [(130, 36, 110, 12)], ['#2a3a1a', '#3a4a2a'], 200, 575, (3, 6))
    for k, x0 in enumerate((44, 130)):
        m = fill(img, '#b8a060', 576 + k, rect=(x0, 100, x0 + 86, 250), scale=4, stretch=(.3, 3))
        clip(img, m, lambda d, x0=x0: [d.line([(px(x0), px(100 + t)), (px(x0 + 86), px(250 - 150 + t - 60))], fill=(90, 70, 30, 160), width=px(2)) for t in range(0, 220, 20)])
    save(img, 'c2_gate', 'Садовая калитка', C, 'b', 170)
    img = canvas(140, 120); floor_shadow(img, 70, 114, 60)                                     # carp food bag
    fill(img, '#e8dcc0', 579, poly=[(24, 114), (116, 114), (110, 30), (30, 30)], scale=3, contrast=.5); volume(img, (24, 30, 116, 114), .5, .3)
    fill(img, '#c02a2a', 580, ell=(44, 56, 96, 90), scale=2); text(img, '鯉', 70, 73, 22, '#f4f0e6', SERIF)
    d = ImageDraw.Draw(img); rr = random.Random(3); [d.ellipse([px(a), px(b), px(a + 5), px(b + 5)], fill=H('#b88a40')) for a, b in [(rr.uniform(20, 60), rr.uniform(104, 116)) for _ in range(7)]]
    save(img, 'c2_koifood', 'Мешочек корма для карпов', C, 'b', 20)
    img = canvas(200, 170); floor_shadow(img, 100, 164, 90)                                    # big frog statue
    blob(img, [(20, 164), (24, 110), (60, 70), (140, 70), (176, 110), (180, 164)], hexc('#5a6a50'), 581)
    for sx in (-1, 1): blob(img, [(100 + sx * 50 - 20, 84), (100 + sx * 50 - 18, 50), (100 + sx * 50, 40), (100 + sx * 50 + 18, 50), (100 + sx * 50 + 20, 84)], hexc('#5a6a50'), 582 + sx)
    for sx in (-1, 1): ell(img, (100 + sx * 50 - 10, 52, 100 + sx * 50 + 10, 72), '#e8c040'); ell(img, (100 + sx * 50 - 3, 56, 100 + sx * 50 + 3, 70), '#1a1414')
    ImageDraw.Draw(img).arc([px(50), px(80), px(150), px(126)], 20, 160, fill=H('#2a3a24'), width=px(3)); text(img, '無事', 100, 146, 18, '#e8e0cc', SERIF)
    save(img, 'c2_kaeru', 'Лягушка «Вернись домой»', C, 'b', 110)
    img = canvas(110, 150); line(img, [(55, 0), (55, 24)], '#1a1410', 2)                          # firefly cage lantern
    fill(img, '#b8975a', 585, rect=(14, 24, 96, 34), scale=2); fill(img, '#b8975a', 586, rect=(14, 130, 96, 140), scale=2)
    soft(img, lambda d: d.ellipse([px(10), px(40), px(100), px(130)], fill=(200, 240, 120, 90)), 10)
    for x in range(18, 96, 10): line(img, [(x, 34), (x, 130)], '#8a7040', 1)
    rr = random.Random(4)
    for _ in range(9): x, y = rr.uniform(26, 86), rr.uniform(44, 124); soft(img, lambda d, x=x, y=y: d.ellipse([px(x - 5), px(y - 5), px(x + 5), px(y + 5)], fill=(230, 255, 140, 255)), 2)
    save(img, 'c2_hotaru', 'Фонарик со светлячками', C, 't', 60, glow=[55, 84])


# ───────────────────────────── ВХОД (+20) ─────────────────────────────
def entrance():
    C = 'Вход'
    img = canvas(150, 310); floor_shadow(img, 75, 304, 64)                                     # bronze lantern
    fill(img, '#3a4a40', 600, rect=(30, 280, 120, 304), scale=4); fill(img, '#3a4a40', 601, rect=(64, 150, 86, 282), scale=4, stretch=(.3, 3))
    fill(img, '#3a4a40', 602, rect=(36, 140, 114, 152), scale=3); fill(img, '#4a5a4a', 603, rect=(42, 80, 108, 140), scale=3, contrast=1.3)
    for x in (56, 75, 94): ImageDraw.Draw(img).rectangle([px(x - 5), px(92), px(x + 5), px(130)], fill=(255, 200, 110, 230))
    poly(img, [(14, 82), (75, 40), (136, 82)], '#3a4a40'); ell(img, (66, 24, 84, 42), '#3a4a40'); volume(img, (14, 24, 136, 304), .5, .3, spec=.2)
    save(img, 'e2_doro', 'Бронзовый фонарь', C, 'b', 190, glow=[75, 110])
    img = canvas(220, 220); floor_shadow(img, 110, 214, 100)                                   # small torii
    for x in (46, 162): fill(img, '#c8321e', 604 + x, rect=(x, 50, x + 14, 214), scale=4, stretch=(.3, 3)); fill(img, '#1a1410', 605 + x, rect=(x - 3, 200, x + 17, 214), scale=3)
    fill(img, '#1a1410', 606, poly=[(4, 30), (216, 30), (206, 46), (14, 46)], scale=4); fill(img, '#c8321e', 607, rect=(26, 70, 194, 82), scale=3)
    fill(img, '#1a1410', 608, rect=(96, 46, 124, 70), scale=3); volume(img, (4, 30, 216, 214), .4, .2)
    save(img, 'e2_torii', 'Маленькие тории', C, 'b', 160)
    img = canvas(240, 330); floor_shadow(img, 120, 324, 110)                                   # nobori flags
    for k, (x, c, ch) in enumerate(((50, '#c8321e', '稲荷'), (120, '#f2eee4', '奉納'), (190, '#c8321e', '福'))):
        line(img, [(x - 22, 324), (x - 22, 10)], '#2a2018', 4); line(img, [(x - 22, 20), (x + 26, 20)], '#2a2018', 3)
        fill(img, c, 609 + k, rect=(x - 18, 22, x + 24, 290), scale=5, stretch=(.4, 3), contrast=.5)
        for j, cc in enumerate(ch): text(img, cc, x + 3, 70 + j * 60, 36, '#1a1410' if c != '#1a1410' and c == '#f2eee4' else '#f2eee4', SERIF)
    save(img, 'e2_nobori', 'Флаги нобори', C, 'b', 90)
    img = canvas(300, 200); floor_shadow(img, 150, 194, 140)                                   # kazaridaru
    for k, (x, y) in enumerate(((60, 194), (150, 194), (240, 194), (105, 116), (195, 116))):
        fill(img, '#e8dcc0', 612 + k, poly=[(x - 42, y), (x + 42, y), (x + 44, y - 76), (x - 44, y - 76)], scale=4, stretch=(4, .5), contrast=.5)
        for yy in (y - 70, y - 8): rope(img, [(x - 44, yy), (x + 44, yy)], '#2a2018', 3)
        text(img, '酒', x, y - 40, 26, '#1a1410' if k % 2 else '#b8322a', SERIF); volume(img, (x - 44, y - 76, x + 44, y), .45, .35)
    save(img, 'e2_kazaridaru', 'Бочки сакэ-подношения', C, 'b', 200)
    img = canvas(240, 120); line(img, [(60, 30), (120, 0), (180, 30)], '#1a1410', 1.6)          # temple plaque
    fill(img, '#2a1a14', 620, rect=(10, 30, 230, 116), scale=5); ImageDraw.Draw(img).rectangle([px(18), px(38), px(222), px(108)], outline=H('#d8b048'), width=px(3))
    text(img, '猫神社', 120, 74, 42, '#d8b048', SERIF); volume(img, (10, 30, 230, 116), .35, .2, spec=.2)
    save(img, 'e2_gaku', 'Табличка «Кошачий храм»', C, 't', 150)
    img = canvas(260, 250); floor_shadow(img, 130, 244, 120)                                   # chozuya
    for x in (20, 226): fill(img, WOOD_D, 621 + x, rect=(x, 50, x + 14, 244), scale=4)
    poly(img, [(0, 60), (130, 16), (260, 60), (250, 72), (130, 30), (10, 72)], '#2a2018')
    stone_blk(img, 40, 160, 220, 244, 623, '#5a5c56'); fill(img, '#3a5a60', 624, ell=(56, 158, 204, 180), scale=3)
    for k, x in enumerate((90, 130, 170)): line(img, [(x, 150), (x + 20, 130)], WOOD_L, 3); fill(img, WOOD_L, 625 + k, ell=(x - 10, 144, x + 6, 160), scale=2)
    fill(img, '#4a5a70', 628, poly=[(30, 110), (70, 100), (80, 130), (60, 150)], scale=3); ImageDraw.Draw(img).line([(px(66), px(144)), (px(70), px(166))], fill=(200, 225, 235, 200), width=px(3))
    save(img, 'e2_chozuya', 'Павильон омовения тёдзуя', C, 'b', 230)
    img = canvas(170, 160); floor_shadow(img, 85, 154, 76)                                     # cairn
    for k, (w, h) in enumerate(((140, 40), (110, 34), (84, 28), (60, 22), (36, 18))):
        y = 154 - sum(hh for _, hh in ((140, 40), (110, 34), (84, 28), (60, 22), (36, 18))[:k]) + k * 4; stone_blk(img, 85 - w / 2, y - h, 85 + w / 2, y, 630 + k, '#6a6d66', k == 0)
    save(img, 'e2_cairn', 'Пирамидка камней', C, 'b', 30)
    img = canvas(130, 230); floor_shadow(img, 65, 224, 50)                                     # sakaki vase
    leaves(img, [(65, 80, 40, 40), (50, 120, 26, 20), (82, 116, 26, 20)], ['#1a3a1a', '#2a5a2a', '#3a6a2a'], 380, 635, (4, 8))
    fill(img, '#f2eee4', 636, poly=[(44, 224), (86, 224), (92, 170), (80, 140), (50, 140), (38, 170)], scale=3, contrast=.3); volume(img, (38, 140, 92, 224), .6, .4, spec=.5)
    save(img, 'e2_sakaki', 'Ветви сакаки в вазочке', C, 'b', 40)
    img = canvas(320, 150); rope(img, [(0, 14), (160, 40), (320, 14)], '#2a2018', 3)             # string of lanterns
    for k in range(6):
        x = 26 + k * 54; y = 14 + 26 * math.sin(math.pi * x / 320)
        soft(img, lambda d, x=x, y=y: d.ellipse([px(x - 26), px(y + 10), px(x + 26), px(y + 80)], fill=(255, 190, 110, 90)), 6)
        fill(img, '#c8321e' if k % 2 else '#f2eee4', 640 + k, ell=(x - 18, y + 14, x + 18, y + 76), scale=3, contrast=.4); volume(img, (x - 18, y + 14, x + 18, y + 76), .5, .4)
        for yy in (y + 14, y + 72): ImageDraw.Draw(img).rectangle([px(x - 10), px(yy), px(x + 10), px(yy + 5)], fill=H('#1a1410'))
    save(img, 'e2_lanterns', 'Цепочка фонариков', C, 't', 80, glow=[160, 80])
    img = canvas(200, 190); floor_shadow(img, 100, 184, 80)                                    # big ema
    line(img, [(100, 184), (100, 150)], WOOD_D, 8)
    fill(img, WOOD_L, 646, poly=[(10, 150), (190, 150), (190, 50), (100, 10), (10, 50)], scale=6, stretch=(4, .5)); ImageDraw.Draw(img).line([(px(10), px(50)), (px(100), px(10)), (px(190), px(50))], fill=H('#2a1a14'), width=px(6))
    blob(img, [(50, 140), (46, 100), (80, 80), (120, 84), (130, 140)], hexc('#f2eee4'), 647, scale=2, k=.3)
    for sx in (-1, 1): poly(img, [(88 + sx * 16, 84), (88 + sx * 22, 64), (88 + sx * 6, 80)], '#f2eee4')
    ell(img, (78, 96, 84, 102), '#1a1414'); ell(img, (94, 96, 100, 102), '#1a1414'); text(img, '招福', 160, 100, 20, '#b8322a', SERIF)
    save(img, 'e2_bigema', 'Большая эма с кошкой', C, 'b', 130)
    img = canvas(100, 240); floor_shadow(img, 50, 234, 30)                                     # gohei
    line(img, [(50, 234), (50, 20)], WOOD_L, 5)
    for k in range(2):
        for j in range(4):
            sx = -1 if k == 0 else 1; y = 40 + j * 22; poly(img, [(50, y), (50 + sx * 30, y), (50 + sx * 30, y + 14), (50 + sx * 10, y + 14), (50 + sx * 10, y + 22), (50, y + 22)], '#f8f4ec')
    save(img, 'e2_gohei', 'Жезл гохэй', C, 'b', 50)
    img = canvas(140, 190); floor_shadow(img, 70, 184, 60)                                     # omikuji box
    fill(img, '#c8321e', 650, poly=[(30, 184), (110, 184), (116, 70), (24, 70)], scale=4); volume(img, (24, 70, 116, 184), .5, .3, spec=.2)
    for j, cc in enumerate('御籤'): text(img, cc, 70, 106 + j * 36, 28, '#f2eee4', SERIF)
    for k in range(5): line(img, [(56 + k * 7, 72), (50 + k * 9, 20 + k % 2 * 8)], '#e8dcc0', 3)
    save(img, 'e2_omikuji', 'Ящик гадания омикудзи', C, 'b', 60)
    img = canvas(220, 250); floor_shadow(img, 110, 244, 100)                                   # getabako
    fill(img, '#5a3a20', 651, rect=(10, 20, 210, 244), scale=6, stretch=(.4, 3))
    for r in range(3):
        for c in range(2):
            x0, y0 = 22 + c * 96, 34 + r * 68; fill(img, '#3a2414', 652 + r * 2 + c, rect=(x0, y0, x0 + 84, y0 + 58), scale=4)
            ImageDraw.Draw(img).rectangle([px(x0 + 34), px(y0 + 10), px(x0 + 50), px(y0 + 18)], fill=H('#e8dcc0'))
    ImageDraw.Draw(img).rectangle([px(24), px(170), px(100), px(226)], fill=H('#1a1008')); fill(img, '#b8322a', 660, rect=(30, 204, 94, 214), scale=2); fill(img, WOOD_L, 661, rect=(30, 214, 94, 224), scale=2)
    volume(img, (10, 20, 210, 244), .35, .2)
    save(img, 'e2_getabako', 'Шкафчик для обуви гэтабако', C, 'b', 140)
    img = canvas(200, 110); line(img, [(50, 20), (100, 0), (150, 20)], '#1a1410', 1.4)          # welcome board
    fill(img, WOOD_L, 662, rect=(10, 20, 190, 104), scale=5, stretch=(4, .5)); text(img, 'ようこそ', 100, 52, 28, '#1a1410', SERIF)
    ell(img, (84, 72, 116, 98), '#f2eee4'); ell(img, (88, 70, 96, 80), '#f2eee4'); ell(img, (104, 70, 112, 80), '#f2eee4'); volume(img, (10, 20, 190, 104), .35, .2)
    save(img, 'e2_welcome', 'Табличка «Добро пожаловать»', C, 't', 40)
    img = canvas(220, 290); floor_shadow(img, 110, 284, 100)                                   # huge maneki-neko
    blob(img, [(34, 284), (30, 200), (60, 150), (160, 150), (190, 200), (186, 284)], hexc('#f2eee4'), 663, spec=.2)
    blob(img, [(46, 160), (40, 100), (60, 70), (110, 60), (160, 70), (180, 100), (174, 160), (110, 176)], hexc('#f2eee4'), 664, spec=.2)
    for sx in (-1, 1): poly(img, [(110 + sx * 50, 90), (110 + sx * 66, 30), (110 + sx * 20, 70)], '#f2eee4'); poly(img, [(110 + sx * 50, 80), (110 + sx * 60, 44), (110 + sx * 30, 70)], '#f0a0a8')
    blob(img, [(170, 150), (176, 90), (196, 60), (214, 80), (200, 150)], hexc('#f2eee4'), 665); ell(img, (78, 104, 94, 114), '#1a1414'); ell(img, (126, 104, 142, 114), '#1a1414')
    rope(img, [(56, 160), (110, 176), (164, 160)], '#c02a2a', 8); fill(img, '#e8c040', 666, ell=(96, 170, 124, 198), scale=2); volume(img, (96, 170, 124, 198), .6, .4, spec=.4)
    fill(img, '#e8c040', 667, ell=(70, 210, 150, 262), scale=3); text(img, '千万両', 110, 236, 18, '#1a1410', SERIF)
    save(img, 'e2_bigmaneki', 'Огромная манэки-нэко', C, 'b', 300)
    img = canvas(140, 230); floor_shadow(img, 70, 224, 56)                                     # candle stand
    fill(img, '#2a2622', 668, rect=(30, 204, 110, 224), scale=3); line(img, [(70, 204), (70, 90)], '#2a2622', 6); fill(img, '#2a2622', 669, rect=(14, 84, 126, 96), scale=3)
    for k, x in enumerate((26, 48, 70, 92, 114)):
        fill(img, '#f2eee4', 670 + k, rect=(x - 5, 52 + (k % 2) * 10, x + 5, 84), scale=2); soft(img, lambda d, x=x, k=k: d.ellipse([px(x - 8), px(34 + (k % 2) * 10), px(x + 8), px(56 + (k % 2) * 10)], fill=(255, 190, 90, 220)), 3)
    save(img, 'e2_candles', 'Стойка со свечами', C, 'b', 70, glow=[70, 50])
    img = canvas(150, 280); fill(img, WOOD_D, 675, rect=(0, 0, 150, 14), scale=4)               # rope with bells
    for k, x in enumerate((40, 110)):
        rope(img, [(x, 14), (x + 4, 140), (x, 270)], '#e8dcc0', 5)
        for j in range(4): y = 40 + j * 56; fill(img, '#d8b048', 676 + k * 4 + j, ell=(x - 12, y, x + 12, y + 24), scale=2); volume(img, (x - 12, y, x + 12, y + 24), .6, .4, spec=.5)
        for j in range(3): poly(img, [(x - 10, 244 + j * 8), (x + 10, 244 + j * 8), (x, 254 + j * 8)], ['#c02a2a', '#2a4a8a', '#2f6a3a'][j])
    save(img, 'e2_suzu', 'Верёвки с бубенцами', C, 't', 80)
    img = canvas(160, 280); floor_shadow(img, 80, 274, 66)                                     # fox with jewel
    fox_statue(img, 80, 274, 690, bib=True, key=False); fill(img, '#e8e0cc', 691, ell=(88, 150, 118, 180), scale=2); volume(img, (88, 150, 118, 180), .6, .4, spec=.6)
    for k in range(4): soft(img, lambda d, k=k: d.ellipse([px(94 + k * 3), px(134 - k * 8), px(112 + k * 3), px(154 - k * 8)], fill=(255, 220, 160, 110)), 3)
    save(img, 'e2_foxjewel', 'Лиса с волшебной жемчужиной', C, 'b', 160)
    img = canvas(180, 150); floor_shadow(img, 90, 144, 80)                                     # jizo in a knitted hat, pair
    for k, x in enumerate((56, 128)):
        blob(img, [(x - 30, 144), (x - 32, 90), (x, 70), (x + 32, 90), (x + 30, 144)], hexc('#7a7c74'), 692 + k); blob(img, [(x - 22, 80), (x - 24, 46), (x, 30), (x + 24, 46), (x + 22, 80)], hexc('#8a8c84'), 694 + k)
        fill(img, '#c02a2a', 696 + k, poly=[(x - 26, 50), (x - 18, 22), (x, 12), (x + 18, 22), (x + 26, 50)], scale=2, contrast=1.3); ell(img, (x - 6, 4, x + 6, 16), '#f2eee4')
        fill(img, '#c02a2a', 698 + k, poly=[(x - 28, 86), (x + 28, 86), (x + 18, 112), (x - 18, 112)], scale=2); line(img, [(x - 8, 60), (x - 3, 62)], '#3a3a36', 1.4); line(img, [(x + 3, 62), (x + 8, 60)], '#3a3a36', 1.4)
    save(img, 'e2_kasajizo', 'Дзидзо в вязаных шапочках', C, 'b', 90)


# ───────────────────────────── ИГРЫ (+22) ─────────────────────────────
def games():
    C = 'Игры'
    img = canvas(200, 250); floor_shadow(img, 100, 244, 80)                                    # kyudo target
    for x in (40, 150): line(img, [(x + 5, 244), (100, 170)], WOOD_D, 5)
    for k, (r, c) in enumerate(((80, '#1a1410'), (64, '#f2eee4'), (50, '#1a1410'), (36, '#f2eee4'), (22, '#1a1410'), (10, '#f2eee4'))): ell(img, (100 - r, 100 - r, 100 + r, 100 + r), c)
    line(img, [(118, 90), (190, 40)], WOOD_L, 3); poly(img, [(180, 34), (198, 30), (192, 48)], '#f2eee4'); volume(img, (20, 20, 180, 180), .4, .3)
    save(img, 'g2_mato', 'Мишень для кюдо', C, 'b', 110)
    img = canvas(120, 320); floor_shadow(img, 60, 314, 40)                                     # bow & quiver
    ImageDraw.Draw(img).arc([px(-60), px(6), px(80), px(314)], 290, 70, fill=H('#2a1a14'), width=px(6)); line(img, [(68, 20), (68, 300)], '#e8e0cc', 1)
    fill(img, '#b8322a', 700, rect=(76, 150, 108, 300), scale=3); for_x = [80, 90, 100]
    for x in for_x: line(img, [(x, 150), (x, 110)], WOOD_L, 2); poly(img, [(x - 5, 110), (x + 5, 110), (x, 96)], '#f2eee4')
    save(img, 'g2_yumi', 'Лук юми и колчан', C, 'b', 120)
    img = canvas(200, 200); floor_shadow(img, 100, 194, 90)                                    # kendo men + shinai
    line(img, [(20, 190), (190, 40)], '#c8b070', 7); rope(img, [(40, 172), (170, 58)], '#2a2018', 1)
    blob(img, [(50, 170), (44, 110), (70, 70), (130, 70), (156, 110), (150, 170)], hexc('#2a3a5a'), 701, scale=3)
    m = fill(img, '#8a8a90', 702, ell=(66, 84, 134, 150), scale=2); clip(img, m, lambda d: [d.line([(0, px(y)), (px(200), px(y))], fill=(30, 30, 30, 255), width=px(2)) for y in range(90, 150, 8)])
    ImageDraw.Draw(img).line([(px(100), px(84)), (px(100), px(150))], fill=H('#3a3a40'), width=px(3)); fill(img, '#2a3a5a', 703, rect=(40, 160, 160, 194), scale=3)
    save(img, 'g2_kendo', 'Шлем кэндо и синай', C, 'b', 110)
    img = canvas(170, 170); floor_shadow(img, 85, 164, 70)                                     # hanetsuki shuttle & paddle
    fill(img, WOOD_L, 704, poly=[(40, 30), (100, 30), (104, 120), (80, 126), (76, 164), (64, 164), (60, 126), (36, 120)], scale=3); flowers(img, 70, 72, 20, 28, ['#c02a2a', '#e8a0b6'], 4, 705, (7, 10))
    ell(img, (120, 120, 136, 136), '#1a1414')
    for k, c in enumerate(('#c02a2a', '#2a8a4a', '#e8c040', '#2a4a8a')): a = -math.pi / 2 + (k - 1.5) * .35; poly(img, [(128, 124), (128 + math.cos(a) * 36 - 6, 124 + math.sin(a) * 36), (128 + math.cos(a) * 36 + 6, 124 + math.sin(a) * 36)], c)
    save(img, 'g2_hane', 'Волан ханэ с ракеткой', C, 'b', 40)
    img = canvas(160, 110); floor_shadow(img, 80, 104, 70)                                     # dice cup
    fill(img, '#2a1a14', 706, poly=[(20, 30), (70, 30), (64, 100), (26, 100)], scale=3); volume(img, (20, 30, 70, 100), .5, .3, spec=.3)
    for k, (x, y, n) in enumerate(((100, 70, 1), (136, 80, 3))):
        fill(img, '#f2eee4', 707 + k, rect=(x - 16, y - 16, x + 16, y + 16), scale=2, contrast=.3); volume(img, (x - 16, y - 16, x + 16, y + 16), .5, .3)
        for t in range(n): ell(img, (x - 4 + (t - n // 2) * 8, y - 4 + (t - n // 2) * 8, x + 4 + (t - n // 2) * 8, y + 4 + (t - n // 2) * 8), '#c02a2a' if n == 1 else '#1a1414')
    save(img, 'g2_dice', 'Кости и стаканчик', C, 'b', 30)
    img = canvas(200, 130); floor_shadow(img, 100, 124, 90)                                    # go stones bowls
    for k, (x, c) in enumerate(((56, '#1a1414'), (144, '#f2eee4'))):
        fill(img, '#6a3a1a', 710 + k, ell=(x - 44, 50, x + 44, 124), scale=4, stretch=(4, 1)); volume(img, (x - 44, 50, x + 44, 124), .5, .35, spec=.4)
        for t in range(-2, 3): ell(img, (x + t * 12 - 8, 46 + abs(t) * 3, x + t * 12 + 8, 58 + abs(t) * 3), c)
    save(img, 'g2_go', 'Чаши с камнями го', C, 'b', 60)
    img = canvas(200, 190); floor_shadow(img, 100, 184, 90)                                    # origami set
    fill(img, '#efe6d0', 712, poly=[(20, 184), (180, 184), (170, 140), (30, 140)], scale=3, contrast=.3)
    for k, (x, c) in enumerate(((50, '#c02a2a'), (100, '#2a4a8a'), (150, '#e8c040'))):
        poly(img, [(x - 26, 140), (x, 100), (x + 26, 140)], c); poly(img, [(x, 100), (x + 26, 140), (x + 10, 140)], dk(H(c), .25))
    poly(img, [(70, 90), (100, 50), (130, 90), (100, 76)], '#e8a0b6'); poly(img, [(100, 50), (116, 30), (108, 58)], '#e8a0b6')
    save(img, 'g2_origami', 'Набор оригами', C, 'b', 30)
    img = canvas(220, 170); floor_shadow(img, 110, 164, 100)                                   # wooden skittles
    for k, (x, y) in enumerate(((60, 164), (110, 164), (160, 164), (85, 130), (135, 130))):
        blob(img, [(x - 12, y), (x - 16, y - 40), (x - 8, y - 66), (x - 10, y - 86), (x, y - 96), (x + 10, y - 86), (x + 8, y - 66), (x + 16, y - 40), (x + 12, y)], hexc('#e8dcc0'), 713 + k, scale=2, spec=.3)
        ImageDraw.Draw(img).rectangle([px(x - 9), px(y - 70), px(x + 9), px(y - 64)], fill=H('#c02a2a'))
    ell(img, (170, 130, 210, 164), '#2a4a8a'); volume(img, (170, 130, 210, 164), .6, .4, spec=.4)
    save(img, 'g2_kegli', 'Деревянные кегли', C, 'b', 40)
    img = canvas(200, 150); floor_shadow(img, 100, 144, 80)                                    # jump rope
    ImageDraw.Draw(img).arc([px(30), px(20), px(170), px(150)], 200, 520, fill=H('#e8a0b6'), width=px(4))
    for x in (30, 170): fill(img, WOOD_L, 720 + x, rect=(x - 8, 70, x + 8, 124), scale=2); ImageDraw.Draw(img).rectangle([px(x - 8), px(70), px(x + 8), px(78)], fill=H('#c02a2a'))
    save(img, 'g2_nawa', 'Скакалка', C, 'b', 20)
    img = canvas(240, 300); floor_shadow(img, 120, 294, 110)                                   # swing
    for x in (20, 206): fill(img, WOOD_D, 721 + x, poly=[(x, 294), (x + 14, 294), (x + 34 if x < 100 else x - 6, 20), (x + 20 if x < 100 else x - 20, 20)], scale=4)
    fill(img, WOOD_D, 723, rect=(20, 14, 220, 28), scale=4)
    for x in (80, 160): rope(img, [(x, 28), (x, 220)], '#b8975a', 3)
    fill(img, '#c02a2a', 724, rect=(70, 216, 170, 232), scale=3); volume(img, (70, 216, 170, 232), .5, .3)
    save(img, 'g2_swing', 'Качели', C, 'b', 150)
    img = canvas(140, 310); floor_shadow(img, 70, 304, 56)                                     # takeuma stilts
    for k, x in enumerate((44, 96)): bamboo(img, x, 10, 304, 14, 725 + k, '#a8a060'); fill(img, WOOD, 727 + k, rect=(x - 20, 220, x + 7, 232), scale=2); rope(img, [(x - 20, 226), (x, 240)], '#2a2018', 2)
    save(img, 'g2_takeuma', 'Бамбуковые ходули такэума', C, 'b', 40)
    img = canvas(280, 110); floor_shadow(img, 140, 104, 130)                                   # bokken on a stand
    fill(img, WOOD_D, 729, rect=(20, 70, 260, 104), scale=4); for_y = (40, 64)
    for k, y in enumerate(for_y): line(img, [(30, y + 4), (250, y - 4)], '#c8a870', 7); fill(img, '#1a1410', 730 + k, rect=(78, y - 2, 86, y + 12), scale=2)
    for x in (60, 220): fill(img, WOOD_D, 732 + x, rect=(x - 6, 30, x + 6, 72), scale=2)
    save(img, 'g2_bokken', 'Деревянные мечи боккэн', C, 'b', 80)
    img = canvas(90, 280); floor_shadow(img, 45, 274, 30)                                      # shakuhachi
    bamboo(img, 45, 20, 274, 20, 734, '#b89a60'); [ell(img, (41, y, 49, y + 8), '#2a1a10') for y in (100, 130, 160, 190)]
    poly(img, [(35, 20), (55, 20), (55, 30)], '#f2eee4')
    save(img, 'g2_shakuhachi', 'Флейта сякухати', C, 'b', 60)
    img = canvas(140, 300); floor_shadow(img, 70, 294, 50)                                     # shamisen
    fill(img, '#2a1a14', 735, rect=(64, 20, 76, 200), scale=2); fill(img, '#2a1a14', 736, poly=[(60, 20), (80, 20), (82, 6), (58, 6)], scale=2)
    for y in (26, 36, 46): line(img, [(56, y), (84, y)], '#e8dcc0', 3)
    fill(img, '#3a2418', 737, rect=(20, 190, 120, 290), scale=3); fill(img, '#f2ead8', 738, rect=(28, 198, 112, 282), scale=3, contrast=.3)
    for x in (66, 70, 74): line(img, [(x, 20), (x, 270)], '#e8e0cc', .6)
    fill(img, '#d8b048', 739, poly=[(90, 250), (120, 210), (134, 222), (100, 260)], scale=2)
    save(img, 'g2_shamisen', 'Сямисэн с плектром', C, 'b', 130)
    img = canvas(320, 120); floor_shadow(img, 160, 114, 150)                                   # koto
    fill(img, '#8a5a30', 740, poly=[(10, 60), (310, 40), (314, 70), (14, 100)], scale=5, stretch=(6, .5)); volume(img, (10, 40, 314, 100), .4, .25, spec=.2)
    for k in range(13):
        y0 = 62 + k * 2.4; line(img, [(24, y0 + 30 - k * 2), (300, y0 - 16 - k * 2)], '#f2eee4', .6)
        x = 60 + (k * 37) % 220; poly(img, [(x - 4, 76 - x * .07 + k * .5), (x + 4, 76 - x * .07 + k * .5), (x, 64 - x * .07 + k * .5)], '#f2eee4')
    save(img, 'g2_koto', 'Цитра кото', C, 'b', 200)
    img = canvas(200, 250); floor_shadow(img, 100, 244, 90)                                    # gong
    for x in (20, 166): fill(img, '#2a1a14', 741 + x, rect=(x, 20, x + 14, 244), scale=3)
    fill(img, '#2a1a14', 743, rect=(10, 14, 190, 28), scale=3); for_x2 = (70, 130)
    for x in for_x2: line(img, [(x, 28), (x, 56)], '#e8dcc0', 2)
    fill(img, '#b8903a', 744, ell=(30, 50, 170, 190), scale=3); volume(img, (30, 50, 170, 190), .5, .3, spec=.5)
    ImageDraw.Draw(img).ellipse([px(80), px(100), px(120), px(140)], outline=H('#8a6a2a'), width=px(4)); line(img, [(160, 220), (190, 160)], WOOD_L, 5); ell(img, (180, 146, 200, 166), '#c02a2a')
    save(img, 'g2_gong', 'Гонг с колотушкой', C, 'b', 150)
    img = canvas(200, 130); floor_shadow(img, 100, 124, 90)                                    # karuta
    fill(img, '#c02a2a', 745, rect=(20, 70, 110, 124), scale=3); text(img, '百人一首', 65, 97, 16, '#f2eee4', SERIF); volume(img, (20, 70, 110, 124), .4, .2)
    rr = random.Random(5)
    for k in range(6): x, y = 110 + rr.uniform(-10, 60), 50 + rr.uniform(-10, 50); fill(img, '#f2ead8', 746 + k, rect=(x, y, x + 34, y + 48), scale=2, contrast=.2); text(img, 'あいうえおか'[k], x + 17, y + 24, 16, '#1a1410', SERIF)
    save(img, 'g2_karuta', 'Коробка карт карута', C, 'b', 40)
    img = canvas(180, 110); floor_shadow(img, 90, 104, 80)                                     # menko
    for k, (x, y, c) in enumerate(((50, 70, '#c02a2a'), (100, 60, '#2a4a8a'), (140, 76, '#e8c040'), (80, 90, '#2f6a3a'))):
        fill(img, c, 752 + k, ell=(x - 30, y - 18, x + 30, y + 18), scale=2); ImageDraw.Draw(img).ellipse([px(x - 30), px(y - 18), px(x + 30), px(y + 18)], outline=H('#1a1414'), width=px(2))
        text(img, '鬼猫龍虎'[k], x, y, 16, '#f2eee4', SERIF)
    save(img, 'g2_menko', 'Карточки мэнко', C, 'b', 20)
    img = canvas(200, 160); floor_shadow(img, 100, 154, 80)                                    # fighting tops arena
    fill(img, '#b8975a', 756, ell=(10, 90, 190, 154), scale=3, contrast=.5); fill(img, '#e8dcc0', 757, ell=(26, 96, 174, 140), scale=3, contrast=.3)
    for k, (x, c) in enumerate(((70, '#c02a2a'), (130, '#2a4a8a'))):
        poly(img, [(x - 24, 96), (x + 24, 96), (x, 128)], c); fill(img, c, 758 + k, ell=(x - 24, 86, x + 24, 104), scale=2); line(img, [(x, 88), (x, 66)], WOOD_D, 4); volume(img, (x - 24, 66, x + 24, 128), .5, .4, spec=.3)
    save(img, 'g2_bei', 'Арена для волчков бэй', C, 'b', 50)
    img = canvas(220, 280); line(img, [(110, 150), (140, 280)], '#e8e0cc', 1)                    # owl kite
    fill(img, '#f2ead8', 760, poly=[(20, 20), (200, 20), (200, 170), (20, 170)], scale=3, contrast=.3); ImageDraw.Draw(img).rectangle([px(20), px(20), px(200), px(170)], outline=H('#8a6038'), width=px(2))
    blob(img, [(50, 160), (40, 80), (70, 40), (150, 40), (180, 80), (170, 160)], hexc('#8a5a30'), 761, scale=3, k=.3)
    for sx in (-1, 1): ell(img, (110 + sx * 30 - 22, 64, 110 + sx * 30 + 22, 108), '#f2e8c0'); ell(img, (110 + sx * 30 - 9, 76, 110 + sx * 30 + 9, 96), '#1a1414')
    poly(img, [(100, 104), (120, 104), (110, 124)], '#e8a030')
    for k in range(5): poly(img, [(140 + k * 3, 200 + k * 16), (152 + k * 3, 206 + k * 16), (140 + k * 3, 212 + k * 16)], ['#c02a2a', '#2a4a8a'][k % 2])
    save(img, 'g2_owlkite', 'Воздушный змей «Сова»', C, 't', 60)
    img = canvas(200, 170); floor_shadow(img, 100, 164, 90)                                    # hanabi crate
    fill(img, WOOD_L, 762, rect=(20, 90, 180, 164), scale=5, stretch=(4, .5)); text(img, '花火', 100, 128, 30, '#b8322a', SERIF); volume(img, (20, 90, 180, 164), .4, .2)
    for k, (x, c) in enumerate(((44, '#c02a2a'), (70, '#2a4a8a'), (100, '#e8c040'), (130, '#2f6a3a'), (156, '#e8a0b6'))):
        fill(img, c, 763 + k, rect=(x - 8, 40 + (k % 2) * 14, x + 8, 92), scale=2); line(img, [(x, 40 + (k % 2) * 14), (x + 4, 24 + (k % 2) * 14)], '#1a1410', 1.4)
    save(img, 'g2_hanabi', 'Ящик фейерверков ханаби', C, 'b', 60)
    img = canvas(160, 190); floor_shadow(img, 80, 184, 70)                                     # daruma otoshi tall / kanji blocks
    for k, c in enumerate(('#c02a2a', '#2a4a8a', '#e8c040', '#2f6a3a', '#e8a0b6')):
        y = 184 - k * 30; fill(img, c, 770 + k, rect=(34, y - 28, 126, y), scale=2); volume(img, (34, y - 28, 126, y), .5, .3, spec=.3); text(img, 'いろはにほ'[k], 80, y - 14, 18, '#f2eee4', SERIF)
    save(img, 'g2_blocks', 'Кубики с азбукой', C, 'b', 30)



if __name__ == '__main__':
    veranda(); bedroom(); onsen(); wardrobe(); courtyard(); entrance(); games()
    pack(); json.dump(ROWS, open(f'{OUT}/rooms2.json', 'w'), ensure_ascii=False, indent=0); print('TOTAL', len(ROWS))
