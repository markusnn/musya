#!/usr/bin/env python3
"""«Рёкан для ёкаев» (feat/ryokan.js): three futons (each = back part: mattress + pillow, front part: the comforter that
covers the sleeping guest), the standing lantern sign «宿» for the gate and six gifts «Подарки постояльцев» —
everything packed into ONE atlas assets/items/atlas_ry.webp. Prints the rect map as JSON (pasted into feat/ryokan.js).
Preview → art/out/atlas_ry.png.   Usage: ryokan_art.py [assets dir]"""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw
ASSETS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'assets')
sys.argv = [sys.argv[0], os.path.join(os.path.dirname(__file__), 'out')]     # items.py reads its out dir from argv[1]
import paint as P
from paint import hexc, mixc
import items as I
from items import px, fill, volume, line, ell, poly, text, soft, floor_shadow, dk, lt, H, mask_poly

FW, FH = 380, 180          # futon sprite (both parts share the rect); the guest stands at (190, 146)


def done(img):
    out = img.resize((P.W, P.H), Image.LANCZOS); a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .86; a[..., :3] += np.random.default_rng(17).normal(0, 3.2, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def overlay(img, m, draw, alpha=.85):
    """draw a pattern on its own layer and keep it only inside mask m"""
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); draw(ImageDraw.Draw(l), l)
    a = np.asarray(l, np.float32); a[..., 3] *= np.asarray(m, np.float32) / 255 * alpha; img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))


def crane(d, x, y, s, col, rnd):
    """a flying crane: wide white wings with dark tips, long neck forward, red cap, legs trailing"""
    a = rnd.uniform(-.2, .2); c, sn = math.cos(a), math.sin(a)
    R = lambda u, v: (px(x + (u * c - v * sn) * s), px(y + (u * sn + v * c) * s))
    d.polygon([R(-12, 0), R(2, -4), R(12, -1), R(2, 4)], fill=col)                              # body
    d.polygon([R(-4, -2), R(-20, -22), R(-6, -18), R(6, -3)], fill=col)                         # back wing
    d.polygon([R(-2, -2), R(-6, -24), R(10, -22), R(8, -2)], fill=col)                          # front wing
    d.polygon([R(-20, -22), R(-14, -22), R(-11, -19)], fill=(30, 26, 24, 230))                  # dark wing tips
    d.polygon([R(-6, -24), R(2, -24), R(0, -21)], fill=(30, 26, 24, 230))
    d.line([R(10, -1), R(18, -7), R(26, -8)], fill=col, width=max(1, px(2.2 * s / 1.4)))        # neck
    d.line([R(-12, 1), R(-24, 5)], fill=(30, 26, 24, 230), width=max(1, px(1.2 * s / 1.4)))     # legs
    cx, cy = R(24, -9); r = px(2 * s); d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(196, 40, 36, 255))


KIND = {   # mattress, comforter, pattern colour, roll (fold band) colour
    'simple': ('#cfc8b6', '#2c3f62', '#dcd6c8', '#d8d1c2'),
    'down':   ('#d6c6b2', '#c9a491', '#ecdcc8', '#efe4d2'),
    'crane':  ('#d2cab8', '#7a2a2c', '#efe8da', '#d9cdb4'),
}


