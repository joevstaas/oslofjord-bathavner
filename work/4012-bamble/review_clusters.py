"""Kontaktark for alle pirklynger. Originalbilder beholdes; utsnittet er georeferert QA, ikke ny kildedatering."""
import json,warnings
from pathlib import Path
from PIL import Image,ImageDraw
from shapely.geometry import box,shape
from shapely.ops import transform
from pyproj import Transformer
warnings.filterwarnings('ignore');P=Path(__file__).parent
T=Transformer.from_crs(4326,25833,always_xy=True).transform
B=transform(T,shape(json.loads((P/'kommunegrense.geojson').read_text())['features'][0]['geometry']))
imgs=[]
for f in sorted((P/'images').glob('*.jpg')):
 m=json.loads(f.with_suffix('.json').read_text());imgs.append((f,m))
rows=[];panels=[]
for c in json.loads((P/'clusters.json').read_text()):
 a,b,d,e=c['bounds'];cx=(a+d)/2;cy=(b+e)/2;side=(220 if c['cid']=='C007' else max(220,d-a+90,e-b+90));fr=[cx-side/2,cy-side/2,cx+side/2,cy+side/2];area=box(*fr)
 matches=[(f,m) for f,m in imgs if box(*m['bbox']).covers(area)]
 if not matches:
  continue
 f,m=matches[0];x0,y0,x1,y1=m['bbox'];W,H=m['width'],m['height'];im=Image.open(f);im.load()
 clean=im.crop(((fr[0]-x0)/(x1-x0)*W,(y1-fr[3])/(y1-y0)*H,(fr[2]-x0)/(x1-x0)*W,(y1-fr[1])/(y1-y0)*H)).resize((500,500))
 clean.save(P/'qa'/f"{c['cid']}-clean.jpg",quality=94)
 dr=ImageDraw.Draw(clean);px=lambda x,y:((x-fr[0])/side*500,(fr[3]-y)/side*500)
 for p in c['piers']:dr.line([px(*z) for z in shape(p['geometry']).coords],fill='red',width=1)
 cl=B.boundary.intersection(area)
 for ln in getattr(cl,'geoms',[cl]):
  if ln.geom_type=='LineString':dr.line([px(*z) for z in ln.coords],fill='yellow',width=2)
 panel=Image.new('RGB',(500,525),'white');panel.paste(clean,(0,25));ImageDraw.Draw(panel).text((4,4),c['cid']+' '+','.join(m['tags'].get('name','?') for m in c['marks'])[:56],fill='black');panels.append(panel)
 rows.append(dict(cid=c['cid'],image_id=f.stem,review_bbox=fr,review_width=500,review_height=500))
for n in range(0,len(panels),6):
 can=Image.new('RGB',(1500,1050),'white')
 for i,pn in enumerate(panels[n:n+6]):can.paste(pn,(i%3*500,i//3*525))
 can.save(P/'qa'/f'clusters-{n//6:02}.jpg',quality=93)
(P/'cluster-review-index.json').write_text(json.dumps(rows,indent=1));print('ready',len(rows),'of',len(json.loads((P/'clusters.json').read_text())))
