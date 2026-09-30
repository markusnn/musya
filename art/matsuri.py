#!/usr/bin/env python3
"""Night fair (matsuri) — a new location painted as depth layers, like layers.py.
Stalls (yatai) stand on the ground line y≈1080: mask shop, goldfish scooping, the taiko tower (yagura),
the cork-gun shooting gallery and takoyaki. Strings of red and white chōchin sag from the tower to the edges.
Usage: cd art && python3 matsuri.py ../assets/layers  →  matsuri_<layer>.webp; preview and matsuri.json stay in art/."""
import json, math, os, random, shutil, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc, fbm, textured_fill, layer, gradient, atmos, fog_layer, glow, wood_block, ground, cedar, bushes, SS, SW, SH
import layers as LY
from layers import Stack, near_fern, near_foliage
import items as I
from items import px, SERIF, SANS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
BLACK, WHITE = (0, 0, 0, 255), (255, 255, 255, 255)
RED, RED_D = hexc('#b8342a'), hexc('#7e1f18')
CLOTH_W = hexc('#e8ddc8')
INDIGO = hexc('#263a66')
WARM = hexc('#ffb45a')
WOOD, WOOD_D, WOOD_L = hexc('#3c2a1e'), hexc('#160e09'), hexc('#5a4230')
BASE = 1080                      # every stall stands here
STALLS = {}


# ───────────── small helpers ─────────────
def comp(img, patch, x, y):
    """alpha_composite that tolerates patches hanging off the canvas (x, y in supersampled px)."""
    x, y = int(x), int(y); sx, sy = max(0, -x), max(0, -y)
    w, h = min(patch.width - sx, img.width - x - sx), min(patch.height - sy, img.height - y - sy)
    if w <= 0 or h <= 0: return
    img.alpha_composite(patch.crop((sx, sy, sx + w, sy + h)), (x + sx, y + sy))


def lglow(img, cx, cy, r, col, strength, squash=1.0):
    """Local soft light: cheaper than paint.glow for dozens of lanterns."""
    n = max(4, int(2 * r * SS / 2)); yy, xx = np.mgrid[0:n, 0:n]
    d = np.sqrt(((xx - n / 2) / (n / 2)) ** 2 + ((yy - n / 2) / (n / 2 * squash)) ** 2)
    a = np.clip(1 - d, 0, 1) ** 2 * strength * 255
    g = Image.new('RGBA', (n, n), col); g.putalpha(Image.fromarray(a.astype(np.uint8)))
    g = g.resize((int(2 * r * SS), int(2 * r * SS)), Image.BICUBIC)
    comp(img, g, (cx - r) * SS, (cy - r) * SS)


def shade_rows(img, box, top_k, bot_k):
    """Multiply a region's colour by a vertical ramp (darker under roofs, lit toward the lamps)."""
    x0, y0, x1, y1 = (px(v) for v in box); x0, y0 = max(0, x0), max(0, y0); x1, y1 = min(img.width, x1), min(img.height, y1)
    reg = np.asarray(img.crop((x0, y0, x1, y1)), np.float32)
    reg[..., :3] *= np.linspace(top_k, bot_k, reg.shape[0])[:, None, None]
    img.paste(Image.fromarray(np.clip(reg, 0, 255).astype(np.uint8), 'RGBA'), (x0, y0))


def lantern(img, cx, cy, r, kind='red', mark=None, seed=0, halo=.55, string=None):
    """Paper chōchin lit from inside: ribs, black caps, a kanji, warm halo."""
    hh = r * 1.28
    col = {'red': hexc('#c83a2c'), 'white': hexc('#f0e4c8'), 'orange': hexc('#e39640')}[kind]
    if halo: lglow(img, cx, cy, r * 3.4, hexc('#ffac50') if kind != 'white' else hexc('#ffd28a'), halo)
    if string is not None: I.line(img, [(cx, string), (cx, cy - hh - r * .1)], '#120c08', max(1.2, r * .08))
    m = I.fill(img, col, seed, ell=(cx - r, cy - hh, cx + r, cy + hh), scale=max(2, r / 6), contrast=.5, dark=.25, light=.3)
    box = m.getbbox()
    if box:
        reg = np.asarray(img.crop(box), np.float32); h, w = reg.shape[:2]
        yy = np.linspace(-1, 1, h)[:, None]; xx = np.linspace(-1, 1, w)[None, :]
        lit = 1.28 - .62 * xx ** 2 - .22 * yy ** 2
        a = np.asarray(m.crop(box), np.float32) / 255
        reg[..., :3] = reg[..., :3] * (1 - a[..., None]) + np.clip(reg[..., :3] * lit[..., None] + np.array([26, 12, 0]) * (1 - xx ** 2)[..., None], 0, 255) * a[..., None]
        img.paste(Image.fromarray(reg.astype(np.uint8), 'RGBA'), box[:2])
    d = ImageDraw.Draw(img); rib = mixc(col, BLACK, .45)
    for k in range(1, 8):
        dy = -hh + 2 * hh * k / 8; half = r * math.sqrt(max(0, 1 - (dy / hh) ** 2)) * .98
        d.line([(px(cx - half), px(cy + dy)), (px(cx + half), px(cy + dy))], fill=rib[:3] + (150,), width=max(1, px(r * .045)))
    if mark: I.text(img, mark, cx, cy + r * .05, r * 1.05, '#1c1210' if kind != 'red' else '#20100c', SERIF, brush=True)
    for yv, hgt in ((cy - hh - r * .12, r * .26), (cy + hh - r * .14, r * .26)):
        d.rounded_rectangle([px(cx - r * .56), px(yv), px(cx + r * .56), px(yv + hgt)], px(r * .08), fill=hexc('#140d09'))


