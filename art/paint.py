#!/usr/bin/env python3
"""Painterly backgrounds for «Мусин дом»: gloomy Japan, dense textured foliage, fog, wood, paper.
Every scene is 1800×1400, bottom-anchored: the floor the cat stands on is the bottom ~250 px."""
import math, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H, SS = 1800, 1400, 2          # final size, supersampling factor for strokes
SW, SH = W * SS, H * SS


def set_size(w, h):
    global W, H, SW, SH
    W, H, SW, SH = w, h, w * SS, h * SS


def hexc(h, a=255):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def mixc(c1, c2, t):
    return tuple(int(round(c1[i] + (c2[i] - c1[i]) * t)) for i in range(len(c1)))


def fbm(w, h, scale, octaves=5, seed=0, stretch=(1, 1)):
    """Fractal value noise in 0..1 built from upsampled random grids."""
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32); amp = 1.0; tot = 0
    for o in range(octaves):
        gw = max(2, int(w / scale * 2 ** o / stretch[0])); gh = max(2, int(h / scale * 2 ** o / stretch[1]))
        grid = (rng.random((gh, gw)) * 255).astype(np.uint8)
        layer = np.asarray(Image.fromarray(grid).resize((w, h), Image.BICUBIC), np.float32) / 255
        out += layer * amp; tot += amp; amp *= 0.5
    out /= tot
    return (out - out.min()) / (out.max() - out.min() + 1e-6)


def layer():
    return Image.new('RGBA', (SW, SH), (0, 0, 0, 0))


def gradient(top, bottom, h=None, w=None):
    h = h or SH; w = w or SW
    t = np.linspace(0, 1, h)[:, None]
    a = np.array(top[:3], np.float32); b = np.array(bottom[:3], np.float32)
    rgb = a + (b - a) * t[..., None]
    rgb = np.repeat(rgb, w, axis=1)
    return Image.fromarray(np.dstack([rgb, np.full((h, w), 255)]).astype(np.uint8), 'RGBA')


def textured_fill(mask, base, dark, light, scale, seed, stretch=(1, 1), contrast=1.0):
    """Fill a mask (L image) with a noise-modulated color; returns RGBA layer."""
    n = fbm(mask.width, mask.height, scale, 5, seed, stretch)
    fine = fbm(mask.width, mask.height, max(2 * SS, scale / 5), 3, seed + 77, stretch)
    n = 0.68 * n + 0.32 * fine                                         # large mottling + fine tooth
    n = np.clip((n - 0.5) * contrast + 0.5, 0, 1)[..., None]
    b = np.array(base[:3], np.float32); d = np.array(dark[:3], np.float32); l = np.array(light[:3], np.float32)
    rgb = np.where(n < 0.5, d + (b - d) * (n / 0.5), b + (l - b) * ((n - 0.5) / 0.5))
    a = np.asarray(mask, np.float32)[..., None]
    return Image.fromarray(np.concatenate([rgb, a], -1).astype(np.uint8), 'RGBA')


def atmos(img, fog, amount, blur=0):
    """Push a layer toward the fog color (aerial perspective) and optionally soften it."""
    a = np.asarray(img, np.float32)
    f = np.array(fog[:3], np.float32)
    a[..., :3] = a[..., :3] + (f - a[..., :3]) * amount
    out = Image.fromarray(a.astype(np.uint8), 'RGBA')
    return out.filter(ImageFilter.GaussianBlur(blur * SS)) if blur else out


