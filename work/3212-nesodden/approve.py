"""Innlem Nesodden rev-01 etter eksplisitt brukergodkjenning. Avbryter ved gjentakelse."""
import json,csv,hashlib,datetime,collections
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'data/kommuner/3212-nesodden/rev-01'
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=1)+'\n')
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
sp=R/'data/samlet/oslofjorden-bathavner-samlet.geojson';mp=R/'data/samlet/samlet-manifest.json';stp=R/'status.json'
sam=read(sp);fc=read(O/'bathavner.geojson');man=read(mp);st=read(stp)
assert len(sam['features'])==458 and not any(f['properties']['municipality']=='Nesodden' for f in sam['features'])
assert len(fc['features'])==11 and all(f['properties']['approval_status']=='til_godkjenning' for f in fc['features'])
oldhash=digest(sam['features']);now=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
for f in fc['features']:f['properties'].update(approval_status='godkjent_av_bruker',approved_utc=now)
fc['description']='Godkjent revisjon 1: 11 anleggsgrupper og 11 polygoner, inkludert 3 mulige havner. Kjente usikkerheter og åpne kandidater beholdt.'
fc['name']='Nesodden – småbåthavner, godkjent revisjon 1'
sam['features']+=fc['features'];assert len({f['properties']['id'] for f in sam['features']})==469
man['municipalities'].append(dict(name='Nesodden',kommunenummer='3212',features=11,harbours=11,revision=1,delivery_status='godkjent_av_bruker',method_version='1.2',schema_version='1.1'))
man.update(features=469,updated_date=now[:10],classification_counts=dict(collections.Counter(f['properties'].get('classification') or f['properties'].get('status') for f in sam['features'])))
man['method_note']+=' Nesodden rev-01 godkjent: 11 anleggsgrupper / 11 polygoner, inkludert 3 mulige og 5 usikre avgrensninger. Bomansvik og øvrige avklaringer beholdes. Plasstall er kildeopplysninger, ikke målinger.'
m=next(m for m in st['municipalities'] if m['code']=='3212');m.update(status='godkjent_av_bruker',approved_utc=now,candidate_ledger=str((O/'candidate-ledger.json').relative_to(R)))
st.update(updated_utc=now,in_progress='Nesodden rev-01 godkjent og innlemmet. Samlet 469 polygoner / 16 kommuner. Ingen neste kommune startet.',next_municipality_started=False)
st['remaining_after_batch']=[r for r in st['remaining_after_batch'] if not r.startswith('Nesodden ')]
write(O/'bathavner.geojson',fc)
with (O/'metadata.csv').open('w',encoding='utf-8-sig',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(fc['features'][0]['properties']),delimiter=';',lineterminator='\n');w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in f['properties'].items()} for f in fc['features'])
write(sp,sam);write(mp,man);write(stp,st)
write(O/'approval.json',dict(approved_utc=now,authorization='Bruker: Godkjent',revision=1,polygons=11,known_uncertainties_retained=True,previous_features=458,previous_features_sha256=oldhash,combined_features=469,municipalities=16))
print('Godkjent:',now,'469 polygoner / 16 kommuner')
