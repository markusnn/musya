#!/usr/bin/env python3
"""«Лес за тории» (add-on fo): an old hand-painted map of the forest behind the house (aged paper, ink, a little colour),
15 painted night vignettes (14 landmarks + the heart of the forest) and 10 forest finds.
Usage: cd art && python3 forest_art.py ../assets/items [map] [cards] [items]
  → atlas_fomap.webp (map 700×1040), atlas_fov1.webp + atlas_fov2.webp (vignettes 420×285, 2 columns),
    atlas_foi.webp (items) and forest.json (rects); previews go to art/out/."""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc, fbm
import items as I
from items import px, canvas, fill, volume, floor_shadow, line, ell, poly, text, H, dk, lt, SERIF, mask_poly
from room_items import blob, clip, cr
import travel_art as T
from travel_art import card, vgrad, glowc, mist, cedars, foliage, lantern_glow, stone_lantern, musya, paw, newl, vol, rgba, reflect, torii_front, PINE

OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
CW, CH = T.CW, T.CH          # vignettes are painted at 560×380 and shrunk to 420×285
VW, VH = 420, 285
MW, MH, GY, CS = 700, 1040, 130, 100   # map: 7×8 cells of 100 px below a 130 px cloud strip
INK = (36, 27, 20)
def ink(a=225): return INK + (a,)
def cc(c, r): return (c * CS + CS / 2, GY + r * CS + CS / 2)
# landmark id → cell (must match feat/forest.js)
LM = {'well': (1, 7), 'jizo': (4, 6), 'fox': (6, 6), 'bamboo': (0, 5), 'bridge': (2, 5), 'tea': (3, 4), 'mush': (5, 4),
      'hotaru': (1, 3), 'cedar': (2, 2), 'lotus': (5, 2), 'hermit': (0, 1), 'neko': (6, 1), 'temple': (1, 0), 'stairs': (3, 0)}


# ───────────── the map ─────────────
def paper():
    img = canvas(MW, MH); w, h = img.size
    n = fbm(w, h, 140 * P.SS, 5, 7); n2 = fbm(w, h, 14 * P.SS, 3, 8); st = fbm(w, h, 240 * P.SS, 4, 9)
    rgb = np.array([186, 163, 120], np.float32)[None, None] * (0.84 + 0.2 * n[..., None] + 0.07 * n2[..., None])
    stain = np.clip((st - .6) * 3.5, 0, 1)[..., None]; rgb = rgb * (1 - stain * .3) + np.array([110, 76, 40], np.float32) * stain * .3
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); en = fbm(w, h, 30 * P.SS, 4, 10)
    d = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy)) / P.SS + en * 22
    e = np.clip(1 - d / 46, 0, 1) ** 1.6; rgb = rgb * (1 - e[..., None] * .7) + np.array([60, 36, 18], np.float32) * e[..., None] * .35
    for cx in (w // 2,): rgb[:, cx - 2:cx] *= .86; rgb[:, cx:cx + 6] *= 1.05
    for cy in (h // 2,): rgb[cy - 2:cy] *= .86; rgb[cy:cy + 6] *= 1.05
    rr = np.random.default_rng(3)
    for _ in range(70):   # foxing spots
        x, y, r = rr.uniform(0, w), rr.uniform(0, h), rr.uniform(2, 9) * P.SS
        m = ((xx - x) ** 2 + (yy - y) ** 2) < r * r; rgb[m] = rgb[m] * .9 + np.array([120, 80, 40]) * .1
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), np.full((h, w), 255)]).astype(np.uint8), 'RGBA')


def wash(img, col, a, fn, blur=2.0):
    l = newl(img); fn(ImageDraw.Draw(l), H(col)[:3] + (a,)); img.alpha_composite(l.filter(ImageFilter.GaussianBlur(blur * P.SS)))


def bleed(lay, b=.55): return lay.filter(ImageFilter.GaussianBlur(b * P.SS))


def tree_c(L, x, y, s):
    line(L, [(x, y), (x, y - 17 * s)], ink(200), 1.1 * s)
    for k in range(4):
        yy = y - 5 * s - k * 4.2 * s; ww = (7.5 - k * 1.5) * s
        line(L, [(x - ww, yy + 2.2 * s), (x, yy - 2.6 * s), (x + ww, yy + 2.2 * s)], ink(205), 1.1 * s)


def tree_r(L, x, y, s, rr):
    line(L, [(x, y), (x, y - 8 * s)], ink(190), 1.1 * s); d = ImageDraw.Draw(L)
    for k in range(5):
        a = k / 5 * math.pi * 2; cx, cy, r = x + math.cos(a) * 4 * s, y - 13 * s + math.sin(a) * 3 * s, 4.2 * s
        d.arc([px(cx - r), px(cy - r), px(cx + r), px(cy + r)], 160 + k * 20, 380 + k * 20, fill=ink(190), width=max(1, px(.9 * s)))


def ptsd(pts, step=9):
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
        out += [(x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n) for k in range(n)]
    return out


STREAM = [(560, 392), (520, 450), (470, 520), (430, 590), (360, 650), (250, 690), (160, 750), (70, 800), (-10, 830)]
TRAIL = [(350, 900), (420, 820), (440, 760), (350, 715), (250, 690), (300, 640), (350, 590), (320, 520), (260, 470), (250, 380), (300, 300), (350, 240), (350, 180), (350, 120)]


def cloud_band(img, blobs, fillc='#e2d2a4'):
    L = newl(img); d = ImageDraw.Draw(L)
    for x, y, rx, ry in blobs: d.ellipse([px(x - rx - 1.6), px(y - ry - 1.6), px(x + rx + 1.6), px(y + ry + 1.6)], fill=ink(200))
    for x, y, rx, ry in blobs: d.ellipse([px(x - rx), px(y - ry), px(x + rx), px(y + ry)], fill=H(fillc))
    for x, y, rx, ry in blobs: d.arc([px(x - rx * .6), px(y - ry * .5), px(x + rx * .6), px(y + ry * .7)], 200, 320, fill=ink(110), width=max(1, px(.8)))
    img.alpha_composite(bleed(L, .4))


def torii_glyph(L, x, b, w, h, col='#b8402a'):
    for sd in (-1, 1): line(L, [(x + sd * w * .34, b), (x + sd * w * .32, b - h)], col, w * .09)
    line(L, [(x - w * .45, b - h * .72), (x + w * .45, b - h * .72)], col, w * .07)
    pts = [(x - w * .58 + w * 1.16 * u / 10, b - h * .98 + (4 * (u / 10 - .5) ** 2) * h * .12) for u in range(11)]
    line(L, pts, INK + (240,), w * .1); line(L, [(x - w * .5, b - h * .86), (x + w * .5, b - h * .86)], col, w * .06)