def fog_layer(color, y0, y1, density, seed, scale=260):
    """Soft band of fog with fractal structure between y0 and y1 (final-pixel units)."""
    n = fbm(SW // 4, SH // 4, scale / 4 * SS, 5, seed, (2.5, 1))
    t = np.linspace(0, 1, SH // 4)[:, None]
    yy0, yy1 = y0 / H, y1 / H
    band = np.clip(1 - np.abs((t - (yy0 + yy1) / 2) / ((yy1 - yy0) / 2 + 1e-6)), 0, 1) ** 1.3
    a = np.clip(band * (0.35 + 0.9 * n) * density, 0, 1) * 255
    img = Image.new('RGBA', (SW // 4, SH // 4), color)
    img.putalpha(Image.fromarray(a.astype(np.uint8)))
    return img.resize((SW, SH), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6 * SS))


# ───────────── foliage ─────────────

def dab_mass(draw, blobs, n, kind, pal, rnd, light_dir=(-0.5, -0.85), size=(5, 11), droop=0.25):
    """Paint a foliage mass with brush-like strokes. Density thins toward the rim, so edges
    dissolve instead of forming an outline; tone follows the light for volume."""
    lx, ly = light_dir
    for _ in range(n):
        cx, cy, rx, ry = rnd.choice(blobs)
        ang = rnd.random() * math.tau; r = rnd.random() ** 0.5
        if r > 0.8 and rnd.random() < 0.55: continue                # feathered rim
        dx, dy = math.cos(ang) * r, math.sin(ang) * r
        x = cx + dx * rx * 1.08; y = cy + dy * ry * 1.08
        lit = -(dx * lx + dy * ly) * 0.9 + (rnd.random() - 0.5) * 1.0
        t = min(0.999, max(0, (lit + 1) / 2)) ** 1.2
        col = pal[int(t * len(pal))]
        alpha = int(rnd.uniform(150, 255) * (1 - 0.35 * r))
        col = (col[0], col[1], col[2], alpha)
        s_ = rnd.uniform(*size) * SS
        if kind == 'needle':
            base_a = rnd.uniform(0, math.tau)
            for k in range(rnd.randint(3, 6)):
                a = base_a + (k - 2.5) * 0.28
                ex, ey = x + math.cos(a) * s_, y + math.sin(a) * s_ * 0.75 + s_ * droop
                draw.line([(x, y), (ex, ey)], fill=col, width=max(1, int(SS * rnd.uniform(0.8, 1.4))))
        else:
            a = rnd.uniform(0, math.tau); L = s_ * 0.5
            draw.line([(x - math.cos(a) * L, y - math.sin(a) * L), (x + math.cos(a) * L, y + math.sin(a) * L)],
                      fill=col, width=max(2, int(SS * rnd.uniform(1.6, 2.8))))


def ragged(blobs, rnd, k=7, jitter=0.55):
    """Break smooth ellipses into ragged clusters so silhouettes look like real foliage."""
    out = []
    for cx, cy, rx, ry in blobs:
        for _ in range(k):
            a = rnd.uniform(0, math.tau); r = rnd.random() ** 0.6
            out.append((cx + math.cos(a) * rx * r * 0.85, cy + math.sin(a) * ry * r * 0.75,
                        rx * rnd.uniform(0.25, jitter), ry * rnd.uniform(0.35, jitter + 0.2)))
    return out


def wobble(p0, p1, segs, amp, rnd):
    (x0, y0), (x1, y1) = p0, p1
    nx, ny = -(y1 - y0), (x1 - x0); L = math.hypot(nx, ny) or 1; nx, ny = nx / L, ny / L
    pts = []
    ph = rnd.uniform(0, 6)
    for i in range(segs + 1):
        u = i / segs; w = math.sin(u * math.pi) * (math.sin(u * 7 + ph) * 0.6 + rnd.uniform(-0.4, 0.4)) * amp
        pts.append((x0 + (x1 - x0) * u + nx * w, y0 + (y1 - y0) * u + ny * w))
    return pts


def shadow_blobs(img, blobs, col, grow=1.0):
    """Soft dark core of a foliage mass (blurred, slightly inset) — depth without an outline."""
    xs = [cx for cx, _, rx, _ in blobs]; ys = [cy for _, cy, _, ry in blobs]
    R = max(max(rx for _, _, rx, _ in blobs), max(ry for *_, ry in blobs)) * 1.3 + 20 * SS
    x0, y0 = int(min(xs) - R), int(min(ys) - R); x1, y1 = int(max(xs) + R), int(max(ys) + R)
    tmp = Image.new('RGBA', (max(1, x1 - x0), max(1, y1 - y0)), (0, 0, 0, 0)); d = ImageDraw.Draw(tmp)
    for cx, cy, rx, ry in blobs:
        rx *= 0.82 * grow; ry *= 0.8 * grow
        d.ellipse([cx - x0 - rx, cy - y0 - ry + ry * 0.2, cx - x0 + rx, cy - y0 + ry + ry * 0.2], fill=(col[0], col[1], col[2], 235))
    tmp = tmp.filter(ImageFilter.GaussianBlur(5 * SS))
    img.alpha_composite(tmp, (x0, y0))


def trunk(img, pts, widths, bark, seed, moss=None):
    """Tapered trunk/branch along a polyline with bark texture and cylindrical shading."""
    mask = Image.new('L', img.size, 0); md = ImageDraw.Draw(mask)
    for (x0, y0), (x1, y1), w0, w1 in zip(pts, pts[1:], widths, widths[1:]):
        ang = math.atan2(y1 - y0, x1 - x0) + math.pi / 2
        c, s = math.cos(ang), math.sin(ang)
        md.polygon([(x0 + c * w0, y0 + s * w0), (x1 + c * w1, y1 + s * w1), (x1 - c * w1, y1 - s * w1), (x0 - c * w0, y0 - s * w0)], fill=255)
        md.ellipse([x1 - w1, y1 - w1, x1 + w1, y1 + w1], fill=255)
    box = mask.getbbox()
    if not box: return
    x0, y0, x1, y1 = box; sub = mask.crop(box)
    tex = textured_fill(sub, bark[1], bark[0], bark[2], 26 * SS, seed, stretch=(0.18, 3), contrast=1.6)
    # cylindrical shading: darker at the silhouette edges
    a = np.asarray(sub, np.float32) / 255
    edge = np.asarray(sub.filter(ImageFilter.GaussianBlur(6 * SS)), np.float32) / 255
    t = np.asarray(tex, np.float32)
    t[..., :3] *= (0.45 + 0.55 * edge[..., None])
    if moss is not None:
        mn = fbm(sub.width, sub.height, 30 * SS, 4, seed + 9)
        m = np.clip((mn - 0.55) * 4, 0, 1)[..., None] * 0.8
        t[..., :3] = t[..., :3] * (1 - m) + np.array(moss[:3], np.float32) * m
    t[..., 3] = a * 255
    img.alpha_composite(Image.fromarray(t.astype(np.uint8), 'RGBA'), (x0, y0))


def cedar(img, x, base, h, w, seed, pal, bark):
    """Japanese cedar (sugi): straight tall trunk, dense tufted foliage tiers."""
    rnd = random.Random(seed); d = ImageDraw.Draw(img)
    trunk(img, [(x, base), (x + rnd.uniform(-6, 6) * SS, base - h)], [w * 0.075, w * 0.02], bark, seed)
    tiers = int(h / (38 * SS))
    for i in range(tiers):
        u = i / tiers
        y = base - h * (0.28 + 0.72 * u)
        L = w * (0.55 * (1 - u) ** 0.85 + 0.1) * rnd.uniform(0.7, 1.15)
        for side in (-1, 1):
            if rnd.random() < 0.15 and u < 0.5: continue
            blobs = []
            for k in range(4):
                t = (k + 0.5) / 4
                blobs.append((x + side * L * t, y + L * 0.12 * t + rnd.uniform(-6, 6) * SS, L * 0.32 * (1.1 - t * 0.4), L * 0.16 * (1.1 - t * 0.3)))
            blobs = ragged(blobs, rnd, 4, 0.7)
            shadow_blobs(img, blobs, pal[0])
            dab_mass(d, blobs, int(260 * L / (60 * SS)) + 80, 'needle', pal, rnd, size=(4, 9), droop=0.35)
    top = [(x, base - h * 1.02, w * 0.08, h * 0.05)]
    dab_mass(d, top, 90, 'needle', pal, rnd, size=(3, 7))


def pine(img, x, base, h, seed, pal, bark, lean=0.0, pads=6, spread=1.0):
    """Japanese black pine: gnarled leaning trunk, layered ragged needle pads."""
    rnd = random.Random(seed); d = ImageDraw.Draw(img)
    top = (x + lean * h * 0.45, base - h)
    pts = wobble((x, base), top, 12, h * 0.06, rnd)
    widths = [h * 0.04 * (1 - i / 14) ** 1.2 + 2.5 * SS for i in range(len(pts))]
    trunk(img, pts, widths, bark, seed, moss=hexc('#3a4630'))
    for i in range(pads):
        k = 3 + int((len(pts) - 4) * i / max(1, pads - 1))
        px, py = pts[k]
        side = -1 if (i + seed) % 2 == 0 else 1
        L = h * rnd.uniform(0.26, 0.4) * spread * (1 - i / (pads * 1.7))
        bx, by = px + side * L, py + rnd.uniform(-10, 40) * SS
        bp = wobble((px, py), (bx, by), 6, L * 0.08, rnd)
        trunk(img, bp, [widths[k] * 0.5 * (1 - j / 8) + 2 * SS for j in range(len(bp))], bark, seed + i * 7)
        for j in range(2, len(bp)):
            tx, ty = bp[j]; tw = wobble((tx, ty), (tx + side * rnd.uniform(20, 60) * SS, ty + rnd.uniform(-40, 10) * SS), 3, 6 * SS, rnd)
            trunk(img, tw, [2.2 * SS, 1.6 * SS, 1.2 * SS, 1 * SS], bark, seed + i * 11 + j)
        blobs = [(bx - side * L * u, by - 10 * SS - L * 0.05 * u, L * (0.34 - u * 0.12), L * 0.1) for u in (0, 0.25, 0.5, 0.75)]
        blobs = ragged(blobs, rnd, 9)
        shadow_blobs(img, blobs, pal[0], 1.0)
        dab_mass(d, blobs, int(2200 * L / (200 * SS)), 'needle', pal, rnd, size=(4, 10), droop=0.08)
    tx, ty = pts[-1]
    blobs = ragged([(tx + rnd.uniform(-40, 40) * SS, ty, h * 0.14, h * 0.05)], rnd, 12)
    shadow_blobs(img, blobs, pal[0]); dab_mass(d, blobs, 1600, 'needle', pal, rnd, size=(4, 9), droop=0.05)


def maple(img, x, base, h, seed, pal, bark, lean=0.0):
    """Garden maple: thin twisting trunks and a deep, ragged crown of small leaves."""
    rnd = random.Random(seed); d = ImageDraw.Draw(img)
    tips = []
    def branch(x0, y0, ang, L, wd, depth):
        if depth > 5 or L < 22 * SS:
            tips.append((x0, y0)); return
        x1 = x0 + math.sin(ang) * L; y1 = y0 - math.cos(ang) * L
        pts = wobble((x0, y0), (x1, y1), 5, L * 0.07, rnd)
        trunk(img, pts, [wd * (1 - 0.35 * j / 5) for j in range(6)], bark, seed + depth * 13 + int(L))
        n = 2 if depth < 2 else rnd.choice((1, 2, 2, 3))
        for k in range(n):
            branch(x1, y1, ang + rnd.uniform(-0.75, 0.75), L * rnd.uniform(0.6, 0.8), wd * 0.64, depth + 1)
    branch(x, base, lean, h * 0.32, h * 0.028, 0)
    blobs = ragged([(tx, ty, rnd.uniform(55, 95) * SS, rnd.uniform(30, 50) * SS) for tx, ty in tips], rnd, 6, 0.6)
    shadow_blobs(img, blobs, pal[0], 0.95)
    dab_mass(d, blobs, 150 * len(blobs), 'leaf', pal, rnd, size=(3, 6))


def bushes(img, y, x0, x1, seed, pal, count=8, rmin=60, rmax=130):
    rnd = random.Random(seed); d = ImageDraw.Draw(img)
    for i in range(count):
        cx = rnd.uniform(x0, x1) * SS; r = rnd.uniform(rmin, rmax) * SS
        blobs = ragged([(cx + rnd.uniform(-0.6, 0.6) * r, y * SS - r * rnd.uniform(0.3, 0.6), r * rnd.uniform(0.5, 0.8), r * rnd.uniform(0.35, 0.55)) for _ in range(4)], rnd, 6, 0.6)
        shadow_blobs(img, blobs, pal[0], 1.02)
        dab_mass(d, blobs, int(r / SS * 70), 'leaf', pal, rnd, size=(2.5, 5.5))


# ───────────── man-made textures ─────────────

def wood_planks(img, y0, y1, seed, base, dark, light, plank_h=46, horizontal=True):
    """Weathered planks with grain, seams and a soft sheen."""
    h = (y1 - y0) * SS
    n = fbm(SW, h, 40 * SS, 5, seed, (6, 0.25) if horizontal else (0.25, 6))
    grain = np.sin((np.arange(h)[:, None] / (3.2 * SS)) + n * 14) * 0.5 + 0.5
    v = np.clip(0.55 * n + 0.45 * grain, 0, 1)
    b, d_, l = (np.array(c[:3], np.float32) for c in (base, dark, light))
    rgb = np.where(v[..., None] < 0.5, d_ + (b - d_) * (v[..., None] / 0.5), b + (l - b) * ((v[..., None] - 0.5) / 0.5))
    rng = np.random.default_rng(seed)
    ph = plank_h * SS
    for yy in range(0, h, ph):
        rgb[yy:yy + 2 * SS] *= 0.35                                  # seam
        rgb[yy + 2 * SS: yy + 4 * SS] *= 1.12                       # worn edge
        rgb[yy:yy + ph] *= rng.uniform(0.85, 1.08)                   # each plank its own tone
        for _ in range(2):
            x = int(rng.uniform(0, SW)); rgb[yy:yy + ph, x:x + 2 * SS] *= 0.4
    t = np.linspace(0, 1, h)[:, None, None]
    rgb *= (0.8 + 0.35 * t)                                          # nearer = a touch lighter
    img.alpha_composite(Image.fromarray(np.dstack([np.clip(rgb, 0, 255), np.full((h, SW), 255)]).astype(np.uint8), 'RGBA'), (0, y0 * SS))


def wood_block(img, box, seed, base, dark, light, vertical=False):
    x0, y0, x1, y1 = (int(v * SS) for v in box)
    m = Image.new('L', (x1 - x0, y1 - y0), 255)
    t = textured_fill(m, base, dark, light, 30 * SS, seed, stretch=((0.12, 5) if vertical else (5, 0.12)), contrast=1.1)
    img.alpha_composite(t, (x0, y0))


def paper(img, box, seed, base, lit=1.0, grid=(3, 5), frame=None):
    """Shoji: washi paper texture with fibres, wooden kumiko lattice."""
    x0, y0, x1, y1 = (int(v * SS) for v in box)
    m = Image.new('L', (x1 - x0, y1 - y0), 255)
    t = textured_fill(m, base, mixc(base, (0, 0, 0, 255), 0.18), mixc(base, (255, 255, 255, 255), 0.1), 8 * SS, seed, contrast=0.8)
    a = np.asarray(t, np.float32); gy = np.linspace(1, 0.7, a.shape[0])[:, None, None]; a[..., :3] *= gy * lit
    img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'), (x0, y0))
    d = ImageDraw.Draw(img); fc = frame or hexc('#241a14')
    for i in range(1, grid[0]):
        x = x0 + (x1 - x0) * i / grid[0]; d.rectangle([x - 2 * SS, y0, x + 2 * SS, y1], fill=fc)
    for i in range(1, grid[1]):
        y = y0 + (y1 - y0) * i / grid[1]; d.rectangle([x0, y - 2 * SS, x1, y + 2 * SS], fill=fc)
    wood_block(img, (box[0] - 8, box[1] - 8, box[2] + 8, box[1]), seed + 1, hexc('#2a1f18'), hexc('#140e0b'), hexc('#3b2c22'))
    wood_block(img, (box[0] - 8, box[3], box[2] + 8, box[3] + 10), seed + 2, hexc('#2a1f18'), hexc('#140e0b'), hexc('#3b2c22'))
    wood_block(img, (box[0] - 8, box[1], box[0], box[3]), seed + 3, hexc('#2a1f18'), hexc('#140e0b'), hexc('#3b2c22'), True)
    wood_block(img, (box[2], box[1], box[2] + 8, box[3]), seed + 4, hexc('#2a1f18'), hexc('#140e0b'), hexc('#3b2c22'), True)


def stone(img, cx, cy, rx, ry, seed, base=hexc('#4a4f4a'), moss=True):
    m = Image.new('L', (int(rx * 2 * SS), int(ry * 2 * SS)), 0)
    ImageDraw.Draw(m).ellipse([0, 0, m.width - 1, m.height - 1], fill=255)
    t = textured_fill(m, base, mixc(base, (0, 0, 0, 255), 0.45), mixc(base, (255, 255, 255, 255), 0.14), 26 * SS, seed, contrast=1.05)
    a = np.asarray(t, np.float32)
    yy = np.linspace(-1, 1, a.shape[0])[:, None]; xx = np.linspace(-1, 1, a.shape[1])[None, :]
    shade = np.clip(1.15 - 0.55 * (yy + 0.35 * xx), 0.35, 1.25)[..., None]
    a[..., :3] *= shade
    if moss:
        mn = fbm(a.shape[1], a.shape[0], 12 * SS, 4, seed + 5)
        mm = np.clip((mn - 0.45) * 3, 0, 1) * np.clip(-yy * 1.4 + 0.2, 0, 1)
        a[..., :3] = a[..., :3] * (1 - mm[..., None] * 0.85) + np.array([58, 72, 42], np.float32) * mm[..., None] * 0.85
    img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'), (int((cx - rx) * SS), int((cy - ry) * SS)))


def toro(img, x, base, h, seed):
    """Stone lantern (tōrō) with moss."""
    s = h / 100
    def blk(bx0, by0, bx1, by1, sd):
        stone(img, (bx0 + bx1) / 2, (by0 + by1) / 2, (bx1 - bx0) / 2, (by1 - by0) / 2, seed + sd, hexc('#55594f'))
    wood = ImageDraw.Draw(img)
    blk(x - 22 * s, base - 14 * s, x + 22 * s, base, 1)
    blk(x - 8 * s, base - 52 * s, x + 8 * s, base - 12 * s, 2)
    blk(x - 20 * s, base - 62 * s, x + 20 * s, base - 50 * s, 3)
    blk(x - 14 * s, base - 84 * s, x + 14 * s, base - 60 * s, 4)
    wood.rectangle([(x - 6 * s) * SS, (base - 80 * s) * SS, (x + 6 * s) * SS, (base - 66 * s) * SS], fill=hexc('#15130f'))
    blk(x - 30 * s, base - 96 * s, x + 30 * s, base - 82 * s, 5)
    blk(x - 7 * s, base - 106 * s, x + 7 * s, base - 94 * s, 6)


def torii(img, x, base, w, h, seed, col=hexc('#2a1a15')):
    p = w * 0.075
    wood_block(img, (x - w * 0.37, base - h, x - w * 0.37 + p, base), seed, col, mixc(col, (0, 0, 0, 255), .5), mixc(col, (140, 120, 100, 255), .25), True)
    wood_block(img, (x + w * 0.37 - p, base - h, x + w * 0.37, base), seed + 1, col, mixc(col, (0, 0, 0, 255), .5), mixc(col, (140, 120, 100, 255), .25), True)
    wood_block(img, (x - w * 0.44, base - h * 0.8, x + w * 0.44, base - h * 0.73), seed + 2, col, mixc(col, (0, 0, 0, 255), .5), mixc(col, (140, 120, 100, 255), .25))
    # curved kasagi
    m = Image.new('L', (SW, SH), 0); md = ImageDraw.Draw(m)
    pts = []
    for i in range(41):
        u = i / 40; xx = x - w * 0.58 + w * 1.16 * u; yy = base - h * 1.02 + (4 * (u - 0.5) ** 2) * h * 0.09
        pts.append((xx * SS, yy * SS))
    lower = [(px, py + h * 0.1 * SS) for px, py in reversed(pts)]
    md.polygon(pts + lower, fill=255)
    box = m.getbbox(); sub = m.crop(box)
    img.alpha_composite(textured_fill(sub, col, mixc(col, (0, 0, 0, 255), .5), mixc(col, (140, 120, 100, 255), .25), 22 * SS, seed + 3, (4, .2), 1.5), (box[0], box[1]))
    wood_block(img, (x - p * 0.35, base - h * 0.93, x + p * 0.35, base - h * 0.8), seed + 4, col, mixc(col, (0, 0, 0, 255), .5), mixc(col, (140, 120, 100, 255), .25), True)


def grain(img, amount=10, seed=0):
    a = np.asarray(img, np.float32)
    n = np.random.default_rng(seed).normal(0, amount, a.shape[:2])[..., None]
    a[..., :3] = np.clip(a[..., :3] + n, 0, 255)
    return Image.fromarray(a.astype(np.uint8), 'RGBA')


def grade(img, lift=(12, 16, 14), gamma=1.0, sat=0.85, vignette=0.5):
    a = np.asarray(img, np.float32)[..., :3] / 255
    lum = (a * [0.3, 0.59, 0.11]).sum(-1, keepdims=True)
    a = lum + (a - lum) * sat
    a = a ** gamma
    a = a * (1 - np.array(lift) / 255) + np.array(lift) / 255
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / (w * 0.65)) ** 2 + ((yy - h * 0.55) / (h * 0.7)) ** 2)
    a *= (1 - vignette * np.clip(r - 0.35, 0, 1) ** 1.5)[..., None]
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert('RGBA')


def finish(img, name, **kw):
    out = img.resize((W, H), Image.LANCZOS)
    out = grade(out, **kw)
    out = grain(out, 6, hash(name) % 1000)
    out.convert('RGB').save(f'{OUT}/{name}.webp', 'WEBP', quality=82, method=6)
    out.convert('RGB').resize((W // 3, H // 3)).save(f'{OUT}/preview-{name}.jpg', quality=85)
    print('rendered', name)


OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
PAL_CEDAR = [hexc('#141c17'), hexc('#1c2820'), hexc('#26342a'), hexc('#324337'), hexc('#435645')]
PAL_PINE = [hexc('#0e1511'), hexc('#162019'), hexc('#1f2d23'), hexc('#2b3d30'), hexc('#3e5445')]
PAL_MAPLE = [hexc('#111812'), hexc('#19231a'), hexc('#223022'), hexc('#2e3f2c'), hexc('#3f5239'), hexc('#566a4c')]
PAL_BUSH = [hexc('#0e140f'), hexc('#162018'), hexc('#1f2c20'), hexc('#2a3a2a'), hexc('#3a4c37'), hexc('#4d6048')]
BARK = (hexc('#16110e'), hexc('#2b231d'), hexc('#4a4038'))
FOG = hexc('#a2aaa4')


def ground(img, y0, y1, seed, base=hexc('#2b3326'), dark=hexc('#141911'), light=hexc('#46513a'), pebbles=0):
    h = (y1 - y0) * SS; m = Image.new('L', (SW, h), 255)
    t = textured_fill(m, base, dark, light, 44 * SS, seed, stretch=(3, 1), contrast=1.15)
    a = np.asarray(t, np.float32); a[..., :3] *= np.linspace(0.75, 1.05, h)[:, None, None]
    img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'), (0, y0 * SS))
    rnd = random.Random(seed); d = ImageDraw.Draw(img)
    for _ in range(pebbles):
        x = rnd.uniform(0, SW); y = rnd.uniform(y0, y1) * SS; r = rnd.uniform(1.5, 4) * SS
        c = rnd.choice([hexc('#5a5c55'), hexc('#6d6e66'), hexc('#3e403a')]); d.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=c)


def forest_layers(img, y, fog, seeds, counts, hs, fogs, blurs, pal=None, bark=BARK):
    for sd, cnt, (h0, h1), fa, bl in zip(seeds, counts, hs, fogs, blurs):
        L = layer(); r = random.Random(sd)
        for i in range(cnt):
            cedar(L, (i + r.uniform(0, 1)) * (W / cnt) * SS, y * SS, r.uniform(h0, h1) * SS, r.uniform(200, 280) * SS, sd * 10 + i, pal or PAL_CEDAR, bark)
        img.alpha_composite(atmos(L, fog, fa, blur=bl))
        img.alpha_composite(fog_layer(fog, y - (h0 + h1) / 3, y + 40, 0.55, sd))


def engawa():
    fog = hexc('#8c958f')
    img = gradient(hexc('#838c86'), hexc('#454e48'))
    forest_layers(img, 640, fog, [101, 102], [11, 8], [(420, 560), (520, 660)], [0.78, 0.6], [3, 1.8])
    wall = layer(); m = Image.new('L', (SW, 240 * SS), 255)
    wall.alpha_composite(textured_fill(m, hexc('#5f655e'), hexc('#3e443d'), hexc('#798078'), 30 * SS, 3, contrast=1.4), (0, 540 * SS))
    d = ImageDraw.Draw(wall); d.rectangle([0, 520 * SS, SW, 548 * SS], fill=hexc('#232723'))
    for x in range(0, SW, 22 * SS): d.arc([x, 508 * SS, x + 22 * SS, 532 * SS], 180, 360, fill=hexc('#171a17'), width=3 * SS)
    img.alpha_composite(atmos(wall, fog, 0.4, blur=0.8))
    back = layer()
    pine(back, 1250 * SS, 1060 * SS, 920 * SS, 33, PAL_PINE, BARK, lean=-0.3, pads=8, spread=1.25)
    maple(back, 260 * SS, 1060 * SS, 820 * SS, 44, PAL_MAPLE, BARK, lean=0.25)
    img.alpha_composite(atmos(back, fog, 0.32, blur=0.6))
    img.alpha_composite(fog_layer(fog, 700, 980, 0.45, 2))
    mid = layer()
    maple(mid, 640 * SS, 1080 * SS, 860 * SS, 21, PAL_MAPLE, BARK, lean=0.1)
    maple(mid, 960 * SS, 1080 * SS, 700 * SS, 27, PAL_MAPLE, BARK, lean=-0.2)
    img.alpha_composite(atmos(mid, fog, 0.12, blur=0.2))
    ground(img, 960, 1120, 71, pebbles=900)
    near = layer()
    toro(near, 1180, 1085, 200, 5)
    bushes(near, 1100, -40, 1840, 7, PAL_BUSH, count=20, rmin=70, rmax=160)
    for i, (sx, sy) in enumerate([(520, 1098), (760, 1104), (1000, 1098)]):
        stone(near, sx, sy, 58, 14, 40 + i, hexc('#454a44'))
    img.alpha_composite(atmos(near, fog, 0.06))
    fr = layer()
    wood_block(fr, (0, 0, 1800, 92), 51, hexc('#1f1712'), hexc('#0b0806'), hexc('#34281f'))
    wood_block(fr, (0, 92, 1800, 112), 52, hexc('#17110d'), hexc('#080605'), hexc('#281e17'))
    wood_block(fr, (0, 0, 64, 1120), 53, hexc('#18120e'), hexc('#080605'), hexc('#2a2019'), True)
    paper(fr, (1400, 124, 1792, 1100), 54, hexc('#a8a292'), lit=0.62, grid=(3, 6))
    wood_block(fr, (1380, 112, 1400, 1120), 55, hexc('#18120e'), hexc('#080605'), hexc('#2a2019'), True)
    img.alpha_composite(fr)
    wood_planks(img, 1120, 1400, 61, hexc('#3f332a'), hexc('#17120e'), hexc('#5d4d3e'), plank_h=40)
    d = ImageDraw.Draw(img); d.rectangle([0, 1118 * SS, SW, 1124 * SS], fill=hexc('#0e0a08'))
    finish(img, 'engawa', lift=(8, 11, 10), sat=0.72, gamma=1.08, vignette=0.6)


PAL_SAKURA = [hexc('#6e3a48'), hexc('#9a5566'), hexc('#c07a8c'), hexc('#dc9fb0'), hexc('#efc3cf'), hexc('#f8dde4')]


def plaster(img, box, seed, base, dark, light):
    x0, y0, x1, y1 = (int(v * SS) for v in box)
    img.alpha_composite(textured_fill(Image.new('L', (x1 - x0, y1 - y0), 255), base, dark, light, 60 * SS, seed, contrast=0.75), (x0, y0))


def vertical_boards(img, box, seed, base, dark, light, board=70):
    x0, y0, x1, y1 = box
    wood_block(img, box, seed, base, dark, light, True)
    d = ImageDraw.Draw(img)
    for x in range(int(x0), int(x1), board):
        d.rectangle([x * SS, y0 * SS, x * SS + 2 * SS, y1 * SS], fill=mixc(dark, (0, 0, 0, 255), .4))


def tatami(img, y0, y1, seed, lit=1.0, base=hexc('#5b5a3e')):
    h = (y1 - y0) * SS
    n = fbm(SW, h, 30 * SS, 4, seed, (4, 1))
    weave = (np.sin(np.arange(h)[:, None] / (1.3 * SS)) * 0.5 + 0.5) * 0.25
    v = np.clip(0.55 * n + weave + 0.2, 0, 1)
    b = np.array(base[:3], np.float32)
    rgb = b[None, None] * (0.55 + 0.6 * v[..., None]) * lit
    rgb *= np.linspace(0.7, 1.05, h)[:, None, None]
    img.alpha_composite(Image.fromarray(np.dstack([np.clip(rgb, 0, 255), np.full((h, SW), 255)]).astype(np.uint8), 'RGBA'), (0, y0 * SS))
    d = ImageDraw.Draw(img); heri = hexc('#1a1712')
    for x in range(-200, W + 400, 620):
        d.rectangle([x * SS, y0 * SS, x * SS + 9 * SS, y1 * SS], fill=heri)
    d.rectangle([0, int((y0 + (y1 - y0) * 0.55) * SS), SW, int((y0 + (y1 - y0) * 0.55) * SS) + 8 * SS], fill=heri)


def glow(img, cx, cy, r, color, strength):
    yy, xx = np.mgrid[0:SH // 4, 0:SW // 4]
    d = np.sqrt((xx - cx * SS / 4) ** 2 + (yy - cy * SS / 4) ** 2) / (r * SS / 4)
    a = np.clip(1 - d, 0, 1) ** 2 * strength * 255
    g = Image.new('RGBA', (SW // 4, SH // 4), color); g.putalpha(Image.fromarray(a.astype(np.uint8)))
    img.alpha_composite(g.resize((SW, SH), Image.BICUBIC))


def darken(img, amount, tint=(10, 14, 28)):
    a = np.asarray(img, np.float32); a[..., :3] = a[..., :3] * (1 - amount) + np.array(tint, np.float32) * amount
    return Image.fromarray(a.astype(np.uint8), 'RGBA')


def ceramic(img, cx, base, w, h, seed, col):
    m = Image.new('L', (int(w * SS), int(h * SS)), 0); md = ImageDraw.Draw(m)
    md.chord([0, -h * SS, w * SS - 1, h * SS - 1], 0, 180, fill=255)
    t = textured_fill(m, col, mixc(col, (0, 0, 0, 255), .5), mixc(col, (255, 255, 255, 255), .25), 6 * SS, seed, contrast=1.2)
    img.alpha_composite(t, (int((cx - w / 2) * SS), int((base - h) * SS)))
    d = ImageDraw.Draw(img); d.line([((cx - w / 2) * SS, (base - h) * SS), ((cx + w / 2) * SS, (base - h) * SS)], fill=mixc(col, (255, 255, 255, 255), .3), width=2 * SS)


def chochin(img, cx, cy, r, lit=True):
    m = Image.new('L', (int(r * 2 * SS), int(r * 2.8 * SS)), 0); ImageDraw.Draw(m).ellipse([0, 0, m.width - 1, m.height - 1], fill=255)
    base = hexc('#d98c45') if lit else hexc('#6d5a44')
    t = textured_fill(m, base, mixc(base, (60, 20, 0, 255), .45), mixc(base, (255, 230, 170, 255), .4), 5 * SS, 3, contrast=1)
    a = np.asarray(t, np.float32); yy = np.linspace(-1, 1, a.shape[0])[:, None]
    for k in range(-5, 6): a[np.abs(yy[:, 0] - k * 0.17) < 0.012, :, :3] *= 0.55
    xx = np.linspace(-1, 1, a.shape[1])[None, :]; a[..., :3] *= (1 - 0.45 * xx ** 2)[..., None]
    img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'), (int((cx - r) * SS), int((cy - r * 1.4) * SS)))
    d = ImageDraw.Draw(img)
    for yy_ in (cy - r * 1.45, cy + r * 1.3):
        d.rectangle([(cx - r * 0.7) * SS, yy_ * SS, (cx + r * 0.7) * SS, (yy_ + r * 0.16) * SS], fill=hexc('#140d09'))
    d.line([(cx * SS, 0), (cx * SS, (cy - r * 1.45) * SS)], fill=hexc('#0d0906'), width=2 * SS)


def pool(img, cx, cy, rx, ry, seed):
    m = Image.new('L', (int(rx * 2 * SS), int(ry * 2 * SS)), 0); ImageDraw.Draw(m).ellipse([0, 0, m.width - 1, m.height - 1], fill=255)
    t = textured_fill(m, hexc('#1e2c2c'), hexc('#0c1414'), hexc('#3e5352'), 20 * SS, seed, stretch=(5, 1), contrast=1.4)
    img.alpha_composite(t, (int((cx - rx) * SS), int((cy - ry) * SS)))
    rnd = random.Random(seed)
    for i in range(46):
        a = i / 46 * math.tau + rnd.uniform(-.05, .05)
        stone(img, cx + math.cos(a) * rx * 1.02, cy + math.sin(a) * ry * 1.05, rnd.uniform(40, 70), rnd.uniform(22, 36), seed + i, hexc('#454a45'))


def kitchen():
    img = gradient(hexc('#2a2019'), hexc('#1a130f'))
    vertical_boards(img, (0, 0, 1800, 1150), 11, hexc('#3a2c22'), hexc('#1a130e'), hexc('#54412f'))
    # lattice window to a foggy garden
    win = gradient(hexc('#7d8781'), hexc('#46504a'))
    g = layer(); maple(g, 520 * SS, 700 * SS, 700 * SS, 5, PAL_MAPLE, BARK, 0.2); bushes(g, 720, 200, 900, 9, PAL_BUSH, 8, 60, 120)
    win.alpha_composite(atmos(g, hexc('#8a938d'), .3, .4)); win.alpha_composite(fog_layer(hexc('#8a938d'), 300, 700, .6, 4))
    m = Image.new('L', (SW, SH), 0); ImageDraw.Draw(m).rectangle([240 * SS, 180 * SS, 820 * SS, 640 * SS], fill=255)
    img.paste(win, (0, 0), m)
    d = ImageDraw.Draw(img)
    for x in range(240, 821, 36): d.rectangle([x * SS, 180 * SS, (x + 7) * SS, 640 * SS], fill=hexc('#1b130e'))
    for y in (180, 400, 640): d.rectangle([232 * SS, (y - 6) * SS, 828 * SS, (y + 8) * SS], fill=hexc('#1b130e'))
    # shelf with ceramics
    wood_block(img, (960, 470, 1660, 492), 12, hexc('#3f3023'), hexc('#1a130e'), hexc('#5a4633'))
    wood_block(img, (960, 700, 1660, 722), 13, hexc('#3f3023'), hexc('#1a130e'), hexc('#5a4633'))
    for i, (cx, w, h, c) in enumerate([(1010, 70, 34, '#5b3a2a'), (1100, 90, 40, '#3c4a52'), (1200, 60, 50, '#8b7c62'), (1300, 96, 36, '#2e2a26'), (1420, 70, 60, '#6c5a3e'), (1530, 88, 42, '#44564f')]):
        ceramic(img, cx, 470, w, h, 20 + i, hexc(c))
    for i, (cx, w, h, c) in enumerate([(1030, 110, 60, '#2a2522'), (1180, 80, 44, '#7a6a52'), (1330, 120, 54, '#3b4a45'), (1500, 90, 70, '#5a3a2a')]):
        ceramic(img, cx, 700, w, h, 40 + i, hexc(c))
    # kamado stove
    m = Image.new('L', (int(460 * SS), int(300 * SS)), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, m.width - 1, m.height - 1], 30 * SS, fill=255)
    img.alpha_composite(textured_fill(m, hexc('#5e4f3e'), hexc('#3a2e22'), hexc('#76664f'), 34 * SS, 50, contrast=0.9), (int(1240 * SS), int(850 * SS)))
    d.ellipse([1330 * SS, 960 * SS, 1440 * SS, 1060 * SS], fill=hexc('#120c08'))
    glow(img, 1385, 1030, 120, hexc('#e0702a'), .45)
    d.ellipse([1300 * SS, 800 * SS, 1600 * SS, 880 * SS], fill=hexc('#171513')); d.rectangle([1320 * SS, 760 * SS, 1580 * SS, 840 * SS], fill=hexc('#1f1c19'))
    # noren doorway
    for i in range(3):
        x0 = 30 + i * 62
        m = Image.new('L', (int(58 * SS), int(420 * SS)), 255)
        img.alpha_composite(textured_fill(m, hexc('#1e2a3b'), hexc('#0f1520'), hexc('#2c3b52'), 16 * SS, 60 + i, (1, 4)), (int(x0 * SS), 0))
    d.ellipse([70 * SS, 250 * SS, 150 * SS, 330 * SS], fill=hexc('#c9c1ae')); d.ellipse([88 * SS, 262 * SS, 150 * SS, 320 * SS], fill=hexc('#1e2a3b'))
    chochin(img, 1560, 300, 62, True)
    glow(img, 1560, 300, 520, hexc('#e39a55'), .38)
    ground(img, 1150, 1400, 70, hexc('#3b342c'), hexc('#1a1612'), hexc('#51483c'), pebbles=300)
    wood_block(img, (0, 1128, 1800, 1156), 71, hexc('#3a2c21'), hexc('#150f0b'), hexc('#57432f'))
    finish(img, 'kitchen', lift=(10, 8, 6), sat=0.8, gamma=1.05, vignette=0.55)


def onsen():
    fog = hexc('#8f9892')
    img = gradient(hexc('#8c948f'), hexc('#48514b'))
    forest_layers(img, 720, fog, [201, 202, 203], [10, 8, 6], [(480, 620), (620, 760), (760, 920)], [0.75, 0.52, 0.3], [3, 1.6, .7])
    # bamboo fence
    f = layer(); d = ImageDraw.Draw(f); rnd = random.Random(3)
    for x in range(0, W, 26):
        c = mixc(hexc('#4a4a33'), hexc('#26261a'), rnd.random())
        d.rectangle([x * SS, 760 * SS, (x + 22) * SS, 980 * SS], fill=c)
        for y in (800, 880, 950): d.line([(x * SS, y * SS), ((x + 22) * SS, y * SS)], fill=mixc(c, (0, 0, 0, 255), .5), width=2 * SS)
    d.rectangle([0, 840 * SS, SW, 852 * SS], fill=hexc('#2a2418'))
    img.alpha_composite(atmos(f, fog, .18, .3))
    img.alpha_composite(fog_layer(fog, 700, 1000, .5, 7))
    ground(img, 960, 1400, 81, hexc('#30352e'), hexc('#161a15'), hexc('#4a5046'), pebbles=1400)
    pool(img, 900, 1080, 620, 110, 90)
    near = layer(); bushes(near, 1000, -60, 260, 8, PAL_BUSH, 5, 70, 130); bushes(near, 1000, 1560, 1860, 9, PAL_BUSH, 5, 70, 130)
    img.alpha_composite(near)
    for i, (x, y, rx, ry) in enumerate([(900, 1330, 190, 46), (520, 1300, 130, 40), (1300, 1310, 150, 44), (160, 1250, 110, 50), (1660, 1260, 120, 54)]):
        stone(img, x, y, rx, ry, 300 + i, hexc('#4b4f49'))
    img.alpha_composite(fog_layer(hexc('#d6dbd7'), 900, 1150, .5, 11, 180))
    finish(img, 'onsen', lift=(9, 12, 11), sat=0.72, gamma=1.08, vignette=0.55)


def bedroom(lit):
    img = gradient(hexc('#3a352c'), hexc('#26221c'))
    plaster(img, (0, 0, 1800, 1140), 21, hexc('#4b4436'), hexc('#2d281f'), hexc('#5e5646'))
    wood_block(img, (0, 0, 1800, 70), 22, hexc('#241a14'), hexc('#0e0a08'), hexc('#3a2c22'))
    # tokonoma alcove with scroll and ikebana
    wood_block(img, (70, 150, 470, 1080), 23, hexc('#2b241c'), hexc('#15110c'), hexc('#3b3226'), True)
    plaster(img, (90, 170, 450, 1060), 24, hexc('#3d372c'), hexc('#241f18'), hexc('#4d4638'))
    scroll = gradient(hexc('#cfc6b0'), hexc('#b8ae96'), h=int(560 * SS), w=int(160 * SS))
    sc = layer(); sc.alpha_composite(scroll, (int(190 * SS), int(220 * SS)))
    m = layer(); pine(m, 270 * SS, 740 * SS, 420 * SS, 7, [hexc('#1a1a18'), hexc('#2a2a26'), hexc('#3a3934'), hexc('#4d4b45')], (hexc('#111111'), hexc('#222222'), hexc('#333333')), lean=.2, pads=4, spread=.5)
    sc.alpha_composite(atmos(m, hexc('#bdb39b'), .35))
    mm = Image.new('L', (SW, SH), 0); ImageDraw.Draw(mm).rectangle([190 * SS, 220 * SS, 350 * SS, 780 * SS], fill=255); img.paste(sc, (0, 0), mm)
    d = ImageDraw.Draw(img); d.rectangle([180 * SS, 205 * SS, 360 * SS, 222 * SS], fill=hexc('#2a1d14')); d.rectangle([180 * SS, 778 * SS, 360 * SS, 796 * SS], fill=hexc('#2a1d14'))
    ceramic(img, 270, 1060, 90, 70, 5, hexc('#2b3a3a'))
    ik = layer(); maple(ik, 270 * SS, 995 * SS, 330 * SS, 12, PAL_SAKURA, BARK, -.2); img.alpha_composite(atmos(ik, hexc('#3a352c'), .25))
    # shoji window with moonlight and a pine shadow
    moon = hexc('#9fa3a6') if not lit else hexc('#b3ab97')
    paper(img, (640, 150, 1560, 1000), 25, moon, lit=0.85 if not lit else 0.7, grid=(4, 5))
    sh = layer(); pine(sh, 1400 * SS, 1100 * SS, 900 * SS, 13, [hexc('#000000')] * 5, (hexc('#000000'), hexc('#000000'), hexc('#000000')), lean=-.4, pads=6)
    sh = sh.filter(ImageFilter.GaussianBlur(4 * SS)); a = np.asarray(sh, np.float32); a[..., 3] *= 0.55
    mk = Image.new('L', (SW, SH), 0); ImageDraw.Draw(mk).rectangle([640 * SS, 150 * SS, 1560 * SS, 1000 * SS], fill=255)
    img.paste(Image.fromarray(a.astype(np.uint8), 'RGBA'), (0, 0), ImageChops_min(mk, Image.fromarray(a[..., 3].astype(np.uint8))))
    paper_frame = hexc('#1d150f')
    tatami(img, 1140, 1400, 26, lit=1.0 if lit else 0.8)
    # futon under the cat
    m = Image.new('L', (int(900 * SS), int(150 * SS)), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, m.width - 1, m.height - 1], 40 * SS, fill=255)
    img.alpha_composite(textured_fill(m, hexc('#2e3446'), hexc('#1a1f2c'), hexc('#3e4660'), 40 * SS, 27, (3, 1), 0.8), (int(450 * SS), int(1230 * SS)))
    d = ImageDraw.Draw(img)
    for x in range(520, 1330, 90): d.line([(x * SS, 1240 * SS), (x * SS, 1370 * SS)], fill=hexc('#20263a'), width=2 * SS)
    # andon lamp
    ax, ab = 330, 1300
    wood_block(img, (ax - 70, ab - 20, ax + 70, ab), 28, hexc('#241a13'), hexc('#0e0a07'), hexc('#3a2b1f'))
    pap = hexc('#f0d59a') if lit else hexc('#5f584a')
    m = Image.new('L', (int(110 * SS), int(200 * SS)), 255)
    img.alpha_composite(textured_fill(m, pap, mixc(pap, (0, 0, 0, 255), .25), mixc(pap, (255, 255, 255, 255), .2), 5 * SS, 29), (int((ax - 55) * SS), int((ab - 240) * SS)))
    for xx in (ax - 58, ax + 52): d.rectangle([xx * SS, (ab - 250) * SS, (xx + 6) * SS, ab * SS], fill=hexc('#160f0a'))
    d.rectangle([(ax - 58) * SS, (ab - 144) * SS, (ax + 58) * SS, (ab - 138) * SS], fill=hexc('#160f0a'))
    d.rectangle([(ax - 58) * SS, (ab - 250) * SS, (ax + 58) * SS, (ab - 242) * SS], fill=hexc('#160f0a'))
    if lit:
        glow(img, ax, ab - 150, 900, hexc('#e6b46a'), .42); glow(img, ax, ab - 150, 260, hexc('#ffd999'), .35)
        finish(img, 'bedroom_on', lift=(10, 8, 6), sat=0.8, gamma=1.02, vignette=0.6)
    else:
        img = darken(img, .55, (8, 12, 26)); glow(img, 1100, 560, 700, hexc('#8fa0b8'), .22)
        finish(img, 'bedroom_off', lift=(6, 8, 12), sat=0.7, gamma=1.1, vignette=0.7)


def ImageChops_min(a, b):
    from PIL import ImageChops
    return ImageChops.darker(a, b)


def wardrobe():
    img = gradient(hexc('#211a14'), hexc('#140f0c'))
    plaster(img, (0, 0, 1800, 1140), 31, hexc('#2e2720'), hexc('#1a1511'), hexc('#3b3229'))
    # six-panel byōbu with gold leaf, mist bands and a blossoming sakura
    x0, y0, x1, y1 = 120, 150, 1680, 1060
    gold = Image.new('RGBA', (int((x1 - x0) * SS), int((y1 - y0) * SS)))
    gw, gh = gold.size; n = fbm(gw, gh, 40 * SS, 4, 32)
    sq = 70 * SS; rng = np.random.default_rng(3)
    tiles = rng.uniform(.82, 1.08, (gh // sq + 1, gw // sq + 1))
    tv = np.kron(tiles, np.ones((sq, sq)))[:gh, :gw]
    base = np.array([150, 118, 62], np.float32)
    rgb = base * (0.6 + 0.5 * n[..., None]) * tv[..., None]
    gold = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), np.full((gh, gw), 255)]).astype(np.uint8), 'RGBA')
    art = layer(); maple(art, 1180 * SS, 1060 * SS, 1100 * SS, 77, PAL_SAKURA, (hexc('#1a120e'), hexc('#2c201a'), hexc('#46372c')), -.35)
    maple(art, 420 * SS, 1060 * SS, 700 * SS, 78, PAL_SAKURA, (hexc('#1a120e'), hexc('#2c201a'), hexc('#46372c')), .3)
    screen = layer(); screen.alpha_composite(gold, (int(x0 * SS), int(y0 * SS)))
    screen.alpha_composite(fog_layer(hexc('#e2c98e'), 820, 980, .7, 33, 200)); screen.alpha_composite(art)
    screen.alpha_composite(fog_layer(hexc('#e8d19a'), 300, 420, .55, 34, 220))
    mk = Image.new('L', (SW, SH), 0); ImageDraw.Draw(mk).rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], fill=255)
    screen = darken(screen, .35, (20, 12, 6))
    img.paste(screen, (0, 0), mk)
    d = ImageDraw.Draw(img)
    for i in range(7):
        x = x0 + (x1 - x0) * i / 6
        d.rectangle([(x - 7) * SS, y0 * SS, (x + 7) * SS, y1 * SS], fill=hexc('#1a0f0a'))
        # fold shading
        if i < 6:
            shade = Image.new('RGBA', (int((x1 - x0) / 6 * SS), int((y1 - y0) * SS)), (0, 0, 0, 0))
            a = np.zeros((shade.height, shade.width, 4), np.float32); ramp = np.linspace(0, 1, shade.width)
            a[..., 3] = (ramp if i % 2 else 1 - ramp)[None, :] * 70
            img.alpha_composite(Image.fromarray(a.astype(np.uint8), 'RGBA'), (int(x * SS), int(y0 * SS)))
    d.rectangle([(x0 - 7) * SS, (y0 - 14) * SS, (x1 + 7) * SS, y0 * SS], fill=hexc('#1a0f0a')); d.rectangle([(x0 - 7) * SS, y1 * SS, (x1 + 7) * SS, (y1 + 14) * SS], fill=hexc('#1a0f0a'))
    tatami(img, 1140, 1400, 35, lit=.8)
    glow(img, 900, 500, 900, hexc('#d6a860'), .15)
    finish(img, 'wardrobe', lift=(9, 7, 5), sat=0.85, gamma=1.05, vignette=0.6)


