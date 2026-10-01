#!/usr/bin/env python3
"""«Питомец Муси»: a little bakeneko kitten in 3 growth stages × 5 poses (+ the wet box at the gate), and its 3 things.
Same organic spline toolkit as story_art.py / guests_art.py. Every frame is 280×250, facing right, floor at y=238.
Usage: pet2_art.py <assets dir>  → assets/mon/m_pt_atlas.webp, assets/items/atlas_pt.webp (+ previews in art/out);
prints the rect JSON that feat/pet2.js embeds."""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
ASSETS = sys.argv[1]
sys.argv = [sys.argv[0], os.path.join(ASSETS, 'mon')]   # monsters.py reads its OUT from argv[1]
import paint as P
from paint import hexc, mixc
import monsters as M
from monsters import canvas, px, soft
from story_art import cr, shape, clipped, poly_s
from guests_art import tube, fur_ticks, stroke

FW, FH, CX, FY = 280, 250, 140, 238
FUR, FUR_D, FUR_L = hexc('#cdc4b6'), hexc('#a2978a'), hexc('#ddd5c8')
WHT, PINK, INK = hexc('#f3eee5'), hexc('#dd9d9d'), (58, 48, 44, 255)
STRIPE = (104, 92, 84, 150)
EYE = [hexc('#e9b04a'), hexc('#e8a83a'), hexc('#f1c64a')]
# stage: head r, half body length, body half height, legs, tail length, split share, ear size, paw width
G = [dict(hr=40, bl=32, bh=23, lg=14, tl=34, sp=.42, ear=.86, pw=7),
     dict(hr=34, bl=42, bh=24, lg=24, tl=62, sp=.5, ear=.82, pw=7.5),
     dict(hr=31, bl=48, bh=25, lg=31, tl=82, sp=1.0, ear=.8, pw=8)]


def curve(x, y, a, L, bend, n=7):
    pts = [(x, y)]; st = L / n
    for i in range(n):
        a2 = a + bend * (i + .5) / n; x += math.cos(a2) * st; y += math.sin(a2) * st; pts.append((x, y))
    return pts


def fire(img, x, y, s, ang=-math.pi / 2):
    """Kitsune-bi at the tail tip: a faint blue flame with a soft halo."""
    soft(img, lambda d: d.ellipse([px(x - s * 1.6), px(y - s * 1.9), px(x + s * 1.6), px(y + s * 1.3)], fill=(110, 180, 255, 120)), s * .7)
    ca, sa = math.cos(ang), math.sin(ang)
    def fl(k, col):
        r = s * .55 * k; tip = (x + ca * s * 1.9 * k, y + sa * s * 1.9 * k)
        pts = [(x + math.cos(ang + math.pi / 2 + t) * r, y + math.sin(ang + math.pi / 2 + t) * r) for t in np.linspace(0, math.pi, 7)]
        l = Image.new('RGBA', img.size, (0, 0, 0, 0)); poly_s(ImageDraw.Draw(l), pts + [tip], col, 6)
        img.alpha_composite(l.filter(ImageFilter.GaussianBlur(s * .18 * M.S)))
    fl(1, (150, 205, 255, 170)); fl(.62, (214, 238, 255, 225))


