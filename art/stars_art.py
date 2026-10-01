#!/usr/bin/env python3
"""«Звездопад и телескоп» (st): eight star things, one for each meteor shower caught.
Jars of star dust, a star-water flask, a star lantern, a star-map scroll, a brass telescope, a glass furin.
Same brush toolkit as art/items.py; everything goes into one atlas.
Usage: stars_art.py <outdir>  →  <outdir>/atlas_st.webp + prints the JS rows (id, w, h, at)."""
import json, math, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.argv = sys.argv[:2] if len(sys.argv) > 1 else [sys.argv[0], '.']
import paint as P
import items as I
from items import px, canvas, fill, volume, soft, floor_shadow, line, ell, poly, H, dk, lt, SERIF

OUT = sys.argv[1]
IMGS, ROWS = [], []


def save(img, iid, anchor='b', glow=None):
    out = img.resize((P.W, P.H), Image.LANCZOS)
    a = np.asarray(out, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * .9
    a[..., :3] += np.random.default_rng(sum(map(ord, iid))).normal(0, 3, a.shape[:2])[..., None]
    IMGS.append((iid, Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')))
    r = {'id': iid, 'w': P.W, 'h': P.H, 'a': anchor}
    if glow: r['glow'] = glow
    ROWS.append(r)


def rrect_mask(img, box, r):
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).rounded_rectangle([px(v) for v in box], px(r), fill=255); return m


def ell_mask(img, box):
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).ellipse([px(v) for v in box], fill=255); return m


def glint(d, x, y, r, col):
    """A four-point star sparkle."""
    w = max(.6, r * .16)
    d.polygon([(px(x - r), px(y)), (px(x), px(y - w)), (px(x + r), px(y)), (px(x), px(y + w))], fill=col)
    d.polygon([(px(x), px(y - r)), (px(x - w), px(y)), (px(x), px(y + r)), (px(x + w), px(y))], fill=col)


def dust(img, mask, box, col, seed, n=160, glints=5, level=.0):
    """Glowing star dust inside a mask: a soft glow, grains of light and a few sparkles."""
    x0, y0, x1, y1 = box; rr = random.Random(seed); c = H(col)
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    top = y0 + (y1 - y0) * level
    d.ellipse([px(x0 - 6), px(top), px(x1 + 6), px(y1 + 24)], fill=c[:3] + (150,))
    l = l.filter(ImageFilter.GaussianBlur(9 * P.SS)); d = ImageDraw.Draw(l)
    for _ in range(n):
        x, y = rr.uniform(x0, x1), top + (y1 - top) * rr.random() ** .7
        s = rr.choice((.7, .9, 1.1, 1.4, 2.0)); a = rr.randint(120, 255)
        cc = lt(c, rr.uniform(.2, .8))[:3] + (a,)
        d.ellipse([px(x - s), px(y - s), px(x + s), px(y + s)], fill=cc)
    for _ in range(glints):
        glint(d, rr.uniform(x0 + 6, x1 - 6), rr.uniform(top + 4, y1 - 6), rr.uniform(4, 8), (255, 255, 240, 235))
    a = np.asarray(l, np.float32); a[..., 3] *= np.asarray(mask, np.float32) / 255
    img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))


def cork(img, cx, y0, w, h, seed):
    fill(img, '#8a6a44', seed, rect=(cx - w / 2, y0, cx + w / 2, y0 + h), scale=3, contrast=1.1)
    volume(img, (cx - w / 2, y0, cx + w / 2, y0 + h), .6, .35)
    ell(img, (cx - w / 2, y0 - 4, cx + w / 2, y0 + 4), '#a8845a')


def label(img, x0, y0, x1, y1, ch, seed, ink='#2a1a12'):
    fill(img, '#e6dcc0', seed, rect=(x0, y0, x1, y1), scale=5, contrast=.5, dark=.12, light=.08)
    I.text(img, ch, (x0 + x1) / 2, (y0 + y1) / 2 - 2, (y1 - y0) * .55, ink, SERIF, brush=True)
    ImageDraw.Draw(img).rectangle([px(x1 - 9), px(y1 - 9), px(x1 - 3), px(y1 - 3)], fill=H('#b8322a'))


