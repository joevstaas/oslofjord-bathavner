"""Filtrer Overpass-svar til Råde (med 300 m belte) og lag kandidatliste og pir-klynger."""
import json
from pathlib import Path
from pyproj import Transformer
from shapely.geometry import shape, Point
from shapely import ops
P = Path(__file__).parent
T = Transformer.from_crs(4326, 25833, always_xy=True).transform
g = ops.transform(T, shape(json.loads((P / 'kommunegrense.geojson').read_text())['features'][0]['geometry']))
els = json.loads((P / 'raw/overpass-rade.json').read_text())['elements']
cands, piers = [], []
for e in els:
    c = e.get('center', e); t = e.get('tags', {})
    x, y = T(c['lon'], c['lat']); pt = Point(x, y)
    if pt.distance(g) > 300:
        continue
    rec = dict(osm_id=f"{e['type']}/{e['id']}", lon=c['lon'], lat=c['lat'], x=round(x), y=round(y),
               inside=g.contains(pt), tags=t)
    (piers if t.get('man_made') == 'pier' else cands).append(rec)
(P / 'osm-candidates.json').write_text(json.dumps(cands, ensure_ascii=False, indent=1))
(P / 'osm-piers.json').write_text(json.dumps(piers, ensure_ascii=False, indent=1))
print('kandidater', len(cands), 'pirer', len(piers))
for c in cands:
    print(c['osm_id'], c['x'], c['y'], c['inside'], c['tags'].get('leisure'), c['tags'].get('name'), c['tags'].get('mooring'))
# pirklynger: grupper pirer innen 150 m
cl = []
for p in piers:
    for k in cl:
        if any(abs(p['x'] - q['x']) < 150 and abs(p['y'] - q['y']) < 150 for q in k):
            k.append(p); break
    else:
        cl.append([p])
print('pirklynger med >=2 pirer:')
for k in sorted(cl, key=len, reverse=True):
    if len(k) >= 2:
        print(len(k), round(sum(q['x'] for q in k) / len(k)), round(sum(q['y'] for q in k) / len(k)), [q['tags'].get('name') for q in k if q['tags'].get('name')])
