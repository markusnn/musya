#!/usr/bin/env python3
"""«Лавка тануки» (feat/shop.js, prefix tn): the tanuki's night cart at the fair (3 frames: back, front open,
front closed) → assets/items/tn_stall.webp, and 12 rare things «Лавка тануки» → assets/items/atlas_tn.webp.
Prints the rect maps as JSON (pasted into feat/shop.js). Previews → art/out/tn_*.png.
Usage: shop_art.py [assets dir]"""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw
ASSETS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'assets')
OUTD = os.path.join(os.path.dirname(__file__), 'out'); os.makedirs(OUTD, exist_ok=True)
sys.argv = [sys.argv[0], OUTD]
import paint as P
from paint import hexc, mixc
import items as I
from items import px, fill, volume, line, ell, poly, text, soft, floor_shadow, dk, lt, H, SERIF, SANS


GLOWS = []


def done(img, sat=.9):
    if GLOWS:
        l = Image.new('RGBA', img.size, (0, 0, 0, 0))
        for x, y, r, c, a in GLOWS: soft(l, lambda d: d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=(c[0], c[1], c[2], a)), r * .45)
        l.alpha_composite(img); img = l; GLOWS.clear()
    out = img.resize((P.W, P.H), Image.LANCZOS); a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * sat; a[..., :3] += np.random.default_rng(17).normal(0, 3, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def arc(img, box, a0, a1, col, w):
    ImageDraw.Draw(img).arc([px(v) for v in box], a0, a1, fill=H(col), width=max(1, px(w)))


def glowdot(img, x, y, r, col, a=150, top=False):
    c = H(col)
    if top: soft(img, lambda d: d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=(c[0], c[1], c[2], a)), r * .45)
    else: GLOWS.append((x, y, r, c, a))      # halo: painted under the finished picture


def leaf(img, cx, cy, L, ang, col, seed):
    c, s = math.cos(ang), math.sin(ang); R = lambda x, y: (cx + x * c - y * s, cy + x * s + y * c)
    pts = [R(-L * .5, 0), R(-L * .2, -L * .24), R(L * .25, -L * .2), R(L * .5, 0), R(L * .25, L * .2), R(-L * .2, L * .24)]
    fill(img, col, seed, poly=pts, scale=3, contrast=.9)
    line(img, [R(-L * .62, 0), R(L * .42, 0)], dk(H(col), .4), max(.8, L * .05))
    for k in (-.15, .1):
        line(img, [R(L * k, 0), R(L * (k + .15), -L * .13)], dk(H(col), .3), max(.6, L * .03)); line(img, [R(L * k, 0), R(L * (k + .15), L * .13)], dk(H(col), .3), max(.6, L * .03))


def tanuki_face(img, cx, cy, r, fur='#8a6a48', mask='#2e2218', light='#d8c4a0', sleepy=False):
    """A round tanuki head: ears, pale muzzle, the dark 'bandit' eye patches (on its own layer, so the shading stays on the head)."""
    dst = img; img = Image.new('RGBA', dst.size, (0, 0, 0, 0))
    for sx in (-1, 1):
        ell(img, (cx + sx * r * .72 - r * .3, cy - r * 1.0, cx + sx * r * .72 + r * .3, cy - r * .42), dk(H(fur), .35))
    fill(img, fur, int(cx * 7 + cy), ell=(cx - r, cy - r * .9, cx + r, cy + r * .85), scale=2, contrast=.7)
    for sx in (-1, 1):
        fill(img, mask, int(cx + sx * 9), poly=[(cx + sx * r * .1, cy - r * .1), (cx + sx * r * .78, cy - r * .2), (cx + sx * r * .85, cy + r * .25), (cx + sx * r * .2, cy + r * .3)], scale=1, contrast=.5)
    ell(img, (cx - r * .42, cy + r * .05, cx + r * .42, cy + r * .72), light)
    ell(img, (cx - r * .14, cy + r * .12, cx + r * .14, cy + r * .3), '#1a120c')
    for sx in (-1, 1):
        ex = cx + sx * r * .42
        if sleepy: arc(img, (ex - r * .16, cy - r * .08, ex + r * .16, cy + r * .14), 20, 160, '#f0e0c0', max(.8, r * .07))
        else:
            ell(img, (ex - r * .13, cy - r * .1, ex + r * .13, cy + r * .14), '#1a0f08'); ell(img, (ex - r * .06, cy - r * .06, ex, cy), '#f0e6d0')
    volume(img, (cx - r, cy - r, cx + r, cy + r * .85), .5, .35); dst.alpha_composite(img)