def board(img, box, text, seed, bg=hexc('#ece2cc'), fg='#1c1410', size=46, frame=WOOD_D, vertical=False):
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img); d.rectangle([px(x0 - 6), px(y0 - 6), px(x1 + 6), px(y1 + 6)], fill=frame)
    I.fill(img, bg, seed, rect=box, scale=6, contrast=.6, dark=.2, light=.12)
    shade_rows(img, box, .92, 1.05)
    if vertical:
        for k, ch in enumerate(text): I.text(img, ch, (x0 + x1) / 2, y0 + size * .75 + k * size * 1.02, size, fg, SERIF, brush=True)
    else: I.text(img, text, (x0 + x1) / 2, (y0 + y1) / 2 + 2, size, fg, SERIF, brush=True)


def awning(img, x0, x1, y0, y1, cols, seed, flare=20, stripe=44):
    """Striped cloth awning seen from below-front, with a scalloped valance."""
    wdt = x1 - x0; n = max(4, round(wdt / stripe)); bw = (wdt + 2 * flare) / n
    for i in range(n):
        u0, u1 = i / n, (i + 1) / n
        pts = [(x0 + u0 * wdt, y0), (x0 + u1 * wdt, y0), (x0 - flare + u1 * (wdt + 2 * flare), y1), (x0 - flare + u0 * (wdt + 2 * flare), y1)]
        I.fill(img, cols[i % len(cols)], seed + i, poly=pts, scale=10, stretch=(.4, 3), contrast=.7, dark=.35, light=.15)
    shade_rows(img, (x0 - flare, y0, x1 + flare, y1), .55, 1.0)
    d = ImageDraw.Draw(img)
    for i in range(n):   # valance scallops
        bx = x0 - flare + (i + .5) * bw
        c = cols[i % len(cols)]
        d.pieslice([px(bx - bw / 2), px(y1 - bw * .42), px(bx + bw / 2), px(y1 + bw * .42)], 0, 180, fill=mixc(c, BLACK, .1))
    d.line([(px(x0 - flare), px(y1)), (px(x1 + flare), px(y1))], fill=mixc(cols[0], BLACK, .5), width=px(2.5))


def kohaku(img, x0, x1, y0, y1, seed, stripe=34, cols=(RED, CLOTH_W)):
    """Red-and-white festival curtain (kōhaku-maku) with soft vertical folds."""
    n = max(2, round((x1 - x0) / stripe)); sw = (x1 - x0) / n
    for i in range(n):
        I.fill(img, cols[i % 2], seed + i, rect=(x0 + i * sw, y0, x0 + (i + 1) * sw + .5, y1), scale=8, stretch=(.3, 3), contrast=.6, dark=.3, light=.12)
    X0, Y0, X1, Y1 = px(x0), px(y0), px(x1), px(y1)
    reg = np.asarray(img.crop((X0, Y0, X1, Y1)), np.float32); w = reg.shape[1]
    fold = .84 + .16 * np.sin(np.linspace(0, (x1 - x0) / 22, w))[None, :, None]
    reg[..., :3] *= fold * np.linspace(.75, 1.0, reg.shape[0])[:, None, None]
    img.paste(Image.fromarray(np.clip(reg, 0, 255).astype(np.uint8), 'RGBA'), (X0, Y0))


def stall_shadow(img, x0, x1):
    I.soft(img, lambda d: d.rectangle([px(x0 - 10), px(BASE - 16), px(x1 + 10), px(BASE + 18)], fill=(0, 0, 0, 150)), 8)


def yatai(img, x0, x1, top, seed, cols, sign, counter_y, interior=None, skirt='kohaku', sign_size=46, lanterns=('red', 'red'), marks=('祭', '祭'), sign_bg=None, sign_fg='#1c1410'):
    """A festival stall: sign board, striped awning, posts, a glowing interior, counter and skirt."""
    stall_shadow(img, x0, x1)
    aw0, aw1 = top + 78, top + 172
    # dark interior with a warm lamp inside
    I.fill(img, hexc('#24170f'), seed, rect=(x0 + 20, aw0, x1 - 20, counter_y), scale=20, contrast=.9, dark=.4, light=.18)
    lglow(img, (x0 + x1) / 2, aw1 + 70, (x1 - x0) * .62, WARM, .42, .8)
    if interior: interior((x0 + 26, aw1 + 14, x1 - 26, counter_y))
    # posts
    for px0 in (x0 + 4, x1 - 24): wood_block(img, (px0, top + 60, px0 + 20, BASE), seed + px0, WOOD, WOOD_D, WOOD_L, True)
    # counter slab and skirt
    wood_block(img, (x0 - 6, counter_y, x1 + 6, counter_y + 18), seed + 3, hexc('#5a4230'), WOOD_D, hexc('#7a5e44'))
    d = ImageDraw.Draw(img); d.line([(px(x0 - 6), px(counter_y)), (px(x1 + 6), px(counter_y))], fill=hexc('#c89a60'), width=px(2))
    if skirt == 'kohaku': kohaku(img, x0 + 6, x1 - 6, counter_y + 18, BASE, seed + 4)
    elif skirt == 'indigo':
        I.fill(img, INDIGO, seed + 4, rect=(x0 + 6, counter_y + 18, x1 - 6, BASE), scale=10, stretch=(.4, 3), contrast=.7)
        shade_rows(img, (x0 + 6, counter_y + 18, x1 - 6, BASE), .75, 1.0)
    else: wood_block(img, (x0 + 6, counter_y + 18, x1 - 6, BASE), seed + 4, WOOD, WOOD_D, WOOD_L, True)
    # roof beam, awning, sign
    wood_block(img, (x0 - 14, top + 60, x1 + 14, aw0), seed + 5, WOOD, WOOD_D, WOOD_L)
    awning(img, x0 - 4, x1 + 4, aw0, aw1, cols, seed + 10)
    lglow(img, (x0 + x1) / 2, aw1 - 10, (x1 - x0) * .5, WARM, .18, .35)
    board(img, (x0 + 22, top, x1 - 22, top + 58), sign, seed + 20, bg=sign_bg or hexc('#ece2cc'), fg=sign_fg, size=sign_size)
    # chōchin at the awning corners
    for (lx, kind, mk) in ((x0 + 16, lanterns[0], marks[0]), (x1 - 16, lanterns[1], marks[1])):
        if kind: lantern(img, lx, aw1 + 52, 24, kind, mk, seed + lx, .6, string=aw1 + 12)


