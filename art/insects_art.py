#!/usr/bin/env python3
"""Add-on art «Сачок и насекомые»: 14 insects of Japan (2 frames each: still / wings or legs moving) and 3 things
(a bamboo cricket cage, a specimen box, a butterfly net) — all in one atlas.
Usage: cd art && python3 insects_art.py ../assets/items  →  atlas_mu.webp; the rect map is printed as JSON
(pasted into feat/insects.js as MU_R). Preview → art/out/mu_atlas.png"""
import json, math, os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from birds_art import Cv, blur, light, C
from paint import fbm

OUT = sys.argv[1] if len(sys.argv) > 1 else '../assets/items'
SS = 3
D2R = math.pi / 180


class Ins:
    """a sprite cell in final px; painting happens at SS× and is reduced in done()"""
    def __init__(s, w, h, seed=1):
        s.w, s.h, s.seed = w, h, seed; s.cv = Cv(w * SS, h * SS)

    def E(s, cx, cy, rx, ry, ang=0): return s.cv.ell(cx * SS, cy * SS, rx * SS, ry * SS, ang * D2R, 1.2)
    def P(s, pts): return s.cv.poly([(x * SS, y * SS) for x, y in pts])
    def L(s, pts, wd): return s.cv.line([(x * SS, y * SS) for x, y in pts], wd * SS)
    def put(s, m, col, a=1.): s.cv.put(m * a, C(col) if isinstance(col, str) else col)

    def noise(s, sc, seed=0): return fbm(s.cv.w, s.cv.h, sc * SS, 3, s.seed * 7 + seed)

    def shade(s, m, col, sig=5, spec=.15, k=1.6, tex=0., amb=.42, dif=.8, a=1.):
        sh, sp = light(m, sig * SS, k=k, amb=amb, dif=dif, spec=spec)
        c = (C(col)[None, None, :] if isinstance(col, str) else col) * sh[..., None]
        if tex: n = s.noise(3); c = c * (1 - tex / 2 + tex * n[..., None])
        s.cv.put(m * a, np.clip(c + 255 * sp[..., None], 0, 255))

    def leg(s, pts, w0, w1, col='#1e140c', claw=True):
        n = len(pts) - 1
        for i in range(n):
            w = w0 + (w1 - w0) * i / max(1, n - 1)
            s.put(s.L([pts[i], pts[i + 1]], w), col)
        if claw:
            (x0, y0), (x1, y1) = pts[-2], pts[-1]; d = math.hypot(x1 - x0, y1 - y0) or 1; ux, uy = (x1 - x0) / d, (y1 - y0) / d
            for a in (-35, 35):
                c, si = math.cos(a * D2R), math.sin(a * D2R); s.put(s.L([(x1, y1), (x1 + 2.6 * (ux * c - uy * si), y1 + 2.6 * (ux * si + uy * c))], .6), col)

    def wing(s, pts, col, alpha, vein='#3a3a36', veins=(), vw=.45, va=.7):
        m = s.P(pts); s.put(m, col, alpha)
        for v in veins: s.put(s.L(v, vw) * m.clip(0, 1) ** .3, vein, va)
        return m

    def done(s, halo=.5):
        cv = s.cv; a = np.clip(cv.a, 0, 1)
        rgb = cv.rgb + np.random.default_rng(s.seed).normal(0, 3, (cv.h, cv.w))[..., None]
        hl = blur(a, 1.3 * SS) * halo; fa = a + hl * (1 - a)
        frgb = (rgb * a[..., None] + np.array([16, 13, 10])[None, None] * (hl * (1 - a))[..., None]) / np.maximum(fa, 1e-4)[..., None]
        im = Image.fromarray(np.dstack([np.clip(frgb, 0, 255), fa * 255]).astype(np.uint8), 'RGBA')
        return im.resize((s.w, s.h), Image.LANCZOS)


def mirror(pts, cx): return [(2 * cx - x, y) for x, y in pts]
def rot(pts, ox, oy, deg):
    c, si = math.cos(deg * D2R), math.sin(deg * D2R); return [(ox + (x - ox) * c - (y - oy) * si, oy + (x - ox) * si + (y - oy) * c) for x, y in pts]
def squash(pts, cx, k): return [(cx + (x - cx) * k, y) for x, y in pts]


# ── beetles and climbers, seen from above, head up
def dorsal_legs(I, cx, f, sets, col, w0=2.6, w1=1.3):
    for i, (pts) in enumerate(sets):
        for side in (-1, 1):
            sh = (3 if (i + (side > 0)) % 2 == f else -1) if f >= 0 else 0
            p = [(cx + side * (x - cx), y + (sh if j > 0 else 0)) for j, (x, y) in enumerate(pts)]
            I.leg(p, w0, w1, col)


