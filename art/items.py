#!/usr/bin/env python3
"""200 collectible things for «Мусин дом»: painted with the same brush toolkit as the rooms.
Usage: items.py <outdir>  →  <outdir>/<id>.webp + <outdir>/items.json  (catalogue with names, categories, sizes)."""
import json, math, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import paint as P
from paint import hexc, mixc, textured_fill

OUT = sys.argv[1]
S = P.SS
SANS = '/System/Library/Fonts/Hiragino Sans GB.ttc'
SERIF = '/System/Library/Fonts/Supplemental/AppleMyungjo.ttf'
CAT = []          # catalogue rows
ARIALU = '/Library/Fonts/Arial Unicode.ttf'
_FONT_OK = {}


def has_glyph(font, ch):
    key = (font, ch)
    if key not in _FONT_OK:
        f = ImageFont.truetype(font, 40)
        def g(c):
            im = Image.new('L', (64, 64)); ImageDraw.Draw(im).text((8, 8), c, font=f, fill=255); return im.tobytes()
        gc = g(ch); _FONT_OK[key] = gc != g('\uFFFF') and gc != g('\U0010FFFD') and any(gc)
    return _FONT_OK[key]


def font_for(text, prefer):
    for f in (prefer, SERIF, ARIALU, SANS):
        if all(has_glyph(f, c) for c in text): return f
    return ARIALU


def lum(c): c = H(c); return .3 * c[0] + .59 * c[1] + .11 * c[2]
BLACK, WHITE = (0, 0, 0, 255), (255, 255, 255, 255)


def px(v): return int(round(v * S))
def canvas(w, h): P.set_size(w, h); return P.layer()
def dk(c, k=.5): return mixc(c, BLACK, k)
def lt(c, k=.25): return mixc(c, WHITE, k)
def H(c): return hexc(c) if isinstance(c, str) else c


def mask_poly(img, poly=None, ell=None, rect=None):
    m = Image.new('L', img.size, 0); d = ImageDraw.Draw(m)
    if poly: d.polygon([(px(x), px(y)) for x, y in poly], fill=255)
    if ell: d.ellipse([px(v) for v in ell], fill=255)
    if rect: d.rectangle([px(v) for v in rect], fill=255)
    return m


def fill(img, base, seed, poly=None, ell=None, rect=None, scale=8, stretch=(1, 1), contrast=1.0, dark=.45, light=.2, mask=None):
    base = H(base); m = mask or mask_poly(img, poly, ell, rect); box = m.getbbox()
    if not box: return m
    sub = m.crop(box)
    img.alpha_composite(textured_fill(sub, base, dk(base, dark), lt(base, light), scale * S, seed, stretch, contrast), box[:2])
    return m


def volume(img, box, k=.5, rim=.35, spec=0.0, lx=-.55, ly=-.8):
    """Light from the upper left, darker rim: gives round things body."""
    x0, y0, x1, y1 = (max(0, px(v)) for v in box); x1 = min(x1, img.width); y1 = min(y1, img.height)
    reg = img.crop((x0, y0, x1, y1)); a = np.asarray(reg, np.float32)
    h, w = a.shape[:2]; yy = np.linspace(-1, 1, h)[:, None]; xx = np.linspace(-1, 1, w)[None, :]
    lit = 1 + k * (-(xx * lx + yy * ly)) * .55
    lit = lit * (1 - rim * np.clip(xx ** 2 + yy ** 2 - .35, 0, 1.2))
    a[..., :3] *= lit[..., None]
    if spec:
        g = np.exp(-(((xx + .38) / .22) ** 2 + ((yy + .45) / .16) ** 2)) * spec * 255
        a[..., :3] += g[..., None]
    img.paste(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA'), (x0, y0))


def soft(img, fn, blur):
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(l)); img.alpha_composite(l.filter(ImageFilter.GaussianBlur(blur * S)))


def floor_shadow(img, cx, base, rx, a=110):
    soft(img, lambda d: d.ellipse([px(cx - rx), px(base - rx * .16), px(cx + rx), px(base + rx * .12)], fill=(0, 0, 0, a)), 5)


def text(img, ch, x, y, size, col, font=SANS, brush=False):
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    d.text((px(x), px(y)), ch, font=ImageFont.truetype(font_for(ch, font), px(size)), fill=H(col), anchor='mm')
    if brush:   # ink: slightly bled edges and dry-brush speckle
        a = np.asarray(l, np.float32); n = np.random.default_rng(len(ch) + int(x)).random(a.shape[:2])
        a[..., 3] *= np.where(n < .08, .45, 1); l = Image.fromarray(a.astype(np.uint8), 'RGBA').filter(ImageFilter.GaussianBlur(.6 * S))
    img.alpha_composite(l)


def line(img, pts, col, w):
    ImageDraw.Draw(img).line([(px(x), px(y)) for x, y in pts], fill=H(col), width=max(1, px(w)), joint='curve')


def ell(img, box, col):
    ImageDraw.Draw(img).ellipse([px(v) for v in box], fill=H(col))


def poly(img, pts, col):
    ImageDraw.Draw(img).polygon([(px(x), px(y)) for x, y in pts], fill=H(col))


def save(img, iid, name, cat, anchor='b', price=60, story=False, glow=None, extra=None):
    out = img.resize((P.W, P.H), Image.LANCZOS)
    a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .88
    rng = np.random.default_rng(abs(hash(iid)) % 2 ** 32); a[..., :3] += rng.normal(0, 3.5, a.shape[:2])[..., None]
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').save(f'{OUT}/{iid}.webp', 'WEBP', quality=86, alpha_quality=90, method=6)
    row = {'id': iid, 'n': name, 'c': cat, 'w': P.W, 'h': P.H, 'a': anchor, 'p': price}
    if story: row['story'] = 1
    if glow: row['glow'] = glow
    if extra: row.update(extra)
    CAT.append(row); print(iid, P.W, P.H, name)


# ───────────────────────────── 1. Омамори ─────────────────────────────
def omamori(iid, name, col, kanji, cord='#c9a24a', story=False):
    img = canvas(70, 150); col = H(col)
    line(img, [(35, 2), (22, 22), (35, 38), (48, 22), (35, 2)], cord, 2.2)
    for dx in (-3, 3): line(img, [(35 + dx, 34), (35 + dx * 3, 50)], cord, 2)
    body = [(10, 52), (35, 40), (60, 52), (62, 146), (8, 146)]
    fill(img, col, hash(iid) % 999, poly=body, scale=5, contrast=1.3)
    d = ImageDraw.Draw(img); rnd = random.Random(iid)
    gold = lt(H(cord), .1)
    for _ in range(46):   # brocade pattern
        x, y = rnd.uniform(14, 56), rnd.uniform(56, 142); r = rnd.uniform(1.2, 2.2)
        d.polygon([(px(x), px(y - r)), (px(x + r), px(y)), (px(x), px(y + r)), (px(x - r), px(y))], fill=mixc(col, gold, .45))
    d.line([(px(10), px(62)), (px(60), px(62))], fill=dk(col, .35), width=px(2))
    fill(img, mixc(col, gold, .2), 7, rect=(20, 74, 50, 132), scale=4, contrast=.8)
    text(img, kanji, 35, 103, 24, gold if lum(col) < 140 else H('#5a1a14'), SERIF)
    volume(img, (8, 40, 62, 146), .55, .25)
    save(img, iid, name, 'Омамори', 't', 45, story)


# ───────────────────────────── 2. Эма ─────────────────────────────
def ema(iid, name, kanji, accent, motif):
    img = canvas(150, 130)
    line(img, [(40, 4), (75, 20), (110, 4)], '#b3322a', 2.4)
    board = [(8, 36), (75, 16), (142, 36), (142, 126), (8, 126)]
    fill(img, '#c9a778', hash(iid) % 777, poly=board, scale=14, stretch=(6, .6), contrast=1.2, dark=.3, light=.15)
    d = ImageDraw.Draw(img)
    d.line([(px(8), px(36)), (px(75), px(16)), (px(142), px(36))], fill=H('#5a3e22'), width=px(4))
    ac = H(accent); rnd = random.Random(iid)
    if motif == 'sun': soft(img, lambda dd: dd.ellipse([px(88), px(44), px(130), px(86)], fill=mixc(ac, (0, 0, 0, 0), 0)[:3] + (220,)), .6)
    elif motif == 'wave':
        for k in range(3): d.arc([px(14 + k * 40), px(92), px(58 + k * 40), px(128)], 180, 360, fill=ac, width=px(3))
    elif motif == 'cloud':
        for cx, cy in ((110, 60), (126, 70), (100, 72)): d.ellipse([px(cx - 14), px(cy - 9), px(cx + 14), px(cy + 9)], fill=ac)
    elif motif == 'plum':
        for _ in range(7):
            cx, cy = rnd.uniform(90, 132), rnd.uniform(44, 110)
            for p in range(5):
                a = p / 5 * math.tau; d.ellipse([px(cx + math.cos(a) * 4 - 3), px(cy + math.sin(a) * 4 - 3), px(cx + math.cos(a) * 4 + 3), px(cy + math.sin(a) * 4 + 3)], fill=ac)
    elif motif == 'bamboo':
        for x in (110, 124): d.line([(px(x), px(46)), (px(x - 4), px(122))], fill=ac, width=px(4))
    text(img, kanji, 52, 80, 50, '#1c1410', SERIF, brush=True)
    d.rectangle([px(118), px(100), px(134), px(116)], fill=H('#b8322a'))
    volume(img, (8, 16, 142, 126), .35, .15)
    save(img, iid, name, 'Эма', 't', 35)


# ───────────────────────────── 3. Тётин (бумажные фонари) ─────────────────────────────
def chochin(iid, name, col, kanji, tall=True, ink='#1a0806', story=False):
    w, h = (110, 250) if tall else (140, 210)
    img = canvas(w, h); col = H(col)
    line(img, [(w / 2, 0), (w / 2, 30)], '#120c09', 2)
    top, bot = 34, h - 18
    m = mask_poly(img, ell=(8, top + 6, w - 8, bot - 6))
    m2 = mask_poly(img, rect=(w * .22, top, w * .78, bot))
    mm = Image.fromarray(np.maximum(np.asarray(m), np.asarray(m2)))
    fill(img, col, hash(iid) % 555, mask=mm, scale=5, contrast=1.1, dark=.35, light=.25)
    a = np.asarray(img, np.float32); yy = np.arange(a.shape[0])
    for k in range(1, 14):
        yk = px(top + (bot - top) * k / 14); a[max(0, yk - 1):yk + 1, :, :3] *= .55
    img = Image.fromarray(a.astype(np.uint8), 'RGBA')
    text(img, kanji, w / 2, (top + bot) / 2, w * .5, ink, SERIF)
    volume(img, (8, top, w - 8, bot), .5, .45)
    for y in (top - 6, bot - 4): ImageDraw.Draw(img).rectangle([px(w * .22), px(y), px(w * .78), px(y + 12)], fill=H('#140d09'))
    save(img, iid, name, 'Фонари', 't', 70, story, glow=[w / 2, (top + bot) / 2])


def andon(iid, name, kind, paper='#efd49a', frame='#1a120c', mark=None):
    if kind == 'maru':   # cylinder
        img = canvas(150, 300); floor_shadow(img, 75, 292, 64)
        fill(img, paper, 3, rect=(24, 60, 126, 262), scale=6, contrast=.8)
        volume(img, (24, 60, 126, 262), .15, .55)
        for y in (56, 262): ImageDraw.Draw(img).rectangle([px(20), px(y), px(130), px(y + 10)], fill=H(frame))
        for x in (34, 116): line(img, [(x, 272), (x - 6, 294)], frame, 5)
        if mark: text(img, mark, 75, 160, 44, '#4a2a10', SERIF)
        save(img, iid, name, 'Светильники', 'b', 120, glow=[75, 160]); return
    if kind == 'toro':  # small stone garden lantern
        img = canvas(170, 280); floor_shadow(img, 85, 272, 70)
        st = '#6a6d66'
        fill(img, st, 11, poly=[(40, 272), (130, 272), (120, 240), (50, 240)], scale=6, contrast=1.3)
        fill(img, st, 12, rect=(72, 150, 98, 242), scale=6, contrast=1.3)
        fill(img, st, 13, poly=[(46, 150), (124, 150), (116, 110), (54, 110)], scale=6, contrast=1.3)
        ImageDraw.Draw(img).rectangle([px(70), px(118), px(100), px(144)], fill=H('#f2c878'))
        fill(img, st, 14, poly=[(20, 110), (150, 110), (104, 62), (66, 62)], scale=6, contrast=1.3)
        ell(img, (74, 44, 96, 66), st)
        volume(img, (20, 44, 150, 272), .4, .2)
        save(img, iid, name, 'Светильники', 'b', 160, glow=[85, 130]); return
    if kind == 'yukimi':
        img = canvas(200, 230); floor_shadow(img, 100, 224, 88)
        st = '#5f635d'
        for x0 in (40, 100, 150): fill(img, st, x0, poly=[(x0, 226), (x0 + 12, 226), (x0 + 16, 150), (x0 + 6, 150)], scale=5, contrast=1.3)
        fill(img, st, 21, poly=[(52, 150), (148, 150), (140, 110), (60, 110)], scale=6, contrast=1.3)
        ImageDraw.Draw(img).rectangle([px(82), px(116), px(118), px(144)], fill=H('#f2c878'))
        fill(img, st, 22, poly=[(6, 112), (194, 112), (120, 66), (80, 66)], scale=6, contrast=1.3)
        ell(img, (88, 46, 112, 70), st)
        volume(img, (6, 46, 194, 226), .4, .2)
        save(img, iid, name, 'Светильники', 'b', 170, glow=[100, 130]); return
    # square andon on legs
    img = canvas(150, 310); floor_shadow(img, 75, 302, 66)
    fill(img, paper, 5, rect=(28, 70, 122, 262), scale=6, contrast=.8)
    d = ImageDraw.Draw(img)
    for x in (22, 122): d.rectangle([px(x), px(56), px(x + 7), px(304)], fill=H(frame))
    for y in (56, 150 if kind == 'tall' else 166, 262): d.rectangle([px(22), px(y), px(129), px(y + 6)], fill=H(frame))
    if mark == 'moon': ell(img, (54, 90, 96, 132), '#fff1c9')
    elif mark: text(img, mark, 75, 210, 40, '#4a2a10', SERIF)
    volume(img, (22, 56, 129, 304), .2, .2)
    save(img, iid, name, 'Светильники', 'b', 130, glow=[75, 170])


