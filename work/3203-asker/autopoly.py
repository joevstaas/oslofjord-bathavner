"""Halvautomatiske kandidatpolygoner: OSM-pirer klynges (60 m), bufres 12 m, lukkes (20 m) og klippes mot
vannmaske fra Kartverkets topografiske kart (utvidet 4 m) og kommunegrensen. Resultatet er utkast som MÅ
kontrolleres visuelt; det er ikke leveransegeometri før det er godkjent i review."""
import json, warnings
from pathlib import Path
import numpy as np
from PIL import Image
from pyproj import Transformer
from shapely.geometry import shape, LineString, Point, box, Polygon, mapping
from shapely.ops import unary_union
from shapely import ops
warnings.filterwarnings('ignore')
P = Path(__file__).parent
T = Transformer.from_crs(4326, 25833, always_xy=True).transform
B = ops.transform(T, shape(json.loads((P / 'kommunegrense.geojson').read_text())['features'][0]['geometry']))
topo = json.loads((P / 'scan-topo.json').read_text())

def water(bb):
    """Vannflate (shapely) innen bb fra topografiske fliser, 2,5 m-raster, som radvise løp."""
    rects = []
    for s in topo:
        a, b, c, d = s['bbox']
        if not box(a, b, c, d).intersects(box(*bb)): continue
        arr = np.asarray(Image.open(P / 'images' / f"{s['id']}.png").convert('RGB')).astype(int)
        x0, y0, x1, y1 = box(a, b, c, d).intersection(box(*bb)).bounds
        u0, u1 = int((x0 - a) / 2.5), int(np.ceil((x1 - a) / 2.5)); v0, v1 = int((d - y1) / 2.5), int(np.ceil((d - y0) / 2.5))
        sub = arr[v0:v1, u0:u1]; w = (sub[..., 2] > sub[..., 0] + 12) & (sub[..., 2] >= sub[..., 1] - 2)
        for i, row in enumerate(w):
            j = 0; n = len(row)
            while j < n:
                if row[j]:
                    k = j
                    while k < n and row[k]: k += 1
                    rects.append(box(a + (u0 + j) * 2.5, d - (v0 + i + 1) * 2.5, a + (u0 + k) * 2.5, d - (v0 + i) * 2.5)); j = k
                else: j += 1
    return unary_union(rects) if rects else Polygon()

els = json.loads((P / 'raw/overpass-asker.json').read_text())['elements']
piers, marks = [], []
for e in els:
    t = e.get('tags', {})
    if e['type'] == 'way' and t.get('man_made') == 'pier' and 'geometry' in e:
        g = LineString([T(p['lon'], p['lat']) for p in e['geometry']])
        if g.distance(B) < 50: piers.append(dict(id=f"way/{e['id']}", g=g, tags=t))
    elif t.get('leisure') == 'marina' or 'mooring' in t:
        if e['type'] == 'node': g = Point(T(e['lon'], e['lat']))
        elif 'geometry' in e: g = LineString([T(p['lon'], p['lat']) for p in e['geometry']]) if len(e['geometry']) > 1 else Point(T(e['geometry'][0]['lon'], e['geometry'][0]['lat']))
        else: continue
        if g.distance(B) < 300: marks.append(dict(id=f"{e['type']}/{e['id']}", g=g, name=t.get('name'), kind=t.get('leisure') or 'mooring'))
cl = []
for p in piers:
    hit = [k for k in cl if any(p['g'].distance(q['g']) < 60 for q in k)]
    if hit:
        k = hit[0]; k.append(p)
        for o in hit[1:]: k.extend(o); cl.remove(o)
    else: cl.append([p])
out = []
for k in cl:
    L = sum(p['g'].length for p in k); u = unary_union([p['g'] for p in k])
    near = [m for m in marks if m['g'].distance(u) < 120]
    if L < 25 and not near: continue
    poly = unary_union([p['g'].buffer(12, cap_style=2) for p in k]).buffer(20).buffer(-20)
    bb = [v + o for v, o in zip(poly.bounds, (-30, -30, 30, 30))]
    poly = poly.intersection(water(bb).buffer(4)).intersection(B)
    if poly.is_empty: continue
    if poly.geom_type == 'MultiPolygon': poly = max(poly.geoms, key=lambda g: g.area) if max(g.area for g in poly.geoms) > 0.8 * poly.area else poly
    c = u.centroid
    out.append(dict(cid=f'A{len(out)+1:03d}', x=round(c.x), y=round(c.y), pier_len=round(L), n_piers=len(k), area=round(poly.area),
                    osm_piers=[p['id'] for p in k], marks=[dict(id=m['id'], name=m['name'], kind=m['kind']) for m in near],
                    geom=mapping(poly)))
out.sort(key=lambda r: (r['x'] // 2000, -r['y']))
for i, r in enumerate(out): r['cid'] = f'A{i+1:03d}'
(P / 'auto-candidates.json').write_text(json.dumps(out, ensure_ascii=False))
marked = {m['id'] for r in out for m in r['marks']}
orph = [dict(id=m['id'], name=m['name'], kind=m['kind'], x=round(m['g'].centroid.x), y=round(m['g'].centroid.y)) for m in marks if m['id'] not in marked]
(P / 'osm-marks-without-piers.json').write_text(json.dumps(orph, ensure_ascii=False, indent=1))
print('pirer', len(piers), 'klynger', len(cl), 'kandidater', len(out), 'merker uten pirklynge', len(orph))
for r in out: print(r['cid'], r['x'], r['y'], r['pier_len'], r['n_piers'], r['area'], [m['name'] for m in r['marks']])
