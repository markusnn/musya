#!/usr/bin/env python3
"""«Теневой театр» (kage-e): 22 black cut-paper silhouettes for the shadow screen (crisp, with cut-out holes where
light shows through: eyes, ribs, lattice) + 2 collectible things (a small kage-e screen with a fox shadow, a box of paper
figures on rods). One atlas: 6×4 cells of 240 px (2 px gaps); the things sit in the last two cells.
Usage: python3 art/shadow_art.py → assets/items/atlas_kg.webp (+ art/out/shadow_preview.png); prints the JS rect map."""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets/items/atlas_kg.webp')
PREV = os.path.join(ROOT, 'art/out'); os.makedirs(PREV, exist_ok=True)
C, SS, GAP = 240, 4, 2
U = C * SS / 100            # one unit of the 100×100 figure grid in supersampled px
SERIF = '/System/Library/Fonts/Supplemental/Songti.ttc'
if not os.path.exists(SERIF): SERIF = '/System/Library/Fonts/Hiragino Sans GB.ttc'


def cr(pts, n=10, closed=False):
    """Catmull-Rom spline through the points → dense polyline."""
    P = list(pts); out = []
    if closed: P = [P[-1]] + P + [P[0], P[1]]
    else: P = [P[0]] + P + [P[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = (np.array(P[j], float) for j in (i - 1, i, i + 1, i + 2))
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)))
    if not closed: out.append(tuple(P[-2]))
    return out


class M:
    def __init__(s): s.im = Image.new('L', (C * SS, C * SS), 0); s.d = ImageDraw.Draw(s.im)
    def pg(s, pts, v=255): s.d.polygon([(x * U, y * U) for x, y in pts], fill=v)
    def blob(s, pts, v=255): s.pg(cr(pts, 8, True), v)                       # smooth closed shape
    def ell(s, cx, cy, rx, ry, v=255, rot=0):
        if rot:
            c, si = math.cos(rot), math.sin(rot)
            s.pg([(cx + rx * math.cos(a) * c - ry * math.sin(a) * si, cy + rx * math.cos(a) * si + ry * math.sin(a) * c) for a in np.linspace(0, 2 * math.pi, 72, endpoint=False)], v)
        else: s.d.ellipse([(cx - rx) * U, (cy - ry) * U, (cx + rx) * U, (cy + ry) * U], fill=v)
    def ln(s, pts, w, v=255, smooth=False):
        if smooth: pts = cr(pts, 8)
        s.d.line([(x * U, y * U) for x, y in pts], fill=v, width=max(1, int(w * U)), joint='curve')
        r = w * U / 2
        for x, y in (pts[0], pts[-1]): s.d.ellipse([x * U - r, y * U - r, x * U + r, y * U + r], fill=v)
    def tube(s, pts, w0, w1, v=255):                                         # tapered stroke along a spline
        q = cr(pts, 10); n = len(q); L, R = [], []
        for i, (x, y) in enumerate(q):
            a, b = q[max(0, i - 1)], q[min(n - 1, i + 1)]; dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy) or 1
            w = (w0 + (w1 - w0) * i / (n - 1)) / 2; L.append((x - dy / d * w, y + dx / d * w)); R.append((x + dy / d * w, y - dx / d * w))
        s.pg(L + R[::-1], v); r = w0 / 2; x, y = q[0]; s.ell(x, y, r, r, v)
        return q
    def rect(s, x0, y0, x1, y1, v=255): s.d.rectangle([x0 * U, y0 * U, x1 * U, y1 * U], fill=v)
    def pie(s, cx, cy, r, a0, a1, v=255): s.d.pieslice([(cx - r) * U, (cy - r) * U, (cx + r) * U, (cy + r) * U], a0, a1, fill=v)
    def text(s, ch, x, y, size, v=0):
        s.d.text((x * U, y * U), ch, font=ImageFont.truetype(SERIF, int(size * U)), fill=v, anchor='mm')
    def waves(s, y, amp=1.6, per=12, bot=100):
        s.pg([(x, y + amp * math.sin(x / per * 2 * math.pi)) for x in np.linspace(0, 100, 80)] + [(100, bot), (0, bot)])
    def eye(s, x, y, r=1.6, ry=None): s.ell(x, y, r, ry or r * .75, 0)
    def out(s): return s.im.resize((C, C), Image.LANCZOS)


def rotp(pts, cx, cy, a): c, si = math.cos(a), math.sin(a); return [(cx + (x - cx) * c - (y - cy) * si, cy + (x - cx) * si + (y - cy) * c) for x, y in pts]


# ───────────────────────── the figures (all face right, stand on y≈96) ─────────────────────────
def cat(m):
    m.blob([(30, 95), (22, 80), (26, 60), (40, 46), (56, 44), (64, 56), (64, 78), (66, 95)])
    m.ell(63, 36, 12, 11); m.pg([(54, 30), (56, 15), (63, 27)]); m.pg([(64, 26), (72, 15), (74, 31)])
    m.ell(73, 40, 6, 4.4); m.rect(56, 70, 64, 95); m.ell(62, 95, 7, 2)
    m.ln([(28, 92), (14, 95), (6, 88), (6, 77), (11, 72)], 5, smooth=True)
    m.eye(67, 34, 2.2, 1.1); m.ln([(78, 41), (92, 37)], .5, 0); m.ln([(78, 43), (92, 45)], .5, 0)
    m.ln([(77, 41), (92, 37)], .55); m.ln([(77, 43), (92, 46)], .55)


