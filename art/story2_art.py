#!/usr/bin/env python3
"""Second story «Кошачья гора»: the old cat king of Nekodake (a huge grey bakeneko with a torn ear, a staff and a lantern),
Akari the lantern-bearer kitten, and 7 relics packed into one atlas. Same organic spline toolkit as story_art.py.
Usage: story2_art.py <mondir> <itemdir>   (assets/mon assets/items) → m_s2_king.webp, m_s2_akari.webp, atlas_s2.webp; prints the rect map."""
import json, math, random, sys
MON_DIR, ITEM_DIR = sys.argv[1], sys.argv[2]
sys.argv = [sys.argv[0], MON_DIR]          # monsters/items read their output dir from argv[1]
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc
import monsters as M
from monsters import canvas, px, soft, save
from story_art import cr, mask_of, shape, clipped, poly_s, folds
from guests_art import stroke, tube, fur_ticks
import items as I
from items import text, SERIF

BLACK, WHITE = (0, 0, 0, 255), (255, 255, 255, 255)


def glow(img, x, y, r, col, a=150):
    soft(img, lambda d: [d.ellipse([px(x - r * k), px(y - r * k), px(x + r * k), px(y + r * k)], fill=col[:3] + (int(a * (1.1 - k)),)) for k in (1, .7, .45)], r * .35)


def chochin(img, x, y0, w, h, seed, paper='#f2c572', kanji=None):
    """A small round paper lantern hanging from (x, y0), lit from inside."""
    glow(img, x, y0 + h / 2, w * 1.25, hexc('#ffb454'), 120)
    m = shape(img, hexc(paper), seed, ell=(x - w / 2, y0 + 6, x + w / 2, y0 + h - 6), scale=4, contrast=.5, dk=.18, lt=.35, k=-.2, rim=.25, spec=.15)
    clipped(img, m, lambda d, l: [d.arc([px(x - w / 2), px(y0 + 6 + k * (h - 12) / 7 - 3), px(x + w / 2), px(y0 + 6 + k * (h - 12) / 7 + 3)], 0, 180, fill=(150, 90, 40, 150), width=px(1.2)) for k in range(1, 7)])
    soft(img, lambda d: d.ellipse([px(x - w * .28), px(y0 + h * .3), px(x + w * .28), px(y0 + h * .7)], fill=(255, 240, 190, 120)), w * .12)
    if kanji: text(img, kanji, x, y0 + h / 2 + 1, w * .42, '#7a2a18', SERIF)
    d = ImageDraw.Draw(img)
    for yy in (y0, y0 + h - 8): d.rounded_rectangle([px(x - w * .3), px(yy), px(x + w * .3), px(yy + 8)], px(2), fill=(26, 18, 14, 255))


