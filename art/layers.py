#!/usr/bin/env python3
"""2.5D dioramas: every room is painted as depth layers for parallax.
Output: <out>/<room>_<layer>.webp (RGBA) and layers.json {room: [[layer, depth], ...]} (back to front)."""
import json, math, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import *

OUT = sys.argv[1]
MANIFEST = {}


def grade_rgba(img, lift=(12, 16, 14), gamma=1.0, sat=0.85):
    a = np.asarray(img, np.float32); rgb = a[..., :3] / 255
    lum = (rgb * [0.3, 0.59, 0.11]).sum(-1, keepdims=True)
    rgb = lum + (rgb - lum) * sat
    rgb = np.clip(rgb, 0, 1) ** gamma
    rgb = rgb * (1 - np.array(lift) / 255) + np.array(lift) / 255
    a[..., :3] = np.clip(rgb, 0, 1) * 255
    return Image.fromarray(a.astype(np.uint8), 'RGBA')


def darken_rgba(img, amount, tint):
    a = np.asarray(img, np.float32); a[..., :3] = a[..., :3] * (1 - amount) + np.array(tint, np.float32) * amount
    return Image.fromarray(a.astype(np.uint8), 'RGBA')


class Stack:
    def __init__(self, name): self.name = name; self.items = []
    def cut(self, img, lname, depth, blur=0):
        self.items.append((lname, depth, img, blur)); return layer()
    def finish(self, img, lname, depth, blur=0, darken=None, extra_glow=None, **kw):
        self.items.append((lname, depth, img, blur))
        comp = None; MANIFEST[self.name] = []
        for i, (ln, dp, im, bl) in enumerate(self.items):
            out = im.resize((W, H), Image.LANCZOS)
            if bl: out = out.filter(ImageFilter.GaussianBlur(bl))
            if darken: out = darken_rgba(out, *darken)
            out = grade_rgba(out, **kw)
            if i == 0: out = Image.alpha_composite(Image.new('RGBA', out.size, (13, 18, 16, 255)), out)
            out.save(f'{OUT}/{self.name}_{ln}.webp', 'WEBP', quality=84, alpha_quality=90, method=6)
            MANIFEST[self.name].append([ln, dp])
            comp = out if comp is None else Image.alpha_composite(comp, out)
        comp.convert('RGB').resize((W // 3, H // 3)).save(f'{OUT}/preview-{self.name}.jpg', quality=85)
        print('layers', self.name, [x[0] for x in self.items])


# ───────────── near-camera, out-of-focus foreground ─────────────
PAL_NEAR = [hexc('#070a08'), hexc('#0c120d'), hexc('#121a13'), hexc('#19241a'), hexc('#223022')]


def near_fern(img, x, base, h, seed, lean=0, pal=PAL_NEAR):
    """Fern / grass clump rising from the bottom edge, close to the lens."""
    rnd = random.Random(seed); d = ImageDraw.Draw(img)
    for i in range(26):
        a = lean + rnd.uniform(-1.1, 1.1); L = h * rnd.uniform(.55, 1)
        x0, y0 = x * SS + rnd.uniform(-30, 30) * SS, base * SS
        pts = []
        for k in range(14):
            u = k / 13; bend = a * u * u
            pts.append((x0 + math.sin(bend) * L * u * SS, y0 - math.cos(bend) * L * u * SS))
        col = pal[rnd.randint(1, len(pal) - 1)]
        d.line(pts, fill=col, width=int(rnd.uniform(5, 9) * SS))
        for k in range(2, 13, 1):   # fronds
            px_, py_ = pts[k]; s = (1 - k / 14) * 60 * SS
            for sd in (-1, 1):
                d.line([(px_, py_), (px_ + sd * s * math.cos(a + .6), py_ + s * .3)], fill=col, width=int(5 * SS))


def near_foliage(img, spots, seed, pal=PAL_NEAR, size=(12, 24)):
    rnd = random.Random(seed); d = ImageDraw.Draw(img)
    blobs = ragged([(x * SS, y * SS, rx * SS, ry * SS) for x, y, rx, ry in spots], rnd, 8, .6)
    shadow_blobs(img, blobs, pal[0]); dab_mass(d, blobs, len(blobs) * 140, 'leaf', pal, rnd, size=size)


def near_branch(img, x0, y0, x1, y1, seed, pal=PAL_NEAR):
    rnd = random.Random(seed)
    pts = wobble((x0 * SS, y0 * SS), (x1 * SS, y1 * SS), 8, 30 * SS, rnd)
    trunk(img, pts, [26 * SS * (1 - i / 10) + 5 * SS for i in range(len(pts))], (hexc('#050505'), hexc('#0d0b0a'), hexc('#1a1612')), seed)
    spots = [(p[0] / SS + rnd.uniform(-40, 40), p[1] / SS + rnd.uniform(20, 70), rnd.uniform(120, 190), rnd.uniform(55, 90)) for p in pts[2::2]]
    near_foliage(img, spots, seed + 1, pal)


# ───────────── scenes ─────────────
def engawa():
    st = Stack('engawa'); fog = hexc('#8c958f')
    img = gradient(hexc('#838c86'), hexc('#454e48'))
    forest_layers(img, 640, fog, [101, 102], [11, 8], [(420, 560), (520, 660)], [0.78, 0.6], [3, 1.8])
    img = st.cut(img, 'sky', .06)
    m = Image.new('L', (SW, 240 * SS), 255)
    img.alpha_composite(atmos(textured_fill(m, hexc('#5f655e'), hexc('#3e443d'), hexc('#798078'), 30 * SS, 3, contrast=1.4), fog, .4, .8), (0, 540 * SS))
    d = ImageDraw.Draw(img); d.rectangle([0, 520 * SS, SW, 548 * SS], fill=mixc(hexc('#232723'), fog, .4))
    back = layer()
    pine(back, 1250 * SS, 1060 * SS, 920 * SS, 33, PAL_PINE, BARK, lean=-0.3, pads=8, spread=1.25)
    maple(back, 260 * SS, 1060 * SS, 820 * SS, 44, PAL_MAPLE, BARK, lean=0.25)
    img.alpha_composite(atmos(back, fog, 0.32, blur=0.6))
    img = st.cut(img, 'far', .2)
    mid = layer()
    maple(mid, 640 * SS, 1080 * SS, 860 * SS, 21, PAL_MAPLE, BARK, lean=0.1)
    maple(mid, 960 * SS, 1080 * SS, 700 * SS, 27, PAL_MAPLE, BARK, lean=-0.2)
    img.alpha_composite(atmos(mid, fog, 0.12, blur=0.2))
    ground(img, 960, 1190, 71, pebbles=900)
    toro(img, 1180, 1085, 200, 5)
    bushes(img, 1100, -40, 1840, 7, PAL_BUSH, count=20, rmin=70, rmax=160)
    for i, (sx, sy) in enumerate([(520, 1098), (760, 1104), (1000, 1098)]):
        stone(img, sx, sy, 58, 14, 40 + i, hexc('#454a44'))
    img = st.cut(img, 'mid', .42)
    wood_planks(img, 1116, 1400, 61, hexc('#3f332a'), hexc('#17120e'), hexc('#5d4d3e'), plank_h=40)
    d = ImageDraw.Draw(img); d.rectangle([0, 1116 * SS, SW, 1124 * SS], fill=hexc('#0e0a08'))
    img = st.cut(img, 'floor', .8)
    wood_block(img, (0, 0, 1800, 92), 51, hexc('#1f1712'), hexc('#0b0806'), hexc('#34281f'))
    wood_block(img, (0, 92, 1800, 112), 52, hexc('#17110d'), hexc('#080605'), hexc('#281e17'))
    wood_block(img, (0, 0, 64, 1124), 53, hexc('#18120e'), hexc('#080605'), hexc('#2a2019'), True)
    paper(img, (1400, 124, 1792, 1100), 54, hexc('#a8a292'), lit=0.62, grid=(3, 6))
    wood_block(img, (1380, 112, 1400, 1124), 55, hexc('#18120e'), hexc('#080605'), hexc('#2a2019'), True)
    img = st.cut(img, 'frame', .92)
    near_fern(img, 430, 1440, 480, 1, lean=.35); near_fern(img, 1410, 1440, 440, 2, lean=-.4)
    near_branch(img, 1500, -40, 1180, 120, 3)
    st.finish(img, 'near', 1.5, blur=5, lift=(8, 11, 10), sat=0.72, gamma=1.08)


def kitchen():
    st = Stack('kitchen')
    win = gradient(hexc('#7d8781'), hexc('#46504a'))
    g = layer(); maple(g, 520 * SS, 700 * SS, 700 * SS, 5, PAL_MAPLE, BARK, 0.2); bushes(g, 720, 200, 900, 9, PAL_BUSH, 8, 60, 120)
    win.alpha_composite(atmos(g, hexc('#8a938d'), .3, .4)); win.alpha_composite(fog_layer(hexc('#8a938d'), 300, 700, .6, 4))
    img = st.cut(win, 'garden', .15)
    vertical_boards(img, (0, 0, 1800, 1200), 11, hexc('#3a2c22'), hexc('#1a130e'), hexc('#54412f'))
    cut = Image.new('L', (SW, SH), 255); ImageDraw.Draw(cut).rectangle([240 * SS, 180 * SS, 820 * SS, 640 * SS], fill=0)
    a = np.asarray(img, np.float32); a[..., 3] *= np.asarray(cut, np.float32) / 255; img = Image.fromarray(a.astype(np.uint8), 'RGBA')
    d = ImageDraw.Draw(img)
    for x in range(240, 821, 36): d.rectangle([x * SS, 180 * SS, (x + 7) * SS, 640 * SS], fill=hexc('#1b130e'))
    for y in (180, 400, 640): d.rectangle([232 * SS, (y - 6) * SS, 828 * SS, (y + 8) * SS], fill=hexc('#1b130e'))
    wood_block(img, (960, 470, 1660, 492), 12, hexc('#3f3023'), hexc('#1a130e'), hexc('#5a4633'))
    wood_block(img, (960, 700, 1660, 722), 13, hexc('#3f3023'), hexc('#1a130e'), hexc('#5a4633'))
    for i, (cx, w, h, c) in enumerate([(1010, 70, 34, '#5b3a2a'), (1100, 90, 40, '#3c4a52'), (1200, 60, 50, '#8b7c62'), (1300, 96, 36, '#2e2a26'), (1420, 70, 60, '#6c5a3e'), (1530, 88, 42, '#44564f')]):
        ceramic(img, cx, 470, w, h, 20 + i, hexc(c))
    for i, (cx, w, h, c) in enumerate([(1030, 110, 60, '#2a2522'), (1180, 80, 44, '#7a6a52'), (1330, 120, 54, '#3b4a45'), (1500, 90, 70, '#5a3a2a')]):
        ceramic(img, cx, 700, w, h, 40 + i, hexc(c))
    for i in range(3):
        x0 = 30 + i * 62; m = Image.new('L', (int(58 * SS), int(420 * SS)), 255)
        img.alpha_composite(textured_fill(m, hexc('#1e2a3b'), hexc('#0f1520'), hexc('#2c3b52'), 16 * SS, 60 + i, (1, 4)), (int(x0 * SS), 0))
    d.ellipse([70 * SS, 250 * SS, 150 * SS, 330 * SS], fill=hexc('#c9c1ae')); d.ellipse([88 * SS, 262 * SS, 150 * SS, 320 * SS], fill=hexc('#1e2a3b'))
    chochin(img, 1560, 300, 62, True); glow(img, 1560, 300, 520, hexc('#e39a55'), .38)
    img = st.cut(img, 'wall', .5)
    m = Image.new('L', (int(460 * SS), int(300 * SS)), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, m.width - 1, m.height - 1], 30 * SS, fill=255)
    img.alpha_composite(textured_fill(m, hexc('#5e4f3e'), hexc('#3a2e22'), hexc('#76664f'), 34 * SS, 50, contrast=0.9), (int(1240 * SS), int(850 * SS)))
    d = ImageDraw.Draw(img); d.ellipse([1330 * SS, 960 * SS, 1440 * SS, 1060 * SS], fill=hexc('#120c08'))
    glow(img, 1385, 1030, 120, hexc('#e0702a'), .45)
    d.ellipse([1300 * SS, 800 * SS, 1600 * SS, 880 * SS], fill=hexc('#171513')); d.rectangle([1320 * SS, 760 * SS, 1580 * SS, 840 * SS], fill=hexc('#1f1c19'))
    ground(img, 1150, 1400, 70, hexc('#3b342c'), hexc('#1a1612'), hexc('#51483c'), pebbles=300)
    wood_block(img, (0, 1128, 1800, 1156), 71, hexc('#3a2c21'), hexc('#150f0b'), hexc('#57432f'))
    img = st.cut(img, 'floor', .8)
    near_foliage(img, [(470, 40, 90, 70), (520, 150, 70, 60)], 9, [hexc('#15100b'), hexc('#241a10'), hexc('#3a2a16'), hexc('#5a3c1c')], (10, 20))
    d = ImageDraw.Draw(img); d.line([(460 * SS, 0), (480 * SS, 200 * SS)], fill=hexc('#0e0a07'), width=6 * SS)
    st.finish(img, 'near', 1.5, blur=6, lift=(10, 8, 6), sat=0.8, gamma=1.05)


def onsen():
    st = Stack('onsen'); fog = hexc('#8f9892')
    img = gradient(hexc('#8c948f'), hexc('#48514b'))
    forest_layers(img, 720, fog, [201, 202], [10, 8], [(480, 620), (620, 760)], [0.75, 0.52], [3, 1.6])
    img = st.cut(img, 'sky', .06)
    forest_layers(img, 720, fog, [203], [6], [(760, 920)], [0.3], [.7])
    f = layer(); d = ImageDraw.Draw(f); rnd = random.Random(3)
    for x in range(0, W, 26):
        c = mixc(hexc('#4a4a33'), hexc('#26261a'), rnd.random())
        d.rectangle([x * SS, 760 * SS, (x + 22) * SS, 980 * SS], fill=c)
        for y in (800, 880, 950): d.line([(x * SS, y * SS), ((x + 22) * SS, y * SS)], fill=mixc(c, (0, 0, 0, 255), .5), width=2 * SS)
    d.rectangle([0, 840 * SS, SW, 852 * SS], fill=hexc('#2a2418'))
    img.alpha_composite(atmos(f, fog, .18, .3)); img.alpha_composite(fog_layer(fog, 700, 1000, .5, 7))
    img = st.cut(img, 'fence', .28)
    ground(img, 960, 1400, 81, hexc('#30352e'), hexc('#161a15'), hexc('#4a5046'), pebbles=1400)
    pool(img, 900, 1080, 620, 110, 90)
    bushes(img, 1000, -60, 260, 8, PAL_BUSH, 5, 70, 130); bushes(img, 1000, 1560, 1860, 9, PAL_BUSH, 5, 70, 130)
    img = st.cut(img, 'pool', .55)
    for i, (x, y, rx, ry) in enumerate([(900, 1330, 190, 46), (520, 1300, 130, 40), (1300, 1310, 150, 44), (160, 1250, 110, 50), (1660, 1260, 120, 54)]):
        stone(img, x, y, rx, ry, 300 + i, hexc('#4b4f49'))
    img = st.cut(img, 'floor', .82)
    near_fern(img, 420, 1440, 480, 4, lean=.4); near_fern(img, 1400, 1440, 460, 5, lean=-.35)
    near_branch(img, 300, -60, 900, 60, 6)
    st.finish(img, 'near', 1.5, blur=5, lift=(9, 12, 11), sat=0.72, gamma=1.08)


def bedroom(lit):
    name = 'bedroom_on' if lit else 'bedroom_off'; st = Stack(name)
    img = gradient(hexc('#3a352c'), hexc('#26221c'))
    plaster(img, (0, 0, 1800, 1190), 21, hexc('#4b4436'), hexc('#2d281f'), hexc('#5e5646'))
    wood_block(img, (0, 0, 1800, 70), 22, hexc('#241a14'), hexc('#0e0a08'), hexc('#3a2c22'))
    moon = hexc('#9fa3a6') if not lit else hexc('#b3ab97')
    paper(img, (640, 150, 1560, 1000), 25, moon, lit=0.85 if not lit else 0.7, grid=(4, 5))
    sh = layer(); pine(sh, 1400 * SS, 1100 * SS, 900 * SS, 13, [hexc('#000000')] * 5, (hexc('#000000'), hexc('#000000'), hexc('#000000')), lean=-.4, pads=6)
    sh = sh.filter(ImageFilter.GaussianBlur(4 * SS)); a = np.asarray(sh, np.float32); a[..., 3] *= 0.55
    mk = Image.new('L', (SW, SH), 0); ImageDraw.Draw(mk).rectangle([640 * SS, 150 * SS, 1560 * SS, 1000 * SS], fill=255)
    img.paste(Image.fromarray(a.astype(np.uint8), 'RGBA'), (0, 0), ImageChops_min(mk, Image.fromarray(a[..., 3].astype(np.uint8))))
    img = st.cut(img, 'wall', .4)
    # tokonoma is a recess: its own layer just in front of the wall
    wood_block(img, (70, 150, 470, 1080), 23, hexc('#2b241c'), hexc('#15110c'), hexc('#3b3226'), True)
    plaster(img, (90, 170, 450, 1060), 24, hexc('#3d372c'), hexc('#241f18'), hexc('#4d4638'))
    scroll = gradient(hexc('#cfc6b0'), hexc('#b8ae96'), h=int(560 * SS), w=int(160 * SS))
    sc = layer(); sc.alpha_composite(scroll, (int(190 * SS), int(220 * SS)))
    m = layer(); pine(m, 270 * SS, 740 * SS, 420 * SS, 7, [hexc('#1a1a18'), hexc('#2a2a26'), hexc('#3a3934'), hexc('#4d4b45')], (hexc('#111111'), hexc('#222222'), hexc('#333333')), lean=.2, pads=4, spread=.5)
    sc.alpha_composite(atmos(m, hexc('#bdb39b'), .35))
    mm = Image.new('L', (SW, SH), 0); ImageDraw.Draw(mm).rectangle([190 * SS, 220 * SS, 350 * SS, 780 * SS], fill=255); img.paste(sc, (0, 0), mm)
    d = ImageDraw.Draw(img); d.rectangle([180 * SS, 205 * SS, 360 * SS, 222 * SS], fill=hexc('#2a1d14')); d.rectangle([180 * SS, 778 * SS, 360 * SS, 796 * SS], fill=hexc('#2a1d14'))
    ceramic(img, 270, 1060, 90, 70, 5, hexc('#2b3a3a'))
    ik = layer(); maple(ik, 270 * SS, 995 * SS, 330 * SS, 12, PAL_SAKURA, BARK, -.2); img.alpha_composite(atmos(ik, hexc('#3a352c'), .25))
    img = st.cut(img, 'alcove', .5)
    tatami(img, 1140, 1400, 26, lit=1.0 if lit else 0.8)
    m = Image.new('L', (int(900 * SS), int(150 * SS)), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, m.width - 1, m.height - 1], 40 * SS, fill=255)
    img.alpha_composite(textured_fill(m, hexc('#2e3446'), hexc('#1a1f2c'), hexc('#3e4660'), 40 * SS, 27, (3, 1), 0.8), (int(450 * SS), int(1230 * SS)))
    d = ImageDraw.Draw(img)
    for x in range(520, 1330, 90): d.line([(x * SS, 1240 * SS), (x * SS, 1370 * SS)], fill=hexc('#20263a'), width=2 * SS)
    ax, ab = 330, 1300
    wood_block(img, (ax - 70, ab - 20, ax + 70, ab), 28, hexc('#241a13'), hexc('#0e0a07'), hexc('#3a2b1f'))
    pap = hexc('#f0d59a') if lit else hexc('#5f584a')
    m = Image.new('L', (int(110 * SS), int(200 * SS)), 255)
    img.alpha_composite(textured_fill(m, pap, mixc(pap, (0, 0, 0, 255), .25), mixc(pap, (255, 255, 255, 255), .2), 5 * SS, 29), (int((ax - 55) * SS), int((ab - 240) * SS)))
    for xx in (ax - 58, ax + 52): d.rectangle([xx * SS, (ab - 250) * SS, (xx + 6) * SS, ab * SS], fill=hexc('#160f0a'))
    d.rectangle([(ax - 58) * SS, (ab - 144) * SS, (ax + 58) * SS, (ab - 138) * SS], fill=hexc('#160f0a'))
    d.rectangle([(ax - 58) * SS, (ab - 250) * SS, (ax + 58) * SS, (ab - 242) * SS], fill=hexc('#160f0a'))
    if lit: glow(img, ax, ab - 150, 900, hexc('#e6b46a'), .42); glow(img, ax, ab - 150, 260, hexc('#ffd999'), .35)
    else: glow(img, 1100, 560, 700, hexc('#8fa0b8'), .22)
    img = st.cut(img, 'floor', .8)
    # a sliding fusuma edge right next to the lens
    wood_block(img, (1700, 0, 1760, 1400), 91, hexc('#120d0a'), hexc('#060404'), hexc('#1f1712'), True)
    m = Image.new('L', (int(40 * SS), int(1400 * SS)), 255)
    img.alpha_composite(textured_fill(m, hexc('#3a352c'), hexc('#1f1b16'), hexc('#4a4438'), 20 * SS, 92), (int(1760 * SS), 0))
    if lit: st.finish(img, 'near', 1.4, blur=6, lift=(10, 8, 6), sat=0.8, gamma=1.02)
    else: st.finish(img, 'near', 1.4, blur=6, darken=(.55, (8, 12, 26)), lift=(6, 8, 12), sat=0.7, gamma=1.1)


