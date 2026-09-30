#!/usr/bin/env python3
"""Add-on art: a sakura that grows for a month in the courtyard (7 stages + 3 seasonal looks of the grown tree)
and a gachapon machine at the night fair with 18 capsule figurines (3 series × 6).
Usage: cd art && python3 tree_gacha_art.py ../assets/items  →  atlas_sk.webp, atlas_sk1.webp, atlas_fg.webp;
the rect maps are printed as JSON and saved to out/tree_gacha.json (they are pasted into feat/sakura.js, feat/gacha.js)."""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc, textured_fill
from items import px, canvas, fill, volume, soft, floor_shadow, line, ell, poly, text, H, dk, lt, mask_poly, SERIF, SANS
from room_items import blob, cr


def ocr(pts, n=8):
    """open Catmull-Rom spline through pts"""
    out = []; N = len(pts); g = lambda j: pts[min(max(j, 0), N - 1)]
    for i in range(N - 1):
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * (2 * p1[c] + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t2 + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t3) for c in (0, 1)))
    return out + [pts[-1]]

OUT = sys.argv[1] if len(sys.argv) > 1 else '../assets/items'
S = P.SS
RECTS = {}


def finish(img, grade=.88, noise=3.0, seed=1):
    out = img.resize((P.W, P.H), Image.LANCZOS)
    a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * grade
    a[..., :3] += np.random.default_rng(seed).normal(0, noise, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def pack(name, items, width, quality=84):
    """items: [(key, img)] → shelf-packed atlas; rects {key:[x,y,w,h]}"""
    lst = sorted(items, key=lambda t: -t[1].height); x = y = rowh = 0; pos = {}
    for k, im in lst:
        if x + im.width + 2 > width: x = 0; y += rowh + 2; rowh = 0
        pos[k] = (x, y); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (width, y + rowh), (0, 0, 0, 0))
    for k, im in lst: at.paste(im, pos[k])
    f = f'{OUT}/atlas_{name}.webp'; at.save(f, 'WEBP', quality=quality, alpha_quality=88, method=6)
    RECTS[name] = {'w': at.width, 'h': at.height, 'r': {k: [pos[k][0], pos[k][1], im.width, im.height] for k, im in items}}
    print('atlas', name, at.size, os.path.getsize(f) // 1024, 'KB')


# ───────────────────────────── the sakura ─────────────────────────────
BARK = (hexc('#1a1412'), hexc('#3a2e2a'), hexc('#6a5a52'))
PAL = {
    'bloom': [hexc(c) for c in ('#4a2c3a', '#7a4a5e', '#a86e84', '#cf97aa', '#e9bccb', '#f6dde4')],
    'summer': [hexc(c) for c in ('#152014', '#22341e', '#33492a', '#4a6236', '#657d44', '#86994f')],
    'autumn': [hexc(c) for c in ('#35160e', '#5e2415', '#8e3a1c', '#b85a24', '#d4842e', '#e2aa48')],
    'young': [hexc(c) for c in ('#1c2c18', '#2c4424', '#40602e', '#5a7c3a', '#7a9a4a', '#9ab45c')],
}


def limb_mask(size, segs):
    m = Image.new('L', size, 0); d = ImageDraw.Draw(m)
    for (x0, y0), (x1, y1), w0, w1 in segs:
        a = math.atan2(y1 - y0, x1 - x0) + math.pi / 2; c, s = math.cos(a), math.sin(a)
        d.polygon([(x0 + c * w0, y0 + s * w0), (x1 + c * w1, y1 + s * w1), (x1 - c * w1, y1 - s * w1), (x0 - c * w0, y0 - s * w0)], fill=255)
        d.ellipse([x1 - w1, y1 - w1, x1 + w1, y1 + w1], fill=255); d.ellipse([x0 - w0, y0 - w0, x0 + w0, y0 + w0], fill=255)
    return m


def bark_paint(img, segs, seed, lenticels=True):
    """Cherry bark: dark, glossy, with horizontal lenticel bands; cylindrical shading."""
    if not segs: return
    m = limb_mask(img.size, segs); box = m.getbbox()
    if not box: return
    sub = m.crop(box)
    tex = textured_fill(sub, BARK[1], BARK[0], BARK[2], 12 * S, seed, stretch=(2, .5), contrast=1.05)
    t = np.asarray(tex, np.float32)
    edge = np.asarray(sub.filter(ImageFilter.GaussianBlur(5 * S)), np.float32) / 255
    xx = np.linspace(0, 1, sub.width)[None, :]
    t[..., :3] *= (.4 + .6 * edge[..., None]) * (1.08 - .25 * xx[..., None])     # lit from the left
    if lenticels:
        n = P.fbm(sub.width, sub.height, 3 * S, 3, seed + 5, (6, .3))
        band = np.clip((n - .72) * 5, 0, 1)[..., None] * .3
        t[..., :3] = t[..., :3] * (1 - band) + np.array([120, 108, 100], np.float32) * band
    t[..., 3] = np.asarray(sub, np.float32)
    img.alpha_composite(Image.fromarray(np.clip(t, 0, 255).astype(np.uint8), 'RGBA'), box[:2])


def dabs(img, blobs, n, pal, rnd, size=(3, 6), shape='leaf', light=(-.55, -.8), alpha=(150, 255)):
    d = ImageDraw.Draw(img); lx, ly = light
    for _ in range(n):
        cx, cy, rx, ry = rnd.choice(blobs); a = rnd.random() * math.tau; r = rnd.random() ** .5
        if r > .8 and rnd.random() < .5: continue
        dx, dy = math.cos(a) * r, math.sin(a) * r; x, y = cx + dx * rx, cy + dy * ry
        lit = -(dx * lx + dy * ly) * .9 + (rnd.random() - .5) * .9; tt = min(.999, max(0, (lit + 1) / 2)) ** 1.15
        c = pal[int(tt * len(pal))]; col = (c[0], c[1], c[2], int(rnd.uniform(*alpha) * (1 - .3 * r)))
        s = rnd.uniform(*size) * S
        if shape == 'dot':
            d.ellipse([x - s * .5, y - s * .42, x + s * .5, y + s * .42], fill=col)
        else:
            b = rnd.uniform(0, math.tau); L = s * .55
            d.line([(x - math.cos(b) * L, y - math.sin(b) * L), (x + math.cos(b) * L, y + math.sin(b) * L)], fill=col, width=max(2, int(S * rnd.uniform(1.6, 2.6))))


def core_shadow(img, blobs, col, k=.8):
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    for cx, cy, rx, ry in blobs: d.ellipse([cx - rx * k, cy - ry * k + ry * .25, cx + rx * k, cy + ry * k + ry * .25], fill=col[:3] + (225,))
    img.alpha_composite(l.filter(ImageFilter.GaussianBlur(6 * S)))


def grow(cx, base, trunk_h, spread, depth, seed, w0):
    """Branch skeleton: returns segment lists per thickness class and the twig tips."""
    rnd = random.Random(seed); segs = [[], [], []]; tips = []; snow = []
    def br(x0, y0, ang, L, wd, d):
        if d > depth or L < 9 * S:
            tips.append((x0, y0, d)); return
        pts = P.wobble((x0, y0), (x0 + math.sin(ang) * L, y0 - math.cos(ang) * L), 4, L * .06, rnd)
        for i in range(len(pts) - 1):
            u0, u1 = i / (len(pts) - 1), (i + 1) / (len(pts) - 1)
            seg = (pts[i], pts[i + 1], wd * (1 - .3 * u0), wd * (1 - .3 * u1)); segs[min(2, d)].append(seg)
            if abs(math.sin(ang)) > .25: snow.append(seg)
        x1, y1 = pts[-1]
        k = 3 if d == 0 else rnd.choice((2, 2, 3))
        for j in range(k):
            f = (j - (k - 1) / 2) / max(1, (k - 1) / 2)
            na = ang * .55 + f * spread * (1.0 if d == 0 else .7) + rnd.uniform(-.22, .22)
            br(x1, y1, na, L * rnd.uniform(.6, .72), wd * .62, d + 1)
        if d >= 2: tips.append((x1, y1, d))
    # trunk: a short bole with a root flare, then the main limbs
    pts = P.wobble((cx, base), (cx + rnd.uniform(-8, 8) * S, base - trunk_h), 6, trunk_h * .04, rnd)
    for i in range(len(pts) - 1):
        u0, u1 = i / (len(pts) - 1), (i + 1) / (len(pts) - 1)
        segs[0].append((pts[i], pts[i + 1], w0 * (1.25 - .45 * u0), w0 * (1.25 - .45 * u1)))
    x1, y1 = pts[-1]; nl = 4 if depth >= 4 else 3
    for j in range(nl):
        f = (j - (nl - 1) / 2) / ((nl - 1) / 2)
        br(x1, y1, f * spread + rnd.uniform(-.12, .12), trunk_h * rnd.uniform(.5, .62), w0 * .7, 1)
    return segs, tips, snow


def mound(img, cx, base, rx, seed, snowy=False):
    fill(img, '#2a231c', seed, ell=(cx - rx, base - rx * .22, cx + rx, base + rx * .1), scale=5, contrast=1.3)
    rr = random.Random(seed); d = ImageDraw.Draw(img)
    for _ in range(int(rx * 1.2)):
        x = cx + rr.uniform(-rx, rx) * .9; y = base - rx * .08 + rr.uniform(-rx * .1, rx * .08)
        c = rr.choice(['#4a4034', '#3a3228', '#5a5044', '#1a1510']); r = rr.uniform(.8, 2.2)
        d.ellipse([px(x - r), px(y - r * .7), px(x + r), px(y + r * .7)], fill=H(c))
    volume(img, (cx - rx, base - rx * .22, cx + rx, base + rx * .1), .5, .4)
    if snowy: soft(img, lambda dd: dd.ellipse([px(cx - rx * .9), px(base - rx * .2), px(cx + rx * .9), px(base - rx * .02)], fill=(222, 228, 234, 210)), 1.2)


def label(img, x, base, h=70, tilt=.08):
    """wooden plant label (fuda) stuck into the soil with 桜 in ink"""
    top = base - h; w = 16
    pts = [(x - w / 2, top), (x + w / 2, top - w * tilt * 4), (x + w / 2 + h * tilt, base), (x - w / 2 + h * tilt, base)]
    fill(img, '#b8a07a', 7, poly=pts, scale=3, stretch=(.3, 3), contrast=1.2)
    poly(img, [(x - w / 2, top), (x, top - 8), (x + w / 2, top - w * tilt * 4)], '#b8a07a')
    text(img, '桜', x + 2 + h * tilt * .25, top + 16, 13, '#1a1210', SERIF, brush=True)
    volume(img, (x - w / 2, top - 8, x + w / 2 + h * tilt, base), .4, .3)


def leaf(img, x, y, ang, L, col, seed):
    c = H(col); a = math.radians(ang); nx, ny = math.cos(a), math.sin(a)
    pts = [(x, y), (x + nx * L * .45 - ny * L * .22, y + ny * L * .45 + nx * L * .22), (x + nx * L, y + ny * L), (x + nx * L * .45 + ny * L * .22, y + ny * L * .45 - nx * L * .22)]
    blob(img, pts, c, seed, scale=3, contrast=.8, k=.5, rim=.2)
    line(img, [(x, y), (x + nx * L * .9, y + ny * L * .9)], dk(c, .35), .8)


def stem(img, pts, w, col='#4a5a2a'):
    for (a, b) in zip(pts, pts[1:]): line(img, [a, b], col, w)
    line(img, [(p[0] - w * .25, p[1]) for p in pts], lt(H(col), .25), max(.6, w * .3))


def young(stage):
    """stages 0..2: mound + label, sprout, sapling with a bamboo stake"""
    if stage == 0:
        img = canvas(170, 130); floor_shadow(img, 85, 122, 70); mound(img, 85, 118, 58, 3)
        ImageDraw.Draw(img).ellipse([px(78), px(100), px(92), px(106)], fill=H('#3a2a20'))       # the planted stone, a dimple
        label(img, 122, 112, 74); return img
    if stage == 1:
        img = canvas(160, 180); floor_shadow(img, 80, 172, 64); mound(img, 80, 168, 54, 4)
        stem(img, [(78, 160), (79, 130), (82, 100)], 3.2)
        leaf(img, 82, 104, -160, 30, '#6a8a3a', 11); leaf(img, 82, 104, -20, 30, '#7a9a44', 12)
        leaf(img, 82, 100, -110, 22, '#8aaa4c', 13); leaf(img, 82, 100, -70, 20, '#96b454', 14)
        label(img, 126, 162, 70); return img
    img = canvas(230, 330); floor_shadow(img, 115, 322, 80); mound(img, 112, 318, 66, 5)
    line(img, [(142, 318), (140, 70)], '#8a8a4a', 5); line(img, [(141, 318), (139, 70)], '#b0a860', 1.6)     # bamboo stake
    for y in (140, 220, 290): line(img, [(139, y), (143, y)], '#5a5a2a', 5)
    st = [(112, 312), (116, 250), (114, 190), (120, 130), (118, 80)]; stem(img, st, 4.2, '#4a3a2a')
    for y in (170, 110): line(img, [(117, y), (141, y + 4)], '#c8b070', 1.6)                                 # straw ties
    rr = random.Random(9)
    for i, (x, y) in enumerate([(116, 250), (114, 210), (118, 170), (120, 130), (119, 104), (118, 82)]):
        side = -1 if i % 2 else 1; bx = x + side * 28
        line(img, [(x, y), (bx, y - 16)], '#4a3a2a', 2)
        for k in range(3): leaf(img, bx, y - 16, (-150 if side < 0 else -30) + rr.uniform(-40, 40), rr.uniform(20, 28), rr.choice(['#5a7a34', '#6a8a3a', '#7a9a44']), i * 7 + k)
    for k in range(4): leaf(img, 118, 80, -90 + (k - 1.5) * 34, 24, '#7a9a44', 60 + k)
    label(img, 70, 312, 70, -.06); return img


def tree(w, h, trunk_h, spread, depth, w0, crown, seed, season='young', buds=False, lab=False):
    img = canvas(w, h); cx, base = w / 2 * S, (h - 14) * S
    floor_shadow(img, w / 2, h - 10, w * .36, 120)
    segs, tips, snow = grow(cx, base, trunk_h * S, spread, depth, seed, w0 * S)
    rnd = random.Random(seed + 1); m = crown * 1.25 * S
    xs = [p[0] for sg in segs for a in sg for p in a[:2]] + [t[0] for t in tips]; ys = [p[1] for sg in segs for a in sg for p in a[:2]] + [t[1] for t in tips]
    k = min(1, (cx - m) / max(1, max(abs(x - cx) for x in xs)), (base - m * 1.1) / max(1, base - min(ys)))
    T = lambda p: (cx + (p[0] - cx) * k, base + (p[1] - base) * k)
    segs = [[(T(a), T(b_), w_a, w_b) for a, b_, w_a, w_b in sg] for sg in segs]; snow = [(T(a), T(b_), w_a, w_b) for a, b_, w_a, w_b in snow]
    tips = [T(t[:2]) + (t[2],) for t in tips]
    mound(img, w / 2, h - 14, max(40, w * .14), seed, snowy=season == 'winter')
    if season == 'winter':
        # bare: fine twigs from every tip
        tw = []
        for x, y, d in tips:
            for k in range(rnd.choice((2, 3))):
                a = rnd.uniform(-1.2, 1.2); L = rnd.uniform(14, 34) * S
                tw.append(((x, y), (x + math.sin(a) * L, y - math.cos(a) * L), 1.4 * S, .6 * S))
        for i, sg in enumerate(segs[::-1]): bark_paint(img, sg, seed + i, lenticels=(i == 2))
        bark_paint(img, tw, seed + 9, lenticels=False)
        # snow on the upper side of branches, a few clumps
        l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l)
        for (x0, y0), (x1, y1), w_0, w_1 in snow:
            if rnd.random() < .75:
                sw = min((w_0 + w_1) * .3, 5 * S); d.line([(x0, y0 - w_0 * .8), (x1, y1 - w_1 * .8)], fill=(214, 222, 230, 205), width=max(2, int(sw)))
        for x, y, dd in tips:
            if rnd.random() < .35: r = rnd.uniform(3, 7) * S; d.ellipse([x - r, y - r * .6, x + r, y + r * .5], fill=(226, 232, 240, 220))
        img.alpha_composite(l.filter(ImageFilter.GaussianBlur(1.1 * S)))
        return img
    blobs = []
    for x, y, d in tips:
        r = crown * rnd.uniform(.8, 1.2) * S * (1 if d > 2 else .85)
        blobs.append((x + rnd.uniform(-.3, .3) * r, y - r * .35, r, r * .7))
    blobs = P.ragged(blobs, rnd, 5, .65)
    pal = PAL[season]
    # far half of the crown, then the limbs, then the near half: branches read through the foliage
    back = [b for b in blobs if rnd.random() < .5]
    core_shadow(img, blobs, dk(pal[0], .4), .85)
    dabs(img, back, 70 * len(back), pal[:-1], rnd, size=(3, 6), shape='dot' if season == 'bloom' else 'leaf', alpha=(120, 220))
    for i, sg in enumerate(segs[::-1]): bark_paint(img, sg, seed + i, lenticels=(i == 2))
    front = [b for b in blobs if b not in back]
    dabs(img, front, 90 * len(front), pal, rnd, size=(3, 6.5), shape='dot' if season == 'bloom' else 'leaf')
    if season == 'bloom':           # white-pink highlights on the lit side and a few single flowers
        hi = [b for b in blobs if b[1] < base - trunk_h * S * 1.2]
        dabs(img, hi or blobs, 25 * len(blobs), [hexc('#f8e6ec'), hexc('#fff2f5')], rnd, size=(2, 4), shape='dot', alpha=(120, 230))
    if buds:
        dabs(img, blobs, 6 * len(blobs), [hexc('#b86a82'), hexc('#d890a4')], rnd, size=(2, 3), shape='dot')
    if season == 'autumn':          # a few leaves already on the ground
        d = ImageDraw.Draw(img)
        for _ in range(60):
            x = cx + rnd.uniform(-w * .38, w * .38) * S; y = base + rnd.uniform(-8, 6) * S; c = rnd.choice(pal[2:])
            d.ellipse([x - 3 * S, y - 1.6 * S, x + 3 * S, y + 1.6 * S], fill=c)
    return img


