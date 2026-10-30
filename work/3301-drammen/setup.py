"""Kommunegrense, søkefliser og tidtaking for Drammen rev. 1."""
import json
from pathlib import Path
from pyproj import Transformer
from shapely.geometry import shape, box, mapping
from shapely.ops import transform

P = Path(__file__).parent
T = Transformer.from_crs(4326, 25833, always_xy=True).transform
src = json.loads((P / 'raw/kommunegrense-4326.json').read_text())
geo = shape(src['omrade'])
fc = dict(type='FeatureCollection', features=[dict(type='Feature', properties=dict(
    kommunenummer=src['kommunenummer'], kommunenavn=src['kommunenavn'],
    source='https://api.kartverket.no/kommuneinfo/v1/kommuner/3301/omrade?utkoordsys=4326',
    source_crs='EPSG:4326', retrieved_date='2026-10-29'), geometry=mapping(geo))])
(P / 'kommunegrense.geojson').write_text(json.dumps(fc, ensure_ascii=False))
g = transform(T, geo)
x0, y0, x1, y1 = g.bounds
print('bounds 25833', [round(v) for v in g.bounds], 'area km2', round(g.area / 1e6, 1))
tiles = []
for i, x in enumerate(range(int(x0) // 1000 * 1000, int(x1), 3600)):
    for j, y in enumerate(range(int(y0) // 1000 * 1000, int(y1), 3600)):
        b = [x, y, x + 4000, y + 4000]
        if g.intersects(box(*b)):
            tiles.append(dict(id=f'coast-{i}-{j}', bbox=b, width=1600, height=1600))
(P / 'scan-topo.json').write_text(json.dumps(tiles, indent=1))
(P / 'scan-esri.json').write_text(json.dumps([dict(t, id='a-' + t['id']) for t in tiles], indent=1))
print('fliser', len(tiles))
