#!/usr/bin/env python3
"""«Ханафуда с тануки»: the 48 hanafuda cards (12 months × 4) + the black-red back, packed into one atlas,
and 5 reward things (deck, lacquer box, play cushion, willow fan, «five lights» scroll) in a second atlas.
Usage: hanafuda_art.py  →  assets/items/atlas_hfc.webp (7×7 cards, 100×156 each, 2 px gaps; index = month*4+k, back = 48)
                           assets/items/atlas_hf.webp (+ prints the item rects for feat/hanafuda.js), previews → art/out/"""
import math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CW, CH, K = 100, 156, 4          # card size, supersampling
FONT = '/System/Library/Fonts/Supplemental/Songti.ttc'

def hx(h, a=255):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)

RED, DRED, INK, CREAM = '#c63a2b', '#8a2219', '#1b1613', '#eee2c4'
YEL, GRN, DGRN, BLUE = '#ddb03c', '#4a7d3c', '#26462b', '#2f4f8e'
PURP, PINK, WHITE, BROWN = '#5a3d86', '#e8a3b3', '#f6f0e2', '#7a4a26'


class C:
    """A card painter in card units (0..100 × 0..156), drawn ×K."""
    def __init__(s, seed):
        s.im = Image.new('RGBA', (CW * K, CH * K), (0, 0, 0, 0)); s.d = ImageDraw.Draw(s.im); s.r = random.Random(seed)
    def p(s, pts): return [(x * K, y * K) for x, y in pts]
    def poly(s, pts, col, ol=None, w=1.2):
        s.d.polygon(s.p(pts), fill=hx(col) if isinstance(col, str) else col)
        if ol: s.d.line(s.p(pts + pts[:1]), fill=hx(ol), width=int(w * K), joint='curve')
    def ell(s, cx, cy, rx, ry, col, ol=None, w=1.2):
        s.d.ellipse([(cx - rx) * K, (cy - ry) * K, (cx + rx) * K, (cy + ry) * K], fill=hx(col) if isinstance(col, str) else col, outline=hx(ol) if ol else None, width=int(w * K) if ol else 0)
    def line(s, pts, col, w):
        s.d.line(s.p(pts), fill=hx(col) if isinstance(col, str) else col, width=max(1, int(w * K)), joint='curve')
        for x, y in (pts[0], pts[-1]): s.d.ellipse([(x - w / 2) * K, (y - w / 2) * K, (x + w / 2) * K, (y + w / 2) * K], fill=hx(col) if isinstance(col, str) else col)
    def rect(s, x0, y0, x1, y1, col): s.d.rectangle([x0 * K, y0 * K, x1 * K, y1 * K], fill=hx(col))
    def curve(s, pts, n=24):
        """Catmull-Rom through the points."""
        out = []
        P = [pts[0]] + pts + [pts[-1]]
        for i in range(1, len(P) - 2):
            p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
            for k in range(n):
                t = k / n; t2, t3 = t * t, t * t * t
                out.append(tuple(.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
        out.append(pts[-1]); return out
    def branch(s, pts, col, w0, w1=None):
        c = s.curve(pts); w1 = w0 * .45 if w1 is None else w1
        for i in range(len(c) - 1):
            w = w0 + (w1 - w0) * i / len(c); s.line([c[i], c[i + 1]], col, w)
    def text(s, t, x, y, size, col, vertical=True):
        f = ImageFont.truetype(FONT, int(size * K))
        for i, ch in enumerate(t):
            s.d.text(((x) * K, (y + i * size * 1.02) * K), ch, font=f, fill=hx(col), anchor='mm')

    # ── motifs
    def blossom(s, x, y, r, col, mid=YEL, ol=None):
        for k in range(5):
            a = k / 5 * math.tau - math.pi / 2; s.ell(x + math.cos(a) * r * .55, y + math.sin(a) * r * .55, r * .48, r * .48, col, ol, .5)
        s.ell(x, y, r * .26, r * .26, mid)
    def ribbon(s, x, y, L, ang, col, txt=None, w=13):
        """A tanzaku strip hanging at an angle (degrees from vertical), top at (x,y)."""
        a = math.radians(ang); dx, dy = math.sin(a), math.cos(a); nx, ny = dy, -dx
        c = lambda u, v: (x + dx * u + nx * v, y + dy * u + ny * v)
        sh = '#' + ''.join('%02x' % int(v * .62) for v in hx(col)[:3])
        s.poly([c(0, -w / 2 + 2), c(0, w / 2 + 2), c(L, w / 2 + 2), c(L, -w / 2 + 2)], (0, 0, 0, 70))
        s.poly([c(0, -w / 2), c(0, w / 2), c(L, w / 2), c(L, -w / 2)], col, INK, .8)
        s.poly([c(0, -w / 2), c(0, w / 2), c(7, w / 2), c(5, -w / 2)], sh)
        s.line([c(2, -w / 2 + 2), c(L - 2, -w / 2 + 2)], (255, 255, 255, 60), 1.2)
        if txt:
            f = ImageFont.truetype(FONT, int(8.5 * K)); n = len(txt)
            for i, ch in enumerate(txt):
                u = 14 + i * (L - 22) / max(1, n - 1) if n > 1 else L / 2
                px_, py_ = c(u, 0)
                l = Image.new('RGBA', (int(14 * K), int(14 * K)), (0, 0, 0, 0)); ImageDraw.Draw(l).text((7 * K, 7 * K), ch, font=f, fill=hx(INK), anchor='mm')
                l = l.rotate(-ang, resample=Image.BICUBIC); s.im.alpha_composite(l, (int(px_ * K - 7 * K), int(py_ * K - 7 * K)))
    def mist(s, y, x0, x1, col, h=9):
        s.d.rounded_rectangle([x0 * K, (y - h / 2) * K, x1 * K, (y + h / 2) * K], radius=h / 2 * K, fill=hx(col), outline=hx(INK), width=int(.7 * K))
    def pine_tuft(s, x, y, r, col=DGRN):
        s.d.pieslice([(x - r) * K, (y - r * .8) * K, (x + r) * K, (y + r * .8) * K], 180, 360, fill=hx(col), outline=hx(INK), width=int(.8 * K))
        for k in range(9):
            a = math.pi + (k + .5) / 9 * math.pi; s.line([(x, y), (x + math.cos(a) * r * .95, y + math.sin(a) * r * .76)], INK, .55)
    def hill(s, pts, col, ol=INK):
        s.poly(s.curve(pts, 10) + [(pts[-1][0], 160), (pts[0][0], 160)], col, ol, .9)
    def leaf(s, x, y, L, ang, col, w=.32):
        a = math.radians(ang); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
        pts = [(x, y), (x + dx * L * .5 + nx * L * w, y + dy * L * .5 + ny * L * w), (x + dx * L, y + dy * L), (x + dx * L * .5 - nx * L * w, y + dy * L * .5 - ny * L * w)]
        s.poly(s.curve(pts + [pts[0]], 6), col, INK, .6); s.line([(x, y), (x + dx * L * .9, y + dy * L * .9)], INK, .45)
    def maple_leaf(s, x, y, r, col, rot=0):
        pts = []
        for k in range(14):
            a = rot - math.pi / 2 + k / 14 * math.tau; rr = r if k % 2 == 0 else r * .42
            if k in (6, 8): rr *= .7
            pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
        s.poly(pts, col, INK, .5); s.line([(x, y), (x + math.cos(rot + math.pi / 2) * r * 1.2, y + math.sin(rot + math.pi / 2) * r * 1.2)], INK, .6)
    def chrys(s, x, y, r, col, mid):
        for k in range(22):
            a = k / 22 * math.tau; s.line([(x, y), (x + math.cos(a) * r, y + math.sin(a) * r)], col, r * .28)
        for k in range(22):
            a = (k + .5) / 22 * math.tau; s.line([(x + math.cos(a) * r * .3, y + math.sin(a) * r * .3), (x + math.cos(a) * r * .98, y + math.sin(a) * r * .98)], INK, .35)
        s.ell(x, y, r * .3, r * .3, mid, INK, .5)
    def peony(s, x, y, r):
        for k, (rr, c) in enumerate(((1, RED), (.78, '#d8503c'), (.55, RED), (.32, '#e86a50'))):
            pts = [(x + math.cos(a) * r * rr * (1 + .12 * math.sin(a * 7 + k)), y + math.sin(a) * r * rr * .82 * (1 + .12 * math.sin(a * 7 + k))) for a in np.linspace(0, math.tau, 40)]
            s.poly(pts, c, DRED, .6)
        s.ell(x, y - r * .1, r * .14, r * .1, YEL)
    def bird(s, x, y, sc, body, wing, flip=1, fly=True):
        f = lambda u, v: (x + u * sc * flip, y + v * sc)
        if fly:
            s.poly([f(-2, 0), f(-14, -12), f(-22, -10), f(-6, 2)], wing, INK, .6)
            s.poly([f(2, 0), f(10, -14), f(18, -14), f(8, 2)], wing, INK, .6)
        s.ell(x, y + 1 * sc, 9 * sc, 4 * sc, body, INK, .6)
        s.ell(x + 9 * sc * flip, y - 1 * sc, 3.6 * sc, 3.2 * sc, body, INK, .6)
        s.poly([f(12, -2), f(17, -1), f(12, 0)], INK)
        s.poly([f(-8, 0), f(-16, 4), f(-15, 0)], wing, INK, .5)
        s.ell(x + 10 * sc * flip, y - 1.6 * sc, .7 * sc, .7 * sc, INK)

    def finish(s, back=False):
        """Card body: black edge (the folded back paper), face inside with paper grain."""
        out = Image.new('RGBA', s.im.size, (0, 0, 0, 0)); od = ImageDraw.Draw(out)
        od.rounded_rectangle([0, 0, CW * K - 1, CH * K - 1], radius=7 * K, fill=hx('#15100e'))
        m = Image.new('L', s.im.size, 0); ImageDraw.Draw(m).rounded_rectangle([3.2 * K, 3.2 * K, (CW - 3.2) * K, (CH - 3.2) * K], radius=4.5 * K, fill=255)
        face = Image.new('RGBA', s.im.size, hx('#5a1410') if back else hx(CREAM)); face.alpha_composite(s.im)
        out.paste(face, (0, 0), m)
        out = out.resize((CW, CH), Image.LANCZOS)
        a = np.asarray(out, np.float32); rng = np.random.default_rng(len(s.r.random.__name__) + int(s.r.random() * 1e6))
        g = rng.normal(0, 4.2, a.shape[:2]); a[..., :3] += g[..., None]
        lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True); a[..., :3] = lum + (a[..., :3] - lum) * .9   # a touch muted
        yy = np.linspace(-1, 1, CH)[:, None]; xx = np.linspace(-1, 1, CW)[None, :]
        a[..., :3] *= (1 - .1 * np.clip(xx * xx + yy * yy - .3, 0, 1))[..., None]                       # worn, slightly darker edges
        return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


# ───────────────────────── the 12 months ─────────────────────────
def m1(c, k):   # Pine & crane
    c.hill([(4, 132), (30, 120), (52, 130), (76, 118), (98, 128)], RED, DRED); c.hill([(4, 146), (40, 136), (70, 144), (98, 138)], DRED)
    if k == 'h':
        c.ell(50, 40, 27, 27, RED, DRED, 1); c.branch([(10, 150), (16, 110), (12, 78), (20, 50)], BROWN, 4.5)
        for x, y, r in ((18, 52, 13), (12, 76, 11), (24, 100, 12)): c.pine_tuft(x, y, r)
        # crane: white body facing left, black tail feathers, long neck, red crown
        body = [(46, 102), (54, 92), (70, 88), (86, 94), (82, 106), (62, 110)]
        c.poly(c.curve(body + [body[0]], 6), WHITE, INK, .9)
        c.poly([(80, 92), (96, 100), (92, 104), (98, 110), (84, 106)], INK)
        c.line([(58, 96), (70, 94), (80, 98)], '#b8b2a4', 1)
        c.branch([(54, 96), (50, 80), (56, 66), (58, 56)], WHITE, 5, 3.6); c.line(c.curve([(51, 95), (47, 80), (53, 66), (56, 57)], 6), INK, .6)
        c.ell(58, 53, 4.6, 3.8, WHITE, INK, .6); c.ell(58.5, 50.6, 2.6, 1.6, RED); c.poly([(54, 53), (43, 56), (54, 55.5)], '#c9a24a', INK, .4); c.ell(57, 52.6, .7, .7, INK)
        c.line([(60, 108), (58, 134)], INK, 1.2); c.line([(70, 108), (73, 134)], INK, 1.2)
        c.line([(58, 134), (53, 136)], INK, 1); c.line([(73, 134), (78, 136)], INK, 1)
        return
    c.branch([(30, 152), (40, 120), (36, 86), (56, 60), (76, 40)], BROWN, 6)
    c.branch([(38, 98), (20, 80), (12, 64)], BROWN, 3)
    for x, y, r in ((74, 34, 17), (52, 56, 15), (14, 60, 13), (30, 84, 12), (64, 84, 13), (26, 30, 12)): c.pine_tuft(x, y, r)
    if k == 'r': c.ribbon(54, 70, 62, 14, RED, 'あかよろし')


def m2(c, k):   # Plum & bush warbler
    c.mist(128, 6, 70, RED, 10); c.mist(142, 34, 96, RED, 10)
    c.branch([(8, 150), (24, 112), (16, 80), (40, 52), (60, 20)], INK, 6)
    c.branch([(22, 96), (54, 86), (88, 60)], INK, 3.2); c.branch([(40, 52), (70, 46), (90, 30)], INK, 2.6)
    for x, y in ((60, 22), (46, 44), (74, 44), (88, 30), (30, 70), (56, 84), (80, 64), (14, 96), (36, 104), (70, 72), (24, 52)):
        c.blossom(x, y, 7.5, RED, '#f3e3c0', DRED)
    if k == 't':
        c.ell(58, 104, 12, 8, '#8a9a3a', INK, .8); c.ell(68, 96, 6, 5.5, '#8a9a3a', INK, .8)
        c.poly([(46, 104), (34, 112), (36, 104)], '#6a7a2a', INK, .5); c.poly([(73, 95), (79, 96), (73, 98)], INK)
        c.ell(69, 94.5, 1, 1, INK); c.poly([(52, 100), (64, 104), (52, 110)], '#6e7e2c', INK, .5)
    if k == 'r': c.ribbon(60, 58, 60, 10, RED, 'あかよろし')


def m3(c, k):   # Cherry & curtain
    c.branch([(6, 150), (14, 110), (8, 70)], INK, 6)
    for i, (x, y) in enumerate(((20, 22), (40, 14), (62, 24), (84, 16), (30, 40), (52, 44), (76, 40), (90, 52), (14, 58), (40, 64), (64, 62))):
        c.blossom(x, y, 8, PINK if i % 3 else WHITE, '#d8506a', '#b06070')
    c.mist(78, 4, 60, RED, 10); c.mist(92, 30, 96, RED, 10)
    if k == 'h':
        c.poly([(4, 98), (96, 98), (96, 148), (4, 148)], WHITE, INK, .9)
        for x in range(4, 97, 23): c.poly([(x, 98), (x + 11.5, 98), (x + 11.5, 148), (x, 148)], RED)
        c.line([(4, 100), (96, 100)], INK, 2.2)
        for x in range(10, 96, 14): c.ell(x, 101, 2, 2, YEL, INK, .4)
        c.ell(50, 124, 14, 14, WHITE, INK, 1); c.ell(50, 124, 10, 10, PURP)
        for kk in range(3):
            a = kk / 3 * math.tau - math.pi / 2; c.ell(50 + math.cos(a) * 4.4, 124 + math.sin(a) * 4.4, 3.4, 3.4, WHITE)
    else:
        for x, y in ((24, 104), (58, 116), (84, 108), (36, 132), (72, 138)): c.blossom(x, y, 7, PINK, '#d8506a', '#b06070')
    if k == 'r': c.ribbon(58, 66, 58, 12, RED, 'みよしの')


def m4(c, k):   # Wisteria & cuckoo
    for x, top, n in ((14, 8, 8), (34, 4, 10), (56, 10, 7), (78, 4, 9), (92, 14, 6)):
        c.line([(x, 0), (x + 2, top + n * 7)], '#7a3a20', 1)
        for i in range(n):
            w = 6 - i * .45; c.ell(x + 2 * i / n + (i % 2 - .5) * 2.2, top + i * 7, w, 3.6, PURP if i % 2 else '#3a2a5a', INK, .4)
    for x, y, a in ((20, 6, 30), (48, 4, 160), (70, 8, 20)): c.leaf(x, y, 16, a, GRN)
    if k == 't':
        c.ell(70, 108, 18, 18, YEL, INK, .8); c.ell(78, 102, 16, 16, CREAM)
        c.bird(42, 112, 1.3, '#4a4440', '#2a2522', 1)
        c.ell(56, 111, 1.2, 1.2, RED)
    elif k == 'r': c.ribbon(44, 76, 60, -12, RED)
    else:
        c.line([(8, 150), (30, 128), (60, 136), (92, 120)], '#7a3a20', 1.6)
        for x, y, a in ((30, 128, -60), (60, 136, -110), (80, 124, -40)): c.leaf(x, y, 14, a, GRN)


def m5(c, k):   # Iris & eight-plank bridge
    for x, top, lean in ((12, 40, -6), (26, 30, 4), (44, 48, -3), (62, 34, 6), (80, 44, -4), (92, 56, 2)):
        c.poly([(x - 2.4, 152), (x + lean, top), (x + 2.4, 152)], GRN, INK, .5)
    for x, y in ((24, 36), (60, 30), (84, 46)):
        for a in (-150, -90, -30):
            r = math.radians(a); c.leaf(x, y, 12, a, '#6a50a0', .38)
        for a in (40, 140):
            c.leaf(x, y, 13, a, '#4a3a8a', .42)
        c.ell(x, y + 2, 2.4, 2.4, YEL)
    if k == 't':
        for i, (x0, y0) in enumerate(((0, 98), (46, 116), (0, 134))):
            dx = 62 if i % 2 == 0 else 54
            c.poly([(x0, y0), (x0 + dx, y0 + 10), (x0 + dx, y0 + 18), (x0, y0 + 8)], '#c49a5a', INK, .8)
            for j in range(1, 6): c.line([(x0 + dx * j / 6, y0 + 10 * j / 6), (x0 + dx * j / 6, y0 + 10 * j / 6 + 8)], '#8a6030', .6)
            c.rect(x0 + dx - 3, y0 + 14, x0 + dx, y0 + 26, '#6a4020')
    elif k == 'r': c.ribbon(40, 74, 60, 10, RED)


def m6(c, k):   # Peony & butterflies
    for x, y, a in ((14, 120, -30), (36, 140, -70), (70, 132, -110), (90, 112, -150), (52, 108, -90), (20, 96, -20)): c.leaf(x, y, 20, a, DGRN, .36)
    c.peony(34, 118, 20); c.peony(74, 98, 16)
    if k == 't':
        for x, y, sc, cw, cw2 in ((36, 40, 1.1, '#3a6aaa', YEL), (70, 62, .9, YEL, '#3a6aaa')):
            for sd in (-1, 1):
                c.poly([(x, y), (x + sd * 16 * sc, y - 14 * sc), (x + sd * 20 * sc, y - 2 * sc), (x + sd * 4 * sc, y + 2 * sc)], cw, INK, .6)
                c.poly([(x, y + 2), (x + sd * 14 * sc, y + 6 * sc), (x + sd * 10 * sc, y + 16 * sc), (x + sd * 2, y + 6 * sc)], cw2, INK, .6)
                c.ell(x + sd * 11 * sc, y - 6 * sc, 2.4 * sc, 2.4 * sc, RED)
            c.ell(x, y + 2, 1.6, 7 * sc, INK)
    elif k == 'r': c.ribbon(48, 18, 62, -14, BLUE)
    else:
        c.peony(70 if k == 'k1' else 26, 46, 15)
        for x, y, a in ((50, 52, -10), (86, 40, -160), (40, 30, 30)): c.leaf(x, y, 15, a, DGRN, .36)


def m7(c, k):   # Bush clover & boar
    c.hill([(4, 142), (40, 136), (98, 144)], RED, DRED)
    for (x0, y0, x1, y1, x2, y2) in ((6, 150, 30, 60, 70, 10), (30, 150, 54, 70, 96, 30), (60, 150, 70, 100, 96, 80)):
        pts = c.curve([(x0, y0), (x1, y1), (x2, y2)], 12); c.branch([(x0, y0), (x1, y1), (x2, y2)], INK, 2.2, 1)
        for i in range(2, len(pts) - 1, 3):
            x, y = pts[i]; c.ell(x + 4, y - 1, 3, 2, '#c02a5a', INK, .3); c.leaf(x, y, 7, 160 + (i * 37) % 60, GRN, .4)
    if k == 't':
        c.ell(52, 116, 26, 13, '#6a4428', INK, 1); c.poly([(30, 108), (50, 100), (74, 106), (50, 106)], '#3a2416')
        c.poly([(76, 110), (92, 116), (90, 122), (76, 124)], '#6a4428', INK, .8); c.ell(91, 119, 2.2, 3, '#3a2416')
        c.poly([(70, 104), (74, 98), (76, 108)], '#3a2416', INK, .4); c.ell(82, 113, 1.1, 1.1, INK)
        for x, dx in ((34, -6), (44, 5), (60, -5), (70, 7)): c.line([(x, 124), (x + dx, 136)], '#3a2416', 3)
        c.line([(27, 114), (20, 108)], '#3a2416', 1.4)
    elif k == 'r': c.ribbon(40, 64, 60, -8, RED)


def m8(c, k):   # Susuki: moon / geese
    if k in ('h', 't'): c.rect(0, 0, 100, 100, RED if k == 'h' else '#d8662a')
    if k == 'h': c.ell(50, 52, 30, 30, '#f4ead0', INK, 1)
    if k == 't':
        for x, y, sc in ((26, 30, 1.0), (52, 18, .9), (72, 40, .85)):
            c.bird(x, y, sc * 1.25, '#2a2522', '#1b1613', -1)
    top = 96 if k in ('h', 't') else (70 if k == 'k1' else 80)
    c.hill([(4, top + 6), (30, top - 6), (60, top + 2), (98, top - 4)], INK)
    for i in range(14):
        x = 8 + i * 6.4; y = top + 8 + (i * 7) % 12
        c.branch([(x, 152), (x + 3, y + 20), (x + 9, y)], '#e8dcc0', 1.1, .5)
    for i in range(7):
        x = 10 + i * 13; y = top - 4 + (i * 5) % 8
        c.line([(x, y + 6), (x + 6, y - 6)], '#e8dcc0', .9)


def m9(c, k):   # Chrysanthemum & sake cup
    for x, y, a in ((20, 92, -40), (44, 106, -100), (76, 96, -140), (60, 72, -80), (16, 60, -10), (88, 60, -160)): c.leaf(x, y, 18, a, DGRN, .4)
    c.line([(30, 152), (30, 60)], DGRN, 1.4); c.line([(66, 152), (72, 50)], DGRN, 1.4)
    c.chrys(30, 44, 15, YEL, '#c88a2a'); c.chrys(74, 36, 13, RED, '#f0c060'); c.chrys(52, 76, 10, '#f2e6c8', YEL)
    if k == 't':
        c.ell(50, 134, 24, 6, '#7a1a12', INK, .8); c.poly([(28, 118), (72, 118), (66, 134), (34, 134)], RED, INK, .9)
        c.ell(50, 118, 22, 6, '#e05a40', INK, .9); c.ell(50, 118, 16, 3.6, '#b02a1e')
        c.text('寿', 50, 126, 9, YEL)
    elif k == 'r': c.ribbon(44, 70, 62, 10, BLUE)


def m10(c, k):  # Maple & deer
    c.branch([(96, 6), (60, 30), (30, 26), (6, 44)], INK, 3); c.branch([(60, 30), (70, 60), (96, 70)], INK, 2.2)
    for i, (x, y) in enumerate(((20, 30), (40, 20), (62, 18), (84, 22), (30, 50), (54, 44), (78, 46), (90, 72), (66, 66), (12, 60))):
        c.maple_leaf(x, y, 9, (RED, '#e0782a', '#b8281e')[i % 3], (i * .7) % 1.2 - .6)
    if k == 't':
        c.ell(52, 116, 22, 11, '#a86a36', INK, .9)
        for x in (36, 44, 60, 68): c.line([(x, 120), (x + (2 if x < 50 else -2), 146)], '#7a4a26', 2.6)
        c.branch([(66, 110), (70, 92), (64, 82)], '#a86a36', 7, 5)
        c.ell(60, 80, 7, 5, '#a86a36', INK, .8); c.poly([(54, 80), (46, 84), (55, 84)], '#7a4a26', INK, .5)
        c.poly([(64, 75), (70, 70), (67, 78)], '#7a4a26', INK, .4); c.ell(58, 78.5, 1, 1, INK)
        for x, y in ((40, 112), (50, 108), (58, 116), (46, 120), (62, 108)): c.ell(x, y, 1.6, 1.6, '#f0e2c4')
        c.poly([(30, 112), (25, 106), (32, 108)], '#f0e2c4', INK, .4)
    elif k == 'r': c.ribbon(46, 72, 60, -10, BLUE)
    else:
        for i, (x, y) in enumerate(((24, 110), (58, 124), (82, 104), (40, 140))): c.maple_leaf(x, y, 8, (RED, '#e0782a')[i % 2], i * .5)


def m11(c, k):  # Willow: rain man, swallow, ribbon, lightning
    if k == 'k':
        c.rect(0, 0, 100, 160, RED)
        for x, y, r in ((20, 26, 14), (40, 18, 16), (64, 24, 15), (84, 18, 13)): c.ell(x, y, r, r * .8, INK)
        c.rect(0, 0, 100, 18, INK)
        c.poly([(46, 34), (30, 72), (44, 72), (24, 118), (64, 64), (48, 64), (62, 34)], YEL, INK, .9)
        for x, y in ((22, 134), (50, 140), (78, 132)):
            c.ell(x, y, 10, 10, INK); c.ell(x, y, 6, 6, RED)
            for kk in range(3):
                a = kk / 3 * math.tau; c.ell(x + math.cos(a) * 3, y + math.sin(a) * 3, 2, 2, INK)
        return
    c.rect(0, 0, 100, 160, '#4b5560')
    for i in range(26):
        x = (i * 37) % 100; y = (i * 53) % 150; c.line([(x, y), (x - 3, y + 10)], (210, 220, 230, 120), .5)
    for x0 in (10, 26, 44, 62, 80, 94):
        pts = c.curve([(x0, 0), (x0 - 4, 30), (x0 + 2, 60), (x0 - 2, 70 + (x0 % 3) * 10)], 10)
        c.branch([(x0, 0), (x0 - 4, 30), (x0 + 2, 60), (x0 - 2, 70 + (x0 % 3) * 10)], '#2a3a28', 1.2, .6)
        for i in range(1, len(pts), 3):
            x, y = pts[i]; c.leaf(x, y, 6, 100 + (i % 2) * 40 - 20, '#5a8a3a', .3)
    if k == 'h':
        c.rect(0, 136, 100, 160, '#2a4a7a'); c.line([(0, 140), (100, 138)], '#8aa4c8', .8)
        c.d.pieslice([24 * K, 52 * K, 84 * K, 104 * K], 180, 360, fill=hx(RED), outline=hx(INK), width=int(.9 * K))
        for kk in range(7):
            a = math.pi + (kk + .5) / 7 * math.pi; c.line([(54, 78), (54 + math.cos(a) * 30, 78 + math.sin(a) * 26)], DRED, .5)
        c.line([(54, 78), (50, 112)], INK, 1.2)
        c.poly([(40, 132), (46, 92), (62, 90), (70, 132)], YEL, INK, .9); c.poly([(46, 100), (40, 118), (50, 114)], '#c08a2a', INK, .5)
        c.ell(56, 86, 5, 5.5, '#f0dcc0', INK, .6); c.poly([(51, 82), (61, 82), (58, 74), (54, 74)], INK)
        c.poly([(40, 132), (70, 132), (68, 136), (42, 136)], INK)
        c.ell(20, 128, 7, 5, '#5a9a3a', INK, .8); c.ell(25, 124, 2, 2, '#e8e0a0', INK, .4); c.line([(14, 130), (8, 134)], '#5a9a3a', 1.6)
    elif k == 't':
        c.rect(0, 120, 100, 160, '#2a4a7a')
        c.poly([(30, 84), (56, 72), (80, 90), (58, 80), (40, 94)], INK, INK, .4)
        c.poly([(56, 76), (76, 52), (70, 74)], INK); c.poly([(52, 80), (26, 104), (40, 82)], INK)
        c.ell(54, 79, 3, 2, WHITE); c.ell(78, 88, 2.6, 2.2, RED)
    elif k == 'r': c.ribbon(54, 70, 60, 14, RED)


def m12(c, k):  # Paulownia & phoenix
    if k == 'k3': c.rect(0, 112, 100, 160, YEL)
    for x, y, r in ((24, 128, 22), (72, 122, 24), (48, 146, 18)):
        c.ell(x, y, r, r * .8, '#1f3a26', INK, 1)
        for a in (-150, -110, -70, -30): aa = math.radians(a); c.line([(x, y + r * .4), (x + math.cos(aa) * r * .9, y + r * .4 + math.sin(aa) * r * .9)], '#3a5a3a', .7)
    if k == 'h':
        c.rect(0, 0, 100, 74, YEL)
        for i, col in enumerate((RED, GRN, BLUE, RED, '#e08a2a')):
            c.branch([(52, 40), (30 - i * 4, 54 + i * 4), (8 + i * 2, 80 + i * 6)], col, 4.2 - i * .4, 1.2)
        c.poly([(52, 40), (90, 10), (84, 30), (96, 32), (70, 48)], RED, INK, .9); c.poly([(52, 40), (78, 20), (70, 40)], GRN, INK, .6)
        c.ell(52, 42, 12, 8, '#e05a3a', INK, .8); c.branch([(56, 38), (66, 26), (68, 16)], '#e05a3a', 4, 3)
        c.ell(69, 14, 4, 3.6, '#e05a3a', INK, .6); c.poly([(72, 13), (78, 14), (72, 16)], YEL, INK, .4); c.ell(70, 13, .8, .8, INK)
        c.poly([(66, 10), (64, 4), (70, 9)], GRN, INK, .4)
    else:
        for x, y in ((30, 76), (64, 66), (86, 90)) if k != 'k2' else ((20, 70), (50, 60), (80, 76)):
            c.line([(x, y + 34), (x, y - 20)], '#5a7a4a', 1.2)
            for i in range(7): c.ell(x + (i % 2 - .5) * 6, y - 18 + i * 6, 3.6, 3, PURP if i % 2 else '#7a5aa8', INK, .4)
            c.ell(x, y - 22, 2.4, 2.4, YEL)


MONTHS = [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12]
KINDS = [['h', 'r', 'k1', 'k2'], ['t', 'r', 'k1', 'k2'], ['h', 'r', 'k1', 'k2'], ['t', 'r', 'k1', 'k2'], ['t', 'r', 'k1', 'k2'], ['t', 'r', 'k1', 'k2'],
         ['t', 'r', 'k1', 'k2'], ['h', 't', 'k1', 'k2'], ['t', 'r', 'k1', 'k2'], ['t', 'r', 'k1', 'k2'], ['h', 't', 'r', 'k'], ['h', 'k1', 'k2', 'k3']]


def card(i):
    m, j = divmod(i, 4); c = C(i * 7 + 3); k = KINDS[m][j]
    if k == 'k2':                     # the second plain card: the same plant, mirrored
        MONTHS[m](c, 'k1'); c.im = c.im.transpose(Image.FLIP_LEFT_RIGHT); c.d = ImageDraw.Draw(c.im)
    else: MONTHS[m](c, k)
    return c.finish()


def back():
    c = C(99); d = c.d
    d.rounded_rectangle([7 * K, 7 * K, (CW - 7) * K, (CH - 7) * K], radius=4 * K, fill=hx('#1a0f0c'), outline=hx('#8a2a1c'), width=int(1.4 * K))
    d.rounded_rectangle([11 * K, 11 * K, (CW - 11) * K, (CH - 11) * K], radius=3 * K, outline=hx('#5a1810'), width=int(.8 * K))
    c.ell(50, 78, 17, 17, '#8a2a1c', '#c0503a', 1); c.ell(50, 78, 13, 13, '#2a110c')
    c.text('花', 50, 78, 16, '#c0503a')
    return c.finish(back=True)


def cards_atlas():
    ims = [card(i) for i in range(48)] + [back()]
    at = Image.new('RGBA', (7 * (CW + 2), 7 * (CH + 2)), (0, 0, 0, 0))
    for i, im in enumerate(ims): at.paste(im, ((i % 7) * (CW + 2), (i // 7) * (CH + 2)))
    at.save(f'{ROOT}/assets/items/atlas_hfc.webp', 'WEBP', quality=88, alpha_quality=92, method=6)
    os.makedirs(f'{ROOT}/art/out', exist_ok=True)
    bg = Image.new('RGBA', at.size, hx('#2a2420')); bg.alpha_composite(at); bg.convert('RGB').resize((at.width * 2, at.height * 2), Image.LANCZOS).save(f'{ROOT}/art/out/hf_cards.png')
    return ims


# ───────────────────────── reward things ─────────────────────────
def items(cards):
    sys.argv = [sys.argv[0], f'{ROOT}/art/out']; sys.path.insert(0, f'{ROOT}/art')
    import paint as P
    import items as I
    from items import px, canvas, fill, volume, floor_shadow, line, ell, poly, text, H, dk, lt, SERIF
    OUT = []

    def put(img, name):     # paste a card picture (already 1×) into an item canvas (×S)
        return img

    def card_on(img, ci, x, y, w, rot=0, shadow=True):
        c = cards[ci].resize((px(w), px(w * CH / CW)), Image.LANCZOS)
        if rot: c = c.rotate(rot, expand=True, resample=Image.BICUBIC)
        if shadow:
            sh = Image.new('RGBA', c.size, (0, 0, 0, 0)); sh.putalpha(c.getchannel('A').point(lambda v: v * .45)); sh = sh.filter(ImageFilter.GaussianBlur(px(2)))
            img.alpha_composite(sh, (px(x) - c.width // 2 + px(2), px(y) - c.height // 2 + px(3)))
        img.alpha_composite(c, (px(x) - c.width // 2, px(y) - c.height // 2))

    def done(img, iid):
        out = img.resize((P.W, P.H), Image.LANCZOS); a = np.asarray(out, np.float32)
        lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True); a[..., :3] = lum + (a[..., :3] - lum) * .9
        a[..., :3] += np.random.default_rng(len(iid)).normal(0, 3, a.shape[:2])[..., None]
        OUT.append((iid, Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')))

    # 1. a deck in a paper wrapper with a tanuki leaf + two cards beside it
    img = canvas(170, 120); floor_shadow(img, 85, 112, 78, 100)
    for k in range(6): fill(img, '#1d1412', 3 + k, rect=(34 - k * .3, 58 + k * 3.2, 104 - k * .3, 108 + k * 1), scale=4, contrast=.6)
    fill(img, '#e6d6b0', 11, poly=[(32, 60), (104, 60), (104, 98), (32, 98)], scale=6, contrast=.7, dark=.2)
    ImageDraw.Draw(img).rectangle([px(32), px(72), px(104), px(84)], fill=H('#b8322a'))
    text(img, '花札', 68, 66, 9, '#1b1613', SERIF); text(img, '天狗', 68, 90, 8, '#1b1613', SERIF)
    poly(img, [(84, 50), (98, 40), (106, 52), (94, 60)], '#5a8a3a'); line(img, [(84, 52), (102, 46)], '#2a4a1a', 1)
    card_on(img, 0, 128, 82, 34, -12); card_on(img, 28, 146, 78, 34, 8)
    P.set_size(170, 120); done(img, 'hf_deck')

    # 2. black-red lacquer box, the lid leaning on it, gold 花
    img = canvas(170, 130); floor_shadow(img, 85, 124, 80, 110)
    fill(img, '#1a0d0b', 21, poly=[(24, 70), (130, 70), (130, 118), (24, 118)], scale=8, contrast=.6, dark=.2, light=.25)
    fill(img, '#5a1510', 22, poly=[(24, 62), (130, 62), (144, 50), (38, 50)], scale=8, contrast=.6)
    for k in range(4): card_on(img, (8, 40, 44, 21)[k], 52 + k * 16, 52, 22, (k - 1.5) * 6, False)
    fill(img, '#1a0d0b', 23, poly=[(24, 62), (130, 62), (130, 74), (24, 74)], scale=8, contrast=.6, dark=.2, light=.25)
    volume(img, (24, 62, 130, 118), .5, .25, 0)
    fill(img, '#6a1a12', 24, poly=[(132, 40), (160, 30), (166, 118), (138, 122)], scale=8, contrast=.6)
    d = ImageDraw.Draw(img); d.line([(px(132), px(40)), (px(160), px(30)), (px(166), px(118)), (px(138), px(122)), (px(132), px(40))], fill=H('#c8a24a'), width=px(1.4))
    text(img, '花', 149, 76, 16, '#d8b048', SERIF); d.rectangle([px(24), px(92), px(130), px(94)], fill=H('#b8962a'))
    P.set_size(170, 130); done(img, 'hf_box')

    # 3. the red play cushion (hanafuda is played on a zabuton) with cards laid out
    img = canvas(300, 120); floor_shadow(img, 150, 112, 140, 90)
    pp = [(28, 36), (272, 36), (294, 98), (6, 98)]
    fill(img, '#9a2a20', 31, poly=pp, scale=16, stretch=(3, 1), contrast=.9)
    edge = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(edge).polygon([(px(6), px(98)), (px(294), px(98)), (px(287), px(110)), (px(13), px(110))], fill=H('#5a1410')); img.alpha_composite(edge)
    for x, y in pp: ell(img, (x - 5, y - 5, x + 5, y + 5), '#d8b048')
    for k, ci in enumerate((28, 32, 8, 44, 20)): card_on(img, ci, 70 + k * 30, 66, 22, (k - 2) * 3)
    for k, ci in enumerate((40, 24)): card_on(img, ci, 236 + k * 26, 64, 22, 8 - k * 14)
    card_on(img, 48, 34, 64, 22, -6)
    P.set_size(300, 120); done(img, 'hf_mat')

    # 4. a folding fan with the Willow bright card painted on it
    img = canvas(220, 140); cx, cy, R, r = 110, 132, 108, 36
    m = Image.new('L', img.size, 0); md = ImageDraw.Draw(m)
    md.pieslice([px(cx - R), px(cy - R), px(cx + R), px(cy + R)], 200, 340, fill=255); md.pieslice([px(cx - r), px(cy - r), px(cx + r), px(cy + r)], 200, 340, fill=0)
    fill(img, '#4b5560', 41, mask=m, scale=8, contrast=.7)
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); c = cards[40].resize((px(64), px(100)), Image.LANCZOS)
    l.alpha_composite(c, (px(cx - 32), px(cy - 112))); a = np.asarray(l, np.float32); a[..., 3] *= np.asarray(m, np.float32) / 255; img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))
    d = ImageDraw.Draw(img)
    for k in range(16):
        aa = math.radians(200 + k * 140 / 15)
        d.line([(px(cx + math.cos(aa) * r), px(cy + math.sin(aa) * r)), (px(cx + math.cos(aa) * R), px(cy + math.sin(aa) * R))], fill=(20, 20, 24, 90), width=px(1))
        d.line([(px(cx), px(cy)), (px(cx + math.cos(aa) * r), px(cy + math.sin(aa) * r))], fill=H('#2a1a12'), width=px(2.4))
    ell(img, (cx - 5, cy - 5, cx + 5, cy + 5), '#b8962a')
    P.set_size(220, 140); done(img, 'hf_fan')

    # 5. a hanging scroll with the five bright cards
    img = canvas(130, 330)
    line(img, [(36, 4), (65, 0), (94, 4)], '#1a120c', 1.4)
    ImageDraw.Draw(img).rectangle([px(14), px(8), px(116), px(16)], fill=H('#2a1c14'))
    fill(img, '#3a2a4a', 51, rect=(12, 14, 118, 312), scale=6, contrast=1.1)
    fill(img, '#e9e1cc', 52, rect=(22, 40, 108, 280), scale=10, contrast=.6, dark=.12, light=.1)
    text(img, '五光', 65, 58, 15, '#1b1714', SERIF, brush=True)
    for k, ci in enumerate((0, 8, 28, 40, 44)):
        x, y = (44, 86, 44, 86, 65)[k], (108, 108, 170, 170, 236)[k]; card_on(img, ci, x, y, 30, 0)
    d = ImageDraw.Draw(img); d.rectangle([px(8), px(306), px(122), px(320)], fill=H('#1e140e'))
    for x in (6, 114): d.rectangle([px(x), px(304), px(x + 10), px(322)], fill=H('#caa860'))
    P.set_size(130, 330); done(img, 'hf_scroll')

    # pack in one row
    W = sum(im.width + 2 for _, im in OUT); Hh = max(im.height for _, im in OUT)
    at = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); x = 0; rects = {}
    for iid, im in OUT: at.paste(im, (x, 0)); rects[iid] = (x, 0, im.width, im.height); x += im.width + 2
    at.save(f'{ROOT}/assets/items/atlas_hf.webp', 'WEBP', quality=88, alpha_quality=92, method=6)
    bg = Image.new('RGBA', at.size, hx('#2a2420')); bg.alpha_composite(at); bg.convert('RGB').save(f'{ROOT}/art/out/hf_items.png')
    print('atlas_hf', at.size, rects)


if __name__ == '__main__':
    cs = cards_atlas()
    items(cs)