def sakura_all():
    F = lambda im, i=0: finish(im, .9, 3, i)          # finish right away: finish() resizes to the current canvas size
    st = [F(young(0)), F(young(1)), F(young(2)),
          F(tree(330, 450, 120, .75, 3, 7, 34, 21)),
          F(tree(450, 590, 170, .8, 3, 10, 44, 22)),
          F(tree(590, 740, 230, .85, 4, 15, 44, 23, buds=True)),
          F(tree(800, 900, 300, .9, 4, 22, 52, 24, 'bloom'))]
    pack('sk', [(f's{i}', im) for i, im in enumerate(st[:6])], 1400, 78)
    se = [(k, F(tree(800, 900, 300, .9, 4, 22, 52, 24, k))) for k in ('summer', 'autumn', 'winter')]
    pack('sk1', [('s6', st[6]), se[0]], 1604, 76)
    pack('sk2', se[1:], 1604, 76)
    prev = Image.new('RGBA', (2000, 260), (38, 42, 40, 255)); x = 0
    for im in st + [s[1] for s in se]:
        t = im.copy(); t.thumbnail((190, 240)); prev.alpha_composite(t, (x, 250 - t.height)); x += 196
    prev.convert('RGB').save('out/sk_preview.png')


# ───────────────────────────── gachapon figurines ─────────────────────────────
SER_BASE = {1: '#4e6450', 2: '#3e3e5e', 3: '#7a5e44', 0: '#c89a3a'}


