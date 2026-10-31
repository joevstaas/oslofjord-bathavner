import urllib.request,urllib.parse,json,hashlib,datetime,concurrent.futures
from pathlib import Path
from shapely.geometry import shape
P=Path(__file__).parent
w,s,e,n=shape(json.loads((P/'raw/kommunegrense-4326.json').read_text())['omrade']).bounds
xm=(w+e)/2;ym=(s+n)/2
xs=[w+(e-w)*i/3 for i in range(4)];ys=[s+(n-s)*i/3 for i in range(4)]
boxes=[(ys[j],xs[i],ys[j+1],xs[i+1]) for j in range(3) for i in range(3)]
# Delrute 6 tidsavbrøt gjentatte ganger; erstattes av fire mindre ruter 60-63.
b6=boxes[6];my=(b6[0]+b6[2])/2;mx=(b6[1]+b6[3])/2
sub=[(b6[0],b6[1],my,mx),(b6[0],mx,my,b6[3]),(my,b6[1],b6[2],mx),(my,mx,b6[2],b6[3])]
jobs=[(i,b) for i,b in enumerate(boxes) if i!=6]+[(60+k,b) for k,b in enumerate(sub)]
def fetch(z):
 i,bb=z;bb=','.join(map(str,bb));q=f'[out:json][timeout:30];(nwr["leisure"="marina"]({bb});nwr["mooring"]({bb});nwr["harbour"]({bb});nwr["leisure"="slipway"]({bb});way["man_made"="pier"]({bb});way["man_made"="breakwater"]({bb});way["natural"="coastline"]({bb}););out geom tags;'
 f=P/'raw'/f'overpass-tile-{i}.json'
 if f.exists():return json.loads(f.read_text())
 for ep in ['https://overpass-api.de/api/interpreter','https://overpass.private.coffee/api/interpreter','https://maps.mail.ru/osm/tools/overpass/api/interpreter','https://overpass-api.de/api/interpreter']:
  try:
   u=ep;b=urllib.request.urlopen(urllib.request.Request(u,data=urllib.parse.urlencode({'data':q}).encode(),headers={'User-Agent':'oslofjord-bathavner/1.0'}),timeout=40).read();d=json.loads(b);assert 'elements' in d and 'remark' not in d;f.write_bytes(b)
   f.with_suffix('.provenance.json').write_text(json.dumps(dict(url=u,query=q,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(b).hexdigest()),indent=1));print(i,ep,len(d['elements']),flush=True);return d
  except Exception as ex:print(i,ep,str(ex)[:100],flush=True)
 raise RuntimeError(f'tile {i} failed')
with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:ds=list(ex.map(fetch,jobs))
a={}
for d in ds:
 for el in d['elements']:a[(el['type'],el['id'])]=el
out=dict(version=.6,elements=list(a.values()));(P/'raw/overpass-bamble.json').write_text(json.dumps(out));print('unique',len(a),flush=True)
for el in a.values():
 if el.get('tags',{}).get('leisure')=='marina':print(el['id'],el['tags'],flush=True)
