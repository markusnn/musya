#!/usr/bin/env python3
"""Movable props: objects that used to be baked into the scenery, rendered as separate sprites.
Output: <out>/<id>.webp and props.json [{id, room, n, x, y, w, h, d, v}] where (x, y) is the bottom-centre in scene px."""
import json, sys
import numpy as np
from PIL import Image, ImageDraw
import paint as P
from paint import *
from layers import grade_rgba, darken_rgba

OUT = sys.argv[1]
META = []
GRADE = {
    'engawa': dict(lift=(8, 11, 10), sat=0.72, gamma=1.08), 'kitchen': dict(lift=(10, 8, 6), sat=0.8, gamma=1.05),
    'onsen': dict(lift=(9, 12, 11), sat=0.72, gamma=1.08), 'games': dict(lift=(9, 12, 11), sat=0.7, gamma=1.1),
    'courtyard': dict(lift=(10, 13, 12), sat=0.6, gamma=1.08), 'entrance': dict(lift=(5, 7, 6), sat=0.55, gamma=1.12),
    'bedroom_on': dict(lift=(10, 8, 6), sat=0.8, gamma=1.02), 'bedroom_off': dict(lift=(6, 8, 12), sat=0.7, gamma=1.1),
}


def prop(room, pid, name, depth, draw, variant=None, darken=None):
    set_size(1800, 1400); img = layer(); draw(img)
    out = img.resize((W, H), Image.LANCZOS)
    if darken: out = darken_rgba(out, *darken)
    out = grade_rgba(out, **GRADE[variant or room])
    box = out.getchannel('A').point(lambda v: 255 if v > 6 else 0).getbbox()
    x0, y0, x1, y1 = max(0, box[0] - 4), max(0, box[1] - 4), min(W, box[2] + 4), min(H, box[3] + 4)
    fname = pid + (('_' + variant.split('_')[1]) if variant else '')
    out.crop((x0, y0, x1, y1)).save(f'{OUT}/{fname}.webp', 'WEBP', quality=86, alpha_quality=90, method=6)
    if not variant or variant.endswith('_on'):
        META.append({'id': pid, 'room': room, 'n': name, 'x': (x0 + x1) / 2, 'y': y1, 'w': x1 - x0, 'h': y1 - y0, 'd': depth, 'v': bool(variant)})
    print('prop', fname, x1 - x0, y1 - y0)


# engawa garden
prop('engawa', 'p_eng_toro', 'Каменный фонарь', .42, lambda im: toro(im, 1180, 1085, 200, 5))
for i, (sx, sy) in enumerate([(520, 1098), (760, 1104), (1000, 1098)]):
    prop('engawa', f'p_eng_stone{i}', 'Садовый камень', .42, lambda im, sx=sx, sy=sy, i=i: stone(im, sx, sy, 58, 14, 40 + i, hexc('#454a44')))

# kitchen
for i, (cx, w, h, c) in enumerate([(1010, 70, 34, '#5b3a2a'), (1100, 90, 40, '#3c4a52'), (1200, 60, 50, '#8b7c62'), (1300, 96, 36, '#2e2a26'), (1420, 70, 60, '#6c5a3e'), (1530, 88, 42, '#44564f')]):
    prop('kitchen', f'p_kit_bowl{i}', 'Пиала', .5, lambda im, cx=cx, w=w, h=h, c=c, i=i: ceramic(im, cx, 470, w, h, 20 + i, hexc(c)))
for i, (cx, w, h, c) in enumerate([(1030, 110, 60, '#2a2522'), (1180, 80, 44, '#7a6a52'), (1330, 120, 54, '#3b4a45'), (1500, 90, 70, '#5a3a2a')]):
    prop('kitchen', f'p_kit_pot{i}', 'Горшок', .5, lambda im, cx=cx, w=w, h=h, c=c, i=i: ceramic(im, cx, 700, w, h, 40 + i, hexc(c)))
prop('kitchen', 'p_kit_lantern', 'Бумажный фонарь', .5, lambda im: chochin(im, 1560, 300, 62, True))


def noren(im):
    for i in range(3):
        x0 = 30 + i * 62; m = Image.new('L', (int(58 * SS), int(420 * SS)), 255)
        im.alpha_composite(textured_fill(m, hexc('#1e2a3b'), hexc('#0f1520'), hexc('#2c3b52'), 16 * SS, 60 + i, (1, 4)), (int(x0 * SS), 0))
    d = ImageDraw.Draw(im); d.ellipse([70 * SS, 250 * SS, 150 * SS, 330 * SS], fill=hexc('#c9c1ae')); d.ellipse([88 * SS, 262 * SS, 150 * SS, 320 * SS], fill=hexc('#1e2a3b'))
prop('kitchen', 'p_kit_noren', 'Занавеска норэн', .5, noren)


def kamado(im):
    m = Image.new('L', (int(460 * SS), int(300 * SS)), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, m.width - 1, m.height - 1], 30 * SS, fill=255)
    im.alpha_composite(textured_fill(m, hexc('#5e4f3e'), hexc('#3a2e22'), hexc('#76664f'), 34 * SS, 50, contrast=0.9), (int(1240 * SS), int(850 * SS)))
    d = ImageDraw.Draw(im); d.ellipse([1330 * SS, 960 * SS, 1440 * SS, 1060 * SS], fill=hexc('#120c08'))
    d.ellipse([1300 * SS, 800 * SS, 1600 * SS, 880 * SS], fill=hexc('#171513')); d.rectangle([1320 * SS, 760 * SS, 1580 * SS, 840 * SS], fill=hexc('#1f1c19'))
    fire = layer(); ImageDraw.Draw(fire).ellipse([1345 * SS, 990 * SS, 1425 * SS, 1060 * SS], fill=(230, 110, 40, 200)); im.alpha_composite(fire)
