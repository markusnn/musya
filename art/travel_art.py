#!/usr/bin/env python3
"""«Путешествия Муси» (add-on tv): 15 painted postcards of real Japan with a tiny Musya seen from behind,
15 souvenirs and a few sprites (bundle on her back, the call bell, the red post box).
Usage: cd art && python3 travel_art.py ../assets/items  →  atlas_tvp1.webp, atlas_tvp2.webp (postcards 560×380),
atlas_tvs.webp (souvenirs + sprites) and travel.json (rects); previews go to art/out/."""
import json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import hexc, mixc, fbm, textured_fill
import items as I
from items import px, canvas, fill, volume, soft, floor_shadow, line, ell, poly, text, H, dk, lt, SERIF, mask_poly
from room_items import blob, clip, cr

OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
CW, CH = 560, 380
BLACK, WHITE = (0, 0, 0, 255), (255, 255, 255, 255)


# ───────────── card helpers (final-pixel coords, the canvas is supersampled ×2) ─────────────
def card(): return canvas(CW, CH)
def rgba(c, a=255): c = H(c); return (c[0], c[1], c[2], a)


def vgrad(img, stops, y0=0, y1=CH, x0=0, x1=CW):
    """Vertical gradient through several colour stops, painted over a box."""
    h = px(y1 - y0); w = px(x1 - x0); t = np.linspace(0, 1, h)[:, None]
    ps = [s for s, _ in stops]; cs = [np.array(H(c)[:3], np.float32) for _, c in stops]
    rgb = np.zeros((h, 1, 3), np.float32)
    for i in range(3): rgb[..., i] = np.interp(t, ps, [c[i] for c in cs])
    rgb = np.repeat(rgb, w, 1)
    n = fbm(w, h, 60 * P.SS, 4, len(stops) * 7 + int(y0), (4, 1))[..., None]
    rgb = rgb * (0.94 + 0.12 * n)
    img.alpha_composite(Image.fromarray(np.dstack([np.clip(rgb, 0, 255), np.full((h, w), 255)]).astype(np.uint8), 'RGBA'), (px(x0), px(y0)))


def newl(img): return Image.new('RGBA', img.size, (0, 0, 0, 0))


def vol(img, lay, box, *a, **k):
    volume(lay, box, *a, **k); img.alpha_composite(lay)


def glowc(img, cx, cy, r, col, strength, squash=1.0):
    n = 64; yy, xx = np.mgrid[0:n, 0:n]
    d = np.sqrt(((xx - n / 2) / (n / 2)) ** 2 + ((yy - n / 2) / (n / 2 * squash)) ** 2)
    a = np.clip(1 - d, 0, 1) ** 2 * strength * 255
    g = Image.new('RGBA', (n, n), rgba(col)); g.putalpha(Image.fromarray(a.astype(np.uint8)))
    g = g.resize((px(2 * r), px(2 * r)), Image.BICUBIC); ox, oy = px(cx - r), px(cy - r)
    sx, sy = max(0, -ox), max(0, -oy); w, h = min(g.width - sx, img.width - ox - sx), min(g.height - sy, img.height - oy - sy)
    if w > 0 and h > 0: img.alpha_composite(g.crop((sx, sy, sx + w, sy + h)), (ox + sx, oy + sy))


def ridge(img, y, amp, col, seed, rough=3, peaks=None, fog=None, fog_amt=0.0, blur=0, dark=.35, light=.18):
    """A mountain/forest ridge: noisy silhouette down to the bottom of the card."""
    rng = np.random.default_rng(seed); xs = np.linspace(0, CW, 120)
    n = fbm(120, 2, 120 / rough, 4, seed)[0]
    ys = y - (n - .5) * amp * 2
    if peaks:
        for (pxc, ph, pw) in peaks: ys = ys - ph * np.exp(-((xs - pxc) / pw) ** 2)
    pts = [(float(x), float(v)) for x, v in zip(xs, ys)] + [(CW, CH + 2), (0, CH + 2)]
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); fill(lay, col, seed, poly=pts, scale=14, stretch=(3, 1), contrast=1.1, dark=dark, light=light)
    if fog is not None: lay = P.atmos(lay, H(fog), fog_amt, blur)
    img.alpha_composite(lay)


def mist(img, y0, y1, col, density, seed):
    P.set_size(CW, CH); img.alpha_composite(P.fog_layer(H(col), y0, y1, density, seed, scale=120))


def reflect(img, yl, y_end=CH, dark=.35, tint=None, ripple=3.0, seed=0):
    """Mirror everything above the water line into the water with a horizontal ripple and darkening."""
    a = np.asarray(img, np.float32); L = px(yl); E = px(y_end); h = E - L
    src = a[max(0, L - h):L][::-1]
    if src.shape[0] < h: src = np.concatenate([src, np.repeat(src[-1:], h - src.shape[0], 0)], 0)
    rows = np.arange(h); rng = np.random.default_rng(seed)
    shift = (np.sin(rows / (2.2 * P.SS) + rng.random() * 6) * ripple * P.SS * (0.3 + rows / h)).astype(int)
    out = np.empty_like(src)
    for i in range(h): out[i] = np.roll(src[i], shift[i], axis=0)
    out[..., :3] *= (1 - dark) * np.linspace(1, .8, h)[:, None, None]
    if tint is not None: out[..., :3] = out[..., :3] * .75 + np.array(H(tint)[:3], np.float32) * .25
    n = fbm(out.shape[1], h, 10 * P.SS, 3, seed + 3, (6, .3))
    out[..., :3] *= (0.9 + 0.2 * n)[..., None]
    lines = (np.sin(rows / (1.7 * P.SS) + np.sqrt(rows) * .8) > .97)[:, None]
    out[..., :3] = np.where(lines[..., None], out[..., :3] * 1.07 + 3, out[..., :3])
    a[L:E] = out; a[L:E, :, 3] = 255
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def stones(img, y0, y1, seed, base='#4a4a44', n=60, rmin=6, rmax=16):
    rr = random.Random(seed)
    for _ in range(n):
        x = rr.uniform(-10, CW + 10); y = rr.uniform(y0, y1); r = rr.uniform(rmin, rmax) * (0.6 + (y - y0) / (y1 - y0 + 1))
        P.stone(img, x, y, r, r * .45, rr.randint(0, 999), mixc(H(base), BLACK, rr.uniform(0, .3)), moss=False)


def snowfall(img, n, seed, col=(235, 240, 248)):
    rr = random.Random(seed); d = ImageDraw.Draw(img)
    for _ in range(n):
        x, y = rr.uniform(0, CW), rr.uniform(0, CH); r = rr.uniform(.6, 2.0)
        d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=col + (int(rr.uniform(110, 230)),))


def cedars(img, y, n, hmin, hmax, seed, pal=None, fogc=None, fog_amt=0.0, x0=-20, x1=CW + 20, w=(60, 90)):
    P.set_size(CW, CH); L = P.layer(); rr = random.Random(seed)
    for i in range(n):
        P.cedar(L, (x0 + (i + rr.uniform(0, 1)) * (x1 - x0) / n) * P.SS, y * P.SS, rr.uniform(hmin, hmax) * P.SS, rr.uniform(*w) * P.SS, seed * 10 + i, pal or P.PAL_CEDAR, P.BARK)
    if fogc is not None: L = P.atmos(L, H(fogc), fog_amt)
    img.alpha_composite(L)


def paw(img, x=CW - 34, y=CH - 30, col='#b8322a', s=1.0, a=175):
    """Musya's signature: a small ink paw print, like a hanko."""
    l = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l); c = rgba(col, a)
    d.ellipse([px(x - 8 * s), px(y - 3 * s), px(x + 8 * s), px(y + 9 * s)], fill=c)
    for dx, dy, r in ((-9, -7, 3.4), (-3.5, -12, 3.6), (3.5, -12, 3.6), (9, -7, 3.4)):
        d.ellipse([px(x + (dx - r) * s), px(y + (dy - r) * s), px(x + (dx + r) * s), px(y + (dy + r) * s)], fill=c)
    ar = np.asarray(l, np.float32); n = np.random.default_rng(int(x * 7 + y)).random(ar.shape[:2]); ar[..., 3] *= np.where(n < .18, .35, 1)
    img.alpha_composite(Image.fromarray(ar.astype(np.uint8), 'RGBA').filter(ImageFilter.GaussianBlur(.5 * P.SS)))


def bundle(img, x, base, s, col='#2a4a7a', fg='#e8e0d0'):
    """The furoshiki bundle Musya travels with."""
    out = img; img = newl(out)
    floor_shadow(img, x, base, 9 * s, 90)
    fill(img, col, 5, poly=[(x - 9 * s, base), (x - 11 * s, base - 8 * s), (x - 6 * s, base - 13 * s), (x + 6 * s, base - 13 * s), (x + 11 * s, base - 8 * s), (x + 9 * s, base)], scale=3, contrast=.8)
    d = ImageDraw.Draw(img)
    for k in range(5): d.ellipse([px(x - 8 * s + k * 4 * s), px(base - 9 * s), px(x - 6.8 * s + k * 4 * s), px(base - 7.8 * s)], fill=rgba(fg, 200))
    poly(img, [(x - 4 * s, base - 12 * s), (x - 7 * s, base - 19 * s), (x - 1 * s, base - 14 * s)], dk(H(col), .15))
    poly(img, [(x + 4 * s, base - 12 * s), (x + 7 * s, base - 19 * s), (x + 1 * s, base - 14 * s)], dk(H(col), .15))
    ell(img, (x - 2.2 * s, base - 15 * s, x + 2.2 * s, base - 11 * s), dk(H(col), .3))
    vol(out, img, (x - 12 * s, base - 20 * s, x + 12 * s, base), .5, .3)