def kabuto(f):
    I = Ins(84, 128, 1); cx = 42
    dorsal_legs(I, cx, f, [[(32, 50), (16, 38), (10, 20)], [(28, 68), (10, 66), (3, 82)], [(30, 88), (12, 98), (8, 120)]], '#24140a', 3.2, 1.6)
    el = I.E(cx, 84, 23, 31); I.shade(el, '#55290f', 8, .55, 2., .14)
    I.put(I.L([(cx, 56), (cx, 114)], 1.1), '#160a04', .8)
    pr = I.E(cx, 50, 21, 15); I.shade(pr, '#3c1d0c', 6, .6, 2.)
    hd = I.E(cx, 35, 10, 7); I.shade(hd, '#2a1408', 3, .3)
    tilt = 2 if f else 0
    hm = np.maximum(I.L([(cx, 40), (cx + tilt * .3, 26), (cx + tilt, 14)], 8.5), I.P([(cx - 4, 44), (cx + 4, 44), (cx, 32)]))
    hm = np.maximum(hm, np.maximum(I.L([(cx + tilt, 15), (cx - 6 + tilt, 4)], 4.4), I.L([(cx + tilt, 15), (cx + 6 + tilt, 4)], 4.4)))
    I.shade(hm, '#3a1c0c', 2.5, .5, 2.)
    I.shade(I.P([(cx - 4, 42), (cx + 4, 42), (cx, 34)]), '#2a1408', 1.5, .4)     # small thoracic horn
    return I.done()


def kuwagata(f):
    I = Ins(80, 124, 2); cx = 40
    dorsal_legs(I, cx, f, [[(30, 58), (16, 50), (10, 36)], [(26, 76), (8, 74), (2, 90)], [(28, 94), (12, 104), (8, 120)]], '#1c120a', 2.8, 1.4)
    el = I.E(cx, 89, 19, 27); I.shade(el, '#2e1a0e', 7, .5, 2., .1)
    I.put(I.L([(cx, 64), (cx, 114)], 1), '#0e0804', .8)
    I.shade(I.E(cx, 59, 18, 11), '#26160c', 5, .5, 2.)
    I.shade(I.E(cx, 43, 17, 9), '#2a170c', 5, .35, 1.8)
    o = 3 if f else 0
    for sd in (-1, 1):
        mp = [(cx + sd * 10, 38), (cx + sd * (17 + o), 26), (cx + sd * (16 + o), 12), (cx + sd * (9 + o * .5), 4)]
        m = np.maximum(I.L(mp, 4.6), I.L([(cx + sd * (16 + o), 22), (cx + sd * (11 + o), 20)], 2.2))
        I.shade(m, '#6a3416', 2, .45, 2.)
    for sd in (-1, 1): I.shade(I.E(cx + sd * 15, 42, 3, 2.6), '#120a06', 1.2, .5)
    return I.done()


def minmin(f):
    I = Ins(80, 104, 3); cx = 40
    for sd in (-1, 1): I.leg([(cx + sd * 8, 42), (cx + sd * 18, 34 - 2 * f), (cx + sd * 22, 24)], 2, 1.2, '#2a3022')
    for sd in (-1, 1): I.leg([(cx + sd * 8, 52), (cx + sd * 20, 56), (cx + sd * 26, 64 + 2 * f)], 2, 1.2, '#2a3022')
    I.shade(I.E(cx, 66, 11, 18), '#2a2a22', 5, .2, 1.6, .2)
    for y in range(54, 84, 5): I.put(I.L([(cx - 9, y), (cx + 9, y)], .6), '#5a5a4a', .5)
    th = I.E(cx, 40, 15, 13); I.shade(th, '#2c3a26', 5, .35, 1.8)
    for sd in (-1, 1): I.shade(I.E(cx + sd * 6, 36, 3.5, 7, sd * 10), '#78a85a', 2, .3)
    I.shade(I.E(cx, 46, 4, 3), '#7aa860', 1.5, .3); I.put(I.E(cx, 30, 6, 2.5), '#cfd8c0', .5)
    I.shade(I.E(cx, 24, 15, 7), '#34442c', 4, .3)
    for sd in (-1, 1): I.shade(I.E(cx + sd * 15, 24, 5, 5), '#6a7a64', 2, .7, 2.)
    for dx in (-3, 0, 3): I.put(I.E(cx + dx, 21 + (dx == 0), 1, 1), '#d84a3a')
    for sd in (-1, 1):
        w = [(cx + sd * 5, 34), (cx + sd * 15, 40), (cx + sd * 22, 70), (cx + sd * 20, 94), (cx + sd * 12, 101), (cx + sd * 3, 86), (cx + sd * 1, 48)]
        if f: w = rot(w, cx + sd * 5, 34, -sd * 16)
        vs = [[w[0], w[3]], [w[0], w[4]], [(w[0][0], w[0][1] + 6), w[5]], [w[1], w[2]]]
        I.wing(w, '#d8e8dc', .3, '#2e4a30', vs, .5, .8)
        I.put(I.L([w[0], w[1], w[2], w[3]], 1.1), '#3a6a3a', .9)
    return I.done()


