#!/usr/bin/env python3
"""Characters of the story «Дом, где погас фонарь»: zashiki-warashi (front/back), akaname, kappa, the fox bride, a big chōchin-obake.
Organic shapes: every outline is a Catmull-Rom spline with a feathered edge, lit from the upper left.
Usage: story_art.py <outdir> (assets/mon)"""
import json, math, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc, textured_fill
import monsters as M
from monsters import canvas, px, soft, hair, save

S = M.S
BLACK, WHITE = (0, 0, 0, 255), (255, 255, 255, 255)


def cr(pts, n=10, closed=True):
    N = len(pts); out = []
    for i in (range(N) if closed else range(N - 1)):
        g = (lambda j: pts[j % N]) if closed else (lambda j: pts[min(max(j, 0), N - 1)])
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * (2 * p1[c] + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t2 + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t3) for c in (0, 1)))
    if not closed: out.append(pts[-1])
    return out


def mask_of(img, pts=None, ell=None, feather=.7, smooth=True):
    m = Image.new('L', img.size, 0); d = ImageDraw.Draw(m)
    if ell: d.ellipse([px(v) for v in ell], fill=255)
    else: d.polygon([(px(x), px(y)) for x, y in (cr(pts) if smooth else pts)], fill=255)
    return m.filter(ImageFilter.GaussianBlur(feather * S)) if feather else m


def shape(img, base, seed, pts=None, ell=None, scale=10, contrast=1.0, dk=.5, lt=.2, stretch=(1, 1), k=.5, rim=.4, feather=.7, spec=0.0, smooth=True):
    m = mask_of(img, pts, ell, feather, smooth); box = m.getbbox()
    if not box: return m
    sub = m.crop(box)
    t = textured_fill(sub, base, mixc(base, BLACK, dk), mixc(base, WHITE, lt), scale * S, seed, stretch, contrast)
    a = np.asarray(t, np.float32); h, w = a.shape[:2]; yy = np.linspace(-1, 1, h)[:, None]; xx = np.linspace(-1, 1, w)[None, :]
    lit = (1 + k * (.55 * -xx + .8 * -yy) * .55) * (1 - rim * np.clip(xx ** 2 + yy ** 2 - .35, 0, 1.2))
    a[..., :3] *= lit[..., None]
    if spec: a[..., :3] += (np.exp(-(((xx + .35) / .25) ** 2 + ((yy + .45) / .2) ** 2)) * spec * 255)[..., None]
    img.alpha_composite(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA'), box[:2])
    return m


def clipped(img, m, fn, alpha=1.0):
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(l), l)
    a = np.asarray(l, np.float32); a[..., 3] *= np.asarray(m, np.float32) / 255 * alpha
    img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))


def poly_s(d, pts, col, n=8):
    d.polygon([(px(x), px(y)) for x, y in cr(pts, n)], fill=col)


def flower(d, x, y, r, col, center=(232, 196, 80, 255), n=5):
    for p in range(n):
        a = p / n * math.tau - math.pi / 2
        d.ellipse([px(x + math.cos(a) * r - r * .62), px(y + math.sin(a) * r - r * .62), px(x + math.cos(a) * r + r * .62), px(y + math.sin(a) * r + r * .62)], fill=col)
    d.ellipse([px(x - r * .35), px(y - r * .35), px(x + r * .35), px(y + r * .35)], fill=center)


def kimono_pattern(img, m, seed, count, box, cols=((244, 236, 222, 235), (238, 172, 190, 235))):
    rnd = random.Random(seed)
    def fn(d, l):
        for _ in range(count):
            x, y = rnd.uniform(box[0], box[2]), rnd.uniform(box[1], box[3]); r = rnd.uniform(4, 7)
            flower(d, x, y, r, rnd.choice(cols))
        for _ in range(count // 3):
            x, y = rnd.uniform(box[0], box[2]), rnd.uniform(box[1], box[3]); d.arc([px(x - 9), px(y - 9), px(x + 9), px(y + 9)], 200, 340, fill=(216, 178, 90, 200), width=px(1.6))
    clipped(img, m, fn)


def folds(img, m, lines, col=(0, 0, 0, 70), w=3):
    def fn(d, l):
        for pts in lines: d.line([(px(x), px(y)) for x, y in cr(pts, 8, False)], fill=col, width=px(w))
    l2 = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(l2), l2); l2 = l2.filter(ImageFilter.GaussianBlur(2 * S))
    a = np.asarray(l2, np.float32); a[..., 3] *= np.asarray(m, np.float32) / 255; img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))


