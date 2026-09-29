#!/usr/bin/env python3
"""Decorations made for each room of «Мусин дом» (kitchen first). Same brushes as items.py.
Usage: room_items.py <outdir> → <outdir>/<id>.webp + rooms.json (catalogue rows, category = room)"""
import json, math, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc
import items as I
from items import px, canvas, fill, volume, soft, floor_shadow, line, ell, poly, text, H, dk, lt, SERIF, SANS, mask_poly

OUT = sys.argv[1]
I.OUT = OUT
CAT = I.CAT
WOOD, WOOD_D, WOOD_L = '#8a6038', '#5a3a20', '#b88a58'
rnd_g = random.Random(11)


def save(img, iid, name, cat, anchor='b', price=60, glow=None):
    I.save(img, iid, name, cat, anchor, price, glow=glow)


def clip(img, m, fn):
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(l))
    a = np.asarray(l, np.float32); a[..., 3] *= np.asarray(m, np.float32) / 255; img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))


def barrel(img, cx, base, w, h, col, seed, hoops='#2a2018'):
    m = fill(img, col, seed, poly=[(cx - w * .46, base), (cx + w * .46, base), (cx + w * .5, base - h * .5), (cx + w * .46, base - h), (cx - w * .46, base - h), (cx - w * .5, base - h * .5)], scale=8, stretch=(.3, 3), contrast=1.1)
    clip(img, m, lambda d: [d.line([(px(cx - w / 2 + k * w / 7), px(base - h)), (px(cx - w / 2 + k * w / 7), px(base))], fill=(0, 0, 0, 60), width=px(1.4)) for k in range(1, 7)])
    for yy in (base - h * .82, base - h * .18): ImageDraw.Draw(img).rounded_rectangle([px(cx - w * .5), px(yy - 5), px(cx + w * .5), px(yy + 5)], px(3), fill=H(hoops))
    volume(img, (cx - w / 2, base - h, cx + w / 2, base), .45, .4)
    ImageDraw.Draw(img).ellipse([px(cx - w * .46), px(base - h - 10), px(cx + w * .46), px(base - h + 10)], fill=dk(H(col), .15))


def crock(img, cx, base, w, h, col, seed, lid=None):
    fill(img, col, seed, poly=[(cx - w * .3, base), (cx + w * .3, base), (cx + w * .5, base - h * .45), (cx + w * .34, base - h * .92), (cx - w * .34, base - h * .92), (cx - w * .5, base - h * .45)], scale=6, contrast=1.3)
    volume(img, (cx - w / 2, base - h, cx + w / 2, base), .55, .4, spec=.3)
    if lid: fill(img, lid, seed + 1, ell=(cx - w * .38, base - h - 8, cx + w * .38, base - h + 10), scale=5, stretch=(3, .5))


def plate(img, cx, cy, w, col='#e9e4d8', rim='#2a4a7a'):
    fill(img, col, 4, ell=(cx - w / 2, cy - w * .14, cx + w / 2, cy + w * .14), scale=4, contrast=.5)
    ImageDraw.Draw(img).ellipse([px(cx - w / 2), px(cy - w * .14), px(cx + w / 2), px(cy + w * .14)], outline=H(rim), width=px(2))


def rope(img, pts, col='#b8975a', w=3): line(img, pts, col, w); line(img, pts, dk(H(col), .3), w * .35)