# ───────────── stall interiors ─────────────
def mask_face(img, cx, cy, s, kind, seed):
    d = ImageDraw.Draw(img)
    if kind == 'kitsune':
        for sx in (-1, 1): I.poly(img, [(cx + sx * s * .35, cy - s * .55), (cx + sx * s * .62, cy - s * 1.05), (cx + sx * s * .72, cy - s * .35)], '#efe8da')
        I.fill(img, '#efe8da', seed, poly=[(cx - s * .7, cy - s * .5), (cx + s * .7, cy - s * .5), (cx + s * .5, cy + s * .2), (cx, cy + s * .8), (cx - s * .5, cy + s * .2)], scale=3, contrast=.4)
        for sx in (-1, 1): I.line(img, [(cx + sx * s * .15, cy - s * .12), (cx + sx * s * .55, cy - s * .25)], '#c02a2a', s * .12)
        I.ell(img, (cx - s * .08, cy + s * .55, cx + s * .08, cy + s * .7), '#1a1010')
    elif kind == 'oni':
        for sx in (-1, 1): I.poly(img, [(cx + sx * s * .3, cy - s * .6), (cx + sx * s * .55, cy - s * 1.1), (cx + sx * s * .62, cy - s * .5)], '#e8d8a8')
        I.fill(img, '#b8322a', seed, ell=(cx - s * .72, cy - s * .75, cx + s * .72, cy + s * .8), scale=3, contrast=.5)
        for sx in (-1, 1): I.ell(img, (cx + sx * s * .3 - s * .14, cy - s * .2, cx + sx * s * .3 + s * .14, cy), '#f2d23a')
        I.poly(img, [(cx - s * .4, cy + s * .3), (cx + s * .4, cy + s * .3), (cx, cy + s * .6)], '#2a0a08')
    elif kind == 'hyottoko':
        I.fill(img, '#d8b98a', seed, ell=(cx - s * .66, cy - s * .8, cx + s * .66, cy + s * .8), scale=3, contrast=.4)
        for sx in (-1, 1): I.ell(img, (cx + sx * s * .28 - s * .12, cy - s * .25, cx + sx * s * .28 + s * .12, cy - s * .12 + (sx > 0) * s * .08), '#1a1410')
        I.ell(img, (cx + s * .05, cy + s * .25, cx + s * .35, cy + s * .5), '#b85a4a')
    elif kind == 'okame':
        I.fill(img, '#f2ece0', seed, ell=(cx - s * .72, cy - s * .78, cx + s * .72, cy + s * .82), scale=3, contrast=.3)
        for sx in (-1, 1):
            d.arc([px(cx + sx * s * .3 - s * .14), px(cy - s * .25), px(cx + sx * s * .3 + s * .14), px(cy - s * .05)], 200, 340, fill=(30, 20, 18, 255), width=px(max(1, s * .06)))
            I.soft(img, lambda dd, sx=sx: dd.ellipse([px(cx + sx * s * .42 - s * .16), px(cy + s * .05), px(cx + sx * s * .42 + s * .16), px(cy + s * .3)], fill=(230, 120, 120, 120)), 2)
        I.ell(img, (cx - s * .08, cy + s * .42, cx + s * .08, cy + s * .54), '#b82a2a')
    elif kind == 'tengu':
        I.fill(img, '#b02a22', seed, ell=(cx - s * .66, cy - s * .8, cx + s * .66, cy + s * .8), scale=3, contrast=.5)
        I.poly(img, [(cx - s * .12, cy - s * .05), (cx + s * .12, cy - s * .05), (cx + s * .05, cy + s * .95)], '#c8342a')
        for sx in (-1, 1): I.line(img, [(cx + sx * s * .1, cy - s * .35), (cx + sx * s * .55, cy - s * .5)], '#f2f0e8', s * .14)
    else:   # a round cartoon mask: the kids' favourite
        I.fill(img, kind, seed, ell=(cx - s * .72, cy - s * .75, cx + s * .72, cy + s * .8), scale=3, contrast=.4)
        for sx in (-1, 1): I.ell(img, (cx + sx * s * .28 - s * .16, cy - s * .25, cx + sx * s * .28 + s * .16, cy + s * .08), '#ffffff'); I.ell(img, (cx + sx * s * .28 - s * .07, cy - s * .15, cx + sx * s * .28 + s * .07, cy + s * .02), '#101014')
        d.arc([px(cx - s * .3), px(cy + s * .1), px(cx + s * .3), px(cy + s * .5)], 20, 160, fill=(30, 20, 20, 255), width=px(max(1, s * .08)))
    I.volume(img, (cx - s * .8, cy - s * 1.1, cx + s * .8, cy + s * .9), .45, .3, spec=.12)


def omen_interior(box):
    x0, y0, x1, y1 = box
    kinds = ['kitsune', 'oni', 'hyottoko', 'okame', '#e8c040', 'tengu', '#5aa0d8', 'kitsune', 'oni', '#e87aa0', 'okame', 'hyottoko']
    I.fill(IMG[0], '#3a2a1c', 801, rect=(x0, y0, x1, y1), scale=12, stretch=(3, .4), contrast=.8)   # pegboard
    cols, rows = 4, 3; k = 0
    for r in range(rows):
        for c in range(cols):
            cx = x0 + (c + .5) * (x1 - x0) / cols; cy = y0 + 40 + r * (y1 - y0 - 40) / rows
            I.line(IMG[0], [(cx, cy - 34), (cx, cy - 26)], '#120c08', 2)
            mask_face(IMG[0], cx, cy, 24, kinds[k % len(kinds)], 810 + k); k += 1


