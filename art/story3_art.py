#!/usr/bin/env python3
"""Third story «Шпилька Бэни»: young Haru as a girl of 1924 (indigo yagasuri kimono, mustard obi, a bob pinned with the kanzashi —
black lacquer, silver plum blossom, red coral bead — and a paper pinwheel), plus 7 relics packed into one atlas.
Same organic spline toolkit as story_art.py / story2_art.py.
Usage: story3_art.py <mondir> <itemdir>   (assets/mon assets/items) → m_s3_haru.webp, atlas_s3.webp; prints the rect map."""
import json, math, random, sys
MON_DIR, ITEM_DIR = sys.argv[1], sys.argv[2]
sys.argv = [sys.argv[0], MON_DIR]          # monsters/items read their output dir from argv[1]
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc
import monsters as M
from monsters import canvas, px, soft, save
from story_art import cr, mask_of, shape, clipped, poly_s, folds, hair_texture, face_kid, flower
import items as I
from items import text, SERIF

BLACK, WHITE = (0, 0, 0, 255), (255, 255, 255, 255)
BLK = (16, 14, 15, 255)
INDIGO, INDIGO_D = hexc('#3d3768'), hexc('#2c284e')
OBI = hexc('#cf9f3c')


def glow(img, x, y, r, col, a=150):
    soft(img, lambda d: [d.ellipse([px(x - r * k), px(y - r * k), px(x + r * k), px(y + r * k)], fill=col[:3] + (int(a * (1.1 - k)),)) for k in (1, .7, .45)], r * .35)


def yagasuri(img, m, box, step=(22, 34), cols=((196, 190, 214, 210), (112, 100, 160, 210))):
    """Arrow-feather pattern of the Taisho schoolgirl kimono: columns of chevrons, alternating light/lilac."""
    x0, y0, x1, y1 = box
    def fn(d, l):
        for ci, x in enumerate(np.arange(x0 - 4, x1 + 4, step[0])):
            off = (ci % 2) * step[1] / 2
            for ri, y in enumerate(np.arange(y0 - step[1] + off, y1 + step[1], step[1])):
                c = cols[(ri + ci) % 2]; w = step[0] / 2 - 2; h = step[1] / 2
                d.polygon([(px(x - w), px(y)), (px(x), px(y + h * .55)), (px(x + w), px(y)), (px(x + w), px(y + h)), (px(x), px(y + h * 1.55)), (px(x - w), px(y + h))], fill=c)
                d.line([(px(x), px(y + h * .55)), (px(x), px(y + h * 1.55))], fill=(40, 34, 70, 160), width=px(1.2))
    clipped(img, m, fn, .78)


def pinwheel(img, cx, cy, r, seed):
    """Paper kazaguruma: four curled petals red/white, a nail in the middle."""
    cols = [hexc('#c8342c'), hexc('#efe6d6'), hexc('#c8342c'), hexc('#efe6d6')]
    for k in range(4):
        a = k * math.pi / 2 + .35
        p0 = (cx, cy); p1 = (cx + math.cos(a) * r, cy + math.sin(a) * r); p2 = (cx + math.cos(a + 1.1) * r * .72, cy + math.sin(a + 1.1) * r * .72)
        mid = ((p1[0] + p2[0]) / 2 + math.cos(a + .5) * r * .25, (p1[1] + p2[1]) / 2 + math.sin(a + .5) * r * .25)
        shape(img, cols[k], seed + k, [p0, p1, mid, p2], scale=4, contrast=.4, dk=.25, lt=.15, k=.5, rim=.2, feather=.4, smooth=False)
    d = ImageDraw.Draw(img); d.ellipse([px(cx - 4), px(cy - 4), px(cx + 4), px(cy + 4)], fill=(210, 180, 90, 255))