def musya(img, x, base, h, rim='#ffc88a', rim_side=1, fur='#8a6242', seed=1, bag=True, look=0.0):
    """Tiny Musya from behind, sitting and looking at the view: tabby back, two ears, a curled tail."""
    fur = H(fur); r = h
    floor_shadow(img, x, base, r * .38, 120)
    tmp = Image.new('RGBA', img.size, (0, 0, 0, 0))
    # tail curls around on the ground
    tl = [(x + r * .18, base - r * .05), (x + r * .42, base - r * .04), (x + r * .55, base - r * .14), (x + r * .5, base - r * .24)]
    line(tmp, tl, dk(fur, .25), r * .1)
    body = [(x - r * .28, base), (x - r * .31, base - r * .22), (x - r * .24, base - r * .48), (x - r * .12, base - r * .62), (x + r * .12, base - r * .62),
            (x + r * .24, base - r * .48), (x + r * .31, base - r * .22), (x + r * .28, base)]
    blob(tmp, body, fur, seed, scale=3, contrast=1.1, k=.3, rim=.25)
    hx = x + look * r * .06
    head = [(hx - r * .2, base - r * .66), (hx - r * .22, base - r * .8), (hx - r * .14, base - r * .92), (hx + r * .14, base - r * .92), (hx + r * .22, base - r * .8), (hx + r * .2, base - r * .66), (hx, base - r * .6)]
    blob(tmp, head, fur, seed + 1, scale=3, contrast=1.1, k=.3, rim=.25)
    for sd in (-1, 1):
        poly(tmp, [(hx + sd * r * .07, base - r * .9), (hx + sd * r * .2, base - r * 1.04), (hx + sd * r * .2, base - r * .82)], dk(fur, .1))
        poly(tmp, [(hx + sd * r * .1, base - r * .9), (hx + sd * r * .18, base - r * .99), (hx + sd * r * .18, base - r * .86)], mixc(fur, H('#c08a78'), .4))
    # tabby stripes across the back and head
    m = mask_poly(tmp, poly=cr(body) + []); d = ImageDraw.Draw(tmp)
    def stripes(dd):
        for k in range(6):
            yy = base - r * (.14 + k * .085)
            dd.arc([px(x - r * .3), px(yy - r * .08), px(x + r * .3), px(yy + r * .1)], 200, 340, fill=rgba(dk(fur, .55), 190), width=max(1, px(r * .028)))
        dd.line([(px(x), px(base - r * .62)), (px(x), px(base - r * .1))], fill=rgba(dk(fur, .5), 160), width=max(1, px(r * .035)))
    clip(tmp, m, stripes)
    for k in range(3): line(tmp, [(hx - r * .06 + k * r * .06, base - r * .9), (hx - r * .06 + k * r * .06, base - r * .72)], dk(fur, .5), max(.4, r * .018))
    # rim light from the scene's light
    a = np.asarray(tmp, np.float32); al = a[..., 3] / 255
    sh = np.roll(al, -rim_side * max(1, px(r * .045)), axis=1); edge = np.clip(al - sh, 0, 1)
    rc = np.array(H(rim)[:3], np.float32)
    a[..., :3] = a[..., :3] * (1 - edge[..., None] * .8) + rc * edge[..., None] * .8
    img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'))
    if bag: bundle(img, x - r * .52, base, r * .017)


def finish_card(img, name, sat=.92, lift=(6, 7, 8), gamma=1.0, vig=.42):
    out = img.resize((CW, CH), Image.LANCZOS)
    out = P.grade(out, lift=lift, gamma=gamma, sat=sat, vignette=vig)
    out = P.grain(out, 4.5, hash(name) % 997)
    return out


# ───────────── pieces used by several cards ─────────────
VERM = '#c9452e'


def torii_front(img, cx, base, w, h, col=VERM, seed=0, fogc=None, fog_amt=0.0, black_feet=True, cap='#1c1412'):
    """A torii seen head-on (the tunnel of Inari, the sea gates)."""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); pw = max(1.2, w * .085)
    for sd in (-1, 1):
        x = cx + sd * w * .36
        fill(lay, col, seed + sd, rect=(x - pw / 2, base - h, x + pw / 2, base), scale=max(2, w / 30), stretch=(.2, 3), contrast=1.0)
        if black_feet: fill(lay, '#1a1414', seed + 5, rect=(x - pw / 2 - w * .005, base - h * .12, x + pw / 2 + w * .005, base), scale=3)
    fill(lay, col, seed + 2, rect=(cx - w * .46, base - h * .8, cx + w * .46, base - h * .72), scale=max(2, w / 30), stretch=(3, .3))
    pts = []
    for i in range(21):
        u = i / 20; pts.append((cx - w * .56 + w * 1.12 * u, base - h * 1.0 + (4 * (u - .5) ** 2) * h * .07))
    low = [(x, y + h * .09) for x, y in reversed(pts)]
    fill(lay, cap, seed + 3, poly=pts + low, scale=3, stretch=(3, .3))
    fill(lay, col, seed + 4, rect=(cx - w * .5, base - h * .92, cx + w * .5, base - h * .86), scale=3, stretch=(3, .3))
    if fogc is not None: lay = P.atmos(lay, H(fogc), fog_amt)
    img.alpha_composite(lay)


def inari_tunnel(img, vp, n, near_w, far_w, near_base, col=VERM, fogc='#f2b870', night=False, seed=0):
    """Senbon torii: dozens of gates receding to a glowing vanishing point."""
    vx, vy = vp
    zf = near_w / far_w
    for i in range(n):
        z = 1 + (zf - 1) * (1 - i / (n - 1)); k = 1 / z; u = i / (n - 1)
        w = near_w * k; h = w * 1.25; base = vy + (near_base - vy) * k
        amt = min(.92, (1 - k) ** 1.2 * (.8 if not night else .9))
        c = mixc(H(col), BLACK, .15 * (i % 2))
        torii_front(img, vx, base, w, h, c, seed + i, fogc, amt)


def deer(img, x, base, s, flip=1, stag=False, seed=0, col='#8a5a36', graze=False):
    col = H(col); lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    floor_shadow(lay, x, base, 26 * s, 100)
    for dx, sp in ((-16, -2), (-10, 2), (12, 2), (18, -2)):
        line(lay, [(x + dx * s * flip, base - 26 * s), (x + (dx + sp) * s * flip, base - 12 * s), (x + (dx + sp * .5) * s * flip, base)], dk(col, .35), 2.6 * s)
    blob(lay, [(x - 24 * s * flip, base - 34 * s), (x - 20 * s * flip, base - 44 * s), (x + 14 * s * flip, base - 46 * s), (x + 24 * s * flip, base - 38 * s), (x + 20 * s * flip, base - 24 * s), (x - 18 * s * flip, base - 24 * s)], col, seed, scale=3, k=.45)
    hy = base - (30 if graze else 66) * s; hx = x + (34 if graze else 28) * s * flip
    line(lay, [(x + 16 * s * flip, base - 40 * s), (hx - 4 * s * flip, hy + 6 * s)], col, 8 * s)
    blob(lay, [(hx - 7 * s * flip, hy - 4 * s), (hx + 2 * s * flip, hy - 7 * s), (hx + 12 * s * flip, hy + 2 * s), (hx + 10 * s * flip, hy + 6 * s), (hx - 4 * s * flip, hy + 6 * s)], col, seed + 1, scale=2, k=.4)
    poly(lay, [(hx - 5 * s * flip, hy - 5 * s), (hx - 13 * s * flip, hy - 12 * s), (hx - 3 * s * flip, hy - 9 * s)], dk(col, .15))
    if stag:
        for sd in (-1, 1):
            line(lay, [(hx - 2 * s * flip, hy - 6 * s), (hx - (4 + sd * 3) * s * flip, hy - 20 * s), (hx - (2 + sd * 7) * s * flip, hy - 28 * s)], '#d8c8a8', 1.6 * s)
    d = ImageDraw.Draw(lay); rr = random.Random(seed)
    for _ in range(14):
        sx, sy = x + rr.uniform(-16, 16) * s, base - rr.uniform(30, 42) * s
        d.ellipse([px(sx - s), px(sy - s * .8), px(sx + s), px(sy + s * .8)], fill=(236, 214, 180, 170))
    ell(lay, (hx + 9 * s * flip - 1.4 * s, hy - 1.4 * s + 2 * s, hx + 9 * s * flip + 1.4 * s, hy + 1.4 * s + 2 * s), '#141010')
    img.alpha_composite(lay)


def monkey(img, x, base, s, seed=0, flip=1, col='#6e6052', face='#d0604e', in_water=True):
    col = H(col); lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    blob(lay, [(x - 16 * s, base), (x - 18 * s, base - 16 * s), (x - 10 * s, base - 28 * s), (x + 10 * s, base - 28 * s), (x + 18 * s, base - 16 * s), (x + 16 * s, base)], col, seed, scale=2, contrast=1.3, k=.5)
    hx, hy = x + 3 * s * flip, base - 36 * s
    blob(lay, [(hx - 11 * s, hy + 6 * s), (hx - 12 * s, hy - 6 * s), (hx, hy - 13 * s), (hx + 12 * s, hy - 6 * s), (hx + 11 * s, hy + 6 * s), (hx, hy + 11 * s)], col, seed + 1, scale=2, contrast=1.3, k=.5)
    blob(lay, [(hx - 6 * s, hy + 6 * s), (hx - 7 * s, hy - 2 * s), (hx, hy - 6 * s), (hx + 7 * s, hy - 2 * s), (hx + 6 * s, hy + 6 * s), (hx, hy + 9 * s)], face, seed + 2, scale=2, k=.3)
    for sd in (-1, 1): ell(lay, (hx + sd * 3 * s - 1.1 * s, hy - 1 * s, hx + sd * 3 * s + 1.1 * s, hy + 1.2 * s), '#1a0e0a')
    d = ImageDraw.Draw(lay); rr = random.Random(seed)
    for _ in range(int(8 * s)):   # snow on the fur
        sx, sy = hx + rr.uniform(-10, 10) * s, hy - rr.uniform(6, 13) * s
        d.ellipse([px(sx - .8 * s), px(sy - .8 * s), px(sx + .8 * s), px(sy + .8 * s)], fill=(240, 244, 248, 200))
    img.alpha_composite(lay)


