#!/usr/bin/env python3
"""Night visitors lured by things (feat/visitors.js): eight folklore yōkai + their gifts.
karakasa-obake, bakezori, hitotsume-kozō, azuki-arai, kamaitachi, nuppeppō, yosuzume, mokumokuren → assets/mon/m_vs_*.webp;
nine gift things packed into assets/items/atlas_vs.webp (rect map printed as JSON, pasted into feat/visitors.js).
Same organic spline toolkit as story_art.py / guests_art.py.
Usage: visitors_art.py <assets dir>"""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
ASSETS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'assets')
sys.argv = [sys.argv[0], os.path.join(ASSETS, 'mon')]          # monsters.py / items.py read their out dir from argv[1]
import paint as P
from paint import hexc, mixc
import monsters as M
from monsters import canvas, px, soft, save
from story_art import cr, mask_of, shape, clipped, poly_s, folds
from guests_art import stroke, tube, fur_ticks
import items as I

SKIN = hexc('#dcc2a2')


def eye1(img, x, y, rx, ry, look=(0, 0), iris=(46, 30, 22, 255), rim=(110, 36, 34, 255), lid=0.0, lidcol=None, shade=90):
    """One big friendly yōkai eye: shaded socket, white, iris, a highlight, optional upper lid."""
    soft(img, lambda d: d.ellipse([px(x - rx * 1.18), px(y - ry * 1.22), px(x + rx * 1.18), px(y + ry * 1.28)], fill=(0, 0, 0, shade)), 4)
    ImageDraw.Draw(img).ellipse([px(x - rx), px(y - ry), px(x + rx), px(y + ry)], fill=(244, 238, 226, 255))
    m = mask_of(img, ell=(x - rx, y - ry, x + rx, y + ry), feather=.3); ir = ry * .6; ix, iy = x + look[0] * rx * .35, y + look[1] * ry * .3
    def fn(d, l):
        d.ellipse([px(ix - ir), px(iy - ir), px(ix + ir), px(iy + ir)], fill=iris)
        d.ellipse([px(ix - ir * .5), px(iy - ir * .5), px(ix + ir * .5), px(iy + ir * .5)], fill=(8, 6, 6, 255))
        d.ellipse([px(ix - ir * .62), px(iy - ir * .66), px(ix - ir * .12), px(iy - ir * .18)], fill=(255, 255, 255, 235))
        if lid: d.rectangle([px(x - rx - 2), px(y - ry - 2), px(x + rx + 2), px(y - ry + 2 * ry * lid)], fill=lidcol)
    clipped(img, m, fn)
    ImageDraw.Draw(img).ellipse([px(x - rx), px(y - ry), px(x + rx), px(y + ry)], outline=rim, width=px(2.2))
    if lid: stroke(ImageDraw.Draw(img), [(x - rx, y - ry + 2 * ry * lid + 2), (x, y - ry + 2 * ry * lid - 1), (x + rx, y - ry + 2 * ry * lid + 2)], (40, 24, 20, 255), 2.6)


def blush(img, pts, r=13, a=70):
    soft(img, lambda d: [d.ellipse([px(x - r), px(y - r * .6), px(x + r), px(y + r * .6)], fill=(226, 120, 120, a)) for x, y in pts], 4)


def ellpts(cx, cy, rx, ry, n=14):
    return [(cx + math.cos(a) * rx, cy + math.sin(a) * ry) for a in np.linspace(0, math.tau, n, endpoint=False)]


# ───────────── Karakasa-obake: an old umbrella on one leg in a one-tooth geta, one eye, a long tongue ─────────────
def karakasa():
    img = canvas(300, 460); cx = 150
    shape(img, hexc('#7a5a34'), 201, [(cx - 7, 270), (cx + 7, 270), (cx + 7, 330), (cx - 7, 330)], scale=4, stretch=(.3, 3), k=.4, rim=.2, smooth=False)
    shape(img, SKIN, 202, tube([(cx, 318), (cx - 5, 346), (cx - 10, 372), (cx - 4, 396), (cx, 416)], 14, 9), scale=6, contrast=.5, dk=.3, lt=.12, k=.5, rim=.35)
    shape(img, SKIN, 203, ell=(cx - 22, 406, cx + 20, 428), scale=4, contrast=.4, k=.4, rim=.3)
    I.fill(img, '#5a3a22', 204, poly=[(cx - 48, 424), (cx + 48, 424), (cx + 50, 438), (cx - 50, 438)], scale=4, stretch=(4, .4))
    I.fill(img, '#46301c', 205, poly=[(cx - 9, 438), (cx + 9, 438), (cx + 7, 456), (cx - 7, 456)], scale=3)
    stroke(ImageDraw.Draw(img), [(cx - 22, 424), (cx - 2, 410), (cx + 20, 424)], hexc('#b3302b'), 5)
    bot = [(cx + 124, 290), (cx + 104, 300), (cx + 82, 290), (cx + 60, 303), (cx + 36, 292), (cx + 12, 305), (cx - 12, 292), (cx - 36, 305), (cx - 60, 292), (cx - 82, 303), (cx - 104, 291), (cx - 124, 290)]
    cone = [(cx, 16), (cx + 30, 70), (cx + 64, 146), (cx + 98, 224)] + bot + [(cx - 98, 224), (cx - 64, 146), (cx - 30, 70)]
    mc = shape(img, hexc('#34466a'), 206, cone, scale=10, stretch=(.4, 2), contrast=1.1, dk=.5, lt=.18, k=.55, rim=.3)
    xs = list(range(cx - 120, cx + 121, 24))
    def ribs(d, l):
        for i, (a, b) in enumerate(zip(xs, xs[1:])):
            d.polygon([(px(cx), px(16)), (px(a), px(300)), (px(b), px(300))], fill=(0, 0, 0, 46) if i % 2 else (255, 255, 255, 16))
        for x in xs: d.line([(px(cx), px(16)), (px(x), px(302))], fill=(16, 20, 34, 150), width=px(1.6))
        d.line([(px(x), px(y)) for x, y in cr([(cx - 90, 146), (cx, 164), (cx + 90, 146)], 8, False)], fill=(228, 218, 192, 235), width=px(15))
        d.line([(px(x), px(y)) for x, y in cr([(cx - 130, 272), (cx, 284), (cx + 130, 272)], 8, False)], fill=(206, 170, 90, 200), width=px(4))
    clipped(img, mc, ribs)
    folds(img, mc, [[(cx - 40, 200), (cx - 60, 280)], [(cx + 46, 210), (cx + 70, 286)]], (0, 0, 0, 60), 4)
    I.fill(img, '#2a1c14', 207, poly=[(cx - 8, 4), (cx + 8, 4), (cx + 9, 24), (cx - 9, 24)], scale=3)
    eye1(img, cx, 204, 33, 27, look=(-.2, .1), lid=.18, lidcol=hexc('#2e3e5e'))
    d = ImageDraw.Draw(img)
    poly_s(d, [(cx - 40, 242), (cx, 254), (cx + 40, 242), (cx + 30, 262), (cx, 270), (cx - 30, 262)], (44, 12, 14, 255), 6)
    for k in (-1, 1): d.polygon([(px(cx + k * 26), px(246)), (px(cx + k * 18), px(249)), (px(cx + k * 22), px(258))], fill=(236, 228, 206, 255))
    mt = shape(img, hexc('#d9606e'), 208, tube([(cx + 2, 256), (cx + 8, 290), (cx + 20, 322), (cx + 42, 344), (cx + 66, 340), (cx + 74, 326)], 12, 7), scale=5, contrast=.7, dk=.3, lt=.25, k=.4, rim=.3, spec=.2)
    clipped(img, mt, lambda dd, l: dd.line([(px(x), px(y)) for x, y in cr([(cx + 3, 262), (cx + 10, 296), (cx + 24, 326), (cx + 46, 342), (cx + 68, 334)], 8, False)], fill=(160, 50, 62, 220), width=px(2.2)))
    save(img, 'm_vs_karakasa')