def futon_back(kind):
    mat, *_ = KIND[kind]; img = I.canvas(FW, FH)
    floor_shadow(img, 190, 166, 186, 120)
    top = [(48, 64), (332, 64), (374, 150), (6, 150)]
    fill(img, mat, 3, poly=top, scale=16, stretch=(3, 1), contrast=.7, dark=.3, light=.15)
    edge = [(6, 150), (374, 150), (370, 166), (10, 166)]
    fill(img, dk(H(mat), .35), 4, poly=edge, scale=10, stretch=(4, .5), contrast=.6)
    if kind == 'simple':      # thin indigo stripes along the mattress sides
        m = mask_poly(img, poly=top)
        overlay(img, m, lambda d, l: [d.line([(px(x0), px(150)), (px(x1), px(64))], fill=H('#3a4a6a'), width=px(2)) for x0, x1 in ((34, 70), (44, 78), (346, 310), (336, 302))], .55)
    volume(img, (6, 64, 374, 166), .35, .25)
    # pillow (buckwheat makura) at the far end, white cover with a coloured band
    pc = {'simple': '#efe9dc', 'down': '#f2e8dc', 'crane': '#ece4d4'}[kind]
    pl = Image.new('RGBA', img.size, (0, 0, 0, 0))                     # pillow on its own layer: volume must not darken the mattress
    soft(img, lambda d: d.ellipse([px(140), px(66), px(244), px(84)], fill=(0, 0, 0, 70)), 3)
    fill(pl, pc, 5, ell=(138, 38, 242, 80), scale=6, contrast=.6, dark=.25)
    band = {'simple': '#3a4a6a', 'down': '#c98f84', 'crane': '#8a3030'}[kind]
    m = mask_poly(pl, ell=(138, 38, 242, 80)); overlay(pl, m, lambda d, l: d.rectangle([px(180), px(34), px(200), px(84)], fill=H(band)), .9)
    volume(pl, (138, 38, 242, 80), .55, .35, spec=.12); img.alpha_composite(pl)
    return done(img)


def futon_front(kind):
    _, cf, pat, roll = KIND[kind]; img = I.canvas(FW, FH); rnd = random.Random(kind)
    puff = 1.25 if kind == 'down' else 1.0
    # comforter: a lap mound in the middle (where the guest sits), draping over the front edge
    top = [(26 + (354 - 26) * k / 20, 110 - 36 * puff * math.sin(math.pi * k / 20) ** 1.5) for k in range(21)]
    body = top + [(380, 160), (376, 176), (4, 176), (0, 160)]
    m = fill(img, cf, 7, poly=body, scale=14, stretch=(2.5, 1), contrast=.85, dark=.35, light=.2)
    if kind == 'simple':     # indigo cotton with white kasuri marks and stripes
        def dr(d, l):
            for x in range(0, 390, 26): d.line([(px(x), px(176)), (px(x + 6 + (x - 190) * .12), px(70))], fill=H(pat), width=px(1.6))
            for _ in range(60):
                x, y = rnd.uniform(8, 372), rnd.uniform(84, 172); d.line([(px(x - 3), px(y)), (px(x + 3), px(y))], fill=H(pat), width=px(1.4))
        overlay(img, m, dr, .7)
    elif kind == 'down':     # plump peach silk with pale plum blossoms and quilting
        def dr(d, l):
            for _ in range(16):
                x, y = rnd.uniform(20, 360), rnd.uniform(96, 168)
                for p in range(5):
                    a = p / 5 * math.tau; d.ellipse([px(x + math.cos(a) * 4.5 - 4), px(y + math.sin(a) * 3.6 - 3.4), px(x + math.cos(a) * 4.5 + 4), px(y + math.sin(a) * 3.6 + 3.4)], fill=H(pat))
                d.ellipse([px(x - 1.6), px(y - 1.6), px(x + 1.6), px(y + 1.6)], fill=H('#b8625a'))
            for x in (95, 190, 285): d.line([(px(x), px(176)), (px(x + (x - 190) * .1), px(80))], fill=dk(H(cf), .25), width=px(1.4))
        overlay(img, m, dr, .8)
    else:                    # deep red silk: white cranes over gold clouds
        def dr(d, l):
            for _ in range(7):
                x, y = rnd.uniform(20, 360), rnd.uniform(100, 170); w = rnd.uniform(26, 44)
                for k in range(3): d.ellipse([px(x + k * w * .3 - w * .3), px(y - 5 - (k % 2) * 3), px(x + k * w * .3 + w * .2), px(y + 4)], fill=(200, 160, 72, 200))
            for x, y, s in ((84, 124, 1.5), (176, 150, 1.4), (262, 112, 1.6), (322, 160, 1.3), (40, 164, 1.1)): crane(d, x, y, s, H(pat), rnd)
        overlay(img, m, dr, .92)
    # the folded-back top edge: a light roll along the mound
    rl = top + [(p[0], p[1] + 14) for p in top[::-1]]
    fill(img, roll, 9, poly=rl, scale=8, stretch=(4, .6), contrast=.6, dark=.2)
    volume(img, (0, 70, 380, 178), .45, .3)
    d = ImageDraw.Draw(img); d.line([(px(x), px(y + 14)) for x, y in top], fill=dk(H(roll), .35), width=px(1.2))
    soft(img, lambda dd: dd.polygon([(px(4), px(172)), (px(376), px(172)), (px(372), px(180)), (px(8), px(180))], fill=(0, 0, 0, 90)), 2)
    return done(img)


