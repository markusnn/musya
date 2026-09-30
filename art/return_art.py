#!/usr/bin/env python3
"""«Пока тебя не было» + «Фонарики дней»: Musya's finds, rare-guest gifts, the seven day lanterns and four rare seasonal guests.
Same brush toolkit as items.py / story_art.py / guests_art.py.
Usage (from the site root): python3 art/return_art.py
  → assets/items/atlas_fd.webp (finds), assets/items/atlas_rg.webp (gifts + lantern sprites), assets/mon/m_rg_*.webp
  → prints the JSON rows that feat/return.js and feat/lanterns.js embed."""
import json, math, os, random, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.argv = [sys.argv[0], os.path.join(ROOT, 'assets/mon')]          # monsters.py / items.py read their outdir at import
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc
import monsters as M
from items import px, canvas, fill, volume, soft, floor_shadow, line, ell, poly, text, dk, lt, H, SERIF
from story_art import cr, shape, clipped, mask_of, poly_s, folds, hair_texture, flower
from guests_art import tube, fur_ticks, stroke
from monsters import hair

OUT_I = os.path.join(ROOT, 'assets/items'); M.OUT = os.path.join(ROOT, 'assets/mon')
PREV = os.path.join(ROOT, 'art/out'); os.makedirs(PREV, exist_ok=True)
BLACK, WHITE = (0, 0, 0, 255), (255, 255, 255, 255)
ATL = {'fd': [], 'rg': []}; ROWS = []


def keep(img, iid, atlas, name=None, anchor='b', glow=None, sat=.9):
    out = img.resize((P.W, P.H), Image.LANCZOS)
    a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * sat
    a[..., :3] += np.random.default_rng(sum(map(ord, iid))).normal(0, 3.2, a.shape[:2])[..., None]
    ATL[atlas].append((iid, Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')))
    if name: ROWS.append({'id': iid, 'n': name, 'w': P.W, 'h': P.H, 'a': anchor, **({'glow': glow} if glow else {})})


def pack(key, W=1024):
    lst = sorted(ATL[key], key=lambda t: -t[1].height); x = y = rowh = 0; pos = {}
    for iid, im in lst:
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[iid] = (x, y); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for iid, im in lst: at.paste(im, pos[iid])
    at.save(f'{OUT_I}/atlas_{key}.webp', 'WEBP', quality=87, alpha_quality=90, method=6)
    bg = Image.new('RGBA', at.size, (52, 60, 56, 255)); bg.alpha_composite(at); bg.convert('RGB').save(f'{PREV}/atlas_{key}.jpg')
    print('atlas', key, at.size)
    return {iid: [pos[iid][0], pos[iid][1], im.width, im.height] for iid, im in lst}, list(at.size)


def oval(cx, cy, rx, ry, n=24, sq=0):
    return [(cx + math.cos(a) * rx * (1 + sq * math.cos(a) ** 2 * 0), cy + math.sin(a) * ry) for a in np.linspace(0, math.tau, n, endpoint=False)]


def glowdot(img, x, y, r, col, a=200, blur=None):
    soft(img, lambda d: d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=col[:3] + (a,)), blur or r * .5)


# ───────────────────────── Musya's finds ─────────────────────────
def f_crow():
    img = canvas(80, 180)
    vane = [(40, 10), (54, 40), (60, 90), (54, 140), (44, 170), (36, 168), (26, 130), (22, 80), (28, 36)]
    m = shape(img, hexc('#1c1f2a'), 1, vane, scale=5, stretch=(1, 4), contrast=1.2, dk=.4, lt=.25, k=.5, rim=.3, spec=.25)
    clipped(img, m, lambda d, l: [d.line([(px(40), px(20 + i * 5)), (px(40 + s * 26), px(10 + i * 5 + 16))], fill=(70, 80, 110, 90), width=px(1)) for i in range(30) for s in (-1, 1)])
    clipped(img, m, lambda d, l: d.line([(px(44), px(60)), (px(52), px(110))], fill=(90, 110, 150, 120), width=px(5)), .7)
    line(img, [(40, 12), (41, 90), (40, 176)], '#c8c4b4', 1.6)
    floor_shadow(img, 40, 172, 24, 70); keep(img, 'fd_crow', 'fd', 'Вороново перо')


def f_pebble():
    img = canvas(120, 80); floor_shadow(img, 60, 70, 48)
    m = shape(img, hexc('#77807c'), 2, oval(60, 44, 50, 27), scale=6, contrast=1.1, dk=.4, lt=.25, k=.7, rim=.45, spec=.35)
    clipped(img, m, lambda d, l: d.line([(px(18), px(52)), (px(60), px(38)), (px(104), px(46))], fill=(222, 218, 205, 170), width=px(3)))
    rnd = random.Random(2); clipped(img, m, lambda d, l: [d.point((px(rnd.uniform(12, 108)), px(rnd.uniform(20, 70))), fill=(40, 40, 38, 200)) for _ in range(90)])
    keep(img, 'fd_pebble', 'fd', 'Гладкий речной камешек')


def f_button():
    img = canvas(90, 70); floor_shadow(img, 45, 62, 36)
    shape(img, hexc('#6a4f22'), 3, oval(45, 40, 36, 24), scale=4, contrast=1.1, k=.6, rim=.5)
    m = shape(img, hexc('#b8903e'), 4, oval(45, 37, 32, 20), scale=4, contrast=1.1, dk=.4, lt=.3, k=.7, rim=.4, spec=.45)
    clipped(img, m, lambda d, l: [d.ellipse([px(45 + math.cos(a) * 9 - 5), px(37 + math.sin(a) * 6 - 3.5), px(45 + math.cos(a) * 9 + 5), px(37 + math.sin(a) * 6 + 3.5)], fill=(120, 86, 30, 220)) for a in np.linspace(-math.pi / 2, 1.5 * math.pi, 5, endpoint=False)])
    clipped(img, m, lambda d, l: d.ellipse([px(42), px(35), px(48), px(39)], fill=(90, 60, 20, 255)))
    keep(img, 'fd_button', 'fd', 'Старая латунная пуговица')


def f_mon():
    img = canvas(100, 100); floor_shadow(img, 50, 94, 36)
    m = shape(img, hexc('#8a6a3a'), 5, oval(50, 50, 42, 42, 32), scale=5, contrast=1.2, dk=.45, lt=.25, k=.6, rim=.35, spec=.2)
    rnd = random.Random(5)
    clipped(img, m, lambda d, l: [d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=(70, 120, 100, 130)) for x, y, r in [(rnd.uniform(10, 90), rnd.uniform(10, 90), rnd.uniform(3, 9)) for _ in range(14)]])
    d = ImageDraw.Draw(img); d.ellipse([px(12), px(12), px(88), px(88)], outline=(60, 44, 20, 200), width=px(2))
    d.rectangle([px(40), px(40), px(60), px(60)], fill=(0, 0, 0, 0))
    img.paste((0, 0, 0, 0), (px(41), px(41), px(59), px(59)))
    d.rectangle([px(38), px(38), px(62), px(62)], outline=(60, 44, 20, 220), width=px(2))
    for ch, x, y in (('寛', 50, 26), ('永', 50, 75), ('通', 74, 50), ('寳', 26, 50)): text(img, ch, x, y, 17, '#4a3414', SERIF)
    keep(img, 'fd_mon', 'fd', 'Старинная монетка мон')