def tails(img, g, x, y, a, bend, seed, scale=1.0, fires=True):
    """The bakeneko tail: stubby and forked at the tip for the baby, split from the root in the young bakeneko."""
    p = G[g]; L = p['tl'] * scale; w0 = [7.5, 7.5, 7.5][g]; tips = []
    def one(pts, wa, wb, col, sd, tip=True):
        m = shape(img, col, sd, tube(pts, wa, wb), scale=6, contrast=.6, dk=.3, lt=.12, k=.5, rim=.3)
        ex, ey = pts[-1]
        if tip: clipped(img, m, lambda d, l: d.ellipse([px(ex - 16), px(ey - 16), px(ex + 16), px(ey + 16)], fill=(118, 116, 130, 200)))
        rings = pts[2:-1:2]
        clipped(img, m, lambda d, l: [d.line([(px(qx - 9), px(qy - 3)), (px(qx + 9), px(qy + 3))], fill=STRIPE, width=px(3)) for qx, qy in rings])
        tips.append((ex, ey, math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0])))
    if p['sp'] >= 1:   # two full tails
        one(curve(x, y, a - .42, L * .92, bend * 1.1), w0 * .9, 4.2, FUR_D, seed + 1)
        one(curve(x, y, a, L, bend), w0, 4.5, FUR, seed)
    else:
        base = curve(x, y, a, L * (1 - p['sp']), bend * (1 - p['sp']), 5)
        ax = a + bend * (1 - p['sp']); bx, by = base[-1]; wm = w0 * .8
        one(base, w0, wm, FUR, seed, False)
        one(curve(bx, by, ax - .45, L * p['sp'], bend * p['sp'], 4), wm * .78, 3.6, FUR_D, seed + 1)
        one(curve(bx, by, ax + .3, L * p['sp'], bend * p['sp'], 4), wm * .8, 3.8, FUR, seed + 2)
    if fires:
        for ex, ey, _ in tips[-2:]: fire(img, ex, ey - 2, [5.5, 6.5, 7.5][g])
    return [(round(ex), round(ey - 4)) for ex, ey, _ in tips[-2:]]


def ear(img, bx, by, ang, size, seed, col=FUR):
    ca, sa, pa = math.cos(ang), math.sin(ang), ang + math.pi / 2
    tip = (bx + ca * size, by + sa * size); l = (bx + math.cos(pa) * size * .5, by + math.sin(pa) * size * .5); r = (bx - math.cos(pa) * size * .5, by - math.sin(pa) * size * .5)
    shape(img, col, seed, [l, tip, r, (bx - ca * size * .2, by - sa * size * .2)], scale=5, k=.4, rim=.25)
    d = ImageDraw.Draw(img); k = .62
    poly_s(d, [(bx + (l[0] - bx) * k, by + (l[1] - by) * k + 2), (bx + (tip[0] - bx) * .78, by + (tip[1] - by) * .78), (bx + (r[0] - bx) * k, by + (r[1] - by) * k + 2)], PINK, 4)


def leg(img, x0, y0, x1, y1, w, seed, col=FUR, paw=True):
    mx, my = (x0 + x1) / 2 + 1, (y0 + y1) / 2
    shape(img, col, seed, tube([(x0, y0), (mx, my), (x1, y1 - w * .3)], w, w * .85), scale=5, contrast=.6, dk=.3, lt=.1, k=.5, rim=.3)
    if paw: shape(img, WHT, seed + 50, ell=(x1 - w * 1.15, y1 - w * .9, x1 + w * 1.25, y1 + 1), scale=4, contrast=.4, dk=.15, lt=.05, k=.4, rim=.2)


