#!/usr/bin/env python3
"""Food for the kitchen, the fishing pond and the vegetable garden: ingredients, harvest, fish, cooked dishes,
and the garden plants in three growth stages. Same brush toolkit and colour grade as the room things.
Usage: food.py <outdir> → <outdir>/atlas_food.webp + <outdir>/atlas_garden.webp + art/food.json
food.json: {"food": {"w", "h", "r": {id: [x, y, w, h]}}, "garden": {...}}; garden pictures are bottom-centre anchored."""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc, fbm
import items as I
from items import px, canvas, fill, volume, soft, line, ell, poly, text, H, dk, lt, SERIF, SANS, mask_poly
from room_items import clip, cr, blob, plate, WOOD, WOOD_D, WOOD_L

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
S = I.S
IMGS = {'food': [], 'garden': []}


def finish(img, iid, atlas='food', bottom=False, margin=3):
    """Grade like the room things, then crop to the picture (garden: keep the base at the bottom edge, centred)."""
    out = img.resize((P.W, P.H), Image.LANCZOS)
    a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .88
    a[..., :3] += np.random.default_rng(sum(map(ord, iid)) * 7919).normal(0, 3.5, a.shape[:2])[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')
    bb = im.getchannel('A').point(lambda v: 255 if v > 10 else 0).getbbox()
    if bottom:
        cx = P.W / 2; half = max(cx - bb[0], bb[2] - cx) + margin
        box = (int(round(cx - half)), max(0, bb[1] - margin), int(round(cx + half)), P.H)
    else:
        box = (bb[0] - margin, bb[1] - margin, bb[2] + margin, bb[3] + margin)
    im = im.crop(box)
    IMGS[atlas].append((iid, im)); print(atlas, iid, im.size)


def pack():
    meta = {}
    for name, lst in IMGS.items():
        lst = sorted(lst, key=lambda t: -t[1].height); W = 1400; x = y = rowh = 0; pos = {}
        for iid, im in lst:
            if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
            pos[iid] = (x, y); x += im.width + 2; rowh = max(rowh, im.height)
        at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
        for iid, im in lst: at.paste(im, pos[iid])
        at.save(f'{OUT}/atlas_{name}.webp', 'WEBP', quality=88, alpha_quality=92, method=6)
        meta[name] = {'w': W, 'h': y + rowh, 'r': {iid: [pos[iid][0], pos[iid][1], im.width, im.height] for iid, im in lst}}
        print('atlas', name, at.size, len(lst))
    json.dump(meta, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'food.json'), 'w'), indent=0)


# ───────────────────────────── helpers ─────────────────────────────
def rgba(c, a): c = H(c); return (c[0], c[1], c[2], int(a))


def volm(img, m, box, k=.5, rim=.35, spec=0.0):
    """volume() limited to one object's mask, so shading never darkens what lies behind it."""
    x0, y0, x1, y1 = (max(0, px(v)) for v in box); x1 = min(x1, img.width); y1 = min(y1, img.height)
    if x1 <= x0 or y1 <= y0: return
    reg = img.crop((x0, y0, x1, y1)); sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); sh.paste(reg, (x0, y0)); volume(sh, box, k, rim, spec)
    img.paste(sh.crop((x0, y0, x1, y1)), (x0, y0), m.crop((x0, y0, x1, y1)))


def glowdot(img, x, y, r, col, a=160):
    soft(img, lambda d: d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=rgba(col, a)), r * .45)


def bowl(img, cx, rim, w, depth, col, seed, inner='#1a1210', foot='#2a1c14', pattern=None, lacquer=False):
    """Japanese bowl, seen 3/4 from the front: rim ellipse at y=rim, round body below, small foot ring."""
    ry = w * .16
    fill(img, foot, seed + 3, rect=(cx - w * .2, rim + depth * .86, cx + w * .2, rim + depth + 5), scale=3)
    pts = [(cx + w / 2 * math.cos(a), rim + depth * math.sin(a) ** .75) for a in np.linspace(0, math.pi, 40)]
    m = fill(img, col, seed, poly=pts, scale=5, contrast=.8 if lacquer else 1.1)
    if pattern: clip(img, m, pattern)
    volm(img, m, (cx - w / 2, rim - ry, cx + w / 2, rim + depth), .55, .35, spec=.45 if lacquer else .25)
    fill(img, inner, seed + 1, ell=(cx - w / 2, rim - ry, cx + w / 2, rim + ry), scale=4, contrast=.6)
    ImageDraw.Draw(img).ellipse([px(cx - w / 2), px(rim - ry), px(cx + w / 2), px(rim + ry)], outline=lt(H(col), .25), width=px(2))
    return ry


def surface(img, cx, rim, w, ry, col, seed, sink=.18, scale=4, contrast=.8):
    """Liquid or food surface inside a bowl: a slightly smaller ellipse, lowered into the bowl."""
    k = .9; y = rim + ry * sink
    return fill(img, col, seed, ell=(cx - w / 2 * k, y - ry * k, cx + w / 2 * k, y + ry * k), scale=scale, contrast=contrast)


def rice_mound(img, cx, base, w, h, seed, col='#f1eee6'):
    pts = [(cx - w / 2, base), (cx - w * .42, base - h * .55), (cx - w * .2, base - h * .95), (cx + w * .12, base - h), (cx + w * .38, base - h * .6), (cx + w / 2, base)]
    m = blob(img, pts, H(col), seed, scale=2, contrast=.6, k=.45, rim=.25)
    grains(img, m, seed)
    return m


def grains(img, m, seed, n=None, col='#fbf9f2'):
    bb = m.getbbox(); rr = random.Random(seed)
    if not bb: return
    x0, y0, x1, y1 = (v / S for v in bb); n = n or int((x1 - x0) * (y1 - y0) / 14)
    def g(d):
        for _ in range(n):
            x, y = rr.uniform(x0, x1), rr.uniform(y0, y1); a = rr.uniform(0, math.pi); L = 2.3
            c = rr.choice([(255, 255, 250, 230), (200, 196, 184, 170), (236, 232, 222, 200)])
            d.line([(px(x - math.cos(a) * L), px(y - math.sin(a) * L)), (px(x + math.cos(a) * L), px(y + math.sin(a) * L))], fill=c, width=px(1.6))
    clip(img, m, g)


def chopsticks(img, x0, y0, x1, y1, col='#6a3a22', w=4):
    line(img, [(x0, y0), (x1, y1)], dk(H(col), .3), w + 1); line(img, [(x0, y0), (x1, y1)], col, w)
    line(img, [(x0 + 7, y0 + 5), (x1 + 7, y1 + 5)], dk(H(col), .3), w + 1); line(img, [(x0 + 7, y0 + 5), (x1 + 7, y1 + 5)], col, w)


def oval_plate(img, cx, cy, w, h, col='#e9e4d8', rim='#2a4a7a', seed=4):
    fill(img, dk(H(col), .35), seed + 1, ell=(cx - w / 2, cy - h / 2 + 5, cx + w / 2, cy + h / 2 + 5), scale=4, contrast=.5)
    fill(img, col, seed, ell=(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), scale=4, contrast=.5)
    if rim: ImageDraw.Draw(img).ellipse([px(cx - w / 2), px(cy - h / 2), px(cx + w / 2), px(cy + h / 2)], outline=H(rim), width=px(2))
    fill(img, dk(H(col), .08), seed + 2, ell=(cx - w * .36, cy - h * .3, cx + w * .36, cy + h * .3), scale=4, contrast=.4)


def rect_plate(img, x0, y0, x1, y1, col='#2a2622', seed=5, lip='#4a423a'):
    """Long rectangular plate in 3/4 view (top face parallelogram and a front edge)."""
    sk = 10
    fill(img, dk(H(col), .4), seed + 1, poly=[(x0, y1), (x1 - sk, y1), (x1 - sk, y1 + 7), (x0, y1 + 7)], scale=4)
    fill(img, col, seed, poly=[(x0 + sk, y0), (x1, y0), (x1 - sk, y1), (x0, y1)], scale=4, contrast=.6)
    ImageDraw.Draw(img).polygon([(px(x0 + sk), px(y0)), (px(x1), px(y0)), (px(x1 - sk), px(y1)), (px(x0), px(y1))], outline=H(lip), width=px(2))


def leaf_pts(x, y, ang, L, Wd, kind='oval', n=18):
    """Outline of a leaf from its base (x, y) along the angle (0 = up, positive = clockwise)."""
    ax, ay = math.sin(ang), -math.cos(ang); nx, ny = -ay, ax; L_, R_ = [], []
    for i in range(n + 1):
        t = i / n
        if kind == 'heart': wd = Wd * (math.sin(math.pi * min(1, t * 1.15)) ** .7) * (1.15 - .5 * t) if t < .95 else Wd * .05
        elif kind == 'long': wd = Wd * math.sin(math.pi * t) ** 1.4
        elif kind == 'round': wd = Wd * math.sin(math.pi * t) ** .55
        else: wd = Wd * math.sin(math.pi * t) ** .9
        cx_, cy_ = x + ax * L * t, y + ay * L * t
        L_.append((cx_ + nx * wd, cy_ + ny * wd)); R_.append((cx_ - nx * wd, cy_ - ny * wd))
    return L_ + R_[::-1]


def leaf(img, x, y, ang, L, Wd, col, seed, kind='oval', vein=True, serr=0, lobes=0):
    pts = leaf_pts(x, y, ang, L, Wd, kind)
    if serr or lobes:
        rr = random.Random(seed); out = []
        ax, ay = math.sin(ang), -math.cos(ang)
        for i, (qx, qy) in enumerate(pts):
            k = 0
            if serr: k += (serr if i % 2 else -serr * .3)
            if lobes: k += Wd * .22 * math.sin(i / len(pts) * math.pi * 2 * lobes) ** 2
            cx_, cy_ = x + ax * L * .5, y + ay * L * .5; dx, dy = qx - cx_, qy - cy_; dl = math.hypot(dx, dy) + 1e-6
            out.append((qx + dx / dl * k, qy + dy / dl * k))
        pts = out
    m = fill(img, col, seed, poly=pts, scale=4, contrast=1.1)
    xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
    volm(img, m, (min(xs), min(ys), max(xs), max(ys)), .45, .3)
    if vein:
        ax, ay = math.sin(ang), -math.cos(ang)
        line(img, [(x, y), (x + ax * L * .9, y + ay * L * .9)], lt(H(col), .28), max(1, Wd * .09))
        for t in (.3, .5, .7):
            bx, by = x + ax * L * t, y + ay * L * t
            for sg in (-1, 1):
                a2 = ang + sg * .9; line(img, [(bx, by), (bx + math.sin(a2) * Wd * .7, by - math.cos(a2) * Wd * .7)], lt(H(col), .18), max(.6, Wd * .045))
    return m


def stem(img, pts, col, w):
    line(img, pts, dk(H(col), .35), w + 1.2); line(img, pts, col, w)


def ground_dots(img, cx, base, w, seed):
    """A little crumble of soil at the foot, so the plant sits in the bed."""
    rr = random.Random(seed)
    for _ in range(14):
        x = cx + rr.uniform(-w / 2, w / 2); r = rr.uniform(1.5, 3.5)
        ell(img, (x - r, base - r * 1.2, x + r, base), rr.choice(['#2a1e16', '#3a2a1e', '#1e1610']))