def f_tsuru():
    img = canvas(140, 110); floor_shadow(img, 70, 102, 46)
    red, red_d, wh = hexc('#c23a32'), hexc('#8a2420'), hexc('#e9dfcc')
    poly_s(ImageDraw.Draw(img), [(70, 60), (126, 20), (96, 70)], red_d, 1)          # far wing
    fill(img, red, 6, poly=[(34, 72), (70, 56), (106, 72), (70, 100)], scale=4, contrast=.8)   # body
    fill(img, red_d, 7, poly=[(70, 56), (106, 72), (70, 100)], scale=4, contrast=.8)
    fill(img, red, 8, poly=[(70, 62), (14, 18), (58, 74)], scale=4, contrast=.8)       # near wing
    fill(img, lt(red, .15), 9, poly=[(40, 74), (22, 30), (16, 58)], scale=4)            # neck up
    fill(img, red_d, 10, poly=[(22, 30), (12, 36), (18, 40)], scale=3)                  # head
    fill(img, red, 11, poly=[(100, 72), (128, 50), (112, 76)], scale=3)                 # tail
    rnd = random.Random(12); d = ImageDraw.Draw(img)
    for _ in range(30): x, y = rnd.uniform(30, 110), rnd.uniform(30, 96); d.ellipse([px(x - 1.2), px(y - 1.2), px(x + 1.2), px(y + 1.2)], fill=wh[:3] + (150,))
    line(img, [(70, 56), (70, 100)], dk(red, .5), .8); keep(img, 'fd_tsuru', 'fd', 'Бумажный журавлик')


def f_momiji():
    img = canvas(130, 130); floor_shadow(img, 64, 118, 44)
    cx, cy = 64, 70; pts = []
    for i in range(7):
        a = -math.pi / 2 + (i - 3) * .52; L = [44, 50, 56, 60, 56, 50, 44][i]
        for da, r in ((-.2, .38), (-.08, .8), (0, 1), (.08, .8), (.2, .38)): pts.append((cx + math.cos(a + da) * L * r, cy + math.sin(a + da) * L * r * .95))
    m = shape(img, hexc('#c04a24'), 13, pts, scale=6, contrast=1.1, dk=.35, lt=.3, k=.5, rim=.3, smooth=False, feather=.5)
    clipped(img, m, lambda d, l: [d.ellipse([px(30), px(20), px(100), px(80)], fill=(220, 150, 50, 120))], .8)
    for i in range(7):
        a = -math.pi / 2 + (i - 3) * .52; line(img, [(cx, cy + 6), (cx + math.cos(a) * 46, cy + math.sin(a) * 44)], '#7a2a14', 1.2)
    line(img, [(cx, cy + 4), (cx + 4, cy + 30), (cx + 12, cy + 44)], '#6a3a1a', 2)
    keep(img, 'fd_momiji', 'fd', 'Кленовый лист')


def f_cone():
    img = canvas(90, 120); floor_shadow(img, 45, 112, 34)
    m = shape(img, hexc('#6e4a2a'), 14, [(45, 8), (66, 30), (74, 64), (66, 96), (45, 112), (24, 96), (16, 64), (24, 30)], scale=5, k=.6, rim=.4)
    def scales(d, l):
        for r in range(10):
            y = 16 + r * 10; n = 5
            for c in range(n):
                x = 18 + c * 13 + (r % 2) * 6.5
                d.polygon([(px(x), px(y)), (px(x + 7), px(y + 6)), (px(x), px(y + 12)), (px(x - 7), px(y + 6))], fill=(146, 104, 62, 220), outline=(50, 30, 16, 230))
    clipped(img, m, scales); volume(img, (16, 8, 74, 112), .6, .35)
    keep(img, 'fd_cone', 'fd', 'Сосновая шишка')


def f_acorn():
    img = canvas(80, 100); floor_shadow(img, 40, 94, 28)
    shape(img, hexc('#a0662c'), 15, [(40, 36), (60, 44), (66, 66), (56, 88), (40, 94), (24, 88), (14, 66), (20, 44)], scale=5, contrast=.8, k=.7, rim=.4, spec=.45)
    cap = shape(img, hexc('#6a5236'), 16, [(10, 44), (22, 24), (40, 18), (58, 24), (70, 44), (56, 50), (40, 52), (24, 50)], scale=3, contrast=1.4, k=.5, rim=.3)
    rnd = random.Random(16); clipped(img, cap, lambda d, l: [d.arc([px(x - 4), px(y - 3), px(x + 4), px(y + 3)], 20, 160, fill=(40, 30, 18, 220), width=px(1.2)) for x, y in [(rnd.uniform(12, 68), rnd.uniform(22, 50)) for _ in range(40)]])
    line(img, [(40, 20), (42, 10), (48, 4)], '#4a3622', 2.4); keep(img, 'fd_acorn', 'fd', 'Желудь')


def f_shard():
    img = canvas(120, 90); floor_shadow(img, 60, 80, 46)
    pts = [(14, 50), (34, 18), (70, 12), (104, 30), (96, 62), (58, 78), (26, 72)]
    m = shape(img, hexc('#e6e4dc'), 17, pts, scale=6, contrast=.4, dk=.15, lt=.1, k=.5, rim=.2, spec=.4, smooth=False, feather=.4)
    def pat(d, l):
        blue = (40, 70, 140, 230)
        for r in (14, 24, 34): d.arc([px(50 - r), px(50 - r), px(50 + r), px(50 + r)], 180, 360, fill=blue, width=px(2.2))
        d.line([(px(20), px(62)), (px(100), px(56))], fill=blue, width=px(3))
        for k in range(4): x = 70 + k * 7; d.ellipse([px(x), px(24 + k * 3), px(x + 6), px(30 + k * 3)], fill=blue)
    clipped(img, m, pat)
    line(img, [(14, 50), (26, 72), (58, 78)], '#b8b0a0', 1.4)
    soft(img, lambda d: d.line([(px(40), px(22)), (px(72), px(18))], fill=(255, 255, 255, 200), width=px(3)), 1)
    keep(img, 'fd_shard', 'fd', 'Осколок синей глазури')


def f_bell():
    img = canvas(84, 104); floor_shadow(img, 42, 98, 30)
    line(img, [(42, 4), (34, 10), (42, 18), (50, 10), (42, 4)], '#6a5028', 3)
    m = shape(img, hexc('#8a6a34'), 18, [(42, 18), (56, 24), (62, 50), (70, 84), (74, 94), (10, 94), (14, 84), (22, 50), (28, 24)], scale=5, contrast=1.2, dk=.45, lt=.3, k=.7, rim=.35, spec=.35)
    clipped(img, m, lambda d, l: [d.line([(px(10), px(y)), (px(74), px(y))], fill=(70, 50, 20, 200), width=px(2)) for y in (40, 78, 86)])
    clipped(img, m, lambda d, l: [d.ellipse([px(24 + c * 9), px(52), px(30 + c * 9), px(58)], fill=(160, 130, 70, 230)) for c in range(4)])
    ell(img, (14, 90, 70, 98), (30, 22, 12, 255)); keep(img, 'fd_bell', 'fd', 'Колокольчик без язычка')


def f_thread():
    img = canvas(120, 90); floor_shadow(img, 60, 80, 46); rnd = random.Random(19)
    for k in range(26):
        cx, cy = 58 + rnd.uniform(-10, 10), 48 + rnd.uniform(-6, 6); rx, ry = rnd.uniform(18, 34), rnd.uniform(12, 24); a0 = rnd.uniform(0, 6)
        pts = [(cx + math.cos(a0 + t) * rx, cy + math.sin(a0 + t) * ry) for t in np.linspace(0, math.pi * 1.6, 14)]
        col = mixc(hexc('#b8262a'), hexc('#e0484a'), rnd.random()); line(img, pts, col, 1.6)
    line(img, [(84, 60), (100, 70), (108, 64), (116, 76)], '#c83034', 1.8)
    volume(img, (20, 20, 100, 80), .5, .3); keep(img, 'fd_thread', 'fd', 'Моток красной нити')