def hair_texture(img, m, seed, roots, length, count, gravity=.05, sway=.1, width=(1, 2), col=(46, 42, 44)):
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); hair(l, roots, length, count, seed, sway=sway, col=col, width=width, gravity=gravity)
    a = np.asarray(l.filter(ImageFilter.GaussianBlur(.4 * S)), np.float32); a[..., 3] *= np.asarray(m, np.float32) / 255 * .8
    img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))


def face_kid(img, cx, cy, rx, ry, seed):
    shape(img, (240, 232, 222, 255), seed, ell=(cx - rx, cy - ry, cx + rx, cy + ry), scale=10, contrast=.35, dk=.2, lt=.1, k=.35, rim=.25)
    soft(img, lambda d: [d.ellipse([px(cx - rx * .78), px(cy + ry * .18), px(cx - rx * .34), px(cy + ry * .46)], fill=(232, 130, 140, 80)),
                         d.ellipse([px(cx + rx * .34), px(cy + ry * .18), px(cx + rx * .78), px(cy + ry * .46)], fill=(232, 130, 140, 80))], 4)


# ───────────── Zashiki-warashi, the child spirit of the house ─────────────
RED, RED_D = hexc('#b3302b'), hexc('#8e2422')
BLK = (16, 14, 15, 255)


def warashi():
    img = canvas(300, 640)
    body = [(118, 238), (150, 234), (182, 238), (206, 266), (214, 340), (222, 450), (232, 598), (150, 610), (68, 598), (78, 450), (86, 340), (94, 266)]
    mb = shape(img, RED, 31, body, scale=24, stretch=(1, 3), contrast=1.1, dk=.45, lt=.12, k=.35, rim=.3)
    kimono_pattern(img, mb, 5, 22, (80, 430, 222, 600)); folds(img, mb, [[(120, 430), (112, 520), (108, 600)], [(182, 430), (188, 520), (196, 600)], [(150, 440), (152, 600)]])
    for sx in (-1, 1):   # long furisode sleeves
        sl = [(150 + sx * 52, 252), (150 + sx * 84, 268), (150 + sx * 100, 320), (150 + sx * 104, 470), (150 + sx * 94, 506), (150 + sx * 58, 504), (150 + sx * 48, 470), (150 + sx * 46, 320)]
        ms = shape(img, RED, 32 + sx, sl, scale=20, stretch=(1, 3), contrast=1.1, dk=.45, lt=.12, k=.5, rim=.35)
        kimono_pattern(img, ms, 6 + sx, 10, (150 + min(sx * 104, sx * 46), 380, 150 + max(sx * 104, sx * 46), 500))
    d = ImageDraw.Draw(img)
    poly_s(d, [(124, 238), (150, 312), (176, 238), (166, 238), (150, 288), (134, 238)], (240, 234, 222, 255), 4)
    obi = [(86, 368), (214, 368), (216, 424), (84, 424)]
    mo = shape(img, hexc('#e6d6b4'), 34, obi, scale=6, contrast=.8, dk=.3, lt=.15, k=.3, rim=.15, smooth=False)
    clipped(img, mo, lambda dd, l: [dd.line([(px(84), px(y)), (px(216), px(y))], fill=(190, 150, 80, 220), width=px(2)) for y in (380, 412)])
    d.rounded_rectangle([px(84), px(392), px(216), px(399)], px(3), fill=hexc('#c43a2a'))
    for x in (108, 178):   # tabi + geta
        d.rounded_rectangle([px(x - 17), px(600), px(x + 17), px(622)], px(8), fill=(238, 232, 220, 255))
        d.rounded_rectangle([px(x - 21), px(620), px(x + 21), px(630)], px(3), fill=hexc('#2a1c14'))
    # temari cupped in both hands
    shape(img, hexc('#c02a2a'), 35, ell=(124, 446, 176, 498), scale=4, contrast=.5, k=.6, rim=.5, spec=.25)
    def tem(dd, l):
        for kk in range(6):
            a = kk / 6 * math.pi; dd.line([(px(150 + math.cos(a) * 25), px(472 + math.sin(a) * 25)), (px(150 - math.cos(a) * 25), px(472 - math.sin(a) * 25))], fill=(242, 236, 216, 230), width=px(1.6))
        dd.ellipse([px(138), px(460), px(162), px(484)], outline=(230, 190, 70, 240), width=px(2.4))
    clipped(img, mask_of(img, ell=(124, 446, 176, 498), feather=0), tem)
    for hx in (124, 176): shape(img, (236, 226, 212, 255), 36, ell=(hx - 13, 462, hx + 13, 486), scale=6, contrast=.3, k=.4, rim=.3)
    shape(img, (230, 220, 206, 255), 37, [(132, 212), (168, 212), (170, 246), (130, 246)], scale=8, contrast=.3, k=.3, rim=.2)   # neck
    # hair back, face, bangs, side locks
    hb = shape(img, BLK, 38, [(84, 238), (80, 170), (88, 112), (116, 80), (150, 72), (184, 80), (212, 112), (220, 170), (216, 238)], scale=6, contrast=.6, dk=.2, lt=.12, k=.3, rim=.1)
    hair_texture(img, hb, 42, [(150 + x, 78, 0) for x in range(-64, 65, 5)], 160, 150)
    face_kid(img, 150, 174, 54, 64, 39)
    bangs = [(92, 152), (94, 112), (118, 84), (150, 78), (182, 84), (206, 112), (208, 152), (180, 154), (150, 155), (120, 154)]
    mb2 = shape(img, BLK, 40, bangs, scale=6, contrast=.6, dk=.2, lt=.12, k=.3, rim=.1)
    for sx in (-1, 1): shape(img, BLK, 41 + sx, [(150 + sx * 66, 140), (150 + sx * 52, 150), (150 + sx * 50, 236), (150 + sx * 68, 238)], scale=6, contrast=.6, dk=.2, lt=.12, k=.2, rim=.05, feather=.5)
    hair_texture(img, mb2, 43, [(150 + x, 80, 0) for x in range(-56, 57, 4)], 76, 120)
    soft(img, lambda dd: dd.arc([px(108), px(82), px(170), px(128)], 200, 300, fill=(120, 116, 118, 120), width=px(5)), 2)    # sheen
    d = ImageDraw.Draw(img)
    for ex in (130, 170):
        d.ellipse([px(ex - 9), px(172), px(ex + 9), px(190)], fill=(22, 14, 12, 255)); d.ellipse([px(ex - 5), px(174), px(ex - 1), px(179)], fill=(255, 255, 255, 220))
        d.arc([px(ex - 11), px(166), px(ex + 11), px(184)], 200, 340, fill=(30, 20, 18, 255), width=px(2))
    d.arc([px(140), px(206), px(160), px(216)], 20, 160, fill=(170, 40, 46, 255), width=px(3))
    save(img, 'm_warashi')


