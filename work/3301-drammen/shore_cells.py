"""Finn 1 km-ruter i Drammen (med 150 m belte) som inneholder både vann og land i topografisk kart.
Vannmaske brukes bare til prioritering; resultatet kontrolleres mot oversiktsmosaikk."""
import json
from pathlib import Path
import numpy as np
from PIL import Image
from pyproj import Transformer
from shapely.geometry import shape, box
from shapely import ops
P = Path(__file__).parent
T = Transformer.from_crs(4326, 25833, always_xy=True).transform
g = ops.transform(T, shape(json.loads((P / 'kommunegrense.geojson').read_text())['features'][0]['geometry']))
gb = g.buffer(150)
specs = json.loads((P / 'scan-topo.json').read_text())
def water_frac(cell):
    tot = wat = 0
    for s in specs:
        a, b, c, d = s['bbox']
        inter = box(a, b, c, d).intersection(cell)
        if inter.is_empty or inter.area < 1: continue
        arr = np.asarray(Image.open(P / 'images' / f"{s['id']}.png").convert('RGB')).astype(int)
        x0, y0, x1, y1 = inter.bounds
        u0, u1 = int((x0 - a) / 2.5), int((x1 - a) / 2.5); v0, v1 = int((d - y1) / 2.5), int((d - y0) / 2.5)
        sub = arr[v0:v1, u0:u1]
        r, gg, bl = sub[..., 0], sub[..., 1], sub[..., 2]
        w = (bl > r + 12) & (bl >= gg - 2)
        tot += w.size; wat += w.sum()
    return wat / tot if tot else None
x0, y0, x1, y1 = g.bounds
cells = []
for x in range(int(x0) // 1000 * 1000, int(x1) + 1, 1000):
    for y in range(int(y0) // 1000 * 1000, int(y1) + 1, 1000):
        cell = box(x, y, x + 1000, y + 1000)
        if not gb.intersects(cell): continue
        f = water_frac(cell)
        cells.append(dict(cell=f'c{x//1000}-{y//1000}', bbox=[x, y, x + 1000, y + 1000], water_frac=None if f is None else round(float(f), 3),
                          in_boundary_frac=round(cell.intersection(g).area / 1e6, 3)))
shore = [c for c in cells if c['water_frac'] is not None and 0.003 < c['water_frac'] < 0.995]
(P / 'cells.json').write_text(json.dumps(cells, indent=1))
print('ruter', len(cells), 'kystruter', len(shore))
print(' '.join(c['cell'] for c in shore))
