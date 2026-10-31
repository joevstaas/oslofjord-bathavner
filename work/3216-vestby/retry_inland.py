"""Fullstendig henting av sørøstre delrute via fire mindre GET-spørringer etter POST-tidsavbrudd."""
import json,urllib.request,urllib.parse,hashlib,datetime,concurrent.futures
from pathlib import Path
from shapely.geometry import shape
P=Path(__file__).parent;w,s,e,n=shape(json.loads((P/'raw/kommunegrense-4326.json').read_text())['omrade']).bounds
w=(w+e)/2;n=(s+n)/2;xm=(w+e)/2;ym=(s+n)/2
bbs=[(s,w,ym,xm),(s,xm,ym,e),(ym,w,n,xm),(ym,xm,n,e)]
def fetch(z):
 i,bb=z;fn=P/'raw'/f'overpass-inland-{i}.json'
 if fn.exists():return json.loads(fn.read_text())
 bb=','.join(map(str,bb));q=f'[out:json][timeout:15];(nwr["leisure"="marina"]({bb});nwr["mooring"]({bb});nwr["harbour"]({bb});nwr["leisure"="slipway"]({bb});way["man_made"="pier"]({bb});way["man_made"="breakwater"]({bb});way["natural"="coastline"]({bb}););out geom tags;'
 for ep in ['https://overpass-api.de/api/interpreter','https://maps.mail.ru/osm/tools/overpass/api/interpreter']:
  try:
   u=ep+'?'+urllib.parse.urlencode({'data':q});b=urllib.request.urlopen(u,timeout=25).read();d=json.loads(b);assert 'elements' in d and 'remark' not in d;fn.write_bytes(b);fn.with_suffix('.provenance.json').write_text(json.dumps(dict(url=u,query=q,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(b).hexdigest()),indent=1));print(i,len(d['elements']),flush=True);return d
  except Exception as ex:print(i,str(ex)[:90],flush=True)
 raise RuntimeError(i)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:ds=list(pool.map(fetch,enumerate(bbs)))
a={}
for d in ds:
 for el in d['elements']:a[(el['type'],el['id'])]=el
f=P/'raw/overpass-tile-1.json';f.write_text(json.dumps(dict(version=.6,elements=list(a.values()))));f.with_suffix('.provenance.json').write_text(json.dumps(dict(derived_from=[f'overpass-inland-{i}.json' for i in range(4)],method='deduplicate four complete spatial subqueries; same selectors',retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(f.read_bytes()).hexdigest()),indent=1));print('inland complete')
