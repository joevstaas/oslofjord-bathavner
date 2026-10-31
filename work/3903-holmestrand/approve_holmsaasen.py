"""Innlem godkjent Holmsåsen-supplement uten å endre tidligere features."""
import json,csv,hashlib,datetime,collections
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'data/kommuner/3903-holmestrand/rev-02-holmsaasen'
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=1)+'\n')
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
assert not (O/'approval.json').exists(),'Allerede innlemmet'
sp=R/'data/samlet/oslofjorden-bathavner-samlet.geojson';mp=R/'data/samlet/samlet-manifest.json';stp=R/'status.json'
sam=read(sp);fc=read(O/'bathavner.geojson');man=read(mp);st=read(stp);old=sam['features'][:];oldhash=digest(old)
assert len(old)==758 and len(fc['features'])==2
assert not ({f['properties']['id'] for f in old}&{f['properties']['id'] for f in fc['features']})
now=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
for f in fc['features']:f['properties'].update(approval_status='godkjent_av_bruker',approved_utc=now)
sam['features']+=fc['features'];assert digest(sam['features'][:758])==oldhash
m=next(m for m in man['municipalities'] if m['kommunenummer']=='3903');m['features']=16;m['harbours']=len({f['properties']['harbour_id'] for f in sam['features'] if f['properties']['municipality']=='Holmestrand'});m['supplements']=['data/kommuner/3903-holmestrand/rev-02-holmsaasen']
man.update(features=760,updated_date=now[:10],classification_counts=dict(collections.Counter(f['properties'].get('classification') or f['properties'].get('status') for f in sam['features'])))
man['method_note']+=' Holmsåsen-supplement godkjent: to nye polygoner / to grupper, hvorav én mulig. Holmestrand har 16 polygoner. Ukjent bildedato, operatører og geometriusikkerhet beholdes.'
m=next(m for m in st['municipalities'] if m['code']=='3903');m['polygons']=16;m['supplements']=[dict(result='data/kommuner/3903-holmestrand/rev-02-holmsaasen/bathavner.geojson',metadata='data/kommuner/3903-holmestrand/rev-02-holmsaasen/metadata.csv',approved_utc=now,polygons=2)]
a=next(a for a in st['area_reviews'] if a['area']=='Holmsåsen campingbukt');a.update(status='godkjent_av_bruker',approved_utc=now,combined_unchanged=False)
st.update(updated_utc=now,in_progress='Holmsåsen-supplement godkjent og innlemmet: to nye polygoner. Samlet 760 polygoner / 22 kommuner. Kjente usikkerheter beholdes.')
write(O/'bathavner.geojson',fc)
with (O/'metadata.csv').open('w',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(fc['features'][0]['properties']),delimiter=';',lineterminator='\n');w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in f['properties'].items()} for f in fc['features'])
write(sp,sam);write(mp,man);write(stp,st)
write(O/'approval.json',dict(approved_utc=now,authorization='Bruker: Innlem de to nye polygonene i samlefilen',polygons=2,groups=2,possible_groups=1,known_uncertainties_retained=True,previous_features=758,previous_features_sha256=oldhash,combined_features=760,municipalities=22))
s=read(O/'summary.json');s.update(status='godkjent_av_bruker',approved_utc=now,combined_unchanged=False,website_unchanged=False);write(O/'summary.json',s)
p=O/'README.md';s=p.read_text().replace('til godkjenning','godkjent og innlemmet').replace('Godkjent rev-01, samlefil og nettsted er uendret; supplementet venter på brukergodkjenning.','Godkjent rev-01 er uendret. Brukeren godkjente innlemming av begge polygonene; samlet fil og lokale kartdata er oppdatert til 760 polygoner / 22 kommuner.');p.write_text(s)
print('Innlemmet: 760 polygoner / 22 kommuner; tidligere 758 features uendret.')