def fuyu(f):
    I = Ins(96, 84, 4); cx = 48
    if not f:     # wings closed: a piece of bark
        w = [(46, 10), (56, 16), (60, 30), (66, 40), (60, 50), (68, 64), (58, 70), (48, 74), (40, 66), (34, 50), (38, 34), (36, 20)]
        m = I.P(w); n = I.noise(2, 1); n2 = I.noise(6, 2)
        col = C('#5a4c3e')[None, None] * (.55 + .7 * n[..., None]) * (.8 + .4 * n2[..., None])
        I.shade(m, col, 4, .05, 1.2)
        for v in ([(40, 30), (60, 46)], [(38, 48), (64, 60)], [(46, 14), (50, 70)]): I.put(I.L(v, .6) * m, '#2a2018', .6)
        I.put(I.L([(44, 22), (44, 66)], 2.2), '#2a2218', .8)
        for sd in (-1, 1): I.put(I.L([(44, 14), (44 + sd * 3, 6), (44 + sd * 8, 1)], .7), '#2a2218')
        I.put(I.E(52, 40, 2.5, 1.5), '#e8e4d8', .6)
    else:          # wings opened on a warm noon: velvet black with a sky-blue band
        for sd in (-1, 1):
            fw = [(cx + sd * 2, 34), (cx + sd * 26, 12), (cx + sd * 42, 14), (cx + sd * 40, 26), (cx + sd * 32, 38), (cx + sd * 4, 42)]
            hw = [(cx + sd * 3, 42), (cx + sd * 30, 40), (cx + sd * 38, 54), (cx + sd * 30, 66), (cx + sd * 34, 74), (cx + sd * 20, 70), (cx + sd * 4, 54)]
            for w in (hw, fw):
                m = I.P(w); I.shade(m, '#1e2030', 6, .08, 1.2, .25)
            band = (I.L([(cx + sd * 8, 34), (cx + sd * 24, 20), (cx + sd * 38, 18)], 4) + I.L([(cx + sd * 8, 46), (cx + sd * 22, 50), (cx + sd * 32, 62)], 4))
            I.put(np.clip(band, 0, 1) * np.maximum(I.P(fw), I.P(hw)), '#7cc0e0', .9)
            I.put(I.E(cx + sd * 36, 18, 2, 1.6), '#f0f0f0', .9)
        I.shade(I.E(cx, 44, 3, 13), '#2a2620', 2, .2)
        for sd in (-1, 1): I.put(I.L([(cx, 32), (cx + sd * 6, 20), (cx + sd * 10, 12)], .7), '#2a2218')
    return I.done()


def tento(f):
    I = Ins(60, 60, 5); cx = 30
    dorsal_legs(I, cx, f, [[(24, 22), (16, 16), (13, 10)], [(20, 34), (10, 36), (7, 42)], [(22, 44), (12, 50), (10, 56)]], '#141210', 1.6, 1)
    if f:
        for sd in (-1, 1): I.wing([(cx, 30), (cx + sd * 26, 40), (cx + sd * 24, 56), (cx + sd * 6, 50)], '#d8c8b0', .4, '#6a5a48', [[(cx, 30), (cx + sd * 24, 52)]])
    I.shade(I.E(cx, 13, 6, 4), '#141414', 2, .4)
    for sd in (-1, 1): I.put(I.E(cx + sd * 3, 11, 1.4, 1.2), '#e8e4dc')
    I.shade(I.E(cx, 19, 11, 6), '#161616', 3, .5, 1.8)
    for sd in (-1, 1): I.put(I.E(cx + sd * 8, 19, 2.8, 3.2), '#ece8de')
    spots = [(0, 25, 3.6), (-9, 31, 3.4), (9, 31, 3.4), (-12, 42, 3), (12, 42, 3), (-6, 49, 2.6), (6, 49, 2.6)]
    halves = [(-1, -24 if f else 0), (1, 24 if f else 0)]
    for sd, ang in halves:
        ox = cx + sd * (5 if f else 0)
        m = I.E(ox + sd * 8.5, 37, 8.6, 15, ang) if f else I.E(cx, 37, 17, 17) * (I.cv.xx * sd >= cx * SS * sd - .5).astype(np.float32)
        col = np.broadcast_to(C('#c8321e'), (I.cv.h, I.cv.w, 3)).copy()
        for dx, y, r in spots:
            if dx * sd < 0 or (dx == 0 and f): continue
            sx = cx + dx + (sd * 6 if f else 0); sm = I.E(sx, y, r, r)[..., None]; col = col * (1 - sm) + C('#141210') * sm
        I.shade(m, col, 6, .7, 2.2)
    if not f: I.put(I.L([(cx, 21), (cx, 54)], .7), '#3a0a04', .8)
    return I.done()