def head(img, g, hx, hy, seed, eyes='open', look=(0, 0), mew=False, tilt=0):
    p = G[g]; r = p['hr']; e = p['ear'] * r
    ear(img, hx - r * .5, hy - r * .58, -math.pi / 2 - .42 + tilt, e, seed + 1, FUR_D)
    ear(img, hx + r * .5, hy - r * .6, -math.pi / 2 + .36 + tilt, e, seed + 2)
    pts = [(hx, hy - r * .92), (hx + r * .7, hy - r * .74), (hx + r * 1.02, hy - r * .1), (hx + r * 1.12, hy + r * .32), (hx + r * .86, hy + r * .62),
           (hx + r * .3, hy + r * .84), (hx - r * .3, hy + r * .84), (hx - r * .86, hy + r * .6), (hx - r * 1.1, hy + r * .28), (hx - r * 1.0, hy - r * .14), (hx - r * .7, hy - r * .74)]
    mh = shape(img, FUR, seed, pts, scale=7, contrast=.6, dk=.3, lt=.14, k=.5, rim=.38)
    shape(img, WHT, seed + 3, ell=(hx - r * .38, hy + r * .12, hx + r * .62, hy + r * .8), scale=5, contrast=.4, dk=.12, lt=.05, k=.3, rim=.2)
    clipped(img, mh, lambda d, l: [stroke(d, [(hx + r * (o * .22 + .08), hy - r * .95), (hx + r * (o * .2 + .08), hy - r * .7), (hx + r * (o * .12 + .08), hy - r * .45)], STRIPE, 3.2) for o in (-1, 0, 1)])
    clipped(img, mh, lambda d, l: [stroke(d, [(hx + s * r * 1.1, hy + r * (.02 + k * .16)), (hx + s * r * .78, hy + r * (.04 + k * .14))], STRIPE, 2.4) for s in (-1, 1) for k in (0, 1)])
    fur_ticks(img, mh, seed + 4, (hx - r, hy - r, hx + r, hy + r * .8), 50, (120, 105, 95, 70), (3, 6))
    d = ImageDraw.Draw(img); fx = hx + r * .1
    for sx in (-1, 1):
        ex, ey = fx + sx * r * .41, hy + r * .04; rx = r * .22 * (.9 if sx < 0 else 1); ry = r * (.19 if g == 2 else .25)
        if eyes == 'closed':
            d.arc([px(ex - rx), px(ey - ry * .9), px(ex + rx), px(ey + ry * .7)], 20, 160, fill=INK, width=px(2.6)); continue
        if g == 2:   # almond eyes, slightly uncanny
            poly_s(d, [(ex - rx * 1.15, ey + ry * .1), (ex - rx * .2, ey - ry), (ex + rx * 1.1, ey - ry * .4), (ex + rx * .3, ey + ry * .95)], EYE[g], 6)
        else: d.ellipse([px(ex - rx), px(ey - ry), px(ex + rx), px(ey + ry)], fill=EYE[g])
        d.ellipse([px(ex - rx), px(ey - ry), px(ex + rx), px(ey + ry)], outline=(70, 50, 34, 255), width=px(1.6)) if g < 2 else None
        pr = r * (.15 if eyes == 'wide' else .045 if g == 2 else .11); qy = r * (.2 if g == 2 else .17)
        cx_, cy_ = ex + look[0] * rx * .3, ey + look[1] * ry * .35
        d.ellipse([px(cx_ - pr), px(cy_ - qy), px(cx_ + pr), px(cy_ + qy)], fill=(16, 12, 14, 255))
        d.ellipse([px(cx_ - rx * .55), px(cy_ - ry * .62), px(cx_ - rx * .1), px(cy_ - ry * .2)], fill=(255, 255, 255, 235))
        d.ellipse([px(cx_ + rx * .2), px(cy_ + ry * .25), px(cx_ + rx * .42), px(cy_ + ry * .45)], fill=(255, 255, 255, 170))
    ny = hy + r * .36
    poly_s(d, [(fx - r * .09, ny - r * .05), (fx + r * .09, ny - r * .05), (fx, ny + r * .06)], PINK, 3)
    if mew: d.ellipse([px(fx - r * .1), px(ny + r * .1), px(fx + r * .1), px(ny + r * .28)], fill=(120, 52, 60, 255))
    d.arc([px(fx - r * .16), px(ny), px(fx), px(ny + r * .14)], 10, 170, fill=INK, width=px(1.6)); d.arc([px(fx), px(ny), px(fx + r * .16), px(ny + r * .14)], 10, 170, fill=INK, width=px(1.6))
    for sx in (-1, 1):
        for k in range(3): d.line([(px(fx + sx * r * .28), px(ny + r * .08 + k * 3)), (px(fx + sx * r * 1.05), px(ny - r * .05 + k * r * .14))], fill=(235, 230, 220, 150), width=px(.9))
    soft(img, lambda dd: [dd.ellipse([px(fx + s * r * .62 - r * .17), px(ny - r * .1), px(fx + s * r * .62 + r * .17), px(ny + r * .08)], fill=(235, 130, 130, 70)) for s in (-1, 1)], 3)


