#!/usr/bin/env python3
"""Add-on art «Сад камней» (zen sand garden): top-down painted stones, moss islands and a stone lantern seen from above,
all in one atlas with baked soft shadows (moonlight from the top-left).
Usage: cd art && python3 zen_art.py ../assets/items  →  atlas_zn.webp; the rect map is printed as JSON (pasted into feat/zen.js)."""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageFilter
from paint import fbm

OUT = sys.argv[1] if len(sys.argv) > 1 else '../assets/items'
LIGHT = np.array([-.52, -.62, .58]); LIGHT /= np.linalg.norm(LIGHT)


def polar(w, h, rx, ry, rot):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); dx, dy = xx - w / 2, yy - h / 2
    c, s = math.cos(rot), math.sin(rot); u = (dx * c + dy * s) / rx; v = (-dx * s + dy * c) / ry
    return np.sqrt(u * u + v * v), np.arctan2(v, u)


def outline(th, rng, rough, ang):
    """radius multiplier along the angle: soft harmonics blended with a random convex polygon (angular rocks)"""
    R = 1 + sum(rng.uniform(-1, 1) * rough / k * np.sin(k * th + rng.uniform(0, 6.3)) for k in range(2, 7))
    if ang > 0:
        n = rng.integers(5, 9); phis = np.sort(rng.uniform(0, 2 * np.pi, n)); ds = rng.uniform(.82, 1.0, n)
        Rp = 1 / np.max([np.clip(np.cos(th - p), 1e-3, None) / d for p, d in zip(phis, ds)], axis=0)
        R = R * (1 - ang) + np.minimum(Rp, 1.25) * ang
    return R


def shade(alb, hgt, hs, mask):
    gy, gx = np.gradient(hgt * hs)
    n = np.dstack([-gx, -gy, np.ones_like(gx)]); n /= np.linalg.norm(n, axis=2, keepdims=True)
    lam = np.clip((n * LIGHT).sum(2), 0, 1)
    spec = np.clip((n * np.array([-.3, -.4, .87])).sum(2), 0, 1) ** 24 * .18
    return alb * (.26 + .95 * lam)[..., None] + spec[..., None] * 255


def shadowed(rgb, mask, off, blur, a=.62, contact=.55):
    """stone RGB + mask → RGBA sprite with a soft cast shadow (bottom-right) and a tight contact shadow"""
    h, w = mask.shape; M = Image.fromarray((mask * 255).astype(np.uint8))
    sh = Image.new('L', (w, h)); sh.paste(M, (int(off[0]), int(off[1])))
    sh = np.asarray(sh.filter(ImageFilter.GaussianBlur(blur)), np.float32) / 255 * a
    ct = Image.new('L', (w, h)); ct.paste(M, (2, 3)); ct = np.asarray(ct.filter(ImageFilter.GaussianBlur(3)), np.float32) / 255 * contact
    sa = np.maximum(sh, ct)
    al = mask + sa * (1 - mask)
    col = rgb * mask[..., None] / np.maximum(al, 1e-4)[..., None]
    out = np.dstack([np.clip(col, 0, 255), al * 255])
    return Image.fromarray(out.astype(np.uint8), 'RGBA')