def glyphs(img):
    L = newl(img); d = ImageDraw.Draw(L); rr = random.Random(5)
    # the forest: little ink cedars and round trees everywhere except landmarks, water and the trail
    busy = [cc(*v) for v in LM.values()] + [(350, 880), (550, 380)]
    sd = ptsd(STREAM, 14) + ptsd(TRAIL, 14)
    wash(img, '#56603e', 70, lambda dd, c: [dd.ellipse([px(x - 26), px(y - 18), px(x + 26), px(y + 18)], fill=c) for x, y in
         [(rr.uniform(10, 690), rr.uniform(150, 920)) for _ in range(110)]], 6)
    for _ in range(330):
        x, y = rr.uniform(14, 686), rr.uniform(150, 925)
        if min(math.hypot(x - a, y - b) for a, b in busy) < 40 or min(math.hypot(x - a, y - b) for a, b in sd) < 15: continue
        s = rr.uniform(.8, 1.15)
        (tree_c if rr.random() < .62 else lambda L_, x_, y_, s_: tree_r(L_, x_, y_, s_, rr))(L, x, y, s)
    # the stream and the trail
    wash(img, '#5d7f88', 150, lambda dd, c: dd.line([(px(x), px(y)) for x, y in STREAM], fill=c, width=px(13), joint='curve'), 1.5)
    for off in (-7, 7): line(L, [(x, y + off) for x, y in STREAM], ink(190), 1.1)
    for x, y in ptsd(STREAM, 26)[1::2]: line(L, [(x - 4, y), (x, y - 1.5), (x + 4, y)], ink(120), .8)
    for x, y in ptsd(TRAIL, 8)[::2]: d.ellipse([px(x - 1.5), px(y - 1.5), px(x + 1.5), px(y + 1.5)], fill=(150, 46, 30, 210))
    # mountains behind the clouds
    for k, (y, a) in enumerate(((112, 70), (124, 110))):
        pts = [(x, y - 30 * abs(math.sin(x / (60 + k * 25) + k)) - 20 * rr.random()) for x in range(-10, 720, 20)]
        wash(img, '#3a3a34', a, lambda dd, c, p=pts: dd.polygon([(px(x), px(y)) for x, y in p + [(720, 140), (-10, 140)]], fill=c), 3)
    img.alpha_composite(bleed(L)); L = newl(img); d = ImageDraw.Draw(L)
    # landmarks
    def lab(t, x, y, s=12): text(L, t, x, y, s, ink(235), SERIF)
    x, y = cc(*LM['well']); ell(L, (x - 13, y - 2, x + 13, y + 8), ink(220)); ell(L, (x - 10, y - 1, x + 10, y + 5), (30, 40, 46, 255))
    for s_ in (-1, 1): line(L, [(x + s_ * 12, y + 3), (x + s_ * 12, y - 20)], ink(), 1.6)
    line(L, [(x - 17, y - 20), (x, y - 27), (x + 17, y - 20)], ink(), 2); lab('古井戸', x, y + 24)
    x, y = cc(*LM['jizo']); blob(L, [(x - 8, y + 10), (x - 9, y - 4), (x, y - 10), (x + 9, y - 4), (x + 8, y + 10)], '#8a887c', 11, scale=2, k=.4)
    ell(L, (x - 6, y - 19, x + 6, y - 8), '#8a887c'); poly(L, [(x - 8, y - 8), (x + 8, y - 8), (x, y + 1)], '#b8322a'); ell(L, (x - 6, y - 22, x + 6, y - 16), '#b8322a'); lab('地蔵', x, y + 24)
    x, y = cc(*LM['fox']); fill(L, '#4a4030', 12, poly=[(x - 26, y + 10), (x - 14, y - 10), (x + 14, y - 12), (x + 28, y + 10)], scale=3)
    ell(L, (x - 9, y - 3, x + 9, y + 10), (16, 12, 10, 255)); ell(L, (x - 5, y + 2, x - 2, y + 4), '#f0b040'); ell(L, (x + 2, y + 2, x + 5, y + 4), '#f0b040')
    for k, (fx, fy) in enumerate(((x - 20, y - 18), (x + 18, y - 22), (x + 2, y - 30))): glowc(L, fx, fy, 7, '#6ab0ff', .8); ell(L, (fx - 1.6, fy - 2.4, fx + 1.6, fy + 1.6), '#d8f0ff')
    lab('狐穴', x, y + 26)
    x, y = cc(*LM['bamboo'])
    for k in range(9):
        bx = x - 24 + k * 6 + rr.uniform(-1, 1); line(L, [(bx, y + 14), (bx + 1, y - 30)], (70, 110, 60, 235), 1.8)
        for j in range(4): line(L, [(bx - 1.5, y + 8 - j * 10), (bx + 2, y + 8 - j * 10)], ink(200), .8)
        line(L, [(bx, y - 24 + k % 3 * 5), (bx + 6, y - 28 + k % 3 * 5)], (70, 110, 60, 200), 1)
    lab('竹林', x + 6, y + 26)
    x, y = cc(*LM['bridge']); line(L, [(x - 22, y + 8), (x - 10, y - 2), (x + 10, y - 2), (x + 22, y + 8)], '#9a3a22', 3.4)
    line(L, [(x - 20, y - 4), (x - 10, y - 12), (x + 10, y - 12), (x + 20, y - 4)], '#9a3a22', 1.4)
    for k in range(-2, 3): line(L, [(x + k * 8, y - (12 if abs(k) < 2 else 6)), (x + k * 8, y - (2 if abs(k) < 2 else -4))], '#9a3a22', 1.2)
    lab('橋', x - 26, y - 22, 13)
    x, y = cc(*LM['tea']); fill(L, '#6a6a5a', 13, rect=(x - 22, y + 2, x + 22, y + 8), scale=2)
    for k in (-16, -2, 14): line(L, [(x + k, y + 2), (x + k + rr.uniform(-2, 2), y - 10 - rr.uniform(0, 8))], ink(), 2)
    line(L, [(x - 26, y - 10), (x - 4, y - 22), (x + 12, y - 16)], ink(), 2); ell(L, (x + 16, y - 2, x + 26, y + 5), '#7a7a70'); lab('茶室跡', x, y + 24)
    x, y = cc(*LM['mush'])
    for k, (mx, ms, c) in enumerate(((-14, 1, '#8a4a2a'), (0, 1.3, '#7a4024'), (14, .9, '#8a4a2a'), (-5, .7, '#c8e8c0'), (9, .6, '#c8e8c0'))):
        if c == '#c8e8c0': glowc(L, x + mx, y + 2, 9, '#a8f0a0', .5)
        line(L, [(x + mx, y + 8), (x + mx, y + 8 - 8 * ms)], '#e8dcc0', 2.6 * ms)
        poly(L, [(x + mx - 7 * ms, y + 8 - 7 * ms), (x + mx, y + 8 - 13 * ms), (x + mx + 7 * ms, y + 8 - 7 * ms)], c)
    lab('茸', x + 24, y - 10, 13)
    x, y = cc(*LM['hotaru'])
    for k in range(12): line(L, [(x - 22 + k * 4, y + 12), (x - 22 + k * 4 + rr.uniform(-3, 3), y + 2 - rr.uniform(0, 6))], ink(170), .9)
    for k in range(9):
        fx, fy = x + rr.uniform(-24, 24), y + rr.uniform(-26, 2); glowc(L, fx, fy, 8, '#e8f070', .9); ell(L, (fx - 1.2, fy - 1.2, fx + 1.2, fy + 1.2), '#fffbd0')
    lab('蛍', x - 30, y - 16, 13)
    x, y = cc(*LM['cedar']); line(L, [(x, y + 16), (x, y - 36)], ink(), 4)
    for k in range(6):
        yy = y + 4 - k * 7; ww = 24 - k * 3.6; line(L, [(x - ww, yy + 4), (x, yy - 4), (x + ww, yy + 4)], ink(), 2.2)
    line(L, [(x - 6, y + 4), (x + 6, y + 4)], '#d8c890', 2.4)
    for k in (-3, 2): poly(L, [(x + k, y + 5), (x + k + 3, y + 5), (x + k + 1, y + 9), (x + k + 4, y + 12), (x + k + 1, y + 12)], '#f4f0e4')
    lab('大杉', x + 30, y + 14)
    x, y = cc(*LM['lotus']); wash(L, '#5d7f88', 200, lambda dd, c: dd.ellipse([px(x - 32), px(y - 15), px(x + 32), px(y + 15)], fill=c), .8)
    d.ellipse([px(x - 33), px(y - 16), px(x + 33), px(y + 16)], outline=ink(210), width=px(1.2))
    for k, (lx, ly) in enumerate(((-16, -4), (8, 4), (18, -6), (-4, 7))):
        ell(L, (x + lx - 6, y + ly - 3, x + lx + 6, y + ly + 3), '#4a6a3a'); ell(L, (x + lx - 2, y + ly - 4, x + lx + 2, y + ly), '#e8a0b0') if k % 2 == 0 else None
    lab('蓮池', x, y + 26)
    x, y = cc(*LM['hermit']); fill(L, '#5a4a32', 14, rect=(x - 14, y - 4, x + 14, y + 10), scale=2)
    fill(L, '#8a7a50', 15, poly=[(x - 20, y - 2), (x, y - 20), (x + 20, y - 2)], scale=2, stretch=(.3, 2)); ell(L, (x + 3, y, x + 9, y + 6), '#f0b860')
    for k in range(3): ell(L, (x + 6 + k * 3, y - 26 - k * 7, x + 12 + k * 4, y - 22 - k * 7), (120, 120, 112, 120))
    lab('庵', x + 28, y + 6, 13)
    x, y = cc(*LM['neko']); blob(L, [(x - 18, y + 8), (x - 16, y - 4), (x - 4, y - 8), (x + 8, y - 12), (x + 16, y - 6), (x + 18, y + 8)], '#8e8c84', 16, scale=2, k=.5)
    poly(L, [(x + 6, y - 10), (x + 8, y - 18), (x + 11, y - 11)], '#8e8c84'); poly(L, [(x + 12, y - 9), (x + 16, y - 16), (x + 17, y - 7)], '#8e8c84')
    line(L, [(x - 16, y + 6), (x - 24, y + 2), (x - 22, y - 4)], '#7e7c74', 2.2); lab('猫石', x - 6, y + 24)
    x, y = cc(*LM['temple']); fill(L, '#3a3028', 17, rect=(x - 18, y - 6, x + 18, y + 10), scale=2)
    poly(L, [(x - 28, y - 4), (x - 18, y - 12), (x, y - 20), (x + 18, y - 12), (x + 28, y - 4), (x + 18, y - 8), (x - 18, y - 8)], ink(240))
    fill(L, '#7a6a50', 18, rect=(x - 22, y + 10, x + 22, y + 14), scale=2); ell(L, (x - 3, y + 1, x + 3, y + 7), '#e0a050'); lab('廃寺', x, y + 26)
    x, y = cc(*LM['stairs'])
    for k in range(7): yy = y + 16 - k * 6; ww = 16 - k * 1.7; line(L, [(x - ww, yy), (x + ww, yy)], ink(225 - k * 22), 2)
    lab('石段', x + 30, y + 6)
    # home: the torii, the house
    torii_glyph(L, 350, 900, 44, 34); lab('鳥居', 395, 885, 11)
    x, y = 350, 995; fill(L, '#4a3a2a', 19, rect=(x - 34, y - 14, x + 34, y + 14), scale=2)
    poly(L, [(x - 46, y - 12), (x - 30, y - 30), (x + 30, y - 30), (x + 46, y - 12)], ink(240)); ell(L, (x - 18, y - 6, x - 6, y + 4), '#f0b050'); ell(L, (x + 6, y - 6, x + 18, y + 4), '#f0b050')
    glowc(L, x, y, 40, '#ffb050', .3); lab('家', x + 58, y - 6, 15)
    img.alpha_composite(bleed(L, .45))
    # the heart of the forest: an old torii standing on clouds (hidden by drifting clouds in the game until the end)
    glowc(img, 350, 70, 70, '#ffe0a0', .55)
    L = newl(img); torii_glyph(L, 350, 96, 66, 58, '#c04a2c'); img.alpha_composite(bleed(L, .4))
    text(img, '森の心', 350, 18, 13, ink(235), SERIF)
    rr2 = random.Random(9)
    cloud_band(img, [(x, 104 + rr2.uniform(-6, 6), rr2.uniform(26, 44), rr2.uniform(8, 12)) for x in range(10, 700, 46)])
    cloud_band(img, [(x, 122 + rr2.uniform(-4, 4), rr2.uniform(30, 48), rr2.uniform(9, 13)) for x in range(-20, 720, 52)])
    # cartouche, seal and compass
    L = newl(img); d = ImageDraw.Draw(L)
    d.rectangle([px(18), px(940), px(64), px(1024)], fill=(214, 196, 150, 255), outline=ink(230), width=px(1.6))
    d.rectangle([px(22), px(944), px(60), px(1020)], outline=ink(160), width=px(.8))
    for k, ch in enumerate('裏山之図'): text(L, ch, 41, 956 + k * 18, 15, ink(240), SERIF)
    d.rectangle([px(72), px(990), px(98), px(1016)], fill=(168, 44, 34, 225)); text(L, '森', 85, 1003, 15, (230, 210, 180, 255), SERIF)
    x, y = 646, 990; d.ellipse([px(x - 26), px(y - 26), px(x + 26), px(y + 26)], outline=ink(200), width=px(1.2))
    poly(L, [(x, y - 30), (x - 6, y), (x + 6, y)], (150, 46, 30, 235)); poly(L, [(x, y + 26), (x - 5, y), (x + 5, y)], ink(220))
    line(L, [(x - 26, y), (x + 26, y)], ink(160), .8); text(L, '北', x, y - 40, 13, ink(240), SERIF)
    img.alpha_composite(bleed(L, .4))
    out = img.resize((MW, MH), Image.LANCZOS)
    out = P.grade(out, lift=(4, 3, 2), sat=.9, vignette=.25)
    return P.grain(out, 5, 11)


