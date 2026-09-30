#!/usr/bin/env python3
"""Two new rooms for «Мусин дом» (idea #10, add-on rooms2): the tea house 茶室 and the forest shrine 祠.
Each room is painted as depth layers like layers.py / matsuri.py, plus ~30 decorations per room packed into one atlas.
Usage: cd art && python3 rooms2_art.py ../assets
  → ../assets/layers/chashitsu_<layer>.webp, hokora_<layer>.webp, ../assets/items/atlas_cha.webp, atlas_hok.webp
  → art/rooms2.json (item rows with "at", room hot-spots); previews → art/out/"""
import json, math, os, random, shutil, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
ASSETS = os.path.abspath(sys.argv[1]); HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv[1] = os.path.join(ASSETS, 'layers')          # layers.py / items.py read their output folder from argv
import paint as P
from paint import hexc, mixc, fbm, textured_fill, layer, gradient, atmos, fog_layer, glow, wood_block, ground, cedar, trunk, SS, SW, SH
import layers as LY
from layers import Stack, near_fern, near_foliage, near_branch
import items as I
from items import px, SERIF, SANS, canvas, fill, volume, soft, floor_shadow, line, ell, poly, text, H, dk, lt, mask_poly
from room_items import clip, rope, blob, cr, figure_base, plate, WOOD, WOOD_D, WOOD_L

LY.OUT = os.path.join(ASSETS, 'layers'); OUTI = os.path.join(ASSETS, 'items'); PREV = os.path.join(HERE, 'out')
os.makedirs(PREV, exist_ok=True)
BLACK = (0, 0, 0, 255)
WARM = hexc('#ffb45a')
META = {}
T20, ASP = math.tan(math.radians(20)), 1800 / 1400


def fz(Z): return 700 + 2950 / Z                      # image y of the ground at depth Z (camera of index.html)
def fx(X, Z): return 900 + X / (Z * T20 * ASP) * 900  # image x of a ground point


def comp(img, patch, x, y):
    x, y = int(x), int(y); sx, sy = max(0, -x), max(0, -y)
    w, h = min(patch.width - sx, img.width - x - sx), min(patch.height - sy, img.height - y - sy)
    if w > 0 and h > 0: img.alpha_composite(patch.crop((sx, sy, sx + w, sy + h)), (x + sx, y + sy))


def lglow(img, cx, cy, r, col, strength, squash=1.0):
    n = max(4, int(r)); yy, xx = np.mgrid[0:n, 0:n]
    d = np.sqrt(((xx - n / 2) / (n / 2)) ** 2 + ((yy - n / 2) / (n / 2 * squash)) ** 2)
    a = np.clip(1 - d, 0, 1) ** 2 * strength * 255
    g = Image.new('RGBA', (n, n), H(col)); g.putalpha(Image.fromarray(a.astype(np.uint8)))
    comp(img, g.resize((int(2 * r * SS), int(2 * r * SS)), Image.BICUBIC), (cx - r) * SS, (cy - r) * SS)


def shade(img, box, top_k, bot_k, horiz=False):
    x0, y0, x1, y1 = (px(v) for v in box); x0, y0 = max(0, x0), max(0, y0); x1, y1 = min(img.width, x1), min(img.height, y1)
    reg = np.asarray(img.crop((x0, y0, x1, y1)), np.float32)
    ramp = np.linspace(top_k, bot_k, reg.shape[1] if horiz else reg.shape[0])
    reg[..., :3] *= ramp[None, :, None] if horiz else ramp[:, None, None]
    img.paste(Image.fromarray(np.clip(reg, 0, 255).astype(np.uint8), 'RGBA'), (x0, y0))


def fibres(img, box, n, seed, col=(214, 180, 110), a=(40, 110)):
    """Chopped straw in a clay wall (tsuchikabe)."""
    rnd = random.Random(seed); d = ImageDraw.Draw(img); x0, y0, x1, y1 = box
    for _ in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1); L = rnd.uniform(4, 14); t = rnd.uniform(0, math.pi)
        d.line([(px(x), px(y)), (px(x + math.cos(t) * L), px(y + math.sin(t) * L))], fill=col + (int(rnd.uniform(*a)),), width=px(rnd.uniform(.8, 1.6)))


def bamboo_stick(img, pts, w, col='#8a7a4a', seed=0):
    line(img, pts, dk(H(col), .45), w + 1.2); line(img, pts, col, w); line(img, [(x - w * .2, y - w * .2) for x, y in pts], lt(H(col), .3), max(.6, w * .3))


def shide(img, x, y, s=1.0):
    """Zigzag paper streamer."""
    pts = [(x, y), (x + 9 * s, y + 10 * s), (x - 1 * s, y + 18 * s), (x + 10 * s, y + 30 * s), (x, y + 38 * s), (x + 11 * s, y + 52 * s)]
    for (a, b), (c, e) in zip(pts, pts[1:]):
        poly(img, [(a - 5 * s, b), (a + 6 * s, b), (c + 6 * s, e), (c - 5 * s, e)], '#eeeadf')
    line(img, [(x, y - 4 * s), (x, y + 2 * s)], '#d8d2c2', 1.2)


def straw_rope(img, pts, w, seed, col='#b89a5a'):
    """Twisted straw shimenawa along a polyline."""
    line(img, pts, dk(H(col), .45), w + 3); line(img, pts, col, w)
    d = ImageDraw.Draw(img); L = 0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        seg = math.hypot(x1 - x0, y1 - y0); n = max(1, int(seg / (w * .55)))
        for k in range(n):
            u = k / n; x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
            d.line([(px(x - w * .28), px(y - w * .42)), (px(x + w * .28), px(y + w * .42))], fill=dk(H(col), .35)[:3] + (200,), width=px(max(1, w * .12)))
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d.line([(px(x0), px(y0 - w * .3)), (px(x1), px(y1 - w * .3))], fill=lt(H(col), .25)[:3] + (120,), width=px(max(1, w * .15)))


# ═════════════════════════════ 茶室 THE TEA HOUSE ═════════════════════════════
CLAY, CLAY_D, CLAY_L = hexc('#6e5c43'), hexc('#46392a'), hexc('#8a7556')