# ───────────────────────────── КУХНЯ ─────────────────────────────
def kitchen():
    C = 'Кухня'
    # 1 iron pot on a tripod
    img = canvas(220, 250); floor_shadow(img, 110, 244, 90)
    for x0, x1 in ((40, 90), (180, 130), (110, 110)): line(img, [(x0, 244), (x1, 30)], '#2a2622', 5)
    line(img, [(110, 30), (110, 110)], '#2a2622', 2)
    fill(img, '#242224', 3, ell=(46, 100, 174, 226), scale=4, contrast=1.3); ImageDraw.Draw(img).rectangle([px(40), px(96), px(180), px(130)], fill=(0, 0, 0, 0))
    fill(img, '#242224', 4, poly=[(46, 126), (174, 126), (178, 160), (42, 160)], scale=4, contrast=1.3)
    fill(img, '#6a4a2a', 5, ell=(50, 110, 170, 136), scale=6, stretch=(3, .5))
    volume(img, (42, 110, 178, 226), .6, .35, spec=.25)
    for k in range(4): soft(img, lambda d, k=k: d.ellipse([px(90 + k * 10), px(60 - k * 14), px(116 + k * 10), px(90 - k * 14)], fill=(230, 232, 235, 70)), 6)
    save(img, 'k_irinabe', 'Котёл на треноге', C, 'b', 150)
    # 2 hagama rice pot
    img = canvas(200, 170); floor_shadow(img, 100, 164, 84)
    fill(img, '#2a2622', 3, ell=(30, 60, 170, 162), scale=4, contrast=1.4)
    fill(img, '#2a2622', 4, ell=(6, 70, 194, 100), scale=4, contrast=1.3)
    fill(img, WOOD, 5, ell=(46, 38, 154, 78), scale=8, stretch=(4, .5)); fill(img, WOOD_D, 6, rect=(90, 30, 110, 50), scale=4)
    volume(img, (6, 38, 194, 162), .55, .35, spec=.2)
    save(img, 'k_hagama', 'Рисоварка хагама', C, 'b', 120)
    # 3 bamboo steamers
    img = canvas(170, 190); floor_shadow(img, 85, 184, 74)
    for k in range(3):
        y0 = 150 - k * 44; fill(img, '#c8a86a', 10 + k, rect=(14, y0, 156, y0 + 40), scale=6, stretch=(4, .4), contrast=.9)
        ImageDraw.Draw(img).line([(px(14), px(y0 + 2)), (px(156), px(y0 + 2))], fill=H('#8a6a3a'), width=px(2))
    fill(img, '#d8b87a', 20, ell=(12, 44, 158, 72), scale=6, stretch=(4, .5)); ell(img, (76, 50, 94, 62), '#8a6a3a')
    for k in range(3): soft(img, lambda d, k=k: d.ellipse([px(50 + k * 30), px(4), px(80 + k * 30), px(46)], fill=(235, 236, 238, 70)), 7)
    volume(img, (12, 44, 158, 190), .35, .25)
    save(img, 'k_seiro', 'Бамбуковые пароварки', C, 'b', 70)
    # 4 cutting board with fish
    img = canvas(240, 110); floor_shadow(img, 120, 104, 106)
    fill(img, '#c8a070', 3, poly=[(10, 60), (230, 60), (234, 96), (6, 96)], scale=8, stretch=(5, .5)); fill(img, '#a88050', 4, rect=(6, 92, 234, 104), scale=6)
    fill(img, '#8a9aa6', 5, ell=(40, 38, 180, 76), scale=4, contrast=.8); poly(img, [(170, 57), (210, 34), (204, 58), (210, 80)], '#7a8a96')
    d = ImageDraw.Draw(img); d.ellipse([px(52), px(50), px(62), px(60)], fill=H('#1a1a1a')); d.arc([px(66), px(42), px(84), px(72)], 280, 80, fill=H('#5a6a74'), width=px(2))
    for k in range(6): d.arc([px(90 + k * 12), px(46), px(104 + k * 12), px(68)], 280, 80, fill=(90, 105, 115, 160), width=px(1))
    volume(img, (40, 38, 210, 80), .5, .3, spec=.4)
    save(img, 'k_manaita', 'Доска с рыбой', C, 'b', 60)
    # 5 soy sauce keg, 6 sake barrel, 7 miso crock, 8 umeboshi jar
    img = canvas(130, 150); floor_shadow(img, 65, 144, 54); barrel(img, 65, 144, 110, 118, WOOD_L, 21)
    fill(img, '#efe6cc', 22, rect=(40, 64, 90, 116), scale=4, contrast=.4); text(img, '醤油', 65, 90, 18, '#1a1410', SERIF)
    save(img, 'k_shoyu', 'Бочонок соевого соуса', C, 'b', 70)
    img = canvas(180, 190); floor_shadow(img, 90, 184, 76)
    fill(img, '#d8c49a', 23, poly=[(14, 184), (166, 184), (172, 90), (160, 30), (20, 30), (8, 90)], scale=5, stretch=(.3, 3), contrast=1.1)
    for yy in (52, 170): rope(img, [(10, yy), (90, yy + 6), (170, yy)], '#6a4a2a', 5)
    for x in (30, 150): rope(img, [(x, 50), (x + (8 if x < 90 else -8), 176)], '#6a4a2a', 3)
    fill(img, '#efe8d6', 24, rect=(58, 76, 122, 150), scale=4, contrast=.4); text(img, '酒', 90, 112, 44, '#b8322a', SERIF, brush=True)
    ell(img, (40, 18, 140, 42), '#b8a070'); volume(img, (8, 18, 172, 184), .45, .35)
    save(img, 'k_komodaru', 'Бочка сакэ комодару', C, 'b', 150)
    img = canvas(140, 150); floor_shadow(img, 70, 144, 56); crock(img, 70, 144, 120, 120, '#6a4a30', 25, lid=WOOD)
    fill(img, '#efe6cc', 26, rect=(46, 68, 94, 110), scale=4, contrast=.4); text(img, '味噌', 70, 89, 18, '#1a1410', SERIF)
    save(img, 'k_miso', 'Горшок мисо', C, 'b', 70)
    img = canvas(120, 150); floor_shadow(img, 60, 144, 48)
    m = fill(img, (200, 220, 225, 150), 27, poly=[(16, 144), (104, 144), (108, 40), (12, 40)], scale=4, contrast=.3)
    rr = random.Random(3); clip(img, m, lambda d: [d.ellipse([px(x - 9), px(y - 9), px(x + 9), px(y + 9)], fill=(160, 30, 40, 235)) for x, y in [(rr.uniform(24, 96), rr.uniform(70, 138)) for _ in range(22)]])
    fill(img, '#c8a070', 28, ell=(10, 28, 110, 50), scale=5, stretch=(3, .5)); ImageDraw.Draw(img).rectangle([px(20), px(52), px(28), px(136)], fill=(255, 255, 255, 90))
    save(img, 'k_umeboshi', 'Банка умэбоси', C, 'b', 50)
    # 9 hanging red peppers, 10 dried fish on a rope, 11 hanging noodles
    img = canvas(70, 260); rope(img, [(35, 0), (35, 250)], '#b8975a', 2.5); rr = random.Random(5)
    for k in range(16):
        y = 20 + k * 14; s = 1 if k % 2 else -1
        fill(img, rr.choice(['#c8281e', '#b01e18', '#d83a22']), 40 + k, poly=[(35, y), (35 + s * 28, y + 10), (35 + s * 30, y + 18), (35 + s * 4, y + 8)], scale=3, contrast=.8)
    volume(img, (0, 0, 70, 260), .4, .2, spec=.2)
    save(img, 'k_togarashi', 'Связка острого перца', C, 't', 30)
    img = canvas(260, 170); rope(img, [(4, 20), (130, 36), (256, 20)], '#8a6a3a', 3)
    for k in range(5):
        x = 30 + k * 50; y = 30 + 8 * math.sin(math.pi * (x - 4) / 252)
        fill(img, '#a88a6a', 60 + k, ell=(x - 14, y + 4, x + 14, y + 130), scale=4, contrast=1.1); poly(img, [(x - 14, y + 124), (x + 14, y + 124), (x, y + 150)], '#8a6a4a')
        ell(img, (x - 5, y + 14, x + 1, y + 20), '#1a1410'); volume(img, (x - 14, y + 4, x + 14, y + 140), .5, .4, spec=.35)
    save(img, 'k_himono', 'Сушёная рыба на верёвке', C, 't', 50)
    img = canvas(230, 220); fill(img, WOOD, 70, rect=(4, 12, 226, 24), scale=6, stretch=(6, .5))
    d = ImageDraw.Draw(img); rr = random.Random(7)
    for k in range(34): x = 12 + k * 6.2; d.line([(px(x), px(22)), (px(x + rr.uniform(-4, 4)), px(22 + rr.uniform(140, 196)))], fill=H(rr.choice(['#efe6d0', '#e6dcc0', '#f4ecd8'])), width=px(2.2))
    save(img, 'k_udon', 'Сохнущая лапша удон', C, 't', 40)
    # 12 basket of vegetables, 13 basket of mikan, 14 watermelon
    img = canvas(230, 170); floor_shadow(img, 115, 164, 96)
    for k, (x, a) in enumerate(((70, -.5), (100, -.2), (150, .3))):
        fill(img, '#f2eee4', 80 + k, poly=[(x, 110), (x + 18, 110), (x + 18 + a * 120, 10), (x + a * 120, 12)], scale=5, stretch=(.3, 3), contrast=.4)
        fill(img, '#4a7a3a', 90 + k, poly=[(x + a * 120 - 6, 16), (x + 22 + a * 120, 12), (x + 30 + a * 140, -4), (x - 14 + a * 140, 0)], scale=4)
    for x in (120, 136): fill(img, '#e07028', 95 + x, poly=[(x, 96), (x + 14, 96), (x + 30, 30), (x + 22, 28)], scale=3)
    fill(img, '#b08a50', 99, poly=[(14, 100), (216, 100), (196, 166), (34, 166)], scale=5, stretch=(4, 1), contrast=1.2)
    d = ImageDraw.Draw(img)
    for k in range(6): d.line([(px(20 + k * 4), px(104 + k * 11)), (px(210 - k * 4), px(104 + k * 11))], fill=H('#7a5a30'), width=px(1.4))
    volume(img, (14, 100, 216, 166), .45, .25)
    save(img, 'k_yasai', 'Корзина с овощами', C, 'b', 60)
    img = canvas(200, 150); floor_shadow(img, 100, 144, 84); rr = random.Random(9)
    for k in range(9):
        x, y = 40 + (k % 4) * 38 + (k // 4) * 18, 72 - (k // 4) * 26; fill(img, '#e8841e', 100 + k, ell=(x - 20, y - 18, x + 20, y + 18), scale=3, contrast=1.2); volume(img, (x - 20, y - 18, x + 20, y + 18), .6, .45, spec=.3)
        ell(img, (x - 3, y - 18, x + 3, y - 12), '#4a6a2a')
    fill(img, '#a8844a', 110, poly=[(10, 84), (190, 84), (172, 144), (28, 144)], scale=5, stretch=(4, 1), contrast=1.2)
    volume(img, (10, 84, 190, 144), .45, .25)
    save(img, 'k_mikan', 'Корзинка мандаринов микан', C, 'b', 40)
    img = canvas(180, 120); floor_shadow(img, 90, 114, 80)
    fill(img, '#2f6a2a', 111, poly=[(8, 60), (172, 60), (150, 104), (90, 116), (30, 104)], scale=5, contrast=1.2)
    clip(img, mask_poly(img, poly=[(8, 60), (172, 60), (150, 104), (90, 116), (30, 104)]), lambda d: [d.arc([px(20 + k * 22), px(40), px(60 + k * 22), px(130)], 20, 160, fill=(20, 40, 18, 200), width=px(3)) for k in range(7)])
    fill(img, '#d83a3a', 112, ell=(12, 40, 168, 80), scale=4, contrast=.8); ImageDraw.Draw(img).ellipse([px(12), px(40), px(168), px(80)], outline=H('#f0f0d8'), width=px(3))
    rr = random.Random(2); d = ImageDraw.Draw(img); [d.ellipse([px(x - 2), px(y - 3), px(x + 2), px(y + 3)], fill=H('#1a1414')) for x, y in [(rr.uniform(34, 146), rr.uniform(50, 70)) for _ in range(14)]]
    save(img, 'k_suika', 'Половинка арбуза', C, 'b', 40)
    # 15 rice bales, 16 mortar, 17 hibachi with kettle, 18 water jar
    img = canvas(260, 200); floor_shadow(img, 130, 194, 118)
    for k, (x, y) in enumerate(((70, 190), (190, 190), (130, 118))):
        fill(img, '#c8ae74', 120 + k, ell=(x - 64, y - 76, x + 64, y), scale=4, stretch=(4, .4), contrast=1.2)
        for yy in (y - 58, y - 18): rope(img, [(x - 60, yy), (x, yy + 6), (x + 60, yy)], '#7a5a2a', 3)
        fill(img, '#a88a50', 125 + k, ell=(x + 42, y - 72, x + 66, y - 4), scale=4); volume(img, (x - 64, y - 76, x + 66, y), .45, .3)
    save(img, 'k_komedawara', 'Мешки риса комэдавара', C, 'b', 120)
    img = canvas(180, 150); floor_shadow(img, 90, 144, 72)
    fill(img, '#8a4a2a', 130, poly=[(20, 50), (160, 50), (130, 140), (50, 140)], scale=5, contrast=1.2); fill(img, '#5a3020', 131, ell=(20, 38, 160, 62), scale=4)
    clip(img, mask_poly(img, ell=(24, 40, 156, 60)), lambda d: [d.line([(px(30 + k * 10), px(40)), (px(40 + k * 10), px(62))], fill=(40, 20, 12, 200), width=px(1.2)) for k in range(12)])
    fill(img, '#c8a070', 132, poly=[(110, 54), (120, 50), (176, 4), (168, 0)], scale=4)
    volume(img, (20, 38, 160, 140), .5, .35, spec=.25)
    save(img, 'k_suribachi', 'Ступка сурибати', C, 'b', 50)
    img = canvas(200, 230); floor_shadow(img, 100, 224, 86)
    fill(img, '#3a2a1e', 140, rect=(20, 140, 180, 224), scale=6, contrast=1.1); fill(img, '#6a4a2a', 141, rect=(14, 132, 186, 146), scale=5)
    soft(img, lambda d: d.ellipse([px(50), px(118), px(150), px(150)], fill=(240, 120, 40, 150)), 8)
    fill(img, '#2a2622', 142, ell=(40, 50, 160, 138), scale=4, contrast=1.4); line(img, [(58, 64), (100, 18), (142, 64)], '#1a1714', 5)
    fill(img, '#2a2622', 143, poly=[(150, 90), (190, 70), (186, 82), (156, 104)], scale=4)
    volume(img, (40, 50, 160, 138), .55, .35, spec=.25); volume(img, (14, 132, 186, 224), .4, .2)
    for k in range(3): soft(img, lambda d, k=k: d.ellipse([px(176 + k * 6), px(40 - k * 18), px(196 + k * 6), px(66 - k * 18)], fill=(235, 236, 238, 80)), 5)
    save(img, 'k_hibachi', 'Жаровня хибати с чайником', C, 'b', 160, glow=[100, 134])
    img = canvas(170, 230); floor_shadow(img, 85, 224, 70); crock(img, 85, 224, 150, 190, '#4a3a2e', 144, lid=WOOD)
    fill(img, WOOD_D, 145, rect=(60, 20, 70, 34), scale=3); line(img, [(104, 30), (150, 4)], '#c8a070', 4); ell(img, (140, -2, 162, 14), '#c8a070')
    save(img, 'k_mizugame', 'Кувшин для воды', C, 'b', 90)
    # 19 hanging ladles rack, 20 broom, 21 apron on a peg
    img = canvas(240, 200); fill(img, WOOD, 150, rect=(4, 10, 236, 26), scale=6, stretch=(6, .5))
    for k, x in enumerate((40, 90, 140, 190)):
        line(img, [(x, 26), (x, 130)], '#b8975a', 5); fill(img, '#c8a070' if k % 2 else '#9a7a4a', 151 + k, ell=(x - 20, 120, x + 20, 170), scale=4, contrast=1.1); volume(img, (x - 20, 120, x + 20, 170), .5, .4)
    save(img, 'k_hishaku', 'Черпаки на полке', C, 't', 50)
    img = canvas(90, 280); floor_shadow(img, 50, 274, 36)
    line(img, [(46, 4), (52, 180)], '#c8a070', 6)
    fill(img, '#c8a860', 160, poly=[(30, 176), (70, 176), (90, 274), (8, 274)], scale=4, stretch=(.3, 3), contrast=1.2)
    for yy in (186, 200): rope(img, [(30, yy), (70, yy)], '#b8322a', 3)
    save(img, 'k_hoki', 'Веник хоки', C, 'b', 25)
    img = canvas(170, 250); ell(img, (78, 0, 92, 14), '#3a2a1e')
    fill(img, '#f2eee4', 161, poly=[(40, 14), (130, 14), (150, 240), (20, 240)], scale=6, contrast=.4, dark=.15)
    for sx in (-1, 1): fill(img, '#f2eee4', 162 + sx, poly=[(85 + sx * 40, 16), (85 + sx * 84, 60), (85 + sx * 76, 150), (85 + sx * 46, 110)], scale=6, contrast=.4, dark=.15)
    fill(img, '#2a4a7a', 164, rect=(40, 120, 130, 132), scale=4); text(img, '猫', 85, 180, 30, '#b8322a', SERIF)
    volume(img, (20, 14, 150, 240), .35, .25)
    save(img, 'k_kappogi', 'Фартук каппоги на крючке', C, 't', 40)
    # 22-24 noren curtains
    for iid, n, col, k, fg in (('k_noren_neko', 'Норэн «Кошка»', '#26386a', '猫', '#f2ecd8'), ('k_noren_shoku', 'Норэн «Еда»', '#9a2a22', '食', '#f2ecd8'), ('k_noren_yu', 'Норэн «Горячая вода»', '#e8e0cc', 'ゆ', '#9a2a22')):
        img = canvas(300, 260); fill(img, WOOD_D, 170, rect=(0, 0, 300, 12), scale=5, stretch=(6, .5))
        for j in range(3):
            x0 = 6 + j * 97; fill(img, col, 171 + j, poly=[(x0, 12), (x0 + 92, 12), (x0 + 92 + (j - 1) * 4, 250), (x0 + (j - 1) * 4, 250)], scale=10, stretch=(.5, 3), contrast=.8)
        text(img, k, 150, 120, 110, fg, SERIF, brush=True)
        volume(img, (0, 12, 300, 250), .3, .15)
        save(img, iid, n, C, 't', 90)
    # 25 tamagoyaki pan, 26 onigiri plate, 27 sushi geta, 28 dango plate, 29 open bento, 30 herbs pot
    img = canvas(230, 90); floor_shadow(img, 90, 84, 80)
    fill(img, '#3a3432', 180, rect=(20, 30, 150, 80), scale=4, contrast=1.2); fill(img, WOOD, 181, rect=(150, 44, 226, 58), scale=5, stretch=(4, .5))
    for k in range(3): fill(img, '#f0c040', 182 + k, rect=(32 + k * 38, 36, 66 + k * 38, 72), scale=3, contrast=.6)
    volume(img, (20, 30, 150, 80), .4, .2, spec=.3)
    save(img, 'k_tamagoyaki', 'Сковородка тамагояки', C, 'b', 50)
    img = canvas(200, 110); floor_shadow(img, 100, 104, 84); plate(img, 100, 84, 180)
    for k, x in enumerate((56, 100, 144)):
        fill(img, '#f4f2ec', 190 + k, poly=[(x - 24, 84), (x + 24, 84), (x + 4, 40), (x - 4, 40)], scale=3, contrast=.3); fill(img, '#1a2a1a', 193 + k, rect=(x - 16, 66, x + 16, 84), scale=3); volume(img, (x - 24, 40, x + 24, 84), .4, .3)
    save(img, 'k_onigiri', 'Тарелка онигири', C, 'b', 40)
    img = canvas(230, 100); floor_shadow(img, 115, 94, 100)
    fill(img, WOOD_L, 200, rect=(10, 60, 220, 80), scale=6, stretch=(6, .5)); fill(img, WOOD_D, 201, rect=(30, 80, 50, 94), scale=4); fill(img, WOOD_D, 202, rect=(180, 80, 200, 94), scale=4)
    for k, top in enumerate(('#e8704a', '#f09a70', '#d83a3a', '#f4e4c0', '#e8704a', '#2a3a2a')):
        x = 30 + k * 32; fill(img, '#f4f2ec', 203 + k, rect=(x, 44, x + 26, 60), scale=3, contrast=.3); fill(img, top, 210 + k, rect=(x - 2, 34, x + 28, 48), scale=3); volume(img, (x - 2, 34, x + 28, 60), .5, .3, spec=.3)
    save(img, 'k_sushi', 'Суси на подставке', C, 'b', 70)
    img = canvas(200, 110); floor_shadow(img, 100, 104, 84); plate(img, 100, 86, 180, rim='#b8322a')
    for k, cols in enumerate((('#f2b8c8', '#f4f0e6', '#8ab86a'), ('#8a4a2a', '#8a4a2a', '#8a4a2a'), ('#f2b8c8', '#f4f0e6', '#8ab86a'))):
        x = 60 + k * 40; line(img, [(x - 30, 90), (x + 30, 30)], '#c8a070', 2.4)
        for j, c in enumerate(cols): cx, cy = x - 12 + j * 14, 74 - j * 14; fill(img, c, 220 + k * 3 + j, ell=(cx - 12, cy - 12, cx + 12, cy + 12), scale=3, contrast=.4); volume(img, (cx - 12, cy - 12, cx + 12, cy + 12), .5, .4, spec=.3)
    save(img, 'k_dango', 'Данго на блюде', C, 'b', 40)
    img = canvas(200, 130); floor_shadow(img, 100, 124, 88)
    fill(img, '#1a1412', 230, rect=(14, 40, 186, 124), scale=5, contrast=.8); fill(img, '#8a1a14', 231, rect=(22, 48, 178, 116), scale=5, contrast=.6)
    for k, (x0, y0, x1, y1, c) in enumerate(((26, 52, 96, 112, '#f4f2ec'), (100, 52, 174, 80, '#f0c040'), (100, 84, 136, 112, '#d8573a'), (140, 84, 174, 112, '#4a8a3a'))):
        fill(img, c, 232 + k, rect=(x0, y0, x1, y1), scale=3, contrast=.5)
    ell(img, (52, 74, 70, 92), '#c02a3a'); volume(img, (14, 40, 186, 124), .35, .2, spec=.2)
    save(img, 'k_bento', 'Открытое бэнто', C, 'b', 70)
    img = canvas(150, 190); floor_shadow(img, 75, 184, 56)
    P.maple(img, px(75), px(116), px(110), 17, [hexc('#1c3a18'), hexc('#2a5a22'), hexc('#3a7a2e'), hexc('#5a9a3e'), hexc('#7aba5a')], P.BARK, lean=0)
    fill(img, '#b8683a', 240, poly=[(34, 110), (116, 110), (106, 184), (44, 184)], scale=5, contrast=1.2); volume(img, (34, 110, 116, 184), .5, .3, spec=.2)
    save(img, 'k_shiso', 'Горшочек сисо', C, 'b', 35)
    # 31 kitchen paper lantern, 32 spice shelf
    img = canvas(110, 240); line(img, [(55, 0), (55, 24)], '#120c09', 2)
    m = fill(img, '#f2e8cc', 250, ell=(10, 30, 100, 226), scale=5, contrast=.8)
    clip(img, m, lambda d: [d.line([(0, px(30 + 196 * k / 13)), (px(110), px(30 + 196 * k / 13))], fill=(120, 90, 50, 150), width=px(1.6)) for k in range(1, 13)])
    text(img, '台所', 55, 128, 30, '#1a1410', SERIF); volume(img, (10, 30, 100, 226), .5, .45)
    for y in (26, 222): ImageDraw.Draw(img).rectangle([px(30), px(y), px(80), px(y + 10)], fill=H('#140d09'))
    save(img, 'k_chochin', 'Кухонный фонарь', C, 't', 60, glow=[55, 128])
    img = canvas(220, 190); floor_shadow(img, 110, 184, 96)
    fill(img, WOOD, 260, rect=(10, 20, 210, 186), scale=7, stretch=(4, .6)); fill(img, WOOD_D, 261, rect=(20, 30, 200, 176), scale=6)
    for yy in (100, 176): fill(img, WOOD_L, 262 + yy, rect=(16, yy - 6, 204, yy + 4), scale=5, stretch=(6, .5))
    rr = random.Random(12)
    for row, yb in ((0, 94), (1, 170)):
        for k in range(5):
            x = 34 + k * 36; h = rr.uniform(34, 56); c = rr.choice(['#c8a060', '#6a3a1e', '#a83a22', '#e8d8b0', '#3a5a3a'])
            fill(img, (200, 215, 220, 170), 270 + row * 5 + k, rect=(x - 13, yb - h, x + 13, yb), scale=3, contrast=.3); fill(img, c, 280 + row * 5 + k, rect=(x - 11, yb - h * .7, x + 11, yb - 2), scale=3, contrast=.8)
            fill(img, '#8a6038', 290 + row * 5 + k, rect=(x - 9, yb - h - 8, x + 9, yb - h), scale=3)
    volume(img, (10, 20, 210, 186), .35, .2)
    save(img, 'k_spices', 'Полка со специями', C, 'b', 90)


def pair(img, fn, x0, x1):
    fn(img, x0); fn(img, x1)


def figure_base(img, cx, base, w, col='#6a6d66', seed=1):
    fill(img, col, seed, rect=(cx - w / 2, base - 26, cx + w / 2, base), scale=5, contrast=1.3); volume(img, (cx - w / 2, base - 26, cx + w / 2, base), .4, .2)


# ───────────────────────────── ВЕРАНДА ─────────────────────────────
def veranda():
    C = 'Веранда'
    img = canvas(170, 140); floor_shadow(img, 85, 134, 66)                                   # kayari-buta mosquito pig
    fill(img, '#4a5a4a', 3, ell=(14, 36, 156, 132), scale=4, contrast=1.2); fill(img, '#4a5a4a', 4, rect=(30, 118, 50, 134), scale=4); fill(img, '#4a5a4a', 5, rect=(120, 118, 140, 134), scale=4)
    fill(img, '#3a483a', 6, ell=(140, 64, 170, 104), scale=4); ell(img, (150, 76, 158, 84), '#1a1a1a'); ell(img, (158, 76, 166, 84), '#1a1a1a')
    for sx in (40, 66): poly(img, [(sx, 44), (sx + 14, 20), (sx + 22, 44)], '#3a483a')
    ell(img, (34, 70, 44, 80), '#1a1a1a'); volume(img, (14, 20, 170, 134), .55, .35, spec=.25)
    for k in range(4): soft(img, lambda d, k=k: d.ellipse([px(146 + k * 4), px(40 - k * 14), px(160 + k * 4), px(60 - k * 14)], fill=(220, 224, 226, 90)), 4)
    save(img, 'v_kayaributa', 'Свинка от комаров', C, 'b', 50)
    img = canvas(150, 170); floor_shadow(img, 75, 164, 62)                                     # cricket cage
    fill(img, '#c8a86a', 7, poly=[(14, 150), (136, 150), (136, 164), (14, 164)], scale=5, stretch=(4, .5)); poly(img, [(10, 52), (75, 8), (140, 52)], '#a8844a')
    d = ImageDraw.Draw(img)
    for k in range(12): x = 18 + k * 10.4; d.line([(px(x), px(52)), (px(x), px(150))], fill=H('#b8975a'), width=px(1.8))
    for y in (52, 100): d.line([(px(14), px(y)), (px(136), px(y))], fill=H('#9a7a40'), width=px(3))
    fill(img, '#4a6a2a', 8, ell=(60, 120, 96, 140), scale=3); line(img, [(75, 8), (75, -4)], '#6a4a2a', 2)
    save(img, 'v_mushikago', 'Клетка для сверчка', C, 'b', 60)
    img = canvas(240, 300); fill(img, '#6a4a2a', 9, rect=(0, 0, 240, 12), scale=5)             # sudare blind
    m = fill(img, '#c8a86a', 10, rect=(8, 12, 232, 290), scale=6, stretch=(6, .3), contrast=.9)
    clip(img, m, lambda d: [d.line([(0, px(y)), (px(240), px(y))], fill=(90, 60, 30, 120), width=px(1.2)) for y in range(16, 290, 6)])
    for x in (40, 200): line(img, [(x, 12), (x, 292)], '#b8322a', 2)
    save(img, 'v_sudare', 'Бамбуковая штора сударэ', C, 't', 70)
    img = canvas(170, 320); floor_shadow(img, 85, 314, 60)                                     # asagao on a trellis
    for x in (40, 85, 130): line(img, [(x, 250), (x + (85 - x) * .2, 20)], '#8a6a3a', 3)
    for y in (80, 150, 220): line(img, [(34, y), (136, y)], '#8a6a3a', 2)
    rr = random.Random(4); d = ImageDraw.Draw(img)
    for k in range(40): x, y = rr.uniform(30, 140), rr.uniform(30, 250); d.ellipse([px(x - 8), px(y - 5), px(x + 8), px(y + 5)], fill=H(rr.choice(['#2f5a2a', '#3e6a34', '#4a7a3a'])))
    for k in range(9):
        x, y = rr.uniform(34, 136), rr.uniform(34, 240); c = rr.choice(['#3a4ab8', '#6a3ab0', '#b03a8a'])
        d.ellipse([px(x - 13), px(y - 13), px(x + 13), px(y + 13)], fill=H(c)); d.ellipse([px(x - 5), px(y - 5), px(x + 5), px(y + 5)], fill=H('#f4f0f8'))
    fill(img, '#2a3a4a', 11, poly=[(40, 250), (130, 250), (120, 314), (50, 314)], scale=5, contrast=1.2); volume(img, (40, 250, 130, 314), .5, .3, spec=.2)
    save(img, 'v_asagao', 'Вьюнок асагао на шпалере', C, 'b', 110)
    img = canvas(220, 150); floor_shadow(img, 110, 144, 96)                                    # tub with a watermelon
    fill(img, '#2f6a2a', 12, ell=(60, 20, 170, 110), scale=4, contrast=1.1)
    clip(img, mask_poly(img, ell=(60, 20, 170, 110)), lambda d: [d.arc([px(40 + k * 18), px(10), px(90 + k * 18), px(120)], 250, 290, fill=(20, 40, 18, 220), width=px(4)) for k in range(8)])
    volume(img, (60, 20, 170, 110), .6, .45, spec=.35)
    fill(img, (150, 190, 205, 255), 13, ell=(16, 70, 204, 102), scale=4, contrast=.5)
    fill(img, WOOD_L, 14, poly=[(12, 84), (208, 84), (196, 144), (24, 144)], scale=6, stretch=(.4, 3)); [rope(img, [(14, y), (110, y + 4), (206, y)], '#2a2018', 3) for y in (96, 132)]
    save(img, 'v_suika_tub', 'Арбуз в тазу с водой', C, 'b', 70)
    img = canvas(190, 90); floor_shadow(img, 95, 84, 84)                                       # geta pair
    for x in (50, 140):
        fill(img, WOOD_L, 15 + x, rect=(x - 34, 40, x + 34, 58), scale=5, stretch=(4, .5)); fill(img, WOOD_D, 16 + x, rect=(x - 28, 58, x - 18, 80), scale=4); fill(img, WOOD_D, 17 + x, rect=(x + 18, 58, x + 28, 80), scale=4)
        line(img, [(x - 20, 42), (x, 26), (x + 20, 42)], '#b8322a', 4)
    save(img, 'v_geta', 'Гэта у края веранды', C, 'b', 40)
    img = canvas(200, 110); floor_shadow(img, 100, 104, 86)                                    # matcha tray
    fill(img, '#2a1a14', 18, rect=(10, 70, 190, 90), scale=5); fill(img, '#1a1210', 19, rect=(20, 90, 36, 104), scale=3); fill(img, '#1a1210', 20, rect=(164, 90, 180, 104), scale=3)
    fill(img, '#5a4a3a', 21, poly=[(40, 40), (100, 40), (94, 70), (46, 70)], scale=4, contrast=1.2); ell(img, (42, 34, 98, 46), '#6a9a3a')
    fill(img, '#d8c8a0', 22, poly=[(128, 64), (148, 64), (150, 30), (126, 30)], scale=3, stretch=(.3, 3)); d = ImageDraw.Draw(img); [d.line([(px(128 + k * 2), px(30)), (px(126 + k * 2.4), px(12))], fill=H('#d8c8a0'), width=px(1)) for k in range(10)]
    volume(img, (10, 12, 190, 104), .35, .2, spec=.2)
    save(img, 'v_matcha', 'Поднос с маття', C, 'b', 50)
    img = canvas(200, 110); floor_shadow(img, 100, 104, 90)                                    # shogi board
    fill(img, '#d8b070', 23, rect=(14, 30, 186, 88), scale=6, stretch=(4, .5)); fill(img, '#b88a48', 24, rect=(14, 88, 186, 104), scale=5)
    d = ImageDraw.Draw(img)
    for k in range(10): d.line([(px(24 + k * 17), px(34)), (px(24 + k * 17), px(84))], fill=H('#3a2a1a'), width=px(1)); d.line([(px(24), px(34 + k * 5.5)), (px(177), px(34 + k * 5.5))], fill=H('#3a2a1a'), width=px(1))
    rr = random.Random(6)
    for k in range(10): x, y = rr.uniform(30, 170), rr.uniform(38, 82); poly(img, [(x - 5, y + 5), (x, y - 6), (x + 5, y + 5)], '#e8cc88')
    save(img, 'v_shogi', 'Доска сёги', C, 'b', 90)
    img = canvas(150, 220); line(img, [(75, 0), (75, 60)], '#6a4a2a', 2)                         # bird feeder
    poly(img, [(10, 100), (75, 50), (140, 100)], '#6a4a2a'); fill(img, WOOD_L, 25, rect=(26, 100, 124, 190), scale=6, stretch=(.4, 3))
    ell(img, (56, 120, 94, 158), '#1a1410'); fill(img, WOOD_D, 26, rect=(66, 164, 84, 174), scale=3)
    fill(img, '#8a6a4a', 27, ell=(96, 170, 134, 200), scale=3); ell(img, (126, 176, 134, 184), '#1a1414'); poly(img, [(134, 184), (146, 182), (134, 188)], '#e0a030')
    volume(img, (10, 50, 140, 200), .4, .2)
    save(img, 'v_birdhouse', 'Скворечник с птичкой', C, 't', 60)
    img = canvas(110, 150); floor_shadow(img, 55, 144, 44)                                     # jar of fireflies
    m = fill(img, (180, 200, 190, 255), 28, poly=[(16, 144), (94, 144), (100, 40), (10, 40)], scale=4, contrast=.3)
    rr = random.Random(8)
    for k in range(9): x, y = rr.uniform(24, 86), rr.uniform(56, 134); soft(img, lambda d, x=x, y=y: d.ellipse([px(x - 8), px(y - 8), px(x + 8), px(y + 8)], fill=(214, 242, 122, 200)), 3); ell(img, (x - 2, y - 2, x + 2, y + 2), '#f8ffd8')
    fill(img, '#b8975a', 29, ell=(6, 30, 104, 50), scale=4, stretch=(3, .5)); rope(img, [(20, 34), (55, 14), (90, 34)], '#b8322a', 2)
    save(img, 'v_hotaru', 'Банка со светлячками', C, 'b', 90, glow=[55, 96])
    img = canvas(190, 90); floor_shadow(img, 95, 84, 88)                                       # round cat cushion
    fill(img, '#b8322a', 30, ell=(8, 20, 182, 84), scale=6, contrast=.8); fill(img, '#d8484a', 31, ell=(30, 28, 160, 66), scale=6, contrast=.6)
    rr = random.Random(9); d = ImageDraw.Draw(img); [d.ellipse([px(x - 3), px(y - 3), px(x + 3), px(y + 3)], fill=H('#f4e0c0')) for x, y in [(rr.uniform(40, 150), rr.uniform(34, 62)) for _ in range(14)]]
    volume(img, (8, 20, 182, 84), .5, .35, spec=.15)
    save(img, 'v_nekozabuton', 'Круглая лежанка для кошки', C, 'b', 60)
    img = canvas(80, 200); line(img, [(40, 0), (40, 80)], '#b8322a', 3)                          # bell with a ribbon
    fill(img, '#d8b048', 32, ell=(14, 76, 66, 128), scale=3, contrast=1.3); d = ImageDraw.Draw(img); d.line([(px(16), px(102)), (px(64), px(102))], fill=H('#6a4a12'), width=px(2)); d.ellipse([px(34), px(106), px(46), px(118)], fill=H('#3a2a08'))
    volume(img, (14, 76, 66, 128), .7, .4, spec=.5)
    for sx in (-1, 1): fill(img, '#b8322a', 33 + sx, poly=[(40, 128), (40 + sx * 20, 196), (40 + sx * 6, 190)], scale=3)
    save(img, 'v_suzu', 'Колокольчик с лентами', C, 't', 30)
    img = canvas(170, 150); floor_shadow(img, 85, 144, 74)                                     # uchimizu bucket and ladle
    fill(img, WOOD_L, 35, poly=[(30, 60), (140, 60), (132, 144), (38, 144)], scale=6, stretch=(.4, 3)); [rope(img, [(32, y), (85, y + 4), (138, y)], '#2a2018', 3) for y in (76, 128)]
    fill(img, (140, 180, 200, 255), 36, ell=(32, 52, 138, 70), scale=4, contrast=.4); line(img, [(100, 60), (160, 4)], '#c8a070', 4); fill(img, '#c8a070', 37, ell=(84, 50, 114, 74), scale=3)
    volume(img, (30, 52, 140, 144), .45, .3)
    save(img, 'v_uchimizu', 'Ведёрко для полива', C, 'b', 40)


# ───────────────────────────── СПАЛЬНЯ ─────────────────────────────
def screen(img, x0, y0, w, h, panels, paint_fn, frame='#1a120c', base='#d8c088', seed=1):
    pw = w / panels
    for k in range(panels):
        xa = x0 + k * pw; fill(img, base, seed + k, rect=(xa, y0, xa + pw - 2, y0 + h), scale=8, contrast=.6, dark=.2, light=.15)
    paint_fn(img)
    d = ImageDraw.Draw(img)
    for k in range(panels + 1): d.line([(px(x0 + k * pw - 1), px(y0)), (px(x0 + k * pw - 1), px(y0 + h))], fill=H(frame), width=px(4))
    d.rectangle([px(x0), px(y0), px(x0 + w), px(y0 + h)], outline=H(frame), width=px(4))


def bedroom():
    C = 'Спальня'
    img = canvas(240, 260); floor_shadow(img, 120, 254, 110)                                  # tansu
    fill(img, '#6a3a1e', 40, rect=(14, 20, 226, 250), scale=8, stretch=(4, .6), contrast=1.1)
    d = ImageDraw.Draw(img)
    for k, (y0, y1) in enumerate(((30, 90), (96, 150), (156, 240))):
        d.rectangle([px(24), px(y0), px(216), px(y1)], outline=H('#3a1e10'), width=px(2))
        for x in (70, 170): d.ellipse([px(x - 12), px((y0 + y1) / 2 - 12), px(x + 12), px((y0 + y1) / 2 + 12)], fill=H('#2a2622')); d.arc([px(x - 9), px((y0 + y1) / 2 - 4), px(x + 9), px((y0 + y1) / 2 + 12)], 0, 180, fill=H('#8a8074'), width=px(2))
    for x, y in ((14, 20), (214, 20), (14, 238), (214, 238)): d.rectangle([px(x), px(y), px(x + 12), px(y + 12)], fill=H('#2a2622'))
    volume(img, (14, 20, 226, 250), .4, .2, spec=.15)
    save(img, 'b_tansu', 'Комод тансу', C, 'b', 220)
    img = canvas(300, 230); floor_shadow(img, 150, 226, 140)
    screen(img, 10, 10, 280, 212, 4, lambda im: [(line(im, [(60 + k * 60, 150), (90 + k * 60, 110)], '#2a2622', 2), poly(im, [(70 + k * 60, 120), (100 + k * 60, 96), (130 + k * 60, 118), (100 + k * 60, 112)], '#f4f0e6'), ell(im, (96 + k * 60, 92, 104 + k * 60, 100), '#c02a2a')) for k in range(3)], base='#d8b870', seed=41)
    save(img, 'b_byobu_tsuru', 'Ширма с журавлями', C, 'b', 200)
    img = canvas(300, 230); floor_shadow(img, 150, 226, 140); rr = random.Random(12)
    def sak(im):
        line(im, [(30, 200), (90, 120), (160, 80), (270, 50)], '#2a1a14', 6); line(im, [(120, 100), (150, 150)], '#2a1a14', 3)
        dd = ImageDraw.Draw(im)
        for _ in range(60): x, y = rr.uniform(60, 280), rr.uniform(30, 170); dd.ellipse([px(x - 4), px(y - 4), px(x + 4), px(y + 4)], fill=H(rr.choice(['#f4c4d2', '#e896b0', '#f8dde4'])))
    screen(img, 10, 10, 280, 212, 4, sak, base='#2a2a30', seed=45)
    save(img, 'b_byobu_sakura', 'Ширма с сакурой', C, 'b', 200)
    img = canvas(110, 260); floor_shadow(img, 55, 254, 44)                                     # bonbori
    fill(img, '#1a1210', 50, rect=(49, 110, 61, 240), scale=3); fill(img, '#1a1210', 51, ell=(20, 232, 90, 254), scale=4)
    fill(img, '#f0d8a0', 52, poly=[(18, 28), (92, 28), (100, 114), (10, 114)], scale=5, contrast=.6); ImageDraw.Draw(img).rectangle([px(18), px(20), px(92), px(30)], fill=H('#1a1210'))
    ImageDraw.Draw(img).line([(px(55), px(28)), (px(55), px(114))], fill=(160, 110, 50, 150), width=px(1)); text(img, '桃', 55, 74, 24, '#b8322a', SERIF)
    save(img, 'b_bonbori', 'Фонарь бонбори', C, 'b', 110, glow=[55, 70])
    img = canvas(200, 90); floor_shadow(img, 100, 84, 90)                                      # makura
    fill(img, '#2a3a6a', 53, ell=(10, 24, 190, 84), scale=5, contrast=.8)
    clip(img, mask_poly(img, ell=(10, 24, 190, 84)), lambda d: [d.arc([px(x - 14), px(40), px(x + 14), px(70)], 180, 360, fill=(220, 225, 235, 200), width=px(2)) for x in range(14, 190, 22)])
    fill(img, '#f2eee4', 54, ell=(4, 30, 30, 78), scale=3); fill(img, '#f2eee4', 55, ell=(170, 30, 196, 78), scale=3); volume(img, (4, 24, 196, 84), .55, .4)
    save(img, 'b_makura', 'Подушка-валик макура', C, 'b', 40)
    img = canvas(160, 150); floor_shadow(img, 80, 144, 70); rr = random.Random(13)            # stack of books
    for k in range(5):
        y = 132 - k * 24; w = rr.uniform(110, 140); c = rr.choice(['#6a2a22', '#2a3a5a', '#3a5a3a', '#c8a060', '#4a2a4a'])
        fill(img, c, 60 + k, rect=(80 - w / 2 + rr.uniform(-8, 8), y - 20, 80 + w / 2, y), scale=4, stretch=(4, .5)); ImageDraw.Draw(img).line([(px(80 - w / 2 + 6), px(y - 4)), (px(80 + w / 2 - 6), px(y - 4))], fill=H('#efe6d0'), width=px(1.4))
    volume(img, (10, 20, 150, 140), .35, .2)
    save(img, 'b_books', 'Стопка книг', C, 'b', 40)
    img = canvas(220, 170); floor_shadow(img, 110, 164, 100)                                   # hina dolls
    fill(img, '#b8322a', 70, rect=(10, 140, 210, 164), scale=5)
    for k, (x, robe, hat) in enumerate(((66, '#1a2a4a', 'eboshi'), (154, '#b8322a', 'crown'))):
        fill(img, robe, 71 + k, poly=[(x - 40, 140), (x + 40, 140), (x + 24, 70), (x - 24, 70)], scale=4, contrast=.9)
        for j, c in enumerate(('#e8c040', '#2f6a3a', '#f4f0e6')): ImageDraw.Draw(img).line([(px(x - 22 + j * 3), px(76 + j * 4)), (px(x), px(110)), (px(x + 22 - j * 3), px(76 + j * 4))], fill=H(c), width=px(2))
        fill(img, '#f4efe6', 73 + k, ell=(x - 16, 38, x + 16, 72), scale=3, contrast=.3); ImageDraw.Draw(img).chord([px(x - 16), px(36), px(x + 16), px(70)], 180, 360, fill=H('#15110f'))
        if hat == 'eboshi': poly(img, [(x - 8, 38), (x + 8, 38), (x + 2, 12), (x - 4, 14)], '#15110f')
        else: poly(img, [(x - 14, 40), (x - 10, 26), (x, 34), (x + 10, 26), (x + 14, 40)], '#d8b048')
        volume(img, (x - 40, 12, x + 40, 140), .45, .25)
    save(img, 'b_hina', 'Куклы хина', C, 'b', 180)
    img = canvas(130, 150); floor_shadow(img, 65, 144, 50)                                     # moon night lamp
    fill(img, WOOD_D, 80, rect=(40, 120, 90, 144), scale=4); soft(img, lambda d: d.ellipse([px(4), px(4), px(126), px(126)], fill=(250, 220, 150, 110)), 10)
    fill(img, '#f4e8c0', 81, ell=(18, 18, 112, 112), scale=4, contrast=.6); rr = random.Random(2); d = ImageDraw.Draw(img)
    for _ in range(6): x, y, r = rr.uniform(40, 90), rr.uniform(40, 90), rr.uniform(5, 10); d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=(220, 200, 150, 150))
    save(img, 'b_moonlamp', 'Ночник-луна', C, 'b', 90, glow=[65, 65])
    img = canvas(170, 110); floor_shadow(img, 85, 104, 76)                                     # lacquer letter box
    fill(img, '#1a1214', 82, rect=(14, 40, 156, 100), scale=5, contrast=.7); fill(img, '#2a1a1c', 83, poly=[(8, 44), (162, 44), (150, 24), (20, 24)], scale=5)
    d = ImageDraw.Draw(img); d.arc([px(40), px(46), px(110), px(96)], 200, 340, fill=H('#d8b048'), width=px(2)); [d.ellipse([px(x - 3), px(y - 3), px(x + 3), px(y + 3)], fill=H('#d8b048')) for x, y in ((110, 64), (124, 72), (132, 60))]
    rope(img, [(20, 70), (85, 76), (150, 70)], '#c02a2a', 2); volume(img, (8, 24, 162, 100), .4, .25, spec=.4)
    save(img, 'b_fubako', 'Лаковая шкатулка для писем', C, 'b', 90)
    img = canvas(300, 190); floor_shadow(img, 150, 184, 140)                                   # kotatsu
    fill(img, '#8a3a2a', 84, poly=[(16, 110), (284, 110), (296, 180), (4, 180)], scale=8, contrast=.8)
    clip(img, mask_poly(img, poly=[(16, 110), (284, 110), (296, 180), (4, 180)]), lambda d: [d.line([(px(x), px(110)), (px(x - 8), px(180))], fill=(240, 200, 150, 90), width=px(3)) for x in range(30, 290, 28)])
    fill(img, WOOD_L, 85, poly=[(30, 96), (270, 96), (284, 114), (16, 114)], scale=6, stretch=(6, .5))
    for k, x in enumerate((110, 150, 190)): fill(img, '#e8841e', 86 + k, ell=(x - 16, 70, x + 16, 100), scale=3, contrast=1.1); volume(img, (x - 16, 70, x + 16, 100), .6, .4, spec=.3)
    volume(img, (4, 70, 296, 180), .35, .2)
    save(img, 'b_kotatsu', 'Котацу с мандаринами', C, 'b', 240)
    img = canvas(80, 170); floor_shadow(img, 40, 164, 30)                                      # candle
    fill(img, '#2a2622', 90, rect=(14, 146, 66, 164), scale=3); fill(img, '#2a2622', 91, rect=(34, 110, 46, 148), scale=3); fill(img, '#2a2622', 92, ell=(18, 100, 62, 116), scale=3)
    fill(img, '#f2eee0', 93, rect=(28, 50, 52, 106), scale=3, contrast=.3); soft(img, lambda d: d.ellipse([px(14), px(4), px(66), px(60)], fill=(250, 190, 90, 120)), 6)
    poly(img, [(40, 16), (48, 38), (40, 50), (32, 38)], '#f8b040'); ell(img, (37, 34, 43, 48), '#fff4d0')
    save(img, 'b_candle', 'Свеча в подсвечнике', C, 'b', 30, glow=[40, 36])
    img = canvas(240, 150); floor_shadow(img, 120, 144, 110)                                   # nagamochi chest
    fill(img, '#5a2a1a', 94, rect=(14, 50, 226, 144), scale=7, stretch=(4, .6)); fill(img, '#6a3420', 95, rect=(8, 36, 232, 58), scale=6)
    d = ImageDraw.Draw(img)
    for x in (14, 214): d.rectangle([px(x), px(50), px(x + 12), px(144)], fill=H('#2a2622'))
    for x in (60, 180): d.arc([px(x - 18), px(20), px(x + 18), px(52)], 180, 360, fill=H('#2a2622'), width=px(4))
    ell(img, (110, 74, 130, 94), '#d8b048'); volume(img, (8, 20, 232, 144), .4, .25, spec=.2)
    save(img, 'b_nagamochi', 'Сундук нагамоти', C, 'b', 160)
    img = canvas(120, 140); floor_shadow(img, 60, 134, 50)                                     # cloth cat doll
    fill(img, '#f2e6d0', 96, ell=(20, 56, 100, 134), scale=4, contrast=.5); fill(img, '#f2e6d0', 97, ell=(24, 14, 96, 76), scale=4, contrast=.5)
    for sx in (-1, 1): poly(img, [(60 + sx * 34, 36), (60 + sx * 30, 0), (60 + sx * 12, 20)], '#f2e6d0')
    rr = random.Random(5); d = ImageDraw.Draw(img); [d.ellipse([px(x - 7), px(y - 5), px(x + 7), px(y + 5)], fill=H(rr.choice(['#d08040', '#2a2420']))) for x, y in ((40, 90), (80, 104), (44, 30), (84, 60))]
    for ex in (46, 74): d.ellipse([px(ex - 3), px(42), px(ex + 3), px(50)], fill=H('#1a1414'))
    d.polygon([(px(57), px(56)), (px(63), px(56)), (px(60), px(60))], fill=H('#d77a80')); ImageDraw.Draw(img).rounded_rectangle([px(34), px(74), px(86), px(80)], px(3), fill=H('#b8322a'))
    volume(img, (20, 0, 100, 134), .45, .35)
    save(img, 'b_nekodoll', 'Тряпичная кошечка', C, 'b', 50)


