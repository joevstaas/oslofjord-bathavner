from pathlib import Path
import json,sys,re
P=Path(__file__).parent;sys.path.insert(0,str(P/'deps'))
from pyproj import Transformer
from shapely.geometry import shape,mapping
from shapely.ops import transform
F=Transformer.from_crs(4258,25833,always_xy=True).transform;G=Transformer.from_crs(4258,4326,always_xy=True).transform
x=json.loads((P/'raw/kommunegrense-response.json').read_text());geom=x['omrade'];print('source CRS',geom.get('crs'));g=shape(geom);wgs=transform(G,g);(P/'kommunegrense.geojson').write_text(json.dumps({'type':'FeatureCollection','features':[{'type':'Feature','properties':{'name':'Færder','municipality_code':'3911','source':'Kartverket kommuneinfo','source_crs':'EPSG:4258'},'geometry':mapping(wgs)}]}));print('projected bounds',transform(F,g).bounds)
links=json.loads((P/'raw/candidate-links.json').read_text());objs=[]
for l in links:
 if '/gjestehavner/' not in l:continue
 t,n=re.search(r'osm-(node|way|relation)-(\d+)',l).groups();objs.append({'type':t,'id':int(n),'link':'https://www.sjosett.com'+l})
(P/'candidate-specs.json').write_text(json.dumps(objs,indent=2));print('marina source objects',len(objs))
