#!/usr/bin/env python3
"""«Ночной парад ста демонов» (feat/parade.js): three parade extras + the parade's things.
chōchin-kozō (lantern bearer), biwa-bokuboku, wanyūdō → assets/mon/m_pd_*.webp;
12 month emaki scrolls + 5 souvenirs packed into assets/items/atlas_pd.webp (rect map printed as JSON → feat/parade.js).
Same organic spline toolkit as story_art.py / visitors_art.py.
Usage: parade_art.py <assets dir>"""
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
from guests_art import stroke, tube
import items as I

SKIN_RED = hexc('#cf6a4c')


def glow_blob(img, cx, cy, r, col, a, blur):
    soft(img, lambda d: d.ellipse([px(cx - r), px(cy - r), px(cx + r), px(cy + r)], fill=col + (a,)), blur)


def lantern(img, cx, cy, rw, rh, seed, kanji='百'):
    """A lit paper chōchin: warm paper, ribs, dark caps, an ink kanji."""
    glow_blob(img, cx, cy, rw * 1.9, (255, 196, 110), 70, 18)
    m = shape(img, hexc('#f2c46e'), seed, ell=(cx - rw, cy - rh, cx + rw, cy + rh), scale=5, contrast=.7, dk=.25, lt=.35, k=.35, rim=.35)
    def ribs(d, l):
        for k in range(1, 9):
            y = cy - rh + 2 * rh * k / 9; d.line([(px(cx - rw - 4), px(y)), (px(cx + rw + 4), px(y))], fill=(150, 90, 40, 150), width=px(1.3))
    clipped(img, m, ribs)
    clipped(img, m, lambda d, l: d.ellipse([px(cx - rw * .55), px(cy - rh * .5), px(cx + rw * .55), px(cy + rh * .55)], fill=(255, 236, 170, 120)))
    I.text(img, kanji, cx, cy + 2, rw * 1.05, '#3a1408', I.SERIF, brush=True)
    d = ImageDraw.Draw(img)
    for y, h in ((cy - rh - 7, 10), (cy + rh - 3, 10)): d.rounded_rectangle([px(cx - rw * .55), px(y), px(cx + rw * .55), px(y + h)], px(3), fill=(24, 16, 12, 255))


def closed_eye(d, x, y, r, col=(40, 20, 16, 255), w=3.2):
    stroke(d, [(x - r, y - 1), (x, y + r * .45), (x + r, y - 1)], col, w)


