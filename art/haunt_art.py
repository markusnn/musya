#!/usr/bin/env python3
"""«Одержимая комната»: eight small trophies the hiding yōkai drop when Musya finds them.
Same brush toolkit as art/items.py; everything goes into one atlas.
Usage: haunt_art.py <outdir>  →  <outdir>/atlas_hn.webp + prints the JS rows (id, w, h, at)."""
import json, math, random, sys
import numpy as np
from PIL import Image, ImageDraw
sys.argv = sys.argv[:2] if len(sys.argv) > 1 else [sys.argv[0], '.']
import paint as P
import items as I
from items import px, canvas, fill, volume, soft, floor_shadow, line, ell, poly, H, dk, lt

OUT = sys.argv[1]
IMGS, ROWS = [], []


def save(img, iid, anchor='b', glow=None):
    out = img.resize((P.W, P.H), Image.LANCZOS)
    a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .88
    a[..., :3] += np.random.default_rng(sum(map(ord, iid))).normal(0, 3.5, a.shape[:2])[..., None]
    IMGS.append((iid, Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')))
    r = {'id': iid, 'w': P.W, 'h': P.H, 'a': anchor}
    if glow: r['glow'] = glow
    ROWS.append(r)


def strands(img, x0, y0, n, L, col, seed, spread=1.0, w=1.2, curl=.0, a0=0.0):
    rr = random.Random(seed); d = ImageDraw.Draw(img)
    for _ in range(n):
        a = a0 + rr.uniform(-.5, .5) * spread; pts = []; x, y = x0 + rr.uniform(-6, 6), y0
        for k in range(10):
            pts.append((px(x), px(y))); a += rr.uniform(-.12, .12) + curl; x += math.sin(a) * L / 10; y += math.cos(a) * L / 10
        c = H(col); c = (min(255, c[0] + rr.randint(-14, 14)), min(255, c[1] + rr.randint(-14, 14)), min(255, c[2] + rr.randint(-14, 14)), 255)
        d.line(pts, fill=c, width=max(1, px(w)), joint='curve')


def tokkuri():   # tanuki: a borrowed sake flask with the shop mark and a tally line
    img = canvas(110, 170); floor_shadow(img, 55, 164, 42)
    fill(img, '#d8cfb8', 3, poly=[(40, 38), (70, 38), (72, 60), (96, 96), (98, 130), (86, 160), (24, 160), (12, 130), (14, 96), (38, 60)], scale=4, contrast=.6)
    fill(img, '#6a4a2a', 4, poly=[(44, 22), (66, 22), (70, 40), (40, 40)], scale=3)          # cork
    line(img, [(40, 44), (70, 44)], '#b8322a', 3)                                              # red cord
    line(img, [(70, 44), (80, 60), (78, 74)], '#b8322a', 2)
    volume(img, (12, 38, 98, 160), .7, .45, spec=.35)
    I.text(img, '酒', 55, 108, 34, '#2a1a12', brush=True)
    line(img, [(30, 140), (80, 140)], '#3a2a1a', 1.6)                                          # tally line
    save(img, 'hn_tokkuri')


def fur():       # kitsune: a tuft of white-gold fox fur tied with red thread
    img = canvas(150, 110); floor_shadow(img, 75, 104, 58, 80)
    strands(img, 40, 62, 80, 100, '#efe6d6', 3, spread=.8, w=1.6, curl=-.004, a0=1.5)
    strands(img, 40, 60, 40, 80, '#f8f2e8', 5, spread=.5, w=1.3, a0=1.45)
    strands(img, 90, 60, 36, 46, '#dcb47c', 7, spread=.6, w=1.2, a0=1.55)            # golden tips
    ell(img, (32, 48, 50, 76), '#b8322a'); line(img, [(40, 72), (30, 100)], '#b8322a', 2); line(img, [(44, 72), (54, 102)], '#b8322a', 2)
    volume(img, (10, 20, 146, 100), .4, .2)
    save(img, 'hn_fur')


def scale():     # kappa: an iridescent green scale
    img = canvas(120, 110); floor_shadow(img, 60, 104, 46, 90)
    pts = [(60, 12), (100, 36), (108, 70), (88, 98), (60, 104), (32, 98), (12, 70), (20, 36)]
    m = fill(img, '#4f8a5a', 3, poly=pts, scale=4, contrast=1.1)
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    for k in range(5):
        r = 18 + k * 16; d.arc([px(60 - r), px(104 - r * 1.2), px(60 + r), px(104 + r * .5)], 200, 340, fill=(20, 50, 30, 120), width=px(2))
    a = np.asarray(l, np.float32); a[..., 3] *= np.asarray(m, np.float32) / 255; img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))
    soft(img, lambda d: d.ellipse([px(28), px(26), px(70), px(62)], fill=(170, 230, 210, 110)), 6)
    soft(img, lambda d: d.ellipse([px(62), px(50), px(96), px(80)], fill=(150, 120, 220, 70)), 7)
    volume(img, (12, 12, 108, 104), .6, .35, spec=.6)
    save(img, 'hn_scale')