def cat(img, x, base, s, col, seed, flip=1, spots=None, sit=True):
    """A generic island cat, side view sitting (Aoshima)."""
    col = H(col); lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); floor_shadow(lay, x, base, 10 * s, 110)
    line(lay, [(x - 8 * s * flip, base - 1 * s), (x - 16 * s * flip, base - 3 * s), (x - 18 * s * flip, base - 9 * s)], dk(col, .1), 2.4 * s)
    blob(lay, [(x - 10 * s * flip, base), (x - 11 * s * flip, base - 10 * s), (x - 4 * s * flip, base - 20 * s), (x + 5 * s * flip, base - 20 * s), (x + 8 * s * flip, base - 8 * s), (x + 8 * s * flip, base)], col, seed, scale=2, k=.45)
    hx, hy = x + 4 * s * flip, base - 23 * s
    blob(lay, [(hx - 6 * s, hy + 4 * s), (hx - 7 * s, hy - 3 * s), (hx, hy - 7 * s), (hx + 7 * s, hy - 3 * s), (hx + 6 * s, hy + 4 * s)], col, seed + 1, scale=2, k=.45)
    for sd in (-1, 1): poly(lay, [(hx + sd * 2 * s, hy - 5 * s), (hx + sd * 6 * s, hy - 11 * s), (hx + sd * 7 * s, hy - 2 * s)], dk(col, .08))
    if spots:
        m = mask_poly(lay, poly=[(x - 12 * s, base + 1), (x - 12 * s, base - 30 * s), (x + 12 * s, base - 30 * s), (x + 12 * s, base + 1)])
        clip(lay, m, lambda d: [d.ellipse([px(x + a * s - r * s), px(base + b * s - r * s), px(x + a * s + r * s), px(base + b * s + r * s)], fill=rgba(spots)) for a, b, r in ((-5, -12, 5), (5, -24, 4), (3, -6, 3))])
    img.alpha_composite(lay)


def lantern_glow(img, x, y, r, col='#ffb45a', s=.6):
    glowc(img, x, y, r * 4, col, s); fill(img, '#f0b060', 3, ell=(x - r, y - r * 1.3, x + r, y + r * 1.3), scale=2, contrast=.5)
    ell(img, (x - r * .6, y - r * 1.45, x + r * .6, y - r * 1.2), '#1a120c'); ell(img, (x - r * .6, y + r * 1.2, x + r * .6, y + r * 1.45), '#1a120c')


def stone_lantern(img, x, base, h, seed, lit=True, col='#6a6a60'):
    s = h / 100; out = img; img = newl(out)
    for (a, b, c, d_, k) in ((-18, -12, 18, 0, 0), (-6, -52, 6, -12, 1), (-16, -62, 16, -52, 2), (-12, -80, 12, -62, 3), (-24, -92, 24, -80, 4), (-5, -100, 5, -92, 5)):
        fill(img, col, seed + k, rect=(x + a * s, base + b * s, x + c * s, base + d_ * s), scale=2, contrast=1.1)
    fill(img, '#f2c070' if lit else '#1a1814', seed, rect=(x - 5 * s, base - 77 * s, x + 5 * s, base - 65 * s), scale=2, contrast=.4)
    vol(out, img, (x - 24 * s, base - 100 * s, x + 24 * s, base), .5, .3)
    if lit: glowc(out, x, base - 71 * s, 34 * s, '#ffb45a', .5)


def foliage(img, blobs, pal, seed, n=None, kind='leaf', size=(2.4, 5)):
    """Painted foliage mass in card coords (blobs in final px)."""
    rnd = random.Random(seed); B = [(cx * P.SS, cy * P.SS, rx * P.SS, ry * P.SS) for cx, cy, rx, ry in blobs]
    B = P.ragged(B, rnd, 6, .6); P.shadow_blobs(img, B, pal[0], 1.0)
    P.dab_mass(ImageDraw.Draw(img), B, n or 90 * len(B), kind, pal, rnd, size=size)


MAPLE_RED = [hexc('#4a120c'), hexc('#6e1c10'), hexc('#9a2c14'), hexc('#c44a1c'), hexc('#e0762a'), hexc('#f0a040')]
PINE = [hexc('#0e1611'), hexc('#162219'), hexc('#1f3023'), hexc('#2b4230'), hexc('#3e5a44')]
SAKURA = [hexc('#6e3a48'), hexc('#9a5566'), hexc('#c07a8c'), hexc('#dc9fb0'), hexc('#efc3cf'), hexc('#f8dde4')]


# ───────────── the fifteen postcards ─────────────
def c_fushimi():
    img = card(); vgrad(img, [(0, '#1a2416'), (.5, '#3a4a2a'), (1, '#1a1a12')])
    foliage(img, [(80, 90, 140, 90), (480, 80, 140, 90), (60, 250, 120, 80), (500, 240, 120, 80)], [hexc(c) for c in ('#0e160c', '#16220f', '#22321a', '#34482a', '#4e6a3a')], 9, size=(2.4, 5))
    glowc(img, 280, 200, 170, '#ffd08a', .9); glowc(img, 280, 200, 60, '#fff0c8', .9)
    inari_tunnel(img, (280, 200), 30, 640, 34, 440, VERM, '#ffcf8a', seed=10)
    fill(img, '#5a5048', 3, poly=[(0, 380), (560, 380), (320, 236), (240, 236)], scale=6, stretch=(3, 1), contrast=1.2)
    glowc(img, 280, 300, 120, '#ffb45a', .35, .4)
    for x in (70, 490): lantern_glow(img, x, 250, 7, s=.45)
    musya(img, 282, 356, 60, rim='#ffd49a', seed=11)
    paw(img); return finish_card(img, 'fushimi', sat=.95)


def c_fuji():
    img = card(); vgrad(img, [(0, '#1c2a44'), (.38, '#6a6a8a'), (.56, '#e8a88a'), (.62, '#f0c8a0')], 0, 236)
    glowc(img, 400, 226, 120, '#ffd8b0', .6)
    fx = 290; pts = [(fx - 250, 236), (fx - 120, 170), (fx - 40, 92), (fx - 18, 72), (fx + 20, 70), (fx + 44, 92), (fx + 130, 172), (fx + 260, 236)]
    M = newl(img); fill(M, '#4a5a78', 7, poly=pts, scale=10, contrast=1.1)
    n = fbm(200, 1, 12, 3, 4)[0]
    snow = [(fx - 18, 72), (fx + 20, 70), (fx + 44, 92)] + [(fx + 70 - k * 140 / 19, 118 + (n[k * 10] - .5) * 30 + math.sin(k * 1.7) * 9) for k in range(20)] + [(fx - 40, 92)]
    fill(M, '#e8eef4', 8, poly=snow, scale=4, stretch=(.3, 2), contrast=1.2, dark=.25)
    vol(img, M, (fx - 250, 70, fx + 260, 236), .9, .1, lx=.7, ly=-.4)
    mist(img, 170, 236, '#d8b8b0', .5, 3)
    ridge(img, 222, 10, '#1e2a30', 21, rough=5, fog='#8a8aa0', fog_amt=.35)
    ridge(img, 236, 4, '#141c20', 22, rough=8)
    img2 = reflect(img, 240, 380, dark=.3, tint='#2a3450', ripple=2.4, seed=5); img.paste(img2)
    fill(img, '#2a2a2c', 9, poly=[(0, 380), (0, 318), (60, 300), (170, 312), (250, 336), (290, 380)], scale=5, contrast=1.3)
    for x, y, r in ((90, 306, 22), (170, 318, 16)): P.stone(img, x, y, r, r * .5, int(x), hexc('#3a3a36'), moss=True)
    P.set_size(CW, CH); L = P.layer(); P.pine(L, -30 * P.SS, 400 * P.SS, 340 * P.SS, 17, PINE, P.BARK, lean=.9, pads=4, spread=.8); img.alpha_composite(L)
    musya(img, 160, 312, 44, rim='#ffc8a8', rim_side=1, seed=12)
    paw(img); return finish_card(img, 'fuji', sat=.9)


def c_nara():
    img = card(); vgrad(img, [(0, '#2a2418'), (.5, '#5a4a2a'), (1, '#2a2416')])
    glowc(img, 360, 170, 220, '#f0c070', .6)
    cedars(img, 250, 7, 300, 380, 31, fogc='#b89a60', fog_amt=.55)
    mist(img, 150, 270, '#c8a870', .45, 32)
    cedars(img, 270, 5, 360, 420, 33, fogc='#8a7040', fog_amt=.25)
    fill(img, '#4a4a2c', 34, poly=[(0, 250), (560, 250), (560, 380), (0, 380)], scale=10, stretch=(4, 1), contrast=1.2)
    glowc(img, 330, 300, 200, '#f0b060', .25, .4)
    for i, x in enumerate((452, 392, 348)): stone_lantern(img, x, 270 + i * -6, 58 - i * 12, 40 + i)
    for i, x in enumerate((60, 120)): stone_lantern(img, x, 262 - i * 4, 46 - i * 10, 50 + i)
    deer(img, 200, 290, .9, 1, False, 61, graze=True)
    deer(img, 430, 322, 1.25, -1, True, 62)
    deer(img, 330, 360, 1.0, -1, False, 63)
    musya(img, 250, 364, 48, rim='#ffc070', rim_side=1, seed=13, look=.6)
    paw(img); return finish_card(img, 'nara')


