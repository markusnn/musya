#!/usr/bin/env python3
"""«Чайная церемония» (add-on tea, feat/tea.js): the painted tatami for the ceremony mini-game and one atlas with
6 collectible tea things (side view) + the utensils seen from above for the game + a travel tea box for the veranda.
Usage: cd art && python3 tea_art.py ../assets
  → ../assets/bg/te_mat.webp (900×1500), ../assets/items/atlas_te.webp; rect map printed as JSON (pasted into feat/tea.js)
  previews → art/out/tea/"""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
ASSETS = os.path.abspath(sys.argv[1]); HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv[1] = os.path.join(ASSETS, 'items')
import paint as P
from paint import hexc, mixc, fbm
import items as I
from items import px, canvas, fill, volume, soft, floor_shadow, line, ell, poly, text, H, dk, lt, mask_poly, SERIF
PREV = os.path.join(HERE, 'out', 'tea'); os.makedirs(PREV, exist_ok=True)
SPR = {}     # name -> RGBA image (final size)


def grain(im, seed, amt=3.2, sat=.9):
    a = np.asarray(im, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * sat
    a[..., :3] += np.random.default_rng(seed).normal(0, amt, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def keep(name, img, seed=1):
    """A canvas() picture at 2x → final size, slight desaturation + grain."""
    SPR[name] = grain(img.resize((P.W, P.H), Image.LANCZOS), seed)


# ───────────── top-down discs in numpy (the game sees the utensils from above) ─────────────
def disc_xy(n):
    y, x = np.mgrid[0:n, 0:n].astype(np.float32); c = (n - 1) / 2
    return (x - c) / c, (y - c) / c


def aa(r, R, n):   # anti-aliased inside of radius R
    return np.clip((R - r) * n / 2.4 + .5, 0, 1)


def cmix(a, b, t):
    a = np.array(H(a)[:3], np.float32); b = np.array(H(b)[:3], np.float32); t = np.asarray(t, np.float32)[..., None]
    return a + (b - a) * t


def rgba(rgb, al):
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), np.clip(al * 255, 0, 255)]).astype(np.uint8), 'RGBA')


def top_bowl(size=260, seed=3):
    n = size * 2; x, y = disc_xy(n); r = np.hypot(x, y); ang = np.arctan2(y, x)
    N = fbm(n, n, 40, 5, seed); F = fbm(n, n, 8, 3, seed + 5)
    body = cmix('#16130f', '#3a332c', np.clip(N * .9 + F * .3 - .2, 0, 1))                       # raku black, mottled
    crest = np.exp(-((r - .925) / .03) ** 2)                                                       # the rim's lip
    rgb = body + crest[..., None] * 34
    cav = r < .86; wall = np.clip((r - .55) / .31, 0, 1)
    inner = cmix('#0d0b09', '#2a241e', wall * .8 + N * .25)
    rgb = np.where(cav[..., None], inner, rgb)
    rgb -= (np.exp(-((r - .86) / .02) ** 2) * 30)[..., None]                                       # the inner edge in shadow
    # the front (shōmen): an amber glaze drip at the bottom and a gold kintsugi seam
    da = np.angle(np.exp(1j * (ang - math.pi / 2)))
    edge = .76 + .16 * (np.abs(da) / .28) ** 2 + .025 * np.sin(ang * 9 + 1)                   # a soft amber pool over the rim
    drip = np.clip((.28 - np.abs(da)) * 40, 0, 1) * np.clip((r - edge) * 40, 0, 1) * np.clip((1.0 - r) * 60, 0, 1)
    rgb = rgb * (1 - drip[..., None]) + cmix('#6a3a16', '#c8863a', np.clip(F * .7 + (r - .8) * 2, 0, 1)) * drip[..., None]
    al = aa(r, 1, n)
    img = rgba(rgb, al)
    d = ImageDraw.Draw(img); rr = random.Random(seed); pts = []; a0 = 2.25; rad = 1.0
    while rad > .5: pts.append(((math.cos(a0) * rad + 1) * n / 2, (math.sin(a0) * rad + 1) * n / 2)); rad -= .07; a0 += rr.uniform(-.1, .12)
    d.line(pts, fill=(214, 172, 74, 255), width=5, joint='curve'); d.line(pts, fill=(255, 226, 150, 200), width=2)
    return grain(img.resize((size, size), Image.LANCZOS), seed)