# ───────────────────────────── Ингредиенты ─────────────────────────────
def ingredients():
    img = canvas(170, 130); ry = bowl(img, 85, 62, 130, 58, '#2a3a5a', 11, pattern=lambda d: [d.ellipse([px(20 + k * 26), px(80), px(34 + k * 26), px(94)], outline=(220, 220, 230, 150), width=px(2)) for k in range(5)])
    surface(img, 85, 62, 130, ry, '#dcd8cc', 13, sink=-.05); rice_mound(img, 85, 68, 116, 36, 12); finish(img, 'i_rice')

    img = canvas(170, 120)                                                                   # nori
    for k in range(4):
        dx, dy = k * 5, -k * 9
        fill(img, '#1c261c' if k % 2 else '#223022', 20 + k, poly=[(30 + dx, 90 + dy), (130 + dx, 90 + dy), (150 + dx, 60 + dy), (50 + dx, 60 + dy)], scale=3, contrast=1.5)
        line(img, [(30 + dx, 90 + dy), (130 + dx, 90 + dy)], '#3a4a36', 1.2)
    for k in range(4):
        dx, dy = k * 5, -k * 9; line(img, [(50 + dx, 60 + dy), (150 + dx, 60 + dy)], '#56704a', 1.4); line(img, [(130 + dx, 90 + dy), (150 + dx, 60 + dy)], '#46603e', 1.2)
    soft(img, lambda d: d.line([(px(70), px(38)), (px(150), px(36))], fill=(170, 210, 160, 120), width=px(3)), 1.5)
    fill(img, '#e8dcc0', 23, poly=[(76, 94), (98, 94), (124, 56), (102, 56)], scale=2, contrast=.4); text(img, '海苔', 99, 76, 13, '#2a3a2a', SERIF)
    finish(img, 'i_nori')

    img = canvas(160, 120)                                                                   # eggs
    for x, c, sd in ((62, '#e8dcc4', 30), (100, '#c89a6a', 31)):
        m = blob(img, [(x - 26, 70), (x - 18, 40), (x, 28), (x + 18, 40), (x + 26, 70), (x + 16, 96), (x - 16, 96)], H(c), sd, scale=5, contrast=.5, k=.6, rim=.3, spec=.5)
    finish(img, 'i_egg')

    img = canvas(150, 150)                                                                   # mochigome sack
    m = blob(img, [(30, 140), (26, 90), (42, 54), (60, 44), (92, 44), (110, 54), (124, 90), (120, 140)], H('#e2d6bc'), 40, scale=4, contrast=1.1)
    clip(img, m, lambda d: [d.line([(px(30), px(60 + k * 16)), (px(124), px(62 + k * 16))], fill=(160, 140, 110, 70), width=px(1)) for k in range(5)])
    fill(img, '#e9e3d4', 41, ell=(46, 28, 106, 56), scale=2, contrast=.5); grains(img, mask_poly(img, ell=(46, 28, 106, 56)), 42)
    line(img, [(46, 56), (106, 56)], '#8a5a30', 4); line(img, [(98, 56), (112, 74)], '#8a5a30', 2.5)
    text(img, 'もち米', 75, 104, 18, '#6a2a1a', SERIF); finish(img, 'i_mochigome')

    img = canvas(160, 120); ry = bowl(img, 80, 56, 120, 48, '#c8b89a', 50)                  # azuki
    m = surface(img, 80, 56, 120, ry, '#5a1a1c', 51, sink=-.2)
    rr = random.Random(5)
    for _ in range(70):
        x, y = rr.uniform(34, 126), rr.uniform(40, 66)
        if ((x - 80) / 52) ** 2 + ((y - 52) / 15) ** 2 > 1: continue
        ell(img, (x - 4, y - 3, x + 4, y + 3), rr.choice(['#6a1e22', '#4a1216', '#7a2a2a'])); ell(img, (x - 2, y - 2, x, y - 1), '#c87a70')
    finish(img, 'i_azuki')

    img = canvas(150, 150)                                                                   # flour sack
    m = blob(img, [(28, 140), (24, 80), (38, 40), (112, 40), (126, 80), (122, 140)], H('#ece6d8'), 60, scale=4, contrast=.8)
    fill(img, '#f8f6f0', 61, poly=[(38, 42), (60, 22), (90, 18), (112, 42)], scale=2, contrast=.3)
    text(img, '粉', 75, 96, 38, '#2a3a6a', SERIF); line(img, [(36, 50), (114, 50)], '#b8a57a', 3)
    soft(img, lambda d: d.ellipse([px(96), px(128), px(146), px(146)], fill=(250, 248, 240, 200)), 2)
    finish(img, 'i_flour')

    img = canvas(170, 120); oval_plate(img, 85, 88, 150, 44, '#d8d0bc', '#6a4a2a', 70)     # aburaage
    for k, (x, y) in enumerate(((46, 58), (92, 50), (70, 70))):
        m = fill(img, '#c89040', 71 + k, poly=[(x, y), (x + 56, y - 6), (x + 60, y + 18), (x + 4, y + 24)], scale=2, contrast=1.8)
        volm(img, m, (x, y - 6, x + 60, y + 24), .5, .3, spec=.3)
        clip(img, m, lambda d, x=x, y=y: [d.point([(px(x + rr.uniform(4, 56)), px(y + rr.uniform(0, 20))) for _ in range(40)], fill=(240, 200, 120, 200))])
    finish(img, 'i_aburaage')

    img = canvas(150, 150)                                                                   # miso pot
    fill(img, '#6a4a30', 80, poly=[(30, 60), (120, 60), (126, 110), (110, 140), (40, 140), (24, 110)], scale=5, contrast=1.3)
    volume(img, (24, 60, 126, 140), .55, .4, spec=.3)
    fill(img, '#3a2618', 81, ell=(30, 48, 120, 72), scale=3); fill(img, '#9a6a34', 82, ell=(36, 50, 114, 70), scale=2, contrast=1.6)
    line(img, [(80, 60), (132, 18)], WOOD_D, 7); line(img, [(80, 60), (132, 18)], WOOD_L, 5)
    fill(img, WOOD_L, 83, ell=(66, 54, 92, 68), scale=2)
    finish(img, 'i_miso')

    img = canvas(110, 170)                                                                   # shoyu bottle
    fill(img, '#1a0e0c', 90, poly=[(34, 160), (76, 160), (80, 150), (80, 80), (68, 58), (42, 58), (30, 80), (30, 150)], scale=3, contrast=.6)
    volume(img, (30, 58, 80, 160), .5, .3, spec=.7)
    fill(img, '#c02a24', 91, poly=[(40, 58), (70, 58), (68, 36), (60, 28), (50, 28), (42, 36)], scale=2)
    volume(img, (40, 28, 70, 58), .5, .3, spec=.4); poly(img, [(56, 28), (64, 14), (68, 18), (60, 30)], '#c02a24')
    fill(img, '#f0e8d8', 92, rect=(36, 96, 74, 136), scale=2); text(img, '醤油', 55, 116, 15, '#1a1410', SERIF)
    finish(img, 'i_shoyu')

    img = canvas(170, 140)                                                                   # octopus
    for k in range(6):
        a = math.pi * (.15 + .7 * k / 5); x0 = 85 + math.cos(a) * 18; pts = []
        for i in range(12):
            t = i / 11; r = 18 + 48 * t; aa = a + .5 * math.sin(t * 3 + k) * t
            pts.append((85 + math.cos(aa) * r * 1.1, 78 + math.sin(aa) * r * .55 + t * 10))
        line(img, pts, '#8a2a24', 12 - 7 * 0); line(img, pts[:-2], '#c24a3a', 9)
        for q in pts[3::2]: ell(img, (q[0] - 2, q[1] + 1, q[0] + 2, q[1] + 5), '#f0c0a0')
    blob(img, [(56, 82), (54, 46), (70, 24), (100, 24), (116, 46), (114, 82)], H('#c84a3a'), 100, scale=4, contrast=1.1, spec=.4)
    for sx in (-1, 1): ell(img, (85 + sx * 12 - 6, 56, 85 + sx * 12 + 6, 68), '#f4ece0'); ell(img, (85 + sx * 12 - 3, 59, 85 + sx * 12 + 3, 66), '#1a1414')
    ell(img, (80, 70, 90, 78), '#8a2a24')
    finish(img, 'i_tako')

    img = canvas(180, 110)                                                                   # dry noodles
    rr = random.Random(7)
    for k in range(40):
        y = 36 + k * 1.3 + rr.uniform(-1, 1); line(img, [(18, y + 12), (162, y - 8)], rr.choice(['#efe6c8', '#e2d6b0', '#f6f0dc']), 1.6)
    fill(img, '#2a4a8a', 110, poly=[(78, 22), (104, 18), (110, 90), (84, 94)], scale=2); text(img, '麺', 94, 56, 20, '#f0e8d8', SERIF)
    finish(img, 'i_noodles')

    img = canvas(150, 150)                                                                   # sugar jar
    m = fill(img, '#e8e0cc', 120, poly=[(34, 56), (116, 56), (122, 90), (114, 136), (36, 136), (28, 90)], scale=4, contrast=.6); volm(img, m, (28, 50, 122, 136), .55, .4, spec=.35)
    fill(img, '#2a4a7a', 121, rect=(40, 84, 110, 116), scale=2); text(img, '砂糖', 75, 100, 17, '#f4f0e6', SERIF)
    fill(img, '#bfb6a0', 122, ell=(32, 48, 118, 64), scale=2); fill(img, '#faf8f2', 123, ell=(38, 44, 112, 62), scale=2, contrast=.3)
    clip(img, mask_poly(img, ell=(38, 44, 112, 62)), lambda d: [d.point([(px(40 + rr.uniform(0, 72)), px(44 + rr.uniform(0, 18))) for _ in range(120)], fill=(255, 255, 255, 255))])
    m = fill(img, '#d8d0bc', 124, poly=[(96, 44), (140, 22), (146, 32), (104, 52)], scale=2); line(img, [(40, 50), (74, 26)], WOOD_L, 4)
    fill(img, WOOD_L, 125, ell=(30, 44, 52, 56), scale=2)
    finish(img, 'i_sugar')

    img = canvas(190, 130)                                                                   # shrimp: arched back, legs inside the curl
    C = (92, 78); rx, ry = 62, 50
    path = [(C[0] + rx * math.cos(a), C[1] + ry * math.sin(a)) for a in np.linspace(math.pi * 1.93, math.pi * .88, 34)]
    N = len(path) - 1; prof = lambda t: 18 * (1 - .7 * t) + 2
    def nrm(i):
        x, y = path[i]; dx, dy = x - C[0], y - C[1]; dl = math.hypot(dx, dy); return dx / dl, dy / dl      # outward = the back
    outer = [(x + nx * prof(i / N), y + ny * prof(i / N)) for i, (x, y) in enumerate(path) for nx, ny in [nrm(i)]]
    inner = [(x - nx * prof(i / N), y - ny * prof(i / N)) for i, (x, y) in enumerate(path) for nx, ny in [nrm(i)]]
    for i in range(3, 22, 3):
        x, y = inner[i]; nx, ny = nrm(i); line(img, [(x, y), (x - nx * 11 - 2, y - ny * 11 + 2)], '#d8704a', 1.5)
    tx, ty = path[-1]; fx, fy = path[-1][0] - path[-3][0], path[-1][1] - path[-3][1]; fl = math.hypot(fx, fy); fx, fy = fx / fl, fy / fl; nx, ny = -fy, fx
    fill(img, '#d8563a', 139, poly=[(tx - fx * 2, ty - fy * 2), (tx + fx * 22 + nx * 13, ty + fy * 22 + ny * 13), (tx + fx * 14, ty + fy * 14), (tx + fx * 22 - nx * 13, ty + fy * 22 - ny * 13)], scale=2)
    m = fill(img, '#f08a62', 131, poly=outer + inner[::-1], scale=2, contrast=.7)
    for i in range(4, 32, 4): clip(img, m, lambda d, i=i: d.line([(px(outer[i][0]), px(outer[i][1])), (px(inner[i][0]), px(inner[i][1]))], fill=(196, 76, 46, 210), width=px(1.6)))
    clip(img, m, lambda d: d.line([(px(x), px(y)) for x, y in outer[2:30]], fill=(252, 214, 190, 220), width=px(2.2)))
    volm(img, m, bbox(outer + inner), .5, .35, spec=.35)
    hx, hy = path[0]; gx, gy = path[0][0] - path[2][0], path[0][1] - path[2][1]; gl = math.hypot(gx, gy); gx, gy = gx / gl, gy / gl; ux, uy = nrm(0)
    P_ = lambda f, u: (hx + gx * f + ux * u, hy + gy * f + uy * u)
    for k in range(2): line(img, [P_(18, 8), P_(40, 30 + k * 10), P_(10, 58 + k * 6), P_(-40, 56 + k * 4)], '#c8603a', 1.2)
    m = fill(img, '#e06a44', 150, poly=cr([P_(-8, 20), P_(14, 22), P_(26, 10), P_(40, 6), P_(26, 2), P_(18, -16), P_(-6, -20)], 4), scale=2)
    volm(img, m, bbox([P_(-8, 22), P_(40, 6), P_(-6, -20), P_(18, -16)]), .5, .3, spec=.35)
    ex, ey = P_(12, 8); ell(img, (ex - 3.6, ey - 3.6, ex + 3.6, ey + 3.6), '#1a1010'); ell(img, (ex - 1.6, ey - 2.4, ex, ey - .8), '#f0e0d8')
    for k in range(3): x, y = P_(6 - k * 7, -18); line(img, [(x, y), (x - uy * 0 - ux * 10 + gx * 3, y - uy * 10 + gy * 3)], '#d8704a', 1.3)
    finish(img, 'i_ebi')

    img = canvas(180, 120)                                                                   # katsuobushi on kombu
    blob(img, [(10, 90), (40, 70), (90, 78), (140, 64), (172, 84), (150, 104), (90, 100), (40, 108)], H('#2e2a1c'), 140, scale=3, contrast=1.3, spec=.2)
    rr = random.Random(9)
    for _ in range(26):
        x, y = rr.uniform(46, 130), rr.uniform(46, 84); a = rr.uniform(0, 6.28)
        pts = [(x + math.cos(a + t) * rr.uniform(6, 12), y + math.sin(a + t) * rr.uniform(4, 8)) for t in np.linspace(0, 4, 7)]
        poly(img, pts, rr.choice(['#e8b8a0', '#d89878', '#f2d0bc', '#c88a6a']))
    finish(img, 'i_katsuobushi')


# ───────────────────────────── Урожай ─────────────────────────────
def bumpy(img, m, seed, col, n=40):
    bb = m.getbbox(); rr = random.Random(seed)
    if not bb: return
    x0, y0, x1, y1 = (v / S for v in bb)
    clip(img, m, lambda d: [d.ellipse([px(x - 1.6), px(y - 1.6), px(x + 1.6), px(y + 1.6)], fill=rgba(col, 170)) for x, y in [(rr.uniform(x0, x1), rr.uniform(y0, y1)) for _ in range(n)]])


def cucumber(img, x0, y0, x1, y1, w, seed, flower=True):
    ang = math.atan2(y1 - y0, x1 - x0); nx, ny = -math.sin(ang), math.cos(ang); pts, bot = [], []
    for i in range(13):
        t = i / 12; wd = w * (.55 + .45 * math.sin(math.pi * min(1, t * 1.1)) ** .5) * (1 - .15 * t)
        cx_, cy_ = x0 + (x1 - x0) * t + nx * math.sin(t * math.pi) * w * .4, y0 + (y1 - y0) * t + ny * math.sin(t * math.pi) * w * .4
        pts.append((cx_ + nx * wd / 2, cy_ + ny * wd / 2)); bot.append((cx_ - nx * wd / 2, cy_ - ny * wd / 2))
    m = fill(img, '#2f5a26', seed, poly=pts + bot[::-1], scale=3, stretch=(3, 1), contrast=1.4)
    volm(img, m, (min(x0, x1) - w * .6, min(y0, y1) - w * .6, max(x0, x1) + w * .6, max(y0, y1) + w * .6), .5, .3, spec=.3)
    bumpy(img, m, seed, '#a8c878', int(math.hypot(x1 - x0, y1 - y0) * w / 60))
    if flower: ell(img, (x1 - 4, y1 - 4, x1 + 4, y1 + 4), '#e8c030')
    fill(img, '#5a6a2a', seed + 1, ell=(x0 - 4, y0 - 4, x0 + 4, y0 + 4), scale=2)