def grade(img, sat=.82, noise=2.4, seed=0):
    a = np.asarray(img, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1, keepdims=True)
    a[..., :3] = lum + (a[..., :3] - lum) * sat
    a[..., :3] += np.random.default_rng(seed).normal(0, noise, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def stone(seed, rx, ry, base, rot=0., ang=.5, rough=.22, flat=.6, moss=0., lichen=.3, strata=0.):
    rng = np.random.default_rng(seed); pad = int(max(rx, ry) * .55) + 10
    w, h = int(rx * 2 + pad * 2), int(ry * 2 + pad * 2)
    r, th = polar(w, h, rx, ry, rot); R = outline(th, rng, rough, ang)
    q = r / R; mask = np.clip((1 - q) * min(rx, ry) + .5, 0, 1)
    big = fbm(w, h, 40, 4, seed + 1); fine = fbm(w, h, 7, 3, seed + 2)
    hgt = np.clip(1 - q * q, 0, 1) ** flat + (big - .5) * .35 + (fine - .5) * .06
    if strata:      # layered rock: soft parallel bands
        yy, xx = np.mgrid[0:h, 0:w]; b = np.sin((xx * math.sin(rot + .6) + yy * math.cos(rot + .6)) / (rx * .16) + big * 4)
        hgt += b * .03 * strata
    hgt *= mask
    b = np.array(base, np.float32)
    tone = .78 + .44 * big[..., None] + (fine[..., None] - .5) * .25
    alb = b * tone
    alb += np.random.default_rng(seed + 3).normal(0, 7, (h, w))[..., None]          # granite grain
    dots = np.random.default_rng(seed + 4).random((h, w)) > .985; alb[dots] = alb[dots] * .6 + 70
    if lichen:
        ln = fbm(w, h, 16, 4, seed + 5); lm = np.clip((ln - .72) * 6, 0, 1) * lichen
        alb = alb * (1 - lm[..., None] * .7) + np.array([150, 158, 140]) * lm[..., None] * .7
    if moss:
        mn = fbm(w, h, 14, 4, seed + 6); top = np.clip(1.3 - q, 0, 1)
        mm = np.clip((mn - (1 - moss * .55)) * 5, 0, 1) * top
        mc = np.array([62, 84, 44]) * (.7 + .6 * fbm(w, h, 4, 2, seed + 7))[..., None]
        alb = alb * (1 - mm[..., None]) + mc * mm[..., None]; hgt += mm * .05
    rgb = shade(alb, hgt, min(rx, ry) * .55, mask)
    rgb *= (.55 + .45 * np.clip(hgt * 5, 0, 1))[..., None]                         # occlusion at the foot
    return grade(shadowed(rgb, mask, (rx * .2, ry * .24), max(4, rx * .1)), seed=seed)


def moss_island(seed, rx, ry, rot=0.):
    rng = np.random.default_rng(seed); pad = 18; w, h = int(rx * 2 + pad * 2), int(ry * 2 + pad * 2)
    r, th = polar(w, h, rx, ry, rot); R = outline(th, rng, .3, 0)
    edge = fbm(w, h, 6, 3, seed + 1); q = r / R
    mask = np.clip((1 - q + (edge - .5) * .1) * min(rx, ry) * .5 + .5, 0, 1)
    mask = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.8)), np.float32) / 255
    bumps = fbm(w, h, 11, 4, seed + 2); big = fbm(w, h, 50, 3, seed + 3)
    hgt = (np.clip(1 - q * q, 0, 1) ** .3 * .5 + bumps * .6) * mask
    c0, c1, c2 = np.array([28, 36, 24.]), np.array([56, 72, 42.]), np.array([104, 118, 72.])
    t = np.clip(bumps * .7 + big * .5 - .1, 0, 1)[..., None]
    alb = np.where(t < .5, c0 + (c1 - c0) * t * 2, c1 + (c2 - c1) * (t - .5) * 2)
    alb *= (.9 + .2 * fbm(w, h, 3, 2, seed + 4))[..., None]
    brown = np.clip(1 - mask * 1.6, 0, 1)[..., None] + np.clip(q - .82, 0, .2)[..., None] * 2   # thin dry rim
    alb = alb * (1 - brown * .5) + np.array([70, 60, 40]) * brown * .5
    sp = np.random.default_rng(seed + 5).random((h, w)) > .992; alb[sp] = [150, 160, 96]   # sporophyte specks
    rgb = shade(alb, hgt, 9, mask)
    return grade(shadowed(rgb, mask, (5, 6), 4, a=.45, contact=.4), sat=.7, seed=seed)