def body_shape(img, pts, seed):
    m = shape(img, FUR, seed, pts, scale=8, contrast=.6, dk=.3, lt=.12, k=.55, rim=.4)
    x0, y0, x1, y1 = [v / M.S for v in m.getbbox()]
    clipped(img, m, lambda d, l: [stroke(d, [(x0 + (x1 - x0) * f, y0 - 2), (x0 + (x1 - x0) * (f - .03), (y0 + y1) / 2), (x0 + (x1 - x0) * (f + .02), y0 + (y1 - y0) * .7)], STRIPE, 3.6) for f in (.3, .48, .66)], .8)
    fur_ticks(img, m, seed + 5, (x0, y0, x1, y1), 70, (120, 105, 95, 70), (4, 8))
    return m


def sit(g, look=False):
    p = G[g]; bl, bh, lg, hr = p['bl'], p['bh'], p['lg'], p['hr']; img = canvas(FW, FH); sd = 300 + g * 40 + look * 20
    tips = tails(img, g, CX - bl * .7, FY - 6, math.pi * .97, 1.85 if g < 2 else 1.7, sd)
    shape(img, FUR_D, sd + 1, ell=(CX - bl * 1.05, FY - bh * 1.9, CX + bl * .35, FY), scale=8, k=.5, rim=.35)
    body_shape(img, [(CX - bl * .85, FY - bh * .7), (CX - bl * .65, FY - bh * 1.6 - lg * .5), (CX - bl * .15, FY - bh * 2.2 - lg * .85), (CX + bl * .42, FY - bh * 2.05 - lg * .85),
                     (CX + bl * .62, FY - bh * 1.2 - lg * .5), (CX + bl * .45, FY - 4), (CX - bl * .25, FY - 1)], sd + 2)
    shape(img, WHT, sd + 3, ell=(CX + bl * .02, FY - bh * 2.0 - lg * .8, CX + bl * .6, FY - bh * .5), scale=5, contrast=.4, dk=.12, lt=.05, k=.3, rim=.2)
    shape(img, WHT, sd + 4, ell=(CX - bl * .25, FY - 9, CX + bl * .2, FY + 1), scale=4, k=.3, rim=.2)   # hind paw
    leg(img, CX + bl * .16, FY - bh * 1.3 - lg * .4, CX + bl * .14, FY - 2, p['pw'] * .92, sd + 5, FUR_D)
    if look: leg(img, CX + bl * .5, FY - bh * 1.4 - lg * .5, CX + bl * 1.0, FY - bh * 2.0 - lg * .6, p['pw'], sd + 6)
    else: leg(img, CX + bl * .46, FY - bh * 1.3 - lg * .4, CX + bl * .5, FY - 1, p['pw'], sd + 6)
    hy = FY - bh * 2.15 - lg * .9 - hr * (.75 if look else .55)
    head(img, g, CX + bl * (.36 if look else .3), hy, sd + 7, 'open', (.4, -1) if look else (.5, .1), mew=look, tilt=.12 if look else 0)
    return img, tips