def games():
    fog = hexc('#8d9690')
    img = gradient(hexc('#8e9791'), hexc('#4a534d'))
    forest_layers(img, 900, fog, [301, 302, 303], [12, 9, 6], [(600, 760), (760, 900), (900, 1080)], [0.8, 0.58, 0.36], [3.2, 1.8, .8])
    t = layer(); torii(t, 900, 1180, 820, 820, 7, hexc('#3a1f18'))
    img.alpha_composite(atmos(t, fog, .12))
    near = layer()
    cedar(near, -60 * SS, 1300 * SS, 1500 * SS, 380 * SS, 991, PAL_CEDAR, BARK)
    cedar(near, 1860 * SS, 1300 * SS, 1500 * SS, 380 * SS, 992, PAL_CEDAR, BARK)
    img.alpha_composite(near)
    ground(img, 1150, 1400, 91, pebbles=1500)
    for i, x in enumerate(range(620, 1200, 120)):
        stone(img, x + (i % 2) * 20, 1300 - i * 3, 70, 16, 400 + i, hexc('#4c504a'))
    toro(img, 360, 1250, 250, 8); toro(img, 1440, 1250, 250, 9)
    img.alpha_composite(fog_layer(fog, 1000, 1250, .4, 12))
    finish(img, 'games', lift=(9, 12, 11), sat=0.7, gamma=1.1, vignette=0.6)