# ───────────── Neko-no-ō: the old cat king of Nekodake ─────────────
def king():
    img = canvas(520, 600)
    grey, grey_d, grey_l, cream = hexc('#8a8c8c'), hexc('#5f6264'), hexc('#a9aaa6'), hexc('#dcd6c8')
    cx = 280
    # two old tails curling on the ground to the right, ringed with dark grey
    for i, (pts, w0, w1) in enumerate((([(340, 560), (410, 572), (466, 548), (498, 496), (492, 444), (470, 420)], 24, 15),
                                       ([(330, 578), (400, 590), (462, 586), (504, 560), (514, 522)], 22, 14))):
        mt = shape(img, grey if i else grey_l, 201 + i, tube(pts, w0, w1), scale=8, contrast=.9, k=.5, rim=.35)
        clipped(img, mt, lambda d, l, pp=pts: [d.line([(px(x - 20), px(y - 18)), (px(x + 20), px(y + 18))], fill=(60, 62, 64, 190), width=px(9)) for x, y in pp[1:-1]])
        fur_ticks(img, mt, 203 + i, (330, 410, 516, 596), 60, (70, 70, 72, 110))
    # haunches and the big sitting body
    for sx in (-1, 1): shape(img, grey_d, 205 + sx, ell=(cx + sx * 70 - 70, 440, cx + sx * 70 + 70, 596), scale=9, k=.5, rim=.4)
    body = [(cx, 244), (cx + 70, 262), (cx + 112, 330), (cx + 128, 430), (cx + 118, 540), (cx + 70, 584), (cx, 592), (cx - 70, 584), (cx - 118, 540), (cx - 128, 430), (cx - 112, 330), (cx - 70, 262)]
    mb = shape(img, grey, 207, body, scale=11, contrast=.9, dk=.45, lt=.2, k=.5, rim=.4)
    clipped(img, mb, lambda d, l: [stroke(d, [(cx + sx * 124, y), (cx + sx * 96, y + 14), (cx + sx * 70, y + 40)], (72, 74, 76, 170), 11) for sx in (-1, 1) for y in (330, 390, 450, 510)])
    fur_ticks(img, mb, 208, (cx - 128, 250, cx + 128, 590), 380, (58, 60, 62, 110), (5, 12))
    fur_ticks(img, mb, 209, (cx - 128, 250, cx + 128, 590), 160, (200, 200, 196, 70), (4, 9))
    # long cream chest ruff, ragged at the bottom
    ruff = [(cx - 62, 270), (cx, 262), (cx + 62, 270), (cx + 70, 330), (cx + 50, 400), (cx + 34, 440), (cx + 16, 420), (cx, 468), (cx - 16, 420), (cx - 34, 440), (cx - 50, 400), (cx - 70, 330)]
    mr = shape(img, cream, 210, ruff, scale=7, contrast=.6, dk=.3, lt=.1, k=.4, rim=.25)
    fur_ticks(img, mr, 211, (cx - 70, 262, cx + 70, 468), 170, (160, 150, 136, 120), (6, 14), 1.57)
    # right front leg down to the paw (viewer's right)
    shape(img, grey, 212, [(cx + 30, 400), (cx + 72, 400), (cx + 78, 560), (cx + 26, 566)], scale=8, k=.5, rim=.35)
    shape(img, cream, 213, ell=(cx + 14, 546, cx + 92, 596), scale=5, contrast=.5, k=.4, rim=.3)
    d = ImageDraw.Draw(img)
    for t in range(3): d.line([(px(cx + 36 + t * 14), px(574)), (px(cx + 36 + t * 14), px(594))], fill=(120, 110, 100, 200), width=px(1.4))
    # the staff: gnarled wood with a crook; a lantern hangs from it
    stroke(d, [(64, 598), (60, 420), (66, 250), (60, 110), (70, 52), (98, 34), (122, 44)], (48, 32, 20, 255), 11)
    stroke(d, [(62, 590), (58, 420), (64, 250), (58, 112)], (92, 66, 40, 200), 4)
    for y in (180, 330, 470): d.ellipse([px(56), px(y), px(70), px(y + 10)], fill=(36, 24, 16, 255))
    stroke(d, [(122, 44), (122, 64)], (30, 20, 14, 255), 2)
    chochin(img, 122, 62, 58, 76, 214, kanji='王')
    # left front leg raised to the staff, the paw wrapped around it
    arm = tube([(cx - 60, 300), (cx - 120, 350), (cx - 170, 392), (cx - 200, 402)], 30, 24)
    ma = shape(img, grey, 215, arm, scale=8, k=.5, rim=.35)
    fur_ticks(img, ma, 216, (cx - 210, 300, cx - 50, 420), 80, (60, 62, 64, 110))
    shape(img, cream, 217, ell=(40, 376, 104, 424), scale=5, contrast=.5, k=.4, rim=.3)
    d = ImageDraw.Draw(img)
    for t in range(3): d.line([(px(52 + t * 14), px(380)), (px(56 + t * 14), px(396))], fill=(120, 110, 100, 210), width=px(1.4))
    # shimenawa: a thick straw rope round the neck with zigzag paper shide
    rope = [(cx - 96, 264), (cx, 292), (cx + 96, 264), (cx + 96, 286), (cx, 316), (cx - 96, 286)]
    mrp = shape(img, hexc('#c9ae6c'), 218, rope, scale=4, stretch=(2, 1), contrast=1.2, dk=.4, lt=.2, k=.4, rim=.2)
    clipped(img, mrp, lambda d, l: [d.line([(px(cx - 100 + k * 12), px(260)), (px(cx - 88 + k * 12), px(320))], fill=(120, 96, 50, 200), width=px(2.2)) for k in range(18)])
    for sx in (-.55, 0, .55):
        x0, y0 = cx + sx * 96, 300 - abs(sx) * 26 + 8
        I.poly(img, [(x0 - 8, y0), (x0 + 6, y0), (x0 + 6, y0 + 16), (x0 - 2, y0 + 16), (x0 + 10, y0 + 34), (x0 + 2, y0 + 34), (x0 + 12, y0 + 54), (x0 - 4, y0 + 54), (x0 - 10, y0 + 36), (x0 - 2, y0 + 36), (x0 - 12, y0 + 18), (x0 - 8, y0 + 18)], (246, 242, 230, 255))
    # head: ears (the left one torn), big cheek ruffs, heavy old face
    shape(img, grey, 219, [(cx - 50, 100), (cx - 92, 22), (cx - 110, 118)], scale=6, contrast=.8, k=.4)
    poly_s(ImageDraw.Draw(img), [(cx - 60, 100), (cx - 88, 44), (cx - 98, 110)], (170, 120, 116, 255), 4)
    torn = [(cx + 50, 100), (cx + 72, 52), (cx + 82, 70), (cx + 88, 48), (cx + 96, 24), (cx + 112, 118)]
    shape(img, grey, 220, torn, scale=6, contrast=.8, k=.4, smooth=False, feather=.5)
    poly_s(ImageDraw.Draw(img), [(cx + 62, 100), (cx + 76, 72), (cx + 84, 84), (cx + 92, 56), (cx + 100, 110)], (170, 120, 116, 255), 2)
    cheeks = [(cx, 80), (cx + 70, 92), (cx + 116, 140), (cx + 150, 196), (cx + 120, 214), (cx + 138, 236), (cx + 90, 254), (cx + 40, 270), (cx, 276),
              (cx - 40, 270), (cx - 90, 254), (cx - 138, 236), (cx - 120, 214), (cx - 150, 196), (cx - 116, 140), (cx - 70, 92)]
    mh = shape(img, grey, 221, cheeks, scale=9, contrast=.9, dk=.4, lt=.2, k=.55, rim=.35)
    clipped(img, mh, lambda d, l: [stroke(d, [(cx + sx * 20, 96), (cx + sx * 26, 120), (cx + sx * 22, 140)], (70, 72, 74, 200), 7) for sx in (-1, 0, 1)])
    fur_ticks(img, mh, 222, (cx - 150, 84, cx + 150, 276), 260, (62, 64, 66, 110), (4, 10))
    fur_ticks(img, mh, 223, (cx - 150, 190, cx + 150, 276), 110, (210, 208, 200, 90), (6, 14), 1.9)
    muz = shape(img, cream, 224, [(cx - 44, 196), (cx, 186), (cx + 44, 196), (cx + 52, 232), (cx, 262), (cx - 52, 232)], scale=6, contrast=.5, dk=.2, lt=.1, k=.4, rim=.2)
    fur_ticks(img, muz, 225, (cx - 52, 186, cx + 52, 262), 60, (170, 160, 146, 110), (3, 7), 1.6)
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):   # heavy-lidded eyes; the right one clouded
        ex, ey = cx + sx * 50, 166
        d.ellipse([px(ex - 24), px(ey - 16), px(ex + 24), px(ey + 16)], fill=hexc('#b9a868') if sx < 0 else hexc('#9fa8a6'))
        d.ellipse([px(ex - 4), px(ey - 13), px(ex + 4), px(ey + 13)], fill=(18, 14, 10, 255) if sx < 0 else (70, 78, 80, 255))
        d.ellipse([px(ex - 14), px(ey - 8), px(ex - 8), px(ey - 2)], fill=(255, 255, 255, 200))
        poly_s(d, [(ex - 28, ey - 20), (ex + 28, ey - 20), (ex + 28, ey - 3), (ex, ey - 7), (ex - 28, ey - 3)], grey_d, 4)   # the old lid
        d.arc([px(ex - 24), px(ey - 16), px(ex + 24), px(ey + 16)], 180, 360, fill=(40, 36, 32, 255), width=px(2.4))
        d.line([(px(ex - 26), px(ey + 4)), (px(ex + 26), px(ey + 4))], fill=(40, 36, 32, 180), width=px(2))
        for k in range(7):   # long white brows
            stroke(d, [(ex + sx * (-10 + k * 5), ey - 22), (ex + sx * (10 + k * 8), ey - 44 - k * 2), (ex + sx * (30 + k * 10), ey - 50 - k * 3)], (236, 234, 226, 200), 1.3)
    shape(img, hexc('#8a6a66'), 226, [(cx - 13, 204), (cx + 13, 204), (cx, 220)], scale=3, k=.3, rim=.1, smooth=False, feather=.4)
    d = ImageDraw.Draw(img)
    d.line([(px(cx), px(220)), (px(cx), px(230))], fill=(70, 50, 46, 255), width=px(2))
    d.arc([px(cx - 20), px(220), px(cx), px(240)], 20, 160, fill=(70, 50, 46, 255), width=px(2.2)); d.arc([px(cx), px(220), px(cx + 20), px(240)], 20, 160, fill=(70, 50, 46, 255), width=px(2.2))
    for sx in (-1, 1):   # long drooping whiskers
        for k in range(4):
            stroke(d, [(cx + sx * 34, 222 + k * 5), (cx + sx * 110, 226 + k * 12), (cx + sx * (180 + k * 8), 250 + k * 20)], (240, 238, 230, 210), 1.3)
    beard = [(cx - 26, 250), (cx + 26, 250), (cx + 16, 290), (cx + 4, 320), (cx - 6, 300), (cx - 18, 286)]
    mbd = shape(img, hexc('#e8e4da'), 227, beard, scale=5, contrast=.4, dk=.2, lt=.05, k=.3, rim=.2)
    fur_ticks(img, mbd, 228, (cx - 26, 250, cx + 26, 320), 50, (170, 164, 150, 120), (6, 12), 1.62)
    # the lantern's warm light on his left side
    lit = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(lit).ellipse([px(-120), px(-40), px(300), px(420)], fill=(255, 170, 80, 60))
    lit = lit.filter(ImageFilter.GaussianBlur(40 * M.S)); a = np.asarray(lit, np.float32); a[..., 3] *= np.asarray(img.getchannel('A'), np.float32) / 255
    img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))
    save(img, 'm_s2_king')


