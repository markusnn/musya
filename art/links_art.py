#!/usr/bin/env python3
"""«Всё связано» (links between add-ons): small pictures for the new connections.
  assets/items/atlas_ws2.webp — 3 new workshop things (feat/workshop.js): нэко-цугура, варадзи, глиняный манэки-нэко
  assets/items/atlas_ri2.webp — the dish «Тядзукэ из своего риса» (feat/rice.js, FATL.ri2)
Reuses the painting helpers of art/workshop_art.py. Prints both rect maps. Previews → art/out/atlas_ws2.png, atlas_ri2.png."""
import json, math, os, random, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'assets')
sys.path.insert(0, HERE)
import workshop_art as WA                     # sets argv for items.py and gives done(), arc(), paw()
from workshop_art import I, done, arc
from items import px, fill, volume, line, ell, poly, soft, floor_shadow, dk, lt, H
from paint import mixc


def dome(cx, base, rx, top, n=40, bulge=.12):
    pts = []
    for k in range(n + 1):
        t = math.pi * k / n; s = math.sin(t)
        pts.append((cx + rx * math.cos(t) * (1 + bulge * s * (1 - s)), base - (base - top) * s ** .8))
    return pts


# ── нэко-цугура: a woven rice-straw cat house (Niigata), coiled rings + stitches, round door, a red cushion inside
def i_tsugura():
    img = I.canvas(200, 170); floor_shadow(img, 100, 164, 92); s = H('#c9a356'); rnd = random.Random(21)
    pts = dome(100, 162, 88, 16)
    fill(img, s, 1, poly=pts, scale=3, contrast=.8, dark=.35, light=.25)
    for k in range(1, 16):                                                      # coils
        f = k / 16; y = 162 - (162 - 16) * f ** 1.05; w = 88 * math.sqrt(max(0, 1 - f ** 1.6)) * 1.02
        line(img, [(100 - w, y), (100 + w, y)], dk(s, .32), 1.2)
        for j in range(int(w / 7)):                                             # binding stitches
            x = 100 - w + 6 + j * 14 + (k % 2) * 7
            if x < 100 + w - 4: line(img, [(x - 2, y - 4.5), (x + 2, y + .5)], mixc(dk(s, .45), H('#7a5a26'), rnd.random()), 1.1)
    volume(img, (12, 14, 188, 164), .55, .38, spec=.08)
    fill(img, '#160e08', 2, ell=(64, 70, 136, 146), scale=2)                    # the door
    fill(img, "#a8323a", 3, ell=(74, 124, 126, 146), scale=2); volume(img, (74, 124, 126, 146), .5, .3)   # the cushion inside
    arc(img, (60, 66, 140, 150), 180, 360, lt(s, .15), 5); arc(img, (60, 66, 140, 150), 0, 180, dk(s, .1), 4)
    for k in range(10):
        a = math.pi + k * math.pi / 9; x, y = 100 + 40 * math.cos(a), 108 + 42 * math.sin(a); line(img, [(x - 2, y - 3), (x + 2, y + 3)], dk(s, .45), 1)
    line(img, [(92, 18), (100, 6), (108, 18)], dk(s, .2), 2.2)                # the knot on top
    return done(img)


