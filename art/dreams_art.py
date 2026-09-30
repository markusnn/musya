#!/usr/bin/env python3
"""«Сны Муси»: Baku the dream-eater, twelve things that exist only in dreams, and one sprite sheet for the dream worlds
(paper lantern-fish, the moon with its rabbit, cloud steps, glass wind-bells, a bamboo-leaf boat, a torii and a shrine roof,
Musya's thought bubble). Same organic spline toolkit as story_art.py / guests_art.py and the item brushes of items.py.
Usage: cd art && python3 dreams_art.py ../assets
  → ../assets/mon/m_dr_baku.webp, ../assets/items/atlas_dr.webp, ../assets/bg/dr_sprites.webp; rect maps printed as JSON
    (and written to art/out/dreams.json) — they are embedded in feat/dreams.js."""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc, textured_fill
import monsters as M
from monsters import px
from story_art import cr, shape, clipped, poly_s
import items as I
from items import fill, volume, floor_shadow, text, SERIF, dk, lt, H

ROOT = sys.argv[1] if len(sys.argv) > 1 else '../assets'
M.OUT = ROOT + '/mon'
BLACK, WHITE = (0, 0, 0, 255), (255, 255, 255, 255)
S = P.SS


def canvas(w, h): P.set_size(w, h); return P.layer()


def soft(img, fn, blur):
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(l)); img.alpha_composite(l.filter(ImageFilter.GaussianBlur(max(.1, blur * S))))


def stroke(img, pts, col, w, n=8, closed=False):
    ImageDraw.Draw(img).line([(px(x), px(y)) for x, y in cr(pts, n, closed)], fill=H(col), width=max(1, px(w)), joint='curve')


def tube(center, w0, w1):
    L, R = [], []; n = len(center)
    for i, (x, y) in enumerate(center):
        x0, y0 = center[max(0, i - 1)]; x1, y1 = center[min(n - 1, i + 1)]
        a = math.atan2(y1 - y0, x1 - x0) + math.pi / 2; w = w0 + (w1 - w0) * i / (n - 1)
        L.append((x + math.cos(a) * w, y + math.sin(a) * w)); R.append((x - math.cos(a) * w, y - math.sin(a) * w))
    ex, ey = center[-1]; qx, qy = center[-2]; a = math.atan2(ey - qy, ex - qx)
    return L + [(ex + math.cos(a) * w1, ey + math.sin(a) * w1)] + R[::-1]


def glowdot(img, cx, cy, r, col, a=160):
    """Additive-looking soft light: a blurred disc painted over."""
    soft(img, lambda d: d.ellipse([px(cx - r), px(cy - r), px(cx + r), px(cy + r)], fill=H(col)[:3] + (a,)), r * .45)


def curl(img, cx, cy, r, col, turns=1.6, w=2.0, ccw=False):
    """A painted spiral curl — the mane and flame tufts of Edo carvings."""
    pts = []
    for i in range(40):
        u = i / 39; a = u * turns * math.tau * (-1 if ccw else 1); rr = r * (1 - u * .85)
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    ImageDraw.Draw(img).line([(px(x), px(y)) for x, y in pts], fill=H(col), width=max(1, px(w)), joint='curve')


def finish_arr(img, seed, sat=.9, noise=3.5):
    out = img.resize((P.W, P.H), Image.LANCZOS)
    a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * sat
    a[..., :3] += np.random.default_rng(seed).normal(0, noise, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


# ───────────────────────────── shared dream shapes ─────────────────────────────
def lantern_fish(img, cx, cy, rx, ry, body, belly, seed, fin=None, spots=None, cap=True):
    """A kingyo-chōchin: a goldfish-shaped paper lantern with bamboo ribs, lit from inside. Faces left."""
    body, belly = H(body), H(belly); fin = H(fin) if fin else lt(body, .25)
    # tail: two paper fins with ribs, fluttering
    for sd, sk in ((-1, seed + 1), (1, seed + 2)):
        tail = [(cx + rx * .78, cy + sd * ry * .08), (cx + rx * 1.25, cy + sd * ry * .55), (cx + rx * 1.62, cy + sd * ry * 1.02), (cx + rx * 1.7, cy + sd * ry * .62), (cx + rx * 1.42, cy + sd * ry * .12)]
        m = shape(img, fin, sk, tail, scale=5, contrast=.7, dk=.3, lt=.25, k=.3, rim=.2, feather=.9)
        clipped(img, m, lambda d, l, s=sd: [d.line([(px(cx + rx * .85), px(cy)), (px(cx + rx * (1.3 + k * .1)), px(cy + s * ry * (.25 + k * .2)))], fill=dk(fin, .35)[:3] + (120,), width=px(1.2)) for k in range(4)])
    # dorsal fin and a small pectoral fin
    m = shape(img, fin, seed + 3, [(cx - rx * .15, cy - ry * .9), (cx + rx * .1, cy - ry * 1.32), (cx + rx * .42, cy - ry * 1.18), (cx + rx * .5, cy - ry * .8)], scale=4, contrast=.7, k=.3, rim=.2)
    clipped(img, m, lambda d, l: [d.line([(px(cx + rx * (-.1 + k * .14)), px(cy - ry * .85)), (px(cx + rx * (.02 + k * .16)), px(cy - ry * 1.25))], fill=dk(fin, .35)[:3] + (110,), width=px(1)) for k in range(4)])
    # body
    mb = shape(img, body, seed + 4, ell=(cx - rx, cy - ry, cx + rx, cy + ry), scale=6, contrast=.8, dk=.35, lt=.3, k=.55, rim=.45, spec=.18)
    clipped(img, mb, lambda d, l: d.ellipse([px(cx - rx * .95), px(cy + ry * .05), px(cx + rx * .7), px(cy + ry * 1.25)], fill=belly), .92)
    if spots:
        rr = random.Random(seed)
        clipped(img, mb, lambda d, l: [d.ellipse([px(x - r), px(y - r * .8), px(x + r), px(y + r * .8)], fill=H(spots)) for x, y, r in [(cx + rr.uniform(-.5, .6) * rx, cy + rr.uniform(-.75, .1) * ry, rr.uniform(.12, .22) * rx) for _ in range(5)]], .9)
    # inner light: the candle glows through the paper
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(l).ellipse([px(cx - rx * .6), px(cy - ry * .45), px(cx + rx * .5), px(cy + ry * .6)], fill=(255, 226, 160, 150))
    l = l.filter(ImageFilter.GaussianBlur(ry * .45 * S)); a = np.asarray(l, np.float32); a[..., 3] *= np.asarray(mb, np.float32) / 255; img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))
    # bamboo ribs: rings around the body seen from the side
    def ribs(d, l):
        for u in (.2, .42, .62, .8, .94):
            for s0, s1 in ((-90, 90), (90, 270)):
                d.arc([px(cx - rx * u), px(cy - ry), px(cx + rx * u), px(cy + ry)], s0, s1, fill=(60, 20, 10, 70), width=px(1.1))
    clipped(img, mb, ribs)
    # eye and mouth
    ex, ey = cx - rx * .6, cy - ry * .2; er = ry * .22
    ImageDraw.Draw(img).ellipse([px(ex - er), px(ey - er), px(ex + er), px(ey + er)], fill=(246, 238, 220, 255))
    ImageDraw.Draw(img).ellipse([px(ex - er * .62), px(ey - er * .62), px(ex + er * .62), px(ey + er * .62)], fill=(18, 12, 14, 255))
    ImageDraw.Draw(img).ellipse([px(ex - er * .45), px(ey - er * .5), px(ex - er * .1), px(ey - er * .15)], fill=(255, 255, 255, 230))
    ImageDraw.Draw(img).arc([px(cx - rx * 1.02), px(cy - ry * .02), px(cx - rx * .82), px(cy + ry * .22)], 100, 260, fill=(70, 20, 16, 220), width=px(1.6))
    if cap:   # the black lantern caps top and bottom
        for yy, h in ((cy - ry * 1.02, ry * .14), (cy + ry * .9, ry * .12)):
            shape(img, hexc('#1c1616'), seed + 7, ell=(cx - rx * .16, yy - h * .5, cx + rx * .16, yy + h * .5), scale=3, k=.4, rim=.2, spec=.2)


