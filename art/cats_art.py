#!/usr/bin/env python3
"""«Кошки соседей»: 8 painted neighbour cats (ordinary cats, adult proportions, soft painted volumes) and their 8 little gifts.
Per cat: sit (front, sitting on an edge), sit with a flicked ear, lie (loaf on a wall, head to the viewer), walk ×2 (side view),
and a separate hanging tail (swung in the game). Same organic spline toolkit as pet2_art.py / guests_art.py.
Usage: cats_art.py <assets dir>  → assets/items/atlas_nk.webp (cats), assets/items/atlas_nk2.webp (gifts) + previews in art/out;
prints the rect JSON that feat/cats.js embeds."""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
ASSETS = sys.argv[1]
sys.argv = [sys.argv[0], os.path.join(ASSETS, 'mon')]   # monsters.py reads its OUT from argv[1]
import paint as P
from paint import hexc, mixc
import monsters as M
from monsters import canvas, px, soft
from story_art import shape, clipped, poly_s
from guests_art import tube, fur_ticks, stroke

INK = (40, 32, 30, 255)
PINK = hexc('#d99a98')
# cat looks: base fur, shadow, light; white parts; pattern; eyes; build (fat, size), ears, extras
CATS = {
 'daifuku': dict(b='#d4873f', d='#a35a26', l='#efb36c', wh='chest', pat='tabby', st=(150, 80, 36, 150), eye=('#d9a63c',), fat=1.32, sz=1.04, ear=.78, nose='#c9776e'),
 'mike':    dict(b='#efe8dc', d='#c7bdb0', l='#fbf8f2', wh=None, pat='calico', eye=('#c9a13c',), fat=1.0, sz=.95, ear=.88, nose='#e0a0a0', acc='bell'),
 'sumimi':  dict(b='#2b2930', d='#141317', l='#4a4752', wh=None, pat=None, eye=('#c6c94c',), fat=.96, sz=1.0, ear=.9, nose='#3a2c30'),
 'yuki':    dict(b='#eeeae2', d='#c4bdb2', l='#fbf9f4', wh=None, pat=None, eye=('#7fb0d8', '#d8b048'), fat=1.08, sz=.98, ear=.8, nose='#e3a8a6', old=True),
 'tora':    dict(b='#9c8460', d='#665238', l='#c4ad86', wh='chin', pat='tabby', st=(48, 36, 24, 190), eye=('#d4b03a',), fat=1.1, sz=1.06, ear=.82, nose='#a86a5e', notch=True),
 'kinako':  dict(b='#e7d8bf', d='#bfa98a', l='#f6ecdc', wh=None, pat='points', pt='#4e3a30', eye=('#6aa4dc',), fat=.88, sz=.98, ear=1.0, nose='#6a4a44', acc='ribbon'),
 'pochi':   dict(b='#f1ebe1', d='#c9c0b3', l='#fdfaf4', wh=None, pat='bicolor', pc='#8a5a36', eye=('#c9a54a',), fat=1.0, sz=.98, ear=.86, nose='#dc9c98', bob=True),
 'maru':    dict(b='#8e9096', d='#5e6066', l='#b6b8bd', wh='socks', pat='tabby', st=(66, 68, 74, 150), eye=('#d2bc4a',), fat=.9, sz=.8, ear=.95, nose='#d49a9a', young=True),
}
SIT_W, SIT_H, LIE_W, LIE_H, WALK_W, WALK_H, TL_W, TL_H = 120, 150, 168, 96, 176, 124, 34, 112


def C(c, k): return hexc(c[k]) if isinstance(c[k], str) else c[k]