# ───────────── Bakezori: a worn straw sandal with one eye, two teeth, twig arms ─────────────
def bakezori():
    img = canvas(280, 370); cx = 140; straw, straw_d = hexc('#c9a55a'), hexc('#8e7036')
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):   # twisted-straw legs and arms
        stroke(d, [(cx + sx * 26, 296), (cx + sx * 30, 326), (cx + sx * 26, 350)], straw_d, 8)
        shape(img, straw_d, 301 + sx, ell=(cx + sx * 28 - 17, 344, cx + sx * 28 + 17, 360), scale=4, k=.4, rim=.3)
        d = ImageDraw.Draw(img)
        arm = [(cx + sx * 64, 190), (cx + sx * 92, 176 if sx < 0 else 206), (cx + sx * 112, 150 if sx < 0 else 222)]
        stroke(d, arm, straw_d, 6)
        ex, ey = arm[-1]
        for a in (-.6, 0, .6): stroke(d, [(ex, ey), (ex + sx * math.cos(a) * 12, ey + math.sin(a) * 12 - (8 if sx < 0 else -4))], straw_d, 3)
    sole = [(cx, 36), (cx + 50, 48), (cx + 72, 96), (cx + 74, 160), (cx + 64, 204), (cx + 70, 252), (cx + 60, 290), (cx + 30, 306), (cx, 310), (cx - 30, 306), (cx - 60, 290), (cx - 70, 252), (cx - 64, 204), (cx - 74, 160), (cx - 72, 96), (cx - 50, 48)]
    ms = shape(img, straw, 303, sole, scale=6, stretch=(4, .4), contrast=1.3, dk=.45, lt=.2, k=.5, rim=.35)
    def weave(d, l):
        for y in range(44, 312, 11): d.line([(px(cx - 80), px(y)), (px(cx + 80), px(y + 2))], fill=(110, 84, 36, 170), width=px(1.8))
        for x in (cx - 30, cx, cx + 30): d.line([(px(x), px(40)), (px(x + 2), px(310))], fill=(120, 92, 40, 90), width=px(1.2))
    clipped(img, ms, weave)
    rnd = random.Random(304); d = ImageDraw.Draw(img)
    for _ in range(40):   # frayed straw sticking out of the rim
        a = rnd.uniform(0, math.tau); bx, by = cx + math.cos(a) * 70, 172 + math.sin(a) * 134
        d.line([(px(bx), px(by)), (px(bx + math.cos(a) * rnd.uniform(6, 14)), px(by + math.sin(a) * rnd.uniform(6, 14)))], fill=(176, 146, 80, 220), width=px(1.4))
    # the red hanao strap sits on it like a headband
    for sx in (-1, 1):
        mh = shape(img, hexc('#a8322a'), 305 + sx, tube([(cx, 62), (cx + sx * 34, 88), (cx + sx * 60, 118), (cx + sx * 74, 128)], 8, 7), scale=4, contrast=.8, k=.5, rim=.3)
        clipped(img, mh, lambda dd, l, s=sx: [dd.line([(px(cx + s * t), px(62 + t * .9 - 6)), (px(cx + s * (t + 6)), px(62 + t * .9 + 6))], fill=(236, 200, 180, 150), width=px(1.2)) for t in range(0, 76, 9)])
    shape(img, hexc('#8e2420'), 307, ell=(cx - 11, 52, cx + 11, 72), scale=3, k=.5, rim=.3, spec=.3)
    eye1(img, cx, 162, 30, 26, look=(.15, .1), rim=(90, 60, 20, 255))
    d = ImageDraw.Draw(img)
    poly_s(d, [(cx - 30, 216), (cx, 224), (cx + 30, 216), (cx + 20, 238), (cx, 244), (cx - 20, 238)], (48, 22, 12, 255), 6)
    for x in (cx - 10, cx + 3): d.rounded_rectangle([px(x), px(219), px(x + 8), px(231)], px(2), fill=(240, 232, 212, 255))
    blush(img, [(cx - 44, 204), (cx + 44, 204)], 11, 60)
    save(img, 'm_vs_bakezori')


