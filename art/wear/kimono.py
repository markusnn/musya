#!/usr/bin/env python3
"""Volumetric kimono for Musya (worn in the sitting neck-slot poses), painted per pixel onto a body model
measured from the sprite frames. Cell = frame pixels x 84..316, y 176..392 of the 384×416 @2x frame, 1:1.
Body: median alpha of the neutral sitting frames → left/right edge per row (the tail side is mirrored).
Shading: torso = surface of revolution r(y) (cylindrical falloff, belly bulge), light from the upper left,
wrap diffuse + silk/cotton sheen, AO under the neck/obi/collar/sleeves, diagonal drape folds (normal bumps).
Pattern is sampled on the unwrapped surface (arc length asin(u)·R, smile curve on t), so it squeezes at the sides.
Sleeves hang at the sides as their own tilted cylinders; front panels left over right; eri with juban;
obi as a band on a wider cylinder with obiage, obijime cord and knot; padded hem (fuki) with the lining showing.
Semi-transparent contact shadows below the hem and inside the collar V fall on the fur.
Usage: kimono.py <outdir> [preview] → <outdir>/kimono.webp (atlas) + kimono.json {w,h,r:{id:[x,y,w,h]}}"""
import json, math, random, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from items import px, H, dk, lt

OUT = sys.argv[1]
ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
X0, Y0, CW, CH = 84, 176, 232, 216          # cell in frame pixels
SS = 2                                         # supersampling (same as P.SS, px() uses it)
TW, TH = 320, 240                              # unwrapped pattern texture (pattern px)
W, HH = TW, TH                                 # pattern painters use these

# ── body model (measured, see docstring) ──
NEUTRAL = {'rest': range(8), 'purr': [0, 1, 2, 5, 7], 'gaze9': range(8), 'gaze10': range(8), 'treat': [5, 6, 7], 'highfive': [0, 7], 'groom': [0, 7]}


def body_edges():
    acc = []
    for st, fr in NEUTRAL.items():
        a = np.asarray(Image.open(f'{ROOT}/assets/{st}@2x.webp').convert('RGBA'))[..., 3].astype(np.float32) / 255
        acc += [a[:, f * 384:(f + 1) * 384] for f in fr]
    m = np.median(np.stack(acc), 0) > .5
    ys = np.arange(150, 400); L = np.zeros(len(ys)); R = np.zeros(len(ys))
    for i, y in enumerate(ys):
        r = np.nonzero(m[y])[0]; L[i], R[i] = (r[0], r[-1]) if len(r) else (L[i - 1], R[i - 1])
    R = np.where(ys >= 310, 399 - L, R)                                    # tail side: mirror the haunch
    k = np.ones(9) / 9; L = np.convolve(np.pad(L, 4, 'edge'), k, 'valid'); R = np.convolve(np.pad(R, 4, 'edge'), k, 'valid')
    return ys, L, R


def cr_open(pts, n=12):
    p = [pts[0]] + list(pts) + [pts[-1]]; out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        for k in range(n + 1):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * (2 * p1[c] + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t2 + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t3) for c in (0, 1)))
    return out


# ── patterns (drawn flat on the unwrapped TW×TH texture) ──
def P5(d, x, y, r, col, center, n=5, rot=0):
    for k in range(n):
        a = k / n * math.tau + rot; ex, ey = x + math.cos(a) * r * .6, y + math.sin(a) * r * .6
        d.ellipse([px(ex - r * .5), px(ey - r * .5), px(ex + r * .5), px(ey + r * .5)], fill=H(col))
    if center: d.ellipse([px(x - r * .25), px(y - r * .25), px(x + r * .25), px(y + r * .25)], fill=H(center))


def scatter(seed, n, box=None):
    box = box or (6, 6, TW - 6, TH - 6); rr = random.Random(seed); n = int(n * 1.8)
    return [(rr.uniform(box[0], box[2]), rr.uniform(box[1], box[3]), rr.random()) for _ in range(n)]


def pat_sakura(d):
    for x, y, t in scatter(1, 34): P5(d, x, y, 7 + t * 4, '#fbe6ee' if t > .5 else '#f4b8cc', '#d0607e', rot=t * 3)
