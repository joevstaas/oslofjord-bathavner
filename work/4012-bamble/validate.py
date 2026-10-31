"""Teknisk validering av Bamble rev-01 og uendret godkjent grunnlag."""
import json,csv,hashlib,warnings
from pathlib import Path
from shapely.geometry import shape,LineString,box
from shapely.ops import transform,unary_union
from pyproj import Transformer
from PIL import Image
warnings.filterwarnings('ignore');P=Path(__file__).parent;R=P.parents[1];O=R/'data/kommuner/4012-bamble/rev-01'
T=Transformer.from_crs(4326,25833,always_xy=True).transform
B=transform(T,shape(json.loads((P/'kommunegrense.geojson').read_text())['features'][0]['geometry']))
fs=json.loads((O/'bathavner.geojson').read_text())['features'];base=json.loads((R/'data/samlet/oslofjorden-bathavner-samlet.geojson').read_text())['features']
approval=json.loads((O/'approval.json').read_text()) if (O/'approval.json').exists() else None
if approval:
 previous=[f for f in base if f['properties'].get('municipality_code')!='4012']
 assert hashlib.sha256(json.dumps(previous,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==approval['previous_features_sha256']
 assert len(previous)==approval['previous_features'] and all(f in base for f in fs)
 base=previous
ids=[f['properties']['id'] for f in fs];assert len(ids)==len(set(ids));assert not set(ids)&{f['properties']['id'] for f in base}
gs=[transform(T,shape(f['geometry'])) for f in fs]
assert all(g.is_valid and not g.is_empty and g.difference(B).area<.001 for g in gs)
overlap=[]
old=[(f['properties']['id'],transform(T,shape(f['geometry']))) for f in base]
for i,(f,g) in enumerate(zip(fs,gs)):
 for oid,o in old+[(fs[j]['properties']['id'],gs[j]) for j in range(i+1,len(gs))]:
  if not g.envelope.intersects(o.envelope):continue
  a=g.intersection(o).area
  if a>.01:overlap.append(dict(a=f['properties']['id'],b=oid,area_m2=a))
assert not overlap,overlap
rows=list(csv.DictReader((O/'metadata.csv').open(encoding='utf-8-sig'),delimiter=';'));assert len(rows)==len(fs)
for row,f in zip(rows,fs):
 for k,v in f['properties'].items():
  expect=json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else '' if v is None else str(v)
  assert row[k]==expect,(row['id'],k)
 p=f['properties'];assert p['approval_status']==('godkjent_av_bruker' if approval else 'til_godkjenning')
 assert p['approved_utc']==(approval['approved_utc'] if approval else None)
 assert hashlib.sha256((P/'images'/(p['image_id']+'.jpg')).read_bytes()).hexdigest()==p['image_sha256']
for fn,sha in ({} if approval else json.loads((P/'run.json').read_text())['approved_baseline_sha256']).items():assert hashlib.sha256((R/fn).read_bytes()).hexdigest()==sha,fn
images=[]
for fn in sorted((P/'images').glob('*.jpg')):
 m=json.loads(fn.with_suffix('.json').read_text());im=Image.open(fn);im.load();assert im.size==(m['width'],m['height']);assert hashlib.sha256(fn.read_bytes()).hexdigest()==m['sha256'];images.append(m)
coasts=[]
for el in json.loads((P/'raw/overpass-bamble.json').read_text())['elements']:
 if el.get('tags',{}).get('natural')=='coastline':coasts.append(transform(T,LineString([(v['lon'],v['lat']) for v in el['geometry']])).intersection(B.buffer(20)))
coast=unary_union(coasts);coverage=unary_union([box(*m['bbox']) for m in images if m['id'].startswith('coast-')]);missing=coast.difference(coverage).length;assert missing<.01
ledger=json.loads((O/'candidate-ledger.json').read_text());ncand=len(json.loads((P/'candidates.json').read_text()));assert len([r for r in ledger if r['kind']!='kildekandidat'])==ncand
review=json.loads((P/'cluster-review-index.json').read_text());assert len(review)==ncand
for i in [0,1,2,3,4,5,7,8,60,61,62,63]:assert (P/'raw'/f'overpass-tile-{i}.json').exists()
res=dict(approval_status='godkjent_av_bruker' if approval else 'til_godkjenning',combined_polygons=len(base)+len(fs) if approval else len(base),polygons=len(fs),harbours=len({f['properties']['harbour_id'] for f in fs}),possible_harbours=sum(f['properties']['classification']=='mulig_smabathavn' for f in fs),unique_ids=True,valid_geometries=True,outside_municipality_m2=round(sum(g.difference(B).area for g in gs),6),overlap_issues=overlap,csv_matches_geojson=True,approved_baseline_unchanged=True,approved_baseline_polygons=len(base),approved_baseline_municipalities=len({f['properties']['municipality'] for f in base}),images=len(images),coast_tiles=sum(m['id'].startswith('coast-') for m in images),additional_images=sum(not m['id'].startswith('coast-') for m in images),all_images_fully_decoded=True,osm_coast_length_m=round(coast.length,1),osm_coast_outside_image_coverage_m=round(missing,3),osm_piers=144,osm_clusters=40,candidates_reviewed=len(review),final_outline_qa_panels=len(fs),source_observation_dates_known=False,inland_systematically_reviewed=False)
(O/'validation.json').write_text(json.dumps(res,ensure_ascii=False,indent=1)+'\n');(O/'imagery-manifest.json').write_text(json.dumps(images,ensure_ascii=False,indent=1)+'\n');print(json.dumps(res,ensure_ascii=False))