def cloud_mask(img, puffs, flat=None):
    m = Image.new('L', img.size, 0); d = ImageDraw.Draw(m)
    for x, y, r in puffs: d.ellipse([px(x - r), px(y - r * .82), px(x + r), px(y + r * .82)], fill=255)
    if flat: d.rectangle([0, px(flat), img.width, img.height], fill=0)
    return m.filter(ImageFilter.GaussianBlur(1.6 * S))


def cloud(img, puffs, seed, base='#6c67a0', light='#d6d0f0', shade='#2e2c5c', flat=None, rim=(236, 226, 255)):
    """Soft moon-lit cumulus: lavender body, deep indigo underside, pale rim toward the moon (upper right)."""
    m = cloud_mask(img, puffs, flat); box = m.getbbox()
    if not box: return m
    t = textured_fill(m.crop(box), H(base), H(shade), H(light), 7 * S, seed, (1.6, 1), 1.1)
    a = np.asarray(t, np.float32); h, w = a.shape[:2]; yy = np.linspace(0, 1, h)[:, None]; xx = np.linspace(0, 1, w)[None, :]
    a[..., :3] *= (1.12 - .55 * yy ** 1.3 + .12 * (xx - .5))[..., None]
    img.alpha_composite(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA'), box[:2])
    # rim light: where the mask ends toward the upper right
    mm = np.asarray(m, np.float32) / 255; sh = np.roll(np.roll(mm, px(5), 0), -px(4), 1); edge = np.clip(mm - sh, 0, 1)
    l = np.zeros(mm.shape + (4,), np.float32); l[..., :3] = rim; l[..., 3] = edge * 210
    img.alpha_composite(Image.fromarray(l.astype(np.uint8), 'RGBA').filter(ImageFilter.GaussianBlur(1.2 * S)))
    return m


def glass_bell(img, cx, top, r, tint, seed, pattern=None, strip='#c9b8e8', kanji='夢'):
    """A furin: blown-glass dome, a painted pattern inside, a clapper and a paper strip that catches the wind."""
    tint = H(tint)
    stroke(img, [(cx, 0), (cx, top + 2)], '#d8d0c0', 1.4)
    dome = [(cx - r * .95, top + r * 1.25), (cx - r, top + r * .7), (cx - r * .72, top + r * .12), (cx, top - r * .02), (cx + r * .72, top + r * .12), (cx + r, top + r * .7), (cx + r * .95, top + r * 1.25)]
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).polygon([(px(x), px(y)) for x, y in cr(dome, 10, False)], fill=255); m = m.filter(ImageFilter.GaussianBlur(.6 * S))
    t = textured_fill(m.crop(m.getbbox()), tint, dk(tint, .3), lt(tint, .45), 4 * S, seed, (1, 1), .4)
    a = np.asarray(t, np.float32); a[..., 3] *= .62; img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'), m.getbbox()[:2])
    if pattern: clipped(img, m, pattern, .95)
    # thick glass lip and a bright highlight stroke
    stroke(img, [(cx - r * .95, top + r * 1.25), (cx, top + r * 1.34), (cx + r * .95, top + r * 1.25)], lt(tint, .55), 2.2)
    soft(img, lambda d: d.line([(px(cx - r * .6), px(top + r * .25)), (px(cx - r * .78), px(top + r * .7)), (px(cx - r * .72), px(top + r * 1.05))], fill=(255, 255, 255, 190), width=px(r * .12)), .8)
    # clapper and the paper strip
    stroke(img, [(cx, top + r * .2), (cx, top + r * 2.1)], '#d8d0c0', 1.1)
    ImageDraw.Draw(img).ellipse([px(cx - r * .14), px(top + r * 1.05), px(cx + r * .14), px(top + r * 1.33)], fill=(240, 236, 226, 230))
    sw, sh = r * .9, r * 2.3; y0 = top + r * 2.05
    ms = fill(img, strip, seed + 5, poly=[(cx - sw / 2, y0), (cx + sw / 2, y0 + 2), (cx + sw / 2 + 3, y0 + sh), (cx - sw / 2 + 2, y0 + sh - 3)], scale=4, contrast=.6)
    if kanji: text(img, kanji, cx + 1, y0 + sh * .45, sw * .72, dk(H(strip), .6), SERIF, brush=True)


