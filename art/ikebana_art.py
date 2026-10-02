#!/usr/bin/env python3
"""«Икебана» (add-on ik): 15 seasonal flowers/branches painted as long transparent stems, 3 vessels for the arranging game
(суйбан, высокая ваза, бамбуковая ваза) and 4 collectible things — all in ONE atlas.
Usage: cd art && python3 ikebana_art.py ../assets/items  →  atlas_ik.webp + art/ikebana.json (rects); preview → art/out/ik_atlas.png"""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P

OUT = sys.argv[1] if len(sys.argv) > 1 else '../assets/items'
HERE = os.path.dirname(os.path.abspath(__file__))
SS = 2
CW, CH = 120, 380                      # a stem cell: base at the bottom centre (60, 378)
BX, BY = 60, 378


def hx(h, a=255):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def mix(a, b, t): return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(4))
def dk(c, k=.35): return mix(c, (0, 0, 0, c[3]), k)
def lt(c, k=.3): return mix(c, (255, 255, 255, c[3]), k)
def L(w, h): return Image.new('RGBA', (w * SS, h * SS), (0, 0, 0, 0))
def S(pts): return [(x * SS, y * SS) for x, y in pts]
def poly(img, pts, col): ImageDraw.Draw(img).polygon(S(pts), fill=col)
def dot(img, x, y, r, col): ImageDraw.Draw(img).ellipse([(x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS], fill=col)
def ln(img, pts, col, w): ImageDraw.Draw(img).line(S(pts), fill=col, width=max(1, int(w * SS)), joint='curve')


def ellpts(cx, cy, rx, ry, a=0.0, n=20):
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + rx * math.cos(t) * ca - ry * math.sin(t) * sa, cy + rx * math.cos(t) * sa + ry * math.sin(t) * ca)
            for t in np.linspace(0, 2 * math.pi, n, endpoint=False)]


def qc(p0, p1, p2, n=24):
    return [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1])
            for u in np.linspace(0, 1, n)]


def stroke(img, pts, w0, w1, col, hi=None):
    """A tapered stem/branch: quads between points, round joints; an optional lit edge on the left."""
    d = ImageDraw.Draw(img); n = len(pts)
    for i in range(n - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]; a = w0 + (w1 - w0) * i / (n - 1); b = w0 + (w1 - w0) * (i + 1) / (n - 1)
        dx, dy = x1 - x0, y1 - y0; l = math.hypot(dx, dy) or 1; nx, ny = -dy / l, dx / l
        q = [(x0 + nx * a / 2, y0 + ny * a / 2), (x1 + nx * b / 2, y1 + ny * b / 2), (x1 - nx * b / 2, y1 - ny * b / 2), (x0 - nx * a / 2, y0 - ny * a / 2)]
        d.polygon(S(q), fill=col); r = b / 2 * SS; d.ellipse([x1 * SS - r, y1 * SS - r, x1 * SS + r, y1 * SS + r], fill=col)
    if hi:
        for i in range(n - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]; a = w0 + (w1 - w0) * i / (n - 1)
            dx, dy = x1 - x0, y1 - y0; l = math.hypot(dx, dy) or 1; nx, ny = -dy / l, dx / l
            if nx > 0: nx, ny = -nx, -ny
            d.line(S([(x0 + nx * a * .25, y0 + ny * a * .25), (x1 + nx * a * .25, y1 + ny * a * .25)]), fill=hi, width=max(1, int(a * .3 * SS)))


def leaf(img, bx, by, ang, ln_, wd, col, curl=0.0, rib=True, shape=.8):
    """Lanceolate leaf from (bx,by) along angle `ang` (0 = up), bent by `curl`; lit left half, dark right half, midrib."""
    ax, ay = math.sin(ang), -math.cos(ang); nx, ny = -ay, ax
    def p(t, s):
        bend = curl * ln_ * t * t
        return (bx + ax * ln_ * t + nx * (s * wd * math.sin(math.pi * min(1, t)) ** shape + bend), by + ay * ln_ * t + ny * (s * wd * math.sin(math.pi * min(1, t)) ** shape + bend))
    ts = np.linspace(0, 1, 16)
    left = [p(t, -.5) for t in ts]; right = [p(t, .5) for t in ts]; mid = [p(t, 0) for t in ts]
    poly(img, left + mid[::-1], lt(col, .12)); poly(img, mid + right[::-1], dk(col, .22))
    if rib: ln(img, mid[:-2], dk(col, .4), max(.6, wd * .07))


