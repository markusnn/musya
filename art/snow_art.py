#!/usr/bin/env python3
"""Add-on art «Зимние забавы» (feat/snow.js): a kamakura (rough pile → packed dome → hut with a dark entrance + its
candle-lit inside as a separate overlay), a snowball, a puddle, the snowman's dressing (bucket, knit cap, scarf, twig and
pine arms, charcoal / pebble / nandina-berry eyes, mikan / leaf / twig mouths), a clay brazier with a toasting mochi and
the three reward things (bucket hat, knit scarf, candle lantern) — all in ONE atlas.
Usage: cd art && python3 snow_art.py ../assets/items  →  atlas_yk.webp; the rect map is printed as JSON (pasted into
feat/snow.js as YK_R). Preview → art/out/yk_atlas.png"""
import json, math, os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from birds_art import Cv, blur, light, C, pack
from paint import fbm

OUT = sys.argv[1] if len(sys.argv) > 1 else '../assets/items'
SS = 2
L = np.array([-.5, -.68, .54]); L /= np.linalg.norm(L)
SNOW_HI, SNOW_LO = C('#eef3f7'), C('#5d6d8a')


class Cell:
    def __init__(s, w, h, seed=1):
        s.w, s.h, s.seed = w, h, seed; s.cv = Cv(w * SS, h * SS)
        s.X, s.Y = s.cv.xx / SS, s.cv.yy / SS          # final-px coordinates of every supersampled pixel

    def E(s, cx, cy, rx, ry, ang=0, soft=1.2): return s.cv.ell(cx * SS, cy * SS, rx * SS, ry * SS, ang * math.pi / 180, soft)
    def P(s, pts): return s.cv.poly([(x * SS, y * SS) for x, y in pts])
    def Ln(s, pts, wd): return s.cv.line([(x * SS, y * SS) for x, y in pts], wd * SS)
    def put(s, m, col, a=1.): s.cv.put(np.clip(m, 0, 1) * a, C(col) if isinstance(col, str) else col)
    def N(s, sc, seed=0, oct=4): return fbm(s.cv.w, s.cv.h, sc * SS, oct, s.seed * 13 + seed)

    def shade(s, m, col, sig=5, spec=.1, k=1.6, amb=.45, dif=.75, tex=0., a=1.):
        sh, sp = light(m, sig * SS, k=k, amb=amb, dif=dif, spec=spec)
        c = C(col)[None, None, :] * sh[..., None]
        if tex: n = s.N(3, 5); c = c * (1 - tex / 2 + tex * n[..., None])
        s.put(m * a, np.clip(c + 255 * sp[..., None], 0, 255))

    def done(s):
        rgba = np.dstack([np.clip(s.cv.rgb, 0, 255), np.clip(s.cv.a * 255, 0, 255)]).astype(np.uint8)
        return Image.fromarray(rgba, 'RGBA').resize((s.w, s.h), Image.LANCZOS)


def snow_col(lam, bump=None):
    """moonlit snow: cool shadows, near-white light"""
    t = np.clip(lam, 0, 1)[..., None]
    return SNOW_LO + (SNOW_HI - SNOW_LO) * t


def sparkle(c, m, lam, n=60, seed=1):
    rng = np.random.default_rng(seed); h, w = m.shape
    for _ in range(n):
        x, y = rng.integers(0, w), rng.integers(0, h)
        if m[y, x] > .9 and lam[y, x] > .62:
            r = rng.integers(1, 3) * SS // 2 + 1
            c.cv.rgb[max(0, y - r):y + r, max(0, x - r):x + r] = 255


