"""Fetch candidates and coastline for the entire municipality bounding box; save exact query and response."""
import datetime,json,pathlib,urllib.request,urllib.parse,hashlib
from shapely.geometry import shape
P=pathlib.Path(__file__).parent
b=shape(json.loads((P/'raw/kommunegrense-4326.json').read_text())['omrade']).bounds
west,south,east,north=b;bb=f'{south-0.002},{west-0.004},{north+0.002},{east+0.002}'
q=f'[out:json][timeout:35];(nwr["leisure"="marina"]({bb});nwr["mooring"]({bb});nwr["harbour"]({bb});nwr["leisure"="slipway"]({bb});way["man_made"="pier"]({bb});way["man_made"="breakwater"]({bb});way["natural"="coastline"]({bb}););out geom tags;'
(P/'raw/overpass-query.txt').write_text(q)
for endpoint in ['https://overpass-api.de/api/interpreter','https://overpass.private.coffee/api/interpreter']:
 try:
  data=urllib.parse.urlencode({'data':q}).encode();req=urllib.request.Request(endpoint,data=data,headers={'User-Agent':'oslofjord-bathavner/1.0 (public research)'})
  with urllib.request.urlopen(req,timeout=45) as r:raw=r.read()
  j=json.loads(raw);assert 'elements' in j
  (P/'raw/overpass-nordre-follo.json').write_bytes(raw)
  (P/'raw/overpass-provenance.json').write_text(json.dumps(dict(endpoint=endpoint,query=q,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(raw).hexdigest(),osm_base_timestamp=j.get('osm3s',{}).get('timestamp_osm_base')),indent=2));print('elements',len(j['elements']),flush=True)
  for e in j['elements']:
   t=e.get('tags',{});g=e.get('geometry',[]);p=g[len(g)//2] if g else e
   print(e['type'],e['id'],t.get('name',''),t.get('leisure') or t.get('man_made') or t.get('natural') or 'mooring',p.get('lat'),p.get('lon'),flush=True)
  break
 except Exception as e:print(endpoint,type(e).__name__,str(e),flush=True)
else:raise RuntimeError('No complete candidate extraction obtained')
