"""Innlem godkjent batch (Bærum, Asker, Lier, Drammen, Oslo) i samlefilen.
Skriver data/kommuner/<kode>-<navn>/rev-01/, oppdaterer samlefil, manifest og status.json.
Kjøres én gang etter brukerens godkjenning; avbryter hvis en kommune allerede finnes i samlefilen.
Merk: kjøringen 2026-10-30 stoppet ved klassifiseringstellingen (pilotene mangler classification) etter at samlefilen var skrevet;
manifest og status ble fullført i et eget steg ved å legge nye tellinger til de eksisterende."""
import json, csv, shutil
from datetime import datetime, timezone
from pathlib import Path
from pyproj import Transformer
from shapely.geometry import shape
from shapely import ops

R = Path(__file__).resolve().parents[1]
NOW = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
BATCH = [('3201', 'baerum', 'Bærum'), ('3203', 'asker', 'Asker'), ('3312', 'lier', 'Lier'),
         ('3301', 'drammen', 'Drammen'), ('0301', 'oslo', 'Oslo')]
COPY = ['auto-candidates.json', 'candidate-ledger.csv', 'candidate-ledger.json', 'coverage.json', 'decisions.py',
        'decisions_lib.py', 'neighbour-pending.json', 'source-notes.json', 'summary.json', 'timing.json', 'validation.json']
F = Transformer.from_crs(4326, 25833, always_xy=True).transform

def rd(p): return json.loads(p.read_text())
def wr(p, o): p.write_text(json.dumps(o, ensure_ascii=False, indent=1) + '\n')
def write_csv(path, feats):
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(feats[0]['properties']), delimiter=';'); w.writeheader()
        w.writerows({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v for k, v in x['properties'].items()} for x in feats)

sam_p = R / 'data/samlet/oslofjorden-bathavner-samlet.geojson'; man_p = R / 'data/samlet/samlet-manifest.json'; st_p = R / 'status.json'
sam, man, st = rd(sam_p), rd(man_p), rd(st_p)
present = {f['properties']['municipality'] for f in sam['features']}
assert not present & {n for _, _, n in BATCH}, 'Batch finnes allerede i samlefilen'

new = []
for code, slug, name in BATCH:
    w = R / 'work' / f'{code}-{slug}'
    fc = rd(w / f'{slug}-bathavner.geojson')
    assert all(f['properties']['approval_status'] == 'til_godkjenning' for f in fc['features'])
    for f in fc['features']:
        f['properties'].update(approval_status='godkjent_av_bruker', approved_utc=NOW)
    wr(w / f'{slug}-bathavner.geojson', fc); write_csv(w / f'{slug}-metadata.csv', fc['features'])
    out = R / 'data/kommuner' / f'{code}-{slug}' / 'rev-01'; out.mkdir(parents=True, exist_ok=False)
    wr(out / 'bathavner.geojson', dict(type='FeatureCollection', name=f'{name} – godkjent uttrekk fra samlefil', features=fc['features']))
    write_csv(out / 'metadata.csv', fc['features'])
    for fn in COPY:
        if (w / fn).exists(): shutil.copy2(w / fn, out / fn)
    new += fc['features']
    s = rd(w / 'summary.json')
    man['municipalities'].append(dict(name=name, kommunenummer=code, features=len(fc['features']), harbours=s['harbours'], revision=1,
                                      delivery_status='godkjent_av_bruker', method_version='1.2', schema_version='1.1'))
    m = next(x for x in st['municipalities'] if x['code'] == code)
    m.update(status='godkjent_av_bruker', approved_utc=NOW, work_dir=f'work/{code}-{slug}',
             result=f'data/kommuner/{code}-{slug}/rev-01/bathavner.geojson', metadata=f'data/kommuner/{code}-{slug}/rev-01/metadata.csv',
             candidate_ledger=f'data/kommuner/{code}-{slug}/rev-01/candidate-ledger.json',
             neighbour_pending=f'data/kommuner/{code}-{slug}/rev-01/neighbour-pending.json')

# kontroll: ID-kollisjon og overlapp mot eksisterende og innbyrdes
ids = [f['properties']['id'] for f in sam['features'] + new]
assert len(ids) == len(set(ids)), 'ID-kollisjon'
old = [ops.transform(F, shape(f['geometry'])) for f in sam['features']]
ng = [ops.transform(F, shape(f['geometry'])) for f in new]
ov = [(new[i]['properties']['id'], round(g.intersection(o).area, 2)) for i, g in enumerate(ng) for o in old + ng[i + 1:] if g.intersection(o).area > 1]
assert not ov, ov

sam['features'] += new; wr(sam_p, sam)
cc = {}
for f in sam['features']: cc[f['properties']['classification']] = cc.get(f['properties']['classification'], 0) + 1
man.update(features=len(sam['features']), classification_counts=cc, updated_date=NOW[:10],
           method_note=man['method_note'] + ' Batch Bærum/Asker/Lier/Drammen/Oslo: godkjent samlet revisjon 1, metode 1.2; Bærum 42/49, Asker 53/60, Lier 2/2, Drammen 17/19, Oslo 32/36 anlegg/polygoner; grenseanlegg klippet med cross_municipality_group_id; åpne kandidater i neighbour-pending beholdt.')
wr(man_p, man)
st['batch']['approved_utc'] = NOW
st.update(updated_utc=NOW, next_municipality_started=False,
          in_progress='Batch Bærum–Asker–Lier–Drammen–Oslo godkjent og innlemmet. Neste batch (Nordre Follo, Nesodden, Frogn, Vestby) startes kun etter brukerens beskjed.')
wr(st_p, st)
print(len(sam['features']), 'polygoner,', len({f['properties']['municipality'] for f in sam['features']}), 'kommuner,', NOW)