# ───────────── portrait backgrounds for mini-games ─────────────

def g_forest_night():
    set_size(1400, 1800); fog = hexc('#3a4550')
    img = gradient(hexc('#1c2430'), hexc('#0c1012'))
    forest_layers(img, 1200, fog, [401, 402, 403], [7, 6, 4], [(800, 1000), (1000, 1250), (1300, 1600)], [0.7, 0.45, 0.2], [3, 1.6, .6],
                  pal=[hexc('#0a0e0c'), hexc('#10160f'), hexc('#161e17'), hexc('#1d271e'), hexc('#26332a')])
    ground(img, 1500, 1800, 93, hexc('#141914'), hexc('#080a08'), hexc('#20271f'), pebbles=0)
    img.alpha_composite(fog_layer(hexc('#5a6878'), 1250, 1600, .5, 14))
    finish(img, 'g_forest', lift=(4, 6, 10), sat=0.75, gamma=1.15, vignette=0.7)


def g_temple_night():
    set_size(1400, 1800); fog = hexc('#4a5460')
    img = gradient(hexc('#262d36'), hexc('#0e1113'))
    forest_layers(img, 1150, fog, [501, 502], [8, 6], [(700, 900), (900, 1150)], [0.65, 0.4], [2.6, 1.2],
                  pal=[hexc('#0a0e0c'), hexc('#10160f'), hexc('#161e17'), hexc('#1d271e'), hexc('#26332a')])
    t = layer(); torii(t, 700, 1250, 1000, 900, 17, hexc('#2e1813')); img.alpha_composite(atmos(t, fog, .15))
    ground(img, 1250, 1800, 94, hexc('#1b1f1b'), hexc('#0a0c0a'), hexc('#2b302a'), pebbles=0)
    toro(img, 220, 1450, 280, 18); toro(img, 1180, 1450, 280, 19)
    glow(img, 220, 1330, 160, hexc('#e8a050'), .35); glow(img, 1180, 1330, 160, hexc('#e8a050'), .35)
    img.alpha_composite(fog_layer(hexc('#6a7480'), 1100, 1450, .45, 15))
    finish(img, 'g_temple', lift=(5, 6, 10), sat=0.75, gamma=1.12, vignette=0.7)