# ───────────────────────────── 4. Фурин ─────────────────────────────
def furin(iid, name, glass, motif, iron=False, strip='#d9cfb5', ch='涼'):
    img = canvas(100, 270); d = ImageDraw.Draw(img)
    line(img, [(50, 0), (50, 48)], '#1a1410', 1.4)
    if iron:
        fill(img, glass, hash(iid) % 99, ell=(18, 42, 82, 108), scale=4, contrast=1.4)
        ImageDraw.Draw(img).rectangle([px(10), px(82), px(90), px(112)], fill=(0, 0, 0, 0))
        fill(img, glass, 5, poly=[(20, 76), (80, 76), (86, 110), (14, 110)], scale=4, contrast=1.4)
        volume(img, (14, 42, 86, 110), .6, .3, spec=.25)
    else:
        m = Image.new('RGBA', img.size, (0, 0, 0, 0)); md = ImageDraw.Draw(m); g = H(glass)
        md.pieslice([px(14), px(44), px(86), px(150)], 180, 360, fill=g[:3] + (165,))
        rnd = random.Random(iid)
        if motif == 'kingyo':
            for fx, fy in ((40, 84), (62, 74)):
                md.ellipse([px(fx - 7), px(fy - 4), px(fx + 7), px(fy + 4)], fill=hexc('#d2402c', 235)); md.polygon([(px(fx + 6), px(fy)), (px(fx + 13), px(fy - 5)), (px(fx + 13), px(fy + 5))], fill=hexc('#d2402c', 235))
        elif motif == 'asagao':
            for fx, fy, c in ((38, 80, '#5a4ab8'), (64, 86, '#b04a9a')):
                md.ellipse([px(fx - 9), px(fy - 9), px(fx + 9), px(fy + 9)], fill=hexc(c, 235)); md.ellipse([px(fx - 3), px(fy - 3), px(fx + 3), px(fy + 3)], fill=(255, 255, 255, 220))
        elif motif == 'hanabi':
            for fx, fy, c in ((40, 76, '#f0a030'), (64, 88, '#e05070')):
                for k in range(12):
                    a = k / 12 * math.tau; md.line([(px(fx), px(fy)), (px(fx + math.cos(a) * 9), px(fy + math.sin(a) * 9))], fill=hexc(c, 235), width=px(1.2))
        elif motif == 'tombo':
            md.line([(px(34), px(84)), (px(66), px(84))], fill=hexc('#3a5a8a', 240), width=px(2.4))
            for sx in (44, 52):
                for sy in (-1, 1): md.ellipse([px(sx - 7), px(84 + sy * 7 - 3), px(sx + 7), px(84 + sy * 7 + 3)], fill=(220, 235, 255, 160))
        elif motif == 'momiji':
            for fx, fy in ((38, 78), (60, 88), (66, 70)):
                for k in range(5):
                    a = -math.pi / 2 + (k - 2) * .6; md.line([(px(fx), px(fy)), (px(fx + math.cos(a) * 8), px(fy + math.sin(a) * 8))], fill=hexc('#c8442a', 240), width=px(2.4))
        elif motif == 'dots':
            for _ in range(14):
                x, y = rnd.uniform(24, 76), rnd.uniform(62, 96); md.ellipse([px(x - 2.5), px(y - 2.5), px(x + 2.5), px(y + 2.5)], fill=(255, 255, 255, 210))
        elif motif == 'nami':
            for k in range(3): md.arc([px(18 + k * 22), px(82), px(40 + k * 22), px(100)], 180, 360, fill=(255, 255, 255, 220), width=px(1.6))
        md.ellipse([px(28), px(54), px(42), px(66)], fill=(255, 255, 255, 170))
        img.alpha_composite(m)
        d.line([(px(14), px(96)), (px(86), px(96))], fill=(230, 240, 250, 170), width=px(1.6))
    d = ImageDraw.Draw(img)
    line(img, [(50, 94), (50, 150)], '#1a1410', 1.2); d.rectangle([px(46), px(144), px(54), px(152)], fill=H('#2a2622'))
    fill(img, strip, 7, rect=(34, 152, 66, 266), scale=5, contrast=.8)
    text(img, ch, 50, 190, 22, '#2a1a14', SERIF)
    save(img, iid, name, 'Фурины', 't', 55)


# ───────────────────────────── 5. Кокэси ─────────────────────────────
def kokeshi(iid, name, body, pattern, h=230, hair='top', face_col='#f3e3c8'):
    w = 92; img = canvas(w, h + 8); floor_shadow(img, w / 2, h + 2, 38)
    body = H(body); by = h * .36
    fill(img, body, hash(iid) % 400, poly=[(22, by), (70, by), (74, h), (18, h)], scale=10, stretch=(.4, 3), contrast=.9)
    d = ImageDraw.Draw(img); rnd = random.Random(iid)
    if pattern == 'rings':
        for k in range(4): d.rectangle([px(19), px(by + 18 + k * (h - by - 30) / 4), px(73), px(by + 24 + k * (h - by - 30) / 4)], fill=H(rnd.choice(['#b3322a', '#2a4a7a', '#2f6b3a', '#1a1414'])))
    elif pattern in ('kiku', 'ume', 'tsubaki'):
        c = {'kiku': '#c9383a', 'ume': '#d86a8a', 'tsubaki': '#a0202a'}[pattern]
        for fy in (by + 30, by + 70, by + 110):
            if fy > h - 16: continue
            cx = 46 + rnd.uniform(-8, 8)
            for k in range(8 if pattern == 'kiku' else 5):
                a = k / (8 if pattern == 'kiku' else 5) * math.tau; r = 9 if pattern == 'kiku' else 7
                d.ellipse([px(cx + math.cos(a) * r - 5), px(fy + math.sin(a) * r - 5), px(cx + math.cos(a) * r + 5), px(fy + math.sin(a) * r + 5)], fill=H(c))
            d.ellipse([px(cx - 4), px(fy - 4), px(cx + 4), px(fy + 4)], fill=H('#e8c040'))
            line(img, [(cx + 10, fy + 8), (cx + 22, fy + 20)], '#2f5a2a', 2.2)
    elif pattern == 'stripes':
        for k in range(10): d.line([(px(24 + k * 5), px(by + 6)), (px(22 + k * 5.6), px(h - 4))], fill=H(rnd.choice(['#8a2a22', '#e0b050', '#2a4a6a'])), width=px(1.6))
    elif pattern == 'kimono':
        d.polygon([(px(22), px(by + 4)), (px(46), px(by + 40)), (px(70), px(by + 4))], fill=H('#f2ead8'))
        d.rectangle([px(20), px(by + 52), px(72), px(by + 66)], fill=H('#d8a93a'))
    volume(img, (18, by, 74, h), .45, .5)
    # head
    fill(img, face_col, 3, ell=(14, 8, 78, by + 8), scale=8, contrast=.5)
    d = ImageDraw.Draw(img)
    if hair == 'top':
        d.chord([px(14), px(6), px(78), px(by + 4)], 180, 360, fill=H('#15110f')); d.ellipse([px(36), px(0), px(56), px(16)], fill=H('#15110f'))
    else:  # bob with bangs
        d.chord([px(12), px(4), px(80), px(by + 12)], 170, 370, fill=H('#15110f'))
        d.rectangle([px(12), px(by * .5), px(22), px(by + 4)], fill=H('#15110f')); d.rectangle([px(70), px(by * .5), px(80), px(by + 4)], fill=H('#15110f'))
    for ex in (36, 56): d.arc([px(ex - 5), px(by * .58), px(ex + 5), px(by * .58 + 7)], 200, 340, fill=H('#1a1210'), width=px(1.8))
    d.ellipse([px(43), px(by * .8), px(49), px(by * .8 + 4)], fill=H('#c0302a'))
    for cx in (28, 64): soft(img, lambda dd, cx=cx: dd.ellipse([px(cx - 6), px(by * .7), px(cx + 6), px(by * .7 + 7)], fill=(220, 110, 110, 90)), 2)
    volume(img, (14, 6, 78, by + 8), .45, .35, spec=.12)
    save(img, iid, name, 'Кокэси', 'b', 80)


# ───────────────────────────── 6. Дарума ─────────────────────────────
def daruma(iid, name, col, kanji, eyes=0, gold='#e0b64a'):
    img = canvas(160, 176); floor_shadow(img, 80, 168, 66); col = H(col)
    fill(img, col, hash(iid) % 300, ell=(12, 16, 148, 170), scale=6, contrast=1.1)
    fill(img, '#f1ece2', 4, ell=(38, 32, 122, 108), scale=6, contrast=.5)
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        d.arc([px(80 + sx * 22 - 16), px(40), px(80 + sx * 22 + 16), px(64)], 200 if sx < 0 else 250, 290 if sx < 0 else 340, fill=H('#15110f'), width=px(4))
        ex = 80 + sx * 20; d.ellipse([px(ex - 11), px(58), px(ex + 11), px(80)], fill=H('#fbf8f0')); d.ellipse([px(ex - 11), px(58), px(ex + 11), px(80)], outline=H('#15110f'), width=px(1.6))
        if (eyes == 1 and sx < 0) or eyes == 2: d.ellipse([px(ex - 6), px(63), px(ex + 6), px(75)], fill=H('#15110f'))
    for k in range(7):   # beard strokes
        a = math.pi * (.15 + .7 * k / 6); d.line([(px(80 + math.cos(a) * 24), px(92 + math.sin(a) * 6)), (px(80 + math.cos(a) * 36), px(98 + math.sin(a) * 12))], fill=H('#15110f'), width=px(2))
    d.arc([px(70), px(84), px(90), px(96)], 20, 160, fill=H('#15110f'), width=px(2))
    text(img, kanji, 80, 134, 34 if len(kanji) == 1 else 22, gold if lum(col) < 130 else H('#5a1414'), SERIF)
    volume(img, (12, 16, 148, 170), .6, .4, spec=.2)
    save(img, iid, name, 'Дарума', 'b', 70)


# ───────────────────────────── 7. Манэки-нэко ─────────────────────────────
def maneki(iid, name, fur, spots=None, paw='l', collar='#b8322a', coin='#e2b84a'):
    img = canvas(150, 186); floor_shadow(img, 75, 180, 62); fur = H(fur)
    fill(img, fur, hash(iid) % 222, ell=(20, 80, 130, 182), scale=8, contrast=.6)          # body
    fill(img, fur, 3, ell=(22, 18, 128, 104), scale=8, contrast=.6)                          # head
    for sx in (-1, 1):
        poly(img, [(75 + sx * 50, 44), (75 + sx * 44, 4), (75 + sx * 22, 30)], fur)
        poly(img, [(75 + sx * 44, 38), (75 + sx * 42, 14), (75 + sx * 28, 32)], '#e7a3a8')
    d = ImageDraw.Draw(img); rnd = random.Random(iid)
    if spots:
        for c in spots:
            cx, cy = rnd.uniform(34, 116), rnd.uniform(30, 160); r = rnd.uniform(10, 18)
            soft(img, lambda dd, cx=cx, cy=cy, r=r, c=c: dd.ellipse([px(cx - r), px(cy - r * .8), px(cx + r), px(cy + r * .8)], fill=H(c)), 1)
    d = ImageDraw.Draw(img)
    for ex in (56, 94): d.arc([px(ex - 9), px(54), px(ex + 9), px(66)], 200, 340, fill=H('#1a1414'), width=px(2.4))
    d.polygon([(px(71), px(70)), (px(79), px(70)), (px(75), px(75))], fill=H('#d77a80'))
    d.arc([px(66), px(72), px(76), px(80)], 10, 170, fill=H('#1a1414'), width=px(1.4)); d.arc([px(74), px(72), px(84), px(80)], 10, 170, fill=H('#1a1414'), width=px(1.4))
    for sx in (-1, 1):
        for k in range(3): d.line([(px(75 + sx * 18), px(74 + k * 3)), (px(75 + sx * 42), px(70 + k * 6))], fill=H('#8a8078'), width=px(1))
    d.rounded_rectangle([px(38), px(100), px(112), px(110)], px(5), fill=H(collar))
    ell(img, (68, 104, 82, 118), '#e6c048')
    x0 = 20 if paw == 'l' else 104
    fill(img, fur, 9, ell=(x0, 28, x0 + 28, 72), scale=6, contrast=.6)
    fill(img, fur, 10, rect=(x0 + 4, 50, x0 + 24, 110), scale=6, contrast=.6)
    fill(img, coin, 11, ell=(44, 118, 106, 170), scale=5, contrast=1.1)
    text(img, '千万両', 75, 144, 13, '#6a4a12', SERIF)
    volume(img, (20, 18, 130, 182), .45, .35, spec=.15)
    save(img, iid, name, 'Манэки-нэко', 'b', 110)