def kanzashi(img, x, y, s=1.0, ang=-.5):
    """Black lacquer pin with a silver plum blossom and a dangling red coral bead."""
    ca, sa = math.cos(ang), math.sin(ang)
    d = ImageDraw.Draw(img)
    d.line([(px(x - ca * 34 * s), px(y - sa * 34 * s)), (px(x + ca * 30 * s), px(y + sa * 30 * s))], fill=(10, 8, 8, 255), width=px(4 * s))
    d.line([(px(x - ca * 30 * s), px(y - sa * 30 * s - 1)), (px(x + ca * 10 * s), px(y + sa * 10 * s - 1))], fill=(120, 110, 110, 160), width=px(1.2 * s))
    fx, fy = x + ca * 30 * s, y + sa * 30 * s
    flower(d, fx, fy, 6.5 * s, (214, 216, 222, 255), center=(170, 140, 70, 255))
    for k in range(5):
        a = k / 5 * math.tau - math.pi / 2; d.ellipse([px(fx + math.cos(a) * 6.5 * s - 1.4), px(fy + math.sin(a) * 6.5 * s - 1.4), px(fx + math.cos(a) * 6.5 * s + .6), px(fy + math.sin(a) * 6.5 * s + .6)], fill=(255, 255, 255, 200))
    d.line([(px(fx), px(fy + 6 * s)), (px(fx + 1), px(fy + 20 * s))], fill=(190, 190, 196, 230), width=px(1.2))
    shape(img, hexc('#c22a26'), 77, ell=(fx + 1 - 6 * s, fy + 19 * s, fx + 1 + 6 * s, fy + 31 * s), scale=3, contrast=.3, k=.7, rim=.4, spec=.45, feather=.3)


# ───────────── Haru, seven years old, autumn 1924 ─────────────
def haru():
    img = canvas(300, 640)
    body = [(118, 238), (150, 234), (182, 238), (206, 266), (214, 340), (220, 450), (228, 598), (150, 610), (72, 598), (80, 450), (86, 340), (94, 266)]
    mb = shape(img, INDIGO, 61, body, scale=24, stretch=(1, 3), contrast=1.0, dk=.4, lt=.14, k=.35, rim=.3)
    yagasuri(img, mb, (80, 420, 222, 606))
    folds(img, mb, [[(120, 430), (112, 520), (108, 600)], [(182, 430), (188, 520), (196, 600)], [(150, 440), (152, 600)]], (0, 0, 0, 90))
    for sx in (-1, 1):   # medium sleeves of a girl's festive kimono
        sl = [(150 + sx * 52, 252), (150 + sx * 82, 268), (150 + sx * 96, 320), (150 + sx * 98, 440), (150 + sx * 88, 470), (150 + sx * 56, 468), (150 + sx * 48, 440), (150 + sx * 46, 320)]
        ms = shape(img, INDIGO_D if sx < 0 else INDIGO, 62 + sx, sl, scale=20, stretch=(1, 3), contrast=1.0, dk=.42, lt=.12, k=.5, rim=.35)
        yagasuri(img, ms, (150 + min(sx * 98, sx * 46), 300, 150 + max(sx * 98, sx * 46), 470))
    d = ImageDraw.Draw(img)
    poly_s(d, [(122, 238), (150, 318), (178, 238), (170, 238), (150, 296), (130, 238)], hexc('#b8342c'), 4)   # red juban collar
    poly_s(d, [(127, 238), (150, 304), (173, 238), (166, 238), (150, 286), (134, 238)], (240, 234, 222, 255), 4)
    obi = [(86, 360), (214, 360), (216, 420), (84, 420)]
    mo = shape(img, OBI, 64, obi, scale=6, contrast=.8, dk=.3, lt=.18, k=.3, rim=.15, smooth=False)
    clipped(img, mo, lambda dd, l: [dd.line([(px(84), px(y)), (px(216), px(y))], fill=(150, 100, 30, 200), width=px(2)) for y in (372, 408)] +
            [flower(dd, x, 390, 5, (236, 214, 150, 220), center=(190, 60, 50, 255)) for x in (104, 196)])
    d.rounded_rectangle([px(84), px(386), px(216), px(393)], px(3), fill=hexc('#d0566a'))   # pink obijime
    for x in (110, 176):   # tabi + geta with red hanao
        d.rounded_rectangle([px(x - 17), px(600), px(x + 17), px(622)], px(8), fill=(238, 232, 220, 255))
        d.line([(px(x - 9), px(612)), (px(x), px(603)), (px(x + 9), px(612))], fill=hexc('#c8342c'), width=px(3))
        d.rounded_rectangle([px(x - 21), px(620), px(x + 21), px(630)], px(3), fill=hexc('#6a4a2c'))
    # the pinwheel held up in front, a little to the right
    d.line([(px(168), px(470)), (px(236), px(316))], fill=hexc('#8a6a3a'), width=px(4))
    glow(img, 238, 312, 46, hexc('#ffd8a0'), 50)
    pinwheel(img, 238, 312, 36, 66)
    for hx, hy in ((160, 456), (180, 446)): shape(img, (236, 226, 212, 255), 67 + hx, ell=(hx - 12, hy - 11, hx + 12, hy + 11), scale=6, contrast=.3, k=.4, rim=.3)
    shape(img, (230, 220, 206, 255), 68, [(132, 212), (168, 212), (170, 246), (130, 246)], scale=8, contrast=.3, k=.3, rim=.2)   # neck
    # bob hair (shorter than Beni's), face, side-swept bangs pinned with the kanzashi
    hb = shape(img, BLK, 69, [(88, 220), (82, 166), (90, 112), (118, 80), (150, 72), (182, 80), (210, 112), (218, 166), (212, 220), (150, 212)], scale=6, contrast=.6, dk=.2, lt=.12, k=.3, rim=.1)
    hair_texture(img, hb, 70, [(150 + x, 78, 0) for x in range(-62, 63, 5)], 140, 150)
    face_kid(img, 150, 174, 54, 64, 71)
    bangs = [(94, 150), (96, 110), (120, 84), (150, 78), (184, 84), (206, 110), (208, 128), (186, 130), (160, 140), (128, 150), (110, 156)]
    mb2 = shape(img, BLK, 72, bangs, scale=6, contrast=.6, dk=.2, lt=.12, k=.3, rim=.1)
    for sx in (-1, 1): shape(img, BLK, 73 + sx, [(150 + sx * 64, 140), (150 + sx * 52, 150), (150 + sx * 52, 214), (150 + sx * 66, 220)], scale=6, contrast=.6, dk=.2, lt=.12, k=.2, rim=.05, feather=.5)
    hair_texture(img, mb2, 74, [(150 + x, 80, 0) for x in range(-54, 57, 4)], 70, 120)
    soft(img, lambda dd: dd.arc([px(106), px(82), px(170), px(128)], 200, 300, fill=(120, 116, 118, 120), width=px(5)), 2)    # sheen
    kanzashi(img, 182, 118, 1.35, -.6)
    d = ImageDraw.Draw(img)
    for ex in (130, 170):   # bright eyes, a wide smile
        d.ellipse([px(ex - 9), px(170), px(ex + 9), px(188)], fill=(22, 14, 12, 255)); d.ellipse([px(ex - 5), px(172), px(ex - 1), px(177)], fill=(255, 255, 255, 230))
        d.arc([px(ex - 11), px(164), px(ex + 11), px(182)], 200, 340, fill=(30, 20, 18, 255), width=px(2))
    d.chord([px(138), px(200), px(162), px(220)], 0, 180, fill=(150, 40, 46, 255))
    d.arc([px(138), px(200), px(162), px(220)], 0, 180, fill=(110, 30, 34, 255), width=px(2))
    save(img, 'm_s3_haru')