def hotaru(f):
    I = Ins(52, 66, 6); cx = 26
    dorsal_legs(I, cx, f, [[(22, 22), (14, 18), (11, 12)], [(20, 32), (11, 34), (7, 40)], [(21, 42), (12, 48), (10, 55)]], '#1a1814', 1.4, .9)
    I.shade(I.E(cx, 56, 7, 6), '#e8eaa8', 3, .3, 1.4, amb=.8, dif=.3)
    if f:
        for sd in (-1, 1): I.wing([(cx, 28), (cx + sd * 22, 36), (cx + sd * 22, 54), (cx + sd * 6, 50)], '#c8c8b8', .35, '#4a4a40', [[(cx, 28), (cx + sd * 20, 50)]])
        for sd in (-1, 1): I.shade(I.E(cx + sd * 10, 36, 5, 13, sd * 26), '#1e1e22', 3, .5, 1.8)
    else: I.shade(I.E(cx, 38, 10, 17), '#1c1c20', 4, .45, 1.8); I.put(I.L([(cx, 24), (cx, 54)], .6), '#000000', .8)
    I.shade(I.E(cx, 19, 9, 6), '#e2785a', 3, .3)
    I.put(np.maximum(I.L([(cx, 15), (cx, 23)], 2), I.L([(cx - 3.5, 19), (cx + 3.5, 19)], 1.6)), '#1a1210', .9)
    I.shade(I.E(cx, 12, 4, 3), '#1a1816', 1.5, .3)
    for sd in (-1, 1): I.put(I.L([(cx + sd * 2, 10), (cx + sd * 6, 4), (cx + sd * 9, 1)], .7), '#1a1816')
    return I.done()


# ── butterflies and dragonflies from above
def butterfly(kind, f):
    big = kind == 'ageha'; W, H = (132, 112) if big else (104, 88); I = Ins(W, H, 7 if big else 8); cx = W / 2
    k = .32 if f else 1.
    if big:
        fw = [(cx + 2, 42), (cx + 52, 14), (cx + 61, 22), (cx + 45, 55), (cx + 4, 58)]
        hw = [(cx + 3, 56), (cx + 40, 57), (cx + 47, 73), (cx + 36, 90), (cx + 26, 94), (cx + 21, 108), (cx + 16, 96), (cx + 5, 76)]
    else:
        fw = [(cx + 2, 32), (cx + 38, 13), (cx + 46, 22), (cx + 36, 44), (cx + 3, 46)]
        hw = [(cx + 2, 44), (cx + 30, 46), (cx + 35, 60), (cx + 23, 72), (cx + 5, 66)]
    for sd in (-1, 1):
        F = squash(fw if sd > 0 else mirror(fw, cx), cx, k); Hh = squash(hw if sd > 0 else mirror(hw, cx), cx, k)
        mf, mh = I.P(F), I.P(Hh); m = np.maximum(mf, mh)
        if big:
            col = np.broadcast_to(C('#e6d08a'), (I.cv.h, I.cv.w, 3)).copy()
            edge = np.clip(m - blur(m, 4 * SS * k ** .5) * 1.25, 0, 1)
            blk = np.clip(edge * 2.2, 0, 1)
            base = I.E(cx + sd * 6 * k, 50, 14 * k, 16)
            for v in range(5):     # black stripes along the veins
                t = v / 4; blk = np.maximum(blk, I.L([(cx + sd * 4 * k, 44), (cx + sd * (20 + 30 * t) * k, 18 + 20 * t)], 2.4) * mf)
                blk = np.maximum(blk, I.L([(cx + sd * 5 * k, 60), (cx + sd * (18 + 22 * t) * k, 88 - 26 * t)], 2) * mh)
            blk = np.maximum(blk, base * m)
            col = col * (1 - blk[..., None]) + C('#1a1612') * blk[..., None]
            for t in np.linspace(.15, .85, 5):    # pale lunules in the black margin, blue + red eyespot on the hindwing
                p = F[1][0] + (F[3][0] - F[1][0]) * t, F[1][1] + (F[3][1] - F[1][1]) * t
                lm = I.E(p[0] - sd * 3 * k, p[1], 2.2 * k + .4, 1.6)[..., None]; col = col * (1 - lm) + C('#e0cc8a') * lm
            for t in np.linspace(.1, .8, 4):
                p = Hh[1][0] + (Hh[4][0] - Hh[1][0]) * t, Hh[1][1] + (Hh[4][1] - Hh[1][1]) * t
                lm = I.E(p[0] - sd * 3 * k, p[1] - 3, 2.4 * k + .4, 2)[..., None]; col = col * (1 - lm) + C('#5a78c8') * lm
            em = I.E(cx + sd * 15 * k, 90, 3 * k + .6, 3)[..., None]; col = col * (1 - em) + C('#c8402a') * em
            I.shade(m, col, 3, .05, 1., amb=.62, dif=.45)
        else:
            col = np.broadcast_to(C('#ece8dc'), (I.cv.h, I.cv.w, 3)).copy()
            tip = I.E(cx + sd * 40 * k, 16, 12 * k + .5, 9)[..., None] * mf[..., None]; col = col * (1 - tip * .85) + C('#3a3a3a') * tip * .85
            for (x, y, r) in ((26, 30, 3), (22, 38, 2.6)):
                sm = I.E(cx + sd * x * k, y, r * k + .3, r)[..., None] * mf[..., None]; col = col * (1 - sm) + C('#2a2a2a') * sm
            bs = I.E(cx + sd * 4 * k, 40, 7 * k, 10)[..., None]; col = col * (1 - bs * .5) + C('#8a8a80') * bs * .5
            sm = I.E(cx + sd * 10 * k, 47, 2 * k + .3, 2)[..., None] * mh[..., None]; col = col * (1 - sm) + C('#3a3a3a') * sm
            I.shade(m, col, 3, .04, 1., amb=.66, dif=.4)
        I.put(I.L(F[:3], .7) * mf, '#141210', .5)
    y0, y1 = (34, 84) if big else (26, 66)
    I.shade(I.E(cx, (y0 + y1) / 2 + 4, 3.4 if big else 2.6, (y1 - y0) / 2), '#24201c' if big else '#3a3a38', 2, .3)
    I.shade(I.E(cx, y0, 4 if big else 3, 4 if big else 3), '#24201c' if big else '#3a3a38', 1.5, .4)
    for sd in (-1, 1):
        a = [(cx + sd * 1.5, y0 - 2), (cx + sd * 7, y0 - 16), (cx + sd * 10, y0 - 26)]
        I.put(I.L(a, .8), '#1a1814'); I.put(I.E(a[-1][0], a[-1][1], 1.6, 2), '#1a1814')
    return I.done()