def top_natsume(size=150, seed=7):
    n = size * 2; x, y = disc_xy(n); r = np.hypot(x, y); N = fbm(n, n, 30, 4, seed)
    rgb = cmix('#5a1a12', '#8a2e1c', N)                                    # negoro: red lacquer, black worn through
    worn = fbm(n, n, 14, 4, seed + 3) > .7
    rgb = np.where(worn[..., None], cmix('#120c0a', '#2a1a14', N), rgb)
    rgb += (np.exp(-((r - .9) / .025) ** 2) * 40)[..., None] - (np.exp(-((r - .86) / .02) ** 2) * 50)[..., None]
    spec = np.exp(-(((x + .38) / .26) ** 2 + ((y + .42) / .16) ** 2)) * 120
    rgb += spec[..., None]
    img = rgba(rgb, aa(r, 1, n)); d = ImageDraw.Draw(img); c = n / 2
    # gold: an autumn moon and susuki grass
    d.ellipse([c + .05 * c, c - .55 * c, c + .5 * c, c - .1 * c], fill=(220, 178, 80, 255)); d.ellipse([c + .16 * c, c - .62 * c, c + .6 * c, c - .18 * c], fill=None)
    mm = Image.new('L', img.size, 0); ImageDraw.Draw(mm).ellipse([c + .16 * c, c - .62 * c, c + .6 * c, c - .18 * c], fill=255)
    a = np.asarray(img).copy(); m2 = np.asarray(mm) > 0
    a[m2] = np.asarray(rgba(rgb, aa(r, 1, n)))[m2]; img = Image.fromarray(a, 'RGBA'); d = ImageDraw.Draw(img)
    for k in range(6):
        bx = c - .55 * c + k * .1 * c; pts = [(bx + (j / 8) ** 2 * (.25 + k * .05) * c, c + .7 * c - j / 8 * (.75 + .1 * (k % 3)) * c) for j in range(9)]
        d.line(pts, fill=(214, 170, 72, 230), width=3, joint='curve')
    return grain(img.resize((size, size), Image.LANCZOS), seed)


def top_kama(size=320, seed=11):
    n = size * 2; x, y = disc_xy(n); x = x / .84; y = y / .84; r = np.hypot(x, y); N = fbm(n, n, 30, 4, seed)
    rgb = cmix('#1c1a18', '#3e3a35', N * .8)
    # arare bumps in rings
    bump = np.zeros_like(r)
    for k, rad in enumerate((.62, .7, .78, .86, .94)):
        cnt = int(rad * 34); ph = (np.arctan2(y, x) * cnt / (2 * math.pi) + k * .5) % 1
        bump += np.exp(-((ph - .5) / .18) ** 2) * np.exp(-((r - rad) / .03) ** 2)
    rgb += bump[..., None] * 38
    rgb = np.where((r < .52)[..., None], cmix('#141210', '#2a2622', N), rgb)                    # the lid
    rgb += (np.exp(-((r - .52) / .015) ** 2) * 50)[..., None]
    rgb = np.where((r < .12)[..., None], cmix('#5a4a2c', '#a88a50', np.clip(.5 - x * 2 - y * 2, 0, 1)), rgb)  # bronze knob
    rgb += (np.exp(-(((x + .3) / .3) ** 2 + ((y + .35) / .2) ** 2)) * 46)[..., None]
    img = rgba(rgb, aa(r, 1, n * .84)); d = ImageDraw.Draw(img); c = n / 2
    for sx in (-1, 1):   # the kan rings
        cx = c + sx * .9 * c; d.ellipse([cx - .1 * c, c - .16 * c, cx + .1 * c, c + .16 * c], outline=(60, 56, 50, 255), width=int(.035 * c))
        d.ellipse([cx - .1 * c, c - .16 * c, cx + .1 * c, c + .16 * c], outline=(110, 104, 96, 160), width=int(.01 * c))
    return grain(img.resize((size, size), Image.LANCZOS), seed)