# ───────────── Relics: 7 things, one per chapter ─────────────
def item_img(w, h, fn):
    img = I.canvas(w, h); fn(img)
    out = img.resize((w, h), Image.LANCZOS); a = np.asarray(out, np.float32)
    lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True); a[..., :3] = lum + (a[..., :3] - lum) * .9
    a[..., :3] += np.random.default_rng(w * h).normal(0, 3.5, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def case(img):    # empty black lacquer case, lid propped behind, red silk inside with the pressed print of a plum blossom
    I.floor_shadow(img, 90, 104, 80)
    I.fill(img, '#1c1412', 501, poly=[(26, 14), (150, 4), (156, 46), (32, 58)], scale=5, contrast=.6); I.volume(img, (26, 4, 156, 58), .5, .25, .2)
    I.line(img, [(30, 18), (150, 8)], '#a07a3a', 1.6)
    I.fill(img, '#1a1210', 502, poly=[(8, 52), (172, 52), (166, 102), (14, 102)], scale=5, contrast=.6); I.volume(img, (8, 52, 172, 102), .5, .3, .25)
    I.fill(img, '#9a1e22', 503, poly=[(20, 58), (160, 58), (154, 86), (26, 86)], scale=3, stretch=(3, 1), contrast=1.3, light=.3)
    soft(img, lambda d: [d.line([(px(30), px(62 + k * 6)), (px(150), px(60 + k * 6))], fill=(230, 120, 110, 50), width=px(1.4)) for k in range(4)], .8)
    # the pressed print: a pin line, a blossom, a round dent
    soft(img, lambda d: [d.line([(px(44), px(78)), (px(118), px(66))], fill=(60, 10, 12, 170), width=px(3)), d.ellipse([px(116), px(60), px(134), px(76)], fill=(60, 10, 12, 140)),
                         d.ellipse([px(126), px(76), px(136), px(86)], fill=(60, 10, 12, 150))], .7)
    I.line(img, [(8, 52), (172, 52)], '#c9a24a', 1.6); I.line(img, [(14, 100), (166, 100)], '#6a4a20', 1.2)


def kitsunebi(img):   # small paper lantern lit by a blue fox-fire, a fox face brushed on it
    glow(img, 55, 112, 64, hexc('#7ac8ff'), 110)
    I.line(img, [(55, 2), (55, 30)], '#5a4a36', 2)
    m = I.fill(img, '#dfe8ee', 504, ell=(10, 40, 100, 190), scale=4, contrast=.5, dark=.2, light=.35); I.volume(img, (10, 40, 100, 190), -.2, .25, .15)
    soft(img, lambda d: d.ellipse([px(26), px(78), px(84), px(160)], fill=(120, 200, 255, 160)), 10)
    soft(img, lambda d: d.polygon([(px(48), px(150)), (px(55), px(104)), (px(64), px(150))], fill=(170, 230, 255, 220)), 3)
    for k in range(1, 8): I.line(img, [(14, 40 + k * 19), (55, 37 + k * 19 + 6), (96, 40 + k * 19)], (110, 120, 130, 120), 1)
    I.line(img, [(32, 104), (46, 98)], '#a0281e', 2.6); I.line(img, [(64, 98), (78, 104)], '#a0281e', 2.6)   # a fox mask in red brush
    I.line(img, [(30, 90), (36, 70), (46, 86)], '#a0281e', 2); I.line(img, [(64, 86), (74, 70), (80, 90)], '#a0281e', 2)
    I.ell(img, (52, 116, 58, 122), '#a0281e')
    for y in (30, 182): I.fill(img, '#2a1c14', 505 + y, rect=(30, y, 80, y + 10), scale=3); I.volume(img, (30, y, 80, y + 10), .4, .2)


def geta(img):    # a child's geta with a red hanao, dark from a hundred years under water, a strand of pond weed
    I.floor_shadow(img, 75, 92, 62)
    I.fill(img, '#5a4a32', 506, poly=[(14, 46), (136, 34), (142, 54), (18, 70)], scale=6, stretch=(4, 1), contrast=1.1); I.volume(img, (14, 34, 142, 70), .5, .3)
    for x0 in (36, 104): I.fill(img, '#3a2e20', 507 + x0, poly=[(x0 - 8, 62), (x0 + 8, 60), (x0 + 8, 88), (x0 - 8, 90)], scale=4); I.volume(img, (x0 - 8, 60, x0 + 8, 90), .4, .3)
    I.line(img, [(28, 54), (50, 30), (76, 40)], '#b8302a', 6); I.line(img, [(124, 44), (100, 24), (76, 40)], '#b8302a', 6)
    I.line(img, [(32, 50), (50, 33)], '#e2726a', 1.6)
    I.ell(img, (72, 36, 80, 44), '#7a1c18')
    soft(img, lambda d: d.line([(px(120), px(40)), (px(132), px(60)), (px(124), px(78)), (px(134), px(94))], fill=(80, 120, 60, 200), width=px(3)), .6)


def mouse(img):   # a faded chirimen cloth mouse, a cat's toy, one ear chewed, a red thread tail
    I.floor_shadow(img, 64, 82, 54)
    I.line(img, [(108, 66), (124, 58), (130, 70), (140, 62)], '#b8302a', 2.2)
    m = I.fill(img, '#b9a48e', 508, ell=(12, 26, 112, 82), scale=3, contrast=1.3, light=.3); I.volume(img, (12, 26, 112, 82), .6, .35, .1)
    rnd = random.Random(509)
    for _ in range(26):
        x, y = rnd.uniform(18, 108), rnd.uniform(30, 80); I.ell(img, (x - 2, y - 2, x + 2, y + 2), (150, 120, 150, 120))
    I.fill(img, '#c9b29a', 510, ell=(20, 14, 44, 38), scale=3); I.ell(img, (25, 19, 39, 33), '#d89a92')
    I.fill(img, '#c9b29a', 511, poly=[(42, 12), (60, 10), (62, 26), (56, 22), (52, 30), (44, 28)], scale=3); I.ell(img, (46, 15, 56, 25), '#d89a92')
    I.ell(img, (14, 52, 19, 57), '#1a1210'); I.ell(img, (9, 56, 13, 60), '#5a3a3a')
    I.line(img, [(10, 58), (2, 54)], (60, 50, 40, 160), 1); I.line(img, [(10, 59), (2, 62)], (60, 50, 40, 160), 1)


def ame(img):     # chitose-ame: the long Shichi-go-san candy bag with crane and turtle, red and white sticks poking out
    I.floor_shadow(img, 48, 214, 40)
    for k, (x, c) in enumerate(((34, '#efe8de'), (50, '#c8342c'), (62, '#efe8de'))): I.fill(img, c, 512 + k, rect=(x - 5, 6 + k * 6, x + 5, 70), scale=3, stretch=(1, 4)); I.volume(img, (x - 5, 6, x + 5, 70), .5, .3, .25)
    m = I.fill(img, '#efe4cc', 516, poly=[(12, 46), (84, 42), (88, 210), (8, 212)], scale=5, stretch=(1, 3), contrast=.8); I.volume(img, (8, 42, 88, 212), .5, .3)
    I.fill(img, '#c8342c', 517, rect=(12, 46, 84, 64), scale=4); I.line(img, [(10, 64), (86, 62)], '#c9a24a', 2)
    text(img, '千', 48, 86, 18, '#2a1a12', SERIF, brush=True); text(img, '歳', 48, 108, 18, '#2a1a12', SERIF, brush=True); text(img, '飴', 48, 130, 18, '#2a1a12', SERIF, brush=True)
    d = ImageDraw.Draw(img)   # crane: white body, black neck, red crown; turtle below in green
    d.ellipse([px(22), px(150), px(48), px(166)], fill=(250, 248, 240, 255)); d.line([(px(44), px(154)), (px(58), px(140))], fill=(20, 16, 16, 255), width=px(2.4))
    d.ellipse([px(56), px(136), px(62), px(142)], fill=(200, 40, 40, 255)); d.polygon([(px(26), px(156)), (px(10), px(144)), (px(30), px(150))], fill=(240, 236, 226, 255))
    d.ellipse([px(38), px(178), px(72), px(198)], fill=(70, 110, 70, 255)); d.ellipse([px(70), px(184), px(78), px(192)], fill=(90, 130, 80, 255))
    for x, y in ((46, 184), (56, 182), (64, 188)): d.ellipse([px(x - 3), px(y - 3), px(x + 3), px(y + 3)], outline=(40, 70, 40, 255), width=px(1))


def hashi(img):   # a child's red lacquer chopsticks on a little rest shaped like a plum blossom
    I.floor_shadow(img, 92, 64, 84)
    for k, dy in enumerate((0, 10)):
        I.fill(img, '#a8221e', 518 + k, poly=[(10, 34 + dy), (168, 20 + dy), (170, 25 + dy), (12, 40 + dy)], scale=3, stretch=(6, 1), light=.35); I.volume(img, (10, 20 + dy, 170, 40 + dy), .5, .2, .3)
        I.fill(img, '#1a1210', 520 + k, poly=[(10, 34 + dy), (40, 31 + dy), (41, 37 + dy), (12, 40 + dy)], scale=3)
        I.line(img, [(120, 25 + dy), (128, 24 + dy)], '#d8b048', 1.6)
    d = ImageDraw.Draw(img); flower(d, 142, 52, 8, (236, 228, 214, 255), center=(200, 160, 70, 255))
    I.volume(img, (128, 38, 156, 66), .5, .3, .2)


def kaza(img):    # Haru's pinwheel on a bamboo stick
    I.floor_shadow(img, 56, 196, 30)
    I.line(img, [(56, 196), (56, 64)], '#8a6a3a', 4); I.line(img, [(54, 190), (54, 70)], '#b8945a', 1.2)
    for y in (110, 150): I.line(img, [(52, y), (60, y)], '#5a4426', 2)
    pinwheel(img, 56, 56, 48, 522)
    soft(img, lambda d: d.arc([px(6), px(6), px(106), px(106)], 200, 320, fill=(255, 240, 220, 80), width=px(3)), 2)


RELICS = [('s3_case', 180, 110, case), ('s3_fox', 110, 200, kitsunebi), ('s3_geta', 150, 100, geta), ('s3_mouse', 144, 92, mouse),
          ('s3_ame', 96, 220, ame), ('s3_hashi', 180, 74, hashi), ('s3_kaza', 112, 204, kaza)]


def atlas():
    ims = [(iid, item_img(w, h, fn)) for iid, w, h, fn in RELICS]
    W = sum(im.width for _, im in ims) + 4 * (len(ims) - 1); H = max(im.height for _, im in ims)
    at = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x = 0; rects = {}
    for iid, im in ims: at.alpha_composite(im, (x, 0)); rects[iid] = [x, 0, im.width, im.height]; x += im.width + 4
    at.save(f'{ITEM_DIR}/atlas_s3.webp', 'WEBP', quality=88, alpha_quality=92, method=6)
    print(json.dumps({'atlas': [W, H], 'rects': rects}))


if __name__ == '__main__':
    haru(); atlas()