# ───────────────────────────── ОНСЭН ─────────────────────────────
def onsen():
    C = 'Онсэн'
    img = canvas(150, 80); floor_shadow(img, 75, 74, 68)                                        # kerorin tub
    fill(img, '#f0c830', 100, poly=[(8, 20), (142, 20), (126, 74), (24, 74)], scale=4, contrast=.6); fill(img, '#d8a820', 101, ell=(8, 12, 142, 30), scale=4)
    text(img, 'ケロリン', 75, 50, 16, '#c02a2a', SANS); volume(img, (8, 12, 142, 74), .5, .3, spec=.3)
    save(img, 'o_kerorin', 'Жёлтый тазик кэрорин', C, 'b', 30)
    img = canvas(140, 110); floor_shadow(img, 70, 104, 62)                                      # bath stool
    fill(img, WOOD_L, 102, rect=(10, 30, 130, 50), scale=6, stretch=(5, .5)); fill(img, WOOD, 103, rect=(18, 50, 34, 104), scale=4); fill(img, WOOD, 104, rect=(106, 50, 122, 104), scale=4)
    volume(img, (10, 30, 130, 104), .4, .2)
    save(img, 'o_isu', 'Деревянный банный табурет', C, 'b', 40)
    img = canvas(170, 130); floor_shadow(img, 85, 124, 76)                                      # bottles
    for k, (x, c, h) in enumerate(((40, '#2a6a5a', 96), (85, '#e8e0cc', 110), (130, '#8a3a2a', 88))):
        fill(img, c, 105 + k, rect=(x - 18, 124 - h, x + 18, 124), scale=4, contrast=.7); fill(img, '#1a1a1a', 108 + k, rect=(x - 8, 110 - h, x + 8, 124 - h), scale=3)
        fill(img, '#f2eee4', 111 + k, rect=(x - 14, 124 - h * .7, x + 14, 124 - h * .35), scale=3, contrast=.3); volume(img, (x - 18, 110 - h, x + 18, 124), .6, .4, spec=.4)
    save(img, 'o_bottles', 'Бутылочки для мытья', C, 'b', 40)
    img = canvas(80, 150); floor_shadow(img, 40, 144, 30)                                       # milk bottle
    fill(img, (240, 244, 246, 255), 115, poly=[(14, 144), (66, 144), (66, 70), (54, 40), (54, 22), (26, 22), (26, 40), (14, 70)], scale=3, contrast=.2)
    fill(img, '#e8d8a0', 116, rect=(24, 10, 56, 24), scale=3); fill(img, '#2a5aa8', 117, rect=(18, 80, 62, 120), scale=3, contrast=.4); text(img, '牛乳', 40, 100, 14, '#f4f0e6', SERIF)
    volume(img, (14, 10, 66, 144), .6, .4, spec=.55)
    save(img, 'o_milk', 'Молоко после бани', C, 'b', 25)
    img = canvas(200, 150); floor_shadow(img, 100, 144, 88)                                     # clothes basket
    fill(img, '#b08a50', 118, poly=[(10, 40), (190, 40), (176, 144), (24, 144)], scale=5, stretch=(4, 1), contrast=1.2)
    clip(img, mask_poly(img, poly=[(10, 40), (190, 40), (176, 144), (24, 144)]), lambda d: [d.line([(px(0), px(y)), (px(200), px(y))], fill=(90, 60, 30, 150), width=px(1.4)) for y in range(46, 144, 9)])
    fill(img, '#2a3a6a', 119, poly=[(30, 44), (110, 20), (170, 44), (120, 56)], scale=5); fill(img, '#f2eee4', 120, poly=[(90, 44), (150, 26), (176, 44)], scale=4, contrast=.3)
    volume(img, (10, 20, 190, 144), .45, .25)
    save(img, 'o_kago', 'Корзина для одежды', C, 'b', 40)
    img = canvas(110, 90); floor_shadow(img, 55, 84, 44)                                        # rubber duck
    fill(img, '#f4cc30', 121, ell=(8, 36, 100, 86), scale=3, contrast=.5); fill(img, '#f4cc30', 122, ell=(44, 6, 88, 50), scale=3, contrast=.5)
    poly(img, [(86, 30), (106, 34), (86, 40)], '#e8841e'); ell(img, (72, 20, 78, 26), '#1a1414'); volume(img, (8, 6, 106, 86), .6, .4, spec=.45)
    save(img, 'o_duck', 'Резиновая уточка', C, 'b', 20)
    img = canvas(160, 160); floor_shadow(img, 80, 154, 64)                                      # snow monkey statue
    fill(img, '#8a8478', 123, ell=(24, 70, 136, 156), scale=5, contrast=1.1); fill(img, '#8a8478', 124, ell=(42, 18, 118, 88), scale=5, contrast=1.1)
    fill(img, '#d89a8a', 125, ell=(58, 38, 102, 80), scale=3, contrast=.5); ell(img, (66, 50, 74, 58), '#1a1414'); ell(img, (86, 50, 94, 58), '#1a1414')
    fill(img, '#f2eee4', 126, ell=(56, 8, 104, 30), scale=3, contrast=.2); volume(img, (24, 8, 136, 156), .5, .35)
    save(img, 'o_saru', 'Снежная обезьянка', C, 'b', 80)
    img = canvas(170, 110); floor_shadow(img, 85, 104, 76)                                      # towel on a stone
    fill(img, '#6a6d66', 127, ell=(8, 50, 162, 108), scale=5, contrast=1.3); volume(img, (8, 50, 162, 108), .5, .3)
    fill(img, '#f2eee4', 128, poly=[(40, 56), (130, 50), (136, 76), (46, 84)], scale=4, contrast=.3); fill(img, '#2a4a7a', 129, rect=(60, 60, 120, 66), scale=3)
    save(img, 'o_towelstone', 'Полотенце на камне', C, 'b', 25)
    img = canvas(170, 130); floor_shadow(img, 85, 124, 76); rr = random.Random(21)             # yuzu basket
    for k in range(8): x, y = 40 + (k % 4) * 30 + (k // 4) * 14, 60 - (k // 4) * 22; fill(img, '#e8c030', 130 + k, ell=(x - 17, y - 16, x + 17, y + 16), scale=3, contrast=1.3); volume(img, (x - 17, y - 16, x + 17, y + 16), .6, .45, spec=.3)
    fill(img, '#a8844a', 140, poly=[(10, 70), (160, 70), (146, 124), (24, 124)], scale=5, stretch=(4, 1), contrast=1.2); volume(img, (10, 70, 160, 124), .45, .25)
    save(img, 'o_yuzukago', 'Корзинка юдзу', C, 'b', 35)
    img = canvas(120, 160); fill(img, WOOD_L, 141, rect=(10, 10, 110, 150), scale=6, stretch=(.4, 3)); line(img, [(30, 10), (60, 0), (90, 10)], '#2a2018', 2)   # 湯 sign
    text(img, '湯', 60, 80, 70, '#1a1410', SERIF, brush=True); volume(img, (10, 10, 110, 150), .35, .2)
    save(img, 'o_yusign', 'Табличка «Горячая вода»', C, 't', 40)
    img = canvas(170, 60); floor_shadow(img, 85, 54, 76)                                        # bath slippers
    for x in (50, 120): fill(img, '#2a4a7a', 142 + x, ell=(x - 30, 20, x + 30, 54), scale=4, contrast=.6); fill(img, '#e8e0cc', 143 + x, ell=(x - 22, 18, x + 22, 34), scale=3)
    save(img, 'o_slippers', 'Банные тапочки', C, 'b', 20)
    img = canvas(110, 60); floor_shadow(img, 55, 54, 46)                                        # soap in a dish
    fill(img, '#e8e0cc', 145, ell=(6, 26, 104, 56), scale=3, contrast=.5); fill(img, '#f2b8c8', 146, rect=(30, 14, 80, 38), scale=3, contrast=.4); volume(img, (30, 14, 80, 38), .5, .3, spec=.4)
    for k in range(4): soft(img, lambda d, k=k: d.ellipse([px(30 + k * 12), px(4 + (k % 2) * 6), px(40 + k * 12), px(14 + (k % 2) * 6)], outline=(240, 240, 255, 200), width=px(1)), .5)
    save(img, 'o_soap', 'Мыло в мыльнице', C, 'b', 15)


# ───────────────────────────── ГАРДЕРОБ ─────────────────────────────
def wardrobe():
    C = 'Гардероб'
    for iid, n, col, pat in (('wr_ikou_blue', 'Кимоно на вешалке «Волны»', '#223a6a', 'nami'), ('wr_ikou_red', 'Кимоно на вешалке «Камелии»', '#8a1e24', 'tsubaki'), ('wr_ikou_green', 'Кимоно на вешалке «Бамбук»', '#2a4a34', 'take')):
        img = canvas(300, 330); floor_shadow(img, 150, 324, 140)
        fill(img, '#1a120c', 150, rect=(4, 20, 296, 32), scale=5, stretch=(6, .5)); fill(img, '#1a120c', 151, rect=(40, 32, 52, 324), scale=4); fill(img, '#1a120c', 152, rect=(248, 32, 260, 324), scale=4)
        fill(img, '#1a120c', 153, rect=(30, 306, 70, 324), scale=4); fill(img, '#1a120c', 154, rect=(238, 306, 278, 324), scale=4)
        m = fill(img, col, 155, poly=[(10, 36), (290, 36), (286, 150), (220, 160), (230, 300), (70, 300), (80, 160), (14, 150)], scale=10, stretch=(1, 3), contrast=.9)
        rr = random.Random(len(iid))
        if pat == 'nami': clip(img, m, lambda d: [d.arc([px(x - 14), px(y - 10), px(x + 14), px(y + 10)], 180, 360, fill=(220, 225, 235, 200), width=px(2)) for x in range(10, 300, 24) for y in range(200, 300, 16)])
        elif pat == 'tsubaki': clip(img, m, lambda d: [d.ellipse([px(x - 9), px(y - 9), px(x + 9), px(y + 9)], fill=(236, 230, 214, 230)) for x, y in [(rr.uniform(20, 280), rr.uniform(50, 290)) for _ in range(26)]])
        else: clip(img, m, lambda d: [d.line([(px(x), px(160)), (px(x), px(300))], fill=(150, 190, 130, 200), width=px(4)) for x in range(90, 220, 26)])
        fill(img, '#d8b048', 156, rect=(80, 150, 220, 184), scale=4, contrast=.8)
        poly(img, [(128, 36), (150, 100), (172, 36)], '#f2eee4'); volume(img, (10, 36, 290, 300), .35, .2)
        save(img, iid, n, C, 'b', 260)
    img = canvas(200, 120); floor_shadow(img, 100, 114, 88)                                     # obi rolls
    for k, (x, y, c) in enumerate(((50, 90, '#d8b048'), (110, 90, '#b8322a'), (170, 90, '#2a3a6a'), (80, 50, '#e8a0b6'), (140, 50, '#2f6a3a'))):
        fill(img, c, 160 + k, ell=(x - 30, y - 30, x + 30, y + 26), scale=3, contrast=.8); ImageDraw.Draw(img).ellipse([px(x - 12), px(y - 12), px(x + 12), px(y + 10)], outline=dk(H(c), .3), width=px(2)); volume(img, (x - 30, y - 30, x + 30, y + 26), .5, .4, spec=.2)
    save(img, 'wr_obi', 'Свёрнутые пояса оби', C, 'b', 90)
    img = canvas(220, 110); floor_shadow(img, 110, 104, 100)                                    # tatoushi box
    fill(img, '#efe6cc', 165, rect=(10, 30, 210, 100), scale=6, contrast=.4); rope(img, [(110, 30), (110, 100)], '#b8322a', 3); rope(img, [(10, 64), (210, 64)], '#b8322a', 3)
    text(img, '着物', 60, 48, 18, '#3a2a1a', SERIF); volume(img, (10, 30, 210, 100), .3, .2)
    save(img, 'wr_tatoushi', 'Коробка для кимоно', C, 'b', 50)
    img = canvas(160, 110); floor_shadow(img, 80, 104, 70)                                      # kanzashi box
    fill(img, '#1a1214', 166, rect=(14, 50, 146, 104), scale=5); fill(img, '#8a1a1a', 167, rect=(20, 54, 140, 70), scale=4)
    for k, x in enumerate((40, 70, 100, 124)): line(img, [(x, 60), (x + 14, 10)], '#d8b048', 2); I.ell(img, (x + 6, 2, x + 22, 18), ['#f090b0', '#e8c040', '#c02a4a', '#f4c4d2'][k])
    volume(img, (14, 50, 146, 104), .4, .2, spec=.3)
    save(img, 'wr_kanzashibox', 'Шкатулка с кандзаси', C, 'b', 90)
    img = canvas(170, 70); floor_shadow(img, 85, 64, 76)                                        # zori
    for x in (50, 120): fill(img, '#f2eee4', 170 + x, ell=(x - 30, 22, x + 30, 60), scale=4, contrast=.3); line(img, [(x - 16, 30), (x, 22), (x + 16, 30)], '#b8322a', 4)
    save(img, 'wr_zori', 'Сандалии дзори', C, 'b', 50)
    img = canvas(190, 150); floor_shadow(img, 95, 144, 84)                                      # sewing box
    fill(img, '#8a5a30', 175, rect=(14, 70, 176, 144), scale=6, stretch=(4, .5)); fill(img, '#6a4020', 176, rect=(8, 60, 182, 74), scale=5)
    for k, (x, c) in enumerate(((50, '#b8322a'), (90, '#2a4a8a'), (130, '#e8c040'))): fill(img, c, 177 + k, ell=(x - 20, 30, x + 20, 70), scale=3, contrast=.9); volume(img, (x - 20, 30, x + 20, 70), .5, .4)
    line(img, [(150, 60), (176, 16)], '#c8c8d0', 1.6); volume(img, (8, 60, 182, 144), .4, .2)
    save(img, 'wr_haribako', 'Шкатулка для шитья', C, 'b', 60)
    img = canvas(200, 170); floor_shadow(img, 100, 164, 80)                                     # fan on a stand
    fill(img, WOOD_D, 180, rect=(40, 150, 160, 164), scale=4); line(img, [(100, 150), (100, 120)], '#3a2a1a', 4)
    m = Image.new('L', img.size, 0); md = ImageDraw.Draw(m); md.pieslice([px(10), px(30), px(190), px(210)], 200, 340, fill=255); md.pieslice([px(70), px(90), px(130), px(150)], 200, 340, fill=0)
    fill(img, '#2a1c14', 181, mask=m, scale=6); rr = random.Random(3)
    clip(img, m, lambda d: [d.rectangle([px(x - 6), px(y - 6), px(x + 6), px(y + 6)], fill=(216, 176, 72, 220)) for x, y in [(rr.uniform(10, 190), rr.uniform(30, 120)) for _ in range(40)]])
    save(img, 'wr_fanstand', 'Веер на подставке', C, 'b', 90)


# ───────────────────────────── ДВОРИК ─────────────────────────────
def courtyard():
    C = 'Дворик'
    st = '#6a6d66'
    img = canvas(180, 110); floor_shadow(img, 90, 104, 84)                                      # stone turtle
    fill(img, st, 190, ell=(20, 30, 150, 100), scale=5, contrast=1.3); fill(img, st, 191, ell=(136, 50, 176, 82), scale=4, contrast=1.3)
    clip(img, mask_poly(img, ell=(20, 30, 150, 100)), lambda d: [d.polygon([(px(x + 12 * math.cos(a)), px(y + 10 * math.sin(a))) for a in [k * math.pi / 3 for k in range(6)]], outline=(60, 62, 58, 220), width=px(2)) for x, y in ((60, 56), (90, 50), (116, 60), (74, 80), (104, 80))])
    for x in (36, 128): fill(img, st, 192 + x, ell=(x - 14, 84, x + 14, 104), scale=3)
    volume(img, (20, 30, 176, 104), .5, .3); P.dab_mass(ImageDraw.Draw(img), [(px(80), px(40), px(40), px(10))], 120, 'leaf', [hexc('#2a3e20'), hexc('#3e5a2c'), hexc('#5a7a3c')], random.Random(3), size=(2, 4))
    save(img, 'c_kame', 'Каменная черепаха', C, 'b', 90)
    img = canvas(140, 300); floor_shadow(img, 70, 294, 50)                                      # heron
    line(img, [(60, 294), (64, 190)], '#3a3432', 3); line(img, [(84, 294), (78, 190)], '#3a3432', 3)
    fill(img, '#e8e6e0', 193, ell=(34, 120, 118, 200), scale=4, contrast=.4); fill(img, '#e8e6e0', 194, poly=[(90, 130), (104, 60), (96, 30), (84, 34), (92, 60), (78, 128)], scale=4, contrast=.4)
    fill(img, '#e8e6e0', 195, ell=(80, 20, 110, 44), scale=3); poly(img, [(106, 30), (140, 34), (106, 38)], '#d8a830'); ell(img, (96, 28, 101, 33), '#1a1414')
    line(img, [(84, 24), (60, 20)], '#1a1a1a', 2); fill(img, '#9a9a98', 196, poly=[(34, 150), (4, 190), (40, 180)], scale=3); volume(img, (4, 20, 140, 200), .45, .25)
    save(img, 'c_sagi', 'Белая цапля', C, 'b', 110)
    img = canvas(200, 320); floor_shadow(img, 100, 314, 50)                                     # kakashi scarecrow
    line(img, [(100, 314), (100, 60)], '#6a4a2a', 6); line(img, [(20, 120), (180, 120)], '#6a4a2a', 5)
    fill(img, '#2a4a7a', 197, poly=[(40, 110), (160, 110), (150, 230), (50, 230)], scale=6, contrast=.8); fill(img, '#b8322a', 198, rect=(50, 160, 150, 174), scale=4)
    fill(img, '#efe6d0', 199, ell=(70, 50, 130, 110), scale=3, contrast=.3); ell(img, (86, 72, 94, 80), '#1a1414'); ell(img, (106, 72, 114, 80), '#1a1414'); line(img, [(90, 94), (110, 94)], '#1a1414', 2)
    poly(img, [(30, 60), (100, 20), (170, 60)], '#b8975a'); volume(img, (20, 20, 180, 230), .35, .2)
    save(img, 'c_kakashi', 'Пугало какаси', C, 'b', 90)
    img = canvas(160, 110); floor_shadow(img, 80, 104, 70)                                      # sand rake
    fill(img, '#d8d0bc', 200, rect=(4, 60, 156, 104), scale=6, contrast=.4)
    clip(img, mask_poly(img, rect=(4, 60, 156, 104)), lambda d: [d.line([(px(0), px(y)), (px(160), px(y))], fill=(150, 140, 120, 180), width=px(1.2)) for y in range(64, 104, 6)])
    line(img, [(40, 64), (150, 4)], '#8a6038', 4); fill(img, WOOD, 201, rect=(14, 56, 70, 64), scale=3)
    save(img, 'c_rake', 'Грабли для сада камней', C, 'b', 50)
    img = canvas(160, 150); floor_shadow(img, 80, 144, 70)                                      # mossy stump with mushrooms
    fill(img, '#6a4a2a', 202, poly=[(24, 144), (136, 144), (126, 50), (34, 50)], scale=5, stretch=(.3, 3)); fill(img, '#a8844a', 203, ell=(34, 38, 126, 62), scale=4)
    ImageDraw.Draw(img).ellipse([px(60), px(44), px(100), px(56)], outline=H('#6a4a2a'), width=px(2))
    P.dab_mass(ImageDraw.Draw(img), [(px(40), px(120), px(20), px(20))], 200, 'leaf', [hexc('#2a3e20'), hexc('#3e5a2c'), hexc('#5a7a3c')], random.Random(4), size=(2, 4))
    for x, y, r in ((120, 110, 14), (138, 124, 10)): fill(img, '#b8322a', 204 + x, ell=(x - r, y - r * .7, x + r, y + r * .3), scale=3); ImageDraw.Draw(img).rectangle([px(x - 3), px(y), px(x + 3), px(y + r)], fill=H('#efe6d0'))
    volume(img, (24, 38, 150, 144), .45, .25)
    save(img, 'c_stump', 'Пенёк с грибами', C, 'b', 50)
    img = canvas(280, 140); floor_shadow(img, 140, 134, 128)                                    # little arched bridge
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).chord([px(10), px(40), px(270), px(220)], 180, 360, fill=255); ImageDraw.Draw(m).chord([px(50), px(80), px(230), px(240)], 180, 360, fill=0)
    fill(img, '#b8322a', 206, mask=m, scale=6, contrast=.9)
    d = ImageDraw.Draw(img); d.arc([px(20), px(20), px(260), px(160)], 190, 350, fill=H('#b8322a'), width=px(6))
    for k in range(7): a = math.radians(195 + k * 25); d.line([(px(140 + math.cos(a) * 120), px(90 + math.sin(a) * 70)), (px(140 + math.cos(a) * 130), px(130 + math.sin(a) * 50))], fill=H('#8a1a14'), width=px(4))
    volume(img, (10, 20, 270, 134), .35, .2)
    save(img, 'c_bridge', 'Горбатый мостик', C, 'b', 240)
    img = canvas(170, 110); floor_shadow(img, 85, 104, 76)                                      # frogs on a stone
    fill(img, st, 207, ell=(8, 50, 162, 108), scale=5, contrast=1.3); volume(img, (8, 50, 162, 108), .5, .3)
    for k, x in enumerate((50, 90, 126)):
        fill(img, '#4a7a3a', 208 + k, ell=(x - 18, 32 - k * 4, x + 18, 62 - k * 4), scale=3); ell(img, (x - 12, 28 - k * 4, x - 4, 36 - k * 4), '#e8e0a0'); ell(img, (x + 4, 28 - k * 4, x + 12, 36 - k * 4), '#e8e0a0')
    save(img, 'c_kaeru3', 'Три лягушки на камне', C, 'b', 60)
    img = canvas(170, 170); floor_shadow(img, 85, 164, 72)                                      # koi fountain statue
    fill(img, st, 211, rect=(40, 124, 130, 164), scale=5, contrast=1.3); volume(img, (40, 124, 130, 164), .4, .2)
    m = blob(img, [(78, 126), (70, 96), (72, 62), (86, 34), (104, 20), (120, 22), (116, 40), (100, 62), (94, 96), (96, 126)], hexc('#c8442a'), 212, scale=3, k=.55, spec=.3)
    clip(img, m, lambda d: [d.arc([px(x - 8), px(y - 6), px(x + 8), px(y + 6)], 200, 340, fill=(240, 200, 170, 170), width=px(1.2)) for x, y in [(84 + j % 2 * 6, 60 + j * 10) for j in range(6)]])
    blob(img, [(80, 124), (60, 146), (74, 150), (88, 136), (102, 150), (114, 144), (96, 124)], hexc('#e8e2d6'), 213, scale=3, k=.3)      # tail fin
    blob(img, [(94, 70), (122, 84), (100, 88)], hexc('#e8e2d6'), 214, scale=3, k=.3)
    ell(img, (104, 28, 110, 34), '#1a1414'); line(img, [(118, 36), (134, 44)], '#e8b060', 1.6)
    for k in range(6): soft(img, lambda d, k=k: d.ellipse([px(120 + k * 4), px(10 + k * 16), px(128 + k * 4), px(18 + k * 16)], fill=(190, 215, 225, 180)), 1)
    save(img, 'c_koifountain', 'Фонтан-карп', C, 'b', 120)