# ───────────── Hitotsume-kozō: a bald little monk boy with one eye, carrying tofu ─────────────
def kozo():
    img = canvas(300, 500); cx = 150; skin = hexc('#e8dac4')
    for sx in (-1, 1):
        shape(img, skin, 401 + sx, [(cx + sx * 12, 428), (cx + sx * 34, 428), (cx + sx * 32, 470), (cx + sx * 14, 470)], scale=5, contrast=.4, k=.4, rim=.3, smooth=False)
        shape(img, hexc('#b89a5c'), 403 + sx, ell=(cx + sx * 24 - 21, 462, cx + sx * 24 + 21, 486), scale=4, stretch=(3, .5), contrast=1.2, k=.4, rim=.3)
        stroke(ImageDraw.Draw(img), [(cx + sx * 14, 466), (cx + sx * 24, 458), (cx + sx * 34, 466)], hexc('#6a4a2a'), 3)
    body = [(cx - 42, 236), (cx, 228), (cx + 42, 236), (cx + 62, 300), (cx + 72, 380), (cx + 68, 434), (cx, 442), (cx - 68, 434), (cx - 72, 380), (cx - 62, 300)]
    mb = shape(img, hexc('#34466e'), 405, body, scale=12, stretch=(1, 2), contrast=1.1, k=.45, rim=.35)
    rnd = random.Random(406)
    def kasuri(d, l):
        for _ in range(46):
            x, y = rnd.uniform(cx - 80, cx + 80), rnd.uniform(232, 442)
            d.line([(px(x - 4), px(y)), (px(x + 4), px(y))], fill=(214, 220, 230, 190), width=px(2)); d.line([(px(x), px(y - 4)), (px(x), px(y + 4))], fill=(214, 220, 230, 190), width=px(2))
    clipped(img, mb, kasuri)
    folds(img, mb, [[(cx - 30, 360), (cx - 34, 440)], [(cx + 28, 360), (cx + 32, 440)]])
    d = ImageDraw.Draw(img); poly_s(d, [(cx - 22, 236), (cx, 282), (cx + 22, 236), (cx + 12, 236), (cx, 268), (cx - 12, 236)], (236, 230, 216, 255), 4)
    shape(img, hexc('#8e2a24'), 407, [(cx - 66, 318), (cx + 66, 318), (cx + 68, 338), (cx - 68, 338)], scale=5, k=.3, rim=.1, smooth=False)
    for sx in (-1, 1):
        shape(img, hexc('#2e3e62'), 408 + sx, [(cx + sx * 38, 242), (cx + sx * 76, 262), (cx + sx * 92, 312), (cx + sx * 86, 346), (cx + sx * 50, 352), (cx + sx * 42, 300)], scale=10, k=.5, rim=.35)
    I.fill(img, '#7a5230', 410, poly=[(cx - 64, 350), (cx + 64, 350), (cx + 58, 366), (cx - 58, 366)], scale=4, stretch=(4, .5))
    for pts, col in (([(cx - 30, 318), (cx + 12, 318), (cx + 28, 306), (cx - 14, 306)], '#f4f0e4'), ([(cx - 30, 318), (cx + 12, 318), (cx + 12, 350), (cx - 30, 350)], '#dcd6c4'), ([(cx + 12, 318), (cx + 28, 306), (cx + 28, 338), (cx + 12, 350)], '#c4bea9')):
        I.fill(img, col, 411, poly=pts, scale=3, contrast=.4, dark=.15, light=.08)
    poly_s(ImageDraw.Draw(img), [(cx + 30, 350), (cx + 44, 336), (cx + 58, 342), (cx + 50, 354)], (170, 54, 30, 255), 4)   # a maple leaf on the tray
    for sx in (-1, 1): shape(img, skin, 412 + sx, ell=(cx + sx * 56 - 13, 340, cx + sx * 56 + 13, 364), scale=4, contrast=.4, k=.4, rim=.3)
    for sx in (-1, 1): shape(img, skin, 414 + sx, ell=(cx + sx * 68 - 14, 150, cx + sx * 68 + 14, 186), scale=4, contrast=.4, k=.4, rim=.3)
    mh = shape(img, skin, 416, ell=(cx - 68, 94, cx + 68, 236), scale=10, contrast=.35, dk=.2, lt=.1, k=.4, rim=.3)
    clipped(img, mh, lambda dd, l: dd.ellipse([px(cx - 72), px(70), px(cx + 72), px(150)], fill=(120, 136, 150, 70)))   # the shaved scalp
    soft(img, lambda dd: dd.arc([px(cx - 40), px(104), px(cx + 10), px(140)], 200, 300, fill=(255, 255, 255, 90), width=px(5)), 3)
    eye1(img, cx, 170, 31, 27, look=(0, .15), iris=(58, 40, 30, 255))
    d = ImageDraw.Draw(img); d.arc([px(cx - 36), px(126), px(cx + 36), px(154)], 205, 335, fill=(60, 44, 36, 255), width=px(4))
    poly_s(d, [(cx - 13, 208), (cx + 13, 208), (cx + 8, 218), (cx - 8, 218)], (70, 20, 20, 255), 3)
    shape(img, hexc('#d9606e'), 417, tube([(cx, 212), (cx + 2, 224), (cx + 6, 234)], 7, 5), scale=3, k=.4, rim=.2, spec=.2)
    blush(img, [(cx - 44, 204), (cx + 44, 204)], 13, 75)
    save(img, 'm_vs_kozo')