def sasabune(img, x0, y0, L, h, seed, col='#5f8c52'):
    """A bamboo-leaf boat: the leaf folded at both ends, slits tucked in — the toy every Japanese child floats in a ditch."""
    col = H(col)
    hull = [(x0, y0 + h * .2), (x0 + L * .18, y0 + h * .55), (x0 + L * .5, y0 + h * .78), (x0 + L * .82, y0 + h * .55), (x0 + L, y0 + h * .12), (x0 + L * .8, y0 + h * .4), (x0 + L * .5, y0 + h * .46), (x0 + L * .2, y0 + h * .42)]
    m = fill(img, col, seed, poly=cr(hull, 8), scale=5, stretch=(4, 1), contrast=.9)
    volume(img, (x0, y0, x0 + L, y0 + h), .5, .3)
    # the inner fold (darker) and the raised side wall
    fill(img, dk(col, .35), seed + 1, poly=cr([(x0 + L * .2, y0 + h * .42), (x0 + L * .5, y0 + h * .3), (x0 + L * .8, y0 + h * .4), (x0 + L * .5, y0 + h * .5)], 8), scale=4, contrast=.7)
    side = [(x0 + L * .14, y0 + h * .44), (x0 + L * .5, y0 + h * .52), (x0 + L * .86, y0 + h * .42), (x0 + L * .8, y0 + h * .62), (x0 + L * .5, y0 + h * .76), (x0 + L * .22, y0 + h * .62)]
    fill(img, lt(col, .12), seed + 2, poly=cr(side, 8), scale=5, stretch=(4, 1), contrast=.8)
    stroke(img, [(x0 + L * .16, y0 + h * .56), (x0 + L * .5, y0 + h * .64), (x0 + L * .84, y0 + h * .54)], lt(col, .4)[:3] + (160,), 1.2)
    # the folded tips with their slits
    for tx, sd in ((x0 + L * .1, -1), (x0 + L * .9, 1)):
        fill(img, lt(col, .2), seed + 3 + sd, poly=[(tx - sd * L * .06, y0 + h * .5), (tx + sd * L * .02, y0 - h * .05), (tx + sd * L * .08, y0 + h * .35)], scale=3, contrast=.6)
        stroke(img, [(tx - sd * L * .01, y0 + h * .12), (tx + sd * L * .03, y0 + h * .38)], dk(col, .5), 1.2)


def torii_shape(img, cx, base, w, h, seed, col='#b8412c'):
    col = H(col); pw = w * .075
    for sd in (-1, 1):   # pillars lean in a little
        x = cx + sd * w * .33
        fill(img, col, seed + sd, poly=[(x - pw * .55, base - h * .86), (x + pw * .55, base - h * .86), (x + pw * .62 + sd * 2, base), (x - pw * .62 + sd * 2, base)], scale=4, stretch=(1, 3))
        fill(img, '#1d1618', seed + 5 + sd, rect=(x - pw * .72, base - h * .07, x + pw * .72, base), scale=3)
        volume(img, (x - pw * .62, base - h * .86, x + pw * .62, base), .6, .2)
    fill(img, col, seed + 3, rect=(cx - w * .43, base - h * .7, cx + w * .43, base - h * .63), scale=4, stretch=(4, 1))   # nuki
    fill(img, col, seed + 4, rect=(cx - pw * .35, base - h * .86, cx + pw * .35, base - h * .7), scale=3)
    kas = [(cx - w * .52, base - h * .98), (cx - w * .3, base - h * .9), (cx, base - h * .885), (cx + w * .3, base - h * .9), (cx + w * .52, base - h * .98), (cx + w * .5, base - h * .9), (cx + w * .3, base - h * .82), (cx, base - h * .805), (cx - w * .3, base - h * .82), (cx - w * .5, base - h * .9)]
    fill(img, col, seed + 6, poly=cr(kas, 8), scale=4, stretch=(4, 1))
    top = [(cx - w * .54, base - h * 1.0), (cx - w * .3, base - h * .925), (cx, base - h * .91), (cx + w * .3, base - h * .925), (cx + w * .54, base - h * 1.0), (cx + w * .52, base - h * .955), (cx + w * .3, base - h * .885), (cx, base - h * .87), (cx - w * .3, base - h * .885), (cx - w * .52, base - h * .955)]
    fill(img, '#1d1618', seed + 7, poly=cr(top, 8), scale=3)
    volume(img, (cx - w * .54, base - h, cx + w * .54, base - h * .8), .5, .15)


