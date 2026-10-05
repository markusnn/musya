#!/usr/bin/env python3
"""«Сумо с каппой» (feat/sumo.js): the night dohyō for the bout (clay ring with straw bales, the hanging tsuriyane roof
with four tassels, yōkai audience in the dark) + an atlas of 5 «Сумо» things, the chanko-nabe dish and the gyōji fan.
Same spline toolkit as story_art.py / birthday_art.py.
Usage: python3 art/sumo_art.py [bg|atlas]  → assets/bg/sm_dohyo.webp (1000×1400), assets/items/atlas_sm.webp; prints the rect map."""
import json, math, os, random, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WHAT = sys.argv[1] if len(sys.argv) > 1 else 'all'
sys.argv = [sys.argv[0], os.path.join(ROOT, 'art/out')]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc, textured_fill
from monsters import canvas, px, soft
from story_art import cr, shape, clipped, poly_s, mask_of
from items import text, SERIF

PREV = os.path.join(ROOT, 'art/out'); os.makedirs(PREV, exist_ok=True)
W_, BLK = (255, 255, 255, 255), (0, 0, 0, 255)
CLAY, SAND, STRAW = hexc('#8a6644'), hexc('#a98a62'), hexc('#bfa46a')
GOLD, LAC, PURPLE, INDIGO = hexc('#d8b048'), (24, 17, 15, 255), hexc('#4a2a5e'), hexc('#26385e')


def ell_pt(cx, cy, rx, ry, a): return (cx + rx * math.cos(a), cy + ry * math.sin(a))


def strand_line(d, x0, y0, x1, y1, col, w): d.line([(px(x0), px(y0)), (px(x1), px(y1))], fill=col, width=max(1, px(w)))


def bale(img, x, y, w, h, seed, base=STRAW):
    """One straw bale seen side-on: a rounded capsule with straw fibres and a lit top."""
    shape(img, base, seed, ell=(x - w / 2, y - h / 2, x + w / 2, y + h / 2), scale=3, stretch=(4, .4), contrast=1.4, k=.8, rim=.5, feather=.4)
    d = ImageDraw.Draw(img); r = random.Random(seed)
    for i in range(int(w / 3)):
        xx = x - w / 2 + 2 + r.random() * (w - 4); strand_line(d, xx - 2, y - h * .35, xx + 2, y + h * .3, mixc(base, BLK, .35 + r.random() * .2), .6)
    for k in (-.28, .28): strand_line(d, x + w * k, y - h * .48, x + w * k, y + h * .45, mixc(base, BLK, .6), 1.2)   # binding ropes


def bale_ring(img, cx, cy, rx, ry, n, seed, front):
    """Ring of bales along an ellipse; front=True draws only the near half (sin>0)."""
    for i in range(n):
        a = (i + .5) / n * 2 * math.pi; s = math.sin(a)
        if (s > 0) != front: continue
        x, y = ell_pt(cx, cy, rx, ry, a); dep = .75 + .25 * (s + 1) / 2
        w = 2 * math.pi * math.hypot(rx * math.sin(a), ry * math.cos(a)) / n * 1.02
        bale(img, x, y - 8 * dep, max(12, w * 1.12), 21 * dep, seed + i, mixc(STRAW, BLK, .25 * (1 - dep)))


def tassel(img, x, y0, y1, col, seed, wd=1.0):
    d = ImageDraw.Draw(img); r = random.Random(seed)
    strand_line(d, x, y0, x, y0 + 50 * wd, mixc(col, BLK, .3), 4 * wd)
    shape(img, col, seed, ell=(x - 22 * wd, y0 + 40 * wd, x + 22 * wd, y0 + 82 * wd), scale=3, k=.9, rim=.5, spec=.25, feather=.5)
    shape(img, mixc(col, GOLD, .35), seed + 1, pts=[(x - 17 * wd, y0 + 80 * wd), (x + 17 * wd, y0 + 80 * wd), (x + 19 * wd, y0 + 100 * wd), (x - 19 * wd, y0 + 100 * wd)], smooth=False, scale=3, k=.6, feather=.3)
    top = y0 + 98 * wd; m = Image.new('L', img.size, 0); md = ImageDraw.Draw(m)
    md.polygon([(px(x - 20 * wd), px(top)), (px(x + 20 * wd), px(top)), (px(x + 36 * wd), px(y1)), (px(x - 36 * wd), px(y1))], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(1.2 * P.SS))
    t = textured_fill(m.crop(m.getbbox()), col, mixc(col, BLK, .55), mixc(col, W_, .25), 3 * P.SS, seed + 2, (.3, 6), 1.6)
    img.alpha_composite(t, m.getbbox()[:2])
    for i in range(46):   # fringe strands
        u = r.random() * 2 - 1; L = y1 - top - r.random() * 18 * wd
        strand_line(d, x + u * 19 * wd, top + 2, x + u * 35 * wd + r.uniform(-3, 3), top + L, mixc(col, BLK if r.random() < .5 else W_, r.uniform(.15, .45)), .8 * wd)