def sign():
    """a standing lantern signboard (andon kanban) with «宿»: wooden legs, a little roof, paper panel"""
    img = I.canvas(130, 290); floor_shadow(img, 65, 284, 58)
    fr = '#2a1c12'
    fill(img, '#efd49a', 5, rect=(20, 58, 110, 236), scale=6, contrast=.8)
    volume(img, (20, 58, 110, 236), .15, .45)
    d = ImageDraw.Draw(img)
    for x in (14, 110): d.rectangle([px(x), px(46), px(x + 7), px(288)], fill=H(fr))
    for y in (52, 236): d.rectangle([px(12), px(y), px(119), px(y + 7)], fill=H(fr))
    d.rectangle([px(20), px(258), px(110), px(263)], fill=H(fr))
    text(img, '宿', 65, 132, 62, '#2a1208', I.SERIF, brush=True)
    text(img, '御', 65, 76, 18, '#5a2a14', I.SERIF)
    ell(img, (50, 188, 80, 218), '#a8322a'); text(img, '猫', 65, 203, 16, '#f2e2c8', I.SERIF)     # a red seal: the cat's inn
    fill(img, '#3a2a1e', 6, poly=[(2, 50), (65, 24), (128, 50), (122, 56), (65, 32), (8, 56)], scale=4, stretch=(3, .4), contrast=1.2)
    volume(img, (2, 24, 128, 288), .25, .15)
    return done(img)


# ───────────── gifts «Подарки постояльцев» ─────────────
def g_noren():
    img = I.canvas(210, 180)
    line(img, [(4, 12), (206, 12)], '#5a4030', 7)
    for x in (6, 202): ell(img, (x - 6, 6, x + 6, 18), '#3a2a20')
    for k in range(3):
        x0 = 12 + k * 63; fill(img, '#2c3a5a', 20 + k, rect=(x0, 16, x0 + 60, 170 - (k % 2) * 6), scale=8, stretch=(.4, 3), contrast=.8)
        volume(img, (x0, 16, x0 + 60, 170), .35, .2)
    text(img, '宿', 105, 92, 74, '#e9e2d2', I.SERIF, brush=True)
    for k in range(1, 3): line(img, [(12 + k * 63 - 1.5, 18), (12 + k * 63 - 1.5, 170)], '#141a28', 2.5)
    return 'ry_noren', done(img), 't'


def g_chochin():
    img = I.canvas(120, 200); col = H('#d8cdb2')
    line(img, [(60, 0), (60, 22)], '#120c09', 2)
    top, bot = 28, 186
    m = Image.fromarray(np.maximum(np.asarray(mask_poly(img, ell=(8, top + 6, 112, bot - 6))), np.asarray(mask_poly(img, rect=(26, top, 94, bot)))))
    fill(img, col, 31, mask=m, scale=5, contrast=1.0, dark=.3, light=.25)
    a = np.asarray(img, np.float32)
    for k in range(1, 12): yk = px(top + (bot - top) * k / 12); a[max(0, yk - 1):yk + 1, :, :3] *= .6
    img = Image.fromarray(a.astype(np.uint8), 'RGBA')
    overlay(img, m, lambda d, l: [d.rectangle([px(0), px(top), px(120), px(top + 18)], fill=H('#a8322a')), d.rectangle([px(0), px(bot - 18), px(120), px(bot)], fill=H('#a8322a'))], .9)
    text(img, '御', 60, 78, 34, '#1a0806', I.SERIF, brush=True); text(img, '宿', 60, 128, 40, '#1a0806', I.SERIF, brush=True)
    volume(img, (8, top, 112, bot), .5, .45)
    for y in (top - 6, bot - 4): ImageDraw.Draw(img).rectangle([px(26), px(y), px(94), px(y + 10)], fill=H('#140d09'))
    return 'ry_chochin', done(img), 't'


