"""Innlem Nordre Follo rev-01 etter eksplisitt brukergodkjenning. Avbryter ved gjentakelse."""
import json,csv,hashlib,datetime,collections
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'data/kommuner/3207-nordre-follo/rev-01'
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=1)+'\n')
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
sp=R/'data/samlet/oslofjorden-bathavner-samlet.geojson';mp=R/'data/samlet/samlet-manifest.json';stp=R/'status.json'
sam=read(sp);fc=read(O/'bathavner.geojson');man=read(mp);st=read(stp)
assert len(sam['features'])==456 and not any(f['properties']['municipality']=='Nordre Follo' for f in sam['features'])
assert len(fc['features'])==2 and all(f['properties']['approval_status']=='til_godkjenning' for f in fc['features'])
oldhash=digest(sam['features']);now=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
for f in fc['features']:f['properties'].update(approval_status='godkjent_av_bruker',approved_utc=now)
fc['description']='Godkjent revisjon 1. Én saltvannshavn (kommunedel av grenseanlegg) og én mulig ferskvannshavn. Kjente usikkerheter beholdt.'
sam['features']+=fc['features'];assert len({f['properties']['id'] for f in sam['features']})==458
man['municipalities'].append(dict(name='Nordre Follo',kommunenummer='3207',features=2,harbours=2,revision=1,delivery_status='godkjent_av_bruker',method_version='1.2',schema_version='1.1'))
man.update(features=458,updated_date=now[:10],classification_counts=dict(collections.Counter(f['properties'].get('classification') or f['properties'].get('status') for f in sam['features'])))
man['method_note']+=' Nordre Follo rev-01 godkjent: 2 polygoner, én saltvannshavn og én mulig ferskvannshavn; Ljansbruket koblet til Oslo med X-HVERVEN-0301-3207. 350 plasser gjelder hele grenseanlegget og skal ikke dobbelttelles.'
m=next(m for m in st['municipalities'] if m['code']=='3207');m.update(status='godkjent_av_bruker',approved_utc=now,candidate_ledger=str((O/'candidate-ledger.json').relative_to(R)))
st.update(updated_utc=now,in_progress='Nordre Follo rev-01 godkjent og innlemmet. Samlet 458 polygoner / 15 kommuner. Ingen neste kommune startet.',next_municipality_started=False)
st['remaining_after_batch']=[r for r in st['remaining_after_batch'] if not r.startswith('Nordre Follo ')]
write(O/'bathavner.geojson',fc)
with (O/'metadata.csv').open('w',encoding='utf-8-sig',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(fc['features'][0]['properties']),delimiter=';',lineterminator='\n');w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in f['properties'].items()} for f in fc['features'])
write(sp,sam);write(mp,man);write(stp,st)
write(O/'approval.json',dict(approved_utc=now,authorization='Bruker: Godkjent',revision=1,polygons=2,known_uncertainties_retained=True,previous_features=456,previous_features_sha256=oldhash,combined_features=458,municipalities=15))
print('Godkjent:',now,'458 polygoner / 15 kommuner')