def fox(m):
    m.blob([(36, 80), (22, 86), (8, 76), (3, 56), (10, 38), (19, 32), (18, 48), (22, 64), (34, 72)])     # tail
    m.blob([(34, 95), (30, 76), (36, 56), (48, 44), (58, 46), (62, 60), (62, 80), (64, 95)])
    m.ell(62, 38, 10, 9); m.pg([(58, 32), (74, 34), (88, 40), (86, 43), (70, 47), (58, 46)])
    m.pg([(55, 32), (57, 11), (65, 29)]); m.pg([(63, 29), (71, 10), (73, 33)])
    m.rect(55, 64, 61, 95); m.ell(60, 95, 6, 2)
    m.ell(68, 36, 3, 1, 0, -.35)
    for k in range(3): m.ln(cr([(10 + k * 3, 52 + k * 7), (15 + k * 3, 62 + k * 5), (24 + k * 2, 70 + k * 3)], 6), .7, 0)
    m.ell(9, 37, 3, 2, 0, .6)                                                                           # pale tail tip ring


def tanuki(m):
    m.ell(74, 86, 9, 6, 255, -.4)                                                                       # tail
    m.ell(48, 64, 24, 27); m.ell(48, 34, 15, 13)
    m.ell(48, 22, 21, 5); m.ell(48, 17, 10, 8)                                                         # straw hat
    m.ell(38, 93, 9, 4); m.ell(58, 93, 9, 4)
    m.ln([(30, 52), (22, 64), (24, 72)], 7, smooth=True)
    m.pg([(14, 66), (22, 64), (24, 82), (12, 84)]); m.ell(18, 64, 3, 2.4)                             # sake flask
    m.rect(15, 72, 22, 76, 0)
    m.ln([(66, 52), (74, 62), (72, 70)], 7, smooth=True)
    m.ell(42, 34, 3.4, 2.8, 0); m.ell(54, 34, 3.4, 2.8, 0); m.ell(42.5, 34.5, 1.4, 1.4); m.ell(53.5, 34.5, 1.4, 1.4)
    m.ell(48, 40, 2.4, 1.6, 0)
    m.d.arc([(36 * U), (60 * U), (60 * U), (86 * U)], 200, 340, fill=0, width=int(.9 * U))               # belly line


def crane(m):
    m.ell(44, 52, 20, 10, 255, -.18)
    m.tube([(56, 46), (63, 34), (66, 22), (70, 13)], 5, 3.4); m.ell(71, 12, 4, 3.4)
    m.pg([(73, 10.5), (88, 14), (73, 14)]); m.eye(71, 11, 1, .8)
    m.pg([(26, 50), (12, 60), (18, 59), (10, 67), (21, 62), (17, 70), (28, 60)])                     # bustle
    m.pg([(32, 48), (34, 30), (42, 14), (52, 6), (56, 18), (54, 34), (48, 48)])                       # raised wing
    for k in range(4): m.ln([(40 + k * 3.5, 22 - k * 3), (44 + k * 3, 36 - k * 2.5)], .8, 0)
    m.ln([(45, 60), (46, 80), (47, 95)], 1.6); m.ln([(49, 60), (54, 72), (47, 75)], 1.6)
    m.ln([(40, 95.5), (54, 95.5)], 1.4)


def rabbit(m):
    m.ell(35, 66, 12, 16, 255, .25); m.ell(41, 44, 9, 8); m.ell(48, 47, 4, 3)
    m.ell(35, 25, 3.3, 13, 255, -.25); m.ell(44, 26, 3, 12.5, 255, .2)
    m.ln([(40, 58), (54, 46)], 3.4); m.ln([(40, 66), (72, 33)], 2.4)
    m.pg(rotp([(63, 28), (83, 28), (83, 36), (63, 36)], 73, 32, .77)); m.ell(*rotp([(63, 32)], 73, 32, .77)[0], 4, 4); m.ell(*rotp([(83, 32)], 73, 32, .77)[0], 4, 4)
    m.ell(31, 86, 10, 7); m.ell(37, 94, 10, 2.6); m.ell(23, 71, 4.4, 4.4)
    m.pg([(62, 76), (90, 76), (86, 84), (83, 95), (69, 95), (66, 84)]); m.ell(76, 76, 14, 3)
    m.ell(76, 74, 9, 3)                                                                                # mochi
    m.eye(45, 42, 1.4, 1.1); m.ln([(30, 15), (32, 30)], .7, 0)


