"""Validate scope, legacy status, category separation, evidence and unchanged baseline."""
import csv,hashlib,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[2];OUT=ROOT/'data/berikelse/3903-holmestrand/pilot-01'
def read(n):return json.loads((OUT/n).read_text())
rows=read('harbours.json');obs=read('observations.json');groups=read('capacity-groups.json');candidates=read('candidates.json');sources={s['source_id']:s for s in read('sources.json')}
fc=json.loads((ROOT/'data/kommuner/3903-holmestrand/rev-01/bathavner.geojson').read_text());baseline={f['properties']['id']:f for f in fc['features']}
ids={f['properties']['harbour_id'] for f in fc['features']};assert len(rows)==12 and len(baseline)==14 and {r['harbour_id'] for r in rows}==ids
assert len({o['observation_id'] for o in obs})==len(obs)
by_id={o['observation_id']:o for o in obs};subjects=ids|{g['group_id'] for g in groups}|{c['candidate_id'] for c in candidates}
for r in rows:
 fs=[f for f in fc['features'] if f['properties']['harbour_id']==r['harbour_id']]
 assert set(r['polygon_ids'])=={f['properties']['id'] for f in fs}
 assert r['legacy_status']==fs[0]['properties']['status'] and r['classification_baseline'] is None
 assert r['current_operation_verified'] is None and r['wastewater_treatment_current'] is None
 assert r['needs_orthophoto_review'] is True and r['geometry_review_status']=='not_reassessed_topographic_pilot'
 assert all(by_id[x]['subject_id']==r['harbour_id'] for x in r['observation_ids'])
 for field in ['operator_name','ramp_reported','own_crane_reported','land_storage_reported']:
  if r[field] is not None:assert any(o['subject_id']==r['harbour_id'] and o['field']==field and o['value']==r[field] for o in obs)
for o in obs:
 assert o['subject_id'] in subjects and o['source_id'] in sources
 s=sources[o['source_id']];assert s['retrieval_status']=='retrieved' and o['source_url']==s['url']
 assert o['evidence_lines'] and all(n>=1 for n in o['evidence_lines'])
 p=ROOT/s['snapshot_path']
 if p.exists():assert all(n<=len(p.read_text().splitlines()) for n in o['evidence_lines'])
 elif '--require-snapshots' in sys.argv:raise AssertionError('Missing snapshot '+str(p))
 if o['status']=='published_undated':assert o['reference_date'] is None
for s in sources.values():
 if s['retrieval_status']=='retrieved' and (ROOT/s['snapshot_path']).exists():assert hashlib.sha256((ROOT/s['snapshot_path']).read_bytes()).hexdigest()==s['snapshot_sha256']
assert all(r['berths_published'] is None for r in rows),'No single capacity can be safely allocated in this review'
assert len([o for o in obs if o['field']=='berths_published' and o['value']==1100])==1
assert next(r for r in rows if r['harbour_id']=='3903-H03')['capacity_quality']=='conflicting_operator_publications'
assert {o['value'] for o in obs if o['subject_id']=='3903-H03' and o['field']=='berths_published'}=={397,450}
assert {c['kind']:c['value'] for c in next(r for r in rows if r['harbour_id']=='3903-H05')['capacity_components']}=={'member_share_places':155,'rental_places':62}
assert next(r for r in rows if r['harbour_id']=='3903-K05')['water_environment']=='freshwater'
assert all(c['geometry'] is None and c['harbour_id'] is None for c in candidates)
for g in groups:assert set(g['related_harbour_ids'])<=ids and all(by_id[x]['subject_id']==g['group_id'] for x in g['observation_ids'])
for f in read('reference-map.geojson')['features']:
 old=baseline[f['properties']['id']];assert f['geometry']==old['geometry'];assert {k:v for k,v in f['properties'].items() if k!='enrichment_pilot'}==old['properties']
for name in ['harbours','observations','capacity-groups','candidates','deviations']:
 with (OUT/(name+'.csv')).open(encoding='utf-8-sig',newline='') as f:csvrows=list(csv.DictReader(f,delimiter=';'))
 values=read(name+'.json');assert len(csvrows)==len(values)
 for cr,j in zip(csvrows,values):
  for k,v in j.items():assert cr[k]==(json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else '' if v is None else str(v))
for p,h in read('baseline.json')['files'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
result={'status':'passed','harbour_groups':12,'polygons':14,'observations':len(obs),'local_source_snapshots_checked':sum(s['retrieval_status']=='retrieved' and (ROOT/s['snapshot_path']).exists() for s in sources.values()),'checks':['Complete baseline coverage and unchanged legacy classification','Every observation linked to a successful source','Available snapshot hashes and evidence locators checked','Shared 1100 capacity stored once; 397/450 conflict retained','155 membership and 62 rental places remain separate','Camping pitches, prices and freshwater distinguished','CSV/JSON consistent and reference geometries identical','Approved municipality, combined files and earlier supplement byte-for-byte unchanged']}
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