def warashi_back():
    img = canvas(280, 620)
    for sx in (-1, 1):
        sl = [(140 + sx * 50, 244), (140 + sx * 80, 260), (140 + sx * 96, 312), (140 + sx * 100, 460), (140 + sx * 90, 494), (140 + sx * 56, 492), (140 + sx * 46, 460), (140 + sx * 44, 312)]
        ms = shape(img, RED_D, 50 + sx, sl, scale=20, stretch=(1, 3), contrast=1.1, dk=.45, lt=.12)
        kimono_pattern(img, ms, 51 + sx, 8, (140 + min(sx * 100, sx * 44), 380, 140 + max(sx * 100, sx * 44), 490))
    body = [(108, 232), (140, 228), (172, 232), (196, 260), (204, 332), (212, 440), (222, 590), (140, 600), (58, 590), (68, 440), (76, 332), (84, 260)]
    mb = shape(img, RED, 52, body, scale=24, stretch=(1, 3), contrast=1.1, dk=.45, lt=.12, k=.35, rim=.3)
    kimono_pattern(img, mb, 53, 20, (70, 430, 212, 590)); folds(img, mb, [[(112, 440), (104, 590)], [(170, 440), (178, 590)]])
    mo = shape(img, hexc('#e6d6b4'), 54, [(76, 356), (204, 356), (206, 400), (74, 400)], scale=6, contrast=.8, dk=.3, lt=.15, k=.3, rim=.15, smooth=False)
    shape(img, hexc('#e6d6b4'), 55, [(94, 322), (186, 322), (196, 372), (188, 428), (92, 428), (84, 372)], scale=6, contrast=.8, dk=.3, lt=.15, k=.45, rim=.3)   # taiko bow
    d = ImageDraw.Draw(img); d.rounded_rectangle([px(74), px(374), px(206), px(381)], px(3), fill=hexc('#c43a2a'))
    for x, y in ((118, 592), (166, 578)):
        d.rounded_rectangle([px(x - 16), px(y), px(x + 16), px(y + 20)], px(8), fill=(238, 232, 220, 255)); d.rounded_rectangle([px(x - 20), px(y + 18), px(x + 20), px(y + 27)], px(3), fill=hexc('#2a1c14'))
    hb = shape(img, BLK, 56, [(76, 232), (72, 160), (82, 102), (110, 72), (140, 64), (170, 72), (198, 102), (208, 160), (204, 232), (140, 238)], scale=6, contrast=.6, dk=.2, lt=.12, k=.4, rim=.15)
    hair_texture(img, hb, 57, [(140 + x, 70, 0) for x in range(-62, 63, 4)], 170, 220)
    soft(img, lambda dd: dd.arc([px(96), px(78), px(170), px(150)], 200, 300, fill=(120, 116, 118, 110), width=px(6)), 3)
    save(img, 'm_warashi_back')