def wardrobe():
    st = Stack('wardrobe')
    img = gradient(hexc('#211a14'), hexc('#140f0c'))
    plaster(img, (0, 0, 1800, 1190), 31, hexc('#2e2720'), hexc('#1a1511'), hexc('#3b3229'))
    img = st.cut(img, 'wall', .3)
    x0, y0, x1, y1 = 120, 150, 1680, 1060
    gold = Image.new('RGBA', (int((x1 - x0) * SS), int((y1 - y0) * SS)))
    gw, gh = gold.size; n = fbm(gw, gh, 40 * SS, 4, 32)
    sq = 70 * SS; rng = np.random.default_rng(3)
    tiles = rng.uniform(.82, 1.08, (gh // sq + 1, gw // sq + 1)); tv = np.kron(tiles, np.ones((sq, sq)))[:gh, :gw]
    rgb = np.array([150, 118, 62], np.float32) * (0.6 + 0.5 * n[..., None]) * tv[..., None]
    gold = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), np.full((gh, gw), 255)]).astype(np.uint8), 'RGBA')
    art = layer(); maple(art, 1180 * SS, 1060 * SS, 1100 * SS, 77, PAL_SAKURA, (hexc('#1a120e'), hexc('#2c201a'), hexc('#46372c')), -.35)
    maple(art, 420 * SS, 1060 * SS, 700 * SS, 78, PAL_SAKURA, (hexc('#1a120e'), hexc('#2c201a'), hexc('#46372c')), .3)
    screen = layer(); screen.alpha_composite(gold, (int(x0 * SS), int(y0 * SS)))
    screen.alpha_composite(fog_layer(hexc('#e2c98e'), 820, 980, .7, 33, 200)); screen.alpha_composite(art)
    screen.alpha_composite(fog_layer(hexc('#e8d19a'), 300, 420, .55, 34, 220))
    mk = Image.new('L', (SW, SH), 0); ImageDraw.Draw(mk).rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], fill=255)
    screen = darken(screen, .35, (20, 12, 6)); img.paste(screen, (0, 0), mk)
    d = ImageDraw.Draw(img)
    for i in range(7):
        x = x0 + (x1 - x0) * i / 6
        d.rectangle([(x - 7) * SS, y0 * SS, (x + 7) * SS, y1 * SS], fill=hexc('#1a0f0a'))
        if i < 6:
            shade = np.zeros((int((y1 - y0) * SS), int((x1 - x0) / 6 * SS), 4), np.float32); ramp = np.linspace(0, 1, shade.shape[1])
            shade[..., 3] = (ramp if i % 2 else 1 - ramp)[None, :] * 70
            img.alpha_composite(Image.fromarray(shade.astype(np.uint8), 'RGBA'), (int(x * SS), int(y0 * SS)))
    d.rectangle([(x0 - 7) * SS, (y0 - 14) * SS, (x1 + 7) * SS, y0 * SS], fill=hexc('#1a0f0a')); d.rectangle([(x0 - 7) * SS, y1 * SS, (x1 + 7) * SS, (y1 + 14) * SS], fill=hexc('#1a0f0a'))
    glow(img, 900, 500, 900, hexc('#d6a860'), .15)
    img = st.cut(img, 'screen', .5)
    tatami(img, 1140, 1400, 35, lit=.8)
    img = st.cut(img, 'floor', .8)
    near_foliage(img, [(1380, 1360, 110, 60), (1460, 1300, 70, 50)], 93, [hexc('#2a1216'), hexc('#4a1e28'), hexc('#6e2e3c'), hexc('#8e4454')], (10, 20))
    st.finish(img, 'near', 1.5, blur=5, lift=(9, 7, 5), sat=0.85, gamma=1.05)