def disc(img, cx, by, rx, col, gold=False):
    c = H(col)
    fill(img, dk(c, .25), 5, rect=(cx - rx, by, cx + rx, by + 8), scale=3, contrast=.6)
    fill(img, dk(c, .25), 6, ell=(cx - rx, by + 8 - rx * .2, cx + rx, by + 8 + rx * .2), scale=3, contrast=.6)
    fill(img, c, 7, ell=(cx - rx, by - rx * .2, cx + rx, by + rx * .2), scale=4, contrast=.7)
    volume(img, (cx - rx, by - rx * .2, cx + rx, by + 8 + rx * .2), .5, .35, spec=.35 if gold else .15)
    soft(img, lambda d: d.ellipse([px(cx - rx * .6), px(by - rx * .16), px(cx - rx * .05), px(by - rx * .06)], fill=(255, 255, 255, 70)), 1)


def B(img, pts, col, seed, spec=.18, k=.55, scale=4, contrast=.7):
    return blob(img, pts, H(col), seed, scale=scale, contrast=contrast, k=k, rim=.35, spec=spec)


def O(img, cx, cy, rx, ry, col, seed, spec=.2, k=.55, contrast=.7):
    c = H(col); fill(img, c, seed, ell=(cx - rx, cy - ry, cx + rx, cy + ry), scale=4, contrast=contrast)
    volume(img, (cx - rx, cy - ry, cx + rx, cy + ry), k, .38, spec=spec)


def eyes(img, cx, y, dx, r=4.2, col='#141012'):
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        x = cx + sx * dx; d.ellipse([px(x - r), px(y - r * 1.15), px(x + r), px(y + r * 1.15)], fill=H(col))
        d.ellipse([px(x - r * .55), px(y - r * .8), px(x - r * .05), px(y - r * .25)], fill=(255, 255, 255, 235))


def happy(img, cx, y, dx, w=5, col='#1a1414'):
    d = ImageDraw.Draw(img)
    for sx in (-1, 1): x = cx + sx * dx; d.arc([px(x - w), px(y - w * .6), px(x + w), px(y + w * .8)], 200, 340, fill=H(col), width=px(1.8))


def blush(img, cx, y, dx, r=4):
    for sx in (-1, 1): soft(img, lambda d, sx=sx: d.ellipse([px(cx + sx * dx - r), px(y - r * .6), px(cx + sx * dx + r), px(y + r * .6)], fill=(230, 110, 120, 110)), 1.2)


def cat_face(img, cx, cy, fur, ear_in='#e7a3a8', eyes_kind='dot', eye_col='#141012', r=26, seed=1, stripes=None):
    fur = H(fur)
    for sx in (-1, 1):
        B(img, [(cx + sx * r * .95, cy - r * .2), (cx + sx * r * .85, cy - r * 1.15), (cx + sx * r * .3, cy - r * .7)], fur, seed + sx, spec=0)
        poly(img, [(cx + sx * r * .82, cy - r * .35), (cx + sx * r * .78, cy - r * .95), (cx + sx * r * .42, cy - r * .66)], ear_in)
    O(img, cx, cy, r, r * .86, fur, seed + 3, spec=.22)
    if stripes:
        d = ImageDraw.Draw(img)
        for k in (-1, 0, 1): d.line([(px(cx + k * 6), px(cy - r * .82)), (px(cx + k * 5), px(cy - r * .5))], fill=H(stripes), width=px(2.4))
    if eyes_kind == 'dot': eyes(img, cx, cy + 1, r * .4, r * .15, eye_col)
    elif eyes_kind == 'happy': happy(img, cx, cy, r * .4, r * .18)
    elif eyes_kind == 'yellow':
        d = ImageDraw.Draw(img)
        for sx in (-1, 1):
            x = cx + sx * r * .4; d.ellipse([px(x - 5.5), px(cy - 4), px(x + 5.5), px(cy + 5)], fill=H('#e8c830')); d.ellipse([px(x - 1.4), px(cy - 3.5), px(x + 1.4), px(cy + 4.5)], fill=H('#141012'))
    d = ImageDraw.Draw(img)
    d.polygon([(px(cx - 2.5), px(cy + 6)), (px(cx + 2.5), px(cy + 6)), (px(cx), px(cy + 9))], fill=H('#d77a80'))
    d.arc([px(cx - 6), px(cy + 7), px(cx), px(cy + 12)], 10, 170, fill=H('#2a1a1a'), width=px(1.2)); d.arc([px(cx), px(cy + 7), px(cx + 6), px(cy + 12)], 10, 170, fill=H('#2a1a1a'), width=px(1.2))
    for sx in (-1, 1):
        for k in range(2): d.line([(px(cx + sx * 10), px(cy + 8 + k * 3)), (px(cx + sx * 24), px(cy + 5 + k * 6))], fill=(200, 190, 180, 150), width=px(.8))


FIG = []   # (id, name, series, secret, img)


def fig(fid, name, ser, secret=False, w=120, h=146):
    def deco(fn):
        img = canvas(w, h); floor_shadow(img, w / 2, h - 6, w * .42, 90)
        disc(img, w / 2, h - 18, w * .38, SER_BASE[0 if secret else ser], secret)
        fn(img, w / 2, h - 20)
        FIG.append((fid, name, ser, secret, finish(img, .92, 2.5, len(FIG) + 3))); return fn
    return deco


