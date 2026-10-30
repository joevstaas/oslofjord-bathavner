"""Visning av georeferert bilde med 50 m-rutenett, koordinatetiketter, kommunegrense (gul) og ev. polygoner (rød).
Bruk: view.py <image_id> [size] [crop xmin,ymin,xmax,ymax] [polys.json]"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw
from pyproj import Transformer
from shapely.geometry import shape, box
from shapely import ops
P = Path(__file__).parent
key = sys.argv[1]; S = int(sys.argv[2]) if len(sys.argv) > 2 else 900
m = json.loads((P / 'images' / f'{key}.json').read_text()); a, b, c, d = m['bbox']
im = Image.open(P / 'images' / f"{key}.{'png' if (P / 'images' / f'{key}.png').exists() else 'jpg'}").convert('RGB')
W, H = im.size
if len(sys.argv) > 3 and sys.argv[3] != '-':
    xa, ya, xb, yb = map(float, sys.argv[3].split(','))
    im = im.crop((int((xa - a) / (c - a) * W), int((d - yb) / (d - b) * H), int((xb - a) / (c - a) * W), int((d - ya) / (d - b) * H)))
    a, b, c, d = xa, ya, xb, yb
im = im.resize((S, int(S * (d - b) / (c - a))), Image.LANCZOS); W, H = im.size
dr = ImageDraw.Draw(im)
px = lambda x, y: ((x - a) / (c - a) * W, (d - y) / (d - b) * H)
step = 50 if c - a <= 1000 else 100
for x in range(int(a) // step * step + step, int(c), step):
    dr.line([px(x, b), px(x, d)], fill=(255, 255, 255) if x % 100 == 0 else (150, 150, 150), width=1)
    if x % 100 == 0: dr.text((px(x, d)[0] + 2, 2), str(x % 10000), fill='cyan')
for y in range(int(b) // step * step + step, int(d), step):
    dr.line([px(a, y), px(c, y)], fill=(255, 255, 255) if y % 100 == 0 else (150, 150, 150), width=1)
    if y % 100 == 0: dr.text((2, px(a, y)[1] + 2), str(y % 10000), fill='cyan')
T = Transformer.from_crs(4326, 25833, always_xy=True).transform
g = ops.transform(T, shape(json.loads((P / 'kommunegrense.geojson').read_text())['features'][0]['geometry']))
cl = g.boundary.intersection(box(a, b, c, d))
for ln in getattr(cl, 'geoms', [cl]):
    if not ln.is_empty: dr.line([px(*q) for q in ln.coords], fill='yellow', width=2)
if len(sys.argv) > 4:
    for name, coords in json.loads(Path(sys.argv[4]).read_text()).items():
        pts = [px(*q) for q in coords]; dr.line(pts + [pts[0]], fill='red', width=2); dr.text(pts[0], name, fill='red')
out = P / 'qa' / f'view-{key}.jpg'; im.save(out, quality=90); print(out)