# ───────────────────────────── 8. Маски ─────────────────────────────
def mask(iid, name, kind):
    img = canvas(130, 176); d = ImageDraw.Draw(img)
    line(img, [(18, 70), (65, 6), (112, 70)], '#8a2a22', 1.6)
    if kind in ('kitsune', 'kitsune_black', 'neko', 'usagi'):
        base = {'kitsune': '#f3eee4', 'kitsune_black': '#1c1a1c', 'neko': '#f1ece3', 'usagi': '#f4f1ec'}[kind]
        ear = {'kitsune': (26, 16), 'kitsune_black': (26, 16), 'neko': (30, 34), 'usagi': (46, 0)}[kind]
        for sx in (-1, 1):
            if kind == 'usagi': fill(img, base, 5 + sx, ell=(65 + sx * 22 - 11, 0, 65 + sx * 22 + 11, 70), scale=6, contrast=.5)
            else: poly(img, [(65 + sx * 50, 70), (65 + sx * 44, ear[1]), (65 + sx * 14, 46)], base)
        fill(img, base, 7, poly=[(14, 64), (65, 38), (116, 64), (104, 128), (65, 172), (26, 128)] if kind != 'neko' and kind != 'usagi' else None, ell=(14, 40, 116, 164) if kind in ('neko', 'usagi') else None, scale=6, contrast=.55)
        red = '#c0302a' if kind != 'kitsune_black' else '#d4a23a'
        d = ImageDraw.Draw(img)
        for sx in (-1, 1):
            d.line([(px(65 + sx * 12), px(92)), (px(65 + sx * 34), px(84))], fill=H(red), width=px(4))
            d.arc([px(65 + sx * 24 - 12), px(78), px(65 + sx * 24 + 12), px(98)], 200, 340, fill=H('#1a1414' if kind != 'kitsune_black' else '#e8d8b0'), width=px(3))
            if kind != 'usagi': d.line([(px(65 + sx * 10), px(60)), (px(65 + sx * 22), px(44))], fill=H(red), width=px(3))
        d.ellipse([px(58), px(120 if kind not in ('neko', 'usagi') else 112), px(72), px(132 if kind not in ('neko', 'usagi') else 122)], fill=H('#1a1414' if kind != 'kitsune_black' else '#d4a23a'))
        if kind in ('neko', 'usagi'):
            for sx in (-1, 1):
                for k in range(3): d.line([(px(65 + sx * 12), px(124 + k * 4)), (px(65 + sx * 44), px(118 + k * 8))], fill=H('#9a8a80'), width=px(1.2))
        volume(img, (14, 20, 116, 172), .5, .3, spec=.18)
    elif kind in ('oni_red', 'oni_blue', 'hannya'):
        base = {'oni_red': '#b8342a', 'oni_blue': '#34507a', 'hannya': '#e8e0cc'}[kind]
        for sx in (-1, 1): poly(img, [(65 + sx * 26, 40), (65 + sx * 50, 2), (65 + sx * 40, 44)], '#e8dcbc' if kind != 'hannya' else '#c8b27a')
        fill(img, base, 11, ell=(12, 26, 118, 172), scale=6, contrast=.8)
        d = ImageDraw.Draw(img)
        for sx in (-1, 1):
            d.polygon([(px(65 + sx * 8), px(70)), (px(65 + sx * 40), px(58)), (px(65 + sx * 36), px(70))], fill=H('#1a1010'))
            ey = 84; d.ellipse([px(65 + sx * 24 - 11), px(ey - 8), px(65 + sx * 24 + 11), px(ey + 8)], fill=H('#e0b83a' if kind == 'hannya' else '#f2e8c8'))
            d.ellipse([px(65 + sx * 24 - 4), px(ey - 4), px(65 + sx * 24 + 4), px(ey + 4)], fill=H('#1a1010'))
        d.chord([px(28), px(118), px(102), px(166)], 0, 180, fill=H('#5a1010'))
        for sx in (-1, 1): d.polygon([(px(65 + sx * 26), px(140)), (px(65 + sx * 20), px(166)), (px(65 + sx * 32), px(144))], fill=H('#f2ecd8'))
        for k in range(-3, 4): d.rectangle([px(65 + k * 7 - 3), px(140), px(65 + k * 7 + 3), px(148)], fill=H('#f2ecd8'))
        volume(img, (12, 26, 118, 172), .6, .35, spec=.15)
    elif kind in ('okame', 'hyottoko'):
        base = '#f4ede0'
        fill(img, base, 13, ell=(16, 20, 114, 172), scale=6, contrast=.5)
        d = ImageDraw.Draw(img)
        if kind == 'okame':
            d.chord([px(16), px(16), px(114), px(96)], 180, 360, fill=H('#15110f'))
            for sx in (-1, 1):
                d.ellipse([px(65 + sx * 22 - 6), px(62), px(65 + sx * 22 + 6), px(68)], fill=H('#15110f'))
                d.arc([px(65 + sx * 22 - 12), px(78), px(65 + sx * 22 + 12), px(92)], 200, 340, fill=H('#15110f'), width=px(2.4))
                soft(img, lambda dd, sx=sx: dd.ellipse([px(65 + sx * 32 - 14), px(106), px(65 + sx * 32 + 14), px(126)], fill=(220, 90, 100, 150)), 3)
            d = ImageDraw.Draw(img); d.ellipse([px(58), px(136), px(72), px(146)], fill=H('#c0302a'))
        else:
            d.chord([px(16), px(18), px(114), px(70)], 180, 360, fill=H('#15110f'))
            d.ellipse([px(34), px(78), px(52), px(92)], fill=H('#15110f')); d.ellipse([px(78), px(72), px(100), px(90)], fill=H('#15110f'))
            d.ellipse([px(36), px(80), px(46), px(88)], fill=H('#f4ede0'))
            d.ellipse([px(76), px(128), px(104), px(152)], fill=H('#e6d6c0')); d.ellipse([px(84), px(134), px(98), px(146)], fill=H('#3a1212'))
            d.line([(px(40), px(120)), (px(60), px(118))], fill=H('#15110f'), width=px(2))
        volume(img, (16, 20, 114, 172), .5, .3, spec=.15)
    elif kind in ('tengu', 'tanuki', 'kappa'):
        base = {'tengu': '#b0261c', 'tanuki': '#8a6a48', 'kappa': '#5a8a4a'}[kind]
        if kind == 'tanuki':
            for sx in (-1, 1): ell(img, (65 + sx * 36 - 16, 20, 65 + sx * 36 + 16, 52), dk(H(base), .2))
        fill(img, base, 17, ell=(14, 26, 116, 170), scale=6, contrast=.8)
        d = ImageDraw.Draw(img)
        if kind == 'tengu':
            for sx in (-1, 1):
                d.polygon([(px(65 + sx * 8), px(66)), (px(65 + sx * 42), px(56)), (px(65 + sx * 36), px(70))], fill=H('#15110f'))
                d.ellipse([px(65 + sx * 22 - 8), px(74), px(65 + sx * 22 + 8), px(86)], fill=H('#f2e8c8')); d.ellipse([px(65 + sx * 22 - 3), px(77), px(65 + sx * 22 + 3), px(83)], fill=H('#15110f'))
            fill(img, base, 18, poly=[(56, 88), (74, 88), (72, 170), (64, 176)], scale=5, contrast=1)
            volume(img, (54, 86, 76, 176), .6, .2)
            d = ImageDraw.Draw(img)
            for k in range(8): d.line([(px(30 + k * 4), px(128)), (px(24 + k * 3), px(160))], fill=H('#f0ece0'), width=px(2))
            for k in range(8): d.line([(px(100 - k * 4), px(128)), (px(106 - k * 3), px(160))], fill=H('#f0ece0'), width=px(2))
        elif kind == 'tanuki':
            for sx in (-1, 1):
                soft(img, lambda dd, sx=sx: dd.ellipse([px(65 + sx * 24 - 18), px(66), px(65 + sx * 24 + 18), px(100)], fill=(40, 26, 18, 230)), 2)
            d = ImageDraw.Draw(img)
            for sx in (-1, 1): d.ellipse([px(65 + sx * 24 - 6), px(76), px(65 + sx * 24 + 6), px(88)], fill=H('#f2e8c8'))
            ell(img, (40, 100, 90, 150), '#e8dcc4'); ell(img, (58, 104, 72, 116), '#15110f')
        else:
            ell(img, (34, 18, 96, 40), '#d8d0b0')
            for sx in (-1, 1): d.ellipse([px(65 + sx * 22 - 9), px(70), px(65 + sx * 22 + 9), px(88)], fill=H('#f2e8a8')); d.ellipse([px(65 + sx * 22 - 3), px(76), px(65 + sx * 22 + 3), px(82)], fill=H('#15110f'))
            poly(img, [(46, 108), (84, 108), (65, 140)], '#d6a83a')
        volume(img, (14, 20, 116, 176), .5, .3, spec=.12)
    save(img, iid, name, 'Маски', 't', 120)


# ───────────────────────────── 9. Веера ─────────────────────────────
def sensu(iid, name, paper, motif, rib='#2a1a12'):
    img = canvas(220, 140); cx, cy, R, r = 110, 132, 108, 36
    m = Image.new('L', img.size, 0); md = ImageDraw.Draw(m)
    md.pieslice([px(cx - R), px(cy - R), px(cx + R), px(cy + R)], 200, 340, fill=255); md.pieslice([px(cx - r), px(cy - r), px(cx + r), px(cy + r)], 200, 340, fill=0)
    fill(img, paper, hash(iid) % 88, mask=m, scale=8, contrast=.7)
    d = ImageDraw.Draw(img); rnd = random.Random(iid); pc = H(paper)
    if motif == 'nami':
        for ring in range(3):
            for k in range(9):
                a = math.radians(205 + k * 16); rr = 50 + ring * 20
                x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr; d.arc([px(x - 9), px(y - 9), px(x + 9), px(y + 9)], 180, 360, fill=H('#2a4a7a'), width=px(2))
    elif motif == 'sakura':
        line(img, [(40, 84), (90, 50), (150, 44)], '#3a2418', 3)
        for _ in range(16):
            x, y = rnd.uniform(50, 170), rnd.uniform(34, 90)
            for p in range(5):
                a = p / 5 * math.tau; d.ellipse([px(x + math.cos(a) * 3.5 - 3), px(y + math.sin(a) * 3.5 - 3), px(x + math.cos(a) * 3.5 + 3), px(y + math.sin(a) * 3.5 + 3)], fill=H('#e8a0b6'))
    elif motif == 'moon':
        ell(img, (126, 40, 158, 72), '#f4e6b0')
        for x0, y0 in ((60, 70), (80, 60), (120, 80)): d.ellipse([px(x0), px(y0), px(x0 + 44), px(y0 + 14)], fill=mixc(pc, H('#8a8a9a'), .5))
    elif motif == 'gold':
        for _ in range(40):
            x, y = rnd.uniform(20, 200), rnd.uniform(20, 120)
            if math.hypot(x - cx, y - cy) < R - 4 and math.hypot(x - cx, y - cy) > r + 4: d.rectangle([px(x - 6), px(y - 6), px(x + 6), px(y + 6)], fill=hexc('#d8b048', 200))
    elif motif == 'tsuru':
        d.polygon([(px(80), px(70)), (px(110), px(50)), (px(140), px(66)), (px(112), px(62))], fill=H('#f4f0e8')); d.ellipse([px(106), px(46), px(114), px(54)], fill=H('#c0302a'))
        line(img, [(110, 54), (118, 38)], '#15110f', 2)
    elif motif == 'momiji':
        for _ in range(9):
            x, y = rnd.uniform(40, 180), rnd.uniform(34, 100)
            if math.hypot(x - cx, y - cy) > R - 8: continue
            for k in range(5):
                a = -math.pi / 2 + (k - 2) * .6; d.line([(px(x), px(y)), (px(x + math.cos(a) * 9), px(y + math.sin(a) * 9))], fill=H(rnd.choice(['#c8442a', '#e0782a', '#a0281e'])), width=px(3))
    for k in range(16):
        a = math.radians(200 + k * 140 / 15)
        d.line([(px(cx + math.cos(a) * r), px(cy + math.sin(a) * r)), (px(cx + math.cos(a) * R), px(cy + math.sin(a) * R))], fill=mixc(pc, BLACK, .18), width=px(1))
        d.line([(px(cx), px(cy)), (px(cx + math.cos(a) * r), px(cy + math.sin(a) * r))], fill=H(rib), width=px(2.4))
    ell(img, (cx - 5, cy - 5, cx + 5, cy + 5), '#b8962a')
    save(img, iid, name, 'Веера', 't', 65)


def uchiwa(iid, name, paper, motif):
    img = canvas(130, 200)
    fill(img, '#c8a870', 3, rect=(59, 110, 71, 198), scale=6, stretch=(.3, 4))
    fill(img, paper, hash(iid) % 66, ell=(8, 4, 122, 124), scale=8, contrast=.7)
    d = ImageDraw.Draw(img); rnd = random.Random(iid)
    for k in range(18):
        a = k / 18 * math.tau; d.line([(px(65), px(64)), (px(65 + math.cos(a) * 56), px(64 + math.sin(a) * 58))], fill=mixc(H(paper), BLACK, .12), width=px(1))
    if motif == 'kingyo':
        for fx, fy in ((48, 52), (78, 76)):
            d.ellipse([px(fx - 12), px(fy - 7), px(fx + 12), px(fy + 7)], fill=H('#d2402c')); d.polygon([(px(fx + 10), px(fy)), (px(fx + 22), px(fy - 9)), (px(fx + 22), px(fy + 9))], fill=H('#d2402c'))
        for _ in range(6): x, y = rnd.uniform(30, 100), rnd.uniform(20, 100); d.ellipse([px(x - 3), px(y - 3), px(x + 3), px(y + 3)], outline=H('#8ab0d0'), width=px(1))
    elif motif == 'hanabi':
        for fx, fy, c in ((46, 44, '#f0a030'), (84, 70, '#e05070'), (52, 88, '#70c0e0')):
            for k in range(16):
                a = k / 16 * math.tau; d.line([(px(fx + math.cos(a) * 4), px(fy + math.sin(a) * 4)), (px(fx + math.cos(a) * 18), px(fy + math.sin(a) * 18))], fill=H(c), width=px(1.6))
    elif motif == 'tombo':
        d.line([(px(40), px(70)), (px(92), px(56))], fill=H('#2a3a5a'), width=px(3))
        for sx in (54, 66):
            for sy in (-1, 1): d.ellipse([px(sx - 12), px(62 + sy * 9 - 4), px(sx + 12), px(62 + sy * 9 + 4)], fill=hexc('#a0c0e0', 200))
    elif motif == 'asagao':
        for fx, fy, c in ((50, 50, '#4a3ab0'), (82, 74, '#a04090'), (52, 90, '#3a70c0')):
            d.ellipse([px(fx - 14), px(fy - 14), px(fx + 14), px(fy + 14)], fill=H(c)); d.ellipse([px(fx - 4), px(fy - 4), px(fx + 4), px(fy + 4)], fill=H('#f4f0e8'))
    volume(img, (8, 4, 122, 124), .3, .2)
    save(img, iid, name, 'Веера', 't', 45)