def flower5(img, cx, cy, r, col, ctr, a0=0.0, n=5, petal=.62):
    for i in range(n):
        a = a0 + i * 2 * math.pi / n
        poly(img, ellpts(cx + math.cos(a) * r * .55, cy + math.sin(a) * r * .55, r * .55, r * petal * .55 / .62 * .62, a), mix(col, dk(col, .2), (i % 2) * .5))
    for i in range(n):
        a = a0 + i * 2 * math.pi / n
        poly(img, ellpts(cx + math.cos(a) * r * .42, cy + math.sin(a) * r * .42 - r * .06, r * .32, r * .22, a), lt(col, .25))
    dot(img, cx, cy, r * .22, ctr)


def finish(img, w, h, seed, sat=.86, tex=.32, edge=.5):
    """Painterly finish: noise mottling, darker soft edges, muted colour; downsample to w×h."""
    a = np.asarray(img, np.float32)
    n = P.fbm(img.width, img.height, 7 * SS, 4, seed)
    a[..., :3] *= (1 - tex / 2 + tex * n)[..., None]
    al = a[..., 3] / 255; bl = np.asarray(Image.fromarray((al * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6 * SS)), np.float32) / 255
    e = np.clip((al - bl) * 2.2, 0, 1); a[..., :3] *= (1 - edge * e)[..., None]
    lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True); a[..., :3] = lum + (a[..., :3] - lum) * sat
    out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').resize((w, h), Image.LANCZOS)
    return out


# ───────────── the 15 materials ─────────────
G1, G2, G3 = hx('#4d7a4a'), hx('#3c6a48'), hx('#5f8a52')
BARK, BARK2 = hx('#4a3426'), hx('#2f2219')


def branch_pts(seed, h, lean, wig=10):
    r = random.Random(seed); pts = []; x, y = BX, BY
    for i in range(9):
        t = i / 8; pts.append((BX + lean * h * t * t + r.uniform(-wig, wig) * (t > 0), BY - h * t))
    return pts


def twig(pts, at, side, ln_, up=.55):
    i = int(at * (len(pts) - 1)); x, y = pts[i]
    return [(x, y), (x + side * ln_ * .6, y - ln_ * up * .7), (x + side * ln_, y - ln_ * up)]


def sakura(img, seed=1, col=hx('#efc3cf'), ctr=hx('#b4506c'), ume=False):
    r = random.Random(seed); m = branch_pts(seed, 350, -.02, 7)
    stroke(img, m, 7, 2, BARK2 if ume else BARK, hi=lt(BARK, .15))
    tw = [twig(m, .35, 1, 44, .9), twig(m, .55, -1, 40, .8), twig(m, .75, 1, 32, .7)]
    for t in tw: stroke(img, t, 3, 1.4, BARK2 if ume else BARK)
    spots = [p for t in tw for p in t[1:]] + m[3:]
    for (x, y) in spots:
        for k in range(2 if ume else 3):
            fx, fy = x + r.uniform(-9, 9), y + r.uniform(-10, 6)
            if not ume and r.random() < .35: leaf(img, fx, fy, r.uniform(-1.4, 1.4), 14, 6, hx('#6a8a4a'), rib=False)
            flower5(img, fx, fy, r.uniform(6.5, 8.5), col, ctr, r.uniform(0, 6))
            if ume: [dot(img, fx + math.cos(q) * 2.6, fy + math.sin(q) * 2.6, .9, hx('#e8c24a')) for q in np.linspace(0, 6.28, 6, endpoint=False)]
    for (x, y) in spots[::2]: dot(img, x + r.uniform(-4, 4), y - r.uniform(2, 8), 3, mix(col, ctr, .5))   # buds


def tsubaki(img, seed=3):
    r = random.Random(seed); m = branch_pts(seed, 300, .1, 5); stroke(img, m, 5, 2, hx('#3a3020'), hi=hx('#55472f'))
    for i, (x, y) in enumerate(m[2:-1]):
        s = 1 if i % 2 else -1; leaf(img, x, y, s * r.uniform(.5, 1.1), r.uniform(34, 42), 18, hx('#24452c'), curl=.08 * s)
    x, y = m[-1]; leaf(img, x, y + 10, -.6, 36, 17, hx('#24452c'), curl=-.1); leaf(img, x, y + 6, .8, 32, 16, hx('#2a4d30'))
    red = hx('#a3263a')
    for i in range(6): a = i * 1.047 + .3; poly(img, ellpts(x + math.cos(a) * 9, y - 6 + math.sin(a) * 8, 12, 10, a), mix(red, dk(red, .3), (i % 2) * .6))
    poly(img, ellpts(x, y - 9, 9, 6, 0), lt(red, .1)); dot(img, x, y - 7, 4.5, hx('#e2c048'))
    for q in range(7): dot(img, x + r.uniform(-3, 3), y - 7 + r.uniform(-3, 2), 1.2, hx('#f3e08a'))
    bx, by = m[4]; dot(img, bx + 14, by - 6, 6, red); poly(img, ellpts(bx + 14, by - 3, 6, 4, 0), hx('#2a4d30'))   # a bud


