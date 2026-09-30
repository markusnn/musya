#!/usr/bin/env python3
"""«Сто свечей» (hyakumonogatari): the blue-lantern spirit Ao-andon, the candle stand of the bedroom,
the milestone things and a dark tatami for the candle panel. Same spline toolkit as story_art.py.
Usage: python3 art/candles_art.py  → assets/mon/m_cd_aoandon.webp, assets/items/atlas_cd.webp, assets/bg/cd_tatami.webp
Prints the atlas rect map (paste into feat/candles.js)."""
import json, math, os, random, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.argv = [sys.argv[0], os.path.join(ROOT, 'assets/mon')]          # monsters.py reads its out dir from argv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc, fbm
import monsters as M
from monsters import canvas, px, soft, hair
from story_art import cr, mask_of, shape, clipped, poly_s, folds, hair_texture
from items import text, SERIF

BLK = (16, 14, 16, 255)
PREV = os.path.join(ROOT, 'art/out'); os.makedirs(PREV, exist_ok=True)


def finish(img, seed):
    out = img.resize((P.W, P.H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(.5))
    a = np.asarray(out, np.float32); n = np.random.default_rng(seed).normal(0, 4.5, a.shape[:2])[..., None]
    a[..., :3] = np.clip(a[..., :3] + n, 0, 255); return Image.fromarray(a.astype(np.uint8), 'RGBA')


def stroke(d, pts, col, w, n=8):
    d.line([(px(x), px(y)) for x, y in cr(pts, n, False)], fill=col, width=max(1, px(w)), joint='curve')


def flame(img, x, y, h, blue=False):
    """A small painted candle flame with its tip at (x, y-h) and the wick at (x, y)."""
    halo = (120, 170, 255, 70) if blue else (255, 190, 110, 70)
    soft(img, lambda d: d.ellipse([px(x - h * .9), px(y - h * 1.3), px(x + h * .9), px(y + h * .2)], fill=halo), h * .35)
    out = (90, 140, 255, 255) if blue else (240, 150, 60, 255); mid = (170, 210, 255, 255) if blue else (255, 214, 120, 255)
    d = ImageDraw.Draw(img)
    for k, col in ((1, out), (.72, mid), (.4, (255, 250, 232, 255))):
        poly_s(d, [(x, y - h * k * 1.02), (x + h * .26 * k, y - h * .35 * k), (x + h * .18 * k, y - h * .02), (x, y + h * .06), (x - h * .18 * k, y - h * .02), (x - h * .26 * k, y - h * .35 * k)], col, 6)
    d.line([(px(x), px(y + 1)), (px(x), px(y - h * .12))], fill=(30, 20, 14, 255), width=px(1.4))


def candle(img, x, top, bot, w, seed, col=(236, 228, 210, 255), drips=True):
    """Japanese warōsoku: slightly wider at the top, wax drips, a dark wick."""
    pts = [(x - w * .56, top), (x + w * .56, top), (x + w * .44, bot), (x - w * .44, bot)]
    m = shape(img, col, seed, pts, scale=5, contrast=.5, dk=.35, lt=.15, k=.6, rim=.35, smooth=False, feather=.4)
    if drips:
        rnd = random.Random(seed)
        def fn(d, l):
            for _ in range(3):
                dx = rnd.uniform(-.4, .4) * w; L = rnd.uniform(.12, .35) * (bot - top)
                d.rounded_rectangle([px(x + dx - 1.6), px(top), px(x + dx + 1.6), px(top + L)], px(1.6), fill=mixc(col, (255, 255, 255, 255), .35))
        clipped(img, m, fn)
    ImageDraw.Draw(img).ellipse([px(x - w * .56), px(top - 2.5), px(x + w * .56), px(top + 2.5)], fill=mixc(col, (255, 255, 255, 255), .25))
    return m


# ───────────── Ao-andon: the spirit of the blue lantern, who comes after the hundredth tale ─────────────
def andon_lamp(img, x0, x1, y0, y1, seed, lit=1.0):
    """A floor andon with blue paper: four legs, a lacquer frame, kumiko grid, a handle on top."""
    lac = (26, 18, 16, 255); d = ImageDraw.Draw(img)
    w = x1 - x0; ly = y1 - (y1 - y0) * .1
    for lx in (x0 + 4, x1 - 10): d.rectangle([px(lx), px(ly - 8), px(lx + 6), px(y1)], fill=lac)
    stroke(d, [(x0 + w * .2, y0 + 2), (x0 + w * .3, y0 - (y1 - y0) * .16), (x0 + w * .7, y0 - (y1 - y0) * .16), (x0 + w * .8, y0 + 2)], lac, 4)
    mp = shape(img, hexc('#5f8fc4'), seed, [(x0 + 6, y0 + 8), (x1 - 6, y0 + 8), (x1 - 6, ly - 10), (x0 + 6, ly - 10)], scale=6, contrast=.7, dk=.3, lt=.3, k=.2, rim=.25, smooth=False)
    cx, cy = (x0 + x1) / 2, (y0 + ly) / 2
    gl = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).ellipse([px(cx - w * .34), px(cy - (ly - y0) * .34), px(cx + w * .34), px(cy + (ly - y0) * .36)], fill=(214, 238, 255, int(210 * lit)))
    a = np.asarray(gl.filter(ImageFilter.GaussianBlur(w * .16 * P.SS)), np.float32); a[..., 3] *= np.asarray(mp, np.float32) / 255; img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))
    d = ImageDraw.Draw(img)
    for k in (1, 2): d.line([(px(x0 + 6), px(y0 + 8 + (ly - y0 - 18) * k / 3)), (px(x1 - 6), px(y0 + 8 + (ly - y0 - 18) * k / 3))], fill=(40, 60, 90, 150), width=px(1.4))
    d.line([(px(cx), px(y0 + 8)), (px(cx), px(ly - 10))], fill=(40, 60, 90, 130), width=px(1.4))
    for yy in (y0 + 2, ly - 12): d.rectangle([px(x0), px(yy), px(x1), px(yy + 9)], fill=lac)
    for xx in (x0, x1 - 7): d.rectangle([px(xx), px(y0 + 2), px(xx + 7), px(ly)], fill=lac)
    d.rectangle([px(x0 + 3), px(ly - 3), px(x1 - 3), px(ly + 3)], fill=(44, 30, 24, 255))


