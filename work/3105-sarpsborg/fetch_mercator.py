"""Hent manglende bilder i Esris native EPSG:3857; bevar original og resample eksplisitt til UTM med projisert pikselmesh."""
import requests,json,sys,hashlib,datetime,concurrent.futures,math,time
from pathlib import Path
from PIL import Image
from pyproj import Transformer
P=Path(__file__).parent;U='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export';T=Transformer.from_crs(25833,3857,always_xy=True);specs=json.loads((P/sys.argv[1]).read_text())
def fetch(s):
 key=s['id'];out=P/'images'/f'{key}.jpg';meta=out.with_suffix('.json')
 if out.exists() and meta.exists():return key,'cached'
 a,b,c,d=s['bbox'];corners=[T.transform(x,y) for x,y in [(a,b),(a,d),(c,b),(c,d)]];bb=[min(x for x,y in corners),min(y for x,y in corners),max(x for x,y in corners),max(y for x,y in corners)];W=s['width'];H=s['height'];SW=min(4096,math.ceil(W*1.1));SH=min(4096,math.ceil(H*1.1));q=dict(f='pjson',bbox=','.join(map(str,bb)),bboxSR=3857,imageSR=3857,size=f'{SW},{SH}',format='jpg')
 for attempt in range(2):
  try:
   r=requests.get(U,params=q,timeout=25);r.raise_for_status();m=r.json();assert m.get('href') and m.get('width'),m
   r2=requests.get(m['href'],timeout=25);r2.raise_for_status();raw=P/'raw'/f'{key}-native3857.jpg';raw.write_bytes(r2.content);(P/'raw'/f'{key}-native3857-export.json').write_text(json.dumps(m,indent=1));im=Image.open(raw);im.load();e=m['extent'];x0,y0,x1,y1=e['xmin'],e['ymin'],e['xmax'],e['ymax']
   def pixel(x,y):
    X,Y=T.transform(a+x/W*(c-a),d-y/H*(d-b));return (X-x0)/(x1-x0)*im.width,(y1-Y)/(y1-y0)*im.height
   mesh=[]
   for y in range(0,H,32):
    for x in range(0,W,32):
     X,Y=min(x+32,W),min(y+32,H);mesh.append(((x,y,X,Y),pixel(x,y)+pixel(x,Y)+pixel(X,Y)+pixel(X,y)))
   derived=im.transform((W,H),Image.Transform.MESH,mesh,Image.Resampling.BICUBIC);derived.save(out,quality=95)
   now=datetime.datetime.now(datetime.timezone.utc).isoformat();md=dict(s,requested_bbox=s['bbox'],actual_bbox=s['bbox'],crs='EPSG:25833',source='Esri World Imagery',attribution='Source: Esri, Vantor, Earthstar Geographics, and the GIS User Community',url=r.url,image_url=m['href'],retrieved_date=now[:10],retrieved_utc=now,source_observation_date=None,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),source_image=str(raw.relative_to(P)),source_image_sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),source_crs='EPSG:3857',source_extent=e,source_width=im.width,source_height=im.height,processing='Deterministisk omprojisering med pyproj og PIL MESH, rutenett 32 utpiksler; original bevares. Ikke nytt opptak.');meta.write_text(json.dumps(md,ensure_ascii=False,indent=1));return key,len(r2.content)
  except Exception as ex:
   if attempt:raise
 raise RuntimeError(key)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 futures={ex.submit(fetch,s):s['id'] for s in specs}
 for f in concurrent.futures.as_completed(futures):
  try:print(f.result(),flush=True)
  except Exception as e:print(futures[f],'ERROR',str(e)[:150],flush=True)
