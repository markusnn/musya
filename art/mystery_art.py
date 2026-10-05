#!/usr/bin/env python3
"""«Пропажа в доме» (feat/mystery.js): small floor clues the culprit leaves + four detective things.
Same brush toolkit as art/items.py / art/haunt_art.py; everything goes into one atlas.
Usage: mystery_art.py <outdir>  →  <outdir>/atlas_dt.webp + prints the JS rect map."""
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


def strands(img, x0, y0, n, L, col, seed, spread=1.0, w=1.2, curl=.0, a0=0.0, jx=6, jy=0):
    rr = random.Random(seed); d = ImageDraw.Draw(img)
    for _ in range(n):
        a = a0 + rr.uniform(-.5, .5) * spread; pts = []; x, y = x0 + rr.uniform(-jx, jx), y0 + rr.uniform(-jy, jy)
        for k in range(10):
            pts.append((px(x), px(y))); a += rr.uniform(-.12, .12) + curl; x += math.sin(a) * L / 10; y += math.cos(a) * L / 10 * .45
        c = H(col); c = (min(255, c[0] + rr.randint(-14, 14)), min(255, c[1] + rr.randint(-14, 14)), min(255, c[2] + rr.randint(-14, 14)), 255)
        d.line(pts, fill=c, width=max(1, px(w)), joint='curve')


def sheen(img, box, a=90):   # a wet glint
    soft(img, lambda d: d.ellipse([px(v) for v in box], fill=(200, 225, 235, a)), 1.5)


# ── clues: flat things lying on the floor, seen at a low angle ──
def c_wet():      # kappa: wet webbed footprints
    img = canvas(150, 70)
    for k, (cx, cy) in enumerate([(26, 50), (72, 30), (120, 46)]):
        soft(img, lambda d, cx=cx, cy=cy: d.ellipse([px(cx - 17), px(cy - 9), px(cx + 17), px(cy + 9)], fill=(30, 46, 52, 150)), 1.5)
        for j in (-1, 0, 1):   # three webbed toes
            tx, ty = cx + j * 11 + 4, cy - 12 - abs(j) * -2
            soft(img, lambda d, tx=tx, ty=ty: d.polygon([(px(cx + j * 4), px(cy - 4)), (px(tx - 5), px(ty)), (px(tx + 5), px(ty))], fill=(30, 46, 52, 150)), 1)
        sheen(img, (cx - 10, cy - 6, cx + 2, cy - 1), 110)
    for x, y in ((48, 44), (98, 40), (138, 30)):
        sheen(img, (x - 3, y - 2, x + 3, y + 2), 140)
    save(img, 'dc_wet')


def c_cuke():     # kappa: a cucumber peel spiral
    img = canvas(120, 64); floor_shadow(img, 60, 58, 46, 70)
    d = ImageDraw.Draw(img); pts = []
    for k in range(60):
        t = k / 59; a = t * 9.5; r = 8 + t * 34
        pts.append((px(60 + math.cos(a) * r), px(34 + math.sin(a) * r * .38)))
    d.line(pts, fill=H('#2f5a26'), width=px(7), joint='curve')
    d.line([(x, y - px(2)) for x, y in pts], fill=H('#6a9a48'), width=px(3), joint='curve')
    d.line([(x, y + px(2)) for x, y in pts], fill=H('#c9d89a'), width=px(1.6), joint='curve')
    volume(img, (10, 10, 110, 60), .5, .2)
    save(img, 'dc_cuke')


def c_hair():     # kitsune: a tuft of white-gold fox hair
    img = canvas(120, 56); floor_shadow(img, 60, 46, 50, 60)
    strands(img, 18, 30, 60, 90, '#efe6d6', 3, spread=.5, w=1.3, a0=1.55, jy=6)
    strands(img, 30, 30, 30, 70, '#dcb47c', 7, spread=.5, w=1.1, a0=1.6, jy=5)
    strands(img, 80, 30, 18, 30, '#f8f2e8', 9, spread=.4, w=1, a0=1.5, jy=4)
    save(img, 'dc_hair')


def c_rice():     # kitsune: spilled rice and a bit of fried tofu (Inari's offering)
    img = canvas(110, 56); rr = random.Random(4)
    fill(img, '#c08a3a', 3, poly=[(58, 22), (86, 18), (92, 34), (64, 40)], scale=3, contrast=1.2); volume(img, (58, 18, 92, 40), .6, .3)
    for _ in range(70):
        x = rr.gauss(46, 20); y = rr.gauss(36, 7); a = rr.uniform(0, math.pi)
        ell(img, (x - 2.6, y - 1.4, x + 2.6, y + 1.4), (236, 232, 218, 255) if rr.random() > .2 else (210, 206, 190, 255))
    save(img, 'dc_rice')