# ───────────────────────────── ВХОД ─────────────────────────────
def cr(pts, n=10):
    N = len(pts); out = []
    for i in range(N):
        p0, p1, p2, p3 = pts[(i - 1) % N], pts[i], pts[(i + 1) % N], pts[(i + 2) % N]
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * (2 * p1[c] + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t2 + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t3) for c in (0, 1)))
    return out


def blob(img, pts, col, seed, scale=5, contrast=1.2, k=.5, rim=.35, spec=0):
    sp = cr(pts); m = mask_poly(img, poly=sp).filter(ImageFilter.GaussianBlur(.6 * I.S)); tmp = Image.new('RGBA', img.size, (0, 0, 0, 0)); fill(tmp, col, seed, mask=m, scale=scale, contrast=contrast)
    xs = [q[0] for q in sp]; ys = [q[1] for q in sp]; volume(tmp, (min(xs), min(ys), max(xs), max(ys)), k, rim, spec=spec); img.alpha_composite(tmp); return m


def lion(img, cx, base, flip, seed, col='#7a7c74', open_mouth=True):
    figure_base(img, cx, base, 120, '#5a5c56', seed)
    s = -1 if flip else 1; X = lambda x: cx + s * x; b = base - 26
    blob(img, [(X(-44), b), (X(-50), b - 40), (X(-30), b - 76), (X(0), b - 84), (X(24), b - 70), (X(30), b - 30), (X(40), b)], col, seed + 1)      # haunch and body
    for dx in (4, 26): blob(img, [(X(dx - 8), b), (X(dx - 9), b - 60), (X(dx + 9), b - 60), (X(dx + 9), b)], dk(H(col), .05), seed + 2 + dx, k=.4)   # front legs
    rr = random.Random(seed); d = ImageDraw.Draw(img); hx, hy = X(10), b - 104
    for k in range(14):
        a = math.pi * (.5 + k / 13 * 1.6) * (1 if s > 0 else -1); r = 34 + rr.uniform(-3, 3)
        q = (hx + math.cos(a) * r * .9, hy + math.sin(a) * r)
        blob(img, [(q[0] - 11, q[1]), (q[0], q[1] - 11), (q[0] + 11, q[1]), (q[0], q[1] + 11)], dk(H(col), .2), seed + 10 + k, scale=3, k=.6, rim=.3)
    blob(img, [(hx - 26, hy + 14), (hx - 28, hy - 14), (hx - 10, hy - 30), (hx + 14, hy - 30), (hx + 30, hy - 12), (hx + 28, hy + 16), (hx, hy + 26)], col, seed + 30)
    d = ImageDraw.Draw(img)
    for ex in (-11, 11): d.ellipse([px(hx + ex - 6), px(hy - 12), px(hx + ex + 6), px(hy - 2)], fill=H('#e8e2d6')); d.ellipse([px(hx + ex - 3), px(hy - 10), px(hx + ex + 3), px(hy - 4)], fill=H('#2a2a28'))
    d.ellipse([px(hx - 7), px(hy - 2), px(hx + 7), px(hy + 6)], fill=dk(H(col), .35))
    if open_mouth: d.chord([px(hx - 16), px(hy + 2), px(hx + 16), px(hy + 22)], 0, 180, fill=H('#3a2422')); [d.polygon([(px(hx + t - 3), px(hy + 8)), (px(hx + t + 3), px(hy + 8)), (px(hx + t), px(hy + 14))], fill=H('#e8e2d6')) for t in (-9, 9)]
    else: d.arc([px(hx - 14), px(hy + 4), px(hx + 14), px(hy + 16)], 20, 160, fill=H('#3a2422'), width=px(3))
    P.dab_mass(ImageDraw.Draw(img), [(px(X(-30)), px(b - 10), px(14), px(8))], 80, 'leaf', [hexc('#2a3e20'), hexc('#3e5a2c'), hexc('#5a7a3c')], rr, size=(2, 4))


