from pathlib import Path
import json,sys
P=Path(__file__).parent;sys.path.insert(0,str(P/'deps'))
from pyproj import Transformer
from shapely.geometry import shape,box
from shapely.ops import transform
T=Transformer.from_crs(4326,25833,always_xy=True)
ss=[]
for i,f in enumerate(json.loads((P/'osm-candidates.json').read_text())):
 if 'lon' not in f:print('ERROR CANDIDATE',i,f);continue
 x,y=T.transform(f['lon'],f['lat']);ss.append(dict(id=f'p{i:02d}',bbox=[x-500,y-500,x+500,y+500],width=1500,height=1500))
(P/'detail.json').write_text(json.dumps(ss,indent=2))
g=transform(T.transform,shape(json.loads((P/'kommunegrense.geojson').read_text())['features'][0]['geometry']));print(g.bounds)
x0,y0,x1,y1=g.bounds;ss=[]
for i,x in enumerate(range(int(x0)//1000*1000,int(x1),3600)):
 for j,y in enumerate(range(int(y0)//1000*1000,int(y1),3600)):
  b=[x,y,x+4000,y+4000]
  if g.intersects(box(*b)):ss.append(dict(id=f'coast-{i}-{j}',bbox=b,width=1600,height=1600))
(P/'scan.json').write_text(json.dumps(ss,indent=2));(P/'coast-esri.json').write_text(json.dumps([dict(s,id='a-'+s['id']) for s in ss],indent=2));print('scan tiles',len(ss))
