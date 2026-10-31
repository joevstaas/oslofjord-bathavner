"""Navnestøtte ved alle OSM-kandidater; ikke operatørbevis."""
import requests,json,datetime,hashlib,concurrent.futures
from pathlib import Path
P=Path(__file__).parent
cs=json.loads((P/'clusters.json').read_text());f=P/'raw/names.json';old=json.loads(f.read_text()) if f.exists() else {}
def fetch(c):
 if c['cid'] in old:return c['cid'],old[c['cid']]
 x,y=c['center'];r=requests.get('https://api.kartverket.no/stedsnavn/v1/punkt',params=dict(nord=y,ost=x,koordsys=25833,radius=350,utkoordsys=25833,treffPerSide=15),timeout=20);r.raise_for_status();return c['cid'],dict(url=r.url,response=r.json(),retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:res=dict(ex.map(fetch,cs))
f.write_text(json.dumps(res,ensure_ascii=False,indent=1));f.with_suffix('.provenance.json').write_text(json.dumps(dict(urls=[v['url'] for v in res.values()],sha256=hashlib.sha256(f.read_bytes()).hexdigest(),retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=1))
for k,v in res.items():print(k,[n['stedsnavn'][0]['skrivemåte'] for n in v['response']['navn']][:6])
