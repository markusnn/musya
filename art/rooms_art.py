#!/usr/bin/env python3
"""«Дом открывается постепенно»: two rooms that open later — the attic (屋根裏) and the storehouse (蔵 kura) —
painted as depth layers like layers.py / matsuri.py, plus ~30 decorations per room packed into one atlas each,
and a sheet of boards / padlock / cobweb for the locked-room preview.
Usage: cd art && python3 rooms_art.py ../assets/layers
  → assets/layers/{attic,kura}_{wall,floor,near}.webp, assets/items/atlas_{att,kra}.webp, assets/layers/ro_boards.webp,
    art/rooms_art.json (item rows + sprite rects, pasted into feat/rooms.js); previews → art/out/"""
import json, math, os, random, shutil, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc, fbm, textured_fill, layer, gradient, glow, wood_block, SS
import layers as LY
from layers import Stack, near_foliage
import items as I
from items import px, canvas, fill, volume, soft, floor_shadow, line, ell, poly, text, H, dk, lt, SERIF
import room_items as RI
from room_items import clip, barrel, crock, rope, blob

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
ITEMS_DIR = os.path.join(HERE, '..', 'assets', 'items')
PREV = os.path.join(HERE, 'out')
VPX, VPY = 900, 700                      # vanishing point of the home camera (horizon at y=700)
FL = 1140                                # floor line of both rooms (L3 g)
SW, SH = 1800 * SS, 1400 * SS


def vp_scale(p, s): return (VPX + (p[0] - VPX) * s, VPY + (p[1] - VPY) * s)


def persp_floor(img, y0, seed, base, dark, light, pw=.3, L=.6, far=.62):
    """Planks running into the depth: seams converge to the vanishing point, butt joints lie at constant depth."""
    ys = (np.arange(y0 * SS, SH) + .5) / SS; xs = (np.arange(SW) + .5) / SS
    X, Y = np.meshgrid(xs, ys); dy = Y - VPY; u = (X - VPX) / dy; z = 440 / dy
    q = u / pw; p = np.floor(q); f = q - p; pi = (p.astype(int) + 64) % 128
    rng = np.random.default_rng(seed); tone = rng.uniform(.8, 1.1, 128); off = rng.uniform(0, L, 128)
    N = fbm(512, 512, 40, 4, seed)
    n = N[((z * 380).astype(int)) % 512, ((u + 4) * 90).astype(int) % 512]
    v = np.clip(.5 * n + .5 * (np.sin(u * 160 + n * 9) * .5 + .5), 0, 1)[..., None]
    b, d, l = (np.array(H(c)[:3], np.float32) for c in (base, dark, light))
    rgb = np.where(v < .5, d + (b - d) * v / .5, b + (l - b) * (v - .5) / .5) * tone[pi][..., None]
    wpx = pw * dy                                                    # plank width in px at this row
    rgb[(f * wpx < 1.7) | ((1 - f) * wpx < .8)] *= .3                # seams
    jz = ((z + off[pi]) / L) % 1 * L; rgb[jz < 1.6 * 440 / dy ** 2] *= .35   # butt joints
    rgb[(f * wpx > 1.7) & (f * wpx < 3.2)] *= 1.12                   # worn edge
    rgb *= (far + (1.05 - far) * np.clip((Y - y0) / (1400 - y0), 0, 1))[..., None]
    img.alpha_composite(Image.fromarray(np.dstack([np.clip(rgb, 0, 255), np.full(X.shape, 255)]).astype(np.uint8), 'RGBA'), (0, y0 * SS))


def specks(img, box, n, col, seed, r=(1, 2.4), a=(40, 120)):
    rr = random.Random(seed); d = ImageDraw.Draw(img); x0, y0, x1, y1 = box
    for _ in range(n):
        x, y, s = rr.uniform(x0, x1), rr.uniform(y0, y1), rr.uniform(*r)
        d.ellipse([px(x - s), px(y - s), px(x + s), px(y + s)], fill=H(col)[:3] + (int(rr.uniform(*a)),))


def straws(img, box, n, seed, cols=('#8a7446', '#6a5632', '#a88e58'), L=(8, 26), a=(90, 200)):
    rr = random.Random(seed); d = ImageDraw.Draw(img); x0, y0, x1, y1 = box
    for _ in range(n):
        x, y = rr.uniform(x0, x1), rr.uniform(y0, y1); ang = rr.uniform(0, math.pi); ll = rr.uniform(*L)
        d.line([(px(x), px(y)), (px(x + math.cos(ang) * ll), px(y + math.sin(ang) * ll * .45))], fill=H(rr.choice(cols))[:3] + (int(rr.uniform(*a)),), width=px(1.2))


def cobweb(img, cx, cy, R, a0, a1, seed, alpha=80):
    """Corner cobweb: radial threads between two angles and sagging rings."""
    rr = random.Random(seed); l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    rays = [a0 + (a1 - a0) * k / 7 + rr.uniform(-.05, .05) for k in range(8)]
    col = (205, 200, 185, alpha)
    for a in rays: d.line([(px(cx), px(cy)), (px(cx + math.cos(a) * R), px(cy + math.sin(a) * R))], fill=col, width=px(.9))
    for k in range(1, 9):
        r = R * k / 9 * rr.uniform(.9, 1.05); pts = []
        for i, a in enumerate(rays):
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
            if i < len(rays) - 1:
                am = (a + rays[i + 1]) / 2; rm = r * .88; pts.append((cx + math.cos(am) * rm, cy + math.sin(am) * rm))
        d.line([(px(x), px(y)) for x, y in pts], fill=col[:3] + (int(alpha * .8),), width=px(.8))
    img.alpha_composite(l.filter(ImageFilter.GaussianBlur(.35 * SS)))


def light_wedge(img, pts, col, a_top, a_bot, blur=18):
    """A soft shaft of light: polygon with a vertical alpha ramp."""
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).polygon([(px(x), px(y)) for x, y in pts], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(blur * SS)); ys = [p[1] for p in pts]
    ramp = np.clip((np.arange(img.height)[:, None] / SS - min(ys)) / (max(ys) - min(ys) + 1e-6), 0, 1)
    a = np.asarray(m, np.float32) / 255 * (a_top + (a_bot - a_top) * ramp)
    g = Image.new('RGBA', img.size, H(col)); g.putalpha(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))); img.alpha_composite(g)


def dust_on(img, box, seed, a=70):
    """Grey dust settled on the top of furniture."""
    x0, y0, x1, y1 = box; m = I.mask_poly(img, rect=box); tmp = Image.new('RGBA', img.size, (0, 0, 0, 0))
    fill(tmp, '#8a8474', seed, mask=m, scale=3, contrast=1.6); t = np.asarray(tmp, np.float32); t[..., 3] *= a / 255
    img.alpha_composite(Image.fromarray(t.astype(np.uint8), 'RGBA'))