def lantern(img, x, y, r, seed):
    soft(img, lambda d: d.ellipse([px(x - r * 3), px(y - r * 3), px(x + r * 3), px(y + r * 3)], fill=(255, 170, 80, 70)), r * .9)
    shape(img, hexc('#d98c45'), seed, ell=(x - r, y - r * 1.25, x + r, y + r * 1.25), scale=3, k=.3, rim=.45, lt=.45, feather=.4)
    d = ImageDraw.Draw(img)
    for yy in (y - r * 1.3, y + r * 1.15): d.rectangle([px(x - r * .6), px(yy), px(x + r * .6), px(yy + r * .2)], fill=(20, 13, 9, 255))


def audience(img, y, n, sc, seed, fog):
    r = random.Random(seed); d = ImageDraw.Draw(img); eyes = []
    for i in range(n):
        x = (i + r.random() * .6) / n * 1060 - 30; hr = (20 + r.random() * 14) * sc; yy = y + r.uniform(-8, 8) * sc
        col = mixc(hexc('#0b0b0d'), fog, r.random() * .25)
        d.ellipse([px(x - hr * 1.9), px(yy - hr * .2), px(x + hr * 1.9), px(yy + hr * 3)], fill=col)       # shoulders
        d.ellipse([px(x - hr), px(yy - hr * 1.9), px(x + hr), px(yy + hr * .1)], fill=col)                 # head
        k = r.random()
        if k < .25:   # cat / fox ears
            for s in (-1, 1): d.polygon([(px(x + s * hr * .25), px(yy - hr * 1.6)), (px(x + s * hr * .95), px(yy - hr * 1.3)), (px(x + s * hr * .85), px(yy - hr * 2.6))], fill=col)
        elif k < .38:  # oni horn
            d.polygon([(px(x - hr * .2), px(yy - hr * 1.8)), (px(x + hr * .2), px(yy - hr * 1.8)), (px(x), px(yy - hr * 2.8))], fill=col)
        elif k < .5:   # straw hat
            d.polygon([(px(x - hr * 1.8), px(yy - hr * 1.2)), (px(x + hr * 1.8), px(yy - hr * 1.2)), (px(x), px(yy - hr * 2.4))], fill=col)
        elif k < .58:  # kappa plate
            d.ellipse([px(x - hr * .7), px(yy - hr * 2.05), px(x + hr * .7), px(yy - hr * 1.6)], fill=mixc(col, hexc('#6a8a8a'), .35))
        if r.random() < .3: eyes.append((x, yy - hr * 1.0, hr))
        # warm rim from the ring light
        d.arc([px(x - hr), px(yy - hr * 1.9), px(x + hr), px(yy + hr * .1)], 200, 340, fill=(120, 80, 45, 120), width=max(1, px(1.5)))
    for x, yy, hr in eyes:
        c = (255, 214, 120, 255) if r.random() < .7 else (170, 230, 210, 255)
        soft(img, lambda d2: [d2.ellipse([px(x + s * hr * .35 - 3.2), px(yy - 2.6), px(x + s * hr * .35 + 3.2), px(yy + 2.6)], fill=c) for s in (-1, 1)], .5)