def g_yukata():
    img = I.canvas(220, 230); floor_shadow(img, 110, 226, 100)
    fr = '#3a2618'
    d = ImageDraw.Draw(img)
    for x in (22, 190): d.rectangle([px(x), px(20), px(x + 8), px(226)], fill=H(fr))
    for x in (12, 180): d.rectangle([px(x), px(218), px(x + 28), px(226)], fill=H(fr))
    line(img, [(4, 26), (216, 26)], '#4a3220', 7)
    body = [(14, 30), (206, 30), (196, 190), (24, 190)]
    m = fill(img, '#e6e0d2', 41, poly=body, scale=10, stretch=(.6, 2), contrast=.6)
    def dr(d, l):          # indigo checks + the inn crest
        for x in range(10, 216, 18): d.line([(px(x), px(30)), (px(x + (x - 110) * .05), px(190))], fill=H('#33476e'), width=px(2))
        for y in range(40, 190, 22): d.line([(px(10), px(y)), (px(210), px(y))], fill=H('#33476e'), width=px(1.2))
    overlay(img, m, dr, .75)
    poly(img, [(96, 30), (110, 74), (124, 30)], '#d4ccbb'); line(img, [(96, 30), (110, 74), (124, 30)], '#33476e', 3)
    fill(img, '#33476e', 43, rect=(30, 120, 190, 136), scale=4, stretch=(4, .5)); ell(img, (146, 72, 176, 102), '#efe9dc'); text(img, '宿', 161, 87, 18, '#33476e', I.SERIF)
    volume(img, (14, 30, 206, 190), .35, .2)
    return 'ry_yukata', done(img), 'b'


def g_zen():
    img = I.canvas(200, 120); floor_shadow(img, 100, 112, 92)
    fill(img, '#4a1a16', 51, poly=[(24, 44), (176, 44), (194, 88), (6, 88)], scale=6, stretch=(3, .5), contrast=1.1)
    fill(img, '#2a0e0c', 52, poly=[(6, 88), (194, 88), (188, 100), (12, 100)], scale=4)
    for x in (22, 170): ImageDraw.Draw(img).rectangle([px(x), px(100), px(x + 8), px(112)], fill=H('#240c0a'))
    volume(img, (6, 44, 194, 112), .4, .2, spec=.18)
    # bowls: rice, miso, a fish plate, pickles, chopsticks
    for (x, y, r, c, fd) in ((62, 70, 22, '#1a1012', '#f2efe6'), (126, 70, 20, '#8a1e18', '#8a5a2e')):
        fill(img, c, x, ell=(x - r, y - r * .9, x + r, y + r * .6), scale=3, contrast=.8); ell(img, (x - r * .8, y - r * .8, x + r * .8, y - r * .2), fd)
        volume(img, (x - r, y - r * .9, x + r, y + r * .6), .5, .3, spec=.25)
    fill(img, '#d8d2c4', 60, ell=(38, 46, 96, 60), scale=3); poly(img, [(50, 52), (78, 48), (90, 53), (78, 57)], '#a8743a'); line(img, [(46, 53), (50, 52)], '#a8743a', 3)
    fill(img, '#2a4a7a', 61, ell=(150, 46, 180, 58), scale=3); ell(img, (156, 48, 174, 55), '#e2c84a')
    line(img, [(36, 84), (150, 80)], '#c9a870', 2.4); line(img, [(36, 88), (150, 84)], '#c9a870', 2.4)
    return 'ry_zen', done(img), 'b'