def oni(m):
    m.ell(48, 27, 13, 13)
    m.pg([(32, 26)] + [(48 + 18 * math.cos(a) + (2.5 if i % 2 else -1.5) * math.cos(a), 27 + 18 * math.sin(a)) for i, a in enumerate(np.linspace(math.pi * .95, math.pi * 2.05, 15))] + [(64, 26)])
    m.pg([(40, 18), (35, 3), (45, 14)]); m.pg([(55, 14), (62, 2), (60, 19)])
    m.pg([(32, 40), (64, 40), (71, 62), (27, 62)])
    m.pg([(27, 62)] + [(27 + 44 * i / 10, 76 + (3 if i % 2 else 0)) for i in range(11)] + [(71, 62)])
    for k in range(4): m.ln([(33 + k * 9, 64), (36 + k * 9, 72)], 1.1, 0)
    m.pg([(33, 76), (46, 76), (44, 95), (31, 95)]); m.pg([(52, 76), (65, 76), (67, 95), (54, 95)])
    m.ell(36, 95, 7, 2); m.ell(62, 95, 7, 2)
    m.ln([(33, 44), (22, 58), (24, 70)], 7, smooth=True); m.ln([(63, 44), (76, 38), (80, 26)], 7, smooth=True)
    club = rotp([(77, 33), (81, 33), (84.5, 6), (82, 1), (76, 1), (73.5, 6)], 79, 28, .22); m.pg(club)
    for k in range(5):
        for j in (-1, 1):
            x, y = rotp([(79 + j * (1.6 + k * .45), 24 - k * 4.4)], 79, 28, .22)[0]; m.ell(x, y, .75, .75, 0)
    m.ell(43, 25, 3.2, 2.4, 0); m.ell(53, 25, 3.2, 2.4, 0)
    m.pg([(41, 32), (55, 32), (53, 36.5), (43, 36.5)], 0); m.pg([(43, 32), (45, 35), (46, 32)]); m.pg([(50, 32), (51, 35), (53, 32)])


def yurei(m):
    m.blob([(46, 30), (58, 28), (66, 44), (68, 58), (62, 72), (52, 82), (40, 90), (26, 96), (34, 86), (42, 72), (44, 52)])
    m.ell(56, 21, 8, 9.5)
    m.blob([(50, 12), (58, 11), (52, 22), (50, 36), (46, 52), (40, 62), (42, 48), (44, 32)])            # hair
    for k in range(5): m.ln([(47 - k, 20 + k * 5), (40 - k * 2, 46 + k * 4)], .9)
    m.pg([(58, 33), (79, 39), (82, 45), (60, 45)])
    for k in range(3): m.ln([(78 + k * 1.4, 42), (80 + k * 1.6, 48), (79.5 + k * 1.6, 53)], 1.3, smooth=True)
    m.pg([(56, 12.5), (62, 11.5), (60, 16.5)], 0)                                                      # hitaikakushi
    for k in range(4): m.ln([(50 + k * 3, 40 + k * 8), (46 + k * 3, 54 + k * 7)], .7, 0)
    m.blob([(84, 22), (88, 14), (86, 6), (91, 13), (92, 22), (88, 26)])                                # hitodama
    m.ell(88.5, 21, 1.6, 1.6, 0)


def kappa(m):
    m.ell(34, 56, 12, 17, 255, -.15)                                                                   # shell
    for y in (46, 56, 66): m.ln([(25, y), (30, y - 3), (38, y - 3), (43, y)], .8, 0)
    m.ln([(30, 42), (30, 70)], .8, 0); m.ln([(38, 41), (38, 70)], .8, 0)
    m.ell(48, 60, 14, 16); m.ell(54, 28, 12, 11)
    m.pg([(41, 22)] + [(54 + 15 * math.cos(a) * (1 if i % 2 else .82), 23 + 9 * math.sin(a) * (1 if i % 2 else .82)) for i, a in enumerate(np.linspace(math.pi, math.pi * 2, 13))] + [(67, 22)])
    m.ell(54, 15, 9, 3.2, 0); m.ell(54, 15, 7, 2)
    m.pg([(63, 26), (76, 30), (63, 33)]); m.eye(59, 25, 2, 1.8)
    m.ln([(56, 52), (68, 58)], 4.4); m.ell(78, 56, 11, 3, 255, -.45)
    for k in range(4): m.ell(72 + k * 3, 59 - k * 1.5, .6, .6, 0)
    m.pg([(66, 52), (72, 50), (70, 56), (72, 60), (66, 60)])
    m.pg([(40, 72), (50, 72), (46, 86), (54, 92), (38, 93)]); m.pg([(52, 72), (60, 70), (64, 86), (70, 94), (54, 94)])
    m.pg([(34, 93), (40, 89), (39, 95.5), (32, 96)])


def pine(m):
    m.ell(46, 97, 20, 3)
    m.tube([(46, 96), (44, 82), (52, 66), (47, 52), (57, 38), (62, 24)], 10, 3)
    m.tube([(50, 64), (36, 58), (20, 52)], 4.4, 1.6); m.tube([(51, 49), (70, 44), (84, 38)], 3.6, 1.4); m.tube([(48, 52), (40, 38)], 3, 1.4)

    def pad(cx, cy, w, h):
        m.ell(cx - w * .32, cy, w * .36, h * .55); m.ell(cx + w * .02, cy - h * .28, w * .42, h * .7); m.ell(cx + w * .34, cy + h * .02, w * .34, h * .52)
        m.rect(cx - w * .62, cy, cx + w * .62, cy + h * .45)
        m.pg([(cx - w * .62 + i * w * 1.24 / 18, cy + h * (.45 if i % 2 else .75)) for i in range(19)] + [(cx + w * .62, cy), (cx - w * .62, cy)])
        for i in range(7): m.ln([(cx - w * .5 + i * w / 6, cy + h * .3), (cx - w * .45 + i * w / 6, cy + h * .6)], .5, 0)
    pad(19, 47, 30, 11); pad(84, 33, 27, 10); pad(60, 16, 34, 12); pad(39, 32, 20, 8)
    m.ln([(44, 86), (49, 80)], .6, 0); m.ln([(49, 70), (53, 64)], .6, 0)