def g_river():
    set_size(1400, 1800); fog = hexc('#8a938e')
    img = gradient(hexc('#8a938e'), hexc('#3e4742'))
    # gorge slopes
    for k, (col, top, fa) in enumerate([(hexc('#56605a'), 380, .6), (hexc('#3a443d'), 520, .35)]):
        L = layer(); r = random.Random(k)
        for i in range(9 + k * 3):
            x = r.uniform(-100, 1500) * SS
            cedar(L, x, (top + 520 + r.uniform(-60, 60)) * SS, r.uniform(380, 560) * SS, 220 * SS, 600 + k * 20 + i, PAL_CEDAR, BARK)
        img.alpha_composite(atmos(L, fog, fa, 1.5 - k))
        img.alpha_composite(fog_layer(fog, top + 200, top + 600, .6, 20 + k))
    d = ImageDraw.Draw(img)
    # suspension bridge in the mist
    for x in range(260, 1140, 18): d.line([(x * SS, 820 * SS), (x * SS, (838 + 30 * math.sin((x - 260) / 880 * math.pi)) * SS)], fill=hexc('#3b3a35'), width=2 * SS)
    d.line([(260 * SS, 820 * SS), (1140 * SS, 820 * SS)], fill=hexc('#34332f'), width=3 * SS)
    pts = [((260 + i * 22) * SS, (840 + 30 * math.sin(i * 22 / 880 * math.pi)) * SS) for i in range(41)]; d.line(pts, fill=hexc('#2d2c28'), width=5 * SS)
    img.alpha_composite(fog_layer(fog, 700, 950, .5, 25))
    m = Image.new('L', (SW, int(420 * SS)), 255)
    img.alpha_composite(textured_fill(m, hexc('#25302e'), hexc('#101716'), hexc('#4a5a58'), 30 * SS, 26, (6, 1), 1.5), (0, int(1080 * SS)))
    ground(img, 1480, 1800, 95, hexc('#34332c'), hexc('#161512'), hexc('#4e4c42'), pebbles=1800)
    for i in range(7): stone(img, 100 + i * 210, 1490 + (i % 2) * 20, 110, 40, 700 + i, hexc('#4a4d47'))
    bushes(img, 1500, -80, 300, 27, PAL_BUSH, 4, 60, 110)
    finish(img, 'g_river', lift=(9, 12, 11), sat=0.72, gamma=1.08, vignette=0.6)