# ───────────── vignettes ─────────────
def fin(img, name):
    return T.finish_card(img, name, sat=.9, lift=(5, 6, 9), vig=.45).resize((VW, VH), Image.LANCZOS)


def night(img, seed, top='#070b12', mid='#121c22', bot='#0b0f0d', fogc='#30404a', moon=None):
    vgrad(img, [(0, top), (.55, mid), (1, bot)])
    if moon: glowc(img, moon[0], moon[1], 110, '#c8d4e8', .35); fill(img, '#e8ecf0', seed, ell=(moon[0] - 16, moon[1] - 16, moon[0] + 16, moon[1] + 16), scale=2, contrast=.4)
    cedars(img, 250, 9, 200, 300, seed, fogc=fogc, fog_amt=.7)
    mist(img, 140, 300, '#4a5a62', .5, seed + 1)
    cedars(img, 330, 5, 260, 360, seed + 2, fogc='#121a1c', fog_amt=.3, w=(70, 100))


def ground(img, seed, y=300, col='#1c2220'):
    fill(img, col, seed, poly=[(0, y + 6), (180, y - 4), (400, y + 2), (560, y - 6), (560, 380), (0, 380)], scale=6, stretch=(3, 1), contrast=1.2)


def musya_l(img, x, base, h, seed=1, side=1, look=0.0):
    musya(img, x, base, h, rim='#ffc070', rim_side=side, seed=seed, bag=False, look=look)
    lx = x + side * h * .5; glowc(img, lx, base - h * .15, h * 2.2, '#ffa850', .3)
    line(img, [(lx, base), (lx, base - h * .12)], '#2a1a10', 1); lantern_glow(img, lx, base - h * .2, h * .075, s=.7)