def spindle(cx0, cy0, cx1, cy1, prof, n=24):
    """Closed outline around the segment (x0,y0)→(x1,y1); prof(t) gives the half-width along it."""
    ang = math.atan2(cy1 - cy0, cx1 - cx0); nx, ny = -math.sin(ang), math.cos(ang); a_, b_ = [], []
    for i in range(n + 1):
        t = i / n; w = prof(t); x, y = cx0 + (cx1 - cx0) * t, cy0 + (cy1 - cy0) * t
        a_.append((x + nx * w, y + ny * w)); b_.append((x - nx * w, y - ny * w))
    return a_ + b_[::-1]


def bbox(pts, pad=0): xs = [q[0] for q in pts]; ys = [q[1] for q in pts]; return (min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)


def eggplant(img, x, y, L, w, seed, ang=0.0):
    """Glossy nasu hanging from its calyx at (x, y); ang = direction of the body (0 = straight down)."""
    x1, y1 = x + math.sin(ang) * L, y + math.cos(ang) * L
    pts = cr(spindle(x, y, x1, y1, lambda t: w * (.42 + .58 * t ** .8) * max(0, 1 - (2 * t - 1) ** 8) ** .5, 20)[::2], 4)
    m = fill(img, '#3a1840', seed, poly=pts, scale=4, contrast=.7)
    volm(img, m, bbox(pts), .7, .4, spec=1.0)
    soft(img, lambda d: d.line([(px(x + math.sin(ang) * L * .35 - 3), px(y + math.cos(ang) * L * .35)), (px(x + math.sin(ang) * L * .7 - w * .4), px(y + math.cos(ang) * L * .7))], fill=(230, 200, 255, 110), width=px(2.5)), 1)
    for k in range(5):
        a = ang + (k - 2) * .55; ex, ey = x + math.sin(a) * L * .26, y + math.cos(a) * L * .24
        poly(img, [(x - 4, y), (x + 4, y), (ex, ey)], '#34502a')
    fill(img, '#46622c', seed + 1, ell=(x - 8, y - 5, x + 8, y + 5), scale=2); line(img, [(x, y - 3), (x - math.sin(ang) * 12, y - math.cos(ang) * 12)], '#56682c', 4)


def pumpkin(img, cx, base, w, h, seed, col='#29432a'):
    """Squat kabocha: dark green rind with paler stripes along the ribs, corky stem."""
    pts = [(cx + w / 2 * math.cos(a), base - h / 2 + h / 2 * math.sin(a) * (1 if math.sin(a) > 0 else .92)) for a in np.linspace(0, 2 * math.pi, 48)]
    m = fill(img, col, seed, poly=pts, scale=4, contrast=1.1)
    for k in range(-3, 4):
        u = k / 3.6; xm = cx + w / 2 * u
        clip(img, m, lambda d, xm=xm, u=u: d.arc([px(xm - w * .06 - abs(u) * w * .1), px(base - h), px(xm + w * .06 + abs(u) * w * .1), px(base)], 250 if u < 0 else 290, 110 if u < 0 else 70, fill=(22, 36, 22, 230), width=px(2.2)))
        clip(img, m, lambda d, xm=xm: d.line([(px(xm + w * .05), px(base - h * .9)), (px(xm + w * .05), px(base - h * .1))], fill=(120, 150, 100, 70), width=px(3)))
    rr = random.Random(seed)
    clip(img, m, lambda d: [d.ellipse([px(x - 1.2), px(y - .8), px(x + 1.2), px(y + .8)], fill=(170, 170, 110, 160)) for x, y in [(cx + rr.uniform(-w * .45, w * .45), base - rr.uniform(h * .1, h * .9)) for _ in range(int(w * h / 180))]])
    volm(img, m, bbox(pts), .6, .45, spec=.35)
    fill(img, '#1e3020', seed + 3, ell=(cx - w * .12, base - h - 2, cx + w * .12, base - h + h * .12), scale=2)
    line(img, [(cx - 1, base - h + 3), (cx + 2, base - h - 10), (cx + 9, base - h - 15)], '#7a6a3a', 7); line(img, [(cx, base - h + 2), (cx + 3, base - h - 9)], '#a8945a', 2.5)


def sweetpotato(img, x0, y0, x1, y1, w, seed):
    pts = cr(spindle(x0, y0, x1, y1, lambda t: w / 2 * math.sin(math.pi * t) ** .55 + 1.5, 20)[::2], 4)
    m = fill(img, '#8a2248', seed, poly=pts, scale=3, stretch=(3, 1), contrast=1.2)
    rr = random.Random(seed)
    clip(img, m, lambda d: [d.arc([px(x - 4), px(y - 2), px(x + 4), px(y + 2)], 20, 160, fill=(50, 10, 26, 170), width=px(1)) for x, y in [(x0 + (x1 - x0) * t + rr.uniform(-4, 4), y0 + (y1 - y0) * t + rr.uniform(-w * .25, w * .25)) for t in (.2, .35, .5, .62, .8)]])
    volm(img, m, bbox(pts), .65, .5, spec=.45)
    line(img, [(x1, y1), (x1 + (x1 - x0) * .06, y1 + (y1 - y0) * .06 + 2)], '#6a3a2a', 1.4); line(img, [(x0, y0), (x0 - (x1 - x0) * .05, y0 - (y1 - y0) * .05)], '#6a3a2a', 1.6)


def edamame_pod(img, x, y, ang, L, seed, col='#7aa844'):
    """Fuzzy soybean pod with three bean bulges; (x, y) is the stalk end, ang the direction (radians, 0 = right)."""
    x1, y1 = x + math.cos(ang) * L, y + math.sin(ang) * L
    wd = L * .2
    prof = lambda t: wd * (.55 + .45 * abs(math.cos(t * math.pi * 3))) * min(1, t * 7, (1 - t) * 5) ** .6
    pts = spindle(x, y, x1, y1, prof, 36)
    m = fill(img, col, seed, poly=pts, scale=2, contrast=.9)
    for k in range(3):
        t = (k + .5) / 3; bx, by = x + (x1 - x) * t, y + (y1 - y) * t
        clip(img, m, lambda d, bx=bx, by=by: d.ellipse([px(bx - wd * .7), px(by - wd * .7), px(bx + wd * .7), px(by + wd * .7)], fill=(170, 210, 110, 90)))
    volm(img, m, bbox(pts, 1), .55, .45, spec=.25)
    rr = random.Random(seed)
    clip(img, m, lambda d: [d.point([(px(qx + rr.uniform(-1, 1)), px(qy + rr.uniform(-1, 1))) for qx, qy in pts for _ in range(2)], fill=(225, 240, 190, 200))])
    line(img, [(x, y), (x - math.cos(ang) * 6, y - math.sin(ang) * 6)], '#5a7a2a', 2)


def strawberry(img, cx, cy, r, seed):
    pts = [(cx - r, cy - r * .5), (cx - r * .7, cy + r * .4), (cx, cy + r * 1.2), (cx + r * .7, cy + r * .4), (cx + r, cy - r * .5), (cx, cy - r * .8)]
    m = blob(img, pts, H('#c8222a'), seed, scale=3, contrast=.8, spec=.6)
    rr = random.Random(seed)
    for _ in range(int(r * 1.4)):
        x, y = cx + rr.uniform(-r * .8, r * .8), cy + rr.uniform(-r * .4, r * 1)
        if ((x - cx) / r) ** 2 + ((y - cy - r * .2) / (r * 1.05)) ** 2 < .8: ell(img, (x - 1, y - 1.4, x + 1, y + 1.4), '#f0d060')
    for k in range(5):
        a = math.pi * (1.1 + k * .2); poly(img, [(cx - 3, cy - r * .6), (cx + 3, cy - r * .6), (cx + math.cos(a) * r * .75, cy - r * .55 + math.sin(a) * r * .3 + r * .2)], '#3a6a26')
    line(img, [(cx, cy - r * .6), (cx + 2, cy - r * 1.1)], '#4a6a2a', 2.4)


def shiitake(img, cx, top, w, seed, col='#6a3e22', stemh=None, tilt=0):
    stemh = stemh if stemh is not None else w * .45
    fill(img, '#e6dcc4', seed + 1, poly=[(cx - w * .12, top + w * .2), (cx + w * .12, top + w * .2), (cx + w * .1 + tilt, top + w * .2 + stemh), (cx - w * .1 + tilt, top + w * .2 + stemh)], scale=2)
    fill(img, '#d8ccb0', seed + 2, ell=(cx - w * .48, top + w * .14, cx + w * .48, top + w * .32), scale=2)
    for k in range(9):
        a = math.pi * k / 8; line(img, [(cx, top + w * .24), (cx + math.cos(a) * w * .46, top + w * .24 + math.sin(a) * w * .06)], '#b8a888', .8)
    m = blob(img, [(cx - w / 2, top + w * .24), (cx - w * .42, top + w * .06), (cx - w * .15, top - w * .06), (cx + w * .15, top - w * .06), (cx + w * .42, top + w * .06), (cx + w / 2, top + w * .24)], H(col), seed, scale=3, contrast=1.1, spec=.25)
    rr = random.Random(seed)
    for _ in range(int(w / 5)):
        x = cx + rr.uniform(-w * .38, w * .38); y = top + rr.uniform(-w * .02, w * .16)
        line(img, [(x - 2, y), (x + rr.uniform(-3, 3), y + 3), (x + 2, y + 1)], '#e8dcc4', 1.1)


def ghost_mushroom(img, cx, base, h, w, seed, eye=False):
    glowdot(img, cx, base - h * .75, w * .75, '#8a7aff', 70)
    fill(img, '#c8c8f0', seed + 1, poly=[(cx - w * .1, base), (cx + w * .1, base), (cx + w * .08, base - h * .7), (cx - w * .06, base - h * .7)], scale=2, contrast=.5)
    m = blob(img, [(cx - w / 2, base - h * .68), (cx - w * .4, base - h * .9), (cx, base - h * 1.05), (cx + w * .4, base - h * .9), (cx + w / 2, base - h * .68), (cx, base - h * .6)], H('#5a4aa8'), seed, scale=3, contrast=1.3, spec=.5)
    rr = random.Random(seed)
    for _ in range(int(w / 3)):
        x = cx + rr.uniform(-w * .38, w * .38); y = base - h * rr.uniform(.72, .98)
        glowdot(img, x, y, 2.4, '#bff4ff', 200); ell(img, (x - 1, y - 1, x + 1, y + 1), '#eaffff')
    if eye:
        ey = base - h * .8
        ell(img, (cx - w * .16, ey - 3.5, cx + w * .16, ey + 3.5), '#f4f0ff'); ell(img, (cx - 3, ey - 3, cx + 3, ey + 3), '#1a0a2a')


def produce():
    img = canvas(200, 90); cucumber(img, 18, 62, 176, 40, 22, 200); cucumber(img, 30, 74, 150, 72, 17, 201); finish(img, 'v_kyuri')

    img = canvas(170, 200)                                                                   # daikon
    for k, a in enumerate((-.7, -.35, 0, .35, .7)):
        leaf(img, 88, 64, a, 60, 13, '#3e6a2e', 210 + k, 'long', serr=1.5)
    m = blob(img, [(66, 64), (110, 64), (106, 110), (96, 160), (88, 196), (80, 160), (70, 110)], H('#eeebe2'), 215, scale=3, contrast=.6, spec=.3)
    clip(img, m, lambda d: d.rectangle([px(60), px(60), px(116), px(82)], fill=(150, 190, 120, 140)))
    for y in (100, 124, 146): line(img, [(76, y), (84, y + 1)], '#b8b4a6', 1)
    finish(img, 'v_daikon')

    img = canvas(170, 120); eggplant(img, 28, 46, 122, 25, 220, ang=1.42); eggplant(img, 40, 78, 104, 21, 221, ang=1.68); finish(img, 'v_nasu')
    img = canvas(170, 130); pumpkin(img, 85, 118, 140, 88, 230); finish(img, 'v_kabocha')
    img = canvas(190, 110); sweetpotato(img, 16, 70, 150, 48, 34, 240); sweetpotato(img, 50, 88, 176, 82, 26, 241); finish(img, 'v_imo')

    img = canvas(170, 120)
    for k, (x, y, a) in enumerate(((30, 46, -.22), (26, 68, -.06), (34, 92, .1), (40, 60, -.4))):
        edamame_pod(img, x, y, a, 104 - k * 6, 250 + k)
    line(img, [(28, 70), (14, 76), (8, 90)], '#5a7a2a', 3); finish(img, 'v_edamame')

    img = canvas(170, 130)
    for k, (x, y, r) in enumerate(((56, 70, 26), (104, 60, 28), (82, 92, 24))): strawberry(img, x, y, r, 260 + k)
    leaf(img, 140, 100, 1.2, 30, 11, '#3a6a26', 263, serr=1.2); finish(img, 'v_ichigo')

    img = canvas(170, 120)
    shiitake(img, 60, 40, 76, 270, stemh=32, tilt=-4); shiitake(img, 112, 34, 70, 271, stemh=38, tilt=4); shiitake(img, 88, 62, 58, 272, '#7a4a2a', stemh=22)
    finish(img, 'v_shiitake')

    img = canvas(200, 90)                                                                    # negi
    for k, dy in enumerate((0, 12, 22)):
        y = 40 + dy
        for rk in range(6): line(img, [(20, y + 4), (6 + rk * 2, y + rk * 3 - 4)], '#d8ccb0', 1)
        fill(img, '#eceadc', 280 + k, poly=[(20, y), (88, y - 2), (88, y + 10), (20, y + 10)], scale=2, contrast=.4)
        fill(img, '#4a8a36', 283 + k, poly=[(86, y - 2), (184 - dy * 2, y - 8 - k * 4), (186 - dy * 2, y - 2 - k * 4), (86, y + 10)], scale=2, stretch=(4, 1), contrast=1.2)
        volm(img, mask_poly(img, poly=[(20, y), (88, y - 2), (184 - dy * 2, y - 8 - k * 4), (186 - dy * 2, y - 2 - k * 4), (88, y + 10), (20, y + 10)]), (20, y - 10, 186, y + 10), .45, .25, spec=.2)
    finish(img, 'v_negi')

    img = canvas(230, 200)
    ghost_mushroom(img, 90, 165, 96, 64, 290); ghost_mushroom(img, 142, 165, 70, 54, 291, eye=True); ghost_mushroom(img, 116, 169, 44, 36, 292)
    finish(img, 'v_obaketake')