def aoandon():
    img = canvas(420, 660)
    blue, blue_d, blue_l = hexc('#27497a'), hexc('#1b3358'), hexc('#4a74a8')
    # long black hair behind the whole figure
    hb = shape(img, BLK, 201, [(206, 90), (226, 58), (266, 48), (306, 58), (326, 92), (344, 220), (356, 360), (350, 452), (268, 470), (190, 452), (184, 360), (190, 220)], scale=8, contrast=.5, dk=.2, lt=.1, k=.3, rim=.1)
    hair_texture(img, hb, 202, [(266 + x, 60, 0) for x in range(-56, 57, 4)], 420, 260, gravity=.02, col=(30, 32, 40))
    # the robe: a long blue kosode trailing on the floor to the right
    body = [(226, 190), (266, 184), (306, 190), (330, 240), (340, 330), (352, 450), (372, 560), (406, 640), (360, 652), (266, 656), (170, 650), (168, 560), (182, 450), (194, 330), (204, 240)]
    mb = shape(img, blue, 203, body, scale=26, stretch=(1, 3), contrast=1.05, dk=.5, lt=.18, k=.45, rim=.35)
    def waves(d, l):   # seigaiha waves at the hem, pale as moonlit water
        for row in range(6):
            yy = 548 + row * 18
            for k in range(-1, 16):
                xx = 160 + k * 18 + (row % 2) * 9
                for r in (15, 10, 5): d.arc([px(xx - r), px(yy - r), px(xx + r), px(yy + r)], 180, 360, fill=(150, 186, 226, 130), width=px(1.3))
    clipped(img, mb, waves)
    rnd = random.Random(204)
    def kikyo(d, l):   # a few pale bellflowers scattered on the robe
        for _ in range(16):
            x, y = rnd.uniform(190, 350), rnd.uniform(260, 520); r = rnd.uniform(5, 7)
            for p in range(5):
                a = p / 5 * math.tau - math.pi / 2
                d.polygon([(px(x), px(y)), (px(x + math.cos(a - .32) * r), px(y + math.sin(a - .32) * r)), (px(x + math.cos(a) * r * 1.3), px(y + math.sin(a) * r * 1.3)), (px(x + math.cos(a + .32) * r), px(y + math.sin(a + .32) * r))], fill=(176, 170, 226, 170))
            d.ellipse([px(x - 1.6), px(y - 1.6), px(x + 1.6), px(y + 1.6)], fill=(240, 236, 200, 200))
    clipped(img, mb, kikyo)
    folds(img, mb, [[(236, 400), (226, 520), (214, 648)], [(300, 400), (318, 520), (344, 640)], [(268, 420), (270, 650)]], w=4)
    # obi, dark as ink, with a silver cord
    mo = shape(img, hexc('#15182a'), 205, [(198, 326), (336, 326), (340, 378), (194, 378)], scale=6, contrast=.8, dk=.3, lt=.15, k=.3, rim=.15, smooth=False)
    ImageDraw.Draw(img).rounded_rectangle([px(196), px(348), px(340), px(354)], px(3), fill=(170, 184, 204, 255))
    # the right sleeve hangs, the left arm reaches toward the lantern
    shape(img, blue_d, 206, [(300, 196), (334, 214), (352, 280), (360, 430), (348, 470), (316, 472), (306, 430), (304, 300)], scale=18, stretch=(1, 3), contrast=1.0, dk=.45, lt=.15, k=.5, rim=.35)
    ms = shape(img, blue_l, 207, [(228, 200), (196, 226), (160, 300), (130, 356), (118, 392), (150, 412), (182, 380), (214, 320), (232, 270)], scale=16, stretch=(2, 1), contrast=1.0, dk=.45, lt=.15, k=.5, rim=.35)
    shape(img, (208, 220, 236, 255), 208, [(132, 384), (112, 392), (96, 404), (92, 414), (104, 416), (122, 410), (140, 402)], scale=5, contrast=.3, k=.3, rim=.2, feather=.5)   # hand
    d = ImageDraw.Draw(img)
    for k in range(3): stroke(d, [(114 - k * 3, 404 + k * 4), (96 - k * 4, 410 + k * 5), (88 - k * 4, 414 + k * 5)], (200, 214, 232, 255), 3.2)
    # collar: white eri over a pale under-collar
    poly_s(d, [(242, 188), (266, 262), (290, 188), (280, 188), (266, 238), (252, 188)], (232, 236, 240, 255), 4)
    poly_s(d, [(236, 190), (266, 280), (296, 190), (290, 190), (266, 262), (242, 190)], (150, 176, 206, 255), 4)
    shape(img, (206, 216, 230, 255), 209, [(250, 150), (282, 150), (286, 196), (246, 196)], scale=8, contrast=.3, k=.3, rim=.2)   # neck
    # face: pale, lit blue from below-left
    shape(img, (220, 228, 238, 255), 210, ell=(229, 80, 303, 184), scale=10, contrast=.3, dk=.2, lt=.08, k=.35, rim=.25)
    # horns through the hair
    for sx, bx in ((-1, 244), (1, 288)):
        hp = [(bx - 7, 78), (bx + 7, 78), (bx + sx * 10 + 3, 50), (bx + sx * 16, 30), (bx + sx * 11, 48)]
        shape(img, (226, 218, 196, 255), 211 + sx, hp, scale=4, contrast=.5, dk=.35, lt=.1, k=.5, rim=.3, feather=.4)
        clipped(img, mask_of(img, hp, feather=0), lambda dd, l: [dd.line([(px(bx - 7), px(70 - k * 8)), (px(bx + 7), px(66 - k * 8))], fill=(150, 136, 110, 160), width=px(1.2)) for k in range(4)])
    # hair in front: centre parting, curtains down past the shoulders
    for sx in (-1, 1):
        cp = [(266, 62), (266 + sx * 30, 64), (266 + sx * 48, 96), (266 + sx * 52, 180), (266 + sx * 58, 300), (266 + sx * 44, 330), (266 + sx * 34, 200), (266 + sx * 30, 120), (266 + sx * 10, 76)]
        mh = shape(img, BLK, 212 + sx, cp, scale=6, contrast=.5, dk=.2, lt=.12, k=.3, rim=.1, feather=.5)
        hair_texture(img, mh, 214 + sx, [(266 + sx * k, 66, sx * .1) for k in range(4, 50, 3)], 270, 90, gravity=.05, col=(34, 36, 46))
    soft(img, lambda dd: dd.arc([px(232), px(58), px(300), px(110)], 200, 330, fill=(110, 130, 170, 120), width=px(5)), 3)   # blue sheen
    d = ImageDraw.Draw(img)
    # hikimayu: soft painted eyebrows high on the forehead
    soft(img, lambda dd: [dd.ellipse([px(x - 7), px(96), px(x + 7), px(104)], fill=(40, 40, 52, 190)) for x in (250, 282)], 2)
    for ex in (252, 280):   # narrow half-closed eyes, a cold glint
        poly_s(d, [(ex - 9, 128), (ex - 1, 125.5), (ex + 9, 128), (ex, 130)], (26, 24, 32, 255), 5)
        d.ellipse([px(ex - 1.5), px(126.5), px(ex + 2), px(128.5)], fill=(160, 210, 255, 230))
        d.arc([px(ex - 10), px(122), px(ex + 10), px(134)], 205, 335, fill=(30, 28, 36, 255), width=px(1.4))
    soft(img, lambda dd: dd.line([(px(267), px(136)), (px(268), px(148))], fill=(140, 150, 170, 110), width=px(2)), 1.5)
    # the smile: red lips, blackened teeth (ohaguro)
    d = ImageDraw.Draw(img)
    poly_s(d, [(256, 161), (266, 158.5), (276, 161), (273, 167), (266, 169), (259, 167)], (150, 40, 54, 255), 6)
    poly_s(d, [(259, 162.5), (266, 161), (273, 162.5), (270, 165.5), (266, 166.2), (262, 165.5)], (14, 12, 16, 255), 6)
    # the lantern at her side
    andon_lamp(img, 18, 118, 400, 650, 215)
    # blue light from the lantern: cool rim on the left, the right side sinks into the dark
    a = np.asarray(img, np.float32); h, w = a.shape[:2]; xx = np.linspace(0, 1, w)[None, :]; yy = np.linspace(0, 1, h)[:, None]
    lamp = np.exp(-(((xx - .16) / .5) ** 2 + ((yy - .8) / .55) ** 2))
    a[..., 0] *= .82 + .1 * lamp; a[..., 1] *= .9 + .12 * lamp; a[..., 2] = np.minimum(255, a[..., 2] * (1.02 + .22 * lamp))
    a[..., :3] *= (.8 + .28 * lamp)[..., None]
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')
    out = finish(img, 216); out.save(os.path.join(ROOT, 'assets/mon/m_cd_aoandon.webp'), 'WEBP', quality=88, alpha_quality=92, method=6)
    print('m_cd_aoandon', out.size); return out