# ───────────────────────────── 10. Посуда ─────────────────────────────
def chawan(iid, name, glaze, style, story=False):
    img = canvas(150, 100); floor_shadow(img, 75, 96, 58); g = H(glaze)
    fill(img, dk(g, .3), 4, poly=[(52, 88), (98, 88), (94, 96), (56, 96)], scale=5)
    body = [(12, 26), (138, 26), (132, 60), (112, 86), (38, 86), (18, 60)]
    fill(img, g, hash(iid) % 321, poly=body, scale=5, contrast=1.4, dark=.5, light=.3)
    d = ImageDraw.Draw(img); rnd = random.Random(iid)
    if style == 'shino':
        for _ in range(12): x, y = rnd.uniform(24, 126), rnd.uniform(34, 78); soft(img, lambda dd, x=x, y=y: dd.ellipse([px(x - 3), px(y - 3), px(x + 3), px(y + 3)], fill=(150, 70, 40, 200)), .6)
    elif style == 'oribe':
        d.polygon([(px(14), px(28)), (px(80), px(28)), (px(60), px(70)), (px(22), px(60))], fill=H('#3f6a3a'))
    elif style == 'tenmoku':
        for _ in range(30): x, y = rnd.uniform(20, 130), rnd.uniform(30, 80); d.ellipse([px(x - 1.5), px(y - 1.5), px(x + 1.5), px(y + 1.5)], fill=H(rnd.choice(['#5a6aa0', '#8aa0c0', '#a08050'])))
    elif style == 'kintsugi':
        pts = [(30, 30)]
        for _ in range(6): pts.append((pts[-1][0] + rnd.uniform(8, 18), pts[-1][1] + rnd.uniform(-2, 10)))
        line(img, pts, '#e0b040', 2.4); line(img, [(90, 40), (104, 70), (100, 84)], '#e0b040', 2)
    elif style == 'sometsuke':
        for k in range(5): d.arc([px(20 + k * 22), px(50), px(42 + k * 22), px(70)], 180, 360, fill=H('#2a4a8a'), width=px(2.2))
        d.line([(px(18), px(36)), (px(132), px(36))], fill=H('#2a4a8a'), width=px(2))
    elif style == 'hagi':
        for _ in range(40): x, y = rnd.uniform(22, 128), rnd.uniform(30, 82); d.point((px(x), px(y)), fill=H('#8a5a40'))
    volume(img, (12, 26, 138, 96), .5, .35, spec=.35)
    ImageDraw.Draw(img).ellipse([px(12), px(18), px(138), px(36)], fill=dk(g, .55))
    ImageDraw.Draw(img).ellipse([px(16), px(20), px(134), px(34)], fill=mixc(dk(g, .3), H('#3a5a3a'), .35 if style != 'raku' else 0))
    save(img, iid, name, 'Посуда', 'b', 50, story)


def vessel(iid, name, kind, col):
    col = H(col)
    if kind == 'tokkuri':
        img = canvas(110, 190); floor_shadow(img, 55, 184, 44)
        fill(img, col, 5, poly=[(44, 14), (66, 14), (64, 64), (96, 120), (92, 172), (18, 172), (14, 120), (46, 64)], scale=6, contrast=1.2)
        fill(img, col, 6, ell=(12, 90, 98, 182), scale=6, contrast=1.2)
        volume(img, (12, 14, 98, 182), .55, .35, spec=.3)
        for k in range(3): ImageDraw.Draw(img).line([(px(22), px(128 + k * 10)), (px(88), px(128 + k * 10))], fill=dk(col, .35), width=px(2))
        save(img, iid, name, 'Посуда', 'b', 60); return
    if kind == 'kyusu':
        img = canvas(190, 140); floor_shadow(img, 90, 134, 70)
        fill(img, col, 7, rect=(150, 64, 186, 76), scale=5); fill(img, col, 8, poly=[(20, 70), (42, 78), (40, 92), (4, 64)], scale=5)
        fill(img, col, 9, ell=(30, 44, 150, 132), scale=6, contrast=1.2)
        fill(img, dk(col, .1), 10, ell=(58, 34, 122, 56), scale=5); ell(img, (82, 24, 98, 38), dk(col, .3))
        volume(img, (30, 30, 150, 132), .55, .3, spec=.3)
        save(img, iid, name, 'Посуда', 'b', 90); return
    if kind == 'natsume':
        img = canvas(120, 110); floor_shadow(img, 60, 104, 50)
        fill(img, col, 11, rect=(14, 30, 106, 100), scale=6, contrast=.7); ImageDraw.Draw(img).ellipse([px(14), px(16), px(106), px(44)], fill=lt(col, .12))
        d = ImageDraw.Draw(img); d.line([(px(14), px(46)), (px(106), px(46))], fill=dk(col, .4), width=px(2))
        for k in range(5): d.arc([px(24 + k * 14), px(58), px(46 + k * 14), px(86)], 200, 330, fill=H('#d8b048'), width=px(2))
        volume(img, (14, 16, 106, 100), .4, .45, spec=.4)
        save(img, iid, name, 'Посуда', 'b', 80); return
    if kind == 'jubako':
        img = canvas(170, 170); floor_shadow(img, 85, 164, 74)
        for k in range(3):
            y0 = 40 + k * 42; fill(img, col, 12 + k, rect=(16, y0, 154, y0 + 40), scale=6, contrast=.6)
            ImageDraw.Draw(img).line([(px(16), px(y0 + 40)), (px(154), px(y0 + 40))], fill=H('#1a0a08'), width=px(2))
        fill(img, col, 20, poly=[(10, 40), (160, 40), (150, 22), (20, 22)], scale=6)
        d = ImageDraw.Draw(img)
        for _ in range(3): d.arc([px(100), px(60), px(140), px(100)], 180, 330, fill=H('#d8b048'), width=px(2.4))
        line(img, [(40, 62), (60, 90), (84, 76)], '#d8b048', 2.4)
        volume(img, (10, 22, 160, 166), .35, .25, spec=.25)
        save(img, iid, name, 'Посуда', 'b', 120); return
    if kind == 'yunomi':
        img = canvas(90, 130); floor_shadow(img, 45, 126, 36)
        fill(img, col, 21, poly=[(12, 18), (78, 18), (74, 120), (16, 120)], scale=5, contrast=1.3)
        text(img, '寿', 45, 70, 30, dk(col, .6), SERIF)
        volume(img, (12, 18, 78, 120), .5, .4, spec=.3); ImageDraw.Draw(img).ellipse([px(12), px(12), px(78), px(26)], fill=dk(col, .5))
        save(img, iid, name, 'Посуда', 'b', 40); return
    if kind == 'donburi':
        img = canvas(170, 130); floor_shadow(img, 85, 126, 66)
        fill(img, col, 22, poly=[(14, 64), (156, 64), (138, 112), (32, 112)], scale=6, contrast=1.2)
        fill(img, col, 23, ell=(20, 28, 150, 76), scale=6, contrast=1.2); ell(img, (72, 12, 98, 32), dk(col, .2))
        d = ImageDraw.Draw(img)
        for k in range(6): d.arc([px(26 + k * 20), px(78), px(46 + k * 20), px(98)], 180, 360, fill=H('#e8e0d0'), width=px(2))
        volume(img, (14, 12, 156, 124), .5, .3, spec=.3)
        save(img, iid, name, 'Посуда', 'b', 60); return


# ───────────────────────────── 11. Свитки ─────────────────────────────
def scroll(iid, name, frame, motif, story=False):
    img = canvas(150, 470); frame = H(frame)
    line(img, [(40, 4), (75, 0), (110, 4)], '#1a120c', 1.4)
    ImageDraw.Draw(img).rectangle([px(18), px(8), px(132), px(16)], fill=H('#2a1c14'))
    fill(img, frame, hash(iid) % 444, rect=(16, 14, 134, 452), scale=6, contrast=1.1)
    fill(img, '#e9e1cc', 8, rect=(28, 60, 122, 400), scale=10, contrast=.6, dark=.12, light=.1)
    ink = H('#1b1714'); rnd = random.Random(iid); d = ImageDraw.Draw(img)
    if motif.startswith('kanji:'):
        k = motif[6:]; text(img, k, 75, 200 if len(k) == 1 else 230, 70 if len(k) == 1 else 44, ink, SERIF, brush=True)
        if len(k) == 1: d.rectangle([px(96), px(330), px(112), px(346)], fill=H('#b8322a'))
    elif motif == 'enso':
        for k in range(60):
            a = math.radians(40 + k * 5.2); w = 7 * (1 - k / 70) + 1
            x, y = 75 + math.cos(a) * 36, 210 + math.sin(a) * 38; d.ellipse([px(x - w / 2), px(y - w / 2), px(x + w / 2), px(y + w / 2)], fill=ink)
    elif motif == 'moon_pine':
        ell(img, (70, 90, 108, 128), '#f2ead0'); d = ImageDraw.Draw(img); d.ellipse([px(70), px(90), px(108), px(128)], outline=ink, width=px(1))
        sub = canvas(94, 340); P.pine(sub, px(40), px(330), px(260), 5 + len(iid), [ink[:3] + (255,)] * 2 + [(60, 56, 52, 255), (90, 86, 80, 255)], (ink, ink, (60, 56, 52, 255)), lean=.3, pads=3, spread=.7)
        P.set_size(150, 470); img.alpha_composite(sub.resize((px(94), px(340))), (px(28), px(60)))
    elif motif == 'bamboo':
        for x, h0 in ((56, 70), (84, 110)):
            line(img, [(x, 390), (x + 4, h0)], ink, 5)
            for y in range(int(h0) + 30, 390, 50): d.line([(px(x - 5), px(y)), (px(x + 7), px(y))], fill=H('#e9e1cc'), width=px(2))
            for k in range(4):
                y = h0 + 20 + k * 60; s = rnd.choice((-1, 1)); d.polygon([(px(x), px(y)), (px(x + s * 34), px(y + 10)), (px(x + s * 6), px(y + 8))], fill=ink)
    elif motif == 'plum':
        line(img, [(40, 380), (60, 280), (52, 200), (84, 140), (110, 110)], ink, 5); line(img, [(58, 240), (100, 220)], ink, 3)
        for _ in range(14):
            x, y = rnd.uniform(40, 112), rnd.uniform(100, 290)
            for p in range(5): a = p / 5 * math.tau; d.ellipse([px(x + math.cos(a) * 4 - 3), px(y + math.sin(a) * 4 - 3), px(x + math.cos(a) * 4 + 3), px(y + math.sin(a) * 4 + 3)], fill=H('#c0304a'))
    elif motif == 'fuji':
        poly(img, [(28, 300), (68, 150), (82, 150), (122, 300)], '#56606a'); poly(img, [(60, 180), (68, 150), (82, 150), (90, 180), (78, 172), (72, 184)], '#f2ead8')
        for y in (310, 330): d.line([(px(30), px(y)), (px(120), px(y))], fill=hexc('#8a9098', 160), width=px(3))
        ell(img, (92, 90, 112, 110), '#b8322a')
    elif motif == 'koi':
        for fx, fy, c in ((64, 160, '#c8442a'), (86, 260, '#1a1714')):
            d.ellipse([px(fx - 10), px(fy - 26), px(fx + 10), px(fy + 26)], fill=H(c)); d.polygon([(px(fx), px(fy + 22)), (px(fx - 12), px(fy + 42)), (px(fx + 12), px(fy + 42))], fill=H(c))
        for k in range(6): d.arc([px(40), px(120 + k * 40), px(110), px(140 + k * 40)], 200, 340, fill=hexc('#6a7a8a', 150), width=px(1.4))
    elif motif == 'crane':
        d.polygon([(px(40), px(220)), (px(76), px(180)), (px(112), px(214)), (px(80), px(206))], fill=H('#f4f0e6')); d.polygon([(px(40), px(220)), (px(76), px(180)), (px(112), px(214)), (px(80), px(206))], outline=ink, width=px(1))
        line(img, [(76, 200), (84, 150), (80, 136)], ink, 2.4); ell(img, (74, 128, 86, 140), '#b8322a'); line(img, [(84, 134), (100, 138)], ink, 2)
        line(img, [(70, 212), (64, 280)], ink, 1.6); line(img, [(80, 212), (82, 282)], ink, 1.6)
    elif motif == 'nami':
        for row in range(5):
            for k in range(3):
                x, y = 44 + k * 32, 150 + row * 44; d.arc([px(x - 18), px(y - 16), px(x + 18), px(y + 16)], 180, 360, fill=H('#2a3a6a'), width=px(2.4))
        for _ in range(20): x, y = rnd.uniform(34, 116), rnd.uniform(110, 150); d.ellipse([px(x - 2), px(y - 2), px(x + 2), px(y + 2)], fill=H('#2a3a6a'))
    elif motif == 'neko':
        ell(img, (44, 220, 106, 300), '#2a2420'); ell(img, (54, 186, 96, 228), '#2a2420')
        for sx in (-1, 1): poly(img, [(75 + sx * 20, 200), (75 + sx * 18, 176), (75 + sx * 6, 192)], '#2a2420')
        line(img, [(100, 290), (118, 270), (112, 240)], '#2a2420', 5); ell(img, (86, 118, 112, 144), '#e2d6b0')
    elif motif == 'dragon':
        pts = [(40 + 60 * (0.5 + 0.5 * math.sin(k * .45)), 110 + k * 12) for k in range(22)]
        for i, (x, y) in enumerate(pts): w = 9 - i * .3; d.ellipse([px(x - w), px(y - w), px(x + w), px(y + w)], fill=ink)
        ell(img, (66, 96, 96, 118), '#1b1714'); d.ellipse([px(76), px(102), px(82), px(108)], fill=H('#d8b048'))
        for k in range(8): x, y = pts[k * 2 + 4]; d.line([(px(x), px(y)), (px(x + 12), px(y - 8))], fill=ink, width=px(2))
    d.rectangle([px(10), px(446), px(140), px(462)], fill=H('#1e140e'))
    for x in (8, 132): d.rectangle([px(x), px(444), px(x + 10), px(464)], fill=H('#caa860'))
    save(img, iid, name, 'Свитки', 't', 110, story)


