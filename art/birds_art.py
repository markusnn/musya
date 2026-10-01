#!/usr/bin/env python3
"""Add-on art «Кормушка для птиц»: 12 painted birds of Japan (sit / peck / fly), a wooden feeder on a post,
a heap of seeds, a mandarin slice and 5 bird things (feathers, a clay whistle) — packed into two atlases.
Usage: cd art && python3 birds_art.py ../assets/items  →  atlas_bi.webp (birds) + atlas_bi2.webp (feeder, items);
the rect maps are printed as JSON (pasted into feat/birds.js). Previews → art/out/bi_*.png"""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from paint import fbm

OUT = sys.argv[1] if len(sys.argv) > 1 else '../assets/items'
SS = 2                      # supersampling
PXCM = 7.0                  # sprite px per cm of a real bird (≈1.25 sprite px per image px in the game)
LIGHT = np.array([-.5, -.7, .6]); LIGHT /= np.linalg.norm(LIGHT)
D2R = math.pi / 180


def C(h): h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32)


class Cv:
    """float RGB + alpha canvas with soft-mask painting"""
    def __init__(s, w, h):
        s.w, s.h = w, h; s.rgb = np.zeros((h, w, 3), np.float32); s.a = np.zeros((h, w), np.float32)
        s.yy, s.xx = np.mgrid[0:h, 0:w].astype(np.float32)

    def put(s, m, col):
        m = np.clip(m, 0, 1)[..., None]; col = np.broadcast_to(col, s.rgb.shape) if np.ndim(col) == 1 else col
        s.rgb = s.rgb * (1 - m) + col * m; s.a = s.a + m[..., 0] * (1 - s.a)

    def loc(s, cx, cy, ang):
        c, si = math.cos(ang), math.sin(ang); dx, dy = s.xx - cx, s.yy - cy
        return dx * c + dy * si, -dx * si + dy * c

    def ell(s, cx, cy, rx, ry, ang=0., soft=1.2):
        u, v = s.loc(cx, cy, ang); q = np.sqrt((u / rx) ** 2 + (v / ry) ** 2)
        return np.clip((1 - q) * min(rx, ry) / soft + .5, 0, 1)

    def poly(s, pts, blur=.8):
        im = Image.new('L', (s.w, s.h)); ImageDraw.Draw(im).polygon([(float(x), float(y)) for x, y in pts], fill=255)
        if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
        return np.asarray(im, np.float32) / 255

    def line(s, pts, wd, blur=.6):
        im = Image.new('L', (s.w, s.h)); d = ImageDraw.Draw(im)
        d.line([(float(x), float(y)) for x, y in pts], fill=255, width=max(1, int(wd)), joint='curve')
        for x, y in (pts[0], pts[-1]): d.ellipse([x - wd / 2, y - wd / 2, x + wd / 2, y + wd / 2], fill=255)
        if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
        return np.asarray(im, np.float32) / 255


def blur(m, r):
    return np.asarray(Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)), np.float32) / 255


def light(m, sig, k=1.6, amb=.5, dif=.72, spec=.12):
    """dome shading of a soft mask: blurred mask as height → normal → lambert + a little gloss"""
    h = blur(m, sig) * sig * k; gy, gx = np.gradient(h)
    n = np.dstack([-gx, -gy, np.ones_like(gx)]); n /= np.linalg.norm(n, axis=2, keepdims=True)
    lam = np.clip((n * LIGHT).sum(2), 0, 1); sp = np.clip((n * np.array([-.25, -.45, .86])).sum(2), 0, 1) ** 18 * spec
    return amb + dif * lam, sp


def smooth(a, b, x): t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)


