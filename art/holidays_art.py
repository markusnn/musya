#!/usr/bin/env python3
"""Things for four new holidays (feat/holidays.js): Cat Day, Japanese Halloween, Japanese Christmas, Omisoka.
Same brushes as fest_items.py. All pictures go into ONE atlas: assets/items/atlas_hl.webp; the rect map is printed
and written to art/out/hl.json (it is pasted into feat/holidays.js).
Usage: python3 art/holidays_art.py"""
import json, math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); os.makedirs(f'{HERE}/out', exist_ok=True)
sys.argv = [sys.argv[0], f'{HERE}/out']            # the imported painters read an out dir at import time
import numpy as np
from PIL import Image, ImageDraw
import paint as P
from paint import hexc, mixc
from items import px, canvas, fill, volume, soft, floor_shadow, line, ell, poly, text, H, dk, lt, SERIF
from room_items import clip, plate, rope, blob, WOOD, WOOD_D, WOOD_L
from fest_items import ball, part, rect_part, leaf

IMGS, RECT = [], {}
LACQ, LACQ_R, GOLD = '#1a1412', '#8a1a14', '#d8b048'


def save(img, iid):
    out = img.resize((P.W, P.H), Image.LANCZOS)
    a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .88
    a[..., :3] += np.random.default_rng(sum(map(ord, iid))).normal(0, 3.5, a.shape[:2])[..., None]
    IMGS.append((iid, Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA'))); print(iid, P.W, P.H)


def paw(img, x, y, s, col, a=1.0):
    c = H(col)[:3] + (int(255 * a),)
    soft(img, lambda d: [d.ellipse([px(x - s * .55), px(y - s * .3), px(x + s * .55), px(y + s * .45)], fill=c)] +
         [d.ellipse([px(x + dx * s - s * .2), px(y + dy * s - s * .24), px(x + dx * s + s * .2), px(y + dy * s + s * .24)], fill=c)
          for dx, dy in ((-.62, -.52), (-.22, -.86), (.22, -.86), (.62, -.52))], .5)


def pumpkin(img, cx, base, w, h, col, seed, stem='#5a4a24', grooves=True):
    """Squat ribbed pumpkin: lobes painted back to front."""
    for i in (-2, 2, -1, 1, 0):
        lw = w * (.34 if abs(i) == 2 else .42 if abs(i) == 1 else .46); lh = h * (.86 if abs(i) == 2 else .95 if abs(i) == 1 else 1)
        x = cx + i * w * .17
        ball(img, x, base - lh / 2, lw / 2, lh / 2, mixc(H(col), (0, 0, 0, 255), .12 * abs(i)), seed + i, spec=.22, k=.5, rim=.5)
    if grooves:
        for i in (-1.5, -.5, .5, 1.5):
            x = cx + i * w * .17
            line(img, [(x, base - h * .9), (x + i * 2, base - h * .5), (x, base - h * .08)], dk(H(col), .45), 1.6)
    rect_part(img, stem, seed + 9, (cx - 5, base - h - 12, cx + 5, base - h + 6), k=.3)


def carved_face(img, cx, cy, s, hot='#ffd27a'):
    for sx in (-1, 1):
        poly(img, [(cx + sx * s * .42, cy - s * .38), (cx + sx * s * .14, cy - s * .08), (cx + sx * s * .6, cy - s * .06)], '#3a1606')
        poly(img, [(cx + sx * s * .41, cy - s * .3), (cx + sx * s * .2, cy - s * .1), (cx + sx * s * .55, cy - s * .09)], hot)
    poly(img, [(cx - s * .1, cy + s * .02), (cx + s * .1, cy + s * .02), (cx, cy + s * .14)], hot)
    m = [(cx - s * .62, cy + s * .2), (cx - s * .4, cy + s * .3), (cx - s * .28, cy + s * .22), (cx - s * .1, cy + s * .32), (cx + s * .1, cy + s * .22), (cx + s * .28, cy + s * .32),
         (cx + s * .4, cy + s * .22), (cx + s * .62, cy + s * .2), (cx + s * .38, cy + s * .52), (cx - s * .38, cy + s * .52)]
    poly(img, m, '#3a1606'); poly(img, [(x * .92 + cx * .08, y * .9 + (cy + s * .35) * .1) for x, y in m], hot)
    soft(img, lambda d: d.ellipse([px(cx - s * .8), px(cy - s * .5), px(cx + s * .8), px(cy + s * .6)], fill=(255, 190, 90, 70)), 10)


# ───────────────────────────── 猫の日 Cat Day ─────────────────────────────
def catday():
    img = canvas(170, 120); floor_shadow(img, 85, 112, 78)                                   # paw stamps on washi
    part(img, '#efe6d2', 501, [(10, 92), (104, 74), (128, 108), (30, 116)], k=.2, rim=.1, scale=3)
    for k, (x, y) in enumerate(((34, 100), (56, 90), (78, 98), (98, 86))): paw(img, x, y, 7, '#b0282a', .85)
    fill(img, '#2a1a14', 502, ell=(112, 84, 160, 108), scale=3); fill(img, '#a8201e', 503, ell=(116, 82, 156, 100), scale=3, contrast=.6)
    volume(img, (112, 80, 160, 108), .4, .3, spec=.2)
    rect_part(img, '#c9a26a', 504, (122, 20, 142, 74), k=.5, spec=.2, stretch=(.4, 3))
    ball(img, 132, 20, 11, 8, '#d8b47a', 505, spec=.3)
    paw(img, 132, 66, 6, '#7a1a16', .9)
    save(img, 'hl_pawstamp')

    img = canvas(210, 130); floor_shadow(img, 105, 122, 96)                                  # cat-shaped cushion
    m = blob(img, [(16, 104), (20, 70), (60, 50), (120, 52), (160, 70), (176, 104), (110, 118), (50, 118)], hexc('#d8a468'), 511, scale=4, contrast=.8, k=.4)
    clip(img, m, lambda d: [d.line([(px(x), px(50)), (px(x - 8), px(120))], fill=(150, 90, 40, 120), width=px(5)) for x in range(36, 170, 22)])
    blob(img, [(150, 76), (152, 42), (186, 40), (200, 70), (192, 100), (160, 102)], hexc('#e0ae72'), 512, scale=4, contrast=.8, k=.45)
    for x0, x1 in ((154, 168), (182, 196)):
        poly(img, [(x0, 50), (x1, 50), ((x0 + x1) / 2 + (2 if x0 > 170 else -2), 24)], '#d8a468'); poly(img, [(x0 + 4, 48), (x1 - 4, 48), ((x0 + x1) / 2, 32)], '#e7a3a8')
    d = ImageDraw.Draw(img)
    for ex in (166, 186): d.arc([px(ex - 7), px(64), px(ex + 7), px(74)], 20, 160, fill=H('#3a2416'), width=px(2))
    poly(img, [(173, 78), (179, 78), (176, 82)], '#c87a7a')
    for s in (-1, 1): line(img, [(176 + s * 10, 82), (176 + s * 30, 78 + s * 0)], '#f2e8d8', .8)
    line(img, [(22, 100), (10, 80), (14, 60), (30, 52)], '#c8945a', 9); line(img, [(26, 54), (32, 52)], '#f2e6d0', 9)
    save(img, 'hl_nekocushion')

    img = canvas(190, 120); plate(img, 95, 96, 176, '#ebe5d8', '#2a4a7a')                    # cat onigiri
    for k, (x, y) in enumerate(((62, 74), (128, 76))):
        for s in (-1, 1): poly(img, [(x + s * 26, y - 14), (x + s * 8, y - 28), (x + s * 26, y - 40)], '#eee8dc')
        ball(img, x, y, 32, 28, '#f2ede2', 521 + k, spec=.15, k=.3, rim=.25)
        clip(img, mask_round(img, x, y, 32, 28), lambda d, x=x, y=y: [d.rectangle([px(x - 34), px(y + 8), px(x + 34), px(y + 30)], fill=H('#1c2620'))])
        for s in (-1, 1): ell(img, (x + s * 11 - 3, y - 8, x + s * 11 + 3, y - 2), '#1a1a18'); soft(img, lambda d, x=x, y=y, s=s: d.ellipse([px(x + s * 18 - 5), px(y - 1), px(x + s * 18 + 5), px(y + 5)], fill=(230, 140, 150, 160)), 1.5)
        poly(img, [(x - 2, y + 1), (x + 2, y + 1), (x, y + 3)], '#b07070')
        for s in (-1, 1): line(img, [(x + s * 6, y + 1), (x + s * 20, y - 2)], '#3a3a36', .6)
    save(img, 'hl_nekoonigiri')

    img = canvas(220, 150); floor_shadow(img, 110, 142, 100)                                 # reward: Musya's throne
    part(img, LACQ, 531, [(26, 140), (194, 140), (200, 112), (20, 112)], k=.3, spec=.15)
    line(img, [(20, 112), (200, 112)], GOLD, 2)
    for x in (34, 186): rect_part(img, LACQ, 532 + x, (x - 6, 112, x + 6, 142), k=.3)
    m = blob(img, [(14, 104), (60, 70), (160, 70), (206, 104), (160, 122), (60, 122)], hexc('#a82a2a'), 533, scale=4, contrast=.7, k=.45, spec=.15)
    clip(img, m, lambda d: [d.line([(px(60), px(96)), (px(160), px(96))], fill=H('#c8963a'), width=px(1.5)), d.line([(px(110), px(74)), (px(110), px(120))], fill=H('#c8963a'), width=px(1.5))])
    paw(img, 110, 96, 9, '#e8c060', .95)
    for x, y in ((14, 104), (206, 104), (60, 72), (160, 72)):
        line(img, [(x, y), (x, y + 18)], GOLD, 2.5); part(img, '#d8a838', 534 + x, [(x - 5, y + 16), (x + 5, y + 16), (x + 7, y + 34), (x - 7, y + 34)], k=.3)
    save(img, 'hl_r_throne')


def mask_round(img, x, y, rx, ry):
    from items import mask_poly
    return mask_poly(img, ell=(x - rx, y - ry, x + rx, y + ry))


# ───────────────────────────── ハロウィン Halloween ─────────────────────────────
def halloween():
    img = canvas(160, 140); floor_shadow(img, 80, 132, 72)                                   # jack-o'-lantern
    soft(img, lambda d: d.ellipse([px(10), px(20), px(150), px(140)], fill=(255, 150, 60, 40)), 16)
    pumpkin(img, 80, 130, 140, 98, '#c06a24', 601)
    carved_face(img, 80, 86, 52)
    save(img, 'hl_jack')

    img = canvas(250, 200); floor_shadow(img, 125, 192, 110)                                 # uncarved, for the carving panel
    pumpkin(img, 125, 190, 220, 156, '#c06a24', 611)
    save(img, 'hl_kab0')

    img = canvas(170, 130); floor_shadow(img, 85, 124, 76)                                   # basket of candies
    line(img, [(28, 70), (40, 20), (85, 6), (130, 20), (142, 70)], '#8a6038', 4)
    rr = random.Random(3)
    for k in range(9):
        x, y = 38 + k * 12 + rr.uniform(-4, 4), 62 + rr.uniform(-8, 6); c = ['#b8322a', '#e0b040', '#6a3a8a', '#2f6b3a', '#d86a2a', '#e8e0d0'][k % 6]
        poly(img, [(x - 14, y - 6), (x - 7, y), (x - 14, y + 6)], c); poly(img, [(x + 14, y - 6), (x + 7, y), (x + 14, y + 6)], c)
        ball(img, x, y, 9, 7, c, 621 + k, spec=.45, k=.4)
    m = part(img, WOOD_L, 630, [(18, 66), (152, 66), (138, 122), (32, 122)], k=.4, stretch=(1, 1))
    clip(img, m, lambda d: [d.line([(px(x), px(66)), (px(x + 18), px(122))], fill=(80, 50, 24, 150), width=px(1.4)) for x in range(4, 160, 10)] +
         [d.line([(px(x + 18), px(66)), (px(x), px(122))], fill=(80, 50, 24, 110), width=px(1.4)) for x in range(4, 160, 10)])
    line(img, [(18, 66), (152, 66)], '#6a4a28', 3)
    for x, c in ((60, '#e0b040'), (104, '#b8322a')):
        for k in range(5): a = k / 5 * math.tau; poly(img, [(x + math.cos(a) * 6, 60 + math.sin(a) * 6), (x + math.cos(a + .6) * 3, 60 + math.sin(a + .6) * 3), (x + math.cos(a - .6) * 3, 60 + math.sin(a - .6) * 3)], c)
    save(img, 'hl_candy')

    img = canvas(140, 210); floor_shadow(img, 70, 204, 52)                                    # sheet-ghost costume on a stand
    rect_part(img, WOOD_D, 640, (40, 194, 100, 206), k=.3); rect_part(img, WOOD, 641, (66, 40, 74, 196), k=.3)
    m = blob(img, [(70, 22), (104, 40), (112, 100), (124, 168), (104, 160), (88, 174), (70, 160), (52, 174), (36, 160), (16, 168), (28, 100), (36, 40)],
             hexc('#e8e4dc'), 642, scale=5, contrast=.6, k=.45, rim=.3)
    clip(img, m, lambda d: [d.line([(px(x), px(60)), (px(x + (x - 70) * .3), px(170))], fill=(150, 150, 160, 70), width=px(2)) for x in (46, 60, 84, 98)])
    for x in (56, 84): ell(img, (x - 8, 62, x + 8, 82), '#1a1414')
    poly(img, [(62, 96), (78, 96), (74, 112), (66, 112)], '#b84a4a')
    save(img, 'hl_obakecos')

    img = canvas(180, 180); floor_shadow(img, 90, 172, 80)                                    # reward: kabocha yōkai
    pumpkin(img, 90, 170, 160, 120, '#2e4a2c', 651, stem='#6a5a2a')
    rr = random.Random(5)
    for _ in range(30): x, y = rr.uniform(30, 150), rr.uniform(70, 160); ell(img, (x - 1.2, y - 1.2, x + 1.2, y + 1.2), '#6a8a5a')
    ball(img, 90, 98, 24, 22, '#f2ecd8', 652, spec=.3, k=.3); ball(img, 94, 100, 11, 12, '#8a2a1a', 653, spec=.2, k=.3); ell(img, (90, 96, 98, 104), '#140c0a')
    ell(img, (88, 92, 92, 96), '#ffffff')
    poly(img, [(60, 128), (120, 128), (106, 142), (74, 142)], '#2a0e08')
    blob(img, [(82, 134), (100, 134), (104, 160), (96, 176), (86, 170), (80, 152)], hexc('#c8404a'), 654, scale=3, k=.3, spec=.2)
    leaf(img, 94, 52, 30, 9, -.4, '#3a5a2a', 655)
    save(img, 'hl_r_kabotan')


# ───────────────────────────── クリスマス Christmas ─────────────────────────────
BULBS = ['#ffe8a8', '#e04a3a', '#3a8a4a', '#e8b030', '#4a7ac8']


def xmas():
    img = canvas(280, 120)                                                                    # string lights (hangs)
    pts = [(x, 14 + 26 * math.sin(math.pi * ((x - 8) % 132) / 132) ** 1.2) for x in range(8, 274, 4)]
    line(img, pts, '#1a2016', 1.6)
    for k, (x, y) in enumerate(pts[::4]):
        c = BULBS[k % 5]; soft(img, lambda d, x=x, y=y, c=c: d.ellipse([px(x - 12), px(y - 4), px(x + 12), px(y + 22)], fill=H(c)[:3] + (90,)), 5)
        rect_part(img, '#2a2a22', 701 + k, (x - 2.5, y, x + 2.5, y + 5), k=.2); ball(img, x, y + 11, 4.5, 7, c, 720 + k, spec=.6, k=.2, rim=.2)
    save(img, 'hl_lights')

    img = canvas(160, 140); floor_shadow(img, 80, 132, 74)                                   # strawberry shortcake
    plate(img, 80, 124, 150, '#ece6da', '#9a8a6a')
    part(img, '#f4eee2', 731, [(28, 66), (132, 66), (132, 118), (28, 118)], k=.35, rim=.2, scale=3)
    line(img, [(28, 92), (132, 92)], '#e8b0b0', 3)
    for x in range(36, 128, 18): ell(img, (x - 4, 88, x + 4, 96), '#d84a4a')
    fill(img, '#fbf7ee', 732, ell=(28, 54, 132, 78), scale=3, contrast=.3)
    for k, x in enumerate(range(34, 130, 16)): ball(img, x, 64 + (k % 2) * 4, 7, 6, '#fbf8f0', 733 + k, spec=.3, k=.3)
    for k, (x, y) in enumerate(((48, 52), (80, 48), (112, 52), (64, 60), (96, 60))):
        part(img, '#c8202a', 740 + k, [(x - 8, y - 6), (x + 8, y - 6), (x + 6, y + 4), (x, y + 10), (x - 6, y + 4)], k=.35, spec=.4, scale=2)
        for s in (-1, 0, 1): line(img, [(x, y - 6), (x + s * 5, y - 11)], '#3a6a2a', 1.6)
    part(img, '#5a3420', 750, [(64, 36), (100, 32), (102, 46), (66, 50)], k=.3, spec=.2); line(img, [(70, 42), (96, 39)], '#f0e6d0', .9)
    save(img, 'hl_cake')

    img = canvas(160, 190); floor_shadow(img, 80, 184, 56)                                   # poinsettia
    part(img, '#a82a24', 760, [(46, 128), (114, 128), (104, 184), (56, 184)], k=.45, spec=.2)
    line(img, [(46, 136), (114, 136)], GOLD, 2.4)
    for k in range(7): a = -math.pi * (.05 + k * .15); leaf(img, 80, 112, 52, 14, a, '#2e5a2c', 761 + k)
    for k in range(9): a = k / 9 * math.tau + .2; leaf(img, 80, 80, 46, 14, a, '#c0242a', 770 + k)
    for k in range(6): a = k / 6 * math.tau; leaf(img, 80, 80, 26, 9, a + .5, '#d83a3a', 780 + k, vein=False)
    for k in range(7): a = k / 7 * math.tau; ball(img, 80 + math.cos(a) * 5, 80 + math.sin(a) * 5, 2.6, 2.6, '#e8c040', 790 + k, spec=.4)
    save(img, 'hl_poinsettia')

    img = canvas(140, 140); floor_shadow(img, 70, 134, 64)                                   # present
    part(img, '#a8242a', 801, [(16, 70), (104, 70), (104, 132), (16, 132)], k=.35, spec=.1)
    part(img, '#7a1a1e', 802, [(104, 70), (128, 54), (128, 114), (104, 132)], k=.3)
    part(img, '#c43a3a', 803, [(16, 70), (40, 54), (128, 54), (104, 70)], k=.25)
    rect_part(img, GOLD, 804, (54, 70, 66, 132), k=.3, spec=.3); poly(img, [(104, 92), (128, 76), (128, 86), (104, 102)], '#b89038')
    poly(img, [(54, 70), (66, 70), (90, 54), (78, 54)], '#e8c060'); poly(img, [(28, 62), (36, 58), (116, 58), (108, 62)], '#e8c060')
    for s in (-1, 1): ball(img, 72 + s * 16, 50, 16, 9, GOLD, 805 + s, spec=.4, k=.4)
    ball(img, 72, 54, 6, 5, '#c89838', 807, spec=.3)
    for s in (-1, 1): line(img, [(72, 56), (72 + s * 10, 74)], '#d8b048', 3)
    save(img, 'hl_present')

    img = canvas(160, 180); floor_shadow(img, 80, 174, 64)                                   # reward: snow globe
    part(img, WOOD_D, 811, [(30, 176), (130, 176), (118, 140), (42, 140)], k=.45, spec=.15)
    line(img, [(42, 146), (118, 146)], GOLD, 2)
    soft(img, lambda d: d.ellipse([px(20), px(16), px(140), px(146)], fill=(150, 190, 220, 60)), 1)
    fill(img, '#f2f2f4', 812, ell=(30, 112, 130, 146), scale=3, contrast=.3)
    part(img, '#4a3428', 813, [(60, 124), (100, 124), (100, 96), (60, 96)], k=.3)
    poly(img, [(52, 98), (80, 74), (108, 98)], '#f2f2f4'); poly(img, [(56, 98), (80, 80), (104, 98)], '#3a2a24')
    poly(img, [(54, 96), (80, 76), (106, 96), (100, 92), (80, 80), (60, 92)], '#f4f4f6')
    rect_part(img, '#ffd27a', 814, (72, 104, 88, 116), k=.1); soft(img, lambda d: d.ellipse([px(64), px(98), px(96), px(122)], fill=(255, 210, 120, 90)), 5)
    rr = random.Random(7)
    for _ in range(26): x, y = rr.uniform(34, 126), rr.uniform(30, 110); ell(img, (x - 1.6, y - 1.6, x + 1.6, y + 1.6), '#ffffff')
    d = ImageDraw.Draw(img); d.arc([px(22), px(18), px(138), px(144)], 200, 280, fill=(255, 255, 255, 170), width=px(2.4)); d.ellipse([px(20), px(16), px(140), px(146)], outline=(200, 220, 235, 120), width=px(1.2))
    save(img, 'hl_r_globe')


# ───────────────────────────── 大晦日 Omisoka ─────────────────────────────
def soba_bowl(img, cx, cy, w, seed):
    fill(img, '#1a1210', seed, ell=(cx - w / 2, cy - w * .2, cx + w / 2, cy + w * .44), scale=3); volume(img, (cx - w / 2, cy - w * .2, cx + w / 2, cy + w * .44), .4, .4, spec=.2)
    fill(img, '#8a1a14', seed + 1, ell=(cx - w / 2, cy - w * .22, cx + w / 2, cy + w * .16), scale=3)
    m = fill(img, '#5a3418', seed + 2, ell=(cx - w * .44, cy - w * .17, cx + w * .44, cy + w * .12), scale=3)
    rr = random.Random(seed)
    clip(img, m, lambda d: [d.arc([px(cx - w * .4 + rr.uniform(-6, 6)), px(cy - w * .14 + rr.uniform(-4, 4)), px(cx + w * .2 + rr.uniform(-6, 6)), px(cy + w * .1 + rr.uniform(-3, 3))],
                                  rr.uniform(0, 180), rr.uniform(200, 360), fill=(150, 130, 108, 255), width=px(1.6)) for _ in range(26)])
    part(img, '#d8a040', seed + 3, [(cx + w * .02, cy - w * .1), (cx + w * .36, cy - w * .04), (cx + w * .34, cy + w * .04), (cx + w * .04, cy - w * .02)], k=.3, scale=2)
    poly(img, [(cx + w * .34, cy - w * .04), (cx + w * .44, cy - w * .1), (cx + w * .42, cy + w * .02)], '#d84a2a')
    for k in range(9): x, y = cx - w * .3 + rr.uniform(0, w * .26), cy - w * .08 + rr.uniform(0, w * .1); ell(img, (x - 2.4, y - 1.6, x + 2.4, y + 1.6), '#7aa04a')
    for k, x in enumerate((cx - w * .16, cx - w * .02)): ell(img, (x - 7, cy + w * .02, x + 7, cy + w * .08), '#f2e6e0'); line(img, [(x - 6, cy + w * .04), (x + 6, cy + w * .04)], '#e08a9a', 1.4)


def omisoka():
    img = canvas(190, 120); floor_shadow(img, 95, 114, 86)                                   # soba on a tray
    part(img, LACQ_R, 901, [(10, 108), (180, 108), (166, 66), (24, 66)], k=.3, spec=.15)
    line(img, [(24, 66), (166, 66)], '#3a0e0a', 2)
    soba_bowl(img, 86, 74, 110, 902)
    for k in range(2): line(img, [(150 + k * 6, 102), (170 + k * 4, 62)], '#c8a070', 2.2)
    save(img, 'hl_sobaset')

    img = canvas(150, 92)                                                                    # the dish (pantry / cooking)
    soba_bowl(img, 75, 34, 138, 911)
    save(img, 'ds_hl_soba')

    img = canvas(110, 240); floor_shadow(img, 55, 234, 40)                                   # broom
    rr = random.Random(9); pts = [(30, 236), (80, 236), (66, 160), (44, 160)]
    m = part(img, '#b8a060', 921, pts, k=.35, stretch=(.2, 3))
    clip(img, m, lambda d: [d.line([(px(55 + (x - 55) * .3), px(160)), (px(x), px(236))], fill=(110, 90, 40, 160), width=px(1)) for x in range(30, 82, 3)])
    rope(img, [(44, 172), (66, 172)], '#6a3a20', 4); rope(img, [(42, 182), (68, 182)], '#6a3a20', 3)
    rect_part(img, '#b8a868', 922, (51, 10, 59, 166), k=.4, stretch=(.2, 3))
    for y in (40, 90, 140): line(img, [(50, y), (60, y)], '#7a6a38', 1.6)
    save(img, 'hl_broom')

    img = canvas(170, 110); floor_shadow(img, 85, 104, 78)                                   # basket of mikan
    fill(img, '#8a6a3a', 931, ell=(12, 54, 158, 104), scale=3, contrast=.6); volume(img, (12, 54, 158, 104), .4, .4)
    for k, (x, y) in enumerate(((50, 62), (84, 56), (118, 62), (66, 76), (102, 76), (84, 70))):
        ball(img, x, y, 19, 16, '#e8862a', 932 + k, spec=.35, k=.45)
        ell(img, (x - 2, y - 15, x + 2, y - 12), '#4a5a24')
    leaf(img, 86, 56, 26, 8, -.6, '#2e5a2c', 940); leaf(img, 60, 48, 22, 7, -2.6, '#2e5a2c', 941)
    save(img, 'hl_mikan')

    img = canvas(210, 250); floor_shadow(img, 105, 244, 96)                                  # reward: temple bell in snow
    fill(img, '#eef0f2', 951, ell=(14, 228, 196, 250), scale=3, contrast=.3)
    for x in (30, 180): rect_part(img, WOOD_D, 952 + x, (x - 7, 40, x + 7, 240), k=.4, stretch=(.2, 3))
    part(img, '#2a201a', 955, [(4, 46), (206, 46), (180, 20), (30, 20)], k=.3)
    part(img, '#f2f2f4', 956, [(4, 40), (206, 40), (184, 16), (26, 16)], k=.25, rim=.1, scale=3)
    rect_part(img, WOOD_D, 957, (20, 52, 190, 60), k=.3)
    m = part(img, '#5e5236', 958, [(76, 70), (134, 70), (140, 92), (142, 180), (150, 196), (60, 196), (68, 180), (70, 92)], k=.55, rim=.45, spec=.2)
    clip(img, m, lambda d: [d.line([(0, px(y)), (px(210), px(y))], fill=(40, 34, 20, 200), width=px(2)) for y in (88, 150, 178)] +
         [d.line([(px(105), px(88)), (px(105), px(150))], fill=(40, 34, 20, 160), width=px(1.5))])
    for r in range(3):
        for c in range(3):
            for s in (-1, 1): ball(img, 105 + s * (10 + c * 9), 98 + r * 10, 2.6, 2.4, '#8a7a50', 960 + r * 7 + c, spec=.4)
    rect_part(img, '#4a4028', 970, (98, 60, 112, 72), k=.3)
    soft(img, lambda d: d.ellipse([px(70), px(62), px(140), px(76)], fill=(250, 250, 255, 200)), 1.5)
    rope(img, [(36, 60), (40, 132)], '#c8b07a', 2); rope(img, [(52, 60), (56, 132)], '#c8b07a', 2)
    rect_part(img, '#a88a5a', 971, (20, 128, 70, 140), k=.4, stretch=(3, .4))
    save(img, 'hl_r_bell')


def pack():
    lst = sorted(IMGS, key=lambda t: -t[1].height); W = 1100; x = y = rowh = 0; pos = {}
    for iid, im in lst:
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[iid] = (x, y); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for iid, im in lst: at.paste(im, pos[iid]); RECT[iid] = [pos[iid][0], pos[iid][1], im.width, im.height]
    at.save(f'{ROOT}/assets/items/atlas_hl.webp', 'WEBP', quality=88, alpha_quality=90, method=6)
    at.save(f'{HERE}/out/atlas_hl_preview.png')
    print('atlas', at.size, os.path.getsize(f'{ROOT}/assets/items/atlas_hl.webp') // 1024, 'KB')
    json.dump({'w': W, 'h': at.height, 'r': RECT}, open(f'{HERE}/out/hl.json', 'w'), separators=(',', ':'))
    print(json.dumps({'w': W, 'h': at.height, 'r': RECT}, separators=(',', ':')))


if __name__ == '__main__':
    catday(); halloween(); xmas(); omisoka(); pack()