def walk(g):
    p = G[g]; bl, bh, lg, hr = p['bl'], p['bh'], p['lg'], p['hr']; img = canvas(FW, FH); sd = 400 + g * 40; by = FY - lg - bh * .95
    tips = tails(img, g, CX - bl * .95, by - bh * .4, -math.pi * .62, .95, sd)
    leg(img, CX + bl * .5, by, CX + bl * .66, FY - 3, p['pw'] * .9, sd + 1, FUR_D); leg(img, CX - bl * .55, by, CX - bl * .72, FY - 3, p['pw'] * .9, sd + 2, FUR_D)
    body_shape(img, [(CX - bl * 1.1, by - bh * .2), (CX - bl * .7, by - bh * .95), (CX + bl * .2, by - bh * 1.0), (CX + bl * .85, by - bh * .9), (CX + bl * 1.05, by - bh * .1),
                     (CX + bl * .7, by + bh * .75), (CX - bl * .1, by + bh * .7), (CX - bl * .85, by + bh * .75)], sd + 3)
    shape(img, WHT, sd + 4, ell=(CX + bl * .35, by - bh * .3, CX + bl * 1.0, by + bh * .75), scale=5, contrast=.4, dk=.12, lt=.05, k=.3, rim=.2)
    leg(img, CX + bl * .55, by + 2, CX + bl * .32, FY - 2, p['pw'], sd + 5); leg(img, CX - bl * .7, by + 2, CX - bl * .45, FY - 2, p['pw'], sd + 6)
    head(img, g, CX + bl * .98, by - bh * .7 - hr * .45, sd + 7, 'open', (.8, 0))
    return img, tips


def sleep(g):
    p = G[g]; bl, bh, lg, hr = p['bl'], p['bh'], p['lg'], p['hr']; img = canvas(FW, FH); sd = 500 + g * 40
    rx, ry = bl * 1.2 + 6, bh * 1.05 + lg * .18; cy = FY - ry
    body_shape(img, [(CX - rx, cy + ry * .3), (CX - rx * .8, cy - ry * .75), (CX - rx * .1, cy - ry * 1.02), (CX + rx * .6, cy - ry * .8), (CX + rx, cy - ry * .05),
                     (CX + rx * .8, cy + ry * .9), (CX, cy + ry), (CX - rx * .8, cy + ry * .95)], sd)
    tips = tails(img, g, CX - rx * .95, FY - 13, .22, -.95, sd + 1, .8)
    shape(img, WHT, sd + 2, ell=(CX + rx * .25, FY - 14, CX + rx * .85, FY), scale=4, k=.3, rim=.2)
    hx, hy = CX + rx * .5, cy + ry * .05
    head(img, g, hx, hy, sd + 3, 'closed', tilt=.25)
    return img, tips


def pounce(g):
    p = G[g]; bl, bh, lg, hr = p['bl'], p['bh'], p['lg'], p['hr']; img = canvas(FW, FH); sd = 600 + g * 40; by = FY - lg * .7 - bh
    tips = tails(img, g, CX - bl * .95, by - bh * .8, -math.pi * .7, -.7, sd)
    shape(img, FUR_D, sd + 1, ell=(CX - bl * 1.15, by - bh * 1.1, CX - bl * .15, FY - 2), scale=7, k=.5, rim=.35)
    leg(img, CX + bl * .55, by + bh * .2, CX + bl * 1.05, FY - 2, p['pw'] * .9, sd + 2, FUR_D)
    body_shape(img, [(CX - bl * 1.05, by - bh * .7), (CX - bl * .6, by - bh * 1.15), (CX + bl * .2, by - bh * .7), (CX + bl * .85, by - bh * .2), (CX + bl * .95, by + bh * .5),
                     (CX + bl * .3, by + bh * .85), (CX - bl * .5, by + bh * .7), (CX - bl * .95, by + bh * .3)], sd + 3)
    shape(img, WHT, sd + 4, ell=(CX - bl * .55, FY - 9, CX - bl * .05, FY + 1), scale=4, k=.3, rim=.2)
    leg(img, CX + bl * .45, by + bh * .3, CX + bl * .85, FY - 1, p['pw'], sd + 5)
    head(img, g, CX + bl * 1.1, FY - hr * .95 - lg * .25 - 4, sd + 6, 'wide', (.9, .2))
    return img, tips