def suisen(img, seed=4):
    r = random.Random(seed)
    for k, (a, l) in enumerate([(-.12, 250), (.1, 220), (-.25, 180), (.22, 160)]): leaf(img, BX + k * 2 - 3, BY, a, l, 9, hx('#4a7a62'), curl=.05 * (1 if a > 0 else -1), shape=.35)
    st = qc((BX, BY), (BX + 4, BY - 160), (BX - 6, BY - 290)); stroke(img, st, 4, 3, hx('#5c8a5a'))
    tx, ty = st[-1]; poly(img, [(tx - 2, ty), (tx + 6, ty - 14), (tx + 3, ty + 4)], hx('#c8b48a'))   # papery spathe
    for k, (dx, dy, a) in enumerate([(-14, 14, -1.2), (12, 10, 1.1), (-2, -4, .1)]):
        fx, fy = tx + dx, ty + dy; ln(img, [(tx, ty), (fx, fy)], hx('#5c8a5a'), 1.5)
        flower5(img, fx, fy, 10, hx('#f1ede0'), hx('#e6b43c'), a, 6, .7); dot(img, fx, fy, 3.6, hx('#e9a53a')); dot(img, fx, fy, 1.6, hx('#c2722a'))


def ayame(img, seed=5):
    r = random.Random(seed)
    for k, (a, l) in enumerate([(-.08, 260), (.07, 230), (-.2, 190), (.18, 150)]): leaf(img, BX + k * 3 - 4, BY, a, l, 11, hx('#3f6e45'), shape=.3)
    st = qc((BX, BY), (BX - 3, BY - 180), (BX + 4, BY - 320)); stroke(img, st, 4, 3, hx('#4f7c4a'))
    x, y = st[-1]; pu = hx('#4d3f93')
    for s in (-1, 1): poly(img, ellpts(x + s * 13, y + 10, 15, 7, s * .9), dk(pu, .1)); dot(img, x + s * 12, y + 9, 2.5, hx('#e2c048'))
    poly(img, ellpts(x, y + 14, 7, 14, 0), pu)
    for s in (-1, 0, 1): poly(img, ellpts(x + s * 6, y - 10, 5, 12, s * .35), lt(pu, .18))
    dot(img, x, y + 12, 2.2, hx('#f2dc6a'))
    bx, by = st[14]; poly(img, ellpts(bx + 3, by - 8, 4, 11, .1), dk(pu, .2))   # a bud


def ajisai(img, seed=6):
    r = random.Random(seed); st = qc((BX, BY), (BX + 8, BY - 140), (BX - 4, BY - 250)); stroke(img, st, 5, 4, hx('#5a6e3a'), hi=hx('#7a8a4a'))
    for i, t in enumerate((6, 11, 16)):
        x, y = st[t]; s = 1 if i % 2 else -1; leaf(img, x, y, s * 1.0, 44, 26, hx('#3b6a3e'), curl=.06 * s)
    cx, cy = st[-1][0], st[-1][1] - 22
    for k in range(70):
        a = r.uniform(0, 6.28); d = 34 * math.sqrt(r.random()); fx, fy = cx + math.cos(a) * d, cy + math.sin(a) * d * .85
        c = mix(hx('#6f86c8'), hx('#9a7ec4'), r.random()); c = lt(c, .25 * (1 - (fy - cy + 30) / 60))
        for q in range(4): qa = q * 1.57 + a; poly(img, ellpts(fx + math.cos(qa) * 3.2, fy + math.sin(qa) * 3.2, 3.6, 2.6, qa), mix(c, dk(c, .2), q % 2 * .7))
        dot(img, fx, fy, .9, hx('#e8e4f4'))


