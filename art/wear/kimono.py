#!/usr/bin/env python3
"""Kimono for Musya: worn over the sitting body (neck-slot poses). Sizes in cat-frame pixels (384×416 frame).
The V of the collar is left open so the chest fur shows through; sleeves hang at the sides.
Usage: kimono.py <outdir> → <outdir>/kimono.webp (atlas) + kimono.json {w,h,r:{id:[x,y,w,h]}}"""
import json, math, random, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
from PIL import Image, ImageDraw
import paint as P
import items as I
from items import px, canvas, fill, volume, soft, line, ell, poly, H, dk, lt, mask_poly

OUT = sys.argv[1]; IMGS = []
W, HH = 220, 190


def cr(pts, n=10):
    N = len(pts); out = []
    for i in range(N):
        p0, p1, p2, p3 = pts[(i - 1) % N], pts[i], pts[(i + 1) % N], pts[(i + 2) % N]
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * (2 * p1[c] + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t2 + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t3) for c in (0, 1)))
    return out


# one soft bell: sloping shoulders, rounded sleeves, a hem that follows the round lap
SIL = cr([(80, 6), (140, 6), (170, 22), (196, 44), (208, 96), (204, 150), (188, 170), (164, 180), (110, 188), (56, 180), (32, 170), (16, 150), (12, 96), (24, 44), (50, 22)])
SLV_L = cr([(-10, 20), (58, 26), (60, 110), (56, 176), (-10, 190)], 8)      # sleeve zones (intersected with the silhouette)
SLV_R = [(W - x, y) for x, y in SLV_L]
VNECK = [(80, 0), (140, 0), (104, 82)]             # open collar: fur shows through
OBI_TOP = [(54, 104), (110, 112), (166, 104)]; OBI_BOT = [(166, 132), (110, 140), (54, 132)]


def layer_clip(img, m, fn):
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(l), l)
    a = np.asarray(l, np.float32); a[..., 3] *= np.asarray(m, np.float32) / 255; img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))


def P5(d, x, y, r, col, center, n=5, rot=0):
    for k in range(n):
        a = k / n * math.tau + rot; ex, ey = x + math.cos(a) * r * .6, y + math.sin(a) * r * .6
        d.ellipse([px(ex - r * .5), px(ey - r * .5), px(ex + r * .5), px(ey + r * .5)], fill=H(col))
    if center: d.ellipse([px(x - r * .25), px(y - r * .25), px(x + r * .25), px(y + r * .25)], fill=H(center))


def scatter(seed, n, box=(10, 10, W - 10, HH - 6)):
    rr = random.Random(seed); return [(rr.uniform(box[0], box[2]), rr.uniform(box[1], box[3]), rr.random()) for _ in range(n)]


def pat_sakura(d, l):
    for x, y, t in scatter(1, 34): P5(d, x, y, 7 + t * 4, '#fbe6ee' if t > .5 else '#f4b8cc', '#d0607e', rot=t * 3)
def pat_seigaiha(d, l):
    for r in range(0, 16):
        for c in range(-1, 12):
            x = c * 26 + (13 if r % 2 else 0); y = r * 13
            for k, col in enumerate(('#f2eee4', '#2a3a6a', '#f2eee4', '#2a3a6a')):
                rad = 15 - k * 4; d.pieslice([px(x - rad), px(y - rad), px(x + rad), px(y + rad)], 180, 360, fill=H(col))
def pat_tsuru(d, l):
    for x, y, t in scatter(3, 12):
        s = .8 + t * .5; d.polygon([(px(x - 16 * s), px(y)), (px(x), px(y - 9 * s)), (px(x + 16 * s), px(y)), (px(x), px(y - 3 * s))], fill=H('#f4f0e6'))
        d.line([(px(x), px(y - 4 * s)), (px(x + 7 * s), px(y - 12 * s))], fill=H('#f4f0e6'), width=px(2)); d.ellipse([px(x + 6 * s), px(y - 15 * s), px(x + 10 * s), px(y - 11 * s)], fill=H('#d8322a'))
    for x, y, t in scatter(4, 10): d.arc([px(x - 14), px(y - 6), px(x + 14), px(y + 6)], 180, 360, fill=H('#d8b048'), width=px(1.6))
def pat_asagao(d, l):
    for x, y, t in scatter(5, 26): d.ellipse([px(x - 5), px(y + 2), px(x + 11), px(y + 9)], fill=H('#3a7a4a'))
    for x, y, t in scatter(6, 16): P5(d, x, y, 12 + t * 3, '#3a52c0' if t > .4 else '#7a4ac0', '#f4f0f8')