def g_field_night():
    set_size(1400, 1800); fog = hexc('#3c4858')
    img = gradient(hexc('#141c2a'), hexc('#0b0f12'))
    glow(img, 1050, 320, 300, hexc('#c9d2dc'), .35); d = ImageDraw.Draw(img); d.ellipse([1010 * SS, 280 * SS, 1090 * SS, 360 * SS], fill=hexc('#d9dfe4'))
    forest_layers(img, 900, fog, [801, 802], [10, 8], [(260, 360), (340, 460)], [0.7, 0.5], [2, 1],
                  pal=[hexc('#0a0e0c'), hexc('#10160f'), hexc('#161e17'), hexc('#1d271e'), hexc('#26332a')])
    grass = Image.new('RGBA', (SW, int(900 * SS)), (0, 0, 0, 0)); gd = ImageDraw.Draw(grass); rnd = random.Random(4)
    for _ in range(26000):
        x = rnd.uniform(0, SW); y = rnd.uniform(0, 900 * SS); h = rnd.uniform(14, 40) * SS * (0.4 + y / (900 * SS))
        c = mixc(hexc('#0c120e'), hexc('#2a3a2c'), rnd.random() * (0.3 + 0.7 * (1 - y / (900 * SS))))
        gd.line([(x, y), (x + rnd.uniform(-10, 10) * SS, y - h)], fill=c, width=SS)
    base = gradient(hexc('#141c16'), hexc('#070a08'), h=int(900 * SS)); base.alpha_composite(grass)
    img.alpha_composite(base, (0, int(900 * SS)))
    img.alpha_composite(fog_layer(fog, 850, 1100, .55, 30))
    finish(img, 'g_field', lift=(4, 6, 10), sat=0.8, gamma=1.12, vignette=0.7)


def g_room_night():
    set_size(1400, 1800)
    img = gradient(hexc('#1a1714'), hexc('#0c0a09'))
    plaster(img, (0, 0, 1400, 1200), 61, hexc('#2a251e'), hexc('#15120e'), hexc('#35302a'))
    paper(img, (250, 220, 1150, 1020), 62, hexc('#6d6c68'), lit=.55, grid=(4, 5))
    wood_block(img, (0, 0, 1400, 80), 63, hexc('#1c1510'), hexc('#0a0706'), hexc('#2c2119'))
    tatami(img, 1200, 1800, 64, lit=.6)
    img = darken(img, .25, (6, 8, 16))
    finish(img, 'g_room', lift=(4, 5, 8), sat=0.75, gamma=1.1, vignette=0.75)



if __name__ == '__main__':
    which = sys.argv[2:] or ['engawa']
    for n in which:
        set_size(1800, 1400)
        if n == 'bedroom_on': bedroom(True)
        elif n == 'bedroom_off': bedroom(False)
        else: globals()[n]()