def c_well():
    img = card(); night(img, 300); ground(img, 301)
    x, b = 330, 330; L = newl(img)
    fill(L, '#5a5a52', 302, rect=(x - 70, b - 62, x + 70, b), scale=4, contrast=1.3)
    for k in range(4):
        line(L, [(x - 70, b - 15 * k - 2), (x + 70, b - 15 * k - 2)], '#26261f', 1.3)
        for j in range(5): xx = x - 60 + j * 28 + (k % 2) * 14; line(L, [(xx, b - 15 * k - 2), (xx, b - 15 * k - 16)], '#26261f', 1.1)
    fill(L, '#6a6a62', 303, ell=(x - 72, b - 74, x + 72, b - 50), scale=3); fill(L, '#04070a', 304, ell=(x - 60, b - 70, x + 60, b - 54), scale=2)
    for sd in (-1, 1): fill(L, '#3a2a1e', 305 + sd, rect=(x + sd * 62 - 4, b - 150, x + sd * 62 + 4, b - 58), scale=2, stretch=(.2, 3))
    fill(L, '#2a1e16', 307, rect=(x - 70, b - 128, x + 70, b - 122), scale=2); line(L, [(x, b - 125), (x, b - 92)], '#8a7a5a', 1.2)
    fill(L, '#4a3a28', 308, poly=[(x - 12, b - 92), (x + 12, b - 92), (x + 10, b - 74), (x - 10, b - 74)], scale=2)
    fill(L, '#22282c', 309, poly=[(x - 92, b - 140), (x, b - 180), (x + 92, b - 140), (x + 84, b - 134), (x, b - 168), (x - 84, b - 134)], scale=3)
    vol(img, L, (x - 92, b - 182, x + 92, b), .45, .25)
    glowc(img, x, b - 62, 50, '#7ab8e0', .45, .3)
    for k in range(5): glowc(img, x - 40 + k * 20, b - 62 - (k % 2) * 3, 4, '#d8f0ff', .9)
    musya_l(img, 170, 356, 52, seed=310)
    paw(img); return fin(img, 'well')


def c_bamboo():
    img = card(); vgrad(img, [(0, '#0a1410'), (.6, '#16261c'), (1, '#0a100c')]); rr = random.Random(41)
    for li, (n, wmin, wmax, amt) in enumerate(((36, 3, 6, .6), (22, 6, 11, .35), (12, 11, 19, .08))):
        lay = newl(img)
        for i in range(n):
            x = rr.uniform(-20, CW + 20)
            if 290 < x < 370: x += 110
            w = rr.uniform(wmin, wmax); col = mixc(H('#1e3a24'), H('#4a7a44'), rr.random() * .7); lean = rr.uniform(-6, 6)
            fill(lay, col, 400 + i + li * 50, poly=[(x - w / 2, 380), (x + w / 2, 380), (x + w / 2 + lean, -5), (x - w / 2 + lean, -5)], scale=3, stretch=(.2, 4), contrast=1.2)
            for k in range(int(rr.uniform(3, 6))):
                yy = rr.uniform(20, 360); line(lay, [(x - w / 2 + lean * (1 - yy / 380), yy), (x + w / 2 + lean * (1 - yy / 380), yy)], dk(col, .45), max(.8, w * .16))
        volume(lay, (0, 0, CW, CH), .3, 0, lx=-.8, ly=0); img.alpha_composite(P.atmos(lay, H('#1a2a26'), amt))
        if li == 0: mist(img, 160, 380, '#3a5048', .4, 42)
    glowc(img, 330, 210, 150, '#ffe8a0', .4); L = newl(img)
    fill(L, '#f4e8a8', 45, rect=(323, -5, 337, 380), scale=2, stretch=(.2, 4), contrast=.5)
    for yy in (60, 130, 200, 270): line(L, [(322, yy), (338, yy)], '#c8b060', 1.6)
    img.alpha_composite(L); glowc(img, 330, 236, 40, '#fff8d8', .6, 1.6)
    fill(img, '#2a2a20', 43, poly=[(0, 380), (560, 380), (560, 350), (0, 356)], scale=5, stretch=(3, 1))
    musya_l(img, 250, 360, 48, seed=14, look=.6)
    paw(img); return fin(img, 'bamboo')


def c_temple():
    img = card(); night(img, 320, fogc='#2a3640'); ground(img, 321, 300, '#22242a')
    L = newl(img)
    fill(L, '#4a4a46', 322, rect=(120, 262, 440, 304), scale=4, contrast=1.2)
    for k in range(3): fill(L, '#5a5a54', 323 + k, rect=(230 - k * 10, 304 + k * 9, 330 + k * 10, 313 + k * 9), scale=3)
    fill(L, '#2a2018', 326, rect=(150, 180, 410, 264), scale=4, stretch=(.3, 2), contrast=1.3)
    for k in range(5): line(L, [(150 + k * 65, 180), (150 + k * 65, 264)], '#140e0a', 3)
    fill(L, '#3a2c1e', 327, rect=(218, 196, 342, 262), scale=3)
    fill(L, '#0c0806', 328, rect=(246, 198, 314, 262), scale=2)
    fill(L, '#1a1e22', 329, poly=[(84, 198), (130, 180), (200, 140), (280, 112), (360, 140), (430, 180), (476, 198), (446, 196), (280, 130), (114, 196)], scale=4, stretch=(3, 1))
    fill(L, '#14171a', 330, poly=[(114, 196), (280, 130), (446, 196), (430, 186), (280, 128), (130, 186)], scale=3)
    vol(img, L, (84, 110, 476, 320), .35, .2)
    glowc(img, 280, 236, 34, '#ffb060', .5); fill(img, '#ffd890', 331, rect=(278, 230, 282, 242), scale=1)
    stone_lantern(img, 92, 336, 96, 332, lit=False, col='#55554e')
    rr = random.Random(333)
    for _ in range(60): x, y = rr.uniform(140, 440), rr.uniform(262, 340); ell(img, (x - 2.5, y - 1.2, x + 2.5, y + 1.2), mixc(H('#7a3a1a'), H('#c87a2a'), rr.random()))
    mist(img, 240, 380, '#3a4650', .45, 334)
    musya_l(img, 300, 364, 46, seed=335)
    paw(img); return fin(img, 'temple')