def wick():      # chōchin-obake: a burnt wick stub on a clay dish, still glowing
    img = canvas(100, 150); floor_shadow(img, 50, 144, 42)
    fill(img, '#7a4a2a', 3, poly=[(10, 124), (90, 124), (80, 142), (20, 142)], scale=4); volume(img, (10, 118, 90, 142), .6, .3)
    fill(img, '#e0d2b0', 4, poly=[(40, 92), (60, 90), (62, 126), (38, 126)], scale=3)
    line(img, [(50, 92), (48, 80), (52, 70)], '#1a1210', 2.4)
    soft(img, lambda d: d.ellipse([px(26), px(20), px(74), px(84)], fill=(255, 150, 70, 110)), 6)
    fill(img, '#ff9a48', 5, poly=[(51, 30), (60, 56), (51, 72), (42, 56)], scale=3)
    ell(img, (47, 52, 55, 70), '#fff0c8')
    save(img, 'hn_wick', glow=[50, 55])


def hair():      # rokurokubi: a long black lock tied with a white paper motoyui
    img = canvas(110, 200)
    strands(img, 55, 20, 90, 170, '#141212', 3, spread=.28, w=1.3, curl=.004)
    fill(img, '#efe9dc', 4, rect=(44, 30, 66, 52), scale=3); line(img, [(44, 36), (66, 36)], '#b8322a', 1.4); line(img, [(44, 46), (66, 46)], '#b8322a', 1.4)
    soft(img, lambda d: d.line([px(52), px(60), px(46), px(180)], fill=(160, 160, 170, 60), width=px(4)), 2)
    save(img, 'hn_hair', anchor='t')


def fluff():     # nekomata: a little ball of calico fur combed from both tails
    img = canvas(130, 110); floor_shadow(img, 65, 104, 50)
    fill(img, '#efe8dc', 3, ell=(14, 18, 116, 102), scale=5, contrast=.5)
    fill(img, '#d88a3a', 4, ell=(20, 22, 70, 70), scale=5, contrast=.8)
    fill(img, '#2a2220', 5, ell=(66, 50, 108, 92), scale=5, contrast=.8)
    for k, (cx, cy) in enumerate([(40, 40), (86, 70), (70, 30), (40, 80)]):
        strands(img, cx, cy, 16, 26, ['#f4ecdf', '#e39a4a', '#3a302a', '#f4ecdf'][k], 10 + k, spread=6, w=1)
    volume(img, (14, 18, 116, 102), .6, .4)
    save(img, 'hn_fluff')


def koma():      # zashiki-warashi: a wooden spinning top with painted rings
    img = canvas(120, 130); floor_shadow(img, 60, 124, 40)
    fill(img, '#c89a5a', 3, poly=[(12, 58), (108, 58), (96, 84), (64, 118), (56, 118), (24, 84)], scale=5, stretch=(3, 1))
    ell(img, (12, 44, 108, 72), '#d8aa68')
    for r, c in ((44, '#b8322a'), (32, '#2a4a8a'), (20, '#2f6b3a'), (9, '#d8b048')):
        soft(img, lambda d, r=r, c=c: d.ellipse([px(60 - r), px(58 - r * .28), px(60 + r), px(58 + r * .28)], outline=H(c), width=px(4)), .4)
    fill(img, '#6a4424', 4, rect=(55, 10, 65, 52), scale=3)
    line(img, [(46, 70), (74, 70)], '#b8322a', 2.5); line(img, [(40, 80), (80, 80)], '#2a4a8a', 2.5)
    volume(img, (12, 10, 108, 118), .6, .35, spec=.3)
    save(img, 'hn_koma')


def claw():      # akaname: a small red claw, the only thing it left in the tub
    img = canvas(120, 90); floor_shadow(img, 60, 84, 46, 80)
    fill(img, '#a8402e', 3, poly=[(10, 70), (30, 44), (62, 30), (96, 22), (112, 28), (92, 40), (66, 56), (44, 76), (20, 80)], scale=4, contrast=1.1)
    fill(img, '#e8d8c0', 4, poly=[(96, 22), (116, 16), (110, 30), (98, 32)], scale=3)
    line(img, [(28, 62), (62, 42), (92, 30)], '#6a1a12', 1.4)
    volume(img, (10, 16, 116, 80), .7, .4, spec=.45)
    save(img, 'hn_claw')


def pack():
    lst = sorted(IMGS, key=lambda t: -t[1].height); W = 1024; x = y = rowh = 0; pos = {}
    for iid, im in lst:
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[iid] = (x, y); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for iid, im in lst: at.paste(im, pos[iid])
    at.save(f'{OUT}/atlas_hn.webp', 'WEBP', quality=88, alpha_quality=90, method=6)
    for r in ROWS: r['at'] = ['hn', *pos[r['id']]]
    print('atlas', at.size); print(json.dumps(ROWS, ensure_ascii=False))
    prev = Image.new('RGBA', at.size, (40, 46, 42, 255)); prev.alpha_composite(at); prev.convert('RGB').save(f'{OUT}/hn_preview.png') if 'out' in OUT else None


if __name__ == '__main__':
    tokkuri(); fur(); scale(); wick(); hair(); fluff(); koma(); claw(); pack()
