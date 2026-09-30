#!/usr/bin/env python3
"""Yōkai guests who knock at the gate: a tanuki with a straw hat and a sake flask, and a two-tailed nekomata
dancing with a tenugui on her head. Same organic spline toolkit as story_art.py.
Usage: guests_art.py <outdir> (assets/mon)"""
import json, math, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc
import monsters as M
from monsters import canvas, px, soft, save
from story_art import cr, mask_of, shape, clipped, poly_s, folds
from items import text, SERIF

BLACK, WHITE = (0, 0, 0, 255), (255, 255, 255, 255)


def stroke(d, pts, col, w, n=8):
    d.line([(px(x), px(y)) for x, y in cr(pts, n, False)], fill=col, width=px(w), joint='curve')


def tube(center, w0, w1):
    """A tapering sausage along a centerline, as spline points for shape()."""
    L, R = [], []
    n = len(center)
    for i, (x, y) in enumerate(center):
        x0, y0 = center[max(0, i - 1)]; x1, y1 = center[min(n - 1, i + 1)]
        a = math.atan2(y1 - y0, x1 - x0) + math.pi / 2; w = w0 + (w1 - w0) * i / (n - 1)
        L.append((x + math.cos(a) * w, y + math.sin(a) * w)); R.append((x - math.cos(a) * w, y - math.sin(a) * w))
    ex, ey = center[-1]; px_, py_ = center[-2]; a = math.atan2(ey - py_, ex - px_)
    return L + [(ex + math.cos(a) * w1, ey + math.sin(a) * w1)] + R[::-1]


def fur_ticks(img, m, seed, box, n, col=(30, 20, 12, 150), length=(6, 12), ang=1.4):
    """Short brush strokes clipped to a shape: reads as fur without outlining it."""
    rnd = random.Random(seed)
    def fn(d, l):
        for _ in range(n):
            x, y = rnd.uniform(box[0], box[2]), rnd.uniform(box[1], box[3]); L = rnd.uniform(*length); a = ang + rnd.uniform(-.5, .5)
            d.line([(px(x), px(y)), (px(x + math.cos(a) * L), px(y + math.sin(a) * L))], fill=col, width=px(rnd.uniform(1, 2)))
    clipped(img, m, fn)


