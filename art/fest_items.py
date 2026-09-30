#!/usr/bin/env python3
"""Festival things for the ten holidays of the Japanese year, and presents that yōkai guests leave behind.
Same brushes as items.py / room_items2.py; pictures are packed into two atlases (the Claude copy allows ~500 files).
Usage: fest_items.py <outdir> → <outdir>/atlas_fst.webp, atlas_gft.webp + fest.json (rows carry "at": [slug, x, y])"""
import json, math, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc
import items as I
from items import px, canvas, fill, volume, soft, floor_shadow, line, ell, poly, text, H, dk, lt, SERIF, SANS, mask_poly
from room_items import clip, crock, plate, rope, cr, blob, figure_base, WOOD, WOOD_D, WOOD_L
from room_items2 import flowers, leaves, glass, pot

OUT = sys.argv[1]
ROWS, IMGS = [], {}
SLUG = {'Праздники': 'fst', 'Подарки гостей': 'gft'}
FEST = None
LACQ, LACQ_R, GOLD, PAPER = '#1a1412', '#8a1a14', '#d8b048', '#f2ead8'


def save(img, iid, name, anchor='b', price=40, glow=None, reward=False, gift=None, gl=None):
    cat = 'Подарки гостей' if gift else 'Праздники'
    out = img.resize((P.W, P.H), Image.LANCZOS)
    a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .88
    a[..., :3] += np.random.default_rng(sum(map(ord, iid))).normal(0, 3.5, a.shape[:2])[..., None]
    IMGS.setdefault(cat, []).append((iid, Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')))
    row = {'id': iid, 'n': name, 'c': cat, 'w': P.W, 'h': P.H, 'a': anchor, 'p': 0 if (reward or gift) else price}
    if glow: row['glow'] = glow
    if gift: row['gift'] = gift; row['gl'] = gl
    else: row['fest'] = FEST
    if reward: row['reward'] = True
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


# ───────────────────────────── shared shapes ─────────────────────────────
def ball(img, cx, cy, rx, ry, col, seed, k=.5, rim=.45, spec=.3, scale=3, contrast=.5):
    tmp = Image.new('RGBA', img.size, (0, 0, 0, 0))
    fill(tmp, col, seed, ell=(cx - rx, cy - ry, cx + rx, cy + ry), scale=scale, contrast=contrast)
    volume(tmp, (cx - rx, cy - ry, cx + rx, cy + ry), k, rim, spec=spec); img.alpha_composite(tmp)


def part(img, col, seed, pts, k=.45, rim=.3, spec=0, scale=5, contrast=1.0, stretch=(1, 1)):
    """Sharp-edged polygon painted on its own layer so the volume shading does not touch its neighbours."""
    tmp = Image.new('RGBA', img.size, (0, 0, 0, 0)); m = fill(tmp, col, seed, poly=pts, scale=scale, contrast=contrast, stretch=stretch)
    xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
    if max(xs) > 0 and max(ys) > 0 and min(xs) < P.W and min(ys) < P.H: volume(tmp, (max(0, min(xs)), max(0, min(ys)), max(xs), max(ys)), k, rim, spec=spec)
    img.alpha_composite(tmp); return m


def rect_part(img, col, seed, box, **kw):
    x0, y0, x1, y1 = box; return part(img, col, seed, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], **kw)


def sanbo(img, cx, base, w, seed):
    """Wooden offering stand: box with an eye-shaped cut-out, tray with a raised rim. Returns the tray top."""
    h1 = w * .42
    part(img, '#c9a26a', seed, [(cx - w * .34, base), (cx + w * .34, base), (cx + w * .3, base - h1), (cx - w * .3, base - h1)], stretch=(3, .5), k=.35)
    blob(img, [(cx - w * .12, base - h1 * .5), (cx, base - h1 * .74), (cx + w * .12, base - h1 * .5), (cx, base - h1 * .26)], hexc('#3a2616'), seed + 1, scale=3, k=.2)
    rect_part(img, '#d8b47a', seed + 2, (cx - w / 2, base - h1 - 16, cx + w / 2, base - h1), stretch=(4, .5), k=.3)
    ImageDraw.Draw(img).line([(px(cx - w / 2), px(base - h1 - 15)), (px(cx + w / 2), px(base - h1 - 15))], fill=H('#f0d8a8'), width=px(1.5))
    return base - h1 - 16


def kakejiku(img, W, Hh, seed, paint, mount='#5a4a34', paper='#e6dcc4'):
    rope(img, [(W / 2 - 34, 16), (W / 2, 3), (W / 2 + 34, 16)], '#c8a060', 1.8)
    rect_part(img, '#2a1c14', seed, (8, 13, W - 8, 24), k=.3)
    fill(img, mount, seed + 1, rect=(14, 24, W - 14, Hh - 24), scale=4, contrast=.8)
    fill(img, paper, seed + 2, rect=(24, 46, W - 24, Hh - 52), scale=6, contrast=.35)
    paint((24, 46, W - 24, Hh - 52))
    rect_part(img, '#2a1c14', seed + 3, (6, Hh - 24, W - 6, Hh - 12), k=.3)
    for x in (2, W - 14): rect_part(img, '#8a6a3a', seed + 4 + x, (x, Hh - 26, x + 12, Hh - 10), k=.4, spec=.2)


def paper_lantern(img, cx, y0, y1, w, col, seed, ribs=9, caps='#1a1412', lit=True):
    m = fill(img, col, seed, ell=(cx - w / 2, y0, cx + w / 2, y1), scale=5, contrast=.55)
    clip(img, m, lambda d: [d.line([(0, px(y0 + (y1 - y0) * k / ribs)), (px(cx + w), px(y0 + (y1 - y0) * k / ribs))], fill=(110, 80, 50, 110), width=px(1.2)) for k in range(1, ribs)])
    if lit: soft(img, lambda d: d.ellipse([px(cx - w * .3), px(y0 + (y1 - y0) * .25), px(cx + w * .3), px(y1 - (y1 - y0) * .25)], fill=(255, 220, 150, 70)), 8)
    volume(img, (cx - w / 2, y0, cx + w / 2, y1), .45, .45)
    for yy, hh in ((y0 - 6, 12), (y1 - 6, 12)): rect_part(img, caps, seed + int(yy), (cx - w * .26, yy, cx + w * .26, yy + hh), k=.3, spec=.15)
    return m


def leaf(img, x, y, L, Wd, ang, col, seed, vein=True):
    ca, sa = math.cos(ang), math.sin(ang); pts = []
    for k in range(9):
        u = k / 8; r = Wd * math.sin(math.pi * u) ** .8; pts.append((x + ca * L * u - sa * r, y + sa * L * u + ca * r))
    for k in range(7, 0, -1):
        u = k / 8; r = Wd * math.sin(math.pi * u) ** .8; pts.append((x + ca * L * u + sa * r, y + sa * L * u - ca * r))
    part(img, col, seed, pts, k=.35, rim=.2, scale=3)
    if vein: line(img, [(x, y), (x + ca * L * .9, y + sa * L * .9)], lt(H(col), .25), max(1, Wd * .08))


def cup(img, cx, base, w, h, col, seed, inside='#f2ead8'):
    part(img, col, seed, [(cx - w / 2, base - h), (cx + w / 2, base - h), (cx + w * .36, base), (cx - w * .36, base)], k=.5, spec=.25, scale=3)
    fill(img, inside, seed + 1, ell=(cx - w / 2, base - h - w * .12, cx + w / 2, base - h + w * .12), scale=3, contrast=.3)


def spikes(img, cx, cy, r, n, col):
    for k in range(n):
        a = k / n * math.tau; poly(img, [(cx + math.cos(a) * r, cy + math.sin(a) * r), (cx + math.cos(a + .25) * r * .55, cy + math.sin(a + .25) * r * .55), (cx + math.cos(a - .25) * r * .55, cy + math.sin(a - .25) * r * .55)], col)


def carp(img, x0, y0, L, Hc, col, belly, seed, wave=0.0):
    """Koinobori windsock: mouth on the left, tail streaming to the right."""
    def yo(u): return y0 + math.sin(u * 5 + seed) * wave * Hc * .25 * u
    top = [(x0 + L * u, yo(u) - Hc * (.46 - .12 * u) + (Hc * .18 if u > .86 else 0)) for u in (0, .15, .35, .55, .72, .86)]
    bot = [(x0 + L * u, yo(u) + Hc * (.46 - .12 * u) - (Hc * .18 if u > .86 else 0)) for u in (.86, .72, .55, .35, .15, 0)]
    tail = [(x0 + L, yo(1) - Hc * .5), (x0 + L * .94, yo(.94)), (x0 + L, yo(1) + Hc * .5)]
    pts = top + tail + bot
    m = part(img, col, seed, pts, k=.35, rim=.35, scale=4, contrast=.8)
    part(img, belly, seed + 1, [(x0 + L * .05, yo(.05) + Hc * .12), (x0 + L * .7, yo(.7) + Hc * .08), (x0 + L * .7, yo(.7) + Hc * .3), (x0 + L * .05, yo(.05) + Hc * .4)], k=.2, scale=3)
    def scales(d):
        for i in range(5):
            for j in range(3):
                x = x0 + L * (.26 + i * .1); y = yo(.26 + i * .1) - Hc * .25 + j * Hc * .2
                d.arc([px(x - Hc * .12), px(y - Hc * .1), px(x + Hc * .12), px(y + Hc * .1)], 90, 270, fill=(255, 255, 255, 90), width=px(1.4))
    clip(img, m, scales)
    ex, ey = x0 + L * .12, yo(.12) - Hc * .1
    ell(img, (ex - Hc * .16, ey - Hc * .16, ex + Hc * .16, ey + Hc * .16), '#f2eee4'); ell(img, (ex - Hc * .08, ey - Hc * .08, ex + Hc * .08, ey + Hc * .08), '#141010')
    ImageDraw.Draw(img).ellipse([px(x0 - 3), px(y0 - Hc * .44), px(x0 + 7), px(y0 + Hc * .44)], outline=H('#e8e0d0'), width=px(2.4))


def doll(img, cx, base, h, robe, seed, crown=None, face='#f2ece2', skirt=None):
    part(img, robe, seed, [(cx - h * .46, base), (cx - h * .34, base - h * .5), (cx - h * .14, base - h * .68), (cx + h * .14, base - h * .68), (cx + h * .34, base - h * .5), (cx + h * .46, base)], k=.45, scale=3)
    if skirt: part(img, skirt, seed + 1, [(cx - h * .2, base), (cx - h * .12, base - h * .4), (cx + h * .12, base - h * .4), (cx + h * .2, base)], k=.3, scale=3)
    for s in (-1, 1): line(img, [(cx, base - h * .5), (cx + s * h * .12, base - h * .68)], '#f2eee4', max(1.2, h * .03))
    ball(img, cx, base - h * .82, h * .13, h * .15, '#161212', seed + 2, spec=.2)
    ball(img, cx, base - h * .8, h * .1, h * .12, face, seed + 3, spec=.15, k=.3)
    if crown: poly(img, [(cx - h * .06, base - h * .94), (cx + h * .06, base - h * .94), (cx + h * .02, base - h * 1.08), (cx - h * .02, base - h * 1.08)], crown)


# ───────────────────────────── 1. Сёгацу (Новый год) ─────────────────────────────
def shogatsu():
    global FEST; FEST = 'shogatsu'
    img = canvas(160, 180); floor_shadow(img, 80, 174, 70)                                     # kagami mochi
    top = sanbo(img, 80, 174, 140, 101)
    part(img, '#f4f0e8', 102, [(22, top + 2), (80, top - 16), (138, top + 2), (80, top + 10)], k=.2, scale=3)
    ImageDraw.Draw(img).line([(px(22), px(top + 2)), (px(80), px(top + 10)), (px(138), px(top + 2))], fill=H('#c02a2a'), width=px(2))
    ball(img, 80, top - 20, 52, 22, '#f2eee6', 103, spec=.25, k=.35)
    ball(img, 80, top - 48, 38, 17, '#f4f0ea', 104, spec=.3, k=.35)
    ball(img, 80, top - 74, 17, 15, '#e8902a', 105, spec=.35)
    leaf(img, 82, top - 88, 26, 7, -.5, '#2f6a2a', 106)
    save(img, 'f_kagamimochi', 'Кагами-моти с мандарином', 'b', 80)

    img = canvas(200, 220)                                                                     # shimekazari
    line(img, [(100, 0), (100, 18)], '#3a2a1a', 2)
    d = ImageDraw.Draw(img)
    for k in range(3):
        d.ellipse([px(36 + k * 4), px(20 + k * 4), px(164 - k * 4), px(148 - k * 4)], outline=H(['#a88a44', '#d0b068', '#b89a52'][k]), width=px(6))
    for a in range(0, 360, 15):
        r = 58; x, y = 100 + math.cos(math.radians(a)) * r, 84 + math.sin(math.radians(a)) * r; ta = math.radians(a + 90)
        line(img, [(x - math.cos(ta + .8) * 7, y - math.sin(ta + .8) * 7), (x + math.cos(ta + .8) * 7, y + math.sin(ta + .8) * 7)], '#7a6030', 1.4)
    rr = random.Random(7)
    for k in range(22): x = 78 + k * 2; line(img, [(x, 140), (x + rr.uniform(-4, 4), 214)], rr.choice(['#c8a860', '#b89a52', '#d8b870']), 1.6)
    rect_part(img, '#c02a2a', 108, (72, 132, 128, 146), k=.3)
    for sx in (-1, 1):
        x = 100 + sx * 58
        for j in range(4): poly(img, [(x - 9 + j % 2 * 6, 110 + j * 20), (x + 9 + j % 2 * 6, 110 + j * 20), (x + 9 + (j + 1) % 2 * 6, 130 + j * 20), (x - 9 + (j + 1) % 2 * 6, 130 + j * 20)], '#f6f2ea')
    for k in range(5): leaf(img, 100, 70, 34, 5, math.pi + .35 + k * .23, '#1f4a22', 110 + k, vein=False)
    ball(img, 100, 76, 20, 18, '#e8882a', 116, spec=.4)
    fill(img, '#f2eee4', 117, poly=[(70, 92), (130, 92), (124, 124), (76, 124)], scale=3, contrast=.2); text(img, '迎春', 100, 108, 17, '#b02a22', SERIF)
    save(img, 'f_shimekazari', 'Симэкадзари над дверью', 't', 70)

    img = canvas(90, 300); floor_shadow(img, 45, 294, 36)                                     # hamaya arrow
    rect_part(img, LACQ, 120, (18, 262, 72, 294), k=.3, spec=.15); rect_part(img, '#c02a2a', 121, (14, 256, 76, 264), k=.3)
    rect_part(img, '#f2eee4', 122, (41, 40, 49, 262), k=.3)
    for s in (-1, 1): part(img, '#f4f2ec', 123 + s, [(45, 20), (45 + s * 18, 34), (45 + s * 16, 96), (45, 84)], k=.2, scale=2)
    for y in (40, 56, 72): line(img, [(30, y + 4), (60, y)], '#c8c0b0', .8)
    line(img, [(45, 120), (60, 140)], '#c02a2a', 1.4); line(img, [(46, 120), (32, 142)], '#f2eee4', 1.4)
    fill(img, '#d8b068', 124, poly=[(22, 140), (54, 140), (60, 150), (60, 186), (16, 186), (16, 150)], scale=4, stretch=(3, .5)); text(img, '破魔', 38, 164, 13, '#1a1410', SERIF)
    ball(img, 62, 152, 7, 7, GOLD, 125, spec=.5)
    save(img, 'f_hamaya', 'Стрела-оберег хамая', 'b', 60)

    img = canvas(160, 90); floor_shadow(img, 80, 84, 72)                                      # nengajo cards
    for k in range(4): part(img, '#f2eee4', 130 + k, [(20 + k * 4, 80 - k * 5), (124 + k * 4, 72 - k * 6), (132 + k * 4, 30 - k * 6), (28 + k * 4, 38 - k * 5)], k=.2, scale=3, contrast=.3)
    ell(img, (70, 28, 96, 50), '#c83a2a'); text(img, '賀正', 110, 44, 13, '#1a1410', SERIF)
    rect_part(img, '#2a5a8a', 135, (116, 16, 130, 32), k=.2)
    save(img, 'f_nengajo', 'Стопка открыток нэнгадзё', 'b', 30)

    img = canvas(150, 100); floor_shadow(img, 75, 94, 66)                                     # otoshidama
    for k, (x, c, a) in enumerate(((42, '#f4d4dc', -.25), (75, '#f2eee4', 0), (108, '#c83a2a', .25))):
        ca, sa = math.cos(a), math.sin(a); pts = [(-22, -34), (22, -34), (22, 34), (-22, 34)]
        part(img, c, 140 + k, [(x + px_ * ca - py * sa, 58 + px_ * sa + py * ca) for px_, py in pts], k=.3, scale=3, contrast=.4)
    text(img, 'お年玉', 108, 58, 11, GOLD, SERIF); ell(img, (68, 40, 82, 54), '#c83a2a'); text(img, '梅', 42, 60, 16, '#b0343a', SERIF)
    save(img, 'f_otoshidama', 'Конвертики отосидама', 'b', 40)

    def dream(box):
        x0, y0, x1, y1 = box; w = x1 - x0; cx = x0 + w * .5
        ell(img, (x1 - 40, y0 + 10, x1 - 12, y0 + 38), '#c83a2a')
        hx, hy = x0 + w * .32, y0 + 34
        poly(img, [(hx - 24, hy + 4), (hx, hy - 6), (hx + 24, hy + 4), (hx + 4, hy + 2), (hx, hy + 10), (hx - 4, hy + 2)], '#2a2018')
        part(img, '#3a5a8a', 151, [(x0 + 2, y0 + 136), (cx, y0 + 58), (x1 - 2, y0 + 136)], k=.3, scale=6)
        part(img, '#f2eee8', 152, [(cx - w * .13, y0 + 80), (cx, y0 + 58), (cx + w * .13, y0 + 80), (cx + w * .05, y0 + 86), (cx - w * .05, y0 + 82)], k=.1, scale=3)
        ey = y0 + 184
        blob(img, [(cx - 26, ey + 14), (cx - 16, ey - 16), (cx + 6, ey - 24), (cx + 24, ey - 6), (cx + 20, ey + 18), (cx - 4, ey + 26)], hexc('#4a2a6a'), 153, scale=3, spec=.4)
        poly(img, [(cx - 2, ey - 30), (cx + 16, ey - 20), (cx + 8, ey - 12), (cx - 6, ey - 16)], '#2f5a2a')
        for k, ch in enumerate('初夢'): text(img, ch, x0 + 13, y0 + 162 + k * 22, 16, '#1a1410', SERIF)
    kakejiku(img := canvas(170, 330), 170, 330, 150, dream)
    save(img, 'f_r_hatsuyume', 'Свиток «Первый сон»: Фудзи, ястреб, баклажан', 't', reward=True)


# ───────────────────────────── 2. Сэцубун ─────────────────────────────
def setsubun():
    global FEST; FEST = 'setsubun'
    img = canvas(150, 120); floor_shadow(img, 75, 114, 66)                                    # masu with beans
    part(img, '#d8b47a', 201, [(20, 50), (130, 50), (124, 114), (26, 114)], stretch=(3, .5), k=.4)
    part(img, '#c49a60', 202, [(20, 50), (130, 50), (116, 38), (34, 38)], stretch=(3, .5), k=.2)
    rr = random.Random(3)
    for k in range(70):
        x = rr.uniform(32, 118); y = 48 - math.sin((x - 32) / 86 * math.pi) * 18 * rr.random()
        ball(img, x, y, 6, 5, rr.choice(['#c8984a', '#d8aa5a', '#b8883a']), 203 + k, spec=.4, k=.4)
    text(img, '福', 75, 84, 34, '#1a1410', SERIF)
    save(img, 'f_masu', 'Мера с бобами фукумамэ', 'b', 30)

    img = canvas(140, 240); line(img, [(70, 0), (70, 24)], '#3a2a1a', 1.8)                    # hiiragi + sardine
    line(img, [(70, 24), (76, 230)], '#4a3222', 4)
    for k, (y, s) in enumerate(((70, -1), (96, 1), (124, -1), (150, 1), (178, -1), (204, 1))):
        pts = []
        for j in range(7):
            u = j / 6; r = 13 * math.sin(math.pi * u) + (5 if j % 2 else 0)
            pts.append((72 + s * 48 * u, y - 16 * u - r))
        for j in range(6, -1, -1):
            u = j / 6; r = 13 * math.sin(math.pi * u) + (5 if j % 2 else 0)
            pts.append((72 + s * 48 * u, y - 16 * u + r * .6))
        part(img, '#1e3e22', 220 + k, pts, k=.35, spec=.25, scale=3)
    part(img, '#8a98a8', 230, [(52, 60), (70, 26), (88, 60), (70, 70)], k=.4, spec=.5, scale=2)
    ell(img, (62, 38, 72, 48), '#f2eee4'); ell(img, (65, 41, 70, 46), '#141010')
    line(img, [(58, 58), (82, 58)], '#c8b8a0', 1.2)
    save(img, 'f_hiiragi', 'Ветка остролиста с сардиной', 't', 40)

    img = canvas(170, 190); line(img, [(30, 70), (85, 4), (140, 70)], '#e8e0d0', 1.2)         # paper oni mask
    for s in (-1, 1): part(img, '#e8c040', 240 + s, [(85 + s * 36, 58), (85 + s * 62, 6), (85 + s * 54, 62)], k=.4, spec=.3, scale=2)
    m = part(img, '#c8321e', 242, cr([(20, 90), (30, 46), (85, 30), (140, 46), (150, 90), (132, 160), (85, 184), (38, 160)]), k=.35, scale=4, contrast=.6)
    rr = random.Random(9)
    for k in range(9): x = 30 + k * 14; ell(img, (x - 12, 26 + rr.uniform(-6, 6), x + 12, 50 + rr.uniform(-6, 6)), '#1a1410')
    for s in (-1, 1):
        poly(img, [(85 + s * 16, 82), (85 + s * 54, 70), (85 + s * 50, 86)], '#1a1410')
        ell(img, (85 + s * 34 - 16, 90, 85 + s * 34 + 16, 118), '#f2e04a'); ell(img, (85 + s * 34 - 6, 98, 85 + s * 34 + 6, 112), '#141010')
    ball(img, 85, 130, 12, 9, '#a82618', 243, spec=.3)
    part(img, '#3a1410', 244, [(44, 148), (126, 148), (110, 172), (60, 172)], k=.2, scale=2)
    for s in (-1, 1): poly(img, [(85 + s * 30, 148), (85 + s * 22, 148), (85 + s * 26, 132)], '#f2eee4')
    save(img, 'f_onimen', 'Бумажная маска красного óни', 't', 40)

    img = canvas(220, 100); floor_shadow(img, 110, 94, 100)                                   # ehomaki
    m = part(img, '#b8a060', 250, [(10, 70), (200, 60), (214, 90), (22, 96)], k=.3, stretch=(.3, 3), scale=4)
    clip(img, m, lambda d: [d.line([(px(10 + k * 12), px(60)), (px(22 + k * 12), px(98))], fill=(90, 70, 30, 120), width=px(1)) for k in range(17)])
    part(img, '#161a14', 251, [(20, 48), (176, 38), (180, 72), (24, 82)], k=.55, rim=.3, spec=.2, scale=3)
    ball(img, 180, 55, 18, 20, '#f2eee6', 252, k=.2, spec=0)
    ImageDraw.Draw(img).ellipse([px(162), px(35), px(198), px(75)], outline=H('#161a14'), width=px(3))
    for (dx, dy, c) in ((-6, -6, '#e8c040'), (5, -4, '#e8889a'), (-3, 7, '#3a7a3a'), (7, 7, '#c05a2a')): ell(img, (180 + dx - 4, 55 + dy - 4, 180 + dx + 4, 55 + dy + 4), c)
    save(img, 'f_ehomaki', 'Эхомаки на бамбуковой циновке', 'b', 50)

    img = canvas(120, 320); floor_shadow(img, 60, 314, 44)                                    # kanabo
    rect_part(img, '#3a2a1e', 260, (22, 290, 98, 314), k=.3)
    part(img, '#2a2a2e', 261, [(44, 290), (76, 290), (84, 30), (60, 12), (36, 30)], k=.55, rim=.35, spec=.25, scale=3)
    for y in range(44, 250, 22):
        for x in ((40 + (y - 30) * .03), 60, (80 - (y - 30) * .03)):
            ball(img, x + (6 if (y // 22) % 2 else -6) * (x == 60), y, 5, 5, GOLD, 262 + y + int(x), spec=.6, k=.4)
    rect_part(img, '#8a1a14', 263, (46, 250, 74, 290), k=.3)
    for y in range(254, 290, 8): line(img, [(46, y), (74, y + 4)], '#5a0e0a', 1.4)
    save(img, 'f_r_kanabo', 'Шипастая палица óни канабо', 'b', reward=True)


# ───────────────────────────── 3. Хинамацури ─────────────────────────────
def hina():
    global FEST; FEST = 'hina'
    img = canvas(320, 330); floor_shadow(img, 160, 324, 150)                                  # hina dan
    for k, (y, w) in enumerate(((320, 300), (230, 240), (140, 180))):
        part(img, '#b8241c', 301 + k, [(160 - w / 2, y), (160 + w / 2, y), (160 + w / 2 - 6, y - 90), (160 - w / 2 + 6, y - 90)], k=.35, rim=.2, scale=6, contrast=.7)
        rect_part(img, '#d83a2a', 305 + k, (160 - w / 2 + 6, y - 94, 160 + w / 2 - 6, y - 84), k=.2)
    fill(img, '#c8a040', 310, rect=(80, 12, 240, 52), scale=4, contrast=.6)
    for x in range(80, 241, 32): line(img, [(x, 12), (x, 52)], '#8a6a2a', 1.4)
    doll(img, 120, 50, 58, '#1a2440', 311, crown='#e8c040'); doll(img, 200, 50, 58, '#b02030', 312, crown='#e8c040', skirt='#e8c048')
    for k, x in enumerate((110, 160, 210)): doll(img, x, 140, 46, '#f2eee4', 313 + k, skirt='#c02a2a')
    for x in (60, 260):
        line(img, [(x, 230), (x, 196)], '#1a1412', 2.4); rect_part(img, '#f2e8c8', 320 + x, (x - 10, 176, x + 10, 198), k=.3); rect_part(img, LACQ, 321 + x, (x - 12, 172, x + 12, 178), k=.2)
    for k, x in enumerate((100, 160, 220)):
        rect_part(img, '#2a1c14', 330 + k, (x - 20, 214, x + 20, 230), k=.3)
        for j, c in enumerate(('#e888a8', '#f2eee4', '#5a9a4a')): part(img, c, 333 + k * 3 + j, [(x - 16, 212 - j * 6), (x + 16, 212 - j * 6), (x + 12, 206 - j * 6), (x - 20, 206 - j * 6)], k=.2, scale=2)
    save(img, 'f_hinadan', 'Лесенка кукол хина', 'b', 300)

    img = canvas(150, 130); floor_shadow(img, 75, 124, 64)                                    # hishi mochi
    part(img, LACQ, 350, [(26, 124), (124, 124), (118, 96), (32, 96)], k=.4, spec=.2)
    part(img, LACQ_R, 351, [(20, 96), (130, 96), (126, 86), (24, 86)], k=.3)
    for j, c in enumerate(('#5a9a4a', '#f4f0e8', '#ec8aa8')):
        y = 86 - j * 18; part(img, c, 352 + j, [(22, y), (96, y), (130, y - 14), (56, y - 14)], k=.2, scale=3, contrast=.4)
        part(img, dk(H(c), .12), 356 + j, [(22, y), (96, y), (96, y + 6), (22, y + 6)], k=.1, scale=2)
    save(img, 'f_hishimochi', 'Трёхцветный хиси-моти', 'b', 40)

    img = canvas(170, 300); floor_shadow(img, 85, 294, 54)                                    # peach branch
    rr = random.Random(11); d = ImageDraw.Draw(img); pts = []
    def br(x, y, a, L, w, dd):
        if dd > 3 or L < 14: return
        x1, y1 = x + math.sin(a) * L, y - math.cos(a) * L; line(img, [(x, y), (x1, y1)], '#3a2418', w); pts.append((x1, y1)); pts.append(((x + x1) / 2, (y + y1) / 2))
        br(x1, y1, a + rr.uniform(-.5, -.15), L * .7, w * .7, dd + 1); br(x1, y1, a + rr.uniform(.15, .5), L * .66, w * .7, dd + 1)
    br(80, 210, -.25, 64, 5, 0); br(90, 210, .3, 58, 4, 0)
    for (x, y) in pts: flowers(img, x, y, 10, 10, ['#f4a8c0', '#f8c8d8', '#e888a8'], 3, int(x * y) % 997, (5, 7), '#c83a5a')
    crock(img, 85, 294, 90, 92, '#e8e0cc', 360)
    for y in (230, 250): line(img, [(48, y), (122, y)], '#2a4a7a', 1.4)
    save(img, 'f_momo', 'Ветка персика в вазе', 'b', 60)

    img = canvas(150, 110); floor_shadow(img, 75, 104, 66)                                    # amazake
    part(img, LACQ, 370, [(10, 104), (140, 104), (136, 86), (14, 86)], k=.3, spec=.2)
    for k, x in enumerate((48, 104)):
        cup(img, x, 88, 44, 34, ['#3a5a7a', '#8a3a2a'][k], 371 + k * 3, '#f4f0e6')
        for j in range(2): soft(img, lambda dd, j=j, x=x: dd.ellipse([px(x - 10 + j * 8), px(20 - j * 8), px(x + 6 + j * 8), px(46 - j * 8)], fill=(235, 236, 238, 70)), 5)
    save(img, 'f_amazake', 'Амадзакэ в чашках', 'b', 30)

    img = canvas(220, 130); floor_shadow(img, 110, 124, 100)                                  # nagashibina boat
    for k in range(3): soft(img, lambda d, k=k: d.ellipse([px(20 - k * 10), px(104 + k * 6), px(200 + k * 10), px(124 + k * 4)], outline=(190, 215, 225, 120 - k * 30), width=px(1.5)), .5)
    m = part(img, '#c8a860', 380, cr([(20, 90), (110, 74), (200, 90), (170, 118), (110, 122), (50, 118)]), k=.35, scale=4, stretch=(4, .5))
    clip(img, m, lambda d: [d.line([(px(20), px(88 + k * 6)), (px(200), px(88 + k * 6))], fill=(110, 80, 40, 110), width=px(1)) for k in range(6)])
    doll(img, 86, 94, 58, '#2a3a6a', 381); doll(img, 134, 94, 58, '#c02a3a', 382, skirt='#e8c048')
    flowers(img, 46, 84, 10, 6, ['#f4a8c0', '#f8c8d8'], 4, 383, (5, 7), '#c83a5a'); flowers(img, 176, 84, 10, 6, ['#f4a8c0', '#f8c8d8'], 4, 384, (5, 7), '#c83a5a')
    save(img, 'f_r_nagashibina', 'Лодочка с куклами нагаси-бина', 'b', reward=True)


# ───────────────────────────── 4. Ханами ─────────────────────────────
def hanami():
    global FEST; FEST = 'hanami'
    img = canvas(180, 170); floor_shadow(img, 90, 164, 80)                                    # hanami bento in furoshiki
    for k in range(3): rect_part(img, LACQ, 401 + k, (26, 160 - (k + 1) * 34, 154, 160 - k * 34), k=.4, spec=.2)
    m = part(img, '#e8a0b4', 405, [(18, 162), (162, 162), (166, 80), (140, 60), (40, 60), (14, 80)], k=.35, scale=5, contrast=.6)
    flowers(img, 90, 110, 64, 40, ['#f8e8ee', '#fbd6e0'], 16, 406, (6, 8), '#e8c040')
    blob(img, [(56, 64), (78, 30), (92, 50), (106, 30), (126, 64), (90, 76)], hexc('#e094aa'), 407, scale=3)
    blob(img, [(40, 44), (70, 20), (84, 40), (70, 58)], hexc('#d888a0'), 408, scale=3); blob(img, [(140, 44), (110, 20), (96, 40), (110, 58)], hexc('#d888a0'), 409, scale=3)
    save(img, 'f_hanamibento', 'Ярусный ханами-бэнто в платке', 'b', 60)

    img = canvas(160, 90); floor_shadow(img, 80, 84, 72)                                      # sakura mochi
    plate(img, 80, 66, 150, '#f0ece2', '#3a5a8a')
    for k, x in enumerate((44, 80, 116)):
        leaf(img, x - 26, 64 - (k == 1) * 6, 52, 12, -.12, '#5a7a3a', 410 + k)
        ball(img, x, 54 - (k == 1) * 6, 20, 13, '#f0a8bc', 414 + k, spec=.3, k=.35)
    save(img, 'f_sakuramochi', 'Сакура-моти на блюде', 'b', 30)

    img = canvas(330, 90); floor_shadow(img, 165, 84, 158, 70)                                # picnic mat
    m = part(img, '#4a7aa8', 420, [(30, 20), (300, 20), (326, 84), (4, 84)], k=.25, scale=6, stretch=(6, .4), contrast=.6)
    clip(img, m, lambda d: [d.line([(0, px(20 + k * 8)), (px(330), px(20 + k * 8))], fill=(240, 240, 235, 80 if k % 2 else 30), width=px(2)) for k in range(9)])
    rr = random.Random(4)
    for _ in range(26): x, y = rr.uniform(30, 300), rr.uniform(28, 80); ell(img, (x - 3, y - 2, x + 3, y + 2), rr.choice(['#f4c4d2', '#f8dde4']))
    cup(img, 250, 60, 26, 18, '#7a3a2a', 421)
    save(img, 'f_hanamigoza', 'Циновка для пикника', 'b', 40)

    img = canvas(110, 260); floor_shadow(img, 55, 254, 40)                                    # bonbori
    rect_part(img, LACQ, 430, (30, 238, 80, 254), k=.3, spec=.2); line(img, [(55, 238), (55, 140)], '#1a1412', 4)
    m = part(img, '#f4e8cc', 431, [(18, 60), (92, 60), (86, 146), (24, 146)], k=.3, scale=4, contrast=.4)
    soft(img, lambda d: d.ellipse([px(22), px(66), px(88), px(140)], fill=(255, 210, 140, 110)), 10)
    for x, y in ((36, 96), (70, 84), (56, 124)): flowers(img, x, y, 8, 8, ['#e88aa8', '#f4a8c0'], 3, 432 + x, (4, 6), '#c83a5a')
    line(img, [(40, 70), (58, 110)], '#3a2418', 1.4); line(img, [(58, 110), (74, 90)], '#3a2418', 1.4)
    part(img, LACQ, 433, [(12, 60), (98, 60), (82, 44), (28, 44)], k=.3, spec=.2); rect_part(img, LACQ, 434, (20, 144, 90, 152), k=.3)
    save(img, 'f_bonbori_s', 'Фонарь бонбори с сакурой', 'b', 70, glow=[55, 100])

    img = canvas(130, 160); floor_shadow(img, 65, 154, 54)                                    # hanami dango
    part(img, '#c8a870', 440, [(24, 154), (106, 154), (100, 126), (30, 126)], k=.35, stretch=(3, .5))
    for k, (x, a) in enumerate(((40, -.2), (65, 0), (90, .2))):
        line(img, [(x, 130), (x + math.sin(a) * 120, 130 - math.cos(a) * 120)], '#c8a870', 2)
        for j, c in enumerate(('#5a9a4a', '#f4f0e8', '#ec8aa8')):
            yy = 112 - j * 26; ball(img, x + math.sin(a) * (130 - yy), yy, 13, 12, c, 441 + k * 3 + j, spec=.35, k=.4)
    save(img, 'f_hanamidango', 'Трёхцветные ханами-данго', 'b', 30)

    img = canvas(260, 360); floor_shadow(img, 130, 354, 80)                                   # sakura branch in jar
    rr = random.Random(21); pts = []
    def br(x, y, a, L, w, dd):
        if dd > 4 or L < 14: return
        x1, y1 = x + math.sin(a) * L, y - math.cos(a) * L; line(img, [(x, y), (x1, y1)], '#2e1c14', w); pts.extend([(x1, y1), ((x + x1) / 2, (y + y1) / 2)])
        br(x1, y1, a + rr.uniform(-.6, -.15), L * .72, w * .7, dd + 1); br(x1, y1, a + rr.uniform(.15, .6), L * .68, w * .7, dd + 1)
    br(122, 250, -.38, 74, 7, 0); br(138, 250, .36, 74, 6, 0); br(130, 250, .02, 70, 5, 1)
    for (x, y) in pts: flowers(img, x, y, 16, 14, ['#f4c4d2', '#f8dde4', '#e8a0b8'], 5, int(x * 7 + y) % 997, (5, 8), '#c8506a')
    blob(img, [(86, 354), (70, 300), (84, 250), (108, 236), (152, 236), (176, 250), (190, 300), (174, 354)], hexc('#4a6a8a'), 450, spec=.35)
    for y in (272, 300, 328): ImageDraw.Draw(img).arc([px(80), px(y - 10), px(180), px(y + 10)], 0, 180, fill=H('#e8e2d6'), width=px(1.6))
    save(img, 'f_r_sakuraeda', 'Цветущая ветка сакуры в кувшине', 'b', reward=True)


# ───────────────────────────── 5. Кодомо-но хи ─────────────────────────────
def kodomo():
    global FEST; FEST = 'kodomo'
    img = canvas(260, 520); floor_shadow(img, 40, 514, 40)                                    # koinobori
    rect_part(img, '#6a6d66', 501, (14, 490, 66, 514), k=.3)
    m = rect_part(img, '#b89a5a', 502, (34, 30, 46, 492), k=.4, stretch=(.3, 3))
    for y in range(60, 490, 48): line(img, [(34, y), (46, y)], '#6a5030', 2)
    for k in range(8):
        a = k / 8 * math.tau; line(img, [(40, 26), (40 + math.cos(a) * 18, 26 + math.sin(a) * 18)], ['#c02a2a', '#2a5a9a', '#e8c040', '#2f7a3a'][k % 4], 3)
    ball(img, 40, 26, 6, 6, GOLD, 503, spec=.5)
    for k, c in enumerate(('#c02a2a', '#f2eee4', '#2a5a9a', '#e8c040', '#2f7a3a')):
        part(img, c, 504 + k, [(46, 44 + k * 7), (240, 60 + k * 7), (236, 68 + k * 7), (46, 51 + k * 7)], k=.1, scale=2)
    carp(img, 48, 136, 190, 64, '#20242a', '#e8e0d0', 510, wave=.5)
    carp(img, 48, 226, 160, 54, '#c8321e', '#f2d8c8', 511, wave=.6)
    carp(img, 48, 306, 130, 44, '#2a5aa8', '#dde8f4', 512, wave=.7)
    save(img, 'f_koinobori', 'Шест с карпами коинобори', 'b', 150)

    img = canvas(220, 220); floor_shadow(img, 110, 214, 96)                                   # kabuto helmet
    part(img, LACQ, 520, [(30, 214), (190, 214), (180, 186), (40, 186)], k=.35, spec=.25)
    rect_part(img, LACQ_R, 521, (40, 178, 180, 188), k=.3)
    for k in range(4):
        y = 118 + k * 16; w = 70 + k * 12
        m = part(img, '#1c1c24', 522 + k, [(110 - w, y + 14), (110 + w, y + 14), (110 + w - 8, y), (110 - w + 8, y)], k=.4, spec=.2, scale=3)
        clip(img, m, lambda d, y=y: [d.line([(px(x), px(y)), (px(x), px(y + 14))], fill=H('#c02a2a'), width=px(2)) for x in range(20, 200, 10)])
    ball(img, 110, 104, 58, 46, '#26262e', 526, spec=.45, k=.55)
    for x in range(64, 160, 12): line(img, [(x, 64), (x + (x - 110) * .1, 140)], '#3a3a44', 1.2)
    rect_part(img, GOLD, 527, (60, 120, 160, 132), k=.3, spec=.4)
    for s in (-1, 1): part(img, GOLD, 528 + s, [(110 + s * 10, 70), (110 + s * 30, 70), (110 + s * 86, 6), (110 + s * 74, 4)], k=.3, spec=.55, scale=2)
    ball(img, 110, 66, 12, 12, GOLD, 530, spec=.6)
    save(img, 'f_kabuto', 'Шлем кабуто на подставке', 'b', 120)

    img = canvas(160, 100); floor_shadow(img, 80, 94, 72)                                     # kashiwa mochi
    plate(img, 80, 76, 150, '#e8e2d6', '#6a4a2a')
    for k, x in enumerate((46, 80, 114)):
        yy = 62 - (k == 1) * 6
        ball(img, x + 4, yy - 2, 20, 14, '#f4f0e8', 540 + k, spec=.25, k=.3)
        pts = [(x - 26, yy + 10), (x - 22, yy - 6), (x - 14, yy - 2), (x - 8, yy - 16), (x, yy - 8), (x + 6, yy - 18), (x + 10, yy + 12)]
        part(img, '#3a5a2a', 543 + k, pts, k=.4, scale=3); line(img, [(x - 22, yy + 6), (x + 6, yy - 10)], '#6a8a4a', 1.2)
    save(img, 'f_kashiwamochi', 'Касива-моти в дубовых листьях', 'b', 30)

    img = canvas(180, 260); floor_shadow(img, 90, 254, 70)                                    # iris
    rr = random.Random(8)
    for k in range(9):
        x = 50 + k * 10; top = rr.uniform(40, 120); lean = rr.uniform(-20, 20)
        part(img, rr.choice(['#2a5a2a', '#3a6a32', '#1e4a22']), 550 + k, [(x - 3, 200), (x + 3, 200), (x + lean + 1, top), (x + lean - 1, top + 4)], k=.2, scale=2)
    for k, (x, y) in enumerate(((66, 70), (112, 56), (92, 104), (134, 96))):
        line(img, [(x, y + 10), (x + rr.uniform(-6, 6), 200)], '#2f5a2a', 2.4)
        for a in (0, 2.1, 4.2):
            part(img, '#5a3aa8', 556 + k * 3 + int(a), [(x, y), (x + math.cos(a) * 22, y + math.sin(a) * 12 - 6), (x + math.cos(a + .5) * 24, y + math.sin(a + .5) * 14 + 8)], k=.3, scale=2)
        ell(img, (x - 4, y - 2, x + 4, y + 6), '#e8c040')
    part(img, WOOD_L, 570, [(34, 200), (146, 200), (138, 254), (42, 254)], k=.4, stretch=(.3, 3))
    for y in (210, 244): ImageDraw.Draw(img).rectangle([px(34), px(y - 3), px(146), px(y + 3)], fill=H('#2a2018'))
    save(img, 'f_shobu', 'Ирисы сёбу в кадке', 'b', 50)

    img = canvas(220, 240); floor_shadow(img, 110, 234, 96)                                   # kintaro on a carp
    rect_part(img, LACQ, 580, (24, 212, 196, 234), k=.3, spec=.2)
    for k in range(4): part(img, ['#2a5a8a', '#3a6a9a', '#4a7aaa', '#dde8f4'][k], 581 + k, [(20 + k * 8, 212), (60 + k * 10, 190 - k * 6), (100 + k * 6, 212)], k=.2, scale=2)
    blob(img, [(40, 200), (70, 150), (130, 130), (190, 140), (206, 110), (196, 170), (150, 196), (90, 206)], hexc('#c8321e'), 585, spec=.3)
    for i in range(4): ImageDraw.Draw(img).arc([px(90 + i * 22), px(150), px(114 + i * 22), px(174)], 90, 270, fill=(255, 230, 200, 140), width=px(1.6))
    ell(img, (66, 156, 82, 172), '#f2eee4'); ell(img, (71, 161, 77, 167), '#141010')
    ball(img, 120, 108, 32, 30, '#f0c8a8', 586, spec=.2, k=.3)
    part(img, '#c02a2a', 587, [(96, 92), (144, 92), (140, 138), (100, 138)], k=.3, scale=2); text(img, '金', 120, 114, 22, GOLD, SERIF)
    ball(img, 120, 62, 26, 24, '#f2d0b4', 588, spec=.2, k=.3)
    part(img, '#161212', 589, [(94, 58), (98, 38), (120, 30), (142, 38), (146, 58), (136, 48), (104, 48)], k=.3, scale=2)
    ell(img, (110, 60, 116, 66), '#1a1410'); ell(img, (126, 60, 132, 66), '#1a1410'); ImageDraw.Draw(img).arc([px(112), px(66), px(130), px(78)], 20, 160, fill=H('#a0402a'), width=px(2))
    for s in (-1, 1): ball(img, 120 + s * 36, 120, 10, 9, '#f0c8a8', 590 + s, spec=.2)
    save(img, 'f_r_kintaro', 'Кукла Кинтаро верхом на карпе', 'b', reward=True)


# ───────────────────────────── 6. Танабата ─────────────────────────────
def tanabata():
    global FEST; FEST = 'tanabata'
    img = canvas(260, 520); floor_shadow(img, 120, 514, 80)                                  # sasa with wishes
    rect_part(img, WOOD_D, 601, (80, 488, 160, 514), k=.3)
    line(img, [(120, 492), (126, 20)], '#6a8a3a', 7)
    for y in range(60, 490, 60): line(img, [(116, y), (130, y)], '#3a5a22', 2.5)
    rr = random.Random(12); tips = []
    for k in range(14):
        y = 50 + k * 30; s = 1 if k % 2 else -1; L = rr.uniform(60, 110); x1 = 124 + s * L; y1 = y + rr.uniform(10, 40)
        line(img, [(124, y), (x1, y1)], '#4a6a2a', 1.8); tips.append((x1, y1))
        for j in range(5): leaf(img, 124 + s * L * (.3 + j * .15), y + (y1 - y) * (.3 + j * .15), 30, 5, (0 if s > 0 else math.pi) + rr.uniform(.3, 1.2) * s, rr.choice(['#2a5a22', '#3a6a2a', '#1e4a1a']), 610 + k * 5 + j, vein=False)
    for k, (x, y) in enumerate(tips[::1]):
        c = ['#c02a2a', '#e8c040', '#2a5a9a', '#f2eee4', '#8a3aa8', '#2f7a3a'][k % 6]
        line(img, [(x, y), (x, y + 10)], '#e8e0d0', .8); rect_part(img, c, 700 + k, (x - 7, y + 10, x + 7, y + 58), k=.2, scale=2)
    for k in range(3):
        x, y = 60 + k * 70, 150 + k * 90; line(img, [(x, y - 20), (x, y)], '#e8e0d0', .8)
        spikes(img, x, y + 12, 14, 5, '#e8c040'); ell(img, (x - 6, y + 6, x + 6, y + 18), '#e8c040')
    save(img, 'f_sasa', 'Бамбук с желаниями тандзаку', 'b', 100)

    img = canvas(150, 360); line(img, [(75, 0), (75, 22)], '#3a2a1a', 1.8)                   # fukinagashi
    ball(img, 75, 60, 46, 40, '#e88aa8', 720, spec=.2, k=.3)
    flowers(img, 75, 60, 40, 34, ['#f4a8c0', '#f8dde4', '#e8c040', '#f2eee4'], 30, 721, (5, 8), '#c83a5a')
    for k, c in enumerate(('#c02a2a', '#e8c040', '#2a5a9a', '#f2eee4', '#2f7a3a', '#8a3aa8', '#e88aa8')):
        x = 36 + k * 13; pts = [(x - 5 + math.sin(y / 30 + k) * 5, y) for y in range(96, 356, 20)]
        pts2 = [(p[0] + 10, p[1]) for p in pts[::-1]]; part(img, c, 722 + k, pts + pts2, k=.15, scale=2)
    save(img, 'f_fukinagashi', 'Ленты фукинагаси', 't', 60)

    img = canvas(150, 190); line(img, [(20, 20), (130, 20)], '#8a6a3a', 2); line(img, [(75, 0), (75, 20)], '#3a2a1a', 1.5)   # kamigoromo
    m = part(img, '#e8a0b8', 730, [(20, 26), (130, 26), (130, 80), (110, 80), (106, 184), (44, 184), (40, 80), (20, 80)], k=.15, scale=4, contrast=.5)
    clip(img, m, lambda d: [d.polygon([(px(x), px(y)), (px(x + 8), px(y - 6)), (px(x + 16), px(y)), (px(x + 8), px(y + 6))], fill=(255, 245, 240, 170)) for x in range(24, 130, 20) for y in range(40, 184, 22)])
    poly(img, [(62, 26), (75, 70), (88, 26)], '#f2eee4'); line(img, [(62, 26), (75, 70), (88, 26)], '#8a3a4a', 1.4)
    rect_part(img, '#2a3a7a', 731, (44, 100, 106, 118), k=.2)
    save(img, 'f_kamigoromo', 'Бумажное кимоно камигоромо', 't', 30)

    img = canvas(170, 110); floor_shadow(img, 85, 104, 76)                                    # somen
    glass(img, [(14, 40), (156, 40), (130, 100), (40, 100)], 740, (180, 210, 225))
    rr = random.Random(2)
    for k in range(30): x = rr.uniform(30, 140); ImageDraw.Draw(img).arc([px(x - 20), px(44), px(x + 20), px(78)], 0, 180, fill=(250, 248, 240, 230), width=px(1.2))
    for k, (x, y, c) in enumerate(((50, 52, '#e8889a'), (90, 48, '#5a9a4a'), (122, 56, '#e8c040'))): spikes(img, x, y, 9, 5, c); ell(img, (x - 4, y - 4, x + 4, y + 4), c)
    for x in (64, 110): part(img, '#dff0f8', 741 + x, [(x, 46), (x + 12, 44), (x + 14, 56), (x + 2, 58)], k=.1, scale=2)
    save(img, 'f_somen', 'Холодная лапша сомэн со звёздочками', 'b', 30)

    img = canvas(160, 240); floor_shadow(img, 80, 234, 60)                                    # star river lantern
    for x in (30, 124): rect_part(img, LACQ, 750 + x, (x, 40, x + 8, 234), k=.3)
    m = part(img, '#1e2a5a', 752, [(36, 50), (126, 50), (126, 206), (36, 206)], k=.1, scale=5, contrast=.5)
    rr = random.Random(5)
    def stars(d):
        for _ in range(140):
            u = rr.random(); x = 36 + u * 90; y = 190 - u * 130 + rr.gauss(0, 14); r = rr.uniform(.6, 1.8)
            d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=(255, 245, 210, 230))
        for _ in range(30): x, y = rr.uniform(38, 124), rr.uniform(52, 204); d.ellipse([px(x - .7), px(y - .7), px(x + .7), px(y + .7)], fill=(220, 230, 255, 200))
    clip(img, m, stars)
    soft(img, lambda d: d.ellipse([px(46), px(80), px(116), px(180)], fill=(255, 230, 160, 60)), 12)
    rect_part(img, LACQ, 753, (24, 30, 138, 42), k=.3, spec=.2); rect_part(img, LACQ, 754, (24, 206, 138, 216), k=.3)
    save(img, 'f_r_hoshi', 'Фонарь «Звёздная река»', 'b', reward=True, glow=[80, 128])


# ───────────────────────────── 7. Обон ─────────────────────────────
def obon():
    global FEST; FEST = 'obon'
    img = canvas(240, 130); floor_shadow(img, 120, 124, 108)                                  # cucumber horse + eggplant cow
    plate(img, 120, 112, 226, '#6a8a4a', '#3a5a2a')
    for x in (30, 44, 76, 90): line(img, [(x, 70), (x - 2, 110)], '#e8dcc0', 2.4)
    blob(img, [(16, 66), (40, 50), (90, 48), (112, 58), (96, 74), (40, 76)], hexc('#3a7a2a'), 801, spec=.35, scale=3)
    rr = random.Random(1)
    for _ in range(18): x, y = rr.uniform(26, 100), rr.uniform(54, 72); ell(img, (x - 1.2, y - 1.2, x + 1.2, y + 1.2), '#a8c890')
    for x in (146, 160, 190, 204): line(img, [(x, 76), (x + 2, 112)], '#e8dcc0', 2.4)
    blob(img, [(136, 74), (150, 54), (190, 50), (222, 62), (220, 82), (180, 88)], hexc('#3a1a4a'), 802, spec=.5, scale=3)
    part(img, '#2f5a2a', 803, [(130, 68), (144, 54), (150, 66), (140, 78)], k=.3, scale=2)
    save(img, 'f_shoryouma', 'Огурец-лошадка и баклажан-бычок', 'b', 40)

    img = canvas(150, 300); line(img, [(75, 0), (75, 24)], '#3a2a1a', 2)                      # gifu bon lantern
    m = paper_lantern(img, 75, 44, 230, 110, '#e8eef2', 810, ribs=12, caps=LACQ)
    for (x, y) in ((56, 96), (96, 120), (66, 160), (98, 186)): flowers(img, x, y, 10, 10, ['#6a5ab8', '#8a7ad0'], 3, 811 + x, (6, 8), '#f2eee4', 5)
    line(img, [(40, 110), (70, 150), (58, 190)], '#3a6a3a', 1.4); line(img, [(100, 100), (90, 140)], '#3a6a3a', 1.4)
    part(img, LACQ, 812, [(54, 230), (96, 230), (84, 250), (66, 250)], k=.3, spec=.2)
    for k in range(9): line(img, [(66 + k * 2.2, 250), (64 + k * 2.6, 296)], ['#c02a2a', '#6a5ab8', '#e8c040'][k % 3], 1.4)
    save(img, 'f_bonchochin', 'Расписной бон-фонарь', 't', 90, glow=[75, 136])

    img = canvas(150, 120); floor_shadow(img, 75, 114, 66)                                    # mukaebi
    part(img, '#8a5a3a', 820, [(12, 90), (138, 90), (124, 114), (26, 114)], k=.4, scale=4)
    fill(img, '#5a3a24', 821, ell=(12, 82, 138, 98), scale=3)
    for k in range(7): line(img, [(30 + k * 6, 92), (110 - k * 4, 70 + k * 2)], '#e8dcc0', 2.2)
    for k in range(3):
        c = ['#e84a1a', '#f0902a', '#f8d060'][k]; w = 30 - k * 8; h = 56 - k * 14
        blob(img, [(75 - w, 86), (75 - w * .6, 86 - h * .5), (75, 86 - h), (75 + w * .6, 86 - h * .5), (75 + w, 86)], hexc(c), 822 + k, scale=2, k=.1, rim=.1)
    for k in range(3): soft(img, lambda d, k=k: d.ellipse([px(60 + k * 6), px(8 - k * 2), px(86 + k * 6), px(40 - k * 2)], fill=(200, 200, 205, 60)), 6)
    save(img, 'f_mukaebi', 'Костерок мукаэби на блюде', 'b', 40, glow=[75, 66])

    img = canvas(150, 150); floor_shadow(img, 75, 144, 66, 60)                                # toro nagashi
    for k in range(3): soft(img, lambda d, k=k: d.ellipse([px(10 - k * 8), px(122 + k * 5), px(140 + k * 8), px(144 + k * 3)], outline=(200, 220, 230, 140 - k * 40), width=px(1.6)), .5)
    part(img, WOOD, 830, [(22, 126), (128, 126), (120, 140), (30, 140)], k=.35, stretch=(3, .5))
    m = part(img, '#f4ecd8', 831, [(34, 52), (116, 52), (116, 126), (34, 126)], k=.25, scale=4, contrast=.4)
    soft(img, lambda d: d.ellipse([px(40), px(58), px(110), px(122)], fill=(255, 210, 130, 110)), 10)
    text(img, '灯', 75, 90, 30, '#6a2a1a', SERIF)
    for x in (34, 112): rect_part(img, WOOD_D, 832 + x, (x, 48, x + 4, 128), k=.2)
    rect_part(img, WOOD_D, 834, (30, 46, 120, 54), k=.2)
    save(img, 'f_toro', 'Бумажный фонарик торо-нагаси', 'b', 40, glow=[75, 90])

    img = canvas(130, 180); floor_shadow(img, 65, 174, 30)                                    # bon odori uchiwa
    line(img, [(65, 100), (65, 174)], '#c8a870', 5)
    m = part(img, '#f2eee4', 840, cr([(10, 60), (22, 18), (65, 4), (108, 18), (120, 60), (100, 100), (65, 112), (30, 100)]), k=.2, scale=4, contrast=.4)
    clip(img, m, lambda d: [d.line([(px(65), px(112)), (px(65 + math.cos(a) * 80), px(112 - math.sin(a) * 110))], fill=(160, 130, 80, 90), width=px(1)) for a in np.linspace(.2, math.pi - .2, 16)])
    ell(img, (26, 12, 104, 60), '#2a4a8a'); text(img, '盆踊', 65, 36, 20, '#f2eee4', SERIF)
    for k, x in enumerate((36, 65, 94)):
        ball(img, x, 70, 5, 5, '#1a1410', 841 + k, spec=0); line(img, [(x, 74), (x, 92)], '#c02a2a', 4); line(img, [(x, 78), (x + (-8 if k % 2 else 8), 70)], '#1a1410', 1.4)
    save(img, 'f_bonuchiwa', 'Веер бон-одори', 'b', 30)

    img = canvas(150, 300); floor_shadow(img, 75, 294, 50)                                    # lantern that guides spirits
    rect_part(img, LACQ, 850, (40, 274, 110, 294), k=.3, spec=.2); line(img, [(75, 274), (75, 200)], '#1a1412', 4)
    paper_lantern(img, 75, 60, 204, 104, '#f0ecdc', 851, ribs=10, caps=LACQ, lit=False)
    soft(img, lambda d: d.ellipse([px(40), px(80), px(110), px(190)], fill=(150, 230, 220, 110)), 12)
    for k in range(3): blob(img, [(75 - 18 + k * 6, 170), (75 - 10 + k * 5, 130), (75 + k * 3, 106 + k * 8), (75 + 12, 140), (75 + 16 - k * 4, 170)], hexc(['#7ad8c8', '#a8f0e0', '#e8fff8'][k]), 852 + k, scale=2, k=.1, rim=.1)
    part(img, LACQ, 855, [(40, 60), (110, 60), (96, 44), (54, 44)], k=.3, spec=.2); line(img, [(75, 44), (75, 20)], '#1a1412', 2); ell(img, (68, 12, 82, 26), GOLD)
    save(img, 'f_r_hitodama', 'Фонарь, что ведёт духов домой', 'b', reward=True, glow=[75, 138])


# ───────────────────────────── 8. Цукими ─────────────────────────────
def tsukimi():
    global FEST; FEST = 'tsukimi'
    img = canvas(170, 170); floor_shadow(img, 85, 164, 74)                                    # tsukimi dango pyramid
    top = sanbo(img, 85, 164, 150, 901)
    part(img, '#f4f0e8', 902, [(22, top + 2), (85, top - 12), (148, top + 2), (85, top + 8)], k=.1, scale=3)
    r = 14; k0 = 0
    for row, n in enumerate((4, 3, 2, 1)):
        for j in range(n):
            x = 85 + (j - (n - 1) / 2) * r * 2; y = top - r - row * r * 1.7
            ball(img, x, y, r, r * .95, '#f6f2ea', 903 + k0, spec=.35, k=.4); k0 += 1
    save(img, 'f_tsukimidango', 'Пирамида цукими-данго', 'b', 40)

    img = canvas(190, 360); floor_shadow(img, 95, 354, 56)                                    # susuki pampas
    rr = random.Random(31)
    for k in range(9):
        a = -.44 + k * .11 + rr.uniform(-.04, .04); L = rr.uniform(150, 195); x0, y0 = 95, 270
        pts = [(x0 + math.sin(a) * L * u + math.sin(a) * (u ** 2) * 40, y0 - math.cos(a) * L * u) for u in np.linspace(0, 1, 8)]
        line(img, pts, '#8a8a5a', 1.6)
        tx, ty = pts[-1]; hx, hy = pts[-3]; ang = math.atan2(ty - hy, tx - hx) + (.35 if a > 0 else -.35)
        leaf(img, hx, hy, 52, 8, ang, rr.choice(['#d8ccb0', '#e2d8bc', '#cbbf9e']), 900 + k, vein=False)
        for j in range(16):
            u = rr.uniform(.1, 1); x = hx + math.cos(ang) * 52 * u; y = hy + math.sin(ang) * 52 * u; s2 = 1 if j % 2 else -1
            line(img, [(x, y), (x + math.cos(ang + s2 * .6) * 12, y + math.sin(ang + s2 * .6) * 12 + 3)], rr.choice(['#f2ecd8', '#e8e0c8', '#c8b890']), 1)
    for k in range(6): leaf(img, 95, 270, rr.uniform(70, 110), 3, -math.pi / 2 + rr.uniform(-1, 1), '#3a4a2a', 910 + k, vein=False)
    crock(img, 95, 354, 96, 92, '#6a5a4a', 920)
    save(img, 'f_susuki', 'Мискант сусуки в кувшине', 'b', 50)

    img = canvas(180, 190); floor_shadow(img, 90, 184, 80)                                    # moon rabbit with mortar
    figure_base(img, 90, 184, 170, '#5a5c56', 930)
    part(img, WOOD, 931, [(94, 158), (156, 158), (150, 116), (100, 116)], k=.4, stretch=(.3, 3)); fill(img, '#f4f0e8', 932, ell=(98, 108, 152, 124), scale=3)
    blob(img, [(40, 158), (32, 120), (48, 90), (78, 84), (92, 110), (88, 158)], hexc('#f2eee8'), 933, spec=.2)
    blob(img, [(46, 94), (40, 64), (60, 50), (80, 62), (80, 90)], hexc('#f4f0ea'), 934, spec=.2)
    for s, x in ((-1, 50), (1, 62)): blob(img, [(x - 6, 58), (x - 10, 18), (x, 8), (x + 6, 20), (x + 4, 58)], hexc('#f2eee8'), 935 + s, scale=2)
    for x in (50, 62): line(img, [(x - 2, 20), (x, 52)], '#e8a8b4', 2.4)
    ell(img, (64, 68, 72, 76), '#b02a3a'); ell(img, (76, 78, 80, 82), '#e8a0b0')
    line(img, [(84, 100), (128, 60)], WOOD_D, 5); rect_part(img, WOOD_D, 936, (116, 44, 142, 64), k=.3)
    save(img, 'f_tsukiusagi', 'Лунный кролик со ступкой', 'b', 80)

    img = canvas(180, 110); floor_shadow(img, 90, 104, 80)                                    # chestnuts and sweet potato
    part(img, '#b8905a', 940, [(8, 80), (172, 80), (160, 104), (20, 104)], k=.3, stretch=(3, .5)); fill(img, '#9a7040', 941, ell=(8, 70, 172, 90), scale=4)
    blob(img, [(20, 76), (40, 56), (84, 50), (104, 60), (88, 78), (40, 84)], hexc('#8a2a4a'), 942, spec=.35, scale=3)
    fill(img, '#f0c84a', 943, ell=(90, 56, 106, 76), scale=2)
    rr = random.Random(6)
    for k in range(6):
        x, y = 110 + (k % 3) * 20, 70 - (k // 3) * 14
        blob(img, [(x - 11, y + 7), (x - 11, y - 2), (x - 3, y - 11), (x, y - 14), (x + 3, y - 11), (x + 11, y - 2), (x + 11, y + 7), (x, y + 10)], hexc('#6a2e14'), 944 + k, spec=.55, scale=2)
        ell(img, (x - 9, y + 2, x + 9, y + 10), '#c8a070')
    save(img, 'f_kuri', 'Каштаны и батат на подносе', 'b', 30)

    img = canvas(180, 260); line(img, [(90, 0), (90, 40)], '#3a2a1a', 2)                      # full moon lamp
    rect_part(img, LACQ, 960, (74, 36, 106, 46), k=.3, spec=.2)
    ball(img, 90, 140, 84, 92, '#f4dc98', 961, spec=.25, k=.25, rim=.3, contrast=.6)
    rr = random.Random(9)
    for _ in range(8): x, y, r = rr.uniform(40, 140), rr.uniform(70, 210), rr.uniform(6, 16); soft(img, lambda d, x=x, y=y, r=r: d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=(190, 150, 80, 70)), 2)
    blob(img, [(70, 170), (66, 140), (82, 126), (100, 140), (104, 170)], hexc('#b89050'), 962, scale=2, k=.1)
    for x in (78, 88): blob(img, [(x - 4, 128), (x - 3, 100), (x + 2, 96), (x + 4, 128)], hexc('#b89050'), 963 + x, scale=2, k=.1)
    soft(img, lambda d: d.ellipse([px(0), px(50), px(180), px(230)], outline=(255, 230, 160, 60), width=px(8)), 10)
    save(img, 'f_moonlamp', 'Фонарь «Полная луна»', 't', 90, glow=[90, 140])

    def moon(box):
        x0, y0, x1, y1 = box; w = x1 - x0
        fill(img, '#2a2e3a', 970, rect=box, scale=6, contrast=.4)
        ball(img, x0 + w * .5, y0 + 70, 46, 46, '#f4dc98', 971, spec=.2, k=.2)
        for k, sx in enumerate((-1, 1)):
            cx = x0 + w * .5 + sx * 20; blob(img, [(cx - 9, y0 + 100), (cx - 10, y0 + 84), (cx, y0 + 78), (cx + 10, y0 + 86), (cx + 9, y0 + 100)], hexc('#9a7a40'), 972 + k, scale=2, k=.1)
            for e in (-3, 3): line(img, [(cx + e, y0 + 80), (cx + e * 2 - sx * 4, y0 + 58)], '#9a7a40', 3.4)
            line(img, [(cx - sx * 6, y0 + 88), (x0 + w * .5 + sx * 4, y0 + 70)], '#6a4a2a', 2.4)
        part(img, '#6a4a2a', 975, [(x0 + w * .5 - 9, y0 + 92), (x0 + w * .5 + 9, y0 + 92), (x0 + w * .5 + 7, y0 + 106), (x0 + w * .5 - 7, y0 + 106)], k=.1, scale=2)
        rr = random.Random(3)
        for k in range(14):
            a = -.7 + k * .1; L = rr.uniform(60, 110); bx = x0 + 10 + k * 7
            line(img, [(bx, y1), (bx + math.sin(a) * L, y1 - math.cos(a) * L)], '#9a9070', 1.2)
            line(img, [(bx + math.sin(a) * L, y1 - math.cos(a) * L), (bx + math.sin(a) * L * .85 + 5, y1 - math.cos(a) * L * .85)], '#e8e0c8', 2.4)
        text(img, '月見', x0 + w * .5, y0 + 150, 18, '#e8e0c8', SERIF)
    kakejiku(img := canvas(170, 330), 170, 330, 976, moon)
    save(img, 'f_r_tsuki', 'Свиток «Кролики толкут моти на луне»', 't', reward=True)


# ───────────────────────────── 9. Сити-го-сан ─────────────────────────────
def shichigosan():
    global FEST; FEST = 'shichigosan'
    img = canvas(100, 280); floor_shadow(img, 50, 274, 36)                                    # chitose ame bag
    for k, (x, c) in enumerate(((36, '#c02a2a'), (50, '#f2eee4'), (64, '#c02a2a'))): rect_part(img, c, 1001 + k, (x - 5, 10 + k * 6, x + 5, 90), k=.3, spec=.4)
    m = part(img, '#f2eee4', 1004, [(16, 70), (84, 70), (84, 274), (16, 274)], k=.3, scale=4, contrast=.4)
    rect_part(img, '#c02a2a', 1005, (16, 70, 84, 90), k=.2)
    for k, ch in enumerate('千歳飴'): text(img, ch, 50, 120 + k * 22, 18, '#1a1410', SERIF)
    poly(img, [(24, 212), (40, 200), (56, 212), (40, 206)], '#1a1410'); line(img, [(40, 206), (40, 222)], '#1a1410', 1.2)
    ball(img, 62, 246, 12, 8, '#3a6a3a', 1006, spec=.3); ell(img, (72, 244, 78, 250), '#3a6a3a')
    ell(img, (26, 196, 36, 206), '#c02a2a')
    save(img, 'f_chitose', 'Пакет конфет титосэ-амэ', 'b', 40)

    img = canvas(140, 140); floor_shadow(img, 70, 134, 56)                                    # tsumami kanzashi
    part(img, '#6a2a3a', 1010, [(18, 134), (122, 134), (114, 112), (26, 112)], k=.35, scale=3)
    for k, (x, y, c) in enumerate(((52, 52, '#e8506a'), (86, 46, '#f4a8c0'), (70, 76, '#f2eee4'), (40, 82, '#e8c040'), (100, 80, '#e8506a'))):
        for j in range(8):
            a = j / 8 * math.tau; part(img, c, 1011 + k * 8 + j, [(x, y), (x + math.cos(a - .3) * 16, y + math.sin(a - .3) * 16), (x + math.cos(a) * 22, y + math.sin(a) * 22), (x + math.cos(a + .3) * 16, y + math.sin(a + .3) * 16)], k=.3, scale=2)
        ell(img, (x - 4, y - 4, x + 4, y + 4), GOLD)
    for k in range(5): x = 44 + k * 13; line(img, [(x, 94), (x + 2, 118)], '#c8a040', 1); ell(img, (x - 3, 116, x + 5, 124), '#e8506a')
    save(img, 'f_tsumami', 'Цумами-кандзаси с шёлковыми цветами', 'b', 60)

    img = canvas(130, 150); floor_shadow(img, 65, 144, 54)                                    # kinchaku
    m = blob(img, [(22, 144), (14, 100), (30, 52), (65, 40), (100, 52), (116, 100), (108, 144)], hexc('#b02a3a'), 1030, spec=.2)
    rr = random.Random(4)
    clip(img, m, lambda d: [d.polygon([(px(x), px(y - 4)), (px(x + 4), px(y)), (px(x), px(y + 4)), (px(x - 4), px(y))], fill=H('#e8c060')) for x, y in [(rr.uniform(20, 110), rr.uniform(56, 140)) for _ in range(34)]])
    for x in range(34, 100, 8): line(img, [(x, 46), (x + 2, 64)], dk(H('#b02a3a'), .3), 1)
    line(img, [(40, 56), (26, 20), (65, 34), (104, 20), (90, 56)], '#e8c040', 2.4)
    for x in (26, 104): ball(img, x, 20, 7, 7, '#e8c040', 1031 + x, spec=.4)
    save(img, 'f_kinchaku', 'Праздничный мешочек кинтяку', 'b', 40)

    img = canvas(140, 150); floor_shadow(img, 70, 144, 56)                                    # silk temari on stand
    part(img, LACQ, 1040, [(26, 144), (114, 144), (104, 124), (36, 124)], k=.35, spec=.2)
    m = Image.new('RGBA', img.size, (0, 0, 0, 0)); fill(m, '#f2eee4', 1041, ell=(20, 20, 120, 126), scale=3, contrast=.4); mk = mask_poly(img, ell=(20, 20, 120, 126))
    def threads(d):
        for k in range(12):
            a = k / 12 * math.pi; c = ['#c02a2a', '#2a5a9a', '#e8c040', '#2f7a3a'][k % 4]
            d.line([(px(70 + math.cos(a) * 52), px(73 + math.sin(a) * 54)), (px(70 - math.cos(a) * 52), px(73 - math.sin(a) * 54))], fill=H(c), width=px(3))
        d.ellipse([px(52), px(55), px(88), px(91)], outline=H('#c02a2a'), width=px(4))
    clip(m, mk, threads); volume(m, (20, 20, 120, 126), .5, .45, spec=.25); img.alpha_composite(m)
    save(img, 'f_temari753', 'Шёлковый тэмари на подставке', 'b', 50)

    img = canvas(200, 330); floor_shadow(img, 100, 324, 70)                                   # umbrella with crane and turtle
    line(img, [(100, 120), (104, 324)], '#3a2418', 4); rect_part(img, '#c02a2a', 1050, (98, 280, 108, 322), k=.3)
    m = part(img, '#c8322e', 1051, [(4, 130)] + [(100 + math.cos(a) * 96, 130 - math.sin(a) * 118) for a in np.linspace(math.pi, 0, 22)] + [(196, 130), (100, 146)], k=.35, rim=.25, scale=4, contrast=.5)
    clip(img, m, lambda d: [d.line([(px(100), px(12)), (px(100 + math.cos(a) * 100), px(130 - math.sin(a) * 30 + 10))], fill=(90, 20, 14, 120), width=px(1.2)) for a in np.linspace(math.pi, 0, 14)])
    clip(img, m, lambda d: d.ellipse([px(70), px(30), px(130), px(90)], outline=(245, 238, 225, 230), width=px(5)))
    poly(img, [(40, 80), (62, 64), (84, 72), (70, 78), (60, 92)], '#f2eee4'); ell(img, (58, 60, 66, 68), '#c02a2a')
    ball(img, 150, 96, 16, 11, '#3a5a3a', 1052, spec=.3); ell(img, (162, 88, 172, 98), '#3a5a3a')
    save(img, 'f_r_753', 'Зонтик с журавлём и черепахой', 'b', reward=True)


# ───────────────────────────── 10. Тодзи ─────────────────────────────
def toji():
    global FEST; FEST = 'toji'
    img = canvas(190, 130); floor_shadow(img, 95, 124, 86)                                    # tub with yuzu
    m = part(img, WOOD_L, 1101, [(14, 60), (176, 60), (164, 124), (26, 124)], k=.4, stretch=(.3, 3))
    clip(img, m, lambda d: [d.line([(px(x), px(60)), (px(x + (x - 95) * -.06), px(124))], fill=(60, 40, 20, 80), width=px(1)) for x in range(24, 176, 14)])
    for y in (72, 112): ImageDraw.Draw(img).rectangle([px(18), px(y - 3), px(172), px(y + 3)], fill=H('#2a2018'))
    fill(img, '#9ab8c0', 1102, ell=(14, 50, 176, 72), scale=3, contrast=.3)
    for k, (x, y) in enumerate(((50, 50), (84, 44), (120, 48), (150, 54), (66, 60), (104, 60), (136, 64))):
        ball(img, x, y, 16, 14, '#f0c830', 1103 + k, spec=.45, k=.45)
        ell(img, (x - 2, y - 14, x + 2, y - 10), '#5a6a2a')
    save(img, 'f_yuzuoke', 'Кадка с юдзу', 'b', 40)

    img = canvas(170, 120); floor_shadow(img, 85, 114, 76)                                    # kabocha on a plate
    plate(img, 85, 100, 160, '#e8e2d6', '#2a4a7a')
    blob(img, [(34, 94), (30, 70), (52, 50), (85, 44), (118, 50), (140, 70), (136, 94), (85, 102)], hexc('#2a4a2a'), 1110, spec=.35, scale=3)
    for dx in (-40, -22, -6, 10, 26, 42):
        line(img, [(85 + dx * .2, 50), (85 + dx * .9, 60), (85 + dx, 78), (85 + dx * .9, 96)], '#1a2e1a', 1.4)
    rr = random.Random(5)
    for _ in range(24): x, y = rr.uniform(40, 130), rr.uniform(56, 96); ell(img, (x - 1.2, y - 1.2, x + 1.2, y + 1.2), '#5a7a4a')
    rect_part(img, '#5a4a2a', 1116, (81, 34, 89, 50), k=.3)
    for k, x in enumerate((38, 132)): part(img, '#f09a2a', 1117 + k, [(x - 16, 104), (x + 16, 104), (x + 11, 90), (x - 11, 90)], k=.3, scale=2); line(img, [(x - 12, 91), (x + 12, 91)], '#2a4a2a', 2.4)
    save(img, 'f_kabocha', 'Тыква кабоча на тарелке', 'b', 30)

    img = canvas(150, 200); line(img, [(30, 40), (75, 4), (120, 40)], '#8a6a3a', 1.6)          # yuzuyu sign
    rect_part(img, WOOD_L, 1120, (20, 40, 130, 196), k=.35, stretch=(.3, 3))
    ImageDraw.Draw(img).rectangle([px(26), px(46), px(124), px(190)], outline=H(WOOD_D), width=px(2))
    for k, ch in enumerate('ゆず湯'): text(img, ch, 60, 74 + k * 36, 28, '#1a1410', SERIF, brush=True)
    ball(img, 104, 160, 14, 13, '#f0c830', 1121, spec=.4); leaf(img, 104, 148, 18, 5, -1.2, '#3a5a2a', 1122)
    save(img, 'f_yuzuyu', 'Табличка «Юдзу-ю»', 't', 30)

    img = canvas(150, 170); floor_shadow(img, 75, 164, 56)                                    # yuzu lantern
    rect_part(img, WOOD_D, 1130, (40, 146, 110, 164), k=.3)
    ball(img, 75, 92, 58, 54, '#f4c830', 1131, spec=.2, k=.25, contrast=.7)
    rr = random.Random(2)
    for _ in range(40): x, y = rr.uniform(26, 124), rr.uniform(46, 140); ell(img, (x - 1.4, y - 1.4, x + 1.4, y + 1.4), '#c89a20')
    soft(img, lambda d: d.ellipse([px(40), px(58), px(110), px(126)], fill=(255, 240, 170, 120)), 10)
    rect_part(img, '#4a5a2a', 1132, (70, 32, 80, 42), k=.3); leaf(img, 78, 36, 36, 9, -.5, '#3a6a2a', 1133)
    save(img, 'f_r_yuzu', 'Юдзу-фонарик', 'b', reward=True, glow=[75, 92])


# ───────────────────────────── Подарки гостей ─────────────────────────────
def gifts():
    G = lambda iid, name, who, gl, anchor='b', glow=None: save(img, iid, name, anchor, glow=glow, gift=who, gl=gl)
    img = canvas(150, 90); floor_shadow(img, 75, 84, 64)                                      # kappa: plate
    part(img, '#6a2a3a', 1201, [(20, 84), (130, 84), (124, 66), (26, 66)], k=.3, scale=3)
    ball(img, 75, 56, 60, 18, '#c8d8c8', 1202, spec=.4, k=.4)
    fill(img, '#6a9aa0', 1203, ell=(28, 44, 122, 66), scale=3, contrast=.4); soft(img, lambda d: d.ellipse([px(46), px(48), px(80), px(56)], fill=(255, 255, 255, 140)), 2)
    G('gf_kappa_sara', 'Блюдце с макушки каппы', 'kappa', 1)
    img = canvas(170, 130); floor_shadow(img, 85, 124, 76)                                    # kappa: basket of cucumbers
    for k in range(6): blob(img, [(30 + k * 18, 70), (40 + k * 18, 20 + (k % 2) * 10), (52 + k * 18, 22 + (k % 2) * 10), (46 + k * 18, 72)], hexc('#2f6a2a'), 1210 + k, spec=.35, scale=2)
    m = part(img, '#b8964e', 1216, [(14, 60), (156, 60), (140, 124), (30, 124)], k=.4, scale=3)
    clip(img, m, lambda d: [d.line([(0, px(y)), (px(170), px(y))], fill=(90, 60, 20, 150), width=px(1.6)) for y in range(64, 124, 7)] + [d.line([(px(x), px(60)), (px(x), px(124))], fill=(90, 60, 20, 90), width=px(1.2)) for x in range(20, 160, 12)])
    G('gf_kappa_kyuri', 'Корзинка речных огурцов', 'kappa', 2)
    def kp(box):
        x0, y0, x1, y1 = box; cx = (x0 + x1) / 2
        blob(img, [(cx - 22, y0 + 110), (cx - 26, y0 + 60), (cx, y0 + 40), (cx + 26, y0 + 60), (cx + 22, y0 + 110)], hexc('#3a7a3a'), 1220, scale=2, k=.2)
        fill(img, '#c8d8c8', 1221, ell=(cx - 16, y0 + 36, cx + 16, y0 + 46), scale=2); poly(img, [(cx - 5, y0 + 64), (cx + 5, y0 + 64), (cx, y0 + 72)], '#e8a030')
        ell(img, (cx - 12, y0 + 52, cx - 6, y0 + 58), '#1a1410'); ell(img, (cx + 6, y0 + 52, cx + 12, y0 + 58), '#1a1410')
        text(img, '河童', cx, y0 + 140, 20, '#1a1410', SERIF, brush=True); text(img, '秘薬', cx, y0 + 168, 16, '#8a2a1a', SERIF)
    kakejiku(img := canvas(150, 260), 150, 260, 1222, kp)
    G('gf_kappa_scroll', 'Свиток «Мазь каппы»', 'kappa', 3, 't')

    img = canvas(120, 150); floor_shadow(img, 60, 144, 46)                                    # kitsune: hoshi no tama
    part(img, '#c02a2a', 1230, [(24, 144), (96, 144), (88, 122), (32, 122)], k=.35, scale=3)
    soft(img, lambda d: d.ellipse([px(14), px(20), px(106), px(128)], fill=(230, 240, 255, 80)), 12)
    blob(img, [(30, 110), (26, 80), (44, 56), (60, 20), (64, 50), (82, 60), (94, 84), (90, 110), (60, 122)], hexc('#e8eef4'), 1231, spec=.6, k=.4)
    for k in range(3): line(img, [(40 + k * 10, 110), (54 + k * 8, 60 - k * 10)], '#c8d8ec', 1.4)
    G('gf_kitsune_tama', 'Лисья жемчужина хоси-но-тама', 'kitsune', 1, glow=[60, 86])
    img = canvas(200, 260); floor_shadow(img, 100, 254, 70)                                   # kitsune: wedding umbrella
    line(img, [(100, 90), (104, 254)], '#3a2418', 4)
    m = part(img, '#b8201a', 1240, [(6, 100)] + [(100 + math.cos(a) * 94, 100 - math.sin(a) * 92) for a in np.linspace(math.pi, 0, 22)] + [(194, 100), (100, 114)], k=.35, rim=.25, scale=4, contrast=.5)
    clip(img, m, lambda d: [d.line([(px(100), px(8)), (px(100 + math.cos(a) * 100), px(110))], fill=(80, 14, 10, 130), width=px(1.2)) for a in np.linspace(math.pi, 0, 14)])
    clip(img, m, lambda d: d.ellipse([px(76), px(20), px(124), px(68)], outline=(245, 238, 225, 230), width=px(5)))
    for s in (-1, 1): poly(img, [(100 + s * 8, 34), (100 + s * 18, 22), (100 + s * 16, 44)], '#f2eee4')
    ell(img, (90, 38, 110, 56), '#f2eee4')
    G('gf_kitsune_kasa', 'Свадебный зонтик лис', 'kitsune', 2)
    img = canvas(150, 150); line(img, [(40, 40), (75, 6), (110, 40)], '#c02a2a', 2)            # kitsune: fox ema
    part(img, '#e8d0a0', 1250, [(20, 30), (48, 60), (102, 60), (130, 30), (126, 90), (100, 128), (75, 142), (50, 128), (24, 90)], k=.3, stretch=(3, .5), scale=4)
    for s in (-1, 1): poly(img, [(75 + s * 38, 44), (75 + s * 50, 38), (75 + s * 48, 64)], '#c02a2a')
    for s in (-1, 1): line(img, [(75 + s * 10, 88), (75 + s * 30, 80)], '#c02a2a', 3)
    ell(img, (70, 124, 80, 132), '#1a1410'); text(img, '稲荷', 75, 106, 16, '#1a1410', SERIF)
    G('gf_kitsune_ema', 'Эма с лисьей мордочкой', 'kitsune', 3, 't')

    img = canvas(180, 170); floor_shadow(img, 90, 164, 80)                                    # tanuki: bunbuku kettle
    ball(img, 84, 112, 62, 52, '#2a2a2c', 1260, spec=.4, k=.55)
    rect_part(img, '#3a3a3e', 1261, (54, 56, 114, 66), k=.3); ImageDraw.Draw(img).arc([px(50), px(20), px(118), px(80)], 180, 360, fill=H('#2a2a2c'), width=px(4))
    blob(img, [(140, 110), (170, 90), (176, 120), (150, 140)], hexc('#6a4a2a'), 1262, scale=3)
    for k in range(3): line(img, [(150 + k * 6, 98 + k * 4), (158 + k * 6, 126 - k * 2)], '#2a1a10', 2)
    blob(img, [(4, 100), (14, 78), (34, 74), (44, 94), (30, 116)], hexc('#8a6a42'), 1263, scale=3)
    ell(img, (14, 86, 38, 104), '#2a1e14'); ell(img, (20, 90, 26, 96), '#f2eee4'); ell(img, (6, 94, 12, 100), '#1a1410')
    for s in (-1, 1): blob(img, [(60 + s * 20, 160), (54 + s * 20, 144), (68 + s * 20, 140), (72 + s * 20, 160)], hexc('#6a4a2a'), 1264 + s, scale=2)
    G('gf_tanuki_kettle', 'Чайник-оборотень бумбуку', 'tanuki', 1)
    img = canvas(120, 150); floor_shadow(img, 60, 144, 44)                                    # tanuki: transformation leaf
    part(img, WOOD_D, 1270, [(30, 144), (90, 144), (84, 126), (36, 126)], k=.3); line(img, [(60, 126), (60, 100)], '#4a3a1a', 3)
    leaf(img, 60, 104, 92, 30, -math.pi / 2 - .05, '#4a8a3a', 1271)
    for k in range(4): line(img, [(60, 88 - k * 18), (40 + k * 2, 76 - k * 18)], '#7aaa5a', 1); line(img, [(60, 88 - k * 18), (80 - k * 2, 76 - k * 18)], '#7aaa5a', 1)
    soft(img, lambda d: d.ellipse([px(30), px(10), px(90), px(80)], fill=(240, 250, 200, 40)), 10)
    G('gf_tanuki_leaf', 'Лист превращений на подставке', 'tanuki', 2)
    img = canvas(180, 90); floor_shadow(img, 90, 84, 82)                                      # tanuki: straw hat
    m = blob(img, [(6, 74), (40, 54), (90, 18), (140, 54), (174, 74), (90, 86)], hexc('#c8a860'), 1280, scale=3, k=.45)
    clip(img, m, lambda d: [d.line([(px(90), px(18)), (px(90 + math.cos(a) * 110), px(18 + math.sin(a) * 70))], fill=(120, 90, 40, 120), width=px(1.2)) for a in np.linspace(.2, math.pi - .2, 18)])
    rect_part(img, '#6a2a1a', 1281, (60, 56, 120, 62), k=.2)
    G('gf_tanuki_hat', 'Соломенная шляпа тануки', 'tanuki', 3)

    img = canvas(120, 120); floor_shadow(img, 60, 114, 46)                                    # nekomata: bell with two cords
    for s in (-1, 1): line(img, [(60, 40), (60 + s * 20, 8), (60 + s * 40, 30), (60 + s * 48, 12)], '#c02a2a', 4)
    ball(img, 60, 74, 36, 36, '#d8b048', 1290, spec=.6, k=.5)
    line(img, [(26, 74), (94, 74)], '#8a6a2a', 2); ell(img, (54, 82, 66, 96), '#2a1a10'); line(img, [(60, 90), (60, 108)], '#2a1a10', 2)
    G('gf_neko_suzu', 'Бубенчик на два хвоста', 'nekomata', 1)
    img = canvas(180, 200); line(img, [(20, 20), (160, 20)], '#8a6a3a', 2); line(img, [(90, 0), (90, 20)], '#3a2a1a', 1.5)   # nekomata: tenugui
    m = part(img, '#2a3a6a', 1300, [(24, 22), (156, 22), (152, 196), (28, 194)], k=.15, scale=4, contrast=.6)
    def cats(d):
        for (x, y, s) in ((60, 70, 1), (120, 110, -1), (70, 160, 1)):
            d.ellipse([px(x - 12), px(y - 10), px(x + 12), px(y + 14)], fill=(242, 238, 228, 230)); d.ellipse([px(x - 9), px(y - 24), px(x + 9), px(y - 6)], fill=(242, 238, 228, 230))
            for e in (-1, 1): d.polygon([(px(x + e * 8), px(y - 20)), (px(x + e * 10), px(y - 30)), (px(x + e * 3), px(y - 22))], fill=(242, 238, 228, 230))
            d.line([(px(x - 10), px(y)), (px(x - 22), px(y - 14))], fill=(242, 238, 228, 230), width=px(3)); d.line([(px(x + 10), px(y)), (px(x + 20), px(y - 16))], fill=(242, 238, 228, 230), width=px(3))
            for t in (-1, 1): d.line([(px(x + s * 10), px(y + 10)), (px(x + s * 26), px(y + 4 + t * 8))], fill=(242, 238, 228, 230), width=px(2))
    clip(img, m, cats)
    G('gf_neko_tenugui', 'Тэнугуи для кошачьих танцев', 'nekomata', 2, 't')
    img = canvas(130, 180); floor_shadow(img, 65, 174, 46)                                    # nekomata: cat lantern
    rect_part(img, LACQ, 1310, (34, 158, 96, 174), k=.3)
    for s in (-1, 1): part(img, '#f0e4c8', 1311 + s, [(65 + s * 16, 50), (65 + s * 46, 20), (65 + s * 44, 66)], k=.3, scale=2)
    paper_lantern(img, 65, 40, 160, 104, '#f2e6c8', 1313, ribs=8, caps='#2a1a10')
    for s in (-1, 1): part(img, '#1a1410', 1314 + s, [(65 + s * 12, 88), (65 + s * 28, 84), (65 + s * 24, 100)], k=.1, scale=2)
    poly(img, [(60, 106), (70, 106), (65, 112)], '#c05a6a')
    for s in (-1, 1):
        for t in (-1, 0, 1): line(img, [(65 + s * 12, 112 + t * 4), (65 + s * 38, 108 + t * 8)], '#5a4a3a', .8)
    G('gf_neko_lamp', 'Кошачий фонарик', 'nekomata', 3, glow=[65, 100])

    img = canvas(130, 90); floor_shadow(img, 65, 84, 56)                                      # akaname: tawashi
    m = blob(img, [(10, 60), (30, 30), (65, 22), (100, 30), (120, 60), (100, 80), (30, 80)], hexc('#8a6030'), 1320, scale=2, k=.45)
    rr = random.Random(3); clip(img, m, lambda d: [d.line([(px(x), px(y)), (px(x + rr.uniform(-4, 4)), px(y - 6))], fill=(60, 36, 14, 200), width=px(1)) for x, y in [(rr.uniform(10, 120), rr.uniform(24, 82)) for _ in range(260)]])
    line(img, [(62, 22), (66, 8), (74, 22)], '#c8a060', 1.6)
    G('gf_aka_tawashi', 'Мочалка аканамэ', 'akaname', 1)
    img = canvas(170, 110); floor_shadow(img, 80, 104, 70)                                    # akaname: hinoki dipper
    m = part(img, '#d8b47a', 1330, [(20, 50), (110, 50), (104, 104), (26, 104)], k=.45, stretch=(.3, 3))
    clip(img, m, lambda d: [d.line([(px(x), px(50)), (px(x), px(104))], fill=(120, 80, 40, 80), width=px(1)) for x in range(28, 110, 10)])
    for y in (60, 94): ImageDraw.Draw(img).rectangle([px(22), px(y - 2), px(108), px(y + 2)], fill=H('#8a6030'))
    fill(img, '#c89a60', 1331, ell=(20, 42, 110, 58), scale=3)
    rect_part(img, '#d8b47a', 1332, (106, 56, 166, 66), k=.35, stretch=(3, .5))
    G('gf_aka_oke', 'Кипарисовый ковшик', 'akaname', 2)
    img = canvas(120, 100); floor_shadow(img, 60, 94, 50)                                     # akaname: red duck
    blob(img, [(10, 70), (20, 50), (60, 46), (104, 54), (110, 72), (86, 92), (30, 92)], hexc('#c8281e'), 1340, spec=.5)
    ball(img, 36, 36, 22, 20, '#c8281e', 1341, spec=.55)
    poly(img, [(12, 40), (4, 44), (14, 48)], '#e8a030'); ell(img, (28, 28, 36, 36), '#1a1410'); ell(img, (30, 29, 33, 32), '#f2eee4')
    part(img, '#a81e16', 1342, [(60, 60), (96, 56), (84, 78)], k=.3, scale=2)
    G('gf_aka_duck', 'Красная банная уточка', 'akaname', 3)

    img = canvas(90, 180); floor_shadow(img, 45, 174, 34)                                     # obake: blue candle
    part(img, '#2a2a2e', 1350, [(14, 174), (76, 174), (60, 150), (30, 150)], k=.4, spec=.3); rect_part(img, '#2a2a2e', 1351, (40, 110, 50, 150), k=.3)
    part(img, '#f2eee4', 1352, [(30, 60), (60, 60), (60, 112), (30, 112)], k=.35, scale=3)
    for k in range(3): blob(img, [(45 - 12 + k * 3, 58), (45 - 6 + k * 2, 36), (45, 12 + k * 10), (45 + 6 - k, 36), (45 + 12 - k * 3, 58)], hexc(['#2a5ad8', '#6a9af0', '#e8f0ff'][k]), 1353 + k, scale=2, k=.1, rim=.1)
    G('gf_obake_candle', 'Синяя свеча, что не гаснет', 'obake', 1, glow=[45, 40])
    img = canvas(150, 240); floor_shadow(img, 75, 234, 40)                                    # obake: kasa-obake
    part(img, '#6a4a2a', 1360, [(56, 234), (94, 234), (90, 222), (60, 222)], k=.3); line(img, [(75, 222), (75, 190)], '#d8c8a0', 5)
    part(img, '#c8a050', 1361, [(75, 10), (130, 190), (20, 190)], k=.35, scale=4, contrast=.6)
    for k in range(5): line(img, [(75, 10), (24 + k * 25, 190)], '#8a6a2a', 1.2)
    ell(img, (52, 70, 98, 112), '#f2eee4'); ell(img, (66, 82, 84, 100), '#141010')
    part(img, '#c83a4a', 1362, [(66, 130), (84, 130), (86, 176), (74, 186), (64, 170)], k=.3, scale=2)
    G('gf_obake_kasa', 'Зонтик-одноглазик каса-обакэ', 'obake', 2)
    img = canvas(90, 170); line(img, [(45, 0), (45, 22)], '#3a2a1a', 1.8)                      # obake: mini chochin
    paper_lantern(img, 45, 30, 150, 72, '#e8dcc0', 1370, ribs=8)
    ell(img, (26, 56, 60, 84), '#f2eee4'); ell(img, (36, 62, 50, 78), '#141010')
    part(img, '#c83a4a', 1371, [(34, 104), (56, 104), (54, 138), (44, 146), (36, 132)], k=.3, scale=2)
    G('gf_obake_mini', 'Маленький тётин с глазом', 'obake', 3, 't', glow=[45, 90])

    img = canvas(150, 90); floor_shadow(img, 75, 84, 66)                                      # warashi: otedama
    for k, (x, y, c) in enumerate(((40, 60, '#c02a3a'), (78, 66, '#2a5a8a'), (112, 58, '#e8a0b8'), (60, 40, '#e8c040'))):
        m = blob(img, [(x - 20, y + 10), (x - 16, y - 12), (x, y - 16), (x + 16, y - 12), (x + 20, y + 10), (x, y + 16)], hexc(c), 1380 + k, scale=2, spec=.2)
        clip(img, m, lambda d, x=x, y=y: [d.ellipse([px(x + a - 2), px(y + b - 2), px(x + a + 2), px(y + b + 2)], fill=(245, 240, 230, 200)) for a, b in ((-8, -4), (6, 2), (-2, 8), (8, -8))])
    G('gf_wara_otedama', 'Мешочки отэдама', 'warashi', 1)
    img = canvas(140, 70); floor_shadow(img, 70, 64, 62)                                      # warashi: ohajiki
    part(img, '#6a2a3a', 1390, [(8, 30), (132, 30), (138, 64), (2, 64)], k=.2, scale=4)
    rr = random.Random(7)
    for k in range(11):
        x, y = rr.uniform(18, 122), rr.uniform(36, 58); c = rr.choice([(120, 190, 230), (240, 150, 170), (150, 220, 160), (240, 220, 120)])
        l = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(l).ellipse([px(x - 9), px(y - 5), px(x + 9), px(y + 5)], fill=c + (190,)); img.alpha_composite(l)
        ell(img, (x - 5, y - 3, x - 1, y - 1), '#ffffff')
    G('gf_wara_ohajiki', 'Стекляшки охадзики', 'warashi', 2)
    img = canvas(110, 200); floor_shadow(img, 55, 194, 44)                                    # warashi: ichimatsu doll
    part(img, '#b8202a', 1400, [(14, 194), (22, 110), (40, 90), (70, 90), (88, 110), (96, 194)], k=.4, scale=4)
    flowers(img, 55, 150, 34, 40, ['#f4c4d2', '#f2eee4', '#e8c040'], 12, 1401, (4, 6), '#c83a5a')
    rect_part(img, '#e8c048', 1402, (22, 124, 88, 140), k=.3, spec=.3)
    for s in (-1, 1): line(img, [(55, 90), (55 + s * 14, 110)], '#f2eee4', 2.4)
    ball(img, 55, 58, 34, 36, '#161212', 1403, spec=.3)
    ball(img, 55, 66, 26, 28, '#f4efe6', 1404, spec=.15, k=.3)
    part(img, '#161212', 1405, [(28, 50), (30, 30), (55, 24), (80, 30), (82, 50), (70, 44), (40, 44)], k=.2, scale=2)
    ell(img, (43, 62, 49, 68), '#1a1410'); ell(img, (61, 62, 67, 68), '#1a1410'); ell(img, (52, 78, 58, 82), '#c02a3a')
    G('gf_wara_doll', 'Кукла итимацу', 'warashi', 3)


if __name__ == '__main__':
    shogatsu(); setsubun(); hina(); hanami(); kodomo(); tanabata(); obon(); tsukimi(); shichigosan(); toji(); gifts()
    pack(); json.dump(ROWS, open(f'{OUT}/fest.json', 'w'), ensure_ascii=False, indent=0); print('TOTAL', len(ROWS))
