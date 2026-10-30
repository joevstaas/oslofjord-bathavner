"""Sjekk OSM-pirer/moloer i Fredrikstad (50 m belte) mot leverte polygoner; klynger udekkede objekter."""
import json, warnings
from shapely.geometry import shape, LineString
from shapely import ops
from pyproj import Transformer
warnings.filterwarnings('ignore')
T = Transformer.from_crs(4326, 25833, always_xy=True).transform
g = ops.transform(T, shape(json.load(open('kommunegrense.geojson'))['features'][0]['geometry']))
polys = [ops.transform(T, shape(f['geometry'])) for f in json.load(open('fredrikstad-bathavner.geojson'))['features']]
els = json.load(open('raw/overpass-rade-piers-geom.json'))['elements']
lines = []
for e in els:
    if 'geometry' not in e: continue
    ls = LineString([T(p['lon'], p['lat']) for p in e['geometry']])
    if ls.distance(g) > 50: continue
    lines.append(dict(id=e['id'], ls=ls, cov=any(ls.distance(p) < 30 for p in polys), tags=e.get('tags', {})))
un = [l for l in lines if not l['cov']]
print('ways', len(lines), 'udekket', len(un))
cl = []
for l in un:
    hit = [k for k in cl if any(l['ls'].distance(m['ls']) < 60 for m in k)]
    if hit:
        k = hit[0]; k.append(l)
        for o in hit[1:]: k.extend(o); cl.remove(o)
    else: cl.append([l])
out = []
for k in sorted(cl, key=lambda k: -sum(m['ls'].length for m in k)):
    c = ops.unary_union([m['ls'] for m in k]).centroid
    out.append(dict(n=len(k), len_m=round(sum(m['ls'].length for m in k)), x=round(c.x), y=round(c.y), inside=g.contains(c),
                    osm_ids=['way/%d' % m['id'] for m in k], kinds=sorted({m['tags'].get('man_made') or m['tags'].get('leisure') or '' for m in k})))
json.dump(out, open('osm-uncovered-piers.json', 'w'), indent=1)
for o in out: print(o['n'], o['len_m'], o['x'], o['y'], o['inside'], o['kinds'])