# ───────────── The bedroom candle stand: three lacquer steps, seven candles (flames are drawn live) ─────────────
STAND_FLAMES = []


def stand():
    img = canvas(230, 200)
    lac, red = (24, 16, 14, 255), hexc('#7a2a20')
    tiers = [(8, 222, 168, 184), (30, 200, 120, 132), (56, 174, 74, 86)]   # x0,x1,top,bottom (front to back)
    d = ImageDraw.Draw(img)
    for x in (16, 212): d.rectangle([px(x - 4), px(184), px(x + 4), px(198)], fill=lac)
    for x0, x1, t, b in tiers[1:]:
        for x in (x0 + 8, x1 - 8): d.rectangle([px(x - 3), px(b), px(x + 3), px(184)], fill=lac)
    cands = [[(44, 40), (115, 44), (186, 40)], [(78, 38), (152, 38)], [(96, 34), (134, 34)]]
    for (x0, x1, t, b), row in zip(tiers[::-1], cands[::-1]):   # back first
        m = shape(img, lac, 300 + t, [(x0, t), (x1, t), (x1, b), (x0, b)], scale=6, contrast=.8, dk=.3, lt=.25, k=.4, rim=.2, smooth=False, feather=.4)
        clipped(img, m, lambda dd, l, x0=x0, x1=x1, t=t: [dd.line([(px(x0 + 6), px(t + 2)), (px(x1 - 6), px(t + 2))], fill=mixc(red, (0, 0, 0, 255), .2), width=px(2)),
                                                           dd.line([(px(x0 + 30), px(t + 7)), (px(x0 + 60), px(t + 7))], fill=(110, 50, 36, 200), width=px(1.4))])
        for i, (cx, ch) in enumerate(row):
            ImageDraw.Draw(img).ellipse([px(cx - 9), px(t - 3), px(cx + 9), px(t + 3)], fill=(60, 44, 30, 255))
            candle(img, cx, t - ch, t - 1, 13, 320 + cx + t)
            STAND_FLAMES.append((cx, t - ch - 1))
    # soot and old wax on the steps
    soft(img, lambda dd: [dd.ellipse([px(x - 10), px(y - 4), px(x + 10), px(y + 2)], fill=(230, 220, 200, 70)) for x, y in ((60, 168), (170, 120), (120, 74))], 2)
    return finish(img, 330)