def top_ring_bowl(size, seed, outer, inner, rim=.85, spots=None, lid=None):
    n = size * 2; x, y = disc_xy(n); r = np.hypot(x, y); N = fbm(n, n, 26, 4, seed)
    rgb = cmix(dk(H(outer), .3), lt(H(outer), .15), N)
    rgb += (np.exp(-((r - (rim + 1) / 2) / .03) ** 2) * 30)[..., None]
    if lid:
        rgb = np.where((r < rim)[..., None], cmix(lid, lt(H(lid), .12), N * .6), rgb)
        rgb += (np.exp(-(((x + .3) / .28) ** 2 + ((y + .4) / .15) ** 2)) * 90 * (r < rim))[..., None]
    else:
        rgb = np.where((r < rim)[..., None], cmix(inner, lt(H(inner), .1), np.clip((r / rim) ** 3 + N * .2, 0, 1)), rgb)
    rgb -= (np.exp(-((r - rim) / .02) ** 2) * 30)[..., None]
    img = rgba(rgb, aa(r, 1, n))
    if spots:
        d = ImageDraw.Draw(img); rr = random.Random(seed); c = n / 2
        for _ in range(26):
            a = rr.uniform(0, 6.3); rad = rr.uniform(rim + .02, .97) * c; s = rr.uniform(2, 6)
            d.ellipse([c + math.cos(a) * rad - s, c + math.sin(a) * rad - s, c + math.cos(a) * rad + s, c + math.sin(a) * rad + s], fill=H(spots))
        if lid: d.ellipse([c - .1 * c, c - .1 * c, c + .1 * c, c + .1 * c], fill=(30, 24, 18, 255))
    return grain(img.resize((size, size), Image.LANCZOS).filter(ImageFilter.GaussianBlur(.4)), seed)


def top_chasen(size=130, seed=13):
    n = size * 2; img = Image.new('RGBA', (n, n), (0, 0, 0, 0)); d = ImageDraw.Draw(img); c = n / 2; rr = random.Random(seed)
    for k in range(80):   # outer tines curl outwards
        a = k / 80 * 2 * math.pi; col = mixc(H('#efe4bc'), H('#a8945c'), rr.random() * .6)
        d.line([(c + math.cos(a) * .4 * c, c + math.sin(a) * .4 * c), (c + math.cos(a + .05) * .8 * c, c + math.sin(a + .05) * .8 * c), (c + math.cos(a + .14) * .97 * c, c + math.sin(a + .14) * .97 * c)], fill=col, width=3, joint='curve')
    d.ellipse([c - .42 * c, c - .42 * c, c + .42 * c, c + .42 * c], fill=(70, 58, 34, 255))
    for k in range(40):   # inner tines bundle
        a = k / 40 * 2 * math.pi; d.line([(c, c), (c + math.cos(a) * .36 * c, c + math.sin(a) * .36 * c)], fill=mixc(H('#e2d6a8'), H('#9a8650'), rr.random()), width=3)
    d.ellipse([c - .1 * c, c - .1 * c, c + .1 * c, c + .1 * c], fill=(200, 184, 130, 255))
    return grain(img.resize((size, size), Image.LANCZOS), seed)


def top_hishaku(seed=17):
    W0, H0 = 420, 96; n = 2; img = Image.new('RGBA', (W0 * n, H0 * n), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    cy = H0 / 2 * n
    d.line([(8 * n, cy + 3 * n), (338 * n, cy)], fill=H('#9a8650'), width=10 * n)
    d.line([(8 * n, cy + 1 * n), (338 * n, cy - 2 * n)], fill=H('#d8c48c'), width=3 * n)
    for xk in (120, 250): d.line([(xk * n, cy - 5 * n), (xk * n, cy + 6 * n)], fill=H('#6a5a30'), width=2 * n)
    cx, R = 372 * n, 42 * n
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=H('#b49c5c')); d.ellipse([cx - R + 7 * n, cy - R + 7 * n, cx + R - 7 * n, cy + R - 7 * n], fill=H('#3a3018'))
    d.arc([cx - R + 2 * n, cy - R + 2 * n, cx + R - 2 * n, cy + R - 2 * n], 200, 300, fill=H('#e8d8a0'), width=3 * n)
    return grain(img.resize((W0, H0), Image.LANCZOS), seed)