def dragonfly(kind, f):
    aka = kind == 'akatombo'; I = Ins(132, 124, 9 if aka else 10); cx = 66
    wc, base = ('#eef0ea', '#d89a48') if aka else ('#e8eef2', '#7a8a98')
    for sd in (-1, 1):
        fw = [(cx + 3, 26), (cx + 30, 19), (cx + 58, 19), (cx + 62, 24), (cx + 44, 30), (cx + 4, 32)]
        hw = [(cx + 3, 35), (cx + 34, 33), (cx + 58, 37), (cx + 54, 45), (cx + 30, 46), (cx + 4, 42)]
        if f: fw = rot(fw, cx + 3, 28, -10); hw = rot(hw, cx + 3, 38, 12)
        if sd < 0: fw, hw = mirror(fw, cx), mirror(hw, cx)
        for w in (fw, hw):
            m = I.wing(w, wc, .3 if f else .42, "#4a4a46", [[w[0], w[2]], [w[5], w[3]], [(w[0][0] + sd * 10, w[0][1] + 2), w[3]]], .45, .75)
            I.put(I.E(w[0][0] + sd * 6, (w[0][1] + w[-1][1]) / 2, 7, 4) * m, base, .45)
            I.put(I.L([w[0], w[1], w[2]], .9), '#3a3a36', .7)
            tx, ty = w[2][0] - sd * 6, w[2][1] + 1.6; I.put(I.E(tx, ty, 3, 1.3), '#7a2a1a' if aka else '#2a2a2a', .9)
    ab = '#c8341e' if aka else '#8aa4bc'
    am = np.maximum(I.P([(cx - 3.2, 40), (cx + 3.2, 40), (cx + 2.2, 118), (cx - 2.2, 118)]), I.E(cx, 44, 4, 5))
    col = np.broadcast_to(C(ab), (I.cv.h, I.cv.w, 3)).copy()
    if not aka:
        tipm = (I.cv.yy > 100 * SS).astype(np.float32)[..., None]; col = col * (1 - tipm) + C('#1e2226') * tipm
    I.shade(am, col, 1.6, .35, 1.8)
    for y in range(50, 118, 8): I.put(I.L([(cx - 3, y), (cx + 3, y)], .7), '#3a1208' if aka else '#2a3440', .7)
    I.shade(I.E(cx, 30, 7, 10), '#8a4a2a' if aka else '#2a3038', 3, .35)
    I.put(I.L([(cx - 3, 24), (cx - 4, 36)], .8), '#e0b880' if aka else '#8aa0b0', .6)
    I.put(I.L([(cx + 3, 24), (cx + 4, 36)], .8), '#e0b880' if aka else '#8aa0b0', .6)
    for sd in (-1, 1): I.shade(I.E(cx + sd * 5, 15, 6, 6.5), '#9a4028' if aka else '#3a7078', 2.5, .7, 2.)
    return I.done()