def f_shell():
    img = canvas(120, 96); floor_shadow(img, 60, 88, 46)
    outer = [(10, 60), (22, 26), (60, 12), (98, 26), (110, 60), (96, 80), (60, 86), (24, 80)]
    shape(img, hexc('#b89a78'), 20, outer, scale=5, contrast=1, k=.6, rim=.35)
    inner = shape(img, hexc('#f0e6cc'), 21, [(18, 58), (28, 30), (60, 20), (92, 30), (102, 58), (90, 74), (60, 80), (30, 74)], scale=5, contrast=.5, dk=.2, lt=.1, k=.3, rim=.2)
    def paint_in(d, l):
        d.polygon([(px(20), px(60)), (px(50), px(40)), (px(70), px(52)), (px(100), px(38)), (px(100), px(78)), (px(20), px(78))], fill=(210, 170, 70, 200))
        for x, y in ((44, 34), (74, 30)): flower(d, x, y, 5, (220, 90, 110, 240))
        d.arc([px(30), px(40), px(90), px(90)], 200, 340, fill=(60, 90, 70, 200), width=px(2))
    clipped(img, inner, paint_in); keep(img, 'fd_shell', 'fd', 'Расписная ракушка')


def f_hotaru():
    img = canvas(76, 136); floor_shadow(img, 38, 130, 28)
    glowdot(img, 38, 84, 34, (190, 240, 110), 120, 14)
    body = [(28, 30), (48, 30), (50, 46), (64, 66), (66, 110), (58, 128), (18, 128), (10, 110), (12, 66), (26, 46)]
    m = shape(img, (170, 200, 190, 110), 22, body, scale=6, contrast=.3, dk=.1, lt=.2, k=.4, rim=-.3, spec=.5)
    glowdot(img, 40, 90, 10, (230, 255, 150), 240, 3); ell(img, (37, 87, 43, 93), (250, 255, 220, 255))
    line(img, [(36, 88), (30, 80)], (230, 255, 170, 150), 1)
    fill(img, '#9a7a4e', 23, poly=[(26, 14), (50, 14), (48, 32), (28, 32)], scale=3, contrast=1.2)
    soft(img, lambda d: d.line([(px(18), px(70)), (px(18), px(116))], fill=(255, 255, 255, 170), width=px(3)), 1)
    keep(img, 'fd_hotaru', 'fd', 'Светлячок в бутылочке', glow=[38, 88])


def f_semi():
    img = canvas(100, 84); floor_shadow(img, 50, 76, 38)
    amber = (196, 140, 60, 210)
    m = shape(img, amber, 24, [(20, 44), (34, 24), (62, 20), (86, 34), (90, 52), (70, 64), (36, 64)], scale=4, contrast=1, dk=.4, lt=.35, k=.5, rim=-.2, spec=.5)
    clipped(img, m, lambda d, l: [d.arc([px(30 + k * 10), px(22), px(44 + k * 10), px(64)], 250, 290, fill=(110, 70, 26, 220), width=px(1.6)) for k in range(5)])
    clipped(img, m, lambda d, l: d.line([(px(40), px(22)), (px(80), px(30))], fill=(250, 220, 170, 180), width=px(2)))
    for k in range(3):
        for s in (-1, 1): line(img, [(40 + k * 14, 58), (36 + k * 14 + s * 4, 70), (30 + k * 14 + s * 6, 76)], '#8a5a24', 1.4)
    ell(img, (22, 34, 32, 44), (120, 80, 40, 230)); keep(img, 'fd_semi', 'fd', 'Шкурка цикады')


def f_hane():
    img = canvas(86, 126); floor_shadow(img, 43, 120, 24)
    for a, col in ((-.45, '#d84a5a'), (-.15, '#f0e6d0'), (.15, '#3a8a5a'), (.45, '#e8c040')):
        c = [(43, 84), (43 + math.sin(a) * 20, 84 - 34), (43 + math.sin(a) * 34, 84 - 70)]
        shape(img, H(col), 25 + int(a * 10), tube(c, 3, 9), scale=3, stretch=(1, 3), contrast=1, k=.4, rim=.2)
    shape(img, hexc('#161412'), 29, oval(43, 98, 15, 15), scale=3, contrast=.6, k=.8, rim=.4, spec=.6)
    keep(img, 'fd_hane', 'fd', 'Волан для ханэцуки')


def f_tsubaki():
    img = canvas(116, 96); floor_shadow(img, 58, 88, 44)
    shape(img, hexc('#2e5a34'), 30, [(8, 70), (30, 58), (54, 70), (30, 80)], scale=4, k=.5, rim=.3, spec=.2)
    for i in range(6):
        a = i / 6 * math.tau; x, y = 60 + math.cos(a) * 20, 50 + math.sin(a) * 15
        shape(img, hexc('#b82232'), 31 + i, oval(x, y, 20, 17), scale=4, contrast=.8, dk=.4, lt=.2, k=.5, rim=.35)
    shape(img, hexc('#d63a46'), 38, oval(60, 48, 17, 13), scale=4, contrast=.6, k=.5, rim=.2)
    d = ImageDraw.Draw(img)
    for k in range(14): a = k / 14 * math.tau; d.line([(px(60), px(48)), (px(60 + math.cos(a) * 9), px(44 + math.sin(a) * 6))], fill=(236, 204, 80, 255), width=px(1.4))
    ell(img, (56, 42, 64, 50), (240, 220, 120, 255)); keep(img, 'fd_tsubaki', 'fd', 'Цветок камелии')


def f_tengu():
    img = canvas(100, 230)
    glowdot(img, 50, 110, 44, (230, 150, 70), 60, 20)
    vane = [(50, 8), (70, 50), (80, 110), (72, 170), (54, 214), (44, 212), (26, 160), (20, 100), (30, 44)]
    m = shape(img, hexc('#2a2224'), 39, vane, scale=5, stretch=(1, 4), contrast=1.2, dk=.4, lt=.3, k=.5, rim=.3, spec=.2)
    clipped(img, m, lambda d, l: [d.line([(px(50), px(20 + i * 6)), (px(50 + s * 36), px(8 + i * 6 + 20))], fill=(150, 70, 50, 110), width=px(1.2)) for i in range(32) for s in (-1, 1)])
    clipped(img, m, lambda d, l: [d.line(cr_pts, fill=(220, 160, 70, 200), width=px(2.5)) for cr_pts in [[(px(x), px(y)) for x, y in cr([(28, 60), (22, 110), (30, 170), (46, 212)], 6, False)], [(px(x), px(y)) for x, y in cr([(70, 50), (78, 110), (70, 172)], 6, False)]]])
    line(img, [(50, 10), (51, 110), (49, 224)], '#e0d8c0', 2)
    rnd = random.Random(40); d = ImageDraw.Draw(img)
    for _ in range(9): x, y = rnd.uniform(14, 86), rnd.uniform(20, 200); glowdot(img, x, y, 3, (255, 220, 150), 220, 1.5)
    keep(img, 'fd_tengu', 'fd', 'Перо тэнгу')


def f_magatama():
    img = canvas(96, 110); floor_shadow(img, 48, 102, 30)
    line(img, [(48, 8), (30, 20), (40, 36)], '#b8975a', 2); line(img, [(48, 8), (66, 18), (58, 36)], '#b8975a', 2)
    pts = [(48, 30), (70, 40), (76, 64), (66, 88), (46, 96), (30, 90), (26, 76), (38, 70), (46, 60), (36, 48), (32, 38)]
    m = shape(img, hexc('#3a8a5e'), 41, pts, scale=5, contrast=1.1, dk=.45, lt=.35, k=.6, rim=.35, spec=.55)
    clipped(img, m, lambda d, l: d.ellipse([px(50), px(56), px(76), px(92)], fill=(120, 200, 150, 90)))
    ell(img, (47, 38, 57, 48), (20, 40, 28, 255)); keep(img, 'fd_magatama', 'fd', 'Магатама из нефрита')


