"""Oversiktsmosaikk av søkefliser med kommunegrense og rutenett (EPSG:25833-koordinater). Bruk: mosaic.py esri|topo [px_per_km]"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw
from pyproj import Transformer
from shapely.geometry import shape
from shapely import ops
P = Path(__file__).parent
prov = sys.argv[1]; ppk = int(sys.argv[2]) if len(sys.argv) > 2 else 100
specs = json.loads((P / ('scan-esri.json' if prov == 'esri' else 'scan-topo.json')).read_text())
X0 = min(s['bbox'][0] for s in specs); Y1 = max(s['bbox'][3] for s in specs)
X1 = max(s['bbox'][2] for s in specs); Y0 = min(s['bbox'][1] for s in specs)
W = int((X1 - X0) / 1000 * ppk); H = int((Y1 - Y0) / 1000 * ppk)
can = Image.new('RGB', (W, H), 'white')
px = lambda x, y: ((x - X0) / 1000 * ppk, (Y1 - y) / 1000 * ppk)
for s in specs:
    m = json.loads((P / 'images' / f"{s['id']}.json").read_text())
    a, b, c, d = m['bbox']
    im = Image.open(P / 'images' / f"{s['id']}.{'jpg' if prov == 'esri' else 'png'}").convert('RGB')
    im = im.resize((int((c - a) / 1000 * ppk), int((d - b) / 1000 * ppk)))
    can.paste(im, tuple(int(v) for v in px(a, d)))
dr = ImageDraw.Draw(can)
T = Transformer.from_crs(4326, 25833, always_xy=True).transform
g = ops.transform(T, shape(json.loads((P / 'kommunegrense.geojson').read_text())['features'][0]['geometry']))
for poly in getattr(g, 'geoms', [g]):
    dr.line([px(*c) for c in poly.exterior.coords], fill='yellow', width=2)
for x in range(int(X0) // 1000 * 1000, int(X1), 1000):
    dr.line([px(x, Y0), px(x, Y1)], fill=(255, 0, 255) if x % 5000 == 0 else (120, 120, 120), width=1)
    if x % 2000 == 0: dr.text((px(x, Y1)[0] + 2, 2), str(x // 1000), fill='red')
for y in range(int(Y0) // 1000 * 1000, int(Y1), 1000):
    dr.line([px(X0, y), px(X1, y)], fill=(255, 0, 255) if y % 5000 == 0 else (120, 120, 120), width=1)
    if y % 2000 == 0: dr.text((2, px(X0, y)[1] + 2), str(y // 1000), fill='red')
out = P / 'qa' / f'mosaic-{prov}-{ppk}.jpg'; can.save(out, quality=88); print(out, can.size, 'X0', X0, 'Y1', Y1)