def patch_layer(img, m, c, seed, box, horiz=False):
    """Pattern clipped to a body-part mask: tabby stripes, calico/bicolor patches, siamese points."""
    x0, y0, x1, y1 = box; rnd = random.Random(seed); pat = c['pat']
    if pat == 'tabby' and horiz:
        clipped(img, m, lambda d, l: [stroke(d, [(x0 - 3, y0 + (y1 - y0) * f), (x0 + (x1 - x0) * .25, y0 + (y1 - y0) * (f + .05)), (x0 + (x1 - x0) * .4, y0 + (y1 - y0) * (f + .02))], c['st'], rnd.uniform(2, 3)) for f in np.linspace(.15, .85, 5)] +
                [stroke(d, [(x1 + 3, y0 + (y1 - y0) * f), (x1 - (x1 - x0) * .25, y0 + (y1 - y0) * (f + .05)), (x1 - (x1 - x0) * .4, y0 + (y1 - y0) * (f + .02))], c['st'], rnd.uniform(2, 3)) for f in np.linspace(.15, .85, 5)], .85)
    elif pat == 'tabby':
        clipped(img, m, lambda d, l: [stroke(d, [(x0 + (x1 - x0) * f, y0 - 3), (x0 + (x1 - x0) * (f + rnd.uniform(-.05, .05)), (y0 + y1) / 2), (x0 + (x1 - x0) * (f + rnd.uniform(-.06, .06)), y1 + 3)],
                                             c['st'], rnd.uniform(2.2, 3.4)) for f in np.linspace(.12, .88, 6)], .85)
    elif pat in ('calico', 'bicolor'):
        cols = [hexc('#d27b35', 230), hexc('#2c2624', 235)] if pat == 'calico' else [hexc(c['pc'], 230)]
        def fn(d, l):
            for i in range(3 if pat == 'calico' else 2):
                col = cols[i % len(cols)]; cx, cy = rnd.uniform(x0, x1), rnd.uniform(y0, y1); rx, ry = (x1 - x0) * rnd.uniform(.22, .4), (y1 - y0) * rnd.uniform(.2, .36)
                d.ellipse([px(cx - rx), px(cy - ry), px(cx + rx), px(cy + ry)], fill=col)
        l = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(l), l); l = l.filter(ImageFilter.GaussianBlur(1.6 * M.S))
        a = np.asarray(l, np.float32); a[..., 3] *= np.asarray(m, np.float32) / 255; img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))


def points(img, m, c, cx, cy, rx, ry, a=.9):
    """Siamese darker points: a soft dark blob clipped to the part."""
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l); col = hexc(c['pt'], int(255 * a))
    d.ellipse([px(cx - rx), px(cy - ry), px(cx + rx), px(cy + ry)], fill=col); l = l.filter(ImageFilter.GaussianBlur(min(rx, ry) * .55 * M.S))
    q = np.asarray(l, np.float32); q[..., 3] *= np.asarray(m, np.float32) / 255; img.alpha_composite(Image.fromarray(q.astype(np.uint8), 'RGBA'))


def ear(img, c, bx, by, ang, size, seed, notch=False):
    ca, sa, pa = math.cos(ang), math.sin(ang), ang + math.pi / 2
    tip = (bx + ca * size, by + sa * size); l = (bx + math.cos(pa) * size * .55, by + math.sin(pa) * size * .55); r = (bx - math.cos(pa) * size * .55, by - math.sin(pa) * size * .55)
    col = hexc(c['pt']) if c['pat'] == 'points' else C(c, 'd') if c['pat'] in ('calico',) and seed % 2 else C(c, 'b')
    if c['pat'] == 'calico' and seed % 2: col = hexc('#2c2624')
    if c['pat'] == 'bicolor': col = hexc(c['pc'])
    m = shape(img, col, seed, [l, tip, r, (bx - ca * size * .25, by - sa * size * .25)], scale=5, k=.4, rim=.25)
    d = ImageDraw.Draw(img); k = .6
    inner = PINK if c['b'] not in ('#2b2930',) else hexc('#4a3a40')
    poly_s(d, [(bx + (l[0] - bx) * k, by + (l[1] - by) * k + 1.5), (bx + (tip[0] - bx) * .74, by + (tip[1] - by) * .74), (bx + (r[0] - bx) * k, by + (r[1] - by) * k + 1.5)], inner[:3] + (200,), 4)
    if notch:   # Tora's torn ear
        ImageDraw.Draw(img).ellipse([px(tip[0] - size * .2 + ca * -size * .25), px(tip[1] - size * .16), px(tip[0] + size * .1), px(tip[1] + size * .14)], fill=(0, 0, 0, 0))