def g_book():
    img = I.canvas(190, 130); floor_shadow(img, 95, 124, 88); rnd = random.Random(4)
    fill(img, '#3a2618', 70, poly=[(18, 62), (172, 62), (186, 92), (4, 92)], scale=6, stretch=(4, .4), contrast=1.1)   # low desk
    for x in (14, 168): ImageDraw.Draw(img).rectangle([px(x), px(92), px(x + 8), px(124)], fill=H('#24160e'))
    volume(img, (4, 62, 186, 124), .35, .2)
    fill(img, '#e8e0cc', 71, poly=[(40, 44), (96, 50), (96, 80), (36, 74)], scale=4, contrast=.6)                       # open book
    fill(img, '#ece4d2', 72, poly=[(96, 50), (152, 42), (158, 72), (96, 80)], scale=4, contrast=.6)
    d = ImageDraw.Draw(img)
    for k in range(5):
        x = 48 + k * 9; d.line([(px(x), px(52 + k * .6)), (px(x - 1), px(72 + k * .4))], fill=(40, 30, 26, 200), width=px(1.2))
        x = 106 + k * 9; d.line([(px(x), px(50 - k * .8)), (px(x + 1), px(74 - k * .8))], fill=(40, 30, 26, 200), width=px(1.2))
    poly(img, [(36, 74), (96, 80), (152, 72), (158, 76), (96, 84), (34, 78)], '#5a2a20')
    ell(img, (124, 54, 140, 68), '#a8322a')
    line(img, [(150, 34), (176, 60)], '#c9a870', 4); poly(img, [(176, 60), (184, 70), (180, 62)], '#141010')
    text(img, '宿帳', 60, 34, 14, '#e9dcc0', I.SERIF)
    return 'ry_book', done(img), 'b'


def g_hibachi():
    img = I.canvas(160, 170); floor_shadow(img, 80, 164, 72)
    fill(img, '#5a3a24', 80, poly=[(18, 98), (142, 98), (136, 160), (24, 160)], scale=6, stretch=(.6, 2), contrast=1.1)   # wooden brazier
    fill(img, '#2a201a', 81, ell=(22, 90, 138, 108), scale=3)
    soft(img, lambda d: d.ellipse([px(40), px(92), px(120), px(104)], fill=(230, 110, 40, 200)), 2)                 # embers
    volume(img, (18, 90, 142, 160), .4, .2)
    line(img, [(52, 98), (64, 70)], '#3a3430', 3); line(img, [(108, 98), (96, 70)], '#3a3430', 3)                      # trivet
    fill(img, '#2a2826', 82, ell=(36, 34, 124, 92), scale=3, contrast=1.2)                                           # tetsubin
    d = ImageDraw.Draw(img)
    for y in range(44, 88, 7):
        for x in range(42, 120, 7): d.ellipse([px(x - 1.4), px(y - 1.4), px(x + 1.4), px(y + 1.4)], fill=(60, 56, 52, 200))
    volume(img, (36, 34, 124, 92), .6, .4, spec=.2)
    poly(img, [(120, 58), (148, 40), (150, 46), (124, 66)], '#2a2826')
    d.arc([px(46), px(4), px(114), px(56)], 190, 350, fill=H('#3a3430'), width=px(4))
    ell(img, (70, 30, 90, 40), '#3a3430')
    soft(img, lambda dd: [dd.line([(px(150), px(38)), (px(146 + k * 3), px(14 - k * 4))], fill=(230, 230, 230, 60), width=px(4)) for k in range(3)], 3)
    return 'ry_hibachi', done(img), 'b'


GIFTS = [g_noren, g_chochin, g_yukata, g_zen, g_book, g_hibachi]

if __name__ == '__main__':
    ims = []
    for k in ('simple', 'down', 'crane'): ims += [('fb_' + k, futon_back(k), 'b'), ('ff_' + k, futon_front(k), 'b')]
    ims.append(('sign', sign(), 'b'))
    ims += [f() for f in GIFTS]
    W = 1160; x = y = rowh = 0; pos = {}
    for iid, im, _ in sorted(ims, key=lambda t: -t[1].height):
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[iid] = (x, y, im.width, im.height); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for iid, im, _ in ims: at.paste(im, pos[iid][:2])
    at.save(os.path.join(ASSETS, 'items', 'atlas_ry.webp'), 'WEBP', quality=88, alpha_quality=92, method=6)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'out'), exist_ok=True)
    pv = Image.new('RGBA', at.size, (34, 30, 28, 255)); pv.alpha_composite(at); pv.convert('RGB').save(os.path.join(os.path.dirname(__file__), 'out', 'atlas_ry.png'))
    print(json.dumps({'size': [W, y + rowh], 'at': {iid: list(pos[iid]) + [a] for iid, _, a in ims}}))