def f_moon():
    img = canvas(104, 86); floor_shadow(img, 52, 78, 40)
    glowdot(img, 52, 48, 40, (170, 200, 255), 110, 16)
    m = shape(img, hexc('#c8d0dc'), 42, [(12, 52), (26, 24), (56, 16), (88, 28), (94, 56), (74, 74), (40, 76), (18, 68)], scale=6, contrast=.5, dk=.2, lt=.2, k=.5, rim=.3, spec=.6)
    clipped(img, m, lambda d, l: d.ellipse([px(30), px(26), px(80), px(60)], fill=(150, 190, 255, 120)))
    soft(img, lambda d: d.ellipse([px(34), px(28), px(60), px(40)], fill=(255, 255, 255, 200)), 3)
    keep(img, 'fd_moon', 'fd', 'Лунный камешек', glow=[52, 46])


def f_ryu():
    img = canvas(104, 116); floor_shadow(img, 52, 108, 38)
    pts = [(52, 20), (70, 10), (90, 22), (92, 56), (74, 86), (52, 110), (30, 86), (12, 56), (14, 22), (34, 10)]
    m = shape(img, hexc('#2a7a78'), 43, pts, scale=5, contrast=1, dk=.45, lt=.3, k=.6, rim=.35, spec=.5)
    def irid(d, l):
        for k, col in enumerate([(220, 190, 90, 120), (120, 220, 200, 110), (170, 120, 220, 90)]):
            d.arc([px(20 + k * 6), px(20 + k * 8), px(84 - k * 6), px(100 - k * 4)], 200, 340, fill=col, width=px(6))
        for k in range(7): d.line([(px(52), px(18)), (px(20 + k * 10), px(96))], fill=(10, 40, 40, 90), width=px(1))
    clipped(img, m, irid); line(img, [(52, 22), (52, 104)], (230, 240, 210), 1.6)
    keep(img, 'fd_ryu', 'fd', 'Чешуйка дракона', glow=[52, 56])


# ───────────────────────── Rare-guest gifts ─────────────────────────
def g_yuki_usagi():
    img = canvas(150, 104); floor_shadow(img, 75, 96, 62)
    m = shape(img, hexc('#eef2f6'), 50, [(14, 84), (26, 50), (70, 36), (120, 46), (138, 80), (118, 94), (30, 94)], scale=6, contrast=.4, dk=.2, lt=.05, k=.6, rim=.3, spec=.2)
    clipped(img, m, lambda d, l: d.rectangle([px(0), px(78), px(150), px(100)], fill=(190, 205, 225, 120)))
    for x, a in ((56, -.5), (78, -.2)):
        c = [(x, 42), (x + math.sin(a) * 18, 22), (x + math.sin(a) * 30, 4)]
        shape(img, hexc('#3a6a34'), 51 + int(x), tube(c, 3, 8), scale=3, stretch=(1, 3), k=.5, rim=.3, spec=.2)
    for x in (40, 58): shape(img, hexc('#c82a2a'), 53 + x, oval(x, 60, 4.5, 4.5), scale=2, k=.6, rim=.3, spec=.7)
    rnd = random.Random(52); d = ImageDraw.Draw(img)
    for _ in range(18): x, y = rnd.uniform(20, 130), rnd.uniform(40, 90); d.ellipse([px(x - 1), px(y - 1), px(x + 1), px(y + 1)], fill=(255, 255, 255, 230))
    keep(img, 'rg_yuki_usagi', 'rg', 'Снежный зайчик, который не тает')


def g_yuki_comb():
    img = canvas(150, 84); floor_shadow(img, 75, 78, 60)
    body = [(12, 60), (18, 22), (50, 10), (100, 10), (132, 22), (138, 60)]
    m = shape(img, (190, 220, 240, 220), 54, body, scale=5, contrast=.6, dk=.25, lt=.25, k=.5, rim=-.1, spec=.5, smooth=False, feather=.5)
    clipped(img, m, lambda d, l: [d.line([(px(18 + k * 5.6), px(40)), (px(18 + k * 5.6), px(62))], fill=(0, 0, 0, 0), width=px(2.4)) for k in range(21)])
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(l)
    for k in range(21): dl.line([(px(20.8 + k * 5.6), px(40)), (px(20.8 + k * 5.6), px(62))], fill=(255, 255, 255, 255), width=px(2.2))
    a = np.asarray(img).copy(); la = np.asarray(l)[..., 3] > 0; a[la, 3] = (a[la, 3] * .15).astype(np.uint8); img.paste(Image.fromarray(a), (0, 0))
    def frost(d, l2):
        for cx, cy, r in ((50, 26, 9), (90, 24, 7), (116, 30, 5)):
            for k in range(6): an = k / 6 * math.pi; d.line([(px(cx - math.cos(an) * r), px(cy - math.sin(an) * r)), (px(cx + math.cos(an) * r), px(cy + math.sin(an) * r))], fill=(255, 255, 255, 230), width=px(1.3))
    clipped(img, m, frost); keep(img, 'rg_yuki_comb', 'rg', 'Ледяной гребень Юки-онны', glow=[75, 30])


def g_kodama_sprout():
    img = canvas(130, 160); floor_shadow(img, 65, 152, 50)
    shape(img, hexc('#8a5a3c'), 55, [(26, 100), (104, 100), (96, 150), (34, 150)], scale=5, contrast=1, k=.6, rim=.35, smooth=False, feather=.4)
    ell(img, (24, 94, 106, 106), (70, 46, 30, 255)); ell(img, (30, 96, 100, 104), (58, 44, 30, 255))
    line(img, [(65, 100), (63, 70), (68, 40), (64, 20)], '#5a4028', 3)
    line(img, [(64, 64), (46, 50)], '#5a4028', 2); line(img, [(67, 46), (86, 34)], '#5a4028', 2)
    for x, y, a in ((44, 46, -.8), (88, 30, .7), (60, 16, -.2), (72, 12, .5), (40, 56, -1.1), (92, 40, 1.2)):
        c = [(x, y), (x + math.sin(a) * 10, y - 10)]
        shape(img, hexc('#6aa04a'), 56 + int(x + y), tube([(x, y), ((x + c[1][0]) / 2, (y + c[1][1]) / 2), c[1]], 3, 7), scale=3, k=.5, rim=.3, spec=.15)
    line(img, [(28, 116), (65, 122), (102, 116)], '#d8c07a', 3.4)
    for x in (44, 65, 86): poly(img, [(x - 4, 120), (x + 4, 120), (x, 128), (x + 5, 128), (x + 1, 138), (x - 4, 138)], '#f2eee2')
    keep(img, 'rg_kodama_sprout', 'rg', 'Росток векового дерева')