def head(img, c, hx, hy, r, seed, flick=False, closed=False, look=(0, 0)):
    """Adult cat head, front view: wide cheeks, almond eyes, small nose. Returns the eye boxes for blinking."""
    e = c['ear'] * r * 1.05; w = r * (1.18 if c['fat'] > 1.2 else 1.08 if c['fat'] > 1.05 else 1.0)
    ear(img, c, hx - r * .55, hy - r * .55, -math.pi / 2 - .42, e, seed + 1)
    ear(img, c, hx + r * .55, hy - r * .55, -math.pi / 2 + (.95 if flick else .42), e * (.9 if flick else 1), seed + 2, c.get('notch'))
    pts = [(hx, hy - r * .86), (hx + w * .66, hy - r * .7), (hx + w * .98, hy - r * .12), (hx + w * 1.06, hy + r * .3), (hx + w * .78, hy + r * .64),
           (hx + w * .28, hy + r * .82), (hx - w * .28, hy + r * .82), (hx - w * .78, hy + r * .64), (hx - w * 1.06, hy + r * .3), (hx - w * .98, hy - r * .12), (hx - w * .66, hy - r * .7)]
    mh = shape(img, C(c, 'b'), seed, pts, scale=6, contrast=.6, dk=.32, lt=.14, k=.55, rim=.4)
    box = (hx - w, hy - r, hx + w, hy + r * .8)
    if c['pat'] == 'tabby':
        clipped(img, mh, lambda d, l: [stroke(d, [(hx + r * o * .2, hy - r * .9), (hx + r * o * .17, hy - r * .62), (hx + r * o * .1, hy - r * .4)], c['st'], 2.2) for o in (-1, 0, 1)])
        clipped(img, mh, lambda d, l: [stroke(d, [(hx + s * w * 1.05, hy + r * (.05 + k * .2)), (hx + s * w * .7, hy + r * (.1 + k * .16))], c['st'], 1.8) for s in (-1, 1) for k in (0, 1)])
    elif c['pat'] in ('calico', 'bicolor'):
        cols = (hexc('#d27b35', 235), hexc('#2c2624', 240)) if c['pat'] == 'calico' else (hexc(c['pc'], 235), hexc(c['pc'], 235))
        def fn(d, l):
            d.ellipse([px(hx - w * 1.1), px(hy - r * 1.0), px(hx - w * .05), px(hy + r * .15)], fill=cols[0])
            d.ellipse([px(hx + w * .25), px(hy - r * 1.0), px(hx + w * 1.15), px(hy - r * .2)], fill=cols[1])
        l = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(l), l); l = l.filter(ImageFilter.GaussianBlur(1.4 * M.S))
        a = np.asarray(l, np.float32); a[..., 3] *= np.asarray(mh, np.float32) / 255; img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))
    elif c['pat'] == 'points':
        points(img, mh, c, hx, hy + r * .3, w * .62, r * .62, .95)
    if c.get('wh') in ('chest', 'chin', 'socks') or c['pat'] in ('calico', 'bicolor'):
        shape(img, hexc('#f1ece2'), seed + 3, ell=(hx - w * .36, hy + r * .2, hx + w * .36, hy + r * .8), scale=4, contrast=.4, dk=.12, lt=.05, k=.3, rim=.2)
    fur_ticks(img, mh, seed + 4, box, 26, mixc(C(c, 'd'), (0, 0, 0, 255), .2)[:3] + (60,), (2, 4))
    d = ImageDraw.Draw(img); eyes = []
    dark = c['b'] == '#2b2930'
    for i, sx in enumerate((-1, 1)):
        ex, ey = hx + sx * r * .4, hy + r * .02; rx, ry = r * .2, r * (.15 if not c.get('young') else .18)
        ic = hexc(c['eye'][i % len(c['eye'])]); eyes.append((ex, ey, rx * 1.25, ry * 1.4))
        if closed:
            d.arc([px(ex - rx), px(ey - ry), px(ex + rx), px(ey + ry * .8)], 15, 165, fill=INK, width=px(1.6)); continue
        al = [(ex - rx * 1.1, ey + ry * .15), (ex - rx * .3, ey - ry), (ex + rx * .8, ey - ry * .75), (ex + rx * 1.12, ey + ry * .05), (ex + rx * .2, ey + ry * .95), (ex - rx * .6, ey + ry * .7)]
        poly_s(d, al, ic, 6)
        pr = rx * (.3 if dark else .22); d.ellipse([px(ex - pr + look[0] * rx * .3), px(ey - ry * .8), px(ex + pr + look[0] * rx * .3), px(ey + ry * .8)], fill=(14, 10, 12, 255))
        d.line([(px(x), px(y)) for x, y in al[:4]], fill=(30, 22, 20, 230), width=px(1.3))
        d.ellipse([px(ex - rx * .55), px(ey - ry * .6), px(ex - rx * .15), px(ey - ry * .15)], fill=(255, 255, 255, 220))
        if c.get('old'):   # sleepy old lady: heavy upper lids
            poly_s(d, [(ex - rx * 1.25, ey - ry * 1.2), (ex + rx * 1.25, ey - ry * 1.2), (ex + rx * 1.2, ey - ry * .05), (ex - rx * 1.2, ey - ry * .1)], C(c, 'b'), 4)
            d.line([(px(ex - rx * 1.1), px(ey - ry * .05)), (px(ex + rx * 1.1), px(ey - ry * .05))], fill=(60, 50, 46, 200), width=px(1.2))
    ny = hy + r * .36; nc = hexc(c['nose'])
    poly_s(d, [(hx - r * .1, ny - r * .05), (hx + r * .1, ny - r * .05), (hx, ny + r * .07)], nc, 3)
    lc = (200, 190, 180, 200) if dark else INK
    d.arc([px(hx - r * .16), px(ny), px(hx), px(ny + r * .14)], 10, 170, fill=lc, width=px(1.2)); d.arc([px(hx), px(ny), px(hx + r * .16), px(ny + r * .14)], 10, 170, fill=lc, width=px(1.2))
    for sx in (-1, 1):
        for k in range(3): d.line([(px(hx + sx * r * .26), px(ny + r * .08 + k * 2)), (px(hx + sx * r * 1.15), px(ny - r * .06 + k * r * .15))], fill=(236, 232, 224, 130), width=px(.7))
    return eyes


