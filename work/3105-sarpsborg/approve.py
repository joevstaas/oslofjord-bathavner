"""Innlem Sarpsborg rev-02 etter eksplisitt godkjenning. Bevar alle tidligere godkjente features."""
import json,csv,hashlib,datetime,collections,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'data/kommuner/3105-sarpsborg/rev-02'
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=1)+'\n')
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
assert not (O/'approval.json').exists(),'Godkjenningen er allerede registrert.'
sp=R/'data/samlet/oslofjorden-bathavner-samlet.geojson';mp=R/'data/samlet/samlet-manifest.json';stp=R/'status.json'
sam=read(sp);fc=read(O/'bathavner.geojson');man=read(mp);st=read(stp);previous=sam['features'][:]
assert len(previous)==630 and not any(f['properties'].get('municipality_code')=='3105' for f in previous)
assert len(fc['features'])==62 and all(f['properties']['approval_status']=='til_godkjenning' for f in fc['features'])
now=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ');oldhash=digest(previous)
shutil.copy2(O/'validation.json',O/'validation-before-approval.json')
for f in fc['features']:f['properties'].update(approval_status='godkjent_av_bruker',approved_utc=now)
fc.update(name='Sarpsborg – småbåthavner, godkjent revisjon 2',description='Godkjent revisjon 2: 46 anleggsgrupper / 62 polygoner, inkludert 16 mulige havner og 61 usikre avgrensninger. Ukjent bildedato/drift, seilforeningens 2025-utvidelse og elleve åpne avklaringer beholdes.')
sam['features']+=fc['features'];assert len({f['properties']['id'] for f in sam['features']})==692
assert digest([f for f in sam['features'] if f['properties'].get('municipality_code')!='3105'])==oldhash
man['municipalities'].append(dict(name='Sarpsborg',kommunenummer='3105',features=62,harbours=46,revision=2,delivery_status='godkjent_av_bruker',method_version='1.2',schema_version='1.1'))
man.update(features=692,updated_date=now[:10],classification_counts=dict(collections.Counter(f['properties'].get('classification') or f['properties'].get('status') for f in sam['features'])))
man['method_note']+=' Sarpsborg rev-02 godkjent etter seks brukerinnspill: 46 anleggsgrupper / 62 polygoner, inkludert 16 mulige og 61 usikre avgrensninger. Ukjent bildedato/drift, seilforeningens 2025-utvidelse og elleve åpne avklaringer beholdes. Kapasitetstall er kildeopplysninger, ikke målinger.'
m=next(m for m in st['municipalities'] if m['code']=='3105');m.update(status='godkjent_av_bruker',approved_utc=now)
st.update(updated_utc=now,in_progress='Sarpsborg rev-02 godkjent og innlemmet. Samlet 692 polygoner / 21 kommuner. Kjente usikkerheter og kontrollhull beholdes. Ingen neste kommune startet.',next_municipality_started=False)
st['remaining_after_batch']=[r for r in st['remaining_after_batch'] if not r.startswith('Sarpsborg ')]
write(O/'bathavner.geojson',fc)
with (O/'metadata.csv').open('w',encoding='utf-8-sig',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(fc['features'][0]['properties']),delimiter=';',lineterminator='\n');w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in f['properties'].items()} for f in fc['features'])
write(sp,sam);write(mp,man);write(stp,st)
write(O/'approval.json',dict(approved_utc=now,authorization='Bruker: Godkjent. Commit, push og PR',revision=2,polygons=62,harbours=46,possible_harbours=16,uncertain_geometries=61,known_uncertainties_retained=True,previous_features=630,previous_features_sha256=oldhash,combined_features=692,municipalities=21))
p=O/'README.md';s=p.read_text().replace('revisjon 2 til godkjenning','revisjon 2 godkjent').replace('Leveransen er ikke godkjent eller innlemmet i samledata/nettsted.',f'Brukeren godkjente revisjon 2 {now}. Alle 62 polygonene er innlemmet i samledata; nettstedets kartdata er oppdatert. Kjente usikkerheter er beholdt.').replace('status `til_godkjenning`','status `godkjent_av_bruker`').replace('`validation.json`: gyldige','`validation-before-approval.json`: kontroll før godkjenning. `validation.json`: gyldige');p.write_text(s)
print('Sarpsborg godkjent:',now,'692 polygoner / 21 kommuner')