def ball(r=100, seed=1):
    """a rolled snowball: analytic sphere + lumpy bumps + a few rolled-in streaks"""
    w = h = 2 * r + 8; c = Cell(w, h, seed); cx = cy = w / 2
    u, v = (c.X - cx) / r, (c.Y - cy) / r; d2 = u * u + v * v
    nz = np.sqrt(np.clip(1 - d2, 0, 1))
    n1 = c.N(r * .22, 1); n2 = c.N(r * .07, 2)
    gy, gx = np.gradient(n1 * 3 + n2 * .45)
    nx, ny = u + gx * 1.0 * r * SS / 60, v + gy * 1.0 * r * SS / 60
    nn = np.sqrt(nx * nx + ny * ny + nz * nz) + 1e-6
    lam = np.clip((nx * L[0] + ny * L[1] + nz * L[2]) / nn, 0, 1)
    lam = .2 + .85 * lam + .18 * np.clip(u * .6 + v * .8, 0, 1) ** 2 * (1 - nz)     # bounce light from the snow below
    lam = lam * (.93 + .1 * n2)
    m = np.clip((1 - np.sqrt(d2)) * r * SS / 1.4 + .5, 0, 1)
    # silhouette not a perfect circle: lumps on the rim
    m = m * np.clip((1 - np.sqrt(d2) + (n1 - .5) * .07) * r * SS / 1.4 + .5, 0, 1)
    col = snow_col(lam)
    # rolled streaks: thin darker arcs (dirt and leaves picked up while rolling)
    st = np.sin((u * .8 + v * .6) * 22 + n1 * 9) * np.sin((u - v) * 7 + n2 * 5)
    col = col * (1 - .07 * np.clip(st - .55, 0, 1)[..., None] * 3)
    c.put(m, col); sparkle(c, m, lam, 90, seed)
    return c.done()


def dome(kind, seed=3):
    """kind: 'mound' (rough pile), 'dome' (packed), 'km' (hut with a dark entrance), 'glow' (lit inside only)"""
    W, H = 480, 330; c = Cell(W, H, seed); cx, by, rx, ry = 240, 300, 210, 250
    n1 = c.N(40, 1); n2 = c.N(12, 2); n3 = c.N(5, 3)
    if kind == 'mound':
        m = np.zeros_like(c.X)
        for (x, y, a, b) in [(240, 300, 205, 180), (150, 300, 110, 120), (330, 300, 120, 135), (210, 230, 90, 70), (290, 215, 80, 60),
                             (240, 175, 60, 45), (110, 300, 80, 60), (380, 300, 80, 70)]:
            m = np.maximum(m, c.E(x, y, a, b, 0, 3))
        m = m * (c.Y < 300 + 10 * n1 * SS / SS) + c.E(240, 300, 225, 24, 0, 4) * .95
        m = np.clip(m + (n1 - .5) * .5 * (m > .05) * (m < .95), 0, 1)
        hgt = m * (.7 + .6 * n2)
        sh, sp = light(hgt, 6 * SS, k=3.2, amb=.25, dif=.9, spec=0)
        lam = (sh - .25) / .9 * (.88 + .2 * n3)
        c.put(m, snow_col(lam)); sparkle(c, m, lam, 70, seed); return c.done()
    u = (c.X - cx) / rx; v = (by - c.Y) / ry; d2 = u * u + v * v
    nz = np.sqrt(np.clip(1 - d2, 0, 1))
    pats = (n2 - .5) * (1.1 if kind == 'dome' else .9) + (n3 - .5) * .35
    gy, gx = np.gradient(pats)
    nx, ny = u + gx * 8, -v + gy * 8
    nn = np.sqrt(nx * nx + ny * ny + nz * nz) + 1e-6
    lam = np.clip((nx * L[0] + ny * L[1] + nz * L[2]) / nn, 0, 1)
    lam = .22 + .82 * lam
    edge = np.clip((1 - np.sqrt(d2) + (n1 - .5) * .025) * min(rx, ry) * SS / 1.5 + .5, 0, 1) * (c.Y <= by + 1)
    base = c.E(cx, by, rx + 22, 26, 0, 6)          # snow banked around the foot
    m = np.maximum(edge, base * .98)
    bl = np.clip((c.Y - (by - 30)) / 40, 0, 1)
    lam = lam * (1 - bl * .12) + bl * .12 * (.6 + .4 * n2)
    col = snow_col(lam * (.94 + .1 * n3))
    if kind == 'glow':
        col = col * 0
    c.put(m if kind != 'glow' else m * 0, col)
    if kind in ('km', 'glow'):
        # the entrance: an arch (half ellipse over a short rectangle)
        ex, ew, eh, ey = cx + 6, 66, 150, by - 4
        arch = np.maximum(c.E(ex, ey - eh + 66, ew, 66, 0, 1.4), c.P([(ex - ew, ey - eh + 66), (ex + ew, ey - eh + 66), (ex + ew, ey), (ex - ew, ey)]))
        inner = np.maximum(c.E(ex - 12, ey - eh + 74, ew - 6, 62, 0, 1.4), c.P([(ex - ew - 6, ey - eh + 74), (ex + ew - 18, ey - eh + 74), (ex + ew - 18, ey - 8), (ex - ew - 6, ey - 8)])) * arch
        wall = np.clip(arch - inner, 0, 1)          # the thickness of the wall seen on the right side of the arch
        if kind == 'km':
            c.put(arch, C('#2a2026')); c.put(inner, C('#120d10'))
            c.put(wall * (.6 + .4 * n3), snow_col(.45 + .1 * n2))
        else:
            # candle light: bright warm floor centre, dimmer walls and ceiling
            dx, dy = (c.X - ex) / 70, (c.Y - (ey - 18)) / 120
            g = np.clip(1 - np.sqrt(dx * dx + dy * dy), 0, 1)
            warm = C('#4a1e10') + (C('#ffc46a') - C('#4a1e10')) * (g ** 1.3)[..., None]
            warm = warm * (.88 + .2 * n3[..., None])
            c.put(inner, warm)
            c.put(wall, C('#f3b36a') * (.62 + .3 * n2)[..., None] + C('#ffd9a0') * 0)
            # spill of warm light on the banked snow in front of the entrance
            sp = c.E(ex, ey + 10, 120, 22, 0, 10) * (1 - arch) * .3
            c.put(sp, C('#ffcf8a'))
            # a tiny candle at the back
            c.put(c.P([(ex - 12, ey - 44), (ex - 4, ey - 44), (ex - 4, ey - 22), (ex - 12, ey - 22)]), C('#e9dcc4')); c.put(c.E(ex - 8, ey - 52, 3.5, 7, 0, 1.4), C('#fff6c8'))
    else:
        sparkle(c, m, lam, 90, seed)
    return c.done()