# ───────────── Chōchin-kozō: the red-faced lantern boy of Sendai, walks ahead of travellers ─────────────
def bearer():
    img = canvas(320, 520); cx = 196
    # pole over the shoulder and the lantern leading the way (they walk to the left)
    stroke(ImageDraw.Draw(img), [(214, 318), (130, 214), (40, 98)], (74, 52, 30, 255), 6)
    stroke(ImageDraw.Draw(img), [(42, 100), (44, 132)], (30, 20, 14, 255), 2)
    lantern(img, 46, 196, 34, 54, 301)
    # geta and shins
    for x in (cx - 26, cx + 22):
        shape(img, hexc('#d08a6a'), x, tube([(x, 452), (x - 1, 492)], 9, 8), scale=4, contrast=.4, k=.4, rim=.3)
        I.fill(img, '#4a3220', x + 1, poly=[(x - 22, 494), (x + 22, 494), (x + 22, 504), (x - 22, 504)], scale=3, stretch=(4, .4))
        I.fill(img, '#2e1e12', x + 2, rect=(x - 6, 504, x + 6, 516), scale=2)
        stroke(ImageDraw.Draw(img), [(x - 12, 494), (x, 486), (x + 12, 494)], (170, 40, 34, 255), 3)
    # kimono: short indigo with a hemp-leaf hint, tucked up for walking
    body = [(cx - 46, 262), (cx + 46, 262), (cx + 62, 330), (cx + 70, 420), (cx + 74, 466), (cx - 74, 466), (cx - 68, 420), (cx - 60, 330)]
    mb = shape(img, hexc('#2c3a5e'), 302, body, scale=9, contrast=.9, dk=.5, lt=.16, k=.55, rim=.35)
    def asanoha(d, l):
        for gx in range(int(cx - 80), int(cx + 80), 26):
            for gy in range(262, 470, 26):
                for a in range(0, 360, 60):
                    t = math.radians(a); d.line([(px(gx), px(gy)), (px(gx + math.cos(t) * 13), px(gy + math.sin(t) * 13))], fill=(150, 170, 210, 46), width=px(1))
    clipped(img, mb, asanoha)
    folds(img, mb, [[(cx - 20, 370), (cx - 30, 460)], [(cx + 22, 372), (cx + 36, 460)]], (0, 0, 0, 70), 4)
    I.fill(img, '#a8823c', 303, poly=[(cx - 64, 350), (cx + 64, 350), (cx + 66, 376), (cx - 66, 376)], scale=4, stretch=(4, .4))
    stroke(ImageDraw.Draw(img), [(cx - 40, 262), (cx - 4, 330)], (220, 210, 190, 255), 5)
    stroke(ImageDraw.Draw(img), [(cx + 40, 262), (cx - 4, 330)], (220, 210, 190, 255), 5)
    # arm in a sleeve, the hand on the pole
    shape(img, hexc('#283656'), 304, [(cx - 30, 272), (cx + 4, 282), (cx + 20, 312), (cx + 18, 340), (cx - 8, 344), (cx - 30, 316)], scale=8, contrast=.8, k=.5, rim=.3)
    shape(img, hexc('#d08a6a'), 305, ell=(cx + 4, 306, cx + 34, 334), scale=4, contrast=.4, k=.5, rim=.3)
    # head: a big round shaven head, red as a ripe hōzuki, eyes shut in a smile
    shape(img, SKIN_RED, 306, ell=(cx - 76, 116, cx + 76, 268), scale=7, contrast=.55, dk=.35, lt=.18, k=.6, rim=.4, spec=.18)
    for sx in (-1, 1): shape(img, mixc(SKIN_RED, (0, 0, 0, 255), .1), 307 + sx, ell=(cx + sx * 74 - 12, 186, cx + sx * 74 + 12, 214), scale=3, k=.4)
    d = ImageDraw.Draw(img)
    for sx in (-1, 1): closed_eye(d, cx + sx * 28 - 6, 196, 13)
    stroke(d, [(cx - 16, 232), (cx - 6, 238), (cx + 6, 236)], (90, 26, 20, 255), 3)
    soft(img, lambda dd: [dd.ellipse([px(cx + sx * 44 - 16), px(212), px(cx + sx * 44 + 12), px(230)], fill=(240, 110, 100, 90)) for sx in (-1, 1)], 4)
    soft(img, lambda dd: dd.ellipse([px(cx - 30), px(130), px(cx + 10), px(150)], fill=(255, 220, 190, 70)), 6)
    save(img, 'm_pd_bearer')