def night_falloff(img, lights, amount):
    """Darken the layer away from the light sources (andon, hearth, window)."""
    a = np.asarray(img, np.float32); h, w = a.shape[:2]; yy, xx = np.mgrid[0:h:4, 0:w:4] / SS; lit = np.zeros(yy.shape, np.float32)
    for cx, cy, r in lights: lit = np.maximum(lit, np.clip(1 - np.hypot(xx - cx, yy - cy) / r, 0, 1) ** 1.5)
    k = np.asarray(Image.fromarray(((1 - amount * (1 - lit)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
    a[..., :3] *= k[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def tea_wall():
    img = gradient(hexc('#2c241a'), hexc('#1c170f'))
    I.fill(img, CLAY, 3001, rect=(0, 96, 1800, 1140), scale=70, contrast=.8, dark=.35, light=.18)
    fibres(img, (0, 100, 1800, 1140), 1500, 3, a=(20, 60))
    # low reed ceiling and the lintel
    I.fill(img, '#2a2116', 3002, rect=(0, 0, 1800, 70), scale=6, stretch=(8, .3), contrast=1.2)
    d = ImageDraw.Draw(img)
    for y in range(4, 70, 9): d.line([(0, px(y)), (px(1800), px(y))], fill=(12, 9, 6, 120), width=px(1.4))
    wood_block(img, (0, 70, 1800, 100), 3003, hexc('#3a2c1f'), hexc('#150f0a'), hexc('#5a4430'))
    # koshibari: old washi pasted along the bottom of the wall
    for i, x in enumerate(range(0, 1800, 132)):
        for j, (y0, y1) in enumerate(((1010, 1076), (1074, 1140))):
            I.fill(img, '#4a4d52' if (i + j) % 2 else '#55575a', 3010 + i * 2 + j, rect=(x + (j * 66) % 132 - 66, y0, x + (j * 66) % 132 + 68, y1), scale=5, contrast=.5, dark=.2, light=.12)
    d.line([(0, px(1010)), (px(1800), px(1010))], fill=hexc('#2a2419'), width=px(3))
    # shitajimado: clay left off, bamboo lath shows, moonlit paper behind
    x0, y0, x1, y1 = 130, 330, 340, 540
    I.fill(img, '#8d9296', 3020, rect=(x0, y0, x1, y1), scale=8, contrast=.5, dark=.15, light=.12)
    glow(img, (x0 + x1) / 2, (y0 + y1) / 2, 160, hexc('#b8c4d0'), .18)
    for x in range(x0 + 14, x1, 30): bamboo_stick(img, [(x, y0 - 6), (x + 2, y1 + 6)], 5, '#6a5a3a')
    for y in range(y0 + 20, y1, 44): bamboo_stick(img, [(x0 - 6, y), (x1 + 6, y + 1)], 4, '#6a5a3a')
    for x in range(x0 + 14, x1, 30):
        for y in range(y0 + 20, y1, 44): I.ell(img, (x - 3, y - 3, x + 4, y + 4), '#2a2016')
    I.soft(img, lambda dd: dd.rectangle([px(x0), px(y0), px(x1), px(y0 + 16)], fill=(20, 14, 8, 160)), 4)
    # host's door (sadōguchi) with an arched top
    m = Image.new('L', img.size, 0); md = ImageDraw.Draw(m)
    md.rectangle([px(120), px(700), px(410), px(1140)], fill=255); md.ellipse([px(120), px(600), px(410), px(800)], fill=255)
    I.fill(img, '#3c3528', 3021, mask=m, scale=10, contrast=.6, dark=.25, light=.12)
    d.arc([px(120), px(600), px(410), px(800)], 180, 360, fill=hexc('#1a130c'), width=px(6))
    for x in (120, 410): d.line([(px(x), px(700)), (px(x), px(1140))], fill=hexc('#1a130c'), width=px(6))
    d.line([(px(265), px(610)), (px(265), px(1140))], fill=(20, 15, 10, 150), width=px(2))
    I.ell(img, (372, 900, 392, 920), '#171109'); I.ell(img, (376, 904, 388, 916), '#5a4a30')
    # posts
    for bx, sd in ((0, 3030), (470, 3031), (1400, 3032), (1770, 3033)):
        wood_block(img, (bx, 96, bx + 34, 1140), sd, hexc('#3a2c1f'), hexc('#140e09'), hexc('#5a4430'), True)
    # the round window: moonlit garden behind a bamboo lattice
    cx, cy, R = 1190, 560, 190
    view = gradient(hexc('#56647a'), hexc('#1c2630'), h=px(2 * R), w=px(2 * R))
    v = layer(); v.alpha_composite(view, (px(cx - R), px(cy - R)))
    lglow(v, 1262, 452, 150, '#dfe6f0', .55); I.ell(v, (1226, 416, 1298, 488), '#f2eee0'); I.soft(v, lambda dd: dd.ellipse([px(1236), px(424), px(1270), px(456)], fill=(200, 196, 180, 90)), 3)
    v.alpha_composite(fog_layer(hexc('#8a98a6'), 560, 700, .55, 3040, 120))
    g = layer(); rnd = random.Random(3041)
    for k in range(9):                                          # bamboo grove silhouettes
        x = cx - R + 20 + k * 44 + rnd.uniform(-10, 10); c = mixc(hexc('#101814'), hexc('#2a3830'), rnd.random() * .6)
        line(g, [(x, cy + R + 10), (x + rnd.uniform(-14, 14), cy - R - 20)], c, rnd.uniform(5, 9))
        for y in range(int(cy - R), int(cy + R), 36): line(g, [(x - 5, y), (x + 5, y)], dk(c, .4), 2)
        for _ in range(7):
            y = rnd.uniform(cy - R, cy + 40); s = rnd.choice((-1, 1))
            poly(g, [(x, y), (x + s * rnd.uniform(26, 44), y + rnd.uniform(4, 14)), (x + s * 8, y + 7)], c)
    P.toro(g, 1110, cy + 150, 110, 3042)
    lglow(g, 1110, cy + 80, 40, '#ffb060', .8)
    v.alpha_composite(atmos(g, hexc('#5a6a78'), .3, .6)); v.alpha_composite(fog_layer(hexc('#7a8896'), 640, 760, .5, 3043, 90))
    mk = Image.new('L', img.size, 0); ImageDraw.Draw(mk).ellipse([px(cx - R), px(cy - R), px(cx + R), px(cy + R)], fill=255)
    img.paste(v, (0, 0), mk)
    lat = layer()
    for x in range(cx - R + 16, cx + R, 34): bamboo_stick(lat, [(x, cy - R), (x + 1, cy + R)], 4.2, '#8a7648')
    for y in range(cy - R + 30, cy + R, 60): bamboo_stick(lat, [(cx - R, y), (cx + R, y + 1)], 3.6, '#7a6840')
    a = np.asarray(lat, np.float32); a[..., 3] *= np.asarray(mk, np.float32) / 255; img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))
    ring = Image.new('L', img.size, 0); rd = ImageDraw.Draw(ring); rd.ellipse([px(cx - R - 12), px(cy - R - 12), px(cx + R + 12), px(cy + R + 12)], fill=255); rd.ellipse([px(cx - R), px(cy - R), px(cx + R), px(cy + R)], fill=0)
    I.fill(img, CLAY_L, 3044, mask=ring, scale=10, contrast=.7)
    I.soft(img, lambda dd: dd.arc([px(cx - R + 2), px(cy - R + 2), px(cx + R - 2), px(cy + R - 2)], 190, 350, fill=(12, 8, 4, 190), width=px(10)), 5)
    # nijiriguchi: the low crawl-in door, slid half open onto the night garden
    nx0, ny0, nx1, ny1 = 1460, 830, 1720, 1140
    out = gradient(hexc('#2a3440'), hexc('#161c16'), h=px(ny1 - ny0), w=px(nx1 - nx0)); o = layer(); o.alpha_composite(out, (px(nx0), px(ny0)))
    P.bushes(o, 1000, 1480, 1720, 3050, P.PAL_BUSH, 5, 40, 80)
    I.fill(o, '#6a6e70', 3051, ell=(1560, 1080, 1700, 1122), scale=5, contrast=1.1); lglow(o, 1630, 1090, 90, '#a8b8d0', .35, .4)
    mk = Image.new('L', img.size, 0); ImageDraw.Draw(mk).rectangle([px(nx0), px(ny0), px(nx1), px(ny1)], fill=255); img.paste(o, (0, 0), mk)
    wood_block(img, (nx0 - 16, ny0 - 18, nx1 + 16, ny0), 3052, hexc('#3a2c1f'), hexc('#140e09'), hexc('#5a4430'))
    for bx in (nx0 - 16, nx1): wood_block(img, (bx, ny0, bx + 16, ny1), 3053 + bx, hexc('#3a2c1f'), hexc('#140e09'), hexc('#5a4430'), True)
    for k in range(4): wood_block(img, (nx0 + k * 38, ny0 + 4, nx0 + k * 38 + 38, ny1 - 2), 3060 + k, hexc('#4a3a28'), hexc('#1e150d'), hexc('#6a5438'), True)
    for y in (ny0 + 60, ny1 - 70): wood_block(img, (nx0, y, nx0 + 152, y + 12), 3065 + y, hexc('#3a2c1f'), hexc('#140e09'), hexc('#5a4430'))
    shade(img, (nx0, ny0, nx0 + 152, ny1), .9, .7)
    # warm light of the andon on the left and the hearth on the right, cool moonlight at the window
    glow(img, 300, 900, 760, hexc('#f0b060'), .26); glow(img, 1120, 1080, 520, hexc('#e08a40'), .12); glow(img, 1190, 560, 360, hexc('#b8c8e0'), .08)
    shade(img, (0, 96, 1800, 400), .72, 1.0)
    return night_falloff(img, [(300, 900, 900), (1120, 1100, 700), (1190, 560, 420)], .5)


def tea_alcove(img):
    # tokonoma: a recess with a darker back wall, a lacquered sill and a natural log post
    x0, x1 = 505, 965
    I.fill(img, '#5c4b36', 3101, rect=(x0, 100, x1, 1062), scale=60, contrast=.8, dark=.3, light=.16)
    fibres(img, (x0, 100, x1, 1062), 400, 3102, (200, 168, 104), a=(18, 50))
    wood_block(img, (x0, 100, x1 + 10, 150), 3103, hexc('#3a2c1f'), hexc('#140e09'), hexc('#5a4430'))
    shade(img, (x0, 150, x1, 1062), .55, 1.0); shade(img, (x0, 150, x0 + 60, 1062), .6, 1.0, True)
    I.soft(img, lambda d: d.rectangle([px(x0), px(150), px(x1), px(190)], fill=(10, 7, 4, 170)), 8)
    # the hanging scroll: 一期一会
    sx0, sx1 = 682, 808
    line(img, [(sx0 + 20, 196), (745, 168), (sx1 - 20, 196)], '#1a120c', 1.6); I.ell(img, (741, 162, 749, 170), '#8a7040')
    I.fill(img, '#3e3c2a', 3104, rect=(sx0, 196, sx1, 820), scale=6, contrast=1.1)
    I.fill(img, '#6a5a3a', 3105, rect=(sx0 + 8, 250, sx1 - 8, 262), scale=3); I.fill(img, '#6a5a3a', 3106, rect=(sx0 + 8, 752, sx1 - 8, 764), scale=3)
    I.fill(img, '#e2d8bf', 3107, rect=(sx0 + 14, 272, sx1 - 14, 742), scale=10, contrast=.6, dark=.12, light=.1)
    for k, ch in enumerate('一期一会'): I.text(img, ch, 745, 332 + k * 102, 78, '#1b1714', SERIF, brush=True)
    ImageDraw.Draw(img).rectangle([px(760), px(706), px(774), px(722)], fill=hexc('#a8302a'))
    for y in (196, 812): I.fill(img, '#1e150d', 3108 + y, rect=(sx0 - 8, y - 2, sx1 + 8, y + 10), scale=3)
    for x in (sx0 - 12, sx1 + 4): I.fill(img, '#c8a860', 3110 + x, rect=(x, 810, x + 10, 824), scale=2)
    I.soft(img, lambda d: d.rectangle([px(sx1), px(210), px(sx1 + 14), px(820)], fill=(0, 0, 0, 90)), 6)
    # bamboo vase with a single camellia, standing on the toko floor
    vx, vb = 610, 1060
    I.soft(img, lambda d: d.ellipse([px(vx - 34), px(vb - 8), px(vx + 34), px(vb + 6)], fill=(0, 0, 0, 150)), 4)
    I.fill(img, '#9a8a50', 3120, rect=(vx - 24, 880, vx + 24, vb), scale=4, stretch=(.3, 4), contrast=.9)
    volume(img, (vx - 24, 880, vx + 24, vb), .6, .45, spec=.25)
    for y in (940, 1010): I.line(img, [(vx - 24, y), (vx + 24, y)], '#5a4a26', 3)
    I.ell(img, (vx - 24, 872, vx + 24, 888), '#3a3018'); I.ell(img, (vx - 18, 875, vx + 18, 885), '#18120a')
    for (a, b, c_, e) in ((vx, 878, vx - 50, 810), (vx + 2, 878, vx + 30, 792), (vx, 878, vx - 12, 770)):
        I.line(img, [(a, b), ((a + c_) / 2 + 4, (b + e) / 2), (c_, e)], '#2a2a16', 3)
    for lx, ly, ang in ((vx - 56, 812, -.5), (vx - 30, 836, .4), (vx + 34, 794, .9), (vx - 18, 772, -.9), (vx + 10, 830, 2.2)):
        L = 30; pts = [(lx + math.cos(ang + k * math.pi / 5) * (L if k % 5 == 0 else L * .45 * math.sin(k * math.pi / 5) + 6), ly + math.sin(ang + k * math.pi / 5) * (L if k % 5 == 0 else L * .45)) for k in range(10)]
        I.fill(img, '#1e3a22', 3130 + lx, poly=[(lx - 20 * math.cos(ang), ly - 20 * math.sin(ang)), (lx + 8 * math.cos(ang + 1.6), ly + 8 * math.sin(ang + 1.6)), (lx + 24 * math.cos(ang), ly + 24 * math.sin(ang)), (lx + 8 * math.cos(ang - 1.6), ly + 8 * math.sin(ang - 1.6))], scale=3, contrast=1.2)
        I.line(img, [(lx - 16 * math.cos(ang), ly - 16 * math.sin(ang)), (lx + 20 * math.cos(ang), ly + 20 * math.sin(ang))], '#3a5a3a', 1)
    fx_, fy_ = vx - 14, 764
    fl = layer(); camellia(fl, fx_, fy_, 22, 3140); I.ell(fl, (fx_ - 4, fy_ - 4, fx_ + 4, fy_ + 4), '#f4e090'); img.alpha_composite(fl)
    I.fill(img, '#8a1a22', 3150, ell=(vx + 22, 784, vx + 38, 804), scale=2); I.fill(img, '#2a4a26', 3151, poly=[(vx + 22, 800), (vx + 38, 800), (vx + 30, 812)], scale=2)
    # sill and toko floor front
    wood_block(img, (x0 - 6, 1060, x1 + 10, 1086), 3160, hexc('#1a1410'), hexc('#060404'), hexc('#3a2e26'))
    ImageDraw.Draw(img).line([(px(x0 - 6), px(1061)), (px(x1 + 10), px(1061))], fill=(150, 120, 80, 140), width=px(1.5))
    wood_block(img, (x0 - 6, 1086, x1 + 10, 1140), 3161, hexc('#3a2c1f'), hexc('#140e09'), hexc('#5a4430'))
    # toko-bashira: a natural log with bark and knots
    I.fill(img, '#6a5234', 3162, poly=[(965, 100), (1004, 100), (1008, 600), (1002, 1140), (962, 1140), (968, 600)], scale=6, stretch=(.2, 5), contrast=1.4)
    volume(img, (962, 100, 1008, 1140), .5, .5, spec=.1)
    for ky in (330, 610, 880): I.ell(img, (976, ky, 992, ky + 20), '#2a1c10'); I.ell(img, (979, ky + 4, 989, ky + 14), '#5a4428')
    glow(img, 300, 900, 700, hexc('#f0b060'), .1)
    return img


def tatami_floor(img, y0, seed):
    """Tatami seen from a cat's height: weave, perspective seams and dark heri borders."""
    h = (1400 - y0) * SS
    n = fbm(SW, h, 30 * SS, 4, seed, (4, 1))
    yy = np.arange(h)[:, None] / SS + y0; Z = 2950 / (yy - 700)
    weave = (np.sin(yy / (1.2 + (yy - y0) / 200)) * .5 + .5) * .22
    v = np.clip(.55 * n + weave + .2, 0, 1)
    b = np.array(hexc('#5a5638')[:3], np.float32)
    rgb = b[None, None] * (.55 + .6 * v[..., None]) * np.clip(1.25 - (Z - 4) * .09, .7, 1.1)[..., None]
    img.alpha_composite(Image.fromarray(np.dstack([np.clip(rgb, 0, 255), np.full((h, SW), 255)]).astype(np.uint8), 'RGBA'), (0, y0 * SS))
    heri = hexc('#1c1812'); Zs, Ze = 2950 / (y0 - 700), 2950 / 700
    for X in (-2.9, -1.4, 1.5):
        I.poly(img, [(fx(X - .03, Zs), y0), (fx(X + .03, Zs), y0), (fx(X + .03, Ze), 1400), (fx(X - .03, Ze), 1400)], heri)
    for Zh in (5.25,):
        I.poly(img, [(fx(-1.4, Zh), fz(Zh) - 2), (fx(1.5, Zh), fz(Zh) - 2), (fx(1.5, Zh), fz(Zh) + 5), (fx(-1.4, Zh), fz(Zh) + 5)], heri)


def tea_floor(img):
    tatami_floor(img, 1140, 3201)
    I.soft(img, lambda d: d.rectangle([0, px(1136), px(1800), px(1160)], fill=(10, 7, 4, 150)), 6)
    # the sunken hearth (ro): black lacquered frame, ash and glowing charcoal under the kettle
    q = lambda X, Z: (fx(X, Z), fz(Z))
    X0, X1, Z0, Z1 = .35, .95, 5.4, 6.0
    I.fill(img, '#1c1612', 3202, poly=[q(X0 - .07, Z1 + .08), q(X1 + .07, Z1 + .08), q(X1 + .07, Z0 - .07), q(X0 - .07, Z0 - .07)], scale=4, contrast=.8)
    I.fill(img, '#8a8278', 3203, poly=[q(X0, Z1), q(X1, Z1), q(X1, Z0), q(X0, Z0)], scale=3, contrast=.9, dark=.4, light=.2)
    shade(img, (fx(X0, Z0), fz(Z1), fx(X1, Z0), fz(Z0)), .45, .95)
    for k in range(6):
        X, Z = X0 + .12 + (k % 3) * .17, 5.62 + (k // 3) * .16
        I.fill(img, '#2a1a12', 3210 + k, ell=(fx(X, Z) - 14, fz(Z) - 5, fx(X, Z) + 14, fz(Z) + 5), scale=2)
        lglow(img, fx(X, Z), fz(Z), 14, '#ff5a18', .45, .45)
    lglow(img, fx(.65, 5.7), fz(5.7), 170, '#ff8a3a', .35, .45)
    ImageDraw.Draw(img).line([q(X0 - .07, Z0 - .07)[0] * SS, q(X0 - .07, Z0 - .07)[1] * SS, q(X1 + .07, Z0 - .07)[0] * SS, q(X1 + .07, Z0 - .07)[1] * SS], fill=(180, 150, 110, 150), width=px(1.6))
    META['cha'] = {'kama': [round(fx(.65, 5.72)), round(fz(5.72))], 'ro': [round(fx(.65, 5.7)), round(fz(5.7))]}
    # andon on the left, standing at the wall line
    ax, ab = 300, 1152
    I.soft(img, lambda d: d.ellipse([px(ax - 70), px(ab - 12), px(ax + 70), px(ab + 10)], fill=(0, 0, 0, 150)), 6)
    lglow(img, ax, 1000, 260, '#ffb050', .55, .9)
    for lx in (ax - 52, ax + 44): wood_block(img, (lx, 880, lx + 8, ab), 3220 + lx, hexc('#2a1c12'), hexc('#0e0906'), hexc('#4a3424'), True)
    I.fill(img, '#f4d8a0', 3222, rect=(ax - 46, 900, ax + 46, 1100), scale=5, contrast=.5, dark=.1, light=.2)
    shade(img, (ax - 46, 900, ax + 46, 1100), 1.05, .92); shade(img, (ax - 46, 900, ax + 46, 1100), .85, 1.0, True)
    for y in (900, 1000, 1100): wood_block(img, (ax - 52, y - 4, ax + 52, y + 4), 3223 + y, hexc('#2a1c12'), hexc('#0e0906'), hexc('#4a3424'))
    I.line(img, [(ax, 1000), (ax, 1100)], '#3a2a18', 2)
    wood_block(img, (ax - 58, 870, ax + 58, 882), 3226, hexc('#2a1c12'), hexc('#0e0906'), hexc('#4a3424'))
    lglow(img, ax, 1170, 180, '#ffb050', .3, .25)
    META['cha']['andon'] = [ax, 1000]
    # moonlight spilling in through the crawl-in door
    I.soft(img, lambda d: d.polygon([(px(1560), px(1140)), (px(1720), px(1140)), (px(1800), px(1250)), (px(1600), px(1250))], fill=(170, 190, 220, 50)), 14)
    return night_falloff(img, [(300, 1150, 700), (1120, 1220, 600), (900, 1400, 700)], .45)


def tea_near(img):
    wood_block(img, (1726, -20, 1800, 1420), 3301, hexc('#1a130d'), hexc('#070504'), hexc('#2c2118'), True)
    # a low folding screen (furosaki) just in front of the lens, bottom left
    for k in range(3):
        x0 = -40 + k * 118
        I.fill(img, '#8a7c60', 3302 + k, rect=(x0 + 8, 1270, x0 + 112, 1420), scale=10, contrast=.6, dark=.2, light=.1)
        shade(img, (x0 + 8, 1270, x0 + 112, 1420), .7 if k % 2 else .85, .45 if k % 2 else .6, True)
        wood_block(img, (x0, 1260, x0 + 8, 1420), 3306 + k, hexc('#1a130d'), hexc('#070504'), hexc('#2c2118'), True)
    wood_block(img, (-40, 1256, 322, 1272), 3310, hexc('#1a130d'), hexc('#070504'), hexc('#2c2118'))
    return img


def chashitsu():
    P.set_size(1800, 1400)
    st = Stack('chashitsu')
    img = tea_wall(); img = st.cut(img, 'wall', .4)
    img = tea_alcove(img); img = st.cut(img, 'alcove', .5)
    img = tea_floor(img); img = st.cut(img, 'floor', .8)
    img = tea_near(img)
    st.finish(img, 'near', 1.4, blur=6, lift=(10, 8, 5), sat=0.82, gamma=1.03)
    META['cha'].update({'scroll': [682, 196, 808, 824], 'vase': [610, 1060], 'window': [1190, 560, 190]})


# ═════════════════════════════ 祠 THE FOREST SHRINE ═════════════════════════════
MOSS = [hexc('#1e2a18'), hexc('#2a3a20'), hexc('#3a4e2a'), hexc('#4e6436')]
STONE, STONE_D, STONE_L = hexc('#5a5c56'), hexc('#2a2c28'), hexc('#7e8076')
PAL_DARK = [hexc('#070a08'), hexc('#0c110d'), hexc('#121912'), hexc('#1a231a'), hexc('#243024')]


def moss_on(img, box, seed, amount=.5):
    """Mottle moss over whatever is painted inside box (keeps alpha)."""
    x0, y0, x1, y1 = (max(0, px(v)) for v in box); x1 = min(img.width, x1); y1 = min(img.height, y1)
    reg = np.asarray(img.crop((x0, y0, x1, y1)), np.float32); h, w = reg.shape[:2]
    n = fbm(w, h, 10 * SS, 4, seed); top = np.linspace(1.0, .55, h)[:, None]
    m = np.clip((n - (1 - amount)) * 3, 0, 1) * top * (reg[..., 3] > 0)
    col = np.array([58, 78, 40], np.float32) * (.7 + .6 * n[..., None])
    reg[..., :3] = reg[..., :3] * (1 - m[..., None]) + col * m[..., None]
    img.paste(Image.fromarray(reg.astype(np.uint8), 'RGBA'), (x0, y0))


def stone_lantern(img, x, base, h, seed, lit=True):
    """Kasuga tōrō: base, pole, fire box with glowing windows, roof with curled corners, jewel."""
    s = h / 380; w = lambda v: v * s
    I.soft(img, lambda d: d.ellipse([px(x - w(90)), px(base - w(14)), px(x + w(90)), px(base + w(12))], fill=(0, 0, 0, 150)), 6)
    parts = [((x - w(70), base - w(40), x + w(70), base), 1.0), ((x - w(26), base - w(170), x + w(26), base - w(40)), .9),
             ((x - w(60), base - w(196), x + w(60), base - w(170)), 1.0)]
    for k, (bx, _) in enumerate(parts):
        I.fill(img, STONE, seed + k, rect=bx, scale=6, contrast=1.3, dark=.5, light=.25); volume(img, bx, .5, .35)
    fb = (x - w(44), base - w(270), x + w(44), base - w(196))
    I.fill(img, STONE, seed + 5, rect=fb, scale=6, contrast=1.3, dark=.5, light=.25); volume(img, fb, .5, .3)
    win = (x - w(24), base - w(258), x + w(24), base - w(208))
    I.fill(img, '#ffc070' if lit else '#1a1a16', seed + 6, rect=win, scale=3, contrast=.5, dark=.2, light=.3)
    if lit: lglow(img, x, base - w(233), w(120), '#ffae50', .6)
    I.line(img, [(x, win[1]), (x, win[3])], '#3a3a34', w(4))
    roof = [(x - w(96), base - w(268)), (x + w(96), base - w(268)), (x + w(104), base - w(282)), (x + w(40), base - w(318)), (x - w(40), base - w(318)), (x - w(104), base - w(282))]
    I.fill(img, STONE, seed + 7, poly=roof, scale=6, contrast=1.3, dark=.5, light=.25); volume(img, (x - w(104), base - w(318), x + w(104), base - w(268)), .5, .3)
    I.fill(img, STONE, seed + 8, ell=(x - w(22), base - w(360), x + w(22), base - w(316)), scale=4, contrast=1.2); volume(img, (x - w(22), base - w(360), x + w(22), base - w(316)), .5, .4)
    I.poly(img, [(x - w(8), base - w(356)), (x + w(8), base - w(356)), (x, base - w(380))], STONE_D)
    moss_on(img, (x - w(110), base - w(380), x + w(110), base), seed + 9, .55)
    return (x, base - w(233))


def kitsune(img, x, base, h, seed, flip=False, holds='jewel'):
    """A seated stone fox of an Inari shrine, side view, red bib; returns the eye position."""
    tmp = layer(); s = h / 300; f = -1 if flip else 1
    X = lambda v: x + f * v * s; Y = lambda v: base - v * s
    ped = [(X(-70), Y(0)), (X(70), Y(0)), (X(62), Y(46)), (X(-62), Y(46))]
    I.fill(tmp, STONE, seed, poly=ped, scale=6, contrast=1.3, dark=.5, light=.25); volume(tmp, (x - 70 * s, Y(46), x + 70 * s, Y(0)), .5, .3)
    I.fill(tmp, STONE_L, seed + 1, poly=[(X(-66), Y(46)), (X(66), Y(46)), (X(60), Y(58)), (X(-60), Y(58))], scale=4)
    col = hexc('#8a8a80')
    blob(tmp, [(X(-40), Y(58)), (X(-60), Y(110)), (X(-70), Y(170)), (X(-84), Y(230)), (X(-66), Y(260)), (X(-48), Y(214)), (X(-34), Y(150)), (X(-14), Y(62))], col, seed + 2, k=.4)     # tail
    blob(tmp, [(X(-34), Y(58)), (X(-44), Y(120)), (X(-20), Y(186)), (X(10), Y(214)), (X(30), Y(196)), (X(34), Y(130)), (X(40), Y(58))], col, seed + 3)                               # body
    blob(tmp, [(X(18), Y(58)), (X(16), Y(140)), (X(34), Y(140)), (X(38), Y(58))], dk(col, .08), seed + 4, k=.35)                                                                           # foreleg
    hx, hy = X(18), Y(226)
    blob(tmp, [(X(-8), Y(206)), (X(-6), Y(236)), (X(10), Y(250)), (X(30), Y(246)), (X(64), Y(222)), (X(70), Y(212)), (X(40), Y(200)), (X(14), Y(196))], col, seed + 5)                  # head & snout
    for e, (a, b) in enumerate(((-4, 4), (12, 18))):
        blob(tmp, [(X(a - 6), Y(240)), (X(a + 2), Y(292)), (X(b + 10), Y(244))], col, seed + 6 + e, scale=3, k=.3)                                                                         # ears
    I.line(tmp, [(X(24), Y(228)), (X(40), Y(224))], '#2a2622', 2.4)
    ex, ey = X(32), Y(226)
    I.ell(tmp, (X(66) - 4, Y(214) - 4, X(66) + 4, Y(214) + 4), '#2a2622')
    blob(tmp, [(X(-6), Y(196)), (X(40), Y(200)), (X(34), Y(160)), (X(14), Y(146)), (X(0), Y(166))], hexc('#b02a22'), seed + 8, scale=3, k=.3)                                                # red bib
    if holds == 'jewel': I.ell(tmp, (X(56) - 13, Y(208) - 13, X(56) + 13, Y(208) + 13), '#9a9a90'); volume(tmp, (X(56) - 13, Y(221), X(56) + 13, Y(195)), .6, .4, spec=.2)
    else: I.line(tmp, [(X(50), Y(212)), (X(80), Y(196))], '#7a7a70', 5); I.ell(tmp, (X(80) - 9, Y(196) - 9, X(80) + 9, Y(196) + 9), '#7a7a70')
    moss_on(tmp, (x - 90 * s, Y(300), x + 90 * s, Y(0)), seed + 9, .5)
    img.alpha_composite(tmp)
    return [round(ex), round(ey)]


def hk_sky():
    img = gradient(hexc('#1a2622'), hexc('#0a0f0d'))
    glow(img, 1320, 160, 420, hexc('#8a9aa0'), .22)
    rnd = random.Random(4001); d = ImageDraw.Draw(img)
    for _ in range(120):
        x, y = rnd.uniform(0, 1800), rnd.uniform(0, 420); r = rnd.choice([.7, .9, 1.2])
        d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=(210, 220, 215, int(rnd.uniform(40, 150) * (1 - y / 500))))
    img.alpha_composite(fog_layer(hexc('#4a5854'), 80, 300, .35, 4002, 380))
    P.forest_layers(img, 840, hexc('#2a3530'), [4003, 4004], [10, 8], [(620, 820), (760, 940)], [0.62, 0.4], [2.6, 1.4], pal=PAL_DARK)
    return img


def hk_trees(img):
    rnd = random.Random(4101)
    for i, x in enumerate((60, 250, 1480, 1700, 1210)):
        cedar(img, x * SS, 900 * SS, rnd.uniform(1100, 1300) * SS, rnd.uniform(260, 330) * SS, 4110 + i, PAL_DARK, (hexc('#0c0c0a'), hexc('#1a1a16'), hexc('#2e2c26')))
    for x, w in ((170, 46), (1580, 52), (1320, 30)):
        trunk(img, [(x * SS, 910 * SS), ((x + 4) * SS, -40 * SS)], [w * SS, w * .75 * SS], (hexc('#121310'), hexc('#262722'), hexc('#3e3e36')), 4120 + x, moss=hexc('#243020'))
    ground(img, 860, 930, 4130, hexc('#1c221a'), hexc('#0c0f0b'), hexc('#2c3426'), pebbles=200)
    P.bushes(img, 910, -40, 1840, 4131, PAL_DARK, 16, 50, 110)
    img = atmos(img, hexc('#2a3530'), .28)
    img.alpha_composite(fog_layer(hexc('#6a7a74'), 760, 960, .6, 4132, 260))
    return img


def hokora_building(img, cx, top_y, base_y, seed):
    """A tiny wooden hokora on a two-tier stone plinth, shimenawa across the eave."""
    I.fill(img, STONE, seed, rect=(cx - 150, base_y - 34, cx + 150, base_y), scale=6, contrast=1.3, dark=.5, light=.25); volume(img, (cx - 150, base_y - 34, cx + 150, base_y), .5, .3)
    I.fill(img, STONE, seed + 1, rect=(cx - 118, base_y - 66, cx + 118, base_y - 34), scale=6, contrast=1.3, dark=.5, light=.25); volume(img, (cx - 118, base_y - 66, cx + 118, base_y - 34), .5, .3)
    moss_on(img, (cx - 150, base_y - 66, cx + 150, base_y), seed + 2, .6)
    b0 = base_y - 66; wx0, wx1, wy0 = cx - 88, cx + 88, top_y + 120
    wood_block(img, (wx0 - 10, b0 - 20, wx1 + 10, b0), seed + 3, hexc('#3a2a1c'), hexc('#140e09'), hexc('#5a4430'))
    I.fill(img, '#4a3622', seed + 4, rect=(wx0, wy0, wx1, b0 - 20), scale=5, stretch=(.3, 4), contrast=1.1)
    for k in range(2):                                      # lattice doors with brass fittings
        dx0 = cx - 70 + k * 72; I.fill(img, '#2a1c10', seed + 5 + k, rect=(dx0, wy0 + 26, dx0 + 68, b0 - 34), scale=4)
        for gx in range(int(dx0) + 10, int(dx0) + 66, 14): I.line(img, [(gx, wy0 + 30), (gx, b0 - 38)], '#6a5236', 2.4)
        for gy in range(int(wy0) + 40, int(b0) - 34, 22): I.line(img, [(dx0 + 4, gy), (dx0 + 64, gy)], '#6a5236', 2)
        I.ell(img, (dx0 + (58 if k == 0 else 4), (wy0 + b0) / 2 - 18, dx0 + (66 if k == 0 else 12), (wy0 + b0) / 2 - 10), '#c8a050')
    lglow(img, cx, (wy0 + b0) / 2, 60, '#ffb060', .25)
    for bx in (wx0 - 8, wx1 - 6): wood_block(img, (bx, wy0, bx + 14, b0 - 20), seed + 8 + bx, hexc('#3a2a1c'), hexc('#140e09'), hexc('#5a4430'), True)
    # the roof: dark cypress bark with a mossy ridge, chigi and katsuogi on top
    roof = [(cx - 150, wy0 + 6), (cx + 150, wy0 + 6), (cx + 128, wy0 - 30), (cx + 40, top_y + 22), (cx - 40, top_y + 22), (cx - 128, wy0 - 30)]
    I.fill(img, '#2c241c', seed + 10, poly=roof, scale=4, stretch=(.3, 3), contrast=1.2); volume(img, (cx - 150, top_y + 22, cx + 150, wy0 + 6), .5, .3)
    I.fill(img, '#1a140e', seed + 11, rect=(cx - 152, wy0 + 2, cx + 152, wy0 + 12), scale=3)
    moss_on(img, (cx - 150, top_y + 20, cx + 150, wy0), seed + 12, .45)
    I.fill(img, '#3a2e22', seed + 13, rect=(cx - 46, top_y + 10, cx + 46, top_y + 26), scale=3)
    for sgn in (-1, 1): I.line(img, [(cx + sgn * 44, top_y + 22), (cx + sgn * 66, top_y - 12)], '#2a2016', 7)
    for k in (-24, 0, 24): I.fill(img, '#3a2e22', seed + 20 + k, ell=(cx + k - 9, top_y, cx + k + 9, top_y + 14), scale=2)
    # shimenawa with shide across the eave, the bell and its rope
    pts = [(cx - 104 + 208 * u, wy0 + 16 + 14 * math.sin(math.pi * u)) for u in np.linspace(0, 1, 16)]
    straw_rope(img, pts, 10, seed + 30)
    for u in (.2, .5, .8): shide(img, cx - 104 + 208 * u, wy0 + 20 + 14 * math.sin(math.pi * u), .9)
    return wy0


def hk_shrine(img):
    # the giant old cedar (goshinboku) with its own sacred rope
    tx, tb = 520, 1045
    pts = [(tx * SS, tb * SS), ((tx + 10) * SS, 700 * SS), ((tx + 4) * SS, 300 * SS), ((tx + 14) * SS, -60 * SS)]
    trunk(img, pts, [128 * SS, 104 * SS, 92 * SS, 84 * SS], (hexc('#1e1a15'), hexc('#3a322a'), hexc('#5e5446')), 4201, moss=hexc('#34442a'))
    for k, (dx, dy) in enumerate(((-150, 26), (-90, 18), (110, 22), (170, 30))):
        trunk(img, [((tx + dx * .3) * SS, (tb - 90) * SS), ((tx + dx) * SS, (tb + dy) * SS)], [40 * SS, 12 * SS], (hexc('#1e1a15'), hexc('#3a322a'), hexc('#5e5446')), 4202 + k, moss=hexc('#34442a'))
    rope_pts = [(tx - 124 + 256 * u, 610 + 34 * math.sin(math.pi * u) - 10 * u) for u in np.linspace(0, 1, 20)]
    straw_rope(img, rope_pts, 20, 4210)
    for u in (.18, .42, .66, .88): shide(img, tx - 124 + 256 * u, 616 + 34 * math.sin(math.pi * u) - 10 * u, 1.5)
    rnd = random.Random(4211); d = ImageDraw.Draw(img)
    for i in range(3):
        blobs = P.ragged([((tx + rnd.uniform(-260, 260)) * SS, (60 + i * 90) * SS, 200 * SS, 70 * SS) for _ in range(3)], rnd, 5, .7)
        P.shadow_blobs(img, blobs, PAL_DARK[0]); P.dab_mass(d, blobs, 3200, 'needle', P.PAL_CEDAR, rnd, size=(5, 11), droop=.3)
    # ground and ferns around the plinth
    gl = layer(); ground(gl, 990, 1120, 4220, hexc('#26301f'), hexc('#10150d'), hexc('#3c4a30'), pebbles=500)
    ga = np.asarray(gl, np.float32); ga[..., 3] *= np.clip((np.arange(ga.shape[0]) / SS - 990) / 50, 0, 1)[:, None]; img.alpha_composite(Image.fromarray(ga.astype(np.uint8), 'RGBA'))
    # the hokora at the top of the steps
    cx = 900; wy0 = hokora_building(img, cx, 600, 930, 4230)
    # stone steps down to the clearing, worn and mossy
    steps = [(930, 250), (970, 290), (1012, 330), (1056, 372)]
    y = 930
    for k, (yb, w) in enumerate(steps):
        I.fill(img, STONE, 4240 + k, rect=(cx - w / 2, y, cx + w / 2, yb), scale=6, contrast=1.3, dark=.5, light=.25)
        shade(img, (cx - w / 2, y, cx + w / 2, yb), 1.15, .7)
        ImageDraw.Draw(img).line([(px(cx - w / 2), px(y)), (px(cx + w / 2), px(y))], fill=(150, 150, 140, 160), width=px(2)); y = yb
    moss_on(img, (cx - 190, 930, cx + 190, 1060), 4250, .55)
    # offering stand to the right under the eave, where dishes are left
    ox, oy = 978, 930
    I.fill(img, '#b8a888', 4260, rect=(ox - 34, oy - 30, ox + 34, oy - 20), scale=3, contrast=.6)
    I.fill(img, '#9a8a6a', 4261, poly=[(ox - 26, oy - 20), (ox + 26, oy - 20), (ox + 20, oy), (ox - 20, oy)], scale=3); I.ell(img, (ox - 8, oy - 16, ox + 8, oy - 6), '#2a2016')
    P.bushes(img, 1050, 560, 760, 4270, PAL_DARK, 5, 40, 80); P.bushes(img, 1050, 1060, 1300, 4271, PAL_DARK, 5, 40, 80)
    for fxp in (700, 1110): near_fern(img, fxp, 1050, 110, 4272 + fxp, lean=.2 if fxp < 900 else -.2, pal=[hexc('#0e140e'), hexc('#1a2616'), hexc('#26361e'), hexc('#34482a'), hexc('#44583a')])
    META['hok'] = {'bell': [cx - 40, wy0 + 30], 'rope': [cx - 40, 880], 'offer': [ox, oy - 30], 'hokora': [cx - 150, 600, cx + 150, 930]}
    return img


def hk_floor(img):
    ground(img, 1100, 1400, 4301, hexc('#28301f'), hexc('#10140c'), hexc('#3e4a30'), pebbles=2600)
    n = fbm(SW, 300 * SS, 40 * SS, 4, 4302); a = np.asarray(img.crop((0, 1100 * SS, SW, 1400 * SS)), np.float32)
    m = np.clip((n - .45) * 2.5, 0, 1)[..., None] * .5; a[..., :3] = a[..., :3] * (1 - m) + np.array([54, 74, 38], np.float32) * m
    img.paste(Image.fromarray(a.astype(np.uint8), 'RGBA'), (0, 1100 * SS))
    for k, Z in enumerate((7.05, 6.3, 5.6)):                   # flat stepping stones towards the steps
        X = .22 * math.sin(k * 2.1); cx, cy = fx(X, Z), fz(Z); rw = 1.0 / (Z * T20 * ASP) * 900 * .3; rh = 2950 / Z ** 2 * .22
        pts = [(cx + math.cos(a) * rw * (1 + .12 * math.sin(a * 3 + k)), cy + math.sin(a) * rh * (1 + .15 * math.cos(a * 2 + k))) for a in np.linspace(0, math.tau, 18)]
        I.fill(img, '#5c5e56', 4310 + k, poly=pts, scale=5, contrast=1.2, dark=.45, light=.25)
        volume(img, (cx - rw, cy - rh, cx + rw, cy + rh), .4, .4)
    moss_on(img, (0, 1100, 1800, 1400), 4320, .35)
    I.soft(img, lambda d: d.rectangle([0, px(1092), px(1800), px(1112)], fill=(0, 0, 0, 90)), 6)
    lanterns = [stone_lantern(img, 330, 1104, 400, 4330), stone_lantern(img, 1470, 1104, 400, 4340)]
    eyes = [kitsune(img, 640, 1102, 300, 4350, flip=False, holds='jewel'), kitsune(img, 1160, 1102, 300, 4360, flip=True, holds='key')]
    for lx, (gx, gy) in zip((330, 1470), lanterns): lglow(img, gx, 1150, 260, '#ffa048', .22, .3)
    pal = [hexc('#0c120c'), hexc('#162214'), hexc('#20301c'), hexc('#2c4024'), hexc('#3a5230')]
    for fxp, sd in ((470, 1), (560, 2), (1260, 3), (1340, 4), (180, 5), (1620, 6)): near_fern(img, fxp, 1112, 140, 4370 + sd, lean=.3 if fxp < 900 else -.3, pal=pal)
    META['hok'].update({'eyes': eyes, 'lanterns': [[round(x), round(y)] for x, y in lanterns], 'foxes': [[560, 800, 720, 1102], [1080, 800, 1240, 1102]]})
    return img


def hk_near(img):
    near_fern(img, 400, 1440, 460, 4401, lean=.35); near_fern(img, 1420, 1440, 420, 4402, lean=-.35)
    near_branch(img, 1520, -50, 1180, 110, 4403)
    trunk(img, [(-30 * SS, 1450 * SS), (20 * SS, -60 * SS)], [70 * SS, 60 * SS], (hexc('#0a0a08'), hexc('#161612'), hexc('#262620')), 4404)
    return img


def hokora():
    P.set_size(1800, 1400)
    st = Stack('hokora')
    img = hk_sky(); img = st.cut(img, 'sky', .06)
    img = hk_trees(img); img = st.cut(img, 'trees', .22)
    img = hk_shrine(img); img = st.cut(img, 'shrine', .45)
    img = hk_floor(img); img = st.cut(img, 'floor', .8)
    img = hk_near(img)
    st.finish(img, 'near', 1.5, blur=5, lift=(6, 9, 8), sat=0.62, gamma=1.1)
    slim('hokora_trees')


def slim(name, blur=1.0, q=74):
    """Dense far foliage compresses badly: soften it a touch (it sits behind fog anyway) to stay under ~300 KB."""
    p = os.path.join(LY.OUT, name + '.webp'); im = Image.open(p).convert('RGBA')
    im.filter(ImageFilter.GaussianBlur(blur)).save(p, 'WEBP', quality=q, alpha_quality=70, method=6)


# ═════════════════════════════ DECORATIONS: ~30 per room, one atlas per room ═════════════════════════════
ROWS, IMGS = [], {}
CAT_TEA, CAT_HOK = 'Чайный домик', 'Святилище'
SLUG = {CAT_TEA: 'cha', CAT_HOK: 'hok'}


def save_it(img, iid, name, cat, anchor='b', price=60, glow=None):
    out = img.resize((P.W, P.H), Image.LANCZOS)
    a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .88
    a[..., :3] += np.random.default_rng(sum(map(ord, iid))).normal(0, 3.2, a.shape[:2])[..., None]
    IMGS.setdefault(cat, []).append((iid, Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')))
    row = {'id': iid, 'n': name, 'c': cat, 'w': P.W, 'h': P.H, 'a': anchor, 'p': price}
    if glow: row['glow'] = glow
    ROWS.append(row)


def pack():
    for cat, lst in IMGS.items():
        lst = sorted(lst, key=lambda t: -t[1].height); W = 1400; x = y = rowh = 0; pos = {}
        for iid, im in lst:
            if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
            pos[iid] = (x, y); x += im.width + 2; rowh = max(rowh, im.height)
        at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
        for iid, im in lst: at.paste(im, pos[iid])
        at.save(f'{OUTI}/atlas_{SLUG[cat]}.webp', 'WEBP', quality=86, alpha_quality=90, method=6)
        for r in ROWS:
            if r['id'] in pos: r['at'] = [SLUG[cat], pos[r['id']][0], pos[r['id']][1]]
        META.setdefault('atlas', {})[SLUG[cat]] = list(at.size)
        at.convert('RGBA').save(os.path.join(PREV, f'atlas_{SLUG[cat]}.png'))
        print('atlas', cat, at.size, len(lst))


def bowl(img, cx, top, w, h, glaze, seed, rim_in='#2a2a24'):
    g = H(glaze)
    fill(img, dk(g, .35), seed + 1, poly=[(cx - w * .2, top + h * .86), (cx + w * .2, top + h * .86), (cx + w * .18, top + h), (cx - w * .18, top + h)], scale=4)
    body = [(cx - w / 2, top), (cx + w / 2, top), (cx + w * .47, top + h * .5), (cx + w * .32, top + h * .88), (cx - w * .32, top + h * .88), (cx - w * .47, top + h * .5)]
    m = fill(img, g, seed, poly=body, scale=5, contrast=1.4, dark=.5, light=.3)
    return m


def bowl_rim(img, cx, top, w, g, inner):
    ImageDraw.Draw(img).ellipse([px(cx - w / 2), px(top - w * .1), px(cx + w / 2), px(top + w * .1)], fill=dk(H(g), .45))
    ImageDraw.Draw(img).ellipse([px(cx - w / 2 + 5), px(top - w * .1 + 3), px(cx + w / 2 - 5), px(top + w * .1 - 2)], fill=H(inner))


def matcha_foam(img, cx, top, w, seed):
    fill(img, '#7a9a3a', seed, ell=(cx - w / 2 + 6, top - w * .1 + 4, cx + w / 2 - 6, top + w * .1 - 2), scale=2, contrast=1.1, dark=.3, light=.35)
    rr = random.Random(seed); d = ImageDraw.Draw(img)
    for _ in range(40):
        x, y = cx + rr.uniform(-w * .4, w * .4), top + rr.uniform(-w * .06, w * .06); r = rr.uniform(.8, 2.2)
        d.ellipse([px(x - r), px(y - r * .6), px(x + r), px(y + r * .6)], fill=(200, 222, 150, 150))


def kakemono(iid, name, chars, frame, price, seal=True, pic=None):
    img = canvas(130, 430); fr = H(frame)
    line(img, [(35, 12), (65, 2), (95, 12)], '#1a120c', 1.4)
    fill(img, '#2a1c14', 1, rect=(12, 10, 118, 20), scale=3)
    fill(img, fr, sum(map(ord, iid)), rect=(14, 18, 116, 408), scale=6, contrast=1.1)
    fill(img, dk(fr, .25), 7, rect=(18, 70, 112, 80), scale=3); fill(img, dk(fr, .25), 8, rect=(18, 350, 112, 360), scale=3)
    fill(img, '#e6dcc4', 9, rect=(24, 86, 106, 344), scale=8, contrast=.6, dark=.12, light=.1)
    if pic: pic(img)
    n = max(1, len(chars)); sz = min(52, 230 / n)
    for k, ch in enumerate(chars): text(img, ch, 65, 86 + (258 - sz * n * 1.02) / 2 + sz * .55 + k * sz * 1.02, sz, '#1b1714', SERIF, brush=True)
    if seal: ImageDraw.Draw(img).rectangle([px(80), px(322), px(92), px(336)], fill=H('#a8302a'))
    fill(img, '#1e140e', 10, rect=(6, 404, 124, 418), scale=3)
    for x in (2, 118): fill(img, '#c8a860', 11 + x, rect=(x, 402, x + 10, 420), scale=2)
    save_it(img, iid, name, CAT_TEA, 't', price)


def camellia(img, x, y, r, seed, col='#b8202a'):
    for k in range(5):
        a = k / 5 * math.tau - .3
        fill(img, col, seed + k, ell=(x + math.cos(a) * r * .45 - r * .5, y + math.sin(a) * r * .4 - r * .42, x + math.cos(a) * r * .45 + r * .5, y + math.sin(a) * r * .4 + r * .42), scale=2, contrast=.8)
    volume(img, (x - r, y - r, x + r, y + r), .6, .4, spec=.2)
    for k in range(9): a = k / 9 * math.tau; line(img, [(x, y), (x + math.cos(a) * r * .28, y + math.sin(a) * r * .24)], '#f0d060', max(.8, r * .05))


def leaf(img, x, y, L, ang, col, seed):
    c, s = math.cos(ang), math.sin(ang)
    fill(img, col, seed, poly=[(x, y), (x + c * L * .5 - s * L * .22, y + s * L * .5 + c * L * .22), (x + c * L, y + s * L), (x + c * L * .5 + s * L * .22, y + s * L * .5 - c * L * .22)], scale=2, contrast=1.1)
    line(img, [(x, y), (x + c * L * .9, y + s * L * .9)], lt(H(col), .2), max(.6, L * .03))


def bamboo_tube(img, x0, y0, x1, y1, seed, col='#9a8a50', nodes=()):
    fill(img, col, seed, rect=(x0, y0, x1, y1), scale=3, stretch=(.3, 4), contrast=.9); volume(img, (x0, y0, x1, y1), .6, .45, spec=.25)
    for y in nodes: line(img, [(x0, y), (x1, y)], dk(H(col), .4), 2.4)


def fox_small(img, x, base, h, seed, col='#f2ece0', bib='#c02a2a', flip=False):
    s = h / 100; f = -1 if flip else 1; X = lambda v: x + f * v * s; Y = lambda v: base - v * s; c = H(col)
    blob(img, [(X(-14), Y(0)), (X(-26), Y(20)), (X(-36), Y(52)), (X(-30), Y(70)), (X(-20), Y(46)), (X(-4), Y(8))], c, seed, scale=2, k=.4)
    blob(img, [(X(-16), Y(0)), (X(-18), Y(40)), (X(-4), Y(66)), (X(12), Y(64)), (X(16), Y(30)), (X(18), Y(0))], c, seed + 1, scale=2)
    blob(img, [(X(-8), Y(62)), (X(-6), Y(80)), (X(6), Y(88)), (X(28), Y(74)), (X(30), Y(68)), (X(10), Y(58))], c, seed + 2, scale=2)
    for a, b in ((-6, 2), (4, 12)): poly(img, [(X(a - 3), Y(80)), (X(a + 2), Y(100)), (X(b + 3), Y(82))], c)
    for a in (-3, 7): line(img, [(X(a), Y(88)), (X(a + 2), Y(95))], '#c02a2a', 1.2)
    line(img, [(X(8), Y(76)), (X(16), Y(74))], '#c02a2a', 1.6)
    blob(img, [(X(-10), Y(60)), (X(16), Y(60)), (X(6), Y(40)), (X(-4), Y(42))], H(bib), seed + 3, scale=2, k=.3)


def tea_items():
    C = CAT_TEA
    # bowls
    img = canvas(170, 120); floor_shadow(img, 85, 114, 70); bowl(img, 85, 30, 150, 84, '#2a2622', 1); volume(img, (10, 30, 160, 114), .5, .35, spec=.35)
    bowl_rim(img, 85, 30, 150, '#2a2622', '#1a1a14'); matcha_foam(img, 85, 30, 150, 2)
    soft(img, lambda d: [d.ellipse([px(70 + k * 14), px(-2 + k * 4), px(96 + k * 14), px(22 + k * 4)], fill=(240, 240, 232, 40)) for k in range(2)], 5)
    save_it(img, 'ch_matcha', 'Чаван со взбитым маття', C, 'b', 60)
    img = canvas(170, 120); floor_shadow(img, 85, 114, 70); m = bowl(img, 85, 28, 152, 86, '#c89a64', 3)
    clip(img, m, lambda d: [d.line([(px(a), px(b)), (px(a + random.Random(a).uniform(-14, 14)), px(b + 12))], fill=(120, 80, 40, 150), width=px(1)) for a in range(16, 160, 9) for b in (40, 60, 80)])
    clip(img, m, lambda d: d.rectangle([px(20), px(94), px(150), px(116)], fill=(210, 190, 150, 170)))
    volume(img, (9, 28, 161, 114), .5, .35, spec=.3); bowl_rim(img, 85, 28, 152, '#c89a64', '#6a5a3a')
    save_it(img, 'ch_ido', 'Корейский чаван идо', C, 'b', 90)
    img = canvas(160, 116); floor_shadow(img, 80, 110, 66); m = bowl(img, 80, 28, 140, 82, '#a8a090', 4)
    clip(img, m, lambda d: [d.line([(px(x), px(96)), (px(x + 6), px(50)), (px(x + 14), px(40))], fill=(60, 40, 30, 220), width=px(2)) for x in (40, 58, 96, 112)])
    volume(img, (10, 28, 150, 110), .5, .35, spec=.3); bowl_rim(img, 80, 28, 140, '#a8a090', '#5a5448')
    save_it(img, 'ch_egaratsu', 'Чаван с осенними травами', C, 'b', 70)
    img = canvas(160, 116); floor_shadow(img, 80, 110, 66); m = bowl(img, 80, 28, 140, 82, '#e8dcc4', 5)
    for (a, b, r) in ((80, 70, 11), (64, 52, 5), (76, 47, 5), (88, 47, 5), (98, 54, 5)): ell(img, (a - r, b - r * .9, a + r, b + r * .9), '#7a5236')
    volume(img, (10, 28, 150, 110), .5, .35, spec=.35); bowl_rim(img, 80, 28, 140, '#e8dcc4', '#8a7a60')
    save_it(img, 'ch_pawbowl', 'Чаван с отпечатком лапки', C, 'b', 80)
    # tea caddies
    img = canvas(170, 150); floor_shadow(img, 85, 144, 76)
    fill(img, '#6a2a3a', 6, poly=[(96, 144), (164, 144), (158, 90), (140, 70), (120, 70), (102, 90)], scale=3, contrast=.8)
    clip(img, mask_poly(img, poly=[(96, 144), (164, 144), (158, 90), (140, 70), (120, 70), (102, 90)]), lambda d: [d.ellipse([px(a), px(b), px(a + 8), px(b + 8)], outline=(216, 176, 72, 200), width=px(1.2)) for a in range(104, 160, 14) for b in range(80, 140, 14)])
    line(img, [(116, 72), (144, 72)], '#d8b048', 3); volume(img, (96, 70, 164, 144), .5, .3)
    fill(img, '#4a2a18', 7, poly=[(14, 144), (86, 144), (82, 84), (66, 54), (34, 54), (18, 84)], scale=4, contrast=1.3)
    fill(img, '#2a1a0e', 8, poly=[(20, 110), (80, 110), (84, 144), (16, 144)], scale=3); volume(img, (14, 44, 86, 144), .6, .35, spec=.45)
    fill(img, '#f2ead8', 9, ell=(30, 38, 70, 54), scale=2); volume(img, (30, 38, 70, 54), .5, .3, spec=.3)
    save_it(img, 'ch_chaire', 'Чайница тяирэ в шёлковом мешочке', C, 'b', 90)
    img = canvas(130, 120); floor_shadow(img, 65, 114, 56)
    fill(img, '#16120e', 10, rect=(14, 36, 116, 112), scale=5, contrast=.6); ImageDraw.Draw(img).ellipse([px(14), px(22), px(116), px(50)], fill=H('#221a14'))
    line(img, [(14, 52), (116, 52)], '#0a0806', 2)
    for (a, b) in ((40, 76), (84, 88)):
        poly(img, [(a, b), (a + 16, b - 10), (a + 34, b - 6), (a + 16, b - 2)], '#d8b048'); line(img, [(a + 16, b - 6), (a + 20, b - 20), (a + 26, b - 24)], '#d8b048', 1.6)
    volume(img, (14, 22, 116, 112), .4, .45, spec=.5)
    save_it(img, 'ch_natsume', 'Нацумэ с золотыми журавлями', C, 'b', 110)
    # whisk and scoop
    img = canvas(110, 170); floor_shadow(img, 55, 164, 44)
    fill(img, '#f2eee4', 11, poly=[(34, 164), (76, 164), (70, 110), (40, 110)], scale=3, contrast=.4); volume(img, (34, 110, 76, 164), .5, .3, spec=.3)
    rr = random.Random(12)
    for k in range(34):
        a = -1.25 + 2.5 * k / 33; x0, y0 = 55 + math.sin(a) * 38, 70 + (1 - math.cos(a)) * 30
        line(img, [(55 + math.sin(a) * 10, 112), (x0, y0 + 10), (55 + math.sin(a) * 18, 36)], mixc(H('#d8c890'), H('#a89860'), rr.random()), 1.2)
    bamboo_tube(img, 47, 104, 63, 150, 13, '#c8b880'); ImageDraw.Draw(img).rectangle([px(45), px(106), px(65), px(112)], fill=H('#2a1a10'))
    save_it(img, 'ch_chasen', 'Бамбуковый венчик часэн', C, 'b', 40)
    img = canvas(150, 190); floor_shadow(img, 75, 184, 62)
    bamboo_tube(img, 84, 20, 120, 184, 14, '#a89458', (60, 150)); fill(img, '#e8e0cc', 15, rect=(90, 80, 114, 130), scale=2, contrast=.3); text(img, '銘', 102, 104, 16, '#1a1410', SERIF)
    line(img, [(20, 176), (86, 120), (104, 108)], '#6a5028', 4); line(img, [(98, 112), (110, 102)], '#c8a868', 5)
    save_it(img, 'ch_chashaku', 'Ложечка тясяку и её футляр', C, 'b', 50)
    # iron and bronze
    img = canvas(190, 180); floor_shadow(img, 95, 174, 84)
    fill(img, '#2a2826', 16, ell=(14, 42, 176, 172), scale=3, contrast=1.3, dark=.5, light=.35)
    clip(img, mask_poly(img, ell=(14, 42, 176, 172)), lambda d: [d.ellipse([px(a - 2.2), px(b - 2.2), px(a + 2.2), px(b + 2.2)], fill=(70, 66, 60, 230)) for a in range(22, 172, 9) for b in range(52, 150, 9) if (a // 9 + b // 9) % 2])
    volume(img, (14, 42, 176, 172), .6, .35, spec=.25)
    fill(img, '#1a1816', 17, ell=(52, 30, 138, 58), scale=3); fill(img, '#3a3430', 18, ell=(86, 18, 104, 36), scale=2)
    for x in (8, 170): ell(img, (x, 76, x + 14, 104), '#1a1816'); ImageDraw.Draw(img).arc([px(x - 4), px(64), px(x + 18), px(116)], 0, 360, fill=H('#3a3632'), width=px(3))
    save_it(img, 'ch_kama', 'Чугунный котёл кама', C, 'b', 160)
    img = canvas(230, 290); floor_shadow(img, 115, 284, 104)
    for x in (40, 176): fill(img, '#6a5a36', 19 + x, poly=[(x, 250), (x + 16, 250), (x + 14, 284), (x + 2, 284)], scale=3)
    fill(img, '#6a5a36', 21, poly=[(20, 150), (210, 150), (198, 256), (32, 256)], scale=5, contrast=1.2, dark=.45, light=.25)
    fill(img, '#4a7a62', 22, rect=(20, 150, 210, 160), scale=3, contrast=.8)
    for x in (60, 150): fill(img, '#1a120c', 23 + x, ell=(x, 190, x + 22, 222), scale=2); soft(img, lambda d, x=x: d.ellipse([px(x + 4), px(198), px(x + 18), px(216)], fill=(255, 120, 40, 200)), 2)
    volume(img, (20, 150, 210, 256), .5, .3, spec=.25)
    fill(img, '#2a2826', 25, ell=(44, 60, 186, 170), scale=3, contrast=1.3, dark=.5, light=.35); volume(img, (44, 60, 186, 170), .6, .35, spec=.25)
    fill(img, '#1a1816', 26, ell=(80, 50, 150, 72), scale=3); ell(img, (106, 40, 124, 56), '#3a3430')
    soft(img, lambda d: [d.ellipse([px(96 + k * 12), px(0 + k * 6), px(134 + k * 12), px(40 + k * 6)], fill=(236, 236, 228, 36)) for k in range(3)], 7)
    save_it(img, 'ch_furo', 'Бронзовая жаровня фуро с котлом', C, 'b', 240)
    img = canvas(140, 200); floor_shadow(img, 70, 194, 58)
    fill(img, '#e2d8c4', 27, poly=[(22, 40), (118, 40), (124, 120), (112, 190), (28, 190), (16, 120)], scale=5, contrast=1.3, dark=.3, light=.15)
    rr = random.Random(28)
    for _ in range(14): x, y = rr.uniform(26, 114), rr.uniform(50, 180); soft(img, lambda d, x=x, y=y: d.ellipse([px(x - 5), px(y - 4), px(x + 5), px(y + 4)], fill=(150, 80, 50, 180)), 1.2)
    volume(img, (16, 40, 124, 190), .55, .4, spec=.3); fill(img, '#16120e', 29, ell=(18, 26, 122, 52), scale=3); volume(img, (18, 26, 122, 52), .4, .3, spec=.5); ell(img, (62, 22, 78, 32), '#2a2016')
    save_it(img, 'ch_mizusashi', 'Кувшин для воды мидзусаси', C, 'b', 120)
    img = canvas(250, 130); floor_shadow(img, 125, 124, 110)
    bamboo_tube(img, 150, 66, 196, 124, 30, '#a89458'); ImageDraw.Draw(img).ellipse([px(150), px(58), px(196), px(74)], fill=H('#3a3018'))
    line(img, [(10, 104), (160, 66)], '#c8b070', 5); line(img, [(10, 104), (160, 66)], '#e0d0a0', 1.4)
    fill(img, '#b8a060', 31, poly=[(154, 50), (200, 50), (198, 80), (156, 80)], scale=2); ImageDraw.Draw(img).ellipse([px(154), px(44), px(200), px(58)], fill=H('#5a4a28'))
    save_it(img, 'ch_hishaku', 'Черпак хисяку на подставке', C, 'b', 60)
    img = canvas(160, 100); floor_shadow(img, 80, 94, 70)
    fill(img, '#7a5a30', 32, poly=[(12, 34), (148, 34), (136, 90), (24, 90)], scale=4, contrast=1.2); volume(img, (12, 34, 148, 90), .6, .35, spec=.35)
    ImageDraw.Draw(img).ellipse([px(12), px(24), px(148), px(46)], fill=H('#4a3418')); ImageDraw.Draw(img).ellipse([px(18), px(27), px(142), px(43)], fill=H('#2a2014'))
    save_it(img, 'ch_kensui', 'Чаша для слива кэнсуй', C, 'b', 40)
    # scrolls
    kakemono('ch_ichigo', 'Свиток «Одна встреча — одна жизнь»', '一期一会', '#3e3c2a', 130)
    kakemono('ch_hibi', 'Свиток «Каждый день — хороший день»', '日日是好日', '#2a3a44', 130)
    kakemono('ch_kissako', 'Свиток «Выпей чаю»', '喫茶去', '#4a2a22', 130)
    def moon_pic(im):
        ell(im, (44, 110, 86, 152), '#f2ead0'); ImageDraw.Draw(im).ellipse([px(44), px(110), px(86), px(152)], outline=H('#8a8070'), width=px(1))
        for k in range(3): line(im, [(28, 240 + k * 16), (102, 236 + k * 16)], '#9a948a', 1.4)
    kakemono('ch_tsuki', 'Свиток «Луна и осенние травы»', '', '#3a3a3e', 140, pic=lambda im: (moon_pic(im), [line(im, [(x, 330), (x + (x - 65) * .3, 200 + abs(x - 65))], '#3a3a30', 1.6) for x in range(36, 100, 8)]))
    # flowers
    img = canvas(120, 250); floor_shadow(img, 60, 244, 40)
    bamboo_tube(img, 38, 110, 82, 244, 33, '#9a8a50', (170, 220)); ell(img, (38, 104, 82, 116), '#18120a')
    for (a, b, c_, e) in ((58, 110, 22, 40), (62, 110, 92, 60), (60, 110, 60, 30)): line(img, [(a, b), ((a + c_) / 2 + 4, (b + e) / 2), (c_, e)], '#2a2a16', 3)
    for k, (lx, ly, ang) in enumerate(((22, 46, -2.4), (40, 70, 2.8), (92, 62, -.6), (70, 40, -1.2), (60, 86, 1.9))): leaf(img, lx, ly, 34, ang, '#1e3a22', 34 + k)
    camellia(img, 54, 34, 22, 40); fill(img, '#8a1a22', 41, ell=(84, 50, 100, 70), scale=2)
    save_it(img, 'ch_tsubaki', 'Камелия в бамбуковой вазе', C, 'b', 80)
    img = canvas(180, 250); floor_shadow(img, 90, 244, 70)
    rr = random.Random(42)
    for k in range(14): line(img, [(90 + rr.uniform(-20, 20), 140), (90 + rr.uniform(-80, 80), rr.uniform(10, 60))], '#8a8a50' if k % 2 else '#6a7a40', 1.6)
    for x, y, c in ((56, 56, '#6a5ab8'), (110, 40, '#7a6ac8'), (130, 80, '#f0e8e0'), (70, 90, '#e89ab0'), (100, 70, '#6a5ab8')):
        for k in range(5): a = k / 5 * math.tau; ell(img, (x + math.cos(a) * 6 - 6, y + math.sin(a) * 6 - 6, x + math.cos(a) * 6 + 6, y + math.sin(a) * 6 + 6), c)
        ell(img, (x - 2, y - 2, x + 2, y + 2), '#f0e0a0')
    m = fill(img, '#8a6a3a', 43, poly=[(40, 130), (140, 130), (126, 244), (54, 244)], scale=3, contrast=1.2)
    clip(img, m, lambda d: [d.line([(px(30 + k * 10), px(130)), (px(50 + k * 10 - 30), px(244))], fill=(50, 34, 16, 200), width=px(1.6)) for k in range(14)] + [d.line([(px(30 + k * 10), px(130)), (px(20 + k * 10 + 30), px(244))], fill=(170, 136, 80, 150), width=px(1.2)) for k in range(14)])
    volume(img, (40, 130, 140, 244), .5, .3); ImageDraw.Draw(img).arc([px(56), px(96), px(124), px(170)], 180, 360, fill=H('#6a4a24'), width=px(4))
    save_it(img, 'ch_kago', 'Корзинка с полевыми цветами', C, 'b', 90)
    img = canvas(110, 280); line(img, [(55, 0), (55, 40)], '#1a120c', 1.4); ell(img, (51, 36, 59, 44), '#8a7040')
    bamboo_tube(img, 36, 44, 74, 270, 44, '#9a8a50', (120, 230)); fill(img, '#18120a', 45, rect=(40, 140, 70, 190), scale=2)
    line(img, [(54, 150), (40, 120), (20, 110), (14, 150)], '#3a5a2a', 2)
    for k, (x, y) in enumerate(((16, 150), (34, 118))): fill(img, '#4a5ac0', 46 + k, ell=(x - 14, y - 12, x + 14, y + 12), scale=2); ell(img, (x - 4, y - 4, x + 4, y + 4), '#f0f0f8')
    leaf(img, 40, 128, 22, 2.6, '#2e4a26', 48); leaf(img, 24, 138, 20, 1.9, '#2e4a26', 49)
    save_it(img, 'ch_kakebana', 'Висячая ваза с вьюнком', C, 't', 70)
    # sweets
    img = canvas(190, 110); floor_shadow(img, 95, 104, 86)
    fill(img, '#1a1410', 50, ell=(8, 50, 182, 104), scale=3, contrast=.6); fill(img, '#2a2016', 51, ell=(16, 54, 174, 96), scale=3, contrast=.6); volume(img, (8, 50, 182, 104), .4, .3, spec=.3)
    for k in range(5): a = k / 5 * math.tau - .3; fill(img, '#f0b0c0', 52 + k, ell=(66 + math.cos(a) * 16 - 16, 60 + math.sin(a) * 12 - 13, 66 + math.cos(a) * 16 + 16, 60 + math.sin(a) * 12 + 13), scale=2, contrast=.5)
    ell(img, (60, 55, 72, 65), '#f6e080'); volume(img, (34, 36, 98, 86), .5, .35, spec=.3)
    fill(img, '#7a9a4a', 58, poly=[(104, 76), (124, 44), (152, 38), (150, 62), (126, 82)], scale=2, contrast=.6); line(img, [(108, 74), (148, 42)], '#5a7a34', 1.6); volume(img, (104, 38, 152, 82), .5, .3, spec=.2)
    line(img, [(40, 96), (170, 78)], '#c8a870', 2.4)
    save_it(img, 'ch_wagashi', 'Вагаси на лаковой тарелке', C, 'b', 50)
    img = canvas(180, 90); floor_shadow(img, 90, 84, 82)
    fill(img, '#1a1410', 59, poly=[(10, 50), (170, 50), (176, 80), (4, 80)], scale=3); fill(img, '#8a1a1a', 60, poly=[(12, 46), (168, 46), (170, 52), (10, 52)], scale=2); volume(img, (4, 46, 176, 80), .4, .3, spec=.3)
    for k, (x, c) in enumerate(((40, '#e8c870'), (70, '#f0e8e0'), (100, '#c85a3a'), (130, '#f0b8c8'))):
        if k == 2:
            for j in range(5): a = j / 5 * math.tau - math.pi / 2; poly(img, [(x, 40), (x + math.cos(a) * 16, 40 + math.sin(a) * 12), (x + math.cos(a + .6) * 7, 40 + math.sin(a + .6) * 5)], c)
        else:
            for j in range(8): a = j / 8 * math.tau; ell(img, (x + math.cos(a) * 9 - 6, 40 + math.sin(a) * 6 - 5, x + math.cos(a) * 9 + 6, 40 + math.sin(a) * 6 + 5), c)
            ell(img, (x - 5, 36, x + 5, 44), lt(H(c), .2))
        volume(img, (x - 18, 26, x + 18, 54), .5, .3)
    save_it(img, 'ch_higashi', 'Сухие сладости хигаси', C, 'b', 40)
    img = canvas(170, 60); floor_shadow(img, 85, 54, 76)
    fill(img, '#e8dcc0', 61, poly=[(10, 34), (150, 26), (160, 34), (150, 44), (10, 40)], scale=3, contrast=.4)
    fill(img, '#2a1a12', 62, poly=[(8, 32), (40, 30), (40, 42), (8, 42)], scale=2); ImageDraw.Draw(img).ellipse([px(12), px(33), px(18), px(39)], fill=H('#c8a050'))
    line(img, [(60, 32), (140, 28)], '#d8b048', 2); line(img, [(60, 38), (140, 38)], '#b84a3a', 1.4)
    save_it(img, 'ch_sensu', 'Чайный веер сэнсу', C, 'b', 30)
    img = canvas(300, 110); floor_shadow(img, 150, 104, 140, 80)
    fill(img, '#7a7650', 63, poly=[(40, 20), (260, 20), (296, 96), (4, 96)], scale=3, stretch=(6, .4), contrast=1.1, dark=.35, light=.2)
    clip(img, mask_poly(img, poly=[(40, 20), (260, 20), (296, 96), (4, 96)]), lambda d: [d.line([(0, px(y)), (px(300), px(y))], fill=(60, 56, 34, 120), width=px(1)) for y in range(22, 96, 4)])
    for a, b in (((40, 20), (4, 96)), ((260, 20), (296, 96))): line(img, [a, b], '#1c1812', 7)
    fill(img, '#4a4630', 64, poly=[(4, 96), (296, 96), (296, 106), (4, 106)], scale=2)
    save_it(img, 'ch_tatami', 'Половинка татами', C, 'b', 60)
    # lights
    img = canvas(130, 250); floor_shadow(img, 65, 244, 58)
    soft(img, lambda d: d.ellipse([px(0), px(40), px(130), px(220)], fill=(255, 180, 90, 60)), 14)
    for x in (18, 104): fill(img, WOOD_D, 65 + x, rect=(x, 30, x + 8, 244), scale=2)
    fill(img, '#f6d8a0', 67, rect=(24, 44, 106, 204), scale=4, contrast=.5, dark=.1, light=.2); volume(img, (24, 44, 106, 204), .3, .4)
    for y in (44, 124, 204): fill(img, WOOD_D, 68 + y, rect=(16, y - 4, 114, y + 4), scale=2)
    fill(img, WOOD_D, 71, rect=(12, 24, 118, 32), scale=2)
    save_it(img, 'ch_andon', 'Андон чайного домика', C, 'b', 100, glow=[65, 124])
    img = canvas(80, 220); floor_shadow(img, 40, 214, 30)
    fill(img, '#1a1410', 72, ell=(14, 196, 66, 216), scale=2); line(img, [(40, 204), (40, 90)], '#1a1410', 6); fill(img, '#1a1410', 73, ell=(18, 82, 62, 96), scale=2)
    fill(img, '#f2ead8', 74, rect=(32, 44, 48, 86), scale=2, contrast=.3); soft(img, lambda d: d.ellipse([px(4), px(-6), px(76), px(66)], fill=(255, 190, 100, 90)), 10)
    poly(img, [(40, 12), (48, 36), (40, 46), (32, 36)], '#ffd070'); poly(img, [(40, 24), (44, 38), (40, 44), (36, 38)], '#fff4c0')
    save_it(img, 'ch_teshoku', 'Свеча на подставке тэсёку', C, 'b', 60, glow=[40, 34])
    # furniture
    img = canvas(260, 170); floor_shadow(img, 130, 164, 124)
    for k in range(2):
        x0 = 8 + k * 122; fill(img, '#c8b890', 75 + k, rect=(x0 + 6, 20, x0 + 118, 160), scale=6, contrast=.5, dark=.2, light=.1)
        clip(img, mask_poly(img, rect=(x0 + 6, 20, x0 + 118, 160)), lambda d, x0=x0: [d.line([(px(x0 + 20 + j * 12), px(150)), (px(x0 + 30 + j * 12), px(90 - j * 6))], fill=(80, 90, 50, 180), width=px(1.4)) for j in range(8)])
        ImageDraw.Draw(img).rectangle([px(x0), px(14), px(x0 + 124), px(164)], outline=H('#1a120c'), width=px(6))
    save_it(img, 'ch_furosaki', 'Низкая ширма фуросаки', C, 'b', 140)
    img = canvas(220, 230); floor_shadow(img, 110, 224, 100)
    for x in (14, 196): fill(img, '#1a1410', 78 + x, rect=(x, 30, x + 10, 224), scale=2)
    for y in (30, 120, 210): fill(img, '#2a1e16', 80 + y, rect=(8, y, 212, y + 12), scale=3); volume(img, (8, y, 212, y + 12), .4, .3, spec=.3)
    fill(img, '#16120e', 84, rect=(40, 76, 84, 120), scale=3); ImageDraw.Draw(img).ellipse([px(40), px(68), px(84), px(84)], fill=H('#221a14')); volume(img, (40, 68, 84, 120), .4, .4, spec=.4)
    fill(img, '#e2d8c4', 85, poly=[(120, 130), (176, 130), (180, 210), (116, 210)], scale=4, contrast=1.2); volume(img, (116, 130, 180, 210), .5, .4, spec=.3); ell(img, (118, 124, 178, 138), '#16120e')
    line(img, [(110, 104), (190, 90)], '#c8b070', 3)
    save_it(img, 'ch_tana', 'Полочка для утвари', C, 'b', 160)
    img = canvas(190, 190); floor_shadow(img, 95, 184, 76)
    fill(img, '#2a2622', 86, ell=(30, 80, 160, 184), scale=3, contrast=1.3, dark=.5, light=.35)
    clip(img, mask_poly(img, ell=(30, 80, 160, 184)), lambda d: [d.ellipse([px(a - 2), px(b - 2), px(a + 2), px(b + 2)], fill=(68, 64, 58, 230)) for a in range(36, 158, 8) for b in range(88, 180, 8) if (a // 8 + b // 8) % 2])
    volume(img, (30, 80, 160, 184), .6, .35, spec=.25)
    fill(img, '#2a2622', 87, poly=[(150, 120), (184, 96), (188, 104), (158, 136)], scale=2)
    fill(img, '#1a1816', 88, ell=(66, 72, 124, 92), scale=2); ell(img, (88, 62, 102, 76), '#3a3430')
    ImageDraw.Draw(img).arc([px(40), px(10), px(150), px(130)], 190, 350, fill=H('#1a1816'), width=px(6))
    save_it(img, 'ch_tetsubin', 'Чугунный чайник тэцубин', C, 'b', 110)
    img = canvas(200, 150); floor_shadow(img, 100, 144, 90)
    m = fill(img, '#6a4a28', 89, poly=[(20, 60), (180, 60), (170, 144), (30, 144)], scale=3, contrast=1.2)
    clip(img, m, lambda d: [d.line([(px(20 + k * 8), px(60)), (px(30 + k * 8 - 10), px(144))], fill=(40, 26, 12, 200), width=px(1.4)) for k in range(22)])
    for k in range(7): x = 40 + k * 18; fill(img, '#1a1612', 90 + k, rect=(x, 40 + (k % 3) * 6, x + 16, 66), scale=2); ImageDraw.Draw(img).ellipse([px(x), px(38 + (k % 3) * 6), px(x + 16), px(46 + (k % 3) * 6)], fill=H('#3a3430'))
    fill(img, '#2a2622', 97, poly=[(150, 20), (190, 10), (196, 16), (160, 40)], scale=2); line(img, [(120, 64), (170, 24)], '#3a3632', 3)
    for k in range(6): line(img, [(26 + k * 3, 70), (6 + k * 5, 18 + k * 2)], mixc(H('#e8e0d0'), H('#5a4a38'), k / 6), 3)
    volume(img, (20, 40, 180, 144), .4, .3)
    save_it(img, 'ch_sumitori', 'Корзинка для угля с пером', C, 'b', 60)
    img = canvas(140, 90); floor_shadow(img, 70, 84, 60)
    fill(img, '#e8dcc4', 98, ell=(14, 30, 126, 86), scale=3, contrast=.8); volume(img, (14, 30, 126, 86), .5, .35, spec=.35)
    for sx in (-1, 1): poly(img, [(40 + sx * 12, 36), (40 + sx * 16, 18), (40 + sx * 4, 30)], '#e8dcc4')
    ell(img, (20, 26, 64, 60), '#e8dcc4'); volume(img, (20, 18, 64, 60), .5, .35)
    for sx in (-1, 1): line(img, [(40 + sx * 10, 44), (40 + sx * 4, 44)], '#2a2016', 1.8)
    line(img, [(110, 70), (126, 54), (120, 40)], '#e8dcc4', 6); line(img, [(60, 58), (118, 56)], '#8a7a60', 1)
    for (a, b) in ((70, 50), (92, 64), (100, 44)): ell(img, (a - 5, b - 5, a + 5, b + 5), '#c8a050')
    save_it(img, 'ch_kogo', 'Коробочка для благовоний «Кошка»', C, 'b', 70)
    img = canvas(230, 170); floor_shadow(img, 115, 164, 104)
    fill(img, '#5a5c56', 99, ell=(20, 70, 210, 166), scale=5, contrast=1.3); volume(img, (20, 70, 210, 166), .5, .35); moss_on(img, (20, 70, 210, 166), 100, .4)
    fill(img, '#1a2a2c', 101, ell=(70, 80, 160, 104), scale=3); lglow(img, 115, 92, 30, '#8ab0c8', .3, .4)
    line(img, [(44, 60), (126, 92)], '#c8b070', 3); fill(img, '#b8a060', 102, ell=(116, 84, 146, 100), scale=2)
    bamboo_tube(img, 188, 20, 204, 120, 103, '#9a8a50'); line(img, [(196, 30), (150, 50)], '#9a8a50', 6)
    save_it(img, 'ch_tsukubai', 'Каменный умывальник цукубай', C, 'b', 150)


def hok_items():
    C = CAT_HOK
    img = canvas(240, 250); floor_shadow(img, 120, 244, 110)
    for x in (54, 170): fill(img, STONE, 200 + x, rect=(x, 70, x + 18, 244), scale=4, contrast=1.3); volume(img, (x, 70, x + 18, 244), .5, .3)
    fill(img, STONE, 202, rect=(40, 90, 200, 104), scale=4); fill(img, STONE, 203, poly=[(14, 44), (226, 44), (220, 66), (20, 66)], scale=4, contrast=1.3); volume(img, (14, 44, 226, 104), .5, .3)
    fill(img, STONE, 204, rect=(112, 66, 128, 90), scale=2); moss_on(img, (10, 40, 230, 244), 205, .6)
    save_it(img, 'hk_torii_moss', 'Мшистые каменные тории', C, 'b', 150)
    img = canvas(280, 250); floor_shadow(img, 140, 244, 130)
    for k, (cx, s) in enumerate(((180, .62), (150, .8), (110, 1.0))):
        w, h = 150 * s, 200 * s; b = 244 - (2 - k) * 10
        for x in (cx - w * .36, cx + w * .36 - 12 * s): fill(img, '#c8402a', 206 + k * 5 + int(x), rect=(x, b - h, x + 12 * s, b), scale=3, contrast=.8)
        fill(img, '#1a1410', 207 + k, poly=[(cx - w * .56, b - h - 4), (cx + w * .56, b - h - 4), (cx + w * .5, b - h + 10 * s), (cx - w * .5, b - h + 10 * s)], scale=2)
        fill(img, '#c8402a', 208 + k, rect=(cx - w * .44, b - h * .82, cx + w * .44, b - h * .76), scale=2)
        for x in (cx - w * .36, cx + w * .36 - 12 * s): fill(img, '#1a1410', 209 + k + int(x), rect=(x - 1, b - 14 * s, x + 13 * s, b), scale=2)
        volume(img, (cx - w * .56, b - h - 4, cx + w * .56, b), .4, .2)
    save_it(img, 'hk_senbon', 'Коридор красных тории', C, 'b', 200)
    for iid, name, holds, sd in (('hk_fox_scroll', 'Лиса со свитком', 'scroll', 220), ('hk_fox_ine', 'Лиса с рисовым колосом', 'ine', 230)):
        img = canvas(170, 250); floor_shadow(img, 85, 244, 70)
        fill(img, STONE, sd, rect=(20, 210, 150, 244), scale=5, contrast=1.3); volume(img, (20, 210, 150, 244), .5, .3)
        fox_small(img, 80, 212, 190, sd + 1, '#8a8a80', '#b02a22', flip=holds == 'ine')
        if holds == 'scroll': fill(img, '#d8d0b8', sd + 5, rect=(98, 68, 142, 78), scale=2); ell(img, (94, 66, 102, 80), '#8a1a1a'); ell(img, (138, 66, 146, 80), '#8a1a1a')
        else:
            line(img, [(62, 80), (34, 40), (26, 14)], '#b89a4a', 2)
            for k in range(8): ell(img, (28 + k * 1.2 - 4, 14 + k * 4, 28 + k * 1.2 + 4, 22 + k * 4), '#d8b048')
        moss_on(img, (10, 10, 160, 244), sd + 6, .4)
        save_it(img, iid, name, C, 'b', 150)
    img = canvas(200, 130); floor_shadow(img, 100, 124, 90)
    for k, (x, h, fl) in enumerate(((50, 90, False), (100, 110, False), (150, 80, True))): fox_small(img, x, 124, h, 240 + k * 5, flip=fl)
    save_it(img, 'hk_fox_small', 'Фарфоровые лисички', C, 'b', 70)
    img = canvas(250, 220); floor_shadow(img, 125, 214, 114)
    for x in (16, 222): fill(img, WOOD_D, 250 + x, rect=(x, 30, x + 12, 214), scale=2)
    fill(img, '#3a2a1c', 252, poly=[(4, 20), (246, 20), (240, 36), (10, 36)], scale=3)
    for row, y in enumerate((50, 128)):
        for k in range(4):
            x = 44 + k * 52 + (row * 10); line(img, [(x, y - 6), (x, y)], '#c02a2a', 1.4)
            poly(img, [(x - 22, y + 4), (x - 14, y - 10), (x - 6, y + 4), (x + 6, y + 4), (x + 14, y - 10), (x + 22, y + 4), (x + 20, y + 34), (x, y + 58), (x - 20, y + 34)], '#e6d6b0')
            for sx in (-1, 1): line(img, [(x + sx * 4, y + 22), (x + sx * 14, y + 18)], '#c02a2a', 2)
            text(img, '願い'[k % 2], x, y + 40, 10, '#1a1410', SERIF)
        line(img, [(20, y - 6), (230, y - 6)], '#6a4a2a', 2)
    save_it(img, 'hk_ema_fox', 'Стойка с лисьими эма', C, 'b', 70)
    img = canvas(130, 120); line(img, [(65, 0), (65, 14)], '#c02a2a', 1.6)
    fill(img, '#d8c49a', 256, poly=[(8, 40), (65, 12), (122, 40), (122, 116), (8, 116)], scale=4, contrast=.5); volume(img, (8, 12, 122, 116), .3, .2)
    ell(img, (42, 64, 88, 104), '#e0a060'); ell(img, (48, 44, 82, 76), '#e0a060')
    for sx in (-1, 1): poly(img, [(65 + sx * 14, 52), (65 + sx * 16, 34), (65 + sx * 4, 48)], '#e0a060')
    for sx in (-1, 1): ell(img, (65 + sx * 8 - 3, 56, 65 + sx * 8 + 3, 62), '#1a1410')
    text(img, '猫', 104, 60, 14, '#a82a22', SERIF)
    save_it(img, 'hk_ema_cat', 'Эма с котёнком', C, 't', 40)
    img = canvas(170, 250); floor_shadow(img, 85, 244, 60)
    line(img, [(85, 244), (84, 150), (60, 90), (40, 60)], '#3a2a1c', 8); line(img, [(84, 150), (120, 100), (140, 60)], '#3a2a1c', 6); line(img, [(84, 150), (90, 70), (96, 30)], '#3a2a1c', 5)
    rr = random.Random(260)
    for _ in range(26):
        x, y = rr.uniform(30, 150), rr.uniform(26, 150); poly(img, [(x - 6, y - 3), (x + 6, y - 3), (x + 4, y + 3), (x - 4, y + 3)], '#f2eee4'); line(img, [(x, y - 3), (x + rr.uniform(-2, 2), y + 12)], '#e8e2d4', 2)
    save_it(img, 'hk_omikuji_tree', 'Деревце с омикудзи', C, 'b', 90)
    img = canvas(210, 160); floor_shadow(img, 105, 154, 96)
    fill(img, '#4a3422', 262, poly=[(14, 60), (196, 60), (186, 154), (24, 154)], scale=4, stretch=(4, .5), contrast=1.2); volume(img, (14, 60, 196, 154), .4, .3)
    for k in range(9): fill(img, '#2a1c10', 263 + k, rect=(24 + k * 20, 62, 34 + k * 20, 76), scale=2)
    fill(img, '#3a2818', 273, rect=(8, 48, 202, 62), scale=3)
    ell(img, (88, 96, 122, 130), '#c8a050'); fox_small(img, 105, 128, 30, 274, '#2a1c10', '#2a1c10')
    text(img, '奉納', 105, 146, 12, '#e8d8b0', SERIF)
    save_it(img, 'hk_saisen', 'Ящик для подношений с лисьим гербом', C, 'b', 80)
    img = canvas(110, 250); floor_shadow(img, 55, 244, 40)
    fill(img, '#3a2a1c', 280, rect=(30, 200, 80, 244), scale=3); fill(img, '#3a2a1c', 281, rect=(22, 190, 88, 202), scale=3)
    line(img, [(55, 190), (55, 30)], '#c8a868', 4)
    for sx in (-1, 1):
        pts = [(55, 40), (55 + sx * 22, 58), (55 + sx * 8, 76), (55 + sx * 30, 98), (55 + sx * 12, 118), (55 + sx * 36, 142)]
        for (a, b), (c_, e) in zip(pts, pts[1:]): poly(img, [(a - 5, b), (a + 5, b), (c_ + 5, e), (c_ - 5, e)], '#e8c060')
    volume(img, (10, 30, 100, 150), .4, .2, spec=.3)
    save_it(img, 'hk_gohei_gold', 'Золотой жезл гохэй', C, 'b', 70)
    img = canvas(150, 260); stone_lantern(img, 75, 256, 250, 290)
    save_it(img, 'hk_toro', 'Мшистый каменный фонарь', C, 'b', 170, glow=[75, 110])
    img = canvas(100, 290)
    for k in range(40):
        y = 60 + k * 5.6; line(img, [(50 + 6 * math.sin(k), y), (50 - 6 * math.sin(k), y + 6)], '#c02a2a' if k % 2 else '#f2eee4', 6)
    for k in range(3): x = 30 + k * 20; fill(img, '#d8b048', 300 + k, ell=(x - 16, 16 + (k % 2) * 8, x + 16, 48 + (k % 2) * 8), scale=2); volume(img, (x - 16, 16, x + 16, 56), .6, .4, spec=.5); line(img, [(x - 8, 40 + (k % 2) * 8), (x + 8, 40 + (k % 2) * 8)], '#6a4a18', 2)
    line(img, [(50, 0), (50, 20)], '#3a2a1c', 3)
    for k in range(3): poly(img, [(40 + k * 10, 280), (44 + k * 10, 290), (36 + k * 10, 290)], '#c02a2a')
    save_it(img, 'hk_suzu', 'Бубенцы судзу на шнуре', C, 't', 90)
    img = canvas(140, 150); floor_shadow(img, 70, 144, 60)
    fill(img, '#c8b890', 310, rect=(10, 124, 130, 144), scale=3)
    for x in (42, 98):
        fill(img, '#f2eee4', 311 + x, poly=[(x - 10, 50), (x + 10, 50), (x + 22, 90), (x + 18, 124), (x - 18, 124), (x - 22, 90)], scale=3, contrast=.5); volume(img, (x - 22, 50, x + 22, 124), .5, .35, spec=.35)
        fill(img, '#f8f4ea', 313 + x, poly=[(x - 14, 34), (x + 14, 34), (x + 10, 54), (x - 10, 54)], scale=2); line(img, [(x - 12, 52), (x + 12, 52)], '#c02a2a', 2)
        for k in range(3): line(img, [(x - 6 + k * 6, 26), (x - 4 + k * 6, 36)], '#d8d0c0', 1.6)
    save_it(img, 'hk_heishi', 'Кувшинчики сакэ хэйси', C, 'b', 50)
    img = canvas(170, 180); floor_shadow(img, 85, 174, 74)
    fill(img, '#d8c49a', 320, poly=[(30, 110), (140, 110), (130, 174), (40, 174)], scale=4, contrast=.6); ell(img, (72, 128, 98, 154), '#2a2016')
    fill(img, '#e8d8b0', 321, rect=(18, 96, 152, 112), scale=3); volume(img, (18, 96, 152, 174), .4, .3)
    fill(img, '#f4f0e6', 322, ell=(36, 56, 134, 100), scale=3, contrast=.3); fill(img, '#f4f0e6', 323, ell=(50, 26, 120, 64), scale=3, contrast=.3); volume(img, (36, 26, 134, 100), .5, .35, spec=.3)
    fill(img, '#e8a030', 324, ell=(70, 8, 100, 34), scale=2); leaf(img, 86, 12, 20, -.6, '#3a6a2a', 325)
    fill(img, '#f2eee4', 326, poly=[(24, 94), (60, 84), (60, 100)], scale=2); fill(img, '#c02a2a', 327, poly=[(110, 84), (146, 94), (110, 100)], scale=2)
    save_it(img, 'hk_mochi', 'Моти-подношение на подставке', C, 'b', 60)
    img = canvas(130, 180); line(img, [(30, 0), (65, 30), (100, 0)], '#c02a2a', 2)
    fill(img, '#f2ece0', 330, poly=[(20, 40), (110, 40), (104, 110), (65, 170), (26, 110)], scale=3, contrast=.4)
    for sx in (-1, 1): poly(img, [(65 + sx * 28, 44), (65 + sx * 44, 4), (65 + sx * 48, 58)], '#f2ece0'); poly(img, [(65 + sx * 32, 40), (65 + sx * 42, 16), (65 + sx * 42, 48)], '#c02a2a')
    for sx in (-1, 1): line(img, [(65 + sx * 12, 86), (65 + sx * 36, 74)], '#c02a2a', 4); line(img, [(65 + sx * 8, 90), (65 + sx * 26, 84)], '#1a1410', 2)
    line(img, [(65, 30), (65, 60)], '#d8b048', 3); ell(img, (60, 154, 70, 164), '#1a1410'); volume(img, (20, 4, 110, 170), .45, .3, spec=.2)
    save_it(img, 'hk_kitsune_mask', 'Маска лисы-невесты', C, 't', 70)
    img = canvas(260, 190); floor_shadow(img, 130, 184, 120)
    fill(img, '#5a5c56', 340, ell=(60, 110, 230, 184), scale=5, contrast=1.3); volume(img, (60, 110, 230, 184), .5, .35); moss_on(img, (60, 110, 230, 184), 341, .5)
    fill(img, '#1a2a2c', 342, ell=(92, 118, 200, 140), scale=3); lglow(img, 146, 128, 40, '#8ab0c8', .3, .4)
    bamboo_tube(img, 20, 30, 38, 184, 343, '#8a9a50'); bamboo_tube(img, 20, 34, 150, 50, 344, '#8a9a50')
    line(img, [(150, 50), (150, 60), (148, 122)], '#b8d8e8', 3); line(img, [(150, 50), (150, 122)], '#e8f4f8', 1)
    save_it(img, 'hk_kakehi', 'Бамбуковый жёлоб с водой', C, 'b', 120)
    img = canvas(150, 250); floor_shadow(img, 75, 244, 50)
    cedar(img, 75 * SS, 220 * SS, 200 * SS, 110 * SS, 350, P.PAL_CEDAR, P.BARK)
    fill(img, '#5a5c56', 351, ell=(30, 214, 120, 244), scale=3); straw_rope(img, [(52, 196), (75, 202), (98, 196)], 5, 352); shide(img, 75, 200, .5)
    save_it(img, 'hk_sugi', 'Саженец криптомерии', C, 'b', 70)
    img = canvas(220, 110); floor_shadow(img, 110, 104, 104)
    for k, (x, y, w, h) in enumerate(((20, 40, 90, 64), (90, 20, 100, 84), (160, 60, 56, 44))):
        fill(img, STONE, 360 + k, ell=(x, y, x + w, y + h), scale=4, contrast=1.3); volume(img, (x, y, x + w, y + h), .5, .4)
    moss_on(img, (10, 10, 220, 110), 364, .75)
    save_it(img, 'hk_moss', 'Мшистые камни', C, 'b', 50)
    img = canvas(230, 190); floor_shadow(img, 115, 184, 104)
    blob(img, [(20, 184), (14, 120), (50, 50), (120, 26), (190, 60), (216, 130), (210, 184)], H('#56584f'), 370, scale=6); moss_on(img, (10, 20, 220, 184), 371, .5)
    straw_rope(img, [(22, 110), (80, 128), (150, 126), (212, 104)], 10, 372)
    for x in (70, 130, 180): shide(img, x, 126 - (x - 115) ** 2 / 400, .8)
    save_it(img, 'hk_iwakura', 'Священный камень ивакура', C, 'b', 130)
    img = canvas(200, 250); floor_shadow(img, 100, 244, 90)
    fill(img, STONE, 380, rect=(20, 210, 180, 244), scale=4); volume(img, (20, 210, 180, 244), .5, .3)
    fill(img, '#4a3622', 381, rect=(46, 110, 154, 210), scale=4, stretch=(.3, 4)); fill(img, '#2a1c10', 382, rect=(66, 128, 134, 200), scale=3)
    for gx in range(72, 132, 10): line(img, [(gx, 132), (gx, 196)], '#6a5236', 1.6)
    fill(img, '#2c241c', 383, poly=[(24, 114), (176, 114), (150, 70), (50, 70)], scale=3); volume(img, (24, 70, 176, 114), .5, .3); moss_on(img, (24, 60, 176, 114), 384, .5)
    for sgn in (-1, 1): line(img, [(100 + sgn * 26, 72), (100 + sgn * 42, 50)], '#2a2016', 4)
    straw_rope(img, [(46, 120), (100, 132), (154, 120)], 5, 385); shide(img, 100, 130, .5)
    save_it(img, 'hk_minihokora', 'Маленькая хокора', C, 'b', 180)
    img = canvas(160, 90); floor_shadow(img, 80, 84, 72); plate(img, 80, 62, 144, '#e9e4d8', '#8a2a22')
    for k, (x, y) in enumerate(((56, 48), (100, 44), (80, 58))): fill(img, '#c8883a', 390 + k, poly=[(x - 26, y - 10), (x + 26, y - 14), (x + 28, y + 6), (x - 24, y + 10)], scale=2, contrast=1.2); volume(img, (x - 26, y - 14, x + 28, y + 10), .5, .3, spec=.3)
    save_it(img, 'hk_aburaage', 'Абураагэ для лисы', C, 'b', 30)
    img = canvas(180, 100); floor_shadow(img, 90, 94, 82)
    fill(img, '#1a1410', 395, poly=[(10, 60), (170, 60), (176, 94), (4, 94)], scale=3); fill(img, '#8a1a1a', 396, rect=(8, 56, 172, 62), scale=2)
    for k in range(3):
        x = 40 + k * 50; fill(img, '#b87a36', 397 + k, poly=[(x - 22, 58), (x + 22, 58), (x + 18, 26), (x, 18), (x - 18, 26)], scale=2, contrast=1.1); volume(img, (x - 22, 18, x + 22, 58), .5, .35, spec=.3)
        for j in range(4): ell(img, (x - 10 + j * 5, 20 + j % 2 * 3, x - 6 + j * 5, 24 + j % 2 * 3), '#f2eee4')
    save_it(img, 'hk_inari', 'Инари-суси на подносе', C, 'b', 40)
    img = canvas(120, 300); line(img, [(60, 0), (60, 290)], '#e8e0cc', 1.2)
    cols = ['#c02a2a', '#e8c040', '#2a6ab0', '#e87aa0', '#3a8a4a', '#f2eee4', '#8a4ab0']
    for k in range(12):
        y = 14 + k * 23; c = cols[k % len(cols)]; poly(img, [(60, y), (44, y + 12), (60, y + 8), (76, y + 12)], c); poly(img, [(60, y + 8), (54, y + 18), (66, y + 18)], dk(H(c), .2))
    for k in range(9): line(img, [(60, 290), (48 + k * 3, 300)], cols[k % len(cols)], 2)
    save_it(img, 'hk_senbazuru', 'Гирлянда бумажных журавликов', C, 't', 60)
    img = canvas(70, 200); line(img, [(35, 0), (35, 10)], '#c02a2a', 1.6)
    fill(img, '#f2eee4', 400, poly=[(12, 30), (35, 10), (58, 30), (58, 196), (12, 196)], scale=3, contrast=.3)
    for k, ch in enumerate('稲荷大神'): text(img, ch, 35, 50 + k * 34, 26, '#1a1410', SERIF, brush=True)
    ImageDraw.Draw(img).rectangle([px(26), px(172), px(44), px(188)], fill=H('#a82a22'))
    save_it(img, 'hk_ofuda', 'Талисман офуда', C, 't', 30)
    img = canvas(200, 290); floor_shadow(img, 100, 284, 90)
    for k, x in enumerate((40, 110, 170)):
        line(img, [(x, 284), (x, 20)], '#2a2016', 4); line(img, [(x, 24), (x + 36, 24)], '#2a2016', 3)
        fill(img, '#c83a2a', 410 + k, rect=(x + 2, 26, x + 36, 240 - k * 16), scale=4, stretch=(.4, 3), contrast=.7)
        for j, ch in enumerate('稲荷'): text(img, ch, x + 19, 70 + j * 44, 24, '#f2eee4', SERIF)
    save_it(img, 'hk_nobori', 'Красные флажки Инари', C, 'b', 70)
    img = canvas(200, 170); floor_shadow(img, 100, 164, 90)
    fill(img, STONE, 420, ell=(100, 100, 190, 164), scale=4, contrast=1.3); volume(img, (100, 100, 190, 164), .5, .4); moss_on(img, (100, 100, 190, 164), 421, .6)
    near_fern(img, 70, 166, 150, 422, lean=-.1, pal=[hexc('#1a2a16'), hexc('#2a4020'), hexc('#3a5a2a'), hexc('#4e7236'), hexc('#628a44')])
    save_it(img, 'hk_fern', 'Папоротник у камня', C, 'b', 30)
    img = canvas(110, 200); line(img, [(55, 0), (55, 30)], '#1a120c', 2)
    soft(img, lambda d: d.ellipse([px(0), px(40), px(110), px(190)], fill=(255, 170, 80, 70)), 12)
    m = fill(img, '#f2e4c4', 430, ell=(12, 44, 98, 178), scale=4, contrast=.5)
    clip(img, m, lambda d: [d.line([(0, px(44 + 134 * k / 9)), (px(110), px(44 + 134 * k / 9))], fill=(120, 90, 50, 140), width=px(1.3)) for k in range(1, 9)])
    fox_small(img, 55, 138, 60, 431, '#b02a22', '#b02a22'); volume(img, (12, 44, 98, 178), .5, .45)
    for y in (30, 176): fill(img, '#1a120c', 432 + y, rect=(30, y, 80, y + 12), scale=2)
    save_it(img, 'hk_lantern_fox', 'Фонарь с лисьим гербом', C, 't', 60, glow=[55, 110])
    img = canvas(300, 150); floor_shadow(img, 150, 144, 140)
    fill(img, '#3a2e22', 440, rect=(6, 126, 294, 144), scale=3)
    for k, (x, h) in enumerate(((40, 70), (86, 74), (140, 90), (200, 74), (250, 70))): fox_small(img, x, 128, h, 441 + k, '#f2ece0', '#f2eee4' if k == 2 else '#c02a2a')
    line(img, [(140, 40), (140, 70)], '#2a1a12', 2); ImageDraw.Draw(img).pieslice([px(106), px(10), px(174), px(60)], 180, 360, fill=H('#c02a2a'))
    for x in (20, 280): lglow(img, x, 100, 20, '#6ad0ff', .6)
    save_it(img, 'hk_yomeiri', 'Фигурки «Лисья свадьба»', C, 'b', 190)
    img = canvas(140, 230); floor_shadow(img, 70, 224, 50)
    fill(img, '#3a2a1c', 450, rect=(40, 190, 100, 224), scale=3); line(img, [(70, 190), (70, 110)], '#b89a5a', 5)
    for k, y in enumerate((50, 70, 90)):
        for j in range(3 + k): x = 70 + (j - (2 + k) / 2) * 14; fill(img, '#d8b048', 451 + k * 5 + j, ell=(x - 7, y - 7, x + 7, y + 7), scale=1); volume(img, (x - 7, y - 7, x + 7, y + 7), .6, .4, spec=.5)
    line(img, [(70, 40), (70, 110)], '#b89a5a', 3)
    for k, c in enumerate(('#c02a2a', '#f2eee4', '#2a6ab0', '#e8c040', '#3a8a4a')): line(img, [(70, 110), (40 + k * 15 + 6 * math.sin(k), 180 + (k % 2) * 16)], c, 4)
    save_it(img, 'hk_kagura', 'Бубенцы кагура с лентами', C, 'b', 80)
    img = canvas(190, 120); floor_shadow(img, 95, 114, 86)
    fill(img, '#d8c49a', 460, rect=(10, 84, 180, 114), scale=3); fill(img, '#e8d8b0', 461, rect=(4, 76, 186, 86), scale=2); volume(img, (4, 76, 186, 114), .4, .3)
    for k, (x, c) in enumerate(((44, '#f4f0e6'), (95, '#f8f8f4'), (146, '#c8d8e0'))):
        fill(img, '#e8e4d8', 462 + k, ell=(x - 26, 58, x + 26, 80), scale=2); volume(img, (x - 26, 58, x + 26, 80), .5, .3, spec=.3)
        if k == 0: fill(img, c, 465, ell=(x - 20, 36, x + 20, 70), scale=1, contrast=.2)
        elif k == 1: fill(img, c, 466, poly=[(x - 18, 68), (x + 18, 68), (x, 34)], scale=1, contrast=.2)
        else: fill(img, '#b8d0dc', 467, ell=(x - 20, 60, x + 20, 72), scale=1)
    text(img, '米', 44, 58, 12, '#8a8070', SERIF); text(img, '塩', 95, 58, 12, '#8a8070', SERIF)
    save_it(img, 'hk_shinsen', 'Рис, соль и вода для ками', C, 'b', 40)
    img = canvas(120, 150); floor_shadow(img, 60, 144, 50)
    fill(img, '#c8b890', 470, rect=(20, 120, 100, 144), scale=2)
    for k in range(9): a = k / 9 * math.pi; ell(img, (60 + math.cos(a) * 30 - 16, 90 - math.sin(a) * 34 - 14, 60 + math.cos(a) * 30 + 16, 90 - math.sin(a) * 34 + 14), ['#c02a2a', '#f2eee4', '#e8c040'][k % 3])
    fill(img, '#e8d8b0', 471, ell=(26, 72, 94, 122), scale=2); text(img, '祭', 60, 98, 22, '#a82a22', SERIF)
    save_it(img, 'hk_kusudama', 'Бумажный шар кусудама', C, 'b', 50)


def build_items():
    tea_items(); hok_items(); pack()
    P.set_size(1800, 1400)
    return ROWS


if __name__ == '__main__':
    what = sys.argv[2:] or ['chashitsu', 'hokora', 'items']
    old = json.load(open(os.path.join(HERE, 'rooms2.json'))) if os.path.exists(os.path.join(HERE, 'rooms2.json')) else {}
    META.update(old.get('meta', {}))
    if 'chashitsu' in what: chashitsu()
    if 'hokora' in what: hokora()
    for n in ('chashitsu', 'hokora'):
        p = os.path.join(LY.OUT, f'preview-{n}.jpg')
        if os.path.exists(p): shutil.move(p, os.path.join(PREV, f'preview-{n}.jpg'))
    rows = old.get('items', [])
    if 'items' in what:
        rows = build_items()
    json.dump({'meta': META, 'items': rows}, open(os.path.join(HERE, 'rooms2.json'), 'w'), ensure_ascii=False, indent=0)
    print(json.dumps(META))