def c_arashiyama():
    img = card(); vgrad(img, [(0, '#c8d8a8'), (.5, '#5a7a48'), (1, '#1e2a18')])
    rr = random.Random(41)
    for layer_i, (n, wmin, wmax, amt) in enumerate(((40, 3, 6, .6), (26, 6, 11, .35), (14, 11, 20, .1))):
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        for i in range(n):
            x = rr.uniform(-20, CW + 20)
            if 230 < x < 330 and layer_i == 2: x += 120
            w = rr.uniform(wmin, wmax); col = mixc(H('#5a8a3a'), H('#a8c070'), rr.random() * .6)
            lean = rr.uniform(-8, 8)
            fill(lay, col, 400 + i + layer_i * 50, poly=[(x - w / 2, 380), (x + w / 2, 380), (x + w / 2 + lean, -5), (x - w / 2 + lean, -5)], scale=3, stretch=(.2, 4), contrast=1.2)
            for k in range(int(rr.uniform(3, 6))):
                yy = rr.uniform(20, 360); d = ImageDraw.Draw(lay)
                d.line([(px(x - w / 2 + lean * (1 - yy / 380)), px(yy)), (px(x + w / 2 + lean * (1 - yy / 380)), px(yy))], fill=rgba(dk(col, .4), 220), width=max(1, px(w * .18)))
        volume(lay, (0, 0, CW, CH), .3, 0, lx=-.8, ly=0)
        img.alpha_composite(P.atmos(lay, H('#dde8c0'), amt))
        if layer_i == 0: mist(img, 160, 380, '#e0e8c8', .35, 42)
    fill(img, '#6a6450', 43, poly=[(160, 380), (400, 380), (300, 250), (270, 250)], scale=5, stretch=(3, 1), contrast=1.1)
    foliage(img, [(40, 300, 70, 40), (520, 310, 70, 44)], [hexc(c) for c in ('#16240f', '#22361a', '#2e4a22', '#44652e', '#5f8440')], 44, size=(2, 4))
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for k in range(5): d.polygon([(px(200 + k * 50), 0), (px(230 + k * 50), 0), (px(310 + k * 30), px(380)), (px(280 + k * 30), px(380))], fill=(255, 250, 210, 26))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(6 * P.SS)))
    musya(img, 288, 350, 46, rim='#f8f4d0', seed=14)
    paw(img); return finish_card(img, 'arashiyama', sat=.95)


def c_itsukushima():
    img = card(); vgrad(img, [(0, '#2a2044'), (.3, '#7a4a6a'), (.52, '#f0905a'), (.6, '#f8c080')], 0, 228)
    glowc(img, 150, 222, 110, '#ffd090', .8)
    ridge(img, 196, 18, '#3a2a40', 51, rough=3, peaks=[(420, 40, 90)], fog='#b07080', fog_amt=.5)
    ridge(img, 214, 8, '#2a2030', 52, rough=6, fog='#a06070', fog_amt=.3)
    fill(img, '#2a2030', 53, rect=(0, 226, 560, 228))
    x, b, w, h = 330, 262, 150, 142
    for sd in (-1, 1):
        for dx in (-.47, -.25):
            fill(img, '#9a3020', 54, rect=(x + sd * w * .36 + sd * dx * 50 - 3, b - h * .55, x + sd * w * .36 + sd * dx * 50 + 3, b), scale=2)
    torii_front(img, x, b, w, h, '#d44a2a', 55, black_feet=False)
    img2 = reflect(img, 228, 380, dark=.28, tint='#402040', ripple=3.2, seed=6); img.paste(img2)
    glowc(img, 150, 250, 90, '#ffc070', .35, .3)
    fill(img, '#3a3430', 56, poly=[(0, 380), (0, 330), (140, 322), (250, 340), (300, 380)], scale=5, contrast=1.3)
    stone_lantern(img, 60, 340, 80, 57)
    musya(img, 170, 336, 44, rim='#ffb070', rim_side=1, seed=15)
    paw(img); return finish_card(img, 'itsukushima')


def c_nachi():
    img = card(); vgrad(img, [(0, '#8a9aa0'), (.5, '#c0c8c0'), (1, '#4a5a50')])
    ridge(img, 150, 30, '#3a4a40', 61, rough=3, peaks=[(420, 90, 120)], fog='#c8d0c8', fog_amt=.5)
    cl = newl(img); fill(cl, '#34403a', 62, poly=cr([(340, 60), (380, 24), (470, 18), (520, 50), (548, 180), (540, 300), (330, 300), (318, 180)]), scale=5, stretch=(1, 3), contrast=1.4)
    foliage(cl, [(350, 60, 40, 20), (500, 40, 50, 22), (530, 150, 30, 40), (330, 170, 26, 40)], PINE, 60, kind='needle', size=(2.5, 5))
    img.alpha_composite(P.atmos(cl, H('#b8c4c0'), .35))
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    fill(lay, '#e8eef0', 63, poly=[(422, 30), (434, 30), (442, 290), (414, 290)], scale=2, stretch=(.1, 6), contrast=1.6, dark=.3)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(.6 * P.SS)))
    mist(img, 220, 320, '#f0f4f4', .8, 64)
    cedars(img, 330, 6, 200, 280, 65, fogc='#b8c4bc', fog_amt=.35, x0=380, x1=600)
    # three-storied pagoda of Seiganto-ji
    px0, base = 190, 300; out = img; img = newl(out)
    for k in range(3):
        y = base - k * 58; w = 92 - k * 14
        fill(img, '#b8402a', 66 + k, rect=(px0 - w * .34, y - 40, px0 + w * .34, y), scale=2, stretch=(.3, 2))
        for c in range(3): fill(img, '#2a1a14', 70 + k + c, rect=(px0 - w * .26 + c * w * .2, y - 32, px0 - w * .2 + c * w * .2, y - 8), scale=2)
        roof = [(px0 - w * .78, y - 36), (px0 - w * .5, y - 50), (px0 + w * .5, y - 50), (px0 + w * .78, y - 36), (px0 + w * .6, y - 42), (px0 - w * .6, y - 42)]
        fill(img, '#2c2a28', 80 + k, poly=roof, scale=3, contrast=1.2)
        line(img, [(px0 - w * .78, y - 37), (px0 + w * .78, y - 37)], '#a8a098', 1.2)
    line(img, [(px0, base - 3 * 58 + 8), (px0, base - 3 * 58 - 40)], '#8a7a4a', 2.4)
    for k in range(6): ell(img, (px0 - 4, base - 3 * 58 - 6 * k - 4, px0 + 4, base - 3 * 58 - 6 * k), '#9a8a50')
    vol(out, img, (px0 - 80, 110, px0 + 80, base), .6, .2); img = out
    cedars(img, 330, 4, 190, 260, 67, fogc='#8a9a90', fog_amt=.3, x0=-40, x1=120)
    fill(img, '#4a4c46', 68, poly=[(0, 380), (0, 332), (560, 316), (560, 380)], scale=6, contrast=1.2)
    for i in range(14): P.stone(img, 20 + i * 40, 338 - i * 1.2, 22, 10, 90 + i, hexc('#5a5c54'), moss=True)
    musya(img, 330, 328, 42, rim='#f0f4f0', seed=16)
    paw(img); return finish_card(img, 'nachi', sat=.9)


def c_jigokudani():
    img = card(); vgrad(img, [(0, '#8a94a0'), (.6, '#c8d0d8'), (1, '#a0a8b0')])
    cedars(img, 190, 9, 170, 230, 71, pal=[hexc('#2a3430'), hexc('#34403a'), hexc('#46524a'), hexc('#8a9690'), hexc('#dde4e8')], fogc='#c8d0d8', fog_amt=.45)
    fill(img, '#e4e8ee', 72, poly=[(0, 380), (0, 190), (160, 200), (400, 186), (560, 196), (560, 380)], scale=8, contrast=.7, dark=.15)
    pool_pts = [(40, 330), (60, 262), (200, 236), (380, 240), (520, 270), (530, 340), (300, 360)]
    fill(img, '#4a7078', 73, poly=cr(pool_pts), scale=10, stretch=(4, 1), contrast=1.1, light=.3)
    for i, (x, y, r) in enumerate(((60, 256, 30), (200, 232, 26), (400, 236, 34), (520, 268, 28), (30, 330, 36), (530, 340, 32), (300, 364, 40))):
        P.stone(img, x, y, r, r * .55, 74 + i, hexc('#5a5854'), moss=False)
        fill(img, '#eef2f6', 80 + i, poly=cr([(x - r * .85, y - r * .3), (x - r * .4, y - r * .6), (x + r * .3, y - r * .62), (x + r * .85, y - r * .3), (x + r * .2, y - r * .38)]), scale=3, contrast=.6, dark=.12)
    monkey(img, 190, 300, 1.2, 81); monkey(img, 280, 290, 1.0, 82, -1); monkey(img, 376, 306, 1.3, 83)
    fill(img, '#4a7078', 84, poly=[(120, 300), (440, 300), (440, 330), (120, 330)], scale=8, stretch=(4, 1), contrast=1.0)
    img.alpha_composite(Image.new('RGBA', img.size, (0, 0, 0, 0)))
    mist(img, 200, 330, '#f0f4f8', .75, 85)
    fill(img, '#e8ecf2', 86, poly=[(380, 380), (420, 346), (520, 336), (560, 350), (560, 380)], scale=5, contrast=.6, dark=.15)
    musya(img, 470, 350, 40, rim='#ffffff', rim_side=-1, seed=17, look=-.5)
    snowfall(img, 160, 87)
    paw(img, 40, CH - 30); return finish_card(img, 'jigokudani', sat=.85)