# ───────────── Biwa-bokuboku: a biwa lute that grew into a blind monk (Toriyama Sekien, 1784) ─────────────
def biwa_man():
    img = canvas(340, 520); cx = 170
    for x in (cx - 40, cx + 40):   # straw sandals under the robe
        I.fill(img, '#a88a50', x, ell=(x - 26, 496, x + 26, 516), scale=3, stretch=(4, .5), contrast=1.2)
    robe = [(cx - 60, 238), (cx + 60, 238), (cx + 92, 300), (cx + 116, 410), (cx + 134, 504), (cx - 134, 504), (cx - 116, 410), (cx - 92, 300)]
    mr = shape(img, hexc('#3b3631'), 311, robe, scale=10, contrast=.9, dk=.5, lt=.15, k=.55, rim=.35)
    folds(img, mr, [[(cx - 60, 330), (cx - 90, 500)], [(cx + 10, 380), (cx + 4, 500)], [(cx + 70, 340), (cx + 100, 500)]], (0, 0, 0, 80), 5)
    kesa = [(cx - 50, 240), (cx + 10, 240), (cx + 120, 440), (cx + 112, 480), (cx + 40, 470)]
    mk = shape(img, hexc('#7a5630'), 312, kesa, scale=6, contrast=1.1, dk=.4, lt=.2, k=.4, rim=.2, smooth=False)
    clipped(img, mk, lambda d, l: [d.line([(px(cx - 60 + k * 22), px(230)), (px(cx + 40 + k * 22), px(490))], fill=(40, 26, 14, 150), width=px(2)) for k in range(-2, 7)] + [d.line([(px(cx - 80), px(250 + k * 40)), (px(cx + 140), px(240 + k * 40 + 60))], fill=(40, 26, 14, 120), width=px(2)) for k in range(7)])
    # both sleeves meet in front, the bone plectrum in the hand
    for sx in (-1, 1):
        shape(img, hexc('#34302b'), 313 + sx, [(cx + sx * 56, 252), (cx + sx * 96, 300), (cx + sx * 70, 370), (cx + sx * 20, 388), (cx + sx * 8, 350), (cx + sx * 40, 300)], scale=8, contrast=.8, k=.5, rim=.3)
    shape(img, hexc('#c9a888'), 315, ell=(cx - 18, 340, cx + 14, 372), scale=4, contrast=.4, k=.5, rim=.3)
    shape(img, hexc('#ece2c8'), 316, [(cx - 8, 352), (cx + 40, 318), (cx + 52, 334), (cx + 4, 366)], scale=3, contrast=.4, k=.5, rim=.2, smooth=False)
    # the head is the biwa: a pear-shaped body, bent neck with pegs, strings over the "face"
    neck = [(cx - 14, 30), (cx + 14, 30), (cx + 18, 120), (cx - 18, 120)]
    shape(img, hexc('#5e3a1c'), 317, neck, scale=4, stretch=(.4, 3), contrast=1.1, k=.5, rim=.3, smooth=False)
    shape(img, hexc('#4a2c14'), 318, [(cx - 12, 34), (cx + 30, 6), (cx + 44, 18), (cx + 8, 46)], scale=3, k=.4, smooth=False)
    for k in range(4):
        y = 14 + k * 9; I.fill(img, '#2a1a0e', 319 + k, ell=(cx + 10 + k * 8 - 18, y - 4, cx + 10 + k * 8 + 18, y + 4), scale=2)
    pear = [(cx, 88), (cx + 42, 112), (cx + 74, 168), (cx + 84, 222), (cx + 64, 262), (cx, 276), (cx - 64, 262), (cx - 84, 222), (cx - 74, 168), (cx - 42, 112)]
    mp = shape(img, hexc('#9a6534'), 323, pear, scale=8, stretch=(1, 2.4), contrast=1.0, dk=.42, lt=.22, k=.55, rim=.45, spec=.15)
    clipped(img, mp, lambda d, l: [d.line([(px(cx - 90 + k * 12), px(80)), (px(cx - 70 + k * 12), px(290))], fill=(70, 40, 18, 60), width=px(1.4)) for k in range(16)])
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):   # crescent sound holes: closed blind eyes
        d.chord([px(cx + sx * 36 - 18), px(160), px(cx + sx * 36 + 18), px(186)], 0, 180, fill=(30, 16, 8, 255))
    stroke(d, [(cx - 40, 128), (cx - 24, 134)], (60, 34, 16, 255), 3); stroke(d, [(cx + 24, 134), (cx + 40, 128)], (60, 34, 16, 255), 3)
    I.fill(img, '#2a1a0e', 324, rect=(cx - 40, 232, cx + 40, 244), scale=2)   # the bridge — a stern mouth
    for k in range(4):
        x = cx - 9 + k * 6; d.line([(px(x), px(36)), (px(cx - 26 + k * 17), px(236))], fill=(226, 214, 180, 200), width=px(1.1))
    for y in (124, 146, 170, 196): d.line([(px(cx - 14), px(y)), (px(cx + 14), px(y))], fill=(60, 36, 16, 230), width=px(4))   # frets
    save(img, 'm_pd_biwa')


