#!/usr/bin/env python3
"""«Слухи и час быка»: yōkai the rumours lead to — a tengu, Okiku with her plates, kosode-no-te (hands from a hung kimono),
Bunbuku the kettle-tanuki — plus the nine «Тайны дома» keepsakes packed into one atlas.
Same organic spline toolkit as story_art.py / guests_art.py.
Usage: rumors_art.py assets/mon   (the atlas goes to assets/items/atlas_rm.webp, previews to art/out/)"""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc
import monsters as M
from monsters import canvas, px, soft, hair, save
from story_art import cr, mask_of, shape, clipped, poly_s, folds, hair_texture, kimono_pattern
from guests_art import stroke, tube, fur_ticks
from items import text, SERIF

S = M.S
HERE = os.path.dirname(os.path.abspath(__file__))
BLK = (16, 14, 15, 255)


def fin(img):
    """Same finish as monsters.save(), but returns the picture (for the atlas)."""
    out = img.resize((P.W, P.H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(.55))
    a = np.asarray(out, np.float32); n = np.random.default_rng(P.W * 7 + P.H).normal(0, 5, a.shape[:2])[..., None]; a[..., :3] = np.clip(a[..., :3] + n, 0, 255)
    return Image.fromarray(a.astype(np.uint8), 'RGBA')


def fade_bottom(img, y0, y1):
    a = np.asarray(img, np.float32); ys = np.arange(a.shape[0])[:, None] / S
    a[..., 3] *= np.clip((y1 - ys) / (y1 - y0), 0, 1); img.paste(Image.fromarray(a.astype(np.uint8), 'RGBA'))


def feather(img, base, tip, w, col, seed, shaft=(200, 190, 170, 150)):
    """One long wing feather: a tapered blade with a pale shaft."""
    (bx, by), (tx, ty) = base, tip; a = math.atan2(ty - by, tx - bx); nx, ny = -math.sin(a), math.cos(a); L = math.hypot(tx - bx, ty - by)
    pts = [(bx + nx * w * .4, by + ny * w * .4), (bx + (tx - bx) * .55 + nx * w, by + (ty - by) * .55 + ny * w), (tx + nx * w * .3, ty + ny * w * .3), (tx, ty),
           (tx - nx * w * .3, ty - ny * w * .3), (bx + (tx - bx) * .55 - nx * w * .8, by + (ty - by) * .55 - ny * w * .8), (bx - nx * w * .4, by - ny * w * .4)]
    m = shape(img, col, seed, pts, scale=6, stretch=(1, 3), contrast=1.0, dk=.5, lt=.18, k=.35, rim=.35, feather=.5)
    clipped(img, m, lambda d, l: d.line([(px(bx), px(by)), (px(bx + (tx - bx) * .9), px(by + (ty - by) * .9))], fill=shaft, width=px(1.6)))
    clipped(img, m, lambda d, l: [d.line([(px(bx + (tx - bx) * u + nx * w * .1), px(by + (ty - by) * u + ny * w * .1)), (px(bx + (tx - bx) * (u + .06) + nx * w), px(by + (ty - by) * (u + .06) + ny * w))], fill=(0, 0, 0, 50), width=px(1)) for u in np.linspace(.15, .8, 7)])


# ───────────── Tengu: red face, long nose, yamabushi robe with bonten pompoms, feather fan, black wings ─────────────
def tengu():
    img = canvas(440, 580); cx = 220
    # wings: long primaries first, then a band of short coverts along the arm
    for sx in (-1, 1):
        sh, wr = (cx + sx * 40, 236), (cx + sx * 200, 84)
        for i in range(12, -1, -1):
            u = i / 12; bx, by = sh[0] + (wr[0] - sh[0]) * u, sh[1] + (wr[1] - sh[1]) * u; a = .12 + .62 * u; L = 170 + 90 * u
            col = mixc(hexc('#2e2822'), hexc('#4a3c2e'), (i % 3) / 3)
            feather(img, (bx, by), (bx + sx * math.sin(a) * L, by + math.cos(a) * L), 17 - 4 * u, col, 300 + i + (sx > 0) * 20)
        for r in range(2):
            for i in range(9):
                u = (i + .5) / 9; bx, by = sh[0] + (wr[0] - sh[0]) * u, sh[1] + (wr[1] - sh[1]) * u + r * 26
                shape(img, mixc(hexc('#3c3228'), hexc('#5a4a38'), r * .5), 330 + i + r * 10 + (sx > 0) * 40, ell=(bx - 22, by - 12, bx + 22, by + 34 - r * 6), scale=5, contrast=.8, dk=.45, lt=.15, k=.4, rim=.4, feather=.5)
    # hakama: wide dark trousers, then the one-tooth geta
    for sx in (-1, 1):
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([px(cx + sx * 46 - 22), px(534), px(cx + sx * 46 + 22), px(544)], px(3), fill=hexc('#3a2618'))
        d.rectangle([px(cx + sx * 46 - 5), px(542), px(cx + sx * 46 + 5), px(574)], fill=hexc('#2a1c12'))
        shape(img, (232, 226, 214, 255), 340 + sx, [(cx + sx * 46 - 18, 520), (cx + sx * 46 + 18, 520), (cx + sx * 46 + 20, 538), (cx + sx * 46 - 20, 538)], scale=4, contrast=.3, k=.3, rim=.2)
    hk = [(cx - 96, 380), (cx + 96, 380), (cx + 118, 470), (cx + 116, 526), (cx + 22, 526), (cx, 500), (cx - 22, 526), (cx - 116, 526), (cx - 118, 470)]
    mh = shape(img, hexc('#4b4a3c'), 343, hk, scale=14, stretch=(1, 3), contrast=1.0, dk=.45, lt=.15, k=.4, rim=.3)
    folds(img, mh, [[(cx - 70, 400), (cx - 80, 520)], [(cx - 36, 400), (cx - 40, 500)], [(cx + 36, 400), (cx + 40, 500)], [(cx + 70, 400), (cx + 80, 520)]], (0, 0, 0, 90), 3)
    # suzukake robe (pale hemp) with a fine check
    robe = [(cx - 72, 214), (cx, 204), (cx + 72, 214), (cx + 98, 280), (cx + 102, 404), (cx - 102, 404), (cx - 98, 280)]
    mr = shape(img, hexc('#cfc3a6'), 344, robe, scale=14, contrast=.8, dk=.35, lt=.12, k=.45, rim=.35)
    clipped(img, mr, lambda d, l: ([d.line([(px(x), px(200)), (px(x), px(410))], fill=(120, 100, 70, 60), width=px(1.2)) for x in range(cx - 100, cx + 101, 14)] +
                                   [d.line([(px(cx - 104), px(y)), (px(cx + 104), px(y))], fill=(120, 100, 70, 60), width=px(1.2)) for y in range(206, 410, 14)]))
    d = ImageDraw.Draw(img)
    poly_s(d, [(cx - 30, 212), (cx, 300), (cx + 30, 212), (cx + 18, 212), (cx, 270), (cx - 18, 212)], (236, 232, 222, 255), 4)
    stroke(d, [(cx - 104, 396), (cx, 404), (cx + 104, 396)], (70, 56, 40, 255), 7)                     # rope belt
    # left arm hanging in a wide sleeve, the right one raised with the fan
    shape(img, hexc('#c4b898'), 345, [(cx - 72, 222), (cx - 118, 262), (cx - 136, 340), (cx - 128, 382), (cx - 96, 386), (cx - 88, 320), (cx - 70, 280)], scale=10, contrast=.8, dk=.4, lt=.12, k=.5, rim=.35)
    shape(img, hexc('#b8483a'), 346, ell=(cx - 132, 370, cx - 104, 398), scale=4, k=.4, rim=.3)
    shape(img, hexc('#c4b898'), 347, [(cx + 70, 222), (cx + 120, 244), (cx + 150, 280), (cx + 146, 306), (cx + 120, 300), (cx + 96, 280), (cx + 76, 270)], scale=10, contrast=.8, dk=.4, lt=.12, k=.5, rim=.35)
    shape(img, hexc('#b8483a'), 348, [(cx + 134, 238), (cx + 156, 244), (cx + 160, 272), (cx + 140, 284), (cx + 128, 262)], scale=4, k=.4, rim=.3)
    # hauchiwa: a fan of brown and white feathers on a red handle
    d = ImageDraw.Draw(img); stroke(d, [(cx + 146, 262), (cx + 150, 200), (cx + 154, 160)], hexc('#8a2a22'), 6)
    for i in range(11):
        a = -math.pi / 2 + (i - 5) * .2; L = 92 - abs(i - 5) * 5
        feather(img, (cx + 154, 168), (cx + 154 + math.cos(a) * L, 168 + math.sin(a) * L), 14, hexc('#e4dccb') if i % 2 else hexc('#7a5a3a'), 360 + i, (150, 120, 90, 150))
    shape(img, hexc('#c8a040'), 372, ell=(cx + 144, 156, cx + 164, 176), scale=3, k=.6, rim=.4, spec=.4)
    # bonten pompoms down the chest
    for sx in (-1, 1):
        for k, (dx, y) in enumerate(((30, 244), (38, 290), (46, 336))):
            mp = shape(img, hexc('#e8e0cc') if k % 2 == 0 else hexc('#c98a3a'), 380 + k + (sx > 0) * 5, ell=(cx + sx * dx - 14, y - 14, cx + sx * dx + 14, y + 14), scale=3, contrast=.8, k=.5, rim=.4)
            fur_ticks(img, mp, 390 + k, (cx + sx * dx - 14, y - 14, cx + sx * dx + 14, y + 14), 30, (90, 70, 50, 120), (3, 5))
    # white mane behind the head, the head, then beard and brows on top
    mane = Image.new('RGBA', img.size, (0, 0, 0, 0))
    hair(mane, [(cx - 6 + math.cos(a) * 54, 150 + math.sin(a) * 58, math.cos(a) * .75) for a in np.linspace(-3.3, .2, 34)], 96, 240, 401, sway=.5, col=(196, 192, 182), width=(2, 4), gravity=.55)
    img.alpha_composite(mane)
    shape(img, hexc('#a8452f'), 402, [(cx, 92), (cx + 44, 104), (cx + 60, 146), (cx + 52, 190), (cx + 20, 214), (cx - 20, 212), (cx - 50, 186), (cx - 58, 140), (cx - 40, 104)], scale=7, contrast=.8, dk=.4, lt=.18, k=.55, rim=.35)
    soft(img, lambda dd: dd.ellipse([px(cx - 30), px(118), px(cx + 50), px(160)], fill=(60, 16, 12, 70)), 6)
    d = ImageDraw.Draw(img)
    for ex in (cx - 18, cx + 30):
        d.ellipse([px(ex - 10), px(138), px(ex + 10), px(152)], fill=hexc('#e2c04a')); d.ellipse([px(ex - 3), px(139), px(ex + 5), px(151)], fill=(18, 10, 6, 255))
        d.ellipse([px(ex - 10), px(138), px(ex + 10), px(152)], outline=(60, 14, 10, 255), width=px(2))
    brows = Image.new('RGBA', img.size, (0, 0, 0, 0))
    hair(brows, [(cx - 34 + k * 4, 132 - k * 1.5, -1.3) for k in range(8)] + [(cx + 18 + k * 4, 128 + k * 1.5, 1.3) for k in range(8)], 28, 50, 403, sway=.3, col=(210, 206, 196), width=(2, 3), gravity=.2)
    img.alpha_composite(brows)
    beard = Image.new('RGBA', img.size, (0, 0, 0, 0))
    hair(beard, [(cx - 36 + k * 6, 186 + abs(k - 6) * 1.5, (k - 6) * .06) for k in range(13)], 90, 170, 404, sway=.4, col=(200, 196, 186), width=(2, 4), gravity=.25)
    img.alpha_composite(beard)
    # the long nose, pointing right and a little down
    shape(img, hexc('#b4503a'), 405, tube([(cx + 14, 162), (cx + 50, 168), (cx + 92, 174), (cx + 128, 182)], 13, 6), scale=5, contrast=.7, dk=.4, lt=.25, k=.6, rim=.3, spec=.35)
    # tokin: the small black pleated cap on the forehead
    tk = [(cx - 12, 108), (cx - 4, 82), (cx + 18, 78), (cx + 30, 100), (cx + 22, 112), (cx, 114)]
    mt = shape(img, (24, 20, 20, 255), 406, tk, scale=3, contrast=.6, dk=.2, lt=.18, k=.5, rim=.2)
    clipped(img, mt, lambda dd, l: [dd.line([(px(cx - 8 + k * 7), px(110)), (px(cx - 2 + k * 6), px(80))], fill=(70, 66, 66, 200), width=px(1.2)) for k in range(5)])
    d = ImageDraw.Draw(img); stroke(d, [(cx - 12, 110), (cx - 40, 118), (cx - 50, 128)], (30, 26, 26, 255), 2)
    save(img, 'm_rm_tengu')


# ───────────── Okiku: a pale, gentle girl with a stack of plates; the hem fades like mist ─────────────
def okiku():
    img = canvas(300, 620); cx = 150
    hb = shape(img, BLK, 410, [(cx - 64, 120), (cx - 58, 64), (cx, 42), (cx + 58, 64), (cx + 64, 120), (cx + 62, 300), (cx + 54, 480), (cx - 54, 480), (cx - 62, 300)], scale=6, contrast=.6, dk=.2, lt=.12, k=.3, rim=.1)
    hair_texture(img, hb, 411, [(cx + x, 60, 0) for x in range(-60, 61, 4)], 420, 260)
    kim = (178, 190, 198, 255)
    for sx in (-1, 1):   # long hanging sleeves
        sl = [(cx + sx * 48, 206), (cx + sx * 84, 222), (cx + sx * 98, 290), (cx + sx * 102, 450), (cx + sx * 88, 480), (cx + sx * 58, 470), (cx + sx * 50, 330)]
        ms = shape(img, mixc(kim, BLK, .08), 412 + sx, sl, scale=20, stretch=(1, 3), contrast=.9, dk=.4, lt=.12, k=.5, rim=.35)
        kimono_pattern(img, ms, 414 + sx, 6, (cx + min(sx * 102, sx * 50), 380, cx + max(sx * 102, sx * 50), 480), ((236, 240, 244, 200), (200, 214, 230, 200)))
    body = [(cx - 44, 196), (cx, 190), (cx + 44, 196), (cx + 66, 260), (cx + 72, 400), (cx + 84, 610), (cx - 84, 610), (cx - 72, 400), (cx - 66, 260)]
    mb = shape(img, kim, 416, body, scale=24, stretch=(1, 3), contrast=.9, dk=.4, lt=.12, k=.35, rim=.3)
    kimono_pattern(img, mb, 417, 16, (cx - 80, 420, cx + 80, 610), ((236, 240, 244, 210), (200, 214, 230, 210)))
    folds(img, mb, [[(cx - 30, 400), (cx - 40, 600)], [(cx + 26, 400), (cx + 34, 600)], [(cx, 420), (cx + 4, 600)]])
    d = ImageDraw.Draw(img)
    poly_s(d, [(cx - 24, 196), (cx, 262), (cx + 24, 196), (cx + 14, 196), (cx, 240), (cx - 14, 196)], (242, 240, 234, 255), 4)
    mo = shape(img, hexc('#5a687c'), 418, [(cx - 70, 322), (cx + 70, 322), (cx + 72, 372), (cx - 72, 372)], scale=6, contrast=.8, dk=.3, lt=.15, k=.3, rim=.15, smooth=False)
    clipped(img, mo, lambda dd, l: dd.line([(px(cx - 72), px(347)), (px(cx + 72), px(347))], fill=(200, 190, 160, 200), width=px(2)))
    # three plates held against the chest
    for k in range(3):
        y = 312 - k * 9
        shape(img, (236, 234, 226, 255), 420 + k, ell=(cx - 50, y - 12, cx + 50, y + 12), scale=4, contrast=.3, k=.4, rim=.3, spec=.2)
        d = ImageDraw.Draw(img); d.ellipse([px(cx - 50), px(y - 12), px(cx + 50), px(y + 12)], outline=(60, 90, 150, 230), width=px(2))
    d.ellipse([px(cx - 26), px(282), px(cx + 26), px(302)], outline=(70, 100, 160, 200), width=px(2))
    for sx in (-1, 1):
        shape(img, (228, 222, 214, 255), 424 + sx, [(cx + sx * 44, 300), (cx + sx * 60, 294), (cx + sx * 64, 316), (cx + sx * 48, 324)], scale=4, contrast=.3, k=.4, rim=.3)
    # neck, face, bangs parted in the middle, side locks over the shoulders
    shape(img, (226, 222, 214, 255), 426, [(cx - 16, 168), (cx + 16, 168), (cx + 18, 200), (cx - 18, 200)], scale=6, contrast=.3, k=.3, rim=.2)
    shape(img, (234, 230, 222, 255), 427, ell=(cx - 38, 88, cx + 38, 182), scale=10, contrast=.3, dk=.2, lt=.08, k=.35, rim=.25)
    for sx in (-1, 1):
        mb2 = shape(img, BLK, 428 + sx, [(cx + sx * 2, 70), (cx + sx * 40, 80), (cx + sx * 46, 130), (cx + sx * 40, 200), (cx + sx * 34, 280), (cx + sx * 26, 200), (cx + sx * 26, 120), (cx + sx * 6, 96)], scale=6, contrast=.6, dk=.2, lt=.12, k=.3, rim=.1, feather=.5)
        hair_texture(img, mb2, 430 + sx, [(cx + sx * x, 72, sx * .1) for x in range(2, 44, 3)], 200, 60)
    d = ImageDraw.Draw(img)
    for ex in (cx - 15, cx + 15):   # eyes closed, lashes down
        d.arc([px(ex - 10), px(128), px(ex + 10), px(142)], 20, 160, fill=(40, 34, 36, 255), width=px(2))
    d.line([(px(cx - 3), px(162)), (px(cx + 3), px(162))], fill=(170, 60, 70, 255), width=px(3))
    soft(img, lambda dd: [dd.ellipse([px(cx - 32), px(146), px(cx - 14), px(158)], fill=(220, 150, 160, 50)), dd.ellipse([px(cx + 14), px(146), px(cx + 32), px(158)], fill=(220, 150, 160, 50))], 4)
    d.line([(px(cx - 40), px(118)), (px(cx - 58), px(160))], fill=(236, 236, 230, 220), width=px(2))   # white paper cord in the hair
    fade_bottom(img, 470, 616)
    save(img, 'm_rm_okiku')


# ───────────── Kosode-no-te: pale hands slip out of a kimono hung on a lacquered rack ─────────────
def ikou(img, w, h, seed, k=1.0):
    lac = (26, 20, 18, 255); d = ImageDraw.Draw(img)
    for x in (w * .14, w * .86):
        shape(img, lac, seed, [(x - 7 * k, 80 * k), (x + 7 * k, 80 * k), (x + 7 * k, h - 30 * k), (x - 7 * k, h - 30 * k)], scale=4, contrast=.5, dk=.2, lt=.25, k=.6, rim=.3, smooth=False)
        shape(img, lac, seed + 1, [(x - 40 * k, h - 32 * k), (x + 40 * k, h - 32 * k), (x + 44 * k, h - 16 * k), (x - 44 * k, h - 16 * k)], scale=4, contrast=.5, dk=.2, lt=.25, k=.6, rim=.3, smooth=False)
        d.ellipse([px(x - 4 * k), px(h - 30 * k), px(x + 4 * k), px(h - 22 * k)], fill=(190, 150, 70, 255))
    bar = [(w * .03, 66 * k), (w * .08, 74 * k), (w * .92, 74 * k), (w * .97, 66 * k), (w * .98, 76 * k), (w * .93, 88 * k), (w * .07, 88 * k), (w * .02, 76 * k)]
    shape(img, lac, seed + 2, bar, scale=4, contrast=.5, dk=.2, lt=.3, k=.7, rim=.3, spec=.25, smooth=False)


def hung_kimono(img, w, h, seed, k=1.0):
    base = hexc('#5a2a3c'); t = 80 * k
    for sx in (-1, 1):
        sl = [(w / 2 + sx * w * .2, t), (w / 2 + sx * w * .42, t), (w / 2 + sx * w * .43, t + 210 * k), (w / 2 + sx * w * .36, t + 226 * k), (w / 2 + sx * w * .2, t + 222 * k)]
        ms = shape(img, mixc(base, BLK, .1), seed + sx, sl, scale=18 * k, stretch=(1, 2), contrast=1.0, dk=.45, lt=.15, k=.4, rim=.3, smooth=False)
        kimono_pattern(img, ms, seed + 3 + sx, int(12 * k) + 2, (w / 2 + min(sx * w * .43, sx * w * .2), t, w / 2 + max(sx * w * .43, sx * w * .2), t + 220 * k), ((236, 226, 206, 230), (216, 150, 170, 230)))
    body = [(w / 2 - w * .22, t), (w / 2 + w * .22, t), (w / 2 + w * .25, h - 70 * k), (w / 2 - w * .25, h - 70 * k)]
    mb = shape(img, base, seed + 5, body, scale=22 * k, stretch=(1, 3), contrast=1.0, dk=.45, lt=.15, k=.35, rim=.3, smooth=False)
    kimono_pattern(img, mb, seed + 6, int(26 * k) + 3, (w / 2 - w * .25, t + 20 * k, w / 2 + w * .25, h - 70 * k), ((236, 226, 206, 230), (216, 150, 170, 230)))
    folds(img, mb, [[(w / 2 - 30 * k, t + 40 * k), (w / 2 - 36 * k, h - 80 * k)], [(w / 2 + 30 * k, t + 40 * k), (w / 2 + 36 * k, h - 80 * k)]])
    d = ImageDraw.Draw(img); d.line([(px(w / 2 - 40 * k), px(t + 2)), (px(w / 2), px(t + 60 * k)), (px(w / 2 + 40 * k), px(t + 2))], fill=(232, 224, 206, 255), width=px(6 * k))
    d.rectangle([px(w / 2 - w * .25), px(h - 76 * k), px(w / 2 + w * .25), px(h - 70 * k)], fill=(170, 60, 60, 255))


def pale_hand(img, root, wrist, seed, sx):
    shape(img, (214, 208, 198, 255), seed, tube([root, ((root[0] + wrist[0]) / 2, (root[1] + wrist[1]) / 2 + 4), wrist], 9, 7), scale=5, contrast=.3, dk=.25, lt=.1, k=.4, rim=.3)
    wx, wy = wrist; a0 = math.atan2(wy - root[1], wx - root[0])
    shape(img, (220, 214, 204, 255), seed + 1, ell=(wx - 13, wy - 10, wx + 13, wy + 14), scale=4, contrast=.3, k=.4, rim=.3)
    d = ImageDraw.Draw(img)
    for i in range(4):   # long slender fingers, gently curled
        a = a0 + (i - 1.5) * .22; L = 34 - abs(i - 1.2) * 4
        pts = [(wx + math.cos(a) * 8, wy + math.sin(a) * 8), (wx + math.cos(a) * L * .6, wy + math.sin(a) * L * .6 + 2), (wx + math.cos(a + sx * .3) * L, wy + math.sin(a + sx * .3) * L + 6)]
        d.line([(px(x), px(y)) for x, y in cr(pts, 6, False)], fill=(222, 216, 206, 255), width=px(5 - i * .4), joint='curve')
    d.line([(px(wx - sx * 8), px(wy)), (px(wx - sx * 18), px(wy + 14))], fill=(222, 216, 206, 255), width=px(5))


def kosode():
    img = canvas(520, 540); w, h = 520, 540
    ikou(img, w, h, 440)
    hung_kimono(img, w, h, 450)
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):   # the dark sleeve openings and the hands slipping out of them
        ox = w / 2 + sx * w * .34
        soft(img, lambda dd, ox=ox: dd.ellipse([px(ox - 26), px(292), px(ox + 26), px(314)], fill=(6, 4, 6, 230)), 2)
        pale_hand(img, (ox, 302), (ox + sx * 30, 352), 460 + sx * 3, sx)
    save(img, 'm_rm_kosode')