def collar(img, c, hx, ny, r):
    if c.get('acc') == 'bell':
        d = ImageDraw.Draw(img); d.arc([px(hx - r * .8), px(ny - r * .5), px(hx + r * .8), px(ny + r * .25)], 20, 160, fill=hexc('#b8322c'), width=px(3.2))
        shape(img, hexc('#d9b24a'), 911, ell=(hx - r * .17, ny + r * .14, hx + r * .17, ny + r * .46), scale=3, k=.6, rim=.3, spec=.5)
    if c.get('acc') == 'ribbon':
        d = ImageDraw.Draw(img); d.arc([px(hx - r * .8), px(ny - r * .5), px(hx + r * .8), px(ny + r * .25)], 20, 160, fill=hexc('#d0607a'), width=px(2.6))
        bx, by = hx + r * .35, ny + r * .2
        for s in (-1, 1): poly_s(d, [(bx, by), (bx + s * r * .42, by - r * .22), (bx + s * r * .45, by + r * .2)], hexc('#e27a92'), 4)
        d.ellipse([px(bx - r * .09), px(by - r * .09), px(bx + r * .09), px(by + r * .09)], fill=hexc('#b84a64'))


def sit(c, seed, flick=False):
    img = canvas(SIT_W, SIT_H); s = c['sz']; f = c['fat']; CX, FY = SIT_W / 2, SIT_H - 3
    hw, ch, r = 31 * s * f, 70 * s, 21 * s * (1.05 if c.get('young') else 1)
    body = [(CX - hw * .8, FY - 1), (CX - hw * 1.0, FY - ch * .16), (CX - hw * .94, FY - ch * .4), (CX - hw * .6, FY - ch * .6), (CX - hw * .5, FY - ch * .86), (CX - hw * .36, FY - ch * 1.02), (CX, FY - ch * 1.08),
            (CX + hw * .36, FY - ch * 1.02), (CX + hw * .5, FY - ch * .86), (CX + hw * .6, FY - ch * .6), (CX + hw * .94, FY - ch * .4), (CX + hw * 1.0, FY - ch * .16), (CX + hw * .8, FY - 1)]
    mb = shape(img, C(c, 'b'), seed, body, scale=8, contrast=.6, dk=.3, lt=.12, k=.55, rim=.42)
    bb = (CX - hw, FY - ch, CX + hw, FY)
    patch_layer(img, mb, c, seed + 1, bb, horiz=True)
    if c['pat'] == 'points': points(img, mb, c, CX, FY, hw * .9, ch * .25, .6)
    for sx in (-1, 1):   # haunches: soft darker crease above each hip
        ImageDraw.Draw(img)
        clipped(img, mb, lambda d, l, sx=sx: stroke(d, [(CX + sx * hw * .98, FY - ch * .36), (CX + sx * hw * .62, FY - ch * .42), (CX + sx * hw * .42, FY - ch * .2), (CX + sx * hw * .4, FY - 2)], mixc(C(c, 'd'), (0, 0, 0, 255), .25)[:3] + (110,), 2.2), .8)
    fur_ticks(img, mb, seed + 2, bb, 40, mixc(C(c, 'd'), (0, 0, 0, 255), .2)[:3] + (55,), (3, 6))
    if c.get('wh') in ('chest', 'chin') or c['pat'] in ('calico', 'bicolor') or c.get('wh') == 'socks':
        shape(img, hexc('#f1ece2'), seed + 3, ell=(CX - hw * .38, FY - ch * .95, CX + hw * .38, FY - ch * .25), scale=4, contrast=.4, dk=.12, lt=.05, k=.3, rim=.25)
    # haunch shading + front legs
    for sx in (-1, 1):
        lc = C(c, 'b'); pawc = hexc('#f1ece2') if (c.get('wh') in ('socks', 'chest') or c['pat'] in ('calico', 'bicolor')) else lc
        if c['pat'] == 'points': lc = mixc(hexc(c['pt']), C(c, 'b'), .35); pawc = hexc(c['pt'])
        if c['b'] == '#2b2930': lc = C(c, 'b')
        lx = CX + sx * hw * .3
        shape(img, lc, seed + 5 + sx, tube([(lx, FY - ch * .6), (lx + sx * .5, FY - ch * .3), (lx + sx * 1, FY - 5)], 5.6 * s, 5.2 * s), scale=4, contrast=.5, dk=.3, lt=.12, k=.5, rim=.35)
        shape(img, pawc, seed + 7 + sx, ell=(lx + sx - 7 * s, FY - 8 * s, lx + sx + 7 * s, FY + 1), scale=3, contrast=.4, dk=.15, lt=.05, k=.4, rim=.25)
        d = ImageDraw.Draw(img)
        for k in (-1, 1): d.line([(px(lx + sx + k * 2.4 * s), px(FY - 3 * s)), (px(lx + sx + k * 2.4 * s), px(FY))], fill=(40, 30, 28, 120), width=px(.7))
    hx, hy = CX, FY - ch * 1.02 - r * .55
    eyes = head(img, c, hx, hy, r, seed + 9, flick)
    collar(img, c, hx, hy + r * .78, r)
    return img, eyes