def jar(iid, col, ch, seed, tall=False):
    """A glass jar of star dust with a cork, twine and a paper label."""
    w, h = (116, 176) if tall else (130, 160); cx = w / 2
    img = canvas(w, h); floor_shadow(img, cx, h - 5, w * .4)
    body = (14, 52, w - 14, h - 8) if tall else (10, 46, w - 10, h - 8)
    m = rrect_mask(img, body, 22 if tall else 34)
    g = Image.new('RGBA', img.size, (150, 176, 196, 64)); g.putalpha(Image.fromarray((np.asarray(m, np.float32) * .3).astype(np.uint8)))
    img.alpha_composite(g)                                                                       # glass
    dust(img, m, body, col, seed, n=210 if tall else 190, glints=6, level=.28)
    soft(img, lambda d: d.rounded_rectangle([px(body[0] + 6), px(body[1] + 10), px(body[0] + 15), px(body[3] - 16)], px(4), fill=(255, 255, 255, 80)), 1.2)   # highlight
    soft(img, lambda d: d.rounded_rectangle([px(v) for v in body], px(22 if tall else 34), outline=(220, 236, 246, 120), width=px(2)), .6)                     # rim of glass
    nk = (cx - 26, 32, cx + 26, 52)
    soft(img, lambda d: d.rounded_rectangle([px(v) for v in nk], px(6), fill=(170, 196, 214, 70), outline=(220, 236, 246, 130), width=px(1.6)), .4)
    cork(img, cx, 14, 42, 24, seed + 1)
    line(img, [(cx - 27, 44), (cx + 27, 44)], '#c9a87a', 2.6); line(img, [(cx + 18, 44), (cx + 26, 60), (cx + 22, 70)], '#c9a87a', 1.8)
    label(img, cx - 19, (body[1] + body[3]) / 2 - 18, cx + 19, (body[1] + body[3]) / 2 + 20, ch, seed + 2)
    save(img, iid, glow=[int(cx), int(body[3] - 30)])


def flask():     # Eta-Aquariids: star water in a round-bellied glass flask
    w, h = 130, 180; cx = w / 2
    img = canvas(w, h); floor_shadow(img, cx, h - 5, 50)
    m = ell_mask(img, (12, 62, w - 12, h - 6)); mn = rrect_mask(img, (cx - 15, 24, cx + 15, 72), 6)
    mm = Image.fromarray(np.maximum(np.asarray(m), np.asarray(mn)))
    g = Image.new('RGBA', img.size, (150, 180, 200, 70)); g.putalpha(Image.fromarray((np.asarray(mm, np.float32) * .3).astype(np.uint8))); img.alpha_composite(g)
    wm = Image.fromarray((np.asarray(m, np.float32) * (np.arange(img.size[1])[:, None] > px(100))).astype(np.uint8))
    wl = Image.new('RGBA', img.size, (40, 96, 150, 200)); wl.putalpha(Image.fromarray((np.asarray(wm, np.float32) * .78).astype(np.uint8))); img.alpha_composite(wl)
    dust(img, wm, (16, 100, w - 16, h - 8), '#9fd4ff', 31, n=120, glints=5)
    soft(img, lambda d: d.arc([px(16), px(96), px(w - 16), px(112)], 0, 180, fill=(210, 236, 255, 170), width=px(1.6)), .4)    # water line
    soft(img, lambda d: d.ellipse([px(12), px(62), px(w - 12), px(h - 6)], outline=(220, 236, 246, 120), width=px(2)), .6)
    soft(img, lambda d: d.ellipse([px(24), px(80), px(40), px(124)], fill=(255, 255, 255, 70)), 1.2)
    cork(img, cx, 10, 30, 22, 33)
    line(img, [(cx - 16, 36), (cx + 16, 36)], '#3a5a8a', 2.4)
    label(img, cx - 16, 122, cx + 16, 156, '水', 34, '#1a2a4a')
    save(img, 'st_eta', glow=[int(cx), 140])