def g_kodama_rope():
    img = canvas(230, 120)
    for k in range(10):
        pts = [(10 + i * 21, 28 + math.sin(i / 10 * math.pi) * 14 + math.sin(i + k) * 1.5) for i in range(11)]
        line(img, pts, mixc(hexc('#c8a860'), hexc('#8a6a30'), (k % 3) / 3), 4 - (k % 3))
    for s in (-1, 1): line(img, [(10 if s < 0 else 220, 28), (6 if s < 0 else 224, 6)], '#8a6a30', 3)
    volume(img, (6, 18, 224, 48), .4, .2)
    for x in (48, 115, 182):
        y0 = 34 + math.sin((x - 10) / 210 * math.pi) * 14
        fill(img, '#f2eee2', int(x), poly=[(x - 8, y0), (x + 8, y0), (x + 8, y0 + 18), (x, y0 + 18), (x, y0 + 36), (x + 8, y0 + 36), (x + 8, y0 + 54), (x - 8, y0 + 54), (x - 8, y0 + 36), (x - 16, y0 + 36), (x - 16, y0 + 18), (x - 8, y0 + 18)], scale=3, contrast=.4)
    keep(img, 'rg_kodama_rope', 'rg', 'Верёвка симэнава со священного дерева', anchor='t')


def g_amabie_print():
    img = canvas(140, 180)
    line(img, [(20, 8), (70, 2), (120, 8)], '#8a7a5a', 1.6)
    m = shape(img, hexc('#e6dcc2'), 57, [(14, 10), (126, 10), (128, 176), (12, 176)], scale=8, contrast=.6, dk=.15, lt=.08, k=.3, rim=.15, smooth=False, feather=.4)
    def draw(d, l):
        ink = (40, 34, 30, 255)
        for x in (114, 104, 94, 84):
            for y in range(22, 60, 9): d.line([(px(x - 3), px(y)), (px(x + 3), px(y))], fill=ink, width=px(1.3))
        d.polygon([(px(44), px(60)), (px(72), px(52)), (px(90), px(66)), (px(88), px(118)), (px(70), px(150)), (px(40), px(150)), (px(30), px(110))], fill=(92, 150, 138, 230))
        for k in range(22): d.line([(px(28 + k * 1.3), px(48)), (px(18 + k * 2.4), px(130))], fill=(30, 30, 30, 200), width=px(1))
        d.ellipse([px(46), px(52), px(76), px(80)], fill=(236, 226, 206, 255))
        d.polygon([(px(58), px(70)), (px(66), px(84)), (px(52), px(80))], fill=(220, 150, 60, 255))
        for ex in (54, 66): d.polygon([(px(ex), px(62)), (px(ex + 3), px(65)), (px(ex), px(68)), (px(ex - 3), px(65))], fill=ink)
        for x in (44, 60, 76): d.polygon([(px(x - 6), px(148)), (px(x + 6), px(148)), (px(x + 9), px(166)), (px(x - 9), px(166))], fill=(80, 130, 120, 240))
        for yy in range(90, 146, 8):
            for xx in range(40, 88, 8): d.arc([px(xx), px(yy), px(xx + 8), px(yy + 8)], 0, 180, fill=(40, 90, 80, 200), width=px(1))
        d.rectangle([px(20), px(154), px(32), px(166)], fill=(190, 50, 40, 230))
    clipped(img, m, draw); text(img, 'アマビエ', 104, 110, 13, '#2a2420', SERIF)
    keep(img, 'rg_amabie_print', 'rg', 'Листок с портретом Амабиэ', anchor='t')


def g_amabie_float():
    img = canvas(124, 124); floor_shadow(img, 62, 116, 46)
    m = shape(img, (60, 150, 120, 200), 58, oval(62, 64, 50, 50, 32), scale=6, contrast=.6, dk=.35, lt=.3, k=.6, rim=-.2, spec=.7)
    clipped(img, m, lambda d, l: d.ellipse([px(36), px(64), px(100), px(112)], fill=(120, 220, 170, 90)))
    for k in range(-3, 4):
        line(img, [(62 + k * 14 - math.copysign(4, k) if k else 62, 14), (62 + k * 16, 64), (62 + k * 14 - math.copysign(4, k) if k else 62, 114)], '#b89a60', 1.6)
    for y in (34, 64, 94): line(img, [(62 + math.cos(a) * 50 * math.sqrt(max(0, 1 - ((y - 64) / 50) ** 2)), y) for a in np.linspace(math.pi, 0, 12)], '#b89a60', 1.6)
    line(img, [(62, 14), (62, 4), (70, 2)], '#b89a60', 2.4)
    keep(img, 'rg_amabie_float', 'rg', 'Стеклянный поплавок из моря Хиго')


def g_usagi_usu():
    img = canvas(170, 160); floor_shadow(img, 85, 150, 66)
    shape(img, hexc('#7a5634'), 59, [(28, 90), (142, 90), (130, 148), (40, 148)], scale=6, stretch=(3, 1), contrast=1.1, k=.6, rim=.35, smooth=False, feather=.5)
    ell(img, (26, 82, 144, 100), hexc('#5a3e24')); ell(img, (40, 86, 130, 98), hexc('#efe8dc'))
    soft(img, lambda d: d.ellipse([px(60), px(84), px(110), px(96)], fill=(255, 255, 255, 200)), 2)
    shape(img, hexc('#9a7248'), 60, tube([(96, 90), (120, 50), (138, 14)], 5, 5), scale=4, stretch=(1, 3), k=.5, rim=.3)
    shape(img, hexc('#8a6440'), 61, tube([(112, 22), (138, 14), (164, 6)], 13, 13), scale=4, stretch=(3, 1), k=.6, rim=.35)
    keep(img, 'rg_usagi_usu', 'rg', 'Лунная ступка с пестиком')


def g_usagi_dango():
    img = canvas(140, 150); floor_shadow(img, 70, 144, 56)
    glowdot(img, 70, 60, 50, (255, 240, 190), 70, 18)
    fill(img, '#c8b48a', 62, poly=[(20, 100), (120, 100), (116, 110), (24, 110)], scale=4)
    fill(img, '#b09a72', 63, poly=[(34, 110), (106, 110), (100, 144), (40, 144)], scale=4)
    ell(img, (60, 118, 80, 136), (70, 56, 40, 255))
    for row, n in ((0, 4), (1, 3), (2, 2), (3, 1)):
        for k in range(n):
            x = 70 + (k - (n - 1) / 2) * 24; y = 88 - row * 20
            shape(img, hexc('#f4f0e6'), 64 + row * 5 + k, oval(x, y, 12.5, 11.5), scale=4, contrast=.3, dk=.18, lt=.05, k=.6, rim=.35, spec=.3)
    keep(img, 'rg_usagi_dango', 'rg', 'Цукими-данго с луны', glow=[70, 60])


# ───────────────────────── The seven day lanterns (chōchin) ─────────────────────────
NUM = '一二三四五六七'