def lie(c, seed):
    """Loaf on the edge: side body to the right, head turned to the viewer, paws tucked; tail hangs separately from the rear."""
    img = canvas(LIE_W, LIE_H); s = c['sz']; f = c['fat']; FY = LIE_H - 3
    L, Hh, r = 108 * s, 34 * s * f, 20 * s
    x0 = 18; x1 = x0 + L
    body = [(x0, FY - 2), (x0 - 4, FY - Hh * .55), (x0 + L * .12, FY - Hh * .98), (x0 + L * .5, FY - Hh * 1.06), (x0 + L * .86, FY - Hh * .9), (x1 + 4, FY - Hh * .4), (x1, FY - 1)]
    mb = shape(img, C(c, 'b'), seed, body, scale=8, contrast=.6, dk=.3, lt=.12, k=.55, rim=.42)
    bb = (x0, FY - Hh, x1, FY)
    patch_layer(img, mb, c, seed + 1, bb)
    if c['pat'] == 'points': points(img, mb, c, x0 + 6, FY - Hh * .4, 18, Hh * .6, .5)
    fur_ticks(img, mb, seed + 2, bb, 50, mixc(C(c, 'd'), (0, 0, 0, 255), .2)[:3] + (55,), (3, 7), ang=.2)
    pawc = hexc('#f1ece2') if (c.get('wh') or c['pat'] in ('calico', 'bicolor')) else C(c, 'b')
    if c['pat'] == 'points': pawc = hexc(c['pt'])
    shape(img, pawc, seed + 3, ell=(x1 - 30 * s, FY - 9 * s, x1 + 2, FY + 1), scale=3, contrast=.4, dk=.15, lt=.05, k=.4, rim=.25)
    hx, hy = x1 - 14 * s, FY - Hh * .9 - r * .3
    eyes = head(img, c, hx, hy, r, seed + 9, closed=False)
    collar(img, c, hx, hy + r * .78, r)
    return img, eyes, (x0 + 4, FY - 4)


def walk(c, seed, ph):
    """Side view walking right, tail up, head turned a little to the viewer; ph 0/1 = stride phases."""
    img = canvas(WALK_W, WALK_H); s = c['sz']; f = c['fat']; FY = WALK_H - 3
    L, Hh, lg, r = 100 * s, 25 * s * f, 30 * s, 19 * s
    x0 = 36; x1 = x0 + L; by = FY - lg - Hh * .5
    tc = C(c, 'b') if c['pat'] != 'points' else hexc(c['pt'])
    if c['pat'] == 'bicolor': tc = hexc(c['pc'])
    if c.get('bob'):
        shape(img, tc, seed + 20, ell=(x0 - 12, by - Hh * .9, x0 + 6, by - Hh * .2), scale=3, k=.5, rim=.3)
    else:
        pts = [(x0 + 4, by - Hh * .2)]; a = -math.pi * .78; x, y = pts[0]
        for i in range(7): a += .2 + (.12 if ph else .06); x += math.cos(a) * 9 * s; y += math.sin(a) * 9 * s; pts.append((x, y))
        mt = shape(img, tc, seed + 20, tube(pts, 5 * s, 3.2 * s), scale=4, contrast=.6, dk=.3, lt=.12, k=.5, rim=.3)
        if c['pat'] == 'tabby': clipped(img, mt, lambda d, l: [d.line([(px(qx - 6), px(qy - 2)), (px(qx + 6), px(qy + 2))], fill=c['st'], width=px(2.4)) for qx, qy in pts[1:-1:2]])
    def legs(back):
        for i, (lx, sw) in enumerate(((x1 - 16 * s, 1), (x0 + 14 * s, -1))):
            o = (11 if ph else -9) * s * (1 if (i == 0) != back else -1)
            lc = mixc(C(c, 'd'), C(c, 'b'), .4) if back else C(c, 'b')
            if c['pat'] == 'points': lc = hexc(c['pt'])
            if i == 0: cl = [(lx, by), (lx + o * .45, by + lg * .55), (lx + o, FY - 3)]
            else: cl = [(lx, by + Hh * .2), (lx + 7 * s + o * .3, by + lg * .42), (lx - 5 * s + o * .7, by + lg * .78), (lx + o, FY - 3)]
            shape(img, lc, seed + 30 + i + back * 5, tube(cl, (6.2 if i else 5.2) * s, 4.2 * s), scale=4, contrast=.5, dk=.3, lt=.1, k=.5, rim=.35)
            pc = hexc('#f1ece2') if (c.get('wh') in ('socks', 'chest') or c['pat'] in ('calico', 'bicolor')) else lc
            shape(img, pc, seed + 40 + i + back * 5, ell=(lx + o - 5 * s, FY - 6 * s, lx + o + 7 * s, FY + 1), scale=3, k=.4, rim=.25)
    legs(True)
    body = [(x0 - 8, by - Hh * .25), (x0 + 2, by - Hh * .8), (x0 + L * .45, by - Hh * 1.02), (x1 - 10, by - Hh * .92), (x1 + 8, by - Hh * .2), (x1 - 4, by + Hh * .9), (x0 + L * .55, by + Hh * .5), (x0 + L * .2, by + Hh * .72), (x0 - 4, by + Hh * .5)]
    mb = shape(img, C(c, 'b'), seed, body, scale=8, contrast=.6, dk=.3, lt=.12, k=.55, rim=.42)
    bb = (x0 - 6, by - Hh, x1 + 8, by + Hh)
    patch_layer(img, mb, c, seed + 1, bb)
    if c['pat'] == 'points': points(img, mb, c, x0, by, 20, Hh, .45)
    fur_ticks(img, mb, seed + 2, bb, 50, mixc(C(c, 'd'), (0, 0, 0, 255), .2)[:3] + (55,), (3, 7), ang=.15)
    if c.get('wh') == 'chest' or c['pat'] in ('calico', 'bicolor'):
        shape(img, hexc('#f1ece2'), seed + 3, ell=(x1 - 22 * s, by - Hh * .1, x1 + 6, by + Hh * .8), scale=4, contrast=.4, dk=.12, lt=.05, k=.3, rim=.2)
    legs(False)
    hx, hy = x1 + 8 * s, by - Hh * .7 - r * .55
    eyes = head(img, c, hx, hy, r, seed + 9, look=(.6, 0))
    collar(img, c, hx, hy + r * .78, r)
    return img, eyes