def hasu(img, seed=7):
    r = random.Random(seed); st = qc((BX, BY), (BX - 10, BY - 170), (BX + 6, BY - 300)); stroke(img, st, 5, 4, hx('#5e7a46'), hi=hx('#7e9a5a'))
    for (x, y) in st[2:-2:3]: dot(img, x + 1, y, .9, hx('#3e5a30'))
    x, y = st[-1]; pk = hx('#e3a1b4'); tip = hx('#c4547a')
    for k, (a, w, l) in enumerate([(-1.0, 9, 30), (1.0, 9, 30), (-.55, 10, 36), (.55, 10, 36), (-.2, 11, 40), (.2, 11, 40), (0, 10, 42)]):
        ax, ay = math.sin(a), -math.cos(a); pts = [(x + ax * l * t + ay * w * math.sin(math.pi * t) * s, y + ay * l * t - ax * w * math.sin(math.pi * t) * s) for s in (1, -1) for t in (np.linspace(0, 1, 10) if s > 0 else np.linspace(1, 0, 10))]
        c = mix(pk, lt(pk, .3), k / 6); poly(img, pts, c); poly(img, ellpts(x + ax * l * .86, y + ay * l * .86, w * .35, w * .55, a), tip)
    dot(img, x, y - 4, 6, hx('#e2c04a'))
    lx, ly = st[7]; stroke(img, [(lx, ly), (lx + 26, ly - 30), (lx + 34, ly - 44)], 2.5, 2, hx('#5e7a46'))
    poly(img, ellpts(lx + 36, ly - 50, 22, 8, -.35), hx('#4c7a44')); poly(img, ellpts(lx + 36, ly - 52, 16, 4, -.35), hx('#6a9a5a'))   # a young leaf