def lantern(seed, R=66):
    """a stone lantern seen from above: hexagonal roof with six lit facets, upturned corners, a sphere finial, moss"""
    pad = 70; w = h = int(R * 2 + pad * 2); cx, cy = w / 2 - 18, h / 2 - 18
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); dx, dy = xx - cx, yy - cy
    r = np.sqrt(dx * dx + dy * dy); th = np.arctan2(dy, dx); rot = .3
    sec = np.floor(((th - rot) % (2 * np.pi)) / (np.pi / 3)); mid = rot + (sec + .5) * np.pi / 3
    hexr = R * math.cos(math.pi / 6) / np.cos(((th - rot) % (np.pi / 3)) - np.pi / 6)
    mask = np.clip(hexr - r + .5, 0, 1)
    tilt = .62; n = np.dstack([np.cos(mid) * math.sin(tilt), np.sin(mid) * math.sin(tilt), np.full_like(r, math.cos(tilt))])
    lam = np.clip((n * LIGHT).sum(2), 0, 1)
    tex = fbm(w, h, 18, 4, seed); grain = np.random.default_rng(seed).normal(0, 8, (h, w))
    alb = np.array([112, 112, 104.]) * (.75 + .5 * tex)[..., None] + grain[..., None]
    mn = fbm(w, h, 12, 4, seed + 1); mm = np.clip((mn - .55) * 4, 0, 1) * np.clip((hexr - r) / R * 3, 0, 1) * (1 - np.clip(r / R - .2, 0, 1) * .3)
    alb = alb * (1 - mm[..., None] * .8) + np.array([58, 80, 42]) * mm[..., None] * .8
    rgb = alb * (.3 + .95 * lam)[..., None]
    ridge = np.abs(((th - rot) % (np.pi / 3))) * r; ridge = np.minimum(ridge, np.abs(((th - rot) % (np.pi / 3)) - np.pi / 3) * r)
    rgb += (np.clip(1 - ridge / 2.2, 0, 1) * 34 * (r > 18))[..., None]                         # hip ridges catch the light
    eave = np.clip(1 - np.abs(hexr - r - 4) / 3.5, 0, 1); rgb *= (1 - eave * .35)[..., None]     # eave line
    # finial: lotus ring + sphere
    for rr, k in ((24, .9), (15, 1.15)):
        d = np.sqrt(dx * dx + dy * dy) / rr; m2 = np.clip((1 - d) * rr + .5, 0, 1); z = np.sqrt(np.clip(1 - d * d, 0, 1))
        nn = np.dstack([dx / rr, dy / rr, z]); l2 = np.clip((nn * LIGHT).sum(2), 0, 1)
        c2 = np.array([124, 122, 112.]) * k * (.3 + .9 * l2)[..., None] + grain[..., None] * .6
        rgb = rgb * (1 - m2[..., None]) + c2 * m2[..., None]
    # upturned corners (warabite): small bright knobs at the six vertices
    for i in range(6):
        a = rot + i * np.pi / 3; vx, vy = cx + math.cos(a) * R * .97, cy + math.sin(a) * R * .97
        d = np.sqrt((xx - vx) ** 2 + (yy - vy) ** 2) / 4.5; m2 = np.clip((1 - d) * 4.5 + .5, 0, 1)
        l2 = np.clip(.6 - (xx - vx + yy - vy) / 9, .2, 1)
        rgb = rgb * (1 - m2[..., None]) + (np.array([120, 118, 108.]) * l2[..., None]) * m2[..., None]; mask = np.maximum(mask, m2)
    return grade(shadowed(rgb, mask, (34, 40), 9, a=.66), seed=seed)      # tall lantern: a long cast shadow


def pack(items, width, quality=88):
    lst = sorted(items, key=lambda t: -t[1].height); x = y = rowh = 0; pos = {}
    for k, im in lst:
        if x + im.width + 2 > width: x = 0; y += rowh + 2; rowh = 0
        pos[k] = (x, y); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (width, y + rowh), (0, 0, 0, 0))
    for k, im in lst: at.paste(im, pos[k])
    f = f'{OUT}/atlas_zn.webp'; at.save(f, 'WEBP', quality=quality, alpha_quality=88, method=6)
    print('atlas zn', at.size, os.path.getsize(f) // 1024, 'KB')
    return {'w': at.width, 'h': at.height, 'r': {k: [pos[k][0], pos[k][1], im.width, im.height] for k, im in items}}, at


if __name__ == '__main__':
    G = (92, 94, 92); B = (104, 96, 86); D = (58, 60, 64); GR = (86, 92, 84)
    items = [
        ('s1', stone(11, 92, 70, G, .3, .55, moss=.5, strata=1)),       # the main upright stone
        ('s2', stone(12, 70, 54, B, -.5, .7, lichen=.5)),
        ('s3', stone(13, 58, 40, D, 1.1, .3, flat=.45)),
        ('s4', stone(14, 46, 38, GR, .2, .8, moss=.35)),
        ('s5', stone(15, 80, 36, G, -.2, .45, flat=.4, strata=1.5)),    # long flat stone
        ('s6', stone(16, 40, 32, B, .7, .2, lichen=.6)),
        ('s7', stone(17, 64, 60, D, 0, .65, moss=.7)),
        ('s8', stone(18, 30, 24, GR, .4, .5)),
        ('m1', moss_island(21, 150, 96, .2)),
        ('m2', moss_island(22, 112, 76, -.4)),
        ('m3', moss_island(23, 82, 60, .9)),
        ('lt', lantern(31)),
    ]
    os.makedirs('out', exist_ok=True)
    rects, at = pack(items, 1024)
    prev = Image.new('RGBA', at.size, (196, 194, 186, 255)); prev.alpha_composite(at); prev.convert('RGB').save('out/zn_atlas_preview.jpg', quality=85)
    print(json.dumps(rects['r'], separators=(',', ':')))