def tail(c, seed):
    img = canvas(TL_W, TL_H); s = c['sz']
    tc = C(c, 'b') if c['pat'] != 'points' else hexc(c['pt'])
    if c['pat'] == 'calico': tc = hexc('#2c2624')
    if c['pat'] == 'bicolor': tc = hexc(c['pc'])
    if c.get('bob'):
        shape(img, tc, seed, ell=(TL_W / 2 - 9, 0, TL_W / 2 + 9, 18), scale=3, k=.5, rim=.3); return img
    pts = [(TL_W / 2, 2)]; x, y = pts[0]; a = math.pi / 2
    n = 9; st = (TL_H - 14) * (.92 if c.get('young') else 1) / n
    for i in range(n): a += (.02 if i < 6 else -.32); x += math.cos(a) * st; y += math.sin(a) * st; pts.append((x, y))
    m = shape(img, tc, seed, tube(pts, 5.4 * s, 3.4 * s), scale=4, contrast=.6, dk=.3, lt=.12, k=.5, rim=.3)
    if c['pat'] == 'tabby' or c['pat'] == 'calico':
        col = c['st'] if c['pat'] == 'tabby' else hexc('#d27b35', 220)
        clipped(img, m, lambda d, l: [d.line([(px(qx - 7), px(qy - 1)), (px(qx + 7), px(qy + 2))], fill=col, width=px(2.6)) for qx, qy in pts[1:-1:2]])
    return img