def c_jizo():
    img = card(); night(img, 340, moon=(470, 70)); ground(img, 341, 296, '#1e2a20')
    x, b = 300, 330; L = newl(img)
    fill(L, '#5a5a52', 342, rect=(x - 42, b - 18, x + 42, b + 4), scale=3)
    blob(L, [(x - 34, b - 18), (x - 38, b - 70), (x - 26, b - 106), (x + 26, b - 106), (x + 38, b - 70), (x + 34, b - 18)], '#8a887e', 343, scale=3, k=.55)
    blob(L, [(x - 24, b - 116), (x - 26, b - 140), (x - 14, b - 158), (x + 14, b - 158), (x + 26, b - 140), (x + 24, b - 116), (x, b - 106)], '#908e84', 344, scale=3, k=.55)
    fill(L, '#b02a22', 345, poly=[(x - 36, b - 108), (x + 36, b - 108), (x + 26, b - 70), (x, b - 58), (x - 26, b - 70)], scale=2, contrast=1.1)
    fill(L, '#b02a22', 346, poly=[(x - 24, b - 150), (x - 18, b - 166), (x, b - 172), (x + 18, b - 166), (x + 24, b - 150)], scale=2)
    for sd in (-1, 1): line(L, [(x + sd * 13, b - 132), (x + sd * 6, b - 130)], '#3a3832', 1.6)
    line(L, [(x - 4, b - 120), (x, b - 118), (x + 4, b - 120)], '#3a3832', 1.2)
    vol(img, L, (x - 42, b - 172, x + 42, b + 4), .55, .3)
    fill(img, '#ece6d8', 347, poly=[(x + 50, b), (x + 58, b - 14), (x + 66, b)], scale=1); fill(img, '#1a1a18', 348, rect=(x + 53, b - 6, x + 63, b), scale=1)
    line(img, [(x - 56, b), (x - 56, b - 40)], '#5a4a30', 1.4)
    for k, c in enumerate(('#d84a3a', '#e0c040', '#4a8ad0', '#e8e0d0')):
        a = k * math.pi / 2 + .4; poly(img, [(x - 56, b - 40), (x - 56 + math.cos(a) * 11, b - 40 + math.sin(a) * 11), (x - 56 + math.cos(a + .9) * 8, b - 40 + math.sin(a + .9) * 8)], c)
    glowc(img, x, b - 120, 90, '#c8d4e8', .15)
    musya_l(img, 170, 360, 50, seed=349, side=1)
    paw(img); return fin(img, 'jizo')


def c_bridge():
    img = card(); night(img, 360, moon=(110, 60))
    fill(img, '#1e2620', 361, poly=[(0, 240), (560, 230), (560, 380), (0, 380)], scale=6, stretch=(3, 1))
    fill(img, '#142028', 362, poly=[(0, 270), (560, 250), (560, 330), (0, 360)], scale=5, stretch=(4, 1), contrast=1.3)
    rr = random.Random(363)
    for _ in range(40): x = rr.uniform(0, 560); y = 262 + rr.uniform(0, 80) - x * .04; line(img, [(x, y), (x + rr.uniform(10, 30), y)], (150, 180, 200, 70), 1)
    L = newl(img); pts = [(140 + 280 * u / 20, 262 - 60 * math.sin(math.pi * u / 20)) for u in range(21)]
    line(L, pts, '#8a3624', 10); line(L, [(x, y - 26) for x, y in pts], '#9a3c26', 3)
    for k in range(1, 20, 3): x, y = pts[k]; line(L, [(x, y - 4), (x, y - 26)], '#7a2e1e', 2.4)
    for xx in (150, 410): fill(L, '#3a2a20', 364 + xx, rect=(xx - 4, 262, xx + 4, 300), scale=2)
    vol(img, L, (130, 170, 430, 300), .45, .2)
    glowc(img, 330, 300, 40, '#ffa850', .25, .3)
    for sd in (-1, 1): glowc(img, 270 + sd * 6, 290, 3, '#d8ffb0', .9)
    musya_l(img, 290, 204, 32, seed=366)
    paw(img); return fin(img, 'bridge')


def c_hotaru():
    img = card(); vgrad(img, [(0, '#05080e'), (.6, '#0c1418'), (1, '#080c0a')])
    cedars(img, 270, 8, 220, 300, 380, fogc='#1a2830', fog_amt=.7); mist(img, 200, 320, '#2a3a40', .4, 381)
    rr = random.Random(382); L = newl(img)
    for _ in range(420):
        x = rr.uniform(-10, 570); h = rr.uniform(20, 70); y = rr.uniform(300, 390)
        line(L, [(x, y), (x + rr.uniform(-8, 8), y - h)], mixc(H('#0e1a12'), H('#24402a'), rr.random()), rr.uniform(.8, 1.8))
    for _ in range(46):
        x, y = rr.uniform(20, 540), rr.uniform(80, 330); glowc(img, x, y, rr.uniform(8, 16), '#d8f070', .7); ell(img, (x - 1.4, y - 1.4, x + 1.4, y + 1.4), '#fffbd0')
    img.alpha_composite(L)
    for _ in range(14):
        x, y = rr.uniform(20, 540), rr.uniform(280, 370); glowc(img, x, y, 12, '#d8f070', .6); ell(img, (x - 1.4, y - 1.4, x + 1.4, y + 1.4), '#fffbd0')
    musya_l(img, 280, 366, 50, seed=383, look=-.4)
    paw(img); return fin(img, 'hotaru')


def c_cedar():
    img = card(); night(img, 400, moon=(470, 50))
    ground(img, 401, 310, '#1c2420'); L = newl(img)
    fill(L, '#4a3628', 402, poly=[(200, -10), (380, -10), (390, 300), (430, 350), (150, 350), (190, 300)], scale=3, stretch=(.25, 4), contrast=1.5)
    for k in range(5): line(L, [(212 + k * 38, -10), (210 + k * 40 + (k - 2) * 6, 340)], '#2a1e16', 2.2)
    vol(img, L, (150, -10, 430, 350), .7, .45)
    L = newl(img); pts = [(186 + 208 * u / 20, 176 + 18 * math.sin(math.pi * u / 20)) for u in range(21)]
    line(L, pts, '#c8b078', 13)
    for k in range(0, 21, 2): x, y = pts[k]; line(L, [(x - 5, y - 6), (x + 5, y + 6)], '#7a6438', 2)
    for k in (4, 10, 16):
        x, y = pts[k]; poly(L, [(x - 4, y + 6), (x + 4, y + 6), (x + 1, y + 16), (x + 7, y + 26), (x + 1, y + 36), (x - 4, y + 30), (x + 1, y + 22), (x - 4, y + 12)], '#f2eee2')
    vol(img, L, (180, 160, 400, 215), .4, .2)
    lay = newl(img); d = ImageDraw.Draw(lay); d.polygon([(px(440), 0), (px(480), 0), (px(300), px(380)), (px(240), px(380))], fill=(200, 215, 235, 26))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(8 * P.SS)))
    musya_l(img, 300, 364, 36, seed=404, look=.3)
    paw(img); return fin(img, 'cedar')


def c_hermit():
    img = card(); night(img, 420, fogc='#34444c'); ground(img, 421, 300, '#202620')
    x = 300; L = newl(img)
    fill(L, '#4a3a2a', 422, rect=(x - 80, 224, x + 80, 304), scale=3, stretch=(.3, 2), contrast=1.2)
    fill(L, '#151010', 423, rect=(x - 60, 246, x - 24, 304), scale=2)
    fill(L, '#7a6a44', 424, poly=[(x - 110, 232), (x, 140), (x + 110, 232), (x + 98, 240), (x, 158), (x - 98, 240)], scale=2, stretch=(.3, 3), contrast=1.4)
    fill(L, '#6a5a3a', 425, poly=[(x - 98, 240), (x, 158), (x + 98, 240), (x + 80, 226), (x, 160), (x - 80, 226)], scale=2, stretch=(.3, 3))
    vol(img, L, (x - 112, 138, x + 112, 306), .45, .25)
    glowc(img, x + 40, 266, 60, '#ffb050', .5); fill(img, '#f4c070', 426, rect=(x + 26, 254, x + 56, 280), scale=2, contrast=.4)
    line(img, [(x + 41, 254), (x + 41, 280)], '#3a2a1a', 1.4); line(img, [(x + 26, 267), (x + 56, 267)], '#3a2a1a', 1.4)
    for k in range(6): glowc(img, x + 40 + k * 6, 132 - k * 18, 14 + k * 3, '#8a8e90', .35)
    for k in range(5): P.stone(img, 200 - k * 18, 330 + k * 9, 12, 5, 430 + k, hexc('#4a4a44'), moss=False)
    musya_l(img, 160, 362, 48, seed=431)
    paw(img); return fin(img, 'hermit')