def kingyo_interior(box):
    x0, y0, x1, y1 = box; img = IMG[0]
    # goldfish in water bags hanging from a bar
    I.line(img, [(x0, y0 + 16), (x1, y0 + 16)], '#2a1c12', 4)
    rnd = random.Random(7)
    for i, bx in enumerate(np.linspace(x0 + 30, x1 - 30, 6)):
        by = y0 + 70 + (i % 2) * 18
        I.line(img, [(bx, y0 + 16), (bx, by - 30)], '#d8d0c0', 1.4)
        bag = [(bx - 6, by - 30), (bx + 6, by - 30), (bx + 22, by + 4), (bx + 18, by + 30), (bx - 18, by + 30), (bx - 22, by + 4)]
        m = I.fill(img, '#9ec4d8', 830 + i, poly=bag, scale=3, contrast=.3, dark=.2, light=.3)
        for _ in range(1 + i % 2):
            fx, fy = bx + rnd.uniform(-8, 8), by + rnd.uniform(0, 16); c = rnd.choice(['#e8541e', '#e8541e', '#1a1616', '#f2eee6'])
            I.ell(img, (fx - 7, fy - 4, fx + 5, fy + 4), c); I.poly(img, [(fx + 4, fy), (fx + 11, fy - 5), (fx + 11, fy + 5)], c)
        I.line(img, [(bx - 14, by - 10), (bx - 10, by + 18)], '#ffffff', 1.2)
    # paper scoops (poi) in a rack
    for i, px0 in enumerate(np.linspace(x0 + 40, x1 - 40, 7)):
        I.line(img, [(px0, y1 - 8), (px0 + 4, y1 - 60)], '#e84a6a' if i % 2 else '#4a8ae8', 4)
        I.fill(img, '#f4f0e6', 850 + i, ell=(px0 - 14, y1 - 90, px0 + 22, y1 - 56), scale=2, contrast=.3)
        ImageDraw.Draw(img).ellipse([px(px0 - 14), px(y1 - 90), px(px0 + 22), px(y1 - 56)], outline=(230, 80, 110, 255) if i % 2 else (70, 130, 230, 255), width=px(2.4))


def kingyo_tub(img, x0, x1):
    top, bot = 1004, BASE - 4
    stall_shadow(img, x0 + 10, x1 - 10)
    I.fill(img, '#3a7ec8', 861, rect=(x0, top + 14, x1, bot), scale=8, contrast=.5, dark=.35, light=.2)   # blue plastic tub
    shade_rows(img, (x0, top + 14, x1, bot), 1.15, .7)
    I.fill(img, '#6aa8e0', 862, rect=(x0 - 6, top, x1 + 6, top + 16), scale=4, contrast=.4)                 # rim
    I.fill(img, '#1e5a8a', 863, rect=(x0 + 6, top + 2, x1 - 6, top + 13), scale=6, stretch=(4, 1), contrast=1.2)   # water
    rnd = random.Random(9); d = ImageDraw.Draw(img)
    for _ in range(26):
        fx, fy = rnd.uniform(x0 + 16, x1 - 16), rnd.uniform(top + 4, top + 11); c = rnd.choice(['#f2641e', '#f2641e', '#ff8a3a', '#1c1818', '#f4f0e8'])
        I.ell(img, (fx - 5, fy - 2, fx + 4, fy + 2), c); I.poly(img, [(fx + 3, fy), (fx + 8, fy - 2.5), (fx + 8, fy + 2.5)], c)
    for _ in range(18):
        rx = rnd.uniform(x0 + 10, x1 - 30); d.line([(px(rx), px(top + 6)), (px(rx + 20), px(top + 6))], fill=(200, 230, 255, 120), width=px(1.2))
    lglow(img, (x0 + x1) / 2, top + 8, (x1 - x0) * .5, hexc('#7ac0ff'), .18, .25)