def fox_statue(img, cx, base, seed, bib=True, key=False):
    figure_base(img, cx, base, 100, '#5a5c56', seed)
    col = hexc('#e8e2d6'); b = base - 26
    blob(img, [(cx + 26, b - 10), (cx + 58, b - 40), (cx + 64, b - 100), (cx + 50, b - 132), (cx + 40, b - 104), (cx + 44, b - 50), (cx + 20, b - 26)], col, seed + 1, k=.4)   # tail
    blob(img, [(cx - 30, b), (cx - 34, b - 50), (cx - 20, b - 100), (cx, b - 110), (cx + 20, b - 100), (cx + 32, b - 50), (cx + 30, b)], col, seed + 2)                         # body
    for dx in (-12, 10): blob(img, [(cx + dx - 7, b), (cx + dx - 7, b - 56), (cx + dx + 7, b - 56), (cx + dx + 7, b)], dk(col, .06), seed + 3 + dx, k=.35)
    hy = b - 124
    blob(img, [(cx - 22, hy + 4), (cx - 20, hy - 14), (cx - 8, hy - 22), (cx + 8, hy - 22), (cx + 20, hy - 14), (cx + 22, hy + 4), (cx + 6, hy + 30), (cx, hy + 36), (cx - 6, hy + 30)], col, seed + 4)
    for sx in (-1, 1): blob(img, [(cx + sx * 8, hy - 16), (cx + sx * 20, hy - 50), (cx + sx * 26, hy - 10)], col, seed + 5 + sx, scale=3, k=.3)
    d = ImageDraw.Draw(img)
    for sx in (-1, 1): d.line([(px(cx + sx * 5), px(hy - 2)), (px(cx + sx * 17), px(hy - 6))], fill=H('#c02a2a'), width=px(2.6)); d.line([(px(cx + sx * 12), px(hy - 22)), (px(cx + sx * 18), px(hy - 40))], fill=H('#c02a2a'), width=px(2))
    d.ellipse([px(cx - 3), px(hy + 30), px(cx + 3), px(hy + 36)], fill=H('#2a2622'))
    if bib: blob(img, [(cx - 22, b - 100), (cx + 22, b - 100), (cx + 4, b - 70), (cx, b - 64), (cx - 4, b - 70)], hexc('#c02a2a'), seed + 8, scale=3, k=.3)
    if key: line(img, [(cx + 8, hy + 30), (cx + 36, hy + 38)], '#d8b048', 4); ell(img, (cx + 32, hy + 32, cx + 44, hy + 44), '#d8b048')