def puddle(seed=4):
    W, H = 300, 90; c = Cell(W, H, seed); n = c.N(14, 1)
    b0 = c.E(150, 46, 140, 36, 0, 10); m = np.clip(b0 * 1.5 - .25 + (n - .5) * .7 * b0, 0, 1); m = blur(m, 2 * SS) * .95
    t = np.clip((c.Y - 14) / 70, 0, 1)
    col = C('#1d2a3c')[None, None, :] * (1 - t[..., None]) + C('#3c4d66')[None, None, :] * t[..., None]
    c.put(m, col)
    c.put(c.E(118, 38, 46, 5, -4, 3) * m, C('#9fb0c8'), .55)       # moon glint
    c.put(c.E(196, 56, 30, 3, 3, 2) * m, C('#7d90ab'), .5)
    rim = np.clip(m - blur(m, 3 * SS) * 1.05, 0, 1) * 2
    c.put(rim, C('#dfe7ef'), .5)                                   # thin icy rim
    return c.done()


def bucket(seed=5):
    """a zinc bucket (baketsu), upright; the game flips it for the snowman's hat"""
    W, H = 150, 140; c = Cell(W, H, seed); n = c.N(6, 1)
    body = c.P([(22, 34), (128, 34), (112, 132), (38, 132)])
    u = (c.X - 75) / 55
    lam = np.clip(.55 + .45 * np.cos((u + .35) * 1.9), 0, 1) * (.9 + .15 * n)
    col = C('#4f5b66')[None, None, :] + (C('#c9d2d8') - C('#4f5b66'))[None, None, :] * lam[..., None]
    c.put(body, col)
    for y in (58, 96):                                          # pressed ribs
        c.put(c.P([(22 + (y - 34) * .16, y), (128 - (y - 34) * .16, y), (128 - (y - 30) * .16, y + 4), (22 + (y - 30) * .16, y + 4)]) * body, C('#2e363e'), .5)
        c.put(c.P([(22 + (y - 38) * .16, y - 3), (128 - (y - 38) * .16, y - 3), (128 - (y - 36) * .16, y - 1), (22 + (y - 36) * .16, y - 1)]) * body, C('#e8eef2'), .45)
    c.put(c.E(75, 34, 54, 9, 0, 1), C('#2b3138')); c.put(c.E(75, 34, 54, 9, 0, 1) - c.E(75, 35, 50, 7, 0, 1), C('#d8e0e6'))
    c.put(c.E(75, 132, 37, 4, 0, 1), C('#39424b'))
    c.put(c.Ln([(22, 40), (26, 14), (75, 4), (124, 14), (128, 40)], 3), C('#8a949c'))   # handle
    c.put(c.E(60, 70, 7, 28, 0, 2) * body, C('#ffffff'), .25)
    return c.done()


