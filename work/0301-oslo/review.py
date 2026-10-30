"""Kontrollark: kandidatpolygon (rød), OSM-pirer (gul), kommunegrense (cyan) på beste tilgjengelige Esri-bilde.
Bruk: review.py <candidates.json> <prefix> [per_ark=9] [ids-kommaseparert]"""
import json, sys, warnings
from pathlib import Path
from PIL import Image, ImageDraw
from pyproj import Transformer
from shapely.geometry import shape, box, LineString
from shapely import ops
warnings.filterwarnings('ignore')
P = Path(__file__).parent
T = Transformer.from_crs(4326, 25833, always_xy=True).transform
bnd = ops.transform(T, shape(json.loads((P / 'kommunegrense.geojson').read_text())['features'][0]['geometry'])).boundary
cands = json.loads((P / sys.argv[1]).read_text()); pre = sys.argv[2]
per = int(sys.argv[3]) if len(sys.argv) > 3 else 9
if len(sys.argv) > 4: ids = sys.argv[4].split(','); cands = [c for c in cands if c['cid'] in ids]
pier = {}
for e in json.loads((P / 'raw/overpass-oslo.json').read_text())['elements']:
    if e['type'] == 'way' and e.get('tags', {}).get('man_made') in ('pier', 'breakwater') and 'geometry' in e:
        pier[f"way/{e['id']}"] = LineString([T(p['lon'], p['lat']) for p in e['geometry']])
imgs = []
for f in (P / 'images').glob('*.json'):
    m = json.loads(f.read_text())
    if m.get('source', '').startswith('Esri') and (P / 'images' / f"{f.stem}.jpg").exists():
        imgs.append((m['bbox'][2] - m['bbox'][0]) / m['width'] and ((m['bbox'][2] - m['bbox'][0]) / m['width'], f.stem, m['bbox']))
imgs.sort()
S = 420; panels = []
for c in cands:
    g = shape(c['geom']) if c.get('geom') else box(c["x"] - c.get("r", 110), c["y"] - c.get("r", 110), c["x"] + c.get("r", 110), c["y"] + c.get("r", 110))
    x0, y0, x1, y1 = g.bounds; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; h = max(x1 - x0, y1 - y0) / 2 + 50
    fr = (cx - h, cy - h, cx + h, cy + h)
    best = next(((r, k, bb) for r, k, bb in imgs if bb[0] <= fr[0] and bb[1] <= fr[1] and bb[2] >= fr[2] and bb[3] >= fr[3]), None)
    if not best:
        best = max(((r, k, bb) for r, k, bb in imgs if box(*bb).intersects(box(*fr))), key=lambda t: box(*t[2]).intersection(box(*fr)).area - t[0], default=None)
    if not best: continue
    r, key, (a, b, cc, d) = best
    im = Image.open(P / 'images' / f'{key}.jpg').convert('RGB'); W, H = im.size
    fr = (max(fr[0], a), max(fr[1], b), min(fr[2], cc), min(fr[3], d))
    im = im.crop((int((fr[0] - a) / (cc - a) * W), int((d - fr[3]) / (d - b) * H), int((fr[2] - a) / (cc - a) * W), int((d - fr[1]) / (d - b) * H)))
    im = im.resize((S, max(1, int(S * (fr[3] - fr[1]) / (fr[2] - fr[0]))))); dr = ImageDraw.Draw(im)
    px = lambda x, y: ((x - fr[0]) / (fr[2] - fr[0]) * im.width, (fr[3] - y) / (fr[3] - fr[1]) * im.height)
    for pid in c.get('osm_piers', []):
        if pid in pier: dr.line([px(*q) for q in pier[pid].coords], fill=(255, 230, 0), width=1)
    cl = bnd.intersection(box(*fr))
    for ln in getattr(cl, 'geoms', [cl]):
        if not ln.is_empty and hasattr(ln, 'coords'): dr.line([px(*q) for q in ln.coords], fill='cyan', width=2)
    for pg in getattr(g, 'geoms', [g]):
        if c.get('geom'): dr.line([px(*q) for q in pg.exterior.coords], fill='red', width=2)
    # 50 m skala
    dr.line([(5, im.height - 8), (5 + 50 / (fr[2] - fr[0]) * S, im.height - 8)], fill='white', width=3)
    panel = Image.new('RGB', (S, S + 30), 'white'); panel.paste(im, (0, 30))
    ImageDraw.Draw(panel).text((3, 2), f"{c['cid']} x{int(fr[0])}-{int(fr[2])} y{int(fr[1])}-{int(fr[3])} {key}", fill='black')
    ImageDraw.Draw(panel).text((3, 15), f"pir {c.get('pier_len','')} m {' / '.join(str(m['name']) for m in c.get('marks', []))[:50]}", fill='black')
    panels.append(panel)
n = 0
for k in range(0, len(panels), per):
    grp = panels[k:k + per]; cols = 3
    can = Image.new('RGB', (cols * S + 10, ((len(grp) + cols - 1) // cols) * (S + 35)), 'white')
    for i, pn in enumerate(grp): can.paste(pn, ((i % cols) * (S + 5), (i // cols) * (S + 35)))
    can.save(P / 'qa' / f'{pre}-{k // per:02d}.jpg', quality=85); n += 1
print(n, 'ark', len(panels), 'paneler')