def games():
    st = Stack('games'); fog = hexc('#8d9690')
    img = gradient(hexc('#8e9791'), hexc('#4a534d'))
    forest_layers(img, 900, fog, [301, 302], [12, 9], [(600, 760), (760, 900)], [0.8, 0.58], [3.2, 1.8])
    img = st.cut(img, 'sky', .06)
    forest_layers(img, 900, fog, [303], [6], [(900, 1080)], [0.36], [.8])
    img = st.cut(img, 'forest', .22)
    t = layer(); torii(t, 900, 1180, 820, 820, 7, hexc('#3a1f18')); img.alpha_composite(atmos(t, fog, .12))
    ground(img, 1100, 1260, 91, pebbles=500)
    img = st.cut(img, 'torii', .45)
    ground(img, 1150, 1400, 92, pebbles=1500)
    for i, x in enumerate(range(620, 1200, 120)):
        stone(img, x + (i % 2) * 20, 1300 - i * 3, 70, 16, 400 + i, hexc('#4c504a'))
    toro(img, 360, 1250, 250, 8); toro(img, 1440, 1250, 250, 9)
    img = st.cut(img, 'floor', .8)
    cedar(img, -60 * SS, 1300 * SS, 1500 * SS, 380 * SS, 991, PAL_CEDAR, BARK)
    cedar(img, 1860 * SS, 1300 * SS, 1500 * SS, 380 * SS, 992, PAL_CEDAR, BARK)
    img = st.cut(img, 'cedars', 1.0)
    near_fern(img, 420, 1440, 460, 7, lean=.3); near_fern(img, 1400, 1440, 440, 8, lean=-.3)
    near_branch(img, 1560, -50, 1200, 100, 9)
    st.finish(img, 'near', 1.5, blur=5, lift=(9, 12, 11), sat=0.7, gamma=1.1)