def c_himeji():
    img = card(); vgrad(img, [(0, '#3a4a6a'), (.5, '#b8a0a8'), (1, '#e8c0a0')], 0, 300)
    cx = 300; out = img; img = newl(out)
    fill(img, '#6a6a62', 91, poly=[(cx - 150, 300), (cx - 120, 226), (cx + 120, 226), (cx + 150, 300)], scale=3, contrast=1.3)
    d = ImageDraw.Draw(img)
    for yy in range(230, 300, 7): d.line([(px(cx - 150 + (300 - yy) * .4), px(yy)), (px(cx + 150 - (300 - yy) * .4), px(yy))], fill=(40, 40, 36, 120), width=px(.8))
    tiers = [(226, 220, 40), (186, 180, 36), (150, 146, 32), (118, 112, 30), (90, 80, 26)]
    for k, (y, w, h) in enumerate(tiers):
        fill(img, '#ecebe4', 92 + k, rect=(cx - w * .42, y - h, cx + w * .42, y), scale=4, contrast=.5, dark=.12)
        nw = max(2, int(w / 60))
        for c in range(nw): wx = cx - w * .3 + c * (w * .6) / max(1, nw - 1); fill(img, '#3a3a3c', 95 + c, rect=(wx - 2.5, y - h * .55, wx + 2.5, y - h * .35), scale=2)
        roof = [(cx - w * .6, y - h + 4), (cx - w * .42, y - h - 10), (cx + w * .42, y - h - 10), (cx + w * .6, y - h + 4), (cx + w * .5, y - h - 1), (cx - w * .5, y - h - 1)]
        fill(img, '#5a6068', 100 + k, poly=roof, scale=3, contrast=1.1)
        if k % 2 == 1: fill(img, '#5a6068', 105 + k, poly=[(cx - 20, y - h - 6), (cx, y - h - 26), (cx + 20, y - h - 6)], scale=2)
        line(img, [(cx - w * .6, y - h + 4), (cx + w * .6, y - h + 4)], '#f0f0ea', 1.1)
    fill(img, '#5a6068', 110, poly=[(cx - 34, 58), (cx, 36), (cx + 34, 58)], scale=2)
    vol(out, img, (cx - 150, 36, cx + 150, 300), .5, .1, lx=-.8, ly=-.2); img = out
    glowc(img, cx, 180, 180, '#ffe0c0', .25)
    foliage(img, [(40, 250, 90, 60), (110, 300, 80, 50), (500, 250, 90, 60), (460, 300, 70, 46)], [hexc(c) for c in ('#5a2a38', '#8a4a5a', '#c07a8c', '#dc9fb0', '#efc3cf', '#f8dde4')], 111, size=(2, 4))
    fill(img, '#3a4a30', 112, poly=[(0, 380), (0, 318), (560, 312), (560, 380)], scale=8, stretch=(4, 1), contrast=1.2)
    fill(img, '#2a3a44', 113, rect=(0, 300, 560, 318), scale=8, stretch=(6, 1))
    rr = random.Random(114); dd = ImageDraw.Draw(img)
    for _ in range(90):
        x, y = rr.uniform(0, CW), rr.uniform(160, 380); dd.ellipse([px(x - 1.6), px(y - 1), px(x + 1.6), px(y + 1)], fill=(248, 214, 224, 200))
    musya(img, 300, 360, 46, rim='#ffe0d0', seed=18)
    paw(img); return finish_card(img, 'himeji', sat=.9)


def c_kamakura():
    img = card(); vgrad(img, [(0, '#5a6a58'), (.6, '#a8a888'), (1, '#4a4a3a')])
    foliage(img, [(80, 120, 120, 90), (480, 110, 130, 90), (280, 60, 200, 60)], [hexc(c) for c in ('#1a2616', '#24341c', '#324a26', '#46603a', '#62804a')], 121, size=(2.4, 5))
    img2 = P.atmos(img, H('#c0c0a0'), .25); img.paste(img2)
    fill(img, '#7a7a70', 122, rect=(120, 318, 440, 350), scale=4, contrast=1.2)
    B = '#5e7a6c'; cx = 280; out = img; img = newl(out)
    blob(img, [(cx - 150, 320), (cx - 140, 280), (cx - 90, 262), (cx + 90, 262), (cx + 140, 280), (cx + 150, 320)], B, 123, scale=4, contrast=1.3, k=.6)
    blob(img, [(cx - 92, 290), (cx - 100, 200), (cx - 70, 150), (cx + 70, 150), (cx + 100, 200), (cx + 92, 290)], B, 124, scale=4, contrast=1.3, k=.6)
    blob(img, [(cx - 50, 270), (cx - 40, 252), (cx + 40, 252), (cx + 50, 270), (cx, 280)], lt(H(B), .08), 125, scale=3, k=.3)
    line(img, [(cx - 44, 262), (cx + 44, 262)], dk(H(B), .3), 1.2)
    blob(img, [(cx - 30, 150), (cx - 44, 110), (cx - 38, 70), (cx, 52), (cx + 38, 70), (cx + 44, 110), (cx + 30, 150)], B, 126, scale=3, contrast=1.3, k=.6)
    d = ImageDraw.Draw(img); rr = random.Random(127)
    for _ in range(90):
        x, y = cx + rr.uniform(-34, 34), rr.uniform(56, 96)
        if ((x - cx) / 38) ** 2 + ((y - 90) / 40) ** 2 < 1: d.ellipse([px(x - 2), px(y - 2), px(x + 2), px(y + 2)], fill=rgba(dk(H(B), .35), 200))
    for sd in (-1, 1): line(img, [(cx + sd * 38, 96), (cx + sd * 46, 128)], dk(H(B), .3), 5)
    for sd in (-1, 1): line(img, [(cx + sd * 20, 106), (cx + sd * 12, 108), (cx + sd * 5, 106)], dk(H(B), .5), 1.8)
    line(img, [(cx, 110), (cx, 122)], dk(H(B), .3), 1.4); line(img, [(cx - 6, 132), (cx + 6, 132)], dk(H(B), .45), 1.4)
    vol(out, img, (cx - 150, 52, cx + 150, 320), .7, .2, lx=-.7, ly=-.5); img = out
    glowc(img, cx - 60, 140, 120, '#ffe0a0', .2)
    fill(img, '#8a8878', 128, poly=[(0, 380), (0, 350), (560, 346), (560, 380)], scale=6, stretch=(4, 1))
    fill(img, '#3a3a36', 129, rect=(262, 330, 298, 356), scale=2); glowc(img, 280, 322, 20, '#ffb060', .5)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); line(lay, [(280, 326), (284, 300), (276, 270), (286, 240)], (220, 220, 210, 60), 4); img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(3 * P.SS)))
    musya(img, 200, 368, 40, rim='#ffe8b0', seed=19, look=.4)
    paw(img); return finish_card(img, 'kamakura', sat=.88)


def c_shirakawa():
    img = card(); vgrad(img, [(0, '#0c1428'), (.5, '#1c2a44'), (1, '#2a3a52')], 0, 240)
    ridge(img, 150, 20, '#d0d8e4', 131, rough=3, peaks=[(150, 40, 90)], fog='#5a6a84', fog_amt=.55, dark=.2)
    cedars(img, 220, 12, 70, 110, 132, pal=[hexc('#0a0e14'), hexc('#121820'), hexc('#1a222c'), hexc('#6a7888'), hexc('#c8d4e0')], fogc='#2a3a52', fog_amt=.4)
    fill(img, '#c8d2e0', 133, rect=(0, 226, 560, 380), scale=10, stretch=(4, 1), contrast=.6, dark=.2)
    for (hx, hb, hw, hh) in ((110, 250, 110, 90), (430, 256, 130, 104), (270, 300, 170, 140)):
        fill(img, '#3a2a1c', hx, rect=(hx - hw * .42, hb - hh * .32, hx + hw * .42, hb), scale=3, contrast=1.1)
        for k in range(3):
            wx = hx - hw * .3 + k * hw * .24; fill(img, '#ffc060', hx + k, rect=(wx, hb - hh * .26, wx + hw * .14, hb - hh * .1), scale=2, contrast=.4)
            glowc(img, wx + hw * .07, hb - hh * .18, hw * .22, '#ffb050', .45)
        roof = [(hx - hw * .56, hb - hh * .3), (hx, hb - hh * 1.1), (hx + hw * .56, hb - hh * .3)]
        fill(img, '#5a4a36', hx + 7, poly=roof, scale=3, stretch=(.5, 1.5), contrast=1.2)
        snow = [(hx - hw * .58, hb - hh * .28), (hx - hw * .5, hb - hh * .4), (hx, hb - hh * 1.12), (hx + hw * .5, hb - hh * .4), (hx + hw * .58, hb - hh * .28), (hx + hw * .3, hb - hh * .5), (hx, hb - hh * .88), (hx - hw * .3, hb - hh * .5)]
        fill(img, '#e8eef6', hx + 9, poly=snow, scale=3, contrast=.6, dark=.2)
        fill(img, '#ffc060', hx + 11, rect=(hx - hw * .06, hb - hh * .7, hx + hw * .06, hb - hh * .56), scale=2, contrast=.3)
        glowc(img, hx, hb + 10, hw * .7, '#ffa040', .22, .3)
    musya(img, 300, 360, 44, rim='#ffc070', seed=20)
    snowfall(img, 260, 134)
    paw(img); return finish_card(img, 'shirakawa', sat=.9, lift=(5, 6, 10))


def c_kinkakuji():
    img = card(); vgrad(img, [(0, '#6a8aa8'), (.6, '#c8d0c0')], 0, 200)
    ridge(img, 150, 20, '#2e4a30', 141, rough=3, fog='#a8b8a8', fog_amt=.3)
    foliage(img, [(60, 170, 90, 40), (500, 168, 90, 40), (180, 180, 60, 26), (380, 184, 60, 24)], PINE, 142, kind='needle', size=(3, 6))
    cx, base = 290, 200; out = img; img = newl(out)
    fill(img, '#5a5040', 143, rect=(cx - 70, base - 30, cx + 70, base), scale=3)
    for c in range(6): fill(img, '#e8e0cc', 144 + c, rect=(cx - 64 + c * 22, base - 26, cx - 50 + c * 22, base - 6), scale=2, contrast=.4)
    GOLD = '#d8a838'
    fill(img, GOLD, 150, rect=(cx - 64, base - 70, cx + 64, base - 38), scale=2, contrast=1.3, light=.45)
    fill(img, GOLD, 151, rect=(cx - 44, base - 112, cx + 44, base - 82), scale=2, contrast=1.3, light=.45)
    for (y, w) in ((base - 30, 170), (base - 70, 160), (base - 112, 120)):
        fill(img, '#2e2a26', int(y), poly=[(cx - w * .56, y + 2), (cx - w * .4, y - 10), (cx + w * .4, y - 10), (cx + w * .56, y + 2), (cx + w * .4, y - 4), (cx - w * .4, y - 4)], scale=3)
    fill(img, '#2e2a26', 152, poly=[(cx - 44, base - 118), (cx, base - 140), (cx + 44, base - 118)], scale=2)
    fill(img, GOLD, 153, poly=[(cx - 5, base - 140), (cx, base - 152), (cx + 6, base - 140)], scale=1, light=.5)
    vol(out, img, (cx - 90, base - 152, cx + 90, base), .6, .1, spec=.25); img = out
    img2 = reflect(img, 202, 380, dark=.25, tint='#2a4a40', ripple=2, seed=7); img.paste(img2)
    for x, y, rx in ((80, 250, 60), (470, 262, 70)):
        fill(img, '#3a4a34', int(x), ell=(x - rx, y - 12, x + rx, y + 12), scale=4)
        foliage(img, [(x, y - 20, rx * .6, 22)], PINE, int(x) + 1, kind='needle', size=(2.5, 5))
    fill(img, '#4a4a38', 154, poly=[(0, 380), (0, 340), (200, 332), (330, 350), (360, 380)], scale=5, contrast=1.2)
    musya(img, 230, 346, 42, rim='#fff0c0', seed=21)
    paw(img); return finish_card(img, 'kinkakuji', sat=.92)