def shateki_interior(box):
    x0, y0, x1, y1 = box; img = IMG[0]
    I.fill(img, '#6a1e1a', 870, rect=(x0, y0, x1, y1), scale=14, stretch=(.4, 3), contrast=.7)   # red velvet back
    shade_rows(img, (x0, y0, x1, y1), .7, 1.1)
    shelves = [y0 + 70, y0 + 150, y0 + 230]
    rnd = random.Random(11)
    for si, sy in enumerate(shelves):
        wood_block(img, (x0 - 4, sy, x1 + 4, sy + 10), 871 + si, hexc('#6a4a30'), WOOD_D, hexc('#8a6a48'))
        x = x0 + 14
        while x < x1 - 30:
            kind = rnd.choice(['box', 'box', 'daruma', 'maneki', 'kokeshi', 'candy', 'bear'])
            if kind == 'box':
                w, h = rnd.uniform(26, 40), rnd.uniform(28, 48); c = rnd.choice(['#e8c040', '#3a7ec8', '#e8547a', '#4aa86a', '#f2eee4'])
                I.fill(img, c, 880 + int(x), rect=(x, sy - h, x + w, sy), scale=3, contrast=.4); I.volume(img, (x, sy - h, x + w, sy), .5, .25)
                I.fill(img, '#f4f0e6', 881 + int(x), rect=(x + 4, sy - h * .62, x + w - 4, sy - h * .38), scale=2, contrast=.2)
            elif kind == 'daruma':
                w = 30; I.fill(img, '#c02a22', 882 + int(x), ell=(x, sy - 36, x + w, sy), scale=3, contrast=.5); I.ell(img, (x + 7, sy - 28, x + w - 7, sy - 14), '#f2e8d8')
                I.ell(img, (x + 10, sy - 24, x + 14, sy - 19), '#101010'); I.volume(img, (x, sy - 36, x + w, sy), .55, .35, spec=.2)
            elif kind == 'maneki':
                w = 30; I.fill(img, '#f2eee6', 883 + int(x), ell=(x, sy - 30, x + w, sy), scale=3, contrast=.3); I.fill(img, '#f2eee6', 884 + int(x), ell=(x + 3, sy - 52, x + w - 3, sy - 26), scale=3, contrast=.3)
                for ex in (x + 6, x + w - 6): I.poly(img, [(ex - 5, sy - 46), (ex + 5, sy - 46), (ex, sy - 58)], '#f2eee6')
                I.ell(img, (x + w - 4, sy - 50, x + w + 7, sy - 37), '#f2eee6'); I.line(img, [(x + 4, sy - 28), (x + w - 4, sy - 28)], '#c02a2a', 3)
                for ex in (x + 10, x + 20): I.ell(img, (ex - 2, sy - 42, ex + 2, sy - 38), '#1a1410')
                I.volume(img, (x, sy - 62, x + w + 2, sy), .45, .25)
            elif kind == 'kokeshi':
                w = 18; I.fill(img, rnd.choice(['#c02a2a', '#e8a040', '#3a6ab8']), 885 + int(x), rect=(x, sy - 40, x + w, sy), scale=2, contrast=.4)
                I.ell(img, (x - 3, sy - 60, x + w + 3, sy - 36), '#f0e6d4'); I.fill(img, '#141010', 886 + int(x), poly=[(x - 3, sy - 50), (x + 2, sy - 60), (x + w - 2, sy - 60), (x + w + 3, sy - 50)], scale=2)
                I.volume(img, (x - 3, sy - 60, x + w + 3, sy), .45, .3)
            elif kind == 'candy':
                w = 30; I.fill(img, '#cfe4ea', 887 + int(x), rect=(x, sy - 40, x + w, sy), scale=3, contrast=.2)
                for _ in range(10): cx_, cy_ = rnd.uniform(x + 4, x + w - 4), rnd.uniform(sy - 34, sy - 4); I.ell(img, (cx_ - 3, cy_ - 3, cx_ + 3, cy_ + 3), rnd.choice(['#e84a6a', '#e8c040', '#4aa86a', '#4a7ae8']))
                I.fill(img, '#e84a4a', 888 + int(x), rect=(x - 2, sy - 46, x + w + 2, sy - 38), scale=2)
            else:
                w = 36; I.fill(img, '#8a5a36', 889 + int(x), ell=(x, sy - 30, x + w, sy), scale=3, contrast=.5); I.fill(img, '#8a5a36', 890 + int(x), ell=(x + 5, sy - 56, x + w - 5, sy - 26), scale=3, contrast=.5)
                for ex in (x + 8, x + w - 8): I.ell(img, (ex - 6, sy - 62, ex + 6, sy - 50), '#8a5a36')
                I.ell(img, (x + 13, sy - 40, x + w - 13, sy - 32), '#d8b890'); I.volume(img, (x, sy - 62, x + w, sy), .45, .3)
            x += w + rnd.uniform(8, 16)


def shateki_counter(img, x0, x1, cy):
    for i, (gx, ang) in enumerate(((x0 + 60, -.12), (x0 + 160, -.08), (x0 + 250, -.14))):
        L = 150; ex, ey = gx + math.cos(ang) * L, cy - 8 + math.sin(ang) * L * .3
        I.line(img, [(gx, cy - 6), (ex, ey)], '#2a1c14', 7); I.line(img, [(gx, cy - 6), (gx + 48, cy - 10)], '#6a4424', 12)
    I.fill(img, '#c8a870', 891, rect=(x1 - 60, cy - 30, x1 - 20, cy), scale=3, contrast=.4)
    for k in range(6): I.ell(img, (x1 - 56 + k * 5, cy - 36, x1 - 48 + k * 5, cy - 28), '#d8b888')


def takoyaki_interior(box):
    x0, y0, x1, y1 = box; img = IMG[0]
    I.fill(img, '#2a1a12', 900, rect=(x0, y0, x1, y1), scale=12, contrast=.8)
    for i, bx in enumerate(np.linspace(x0 + 20, x1 - 40, 4)):   # bottles and tins on a shelf
        wood_block(img, (x0, y0 + 90, x1, y0 + 98), 901, hexc('#5a4230'), WOOD_D, hexc('#7a5e44'))
        I.fill(img, ['#3a2410', '#e8d8b0', '#2a4a2a', '#c8a040'][i], 902 + i, rect=(bx, y0 + 48, bx + 22, y0 + 90), scale=2, contrast=.4); I.volume(img, (bx, y0 + 48, bx + 22, y0 + 90), .5, .3, spec=.2)


def takoyaki_counter(img, x0, x1, cy):
    gx0, gx1 = x0 + 26, x1 - 26
    I.fill(img, '#2a2826', 910, rect=(gx0, cy - 34, gx1, cy + 2), scale=4, contrast=.8)          # cast-iron plate
    I.fill(img, '#4a4644', 909, rect=(gx0 - 4, cy - 38, gx1 + 4, cy - 30), scale=3, contrast=.6)
    cols = 8
    for r_ in range(2):
        for c in range(cols):
            bx = gx0 + 20 + c * (gx1 - gx0 - 40) / (cols - 1); by = cy - 24 + r_ * 14
            I.ell(img, (bx - 12, by - 6, bx + 12, by + 8), '#0e0c0c')                                  # the pit
            I.fill(img, '#c8822e', 911 + r_ * 10 + c, ell=(bx - 11, by - 12, bx + 11, by + 6), scale=2, contrast=.6)
            I.volume(img, (bx - 11, by - 12, bx + 11, by + 6), .6, .35, spec=.3)
            I.line(img, [(bx - 6, by - 7), (bx, by - 4), (bx + 6, by - 8)], '#5a2a10', 1.6)
    lglow(img, (gx0 + gx1) / 2, cy - 30, (gx1 - gx0) * .5, hexc('#ff8a3a'), .25, .4)
    for k in range(5):   # steam
        sx = gx0 + 30 + k * (gx1 - gx0 - 60) / 4
        I.soft(img, lambda d, sx=sx: [d.ellipse([px(sx - 18 - j * 8), px(cy - 80 - j * 44), px(sx + 18 + j * 8), px(cy - 44 - j * 44)], fill=(240, 236, 228, 34 - j * 9)) for j in range(3)], 8)