def courtyard():
    st = Stack('courtyard'); fog = hexc('#9aa29d')
    img = gradient(hexc('#a3aaa6'), hexc('#6c746f'))
    far = layer(); r_ = random.Random(3); top = [(x, 360 + r_.uniform(-40, 40) + (x - 900) * .02) for x in range(900, 1801, 60)]
    rock_mass(far, top + [(1800, 900), (900, 900)], 5, hexc('#4c524e'), False)
    bushes(far, 380, 900, 1800, 12, PAL_BUSH, 10, 40, 80)
    waterfall_sheet(far, 1500, 1720, 340, 820, 6, .7)
    img.alpha_composite(atmos(far, fog, .62, 2)); img.alpha_composite(fog_layer(fog, 300, 800, .6, 3))
    img = st.cut(img, 'sky', .08)
    rock_mass(img, [(0, 0), (880, 0), (910, 120), (850, 300), (905, 520), (860, 900), (0, 960)], 7, hexc('#262a27'))
    bushes(img, 110, 0, 900, 13, PAL_BUSH, 14, 40, 90)
    for x in (90, 780): pine(img, x * SS, 120 * SS, 300 * SS, 14 + x, PAL_PINE, BARK, lean=.4 if x < 400 else -.4, pads=4, spread=.8)
    for i, (a, b, top_) in enumerate([(110, 340, 105), (290, 580, 115), (540, 780, 130)]):
        waterfall_sheet(img, a, b, top_, 930, 20 + i)
    bushes(img, 180, 380, 900, 8, PAL_BUSH, 6, 40, 80)
    img = st.cut(img, 'cliff', .3)
    m = Image.new('L', (SW, int(330 * SS)), 255)
    img.alpha_composite(textured_fill(m, hexc('#3a4642'), hexc('#1c2422'), hexc('#6a7a74'), 30 * SS, 8, (6, 1), 1.3), (0, int(880 * SS)))
    img.alpha_composite(fog_layer(hexc('#eef1ef'), 760, 1080, 1.2, 9, 120))
    img.alpha_composite(fog_layer(hexc('#e6eae8'), 560, 900, .8, 19, 160))
    for i, (x, y, rx, ry) in enumerate([(1130, 930, 140, 50), (1320, 960, 110, 40), (1560, 945, 160, 54), (1000, 1000, 90, 30)]):
        stone(img, x, y, rx, ry, 30 + i, hexc('#3a3f3b'))
    img = st.cut(img, 'pool', .55)
    ground(img, 1150, 1400, 11, hexc('#3a3d38'), hexc('#1c1e1b'), hexc('#555850'), pebbles=600)
    for i, (x, y, rx, ry) in enumerate([(900, 1330, 260, 58), (520, 1300, 150, 40), (1300, 1310, 170, 44), (160, 1270, 130, 50), (1660, 1270, 140, 52)]):
        stone(img, x, y, rx, ry, 60 + i, hexc('#4a4e48'))
    img = st.cut(img, 'floor', .8)
    wood_block(img, (0, 0, 1800, 70), 71, hexc('#1f1712'), hexc('#0b0806'), hexc('#34281f'))
    wood_block(img, (0, 0, 44, 1400), 72, hexc('#18120e'), hexc('#080605'), hexc('#2a2019'), True)
    wood_block(img, (1756, 0, 1800, 1400), 73, hexc('#18120e'), hexc('#080605'), hexc('#2a2019'), True)
    img = st.cut(img, 'frame', .95)
    near_fern(img, 410, 1440, 470, 10, lean=.35); near_fern(img, 1410, 1440, 450, 11, lean=-.35)
    near_branch(img, 1500, -40, 1150, 110, 12)
    st.finish(img, 'near', 1.5, blur=5, lift=(10, 13, 12), sat=0.6, gamma=1.08)