# ───────────── the cart (yatai): 440×470, three frames ─────────────
SW, SH_ = 440, 470


def cart_back():
    img = I.canvas(SW, SH_)
    fill(img, '#1c140e', 1, rect=(52, 120, 388, 330), scale=6, stretch=(.3, 3), contrast=1.2)                 # back boards (dark)
    a = np.asarray(img, np.float32)                                                                            # warm light from the lanterns inside
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]; g = np.exp(-(((xx - px(220)) / px(170)) ** 2 + ((yy - px(200)) / px(110)) ** 2))
    a[..., 0] += 70 * g * (a[..., 3] > 0); a[..., 1] += 38 * g * (a[..., 3] > 0); a[..., 2] += 10 * g * (a[..., 3] > 0)
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')
    for y in (196, 262):                                                                                      # shelves with jars and boxes
        fill(img, '#4a3422', 2 + y, rect=(60, y, 380, y + 8), scale=3, stretch=(5, .3)); volume(img, (60, y, 380, y + 8), .4, .2)
    rnd = random.Random(4)
    x = 70
    while x < 360:
        w = rnd.uniform(18, 34); h = rnd.uniform(22, 44); c = rnd.choice(['#6a4a2a', '#3a4a5a', '#7a3a2a', '#c9a870', '#4a5a3a', '#2a2420'])
        y0 = 196 if x < 220 or rnd.random() < .5 else 262
        if rnd.random() < .5: fill(img, c, int(x), ell=(x, y0 - h, x + w, y0 + 2), scale=2, contrast=.6)
        else: fill(img, c, int(x), rect=(x, y0 - h * .8, x + w, y0), scale=2, contrast=.6)
        volume(img, (x, y0 - h, x + w, y0), .6, .35, spec=.15); x += w + rnd.uniform(6, 16)
    for x in (38, 386):                                                                                       # posts
        fill(img, '#3a2618', x, rect=(x, 84, x + 16, 440), scale=4, stretch=(.3, 3), contrast=1.2); volume(img, (x, 84, x + 16, 440), .5, .3)
    # roof: shingled, with a front beam
    fill(img, '#2a1e16', 3, poly=[(4, 100), (60, 34), (380, 34), (436, 100)], scale=4, stretch=(4, .5), contrast=1.2)
    d = ImageDraw.Draw(img)
    for k in range(6):
        y = 40 + k * 10.5; d.line([(px(60 - (y - 34) * .85), px(y)), (px(380 + (y - 34) * .85), px(y))], fill=(14, 9, 6, 200), width=px(1.6))
    for k in range(22):
        x = 26 + k * 18.5; d.line([(px(x), px(64 + (k % 2) * 6)), (px(x), px(98))], fill=(18, 12, 8, 120), width=px(1))
    volume(img, (4, 34, 436, 100), .5, .2)
    fill(img, '#4a3020', 5, rect=(0, 98, 440, 116), scale=4, stretch=(6, .3), contrast=1.2); volume(img, (0, 98, 440, 116), .4, .2)   # front beam
    line(img, [(0, 99), (440, 99)], '#8a6040', 1.2)
    return done(img)


def wheels(img):
    for cx in (66, 374):
        cy, r = 418, 46
        fill(img, '#3a2618', int(cx), ell=(cx - r, cy - r, cx + r, cy + r), scale=3, contrast=1.1)
        ell(img, (cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8), '#00000000')
        m = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(m).ellipse([px(cx - r + 8), px(cy - r + 8), px(cx + r - 8), px(cy + r - 8)], fill=(0, 0, 0, 255))
        a = np.asarray(img).copy(); mm = np.asarray(m)[..., 3] > 0; a[mm, 3] = 0; img.paste(Image.fromarray(a), (0, 0))
        for k in range(8):
            an = k * math.pi / 4; line(img, [(cx, cy), (cx + math.cos(an) * (r - 6), cy + math.sin(an) * (r - 6))], '#4a3020', 4)
        ell(img, (cx - 9, cy - 9, cx + 9, cy + 9), '#5a3a24'); ell(img, (cx - 3, cy - 3, cx + 3, cy + 3), '#1a100a')
        arc(img, (cx - r, cy - r, cx + r, cy + r), 200, 300, '#7a5a3a', 1.6)