# ── варадзи: a pair of rice-straw sandals seen from above at an angle, red cloth thongs
def i_waraji():
    img = I.canvas(168, 112); s = H('#cfae62')
    floor_shadow(img, 84, 104, 74, 90)
    for cx, cy, rot, sd in ((54, 60, -.16, 4), (114, 54, .12, 5)):
        c, sn = math.cos(rot), math.sin(rot)
        R = lambda x, y, cx=cx, cy=cy, c=c, sn=sn: (cx + x * c - y * sn, cy + x * sn + y * c)
        sole = [R(24 * math.cos(t) * (1 - .12 * math.sin(t)), 44 * math.sin(t)) for t in [k * math.pi * 2 / 32 for k in range(32)]]
        fill(img, s, sd, poly=sole, scale=2, contrast=.8)
        for k in range(-8, 9):                                                  # woven rows
            y = k * 5; w = 24 * math.sqrt(max(0, 1 - (y / 44) ** 2)) - 2
            line(img, [R(-w, y), R(w, y)], dk(s, .3), 1)
        line(img, [R(0, -42), R(0, 42)], dk(s, .22), 1.4)
        volume(img, (cx - 30, cy - 48, cx + 30, cy + 48), .45, .3)
        red = H('#b8322a')
        line(img, [R(0, -40), R(0, -20)], red, 3.2)                             # the thong from the toe
        line(img, [R(-23, -4), R(-6, -18), R(0, -20), R(6, -18), R(23, -4)], red, 2.6)
        for sx in (-1, 1): ell(img, (R(sx * 24, -4)[0] - 3, R(sx * 24, -4)[1] - 3, R(sx * 24, -4)[0] + 3, R(sx * 24, -4)[1] + 3), dk(s, .35))
        line(img, [R(-24, 14), R(-10, 30), R(10, 30), R(24, 14)], mixc(s, H('#8a6a2a'), .5), 2)   # heel rope
    return done(img)


# ── глиняный манэки-нэко: a white clay beckoning cat with a raised paw, red collar, a bell and a gold koban
def i_maneki():
    img = I.canvas(124, 168); w = H('#ece4d4'); floor_shadow(img, 62, 162, 44)
    fill(img, w, 1, poly=[(26, 160), (22, 120), (32, 86), (62, 74), (92, 86), (102, 120), (98, 160)], scale=3, contrast=.5)
    volume(img, (20, 74, 104, 162), .55, .35, spec=.12)
    fill(img, w, 2, poly=[(80, 100), (96, 96), (118, 52), (100, 44)], scale=2, contrast=.4)                    # raised arm
    fill(img, w, 2, ell=(96, 22, 122, 56), scale=2, contrast=.4); volume(img, (96, 22, 122, 56), .5, .3, spec=.1)   # its paw
    for k in range(3): line(img, [(102 + k * 6, 25), (102 + k * 6, 31)], dk(w, .3), .9)
    ell(img, (104, 34, 116, 44), '#e8a0a0')
    fill(img, w, 3, ell=(24, 18, 100, 86), scale=3, contrast=.4); volume(img, (24, 18, 100, 86), .5, .3, spec=.15)  # head
    for sd in (-1, 1):
        poly(img, [(62 + sd * 18, 28), (62 + sd * 36, 6), (62 + sd * 38, 40)], w); poly(img, [(62 + sd * 22, 28), (62 + sd * 33, 14), (62 + sd * 34, 34)], '#e09a9a')
    fill(img, '#c87a3a', 4, ell=(30, 20, 56, 44), scale=2); fill(img, '#2a2420', 5, ell=(70, 24, 88, 38), scale=2)      # calico patches
    for x in (48, 76): arc(img, (x - 7, 48, x + 7, 58), 200, 340, '#1a1410', 1.6)
    poly(img, [(59, 60), (65, 60), (62, 64)], '#d07070'); arc(img, (55, 62, 62, 69), 0, 150, '#1a1410', 1); arc(img, (62, 62, 69, 69), 30, 180, '#1a1410', 1)
    for sd in (-1, 1):
        for k in (-1, 1): line(img, [(62 + sd * 12, 64 + k * 2), (62 + sd * 32, 62 + k * 5)], '#6a5a4a', .6)
    line(img, [(32, 86), (62, 92), (92, 86)], '#b8322a', 5)                     # collar + bell
    fill(img, '#d8a83a', 6, ell=(55, 88, 69, 102), scale=1); ell(img, (58, 90, 63, 94), '#f4dc8a'); line(img, [(57, 96), (67, 96)], '#7a5a1a', .8)
    fill(img, '#d6b04a', 7, ell=(40, 108, 84, 146), scale=2); ell(img, (46, 112, 60, 122), '#ecd48a')          # koban
    for y in (116, 124, 132, 140): line(img, [(48, y), (76, y)], '#9a7a2a', .8)
    ell(img, (32, 128, 50, 146), w); ell(img, (74, 128, 92, 146), w)            # front paws on the coin
    return done(img)