def house(m):
    m.rect(14, 46, 86, 92); m.rect(10, 91, 90, 96)
    m.pg([(4, 48), (26, 16), (74, 16), (96, 48)]); m.pg([(38, 17), (43, 5), (57, 5), (62, 17)]); m.rect(36, 3, 64, 7)
    m.pg([(46, 9), (54, 9), (50, 14)], 0)
    for i in range(10): m.ln([(9 + i * 9, 46), (28 + i * 5, 18)], .5, 0)                                 # thatch strokes
    m.rect(22, 56, 42, 74, 0)
    for x in np.arange(24.5, 42, 3.5): m.rect(x, 56, x + .9, 74)
    m.rect(22, 64.5, 42, 65.5)
    m.rect(54, 58, 74, 92, 0); m.rect(54, 58, 74, 67)
    for x in (59, 64, 69): m.rect(x, 58, x + .8, 67, 0)                                                  # noren
    m.rect(77, 56, 82, 74, 0)


def bridge(m):
    top = [(0, 64), (25, 48), (50, 42), (75, 48), (100, 64)]
    deck = cr(top, 10); m.pg(deck + [(x, y + 8) for x, y in deck[::-1]])
    rail = [(x, y - 14) for x, y in top]; m.ln(cr(rail, 10), 2.4)
    for x, y in cr(top, 2)[1:-1]: m.ln([(x, y), (x, y - 14)], 2)
    for x, y in (top[0], top[-1]):
        x = min(97, max(3, x)); m.ln([(x, y), (x, y - 17)], 3); m.ell(x, y - 19, 2.4, 2.4); m.pg([(x - 1, y - 21), (x, y - 25), (x + 1, y - 21)])
    m.ln(cr([(x, y - 7) for x, y in top], 10), 1)
    for x in (20, 80): m.rect(x - 2, 56, x + 2, 96)
    m.rect(48, 50, 52, 96)
    m.waves(91, 1.8, 14)
    for i in range(6): m.ln([(5 + i * 17, 95), (12 + i * 17, 94)], .6, 0)


def moon(m):
    m.ell(52, 48, 34, 30)
    for i, a in enumerate(np.linspace(0, 2 * math.pi, 15, endpoint=False)):
        r = (11, 15, 9, 13, 16, 10, 12)[i % 7]; m.ell(52 + 37 * math.cos(a), 48 + 32 * math.sin(a), r, r * .82)
    m.ell(56, 44, 23, 23, 0)
    m.blob([(28, 58), (44, 52), (62, 55), (80, 50), (86, 56), (70, 62), (50, 62), (34, 66)])          # cloud wisp
    m.ell(42, 54, 6, 4); m.ell(66, 52, 5, 3.5)
    for x, y, r in ((18, 30, 1.6), (26, 74, 1.2), (84, 76, 1.4), (14, 54, 1), (80, 18, 1.1)):
        m.pg([(x, y - r * 2), (x + r, y), (x, y + r * 2), (x - r, y)], 0)


def boat(m):
    m.pg([(4, 70), (86, 68), (98, 56), (96, 68), (88, 82), (14, 82)])
    m.waves(84, 1.6, 12)
    m.ln([(10, 99), (38, 34)], 1.5)
    m.pg([(20, 48), (31, 48), (33, 70), (19, 70)]); m.ell(26, 42, 4, 4.2); m.pg([(15, 41), (26, 33), (37, 41)])
    m.ln([(29, 52), (33, 50), (32, 46)], 2.6)
    m.pg([(46, 50), (82, 50), (88, 56), (40, 56)]); m.rect(46, 55, 48, 70); m.rect(78, 55, 80, 69)
    m.rect(49, 58, 77, 66, 255)
    for x in range(52, 77, 5): m.rect(x, 59, x + 2.6, 65, 0)
    for i in range(5): m.ln([(18 + i * 15, 76), (26 + i * 15, 76)], .7, 0)


def samurai(m):
    m.ell(55, 17, 7, 8); m.pg([(49, 10), (57, 7), (61, 9.5), (52, 12)]); m.pg([(61, 15), (64.5, 18), (61, 19.5)])
    m.rect(52, 22, 58, 28)
    m.pg([(34, 26), (78, 26), (71, 33), (41, 33)])
    m.pg([(45, 30), (66, 30), (65, 53), (47, 53)])
    m.pg([(44, 52), (68, 52), (77, 95), (35, 95)])
    for x in (49, 56, 63): m.ln([(x, 58), (x + (x - 56) * .35, 92)], .7, 0)
    m.ln([(66, 49), (28, 61)], 2.2); m.ell(61, 50.5, 1.2, 3, 255, .3); m.ln([(66, 47), (36, 54)], 1.7)
    m.ln([(62, 32), (66, 43), (64, 49)], 4.2, smooth=True)
    m.ell(39, 95.5, 5, 1.6); m.ell(73, 95.5, 5, 1.6); m.eye(58, 15.5, 1.1, .8)