# ── Series 1: «Ёкаи дома»
@fig('fg_kappa', 'Каппа', 1)
def _(img, cx, b):
    O(img, cx, b - 30, 30, 24, '#6a5030', 11)                                  # shell behind
    B(img, [(cx - 24, b), (cx - 26, b - 30), (cx - 12, b - 48), (cx + 12, b - 48), (cx + 26, b - 30), (cx + 24, b)], '#5f8a4a', 12)
    O(img, cx, b - 28, 13, 15, '#d8c890', 13, spec=.1)                           # belly
    O(img, cx, b - 74, 32, 28, '#6a9a52', 14, spec=.25)                          # head
    d = ImageDraw.Draw(img)
    for k in range(9):                                                         # hair fringe round the dish
        a = math.pi * (1.05 + k * .1); d.ellipse([px(cx + math.cos(a) * 26 - 7), px(b - 92 + math.sin(a) * 10 - 6), px(cx + math.cos(a) * 26 + 7), px(b - 92 + math.sin(a) * 10 + 6)], fill=H('#1e2a1a'))
    O(img, cx, b - 96, 17, 6, '#bcd8e0', 15, spec=.5); ell(img, (cx - 12, b - 99, cx + 2, b - 96), '#eef6f8')
    eyes(img, cx, b - 74, 12, 5.2)
    O(img, cx, b - 62, 7, 5, '#e0b040', 16, spec=.4)                           # beak
    O(img, cx, b - 30, 26, 5, '#3e6a2a', 17, spec=.3)                          # the cucumber
    d = ImageDraw.Draw(img)
    for k in range(8): d.ellipse([px(cx - 20 + k * 5.5), px(b - 31), px(cx - 18.6 + k * 5.5), px(b - 29.6)], fill=H('#9ac070'))
    for sx in (-1, 1): O(img, cx + sx * 24, b - 30, 7, 6, '#6a9a52', 18 + sx)
    for sx in (-1, 1): O(img, cx + sx * 12, b - 2, 9, 4, '#4e7a3c', 20 + sx, spec=.1)


@fig('fg_kitsune', 'Лиса-невеста', 1)
def _(img, cx, b):
    B(img, [(cx + 18, b - 10), (cx + 44, b - 30), (cx + 48, b - 66), (cx + 36, b - 84), (cx + 30, b - 60), (cx + 26, b - 30)], '#d89a40', 21, spec=.2)
    ell(img, (cx + 34, b - 90, cx + 46, b - 76), '#f4ead8')                          # white tail tip
    B(img, [(cx - 26, b), (cx - 22, b - 40), (cx - 12, b - 54), (cx + 12, b - 54), (cx + 22, b - 40), (cx + 26, b)], '#f2eee6', 22, spec=.25)
    d = ImageDraw.Draw(img)
    d.line([(px(cx - 10), px(b - 54)), (px(cx), px(b - 38)), (px(cx + 10), px(b - 54))], fill=H('#c02a2a'), width=px(2.6))   # red inner collar
    fill(img, '#d8b048', 23, rect=(cx - 22, b - 30, cx + 22, b - 22), scale=3); volume(img, (cx - 22, b - 30, cx + 22, b - 22), .4, .2, spec=.2)
    for sx in (-1, 1):
        B(img, [(cx + sx * 8, b - 84), (cx + sx * 22, b - 116), (cx + sx * 26, b - 80)], '#f2eee6', 24 + sx, spec=0)
        poly(img, [(cx + sx * 12, b - 88), (cx + sx * 21, b - 108), (cx + sx * 22, b - 86)], '#e7a3a8')
    B(img, [(cx - 22, b - 70), (cx - 18, b - 90), (cx, b - 96), (cx + 18, b - 90), (cx + 22, b - 70), (cx + 6, b - 54), (cx, b - 50), (cx - 6, b - 54)], '#f6f2ea', 26, spec=.3)
    fill(img, '#f8f6f0', 27, ell=(cx - 24, b - 100, cx + 24, b - 88), scale=3); volume(img, (cx - 24, b - 100, cx + 24, b - 88), .4, .3, spec=.3)   # tsunokakushi band
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        d.line([(px(cx + sx * 5), px(b - 76)), (px(cx + sx * 15), px(b - 80))], fill=H('#1a1212'), width=px(2.2))
        d.line([(px(cx + sx * 6), px(b - 81)), (px(cx + sx * 16), px(b - 86))], fill=H('#c02a2a'), width=px(1.8))
    d.ellipse([px(cx - 3), px(b - 56), px(cx + 3), px(b - 51)], fill=H('#2a2622'))


@fig('fg_tanuki', 'Тануки', 1)
def _(img, cx, b):
    B(img, [(cx + 20, b - 6), (cx + 42, b - 16), (cx + 44, b - 36), (cx + 30, b - 26)], '#6a4a2e', 31, spec=0)
    d = ImageDraw.Draw(img)
    for k in range(2): d.line([(px(cx + 30 + k * 6), px(b - 30 + k * 2)), (px(cx + 36 + k * 6), px(b - 14))], fill=H('#2a1a10'), width=px(2.4))
    O(img, cx, b - 30, 30, 30, '#7a5a3a', 32)
    O(img, cx - 2, b - 26, 20, 20, '#e8dcc0', 33, spec=.3)
    O(img, cx, b - 74, 26, 22, '#7a5a3a', 34, spec=.2)
    for sx in (-1, 1): O(img, cx + sx * 10, b - 74, 9, 7, '#2a1c14', 35 + sx, spec=0)
    eyes(img, cx, b - 74, 10, 3.2, '#f0e8d8'); eyes(img, cx, b - 74, 10, 2.2)
    O(img, cx, b - 64, 6, 4, '#e8dcc0', 36, spec=0); ell(img, (cx - 2.5, b - 67, cx + 2.5, b - 63), '#1a1212')
    poly(img, [(cx - 44, b - 90), (cx, b - 118), (cx + 44, b - 90), (cx, b - 96)], '#c8a860')          # straw kasa
    fill(img, '#c8a860', 37, poly=[(cx - 44, b - 90), (cx, b - 118), (cx + 44, b - 90), (cx, b - 96)], scale=2, stretch=(.3, 3), contrast=1.4)
    volume(img, (cx - 44, b - 118, cx + 44, b - 90), .5, .2, spec=.15)
    O(img, cx - 30, b - 24, 10, 13, '#ece6d8', 38, spec=.3); ell(img, (cx - 33, b - 42, cx - 27, b - 36), '#6a4a2a')   # sake bottle
    text(img, '福', cx - 30, b - 22, 9, '#a02a22', SERIF)
    for sx in (-1, 1): O(img, cx + sx * 14, b - 3, 10, 4, '#5a3e26', 39 + sx, spec=0)