def finish(img):
    out = img.resize((P.W, P.H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(.45))
    a = np.asarray(out, np.float32); a[..., :3] = np.clip(a[..., :3] + np.random.default_rng(7).normal(0, 3.5, a.shape[:2])[..., None], 0, 255)
    return Image.fromarray(a.astype(np.uint8), 'RGBA')


# ── gifts ──
def g_shell():
    img = canvas(110, 76)
    m = shape(img, hexc('#a9773e'), 801, [(14, 50), (24, 26), (52, 14), (88, 20), (102, 40), (90, 58), (52, 64), (22, 62)], scale=4, contrast=.9, dk=.35, lt=.3, k=.6, rim=.3, spec=.35)
    clipped(img, m, lambda d, l: [d.arc([px(x - 10), px(14), px(x + 10), px(64)], 250, 290, fill=(90, 56, 26, 200), width=px(1.6)) for x in range(36, 96, 9)] +
            [d.line([(px(40), px(22)), (px(70), px(30))], fill=(240, 220, 170, 160), width=px(2))])
    d = ImageDraw.Draw(img)
    for x0, y0, x1, y1 in [(30, 58, 20, 72), (50, 62, 46, 74), (70, 60, 76, 73), (86, 54, 98, 66)]: d.line([(px(x0), px(y0)), (px(x1), px(y1))], fill=(120, 80, 40, 230), width=px(2))
    shape(img, hexc('#8e5e2c'), 802, ell=(6, 34, 26, 52), scale=3, k=.5, rim=.3, spec=.3)
    return finish(img)


def g_ribbon():
    img = canvas(124, 84); d = ImageDraw.Draw(img)
    for s in (-1, 1):
        shape(img, hexc('#d65d7a'), 810 + s, [(62, 36), (62 + s * 50, 10), (62 + s * 56, 40), (62 + s * 44, 58)], scale=4, contrast=.7, k=.6, rim=.3, spec=.2)
        shape(img, hexc('#c24e6a'), 812 + s, tube([(62, 42), (62 + s * 14, 62), (62 + s * 22, 80)], 6, 5), scale=4, k=.5, rim=.3)
    shape(img, hexc('#b8445e'), 814, ell=(52, 28, 72, 50), scale=3, k=.6, rim=.3, spec=.3)
    return finish(img)


def g_cap():
    img = canvas(84, 60)
    shape(img, hexc('#b9bcc0'), 820, ell=(6, 14, 78, 54), scale=3, contrast=.8, k=.6, rim=.35, spec=.35)
    d = ImageDraw.Draw(img)
    for i in range(14):
        a = i / 14 * math.tau; d.line([(px(42 + math.cos(a) * 30), px(34 + math.sin(a) * 15)), (px(42 + math.cos(a) * 36), px(34 + math.sin(a) * 19))], fill=(120, 124, 130, 220), width=px(2.5))
    shape(img, hexc('#3d78b4'), 821, ell=(14, 18, 70, 46), scale=3, k=.5, rim=.2)
    d = ImageDraw.Draw(img); d.ellipse([px(30), px(26), px(54), px(40)], fill=(238, 238, 236, 235))
    return finish(img)


def g_feather():
    img = canvas(60, 196)
    m = shape(img, hexc('#22232a'), 830, [(30, 6), (44, 40), (46, 110), (38, 170), (30, 186), (20, 160), (14, 100), (18, 40)], scale=4, contrast=.8, dk=.4, lt=.5, k=.6, rim=.3, spec=.3)
    clipped(img, m, lambda d, l: [d.line([(px(30), px(y)), (px(30 + s * 18), px(y - 12))], fill=(70, 80, 110, 140), width=px(1.2)) for y in range(30, 180, 8) for s in (-1, 1)])
    d = ImageDraw.Draw(img); d.line([(px(30), px(10)), (px(30), px(194))], fill=(150, 150, 160, 220), width=px(1.6))
    return finish(img)


def g_omamori():
    img = canvas(76, 120)
    m = shape(img, hexc('#b3302c'), 840, [(14, 40), (38, 30), (62, 40), (64, 110), (12, 110)], scale=4, contrast=.7, k=.5, rim=.3, smooth=False)
    clipped(img, m, lambda d, l: [d.ellipse([px(x - 3), px(y - 3), px(x + 3), px(y + 3)], fill=(226, 186, 90, 200)) for x in range(18, 62, 10) for y in range(52, 108, 12)])
    d = ImageDraw.Draw(img); d.rectangle([px(26), px(56), px(50), px(96)], fill=(240, 230, 210, 235)); d.line([(px(38), px(62)), (px(38), px(90))], fill=(40, 30, 30, 220), width=px(2))
    d.line([(px(32), px(70)), (px(44), px(70))], fill=(40, 30, 30, 220), width=px(2))
    stroke(d, [(38, 32), (30, 16), (38, 4), (46, 16), (38, 32)], (220, 190, 90, 255), 2.2)
    return finish(img)


def g_bag():
    img = canvas(104, 130)
    m = shape(img, hexc('#cfb48a'), 850, [(12, 30), (92, 30), (96, 126), (8, 126)], scale=5, contrast=.8, k=.5, rim=.3, smooth=False)
    clipped(img, m, lambda d, l: [d.line([(px(8), px(30 + k * 6)), (px(96), px(30 + k * 6))], fill=(150, 120, 80, 120), width=px(1)) for k in range(0, 3)])
    d = ImageDraw.Draw(img); d.ellipse([px(32), px(60), px(72), px(100)], outline=(150, 70, 50, 230), width=px(2.4))
    d.line([(px(52), px(66)), (px(52), px(94))], fill=(150, 70, 50, 230), width=px(2.4)); d.line([(px(40), px(78)), (px(64), px(78))], fill=(150, 70, 50, 230), width=px(2.4))
    shape(img, hexc('#c88a46'), 851, ell=(30, 8, 74, 40), scale=4, contrast=.6, k=.6, rim=.3, spec=.25)   # a bun peeking out
    return finish(img)


def g_leaf():
    img = canvas(110, 110)
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i / 10 * math.tau; rr = 46 if i % 2 == 0 else 20
        if i in (4, 5, 6): rr *= .8 if i % 2 == 0 else 1
        pts.append((55 + math.cos(a) * rr, 52 + math.sin(a) * rr))
    m = shape(img, hexc('#b53a22'), 860, pts, scale=4, contrast=.7, dk=.3, lt=.25, k=.6, rim=.25, smooth=False)
    clipped(img, m, lambda d, l: [d.line([(px(55), px(56)), (px(x), px(y))], fill=(120, 36, 20, 200), width=px(1.4)) for x, y in pts[::2]])
    d = ImageDraw.Draw(img); d.line([(px(55), px(56)), (px(58), px(104))], fill=(110, 60, 30, 255), width=px(2))
    return finish(img)


def g_yarn():
    img = canvas(100, 92)
    m = shape(img, hexc('#7d9cc4'), 870, ell=(10, 10, 86, 84), scale=4, contrast=.7, k=.6, rim=.4)
    clipped(img, m, lambda d, l: [d.arc([px(10 + k * 7), px(10 + k * 3), px(86 - k * 5), px(84 - k * 4)], 200 + k * 20, 340 + k * 15, fill=(70, 96, 140, 200), width=px(2)) for k in range(6)] +
            [d.arc([px(4), px(20 + k * 10), px(90), px(60 + k * 10)], 190, 350, fill=(170, 196, 226, 150), width=px(1.6)) for k in range(4)])
    d = ImageDraw.Draw(img); stroke(d, [(80, 70), (92, 80), (86, 88), (96, 90)], (125, 156, 196, 255), 2.2)
    return finish(img)


if __name__ == '__main__':
    random.seed(3)
    frames, J = [], {}
    for ci, (cid, c) in enumerate(CATS.items()):
        sd = 100 + ci * 60
        im, ey = sit(c, sd); frames.append((cid + '_sit', finish(im), ey, None))
        im, ey = sit(c, sd, True); frames.append((cid + '_ear', finish(im), ey, None))
        im, ey, root = lie(c, sd + 20); frames.append((cid + '_lie', finish(im), ey, root))
        for ph in (0, 1):
            im, ey = walk(c, sd + 30, ph); frames.append((cid + '_w' + str(ph), finish(im), ey, None))
        frames.append((cid + '_tail', finish(tail(c, sd + 40)), [], None))
    # shelf packing: one row per cat
    rowW = SIT_W * 2 + LIE_W + WALK_W * 2 + TL_W + 12; rowH = max(SIT_H, WALK_H, TL_H) + 2
    A = Image.new('RGBA', (rowW, rowH * len(CATS)), (0, 0, 0, 0)); x = y = 0; prev = None
    for k, f, ey, root in frames:
        cid = k.split('_')[0]
        if cid != prev: x = 0; y = list(CATS).index(cid) * rowH; prev = cid
        A.alpha_composite(f, (x, y)); J[k] = [x, y, f.width, f.height, [[round(v, 1) for v in e] for e in ey]] + ([list(map(round, root))] if root else [])
        x += f.width + 2
    A.save(f'{ASSETS}/items/atlas_nk.webp', 'WEBP', quality=86, alpha_quality=90, method=6)
    gifts = [('nk_shell', g_shell()), ('nk_ribbon', g_ribbon()), ('nk_cap', g_cap()), ('nk_feather', g_feather()), ('nk_omamori', g_omamori()), ('nk_bag', g_bag()), ('nk_leaf', g_leaf()), ('nk_yarn', g_yarn())]
    B = Image.new('RGBA', (sum(i.width for _, i in gifts) + 2 * len(gifts), max(i.height for _, i in gifts)), (0, 0, 0, 0)); IJ = {}; x = 0
    for k, i in gifts: B.alpha_composite(i, (x, 0)); IJ[k] = [x, 0, i.width, i.height]; x += i.width + 2
    B.save(f'{ASSETS}/items/atlas_nk2.webp', 'WEBP', quality=88, alpha_quality=92, method=6)
    OUTP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out'); os.makedirs(OUTP, exist_ok=True)
    pv = Image.new('RGBA', A.size, (58, 64, 60, 255)); pv.alpha_composite(A); pv.convert('RGB').save(OUTP + '/cats_atlas.jpg', quality=88)
    pv = Image.new('RGBA', B.size, (58, 64, 60, 255)); pv.alpha_composite(B); pv.convert('RGB').save(OUTP + '/cats_gifts.jpg', quality=88)
    print(json.dumps({'atlas': list(A.size), 'f': J, 'gifts': list(B.size), 'g': IJ}, separators=(',', ':')))