# ───────────────────────────── Рыбы ─────────────────────────────
def fish(iid, W, Hh, back, side, belly, *, x0=None, x1=None, hh=None, pk=.55, stalk=5, blunt=.55, kt=1.0, kb=1.1,
         tail='fork', tail_len=None, tail_col=None, dorsal=(.45, .62, .7), anal=(.2, .35, .5), wave=0.0, spots=None,
         scales=0.0, alpha=1.0, eye_r=4.0, eye_col='#141210', mouth=True, barbels=0, glow=None, ribs=False, fin_a=110, post=None):
    img = canvas(W, Hh); SSs = S
    x0 = x0 if x0 is not None else W * .2; x1 = x1 if x1 is not None else W - 6; hh = hh if hh is not None else Hh * .32
    CY = Hh * .5; L = x1 - x0
    def half(x):
        u = (x - x0) / L
        if u < 0 or u > 1: return 0
        if u < pk: return stalk + (hh - stalk) * (u / pk) ** 1.1
        return hh * max(0, 1 - ((u - pk) / (1 - pk)) ** 2.4) ** blunt
    def cy(x): return CY + wave * math.sin((x - x0) / L * math.pi * 2.2)
    tcol = H(tail_col or side)
    # fins behind the body
    fin = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(fin, 'RGBA')
    fc = (*tcol[:3], fin_a); ray = (*[max(0, v - 60) for v in tcol[:3]], fin_a)
    tl = tail_len or L * .28; ty = cy(x0)
    if tail == 'fork': tp = [(x0 + 4, ty - stalk), (x0 - tl, ty - hh * 1.05), (x0 - tl * .55, ty), (x0 - tl, ty + hh * 1.05), (x0 + 4, ty + stalk)]
    elif tail == 'round': tp = [(x0 + 4, ty - stalk)] + [(x0 - tl * math.cos(a) ** .8, ty + hh * .9 * math.sin(a)) for a in np.linspace(-1.4, 1.4, 16)] + [(x0 + 4, ty + stalk)]
    elif tail == 'koi': tp = [(x0 + 4, ty)] + [(x0 - tl + tl * .4 * abs(math.sin(a)) ** 1.5, ty + hh * 1.0 * math.sin(a)) for a in np.linspace(-math.pi / 2, math.pi / 2, 24)]
    elif tail == 'veil':
        tp = [(x0 + 6, ty - stalk)]
        for a in np.linspace(-1.5, 1.5, 30): tp.append((x0 - tl * (.75 + .25 * math.cos(a * 3)), ty + hh * 1.5 * math.sin(a) + 8 * math.sin(a * 5)))
        tp.append((x0 + 6, ty + stalk))
    else: tp = None
    if tp:
        d.polygon([(px(x), px(y)) for x, y in tp], fill=fc)
        for q in tp[1:-1:2]: d.line([(px(x0 + 2), px(ty)), (px(q[0]), px(q[1]))], fill=ray, width=max(1, px(.7)))
    if dorsal:
        a_, b_, hgt = dorsal; xa, xb = x0 + L * a_, x0 + L * b_
        dp = [(xa, cy(xa) - half(xa) * kt + 2), (xa + (xb - xa) * .2, cy(xa) - half(xa) * kt - hh * hgt), (xb, cy(xb) - half(xb) * kt - hh * hgt * .35), (xb, cy(xb) - half(xb) * kt + 2)]
        d.polygon([(px(x), px(y)) for x, y in dp], fill=fc)
        for k in range(6): xx = xa + (xb - xa) * k / 6; d.line([(px(xx), px(cy(xx) - half(xx) * kt)), (px(xx + 4), px(cy(xx) - half(xx) * kt - hh * hgt * (1 - k / 8)))], fill=ray, width=max(1, px(.6)))
    if anal:
        a_, b_, hgt = anal; xa, xb = x0 + L * a_, x0 + L * b_
        ap = [(xa, cy(xa) + half(xa) * kb - 2), (xa + (xb - xa) * .3, cy(xa) + half(xa) * kb + hh * hgt), (xb, cy(xb) + half(xb) * kb + hh * hgt * .4), (xb, cy(xb) + half(xb) * kb - 2)]
        d.polygon([(px(x), px(y)) for x, y in ap], fill=fc)
    img.alpha_composite(fin.filter(ImageFilter.GaussianBlur(S * .5)))
    # body
    pts = [(x, cy(x) - half(x) * kt) for x in np.linspace(x0, x1, 80)] + [(x, cy(x) + half(x) * kb) for x in np.linspace(x1, x0, 80)]
    m = mask_poly(img, poly=pts).filter(ImageFilter.GaussianBlur(S * .5)); a = np.asarray(m, np.float32) / 255
    hS, wS = a.shape; yy, xx = np.mgrid[0:hS, 0:wS] / S
    xs = xx[0]; hw = np.array([half(x) for x in xs])[None, :] + 1e-3; cc = np.array([cy(x) for x in xs])[None, :]
    v = np.clip((yy - cc) / (hw * np.where(yy < cc, kt, kb)), -1, 1)
    bk, sd, bl = (np.array(H(c)[:3], np.float32) for c in (back, side, belly))
    t = (v + 1) / 2
    rgb = np.where((t < .5)[..., None], bk + (sd - bk) * (t / .5)[..., None], sd + (bl - sd) * ((t - .5) / .5)[..., None])
    if spots:
        rr = random.Random(sum(map(ord, iid)))
        sp = Image.new('L', img.size, 0); sd_ = ImageDraw.Draw(sp); spc = np.zeros((hS, wS, 3), np.float32)
        for col, n, (r0, r1), (v0, v1), (u0, u1) in spots:
            layer_ = Image.new('L', img.size, 0); ld = ImageDraw.Draw(layer_)
            for _ in range(n):
                x = x0 + L * rr.uniform(u0, u1); vv = rr.uniform(v0, v1); y = cy(x) + half(x) * vv * (kt if vv < 0 else kb); r = rr.uniform(r0, r1)
                ld.ellipse([px(x - r * 1.3), px(y - r), px(x + r * 1.3), px(y + r)], fill=255)
            k = np.asarray(layer_.filter(ImageFilter.GaussianBlur(S * .6)), np.float32)[..., None] / 255
            rgb = rgb * (1 - k) + np.array(H(col)[:3], np.float32) * k
    if scales:
        g = np.sin(xx * 1.1 + yy * 1.1) * np.sin(xx * 1.1 - yy * 1.1); net = np.clip(1 - np.abs(g) * 5, 0, 1) * (1 - np.abs(v))
        rgb = rgb * (1 - net[..., None] * scales)
    tex = fbm(wS, hS, 3 * S, 3, sum(map(ord, iid)))[..., None]
    shade = (1.12 - .5 * v ** 2)[..., None] * (.93 + .14 * tex)
    shine = np.exp(-((v + .35) / .16) ** 2)[..., None] * ((xx > x0 + L * .2) & (xx < x1 - L * .1))[..., None]
    rgb = np.clip(rgb * shade + 38 * shine, 0, 255)
    body = Image.fromarray(np.dstack([rgb, a * 255 * alpha]).astype(np.uint8), 'RGBA')
    if glow: soft(img, lambda d_: d_.polygon([(px(x), px(y)) for x, y in pts], fill=rgba(glow, 110)), 7)
    img.alpha_composite(body)
    dd = ImageDraw.Draw(img)
    if ribs:
        for k in range(10):
            xx_ = x0 + L * (.2 + .06 * k); c0 = cy(xx_); h_ = half(xx_) * .75
            dd.line([(px(xx_ + 6), px(c0 - h_)), (px(xx_ - 2), px(c0)), (px(xx_ + 6), px(c0 + h_))], fill=(235, 248, 255, 170), width=px(1.2))
        dd.line([(px(x0 - 4), px(cy(x0))), (px(x1 - L * .18), px(cy(x1 - L * .18)))], fill=(240, 250, 255, 200), width=px(1.8))
    # pectoral fin, gill, eye, mouth
    gx = x1 - L * .2
    dd.arc([px(gx - hh * .7), px(cy(gx) - half(gx) * .8), px(gx + hh * .3), px(cy(gx) + half(gx) * .8)], -60, 60, fill=(*[int(c * .55) for c in H(side)[:3]], 200), width=px(1.4))
    pf = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(pf).polygon([(px(gx - 2), px(cy(gx) + half(gx) * .3)), (px(gx - hh * .9), px(cy(gx) + half(gx) * .7)), (px(gx - hh * .6), px(cy(gx) + half(gx) * .2))], fill=(*tcol[:3], 150))
    img.alpha_composite(pf.filter(ImageFilter.GaussianBlur(S * .5)))
    ex = x1 - L * .09; ey = cy(ex) - half(ex) * .25
    if eye_r:
        ell(img, (ex - eye_r - 1, ey - eye_r - 1, ex + eye_r + 1, ey + eye_r + 1), dk(H(side), .4) if eye_col == '#141210' else rgba(eye_col, 120))
        ell(img, (ex - eye_r, ey - eye_r, ex + eye_r, ey + eye_r), eye_col); ell(img, (ex - eye_r * .45, ey - eye_r * .6, ex, ey - eye_r * .1), '#e8e8e8')
    if mouth: dd.line([(px(x1), px(cy(x1) + 1)), (px(x1 - L * .05), px(cy(x1) + half(x1 - L * .05) * .35))], fill=(*[int(c * .4) for c in H(side)[:3]], 220), width=px(1.2))
    for k in range(barbels):
        line(img, [(x1 - 3 - k * 3, cy(x1) + 3), (x1 - 1 - k * 4, cy(x1) + 10), (x1 - 6 - k * 4, cy(x1) + 15)], dk(H(side), .3), 1.4)
    if post: post(img, x0, x1, cy, half, hh)
    finish(img, iid)


