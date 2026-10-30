"""Kontaktark for systematisk søk B: detaljfliser med inkluderte kandidatpolygoner (rød), utelatte (oransje), OSM-pirer (gul)."""
import json, sys, warnings
from pathlib import Path
from PIL import Image, ImageDraw
from pyproj import Transformer
from shapely.geometry import shape, box, LineString
from shapely import ops
warnings.filterwarnings('ignore')
P = Path(__file__).parent
T = Transformer.from_crs(4326, 25833, always_xy=True).transform
ns = {}; exec((P / 'decisions.py').read_text(), ns); D = ns['D']
cands = {c['cid']: shape(c['geom']) for c in json.loads((P / 'auto-candidates.json').read_text())}
piers = [LineString([T(p['lon'], p['lat']) for p in e['geometry']]) for e in json.loads((P / 'raw/overpass-drammen.json').read_text())['elements']
         if e['type'] == 'way' and e.get('tags', {}).get('man_made') == 'pier' and 'geometry' in e]
bnd = ops.transform(T, shape(json.loads((P / 'kommunegrense.geojson').read_text())['features'][0]['geometry'])).boundary
specs = sorted(json.loads((P / 'detail-esri.json').read_text()), key=lambda s: (s['bbox'][0] // 3000, -s['bbox'][1], s['bbox'][0]))
skip = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else set()
specs = [s for s in specs if s['id'] not in skip]
S = 430; pre = sys.argv[1]
for k in range(0, len(specs), 9):
    can = Image.new('RGB', (3 * S + 10, 3 * (S + 14)), 'white'); dc = ImageDraw.Draw(can)
    for i, s in enumerate(specs[k:k + 9]):
        m = json.loads((P / 'images' / f"{s['id']}.json").read_text()); a, b, c, d = m['bbox']
        im = Image.open(P / 'images' / f"{s['id']}.jpg").convert('RGB').resize((S, S)); dr = ImageDraw.Draw(im)
        px = lambda x, y: ((x - a) / (c - a) * S, (d - y) / (d - b) * S)
        fr = box(a, b, c, d)
        for pl in piers:
            if pl.intersects(fr): dr.line([px(*q) for q in pl.coords], fill=(255, 230, 0), width=1)
        for cid, g in cands.items():
            if g.intersects(fr):
                col = 'red' if D.get(cid, {}).get('action') != 'exc' else (255, 140, 0)
                for pg in getattr(g, 'geoms', [g]): dr.line([px(*q) for q in pg.exterior.coords], fill=col, width=2)
        cl = bnd.intersection(fr)
        for ln in getattr(cl, 'geoms', [cl]):
            if not ln.is_empty and hasattr(ln, 'coords'): dr.line([px(*q) for q in ln.coords], fill='cyan', width=1)
        X, Y = (i % 3) * (S + 5), (i // 3) * (S + 14)
        can.paste(im, (X, Y + 14)); dc.text((X + 2, Y), f"{s['id']} x{int(a)} y{int(b)}", fill='black')
    can.save(P / 'qa' / f'{pre}-{k // 9:02d}.jpg', quality=82)
print((len(specs) + 8) // 9, 'ark')