# ── crickets, grasshopper, mantis from the side, facing right
def cricket(kind, f):
    suzu = kind == 'suzumushi'; I = Ins(112, 66, 11 if suzu else 12)
    body, wingc, legc = ('#1e1c18', '#3a3228', '#4a3e30') if suzu else ('#9a7e54', '#b89a68', '#8a7050')
    I.leg([(70, 46), (78, 56), (82, 62)], 1.6, 1, legc); I.leg([(58, 46), (60, 56), (56, 62)], 1.6, 1, legc)
    I.put(I.L([(28, 42), (8, 38)], 1.1), legc); I.put(I.L([(28, 44), (10, 46)], 1.1), legc)
    I.shade(I.E(46, 44, 22, 9, -4), body, 4, .35, 1.8, .15)
    if f:     # wings raised: the song
        for o in (0, 3):
            w = [(62, 36), (44 + o, 6), (34 + o, 8), (32 + o, 18), (56, 40)]
            I.wing(w, wingc, .55, '#1a1612' if suzu else '#6a5434', [[(60, 36), (38 + o, 8)], [(58, 38), (34 + o, 16)], [(52, 30), (40 + o, 26)]], .5, .8)
    else:
        w = [(64, 34), (30, 32), (22, 38), (30, 42), (62, 40)]
        I.wing(w, wingc, .85, '#14100c' if suzu else '#6a5434', [[(62, 36), (26, 37)], [(54, 34), (30, 40)], [(46, 33), (38, 41)]], .5, .7)
    I.shade(I.E(66, 38, 9, 8), body, 3, .4, 1.8)
    I.shade(I.E(77, 39, 8, 8), body if suzu else '#8a7048', 3, .45, 1.8)
    I.put(I.E(81, 36, 2, 2.2), '#0a0a0a'); I.put(I.E(80.5, 35.4, .7, .7), '#e8e8e0', .8)
    hl = [(54, 44), (40, 30 - 2 * f), (30, 26 - 2 * f)]
    I.shade(I.L(hl[:2], 5) + I.L(hl[1:], 3.4), legc, 2, .3)
    I.leg([hl[2], (24, 46), (18, 60)], 1.4, 1, legc)
    a = 6 * f
    for dy, (ex, ey) in ((0, (110, 4 + a)), (3, (106, 16 - a))):
        mid = (96, 18 + dy); I.put(I.L([(84, 32), mid, (ex, ey)], .7), '#2a2420' if suzu else '#7a6448')
    if suzu: I.put(I.L([(84, 32), (88, 27)], 1.3), '#ece6d6', .9)
    return I.done()


def batta(f):
    I = Ins(142, 70, 13)
    I.leg([(110, 46), (116, 58), (120, 64)], 1.8, 1.1, '#5a6a38'); I.leg([(96, 48), (96, 58), (92, 64)], 1.8, 1.1, '#5a6a38')
    I.shade(I.E(64, 44, 34, 8, -3), '#8a8a52', 4, .25, 1.6, .15)
    w = [(100, 30), (24, 34), (16, 40), (24, 44), (100, 42)]
    m = I.P(w); n = I.noise(3, 4); col = C('#7a6a46')[None, None] * (.75 + .5 * n[..., None]); I.shade(m, col, 3, .1, 1.3)
    I.put(I.L([(98, 36), (18, 40)], .7), '#4a3e28', .7)
    I.shade(I.E(100, 36, 13, 10), '#6e8444', 4, .3, 1.8, .1)
    I.shade(I.E(118, 38, 11, 12, -15), '#728a46', 4, .35, 1.8)
    I.put(I.E(122, 31, 3.6, 4.6), '#3a2a1c'); I.put(I.E(121, 29.5, 1.2, 1.2), '#e8e4d8', .7)
    for dx in (0, 3): I.put(I.L([(122 + dx, 26), (130 + dx, 14), (134 + dx, 8)], 1), '#4a5a30')
    k = (40, 14) if f else (34, 22)
    fem = np.maximum(I.L([(84, 46), (60, 36)], 9), I.L([(60, 36), k], 6))
    col = C('#6e8a46')[None, None] * (.85 + .3 * np.sin(I.cv.xx / SS * 2.2)[..., None] * .4)
    I.shade(fem, col, 3, .3, 1.8)
    I.leg([k, (k[0] - 10, 58) if not f else (k[0] - 4, 58), (k[0] - 2 if not f else k[0] + 6, 64)], 2.4, 1.6, '#8a4a3a')
    return I.done()