prop('kitchen', 'p_kit_kamado', 'Печь камадо', .8, kamado)

# onsen stepping stones
for i, (x, y, rx, ry) in enumerate([(900, 1330, 190, 46), (520, 1300, 130, 40), (1300, 1310, 150, 44), (160, 1250, 110, 50), (1660, 1260, 120, 54)]):
    prop('onsen', f'p_ons_stone{i}', 'Плоский камень', .82, lambda im, x=x, y=y, rx=rx, ry=ry, i=i: stone(im, x, y, rx, ry, 300 + i, hexc('#4b4f49')))


# bedroom: lamp and ikebana, lit and dark variants
def andon(lit):
    def f(im):
        ax, ab = 330, 1300; d = ImageDraw.Draw(im)
        wood_block(im, (ax - 70, ab - 20, ax + 70, ab), 28, hexc('#241a13'), hexc('#0e0a07'), hexc('#3a2b1f'))
        pap = hexc('#f0d59a') if lit else hexc('#5f584a'); m = Image.new('L', (int(110 * SS), int(200 * SS)), 255)
        im.alpha_composite(textured_fill(m, pap, mixc(pap, (0, 0, 0, 255), .25), mixc(pap, (255, 255, 255, 255), .2), 5 * SS, 29), (int((ax - 55) * SS), int((ab - 240) * SS)))
        for xx in (ax - 58, ax + 52): d.rectangle([xx * SS, (ab - 250) * SS, (xx + 6) * SS, ab * SS], fill=hexc('#160f0a'))
        d.rectangle([(ax - 58) * SS, (ab - 144) * SS, (ax + 58) * SS, (ab - 138) * SS], fill=hexc('#160f0a'))
        d.rectangle([(ax - 58) * SS, (ab - 250) * SS, (ax + 58) * SS, (ab - 242) * SS], fill=hexc('#160f0a'))
    return f
def ikebana_vase(im):
    ceramic(im, 270, 1060, 90, 70, 5, hexc('#2b3a3a'))
    ik = layer(); maple(ik, 270 * SS, 995 * SS, 330 * SS, 12, PAL_SAKURA, BARK, -.2); im.alpha_composite(atmos(ik, hexc('#3a352c'), .25))
for v, lit in (('bedroom_on', True), ('bedroom_off', False)):
    dk = None if lit else (.55, (8, 12, 26))
    prop('bedroom', 'p_bed_andon', 'Андон', .8, andon(lit), variant=v, darken=dk)
    prop('bedroom', 'p_bed_ikebana', 'Икебана в нише', .5, ikebana_vase, variant=v, darken=dk)

# games clearing
prop('games', 'p_gam_toro0', 'Каменный фонарь', .8, lambda im: toro(im, 360, 1250, 250, 8))
prop('games', 'p_gam_toro1', 'Каменный фонарь', .8, lambda im: toro(im, 1440, 1250, 250, 9))
for i, x in enumerate(range(620, 1200, 120)):
    prop('games', f'p_gam_stone{i}', 'Камень дорожки', .8, lambda im, x=x, i=i: stone(im, x + (i % 2) * 20, 1300 - i * 3, 70, 16, 400 + i, hexc('#4c504a')))

# courtyard rocks
for i, (x, y, rx, ry) in enumerate([(1130, 930, 140, 50), (1320, 960, 110, 40), (1560, 945, 160, 54), (1000, 1000, 90, 30)]):
    prop('courtyard', f'p_crt_rock{i}', 'Валун в заводи', .55, lambda im, x=x, y=y, rx=rx, ry=ry, i=i: stone(im, x, y, rx, ry, 30 + i, hexc('#3a3f3b')))
for i, (x, y, rx, ry) in enumerate([(900, 1330, 260, 58), (520, 1300, 150, 40), (1300, 1310, 170, 44), (160, 1270, 130, 50), (1660, 1270, 140, 52)]):
    prop('courtyard', f'p_crt_stone{i}', 'Плоский камень', .8, lambda im, x=x, y=y, rx=rx, ry=ry, i=i: stone(im, x, y, rx, ry, 60 + i, hexc('#4a4e48')))


# entrance
def ent_toro(im):
    toro(im, 330, 1260, 520, 31)
    ImageDraw.Draw(im).rectangle([(330 - 18) * SS, (1260 - 400) * SS, (330 + 18) * SS, (1260 - 350) * SS], fill=hexc('#f2cf8a'))
def ent_pillar(im):
    stone(im, 1180, 1030, 34, 12, 43, hexc('#4a4b45'))
    m = Image.new('L', (int(60 * SS), int(260 * SS)), 255)
    im.alpha_composite(textured_fill(m, hexc('#6a6b63'), hexc('#34352f'), hexc('#8a8b80'), 12 * SS, 44, contrast=1.3), (int(1150 * SS), int(770 * SS)))
prop('entrance', 'p_ent_toro', 'Каменный фонарь', .85, ent_toro)
prop('entrance', 'p_ent_pillar', 'Каменный столб', .7, ent_pillar)

json.dump(META, open(f'{OUT}/props.json', 'w'), ensure_ascii=False)
print(len(META), 'props')