def counter(img):
    floor_shadow(img, 220, 462, 210, 120)
    fill(img, '#4a3020', 6, rect=(30, 304, 410, 436), scale=5, stretch=(6, .35), contrast=1.25)          # box
    d = ImageDraw.Draw(img)
    for k in range(1, 5): d.line([(px(30), px(304 + k * 26.4)), (px(410), px(304 + k * 26.4))], fill=(20, 12, 8, 220), width=px(1.4))
    volume(img, (30, 304, 410, 436), .45, .25)
    fill(img, '#6a4a30', 7, poly=[(18, 292), (422, 292), (430, 306), (10, 306)], scale=4, stretch=(6, .3), contrast=1.2)   # counter top
    line(img, [(18, 292), (422, 292)], '#a07a52', 1.4)
    # leaf crest on the front: a white circle with the tanuki leaf
    ell(img, (184, 326, 256, 398), '#d8ccb0'); ell(img, (188, 330, 252, 394), '#2a1c14')
    leaf(img, 220, 362, 46, -.55, '#d8ccb0', 31)
    wheels(img)


def goods(img):
    """Little things on the counter top (y≈292)."""
    # stack of koban
    for k in range(4): ell(img, (54 + k * 2, 280 - k * 7, 92 + k * 2, 294 - k * 7), mixc(H('#e2b84a'), H('#8a6a20'), k % 2 * .3))
    ell(img, (58, 256, 98, 272), '#f0cc60'); leaf(img, 84, 258, 24, -.4, '#5a7a2a', 8)
    # gourd
    fill(img, '#c8a050', 9, ell=(112, 252, 140, 292), scale=2); fill(img, '#c8a050', 10, ell=(118, 232, 134, 256), scale=2)
    volume(img, (112, 232, 140, 292), .6, .35, spec=.25); line(img, [(116, 256), (136, 256)], '#b8322a', 2.6)
    # pumpkin lantern (lit)
    glowdot(img, 296, 270, 30, '#ffb050', 120)
    fill(img, '#4a5a2a', 11, ell=(272, 250, 322, 294), scale=2, contrast=.8); volume(img, (272, 250, 322, 294), .6, .3)
    for x in (286, 308): line(img, [(x, 252), (x - 2, 292)], '#2a3416', 1.2)
    poly(img, [(288, 264), (294, 270), (288, 274)], '#ffd070'); poly(img, [(306, 264), (300, 270), (306, 274)], '#ffd070'); poly(img, [(290, 282), (304, 282), (297, 288)], '#ffc060')
    line(img, [(297, 250), (299, 242)], '#3a2a14', 3)
    # a little ceramic tanuki
    fill(img, '#7a5636', 12, ell=(340, 252, 382, 294), scale=2); tanuki_face(img, 361, 246, 15)
    poly(img, [(342, 236), (361, 222), (380, 236)], '#c8a868')
    ell(img, (352, 266, 370, 288), '#d8c4a0')
    # fan standing in the middle-left
    fill(img, '#d8c8a0', 13, ell=(150, 226, 200, 276), scale=2, contrast=.5); line(img, [(175, 272), (175, 294)], '#6a4a2a', 3)
    ell(img, (162, 240, 186, 262), '#e8d080'); fill(img, '#5a4030', 14, ell=(170, 252, 184, 266), scale=1)