def c_shinkyo():
    img = card(); vgrad(img, [(0, '#8a9aa8'), (.5, '#b8b8a8'), (1, '#3a4a48')])
    ridge(img, 120, 20, '#3a4a3a', 161, rough=3, fog='#b8bcb0', fog_amt=.45)
    foliage(img, [(80, 140, 120, 60), (460, 130, 130, 60), (270, 150, 110, 40)], MAPLE_RED, 162, size=(2.2, 4.5))
    img2 = P.atmos(img, H('#c8b8a8'), .15); img.paste(img2)
    fill(img, '#4a5a58', 163, poly=[(0, 260), (560, 250), (560, 380), (0, 380)], scale=8, stretch=(5, 1), contrast=1.2, light=.35)
    rr = random.Random(164); d = ImageDraw.Draw(img)
    for _ in range(120):
        x, y = rr.uniform(0, CW), rr.uniform(262, 370); w = rr.uniform(6, 26)
        d.line([(px(x), px(y)), (px(x + w), px(y + rr.uniform(-1, 1)))], fill=(236, 240, 238, int(rr.uniform(60, 170))), width=px(rr.uniform(.8, 2)))
    for i, (x, y, r) in enumerate(((120, 272, 26), (440, 268, 30), (300, 300, 18))): P.stone(img, x, y, r, r * .5, 165 + i, hexc('#4a4c46'))
    # the vermilion arch
    pts = []; low = []
    for i in range(31):
        u = i / 30; x = 60 + 440 * u; y = 200 - math.sin(u * math.pi) * 50
        pts.append((x, y)); low.append((x, y + 14))
    fill(img, '#c4402a', 166, poly=pts + list(reversed(low)), scale=3, stretch=(4, .5))
    for i in range(31):
        u = i / 30; x = 60 + 440 * u; y = 200 - math.sin(u * math.pi) * 50
        if i % 3 == 0: fill(img, '#b83a26', 170 + i, rect=(x - 1.5, y - 16, x + 1.5, y), scale=1)
    line(img, [(q[0], q[1] - 16) for q in pts], '#c4402a', 3)
    line(img, [(q[0], q[1] - 8) for q in pts], '#9a2a1a', 1.2)
    for x in (130, 430):
        fill(img, '#6a6a60', int(x), rect=(x - 12, 180, x + 12, 272), scale=3, contrast=1.2)
    fill(img, '#3a2a24', 172, rect=(52, 186, 68, 290), scale=2); fill(img, '#3a2a24', 173, rect=(492, 186, 508, 290), scale=2)
    foliage(img, [(20, 300, 80, 60), (540, 320, 80, 60)], MAPLE_RED, 174, size=(2.2, 4.5))
    fill(img, '#3a3a34', 175, poly=[(160, 380), (190, 344), (300, 336), (380, 350), (400, 380)], scale=4, contrast=1.3)
    musya(img, 290, 346, 40, rim='#ffd0a0', seed=22)
    rr = random.Random(176); d = ImageDraw.Draw(img)
    for _ in range(40):
        x, y = rr.uniform(0, CW), rr.uniform(0, 380); c = rr.choice(MAPLE_RED[2:]); d.ellipse([px(x - 1.8), px(y - 1.2), px(x + 1.8), px(y + 1.2)], fill=c[:3] + (220,))
    paw(img); return finish_card(img, 'shinkyo', sat=.95)


def c_sunset():
    img = card(); vgrad(img, [(0, '#1a1638'), (.3, '#6a3a5a'), (.5, '#e0704a'), (.58, '#ffb060')], 0, 220)
    glowc(img, 300, 212, 160, '#ffc070', .8); fill(img, '#fff0c0', 3, ell=(284, 196, 316, 228), scale=2, contrast=.2)
    fill(img, '#2a2030', 181, rect=(0, 218, 560, 222))
    img2 = reflect(img, 220, 380, dark=.3, tint='#3a2030', ripple=3.4, seed=8); img.paste(img2)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for k in range(40):
        y = 224 + k * 4; w = 8 + k * 1.6; d.rectangle([px(300 - w / 2), px(y), px(300 + w / 2), px(y + 1.4)], fill=(255, 200, 120, max(0, 140 - k * 3)))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(1.5 * P.SS)))
    fill(img, '#1c1a1e', 182, poly=cr([(220, 300), (240, 272), (300, 266), (370, 276), (390, 302), (300, 312)]), scale=3, contrast=1.3)
    torii_front(img, 300, 278, 110, 120, '#1e1a1c', 183, black_feet=False, cap='#141214')
    rr = random.Random(184); d = ImageDraw.Draw(img)
    for _ in range(60):
        x = rr.uniform(0, CW); y = rr.uniform(300, 360); d.arc([px(x - 14), px(y - 3), px(x + 14), px(y + 3)], 190, 350, fill=(255, 220, 190, 150), width=px(1))
    fill(img, '#18161a', 185, poly=[(0, 380), (0, 336), (90, 322), (180, 334), (230, 380)], scale=4, contrast=1.2)
    musya(img, 120, 330, 46, rim='#ffb060', rim_side=1, seed=23)
    paw(img, col='#d8a040'); return finish_card(img, 'sunset', sat=1.0)


def c_foxnight():
    img = card(); vgrad(img, [(0, '#060a14'), (.6, '#0e1422'), (1, '#10121a')])
    glowc(img, 280, 190, 90, '#ff9a40', .5)
    inari_tunnel(img, (280, 190), 16, 620, 34, 440, '#a8321e', '#1a1210', night=True, seed=190)
    fill(img, '#2a2622', 191, poly=[(0, 380), (560, 380), (318, 226), (242, 226)], scale=6, stretch=(3, 1), contrast=1.2)
    for i, x in enumerate((120, 440)):
        s = 1.0; b = 330; flip = 1 if x < 280 else -1
        fill(img, '#4a4a46', 192 + i, rect=(x - 26, b - 26, x + 26, b), scale=3)
        blob(img, [(x - 16, b - 26), (x - 14, b - 70), (x - 4, b - 86), (x + 8, b - 86), (x + 16, b - 60), (x + 16, b - 26)], '#8a8a84', 194 + i, scale=2, k=.6)
        for sd in (-1, 1): poly(img, [(x + sd * 2, b - 84), (x + sd * 7, b - 100), (x + sd * 10, b - 82)], '#7a7a74')
        fill(img, '#c02a20', 196 + i, poly=[(x - 14, b - 66), (x + 14, b - 66), (x, b - 48)], scale=2)
        line(img, [(x - 16 * flip, b - 30), (x - 30 * flip, b - 50), (x - 24 * flip, b - 80)], '#8a8a84', 7)
    for i, (x, y) in enumerate(((180, 150), (390, 120), (330, 250), (90, 220), (470, 230))):
        glowc(img, x, y, 22, '#6ab0ff', .8); fill(img, '#d8f0ff', 200 + i, ell=(x - 3, y - 5, x + 3, y + 3), scale=1, contrast=.2)
    lantern_glow(img, 318, 344, 7, s=.9); line(img, [(318, 334), (318, 326)], '#1a120c', 1)
    glowc(img, 300, 340, 70, '#ffa050', .35)
    musya(img, 282, 360, 48, rim='#ffb060', rim_side=1, seed=24)
    paw(img, col='#c84a30'); return finish_card(img, 'foxnight', sat=.95, lift=(4, 5, 10))


def c_aoshima():
    img = card(); vgrad(img, [(0, '#9ab8d0'), (.55, '#d8e0e0')], 0, 180)
    ridge(img, 110, 16, '#4a6a50', 201, rough=3, peaks=[(160, 40, 110)], fog='#b8c8c8', fog_amt=.4)
    rr = random.Random(202)
    for i in range(12):
        x = 60 + i * 30 + rr.uniform(-6, 6); y = 150 - math.sin(i / 11 * math.pi) * 30 + rr.uniform(-4, 4); w = rr.uniform(20, 28)
        fill(img, rr.choice(['#d8d0c0', '#c8c0b0', '#e0dcd0']), 203 + i, rect=(x - w / 2, y - 14, x + w / 2, y), scale=2, contrast=.5)
        fill(img, rr.choice(['#5a4a44', '#3a4a5a', '#6a3a30']), 220 + i, poly=[(x - w * .6, y - 13), (x, y - 22), (x + w * .6, y - 13)], scale=2)
    fill(img, '#3a6a7a', 240, rect=(0, 178, 560, 380), scale=10, stretch=(5, 1), contrast=1.0, light=.3)
    d = ImageDraw.Draw(img)
    for _ in range(90):
        x, y = rr.uniform(0, CW), rr.uniform(182, 300); d.line([(px(x), px(y)), (px(x + rr.uniform(6, 20)), px(y))], fill=(230, 240, 240, 110), width=px(1))
    for (bx, by, bw, col) in ((420, 230, 80, '#e8e4dc'), (100, 214, 60, '#dce4e8')):
        fill(img, col, int(bx), poly=[(bx - bw / 2, by - 12), (bx + bw / 2, by - 12), (bx + bw * .4, by), (bx - bw * .45, by)], scale=2, contrast=.6)
        fill(img, '#3a5a8a', int(bx) + 1, rect=(bx - bw * .1, by - 26, bx + bw * .14, by - 12), scale=2)
        line(img, [(bx - bw * .3, by - 12), (bx - bw * .3, by - 40)], '#4a3a30', 1.4)
    fill(img, '#9a9690', 241, poly=[(0, 380), (0, 290), (360, 262), (560, 270), (560, 380)], scale=6, stretch=(4, 1), contrast=.9)
    fill(img, '#6a6660', 242, poly=[(0, 296), (360, 268), (560, 276), (560, 284), (360, 276), (0, 304)], scale=3)
    cats = [(60, 316, '#e8e0d4', '#3a3230', 1), (120, 300, '#2a2626', None, -1), (200, 330, '#c8864a', '#f0e8dc', 1), (380, 300, '#dcd8d0', '#c8864a', -1),
            (440, 330, '#6a6460', None, -1), (500, 296, '#c8864a', None, 1), (250, 290, '#e8e4dc', None, 1)]
    for i, (x, y, c, sp, fl) in enumerate(cats): cat(img, x, y, 1.1 + (y - 290) / 90, c, 250 + i, fl, sp)
    musya(img, 316, 360, 48, rim='#fff4e0', seed=25)
    paw(img); return finish_card(img, 'aoshima', sat=.92)