def noren(img, x0, x1, y0, y1, text, col, seed, fg='#f4efe4'):
    n = len(text); w = (x1 - x0) / n
    for i, ch in enumerate(text):
        a, b = x0 + i * w + 3, x0 + (i + 1) * w - 3
        I.fill(img, col, seed + i, rect=(a, y0, b, y1), scale=8, stretch=(.4, 3), contrast=.6, dark=.35, light=.12)
        shade_rows(img, (a, y0, b, y1), .8, 1.0)
        I.text(img, ch, (a + b) / 2, (y0 + y1) / 2 + 4, min(w * .7, (y1 - y0) * .6), fg, SERIF, brush=True)


# ───────────── the taiko tower ─────────────
def yagura(img, x0, x1):
    cx = (x0 + x1) / 2; plat = 700
    stall_shadow(img, x0, x1)
    # back posts, braces, central pole with streamers at its top
    for bx in (x0 + 40, x1 - 60): wood_block(img, (bx, plat - 80, bx + 18, BASE), 701 + bx, hexc('#2a1c14'), WOOD_D, hexc('#3a2a1e'), True)
    wood_block(img, (cx - 9, 238, cx + 9, plat), 703, hexc('#3a2a1e'), WOOD_D, hexc('#5a4230'), True)
    I.fill(img, '#e8c040', 704, ell=(cx - 16, 222, cx + 16, 254), scale=2, contrast=.5); I.volume(img, (cx - 16, 222, cx + 16, 254), .5, .3, spec=.3)
    for k, c in enumerate(['#c02a2a', '#f2eee4', '#3a6ab8', '#e8c040', '#4aa86a']):
        I.line(img, [(cx, 250), (cx + (k - 2) * 18, 330 + abs(k - 2) * 6)], c, 4)
    # the drum on its stand, face-on
    dx, dy, R = cx, 588, 92
    for sx in (-1, 1): I.line(img, [(dx + sx * 60, dy + 40), (dx + sx * 84, plat)], '#2a1c14', 10)
    I.fill(img, '#5a2014', 705, ell=(dx - R - 14, dy - R - 14, dx + R + 14, dy + R + 14), scale=4, contrast=.8)        # lacquered barrel rim
    I.volume(img, (dx - R - 14, dy - R - 14, dx + R + 14, dy + R + 14), .55, .35, spec=.25)
    I.fill(img, '#e6d8b8', 706, ell=(dx - R, dy - R, dx + R, dy + R), scale=5, contrast=.5, dark=.2, light=.15)             # skin
    I.volume(img, (dx - R, dy - R, dx + R, dy + R), .4, .2)
    d = ImageDraw.Draw(img)
    for k in range(28):   # tacks
        a = k / 28 * math.tau; tx, ty = dx + math.cos(a) * (R + 7), dy + math.sin(a) * (R + 7); d.ellipse([px(tx - 3), px(ty - 3), px(tx + 3), px(ty + 3)], fill=(210, 170, 90, 255))
    for k in range(3):    # mitsudomoe: three commas, each head trailing a tapering tail round the rim
        a0 = k / 3 * math.tau - math.pi / 2; rc, hr, T = 38, 19, 1.75
        ts = np.linspace(0, T, 22)
        outer = [(dx + math.cos(a0 - t) * (rc + hr * (1 - t / T)), dy + math.sin(a0 - t) * (rc + hr * (1 - t / T))) for t in ts]
        inner = [(dx + math.cos(a0 - t) * (rc - hr * (1 - t / T) ** 1.6), dy + math.sin(a0 - t) * (rc - hr * (1 - t / T) ** 1.6)) for t in ts[::-1]]
        I.poly(img, outer + inner, '#1c1210')
        hx, hy = dx + math.cos(a0) * rc, dy + math.sin(a0) * rc; I.ell(img, (hx - hr, hy - hr, hx + hr, hy + hr), '#1c1210')
    I.soft(img, lambda d: d.ellipse([px(dx - 60), px(dy - 70), px(dx + 10), px(dy - 20)], fill=(255, 245, 220, 60)), 12)
    for ang in (-.5, -.2): I.line(img, [(dx + 70, dy + 70), (dx + 70 + math.cos(ang - 1.4) * 110, dy + 70 + math.sin(ang - 1.4) * 110)], '#caa068', 7)   # bachi
    # platform, railing, lanterns along the rail
    wood_block(img, (x0 - 10, plat - 70, x0 + 4, plat), 707, WOOD, WOOD_D, WOOD_L, True); wood_block(img, (x1 - 4, plat - 70, x1 + 10, plat), 708, WOOD, WOOD_D, WOOD_L, True)
    wood_block(img, (x0 - 10, plat - 74, x1 + 10, plat - 62), 709, hexc('#5a4230'), WOOD_D, hexc('#7a5e44'))
    wood_block(img, (x0 - 24, plat, x1 + 24, plat + 26), 710, hexc('#5a4230'), WOOD_D, hexc('#7a5e44'))
    d = ImageDraw.Draw(img); d.line([(px(x0 - 24), px(plat)), (px(x1 + 24), px(plat))], fill=hexc('#c89a60'), width=px(2))
    kohaku(img, x0, x1, plat + 26, BASE, 711, stripe=30)
    for fx in (x0 + 4, x1 - 22): wood_block(img, (fx, plat + 26, fx + 18, BASE), 712 + fx, WOOD, WOOD_D, WOOD_L, True)
    board(img, (cx - 58, plat + 40, cx + 58, plat + 96), '太鼓', 713, size=42)
    for i, lx in enumerate((x0 + 34, x0 + 88, x1 - 88, x1 - 34)):
        lantern(img, lx, plat + 64, 19, 'white' if i % 3 == 0 else 'red', '祭' if i % 3 == 0 else None, 720 + i, .5, string=plat + 26)
    STALLS['taiko'] = [x0 - 24, 230, x1 + 24, BASE]


