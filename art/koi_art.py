#!/usr/bin/env python3
"""«Пруд с карпами»: the nursery tub for the courtyard + 5 koi-show trophies, packed into one atlas.
Koi themselves are painted in the browser from pattern data (feat/koi.js), so no per-fish files.
Usage: koi_art.py <assets dir> → <assets>/items/atlas_ko.webp (+ preview in art/out); prints the rect JSON for feat/koi.js."""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
ASSETS = sys.argv[1]
sys.argv = [sys.argv[0], os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')]
import paint as P
from paint import hexc, mixc
import items as I
from items import px, canvas, fill, volume, soft, floor_shadow, line, ell, poly, text, H, dk, lt, SERIF, SANS, mask_poly
from room_items import clip

IMGS = {}


def fin(img, iid):
    """Finish right away (canvas size is global): downscale, mute colours a bit, film grain."""
    out = img.resize((P.W, P.H), Image.LANCZOS)
    a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .88
    a[..., :3] += np.random.default_rng(abs(hash(iid)) % 2 ** 32).normal(0, 3.2, a.shape[:2])[..., None]
    IMGS[iid] = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA'); print(iid, P.W, P.H)


def tub():
    """Shallow wooden nursery tub (hangiri-like) seen a little from above; dark water inside (fry are drawn live)."""
    W_, H_ = 240, 150; img = canvas(W_, H_); cx = 120
    floor_shadow(img, cx, 140, 116, 120)
    wood, hoop = H('#8a6038'), H('#3a2a1a')
    # outer wall: ellipse top (rim) + straight-ish sides down to the base ellipse
    body = [(cx - 112, 58)] + [(cx - 112 + 224 * k / 30, 58 + 30 * math.sin(math.pi * k / 30)) for k in range(31)] + [(cx + 112, 58), (cx + 104, 120)] + \
           [(cx + 104 - 208 * k / 30, 120 + 18 * math.sin(math.pi * k / 30)) for k in range(31)] + [(cx - 104, 120)]
    m = fill(img, wood, 31, poly=body, scale=7, stretch=(.25, 3), contrast=1.15)
    clip(img, m, lambda d: [d.line([(px(cx - 112 + k * 14), px(60)), (px(cx - 104 + k * 13), px(140))], fill=(0, 0, 0, 55), width=px(1.3)) for k in range(1, 17)])
    for y0, y1 in ((70, 82), (104, 116)):    # bamboo hoops
        pts = [(cx - 110 + 220 * k / 30, y0 + 22 * math.sin(math.pi * k / 30)) for k in range(31)] + [(cx + 108 - 216 * k / 30, y1 + 22 * math.sin(math.pi * (1 - k / 30))) for k in range(31)]
        fill(img, hoop, y0, poly=pts, scale=3, contrast=1.3, light=.35)
    volume(img, (cx - 112, 40, cx + 112, 140), .5, .45)
    # rim (top cut of the staves) and the water inside
    ell(img, (cx - 113, 26, cx + 113, 90), dk(wood, .25)); fill(img, lt(wood, .15), 33, ell=(cx - 111, 27, cx + 111, 88), scale=4, stretch=(3, .4), contrast=1.2)
    fill(img, '#1d3433', 34, ell=(cx - 101, 33, cx + 101, 83), scale=10, contrast=.9, dark=.5, light=.25)
    soft(img, lambda d: d.ellipse([px(cx - 101), px(33), px(cx + 101), px(48)], fill=(0, 0, 0, 120)), 4)     # inner wall shade
    soft(img, lambda d: d.ellipse([px(cx - 30), px(48), px(cx + 70), px(66)], fill=(150, 185, 180, 40)), 6)  # moon on water
    # a lotus pad and a tiny bud floating at the back
    lp = [(cx - 78 + 30 * math.cos(a), 52 + 10 * math.sin(a)) for a in np.linspace(.3, math.tau - .1, 24)] + [(cx - 78, 52)]
    fill(img, '#3f5a32', 35, poly=lp, scale=3, contrast=1.1, light=.3); line(img, [(cx - 78, 52), (cx - 52, 49)], '#2a3d22', 1)
    ell(img, (cx - 96, 40, cx - 86, 50), '#d6a0a8'); ell(img, (cx - 93, 38, cx - 89, 46), '#f0c8cc')
    fin(img, 'tub')


def rosette(iid, c1, c2, kan):
    img = canvas(110, 190); c1, c2 = H(c1), H(c2); cx, cy = 55, 62
    line(img, [(55, 0), (55, 14)], '#2a1c14', 1.2)
    for s, ang in ((-1, .18), (1, -.18)):        # two ribbon tails with notched ends
        x0 = cx + s * 10; pts = [(x0 - 10, 80), (x0 + 10, 80), (x0 + 14 + s * 14, 184), (x0 + s * 14 + 2, 172), (x0 - 10 + s * 14, 186)]
        fill(img, c1, 40 + s, poly=pts, scale=4, stretch=(.4, 3), contrast=1.1)
        line(img, [(x0 + 3 * s, 84), (x0 + s * 16, 176)], c2, 2)
    rnd = random.Random(iid)
    for r, col in ((52, c2), (44, c1)):        # pleated rings
        pts = []
        for k in range(72):
            a = k / 72 * math.tau; rr = r + (4 if k % 2 else -2) + rnd.uniform(-.6, .6); pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        fill(img, col, r, poly=pts, scale=3, contrast=1.25, light=.3)
        clip(img, mask_poly(img, poly=pts), lambda d: [d.line([(px(cx), px(cy)), (px(cx + math.cos(k / 36 * math.tau) * r), px(cy + math.sin(k / 36 * math.tau) * r))], fill=(0, 0, 0, 45), width=px(.8)) for k in range(36)])
    ell(img, (cx - 27, cy - 27, cx + 27, cy + 27), '#e9e1cc'); fill(img, '#efe6cf', 41, ell=(cx - 25, cy - 25, cx + 25, cy + 25), scale=6, contrast=.6, dark=.12)
    ImageDraw.Draw(img).ellipse([px(cx - 25), px(cy - 25), px(cx + 25), px(cy + 25)], outline=H('#b8963a'), width=px(2))
    text(img, kan, cx, cy - 1, 30, '#2a1410', SERIF, brush=True)
    volume(img, (cx - 54, cy - 54, cx + 54, cy + 54), .45, .3, spec=.12)
    fin(img, iid)


def cup():
    img = canvas(150, 210); cx = 75; gold = H('#c9a03a')
    floor_shadow(img, cx, 204, 62, 120)
    fill(img, '#2a1c14', 50, poly=[(cx - 52, 204), (cx + 52, 204), (cx + 46, 172), (cx - 46, 172)], scale=5, contrast=1.2, light=.3)   # wooden plinth
    fill(img, '#1c120c', 51, rect=(cx - 30, 180, cx + 30, 196), scale=4); fill(img, gold, 52, rect=(cx - 26, 183, cx + 26, 193), scale=3, light=.4)
    fill(img, gold, 53, poly=[(cx - 30, 172), (cx + 30, 172), (cx + 12, 158), (cx + 7, 130), (cx - 7, 130), (cx - 12, 158)], scale=3, contrast=1.3, light=.45)
    bowl = [(cx - 50, 30)] + [(cx - 50 + 100 * k / 24, 30 + 92 * math.sin(math.pi * k / 24) ** .8 * (1 if k else 0)) for k in range(25)]
    bowl = [(cx - 50, 30), (cx - 47, 70), (cx - 34, 108), (cx - 10, 128), (cx + 10, 128), (cx + 34, 108), (cx + 47, 70), (cx + 50, 30)]
    from room_items import cr
    fill(img, gold, 54, poly=cr(bowl, 8), scale=4, contrast=1.3, light=.5)
    for s in (-1, 1):  # handles
        pts = [(cx + s * 46, 46), (cx + s * 70, 44), (cx + s * 72, 78), (cx + s * 40, 100)]
        for w, col in ((7, dk(gold, .3)), (4, gold)): line(img, pts, col, w)
    ell(img, (cx - 50, 22, cx + 50, 40), dk(gold, .45)); ell(img, (cx - 46, 25, cx + 46, 37), '#2a1e10')
    volume(img, (cx - 52, 22, cx + 52, 130), .6, .35, spec=.55)
    # engraved koi on the bowl
    d = ImageDraw.Draw(img); pts = [(cx - 22, 82), (cx - 6, 70), (cx + 14, 74), (cx + 24, 82), (cx + 14, 88), (cx - 6, 92)]
    d.line([(px(x), px(y)) for x, y in pts + pts[:1]], fill=dk(gold, .45), width=px(1.6)); d.polygon([(px(cx - 22), px(82)), (px(cx - 32), px(74)), (px(cx - 32), px(92))], outline=dk(gold, .45))
    ell(img, (cx + 13, 77, cx + 17, 81), dk(gold, .5))
    fin(img, 'ko_cup')


def scroll():
    img = canvas(120, 270); fr = H('#3a4a5a')
    line(img, [(34, 4), (60, 0), (86, 4)], '#1a120c', 1.2)
    ImageDraw.Draw(img).rectangle([px(12), px(8), px(108), px(15)], fill=H('#2a1c14'))
    fill(img, fr, 60, rect=(12, 14, 108, 252), scale=6, contrast=1.1)
    fill(img, '#ebe3cc', 61, rect=(22, 40, 98, 220), scale=10, contrast=.6, dark=.12, light=.1)
    ink = H('#1b1714')
    text(img, '鯉', 60, 86, 44, ink, SERIF, brush=True)
    for k, ch in enumerate('品評会'): text(img, ch, 82, 132 + k * 18, 14, ink, SERIF, brush=True)
    for k, ch in enumerate('賞状'): text(img, ch, 40, 140 + k * 20, 16, ink, SERIF, brush=True)
    ImageDraw.Draw(img).rectangle([px(54), px(196), px(68), px(210)], fill=H('#b8322a'))
    fill(img, '#1c120c', 62, rect=(6, 250, 114, 262), scale=4); ell(img, (2, 249, 12, 263), '#3a2a1a'); ell(img, (108, 249, 118, 263), '#3a2a1a')
    volume(img, (6, 8, 114, 262), .3, .2)
    fin(img, 'ko_scroll')


tub()
rosette('ko_rib1', '#b8322a', '#d9b048', '壱')
rosette('ko_rib2', '#2e4a86', '#c8ccd2', '弐')
rosette('ko_rib3', '#e6e0d2', '#a8703a', '参')
cup()
scroll()

# shelf pack: one row, 2 px gaps
order = ['tub', 'ko_cup', 'ko_scroll', 'ko_rib1', 'ko_rib2', 'ko_rib3']
Wt = sum(IMGS[k].width + 2 for k in order); Ht = max(IMGS[k].height for k in order)
at = Image.new('RGBA', (Wt, Ht), (0, 0, 0, 0)); x = 0; R = {}
for k in order:
    im = IMGS[k]; at.paste(im, (x, 0)); R[k] = [x, 0, im.width, im.height]; x += im.width + 2
at.save(os.path.join(ASSETS, 'items', 'atlas_ko.webp'), 'WEBP', quality=88, alpha_quality=90, method=6)
os.makedirs(sys.argv[1], exist_ok=True)
prev = Image.new('RGBA', at.size, (40, 46, 44, 255)); prev.alpha_composite(at); prev.convert('RGB').save(os.path.join(sys.argv[1], 'ko_atlas.png'))
print('atlas', at.size, os.path.getsize(os.path.join(ASSETS, 'items', 'atlas_ko.webp')))
print(json.dumps(R))
