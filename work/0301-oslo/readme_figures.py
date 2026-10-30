"""README-figurer: Dronninghavna (Bygdøy, Oslo) – råbilde, topo, OSM-pirer/utkast og endelige polygoner.
Krever lokale bilder i images/ (ikke i git). Skriver til docs/img/."""
import json, warnings
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from pyproj import Transformer
from shapely.geometry import shape, LineString
from shapely import ops
warnings.filterwarnings('ignore')
P = Path(__file__).parent; OUT = P.parents[1] / 'docs/img'; OUT.mkdir(parents=True, exist_ok=True)
T = Transformer.from_crs(4326, 25833, always_xy=True).transform
FR = (259000, 6648880, 259640, 6649400)  # utsnitt i EPSG:25833
S = 640  # bredde i piksler
H = int(S * (FR[3] - FR[1]) / (FR[2] - FR[0]))
try: FONT = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 15)
except OSError: FONT = ImageFont.load_default()

def mosaic(prefix):
    """Klipp FR ut av alle fliser med gitt prefiks; lim sammen i felles raster."""
    can = Image.new('RGB', (S, H), 'white')
    for f in sorted((P / 'images').glob(f'{prefix}*.json')):
        m = json.loads(f.read_text()); a, b, c, d = m['bbox']
        img = next((P / 'images' / f'{f.stem}{e}' for e in ('.jpg', '.png') if (P / 'images' / f'{f.stem}{e}').exists()), None)
        if not img or a >= FR[2] or c <= FR[0] or b >= FR[3] or d <= FR[1]: continue
        im = Image.open(img).convert('RGB'); W, Hh = im.size
        x0, y0, x1, y1 = max(a, FR[0]), max(b, FR[1]), min(c, FR[2]), min(d, FR[3])
        crop = im.crop((round((x0 - a) / (c - a) * W), round((d - y1) / (d - b) * Hh), round((x1 - a) / (c - a) * W), round((d - y0) / (d - b) * Hh)))
        tw, th = round((x1 - x0) / (FR[2] - FR[0]) * S), round((y1 - y0) / (FR[3] - FR[1]) * H)
        can.paste(crop.resize((tw, th), Image.LANCZOS), (round((x0 - FR[0]) / (FR[2] - FR[0]) * S), round((FR[3] - y1) / (FR[3] - FR[1]) * H)))
    return can

px = lambda x, y: ((x - FR[0]) / (FR[2] - FR[0]) * S, (FR[3] - y) / (FR[3] - FR[1]) * H)

def scalebar(dr):
    L = 100 / (FR[2] - FR[0]) * S
    dr.rectangle([8, H - 26, 16 + L, H - 6], fill=(0, 0, 0))
    dr.line([(12, H - 12), (12 + L, H - 12)], fill='white', width=3); dr.text((14, H - 25), '100 m', fill='white', font=FONT)

def label(dr, txt, xy=(8, 8)):
    w = dr.textlength(txt, font=FONT); dr.rectangle([xy[0], xy[1], xy[0] + w + 10, xy[1] + 22], fill=(0, 0, 0)); dr.text((xy[0] + 5, xy[1] + 3), txt, fill='white', font=FONT)

def side_by_side(a, b, name):
    can = Image.new('RGB', (2 * S + 8, H), 'white'); can.paste(a, (0, 0)); can.paste(b, (S + 8, 0)); can.save(OUT / name, quality=85)

esri = mosaic('d-c259-')
# 1: rådata
raw = esri.copy(); dr = ImageDraw.Draw(raw); label(dr, 'Esri World Imagery, 0.83 m/px'); scalebar(dr)
topo = mosaic('coast-3-3').resize((S, H)); dr = ImageDraw.Draw(topo); label(dr, 'Kartverket topographic map (WMS)'); scalebar(dr)
side_by_side(raw, topo, 'raw-imagery-and-map.jpg')

# 2: OSM-pirer og automatisk utkast
piers = {f"way/{e['id']}": LineString([T(p['lon'], p['lat']) for p in e['geometry']])
         for e in json.loads((P / 'raw/overpass-oslo.json').read_text())['elements']
         if e['type'] == 'way' and e.get('tags', {}).get('man_made') in ('pier', 'breakwater') and 'geometry' in e}
cands = json.loads((P / 'auto-candidates.json').read_text())
a = esri.copy(); dr = ImageDraw.Draw(a)
for pl in piers.values():
    if pl.intersects(shape({'type': 'Polygon', 'coordinates': [[(FR[0], FR[1]), (FR[2], FR[1]), (FR[2], FR[3]), (FR[0], FR[3])]]})):
        dr.line([px(*q) for q in pl.coords], fill=(255, 230, 0), width=3)
label(dr, 'OSM piers (yellow)'); scalebar(dr)
b = esri.copy(); dr = ImageDraw.Draw(b)
for c in cands:
    g = shape(c['geom'])
    if not g.intersects(shape({'type': 'Polygon', 'coordinates': [[(FR[0], FR[1]), (FR[2], FR[1]), (FR[2], FR[3]), (FR[0], FR[3])]]})): continue
    for pg in getattr(g, 'geoms', [g]): dr.line([px(*q) for q in pg.exterior.coords], fill=(255, 40, 40), width=3)
    x, y = px(c['x'], c['y']); label(dr, c['cid'], (x - 20, y - 11))
label(dr, 'Automatic draft: cluster, buffer, clip to water (red)'); scalebar(dr)
side_by_side(a, b, 'osm-piers-and-draft.jpg')

# 3: endelige polygoner
fc = json.loads((P / 'oslo-bathavner.geojson').read_text())
col = {'smabathavn': (0, 200, 255), 'mulig_smabathavn': (255, 160, 0)}
f3 = esri.copy().convert('RGBA'); ov = Image.new('RGBA', f3.size, (0, 0, 0, 0)); do = ImageDraw.Draw(ov)
labs = []
for f in fc['features']:
    g = ops.transform(T, shape(f['geometry'])); p = f['properties']
    if not g.intersects(shape({'type': 'Polygon', 'coordinates': [[(FR[0], FR[1]), (FR[2], FR[1]), (FR[2], FR[3]), (FR[0], FR[3])]]})): continue
    c = col.get(p['classification'], (255, 255, 255))
    do.polygon([px(*q) for q in g.exterior.coords], fill=c + (70,), outline=c + (255,), width=3)
    q = g.representative_point(); labs.append((px(q.x, q.y), p['id']))
f3 = Image.alpha_composite(f3, ov).convert('RGB'); dr = ImageDraw.Draw(f3)
for (x, y), t in labs: label(dr, t, (x - 50, y - 11))
label(dr, 'Final polygons: blue = smabathavn, orange = mulig_smabathavn'); scalebar(dr)
f3.save(OUT / 'final-polygons.jpg', quality=85)
print('OK', OUT)