def box():
    g = 0; p = G[0]; r = p['hr']; img = canvas(FW, FH); d = ImageDraw.Draw(img)
    x0, x1, top = CX - 82, CX + 82, FY - 92
    poly_s(d, [(x0 + 8, top + 2), (x1 - 8, top + 2), (x1 - 14, top + 30), (x0 + 14, top + 30)], (30, 22, 16, 255), 2)   # inside, dark
    for sx in (-1, 1):   # open flaps, sagging with rain
        xa = CX + sx * 82
        shape(img, hexc('#6f5338'), 700 + sx, [(xa, top), (xa + sx * 34, top - 34), (xa + sx * 4, top - 50), (xa - sx * 30, top - 10)], scale=6, k=.4, rim=.2, smooth=False)
    tips = tails(img, g, CX + 26, top + 14, -math.pi * .3, -.2, 710)
    head(img, g, CX - 2, top - r * .35, 720, 'open', (.2, -.6))
    mb = shape(img, hexc('#8b6b47'), 730, [(x0, top), (x1, top), (x1 + 4, FY), (x0 - 4, FY)], scale=9, contrast=.9, dk=.35, lt=.12, k=.5, rim=.25, smooth=False)
    rnd = random.Random(731)
    def wet(dd, l):
        for _ in range(9):
            wx, wy = rnd.uniform(x0, x1), rnd.uniform(FY - 40, FY + 10); dd.ellipse([px(wx - 30), px(wy - 14), px(wx + 30), px(wy + 14)], fill=(56, 38, 24, 120))
        dd.line([(px(x0 + 6), px(top + 8)), (px(x1 - 6), px(top + 8))], fill=(70, 50, 32, 200), width=px(3))
        dd.line([(px(CX - 30), px(top + 40)), (px(CX + 30), px(top + 40))], fill=(60, 44, 30, 160), width=px(6))   # packing tape scrap
    clipped(img, mb, wet)
    for sx in (-1, 1): shape(img, WHT, 740 + sx, ell=(CX + sx * 22 - 10, top - 8, CX + sx * 22 + 10, top + 6), scale=4, k=.3, rim=.2)
    d = ImageDraw.Draw(img)
    for _ in range(14):
        wx, wy = rnd.uniform(x0 - 10, x1 + 10), rnd.uniform(top - 60, FY); d.line([(px(wx), px(wy)), (px(wx - 2), px(wy + 9))], fill=(190, 210, 225, 120), width=px(1.2))
    return img, tips