# ───────────── Akari, the lantern-bearer kitten ─────────────
def akari():
    img = canvas(320, 470)
    fur, fur_d, fur_l = hexc('#3a3436'), hexc('#241f21'), hexc('#5a5254')
    red, cx = hexc('#b3302b'), 196
    # tail curling up behind, the tip just starting to fork
    tl = tube([(240, 420), (282, 400), (300, 350), (292, 300), (300, 262)], 13, 9)
    mt = shape(img, fur, 301, tl, scale=6, contrast=.8, dk=.3, lt=.2, k=.5, rim=.35)
    for sx in (-1, 1): shape(img, fur, 302 + sx, tube([(300, 266), (300 + sx * 8, 248), (300 + sx * 14, 236)], 7, 4), scale=4, k=.4)
    # hind legs and feet
    for sx in (-1, 1):
        shape(img, fur_d, 305 + sx, [(cx + sx * 12, 400), (cx + sx * 46, 402), (cx + sx * 48, 446), (cx + sx * 14, 448)], scale=6, k=.5)
        shape(img, hexc('#e8e2d6'), 307 + sx, [(cx + sx * 8, 440), (cx + sx * 46, 438), (cx + sx * 58, 452), (cx + sx * 54, 466), (cx + sx * 6, 466)], scale=4, k=.4, rim=.3)
    body = [(cx - 40, 250), (cx, 240), (cx + 40, 250), (cx + 56, 320), (cx + 54, 400), (cx, 414), (cx - 54, 400), (cx - 56, 320)]
    shape(img, fur, 309, body, scale=7, contrast=.8, dk=.3, lt=.2, k=.5, rim=.4)
    # red happi jacket with a white crest: 灯, «light»
    hp = [(cx - 48, 250), (cx, 262), (cx + 48, 250), (cx + 66, 300), (cx + 60, 392), (cx - 60, 392), (cx - 66, 300)]
    mh = shape(img, red, 310, hp, scale=10, stretch=(1, 2), contrast=1.1, dk=.45, lt=.12, k=.4, rim=.3)
    folds(img, mh, [[(cx - 30, 300), (cx - 34, 390)], [(cx + 30, 300), (cx + 36, 390)]])
    d = ImageDraw.Draw(img)
    for sx in (-1, 1): stroke(d, [(cx + sx * 44, 252), (cx + sx * 8, 300), (cx + sx * 4, 392)], (236, 228, 212, 255), 7)
    d.ellipse([px(cx + 12), px(318), px(cx + 50), px(356)], fill=(240, 234, 222, 255))
    text(img, '灯', cx + 31, 338, 26, '#8e2422', SERIF)
    d = ImageDraw.Draw(img); d.rectangle([px(cx - 60), px(376), px(cx + 60), px(386)], fill=hexc('#2a1e18'))
    # bamboo pole held in both paws, the lantern hangs at its tip
    stroke(d, [(cx + 20, 380), (cx - 30, 280), (110, 150), (62, 70), (54, 48)], (70, 88, 44, 255), 7)
    stroke(d, [(cx + 18, 376), (cx - 32, 278), (108, 150), (60, 72)], (140, 160, 90, 200), 2.4)
    for t in (.3, .55, .8):
        x, y = cx + 20 + (54 - cx - 20) * t, 380 + (48 - 380) * t; d.line([(px(x - 5), px(y + 2)), (px(x + 5), px(y - 2))], fill=(50, 64, 30, 255), width=px(2))
    stroke(d, [(54, 48), (54, 70)], (30, 20, 14, 255), 2)
    chochin(img, 54, 68, 70, 88, 311, kanji='猫')
    for sx, (x, y) in ((-1, (cx - 20, 300)), (1, (cx + 4, 348))):   # sleeves and paws on the pole
        sl = tube([(cx + (-44 if sx < 0 else 40), 266), ((cx + x) / 2 + 10, (266 + y) / 2), (x + 8, y)], 17, 13)
        shape(img, red, 312 + sx, sl, scale=8, contrast=1.0, dk=.45, lt=.12, k=.4, rim=.3)
        shape(img, hexc('#ece6da'), 314 + sx, ell=(x - 16, y - 14, x + 12, y + 14), scale=4, k=.4, rim=.3)
    # head: kitten proportions, big ears, big green eyes
    for sx in (-1, 1):
        shape(img, fur, 316 + sx, [(cx + sx * 30, 124), (cx + sx * 74, 40), (cx + sx * 86, 136)], scale=5, k=.4)
        poly_s(ImageDraw.Draw(img), [(cx + sx * 42, 122), (cx + sx * 70, 64), (cx + sx * 78, 128)], (170, 110, 116, 255), 4)
    head = [(cx, 96), (cx + 56, 106), (cx + 86, 146), (cx + 90, 190), (cx + 64, 230), (cx, 248), (cx - 64, 230), (cx - 90, 190), (cx - 86, 146), (cx - 56, 106)]
    mhd = shape(img, fur, 318, head, scale=7, contrast=.8, dk=.3, lt=.2, k=.55, rim=.35)
    fur_ticks(img, mhd, 319, (cx - 90, 100, cx + 90, 246), 90, (90, 82, 84, 110), (3, 7))
    shape(img, hexc('#e8e2d6'), 320, [(cx - 26, 196), (cx, 186), (cx + 26, 196), (cx + 30, 222), (cx, 240), (cx - 30, 222)], scale=5, contrast=.4, k=.3, rim=.2)
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        ex, ey = cx + sx * 38, 170
        d.ellipse([px(ex - 22), px(ey - 22), px(ex + 22), px(ey + 22)], fill=hexc('#a9d46e'))
        d.ellipse([px(ex - 22), px(ey - 22), px(ex + 22), px(ey + 22)], outline=(20, 30, 14, 255), width=px(2))
        d.ellipse([px(ex - 12), px(ey - 16), px(ex + 12), px(ey + 18)], fill=(12, 14, 10, 255))
        d.ellipse([px(ex - 11), px(ey - 13), px(ex - 3), px(ey - 5)], fill=(255, 255, 255, 235)); d.ellipse([px(ex + 4), px(ey + 6), px(ex + 8), px(ey + 10)], fill=(255, 255, 255, 170))
    shape(img, hexc('#d98a90'), 321, [(cx - 7, 202), (cx + 7, 202), (cx, 211)], scale=3, k=.3, rim=.1, smooth=False, feather=.4)
    d = ImageDraw.Draw(img)
    d.arc([px(cx - 12), px(208), px(cx), px(220)], 10, 170, fill=(90, 60, 60, 255), width=px(1.8)); d.arc([px(cx), px(208), px(cx + 12), px(220)], 10, 170, fill=(90, 60, 60, 255), width=px(1.8))
    for sx in (-1, 1):
        for k in range(3): d.line([(px(cx + sx * 24), px(210 + k * 4)), (px(cx + sx * 80), px(200 + k * 10))], fill=(220, 214, 204, 200), width=px(1.1))
    # warm lantern light along her left edge
    lit = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(lit).ellipse([px(-60), px(0), px(200), px(300)], fill=(255, 176, 90, 90))
    lit = lit.filter(ImageFilter.GaussianBlur(30 * M.S)); a = np.asarray(lit, np.float32); a[..., 3] *= np.asarray(img.getchannel('A'), np.float32) / 255
    img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))
    save(img, 'm_s2_akari')


