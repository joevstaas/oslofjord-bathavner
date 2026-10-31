"""OSM-kart-API i små ruter etter Overpass-feil. Lagrer original XML; trekk ut kystlinje/pirer og havnemerker."""
import requests,json,datetime,hashlib,concurrent.futures,xml.etree.ElementTree as ET
from pathlib import Path
from shapely.geometry import shape,box
P=Path(__file__).parent;B=shape(json.loads((P/'kommunegrense.geojson').read_text())['features'][0]['geometry'])
# Hele sjø-/kystområdet; egen suppleringsstripe for nedre Glomma og Sandesund.
bbs=[]
for i in range(6):
 for j in range(3):
  bb=[10.94+i*.06,59.08+j*.05,11.0+i*.06,59.13+j*.05]
  if box(*bb).intersects(B):bbs.append(bb)
for i in range(4):
 for j in range(2):
  bb=[10.94+i*.05,59.23+j*.05,10.99+i*.05,59.28+j*.05]
  if box(*bb).intersects(B):bbs.append(bb)
heads={'User-Agent':'OslofjordBathavner/1.0 (public geographic research; https://github.com/joevstaas/oslofjord-bathavner)'}
def fetch(item):
 key,bb=item;p=P/'raw'/f'osm-map-{key}.xml'
 if p.exists():return [p]
 u='https://api.openstreetmap.org/api/0.6/map';r=requests.get(u,params={'bbox':','.join(f'{v:.6f}' for v in bb)},headers=heads,timeout=40)
 if r.status_code==400 and 'too many nodes' in r.text:
  x,y,X,Y=bb;xm=(x+X)/2;ym=(y+Y)/2;out=[]
  for k,b in enumerate([[x,y,xm,ym],[xm,y,X,ym],[x,ym,xm,Y],[xm,ym,X,Y]]):out+=fetch((str(key)+'-'+str(k),b))
  return out
 r.raise_for_status();ET.fromstring(r.content);p.write_bytes(r.content);p.with_suffix('.provenance.json').write_text(json.dumps(dict(url=r.url,bbox=bb,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(r.content).hexdigest()),indent=1));print(key,len(r.content),flush=True);return [p]
files=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
 for out in ex.map(fetch,[(str(i),bb) for i,bb in enumerate(bbs)]):files+=out
nodes={};ways={};rels={}
for p in files:
 root=ET.parse(p).getroot()
 for el in root:
  typ=el.tag
  if typ=='node':nodes[el.attrib['id']]=el
  elif typ=='way':ways[el.attrib['id']]=el
  elif typ=='relation':rels[el.attrib['id']]=el
out=[]
for typ,entries in [('node',nodes),('way',ways),('relation',rels)]:
 for eid,el in entries.items():
  tags={t.attrib['k']:t.attrib['v'] for t in el.findall('tag')}
  if not (tags.get('man_made') in ['pier','breakwater'] or tags.get('natural')=='coastline' or tags.get('leisure')=='marina' or 'mooring' in tags or 'harbour' in tags):continue
  v=dict(type=typ,id=int(eid),tags=tags)
  if typ=='node':v.update(lat=float(el.attrib['lat']),lon=float(el.attrib['lon']))
  elif typ=='way':
   refs=[nd.attrib['ref'] for nd in el.findall('nd')];assert all(ref in nodes for ref in refs)
   v['geometry']=[dict(lat=float(nodes[ref].attrib['lat']),lon=float(nodes[ref].attrib['lon'])) for ref in refs]
  else:v['members']=[m.attrib for m in el.findall('member')]
  out.append(v)
(P/'raw/osm-sarpsborg.json').write_text(json.dumps(dict(source='OSM map API XML; converted to analysis geometry',elements=out),ensure_ascii=False));(P/'osm-coverage.json').write_text(json.dumps(dict(requested_bboxes=bbs,raw_xml=[str(f.relative_to(P)) for f in files],scope='Kystsone 59.08–59.23 N og nedre Glomma 59.23–59.33 N; ikke hele innlandet.',elements=len(out)),ensure_ascii=False,indent=1));print('elements',len(out),'xml',len(files),flush=True)