# ───────────── Wanyūdō: a burning ox-cart wheel with a monk's head (Kyoto, Sekien 1776) ─────────────
def wanyudo():
    img = canvas(460, 460); cx, cy = 230, 236
    rnd = random.Random(331)
    soft(img, lambda d: d.ellipse([px(cx - 226), px(cy - 226), px(cx + 226), px(cy + 226)], fill=(255, 120, 40, 60)), 22)
    def flames(R0, R1, n, cols, wid):
        l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l)
        for i in range(n):
            a = i / n * math.tau + rnd.uniform(-.08, .08); nx, ny = math.cos(a), math.sin(a)
            ux, uy = nx * .55, ny * .55 - .7; L = math.hypot(ux, uy); ux, uy = ux / L, uy / L        # tongues lean upwards
            r0 = R0 + rnd.uniform(-6, 6); h = rnd.uniform(.6, 1) * (R1 - R0) * (1.25 if ny < 0 else .8)
            bx, by = cx + nx * r0, cy + ny * r0; w = wid * rnd.uniform(.7, 1.2)
            pts = [(bx - uy * w, by + ux * w), (bx + ux * h * .5 - uy * w * .7 + rnd.uniform(-6, 6), by + uy * h * .5 + ux * w * .7), (bx + ux * h, by + uy * h),
                   (bx + ux * h * .5 + uy * w * .7, by + uy * h * .5 - ux * w * .7), (bx + uy * w, by - ux * w)]
            d.polygon([(px(x), px(y)) for x, y in cr(pts, 6)], fill=rnd.choice(cols))
        img.alpha_composite(l.filter(ImageFilter.GaussianBlur(1.6 * M.S)))
    flames(176, 236, 34, [(170, 40, 24, 230), (196, 62, 26, 230)], 26)
    flames(182, 220, 30, [(236, 120, 40, 235), (246, 150, 50, 230)], 18)
    flames(188, 206, 26, [(255, 214, 120, 230), (255, 236, 170, 220)], 10)
    # the wheel: wooden rim with iron bands, spokes
    ring = Image.new('L', img.size, 0); dr = ImageDraw.Draw(ring)
    dr.ellipse([px(cx - 196), px(cy - 196), px(cx + 196), px(cy + 196)], fill=255); dr.ellipse([px(cx - 162), px(cy - 162), px(cx + 162), px(cy + 162)], fill=0)
    for k in range(12):
        a = k / 12 * math.tau + .13; dr.line([(px(cx + math.cos(a) * 60), px(cy + math.sin(a) * 60)), (px(cx + math.cos(a) * 170), px(cy + math.sin(a) * 170))], fill=255, width=px(17))
    ring = ring.filter(ImageFilter.GaussianBlur(.6 * M.S))
    I.fill(img, '#4e3220', 332, mask=ring, scale=6, contrast=1.2, dark=.5, light=.18)
    def bands(d, l):
        for k in range(8):
            a = k / 8 * math.tau; d.line([(px(cx + math.cos(a) * 160), px(cy + math.sin(a) * 160)), (px(cx + math.cos(a) * 198), px(cy + math.sin(a) * 198))], fill=(30, 26, 26, 255), width=px(9))
        d.ellipse([px(cx - 194), px(cy - 194), px(cx + 194), px(cy + 194)], outline=(255, 150, 70, 120), width=px(3))
    clipped(img, ring, bands)
    # the head in the hub: a bald old monk, bushy brows, grey beard, eyes slid to the side
    shape(img, hexc('#8c8680'), 333, [(cx - 92, cy + 10), (cx - 70, cy + 92), (cx, cy + 124), (cx + 70, cy + 92), (cx + 92, cy + 10), (cx, cy + 50)], scale=5, stretch=(.5, 2), contrast=1.2, k=.4, rim=.3)
    shape(img, hexc('#c99c76'), 334, ell=(cx - 84, cy - 104, cx + 84, cy + 76), scale=7, contrast=.55, dk=.35, lt=.18, k=.6, rim=.45, spec=.15)
    mb = shape(img, hexc('#9a948c'), 335, [(cx - 76, cy + 20), (cx - 50, cy + 82), (cx, cy + 106), (cx + 50, cy + 82), (cx + 76, cy + 20), (cx + 40, cy + 40), (cx, cy + 34), (cx - 40, cy + 40)], scale=4, stretch=(.4, 2.5), contrast=1.3, k=.4, rim=.3)
    clipped(img, mb, lambda d, l: [d.line([(px(cx + x), px(cy + 30)), (px(cx + x * 1.1), px(cy + 110))], fill=(220, 214, 204, 110), width=px(1.2)) for x in range(-70, 72, 7)])
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        ex, ey = cx + sx * 34, cy - 18
        d.ellipse([px(ex - 17), px(ey - 10), px(ex + 17), px(ey + 10)], fill=(244, 230, 200, 255))
        d.ellipse([px(ex - 15), px(ey - 8), px(ex - 1), px(ey + 6)], fill=(40, 22, 14, 255)); d.ellipse([px(ex - 11), px(ey - 6), px(ex - 6), px(ey - 2)], fill=(255, 240, 210, 220))
        stroke(d, [(ex - 19, ey - 3), (ex, ey - 12), (ex + 19, ey - 4)], (70, 40, 26, 255), 3)
        poly_s(d, [(cx + sx * 12, ey - 26), (cx + sx * 34, ey - 40), (cx + sx * 62, ey - 34), (cx + sx * 56, ey - 22), (cx + sx * 30, ey - 24)], (226, 222, 214, 255), 5)
    poly_s(d, [(cx - 8, cy - 4), (cx, cy + 20), (cx + 12, cy + 16)], (150, 100, 76, 255), 4)
    stroke(d, [(cx - 30, cy + 44), (cx, cy + 38), (cx + 30, cy + 44)], (80, 36, 26, 255), 4)
    soft(img, lambda dd: dd.ellipse([px(cx - 44), px(cy - 96), px(cx + 4), px(cy - 64)], fill=(255, 230, 200, 80)), 7)
    soft(img, lambda dd: dd.ellipse([px(cx - 80), px(cy + 10), px(cx + 80), px(cy + 80)], fill=(255, 130, 50, 40)), 12)
    save(img, 'm_pd_wanyudo')