def lanterns(img, lit):
    for cx in (28, 412):
        cy = 150
        if lit: glowdot(img, cx, cy, 46, '#ff9a40', 110)
        line(img, [(cx, 112), (cx, 124)], '#120c09', 2)
        base = '#c8402a' if lit else '#5a3a30'
        fill(img, base, int(cx), ell=(cx - 20, 124, cx + 20, 178), scale=2, contrast=.9, dark=.4, light=.3 if lit else .1)
        a = np.asarray(img, np.float32)
        for k in range(1, 7): yk = px(124 + 54 * k / 7); a[yk - 1:yk + 1, px(cx - 20):px(cx + 20), :3] *= .6
        img.paste(Image.fromarray(a.astype(np.uint8), 'RGBA'), (0, 0))
        volume(img, (cx - 20, 124, cx + 20, 178), .4, .5)
        if lit: glowdot(img, cx - 3, 146, 12, '#ffe0a0', 120, True)
        text(img, '狸', cx, 152, 22, '#1a0806' if lit else '#2a1a14', SERIF)
        for y in (121, 176): ImageDraw.Draw(img).rectangle([px(cx - 13), px(y), px(cx + 13), px(y + 5)], fill=H('#140d09'))
        line(img, [(cx, 181), (cx, 196)], '#c83a2a' if lit else '#5a2a20', 2)


def noren(img):
    chars = 'たぬき屋'
    for k in range(4):
        x0 = 76 + k * 74; x1 = x0 + 68
        fill(img, '#22345a', 40 + k, poly=[(x0, 112), (x1, 112), (x1 + 1, 168), (x0 - 1, 166)], scale=3, stretch=(.5, 2), contrast=.8, dark=.35, light=.12)
        volume(img, (x0, 112, x1, 168), .3, .15)
        text(img, chars[k], (x0 + x1) / 2, 142, 34, '#e8e0cc', SANS)
    line(img, [(70, 113), (370, 113)], '#5a3a22', 3)


def front_open():
    img = I.canvas(SW, SH_); counter(img); goods(img); noren(img); lanterns(img, True); return done(img)


def front_closed():
    img = I.canvas(SW, SH_)
    # bamboo blind (sudare) lowered over the opening
    fill(img, '#8a7448', 50, rect=(54, 112, 386, 300), scale=3, stretch=(6, .3), contrast=.8, dark=.4, light=.15)
    d = ImageDraw.Draw(img)
    for k in range(48): y = 114 + k * 3.9; d.line([(px(54), px(y)), (px(386), px(y))], fill=(40, 30, 16, 120), width=px(.8))
    for x in (110, 220, 330): line(img, [(x, 112), (x, 300)], '#5a3a20', 1.6)
    volume(img, (54, 112, 386, 300), .3, .2)
    a = np.asarray(img, np.float32); a[..., :3] *= .62; img = Image.fromarray(a.astype(np.uint8), 'RGBA')     # unlit
    # rolled-up noren on the beam
    fill(img, '#22345a', 51, rect=(74, 104, 368, 122), scale=3, stretch=(6, .3)); volume(img, (74, 104, 368, 122), .5, .5)
    for x in (100, 220, 340): line(img, [(x, 102), (x, 124)], '#c8b88a', 2)
    counter(img)
    # the sign plank on two cords (the text is written by the game, in Russian)
    line(img, [(150, 112), (140, 190)], '#c8b88a', 1.6); line(img, [(290, 112), (300, 190)], '#c8b88a', 1.6)
    fill(img, '#a88458', 52, poly=[(112, 186), (328, 186), (332, 262), (108, 262)], scale=4, stretch=(5, .3), contrast=1.1)
    volume(img, (108, 186, 332, 262), .4, .25); line(img, [(112, 187), (328, 187)], '#d8b888', 1.2)
    leaf(img, 314, 200, 22, .5, '#4a6a2a', 53)
    lanterns(img, False)
    return done(img)