# ───────────── Azuki-arai: a hunched old man washing red beans in a sieve ─────────────
def azuki():
    img = canvas(380, 400); cx = 190; skin, skin_d = hexc('#cbb592'), hexc('#a88e6a')
    for sx in (-1, 1):
        shape(img, skin_d, 501 + sx, [(cx + sx * 36, 372), (cx + sx * 98, 366), (cx + sx * 112, 384), (cx + sx * 98, 394), (cx + sx * 34, 394)], scale=5, k=.4, rim=.3)
        d = ImageDraw.Draw(img)
        for t in range(4): d.line([(px(cx + sx * (84 + t * 7)), px(378)), (px(cx + sx * (88 + t * 7)), px(392))], fill=(90, 70, 50, 200), width=px(1.2))
    body = [(cx - 58, 150), (cx, 140), (cx + 58, 150), (cx + 100, 210), (cx + 118, 290), (cx + 108, 350), (cx + 60, 374), (cx, 378), (cx - 60, 374), (cx - 108, 350), (cx - 118, 290), (cx - 100, 210)]
    mb = shape(img, hexc('#6c5c46'), 503, body, scale=12, stretch=(1, 2), contrast=1.2, k=.5, rim=.35)
    clipped(img, mb, lambda d, l: [poly_s(d, [(cx - 90, 200), (cx - 50, 196), (cx - 46, 240), (cx - 92, 244)], (84, 72, 54, 255), 2),
                                   poly_s(d, [(cx + 40, 210), (cx + 86, 216), (cx + 80, 250), (cx + 42, 246)], (92, 80, 60, 255), 2),
                                   [d.line([(px(cx - 92 + k * 8), px(198)), (px(cx - 90 + k * 8), px(204))], fill=(200, 190, 160, 200), width=px(1.2)) for k in range(6)]])
    folds(img, mb, [[(cx - 20, 170), (cx - 30, 260)], [(cx + 24, 170), (cx + 36, 250)]])
    for sx in (-1, 1): shape(img, skin, 504 + sx, ell=(cx + sx * 92 - 34, 238, cx + sx * 92 + 34, 300), scale=6, contrast=.5, k=.5, rim=.4)
    for sx in (-1, 1): shape(img, skin, 506 + sx, tube([(cx + sx * 66, 176), (cx + sx * 104, 222), (cx + sx * 104, 272), (cx + sx * 92, 308)], 15, 10), scale=6, contrast=.5, k=.5, rim=.35)
    I.fill(img, '#b8995a', 508, ell=(cx - 104, 290, cx + 104, 352), scale=4, stretch=(3, .5), contrast=1.2)
    I.fill(img, '#8a6e3c', 509, ell=(cx - 90, 296, cx + 90, 334), scale=4, contrast=1.1)
    rnd = random.Random(510); d = ImageDraw.Draw(img)
    for _ in range(170):   # the bean mound
        a = rnd.uniform(0, math.tau); r = rnd.random() ** .7; x = cx + math.cos(a) * 82 * r; y = 312 + math.sin(a) * 16 * r - (1 - r) * 16
        c = rnd.choice([(122, 30, 26), (140, 38, 30), (104, 24, 22), (150, 48, 36)])
        d.ellipse([px(x - 5), px(y - 3.6), px(x + 5), px(y + 3.6)], fill=c + (255,)); d.ellipse([px(x - 3), px(y - 3), px(x - .5), px(y - 1)], fill=(230, 170, 150, 200))
    m = mask_of(img, ell=(cx - 104, 290, cx + 104, 352), feather=0)
    clipped(img, m, lambda d, l: [d.line([(px(cx - 110 + k * 12), px(330)), (px(cx - 100 + k * 12), px(356))], fill=(90, 70, 36, 170), width=px(1.4)) for k in range(20)])
    for sx in (-1, 1): shape(img, skin, 511 + sx, ell=(cx + sx * 96 - 15, 304, cx + sx * 96 + 15, 330), scale=4, contrast=.4, k=.4, rim=.3)
    d = ImageDraw.Draw(img)
    for x, y in ((cx - 40, 362), (cx + 10, 372), (cx + 52, 360)): poly_s(d, [(x, y - 7), (x + 4, y + 2), (x, y + 6), (x - 4, y + 2)], (180, 214, 230, 210), 3)
    for sx in (-1, 1): shape(img, skin_d, 513 + sx, ell=(cx + sx * 64 - 20, 86, cx + sx * 64 + 20, 136), scale=4, k=.4, rim=.3)
    mh = shape(img, skin, 515, ell=(cx - 62, 44, cx + 62, 178), scale=8, contrast=.6, k=.5, rim=.35)
    clipped(img, mh, lambda d, l: [d.arc([px(cx - 30), px(y), px(cx + 30), px(y + 16)], 200, 340, fill=(130, 104, 76, 180), width=px(1.6)) for y in (64, 74)])
    for sx in (-1, 1):   # white wisps of hair at the temples
        rh = random.Random(516 + sx); d = ImageDraw.Draw(img)
        for _ in range(26):
            x0, y0 = cx + sx * rh.uniform(46, 62), rh.uniform(88, 140)
            d.line([(px(x0), px(y0)), (px(x0 + sx * rh.uniform(8, 20)), px(y0 + rh.uniform(10, 26)))], fill=(226, 222, 212, 220), width=px(1.3))
    for sx in (-1, 1):
        ex = cx + sx * 25
        d.ellipse([px(ex - 15), px(92), px(ex + 15), px(120)], fill=hexc('#efe6c0')); d.ellipse([px(ex - 15), px(92), px(ex + 15), px(120)], outline=(80, 50, 30, 255), width=px(2))
        d.ellipse([px(ex - 5), px(100), px(ex + 5), px(112)], fill=(20, 12, 8, 255)); d.ellipse([px(ex - 4), px(101), px(ex - 1), px(104)], fill=(255, 255, 255, 220))
        stroke(d, [(ex - 16, 86), (ex, 80), (ex + 16, 86)], (220, 216, 206, 255), 5)
    shape(img, skin_d, 518, ell=(cx - 11, 110, cx + 11, 134), scale=3, k=.5, rim=.3, spec=.2)
    d = ImageDraw.Draw(img)
    poly_s(d, [(cx - 36, 140), (cx, 148), (cx + 36, 140), (cx + 26, 158), (cx, 164), (cx - 26, 158)], (46, 16, 12, 255), 6)
    for x in (cx - 18, cx + 4, cx + 16): d.polygon([(px(x), px(143)), (px(x + 8), px(144)), (px(x + 4), px(153))], fill=(236, 226, 196, 255))
    save(img, 'm_vs_azuki')