# ───────────── Akaname: licks the grime of neglected baths ─────────────
def akaname():
    img = canvas(380, 440)
    red, redd = hexc('#a9412e'), hexc('#7e2c20')
    for sx in (-1, 1):   # squatting legs and the one-clawed feet
        shape(img, redd, 60 + sx, [(190 + sx * 70, 330), (190 + sx * 118, 360), (190 + sx * 126, 410), (190 + sx * 104, 426), (190 + sx * 70, 410), (190 + sx * 58, 370)], scale=8, k=.5)
        d = ImageDraw.Draw(img); poly_s(d, [(190 + sx * 118, 418), (190 + sx * 152, 424), (190 + sx * 164, 436), (190 + sx * 140, 432), (190 + sx * 116, 428)], (230, 220, 196, 255), 4)
    shape(img, red, 62, [(128, 250), (190, 232), (252, 250), (292, 314), (286, 380), (240, 404), (140, 404), (94, 380), (88, 314)], scale=10, k=.55, rim=.4)
    for sx in (-1, 1):   # thin arms resting on the knees, three claws
        shape(img, redd, 63 + sx, [(190 + sx * 58, 262), (190 + sx * 94, 292), (190 + sx * 108, 348), (190 + sx * 96, 354), (190 + sx * 82, 306), (190 + sx * 52, 280)], scale=7, k=.5, feather=.5)
        d = ImageDraw.Draw(img)
        for c in range(3): poly_s(d, [(190 + sx * (94 + c * 6), 350), (190 + sx * (98 + c * 7), 370), (190 + sx * (90 + c * 6), 356)], (230, 220, 196, 255), 3)
    # wild hair: spiky tufts around the crown
    rnd = random.Random(64); d = ImageDraw.Draw(img)
    for k in range(26):
        a = math.pi * (1.02 + .96 * k / 25); L = rnd.uniform(40, 86); w = rnd.uniform(.08, .14)
        bx, by = 190 + math.cos(a) * 82, 176 + math.sin(a) * 76
        poly_s(d, [(bx + math.cos(a + math.pi / 2) * 14, by + math.sin(a + math.pi / 2) * 14), (bx + math.cos(a) * L, by + math.sin(a) * L), (bx + math.cos(a - math.pi / 2) * 14, by + math.sin(a - math.pi / 2) * 14)], (22 + rnd.randint(0, 16), 16, 14, 255), 3)
    shape(img, hexc('#b44a34'), 65, ell=(94, 96, 286, 266), scale=8, k=.6, rim=.45)
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        ex = 190 + sx * 36
        d.ellipse([px(ex - 20), px(148), px(ex + 20), px(180)], fill=hexc('#ead65a')); d.ellipse([px(ex - 6), px(154), px(ex + 6), px(174)], fill=(20, 10, 6, 255))
        d.ellipse([px(ex - 20), px(148), px(ex + 20), px(180)], outline=(90, 30, 20, 255), width=px(2))
        poly_s(d, [(190 + sx * 12, 142), (190 + sx * 58, 128), (190 + sx * 60, 140), (190 + sx * 16, 150)], (26, 12, 10, 255), 3)
    for sx in (-1, 1): d.ellipse([px(190 + sx * 8 - 4), px(192), px(190 + sx * 8 + 4), px(200)], fill=(60, 20, 16, 255))
    poly_s(d, [(136, 214), (190, 206), (244, 214), (232, 244), (190, 256), (148, 244)], (46, 10, 10, 255), 6)
    for k in range(6): d.polygon([(px(146 + k * 18), px(214)), (px(156 + k * 18), px(214)), (px(151 + k * 18), px(228))], fill=(236, 228, 206, 255))
    tongue = [(178, 236), (204, 236), (220, 280), (240, 330), (272, 376), (312, 400), (330, 388), (318, 410), (282, 414), (240, 388), (206, 336), (186, 284)]
    mt = shape(img, hexc('#d9606e'), 66, tongue, scale=5, contrast=.7, dk=.3, lt=.25, k=.4, rim=.3, spec=.25)
    clipped(img, mt, lambda dd, l: dd.line([(px(x), px(y)) for x, y in cr([(191, 240), (204, 290), (226, 340), (262, 384), (300, 404)], 8, False)], fill=(160, 50, 62, 220), width=px(2.4)))
    save(img, 'm_akaname')


