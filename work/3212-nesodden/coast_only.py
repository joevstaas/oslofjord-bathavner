from pathlib import Path
import json,urllib.request,urllib.parse,hashlib,datetime
P=Path(__file__).parent
q='[out:json][timeout:15];way["natural"="coastline"](59.72,10.54,59.89,10.75);out geom;'
for ep in ['https://overpass-api.de/api/interpreter','https://overpass.private.coffee/api/interpreter','https://overpass.kumi.systems/api/interpreter']:
 try:
  b=urllib.request.urlopen(urllib.request.Request(ep,data=urllib.parse.urlencode({'data':q}).encode()),timeout=25).read();d=json.loads(b);assert 'elements' in d and not d.get('remark');(P/'raw/coast-only.json').write_bytes(b);print('coast',len(d['elements']),flush=True);break
 except Exception as e:print(str(e),flush=True)
else:raise RuntimeError('coast failed')
(P/'raw/coast-only-provenance.json').write_text(json.dumps(dict(url=ep,query=q,sha256=hashlib.sha256(b).hexdigest(),retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=1))
# Temporary complete coastline seed for imagery planning, replaced with full candidate extract when obtained.
(P/'raw/overpass-nesodden.json').write_bytes(b)
