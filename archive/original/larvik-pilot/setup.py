from pathlib import Path
import json,sys
P=Path(__file__).parent;sys.path.insert(0,str(P/'deps'))
from pyproj import Transformer
T=Transformer.from_crs(4326,25833,always_xy=True)
ss=[]
for i,f in enumerate(json.loads((P/'osm-candidates.json').read_text())):
 x,y=T.transform(f['lon'],f['lat']);ss.append(dict(id=f'p{i:02d}',bbox=[x-500,y-500,x+500,y+500],width=1400,height=1400))
(P/'detail.json').write_text(json.dumps(ss,indent=2))
coords=[T.transform(*xy) for xy in [(9.80,58.94),(10.30,59.09)]];print(coords)
b=[200000,6540000,231000,6563000];(P/'overview.json').write_text(json.dumps([dict(id='overview',bbox=b,width=2170,height=1610)]))