def mush(img, x, b, s, cap, seed, glow=False):
    if glow: glowc(img, x, b - 8 * s, 18 * s, '#b8f8b0', .5)
    L = newl(img); fill(L, '#e4d8bc', seed, rect=(x - 2.6 * s, b - 12 * s, x + 2.6 * s, b), scale=1, contrast=.5)
    fill(L, cap, seed + 1, poly=[(x - 11 * s, b - 10 * s), (x - 8 * s, b - 17 * s), (x, b - 20 * s), (x + 8 * s, b - 17 * s), (x + 11 * s, b - 10 * s)], scale=1.5, contrast=1.1)
    if not glow:
        for k in range(3): line(L, [(x - 5 * s + k * 5 * s, b - 15 * s), (x - 4 * s + k * 4 * s, b - 12 * s)], '#e8dcc4', .8 * s)
    vol(img, L, (x - 11 * s, b - 20 * s, x + 11 * s, b), .5, .3, spec=.2 if glow else 0)


def c_mush():
    img = card(); night(img, 440); fill(img, '#1e2a1a', 441, poly=[(0, 296), (560, 286), (560, 380), (0, 380)], scale=4, contrast=1.3)
    fill(img, '#2a2018', 442, poly=[(330, 300), (540, 280), (548, 300), (336, 318)], scale=3, stretch=(3, .5), contrast=1.3)
    rr = random.Random(443)
    for i in range(16): mush(img, rr.uniform(260, 540), rr.uniform(306, 360), rr.uniform(1.6, 2.6), rr.choice(['#7a4426', '#6a3a20', '#8a5030']), 450 + i * 3)
    for i in range(9): mush(img, rr.uniform(280, 520), rr.uniform(300, 350), rr.uniform(1, 1.6), '#cce8c4', 500 + i * 3, glow=True)
    foliage(img, [(60, 330, 70, 30), (520, 350, 60, 22)], [hexc(c) for c in ('#0c140c', '#142014', '#1e2e1a', '#2a3e24', '#3a5230')], 444, size=(2, 4))
    musya_l(img, 180, 362, 50, seed=445, side=1, look=.5)
    paw(img); return fin(img, 'mush')


def c_fox():
    img = card(); night(img, 460, top='#04060c'); ground(img, 461, 300, '#1a1c18')
    L = newl(img); blob(L, [(250, 380), (270, 250), (340, 200), (460, 190), (580, 230), (580, 380)], '#2a2a22', 462, scale=4, k=.4)
    img.alpha_composite(L); fill(img, '#040404', 463, ell=(340, 262, 430, 330), scale=2)
    for k in range(4): line(img, [(320 + k * 30, 254), (330 + k * 26, 236 - k * 4), (350 + k * 24, 220)], '#3a2e22', 3)
    for ex in (370, 396): glowc(img, ex, 296, 9, '#ffb040', .8); ell(img, (ex - 4, 293, ex + 4, 299), '#ffd070'); ell(img, (ex - 1, 293, ex + 1, 299), '#201000')
    for i, (x, y) in enumerate(((180, 150), (300, 120), (470, 150), (120, 230), (520, 250))):
        glowc(img, x, y, 22, '#6ab0ff', .8); fill(img, '#d8f0ff', 470 + i, ell=(x - 3, y - 5, x + 3, y + 3), scale=1, contrast=.2)
    musya_l(img, 200, 362, 48, seed=475, look=.6)
    paw(img); return fin(img, 'fox')


def c_lotus():
    img = card(); vgrad(img, [(0, '#060a16'), (.5, '#121a2a'), (1, '#0a0e14')])
    glowc(img, 420, 70, 100, '#c8d4e8', .35); fill(img, '#eef0f2', 480, ell=(404, 54, 436, 86), scale=2, contrast=.4)
    cedars(img, 200, 10, 120, 170, 481, fogc='#1c2634', fog_amt=.6, w=(50, 70))
    img = reflect(img, 200, dark=.45, tint='#1a2a3a', seed=482)
    rr = random.Random(483)
    for i in range(16):
        x, y = rr.uniform(160, 560), rr.uniform(220, 370); s = .6 + (y - 200) / 200; L = newl(img)
        fill(L, '#2e4a2c', 484 + i, ell=(x - 24 * s, y - 7 * s, x + 24 * s, y + 7 * s), scale=2, contrast=1.2)
        line(L, [(x, y), (x + 16 * s, y - 3 * s)], '#4a6a3a', 1); vol(img, L, (x - 24 * s, y - 7 * s, x + 24 * s, y + 7 * s), .5, .3)
    for i in range(6):
        x, y = rr.uniform(220, 540), rr.uniform(230, 350); s = .8 + (y - 200) / 160
        glowc(img, x, y - 8 * s, 16 * s, '#ffc0d0', .3)
        for a in (-60, -30, 0, 30, 60):
            r = math.radians(a - 90); poly(img, [(x, y), (x + math.cos(r - .25) * 9 * s, y + math.sin(r - .25) * 9 * s), (x + math.cos(r) * 15 * s, y + math.sin(r) * 15 * s), (x + math.cos(r + .25) * 9 * s, y + math.sin(r + .25) * 9 * s)], mixc(H('#e8a0b4'), H('#fbe0e8'), abs(a) / 80))
    fill(img, '#1a1e18', 490, poly=[(0, 300), (150, 310), (190, 380), (0, 380)], scale=4)
    musya_l(img, 90, 352, 48, seed=491, look=.5)
    paw(img); return fin(img, 'lotus')


def c_stairs():
    img = card(); night(img, 500, fogc='#3a4a54')
    L = newl(img)
    for k in range(22, -1, -1):
        t = k / 22; y = 380 - 270 * (1 - (1 - t) ** 1.7); w = 300 * (1 - t) + 40; hstep = 14 * (1 - t) + 3
        fill(L, mixc(H('#5a5c56'), H('#7c7e78'), .3), 501 + k, rect=(280 - w / 2, y - hstep, 280 + w / 2, y), scale=2, contrast=1.2)
        line(L, [(280 - w / 2, y - hstep), (280 + w / 2, y - hstep)], '#9a9c94', 1)
    img.alpha_composite(L)
    torii_front(img, 280, 112, 70, 60, '#7a3424', 530, fogc='#5a6a74', fog_amt=.7)
    P.set_size(CW, CH); img.alpha_composite(P.fog_layer(H('#6a7a84'), 60, 220, 1.2, 531, scale=120))
    mist(img, 220, 320, '#4a5a64', .35, 532)
    musya_l(img, 280, 372, 44, seed=533)
    paw(img); return fin(img, 'stairs')


def c_tea():
    img = card(); night(img, 540, moon=(90, 60)); ground(img, 541, 300, '#1c2420')
    L = newl(img)
    fill(L, '#55554e', 542, rect=(200, 280, 470, 304), scale=3, contrast=1.2)
    for k, (x, top) in enumerate(((220, 190), (300, 226), (380, 170), (450, 240))): fill(L, '#3a2a1e', 543 + k, poly=[(x - 6, 282), (x + 6, 282), (x + 6, top + 8), (x, top), (x - 6, top + 12)], scale=2, stretch=(.2, 3))
    fill(L, '#5a4a30', 548, poly=[(250, 250), (440, 200), (470, 222), (290, 282)], scale=2, stretch=(2, .3), contrast=1.4)
    vol(img, L, (200, 170, 470, 304), .4, .2)
    P.stone(img, 140, 318, 36, 20, 549, hexc('#5a5a54')); fill(img, '#0a1418', 550, ell=(118, 304, 162, 316), scale=1)
    line(img, [(184, 286), (150, 300)], '#7a8a4a', 4); glowc(img, 140, 310, 20, '#9ac0d8', .3)
    foliage(img, [(500, 300, 50, 30), (180, 250, 40, 24)], [hexc(c) for c in ('#0c140c', '#142014', '#1e2e1a', '#2a3e24', '#3a5230')], 551, size=(2, 4))
    mist(img, 260, 380, '#3a4650', .3, 552)
    musya_l(img, 360, 364, 46, seed=553, side=-1)
    paw(img); return fin(img, 'tea')


