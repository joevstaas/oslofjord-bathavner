import json,sys,time,urllib.request,urllib.parse,concurrent.futures,hashlib
from pathlib import Path
from PIL import Image
P=Path(__file__).parent
specs=json.loads((P/sys.argv[1]).read_text());provider=sys.argv[2] if len(sys.argv)>2 else 'topo'
def fetch(s):
 started=time.monotonic();key=s['id'];ext='png' if provider=='topo' else 'jpg';f=P/'images'/f'{key}.{ext}';meta=f.with_suffix('.json')
 if f.exists() and meta.exists():return key,'cached'
 if provider=='topo':
  q=dict(service='WMS',version='1.3.0',request='GetMap',layers='topo',crs='EPSG:25833',bbox=','.join(map(str,s['bbox'])),width=s['width'],height=s['height'],format='image/png');u='https://wms.geonorge.no/skwms1/wms.topo?'+urllib.parse.urlencode(q);d=urllib.request.urlopen(u,timeout=40).read();m=dict(s,url=u,requested_bbox=s['bbox'],actual_bbox=s['bbox'],crs='EPSG:25833',source='Kartverket Topografisk norgeskart',attribution='© Kartverket')
 else:
  q=dict(f='pjson',bbox=','.join(map(str,s['bbox'])),bboxSR=25833,imageSR=25833,size=f"{s['width']},{s['height']}",format='jpg');u='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export?'+urllib.parse.urlencode(q);res=json.load(urllib.request.urlopen(u,timeout=40));(P/'raw'/f'{key}-export.json').write_text(json.dumps(res,indent=2))
  if 'error' in res:raise ValueError(res['error'])
  img_url=res.get('href')
  if not img_url:
   image_params=dict(q,f='image');img_url='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export?'+urllib.parse.urlencode(image_params)
  try:
   d=urllib.request.urlopen(img_url,timeout=40).read()
  except Exception:
   image_params=dict(q,f='image');img_url='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export?'+urllib.parse.urlencode(image_params);d=urllib.request.urlopen(img_url,timeout=40).read()
  e=res['extent'];actual=[e['xmin'],e['ymin'],e['xmax'],e['ymax']];m=dict(s,url=u,image_url=res['href'],requested_bbox=s['bbox'],bbox=actual,actual_bbox=actual,width=res['width'] or s['width'],height=res['height'] or s['height'],crs='EPSG:25833',source='Esri World Imagery',attribution='Esri, Vantor, Earthstar Geographics, and the GIS User Community')
 f.write_bytes(d)
 with Image.open(f) as im:assert im.size==(m['width'],m['height'])
 m.update(retrieved_date='2026-10-29',source_observation_date=None,sha256=hashlib.sha256(d).hexdigest(),elapsed_seconds=round(time.monotonic()-started,3),bytes=len(d));meta.write_text(json.dumps(m,ensure_ascii=False,indent=2));return key,len(d)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 fs={ex.submit(fetch,s):s['id'] for s in specs}
 for f in concurrent.futures.as_completed(fs):
  try:print(f.result(),flush=True)
  except Exception as e:print(fs[f],'ERROR',repr(e),flush=True)
