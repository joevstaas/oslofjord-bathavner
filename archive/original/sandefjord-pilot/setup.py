import sys,json
from pathlib import Path
P=Path(__file__).parent;sys.path.insert(0,str(P/'deps'))
from pyproj import Transformer
T=Transformer.from_crs(4326,25833,always_xy=True)
fs=json.loads((P/'raw/municipal-harbour-points.geojson').read_text())['features'];ss=[]
for f in fs:
 x,y=T.transform(*f['geometry']['coordinates']);ss.append(dict(id='p%02d'%f['properties']['OBJECTID'],bbox=[x-500,y-500,x+500,y+500],width=1400,height=1400))
(P/'detail.json').write_text(json.dumps(ss,indent=2));print([T.transform(*c) for c in [(10.19,59.045),(10.39,59.245)]])
# Three fjord arms and coastal islands, plus inland lake overview.
bb=[221000,6554000,237000,6579000];(P/'overview.json').write_text(json.dumps([dict(id='overview',bbox=bb,width=1280,height=2000)]))