def top_chashaku(seed=19):
    W0, H0 = 300, 44; n = 2; img = Image.new('RGBA', (W0 * n, H0 * n), (0, 0, 0, 0)); cy = H0 / 2
    top = [(6 + i * 2.6, cy - (4 + 3 * (i / 100))) for i in range(101)]; bot = [(6 + i * 2.6, cy + (4 + 3 * (i / 100))) for i in range(101)]
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).polygon([(px * n, py * n) for px, py in top + bot[::-1]], fill=255)
    ImageDraw.Draw(m).ellipse([(268) * n, (cy - 9) * n, 296 * n, (cy + 9) * n], fill=255)
    N = fbm(img.width, img.height, 6, 3, seed, (8, 1)); rgb = cmix('#8a6a34', '#d4b878', N)
    xs = np.arange(img.width)[None, :] / n
    rgb -= (np.exp(-((xs - 140) / 3) ** 2) * 60)[..., None]           # the node
    rgb += (np.exp(-((np.arange(img.height)[:, None] / n - cy + 2) / 1.6) ** 2) * 40)[..., None]
    img = rgba(rgb, np.asarray(m, np.float32) / 255)
    ImageDraw.Draw(img).ellipse([(274) * n, (cy - 6) * n, 292 * n, (cy + 6) * n], fill=H('#6a4e24'))
    return grain(img.resize((W0, H0), Image.LANCZOS), seed)


def top_fukusa(seed=23):
    W0, H0 = 150, 104; img = canvas(W0, H0)
    fill(img, '#9a3424', seed, poly=[(6, 10), (144, 6), (146, 96), (4, 98)], scale=10, contrast=.8, dark=.35, light=.25)
    fill(img, '#b8462e', seed + 1, poly=[(6, 10), (144, 6), (145, 50), (5, 54)], scale=10, contrast=.8, dark=.3, light=.3)
    line(img, [(5, 54), (145, 50)], '#5a1a10', 2.2); line(img, [(6, 57), (146, 53)], '#d8705a', 1)
    soft(img, lambda d: [d.line([(px(10 + k * 22), px(12)), (px(-10 + k * 22), px(96))], fill=(255, 210, 190, 26), width=px(6)) for k in range(8)], 3)
    volume(img, (4, 6, 146, 98), .4, .3, spec=.2)
    keep('g_fukusa', img, seed); return SPR.pop('g_fukusa')


def wagashi(seed=29):
    img = canvas(140, 112)
    fill(img, '#e8e2d2', seed, poly=[(8, 40), (118, 18), (134, 82), (22, 106)], scale=12, contrast=.4, dark=.15, light=.1)
    fill(img, '#f4efe2', seed + 1, poly=[(16, 34), (124, 26), (128, 86), (14, 98)], scale=12, contrast=.4, dark=.12, light=.08)
    floor_shadow(img, 72, 84, 44, 90)
    c = (72, 58); pts = []
    for k in range(60):   # a maple leaf of nerikiri
        a = -math.pi / 2 + k / 60 * 2 * math.pi; lobe = .55 + .45 * abs(math.cos(a * 2.5 + math.pi / 4)) ** .6
        pts.append((c[0] + math.cos(a) * 46 * lobe, c[1] + math.sin(a) * 38 * lobe))
    fill(img, '#c8502a', seed + 2, poly=pts, scale=6, contrast=.7, dark=.35, light=.3)
    soft(img, lambda d: d.ellipse([px(52), px(40), px(92), px(76)], fill=(250, 170, 70, 140)), 7)
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5; line(img, [c, (c[0] + math.cos(a) * 30, c[1] + math.sin(a) * 25)], '#8a2a14', 1.1)
    volume(img, (24, 18, 120, 98), .5, .3, spec=.25)
    keep('g_wagashi', img, seed); return SPR.pop('g_wagashi')