# ───────────────────────────── Baku ─────────────────────────────
def baku():
    img = canvas(460, 400)
    body, body_d, belly = hexc('#8f86a3'), hexc('#655d7a'), hexc('#c9c0d6')
    tig, stripe, mane = hexc('#c97a3c'), (34, 22, 18, 235), hexc('#4a5c92')
    # ox tail with a curly tuft, behind everything
    stroke(img, [(112, 214), (78, 196), (58, 160), (62, 128)], body_d, 7)
    for i, (x, y, r) in enumerate([(62, 118, 16), (50, 128, 12), (74, 124, 12), (60, 104, 11)]):
        shape(img, mane, 300 + i, ell=(x - r, y - r, x + r, y + r), scale=4, k=.4, rim=.2)
        curl(img, x, y, r * .75, lt(mane, .35), 1.2, 1.3)
    # far legs (darker), tiger-striped
    def leg(x, top, far, seed):
        c = dk(tig, .28) if far else tig
        pts = [(x - 20, top), (x + 18, top), (x + 20, top + 50), (x + 16, top + 78), (x - 16, top + 78), (x - 20, top + 44)]
        m = shape(img, c, seed, pts, scale=6, contrast=.8, k=.5, rim=.3)
        clipped(img, m, lambda d, l: [d.polygon([(px(x - 22), px(top + 16 + k * 18)), (px(x + 4), px(top + 12 + k * 18)), (px(x - 4), px(top + 20 + k * 18))], fill=stripe) for k in range(3)] +
                [d.polygon([(px(x + 22), px(top + 22 + k * 18)), (px(x - 2), px(top + 18 + k * 18)), (px(x + 6), px(top + 26 + k * 18))], fill=stripe) for k in range(3)])
        paw = shape(img, c, seed + 1, ell=(x - 24, top + 68, x + 26, top + 94), scale=5, k=.45, rim=.3)
        for k in range(3):   # small ivory claws
            ImageDraw.Draw(img).polygon([(px(x - 16 + k * 14), px(top + 90)), (px(x - 11 + k * 14), px(top + 90)), (px(x - 14 + k * 14), px(top + 97))], fill=(236, 226, 206, 255))
        # a flame-curl at the elbow, like on temple carvings
        for k, (dx, dy) in enumerate(((-26, 8), (-30, 26))):
            curl(img, x + dx, top + dy, 7, lt(mane, .2) if not far else mane, 1.3, 1.8, ccw=True)
    leg(150, 262, True, 311); leg(304, 258, True, 313)
    # body: a round barrel, pale belly, swirl markings
    bd = [(120, 190), (170, 160), (240, 150), (300, 162), (340, 196), (348, 250), (320, 296), (250, 312), (170, 308), (118, 284), (100, 240)]
    mb = shape(img, body, 320, bd, scale=10, contrast=.9, dk=.45, lt=.25, k=.6, rim=.45)
    lb = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(lb).ellipse([px(136), px(236), px(334), px(346)], fill=belly); lb = lb.filter(ImageFilter.GaussianBlur(14 * S))
    ab = np.asarray(lb, np.float32); ab[..., 3] *= np.asarray(mb, np.float32) / 255 * .8; img.alpha_composite(Image.fromarray(ab.astype(np.uint8), 'RGBA'))
    rr = random.Random(321)
    def swirls(d, l):
        for x, y in ((170, 200), (226, 186), (276, 206), (200, 240), (150, 246)):
            for k in range(3):
                d.arc([px(x - 14 + k * 4), px(y - 10 + k * 3), px(x + 14 - k * 4), px(y + 10 - k * 3)], 200 + rr.uniform(-20, 20), 470, fill=(222, 214, 236, 120), width=px(1.6))
    clipped(img, mb, swirls)
    # near legs
    leg(186, 268, False, 330); leg(318, 262, False, 332)
    # mane of indigo curls along the neck
    for i, (x, y, r) in enumerate([(300, 138, 20), (284, 164, 18), (322, 118, 18), (268, 190, 16), (300, 196, 15), (340, 110, 15)]):
        shape(img, mane, 340 + i, ell=(x - r, y - r, x + r, y + r), scale=4, contrast=.9, k=.5, rim=.3)
        curl(img, x, y, r * .72, lt(mane, .4), 1.3, 1.6, ccw=i % 2 == 0)
    # the big soft elephant ear
    ear = [(338, 132), (310, 120), (296, 150), (300, 196), (322, 222), (350, 214), (360, 176)]
    me = shape(img, body_d, 350, ear, scale=6, contrast=.8, k=.5, rim=.3)
    clipped(img, me, lambda d, l: d.polygon([(px(x), px(y)) for x, y in cr([(334, 140), (312, 138), (306, 170), (318, 204), (342, 204), (348, 170)])], fill=(186, 130, 150, 150)))
    # head dome, heavy brow, a rhino's small wise eye
    hd = [(352, 108), (386, 104), (412, 124), (420, 158), (414, 190), (392, 208), (362, 204), (340, 182), (334, 146)]
    mh = shape(img, body, 351, hd, scale=7, contrast=.8, dk=.4, lt=.28, k=.6, rim=.4, spec=.1)
    shape(img, lt(body, .12), 352, [(360, 132), (392, 124), (414, 140), (404, 150), (378, 146), (360, 148)], scale=4, k=.4, rim=.2)
    ImageDraw.Draw(img).ellipse([px(380), px(146), px(398), px(160)], fill=hexc('#e2b34a'))
    ImageDraw.Draw(img).ellipse([px(386), px(147), px(393), px(159)], fill=(24, 16, 12, 255))
    ImageDraw.Draw(img).ellipse([px(383), px(148), px(387), px(152)], fill=(255, 255, 255, 230))
    stroke(img, [(376, 145), (390, 140), (402, 146)], dk(body, .55), 2.2)
    for k in range(3): stroke(img, [(344 + k * 4, 186 + k * 3), (356 + k * 4, 180 + k * 3)], dk(body, .3), 1.1)
    # the trunk, curling up at the tip — it is how he breathes in bad dreams
    trunk = tube([(404, 196), (416, 232), (420, 268), (430, 300), (446, 312), (452, 296)], 17, 7)
    mt = shape(img, body, 353, trunk, scale=6, contrast=.8, dk=.4, lt=.25, k=.5, rim=.35)
    clipped(img, mt, lambda d, l: [d.arc([px(396), px(200 + k * 14), px(438), px(214 + k * 14)], 20, 160, fill=(70, 60, 88, 150), width=px(1.3)) for k in range(7)])
    # small ivory tusks
    for x0 in (382, 394):
        shape(img, hexc('#efe6d2'), 354 + x0, [(x0, 206), (x0 + 8, 206), (x0 + 12, 226), (x0 + 22, 240), (x0 + 12, 238), (x0 + 2, 222)], scale=3, k=.4, rim=.2, spec=.3)
    # a cloud of dream-mist under his paws
    soft(img, lambda d: [d.ellipse([px(x - r), px(y - r * .5), px(x + r), px(y + r * .5)], fill=(210, 200, 240, 70)) for x, y, r in ((170, 364, 60), (250, 372, 70), (330, 364, 58))], 6)
    M.save(img, 'm_dr_baku')


# ───────────────────────────── items: «Из снов» ─────────────────────────────
ROWS, IMGS = [], []


def isave(img, iid, name, anchor='b', glow=None):
    IMGS.append((iid, finish_arr(img, sum(map(ord, iid)))))
    row = {'id': iid, 'n': name, 'c': 'Из снов', 'w': P.W, 'h': P.H, 'a': anchor, 'p': 0}
    if glow: row['glow'] = glow
    ROWS.append(row); print(iid, P.W, P.H, name)


def pack_items(path):
    lst = sorted(IMGS, key=lambda t: -t[1].height); W = 1024; x = y = rowh = 0; pos = {}
    for iid, im in lst:
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[iid] = (x, y); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for iid, im in lst: at.paste(im, pos[iid])
    at.save(path, 'WEBP', quality=86, alpha_quality=90, method=6)
    for r in ROWS: r['at'] = ['dr', pos[r['id']][0], pos[r['id']][1]]
    print('atlas items', at.size); return at.size


def hang_cord(img, cx, y1, col='#5a4a8a'):
    stroke(img, [(cx, 0), (cx - 1, y1 * .5), (cx, y1)], col, 2)
    ImageDraw.Draw(img).ellipse([px(cx - 4), px(y1 - 4), px(cx + 4), px(y1 + 4)], fill=H(col))