def fishes():
    fish('u_ayu', 210, 76, '#4a5a3a', '#a8aa88', '#e8e8dc', hh=17, pk=.5, stalk=4, blunt=.5, dorsal=(.45, .62, .9), anal=(.22, .36, .5),
         spots=[('#e8c84a', 1, (6, 7), (-.1, .1), (.78, .8))], tail_col='#8a8a6a')
    fish('u_yamame', 220, 80, '#3e4a3a', '#b8b2a0', '#f0ece2', hh=19, pk=.52, dorsal=(.45, .6, .8),
         spots=[('#4a3e5a', 9, (5, 7), (-.15, .25), (.15, .85)), ('#1a1a1a', 22, (1, 1.8), (-.9, -.35), (.2, .85)), ('#d8a0a8', 6, (2, 3), (.05, .2), (.2, .8))])
    fish('u_iwana', 230, 84, '#3a4430', '#6a7050', '#e8c890', hh=20, pk=.5, dorsal=(.45, .6, .8), tail='round', tail_len=40,
         spots=[('#e8e4d0', 38, (1.6, 3), (-.9, .4), (.1, .9)), ('#d8904a', 8, (1.5, 2.2), (0, .5), (.2, .85))])
    fish('u_funa', 190, 96, '#5a5238', '#a89868', '#e0d8b8', hh=30, pk=.55, stalk=7, dorsal=(.3, .72, .6), tail='fork', tail_len=46, scales=.35)
    def whiskers(img, x0, x1, cy, half, hh):
        c = cy(x1); col = '#2a2a1c'
        for pts_ in ([(x1 - 3, c - 1), (x1 + 14, c - 12), (x1 + 26, c + 4), (x1 + 16, c + 30), (x1 + 4, c + 42)],
                     [(x1 - 3, c + 3), (x1 + 12, c + 14), (x1 + 12, c + 34), (x1 + 2, c + 46)]):
            line(img, pts_, col, 2.2)
        for k in range(2): line(img, [(x1 - 14 - k * 8, c + half(x1 - 14) * .7), (x1 - 12 - k * 9, c + half(x1 - 14) + 10)], col, 1.4)
        line(img, [(x1 + 1, c + 2), (x1 - L_ * .07, c + 6)], '#141410', 1.6)
    L_ = 200
    fish('u_namazu', 300, 110, '#2e3024', '#5a5a40', '#d8d0b0', x0=52, x1=258, hh=30, pk=.7, stalk=6, blunt=.22, kt=.72, kb=1.0, tail='round', tail_len=46,
         dorsal=(.62, .68, .35), anal=(.05, .58, .32), eye_r=2.4, mouth=False, spots=[('#1e2016', 18, (2, 4.5), (-.9, .1), (.05, .9))], post=whiskers)
    fish('u_unagi', 330, 72, '#22281e', '#465032', '#e0d090', x0=34, hh=13, pk=.3, stalk=3, blunt=.4, wave=6, tail='round', tail_len=24,
         dorsal=(.02, .62, .9), anal=(.0, .5, .9), eye_r=2.4, fin_a=140)
    fish('u_kingyo', 140, 100, '#d8401a', '#f06a24', '#f8c8a0', x0=56, hh=26, pk=.5, stalk=6, blunt=.8, tail='veil', tail_len=54, tail_col='#f07a3a', fin_a=120,
         dorsal=(.35, .7, .8), anal=(.3, .4, .6), eye_r=4.6, spots=[('#f4f0e8', 3, (5, 9), (-.3, .6), (.1, .6))])
    fish('u_kinkoi', 250, 106, '#b8801a', '#e8b83a', '#f6e0a0', hh=28, pk=.55, stalk=7, tail='koi', tail_len=56, dorsal=(.35, .72, .55), scales=.45, barbels=2)
    fish('u_obakeuo', 230, 96, '#8ab8d8', '#b8def0', '#e8f6ff', hh=24, pk=.55, alpha=.6, ribs=True, glow='#8ad8ff', eye_col='#5af0ff', eye_r=4.5,
         tail='fork', tail_col='#bfe8ff', fin_a=70, dorsal=(.4, .6, .6))

    def ningyo_face(img, x0, x1, cy, half, hh):
        fx, fy = x1 - 20, cy(x1) - 4
        tip = x0 + (x1 - x0) * .3; top = [(fx + 8, fy - 28), (fx - 20, fy - 30), (fx - 60, cy(fx - 60) - half(fx - 60) * .95), (fx - 110, cy(fx - 110) - half(fx - 110) * .7), (tip, cy(tip) - half(tip) * .2)]
        low = [(tip + 10, cy(tip) + 6)] + [(fx - 110 + 50 * k / 3 * 2, cy(fx - 110) + 2 + 7 * math.sin(k * 1.9)) for k in range(4)] + [(fx - 20, fy + 20), (fx - 12, fy + 6)]
        m = fill(img, '#16121a', 3, poly=cr(top + low, 5), scale=2, stretch=(4, 1), contrast=1.2)
        rr = random.Random(3)
        clip(img, m, lambda d: [d.line([(px(fx - 6 - k * 3), px(fy - 24 + k * 1.5)), (px(fx - 70 - k * 6), px(fy - 18 + k * 3 + rr.uniform(-3, 3))), (px(tip + rr.uniform(0, 30)), px(cy(tip) + rr.uniform(-10, 6)))], fill=(60, 56, 72, 150), width=px(1), joint='curve') for k in range(12)])

        m = blob(img, [(fx - 18, fy - 6), (fx - 12, fy - 22), (fx + 6, fy - 26), (fx + 20, fy - 12), (fx + 20, fy + 10), (fx + 6, fy + 24), (fx - 12, fy + 18)], H('#ece2d8'), 300, scale=3, contrast=.4, k=.4, rim=.3)
        fill(img, '#141012', 301, poly=[(fx - 16, fy - 10), (fx - 8, fy - 26), (fx + 10, fy - 28), (fx + 22, fy - 12), (fx + 10, fy - 16), (fx - 4, fy - 12)], scale=2)
        for dx in (-3, 11): ell(img, (fx + dx - 3.4, fy - 4, fx + dx + 3.4, fy + 3), '#140e10'); ell(img, (fx + dx - 1.6, fy - 3, fx + dx, fy - 1), '#f0f0f0')
        line(img, [(fx + 1, fy + 11), (fx + 5, fy + 13), (fx + 9, fy + 11)], '#a8222a', 2)
        soft(img, lambda d_: [d_.ellipse([px(fx + dx - 4), px(fy + 4), px(fx + dx + 4), px(fy + 9)], fill=(230, 120, 130, 90)) for dx in (-4, 14)], 1.5)
    fish('u_ningyo', 270, 126, '#2a3a4a', '#6a8a9a', '#dcd8d0', x0=46, x1=236, hh=30, pk=.6, stalk=7, blunt=.9, tail='koi', tail_len=50, tail_col='#8aa0b0',
         dorsal=(.3, .6, .5), eye_r=0, mouth=False, scales=.5, post=ningyo_face)

    img = canvas(180, 130)                                                                   # old geta with weed, lying tilted
    g = Image.new('RGBA', img.size, (0, 0, 0, 0))
    m = fill(g, '#8a6a48', 310, poly=cr([(20, 50), (60, 36), (150, 30), (164, 40), (130, 58), (34, 64)], 4), scale=3, stretch=(4, 1), contrast=1.3); volm(g, m, (16, 28, 166, 66), .4, .3)
    fill(g, '#5a4230', 311, poly=[(34, 64), (130, 58), (164, 40), (164, 50), (130, 68), (34, 74), (22, 58)], scale=3)
    for x in (50, 116): fill(g, '#3a2a1e', 312 + x, poly=[(x - 4, 70), (x + 18, 68), (x + 18, 80), (x - 4, 82)], scale=2, contrast=1.3)
    line(g, [(46, 52), (82, 36), (132, 44)], '#8a1e1a', 5); line(g, [(46, 52), (82, 36), (132, 44)], '#c0342a', 3); ell(g, (77, 31, 87, 41), '#8a1e1a')
    rr = random.Random(4)
    for k, x in enumerate((44, 64, 84, 104, 124)):
        y0 = 72; line(g, [(x, y0), (x + rr.uniform(-4, 4), y0 + 8), (x + rr.uniform(-6, 6), y0 + 13 + rr.uniform(0, 8))], rr.choice(['#3a6a2a', '#4a7a30', '#2e5a26']), 2.4)
    for _ in range(14): x, y = rr.uniform(30, 150), rr.uniform(34, 60); ell(g, (x - 4, y - 2, x + 4, y + 2), rr.choice(['#3a5a2a', '#4a6a30']))
    img.alpha_composite(g.rotate(10, center=(px(90), px(60)), resample=Image.BICUBIC))
    finish(img, 'u_geta')

    img = canvas(170, 90)                                                                    # bottle with a letter
    glass = Image.new('RGBA', img.size, (0, 0, 0, 0))
    fill(glass, '#8ab8a8', 320, poly=[(16, 30), (112, 26), (128, 36), (152, 38), (152, 52), (128, 54), (112, 64), (16, 62)], scale=3, contrast=.5)
    a = np.asarray(glass, np.float32); a[..., 3] *= .55; img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))
    fill(img, '#e8dcb8', 321, poly=[(30, 36), (104, 34), (104, 56), (30, 58)], scale=2); line(img, [(60, 34), (60, 58)], '#c02a24', 2.4)
    for y in (42, 48): line(img, [(36, y), (54, y)], '#6a5a4a', .8)
    fill(img, '#9a6a3a', 322, rect=(150, 38, 162, 52), scale=2)
    soft(img, lambda d_: d_.line([(px(24), px(34)), (px(110), px(30))], fill=(255, 255, 255, 160), width=px(3)), 1)
    finish(img, 'u_bottle')


# ───────────────────────────── Блюда ─────────────────────────────
def onigiri(img, cx, base, w, seed):
    pts = [(cx - w / 2, base), (cx - w * .3, base - w * .5), (cx, base - w * .82), (cx + w * .3, base - w * .5), (cx + w / 2, base)]
    m = blob(img, pts, H('#f2efe8'), seed, scale=2, contrast=.5, k=.4, rim=.2); grains(img, m, seed)
    fill(img, '#18221a', seed + 1, poly=[(cx - w * .24, base + 2), (cx + w * .24, base + 2), (cx + w * .2, base - w * .3), (cx - w * .2, base - w * .3)], scale=2, contrast=1.4)
    line(img, [(cx - w * .2, base - w * .3), (cx + w * .2, base - w * .3)], '#2e3a2c', 1)


def dango_skewer(img, x0, y0, x1, y1, cols, r, seed, glaze=None):
    line(img, [(x0, y0), (x1, y1)], '#c8a868', 3)
    for k, c in enumerate(cols):
        t = .18 + k * .27; x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        blob(img, [(x - r, y), (x - r * .7, y - r * .7), (x, y - r), (x + r * .7, y - r * .7), (x + r, y), (x + r * .7, y + r * .7), (x, y + r), (x - r * .7, y + r * .7)], H(c), seed + k, scale=2, contrast=.4, k=.5, rim=.3, spec=.35)
        if glaze: m_ = fill(img, glaze, seed + 10 + k, ell=(x - r * .9, y - r, x + r * .9, y + r * .1), scale=2, contrast=.5); volm(img, m_, (x - r, y - r, x + r, y), .4, .2, spec=.8)