def entrance():
    st = Stack('entrance')
    img = gradient(hexc('#141a17'), hexc('#070908'))
    forest_layers(img, 800, hexc('#2a332e'), [901, 902], [9, 7], [(700, 900), (900, 1100)], [0.6, 0.35], [2.5, 1.2],
                  pal=[hexc('#070a08'), hexc('#0c110d'), hexc('#121912'), hexc('#1a231a'), hexc('#243024')])
    img = st.cut(img, 'sky', .08)
    for x, w in ((330, 55), (1480, 60)):
        trunk(img, [(x * SS, 1250 * SS), ((x + 6) * SS, -50 * SS)], [w * SS, w * .8 * SS], (hexc('#1f201c'), hexc('#3d3e37'), hexc('#6a6a5e')), x, moss=hexc('#3a4a30'))
    t = layer(); torii(t, 900, 1010, 720, 640, 13, hexc('#62645c'))
    ta = np.asarray(t, np.float32); ln = fbm(SW, SH, 6 * SS, 3, 14); lm = (np.clip((ln - .6) * 4, 0, 1) * (ta[..., 3] > 0))[..., None]
    ta[..., :3] = ta[..., :3] * (1 - lm * .6) + np.array([150, 158, 140], np.float32) * lm * .6
    img.alpha_composite(atmos(Image.fromarray(ta.astype(np.uint8), 'RGBA'), hexc('#2a2f2c'), .12))
    d = ImageDraw.Draw(img); d.rectangle([872 * SS, 450 * SS, 928 * SS, 530 * SS], fill=hexc('#4a4b45'))
    glow(img, 880, 870, 90, hexc('#f0c070'), .5); d.ellipse([872 * SS, 862 * SS, 888 * SS, 878 * SS], fill=hexc('#ffe3a8'))
    ground(img, 960, 1080, 20, hexc('#34332e'), hexc('#161512'), hexc('#57554c'), pebbles=1200)
    img = st.cut(img, 'torii', .38)
    ground(img, 1000, 1400, 21, hexc('#34332e'), hexc('#161512'), hexc('#57554c'), pebbles=4000)
    path = Image.new('L', (SW, SH), 0); ImageDraw.Draw(path).polygon([(560 * SS, 1400 * SS), (1240 * SS, 1400 * SS), (960 * SS, 990 * SS), (840 * SS, 990 * SS)], fill=255)
    box = path.getbbox(); img.alpha_composite(textured_fill(path.crop(box), hexc('#5a5a54'), hexc('#2c2c28'), hexc('#77776e'), 20 * SS, 22, contrast=1.2), (box[0], box[1]))
    d = ImageDraw.Draw(img); rnd = random.Random(8); y = 990.0
    while y < 1400:
        hgt = 10 + (y - 990) * 0.1; u = (y - 990) / 410; xl = 840 - 280 * u; xr = 960 + 280 * u; x = xl
        while x < xr:
            x2 = min(xr, x + (xr - xl) * rnd.uniform(.18, .34))
            d.rectangle([(x + 1.5) * SS, (y + 1.5) * SS, (x2 - 1.5) * SS, (y + hgt - 1.5) * SS], fill=mixc(hexc('#5d5d56'), hexc('#3a3a35'), rnd.random())); x = x2
        y += hgt
    glow(img, 900, 1180, 360, hexc('#9aa0a0'), .12)
    wet = layer(); wd = ImageDraw.Draw(wet)
    for i in range(40):
        yy = 1000 + i * 10; ww = 12 + i * 1.5; wd.rectangle([(890 - ww / 2) * SS, yy * SS, (890 + ww / 2) * SS, (yy + 4) * SS], fill=(240, 200, 130, max(0, 60 - i)))
    img.alpha_composite(wet.filter(ImageFilter.GaussianBlur(4 * SS)))
    stone(img, 1180, 1030, 34, 12, 43, hexc('#4a4b45'))
    m = Image.new('L', (int(60 * SS), int(260 * SS)), 255)
    img.alpha_composite(textured_fill(m, hexc('#6a6b63'), hexc('#34352f'), hexc('#8a8b80'), 12 * SS, 44, contrast=1.3), (int(1150 * SS), int(770 * SS)))
    img = st.cut(img, 'path', .7)
    toro(img, 330, 1260, 520, 31)
    d = ImageDraw.Draw(img); d.rectangle([(330 - 18) * SS, (1260 - 400) * SS, (330 + 18) * SS, (1260 - 350) * SS], fill=hexc('#f2cf8a'))
    glow(img, 330, 885, 260, hexc('#f0c070'), .35)
    for x in (1360, 1640): wood_block(img, (x, 700, x + 26, 1180), 40 + x, hexc('#2a2019'), hexc('#100c09'), hexc('#44362b'), True)
    rd = Image.new('L', (SW, SH), 0); pts = []
    for i in range(21):
        u = i / 20; pts.append(((1230 + 560 * u) * SS, (700 - 150 * math.sin(math.pi * u) ** .6 + 20 * (u - .5) ** 2 * 4) * SS))
    pts += [(1780 * SS, 740 * SS), (1250 * SS, 740 * SS)]
    ImageDraw.Draw(rd).polygon(pts, fill=255); bx = rd.getbbox()
    rt = textured_fill(rd.crop(bx), hexc('#2e3a28'), hexc('#10150d'), hexc('#51623e'), 12 * SS, 41, (3, 1), 1.5)
    ra = np.asarray(rt, np.float32); rows = np.arange(ra.shape[0]); ra[(rows // (9 * SS)) % 2 == 0, :, :3] *= .8
    img.alpha_composite(Image.fromarray(ra.astype(np.uint8), 'RGBA'), (bx[0], bx[1]))
    d = ImageDraw.Draw(img); d.rectangle([1240 * SS, 736 * SS, 1790 * SS, 752 * SS], fill=hexc('#1a130e'))
    d.line([(1330 * SS, 760 * SS), (1480 * SS, 790 * SS), (1660 * SS, 760 * SS)], fill=hexc('#b8a67a'), width=7 * SS)
    for x in (1400, 1520, 1600):
        pts = [(x, 785), (x + 10, 800), (x - 2, 812), (x + 10, 826), (x - 2, 840)]; d.line([(a * SS, b * SS) for a, b in pts], fill=hexc('#e8e4d8'), width=5 * SS)
    basin = Image.new('L', (int(420 * SS), int(170 * SS)), 255)
    img.alpha_composite(textured_fill(basin, hexc('#5a5c55'), hexc('#2c2e2a'), hexc('#7a7c72'), 16 * SS, 42, contrast=1.3), (int(1300 * SS), int(1030 * SS)))
    d.rectangle([1320 * SS, 1030 * SS, 1700 * SS, 1052 * SS], fill=hexc('#1a2424'))
    for x in (1380, 1450, 1520): d.line([(x * SS, 1040 * SS), ((x + 60) * SS, 1000 * SS)], fill=hexc('#9a8a5a'), width=3 * SS)
    img = st.cut(img, 'shrine', .85)
    for x, w in ((120, 70), (1700, 80)):
        trunk(img, [(x * SS, 1450 * SS), ((x + 6) * SS, -50 * SS)], [w * SS, w * .8 * SS], (hexc('#15160f'), hexc('#2d2e28'), hexc('#4a4a42')), x, moss=hexc('#2a3622'))
    img = st.cut(img, 'trunks', 1.05)
    near_fern(img, 420, 1440, 460, 13, lean=.35); near_fern(img, 1420, 1440, 380, 15, lean=-.3); near_branch(img, 1480, -40, 1180, 120, 14)
    st.finish(img, 'near', 1.5, blur=5, lift=(5, 7, 6), sat=0.55, gamma=1.12)


if __name__ == '__main__':
    import os
    names = sys.argv[2:] or ['engawa', 'kitchen', 'onsen', 'bedroom_on', 'bedroom_off', 'wardrobe', 'games', 'courtyard', 'entrance']
    if os.path.exists(f'{OUT}/layers.json'): MANIFEST.update(json.load(open(f'{OUT}/layers.json')))
    for n in names:
        set_size(1800, 1400)
        if n == 'bedroom_on': bedroom(True)
        elif n == 'bedroom_off': bedroom(False)
        else: globals()[n]()
    json.dump(MANIFEST, open(f'{OUT}/layers.json', 'w'))