def asagao(img, seed=8):
    r = random.Random(seed); ln(img, [(BX + 2, BY), (BX + 4, BY - 340)], hx('#b49a6a'), 2.2)   # a thin bamboo stake
    pts = [(BX + 3 + 11 * math.sin(i * .32), BY - i * 7.4) for i in range(44)]; stroke(img, pts, 2.6, 1.6, hx('#5a7a3e'))
    for i in range(5, 40, 7):
        x, y = pts[i]; s = 1 if (i // 7) % 2 else -1; ln(img, [(x, y), (x + s * 10, y - 4)], hx('#5a7a3e'), 1.2)
        hx_, hy = x + s * 17, y - 6; c = hx('#4a7a3c')
        poly(img, [(x + s * 10, y - 4)] + [(hx_ + 12 * math.sin(t) * .95 * s, hy - 13 * math.cos(t) + 4 * math.cos(2 * t)) for t in np.linspace(0, 2 * math.pi, 18)], c)
        ln(img, [(x + s * 10, y - 4), (hx_ + s * 6, hy - 6)], dk(c, .3), .8)
    bl = hx('#3e5fb4')
    for (i, s) in ((24, 1), (36, -1)):
        x, y = pts[i]; fx, fy = x + s * 13, y - 14; ln(img, [(x, y), (fx, fy)], hx('#5a7a3e'), 1.3)
        poly(img, ellpts(fx, fy, 15, 13, s * .3), bl); poly(img, ellpts(fx - 2, fy - 2, 11, 9, s * .3), lt(bl, .15))
        for q in range(5): a = q * 1.256 + .3; ln(img, [(fx, fy), (fx + math.cos(a) * 11, fy + math.sin(a) * 10)], lt(bl, .45), 1)
        dot(img, fx, fy, 3.8, hx('#efe9f2'))
    x, y = pts[30]; poly(img, ellpts(x - 9, y - 6, 3.4, 9, -.5), dk(bl, .1))   # a furled bud


def kiku(img, seed=9, col=hx('#e2b84a')):
    r = random.Random(seed); st = qc((BX, BY), (BX + 6, BY - 150), (BX - 2, BY - 280)); stroke(img, st, 4, 3, hx('#4c6a3a'))
    for i, t in enumerate((5, 9, 13, 17)):
        x, y = st[t]; s = 1 if i % 2 else -1
        for k in range(3): leaf(img, x, y, s * (.8 + k * .35) + r.uniform(-.1, .1), 22 - k * 3, 11, hx('#3b5a36'), rib=False)
    x, y = st[-1]; y -= 6
    for ring, (rr, nn, c) in enumerate([(30, 30, dk(col, .18)), (23, 26, col), (15, 20, lt(col, .15))]):
        for k in range(nn):
            a = k * 6.283 / nn + ring * .2; poly(img, ellpts(x + math.cos(a) * rr * .55, y + math.sin(a) * rr * .45, rr * .5, 2.2, a), mix(c, dk(c, .15), k % 2 * .6))
    dot(img, x, y, 5, dk(col, .1)); dot(img, x - 1, y - 1, 3, lt(col, .3))
    bx, by = st[15]; ln(img, [(bx, by), (bx - 16, by - 18)], hx('#4c6a3a'), 1.5); dot(img, bx - 17, by - 20, 5, mix(col, hx('#6a8a4a'), .5))


def susuki(img, seed=10):
    r = random.Random(seed)
    for k, (a, l, c) in enumerate([(-.5, 200, -.18), (.35, 230, .2), (-.15, 260, -.12), (.6, 150, .25)]): leaf(img, BX, BY, a, l, 6, hx('#6a7a4a'), curl=c, shape=.3, rib=False)
    st = qc((BX, BY), (BX + 4, BY - 200), (BX + 30, BY - 330)); stroke(img, st, 2.6, 1.6, hx('#8a8a5a'))
    x, y = st[-6]
    for k in range(26):
        ox, oy = st[-6 + int(k / 26 * 5)]; a = r.uniform(.6, 2.0); l = r.uniform(30, 55)
        pts = qc((ox, oy), (ox + math.cos(a - 1.57) * l * .5 + 10, oy - 6), (ox + 14 + math.sin(a) * l * .6, oy + l * .45))
        ln(img, pts, mix(hx('#d8c8a0'), hx('#b8a07a'), r.random()), r.uniform(1.2, 2.2))
    for k in range(40): p = st[-6 + r.randint(0, 5)]; dot(img, p[0] + r.uniform(4, 30), p[1] + r.uniform(0, 40), 1.1, hx('#efe2c2', 200))


def momiji(img, seed=11):
    r = random.Random(seed); m = branch_pts(seed, 330, .03, 6); stroke(img, m, 5, 1.6, hx('#5a2a22'), hi=hx('#7a3a2a'))
    tw = [twig(m, .4, -1, 42, .7), twig(m, .62, 1, 36, .8), twig(m, .82, -1, 28, .6)]
    for t in tw: stroke(img, t, 2.4, 1.2, hx('#5a2a22'))
    def palm(x, y, s, a, c):
        pts = []
        for k in range(14):
            q = a + (k / 14) * 6.283; rr = s if k % 2 == 0 else s * .42; pts.append((x + math.sin(q) * rr, y - math.cos(q) * rr * .95))
        poly(img, pts, c); [ln(img, [(x, y), (x + math.sin(a + k * .898) * s * .8, y - math.cos(a + k * .898) * s * .8)], dk(c, .25), .6) for k in range(7)]
    spots = [p for t in tw for p in t[1:]] + m[4::2]
    for (x, y) in spots:
        for k in range(2):
            c = mix(hx('#b8402a'), hx('#d8782a'), r.random()); palm(x + r.uniform(-10, 10), y + r.uniform(-6, 8), r.uniform(9, 13), r.uniform(-.6, .6), c)


def hagi(img, seed=12):
    r = random.Random(seed)
    for k, (lean, h) in enumerate([(-.26, 300), (.22, 330), (-.05, 250)]):
        pts = qc((BX, BY), (BX + lean * 40, BY - h * .6), (BX + lean * 150, BY - h)); stroke(img, pts, 2.6, 1.2, hx('#6a4a32'))
        for i in range(5, 24, 2):
            x, y = pts[i]; s = 1 if i % 4 else -1
            for q in range(3): leaf(img, x, y, s * 1.2 + (q - 1) * .5, 8, 6, hx('#4a6a3a'), rib=False)
            if i > 12:
                for q in range(2): dot(img, x + s * r.uniform(3, 9), y - r.uniform(2, 8), 2.6, mix(hx('#b84a8a'), hx('#d47aa8'), r.random()))


def matsu(img, seed=13):
    r = random.Random(seed); m = branch_pts(seed, 320, -.18, 12); stroke(img, m, 9, 3, hx('#3e2c20'), hi=hx('#5a4430'))
    tw = [twig(m, .45, 1, 50, .4), twig(m, .68, -1, 46, .5)]
    for t in tw: stroke(img, t, 4, 2, hx('#3e2c20'))
    for (x, y) in [t[-1] for t in tw] + [t[1] for t in tw] + [m[-1], m[-3], m[-5]]:
        for layer, c in ((0, hx('#24402c')), (1, hx('#3a6040')), (2, hx('#5e8456'))):
            for k in range(44):
                a = -1.5 + r.uniform(-1.5, 1.5) + layer * .1; l = r.uniform(20, 32) - layer * 4
                ln(img, [(x, y - layer * 2), (x + math.cos(a) * l, y + math.sin(a) * l * .6 - layer * 2)], c, 1.3)
        dot(img, x, y, 2.4, hx('#5a4430'))


def nanten(img, seed=14):
    r = random.Random(seed); st = qc((BX, BY), (BX - 6, BY - 160), (BX + 2, BY - 300)); stroke(img, st, 4, 2.4, hx('#5a4a2a'))
    for i, t in enumerate((7, 12, 17, 21)):
        x, y = st[t]; s = 1 if i % 2 else -1; ex, ey = x + s * 36, y - 16; ln(img, [(x, y), (ex, ey)], hx('#6a5a32'), 1.2)
        for q in range(5):
            u = (q + 1) / 6; px_, py_ = x + (ex - x) * u, y + (ey - y) * u
            c = mix(hx('#3e6a3a'), hx('#a84a2a'), r.random() * .5 + (.3 if i == 0 else 0))
            leaf(img, px_, py_, s * 1.0 - .7, 15, 6, c, rib=False); leaf(img, px_, py_, s * 1.0 + .7, 15, 6, c, rib=False)
    x, y = st[-1]
    for k in range(22):
        a = r.uniform(-1.2, 1.2); d = r.uniform(4, 26); bx, by = x + math.sin(a) * d * .8, y + 6 + d * .7
        ln(img, [(x, y), (bx, by)], hx('#7a5a32'), .8); dot(img, bx, by, 4, hx('#b8222a')); dot(img, bx - 1.2, by - 1.3, 1.4, hx('#f08a7a'))


def take(img, seed=15):
    r = random.Random(seed); pts = [(BX + 2 * math.sin(i * .2), BY - i * 30) for i in range(12)]
    stroke(img, pts, 14, 10, hx('#6e8a3a'), hi=hx('#9ab25a'))
    for y in (BY - 95, BY - 190, BY - 275): ln(img, [(BX - 7, y), (BX + 7, y)], hx('#3e5a22'), 2); ln(img, [(BX - 6, y - 2), (BX + 6, y - 2)], hx('#b8c87a'), 1)
    for k, (y, s) in enumerate(((BY - 190, 1), (BY - 275, -1), (BY - 320, 1))):
        bx = BX + s * 5; ex, ey = bx + s * 40, y - 30; ln(img, [(bx, y), (ex, ey)], hx('#6e8a3a'), 1.6)
        for q in range(4): leaf(img, ex - s * q * 6, ey + q * 4, s * (1.2 + q * .35) - .2, 34, 6, hx('#4c7a3a'), curl=.08 * s, shape=.5)


FL = [  # id, name, seasons, kind (line = branch/linear, mass = flower), painter, petal colour (falls when it wilts)
    ('sakura', 'Сакура', 'spring', 'line', sakura, '#efc3cf'),
    ('ume', 'Слива умэ', 'spring', 'line', lambda i: sakura(i, 2, hx('#f3e7ea'), hx('#c4506a'), True), '#f3e7ea'),
    ('tsubaki', 'Камелия', 'spring', 'mass', tsubaki, '#a3263a'),
    ('suisen', 'Нарцисс', 'spring,winter', 'mass', suisen, '#f1ede0'),
    ('ayame', 'Ирис', 'summer', 'line', ayame, '#4d3f93'),
    ('ajisai', 'Гортензия', 'summer', 'mass', ajisai, '#7a8ac8'),
    ('hasu', 'Лотос', 'summer', 'mass', hasu, '#e3a1b4'),
    ('asagao', 'Вьюнок', 'summer', 'line', asagao, '#3e5fb4'),
    ('kiku', 'Хризантема', 'autumn', 'mass', kiku, '#e2b84a'),
    ('susuki', 'Мискант сусуки', 'autumn', 'line', susuki, '#d8c8a0'),
    ('momiji', 'Клён', 'autumn', 'line', momiji, '#c0502a'),
    ('hagi', 'Хаги', 'autumn', 'mass', hagi, '#c45a98'),
    ('matsu', 'Сосна', 'winter', 'line', matsu, '#2f5236'),
    ('nanten', 'Нандина', 'winter', 'mass', nanten, '#b8222a'),
    ('take', 'Бамбук', 'winter', 'line', take, '#6e8a3a'),
]


# ───────────── vessels: lathe-shaded profiles ─────────────
def lathe(w, h, prof, base, lx=-.5, spec=.35, seed=0, tex=.18):
    """prof(y) → half-width in px (None = empty row); cylindrical shading lit from the upper left."""
    W_, H_ = w * SS, h * SS; a = np.zeros((H_, W_, 4), np.float32); cx = W_ / 2
    n = P.fbm(W_, H_, 9 * SS, 4, seed)
    for y in range(H_):
        r = prof(y / SS)
        if r is None or r <= 0: continue
        r *= SS; x0, x1 = int(max(0, cx - r)), int(min(W_, cx + r + 1))
        xs = (np.arange(x0, x1) - cx) / r; xs = np.clip(xs, -1, 1); nz = np.sqrt(1 - xs ** 2)
        lit = .45 + .65 * np.clip(-lx * -xs + .75 * nz, 0, 1.2); sp = np.exp(-((xs + .45) / .12) ** 2) * spec
        c = np.array(base[:3], np.float32)[None, :] * lit[:, None] * (1 - tex / 2 + tex * n[y, x0:x1])[:, None] + sp[:, None] * 255
        a[y, x0:x1, :3] = c; a[y, x0:x1, 3] = 255 * np.clip((1 - np.abs(xs)) * r / 1.2, 0, 1)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def suiban():
    w, h = 230, 76; img = L(w, h)
    body = lathe(w, h, lambda y: None if y < 16 else 112 - max(0, y - 52) ** 1.6 * .35 if y < 70 else None, hx('#2c3446'), seed=21, spec=.25)
    img.alpha_composite(body)
    poly(img, ellpts(115, 17, 113, 15), hx('#4a556c')); poly(img, ellpts(115, 18, 106, 12), hx('#121821'))
    poly(img, ellpts(150, 16, 26, 3.2, .02), hx('#3a4660', 200)); poly(img, ellpts(80, 20, 40, 2, 0), hx('#28324a', 220))
    for x in (50, 180): poly(img, ellpts(x, 71, 14, 4), hx('#1a1f2a'))
    return finish(img, w, h, 31, sat=.9, tex=.1, edge=.3)


def heika():
    w, h = 124, 214; img = L(w, h)
    def pr(y):
        if y < 2: return None
        if y < 14: return 30 - (y - 2) * .9                     # flared mouth
        if y < 46: return 19 + (y - 14) * .08                   # neck
        if y < 120: t = (y - 46) / 74; return 22 + 38 * math.sin(t * math.pi / 2) ** .8
        if y < 206: t = (y - 120) / 86; return 60 - 22 * t ** 1.6
        if y < 212: return 36
        return None
    img.alpha_composite(lathe(w, h, pr, hx('#5f7a70'), seed=22, spec=.45))
    poly(img, ellpts(62, 4, 30, 4.5), hx('#7d988c')); poly(img, ellpts(62, 4.5, 23, 3), hx('#141a18'))
    for k in range(9): y = 128 + k * 9; ln(img, [(62 - 55 + k * 1.8, y), (62 + 55 - k * 1.8, y + 1)], hx('#56706a', 90), 1)   # throwing rings
    return finish(img, w, h, 32, sat=.9, tex=.12, edge=.3)


def takezutsu():
    w, h = 92, 236; img = L(w, h)
    img.alpha_composite(lathe(w, h, lambda y: None if y < 6 else 36 + (2.5 if abs(y - 92) < 4 or abs(y - 200) < 4 else 0) if y < 232 else None, hx('#6e7040'), seed=23, spec=.22, tex=.3))
    for y in (92, 200): ln(img, [(12, y), (80, y)], hx('#4e5228'), 1.6); ln(img, [(12, y - 3), (80, y - 3)], hx('#c8c88a'), 1)
    r = random.Random(4)
    for k in range(14): x = r.uniform(18, 74); ln(img, [(x, r.uniform(10, 80)), (x + r.uniform(-1, 1), r.uniform(100, 225))], hx('#6e6e38', 70), .8)
    poly(img, ellpts(46, 7, 36, 5), hx('#9a9658')); poly(img, ellpts(46, 7.5, 31, 3.6), hx('#1e1e10'))
    return finish(img, w, h, 33, sat=.9, tex=.15, edge=.35)


def kenzan():
    w, h = 124, 62; img = L(w, h)
    img.alpha_composite(lathe(w, h, lambda y: None if y < 30 else 54 if y < 58 else None, hx('#4a4c50'), seed=24, spec=.25))
    poly(img, ellpts(62, 31, 54, 12), hx('#5e6064')); r = random.Random(5)
    for k in range(120):
        a = r.uniform(0, 6.28); d = math.sqrt(r.random()); x, y = 62 + math.cos(a) * d * 48, 31 + math.sin(a) * d * 10
        ln(img, [(x, y), (x, y - 14)], hx('#b89a5a'), .9); dot(img, x, y - 14, .7, hx('#e2cc8a'))
    return finish(img, w, h, 34, sat=.95, tex=.08, edge=.25)


def kago():
    w, h = 170, 190; img = L(w, h)
    img.alpha_composite(lathe(w, h, lambda y: None if y < 60 else 60 + (y - 60) * .12 if y < 180 else 70 - (y - 180) * 2 if y < 188 else None, hx('#7a5a36'), seed=25, spec=.15, tex=.35))
    for k in range(14): y = 66 + k * 8.5; ln(img, [(85 - 60 - k, y), (85 + 60 + k, y + 2)], hx('#4a3220', 160), 1.2)
    for k in range(13): x = 30 + k * 9; ln(img, [(x, 62), (x - 4 + k * .6, 184)], hx('#a07a4a', 140), 1)
    ln(img, qc((28, 64), (85, -60), (142, 64), 30), hx('#5a4026'), 4); ln(img, qc((30, 63), (85, -56), (140, 63), 30), hx('#9a7448'), 1.4)
    poly(img, ellpts(85, 62, 60, 7), hx('#8a6a40')); poly(img, ellpts(85, 63, 54, 5), hx('#24180e'))
    return finish(img, w, h, 35, sat=.9, tex=.12, edge=.35)


def compose(vessel, vw, vh, stems, w, h, mouth):
    """A thing for the shop: vessel with stems already in it (stems = [(stem image, angle, scale, dx)])."""
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); vx, vy = (w - vw) // 2, h - vh
    for im, ang, sc, dx in stems:
        s = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS); big = Image.new('RGBA', (s.width * 3, s.height * 2), (0, 0, 0, 0))
        big.alpha_composite(s, (s.width, 0)); rot = big.rotate(-math.degrees(ang), resample=Image.BICUBIC, center=(s.width * 1.5, s.height))
        img.alpha_composite(rot, (int(w / 2 + dx - s.width * 1.5), int(vy + mouth - s.height)))
    img.alpha_composite(vessel, (vx, vy)); img = img.crop(img.getbbox())
    return img.resize((int(img.width * .68), int(img.height * .68)), Image.LANCZOS)


