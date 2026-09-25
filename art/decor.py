#!/usr/bin/env python3
"""Painted decor sprites for room customisation (same brush toolkit as the backgrounds).
Each sprite is saved at its size in background-image pixels, with transparent surroundings."""
import json, math, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import paint as P
from paint import hexc, mixc, textured_fill, fbm

OUT = sys.argv[1]
KANJI_FONT = '/System/Library/Fonts/Hiragino Sans GB.ttc'
META = {}


def canvas(w, h):
    P.set_size(w, h); return P.layer()


def save(img, name, anchor='bottom'):
    out = img.resize((P.W, P.H), Image.LANCZOS)
    a = np.asarray(out, np.float32)
    lum = (a[..., :3] * [0.3, 0.59, 0.11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * 0.85
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').save(f'{OUT}/{name}.webp', 'WEBP', quality=86, method=6)
    META[name] = {'w': P.W, 'h': P.H, 'anchor': anchor}
    print('sprite', name, P.W, P.H)


S = P.SS
def px(v): return v * S


def fill_shape(img, poly, base, dark, light, scale, seed, stretch=(1, 1), contrast=1.0, ellipse=False):
    m = Image.new('L', img.size, 0); d = ImageDraw.Draw(m)
    if ellipse: d.ellipse([px(v) for v in poly], fill=255)
    else: d.polygon([(px(x), px(y)) for x, y in poly], fill=255)
    box = m.getbbox(); sub = m.crop(box)
    img.alpha_composite(textured_fill(sub, base, dark, light, scale * S, seed, stretch, contrast), (box[0], box[1]))


def shade_round(img, box, strength=0.5):
    """Darken the lower-right of whatever is inside box, giving rounded objects volume."""
    x0, y0, x1, y1 = (int(px(v)) for v in box)
    reg = img.crop((x0, y0, x1, y1)); a = np.asarray(reg, np.float32)
    yy = np.linspace(-1, 1, a.shape[0])[:, None]; xx = np.linspace(-1, 1, a.shape[1])[None, :]
    a[..., :3] *= np.clip(1.1 - strength * (0.6 * yy + 0.4 * xx + 0.2), 0.3, 1.2)[..., None]
    img.paste(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA'), (x0, y0))


def pot(img, cx, base, w, h, col, seed):
    fill_shape(img, [(cx - w / 2, base - h), (cx + w / 2, base - h), (cx + w * 0.4, base), (cx - w * 0.4, base)], col, mixc(col, (0, 0, 0, 255), .55), mixc(col, (255, 255, 255, 255), .2), 8, seed)
    d = ImageDraw.Draw(img); d.rectangle([px(cx - w / 2 - 4), px(base - h - 6), px(cx + w / 2 + 4), px(base - h + 4)], fill=mixc(col, (0, 0, 0, 255), .35))
    shade_round(img, (cx - w / 2 - 4, base - h - 6, cx + w / 2 + 4, base), .4)


# ───────────── engawa ─────────────
def bonsai():
    img = canvas(320, 340)
    P.pine(img, px(160), px(262), px(230), 5, P.PAL_PINE, P.BARK, lean=.35, pads=4, spread=.8)
    pot(img, 160, 330, 210, 66, hexc('#3b4a52'), 1)
    d = ImageDraw.Draw(img); d.ellipse([px(70), px(254), px(250), px(274)], fill=hexc('#2c3524'))
    save(img, 'd_bonsai')


def ikebana():
    img = canvas(340, 460)
    P.maple(img, px(170), px(330), px(260), 12, P.PAL_SAKURA, (hexc('#1a120e'), hexc('#2c201a'), hexc('#46372c')), lean=-.3)
    fill_shape(img, [(115, 460), (225, 460), (230, 380), (200, 330), (140, 330), (110, 380)], hexc('#26302c'), hexc('#10150f'), hexc('#3f4b45'), 8, 2)
    shade_round(img, (108, 328, 232, 460), .5)
    save(img, 'd_ikebana')


def kokedama():
    img = canvas(260, 260)
    P.maple(img, px(130), px(140), px(110), 4, P.PAL_MAPLE, P.BARK, lean=.1)
    fill_shape(img, (60, 110, 200, 230), hexc('#34482a'), hexc('#18220f'), hexc('#58703f'), 5, 3, contrast=1.3, ellipse=True)
    shade_round(img, (60, 110, 200, 230), .6)
    fill_shape(img, (30, 225, 230, 258), hexc('#2a2622'), hexc('#121010'), hexc('#3e3a34'), 10, 4, ellipse=True)
    save(img, 'd_kokedama')


def bamboo_pot():
    img = canvas(260, 460); d = ImageDraw.Draw(img); rnd = random.Random(3)
    for i, (x, h) in enumerate([(100, 420), (140, 380), (170, 440), (120, 330)]):
        top = 400 - h
        fill_shape(img, [(x - 7, 400), (x + 7, 400), (x + 6, top), (x - 6, top)], hexc('#56643e'), hexc('#2d3620'), hexc('#7d8a58'), 20, 10 + i, (0.2, 4), 1.2)
        for y in range(int(top) + 40, 400, 55):
            d.rectangle([px(x - 8), px(y), px(x + 8), px(y + 3)], fill=hexc('#2c341f'))
        for k in range(4):
            y = top + 30 + k * 60; s = rnd.choice((-1, 1))
            blobs = [(px(x + s * 34), px(y), px(34), px(9))]
            P.dab_mass(d, blobs, 60, 'leaf', P.PAL_MAPLE, rnd, size=(5, 10))
    pot(img, 135, 458, 170, 70, hexc('#1f1d1b'), 11)
    save(img, 'd_bamboo')


def zabuton(name, base, pattern, seed):
    img = canvas(320, 120)
    poly = [(30, 40), (290, 40), (312, 102), (8, 102)]
    fill_shape(img, poly, base, mixc(base, (0, 0, 0, 255), .5), mixc(base, (255, 255, 255, 255), .15), 18, seed, (3, 1), 0.9)
    d = ImageDraw.Draw(img); rnd = random.Random(seed)
    if pattern == 'asanoha':
        for _ in range(140):
            x = rnd.uniform(40, 280); y = rnd.uniform(46, 98)
            d.line([(px(x), px(y)), (px(x + 6), px(y + 3))], fill=mixc(base, (255, 230, 200, 255), .35), width=S)
    elif pattern == 'waves':
        for row in range(4):
            y = 50 + row * 13
            for x in range(40 - row * 5, 290 + row * 5, 22):
                d.arc([px(x), px(y), px(x + 22), px(y + 16)], 180, 360, fill=mixc(base, (220, 225, 235, 255), .35), width=S)
    elif pattern == 'dots':
        for _ in range(60):
            x = rnd.uniform(40, 280); y = rnd.uniform(48, 96); r = 2.5
            d.ellipse([px(x - r), px(y - r * .6), px(x + r), px(y + r * .6)], fill=mixc(base, (230, 210, 170, 255), .45))
    d.line([(px(160), px(40)), (px(160), px(102))], fill=mixc(base, (0, 0, 0, 255), .35), width=2 * S)
    for x, y in ((30, 40), (290, 40), (312, 102), (8, 102)):
        d.ellipse([px(x - 5), px(y - 5), px(x + 5), px(y + 5)], fill=mixc(base, (0, 0, 0, 255), .3))
    edge = Image.new('RGBA', img.size, (0, 0, 0, 0)); ed = ImageDraw.Draw(edge)
    ed.polygon([(px(8), px(102)), (px(312), px(102)), (px(305), px(116)), (px(15), px(116))], fill=mixc(base, (0, 0, 0, 255), .6))
    img.alpha_composite(edge)
    save(img, name)


def furin(name, kind):
    img = canvas(110, 300); d = ImageDraw.Draw(img)
    d.line([(px(55), 0), (px(55), px(70))], fill=hexc('#1a1410'), width=S)
    if kind == 'iron':
        fill_shape(img, (22, 60, 88, 120), hexc('#2a2622'), hexc('#0f0d0b'), hexc('#4a433b'), 6, 5, contrast=1.3, ellipse=True)
        d.rectangle([px(22), px(90), px(88), px(122)], fill=(0, 0, 0, 0))
        fill_shape(img, [(22, 90), (88, 90), (92, 120), (18, 120)], hexc('#2a2622'), hexc('#0f0d0b'), hexc('#4a433b'), 6, 6, contrast=1.3)
    else:
        glass = hexc('#b9d6e6', 170) if kind == 'glass' else hexc('#6b8fbf', 190)
        m = Image.new('RGBA', img.size, (0, 0, 0, 0)); md = ImageDraw.Draw(m)
        md.pieslice([px(18), px(62), px(92), px(150)], 180, 360, fill=glass)
        md.ellipse([px(30), px(70), px(48), px(84)], fill=(255, 255, 255, 170))
        if kind == 'glass':
            for fx, fy in ((44, 96), (66, 88)):
                md.ellipse([px(fx - 7), px(fy - 4), px(fx + 7), px(fy + 4)], fill=hexc('#c43c2c', 230))
                md.polygon([(px(fx + 6), px(fy)), (px(fx + 13), px(fy - 5)), (px(fx + 13), px(fy + 5))], fill=hexc('#c43c2c', 230))
        else:
            for k in range(6): md.ellipse([px(28 + k * 9), px(90), px(34 + k * 9), px(96)], fill=(245, 245, 255, 200))
        img.alpha_composite(m)
        d.line([(px(18), px(106)), (px(92), px(106))], fill=(230, 240, 250, 160), width=2 * S)
    d.line([(px(55), px(100)), (px(55), px(160))], fill=hexc('#1a1410'), width=S)
    d.rectangle([px(51), px(150), px(59), px(158)], fill=hexc('#2a2622'))
    strip = hexc('#d9cfb5') if kind != 'blue' else hexc('#b8c9d8')
    fill_shape(img, [(38, 160), (72, 160), (72, 290), (38, 290)], strip, mixc(strip, (0, 0, 0, 255), .25), mixc(strip, (255, 255, 255, 255), .2), 6, 7)
    f = ImageFont.truetype(KANJI_FONT, px(26))
    d.text((px(55), px(205)), '風', font=f, fill=hexc('#2a1a14'), anchor='mm'); d.text((px(55), px(245)), '鈴', font=f, fill=hexc('#2a1a14'), anchor='mm')
    save(img, name, 'top')


def chochin_red():
    img = canvas(180, 320)
    d = ImageDraw.Draw(img); d.line([(px(90), 0), (px(90), px(40))], fill=hexc('#120c09'), width=2 * S)
    m = Image.new('L', (px(150), px(230)), 0); ImageDraw.Draw(m).ellipse([0, 0, m.width - 1, m.height - 1], fill=255)
    t = textured_fill(m, hexc('#a3322a'), hexc('#4a100c'), hexc('#e0694a'), 5 * S, 3)
    a = np.asarray(t, np.float32); yy = np.linspace(-1, 1, a.shape[0])
    for k in range(-6, 7): a[np.abs(yy - k * 0.15) < 0.012, :, :3] *= 0.5
    xx = np.linspace(-1, 1, a.shape[1])[None, :]; a[..., :3] *= (1 - 0.5 * xx ** 2)[..., None]
    img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'), (px(15), px(60)))
    f = ImageFont.truetype(KANJI_FONT, px(62)); d.text((px(90), px(178)), '祭', font=f, fill=hexc('#1a0806'), anchor='mm')
    for y in (46, 286): d.rectangle([px(40), px(y), px(140), px(y + 16)], fill=hexc('#140d09'))
    save(img, 'd_chochin', 'top')


def andon(name='d_andon', lit=True):
    img = canvas(170, 320); d = ImageDraw.Draw(img)
    pap = hexc('#f0d59a') if lit else hexc('#8d8472')
    fill_shape(img, [(30, 70), (140, 70), (140, 270), (30, 270)], pap, mixc(pap, (60, 30, 0, 255), .3), mixc(pap, (255, 255, 255, 255), .25), 5, 9)
    for x in (24, 140): d.rectangle([px(x), px(56), px(x + 7), px(318)], fill=hexc('#160f0a'))
    for y in (56, 168, 262): d.rectangle([px(24), px(y), px(147), px(y + 7)], fill=hexc('#160f0a'))
    d.rectangle([px(10), px(306), px(160), px(320)], fill=hexc('#241a13'))
    save(img, name)


# ───────────── onsen ─────────────
def okeya():
    img = canvas(260, 230)
    fill_shape(img, [(40, 90), (220, 90), (205, 220), (55, 220)], hexc('#8a6a45'), hexc('#4a3520'), hexc('#b08a5a'), 14, 3, (0.15, 4), 1.2)
    d = ImageDraw.Draw(img)
    for x in range(52, 212, 20): d.line([(px(x), px(92)), (px(x + (130 - x) * 0.08), px(218))], fill=hexc('#4a3520'), width=S)
    for y, w in ((115, 180), (190, 150)): d.rectangle([px(130 - w / 2 - 6), px(y), px(130 + w / 2 + 6), px(y + 9)], fill=hexc('#6d4a2a'))
    fill_shape(img, (40, 78, 220, 104), hexc('#1e2a2a'), hexc('#0c1414'), hexc('#3e5352'), 10, 4, ellipse=True)
    d.line([(px(170), px(95)), (px(250), px(10))], fill=hexc('#8a6a45'), width=5 * S)
    fill_shape(img, (220, 0, 258, 30), hexc('#8a6a45'), hexc('#4a3520'), hexc('#b08a5a'), 10, 5, ellipse=True)
    shade_round(img, (40, 78, 220, 222), .35)
    save(img, 'd_okeya')


def shishi():
    img = canvas(380, 300)
    P.stone(img, 110, 262, 100, 38, 21, hexc('#4a4e48'))
    d = ImageDraw.Draw(img); d.ellipse([px(40), px(236), px(180), px(262)], fill=hexc('#15201f'))
    for x in (250, 300):
        fill_shape(img, [(x - 7, 290), (x + 7, 290), (x + 6, 140), (x - 6, 140)], hexc('#6b6b44'), hexc('#34341f'), hexc('#8e8d5c'), 14, x, (0.2, 4), 1.1)
    d.rectangle([px(240), px(166), px(312), px(174)], fill=hexc('#2e2e1c'))
    save(img, 'd_shishi_base')
    img = canvas(300, 60)
    fill_shape(img, [(0, 22), (290, 12), (296, 40), (4, 44)], hexc('#77784a'), hexc('#3a3a22'), hexc('#a0a068'), 14, 31, (4, 0.3), 1.1)
    d = ImageDraw.Draw(img)
    for x in (90, 190): d.rectangle([px(x), px(14), px(x + 4), px(44)], fill=hexc('#34341f'))
    d.ellipse([px(0), px(20), px(14), px(46)], fill=hexc('#1e1e12'))
    save(img, 'd_shishi_tube', 'center')


def kaeru():
    img = canvas(220, 170)
    P.stone(img, 110, 120, 90, 46, 41, hexc('#4c5048'))
    P.stone(img, 110, 78, 56, 34, 42, hexc('#4c5048'))
    d = ImageDraw.Draw(img)
    for x in (82, 138):
        P.stone(img, x, 52, 16, 14, 43 + x, hexc('#565a52'), moss=False)
        d.ellipse([px(x - 5), px(48), px(x + 5), px(58)], fill=hexc('#15130f'))
    d.arc([px(84), px(78), px(136), px(100)], 10, 170, fill=hexc('#23241f'), width=2 * S)
    save(img, 'd_kaeru')


def yukimi():
    img = canvas(240, 260)
    P.toro(img, 120, 255, 220, 12)
    save(img, 'd_yukimi')


def yuzu():
    img = canvas(620, 130); d = ImageDraw.Draw(img); rnd = random.Random(8)
    for _ in range(16):
        x = rnd.uniform(40, 580); y = rnd.uniform(40, 100); r = rnd.uniform(15, 22)
        d.ellipse([px(x - r * 1.2), px(y + r * 0.4), px(x + r * 1.2), px(y + r * 0.9)], fill=(20, 30, 30, 120))
        fill_shape(img, (x - r, y - r, x + r, y + r), hexc('#d8a93a'), hexc('#8a5a14'), hexc('#f2d172'), 4, int(x), contrast=1.2, ellipse=True)
        shade_round(img, (x - r, y - r, x + r, y + r), .55)
        d.ellipse([px(x - r * .45), px(y - r * .55), px(x - r * .1), px(y - r * .3)], fill=(255, 245, 210, 150))
    save(img, 'd_yuzu', 'center')


def petals_float():
    img = canvas(620, 130); d = ImageDraw.Draw(img); rnd = random.Random(9)
    blobs = [(px(rnd.uniform(60, 560)), px(rnd.uniform(40, 100)), px(60), px(14)) for _ in range(6)]
    P.dab_mass(d, blobs, 900, 'leaf', P.PAL_SAKURA[2:], rnd, size=(4, 7))
    save(img, 'd_petals', 'center')


# ───────────── bedroom ─────────────
def futon(name, base, pattern, seed):
    img = canvas(900, 150)
    m = Image.new('L', (px(900), px(150)), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, m.width - 1, m.height - 1], px(40), fill=255)
    img.alpha_composite(textured_fill(m, base, mixc(base, (0, 0, 0, 255), .5), mixc(base, (255, 255, 255, 255), .15), 40 * S, seed, (3, 1), .8))
    d = ImageDraw.Draw(img); light = mixc(base, (235, 230, 220, 255), .38); rnd = random.Random(seed)
    if pattern == 'seigaiha':
        for row in range(7):
            y = 12 + row * 19
            for x in range(20 - (row % 2) * 20, 880, 40):
                for k in range(3): d.arc([px(x + k * 5), px(y + k * 5), px(x + 40 - k * 5), px(y + 40 - k * 5)], 180, 360, fill=light, width=S)
    elif pattern == 'asanoha':
        for x in range(20, 880, 44):
            for y in range(14, 140, 38):
                for a in range(6):
                    ang = a * math.pi / 3; d.line([(px(x), px(y)), (px(x + math.cos(ang) * 18), px(y + math.sin(ang) * 18))], fill=light, width=S)
    elif pattern == 'bamboo':
        for x in range(40, 880, 70):
            d.line([(px(x), px(10)), (px(x + 10), px(140))], fill=light, width=2 * S)
            for k in range(5): d.line([(px(x + k * 2), px(20 + k * 26)), (px(x + 24 + k * 2), px(12 + k * 26))], fill=light, width=S)
    elif pattern == 'moons':
        for _ in range(26):
            x = rnd.uniform(40, 860); y = rnd.uniform(20, 130); r = rnd.uniform(6, 11)
            d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=light); d.ellipse([px(x - r + 4), px(y - r - 2), px(x + r + 4), px(y + r - 2)], fill=base)
    for x in range(120, 880, 150): d.line([(px(x), px(8)), (px(x), px(142))], fill=mixc(base, (0, 0, 0, 255), .3), width=S)
    fill_shape(img, (14, 20, 150, 130), hexc('#cfc4a8'), hexc('#8a7f66'), hexc('#e6dcc2'), 6, seed + 1, contrast=1.1, ellipse=True)
    shade_round(img, (14, 20, 150, 130), .5)
    save(img, name)


def scroll(name, art):
    img = canvas(180, 580); d = ImageDraw.Draw(img)
    fill_shape(img, [(0, 0), (180, 0), (180, 580), (0, 580)], hexc('#3a3226'), hexc('#1e1912'), hexc('#57493a'), 10, 3)
    paper = Image.new('L', (px(150), px(470)), 255)
    pa = textured_fill(paper, hexc('#d6ccb3'), hexc('#b3a888'), hexc('#e6dcc4'), 8 * S, 4, contrast=.8)
    art_l = Image.new('RGBA', pa.size, (0, 0, 0, 0)); ad = ImageDraw.Draw(art_l); rnd = random.Random(5)
    ink = (26, 22, 20, 235)
    if art == 'moon':
        ad.ellipse([px(40), px(60), px(110), px(130)], fill=(236, 228, 205, 255)); ad.ellipse([px(40), px(60), px(110), px(130)], outline=(120, 110, 90, 200), width=S)
        for y in (150, 175): ad.line([(px(10), px(y)), (px(140), px(y - 8))], fill=(90, 90, 90, 90), width=px(8))
        P.set_size(150, 470); tmp = P.layer(); P.pine(tmp, px(60), px(470), px(260), 6, [hexc('#161412'), hexc('#1f1c19'), hexc('#2a2622'), hexc('#35302b')], (hexc('#111111'), hexc('#1c1c1c'), hexc('#2a2a2a')), lean=.4, pads=3, spread=.6)
        P.set_size(180, 580); art_l.alpha_composite(tmp.resize(art_l.size))
    elif art == 'koi':
        for i, (cx, cy, ang, col) in enumerate([(70, 160, 0.6, (200, 90, 40, 230)), (90, 300, -0.4, (30, 26, 24, 230))]):
            for k in range(26):
                t = k / 25; w = 16 * math.sin(math.pi * min(1, t * 1.3)) + 2
                x = cx + math.cos(ang + 1.5) * (t - .5) * 150; y = cy + math.sin(ang + 1.5) * (t - .5) * 150
                ad.ellipse([px(x - w), px(y - w * .7), px(x + w), px(y + w * .7)], fill=col)
            for s in (-1, 1): ad.line([(px(cx), px(cy)), (px(cx + s * 30), px(cy + 16))], fill=col, width=px(5))
        for y in range(40, 440, 60): ad.arc([px(10), px(y), px(140), px(y + 20)], 200, 340, fill=(60, 70, 80, 90), width=S)
    elif art == 'neko':
        f = ImageFont.truetype(KANJI_FONT, px(118))
        ad.text((px(75), px(180)), '猫', font=f, fill=ink, anchor='mm')
        ad.ellipse([px(96), px(380), px(130), px(414)], fill=(170, 40, 30, 220))
        art_l = art_l.filter(ImageFilter.GaussianBlur(0.6 * S))
    elif art == 'mountains':
        for k, (y, g) in enumerate([(200, 150), (270, 110), (330, 70)]):
            pts = [(0, px(470))]
            for x in range(0, 151, 10): pts.append((px(x), px(y - 60 * math.exp(-((x - 30 - k * 40) / 40) ** 2) + rnd.uniform(-4, 4))))
            pts.append((px(150), px(470)))
            ad.polygon(pts, fill=(g // 2, g // 2, g // 2, 200))
            ad.rectangle([0, px(y + 10), px(150), px(y + 40)], fill=(214, 204, 180, 120))
    pa.alpha_composite(art_l)
    img.alpha_composite(pa, (px(15), px(55)))
    for y in (0, 564): d.rectangle([px(-4), px(y), px(184), px(y + 16)], fill=hexc('#2a1d14'))
    save(img, name, 'top')


def daruma():
    img = canvas(190, 210)
    fill_shape(img, (15, 20, 175, 205), hexc('#a8261c'), hexc('#4d0e0a'), hexc('#dc5a3e'), 6, 3, contrast=1.1, ellipse=True)
    d = ImageDraw.Draw(img)
    d.ellipse([px(48), px(52), px(142), px(140)], fill=hexc('#e9dfca'))
    for x in (74, 116):
        d.ellipse([px(x - 13), px(80), px(x + 13), px(106)], fill=hexc('#f7f2e6')); d.ellipse([px(x - 4), px(88), px(x + 4), px(96)], fill=hexc('#15110f'))
    d.arc([px(62), px(64), px(92), px(82)], 200, 340, fill=hexc('#15110f'), width=3 * S); d.arc([px(98), px(64), px(128), px(82)], 200, 340, fill=hexc('#15110f'), width=3 * S)
    d.arc([px(70), px(106), px(120), px(130)], 20, 160, fill=hexc('#15110f'), width=2 * S)
    f = ImageFont.truetype(KANJI_FONT, px(34)); d.text((px(95), px(170)), '福', font=f, fill=hexc('#e2b55a'), anchor='mm')
    shade_round(img, (15, 20, 175, 205), .5)
    save(img, 'd_daruma')


def kokeshi():
    img = canvas(110, 250)
    fill_shape(img, [(28, 90), (82, 90), (86, 248), (24, 248)], hexc('#c9a878'), hexc('#8a6a44'), hexc('#e3c79a'), 10, 4, (0.3, 3))
    d = ImageDraw.Draw(img)
    for y, c in ((120, '#a8261c'), (160, '#2e4a3a'), (200, '#a8261c')):
        for k in range(4): d.ellipse([px(32 + k * 12), px(y), px(44 + k * 12), px(y + 12)], fill=hexc(c))
    fill_shape(img, (14, 4, 96, 96), hexc('#e8dcc4'), hexc('#b7a888'), hexc('#f3ead8'), 5, 5, ellipse=True)
    d.chord([px(14), px(4), px(96), px(96)], 180, 360, fill=hexc('#15110f'))
    for x in (40, 70): d.arc([px(x - 6), px(58), px(x + 6), px(66)], 200, 340, fill=hexc('#15110f'), width=2 * S)
    d.ellipse([px(52), px(74), px(58), px(80)], fill=hexc('#a8261c'))
    shade_round(img, (14, 4, 96, 248), .4)
    save(img, 'd_kokeshi')


def maneki():
    img = canvas(200, 240)
    body = hexc('#ece5d6')
    fill_shape(img, (30, 100, 170, 236), body, mixc(body, (80, 70, 60, 255), .4), (255, 255, 255, 255), 6, 3, ellipse=True)
    fill_shape(img, (40, 34, 160, 134), body, mixc(body, (80, 70, 60, 255), .4), (255, 255, 255, 255), 6, 4, ellipse=True)
    d = ImageDraw.Draw(img)
    for ex in ((48, 44, 70, 8), (130, 44, 152, 8)):
        d.polygon([(px(ex[0]), px(ex[1] + 20)), (px((ex[0] + ex[2]) / 2), px(ex[3] + 14)), (px(ex[2]), px(ex[1] + 14))], fill=body)
        d.polygon([(px(ex[0] + 5), px(ex[1] + 18)), (px((ex[0] + ex[2]) / 2), px(ex[3] + 22)), (px(ex[2] - 4), px(ex[1] + 14))], fill=hexc('#d99a9a'))
    fill_shape(img, (140, 20, 186, 110), body, mixc(body, (80, 70, 60, 255), .4), (255, 255, 255, 255), 6, 5, ellipse=True)
    for x in (78, 122): d.arc([px(x - 10), px(78), px(x + 10), px(92)], 200, 340, fill=hexc('#15110f'), width=3 * S)
    d.ellipse([px(96), px(96), px(104), px(102)], fill=hexc('#c77a7a'))
    d.rectangle([px(52), px(130), px(148), px(140)], fill=hexc('#a8261c'))
    d.ellipse([px(88), px(134), px(112), px(158)], fill=hexc('#d9b04a'))
    fill_shape(img, (64, 168, 136, 214), hexc('#c9a13e'), hexc('#7a5a14'), hexc('#f2d172'), 5, 6, ellipse=True)
    f = ImageFont.truetype(KANJI_FONT, px(26)); d.text((px(100), px(191)), '福', font=f, fill=hexc('#5a3a0a'), anchor='mm')
    shade_round(img, (30, 20, 186, 236), .45)
    save(img, 'd_maneki')


def cranes():
    img = canvas(280, 460); d = ImageDraw.Draw(img); rnd = random.Random(12)
    cols = ['#b4362a', '#d9c9a3', '#2c4a6b', '#c77a93', '#3e5a3a']
    d.line([(px(20), px(6)), (px(260), px(6))], fill=hexc('#2a1d14'), width=4 * S)
    for i, x in enumerate((40, 100, 160, 220)):
        L = rnd.uniform(160, 380); d.line([(px(x), px(6)), (px(x), px(L))], fill=hexc('#1a1410'), width=S)
        for k, y in enumerate(np.linspace(60, L - 10, 3)):
            c = hexc(cols[(i + k) % len(cols)]); cl = mixc(c, (255, 255, 255, 255), .25); cd = mixc(c, (0, 0, 0, 255), .35)
            d.polygon([(px(x - 22), px(y - 10)), (px(x), px(y + 4)), (px(x + 22), px(y - 10)), (px(x + 4), px(y + 10))], fill=cl)
            d.polygon([(px(x), px(y + 4)), (px(x + 4), px(y + 10)), (px(x - 6), px(y + 12))], fill=cd)
            d.polygon([(px(x - 22), px(y - 10)), (px(x - 28), px(y - 22)), (px(x - 16), px(y - 6))], fill=c)
    save(img, 'd_cranes', 'top')


def zabutons():
    zabuton('d_zab_indigo', hexc('#27324a'), 'waves', 1)
    zabuton('d_zab_red', hexc('#7a2620'), 'asanoha', 2)
    zabuton('d_zab_moss', hexc('#3c4a2c'), 'dots', 3)


def furins():
    furin('d_furin_glass', 'glass'); furin('d_furin_blue', 'blue'); furin('d_furin_iron', 'iron')


def futons():
    futon('d_futon_waves', hexc('#26314a'), 'seigaiha', 1)
    futon('d_futon_red', hexc('#6e2320'), 'asanoha', 2)
    futon('d_futon_bamboo', hexc('#32402a'), 'bamboo', 3)
    futon('d_futon_moon', hexc('#1c1d2b'), 'moons', 4)


def scrolls():
    scroll('d_scroll_moon', 'moon'); scroll('d_scroll_koi', 'koi'); scroll('d_scroll_neko', 'neko'); scroll('d_scroll_mount', 'mountains')


if __name__ == '__main__':
    for fn in [bonsai, ikebana, kokedama, bamboo_pot, zabutons, furins, chochin_red, andon, okeya, shishi, kaeru, yukimi, yuzu, petals_float,
               futons, scrolls, daruma, kokeshi, maneki, cranes]:
        fn()
    json.dump(META, open(f'{OUT}/decor.json', 'w'), indent=0)