def items():
    # 1. lantern-fish on a string
    img = canvas(170, 190); hang_cord(img, 78, 52, '#3a2a24')
    lantern_fish(img, 72, 104, 46, 40, '#d34a2c', '#f4e4cc', 11, fin='#e8734a')
    isave(img, 'dr_fish', 'Рыба-фонарик', 't', [72, 104])
    # 2. a jar of sleepy lights
    img = canvas(120, 160); floor_shadow(img, 60, 154, 46)
    jar = [(26, 50), (94, 50), (100, 66), (102, 146), (92, 154), (28, 154), (18, 146), (20, 66)]
    fill(img, '#1c2442', 21, poly=jar, scale=4, contrast=.4)
    for x, y, r, c in ((44, 110, 9, '#f6e08a'), (72, 90, 7, '#bfe6ff'), (60, 130, 8, '#f6e08a'), (82, 124, 6, '#e8c8ff'), (40, 80, 5, '#bfe6ff'), (76, 142, 5, '#f6e08a')):
        glowdot(img, x, y, r * 2.2, c, 150); ImageDraw.Draw(img).ellipse([px(x - r * .35), px(y - r * .35), px(x + r * .35), px(y + r * .35)], fill=H(c))
    lantern_fish(img, 58, 104, 12, 10, '#d34a2c', '#f4e4cc', 22, cap=False)
    from room_items2 import glass
    glass(img, jar, 23, (190, 205, 235))
    fill(img, '#9a7a52', 24, rect=(30, 34, 90, 52), scale=3, contrast=1.2); volume(img, (30, 34, 90, 52), .5, .2)
    stroke(img, [(24, 48), (60, 52), (96, 48)], '#d8c8a0', 2); stroke(img, [(96, 48), (104, 60), (100, 70)], '#d8c8a0', 1.6)
    isave(img, 'dr_jar', 'Банка с сонными огоньками', 'b', [60, 104])
    # 3. a pillow made of cloud
    img = canvas(210, 120); floor_shadow(img, 105, 112, 88, 90)
    cloud(img, [(50, 76, 36), (84, 60, 40), (124, 58, 42), (160, 74, 36), (104, 84, 50), (70, 90, 34), (144, 92, 34)], 31, base='#bdb6dc', light='#f4f0ff', shade='#6e6a9c', flat=110, rim=(255, 250, 255))
    for x, y in ((88, 88), (132, 86)): curl(img, x, y, 7, '#d8b85a', .9, 1.6)
    stroke(img, [(96, 70), (104, 64), (112, 70)], '#d8b85a', 1.6)
    isave(img, 'dr_pillow', 'Облачная подушка')
    # 4. the moon key on a ribbon
    img = canvas(100, 220); hang_cord(img, 50, 44, '#3a3a78')
    for sd in (-1, 1): stroke(img, [(50, 44), (50 + sd * 16, 58), (50 + sd * 12, 74)], '#3a3a78', 3)
    moon = Image.new('L', img.size, 0); d = ImageDraw.Draw(moon); d.ellipse([px(22), px(52), px(78), px(108)], fill=255); d.ellipse([px(34), px(46), px(88), px(100)], fill=0)
    gold = hexc('#dccf9a'); t = textured_fill(moon.crop(moon.getbbox()), gold, dk(gold, .4), lt(gold, .45), 4 * S, 41, (1, 1), 1.2); img.alpha_composite(t, moon.getbbox()[:2])
    glowdot(img, 40, 86, 26, '#fff4c8', 70)
    fill(img, gold, 42, rect=(45, 100, 55, 192), scale=3, contrast=1.1); volume(img, (45, 100, 55, 192), .6, .1)
    fill(img, gold, 43, poly=[(55, 160), (70, 160), (70, 170), (62, 170), (62, 176), (70, 176), (70, 190), (55, 192)], scale=3)
    ImageDraw.Draw(img).ellipse([px(44), px(112), px(56), px(124)], fill=hexc('#8fb0e8'))
    for x, y in ((62, 66), (70, 80)): ImageDraw.Draw(img).ellipse([px(x - 2), px(y - 2), px(x + 2), px(y + 2)], fill=(255, 250, 220, 255))
    isave(img, 'dr_key', 'Лунный ключ', 't', [50, 90])
    # 5. a little paper door, lit from behind, with someone's shadow
    img = canvas(140, 210); floor_shadow(img, 70, 204, 64)
    fill(img, '#2c1e16', 51, rect=(14, 12, 126, 200), scale=4, contrast=1.1)
    fill(img, '#f1dcae', 52, rect=(22, 20, 118, 186), scale=4, contrast=.5)
    glowdot(img, 70, 104, 60, '#ffd890', 120)
    soft(img, lambda d: [d.ellipse([px(46), px(96), px(96), px(170)], fill=(40, 26, 30, 150)), d.polygon([(px(52), px(110)), (px(56), px(78)), (px(68), px(102))], fill=(40, 26, 30, 150)),
                         d.polygon([(px(90), px(110)), (px(86), px(78)), (px(74), px(102))], fill=(40, 26, 30, 150)), d.ellipse([px(52), px(92), px(90), px(128)], fill=(40, 26, 30, 150))], 2.5)
    for x in (54, 86): ImageDraw.Draw(img).line([(px(x), px(20)), (px(x), px(186))], fill=hexc('#3a2a1e'), width=px(3))
    for y in (52, 86, 120, 154): ImageDraw.Draw(img).line([(px(22), px(y)), (px(118), px(y))], fill=hexc('#3a2a1e'), width=px(3))
    fill(img, '#0e0c16', 53, rect=(104, 20, 118, 186), scale=3)
    for y, r in ((60, 2.2), (110, 1.6), (150, 2.6)): glowdot(img, 111, y, r * 3, '#cfe0ff', 160)
    fill(img, '#2c1e16', 54, rect=(100, 20, 106, 186), scale=3)
    fill(img, '#1a120c', 55, rect=(8, 194, 132, 206), scale=3)
    volume(img, (8, 8, 132, 206), .4, .2)
    isave(img, 'dr_door', 'Бумажная дверца', 'b', [70, 104])
    # 6. an hourglass with moon sand
    img = canvas(110, 180); floor_shadow(img, 55, 174, 46)
    for y0 in (12, 156): fill(img, '#5a3a24', 61 + y0, rect=(14, y0, 96, y0 + 14), scale=4, contrast=1.1); volume(img, (14, y0, 96, y0 + 14), .5, .2)
    top = [(26, 26), (84, 26), (80, 60), (60, 86), (50, 86), (30, 60)]; bot = [(50, 88), (60, 88), (80, 116), (84, 156), (26, 156), (30, 116)]
    sand = hexc('#b8cef8')
    fill(img, sand, 63, poly=[(40, 62), (70, 62), (58, 84), (52, 84)], scale=3, contrast=.5)
    fill(img, sand, 64, poly=cr([(28, 156), (40, 136), (55, 126), (70, 136), (82, 156)], 6), scale=3, contrast=.6)
    stroke(img, [(55, 84), (55, 128)], lt(sand, .4), 1.4)
    glowdot(img, 55, 140, 30, '#cfe0ff', 110)
    from room_items2 import glass
    glass(img, top, 65, (200, 212, 235)); glass(img, bot, 66, (200, 212, 235))
    for x in (18, 88): fill(img, '#4a2e1c', 67 + x, rect=(x, 26, x + 5, 156), scale=3); volume(img, (x, 26, x + 5, 156), .6, .1)
    isave(img, 'dr_hglass', 'Песочные часы с лунным песком', 'b', [55, 130])
    # 7. the dream furin
    img = canvas(96, 230)
    def stars(d, l):
        rr = random.Random(71)
        d.rectangle([0, 0, l.width, l.height], fill=(30, 36, 92, 150))
        for _ in range(26):
            x, y = rr.uniform(10, 86), rr.uniform(20, 100); r = rr.uniform(.8, 2.2); d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=(255, 244, 200, 230))
        d.ellipse([px(52), px(40), px(70), px(58)], fill=(255, 240, 190, 240)); d.ellipse([px(57), px(37), px(75), px(55)], fill=(30, 36, 92, 255))
    glass_bell(img, 48, 22, 34, (170, 190, 240), 72, stars, strip='#c9b8e8', kanji='夢')
    isave(img, 'dr_furin', 'Стеклянный фурин из сна', 't', [48, 50])
    # 8. the bell of silence
    img = canvas(130, 180); floor_shadow(img, 65, 174, 56)
    for x in (18, 104): fill(img, '#1c1414', 81 + x, rect=(x, 22, x + 8, 170), scale=3); volume(img, (x, 22, x + 8, 170), .6, .1)
    fill(img, '#1c1414', 83, poly=[(6, 18), (124, 18), (120, 28), (10, 28)], scale=3); fill(img, '#1c1414', 84, rect=(12, 158, 118, 168), scale=3)
    stroke(img, [(65, 28), (65, 44)], '#b89a5a', 3)
    bell = [(44, 46), (86, 46), (90, 60), (92, 104), (98, 118), (32, 118), (38, 104), (40, 60)]
    mb = fill(img, '#5f7a6a', 85, poly=bell, scale=4, contrast=1.2)
    clipped(img, mb, lambda d, l: [d.ellipse([px(x - 2.4), px(y - 2.4), px(x + 2.4), px(y + 2.4)], fill=(140, 170, 150, 255)) for x in (50, 58, 66, 74, 82) for y in (56, 64, 72)])
    clipped(img, mb, lambda d, l: [d.line([(px(38), px(y)), (px(92), px(y))], fill=(40, 56, 48, 255), width=px(2)) for y in (80, 104)])
    volume(img, (32, 44, 98, 118), .6, .35, .15)
    text(img, '静', 65, 92, 13, '#c8d8c8', SERIF)
    stroke(img, [(65, 118), (62, 132), (66, 146)], '#7a4aa8', 3)
    fill(img, '#7a4aa8', 86, poly=[(58, 144), (74, 144), (78, 160), (54, 160)], scale=3, contrast=.8)
    isave(img, 'dr_bell', 'Колокольчик тишины')
    # 9. the star boat
    img = canvas(210, 110); floor_shadow(img, 105, 102, 88, 80)
    sasabune(img, 8, 36, 194, 70, 91)
    glowdot(img, 104, 58, 34, '#fff0b0', 150)
    star = [(104 + math.cos(a) * (15 if i % 2 == 0 else 6.5), 56 + math.sin(a) * (15 if i % 2 == 0 else 6.5)) for i, a in enumerate(np.linspace(-math.pi / 2, math.pi * 1.5, 11)[:-1])]
    fill(img, '#f4dc7a', 92, poly=star, scale=2, contrast=.5)
    isave(img, 'dr_boat', 'Звёздная лодочка', 'b', [104, 56])
    # 10. a feather of sleep in a small vase
    img = canvas(96, 230); floor_shadow(img, 48, 224, 34)
    vane = [(48, 12), (60, 30), (66, 70), (62, 120), (54, 160), (48, 176), (42, 160), (34, 118), (30, 70), (36, 30)]
    mv = fill(img, '#d8d0f0', 101, poly=cr(vane, 8), scale=3, stretch=(1, 4), contrast=.8)
    clipped(img, mv, lambda d, l: [d.line([(px(48), px(20 + k * 7)), (px(48 + (1 if k % 2 else -1) * 22), px(12 + k * 7))], fill=(150, 140, 200, 150), width=px(1)) for k in range(22)])
    clipped(img, mv, lambda d, l: d.rectangle([0, px(110), l.width, l.height], fill=(110, 130, 220, 110)))
    stroke(img, [(48, 16), (48, 170), (48, 196)], '#f4f0ff', 1.6)
    for x, y in ((66, 40), (28, 90), (70, 110), (32, 140)): glowdot(img, x, y, 5, '#e8e0ff', 180)
    vase = [(36, 186), (60, 186), (66, 200), (64, 222), (32, 222), (30, 200)]
    fill(img, '#2c3a78', 102, poly=vase, scale=4, contrast=1.1); volume(img, (30, 186, 66, 222), .6, .3, .2)
    isave(img, 'dr_feather', 'Перо сна', 'b', [48, 90])
    # 11. a drowned shrine in a bowl: a little torii standing in water, petals afloat
    img = canvas(200, 150); floor_shadow(img, 100, 144, 88)
    fill(img, '#2a2230', 111, poly=cr([(10, 96), (100, 88), (190, 96), (178, 132), (100, 142), (22, 132)], 8), scale=4, contrast=1.1)
    volume(img, (10, 88, 190, 142), .5, .3)
    water = fill(img, '#1c3050', 112, ell=(18, 86, 182, 112), scale=5, stretch=(4, 1), contrast=.9)
    clipped(img, water, lambda d, l: [d.line([(px(x), px(y)), (px(x + 26), px(y))], fill=(150, 180, 230, 120), width=px(1)) for x, y in ((40, 96), (110, 104), (130, 94), (60, 106))])
    torii_shape(img, 100, 100, 70, 74, 113)
    l2 = Image.new('RGBA', img.size, (0, 0, 0, 0)); torii_shape(l2, 100, 100, 70, 74, 113)
    ref = l2.transpose(Image.FLIP_TOP_BOTTOM); a = np.asarray(ref, np.float32); a[..., 3] *= .28
    ref = Image.fromarray(a.astype(np.uint8), 'RGBA'); sh = ImageChops_offset(ref, 0, px(100) * 2 - img.height)
    a = np.asarray(sh, np.float32); a[..., 3] *= np.asarray(water, np.float32) / 255; img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))
    for x, y, r in ((50, 100, 5), (140, 104, 6), (160, 94, 4), (74, 108, 4)):
        ImageDraw.Draw(img).ellipse([px(x - r), px(y - r * .6), px(x + r), px(y + r * .6)], fill=hexc('#efb8c8'))
    isave(img, 'dr_torii', 'Храм в чаше')
    # 12. Baku's mask
    img = canvas(150, 200)
    stroke(img, [(30, 44), (75, 4), (120, 44)], '#b8412c', 2.4)
    for sd in (-1, 1): shape(img, hexc('#a8703a'), 121 + sd, ell=(75 + sd * 50 - 18, 44, 75 + sd * 50 + 18, 92), scale=4, k=.5, rim=.3)
    face = [(75, 30), (110, 40), (124, 70), (116, 104), (96, 124), (75, 130), (54, 124), (34, 104), (26, 70), (40, 40)]
    mf = shape(img, hexc('#c89a58'), 123, face, scale=5, contrast=1.0, dk=.4, lt=.3, k=.6, rim=.35, spec=.15)
    trunk = tube([(75, 112), (78, 140), (72, 164), (80, 184), (94, 186), (96, 174)], 14, 6)
    shape(img, hexc('#c89a58'), 124, trunk, scale=5, k=.5, rim=.3)
    for k in range(5): stroke(img, [(66, 132 + k * 11), (84, 132 + k * 11)], '#7a5a30', 1.2)
    for sd in (-1, 1):
        ImageDraw.Draw(img).ellipse([px(75 + sd * 24 - 9), px(72), px(75 + sd * 24 + 9), px(86)], fill=hexc('#f0c848'))
        ImageDraw.Draw(img).ellipse([px(75 + sd * 24 - 4), px(74), px(75 + sd * 24 + 4), px(84)], fill=(20, 14, 10, 255))
        stroke(img, [(75 + sd * 12, 68), (75 + sd * 26, 62), (75 + sd * 38, 68)], '#3a2a60', 3)
        shape(img, hexc('#efe6d2'), 125 + sd, [(75 + sd * 12, 118), (75 + sd * 20, 118), (75 + sd * 30, 140), (75 + sd * 20, 138)], scale=3, k=.4, rim=.2)
        stroke(img, [(75 + sd * 30, 100), (75 + sd * 42, 108)], '#b8412c', 2.4)
    for i, x in enumerate((50, 75, 100)): curl(img, x, 46, 9, '#3a4a8a', 1.4, 2.4, ccw=i % 2 == 0)
    isave(img, 'dr_baku', 'Маска Баку', 't', [75, 90])


