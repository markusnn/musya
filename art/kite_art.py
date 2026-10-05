#!/usr/bin/env python3
"""«Воздушный змей» (tako-age): 9 painted washi kites (Edo-dako kanji kites 風 寿 龍, a carp, a yakko footman, a Shirone
crane, a fox mask, a musha warrior, the tengu's fighting kite) in one atlas, and the town strip for the flight scene
(far ridge, a pagoda, kawara roofs, a cedar and two pines, the grassy embankment Musya stands on).
Usage: python3 art/kite_art.py → assets/items/atlas_ta.webp + assets/bg/ta_sky.webp (+ art/out/kite_preview.png);
prints the rect map (TA_R in feat/kite.js) and the tree boxes of the strip (TA_TREES)."""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paint import fbm

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREV = os.path.join(ROOT, 'art/out'); os.makedirs(PREV, exist_ok=True)
SS = 3
FONT = '/System/Library/Fonts/Hiragino Sans GB.ttc'


def C(h, a=255):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


class K:
    """One kite painted at SS× in final-pixel units."""
    def __init__(s, w, h, seed):
        s.w, s.h, s.W, s.H, s.seed = w, h, w * SS, h * SS, seed
        s.im = Image.new('RGBA', (s.W, s.H), (0, 0, 0, 0)); s.k = 0
        s.n = fbm(s.W, s.H, 40 * SS, 5, seed)
    def p(s, x, y): return (x * SS, y * SS)
    def m(s): return Image.new('L', (s.W, s.H), 0)
    def put(s, m, col, tex=.10, blur=.5):
        if blur: m = m.filter(ImageFilter.GaussianBlur(blur * SS / 2))
        s.k += 1; n = fbm(s.W, s.H, 18 * SS, 4, s.seed * 31 + s.k) * .6 + s.n * .4
        rgb = np.array(col[:3], np.float32)[None, None] * (1 + (n[..., None] - .5) * 2 * tex)
        a = np.asarray(m, np.float32)[..., None] * col[3] / 255
        lay = Image.fromarray(np.concatenate([np.clip(rgb, 0, 255), a], -1).astype(np.uint8), 'RGBA')
        s.im.alpha_composite(lay)
    def poly(s, pts, col, tex=.10, blur=.5):
        m = s.m(); ImageDraw.Draw(m).polygon([s.p(*q) for q in pts], fill=255); s.put(m, col, tex, blur)
    def ell(s, cx, cy, rx, ry, col, tex=.10, blur=.5):
        m = s.m(); ImageDraw.Draw(m).ellipse([s.p(cx - rx, cy - ry), s.p(cx + rx, cy + ry)], fill=255); s.put(m, col, tex, blur)
    def line(s, pts, col, w, tex=.06, blur=.4):
        m = s.m(); d = ImageDraw.Draw(m); P = [s.p(*q) for q in pts]; d.line(P, fill=255, width=max(1, int(w * SS)), joint='curve')
        r = w * SS / 2
        for q in (P[0], P[-1]): d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=255)
        s.put(m, col, tex, blur)
    def arc(s, cx, cy, r, a0, a1, col, w):
        s.line([(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in np.linspace(a0, a1, 24)], col, w)
    def kanji(s, ch, cx, cy, size, fill, stroke, sw):
        f = ImageFont.truetype(FONT, int(size * SS), index=2)
        for col, wd in ((stroke, sw), (fill, 0)):
            m = s.m(); ImageDraw.Draw(m).text(s.p(cx, cy), ch, font=f, fill=255, anchor='mm', stroke_width=int(wd * SS), stroke_fill=255)
            a = np.asarray(m, np.float32); rough = fbm(s.W, s.H, 3 * SS, 3, s.seed + int(wd) + 5)
            a = np.where(a > 0, np.clip(a * (0.75 + .5 * rough), 0, 255), 0)        # dry-brush edge
            s.put(Image.fromarray(a.astype(np.uint8)), col, .12, .6)
    def paper(s, pts, col='#eadfc6', rim='#3a2a1c'):
        s.shape = pts; s.poly(pts, C(rim), .1, .3)
        cx = sum(q[0] for q in pts) / len(pts); cy = sum(q[1] for q in pts) / len(pts)
        ins = [(cx + (x - cx) * (1 - 2.6 / max(1, abs(x - cx) + 1e-3) if abs(x - cx) > 3 else 1), cy + (y - cy) * (1 - 2.6 / max(1, abs(y - cy)) if abs(y - cy) > 3 else 1)) for x, y in pts]
        s.poly(ins, C(col), .16, .3)
        # washi fibres
        rnd = np.random.default_rng(s.seed); m = s.m(); d = ImageDraw.Draw(m)
        for _ in range(int(s.w * s.h / 40)):
            x, y = rnd.random() * s.W, rnd.random() * s.H; a = rnd.random() * 6.3; L = rnd.random() * 6 * SS + SS
            d.line([(x, y), (x + math.cos(a) * L, y + math.sin(a) * L)], fill=int(40 + rnd.random() * 50), width=1)
        clip = s.m(); ImageDraw.Draw(clip).polygon([s.p(*q) for q in ins], fill=255)
        s.put(Image.fromarray(np.minimum(np.asarray(m), np.asarray(clip))), C('#fff6e0'), 0, 0)
    def bones(s, lines, col=(50, 34, 20, 46)):
        for a, b in lines: s.line([a, b], col, 1.6, 0, .8)
    def finish(s):
        im = s.im
        # the paper bows in the wind: lit top-left, shaded bottom-right; a bit of rim darkening
        a = np.asarray(im, np.float32); yy, xx = np.mgrid[0:s.H, 0:s.W]
        g = 1.07 - .16 * (xx / s.W * .45 + yy / s.H * .55)
        al = a[..., 3:4] / 255; e = np.asarray(Image.fromarray(a[..., 3].astype(np.uint8)).filter(ImageFilter.GaussianBlur(5 * SS)), np.float32)[..., None] / 255
        a[..., :3] *= g[..., None] * (.82 + .18 * e)
        a[..., :3] = np.clip(a[..., :3], 0, 255); im = Image.fromarray(a.astype(np.uint8), 'RGBA')
        im = im.resize((s.w, s.h), Image.LANCZOS)
        a = np.asarray(im, np.float32); n = np.random.default_rng(s.seed).normal(0, 3.5, a.shape[:2])[..., None]
        a[..., :3] = np.clip(a[..., :3] + n, 0, 255); return Image.fromarray(a.astype(np.uint8), 'RGBA')


def rect(w, h, m=2): return [(m, m), (w - m, m), (w - m, h - m), (m, h - m)]
def edo_bones(w, h): return [((w / 2, 4), (w / 2, h - 4)), ((4, h * .18), (w - 4, h * .18)), ((4, h * .5), (w - 4, h * .5)), ((4, h * .82), (w - 4, h * .82))]
def sq_bones(w, h): return [((4, 4), (w - 4, h - 4)), ((w - 4, 4), (4, h - 4)), ((w / 2, 4), (w / 2, h - 4)), ((4, h / 2), (w - 4, h / 2))]
RED, INK, GOLD, IND = C('#c4302a'), C('#1c1714'), C('#d6a740'), C('#27355e')


def seal(k, x, y, sz=11):
    k.poly([(x, y), (x + sz, y), (x + sz, y + sz), (x, y + sz)], C('#b8322a'), .1, .3)
    k.line([(x + 3, y + 3), (x + sz - 3, y + 3)], C('#f3e6cc', 200), 1.1); k.line([(x + sz / 2, y + 3), (x + sz / 2, y + sz - 3)], C('#f3e6cc', 200), 1.1)


def kite_kanji(ch, seed, paper='#eadfc6', fill=INK, stroke=RED, extra=None):
    w, h = 150, 200; k = K(w, h, seed); k.paper(rect(w, h), paper)
    if extra: extra(k)
    k.bones(edo_bones(w, h)); k.kanji(ch, w / 2, h / 2 + 2, 118, fill, stroke, 7.5); seal(k, w - 22, h - 22); return k.finish()


def ryu_clouds(k):
    for cx, cy, r in ((30, 40, 16), (122, 60, 13), (36, 160, 14), (118, 168, 18), (75, 24, 10)):
        for i in range(3): k.arc(cx, cy, r - i * 5, 180, 470, C('#7aa0c0', 150), 2.2)


def gold_dust(k):
    rnd = np.random.default_rng(7)
    for _ in range(70): x, y, r = rnd.random() * 140 + 5, rnd.random() * 190 + 5, rnd.random() * 1.6 + .5; k.ell(x, y, r, r, C('#d6a740', 200), 0, .2)


def kite_koi():
    w, h = 150, 200; k = K(w, h, 21); k.paper(rect(w, h), '#26345c')
    for row in range(9):           # seigaiha waves
        for col in range(-1, 6):
            cx, cy = col * 30 + (15 if row % 2 else 0), 60 + row * 16
            for r in (14, 9, 4): k.arc(cx, cy, r, 180, 360, C('#a8c4dc', 130 if r > 5 else 90), 1.3)
    k.bones(edo_bones(w, h), (220, 220, 230, 30))
    # the carp climbs a waterfall: head up, body S-curve, tail at the bottom
    cl = [(76, 30), (82, 60), (80, 92), (70, 122), (64, 148), (70, 166)]; wd = [16, 27, 28, 22, 14, 6]
    L, R = [], []
    for i, (x, y) in enumerate(cl):
        a, b = cl[max(0, i - 1)], cl[min(len(cl) - 1, i + 1)]; dx, dy = b[0] - a[0], b[1] - a[1]; n = math.hypot(dx, dy); nx, ny = -dy / n, dx / n
        L.append((x + nx * wd[i], y + ny * wd[i])); R.append((x - nx * wd[i], y - ny * wd[i]))
    k.poly([(70, 160), (44, 190), (64, 182), (72, 196), (82, 182), (104, 186), (76, 160)], C('#c8402a'), .14)   # tail fin
    k.poly([(58, 92), (30, 108), (58, 112)], C('#d8603a'), .1); k.poly([(100, 92), (124, 112), (98, 112)], C('#d8603a'), .1)
    k.poly([(80, 64), (112, 70), (94, 86)], C('#c8402a'), .1)                                                    # dorsal fin
    k.poly([(76, 18)] + L + [(70, 166)] + R[::-1], C('#d2452a'), .16)
    k.poly([(76, 22)] + [(x * .55 + cl[i][0] * .45, y * .55 + cl[i][1] * .45) for i, (x, y) in enumerate(R)] + [(70, 160)], C('#eca45c'), .12, 1)   # belly
    for i in range(1, 5):          # scales
        for j in (-1, 0, 1):
            x, y = cl[i][0] + j * wd[i] * .45, cl[i][1] - 4; k.arc(x, y, 6, 20, 160, C('#8a2618', 170), 1.2)
    k.ell(70, 36, 7, 7, C('#f3e6cc')); k.ell(70, 36, 4.2, 4.2, INK); k.arc(70, 36, 7, 0, 360, GOLD, 1.4); k.ell(68.5, 34.5, 1.3, 1.3, C('#ffffff'))
    k.line([(80, 22), (96, 14), (104, 20)], C('#3a1a10'), 1.2); k.line([(72, 22), (60, 12), (52, 16)], C('#3a1a10'), 1.2)
    return k.finish()


def kite_yakko():
    w, h = 220, 190; k = K(w, h, 31)
    shape = [(6, 64), (214, 64), (214, 122), (156, 122), (150, 132), (176, 186), (44, 186), (70, 132), (64, 122), (6, 122)]
    k.paper(shape, '#2c3a66', '#1a1410')
    k.poly([(8, 66), (212, 66), (212, 76), (8, 76)], C('#b8322a'), .1)            # red sleeve lining
    k.poly([(68, 126), (152, 126), (174, 184), (46, 184)], C('#8a6a3a'), .14)      # hakama
    for x in range(56, 176, 14): k.line([(x + (x - 110) * .1, 132), (x + (x - 110) * .28, 182)], C('#5a4224', 160), 1.6)
    k.poly([(70, 116), (150, 116), (150, 128), (70, 128)], C('#e8dcc0'), .1)      # obi
    k.poly([(100, 114), (120, 114), (120, 130), (100, 130)], C('#b8322a'), .1)
    for cx in (34, 186, 110):                                                      # white mon crests
        cy = 96 if cx != 110 else 96
        k.ell(cx, cy, 13, 13, C('#efe6d2')); k.ell(cx, cy, 8, 8, C('#2c3a66')); k.ell(cx, cy, 3.5, 3.5, C('#efe6d2'))
    k.poly([(98, 62), (110, 76), (122, 62)], C('#efe6d2'), .1)                    # collar
    k.ell(110, 38, 26, 27, C('#f0d2b0'), .08)                                      # face
    k.poly([(84, 34), (88, 12), (110, 6), (132, 12), (136, 34), (124, 22), (96, 22)], INK, .1)   # hair
    k.poly([(104, 2), (116, 2), (118, 10), (102, 10)], INK, .1)                    # topknot
    k.line([(92, 32), (104, 28)], INK, 3.2); k.line([(116, 28), (128, 32)], INK, 3.2)
    k.ell(98, 38, 3, 2.4, INK); k.ell(122, 38, 3, 2.4, INK)
    k.line([(104, 52), (110, 55), (116, 52)], C('#b8322a'), 2.4); k.ell(88, 46, 4, 3, C('#e8a090', 120)); k.ell(132, 46, 4, 3, C('#e8a090', 120))
    k.bones([((10, 70), (210, 70)), ((110, 4), (110, 184))])
    return k.finish()


def kite_tsuru():
    w, h = 170, 170; k = K(w, h, 41); k.paper(rect(w, h), '#e4d4ae')
    k.ell(124, 42, 30, 30, C('#c83a2c'), .12)                                      # the sun
    for cx, cy in ((34, 142), (140, 134)):
        for i in range(3): k.arc(cx, cy, 16 - i * 5, 180, 470, C('#a8843a', 170), 2)
    k.bones(sq_bones(w, h))
    # a crane in flight, wings raised, flying up-left; grey underside, black flight feathers
    LW = [(86, 96), (62, 62), (36, 30), (12, 22), (22, 44), (30, 66), (52, 90), (72, 104)]
    RW = [(98, 92), (116, 58), (140, 26), (162, 18), (154, 44), (146, 70), (126, 92), (106, 104)]
    for W_ in (LW, RW): k.poly([(x + 1.5, y + 1.5) for x, y in W_], C('#6a6458', 120), 0, 1.2)
    k.poly(LW, C('#f4f0e6'), .05); k.poly(RW, C('#f4f0e6'), .05)
    k.poly([(36, 30), (12, 22), (22, 44), (30, 66), (40, 60), (34, 44), (46, 40)], INK, .06)
    k.poly([(140, 26), (162, 18), (154, 44), (146, 70), (136, 64), (142, 46), (130, 40)], INK, .06)
    k.poly([(62, 62), (52, 90), (72, 104), (86, 96)], C('#d8d2c4'), .05); k.poly([(116, 58), (126, 92), (106, 104), (98, 92)], C('#d8d2c4'), .05)
    k.ell(92, 100, 24, 12, C('#f8f4ec'), .04)                                      # body
    k.poly([(108, 100), (134, 118), (126, 108), (140, 110)], INK, .05)              # tail
    k.line([(76, 96), (62, 80), (50, 66)], INK, 5.5)                               # neck
    k.ell(47, 62, 6.5, 5.5, C('#f6f2ea'), .03); k.ell(48, 57.5, 3.5, 2.6, C('#d0302a'), .05)
    k.poly([(42, 60), (26, 58), (42, 65)], C('#8a8070'), .05); k.ell(46, 61, 1.2, 1.2, INK)
    k.line([(112, 106), (142, 128)], INK, 1.6); k.line([(108, 108), (138, 132)], INK, 1.6)
    return k.finish()


def kite_kitsune():
    w, h = 150, 200; k = K(w, h, 51); k.paper(rect(w, h), '#2a2f52')
    k.poly([(6, 6), (144, 6), (144, 14), (6, 14)], GOLD, .1); k.poly([(6, 186), (144, 186), (144, 194), (6, 194)], GOLD, .1)
    k.bones(edo_bones(w, h), (220, 220, 230, 26))
    face = [(34, 30), (60, 70), (90, 70), (116, 30), (122, 92), (126, 118), (98, 146), (82, 176), (68, 176), (52, 146), (24, 118), (28, 92)]
    k.poly(face, C('#f4eee2'), .06)
    k.poly([(38, 40), (56, 70), (44, 74)], C('#c8322c'), .08); k.poly([(112, 40), (94, 70), (106, 74)], C('#c8322c'), .08)
    k.line([(44, 100), (58, 94), (68, 102)], C('#c8322c'), 3.4); k.line([(106, 100), (92, 94), (82, 102)], C('#c8322c'), 3.4)
    k.poly([(48, 104), (66, 100), (60, 108)], C('#e0b040'), .05); k.poly([(102, 104), (84, 100), (90, 108)], C('#e0b040'), .05)
    k.line([(50, 106), (64, 102)], INK, 1.4); k.line([(100, 106), (86, 102)], INK, 1.4)
    k.ell(62, 82, 3.6, 5, C('#c8322c'), .05); k.ell(88, 82, 3.6, 5, C('#c8322c'), .05)
    k.line([(75, 92), (75, 150)], C('#c8322c', 160), 1.6)
    k.ell(75, 168, 7, 5, INK, .05); k.line([(66, 156), (75, 160), (84, 156)], C('#c8322c'), 2)
    for s_ in (-1, 1):
        for i in range(3): k.line([(75 + s_ * 14, 150 + i * 5), (75 + s_ * 34, 146 + i * 7)], C('#8a8070', 150), .9)
    return k.finish()


def kite_musha():
    w, h = 170, 190; k = K(w, h, 61); k.paper(rect(w, h), '#c8562c')
    for i in range(7): k.line([(4, 150 + i * 6), (166, 120 + i * 6)], C('#e8b04a', 90), 3)
    k.bones(sq_bones(w, h), (40, 20, 10, 40))
    k.ell(85, 112, 46, 52, C('#ecc89c'), .08)                                       # face
    k.poly([(30, 80), (36, 44), (60, 28), (110, 28), (134, 44), (140, 80), (126, 70), (44, 70)], C('#26262e'), .12)   # kabuto
    k.poly([(24, 82), (40, 70), (130, 70), (146, 82), (130, 86), (40, 86)], C('#3a3a46'), .1)
    k.poly([(60, 30), (34, 4), (46, 4), (78, 28)], GOLD, .1); k.poly([(110, 30), (136, 4), (124, 4), (92, 28)], GOLD, .1)   # kuwagata
    k.ell(85, 30, 8, 8, C('#b8322a'), .05)
    k.poly([(46, 98), (78, 108), (76, 114), (46, 104)], INK, .05); k.poly([(124, 98), (92, 108), (94, 114), (124, 104)], INK, .05)
    k.ell(62, 118, 9, 6, C('#f6f0e2'), .02); k.ell(108, 118, 9, 6, C('#f6f0e2'), .02); k.ell(66, 118, 3.6, 3.6, INK); k.ell(112, 118, 3.6, 3.6, INK)
    k.line([(48, 126), (60, 134), (56, 148)], C('#b8322a'), 3); k.line([(122, 126), (110, 134), (114, 148)], C('#b8322a'), 3)
    k.line([(85, 112), (80, 138), (90, 140)], C('#7a4a2a'), 2)
    k.poly([(66, 150), (104, 150), (98, 166), (72, 166)], C('#6a1a14'), .05); k.poly([(70, 151), (100, 151), (98, 156), (72, 156)], C('#f3ece0'), .02)
    k.line([(60, 146), (76, 144), (85, 147), (94, 144), (110, 146)], INK, 3.4)
    return k.finish()


def kite_tengu():
    w, h = 150, 200; k = K(w, h, 71); k.paper(rect(w, h), '#1f2c24')
    k.poly([(6, 6), (144, 6), (144, 12), (6, 12)], GOLD, .1); k.poly([(6, 188), (144, 188), (144, 194), (6, 194)], GOLD, .1)
    for i in range(9):            # feather-fan rays behind the head
        a = math.radians(200 + i * 17.5); k.line([(75, 92), (75 + math.cos(a) * 70, 92 + math.sin(a) * 70)], C('#6a7a5a', 120), 5)
    k.bones(edo_bones(w, h), (220, 220, 220, 24))
    k.poly([(30, 150), (75, 192), (120, 150), (100, 140), (50, 140)], C('#ece6da'), .1)   # beard
    k.ell(75, 104, 40, 48, C('#c23a2a'), .12)
    k.poly([(58, 40), (92, 40), (88, 60), (62, 60)], INK, .08)                          # tokin cap
    k.line([(40, 86), (54, 80), (68, 88)], C('#f0ece4'), 6); k.line([(110, 86), (96, 80), (82, 88)], C('#f0ece4'), 6)
    k.ell(57, 98, 6, 4.5, C('#e8c040'), .03); k.ell(93, 98, 6, 4.5, C('#e8c040'), .03); k.ell(58, 98, 2.2, 3, INK); k.ell(92, 98, 2.2, 3, INK)
    k.poly([(68, 104), (82, 104), (132, 150), (128, 158)], C('#d24a34'), .1)           # the long nose
    k.line([(74, 106), (126, 150)], C('#f08a6a', 160), 2)
    k.line([(56, 132), (75, 138), (94, 132)], C('#5a1410'), 2.6)
    return k.finish()


def build_kites():
    K_ = [("ta_kaze", kite_kanji('風', 1)), ("ta_koto", kite_kanji('寿', 2, '#ead9a8', extra=gold_dust)),
          ("ta_koi", kite_koi()), ("ta_yakko", kite_yakko()), ("ta_tsuru", kite_tsuru()), ("ta_kitsune", kite_kitsune()),
          ("ta_ryu", kite_kanji('龍', 3, '#e4e2d6', C('#1a2238'), RED, ryu_clouds)), ("ta_musha", kite_musha()), ("ta_tengu", kite_tengu())]
    # shelf packing, 2 px gaps
    W = 900; x = y = rowh = 0; R = {}; pos = []
    for n, im in K_:
        if x + im.width > W: x = 0; y += rowh + 2; rowh = 0
        R[n] = [x, y, im.width, im.height]; pos.append((im, x, y)); x += im.width + 2; rowh = max(rowh, im.height)
    H = y + rowh; at = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for im, x, y in pos: at.alpha_composite(im, (x, y))
    at.save(os.path.join(ROOT, 'assets/items/atlas_ta.webp'), 'WEBP', quality=88, method=6)
    pv = Image.new('RGBA', (W, H), C('#5a6070')); pv.alpha_composite(at); pv.save(os.path.join(PREV, 'kite_preview.png'))
    print('TA_R =', json.dumps(R, separators=(',', ':')), ' atlas', W, H)


# ── the town strip for the flight scene: 1600×600, transparent sky
def build_strip():
    S2 = 2; W, H = 1600 * S2, 600 * S2; im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); rnd = np.random.default_rng(5); NZ = fbm(W, H, 60, 4, 1)
    def put(mask, col, tex=.12, seed=0, blur=1.0):
        if blur: mask = mask.filter(ImageFilter.GaussianBlur(blur))
        n = np.roll(NZ, (seed * 37) % H, 0) if tex else None
        rgb = np.array(col[:3], np.float32)[None, None] * (1 + ((n[..., None] - .5) * 2 * tex if tex else 0))
        a = np.asarray(mask, np.float32)[..., None] * col[3] / 255
        im.alpha_composite(Image.fromarray(np.concatenate([np.broadcast_to(np.clip(rgb, 0, 255), (H, W, 3)), a], -1).astype(np.uint8), 'RGBA'))
    def P(pts): return [(x * S2, y * S2) for x, y in pts]
    # far ridge in mist
    xs = np.arange(0, 1601, 8); pr = fbm(202, 4, 30, 4, 3)[1]
    ridge = [(x, 300 + 70 * pr[i] - 40 * math.sin(x / 520)) for i, x in enumerate(xs)]
    m = Image.new('L', (W, H)); ImageDraw.Draw(m).polygon(P(ridge + [(1600, 600), (0, 600)]), fill=255); put(m, C('#56607a', 170), .08, 1, 6)
    # a five-storey pagoda far away
    m = Image.new('L', (W, H)); d = ImageDraw.Draw(m); px_, base = 1240, 440
    for i in range(5):
        y0 = base - i * 34; w0 = 46 - i * 6
        d.polygon(P([(px_ - w0, y0), (px_ + w0, y0), (px_ + w0 * .6, y0 - 9), (px_ - w0 * .6, y0 - 9)]), fill=255); d.rectangle(P([(px_ - w0 * .45, y0 - 34), (px_ + w0 * .45, y0)]), fill=255)
    d.rectangle(P([(px_ - 2, base - 210), (px_ + 2, base - 160)]), fill=255); put(m, C('#3e465c', 220), .06, 2, 1.5)
    m = Image.new('L', (W, H)); ImageDraw.Draw(m).rectangle(P([(0, 492), (1600, 600)]), fill=255); put(m, C('#262a26'), .1, 3, 2)
    # kawara roofs: back row lighter (mist), front row darker
    def house(x, w, eave, ground, rows, col_roof, col_wall, seed):
        m = Image.new('L', (W, H)); d = ImageDraw.Draw(m); d.rectangle(P([(x + 6, eave), (x + w - 6, ground)]), fill=255); put(m, col_wall, .1, seed, 1)
        m = Image.new('L', (W, H)); d = ImageDraw.Draw(m)
        for i in range(int(w / 26)):            # warm shoji windows
            wx = x + 16 + i * 26
            if wx + 14 < x + w - 12 and rnd.random() < .55: d.rectangle(P([(wx, eave + 14), (wx + 14, eave + 30)]), fill=255)
        put(m, C('#d9b878', 200), .1, seed + 1, 1)
        rh = rows * 16 + 14
        m = Image.new('L', (W, H)); d = ImageDraw.Draw(m)
        top = [(x - 10 + t * (w + 20), eave - rh + 10 * math.sin(t * math.pi) * 0) for t in np.linspace(0, 1, 2)]
        d.polygon(P([(x - 14, eave + 4), (x + 8, eave - rh + 6), (x + w - 8, eave - rh + 6), (x + w + 14, eave + 4), (x + w / 2, eave - 2)]), fill=255)
        put(m, col_roof, .14, seed + 2, 1)
        m = Image.new('L', (W, H)); d = ImageDraw.Draw(m)
        for tx in range(int(x + 4), int(x + w), 7): d.line(P([(tx, eave - rh + 10), (tx + (tx - x - w / 2) * .12, eave)]), fill=255, width=2)
        put(m, (0, 0, 0, 60), 0, 0, .5)
        m = Image.new('L', (W, H)); ImageDraw.Draw(m).rectangle(P([(x + 4, eave - rh + 2), (x + w - 4, eave - rh + 9)]), fill=255); put(m, (24, 26, 32, 255), .1, seed + 3, .8)
    for i, x in enumerate(range(-40, 1600, 150)):
        w = 130 + rnd.random() * 40; eave = 432 + rnd.random() * 18; house(x + rnd.random() * 30, w, eave, 520, 2, C('#4c5262'), C('#77746a'), 10 + i)
    for i, x in enumerate(range(-90, 1600, 210)):
        w = 170 + rnd.random() * 50; eave = 470 + rnd.random() * 16; house(x + rnd.random() * 40, w, eave, 560, 3, C('#30343e'), C('#8c836e'), 40 + i)
    # trees: a cedar and two pines (their crowns are the snags for the kite)
    trees = []
    def cedar(cx, top, base):
        m = Image.new('L', (W, H)); d = ImageDraw.Draw(m)
        d.rectangle(P([(cx - 7, top + 60), (cx + 7, base)]), fill=255); put(m, C('#3a2a1e'), .2, 70, 1)
        m = Image.new('L', (W, H)); d = ImageDraw.Draw(m); n = 9
        for i in range(n):
            y = top + i * (base - 60 - top) / n; hw = 14 + i * 9
            d.polygon(P([(cx, y - 6), (cx + hw, y + 46), (cx - hw, y + 46)]), fill=255)
        put(m, C('#1e3226'), .25, 71, 1.5); trees.append([cx, top, 14 + n * 9, base - 50])
    def pine(cx, top, base, lean, seed):
        m = Image.new('L', (W, H)); d = ImageDraw.Draw(m); pts = [(cx + lean * (1 - t) ** 2 * 60 - lean * 30 * t, base - (base - top - 30) * t) for t in np.linspace(0, 1, 12)]
        d.line(P(pts), fill=255, width=26, joint='curve'); put(m, C('#3e2c22'), .25, seed, 1)
        m = Image.new('L', (W, H)); d = ImageDraw.Draw(m); pads = []
        for t, s_, hw in ((1.0, 0, 70), (.82, -1, 62), (.7, 1, 66), (.55, -1, 58), (.42, 1, 50)):
            x, y = pts[int(t * 11)]; x += s_ * 40; pads.append((x, y, hw))
            for j in range(5):
                ox, oy, r = (j - 2) * hw * .38 + rnd.random() * 10 - 5, rnd.random() * 10 - (12 if abs(j - 2) < 1 else 2), hw * (.42 if abs(j - 2) < 2 else .32)
                d.ellipse(P([(x + ox - r, y + oy - r * .55), (x + ox + r, y + oy + r * .6)]), fill=255)
            d.line(P([pts[int(t * 11)], (x, y + 6)]), fill=255, width=8)
        put(m, C('#22382a'), .3, seed + 1, 2)
        m = Image.new('L', (W, H)); d = ImageDraw.Draw(m)
        for x, y, hw in pads:
            for j in range(4): r = hw * .26; ox = (j - 1.6) * hw * .4; d.ellipse(P([(x + ox - r, y - 22), (x + ox + r, y - 8)]), fill=255)
        put(m, C('#4a6a44', 150), .3, seed + 2, 3)
        xs_ = [p[0] - p[2] for p in pads] + [p[0] + p[2] for p in pads]; trees.append([round((min(xs_) + max(xs_)) / 2), top - 18, round((max(xs_) - min(xs_)) / 2), base - 120])
    cedar(560, 150, 540); pine(900, 70, 560, 1, 80); pine(1380, 130, 560, -1, 90)
    # the embankment Musya stands on: grass, a footpath
    prof = [(x, 548 + 10 * math.sin(x / 300) + 4 * math.sin(x / 47)) for x in range(0, 1601, 10)]
    m = Image.new('L', (W, H)); ImageDraw.Draw(m).polygon(P(prof + [(1600, 600), (0, 600)]), fill=255); put(m, C('#34422a'), .25, 100, 1)
    m = Image.new('L', (W, H)); d = ImageDraw.Draw(m)
    for _ in range(1400):
        x = rnd.random() * 1600; y0 = 552 + 10 * math.sin(x / 300) + rnd.random() * 46; L = 6 + rnd.random() * 12
        d.line(P([(x, y0), (x + rnd.random() * 6 - 3, y0 - L)]), fill=255, width=2)
    put(m, C('#5e7446', 170), .3, 101, .6)
    m = Image.new('L', (W, H)); ImageDraw.Draw(m).polygon(P([(x, y + 26) for x, y in prof] + [(1600, 600), (0, 600)]), fill=255); put(m, C('#202a1a', 200), .2, 102, 4)
    out = im.resize((1600, 600), Image.LANCZOS)
    a = np.asarray(out, np.float32); n = np.random.default_rng(9).normal(0, 3, a.shape[:2])[..., None]; a[..., :3] = np.clip(a[..., :3] + n, 0, 255)
    out = Image.fromarray(a.astype(np.uint8), 'RGBA'); out.save(os.path.join(ROOT, 'assets/bg/ta_sky.webp'), 'WEBP', quality=86, method=6)
    pv = Image.new('RGBA', out.size, C('#8a9ab4')); pv.alpha_composite(out); pv.convert('RGB').resize((800, 300)).save(os.path.join(PREV, 'kite_strip.png'))
    print('TA_TREES =', json.dumps([[round(v) for v in t] for t in trees]), ' prof y≈548')


if __name__ == '__main__':
    build_kites(); build_strip()