def c_leaf():     # tanuki: the leaf it wears on its head to change shape
    img = canvas(96, 64); floor_shadow(img, 48, 56, 36, 60)
    pts = [(8, 40), (30, 22), (60, 14), (88, 18), (70, 34), (44, 48), (20, 50)]
    fill(img, '#7a8a3a', 3, poly=pts, scale=3, contrast=1.1)
    fill(img, '#b8862e', 4, poly=[(60, 14), (88, 18), (70, 34), (58, 30)], scale=3)
    line(img, [(4, 46), (20, 42), (50, 30), (84, 19)], '#3a3a18', 1.6)
    for x in (30, 46, 62):
        line(img, [(x, 36 - (x - 30) * .3), (x - 6, 26 - (x - 30) * .3)], '#4a4a20', .9); line(img, [(x, 36 - (x - 30) * .3), (x + 2, 46 - (x - 30) * .3)], '#4a4a20', .9)
    volume(img, (4, 12, 92, 52), .5, .25, spec=.15)
    save(img, 'dc_leaf')


def c_paw():      # tanuki: round muddy paw prints
    img = canvas(150, 70)
    for cx, cy in ((24, 48), (66, 28), (108, 50), (140, 30)):
        if cx > 135: cx = 136
        soft(img, lambda d, cx=cx, cy=cy: d.ellipse([px(cx - 10), px(cy - 5), px(cx + 10), px(cy + 7)], fill=(58, 40, 26, 190)), 1)
        for j in (-1.5, -.5, .5, 1.5):
            tx, ty = cx + j * 7, cy - 10 + abs(j) * 2
            soft(img, lambda d, tx=tx, ty=ty: d.ellipse([px(tx - 3.4), px(ty - 2.4), px(tx + 3.4), px(ty + 2.4)], fill=(58, 40, 26, 190)), .8)
    save(img, 'dc_paw')


def c_sake():     # a tipped sake cup and a little spill
    img = canvas(110, 64)
    soft(img, lambda d: d.ellipse([px(30), px(36), px(104), px(58)], fill=(150, 170, 175, 90)), 2); sheen(img, (56, 40, 84, 46), 120)
    fill(img, '#e8e0cc', 3, poly=[(14, 24), (40, 14), (52, 40), (26, 52)], scale=3, contrast=.6)
    ell(img, (36, 14, 56, 42), '#cfc4ac'); ell(img, (40, 18, 52, 38), '#5a4a3a')
    line(img, [(18, 30), (44, 20)], '#2a4a8a', 2)
    volume(img, (12, 12, 56, 52), .6, .3, spec=.35)
    save(img, 'dc_sake')


def c_thread():   # a red silk thread
    img = canvas(116, 52); d = ImageDraw.Draw(img); pts = []
    for k in range(80):
        t = k / 79; pts.append((px(8 + t * 100 + 8 * math.sin(t * 13)), px(28 + 12 * math.sin(t * 7.3) * (1 - t * .4) + 5 * math.cos(t * 19))))
    d.line(pts, fill=(120, 16, 14, 255), width=px(2.6), joint='curve'); d.line(pts, fill=(206, 50, 40, 255), width=px(1.4), joint='curve')
    save(img, 'dc_thread')


def c_bell():     # nekomata: a tiny brass suzu with a red cord
    img = canvas(76, 64); floor_shadow(img, 40, 58, 28, 90)
    line(img, [(8, 40), (20, 30), (34, 30)], '#b8322a', 2.2)
    fill(img, '#c9a24a', 3, ell=(24, 18, 62, 56), scale=3, contrast=.8)
    line(img, [(30, 42), (56, 42)], '#5a4218', 1.6); ell(img, (40, 44, 46, 52), '#3a2a10')
    volume(img, (24, 18, 62, 56), .7, .4, spec=.7)
    save(img, 'dc_bell')


def c_fur2():     # nekomata: black and white hair from two tails
    img = canvas(110, 52)
    strands(img, 16, 26, 36, 80, '#1e1a18', 3, spread=.5, w=1.2, a0=1.6, jy=5)
    strands(img, 26, 28, 34, 70, '#f0eadf', 5, spread=.5, w=1.2, a0=1.5, jy=5)
    save(img, 'dc_fur2')


def c_bone():     # nekomata: a fish skeleton licked clean
    img = canvas(116, 52); floor_shadow(img, 58, 44, 46, 50)
    line(img, [(14, 28), (96, 26)], '#e6ddc8', 2.4)
    for k in range(9):
        x = 26 + k * 8; h = 11 - abs(k - 4) * 1.2
        line(img, [(x, 27), (x - 4, 27 - h)], '#ddd2bc', 1.2); line(img, [(x, 27), (x - 4, 27 + h)], '#ddd2bc', 1.2)
    poly(img, [(96, 26), (110, 14), (106, 27), (110, 40)], '#d8ccb4')
    fill(img, '#d8ccb4', 3, poly=[(4, 28), (16, 18), (22, 28), (16, 38)], scale=3); ell(img, (9, 25, 13, 29), '#2a2018')
    save(img, 'dc_bone')