# ───────────── Kamaitachi: three weasels riding a whirlwind (one topples, one cuts, one heals) ─────────────
def weasel(img, cx, cy, ang, face, sc, seed, blade=False, shell=False):
    ca, sa = math.cos(ang), math.sin(ang)
    def T(x, y): x *= face * sc; y *= sc; return (cx + x * ca - y * sa, cy + x * sa + y * ca)
    fur, belly, dark = hexc('#a8733e'), hexc('#efe2c6'), (40, 24, 14, 255)
    shape(img, fur, seed, tube([T(-58, 2), T(-86, -12), T(-112, -8), T(-134, 8)], 9 * sc, 5 * sc), scale=4, k=.5, rim=.3)
    shape(img, hexc('#5a3a1e'), seed + 1, tube([T(-120, -4), T(-134, 8)], 6 * sc, 4 * sc), scale=3, k=.4, rim=.2)
    d = ImageDraw.Draw(img)
    for a, b in (((-44, 12), (-54, 32)), ((-30, 14), (-26, 34)), ((12, 6), (20, 26))): stroke(d, [T(*a), T(*b)], hexc('#7a5028'), 6 * sc, 4)
    mb = shape(img, fur, seed + 2, tube([T(-62, 4), T(-30, 0), T(0, -4), T(26, -12)], 19 * sc, 15 * sc), scale=5, k=.55, rim=.35)
    fur_ticks(img, mb, seed + 3, (cx - 90 * sc, cy - 50 * sc, cx + 90 * sc, cy + 50 * sc), 50, (70, 44, 20, 110), (4, 8))
    shape(img, belly, seed + 4, tube([T(-48, 13), T(-20, 12), T(8, 7), T(26, 0)], 7 * sc, 6 * sc), scale=4, contrast=.4, k=.3, rim=.2)
    if blade:   # the middle one has sickles for forepaws
        for dx in (0, 14):
            poly_s(ImageDraw.Draw(img), [T(18 + dx, 8), T(40 + dx, 26), T(66 + dx, 22), T(76 + dx, 4), T(64 + dx, 16), T(42 + dx, 16)], (206, 210, 214, 255), 5)
            stroke(ImageDraw.Draw(img), [T(40 + dx, 26), T(66 + dx, 22), T(76 + dx, 4)], (70, 74, 80, 255), 1.6 * sc, 5)
    else: stroke(ImageDraw.Draw(img), [T(22, 2), T(40, 18)], hexc('#7a5028'), 6 * sc, 4)
    for ex, ey in ((34, -36), (48, -40)):
        x, y = T(ex, ey); r = 7 * sc; ImageDraw.Draw(img).ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=hexc('#8a5a30'))
    shape(img, fur, seed + 5, [T(24, -30), T(44, -38), T(64, -30), T(76, -16), T(64, -4), T(42, -2), T(26, -12)], scale=4, k=.55, rim=.3)
    shape(img, belly, seed + 6, [T(44, -14), T(64, -12), T(74, -10), T(56, -2), T(40, -4)], scale=3, contrast=.3, k=.3, rim=.1)
    d = ImageDraw.Draw(img)
    x, y = T(52, -22); r = 4.4 * sc; d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=(14, 8, 6, 255)); d.ellipse([px(x - r * .6), px(y - r * .7), px(x - r * .1), px(y - r * .2)], fill=(255, 255, 255, 230))
    x, y = T(76, -16); r = 3 * sc; d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=(60, 30, 30, 255))
    if shell:   # the third one carries the healing salve in a clam shell
        x, y = T(78, 8); r = 13 * sc
        shape(img, hexc('#e8d2bc'), seed + 7, [(x - r, y), (x - r * .7, y - r * .9), (x, y - r * 1.15), (x + r * .7, y - r * .9), (x + r, y), (x, y + r * .25)], scale=3, k=.4, rim=.2)
        shape(img, hexc('#cfe4c8'), seed + 8, ell=(x - r * .7, y - r * .5, x + r * .7, y + r * .1), scale=3, contrast=.3, k=.3, rim=.1, spec=.3)


def kamaitachi():
    img = canvas(400, 440); cx = 200; rnd = random.Random(601)
    def wind(front):
        l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l)
        for i in range(70):
            y = rnd.uniform(56, 430); u = (y - 56) / 374; r = 22 + 150 * (1 - u) ** .8; sx = cx + math.sin(u * 5) * 18
            st = rnd.uniform(0, 150) if front else rnd.uniform(180, 330); ext = rnd.uniform(40, 120)
            d.arc([px(sx - r), px(y - r * .22), px(sx + r), px(y + r * .22)], st, st + ext, fill=(222, 228, 232, rnd.randint(60, 140)), width=px(rnd.uniform(1.5, 4)))
        img.alpha_composite(l.filter(ImageFilter.GaussianBlur(.8 * M.S)))
    wind(False)
    for _ in range(9):   # leaves caught in the gust
        x, y, a = rnd.uniform(60, 340), rnd.uniform(60, 380), rnd.uniform(0, math.tau); c = rnd.choice([(170, 70, 40), (190, 140, 60), (110, 130, 60)])
        pts = [(x + math.cos(a) * 10, y + math.sin(a) * 10), (x + math.cos(a + 1.9) * 5, y + math.sin(a + 1.9) * 5), (x - math.cos(a) * 10, y - math.sin(a) * 10), (x + math.cos(a - 1.9) * 5, y + math.sin(a - 1.9) * 5)]
        poly_s(ImageDraw.Draw(img), pts, c + (230,), 4)
    weasel(img, 248, 116, -.25, -1, 1.0, 610)
    weasel(img, 150, 232, .12, 1, 1.05, 620, blade=True)
    weasel(img, 236, 342, -.08, -1, .92, 630, shell=True)
    wind(True)
    save(img, 'm_vs_kamaitachi')


# ───────────── Nuppeppō: a shy, soft lump that walks at night (here: mochi-cute) ─────────────
def nuppeppo():
    img = canvas(340, 340); cx = 170; flesh = hexc('#e6c2ac')
    for sx in (-1, 1): shape(img, hexc('#d6ae98'), 701 + sx, ell=(cx + sx * 56 - 28, 296, cx + sx * 56 + 28, 330), scale=5, contrast=.5, k=.4, rim=.3)
    blob = [(cx, 40), (cx + 58, 54), (cx + 102, 100), (cx + 126, 170), (cx + 138, 240), (cx + 124, 290), (cx + 80, 316), (cx, 322), (cx - 80, 316), (cx - 124, 290), (cx - 138, 240), (cx - 126, 170), (cx - 102, 100), (cx - 58, 54)]
    mb = shape(img, flesh, 703, blob, scale=12, contrast=.55, dk=.3, lt=.14, k=.55, rim=.4, spec=.28)
    folds(img, mb, [[(cx - 110, 200), (cx - 70, 222), (cx - 40, 214)], [(cx + 110, 196), (cx + 74, 220), (cx + 44, 212)], [(cx - 90, 270), (cx, 290), (cx + 90, 270)], [(cx - 50, 110), (cx, 100), (cx + 50, 110)]], (120, 60, 50, 90), 4)
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):   # sleepy closed eyes with a drooping fold above
        ex = cx + sx * 36
        d.arc([px(ex - 16), px(138), px(ex + 16), px(162)], 20, 160, fill=(80, 40, 36, 255), width=px(3.4))
        stroke(d, [(ex - 20, 132), (ex, 126), (ex + 20, 132)], (170, 110, 96, 200), 3)
    d.ellipse([px(cx - 7), px(178), px(cx + 7), px(190)], fill=(110, 46, 44, 255))
    blush(img, [(cx - 66, 170), (cx + 66, 170)], 17, 90)
    for sx in (-1, 1):   # tiny arms, fingertips touching — very shy
        shape(img, flesh, 704 + sx, tube([(cx + sx * 76, 212), (cx + sx * 44, 234), (cx + sx * 12, 238)], 15, 11), scale=5, contrast=.4, k=.5, rim=.3)
    poly_s(ImageDraw.Draw(img), [(cx + 104, 72), (cx + 112, 92), (cx + 104, 102), (cx + 96, 92)], (190, 222, 236, 230), 4)   # a nervous sweat drop
    save(img, 'm_vs_nuppeppo')