def rosoku():   # Aizu e-rōsoku: red painted candles in black holders
    img = canvas(150, 200)
    d = ImageDraw.Draw(img)
    for cx in (45, 105):
        shape(img, (30, 22, 20, 255), 400 + cx, ell=(cx - 26, 178, cx + 26, 196), scale=5, k=.5, rim=.3)
        d = ImageDraw.Draw(img); d.rectangle([px(cx - 4), px(158), px(cx + 4), px(186)], fill=(34, 24, 20, 255))
        shape(img, (40, 28, 22, 255), 402 + cx, ell=(cx - 18, 152, cx + 18, 164), scale=5, k=.5, rim=.3)
        m = candle(img, cx, 52, 156, 26, 404 + cx, col=hexc('#a8302a'), drips=False)
        def paint_fl(dd, l, cx=cx):   # a camellia, a leaf, a chrysanthemum
            for fy, col in ((84, (240, 236, 226, 255)), (122, (238, 170, 186, 255))):
                for p in range(5):
                    a = p / 5 * math.tau; dd.ellipse([px(cx + math.cos(a) * 5 - 5), px(fy + math.sin(a) * 5 - 5), px(cx + math.cos(a) * 5 + 5), px(fy + math.sin(a) * 5 + 5)], fill=col)
                dd.ellipse([px(cx - 3), px(fy - 3), px(cx + 3), px(fy + 3)], fill=(230, 190, 70, 255))
            for sx in (-1, 1): dd.ellipse([px(cx + sx * 9 - 5), px(100), px(cx + sx * 9 + 5), px(108)], fill=(70, 110, 60, 255))
        clipped(img, m, paint_fl)
        flame(img, cx, 50, 22)
    return finish(img, 410)