def princess(m):
    m.blob([(52, 12), (49, 30), (45, 56), (38, 82), (28, 96), (46, 96), (52, 64), (56, 34)])            # hair
    m.ell(58, 18, 7, 8)
    m.pg([(52, 26), (64, 26), (76, 56), (84, 96), (24, 96), (40, 58)])
    m.blob([(62, 32), (78, 38), (88, 50), (88, 68), (74, 68), (66, 48)])                                # sleeve
    m.pie(85, 40, 14, -165, -25)
    for a in range(-155, -30, 16):
        r = math.radians(a); m.ln([(85 + 4 * math.cos(r), 40 + 4 * math.sin(r)), (85 + 12.5 * math.cos(r), 40 + 12.5 * math.sin(r))], .55, 0)
    for k in range(3):
        y = 84 + k * 3.2; m.ln(cr([(27 + k * 2, y), (55, y - 2), (82 - k, y)], 6), .6, 0)
        m.ln([(72 + k * 2.2, 54 + k * 2), (86, 64 - k * 3.5)], .55, 0)
    m.ln([(56, 9), (63, 5)], .8); m.ell(63.5, 4.8, 1.2, 1.2); m.eye(61, 17, 1.1, .7)


def dragon(m):
    spine = [(80, 30), (66, 26), (55, 40), (45, 58), (31, 63), (19, 52), (11, 38), (4, 30)]
    q = cr(spine, 10); n = len(q); L, R = [], []
    for i, (x, y) in enumerate(q):
        a, b = q[max(0, i - 1)], q[min(n - 1, i + 1)]; dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy) or 1
        w = 4.6 * (1 - i / n) ** .7 + .7; L.append((x - dy / d * w, y + dx / d * w)); R.append((x + dy / d * w, y - dx / d * w))
        if 3 < i < n - 4 and i % 4 == 0:
            m.pg([(x + dy / d * w * .9, y - dx / d * w * .9), (x + dy / d * (w + 4) - dx / d * 2, y - dx / d * (w + 4) - dy / d * 2), (x + dx / d * 2.4, y + dy / d * 2.4)])
        if 4 < i < n - 3 and i % 7 == 0: m.ln([(x - dy / d * w * .2, y), (x + dx / d * 1.5 - dy / d * w * .8, y + dy / d * 1.5 + dx / d * w * .8)], .5, 0)
    m.pg(L + R[::-1])
    m.blob([(76, 23), (88, 23), (96, 27), (90, 32), (78, 36), (74, 30)])
    m.pg([(85, 29.5), (97, 31), (86, 32.5)], 0)
    m.ln([(78, 24), (72, 12), (65, 7)], 1.6, smooth=True); m.ln([(81, 23), (79, 9)], 1.3)
    m.ln([(95, 26), (100, 17), (97, 8)], .7, smooth=True); m.ln([(94, 32), (99, 40), (96, 48)], .7, smooth=True)
    for k in range(5): m.pg([(72 - k * 2, 24 + k * 2), (64 - k * 3, 18 + k * 4), (70 - k * 2, 28 + k * 2)])
    m.eye(83, 26, 1.3, 1)
    for (i, side) in ((int(n * .2), 1), (int(n * .55), 1)):
        x, y = q[i]; m.ln([(x, y), (x + 5, y + 9), (x + 2, y + 15)], 2.2)
        for c in (-2, 0, 2): m.ln([(x + 2, y + 15), (x + 2 + c * 1.3, y + 18)], .9)
    m.ell(96, 52, 4, 4); m.ell(96, 52, 1.6, 1.6, 0)
    for a in (-1.2, -.6, 0, .6, 1.2): m.ln([(96 + 4 * math.sin(a), 52 - 4 * math.cos(a)), (96 + 7 * math.sin(a), 52 - 7.5 * math.cos(a))], .8)


def butterfly(m):
    m.blob([(50, 46), (36, 22), (16, 12), (6, 22), (14, 38), (32, 48)])
    m.blob([(52, 46), (64, 22), (84, 12), (94, 22), (86, 38), (68, 48)])
    m.blob([(48, 52), (34, 56), (22, 70), (26, 82), (38, 76), (46, 64)]); m.ln([(28, 78), (22, 92)], 2.4)
    m.blob([(52, 52), (66, 56), (78, 70), (74, 82), (62, 76), (54, 64)]); m.ln([(72, 78), (78, 92)], 2.4)
    m.ell(50, 52, 2.6, 14)
    m.ln([(49, 39), (44, 26), (40, 22)], .8, smooth=True); m.ln([(51, 39), (56, 26), (60, 22)], .8, smooth=True)
    m.ell(40, 22, 1.4, 1.4); m.ell(60, 22, 1.4, 1.4)
    for sx in (-1, 1):
        cx = 50 + sx * 24; m.ell(cx, 26, 6, 4.6, 0, sx * .5); m.ell(50 + sx * 33, 20, 2.2, 2.2, 0); m.ell(50 + sx * 14, 66, 3, 3.4, 0)
        for k in range(3): m.ln([(50 + sx * 6, 44), (50 + sx * (16 + k * 8), 34 - k * 8)], .6, 0)