# ───────────── Kappa ─────────────
def kappa():
    img = canvas(340, 480)
    g, gd = hexc('#56834a'), hexc('#3e6436')
    ms = shape(img, hexc('#5e5030'), 70, [(94, 196), (170, 176), (246, 196), (290, 280), (286, 360), (246, 410), (170, 420), (94, 410), (54, 360), (50, 280)], scale=8, contrast=1.3, k=.5)
    clipped(img, ms, lambda dd, l: [dd.line([(px(x0), px(y0)), (px(x1), px(y1))], fill=(40, 32, 18, 200), width=px(3)) for x0, y0, x1, y1 in ((60, 290, 110, 250), (280, 290, 230, 250), (56, 360, 104, 380), (284, 360, 236, 380))])
    for sx in (-1, 1):   # legs and webbed feet
        shape(img, gd, 71 + sx, [(170 + sx * 22, 384), (170 + sx * 52, 390), (170 + sx * 58, 440), (170 + sx * 40, 452), (170 + sx * 22, 440)], scale=7, k=.5)
        shape(img, gd, 73 + sx, [(170 + sx * 20, 446), (170 + sx * 44, 440), (170 + sx * 76, 458), (170 + sx * 70, 470), (170 + sx * 16, 470)], scale=6, k=.4)
    shape(img, g, 75, [(126, 200), (170, 190), (214, 200), (244, 256), (250, 330), (232, 388), (170, 402), (108, 388), (90, 330), (96, 256)], scale=9, k=.55, rim=.4)
    mp = shape(img, hexc('#cdbb72'), 76, [(138, 236), (170, 230), (202, 236), (218, 296), (210, 364), (170, 382), (130, 364), (122, 296)], scale=6, contrast=.8, k=.4, rim=.3)
    clipped(img, mp, lambda dd, l: [dd.line([(px(120), px(y)), (px(220), px(y))], fill=(140, 120, 60, 220), width=px(2)) for y in (270, 300, 330, 356)])
    for sx in (-1, 1):   # arms and webbed hands
        shape(img, g, 77 + sx, [(170 + sx * 64, 214), (170 + sx * 100, 250), (170 + sx * 116, 320), (170 + sx * 104, 330), (170 + sx * 84, 270), (170 + sx * 56, 236)], scale=7, k=.5)
        shape(img, gd, 79 + sx, [(170 + sx * 100, 318), (170 + sx * 134, 334), (170 + sx * 128, 354), (170 + sx * 110, 360), (170 + sx * 96, 344)], scale=5, k=.4)
    shape(img, hexc('#5f8e50'), 81, ell=(92, 64, 248, 200), scale=8, k=.6, rim=.45)
    rnd = random.Random(82); d = ImageDraw.Draw(img)
    for k in range(30):   # the fringe of hair around the dish
        a = math.pi * (1.0 + k / 29); bx, by = 170 + math.cos(a) * 64, 84 + math.sin(a) * 24
        poly_s(d, [(bx - 7, by), (bx + math.cos(a) * rnd.uniform(18, 30), by + 22 + rnd.uniform(0, 14)), (bx + 7, by)], (22, 28, 20, 255), 3)
    shape(img, hexc('#d8d0b0'), 83, ell=(118, 60, 222, 92), scale=5, k=.3, rim=.2)
    shape(img, hexc('#7fb0bf'), 84, ell=(128, 64, 212, 86), scale=4, contrast=.5, k=.3, rim=.2, spec=.5)
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        ex = 170 + sx * 34
        d.ellipse([px(ex - 20), px(104), px(ex + 20), px(138)], fill=hexc('#efe6a8')); d.ellipse([px(ex - 20), px(104), px(ex + 20), px(138)], outline=(40, 60, 30, 255), width=px(2))
        d.ellipse([px(ex - 6), px(112), px(ex + 6), px(132)], fill=(16, 12, 8, 255)); d.ellipse([px(ex - 4), px(113), px(ex), px(118)], fill=(255, 255, 255, 220))
    shape(img, hexc('#d8a83c'), 85, [(144, 146), (170, 142), (196, 146), (190, 170), (170, 186), (150, 170)], scale=5, contrast=.8, k=.5, rim=.3, spec=.2)
    save(img, 'm_kappa')