def lantern(i, lit):
    img = canvas(84, 132)
    line(img, [(42, 0), (42, 10)], '#2a2018', 2); line(img, [(34, 12), (42, 6), (50, 12)], '#2a2018', 2)
    body = [(42, 20), (66, 26), (76, 50), (78, 74), (74, 98), (64, 116), (42, 122), (20, 116), (10, 98), (6, 74), (8, 50), (18, 26)]
    if lit:
        m = mask_of(img, body, feather=.6); box = m.getbbox(); w, h = box[2] - box[0], box[3] - box[1]
        yy, xx = np.mgrid[0:h, 0:w]; u = (xx - w / 2) / (w / 2); v = (yy - h * .52) / (h / 2); r = np.sqrt(u ** 2 * 1.1 + v ** 2)
        n = P.fbm(w, h, 6 * P.SS, 4, 70 + i) * .12
        t = np.clip(r, 0, 1)[..., None]
        core, mid, edge = np.array([255, 238, 190.]), np.array([246, 170, 80.]), np.array([170, 72, 34.])
        rgb = np.where(t < .55, core + (mid - core) * (t / .55), mid + (edge - mid) * ((t - .55) / .45)) * (1 - n[..., None] + .06)
        a = np.asarray(m.crop(box), np.float32)[..., None]
        img.alpha_composite(Image.fromarray(np.concatenate([np.clip(rgb, 0, 255), a], -1).astype(np.uint8), 'RGBA'), box[:2])
        rib, ink = (150, 70, 30, 150), (120, 30, 20, 235)
    else:
        m = shape(img, hexc('#6c655a'), 80 + i, body, scale=6, contrast=.7, dk=.45, lt=.12, k=.55, rim=.45)
        rib, ink = (40, 36, 32, 170), (48, 30, 26, 220)
    def ribs(d, l):
        for k in range(1, 12):
            y = 20 + k * 8.5; d.line([(px(2), px(y)), (px(82), px(y + 1.2))], fill=rib, width=px(1.3))
    clipped(img, m, ribs)
    if lit: soft(img, lambda d: d.ellipse([px(26), px(40), px(58), px(96)], fill=(255, 250, 225, 80)), 8)
    text(img, NUM[i], 42, 72, 32, (96, 22, 14) if lit else '#191311', SERIF, brush=True)
    for y0, y1 in ((14, 24), (116, 126)):
        fill(img, '#1a1614', 90 + i + y0, rect=(22, y0, 62, y1), scale=3, contrast=.6, dark=.3, light=.35)
        line(img, [(23, y0 + 1.5), (61, y0 + 1.5)], (110, 100, 90, 160), 1)
    keep(img, f'lan{i}{"on" if lit else "off"}', 'rg', sat=1)


# ───────────────────────── Rare seasonal guests (assets/mon) ─────────────────────────
def mon_yuki():
    img = M.canvas(340, 620); cx = 170
    soft(img, lambda d: d.ellipse([px(10), px(40), px(330), px(610)], fill=(200, 225, 255, 60)), 40)      # cold halo
    hb = shape(img, (14, 14, 20, 255), 101, [(cx - 70, 110), (cx - 60, 50), (cx, 26), (cx + 60, 50), (cx + 70, 110), (cx + 86, 330), (cx + 64, 420), (cx - 64, 420), (cx - 86, 330)], scale=6, contrast=.6, dk=.2, lt=.15, k=.3, rim=.1)
    hair_texture(img, hb, 102, [(cx + x, 40, 0) for x in range(-66, 67, 4)], 380, 200, col=(60, 62, 76))
    white, shade = (236, 240, 246, 255), (180, 196, 220, 255)
    body = [(cx - 44, 172), (cx, 164), (cx + 44, 172), (cx + 70, 250), (cx + 84, 380), (cx + 100, 520), (cx + 120, 610), (cx - 120, 610), (cx - 100, 520), (cx - 84, 380), (cx - 70, 250)]
    mb = shape(img, white, 103, body, scale=26, stretch=(1, 3), contrast=.7, dk=.25, lt=.05, k=.4, rim=.3)
    folds(img, mb, [[(cx - 20, 330), (cx - 30, 470), (cx - 44, 610)], [(cx + 26, 330), (cx + 40, 470), (cx + 60, 610)], [(cx, 360), (cx + 4, 610)]], (90, 110, 150, 80), 4)
    def snowpat(d, l):
        rnd = random.Random(104)
        for _ in range(26):
            x, y, r = rnd.uniform(cx - 110, cx + 110), rnd.uniform(300, 600), rnd.uniform(5, 9)
            for k in range(3): a = k / 3 * math.pi; d.line([(px(x - math.cos(a) * r), px(y - math.sin(a) * r)), (px(x + math.cos(a) * r), px(y + math.sin(a) * r))], fill=(130, 160, 210, 170), width=px(1.4))
    clipped(img, mb, snowpat)
    a = np.asarray(img, np.float32); fade = np.clip((np.arange(img.height)[:, None] - px(470)) / px(140), 0, 1); a[..., 3] *= 1 - .85 * fade; img = Image.fromarray(a.astype(np.uint8), 'RGBA')   # hem melts into mist
    shape(img, (150, 170, 200, 255), 105, [(cx - 70, 300), (cx + 70, 300), (cx + 72, 332), (cx - 72, 332)], scale=5, contrast=.5, k=.3, rim=.1, smooth=False)   # obi
    line(img, [(cx - 70, 316), (cx + 70, 316)], (230, 236, 246), 2)
    for sx in (-1, 1):
        sl = [(cx + sx * 44, 180), (cx + sx * 78, 210), (cx + sx * 104, 290), (cx + sx * 110, 400), (cx + sx * 96, 430), (cx + sx * 50, 420), (cx + sx * 40, 300)]
        ms = shape(img, white, 106 + sx, sl, scale=18, stretch=(1, 3), contrast=.6, dk=.25, lt=.05, k=.5, rim=.3)
        folds(img, ms, [[(cx + sx * 60, 250), (cx + sx * 76, 410)]], (90, 110, 150, 70), 3)
    shape(img, (226, 230, 238, 255), 108, oval(cx, 318, 26, 16), scale=5, contrast=.3, k=.4, rim=.2)     # hands folded
    poly_s(ImageDraw.Draw(img), [(cx - 26, 172), (cx, 232), (cx + 26, 172), (cx + 16, 172), (cx, 212), (cx - 16, 172)], (200, 212, 232, 255), 4)
    shape(img, (228, 232, 238, 255), 109, [(cx - 16, 130), (cx + 16, 130), (cx + 18, 176), (cx - 18, 176)], scale=8, contrast=.3, k=.3, rim=.2)
    shape(img, (236, 238, 242, 255), 110, oval(cx, 106, 40, 50), scale=10, contrast=.3, dk=.15, lt=.05, k=.35, rim=.25)
    bangs = [(cx - 44, 90), (cx - 40, 58), (cx - 16, 40), (cx + 16, 40), (cx + 40, 58), (cx + 44, 90), (cx + 30, 76), (cx, 72), (cx - 30, 76)]
    mbg = shape(img, (14, 14, 20, 255), 111, bangs, scale=6, contrast=.6, dk=.2, lt=.15, k=.3, rim=.1)
    hair_texture(img, mbg, 112, [(cx + x, 42, 0) for x in range(-44, 45, 3)], 50, 90, col=(60, 62, 76))
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        ex = cx + sx * 16; d.arc([px(ex - 10), px(100), px(ex + 10), px(112)], 20, 160, fill=(40, 44, 60, 255), width=px(2.2))
        for k in range(3): d.line([(px(ex + sx * (4 + k * 3)), px(108)), (px(ex + sx * (7 + k * 3)), px(114))], fill=(40, 44, 60, 200), width=px(1))
    d.arc([px(cx - 8), px(126), px(cx + 8), px(134)], 20, 160, fill=(120, 150, 200, 255), width=px(2.4))
    soft(img, lambda dd: [dd.ellipse([px(cx - 34), px(114), px(cx - 18), px(124)], fill=(170, 190, 230, 70)), dd.ellipse([px(cx + 18), px(114), px(cx + 34), px(124)], fill=(170, 190, 230, 70))], 4)
    rnd = random.Random(113)
    for _ in range(40): x, y = rnd.uniform(10, 330), rnd.uniform(20, 560); glowdot(img, x, y, rnd.uniform(1.5, 3.5), (255, 255, 255), 220, 1)
    M.save(img, 'm_rg_yuki')