def lantern(m):
    m.ln([(54, 22), (40, 12), (20, 12), (5, 22)], 1.8, smooth=True); m.ln([(54, 22), (54, 28)], .8)
    m.ell(54, 54, 19, 25); m.rect(42, 26, 66, 31); m.rect(42, 77, 66, 82); m.rect(50, 82, 58, 86)
    for k in range(1, 9):
        y = 30 + k * 5.2; w = 19 * math.sqrt(max(0, 1 - ((y - 54) / 25) ** 2)) - 1.5
        if w > 2: m.ln(cr([(54 - w, y), (54, y + 1.2), (54 + w, y)], 6), .55, 0)
    m.ell(54, 54, 8, 9.5, 255); m.text('灯', 54, 54, 13, 0)


def karakasa(m):
    pts = [(50, 6), (82, 58)] + [(82 - i * 64 / 12, 58 + (3 if i % 2 else 0)) for i in range(13)] + [(18, 58)]
    m.pg(pts); m.ln([(50, 6), (50, 1)], 2.2)
    for x in (30, 40, 60, 70): m.ln([(50, 10), (x, 56)], .6, 0)
    m.ell(51, 30, 7.5, 6.4, 0); m.ell(52.5, 31, 3.2, 3.2)
    m.ell(52, 45, 6, 2.6, 0)
    m.blob([(50, 46), (60, 50), (68, 58), (74, 68), (68, 70), (62, 60), (54, 50)])
    m.ln([(50, 58), (49, 86)], 3.2); m.rect(39, 86, 60, 90); m.rect(41, 90, 45, 95); m.rect(54, 90, 58, 95)
    m.ln([(26, 40), (16, 34)], .9); m.ln([(74, 40), (84, 34)], .9)


def musya(m):
    m.blob([(30, 95), (28, 78), (36, 60), (48, 54), (60, 60), (62, 78), (60, 95)])
    m.ell(56, 40, 15, 13.5); m.pg([(44, 34), (44, 16), (55, 28)]); m.pg([(58, 27), (70, 15), (70, 33)])
    m.ell(68, 45, 6, 4.4)
    m.ln([(56, 62), (68, 52), (74, 43)], 5.2, smooth=True); m.ell(75.5, 41, 4.2, 3.6)
    m.rect(50, 70, 57, 95); m.ell(55, 95, 6.5, 2)
    m.tube([(32, 88), (18, 82), (14, 66), (22, 54), (18, 42), (12, 38)], 5.6, 2.2)
    m.ell(62, 38, 2.6, 3, 0); m.ell(62.6, 38.6, 1, 1.6)
    for k in range(3): m.ln([(40 + k * 4, 64 + k), (43 + k * 4, 72 + k)], .7, 0)
    m.ln([(72, 46), (86, 42)], .5); m.ln([(72, 48), (86, 50)], .5)
    m.ln([(46, 30), (49, 27)], .6, 0); m.ln([(47, 34), (51, 31)], .6, 0)


def peach(m):
    m.waves(84, 1.8, 13)
    m.ell(42, 58, 22, 24); m.ell(58, 58, 22, 24); m.pg([(30, 44), (50, 22), (70, 44)])
    m.ln(cr([(50, 26), (47, 46), (50, 66), (49, 80)], 8), 1, 0)
    m.ln([(50, 26), (52, 18), (55, 12)], 1.6, smooth=True)
    for cx, cy, rot in ((62, 15, -.5), (40, 17, .5)): m.ell(cx, cy, 11, 4.6, 255, rot)
    m.ln([(55, 17), (69, 11)], .5, 0); m.ln([(47, 19), (33, 21)], .5, 0)
    m.ell(36, 52, 4, 6, 0, .3)


def oldman(m):
    m.pg(rotp([(26, 22), (46, 22), (46, 40), (26, 40)], 36, 31, -.3))                                  # firewood bundle
    for k in range(5): m.ln([(x, y) for x, y in rotp([(24, 24 + k * 3.6), (48, 24 + k * 3.6)], 36, 31, -.3)], 1.4)
    m.ell(60, 24, 7, 7.5); m.blob([(61, 29), (70, 31), (66, 44), (60, 38)])
    m.blob([(46, 30), (60, 32), (66, 52), (62, 70), (44, 70), (40, 48)])
    m.pg([(43, 68), (64, 68), (63, 90), (45, 90)])
    m.ln([(50, 89), (47, 96)], 2.6); m.ln([(58, 89), (62, 96)], 2.6); m.ell(46, 96, 3.6, 1.4); m.ell(64, 96, 3.6, 1.4)
    m.ln([(58, 40), (66, 48), (74, 47)], 3.4, smooth=True)
    m.ln([(77, 20), (76, 60), (74, 97)], 1.7, smooth=True); m.ell(77.5, 19, 2.4, 2.4)
    m.eye(64, 22, 1, .7); m.ln([(54, 18), (58, 15)], .7)
    m.ln(cr([(46, 50), (55, 52), (62, 50)], 6), .6, 0)


FIGS = [('cat', cat), ('fox', fox), ('tanuki', tanuki), ('crane', crane), ('rabbit', rabbit), ('oni', oni), ('yurei', yurei),
        ('kappa', kappa), ('pine', pine), ('house', house), ('bridge', bridge), ('moon', moon), ('boat', boat), ('samurai', samurai),
        ('princess', princess), ('dragon', dragon), ('butterfly', butterfly), ('lantern', lantern), ('karakasa', karakasa),
        ('musya', musya), ('peach', peach), ('oldman', oldman)]


