"""Visuell kontroll: eksportert GeoJSON projisert tilbake på kildebildet, med kommunegrense. Lager qa/qa-<n>.jpg."""
import json, warnings
from pathlib import Path
from PIL import Image, ImageDraw
from pyproj import Transformer
from shapely.geometry import shape, box
from shapely import ops
warnings.filterwarnings('ignore')
P = Path(__file__).parent
F = Transformer.from_crs(4326, 25833, always_xy=True).transform
fs = json.loads((P / 'asker-bathavner.geojson').read_text())['features']
bnd = ops.transform(F, shape(json.loads((P / 'kommunegrense.geojson').read_text())['features'][0]['geometry'])).boundary
S = 480; panels = []
for f in fs:
    p = f['properties']; g = ops.transform(F, shape(f['geometry']))
    m = json.loads((P / 'images' / f"{p['image_id']}.json").read_text()); a, b, c, d = m['bbox']
    x0, y0, x1, y1 = g.bounds; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; half = max(x1 - x0, y1 - y0) / 2 + 40
    fr = (max(a, cx - half), max(b, cy - half), min(c, cx + half), min(d, cy + half))
    im = Image.open(P / 'images' / f"{p['image_id']}.jpg").convert('RGB'); W, H = im.size
    im = im.crop((int((fr[0] - a) / (c - a) * W), int((d - fr[3]) / (d - b) * H), int((fr[2] - a) / (c - a) * W), int((d - fr[1]) / (d - b) * H)))
    im = im.resize((S, int(S * (fr[3] - fr[1]) / (fr[2] - fr[0])))); dr = ImageDraw.Draw(im)
    px = lambda x, y: ((x - fr[0]) / (fr[2] - fr[0]) * im.width, (fr[3] - y) / (fr[3] - fr[1]) * im.height)
    cl = bnd.intersection(box(*fr))
    for ln in getattr(cl, 'geoms', [cl]):
        if not ln.is_empty: dr.line([px(*q) for q in ln.coords], fill='yellow', width=2)
    dr.line([px(*q) for q in g.exterior.coords], fill='red', width=2)
    panel = Image.new('RGB', (S, S + 18), 'white'); panel.paste(im, (0, 18))
    ImageDraw.Draw(panel).text((3, 3), f"{p['id']} {p['name'][:52]}", fill='black'); panels.append(panel)
for k in range(0, len(panels), 6):
    grp = panels[k:k + 6]; can = Image.new('RGB', (3 * S, ((len(grp) + 2) // 3) * (S + 18)), 'white')
    for i, pn in enumerate(grp): can.paste(pn, ((i % 3) * S, (i // 3) * (S + 18)))
    can.save(P / 'qa' / f'qa-{k // 6}.jpg', quality=88)
print(len(panels), 'paneler')
