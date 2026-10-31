"""Innlem Porsgrunn rev-01 etter eksplisitt godkjenning. Bevar alle tidligere godkjente features."""
import json,csv,hashlib,datetime,collections,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'data/kommuner/4001-porsgrunn/rev-01'
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=1)+'\n')
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
assert not (O/'approval.json').exists(),'Godkjenningen er allerede registrert.'
sp=R/'data/samlet/oslofjorden-bathavner-samlet.geojson';mp=R/'data/samlet/samlet-manifest.json';stp=R/'status.json'
sam=read(sp);fc=read(O/'bathavner.geojson');man=read(mp);st=read(stp);previous=sam['features'][:]
assert len(previous)==760 and not any(f['properties'].get('municipality_code')=='4001' for f in previous)
assert len(fc['features'])==56 and all(f['properties']['approval_status']=='til_godkjenning' for f in fc['features'])
now=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ');oldhash=digest(previous)
shutil.copy2(O/'validation.json',O/'validation-before-approval.json')
for f in fc['features']:f['properties'].update(approval_status='godkjent_av_bruker',approved_utc=now)
fc.update(name='Porsgrunn – småbåthavner, godkjent revisjon 1',description='Godkjent revisjon 1: 28 anleggsgrupper / 56 polygoner, inkludert 3 mulige havner og 56 usikre avgrensninger. Ukjent bildedato/drift, tolv åpne avklaringer og ufullstendig innlandskartlegging beholdes.')
sam['features']+=fc['features'];assert len({f['properties']['id'] for f in sam['features']})==816
assert digest([f for f in sam['features'] if f['properties'].get('municipality_code')!='4001'])==oldhash
man['municipalities'].append(dict(name='Porsgrunn',kommunenummer='4001',features=56,harbours=28,revision=1,delivery_status='godkjent_av_bruker',method_version='1.2',schema_version='1.1'))
man.update(features=816,updated_date=now[:10],classification_counts=dict(collections.Counter(f['properties'].get('classification') or f['properties'].get('status') for f in sam['features'])))
man['method_note']+=' Porsgrunn rev-01 godkjent: 28 anleggsgrupper / 56 polygoner, inkludert 3 mulige og 56 usikre avgrensninger. Ukjent bildedato/drift, tolv åpne avklaringer og ufullstendig innlandskartlegging beholdes. Kapasitetstall er kildeopplysninger, ikke målinger.'
m=next(m for m in st['municipalities'] if m['code']=='4001');m.update(status='godkjent_av_bruker',approved_utc=now)
st.update(updated_utc=now,in_progress='Porsgrunn rev-01 godkjent og innlemmet. Samlet 816 polygoner / 23 kommuner. Kjente usikkerheter og kontrollhull beholdes. Ingen neste kommune startet.',next_municipality_started=False)
st['remaining_after_batch']=[r for r in st['remaining_after_batch'] if not r.startswith('Porsgrunn ')]
write(O/'bathavner.geojson',fc)
with (O/'metadata.csv').open('w',encoding='utf-8-sig',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(fc['features'][0]['properties']),delimiter=';',lineterminator='\n');w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in f['properties'].items()} for f in fc['features'])
write(sp,sam);write(mp,man);write(stp,st)
write(O/'approval.json',dict(approved_utc=now,authorization='Bruker: Godkjent',revision=1,polygons=56,harbours=28,possible_harbours=3,uncertain_geometries=56,known_uncertainties_retained=True,previous_features=760,previous_features_sha256=oldhash,combined_features=816,municipalities=23))
p=O/'README.md';s=p.read_text().replace('rev-01 til godkjenning','rev-01 godkjent').replace('Ikke innlemmet i samlefil eller nettsted.',f'Brukeren godkjente revisjonen {now}. Alle 56 polygonene er innlemmet i samledata og nettstedets lokale kartdata. Kjente usikkerheter er beholdt.');p.write_text(s)
print('Porsgrunn godkjent',now,'816 polygoner / 23 kommuner')
