import json
from pathlib import Path
from shapely.geometry import shape,LineString
from shapely.ops import transform
from pyproj import Transformer
P=Path(__file__).parent
tr=Transformer.from_crs(4326,25833,always_xy=True).transform
boundary=transform(tr,shape(json.loads((P/'kommunegrense.geojson').read_text())['features'][0]['geometry']))
data=json.loads((P/'raw/overpass-hvaler.json').read_text())
coasts=[]
for e in data['elements']:
 if e.get('tags',{}).get('natural')=='coastline':
  g=transform(tr,LineString([(p['lon'],p['lat']) for p in e['geometry']])).intersection(boundary.buffer(20))
  if not g.is_empty: coasts.append(g)
from shapely.ops import unary_union
coast=unary_union(coasts)
print('coast bounds',coast.bounds,'length',coast.length)
features=[]
for e in data['elements']:
 if e.get('geometry') and e.get('tags',{}).get('man_made')=='pier':
  g=transform(tr,LineString([(p['lon'],p['lat']) for p in e['geometry']]))
  if g.intersects(boundary): features.append((e['id'],g))
print('inside piers',len(features))
specs=[]
x0,y0,x1,y1=coast.bounds
for y in range(int(y0//900)*900,int(y1)+900,900):
 for x in range(int(x0//900)*900,int(x1)+900,900):
  from shapely.geometry import box
  b=box(x-100,y-100,x+1000,y+1000)
  if b.intersects(coast):specs.append(dict(id=f'coast-{x}-{y}',bbox=list(b.bounds),width=1500,height=1500))
# Inland OSM piers, grouped on a 1km grid; inspect all mapped inland candidates separately.
seen=set()
for eid,g in features:
 if g.distance(coast)<400:continue
 p=g.representative_point();key=(int(p.x//900)*900,int(p.y//900)*900)
 if key in seen:continue
 seen.add(key);x,y=key
 specs.append(dict(id=f'inland-{x}-{y}',bbox=[x-150,y-150,x+1050,y+1050],width=1500,height=1500))
(P/'specs.json').write_text(json.dumps(specs,indent=1))
print('tiles',len(specs), 'coastal',len(specs)-len(seen),'inland',len(seen))