def cap(seed=6):
    """a red knitted cap with a cuff and a pompom"""
    W, H = 150, 128; c = Cell(W, H, seed); n = c.N(4, 1)
    dome_ = np.maximum(c.E(75, 98, 62, 72, 0, 1.5) * (c.Y < 98), c.P([(13, 96), (137, 96), (137, 100), (13, 100)]))
    rib = .82 + .18 * np.abs(np.sin((c.X - 75) * .32 + (c.Y - 98) * .04))
    sh, _ = light(dome_, 9 * SS, k=1.4, amb=.45, dif=.7, spec=0)
    c.put(dome_, C('#a32a24') * (sh * rib * (.9 + .15 * n))[..., None])
    cuff = c.P([(10, 92), (140, 92), (142, 118), (8, 118)]) * c.E(75, 105, 70, 40, 0, 2)
    sh2, _ = light(cuff, 5 * SS, k=1.2, amb=.5, dif=.6, spec=0)
    c.put(cuff, C('#e6dccb') * (sh2 * (.85 + .2 * np.abs(np.sin(c.X * .5))))[..., None])
    pom = np.clip(c.E(75, 24, 20, 19, 0, 3) + (c.N(3, 2) - .5) * .5, 0, 1)
    sh3, _ = light(pom, 5 * SS, k=1.4, amb=.45, dif=.7, spec=0)
    c.put(pom, C('#e6dccb') * (sh3 * (.85 + .25 * c.N(2, 3)))[..., None])
    return c.done()


def scarf(seed=7):
    """a red knitted scarf as worn: a band around the neck and two tails hanging on the right"""
    W, H = 240, 150; c = Cell(W, H, seed); n = c.N(4, 1)
    band = np.clip(c.E(120, 38, 112, 26, 0, 2) - c.E(120, 26, 104, 14, 0, 2) * (c.Y < 30), 0, 1)
    tail1 = c.P([(150, 44), (184, 46), (190, 128), (160, 132)]); tail2 = c.P([(170, 48), (200, 44), (222, 116), (196, 124)])
    for m, k in ((tail2, .78), (band, 1.), (tail1, .92)):
        sh, _ = light(m, 6 * SS, k=1.4, amb=.5, dif=.6, spec=0)
        stripe = np.where(np.sin((c.Y if m is band else c.Y) * .28) > .7, .75, 1.)
        c.put(m, C('#b0302a') * (sh * k * stripe * (.88 + .18 * n))[..., None])
    for x0, y0 in ((160, 132), (196, 124)):
        for i in range(6):
            c.put(c.Ln([(x0 + i * 5, y0 - 2 + i * -1.2), (x0 + i * 5 + 1, y0 + 12 + i * -1.2)], 2.2), C('#8c2420'))
    return c.done()


def scarf_item(seed=8):
    """the reward: a folded knitted scarf with fringe"""
    W, H = 190, 96; c = Cell(W, H, seed); n = c.N(4, 1)
    for i, (y, k) in enumerate(((60, .78), (44, .9), (28, 1.))):
        m = c.P([(18 + i * 4, y), (172 - i * 4, y), (176 - i * 4, y + 26), (14 + i * 4, y + 26)])
        sh, _ = light(m, 5 * SS, k=1.3, amb=.5, dif=.6, spec=0)
        stripe = np.where(np.sin(c.X * .2) > .82, .78, 1.)
        c.put(m, C('#b0302a') * (sh * k * stripe * (.88 + .18 * n))[..., None])
    for i in range(9):
        c.put(c.Ln([(22 + i * 6, 86), (21 + i * 6, 94)], 2), C('#8c2420'))
    return c.done()