@fig('fg_nekomata', 'Нэкомата', 1)
def _(img, cx, b):
    for sx, c in ((-1, '#e8e2d6'), (1, '#d08a3a')):                               # two tails
        pts = [(cx + sx * 10, b - 16), (cx + sx * 30, b - 30), (cx + sx * 26, b - 60), (cx + sx * 38, b - 88)]
        q = ocr(pts, 6); line(img, q, c, 7); line(img, [(p[0] - 1, p[1]) for p in q], lt(H(c), .3), 2)
    B(img, [(cx - 20, b), (cx - 22, b - 34), (cx - 12, b - 50), (cx + 12, b - 50), (cx + 22, b - 34), (cx + 20, b)], '#eee8dc', 41)
    soft(img, lambda d: d.ellipse([px(cx + 2), px(b - 44), px(cx + 20), px(b - 24)], fill=H('#d08a3a')), 1)
    O(img, cx - 20, b - 58, 7, 9, '#eee8dc', 42)                                 # raised paw, dancing
    cat_face(img, cx, b - 72, '#eee8dc', r=25, seed=43)
    soft(img, lambda d: d.ellipse([px(cx - 22), px(b - 90), px(cx - 6), px(b - 74)], fill=H('#2a2420')), 1)
    fill(img, '#2a4a8a', 44, poly=[(cx - 28, b - 84), (cx, b - 104), (cx + 28, b - 84), (cx + 20, b - 80), (cx - 20, b - 80)], scale=3)   # tenugui
    d = ImageDraw.Draw(img)
    for k in range(9): x = cx - 20 + (k % 5) * 10 + (k // 5) * 5; y = b - 88 - (k // 5) * 7; d.ellipse([px(x - 1.6), px(y - 1.6), px(x + 1.6), px(y + 1.6)], fill=H('#e8e4dc'))
    for sx in (-1, 1): O(img, cx + sx * 10, b - 3, 8, 4, '#e0dace', 45 + sx, spec=0)


@fig('fg_akaname', 'Аканамэ', 1)
def _(img, cx, b):
    d = ImageDraw.Draw(img)
    for k in range(11):                                                        # wild hair
        a = math.pi * (1.0 + k * .1); d.polygon([(px(cx + math.cos(a) * 22), px(b - 62 + math.sin(a) * 18)), (px(cx + math.cos(a) * 44), px(b - 62 + math.sin(a) * 40)), (px(cx + math.cos(a + .14) * 22), px(b - 62 + math.sin(a + .14) * 18))], fill=H('#2e1612'))
    B(img, [(cx - 32, b), (cx - 34, b - 40), (cx - 20, b - 78), (cx + 20, b - 78), (cx + 34, b - 40), (cx + 32, b)], '#b8442e', 51, spec=.2)
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        x = cx + sx * 12; d.ellipse([px(x - 7), px(b - 64), px(x + 7), px(b - 54)], fill=H('#e8c830')); d.ellipse([px(x - 2.4), px(b - 62), px(x + 2.4), px(b - 56)], fill=H('#141012'))
        d.line([(px(x - sx * 8), px(b - 70)), (px(x + sx * 6), px(b - 66))], fill=H('#3a1410'), width=px(2.2))
    d.chord([px(cx - 16), px(b - 50), px(cx + 16), px(b - 34)], 0, 180, fill=H('#3a1614'))
    for k in range(5): x = cx - 12 + k * 6; d.polygon([(px(x - 2.5), px(b - 42)), (px(x + 2.5), px(b - 42)), (px(x), px(b - 37))], fill=H('#f0e8d8'))
    B(img, [(cx - 5, b - 40), (cx + 5, b - 40), (cx + 8, b - 20), (cx + 18, b - 6), (cx + 6, b - 2), (cx - 2, b - 16)], '#e07890', 52, spec=.4)   # the long tongue
    for sx in (-1, 1):
        O(img, cx + sx * 30, b - 8, 9, 6, '#a83a26', 53 + sx)
        for k in range(3): d.line([(px(cx + sx * (26 + k * 4)), px(b - 4)), (px(cx + sx * (27 + k * 4)), px(b + 1))], fill=H('#f0e8d8'), width=px(1.6))


@fig('fg_chochin', 'Тётин-обакэ', 1)
def _(img, cx, b):
    fill(img, '#1a1412', 61, rect=(cx - 14, b - 118, cx + 14, b - 110), scale=3); fill(img, '#1a1412', 62, rect=(cx - 16, b - 10, cx + 16, b), scale=3)
    O(img, cx, b - 60, 32, 52, '#e8dcb8', 63, spec=.15, contrast=1.1)
    d = ImageDraw.Draw(img)
    for k in range(1, 9):
        y = b - 110 + k * 11; hw = 32 * math.sqrt(max(0, 1 - ((y - (b - 60)) / 52) ** 2)); d.arc([px(cx - hw), px(y - 3), px(cx + hw), px(y + 3)], 0, 180, fill=(120, 100, 70, 150), width=px(1.2))
    d.ellipse([px(cx - 22), px(b - 92), px(cx + 4), px(b - 70)], fill=H('#f8f4ea')); d.ellipse([px(cx - 22), px(b - 92), px(cx + 4), px(b - 70)], outline=H('#1a1212'), width=px(1.6))
    d.ellipse([px(cx - 14), px(b - 87), px(cx - 3), px(b - 75)], fill=H('#1a1212')); d.ellipse([px(cx - 12), px(b - 85), px(cx - 9), px(b - 82)], fill=(255, 255, 255, 230))
    d.chord([px(cx - 22), px(b - 62), px(cx + 22), px(b - 32)], 0, 180, fill=H('#3a1614'))
    for k in range(6): x = cx - 17 + k * 7; d.polygon([(px(x - 3), px(b - 47)), (px(x + 3), px(b - 47)), (px(x), px(b - 41))], fill=H('#f0e8d8'))
    B(img, [(cx - 6, b - 44), (cx + 8, b - 44), (cx + 10, b - 26), (cx + 2, b - 18), (cx - 4, b - 28)], '#d85a6a', 64, spec=.35)


# ── Series 2: «Ночной парад»
@fig('fg_karakasa', 'Каракаса', 2)
def _(img, cx, b):
    line(img, [(cx + 2, b - 34), (cx + 2, b - 10)], '#d8c0a0', 6)                                                     # leg
    fill(img, '#6a4a2a', 71, rect=(cx - 14, b - 10, cx + 18, b - 2), scale=3); fill(img, '#4a3020', 72, rect=(cx - 10, b - 2, cx - 4, b + 1), scale=2); fill(img, '#4a3020', 73, rect=(cx + 8, b - 2, cx + 14, b + 1), scale=2)
    line(img, [(cx - 2, b - 11), (cx + 2, b - 16), (cx + 6, b - 11)], '#c02a2a', 1.6)
    pts = [(cx, b - 124), (cx + 34, b - 36), (cx + 20, b - 30), (cx, b - 34), (cx - 20, b - 30), (cx - 34, b - 36)]
    fill(img, '#8a2a34', 74, poly=pts, scale=5, stretch=(.5, 2), contrast=1.1); volume(img, (cx - 34, b - 124, cx + 34, b - 30), .5, .3, spec=.15)
    d = ImageDraw.Draw(img)
    for k in (-24, -12, 0, 12, 24): d.line([(px(cx), px(b - 122)), (px(cx + k), px(b - 34))], fill=(40, 10, 14, 150), width=px(1))
    fill(img, '#1a1210', 75, rect=(cx - 3, b - 132, cx + 3, b - 120), scale=2)
    d.ellipse([px(cx - 12), px(b - 90), px(cx + 12), px(b - 66)], fill=H('#f6f0e2')); d.ellipse([px(cx - 12), px(b - 90), px(cx + 12), px(b - 66)], outline=H('#1a1212'), width=px(1.4))
    d.ellipse([px(cx - 6), px(b - 84), px(cx + 5), px(b - 72)], fill=H('#1a1212')); d.ellipse([px(cx - 4), px(b - 82), px(cx - 1), px(b - 79)], fill=(255, 255, 255, 230))
    B(img, [(cx - 4, b - 58), (cx + 6, b - 58), (cx + 16, b - 40), (cx + 10, b - 34), (cx + 2, b - 46)], '#e07080', 76, spec=.35)


@fig('fg_oni', 'Óни с барабаном', 2, w=130)
def _(img, cx, b):
    O(img, cx + 28, b - 22, 20, 20, '#8a4a2a', 81, spec=.15); O(img, cx + 28, b - 38, 20, 6, '#e8dcc0', 82, spec=.2)     # taiko
    d = ImageDraw.Draw(img)
    for k in range(6): d.ellipse([px(cx + 12 + k * 6.4 - 1.4), px(b - 30), px(cx + 12 + k * 6.4 + 1.4), px(b - 27)], fill=H('#d8b048'))
    d.arc([px(cx + 20), px(b - 41), px(cx + 36), px(b - 35)], 0, 360, fill=H('#a02a22'), width=px(1.6))
    B(img, [(cx - 30, b), (cx - 32, b - 34), (cx - 20, b - 50), (cx + 4, b - 50), (cx + 10, b - 30), (cx + 6, b)], '#b83a2a', 83)
    fill(img, '#d8a830', 84, rect=(cx - 30, b - 24, cx + 8, b - 10), scale=3)                                        # tiger-skin cloth
    for k in range(5): d.line([(px(cx - 26 + k * 8), px(b - 24)), (px(cx - 23 + k * 8), px(b - 10))], fill=H('#1a1212'), width=px(2))
    O(img, cx - 12, b - 74, 28, 25, '#c24030', 85, spec=.25)
    for k in range(10):
        a = math.pi * (1.05 + k * .1); d = ImageDraw.Draw(img); r = 5
        d.ellipse([px(cx - 12 + math.cos(a) * 26 - r), px(b - 80 + math.sin(a) * 20 - r), px(cx - 12 + math.cos(a) * 26 + r), px(b - 80 + math.sin(a) * 20 + r)], fill=H('#1e1412'))
    for sx in (-1, 1): B(img, [(cx - 12 + sx * 8, b - 96), (cx - 12 + sx * 16, b - 118), (cx - 12 + sx * 18, b - 94)], '#e8d8a0', 86 + sx, spec=.3)
    d = ImageDraw.Draw(img)
    for sx in (-1, 1):
        x = cx - 12 + sx * 10; d.ellipse([px(x - 6), px(b - 80), px(x + 6), px(b - 70)], fill=H('#f0e070')); d.ellipse([px(x - 2), px(b - 78), px(x + 2), px(b - 72)], fill=H('#141012'))
    d.chord([px(cx - 26), px(b - 66), px(cx + 2), px(b - 54)], 0, 180, fill=H('#3a1614'))
    for sx in (-1, 1): d.polygon([(px(cx - 12 + sx * 8 - 2), px(b - 60)), (px(cx - 12 + sx * 8 + 2), px(b - 60)), (px(cx - 12 + sx * 8), px(b - 54))], fill=H('#f0e8d8'))
    line(img, [(cx + 4, b - 40), (cx + 22, b - 70)], '#8a6a4a', 4); O(img, cx + 22, b - 71, 4, 4, '#e8dcc0', 87)      # bachi
    O(img, cx + 4, b - 40, 7, 6, '#b83a2a', 88)


@fig('fg_rokuro', 'Рокурокуби', 2)
def _(img, cx, b):
    neck = [(cx - 6, b - 50), (cx - 20, b - 70), (cx - 24, b - 94), (cx - 6, b - 108), (cx + 14, b - 100), (cx + 22, b - 84)]
    pts = ocr(neck, 8)
    for col, wd in (('#8f877c', 10), ('#c9c2b5', 7.6), ('#e8e2d6', 3.6)): line(img, pts, col, wd)
    B(img, [(cx - 30, b), (cx - 26, b - 36), (cx - 14, b - 50), (cx + 2, b - 50), (cx + 12, b - 36), (cx + 14, b)], '#4a3a6a', 91)
    d = ImageDraw.Draw(img)
    d.line([(px(cx - 14), px(b - 50)), (px(cx - 6), px(b - 36)), (px(cx + 2), px(b - 50))], fill=H('#e8e2d6'), width=px(2.4))
    fill(img, '#c8a040', 92, rect=(cx - 28, b - 28, cx + 13, b - 20), scale=3)
    for k in range(8): x, y = cx - 24 + (k * 13) % 36, b - 14 + (k % 3) * 4; d.ellipse([px(x - 2), px(y - 2), px(x + 2), px(y + 2)], fill=H('#e8a0b8'))
    O(img, cx + 24, b - 74, 18, 16, '#ede6da', 93, spec=.2)
    d = ImageDraw.Draw(img)
    d.chord([px(cx + 5), px(b - 94), px(cx + 43), px(b - 68)], 180, 360, fill=H('#15110f')); d.ellipse([px(cx + 14), px(b - 106), px(cx + 34), px(b - 88)], fill=H('#15110f'))
    line(img, [(cx + 30, b - 100), (cx + 46, b - 108)], '#d8b048', 1.6)
    happy(img, cx + 24, b - 74, 7, 4); d.ellipse([px(cx + 22), px(b - 66), px(cx + 26), px(b - 63)], fill=H('#c0302a')); blush(img, cx + 24, b - 69, 11, 3)


@fig('fg_bettari', 'Бэттари', 2)
def _(img, cx, b):
    B(img, [(cx - 28, b), (cx - 24, b - 44), (cx - 12, b - 56), (cx + 12, b - 56), (cx + 24, b - 44), (cx + 28, b)], '#a82a24', 101)
    d = ImageDraw.Draw(img)
    fill(img, '#1a1212', 102, rect=(cx - 25, b - 34, cx + 25, b - 24), scale=3); line(img, [(cx - 25, b - 29), (cx + 25, b - 29)], '#c8a040', 1.2)
    d.line([(px(cx - 12), px(b - 56)), (px(cx), px(b - 40)), (px(cx + 12), px(b - 56))], fill=H('#f0e8dc'), width=px(2.4))
    for k in range(6): x, y = cx - 18 + k * 7, b - 14 + (k % 2) * 6; d.ellipse([px(x - 2), px(y - 2), px(x + 2), px(y + 2)], fill=H('#d8b048'))
    O(img, cx, b - 78, 22, 24, '#ede8de', 103, spec=.25)
    d = ImageDraw.Draw(img)
    d.chord([px(cx - 26), px(b - 104), px(cx + 26), px(b - 70)], 180, 360, fill=H('#15110f')); d.ellipse([px(cx - 14), px(b - 122), px(cx + 14), px(b - 98)], fill=H('#15110f'))
    for sx in (-1, 1): d.line([(px(cx + sx * 10), px(b - 112)), (px(cx + sx * 26), px(b - 124))], fill=H('#d8b048'), width=px(1.4))
    d.chord([px(cx - 13), px(b - 76), px(cx + 13), px(b - 58)], 0, 180, fill=H('#3a1614'))
    for k in range(5): d.rectangle([px(cx - 11 + k * 4.6), px(b - 67), px(cx - 8 + k * 4.6), px(b - 63)], fill=H('#141212'))   # blackened teeth
    blush(img, cx, b - 72, 15, 4)


@fig('fg_okubi', 'Оокуби', 2)
def _(img, cx, b):
    rr = random.Random(5)
    for k in range(9): r = rr.uniform(9, 15); x = cx + rr.uniform(-34, 34); y = b - rr.uniform(4, 16); soft(img, lambda d, x=x, y=y, r=r: d.ellipse([px(x - r), px(y - r * .7), px(x + r), px(y + r * .7)], fill=(170, 176, 184, 200)), 2)
    O(img, cx, b - 60, 40, 42, '#ede6da', 111, spec=.25)
    d = ImageDraw.Draw(img)
    d.chord([px(cx - 44), px(b - 110), px(cx + 44), px(b - 44)], 180, 360, fill=H('#15110f'))
    d.rectangle([px(cx - 44), px(b - 78), px(cx - 36), px(b - 44)], fill=H('#15110f')); d.rectangle([px(cx + 36), px(b - 78), px(cx + 44), px(b - 44)], fill=H('#15110f'))
    for sx in (-1, 1): d.ellipse([px(cx + sx * 14 - 7), px(b - 68), px(cx + sx * 14 + 7), px(b - 62)], fill=H('#1a1414')); d.line([(px(cx + sx * 8), px(b - 76)), (px(cx + sx * 20), px(b - 74))], fill=H('#1a1414'), width=px(1.6))
    d.chord([px(cx - 18), px(b - 50), px(cx + 18), px(b - 30)], 0, 180, fill=H('#3a1614'))
    for k in range(7): d.rectangle([px(cx - 15 + k * 4.4), px(b - 40), px(cx - 12 + k * 4.4), px(b - 35)], fill=H('#141212'))
    blush(img, cx, b - 50, 26, 6)


@fig('fg_warashi', 'Дзасики-вараси', 2, secret=True)
def _(img, cx, b):
    B(img, [(cx - 26, b), (cx - 22, b - 40), (cx - 10, b - 52), (cx + 10, b - 52), (cx + 22, b - 40), (cx + 26, b)], '#b42a26', 121)
    d = ImageDraw.Draw(img)
    for k in range(10): x, y = cx - 20 + (k * 11) % 40, b - 44 + (k * 7) % 40; [d.ellipse([px(x + math.cos(a) * 2.4 - 1.6), px(y + math.sin(a) * 2.4 - 1.6), px(x + math.cos(a) * 2.4 + 1.6), px(y + math.sin(a) * 2.4 + 1.6)], fill=H('#f4c4d2')) for a in (0, 1.26, 2.5, 3.8, 5)]
    fill(img, '#e0c060', 122, rect=(cx - 23, b - 32, cx + 23, b - 24), scale=3)
    d.line([(px(cx - 10), px(b - 52)), (px(cx), px(b - 38)), (px(cx + 10), px(b - 52))], fill=H('#f0e8dc'), width=px(2.4))
    O(img, cx + 16, b - 22, 11, 11, '#e8e0d0', 123, spec=.3)                                                     # temari
    for k, c in enumerate(('#c02a2a', '#2a4a8a', '#d8b048')): d = ImageDraw.Draw(img); d.arc([px(cx + 6 + k), px(b - 32 + k * 2), px(cx + 26 - k), px(b - 14 - k * 2)], 20 + k * 40, 200 + k * 40, fill=H(c), width=px(2))
    O(img, cx, b - 78, 22, 23, '#f3e6d4', 124, spec=.2)
    d = ImageDraw.Draw(img)
    d.chord([px(cx - 25), px(b - 104), px(cx + 25), px(b - 68)], 180, 360, fill=H('#15110f'))
    d.rectangle([px(cx - 25), px(b - 86), px(cx - 17), px(b - 64)], fill=H('#15110f')); d.rectangle([px(cx + 17), px(b - 86), px(cx + 25), px(b - 64)], fill=H('#15110f'))
    d.rectangle([px(cx - 18), px(b - 90), px(cx + 18), px(b - 84)], fill=H('#15110f'))
    eyes(img, cx, b - 76, 8, 2.8); blush(img, cx, b - 70, 12, 3.4); d.ellipse([px(cx - 2), px(b - 67), px(cx + 2), px(b - 64)], fill=H('#c0302a'))


# ── Series 3: «Кошки Японии»
@fig('fg_maneki', 'Манэки-нэко', 3)
def _(img, cx, b):
    O(img, cx, b - 30, 28, 30, '#f2eee4', 131)
    for c, x, y, r in (('#d08a3a', cx + 12, b - 44, 8), ('#2a2420', cx - 16, b - 18, 7)): soft(img, lambda d, c=c, x=x, y=y, r=r: d.ellipse([px(x - r), px(y - r * .8), px(x + r), px(y + r * .8)], fill=H(c)), 1)
    O(img, cx - 26, b - 84, 8, 10, '#f2eee4', 132); fill(img, '#f2eee4', 133, rect=(cx - 32, b - 82, cx - 20, b - 50), scale=3)   # beckoning paw
    cat_face(img, cx, b - 72, '#f2eee4', eyes_kind='happy', r=26, seed=134)
    soft(img, lambda d: d.ellipse([px(cx + 8), px(b - 94), px(cx + 24), px(b - 80)], fill=H('#d08a3a')), 1)
    d = ImageDraw.Draw(img); d.rounded_rectangle([px(cx - 20), px(b - 50), px(cx + 20), px(b - 45)], px(2), fill=H('#b8322a'))
    O(img, cx, b - 43, 4, 4, '#e6c048', 135, spec=.5)
    O(img, cx + 6, b - 24, 12, 16, '#e2b84a', 136, spec=.4); text(img, '千両', cx + 6, b - 24, 8, '#6a4a12', SERIF)


@fig('fg_samurai', 'Кот-самурай', 3)
def _(img, cx, b):
    B(img, [(cx - 28, b), (cx - 26, b - 30), (cx - 16, b - 50), (cx + 16, b - 50), (cx + 26, b - 30), (cx + 28, b)], '#2a3a5a', 141)   # hakama
    d = ImageDraw.Draw(img)
    for k in range(4): d.line([(px(cx - 16 + k * 10), px(b - 30)), (px(cx - 18 + k * 12), px(b))], fill=(10, 16, 30, 150), width=px(1.2))
    for sx in (-1, 1): B(img, [(cx + sx * 8, b - 50), (cx + sx * 34, b - 54), (cx + sx * 30, b - 38), (cx + sx * 10, b - 36)], '#5a6a7a', 142 + sx)   # kataginu wings
    line(img, [(cx - 30, b - 30), (cx + 20, b - 44)], '#1a1212', 4); line(img, [(cx + 14, b - 42), (cx + 30, b - 48)], '#c8a040', 3.6)   # the katana at the waist
    cat_face(img, cx, b - 72, '#d8914a', r=25, seed=144, stripes='#9a5a28')
    fill(img, '#1e1c20', 145, poly=[(cx - 28, b - 84), (cx - 24, b - 100), (cx, b - 108), (cx + 24, b - 100), (cx + 28, b - 84), (cx + 34, b - 80), (cx - 34, b - 80)], scale=3)   # kabuto
    volume(img, (cx - 34, b - 108, cx + 34, b - 80), .5, .3, spec=.3)
    B(img, [(cx - 22, b - 104), (cx - 26, b - 126), (cx - 14, b - 108), (cx, b - 112), (cx + 14, b - 108), (cx + 26, b - 126), (cx + 22, b - 104)], '#d8b048', 146, spec=.5)


@fig('fg_kimono', 'Кошка в кимоно', 3)
def _(img, cx, b):
    B(img, [(cx - 28, b), (cx - 24, b - 38), (cx - 12, b - 50), (cx + 12, b - 50), (cx + 24, b - 38), (cx + 28, b)], '#c86a86', 151)
    d = ImageDraw.Draw(img); rr = random.Random(3)
    for k in range(9):
        x, y = cx + rr.uniform(-20, 20), b - rr.uniform(4, 44)
        for a in range(5): q = a * 1.2566; d.ellipse([px(x + math.cos(q) * 2.6 - 1.8), px(y + math.sin(q) * 2.6 - 1.8), px(x + math.cos(q) * 2.6 + 1.8), px(y + math.sin(q) * 2.6 + 1.8)], fill=H('#f6dce4'))
    fill(img, '#d8b048', 152, rect=(cx - 25, b - 34, cx + 25, b - 24), scale=3); volume(img, (cx - 25, b - 34, cx + 25, b - 24), .4, .2, spec=.3)
    d.line([(px(cx - 12), px(b - 50)), (px(cx), px(b - 38)), (px(cx + 12), px(b - 50))], fill=H('#f2ece2'), width=px(2.4))
    cat_face(img, cx, b - 72, '#9a9690', r=25, seed=153)
    for k in range(7):                                                                                              # open fan
        a = math.radians(-160 + k * 16); d = ImageDraw.Draw(img); d.polygon([(px(cx + 26), px(b - 32)), (px(cx + 26 + math.cos(a) * 22), px(b - 32 + math.sin(a) * 22)), (px(cx + 26 + math.cos(a + .28) * 22), px(b - 32 + math.sin(a + .28) * 22))], fill=H('#c02a2a' if k % 2 else '#e8d8b0'))
    O(img, cx + 22, b - 30, 6, 5, '#9a9690', 154)
    ImageDraw.Draw(img).ellipse([px(cx + 10), px(b - 98), px(cx + 22), px(b - 88)], fill=H('#e86a8a'))              # a flower behind the ear


@fig('fg_basket', 'Котёнок в корзинке', 3)
def _(img, cx, b):
    cat_face(img, cx, b - 60, '#b89a78', r=24, seed=161, stripes='#6a5238')
    for sx in (-1, 1): O(img, cx + sx * 14, b - 40, 7, 5, '#c8aa88', 162 + sx)
    pts = [(cx - 38, b - 44), (cx + 38, b - 44), (cx + 30, b), (cx - 30, b)]
    fill(img, '#a8804a', 163, poly=pts, scale=2, stretch=(3, .4), contrast=1.4)
    d = ImageDraw.Draw(img)
    for k in range(9): d.line([(px(cx - 34 + k * 8.5), px(b - 44)), (px(cx - 27 + k * 6.8), px(b))], fill=(70, 46, 20, 170), width=px(1.4))
    for k in range(5): y = b - 38 + k * 8; d.line([(px(cx - 36 + k * 1.6), px(y)), (px(cx + 36 - k * 1.6), px(y))], fill=(210, 176, 120, 120), width=px(1))
    fill(img, '#8a6438', 164, rect=(cx - 40, b - 48, cx + 40, b - 42), scale=2, stretch=(4, .5)); volume(img, (cx - 40, b - 48, cx + 40, b), .45, .3)
    for sx in (-1, 1): O(img, cx + sx * 12, b - 44, 7, 5, '#c8aa88', 165 + sx, spec=.1)


@fig('fg_kuro', 'Чёрный кот на заборе', 3)
def _(img, cx, b):
    for x in (cx - 30, cx + 30): fill(img, '#6a5444', 171 + int(x), rect=(x - 6, b - 58, x + 6, b), scale=3, stretch=(.3, 3), contrast=1.3); poly(img, [(x - 6, b - 58), (x, b - 64), (x + 6, b - 58)], '#6a5444')
    fill(img, '#7a6250', 173, rect=(cx - 46, b - 50, cx + 46, b - 40), scale=3, stretch=(4, .3), contrast=1.2); fill(img, '#7a6250', 174, rect=(cx - 46, b - 22, cx + 46, b - 14), scale=3, stretch=(4, .3), contrast=1.2)
    volume(img, (cx - 46, b - 64, cx + 46, b), .4, .2)
    pts = [(cx + 16, b - 50), (cx + 24, b - 36), (cx + 20, b - 20), (cx + 26, b - 10)]; line(img, ocr(pts, 6), '#1a1618', 5)    # tail hanging down
    B(img, [(cx - 18, b - 48), (cx - 18, b - 70), (cx - 8, b - 82), (cx + 8, b - 82), (cx + 18, b - 70), (cx + 18, b - 48)], '#221e22', 175, spec=.3)
    cat_face(img, cx, b - 96, '#262226', ear_in='#5a3a44', eyes_kind='yellow', r=22, seed=176)
    for sx in (-1, 1): O(img, cx + sx * 8, b - 50, 6, 4, '#2a2628', 177 + sx, spec=.2)


@fig('fg_gold', 'Золотой кот', 3, secret=True)
def _(img, cx, b):
    B(img, [(cx + 18, b - 6), (cx + 38, b - 20), (cx + 36, b - 50), (cx + 28, b - 34), (cx + 22, b - 16)], '#d8a830', 181, spec=.4)
    B(img, [(cx - 22, b), (cx - 24, b - 30), (cx - 14, b - 52), (cx + 14, b - 52), (cx + 24, b - 30), (cx + 22, b)], '#e0b040', 182, spec=.55)
    for sx in (-1, 1): O(img, cx + sx * 9, b - 5, 8, 5, '#e8c050', 183 + sx, spec=.5)
    cat_face(img, cx, b - 72, '#e8b83a', ear_in='#f0c878', eyes_kind='happy', r=25, seed=185)
    volume(img, (cx - 30, b - 100, cx + 30, b), .4, .1, spec=.45)
    d = ImageDraw.Draw(img)
    for x, y, r in ((cx - 30, b - 96, 5), (cx + 32, b - 80, 4), (cx - 34, b - 40, 3.4)):
        d.polygon([(px(x), px(y - r * 2)), (px(x + r * .4), px(y - r * .4)), (px(x + r * 2), px(y)), (px(x + r * .4), px(y + r * .4)), (px(x), px(y + r * 2)), (px(x - r * .4), px(y + r * .4)), (px(x - r * 2), px(y)), (px(x - r * .4), px(y - r * .4))], fill=(255, 246, 200, 240))


def machine():
    """Gachapon machine: clear capsule box on a red cabinet, a picture card, coin slot, crank hub, outlet flap."""
    img = canvas(340, 560); floor_shadow(img, 170, 552, 150, 140)
    fill(img, '#2a2220', 1, rect=(46, 530, 294, 552), scale=4)                                        # plinth
    fill(img, '#b23028', 2, rect=(40, 250, 300, 534), scale=8, contrast=.8); volume(img, (40, 250, 300, 534), .5, .25, spec=.12)
    fill(img, '#8a2420', 3, rect=(34, 238, 306, 258), scale=5); volume(img, (34, 238, 306, 258), .4, .2, spec=.2)
    # the clear box with capsules
    fill(img, '#9aa4a8', 4, rect=(44, 24, 296, 240), scale=10, contrast=.4)
    a = np.asarray(img, np.float32)                      # make the box glassy: lower alpha inside
    a[px(28):px(236), px(50):px(290), 3] *= .45; img = Image.fromarray(a.astype(np.uint8), 'RGBA')
    rr = random.Random(4); cols = ['#d84a4a', '#3a7ad8', '#e8c040', '#48a86a', '#d86aa8', '#8a5ad0', '#e88a3a', '#f2eee6']
    caps = sorted([(rr.uniform(66, 274), 222 - rr.uniform(0, 1) ** .7 * 170, rr.uniform(17, 22), rr.choice(cols), rr.uniform(0, math.tau)) for _ in range(46)], key=lambda c: c[1])
    for x, y, r, c, rot in caps:
        l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l)
        d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=(232, 236, 240, 160))
        d.pieslice([px(x - r), px(y - r), px(x + r), px(y + r)], math.degrees(rot), math.degrees(rot) + 180, fill=H(c))
        img.alpha_composite(l); volume(img, (x - r, y - r, x + r, y + r), .6, .4, spec=.45)
    for k in range(3): soft(img, lambda d, k=k: d.line([(px(70 + k * 30), px(40)), (px(40 + k * 30), px(230))], fill=(255, 255, 255, 60), width=px(8 - k * 2)), 2)
    d = ImageDraw.Draw(img); d.rectangle([px(40), px(20), px(300), px(240)], outline=(200, 210, 214, 200), width=px(4))
    fill(img, '#b23028', 5, rect=(34, 6, 306, 30), scale=5); volume(img, (34, 6, 306, 30), .4, .2, spec=.2)          # lid
    text(img, 'ガチャ', 170, 18, 17, '#f6ecd8', SANS)
    # picture card behind a window
    fill(img, '#efe4c8', 6, rect=(72, 272, 268, 390), scale=6, contrast=.5)
    d = ImageDraw.Draw(img); d.rectangle([px(68), px(268), px(272), px(394)], outline=H('#e8d8b0'), width=px(4))
    text(img, '妖怪', 110, 298, 26, '#1a1210', SERIF, brush=True); text(img, 'ねこ', 226, 298, 22, '#a02a22', SERIF, brush=True)
    for i, c in enumerate(('#6a9a52', '#f2eee6', '#7a5a3a', '#c24030', '#e2b84a', '#262226')):
        x = 96 + i * 30; O(img, x, 346, 11, 11, c, 60 + i, spec=.25); ell(img, (x - 5, 342, x - 1, 346), '#141012'); ell(img, (x + 2, 342, x + 6, 346), '#141012')
    text(img, '一回 百円', 170, 378, 13, '#5a3a22', SERIF)
    # coin slot plate + crank hub + outlet
    fill(img, '#c8ccd0', 7, rect=(76, 408, 144, 468), scale=4, contrast=.5); volume(img, (76, 408, 144, 468), .5, .3, spec=.35)
    ImageDraw.Draw(img).rectangle([px(106), px(420), px(114), px(446)], fill=H('#2a2a2e'))
    O(img, 214, 440, 40, 40, '#d0d4d8', 8, spec=.5, contrast=.5); O(img, 214, 440, 13, 13, '#8a8e92', 9, spec=.4)
    fill(img, '#1a1414', 10, rect=(128, 478, 212, 526), scale=3); volume(img, (128, 478, 212, 526), .3, .4)
    a = np.asarray(img, np.float32); f = Image.new('RGBA', img.size, (0, 0, 0, 0)); fill(f, '#c8d4d8', 11, rect=(130, 480, 210, 506), scale=4, contrast=.3)
    fa = np.asarray(f, np.float32); fa[..., 3] *= .55; img.alpha_composite(Image.fromarray(fa.astype(np.uint8), 'RGBA'))
    volume(img, (40, 238, 300, 534), .3, .15)
    return img


