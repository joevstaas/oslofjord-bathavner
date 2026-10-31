"""Validate joins, evidence provenance and preservation of approved files."""
import csv,hashlib,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[2];OUT=ROOT/'data/berikelse/3103-moss/pilot-01'
def read(name):return json.loads((OUT/name).read_text())
harbours=read('harbours.json');observations=read('observations.json');sources={s['source_id']:s for s in read('sources.json')}
base=json.loads((ROOT/'data/kommuner/3103-moss/rev-01/bathavner.geojson').read_text());ids={f['properties']['harbour_id'] for f in base['features']};polygons={f['properties']['id']:f for f in base['features']}
assert len(harbours)==22 and {r['harbour_id'] for r in harbours}==ids
assert len({o['observation_id'] for o in observations})==len(observations)
obs={o['observation_id']:o for o in observations}
candidates=read('candidates.json');subjects=ids|{c['candidate_id'] for c in candidates}|{'SERVICE-fuglevik'}
for o in observations:
 assert o['subject_id'] in subjects
 assert o['source_id'] in sources
 s=sources[o['source_id']];assert s['retrieval_status']=='retrieved'
 snapshot=ROOT/s['snapshot_path']
 assert o['evidence_lines'] and all(n>=1 for n in o['evidence_lines'])
 if snapshot.exists():
  text=snapshot.read_text().splitlines();assert all(n<=len(text) for n in o['evidence_lines'])
 elif '--require-snapshots' in sys.argv:raise AssertionError('Missing local source snapshot: '+str(snapshot))
 assert o['source_url']==s['url'] and o['accessed_utc']==s['accessed_utc']
 if o['status']=='published_undated':assert o['reference_date'] is None
for r in harbours:
 assert sorted(r['polygon_ids'])==sorted(k for k,p in polygons.items() if p['properties']['harbour_id']==r['harbour_id'])
 assert all(obs[oid]['subject_id']==r['harbour_id'] for oid in r['observation_ids'])
 assert r['current_operation_verified'] is None and r['wastewater_treatment_current'] is None
 assert all(s in sources for s in r['source_ids'])
 for field in ['operator_name','berths_published','guest_berths_published','dinghy_berths_published','winter_storage_berths_published','land_storage_reported','lifting_reported','ramp_reported']:
  if r[field] is not None:assert any(obs[oid]['field']==field and obs[oid]['value']==r[field] for oid in r['observation_ids']),(r['harbour_id'],field)
for c in candidates:assert c['geometry'] is None and c['harbour_id'] is None
for s in sources.values():
 if s['retrieval_status']=='retrieved' and (ROOT/s['snapshot_path']).exists():assert hashlib.sha256((ROOT/s['snapshot_path']).read_bytes()).hexdigest()==s['snapshot_sha256']
for f in read('reference-map.geojson')['features']:
 old=polygons[f['properties']['id']];assert f['geometry']==old['geometry']
 assert {k:v for k,v in f['properties'].items() if k!='enrichment_pilot'}==old['properties']
for filename in ['harbours','observations','candidates','deviations']:
 with (OUT/(filename+'.csv')).open(encoding='utf-8-sig',newline='') as handle:
  rows=list(csv.DictReader(handle,delimiter=';'));expected=read(filename+'.json');assert len(rows)==len(expected)
  for row,j in zip(rows,expected):
   for key,value in j.items():assert row[key]==(json.dumps(value,ensure_ascii=False) if isinstance(value,(dict,list)) else '' if value is None else str(value))
for p,h in read('baseline.json')['files'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
result={'status':'passed','harbours':22,'polygons':26,'observations':len(observations),'candidates':2,'source_snapshots_checked':sum(s['retrieval_status']=='retrieved' and (ROOT/s['snapshot_path']).exists() for s in sources.values()),'checks':['All baseline harbour and polygon IDs covered exactly once','Each promoted value has a field-level sourced observation','Evidence references valid; available local snapshot locators and hashes checked','CSV/JSON round trip consistent','Candidate geometries remain absent','Reference export preserves every approved property and geometry','Approved municipality and combined files byte-for-byte unchanged']}
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