def lantern(seed=9):
    """the reward: a small candle lantern for the kamakura (wooden frame, paper, warm light)"""
    W, H = 120, 176; c = Cell(W, H, seed); n = c.N(5, 1)
    glow = blur(c.E(60, 92, 50, 56, 0, 4), 10 * SS)
    c.put(glow, C('#ffb860'), .35)
    paper = c.P([(26, 52), (94, 52), (94, 140), (26, 140)])
    g = np.clip(1 - np.sqrt(((c.X - 60) / 44) ** 2 + ((c.Y - 110) / 70) ** 2), 0, 1)
    c.put(paper, C('#c7802e') + (C('#ffe7a8') - C('#c7802e')) * (g ** .8 * (.9 + .15 * n))[..., None])
    for x in (26, 94): c.put(c.P([(x - 4, 44), (x + 4, 44), (x + 4, 156), (x - 4, 156)]), C('#3a2416'))
    for y in (52, 96, 140): c.put(c.P([(22, y - 2), (98, y - 2), (98, y + 2), (22, y + 2)]), C('#3a2416'))
    c.put(c.P([(14, 36), (106, 36), (98, 46), (22, 46)]), C('#2c1b10'))
    c.put(c.P([(18, 156), (102, 156), (106, 168), (14, 168)]), C('#2c1b10'))
    c.put(c.Ln([(42, 36), (60, 16), (78, 36)], 4), C('#2c1b10')); c.put(c.E(60, 14, 6, 6, 0, 1), C('#2c1b10'))
    c.put(c.E(60, 118, 6, 14, 0, 1), C('#fff4dc'), .8); c.put(c.E(60, 98, 5, 9, 0, 1.5), C('#fffbe0'))
    return c.done()


def brazier(seed=10):
    """a small clay shichirin with a wire grill and a mochi puffing up on it"""
    W, H = 150, 128; c = Cell(W, H, seed); n = c.N(5, 1)
    body = c.P([(28, 62), (122, 62), (114, 122), (36, 122)])
    u = (c.X - 75) / 50; lam = np.clip(.5 + .5 * np.cos((u + .3) * 1.7), 0, 1) * (.85 + .25 * n)
    c.put(body, C('#5a3a26') + (C('#c79a6c') - C('#5a3a26')) * lam[..., None])
    c.put(c.P([(30, 84), (120, 84), (119, 92), (31, 92)]) * body, C('#2a1a12'), .7)          # band
    c.put(c.P([(62, 100), (88, 100), (88, 116), (62, 116)]), C('#1a0e08'))                   # vent
    c.put(c.E(75, 108, 9, 5, 0, 1), C('#ff7a2a'), .8)
    c.put(c.E(75, 62, 48, 9, 0, 1), C('#1c120c')); c.put(c.E(75, 62, 42, 6, 0, 1.5), C('#ff6a20'), .75)
    for i in range(7): c.put(c.Ln([(32 + i * 14, 58), (30 + i * 14, 64)], 1.4), C('#8a8a8a'))
    c.put(c.Ln([(27, 59), (123, 59)], 1.6), C('#9a9a9a'))
    mochi = np.maximum(c.E(72, 50, 26, 11, 0, 1.2), c.E(80, 38, 13, 12, 0, 1.2))            # the puff
    sh, _ = light(mochi, 4 * SS, k=1.6, amb=.55, dif=.55, spec=0)
    col = C('#f4ecdc') * sh[..., None]
    burn = c.N(3, 4) > .66
    col = np.where(burn[..., None] & (c.Y > 46)[..., None], C('#a8723a'), col)
    c.put(mochi, col)
    return c.done()


def twig(pine=False, seed=11):
    W, H = 200, 84; c = Cell(W, H, seed)
    main = [(6, 60), (60, 52), (110, 42), (160, 28), (194, 16)]
    c.put(c.Ln(main, 9), C('#5a3e28')); c.put(c.Ln(main[:3], 12), C('#5a3e28'))
    for a, b in (((96, 44), (130, 66)), ((120, 38), (150, 50)), ((140, 32), (156, 8)), ((70, 50), (92, 30))):
        c.put(c.Ln([a, b], 5.5), C('#5a3e28'))
    c.put(c.Ln([(8, 55), (108, 37)], 2.4), C('#8a6a4a'), .7)
    if pine:
        rng = np.random.default_rng(seed)
        for (x, y) in ((150, 30), (176, 20), (130, 62), (152, 48), (154, 10), (92, 32), (118, 40)):
            for k in range(14):
                a = rng.uniform(-math.pi, math.pi); r = rng.uniform(10, 18)
                c.put(c.Ln([(x, y), (x + math.cos(a) * r, y + math.sin(a) * r * .8)], 1.6), C('#2f4a2c') if k % 3 else C('#4a6a3e'))
    return c.done()