def entrance():
    C = 'Вход'
    img = canvas(220, 150); floor_shadow(img, 110, 144, 100)                                    # saisen-bako
    fill(img, WOOD_D, 220, rect=(14, 50, 206, 144), scale=7, stretch=(4, .6)); fill(img, WOOD, 221, poly=[(8, 50), (212, 50), (196, 30), (24, 30)], scale=6)
    d = ImageDraw.Draw(img)
    for k in range(9): d.line([(px(30 + k * 20), px(32)), (px(30 + k * 20), px(48))], fill=H('#2a1a10'), width=px(3))
    text(img, '奉納', 110, 96, 30, '#f2e6c0', SERIF); volume(img, (8, 30, 212, 144), .4, .2)
    save(img, 'e_saisen', 'Ящик для пожертвований', C, 'b', 120)
    img = canvas(120, 330); fill(img, '#d8b048', 222, ell=(28, 10, 92, 70), scale=3, contrast=1.3); volume(img, (28, 10, 92, 70), .7, .4, spec=.5)       # shrine bell rope
    for k, c in enumerate(('#c02a2a', '#f2eee4', '#6a3a8a', '#c02a2a', '#f2eee4')): rope(img, [(52 + k * 4, 64), (50 + k * 5, 300)], c, 5)
    fill(img, '#c02a2a', 223, poly=[(40, 290), (80, 290), (86, 326), (34, 326)], scale=3)
    save(img, 'e_suzunawa', 'Колокол с верёвкой', C, 't', 110)
    img = canvas(280, 250); floor_shadow(img, 140, 244, 128)                                     # ema rack
    fill(img, WOOD_D, 224, rect=(20, 30, 32, 244), scale=4); fill(img, WOOD_D, 225, rect=(248, 30, 260, 244), scale=4); poly(img, [(4, 36), (140, 4), (276, 36)], '#3a2418')
    for row, y in enumerate((60, 110, 160)):
        line(img, [(32, y), (248, y)], '#2a1a10', 2)
        for k in range(6): x = 46 + k * 36 + (row % 2) * 8; fill(img, '#c9a778', 230 + row * 6 + k, poly=[(x - 14, y + 8), (x, y + 2), (x + 14, y + 8), (x + 14, y + 36), (x - 14, y + 36)], scale=4, stretch=(4, .5)); ImageDraw.Draw(img).line([(px(x - 6), px(y + 20)), (px(x + 6), px(y + 24))], fill=H('#2a1a10'), width=px(1.4))
    save(img, 'e_emarack', 'Стойка с эма', C, 'b', 150)
    img = canvas(260, 170); line(img, [(4, 10), (256, 10)], '#6a4a2a', 3)                        # omikuji tied on a rope
    rr = random.Random(30)
    for k in range(22): x = 14 + k * 11; fill(img, '#f4f0e6', 240 + k, poly=[(x - 4, 10), (x + 4, 10), (x + 3, 60 + rr.uniform(0, 40)), (x - 3, 60 + rr.uniform(0, 40))], scale=3, contrast=.2); ImageDraw.Draw(img).line([(px(x - 4), px(14)), (px(x + 4), px(20))], fill=H('#c8c0b0'), width=px(1.6))
    save(img, 'e_omikujiwall', 'Верёвка с омикудзи', C, 't', 40)
    img = canvas(160, 210); lion(img, 80, 206, False, 250, open_mouth=True); save(img, 'e_komainu_a', 'Комаину «А»', C, 'b', 180)
    img = canvas(160, 210); lion(img, 80, 206, True, 260, open_mouth=False); save(img, 'e_komainu_un', 'Комаину «Ун»', C, 'b', 180)
    img = canvas(150, 220); fox_statue(img, 64, 216, 270, key=True); save(img, 'e_inari_key', 'Лиса Инари с ключом', C, 'b', 170)
    img = canvas(150, 220); fox_statue(img, 64, 216, 280, key=False); save(img, 'e_inari', 'Лиса Инари', C, 'b', 170)
    img = canvas(120, 190); figure_base(img, 60, 186, 90, '#5a5c56', 290)                         # jizo
    fill(img, '#8a8c84', 291, ell=(22, 50, 98, 166), scale=5, contrast=1.2); fill(img, '#8a8c84', 292, ell=(32, 14, 88, 70), scale=5, contrast=1.2)
    d = ImageDraw.Draw(img); [d.arc([px(x - 7), px(40), px(x + 7), px(48)], 20, 160, fill=H('#3a3a38'), width=px(2)) for x in (50, 70)]
    fill(img, '#c02a2a', 293, poly=[(30, 70), (90, 70), (84, 110), (60, 124), (36, 110)], scale=4, contrast=.7); volume(img, (22, 14, 98, 166), .5, .3)
    save(img, 'e_jizo', 'Дзидзо в красном слюнявчике', C, 'b', 120)
    img = canvas(300, 170); rr = random.Random(31)                                               # shimenawa
    for k in range(3): rope(img, [(4, 20 + k * 6), (150, 44 + k * 6), (296, 20 + k * 6)], '#c8ae74', 10)
    for x in (70, 150, 230):
        for j in range(4): poly(img, [(x - 8, 50 + j * 24), (x + 8, 50 + j * 24), (x + 8 if j % 2 else x - 8, 72 + j * 24)], '#f4f0e6')
    for x in (40, 110, 190, 260): line(img, [(x, 44), (x + rr.uniform(-4, 4), 100)], '#c8ae74', 3)
    save(img, 'e_shimenawa', 'Священная верёвка симэнава', C, 't', 90)