# ───────────── Relics: 7 things, one per chapter ─────────────
def item_img(w, h, fn):
    img = I.canvas(w, h); fn(img)
    out = img.resize((w, h), Image.LANCZOS); a = np.asarray(out, np.float32)
    lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True); a[..., :3] = lum + (a[..., :3] - lum) * .9
    a[..., :3] += np.random.default_rng(w * h).normal(0, 3.5, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def fuda(img):   # wooden pass-plaque on a red cord: 猫岳 and a paw print
    I.line(img, [(55, 2), (36, 30), (55, 44), (74, 30), (55, 2)], '#b3302b', 2.4)
    pl = [(14, 58), (55, 34), (96, 58), (96, 182), (14, 182)]
    I.fill(img, '#b08a58', 401, poly=pl, scale=6, stretch=(1, 4), contrast=1.2); I.volume(img, (14, 34, 96, 182), .4, .3)
    I.line(img, [(18, 62), (55, 40), (92, 62)], '#5a3e22', 2)
    text(img, '猫', 55, 88, 34, '#241810', SERIF, brush=True); text(img, '岳', 55, 126, 34, '#241810', SERIF, brush=True)
    for dx, dy, r in ((0, 162, 8), (-11, 150, 3.6), (-4, 146, 3.6), (4, 146, 3.6), (11, 150, 3.6)): I.ell(img, (55 + dx - r, dy - r, 55 + dx + r, dy + r), (176, 40, 34, 230))


def ogi(img):    # folding fan: indigo night, a full moon and two dancing cats
    cx, cy, R = 110, 128, 104
    pts = [(cx, cy)] + [(cx + math.cos(a) * R, cy + math.sin(a) * R) for a in np.linspace(math.radians(198), math.radians(342), 30)]
    I.floor_shadow(img, cx, 134, 80)
    m = I.fill(img, '#2a3a64', 402, poly=pts, scale=7, contrast=1.1)
    inner = [(cx, cy)] + [(cx + math.cos(a) * 34, cy + math.sin(a) * 34) for a in np.linspace(math.radians(198), math.radians(342), 12)]
    I.poly(img, inner, '#3a2a1a')
    def art(d, l):
        d.ellipse([px(cx + 8), px(38), px(cx + 44), px(74)], fill=(238, 226, 180, 255))
        for k, x in enumerate((cx - 44, cx - 10)):   # two little cats on hind legs, towels on heads
            d.ellipse([px(x - 7), px(78 - k * 4), px(x + 7), px(92 - k * 4)], fill=(236, 230, 214, 255))
            d.polygon([(px(x - 6), px(80 - k * 4)), (px(x - 4), px(72 - k * 4)), (px(x), px(79 - k * 4))], fill=(236, 230, 214, 255))
            d.ellipse([px(x - 8), px(90 - k * 4), px(x + 8), px(112 - k * 4)], fill=(236, 230, 214, 255))
            d.line([(px(x + 6), px(94 - k * 4)), (px(x + 16), px(84 - k * 4))], fill=(236, 230, 214, 255), width=px(3))
            d.rectangle([px(x - 8), px(76 - k * 4), px(x + 8), px(80 - k * 4)], fill=(190, 60, 50, 255))
    clipped(img, m, art)
    clipped(img, m, lambda d, l: [d.line([(px(cx), px(cy)), (px(cx + math.cos(a) * R), px(cy + math.sin(a) * R))], fill=(20, 26, 44, 150), width=px(1.2)) for a in np.linspace(math.radians(198), math.radians(342), 15)])
    I.volume(img, (6, 20, 214, 130), .35, .2)
    I.ell(img, (cx - 5, cy - 5, cx + 5, cy + 5), '#c9a24a')


def hyotan(img):  # gourd flask with water of the mountain spring, sealed with a paper charm
    I.floor_shadow(img, 55, 174, 42)
    I.fill(img, '#c89a55', 403, ell=(12, 88, 98, 176), scale=6, contrast=.9); I.fill(img, '#c89a55', 404, ell=(26, 40, 84, 100), scale=6, contrast=.9)
    I.volume(img, (12, 88, 98, 176), .6, .35, .25); I.volume(img, (26, 40, 84, 100), .6, .35, .25)
    I.fill(img, '#3a2618', 405, rect=(44, 22, 66, 44), scale=4)
    I.line(img, [(34, 96), (55, 100), (76, 96)], '#b3302b', 3.2); I.line(img, [(60, 100), (68, 124), (62, 140)], '#b3302b', 2.2)
    I.fill(img, '#efe8d6', 406, poly=[(47, 18), (63, 18), (63, 78), (47, 78)], scale=3, contrast=.4)
    text(img, '猫', 55, 50, 13, '#b3302b', SERIF)
    soft(img, lambda d: [d.arc([px(40 + k * 8), px(-4 - k * 6), px(60 + k * 8), px(20 - k * 6)], 200, 340, fill=(240, 240, 236, 90), width=px(2)) for k in range(2)], 1.5)


def abura(img):   # clay oil dish on a little stand, a tiny flame on the wick
    glow(img, 96, 50, 34, hexc('#ffb454'), 150)
    I.floor_shadow(img, 75, 114, 52)
    I.fill(img, '#4a3222', 407, poly=[(40, 84), (110, 84), (116, 112), (34, 112)], scale=6, stretch=(3, 1)); I.volume(img, (34, 84, 116, 112), .5, .3)
    I.fill(img, '#9a6a42', 408, ell=(20, 62, 130, 90), scale=5, contrast=.8); I.volume(img, (20, 62, 130, 90), .5, .3, .2)
    I.ell(img, (32, 66, 118, 80), '#2a1c10'); soft(img, lambda d: d.ellipse([px(40), px(68), px(100), px(76)], fill=(200, 150, 60, 120)), 1.5)
    I.line(img, [(70, 72), (90, 64), (96, 58)], '#e8dcc0', 2.2)
    soft(img, lambda d: d.polygon([(px(90), px(58)), (px(96), px(34)), (px(102), px(58))], fill=(255, 196, 90, 255)), 1.2)
    soft(img, lambda d: d.ellipse([px(93), px(46), px(99), px(57)], fill=(255, 250, 220, 255)), .8)


def hotaru(img):  # bamboo firefly cage with green lights inside
    glow(img, 70, 104, 60, hexc('#b8f07a'), 70)
    I.floor_shadow(img, 70, 164, 52)
    I.fill(img, '#5a4a2a', 409, poly=[(20, 40), (70, 14), (120, 40), (120, 50), (20, 50)], scale=5, stretch=(4, 1)); I.volume(img, (20, 14, 120, 50), .4, .2)
    I.line(img, [(70, 14), (70, 2)], '#6a5a36', 2)
    I.fill(img, '#1e2a1c', 410, rect=(26, 50, 114, 156), scale=6, contrast=.6)
    rnd = random.Random(411)
    for k in range(12):
        x, y = rnd.uniform(34, 106), rnd.uniform(62, 148)
        soft(img, lambda d, x=x, y=y: d.ellipse([px(x - 7), px(y - 7), px(x + 7), px(y + 7)], fill=(180, 250, 110, 130)), 3)
        I.ell(img, (x - 2.2, y - 2.2, x + 2.2, y + 2.2), (236, 255, 190, 255))
    for x in range(28, 115, 8): I.line(img, [(x, 50), (x, 156)], '#b89a62', 1.6)
    I.fill(img, '#6a5634', 412, rect=(18, 154, 122, 166), scale=5, stretch=(4, 1)); I.volume(img, (18, 154, 122, 166), .4, .2)


def bowl(img):    # old blue-and-white cat bowl, a chip in the rim, 雲 on the side
    I.floor_shadow(img, 80, 86, 66)
    body = [(10, 30), (150, 30), (140, 60), (118, 78), (42, 78), (20, 60)]
    I.fill(img, '#e8e6de', 413, poly=body, scale=6, contrast=.5, dark=.25, light=.1); I.volume(img, (10, 22, 150, 80), .5, .3, .35)
    I.fill(img, '#d8d6cc', 414, rect=(56, 76, 104, 86), scale=4)
    I.line(img, [(14, 38), (146, 38)], '#2c4a8a', 3); I.line(img, [(34, 70), (126, 70)], '#2c4a8a', 2)
    text(img, '雲', 80, 54, 22, '#23407e', SERIF, brush=True)
    I.ell(img, (10, 20, 150, 40), '#f2f0ea'); I.ell(img, (18, 24, 142, 38), '#b8b4a8')
    d = ImageDraw.Draw(img); d.polygon([(px(112), px(20)), (px(128), px(21)), (px(121), px(31))], fill=(150, 140, 126, 255))   # the chip


def toro(img):    # the king's old iron lantern: pagoda roof with cat-ear tips, amber paper windows
    glow(img, 75, 116, 60, hexc('#ffb454'), 110)
    I.floor_shadow(img, 75, 246, 50)
    I.fill(img, '#3a3a36', 415, poly=[(34, 222), (116, 222), (122, 248), (28, 248)], scale=6); I.volume(img, (28, 222, 122, 248), .5, .3)
    I.fill(img, '#2e2e2a', 416, rect=(64, 158, 86, 224), scale=5, stretch=(1, 3)); I.volume(img, (64, 158, 86, 224), .5, .3)
    I.fill(img, '#2e2e2a', 417, rect=(30, 70, 120, 162), scale=6)
    I.fill(img, '#f0b660', 418, rect=(40, 80, 110, 152), scale=4, contrast=.5, light=.35)
    soft(img, lambda d: d.ellipse([px(50), px(92), px(100), px(142)], fill=(255, 240, 190, 150)), 8)
    I.line(img, [(75, 80), (75, 152)], '#2e2e2a', 3); I.line(img, [(40, 116), (110, 116)], '#2e2e2a', 3)
    text(img, '猫', 57, 99, 18, '#5a2a14', SERIF); text(img, '岳', 93, 134, 18, '#5a2a14', SERIF)
    I.fill(img, '#34342e', 419, poly=[(8, 74), (30, 58), (75, 44), (120, 58), (142, 74), (120, 70), (75, 64), (30, 70)], scale=6)
    I.fill(img, '#34342e', 420, poly=[(50, 50), (56, 20), (70, 42), (80, 42), (94, 20), (100, 50)], scale=5)
    I.volume(img, (8, 20, 142, 76), .5, .25, .15)
    for x in (8, 142): I.ell(img, (x - 4, 70, x + 4, 78), '#c9a24a')


RELICS = [('s2_fuda', 110, 190, fuda), ('s2_ogi', 220, 140, ogi), ('s2_hyotan', 110, 180, hyotan), ('s2_abura', 150, 120, abura),
          ('s2_hotaru', 140, 170, hotaru), ('s2_bowl', 160, 90, bowl), ('s2_toro', 150, 250, toro)]


def atlas():
    ims = [(iid, item_img(w, h, fn)) for iid, w, h, fn in RELICS]
    W = sum(im.width for _, im in ims) + 4 * (len(ims) - 1); H = max(im.height for _, im in ims)
    at = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x = 0; rects = {}
    for iid, im in ims: at.alpha_composite(im, (x, 0)); rects[iid] = [x, 0, im.width, im.height]; x += im.width + 4
    at.save(f'{ITEM_DIR}/atlas_s2.webp', 'WEBP', quality=88, alpha_quality=92, method=6)
    print(json.dumps({'atlas': [W, H], 'rects': rects}))


if __name__ == '__main__':
    king(); akari(); atlas()
