"""Bygg kompakte data til flyover-siden (site/labs/oslofjord-bathavner/data/).
Leser godkjent samlefil, status.json og separat Moss-berikelsespilot; kommunegrenser hentes fra Kartverket og caches i cache/."""
import json, urllib.request
from pathlib import Path
from pyproj import Transformer
from shapely.geometry import shape, mapping
from shapely import ops

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'site/labs/oslofjord-bathavner/data'; OUT.mkdir(parents=True, exist_ok=True)
CACHE = ROOT / 'cache/kommunegrenser'; CACHE.mkdir(parents=True, exist_ok=True)
F = Transformer.from_crs(4326, 25833, always_xy=True).transform
B = Transformer.from_crs(25833, 4326, always_xy=True).transform

# klassifisering: pilotene (Holmestrand/Horten) har bare status-felt og harmoniseres ikke her
LEGACY = {'kart_og_kilde': 'pilot', 'ma_avklares': 'mulig_smabathavn'}
METHOD = [('manuell_digitalisering_georeferert_topografisk', 'Manual, topographic map'),
          ('manuell', 'Manual, aerial image'), ('osm_pirer', 'OSM piers + image review'), ('osm_polygon', 'OSM outline + image review')]

def basis_en(b):
    """Grov engelsk oversettelse av classification_basis til visning; originalverdien finnes i datasettet."""
    if not b: return 'Map and sources (pilot)'
    if 'uklar' in b or 'ukjent' in b or 'ikke_dokumentert' in b or 'ikke_verifisert' in b: return 'Several piers; shared use or capacity unclear'
    if 'gjeste' in b: return 'Documented guest harbour'
    doc = any(w in b for w in ('dokument', 'kommunalt', 'operator', 'avfallsplan', 'registrert', 'forening', 'marina'))
    vis = 'synlige' in b or 'utrigger' in b or 'brygge' in b
    if doc and vis: return 'Documented operator + visible berths'
    if doc: return 'Documented harbour with permanent berths'
    return 'At least ~10 visible berths in one facility'

def rnd(c): return [rnd(x) for x in c] if isinstance(c[0], (list, tuple)) else [round(c[0], 6), round(c[1], 6)]

fc = json.loads((ROOT / 'data/samlet/oslofjorden-bathavner-samlet.geojson').read_text())
feats = []
for f in fc['features']:
    p = f['properties']
    cls = p.get('classification') or LEGACY.get(p.get('status'), 'mulig_smabathavn')
    meth = next((v for k, v in METHOD if p.get('method', '').startswith(k)), p.get('method', ''))
    osm = p.get('osm_ids') or ([p['osm_id']] if p.get('osm_id') else [])
    g = shape(f['geometry'])
    feats.append(dict(type='Feature', id=len(feats), geometry=dict(type='Polygon', coordinates=rnd(f['geometry']['coordinates'])), properties=dict(
        id=p['id'], hid=p['harbour_id'], name=p['name'], mun=p['municipality'], cls=cls,
        basis=('Shared berthing area; permanent berths or operation unverified' if p.get('municipality_code') in ('4012', '3105', '4001') and cls == 'mulig_smabathavn' else 'Shared jetties; permanent berth count or organisation unclear' if p.get('municipality_code') == '3216' and cls == 'mulig_smabathavn' else 'Shared visitor jetties; permanent berth count unclear' if p.get('municipality_code') == '3214' and cls == 'mulig_smabathavn' else 'Shared boat jetty; permanent berth count and operator link unclear' if (p.get('candidate_id') == 'NF002' and p.get('municipality_code') == '3207') or (p.get('municipality_code') == '3212' and cls == 'mulig_smabathavn') else basis_en(p.get('classification_basis'))), area=round(p.get('area_m2') or 0),
        berths=(None if p.get('cross_municipality_group_id') else p.get('berth_count_published')), method=meth,
        gid=p.get('cross_municipality_group_id') or p['harbour_id'],
        unc=bool(p.get('needs_orthophoto_review')), clip=bool(p.get('municipality_clipped')),
        osm=osm[0] if osm else None, nosm=len(osm), note=(p.get('note') or '')[:220],
        lon=round(g.representative_point().x, 6), lat=round(g.representative_point().y, 6))))