# ───────────────────────────── 12. Растения ─────────────────────────────
def potted(iid, name, kind, pot_col, seed):
    tall = kind in ('iris', 'bamboo', 'wisteria', 'pine_tall')
    img = canvas(240, 360 if tall else 300); Hh = 360 if tall else 300
    floor_shadow(img, 120, Hh - 6, 92)
    base = Hh - 70
    if kind in ('pine', 'pine_tall', 'juniper'):
        pal = P.PAL_PINE if kind != 'juniper' else [hexc('#10160f'), hexc('#1a2616'), hexc('#26381f'), hexc('#34502c'), hexc('#4a6a3e')]
        P.pine(img, px(120), px(base), px(Hh * .72 if tall else 200), seed, pal, P.BARK, lean=.3 * (1 if seed % 2 else -1), pads=4, spread=.8)
    elif kind in ('momiji', 'sakura', 'ume', 'azalea', 'kiku', 'camellia', 'wisteria'):
        pal = {'momiji': [hexc('#4a1410'), hexc('#7a2418'), hexc('#a83a22'), hexc('#cc5a2c'), hexc('#e8864a')],
               'sakura': P.PAL_SAKURA, 'ume': [hexc('#5a1a2a'), hexc('#8a2a40'), hexc('#b84460'), hexc('#d8708a'), hexc('#f0a8ba')],
               'azalea': [hexc('#4a1030'), hexc('#8a1a4a'), hexc('#c02a6a'), hexc('#e2548a'), hexc('#f58ab0')],
               'kiku': [hexc('#6a6a5a'), hexc('#a8a898'), hexc('#d8d8c8'), hexc('#efefe6'), hexc('#fbfbf6')],
               'camellia': [hexc('#0e1a10'), hexc('#1a3020'), hexc('#26452c'), hexc('#8a1418'), hexc('#c02a2a')],
               'wisteria': [hexc('#2a1a4a'), hexc('#4a3478'), hexc('#6a54a0'), hexc('#9a88c8'), hexc('#c8bce6')]}[kind]
        P.maple(img, px(120), px(base), px(Hh * .7 if tall else 190), seed, pal, P.BARK, lean=.2 * (1 if seed % 2 else -1))
        if kind == 'wisteria':
            d = ImageDraw.Draw(img); rnd = random.Random(seed)
            for _ in range(10):
                x, y = rnd.uniform(40, 200), rnd.uniform(60, 140)
                for k in range(14): d.ellipse([px(x - 4 + k * .2), px(y + k * 6), px(x + 4 - k * .2), px(y + k * 6 + 6)], fill=pal[2 + k % 3])
    elif kind == 'iris':
        d = ImageDraw.Draw(img); rnd = random.Random(seed)
        for k in range(12):
            x = 90 + k * 5; top = base - rnd.uniform(160, 250); line(img, [(x, base), (x + rnd.uniform(-20, 20), top)], rnd.choice(['#2f5a2a', '#3e6a34', '#24461f']), 5)
        for x, y in ((80, base - 200), (130, base - 240), (156, base - 170)):
            for a in (-1, 1): d.ellipse([px(x + a * 10 - 10), px(y - 6), px(x + a * 10 + 10), px(y + 22)], fill=H('#4a38a0'))
            d.ellipse([px(x - 8), px(y - 24), px(x + 8), px(y + 4)], fill=H('#6a54c0')); d.line([(px(x), px(y)), (px(x), px(y + 14))], fill=H('#e8c040'), width=px(3))
    elif kind == 'bamboo':
        d = ImageDraw.Draw(img); rnd = random.Random(seed)
        for i, (x, h) in enumerate([(100, 250), (130, 280), (150, 220)]):
            top = base - h; fill(img, '#56643e', seed + i, poly=[(x - 7, base), (x + 7, base), (x + 6, top), (x - 6, top)], scale=20, stretch=(.2, 4), contrast=1.2)
            for y in range(int(top) + 40, int(base), 50): ImageDraw.Draw(img).rectangle([px(x - 8), px(y), px(x + 8), px(y + 3)], fill=H('#2c341f'))
            for k in range(3):
                y = top + 20 + k * 60; s = rnd.choice((-1, 1)); P.dab_mass(ImageDraw.Draw(img), [(px(x + s * 30), px(y), px(30), px(8))], 50, 'leaf', P.PAL_MAPLE, rnd, size=(5, 10))
    elif kind == 'moss':
        fill(img, '#2c3b22', seed, ell=(30, base - 60, 210, base + 10), scale=5, contrast=1.4)
        P.dab_mass(ImageDraw.Draw(img), [(px(120), px(base - 34), px(80), px(26))], 900, 'leaf', [hexc('#1a2614'), hexc('#2a3e20'), hexc('#3e5a2c'), hexc('#5a7a3c'), hexc('#7a9a4c')], random.Random(seed), size=(2, 5))
        for sx, sy, r in ((80, base - 40, 14), (150, base - 30, 18)): P.stone(img, px(sx), px(sy), px(r), px(r * .7), seed + sx)
    elif kind == 'orchid':
        d = ImageDraw.Draw(img)
        for sx in (-1, 1): d.polygon([(px(120), px(base)), (px(120 + sx * 80), px(base - 30)), (px(120 + sx * 20), px(base - 12))], fill=H('#2f5a2a'))
        line(img, [(120, base), (126, base - 150), (170, base - 190)], '#3a4a2a', 2.4)
        for k in range(5):
            x, y = 128 + k * 10, base - 150 - k * 9
            for a in range(5): ang = a / 5 * math.tau; d.ellipse([px(x + math.cos(ang) * 8 - 8), px(y + math.sin(ang) * 8 - 6), px(x + math.cos(ang) * 8 + 8), px(y + math.sin(ang) * 8 + 6)], fill=H('#f2e6f0'))
            d.ellipse([px(x - 4), px(y - 3), px(x + 4), px(y + 5)], fill=H('#c04a8a'))
    pc = H(pot_col)
    fill(img, pc, seed + 99, poly=[(56, base - 6), (184, base - 6), (170, Hh - 8), (70, Hh - 8)], scale=6, contrast=1.3)
    ImageDraw.Draw(img).rectangle([px(50), px(base - 14), px(190), px(base - 2)], fill=dk(pc, .3))
    ImageDraw.Draw(img).ellipse([px(58), px(base - 18), px(182), px(base - 4)], fill=H('#2c3524'))
    volume(img, (50, base - 18, 190, Hh - 8), .5, .3, spec=.2)
    save(img, iid, name, 'Растения', 'b', 140)


# ───────────────────────────── 13. Подушки и ткани ─────────────────────────────
def zabuton(iid, name, base, pattern, fg):
    img = canvas(320, 124); base = H(base); fg = H(fg)
    floor_shadow(img, 160, 118, 150, 90)
    polyp = [(30, 40), (290, 40), (312, 102), (8, 102)]
    fill(img, base, hash(iid) % 700, poly=polyp, scale=18, stretch=(3, 1), contrast=.9)
    m = mask_poly(img, poly=polyp); l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l); rnd = random.Random(iid)
    if pattern == 'seigaiha':
        for row in range(5):
            for x in range(10 - row * 4, 320, 26): d.arc([px(x), px(38 + row * 13), px(x + 26), px(58 + row * 13)], 180, 360, fill=fg, width=px(1.6))
    elif pattern == 'shippo':
        for y in range(38, 104, 18):
            for x in range(0, 320, 18): d.ellipse([px(x), px(y), px(x + 18), px(y + 18)], outline=fg, width=px(1.2))
    elif pattern == 'ichimatsu':
        for yi, y in enumerate(range(40, 104, 16)):
            for xi, x in enumerate(range(0, 320, 20)):
                if (xi + yi) % 2: d.rectangle([px(x), px(y), px(x + 20), px(y + 16)], fill=fg)
    elif pattern == 'yagasuri':
        for x in range(0, 330, 22):
            for y in range(36, 104, 20): d.polygon([(px(x), px(y)), (px(x + 11), px(y + 6)), (px(x + 11), px(y + 20)), (px(x), px(y + 14))], fill=fg)
    elif pattern == 'uroko':
        for yi, y in enumerate(range(40, 104, 16)):
            for x in range(-10 + (yi % 2) * 10, 330, 20):
                if yi % 2 == 0: d.polygon([(px(x), px(y + 16)), (px(x + 10), px(y)), (px(x + 20), px(y + 16))], fill=fg)
    elif pattern == 'kikko':
        for yi, y in enumerate(range(36, 110, 16)):
            for x in range(-10 + (yi % 2) * 14, 330, 28):
                pts = [(x + 7, y), (x + 21, y), (x + 28, y + 8), (x + 21, y + 16), (x + 7, y + 16), (x, y + 8)]; d.polygon([(px(a), px(b)) for a, b in pts], outline=fg, width=px(1.2))
    elif pattern == 'sakura':
        for _ in range(26):
            x, y = rnd.uniform(20, 300), rnd.uniform(44, 100)
            for p in range(5): a = p / 5 * math.tau; d.ellipse([px(x + math.cos(a) * 3.5 - 3), px(y + math.sin(a) * 3.5 - 3), px(x + math.cos(a) * 3.5 + 3), px(y + math.sin(a) * 3.5 + 3)], fill=fg)
    elif pattern == 'tatewaku':
        for x in range(0, 330, 30):
            pts = [(x + 8 * math.sin(y / 8), y) for y in range(36, 106, 4)]; d.line([(px(a), px(b)) for a, b in pts], fill=fg, width=px(2.2))
    a = np.asarray(l, np.float32); a[..., 3] *= np.asarray(m, np.float32) / 255 * .8; img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))
    d = ImageDraw.Draw(img)
    for x, y in ((30, 40), (290, 40), (312, 102), (8, 102)): d.ellipse([px(x - 5), px(y - 5), px(x + 5), px(y + 5)], fill=dk(base, .3))
    edge = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(edge).polygon([(px(8), px(102)), (px(312), px(102)), (px(305), px(116)), (px(15), px(116))], fill=dk(base, .6)); img.alpha_composite(edge)
    save(img, iid, name, 'Подушки', 'b', 60)


def furoshiki(iid, name, col, fg):
    img = canvas(170, 150); floor_shadow(img, 85, 144, 70)
    fill(img, col, 3, poly=[(20, 140), (150, 140), (160, 90), (120, 50), (50, 50), (10, 90)], scale=8, contrast=.8)
    for sx in (-1, 1): fill(img, col, 4 + sx, poly=[(85, 50), (85 + sx * 46, 8), (85 + sx * 34, 40)], scale=6)
    d = ImageDraw.Draw(img); rnd = random.Random(iid)
    for _ in range(18): x, y = rnd.uniform(24, 146), rnd.uniform(60, 134); d.ellipse([px(x - 4), px(y - 4), px(x + 4), px(y + 4)], outline=H(fg), width=px(1.4))
    ell(img, (70, 36, 100, 60), dk(H(col), .15))
    volume(img, (10, 8, 160, 140), .5, .35)
    save(img, iid, name, 'Подушки', 'b', 50)


# ───────────────────────────── 14. Игрушки ─────────────────────────────
def temari(iid, name, base, cols):
    img = canvas(110, 116); floor_shadow(img, 55, 112, 44)
    fill(img, base, hash(iid) % 55, ell=(8, 8, 102, 110), scale=4, contrast=.6)
    d = ImageDraw.Draw(img); cx, cy = 55, 59
    for i, c in enumerate(cols):
        for k in range(8):
            a = k / 8 * math.pi + i * .2
            d.line([(px(cx + math.cos(a) * 46), px(cy + math.sin(a) * 50)), (px(cx - math.cos(a) * 46), px(cy - math.sin(a) * 50))], fill=H(c), width=px(2.2 - i * .4))
        d.ellipse([px(cx - 30 + i * 8), px(cy - 30 + i * 8), px(cx + 30 - i * 8), px(cy + 30 - i * 8)], outline=H(c), width=px(2))
    volume(img, (8, 8, 102, 110), .6, .5, spec=.25)
    save(img, iid, name, 'Игрушки', 'b', 40)


