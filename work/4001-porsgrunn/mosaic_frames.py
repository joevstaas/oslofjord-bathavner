import json,hashlib,datetime
from pathlib import Path
from PIL import Image
from shapely.geometry import box
P=Path(__file__).parent
for s in json.loads((P/'specs-manual.json').read_text()):
 out=P/'images'/(s['id']+'.jpg')
 if out.exists():continue
 a,b,c,d=s['bbox'];W=H=1600;im=Image.new('RGB',(W,H));sources=[]
 fs=[]
 for f in (P/'images').glob('*.jpg'):
  if f.stem.startswith('detail-M'):continue
  m=json.loads(f.with_suffix('.json').read_text());bb=m['bbox']
  if box(*bb).intersects(box(a,b,c,d)):fs.append((f,m))
 for f,m in sorted(fs,key=lambda q:(q[1]['bbox'][2]-q[1]['bbox'][0])/q[1]['width'],reverse=True):
  x,y,X,Y=box(*m['bbox']).intersection(box(a,b,c,d)).bounds;ma,mb,mc,md=m['bbox'];src=Image.open(f);crop=src.crop(((x-ma)/(mc-ma)*src.width,(md-Y)/(md-mb)*src.height,(X-ma)/(mc-ma)*src.width,(md-y)/(md-mb)*src.height));px=(round((x-a)/(c-a)*W),round((d-Y)/(d-b)*H),round((X-a)/(c-a)*W),round((d-y)/(d-b)*H));
  if px[2]<=px[0] or px[3]<=px[1]:continue
  im.paste(crop.resize((px[2]-px[0],px[3]-px[1])),px[:2]);sources.append(dict(image_id=f.stem,sha256=m['sha256']))
 im.save(out,quality=96);m=dict(s,crs='EPSG:25833',source='Esri World Imagery',url='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer',retrieved_date='2026-10-31',sha256=hashlib.sha256(out.read_bytes()).hexdigest(),processing='Mosaikk/utsnitt av bevarte georefererte bilder; ingen ny informasjon.',mosaic_sources=sources);out.with_suffix('.json').write_text(json.dumps(m,indent=1))
 print(s['id'],len(sources))