def pat_seigaiha(d):
    for r in range(0, 21):
        for c in range(-1, 14):
            x = c * 26 + (13 if r % 2 else 0); y = r * 13
            for k, col in enumerate(('#f2eee4', '#2a3a6a', '#f2eee4', '#2a3a6a')):
                rad = 15 - k * 4; d.pieslice([px(x - rad), px(y - rad), px(x + rad), px(y + rad)], 180, 360, fill=H(col))
def pat_tsuru(d):
    for x, y, t in scatter(3, 12):
        s = .8 + t * .5; d.polygon([(px(x - 16 * s), px(y)), (px(x), px(y - 9 * s)), (px(x + 16 * s), px(y)), (px(x), px(y - 3 * s))], fill=H('#f4f0e6'))
        d.line([(px(x), px(y - 4 * s)), (px(x + 7 * s), px(y - 12 * s))], fill=H('#f4f0e6'), width=px(2)); d.ellipse([px(x + 6 * s), px(y - 15 * s), px(x + 10 * s), px(y - 11 * s)], fill=H('#d8322a'))
    for x, y, t in scatter(4, 10): d.arc([px(x - 14), px(y - 6), px(x + 14), px(y + 6)], 180, 360, fill=H('#d8b048'), width=px(1.6))
def pat_asagao(d):
    for x, y, t in scatter(5, 26): d.ellipse([px(x - 5), px(y + 2), px(x + 11), px(y + 9)], fill=H('#3a7a4a'))
    for x, y, t in scatter(6, 16): P5(d, x, y, 12 + t * 3, '#3a52c0' if t > .4 else '#7a4ac0', '#f4f0f8')
def pat_momiji(d):
    for x, y, t in scatter(7, 22):
        col = ('#f0a020', '#d83a1a', '#e8c040', '#b82a1a')[int(t * 4)]
        for k in range(5):
            a = -math.pi / 2 + (k - 2) * .62; d.polygon([(px(x), px(y)), (px(x + math.cos(a - .2) * 6), px(y + math.sin(a - .2) * 6)), (px(x + math.cos(a) * 12), px(y + math.sin(a) * 12)), (px(x + math.cos(a + .2) * 6), px(y + math.sin(a + .2) * 6))], fill=H(col))
        d.line([(px(x), px(y)), (px(x), px(y + 8))], fill=H(col), width=px(1.4))
def pat_yagasuri(d):
    for c in range(17):
        x = c * 20
        for r in range(15):
            y = r * 18 + (9 if c % 2 else 0) - 9; col = '#6a3a9a' if (c + r) % 2 else '#f2eee4'
            d.polygon([(px(x), px(y)), (px(x + 10), px(y + 8)), (px(x + 20), px(y)), (px(x + 20), px(y + 12)), (px(x + 10), px(y + 20)), (px(x), px(y + 12))], fill=H(col))
def pat_ichimatsu(d):
    for r in range(15):
        for c in range(19):
            if (r + c) % 2: d.rectangle([px(c * 18 - 2), px(r * 18), px(c * 18 + 16), px(r * 18 + 18)], fill=H('#1a1a1a'))
def pat_kiku(d):
    for x, y, t in scatter(9, 11):
        r = 11 + t * 6; col = '#e8c040' if t > .45 else '#f4f0e6'
        for k in range(16): a = k / 16 * math.tau; d.line([(px(x), px(y)), (px(x + math.cos(a) * r), px(y + math.sin(a) * r))], fill=H(col), width=px(3))
        d.ellipse([px(x - 3), px(y - 3), px(x + 3), px(y + 3)], fill=H('#b8801a'))
def pat_asanoha(d):
    s = 22
    for r in range(-1, 14):
        for c in range(-1, 16):
            x = c * s + (s / 2 if r % 2 else 0); y = r * s * .87
            for k in range(6):
                a = k / 6 * math.tau + math.pi / 6; d.line([(px(x), px(y)), (px(x + math.cos(a) * s * .58), px(y + math.sin(a) * s * .58))], fill=H('#c0304a'), width=px(1.2))
            d.regular_polygon((px(x), px(y), px(s * .58)), 6, rotation=30, outline=H('#c0304a'))