def shokudai():   # a tall iron candlestick with a drip pan
    img = canvas(110, 280)
    iron = (38, 32, 30, 255); d = ImageDraw.Draw(img)
    for sx in (-1, 1): stroke(d, [(55, 240), (55 + sx * 24, 262), (55 + sx * 40, 274)], iron, 5)
    shape(img, iron, 501, ell=(34, 232, 76, 250), scale=4, k=.6, rim=.3, spec=.15)
    shape(img, iron, 502, [(51, 104), (59, 104), (61, 240), (49, 240)], scale=4, k=.6, rim=.3, smooth=False, spec=.2)
    for y in (150, 196): shape(img, iron, 503 + y, ell=(45, y - 5, 65, y + 5), scale=4, k=.6, rim=.3)
    shape(img, (54, 44, 36, 255), 505, ell=(20, 92, 90, 110), scale=4, k=.6, rim=.3, spec=.2)
    candle(img, 55, 44, 100, 24, 506)
    flame(img, 55, 42, 24)
    return finish(img, 510)


def hon():   # «Hyakumonogatari» picture books, a candle stub on top
    img = canvas(200, 150)
    covers = [(hexc('#3a2c24'), 18, 116, 176, 140), (hexc('#2c3e5c'), 26, 94, 184, 118), (hexc('#44304e'), 14, 72, 170, 96)]
    for i, (col, x0, t, x1, b) in enumerate(covers):
        shape(img, (226, 214, 188, 255), 600 + i, [(x0 + 4, t + 4), (x1, t + 4), (x1, b - 3), (x0 + 4, b - 3)], scale=4, contrast=.4, k=.3, rim=.1, smooth=False, feather=.3)
        m = shape(img, col, 610 + i, [(x0, t), (x1 - 4, t), (x1 - 4, t + 6), (x0, t + 6)], scale=6, contrast=.8, k=.4, rim=.2, smooth=False, feather=.3)
        d = ImageDraw.Draw(img)
        for k in range(1, 6): d.line([(px(x1 - 2), px(t + 7 + k * 2.6)), (px(x0 + 6), px(t + 7 + k * 2.6))], fill=(200, 188, 160, 120), width=px(.6))
        d.rectangle([px(x0), px(t + 6), px(x0 + 5), px(b - 2)], fill=mixc(col, (0, 0, 0, 255), .2))
        for k in range(4): d.ellipse([px(x0 + 1), px(t + 9 + k * 4), px(x0 + 4), px(t + 11 + k * 4)], fill=(210, 200, 170, 220))
    # top cover with a title slip
    m = shape(img, hexc('#44304e'), 620, [(14, 60), (170, 60), (170, 74), (14, 74)], scale=6, contrast=.8, k=.4, rim=.2, smooth=False, feather=.3)
    ImageDraw.Draw(img).rectangle([px(96), px(61), px(160), px(72)], fill=(232, 222, 196, 255))
    text(img, '百物語', 128, 66.5, 10, (30, 22, 20), font=SERIF)
    # a burnt-out candle stub and a curl of smoke
    ImageDraw.Draw(img).ellipse([px(40), px(58), px(72), px(66)], fill=(52, 40, 30, 255))
    candle(img, 56, 38, 60, 16, 621)
    ImageDraw.Draw(img).line([(px(56), px(38)), (px(56), px(33))], fill=(30, 20, 14, 255), width=px(1.6))
    soft(img, lambda dd: stroke(dd, [(56, 33), (62, 20), (52, 10), (58, 0)], (200, 204, 214, 120), 2), 1.2)
    return finish(img, 630)