# ── species: sizes in cm-ish units, colours, marks. All face right.
SPEC = {
 'suzume': dict(B=4.6, fat=1.05, hr=.47, tl=.95, tw=.3, lg=.42, beak='cone', bl=.42, back='#8b5b36', belly='#d2c8b6', crown='#7c3d20', face='#ede7da',
                wing='#7e5434', edge='#d6b88c', tailc='#5f4630', beakc='#2b2622', legc='#b49a86', streak='#2a1c12', bar='#efe6d2',
                head=[(.0, .2, .3, .26, '#ede7da'), (-.12, .2, .16, .13, '#1d1a17'), (.38, .62, .34, .3, '#1e1b18')], seed=1),
 'mejiro': dict(B=3.9, fat=1.0, hr=.48, tl=.85, tw=.26, lg=.4, beak='thin', bl=.62, back='#7d8f3a', belly='#d9d6c6', crown='#8a9a3c', face='#8a9a3c',
                wing='#6c7c34', edge='#a8b45c', tailc='#56622c', beakc='#2a2a26', legc='#5a5e66', flank='#b8a88a',
                head=[(.42, .62, .42, .32, '#e8cf3a'), (.62, .3, .3, .22, '#e8cf3a')], ring='#f6f4ec', seed=2),
 'uguisu': dict(B=4.4, fat=.9, hr=.44, tl=1.15, tw=.26, lg=.5, beak='thin', bl=.6, back='#7a7448', belly='#cfcbb8', crown='#787246', face='#a9a27a',
                wing='#6e683e', edge='#9c9464', tailc='#625c38', beakc='#4a3e30', legc='#c8a890', supc='#ddd6b6', stripe='#4a4430', seed=3),
 'tsubame': dict(B=4.7, fat=.85, hr=.44, tl=1.9, tw=.22, fork=1, lg=.16, beak='flat', bl=.32, back='#1c2240', belly='#f0ece2', crown='#1c2240', face='#1c2240',
                 wing='#191d32', edge='#2c3460', tailc='#171b2e', beakc='#141414', legc='#2a2a2a', wlong=1.9, sheen='#3a58a8',
                 head=[(.55, .5, .45, .34, '#a83a2a'), (.82, -.28, .2, .16, '#a83a2a')], band='#151a30', seed=4),
 'hiyodori': dict(B=6.6, fat=.85, hr=.42, tl=1.55, tw=.3, lg=.42, beak='thin', bl=.62, back='#6a6e74', belly='#9ea0a2', crown='#5c6066', face='#7a7d82',
                  wing='#5a5d62', edge='#7c8086', tailc='#4e5156', beakc='#1e1e20', legc='#3a3a3c', crest=1, scale='#c8c8c6',
                  head=[(-.05, .18, .36, .26, '#7a4a32')], seed=5),
 'shijukara': dict(B=4.4, fat=1.0, hr=.48, tl=1.05, tw=.28, lg=.42, beak='cone', bl=.34, back='#7e8a88', belly='#e6e4dc', crown='#141414', face='#141414',
                   wing='#5e6668', edge='#9aa4a6', tailc='#4c5254', beakc='#1a1a1a', legc='#5a6068', bar='#f2f2ec', mantle='#9aa45a',
                   head=[(-.02, .14, .4, .3, '#f4f3ee')], tie='#141414', seed=6),
 'kawasemi': dict(B=4.4, fat=1.05, hr=.56, tl=.55, tw=.3, lg=.2, beak='dagger', bl=1.25, back='#2e8aa8', belly='#d8783a', crown='#1e6a8c', face='#1e6a8c',
                  wing='#2a6e86', edge='#4cb4cc', tailc='#1c5a7a', beakc='#1a1614', legc='#d84a2e', spots='#7fd0e0', stripe2='#4fd4e8',
                  head=[(.05, .1, .34, .2, '#d8783a'), (.0, .55, .3, .24, '#f2f0e6'), (-.55, .4, .2, .18, '#f2f0e6')], seed=7),
 'yamagara': dict(B=4.5, fat=1.0, hr=.5, tl=1.0, tw=.28, lg=.42, beak='cone', bl=.38, back='#6c7480', belly='#b8642e', crown='#141414', face='#ead8b0',
                  wing='#5c6470', edge='#8a929c', tailc='#4c5460', beakc='#1a1a1a', legc='#5a6068',
                  head=[(.4, .62, .4, .3, '#141414'), (-.62, -.1, .22, .3, '#ead8b0')], seed=8),
 'tsugumi': dict(B=7.0, fat=.95, hr=.42, tl=1.15, tw=.32, lg=.62, beak='thin', bl=.6, back='#4a3a2c', belly='#ece6da', crown='#2e241c', face='#2e241c',
                 wing='#a0502a', edge='#c87a44', tailc='#3a2e24', beakc='#2a2420', legc='#9a7a68', supc='#efe8d8', spotc='#1e1814',
                 head=[(.4, .6, .4, .28, '#efe8d8')], seed=9),
 'kijibato': dict(B=9.6, fat=1.08, hr=.34, tl=1.0, tw=.36, lg=.34, beak='dove', bl=.5, back='#7a6458', belly='#b89a90', crown='#8a8490', face='#a8909a',
                  wing='#5e4636', edge='#c8783e', tailc='#4c4a52', beakc='#4a3c3e', legc='#c05a5a', scalloped=1, tailtip='#c8c4c0',
                  neck=1, seed=10),
 'karasu': dict(B=13.0, fat=.95, hr=.44, tl=.85, tw=.36, lg=.5, beak='crow', bl=1.0, back='#17171c', belly='#1a1a20', crown='#141418', face='#161619',
                wing='#141418', edge='#2a2e3e', tailc='#121216', beakc='#0e0e10', legc='#141416', sheen='#3c4a7a', seed=11),
 'fukuro': dict(B=11.5, fat=1.2, hr=.72, tl=.5, tw=.4, lg=.18, beak='hook', bl=.22, back='#7a6e60', belly='#c4b8a4', crown='#766a5a', face='#cdc2ae',
                wing='#5e5446', edge='#b4a690', tailc='#6a5e50', beakc='#d8c88a', legc='#c8bca8', owl=1, spotc='#5a4a3a', seed=12),
}
NAMES = list(SPEC)


def plumage_noise(w, h, seed):
    return fbm(w, h, 10 * SS, 4, seed), fbm(w, h, 2.5 * SS, 2, seed + 50)