# ───────────── layers ─────────────
IMG = [None]


def sky():
    img = gradient(hexc('#070b1c'), hexc('#2c2032'))
    a = np.asarray(img, np.float32)                                    # a little lift near the horizon from the fair's glow
    t = np.clip((np.linspace(0, 1, SH) - .35) / .65, 0, 1)[:, None, None] ** 2
    a[..., :3] += np.array([46, 22, 8], np.float32) * t; img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')
    rnd = random.Random(21); d = ImageDraw.Draw(img)
    for _ in range(420):                                               # stars, denser and brighter up high
        x, y = rnd.uniform(0, 1800), rnd.uniform(0, 700) ** 1.15 / 700 ** .15
        r = rnd.choice([.8, .8, 1, 1.2, 1.6]); b = int(255 * rnd.uniform(.35, 1) * (1 - y / 900))
        d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=(220, 226, 255, b))
    img.alpha_composite(fog_layer(hexc('#3a3350'), 60, 300, .25, 22, 400))   # thin high cloud
    # hills and the far pagoda
    hill = Image.new('L', (SW, SH), 0); hp = [(0, 640)]
    for x in range(0, 1801, 40): hp.append((x, 505 + 40 * math.sin(x / 260) + 22 * math.sin(x / 97 + 1)))
    hp += [(1800, 1400), (0, 1400)]; ImageDraw.Draw(hill).polygon([(px(x), px(y)) for x, y in hp], fill=255)
    img.alpha_composite(textured_fill(hill, hexc('#161a2e'), hexc('#0a0c16'), hexc('#242638'), 40 * SS, 23, (3, 1), 1.1))
    pg = layer(); x = 1630; base = 540
    for k in range(5):
        w = 120 - k * 18; y = base - k * 38
        I.fill(pg, '#0c0c16', 30 + k, rect=(x - w * .32, y - 24, x + w * .32, y), scale=4)
        I.poly(pg, [(x - w * .75, y - 22), (x + w * .75, y - 22), (x + w * .45, y - 40), (x - w * .45, y - 40)], '#0a0a12')
    I.line(pg, [(x, base - 190), (x, base - 250)], '#0a0a12', 4)
    for k in range(5):
        for sx in (-1, 1): lglow(pg, x + sx * (100 - k * 18) * .7, base - k * 38 - 26, 10, WARM, .7)
    img.alpha_composite(atmos(pg, hexc('#2a2438'), .2))
    tree = layer()
    for i, (tx, th) in enumerate(((120, 300), (230, 360), (330, 280), (1300, 300), (1420, 340), (1700, 330))):
        cedar(tree, tx * SS, 640 * SS, th * SS, 180 * SS, 40 + i, [hexc('#07080e'), hexc('#0b0c14'), hexc('#10111a'), hexc('#15161f'), hexc('#1b1c26')], (hexc('#050508'), hexc('#0a0a0e'), hexc('#121218')))
    img.alpha_composite(atmos(tree, hexc('#1c1a2a'), .25))
    glow(img, 900, 900, 1100, hexc('#c8703a'), .22)                    # the whole fair lights the haze from below
    img.alpha_composite(fog_layer(hexc('#6a4a48'), 560, 760, .35, 24, 320))
    return img


def far(img):
    """Distant garlands of lights on the hill paths and a haze of warm glow."""
    L = layer(); rnd = random.Random(31)
    for (xa, ya, xb, yb, sag, n) in ((-40, 560, 700, 520, 40, 22), (620, 520, 1180, 540, 34, 16), (1100, 530, 1840, 570, 46, 22), (200, 640, 900, 610, 30, 18), (900, 612, 1600, 650, 30, 18)):
        pts = [(xa + (xb - xa) * u, ya + (yb - ya) * u + sag * math.sin(math.pi * u)) for u in np.linspace(0, 1, n)]
        I.line(L, pts, '#1a1210', 1.6)
        for k, (x, y) in enumerate(pts[1:-1]):
            c = hexc('#ff9a48') if k % 3 else hexc('#ffe0a8')
            lglow(L, x, y + 8, 14, c, .55); I.ell(L, (x - 3.5, y + 3, x + 3.5, y + 13), c)
    for i, x in enumerate(range(80, 1800, 230)):                       # far stall roofs peeking over the near row
        w = rnd.uniform(140, 200); y = rnd.uniform(560, 600)
        I.fill(L, rnd.choice(['#4a2a28', '#2a3050', '#4a4038']), 50 + i, poly=[(x - w / 2, y + 20), (x + w / 2, y + 20), (x + w / 2 - 14, y), (x - w / 2 + 14, y)], scale=6)
        lglow(L, x, y + 30, w * .6, WARM, .3, .5)
    img.alpha_composite(atmos(L, hexc('#3a2c34'), .3, .8))
    img.alpha_composite(fog_layer(hexc('#8a5a44'), 540, 700, .35, 32, 300))
    return img