# ───────────── 12 things «Лавка тануки» ─────────────
def i_shigaraki():
    img = I.canvas(160, 210); floor_shadow(img, 80, 204, 62)
    fill(img, '#7a5636', 1, poly=[(52, 196), (34, 150), (40, 110), (80, 92), (120, 110), (126, 150), (108, 196)], scale=3)  # body
    fill(img, '#e0cca4', 2, ell=(48, 120, 112, 192), scale=2, contrast=.5); volume(img, (48, 120, 112, 192), .6, .35, spec=.35)   # big belly
    volume(img, (34, 92, 126, 198), .5, .3, spec=.2)
    for sx in (-1, 1): fill(img, '#5a3e26', 3 + sx, ell=(80 + sx * 26 - 16, 186, 80 + sx * 26 + 16, 204), scale=1)          # feet
    tanuki_face(img, 80, 76, 30, fur='#8a6640')
    fill(img, '#c8a868', 4, poly=[(36, 54), (80, 22), (124, 54), (80, 60)], scale=2, stretch=(2, .5)); volume(img, (36, 22, 124, 60), .5, .3)  # straw hat
    for k in range(5): line(img, [(80, 24), (40 + k * 20, 55)], '#8a7040', .8)
    # sake bottle in the right paw, ledger in the left
    fill(img, '#e8e0cc', 5, ell=(118, 128, 148, 176), scale=2); fill(img, '#e8e0cc', 6, rect=(128, 112, 138, 132), scale=1)
    volume(img, (118, 112, 148, 176), .6, .35, spec=.3); text(img, '酒', 133, 152, 16, '#2a1a10', SERIF)
    line(img, [(128, 120), (112, 132)], '#5a3e26', 6)
    fill(img, '#d8c8a0', 7, poly=[(14, 134), (40, 128), (44, 168), (18, 174)], scale=1); text(img, '通', 29, 151, 15, '#2a1a10', SERIF)
    line(img, [(40, 140), (52, 134)], '#5a3e26', 6)
    return done(img)


def i_bunbuku():
    img = I.canvas(200, 210); floor_shadow(img, 100, 204, 80)
    for x in (22, 178): fill(img, '#4a3020', x, rect=(x - 4, 92, x + 4, 202), scale=2)                                    # little rope stand
    line(img, [(18, 96), (182, 96)], '#c8b088', 2.2)
    # kettle body on the rope: iron chagama with a flange (hane) round its waist
    fill(img, '#2c2a28', 8, ell=(46, 92, 142, 172), scale=3, contrast=1.1, light=.3); volume(img, (46, 92, 142, 172), .7, .35, spec=.35)
    fill(img, '#3a3634', 19, poly=[(36, 130), (152, 130), (146, 140), (42, 140)], scale=2, stretch=(4, .4)); volume(img, (36, 130, 152, 140), .5, .3, spec=.2)
    fill(img, '#1e1c1a', 9, rect=(70, 86, 118, 98), scale=1); ell(img, (86, 76, 102, 90), '#3a3634')                    # lid
    arc(img, (58, 52, 130, 118), 200, 340, '#55504a', 4)                                                                  # handle
    fill(img, '#8a6a48', 10, poly=[(48, 122), (16, 104), (8, 120), (44, 140)], scale=1); volume(img, (8, 100, 50, 142), .5, .3)   # tail
    for k in range(3): line(img, [(20 + k * 9, 108 + k * 2), (18 + k * 9, 124 + k * 2)], '#3a2a1a', 2)
    tanuki_face(img, 150, 100, 26)                                                                                          # head out of the side
    for x in (80, 120): line(img, [(x, 166), (x - 4, 182)], '#6a4a2e', 6)                                                  # legs
    # a little open fan in its paw
    fill(img, '#d8b060', 11, poly=[(166, 74), (196, 52), (198, 82)], scale=1); line(img, [(160, 92), (168, 76)], '#6a4a2e', 4)
    for k in range(4): line(img, [(166, 74), (196 + k * .6, 54 + k * 9)], '#a07a30', .8)
    return done(img)


def i_kabocha():
    img = I.canvas(150, 140); floor_shadow(img, 75, 134, 60)
    glowdot(img, 75, 88, 50, '#ff9a40', 90)
    fill(img, '#3e5226', 12, ell=(14, 40, 136, 132), scale=2, contrast=.9, dark=.5, light=.25); volume(img, (14, 40, 136, 132), .6, .35, spec=.15)
    for x in (44, 75, 106): arc(img, (x - 34, 40, x + 34, 132), 250, 290, '#22301a', 1.6)
    for x in (30, 120): arc(img, (x - 20, 46, x + 20, 128), 90 if x < 75 else 270, 270 if x < 75 else 450, '#22301a', 1.4)
    # carved: leaf-window, two eyes and a grin
    poly(img, [(46, 70), (60, 78), (46, 86)], '#ffd070'); poly(img, [(104, 70), (90, 78), (104, 86)], '#ffd070')
    poly(img, [(50, 100), (62, 106), (75, 100), (88, 106), (100, 100), (92, 116), (58, 116)], '#ffb850')
    glowdot(img, 75, 96, 24, '#ffe0a0', 70, True)
    fill(img, '#4a3a1a', 13, poly=[(70, 44), (78, 44), (84, 24), (76, 22)], scale=1); leaf(img, 94, 28, 22, -.3, '#5a7a2a', 14)
    return done(img)