def pat_momiji(d, l):
    for x, y, t in scatter(7, 22):
        col = ('#f0a020', '#d83a1a', '#e8c040', '#b82a1a')[int(t * 4)]
        for k in range(5):
            a = -math.pi / 2 + (k - 2) * .62; d.polygon([(px(x), px(y)), (px(x + math.cos(a - .2) * 6), px(y + math.sin(a - .2) * 6)), (px(x + math.cos(a) * 12), px(y + math.sin(a) * 12)), (px(x + math.cos(a + .2) * 6), px(y + math.sin(a + .2) * 6))], fill=H(col))
        d.line([(px(x), px(y)), (px(x), px(y + 8))], fill=H(col), width=px(1.4))
def pat_yagasuri(d, l):
    for c in range(12):
        x = c * 20
        for r in range(12):
            y = r * 18 + (9 if c % 2 else 0); col = '#6a3a9a' if (c + r) % 2 else '#f2eee4'
            d.polygon([(px(x), px(y)), (px(x + 10), px(y + 8)), (px(x + 20), px(y)), (px(x + 20), px(y + 12)), (px(x + 10), px(y + 20)), (px(x), px(y + 12))], fill=H(col))
def pat_ichimatsu(d, l):
    for r in range(14):
        for c in range(14):
            if (r + c) % 2: d.rectangle([px(c * 18), px(r * 18), px(c * 18 + 18), px(r * 18 + 18)], fill=H('#1a1a1a'))
def pat_kiku(d, l):
    for x, y, t in scatter(9, 11):
        r = 11 + t * 6; col = '#e8c040' if t > .45 else '#f4f0e6'
        for k in range(16): a = k / 16 * math.tau; d.line([(px(x), px(y)), (px(x + math.cos(a) * r), px(y + math.sin(a) * r))], fill=H(col), width=px(3))
        d.ellipse([px(x - 3), px(y - 3), px(x + 3), px(y + 3)], fill=H('#b8801a'))
def pat_asanoha(d, l):
    s = 22
    for r in range(-1, 12):
        for c in range(-1, 12):
            x = c * s + (s / 2 if r % 2 else 0); y = r * s * .87
            for k in range(6):
                a = k / 6 * math.tau + math.pi / 6; d.line([(px(x), px(y)), (px(x + math.cos(a) * s * .58), px(y + math.sin(a) * s * .58))], fill=H('#c0304a'), width=px(1.2))
            d.regular_polygon((px(x), px(y), px(s * .58)), 6, rotation=30, outline=H('#c0304a'))
def pat_hotaru(d, l):
    for x in range(0, W, 6): d.line([(px(x), px(HH)), (px(x + random.Random(x).uniform(-6, 6)), px(HH - random.Random(x + 1).uniform(20, 46)))], fill=H('#2a5a3a'), width=px(1.6))
    for x, y, t in scatter(11, 18, (10, 20, W - 10, HH - 40)):
        d.ellipse([px(x - 5), px(y - 5), px(x + 5), px(y + 5)], fill=(210, 250, 120, 90)); d.ellipse([px(x - 2), px(y - 2), px(x + 2), px(y + 2)], fill=(240, 255, 170, 255))
def pat_fuji(d, l):
    for c in range(9):
        x = 14 + c * 26; L = 5 + (c * 7) % 5
        for k in range(L):
            y = 6 + k * 9; r = 5.5 - k * .35; d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=H('#a88ad8' if k % 2 else '#c8b0f0'))
    for x, y, t in scatter(12, 14, (10, 4, W - 10, 30)): d.ellipse([px(x - 7), px(y - 3), px(x + 7), px(y + 3)], fill=H('#5a8a3a'))
def pat_miko(d, l): pass


KIMONO = [
    ('k_sakura', 'Кимоно «Сакура»', '#e8a0b6', '#c02a2a', '#d8b048', pat_sakura),
    ('k_seigaiha', 'Кимоно «Волны сэйгайха»', '#2a3a6a', '#d8b048', '#c02a2a', pat_seigaiha),
    ('k_tsuru', 'Чёрное кимоно с журавлями', '#17151c', '#c02a2a', '#d8b048', pat_tsuru),
    ('k_asagao', 'Юката с вьюнком', '#f4f0e6', '#e8b030', '#2a3a8a', pat_asagao),
    ('k_momiji', 'Кимоно «Осенние клёны»', '#5a2a1a', '#2f5a3a', '#e8c040', pat_momiji),
    ('k_yagasuri', 'Кимоно «Стрелы» и красный пояс', '#f2eee4', '#b8322a', '#f2eee4', pat_yagasuri),
    ('k_ichimatsu', 'Кимоно в клетку итимацу', '#2f7a5a', '#1a1a1a', '#e8e0cc', pat_ichimatsu),
    ('k_kiku', 'Праздничное кимоно с хризантемами', '#8a1a2a', '#d8b048', '#c02a2a', pat_kiku),
    ('k_asanoha', 'Розовое кимоно «Асаноха»', '#f4c4d0', '#2a1a1a', '#c02a2a', pat_asanoha),
    ('k_hotaru', 'Ночная юката со светлячками', '#1a2440', '#a8d8f0', '#e8c040', pat_hotaru),
    ('k_fuji', 'Кимоно «Глициния»', '#ece4f4', '#6a3a9a', '#d8b048', pat_fuji),
    ('k_miko', 'Наряд мико', '#f8f6f0', '#f8f6f0', '#c8281e', pat_miko),
]