def kamakiri(f):
    I = Ins(126, 120, 14); g, gd = '#7aa048', '#5a7a34'
    for p in ([(72, 82), (84, 98), (90, 114)], [(64, 84), (58, 100), (62, 114)], [(56, 86), (38, 98), (30, 114)]): I.leg(p, 1.8, 1.1, gd)
    I.shade(I.E(42, 86, 32, 10, -10), '#86a856', 4, .25, 1.6, .1)
    I.wing([(72, 76), (14, 88), (12, 94), (72, 84)], '#a8c878', .7, gd, [[(70, 79), (14, 91)]], .6, .8)
    I.shade(I.L([(74, 80), (98, 42)], 6), g, 2, .3)
    if f: hm = I.P([(92, 30), (112, 30), (102, 48)]); eyes = [(93, 32), (111, 32)]
    else: hm = I.P([(92, 36), (112, 28), (106, 46)]); eyes = [(110, 31)]
    I.shade(hm, '#8ab450', 2, .35, 1.8)
    for ex, ey in eyes: I.shade(I.E(ex, ey, 4, 5), '#a8c860', 1.6, .6, 2.); I.put(I.E(ex + .5, ey + 1, 1, 1.2), '#2a3a1a')
    for sd in (-1, 1) if f else (1,):
        ax = 102 + (sd * 3 if f else 4); I.put(I.L([(ax, 30), (ax + sd * 6 + 6, 12), (ax + sd * 10 + 10, 2)], .7), gd)
    lift = 6 if f else 0
    I.shade(I.L([(96, 46), (100, 62)], 5), g, 2, .3)
    I.shade(I.L([(100, 62), (114, 50 - lift)], 4.2), g, 2, .3)
    for t in (.3, .5, .7): x, y = 100 + 14 * t, 62 - (12 + lift) * t; I.put(I.L([(x, y), (x - 1, y + 3)], .8), '#3a4a22')
    I.shade(I.L([(114, 50 - lift), (104, 60 - lift * .5)], 2.6), g, 1.5, .3)
    return I.done()


# ── things
def kago():
    I = Ins(150, 172, 21); cx = 75
    I.shade(I.P([(18, 150), (132, 150), (138, 166), (12, 166)]), '#5a3e26', 4, .2, 1.5, .25)
    inside = I.P([(28, 62), (122, 62), (122, 150), (28, 150)]); I.put(inside, '#1a1610', .55)
    I.shade(I.E(64, 140, 16, 5), '#3a5a28', 3, .3); I.put(I.E(64, 139, 12, 3.4), '#c8d8a0', .9)
    I.shade(I.E(96, 138, 9, 4.5), '#141210', 2, .4); I.put(I.L([(104, 136), (116, 124)], .7), '#e8e2d2', .8)
    for i in range(15):
        x = 30 + i * 6.6; I.shade(I.L([(x, 60), (x, 150)], 1.6), '#c8a868', 1, .3)
    for y in (62, 104, 148): I.shade(I.L([(26, y), (124, y)], 3.4), '#a8844a', 1.5, .3)
    for x in (24, 126): I.shade(I.L([(x, 56), (x, 152)], 4.4), '#8a6a3a', 2, .3)
    I.shade(I.P([(10, 64), (75, 30), (140, 64), (130, 70), (75, 40), (20, 70)]), '#3a2a1c', 3, .35, 1.6, .2)
    I.shade(I.P([(18, 64), (75, 34), (132, 64)]), '#5a4028', 4, .25, 1.4, .3)
    ring = np.clip(I.E(cx, 20, 9, 11) - I.E(cx, 20, 6, 8), 0, 1); I.shade(ring, '#a8844a', 1.4, .3)
    I.put(I.L([(cx, 30), (cx, 36)], 2), '#6a4a2a')
    I.shade(I.E(cx, 112, 9, 9), '#9a7a48', 2, .3); I.put(I.E(cx, 112, 4, 4), '#5a3a20')
    return I.done()