# ───────────── Yosuzume: the night sparrow whose chirping is heard on mountain roads ─────────────
def yosuzume():
    img = canvas(270, 270); brown, cap = hexc('#86583a'), hexc('#7a3e22')
    soft(img, lambda d: d.ellipse([px(26), px(30), px(250), px(250)], fill=(190, 206, 236, 46)), 22)   # a faint moonlit aura
    d = ImageDraw.Draw(img)
    for x in (116, 150):
        stroke(d, [(x, 224), (x + 2, 250)], hexc('#8a6a58'), 4)
        for a in (-.7, 0, .7): stroke(d, [(x + 2, 250), (x + 2 + math.sin(a) * 12, 256)], hexc('#8a6a58'), 3)
    tail = [(196, 150), (250, 104), (262, 118), (214, 178)]
    shape(img, hexc('#5a3a26'), 801, tail, scale=4, stretch=(3, .5), k=.4, rim=.2)
    mb = shape(img, brown, 802, ell=(56, 92, 230, 236), scale=6, contrast=1.1, k=.55, rim=.35)
    clipped(img, mb, lambda d, l: d.ellipse([px(40), px(150), px(200), px(260)], fill=hexc('#ddd4c4')), .95)
    fur_ticks(img, mb, 803, (140, 100, 230, 200), 70, (46, 28, 18, 180), (5, 11), .6)
    mw = shape(img, hexc('#6a4228'), 804, [(130, 132), (190, 118), (232, 150), (220, 190), (160, 196), (128, 170)], scale=5, k=.5, rim=.3)
    clipped(img, mw, lambda d, l: [d.line([(px(140 + k * 20), px(150)), (px(150 + k * 20), px(188))], fill=(232, 222, 200, 220), width=px(3)) for k in range(4)])
    mh = shape(img, hexc('#e8e2d6'), 805, ell=(50, 40, 170, 150), scale=6, contrast=.4, dk=.2, k=.5, rim=.3)
    clipped(img, mh, lambda d, l: d.ellipse([px(46), px(22), px(176), px(92)], fill=cap))
    clipped(img, mh, lambda d, l: d.ellipse([px(106), px(94), px(126), px(110)], fill=(30, 24, 22, 255)))   # the black cheek spot
    shape(img, (28, 22, 20, 255), 806, [(62, 112), (80, 116), (84, 132), (70, 138), (60, 126)], scale=3, k=.2, rim=.1)
    d = ImageDraw.Draw(img)
    poly_s(d, [(58, 94), (30, 104), (60, 112)], (44, 36, 34, 255), 3)
    d.ellipse([px(74), px(76), px(94), px(96)], fill=(10, 8, 10, 255)); d.ellipse([px(78), px(79), px(85), px(86)], fill=(236, 240, 255, 240))
    soft(img, lambda dd: dd.ellipse([px(70), px(72), px(98), px(100)], fill=(200, 214, 255, 50)), 3)
    save(img, 'm_vs_yosuzume')


# ───────────── Mokumokuren: a torn shōji whose panes have eyes (Toriyama Sekien) ─────────────
EYES = [(92, 88, 22, 15, (.3, .1)), (190, 90, 17, 12, (-.2, .2)), (286, 96, 24, 16, (-.4, .1)), (130, 190, 15, 11, (.4, 0)), (256, 200, 26, 18, (-.1, .2)),
        (94, 300, 20, 14, (.2, -.1)), (190, 296, 14, 10, (0, .3)), (290, 304, 19, 13, (-.3, 0)), (178, 396, 23, 16, (.1, -.2))]


def mokumokuren():
    img = canvas(380, 480); x0, y0, x1, y1 = 24, 18, 356, 466; paper = hexc('#d8ccae')
    mp = shape(img, paper, 901, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], scale=16, contrast=.9, dk=.25, lt=.1, k=.35, rim=.15, smooth=False, feather=0)
    rnd = random.Random(902)
    soft(img, lambda d: [d.ellipse([px(x - r), px(y - r * .7), px(x + r), px(y + r * .7)], fill=(150, 120, 70, 50)) for x, y, r in [(rnd.uniform(60, 320), rnd.uniform(60, 420), rnd.uniform(14, 36)) for _ in range(9)]], 6)
    d = ImageDraw.Draw(img)
    for tx, ty in ((226, 244), (70, 400)):   # torn panes: darkness behind, curled paper edges
        pts = [(tx + math.cos(a) * rnd.uniform(14, 26), ty + math.sin(a) * rnd.uniform(12, 22)) for a in np.linspace(0, math.tau, 11, endpoint=False)]
        d.polygon([(px(x), px(y)) for x, y in pts], fill=(24, 20, 18, 255))
        for x, y in pts[::2]: d.line([(px(x), px(y)), (px(x + (x - tx) * .25), px(y + (y - ty) * .25))], fill=(236, 226, 200, 255), width=px(2))
    for x, y, rx, ry, lk in EYES: eye1(img, x, y, rx, ry, look=lk, iris=(54, 36, 26, 255), rim=(90, 40, 34, 255), lid=.2, lidcol=hexc('#cfc2a2'), shade=70)
    wood = '#4a3624'
    for xx in (133, 245): I.fill(img, wood, 903 + xx, rect=(xx - 4, y0, xx + 4, y1), scale=4, stretch=(.3, 4))
    for yy in (142, 246, 350): I.fill(img, wood, 904 + yy, rect=(x0, yy - 4, x1, yy + 4), scale=4, stretch=(4, .3))
    for r in ((x0 - 8, y0 - 8, x0 + 8, y1 + 4), (x1 - 8, y0 - 8, x1 + 8, y1 + 4)): I.fill(img, wood, 905, rect=r, scale=5, stretch=(.3, 4))
    for r in ((x0 - 8, y0 - 12, x1 + 8, y0 + 6), (x0 - 8, y1 - 10, x1 + 8, y1 + 10)): I.fill(img, wood, 906, rect=r, scale=5, stretch=(4, .3))
    I.volume(img, (x0 - 8, y0 - 12, x1 + 8, y1 + 10), k=.35, rim=.15)
    save(img, 'm_vs_mokumokuren')
    return [[x, y, rx, ry] for x, y, rx, ry, _ in EYES]