def ImageChops_offset(im, dx, dy):
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); out.paste(im, (dx, dy)); return out


# ───────────────────────────── sprite sheet for the dream worlds ─────────────────────────────
SPR = []


def ssave(img, name):
    SPR.append((name, finish_arr(img, sum(map(ord, name)), sat=.95, noise=3)))
    print('sprite', name, P.W, P.H)


def sprites():
    for name, body, belly, fin, spots in (('fishR', '#d8462c', '#f6e6cc', '#ee7a4e', None), ('fishW', '#eee4d6', '#fbf4ea', '#f0c0b0', '#d8462c'), ('fishG', '#e0a23a', '#f8ecc8', '#f2c46a', None)):
        img = canvas(210, 150); lantern_fish(img, 84, 78, 60, 52, body, belly, sum(map(ord, name)), fin=fin, spots=spots); ssave(img, name)
    # the moon with the rabbit pounding mochi in its seas
    img = canvas(400, 400); c = 200; R = 190
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).ellipse([px(c - R), px(c - R), px(c + R), px(c + R)], fill=255); m = m.filter(ImageFilter.GaussianBlur(1.2 * S))
    t = textured_fill(m, hexc('#f2ead2'), hexc('#c8bfa4'), hexc('#fffaf0'), 26 * S, 201, (1, 1), 1.0); img.alpha_composite(t)
    def maria(d, l):
        col = (132, 138, 160, 120)
        d.ellipse([px(150), px(190), px(250), px(290)], fill=col)                       # body
        d.ellipse([px(210), px(150), px(268), px(206)], fill=col)                       # head
        d.polygon([(px(x), px(y)) for x, y in cr([(236, 156), (250, 92), (266, 70), (268, 96), (254, 160)])], fill=col)   # ears
        d.polygon([(px(x), px(y)) for x, y in cr([(222, 160), (214, 96), (224, 76), (236, 100), (238, 158)])], fill=col)
        d.polygon([(px(x), px(y)) for x, y in [(150, 300), (138, 250), (160, 240), (178, 296)]], fill=col)
        d.line([(px(230), px(210)), (px(150), px(150))], fill=col, width=px(10))            # the mallet (kine)
        d.ellipse([px(126), px(128), px(170), px(160)], fill=col)
        d.polygon([(px(x), px(y)) for x, y in [(80, 250), (140, 250), (132, 310), (88, 310)]], fill=col)   # the mortar (usu)
        d.ellipse([px(78), px(238), px(142), px(262)], fill=(150, 150, 170, 140))
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); maria(ImageDraw.Draw(l), l); l = l.filter(ImageFilter.GaussianBlur(7 * S))
    a = np.asarray(l, np.float32); a[..., 3] *= np.asarray(m, np.float32) / 255; img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))
    rr = random.Random(202)
    def craters(d, l):
        for _ in range(26):
            x, y = rr.uniform(40, 360), rr.uniform(40, 360); r = rr.uniform(4, 16)
            if (x - c) ** 2 + (y - c) ** 2 > (R - 14) ** 2: continue
            d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=(150, 146, 150, 70)); d.arc([px(x - r), px(y - r), px(x + r), px(y + r)], 200, 380, fill=(255, 250, 235, 110), width=px(1.4))
    clipped(img, m, craters)
    a = np.asarray(img, np.float32); yy, xx = np.mgrid[0:img.height, 0:img.width]; dd = np.sqrt((xx - px(c)) ** 2 + (yy - px(c)) ** 2) / px(R)
    a[..., :3] *= (1 - .28 * np.clip(dd - .55, 0, 1) ** 1.4 * 2.2)[..., None]; img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA'); ssave(img, 'moon')
    # cloud puffs (the steps of the moon ladder and drifting banks)
    for name, (w, h), puffs in (('cloudA', (330, 150), [(60, 100, 44), (110, 78, 56), (170, 66, 62), (230, 80, 52), (280, 102, 40), (140, 108, 50), (210, 110, 46)]),
                                ('cloudB', (260, 120), [(50, 84, 36), (96, 62, 46), (150, 56, 48), (200, 76, 40), (120, 90, 42), (176, 94, 34)]),
                                ('cloudC', (220, 110), [(46, 78, 32), (90, 58, 40), (140, 60, 38), (176, 80, 30), (110, 84, 36)])):
        img = canvas(w, h); cloud(img, puffs, sum(map(ord, name)), flat=h - 16); ssave(img, name)
    # three glass wind-bells with paper strips
    def goldfish(d, l):
        for x, y in ((30, 60), (54, 76)): d.ellipse([px(x - 8), px(y - 4), px(x + 8), px(y + 4)], fill=(214, 64, 44, 230)); d.polygon([(px(x + 7), px(y)), (px(x + 14), px(y - 5)), (px(x + 14), px(y + 5))], fill=(214, 64, 44, 230))
        for x in range(8, 80, 12): d.arc([px(x), px(84), px(x + 12), px(94)], 180, 360, fill=(80, 120, 200, 200), width=px(1.6))
    def asagao(d, l):
        for x, y, col in ((26, 58, (110, 90, 200, 230)), (56, 70, (200, 90, 160, 230))):
            for k in range(5):
                a = k / 5 * math.tau; d.ellipse([px(x + math.cos(a) * 5 - 6), px(y + math.sin(a) * 5 - 6), px(x + math.cos(a) * 5 + 6), px(y + math.sin(a) * 5 + 6)], fill=col)
            d.ellipse([px(x - 3), px(y - 3), px(x + 3), px(y + 3)], fill=(250, 240, 250, 255))
        d.line([(px(10), px(80)), (px(40), px(64)), (px(70), px(86))], fill=(80, 150, 90, 220), width=px(1.6))
    def starry(d, l):
        rr2 = random.Random(5); d.rectangle([0, 0, l.width, l.height], fill=(28, 36, 96, 140))
        for _ in range(18):
            x, y = rr2.uniform(8, 76), rr2.uniform(34, 96); r = rr2.uniform(.8, 2); d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=(255, 244, 200, 230))
    for name, tint, pat, strip, kj in (('furinA', (190, 220, 240), goldfish, '#e8d0a0', '涼'), ('furinB', (220, 200, 240), asagao, '#b8d0e8', '風'), ('furinC', (170, 190, 240), starry, '#d8c0e8', '夢')):
        img = canvas(84, 200); glass_bell(img, 42, 30, 30, tint, sum(map(ord, name)), pat, strip, kj); ssave(img, name)
    # the leaf boat Musya sails in
    img = canvas(300, 110); sasabune(img, 6, 20, 288, 88, 301, col='#5a8a5a'); ssave(img, 'boat')
    # a vermilion torii and a drowned shrine hall
    img = canvas(300, 270); torii_shape(img, 150, 266, 260, 262, 311, col='#c0452e'); ssave(img, 'torii')
    img = canvas(460, 280)
    for x in (70, 170, 290, 390): fill(img, '#8a2e22', 330 + x, rect=(x - 9, 120, x + 9, 280), scale=4, stretch=(1, 3)); volume(img, (x - 9, 120, x + 9, 280), .6, .15)
    fill(img, '#1c1820', 340, rect=(60, 130, 400, 280), scale=5, contrast=.8)
    for x in (80, 180, 280): fill(img, '#d8c8a0', 341 + x, rect=(x + 14, 150, x + 86, 250), scale=4, contrast=.5)
    glowdot(img, 230, 200, 110, '#ffd890', 70)
    for x in (80, 180, 280):
        for k in (1, 2): ImageDraw.Draw(img).line([(px(x + 14 + k * 24), px(150)), (px(x + 14 + k * 24), px(250))], fill=hexc('#2a1e18'), width=px(2))
        for k in (1, 2, 3): ImageDraw.Draw(img).line([(px(x + 14), px(150 + k * 25)), (px(x + 86), px(150 + k * 25))], fill=hexc('#2a1e18'), width=px(2))
    fill(img, '#6a2620', 342, rect=(40, 112, 420, 132), scale=4, stretch=(5, 1)); volume(img, (40, 112, 420, 132), .5, .1)
    roof = [(0, 110), (40, 96), (100, 70), (160, 34), (230, 22), (300, 34), (360, 70), (420, 96), (460, 110), (440, 120), (230, 104), (20, 120)]
    mr = fill(img, '#2c3048', 343, poly=cr(roof, 8), scale=4, stretch=(1, 3), contrast=1.1)
    clipped(img, mr, lambda d, l: [d.line([(px(x), px(0)), (px(x + (x - 230) * .12), px(124))], fill=(20, 22, 36, 150), width=px(1.6)) for x in range(10, 460, 12)])
    volume(img, (0, 20, 460, 124), .5, .25)
    stroke(img, [(40, 100), (160, 38), (230, 26), (300, 38), (420, 100)], '#8a8fb8', 1.6)
    for sd in (-1, 1):   # crossed chigi on the ridge
        stroke(img, [(230 + sd * 60, 36), (230 + sd * 76, 6)], '#2c3048', 5); stroke(img, [(230 + sd * 76, 36), (230 + sd * 60, 6)], '#2c3048', 5)
    fill(img, '#2c3048', 344, rect=(150, 16, 310, 30), scale=3)
    ssave(img, 'shrine')
    # the thought bubble over sleeping Musya, and its two small puffs
    img = canvas(230, 170)
    cloud(img, [(58, 96, 44), (100, 66, 52), (152, 64, 50), (188, 96, 38), (122, 108, 50), (74, 118, 34), (164, 120, 34)], 401, base='#cbc4e6', light='#fbf8ff', shade='#8a84b8', rim=(255, 255, 255))
    ssave(img, 'bubble')
    img = canvas(56, 44); cloud(img, [(28, 22, 22)], 402, base='#cbc4e6', light='#fbf8ff', shade='#8a84b8', rim=(255, 255, 255)); ssave(img, 'puff')


def pack_sprites(path):
    lst = sorted(SPR, key=lambda t: -t[1].height); W = 1024; x = y = rowh = 0; pos = {}
    for n, im in lst:
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[n] = (x, y, im.width, im.height); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for n, im in lst: at.paste(im, pos[n][:2])
    at.save(path, 'WEBP', quality=86, alpha_quality=90, method=6)
    print('atlas sprites', at.size); return at.size, pos


if __name__ == '__main__':
    os.makedirs('out', exist_ok=True)
    which = sys.argv[2:] or ['baku', 'items', 'sprites']
    meta = {}
    if 'baku' in which: baku(); meta['MON'] = M.META
    if 'items' in which: items(); meta['atlas'] = pack_items(ROOT + '/items/atlas_dr.webp'); meta['items'] = ROWS
    if 'sprites' in which: sprites(); sz, pos = pack_sprites(ROOT + '/bg/dr_sprites.webp'); meta['spr_size'] = sz; meta['spr'] = pos
    json.dump(meta, open('out/dreams.json', 'w'), ensure_ascii=False)
    print(json.dumps({k: v for k, v in meta.items() if k != 'items'}, ensure_ascii=False))