def lantern():   # Quadrantids: an indigo paper lantern pricked with stars
    img = canvas(150, 280); floor_shadow(img, 75, 272, 62)
    fill(img, '#26305a', 41, rect=(30, 64, 120, 236), scale=6, contrast=.8)
    soft(img, lambda d: d.ellipse([px(30), px(90), px(120), px(220)], fill=(190, 214, 255, 110)), 16)       # light inside
    rr = random.Random(4); l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    for _ in range(40):
        x, y, s = rr.uniform(36, 114), rr.uniform(70, 230), rr.choice((.8, 1, 1.3, 1.8))
        d.ellipse([px(x - s), px(y - s), px(x + s), px(y + s)], fill=(236, 244, 255, 255))
    for x, y in ((52, 104), (70, 98), (88, 108), (98, 128), (82, 140)):     # a little dipper of holes
        d.ellipse([px(x - 2.4), px(y - 2.4), px(x + 2.4), px(y + 2.4)], fill=(255, 255, 255, 255))
    d.line([(px(52), px(104)), (px(70), px(98)), (px(88), px(108)), (px(98), px(128)), (px(82), px(140))], fill=(220, 232, 255, 90), width=px(1))
    glint(d, 62, 176, 7, (255, 255, 255, 255)); glint(d, 96, 200, 5, (255, 255, 255, 230))
    img.alpha_composite(l.filter(ImageFilter.GaussianBlur(.5 * P.SS))); img.alpha_composite(l)
    volume(img, (30, 64, 120, 236), .25, .45)
    D = ImageDraw.Draw(img)
    for x in (24, 120): D.rectangle([px(x), px(54), px(x + 7), px(266)], fill=H('#1a120c'))
    for y in (54, 150, 236): D.rectangle([px(24), px(y), px(127), px(y + 6)], fill=H('#1a120c'))
    fill(img, '#2a1c12', 42, poly=[(14, 56), (136, 56), (118, 36), (32, 36)], scale=4)          # little roof
    line(img, [(75, 36), (75, 10)], '#1a120c', 3); ell(img, (68, 2, 82, 14), '#c9a24a')
    for x in (30, 114): line(img, [(x, 266), (x - 6, 276)], '#1a120c', 5)
    save(img, 'st_qua', glow=[75, 150])


def starmap():   # Draconids: a hanging scroll with a dragon winding between the stars
    img = canvas(150, 400)
    line(img, [(40, 4), (75, 0), (110, 4)], '#1a120c', 1.4)
    ImageDraw.Draw(img).rectangle([px(18), px(8), px(132), px(16)], fill=H('#2a1c14'))
    fill(img, '#3c2c4e', 51, rect=(16, 14, 134, 384), scale=6, contrast=1.1)
    fill(img, '#18203a', 52, rect=(28, 52, 122, 336), scale=9, contrast=.7, dark=.2, light=.12)
    rr = random.Random(9); d = ImageDraw.Draw(img)
    for _ in range(90):
        x, y, s = rr.uniform(32, 118), rr.uniform(56, 332), rr.choice((.5, .7, .9, 1.2))
        d.ellipse([px(x - s), px(y - s), px(x + s), px(y + s)], fill=(220, 226, 240, rr.randint(110, 230)))
    pts = [(96, 82), (82, 98), (92, 120), (70, 146), (56, 176), (74, 204), (90, 236), (70, 268), (48, 292), (60, 316)]   # Draco, loosely
    gold = H('#d8b048')
    d.line([(px(x), px(y)) for x, y in pts], fill=gold[:3] + (200,), width=px(1.3))
    for i, (x, y) in enumerate(pts):
        r = 3.2 if i in (0, 1, 2) else 2.2
        d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=(255, 248, 220, 255))
    I.text(img, '龍', 50, 84, 30, '#d8b048', SERIF, brush=True)
    d = ImageDraw.Draw(img); d.rectangle([px(98), px(304), px(112), px(318)], fill=H('#b8322a'))
    d.rectangle([px(10), px(378), px(140), px(394)], fill=H('#1e140e'))
    for x in (8, 132): d.rectangle([px(x), px(376), px(x + 10), px(396)], fill=H('#caa860'))
    save(img, 'st_dra', 't')