def dishes():
    img = canvas(170, 120); oval_plate(img, 85, 92, 150, 40, '#d8d0bc', '#6a4a2a', 400)
    leaf(img, 30, 96, 1.35, 120, 18, '#3a6a2a', 401, 'long', vein=True)
    onigiri(img, 62, 96, 58, 402); onigiri(img, 108, 92, 62, 403)
    ell(img, (128, 94, 142, 104), '#a8222a'); finish(img, 'ds_onigiri')

    img = canvas(160, 130); ry = bowl(img, 80, 60, 124, 54, '#5a1410', 410, inner='#240806', lacquer=True)   # miso soup
    m = surface(img, 80, 60, 124, ry, '#8a5a2a', 411, sink=.2, scale=6, contrast=1.4)
    rr = random.Random(2)
    clip(img, m, lambda d: [d.rectangle([px(x), px(y), px(x + 8), px(y + 6)], fill=(242, 236, 220, 255)) for x, y in [(rr.uniform(34, 116), rr.uniform(52, 70)) for _ in range(6)]])
    clip(img, m, lambda d: [d.ellipse([px(x), px(y), px(x + 5), px(y + 3)], fill=(90, 160, 60, 255)) for x, y in [(rr.uniform(30, 124), rr.uniform(50, 72)) for _ in range(14)]])
    clip(img, m, lambda d: [d.polygon([(px(x), px(y)), (px(x + 12), px(y + 2)), (px(x + 6), px(y + 6))], fill=(30, 50, 26, 220)) for x, y in [(rr.uniform(40, 110), rr.uniform(54, 68)) for _ in range(4)]])
    finish(img, 'ds_miso')

    img = canvas(180, 120); rect_plate(img, 16, 66, 170, 104, '#2a2622', 420)                 # tamagoyaki
    for k in range(3):
        x = 38 + k * 40
        fill(img, '#e8b830', 421 + k, poly=[(x, 44), (x + 34, 44), (x + 30, 88), (x - 4, 88)], scale=2, contrast=.6)
        fill(img, '#f4d460', 424 + k, poly=[(x - 4, 88), (x + 30, 88), (x + 30, 94), (x - 4, 94)], scale=2)
        for j in range(3): line(img, [(x + 2 + j * 2, 52 + j * 10), (x + 30 - j * 2, 52 + j * 10)], '#c89020', 1.2)
        volm(img, mask_poly(img, poly=[(x, 44), (x + 34, 44), (x + 30, 94), (x - 4, 94)]), (x - 4, 44, x + 34, 94), .45, .25, spec=.2)
    ell(img, (140, 70, 162, 84), '#e8e4dc'); finish(img, 'ds_tamagoyaki')

    img = canvas(170, 120); oval_plate(img, 85, 94, 150, 34, '#3a2e24', '#1a120c', 430)
    dango_skewer(img, 20, 96, 150, 40, ['#e8a8b8', '#f4f0e6', '#8ab86a'], 17, 431); finish(img, 'ds_dango')

    img = canvas(170, 120); oval_plate(img, 85, 90, 150, 40, '#2a3a5a', '#1a2440', 440)       # mochi
    for k, (x, y) in enumerate(((56, 84), (110, 82), (84, 70))):
        blob(img, [(x - 26, y), (x - 20, y - 16), (x, y - 22), (x + 20, y - 16), (x + 26, y), (x, y + 8)], H('#f4f2ec'), 441 + k, scale=2, contrast=.3, k=.4, rim=.25, spec=.3)
    soft(img, lambda d: [d.point([(px(30 + rr_.uniform(0, 110)), px(52 + rr_.uniform(0, 40))) for _ in range(90)], fill=(255, 255, 255, 220)) for rr_ in [random.Random(4)]], .3)
    finish(img, 'ds_mochi')

    img = canvas(180, 120)                                                                   # takoyaki boat
    fill(img, '#c8b890', 450, poly=[(14, 64), (166, 58), (150, 104), (30, 108)], scale=5, stretch=(4, 1), contrast=.6)
    fill(img, '#e8dcb8', 451, poly=[(22, 60), (160, 56), (150, 70), (30, 74)], scale=4)
    for k, (x, y) in enumerate(((42, 64), (74, 60), (106, 58), (136, 56), (60, 76), (94, 74), (126, 72))):
        blob(img, [(x - 16, y + 4), (x - 12, y - 10), (x, y - 14), (x + 12, y - 10), (x + 16, y + 4), (x, y + 12)], H('#b8762a'), 452 + k, scale=2, contrast=1.2, spec=.2)
        fill(img, '#4a2410', 460 + k, ell=(x - 12, y - 12, x + 12, y - 2), scale=2, contrast=.6)
        line(img, [(x - 10, y - 8), (x - 3, y - 4), (x + 4, y - 9), (x + 10, y - 5)], '#f6f0dc', 1.4)
    rr = random.Random(3)
    for _ in range(40): x, y = rr.uniform(30, 150), rr.uniform(46, 76); ell(img, (x, y, x + 2, y + 2), '#3a6a2a')
    for _ in range(10): x, y = rr.uniform(34, 146), rr.uniform(44, 70); poly(img, [(x, y), (x + 7, y + 2), (x + 3, y + 6)], '#e0a888')
    line(img, [(128, 48), (170, 20)], '#d8c088', 2.5); finish(img, 'ds_takoyaki')

    img = canvas(180, 150); ry = bowl(img, 90, 66, 150, 66, '#1a1a1c', 470, inner='#0e0c0a', pattern=lambda d: [d.arc([px(20 + k * 30), px(84), px(44 + k * 30), px(104)], 180, 360, fill=(170, 40, 30, 200), width=px(2)) for k in range(5)])
    m = surface(img, 90, 66, 150, ry, '#c89a52', 471, sink=.22, scale=6)
    clip(img, m, lambda d: [d.arc([px(30 + k * 5), px(50 + k * 1.2), px(96 + k * 4), px(80 + k)], 200, 330, fill=(240, 220, 150, 255), width=px(1.6)) for k in range(12)])
    clip(img, m, lambda d: d.ellipse([px(98), px(50), px(134), px(70)], fill=(160, 90, 60, 255)))
    clip(img, m, lambda d: [d.ellipse([px(100), px(55), px(130), px(66)], outline=(220, 170, 140, 255), width=px(2))])
    fill(img, '#f4f0e6', 472, ell=(56, 48, 82, 66), scale=2); fill(img, '#f0b830', 473, ell=(62, 52, 76, 62), scale=2)
    fill(img, '#f4efe6', 474, ell=(84, 56, 102, 68), scale=2); ImageDraw.Draw(img).arc([px(87), px(58), px(99), px(66)], 0, 300, fill=H('#e0507a'), width=px(2))
    fill(img, '#18221a', 475, poly=[(128, 40), (150, 36), (146, 66), (126, 66)], scale=2)
    for _ in range(18): x, y = rr.uniform(46, 126), rr.uniform(52, 76); ell(img, (x, y, x + 4, y + 3), '#6aa84a')
    chopsticks(img, 60, 26, 150, 12, '#8a5a30', 3); finish(img, 'ds_ramen')

    img = canvas(180, 120); oval_plate(img, 90, 90, 160, 42, '#2a2622', '#0a0806', 480)      # tempura
    fill(img, '#f0ead8', 481, poly=[(40, 70), (140, 66), (150, 96), (36, 100)], scale=3, contrast=.3)
    for k, (x0, y0, x1, y1) in enumerate(((36, 88, 150, 50), (40, 96, 156, 70))):
        pts = []; bot = []
        for i in range(12):
            t = i / 11; w = 16 * (1 - .4 * t); cx_, cy_ = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t; pts.append((cx_, cy_ - w / 2)); bot.append((cx_, cy_ + w / 2))
        m = fill(img, '#e8b85a', 482 + k, poly=pts + bot[::-1], scale=2, contrast=1.6); volm(img, m, (x0, y1 - 10, x1, y0 + 10), .5, .3, spec=.3)
        clip(img, m, lambda d, s=482 + k: [d.ellipse([px(x - 2), px(y - 2), px(x + 2), px(y + 2)], fill=(250, 220, 150, 220)) for x, y in [(random.Random(s + j).uniform(x0, x1), random.Random(s * 3 + j).uniform(min(y0, y1) - 8, max(y0, y1) + 8)) for j in range(60)]])
        poly(img, [(x1 - 2, y1 - 6), (x1 + 16, y1 - 14), (x1 + 12, y1 + 4), (x1 - 2, y1 + 6)], '#d84a2a')
    fill(img, '#4a7a30', 486, ell=(96, 76, 132, 96), scale=2, contrast=1.3); finish(img, 'ds_tempura')

    img = canvas(200, 120); rect_plate(img, 10, 60, 190, 106, '#e8e2d4', 490, '#4a5a7a')      # grilled fish
    fish_im = Image.new('RGBA', img.size, (0, 0, 0, 0))
    pts = [(40 + x, 80 - 16 * math.sin(math.pi * x / 110) ** .7) for x in range(0, 111, 5)] + [(40 + x, 80 + 12 * math.sin(math.pi * x / 110) ** .7) for x in range(110, -1, -5)]
    m = fill(img, '#b8884a', 491, poly=pts, scale=3, contrast=1.6); volm(img, m, (40, 62, 150, 94), .5, .3, spec=.3)
    clip(img, m, lambda d: [d.line([(px(58 + k * 16), px(66)), (px(66 + k * 16), px(92))], fill=(60, 30, 14, 200), width=px(3)) for k in range(5)])
    poly(img, [(40, 80), (22, 64), (28, 80), (22, 96)], '#8a6030'); ell(img, (136, 72, 142, 78), '#e8e4dc'); ell(img, (138, 73, 141, 76), '#1a1410')
    fill(img, '#f2eee4', 492, ell=(150, 78, 176, 94), scale=2); ell(img, (160, 76, 166, 80), '#e8a080')
    m = fill(img, '#f0d838', 493, poly=[(154 + 16 * math.cos(a), 72 + 12 * math.sin(a)) for a in np.linspace(math.pi, 2 * math.pi, 12)], scale=2)
    line(img, [(138, 72), (170, 72)], '#f8f0c0', 2); finish(img, 'ds_yakizakana')

    img = canvas(170, 120); oval_plate(img, 85, 90, 150, 40, '#2a3a5a', '#1a2440', 500)       # inari
    for k, (x, y) in enumerate(((52, 84), (86, 78), (120, 84))):
        blob(img, [(x - 22, y + 8), (x - 20, y - 12), (x - 4, y - 20), (x + 16, y - 14), (x + 22, y + 6), (x, y + 12)], H('#b87a2a'), 501 + k, scale=2, contrast=1.4, spec=.4)
        fill(img, '#f2eee6', 505 + k, ell=(x - 12, y - 18, x + 10, y - 8), scale=2)
    ell(img, (132, 64, 150, 74), '#e89aa8'); finish(img, 'ds_inari')

    img = canvas(160, 120); ry = bowl(img, 80, 58, 116, 50, '#8a4a2a', 510, inner='#2a1a10')   # asazuke
    rr = random.Random(6)
    for k in range(12):
        x, y = 44 + (k % 6) * 14 + rr.uniform(-2, 2), 46 + (k // 6) * 8 + rr.uniform(-2, 2)
        ell(img, (x - 9, y - 6, x + 9, y + 6), '#2f5a26'); ell(img, (x - 7, y - 4.5, x + 7, y + 4.5), '#c8d8a0')
        for j in range(3): ell(img, (x - 3 + j * 2.5, y - 1, x - 2 + j * 2.5, y), '#8aa060')
    finish(img, 'ds_asazuke')

    img = canvas(160, 130); ry = bowl(img, 80, 62, 124, 52, '#2a2420', 520, inner='#140e0a')   # nimono pumpkin
    for k, (x, y) in enumerate(((52, 52), (82, 44), (108, 54), (68, 64), (98, 66))):
        fill(img, '#2a4a22', 521 + k, poly=[(x - 14, y + 8), (x + 14, y + 8), (x + 12, y + 12), (x - 12, y + 12)], scale=2)
        m = fill(img, '#e89a2a', 526 + k, poly=[(x - 14, y + 8), (x - 10, y - 10), (x + 10, y - 12), (x + 14, y + 8)], scale=2, contrast=.8)
        volm(img, m, (x - 14, y - 12, x + 14, y + 12), .5, .3, spec=.35)
    ell(img, (74, 36, 84, 42), '#6aa84a'); finish(img, 'ds_nimono')

    img = canvas(180, 110)                                                                   # yaki-imo on paper
    fill(img, '#d8c8a0', 530, poly=[(16, 80), (60, 56), (170, 62), (150, 100), (20, 100)], scale=4, contrast=.5)
    sweetpotato(img, 28, 70, 96, 60, 34, 531)
    fill(img, '#f0c040', 532, ell=(86, 44, 110, 76), scale=2, contrast=.6)
    sweetpotato(img, 108, 62, 166, 76, 30, 533); fill(img, '#f6c848', 534, ell=(98, 50, 120, 80), scale=2, contrast=.8)
    soft(img, lambda d: [d.line([(px(90 + k * 14 + 4 * math.sin(t * 7 + k)), px(44 - t * 34)) for t in np.linspace(0, 1, 8)], fill=(240, 240, 240, 60), width=px(1.6), joint='curve') for k in range(3)], 1.2)
    finish(img, 'ds_yakiimo')

    img = canvas(160, 130); ry = bowl(img, 80, 60, 124, 54, '#1a1210', 540, inner='#0e0806', lacquer=True,
                                     pattern=lambda d: [d.ellipse([px(26 + k * 30), px(80), px(40 + k * 30), px(94)], fill=(190, 150, 60, 180)) for k in range(4)])
    m = surface(img, 80, 60, 124, ry, '#d8c8a0', 541, sink=.2, contrast=.4)
    blob(img, [(56, 64), (54, 48), (74, 42), (94, 48), (96, 64), (76, 70)], H('#f4f0e8'), 542, scale=2, contrast=.3, spec=.3)
    for k in range(5): a = k * 1.256; ell(img, (104 + math.cos(a) * 5 - 5, 54 + math.sin(a) * 5 - 5, 104 + math.cos(a) * 5 + 5, 54 + math.sin(a) * 5 + 5), '#e8702a')
    fill(img, '#f4f0ec', 543, poly=[(40, 56), (56, 54), (56, 62), (40, 64)], scale=2); line(img, [(40, 56), (56, 54)], '#e0507a', 2)
    leaf(img, 84, 58, 1.2, 30, 7, '#3a7a2a', 544, 'long', vein=False); finish(img, 'ds_ozoni')

    img = canvas(200, 110); oval_plate(img, 100, 86, 180, 36, '#e8e2d4', '#2a4a7a', 550)     # ehomaki
    m_ = fill(img, '#18221a', 551, poly=[(22, 58), (150, 52), (150, 90), (22, 96)], scale=3, contrast=1.4); volm(img, m_, (22, 52, 170, 96), .5, .3, spec=.25)
    fill(img, '#101812', 552, ell=(136, 50, 172, 92), scale=2); fill(img, '#f2efe6', 553, ell=(140, 54, 168, 88), scale=2)
    for k, (c, dx, dy) in enumerate((('#e8b830', -3, -5), ('#d84a2a', 5, -3), ('#4a8a30', 0, 6), ('#8a5a2a', -6, 5), ('#e89aa8', 6, 7))):
        ell(img, (154 + dx - 4.5, 71 + dy - 4.5, 154 + dx + 4.5, 71 + dy + 4.5), c)
    finish(img, 'ds_ehomaki')

    img = canvas(180, 110)                                                                   # taiyaki
    pts = [(40, 60), (70, 34), (126, 32), (156, 56), (126, 82), (70, 82)]
    blob(img, pts, H('#c8862a'), 560, scale=2, contrast=1.3, spec=.3)
    poly(img, [(44, 58), (16, 34), (24, 58), (16, 84)], '#b8762a'); volm(img, mask_poly(img, poly=[(44, 58), (16, 34), (24, 58), (16, 84)]), (14, 30, 60, 86), .5, .3)
    rr = random.Random(8)
    for k in range(4):
        for j in range(3): x, y = 70 + k * 16, 46 + j * 12; ImageDraw.Draw(img).arc([px(x - 6), px(y - 5), px(x + 6), px(y + 5)], 200, 340, fill=H('#8a5418'), width=px(1.6))
    ell(img, (134, 48, 142, 56), '#6a3a10'); line(img, [(140, 64), (150, 60)], '#6a3a10', 1.6)
    fill(img, '#4a1a1c', 561, poly=[(152, 50), (158, 56), (152, 62)], scale=2); finish(img, 'ds_taiyaki')

    img = canvas(170, 130)                                                                   # unadon in lacquer box
    m_ = fill(img, '#6a1410', 570, poly=[(20, 70), (150, 70), (146, 116), (24, 116)], scale=4, contrast=.6); volm(img, m_, (20, 60, 150, 116), .5, .3, spec=.4)
    fill(img, '#140806', 571, poly=[(28, 54), (148, 54), (150, 70), (20, 70)], scale=3)
    fill(img, '#f2efe6', 572, poly=[(30, 56), (146, 56), (148, 68), (22, 68)], scale=2)
    for k in range(2):
        y = 40 + k * 14
        m_ = fill(img, '#6a3414', 573 + k, poly=[(30, y + 14), (140, y + 8), (144, y + 20), (32, y + 26)], scale=2, contrast=1.6); volm(img, m_, (30, y + 8, 144, y + 26), .5, .3, spec=.7)
        for j in range(6): line(img, [(40 + j * 18, y + 14), (44 + j * 18, y + 24)], '#3a1a0a', 1.4)
    for _ in range(12): x, y = rr.uniform(40, 130), rr.uniform(44, 70); ell(img, (x, y, x + 2, y + 2), '#6a8a3a')
    finish(img, 'ds_unadon')

    img = canvas(180, 110); rect_plate(img, 12, 64, 170, 100, '#2a2622', 580)                  # nasu dengaku
    for k, x in enumerate((30, 96)):
        m_ = fill(img, '#3a1a3e', 581 + k, ell=(x, 48, x + 64, 92), scale=3); volm(img, m_, (x, 48, x + 64, 92), .5, .3, spec=.6)
        fill(img, '#e8d8a0', 583 + k, ell=(x + 4, 50, x + 60, 84), scale=2)
        m_ = fill(img, '#7a3a14', 585 + k, ell=(x + 8, 50, x + 56, 78), scale=2, contrast=1.3); volm(img, m_, (x + 8, 50, x + 56, 78), .4, .2, spec=.7)
        for j in range(8): ell(img, (x + 14 + j * 5, 60 + (j % 3) * 4, x + 16 + j * 5, 61 + (j % 3) * 4), '#f4ecd8')
    finish(img, 'ds_dengaku')

    img = canvas(160, 120); ry = bowl(img, 80, 60, 116, 48, '#e8e2d8', 590, inner='#c8c0b0', pattern=lambda d: [d.line([(px(24 + k * 12), px(66)), (px(24 + k * 12), px(96))], fill=(40, 70, 120, 150), width=px(2)) for k in range(10)])
    for k, (x, y, a) in enumerate(((32, 52, -.2), (52, 42, .3), (40, 62, -.05), (74, 50, .15), (66, 62, -.35), (92, 46, -.3), (84, 60, .2))):
        edamame_pod(img, x, y, a, 46, 591 + k)
    rr = random.Random(12)
    for _ in range(30): x, y = rr.uniform(40, 120), rr.uniform(40, 66); ell(img, (x, y, x + 1.6, y + 1.6), '#ffffff')
    finish(img, 'ds_edamame')

    img = canvas(170, 120); oval_plate(img, 85, 90, 150, 38, '#2a2622', '#0a0806', 600)       # ichigo daifuku
    blob(img, [(34, 86), (32, 64), (48, 48), (72, 46), (86, 62), (86, 86), (60, 94)], H('#f4f0ea'), 601, scale=2, contrast=.3, k=.4, rim=.25, spec=.3)
    blob(img, [(92, 86), (92, 62), (106, 50), (128, 48), (140, 64), (140, 86), (116, 94)], H('#f4f0ea'), 602, scale=2, contrast=.3, k=.4, rim=.25)
    fill(img, '#4a1a1c', 603, ell=(100, 58, 134, 86), scale=2, contrast=1.3)
    strawberry(img, 117, 70, 12, 604)
    fill(img, '#f4f0ea', 605, ell=(94, 50, 104, 90), scale=2)
    finish(img, 'ds_daifuku')


# ───────────────────────────── Огород ─────────────────────────────
def plant_canvas(w, h):
    img = canvas(w + 40, h + 10); return img, (w + 40) / 2, h + 10


def sprout(img, cx, base, h, seed, col='#5a8a3a', kind='round', n=2, stemc=None):
    stem(img, [(cx, base), (cx + 1, base - h * .6)], stemc or dk(H(col), .1), 2.2)
    for k in range(n):
        a = (-1.1 if k % 2 == 0 else 1.1) * (1 + k * .15); leaf(img, cx + 1, base - h * .6, a, h * .55, h * .28 if kind != 'long' else h * .12, col, seed + k, kind)


def trellis(img, cx, base, h, w):
    for x in (cx - w / 2, cx + w / 2):
        line(img, [(x, base), (x + 2, base - h)], '#6a5a3a', 4); line(img, [(x - 1, base), (x + 1, base - h)], '#a8966a', 2)
    for y in (base - h * .35, base - h * .7, base - h * .95):
        line(img, [(cx - w / 2 - 4, y), (cx + w / 2 + 4, y - 3)], '#8a7a5a', 2)
        for x in (cx - w / 2, cx + w / 2): line(img, [(x - 4, y - 3), (x + 4, y + 3)], '#c8b890', 1.4)


def log(img, cx, base, w, h, seed, col='#4a3a2a', dark=False):
    m = fill(img, col, seed, poly=[(cx - w / 2, base - h), (cx + w / 2 - h * .25, base - h), (cx + w / 2 - h * .25, base), (cx - w / 2, base)], scale=3, stretch=(4, 1), contrast=1.6)
    volm(img, m, (cx - w / 2, base - h, cx + w / 2, base), .5, .45)
    fill(img, '#8a6a48' if not dark else '#3a3024', seed + 1, ell=(cx + w / 2 - h * .5, base - h, cx + w / 2, base), scale=2, contrast=.6)
    for r in (.35, .22, .1): ImageDraw.Draw(img).ellipse([px(cx + w / 2 - h * .25 - h * r), px(base - h / 2 - h * r), px(cx + w / 2 - h * .25 + h * r), px(base - h / 2 + h * r)], outline=H('#5a4230' if not dark else '#2a2018'), width=px(1))
    rr = random.Random(seed)
    for _ in range(int(w / 8)):
        x = cx - w / 2 + rr.uniform(4, w - h * .4); line(img, [(x, base - h + 2), (x + rr.uniform(-4, 4), base - 3)], '#241a12' if not dark else '#14100c', 1)
    if dark:
        for _ in range(int(w / 5)): x = cx - w / 2 + rr.uniform(0, w - h * .3); ell(img, (x - 3, base - h - 2, x + 5, base - h + 4), rr.choice(['#2a4a2a', '#3a5a30']))


def garden():
    G = 'garden'
    # ── kyuri: cucumbers climbing a bamboo trellis
    img, cx, b = plant_canvas(70, 60); sprout(img, cx, b, 44, 700, '#6a9a40'); finish(img, 'g_kyuri_1', G, True)
    img, cx, b = plant_canvas(110, 110); trellis(img, cx, b, 100, 70)
    stem(img, [(cx, b), (cx - 10, b - 40), (cx + 12, b - 70), (cx - 6, b - 96)], '#4a7a2a', 3)
    for k, (dx, dy, a) in enumerate(((-12, 40, -1.2), (12, 60, 1.0), (-8, 80, -.9), (6, 96, .6))): leaf(img, cx + dx * .6, b - dy, a, 36, 18, '#3e6e2a', 701 + k, 'heart', lobes=2)
    finish(img, 'g_kyuri_2', G, True)
    img, cx, b = plant_canvas(150, 170); trellis(img, cx, b, 162, 110)
    stem(img, [(cx - 20, b), (cx - 34, b - 50), (cx - 10, b - 96), (cx - 30, b - 140), (cx - 12, b - 160)], '#4a7a2a', 3)
    stem(img, [(cx + 16, b), (cx + 30, b - 60), (cx + 12, b - 110), (cx + 34, b - 150)], '#4a7a2a', 3)
    for k, (dx, dy, a) in enumerate(((-40, 40, -1.3), (-18, 70, -.4), (-38, 110, -1.1), (-14, 150, -.2), (34, 50, 1.2), (20, 100, .6), (38, 140, 1.1))):
        leaf(img, cx + dx, b - dy, a, 42, 22, '#3e6e2a' if k % 2 else '#4a7a30', 710 + k, 'heart', lobes=2)
    cucumber(img, cx - 20, b - 94, cx - 26, b - 30, 13, 720); cucumber(img, cx + 20, b - 128, cx + 14, b - 64, 12, 721); cucumber(img, cx - 2, b - 150, cx + 2, b - 100, 10, 722)
    for x, y in ((cx - 44, b - 130), (cx + 44, b - 80), (cx + 4, b - 50)):
        for k in range(5): a = k * 1.256; ell(img, (x + math.cos(a) * 4 - 4, y + math.sin(a) * 4 - 4, x + math.cos(a) * 4 + 4, y + math.sin(a) * 4 + 4), '#f0c830')
        ell(img, (x - 2, y - 2, x + 2, y + 2), '#c89020')
    finish(img, 'g_kyuri_3', G, True)

    # ── daikon
    img, cx, b = plant_canvas(70, 60); sprout(img, cx, b, 40, 730, '#5a8a3a', 'heart'); finish(img, 'g_daikon_1', G, True)
    img, cx, b = plant_canvas(110, 110)
    for k, a in enumerate((-.9, -.45, -.1, .3, .75)): leaf(img, cx, b - 4, a, 80 + (k % 2) * 16, 14, '#3e6a2e', 731 + k, 'long', serr=2)
    finish(img, 'g_daikon_2', G, True)
    img, cx, b = plant_canvas(150, 170)
    blob(img, [(cx - 17, b + 2), (cx - 19, b - 16), (cx - 8, b - 26), (cx + 8, b - 26), (cx + 19, b - 16), (cx + 17, b + 2)], H('#eeebe2'), 740, scale=2, contrast=.5, spec=.35)
    m = mask_poly(img, poly=[(cx - 20, b - 30), (cx + 20, b - 30), (cx + 20, b - 12), (cx - 20, b - 12)]); clip(img, m, lambda d: d.rectangle([0, 0, img.width, img.height], fill=(150, 190, 110, 120)))
    for k, a in enumerate((-1.05, -.65, -.3, .05, .4, .75, 1.1)): leaf(img, cx + (k - 3) * 2, b - 24, a, 118 + 14 * math.cos(k * 1.7), 17, '#3e6a2e' if k % 2 else '#4a7a34', 742 + k, 'long', serr=3, lobes=3)
    finish(img, 'g_daikon_3', G, True)

    # ── nasu
    img, cx, b = plant_canvas(70, 60); sprout(img, cx, b, 42, 750, '#4a7a3a', 'oval', stemc='#5a2a5a'); finish(img, 'g_nasu_1', G, True)
    img, cx, b = plant_canvas(110, 110); stem(img, [(cx, b), (cx + 2, b - 90)], '#4a2a4a', 4)
    for k, (dy, a) in enumerate(((30, -1.3), (46, 1.2), (66, -1.0), (82, .9), (94, -.2))): leaf(img, cx + 1, b - dy, a, 42, 18, '#3a6a30', 751 + k, 'oval', lobes=1)
    finish(img, 'g_nasu_2', G, True)
    img, cx, b = plant_canvas(150, 170); stem(img, [(cx, b), (cx + 2, b - 150)], '#4a2a4a', 5)
    for x1, y1 in ((cx - 40, b - 110), (cx + 44, b - 96), (cx - 30, b - 60), (cx + 34, b - 140)): stem(img, [(cx + 1, y1 + 30), (x1, y1)], '#4a2a4a', 3)
    for k, (x, y, a) in enumerate(((cx - 40, b - 110, -1.4), (cx + 44, b - 96, 1.3), (cx - 30, b - 60, -1.1), (cx + 34, b - 140, .9), (cx, b - 150, 0), (cx - 20, b - 140, -.6), (cx + 20, b - 40, 1.4))):
        leaf(img, x, y, a, 48, 22, '#3a6a30' if k % 2 else '#446e34', 760 + k, 'oval', lobes=1)
    eggplant(img, cx - 20, b - 96, 48, 14, 770, ang=.2); eggplant(img, cx + 22, b - 84, 54, 15, 771, ang=-.15); eggplant(img, cx + 4, b - 50, 40, 12, 772, ang=.1)
    for k in range(5): a = k * 1.256; ell(img, (cx - 44 + math.cos(a) * 4 - 4, b - 130 + math.sin(a) * 4 - 4, cx - 44 + math.cos(a) * 4 + 4, b - 130 + math.sin(a) * 4 + 4), '#8a5ab8')
    ell(img, (cx - 46, b - 132, cx - 42, b - 128), '#e8d040'); finish(img, 'g_nasu_3', G, True)

    # ── kabocha
    img, cx, b = plant_canvas(70, 60); sprout(img, cx, b, 40, 780, '#5a8a3a', 'round'); finish(img, 'g_kabocha_1', G, True)
    img, cx, b = plant_canvas(110, 110)
    stem(img, [(cx, b), (cx - 30, b - 6), (cx - 50, b - 2)], '#4a7a2a', 3)
    for k, (dx, h, a) in enumerate(((-30, 26, -.9), (4, 44, -.1), (30, 30, .8))):
        stem(img, [(cx + dx * .3, b), (cx + dx, b - h)], '#5a8a30', 2.4); leaf(img, cx + dx, b - h, a, 40, 24, '#3e6e2a' if k % 2 else '#4a7a30', 781 + k, 'heart', lobes=2)
    finish(img, 'g_kabocha_2', G, True)
    img, cx, b = plant_canvas(150, 170)
    stem(img, [(cx - 60, b - 4), (cx - 20, b - 12), (cx + 30, b - 6), (cx + 64, b - 10)], '#4a7a2a', 4)
    for k, (dx, h, a) in enumerate(((-58, 30, -1.1), (-30, 62, -.45), (40, 56, .6), (64, 28, 1.1), (6, 84, .05), (-6, 40, -.2))):
        stem(img, [(cx + dx * .5, b - 6), (cx + dx, b - h)], '#5a8a30', 2.6); leaf(img, cx + dx, b - h, a, 46 + (k % 3) * 6, 28, '#3e6e2a' if k % 2 else '#4a7a30', 790 + k, 'heart', lobes=2)
    pumpkin(img, cx + 8, b, 78, 52, 797)
    ImageDraw.Draw(img).arc([px(cx - 70), px(b - 60), px(cx - 50), px(b - 40)], 90, 400, fill=H('#5a8a2a'), width=px(1.6))
    for k in range(5): a = k * 1.256; x, y = cx - 34, b - 74; poly(img, [(x, y), (x + math.cos(a) * 12 + math.cos(a + .6) * 5, y + math.sin(a) * 12 + math.sin(a + .6) * 5), (x + math.cos(a) * 12, y + math.sin(a) * 12)], '#f0b820')
    finish(img, 'g_kabocha_3', G, True)

    # ── imo (sweet potato vine)
    img, cx, b = plant_canvas(70, 60); sprout(img, cx, b, 40, 800, '#4a7a3a', 'heart', stemc='#6a2a4a'); finish(img, 'g_imo_1', G, True)
    img, cx, b = plant_canvas(110, 110)
    for k, (dx, dy, a) in enumerate(((-30, 20, -1.2), (-8, 44, -.5), (14, 30, .7), (30, 14, 1.3), (0, 64, .1))):
        stem(img, [(cx, b), (cx + dx * .8, b - dy + 10)], '#6a2a4a', 2); leaf(img, cx + dx * .8, b - dy + 10, a, 34, 16, '#3e6a2e' if k % 2 else '#5a6a2e', 801 + k, 'heart')
    finish(img, 'g_imo_2', G, True)
    img, cx, b = plant_canvas(150, 170)
    sweetpotato(img, cx - 34, b - 6, cx + 30, b - 14, 26, 810)
    for k, (dx, dy, a) in enumerate(((-60, 26, -1.3), (-40, 60, -.8), (-14, 88, -.3), (10, 108, .2), (30, 80, .7), (54, 46, 1.2), (66, 20, 1.5), (-4, 40, 0))):
        stem(img, [(cx, b - 8), (cx + dx * .8, b - dy + 12)], '#6a2a4a', 2.4); leaf(img, cx + dx * .8, b - dy + 12, a, 40, 20, '#3e6a2e' if k % 2 else '#5a6a2e', 811 + k, 'heart')
    finish(img, 'g_imo_3', G, True)

    # ── edamame
    img, cx, b = plant_canvas(70, 60); sprout(img, cx, b, 38, 820, '#6a9a40', 'round'); finish(img, 'g_edamame_1', G, True)
    img, cx, b = plant_canvas(110, 110); stem(img, [(cx, b), (cx, b - 80)], '#5a7a2a', 3)
    for k, (dy, a) in enumerate(((36, -1.2), (50, 1.1), (70, -.8), (80, .6))):
        for j in (-.45, 0, .45): leaf(img, cx, b - dy, a + j, 30, 11, '#4a7a30', 821 + k * 3 + int(j * 10), 'oval')
    finish(img, 'g_edamame_2', G, True)
    img, cx, b = plant_canvas(150, 170)
    for sx in (-1, 1): stem(img, [(cx, b), (cx + sx * 20, b - 70), (cx + sx * 10, b - 140)], '#5a7a2a', 3)
    for k, (dx, dy, a) in enumerate(((-34, 60, -1.2), (32, 70, 1.1), (-24, 110, -.8), (24, 120, .7), (-6, 150, -.1), (40, 30, 1.3), (-40, 30, -1.4))):
        for j in (-.45, 0, .45): leaf(img, cx + dx, b - dy, a + j, 34, 13, '#4a7a30' if k % 2 else '#3e6e2a', 830 + k * 5 + int(j * 10), 'oval')
    for k, (x, y, a) in enumerate(((cx - 16, b - 90, 2.8), (cx + 14, b - 96, 3.4), (cx - 8, b - 60, 2.9), (cx + 12, b - 56, 3.3), (cx + 2, b - 120, 3.1))):
        edamame_pod(img, x, y, math.pi / 2 + (a - 3.1) * .9, 32, 860 + k)
    finish(img, 'g_edamame_3', G, True)

    # ── ichigo
    img, cx, b = plant_canvas(70, 60)
    for j in (-.5, 0, .5): stem(img, [(cx, b), (cx + j * 20, b - 26)], '#5a7a2a', 1.6); leaf(img, cx + j * 20, b - 26, j * 1.4, 16, 8, '#3e6e2a', 870 + int(j * 10), 'round', serr=.8)
    finish(img, 'g_ichigo_1', G, True)
    img, cx, b = plant_canvas(110, 110)
    for k, a in enumerate((-1.2, -.5, .15, .7, 1.25)):
        ln = (38, 52, 44, 56, 34)[k]; x1, y1 = cx + math.sin(a) * ln * .9, b - math.cos(a) * ln - 6; stem(img, [(cx, b), (cx + math.sin(a) * ln * .4, b - ln * .6), (x1, y1)], '#5a7a2a', 2)
        for j in (-.5, 0, .5): leaf(img, x1, y1, a + j, 22, 10, '#3e6e2a', 875 + k * 3 + int(j * 10), 'round', serr=1)
    finish(img, 'g_ichigo_2', G, True)
    img, cx, b = plant_canvas(150, 170)
    for k, a in enumerate((-1.3, -.8, -.3, .2, .7, 1.2, -.05)):
        ln = (52, 74, 62, 80, 66, 50, 92)[k]; x1, y1 = cx + math.sin(a) * ln * .85, b - math.cos(a) * ln - 8; stem(img, [(cx, b), (cx + math.sin(a) * ln * .35, b - ln * .6), (x1, y1)], '#5a7a2a', 2.4)
        for j in (-.5, 0, .5): leaf(img, x1, y1, a + j, 28, 13, '#3e6e2a' if k % 2 else '#4a7a30', 890 + k * 3 + int(j * 10), 'round', serr=1.2)
    for k, (x, y) in enumerate(((cx - 40, b - 18), (cx + 34, b - 22), (cx - 8, b - 12), (cx + 60, b - 40))):
        stem(img, [(cx, b - 30), (x, y - 14)], '#6a8a3a', 1.4); strawberry(img, x, y, 12, 910 + k)
    for k in range(5): a = k * 1.256; x, y = cx - 56, b - 50; ell(img, (x + math.cos(a) * 4 - 4, y + math.sin(a) * 4 - 4, x + math.cos(a) * 4 + 4, y + math.sin(a) * 4 + 4), '#f4f0e8')
    ell(img, (cx - 58, b - 52, cx - 54, b - 48), '#e8c040'); finish(img, 'g_ichigo_3', G, True)

    # ── shiitake on a log
    img, cx, b = plant_canvas(70, 60); log(img, cx, b, 70, 26, 920)
    for x in (cx - 18, cx - 2, cx + 12): ell(img, (x - 3, b - 30, x + 3, b - 24), '#8a5a34')
    finish(img, 'g_shiitake_1', G, True)
    img, cx, b = plant_canvas(110, 110); log(img, cx, b, 110, 34, 921)
    for k, (x, w) in enumerate(((cx - 34, 22), (cx - 6, 26), (cx + 22, 18))): shiitake(img, x, b - 46, w, 922 + k, stemh=6)
    finish(img, 'g_shiitake_2', G, True)
    img, cx, b = plant_canvas(150, 170)
    lx0, ly0, lx1, ly1 = cx - 60, b - 22, cx + 52, b - 128; pts = spindle(lx0, ly0, lx1, ly1, lambda t: 15, 8)
    m = fill(img, '#3e3024', 930, poly=pts, scale=3, stretch=(1, 4), contrast=1.6); volm(img, m, bbox(pts), .5, .45)
    fill(img, '#8a6a48', 939, ell=(lx1 - 13, ly1 - 10, lx1 + 13, ly1 + 10), scale=2, contrast=.6)
    for k, t in enumerate((.45, .66, .86)): x, y = lx0 + (lx1 - lx0) * t, ly0 + (ly1 - ly0) * t; shiitake(img, x - 12, y - 16, 24 - k * 2, 940 + k, stemh=3)
    log(img, cx, b, 150, 44, 931)
    for k, (x, y, w) in enumerate(((cx - 50, b - 58, 34), (cx - 14, b - 62, 40), (cx + 26, b - 56, 32), (cx - 32, b - 40, 26), (cx + 8, b - 38, 28), (cx + 44, b - 40, 22))):
        shiitake(img, x, y, w, 932 + k, stemh=4)
    finish(img, 'g_shiitake_3', G, True)

    # ── negi
    img, cx, b = plant_canvas(70, 60)
    for k, dx in enumerate((-8, 0, 8)): line(img, [(cx + dx, b), (cx + dx * 1.6, b - 40 - k * 4)], '#5a9a3a', 3)
    finish(img, 'g_negi_1', G, True)
    img, cx, b = plant_canvas(110, 110)
    for k, dx in enumerate((-18, -6, 6, 18)):
        line(img, [(cx + dx, b), (cx + dx, b - 20)], '#e8e6d8', 7); line(img, [(cx + dx, b - 18), (cx + dx * 1.8, b - 90 - (k % 2) * 8)], '#4a8a36', 5)
        line(img, [(cx + dx - 1, b - 20), (cx + dx * 1.8 - 1, b - 88 - (k % 2) * 8)], '#7ab85a', 1.4)
    finish(img, 'g_negi_2', G, True)
    img, cx, b = plant_canvas(150, 170)
    for k, dx in enumerate((-36, -22, -8, 6, 20, 34)):
        top = b - 140 - (k % 3) * 14
        line(img, [(cx + dx, b), (cx + dx, b - 34)], '#eceadc', 10); line(img, [(cx + dx, b - 30), (cx + dx * 1.5, top)], '#3e7e30', 7)
        line(img, [(cx + dx - 2, b - 30), (cx + dx * 1.5 - 2, top + 2)], '#7ab85a', 1.8)
    x, y = cx + 3, b - 176
    m_ = fill(img, '#e8e6c8', 950, ell=(x - 13, y - 13, x + 13, y + 13), scale=1.5, contrast=1.5); volm(img, m_, (x - 13, y - 13, x + 13, y + 13), .5, .3)
    line(img, [(x, y + 12), (cx + 3, b - 150)], '#3e7e30', 5)
    finish(img, 'g_negi_3', G, True)

    # ── obaketake (ghost mushrooms on a dark log)
    img, cx, b = plant_canvas(70, 60); log(img, cx, b, 70, 26, 960, '#2a2420', dark=True)
    for x in (cx - 16, cx + 4, cx + 14): glowdot(img, x, b - 28, 5, '#8ad8ff', 170); ell(img, (x - 2, b - 30, x + 2, b - 26), '#e8f8ff')
    finish(img, 'g_obaketake_1', G, True)
    img, cx, b = plant_canvas(110, 110); log(img, cx, b, 110, 34, 961, '#2a2420', dark=True)
    for k, (x, h, w) in enumerate(((cx - 28, 30, 22), (cx - 6, 40, 26), (cx + 18, 26, 18))): ghost_mushroom(img, x, b - 30, h, w, 962 + k)
    finish(img, 'g_obaketake_2', G, True)
    img, cx, b = plant_canvas(150, 170); log(img, cx, b, 150, 44, 970, '#2a2420', dark=True)
    for k, (x, h, w, e) in enumerate(((cx - 44, 70, 44, False), (cx - 8, 100, 56, True), (cx + 30, 64, 40, False), (cx + 54, 40, 28, False), (cx - 26, 40, 26, False))):
        ghost_mushroom(img, x, b - 38, h, w, 971 + k, eye=e)
    rr = random.Random(5)
    for _ in range(16): x, y = cx + rr.uniform(-70, 70), b - rr.uniform(60, 160); glowdot(img, x, y, 2.2, '#bff4ff', 190)
    finish(img, 'g_obaketake_3', G, True)

    # ── bed and watering can
    img = canvas(280, 110)
    fill(img, '#1e1610', 980, poly=[(22, 30), (258, 30), (270, 60), (10, 60)], scale=3, contrast=1.3)
    rr = random.Random(7); d = ImageDraw.Draw(img)
    for k in range(4):
        y = 36 + k * 6.5; d.line([(px(20 - k * 2.5), px(y)), (px(260 + k * 2.5), px(y))], fill=(58, 42, 30, 255), width=px(2.4))
    for _ in range(260): x, y = rr.uniform(18, 262), rr.uniform(31, 59); r = rr.uniform(.8, 2.2); d.ellipse([px(x - r), px(y - r * .7), px(x + r), px(y + r * .7)], fill=rr.choice([(20, 14, 10, 255), (70, 52, 38, 255), (46, 34, 24, 255)]))
    for (x0, y0, x1, y1), sd in (((6, 60, 274, 82), 981), ((18, 22, 262, 32), 982)):
        m_ = fill(img, WOOD, sd, rect=(x0, y0, x1, y1), scale=6, stretch=(6, .5), contrast=1.3); volm(img, m_, (x0, y0, x1, y1), .4, .2)
    fill(img, WOOD_D, 983, poly=[(6, 60), (18, 30), (22, 30), (12, 60)], scale=3); fill(img, WOOD_D, 984, poly=[(274, 60), (262, 30), (258, 30), (268, 60)], scale=3)
    for x in (10, 270): fill(img, '#4a3420', 985 + x, rect=(x - 5, 56, x + 5, 88), scale=2)
    finish(img, 'g_bed', G, True)

    img = canvas(140, 110)
    m_ = fill(img, '#4a7a78', 990, poly=[(34, 40), (86, 40), (92, 96), (28, 96)], scale=3, contrast=.8); volm(img, m_, (28, 40, 92, 96), .55, .35, spec=.5)
    fill(img, '#355a58', 991, ell=(32, 34, 88, 46), scale=2)
    line(img, [(88, 80), (130, 36)], '#3a6260', 7); line(img, [(88, 80), (130, 36)], '#5a8a88', 4)
    fill(img, '#c8a050', 992, ell=(122, 26, 138, 44), scale=2); for_ = [ell(img, (126 + i % 3 * 3, 30 + i // 3 * 4, 128 + i % 3 * 3, 32 + i // 3 * 4), '#6a4a20') for i in range(9)]
    ImageDraw.Draw(img).arc([px(30), px(18), px(90), px(62)], 190, 350, fill=H('#2e4a48'), width=px(5))
    ImageDraw.Draw(img).rectangle([px(28), px(84), px(92), px(88)], fill=H('#2e4a48'))
    finish(img, 'g_can', G, True)


rr = random.Random(1)
if __name__ == '__main__':
    ingredients(); produce(); fishes(); dishes(); garden()
    pack()