def stalls(img):
    IMG[0] = img
    ground(img, 1068, 1110, 41, hexc('#2e241c'), hexc('#140f0b'), hexc('#46382a'), pebbles=200)
    # お面 — masks
    yatai(img, 6, 300, 560, 100, [RED, CLOTH_W], 'お面', 930, omen_interior, skirt='wood', sign_size=44, marks=('面', '祭'))
    STALLS['omen'] = [0, 560, 306, BASE]
    # 金魚すくい — goldfish scooping
    yatai(img, 336, 648, 548, 200, [INDIGO, CLOTH_W], '金魚すくい', 940, kingyo_interior, skirt='indigo', sign_size=40, lanterns=('white', 'red'), marks=('金', '魚'))
    kingyo_tub(img, 352, 632)
    STALLS['kingyo'] = [330, 548, 654, BASE]
    # 太鼓 — the tower in the middle
    yagura(img, 740, 1060)
    # 射的 — cork-gun gallery
    yatai(img, 1134, 1458, 548, 300, [RED, CLOTH_W], '射的', 960, shateki_interior, skirt='kohaku', sign_size=46, lanterns=('red', 'white'), marks=('射', '的'))
    shateki_counter(img, 1134, 1458, 960)
    STALLS['shateki'] = [1128, 548, 1464, BASE]
    # たこ焼き — takoyaki
    yatai(img, 1496, 1794, 560, 400, [hexc('#d0702a'), CLOTH_W], 'たこ焼き', 950, takoyaki_interior, skirt='wood', sign_size=42, lanterns=('red', 'orange'), marks=('た', 'こ'), sign_bg=hexc('#c8342a'), sign_fg='#f4efe4')
    noren(img, 1510, 1780, 732, 820, 'たこ焼', RED, 420)
    takoyaki_counter(img, 1496, 1794, 950)
    STALLS['takoyaki'] = [1490, 560, 1800, BASE]
    # everything under the awnings is a bit warmer; the top of the scene cooler
    return img


def floor(img):
    ground(img, 1086, 1400, 51, hexc('#3a2e24'), hexc('#18120d'), hexc('#5a4836'), pebbles=2600)
    path = Image.new('L', (SW, SH), 0); ImageDraw.Draw(path).polygon([(px(560), px(1400)), (px(1240), px(1400)), (px(1010), px(1090)), (px(790), px(1090))], fill=255)
    box = path.getbbox(); img.alpha_composite(atmos(textured_fill(path.crop(box), hexc('#4a3c2e'), hexc('#241c14'), hexc('#6a5842'), 22 * SS, 52, (3, 1), 1.1), hexc('#4a3c2e'), .2), box[:2])
    for x in (150, 490, 900, 1300, 1650):                            # pools of warm light in front of each stall
        lglow(img, x, 1150, 260, hexc('#ff9a48'), .32, .35)
    lglow(img, 492, 1110, 180, hexc('#7ac0ff'), .1, .3)              # a cool glint from the goldfish tub
    d = ImageDraw.Draw(img); rnd = random.Random(53)
    for _ in range(60):                                                # scattered paper lantern light specks on the ground
        x, y = rnd.uniform(0, 1800), rnd.uniform(1100, 1400); r = rnd.uniform(1, 2.2)
        d.ellipse([px(x - r * 2), px(y - r), px(x + r * 2), px(y + r)], fill=(255, 190, 110, 60))
    return img


def string_pts(p0, p1, sag, n):
    return [(p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u + sag * 4 * u * (1 - u)) for u in np.linspace(0, 1, n)]


def lanterns(img):
    top = (900, 246)
    for (end, sag, n, r) in (((-60, 80), 150, 13, 22), ((-60, 250), 110, 12, 24), ((1860, 80), 150, 13, 22), ((1860, 250), 110, 12, 24)):
        pts = string_pts(top, end, sag, 60); I.line(img, pts, '#140c08', 2.2)
        for k, u in enumerate(np.linspace(.1, .96, n)):
            x, y = pts[int(u * 59)]
            kind = 'red' if k % 2 == 0 else 'white'
            rr = r * (0.85 + .3 * u)
            lantern(img, x, y + rr * 1.5, rr, kind, '祭' if kind == 'white' and k % 4 == 1 else None, 600 + k + int(end[1]), .55, string=y)
    return img


def near(img):
    for x, kind in ((64, 'red'), (1736, 'white')):
        wood_block(img, (x - 18, 160, x + 18, 1420), 90 + x, hexc('#1c140e'), hexc('#080604'), hexc('#2c2016'), True)
        lantern(img, x + (60 if x < 900 else -60), 520, 62, kind, '祭', 95 + x, .7, string=380)
        I.line(img, [(x, 380), (x + (60 if x < 900 else -60), 380)], '#120c08', 6)
    warm_pal = [hexc('#0a0806'), hexc('#140e0a'), hexc('#20160e'), hexc('#2c1e12'), hexc('#3a2816')]
    near_fern(img, 380, 1440, 420, 61, lean=.35, pal=warm_pal); near_fern(img, 1440, 1440, 400, 62, lean=-.35, pal=warm_pal)
    return img


def matsuri():
    P.set_size(1800, 1400)
    st = Stack('matsuri')
    img = sky(); img = st.cut(img, 'sky', .06)
    img = far(img); img = st.cut(img, 'far', .25)
    img = stalls(img); img = st.cut(img, 'stalls', .5)
    img = floor(img); img = st.cut(img, 'floor', .8)
    img = lanterns(img); img = st.cut(img, 'lanterns', .95)
    img = near(img)
    st.finish(img, 'near', 1.5, blur=5, lift=(7, 6, 10), sat=0.9, gamma=1.04)
    prev = os.path.join(OUT, 'preview-matsuri.jpg')
    if os.path.exists(prev): shutil.move(prev, os.path.join(HERE, 'L', 'preview-matsuri.jpg'))
    meta = {'layers': LY.MANIFEST['matsuri'],
            'L3': {'stalls': {'g': 1080}, 'floor': {'g': 1090}},
            'stalls': STALLS, 'sky': [0, 40, 1800, 470]}
    json.dump(meta, open(os.path.join(HERE, 'matsuri.json'), 'w'), indent=1)
    print(json.dumps(meta))


if __name__ == '__main__':
    matsuri()