def c_slick():    # akaname: a glistening lick streak on the boards
    img = canvas(150, 50)
    soft(img, lambda d: d.line([(px(10), px(30)), (px(50), px(24)), (px(100), px(28)), (px(140), px(20))], fill=(170, 200, 190, 80), width=px(12), joint='curve'), 2.5)
    soft(img, lambda d: d.line([(px(16), px(28)), (px(50), px(22)), (px(98), px(26)), (px(134), px(20))], fill=(235, 245, 240, 120), width=px(3), joint='curve'), 1)
    for x, y in ((40, 23), (86, 25), (122, 21)): sheen(img, (x - 4, y - 2, x + 4, y + 2), 200)
    save(img, 'dc_slick')


def c_paper():    # chōchin-obake: a torn, oily scrap of lantern paper
    img = canvas(96, 60); floor_shadow(img, 48, 54, 38, 60)
    pts = [(8, 30), (26, 14), (52, 10), (70, 18), (88, 14), (80, 36), (60, 50), (30, 50), (14, 44)]
    fill(img, '#d9c9a0', 3, poly=pts, scale=3, contrast=.8)
    soft(img, lambda d: d.ellipse([px(40), px(22), px(70), px(42)], fill=(150, 110, 50, 110)), 3)
    line(img, [(18, 24), (84, 22)], '#5a3a20', 1.4); line(img, [(16, 40), (76, 38)], '#5a3a20', 1.2)
    I.text(img, '灯', 32, 32, 18, '#8a1e18', brush=True)
    volume(img, (8, 10, 88, 50), .4, .2)
    save(img, 'dc_paper')


def c_wax():      # drips of candle wax and a burnt matchstick-like wick
    img = canvas(96, 52)
    for x, y, r in ((24, 30, 9), (46, 36, 6), (64, 26, 8), (80, 38, 5)):
        soft(img, lambda d, x=x, y=y, r=r: d.ellipse([px(x - r), px(y - r * .55), px(x + r), px(y + r * .55)], fill=(240, 228, 196, 255)), .6)
        sheen(img, (x - r * .5, y - r * .4, x, y - r * .1), 150)
    line(img, [(30, 14), (54, 20)], '#1a1210', 2); ell(img, (52, 17, 57, 22), '#ff8a3a')
    save(img, 'dc_wax')


def c_otedama():  # zashiki-warashi: a little bean bag
    img = canvas(76, 62); floor_shadow(img, 38, 56, 30, 90)
    fill(img, '#b8322a', 3, ell=(10, 14, 66, 56), scale=3, contrast=.8)
    fill(img, '#e8d8b0', 4, poly=[(38, 14), (66, 30), (52, 54), (38, 40)], scale=3)
    for x, y in ((24, 26), (30, 40), (52, 30), (46, 44)): ell(img, (x - 2, y - 2, x + 2, y + 2), '#f2e6c0')
    line(img, [(38, 14), (38, 40), (24, 54)], '#5a1a12', 1)
    volume(img, (10, 14, 66, 56), .7, .45, spec=.25)
    save(img, 'dc_otedama')


def c_bead():     # zashiki-warashi: glass ohajiki chips
    img = canvas(90, 46)
    for x, y, c in ((18, 26, (120, 190, 220)), (42, 18, (230, 140, 160)), (60, 30, (150, 210, 150)), (78, 20, (230, 210, 120))):
        soft(img, lambda d, x=x, y=y, c=c: d.ellipse([px(x - 9), px(y - 5), px(x + 9), px(y + 5)], fill=c + (190,)), .6)
        sheen(img, (x - 6, y - 4, x - 1, y - 1), 220)
    save(img, 'dc_bead')


# ── rewards: the detective's things (category «Дела детектива») ──
def i_loupe():    # a brass magnifier resting on a little wooden stand
    img = canvas(140, 180); floor_shadow(img, 70, 172, 56)
    fill(img, '#6a4424', 3, poly=[(28, 150), (112, 150), (120, 172), (20, 172)], scale=4, stretch=(3, 1)); volume(img, (20, 150, 120, 172), .6, .3)
    fill(img, '#5a3a1e', 4, rect=(64, 104, 76, 152), scale=3)
    fill(img, '#a8782e', 5, poly=[(62, 100), (78, 100), (74, 120), (66, 120)], scale=3)
    ell(img, (18, 8, 122, 108), '#b88a36'); ell(img, (26, 16, 114, 100), '#2a3640')
    soft(img, lambda d: d.ellipse([px(30), px(20), px(110), px(96)], fill=(120, 150, 160, 120)), 4)
    soft(img, lambda d: d.ellipse([px(40), px(28), px(70), px(52)], fill=(240, 248, 255, 170)), 3)
    volume(img, (18, 8, 122, 108), .6, .3, spec=.3)
    save(img, 'dt_loupe')


