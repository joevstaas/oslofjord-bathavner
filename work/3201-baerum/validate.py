"""Teknisk kontroll av Bærum-leveransen. Leser samlefilen uten å endre den."""
import json, csv, warnings
from pathlib import Path
from pyproj import Transformer
from shapely.geometry import shape, Point
from shapely import ops
warnings.filterwarnings('ignore')
P = Path(__file__).parent; R = P.parents[1]
F = Transformer.from_crs(4326, 25833, always_xy=True).transform
fc = json.loads((P / 'baerum-bathavner.geojson').read_text()); assert 'crs' not in fc
fs = fc['features']; ids = [f['properties']['id'] for f in fs]
bnd = ops.transform(F, shape(json.loads((P / 'kommunegrense.geojson').read_text())['features'][0]['geometry']))
gs = [ops.transform(F, shape(f['geometry'])) for f in fs]
res = dict(polygons=len(fs), harbours=len({f['properties']['harbour_id'] for f in fs}), unique_ids=len(set(ids)) == len(ids),
           all_polygon=all(f['geometry']['type'] == 'Polygon' for f in fs), all_valid=all(g.is_valid and g.area > 0 for g in gs),
           closed_rings=all(f['geometry']['coordinates'][0][0] == f['geometry']['coordinates'][0][-1] for f in fs),
           lonlat_order=all(9 < c[0] < 12 and 58 < c[1] < 61 for f in fs for c in f['geometry']['coordinates'][0]),
           outside_boundary_m2=round(sum(g.difference(bnd).area for g in gs), 3),
           rep_point_inside=all(shape(f['geometry']).contains(Point(f['properties']['longitude'], f['properties']['latitude'])) for f in fs),
           internal_overlap_ge_1m2=[(ids[i], ids[j]) for i in range(len(gs)) for j in range(i + 1, len(gs)) if gs[i].intersection(gs[j]).area >= 1])
sam = json.loads((R / 'data/samlet/oslofjorden-bathavner-samlet.geojson').read_text())['features']
res['overlap_with_approved_m2'] = [(ids[i], s['properties']['id'], round(ops.transform(F, shape(s['geometry'])).intersection(g).area, 2)) for s in sam for i, g in enumerate(gs) if ops.transform(F, shape(s['geometry'])).intersection(g).area > 0.01]
res['id_collision_with_approved'] = sorted(set(ids) & {s['properties']['id'] for s in sam})
rows = list(csv.DictReader((P / 'baerum-metadata.csv').open(encoding='utf-8-sig'), delimiter=';'))
res.update(csv_rows=len(rows), csv_ids_match=[r['id'] for r in rows] == ids, all_til_godkjenning=all(f['properties']['approval_status'] == 'til_godkjenning' for f in fs))
(P / 'validation.json').write_text(json.dumps(res, ensure_ascii=False, indent=1) + '\n'); print(json.dumps(res, ensure_ascii=False))