def mon_kodama():
    img = M.canvas(300, 420); cx = 150
    soft(img, lambda d: d.ellipse([px(30), px(60), px(270), px(400)], fill=(170, 220, 140, 45)), 30)
    staff = [(236, 400), (230, 250), (238, 150), (250, 110)]
    shape(img, hexc('#5a4632'), 120, tube(staff, 5, 4), scale=4, stretch=(1, 3), k=.5, rim=.3)
    for x, y, a in ((250, 110, .3), (240, 132, 1.1), (256, 124, -.6)):
        shape(img, hexc('#78b050'), 121 + x, tube([(x, y), (x + math.sin(a) * 9, y - 8), (x + math.sin(a) * 16, y - 18)], 3, 8), scale=3, k=.5, rim=.3, spec=.2)
    cloak = [(cx - 30, 150), (cx, 138), (cx + 30, 150), (cx + 70, 260), (cx + 96, 390), (cx + 60, 410), (cx, 414), (cx - 60, 410), (cx - 96, 390), (cx - 70, 260)]
    mc = shape(img, hexc('#5e5040'), 122, cloak, scale=8, stretch=(1, 4), contrast=1.3, dk=.5, lt=.2, k=.5, rim=.4)
    clipped(img, mc, lambda d, l: [d.line([(px(x), px(150)), (px(x + (x - cx) * .5), px(414))], fill=(36, 28, 20, 150), width=px(3)) for x in range(cx - 30, cx + 31, 10)])
    rnd = random.Random(123)
    clipped(img, mc, lambda d, l: P.dab_mass(d, [(px(rnd.uniform(cx - 80, cx + 80)), px(rnd.uniform(200, 400)), px(26), px(14)) for _ in range(6)], 500, 'leaf', [hexc('#3a5a2a'), hexc('#5a7a3a'), hexc('#7a9a4a'), hexc('#9aba6a')], rnd, size=(3, 5)))
    for sx in (-1, 1):
        shape(img, hexc('#6a5846'), 124 + sx, tube([(cx + sx * 40, 210), (cx + sx * 62, 260), (cx + sx * 74, 300)], 12, 10), scale=5, stretch=(1, 3), k=.5, rim=.3)
    shape(img, hexc('#a88a64'), 126, oval(cx + 74, 304, 12, 12), scale=4, k=.5, rim=.3)
    shape(img, hexc('#a88a64'), 127, oval(cx - 74, 304, 12, 12), scale=4, k=.5, rim=.3)
    face = shape(img, hexc('#b08e66'), 128, [(cx, 60), (cx + 50, 78), (cx + 64, 130), (cx + 46, 176), (cx, 190), (cx - 46, 176), (cx - 64, 130), (cx - 50, 78)], scale=5, stretch=(1, 3), contrast=1, dk=.45, lt=.2, k=.55, rim=.4)
    clipped(img, face, lambda d, l: [d.arc([px(cx - r), px(128 - r * .8), px(cx + r), px(128 + r * .8)], 0, 360, fill=(110, 80, 50, 120), width=px(1.4)) for r in (70, 58)])
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        ex = cx + sx * 22
        d.ellipse([px(ex - 12), px(114), px(ex + 12), px(142)], fill=(40, 28, 18, 255))
        glowdot(img, ex, 128, 11, (220, 240, 140), 150, 5)
        d = ImageDraw.Draw(img); d.ellipse([px(ex - 5), px(122), px(ex + 5), px(134)], fill=(240, 250, 190, 255))
    d.arc([px(cx - 10), px(154), px(cx + 10), px(166)], 20, 160, fill=(70, 46, 28, 255), width=px(2.4))
    rnd = random.Random(129)
    P.dab_mass(ImageDraw.Draw(img), [(px(cx + dx), px(66 + dy), px(38), px(18)) for dx, dy in ((-40, 0), (0, -14), (40, 0))], 900, 'leaf', [hexc('#3e6a2c'), hexc('#5a8a3a'), hexc('#7aaa4a'), hexc('#a8cc70')], rnd, size=(4, 8))
    for x, y in ((cx - 42, 56), (cx + 30, 48), (cx + 6, 42)): flower(ImageDraw.Draw(img), x, y, 5.5, (244, 200, 214, 255))
    M.save(img, 'm_rg_kodama')


def mon_amabie():
    img = M.canvas(360, 480); cx = 180
    soft(img, lambda d: d.ellipse([px(30), px(60), px(330), px(470)], fill=(120, 220, 210, 50)), 34)
    teal, teal_d = hexc('#3f8f86'), hexc('#2a6a64')
    for k, x in enumerate((cx - 58, cx, cx + 58)):                                             # the three scaly legs/fins
        shape(img, teal_d, 140 + k, [(x - 22, 360), (x + 22, 360), (x + 26, 430), (x + 40, 470), (x - 40, 470), (x - 26, 430)], scale=4, k=.5, rim=.3)
        clipped(img, mask_of(img, [(x - 40, 440), (x + 40, 440), (x + 40, 470), (x - 40, 470)]), lambda d, l, x=x: [d.line([(px(x + j * 9), px(440)), (px(x + j * 13), px(470))], fill=(20, 60, 56, 200), width=px(1.4)) for j in range(-3, 4)])
    hb = shape(img, (20, 30, 30, 255), 143, [(cx - 70, 110), (cx - 50, 50), (cx, 34), (cx + 50, 50), (cx + 70, 110), (cx + 120, 300), (cx + 140, 400), (cx + 90, 380), (cx - 90, 380), (cx - 140, 400), (cx - 120, 300)], scale=6, contrast=.6, dk=.2, lt=.2, k=.3, rim=.1)
    hair_texture(img, hb, 144, [(cx + x, 46, math.copysign(.35, x) if x else 0) for x in range(-66, 67, 3)], 380, 260, col=(50, 76, 70), gravity=.2, sway=.4)
    body = [(cx - 50, 170), (cx, 160), (cx + 50, 170), (cx + 76, 260), (cx + 72, 340), (cx + 50, 380), (cx - 50, 380), (cx - 72, 340), (cx - 76, 260)]
    mb = shape(img, teal, 145, body, scale=6, contrast=.8, dk=.4, lt=.25, k=.55, rim=.4, spec=.15)
    def scales(d, l):
        for r in range(16):
            y = 190 + r * 12
            for c in range(12):
                x = cx - 76 + c * 14 + (r % 2) * 7; d.arc([px(x - 7), px(y - 6), px(x + 7), px(y + 8)], 0, 180, fill=(170, 230, 210, 170), width=px(1.4))
    clipped(img, mb, scales)
    for sx in (-1, 1): shape(img, teal_d, 146 + sx, tube([(cx + sx * 56, 196), (cx + sx * 80, 250), (cx + sx * 70, 300)], 11, 9), scale=4, k=.5, rim=.3)
    face = shape(img, (236, 228, 212, 255), 148, oval(cx, 116, 50, 54), scale=8, contrast=.3, dk=.15, lt=.05, k=.4, rim=.25)
    bangs = [(cx - 56, 106), (cx - 50, 66), (cx - 20, 50), (cx + 20, 50), (cx + 50, 66), (cx + 56, 106), (cx + 38, 84), (cx, 80), (cx - 38, 84)]
    mbg = shape(img, (20, 30, 30, 255), 149, bangs, scale=6, contrast=.6, k=.3, rim=.1)
    hair_texture(img, mbg, 150, [(cx + x, 52, 0) for x in range(-50, 51, 3)], 50, 90, col=(50, 76, 70))
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):        # diamond eyes, as in the 1846 print
        ex = cx + sx * 22; d.polygon([(px(ex - 12), px(112)), (px(ex), px(102)), (px(ex + 12), px(112)), (px(ex), px(122))], fill=(30, 26, 22, 255))
        d.ellipse([px(ex - 4), px(106), px(ex + 1), px(111)], fill=(255, 255, 255, 230))
    shape(img, hexc('#e0a040'), 151, [(cx - 12, 126), (cx + 12, 126), (cx + 4, 146), (cx, 158), (cx - 4, 146)], scale=3, k=.6, rim=.3, spec=.4, smooth=False, feather=.4)
    d = ImageDraw.Draw(img); d.line([(px(cx - 8), px(138)), (px(cx + 8), px(138))], fill=(140, 80, 20, 255), width=px(1.4))
    soft(img, lambda dd: [dd.ellipse([px(cx - 44), px(126), px(cx - 26), px(138)], fill=(230, 140, 140, 70)), dd.ellipse([px(cx + 26), px(126), px(cx + 44), px(138)], fill=(230, 140, 140, 70))], 4)
    rnd = random.Random(152)
    for _ in range(22): x, y = rnd.uniform(30, 330), rnd.uniform(60, 470); glowdot(img, x, y, rnd.uniform(1.5, 3), (200, 255, 240), 200, 1)
    M.save(img, 'm_rg_amabie')


