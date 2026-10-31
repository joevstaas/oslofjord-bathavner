import json,requests,datetime,hashlib,concurrent.futures
from pathlib import Path
P=Path(__file__).parent;cs=json.loads((P/'source-candidates.json').read_text())
def fetch(c):
 name=c['name'].replace(' marina','').replace(' båthavn','').replace(' båtforening','')
 if name in ['Sarpsborg','Vestjordets']:return c['id'],dict(name=c['name'],hits=[],note='Navnet krever kobling mot kommunerapportens bilde og kart; ikke adresse alene.')
 r=requests.get('https://api.kartverket.no/stedsnavn/v1/navn',params=dict(sok=name,knr='3105',utkoordsys=25833,treffPerSide=15),timeout=20);r.raise_for_status();return c['id'],dict(url=r.url,response=r.json())
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:res=dict(ex.map(fetch,cs))
f=P/'raw/source-names.json';f.write_text(json.dumps(res,ensure_ascii=False,indent=1));f.with_suffix('.provenance.json').write_text(json.dumps(dict(retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),urls=[v['url'] for v in res.values() if 'url' in v]),indent=1))
for k,v in res.items():print(k,[(a['skrivemåte'],a['representasjonspunkt']) for a in v.get('response',{}).get('navn',[])][:4])