# ───────────── Tanuki: straw hat, leaf, big belly, sake flask on a rope ─────────────
def tanuki():
    img = canvas(340, 470)
    brown, brown_d, brown_l = hexc('#7a5634'), hexc('#553a22'), hexc('#9a7248')
    cream = hexc('#dccaa2'); mask_c = hexc('#2e2016')
    # bushy striped tail behind, to the right
    tail = [(214, 372), (250, 352), (292, 330), (320, 300), (330, 330), (318, 372), (290, 404), (248, 420), (214, 414)]
    mt = shape(img, brown, 101, tail, scale=9, contrast=1.1, k=.5, rim=.35)
    clipped(img, mt, lambda d, l: [stroke(d, [(270 + k * 18, 300 + k * 6), (262 + k * 18, 350 + k * 8), (250 + k * 16, 420)], (40, 26, 14, 200), 12) for k in range(3)])
    fur_ticks(img, mt, 102, (214, 300, 332, 420), 90, (40, 26, 14, 120))
    # stubby legs and big feet
    for sx in (-1, 1):
        shape(img, brown_d, 103 + sx, [(170 + sx * 30, 400), (170 + sx * 70, 402), (170 + sx * 78, 440), (170 + sx * 66, 458), (170 + sx * 26, 450)], scale=8, k=.5)
        shape(img, hexc('#3a281a'), 105 + sx, [(170 + sx * 24, 444), (170 + sx * 64, 440), (170 + sx * 90, 452), (170 + sx * 88, 466), (170 + sx * 22, 466)], scale=6, k=.4)
    # round body and the famous belly
    body = [(118, 214), (170, 200), (222, 214), (262, 268), (276, 340), (262, 404), (220, 430), (170, 436), (120, 430), (78, 404), (64, 340), (78, 268)]
    mb = shape(img, brown, 107, body, scale=10, contrast=1.0, k=.55, rim=.4)
    fur_ticks(img, mb, 108, (64, 210, 276, 436), 260, (48, 32, 18, 110))
    belly = shape(img, cream, 109, ell=(96, 270, 244, 430), scale=8, contrast=.6, dk=.25, lt=.15, k=.45, rim=.35, spec=.12)
    clipped(img, belly, lambda d, l: [d.arc([px(160), px(340), px(180), px(356)], 20, 340, fill=(150, 120, 80, 200), width=px(2))])   # belly button
    fur_ticks(img, belly, 110, (96, 270, 244, 430), 70, (170, 140, 100, 90), (4, 8), 1.2)
    # sake flask hanging from a rope in the left paw
    d = ImageDraw.Draw(img)
    stroke(d, [(70, 316), (58, 330), (56, 350)], (190, 160, 110, 255), 3)
    flask = [(56, 348), (68, 350), (70, 362), (86, 382), (92, 412), (84, 436), (56, 442), (28, 436), (20, 412), (26, 382), (42, 362), (44, 350)]
    mf = shape(img, hexc('#d8c8a8'), 111, flask, scale=5, contrast=.6, dk=.3, lt=.12, k=.55, rim=.4, spec=.3)
    clipped(img, mf, lambda d, l: d.rectangle([px(20), px(342), px(92), px(360)], fill=(70, 50, 34, 255)))
    lab = shape(img, hexc('#f2ebdc'), 112, [(40, 392), (72, 392), (72, 426), (40, 426)], scale=3, contrast=.3, k=.2, rim=.1, smooth=False, feather=.3)
    text(img, '福', 56, 409, 22, '#6a1a14', SERIF)
    # arms: left holds the rope, right pats the belly
    shape(img, brown_d, 113, [(96, 236), (74, 262), (60, 300), (66, 328), (86, 322), (94, 290), (112, 262)], scale=7, k=.5)
    shape(img, hexc('#3a281a'), 114, ell=(56, 304, 88, 334), scale=5, k=.4, rim=.3)
    shape(img, brown_d, 115, [(244, 236), (268, 270), (266, 322), (236, 344), (220, 330), (240, 300), (232, 262)], scale=7, k=.5)
    shape(img, hexc('#3a281a'), 116, ell=(214, 318, 246, 350), scale=5, k=.4, rim=.3)
    # head
    for sx in (-1, 1):   # round ears peeking under the hat brim
        shape(img, brown_d, 117 + sx, ell=(170 + sx * 62 - 22, 88, 170 + sx * 62 + 22, 130), scale=5, k=.4)
        d = ImageDraw.Draw(img); d.ellipse([px(170 + sx * 62 - 11), px(100), px(170 + sx * 62 + 11), px(122)], fill=(40, 28, 20, 255))
    head = [(170, 96), (218, 104), (250, 136), (258, 174), (240, 208), (206, 226), (170, 230), (134, 226), (100, 208), (82, 174), (90, 136), (122, 104)]
    mh = shape(img, brown, 119, head, scale=8, contrast=.9, k=.55, rim=.35)
    fur_ticks(img, mh, 120, (84, 100, 256, 228), 120, (48, 32, 18, 100), (4, 9))
    muzzle = shape(img, cream, 121, [(140, 178), (170, 168), (200, 178), (212, 204), (196, 224), (170, 230), (144, 224), (128, 204)], scale=6, contrast=.5, dk=.2, lt=.12, k=.4, rim=.2)
    for sx in (-1, 1):   # the dark bandit mask around the eyes
        shape(img, mask_c, 122 + sx, [(170 + sx * 8, 150), (170 + sx * 34, 136), (170 + sx * 64, 146), (170 + sx * 70, 176), (170 + sx * 50, 196), (170 + sx * 20, 186)], scale=6, contrast=.6, dk=.2, lt=.15, k=.3, rim=.1)
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        ex = 170 + sx * 38
        d.ellipse([px(ex - 12), px(156), px(ex + 12), px(180)], fill=(236, 226, 196, 255))
        d.ellipse([px(ex - 7), px(160), px(ex + 7), px(178)], fill=(20, 12, 8, 255)); d.ellipse([px(ex - 5), px(161), px(ex - 1), px(166)], fill=(255, 255, 255, 230))
    shape(img, (26, 18, 14, 255), 124, [(160, 190), (170, 186), (180, 190), (176, 200), (170, 204), (164, 200)], scale=3, k=.5, rim=.2, spec=.4)
    d = ImageDraw.Draw(img); d.arc([px(156), px(200), px(170), px(214)], 10, 170, fill=(60, 36, 26, 255), width=px(2.4)); d.arc([px(170), px(200), px(184), px(214)], 10, 170, fill=(60, 36, 26, 255), width=px(2.4))
    soft(img, lambda dd: [dd.ellipse([px(118), px(196), px(144), px(212)], fill=(210, 110, 90, 70)), dd.ellipse([px(196), px(196), px(222), px(212)], fill=(210, 110, 90, 70))], 4)
    # straw sugegasa hat pushed back on the head, strings under the chin
    d = ImageDraw.Draw(img)
    for sx in (-1, 1): stroke(d, [(170 + sx * 70, 118), (170 + sx * 56, 176), (170 + sx * 22, 226)], (200, 170, 110, 220), 2)
    hat = [(170, 22), (214, 50), (262, 84), (292, 108), (270, 120), (170, 118), (70, 120), (48, 108), (78, 84), (126, 50)]
    mhat = shape(img, hexc('#c8a864'), 125, hat, scale=6, stretch=(3, .5), contrast=1.2, dk=.35, lt=.2, k=.5, rim=.25, smooth=True)
    clipped(img, mhat, lambda d, l: [d.line([(px(170), px(22)), (px(170 + math.cos(a) * 200), px(22 + math.sin(a) * 200))], fill=(140, 110, 60, 160), width=px(1.4)) for a in np.linspace(.35, math.pi - .35, 22)])
    clipped(img, mhat, lambda d, l: [d.arc([px(170 - r), px(22 - r * .55), px(170 + r), px(22 + r * .55)], 0, 180, fill=(120, 90, 46, 140), width=px(1.6)) for r in (40, 80, 120)])
    d = ImageDraw.Draw(img); stroke(d, [(52, 110), (170, 122), (288, 110)], (110, 80, 40, 220), 3)
    # the transformation leaf on top of the hat
    leaf = [(170, 30), (184, 6), (204, -2), (216, 4), (206, 22), (188, 34)]
    ml = shape(img, hexc('#5f8a3c'), 126, [(x, y + 8) for x, y in leaf], scale=4, contrast=.8, k=.5, rim=.3, spec=.2)
    d = ImageDraw.Draw(img); stroke(d, [(172, 36), (190, 22), (212, 10)], (46, 70, 30, 255), 1.6); stroke(d, [(168, 38), (164, 46)], (70, 60, 30, 255), 2)
    save(img, 'm_tanuki')


