"""Hent offentlig navnestøtte for nye detaljfunn; navneavstand er ikke operatørbevis."""
import requests,json,concurrent.futures,datetime,hashlib
from pathlib import Path
P=Path(__file__).parent;frames=json.loads((P/'detail-sweep-index.json').read_text())
def fetch(c):
 a,b,d,e=c['review_bbox'];r=requests.get('https://api.kartverket.no/stedsnavn/v1/punkt',params=dict(nord=(b+e)/2,ost=(a+d)/2,koordsys=25833,radius=400,utkoordsys=25833,treffPerSide=15),timeout=25);r.raise_for_status();return c['cid'],dict(url=r.url,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),response=r.json())
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:res=dict(ex.map(fetch,frames))
f=P/'raw/rereview-stedsnavn.json';f.write_text(json.dumps(res,ensure_ascii=False,indent=1))
(P/'raw/rereview-stedsnavn.provenance.json').write_text(json.dumps(dict(urls=[v['url'] for v in res.values()],retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(f.read_bytes()).hexdigest()),indent=1))
for k,v in res.items():print(k,[(a['stedsnavn'][0]['skrivemåte'],a.get('navneobjekttype'),a.get('meterFraPunkt')) for a in v['response'].get('navn',[])][:10])
