from pathlib import Path
import json,re,collections,urllib.parse,hashlib
R=Path(__file__).resolve().parents[2];O=R/'data/miljokort/screening-01';O.mkdir(parents=True,exist_ok=True)
fc=json.loads((R/'data/samlet/oslofjorden-bathavner-samlet.geojson').read_text());groups={}
# Use the public map's gid to preserve the user's denominator, incl. cross-municipality groups.
site=json.loads((R/'site/labs/oslofjord-bathavner/data/harbours.geojson').read_text())
keys={f['properties']['id']:f['properties'].get('gid') or f['properties']['hid'] for f in site['features']}
def urls(x):
 if isinstance(x,str):return re.findall(r'https?://[^\s<>"\]]+',x)
 if isinstance(x,dict):return [u for v in x.values() for u in urls(v)]
 if isinstance(x,list):return [u for v in x for u in urls(v)]
 return []
for f in fc['features']:
 p=f['properties'];gid=keys[p['id']];g=groups.setdefault(gid,dict(group_id=gid,harbour_ids=[],names=[],municipalities=[],polygon_ids=[],urls=[],descriptive_name_only=True))
 for key,v in [('harbour_ids',p['harbour_id']),('names',p['name']),('municipalities',p['municipality']),('polygon_ids',p['id'])]:
  if v not in g[key]:g[key].append(v)
 if p.get('name_is_descriptive') is False:g['descriptive_name_only']=False
 for u in urls(p):
  host=urllib.parse.urlparse(u).netloc.lower()
  if any(z in host for z in ['openstreetmap.org','arcgisonline.com','geonorge.no','kartverket.no','brreg.no','norgeskart.no']):continue
  u=u.rstrip('.,;)')
  if u not in g['urls']:g['urls'].append(u)
assert len(groups)==664
(O/'inventory.json').write_text(json.dumps(list(groups.values()),ensure_ascii=False,indent=2)+'\n')
print('664 groups;',sum(bool(g['urls']) for g in groups.values()),'with public non-map URLs;',len({u for g in groups.values() for u in g['urls']}),'URLs')
print(collections.Counter(g['municipalities'][0] for g in groups.values()))
print('Named',sum(not g['descriptive_name_only'] for g in groups.values()))