def crank():
    img = canvas(120, 120)
    fill(img, '#c8ccd0', 1, rect=(10, 52, 110, 68), scale=3, contrast=.4); volume(img, (10, 52, 110, 68), .6, .3, spec=.6)
    for x in (10, 110): O(img, x if x > 60 else 16, 60, 12, 12, '#d8dce0', 2 + x, spec=.6, contrast=.4)
    O(img, 104, 60, 12, 12, '#d8dce0', 5, spec=.6, contrast=.4)
    O(img, 60, 60, 16, 16, '#a8acb0', 3, spec=.5, contrast=.4)
    return img


def gacha_all():
    items = [(f[0], f[4]) for f in FIG] + [('machine', finish(machine(), .92, 2.5, 99)), ('crank', finish(crank(), .95, 1.5, 98))]
    pack('fg', items, 1400, 86)
    RECTS['fg']['meta'] = [[f[0], f[1], f[2], 1 if f[3] else 0] for f in FIG]
    prev = Image.new('RGBA', (1400, 330), (38, 42, 40, 255))
    for i, f in enumerate(FIG): prev.alpha_composite(f[4], (10 + (i % 12) * 115, 10 + (i // 12) * 160))
    m = items[-2][1].copy(); m.thumbnail((200, 320)); prev.alpha_composite(m, (1200, 5))
    prev.convert('RGB').save('out/fg_preview.png')


if __name__ == '__main__':
    os.makedirs('out', exist_ok=True)
    what = sys.argv[2] if len(sys.argv) > 2 else 'all'
    if what in ('all', 'fg'): gacha_all()
    if what in ('all', 'sk'): sakura_all()
    old = json.load(open('out/tree_gacha.json')) if os.path.exists('out/tree_gacha.json') else {}
    old.update(RECTS); json.dump(old, open('out/tree_gacha.json', 'w'), ensure_ascii=False)
    print(json.dumps(RECTS, ensure_ascii=False))
