#!/usr/bin/env python3
"""Find Musya's eyes on every animation frame (template matching, numpy FFT), so accessories follow head turns and tilts.
Output: eyes.json {strip: [[lx,ly,rx,ry,score] | null] * 8} in 384x416 frame pixels."""
import json, math, sys
import numpy as np
from PIL import Image
STRIPS = ["rest","moveRight","moveLeft","sleep","play","purr","yarn","treat","highfive","stretch","groom","knead","house","butterfly","box","gift","hide","sulk","gaze9","gaze10"]
def frame(st, f):
    im = Image.open(f'assets/{st}@2x.webp').convert('RGBA').crop((f * 384, 0, f * 384 + 384, 416))
    a = np.asarray(im, np.float32); g = (a[..., :3] * [.3, .59, .11]).sum(-1); al = a[..., 3] / 255
    return g * al + 128 * (1 - al), al
REF = frame('rest', 0)[0]
TPL = {'L': REF[112:146, 146:186], 'R': REF[114:148, 203:243]}
def rot_scale(t, ang, sc):
    im = Image.fromarray(t.astype(np.float32), 'F'); w, h = im.size
    im = im.resize((max(8, int(w * sc)), max(8, int(h * sc))), Image.BICUBIC).rotate(ang, Image.BICUBIC, expand=False, fillcolor=float(t.mean()))
    return np.asarray(im, np.float32)
def ncc(img, t):
    th, tw = t.shape; H, W = img.shape
    tz = t - t.mean(); tn = math.sqrt((tz ** 2).sum()) + 1e-6
    F = np.fft.rfft2(img, (H + th, W + tw)); T = np.fft.rfft2(tz[::-1, ::-1], (H + th, W + tw))
    num = np.fft.irfft2(F * T, (H + th, W + tw))[th - 1:H, tw - 1:W]
    c1 = np.pad(img, ((1, 0), (1, 0))).cumsum(0).cumsum(1); c2 = np.pad(img ** 2, ((1, 0), (1, 0))).cumsum(0).cumsum(1)
    s1 = c1[th:, tw:] - c1[:-th, tw:] - c1[th:, :-tw] + c1[:-th, :-tw]; s2 = c2[th:, tw:] - c2[:-th, tw:] - c2[th:, :-tw] + c2[:-th, :-tw]
    var = np.maximum(s2 - s1 ** 2 / (th * tw), 1e-3)
    return num / (np.sqrt(var) * tn)
VARS = {k: [(a, s, rot_scale(t, a, s)) for a in range(-35, 36, 7) for s in (.75, .85, .95, 1.05, 1.15, 1.25)] for k, t in TPL.items()}
def best(img, key):
    out = []
    for a, s, t in VARS[key]:
        m = ncc(img, t); th, tw = t.shape
        for _ in range(3):     # a few peaks per variant
            i = int(m.argmax()); y, x = divmod(i, m.shape[1]); v = float(m[y, x])
            out.append((v, x + tw / 2, y + th / 2, a, s)); m[max(0, y - 8):y + 8, max(0, x - 8):x + 8] = -1
    return out
res = {}
for st in STRIPS:
    res[st] = []
    for f in range(8):
        g, al = frame(st, f)
        L = best(g, 'L'); R = best(g, 'R'); pick = None
        for vl, lx, ly, la, ls in sorted(L, reverse=True)[:40]:
            for vr, rx, ry, ra, rs in sorted(R, reverse=True)[:40]:
                dx, dy = rx - lx, ry - ly; dist = math.hypot(dx, dy); ang = math.degrees(math.atan2(dy, dx))
                if not (30 < dist < 85) or abs(ang) > 40 or abs(la - ra) > 15: continue
                sc = vl + vr - abs(ls - rs) * .3
                if pick is None or sc > pick[0]: pick = (sc, lx, ly, rx, ry, vl, vr)
        if pick and min(pick[5], pick[6]) > .42: res[st].append([round(pick[1], 1), round(pick[2], 1), round(pick[3], 1), round(pick[4], 1), round(min(pick[5], pick[6]), 2)])
        else: res[st].append(None)
    print(st, [('%.2f' % r[4]) if r else '-' for r in res[st]], flush=True)
json.dump(res, open('art/wear/eyes.json', 'w'))