def toy(iid, name, kind, col='#b8322a'):
    col = H(col)
    if kind == 'kendama':
        img = canvas(110, 210); floor_shadow(img, 55, 204, 40)
        fill(img, '#c9a070', 3, poly=[(48, 60), (62, 60), (60, 200), (50, 200)], scale=6, stretch=(.3, 3)); fill(img, '#c9a070', 4, rect=(18, 60, 92, 76), scale=5)
        fill(img, '#c9a070', 5, ell=(10, 50, 30, 86), scale=5); fill(img, '#c9a070', 6, ell=(80, 50, 100, 86), scale=5)
        line(img, [(55, 110), (86, 80), (74, 30)], '#e8dcc0', 1.2)
        fill(img, col, 7, ell=(46, 2, 104, 58), scale=5, contrast=1.1); volume(img, (46, 2, 104, 58), .6, .45, spec=.35)
        save(img, iid, name, 'Игрушки', 'b', 35); return
    if kind == 'koma':
        img = canvas(110, 130); floor_shadow(img, 55, 126, 30)
        fill(img, col, 3, poly=[(8, 50), (102, 50), (60, 118), (50, 118)], scale=5)
        fill(img, col, 4, ell=(8, 34, 102, 66), scale=5)
        d = ImageDraw.Draw(img)
        for k, c in enumerate(['#e0b040', '#2a4a8a', '#f2ecd8']): d.arc([px(14 + k * 12), px(38 + k * 4), px(96 - k * 12), px(62 - k * 4)], 0, 360, fill=H(c), width=px(3))
        fill(img, '#6a4a2a', 5, rect=(50, 8, 60, 44), scale=4)
        volume(img, (8, 8, 102, 118), .5, .3, spec=.3)
        save(img, iid, name, 'Игрушки', 'b', 30); return
    if kind == 'tsuru':
        img = canvas(150, 110); floor_shadow(img, 75, 104, 50)
        poly(img, [(10, 70), (70, 40), (78, 98)], lt(col, .1)); poly(img, [(140, 70), (80, 40), (78, 98)], col)
        poly(img, [(70, 40), (80, 40), (78, 98)], dk(col, .3)); poly(img, [(76, 60), (120, 8), (112, 30), (92, 64)], lt(col, .05)); poly(img, [(112, 30), (120, 8), (126, 26)], dk(col, .2))
        save(img, iid, name, 'Игрушки', 'b', 20); return
    if kind == 'tako':
        img = canvas(150, 230)
        fill(img, '#f0e6cc', 3, poly=[(10, 10), (140, 10), (140, 170), (10, 170)], scale=8, contrast=.6)
        text(img, '龍', 75, 90, 90, col, SERIF, brush=True)
        d = ImageDraw.Draw(img); d.line([(px(10), px(10)), (px(140), px(170))], fill=H('#3a2a1a'), width=px(2)); d.line([(px(140), px(10)), (px(10), px(170))], fill=H('#3a2a1a'), width=px(2))
        for k in range(2): line(img, [(50 + k * 50, 170), (40 + k * 60 + 10 * math.sin(k), 200), (56 + k * 44, 228)], '#b8322a', 3)
        save(img, iid, name, 'Игрушки', 't', 60); return
    if kind == 'otoshi':
        img = canvas(110, 190); floor_shadow(img, 55, 184, 44)
        for k, c in enumerate(['#2a6a3a', '#e0b040', '#2a4a8a', '#b8322a', '#6a3a8a']):
            y0 = 150 - k * 24; fill(img, c, 10 + k, rect=(14, y0, 96, y0 + 24), scale=4, contrast=.8)
        fill(img, '#b8322a', 20, ell=(22, 8, 88, 34 + 22), scale=5); ell(img, (38, 20, 72, 44), '#f2ecd8')
        volume(img, (14, 8, 96, 174), .45, .25, spec=.2)
        save(img, iid, name, 'Игрушки', 'b', 45); return
    if kind == 'denden':
        img = canvas(120, 220); floor_shadow(img, 60, 214, 30)
        fill(img, '#8a5a30', 3, rect=(56, 90, 64, 216), scale=4)
        fill(img, col, 4, ell=(18, 16, 102, 96), scale=5); ImageDraw.Draw(img).ellipse([px(34), px(30), px(86), px(82)], fill=H('#f0e2c0'))
        text(img, '福', 60, 56, 32, col, SERIF)
        for sx in (-1, 1): line(img, [(60 + sx * 40, 56), (60 + sx * 54, 74)], '#e8dcc0', 1.2); ell(img, (60 + sx * 54 - 5, 70, 60 + sx * 54 + 5, 80), '#2a2020')
        volume(img, (18, 16, 102, 96), .4, .3)
        save(img, iid, name, 'Игрушки', 'b', 30); return
    if kind == 'mouse':
        img = canvas(140, 90); floor_shadow(img, 70, 86, 50)
        line(img, [(20, 70), (4, 40), (20, 14)], '#8a7a70', 2)
        fill(img, col, 3, ell=(18, 30, 120, 84), scale=5, contrast=.6); ell(img, (94, 22, 116, 46), dk(col, .15)); ell(img, (98, 26, 112, 42), '#e8a8a8')
        ell(img, (112, 52, 118, 58), '#1a1414'); ell(img, (118, 60, 126, 66), '#d88088')
        volume(img, (18, 22, 126, 84), .5, .4, spec=.25)
        save(img, iid, name, 'Игрушки', 'b', 15); return
    if kind == 'yarn':
        img = canvas(110, 104); floor_shadow(img, 55, 100, 46)
        fill(img, col, 3, ell=(8, 4, 102, 98), scale=4, contrast=.9)
        l = Image.new('RGBA', img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(l); rr = random.Random(iid)
        for k in range(46):
            ang = rr.uniform(0, 180); w2 = rr.uniform(30, 47); h2 = rr.uniform(8, 46); cxx, cyy = 55, 51
            pts = []
            for j in range(40):
                t = math.pi * j / 39; x0, y0 = math.cos(t) * w2, math.sin(t) * h2 * rr.choice((1, -1)) if j == 0 else math.sin(t) * h2
                ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang)); pts.append((px(cxx + x0 * ca - y0 * sa), px(cyy + x0 * sa + y0 * ca)))
            ld.line(pts, fill=lt(col, rr.uniform(.05, .3)) if k % 3 else dk(col, .35), width=px(1.3))
        m = mask_poly(img, ell=(9, 5, 101, 97)); a = np.asarray(l, np.float32); a[..., 3] *= np.asarray(m, np.float32) / 255; img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))
        line(img, [(96, 70), (104, 90), (100, 102)], col, 2.4)
        volume(img, (8, 4, 102, 98), .6, .5, spec=.05)
        save(img, iid, name, 'Игрушки', 'b', 15); return
    if kind == 'teaser':
        img = canvas(90, 250); floor_shadow(img, 60, 246, 22)
        line(img, [(60, 246), (46, 60)], '#6a4a2a', 4); line(img, [(46, 60), (30, 30), (24, 10)], '#d8d0c0', 1.2)
        for k in range(6): a = -1.2 + k * .5; line(img, [(24, 10), (24 + math.cos(a) * 22, 10 + math.sin(a) * 30 + 20)], rnd_col(k), 3)
        save(img, iid, name, 'Игрушки', 'b', 20); return
    if kind == 'suzu':
        img = canvas(90, 100); floor_shadow(img, 45, 96, 34)
        fill(img, '#d8b048', 3, ell=(10, 14, 80, 92), scale=4, contrast=1.3); d = ImageDraw.Draw(img)
        d.line([(px(12), px(56)), (px(78), px(56))], fill=H('#6a4a12'), width=px(2)); d.ellipse([px(38), px(62), px(52), px(76)], fill=H('#3a2a08')); d.line([(px(45), px(70)), (px(45), px(90))], fill=H('#3a2a08'), width=px(2))
        line(img, [(45, 14), (30, 2), (60, 2), (45, 14)], '#b8322a', 2.4)
        volume(img, (10, 14, 80, 92), .7, .4, spec=.5)
        save(img, iid, name, 'Игрушки', 'b', 25); return


def rnd_col(k): return ['#d8b048', '#b8322a', '#e8e0d0', '#2a4a8a', '#6a3a8a', '#2f6b3a'][k % 6]


# ───────────────────────────── 15. Зонтики ─────────────────────────────
def wagasa(iid, name, col, pattern):
    img = canvas(240, 240); floor_shadow(img, 120, 234, 60); col = H(col)
    line(img, [(120, 90), (124, 234)], '#6a4a2a', 4)
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).pieslice([px(8), px(20), px(232), px(200)], 180, 360, fill=255)
    fill(img, col, hash(iid) % 91, mask=m, scale=8, contrast=.9)
    d = ImageDraw.Draw(img); cx, cy = 120, 110
    if pattern == 'janome': d.arc([px(34), px(40), px(206), px(180)], 180, 360, fill=H('#f2ecd8'), width=px(14))
    elif pattern == 'sakura':
        rnd = random.Random(iid)
        for _ in range(18):
            x, y = rnd.uniform(30, 210), rnd.uniform(40, 104)
            if math.hypot((x - 120) / 112, (y - 110) / 90) > 1: continue
            for p in range(5): a = p / 5 * math.tau; d.ellipse([px(x + math.cos(a) * 4 - 3.5), px(y + math.sin(a) * 4 - 3.5), px(x + math.cos(a) * 4 + 3.5), px(y + math.sin(a) * 4 + 3.5)], fill=H('#f4c4d2'))
    elif pattern == 'kiku': d.arc([px(70), px(70), px(170), px(150)], 180, 360, fill=H('#e8c040'), width=px(10))
    for k in range(13):
        a = math.radians(180 + k * 15); d.line([(px(cx), px(cy)), (px(cx + math.cos(a) * 112), px(cy + math.sin(a) * 90))], fill=dk(col, .35), width=px(1.2))
    ImageDraw.Draw(img).rectangle([px(8), px(108), px(232), px(112)], fill=dk(col, .45))
    volume(img, (8, 20, 232, 112), .35, .2)
    ell(img, (114, 12, 126, 24), '#2a1a12')
    save(img, iid, name, 'Зонтики', 'b', 90)


# ───────────────────────────── 16. Цукумогами ─────────────────────────────
def one_eye(img, x, y, r, red=True):
    ell(img, (x - r, y - r * .8, x + r, y + r * .8), '#f6f0e0')
    if red: ImageDraw.Draw(img).ellipse([px(x - r), px(y - r * .8), px(x + r), px(y + r * .8)], outline=H('#a02020'), width=px(1.4))
    ell(img, (x - r * .45, y - r * .45, x + r * .45, y + r * .45), '#1a0e0a')
    ell(img, (x - r * .3, y - r * .38, x - r * .05, y - r * .15), '#ffffff')


def tongue(img, x, y, L, w=10):
    fill(img, '#c83a44', 3, poly=[(x - w / 2, y), (x + w / 2, y), (x + w * .6, y + L * .7), (x, y + L), (x - w * .3, y + L * .8)], scale=4, contrast=.8)


def tsukumo(iid, name, kind):
    if kind == 'kasa':
        img = canvas(200, 260); floor_shadow(img, 104, 254, 40)
        m = Image.new('L', img.size, 0); ImageDraw.Draw(m).polygon([(px(100), px(8)), (px(190), px(170)), (px(10), px(170))], fill=255)
        fill(img, '#6a2a24', 3, mask=m, scale=8, contrast=1.2)
        d = ImageDraw.Draw(img)
        for k in range(7): d.line([(px(100), px(10)), (px(18 + k * 27), px(170))], fill=H('#3a1410'), width=px(1.4))
        one_eye(img, 100, 96, 24); tongue(img, 96, 134, 70, 16)
        line(img, [(104, 170), (104, 234)], '#5a3a22', 5); fill(img, '#3a2a1e', 5, poly=[(84, 234), (128, 234), (126, 254), (82, 254)], scale=4)
        save(img, iid, name, 'Цукумогами', 'b', 150); return
    if kind == 'chochin':
        img = canvas(140, 240)
        line(img, [(70, 0), (70, 24)], '#120c09', 2)
        fill(img, '#e6d6b0', 3, ell=(10, 28, 130, 220), scale=5, contrast=1)
        a = np.asarray(img, np.float32)
        for k in range(1, 12): yk = px(28 + 192 * k / 12); a[max(0, yk - 1):yk + 1, :, :3] *= .55
        img = Image.fromarray(a.astype(np.uint8), 'RGBA')
        one_eye(img, 70, 90, 20); d = ImageDraw.Draw(img)
        d.polygon([(px(28), px(140)), (px(112), px(132)), (px(104), px(160)), (px(36), px(164))], fill=H('#2a0c0a'))
        tongue(img, 70, 150, 90, 18); volume(img, (10, 28, 130, 220), .4, .35)
        save(img, iid, name, 'Цукумогами', 't', 150, glow=[70, 110]); return
    if kind == 'zori':
        img = canvas(170, 120); floor_shadow(img, 85, 114, 70)
        fill(img, '#b8a070', 3, ell=(10, 40, 160, 112), scale=6, stretch=(3, 1)); line(img, [(40, 60), (85, 44), (130, 60)], '#8a1a1a', 5)
        one_eye(img, 85, 82, 16); tongue(img, 130, 90, 30, 10)
        save(img, iid, name, 'Цукумогами', 'b', 120); return
    if kind == 'chawan':
        img = canvas(150, 120); floor_shadow(img, 75, 114, 58)
        fill(img, '#3a2a24', 3, poly=[(12, 30), (138, 30), (132, 64), (112, 96), (38, 96), (18, 64)], scale=5, contrast=1.3)
        one_eye(img, 75, 60, 18); tongue(img, 104, 80, 30, 10); ell(img, (12, 22, 138, 38), '#1a120e')
        volume(img, (12, 22, 138, 104), .5, .3, spec=.3)
        save(img, iid, name, 'Цукумогами', 'b', 120); return
    if kind == 'shoji':
        img = canvas(170, 260); floor_shadow(img, 85, 254, 76)
        fill(img, '#e2dac4', 3, rect=(10, 10, 160, 250), scale=10, contrast=.6)
        d = ImageDraw.Draw(img)
        for x in (10, 60, 110, 160): d.line([(px(x), px(10)), (px(x), px(250))], fill=H('#2a1c14'), width=px(4))
        for y in (10, 70, 130, 190, 250): d.line([(px(10), px(y)), (px(160), px(y))], fill=H('#2a1c14'), width=px(4))
        for (x, y) in ((35, 40), (135, 100), (85, 160), (35, 220), (135, 220)): one_eye(img, x, y, 11)
        save(img, iid, name, 'Цукумогами', 'b', 180); return
    if kind == 'tetsubin':
        img = canvas(170, 170); floor_shadow(img, 85, 164, 64)
        fill(img, '#2a2622', 3, ell=(20, 50, 150, 164), scale=4, contrast=1.4); line(img, [(40, 60), (85, 14), (130, 60)], '#1a1714', 5)
        one_eye(img, 85, 100, 18); fill(img, '#2a2622', 4, poly=[(140, 100), (168, 80), (164, 92), (146, 116)], scale=4)
        tongue(img, 160, 88, 36, 8); volume(img, (20, 50, 150, 164), .5, .35, spec=.2)
        save(img, iid, name, 'Цукумогами', 'b', 140); return
    if kind == 'geta':
        img = canvas(170, 110); floor_shadow(img, 85, 104, 70)
        fill(img, '#9a7a4a', 3, rect=(10, 36, 160, 62), scale=6, stretch=(4, 1))
        for x in (36, 116): fill(img, '#7a5a34', x, rect=(x - 8, 62, x + 12, 100), scale=5)
        line(img, [(50, 36), (85, 20), (120, 36)], '#1a1a4a', 4); one_eye(img, 85, 48, 11); tongue(img, 150, 60, 34, 8)
        save(img, iid, name, 'Цукумогами', 'b', 110); return
    if kind == 'biwa':
        img = canvas(150, 280); floor_shadow(img, 75, 274, 50)
        fill(img, '#8a5028', 3, ell=(14, 110, 136, 272), scale=6, stretch=(.6, 2)); fill(img, '#6a3a1a', 4, poly=[(64, 14), (86, 14), (84, 120), (66, 120)], scale=5)
        for k in range(4): line(img, [(68 + k * 5, 20), (62 + k * 9, 250)], '#e8dcc0', .8)
        one_eye(img, 75, 186, 20); volume(img, (14, 110, 136, 272), .5, .35, spec=.2)
        save(img, iid, name, 'Цукумогами', 'b', 160); return


