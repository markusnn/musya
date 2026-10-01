#!/usr/bin/env python3
"""«Картины Муси» (feat/paint.js): the fallback picture of a framed painting → assets/items/atlas_mp.webp (150×208).
The game paints every real painting (the player's paw prints in its frame) at runtime; this picture is only the
silhouette/fallback for the twelve picture slots mp_1…mp_12. Preview → art/out/atlas_mp.png.  Usage: paint_art.py"""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'assets', 'items', 'atlas_mp.webp')
K = 4                                   # paint at 4×, then downscale
W, H = 150 * K, 208 * K
rnd = random.Random(52)


def washi(w, h):
    """Warm paper: soft mottling + fibres."""
    g = np.random.default_rng(7)
    small = g.normal(0, 1, (h // 24 + 2, w // 24 + 2)).astype(np.float32)
    mott = np.asarray(Image.fromarray(small).resize((w, h), Image.BICUBIC), np.float32)
    lum = 228 + mott * 7 + g.normal(0, 3, (h, w))
    a = np.stack([lum, lum * .955, lum * .86], -1)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    d = ImageDraw.Draw(im, 'RGBA')
    for _ in range(w * h // 900):
        x, y, ang, L = rnd.uniform(0, w), rnd.uniform(0, h), rnd.uniform(0, 6.3), rnd.uniform(6, 30)
        d.line([(x, y), (x + math.cos(ang) * L, y + math.sin(ang) * L)], fill=(255, 250, 236, 70) if rnd.random() < .6 else (120, 96, 64, 26), width=2)
    return im


def paw(layer, x, y, ang, s, col, a):
    d = ImageDraw.Draw(layer, 'RGBA')
    ca, sa = math.cos(ang), math.sin(ang)
    def pt(px, py): return (x + px * ca - py * sa, y + px * sa + py * ca)
    def blob(px, py, rx, ry, al):
        cx, cy = pt(px * s, py * s)
        d.ellipse([cx - rx * s, cy - ry * s, cx + rx * s, cy + ry * s], fill=col + (int(255 * a * al),))
    blob(0, 3, 7, 5.6, .9); blob(-3.4, 6, 3.2, 2.6, .8); blob(3.4, 6, 3.2, 2.6, .8)
    for tx, ty in [(-7.2, -5.5), (-2.6, -10), (2.6, -10), (7.2, -5.5)]:
        blob(tx, ty, 2.6, 3.3, rnd.uniform(.75, 1))


img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
fx, fy, fw, fh, b = 5 * K, 28 * K, 140 * K, 180 * K, 7 * K
# cord and nail
dr = ImageDraw.Draw(img, 'RGBA')
dr.line([(fx + fw * .22, fy + 3 * K), (W / 2, 6 * K), (fx + fw * .78, fy + 3 * K)], fill=(58, 44, 32, 255), width=int(1.4 * K))
dr.ellipse([W / 2 - 3 * K, 3 * K, W / 2 + 3 * K, 9 * K], fill=(150, 112, 52, 255))
# soft shadow
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle([fx + 2 * K, fy + 4 * K, fx + fw + 2 * K, fy + fh + 4 * K], fill=(0, 0, 0, 120))
img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(5 * K)))
# paper + paw prints (sumi), a vermilion seal
iw, ih = fw - 2 * b, fh - 2 * b
paper = washi(iw, ih)
ink = Image.new('RGBA', (iw, ih), (0, 0, 0, 0))
x, y, ang = iw * .25, ih * .85, -1.2
for i in range(9):
    side = 1 if i % 2 else -1
    paw(ink, x + math.cos(ang + 1.57) * side * 7 * K, y + math.sin(ang + 1.57) * side * 7 * K, ang + 1.57, K * 1.25, (29, 26, 24), rnd.uniform(.7, .95))
    ang += rnd.uniform(-.35, .3); x += math.cos(ang) * 13 * K; y += math.sin(ang) * 13 * K
ink = ink.filter(ImageFilter.GaussianBlur(.6 * K))
paper = Image.alpha_composite(paper, ink)
pd = ImageDraw.Draw(paper, 'RGBA')
pd.rounded_rectangle([iw - 26 * K, ih - 34 * K, iw - 12 * K, ih - 14 * K], radius=2 * K, fill=(179, 48, 31, 230))
img.paste(paper, (fx + b, fy + b))
# thin black lacquer frame with a fine gold fillet
dr = ImageDraw.Draw(img, 'RGBA')
for i in range(b):
    t = i / b; c = int(14 + 26 * math.sin(t * math.pi))
    dr.rectangle([fx + i, fy + i, fx + fw - i, fy + fh - i], outline=(c, c - 2, c - 4, 255))
dr.rectangle([fx + b - 2, fy + b - 2, fx + fw - b + 2, fy + fh - b + 2], outline=(176, 142, 82, 200), width=K // 2)
dr.line([(fx + 2, fy + 2), (fx + fw - 2, fy + 2)], fill=(255, 255, 255, 50), width=K // 2)

out = img.resize((150, 208), Image.LANCZOS)
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
out.save(os.path.join(HERE, 'out', 'atlas_mp.png'))
out.save(OUT, 'WEBP', quality=88, method=6)
print('saved', OUT, os.path.getsize(OUT), 'bytes')