def chabako(seed=31):
    img = canvas(240, 170); floor_shadow(img, 120, 164, 112)
    fill(img, '#b8946a', seed, poly=[(30, 70), (190, 70), (190, 160), (30, 160)], scale=5, stretch=(4, 1), contrast=1.1, dark=.35, light=.25)
    fill(img, '#8a6a46', seed + 1, poly=[(190, 70), (214, 56), (214, 146), (190, 160)], scale=5, contrast=1.1)
    fill(img, '#d0ac80', seed + 2, poly=[(30, 70), (190, 70), (214, 56), (54, 56)], scale=5, stretch=(4, 1), contrast=.9, dark=.25)
    line(img, [(30, 84), (190, 84), (214, 70)], '#5a4028', 1.6)
    for (pts, w) in (([(110, 70), (110, 160)], 5), ([(30, 112), (190, 112)], 5)): line(img, pts, '#5a2a5a', w)
    line(img, [(122, 62), (110, 70), (98, 60)], '#5a2a5a', 5); ell(img, (102, 56, 118, 72), '#6a3a6a')
    # a small bowl beside the box and a folded fukusa
    fill(img, '#201c18', seed + 3, poly=[(170 - 160 + 150, 132), (232, 132), (226, 162), (162, 162)], scale=4, contrast=1.3)
    ell(img, (150, 124, 234, 140), '#3a322a'); ell(img, (156, 127, 228, 138), '#4a6a28')
    fill(img, '#b8462e', seed + 4, poly=[(6, 150), (40, 144), (46, 162), (10, 166)], scale=6, contrast=.8)
    volume(img, (6, 56, 234, 166), .4, .3, spec=.15)
    keep('g_chabako', img, seed); return SPR.pop('g_chabako')


# ───────────── the 6 collectible things (side view, like the rest of the room items) ─────────────
ROWS = []


def item(img, iid, name, price):
    keep(iid, img, sum(map(ord, iid))); ROWS.append({'id': iid, 'n': name, 'c': 'Чайная церемония', 'w': P.W, 'h': P.H, 'a': 'b', 'p': price})


def side_bowl(img, cx, top, w, h, glaze, seed):
    g = H(glaze)
    fill(img, dk(g, .35), seed + 1, poly=[(cx - w * .2, top + h * .86), (cx + w * .2, top + h * .86), (cx + w * .18, top + h), (cx - w * .18, top + h)], scale=4)
    body = [(cx - w / 2, top), (cx - w * .05, top - 3), (cx + w / 2, top + 2), (cx + w * .48, top + h * .5), (cx + w * .34, top + h * .9), (cx - w * .3, top + h * .88), (cx - w * .49, top + h * .5)]
    return fill(img, g, seed, poly=body, scale=5, contrast=1.5, dark=.5, light=.35)