# ── тядзукэ: rice under green tea in a brown bowl, nori strips, an umeboshi, a mitsuba leaf
def d_chazuke():
    img = I.canvas(140, 96); b = H('#5a3a28')
    floor_shadow(img, 70, 90, 50, 120)
    fill(img, b, 1, poly=[(8, 34)] + [(70 + 62 * math.cos(t), 34 + 50 * math.sin(t)) for t in [k * math.pi / 20 for k in range(21)]], scale=3, contrast=.8)
    fill(img, dk(b, .2), 2, rect=(50, 80, 90, 90), scale=2)
    volume(img, (8, 30, 132, 90), .5, .4, spec=.1)
    for k in range(3): arc(img, (20 + k * 2, 40 + k * 8, 120 - k * 2, 70 + k * 8), 20, 160, lt(b, .18), 1)
    ell(img, (8, 22, 132, 46), lt(b, .25)); fill(img, '#b8b47a', 3, ell=(12, 24, 128, 44), scale=2, contrast=.5)      # tea
    soft(img, lambda d: d.ellipse([px(30), px(26), px(110), px(42)], fill=(230, 232, 190, 90)), 3)
    fill(img, '#f2eee2', 4, ell=(38, 16, 104, 40), scale=1, contrast=1.3, dark=.25); volume(img, (38, 16, 104, 40), .5, .2)   # rice
    rnd = random.Random(5)
    for _ in range(26):
        x, y = rnd.uniform(42, 100), rnd.uniform(19, 37); ell(img, (x - 2.2, y - 1.2, x + 2.2, y + 1.2), (250, 248, 240, 255))
    for x, y, a in ((52, 22, .4), (62, 18, -.2), (78, 20, .3), (88, 26, -.5), (70, 28, .1)):
        poly(img, [(x - 7 * math.cos(a), y - 7 * math.sin(a) - 1.6), (x + 7 * math.cos(a), y + 7 * math.sin(a) - 1.6), (x + 7 * math.cos(a), y + 7 * math.sin(a) + 1.6), (x - 7 * math.cos(a), y - 7 * math.sin(a) + 1.6)], '#1e2a1c')
    fill(img, '#b8323a', 6, ell=(66, 8, 84, 24), scale=1); volume(img, (66, 8, 84, 24), .5, .3, spec=.35)               # umeboshi
    WA.leaf(img, 94, 16, 14, -.5, '#5f9a3a', 7); WA.leaf(img, 100, 22, 12, .4, '#6aa040', 8)
    for _ in range(8):
        x, y = rnd.uniform(46, 98), rnd.uniform(20, 36); ell(img, (x - .9, y - .6, x + .9, y + .6), '#e8dcb0')
    return done(img)


def pack(ims, W, name):
    x = y = rowh = 0; pos = {}
    for iid, im in sorted(ims, key=lambda t: -t[1].height):
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[iid] = (x, y, im.width, im.height); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for iid, im in ims: at.paste(im, pos[iid][:2])
    at.save(os.path.join(ASSETS, 'items', 'atlas_%s.webp' % name), 'WEBP', quality=88, alpha_quality=92, method=6)
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    pv = Image.new('RGBA', at.size, (34, 30, 28, 255)); pv.alpha_composite(at); pv.convert('RGB').save(os.path.join(HERE, 'out', 'atlas_%s.png' % name))
    return {'size': list(at.size), 'r': {k: list(v) for k, v in pos.items()}}


if __name__ == '__main__':
    ws = pack([('ws_tsugura', i_tsugura()), ('ws_waraji', i_waraji()), ('ws_maneki', i_maneki())], 500, 'ws2')
    ri = pack([('ds_ri_chazuke', d_chazuke())], 140, 'ri2')
    print(json.dumps({'ws2': ws, 'ri2': ri}, separators=(',', ':')))