# ───────────── Gifts (one atlas) ─────────────
def item_done(img):
    out = img.resize((P.W, P.H), Image.LANCZOS); a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .88; a[..., :3] += np.random.default_rng(7).normal(0, 3.5, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def g_geta():
    img = I.canvas(170, 110); I.floor_shadow(img, 85, 100, 62)
    I.fill(img, '#46301c', 1, poly=[(74, 54), (96, 54), (94, 98), (76, 98)], scale=3); I.volume(img, (74, 54, 96, 98), k=.4)
    I.fill(img, '#8a6038', 2, poly=[(14, 44), (156, 44), (152, 60), (18, 60)], scale=4, stretch=(4, .4)); I.volume(img, (14, 40, 156, 60), k=.5, rim=.2)
    I.fill(img, '#a87a4a', 3, poly=[(22, 36), (148, 36), (156, 44), (14, 44)], scale=4, stretch=(4, .4))
    I.line(img, [(34, 42), (60, 22), (85, 16), (110, 22), (136, 42)], '#b3302b', 7); I.line(img, [(85, 16), (85, 40)], '#b3302b', 5)
    return img


def g_kusuri():
    img = I.canvas(150, 100); I.floor_shadow(img, 75, 92, 58)
    I.fill(img, '#d9c2a8', 1, poly=[(30, 50), (40, 18), (75, 6), (110, 18), (120, 50), (75, 56)], scale=4)
    I.volume(img, (30, 6, 120, 56), k=.5)
    for k in range(7): I.line(img, [(75, 52), (36 + k * 13, 16 + abs(3 - k) * 4)], (150, 110, 96, 160), 1.6)
    I.fill(img, '#e8d4bc', 2, ell=(18, 46, 132, 92), scale=4); I.volume(img, (18, 46, 132, 92), k=.5, rim=.3)
    I.fill(img, '#cfe4c8', 3, ell=(30, 50, 120, 74), scale=3, contrast=.3); I.volume(img, (30, 50, 120, 74), k=.3, spec=.35)
    return img


def g_waraji():
    img = I.canvas(170, 150)
    I.line(img, [(85, 0), (85, 30)], '#b3302b', 3); I.line(img, [(85, 30), (58, 50)], '#b3302b', 3); I.line(img, [(85, 30), (112, 50)], '#b3302b', 3)
    I.ell(img, (78, 24, 92, 36), '#8e2420')
    for x in (58, 112):
        I.fill(img, '#c9a55a', x, ell=(x - 24, 50, x + 24, 146), scale=3, stretch=(4, .4), contrast=1.3)
        m = I.mask_poly(img, ell=(x - 24, 50, x + 24, 146))
        clipped(img, m, lambda d, l, x=x: [d.line([(px(x - 26), px(y)), (px(x + 26), px(y + 1))], fill=(110, 84, 36, 170), width=px(1.6)) for y in range(56, 146, 8)])
        I.volume(img, (x - 24, 50, x + 24, 146), k=.5, rim=.3)
        I.line(img, [(x - 18, 80), (x, 60), (x + 18, 80)], '#b3302b', 4)
    return img


def g_mekago():
    img = I.canvas(180, 170); I.floor_shadow(img, 90, 160, 70)
    m = I.fill(img, '#b99a60', 1, poly=[(20, 40), (160, 40), (146, 150), (34, 150)], scale=4, contrast=1.1)
    def kagome(d, l):
        for k in range(-12, 16):
            for a in (0, 60, 120):
                t = math.radians(a); x0, y0 = 90 + k * 13 * math.cos(t + math.pi / 2), 95 + k * 13 * math.sin(t + math.pi / 2)
                d.line([(px(x0 - math.cos(t) * 200), px(y0 - math.sin(t) * 200)), (px(x0 + math.cos(t) * 200), px(y0 + math.sin(t) * 200))], fill=(92, 70, 36, 255), width=px(2.6))
    clipped(img, m, kagome); I.volume(img, (20, 40, 160, 150), k=.5, rim=.35)
    I.fill(img, '#a2844e', 2, ell=(14, 30, 166, 54), scale=3, stretch=(4, .5)); I.fill(img, '#3a2c1a', 3, ell=(26, 36, 154, 50), scale=3)
    return img


def g_zaru():
    img = I.canvas(200, 110); I.floor_shadow(img, 100, 100, 84)
    I.fill(img, '#b8995a', 1, ell=(10, 40, 190, 98), scale=4, stretch=(3, .5), contrast=1.2); I.volume(img, (10, 40, 190, 98), k=.5, rim=.35)
    I.fill(img, '#8a6e3c', 2, ell=(24, 46, 176, 80), scale=4)
    rnd = random.Random(3); d = ImageDraw.Draw(img)
    for _ in range(150):
        a = rnd.uniform(0, math.tau); r = rnd.random() ** .7; x = 100 + math.cos(a) * 70 * r; y = 62 + math.sin(a) * 14 * r - (1 - r) * 16
        c = rnd.choice([(122, 30, 26), (140, 38, 30), (104, 24, 22)]); d.ellipse([px(x - 5), px(y - 3.6), px(x + 5), px(y + 3.6)], fill=c + (255,)); d.ellipse([px(x - 3), px(y - 3), px(x - .5), px(y - 1)], fill=(230, 170, 150, 200))
    return img


def g_plush():
    img = I.canvas(150, 130); I.floor_shadow(img, 75, 122, 58)
    shape(img, hexc('#e8c4b0'), 1, [(75, 18), (112, 30), (132, 70), (136, 110), (110, 124), (40, 124), (14, 110), (18, 70), (38, 30)], scale=5, contrast=.5, dk=.3, lt=.14, k=.55, rim=.35, spec=.25)
    d = ImageDraw.Draw(img)
    for sx in (-1, 1): d.arc([px(75 + sx * 20 - 9), px(60), px(75 + sx * 20 + 9), px(74)], 20, 160, fill=(80, 40, 36, 255), width=px(2.6))
    d.ellipse([px(71), px(82), px(79), px(89)], fill=(110, 46, 44, 255))
    for y in range(26, 122, 7): d.line([(px(75), px(y)), (px(75), px(y + 3))], fill=(170, 110, 100, 200), width=px(1.2))
    I.fill(img, '#f2ebdc', 2, rect=(118, 96, 134, 116), scale=2)
    blush(img, [(40, 84), (110, 84)], 9, 80)
    return img


def g_tsuzura():
    img = I.canvas(170, 140); I.floor_shadow(img, 85, 132, 70)
    for box, s in (((18, 56, 152, 128), 1), ((12, 40, 158, 68), 2)):
        m = I.fill(img, '#9c7a44', s, rect=box, scale=3, contrast=1.2)
        clipped(img, m, lambda d, l, b=box: [d.line([(px(b[0] + k * 8), px(b[1])), (px(b[0] + k * 8 + 6), px(b[3]))], fill=(70, 50, 24, 200), width=px(1.6)) for k in range(20)] + [d.line([(px(b[0]), px(y)), (px(b[2]), px(y))], fill=(190, 160, 100, 140), width=px(1.2)) for y in range(b[1] + 4, b[3], 7)])
        I.volume(img, box, k=.5, rim=.25)
    I.line(img, [(85, 40), (85, 128)], '#c8302a', 4); I.line(img, [(12, 58), (158, 58)], '#c8302a', 4)
    I.line(img, [(85, 40), (66, 24), (84, 36)], '#e8e0d0', 4); I.line(img, [(85, 40), (104, 24), (86, 36)], '#e8e0d0', 4)
    return img


def g_goban():
    img = I.canvas(200, 150); I.floor_shadow(img, 100, 142, 86)
    for x in (34, 150): I.fill(img, '#6a4424', x, rect=(x, 110, x + 18, 138), scale=3)
    I.fill(img, '#b88a4c', 1, poly=[(12, 58), (188, 58), (188, 112), (12, 112)], scale=5, stretch=(4, .4)); I.volume(img, (12, 58, 188, 112), k=.4, rim=.15)
    I.fill(img, '#d8b070', 2, poly=[(40, 18), (160, 18), (188, 58), (12, 58)], scale=5, stretch=(4, .4))
    d = ImageDraw.Draw(img)
    for k in range(7):
        u = k / 6; d.line([(px(40 + 120 * u), px(18)), (px(12 + 176 * u), px(58))], fill=(70, 50, 24, 200), width=px(1.2))
        y = 18 + 40 * u; w = 60 + 28 * u; d.line([(px(100 - w), px(y)), (px(100 + w), px(y))], fill=(70, 50, 24, 200), width=px(1.2))
    for (u, v), c in [((.5, .5), (20, 18, 18)), ((.33, .5), (236, 232, 222)), ((.67, .5), (236, 232, 222)), ((.5, .25), (236, 232, 222)), ((.5, .75), (236, 232, 222)), ((.17, .17), (20, 18, 18))]:
        y = 18 + 40 * v; w = 60 + 28 * v; x = 100 - w + 2 * w * u
        d.ellipse([px(x - 7), px(y - 4.5), px(x + 7), px(y + 4.5)], fill=c + (255,)); d.ellipse([px(x - 4), px(y - 3), px(x - 1), px(y - 1.5)], fill=(255, 255, 255, 150))
    return img


def g_scroll():
    img = I.canvas(150, 440)
    I.fill(img, '#2c3350', 1, rect=(14, 14, 136, 414), scale=5); I.fill(img, '#e6dcc2', 2, rect=(26, 52, 124, 380), scale=6, contrast=.8)
    I.line(img, [(4, 12), (146, 12)], '#3a2618', 8); I.line(img, [(75, 0), (40, 12)], '#6a4a2a', 2); I.line(img, [(75, 0), (110, 12)], '#6a4a2a', 2)
    I.line(img, [(0, 418), (150, 418)], '#3a2618', 10); I.ell(img, (0, 410, 14, 426), '#1e140c'); I.ell(img, (136, 410, 150, 426), '#1e140c')
    I.text(img, '夜', 75, 76, 26, '#2a2020', I.SERIF, brush=True); I.text(img, '客', 75, 104, 26, '#2a2020', I.SERIF, brush=True)
    ink = (40, 34, 34, 230); d = ImageDraw.Draw(img)
    d.polygon([(px(52), px(150)), (px(40), px(176)), (px(64), px(176))], fill=ink); d.line([(px(52), px(176)), (px(52), px(188))], fill=ink, width=px(2))   # umbrella
    d.ellipse([px(86), px(144), px(106), px(186)], fill=ink)                                                                                          # sandal
    d.ellipse([px(40), px(206), px(64), px(230)], fill=ink); d.rectangle([px(44), px(228), px(60), px(250)], fill=ink)                              # kozō
    d.ellipse([px(84), px(222), px(112), px(236)], fill=ink)                                                                                          # sieve
    for k in range(4): d.arc([px(42 - k * 3), px(270 + k * 8), px(64 + k * 3), px(278 + k * 8)], 0, 300, fill=ink, width=px(2))                    # whirlwind
    d.ellipse([px(84), px(270), px(112), px(298)], fill=ink)                                                                                          # nuppeppō
    d.ellipse([px(42), px(320), px(62), px(338)], fill=ink); d.polygon([(px(42), px(326)), (px(34), px(330)), (px(42), px(332))], fill=ink)        # sparrow
    d.rectangle([px(86), px(314), px(110), px(346)], outline=ink, width=px(2)); d.line([(px(98), px(314)), (px(98), px(346))], fill=ink, width=px(1)) # shōji
    I.fill(img, '#b3302b', 3, rect=(96, 352, 114, 370), scale=2)
    return img


GIFTS = [('vs_geta', g_geta, 'b'), ('vs_kusuri', g_kusuri, 'b'), ('vs_waraji', g_waraji, 't'), ('vs_mekago', g_mekago, 'b'), ('vs_zaru', g_zaru, 'b'),
         ('vs_plush', g_plush, 'b'), ('vs_tsuzura', g_tsuzura, 'b'), ('vs_goban', g_goban, 'b'), ('vs_scroll', g_scroll, 't')]


def gifts():
    ims = [(iid, item_done(fn()), a) for iid, fn, a in GIFTS]; W = 1000; x = y = rowh = 0; pos = {}
    for iid, im, _ in sorted(ims, key=lambda t: -t[1].height):
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[iid] = (x, y, im.width, im.height); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for iid, im, _ in ims: at.paste(im, pos[iid][:2])
    at.save(os.path.join(ASSETS, 'items', 'atlas_vs.webp'), 'WEBP', quality=88, alpha_quality=92, method=6)
    return {'size': [W, y + rowh], 'at': {iid: list(p) for iid, p in pos.items()}}


if __name__ == '__main__':
    for f in (karakasa, bakezori, kozo, azuki, kamaitachi, nuppeppo, yosuzume): f()
    eyes = mokumokuren()
    print(json.dumps({'mon': M.META, 'eyes': eyes, 'atlas': gifts()}))