(OUT / 'harbours.geojson').write_text(json.dumps(dict(type='FeatureCollection', features=feats), ensure_ascii=False, separators=(',', ':')))

# kommuner: godkjente + gjenstående i prosjektomfanget
st = json.loads((ROOT / 'status.json').read_text())
muns = [(m['code'], m['name'], 'mapped') for m in st['municipalities'] if m['status'] != 'til_godkjenning']
muns += [(r.split()[-1], ' '.join(r.split()[:-1]), 'remaining') for r in st['remaining_after_batch'] if not r.startswith('Ås')]
# kystnære etikettpunkter for kommuner som ikke er kartlagt ennå
LABEL = {'3216': (10.70, 59.53), '3214': (10.62, 59.665), '3212': (10.64, 59.80), '3207': (10.79, 59.80),
         '3110': (10.98, 59.07), '3105': (11.08, 59.25), '3101': (11.37, 59.12), '4001': (9.66, 59.11), '4012': (9.72, 59.00)}
existing_path = OUT / 'municipalities.geojson'
existing = {f['properties']['code']: f for f in json.loads(existing_path.read_text())['features']} if existing_path.exists() else {}
bfeats = []
for code, name, state in muns:
    cf = CACHE / f'{code}.json'
    if not cf.exists() and code not in existing:
        req = urllib.request.Request(f'https://api.kartverket.no/kommuneinfo/v1/kommuner/{code}/omrade?utkoordsys=4326', headers={'User-Agent': 'oslofjord-bathavner'})
        cf.write_bytes(urllib.request.urlopen(req, timeout=60).read())
    if code in existing:
        # Bevar publiserte kommuneomriss; bare status/tellinger endres.
        geom = existing[code]['geometry']
        g = ops.transform(F, shape(geom))
    else:
        j = json.loads(cf.read_text()); geom = j.get('omrade') or j
        g = ops.transform(F, shape(geom)).simplify(40).buffer(0)
    n = sum(1 for x in feats if x['properties']['mun'] == name)
    h = len({x['properties']['hid'] for x in feats if x['properties']['mun'] == name})
    pts = [(x['properties']['lon'], x['properties']['lat']) for x in feats if x['properties']['mun'] == name]
    lx, ly = (sum(a for a, _ in pts) / len(pts), sum(b for _, b in pts) / len(pts)) if pts else LABEL.get(code, B(*g.representative_point().coords[0]))
    bfeats.append(dict(type='Feature', geometry=(existing[code]['geometry'] if code in existing else json.loads(json.dumps(mapping(ops.transform(B, g))))),
                       properties=dict(code=code, name=name, state=state, polygons=n, harbours=h, lx=round(lx, 5), ly=round(ly, 5))))
for b in bfeats: b['geometry']['coordinates'] = rnd(b['geometry']['coordinates'])
(OUT / 'municipalities.geojson').write_text(json.dumps(dict(type='FeatureCollection', features=bfeats), ensure_ascii=False, separators=(',', ':')))
print(len(feats), 'polygoner;', len(bfeats), 'kommuner;', {p.name: f'{p.stat().st_size/1e6:.2f} MB' for p in OUT.glob('*.geojson')})

# nøkkeltall til metodepanelet (bare godkjente kommuner)
appr = [m for m in st['municipalities'] if m['status'] != 'til_godkjenning']
ledgers = [json.loads((ROOT / m['candidate_ledger']).read_text()) for m in appr if m.get('candidate_ledger')]
timed = [m['elapsed_wall_seconds'] for m in appr if m.get('elapsed_wall_seconds')]
meta = dict(polygons=len(feats), harbours=len({f['properties']['gid'] for f in feats}), municipalities=len(appr),
            candidates_logged=sum(len(l) for l in ledgers), ledger_municipalities=len(ledgers),
            wall_hours=round(sum(timed) / 3600, 1), timed_municipalities=len(timed),
            updated=json.loads((ROOT / 'data/samlet/samlet-manifest.json').read_text())['updated_date'])
(OUT / 'meta.json').write_text(json.dumps(meta, ensure_ascii=False))
print(meta)

# Separat kildeberikelse; endrer ikke godkjente geometrier eller kartklassifisering.
from build_harbour_enrichment import main as build_enrichment
build_enrichment()