# ───────────── Nekomata: a two-tailed calico cat dancing with a tenugui on her head ─────────────
def nekomata():
    img = canvas(360, 470)
    white, white_d = hexc('#efe8dc'), hexc('#d6ccbc')
    ginger, black = hexc('#d0843e'), hexc('#2a2422')
    cx = 170
    # two tails forking behind: one ginger-striped curling right, one white with a black tip rising up
    t1 = tube([(214, 404), (262, 380), (300, 330), (318, 270), (336, 222), (344, 196)], 17, 12)
    m1 = shape(img, ginger, 131, t1, scale=8, contrast=.8, k=.5, rim=.35)
    clipped(img, m1, lambda d, l: [d.line([(px(x - 22), px(y + 8)), (px(x + 22), px(y - 8))], fill=(150, 80, 30, 210), width=px(7)) for x, y in ((296, 336), (314, 290), (330, 246))])
    t2 = tube([(208, 396), (240, 350), (262, 290), (270, 220), (286, 160), (304, 128)], 16, 11)
    m2 = shape(img, white, 132, t2, scale=8, contrast=.7, dk=.3, lt=.1, k=.5, rim=.35)
    clipped(img, m2, lambda d, l: d.ellipse([px(268), px(100), px(330), px(168)], fill=black))
    clipped(img, m2, lambda d, l: d.ellipse([px(236), px(250), px(290), px(300)], fill=ginger), .9)
    # hind legs, standing a little on tiptoe
    for sx in (-1, 1):
        shape(img, white_d, 133 + sx, [(cx + sx * 20, 380), (cx + sx * 60, 382), (cx + sx * 66, 432), (cx + sx * 56, 452), (cx + sx * 24, 446)], scale=7, k=.5)
        shape(img, white, 135 + sx, [(cx + sx * 18, 440), (cx + sx * 58, 438), (cx + sx * 74, 452), (cx + sx * 70, 466), (cx + sx * 16, 466)], scale=5, k=.4, rim=.3)
        d = ImageDraw.Draw(img)
        for t in range(3): d.line([(px(cx + sx * (30 + t * 12)), px(456)), (px(cx + sx * (30 + t * 12)), px(466))], fill=(170, 150, 130, 200), width=px(1.2))
    # body with calico patches
    body = [(cx - 42, 232), (cx, 222), (cx + 42, 232), (cx + 70, 290), (cx + 76, 360), (cx + 62, 410), (cx, 424), (cx - 62, 410), (cx - 76, 360), (cx - 70, 290)]
    mb = shape(img, white, 137, body, scale=9, contrast=.7, dk=.3, lt=.1, k=.5, rim=.4)
    def patches(d, l):
        poly_s(d, [(cx - 90, 240), (cx - 40, 226), (cx - 20, 262), (cx - 44, 300), (cx - 90, 296)], ginger + (), 6)
        poly_s(d, [(cx + 30, 350), (cx + 80, 336), (cx + 90, 400), (cx + 50, 426), (cx + 22, 400)], black, 6)
        poly_s(d, [(cx + 48, 250), (cx + 80, 262), (cx + 76, 300), (cx + 52, 292)], ginger, 6)
    clipped(img, mb, patches, .95)
    chest = shape(img, hexc('#f8f3ea'), 138, [(cx - 30, 240), (cx, 236), (cx + 30, 240), (cx + 36, 300), (cx, 330), (cx - 36, 300)], scale=6, contrast=.4, dk=.15, lt=.05, k=.3, rim=.15)
    fur_ticks(img, mb, 139, (cx - 76, 222, cx + 76, 424), 160, (150, 130, 110, 90), (4, 9))
    # arms: the left paw raised in a dance, the right curled at the chest
    shape(img, white_d, 140, [(cx - 50, 250), (cx - 84, 226), (cx - 104, 176), (cx - 100, 144), (cx - 82, 146), (cx - 80, 180), (cx - 60, 220), (cx - 34, 238)], scale=7, k=.5)
    shape(img, white, 141, ell=(cx - 118, 118, cx - 78, 156), scale=5, k=.4, rim=.3)
    d = ImageDraw.Draw(img)
    for t in range(3): d.ellipse([px(cx - 112 + t * 10), px(120), px(cx - 104 + t * 10), px(128)], fill=(226, 150, 150, 230))
    shape(img, white_d, 142, [(cx + 50, 250), (cx + 84, 272), (cx + 92, 300), (cx + 70, 312), (cx + 44, 296), (cx + 34, 264)], scale=7, k=.5)
    shape(img, white, 143, ell=(cx + 36, 282, cx + 72, 316), scale=5, k=.4, rim=.3)
    # head
    for sx in (-1, 1):   # ears poking out through the tenugui
        shape(img, white if sx < 0 else black, 144 + sx, [(cx + sx * 34, 104), (cx + sx * 66, 50), (cx + sx * 80, 116)], scale=5, k=.4)
        d = ImageDraw.Draw(img); poly_s(d, [(cx + sx * 44, 104), (cx + sx * 64, 66), (cx + sx * 72, 108)], (214, 140, 140, 255), 4)
    head = [(cx, 84), (cx + 50, 94), (cx + 82, 132), (cx + 88, 170), (cx + 68, 208), (cx + 30, 228), (cx, 232), (cx - 30, 228), (cx - 68, 208), (cx - 88, 170), (cx - 82, 132), (cx - 50, 94)]
    mh = shape(img, white, 146, head, scale=8, contrast=.6, dk=.25, lt=.1, k=.5, rim=.35)
    clipped(img, mh, lambda d, l: poly_s(d, [(cx + 10, 84), (cx + 90, 100), (cx + 96, 170), (cx + 50, 176), (cx + 20, 130)], ginger, 6))
    clipped(img, mh, lambda d, l: poly_s(d, [(cx - 96, 150), (cx - 60, 130), (cx - 40, 160), (cx - 70, 196), (cx - 96, 200)], black, 6), .9)
    fur_ticks(img, mh, 147, (cx - 88, 90, cx + 88, 230), 70, (150, 120, 100, 80), (3, 7))
    # tenugui: indigo towel with white dots draped over the head, knot under the chin
    tn = [(cx - 88, 138), (cx - 70, 96), (cx - 30, 76), (cx + 30, 76), (cx + 70, 96), (cx + 88, 138), (cx + 60, 124), (cx, 116), (cx - 60, 124)]
    mt = shape(img, hexc('#2c4a78'), 148, tn, scale=6, contrast=.8, dk=.35, lt=.12, k=.45, rim=.2)
    rnd = random.Random(149)
    clipped(img, mt, lambda d, l: [d.ellipse([px(x - 3.5), px(y - 3.5), px(x + 3.5), px(y + 3.5)], fill=(236, 236, 230, 230)) for x, y in [(rnd.uniform(cx - 90, cx + 90), rnd.uniform(74, 140)) for _ in range(60)]])
    for sx in (-1, 1):   # the two ends falling behind the cheeks
        me = shape(img, hexc('#284470'), 150 + sx, [(cx + sx * 84, 132), (cx + sx * 96, 150), (cx + sx * 92, 210), (cx + sx * 76, 214), (cx + sx * 74, 150)], scale=5, k=.4, rim=.2)
        clipped(img, me, lambda d, l, s=sx: [d.ellipse([px(cx + s * 84 - 3), px(y - 3), px(cx + s * 84 + 3), px(y + 3)], fill=(236, 236, 230, 220)) for y in (160, 184, 204)])
    shape(img, hexc('#284470'), 152, [(cx - 22, 226), (cx, 216), (cx + 22, 226), (cx + 10, 244), (cx - 10, 244)], scale=4, k=.4, rim=.2)
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):   # the knot's two little tails
        poly_s(d, [(cx + sx * 6, 238), (cx + sx * 26, 252), (cx + sx * 20, 262), (cx + sx * 2, 246)], (40, 68, 112, 255), 3)
    # yellow slit eyes, a little uncanny
    for sx in (-1, 1):
        ex = cx + sx * 36
        d.ellipse([px(ex - 17), px(146), px(ex + 17), px(176)], fill=hexc('#e8c23a'))
        d.ellipse([px(ex - 17), px(146), px(ex + 17), px(176)], outline=(60, 40, 20, 255), width=px(2))
        d.ellipse([px(ex - 3.5), px(148), px(ex + 3.5), px(174)], fill=(14, 10, 8, 255))
        d.ellipse([px(ex - 10), px(151), px(ex - 5), px(157)], fill=(255, 255, 255, 230))
    shape(img, hexc('#d98a90'), 153, [(cx - 8, 186), (cx + 8, 186), (cx, 196)], scale=3, k=.3, rim=.1, smooth=False, feather=.4)
    d = ImageDraw.Draw(img)
    d.arc([px(cx - 14), px(192), px(cx), px(206)], 10, 170, fill=(90, 60, 60, 255), width=px(2)); d.arc([px(cx), px(192), px(cx + 14), px(206)], 10, 170, fill=(90, 60, 60, 255), width=px(2))
    for sx in (-1, 1):
        for k in range(3):
            d.line([(px(cx + sx * 26), px(194 + k * 5)), (px(cx + sx * 76), px(186 + k * 10))], fill=(120, 110, 100, 200), width=px(1.1))
    soft(img, lambda dd: [dd.ellipse([px(cx - 70), px(184), px(cx - 44), px(200)], fill=(230, 130, 130, 70)), dd.ellipse([px(cx + 44), px(184), px(cx + 70), px(200)], fill=(230, 130, 130, 70))], 4)
    save(img, 'm_nekomata')


if __name__ == '__main__':
    tanuki(); nekomata()
    print(json.dumps({k: v for k, v in M.META.items()}))