def c_neko():
    img = card(); night(img, 560, moon=(280, 60)); ground(img, 561, 300, '#1e241e')
    x, b = 340, 330; L = newl(img)
    blob(L, [(x - 90, b), (x - 92, b - 40), (x - 50, b - 76), (x + 20, b - 84), (x + 70, b - 70), (x + 92, b - 40), (x + 90, b)], '#8a8a82', 562, scale=4, k=.6)
    blob(L, [(x + 30, b - 70), (x + 34, b - 110), (x + 62, b - 124), (x + 94, b - 110), (x + 98, b - 76), (x + 70, b - 64)], '#8e8e86', 563, scale=3, k=.6)
    poly(L, [(x + 40, b - 106), (x + 44, b - 140), (x + 62, b - 118)], '#8a8a82'); poly(L, [(x + 76, b - 120), (x + 92, b - 142), (x + 96, b - 108)], '#8a8a82')
    line(L, [(x - 86, b - 6), (x - 110, b - 24), (x - 100, b - 50), (x - 76, b - 46)], '#7a7a72', 12)
    for sd in (-1, 1): line(L, [(x + 66 + sd * 12 - 6, b - 96), (x + 66 + sd * 12, b - 92), (x + 66 + sd * 12 + 6, b - 96)], '#3a3a34', 1.6)
    vol(img, L, (x - 112, b - 144, x + 100, b), .55, .3)
    fill(img, '#3a5a30', 564, ell=(x - 60, b - 80, x + 10, b - 66), scale=2)
    glowc(img, x, b - 90, 130, '#c8d4e8', .16)
    fill(img, '#8a9aa8', 565, poly=[(x + 110, b + 6), (x + 140, b - 2), (x + 150, b + 8), (x + 140, b + 14)], scale=1)
    musya_l(img, 150, 362, 50, seed=566)
    paw(img); return fin(img, 'neko')


def c_heart():
    img = card(); vgrad(img, [(0, '#0a0e22'), (.55, '#2a2a48'), (1, '#4a4058')])
    rr = random.Random(580)
    for _ in range(80): x, y = rr.uniform(0, 560), rr.uniform(0, 180); r = rr.uniform(.4, 1.3); ell(img, (x - r, y - r, x + r, y + r), (230, 236, 250, int(rr.uniform(90, 230))))
    glowc(img, 400, 90, 150, '#f0e0c0', .4); fill(img, '#f4f0e4', 581, ell=(370, 60, 430, 120), scale=3, contrast=.4)
    glowc(img, 280, 230, 160, '#ffd8a0', .35)
    torii_front(img, 280, 300, 250, 230, '#b4482e', 582)
    for k, (y, a) in enumerate(((250, .9), (290, 1.1), (330, 1.2))):
        P.set_size(CW, CH); img.alpha_composite(P.fog_layer(H(['#8a8aa8', '#b0aec0', '#d8d2dc'][k]), y - 40, y + 60, a, 583 + k, scale=110))
    fill(img, '#3a3a40', 590, poly=[(200, 380), (230, 352), (330, 348), (370, 380)], scale=3)
    musya_l(img, 280, 358, 44, seed=591)
    paw(img); return fin(img, 'heart')


CARDS = [('well', c_well), ('bamboo', c_bamboo), ('temple', c_temple), ('jizo', c_jizo), ('bridge', c_bridge), ('hotaru', c_hotaru), ('cedar', c_cedar), ('hermit', c_hermit),
         ('mush', c_mush), ('fox', c_fox), ('lotus', c_lotus), ('stairs', c_stairs), ('tea', c_tea), ('neko', c_neko), ('heart', c_heart)]


# ───────────── forest finds (category «Находки из леса») ─────────────
keep = T.keep


def i_mirror():
    img = canvas(120, 150); floor_shadow(img, 60, 144, 46)
    for sd in (-1, 1): line(img, [(60 + sd * 10, 112), (60 + sd * 34, 144)], '#2a1a12', 4)
    fill(img, '#3a2418', 1, rect=(30, 110, 90, 118), scale=2)
    blob(img, [(16, 62), (24, 26), (60, 10), (96, 26), (104, 62), (96, 98), (60, 114), (24, 98)], '#7a6436', 2, scale=3, k=.6, spec=.2)
    fill(img, '#c8c4a8', 3, ell=(30, 26, 90, 98), scale=3, contrast=.5); fill(img, '#4a8a7a', 4, ell=(40, 70, 70, 96), scale=2, contrast=1.3)
    volume(img, (30, 26, 90, 98), .5, .2, spec=.45); keep(img, 'fo_mirror')


def i_flute():
    img = canvas(200, 70); floor_shadow(img, 100, 62, 86)
    fill(img, '#c8a85a', 10, poly=[(14, 40), (186, 22), (190, 34), (18, 54)], scale=3, stretch=(3, .3), contrast=1.2, light=.3)
    for x in (52, 96, 140): line(img, [(x, 46 - (x - 14) * .1), (x + 1, 34 - (x - 14) * .1)], '#7a5a2a', 2)
    for x in (70, 84, 112, 126): ell(img, (x - 2.4, 40 - x * .1 - 2, x + 2.4, 40 - x * .1 + 2), '#2a1a0c')
    line(img, [(170, 30), (172, 50), (166, 62)], '#b8322a', 1.6); volume(img, (14, 20, 190, 56), .6, .4, spec=.2); keep(img, 'fo_flute')


def i_mokugyo():
    img = canvas(160, 130); floor_shadow(img, 80, 124, 66)
    fill(img, '#5a2a4a', 20, poly=[(16, 124), (24, 104), (136, 104), (144, 124)], scale=3)
    blob(img, [(26, 104), (22, 64), (46, 30), (80, 22), (114, 30), (138, 64), (134, 104)], '#8a3a1e', 21, scale=3, k=.6, spec=.3)
    line(img, [(36, 84), (124, 84)], '#2a0e06', 4); line(img, [(40, 80), (120, 80)], '#c87a4a', 1)
    for k in range(5): line(img, [(56 + k * 12, 50), (62 + k * 12, 44), (68 + k * 12, 50)], '#5a2010', 1.4)
    ell(img, (40, 54, 48, 62), '#2a0e06'); keep(img, 'fo_mokugyo')


def i_jizo():
    img = canvas(90, 140); floor_shadow(img, 45, 134, 34)
    fill(img, '#6a6a60', 30, rect=(16, 120, 74, 134), scale=2)
    blob(img, [(20, 122), (16, 80), (26, 56), (64, 56), (74, 80), (70, 122)], '#9a968a', 31, scale=2, k=.55)
    blob(img, [(26, 60), (24, 36), (36, 22), (54, 22), (66, 36), (64, 60), (45, 66)], '#a29e92', 32, scale=2, k=.55)
    fill(img, '#b02a22', 33, poly=[(20, 58), (70, 58), (62, 86), (45, 94), (28, 86)], scale=1.5)
    for sd in (-1, 1): line(img, [(45 + sd * 10, 42), (45 + sd * 4, 43)], '#3a3832', 1.4)
    keep(img, 'fo_jizo')