def telescope():  # Orionids: a small brass telescope on a wooden tripod
    img = canvas(220, 240); floor_shadow(img, 110, 232, 84)
    for a, b in (((110, 132), (40, 232)), ((110, 132), (180, 232)), ((110, 132), (116, 236))):
        line(img, [a, b], '#5a3e26', 7); line(img, [(a[0] - 1, a[1]), (b[0] - 1, b[1])], '#7a5a3a', 2)
    ell(img, (98, 120, 122, 144), '#3a2818')
    ang = math.radians(-28); ux, uy = math.cos(ang), math.sin(ang); nx, ny = -uy, ux
    def seg(c0, c1, r0, r1, col, seed):
        p = [(110 + ux * c0 + nx * r0, 118 + uy * c0 + ny * r0), (110 + ux * c1 + nx * r1, 118 + uy * c1 + ny * r1),
             (110 + ux * c1 - nx * r1, 118 + uy * c1 - ny * r1), (110 + ux * c0 - nx * r0, 118 + uy * c0 - ny * r0)]
        fill(img, col, seed, poly=p, scale=3, contrast=.9, dark=.4, light=.35)
    seg(-86, -40, 8, 10, '#a8823a', 61)          # eyepiece end
    seg(-42, 40, 13, 15, '#c09a48', 62)          # main tube
    seg(38, 92, 17, 19, '#b08a3e', 63)           # objective end
    for c, r in ((-40, 12), (0, 16), (38, 19), (90, 21)):     # brass rings
        line(img, [(110 + ux * c + nx * r, 118 + uy * c + ny * r), (110 + ux * c - nx * r, 118 + uy * c - ny * r)], '#6a4a1a', 3)
    volume(img, (14, 60, 214, 170), .5, .25, spec=.5)
    soft(img, lambda d: d.line([(px(110 + ux * -60 + nx * 6), px(118 + uy * -60 + ny * 6)), (px(110 + ux * 80 + nx * 12), px(118 + uy * 80 + ny * 12))], fill=(255, 240, 200, 150), width=px(2.2)), .6)
    ex, ey = 110 + ux * 92, 118 + uy * 92
    ell(img, (ex - 7, ey - 17, ex + 7, ey + 17), '#1a2238')
    soft(img, lambda d: d.ellipse([px(ex - 3), px(ey - 10), px(ex + 2), px(ey - 2)], fill=(200, 220, 255, 200)), .5)
    save(img, 'st_ori')


def bell():      # Geminids: a glass wind bell sprinkled with twin stars
    img = canvas(100, 260); d = ImageDraw.Draw(img)
    line(img, [(50, 0), (50, 46)], '#1a1410', 1.4)
    m = Image.new('RGBA', img.size, (0, 0, 0, 0)); md = ImageDraw.Draw(m)
    md.pieslice([px(12), px(42), px(88), px(152)], 180, 360, fill=(190, 214, 240, 150))
    rr = random.Random(5)
    for _ in range(18):
        x, y = rr.uniform(22, 78), rr.uniform(64, 94); s = rr.choice((.8, 1.1, 1.5)); md.ellipse([px(x - s), px(y - s), px(x + s), px(y + s)], fill=(255, 255, 255, 230))
    for x, y in ((38, 74), (60, 72)): glint(md, x, y, 6, (255, 252, 230, 255))
    md.ellipse([px(26), px(52), px(40), px(64)], fill=(255, 255, 255, 170))
    img.alpha_composite(m)
    d.line([(px(12), px(96)), (px(88), px(96))], fill=(230, 240, 250, 170), width=px(1.6))
    line(img, [(50, 94), (50, 148)], '#1a1410', 1.2); d.rectangle([px(46), px(142), px(54), px(150)], fill=H('#c9a24a'))
    fill(img, '#2a3358', 71, rect=(34, 150, 66, 256), scale=5, contrast=.8)
    I.text(img, '双', 50, 186, 22, '#e8dcb8', SERIF)
    d = ImageDraw.Draw(img)
    for x, y in ((44, 224), (56, 232)): glint(d, x, y, 4, (240, 232, 200, 255))
    save(img, 'st_gem', 't')


def pack():
    lst = sorted(IMGS, key=lambda t: -t[1].height); W = 1024; x = y = rowh = 0; pos = {}
    for iid, im in lst:
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[iid] = (x, y); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for iid, im in lst: at.paste(im, pos[iid])
    at.save(f'{OUT}/atlas_st.webp', 'WEBP', quality=88, alpha_quality=90, method=6)
    for r in ROWS: r['at'] = ['st', *pos[r['id']]]
    print('atlas', at.size); print(json.dumps(ROWS, ensure_ascii=False))
    prev = Image.new('RGBA', at.size, (30, 34, 44, 255)); prev.alpha_composite(at); prev.convert('RGB').save(__file__.rsplit('/', 1)[0] + '/out/st_preview.png' if '/' in __file__ else 'out/st_preview.png')


if __name__ == '__main__':
    jar('st_per', '#f0c860', '流', 11); jar('st_lyr', '#c8a8f0', '琴', 12, tall=True); jar('st_leo', '#a8c8f0', '獅', 13)
    flask(); lantern(); starmap(); telescope(); bell(); pack()
