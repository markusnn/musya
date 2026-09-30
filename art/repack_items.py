#!/usr/bin/env python3
"""Packs the first batches of things (one .webp per item) into one atlas per category.
The Claude copy of the game allows ~500 files, and one picture per category also loads faster.
Usage: repack_items.py → assets/items/atlas_<slug>.webp, rewrites ITEMS rows in index.html with "at": [slug, x, y]
and the IATL sizes; the single files stay on disk until they are deleted by hand."""
import json, os, re
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), '..')
SLUG = {'Кухня': 'kit', 'Омамори': 'omm', 'Посуда': 'dish', 'Игрушки': 'toy', 'Растения': 'pla', 'Веранда': 'ver1',
        'Спальня': 'bed1', 'Онсэн': 'ons1', 'Эма': 'ema', 'Фонари': 'lan', 'Кокэси': 'kok', 'Маски': 'msk', 'Свитки': 'scr',
        'Вход': 'ent1', 'Фурины': 'fur', 'Дарума': 'dar', 'Веера': 'fan', 'Подушки': 'zab', 'Реликвии': 'rel',
        'Гардероб': 'war1', 'Дворик': 'crt1', 'Игры': 'gam1', 'Светильники': 'lit', 'Манэки-нэко': 'mnk',
        'Цукумогами': 'tsu', 'Зонтики': 'umb'}


def main():
    path = os.path.join(ROOT, 'index.html'); html = open(path, encoding='utf-8').read()
    lines = html.split('\n'); n = next(i for i, l in enumerate(lines) if l.startswith('const ITEMS=['))
    items = json.loads(lines[n][len('const ITEMS='):].rstrip(';'))
    groups = {}
    for it in items:
        if 'at' in it: continue
        groups.setdefault(it['c'], []).append(it)
    sizes = {}
    for cat, lst in groups.items():
        slug = SLUG[cat]; ims = [(it, Image.open(os.path.join(ROOT, 'assets/items', it['id'] + '.webp')).convert('RGBA')) for it in lst]
        ims.sort(key=lambda t: -t[1].height); W = 1400; x = y = rowh = 0; pos = {}
        for it, im in ims:
            if x + im.width + 2 > W: x = 0; y += rowh + 2; rowh = 0
            pos[it['id']] = (x, y); x += im.width + 2; rowh = max(rowh, im.height)
        at = Image.new('RGBA', (W, y + rowh), (0, 0, 0, 0))
        for it, im in ims: at.paste(im, pos[it['id']])
        at.save(os.path.join(ROOT, 'assets/items', f'atlas_{slug}.webp'), 'WEBP', quality=90, alpha_quality=92, method=6)
        for it, _ in ims: it['at'] = [slug, *pos[it['id']]]
        sizes[slug] = [W, y + rowh]; print('atlas', slug, cat, len(lst), at.size)
    lines[n] = 'const ITEMS=' + json.dumps(items, ensure_ascii=False, separators=(',', ':')) + ';'
    html = '\n'.join(lines)
    m = re.search(r'const IATL=(\{.*?\}),IATL_IM', html)
    iatl = json.loads(m.group(1)); iatl.update(sizes)
    html = html[:m.start(1)] + json.dumps(iatl, separators=(',', ':')) + html[m.end(1):]
    open(path, 'w', encoding='utf-8').write(html)


if __name__ == '__main__':
    main()