def sil(fn):
    m = M(); fn(m); a = m.out(); im = Image.new('RGBA', (C, C), (0, 0, 0, 0)); im.putalpha(a); return im, a


# ───────────────────────── the two things ─────────────────────────
def noise(w, h, seed, blur, stretch=(1, 1)):
    r = np.random.default_rng(seed).random((max(2, int(h / stretch[1])), max(2, int(w / stretch[0]))))
    im = Image.fromarray((r * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(im, np.float32) / 255; return (a - a.mean()) / (a.std() + 1e-6)


def wood(w, h, base, seed, grain=(3, 40)):
    n = noise(w, h, seed, 1.2, grain) * .55 + noise(w, h, seed + 9, 3) * .25
    a = np.zeros((h, w, 4), np.float32); a[..., :3] = np.array(base, np.float32) * (1 + .16 * n[..., None]); a[..., 3] = 255
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def paste_mask(dst, src, mask_box, mask):
    x0, y0, x1, y1 = mask_box; m = Image.new('L', dst.size, 0); m.paste(mask.resize((x1 - x0, y1 - y0), Image.LANCZOS), (x0, y0))
    dst.paste(src, (0, 0), m)


def finish(img, w, h, seed):
    out = img.resize((w, h), Image.LANCZOS); a = np.asarray(out, np.float32)
    lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True); a[..., :3] = lum + (a[..., :3] - lum) * .9
    a[..., :3] += np.random.default_rng(seed).normal(0, 3.2, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def screen_item(fox_a):
    w, h, k = 220, 240, 2; W, H = w * k, h * k; img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    # paper lit from behind: warm radial glow from the bottom middle
    px0, py0, px1, py1 = 34 * k, 22 * k, 186 * k, 204 * k
    yy, xx = np.mgrid[py0:py1, px0:px1].astype(np.float32); cx, cy = (px0 + px1) / 2, py1 - 30 * k
    r = np.sqrt(((xx - cx) / (W * .55)) ** 2 + ((yy - cy) / (H * .62)) ** 2)
    lit = np.clip(1.05 - r * .95, 0, 1) ** 1.3; pap = np.zeros(xx.shape + (4,), np.float32)
    for i, (lo, hi) in enumerate(((92, 252), (52, 214), (24, 150))): pap[..., i] = lo + (hi - lo) * lit
    fib = noise(px1 - px0, py1 - py0, 3, 1.4, (1, 6)); pap[..., :3] *= (1 + .05 * fib[..., None]); pap[..., 3] = 255
    paper = Image.fromarray(np.clip(pap, 0, 255).astype(np.uint8), 'RGBA'); img.paste(paper, (px0, py0))
    # the fox shadow on the paper, slightly soft
    sh = Image.new('RGBA', (W, H), (36, 18, 8, 0)); fm = Image.new('L', (W, H), 0)
    fm.paste(fox_a.resize((128 * k, 128 * k), Image.LANCZOS), (int(48 * k), int(70 * k)))
    fm = fm.filter(ImageFilter.GaussianBlur(1.6 * k)).point(lambda v: int(v * .86)); sh.putalpha(fm)
    clip = Image.new('L', (W, H), 0); ImageDraw.Draw(clip).rectangle([px0, py0, px1, py1], fill=255)
    sh.putalpha(Image.fromarray(np.minimum(np.asarray(fm), np.asarray(clip)))); img.alpha_composite(sh)
    # frame, lattice and feet in dark wood
    fr = wood(W, H, (70, 44, 28), 5); m = Image.new('L', (W, H), 0); md = ImageDraw.Draw(m)
    md.rectangle([22 * k, 10 * k, 198 * k, 216 * k], fill=255); md.rectangle([px0, py0, px1, py1], fill=0)
    for x in (85, 135): md.rectangle([x * k - 2 * k, py0, x * k + 2 * k, py1], fill=255)
    for y in (68, 114, 160): md.rectangle([px0, y * k - 2 * k, px1, y * k + 2 * k], fill=255)
    md.rectangle([40 * k, 216 * k, 62 * k, 228 * k], fill=255); md.rectangle([158 * k, 216 * k, 180 * k, 228 * k], fill=255)
    md.rounded_rectangle([18 * k, 226 * k, 84 * k, 236 * k], 4 * k, fill=255); md.rounded_rectangle([136 * k, 226 * k, 202 * k, 236 * k], 4 * k, fill=255)
    img.paste(fr, (0, 0), m)
    d.line([(22 * k, 11 * k), (198 * k, 11 * k)], fill=(150, 104, 62, 255), width=2 * k)
    for x in (85, 135): d.line([(x * k - 2 * k, py0), (x * k - 2 * k, py1)], fill=(120, 80, 46, 255), width=k)
    d.line([(px0, py0), (px1, py0)], fill=(20, 12, 6, 200), width=2 * k)
    # warm spill of light on the frame
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse([60 * k, 120 * k, 160 * k, 250 * k], fill=(255, 190, 110, 50))
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(14 * k)))
    a = np.asarray(img).copy(); a[..., 3] = np.where(np.asarray(m) | np.asarray(clip) | (a[..., 3] > 0), a[..., 3], 0); img = Image.fromarray(a, 'RGBA')
    return finish(img, w, h, 11)