def mon_usagi():
    img = M.canvas(360, 480); cx = 170
    soft(img, lambda d: d.ellipse([px(40), px(0), px(300), px(240)], fill=(250, 232, 170, 120)), 10)          # the moon behind
    shape(img, (244, 232, 190, 200), 160, oval(cx, 118, 116, 116, 40), scale=16, contrast=.6, dk=.12, lt=.05, k=.2, rim=.15)
    white, white_d = hexc('#f2eee6'), hexc('#d8d0c4')
    for sx in (-1, 1):
        shape(img, white_d, 161 + sx, [(cx + sx * 24, 420), (cx + sx * 60, 420), (cx + sx * 78, 470), (cx + sx * 10, 472)], scale=6, k=.5, rim=.3)
    shape(img, hexc('#9a7248'), 163, tube([(cx + 150, 440), (cx + 110, 300), (cx + 70, 160)], 6, 6), scale=4, stretch=(1, 3), k=.5, rim=.3)      # the kine handle
    shape(img, hexc('#8a6440'), 164, tube([(cx + 36, 170), (cx + 70, 160), (cx + 104, 150)], 25, 25), scale=4, stretch=(3, 1), k=.6, rim=.35)
    for e in ((cx + 36, 170), (cx + 104, 150)): ell(img, (e[0] - 8, e[1] - 25, e[0] + 8, e[1] + 25), (70, 50, 30, 200))   # mallet head over the shoulder
    body = [(cx - 50, 250), (cx, 236), (cx + 50, 250), (cx + 72, 330), (cx + 66, 420), (cx, 434), (cx - 66, 420), (cx - 72, 330)]
    mb = shape(img, white, 165, body, scale=9, contrast=.6, dk=.25, lt=.05, k=.5, rim=.35)
    fur_ticks(img, mb, 166, (cx - 72, 240, cx + 72, 432), 140, (170, 160, 150, 90), (4, 8))
    ind = hexc('#2c3e66')
    for sx in (-1, 1):       # a short indigo haori with wide sleeves
        mh = shape(img, ind, 167 + sx, [(cx + sx * 10, 250), (cx + sx * 54, 252), (cx + sx * 90, 300), (cx + sx * 92, 370), (cx + sx * 60, 380), (cx + sx * 58, 400), (cx + sx * 20, 404), (cx + sx * 8, 300)], scale=10, stretch=(1, 3), contrast=1, dk=.4, lt=.15, k=.5, rim=.3)
        clipped(img, mh, lambda d, l, s=sx: [d.ellipse([px(cx + s * 60 - 9), px(290 - 9), px(cx + s * 60 + 9), px(290 + 9)], outline=(230, 220, 190, 230), width=px(2)), d.line([(px(cx + s * 51), px(290)), (px(cx + s * 69), px(290))], fill=(230, 220, 190, 230), width=px(2))])
    line(img, [(cx - 10, 300), (cx + 10, 300)], '#e8d8a0', 2)
    shape(img, white, 170, oval(cx + 62, 190, 16, 14), scale=5, k=.4, rim=.3)                  # paw on the handle
    shape(img, white, 171, oval(cx - 30, 330, 15, 13), scale=5, k=.4, rim=.3)
    for sx, a in ((-1, -.18), (1, .12)):   # long ears
        c = [(cx + sx * 22, 150), (cx + sx * 30 + a * 60, 80), (cx + sx * 34 + a * 120, 16)]
        me = shape(img, white, 172 + sx, tube(c, 17, 13), scale=6, k=.5, rim=.35)
        clipped(img, me, lambda d, l, c=c: d.line([(px(x), px(y)) for x, y in cr(c, 6, False)], fill=(236, 170, 176, 230), width=px(9)))
    head = [(cx, 132), (cx + 44, 142), (cx + 62, 180), (cx + 56, 220), (cx + 26, 244), (cx, 248), (cx - 26, 244), (cx - 56, 220), (cx - 62, 180), (cx - 44, 142)]
    mhd = shape(img, white, 174, head, scale=7, contrast=.6, dk=.22, lt=.05, k=.5, rim=.35)
    fur_ticks(img, mhd, 175, (cx - 60, 136, cx + 60, 246), 60, (170, 160, 150, 80), (3, 6))
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        ex = cx + sx * 26; d.ellipse([px(ex - 9), px(178), px(ex + 9), px(198)], fill=hexc('#b8283a')); d.ellipse([px(ex - 4), px(182), px(ex + 1), px(188)], fill=(255, 255, 255, 230))
    poly_s(d, [(cx - 6, 206), (cx + 6, 206), (cx, 213)], (220, 140, 150, 255), 3)
    d.arc([px(cx - 10), px(210), px(cx), px(222)], 10, 170, fill=(120, 90, 90, 255), width=px(1.8)); d.arc([px(cx), px(210), px(cx + 10), px(222)], 10, 170, fill=(120, 90, 90, 255), width=px(1.8))
    for sx in (-1, 1):
        for k in range(3): d.line([(px(cx + sx * 16), px(212 + k * 4)), (px(cx + sx * 54), px(204 + k * 8))], fill=(150, 140, 130, 180), width=px(1))
    soft(img, lambda dd: [dd.ellipse([px(cx - 50), px(200), px(cx - 30), px(212)], fill=(236, 150, 160, 80)), dd.ellipse([px(cx + 30), px(200), px(cx + 50), px(212)], fill=(236, 150, 160, 80))], 4)
    M.save(img, 'm_rg_usagi')


if __name__ == '__main__':
    for f in (f_crow, f_pebble, f_button, f_mon, f_tsuru, f_momiji, f_cone, f_acorn, f_shard, f_bell, f_thread, f_shell, f_hotaru, f_semi, f_hane, f_tsubaki, f_tengu, f_magatama, f_moon, f_ryu): f()
    for f in (g_yuki_usagi, g_yuki_comb, g_kodama_sprout, g_kodama_rope, g_amabie_print, g_amabie_float, g_usagi_usu, g_usagi_dango): f()
    for i in range(7): lantern(i, True); lantern(i, False)
    posF, szF = pack('fd'); posG, szG = pack('rg')
    for f in (mon_yuki, mon_kodama, mon_amabie, mon_usagi): f()
    rows = []
    for r in ROWS:
        p = posF.get(r['id']) or posG.get(r['id']); r['at'] = ['fd' if r['id'] in posF else 'rg', p[0], p[1]]; rows.append(r)
    lan = {k: v for k, v in posG.items() if k.startswith('lan')}
    json.dump({'atl': {'fd': szF, 'rg': szG}, 'items': rows, 'lan': lan, 'mon': M.META}, open(os.path.join(PREV, 'return_art.json'), 'w'), ensure_ascii=False)
    print(json.dumps({'atl': {'fd': szF, 'rg': szG}, 'lan': lan, 'mon': M.META}, ensure_ascii=False))
    for r in rows: print(json.dumps(r, ensure_ascii=False))