def i_happa():
    img = I.canvas(210, 150)
    line(img, [(6, 10), (60, 34), (105, 40), (150, 34), (204, 10)], '#c8b088', 1.8)
    for k, (x, y) in enumerate(((30, 24), (64, 35), (105, 41), (146, 35), (180, 24))):
        line(img, [(x, y), (x, y + 24)], '#b8322a', 1.4); ell(img, (x - 3, y + 20, x + 3, y + 26), '#c83a2a')
        leaf(img, x + 2, y + 62, 64, math.pi / 2 + (k - 2) * .12, ['#5a7a2a', '#6a8a32', '#4a6a24', '#7a8a30', '#5a7a2a'][k], 60 + k)
    return done(img)


def i_suzu():
    img = I.canvas(110, 210)
    line(img, [(55, 0), (55, 30)], '#120c09', 2.4)
    for x, y, r in ((40, 60, 20), (70, 58, 18), (55, 88, 24)):
        fill(img, '#d8a838', int(x + y), ell=(x - r, y - r, x + r, y + r), scale=2, contrast=.7, light=.35); volume(img, (x - r, y - r, x + r, y + r), .7, .4, spec=.45)
        line(img, [(x - r * .8, y), (x + r * .8, y)], '#7a5a10', 1.2); ell(img, (x - r * .3, y + r * .3, x + r * .3, y + r * .62), '#2a1a08')
    for k, c in enumerate(['#b8322a', '#efe6d4', '#b8322a']):
        line(img, [(48 + k * 7, 110), (44 + k * 9, 200)], c, 4)
    for y in (122, 150, 178): line(img, [(44, y), (68, y + 4)], '#7a1a14', 1)
    return done(img)


def i_tsuki():
    img = I.canvas(180, 230)
    line(img, [(90, 0), (90, 24)], '#120c09', 2.4); ImageDraw.Draw(img).rectangle([px(68), px(24), px(112), px(32)], fill=H('#140d09'))
    glowdot(img, 90, 124, 82, '#ffd890', 90)
    fill(img, '#f0dca0', 15, ell=(10, 34, 170, 214), scale=4, contrast=.5, dark=.25, light=.2)
    a = np.asarray(img, np.float32)
    for k in range(1, 10): yk = px(34 + 180 * k / 10); a[yk - 1:yk + 1, :, :3] *= .8
    img = Image.fromarray(a.astype(np.uint8), 'RGBA')
    # silhouettes: two tanuki drumming on their bellies under pine twigs
    for cx, flip in ((62, 1), (118, -1)):
        ell(img, (cx - 22, 120, cx + 22, 182), '#3a2a1c'); ell(img, (cx - 15, 96, cx + 15, 124), '#3a2a1c')
        poly(img, [(cx - 13, 100), (cx - 9, 88), (cx - 4, 98)], '#3a2a1c'); poly(img, [(cx + 13, 100), (cx + 9, 88), (cx + 4, 98)], '#3a2a1c')
        line(img, [(cx + flip * 18, 130), (cx + flip * 4, 146)], '#3a2a1c', 7); line(img, [(cx - flip * 18, 130), (cx - flip * 26, 112)], '#3a2a1c', 7)
        ell(img, (cx - 12, 136, cx + 12, 162), '#5a4632')
    for k in range(5): line(img, [(30 + k * 8, 60 + k * 2), (50 + k * 8, 50)], '#4a5a3a', 2)
    text(img, '♪', 90, 92, 22, '#3a2a1c', SANS)
    volume(img, (10, 34, 170, 214), .4, .45)
    ImageDraw.Draw(img).rectangle([px(68), px(210), px(112), px(218)], fill=H('#140d09')); line(img, [(90, 218), (90, 230)], '#c83a2a', 2.4)
    return done(img)