def blue_andon():
    img = canvas(140, 260)
    andon_lamp(img, 14, 126, 30, 256, 700)
    return finish(img, 710)


def tatami():
    """The dark room of the candle panel, seen from above at an angle. Projection shared with the JS:
    screen x = W/2 + X*F/Z, y = YH + HC*F/Z (W=720, H=540, F=560, HC=1, YH=-300)."""
    W, H, F, YH = 720, 540, 560.0, -300.0
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    Z = F / (ys - YH); X = (xs - W / 2) * Z / F
    col = np.floor((X + .25) / .5); lx = X + .25 - col * .5
    lz = (Z + .5 * (np.mod(col, 2))) % 1.0
    n = fbm(W, H, 30, 4, 11); n2 = fbm(W, H, 4, 2, 12)
    base = np.array([72, 66, 44], np.float32); gold = np.array([96, 88, 58], np.float32)
    fade = np.clip(1.4 - Z, .25, 1)                                    # far weave blurs out
    weave = .5 + .5 * np.sin(lz * math.tau * 60) * fade
    rgb = base + (gold - base) * (.55 * weave + .4 * n)[..., None] + (n2[..., None] - .5) * 14
    heri = (lx < .016) | (lx > .484)
    rgb[heri] = (np.array([24, 22, 28], np.float32) + (n2[heri, None] - .5) * 10)
    seam = np.minimum(lz, 1 - lz) < .006
    rgb[seam] *= .55
    cx, cy = W / 2, 300
    r = np.sqrt(((xs - cx) / (W * .62)) ** 2 + ((ys - cy) / (H * .62)) ** 2)
    rgb *= np.clip(1.08 - r ** 1.6, .05, 1)[..., None]
    rgb *= (.5 + .5 * np.clip(ys / H * 1.6, 0, 1))[..., None]          # the far end of the room is dark
    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), 'RGB').filter(ImageFilter.GaussianBlur(.6))
    img.save(os.path.join(ROOT, 'assets/bg/cd_tatami.webp'), 'WEBP', quality=84, method=6)
    print('cd_tatami', img.size)


if __name__ == '__main__':
    ao = aoandon()
    parts = [('cd_stand', stand()), ('cd_rosoku', rosoku()), ('cd_shokudai', shokudai()), ('cd_hon', hon()), ('cd_aoandon', blue_andon())]
    gap = 4; AW = sum(p.width for _, p in parts) + gap * (len(parts) - 1); AH = max(p.height for _, p in parts)
    atlas = Image.new('RGBA', (AW, AH), (0, 0, 0, 0)); rects = {}; x = 0
    for name, p in parts: atlas.alpha_composite(p, (x, 0)); rects[name] = [x, 0, p.width, p.height]; x += p.width + gap
    atlas.save(os.path.join(ROOT, 'assets/items/atlas_cd.webp'), 'WEBP', quality=88, alpha_quality=92, method=6)
    tatami()
    pv = Image.new('RGBA', (AW + ao.width + 20, max(AH, ao.height)), (46, 44, 52, 255)); pv.alpha_composite(atlas, (0, 0)); pv.alpha_composite(ao, (AW + 20, 0)); pv.save(os.path.join(PREV, 'candles_preview.png'))
    print('atlas', AW, AH, json.dumps(rects)); print('stand flames', STAND_FLAMES)