def finish(img):
    out = img.resize((P.W, P.H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(.5))
    a = np.asarray(out, np.float32); a[..., :3] = np.clip(a[..., :3] + np.random.default_rng(7).normal(0, 4, a.shape[:2])[..., None], 0, 255)
    return Image.fromarray(a.astype(np.uint8), 'RGBA')


# ── the kitten's things ──
def bowl():
    img = canvas(130, 84); d = ImageDraw.Draw(img)
    shape(img, hexc('#2f4d78'), 800, ell=(10, 20, 120, 82), scale=6, contrast=.7, k=.5, rim=.3, spec=.25)
    shape(img, hexc('#e9e2d2'), 801, ell=(16, 16, 114, 44), scale=5, contrast=.4, k=.3, rim=.15)
    d = ImageDraw.Draw(img); d.ellipse([px(16), px(16), px(114), px(44)], outline=(34, 52, 86, 255), width=px(3))
    for k in range(3): d.arc([px(30 + k * 26), px(52), px(52 + k * 26), px(70)], 200, 340, fill=(230, 228, 216, 230), width=px(2.4))   # waves
    poly_s(d, [(48, 30), (64, 25), (76, 30), (64, 35)], (232, 140, 90, 220), 4); poly_s(d, [(76, 30), (84, 25), (84, 35)], (232, 140, 90, 220), 3)
    return finish(img)


def basket():
    img = canvas(230, 140)
    mb = shape(img, hexc('#9a7a4a'), 810, [(8, 52), (222, 52), (210, 128), (20, 128)], scale=6, contrast=.8, k=.5, rim=.3)
    clipped(img, mb, lambda d, l: [d.line([(px(x), px(50)), (px(x + 6), px(130))], fill=(90, 66, 36, 200), width=px(3)) for x in range(10, 224, 12)] +
            [d.arc([px(0), px(y), px(230), px(y + 30)], 0, 180, fill=(196, 164, 110, 160), width=px(2.5)) for y in range(40, 120, 10)])
    shape(img, hexc('#b0453e'), 811, ell=(26, 22, 204, 70), scale=6, contrast=.7, k=.5, rim=.3)
    m = shape(img, hexc('#c45a4c'), 812, ell=(40, 26, 190, 60), scale=6, contrast=.6, k=.5, rim=.25)
    clipped(img, m, lambda d, l: [d.ellipse([px(x - 4), px(y - 4), px(x + 4), px(y + 4)], fill=(240, 230, 214, 210)) for x, y in [(60, 38), (90, 48), (122, 36), (152, 46), (176, 38), (106, 30)]])
    shape(img, hexc('#b48d58'), 813, ell=(4, 44, 226, 66), scale=5, k=.4, rim=.2)
    return finish(img)


def ball():
    img = canvas(92, 100)
    m = shape(img, hexc('#c9a86a'), 820, ell=(6, 14, 86, 94), scale=5, contrast=.8, k=.6, rim=.4, spec=.2)
    clipped(img, m, lambda d, l: [d.arc([px(6 + k * 8), px(14), px(86 - k * 8), px(94)], 0, 360, fill=(120, 84, 40, 200), width=px(2.4)) for k in range(5)] +
            [d.line([(px(6), px(54)), (px(86), px(54))], fill=(120, 84, 40, 200), width=px(2.4))])
    d = ImageDraw.Draw(img); d.line([(px(46), px(16)), (px(46), px(4))], fill=(180, 40, 40, 255), width=px(3))
    shape(img, hexc('#d6b04a'), 821, ell=(36, 0, 56, 18), scale=3, k=.6, rim=.3, spec=.5)
    return finish(img)


if __name__ == '__main__':
    random.seed(1)
    frames, J = [], {}
    for g in range(3):
        for k, fn in (('sit', lambda: sit(g)), ('walk', lambda: walk(g)), ('sleep', lambda: sleep(g)), ('pounce', lambda: pounce(g)), ('look', lambda: sit(g, True))):
            im, tips = fn(); frames.append((f'{k}{g}', finish(im), tips))
    im, tips = box(); frames.append(('box', finish(im), tips))
    cols = 4; A = Image.new('RGBA', (cols * FW, math.ceil(len(frames) / cols) * FH), (0, 0, 0, 0))
    for i, (k, f, tips) in enumerate(frames):
        x, y = (i % cols) * FW, (i // cols) * FH; A.alpha_composite(f, (x, y)); J[k] = [x, y, [list(t) for t in tips]]
    A.save(f'{ASSETS}/mon/m_pt_atlas.webp', 'WEBP', quality=86, alpha_quality=90, method=6)
    items, IJ, x = [bowl(), basket(), ball()], {}, 0
    B = Image.new('RGBA', (sum(i.width for i in items) + 2 * len(items), max(i.height for i in items)), (0, 0, 0, 0))
    for k, i in zip(('pt_bowl', 'pt_basket', 'pt_ball'), items): B.alpha_composite(i, (x, 0)); IJ[k] = [x, 0, i.width, i.height]; x += i.width + 2
    B.save(f'{ASSETS}/items/atlas_pt.webp', 'WEBP', quality=88, alpha_quality=92, method=6)
    OUTP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out'); os.makedirs(OUTP, exist_ok=True)
    pv = Image.new('RGBA', A.size, (52, 58, 54, 255)); pv.alpha_composite(A); pv.convert('RGB').save(OUTP + '/pet2_atlas.jpg', quality=85)
    pv = Image.new('RGBA', B.size, (52, 58, 54, 255)); pv.alpha_composite(B); pv.convert('RGB').save(OUTP + '/pet2_items.jpg', quality=85)
    print(json.dumps({'atlas': list(A.size), 'f': J, 'items': list(B.size), 'it': IJ}, separators=(',', ':')))
