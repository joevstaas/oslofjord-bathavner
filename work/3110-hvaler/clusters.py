import json,warnings
from pathlib import Path
from pyproj import Transformer
from shapely.geometry import shape,LineString,Point,mapping
from shapely.ops import transform,unary_union
warnings.filterwarnings('ignore')
P=Path(__file__).parent;T=Transformer.from_crs(4326,25833,always_xy=True).transform
B=transform(T,shape(json.loads((P/'kommunegrense.geojson').read_text())['features'][0]['geometry']))
piers=[];marks=[]
for e in json.loads((P/'raw/overpass-hvaler.json').read_text())['elements']:
 t=e.get('tags',{});gg=e.get('geometry')
 if e['type']=='node':g=Point(T(e['lon'],e['lat']))
 elif gg:g=LineString([T(v['lon'],v['lat']) for v in gg])
 else:continue
 if g.distance(B)>20:continue
 if t.get('man_made')=='pier':piers.append(dict(id=f"{e['type']}/{e['id']}",g=g,tags=t))
 if t.get('leisure')=='marina':marks.append(dict(id=f"{e['type']}/{e['id']}",g=g,tags=t))
cs=[]
for p in piers:
 hit=[k for k in cs if any(p['g'].distance(q['g'])<60 for q in k)]
 if hit:
  k=hit[0];k.append(p)
  for o in hit[1:]:k.extend(o);cs.remove(o)
 else:cs.append([p])
out=[]
for k in cs:
 g=unary_union([p['g'] for p in k]);q=g.centroid;near=[m for m in marks if m['g'].distance(g)<180]
 out.append(dict(cid='',center=[q.x,q.y],bounds=list(g.bounds),length_m=round(sum(p['g'].length for p in k),1),piers=[dict(id=p['id'],geometry=mapping(p['g']),tags=p['tags']) for p in k],marks=[dict(id=m['id'],tags=m['tags']) for m in near]))
out.sort(key=lambda x:(int(x['center'][0]//2000),-x['center'][1]))
for i,r in enumerate(out):r['cid']=f'C{i+1:03}'
(P/'clusters.json').write_text(json.dumps(out,ensure_ascii=False,indent=1));print('piers',len(piers),'clusters',len(out))
for r in out:
 if r['length_m']>=25 or r['marks']:print(r['cid'],list(map(round,r['center'])),r['length_m'],len(r['piers']),[m['tags'].get('name') for m in r['marks']])