def bird(name, pose):
    P = SPEC[name]; B = P['B'] * PXCM * SS * (.62 if P.get('owl') else 1); r = P['hr'] * B
    owl = P.get('owl'); W = int(B * (6.2 if pose == 'fly' else 4.4)) + 8; Hh = int(B * (5.2 if pose == 'fly' else 3.6 if not owl else 4.6)) + 8
    cv = Cv(W, Hh); xx, yy = cv.xx, cv.yy; rs = np.random.default_rng(P['seed'] * 10 + len(pose))
    big, fine = plumage_noise(W, Hh, P['seed'])
    # pose geometry (world, y down): body angle, head offset (in B), beak direction, tail drop
    if owl:
        th = -86 * D2R; head = (.02, -1.02); hd = 0.; tdrop = 4; blink = pose == 'peck'
    elif pose == 'sit': th = -24 * D2R; head = (.74, -.74); hd = -4 * D2R; tdrop = 18
    elif pose == 'peck': th = 26 * D2R; head = (.98, .12); hd = 58 * D2R; tdrop = -6
    else: th = -6 * D2R; head = (.98, -.34); hd = -4 * D2R; tdrop = 4
    if name == 'kawasemi' and pose == 'sit': th = -40 * D2R; head = (.6, -.86)
    if name == 'kijibato' and pose == 'sit': head = (.86, -.6)
    if name == 'tsubame' and pose == 'sit': th = -12 * D2R; head = (.86, -.56)
    a, b = B, B * .62 * P['fat']
    ey = math.sqrt((a * math.sin(th)) ** 2 + (b * math.cos(th)) ** 2)
    lg = P['lg'] * B
    if pose == 'fly': cx, cy = W * .5, Hh * .64
    else: cx, cy = W * .52, Hh - 4 * SS - ey - lg * .8
    if owl: cx = W * .5
    ct, st = math.cos(th), math.sin(th)
    def bw(u, v): return cx + (u * ct - v * st) * B, cy + (u * st + v * ct) * B          # body-local (B units) → world
    hx, hy = cx + head[0] * B, cy + head[1] * B
    if owl: hy = cy - ey * .78 - r * .55
    back, belly, wingc, edge = C(P['back']), C(P['belly']), C(P['wing']), C(P['edge'])

    def tex(col, k=.22, kf=.1):
        return col * (1 - k / 2 + k * big[..., None]) * (1 - kf / 2 + kf * fine[..., None])

    # ── far wing (flying) behind everything
    def fly_wing(dx, dy, sc, dark):
        sx, sy = bw(.12, -.28); sx += dx * B; sy += dy * B
        wx, wy = sx - .25 * B * sc, sy - 1.0 * B * sc                       # wrist
        arm = cv.poly([(sx + .32 * B, sy + .12 * B), (sx - .1 * B, sy - .55 * B * sc), (wx + .18 * B, wy), (wx - .12 * B, wy + .08 * B), (sx - .7 * B * sc, sy - .1 * B * sc), (sx - .3 * B, sy + .2 * B)], 1.2)
        col = tex(wingc * dark); m = arm.copy(); cv.put(arm, col)
        for i in range(7):          # primaries fan, fingers
            ang = (-118 - i * 10) * D2R; L = (1.25 - abs(i - 2) * .06) * B * sc * (1.15 if P.get('wlong') else 1)
            fx, fy = wx + math.cos(ang) * L * .5, wy + math.sin(ang) * L * .5
            f = cv.ell(fx, fy, L * .52, B * .11 * sc, ang, 1.5); c2 = wingc * dark * (.84 + .05 * i)
            cv.put(f, tex(c2)); cv.put(np.clip(f - cv.ell(fx + 1, fy + 1, L * .48, B * .07 * sc, ang, 1.5), 0, 1) * .5, edge * dark); m = np.maximum(m, f)
        for i in range(6):          # secondaries along the trailing edge
            t = i / 5; px_, py_ = sx - .66 * B * sc + (wx - sx + .5 * B * sc) * t * .55, sy - .05 * B - (sy - wy) * t * .5
            f = cv.ell(px_ - .18 * B, py_ + .05 * B, .32 * B * sc, .1 * B * sc, (-150 + t * 30) * D2R, 1.4)
            cv.put(f, tex(wingc * dark * .9)); cv.put(np.clip(f - cv.ell(px_ - .18 * B + 1, py_ + .05 * B + 1, .28 * B * sc, .07 * B * sc, (-150 + t * 30) * D2R), 0, 1) * .45, edge * dark)
        sh, sp = light(m, B * .12); cv.rgb = cv.rgb * np.where(m[..., None] > .02, (.75 + .3 * sh[..., None]), 1)
    if pose == 'fly': fly_wing(.3, -.12, .9, .62)

    # ── tail
    rx_, ry_ = bw(-.86, .02); ta = th + math.pi + tdrop * D2R; tl = P['tl'] * B; tw = P['tw'] * B
    tx, ty = rx_ + math.cos(ta) * tl, ry_ + math.sin(ta) * tl; nx, ny = -math.sin(ta), math.cos(ta)
    spread = 1.6 if pose == 'fly' else 1
    mx, my = rx_ + math.cos(ta) * tl * .5, ry_ + math.sin(ta) * tl * .5
    if P.get('fork'):
        pts = [(rx_ + nx * tw, ry_ + ny * tw), (tx + nx * tw * 1.4 * spread, ty + ny * tw * 1.4 * spread), (rx_ + math.cos(ta) * tl * .45, ry_ + math.sin(ta) * tl * .45),
               (tx - nx * tw * 1.1 * spread, ty - ny * tw * 1.1 * spread), (rx_ - nx * tw, ry_ - ny * tw)]
        tm = cv.poly(pts, 1.2)
    else:
        tm = cv.ell(mx, my, tl * .56, tw * .95 * spread, ta, 1.4)
        tm = np.maximum(tm, cv.ell(mx + math.cos(ta) * tl * .18, my + math.sin(ta) * tl * .18, tl * .36, tw * 1.05 * spread, ta, 1.4))
    tc = tex(C(P['tailc']))
    u, v = cv.loc(rx_, ry_, ta); tc = tc * (1 - .16 * (np.sin(v / (tw * .3) * math.pi) > .65)[..., None]) * (1 - .25 * smooth(tl * .3, tl, u))[..., None]   # feather lines, darker tip
    if P.get('tailtip'): tc = np.where((u > tl * .78)[..., None], tex(C(P['tailtip'])), tc)
    sh, sp = light(tm, B * .1); cv.put(tm, tc * sh[..., None] + sp[..., None] * 255)

    # ── legs
    if pose != 'fly':
        fy0 = Hh - 4 * SS; lc = C(P['legc'])
        for k, dxl in enumerate((-.08, .14)):
            lx = cx + dxl * B; top = cy + ey * .55
            wd = max(2, B * (.13 if owl else .065))
            lm = cv.line([(lx, top), (lx + B * .02, fy0 - B * .04)], wd)
            lm = np.maximum(lm, cv.line([(lx - B * .14, fy0 - wd * .4), (lx + B * .22, fy0 - wd * .4)], wd * .8))
            cv.put(lm, lc * (.75 + .25 * k))

    # ── body + head (one shaded volume)
    bm = cv.ell(cx, cy, a, b, th, 1.5)
    hm = cv.ell(hx, hy, r * (1.0 if not owl else 1.02), r * (1.0 if not owl else .9), 0, 1.5)
    if P.get('crest'): hm = np.maximum(hm, cv.poly([(hx - r * .9, hy - r * .1), (hx - r * .55, hy - r * 1.3), (hx + r * .3, hy - r * .85), (hx + r * .6, hy - r * .3)], 1.5))
    neck = cv.poly([(*bw(.2, -.55),), (hx - r * .6, hy + r * .2), (hx + r * .5, hy + r * .6), (*bw(.75, .1),)], 2) if not owl else 0 * bm
    um = np.maximum(np.maximum(bm, hm), neck)
    u, v = cv.loc(cx, cy, th); u /= B; v /= B
    t_low = smooth(-.12, .3, v)
    col = tex(back) * (1 - t_low[..., None]) + tex(belly, .14) * t_low[..., None]
    if P.get('flank') is not None: col = np.where(((v > .05) & (u < .2))[..., None], col * .6 + tex(C(P['flank'])) * .4, col)
    if P.get('mantle'): mm = cv.ell(*bw(.15, -.42), B * .38, B * .2, th, 3); col = col * (1 - mm[..., None] * .7) + tex(C(P['mantle'])) * mm[..., None] * .7
    if P.get('streak'):                     # sparrow back streaks
        s_ = (np.sin(v * 38 + big * 9) > .55) & (v < -.05) & (u > -.7) & (u < .45); col = np.where(s_[..., None], col * .5 + C(P['streak']) * .5, col)
    if P.get('scale'):                      # bulbul: pale scaling on the breast
        s_ = (np.sin(u * 30 + np.sin(v * 20) * 2) * np.sin(v * 30) > .55) & (v > 0); col = np.where(s_[..., None], col * .7 + C(P['scale']) * .3, col)
    if P.get('spotc') and not owl:          # thrush: black breast band and flank spots
        band = cv.ell(*bw(.55, .18), B * .34, B * .3, th, 4); s_ = (fine > .45) & (np.sin(u * 22) * np.sin(v * 26) > .2) & (v > .08)
        col = col * (1 - band[..., None] * .8) + C(P['spotc']) * band[..., None] * .8; col = np.where(s_[..., None], col * .35 + C(P['spotc']) * .65, col)
    if owl:                                 # owl: vertical streaks on the pale breast, mottled back
        s_ = (np.sin(xx / (B * .09) + big * 6) > .78) & (yy > cy - b * .2) & (fine > .3); col = np.where(s_[..., None], col * .45 + C(P['spotc']) * .55, col)
        s2 = (fine > .62) & (yy < cy); col = np.where(s2[..., None], col * .8 + C('#e8e0d0') * .2, col)
    if P.get('tie'):
        tm_ = cv.poly([(*bw(.62, -.05),), (*bw(.82, .05),), (*bw(-.1, .62),), (*bw(-.3, .5),)], 3); col = col * (1 - tm_[..., None]) + C(P['tie']) * tm_[..., None]
    if P.get('sheen'): col = col + C(P['sheen']) * (np.clip(big - .45, 0, 1) * .55 * (1 - t_low * .5))[..., None]
    # head colours (head-local: u along the beak, v down; r units)
    hu, hv = cv.loc(hx, hy, hd); hu /= r; hv /= r
    hcol = tex(C(P['face']), .12); cap = smooth(-.05, -.35, hv)
    if not owl: hcol = hcol * (1 - cap[..., None]) + tex(C(P['crown']), .12) * cap[..., None]
    for (mu, mv, mru, mrv, mc) in P.get('head', []):
        mk = cv.ell(hx + (mu * math.cos(hd) - mv * math.sin(hd)) * r, hy + (mu * math.sin(hd) + mv * math.cos(hd)) * r, mru * r, mrv * r, hd, 2.2)
        hcol = hcol * (1 - mk[..., None]) + tex(C(mc), .1) * mk[..., None]
    if P.get('supc'):
        mk = cv.ell(hx + math.cos(hd) * r * .05 - math.sin(hd) * -.3 * r, hy + math.sin(hd) * r * .05 + math.cos(hd) * -.3 * r, r * .62, r * .09, hd - .12, 1.6)
        hcol = hcol * (1 - mk[..., None]) + C(P['supc']) * mk[..., None]
    if P.get('stripe'):
        mk = cv.ell(hx + math.cos(hd) * r * .1 - math.sin(hd) * -.12 * r, hy + math.sin(hd) * r * .1 + math.cos(hd) * -.12 * r, r * .6, r * .06, hd - .08, 1.4)
        hcol = hcol * (1 - mk[..., None] * .8) + C(P['stripe']) * mk[..., None] * .8
    if P.get('stripe2'):        # kingfisher: barred crown
        s_ = (np.sin(hu * 24) > .5) & (hv < -.25); hcol = np.where(s_[..., None], hcol * .55 + C(P['stripe2']) * .45, hcol)
    if owl:
        disc = cv.ell(hx, hy + r * .08, r * .84, r * .72, 0, 2.5); rim = np.clip(disc - cv.ell(hx, hy + r * .08, r * .74, r * .62, 0, 2.5), 0, 1)
        hcol = hcol * (1 - disc[..., None]) + tex(C(P['face']), .16) * disc[..., None]; hcol = hcol * (1 - rim[..., None] * .6) + C('#5a4a3a') * rim[..., None] * .6
        rings = (np.sin(np.sqrt((xx - hx) ** 2 + (yy - hy - r * .1) ** 2) / (r * .06)) > .7) & (disc > .5); hcol = np.where(rings[..., None], hcol * .9, hcol)
    if P.get('neck'):           # turtle dove: striped neck patch
        nk = cv.ell(hx - r * .7, hy + r * 1.25, r * .5, r * .32, -.5, 2); s_ = np.sin((xx + yy) / (r * .12)) > 0
        col = col * (1 - nk[..., None]) + np.where(s_[..., None], C('#1e1c22'), C('#8a96aa')) * nk[..., None]
    hw_ = np.clip(hm * 1.2 - bm * .2, 0, 1) if not owl else hm
    fullc = col * (1 - hw_[..., None]) + hcol * hw_[..., None]
    if not owl: fullc = np.where((neck > .5)[..., None] & (hm < .5)[..., None], col, fullc)
    sh, sp = light(um, B * .32, k=1.3); cv.put(um, fullc * sh[..., None] + sp[..., None] * 255)

    # ── folded wing (sit / peck)
    if pose != 'fly':
        wl = P.get('wlong', 1.25 if not owl else 1.0)
        wcx, wcy = bw(-.1 if not owl else 0, -.1); wa = th + (5 * D2R if not owl else 0)
        if owl:     # owl: wing along the side of the upright body
            wcx, wcy = cx - a * .02, cy - b * .02; wa = th
        wm = cv.ell(wcx, wcy, B * .78, B * .42 * P['fat'], wa, 1.5)
        tip = bw(-wl, .14 if not owl else .3); wm = np.maximum(wm, cv.poly([bw(-.2, -.3), bw(-.35, .3), tip], 1.4))
        if owl: wm = wm * smooth(cy - b * .9, cy - b * .6, yy)
        wc = tex(wingc, .18); wu, wv = cv.loc(wcx, wcy, wa); wu /= B; wv /= B
        # feather rows: coverts scallops at the front, long primaries/tertials toward the tip
        for i in range(6):
            fx, fy = bw(-.55 - i * .1, .06 + i * .02); f = cv.ell(fx, fy, B * (.55 - i * .03), B * .1, wa - .05, 1.2)
            ring = np.clip(f - cv.ell(fx + 1.5, fy - B * .02, B * (.5 - i * .03), B * .07, wa - .05, 1.2), 0, 1) * .7
            wc = wc * (1 - f[..., None] * .35) + tex(wingc * (.82 + rs.uniform(-.05, .05))) * f[..., None] * .35
            wc = wc * (1 - ring[..., None] * .6 * wm[..., None]) + edge * (ring * .6 * wm)[..., None]
        for row, (u0, v0, n_, sz) in enumerate([(.25, -.18, 6, .15), (.05, .02, 7, .17)]):
            for j in range(n_):
                fx, fy = bw(u0 - j * .13 + rs.uniform(-.02, .02), v0 + row * .02 + rs.uniform(-.02, .02))
                f = cv.ell(fx, fy, B * sz, B * sz * .75, wa, 1.2); ring = np.clip(f - cv.ell(fx + 1.2, fy - B * sz * .12, B * sz * .82, B * sz * .6, wa, 1.2), 0, 1)
                fu, fv = cv.loc(fx, fy, wa); ring = ring * smooth(-.2, .5, fv / (B * sz))
                ec = edge * (1.15 if P.get('scalloped') else 1)
                wc = wc * (1 - ring[..., None] * (.6 if P.get('scalloped') else .5) * wm[..., None]) + ec * (ring * (.6 if P.get('scalloped') else .5) * wm)[..., None]
                if P.get('scalloped'): wc = wc * (1 - (f - ring)[..., None].clip(0, 1) * .12 * wm[..., None])
        if P.get('bar'):
            bm_ = cv.ell(*bw(-.02, .02), B * .5, B * .045, wa + .1, 1.2); wc = wc * (1 - bm_[..., None]) + C(P['bar']) * bm_[..., None]
        if P.get('spots'):
            s_ = (fine > .7) & (wu > -.2); wc = np.where(s_[..., None], wc * .4 + C(P['spots']) * .6, wc)
        # shadow cast by the wing on the body, then the wing
        so = blur(np.roll(np.roll(wm, int(B * .05), 0), int(B * .03), 1), B * .06) * um * (1 - wm)
        cv.rgb = cv.rgb * (1 - so[..., None] * .35)
        sh, sp = light(wm, B * .16, k=1.2); cv.put(wm, wc * sh[..., None] + sp[..., None] * 255)

    # ── beak
    bc = C(P['beakc']); kind = P['beak']; L = P['bl'] * r
    def hp(u_, v_): return hx + (u_ * math.cos(hd) - v_ * math.sin(hd)), hy + (u_ * math.sin(hd) + v_ * math.cos(hd))
    if not owl:
        bx0 = r * .82; half = {'cone': .3, 'thin': .14, 'flat': .22, 'dagger': .2, 'crow': .3, 'dove': .1}[kind] * r
        tipv = {'cone': .06, 'thin': .02, 'flat': .05, 'dagger': .06, 'crow': .14, 'dove': .06}[kind] * r
        top = [hp(bx0 - r * .12, -half), hp(bx0 + L * .55, -half * .55 - (r * .06 if kind == 'crow' else 0)), hp(bx0 + L, tipv)]
        bot = [hp(bx0 + L * .9, tipv + half * .12), hp(bx0 + L * .4, half * .7), hp(bx0 - r * .1, half)]
        bkm = cv.poly(top + bot, 1.0); sh, sp = light(bkm, max(2, half * .4), k=1.0, amb=.55)
        cv.put(bkm, bc * sh[..., None] + sp[..., None] * 380)
        cv.put(cv.line([hp(bx0 - r * .05, half * .12), hp(bx0 + L * .8, tipv * .9)], max(1.5, r * .04)) * .55 * bkm, bc * .3)
        if kind == 'dove': cv.put(cv.ell(*hp(bx0 + r * .05, -half * .5), r * .12, r * .08, hd, 1) * .7, C('#dcd0d4'))
        # eye
        ex, ey_ = hp(r * .34 if kind != 'dagger' else r * .3, -r * .14); er = r * (.11 if kind in ('crow', 'dove') else .135)
        if P.get('ring'): cv.put(cv.ell(ex, ey_, er * 1.9, er * 1.9, 0, 1.2), C(P['ring']))
        cv.put(cv.ell(ex, ey_, er, er, 0, 1.0), C('#140e0a') if name != 'kijibato' else C('#c86a28'))
        if name == 'kijibato': cv.put(cv.ell(ex, ey_, er * .55, er * .55, 0, 1), C('#140e0a'))
        cv.put(cv.ell(ex - er * .35, ey_ - er * .38, er * .3, er * .3, 0, .8) * .9, C('#f4f2ea'))
    else:       # owl face: two dark eyes, small hooked beak between
        for sx_ in (-1, 1):
            ex, ey_ = hx + sx_ * r * .34, hy + r * .02; er = r * .15
            if blink:
                cv.put(cv.line([(ex - er, ey_), (ex + er, ey_ + er * .2)], max(2, r * .05)), C('#2a2018'))
            else:
                cv.put(cv.ell(ex, ey_, er * 1.25, er * 1.25, 0, 1.2) * .5, C('#4a3c30')); cv.put(cv.ell(ex, ey_, er, er, 0, 1.0), C('#0e0a08'))
                cv.put(cv.ell(ex - er * .35, ey_ - er * .4, er * .28, er * .28, 0, .8), C('#f0ece4'))
        bkm = cv.poly([(hx - r * .09, hy + r * .14), (hx + r * .09, hy + r * .14), (hx + r * .02, hy + r * .42), (hx - r * .03, hy + r * .38)], 1.0)
        sh, sp = light(bkm, 3, k=1.0, amb=.6); cv.put(bkm, C(P['beakc']) * sh[..., None] + sp[..., None] * 200)

    if pose == 'fly': fly_wing(-.05, 0, 1.0, 1.0)
    # dark rim on the silhouette, film grain
    edge_m = np.clip(cv.a - blur(cv.a, 1.6 * SS) * 1.0, 0, 1) * 1.6
    cv.rgb = cv.rgb * (1 - np.clip(edge_m, 0, .45)[..., None])
    cv.rgb += np.random.default_rng(P['seed']).normal(0, 3.5, (Hh, W))[..., None]
    rgba = np.dstack([np.clip(cv.rgb, 0, 255), np.clip(cv.a, 0, 1) * 255]).astype(np.uint8)
    im = Image.fromarray(rgba, 'RGBA').resize((W // SS, Hh // SS), Image.LANCZOS)
    bb = im.getbbox(); im = im.crop(bb)
    if pose == 'fly': anc = (cx / SS - bb[0], cy / SS - bb[1])
    else: anc = (cx / SS - bb[0], (Hh - 4 * SS) / SS - bb[1])
    return im, [round(anc[0]), round(anc[1])]


# ── the feeder: a little gabled roof on a tray, on a square post (≈1.25 sprite px per image px)
def wood(cv, m, base, seed, vertical=True, k=.35):
    g = fbm(cv.w, cv.h, 3 * SS, 3, seed, (1, 14) if vertical else (14, 1)); g2 = fbm(cv.w, cv.h, 30 * SS, 3, seed + 1)
    col = C(base) * (1 - k / 2 + k * g[..., None]) * (.85 + .3 * g2[..., None])
    return col


def feeder():
    W, Hh = 300 * SS, 640 * SS; cv = Cv(W, Hh); cx = W / 2
    post_top, ty = 300 * SS, 300 * SS             # tray top line
    # post with a slight taper, a brace under the tray
    pm = cv.poly([(cx - 15 * SS, ty), (cx + 15 * SS, ty), (cx + 17 * SS, Hh - 6 * SS), (cx - 17 * SS, Hh - 6 * SS)])
    sh = .55 + .45 * smooth(cx + 16 * SS, cx - 16 * SS, cv.xx); cv.put(pm, wood(cv, pm, '#5a4430', 3) * sh[..., None])
    for s in (-1, 1):
        br = cv.poly([(cx + s * 13 * SS, ty + 70 * SS), (cx + s * 18 * SS, ty + 64 * SS), (cx + s * 70 * SS, ty + 26 * SS), (cx + s * 62 * SS, ty + 22 * SS)])
        cv.put(br, wood(cv, br, '#4e3b2a', 4, False) * .8)
    # moss and a weathered foot
    mo = cv.ell(cx, Hh - 14 * SS, 26 * SS, 10 * SS, 0, 3) * (fbm(W, Hh, 4 * SS, 3, 9) > .4); cv.put(mo * .9, C('#3c4a2c'))
    # tray: front face + far rim (seen a little from above) + dark inside
    tw = 112 * SS
    inside = cv.poly([(cx - tw + 8 * SS, ty - 12 * SS), (cx + tw - 8 * SS, ty - 12 * SS), (cx + tw, ty + 2 * SS), (cx - tw, ty + 2 * SS)])
    cv.put(inside, C('#2a2018') * (.8 + .3 * fbm(W, Hh, 6 * SS, 3, 5))[..., None])
    rim = cv.poly([(cx - tw + 8 * SS, ty - 16 * SS), (cx + tw - 8 * SS, ty - 16 * SS), (cx + tw - 8 * SS, ty - 11 * SS), (cx - tw + 8 * SS, ty - 11 * SS)]); cv.put(rim, C('#6e5640'))
    front = cv.poly([(cx - tw, ty), (cx + tw, ty), (cx + tw - 3 * SS, ty + 26 * SS), (cx - tw + 3 * SS, ty + 26 * SS)])
    fc = wood(cv, front, '#7a5e42', 6, False); fc = fc * (1 - .25 * smooth(ty, ty + 26 * SS, cv.yy))[..., None]
    cv.put(front, fc); cv.put(cv.line([(cx - tw, ty + 1 * SS), (cx + tw, ty + 1 * SS)], 3 * SS), C('#9a7c5a'))
    for s in (-1, 1):   # corner posts holding the roof
        p = cv.poly([(cx + s * (tw - 16 * SS) - 5 * SS, ty - 128 * SS), (cx + s * (tw - 16 * SS) + 5 * SS, ty - 128 * SS), (cx + s * (tw - 16 * SS) + 5 * SS, ty - 10 * SS), (cx + s * (tw - 16 * SS) - 5 * SS, ty - 10 * SS)])
        cv.put(p, wood(cv, p, '#5e4632', 7 + s) * (.75 if s > 0 else 1))
    # gabled roof of cedar shingles, front gable triangle
    ry0, rh, rw = ty - 196 * SS, 74 * SS, 146 * SS
    gab = cv.poly([(cx, ry0 + 6 * SS), (cx + rw * .78, ry0 + rh + 4 * SS), (cx - rw * .78, ry0 + rh + 4 * SS)]); cv.put(gab, wood(cv, gab, '#3e2e22', 11) * .8)
    for s in (-1, 1):
        sl = cv.poly([(cx, ry0 - 4 * SS), (cx + s * 8 * SS, ry0 - 6 * SS), (cx + s * rw, ry0 + rh), (cx + s * rw, ry0 + rh + 14 * SS), (cx + s * (rw - 10 * SS), ry0 + rh + 16 * SS), (cx, ry0 + 12 * SS)])
        u, v = cv.loc(cx, ry0, math.atan2(rh, s * rw)); rows = (np.mod(u / (16 * SS), 1) < .14)
        col = wood(cv, sl, '#4a3a2e', 12 + s, False, .5) * np.where(rows[..., None], .55, 1) * (.95 if s < 0 else .72)
        moss = (fbm(W, Hh, 7 * SS, 3, 20 + s) > .62) & (v < 10 * SS); col = np.where(moss[..., None], col * .5 + C('#4a5a34') * .5, col)
        cv.put(sl, col)
    cv.put(cv.line([(cx - rw, ry0 + rh + 1 * SS), (cx, ry0 - 4 * SS), (cx + rw, ry0 + rh + 1 * SS)], 4 * SS) * .7, C('#7c6650'))
    # a little nail on the post for the mandarin slice
    cv.put(cv.ell(cx + 16 * SS, ty + 80 * SS, 3 * SS, 3 * SS, 0, 1), C('#2a2a28'))
    e = np.clip(cv.a - blur(cv.a, 2 * SS), 0, 1) * 1.4; cv.rgb *= 1 - np.clip(e, 0, .4)[..., None]
    cv.rgb += np.random.default_rng(3).normal(0, 3, (Hh, W))[..., None]
    im = Image.fromarray(np.dstack([np.clip(cv.rgb, 0, 255), cv.a * 255]).astype(np.uint8), 'RGBA').resize((W // SS, Hh // SS), Image.LANCZOS)
    return im


def seeds():
    W, Hh = 214 * SS, 34 * SS; cv = Cv(W, Hh); rs = np.random.default_rng(4)
    heap = cv.poly([(4 * SS, Hh - 2 * SS)] + [(x, Hh - 4 * SS - (Hh - 10 * SS) * (1 - ((x - W / 2) / (W / 2 - 4 * SS)) ** 2) ** .7 * (.85 + .15 * math.sin(x * .05))) for x in np.linspace(6 * SS, W - 6 * SS, 30)] + [(W - 4 * SS, Hh - 2 * SS)], 2)
    cv.put(heap, C('#b89a62') * (.7 + .4 * fbm(W, Hh, 3 * SS, 3, 4))[..., None])
    for i in range(520):
        x, y = rs.uniform(8 * SS, W - 8 * SS), rs.uniform(2 * SS, Hh - 4 * SS)
        if heap[int(y), int(x)] < .5: continue
        c = C(['#e8dcb8', '#d8b868', '#c89a48', '#f0ead8', '#a87a40', '#3a2a1a'][rs.integers(0, 6)])
        g = cv.ell(x, y, rs.uniform(1.6, 2.8) * SS, rs.uniform(1.0, 1.6) * SS, rs.uniform(0, 3), .8); cv.put(g * .95, c * (.9 + .2 * (y < Hh / 2)))
    im = Image.fromarray(np.dstack([np.clip(cv.rgb, 0, 255), cv.a * 255]).astype(np.uint8), 'RGBA').resize((W // SS, Hh // SS), Image.LANCZOS)
    return im


def mikan():
    W, Hh = 56 * SS, 40 * SS; cv = Cv(W, Hh)
    m = cv.ell(W / 2, Hh * .55, 24 * SS, 16 * SS, 0, 1.5) * (cv.yy < Hh * .62 + 2 * SS)
    cv.put(m, C('#e8862a')); inner = cv.ell(W / 2, Hh * .58, 20 * SS, 12 * SS, 0, 1.5) * (cv.yy < Hh * .6)
    ang = np.arctan2(cv.yy - Hh * .6, cv.xx - W / 2); seg = (np.mod(ang * 9 / math.pi, 1) < .1)
    cv.put(inner, np.where(seg[..., None], C('#f6d8a0'), C('#f4a640'))); cv.put(cv.line([(W / 2 - 22 * SS, Hh * .6), (W / 2 + 22 * SS, Hh * .6)], 2.5 * SS), C('#f8e8c8'))
    return Image.fromarray(np.dstack([np.clip(cv.rgb, 0, 255), cv.a * 255]).astype(np.uint8), 'RGBA').resize((W // SS, Hh // SS), Image.LANCZOS)


def feather(base, edge, pattern, seed, length=190, width=40, curve=.12):
    W, Hh = int(width * 2.4) * SS, (length + 30) * SS; cv = Cv(W, Hh); x0 = W / 2; y0, y1 = 10 * SS, (length + 4) * SS
    def spine(t): return x0 + math.sin(t * math.pi * .9) * curve * length * SS * (t), y0 + (y1 - y0) * t
    rs = np.random.default_rng(seed); pts_l, pts_r = [], []
    for t in np.linspace(0, 1, 40):
        sx, sy = spine(t); wv = width * SS * (math.sin(min(1, t * 1.25) * math.pi) ** .55 if t < .8 else (1 - t) * 3.2 * .85) * (.5 if t > .86 else 1)
        pts_l.append((sx - wv * .45, sy + wv * .25)); pts_r.append((sx + wv * .55, sy + wv * .25))
    vm = cv.poly(pts_l + pts_r[::-1], 1.2)
    u = cv.yy / (Hh); barbs = np.sin((cv.yy + np.abs(cv.xx - x0) * 1.1) / (2.4 * SS)) > .3
    col = C(base) * np.where(barbs[..., None], .9, 1.05) * (.85 + .3 * fbm(W, Hh, 5 * SS, 3, seed))[..., None]
    if pattern == 'bars': col = np.where((np.sin(cv.yy / (11 * SS) + (cv.xx - x0) * .02) > .35)[..., None], col * .45 + C('#4a3826') * .55, col)
    if pattern == 'tip': col = np.where((cv.yy < y0 + 30 * SS)[..., None], C(edge), col)
    if pattern == 'grad': col = col * (1 - smooth(y0, y1, cv.yy) * .5)[..., None] + C(edge) * (smooth(y1 * .55, y1, cv.yy) * .5)[..., None]
    if pattern == 'gloss': col = col + C(edge) * (np.clip(fbm(W, Hh, 20 * SS, 2, seed + 3) - .4, 0, 1) * 1.2)[..., None]
    # ragged gaps in the vane
    gap = (np.abs(np.sin(cv.yy / (23 * SS) + rs.uniform(0, 6))) < .06) & (np.abs(cv.xx - x0) > 4 * SS); vm = vm * (1 - gap * .85)
    sh, sp = light(vm, 5 * SS, k=.8, amb=.6, dif=.5); cv.put(vm, col * sh[..., None] + sp[..., None] * 160)
    cv.put(cv.line([spine(t) for t in np.linspace(0, 1.06, 30)], 2.6 * SS), C('#e8e0cc') * .9)
    # a little dark wooden stand
    st = cv.poly([(x0 - 26 * SS, Hh - 4 * SS), (x0 + 26 * SS, Hh - 4 * SS), (x0 + 22 * SS, Hh - 22 * SS), (x0 - 22 * SS, Hh - 22 * SS)]); cv.put(st, C('#3a2a1e') * (.8 + .3 * smooth(Hh - 22 * SS, Hh - 4 * SS, cv.yy))[..., None])
    cv.put(cv.line([(x0 - 22 * SS, Hh - 21 * SS), (x0 + 22 * SS, Hh - 21 * SS)], 2 * SS), C('#6a5240'))
    im = Image.fromarray(np.dstack([np.clip(cv.rgb, 0, 255), cv.a * 255]).astype(np.uint8), 'RGBA').resize((W // SS, Hh // SS), Image.LANCZOS)
    return im.crop(im.getbbox())


def hatobue():
    """a glazed clay dove whistle (hato-bue) on a little cushion"""
    im, anc = bird('kijibato', 'sit')
    a = np.asarray(im, np.float32); lum = (a[..., :3] * [.3, .59, .11]).sum(-1)
    glaze = np.array([226, 218, 200], np.float32) * (.55 + .55 * lum[..., None] / 255)
    rs = np.random.default_rng(5); h, w = lum.shape
    for _ in range(14):     # painted red and green dabs
        x, y = rs.uniform(w * .2, w * .8), rs.uniform(h * .25, h * .75); c = np.array([[190, 52, 40], [60, 110, 70], [40, 60, 110]][rs.integers(0, 3)], np.float32)
        d = ((np.mgrid[0:h, 0:w][1] - x) ** 2 + (np.mgrid[0:h, 0:w][0] - y) ** 2) < (w * .035) ** 2; glaze[d] = c * (.7 + .5 * lum[d][..., None] / 255)
    a[..., :3] = glaze; out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')
    k = 120 / out.width; return out.resize((120, int(out.height * k)), Image.LANCZOS)


def pack(sprites, W):
    lst = sorted(sprites.items(), key=lambda kv: -kv[1][0].height); x = y = rowh = 0; pos = {}
    for k, (im, anc) in lst:
        if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
        pos[k] = (x, y); x += im.width + 2; rowh = max(rowh, im.height)
    at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
    for k, (im, anc) in lst: at.paste(im, pos[k])
    rect = {k: [pos[k][0], pos[k][1], im.width, im.height] + (anc or []) for k, (im, anc) in sprites.items()}
    return at, rect


if __name__ == '__main__':
    only = sys.argv[2:] or None
    os.makedirs('out', exist_ok=True)
    birds = {}
    for n in NAMES:
        for pose in ('sit', 'peck', 'fly'):
            if only and n not in only: continue
            birds[n + '_' + pose] = bird(n, pose)
    at, rb = pack(birds, 1180)
    if only: at.save('out/bi_test.png'); print(json.dumps(rb)); sys.exit()
    at.save(f'{OUT}/atlas_bi.webp', 'WEBP', quality=86, alpha_quality=88, method=6); at.save('out/bi_atlas.png')
    things = {'feeder': (feeder(), [150, 640]), 'seeds': (seeds(), None), 'mikan': (mikan(), None),
              'bi_f_kawa': (feather('#2a8ab0', '#e07a3a', 'grad', 1, 170, 34, .1), None),
              'bi_f_fuku': (feather('#c8b49a', '#4a3826', 'bars', 2, 200, 46, .08), None),
              'bi_f_kiji': (feather('#7a6a64', '#c87a44', 'tip', 3, 180, 40, .14), None),
              'bi_f_kara': (feather('#141418', '#3c4a8a', 'gloss', 4, 220, 44, .16), None),
              'bi_hatobue': (hatobue(), None)}
    at2, rt = pack(things, 760)
    at2.save(f'{OUT}/atlas_bi2.webp', 'WEBP', quality=86, alpha_quality=88, method=6); at2.save('out/bi_atlas2.png')
    print('atlas_bi', at.size, 'atlas_bi2', at2.size)
    print('BI_R=' + json.dumps(rb, separators=(',', ':')))
    print('BI_T=' + json.dumps(rt, separators=(',', ':')))