# ───────────────────────────── 17. Реликвии сюжета ─────────────────────────────
def relic_bell():
    img = canvas(100, 170)
    line(img, [(50, 0), (50, 60)], '#b8322a', 3); fill(img, '#b8322a', 5, poly=[(30, 60), (70, 60), (60, 80), (40, 80)], scale=4)
    for sx in (-1, 1): line(img, [(50, 70), (50 + sx * 24, 110), (50 + sx * 18, 150)], '#b8322a', 2.4)
    fill(img, '#d8b048', 3, ell=(20, 84, 80, 150), scale=4, contrast=1.3); d = ImageDraw.Draw(img)
    d.line([(px(22), px(118)), (px(78), px(118))], fill=H('#6a4a12'), width=px(2)); d.ellipse([px(43), px(122), px(57), px(136)], fill=H('#3a2a08'))
    volume(img, (20, 84, 80, 150), .7, .4, spec=.5)
    save(img, 'r_bell', 'Бубенчик дзасики-вараси', 'Реликвии', 't', 0, True)


def relic_ribbon():
    img = canvas(160, 110)
    fill(img, '#c02a2a', 3, poly=[(80, 50), (20, 14), (8, 40), (28, 62), (8, 90), (70, 64)], scale=5, contrast=1.2)
    fill(img, '#c02a2a', 4, poly=[(80, 50), (140, 14), (152, 40), (132, 62), (152, 90), (90, 64)], scale=5, contrast=1.2)
    fill(img, '#9a1a1a', 5, ell=(66, 38, 94, 70), scale=4); line(img, [(74, 66), (60, 108)], '#a82020', 5); line(img, [(86, 66), (100, 104)], '#a82020', 5)
    volume(img, (8, 14, 152, 108), .5, .25, spec=.2)
    save(img, 'r_ribbon', 'Красная ленточка', 'Реликвии', 'b', 0, True)


def relic_pearl():
    img = canvas(120, 110); floor_shadow(img, 60, 106, 44)
    fill(img, '#6a8a6a', 3, ell=(8, 60, 112, 104), scale=5, contrast=1.1)
    fill(img, '#dfe8e6', 4, ell=(30, 16, 90, 76), scale=3, contrast=.4); volume(img, (30, 16, 90, 76), .7, .5, spec=.8)
    soft(img, lambda d: d.ellipse([px(24), px(10), px(96), px(82)], outline=(200, 240, 255, 120), width=px(4)), 3)
    save(img, 'r_pearl', 'Жемчужина каппы', 'Реликвии', 'b', 0, True)


def relic_candle():
    img = canvas(90, 170); floor_shadow(img, 45, 164, 36)
    fill(img, '#2a2420', 3, poly=[(14, 150), (76, 150), (70, 164), (20, 164)], scale=4)
    fill(img, '#e8dcc0', 4, poly=[(32, 90), (58, 86), (58, 150), (32, 150)], scale=4); poly(img, [(32, 90), (40, 110), (46, 92), (58, 86)], '#f4ecd8')
    soft(img, lambda d: d.ellipse([px(26), px(20), px(66), px(84)], fill=(140, 180, 255, 110)), 5)
    fill(img, '#8ab8ff', 5, poly=[(45, 34), (54, 62), (45, 80), (36, 62)], scale=3)
    ell(img, (42, 60, 48, 78), '#f0f6ff')
    save(img, 'r_candle', 'Огарок сотой свечи', 'Реликвии', 'b', 0, True, glow=[45, 60])


def relic_brush():
    img = canvas(200, 90)
    fill(img, '#6a4424', 3, poly=[(8, 44), (110, 38), (110, 50), (8, 52)], scale=5, stretch=(4, 1))
    fill(img, '#f4efe6', 4, poly=[(108, 30), (150, 18), (196, 44), (150, 76), (108, 60)], scale=5, contrast=.5)
    fill(img, '#c0402a', 5, poly=[(170, 30), (196, 44), (170, 62), (180, 44)], scale=4)
    volume(img, (8, 18, 196, 76), .4, .2)
    save(img, 'r_foxbrush', 'Лисья кисточка', 'Реликвии', 'b', 0, True)


def relic_mirror():
    img = canvas(140, 200); floor_shadow(img, 70, 194, 50)
    fill(img, '#6a4a1a', 3, rect=(60, 120, 80, 196), scale=4); fill(img, '#b08a3a', 4, ell=(10, 6, 130, 126), scale=4, contrast=1.3)
    fill(img, '#b8c8cc', 5, ell=(22, 18, 118, 114), scale=6, contrast=.5); volume(img, (22, 18, 118, 114), .6, .3, spec=.6)
    soft(img, lambda d: d.ellipse([px(54), px(44), px(86), px(90)], fill=(200, 40, 40, 70)), 6)
    save(img, 'r_mirror', 'Зеркальце хранительницы', 'Реликвии', 'b', 0, True)


def relic_key():
    img = canvas(170, 80)
    fill(img, '#4a4038', 3, ell=(6, 14, 58, 66), scale=4, contrast=1.3); ImageDraw.Draw(img).ellipse([px(20), px(28), px(44), px(52)], fill=(0, 0, 0, 0))
    fill(img, '#4a4038', 4, rect=(54, 34, 160, 46), scale=4); fill(img, '#4a4038', 5, rect=(130, 46, 142, 66), scale=4); fill(img, '#4a4038', 6, rect=(148, 46, 158, 60), scale=4)
    line(img, [(30, 10), (22, 0)], '#b8322a', 3)
    volume(img, (6, 14, 160, 66), .5, .2, spec=.3)
    save(img, 'r_key', 'Ключ от старой кладовой', 'Реликвии', 'b', 0, True)


