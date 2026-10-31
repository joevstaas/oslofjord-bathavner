"""Validate screening coverage, evidence traceability, deduplication and unchanged approved data."""
from pathlib import Path
import json,hashlib,csv,collections
R=Path(__file__).resolve().parents[2];O=R/'data/miljokort/screening-01'
def read(name):return json.loads((O/name).read_text())
rows=read('assessment.json');ev=read('reviewed-evidence.json');ss=read('source-screening.json');s=read('summary.json')
site=json.loads((R/'site/labs/oslofjord-bathavner/data/harbours.geojson').read_text())
keys={f['properties'].get('gid') or f['properties']['hid'] for f in site['features']}
assert len(rows)==len(keys)==664 and {g['group_id'] for g in rows}==keys
assert len({g['group_id'] for g in rows})==664
assert len({e['evidence_id'] for e in ev})==len(ev)
assert all(e['source_id'] in {r['id'] for r in ss} for e in ev)
assert len({r['id'] for r in ss})==len(ss)
for g in rows:
 items=[e for e in ev if e['evidence_id'] in g['evidence_ids']]
 assert all(e['group_id']==g['group_id'] for e in items)
 assert (g['eligibility']!='uavklart')==bool(items)
 assert g['environmental_measures_absent'] is None
 for e in items:assert e['scope'] and e['locator'] and e['claim'] and not e['measured_effect_verified']
for source in ss:
 if source.get('snapshot') and (R/source['snapshot']).exists():assert hashlib.sha256((R/source['snapshot']).read_bytes()).hexdigest()==source['sha256']
assert hashlib.sha256((R/'data/samlet/oslofjorden-bathavner-samlet.geojson').read_bytes()).hexdigest()==s['baseline_sha256']
counts=dict(collections.Counter(g['eligibility'] for g in rows));assert counts==s['counts'];assert s['eligible_lower_bound']==sum(n for k,n in counts.items() if k!='uavklart')
with (O/'assessment.csv').open(encoding='utf-8-sig',newline='') as h:csvrows=list(csv.DictReader(h,delimiter=';'))
assert len(csvrows)==664
for row,g in zip(csvrows,rows):
 for k,v in g.items():assert row[k]==(json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else '' if v is None else str(v)),(g['group_id'],k)
(O/'validation.json').write_text(json.dumps(dict(groups=664,eligible=s['eligible_lower_bound'],counts=counts,unique_group_ids=True,evidence_links_valid=True,source_hashes_match_when_local=True,csv_matches_json=True,approved_baseline_unchanged=True,all_groups_individually_web_searched=False),indent=2)+'\n')
print('Validated:',s['eligible_lower_bound'],'documented candidates / 664 groups;',counts)