# ───────────── Kitsune bride ─────────────
def kitsune():
    img = canvas(400, 450)
    w, wd, cream = hexc('#efe9dd'), hexc('#d8d0c0'), hexc('#f8f4ec')
    mt = shape(img, w, 90, [(250, 438), (318, 440), (366, 414), (390, 360), (380, 300), (352, 270), (338, 300), (352, 350), (338, 392), (296, 410), (250, 404)], scale=10, contrast=.7, k=.5, rim=.35)
    clipped(img, mt, lambda dd, l: dd.ellipse([px(330), px(250), px(400), px(330)], fill=(242, 230, 204, 255)))
    clipped(img, mt, lambda dd, l: [dd.arc([px(x - 16), px(y - 10), px(x + 16), px(y + 10)], 200, 340, fill=(200, 190, 170, 180), width=px(1.4)) for x, y in ((300, 420), (340, 408), (366, 380), (372, 340))])
    shape(img, w, 91, [(200, 226), (252, 246), (280, 318), (286, 400), (262, 436), (138, 436), (114, 400), (120, 318), (148, 246)], scale=10, contrast=.7, k=.5, rim=.4)
    mc = shape(img, cream, 92, [(170, 248), (200, 244), (230, 248), (244, 300), (222, 352), (200, 372), (178, 352), (156, 300)], scale=8, contrast=.5, k=.3, rim=.2)
    rnd = random.Random(93)
    clipped(img, mc, lambda dd, l: [dd.arc([px(x - 12), px(y - 8), px(x + 12), px(y + 8)], 20, 160, fill=(200, 190, 170, 200), width=px(1.4)) for x, y in [(rnd.uniform(166, 234), rnd.uniform(260, 360)) for _ in range(26)]])
    for x in (170, 230):
        shape(img, wd, x, [(x - 13, 320), (x + 13, 320), (x + 14, 426), (x + 18, 438), (x - 16, 438), (x - 12, 426)], scale=6, contrast=.5, k=.4, rim=.3, feather=.5)
    for sx in (-1, 1):   # ears
        shape(img, w, 94 + sx, [(200 + sx * 40, 100), (200 + sx * 70, 20), (200 + sx * 92, 112)], scale=6, contrast=.6, k=.4)
        d = ImageDraw.Draw(img); poly_s(d, [(200 + sx * 54, 100), (200 + sx * 70, 40), (200 + sx * 82, 106)], (70, 50, 46, 255), 4)
    head = [(200, 70), (240, 84), (272, 118), (290, 160), (262, 190), (228, 214), (200, 242), (172, 214), (138, 190), (110, 160), (128, 118), (160, 84)]
    shape(img, w, 96, head, scale=8, contrast=.6, k=.5, rim=.35)
    shape(img, cream, 97, [(176, 176), (200, 170), (224, 176), (216, 222), (200, 240), (184, 222)], scale=6, contrast=.4, k=.3, rim=.2)
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        poly_s(d, [(200 + sx * 16, 150), (200 + sx * 40, 134), (200 + sx * 70, 128), (200 + sx * 44, 146)], (192, 38, 38, 255), 5)
        d.arc([px(200 + sx * 40 - 18), px(134), px(200 + sx * 40 + 18), px(158)], 200, 340, fill=(30, 20, 14, 255), width=px(4))
        poly_s(d, [(200 + sx * 6, 112), (200 + sx * 14, 88), (200 + sx * 22, 110)], (192, 38, 38, 255), 4)
        for kk in range(3): d.line([(px(200 + sx * 24), px(206 + kk * 5)), (px(200 + sx * 60), px(198 + kk * 9))], fill=(150, 140, 130, 200), width=px(1))
    d.ellipse([px(192), px(230), px(208), px(242)], fill=(20, 14, 12, 255))
    # white bridal hood between the ears
    shape(img, hexc('#fbfaf6'), 98, [(146, 104), (158, 66), (200, 54), (242, 66), (254, 104), (228, 92), (200, 88), (172, 92)], scale=5, contrast=.3, dk=.15, lt=.05, k=.3, rim=.15)
    d = ImageDraw.Draw(img); d.line([(px(x), px(y)) for x, y in cr([(150, 100), (200, 84), (250, 100)], 8, False)], fill=(208, 176, 96, 255), width=px(2))
    d = ImageDraw.Draw(img); d.line([(px(x), px(y)) for x, y in cr([(156, 250), (200, 266), (244, 250)], 8, False)], fill=(192, 38, 38, 255), width=px(5))
    shape(img, hexc('#d8b048'), 99, ell=(188, 262, 212, 286), scale=4, contrast=1.2, k=.7, rim=.4, spec=.45)
    d = ImageDraw.Draw(img); d.line([(px(190), px(274)), (px(210), px(274))], fill=(110, 80, 20, 255), width=px(1.4)); d.ellipse([px(197), px(276), px(203), px(282)], fill=(60, 40, 10, 255))
    save(img, 'm_kitsune')