def pat_hotaru(d):
    for x in range(0, TW, 6): d.line([(px(x), px(TH)), (px(x + random.Random(x).uniform(-6, 6)), px(TH - random.Random(x + 1).uniform(20, 46)))], fill=H('#2a5a3a'), width=px(1.6))
    for x, y, t in scatter(11, 18, (10, 20, TW - 10, TH - 50)):
        d.ellipse([px(x - 5), px(y - 5), px(x + 5), px(y + 5)], fill=(210, 250, 120, 90)); d.ellipse([px(x - 2), px(y - 2), px(x + 2), px(y + 2)], fill=(240, 255, 170, 255))
def pat_fuji(d):
    for c in range(12):
        x = 14 + c * 26; L = 5 + (c * 7) % 5
        for k in range(L):
            y = 10 + k * 9; r = 5.5 - k * .35; d.ellipse([px(x - r), px(y - r), px(x + r), px(y + r)], fill=H('#a88ad8' if k % 2 else '#c8b0f0'))
    for x, y, t in scatter(12, 14, (10, 6, TW - 10, 34)): d.ellipse([px(x - 7), px(y - 3), px(x + 7), px(y + 3)], fill=H('#5a8a3a'))
def pat_miko(d): pass


# id, name, base, obi, cord, pattern, obiage (None = yukata, no obiage), fuki lining, silk
KIMONO = [
    ('k_sakura', 'Кимоно «Сакура»', '#e8a0b6', '#c02a2a', '#d8b048', pat_sakura, '#f6dce4', '#c02a2a', 1),
    ('k_seigaiha', 'Кимоно «Волны сэйгайха»', '#2a3a6a', '#d8b048', '#c02a2a', pat_seigaiha, '#e8b8a8', '#c02a2a', 1),
    ('k_tsuru', 'Чёрное кимоно с журавлями', '#1b1920', '#c02a2a', '#d8b048', pat_tsuru, '#e8a0a8', '#b8322a', 1),
    ('k_asagao', 'Юката с вьюнком', '#f4f0e6', '#e8b030', '#2a3a8a', pat_asagao, None, None, 0),
    ('k_momiji', 'Кимоно «Осенние клёны»', '#5a2a1a', '#2f5a3a', '#e8c040', pat_momiji, '#e8c890', '#b8322a', 1),
    ('k_yagasuri', 'Кимоно «Стрелы» и красный пояс', '#f2eee4', '#b8322a', '#f2eee4', pat_yagasuri, '#e8d0e8', '#6a3a9a', 1),
    ('k_ichimatsu', 'Кимоно в клетку итимацу', '#2f7a5a', '#1a1a1a', '#e8e0cc', pat_ichimatsu, '#e8c8a0', '#b8322a', 1),
    ('k_kiku', 'Праздничное кимоно с хризантемами', '#8a1a2a', '#d8b048', '#c02a2a', pat_kiku, '#f0d8a8', '#d8b048', 1),
    ('k_asanoha', 'Розовое кимоно «Асаноха»', '#f4c4d0', '#2a1a1a', '#c02a2a', pat_asanoha, '#f8e8ec', '#c0304a', 1),
    ('k_hotaru', 'Ночная юката со светлячками', '#1a2440', '#a8d8f0', '#e8c040', pat_hotaru, None, None, 0),
    ('k_fuji', 'Кимоно «Глициния»', '#ece4f4', '#6a3a9a', '#d8b048', pat_fuji, '#f4dce8', '#6a3a9a', 1),
    ('k_miko', 'Наряд мико', '#f8f6f0', '#c8281e', '#f8f6f0', pat_miko, None, '#9a1a14', 0),
]

LIGHT = np.array([-.5, -.62, .6]); LIGHT /= np.linalg.norm(LIGHT)
HALF = LIGHT + np.array([0, 0, 1.]); HALF /= np.linalg.norm(HALF)


def rgb(c): return np.array(H(c)[:3], np.float32) / 255
def sstep(a, b, x): t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)


def seg_ridge(X, Y, p0, p1, w, amp):
    """soft fold ridge along a segment; fades at both ends"""
    (x0, y0), (x1, y1) = p0, p1; dx, dy = x1 - x0, y1 - y0; L2 = dx * dx + dy * dy
    t = ((X - x0) * dx + (Y - y0) * dy) / L2; d = np.abs((X - x0) * dy - (Y - y0) * dx) / math.sqrt(L2)
    return amp * np.exp(-(d / w) ** 2) * np.sin(np.clip(t, 0, 1) * math.pi) ** .7


