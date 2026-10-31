import json,warnings
from pathlib import Path
from PIL import Image,ImageDraw
from pyproj import Transformer
from shapely.geometry import shape,LineString,box
from shapely.ops import transform
warnings.filterwarnings('ignore')
P=Path(__file__).parent;T=Transformer.from_crs(4326,25833,always_xy=True).transform
B=transform(T,shape(json.loads((P/'kommunegrense.geojson').read_text())['features'][0]['geometry']))
imgs=[]
for f in sorted((P/'images').glob('*.jpg')):
 m=json.loads(f.with_suffix('.json').read_text());imgs.append((f,m))
rows=[];panels=[]
for el in json.loads((P/'raw/overpass-bamble.json').read_text())['elements']:
 if not el.get('geometry') or el.get('tags',{}).get('man_made')!='pier':continue
 g=transform(T,LineString([(v['lon'],v['lat']) for v in el['geometry']]))
 if not g.intersects(B):continue
 q=g.centroid;area=box(q.x-120,q.y-120,q.x+120,q.y+120)
 matches=[(f,m) for f,m in imgs if box(*m['bbox']).covers(area)]
 if not matches:
  matches=[(f,m) for f,m in imgs if box(*m['bbox']).covers(q)]
  if not matches:continue
  a,b,c,d=matches[0][1]['bbox'];area=area.intersection(box(a,b,c,d))
 f,m=matches[0];a,b,c,d=m['bbox'];im=Image.open(f);W,H=im.size
 fr=area.bounds;crop=im.crop(((fr[0]-a)/(c-a)*W,(d-fr[3])/(d-b)*H,(fr[2]-a)/(c-a)*W,(d-fr[1])/(d-b)*H)).resize((400,400))
 dr=ImageDraw.Draw(crop);px=lambda x,y:((x-fr[0])/(fr[2]-fr[0])*400,(fr[3]-y)/(fr[3]-fr[1])*400)
 dr.line([px(*v) for v in g.coords],fill='red',width=2)
 for ln in getattr(B.boundary.intersection(area),'geoms',[B.boundary.intersection(area)]):
  if ln.geom_type=='LineString':dr.line([px(*v) for v in ln.coords],fill='yellow',width=2)
 pn=Image.new('RGB',(400,425),'white');pn.paste(crop,(0,25));ImageDraw.Draw(pn).text((3,3),f"{el['id']} {f.stem}",fill='black');panels.append(pn)
 rows.append(dict(osm_id=el['id'],image_id=f.stem,center_25833=[q.x,q.y],length_m=g.length))
for n in range(0,len(panels),6):
 sheet=Image.new('RGB',(1200,850),'white')
 for i,p in enumerate(panels[n:n+6]):sheet.paste(p,(i%3*400,i//3*425))
 sheet.save(P/'qa'/f'piers-{n//6:02}.jpg',quality=93)
(P/'pier-review-index.json').write_text(json.dumps(rows,indent=1));print('review panels',len(rows))