def main():
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    stems = {}
    for i, (fid, name, sea, kind, fn, pc) in enumerate(FL):
        img = L(CW, CH); fn(img); st = finish(img, CW, CH, 100 + i); bb = st.split()[3].point(lambda v: 255 if v > 12 else 0).getbbox()
        stems[fid] = (st, bb[1]); print(fid, 'top', bb[1])
    V = {'suiban': suiban(), 'heika': heika(), 'take': takezutsu()}
    kz = kenzan()
    th = lambda f: stems[f][0]
    items = {
        'ik_kenzan': kz,
        'ik_suiban': compose(V['suiban'], 230, 76, [(th('ayame'), -.22, .78, -16), (th('ayame'), -.62, .6, -10), (th('ajisai'), .9, .5, 12), (th('asagao'), .25, .5, 0)], 250, 330, 18),
        'ik_take': compose(V['take'], 92, 236, [(th('tsubaki'), -.3, .62, 0), (th('ume'), .5, .55, 2)], 150, 420, 6),
        'ik_kago': compose(kago(), 170, 190, [(th('susuki'), -.25, .72, -4), (th('hagi'), .45, .62, 6), (th('kiku'), -.7, .5, -6), (th('kiku'), .15, .45, 4)], 220, 400, 64),
    }
    # pack: two rows of stems (cells 120 wide, tight in height), then vessels, then the things
    R = {}; rows = [[f[0] for f in FL[:8]], [f[0] for f in FL[8:]]]; y = 0; Wd = 8 * (CW + 2)
    for row in rows:
        hmax = max(CH - stems[f][1] for f in row)
        for i, f in enumerate(row): R[f] = [i * (CW + 2), y, CW, CH - stems[f][1]]
        y += hmax + 2
    x = 0; hrow = 0; tail = [('v_suiban', V['suiban']), ('v_heika', V['heika']), ('v_take', V['take'])] + list(items.items())
    for k, im in tail:
        if x + im.width > Wd: x = 0; y += hrow + 2; hrow = 0
        R[k] = [x, y, im.width, im.height]; x += im.width + 2; hrow = max(hrow, im.height)
    H_ = y + hrow
    atl = Image.new('RGBA', (Wd, H_), (0, 0, 0, 0))
    for f in stems: s, top = stems[f]; atl.alpha_composite(s.crop((0, top, CW, CH)), tuple(R[f][:2]))
    for k, im in tail: atl.alpha_composite(im, tuple(R[k][:2]))
    atl.save(os.path.join(OUT, 'atlas_ik.webp'), 'WEBP', quality=86, alpha_quality=88, method=6)
    meta = {'size': [Wd, H_], 'r': R, 'fl': [[f[0], f[1], f[2], f[3], f[5]] for f in FL]}
    json.dump(meta, open(os.path.join(HERE, 'ikebana.json'), 'w'), ensure_ascii=False)
    pv = Image.new('RGBA', atl.size, (38, 34, 30, 255)); pv.alpha_composite(atl); pv.convert('RGB').save(os.path.join(HERE, 'out', 'ik_atlas.png'))
    print('atlas', Wd, H_, os.path.getsize(os.path.join(OUT, 'atlas_ik.webp')) // 1024, 'KB'); print(json.dumps(R))


if __name__ == '__main__':
    main()