def i_hotaru():
    img = canvas(110, 140); floor_shadow(img, 55, 134, 42)
    glowc(img, 55, 86, 50, '#d8f070', .45)
    fill(img, '#6a5030', 40, rect=(16, 122, 94, 132), scale=2); fill(img, '#6a5030', 41, rect=(16, 44, 94, 52), scale=2)
    for x in range(20, 94, 8): line(img, [(x, 52), (x, 122)], '#a88a50', 1.6)
    line(img, [(30, 44), (40, 18), (70, 18), (80, 44)], '#8a6a3a', 2.4)
    rr = random.Random(42)
    for _ in range(7): x, y = rr.uniform(26, 84), rr.uniform(62, 114); glowc(img, x, y, 7, '#e8f880', .9); ell(img, (x - 1.4, y - 1.4, x + 1.4, y + 1.4), '#fffbd0')
    keep(img, 'fo_hotaru')


def i_chawan():
    img = canvas(120, 90); floor_shadow(img, 60, 84, 46)
    blob(img, [(12, 30), (108, 30), (100, 64), (80, 80), (40, 80), (20, 64)], '#2a2622', 50, scale=2, contrast=1.3, k=.6, spec=.25)
    fill(img, '#4a3a30', 51, ell=(12, 22, 108, 38), scale=2); fill(img, '#1a1612', 52, ell=(20, 25, 100, 36), scale=2)
    line(img, [(44, 34), (50, 48), (46, 58), (56, 72)], '#e8c060', 2); line(img, [(50, 48), (62, 52)], '#e8c060', 1.4)
    fill(img, '#3a3028', 53, rect=(46, 78, 74, 84), scale=1); keep(img, 'fo_chawan')


def i_kasa():
    img = canvas(160, 80); floor_shadow(img, 80, 74, 70)
    fill(img, '#b89a5a', 60, poly=[(6, 66), (80, 14), (154, 66), (80, 74)], scale=2, stretch=(.3, 2), contrast=1.4, light=.3)
    for k in range(9): line(img, [(80, 16), (14 + k * 16.5, 68)], '#8a7040', 1)
    line(img, [(30, 70), (60, 78), (86, 74)], '#6a3a2a', 1.6); volume(img, (6, 14, 154, 74), .5, .2); keep(img, 'fo_kasa')


def i_lotus():
    img = canvas(140, 110); floor_shadow(img, 70, 104, 56)
    blob(img, [(14, 72), (126, 72), (116, 98), (70, 106), (24, 98)], '#3a4a5a', 70, scale=2, k=.5, spec=.2)
    fill(img, '#2a4a5a', 71, ell=(16, 64, 124, 80), scale=2); fill(img, '#3a6a3a', 72, ell=(70, 62, 120, 76), scale=2)
    for a in (-70, -40, -12, 12, 40, 70):
        r = math.radians(a - 90); x, y = 62, 70
        poly(img, [(x, y), (x + math.cos(r - .3) * 18, y + math.sin(r - .3) * 18), (x + math.cos(r) * 40, y + math.sin(r) * 40), (x + math.cos(r + .3) * 18, y + math.sin(r + .3) * 18)], mixc(H('#e090a8'), H('#fbe4ec'), abs(a) / 80))
    ell(img, (56, 54, 68, 62), '#e8d060'); keep(img, 'fo_lotus')


def i_neko():
    img = canvas(100, 75); floor_shadow(img, 50, 70, 40)
    blob(img, [(10, 66), (12, 42), (34, 30), (64, 30), (88, 42), (90, 66), (50, 72)], '#8a8a84', 80, scale=2, contrast=1.1, k=.6)
    poly(img, [(24, 40), (28, 22), (40, 34)], '#8a8a84'); poly(img, [(76, 40), (72, 22), (60, 34)], '#8a8a84')
    line(img, [(32, 50), (38, 46), (44, 50)], '#2e2e2a', 1.6); line(img, [(56, 50), (62, 46), (68, 50)], '#2e2e2a', 1.6); ell(img, (47, 56, 53, 60), '#c08080')
    keep(img, 'fo_neko')


def i_sasabune():
    img = canvas(140, 60); floor_shadow(img, 70, 54, 56)
    fill(img, '#4a7a3a', 90, poly=[(4, 30), (40, 46), (100, 46), (136, 30), (110, 40), (30, 40)], scale=2, contrast=1.2)
    fill(img, '#5e9446', 91, poly=[(30, 40), (52, 16), (70, 38), (88, 16), (110, 40)], scale=2, contrast=1.1)
    line(img, [(52, 16), (52, 40)], '#2e5a24', 1); line(img, [(88, 16), (88, 40)], '#2e5a24', 1)
    volume(img, (4, 14, 136, 48), .5, .2, spec=.2); keep(img, 'fo_sasabune')


ITEMS = [i_mirror, i_flute, i_mokugyo, i_jizo, i_hotaru, i_chawan, i_kasa, i_lotus, i_neko, i_sasabune]


if __name__ == '__main__':
    only = sys.argv[2:] or ['map', 'cards', 'items']
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    meta = json.load(open(f'{HERE}/forest.json')) if os.path.exists(f'{HERE}/forest.json') else {}
    if 'map' in only:
        m = paper(); m = glyphs(m); m.convert('RGB').save(f'{OUT}/atlas_fomap.webp', 'WEBP', quality=80, method=6); m.convert('RGB').save(f'{HERE}/out/fo_map.jpg', quality=88)
        meta['fomap'] = [MW, MH]; print('map')
    if 'cards' in only:
        pics = []
        for name, fn in CARDS: pics.append((name, fn())); print('card', name)
        meta['cards'] = {}
        for ai, chunk in enumerate((pics[:8], pics[8:])):
            rows = (len(chunk) + 1) // 2; at = Image.new('RGB', (VW * 2, VH * rows), (12, 14, 13))
            for i, (name, im) in enumerate(chunk):
                x, y = (i % 2) * VW, (i // 2) * VH; at.paste(im.convert('RGB'), (x, y)); meta['cards'][name] = ['fov%d' % (ai + 1), x, y]
            at.save(f'{OUT}/atlas_fov{ai + 1}.webp', 'WEBP', quality=80, method=6); meta['fov%d' % (ai + 1)] = list(at.size)
        sheet = Image.new('RGB', (280 * 3, 190 * 5)); [sheet.paste(im.convert('RGB').resize((280, 190)), ((i % 3) * 280, (i // 3) * 190)) for i, (_, im) in enumerate(pics)]
        sheet.save(f'{HERE}/out/fo_cards_sheet.jpg', quality=85)
    if 'items' in only:
        T.SOUV.clear()
        for f in ITEMS: f()
        at, pos = T.pack(T.SOUV, 1000); at.save(f'{OUT}/atlas_foi.webp', 'WEBP', quality=86, alpha_quality=90, method=6)
        meta['foi'] = list(at.size); meta['items'] = {iid: list(pos[iid]) for iid, _, _ in T.SOUV}
        bg = Image.new('RGBA', at.size, (40, 44, 42, 255)); bg.alpha_composite(at); bg.convert('RGB').save(f'{HERE}/out/fo_items.jpg', quality=85)
    json.dump(meta, open(f'{HERE}/forest.json', 'w'), ensure_ascii=False)
    print(json.dumps(meta, ensure_ascii=False))