def build_items():
    # 1 raku bowl: black, thick, with an amber drip and a gold kintsugi seam
    img = canvas(180, 130); floor_shadow(img, 90, 124, 74); m = side_bowl(img, 90, 30, 158, 92, '#24201c', 41)
    soft(img, lambda d: d.polygon([(px(100), px(32)), (px(124), px(32)), (px(120), px(70)), (px(112), px(84)), (px(104), px(66))], fill=(196, 128, 56, 230)), 1.2)
    line(img, [(52, 34), (58, 56), (54, 74), (62, 98)], '#d8b048', 2.2)
    volume(img, (10, 28, 170, 122), .55, .38, spec=.45)
    ImageDraw.Draw(img).ellipse([px(11), px(22), px(169), px(40)], fill=H('#141210')); ImageDraw.Draw(img).ellipse([px(17), px(25), px(163), px(38)], fill=H('#0c0a08'))
    item(img, 'te_raku', 'Чаван раку с золотым швом', 120)
    # 2 natsume under red negoro lacquer
    img = canvas(130, 124); floor_shadow(img, 65, 118, 56)
    fill(img, '#7a2216', 42, rect=(14, 40, 116, 116), scale=5, contrast=.9, dark=.4, light=.3)
    fill(img, '#16100c', 43, ell=(30, 74, 70, 108), scale=4); fill(img, '#16100c', 44, ell=(84, 52, 110, 92), scale=4)
    ImageDraw.Draw(img).ellipse([px(14), px(26), px(116), px(54)], fill=H('#8a2a1a')); line(img, [(14, 56), (116, 56)], '#2a0e08', 2)
    ell(img, (70, 30, 92, 44), '#d8b048'); ell(img, (76, 28, 96, 42), '#8a2a1a')
    volume(img, (14, 26, 116, 116), .45, .45, spec=.55)
    item(img, 'te_natsume', 'Нацумэ под красным лаком', 110)
    # 3 a chasen on its ceramic holder (kusenaoshi)
    img = canvas(120, 190); floor_shadow(img, 60, 184, 46)
    fill(img, '#d8d0c0', 45, poly=[(34, 184), (86, 184), (80, 150), (40, 150)], scale=4, contrast=.5); volume(img, (34, 150, 86, 184), .5, .3, spec=.3)
    fill(img, '#4a6a5a', 46, rect=(38, 160, 82, 166), scale=3)
    rr = random.Random(47)
    for k in range(40):
        a = -1.3 + 2.6 * k / 39; x0, y0 = 60 + math.sin(a) * 44, 92 + (1 - math.cos(a)) * 34
        line(img, [(60 + math.sin(a) * 12, 150), (x0, y0 + 8), (60 + math.sin(a) * 22, 46)], mixc(H('#e4d6a4'), H('#a89860'), rr.random()), 1.2)
    fill(img, '#c8b880', 48, rect=(50, 104, 70, 152), scale=3); line(img, [(50, 112), (70, 112)], '#2a1a10', 3)
    item(img, 'te_chasen', 'Бамбуковый тясэн на подставке', 50)
    # 4 a folded silk fukusa
    img = canvas(170, 96); floor_shadow(img, 85, 88, 76)
    fill(img, '#8a2c22', 49, poly=[(12, 50), (140, 34), (162, 64), (30, 84)], scale=8, contrast=.8, dark=.35, light=.3)
    fill(img, '#b8462e', 50, poly=[(12, 50), (140, 34), (146, 44), (18, 62)], scale=8, contrast=.8, dark=.3, light=.35)
    line(img, [(18, 62), (146, 44)], '#5a1810', 1.6)
    soft(img, lambda d: [d.line([(px(30 + k * 26), px(40)), (px(46 + k * 26), px(80))], fill=(255, 210, 190, 34), width=px(5)) for k in range(5)], 2.5)
    fill(img, '#d8b048', 51, ell=(118, 40, 128, 48), scale=2)
    volume(img, (12, 34, 162, 84), .4, .3, spec=.2)
    item(img, 'te_fukusa', 'Шёлковая фукуса', 60)
    # 5 sweets on a lacquer tray: a maple leaf, a chrysanthemum and a little moon rabbit
    img = canvas(230, 120); floor_shadow(img, 115, 112, 104)
    fill(img, '#1a120e', 52, poly=[(10, 64), (220, 64), (206, 108), (24, 108)], scale=5, contrast=1.1); fill(img, '#2a1a12', 53, ell=(10, 50, 220, 80), scale=5)
    ImageDraw.Draw(img).ellipse([px(18), px(54), px(212), px(76)], fill=H('#3a2216'))
    pts = []
    for k in range(40):
        a = -math.pi / 2 + k / 40 * 2 * math.pi; lobe = .55 + .45 * abs(math.cos(a * 2.5 + math.pi / 4)) ** .6; pts.append((60 + math.cos(a) * 30 * lobe, 54 + math.sin(a) * 18 * lobe))
    fill(img, '#c8502a', 54, poly=pts, scale=4, contrast=.7); volume(img, (30, 34, 90, 72), .5, .3, spec=.3)
    fill(img, '#e8c040', 55, ell=(94, 36, 136, 70), scale=3, contrast=.7)
    for k in range(12): a = k / 12 * 2 * math.pi; line(img, [(115, 53), (115 + math.cos(a) * 19, 53 + math.sin(a) * 15)], '#b88a20', 1)
    volume(img, (94, 36, 136, 70), .5, .3, spec=.3)
    fill(img, '#f4f0e6', 56, ell=(148, 38, 196, 70), scale=3, contrast=.4); fill(img, '#f4f0e6', 57, poly=[(158, 42), (154, 20), (162, 22), (166, 42)], scale=2)
    fill(img, '#f4f0e6', 58, poly=[(170, 42), (172, 20), (180, 24), (176, 42)], scale=2)
    ell(img, (176, 48, 180, 52), '#c02020'); volume(img, (148, 20, 196, 70), .5, .3, spec=.35)
    item(img, 'te_kashi', 'Осенние вагаси на лаковом подносе', 80)
    # 6 a scroll: a single ensō circle and «一期一会»
    img = canvas(130, 430)
    line(img, [(35, 12), (65, 2), (95, 12)], '#1a120c', 1.4); fill(img, '#2a1c14', 1, rect=(12, 10, 118, 20), scale=3)
    fill(img, '#4a3a2a', 59, rect=(14, 18, 116, 408), scale=6, contrast=1.1)
    fill(img, '#e8dec6', 60, rect=(24, 70, 106, 350), scale=8, contrast=.6, dark=.12, light=.1)
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l); rr = random.Random(61)
    for k in range(70):
        a = 1.9 + k / 70 * 5.6; w = 9 * (1 - k / 90) + rr.uniform(-1, 1); x, y = 65 + math.cos(a) * 30, 150 + math.sin(a) * 30
        d.ellipse([px(x - w / 2), px(y - w / 2), px(x + w / 2), px(y + w / 2)], fill=(24, 18, 14, 230 - k))
    img.alpha_composite(l.filter(ImageFilter.GaussianBlur(.8 * I.S)))
    for k, ch in enumerate('一期一会'): text(img, ch, 65, 222 + k * 30, 24, '#1a120c', SERIF, brush=True)
    ell(img, (88, 324, 98, 334), '#b8302a')
    fill(img, '#1a120c', 62, rect=(8, 404, 122, 418), scale=3); ell(img, (2, 402, 14, 420), '#3a2a1a'); ell(img, (116, 402, 128, 420), '#3a2a1a')
    item(img, 'te_jiku', 'Свиток «Итиго итиэ» с кругом энсо', 140)