def box_item(masks):
    w, h, k = 236, 170, 2; W, H = w * k, h * k; img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([20 * k, 150 * k, 222 * k, 168 * k], fill=(0, 0, 0, 120)); img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5 * k)))
    # leaning lid behind on the right
    lid = wood(W, H, (150, 120, 84), 21, (40, 3)); m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).polygon([(150 * k, 70 * k), (214 * k, 52 * k), (226 * k, 150 * k), (166 * k, 158 * k)], fill=255); img.paste(lid, (0, 0), m)
    d.line([(150 * k, 70 * k), (214 * k, 52 * k)], fill=(190, 160, 118, 255), width=2 * k)
    # figures on bamboo rods sticking out of the box
    for name, x, y, s, rot in (('crane', 30, 16, 74, -.12), ('fox', 72, 4, 80, .05), ('moon', 108, 22, 62, .1), ('butterfly', 140, 30, 46, .2), ('oni', 50, 42, 52, -.2)):
        rx = x + s * .5; d.line([(rx * k, (y + s * .8) * k), ((rx + rot * 30) * k, 120 * k)], fill=(168, 140, 86, 255), width=int(2.2 * k))
        fm = masks[name].resize((s * k, s * k), Image.LANCZOS).rotate(-rot * 40, resample=Image.BICUBIC)
        blk = Image.new('RGBA', fm.size, (16, 10, 8, 255)); img.paste(blk, (x * k, y * k), fm)
    # the box: dark opening, front and side faces
    d.polygon([(26 * k, 100 * k), (156 * k, 100 * k), (178 * k, 86 * k), (48 * k, 86 * k)], fill=(26, 18, 12, 255))
    front = wood(W, H, (172, 138, 96), 31, (36, 3)); m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).polygon([(26 * k, 100 * k), (156 * k, 100 * k), (156 * k, 156 * k), (26 * k, 156 * k)], fill=255); img.paste(front, (0, 0), m)
    side = wood(W, H, (122, 96, 64), 41, (3, 30)); m2 = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m2).polygon([(156 * k, 100 * k), (178 * k, 86 * k), (178 * k, 142 * k), (156 * k, 156 * k)], fill=255); img.paste(side, (0, 0), m2)
    d.line([(26 * k, 100 * k), (156 * k, 100 * k), (178 * k, 86 * k)], fill=(210, 182, 140, 255), width=2 * k)
    d.line([(26 * k, 156 * k), (156 * k, 156 * k), (178 * k, 142 * k)], fill=(60, 42, 26, 255), width=2 * k)
    # paper label 影絵
    d.rectangle([76 * k, 108 * k, 106 * k, 150 * k], fill=(226, 212, 180, 255)); d.rectangle([76 * k, 108 * k, 106 * k, 150 * k], outline=(150, 40, 30, 255), width=k)
    f = ImageFont.truetype(SERIF, 15 * k); d.text((91 * k, 119 * k), '影', font=f, fill=(30, 20, 14, 255), anchor='mm'); d.text((91 * k, 138 * k), '絵', font=f, fill=(30, 20, 14, 255), anchor='mm')
    # cord
    d.line([(36 * k, 128 * k), (66 * k, 128 * k)], fill=(150, 40, 34, 255), width=2 * k); d.line([(116 * k, 128 * k), (146 * k, 128 * k)], fill=(150, 40, 34, 255), width=2 * k)
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse([0, 60 * k, 120 * k, 170 * k], fill=(255, 190, 110, 34)); img.alpha_composite(g.filter(ImageFilter.GaussianBlur(16 * k)))
    a = np.asarray(img).copy(); a[..., 3] = np.where(a[..., 3] < 8, 0, a[..., 3]); img = Image.fromarray(a, 'RGBA')
    return finish(img, w, h, 12)


def build():
    cols, rows = 6, 4; AW, AH = cols * (C + GAP) - GAP, rows * (C + GAP) - GAP
    atlas = Image.new('RGBA', (AW, AH), (0, 0, 0, 0)); rects, boxes, masks = {}, {}, {}
    for i, (name, fn) in enumerate(FIGS):
        im, a = sil(fn); masks[name] = a; x, y = (i % cols) * (C + GAP), (i // cols) * (C + GAP)
        atlas.paste(im, (x, y)); rects[name] = [x, y]; bb = a.point(lambda v: 255 if v > 60 else 0).getbbox(); boxes[name] = [round(v / C, 3) for v in bb]
    x, y = 4 * (C + GAP), 3 * (C + GAP); scr = screen_item(masks['fox']); atlas.paste(scr, (x, y)); rects['kg_screen'] = [x, y, scr.width, scr.height]
    x = 5 * (C + GAP); bx = box_item(masks); atlas.paste(bx, (x, y)); rects['kg_box'] = [x, y, bx.width, bx.height]
    atlas.save(OUT, 'WEBP', quality=88, alpha_quality=92, method=6)
    pv = Image.new('RGBA', (AW, AH), (222, 196, 150, 255)); pv.alpha_composite(atlas); pv.convert('RGB').save(os.path.join(PREV, 'shadow_preview.png'))
    print('atlas', AW, AH, os.path.getsize(OUT) // 1024, 'KB')
    print('const KGR=' + json.dumps(rects, separators=(',', ':')) + ';')
    print('const KGB=' + json.dumps(boxes, separators=(',', ':')) + ';')


if __name__ == '__main__':
    build()