def i_koban():
    img = I.canvas(180, 140); floor_shadow(img, 90, 134, 76)
    fill(img, '#2a1410', 16, poly=[(20, 96), (160, 96), (150, 130), (30, 130)], scale=2); volume(img, (20, 96, 160, 130), .4, .3)   # lacquer stand
    fill(img, '#7a1e16', 17, poly=[(10, 86), (170, 86), (162, 100), (18, 100)], scale=2, light=.3); volume(img, (10, 86, 170, 100), .5, .3, spec=.3)
    ell(img, (76, 106, 104, 126), '#120808')
    for k in range(6):
        x, y = 40 + (k % 3) * 34, 74 - (k // 3) * 16
        fill(img, '#e2b84a', 18 + k, ell=(x - 22, y - 12, x + 22, y + 12), scale=1, contrast=.6, light=.35); volume(img, (x - 22, y - 12, x + 22, y + 12), .6, .3, spec=.5)
        ell(img, (x - 15, y - 7, x + 15, y + 7), '#c89a34'); line(img, [(x - 10, y), (x + 10, y)], '#9a7420', 1)
    leaf(img, 126, 46, 46, -.6, '#5a7a2a', 24)
    for x, y in ((40, 34), (150, 70)): text(img, '✦', x, y, 14, '#ffe8a0', SANS)
    return done(img)


def i_hyotan():
    img = I.canvas(110, 200); floor_shadow(img, 55, 194, 40)
    fill(img, '#c89a48', 25, ell=(16, 92, 94, 192), scale=2, contrast=.7, light=.3); fill(img, '#c89a48', 26, ell=(30, 38, 80, 98), scale=2, contrast=.7, light=.3)
    volume(img, (16, 38, 94, 192), .7, .35, spec=.35)
    fill(img, '#5a3a1a', 27, rect=(48, 22, 62, 40), scale=1)
    line(img, [(32, 96), (78, 96)], '#b8322a', 4); line(img, [(56, 98), (70, 130), (64, 150)], '#b8322a', 2.4)
    for k in range(5): line(img, [(64, 150), (58 + k * 3, 172)], '#c83a2a', 1.2)
    return done(img)


def i_uchiwa():
    img = I.canvas(140, 200); floor_shadow(img, 70, 194, 44)
    fill(img, '#4a3020', 28, poly=[(40, 194), (100, 194), (90, 180), (50, 180)], scale=1)                                   # stand
    line(img, [(70, 186), (70, 132)], '#8a6a3a', 6)
    fill(img, '#1e2a44', 29, ell=(8, 8, 132, 138), scale=3, contrast=.7)                                                    # night paper
    for k in range(12): an = math.pi + k * math.pi / 11; line(img, [(70, 132), (70 + 60 * math.cos(an) * .98, 73 + 62 * math.sin(an) * -1)], (60, 70, 100, 90), .8)
    glowdot(img, 96, 40, 22, '#ffe8b0', 120, True); ell(img, (84, 28, 108, 52), '#f4e4b0')                                       # moon
    ell(img, (42, 76, 88, 124), '#6a4e34'); tanuki_face(img, 65, 66, 15, fur='#7a5a3a')                                    # drumming tanuki
    ell(img, (52, 90, 78, 118), '#d8c4a0'); line(img, [(44, 92), (54, 102)], '#6a4e34', 5); line(img, [(86, 92), (76, 102)], '#6a4e34', 5)
    for x, y in ((28, 70), (106, 92)): text(img, '♪', x, y, 16, '#e8d8a8', SANS)
    arc(img, (8, 8, 132, 138), 0, 360, '#8a6a3a', 2.4); volume(img, (8, 8, 132, 138), .4, .3)
    return done(img)


def i_kaki():
    img = I.canvas(120, 230)
    line(img, [(60, 0), (60, 222)], '#c8b088', 1.6)
    for k in range(6):
        y = 22 + k * 34; x = 60 + (k % 2 * 2 - 1) * 4
        fill(img, '#b8602a', 30 + k, ell=(x - 18, y, x + 18, y + 32), scale=1, contrast=.8, dark=.5); volume(img, (x - 18, y, x + 18, y + 32), .6, .35, spec=.2)
        a = np.asarray(img, np.float32); rng = np.random.default_rng(k)
        img = Image.fromarray(a.astype(np.uint8), 'RGBA')
        for j in range(3): arc(img, (x - 14 + j * 4, y + 4, x + 6 + j * 4, y + 28), 250, 300, '#6a2a10', .8)
        poly(img, [(x - 8, y + 2), (x, y - 4), (x + 8, y + 2), (x, y + 5)], '#3a3a1a')
    return done(img)


def i_netsuke():
    img = I.canvas(130, 110); floor_shadow(img, 64, 104, 50)
    line(img, [(100, 52), (118, 20), (122, 4)], '#7a1a14', 1.8); fill(img, '#4a2a1a', 34, ell=(110, 8, 126, 24), scale=1); volume(img, (110, 8, 126, 24), .6, .3, spec=.4)
    fill(img, '#e0d0b0', 35, ell=(14, 40, 112, 102), scale=2, contrast=.5, dark=.3, light=.2)                               # curled body
    fill(img, '#d0bc98', 36, poly=[(20, 86), (8, 62), (30, 52), (48, 90)], scale=1)                                        # tail around
    for k in range(3): line(img, [(14 + k * 8, 66 + k * 6), (26 + k * 8, 60 + k * 6)], '#8a7050', 1.4)
    tanuki_face(img, 82, 70, 22, fur='#d8c6a2', mask='#9a8060', light='#efe4cc', sleepy=True)
    for k in range(5): arc(img, (24 + k * 12, 50, 50 + k * 12, 100), 200, 250, '#a89070', .8)
    volume(img, (8, 40, 112, 102), .6, .3, spec=.3)
    return done(img)


def i_chou():
    img = I.canvas(160, 160); floor_shadow(img, 80, 154, 66)
    fill(img, '#d8c8a0', 37, poly=[(26, 30), (120, 22), (130, 148), (34, 150)], scale=2, contrast=.6)
    for k in range(6): line(img, [(30 + k * 1.2, 40 + k * 20), (36 + k * 1.2, 46 + k * 20)], '#3a2a1a', 2)                # stitched spine
    fill(img, '#efe4c8', 38, poly=[(48, 34), (82, 32), (86, 70), (52, 72)], scale=1)
    text(img, '通', 66, 52, 26, '#1a1008', SERIF); text(img, '狸', 92, 112, 34, '#3a2a1a', SERIF)
    volume(img, (26, 22, 130, 150), .4, .25)
    line(img, [(116, 140), (152, 60)], '#6a4a2e', 4); poly(img, [(150, 56), (158, 50), (156, 62)], '#1a1008')                 # brush
    return done(img)


THINGS = [('tn_shigaraki', i_shigaraki, 'b'), ('tn_bunbuku', i_bunbuku, 'b'), ('tn_kabocha', i_kabocha, 'b'), ('tn_happa', i_happa, 't'),
          ('tn_suzu', i_suzu, 't'), ('tn_tsuki', i_tsuki, 't'), ('tn_koban', i_koban, 'b'), ('tn_hyotan', i_hyotan, 'b'),
          ('tn_uchiwa', i_uchiwa, 'b'), ('tn_kaki', i_kaki, 't'), ('tn_netsuke', i_netsuke, 'b'), ('tn_chou', i_chou, 'b')]


def pack(ims, W, name):
    x = y = rowh = 0; pos = {}
    for iid, im, _ in sorted(ims, key=lambda t: -t[1].height):
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[iid] = (x, y, im.width, im.height); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for iid, im, _ in ims: at.paste(im, pos[iid][:2])
    at.save(os.path.join(ASSETS, 'items', name + '.webp'), 'WEBP', quality=88, alpha_quality=92, method=6)
    pv = Image.new('RGBA', at.size, (34, 30, 28, 255)); pv.alpha_composite(at); pv.convert('RGB').save(os.path.join(OUTD, name + '.png'))
    return {'size': [W, y + rowh], 'at': {iid: list(pos[iid]) + [a] for iid, _, a in ims}}


if __name__ == '__main__':
    st = [('back', cart_back(), ''), ('open', front_open(), ''), ('closed', front_closed(), '')]
    print('stall', json.dumps(pack(st, 3 * SW + 8, 'tn_stall'), separators=(',', ':')))
    print('items', json.dumps(pack([(iid, f(), a) for iid, f, a in THINGS], 1220, 'atlas_tn'), separators=(',', ':')))