# ───────────── things: month emaki scrolls + souvenirs ─────────────
def item_done(img):
    out = img.resize((P.W, P.H), Image.LANCZOS); a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .88; a[..., :3] += np.random.default_rng(7).normal(0, 3.5, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


NUM = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二']
SEASON = {12: 'w', 1: 'w', 2: 'w', 3: 'sp', 4: 'sp', 5: 'sp', 6: 'su', 7: 'su', 8: 'su', 9: 'au', 10: 'au', 11: 'au'}
MOUNT = {'w': '#3a4a6a', 'sp': '#8a4a5a', 'su': '#2f5a4a', 'au': '#7a3a22'}


def emaki(mo):
    """A small unrolled hand-scroll: ink procession, lantern dots, a month seal and a seasonal touch."""
    img = I.canvas(230, 110); s = SEASON[mo]; rnd = random.Random(mo * 17)
    I.fill(img, MOUNT[s], 400 + mo, rect=(6, 16, 224, 98), scale=4, contrast=1.1)
    I.fill(img, '#e8dec4', 401 + mo, rect=(20, 20, 210, 94), scale=8, contrast=.6, dark=.14, light=.1)
    for x in (2, 214):
        I.fill(img, '#2a1c12', 402 + x, rect=(x, 10, x + 14, 104), scale=3); I.volume(img, (x, 10, x + 14, 104), k=.6, rim=.3)
        I.ell(img, (x + 2, 2, x + 12, 12), '#1a120c'); I.ell(img, (x + 2, 100, x + 12, 110), '#1a120c')
    ink = (34, 28, 26, 225); d = ImageDraw.Draw(img); x = 182
    kinds = ['kasa', 'head', 'tall', 'wheel', 'lamp', 'head', 'tall', 'kasa', 'lamp']; rnd.shuffle(kinds)
    for k in kinds:
        y = 82 + rnd.uniform(-2, 2)
        if k == 'kasa': d.polygon([(px(x), px(y - 34)), (px(x - 10), px(y - 14)), (px(x + 10), px(y - 14))], fill=ink); d.line([(px(x), px(y - 14)), (px(x), px(y))], fill=ink, width=px(2))
        elif k == 'head': d.ellipse([px(x - 7), px(y - 30), px(x + 7), px(y - 16)], fill=ink); d.polygon([(px(x - 9), px(y)), (px(x - 5), px(y - 16)), (px(x + 5), px(y - 16)), (px(x + 9), px(y))], fill=ink)
        elif k == 'tall': d.ellipse([px(x - 5), px(y - 40), px(x + 5), px(y - 30)], fill=ink); d.polygon([(px(x - 10), px(y)), (px(x - 4), px(y - 30)), (px(x + 4), px(y - 30)), (px(x + 10), px(y))], fill=ink)
        elif k == 'wheel':
            d.ellipse([px(x - 12), px(y - 26), px(x + 12), px(y - 2)], outline=ink, width=px(2))
            for a in range(0, 180, 45): t = math.radians(a); d.line([(px(x - math.cos(t) * 12), px(y - 14 - math.sin(t) * 12)), (px(x + math.cos(t) * 12), px(y - 14 + math.sin(t) * 12))], fill=ink, width=px(1))
        else: d.ellipse([px(x - 4), px(y - 36), px(x + 4), px(y - 24)], fill=ink); d.line([(px(x), px(y - 24)), (px(x - 3), px(y))], fill=ink, width=px(2))
        if k in ('lamp', 'kasa', 'tall'):
            lx, ly = x - 8, y - 44; glow_blob(img, lx, ly, 8, (255, 180, 80), 120, 3); d = ImageDraw.Draw(img); d.ellipse([px(lx - 3), px(ly - 4), px(lx + 3), px(ly + 4)], fill=(240, 150, 60, 255))
        x -= 17 + rnd.uniform(-1, 2)
    soft(img, lambda dd: dd.rectangle([px(20), px(80), px(210), px(94)], fill=(170, 170, 160, 90)), 4)   # mist along the road
    d = ImageDraw.Draw(img)
    if s == 'sp':
        for _ in range(9): x, y = rnd.uniform(24, 90), rnd.uniform(24, 46); d.ellipse([px(x - 3), px(y - 2), px(x + 3), px(y + 2)], fill=(226, 150, 170, 220))
    elif s == 'su':
        for _ in range(6): x, y = rnd.uniform(24, 80), rnd.uniform(24, 44); d.ellipse([px(x - 4), px(y - 2), px(x + 4), px(y + 2)], fill=(90, 130, 80, 220))
    elif s == 'au':
        for _ in range(7):
            x, y = rnd.uniform(24, 90), rnd.uniform(24, 48)
            d.polygon([(px(x + math.cos(t) * (4 if j % 2 else 1.6)), px(y + math.sin(t) * (4 if j % 2 else 1.6))) for j, t in enumerate(np.linspace(0, math.tau, 10, endpoint=False))], fill=(190, 70, 40, 230))
    else:
        for _ in range(16): x, y = rnd.uniform(22, 208), rnd.uniform(22, 70); d.ellipse([px(x - 1.6), px(y - 1.6), px(x + 1.6), px(y + 1.6)], fill=(250, 250, 250, 210))
    d.ellipse([px(150), px(26), px(166), px(42)], fill=(60, 56, 70, 120))   # the dark new moon
    I.fill(img, '#b3302b', 403, rect=(188, 24, 206, 42), scale=2)
    I.text(img, NUM[mo - 1], 197, 33, 11 if mo < 11 else 7, '#f4e8d8', I.SANS)
    I.text(img, '月', 197, 52, 11, '#2a2020', I.SERIF, brush=True)
    return item_done(img)


def s_kasa():   # a toy karakasa-obake: closed paper umbrella on one leg, one eye
    img = I.canvas(96, 200); I.floor_shadow(img, 48, 192, 30)
    I.fill(img, '#6a4a2a', 1, rect=(44, 150, 52, 186), scale=3)
    I.fill(img, '#3a2618', 2, poly=[(30, 184), (66, 184), (64, 194), (32, 194)], scale=3)
    m = I.fill(img, '#3a4e7a', 3, poly=[(48, 6), (64, 40), (74, 120), (66, 150), (30, 150), (22, 120), (32, 40)], scale=5, stretch=(.4, 2), contrast=1.1)
    clipped(img, m, lambda d, l: [d.line([(px(48), px(6)), (px(26 + k * 11), px(152))], fill=(18, 24, 40, 150), width=px(1.4)) for k in range(5)])
    I.volume(img, (22, 6, 74, 150), k=.55, rim=.35)
    d = ImageDraw.Draw(img); d.ellipse([px(36), px(66), px(60), px(86)], fill=(244, 238, 226, 255)); d.ellipse([px(43), px(70), px(55), px(82)], fill=(40, 24, 18, 255))
    d.ellipse([px(45), px(72), px(49), px(76)], fill=(255, 255, 255, 230))
    shape(img, hexc('#d9606e'), 4, tube([(50, 100), (54, 118), (64, 128)], 6, 4), scale=3, k=.4, rim=.3)
    I.line(img, [(26, 132), (48, 138), (70, 132)], '#c9a24a', 3)
    return item_done(img)


def s_taiko():   # a little óni drum on a stand with two sticks
    img = I.canvas(170, 160); I.floor_shadow(img, 85, 152, 64)
    for x0, x1 in ((40, 26), (130, 144)): I.line(img, [(x0, 100), (x1, 150)], '#3a2416', 7)
    I.fill(img, '#8a2a20', 1, rect=(30, 40, 140, 112), scale=5, stretch=(4, .5)); I.volume(img, (30, 40, 140, 112), k=.6, rim=.4, spec=.15)
    I.fill(img, '#e2d2b0', 2, ell=(22, 30, 62, 122), scale=4); I.volume(img, (22, 30, 62, 122), k=.4, rim=.3)
    d = ImageDraw.Draw(img)
    for k in range(10): a = k / 10 * math.tau; d.ellipse([px(42 + math.cos(a) * 18 - 2), px(76 + math.sin(a) * 42 - 2), px(42 + math.cos(a) * 18 + 2), px(76 + math.sin(a) * 42 + 2)], fill=(30, 22, 18, 255))
    for k in range(3):   # three dark tomoe drops of the drum crest
        a = k / 3 * math.tau - .5; x, y = 42 + math.cos(a) * 6, 76 + math.sin(a) * 15
        d.ellipse([px(x - 4.5), px(y - 8), px(x + 4.5), px(y + 8)], fill=(46, 24, 20, 255))
        stroke(d, [(x, y), (42 + math.cos(a + 1.2) * 9, 76 + math.sin(a + 1.2) * 22)], (46, 24, 20, 255), 2.4)
    for x0 in (96, 116): I.line(img, [(x0, 8), (x0 + 30, 34)], '#c9a070', 5)
    return item_done(img)


def s_bell():   # three shrine bells on a red-and-white cord
    img = I.canvas(96, 200)
    I.line(img, [(48, 0), (48, 70)], '#b8322a', 4); I.line(img, [(51, 0), (51, 70)], '#efe6d6', 2)
    for (x, y) in ((48, 92), (28, 126), (68, 126)):
        I.line(img, [(48, 70), (x, y - 16)], '#b8322a', 2)
        I.fill(img, '#d8b048', x, ell=(x - 17, y - 17, x + 17, y + 17), scale=3, contrast=1.2); I.volume(img, (x - 17, y - 17, x + 17, y + 17), k=.7, rim=.4, spec=.45)
        d = ImageDraw.Draw(img); d.line([(px(x - 14), px(y + 3)), (px(x + 14), px(y + 3))], fill=(90, 60, 14, 255), width=px(2)); d.ellipse([px(x - 3), px(y + 5), px(x + 3), px(y + 11)], fill=(50, 30, 8, 255))
    for k in range(9): I.line(img, [(48, 146), (40 + k * 2, 194)], '#a02a22' if k % 2 else '#c8402e', 2)
    I.fill(img, '#7a1e18', 9, rect=(42, 140, 54, 152), scale=2)
    return item_done(img)


def s_wheel():   # a little cart wheel with embers still glowing in it
    img = I.canvas(170, 170); I.floor_shadow(img, 85, 164, 60)
    glow_blob(img, 85, 86, 70, (255, 120, 40), 60, 10)
    ring = Image.new('L', img.size, 0); dr = ImageDraw.Draw(ring)
    dr.ellipse([px(14), px(14), px(156), px(156)], fill=255); dr.ellipse([px(30), px(30), px(140), px(140)], fill=0)
    for k in range(8): a = k / 8 * math.tau; dr.line([(px(85 + math.cos(a) * 18), px(85 + math.sin(a) * 18)), (px(85 + math.cos(a) * 62), px(85 + math.sin(a) * 62))], fill=255, width=px(8))
    dr.ellipse([px(66), px(66), px(104), px(104)], fill=255)
    I.fill(img, '#5a3a24', 1, mask=ring.filter(ImageFilter.GaussianBlur(.5 * M.S)), scale=5, contrast=1.2, dark=.5, light=.2)
    I.volume(img, (14, 14, 156, 156), k=.5, rim=.3)
    d = ImageDraw.Draw(img)
    for k in range(6): a = k / 6 * math.tau + .3; d.line([(px(85 + math.cos(a) * 70), px(85 + math.sin(a) * 70)), (px(85 + math.cos(a) * 78), px(85 + math.sin(a) * 78))], fill=(30, 26, 26, 255), width=px(6))
    rnd = random.Random(5)
    for _ in range(14):
        a = rnd.uniform(0, math.tau); r = rnd.uniform(62, 76); x, y = 85 + math.cos(a) * r, 85 + math.sin(a) * r
        glow_blob(img, x, y, 6, (255, 150, 60), 160, 2)
    soft(img, lambda dd: dd.ellipse([px(70), px(70), px(100), px(100)], fill=(255, 160, 80, 120)), 4)
    return item_done(img)


def items():
    cap = {}
    I.save = lambda img, iid, *a, **k: cap.__setitem__(iid, item_done(img))
    I.chochin('pd_chochin', 'Фонарь с парада', '#2a3a6a', '百', True, ink='#e8d8b0')
    ims = [('pd_s%02d' % mo, emaki(mo)) for mo in range(1, 13)]
    ims += [('pd_chochin', cap['pd_chochin']), ('pd_kasa', s_kasa()), ('pd_taiko', s_taiko()), ('pd_bell', s_bell()), ('pd_wheel', s_wheel())]
    W = 940; x = y = rowh = 0; pos = {}
    for iid, im in ims:
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[iid] = (x, y, im.width, im.height); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for iid, im in ims: at.paste(im, pos[iid][:2])
    at.save(os.path.join(ASSETS, 'items', 'atlas_pd.webp'), 'WEBP', quality=88, alpha_quality=92, method=6)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'out'), exist_ok=True)
    at.save(os.path.join(os.path.dirname(__file__), 'out', 'pd_atlas_preview.png'))
    return {'size': [W, y + rowh], 'at': {iid: list(p) for iid, p in pos.items()}}


if __name__ == '__main__':
    for f in (bearer, biwa_man, wanyudo): f()
    print(json.dumps({'mon': M.META, 'atlas': items()}))