# ───────────────────────────── ИГРЫ ─────────────────────────────
def games():
    C = 'Игры'
    img = canvas(110, 260); floor_shadow(img, 55, 254, 36)                                     # hagoita
    fill(img, '#f2e6d0', 300, poly=[(14, 20), (96, 20), (96, 190), (70, 200), (40, 200), (14, 190)], scale=5, contrast=.4); fill(img, WOOD, 301, rect=(44, 196, 66, 254), scale=4)
    fill(img, '#b8322a', 302, poly=[(30, 60), (80, 60), (90, 180), (20, 180)], scale=4); fill(img, '#f4efe6', 303, ell=(36, 30, 74, 70), scale=3); ImageDraw.Draw(img).chord([px(34), px(26), px(76), px(62)], 180, 360, fill=H('#15110f'))
    for k in range(5): I.ell(img, (30 + k * 12, 110 + (k % 2) * 20, 42 + k * 12, 122 + (k % 2) * 20), '#e8c040')
    volume(img, (14, 20, 96, 200), .4, .2)
    save(img, 'g_hagoita', 'Ракетка хагоита', C, 'b', 90)
    img = canvas(220, 100); floor_shadow(img, 110, 94, 100)                                     # hanafuda cards
    for k, (x, a, c) in enumerate(((50, -.3, '#c02a2a'), (90, -.1, '#2a4a8a'), (130, .1, '#2f6a3a'), (170, .3, '#e8a0b6'))):
        l = canvas(40, 60); fill(l, '#1a1414', 310 + k, rect=(0, 0, 40, 60), scale=3); fill(l, '#efe6d0', 311 + k, rect=(3, 3, 37, 57), scale=3, contrast=.3); I.ell(l, (8, 8, 32, 32), c); I.poly(l, [(4, 56), (20, 36), (36, 56)], '#2a2622')
        P.set_size(220, 100); r = l.rotate(-a * 57, expand=True, resample=Image.BICUBIC); img.alpha_composite(r, (px(x) - r.width // 2, px(52) - r.height // 2))
    save(img, 'g_hanafuda', 'Карты ханафуда', C, 'b', 40)
    img = canvas(220, 110); floor_shadow(img, 110, 104, 100)                                    # sugoroku board
    fill(img, '#efe6cc', 320, rect=(10, 30, 210, 100), scale=6, contrast=.4); d = ImageDraw.Draw(img)
    for k in range(10): x = 20 + k * 19; d.rectangle([px(x), px(40 + (k % 2) * 20), px(x + 16), px(56 + (k % 2) * 20)], fill=H(['#c02a2a', '#2a4a8a', '#e8c040', '#2f6a3a'][k % 4]))
    ell(img, (150, 70, 170, 90), '#f4f0e6'); ell(img, (156, 76, 160, 80), '#1a1414'); volume(img, (10, 30, 210, 100), .3, .2)
    save(img, 'g_sugoroku', 'Доска сугороку', C, 'b', 50)
    img = canvas(110, 110); floor_shadow(img, 55, 104, 44)                                      # kemari ball
    fill(img, '#efe8da', 321, ell=(8, 8, 102, 102), scale=4, contrast=.5); d = ImageDraw.Draw(img)
    for k in range(6): d.arc([px(8 + k * 4), px(8), px(102 - k * 4), px(102)], 0, 360, fill=(150, 120, 90, 120), width=px(1))
    d.line([(px(20), px(55)), (px(90), px(55))], fill=H('#6a4a2a'), width=px(3)); volume(img, (8, 8, 102, 102), .6, .45, spec=.25)
    save(img, 'g_kemari', 'Мяч кэмари', C, 'b', 40)
    img = canvas(150, 150); floor_shadow(img, 75, 144, 50)                                      # taketombo
    fill(img, '#c8a070', 322, poly=[(4, 30), (146, 20), (146, 34), (4, 42)], scale=4, stretch=(4, .5)); line(img, [(75, 32), (75, 144)], '#8a6038', 4)
    save(img, 'g_taketombo', 'Бамбуковая стрекоза', C, 'b', 20)
    img = canvas(200, 200); floor_shadow(img, 100, 194, 86)                                     # taiko drum
    fill(img, '#8a2a1e', 323, rect=(24, 50, 176, 170), scale=6, stretch=(.4, 3)); fill(img, '#efe6d0', 324, ell=(20, 30, 180, 70), scale=4, contrast=.4)
    d = ImageDraw.Draw(img); [d.ellipse([px(x - 4), px(62), px(x + 4), px(70)], fill=H('#2a2622')) for x in range(30, 176, 16)]; text(img, '祭', 100, 50, 26, '#1a1414', SERIF)
    fill(img, WOOD_D, 325, rect=(40, 170, 56, 194), scale=3); fill(img, WOOD_D, 326, rect=(144, 170, 160, 194), scale=3)
    for x, a in ((140, 60), (170, 40)): line(img, [(x, 20), (x - 30, a + 20)], '#c8a070', 5)
    volume(img, (20, 30, 180, 194), .45, .3, spec=.2)
    save(img, 'g_taiko', 'Барабан тайко', C, 'b', 160)
    img = canvas(210, 300); floor_shadow(img, 105, 294, 90)                                     # kadomatsu
    for k, (x, h) in enumerate(((80, 250), (105, 290), (130, 220))):
        fill(img, '#4a7a3a', 330 + k, poly=[(x - 14, 294), (x + 14, 294), (x + 14, 294 - h + 20), (x - 14, 294 - h)], scale=6, stretch=(.3, 3)); ImageDraw.Draw(img).ellipse([px(x - 14), px(294 - h - 4), px(x + 14), px(294 - h + 22)], fill=H('#c8d8a0'))
    P.pine(img, px(105), px(250), px(120), 33, P.PAL_PINE, P.BARK, lean=0, pads=3, spread=.9)
    fill(img, '#c8ae74', 334, rect=(40, 220, 170, 294), scale=5, stretch=(.3, 3)); [rope(img, [(40, y), (105, y + 4), (170, y)], '#6a4a2a', 4) for y in (236, 278)]
    for x in (50, 160): I.ell(img, (x - 10, 206, x + 10, 226), '#e0402a')
    volume(img, (40, 4, 170, 294), .35, .2)
    save(img, 'g_kadomatsu', 'Кадомацу', C, 'b', 150)
    img = canvas(200, 150); floor_shadow(img, 100, 144, 86)                                     # fukuwarai
    fill(img, '#efe6cc', 335, rect=(10, 40, 190, 144), scale=6, contrast=.4); fill(img, '#f4ece0', 336, ell=(50, 50, 150, 140), scale=4, contrast=.3)
    d = ImageDraw.Draw(img); d.chord([px(50), px(46), px(150), px(106)], 180, 360, fill=H('#15110f')); d.ellipse([px(70), px(88), px(84), px(96)], fill=H('#15110f')); d.ellipse([px(130), px(70), px(144), px(78)], fill=H('#15110f'))
    d.arc([px(84), px(110), px(126), px(128)], 200, 340, fill=H('#c02a2a'), width=px(3)); ell(img, (60, 100, 76, 112), '#f0a0a8')
    save(img, 'g_fukuwarai', 'Игра фукуварай', C, 'b', 40)


if __name__ == '__main__':
    kitchen(); veranda(); bedroom(); onsen(); wardrobe(); courtyard(); entrance(); games()
    json.dump(CAT, open(f'{OUT}/rooms.json', 'w'), ensure_ascii=False, indent=0)
    print('TOTAL', len(CAT))
