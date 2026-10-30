"""Kontaktark av detaljfliser med rutenavn og 100 m-rutenett. Bruk: contact.py <specs.json> <prefix> [per_ark] [px]"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw
P = Path(__file__).parent
specs = json.loads((P / sys.argv[1]).read_text()); pre = sys.argv[2]
n = int(sys.argv[3]) if len(sys.argv) > 3 else 6; S = int(sys.argv[4]) if len(sys.argv) > 4 else 500
specs.sort(key=lambda s: (-s['bbox'][1], s['bbox'][0]))
cols = 3
sheets = []
for k in range(0, len(specs), n):
    grp = specs[k:k + n]; rows = (len(grp) + cols - 1) // cols
    can = Image.new('RGB', (cols * S, rows * (S + 16)), 'white'); d = ImageDraw.Draw(can)
    for i, s in enumerate(grp):
        f = P / 'images' / f"{s['id']}.jpg"
        if not f.exists(): continue
        m = json.loads(f.with_suffix('.json').read_text()); a, b, c, dd = m['bbox']
        im = Image.open(f).convert('RGB').resize((S, S)); di = ImageDraw.Draw(im)
        for x in range(int(a) // 100 * 100 + 100, int(c), 100):
            u = (x - a) / (c - a) * S; di.line([(u, 0), (u, S)], fill=(255, 255, 0) if x % 500 == 0 else (90, 90, 90), width=1)
        for y in range(int(b) // 100 * 100 + 100, int(dd), 100):
            v = (dd - y) / (dd - b) * S; di.line([(0, v), (S, v)], fill=(255, 255, 0) if y % 500 == 0 else (90, 90, 90), width=1)
        can.paste(im, ((i % cols) * S, (i // cols) * (S + 16) + 16))
        d.text(((i % cols) * S + 3, (i // cols) * (S + 16) + 2), f"{s['id']}  x{int(a)}-{int(c)} y{int(b)}-{int(dd)}", fill='black')
    out = P / 'qa' / f'{pre}-{k // n:02d}.jpg'; can.save(out, quality=85); sheets.append(str(out.name))
print(len(sheets), 'ark')