# ───────────── Bunbuku-chagama: a tanuki halfway turned into a tea kettle ─────────────
def chagama():
    img = canvas(360, 380); cx = 180
    brown, brown_d = hexc('#7a5634'), hexc('#553a22')
    tail = [(270, 300), (300, 280), (328, 240), (340, 196), (354, 214), (352, 262), (330, 306), (296, 330), (268, 330)]
    mt = shape(img, brown, 470, tail, scale=8, contrast=1.1, k=.5, rim=.35)
    clipped(img, mt, lambda dd, l: [stroke(dd, [(300 + k * 14, 226 + k * 22), (330 + k * 10, 250 + k * 22)], (40, 26, 14, 200), 10) for k in range(3)])
    for sx in (-1, 1):   # stubby legs under the kettle
        shape(img, brown_d, 471 + sx, [(cx + sx * 40, 318), (cx + sx * 84, 318), (cx + sx * 88, 362), (cx + sx * 76, 374), (cx + sx * 36, 370)], scale=6, k=.5)
    # the iron kettle: round body with arare bumps, a flange and a spout
    shape(img, hexc('#34322f'), 473, tube([(80, 236), (48, 214), (22, 186)], 16, 9), scale=4, contrast=.8, k=.5, rim=.3, spec=.15)
    mk = shape(img, hexc('#3c3a37'), 474, ell=(62, 150, 298, 338), scale=6, contrast=1.0, dk=.5, lt=.2, k=.6, rim=.45, spec=.18)
    rnd = random.Random(475)
    clipped(img, mk, lambda dd, l: [dd.ellipse([px(x - 3), px(y - 3), px(x + 3), px(y + 3)], fill=(110, 104, 96, 200)) for y in range(170, 240, 14) for x in range(70 + (y // 14 % 2) * 7, 300, 14)])
    shape(img, hexc('#2c2a28'), 476, ell=(40, 238, 320, 262), scale=5, contrast=.7, dk=.4, lt=.2, k=.5, rim=.3)
    d = ImageDraw.Draw(img); stroke(d, [(76, 176), (90, 70), (180, 40), (270, 70), (284, 176)], hexc('#8a6a3a'), 6)   # bronze handle
    for x in (76, 284): d.ellipse([px(x - 8), px(168), px(x + 8), px(184)], fill=hexc('#6a4a24'))
    # tanuki head popping out where the lid should be, paws gripping the rim
    for sx in (-1, 1):
        shape(img, brown_d, 477 + sx, ell=(cx + sx * 44 - 16, 72, cx + sx * 44 + 16, 100), scale=4, k=.4)
        d = ImageDraw.Draw(img); d.ellipse([px(cx + sx * 44 - 8), px(80), px(cx + sx * 44 + 8), px(96)], fill=(40, 28, 20, 255))
    shape(img, brown, 479, [(cx, 76), (cx + 38, 84), (cx + 58, 112), (cx + 60, 140), (cx + 40, 166), (cx, 176), (cx - 40, 166), (cx - 60, 140), (cx - 58, 112), (cx - 38, 84)], scale=7, contrast=.9, k=.55, rim=.35)
    shape(img, hexc('#dccaa2'), 480, [(cx - 24, 136), (cx, 128), (cx + 24, 136), (cx + 30, 156), (cx, 174), (cx - 30, 156)], scale=5, contrast=.5, dk=.2, lt=.12, k=.4, rim=.2)
    for sx in (-1, 1):
        shape(img, hexc('#2e2016'), 481 + sx, [(cx + sx * 6, 116), (cx + sx * 26, 106), (cx + sx * 50, 114), (cx + sx * 52, 136), (cx + sx * 36, 148), (cx + sx * 14, 140)], scale=5, contrast=.6, k=.3, rim=.1)
        d = ImageDraw.Draw(img); ex = cx + sx * 28
        d.ellipse([px(ex - 9), px(120), px(ex + 9), px(138)], fill=(236, 226, 196, 255)); d.ellipse([px(ex - 5), px(123), px(ex + 5), px(137)], fill=(20, 12, 8, 255)); d.ellipse([px(ex - 4), px(124), px(ex - 1), px(128)], fill=(255, 255, 255, 230))
    shape(img, (26, 18, 14, 255), 483, [(cx - 7, 146), (cx + 7, 146), (cx, 156)], scale=3, k=.5, rim=.2, spec=.4)
    d = ImageDraw.Draw(img); d.arc([px(cx - 12), px(152), px(cx), px(164)], 10, 170, fill=(60, 36, 26, 255), width=px(2)); d.arc([px(cx), px(152), px(cx + 12), px(164)], 10, 170, fill=(60, 36, 26, 255), width=px(2))
    soft(img, lambda dd: [dd.ellipse([px(cx - 48), px(146), px(cx - 28), px(158)], fill=(210, 110, 90, 80)), dd.ellipse([px(cx + 28), px(146), px(cx + 48), px(158)], fill=(210, 110, 90, 80))], 4)
    for sx in (-1, 1):
        shape(img, brown_d, 484 + sx, ell=(cx + sx * 78 - 18, 160, cx + sx * 78 + 18, 190), scale=4, k=.5, rim=.3)
        d = ImageDraw.Draw(img)
        for k in range(3): d.line([(px(cx + sx * 78 - 8 + k * 8), px(182)), (px(cx + sx * 78 - 8 + k * 8), px(190))], fill=(30, 20, 12, 255), width=px(1.5))
    save(img, 'm_rm_chagama')


# ───────────── The nine keepsakes («Тайны дома»), one atlas ─────────────
def it_chasen():      # Bunbuku's tea whisk in a bowl of matcha
    img = canvas(150, 150)
    shape(img, hexc('#3a3632'), 501, [(20, 88), (130, 88), (122, 128), (104, 142), (46, 142), (28, 128)], scale=5, contrast=.9, k=.5, rim=.35, spec=.12)
    shape(img, hexc('#6f8a3a'), 502, ell=(22, 80, 128, 98), scale=4, contrast=.6, k=.3, rim=.2)
    soft(img, lambda d: d.ellipse([px(46), px(84), px(96), px(94)], fill=(170, 200, 110, 140)), 2)
    d = ImageDraw.Draw(img); d.rounded_rectangle([px(58), px(142), px(92), px(148)], px(2), fill=hexc('#2a2622'))
    for k in range(14):   # the whisk tines standing in the bowl
        x = 58 + k * 2.6; d.line([(px(75), px(22)), (px(x), px(84))], fill=(214, 196, 150, 230), width=px(1.3))
    shape(img, hexc('#cdb88a'), 503, [(68, 10), (82, 10), (84, 34), (66, 34)], scale=3, contrast=.5, k=.5, rim=.3, smooth=False)
    stroke(d, [(84, 20), (100, 30), (98, 44)], (160, 60, 40, 255), 2)
    return fin(img)


def it_kagami():      # round bronze mirror on a small stand; a two-tailed cat in the glass
    img = canvas(140, 180)
    d = ImageDraw.Draw(img)
    for x in (40, 100): d.line([(px(x), px(110)), (px(70 + (x - 70) * 1.6), px(170))], fill=hexc('#2a1c14'), width=px(6))
    d.rounded_rectangle([px(22), px(164), px(118), px(174)], px(3), fill=hexc('#3a2618'))
    shape(img, hexc('#9a7a3a'), 511, ell=(14, 14, 126, 126), scale=4, contrast=1.1, k=.6, rim=.4, spec=.2)
    shape(img, hexc('#c8ccc8'), 512, ell=(24, 24, 116, 116), scale=6, contrast=.4, dk=.3, lt=.2, k=.6, rim=.4, spec=.3)
    soft(img, lambda dd: [dd.ellipse([px(54), px(60), px(86), px(100)], fill=(60, 66, 70, 150)), dd.ellipse([px(58), px(44), px(82), px(66)], fill=(60, 66, 70, 150)),
                          dd.polygon([(px(58), px(50)), (px(62), px(36)), (px(68), px(48))], fill=(60, 66, 70, 150)), dd.polygon([(px(72), px(48)), (px(78), px(36)), (px(82), px(50))], fill=(60, 66, 70, 150)),
                          dd.line([(px(84), px(96)), (px(100), px(70))], fill=(60, 66, 70, 150), width=px(5)), dd.line([(px(84), px(98)), (px(106), px(84))], fill=(60, 66, 70, 150), width=px(5))], 2)
    return fin(img)


def it_hauchiwa():    # the tengu's feather fan on a stand
    img = canvas(140, 210)
    d = ImageDraw.Draw(img); d.rounded_rectangle([px(36), px(194), px(104), px(206)], px(3), fill=hexc('#3a2618')); d.rectangle([px(66), px(150), px(74), px(196)], fill=hexc('#2a1c12'))
    stroke(d, [(70, 170), (70, 120)], hexc('#8a2a22'), 8)
    for i in range(11):
        a = -math.pi / 2 + (i - 5) * .2; L = 100 - abs(i - 5) * 5
        feather(img, (70, 122), (70 + math.cos(a) * L, 122 + math.sin(a) * L), 13, hexc('#e4dccb') if i % 2 else hexc('#7a5a3a'), 520 + i, (150, 120, 90, 150))
    shape(img, hexc('#c8a040'), 532, ell=(60, 112, 80, 132), scale=3, k=.6, rim=.4, spec=.4)
    return fin(img)


def it_azuki():       # a bamboo sieve heaped with red beans
    img = canvas(180, 110)
    mz = shape(img, hexc('#b89a5e'), 541, [(8, 50), (172, 50), (160, 92), (130, 104), (50, 104), (20, 92)], scale=4, stretch=(3, 1), contrast=1.1, k=.5, rim=.3)
    clipped(img, mz, lambda dd, l: [dd.line([(px(x), px(50)), (px(x + 8), px(104))], fill=(120, 96, 50, 160), width=px(1.2)) for x in range(4, 176, 6)] + [dd.line([(px(0), px(y)), (px(180), px(y))], fill=(120, 96, 50, 120), width=px(1.2)) for y in (62, 76, 90)])
    rnd = random.Random(542); d = ImageDraw.Draw(img)
    for _ in range(170):
        x = rnd.gauss(90, 34); y = 54 - 26 * math.exp(-((x - 90) / 50) ** 2) + rnd.uniform(-4, 10)
        if 14 < x < 166: d.ellipse([px(x - 4.5), px(y - 3.5), px(x + 4.5), px(y + 3.5)], fill=mixc(hexc('#7a1c1c'), hexc('#a8342c'), rnd.random()))
    for _ in range(40):
        x, y = rnd.uniform(40, 140), rnd.uniform(30, 52); d.ellipse([px(x - 1.2), px(y - 1.8), px(x + .4), px(y - .6)], fill=(240, 200, 190, 200))
    return fin(img)


def it_key():         # the key to Inari's rice store, on a red cord with a white fox tassel
    img = canvas(110, 210)
    d = ImageDraw.Draw(img); stroke(d, [(55, 0), (52, 30), (55, 56)], hexc('#b3302b'), 4)
    shape(img, hexc('#6a5a44'), 551, tube([(55, 70), (56, 120), (55, 176)], 7, 6), scale=3, contrast=1.0, k=.6, rim=.3, spec=.2)
    ring = shape(img, hexc('#6a5a44'), 552, ell=(33, 50, 77, 94), scale=3, contrast=1.0, k=.6, rim=.3, spec=.2)
    d = ImageDraw.Draw(img); d.ellipse([px(43), px(60), px(67), px(84)], fill=(0, 0, 0, 0))
    img2 = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(img2).ellipse([px(43), px(60), px(67), px(84)], fill=(255, 255, 255, 255))
    a = np.asarray(img, np.float32); a[..., 3] *= 1 - np.asarray(img2.getchannel('A'), np.float32) / 255; img.paste(Image.fromarray(a.astype(np.uint8), 'RGBA'))
    for y, w_ in ((150, 22), (172, 30)): shape(img, hexc('#5c4c38'), 553 + y, [(55, y - 6), (55 + w_, y - 6), (55 + w_, y + 8), (55, y + 8)], scale=3, contrast=1.0, k=.5, rim=.3, smooth=False)
    shape(img, hexc('#e8dfcc'), 555, ell=(26, 96, 50, 120), scale=3, contrast=.4, k=.5, rim=.3, spec=.3)                      # the hōju jewel
    d = ImageDraw.Draw(img); d.polygon([(px(38), px(94)), (px(34), px(88)), (px(42), px(90))], fill=hexc('#e8dfcc'))
    mt = shape(img, hexc('#f1ebde'), 556, [(40, 120), (46, 150), (40, 190), (30, 204), (22, 186), (28, 150)], scale=4, contrast=.5, k=.5, rim=.35)
    clipped(img, mt, lambda dd, l: dd.ellipse([px(18), px(180), px(46), px(208)], fill=(236, 200, 150, 255)))
    return fin(img)


def it_moku():        # a small shoji panel whose paper has eyes
    img = canvas(150, 210)
    d = ImageDraw.Draw(img)
    shape(img, hexc('#d8d0bc'), 561, [(14, 10), (136, 10), (136, 190), (14, 190)], scale=8, contrast=.5, dk=.25, lt=.1, k=.3, rim=.2, smooth=False)
    frame = hexc('#3a2a1c')
    for x in (12, 74, 138): d.rectangle([px(x - 5), px(6), px(x + 5), px(194)], fill=frame)
    for y in (8, 68, 128, 192): d.rectangle([px(8), px(y - 5), px(142), px(y + 5)], fill=frame)
    for x in (43, 105): d.line([(px(x), px(8)), (px(x), px(192))], fill=frame, width=px(4))
    d.rounded_rectangle([px(4), px(194), px(40), px(206)], px(2), fill=frame); d.rounded_rectangle([px(110), px(194), px(146), px(206)], px(2), fill=frame)
    for ex, ey, o in ((28, 38, 1), (90, 100, 1), (58, 160, 0), (120, 40, 0), (122, 162, 1)):
        if o:
            d.ellipse([px(ex - 10), px(ey - 6), px(ex + 10), px(ey + 6)], fill=(236, 230, 218, 255)); d.ellipse([px(ex - 4), px(ey - 5), px(ex + 4), px(ey + 5)], fill=(20, 12, 10, 255))
            d.ellipse([px(ex - 10), px(ey - 6), px(ex + 10), px(ey + 6)], outline=(60, 40, 30, 255), width=px(1.6))
        else: d.arc([px(ex - 10), px(ey - 6), px(ex + 10), px(ey + 6)], 20, 160, fill=(60, 40, 30, 255), width=px(2))
    return fin(img)


def it_sara():        # the tenth plate: blue-and-white, on a little stand
    img = canvas(160, 150)
    d = ImageDraw.Draw(img); d.line([(px(80), px(90)), (px(60), px(144))], fill=hexc('#2a1c14'), width=px(5)); d.line([(px(80), px(90)), (px(100), px(144))], fill=hexc('#2a1c14'), width=px(5))
    shape(img, hexc('#ecebe4'), 571, ell=(14, 4, 146, 136), scale=6, contrast=.3, dk=.2, lt=.1, k=.5, rim=.3, spec=.25)
    d = ImageDraw.Draw(img)
    d.ellipse([px(22), px(12), px(138), px(128)], outline=(40, 70, 140, 230), width=px(5))
    d.ellipse([px(46), px(36), px(114), px(104)], outline=(40, 70, 140, 200), width=px(2))
    for k in range(12):
        a = k / 12 * math.tau; d.ellipse([px(80 + math.cos(a) * 50 - 4), px(70 + math.sin(a) * 50 - 4), px(80 + math.cos(a) * 50 + 4), px(70 + math.sin(a) * 50 + 4)], fill=(50, 80, 150, 200))
    text(img, '十', 80, 70, 40, '#2c4a8c', SERIF)
    return fin(img)


def it_tsuzumi():     # the moon drum: a small shime-daiko with a tomoe, on a stand
    img = canvas(160, 160)
    d = ImageDraw.Draw(img)
    for x0, x1 in ((34, 20), (126, 140)): d.line([(px(x0), px(96)), (px(x1), px(154))], fill=hexc('#2a1c14'), width=px(6))
    shape(img, hexc('#8a2a22'), 581, [(26, 50), (134, 50), (134, 110), (26, 110)], scale=5, contrast=.9, k=.5, rim=.3, spec=.15, smooth=False)
    shape(img, hexc('#e6dcc4'), 582, ell=(18, 22, 142, 62), scale=5, contrast=.4, k=.5, rim=.3)
    d = ImageDraw.Draw(img)
    for k in range(10):
        x = 30 + k * 11; d.line([(px(x), px(58)), (px(x + 6), px(112))], fill=(210, 190, 140, 230), width=px(2))
    for k in range(3):
        a = k / 3 * math.tau; x, y = 80 + math.cos(a) * 11, 42 + math.sin(a) * 6
        d.ellipse([px(x - 7), px(y - 4.5), px(x + 7), px(y + 4.5)], fill=(40, 30, 60, 230))
    shape(img, hexc('#e8d890'), 583, ell=(116, 4, 150, 38), scale=3, contrast=.4, k=.4, rim=.3, spec=.3)
    img2 = Image.new('L', img.size, 0); ImageDraw.Draw(img2).ellipse([px(124), px(0), px(156), px(32)], fill=255)
    a = np.asarray(img, np.float32); a[..., 3] *= 1 - np.asarray(img2, np.float32) / 255 * (np.arange(a.shape[1])[None, :] > px(132)); img.paste(Image.fromarray(a.astype(np.uint8), 'RGBA'))
    return fin(img)


def it_kosode():      # a doll-sized kosode on its rack (no hands… usually)
    img = canvas(200, 200)
    ikou(img, 200, 200, 591, .38)
    hung_kimono(img, 200, 200, 595, .38)
    return fin(img)


ITEMS = [('rm_chasen', it_chasen), ('rm_kagami', it_kagami), ('rm_hauchiwa', it_hauchiwa), ('rm_azuki', it_azuki), ('rm_key', it_key),
         ('rm_moku', it_moku), ('rm_sara', it_sara), ('rm_tsuzumi', it_tsuzumi), ('rm_kosode', it_kosode)]


def atlas():
    pics = [(k, f()) for k, f in ITEMS]
    x = y = rowh = 0; W = 520; rects = {}
    for k, im in pics:
        if x + im.width > W: x = 0; y += rowh + 4; rowh = 0
        rects[k] = [x, y, im.width, im.height]; x += im.width + 4; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for k, im in pics: at.alpha_composite(im, tuple(rects[k][:2]))
    at.save(os.path.join(HERE, '..', 'assets', 'items', 'atlas_rm.webp'), 'WEBP', quality=88, alpha_quality=92, method=6)
    print('atlas', at.size, json.dumps(rects))


if __name__ == '__main__':
    what = sys.argv[2:] or ['tengu', 'okiku', 'kosode', 'chagama', 'atlas']
    for n in what: globals()[n]()
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    json.dump(M.META, open(os.path.join(HERE, 'out', 'rumors_mon.json'), 'w'))
    print(json.dumps(M.META))
