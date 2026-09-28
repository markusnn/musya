#!/usr/bin/env python3
"""Painted yōkai sprites for the scary events: faces, long hair, kimono — same painterly toolkit."""
import json, math, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc, fbm, textured_fill, layer, set_size, dab_mass, ragged, PAL_SAKURA

OUT = sys.argv[1]; META = {}
S = P.SS


def canvas(w, h): set_size(w, h); return layer()
def px(v): return int(v * S)


def save(img, name):
    out = img.resize((P.W, P.H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(.55))
    a = np.asarray(out, np.float32); n = np.random.default_rng(len(name)).normal(0, 5, a.shape[:2])[..., None]; a[..., :3] = np.clip(a[..., :3] + n, 0, 255); out = Image.fromarray(a.astype(np.uint8), 'RGBA')
    out.save(f'{OUT}/{name}.webp', 'WEBP', quality=88, alpha_quality=92, method=6)
    META[name] = [P.W, P.H]; print('monster', name, P.W, P.H)


def soft(img, draw_fn, blur):
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); draw_fn(ImageDraw.Draw(l)); img.alpha_composite(l.filter(ImageFilter.GaussianBlur(blur * S)))


def skin_oval(img, cx, cy, rx, ry, base=(214, 210, 200), seed=1, shade=0.5, rot=0):
    """Pale, powdery face/neck with rounded shading."""
    w, h = px(rx * 2.2), px(ry * 2.2)
    yy, xx = np.mgrid[0:h, 0:w]
    u = (xx - w / 2) / (rx * S); v = (yy - h / 2) / (ry * S)
    if rot: c, s_ = math.cos(rot), math.sin(rot); u, v = u * c + v * s_, -u * s_ + v * c
    r = np.sqrt(u ** 2 + v ** 2)
    a = np.clip((1 - r) * 18, 0, 1)
    n = fbm(w, h, 12 * S, 4, seed)
    lum = (1.05 - shade * (0.55 * r ** 2 + 0.25 * (u * .4 + v * .6).clip(0, None))) * (0.95 + 0.08 * n)
    rgb = np.array(base, np.float32)[None, None] * lum[..., None]
    img.alpha_composite(Image.fromarray(np.dstack([rgb.clip(0, 255), a * 255]).astype(np.uint8), 'RGBA'), (px(cx) - w // 2, px(cy) - h // 2))


def eye(img, x, y, w, h, look=(0, 0), wide=1.0, red=0.4, lid=0.0):
    def sock(d): d.ellipse([px(x - w * 0.9), px(y - h * 1.1), px(x + w * 0.9), px(y + h * 1.2)], fill=(70, 50, 55, 150))
    soft(img, sock, 5)
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    d.ellipse([px(x - w / 2), px(y - h / 2 * wide), px(x + w / 2), px(y + h / 2 * wide)], fill=(236, 230, 222, 255))
    ir = h * .42; ix, iy = x + look[0] * w * .25, y + look[1] * h * .2
    d.ellipse([px(ix - ir), px(iy - ir), px(ix + ir), px(iy + ir)], fill=(38, 30, 26, 255))
    d.ellipse([px(ix - ir * .45), px(iy - ir * .45), px(ix + ir * .45), px(iy + ir * .45)], fill=(6, 4, 4, 255))
    d.ellipse([px(ix - ir * .5 + ir * .2), px(iy - ir * .6), px(ix - ir * .1 + ir * .2), px(iy - ir * .25)], fill=(255, 255, 255, 220))
    if red: d.ellipse([px(x - w / 2), px(y - h / 2 * wide), px(x + w / 2), px(y + h / 2 * wide)], outline=(150, 40, 40, int(200 * red)), width=px(1.6))
    if lid: d.rectangle([px(x - w / 2 - 2), px(y - h / 2 * wide - 2), px(x + w / 2 + 2), px(y - h / 2 * wide + h * lid)], fill=(200, 194, 184, 255))
    mask = Image.new('L', img.size, 0); ImageDraw.Draw(mask).ellipse([px(x - w / 2), px(y - h / 2 * wide), px(x + w / 2), px(y + h / 2 * wide)], fill=255)
    l.putalpha(Image.fromarray(np.minimum(np.asarray(l.getchannel('A')), np.asarray(mask))))
    img.alpha_composite(l.filter(ImageFilter.GaussianBlur(.4 * S)))


def hair(img, roots, length, count, seed, sway=0.3, col=(10, 9, 10), width=(2, 4), spread=1.0, gravity=1.0):
    """Long straight black hair: hundreds of slightly wavy strands falling from root points."""
    rnd = random.Random(seed); d = ImageDraw.Draw(img, 'RGBA')
    for i in range(count):
        rx, ry, ang = rnd.choice(roots)
        L = length * rnd.uniform(.6, 1.0); x, y = rx + rnd.uniform(-6, 6), ry + rnd.uniform(-4, 4)
        a = ang + rnd.uniform(-.15, .15) * spread; pts = [(px(x), px(y))]
        ph = rnd.uniform(0, 6)
        for k in range(1, 26):
            u = k / 25; a2 = a * (1 - u * gravity) + math.sin(u * 5 + ph) * sway * .15
            x += math.sin(a2) * L / 25; y += math.cos(a2) * L / 25; pts.append((px(x), px(y)))
        g = rnd.randint(0, 22); c = (col[0] + g, col[1] + g, col[2] + g, rnd.randint(170, 255))
        d.line(pts, fill=c, width=max(1, int(rnd.uniform(*width) * S)))


def kimono(img, pts, base, seed, obi=None, flowers=0):
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).polygon([(px(x), px(y)) for x, y in pts], fill=255)
    box = m.getbbox(); sub = m.crop(box)
    t = textured_fill(sub, base, mixc(base, (0, 0, 0, 255), .6), mixc(base, (255, 255, 255, 255), .12), 30 * S, seed, (1, 3), 1.2)
    a = np.asarray(t, np.float32); xs = np.linspace(-1, 1, a.shape[1])[None, :]; a[..., :3] *= (1 - .45 * xs ** 2)[..., None]
    img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'), box[:2])
    d = ImageDraw.Draw(img, 'RGBA'); rnd = random.Random(seed)
    for _ in range(9):  # folds
        x0 = rnd.uniform(box[0], box[2]) / S; d.line([(px(x0), px(box[1] / S + 140)), (px(x0 + rnd.uniform(-20, 20)), box[3] - px(10))], fill=(0, 0, 0, 60), width=px(3))
    if obi:
        oy0, oy1, oc = obi; d.rectangle([box[0] + px(18), px(oy0), box[2] - px(18), px(oy1)], fill=oc)
        d.rectangle([box[0] + px(18), px(oy0 + (oy1 - oy0) * .45), box[2] - px(18), px(oy0 + (oy1 - oy0) * .55)], fill=mixc(oc, (200, 170, 90, 255), .45))
    blobs = []
    for _ in range(flowers):
        fx = rnd.uniform(box[0], box[2]); fy = rnd.uniform(box[1] + px(260), box[3])
        if m.getpixel((int(fx), int(fy))) > 0: blobs.append((fx, fy, px(22), px(14)))
    if blobs: dab_mass(d, blobs, 60 * len(blobs), 'leaf', [hexc('#6a5a3a'), hexc('#9a8a5a'), hexc('#c8b890'), hexc('#8a3a3a')], rnd, size=(3, 6))


# ───────────── 1. Ohaguro-bettari: geisha without a face, only a huge mouth ─────────────
def bettari(open_mouth):
    img = canvas(460, 960)
    kimono(img, [(120, 330), (340, 330), (400, 520), (430, 960), (30, 960), (60, 520)], hexc('#7a1c1a'), 3, obi=(640, 740, hexc('#171414')), flowers=10)
    d = ImageDraw.Draw(img, 'RGBA')
    d.polygon([(px(200), px(330)), (px(230), px(420)), (px(260), px(330))], fill=(215, 205, 190, 255))    # collar
    d.line([(px(190), px(330)), (px(230), px(430)), (px(270), px(330))], fill=(180, 170, 150, 255), width=px(5))
    skin_oval(img, 230, 305, 30, 60, seed=4)                                                             # neck
    # geisha hair: wide black wings with comb teeth and dangling kanzashi
    for sgn in (-1, 1):
        l = Image.new('RGBA', img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(l)
        ld.ellipse([px(230 + sgn * 40 - 95), px(95), px(230 + sgn * 40 + 95), px(275)], fill=(12, 11, 12, 255))
        for k in range(18):
            a = math.pi * (0.15 + 0.7 * k / 17); ld.line([(px(230 + sgn * 40), px(185)), (px(230 + sgn * 40 + sgn * math.sin(a) * 120), px(185 - math.cos(a) * 100))], fill=(40, 38, 40, 200), width=px(2))
        img.alpha_composite(l)
    d.ellipse([px(165), px(40), px(295), px(150)], fill=(10, 9, 10, 255))
    hair(img, [(230 + sx, 120, 0) for sx in range(-80, 81, 20)], 60, 120, 5, width=(1, 2))
    for x in (120, 150, 310, 340):
        d.line([(px(x), px(230)), (px(x + 4), px(330))], fill=(210, 190, 140, 200), width=px(1.4))
        d.ellipse([px(x), px(328), px(x + 8), px(336)], fill=(230, 210, 150, 220))
    d.line([(px(240), px(90)), (px(400), px(60))], fill=(210, 200, 170, 255), width=px(3))
    rnd = random.Random(2); d2 = ImageDraw.Draw(img)
    P.dab_mass(d2, [(px(150), px(80), px(40), px(24))], 160, 'leaf', PAL_SAKURA[2:], rnd, size=(4, 7))
    # the face: smooth, featureless egg
    skin_oval(img, 230, 205, 66, 88, base=(226, 224, 216), seed=6, shade=.45)
    if open_mouth:
        l = Image.new('RGBA', img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(l)
        ld.ellipse([px(158), px(170), px(302), px(318)], fill=(96, 14, 18, 255))          # lips
        ld.ellipse([px(168), px(186), px(292), px(308)], fill=(150, 60, 66, 255))         # gums
        ld.ellipse([px(182), px(208), px(278), px(300)], fill=(12, 1, 2, 255))            # throat
        rnd = random.Random(7)
        for y0, dy, n in ((196, 1, 12), (300, -1, 10)):
            for i in range(n):
                u = (i + .5) / n; x = 176 + 108 * u; hh = (26 if y0 < 250 else 20) * math.sin(math.pi * u) ** .6 * rnd.uniform(.7, 1.2) + 6
                col = (26, 22, 20, 255) if rnd.random() < .7 else (214, 204, 184, 255)
                ld.polygon([(px(x - 5.5), px(y0)), (px(x + 5.5), px(y0)), (px(x + rnd.uniform(-2, 2)), px(y0 + dy * hh))], fill=col)
        ld.ellipse([px(206), px(262), px(262), px(330)], fill=(176, 66, 78, 255)); ld.line([(px(234), px(268)), (px(234), px(322))], fill=(120, 30, 40, 255), width=px(2))
        ld.line([(px(196), px(300)), (px(194), px(350))], fill=(200, 200, 205, 150), width=px(2))   # drool
        img.alpha_composite(l.filter(ImageFilter.GaussianBlur(.5 * S)))
        soft(img, lambda dd: dd.ellipse([px(150), px(162), px(310), px(326)], outline=(70, 20, 22, 170), width=px(8)), 4)
    else:
        soft(img, lambda dd: dd.line([(px(200), px(262)), (px(262), px(262))], fill=(120, 60, 60, 120), width=px(3)), 2)
    save(img, 'm_bettari_open' if open_mouth else 'm_bettari')


# ───────────── 2. Rokurokubi head (the neck is drawn live) ─────────────
def rokuro_head():
    img = canvas(260, 300)
    d = ImageDraw.Draw(img); d.ellipse([px(40), px(20), px(220), px(170)], fill=(12, 11, 12, 255))
    d.ellipse([px(80), px(0), px(180), px(70)], fill=(12, 11, 12, 255))
    skin_oval(img, 130, 150, 70, 92, seed=11)
    fr = Image.new('RGBA', img.size, (0, 0, 0, 0)); hair(fr, [(130 + x, 62, x / 160) for x in range(-70, 71, 6)], 62, 160, 12, width=(1, 2), gravity=.6, sway=.4); img.alpha_composite(fr.filter(ImageFilter.GaussianBlur(.8 * S)))
    hair(img, [(62, 120, -.2), (198, 120, .2)], 150, 70, 13, width=(1, 2.5))
    eye(img, 104, 140, 30, 14, look=(.9, .2), wide=.85, red=.6, lid=.25)
    eye(img, 158, 140, 30, 14, look=(.9, .2), wide=.85, red=.6, lid=.25)
    soft(img, lambda dd: [dd.ellipse([px(80), px(150), px(128), px(172)], fill=(60, 50, 60, 90)), dd.ellipse([px(134), px(150), px(182), px(172)], fill=(60, 50, 60, 90))], 5)
    soft(img, lambda dd: dd.polygon([(px(126), px(160)), (px(134), px(160)), (px(138), px(186)), (px(122), px(186))], fill=(150, 120, 110, 110)), 3)
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(l)
    ld.arc([px(96), px(176), px(168), px(214)], 20, 160, fill=(110, 18, 24, 255), width=px(4)); ld.ellipse([px(124), px(204), px(140), px(212)], fill=(110, 18, 24, 255))
    img.alpha_composite(l.filter(ImageFilter.GaussianBlur(.5 * S)))
    d.line([(px(150), px(40)), (px(240), px(20))], fill=(200, 190, 160, 255), width=px(3))
    save(img, 'm_rokuro')


# ───────────── 3. Onryō standing with her back turned ─────────────
def onryo_back():
    img = canvas(320, 860)
    kimono(img, [(110, 200), (210, 200), (250, 420), (262, 800), (58, 800), (70, 420)], hexc('#d8d4c8'), 21)
    skin_oval(img, 96, 520, 16, 140, base=(205, 200, 190), seed=22); skin_oval(img, 224, 520, 16, 140, base=(205, 200, 190), seed=23)
    skin_oval(img, 125, 820, 12, 50, base=(190, 186, 176), seed=24); skin_oval(img, 195, 820, 12, 50, base=(190, 186, 176), seed=25)
    d = ImageDraw.Draw(img); d.ellipse([px(100), px(40), px(220), px(190)], fill=(10, 9, 10, 255))
    hair(img, [(160 + x, 70 + abs(x) * .4, 0) for x in range(-60, 61, 6)], 560, 700, 26, sway=.2, width=(1.5, 3.5), gravity=.1)
    save(img, 'm_onryo')


# ───────────── 4. Head peeking upside-down from under a door ─────────────
def peek_head():
    img = canvas(420, 300)
    # hair fans out across the floor from the crown (the head is upside down: crown at the bottom)
    rnd = random.Random(31); d = ImageDraw.Draw(img, 'RGBA')
    for i in range(520):
        a0 = rnd.uniform(-1.45, 1.45); L = rnd.uniform(80, 200); x, y = 210 + math.sin(a0) * 70, 190 + math.cos(a0) * 30
        pts = [(px(x), px(y))]; ph = rnd.uniform(0, 6)
        for k in range(1, 18):
            u = k / 17; ang = a0 * (1 + .6 * u) + math.sin(u * 4 + ph) * .12
            x += math.sin(ang) * L / 17; y += (math.cos(ang) * .25 + .05) * L / 17; pts.append((px(x), px(min(y, 292))))
        g = rnd.randint(0, 20); d.line(pts, fill=(10 + g, 9 + g, 10 + g, rnd.randint(170, 255)), width=max(1, int(rnd.uniform(1.5, 3) * S)))
    skin_oval(img, 210, 118, 92, 80, seed=32, shade=.65)
    cap = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(cap).chord([px(118), px(122), px(302), px(214)], 0, 180, fill=(12, 11, 12, 255)); img.alpha_composite(cap.filter(ImageFilter.GaussianBlur(3 * S)))
    hair(img, [(210 + x, 150, 0) for x in range(-80, 81, 8)], 40, 160, 33, gravity=.3, width=(1, 2))
    eye(img, 168, 102, 42, 22, look=(.5, -.7), wide=1.2, red=.9)
    eye(img, 252, 102, 42, 22, look=(.5, -.7), wide=1.2, red=.9)
    soft(img, lambda dd: dd.polygon([(px(204), px(74)), (px(216), px(74)), (px(224), px(96)), (px(196), px(96))], fill=(150, 110, 104, 140)), 3)
    soft(img, lambda dd: dd.chord([px(186), px(40), px(234), px(62)], 180, 360, fill=(110, 36, 40, 220)), 1.5)
    save(img, 'm_peek')


# ───────────── 5. Ōkubi: an enormous floating face ─────────────
def okubi():
    img = canvas(760, 660)
    d = ImageDraw.Draw(img); d.ellipse([px(90), px(20), px(670), px(520)], fill=(14, 13, 14, 255))
    skin_oval(img, 380, 350, 250, 290, base=(222, 216, 204), seed=41, shade=.5)
    d.chord([px(118), px(40), px(642), px(330)], 180, 360, fill=(14, 13, 14, 255))
    d.rectangle([px(130), px(150), px(630), px(190)], fill=(14, 13, 14, 255))
    for ex in (290, 470):
        soft(img, lambda dd, ex=ex: dd.ellipse([px(ex - 60), px(270), px(ex + 60), px(330)], fill=(90, 70, 75, 120)), 8)
        l = Image.new('RGBA', img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(l)
        ld.chord([px(ex - 46), px(282), px(ex + 46), px(330)], 180, 360, fill=(22, 16, 16, 255))
        ld.ellipse([px(ex - 12), px(290), px(ex + 4), px(304)], fill=(230, 225, 215, 200))
        img.alpha_composite(l.filter(ImageFilter.GaussianBlur(.8 * S)))
        soft(img, lambda dd, ex=ex: dd.arc([px(ex - 50), px(300), px(ex + 50), px(360)], 200, 340, fill=(120, 90, 90, 120), width=px(4)), 3)
    soft(img, lambda dd: [dd.ellipse([px(180), px(360), px(290), px(440)], fill=(210, 140, 140, 70)), dd.ellipse([px(470), px(360), px(580), px(440)], fill=(210, 140, 140, 70))], 12)
    soft(img, lambda dd: dd.polygon([(px(370), px(330)), (px(390), px(330)), (px(412), px(412)), (px(348), px(412))], fill=(150, 118, 110, 130)), 6)
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(l); rnd = random.Random(44)
    ld.chord([px(220), px(360), px(540), px(540)], 0, 180, fill=(70, 14, 18, 255))
    ld.chord([px(236), px(372), px(524), px(470)], 0, 180, fill=(170, 80, 86, 255))
    for i in range(13):
        u = (i + .5) / 13; x = 244 + 272 * u; top = 452 - 30 * math.sin(math.pi * u) ** 1.5; w = rnd.uniform(8, 11)
        ld.rounded_rectangle([px(x - w), px(top), px(x + w), px(top + rnd.uniform(26, 36))], px(3), fill=tuple(int(c * k) for c, k in zip((236, 228, 206), [rnd.uniform(.78, 1)] * 3)) + (255,))
    for i in range(11):
        u = (i + .5) / 11; x = 262 + 236 * u; bot = 506 + 8 * math.sin(math.pi * u); w = rnd.uniform(7, 10)
        ld.rounded_rectangle([px(x - w), px(bot - rnd.uniform(18, 26)), px(x + w), px(bot)], px(3), fill=tuple(int(c * k) for c, k in zip((224, 214, 190), [rnd.uniform(.75, 1)] * 3)) + (255,))
    img.alpha_composite(l.filter(ImageFilter.GaussianBlur(.7 * S)))
    soft(img, lambda dd: dd.arc([px(214), px(340), px(546), px(548)], 5, 175, fill=(100, 40, 44, 180), width=px(7)), 3)
    save(img, 'm_okubi')


# ───────────── 6. Close-up: a face veiled by hair, one eye ─────────────
def onryo_face():
    img = canvas(800, 800)
    d = ImageDraw.Draw(img); d.rectangle([0, 0, px(800), px(800)], fill=(3, 3, 4, 0))
    skin_oval(img, 430, 520, 190, 250, base=(206, 202, 194), seed=51, shade=.6)
    skin_oval(img, 400, 820, 260, 130, base=(196, 192, 184), seed=52, shade=.6)
    eye(img, 488, 470, 70, 30, look=(-.7, .1), wide=1.2, red=1.0)
    soft(img, lambda dd: dd.chord([px(420), px(620), px(520), px(660)], 0, 180, fill=(90, 50, 55, 200)), 2)
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); hair(l, [(420 + x, 180, .05 * x / 60) for x in range(-220, 221, 8)], 700, 1300, 53, sway=.35, width=(1.5, 4), gravity=.05)
    hair(l, [(300 + x, 200, .1) for x in range(-40, 160, 8)], 650, 360, 54, sway=.3, width=(2, 4))
    a = np.asarray(l, np.float32); cut = np.ones(a.shape[:2], np.float32)
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]; gap = ((xx - px(480)) / px(70)) ** 2 + ((yy - px(520)) / px(170)) ** 2; cut = np.clip((gap - .55) * 2.2, 0, 1) * .9 + .1
    cut[((xx - px(488)) ** 2 / px(52) ** 2 + (yy - px(470)) ** 2 / px(28) ** 2) < 1] = 0   # a clear gap for the eye
    a[..., 3] *= cut; img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))
    save(img, 'm_onryo_face')


if __name__ == '__main__':
    for f in (lambda: bettari(False), lambda: bettari(True), rokuro_head, onryo_back, peek_head, okubi, onryo_face):
        f()
    json.dump(META, open(f'{OUT}/monsters.json', 'w'))