def i_note():     # the detective's notebook with a brush
    img = canvas(170, 110); floor_shadow(img, 85, 104, 76)
    fill(img, '#3a4a5a', 3, poly=[(14, 60), (120, 40), (160, 70), (52, 96)], scale=4)
    fill(img, '#efe6d0', 4, poly=[(20, 58), (118, 39), (152, 64), (52, 88)], scale=4, contrast=.5)
    for k in range(5):
        t = k / 5; line(img, [(40 + t * 60, 56 - t * 12), (66 + t * 60, 78 - t * 12)], '#2a2220', 1)
    I.text(img, '探', 90, 60, 20, '#8a1e18', brush=True)
    fill(img, '#c9a24a', 5, poly=[(30, 96), (140, 30), (146, 36), (36, 102)], scale=3)
    poly(img, [(140, 30), (156, 20), (150, 34)], '#1a1210')
    volume(img, (14, 20, 160, 104), .5, .25)
    save(img, 'dt_note')


def i_jitte():    # an Edo-period okappiki's jitte with a red tassel on a small stand
    img = canvas(110, 230); floor_shadow(img, 55, 222, 44)
    fill(img, '#4a2e1a', 3, poly=[(18, 200), (92, 200), (98, 222), (12, 222)], scale=4, stretch=(3, 1)); volume(img, (12, 200, 98, 222), .6, .3)
    fill(img, '#7a8088', 4, poly=[(50, 18), (60, 18), (61, 150), (49, 150)], scale=3, stretch=(1, 4))
    fill(img, '#7a8088', 5, poly=[(61, 120), (74, 116), (76, 70), (70, 66), (68, 112), (61, 112)], scale=3)
    fill(img, '#2a1a12', 6, rect=(47, 148, 63, 200), scale=3)
    for y in range(152, 198, 6): line(img, [(47, y), (63, y + 3)], '#6a4424', 1.2)
    line(img, [(55, 200), (40, 214)], '#b8322a', 2); fill(img, '#b8322a', 7, poly=[(36, 210), (46, 210), (50, 228), (32, 228)], scale=3)
    volume(img, (40, 16, 80, 200), .7, .45, spec=.5)
    save(img, 'dt_jitte')


def i_gando():    # gandō-chōchin: a copper lantern that shines only forward
    img = canvas(140, 190); floor_shadow(img, 70, 182, 56)
    fill(img, '#8a5a2e', 3, rect=(30, 40, 110, 176), scale=4, stretch=(1, 3), contrast=.9)
    ell(img, (30, 30, 110, 54), '#a06a38'); ell(img, (30, 164, 110, 186), '#6a4424')
    fill(img, '#4a2e1a', 4, rect=(64, 8, 76, 34), scale=3); line(img, [(50, 14), (90, 14)], '#3a2414', 3)
    soft(img, lambda d: d.ellipse([px(36), px(78), px(104), px(146)], fill=(255, 180, 90, 200)), 6)
    ell(img, (46, 88, 94, 136), '#ffd890'); ell(img, (58, 100, 82, 124), '#fff4d8')
    for y in (60, 156): line(img, [(30, y), (110, y)], '#5a3a1e', 2)
    volume(img, (30, 30, 110, 186), .6, .4, spec=.25)
    save(img, 'dt_gando', glow=[70, 112])


def pack():
    lst = sorted(IMGS, key=lambda t: -t[1].height); W = 1024; x = y = rowh = 0; pos = {}
    for iid, im in lst:
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[iid] = (x, y); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for iid, im in lst: at.paste(im, pos[iid])
    at.save(f'{OUT}/atlas_dt.webp', 'WEBP', quality=88, alpha_quality=90, method=6)
    print('atlas', at.size)
    print(json.dumps({r['id']: [*pos[r['id']], r['w'], r['h']] + ([r['glow']] if r.get('glow') else []) for r in ROWS}, ensure_ascii=False, separators=(',', ':')))
    prev = Image.new('RGBA', at.size, (40, 46, 42, 255)); prev.alpha_composite(at)
    prev.convert('RGB').resize((at.width * 2, at.height * 2), Image.LANCZOS).save('art/out/dt_preview.png')


if __name__ == '__main__':
    for f in (c_wet, c_cuke, c_hair, c_rice, c_leaf, c_paw, c_sake, c_thread, c_bell, c_fur2, c_bone, c_slick, c_paper, c_wax, c_otedama, c_bead,
              i_loupe, i_note, i_jitte, i_gando): f()
    pack()