def falloff(img, cx, cy, r, k0):
    """Light that dies away from a lamp: multiply by a radial ramp and warm the lit part slightly."""
    yy, xx = np.mgrid[0:SH // 4, 0:SW // 4]; d = np.clip(np.hypot(xx * 4 / SS - cx, yy * 4 / SS - cy) / r, 0, 1)
    k = Image.fromarray(((k0 + (1 - k0) * (1 - d) ** 1.4) * 255).astype(np.uint8)).resize(img.size, Image.BICUBIC)
    a = np.asarray(img, np.float32); kk = np.asarray(k, np.float32)[..., None] / 255
    a[..., :3] *= kk * np.array([1.04, 1.0, .9]) + (1 - kk) * np.array([.9, .95, 1.05]); img.paste(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA'))


def ramp_shade(img, box, k0, k1):
    x0, y0, x1, y1 = (max(0, px(v)) for v in box); x1 = min(x1, img.width); y1 = min(y1, img.height)
    reg = np.asarray(img.crop((x0, y0, x1, y1)), np.float32); reg[..., :3] *= np.linspace(k0, k1, reg.shape[0])[:, None, None]
    img.paste(Image.fromarray(np.clip(reg, 0, 255).astype(np.uint8), 'RGBA'), (x0, y0))


def log_beam(img, x0, x1, yc, bow, half, seed, col=('#120c08', '#2a1e14', '#4a3826')):
    pts = [(px(x0 + (x1 - x0) * k / 12), px(yc - bow * math.sin(math.pi * k / 12))) for k in range(13)]
    P.trunk(img, pts, [px(half * (1 + .12 * math.sin(k * 1.7))) for k in range(13)], tuple(hexc(c) for c in col), seed)


# ───────────────────────── furniture painted straight into the room ─────────────────────────
def chest(img, x0, y0, x1, y1, seed, col='#3a281a', metal='#1a1614', lid=26, dusty=True):
    fill(img, col, seed, rect=(x0, y0 + lid, x1, y1), scale=10, stretch=(4, .4), contrast=1.1)
    fill(img, dk(H(col), .1), seed + 1, rect=(x0 - 6, y0, x1 + 6, y0 + lid), scale=10, stretch=(4, .4))
    volume(img, (x0, y0, x1, y1), .4, .25)
    d = ImageDraw.Draw(img)
    for x in (x0, x1 - 26):
        d.rectangle([px(x), px(y0 + lid), px(x + 26), px(y0 + lid + 24)], fill=H(metal)); d.rectangle([px(x), px(y1 - 24), px(x + 26), px(y1)], fill=H(metal))
    cx = (x0 + x1) / 2; d.rectangle([px(cx - 20), px(y0 + lid - 4), px(cx + 20), px(y0 + lid + 30)], fill=H(metal))
    d.ellipse([px(cx - 6), px(y0 + lid + 8), px(cx + 6), px(y0 + lid + 20)], fill=H('#5a4a30'))
    for x in (x0 + 40, x1 - 40): d.arc([px(x - 14), px(y0 + lid + 30), px(x + 14), px(y0 + lid + 60)], 0, 180, fill=H('#2a2420'), width=px(3))
    if dusty: dust_on(img, (x0 - 6, y0, x1 + 6, y0 + 10), seed + 5)


def tansu(img, x0, y0, x1, y1, seed, col='#3c2a1c', dusty=True):
    fill(img, col, seed, rect=(x0, y0, x1, y1), scale=10, stretch=(3, .5), contrast=1.1); d = ImageDraw.Draw(img)
    rows = [(y0 + 14, y0 + (y1 - y0) * .28), (y0 + (y1 - y0) * .3, y0 + (y1 - y0) * .52), (y0 + (y1 - y0) * .54, y0 + (y1 - y0) * .76), (y0 + (y1 - y0) * .78, y1 - 14)]
    for i, (a, b) in enumerate(rows):
        if i == 0:
            for xa, xb in ((x0 + 12, (x0 + x1) / 2 - 3), ((x0 + x1) / 2 + 3, x1 - 12)):
                fill(img, lt(H(col), .06), seed + 10 + i + int(xa), rect=(xa, a, xb, b), scale=8, stretch=(3, .5)); d.rectangle([px(xa), px(a), px(xb), px(b)], outline=H('#120c08'), width=px(2))
                cx = (xa + xb) / 2; d.rectangle([px(cx - 14), px((a + b) / 2 - 3), px(cx + 14), px((a + b) / 2 + 3)], fill=H('#15110e'))
        else:
            fill(img, lt(H(col), .04), seed + 10 + i, rect=(x0 + 12, a, x1 - 12, b), scale=8, stretch=(3, .5)); d.rectangle([px(x0 + 12), px(a), px(x1 - 12), px(b)], outline=H('#120c08'), width=px(2))
            for cx in (x0 + (x1 - x0) * .28, x0 + (x1 - x0) * .72):
                d.rectangle([px(cx - 17), px((a + b) / 2 - 12), px(cx + 17), px((a + b) / 2 + 12)], fill=H('#1a1512')); d.arc([px(cx - 12), px((a + b) / 2 - 6), px(cx + 12), px((a + b) / 2 + 14)], 0, 180, fill=H('#4a4034'), width=px(2.4))
    volume(img, (x0, y0, x1, y1), .35, .2)
    if dusty: dust_on(img, (x0, y0, x1, y0 + 8), seed + 7, 90)


def kiri_box(img, x0, y0, x1, y1, seed, label=None, cord='#6a3a2a', col='#9a8466'):
    fill(img, col, seed, rect=(x0, y0, x1, y1), scale=8, stretch=(3, .5), contrast=.8, dark=.35)
    ImageDraw.Draw(img).rectangle([px(x0), px(y0), px(x1), px(y0 + 7)], fill=dk(H(col), .25))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; line(img, [(cx, y0), (cx, y1)], cord, 3.4); line(img, [(x0, cy + 6), (x1, cy + 6)], cord, 3.4)
    ell(img, (cx - 7, cy, cx + 7, cy + 12), cord)
    if label: fill(img, '#d8ceb4', seed + 3, rect=(x0 + 10, y0 + 14, x0 + 34, y1 - 12), scale=3, contrast=.4); text(img, label, x0 + 22, (y0 + y1) / 2, 15, '#1a1210', SERIF)
    volume(img, (x0, y0, x1, y1), .35, .2)


def tawara_end(img, cx, cy, r, seed):
    """Rice bale seen from its round end: radial straw, a rope ring."""
    fill(img, '#8a7648', seed, ell=(cx - r, cy - r, cx + r, cy + r), scale=4, contrast=1.3)
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l); rr = random.Random(seed)
    for k in range(70):
        a = rr.uniform(0, math.tau); r0 = rr.uniform(0, r * .3)
        d.line([(px(cx + math.cos(a) * r0), px(cy + math.sin(a) * r0)), (px(cx + math.cos(a) * r * .95), px(cy + math.sin(a) * r * .95))], fill=(50, 38, 20, 110), width=px(1))
    img.alpha_composite(l)
    d = ImageDraw.Draw(img)
    for rr_ in (r * .82, r * .5): d.ellipse([px(cx - rr_), px(cy - rr_), px(cx + rr_), px(cy + rr_)], outline=H('#5a4626'), width=px(3.5))
    d.ellipse([px(cx - r * .14), px(cy - r * .14), px(cx + r * .14), px(cy + r * .14)], fill=H('#3a2c16'))
    volume(img, (cx - r, cy - r, cx + r, cy + r), .5, .45)


def komodaru(img, cx, base, w, h, seed, mark='酒', band='#b8322a'):
    """Sake cask wrapped in straw matting with a painted label."""
    barrel(img, cx, base, w, h, '#a89060', seed, '#4a3a22')
    m = I.mask_poly(img, rect=(cx - w * .5, base - h * .7, cx + w * .5, base - h * .3))
    clip(img, m, lambda d: d.rectangle([px(cx - w * .5), px(base - h * .66), px(cx + w * .5), px(base - h * .34)], fill=H(band)[:3] + (210,)))
    text(img, mark, cx, base - h * .5, h * .24, '#f0e8d4', SERIF)
    for k, yy in enumerate((base - h * .9, base - h * .1)): rope(img, [(cx - w * .5, yy), (cx + w * .5, yy)], '#6a5430', 4)
    volume(img, (cx - w / 2, base - h, cx + w / 2, base), .4, .35)


def hanging_string(img, x, y0, y1, kind, seed, n=None):
    """Dried persimmons, daikon or herbs hanging from a cord."""
    rr = random.Random(seed); line(img, [(x, y0), (x + rr.uniform(-3, 3), y1)], '#6a5430', 2.2)
    if kind == 'kaki':
        n = n or 8
        for k in range(n):
            y = y0 + 22 + (y1 - y0 - 30) * k / max(1, n - 1); cx = x + rr.uniform(-3, 3)
            blob(img, [(cx - 13, y), (cx - 11, y - 11), (cx, y - 15), (cx + 11, y - 11), (cx + 13, y), (cx + 8, y + 12), (cx, y + 15), (cx - 8, y + 12)], hexc(rr.choice(['#b0501c', '#9a4418', '#c0662a'])), seed + k, scale=3, k=.6, rim=.4, spec=.15)
            poly(img, [(cx - 5, y - 16), (cx + 5, y - 16), (cx, y - 11)], '#3a2a14')
    elif kind == 'daikon':
        for k in range(n or 4):
            y = y0 + 20 + k * 58; cx = x + (k % 2) * 8 - 4
            blob(img, [(cx - 9, y), (cx + 9, y), (cx + 6, y + 60), (cx, y + 78), (cx - 6, y + 60)], hexc('#c8bc98'), seed + k, scale=3, k=.4, rim=.3)
    elif kind == 'herb':
        for k, dx in enumerate((-14, 0, 14)):
            pts = [(x, y0 + 30), (x + dx * 1.6, y1)]; line(img, pts, '#3a4424', 2)
            I.P.dab_mass(ImageDraw.Draw(img), [(px(x + dx * 1.2), px(y0 + 30 + (y1 - y0 - 30) * .7), px(18), px((y1 - y0) * .32))], 140, 'leaf', [hexc('#2a3018'), hexc('#3e4424'), hexc('#5a5a30'), hexc('#6e6a3c')], random.Random(seed + k), size=(3, 6))
        rope(img, [(x - 10, y0 + 26), (x + 10, y0 + 26)], '#8a6a3a', 5)


def ichimatsu(img, cx, base, h, seed, kimono='#8a2a2a'):
    """A forgotten ichimatsu doll sitting: bobbed hair, white face, faded kimono."""
    s = h / 120
    blob(img, [(cx - 34 * s, base), (cx - 30 * s, base - 50 * s), (cx - 16 * s, base - 72 * s), (cx + 16 * s, base - 72 * s), (cx + 30 * s, base - 50 * s), (cx + 34 * s, base)], hexc(kimono), seed, scale=3, k=.5)
    rr = random.Random(seed); d = ImageDraw.Draw(img)
    for _ in range(14):
        x, y = cx + rr.uniform(-26, 26) * s, base - rr.uniform(8, 64) * s; d.ellipse([px(x - 3 * s), px(y - 3 * s), px(x + 3 * s), px(y + 3 * s)], fill=(210, 170, 120, 160))
    fill(img, '#c8a040', seed + 1, rect=(cx - 24 * s, base - 50 * s, cx + 24 * s, base - 40 * s), scale=2)
    ell(img, (cx - 20 * s, base - 112 * s, cx + 20 * s, base - 70 * s), '#e8dcc8'); volume(img, (cx - 20 * s, base - 112 * s, cx + 20 * s, base - 70 * s), .5, .3)
    blob(img, [(cx - 23 * s, base - 84 * s), (cx - 22 * s, base - 110 * s), (cx, base - 122 * s), (cx + 22 * s, base - 110 * s), (cx + 23 * s, base - 84 * s), (cx + 14 * s, base - 100 * s), (cx - 14 * s, base - 100 * s)], hexc('#141010'), seed + 2, scale=2, k=.3)
    for ex in (-7, 7): d.ellipse([px(cx + ex * s - 2 * s), px(base - 92 * s), px(cx + ex * s + 2 * s), px(base - 88 * s)], fill=H('#1a1414'))
    d.ellipse([px(cx - 2 * s), px(base - 80 * s), px(cx + 2 * s), px(base - 77 * s)], fill=H('#b83030'))


def lattice_window_round(img, cx, cy, r, seed, moon=(0, 0)):
    d = ImageDraw.Draw(img)
    sky = gradient(hexc('#1a2438'), hexc('#2c3a50'), h=px(2 * r), w=px(2 * r)); m = Image.new('L', sky.size, 0); ImageDraw.Draw(m).ellipse([0, 0, sky.width - 1, sky.height - 1], fill=255)
    img.paste(sky, (px(cx - r), px(cy - r)), m)
    glow(img, cx + moon[0], cy + moon[1], r * 1.6, hexc('#c8d4e8'), .35)
    ell(img, (cx + moon[0] - 30, cy + moon[1] - 30, cx + moon[0] + 30, cy + moon[1] + 30), '#e9e4cc')
    fill(img, '#d8d2b8', seed, ell=(cx + moon[0] - 30, cy + moon[1] - 30, cx + moon[0] + 30, cy + moon[1] + 30), scale=3, contrast=.6, dark=.15, light=.1)
    for x in (cx - r * .5, cx, cx + r * .5): d.line([(px(x), px(cy - r)), (px(x), px(cy + r))], fill=H('#1c140e'), width=px(5))
    d.line([(px(cx - r), px(cy)), (px(cx + r), px(cy))], fill=H('#1c140e'), width=px(5))
    d.ellipse([px(cx - r - 10), px(cy - r - 10), px(cx + r + 10), px(cy + r + 10)], outline=H('#20160e'), width=px(16))
    d.ellipse([px(cx - r - 12), px(cy - r - 12), px(cx + r + 12), px(cy + r + 12)], outline=H('#3a2a1c'), width=px(3))


# ───────────────────────── 屋根裏 — the attic ─────────────────────────
def attic():
    P.set_size(1800, 1400); st = Stack('attic')
    img = gradient(hexc('#1c150e'), hexc('#120d09'))
    # underside of the thatched roof: straw, bamboo battens radiating to the depth, then the round rafters
    img.alpha_composite(textured_fill(Image.new('L', (SW, SH), 255), hexc('#35291a'), hexc('#150f09'), hexc('#54432a'), 14 * SS, 3, (1, 1), 1.3))
    straws(img, (0, 0, 1800, 1000), 5000, 4, cols=('#6a5634', '#4a3c24', '#8a7244'), L=(10, 34), a=(50, 140))
    A, Pk, B = (-60, 1000), (900, -260), (1860, 1000)
    for k in range(34):
        t = k / 33
        for E in (A, B):
            Q = (E[0] + (Pk[0] - E[0]) * t, E[1] + (Pk[1] - E[1]) * t); Q2 = vp_scale(Q, 3.2)
            line(img, [Q, Q2], '#2a2216', 5); line(img, [(Q[0] + 1, Q[1] - 2), (Q2[0] + 3, Q2[1] - 6)], '#5a4a2e', 1.4)
    for s in (1.06, 1.16, 1.29, 1.45, 1.66, 1.93, 2.3):
        for E in (A, B):
            a, b = vp_scale(E, s), vp_scale(Pk, s); w = 13 * s
            line(img, [a, b], '#140e09', w); line(img, [(a[0] + w * .25, a[1] - w * .25), (b[0] + w * .25, b[1] - w * .25)], '#3a2c1e', w * .3)
    # the gable end wall: earthen plaster in a timber frame
    gm = I.mask_poly(img, poly=[A, Pk, B, (1860, 1400), (-60, 1400)])
    wall = Image.new('RGBA', img.size, (0, 0, 0, 0)); fill(wall, '#4a3c2a', 11, mask=gm, scale=60, contrast=.9, dark=.45, light=.18)
    specks(wall, (0, 0, 1800, 1140), 900, '#2a2016', 12, (1, 3), (60, 140)); img.alpha_composite(wall)
    ramp_shade(img, (0, 0, 1800, 1140), .55, 1.0)
    for E in (A, B): line(img, [E, Pk], '#120c08', 26)
    wood_block(img, (-10, 740, 1810, 764), 13, hexc('#2a1e14'), hexc('#100b07'), hexc('#3c2c1e'))
    for x in (150, 1650): wood_block(img, (x - 22, 300, x + 22, 1140), 14 + x, hexc('#2c2016'), hexc('#100b07'), hexc('#44321f'), True)
    wood_block(img, (-10, 1112, 1810, 1142), 15, hexc('#241a12'), hexc('#0c0806'), hexc('#3a2a1c'))
    # the round window with the moon and its shaft of light
    lattice_window_round(img, 1190, 560, 98, 16, (22, -26))
    light_wedge(img, [(1112, 590), (1268, 610), (1080, 1140), (720, 1140)], '#b8c4d8', 55, 18, 22)
    specks(img, (760, 600, 1260, 1130), 260, '#e8ecf4', 17, (.8, 2.2), (60, 190))
    # the curved log tie beam, the king post and cobwebs where they meet the roof
    wood_block(img, (878, -20, 922, 400), 18, hexc('#2a1e14'), hexc('#100b07'), hexc('#3e2e1e'), True)
    for sx in (-1, 1): line(img, [(900 + sx * 20, 190), (900 + sx * 300, 390)], '#1c140c', 22)
    log_beam(img, -80, 1880, 420, 34, 34, 19)
    cobweb(img, 172, 454, 150, .05, 1.45, 20); cobweb(img, 1628, 454, 150, 1.7, 3.1, 21); cobweb(img, 900, 60, 120, -.4, .6, 22, 60)
    cobweb(img, 120, 1000, 90, -1.3, -.1, 23, 60)
    # things hung from the beam: dried persimmons, herbs, a folded lantern, a straw rope
    for k, x in enumerate((520, 580, 640)): hanging_string(img, x, 430 + k * 6, 650 + k * 30, 'kaki', 30 + k)
    for k, x in enumerate((1420, 1480)): hanging_string(img, x, 436, 590, 'herb', 40 + k)
    line(img, [(300, 440), (300, 480)], '#1a120c', 2)
    fill(img, '#b8a888', 45, rect=(276, 480, 324, 500), scale=3); fill(img, '#9a8a6a', 46, ell=(274, 492, 326, 540), scale=3); ImageDraw.Draw(img).rectangle([px(276), px(536), px(324), px(548)], fill=H('#1a120c'))
    rope(img, [(980 + 150 * k / 20, 440 + 90 * math.sin(math.pi * k / 20)) for k in range(21)], '#8a7244', 7)
    for k in range(10): line(img, [(990 + k * 14, 450 + 88 * math.sin(math.pi * (k + .5) / 10) - 4), (996 + k * 14, 450 + 88 * math.sin(math.pi * (k + .5) / 10) + 5)], '#4a3a1e', 2)
    # the clutter along the wall
    for k, (x0, y0, x1, y1, lb) in enumerate(((40, 1010, 250, 1140, '箱'), (58, 900, 236, 1010, None), (80, 812, 214, 900, '書'))):
        kiri_box(img, x0, y0, x1, y1, 50 + k, lb)
    dust_on(img, (80, 812, 214, 820), 53, 90)
    chest(img, 300, 990, 640, 1140, 55)
    ichimatsu(img, 560, 992, 118, 56)
    fill(img, '#5a4a2e', 57, poly=[(660, 1140), (650, 1070), (690, 1052), (780, 1054), (800, 1076), (790, 1140)], scale=4, contrast=1.2)
    clip(img, I.mask_poly(img, poly=[(660, 1140), (650, 1070), (690, 1052), (780, 1054), (800, 1076), (790, 1140)]),
         lambda d: [d.line([(px(640 + k * 9), px(1050)), (px(610 + k * 9), px(1140))], fill=(30, 22, 12, 120), width=px(2)) for k in range(24)])
    volume(img, (650, 1052, 800, 1140), .4, .3)
    for k in range(4):   # coil of straw rope right of Musya
        r = 70 - k * 13; ImageDraw.Draw(img).ellipse([px(1150 - r), px(1112 - r * .32), px(1150 + r), px(1112 + r * .32)], outline=H('#7a6438'), width=px(8))
        ImageDraw.Draw(img).ellipse([px(1150 - r), px(1112 - r * .32), px(1150 + r), px(1112 + r * .32)], outline=H('#4a3a1e'), width=px(2))
    line(img, [(1260, 1140), (1300, 850)], '#2a2016', 5)                                 # a torn paper umbrella leaning
    poly(img, [(1300, 850), (1236, 1000), (1262, 1010), (1300, 858)], '#6a2a22'); poly(img, [(1300, 850), (1330, 1004), (1300, 1010)], '#5a241c')
    poly(img, [(1300, 850), (1262, 1010), (1300, 1012)], '#7a3228'); line(img, [(1276, 950), (1290, 980)], '#140e0a', 3)
    tansu(img, 1350, 860, 1590, 1140, 60)
    kiri_box(img, 1612, 1030, 1780, 1140, 61, '古', col='#8a7458'); kiri_box(img, 1630, 950, 1760, 1030, 62, None, col='#7a6650')
    straws(img, (0, 1100, 1800, 1140), 300, 63)
    img = st.cut(img, 'wall', .4)
    # the floor: planks into the depth, the moonlit patch with the window's cross, dust and straw
    persp_floor(img, FL, 70, '#3a2c1e', '#150f0a', '#58442e', pw=.26, L=.7)
    ImageDraw.Draw(img).rectangle([0, px(FL), SW, px(FL + 4)], fill=H('#0c0806'))
    patch = Image.new('RGBA', img.size, (0, 0, 0, 0)); pd = ImageDraw.Draw(patch)
    pd.ellipse([px(700), px(1170), px(1080), px(1320)], fill=(190, 200, 220, 70))
    for x in (800, 890, 980): pd.polygon([(px(x), px(1170)), (px(x + 14), px(1170)), (px(x - 20), px(1320)), (px(x - 36), px(1320))], fill=(0, 0, 0, 0))
    pd.rectangle([px(690), px(1236), px(1090), px(1250)], fill=(0, 0, 0, 0))
    img.alpha_composite(patch.filter(ImageFilter.GaussianBlur(9 * SS)))
    specks(img, (0, 1150, 1800, 1400), 700, '#8a8070', 71, (1, 2.6), (40, 110)); straws(img, (0, 1150, 1800, 1400), 400, 72, L=(10, 40))
    img = st.cut(img, 'floor', .8)
    # near the lens: a post, a beam across the top, a hanging straw rope and persimmons, a cobweb
    wood_block(img, (0, -20, 96, 1420), 80, hexc('#16100b'), hexc('#070504'), hexc('#241a12'), True)
    log_beam(img, -60, 1860, 26, 6, 40, 81, ('#0a0705', '#18110c', '#2a1e14'))
    cobweb(img, 96, 60, 220, .1, 1.5, 82, 110)
    rope(img, [(1560, 40), (1566, 300), (1560, 520)], '#6a5634', 12)
    for k in range(5): line(img, [(1548, 520 + k * 3), (1540 + k * 7, 590)], '#6a5634', 3)
    hanging_string(img, 1700, 50, 420, 'kaki', 83, 6)
    st.finish(img, 'near', 1.4, blur=6, lift=(9, 7, 5), sat=0.82, gamma=1.04)


# ───────────────────────── 蔵 — the storehouse ─────────────────────────
def kura():
    P.set_size(1800, 1400); st = Stack('kura')
    img = gradient(hexc('#2a241c'), hexc('#1a150f'))
    # ceiling: boards into the depth and heavy joists
    ce = I.mask_poly(img, rect=(0, 0, 1800, 232)); fill(img, '#2a1e14', 1, mask=ce, scale=20, contrast=1.1)
    for k in range(-14, 15):
        Q = (VPX + k * 64, 232); line(img, [Q, vp_scale(Q, 6)], '#120c08', 3)
    for s, w in ((1.0, 30), (1.3, 42), (1.8, 60)):
        y = VPY - (VPY - 232) * s; wood_block(img, (-10, y - w, 1810, y), 2 + int(s * 10), hexc('#2c1f14'), hexc('#0e0906'), hexc('#44301e'))
        ImageDraw.Draw(img).line([(0, px(y)), (SW, px(y))], fill=H('#0a0604'), width=px(3))
    # thick white plaster walls with a wooden wainscot, posts and a tie beam
    fill(img, '#8e8676', 3, rect=(0, 232, 1800, 880), scale=70, contrast=.8, dark=.3, light=.12)
    specks(img, (0, 240, 1800, 880), 260, '#5a5246', 4, (1, 2.5), (20, 60))
    stain = Image.new('RGBA', img.size, (0, 0, 0, 0)); rr = random.Random(5); sd = ImageDraw.Draw(stain)
    for _ in range(26):
        x, y = rr.uniform(0, 1800), rr.uniform(260, 800); sd.ellipse([px(x - 50), px(y - 20), px(x + 50), px(y + 120)], fill=(60, 50, 34, 40))
    img.alpha_composite(stain.filter(ImageFilter.GaussianBlur(14 * SS)))
    P.vertical_boards(img, (0, 880, 1800, 1140), 6, hexc('#3a2c1e'), hexc('#1a130c'), hexc('#54402a'), 64)
    wood_block(img, (-10, 870, 1810, 890), 7, hexc('#2a1e14'), hexc('#100b07'), hexc('#3e2e1e'))
    wood_block(img, (-10, 232, 1810, 262), 8, hexc('#2a1e14'), hexc('#100b07'), hexc('#3e2e1e'))
    for x in (140, 1660): wood_block(img, (x - 26, 232, x + 26, 1140), 9 + x, hexc('#2e2116'), hexc('#110b07'), hexc('#46331f'), True)
    wood_block(img, (-10, 470, 1810, 500), 10, hexc('#2e2116'), hexc('#110b07'), hexc('#46331f'))
    # the heavy kura door: stepped plaster jambs, two dark leaves, iron, a sliver of moonlight
    for k, (c, g) in enumerate((('#a09888', 0), ('#8a8272', 16), ('#746c5e', 30))):
        fill(img, c, 20 + k, rect=(180 + g, 560 + g, 500 - g, 1140), scale=20, contrast=.7)
    for k, (x0, x1) in enumerate(((226, 338), (342, 454))):
        fill(img, '#3a3632', 23 + k, rect=(x0, 604, x1, 1140), scale=16, contrast=.9); volume(img, (x0, 604, x1, 1140), .3, .2)
        for y in (650, 1080): ImageDraw.Draw(img).rectangle([px(x0), px(y), px(x1), px(y + 14)], fill=H('#16130f'))
    glow(img, 340, 870, 90, hexc('#8ea6d0'), .35); ImageDraw.Draw(img).rectangle([px(337), px(604), px(343), px(1140)], fill=H('#a8bce0'))
    fill(img, '#1c1814', 25, rect=(300, 840, 380, 870), scale=3); ell(img, (322, 830, 358, 880), '#2a2420'); ell(img, (334, 846, 346, 864), '#0a0806')
    # a narrow barred window high up, with the moon
    for k, (c, g) in enumerate((('#9a9282', 0), ('#827a6a', 12))):
        fill(img, c, 30 + k, rect=(1040 + g, 290 + g, 1320 - g, 420 - g), scale=12, contrast=.7)
    sky = gradient(hexc('#152036'), hexc('#26344c'), h=px(106), w=px(256)); img.alpha_composite(sky, (px(1052), px(302)))
    glow(img, 1240, 336, 140, hexc('#c8d4e8'), .3); ell(img, (1222, 318, 1262, 358), '#e6e0c8')
    for k in range(6): wood_block(img, (1068 + k * 44, 300, 1080 + k * 44, 412), 33 + k, hexc('#2a2622'), hexc('#0e0c0a'), hexc('#46403a'), True)
    light_wedge(img, [(1060, 420), (1310, 420), (1150, 1140), (820, 1140)], '#a8b8d4', 34, 10, 26)
    # rice bales stacked end-on
    for k, (cx, cy) in enumerate(((560, 1094), (656, 1094), (752, 1094), (608, 1006), (704, 1006), (656, 918))):
        tawara_end(img, cx, cy, 47, 40 + k)
    # sake casks and a miso barrel on the right of Musya
    komodaru(img, 1090, 1140, 118, 132, 50, '酒'); komodaru(img, 1210, 1140, 118, 132, 51, '福', '#2a4a7a'); komodaru(img, 1150, 1008, 110, 118, 52, '蔵')
    # shelves: kiri boxes, jars and bottles
    for x in (1300, 1520, 1760): wood_block(img, (x - 10, 470, x + 10, 1140), 60 + x, hexc('#2e2116'), hexc('#110b07'), hexc('#46331f'), True)
    rr = random.Random(61)
    for si, y in enumerate((640, 820, 1000)):
        wood_block(img, (1290, y, 1770, y + 16), 62 + si, hexc('#3a2a1c'), hexc('#140e09'), hexc('#54402a'))
        x = 1316
        while x < 1740:
            kind = rr.choice(['box', 'box', 'jar', 'jar', 'bottle']);
            if x + 60 > 1750: break
            if kind == 'box':
                w, h = rr.uniform(70, 110), rr.uniform(50, 110); w = min(w, 1752 - x); kiri_box(img, x, y - h, x + w, y, 70 + si * 10 + int(x), rr.choice(['茶', '器', '書', None]), col=rr.choice(['#9a8466', '#8a7458', '#a8927a'])); x += w + 8
            elif kind == 'jar':
                w, h = rr.uniform(56, 80), rr.uniform(60, 100); crock(img, x + w / 2, y, w, h, rr.choice(['#5a3a24', '#3a3a3a', '#6a5a3a', '#2a3444']), 90 + int(x) + si); x += w + 10
            else:
                crock(img, x + 20, y, 40, 86, '#c8b898', 95 + int(x)); fill(img, '#2a4a7a', 96 + int(x), rect=(x + 10, y - 60, x + 30, y - 40), scale=2); x += 50
        straws(img, (1290, y - 6, 1770, y), 40, 64 + si, L=(6, 14))
    for k, (cx, w, h, col) in enumerate(((1350, 110, 130, '#4a3222'), (1450, 90, 100, '#3a3a36'), (1560, 120, 150, '#5a3a24'), (1680, 100, 116, '#2a3036'))):
        crock(img, cx, 1140, w, h, col, 100 + k, lid='#3a2a1c' if k % 2 == 0 else None)
    # the lantern that lights the kura
    line(img, [(960, 500), (960, 520)], '#0d0906', 3)
    P.chochin(img, 960, 580, 44, True); glow(img, 960, 580, 520, hexc('#ffb060'), .28); glow(img, 960, 580, 150, hexc('#ffc880'), .3)
    ImageDraw.Draw(img).rectangle([px(958), px(500), px(962), px(522)], fill=H('#0d0906'))
    hanging_string(img, 800, 500, 780, 'daikon', 110, 4)
    cobweb(img, 166, 262, 130, .05, 1.5, 111, 70); cobweb(img, 1634, 262, 130, 1.65, 3.1, 112, 70)
    ramp_shade(img, (0, 232, 1800, 1140), .75, 1.0)
    falloff(img, 960, 600, 1250, .42)
    img = st.cut(img, 'wall', .4)
    persp_floor(img, FL, 120, '#3e2e1e', '#171009', '#5e4a32', pw=.34, L=.9)
    ImageDraw.Draw(img).rectangle([0, px(FL), SW, px(FL + 4)], fill=H('#0c0806'))
    glow(img, 960, 1220, 520, hexc('#ffa050'), .2); falloff(img, 960, 700, 1300, .5)
    patch = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(patch).ellipse([px(800), px(1180), px(1160), px(1300)], fill=(170, 186, 214, 50)); img.alpha_composite(patch.filter(ImageFilter.GaussianBlur(14 * SS)))
    straws(img, (0, 1150, 1800, 1400), 600, 121, L=(10, 40)); specks(img, (470, 1145, 820, 1260), 400, '#e8e0cc', 122, (.8, 1.8), (90, 200))
    specks(img, (0, 1150, 1800, 1400), 500, '#8a8070', 123, (1, 2.4), (30, 90))
    img = st.cut(img, 'floor', .8)
    wood_block(img, (0, -20, 84, 1420), 130, hexc('#18110c'), hexc('#070504'), hexc('#281c12'), True)
    wood_block(img, (1726, -20, 1800, 1420), 131, hexc('#18110c'), hexc('#070504'), hexc('#281c12'), True)
    log_beam(img, -60, 1860, 24, 4, 38, 132, ('#0a0705', '#18110c', '#2a1e14'))
    tawara_end(img, 110, 1330, 150, 133)
    for k in range(3): rope(img, [(1726 - 10 * k, 360 + k * 30), (1660 - k * 12, 560 + k * 26), (1726 - 10 * k, 760 + k * 20)], '#6a5634', 9)
    img = P.darken(img, .45, (8, 6, 4))
    st.finish(img, 'near', 1.4, blur=6, lift=(10, 8, 6), sat=0.8, gamma=1.04)


# ───────────────────────── boards, padlock and cobweb for the locked-room preview ─────────────────────────
SPR = {}


def boards_sheet():
    img = canvas(1000, 560)
    for k in range(3):
        y0 = 4 + k * 116; col = ['#6a543a', '#5a4630', '#74603f'][k]
        fill(img, col, 200 + k, rect=(6, y0, 994, y0 + 100), scale=14, stretch=(8, .25), contrast=1.2)
        clip(img, I.mask_poly(img, rect=(6, y0, 994, y0 + 100)), lambda d, y0=y0: [d.line([(0, px(y0 + 8 + j * 9 + math.sin(j) * 3)), (px(1000), px(y0 + 12 + j * 9))], fill=(20, 12, 6, 70), width=px(1.2)) for j in range(10)])
        if k == 1: poly(img, [(6, y0), (60, y0), (6, y0 + 100)], (0, 0, 0, 0))   # a split-off corner
        volume(img, (6, y0, 994, y0 + 100), .3, .25)
        for x in (50, 950):
            for dy in (30, 70): ell(img, (x - 8, y0 + dy - 8, x + 8, y0 + dy + 8), '#1a1614'); ell(img, (x - 4, y0 + dy - 5, x + 1, y0 + dy), '#6a6258')
        SPR['b%d' % k] = [0, y0, 1000, 104]
    y0 = 360; cx = 80                                           # the old Japanese padlock (ebisu-jō)
    line(img, [(cx - 34, y0 + 70), (cx - 34, y0 + 30), (cx, y0 + 8), (cx + 34, y0 + 30), (cx + 34, y0 + 70)], '#2a2420', 12)
    fill(img, '#3a3228', 210, rect=(cx - 56, y0 + 64, cx + 56, y0 + 180), scale=6, contrast=1.3); volume(img, (cx - 56, y0 + 64, cx + 56, y0 + 180), .5, .35, spec=.2)
    fill(img, '#8a6a30', 211, rect=(cx - 44, y0 + 84, cx + 44, y0 + 96), scale=2); ell(img, (cx - 9, y0 + 114, cx + 9, y0 + 132), '#0a0806'); poly(img, [(cx - 4, y0 + 126), (cx + 4, y0 + 126), (cx + 6, y0 + 160), (cx - 6, y0 + 160)], '#0a0806')
    SPR['lock'] = [0, 360, 164, 196]
    cobweb(img, 170, 364, 190, .02, 1.55, 212, 150); SPR['web'] = [168, 360, 200, 200]
    out = img.resize((1000, 560), Image.LANCZOS); out.save(os.path.join(OUT, 'ro_boards.webp'), 'WEBP', quality=86, alpha_quality=90, method=6)


# ───────────────────────── decorations: ~30 per room, one atlas each ─────────────────────────
ROWS, IMGS = [], {}


def save(img, iid, name, cat, anchor='b', price=60, glow_=None, src=None, hint=None):
    out = img.resize((P.W, P.H), Image.LANCZOS)
    a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .88
    a[..., :3] += np.random.default_rng(abs(hash(iid)) % 2 ** 32).normal(0, 3.5, a.shape[:2])[..., None]
    IMGS.setdefault(cat, []).append((iid, Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')))
    row = {'id': iid, 'n': name, 'c': cat, 'w': P.W, 'h': P.H, 'a': anchor, 'p': price}
    if glow_: row['glow'] = glow_
    if src: row['src'] = src; row['hint'] = hint
    ROWS.append(row)


def pack(cat, key):
    lst = sorted(IMGS[cat], key=lambda t: -t[1].height); W = 1400; x = y = rowh = 0; pos = {}
    for iid, im in lst:
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[iid] = (x, y); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for iid, im in lst: at.paste(im, pos[iid])
    at.save(os.path.join(ITEMS_DIR, f'atlas_{key}.webp'), 'WEBP', quality=86, alpha_quality=90, method=6)
    for r in ROWS:
        if r['id'] in pos: r['at'] = [key, pos[r['id']][0], pos[r['id']][1]]
    print('atlas', key, at.size, len(lst)); return [W, y + rowh]


def attic_items():
    C = 'Чердак'; F = '🐾 находка на чердаке'; FH = 'Эта вещь найдётся в сундуке на чердаке — роется Муся раз в день'
    img = canvas(300, 190); floor_shadow(img, 150, 184, 140); chest(img, 12, 40, 288, 184, 300); save(img, 'at_nagamochi', 'Сундук нагамоти', C, 'b', 160)
    img = canvas(220, 270); floor_shadow(img, 110, 264, 104); tansu(img, 10, 14, 210, 264, 301); save(img, 'at_tansu', 'Пыльный комод тансу', C, 'b', 200)
    img = canvas(180, 210); floor_shadow(img, 90, 204, 86); kiri_box(img, 8, 118, 172, 204, 302, '箱'); kiri_box(img, 20, 44, 160, 118, 303, None, col='#8a7458'); save(img, 'at_kiribako', 'Стопка ящиков из павловнии', C, 'b', 90)
    img = canvas(120, 150); floor_shadow(img, 60, 146, 50); ichimatsu(img, 60, 146, 140, 304); save(img, 'at_hina_doll', 'Забытая кукла итимацу', C, 'b', 120)
    img = canvas(110, 280); hanging_string(img, 55, 0, 270, 'kaki', 305, 9); save(img, 'at_hoshigaki', 'Связка сушёной хурмы', C, 't', 50)
    img = canvas(200, 190); rope(img, [(10, 14), (100, 26), (190, 14)], '#6a5634', 3)
    for k, x in enumerate((50, 100, 150)): hanging_string(img, x, 20, 176, 'herb', 306 + k)
    save(img, 'at_herbs', 'Пучки сушёных трав', C, 't', 40)
    img = canvas(180, 110); floor_shadow(img, 90, 104, 84)
    for k in range(4):
        r = 80 - k * 16; ImageDraw.Draw(img).ellipse([px(90 - r), px(76 - r * .34), px(90 + r), px(76 + r * .34)], outline=H('#8a7244'), width=px(10)); ImageDraw.Draw(img).ellipse([px(90 - r), px(76 - r * .34), px(90 + r), px(76 + r * .34)], outline=H('#4a3a1e'), width=px(2))
    save(img, 'at_nawa', 'Моток соломенной верёвки', C, 'b', 20)
    img = canvas(200, 200); cobweb(img, 0, 0, 200, .02, 1.55, 307, 170); save(img, 'at_kumo', 'Паутина в углу', C, 't', 10)
    img = canvas(170, 250); line(img, [(85, 0), (85, 20)], '#2a2016', 3)                              # straw raincoat mino
    m = fill(img, '#7a6438', 308, poly=[(60, 20), (110, 20), (160, 240), (10, 240)], scale=3, stretch=(.3, 3), contrast=1.4)
    clip(img, m, lambda d: [d.line([(px(85 + (k - 20) * 2), px(20)), (px(85 + (k - 20) * 7.5), px(244))], fill=(40, 30, 14, 120), width=px(1.5)) for k in range(41)])
    for y in (80, 150): rope(img, [(20 + (y - 20) * .3, y), (150 - (y - 20) * .3, y)], '#5a4626', 3)
    volume(img, (10, 20, 160, 240), .4, .3); save(img, 'at_mino', 'Соломенный плащ мино', C, 't', 70)
    img = canvas(220, 110); floor_shadow(img, 110, 104, 100)                                             # sugegasa leaning
    fill(img, '#8a7446', 309, poly=[(10, 96), (110, 16), (210, 96)], scale=3, stretch=(1, 2), contrast=1.3)
    clip(img, I.mask_poly(img, poly=[(10, 96), (110, 16), (210, 96)]), lambda d: [d.line([(px(110), px(16)), (px(10 + k * 10), px(96))], fill=(50, 36, 16, 110), width=px(1)) for k in range(21)])
    line(img, [(40, 98), (180, 98)], '#3a2a16', 4); volume(img, (10, 16, 210, 100), .5, .3); save(img, 'at_sugegasa', 'Старая шляпа сугэгаса', C, 'b', 40)
    img = canvas(170, 150); floor_shadow(img, 85, 144, 80)                                               # stacked zaru sieves
    for k in range(4):
        y = 140 - k * 24; fill(img, '#9a8456', 310 + k, ell=(12 + k * 4, y - 26, 158 - k * 4, y), scale=2, contrast=1.3); ImageDraw.Draw(img).ellipse([px(12 + k * 4), px(y - 26), px(158 - k * 4), px(y)], outline=H('#5a4626'), width=px(3))
    volume(img, (12, 40, 158, 140), .4, .3); save(img, 'at_zaru', 'Стопка бамбуковых сит', C, 'b', 30)
    img = canvas(160, 170); floor_shadow(img, 80, 164, 70)                                               # basket of old yarn balls
    for k, (x, c) in enumerate(((56, '#8a3a3a'), (98, '#3a4a6a'), (76, '#7a6a3a'))): fill(img, c, 314 + k, ell=(x - 26, 50 - k * 6, x + 26, 102 - k * 6), scale=2, contrast=1.2); volume(img, (x - 26, 50 - k * 6, x + 26, 102 - k * 6), .5, .4)
    m = fill(img, '#6a5230', 317, poly=[(14, 80), (146, 80), (130, 164), (30, 164)], scale=3, contrast=1.3)
    clip(img, m, lambda d: [d.line([(px(14 + k * 8), px(80)), (px(30 + k * 6), px(164))], fill=(30, 20, 10, 110), width=px(2)) for k in range(18)] + [d.line([(0, px(y)), (px(160), px(y))], fill=(140, 110, 60, 90), width=px(2)) for y in range(86, 164, 10)])
    volume(img, (14, 80, 146, 164), .4, .3); save(img, 'at_kago', 'Корзина со старыми клубками', C, 'b', 40)
    img = canvas(110, 220); floor_shadow(img, 55, 214, 46)                                               # a dusty andon
    fill(img, '#1c140e', 318, rect=(14, 196, 96, 214), scale=3)
    for x in (16, 88): fill(img, '#1c140e', 319 + x, rect=(x, 30, x + 6, 200), scale=3)
    fill(img, '#c8b888', 320, rect=(22, 40, 88, 190), scale=4, contrast=.6)
    for y in (90, 140): line(img, [(22, y), (88, y)], '#2a1e14', 2)
    ImageDraw.Draw(img).polygon([(px(40), px(60)), (px(52), px(100)), (px(36), px(96))], fill=(40, 30, 20, 150))
    fill(img, '#1c140e', 321, rect=(10, 26, 100, 40), scale=3); dust_on(img, (10, 26, 100, 32), 322, 110)
    save(img, 'at_andon', 'Пыльный андон', C, 'b', 90, [55, 115])
    img = canvas(240, 220); floor_shadow(img, 120, 214, 110)                                              # spinning wheel
    ImageDraw.Draw(img).ellipse([px(110), px(20), px(230), px(140)], outline=H('#3a2a1a'), width=px(7))
    for k in range(8): a = k * math.pi / 4; line(img, [(170, 80), (170 + math.cos(a) * 58, 80 + math.sin(a) * 58)], '#3a2a1a', 3)
    ell(img, (160, 70, 180, 90), '#2a1e12'); fill(img, '#4a3622', 323, rect=(10, 170, 230, 196), scale=4, stretch=(4, .5))
    for x in (30, 200): fill(img, '#3a2a1a', 324 + x, rect=(x, 196, x + 12, 214), scale=3)
    line(img, [(170, 80), (170, 172)], '#3a2a1a', 8); line(img, [(40, 170), (40, 110)], '#3a2a1a', 6); fill(img, '#d8ccb0', 325, ell=(26, 94, 54, 118), scale=2)
    line(img, [(52, 104), (160, 30)], '#d8ccb0', 1.2); volume(img, (10, 20, 230, 214), .3, .2); save(img, 'at_itoguruma', 'Прялка итогурума', C, 'b', 150)
    img = canvas(150, 120); floor_shadow(img, 75, 114, 70)
    for k, (c, w) in enumerate((('#3a2a2a', 130), ('#2a3a4a', 120), ('#4a3a24', 126), ('#5a2a24', 110))):
        y = 112 - k * 22; fill(img, c, 326 + k, rect=(75 - w / 2 + k * 3, y - 20, 75 + w / 2 + k * 3, y), scale=3); fill(img, '#d8ccb0', 330 + k, rect=(75 - w / 2 + k * 3 + 4, y - 6, 75 + w / 2 + k * 3 - 2, y - 2), scale=2)
    dust_on(img, (14, 26, 140, 32), 331); volume(img, (10, 22, 140, 112), .3, .2); save(img, 'at_books', 'Стопка старых книг', C, 'b', 40)
    img = canvas(130, 260); floor_shadow(img, 65, 254, 40)                                               # torn umbrella
    line(img, [(65, 254), (65, 20)], '#2a2016', 5)
    for k, c in enumerate(('#6a2a22', '#7a3228', '#5a241c')): poly(img, [(65, 18), (20 + k * 30, 170), (50 + k * 30, 176)], c)
    line(img, [(55, 90), (70, 130), (60, 150)], '#140e0a', 3); fill(img, '#2a2016', 332, rect=(58, 176, 72, 186), scale=2)
    for k in range(5): line(img, [(65, 30), (18 + k * 22, 172)], '#1a120c', 1.4)
    save(img, 'at_wagasa', 'Рваный зонтик вагаса', C, 'b', 30)
    img = canvas(130, 200); floor_shadow(img, 65, 194, 56)                                               # clouded mirror on a stand
    fill(img, '#2a1a12', 333, rect=(20, 160, 110, 194), scale=3); line(img, [(65, 160), (65, 120)], '#2a1a12', 8)
    fill(img, '#2a1a12', 334, ell=(14, 14, 116, 130), scale=3); fill(img, '#7a8488', 335, ell=(24, 24, 106, 120), scale=4, contrast=.8)
    ImageDraw.Draw(img).ellipse([px(38), px(40), px(70), px(90)], fill=(220, 226, 230, 60)); dust_on(img, (24, 24, 106, 60), 336, 80)
    save(img, 'at_kagami', 'Мутное зеркало', C, 'b', 80)
    img = canvas(220, 180); floor_shadow(img, 110, 174, 100)                                              # wooden rocking horse
    for sx in (40, 180): line(img, [(sx, 110), (sx + (10 if sx < 100 else -10), 160)], '#6a4a2a', 7)
    ImageDraw.Draw(img).arc([px(10), px(110), px(210), px(200)], 200, 340, fill=H('#4a3220'), width=px(8))
    blob(img, [(40, 110), (60, 80), (160, 80), (180, 110)], hexc('#9a6a3a'), 337, scale=3); blob(img, [(150, 90), (170, 40), (196, 30), (206, 50), (178, 100)], hexc('#9a6a3a'), 338, scale=3)
    line(img, [(160, 44), (140, 90)], '#2a1a10', 6); ell(img, (186, 38, 194, 46), '#1a1210'); fill(img, '#b8322a', 339, rect=(80, 74, 130, 86), scale=2)
    save(img, 'at_mokuba', 'Деревянная лошадка', C, 'b', 120)
    img = canvas(120, 130); floor_shadow(img, 60, 126, 50)
    blob(img, [(60, 12), (100, 36), (110, 84), (92, 122), (28, 122), (10, 84), (20, 36)], hexc('#8a4a3a'), 340, spec=.1); ell(img, (34, 34, 86, 76), '#d8cbb0')
    ell(img, (40, 46, 54, 60), '#1a1210'); ImageDraw.Draw(img).ellipse([px(66), px(46), px(80), px(60)], outline=H('#1a1210'), width=px(2)); text(img, '福', 60, 98, 22, '#c8a870', SERIF)
    dust_on(img, (20, 12, 100, 40), 341, 90); save(img, 'at_daruma', 'Выцветший дарума', C, 'b', 30)
    img = canvas(180, 240); fill(img, '#d8ccb0', 342, poly=[(10, 10), (170, 10), (170, 170), (10, 170)], scale=4, contrast=.5)            # old kite
    for k in range(3): line(img, [(10 + k * 80, 10), (10 + k * 80, 170)], '#4a3a24', 2)
    text(img, '龍', 90, 90, 90, '#6a2a22', SERIF, True); ImageDraw.Draw(img).polygon([(px(120), px(10)), (px(170), px(10)), (px(170), px(60))], fill=(0, 0, 0, 0))
    for k in range(5): poly(img, [(88 + k * 4, 176 + k * 12), (98 + k * 4, 182 + k * 12), (88 + k * 4, 188 + k * 12)], ['#8a3a2a', '#3a4a6a'][k % 2])
    line(img, [(90, 170), (100, 236)], '#8a7a5a', 1.2); save(img, 'at_tako', 'Старый воздушный змей', C, 't', 50)
    img = canvas(90, 130); line(img, [(45, 0), (45, 22)], '#1a120c', 2); fill(img, '#b8a888', 343, rect=(18, 22, 72, 40), scale=3)
    for k in range(5): fill(img, lt(H('#a89878'), .04 * k), 344 + k, rect=(16, 40 + k * 14, 74, 52 + k * 14), scale=3)
    ImageDraw.Draw(img).rectangle([px(18), px(108), px(72), px(122)], fill=H('#1a120c')); save(img, 'at_chochin', 'Сложенный фонарь тётин', C, 't', 30)
    img = canvas(150, 110); floor_shadow(img, 75, 104, 70); blob(img, [(14, 104), (18, 50), (60, 30), (100, 34), (136, 56), (138, 104)], hexc('#2a4a6a'), 349, scale=3)
    poly(img, [(56, 34), (74, 6), (86, 16), (96, 36)], '#2a4a6a'); clip(img, I.mask_poly(img, rect=(0, 0, 150, 110)), lambda d: [d.ellipse([px(x - 5), px(y - 5), px(x + 5), px(y + 5)], outline=(220, 214, 196, 150), width=px(1.4)) for x in range(24, 140, 18) for y in range(50, 100, 16)])
    save(img, 'at_furoshiki', 'Узелок фуросики', C, 'b', 30)
    img = canvas(140, 70); floor_shadow(img, 70, 64, 64)
    for x0 in (8, 74):
        fill(img, '#6a5034', 350 + x0, poly=[(x0, 40), (x0 + 58, 34), (x0 + 60, 46), (x0 + 2, 52)], scale=3); fill(img, '#3a2a1a', 351 + x0, rect=(x0 + 10, 50, x0 + 20, 64), scale=2); fill(img, '#3a2a1a', 352 + x0, rect=(x0 + 40, 48, x0 + 50, 62), scale=2)
        line(img, [(x0 + 16, 40), (x0 + 30, 26), (x0 + 44, 38)], '#8a2a22', 3)
    save(img, 'at_geta', 'Старые гэта', C, 'b', 20)
    img = canvas(90, 250); line(img, [(45, 4), (45, 150)], '#6a5030', 6); m = fill(img, '#8a7446', 353, poly=[(34, 146), (56, 146), (84, 246), (6, 246)], scale=3, stretch=(.3, 3), contrast=1.3)
    clip(img, m, lambda d: [d.line([(px(45), px(146)), (px(6 + k * 4), px(246))], fill=(50, 36, 16, 120), width=px(1)) for k in range(20)]); rope(img, [(34, 160), (58, 160)], '#b8322a', 3)
    save(img, 'at_hoki', 'Веник хоки', C, 'b', 20)
    img = canvas(120, 70); floor_shadow(img, 60, 64, 56); fill(img, '#6a5034', 354, rect=(10, 36, 110, 64), scale=3); line(img, [(20, 36), (60, 14), (100, 36)], '#3a3a38', 3)
    fill(img, '#d8a040', 355, ell=(52, 44, 68, 56), scale=2); save(img, 'at_nezumitori', 'Мышеловка без мышей', C, 'b', 15)
    img = canvas(160, 380); floor_shadow(img, 80, 374, 60)                                               # ladder
    for x in (30, 124): fill(img, '#5a4228', 356 + x, poly=[(x, 6), (x + 10, 6), (x + 16, 374), (x + 4, 374)], scale=4, stretch=(.3, 4))
    for k in range(9): y = 30 + k * 40; fill(img, '#4a3622', 358 + k, rect=(36, y, 134, y + 10), scale=3, stretch=(4, .5))
    volume(img, (30, 6, 140, 374), .3, .2); save(img, 'at_hashigo', 'Лестница хасиго', C, 'b', 60)
    img = canvas(200, 150); floor_shadow(img, 100, 144, 94)                                               # tsuzura wicker box
    m = fill(img, '#4a3a22', 367, rect=(10, 40, 190, 144), scale=3, contrast=1.3)
    clip(img, m, lambda d: [d.line([(px(x), px(40)), (px(x), px(144))], fill=(20, 14, 8, 130), width=px(1.5)) for x in range(14, 190, 7)])
    fill(img, '#2a1e14', 368, rect=(4, 28, 196, 52), scale=3); text(img, '丸に桔梗', 100, 96, 16, '#c8b070', SERIF); volume(img, (10, 28, 190, 144), .4, .3)
    save(img, 'at_tsuzura', 'Плетёный короб цудзура', C, 'b', 90)
    img = canvas(240, 120); floor_shadow(img, 120, 114, 116)
    blob(img, [(14, 110), (10, 60), (40, 30), (200, 30), (230, 60), (226, 110)], hexc('#5a4a6a'), 369, scale=4)
    for k in range(4): line(img, [(20 + k * 60, 36), (26 + k * 60, 108)], '#3a2e48', 2)
    rope(img, [(70, 30), (70, 112)], '#8a6a3a', 4); rope(img, [(170, 30), (170, 112)], '#8a6a3a', 4); save(img, 'at_futon', 'Свёрнутый старый футон', C, 'b', 60)
    img = canvas(130, 310); floor_shadow(img, 65, 304, 50)                                               # pendulum clock
    fill(img, '#3a2418', 370, rect=(14, 10, 116, 300), scale=5, stretch=(.5, 3)); ell(img, (26, 24, 104, 102), '#d8ccb0'); ImageDraw.Draw(img).ellipse([px(26), px(24), px(104), px(102)], outline=H('#8a6a30'), width=px(3))
    for k in range(12): a = k * math.pi / 6; text(img, '·', 65 + math.cos(a) * 30, 63 + math.sin(a) * 30, 12, '#2a1a10')
    line(img, [(65, 63), (65, 40)], '#1a1210', 2); line(img, [(65, 63), (84, 70)], '#1a1210', 2)
    fill(img, '#20150e', 371, rect=(30, 120, 100, 280), scale=3); glass_ = I.mask_poly(img, rect=(34, 124, 96, 276)); clip(img, glass_, lambda d: d.rectangle([px(34), px(124), px(96), px(276)], fill=(120, 130, 136, 60)))
    line(img, [(65, 128), (58, 230)], '#b8902c', 2); ell(img, (46, 222, 70, 246), '#c8a040'); volume(img, (14, 10, 116, 300), .4, .25)
    save(img, 'at_tokei', 'Часы с маятником', C, 'b', 180)
    img = canvas(150, 130); floor_shadow(img, 75, 124, 66); kiri_box(img, 16, 50, 134, 124, 372, None, cord='#2a4a7a', col='#6a4a30')
    for k in range(6): ell(img, (26 + k * 17, 36, 40 + k * 17, 50), ['#c02a2a', '#e8c040', '#2a4a8a', '#2f6a3a', '#e8e0d0', '#b86a9a'][k])
    save(img, 'at_haribako', 'Шкатулка для рукоделия', C, 'b', 50)
    # finds that only the attic chest gives
    img = canvas(150, 100); floor_shadow(img, 75, 96, 66); fill(img, '#d8ccb0', 380, poly=[(10, 20), (140, 12), (144, 88), (14, 94)], scale=3, contrast=.5)
    poly(img, [(10, 20), (77, 58), (140, 12)], '#c8bca0'); ell(img, (68, 46, 88, 66), '#8a2020'); text(img, '封', 78, 56, 12, '#e8d8c0', SERIF)
    for k in range(3): line(img, [(30, 70 + k * 6), (70 + k * 10, 70 + k * 6)], '#6a5a48', 1)
    save(img, 'at_f_letter', 'Письмо без адреса', C, 'b', 60, src=F, hint=FH)
    img = canvas(150, 100); floor_shadow(img, 75, 96, 60)
    blob(img, [(14, 50), (40, 22), (100, 20), (126, 40), (146, 20), (146, 80), (126, 60), (100, 80), (40, 80)], hexc('#b8402a'), 381, scale=2, spec=.5)
    ell(img, (32, 38, 44, 50), '#f2eee4'); ell(img, (35, 41, 41, 47), '#1a1414')
    for k in range(4): line(img, [(56 + k * 14, 26), (56 + k * 14, 74)], '#e8c040', 2)
    save(img, 'at_f_buriki', 'Жестяная рыбка', C, 'b', 80, src=F, hint=FH)
    img = canvas(130, 110); floor_shadow(img, 65, 104, 56); blob(img, [(20, 104), (16, 60), (50, 40), (80, 40), (114, 60), (110, 104)], hexc('#6a2a4a'), 382, scale=2)
    rope(img, [(46, 44), (84, 44)], '#d8b048', 3)
    for k, c in enumerate(('#6ab0d8', '#e8a0c0', '#a8d890', '#f0d070')): ell(img, (20 + k * 24, 94, 34 + k * 24, 106), c); ImageDraw.Draw(img).ellipse([px(22 + k * 24), px(96), px(28 + k * 24), px(100)], fill=(255, 255, 255, 160))
    save(img, 'at_f_ohajiki', 'Мешочек стекляшек охадзики', C, 'b', 60, src=F, hint=FH)
    img = canvas(130, 160); floor_shadow(img, 65, 156, 56); fill(img, '#2a1a12', 383, rect=(10, 10, 120, 150), scale=3); fill(img, '#9a8e76', 384, rect=(22, 22, 108, 138), scale=4, contrast=.6)
    blob(img, [(40, 138), (46, 90), (64, 80), (82, 90), (88, 138)], hexc('#4a4236'), 385, scale=3, k=.2); ell(img, (52, 52, 76, 82), '#5a5244')
    ImageDraw.Draw(img).polygon([(px(66), px(22)), (px(108), px(22)), (px(108), px(60))], fill=(200, 190, 160, 80)); save(img, 'at_f_photo', 'Старая фотография', C, 'b', 80, src=F, hint=FH)
    img = canvas(110, 140); floor_shadow(img, 55, 136, 46)
    blob(img, [(20, 136), (22, 80), (34, 56), (78, 56), (90, 80), (92, 136)], hexc('#ece6da'), 386, spec=.4); blob(img, [(30, 70), (28, 30), (40, 14), (52, 26), (62, 26), (74, 14), (84, 30), (82, 70)], hexc('#ece6da'), 387, spec=.4)
    poly(img, [(74, 14), (88, 30), (80, 34)], '#ece6da'); ImageDraw.Draw(img).polygon([(px(72), px(14)), (px(84), px(30)), (px(70), px(24))], fill=(90, 80, 70, 255))
    for ex in (44, 68): line(img, [(ex - 5, 44), (ex + 5, 44)], '#1a1414', 2)
    ell(img, (52, 52, 60, 58), '#d87a8a'); ell(img, (30, 90, 50, 110), '#c8a040'); save(img, 'at_f_neko', 'Фарфоровая кошка без уха', C, 'b', 90, src=F, hint=FH)
    img = canvas(150, 120); floor_shadow(img, 75, 116, 70); fill(img, '#4a2418', 388, rect=(12, 50, 138, 116), scale=3); volume(img, (12, 50, 138, 116), .5, .3, spec=.3)
    fill(img, '#5a2c1e', 389, poly=[(12, 50), (138, 50), (150, 10), (24, 10)], scale=3); fill(img, '#c8b890', 390, poly=[(20, 46), (130, 46), (140, 16), (30, 16)], scale=2)
    ell(img, (64, 22, 90, 40), '#d8b048'); text(img, '♪', 76, 30, 14, '#3a2418'); flower = [(40 + k * 18, 84) for k in range(5)]
    for x, y in flower: ell(img, (x - 5, y - 5, x + 5, y + 5), '#e8a0b6')
    save(img, 'at_f_musicbox', 'Музыкальная шкатулка', C, 'b', 120, src=F, hint=FH)


def kura_items():
    C = 'Кура'
    img = canvas(250, 190); floor_shadow(img, 125, 184, 120)
    for k, (cx, cy) in enumerate(((52, 146), (125, 146), (198, 146), (88, 84), (162, 84))): tawara_end(img, cx, cy, 38, 400 + k)
    save(img, 'kr_tawara', 'Рисовые мешки тавара', C, 'b', 90)
    img = canvas(150, 170); floor_shadow(img, 75, 164, 70); komodaru(img, 75, 164, 130, 150, 405); save(img, 'kr_komodaru', 'Бочка сакэ в соломе', C, 'b', 120)
    img = canvas(170, 160); floor_shadow(img, 85, 154, 80); barrel(img, 85, 154, 150, 120, '#6a4a2a', 406, '#2a2018')
    fill(img, '#5a3a1a', 407, ell=(18, 24, 152, 46), scale=3); text(img, '味噌', 85, 104, 26, '#e8dcc0', SERIF); save(img, 'kr_misodaru', 'Бочка мисо', C, 'b', 100)
    img = canvas(150, 190); floor_shadow(img, 75, 184, 64); crock(img, 75, 184, 136, 170, '#5a3a24', 408, lid='#3a2a1c')
    fill(img, '#7a5a3a', 409, rect=(50, 60, 100, 70), scale=2); save(img, 'kr_kame', 'Глиняный кувшин камэ', C, 'b', 70)
    img = canvas(120, 140); floor_shadow(img, 60, 134, 52); crock(img, 60, 134, 104, 110, '#2a3444', 410)
    fill(img, '#d8ccb0', 411, poly=[(30, 22), (90, 22), (96, 34), (24, 34)], scale=2); rope(img, [(26, 30), (94, 30)], '#b8322a', 3); text(img, '梅', 60, 84, 26, '#e8dcc0', SERIF)
    save(img, 'kr_umeboshi', 'Кувшин умэбоси', C, 'b', 60)
    img = canvas(200, 180); floor_shadow(img, 100, 174, 94); kiri_box(img, 10, 96, 190, 174, 412, '茶'); kiri_box(img, 26, 34, 168, 96, 413, '器', col='#a8927a')
    save(img, 'kr_kiribako', 'Ящики из павловнии', C, 'b', 90)
    img = canvas(220, 290); floor_shadow(img, 110, 284, 104)                                             # kaidan-dansu (staircase chest)
    fill(img, '#3c2a1c', 418, poly=[(10, 284), (10, 214), (60, 214), (60, 152), (110, 152), (110, 90), (160, 90), (160, 30), (210, 30), (210, 284)], scale=8, stretch=(3, .5))
    d = ImageDraw.Draw(img)
    for k in range(4):
        y = 214 - k * 62; d.line([(px(10 + k * 50), px(y)), (px(210), px(y))], fill=H('#120c08'), width=px(3)); d.rectangle([px(22 + k * 50), px(y + 20), px(52 + k * 50), px(y + 34)], fill=H('#1a1512'))
        d.line([(px(10 + k * 50), px(y)), (px(10 + k * 50), px(y + 70))], fill=H('#120c08'), width=px(3))
    d.line([(px(110), px(30)), (px(110), px(284))], fill=H('#120c08'), width=px(2)); volume(img, (10, 30, 210, 284), .35, .2)
    save(img, 'kr_tansu', 'Лестничный комод кайдан-дансу', C, 'b', 260)
    img = canvas(240, 170); floor_shadow(img, 120, 164, 114); chest(img, 12, 30, 228, 164, 420, '#4a2a1a', '#2a2420', dusty=False); save(img, 'kr_chest', 'Окованный сундук', C, 'b', 180)
    img = canvas(200, 140); floor_shadow(img, 100, 134, 94); fill(img, '#2a1c14', 421, rect=(10, 40, 190, 134), scale=4)
    for x in (10, 60, 110, 160): fill(img, '#3a3228', 422 + x, rect=(x, 40, x + 30, 134), scale=2)
    fill(img, '#1c140e', 426, rect=(4, 26, 196, 46), scale=3); text(img, '千両', 100, 90, 30, '#c8a040', SERIF); volume(img, (10, 26, 190, 134), .4, .3, spec=.15)
    save(img, 'kr_senryobako', 'Денежный сундук сэнрёбако', C, 'b', 220)
    img = canvas(100, 190); line(img, [(50, 0), (50, 34)], '#1a120c', 2)
    m = fill(img, '#d98c45', 427, ell=(10, 40, 90, 170), scale=3, contrast=1.1, light=.4)
    clip(img, m, lambda d: [d.line([(0, px(40 + k * 13)), (px(100), px(40 + k * 13))], fill=(120, 60, 20, 150), width=px(1.4)) for k in range(1, 10)])
    text(img, '蔵', 50, 104, 34, '#2a1206', SERIF); volume(img, (10, 40, 90, 170), .4, .45)
    for y in (32, 166): fill(img, '#140d09', 428 + y, rect=(26, y, 74, y + 12), scale=2)
    save(img, 'kr_chochin', 'Фонарь хозяина кура', C, 't', 60, [50, 104])
    img = canvas(260, 280); floor_shadow(img, 130, 274, 124)                                             # shelf with jars
    for x in (10, 236): fill(img, '#3a2a1c', 430 + x, rect=(x, 20, x + 14, 274), scale=3, stretch=(.4, 3))
    for k, y in enumerate((100, 180, 260)): fill(img, '#4a3622', 432 + k, rect=(10, y, 250, y + 12), scale=3, stretch=(4, .4))
    for k, (x, y, w, h, c) in enumerate(((30, 100, 60, 70, '#5a3a24'), (100, 100, 50, 56, '#2a3444'), (160, 100, 70, 76, '#6a5a3a'), (30, 180, 80, 70, '#3a3a3a'), (130, 180, 50, 60, '#8a6a4a'), (190, 180, 44, 50, '#2a3444'), (40, 260, 70, 64, '#6a4a2a'), (130, 260, 100, 60, '#4a3222'))):
        crock(img, x + w / 2, y, w, h, c, 435 + k)
    save(img, 'kr_shelf', 'Полка с кувшинами', C, 'b', 150)
    img = canvas(150, 110); floor_shadow(img, 75, 104, 70); fill(img, '#2a1c14', 443, rect=(10, 90, 140, 104), scale=3)
    for k, x in enumerate((36, 76, 116)): crock(img, x, 92, 36, 70 - (k % 2) * 10, ['#d8ccb0', '#3a4a6a', '#d8ccb0'][k], 444 + k)
    ell(img, (56, 94, 70, 102), '#d8ccb0'); save(img, 'kr_tokkuri', 'Кувшинчики токкури', C, 'b', 40)
    img = canvas(160, 100); floor_shadow(img, 80, 94, 76)
    for k, (x, s) in enumerate(((50, 70), (116, 54))):
        fill(img, '#b89868', 447 + k, poly=[(x - s / 2, 94 - s * .8), (x + s / 2, 94 - s * .8), (x + s / 2, 94), (x - s / 2, 94)], scale=3, stretch=(3, .5)); fill(img, '#8a6a40', 449 + k, rect=(x - s / 2 + 5, 94 - s * .8, x + s / 2 - 5, 94 - s * .8 + 8), scale=2)
        text(img, '一升' if k == 0 else '五合', x, 94 - s * .35, s * .22, '#3a2410', SERIF); volume(img, (x - s / 2, 94 - s * .8, x + s / 2, 94), .4, .2)
    save(img, 'kr_masu', 'Мерки для риса масу', C, 'b', 30)
    img = canvas(220, 250); floor_shadow(img, 110, 244, 104); barrel(img, 110, 244, 180, 100, '#6a4a2a', 451, '#3a2a18')     # mochi mortar and mallet
    fill(img, '#2a1c12', 452, ell=(34, 134, 186, 158), scale=3); line(img, [(150, 140), (70, 20)], '#8a6a40', 9); fill(img, '#7a5a34', 453, poly=[(40, 12), (100, 2), (112, 36), (52, 46)], scale=3); volume(img, (40, 2, 112, 46), .5, .3)
    save(img, 'kr_usu', 'Ступа и молот для моти', C, 'b', 140)
    img = canvas(170, 260); line(img, [(85, 0), (85, 30)], '#1a120c', 2); line(img, [(10, 40), (160, 30)], '#6a4a2a', 6)            # steelyard
    for x in (28, 142): line(img, [(x, 40), (x, 60)], '#1a120c', 1.5)
    line(img, [(28, 60), (16, 150)], '#1a120c', 1); line(img, [(28, 60), (40, 150)], '#1a120c', 1); fill(img, '#4a3a24', 454, ell=(6, 142, 50, 162), scale=2)
    line(img, [(142, 36), (142, 190)], '#1a120c', 1.5); fill(img, '#3a3632', 455, poly=[(130, 190), (154, 190), (148, 230), (136, 230)], scale=2); volume(img, (130, 190, 154, 230), .5, .3, spec=.3)
    save(img, 'kr_hakari', 'Весы-безмен', C, 't', 60)
    img = canvas(190, 80); floor_shadow(img, 95, 74, 90); fill(img, '#2a1a10', 456, rect=(8, 14, 182, 72), scale=3); line(img, [(8, 32), (182, 32)], '#1a100a', 3)
    for k in range(13):
        x = 20 + k * 13; line(img, [(x, 16), (x, 70)], '#6a4a2a', 1.5); ell(img, (x - 5, 18, x + 5, 28), '#4a2a1a')
        for j in range(4): ell(img, (x - 5, 38 + j * 8, x + 5, 46 + j * 8), '#4a2a1a')
    save(img, 'kr_soroban', 'Счёты соробан', C, 'b', 40)
    img = canvas(130, 210); line(img, [(65, 0), (65, 24)], '#1a120c', 2); fill(img, '#d8ccb0', 457, rect=(14, 24, 116, 200), scale=4, contrast=.5)
    fill(img, '#2a3a6a', 458, rect=(14, 24, 116, 40), scale=2); 
    for k, ch in enumerate('大福帳'): text(img, ch, 65, 80 + k * 34, 28, '#1a1210', SERIF, True)
    volume(img, (14, 24, 116, 200), .3, .2); save(img, 'kr_daifukucho', 'Торговая книга дайфукутё', C, 't', 50)
    img = canvas(200, 250); floor_shadow(img, 100, 244, 94); chest(img, 20, 150, 180, 244, 459, '#1a1414', '#6a5a3a', lid=18, dusty=False)       # armour chest with kabuto
    blob(img, [(40, 150), (44, 110), (70, 80), (130, 80), (156, 110), (160, 150)], hexc('#2a2622'), 460, spec=.3)
    for k in range(3): line(img, [(40 + k * 4, 126 + k * 10), (160 - k * 4, 126 + k * 10)], '#b8322a', 3)
    poly(img, [(100, 84), (60, 20), (80, 22), (100, 60), (120, 22), (140, 20)], '#c8a040'); save(img, 'kr_yoroibitsu', 'Доспехи предков в ящике', C, 'b', 280)
    img = canvas(140, 60); floor_shadow(img, 70, 56, 64); rope(img, [(8, 30), (132, 30)], '#b8322a', 2)
    for k in range(14): x = 14 + k * 8.6; fill(img, '#8a6a30', 461 + k, ell=(x - 7, 16, x + 7, 44), scale=1.5); ImageDraw.Draw(img).rectangle([px(x - 2), px(27), px(x + 2), px(33)], fill=H('#2a1a0a'))
    save(img, 'kr_zeni', 'Связка монет мон', C, 'b', 40)
    img = canvas(150, 210); line(img, [(75, 0), (75, 16)], '#1a120c', 2); fill(img, '#e0d6c0', 475, rect=(10, 16, 140, 200), scale=4, contrast=.5)                # neko-e: a cat picture against mice
    blob(img, [(40, 170), (44, 110), (60, 84), (98, 84), (112, 110), (116, 170)], hexc('#2a2420'), 476, scale=2, k=.2); blob(img, [(56, 96), (54, 60), (62, 44), (70, 56), (86, 56), (94, 44), (100, 60), (98, 96)], hexc('#2a2420'), 477, scale=2, k=.2)
    for ex in (68, 86): ell(img, (ex - 4, 68, ex + 4, 76), '#d8b048')
    line(img, [(114, 160), (130, 130), (124, 110)], '#2a2420', 6); text(img, '猫', 30, 44, 22, '#8a2020', SERIF, True); save(img, 'kr_nekoe', 'Картина с кошкой от мышей', C, 't', 60)
    img = canvas(180, 150); floor_shadow(img, 90, 144, 84); blob(img, [(14, 144), (18, 60), (60, 30), (120, 30), (162, 60), (166, 144)], hexc('#6a5a3e'), 478, scale=3)
    clip(img, I.mask_poly(img, rect=(0, 0, 180, 150)), lambda d: [d.line([(0, px(y)), (px(180), px(y + 4))], fill=(40, 30, 16, 90), width=px(1)) for y in range(30, 150, 6)])
    for k in range(9): x, y = 50 + (k * 37) % 80, 30 + (k * 13) % 14; ell(img, (x - 10, y - 8, x + 10, y + 8), '#141210')
    save(img, 'kr_sumi', 'Мешок древесного угля', C, 'b', 30)
    img = canvas(170, 150); floor_shadow(img, 85, 144, 80); barrel(img, 85, 144, 150, 100, '#8a6a40', 479, '#2a4a2a'); fill(img, '#3a2a1c', 480, ell=(16, 36, 154, 56), scale=3)
    line(img, [(40, 46), (60, 10), (110, 10), (130, 46)], '#6a4a2a', 5); save(img, 'kr_oke', 'Деревянная кадка', C, 'b', 40)
    img = canvas(140, 170); line(img, [(70, 0), (70, 24)], '#2a2420', 3)                                   # ebisu-jo padlock
    line(img, [(40, 70), (40, 40), (70, 22), (100, 40), (100, 70)], '#2a2420', 10); fill(img, '#3a3228', 481, rect=(16, 64, 124, 164), scale=4, contrast=1.3); volume(img, (16, 64, 124, 164), .5, .35, spec=.2)
    fill(img, '#8a6a30', 482, rect=(26, 80, 114, 90), scale=2); ell(img, (62, 104, 78, 120), '#0a0806'); save(img, 'kr_jo', 'Старинный замок эбису-дзё', C, 't', 70)
    img = canvas(170, 280); rope(img, [(10, 14), (85, 24), (160, 14)], '#6a5634', 3)
    for k, x in enumerate((44, 86, 128)): hanging_string(img, x, 20, 270, 'daikon', 483 + k, 4)
    save(img, 'kr_daikon', 'Вяленый дайкон на верёвке', C, 't', 30)
    img = canvas(150, 110); floor_shadow(img, 75, 104, 70); fill(img, '#1a1010', 486, rect=(10, 34, 140, 104), scale=3); volume(img, (10, 34, 140, 104), .5, .3, spec=.4)
    fill(img, '#2a1414', 487, rect=(4, 22, 146, 40), scale=3); line(img, [(30, 70), (60, 50), (90, 64), (120, 46)], '#c8a040', 2); ell(img, (56, 44, 66, 54), '#c8a040'); ell(img, (86, 58, 96, 68), '#c8a040')
    save(img, 'kr_tebako', 'Лаковая шкатулка тэбако', C, 'b', 90)
    img = canvas(200, 150); floor_shadow(img, 100, 144, 94)
    for k, y in enumerate((96, 50)): fill(img, '#6a6a64', 488 + k, ell=(12, y, 188, y + 48), scale=4, contrast=1.3); fill(img, '#5a5a54', 490 + k, rect=(12, y + 24, 188, y + 44 + (k == 0) * 4), scale=4); volume(img, (12, y, 188, y + 48), .4, .3)
    ell(img, (90, 60, 110, 72), '#1a1a18'); line(img, [(160, 70), (190, 20)], '#6a4a2a', 7); save(img, 'kr_ishiusu', 'Каменные жернова', C, 'b', 110)
    img = canvas(160, 140); floor_shadow(img, 80, 134, 74); crock(img, 80, 134, 150, 90, '#3a3632', 492)
    fill(img, '#8a8278', 493, ell=(20, 44, 140, 64), scale=3); specks(img, (34, 30, 126, 56), 30, '#e07030', 494, (1.5, 3), (160, 240)); glow(img, 80, 50, 40, hexc('#ff8040'), .3)
    save(img, 'kr_hibachi', 'Жаровня хибати', C, 'b', 90)
    img = canvas(140, 140); floor_shadow(img, 70, 134, 60); blob(img, [(20, 130), (14, 84), (40, 56), (100, 56), (126, 84), (120, 130)], hexc('#2a2a28'), 495, spec=.3)
    clip(img, I.mask_poly(img, rect=(0, 50, 140, 134)), lambda d: [d.ellipse([px(x - 3), px(y - 3), px(x + 3), px(y + 3)], fill=(60, 60, 56, 255)) for x in range(24, 120, 10) for y in range(66, 126, 10)])
    line(img, [(30, 60), (70, 14), (110, 60)], '#1a1a18', 5); line(img, [(118, 90), (138, 70)], '#2a2a28', 8); save(img, 'kr_tetsubin', 'Чугунный чайник тэцубин', C, 'b', 60)
    img = canvas(140, 170); floor_shadow(img, 70, 164, 62); barrel(img, 70, 164, 110, 130, '#5a3a24', 496, '#1a1410'); fill(img, '#e0d6c0', 497, rect=(44, 70, 96, 130), scale=2); text(img, '醤油', 70, 100, 18, '#1a1210', SERIF)
    save(img, 'kr_shoyu', 'Бочонок соевого соуса', C, 'b', 70)
    img = canvas(120, 90); floor_shadow(img, 60, 84, 50); blob(img, [(20, 84), (22, 50), (50, 30), (90, 36), (104, 84)], hexc('#8a7648'), 498, scale=2)   # straw nest the mice left
    specks(img, (30, 60, 96, 80), 40, '#e8e0cc', 499, (1, 2), (140, 220)); straws(img, (10, 30, 110, 84), 60, 500)
    save(img, 'kr_komebukuro', 'Мешочек риса', C, 'b', 20)
    img = canvas(120, 270); floor_shadow(img, 60, 264, 40); fill(img, '#1a1a1a', 501, rect=(20, 30, 100, 264), scale=3)          # folded screen
    for k in range(4): fill(img, ['#b8a878', '#a89868'][k % 2], 502 + k, rect=(24 + k * 19, 36, 40 + k * 19, 258), scale=4, contrast=.6)
    P.dab_mass(ImageDraw.Draw(img), [(px(60), px(120), px(30), px(40))], 160, 'leaf', [hexc('#3a4a2a'), hexc('#4a5a34'), hexc('#6a7a44')], random.Random(506), size=(2, 4))
    save(img, 'kr_byobu', 'Сложенная ширма', C, 'b', 110)


if __name__ == '__main__':
    os.makedirs(PREV, exist_ok=True)
    what = sys.argv[2:] or ['attic', 'kura', 'boards', 'items']
    for n in ('attic', 'kura'):
        if n in what:
            globals()[n]()
            pv = os.path.join(OUT, f'preview-{n}.jpg')
            if os.path.exists(pv): shutil.move(pv, os.path.join(PREV, f'preview-{n}.jpg'))
    meta = json.load(open(os.path.join(HERE, 'rooms_art.json'))) if os.path.exists(os.path.join(HERE, 'rooms_art.json')) else {}
    if 'boards' in what: boards_sheet(); meta['spr'] = SPR
    if 'items' in what:
        attic_items(); kura_items(); meta['atl'] = {'att': pack('Чердак', 'att'), 'kra': pack('Кура', 'kra')}; meta['items'] = ROWS
        print('items', len(ROWS), {c: sum(1 for r in ROWS if r['c'] == c) for c in ('Чердак', 'Кура')})
    json.dump(meta, open(os.path.join(HERE, 'rooms_art.json'), 'w'), ensure_ascii=False)
