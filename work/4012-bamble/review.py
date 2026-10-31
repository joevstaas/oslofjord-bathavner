"""Georefererte vurderingspaneler (600 x 600) for alle kandidater, med OSM-pirer (rød), kommunegrense (gul) og 50 m-rutenett med pikseltikker.
Kandidater som ikke dekkes av én kystflis bruker detaljbilde detail-<cid>. Utsnittet er QA, ikke ny kilde."""
import json,warnings,sys
from pathlib import Path
from PIL import Image,ImageDraw
from shapely.geometry import box,shape
from shapely.ops import transform
from pyproj import Transformer
warnings.filterwarnings('ignore');P=Path(__file__).parent;S=600
T=Transformer.from_crs(4326,25833,always_xy=True).transform
B=transform(T,shape(json.loads((P/'kommunegrense.geojson').read_text())['features'][0]['geometry']))
imgs=[(f,json.loads(f.with_suffix('.json').read_text())) for f in sorted((P/'images').glob('*.jpg'))]
C={c['cid']:c for c in json.loads((P/'clusters.json').read_text())}
override=json.loads((P/'frame-overrides.json').read_text()) if (P/'frame-overrides.json').exists() else {}
rows=[];panels=[];missing=[]
for c in json.loads((P/'candidates.json').read_text()):
 cid=c['cid'];x,y=override.get(cid,{}).get('center',c['center']);side=override.get(cid,{}).get('side',c['side']);fr=[x-side/2,y-side/2,x+side/2,y+side/2];area=box(*fr)
 m=[(f,mm) for f,mm in imgs if f.stem=='detail-'+cid and box(*mm['bbox']).buffer(5).covers(area)] or [(f,mm) for f,mm in imgs if box(*mm['bbox']).covers(area)]
 if not m:missing.append(cid);continue
 f,mm=m[0];x0,y0,x1,y1=mm['bbox'];W,H=mm['width'],mm['height'];im=Image.open(f).convert('RGB')
 cl=im.crop(((fr[0]-x0)/(x1-x0)*W,(y1-fr[3])/(y1-y0)*H,(fr[2]-x0)/(x1-x0)*W,(y1-fr[1])/(y1-y0)*H)).resize((S,S))
 cl.save(P/'qa'/f'{cid}-clean.jpg',quality=94);d=ImageDraw.Draw(cl);px=lambda X,Y:((X-fr[0])/side*S,(fr[3]-Y)/side*S)
 g0=int(fr[0]//50+1)*50
 for gx in range(g0,int(fr[2]),50):d.line([px(gx,fr[1]),px(gx,fr[3])],fill=(255,255,255),width=1)
 for gy in range(int(fr[1]//50+1)*50,int(fr[3]),50):d.line([px(fr[0],gy),px(fr[2],gy)],fill=(255,255,255),width=1)
 for k in range(0,S+1,100):d.text((k+2,2),str(k),fill='cyan');d.text((2,k+2),str(k),fill='cyan')
 for p in C.get(cid,{}).get('piers',[]):d.line([px(*z) for z in shape(p['geometry']).coords],fill='red',width=2)
 bl=B.boundary.intersection(area)
 for ln in getattr(bl,'geoms',[bl]):
  if ln.geom_type=='LineString':d.line([px(*z) for z in ln.coords],fill='yellow',width=2)
 pn=Image.new('RGB',(S,S+22),'white');pn.paste(cl,(0,22));ImageDraw.Draw(pn).text((4,4),f"{cid} {c.get('name') or ','.join(filter(None,c.get('marks',[])))} {f.stem} {round(side)}m"[:95],fill='black');panels.append(pn)
 rows.append(dict(cid=cid,image_id=f.stem,review_bbox=fr,review_width=S,review_height=S))
for n in range(0,len(panels),4):
 can=Image.new('RGB',(2*S,2*(S+22)),'white')
 for i,pn in enumerate(panels[n:n+4]):can.paste(pn,(i%2*S,i//2*(S+22)))
 can.save(P/'qa'/f'review-{n//4:02}.jpg',quality=92)
(P/'cluster-review-index.json').write_text(json.dumps(rows,indent=1));print('panels',len(rows),'missing',missing)