# ───────────────────────────── catalogue ─────────────────────────────
def build():
    O = [('om_luck', 'Омамори удачи', '#b8322a', '福'), ('om_health', 'Омамори здоровья', '#2f6b3a', '健'), ('om_study', 'Омамори учёбы', '#2a4a8a', '学'),
         ('om_love', 'Омамори любви', '#d86a8a', '恋'), ('om_ward', 'Омамори от бед', '#1a1a1e', '厄'), ('om_road', 'Омамори дороги', '#6a3a8a', '交'),
         ('om_home', 'Омамори дома', '#8a5a2a', '家'), ('om_cat', 'Кошачье омамори', '#f2ecd8', '猫'), ('om_sleep', 'Омамори сна', '#34507a', '夢'),
         ('om_money', 'Омамори богатства', '#c89a2a', '金'), ('om_fire', 'Омамори от пожара', '#a02a1a', '火'), ('om_water', 'Омамори воды', '#2a6a7a', '水'),
         ('om_kid', 'Детское омамори', '#e8a0b6', '子'), ('om_art', 'Омамори искусства', '#4a2a5a', '芸'), ('om_ghost', 'Омамори от призраков', '#e8e4dc', '魔'),
         ('om_moon', 'Лунное омамори', '#20283a', '月')]
    for iid, n, c, k in O: omamori(iid, n, c, k, '#1a1a1e' if c in ('#f2ecd8', '#e8e4dc') else '#c9a24a')
    Z = [('子', 'мыши', 'sun'), ('丑', 'быка', 'cloud'), ('寅', 'тигра', 'bamboo'), ('卯', 'зайца', 'wave'), ('辰', 'дракона', 'cloud'), ('巳', 'змеи', 'wave'),
         ('午', 'лошади', 'sun'), ('未', 'овцы', 'plum'), ('申', 'обезьяны', 'bamboo'), ('酉', 'петуха', 'sun'), ('戌', 'собаки', 'plum'), ('亥', 'кабана', 'cloud')]
    for i, (k, an, mo) in enumerate(Z): ema(f'ema_{i:02d}', f'Эма года {an}', k, ['#c8342a', '#2a6a8a', '#3a7a3a', '#c07a2a'][i % 4], mo)
    CH = [('ch_matsuri', 'Фонарь «Праздник»', '#a3322a', '祭', True), ('ch_white', 'Белый фонарь', '#efe6d0', '灯', True), ('ch_luck', 'Фонарь удачи', '#c84a2a', '福', False),
          ('ch_dream', 'Фонарь снов', '#2a3a6a', '夢', True), ('ch_moon', 'Лунный фонарь', '#e0d0a0', '月', False), ('ch_cat', 'Кошачий фонарь', '#d88a3a', '猫', False),
          ('ch_black', 'Чёрный фонарь', '#1c1a1c', '鬼', True), ('ch_green', 'Зелёный фонарь', '#3a6a4a', '森', True), ('ch_sakura', 'Фонарь сакуры', '#e8a0b6', '桜', False),
          ('ch_fox', 'Лисий фонарь', '#e8c860', '狐', True), ('ch_rain', 'Фонарь дождя', '#4a6a8a', '雨', False), ('ch_hundred', 'Фонарь ста историй', '#7a1a1a', '百', True)]
    for iid, n, c, k, tall in CH: chochin(iid, n, c, k, tall, ink='#e8d8b0' if c in ('#1c1a1c', '#2a3a6a', '#7a1a1a') else '#1a0806')
    andon('an_square', 'Андон квадратный', 'square'); andon('an_tall', 'Андон высокий', 'tall', mark='夜'); andon('an_moon', 'Андон с луной', 'square', mark='moon')
    andon('an_maru', 'Круглый андон', 'maru'); andon('an_maru_k', 'Андон «Покой»', 'maru', mark='静'); andon('an_toro', 'Садовый торо', 'toro')
    andon('an_yukimi', 'Фонарь юкими', 'yukimi'); andon('an_red', 'Алый андон', 'square', paper='#e8a080', frame='#3a1410')
    F = [('fu_kingyo', 'Фурин с рыбками', '#b9d6e6', 'kingyo'), ('fu_asagao', 'Фурин с вьюнком', '#d6e4f0', 'asagao'), ('fu_hanabi', 'Фурин «Фейерверк»', '#2a3450', 'hanabi'),
         ('fu_tombo', 'Фурин со стрекозой', '#cfe6d8', 'tombo'), ('fu_momiji', 'Осенний фурин', '#f0e0c8', 'momiji'), ('fu_dots', 'Фурин «Капли»', '#6b8fbf', 'dots'),
         ('fu_nami', 'Фурин «Волны»', '#4a7aa8', 'nami'), ('fu_pink', 'Розовый фурин', '#f0c8d4', 'dots')]
    for iid, n, g, mo in F: furin(iid, n, g, mo)
    furin('fu_nanbu', 'Чугунный фурин нанбу', '#2a2622', None, True, ch='鉄'); furin('fu_bronze', 'Бронзовый фурин', '#8a6a3a', None, True, strip='#c8d8c0', ch='鈴')
    K = [('ko_kiku', 'Кокэси «Хризантема»', '#e6d2ae', 'kiku', 'top'), ('ko_ume', 'Кокэси «Слива»', '#efe0c4', 'ume', 'bob'), ('ko_tsubaki', 'Кокэси «Камелия»', '#e8d8b8', 'tsubaki', 'top'),
         ('ko_rings', 'Кокэси с кольцами', '#e2cca4', 'rings', 'top'), ('ko_stripes', 'Полосатая кокэси', '#dcc8a0', 'stripes', 'bob'), ('ko_kimono', 'Кокэси в кимоно', '#6e2a34', 'kimono', 'bob'),
         ('ko_blue', 'Синяя кокэси', '#34507a', 'kimono', 'top'), ('ko_black', 'Чёрная кокэси', '#1e1c1c', 'kiku', 'bob'), ('ko_tall', 'Высокая кокэси', '#e6d2ae', 'rings', 'top'),
         ('ko_mini', 'Малышка кокэси', '#efe0c4', 'ume', 'bob'), ('ko_green', 'Лесная кокэси', '#3a5a3a', 'stripes', 'top'), ('ko_pink', 'Весенняя кокэси', '#e8b0c0', 'tsubaki', 'bob')]
    for iid, n, b, pat, hair in K: kokeshi(iid, n, b, pat, 280 if iid == 'ko_tall' else 160 if iid == 'ko_mini' else 230, hair)
    D = [('da_red', 'Дарума алая', '#b8322a', '福', 0), ('da_white', 'Дарума белая', '#efe8da', '寿', 1), ('da_gold', 'Дарума золотая', '#d4a23a', '金', 2),
         ('da_black', 'Дарума чёрная', '#1c1a1c', '勝', 1), ('da_pink', 'Дарума розовая', '#e8a0b6', '恋', 0), ('da_blue', 'Дарума синяя', '#2a4a8a', '学', 1),
         ('da_green', 'Дарума зелёная', '#2f6b3a', '健', 0), ('da_purple', 'Дарума лиловая', '#5a3a7a', '夢', 2), ('da_orange', 'Дарума рыжая', '#d0702a', '猫', 1),
         ('da_win', 'Дарума «Победа»', '#9a1a1a', '必勝', 2)]
    for iid, n, c, k, e in D: daruma(iid, n, c, k, e, gold='#1a1414' if c in ('#efe8da', '#d4a23a') else '#e0b64a')
    M = [('mn_white', 'Белая манэки-нэко', '#f4f0e8', None, 'l'), ('mn_black', 'Чёрная манэки-нэко', '#1e1c1e', None, 'r'), ('mn_gold', 'Золотая манэки-нэко', '#d8b04a', None, 'l'),
         ('mn_calico', 'Трёхцветная манэки-нэко', '#f4f0e8', ['#d08040', '#2a2420', '#d08040'], 'r'), ('mn_pink', 'Розовая манэки-нэко', '#f0c0cc', None, 'l'),
         ('mn_red', 'Красная манэки-нэко', '#b8322a', None, 'r'), ('mn_ginger', 'Рыжая манэки-нэко', '#e0a060', ['#c07030', '#c07030'], 'l'), ('mn_tabby', 'Полосатая манэки-нэко', '#a89070', ['#6a5a44', '#6a5a44', '#6a5a44'], 'r')]
    for iid, n, f, sp, paw in M: maneki(iid, n, f, sp, paw, collar='#e8c048' if f == '#b8322a' else '#b8322a')
    MK = [('mk_kitsune', 'Маска кицунэ', 'kitsune'), ('mk_kitsune_b', 'Чёрная маска кицунэ', 'kitsune_black'), ('mk_neko', 'Кошачья маска', 'neko'), ('mk_usagi', 'Маска зайца', 'usagi'),
          ('mk_oni_r', 'Маска красного óни', 'oni_red'), ('mk_oni_b', 'Маска синего óни', 'oni_blue'), ('mk_hannya', 'Маска ханнья', 'hannya'), ('mk_okame', 'Маска окамэ', 'okame'),
          ('mk_hyottoko', 'Маска хёттоко', 'hyottoko'), ('mk_tengu', 'Маска тэнгу', 'tengu'), ('mk_tanuki', 'Маска тануки', 'tanuki'), ('mk_kappa', 'Маска каппы', 'kappa')]
    for iid, n, k in MK: mask(iid, n, k)
    for iid, n, p, mo in [('fa_nami', 'Веер «Волны»', '#efe8d6', 'nami'), ('fa_sakura', 'Веер «Сакура»', '#f2e2e0', 'sakura'), ('fa_moon', 'Веер «Луна»', '#2a3050', 'moon'),
                          ('fa_gold', 'Золотой веер', '#2a1c14', 'gold'), ('fa_tsuru', 'Веер с журавлём', '#b8322a', 'tsuru'), ('fa_momiji', 'Осенний веер', '#efe2c4', 'momiji')]: sensu(iid, n, p, mo)
    for iid, n, p, mo in [('uc_kingyo', 'Утива с рыбками', '#e8eef2', 'kingyo'), ('uc_hanabi', 'Утива «Фейерверк»', '#1e2438', 'hanabi'), ('uc_tombo', 'Утива со стрекозой', '#f0ead8', 'tombo'),
                          ('uc_asagao', 'Утива с вьюнком', '#e6f0e8', 'asagao')]: uchiwa(iid, n, p, mo)
    for iid, n, g, st in [('cw_raku', 'Чаван раку', '#2a2220', 'raku'), ('cw_akaraku', 'Красный раку', '#9a3a26', 'plain'), ('cw_shino', 'Чаван сино', '#e6ddcc', 'shino'),
                          ('cw_oribe', 'Чаван орибэ', '#dcd6c6', 'oribe'), ('cw_seiji', 'Селадоновый чаван', '#9ab8a8', 'plain'), ('cw_tenmoku', 'Чаван тэммоку', '#2a1c16', 'tenmoku'),
                          ('cw_hagi', 'Чаван хаги', '#e8c8b8', 'hagi'), ('cw_kintsugi', 'Чаван кинцуги', '#3a3430', 'kintsugi'), ('cw_sometsuke', 'Бело-синий чаван', '#eef0f2', 'sometsuke')]: chawan(iid, n, g, st)
    vessel('ve_tokkuri', 'Токкури для сакэ', 'tokkuri', '#d8cdb8'); vessel('ve_kyusu', 'Чайник кюсу', 'kyusu', '#8a4a2a'); vessel('ve_natsume', 'Чайница нацумэ', 'natsume', '#1a1412')
    vessel('ve_jubako', 'Лаковая шкатулка дзюбако', 'jubako', '#6a1410'); vessel('ve_yunomi', 'Чашка юноми', 'yunomi', '#9ab0a0'); vessel('ve_donburi', 'Донбури с крышкой', 'donburi', '#2a3a6a')
    vessel('ve_tokkuri2', 'Чёрный токкури', 'tokkuri', '#2a2422')
    for iid, n, fr, mo in [('sc_yume', 'Свиток «Сон»', '#3a2a4a', 'kanji:夢'), ('sc_shizuka', 'Свиток «Тишина»', '#2a3a34', 'kanji:静'), ('sc_wa', 'Свиток «Гармония»', '#4a3a24', 'kanji:和'),
                           ('sc_enso', 'Свиток «Энсо»', '#26221e', 'enso'), ('sc_pine', 'Свиток «Сосна и луна»', '#2a3440', 'moon_pine'), ('sc_bamboo', 'Свиток «Бамбук»', '#34402a', 'bamboo'),
                           ('sc_plum', 'Свиток «Слива»', '#4a2a2a', 'plum'), ('sc_fuji', 'Свиток «Фудзи»', '#2a3450', 'fuji'), ('sc_koi', 'Свиток «Карпы»', '#1e2a3a', 'koi'),
                           ('sc_crane', 'Свиток «Журавль»', '#3a2a1e', 'crane'), ('sc_nami', 'Свиток «Волны»', '#1a2440', 'nami'), ('sc_dragon', 'Свиток «Дракон»', '#2a1a14', 'dragon')]: scroll(iid, n, fr, mo)
    for iid, n, k, pc, sd in [('pl_pine', 'Бонсай «Чёрная сосна»', 'pine', '#3b4a52', 11), ('pl_momiji', 'Бонсай «Клён момидзи»', 'momiji', '#6a3a2a', 12), ('pl_juniper', 'Бонсай «Можжевельник»', 'juniper', '#2a2622', 13),
                              ('pl_sakura', 'Сакура в горшке', 'sakura', '#34404a', 14), ('pl_ume', 'Слива умэ', 'ume', '#1e1c1a', 15), ('pl_azalea', 'Азалия сацуки', 'azalea', '#4a5a6a', 16),
                              ('pl_wisteria', 'Глициния', 'wisteria', '#3a2a22', 17), ('pl_iris', 'Ирисы', 'iris', '#2a3a4a', 18), ('pl_orchid', 'Орхидея', 'orchid', '#e8e2d4', 19),
                              ('pl_moss', 'Моховой сад', 'moss', '#3a3430', 20), ('pl_bamboo', 'Бамбуковая роща', 'bamboo', '#1f1d1b', 21), ('pl_camellia', 'Камелия', 'camellia', '#6a2a24', 22),
                              ('pl_kiku', 'Белая хризантема', 'kiku', '#2c3a4a', 23), ('pl_pine_tall', 'Высокая сосна', 'pine_tall', '#4a4038', 24)]: potted(iid, n, k, pc, sd)
    for iid, n, b, pat, fg in [('zb_seigaiha', 'Подушка «Сэйгайха»', '#223250', 'seigaiha', '#9ab0d0'), ('zb_shippo', 'Подушка «Сиппо»', '#5a2a3a', 'shippo', '#e0b0b8'),
                               ('zb_ichimatsu', 'Подушка «Итимацу»', '#2a4a3a', 'ichimatsu', '#1a2a20'), ('zb_yagasuri', 'Подушка «Ягасури»', '#6a2a5a', 'yagasuri', '#e8d8e8'),
                               ('zb_uroko', 'Подушка «Урокo»', '#7a3a1a', 'uroko', '#e8c890'), ('zb_kikko', 'Подушка «Кикко»', '#2a3a2a', 'kikko', '#b8c8a0'),
                               ('zb_sakura', 'Подушка «Сакура»', '#e8c0c8', 'sakura', '#fff4f6'), ('zb_tatewaku', 'Подушка «Татэваку»', '#34304a', 'tatewaku', '#c8b8e8')]: zabuton(iid, n.replace('Урокo', 'Уроко'), b, pat, fg)
    furoshiki('fr_blue', 'Узелок фуросики', '#2a4a7a', '#e8e0d0'); furoshiki('fr_green', 'Зелёный узелок', '#2f6b3a', '#f0e8c0')
    for iid, n, b, cs in [('tm_red', 'Тэмари алый', '#b8322a', ['#e8c040', '#f2ecd8', '#2a4a8a']), ('tm_blue', 'Тэмари синий', '#2a4a8a', ['#f2ecd8', '#e8a0b6']),
                          ('tm_white', 'Тэмари белый', '#efe8da', ['#b8322a', '#2f6b3a', '#e8c040']), ('tm_black', 'Тэмари ночной', '#1c1a1e', ['#d8b048', '#8ab0d0'])]: temari(iid, n, b, cs)
    toy('ty_kendama', 'Кэндама', 'kendama'); toy('ty_koma', 'Волчок кома', 'koma', '#b8322a'); toy('ty_tsuru', 'Бумажный журавлик', 'tsuru', '#d8384a'); toy('ty_tsuru2', 'Синий журавлик', 'tsuru', '#3a5a9a')
    toy('ty_tako', 'Воздушный змей тако', 'tako', '#b8322a'); toy('ty_otoshi', 'Дарума-отоси', 'otoshi'); toy('ty_denden', 'Барабанчик дэндэн', 'denden', '#b8322a')
    toy('ty_mouse', 'Мышка-игрушка', 'mouse', '#9a9088'); toy('ty_yarn_r', 'Красный клубок', 'yarn', '#b8322a'); toy('ty_yarn_b', 'Синий клубок', 'yarn', '#3a5a9a')
    toy('ty_teaser', 'Удочка с пёрышками', 'teaser'); toy('ty_suzu', 'Колокольчик-мячик', 'suzu')
    for iid, n, c, pat in [('ws_red', 'Алый зонтик вагаса', '#b8322a', 'plain'), ('ws_janome', 'Зонтик «Глаз змеи»', '#2a3a6a', 'janome'), ('ws_sakura', 'Зонтик с сакурой', '#c86a86', 'sakura'),
                           ('ws_black', 'Чёрный зонтик', '#1c1a1c', 'janome'), ('ws_kiku', 'Зонтик с хризантемой', '#2f5a3a', 'kiku'), ('ws_paper', 'Зонтик из вощёной бумаги', '#d8c49a', 'plain')]: wagasa(iid, n, c, pat)
    for iid, n, k in [('tk_kasa', 'Каса-обакэ', 'kasa'), ('tk_chochin', 'Тётин-обакэ', 'chochin'), ('tk_zori', 'Ожившая сандалия', 'zori'), ('tk_chawan', 'Одноглазая пиала', 'chawan'),
                      ('tk_shoji', 'Мокумокурэн', 'shoji'), ('tk_tetsubin', 'Чайник с языком', 'tetsubin'), ('tk_geta', 'Гэта-оборотень', 'geta'), ('tk_biwa', 'Бива-бокубоку', 'biwa')]: tsukumo(iid, n, k)
    relic_bell(); chawan('r_ricebowl', 'Рисовая чаша духа', '#b8322a', 'kintsugi', story=True); relic_ribbon(); relic_pearl(); relic_candle(); relic_brush()
    scroll('r_hyakki', 'Свиток ста демонов', '#1a1014', 'dragon', story=True); temari('r_temari', 'Тэмари девочки', '#c02a2a', ['#f2ecd8', '#e8c040', '#1c1a1e']); relic_mirror(); relic_key()
    for r in CAT:
        if r['id'] in ('r_ricebowl', 'r_hyakki', 'r_temari'): r['c'] = 'Реликвии'; r['story'] = 1; r['p'] = 0


if __name__ == '__main__':
    only = sys.argv[2:] if len(sys.argv) > 2 else None
    build()
    json.dump(CAT, open(f'{OUT}/items.json', 'w'), ensure_ascii=False, indent=0)
    print('TOTAL', len(CAT))
