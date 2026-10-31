"""Georefererte kandidatpaneler fra bevarte kilde-/omprojiserte bilder. Piksler er 800x800."""
import json,warnings
from pathlib import Path
from PIL import Image,ImageDraw
from shapely.geometry import box,shape
from shapely.ops import transform
from pyproj import Transformer
warnings.filterwarnings('ignore');P=Path(__file__).parent;S=800;T=Transformer.from_crs(4326,25833,always_xy=True).transform;B=transform(T,shape(json.loads((P/'kommunegrense.geojson').read_text())['features'][0]['geometry']))
imgs=[(f,json.loads(f.with_suffix('.json').read_text())) for f in (P/'images').glob('*.jpg') if f.with_suffix('.json').exists()];rows=[];panels=[];missing=[]
cs=json.loads((P/'clusters.json').read_text())
if (P/'image-candidates.json').exists():cs+=json.loads((P/'image-candidates.json').read_text())
for c in cs:
 cid=c['cid'];a,b,d,e=c['bounds'];cx=(a+d)/2;cy=(b+e)/2;side=max(260,d-a+90,e-b+90);fr=[cx-side/2,cy-side/2,cx+side/2,cy+side/2]
 if c.get('frame_bbox'):fr=c['frame_bbox'];side=fr[2]-fr[0]
 matches=[(f,m) for f,m in imgs if box(*m['bbox']).buffer(.01).covers(box(*fr))]
 if not matches:
  # Detail images explicitly cover their intended candidates; retain their exact frame.
  matches=[(f,m) for f,m in imgs if f.stem=='detail-'+cid]
  if matches:fr=matches[0][1]['bbox'];side=fr[2]-fr[0]
 if not matches:missing.append(cid);continue
 f,m=min(matches,key=lambda fm:(fm[1]['bbox'][2]-fm[1]['bbox'][0])/fm[1]['width']);a,b,d,e=m['bbox'];W,H=m['width'],m['height'];im=Image.open(f);im.load();clean=im.crop(((fr[0]-a)/(d-a)*W,(e-fr[3])/(e-b)*H,(fr[2]-a)/(d-a)*W,(e-fr[1])/(e-b)*H)).resize((S,S));clean.save(P/'qa'/f'{cid}-clean.jpg',quality=96);dr=ImageDraw.Draw(clean)
 for z in range(100,S,100):dr.line([(z,0),(z,S)],fill='white');dr.text((z+2,2),str(z),fill='cyan');dr.line([(0,z),(S,z)],fill='white');dr.text((2,z+2),str(z),fill='cyan')
 boundary=B.boundary.intersection(box(*fr));px=lambda x,y:((x-fr[0])/(fr[2]-fr[0])*S,(fr[3]-y)/(fr[3]-fr[1])*S)
 for ln in getattr(boundary,'geoms',[boundary]):
  if ln.geom_type=='LineString':dr.line([px(*q) for q in ln.coords],fill='yellow',width=2)
 pn=Image.new('RGB',(S,S+25),'white');pn.paste(clean,(0,25));ImageDraw.Draw(pn).text((4,4),f"{cid} {round(side)}m "+','.join(x.get('tags',{}).get('name','') for x in c.get('marks',[])),fill='black');panels.append(pn);rows.append(dict(cid=cid,image_id=f.stem,review_bbox=fr,review_width=S,review_height=S))
for n in range(0,len(panels),4):
 sh=Image.new('RGB',(S*2,(S+25)*2),'white')
 for i,pn in enumerate(panels[n:n+4]):sh.paste(pn,(i%2*S,i//2*(S+25)))
 sh.save(P/'qa'/f'candidates-{n//4:02}.jpg',quality=95)
(P/'cluster-review-index.json').write_text(json.dumps(rows,indent=1));print('ready',len(rows),'missing',missing)
