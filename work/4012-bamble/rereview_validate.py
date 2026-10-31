"""Valider rev-02: geometri, stabile ID-er, revisjonsvern, bildekilder, kandidatbeslutninger og CSV."""
import json,csv,hashlib,warnings,runpy
from pathlib import Path
from PIL import Image
from pyproj import Transformer
from shapely.geometry import shape,box,LineString
from shapely.ops import transform,unary_union
warnings.filterwarnings('ignore');P=Path(__file__).parent;R=P.parents[1];O=R/'data/kommuner/4012-bamble/rev-02';OLD=O.parent/'rev-01'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
T=Transformer.from_crs(4326,25833,always_xy=True).transform
fs=read(O/'bathavner.geojson')['features'];old=read(OLD/'bathavner.geojson')['features'];base=read(R/'data/samlet/oslofjorden-bathavner-samlet.geojson')['features'];B=transform(T,shape(read(O/'kommunegrense.geojson')['features'][0]['geometry']))
approval=read(O/'approval.json') if (O/'approval.json').exists() else None
combined=base[:]
if approval:
 base=[f for f in base if f['properties'].get('municipality_code')!='4012']
 assert len(base)==approval['previous_features']
 assert hashlib.sha256(json.dumps(base,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==approval['previous_features_sha256']
 assert all(f in combined for f in fs)
for fn,digest in read(O/'preservation-manifest.json')['protected_sha256'].items():
 if not approval or fn.startswith('data/kommuner/4012-bamble/rev-01/'):
  assert sha(R/fn)==digest,fn
ids=[f['properties']['id'] for f in fs];assert len(ids)==len(set(ids)) and not set(ids)&{f['properties']['id'] for f in base}
byid={f['properties']['id']:f for f in fs}
for f in old:
 n=byid[f['properties']['id']];assert n['geometry']==f['geometry']
 for k,v in f['properties'].items():
  if k not in ({'revision','approval_status','approved_utc'} if approval else {'revision'}):assert n['properties'][k]==v,(f['properties']['id'],k)
shapes=[transform(T,shape(f['geometry'])) for f in fs]
assert all(g.geom_type=='Polygon' and g.is_valid and g.area>25 for g in shapes)
outside=sum(g.difference(B).area for g in shapes);assert outside<.001,outside
overlap=[];base_shapes=[(f['properties']['id'],transform(T,shape(f['geometry']))) for f in base]
for i,(f,g) in enumerate(zip(fs,shapes)):
 for oid,h in base_shapes+[(fs[j]['properties']['id'],shapes[j]) for j in range(i+1,len(fs))]:
  if g.envelope.intersects(h.envelope) and g.intersection(h).area>.01:overlap.append((f['properties']['id'],oid,g.intersection(h).area))
assert not overlap,overlap
rows=list(csv.DictReader((O/'metadata.csv').open(encoding='utf-8-sig'),delimiter=';'));assert len(rows)==len(fs)
used=set()
for f,row in zip(fs,rows):
 p=f['properties'];assert p['revision']==2 and p['approval_status']==('godkjent_av_bruker' if approval else 'til_godkjenning') and p['approved_utc']==(approval['approved_utc'] if approval else None)
 for k,v in p.items():
  expected=json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else '' if v is None else str(v)
  assert row[k]==expected,(p['id'],k)
 used.add(p['image_id']);assert sha(P/'images'/f"{p['image_id']}.jpg")==p['image_sha256']
ledger=read(O/'candidate-ledger.json');lids=[r['candidate_id'] for r in ledger];assert len(lids)==len(set(lids))
for f in fs:assert any(f['properties']['id'] in row['feature_ids'] for row in ledger),f['properties']['id']
D=runpy.run_path(str(P/'rereview_decisions.py'))['D'];detail=read(O/'detail-review.json');assert {r['cid'] for r in detail}==set(D)
for row in detail:
 assert bool(row['feature_ids'])==(row['decision']['action']=='include')
 for pid in row['feature_ids']:assert byid[pid]['properties']['detail_review_id']==row['cid']
report=read(O/'sweep-review.json');assert set(report['all_sheets_reviewed'])==set(range(64));assert len(report['cells'])==255
for i in range(64):assert (P/'qa'/f'sweep-{i:02}.jpg').exists()
manifest=[]
for image_id in sorted(used):
 m=read(P/'images'/f'{image_id}.json');im=Image.open(P/'images'/f'{image_id}.jpg');im.load();assert im.size==(m['width'],m['height']);manifest.append(m)
coasts=[transform(T,LineString([(v['lon'],v['lat']) for v in el['geometry']])).intersection(B.buffer(20)) for el in read(P/'raw/overpass-bamble.json')['elements'] if el.get('tags',{}).get('natural')=='coastline']
coast=unary_union(coasts);tiles=[read(fn) for fn in (P/'images').glob('coast-*.json')];missing=coast.difference(unary_union([box(*m['bbox']) for m in tiles])).length;assert missing<.01
summary=read(O/'summary.json');assert summary['polygons']==len(fs) and summary['harbours']==len({f['properties']['harbour_id'] for f in fs})
if approval:
 site=read(R/'site/labs/oslofjord-bathavner/data/harbours.geojson')['features'];meta=read(R/'site/labs/oslofjord-bathavner/data/meta.json');muns=read(R/'site/labs/oslofjord-bathavner/data/municipalities.geojson')['features']
 assert len(site)==len(combined)==meta['polygons']==approval['combined_features']
 assert {f['properties']['id'] for f in site}=={f['properties']['id'] for f in combined}
 sb=[f for f in site if f['properties']['mun']=='Bamble'];assert len(sb)==59
 assert sum(f['properties']['cls']=='mulig_smabathavn' for f in sb)==14
 bm=next(f['properties'] for f in muns if f['properties']['code']=='4012');assert bm['state']=='mapped' and bm['polygons']==59 and bm['harbours']==53
res=dict(revision=2,approval_status='godkjent_av_bruker' if approval else 'til_godkjenning',polygons=len(fs),harbours=summary['harbours'],possible_harbours=summary['possible_harbours'],uncertain_geometries=summary['uncertain_geometries'],unique_ids=True,valid_geometries=True,outside_municipality_m2=round(outside,6),overlap_issues=overlap,csv_matches_geojson=True,revision01_files_unchanged=True,revision01_geometries_and_ids_preserved=True,approved_baseline_unchanged=True,site_unchanged=not bool(approval),site_matches_approved_data=bool(approval),combined_polygons=len(combined),approved_baseline_polygons=len(base),approved_baseline_municipalities=len({f['properties']['municipality'] for f in base}),source_images_sha256_match=True,source_images_decoded=len(manifest),coast_tiles=len(tiles),osm_coast_length_m=round(coast.length,1),osm_coast_outside_image_coverage_m=round(missing,3),detail_sweep_cells=255,detail_sweep_sheets=64,detail_candidates_decided=len(detail),new_outline_qa_panels=sum(len(r['feature_ids']) for r in detail),visual_qa_record='outline-review.json',inland_systematically_reviewed=False,source_observation_dates_known=False,cloud_obscured_cells=['G024','G028','G030','G031'])
(O/'validation.json').write_text(json.dumps(res,ensure_ascii=False,indent=1)+'\n');(O/'imagery-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=1)+'\n');print(json.dumps(res,ensure_ascii=False))