def background():
    img = canvas(1000, 1400)
    img.alpha_composite(P.gradient(hexc('#07090d'), hexc('#141110')))
    P.glow(img, 500, 860, 620, (230, 160, 80, 255), .32)
    # back wall: dark wooden pillars + lantern strings
    d = ImageDraw.Draw(img)
    for x in (40, 960): d.rectangle([px(x - 22), 0, px(x + 22), px(900)], fill=(16, 12, 10, 255))
    for row, (yb, sag, rr) in enumerate([(470, 40, 11), (560, 55, 13)]):
        pts = [(x, yb + sag * math.sin(math.pi * ((x % 333) / 333))) for x in range(-20, 1040, 6)]
        d.line([(px(a), px(b)) for a, b in pts], fill=(30, 22, 16, 255), width=px(1.5))
        for i, x in enumerate(range(10 + row * 30, 1000, 64)):
            lantern(img, x, yb + sag * math.sin(math.pi * ((x % 333) / 333)) + rr * 1.5, rr, 50 + i + row * 40)
    img.alpha_composite(P.fog_layer(hexc('#3a2e24'), 380, 700, .35, 9) if hasattr(P, 'fog_layer') else img.copy())
    audience(img, 790, 15, .9, 3, hexc('#2c2622'))
    audience(img, 860, 12, 1.15, 7, hexc('#221d1a'))
    # arena floor
    shape(img, hexc('#2a2119'), 11, pts=[(-20, 1150), (1020, 1150), (1020, 1420), (-20, 1420)], smooth=False, scale=30, stretch=(6, 1), k=.2, rim=.2, feather=0)
    # dohyō mound: side faces, front face, top
    shape(img, mixc(CLAY, BLK, .45), 12, pts=[(150, 870), (60, 1055), (-30, 1265), (-30, 1000)], smooth=False, scale=16, stretch=(1, 3), k=.3, rim=.2, feather=.5)
    shape(img, mixc(CLAY, BLK, .45), 13, pts=[(850, 870), (940, 1055), (1030, 1265), (1030, 1000)], smooth=False, scale=16, stretch=(1, 3), k=.3, rim=.2, feather=.5)
    shape(img, CLAY, 14, pts=[(60, 1052), (940, 1052), (1030, 1268), (-30, 1268)], smooth=False, scale=22, stretch=(2, 1), contrast=.9, k=.4, rim=.25, feather=.5)
    m = mask_of(img, [(60, 1052), (940, 1052), (1030, 1268), (-30, 1268)], smooth=False, feather=.5)
    clipped(img, m, lambda dd, l: [dd.line([(px(-40), px(1060 + i * 26)), (px(1040), px(1060 + i * 26))], fill=(0, 0, 0, 8 + i * 5), width=px(10)) for i in range(9)])
    shape(img, mixc(CLAY, BLK, .1), 15, pts=[(150, 870), (850, 870), (940, 1055), (60, 1055)], smooth=False, scale=12, stretch=(4, 1), k=.3, rim=.15, feather=.4)
    # brushed sand (janome) outside the ring + clay inside
    shape(img, SAND, 16, ell=(500 - 372, 962 - 84, 500 + 372, 962 + 84), scale=6, stretch=(6, 1), contrast=1.3, k=.2, rim=.25, feather=1.5)
    sm = mask_of(img, ell=(500 - 372, 962 - 84, 500 + 372, 962 + 84), feather=1.5)
    def sweeps(dd, l):
        r = random.Random(4)
        for i in range(70):
            a0 = r.random() * 2 * math.pi; rr = 340 + r.random() * 26
            dd.arc([px(500 - rr), px(962 - rr * .227), px(500 + rr), px(962 + rr * .227)], math.degrees(a0), math.degrees(a0) + 25 + r.random() * 40, fill=(235, 215, 175, 60), width=px(1.2))
    clipped(img, sm, sweeps)
    shape(img, mixc(CLAY, W_, .08), 17, ell=(500 - 326, 962 - 70, 500 + 326, 962 + 70), scale=10, stretch=(5, 1), k=.15, rim=.15, feather=1)
    P.glow(img, 500, 955, 300, (255, 205, 140, 255), .28)
    d = ImageDraw.Draw(img)
    for x, s in ((452, -1), (548, 1)): d.line([(px(x + s * 3), px(940)), (px(x - s * 2), px(985))], fill=(236, 230, 214, 230), width=px(4))   # shikiri-sen
    # straw bales: back half of the ring, square edge front row, front half of the ring
    bale_ring(img, 500, 962, 330, 72, 36, 100, False)
    for i in range(22):
        x = 72 + (i + .5) * (856 / 22); bale(img, x, 1052, 856 / 22 * 1.08, 20, 300 + i, mixc(STRAW, BLK, .1))
    for i in range(8):
        y = 878 + i * 23; bale(img, 150 - (i * 23) * 90 / 185 - 4, y, 16, 22, 400 + i, mixc(STRAW, BLK, .3))
        bale(img, 850 + (i * 23) * 90 / 185 + 4, y, 16, 22, 420 + i, mixc(STRAW, BLK, .3))
    for k, yy in enumerate((1110, 1170, 1230)):   # steps cut into the front face
        w = 120 + k * 30; shape(img, mixc(CLAY, W_, .06), 500 + k, pts=[(500 - w / 2, yy - 18), (500 + w / 2, yy - 18), (500 + w / 2 + 6, yy + 20), (500 - w / 2 - 6, yy + 20)], smooth=False, scale=6, k=.5, feather=.4)
        bale(img, 500, yy - 18, w, 12, 520 + k)
    bale_ring(img, 500, 962, 330, 72, 36, 100, True)
    # tsuriyane: the hanging roof
    P.glow(img, 500, 330, 520, (40, 30, 24, 255), .5)
    tassel(img, 215, 290, 520, hexc('#1c1c22'), 61, .8)
    tassel(img, 785, 290, 520, hexc('#d9d3c6'), 62, .8)
    shape(img, hexc('#2c2622'), 20, pts=[(40, 300), (960, 300), (860, 172), (140, 172)], smooth=False, scale=4, stretch=(.25, 6), contrast=1.5, k=.6, rim=.2, feather=.4)
    rm = mask_of(img, [(40, 300), (960, 300), (860, 172), (140, 172)], smooth=False, feather=.4)
    clipped(img, rm, lambda dd, l: [dd.line([(px(x), px(172)), (px(x + (x - 500) * .14), px(300))], fill=(0, 0, 0, 70), width=px(1.6)) for x in range(140, 870, 9)])
    shape(img, hexc('#3d2e24'), 21, pts=[(30, 298), (970, 298), (970, 318), (30, 318)], smooth=False, scale=6, stretch=(8, 1), k=.4, feather=.3)
    shape(img, hexc('#22190f'), 22, pts=[(120, 150), (880, 150), (880, 174), (120, 174)], smooth=False, scale=6, stretch=(8, 1), k=.5, feather=.3)
    for i, x in enumerate(range(240, 780, 90)):   # katsuogi log ends on the ridge
        shape(img, hexc('#2b2016'), 30 + i, ell=(x - 17, 118, x + 17, 152), scale=3, k=.8, rim=.5, feather=.3)
        d = ImageDraw.Draw(img); d.ellipse([px(x - 12), px(122), px(x + 12), px(148)], outline=GOLD, width=px(3))
    for s, x in ((-1, 150), (1, 850)):   # chigi: crossed boards at the gable ends
        for k in (-1, 1):
            shape(img, hexc('#2a1f17'), 40 + k + s, pts=[(x - 8, 178), (x + 8, 178), (x + k * 70 + 8, 52), (x + k * 70 - 8, 52)], smooth=False, scale=4, k=.6, feather=.3)
            d = ImageDraw.Draw(img); d.polygon([(px(x + k * 70 - 8), px(52)), (px(x + k * 70 + 8), px(52)), (px(x + k * 66 + 8), px(64)), (px(x + k * 66 - 8), px(64))], fill=GOLD)
    # mizuhiki-maku: the purple curtain with swags
    cm = Image.new('L', img.size, 0); cd = ImageDraw.Draw(cm)
    edge = [(x, 362 + 18 * abs(math.sin(math.pi * (x - 30) / 235))) for x in range(30, 971, 5)]
    cd.polygon([(px(30), px(318)), (px(970), px(318))] + [(px(a), px(b)) for a, b in reversed(edge)], fill=255)
    cm = cm.filter(ImageFilter.GaussianBlur(.6 * P.SS)); bb = cm.getbbox()
    img.alpha_composite(textured_fill(cm.crop(bb), PURPLE, mixc(PURPLE, BLK, .55), mixc(PURPLE, W_, .2), 4 * P.SS, 23, (.3, 4), 1.3), bb[:2])
    clipped(img, cm, lambda dd, l: [dd.line([(px(x), px(318)), (px(x), px(390))], fill=(0, 0, 0, 60 if (x // 9) % 2 else 0), width=px(4)) for x in range(30, 971, 9)])
    d = ImageDraw.Draw(img); d.line([(px(30), px(322)), (px(970), px(322))], fill=GOLD, width=px(2))
    for i, x in enumerate((147, 382, 618, 853)):   # white crests on the swags
        d.ellipse([px(x - 13), px(338), px(x + 13), px(364)], outline=(225, 218, 200, 230), width=px(3))
        d.ellipse([px(x - 5), px(346), px(x + 5), px(356)], fill=(225, 218, 200, 230))
    tassel(img, 62, 312, 640, hexc('#b23a2a'), 63, 1.05)
    tassel(img, 938, 312, 640, hexc('#2f7a6a'), 64, 1.05)
    # light from the roof onto the ring
    P.glow(img, 500, 920, 340, (255, 215, 160, 255), .12)
    out = img.resize((P.W, P.H), Image.LANCZOS)
    out = P.grade(out, lift=(10, 12, 14), sat=.86, vignette=.4)
    out = P.grain(out, 5, 33)
    dst = os.path.join(ROOT, 'assets/bg/sm_dohyo.webp')
    out.convert('RGB').save(dst, 'WEBP', quality=80, method=6)
    out.convert('RGB').resize((500, 700)).save(os.path.join(PREV, 'sm_dohyo_prev.jpg'), quality=85)
    print('bg', os.path.getsize(dst))


# ───────── things ─────────
def finish(img, seed):
    out = img.resize((P.W, P.H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(.4))
    a = np.asarray(out, np.float32); n = np.random.default_rng(seed).normal(0, 4, a.shape[:2])[..., None]
    a[..., :3] = np.clip(a[..., :3] + n, 0, 255); return Image.fromarray(a.astype(np.uint8), 'RGBA')


def shadow(img, cx, y, rx, a=90):
    soft(img, lambda d: d.ellipse([px(cx - rx), px(y - rx * .16), px(cx + rx), px(y + rx * .16)], fill=(0, 0, 0, a)), 3)


def it_dohyo():
    img = canvas(230, 130); shadow(img, 115, 118, 108, 110)
    shape(img, hexc('#3a2a1c'), 1, pts=[(8, 92), (222, 92), (222, 118), (8, 118)], smooth=False, scale=4, stretch=(6, 1), k=.5, feather=.3)
    shape(img, CLAY, 2, pts=[(40, 40), (190, 40), (214, 94), (16, 94)], smooth=False, scale=5, stretch=(4, 1), k=.6, rim=.3, feather=.4)
    shape(img, SAND, 3, pts=[(44, 40), (186, 40), (196, 62), (34, 62)], smooth=False, scale=4, stretch=(4, 1), k=.3, feather=.4)
    shape(img, mixc(CLAY, W_, .1), 4, ell=(56, 41, 174, 61), scale=4, k=.2, feather=.5)
    d = ImageDraw.Draw(img); d.ellipse([px(56), px(41), px(174), px(61)], outline=STRAW, width=px(3.5))
    d.ellipse([px(57), px(42), px(173), px(60)], outline=mixc(STRAW, BLK, .4), width=px(1))
    for x in (106, 124): d.line([(px(x), px(47)), (px(x), px(55))], fill=W_, width=px(1.5))
    d.line([(px(34), px(63)), (px(196), px(63))], fill=STRAW, width=px(3))
    for x in (20, 210):   # tiny corner posts with tassels
        d.line([(px(x), px(94)), (px(x), px(10))], fill=(40, 28, 20, 255), width=px(3))
    d.line([(px(14), px(12)), (px(216), px(12))], fill=PURPLE, width=px(7))
    for x, c in ((20, hexc('#b23a2a')), (210, hexc('#2f7a6a'))):
        d.ellipse([px(x - 5), px(15), px(x + 5), px(25)], fill=c); d.polygon([(px(x - 4), px(25)), (px(x + 4), px(25)), (px(x + 7), px(44)), (px(x - 7), px(44))], fill=c)
    return finish(img, 1)


def it_kesho():
    img = canvas(150, 210)
    d = ImageDraw.Draw(img); d.line([(px(30), px(6)), (px(75), px(0)), (px(120), px(6))], fill=(60, 40, 30, 255), width=px(2))
    shape(img, hexc('#1c1a26'), 5, pts=[(14, 8), (136, 8), (136, 26), (14, 26)], smooth=False, scale=3, stretch=(5, 1), k=.5, feather=.3)
    shape(img, INDIGO, 6, pts=[(22, 24), (128, 24), (130, 176), (20, 176)], smooth=False, scale=5, stretch=(1, 3), contrast=1.2, k=.5, rim=.3, feather=.4)
    m = mask_of(img, [(22, 24), (128, 24), (130, 176), (20, 176)], smooth=False, feather=.4)
    def emb(dd, l):
        dd.ellipse([px(48), px(46), px(102), px(100)], fill=(226, 206, 140, 255))                          # moon
        for k in range(4):
            yy = 120 + k * 13
            for x in range(14, 140, 26): dd.arc([px(x), px(yy - 9), px(x + 26), px(yy + 13)], 180, 360, fill=(220, 226, 236, 230), width=px(2.4))
        dd.rectangle([px(20), px(24), px(130), px(176)], outline=GOLD, width=px(4))
        dd.ellipse([px(66), px(60), px(84), px(78)], fill=(70, 120, 90, 255))                             # a kappa plate shape on the moon
    clipped(img, m, emb)
    r = random.Random(5)
    for i in range(70):
        x = 20 + i * 110 / 70; strand_line(d, x, 176, x + r.uniform(-1.5, 1.5), 200 + r.uniform(-4, 4), mixc(GOLD, BLK if r.random() < .4 else W_, r.uniform(.05, .35)), 1)
    return finish(img, 2)


def gunbai_fan(img, ox, oy, sc=1.0):
    """The gyōji's gunbai: a light gold-ivory lacquered face inside a thick black-lacquer rim (reads at a glance in the dark
    arena), a red sun disc with 勝, a dark wooden handle and a purple cord with a tassel."""
    X = lambda x: ox + x * sc; Y = lambda y: oy + y * sc
    shape(img, hexc('#3a281a'), 7, pts=[(X(40), Y(104)), (X(50), Y(104)), (X(51), Y(150)), (X(39), Y(150))], smooth=False, scale=3, k=.6, feather=.3)
    pts = [(X(45), Y(2)), (X(78), Y(12)), (X(88), Y(46)), (X(74), Y(86)), (X(56), Y(104)), (X(45), Y(112)), (X(34), Y(104)), (X(16), Y(86)), (X(2), Y(46)), (X(12), Y(12))]
    shape(img, LAC, 8, pts=pts, scale=4, k=.7, rim=.2, spec=.3, feather=.4)                        # black lacquer body = the rim
    cx, cy = X(45), Y(52)
    inner = [(cx + (x - cx) * .8, cy + (y - cy) * .8) for x, y in pts]
    shape(img, hexc('#ead8a2'), 11, pts=inner, scale=5, dk=.18, lt=.3, k=.5, rim=.22, spec=.45, feather=.35)   # light lacquered face
    m = mask_of(img, inner, feather=.35)
    def deco(dd, l):
        dd.line([(px(a), px(b)) for a, b in cr(inner, 8)] + [(px(inner[0][0]), px(inner[0][1]))], fill=hexc('#b08a34'), width=px(2 * sc))
        dd.ellipse([px(X(27)), px(Y(31)), px(X(63)), px(Y(67))], fill=(40, 22, 16, 255))
        dd.ellipse([px(X(29)), px(Y(33)), px(X(61)), px(Y(65))], fill=(184, 40, 32, 255))
    clipped(img, m, deco)
    text(img, '勝', X(45), Y(49), 21 * sc, (246, 232, 200, 255), SERIF)
    d = ImageDraw.Draw(img)
    d.line([(px(X(45)), px(Y(150))), (px(X(52)), px(Y(170)))], fill=PURPLE, width=px(2.5 * sc))
    d.polygon([(px(X(48)), px(Y(168))), (px(X(57)), px(Y(168))), (px(X(61)), px(Y(190))), (px(X(45)), px(Y(190)))], fill=PURPLE)


def it_gunbai():
    img = canvas(110, 215); shadow(img, 55, 205, 46)
    gunbai_fan(img, 10, 0, 1.0)
    shape(img, hexc('#3a2a1c'), 9, pts=[(14, 190), (96, 190), (100, 208), (10, 208)], smooth=False, scale=3, stretch=(5, 1), k=.6, feather=.3)
    return finish(img, 3)


def it_fan_game():
    img = canvas(92, 192); gunbai_fan(img, 1, 1, 1.0); return finish(img, 4)


def it_cup():
    img = canvas(180, 240); shadow(img, 90, 230, 80, 120)
    shape(img, LAC, 10, pts=[(28, 196), (152, 196), (160, 230), (20, 230)], smooth=False, scale=4, stretch=(5, 1), k=.6, spec=.2, feather=.3)
    d = ImageDraw.Draw(img); d.line([(px(20), px(212)), (px(160), px(212))], fill=(176, 42, 34, 255), width=px(5)); d.line([(px(20), px(219)), (px(160), px(219))], fill=(230, 226, 214, 255), width=px(4))
    SIL = hexc('#b9bcc0')
    shape(img, SIL, 11, pts=[(66, 196), (114, 196), (104, 178), (96, 150), (84, 150), (76, 178)], scale=3, k=.9, rim=.4, spec=.4, feather=.3)
    for s in (-1, 1):  # handles
        d = ImageDraw.Draw(img); cx = 90 + s * 64
        d.arc([px(cx - 22), px(36), px(cx + 22), px(96)], 270 if s > 0 else 90, 90 if s > 0 else 270, fill=mixc(SIL, BLK, .3), width=px(7))
        d.arc([px(cx - 22), px(36), px(cx + 22), px(96)], 270 if s > 0 else 90, 90 if s > 0 else 270, fill=mixc(SIL, W_, .2), width=px(3))
    shape(img, SIL, 12, pts=[(26, 30), (154, 30), (146, 92), (120, 136), (98, 152), (82, 152), (60, 136), (34, 92)], scale=14, contrast=.6, lt=.35, dk=.35, k=1.0, rim=.45, spec=.6, feather=.3)
    shape(img, mixc(SIL, BLK, .45), 13, ell=(28, 22, 152, 40), scale=3, k=.3, feather=.3)
    d = ImageDraw.Draw(img); d.ellipse([px(28), px(22), px(152), px(40)], outline=mixc(SIL, W_, .5), width=px(2.5))
    for k in range(6): d.line([(px(44 + k * 18), px(56)), (px(54 + k * 14), px(120))], fill=(255, 255, 255, 60), width=px(2))
    d.arc([px(40), px(44), px(140), px(130)], 200, 330, fill=(255, 255, 255, 120), width=px(3))
    return finish(img, 5)


def it_doll():
    img = canvas(120, 170); shadow(img, 60, 162, 44, 110)
    WOOD = hexc('#d9b98a')
    shape(img, WOOD, 14, ell=(14, 62, 106, 162), scale=5, stretch=(1, 3), k=.8, rim=.45, spec=.15, feather=.4)
    m = mask_of(img, ell=(14, 62, 106, 162), feather=.4)
    clipped(img, m, lambda dd, l: (dd.rectangle([px(0), px(122), px(120), px(146)], fill=INDIGO), dd.rectangle([px(52), px(130), px(68), px(165)], fill=INDIGO),
                                   [dd.line([(px(46 + k * 5), px(146)), (px(46 + k * 5), px(160))], fill=mixc(INDIGO, BLK, .3), width=px(2)) for k in range(6)],
                                   dd.ellipse([px(40), px(98), px(48), px(106)], fill=(150, 90, 70, 200)), dd.ellipse([px(72), px(98), px(80), px(106)], fill=(150, 90, 70, 200))))
    shape(img, WOOD, 15, ell=(30, 16, 90, 74), scale=4, k=.8, rim=.4, spec=.2, feather=.4)
    shape(img, hexc('#141012'), 16, ell=(40, 4, 80, 30), scale=3, k=.6, feather=.4)
    shape(img, hexc('#141012'), 17, pts=[(52, 8), (70, 4), (72, 14), (54, 16)], scale=2, k=.6, feather=.3)   # topknot
    d = ImageDraw.Draw(img)
    for x in (48, 72): d.arc([px(x - 6), px(40), px(x + 6), px(50)], 200, 340, fill=(30, 20, 18, 255), width=px(2.2))
    d.arc([px(53), px(52), px(67), px(62)], 20, 160, fill=(150, 50, 40, 255), width=px(2))
    for x in (38, 82): d.ellipse([px(x - 6), px(52), px(x + 6), px(60)], fill=(230, 140, 130, 110))
    return finish(img, 6)


def it_chanko():
    img = canvas(176, 132); shadow(img, 88, 120, 80, 120)
    shape(img, hexc('#3a2c24'), 18, pts=[(10, 58), (166, 58), (156, 104), (128, 120), (48, 120), (20, 104)], scale=5, k=.7, rim=.4, spec=.15, feather=.4)
    shape(img, hexc('#7a5636'), 19, ell=(12, 40, 164, 78), scale=3, k=.3, feather=.4)
    sm = mask_of(img, ell=(18, 44, 158, 74), feather=.5)
    def stew(dd, l):
        r = random.Random(9); dd.ellipse([px(18), px(44), px(158), px(74)], fill=(176, 120, 64, 255))
        for i in range(5): x = 30 + i * 26; dd.ellipse([px(x), px(48 + (i % 2) * 6), px(x + 26), px(62 + (i % 2) * 6)], fill=(214, 224, 170, 255))      # napa cabbage
        for x, y in ((44, 52), (98, 48), (128, 58)): dd.rectangle([px(x), px(y), px(x + 16), px(y + 12)], fill=(240, 236, 222, 255))                   # tofu
        for x, y in ((70, 58), (112, 62), (58, 46), (140, 50)): dd.ellipse([px(x), px(y), px(x + 14), px(y + 11)], fill=(150, 98, 60, 255))             # chicken balls
        for x, y in ((84, 46), (32, 60)): dd.ellipse([px(x), px(y), px(x + 18), px(y + 10)], fill=(92, 60, 40, 255)); dd.line([(px(x + 5), px(y + 5)), (px(x + 13), px(y + 5))], fill=(220, 200, 170, 255), width=px(1.5))
        for i in range(10): x = 24 + r.random() * 124; y = 46 + r.random() * 24; dd.ellipse([px(x), px(y), px(x + 7), px(y + 5)], outline=(110, 160, 60, 255), width=px(1.6))
    clipped(img, sm, stew)
    d = ImageDraw.Draw(img); d.ellipse([px(12), px(40), px(164), px(78)], outline=hexc('#2a1e16'), width=px(3))
    for s in (-1, 1): shape(img, hexc('#3a2c24'), 20 + s, ell=(88 + s * 82 - 9, 58, 88 + s * 82 + 9, 72), scale=2, k=.6, feather=.3)
    soft(img, lambda dd: [dd.line([(px(x + 6 * math.sin(y / 7)), px(y)) for y in range(4, 42, 3)], fill=(255, 255, 255, 70), width=px(3)) for x in (60, 92, 120)], 1.2)
    return finish(img, 7)


def atlas():
    parts = [('sm_dohyo', it_dohyo()), ('sm_kesho', it_kesho()), ('sm_gunbai', it_gunbai()), ('sm_cup', it_cup()), ('sm_doll', it_doll()),
             ('ds_sm_chanko', it_chanko()), ('sm_fan', it_fan_game())]
    x = 0; rects = {}
    for n, p in parts: rects[n] = [x, 0, p.width, p.height]; x += p.width + 2
    AW, AH = x, max(p.height for _, p in parts)
    A = Image.new('RGBA', (AW, AH), (0, 0, 0, 0))
    for n, p in parts: A.alpha_composite(p, tuple(rects[n][:2]))
    dst = os.path.join(ROOT, 'assets/items/atlas_sm.webp')
    A.save(dst, 'WEBP', quality=88, alpha_quality=92, method=6)
    pv = Image.new('RGBA', (AW, AH), (46, 44, 52, 255)); pv.alpha_composite(A); pv.save(os.path.join(PREV, 'sm_atlas_prev.png'))
    print('atlas', AW, AH, os.path.getsize(dst), json.dumps(rects))


if __name__ == '__main__':
    if WHAT in ('all', 'atlas'): atlas()
    if WHAT in ('all', 'bg'): background()
