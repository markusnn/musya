#!/usr/bin/env python3
"""Painted koi seen from above (head to the right): shaded body, patterns, translucent fins."""
import math, sys, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, fbm

OUT = sys.argv[1]; S = 3                      # supersample
W, H = 300, 110
CY = H / 2


def half(x):
    """Half-width of the body at x: narrow tail stalk, full shoulders, rounded head (nose at 292)."""
    u = (x - 70) / 222
    if u < 0 or u > 1: return 0
    if u < .62: return 4.5 + 29.5 * (u / .62) ** 1.1
    return 34 * max(0, 1 - ((u - .62) / .38) ** 2.4) ** .55


def body_mask():
    m = Image.new('L', (W * S, H * S), 0); pts = []
    for x in range(70, 293, 2): pts.append((x * S, (CY - half(x)) * S))
    for x in range(292, 69, -2): pts.append((x * S, (CY + half(x)) * S))
    ImageDraw.Draw(m).polygon(pts, fill=255)
    return m.filter(ImageFilter.GaussianBlur(S * .6))


def fins(img, col):
    fin = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(fin, 'RGBA')
    c = (*col[:3], 95); ray = (*[max(0, v - 70) for v in col[:3]], 90)
    tail = [(74, CY)] + [(22 + 18 * abs(math.sin(a)) ** 1.5, CY + 26 * math.sin(a)) for a in np.linspace(-math.pi / 2, math.pi / 2, 24)]
    d.polygon([(x * S, y * S) for x, y in tail], fill=c)
    for a in np.linspace(-1.35, 1.35, 13): d.line([(74 * S, CY * S), ((24 + 14 * abs(math.sin(a)) ** 1.5) * S, (CY + 25 * math.sin(a)) * S)], fill=ray, width=S)
    for sgn in (-1, 1):
        base = (212, CY + sgn * 27)
        pts = [base, (196, CY + sgn * 46), (184, CY + sgn * 44), (196, CY + sgn * 30)]
        d.polygon([(x * S, y * S) for x, y in pts], fill=c)
        for k in range(4): d.line([(base[0] * S, base[1] * S), ((186 + k * 3) * S, (CY + sgn * (45 - k)) * S)], fill=ray, width=S)
        pts = [(132, CY + sgn * 22), (118, CY + sgn * 34), (112, CY + sgn * 31), (124, CY + sgn * 21)]
        d.polygon([(x * S, y * S) for x, y in pts], fill=c)
    img.alpha_composite(fin.filter(ImageFilter.GaussianBlur(S * .5)))


def koi(name, base, patches, seed, metallic=False, reticulated=None):
    img = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    fins(img, base if not patches else base)
    m = body_mask(); a = np.asarray(m, np.float32) / 255
    yy, xx = np.mgrid[0:H * S, 0:W * S] / S
    hw = np.vectorize(half)(xx[0])[None, :] + 1e-3
    v = np.clip(np.abs(yy - CY) / hw, 0, 1)
    rgb = np.ones((H * S, W * S, 3), np.float32) * np.array(base[:3], np.float32)
    rng = random.Random(seed)
    for col, thr, sc, sd in patches:
        n = fbm(W * S, H * S, sc * S, 4, seed + sd, (1.4, 1))
        mk = np.clip((n - thr) * 9, 0, 1)[..., None]
        rgb = rgb * (1 - mk) + np.array(col[:3], np.float32) * mk
    if reticulated is not None:
        # scale net: darker diamond edges on the back
        g = (np.sin(xx * .9 + yy * .9) * np.sin(xx * .9 - yy * .9))
        net = np.clip(1 - np.abs(g) * 6, 0, 1) * (1 - v) * (xx > 110) * (xx < 250)
        rgb = rgb * (1 - net[..., None] * .35) + np.array(reticulated[:3], np.float32) * net[..., None] * .35
    tex = fbm(W * S, H * S, 3 * S, 3, seed + 50)[..., None]
    shade = (1.18 - 0.62 * v ** 2)[..., None] * (0.92 + 0.16 * tex)
    if metallic: shade = shade * (1 + 0.35 * np.exp(-((v - .15) / .18) ** 2))[..., None]
    spine = np.exp(-(v / .12) ** 2)[..., None] * ((xx > 100) & (xx < 250))[..., None]
    rgb = np.clip(rgb * shade + 30 * spine, 0, 255)
    body = Image.fromarray(np.dstack([rgb, a * 255]).astype(np.uint8), 'RGBA')
    img.alpha_composite(body)
    d = ImageDraw.Draw(img)
    if name == 'koi_tancho':
        crown = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(crown).ellipse([236 * S, (CY - 12) * S, 262 * S, (CY + 12) * S], fill=(200, 45, 30, 255))
        img.alpha_composite(crown.filter(ImageFilter.GaussianBlur(S)))
    for sgn in (-1, 1):  # eyes at the sides of the head, nostrils, barbels
        ex, ey = 262, CY + sgn * 15
        d.ellipse([(ex - 3.2) * S, (ey - 2.6) * S, (ex + 3.2) * S, (ey + 2.6) * S], fill=(18, 16, 14, 255))
        d.ellipse([(ex - 1) * S, (ey - 1.6) * S, (ex + .6) * S, (ey - .2) * S], fill=(230, 230, 230, 200))
        d.line([(286 * S, (CY + sgn * 5) * S), (297 * S, (CY + sgn * 11) * S)], fill=(*base[:3], 200), width=S)
    out = img.resize((W, H), Image.LANCZOS)
    out.save(f'{OUT}/{name}.webp', 'WEBP', quality=90, method=6)
    print('koi', name)


RED, WHITE, BLACK, GOLD = hexc('#c9391f'), hexc('#f1ede3'), hexc('#171514'), hexc('#d9a33a')
koi('koi_kohaku', WHITE, [(RED, .5, 34, 1)], 11)
koi('koi_kohaku2', WHITE, [(RED, .56, 26, 2), (RED, .62, 50, 3)], 12)
koi('koi_showa', BLACK, [(RED, .52, 30, 4), (WHITE, .6, 36, 5)], 13)
koi('koi_ogon', GOLD, [], 14, metallic=True, reticulated=hexc('#8a5a14'))
koi('koi_asagi', hexc('#7d93a6'), [(hexc('#d8743a'), .7, 60, 6)], 15, reticulated=hexc('#e2e8ee'))
koi('koi_tancho', WHITE, [], 16)