def andm(*ms): return Image.fromarray(np.minimum.reduce([np.asarray(m) for m in ms]), 'L')
def subm(a, b): return Image.fromarray(np.clip(np.asarray(a, np.int16) - np.asarray(b, np.int16), 0, 255).astype(np.uint8), 'L')


def kimono(iid, name, base, obi, cord, pat):
    img = canvas(W, HH)
    sil = mask_poly(img, poly=SIL); body = subm(sil, mask_poly(img, poly=VNECK))
    fill(img, base, 3, mask=body, scale=8, stretch=(1, 3), contrast=.7, dark=.3, light=.15); layer_clip(img, body, pat)
    d = ImageDraw.Draw(img)
    d.line([(px(104), px(82)), (px(86), px(186))], fill=(0, 0, 0, 90), width=px(2))                    # edge of the top panel
    om = andm(mask_poly(img, poly=OBI_TOP + OBI_BOT), body)
    if iid == 'k_miko': layer_clip(img, andm(body, mask_poly(img, poly=OBI_BOT[::-1] + [(220, 190), (0, 190)])), lambda d, l: [d.rectangle([0, 0, px(W), px(HH)], fill=H('#c8281e'))] + [d.line([(px(x), px(130)), (px(x - 6), px(HH))], fill=H('#9a1a14'), width=px(2)) for x in range(30, W, 20)])
    fill(img, obi, 20, mask=om, scale=5, stretch=(4, .5), contrast=.8)
    layer_clip(img, om, lambda d, l: [d.line([(px(x), px(y)) for x, y in cr_open(pts)], fill=(0, 0, 0, 70), width=px(1.4)) for pts in ([(54, 108), (110, 116), (166, 108)], [(54, 128), (110, 136), (166, 128)])])
    line(img, cr_open([(54, 118), (110, 126), (166, 118)]), cord, 3); ell(img, (102, 118, 118, 132), cord)
    for zone, sd in ((SLV_L, 5), (SLV_R, 6)):                                                          # sleeves hang over the obi ends
        sm = andm(sil, mask_poly(img, poly=zone)); fill(img, dk(H(base), .1), sd, mask=sm, scale=8, stretch=(1, 3), contrast=.7, dark=.3, light=.15); layer_clip(img, sm, pat)
        if iid == 'k_miko': layer_clip(img, andm(sm, mask_poly(img, poly=[(0, 150), (W, 150), (W, HH), (0, HH)])), lambda d, l: d.rectangle([0, 0, px(W), px(HH)], fill=H('#f0ece2')))
        seam = zone[len(zone) // 5: len(zone) * 3 // 5]
        layer_clip(img, sil, lambda d, l, seam=seam: d.line([(px(x), px(y)) for x, y in seam], fill=(0, 0, 0, 80), width=px(2.4)))
    for off, col, wd in ((0, '#f4f0e6', 7), (7, dk(H(base), .45) if iid != 'k_miko' else H('#e8e2d6'), 8)):     # juban collar, then kimono collar
        d.line([(px(80 - off), px(0)), (px(104), px(82 + off * 1.3)), (px(140 + off), px(0))], fill=H(col), width=px(wd), joint='curve')
    volume(img, (8, 0, W - 8, HH), .45, .45)
    out = img.resize((P.W, P.H), Image.LANCZOS); IMGS.append((iid, name, out)); print(iid)


def cr_open(pts, n=12):
    p = [pts[0]] + list(pts) + [pts[-1]]; out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        for k in range(n + 1):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * (2 * p1[c] + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t2 + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t3) for c in (0, 1)))
    return out


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for row in KIMONO: kimono(*row)
    cols = 4; at = Image.new('RGBA', (cols * (W + 2), ((len(IMGS) + cols - 1) // cols) * (HH + 2)), (0, 0, 0, 0)); R = {}
    for i, (iid, name, im) in enumerate(IMGS):
        x, y = (i % cols) * (W + 2), (i // cols) * (HH + 2); at.paste(im, (x, y)); R[iid] = [x, y, W, HH]
    at.save(f'{OUT}/kimono.webp', 'WEBP', quality=88, alpha_quality=92, method=6)
    json.dump({'w': at.width, 'h': at.height, 'r': R, 'n': {iid: name for iid, name, _ in IMGS}}, open(f'{OUT}/kimono.json', 'w'), ensure_ascii=False)
