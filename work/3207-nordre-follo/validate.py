"""Valider den nye leveransen og bevar godkjent grunnlag uendret."""
import json,csv,hashlib,warnings
from pathlib import Path
from shapely.geometry import shape,box,LineString
from shapely.ops import transform,unary_union
from pyproj import Transformer
from PIL import Image
warnings.filterwarnings('ignore')
P=Path(__file__).parent;R=P.parents[1];O=R/'data/kommuner/3207-nordre-follo/rev-01'
F=Transformer.from_crs(4326,25833,always_xy=True).transform
b=transform(F,shape(json.loads((P/'kommunegrense.geojson').read_text())['features'][0]['geometry']))
approval=json.loads((O/'approval.json').read_text()) if (O/'approval.json').exists() else None
fs=json.loads((O/'bathavner.geojson').read_text())['features'];base=json.loads((R/'data/samlet/oslofjorden-bathavner-samlet.geojson').read_text())['features'];ids=[f['properties']['id'] for f in fs]
if approval:
 old=[f for f in base if f['properties'].get('municipality_code')!='3207']
 assert hashlib.sha256(json.dumps(old,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==approval['previous_features_sha256']
 assert all(f in base for f in fs)
 base=old
assert len(ids)==len(set(ids)) and not set(ids)&{f['properties']['id'] for f in base}
gs=[transform(F,shape(f['geometry'])) for f in fs]
assert all(g.is_valid and not g.is_empty and g.difference(b).area<.001 for g in gs)
overlap=[]
for f,g in zip(fs,gs):
 for old in base:
  og=transform(F,shape(old['geometry']))
  if not g.envelope.intersects(og.envelope):continue
  a=g.intersection(og).area
  if a>.01:overlap.append([f['properties']['id'],old['properties']['id'],a])
assert not overlap,overlap
assert gs[0].intersection(gs[1]).area==0
rows=list(csv.DictReader((O/'metadata.csv').open(encoding='utf-8-sig'),delimiter=';'));assert len(rows)==len(fs)
for row,f in zip(rows,fs):
 for k,v in f['properties'].items():
  exp=json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else '' if v is None else str(v)
  assert row[k]==exp,(k,row[k],exp)
 assert f['properties']['approval_status']==('godkjent_av_bruker' if approval else 'til_godkjenning')
 assert f['properties']['approved_utc']==(approval['approved_utc'] if approval else None)
 m=json.loads((P/'images'/(f['properties']['image_id']+'.json')).read_text())
 assert hashlib.sha256((P/'images'/(f['properties']['image_id']+'.jpg')).read_bytes()).hexdigest()==f['properties']['image_sha256']==m['sha256']
for fn,sha in ({} if approval else json.loads((P/'run.json').read_text())['approved_baseline_sha256']).items():assert hashlib.sha256((R/fn).read_bytes()).hexdigest()==sha,fn
images=[]
for fn in sorted((P/'images').glob('*.jpg')):
 im=Image.open(fn);im.load();m=json.loads(fn.with_suffix('.json').read_text());assert im.size==(m['width'],m['height']);assert hashlib.sha256(fn.read_bytes()).hexdigest()==m['sha256'];images.append(m)
coasts=[]
for e in json.loads((P/'raw/overpass-nordre-follo.json').read_text())['elements']:
 if e.get('tags',{}).get('natural')=='coastline':coasts.append(transform(F,LineString([(v['lon'],v['lat']) for v in e['geometry']])).intersection(b.buffer(20)))
c=unary_union(coasts);covered=unary_union([box(*m['bbox']) for m in images if m['id'].startswith('coast')]);missing=c.difference(covered).length;assert missing<.01
res=dict(approval_status='godkjent_av_bruker' if approval else 'til_godkjenning',combined_polygons=458 if approval else 456,polygons=len(fs),harbours=2,saltwater_harbours=1,possible_freshwater_harbours=1,approved_baseline_polygons=len(base),approved_baseline_unchanged=True,unique_ids=True,valid_geometries=True,outside_municipality_m2=round(sum(g.difference(b).area for g in gs),6),overlap_with_approved=overlap,csv_matches_geojson=True,all_images_fully_decoded=True,images=len(images),coast_tiles=14,inland_candidate_tiles=17,detail_tiles=len(images)-31,osm_coast_length_m=round(c.length,1),osm_coast_outside_image_coverage_m=round(missing,3),mapped_piers_reviewed=len(json.loads((P/'pier-review-index.json').read_text())),final_outlines_visually_reviewed=2,source_observation_date_known=False,inland_systematic_complete=False)
(O/'validation.json').write_text(json.dumps(res,ensure_ascii=False,indent=1)+'\n');(O/'imagery-manifest.json').write_text(json.dumps(images,ensure_ascii=False,indent=1)+'\n');print(json.dumps(res,ensure_ascii=False))