CARDS = [('fushimi', c_fushimi), ('fuji', c_fuji), ('nara', c_nara), ('arashiyama', c_arashiyama), ('itsukushima', c_itsukushima), ('nachi', c_nachi),
         ('jigokudani', c_jigokudani), ('himeji', c_himeji), ('kamakura', c_kamakura), ('shirakawa', c_shirakawa), ('kinkakuji', c_kinkakuji),
         ('shinkyo', c_shinkyo), ('sunset', c_sunset), ('foxnight', c_foxnight), ('aoshima', c_aoshima)]


# ───────────── souvenirs (category «Сувениры») and sprites ─────────────
SOUV = []


def keep(img, iid, anchor='b'):
    out = img.resize((P.W, P.H), Image.LANCZOS); a = np.asarray(out, np.float32)
    lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True); a[..., :3] = lum + (a[..., :3] - lum) * .9
    a[..., :3] += np.random.default_rng(abs(hash(iid)) % 2 ** 32).normal(0, 3, a.shape[:2])[..., None]
    SOUV.append((iid, Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA'), anchor)); print(iid, P.W, P.H)


def s_torii():
    img = canvas(130, 130); floor_shadow(img, 65, 124, 56)
    fill(img, '#3a2a20', 1, rect=(12, 112, 118, 124), scale=3)
    for x in (34, 96): fill(img, VERM, 2 + x, rect=(x - 5, 30, x + 5, 114), scale=3, stretch=(.3, 3)); fill(img, '#1a1414', 9, rect=(x - 6, 104, x + 6, 114), scale=2)
    fill(img, VERM, 3, rect=(18, 46, 112, 54), scale=3); fill(img, '#1c1412', 4, poly=[(6, 22), (65, 26), (124, 22), (120, 32), (10, 32)], scale=3)
    fill(img, '#f0e8d8', 5, rect=(58, 32, 72, 46), scale=2); text(img, '奉', 65, 39, 10, '#1a1010', SERIF)
    volume(img, (6, 20, 124, 124), .5, .2); keep(img, 'tv_s_torii')


def s_fuji():
    img = canvas(200, 120); floor_shadow(img, 100, 114, 80)
    for k in range(13):
        a = math.radians(200 + k * 11.7); line(img, [(100, 108), (100 + math.cos(a) * 92, 108 + math.sin(a) * 92)], '#2a1a12', 1.6)
    m = Image.new('L', img.size, 0); d = ImageDraw.Draw(m); d.pieslice([px(8), px(16), px(192), px(200)], 200, 340, fill=255); d.pieslice([px(62), px(70), px(138), px(146)], 190, 350, fill=0)
    fill(img, '#e8dcc4', 5, mask=m, scale=4, contrast=.6)
    clip(img, m, lambda d: (d.rectangle([0, 0, px(200), px(80)], fill=(120, 160, 200, 120)), d.polygon([(px(58), px(76)), (px(100), px(22)), (px(142), px(76))], fill=rgba('#3a4a6a')), d.polygon([(px(86), px(40)), (px(100), px(22)), (px(114), px(40)), (px(100), px(46))], fill=rgba('#f4f4f8')), d.ellipse([px(140), px(28), px(156), px(44)], fill=rgba('#c83a2a'))))
    volume(img, (8, 16, 192, 110), .4, .2); keep(img, 'tv_s_fuji')


def s_senbei():
    img = canvas(130, 100); floor_shadow(img, 65, 94, 56)
    for k in range(5): fill(img, '#c89a5a', 10 + k, ell=(14, 50 - k * 7, 116, 90 - k * 7), scale=2, contrast=1.3, light=.3)
    fill(img, '#e8dcc4', 20, rect=(52, 24, 78, 84), scale=2, contrast=.4); text(img, '鹿', 65, 54, 16, '#6a2a1a', SERIF)
    volume(img, (14, 20, 116, 92), .5, .2); keep(img, 'tv_s_senbei')


def s_bamboo():
    img = canvas(80, 120); floor_shadow(img, 40, 114, 32)
    fill(img, '#8aa84a', 30, rect=(14, 20, 66, 114), scale=3, stretch=(.2, 3), contrast=1.2, light=.3)
    fill(img, '#c8d890', 31, ell=(14, 12, 66, 28), scale=2, contrast=.5); fill(img, '#4a5a2a', 32, ell=(20, 15, 60, 25), scale=2)
    line(img, [(14, 70), (66, 70)], '#5a7030', 2.4); volume(img, (14, 12, 66, 114), .6, .4, spec=.25); keep(img, 'tv_s_bamboo')


def s_momiji():
    img = canvas(150, 100); floor_shadow(img, 75, 94, 64)
    fill(img, '#e8dcc8', 40, rect=(10, 40, 140, 90), scale=3, contrast=.5); fill(img, '#b8322a', 41, rect=(10, 40, 140, 50), scale=2)
    for k in range(3):
        cx, cy = 34 + k * 40, 66; pts = []
        for j in range(14):
            a = -math.pi / 2 + j / 14 * math.tau; lob = [17, 15, 12, 4, 12, 15, 17][min(j // 2, 6) if j < 14 else 0]
            r = (lob if j % 2 == 0 else 6) * (.55 if 5 <= j <= 9 else 1); pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r * .85))
        fill(img, '#b86a34', 42 + k, poly=pts, scale=2, contrast=1.2, light=.35); line(img, [(cx, cy + 4), (cx + 2, cy + 14)], '#8a4a20', 2)
    volume(img, (10, 40, 140, 90), .4, .2); keep(img, 'tv_s_momiji')


def s_crow():
    img = canvas(110, 130); floor_shadow(img, 55, 124, 42)
    fill(img, '#4a3a2a', 50, rect=(20, 112, 90, 124), scale=2)
    blob(img, [(34, 110), (30, 80), (44, 56), (66, 56), (80, 76), (78, 110)], '#1c1c22', 51, scale=2, k=.6, spec=.2)
    blob(img, [(46, 58), (44, 40), (56, 30), (70, 36), (70, 54)], '#1c1c22', 52, scale=2, k=.6, spec=.2)
    poly(img, [(70, 40), (90, 44), (70, 48)], '#3a3228'); ell(img, (60, 38, 65, 43), '#e8c040')
    for x in (44, 56, 68): line(img, [(x, 108), (x - 2, 114)], '#1c1c22', 3)
    fill(img, '#c83a2a', 53, poly=[(44, 64), (70, 64), (58, 78)], scale=2)
    keep(img, 'tv_s_crow')


def s_tenugui():
    img = canvas(110, 190)
    line(img, [(10, 10), (100, 10)], '#4a3a2a', 3)
    fill(img, '#2a4a6a', 60, rect=(14, 12, 96, 184), scale=3, contrast=.8)
    d = ImageDraw.Draw(img)
    for k in range(3):
        y = 50 + k * 46; x = 55 + (k - 1) * 12
        d.ellipse([px(x - 14), px(y - 8), px(x + 14), px(y + 14)], fill=rgba('#e8e4dc')); d.ellipse([px(x - 7), px(y - 4), px(x + 7), px(y + 8)], fill=rgba('#d88a7a'))
        d.arc([px(x - 22), px(y + 12), px(x + 22), px(y + 26)], 180, 360, fill=rgba('#e8e4dc'), width=px(2))
    for x in range(18, 96, 6): line(img, [(x, 184), (x, 190)], '#2a4a6a', 1.4)
    volume(img, (14, 12, 96, 184), .3, .1); keep(img, 'tv_s_tenugui', 't')


def s_castle():
    img = canvas(130, 150); floor_shadow(img, 65, 144, 54)
    fill(img, '#6a6a62', 70, poly=[(14, 144), (24, 118), (106, 118), (116, 144)], scale=2, contrast=1.2)
    for k, (y, w, h) in enumerate(((118, 86, 22), (94, 70, 20), (72, 54, 18), (52, 40, 16))):
        fill(img, '#efeee8', 71 + k, rect=(65 - w / 2, y - h, 65 + w / 2, y), scale=2, contrast=.4, dark=.1)
        fill(img, '#5a6068', 75 + k, poly=[(65 - w * .66, y - h + 3), (65 - w * .46, y - h - 7), (65 + w * .46, y - h - 7), (65 + w * .66, y - h + 3)], scale=2)
    fill(img, '#5a6068', 79, poly=[(47, 30), (65, 16), (83, 30)], scale=2)
    volume(img, (14, 16, 116, 144), .5, .2); keep(img, 'tv_s_castle')


def s_hato():
    img = canvas(140, 100); floor_shadow(img, 70, 94, 60)
    fill(img, '#f0ead8', 80, rect=(8, 46, 132, 90), scale=3, contrast=.4); fill(img, '#c8a040', 81, rect=(8, 46, 132, 52), scale=2)
    blob(img, [(20, 70), (40, 60), (62, 58), (82, 64), (96, 78), (70, 86), (40, 84)], '#e0b050', 82, scale=2, contrast=1.1, k=.5, spec=.2)
    blob(img, [(84, 66), (86, 52), (96, 46), (106, 50), (106, 62), (96, 70)], '#e0b050', 83, scale=2, contrast=1.1, k=.5, spec=.2)
    poly(img, [(106, 54), (116, 58), (106, 60)], '#b07a30'); ell(img, (97, 52, 101, 56), '#4a2a10')
    line(img, [(40, 70), (60, 66), (74, 72)], '#b07a30', 1.6); keep(img, 'tv_s_hato')


def s_sarubobo():
    img = canvas(90, 140); floor_shadow(img, 45, 134, 34)
    blob(img, [(20, 132), (22, 90), (45, 80), (68, 90), (70, 132)], '#c02a22', 90, scale=2, k=.6)
    for sd in (-1, 1): blob(img, [(45 + sd * 18, 96), (45 + sd * 36, 86), (45 + sd * 40, 98), (45 + sd * 22, 108)], '#c02a22', 91, scale=2, k=.5)
    blob(img, [(26, 70), (28, 44), (45, 34), (62, 44), (64, 70), (45, 80)], '#c8302a', 92, scale=2, k=.6)
    fill(img, '#1c1c24', 93, poly=[(22, 46), (45, 16), (68, 46), (45, 40)], scale=2)
    fill(img, '#2a2a38', 94, rect=(22, 106, 68, 116), scale=2)
    keep(img, 'tv_s_sarubobo')


def s_yatsuhashi():
    img = canvas(150, 100); floor_shadow(img, 75, 94, 64)
    fill(img, '#3a2a4a', 100, rect=(8, 40, 142, 90), scale=3, contrast=.6); fill(img, '#e8dcc8', 101, rect=(12, 44, 138, 86), scale=3, contrast=.4)
    for k in range(4):
        x = 30 + k * 30; col = ['#e8d8b8', '#8ab070', '#c86a8a', '#6a4a3a'][k]
        fill(img, col, 102 + k, poly=[(x - 14, 80), (x + 14, 80), (x, 54)], scale=2, contrast=.8)
        ell(img, (x - 4, 68, x + 4, 76), '#5a2a1a' if k != 3 else '#d8c090')
    volume(img, (8, 40, 142, 90), .4, .2); keep(img, 'tv_s_yatsuhashi')


def s_monkeys():
    img = canvas(170, 100); floor_shadow(img, 85, 94, 76)
    fill(img, '#4a3a2a', 110, rect=(10, 82, 160, 94), scale=2)
    for k in range(3):
        x = 36 + k * 50
        blob(img, [(x - 18, 84), (x - 18, 60), (x, 50), (x + 18, 60), (x + 18, 84)], '#6a4a2a', 111 + k, scale=2, k=.6)
        blob(img, [(x - 13, 50), (x - 14, 30), (x, 22), (x + 14, 30), (x + 13, 50), (x, 56)], '#6a4a2a', 114 + k, scale=2, k=.6)
        fill(img, '#d8a888', 117 + k, ell=(x - 8, 32, x + 8, 50), scale=2)
        hy = (40, 30, 46)[k]
        for sd in (-1, 1): ell(img, (x + sd * (6 if k != 1 else 13) - 4, hy - 4, x + sd * (6 if k != 1 else 13) + 4, hy + 4), '#8a5a3a')
    keep(img, 'tv_s_monkeys')


def s_shell():
    img = canvas(110, 90); floor_shadow(img, 55, 84, 44)
    pts = [(14, 78), (20, 50), (40, 26), (55, 20), (70, 26), (90, 50), (96, 78), (55, 84)]
    blob(img, pts, '#f0d8c4', 120, scale=2, contrast=.8, k=.6, spec=.3)
    for k in range(7): line(img, [(55, 80), (20 + k * 11.5, 40 + abs(k - 3) * 6)], '#c89878', 1.4)
    keep(img, 'tv_s_shell')


def s_foxbell():
    img = canvas(90, 150)
    line(img, [(45, 4), (45, 70)], '#c02a20', 2.4); line(img, [(45, 70), (30, 96)], '#c02a20', 2); line(img, [(45, 70), (60, 96)], '#c02a20', 2)
    blob(img, [(26, 92), (28, 78), (45, 70), (62, 78), (64, 92), (45, 104)], '#d8b048', 130, scale=2, k=.6, spec=.35)
    line(img, [(32, 92), (58, 92)], '#6a5020', 1.6)
    fill(img, '#f0ebe0', 131, poly=[(30, 110), (45, 140), (60, 110), (45, 118)], scale=2); poly(img, [(30, 110), (26, 100), (38, 112)], '#f0ebe0'); poly(img, [(60, 110), (64, 100), (52, 112)], '#f0ebe0')
    line(img, [(36, 120), (41, 123)], '#c02a20', 1.2); line(img, [(54, 120), (49, 123)], '#c02a20', 1.2)
    keep(img, 'tv_s_foxbell', 't')


def s_catstone():
    img = canvas(110, 80); floor_shadow(img, 55, 74, 46)
    blob(img, [(12, 70), (16, 44), (40, 28), (72, 28), (96, 44), (100, 70), (55, 76)], '#8a8a84', 140, scale=3, contrast=1.1, k=.6)
    line(img, [(30, 58), (40, 52), (50, 58)], '#f0ebe0', 2); line(img, [(60, 58), (70, 52), (80, 58)], '#f0ebe0', 2)
    poly(img, [(28, 44), (32, 30), (40, 40)], '#f0ebe0'); poly(img, [(82, 44), (78, 30), (70, 40)], '#f0ebe0')
    ell(img, (52, 62, 58, 66), '#e0a0a0'); keep(img, 'tv_s_catstone')


def sp_bundle():
    img = canvas(90, 70); bundle(img, 45, 66, 3.6); keep(img, 'tv_bundle')


def sp_bell():
    img = canvas(46, 110)
    line(img, [(23, 0), (23, 58)], '#c02a20', 2.4)
    for k in range(4): line(img, [(19, 14 + k * 11), (27, 19 + k * 11)], '#e8e0d0', 1.4)
    blob(img, [(8, 84), (10, 68), (23, 58), (36, 68), (38, 84), (23, 94)], '#d8b048', 150, scale=2, k=.6, spec=.4)
    line(img, [(12, 84), (34, 84)], '#6a5020', 1.6); ell(img, (20, 86, 26, 92), '#3a2a10')
    line(img, [(18, 94), (16, 108)], '#c02a20', 1.6); line(img, [(28, 94), (30, 108)], '#c02a20', 1.6)
    keep(img, 'tv_bell', 't')


def sp_post():
    img = canvas(84, 170); floor_shadow(img, 42, 164, 36)
    fill(img, '#2a2a28', 160, rect=(30, 130, 54, 164), scale=2)
    blob(img, [(12, 134), (12, 40), (20, 28), (42, 22), (64, 28), (72, 40), (72, 134)], '#b8281e', 161, scale=3, contrast=1.1, k=.7, rim=.4, spec=.2)
    fill(img, '#2a1a16', 162, rect=(20, 58, 64, 66), scale=2)
    fill(img, '#e8e0d0', 163, rect=(26, 80, 58, 100), scale=2, contrast=.4); text(img, '〒', 42, 90, 14, '#b8281e', SERIF)
    fill(img, '#8a1a14', 164, poly=[(8, 34), (42, 14), (76, 34), (72, 40), (12, 40)], scale=2)
    keep(img, 'tv_post')


def sp_card():
    img = canvas(44, 30); fill(img, '#efe6d2', 170, rect=(1, 1, 43, 29), scale=2, contrast=.4); fill(img, '#c83a2a', 171, rect=(30, 4, 40, 14), scale=1)
    line(img, [(6, 18), (26, 18)], '#8a7a6a', 1); line(img, [(6, 23), (22, 23)], '#8a7a6a', 1); keep(img, 'tv_card')


def pack(items, W=1400):
    items = sorted(items, key=lambda t: -t[1].height); x = y = rowh = 0; pos = {}
    for iid, im, _ in items:
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[iid] = (x, y, im.width, im.height); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for iid, im, _ in items: at.paste(im, pos[iid][:2])
    return at, pos


if __name__ == '__main__':
    only = sys.argv[2:]
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    meta = {}
    if not only or 'cards' in only or any(o in dict(CARDS) for o in only):
        pics = []
        for name, fn in CARDS:
            if only and 'cards' not in only and name not in only: continue
            im = fn(); pics.append((name, im)); im.convert('RGB').save(f'{HERE}/out/tv_{name}.jpg', quality=88); print('card', name)
        if not only or 'cards' in only:
            cols = 2; meta['cards'] = {}
            for ai, chunk in enumerate((pics[:8], pics[8:])):
                rows = (len(chunk) + cols - 1) // cols; at = Image.new('RGB', (CW * cols, CH * rows), (12, 14, 13))
                for i, (name, im) in enumerate(chunk):
                    x, y = (i % cols) * CW, (i // cols) * CH; at.paste(im.convert('RGB'), (x, y)); meta['cards'][name] = ['tvp%d' % (ai + 1), x, y]
                at.save(f'{OUT}/atlas_tvp{ai + 1}.webp', 'WEBP', quality=80, method=6); meta['tvp%d' % (ai + 1)] = list(at.size)
            sheet = Image.new('RGB', (CW * 3 // 2 * 3, CH * 3 // 2 * 5 // 1 // 1), (0, 0, 0))
            sheet = Image.new('RGB', (280 * 3, 190 * 5)); [sheet.paste(im.convert('RGB').resize((280, 190)), ((i % 3) * 280, (i // 3) * 190)) for i, (_, im) in enumerate(pics)]
            sheet.save(f'{HERE}/out/tv_cards_sheet.jpg', quality=85)
    if not only or 'souv' in only:
        for f in (s_torii, s_fuji, s_senbei, s_bamboo, s_momiji, s_crow, s_tenugui, s_castle, s_hato, s_sarubobo, s_yatsuhashi, s_monkeys, s_shell, s_foxbell, s_catstone, sp_bundle, sp_bell, sp_post, sp_card): f()
        at, pos = pack(SOUV); at.save(f'{OUT}/atlas_tvs.webp', 'WEBP', quality=86, alpha_quality=90, method=6)
        meta['tvs'] = list(at.size); meta['souv'] = {iid: list(p) + [a] for (iid, _, a), p in zip(SOUV, [pos[i] for i, _, _ in SOUV])}
        bg = Image.new('RGBA', at.size, (40, 44, 42, 255)); bg.alpha_composite(at); bg.convert('RGB').save(f'{HERE}/out/tv_souv.jpg', quality=85)
    old = {}
    if os.path.exists(f'{HERE}/travel.json'): old = json.load(open(f'{HERE}/travel.json'))
    old.update(meta); json.dump(old, open(f'{HERE}/travel.json', 'w'), ensure_ascii=False)
    print(json.dumps(meta, ensure_ascii=False))