# ───────────── the tatami for the ceremony, seen from above (900×1500) ─────────────
def mat():
    W0, H0 = 900, 1500; n = 2; w, h = W0 * n, H0 * n
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); yy /= n; xx /= n
    N = fbm(w, h, 120, 5, 71); F = fbm(w, h, 10, 3, 72, (1, 6))
    def weave(coord, period=7.5): return (np.sin(coord / period * 2 * math.pi) * .5 + .5)
    guest = yy < 470
    wv = np.where(guest, weave(xx + F * 3), weave(yy + F * 3))          # the straw runs along each mat's long side
    v = np.clip(.5 * N + .25 * wv + .2 * F, 0, 1)
    rgb = cmix('#3c3a24', '#7a7448', v)
    # heri: the dark cloth borders of the mats
    def band(mask, col='#17140f'): return np.where(mask[..., None], cmix(col, '#2c271c', F * .7 + N * .3), rgb)
    rgb = band((yy > 466) & (yy < 494))
    rgb = band((xx > 22) & (xx < 46) & (yy > 494)); rgb = band((xx > 854) & (xx < 878) & (yy > 494))
    rgb = band((yy > 8) & (yy < 30) & guest)
    # a wooden board at the top (the edge of the tokonoma) and the seams of mats
    wood = yy < 8
    rgb = np.where(wood[..., None], cmix('#2a1c12', '#4a3220', fbm(w, h, 30, 3, 73, (6, 1))), rgb)
    for (x0, x1) in ((450, 452),): rgb = np.where(((xx > x0) & (xx < x1) & guest & (yy > 30))[..., None], rgb * .7, rgb)
    # zabuton for the guest and for Musya
    def cushion(cx, cy, rw, rh, col):
        d = np.maximum(np.abs(xx - cx) / rw, np.abs(yy - cy) / rh); m = np.clip((1 - d) * 30, 0, 1)
        sh = np.clip((1 - np.maximum(np.abs(xx - cx - 6) / (rw + 10), np.abs(yy - cy - 10) / (rh + 10))) * 8, 0, 1)
        out = rgb * (1 - .45 * sh[..., None])
        body = cmix(dk(H(col), .35), lt(H(col), .1), np.clip(N * .6 + (1 - d) * .8, 0, 1))
        return out * (1 - m[..., None]) + body * m[..., None]
    rgb = cushion(615, 330, 115, 95, '#4a2a3a'); rgb = cushion(250, 350, 95, 80, '#2a3a4a')
    # warm andon light from the upper left, deep dark at the edges, a cooler moonlit lower right
    L = np.exp(-(((xx - 60) / 700) ** 2 + ((yy - 300) / 900) ** 2))
    rgb = rgb * (.42 + .75 * L)[..., None] + np.array([30, 16, 0], np.float32) * L[..., None]
    vig = np.clip(1 - (((xx - 450) / 560) ** 2 + ((yy - 820) / 900) ** 2) ** 1.4 * .55, .35, 1)
    rgb *= vig[..., None]
    rgb += np.array([-6, 0, 10], np.float32) * np.clip((xx + yy - 1400) / 1000, 0, 1)[..., None]
    img = rgba(rgb, np.ones((h, w), np.float32)).resize((W0, H0), Image.LANCZOS)
    img = grain(img, 74, 4.0, .85).convert('RGB')
    img.save(os.path.join(ASSETS, 'bg', 'te_mat.webp'), 'WEBP', quality=80, method=6)
    img.resize((450, 750)).save(os.path.join(PREV, 'te_mat.png'))
    print('bg', os.path.getsize(os.path.join(ASSETS, 'bg', 'te_mat.webp')) // 1024, 'KB')


def pack():
    lst = sorted(SPR.items(), key=lambda t: -t[1].height); W = 1400; x = y = rowh = 0; pos = {}
    for k, im in lst:
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[k] = (x, y); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for k, im in lst: at.paste(im, pos[k])
    p = os.path.join(ASSETS, 'items', 'atlas_te.webp'); at.save(p, 'WEBP', quality=86, alpha_quality=90, method=6)
    prev = Image.new('RGBA', at.size, (60, 70, 60, 255)); prev.alpha_composite(at); prev.convert('RGB').save(os.path.join(PREV, 'atlas_te.png'))
    for r in ROWS: r['at'] = ['te', *pos[r['id']]]
    spr = {k: [*pos[k], SPR[k].width, SPR[k].height] for k in SPR if not k.startswith('te_')}
    print('atlas', at.size, os.path.getsize(p) // 1024, 'KB')
    return {'atlas': list(at.size), 'items': ROWS, 'spr': spr}


if __name__ == '__main__':
    what = sys.argv[2:] or ['mat', 'atlas']
    if 'mat' in what: mat()
    if 'atlas' in what:
        SPR['g_bowl'] = top_bowl(); SPR['g_natsume'] = top_natsume(); SPR['g_kama'] = top_kama()
        SPR['g_kensui'] = top_ring_bowl(180, 37, '#6a5a3a', '#1c160e'); SPR['g_mizusashi'] = top_ring_bowl(190, 39, '#d8cfbc', '#000000', rim=.84, spots='#8a5a3a', lid='#15110d')
        SPR['g_chasen'] = top_chasen(); SPR['g_hishaku'] = top_hishaku(); SPR['g_chashaku'] = top_chashaku(); SPR['g_fukusa'] = top_fukusa()
        SPR['g_wagashi'] = wagashi(); SPR['g_chabako'] = chabako()
        build_items(); P.set_size(1800, 1400)
        out = pack(); json.dump(out, open(os.path.join(PREV, 'tea.json'), 'w'), ensure_ascii=False)
        print(json.dumps(out, ensure_ascii=False, separators=(',', ':')))
