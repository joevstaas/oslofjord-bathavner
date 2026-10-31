"""Historisk sky-kontroll via offentlige visningsfliser; lokale originaler og georeferering bevares."""
import json,requests,math,hashlib,datetime,concurrent.futures
from pathlib import Path
from PIL import Image
from pyproj import Transformer
P=Path(__file__).parent;T=Transformer.from_crs(25833,3857,always_xy=True);Z=17;res=156543.03392804097/2**Z;O=20037508.342789244;U='https://clarity.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/MapServer'
for s in json.loads((P/'specs-clarity.json').read_text()):
 a,b,c,d=s['bbox'];xy=[T.transform(x,y) for x,y in [(a,b),(a,d),(c,b),(c,d)]];x0=min(x for x,y in xy);x1=max(x for x,y in xy);y0=min(y for x,y in xy);y1=max(y for x,y in xy);ix0=int((x0+O)/res/256);ix1=int((x1+O)/res/256);iy0=int((O-y1)/res/256);iy1=int((O-y0)/res/256)
 tasks=[(x,y) for y in range(iy0,iy1+1) for x in range(ix0,ix1+1)]
 def get(q):
  x,y=q;f=P/'raw'/f'clarity-z{Z}-{y}-{x}.jpg'
  if not f.exists():
   r=requests.get(f'{U}/tile/{Z}/{y}/{x}',timeout=20);r.raise_for_status();f.write_bytes(r.content)
  return x,y,f
 im=Image.new('RGB',((ix1-ix0+1)*256,(iy1-iy0+1)*256));orig=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
  for x,y,f in ex.map(get,tasks):
   im.paste(Image.open(f),((x-ix0)*256,(y-iy0)*256));orig.append(dict(path=str(f.relative_to(P)),url=f'{U}/tile/{Z}/{y}/{x}',sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
 nx0=ix0*256*res-O;ny1=O-iy0*256*res;W,H=s['width'],s['height']
 def px(x,y):
  X,Y=T.transform(a+x/W*(c-a),d-y/H*(d-b));return (X-nx0)/res,(ny1-Y)/res
 mesh=[]
 for y in range(0,H,32):
  for x in range(0,W,32):
   X,Y=min(x+32,W),min(y+32,H);mesh.append(((x,y,X,Y),px(x,y)+px(x,Y)+px(X,Y)+px(X,y)))
 out=P/'images'/(s['id']+'.jpg');im.transform((W,H),Image.Transform.MESH,mesh,Image.Resampling.BICUBIC).save(out,quality=95)
 now=datetime.datetime.now(datetime.timezone.utc).isoformat();m=dict(s,crs='EPSG:25833',source='Esri World Imagery Clarity (historisk arkiv)',url=U,retrieved_date=now[:10],retrieved_utc=now,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),source_observation_date=None,processing='Native EPSG:3857 visningsfliser z17, originaler bevart. pyproj/PIL MESH til UTM33. Historisk kontroll, ikke nåtidsbevis.',tile_originals=orig,source_pixel_size_webmercator=res)
 out.with_suffix('.json').write_text(json.dumps(m,indent=1));print(s['id'],len(orig),flush=True)
