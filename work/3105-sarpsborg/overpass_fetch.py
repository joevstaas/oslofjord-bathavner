"""Begrenset GET-uttrekk med beskrivende User-Agent og eksplisitt proveniens. Ingen retry ved 429."""
import requests,json,hashlib,datetime,time
from pathlib import Path
P=Path(__file__).parent
q='[out:json][timeout:25];(way["natural"="coastline"](59.08,10.94,59.43,11.36);way["man_made"="pier"](59.08,10.94,59.43,11.36);way["man_made"="breakwater"](59.08,10.94,59.43,11.36);nwr["leisure"="marina"](59.08,10.94,59.43,11.36););out geom tags;'
for ep in ['https://overpass.private.coffee/api/interpreter','https://overpass-api.de/api/interpreter','https://maps.mail.ru/osm/tools/overpass/api/interpreter']:
 try:
  r=requests.get(ep,params={'data':q},headers={'User-Agent':'OslofjordBathavner/1.0 (public geographic research; https://github.com/joevstaas/oslofjord-bathavner)'},timeout=35)
  print(r.status_code,len(r.content),ep,flush=True)
  if r.status_code==429:continue
  r.raise_for_status();j=r.json();assert 'elements' in j and 'remark' not in j
  f=P/'raw/overpass-sarpsborg.json';f.write_bytes(r.content);(P/'raw/overpass-main.provenance.json').write_text(json.dumps(dict(url=r.url,query=q,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(r.content).hexdigest()),indent=1));print('unique',len(j['elements']),flush=True);break
 except Exception as e:print(type(e).__name__,str(e)[:160],flush=True)
else:raise RuntimeError('Ingen fullstendig Overpass-respons.')