def hako():
    I = Ins(204, 160, 22)
    I.shade(I.P([(6, 8), (198, 8), (198, 150), (6, 150)]), '#8a6a44', 5, .25, 1.4, .3)
    I.put(I.P([(18, 20), (186, 20), (186, 138), (18, 138)]), '#e6dcc4')
    I.put(I.P([(18, 20), (186, 20), (186, 26), (18, 26)]), '#9a8a6a', .5)
    rs = np.random.default_rng(3); cols = ['#4a2a12', '#2a1a0e', '#c8341e', '#e6d08a', '#7aa048', '#8aa4bc', '#1e1c18', '#9a7e54']
    for r in range(3):
        for c in range(5):
            x, y = 38 + c * 32, 40 + r * 36; t = (r * 5 + c) % 8; col = cols[t]
            if t in (3, 5):
                for sd in (-1, 1): I.put(I.E(x + sd * 6, y, 6, 5, sd * 20), col, .95)
                I.put(I.E(x, y + 1, 1.4, 7), '#1a1612')
            else:
                I.shade(I.E(x, y + 2, 5 + (t == 0) * 1.5, 8 + (t == 0) * 2), col, 2, .45, 1.8)
                for sd in (-1, 1): I.put(I.L([(x + sd * 3, y), (x + sd * 9, y - 4)], .7), '#2a2018', .8)
            I.put(I.E(x, y - 7, 1, 1), '#c8c8c8'); I.put(I.L([(x - 6, y + 13), (x + 6, y + 13)], .8), '#8a7a5a', .7)
    I.put(I.P([(18, 20), (186, 20), (186, 138), (18, 138)]) * (I.cv.xx < (I.cv.yy * .8 + 40 * SS)) * (I.cv.xx > (I.cv.yy * .8 + 10 * SS)), '#ffffff', .12)
    for y in (8, 146): I.put(I.L([(6, y + 2), (198, y + 2)], 2), '#4a3420', .6)
    return I.done()


def ami():
    I = Ins(112, 262, 23); cx = 56
    I.shade(I.L([(64, 258), (58, 84)], 5), '#c8a868', 2, .3)
    for y in (120, 170, 220): I.put(I.L([(57 + (258 - y) * .006 * 6, y), (63 + (258 - y) * .0, y)], 2.2), '#8a6a3a', .8)
    bag = I.P([(24, 46), (88, 46), (82, 96), (68, 128), (56, 136), (44, 126), (30, 96)]); I.put(bag, '#dfe6da', .26)
    for i in range(9): x = 26 + i * 7.5; I.put(I.L([(x, 46), (56 + (x - 56) * .3, 132)], .5) * bag, '#e8ece2', .5)
    for j in range(1, 8): y = 46 + j * 11; I.put(I.L([(14, y), (98, y)], .5) * bag, '#e8ece2', .45)
    ring = np.clip(I.E(cx, 44, 34, 30) - I.E(cx, 44, 31, 27), 0, 1); I.shade(ring, '#a8844a', 1.4, .35)
    I.put(I.L([(cx, 74), (58, 86)], 3), '#8a6a3a')
    return I.done()


def pack(sprites, W):
    lst = sorted(sprites.items(), key=lambda kv: -kv[1].height); x = y = rowh = 0; pos = {}
    for k, im in lst:
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[k] = (x, y); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for k, im in lst: at.paste(im, pos[k])
    return at, {k: [pos[k][0], pos[k][1], im.width, im.height] for k, im in sprites.items()}


if __name__ == '__main__':
    os.makedirs('out', exist_ok=True)
    sp = {}
    for f in (0, 1):
        sp[f'kabuto{f}'] = kabuto(f); sp[f'kuwagata{f}'] = kuwagata(f); sp[f'minmin{f}'] = minmin(f); sp[f'fuyu{f}'] = fuyu(f)
        sp[f'tento{f}'] = tento(f); sp[f'hotaru{f}'] = hotaru(f); sp[f'ageha{f}'] = butterfly('ageha', f); sp[f'monshiro{f}'] = butterfly('monshiro', f)
        sp[f'akatombo{f}'] = dragonfly('akatombo', f); sp[f'shiokara{f}'] = dragonfly('shiokara', f)
        sp[f'suzumushi{f}'] = cricket('suzumushi', f); sp[f'matsumushi{f}'] = cricket('matsumushi', f); sp[f'batta{f}'] = batta(f); sp[f'kamakiri{f}'] = kamakiri(f)
    sp['mu_ami'] = ami(); sp['mu_kago'] = kago(); sp['mu_hako'] = hako()
    at, r = pack(sp, 1024)
    at.save(f'{OUT}/atlas_mu.webp', 'WEBP', quality=88, alpha_quality=90, method=6)
    prev = Image.new('RGBA', at.size, (70, 78, 72, 255)); prev.alpha_composite(at); prev.save('out/mu_atlas.png')
    print('atlas_mu', at.size, os.path.getsize(f'{OUT}/atlas_mu.webp') // 1024, 'KB')
    print('MU_R=' + json.dumps(r, separators=(',', ':')))