# ───────────── Big chōchin-obake ─────────────
def obake():
    img = canvas(280, 440)
    d = ImageDraw.Draw(img); d.line([(px(140), 0), (px(140), px(40))], fill=(18, 12, 9, 255), width=px(3))
    m = shape(img, hexc('#e2d0a4'), 81, ell=(18, 44, 262, 420), scale=6, contrast=1.1, k=.5, rim=.45)
    clipped(img, m, lambda dd, l: [dd.line([(px(0), px(44 + 376 * k / 15)), (px(280), px(44 + 376 * k / 15))], fill=(90, 70, 40, 180), width=px(2.4)) for k in range(1, 15)])
    d = ImageDraw.Draw(img)
    poly_s(d, [(60, 116), (84, 146), (70, 176), (64, 148)], (40, 20, 14, 255), 3)
    ex, ey, r = 140, 170, 44
    d.ellipse([px(ex - r), px(ey - r * .75), px(ex + r), px(ey + r * .75)], fill=hexc('#f6f0e0')); d.ellipse([px(ex - r), px(ey - r * .75), px(ex + r), px(ey + r * .75)], outline=hexc('#8a1a1a'), width=px(3))
    d.ellipse([px(ex - r * .42), px(ey - r * .42), px(ex + r * .42), px(ey + r * .42)], fill=(24, 12, 8, 255)); d.ellipse([px(ex - 12), px(ey - 16), px(ex - 2), px(ey - 6)], fill=(255, 255, 255, 230))
    poly_s(d, [(40, 272), (140, 256), (240, 254), (228, 306), (140, 322), (56, 322)], (36, 10, 8, 255), 6)
    for k in range(9): d.polygon([(px(52 + k * 20), px(270 - k * 1.6)), (px(64 + k * 20), px(270 - k * 1.6)), (px(58 + k * 20), px(286 - k * 1.6))], fill=hexc('#efe6cc'))
    shape(img, hexc('#c83a44'), 82, [(120, 292), (166, 292), (182, 360), (168, 410), (148, 432), (138, 396), (126, 350)], scale=5, contrast=.8, dk=.35, lt=.25, k=.4, rim=.3, spec=.2)
    d = ImageDraw.Draw(img)
    for y in (36, 412): d.rounded_rectangle([px(70), px(y), px(210), px(y + 18)], px(4), fill=(20, 13, 9, 255))
    save(img, 'm_obake')


if __name__ == '__main__':
    for f in (warashi, warashi_back, akaname, kappa, kitsune, obake): f()
    json.dump(M.META, open(f'{M.OUT}/story_chars.json', 'w'))
