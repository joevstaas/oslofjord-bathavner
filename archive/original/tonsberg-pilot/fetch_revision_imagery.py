import json,urllib.request,urllib.parse,concurrent.futures
from pathlib import Path
from PIL import Image
P=Path(__file__).parent
specs=[]
for key in ['sentrum','vallo','husvik','husoy','bliksekilen','vestfjord','ringshaug','karlsvika','jarlso']:
 m=json.loads((P/'images'/f'{key}.json').read_text());specs.append(dict(id=key+'-ortho',bbox=m['bbox'],width=2000,height=2000 if key not in ['husvik','vestfjord','ringshaug','karlsvika','sentrum'] else round(2000*(m['bbox'][3]-m['bbox'][1])/(m['bbox'][2]-m['bbox'][0]))))
# Shoreline sectors without previously digitized areas; existing maps remain screening references.
for key,b,size in [('klopp-ortho',[241800,6577100,243400,6578500],(2000,1750)),('husoy-sor-ortho',[241000,6574200,242700,6575900],(2000,2000)),('traeleborg-ortho',[238900,6577200,241200,6579500],(2000,2000)),('nordkyst-ortho',[242900,6583500,244800,6588500],(1200,3158)),('skallevold-ortho',[242800,6580000,245500,6584000],(1800,2667)),('vestkyst-ortho',[235200,6575000,237500,6581000],(1200,3130))]:specs.append(dict(id=key,bbox=b,width=size[0],height=size[1]))
(P/'revision-imagery-specs.json').write_text(json.dumps(specs,indent=2))
def get(s):
 path=P/'images'/f"{s['id']}.jpg"
 if path.exists():return s['id'],'cached'
 params=dict(f='image',bbox=','.join(map(str,s['bbox'])),bboxSR=25833,imageSR=25833,size=f"{s['width']},{s['height']}",format='jpg')
 u='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export?'+urllib.parse.urlencode(params)
 data=urllib.request.urlopen(u,timeout=55).read();path.write_bytes(data)
 with Image.open(path) as im:assert im.size==(s['width'],s['height'])
 meta=dict(s,crs='EPSG:25833',url=u,source='Esri World Imagery',attribution='Esri, Maxar, Earthstar Geographics, and the GIS User Community; see service copyright metadata',retrieved='2026-10-29',source_observation_date=None)
 path.with_suffix('.json').write_text(json.dumps(meta,indent=2));return s['id'],len(data)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 fs={ex.submit(get,s):s['id'] for s in specs}
 for f in concurrent.futures.as_completed(fs):
  try:print(f.result(),flush=True)
  except Exception as e:print(fs[f],repr(e),flush=True)