def small(kind, seed=12):
    if kind == 'coal':
        c = Cell(40, 34, seed); m = np.clip(c.E(20, 17, 15, 12, 20, 1.2) + (c.N(4, 1) - .5) * .5, 0, 1)
        sh, sp = light(m, 3 * SS, k=1.8, amb=.4, dif=.6, spec=.5)
        c.put(m, np.clip(C('#1a1a1c') * sh[..., None] + 255 * sp[..., None], 0, 255))
    elif kind == 'pebble':
        c = Cell(40, 34, seed); m = c.E(20, 17, 14, 11, -10, 1.2)
        sh, sp = light(m, 4 * SS, k=1.6, amb=.45, dif=.6, spec=.3)
        c.put(m, np.clip(C('#6c6a66') * (sh * (.85 + .25 * c.N(3, 2)))[..., None] + 255 * sp[..., None], 0, 255))
    elif kind == 'berry':
        c = Cell(40, 34, seed); m = c.E(20, 18, 12, 12, 0, 1.2)
        sh, sp = light(m, 3 * SS, k=1.8, amb=.4, dif=.65, spec=.8)
        c.put(m, np.clip(C('#c8201c') * sh[..., None] + 255 * sp[..., None], 0, 255))
    elif kind == 'mikan':          # a mandarin segment lying as a smile
        c = Cell(80, 40, seed)
        m = np.clip(c.E(40, 6, 36, 28, 0, 1.2) - c.E(40, -2, 32, 22, 0, 1.2), 0, 1)
        c.put(m, C('#e8862a') * (.85 + .25 * c.N(3, 1))[..., None])
        c.put(np.clip(c.E(40, 6, 36, 28, 0, 1.2) - c.E(40, 4, 34, 26, 0, 1.2), 0, 1) * (c.Y > 20), C('#f6c27a'), .7)
    elif kind == 'leaf':
        c = Cell(80, 40, seed)
        m = c.P([(4, 20), (20, 8), (44, 6), (68, 14), (78, 20), (66, 28), (42, 34), (18, 30)])
        c.put(m, C('#3f6a34') * (.8 + .3 * c.N(4, 1))[..., None]); c.put(c.Ln([(6, 20), (74, 19)], 1.6), C('#a9c48a'), .7)
    else:                          # a short twig as a mouth
        c = Cell(80, 30, seed); c.put(c.Ln([(6, 10), (30, 20), (52, 21), (74, 12)], 5), C('#5a3e28'))
    return c.done()


if __name__ == '__main__':
    os.makedirs('out', exist_ok=True)
    S = {'km': (dome('km'), None), 'km_glow': (dome('glow'), None), 'dome': (dome('dome'), None), 'mound': (dome('mound'), None),
         'ball': (ball(), None), 'puddle': (puddle(), None), 'bucket': (bucket(), None), 'cap': (cap(), None), 'scarf': (scarf(), None),
         'scarf_i': (scarf_item(), None), 'lantern': (lantern(), None), 'brazier': (brazier(), None),
         'twig': (twig(False), None), 'pine': (twig(True, 14), None)}
    for k in ('coal', 'pebble', 'berry', 'mikan', 'leaf', 'twigm'): S[k] = (small(k, 20 + len(k)), None)
    at, rect = pack(S, 1456)
    at.save(f'{OUT}/atlas_yk.webp', 'WEBP', quality=88, alpha_quality=90, method=6)
    bg = Image.new('RGBA', at.size, (40, 46, 60, 255)); bg.alpha_composite(at); bg.save('out/yk_atlas.png')
    print(at.size, os.path.getsize(f'{OUT}/atlas_yk.webp'))
    print(json.dumps(rect, separators=(',', ':')))