def sample(tex, s, t):
    """bilinear sample of an RGBA float texture at pattern px (s,t), wrapping"""
    h, w = tex.shape[:2]; s = s * SS - .5; t = t * SS - .5
    x0 = np.floor(s).astype(int); y0 = np.floor(t).astype(int); fx = (s - x0)[..., None]; fy = (t - y0)[..., None]
    x0 %= w; y0 = np.clip(y0, 0, h - 1); x1 = (x0 + 1) % w; y1 = np.clip(y0 + 1, 0, h - 1)
    return (tex[y0, x0] * (1 - fx) + tex[y0, x1] * fx) * (1 - fy) + (tex[y1, x0] * (1 - fx) + tex[y1, x1] * fx) * fy


def kimono(row, ys, EL, ER):
    iid, name, base, obi, cord, pat, obiage, fuki, silk = row
    base_c, obi_c, cord_c = rgb(base), rgb(obi), rgb(cord)
    miko = iid == 'k_miko'
    # pattern texture
    P.set_size(TW, TH); tl = Image.new('RGBA', (TW * SS, TH * SS), (0, 0, 0, 0)); pat(ImageDraw.Draw(tl))
    tex = np.asarray(tl, np.float32) / 255
    h, w = CH * SS, CW * SS
    X = X0 + (np.arange(w)[None, :] + .5) / SS + np.zeros((h, 1)); Y = Y0 + (np.arange(h)[:, None] + .5) / SS + np.zeros((1, w))
    Lr = np.interp(Y, ys, EL); Rr = np.interp(Y, ys, ER); C = (Lr + Rr) / 2; Wd = (Rr - Lr) / 2 + 3
    dW = np.gradient(np.interp(Y[:, 0], ys, (ER - EL) / 2)) * SS                  # r'(y)
    u = np.clip((X - C) / Wd, -.995, .995); nz = np.sqrt(1 - u * u)
    # regions
    ytop = 183 + 15 * ((X - 192) / 64) ** 2                                # sloping shoulders
    inside = sstep(-.6, .6, np.minimum(X - (Lr - 5), (Rr + 5) - X)) * sstep(-.6, .6, Y - ytop)
    uc = np.clip((X - C) / (Wd + 5), -1, 1); yhem = 344 + 20 * uc ** 2 - 3 * np.cos(uc * 7)  # lap drape, soft scallop
    # V opening: lines NL→VP and NR→VP
    NL, NR, VP = (163, 178), (223, 178), (191, 257)
    def sd(p, q):  # signed distance to line p→q, positive to the right of travel
        dx, dy = q[0] - p[0], q[1] - p[1]; l = math.hypot(dx, dy); return ((X - p[0]) * dy - (Y - p[1]) * dx) / l
    dLv = -sd(NL, VP)     # >0 left/outside of left V line
    dRv = sd(NR, VP)      # >0 right/outside of right V line (negative inside V)
    inV = (dLv < 0) & (dRv < 0) & (Y < VP[1])
    vopen = sstep(-.5, .5, np.minimum(-dLv, -dRv)) * (Y < VP[1] + 1)
    # sleeves: inner edge = fraction of the half-width, bottoms rounded
    a = np.interp(Y, [196, 232, 270, 320, 356], [.8, .7, .64, .62, .66])
    xinL, xinR = C - a * Wd, C + a * Wd
    wL = np.clip((xinL - X) / np.maximum(xinL - (Lr - 5), 1), 0, 1); wR = np.clip((X - xinR) / np.maximum((Rr + 5) - xinR, 1), 0, 1)
    sbotL = 350 + 22 * np.sin(np.clip(wL, 0, 1) * math.pi / 2) ** .6; sbotR = 350 + 22 * np.sin(np.clip(wR, 0, 1) * math.pi / 2) ** .6
    slvL = sstep(-.6, .6, xinL - X) * sstep(-.6, .6, Y - 198) * sstep(-.6, .6, sbotL - Y) * (X < C)
    slvR = sstep(-.6, .6, X - xinR) * sstep(-.6, .6, Y - 198) * sstep(-.6, .6, sbotR - Y) * (X > C)
    slv = np.maximum(slvL, slvR)
    torso = sstep(-.6, .6, yhem - Y)
    # obi band (on a slightly wider cylinder, smile curves)
    uo = np.clip((X - C) / (Wd + 4), -.995, .995); nzo = np.sqrt(1 - uo * uo); sm = 7 * (1 - nzo)
    otop, obot = 262 - sm, 299 - sm
    obim = sstep(-.6, .6, Y - otop) * sstep(-.6, .6, obot - Y)
    # ── folds ──
    F = np.zeros_like(X)
    for sgn in (-1, 1):
        cx0 = 192
        F += seg_ridge(X, Y, (cx0 + sgn * 52, 206), (cx0 + sgn * 18, 256), 3.2, .9)
        F -= seg_ridge(X, Y, (cx0 + sgn * 58, 222), (cx0 + sgn * 26, 258), 2.6, .7)
        F += seg_ridge(X, Y, (cx0 + sgn * 44, 230), (cx0 + sgn * 34, 258), 2.2, .5)
    for p0, p1, ww, am in (((176, 302), (160, 348), 4, 1.), ((196, 303), (200, 350), 3.5, -.8), ((214, 302), (232, 352), 4, 1.),
                           ((232, 300), (262, 350), 3.5, -.7), ((156, 302), (132, 350), 3.5, -.6), ((246, 304), (270, 356), 3, .7)):
        F += seg_ridge(X, Y, p0, p1, ww, am)
    FS = np.zeros_like(X)                      # sleeve folds: long, nearly vertical
    for sgn, xin in ((-1, xinL), (1, xinR)):
        for k, (fr, am) in enumerate(((.25, .9), (.5, -.7), (.75, .8))):
            xs = xin + sgn * fr * np.abs(np.where(sgn < 0, xin - Lr, Rr - xin))
            FS += am * np.exp(-((X - xs - sgn * (Y - 300) * .05) / 3.4) ** 2) * sstep(210, 250, Y) * (np.sign(X - C) == sgn)
    if miko:                                   # hakama pleats
        F += np.where(Y > obot, .9 * np.sin((X - 150) / 7.5 * math.pi) * sstep(0, 12, Y - obot), 0)
    gy, gx = np.gradient(F, 1 / SS); sgy, sgx = np.gradient(FS, 1 / SS)
    # ── normals ──
    ny_t = -dW[:, None] * .9 * nz
    n = np.stack([u - gx * .6, ny_t - gy * .6, nz], -1)
    # belly: the lap bulges forward below the obi then turns under at the hem
    lap = sstep(300, 330, Y) * sstep(yhem + 2, yhem - 14, Y)
    n[..., 1] += np.where(Y > 300, (Y - 316) / 26, 0) * .8 * nz
    n[..., 1] -= sstep(250, 300, Y) * sstep(300, 262, Y) * .0
    # sleeve normals: own cylinder, turned sideways
    def sleeve_n(xin, side, wv):
        xs = np.clip(1 - 2 * wv, -.995, .995) * (-side)     # -1 outer .. +1 inner (in x direction)
        lnz = np.sqrt(1 - .8 * xs * xs); lnx = xs * .9
        phi = side * .55; nx = lnx * math.cos(phi) + lnz * math.sin(phi); nzz = -lnx * math.sin(phi) + lnz * math.cos(phi)
        return nx, nzz, xs
    snxL, snzL, xsL = sleeve_n(xinL, -1, wL); snxR, snzR, xsR = sleeve_n(xinR, 1, wR)
    snx = np.where(X < C, snxL, snxR); snz = np.where(X < C, snzL, snzR)
    sbot = np.where(X < C, sbotL, sbotR)
    sny = .15 + np.clip((Y - (sbot - 12)) / 12, 0, 1) ** 2 * 1.1 - sstep(215, 196, Y) * .8
    ns = np.stack([snx - sgx * .6, sny - sgy * .6, snz], -1)
    for arr in (n, ns): arr /= np.linalg.norm(arr, axis=-1, keepdims=True)
    no = np.stack([uo, -np.clip((Y - otop) / 4, 0, 1) ** 0 * 0 + np.where(Y - otop < 3, -.6, 0) + np.where(obot - Y < 3, .7, 0), nzo], -1)
    no /= np.linalg.norm(no, axis=-1, keepdims=True)

    def shade(nn, alb, spec_k, gloss, amb=.2):
        dif = np.clip((nn @ LIGHT + .12) / 1.12, 0, 1) * (.72 + .28 * np.clip(nn[..., 2], 0, 1))
        sp = np.clip(nn @ HALF, 0, 1) ** gloss * spec_k
        rim = (1 - nn[..., 2]) ** 3 * .08 * spec_k * 3
        col = alb * (amb * np.array([.82, .86, 1.]) + dif[..., None] * np.array([1.02, .97, .9]) * 1.0)
        return col + (sp + rim)[..., None] * (.55 + .45 * alb)

    spec_k, gloss = (.34, 14) if silk else (.07, 6)
    weave = P.fbm(w, h, 6 * SS, 3, seed=hash(iid) % 999, stretch=(1, 4 if silk else 1))
    weave = (1 + (weave - .5) * (.07 if silk else .13))[..., None]
    # torso albedo: base + pattern mapped on the curved surface
    R0 = 92; s_t = TW / 2 + np.arcsin(u) * R0 + F * 1.2; t_t = (Y - Y0) + 8 * (1 - nz) + 4 + gy * 0
    pt = sample(tex, s_t, t_t)
    alb_t = base_c * weave
    alb_t = alb_t * (1 - pt[..., 3:]) + pt[..., :3] * pt[..., 3:]
    if miko: alb_t = np.where((Y > obot)[..., None], rgb('#c02a22') * weave, alb_t)
    # sleeves albedo (own mapping)
    s_s = np.where(X < C, 40 + np.arcsin(xsL) * 26, 270 + np.arcsin(xsR) * 26) + FS * 1.2
    ps = sample(tex, s_s, Y - Y0 + 20)
    alb_s = base_c * .96 * weave; alb_s = alb_s * (1 - ps[..., 3:]) + ps[..., :3] * ps[..., 3:]
    col_t = shade(n, alb_t, spec_k, gloss); col_s = shade(ns, alb_s, spec_k, gloss)
    # AO / cast shadows on the torso
    ao = 1 - .55 * np.exp(-(Y - ytop) / 7)                                  # under the neck
    ao *= 1 - .22 * sstep(yhem - 9, yhem, Y)                                 # hem turns under
    ao *= 1 - .45 * np.exp(-np.clip(Y - obot, 0, None) / 3.2) * (Y > obot)   # below the obi
    ao *= 1 - .3 * np.exp(-np.clip(otop - Y, 0, None) / 2.5) * (Y < otop) * (Y > otop - 8)
    dsl = X - xinL; ao *= 1 - np.where((dsl > 0) & (Y > 200) & (Y < sbotL), .55 * np.exp(-dsl / 5.5), 0)        # left sleeve shadow (lit side)
    dsr = xinR - X; ao *= 1 - np.where((dsr > 0) & (Y > 200) & (Y < sbotR), .35 * np.exp(-dsr / 3), 0)
    ao *= 1 + np.clip(F, -1, 1)[...] * .2                                  # fold troughs
    col_t *= ao[..., None]
    col_s *= (1 - .5 * np.exp(-np.clip(Y - 198, 0, None) / 6))[..., None] * (1 + np.clip(FS, -1, 1) * .14)[..., None]
    # sleeve inner edge: thin highlight
    col_s += (np.exp(-(np.where(X < C, xinL - X, X - xinR)) ** 2 / 1.2) * .12)[..., None]
    # front panels: top (wearer's left, viewer's right) panel edge below the V, with shadow on the under panel
    ex = VP[0] + (Y - VP[1]) * -.2 - 3                                        # the edge drifts left as it goes down
    dpe = X - ex
    below_v = Y > VP[1] - 2
    col_t *= (1 - np.where(below_v & (dpe < 0) & (dpe > -9), .42 * np.exp(dpe / 2.8), 0))[..., None]
    col_t += (np.where(below_v & (dpe >= 0) & (dpe < 2), .10, 0))[..., None]
    # collar bands (eri) along the V; the top panel's collar continues below the V point
    def band(d, w0, w1, colr, extra=0):
        tb = np.clip((d - w0) / (w1 - w0), 0, 1)
        prof = np.sin(tb * math.pi) ** .6                                    # rounded band
        lit = .55 + .55 * prof + extra
        return (d >= w0) & (d < w1), colr * lit[..., None] + (prof ** 6 * .12 * (1 if silk else .4))[..., None]
    eri_c = base_c * (.88 if base_c.mean() > .3 else 1.25) + (0 if base_c.mean() > .3 else .03)
    jub_c = rgb('#c8281e') if miko else rgb('#f2ede2')
    mL_j, cL_j = band(dLv, 0, 4.5, jub_c * .92, -.05); mL_e, cL_e = band(dLv, 4.5, 13, eri_c)
    mR_j, cR_j = band(dRv, 0, 4.5, jub_c, 0); mR_e, cR_e = band(dRv, 4.5, 13, eri_c, .05)
    upper = Y < VP[1] + 1
    col = np.where(inside[..., None] > 0, col_t, 0)
    # left collar (under), then right collar (over): above VP both, below VP only the top panel's collar
    col = np.where((mL_j & upper & (dRv < 4.5))[..., None], cL_j, col); col = np.where((mL_e & upper & (dRv < 0))[..., None], cL_e, col)
    col *= (1 - np.where(upper & (dLv > 13) & (dLv < 19), .35 * np.exp(-(dLv - 13) / 2.5), 0))[..., None]
    rband = (dRv >= -99)
    col = np.where((mR_j & upper)[..., None], cR_j, col); col = np.where((mR_e & (Y < obot))[..., None], cR_e, col)
    col *= (1 - np.where((dRv > 13) & (dRv < 19) & (Y < otop), .3 * np.exp(-(dRv - 13) / 2.5), 0))[..., None]
    col *= (1 - np.where((dRv < 0) & (dRv > -5) & ~upper & (Y < otop), .45 * np.exp(dRv / 2), 0))[..., None]   # shadow of top collar on under panel
    col *= (1 - np.where(mL_e & upper & (dRv > -5) & (dRv < 4.5), .4, 0))[..., None]
    # obi
    ob = obi_c * (1 + .06 * np.sin((Y - otop) / 2.3 * math.pi) * (1 if not miko else 0))[..., None]
    ob = ob * (1 + (P.fbm(w, h, 3 * SS, 2, seed=7, stretch=(5, 1)) - .5) * .14)[..., None]
    if not miko and obiage is not None:                                      # brocade stripe of the cord colour
        ob = np.where((np.abs(Y - (otop + 6)) < 1.1)[..., None] | (np.abs(Y - (obot - 6)) < 1.1)[..., None], cord_c * .9, ob)
    col_o = shade(no, ob, .45 if silk else .12, 18)
    col_o *= (1 - .55 * (np.abs(uo) ** 2.2))[..., None]
    col = np.where(obim[..., None] > .5, col_o, col)
    # obiage: soft scrunched cloth above the obi inside the V
    if obiage is not None:
        oa_top = otop - 5 - 1.5 * np.sin((X - 150) / 5.3)
        oam = (Y > oa_top) & (Y < otop + .5) & (np.abs(X - 191) < 24 - (otop - Y) * 1.2)
        wr = .8 + .25 * np.sin((X - 180) / 2.6 + np.sin(Y / 3)) + .15 * (Y - oa_top) / 5
        col = np.where(oam[..., None], rgb(obiage) * wr[..., None] * (.75 + .3 * nzo)[..., None], col)
    # obijime cord + knot
    yc = (otop + obot) / 2 + 1; dc = Y - yc; rC = 1.9
    cm = (np.abs(dc) < rC) & (obim > .5)
    tw = .78 + .22 * np.sin((X * 1.6 + Y * 2.2) / 1.3)
    ccol = cord_c * (tw * (.55 + .6 * np.sqrt(np.clip(1 - (dc / rC) ** 2, 0, 1))) * (.7 + .4 * nzo) - .12 * (dc > .5))[..., None] + (np.exp(-((dc + .8) / .6) ** 2) * .25)[..., None]
    col = np.where(cm[..., None], ccol, col)
    col *= (1 - np.where((dc > rC) & (dc < rC + 2.5) & (obim > .5), .35, 0))[..., None]
    for kx, ky, rx, ry, ang in ((186, 0, 7, 5, .5), (197, 0, 7, 5, -.5), (191.5, .5, 4.5, 4, 0)):
        ca, sa = math.cos(ang), math.sin(ang); qx = X - kx; qy = Y - (yc[:, :] * 0 + np.interp(kx, X[0], yc[0]) + ky)
        ex_, ey_ = (qx * ca + qy * sa) / rx, (-qx * sa + qy * ca) / ry; r2 = ex_ ** 2 + ey_ ** 2
        km = r2 < 1; kn = np.sqrt(np.clip(1 - r2, 0, 1))
        kl = np.clip(-.5 * ex_ - .6 * ey_ + .7 * kn, 0, 1)
        kc = cord_c * (.35 + .75 * kl)[..., None] + (kl ** 12 * .35)[..., None]
        col = np.where(km[..., None], kc, col)
        col *= (1 - np.where((r2 >= 1) & (r2 < 1.5), .3 * (1.5 - r2) * 2, 0))[..., None]
    # sleeves over everything else (they hang in front of the obi ends)
    col = col * (1 - slv[..., None]) + col_s * slv[..., None]
    # hem: padded edge (fuki) with lining, rounded highlight above it
    fc = rgb(fuki) if fuki else base_c * .8
    lowest = np.where(slv > .5, sbot, yhem)
    dh = lowest - Y
    col = np.where(((dh >= 0) & (dh < 2.2))[..., None], fc * (.55 + .35 * (1 - np.abs(u))[..., None]), col)
    col += (np.where((dh >= 2.2) & (dh < 4.5), .08 * np.sin((dh - 2.2) / 2.3 * math.pi), 0))[..., None]
    # alpha: cloth + contact shadows on the fur
    cloth = inside * np.maximum(torso * (1 - vopen), slv * (Y > 198)) * (1 - 0)
    cloth = np.clip(cloth, 0, 1)
    shadow_hem = np.where((Y > lowest) & (inside > 0), .5 * np.exp(-(Y - lowest) / 3.2), 0)
    shadow_v = np.where(inV, .45 * np.exp(-np.minimum(-dLv, -dRv) / 3.0) + .25 * np.exp(-(Y - 176) / 10), 0)
    sh_a = np.clip(np.maximum(shadow_hem, shadow_v), 0, 1) * (1 - cloth)
    alpha = cloth + sh_a
    rgbv = np.where(cloth[..., None] > 0, col, 0) * (cloth / np.maximum(alpha, 1e-4))[..., None]
    out = np.dstack([np.clip(rgbv, 0, 1) * 255, np.clip(alpha, 0, 1) * 255]).astype(np.uint8)
    img = Image.fromarray(out, 'RGBA').resize((CW, CH), Image.LANCZOS)
    print(iid); return iid, name, img


def build(only=None):
    ys, EL, ER = body_edges()
    rows = [r for r in KIMONO if not only or r[0] in only]
    return [kimono(r, ys, EL, ER) for r in rows]


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[3].split(',') if len(sys.argv) > 3 else None
    IMGS = build(only)
    if len(sys.argv) > 2 and sys.argv[2] == 'preview':
        for iid, _, im in IMGS: im.save(f'{OUT}/kimono3d_{iid}.png')
        sys.exit(0)
    cols = 4; at = Image.new('RGBA', (cols * (CW + 2), ((len(IMGS) + cols - 1) // cols) * (CH + 2)), (0, 0, 0, 0)); R = {}
    for i, (iid, name, im) in enumerate(IMGS):
        x, y = (i % cols) * (CW + 2), (i // cols) * (CH + 2); at.paste(im, (x, y)); R[iid] = [x, y, CW, CH]
    at.save(f'{OUT}/kimono.webp', 'WEBP', quality=88, alpha_quality=92, method=6)
    json.dump({'w': at.width, 'h': at.height, 'r': R, 'n': {iid: name for iid, name, _ in IMGS}, 'cell': [X0, Y0, CW, CH]}, open(f'{OUT}/kimono.json', 'w'), ensure_ascii=False)
